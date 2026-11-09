"""
Run the reference SQL (sql/reference/*.sql) in DuckDB on a directory of input-layer CSV files.

    python src/run_reference_sql.py [--data data/synthetic]

The data directory holds one CSV per input table (named <TABLE>.csv) and contexts.csv, which lists the
reporting contexts to evaluate (name, DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD).
"""
import argparse
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = ROOT / "sql" / "reference"
SCHEMA = SQL_DIR / "00_schema.sql"


def node_files():
    """SQL files after the schema, in execution order."""
    return sorted(p for p in SQL_DIR.glob("[0-9][0-9]_*.sql") if p.name != SCHEMA.name)


def input_tables(con):
    return [r[0] for r in con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' ORDER BY 1").fetchall()]


def build(data_dir):
    """Create an in-memory database: schema, input data from CSV, and all views."""
    con = duckdb.connect(":memory:")
    con.execute(SCHEMA.read_text(encoding="utf-8"))
    for table in input_tables(con):
        f = Path(data_dir) / f"{table}.csv"
        if f.exists():
            con.execute(f"INSERT INTO {table} BY NAME "
                        f"SELECT * FROM read_csv(?, header = true, all_varchar = true, nullstr = '')", [str(f)])
    check_inputs(con)
    for f in node_files():
        con.execute(f.read_text(encoding="utf-8"))
    return con


def check_inputs(con):
    """Data checks the reference SQL relies on. Raises ValueError on violation."""
    dup = con.execute("""
        SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, COUNT(*) AS n
        FROM INTRNL_GRP_RL_IL WHERE GRP_RL_TYP = 'GRP_RL_TYP_1'
        GROUP BY ALL HAVING COUNT(*) > 1""").fetchall()
    if dup:   # decision OI-13: exactly one reporting-agent group role per reporting context
        raise ValueError(f"more than one GRP_RL_TYP_1 row per reporting context: {dup}")


def set_context(con, ctx):
    con.execute("SET VARIABLE dt_rfrnc = ?::DATE", [str(ctx["DT_RFRNC"])])
    for k in ("RPRTNG_AGNT_ID", "ACCNTNG_CNSLDTN_LVL", "ACCNTNG_STNDRD"):
        con.execute(f"SET VARIABLE {k.lower()} = ?", [ctx[k]])
    n = con.execute("SELECT COUNT(*) FROM intrnl_grp_rl_il_snp WHERE GRP_RL_TYP = 'GRP_RL_TYP_1'").fetchone()[0]
    if n != 1:   # decision OI-13: the evaluated context has exactly one reporting-agent group role
        raise ValueError(f"context {ctx.get('name', ctx)} has {n} GRP_RL_TYP_1 rows, expected exactly 1")


def cells(con):
    c0010 = con.execute("SELECT GRSS_CRRYNG_AMNT FROM f_18_00_a_r0070_c0010").fetchone()[0]
    c0060 = con.execute("SELECT GRSS_CRRYNG_AMNT FROM f_18_00_a_r0070_c0060").fetchone()[0]
    ratio = con.execute("SELECT NPL_RATIO FROM npl_ratio").fetchone()[0]
    return {"C0010": c0010, "C0060": c0060, "NPL_RATIO": ratio}


def row_assignments(con):
    """One record per (position, sector row) in row 0070, with its gross carrying amount."""
    return con.execute("""
        SELECT PSTN_SRC, PSTN_ID, SRC_RW, GRSS_CRRYNG_AMNT, PRFRMNG_STTS, DBT_SCRTY_PRFRMNG_STTS_TYP
        FROM f_18_00_a_r0070 ORDER BY PSTN_SRC, PSTN_ID, SRC_RW""").df()


def gross_carrying_amounts(con):
    """Derived gross carrying amount per position, before any template filter."""
    return con.execute("""
        SELECT 'INSTRMNT' AS PSTN_SRC, INSTRMNT_ID AS PSTN_ID, GRSS_CRRYNG_AMNT FROM instrmnt_rl_eil_grss_crryng_amnt
        UNION ALL
        SELECT 'SCRTY_PSTN', SCRTY_ID, GRSS_CRRYNG_AMNT FROM lng_scrty_pstn_eil_grss_crryng_amnt""").df()


def contexts(data_dir):
    return pd.read_csv(Path(data_dir) / "contexts.csv", dtype=str).to_dict("records")


def run(data_dir):
    """Cells per context: {context name: {C0010, C0060, NPL_RATIO}}."""
    con = build(data_dir)
    out = {}
    for ctx in contexts(data_dir):
        set_context(con, ctx)
        out[ctx["name"]] = cells(con)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "data" / "synthetic"))
    a = ap.parse_args()
    for name, c in run(a.data).items():
        print(f"{name:10s} C0010={c['C0010']}  C0060={c['C0060']}  NPL_RATIO={c['NPL_RATIO']}")
