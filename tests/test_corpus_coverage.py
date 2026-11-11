"""Scenario contents, metadata coverage, the s2 subset, and that the committed corpus is the deterministic render."""
import filecmp
import json

import yaml

import render_corpus as rc
from conftest import ROOT

CORPUS = ROOT / "corpus"


def assets(scen):
    return json.loads((CORPUS / scen / "metadata" / "collibra_import.json").read_text(encoding="utf-8"))


def test_scenario_layout():
    top = lambda s: sorted(p.name for p in (CORPUS / s).iterdir())  # noqa: E731
    assert top("s1_rich") == ["docs", "metadata", "sql"]
    assert top("s2_limited") == ["docs", "metadata", "sql"]
    assert top("s3_regulatory_only") == ["sql"]
    assert sorted(p.name for p in (CORPUS / "s1_rich" / "docs").iterdir()) == ["data_model", "reporting_chain.md"]
    assert sorted(p.name for p in (CORPUS / "s2_limited" / "docs").iterdir()) == ["overview.md"]


def test_s1_metadata_covers_every_spec_attribute_and_table(spec):
    names = {a["identifier"]["name"] for a in assets("s1_rich")}
    cols = {n.split(".", 2)[2] for n in names if n.count(".") == 3}          # TABLE.COLUMN
    columns_any = {c.split(".")[1] for c in cols}
    for a in spec["attributes"]:
        if a["table"].endswith("_IL"):
            assert f"{a['table']}.{a['column']}" in cols, a["id"]
        else:                                   # derived attributes live on the enriched-layer views
            assert a["column"] in columns_any, a["id"]
    tables = {a["table"] for a in spec["attributes"] if a["table"].endswith("_IL")}
    assert {f"{rc.DATABASE}.{rc.SCHEMA}.{t}" for t in tables} <= names


def test_s2_is_a_strict_subset_of_s1():
    key = lambda a: (a["identifier"]["name"], a["identifier"]["domain"]["name"])  # noqa: E731
    s1 = {key(a): a for a in assets("s1_rich")}
    s2 = {key(a): a for a in assets("s2_limited")}
    assert set(s2) < set(s1)
    for name, a in s2.items():
        for k, v in a.get("attributes", {}).items():
            assert s1[name]["attributes"][k] == v, (name, k)
        for k, v in a.get("relations", {}).items():
            assert all(r in s1[name]["relations"][k] for r in v), (name, k)
    rules = yaml.safe_load((ROOT / "answer_key" / "s2_subset.yaml").read_text(encoding="utf-8"))
    kept = {n for n, _ in s2 if s2[(n, _)]["type"]["name"] == "Column"}
    assert kept == set(rules["kept_columns"])
    assert not [a for a in s2.values() if a["type"]["name"] in ("Code Set", "Code Value")]


def test_reporting_chain_has_one_section_per_spec_node(spec):
    prov = yaml.safe_load((ROOT / "answer_key" / "provenance.yaml").read_text(encoding="utf-8"))["documents"]
    steps = {k: v for k, v in prov.items() if k.startswith("corpus/s1_rich/docs/reporting_chain.md#step-")}
    assert sorted(v["node"] for v in steps.values()) == sorted(t["id"] for t in spec["transformations"])
    text = (CORPUS / "s1_rich" / "docs" / "reporting_chain.md").read_text(encoding="utf-8")
    assert text.count("\n## Step ") == len(spec["transformations"])


def test_every_metadata_asset_has_provenance():
    prov = yaml.safe_load((ROOT / "answer_key" / "provenance.yaml").read_text(encoding="utf-8"))["metadata"]
    for a in assets("s1_rich"):
        assert a["identifier"]["name"] in prov
    assert {p["provenance"] for p in prov.values()} <= {"bird_official", "gap_fill"}


def same_tree(a, b):
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only:
        return False
    _, mismatch, errors = filecmp.cmpfiles(a, b, cmp.common_files, shallow=False)
    return not mismatch and not errors and all(same_tree(a / d, b / d) for d in cmp.common_dirs)


def test_committed_corpus_is_the_deterministic_render(tmp_path):
    """Two renders with seed 42 are byte-identical, and equal what is in the repository (no hand edits)."""
    rc.render(tmp_path / "a", seed=42)
    rc.render(tmp_path / "b", seed=42)
    for d in ("corpus", "answer_key"):
        assert same_tree(tmp_path / "a" / d, tmp_path / "b" / d), d
        assert same_tree(tmp_path / "a" / d, ROOT / d), f"{d}/ is stale: rerun python src/render_corpus.py"
