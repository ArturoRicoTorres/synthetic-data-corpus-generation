"""Lineage parsed from the reference SQL (sqlglot) matches the spec's transformation graph, node by node.

For every node, through sql/lineage_map.yaml:
  * every spec input is read by the node's SQL, and every spec output is created by it;
  * every column the SQL reads is a spec input, a join/context key, or a declared extra (with a reason).
"""
from functools import lru_cache

import pytest
import sqlglot
import yaml
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import traverse_scope

from conftest import ROOT, SQL_DIR

MAP = yaml.safe_load(open(ROOT / "sql" / "lineage_map.yaml", encoding="utf-8"))
NODES = MAP["nodes"]
KEYS = {k.upper() for k in MAP["keys"]}


def ddl_schema():
    schema = {}
    for stmt in sqlglot.parse((SQL_DIR / "00_schema.sql").read_text(encoding="utf-8"), read="duckdb"):
        if isinstance(stmt, exp.Create):
            cols = {c.name.lower(): "VARCHAR" for c in stmt.this.expressions if isinstance(c, exp.ColumnDef)}
            schema[stmt.this.this.name.lower()] = cols
    return schema


@lru_cache(maxsize=None)
def analysis():
    """Per SQL file: views created (with columns) and source columns read from objects outside the file."""
    schema, out = ddl_schema(), {}
    for path in sorted(SQL_DIR.glob("[0-9][0-9]_*.sql")):
        if path.name == "00_schema.sql":
            continue
        created, refs = {}, set()
        for stmt in sqlglot.parse(path.read_text(encoding="utf-8"), read="duckdb"):
            if not isinstance(stmt, exp.Create):
                continue
            view = stmt.this.name.lower()
            q = qualify(stmt.expression.copy(), schema=schema, dialect="duckdb", validate_qualify_columns=True)
            for scope in traverse_scope(q):
                for col in scope.columns:
                    src = scope.sources.get(col.table)
                    if isinstance(src, exp.Table):
                        refs.add((src.name.upper(), col.name.upper()))
            cols = [c.upper() for c in q.named_selects]
            schema[view] = {c.lower(): "VARCHAR" for c in cols}
            created[view.upper()] = set(cols)
        refs = {r for r in refs if r[0] not in created}       # reads of views created in the same file are internal
        out[path.name] = (created, refs)
    return out


def test_map_covers_every_spec_node(spec):
    spec_nodes = {t["id"]: t for t in spec["transformations"]}
    assert set(NODES) == set(spec_nodes)
    for nid, t in spec_nodes.items():
        assert set(NODES[nid]["inputs"]) == set(t["inputs"]), nid
        assert set(NODES[nid]["outputs"]) == set(t["outputs"]), nid
        assert (SQL_DIR / NODES[nid]["file"]).exists(), nid


def test_every_sql_file_maps_to_one_node():
    files = sorted(p.name for p in SQL_DIR.glob("[0-9][0-9]_*.sql") if p.name != "00_schema.sql")
    assert sorted(n["file"] for n in NODES.values()) == files


def split(ref):
    t, _, c = ref.rpartition(".")
    return t.upper(), c.upper()


@pytest.mark.parametrize("nid", sorted(NODES))
def test_node_lineage(nid):
    node = NODES[nid]
    created, refs = analysis()[node["file"]]
    read_tables = {t for t, _ in refs}
    allowed = set()
    # spec inputs are read
    for name, targets in node["inputs"].items():
        for target in targets:
            if node["compare"] == "table":
                assert target.upper() in read_tables, f"{nid}: input {name} -> {target} not read"
                allowed |= {r for r in refs if r[0] == target.upper()}
            else:
                assert split(target) in refs, f"{nid}: input {name} -> {target} not read"
                allowed.add(split(target))
    # spec outputs are created ("view" or "view.COLUMN")
    for name, targets in node["outputs"].items():
        for target in targets:
            if "." not in target:
                assert target.upper() in created, f"{nid}: output {name} -> {target} not created"
            else:
                v, c = split(target)
                assert v in created and c in created[v], f"{nid}: output {name} -> {target} not created"
    # every column read is explained
    extras = node.get("extras") or []
    for e in extras:
        t, c = split(e["sql"])
        matched = {r for r in refs if r[0] == t and (c == "*" or r[1] == c)}
        assert matched, f"{nid}: extra {e['sql']} is not read (stale entry)"
        allowed |= matched
    unexplained = sorted(f"{t}.{c}" for t, c in refs - allowed if c not in KEYS)
    assert not unexplained, f"{nid}: columns read but not in spec inputs, keys or extras: {unexplained}"


def test_keys_are_join_or_identifier_columns(spec):
    join_keys = {k for j in spec["joins"] for k in j["keys"]} | {
        v for j in spec["joins"] for v in (j.get("key_map") or {}).values()}
    ddl_pk = set()
    for stmt in sqlglot.parse((SQL_DIR / "00_schema.sql").read_text(encoding="utf-8"), read="duckdb"):
        for pk in stmt.find_all(exp.PrimaryKey):
            ddl_pk |= {c.name.upper() for c in pk.expressions}
    assert KEYS <= join_keys | ddl_pk, KEYS - (join_keys | ddl_pk)
