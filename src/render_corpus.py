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


def describe_create(stmt, fname):
    """Object created by a CREATE TABLE / CREATE VIEW statement: name, kind, columns, types, keys, sources."""
    if not isinstance(stmt, exp.Create):
        return None
    if stmt.args.get("kind") == "TABLE":
        defs = [c for c in stmt.this.expressions if isinstance(c, exp.ColumnDef)]
        keys = [e.this.name if isinstance(e, exp.Ordered) else e.name
                for pk in stmt.find_all(exp.PrimaryKey) for e in pk.expressions]
        return {"name": stmt.this.this.name, "kind": "TABLE", "file": fname, "columns": [c.name for c in defs],
                "types": {c.name: c.args["kind"].sql(dialect="tsql") for c in defs}, "keys": keys, "sources": []}
    name = stmt.this.name
    sources = sorted({t.name for t in stmt.expression.find_all(exp.Table)} - {name})
    return {"name": name, "kind": "VIEW", "file": fname, "columns": list(stmt.expression.named_selects),
            "types": {}, "keys": [], "sources": sources}


def sql_header(fname, created, texts, keys):
    """s1 header comment: purpose, official routines, created objects and their columns."""
    spec_txt = texts["files"][fname]
    var = bird_export.indexed("variable", "VARIABLE_ID")
    lines = ["/*", f"File: {fname}"]
    lines += wrap("Purpose: " + spec_txt["purpose"], prefix="")
    if spec_txt["routines"]:
        lines += wrap("Follows the official BIRD routine(s): " + ", ".join(spec_txt["routines"]))
    lines.append("Creates:")
    for o in created:
        lines.append(f"  {o['name']}")
        for c in o["columns"]:
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
        created = [c for c in (describe_create(s, path.name) for s in tstmts) if c]
        objects[path.name] = created
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
        "files": {f: {"node": by_file.get(f), "creates": [o["name"] for o in objs]} for f, objs in objects.items()},
    }


# ---------------------------------------------------------------- shared model of the corpus vocabulary
class Model:
    """Tables, views, columns, BIRD variables, members and legal references used by the corpus."""

    def __init__(self, objects):
        self.objects = [o for objs in objects.values() for o in objs]
        self.tables = [o for o in self.objects if o["kind"] == "TABLE"]
        self.views = [o for o in self.objects if o["kind"] == "VIEW"]
        self.var = bird_export.indexed("variable", "VARIABLE_ID")
        self.mem = bird_export.indexed("member", "MEMBER_ID")
        self.dom = bird_export.indexed("domain", "DOMAIN_ID")
        self.cube = bird_export.indexed("cube", "CUBE_ID")
        self.legal_text = bird_export.indexed("legal_text", "LEGAL_TEXT_ID")
        self.spec = load_yaml(SPEC_PATH)
        self.texts = load_yaml(TEXT_DIR / "sql_comments.yaml")
        self.keys = {k.upper() for k in load_yaml(LINEAGE_MAP)["keys"]}
        lmap = load_yaml(LINEAGE_MAP)
        self.node_of_file = {n["file"]: nid for nid, n in lmap["nodes"].items()}
        self.attr = {(a["table"], a["column"]): a for a in self.spec["attributes"]}
        cols = {c.upper() for o in self.objects for c in o["columns"]}
        self.variables = sorted(c for c in cols if c in self.var.index)
        literals = set()
        for p in reference_files():
            literals |= set(re.findall(r"'([A-Za-z0-9_]+)'", p.read_text(encoding="utf-8")))
        self.members = sorted(m for m in literals if m in self.mem.index)
        self.domains = sorted({self.var.DOMAIN_ID[v] for v in self.variables
                               if self.dom.IS_ENUMERATED.get(self.var.DOMAIN_ID[v]) == "true"})
        self.type_of = {c: t for o in self.tables for c, t in o["types"].items()}

    def domain_of(self, column):
        d = self.var.DOMAIN_ID.get(column.upper()) if column.upper() in self.var.index else None
        return d if d in self.domains else None

    def members_of(self, domain):
        return [m for m in self.members if self.mem.DOMAIN_ID[m] == domain]

    def column_text(self, table, column):
        """(business name, definition, provenance, source) of a column."""
        c = column.upper()
        a = self.attr.get((table, c))
        if a and a.get("business_definition"):
            return a["business_name"], a["business_definition"], "bird_official", f"spec attribute {table}.{c}"
        if c in self.var.index:
            return self.var.NAME[c], self.var.DESCRIPTION[c], "bird_official", f"variable.csv {c}"
        if c in self.texts["columns"]:
            return self.texts["columns"][c], None, "gap_fill", "src/corpus_text/sql_comments.yaml"
        return None, None, None, None

    def legal_refs(self, object_type, object_id):
        """[(register id, article)] for an export object, verbatim from legal_reference.csv."""
        lr = bird_export.read("legal_reference")
        hits = lr[(lr.OBJECT_TYPE == object_type) & (lr.OBJECT_ID == object_id)]
        return [(self.legal_text.LEGAL_CODE[r.LEGAL_TEXT_ID], r.ARTICLE) for r in hits.itertuples()]

    def node_of(self, obj):
        return self.node_of_file.get(obj["file"])


