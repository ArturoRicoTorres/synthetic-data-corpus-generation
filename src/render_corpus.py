"""
Render the classifier corpus and its answer key from the spec, the reference SQL and the official sources.

    python src/render_corpus.py [--seed 42] [--out .]

Writes
  corpus/s1_rich/             SQL (T-SQL, with comments), client metadata, data-model docs, reporting chain
  corpus/s2_limited/          SQL (no comments), sparse client metadata, short data-model overview
  corpus/s3_regulatory_only/  SQL (no comments)
  corpus/shared/regulatory/   regulatory documents, register and glossary (all scenarios)
  answer_key/                 everything that maps the corpus back to the spec; never shown to the classifier

Everything is generated; never edit corpus/ or answer_key/ by hand. Decisions: D1-D7 and OI-14 in decisions.md.
"""
import argparse
import re
import shutil
from pathlib import Path

import sqlglot
import yaml
from sqlglot import exp

import bird_export

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "specs" / "npl_ratio_lineage_spec_v0.2.yaml"
REF_SQL = ROOT / "sql" / "reference"
LINEAGE_MAP = ROOT / "sql" / "lineage_map.yaml"
TEXT_DIR = Path(__file__).resolve().parent / "corpus_text"

SCENARIOS = ["s1_rich", "s2_limited", "s3_regulatory_only"]
VARCHAR = "VARCHAR(255)"          # member ids are longer than the BIRD code lengths, so one length for all text
CONTEXT_TYPES = {"dt_rfrnc": "DATE"}
GO = "GO"


# ---------------------------------------------------------------- helpers
def load_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def dump_yaml(data):
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)


def wrap(text, width=110, prefix=""):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(prefix) + len(cur) + 1 + len(w) > width:
            lines.append(prefix + cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(prefix + cur)
    return lines


# ---------------------------------------------------------------- SQL (decisions D2, D5)
def reference_files():
    return sorted(REF_SQL.glob("[0-9][0-9]_*.sql"))


def to_tsql_ast(stmt):
    """DuckDB reference statement -> statement ready for T-SQL output."""
    stmt = stmt.copy()
    for fn in list(stmt.find_all(exp.Anonymous)):
        if fn.name.lower() == "getvariable":
            key = fn.expressions[0].name
            fn.replace(exp.Cast(this=exp.Anonymous(this="SESSION_CONTEXT", expressions=[exp.National(this=key)]),
                                to=exp.DataType.build(CONTEXT_TYPES.get(key, VARCHAR), dialect="tsql")))
    for div in stmt.find_all(exp.Div):      # decimal / decimal: no FLOAT cast (it would lose precision)
        div.set("typed", True)
    for dt in list(stmt.find_all(exp.DataType)):
        if dt.this in (exp.DataType.Type.TEXT, exp.DataType.Type.VARCHAR) and not dt.expressions:
            dt.replace(exp.DataType.build(VARCHAR, dialect="tsql"))
    return stmt


def created_columns(stmt):
    """(object name, [columns]) for a CREATE VIEW / CREATE TABLE statement."""
    if not isinstance(stmt, exp.Create):
        return None
    if stmt.args.get("kind") == "TABLE":
        return stmt.this.this.name, [c.name for c in stmt.this.expressions if isinstance(c, exp.ColumnDef)]
    return stmt.this.name, list(stmt.expression.named_selects)


def sql_header(fname, created, texts, keys):
    """s1 header comment: purpose, official routines, created objects and their columns."""
    spec_txt = texts["files"][fname]
    var = bird_export.indexed("variable", "VARIABLE_ID")
    lines = ["/*", f"File: {fname}"]
    lines += wrap("Purpose: " + spec_txt["purpose"], prefix="")
    if spec_txt["routines"]:
        lines += wrap("Follows the official BIRD routine(s): " + ", ".join(spec_txt["routines"]))
    lines.append("Creates:")
    for obj, cols in created:
        lines.append(f"  {obj}")
        for c in cols:
            if c.upper() in keys:
                continue
            name = texts["columns"].get(c.upper()) or (var.NAME.get(c.upper()) if c.upper() in var.index else None)
            lines.append(f"    {c:<40} {name}" if name else f"    {c}")
    lines.append("*/")
    return "\n".join(lines)


def render_sql(out):
    texts = load_yaml(TEXT_DIR / "sql_comments.yaml")
    keys = {k.upper() for k in load_yaml(LINEAGE_MAP)["keys"]}
    objects = {}
    for path in reference_files():
        stmts = [s for s in sqlglot.parse(path.read_text(encoding="utf-8"), read="duckdb") if s is not None]
        tstmts = [to_tsql_ast(s) for s in stmts]
        created = [c for c in (created_columns(s) for s in tstmts) if c]
        objects[path.name] = [o for o, _ in created]
        for scen in SCENARIOS:
            with_comments = scen == "s1_rich"
            body = f"\n{GO}\n\n".join(
                s.sql(dialect="tsql", pretty=True, comments=with_comments,
                      unsupported_level=sqlglot.ErrorLevel.RAISE) for s in tstmts)
            text = (sql_header(path.name, created, texts, keys) + "\n\n" if with_comments else "") + body + f"\n{GO}\n"
            write(out / "corpus" / scen / "sql" / path.name, text)
    return objects


def tsql_statements(text):
    """Split a corpus T-SQL file on GO lines and parse each batch."""
    batches = [b for b in re.split(r"^\s*GO\s*$", text, flags=re.MULTILINE | re.IGNORECASE) if b.strip()]
    return [sqlglot.parse_one(b, read="tsql", error_level=sqlglot.ErrorLevel.RAISE) for b in batches]


def tsql_to_duckdb(text):
    """Corpus T-SQL -> DuckDB SQL (used to prove the corpus SQL gives the reference cells)."""
    out = []
    for stmt in tsql_statements(text):
        for fn in list(stmt.find_all(exp.Anonymous)):
            if fn.name.upper() == "SESSION_CONTEXT":
                fn.replace(exp.Anonymous(this="getvariable", expressions=[exp.Literal.string(fn.expressions[0].name)]))
        for pk in stmt.find_all(exp.PrimaryKey):          # T-SQL key columns parse as ordered expressions
            for o in list(pk.find_all(exp.Ordered)):
                o.replace(o.this)
        out.append(stmt.sql(dialect="duckdb", comments=False) + ";")
    return "\n".join(out) + "\n"


def sql_object_map(objects):
    lmap = load_yaml(LINEAGE_MAP)
    by_file = {n["file"]: nid for nid, n in lmap["nodes"].items()}
    return {
        "note": "Corpus SQL object -> spec node. Object names equal the reference SQL (decision D2); the per-node "
                "column mapping is sql/lineage_map.yaml.",
        "dialect": "tsql",
        "scenarios": {s: f"corpus/{s}/sql/" for s in SCENARIOS},
        "files": {f: {"node": by_file.get(f), "creates": objs} for f, objs in objects.items()},
    }


# ---------------------------------------------------------------- main
def render(out=ROOT, seed=42):
    out = Path(out)
    for d in (out / "corpus", out / "answer_key"):
        if d.exists():
            shutil.rmtree(d)
    objects = render_sql(out)
    write(out / "answer_key" / "sql_object_map.yaml", dump_yaml(sql_object_map(objects)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default=str(ROOT))
    a = ap.parse_args()
    render(Path(a.out), a.seed)
    print(f"rendered corpus/ and answer_key/ under {a.out}")
