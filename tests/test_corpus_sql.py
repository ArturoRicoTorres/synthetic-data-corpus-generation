"""Corpus SQL (T-SQL, decision D5): valid T-SQL, same logic in every scenario, and the reference cells exactly."""
import re

import pytest

import render_corpus
import run_reference_sql
from conftest import ROOT, SQL_DIR

CORPUS = ROOT / "corpus"
SCENARIOS = render_corpus.SCENARIOS
FILES = sorted(p.name for p in SQL_DIR.glob("[0-9][0-9]_*.sql"))


def corpus_file(scen, name):
    return CORPUS / scen / "sql" / name


def test_every_scenario_has_every_file():
    for scen in SCENARIOS:
        assert sorted(p.name for p in (CORPUS / scen / "sql").glob("*.sql")) == FILES, scen


@pytest.mark.parametrize("scen", SCENARIOS)
def test_files_parse_as_tsql(scen):
    for name in FILES:
        stmts = render_corpus.tsql_statements(corpus_file(scen, name).read_text(encoding="utf-8"))
        assert stmts, name


@pytest.mark.parametrize("scen", SCENARIOS)
def test_no_duckdb_only_constructs(scen):
    bad = [r"getvariable", r"CREATE\s+OR\s+REPLACE", r"\bVARCHAR\b(?!\s*\()", r"\bTEXT\b", r"::", r"GROUP\s+BY\s+ALL"]
    for name in FILES:
        text = corpus_file(scen, name).read_text(encoding="utf-8")
        code = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        hits = [p for p in bad if re.search(p, code, re.I)]
        assert not hits, f"{scen}/{name}: {hits}"


@pytest.mark.parametrize("scen", SCENARIOS)
def test_one_create_per_batch(scen):
    """T-SQL requires CREATE VIEW to be the only statement in its batch, so batches are separated by GO."""
    for name in FILES:
        text = corpus_file(scen, name).read_text(encoding="utf-8")
        batches = [b for b in re.split(r"^\s*GO\s*$", text, flags=re.M) if b.strip()]
        for b in batches:
            assert len(re.findall(r"\bCREATE\b", re.sub(r"/\*.*?\*/", "", b, flags=re.S))) == 1, name


def test_comments_only_in_rich_scenario():
    for name in FILES:
        assert "/*" in corpus_file("s1_rich", name).read_text(encoding="utf-8"), name
        for scen in ("s2_limited", "s3_regulatory_only"):
            text = corpus_file(scen, name).read_text(encoding="utf-8")
            assert "/*" not in text and "--" not in text, f"{scen}/{name}"


def test_scenarios_have_the_same_logic():
    for name in FILES:
        asts = {scen: [s.sql(dialect="tsql", comments=False) for s in render_corpus.tsql_statements(
            corpus_file(scen, name).read_text(encoding="utf-8"))] for scen in SCENARIOS}
        assert asts["s1_rich"] == asts["s2_limited"] == asts["s3_regulatory_only"], name


def test_corpus_sql_gives_the_reference_cells(synthetic, tmp_path):
    """Round trip T-SQL -> DuckDB; cells and ratio equal the reference SQL exactly (seed 42)."""
    for name in FILES:
        text = corpus_file("s1_rich", name).read_text(encoding="utf-8")
        (tmp_path / name).write_text(render_corpus.tsql_to_duckdb(text), encoding="utf-8")
    data = synthetic(42)
    corpus, reference = run_reference_sql.run(data, tmp_path), run_reference_sql.run(data)
    assert corpus == reference
    assert corpus["IFRS"]["C0010"] > 0