# ---------------------------------------------------------------- Collibra-style metadata (s1 full, s2 subset)
COMMUNITY = "Regulatory Reporting"
DOM_PHYSICAL = "Reporting Data Mart"
DOM_GLOSSARY = "Regulatory Business Glossary"
DOM_CODES = "Regulatory Code Lists"
DATABASE, SCHEMA = "REPORTING_DM", "dbo"


def asset(name, domain, typ, display=None, attributes=None, relations=None):
    a = {"resourceType": "Asset",
         "identifier": {"name": name, "domain": {"name": domain, "community": {"name": COMMUNITY}}},
         "type": {"name": typ}, "displayName": display or name.split(".")[-1]}
    attrs = {k: [{"value": v}] if isinstance(v, str) else [{"value": x} for x in v]
             for k, v in (attributes or {}).items() if v}
    if attrs:
        a["attributes"] = attrs
    rels = {k: [{"name": t} for t in v] for k, v in (relations or {}).items() if v}
    if rels:
        a["relations"] = rels
    return a


def legal_attr(refs):
    return [f"{code}: {article}" for code, article in refs]


def collibra_assets(m, prov):
    """All s1 assets, in a fixed order; records the provenance of each in prov."""
    out = []
    fq = lambda *p: ".".join((DATABASE, SCHEMA) + p)  # noqa: E731
    out.append(asset(DATABASE, DOM_PHYSICAL, "Database", relations={"contains Schema": [f"{DATABASE}.{SCHEMA}"]}))
    prov[DATABASE] = {"provenance": "gap_fill", "source": "render_corpus.py (database name)"}
    out.append(asset(f"{DATABASE}.{SCHEMA}", DOM_PHYSICAL, "Schema",
                     relations={"contains Table": [fq(o["name"]) for o in m.tables],
                                "contains Database View": [fq(o["name"]) for o in m.views]}))
    prov[f"{DATABASE}.{SCHEMA}"] = {"provenance": "gap_fill", "source": "render_corpus.py (schema name)"}
    for o in m.tables + m.views:
        typ = "Table" if o["kind"] == "TABLE" else "Database View"
        if o["kind"] == "TABLE":
            desc, p, src = m.cube.DESCRIPTION.get(o["name"]), "bird_official", f"cube.csv {o['name']}"
            display = m.cube.NAME.get(o["name"]) or o["name"]
        else:
            desc, p, src = m.texts["files"][o["file"]]["purpose"], "gap_fill", "src/corpus_text/sql_comments.yaml"
            display = o["name"]
        out.append(asset(fq(o["name"]), DOM_PHYSICAL, typ, display=display,
                         attributes={"Description": desc,
                                     "Legal reference": legal_attr(m.legal_refs("CUBE", o["name"]))},
                         relations={"contains Column": [fq(o["name"], c) for c in o["columns"]],
                                    "sources from": [fq(s) for s in o["sources"]]}))
        prov[fq(o["name"])] = {"provenance": p, "source": src, "node": m.node_of(o)}
        for c in o["columns"]:
            name, definition, cp, csrc = m.column_text(o["name"], c)
            term = m.var.NAME[c.upper()] if c.upper() in m.var.index else None
            dom = m.domain_of(c)
            out.append(asset(fq(o["name"], c), DOM_PHYSICAL, "Column", display=name or c,
                             attributes={"Description": definition, "Data Type": m.type_of.get(c)},
                             relations={"represents Business Term": [term] if term else [],
                                        "uses Code Set": [m.dom.NAME[dom]] if dom else []}))
            prov[fq(o["name"], c)] = {"provenance": cp or "gap_fill", "source": csrc or "column name only",
                                      "node": m.node_of(o)}
    for v in m.variables:
        out.append(asset(m.var.NAME[v], DOM_GLOSSARY, "Business Term",
                         attributes={"Definition": m.var.DESCRIPTION[v], "BIRD variable": v,
                                     "Legal reference": legal_attr(m.legal_refs("VARIABLE", v))}))
        prov[m.var.NAME[v]] = {"provenance": "bird_official", "source": f"variable.csv {v}"}
    for d in m.domains:
        out.append(asset(m.dom.NAME[d], DOM_CODES, "Code Set",
                         attributes={"Description": m.dom.DESCRIPTION[d], "BIRD domain": d},
                         relations={"contains Code Value": m.members_of(d)}))
        prov[m.dom.NAME[d]] = {"provenance": "bird_official", "source": f"domain.csv {d}"}
        for mid in m.members_of(d):
            out.append(asset(mid, DOM_CODES, "Code Value", display=m.mem.NAME[mid],
                             attributes={"Code": m.mem.CODE[mid], "Description": m.mem.DESCRIPTION[mid],
                                         "Legal reference": legal_attr(m.legal_refs("MEMBER", mid))}))
            prov[mid] = {"provenance": "bird_official", "source": f"member.csv {mid}"}
    return out


