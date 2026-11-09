"""The input-layer DDL matches the spec (attributes and join keys), and the input data checks hold."""
import pandas as pd
import pytest
import sqlglot
from sqlglot import exp

import run_reference_sql
from conftest import SQL_DIR

CTX = {"DT_RFRNC", "RPRTNG_AGNT_ID", "ACCNTNG_CNSLDTN_LVL", "ACCNTNG_STNDRD"}


def ddl():
    out = {}
    for stmt in sqlglot.parse((SQL_DIR / "00_schema.sql").read_text(encoding="utf-8"), read="duckdb"):
        if isinstance(stmt, exp.Create):
            out[stmt.this.this.name.upper()] = {c.name.upper() for c in stmt.this.expressions
                                                if isinstance(c, exp.ColumnDef)}
    return out


def spec_columns(spec):
    cols = {}
    for a in spec["attributes"]:
        if a["table"].endswith("_IL"):
            cols.setdefault(a["table"], set()).add(a["column"])
    for j in spec["joins"]:
        km = j.get("key_map") or {}
        if j["parent"] in cols:
            cols[j["parent"]] |= set(j["keys"])
        if j["child"] in cols:
            cols[j["child"]] |= {km.get(k, k) for k in j["keys"]}
    return {t: c | CTX for t, c in cols.items()}


def test_ddl_tables_match_spec(spec):
    assert set(ddl()) == set(spec_columns(spec))


def test_ddl_columns_match_spec(spec):
    d, s = ddl(), spec_columns(spec)
    for t in s:
        assert d[t] == s[t], f"{t}: only in DDL {d[t] - s[t]}, only in spec {s[t] - d[t]}"


def test_reporting_scheme_gate_is_unique_per_context(synthetic, tmp_path):
    data = synthetic(42)
    grp = pd.read_csv(data / "INTRNL_GRP_RL_IL.csv", dtype=str)
    assert not grp[grp.GRP_RL_TYP == "GRP_RL_TYP_1"].duplicated(sorted(CTX)).any()
    # a second group role row for the same context is rejected
    for f in data.iterdir():
        (tmp_path / f.name).write_bytes(f.read_bytes())
    dup = pd.concat([grp, grp.iloc[[0]].assign(GRP_ID="GRP-OTHER")])
    dup.to_csv(tmp_path / "INTRNL_GRP_RL_IL.csv", index=False)
    with pytest.raises(ValueError, match="GRP_RL_TYP_1"):
        run_reference_sql.build(tmp_path)
