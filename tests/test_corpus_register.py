"""Register and glossary (decision D3): every citation resolves, every link lands, legal quotes are verbatim."""
import html
import json
import re

import pytest
import yaml

import render_corpus as rc
from conftest import ROOT

CORPUS = ROOT / "corpus"
REG = CORPUS / "shared" / "regulatory"
FILES = sorted(p for p in CORPUS.rglob("*") if p.is_file())
MD = [p for p in FILES if p.suffix == ".md"]


@pytest.fixture(scope="module")
def register():
    return yaml.safe_load((REG / "register.yaml").read_text(encoding="utf-8"))["documents"]


@pytest.fixture(scope="module")
def legal():
    return rc.load_legal()


@pytest.fixture(scope="module")
def entries(legal):
    return rc.register_entries(None, legal)


@pytest.mark.parametrize("path", FILES, ids=[p.relative_to(ROOT).as_posix() for p in FILES])
def test_every_citation_resolves_to_the_register(path, register, entries, legal):
    found, unresolved = rc.citations_in(path.read_text(encoding="utf-8"), entries, legal[0]["aliases"])
    assert not unresolved
    assert found <= set(register), found - set(register)
    if path.parent == REG and path.stem == "register":
        return          # the register lists every entry; it is not a citing document
    for reg in found:   # and the register says where it is cited
        assert path.relative_to(ROOT).as_posix() in register[reg]["cited_in"], reg


def anchors(path):
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r'<a id="([^"]+)"></a>', text))


@pytest.mark.parametrize("path", MD, ids=[p.relative_to(ROOT).as_posix() for p in MD])
def test_markdown_links_resolve(path):
    for target in re.findall(r"\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
        if target.startswith("http"):
            continue
        file, _, frag = target.partition("#")
        dest = (path.parent / file).resolve() if file else path
        assert dest.exists(), target
        if frag and dest.name in ("glossary.md", "register.md", "bird_transformation_rules.md",
                                  "bird_definitions.md", "annex_v_extracts.md"):
            assert frag in anchors(dest), target


def test_oi14_register_entries(register):
    old = register["REG_EU_680_2014"]
    assert old["replaced_by"] == "REG_EU_2021_451" and old["status"].startswith("Repealed")
    assert "Article 22" in old["status"]
    # BIRD wording is kept verbatim: definitions still cite 680/2014 (decision OI-14, option A)
    assert "680/2014" in (REG / "bird_definitions.md").read_text(encoding="utf-8")
    assert "REG_EU_2021_451" in register and register["REG_EU_2021_451"]["sha256"]


def test_register_hashes_match_sources(register, legal):
    import hashlib
    assert register["REG_EU_2021_451"]["sha256"] == hashlib.sha256(legal[1].read_bytes()).hexdigest()
    assert register["BIRD_FINREP_4_3"]["sha256"] == rc.bird_export.zip_sha256()


def glossary_blocks():
    text = (REG / "glossary.md").read_text(encoding="utf-8")
    return re.findall(r"^### (.+?)\n(.*?)(?=^### |\Z)", text, flags=re.M | re.S)


def test_every_glossary_entry_links_to_the_register():
    blocks = glossary_blocks()
    assert len(blocks) > 50
    for name, body in blocks:
        assert "](register.md#" in body, name


def test_business_names_used_are_in_the_glossary():
    names = {n.split(":")[0].strip().lower() for n, _ in glossary_blocks()}
    assets = json.loads((CORPUS / "s1_rich" / "metadata" / "collibra_import.json").read_text(encoding="utf-8"))
    used = {a["identifier"]["name"].lower() for a in assets if a["type"]["name"] in ("Business Term", "Code Value")}
    used |= {a["displayName"].lower() for a in assets if a["type"]["name"] == "Table"}
    chain = yaml.safe_load((ROOT / "src" / "corpus_text" / "reporting_chain.yaml").read_text(encoding="utf-8"))
    used |= {t.lower() for s in chain["sections"].values() for t in s["terms"]}
    assert used <= names, sorted(used - names)


def test_annex_v_extracts_are_verbatim(legal):
    _, src, _, _ = legal
    flat = rc.normalise(html.unescape(re.sub(r"<[^>]+>", "", src.read_text(encoding="utf-8"))))
    text = (REG / "annex_v_extracts.md").read_text(encoding="utf-8")
    quotes = re.findall(r"^## Part \d+, paragraph \d+.*?\n\n((?:>.*\n?)+)", text, flags=re.M)
    assert len(quotes) == len(legal[0]["extracts"])
    for q in quotes:
        body = rc.normalise(" ".join(ln[1:].strip() for ln in q.splitlines() if ln.strip() != ">"))
        assert body in flat, body[:80]


def test_bird_rules_are_verbatim():
    text = (REG / "bird_transformation_rules.md").read_text(encoding="utf-8")
    for rid in rc.ROUTINES:
        assert rc.bird_export.algorithm(rid) in text, rid
