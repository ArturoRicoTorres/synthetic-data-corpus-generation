"""Every named edge case lands in the expected sector rows and cells, in the SQL and in the independent check."""
from decimal import Decimal

import pandas as pd
import pytest

import reference_calc
import run_reference_sql


def dec(x):
    return None if x is None or (isinstance(x, float) and pd.isna(x)) or x == "" else Decimal(str(x)).quantize(
        Decimal("0.01"))


@pytest.fixture(scope="module")
def outcomes(synthetic):
    """Per context: SQL row records, SQL gross carrying amounts, independent row records."""
    data = synthetic(42)
    con = run_reference_sql.build(data)
    py_data, consts = reference_calc.load(data), reference_calc.spec_constants()
    out = {}
    for ctx in run_reference_sql.contexts(data):
        run_reference_sql.set_context(con, ctx)
        out[ctx["name"]] = {"sql_rows": run_reference_sql.row_assignments(con),
                            "sql_gca": run_reference_sql.gross_carrying_amounts(con),
                            "py_rows": pd.DataFrame(reference_calc.r0070(py_data, ctx, consts),
                                                    columns=["PSTN_SRC", "PSTN_ID", "RW", "GRSS_CRRYNG_AMNT", "NP"])}
    return out


def expected_cases():
    import generate_synthetic
    b = generate_synthetic.Book()
    generate_synthetic.edge_cases(b)
    return b.cases


CASES = expected_cases()


def contribution(gca, rows, np_flag):
    in_c0010 = bool(rows) and gca is not None and gca > 0
    return in_c0010, in_c0010 and np_flag


@pytest.mark.parametrize("case", CASES, ids=[c["case_id"] for c in CASES])
def test_case_sql(outcomes, case):
    o = outcomes[case["ctx"]]
    r = o["sql_rows"][(o["sql_rows"].PSTN_SRC == case["pstn_src"]) & (o["sql_rows"].PSTN_ID == case["pstn_id"])]
    assert ";".join(sorted(r.SRC_RW)) == case["rows"], case["note"]
    g = o["sql_gca"][(o["sql_gca"].PSTN_SRC == case["pstn_src"]) & (o["sql_gca"].PSTN_ID == case["pstn_id"])]
    got_gca = dec(g.GRSS_CRRYNG_AMNT.iloc[0]) if len(g) else None
    assert got_gca == dec(case["gca"]), case["note"]
    np_flag = bool(((r.PRFRMNG_STTS == "CRDT_QLTY_1") | (r.DBT_SCRTY_PRFRMNG_STTS_TYP == "SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20")).any())
    assert contribution(got_gca, len(r), np_flag) == (bool(case["c0010"]), bool(case["c0060"])), case["note"]


@pytest.mark.parametrize("case", CASES, ids=[c["case_id"] for c in CASES])
def test_case_independent(outcomes, case):
    o = outcomes[case["ctx"]]
    r = o["py_rows"][(o["py_rows"].PSTN_SRC == case["pstn_src"]) & (o["py_rows"].PSTN_ID == case["pstn_id"])]
    assert ";".join(sorted(r.RW)) == case["rows"], case["note"]
    if len(r):   # the independent check derives amounts only for positions inside the cell
        gca = dec(r.GRSS_CRRYNG_AMNT.iloc[0])
        assert gca == dec(case["gca"]), case["note"]
        assert contribution(gca, len(r), bool(r.NP.any())) == (bool(case["c0010"]), bool(case["c0060"])), case["note"]


def test_cases_cover_every_branch():
    rows = {r for c in CASES for r in c["rows"].split(";") if r}
    assert rows == {"R0080", "R0090", "R0100", "R0110", "R0120", "R0150"}
    assert any(c["c0060"] for c in CASES) and any(c["c0010"] and not c["c0060"] for c in CASES)
    assert {c["ctx"] for c in CASES} == {"IFRS", "NGAAP", "SCHEME4"}
    assert {c["pstn_src"] for c in CASES} == {"INSTRMNT", "SCRTY_PSTN"}