def s2_subset(assets, seed):
    """Sparse metadata: structure names only, half of the columns (no definitions), 30% of the terms."""
    import random
    rng = random.Random(seed)
    by_type = {}
    for a in assets:
        by_type.setdefault(a["type"]["name"], []).append(a)
    cols = sorted(a["identifier"]["name"] for a in by_type["Column"])
    terms = sorted(a["identifier"]["name"] for a in by_type["Business Term"])
    keep_cols = set(rng.sample(cols, round(len(cols) * 0.5)))
    keep_terms = set(rng.sample(terms, round(len(terms) * 0.3)))
    out = []
    for a in assets:
        t, name = a["type"]["name"], a["identifier"]["name"]
        b = {k: v for k, v in a.items() if k not in ("attributes", "relations")}
        if t in ("Database", "Schema", "Table", "Database View"):
            rel = {k: v for k, v in a.get("relations", {}).items() if k != "contains Column"}
            rel_cols = [r for r in a.get("relations", {}).get("contains Column", []) if r["name"] in keep_cols]
            if rel_cols:
                rel["contains Column"] = rel_cols
            if rel:
                b["relations"] = rel
            b["displayName"] = name.split(".")[-1]
        elif t == "Column" and name in keep_cols:
            dt = a.get("attributes", {}).get("Data Type")
            if dt:
                b["attributes"] = {"Data Type": dt}
            b["displayName"] = name.split(".")[-1]
        elif t == "Business Term" and name in keep_terms:
            b["attributes"] = {"Definition": a["attributes"]["Definition"]}
        else:
            continue
        out.append(b)
    rules = {"seed": seed, "tables_and_views": "all, names only", "columns": "50% sample, data type only",
             "business_terms": "30% sample, definition only", "code_sets_and_values": "none",
             "kept_columns": sorted(keep_cols), "kept_business_terms": sorted(keep_terms)}
    return out, rules


def render_metadata(out, m, prov, seed):
    import json
    s1 = collibra_assets(m, prov)
    s2, rules = s2_subset(s1, seed)
    for scen, assets in (("s1_rich", s1), ("s2_limited", s2)):
        write(out / "corpus" / scen / "metadata" / "collibra_import.json",
              json.dumps(assets, indent=2, ensure_ascii=False) + "\n")
    write(out / "answer_key" / "s2_subset.yaml", dump_yaml(rules))


# ---------------------------------------------------------------- main
def render(out=ROOT, seed=42):
    out = Path(out)
    for d in (out / "corpus", out / "answer_key"):
        if d.exists():
            shutil.rmtree(d)
    objects = render_sql(out)
    write(out / "answer_key" / "sql_object_map.yaml", dump_yaml(sql_object_map(objects)))
    m, prov = Model(objects), {}
    render_metadata(out, m, prov, seed)
    write(out / "answer_key" / "provenance.yaml",
          dump_yaml({"note": "Provenance of every corpus metadata asset, glossary entry and document section. "
                             "bird_official = verbatim from the BIRD export; gap_fill = written for this project; "
                             "legal:<register id> = quoted from that legal text.",
                     "metadata": prov}))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default=str(ROOT))
    a = ap.parse_args()
    render(Path(a.out), a.seed)
    print(f"rendered corpus/ and answer_key/ under {a.out}")
