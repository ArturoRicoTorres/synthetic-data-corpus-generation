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


# ---------------------------------------------------------------- data-model docs (s1 per table, s2 overview)
GLOSSARY_FROM_DATA_MODEL = "../../../shared/regulatory/glossary.md"
CONTEXT_KEYS = ["DT_RFRNC", "RPRTNG_AGNT_ID", "ACCNTNG_CNSLDTN_LVL", "ACCNTNG_STNDRD"]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def mart_joins(m):
    """Official relationships collapsed to joins between data-mart tables (paths through entities that the mart
    does not store are followed). [(parent, child, [(parent col, child col)], via, relationship names)]"""
    mart = {t["name"]: set(t["columns"]) for t in m.tables}
    edges = {}
    for j in m.spec["joins"]:
        if j.get("provenance") != "bird_official":
            continue
        edges.setdefault(j["parent"], []).append(j)
    out = []
    for parent in mart:
        stack = [(e, [], [e]) for e in edges.get(parent, [])]
        first_keys = {}
        while stack:
            e, via, path = stack.pop()
            child = e["child"]
            if child in mart:
                first = path[0]
                km = first.get("key_map") or {}
                pairs = [(k, km.get(k, k)) for k in first["keys"] if km.get(k, k) in mart[child] and k in mart[parent]]
                key = (parent, child, tuple(pairs), tuple(via))
                first_keys.setdefault(key, []).extend(p["relationship"] for p in path)
            elif len(path) < 6:
                stack += [(n, via + [child], path + [n]) for n in edges.get(child, [])]
        for (p, c, pairs, via), rels in first_keys.items():
            out.append((p, c, list(pairs), list(via), sorted(set(rels))))
    return sorted(out, key=lambda x: (x[0], x[1], x[3]))


def merge_joins(joins):
    """One entry per (parent, child, key pairs): official relationship names and the entities passed merged."""
    merged = {}
    for p, c, pairs, via, rels in joins:
        k = (p, c, tuple(pairs))
        v = merged.setdefault(k, (set(), set()))
        v[0].update(via)
        v[1].update(rels)
    return [(p, c, list(pairs), sorted(v[0]), sorted(v[1])) for (p, c, pairs), v in sorted(merged.items())]


def term_link(m, name, prefix):
    return f"[{name}]({prefix}#{slug(name)})"


def table_page(m, t, joins, prov, rel_path):
    name = t["name"]
    title = m.cube.NAME.get(name) or name
    lines = [f"# {title} ({name})", ""]
    lines += wrap(m.cube.DESCRIPTION.get(name, "").replace("\n", " ")) + [""]
    prov[f"{rel_path}#purpose"] = {"provenance": "bird_official", "source": f"cube.csv {name}"}
    lines += ["## Columns", "", "| Column | Business name | Type | Key | Definition |", "|---|---|---|---|---|"]
    for c in t["columns"]:
        bname, definition, _, _ = m.column_text(name, c)
        bn = term_link(m, m.var.NAME[c], GLOSSARY_FROM_DATA_MODEL) if c in m.var.index else (bname or "")
        d = (definition or "").replace("\n", " ").replace("|", "/")
        lines.append(f"| `{c}` | {bn} | {t['types'][c]} | {'PK' if c in t['keys'] else ''} | {d} |")
    prov[f"{rel_path}#columns"] = {"provenance": "bird_official", "source": "variable.csv / spec attributes"}
    lines += ["", "## Relationships", ""]
    mine = [j for j in joins if name in (j[0], j[1])]
    if name == "INTRNL_GRP_RL_IL":
        lines += wrap("Joined to every position on the reporting context: " + ", ".join(CONTEXT_KEYS) + ". "
                      "Each reporting context has exactly one row with group role type GRP_RL_TYP_1.") + [""]
        prov[f"{rel_path}#relationships-context"] = {"provenance": "gap_fill", "source": "decision OI-13"}
    for p, c, pairs, via, rels in mine:
        other, direction = (c, "has many") if p == name else (p, "belongs to")
        on = ", ".join(f"`{a}` = `{b}`" for a, b in pairs)
        lines.append(f"- {direction} [{other}]({other}.md) on {on}")
        if via:
            lines.append(f"  - through BIRD entities not stored in the data mart: {', '.join(via)}")
        lines.append(f"  - BIRD relationship(s): {', '.join(rels)}")
    prov[f"{rel_path}#relationships"] = {"provenance": "bird_official", "source": "spec joins (cube_relationship)"}
    coded = [c for c in t["columns"] if m.domain_of(c) and m.members_of(m.domain_of(c))]
    if coded:
        lines += ["", "## Code lists", ""]
        for c in coded:
            d = m.domain_of(c)
            lines += [f"### {c}: {m.dom.NAME[d]}", "", "| Code value | Code | Name |", "|---|---|---|"]
            lines += [f"| `{mid}` | {m.mem.CODE[mid]} | {m.mem.NAME[mid]} |" for mid in m.members_of(d)]
            lines.append("")
        prov[f"{rel_path}#code-lists"] = {"provenance": "bird_official", "source": "domain.csv / member.csv"}
    refs = m.legal_refs("CUBE", name)
    if refs:
        lines += ["## Legal references", ""] + [f"- {code}: {art}" for code, art in refs]
    return "\n".join(lines).rstrip() + "\n"


def er_diagram(joins, labels=True):
    lines = ["```mermaid", "erDiagram"]
    for p, c, pairs, via, _ in joins:
        lab = ", ".join(b for _, b in pairs if b not in CONTEXT_KEYS) or "context"
        lines.append(f'    {p} ||--o{{ {c} : "{lab if labels else ""}"')
    lines.append("```")
    return lines


def render_data_model(out, m, prov):
    joins = merge_joins(mart_joins(m))
    base = out / "corpus" / "s1_rich" / "docs" / "data_model"
    for t in m.tables:
        rel = f"corpus/s1_rich/docs/data_model/{t['name']}.md"
        write(base / f"{t['name']}.md", table_page(m, t, joins, prov, rel))
    idx = ["# Reporting data mart: data model", ""]
    idx += wrap("Input tables of the reporting data mart. Every table carries the reporting context: reference "
                "date, reporting agent, consolidation level and accounting standard. Table and column names follow "
                "the ECB BIRD input layer.") + [""]
    idx += ["| Table | Name |", "|---|---|"]
    idx += [f"| [{t['name']}]({t['name']}.md) | {m.cube.NAME.get(t['name'], '')} |" for t in m.tables]
    idx += ["", "## Relationships", ""] + er_diagram(joins)
    write(base / "index.md", "\n".join(idx) + "\n")
    prov["corpus/s1_rich/docs/data_model/index.md#intro"] = {"provenance": "gap_fill", "source": "render_corpus.py"}
    ov = ["# Data mart overview", ""]
    ov += [f"- {t['name']}: {m.cube.NAME.get(t['name'], '')}" for t in m.tables]
    ov += ["", "## Relationships", ""] + er_diagram(joins, labels=False)
    write(out / "corpus" / "s2_limited" / "docs" / "overview.md", "\n".join(ov) + "\n")
    prov["corpus/s2_limited/docs/overview.md"] = {"provenance": "bird_official", "source": "cube.csv names, joins"}
    return joins


# ---------------------------------------------------------------- reporting-chain document (s1, decision D4)
SHARED_FROM_DOCS = "../../shared/regulatory"


def routine_anchor(rid):
    return slug(rid)


def render_reporting_chain(out, m, prov):
    chain = load_yaml(TEXT_DIR / "reporting_chain.yaml")
    lmap = load_yaml(LINEAGE_MAP)
    files = {o["file"] for o in m.objects}
    by_file = {}
    for o in m.objects:
        by_file.setdefault(o["file"], []).append(o)
    rel = "corpus/s1_rich/docs/reporting_chain.md"
    lines = ["# Reporting chain: non-performing loans ratio (FINREP F 18.00.a)", ""]
    lines += wrap(chain["intro"]) + [""]
    prov[f"{rel}#intro"] = {"provenance": "gap_fill", "source": "src/corpus_text/reporting_chain.yaml"}
    nodes = sorted(chain["sections"], key=lambda n: lmap["nodes"][n]["file"])
    for i, nid in enumerate(nodes, 1):
        sec, fname = chain["sections"][nid], lmap["nodes"][nid]["file"]
        assert fname in files, fname
        objs = by_file[fname]
        created = {o["name"] for o in objs}
        reads = sorted({s for o in objs for s in o["sources"]} - created)
        routines = m.texts["files"][fname]["routines"]
        lines += [f"## Step {i}: {sec['title']}", ""] + wrap(sec["text"]) + [""]
        lines.append(f"- SQL file: `{fname}`")
        lines.append(f"- Reads: {', '.join(f'`{r}`' for r in reads)}")
        made = ", ".join("`" + o["name"] + "`" for o in objs)
        lines.append(f"- Creates: {made}")
        if routines:
            lines.append("- Official BIRD routine(s): " + ", ".join(
                f"[{r}]({SHARED_FROM_DOCS}/bird_transformation_rules.md#{routine_anchor(r)})" for r in routines))
        lines.append("- Terms: " + ", ".join(term_link(m, t, f"{SHARED_FROM_DOCS}/glossary.md") for t in sec["terms"]))
        if sec["cites"]:
            lines.append("- References: " + "; ".join(
                f"[{reg}]({SHARED_FROM_DOCS}/register.md#{slug(reg)}) {at}" for reg, at in sec["cites"]))
        lines.append("")
        prov[f"{rel}#step-{i}"] = {"provenance": "gap_fill", "source": "src/corpus_text/reporting_chain.yaml",
                                   "node": nid, "title": sec["title"]}
    write(out / rel, "\n".join(lines).rstrip() + "\n")
    return chain


# ---------------------------------------------------------------- legal text (decisions D3, D7)
def legal_plain_text(path):
    """Plain text of an EUR-Lex HTML file: tags removed, entities decoded, one block per line."""
    import html
    raw = Path(path).read_text(encoding="utf-8", errors="strict")
    txt = html.unescape(re.sub(r"<[^>]+>", "\n", raw))
    return [ln.strip() for ln in re.sub(r"[ \t\r\f\v ]+", " ", txt).split("\n") if ln.strip()]


def normalise(text):
    return re.sub(r"\s+", " ", text.replace(" ", " ")).strip()


def annex_paragraphs(lines, annex="ANNEX V"):
    """{(part, number): {"heading": str, "points": [(label or None, text)]}} for one annex."""
    start = next(i for i, ln in enumerate(lines) if ln == annex and i > 0 and "INSTRUCTIONS" in lines[i + 1])
    end = next(i for i in range(start + 1, len(lines)) if re.fullmatch(r"ANNEX [IVX]+", lines[i]))
    part, cur, heading, out, label = None, None, None, {}, None
    for ln in lines[start:end]:
        if re.fullmatch(r"PART \d+", ln):
            part, cur = int(ln.split()[1]), None
            continue
        if part is None:
            continue
        if re.fullmatch(r"\d+\.", ln):
            cur = (part, int(ln[:-1]))
            out[cur] = {"heading": heading, "points": []}
            label = None
            continue
        if re.match(r"^\d+(\.\d+)*\.\s*\S", ln):
            heading, cur = ln, None
            continue
        if cur is None:
            continue
        if re.fullmatch(r"\([a-z]+\)|\([ivx]+\)", ln):
            label = ln
            continue
        out[cur]["points"].append((label, ln))
        label = None
    return out


def paragraph_text(para, point=None):
    pts = para["points"]
    if point:
        pts = [p for p in pts if p[0] == f"({point})"]
    return [(f"{lab} {t}" if lab else t) for lab, t in pts]


def load_legal():
    cfg = load_yaml(TEXT_DIR / "legal_extracts.yaml")
    src = ROOT / cfg["source"]["file"]
    lines = legal_plain_text(src)
    return cfg, src, lines, annex_paragraphs(lines, cfg["source"]["annex"])


# ---------------------------------------------------------------- regulatory documents (shared by all scenarios)
REG_DIR = Path("corpus") / "shared" / "regulatory"
BIRD_ID = "BIRD_FINREP_4_3"
ROUTINES = ["R_IDT_DER", "R_DER_GRSS_CRRYNG_AMNT_3", "R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_2",
            "R_DER_GRSS_CRRYNG_AMNT_1", "R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_3", "R_F_18.00.a_ALL",
            "R_F_18.00.a_R0070", "R_F_18.00.a_R0080", "R_F_18.00.a_R0090", "R_F_18.00.a_R0100", "R_F_18.00.a_R0110",
            "R_F_18.00.a_R0120", "R_F_18.00.a_R0150", "R_F_18.00.a_C0010", "R_F_18.00.a_C0060"]
TEMPLATE = "F_18.00.a"
USED_ROWS = ["0070", "0080", "0090", "0100", "0110", "0120", "0150"]
USED_COLS = ["0010", "0060"]


def anchor(a):
    return f'<a id="{slug(a)}"></a>'


def reg_link(reg_id, prefix=""):
    return f"[{reg_id}]({prefix}register.md#{slug(reg_id)})"


def header_tree(direction):
    th = bird_export.read("table_header")
    h = bird_export.indexed("header", "HEADER_ID")
    t = th[th.TABLE_ID == TEMPLATE]
    t = t[t.HEADER_ID.map(lambda x: h.DIRECTION.get(x)) == direction]
    t = t.assign(o=t.ORDER_NUMBER.astype(int)).sort_values("o")
    parent = dict(zip(t.HEADER_ID, t.PARENT_HEADER_ID))
    depth = lambda x: 0 if not parent.get(x) else 1 + depth(parent[x])  # noqa: E731
    return [(x, h.CODE[x], h.LABEL[x], depth(x)) for x in t.HEADER_ID]


def render_template(out, prov):
    rel = REG_DIR / "f_18_00_a_template.md"
    rt = bird_export.indexed("rendering_table", "TABLE_ID")
    cube = bird_export.indexed("cube", "CUBE_ID")
    lines = [f"# Template F 18.00.a: {rt.NAME[TEMPLATE]}", ""]
    lines += wrap("Row and column structure of FINREP template F 18.00.a as published in the ECB BIRD metadata "
                  f"(FINREP {bird_export.framework_version()}). Rows and columns marked with * are the ones the "
                  "non-performing loans ratio uses.") + [""]
    for direction, title, used in (("Y", "Rows", USED_ROWS), ("X", "Columns", USED_COLS)):
        lines += [f"## {title}", "", "| Code | Label |", "|---|---|"]
        for _, code, label, depth in header_tree(direction):
            mark = " *" if code in used and (direction == "X" or depth <= 2) else ""
            lines.append(f"| {code}{mark} | {'&nbsp;&nbsp;' * 2 * depth}{label} |")
        lines.append("")
    lines += ["## Cells used", "", "| Cell | Data point | Description |", "|---|---|---|"]
    for col in USED_COLS:
        dp = f"{TEMPLATE}_R0070_C{col}_OL"
        lines.append(f"| r0070, c{col} | `{dp}` | {cube.DESCRIPTION[dp]} |")
    write(out / rel, "\n".join(lines) + "\n")
    prov[str(rel).replace("\\", "/")] = {"provenance": "bird_official",
                                         "source": "rendering_table.csv, header.csv, table_header.csv, cube.csv"}


def render_bird_definitions(out, m, prov):
    rel = REG_DIR / "bird_definitions.md"
    lines = ["# BIRD definitions", ""]
    lines += wrap("Definitions of the BIRD variables and code values used in the reporting data mart, verbatim "
                  f"from the ECB BIRD metadata (FINREP {bird_export.framework_version()}). Legal references are "
                  "given as published there; see the register for the status of each document.") + [""]
    lines += ["## Variables", ""]
    for v in m.variables:
        d = m.var.DOMAIN_ID[v]
        lines += [anchor(v), f"### {m.var.NAME[v]} (`{v}`)", ""] + wrap(m.var.DESCRIPTION[v].replace("\n", " "))
        lines += ["", f"- Domain: {m.dom.NAME.get(d, d)} (`{d}`)"]
        lines += [f"- Legal reference: {reg_link(c)} {a}" for c, a in m.legal_refs("VARIABLE", v)]
        lines.append("")
    lines += ["## Code values", ""]
    for d in m.domains:
        lines += [f"### {m.dom.NAME[d]} (`{d}`)", "", "| Code value | Code | Name | Description |", "|---|---|---|---|"]
        for mid in m.members_of(d):
            desc = m.mem.DESCRIPTION[mid].replace("\n", " ").replace("|", "/")
            lines.append(f"| `{mid}` | {m.mem.CODE[mid]} | {m.mem.NAME[mid]} | {desc} |")
        refs = [(mid, c, a) for mid in m.members_of(d) for c, a in m.legal_refs("MEMBER", mid)]
        if refs:
            lines += ["", "Legal references:"] + [f"- `{mid}`: {reg_link(c)} {a}" for mid, c, a in refs]
        lines.append("")
    write(out / rel, "\n".join(lines).rstrip() + "\n")
    prov[str(rel).replace("\\", "/")] = {"provenance": "bird_official",
                                         "source": "variable.csv, domain.csv, member.csv, legal_reference.csv"}


def render_bird_rules(out, prov):
    rel = REG_DIR / "bird_transformation_rules.md"
    ro = bird_export.indexed("routine", "ROUTINE_ID")
    lines = ["# BIRD transformation rules", ""]
    lines += wrap("Official algorithm text of the BIRD routines behind the non-performing loans ratio, verbatim from "
                  f"the ECB BIRD metadata (FINREP {bird_export.framework_version()}). The algorithms are written in "
                  "the BIRD pseudo-code and are not directly executable.") + [""]
    for rid in ROUTINES:
        lines += [anchor(rid), f"## {rid}", ""]
        desc = ro.DESCRIPTION.get(rid) or ro.NAME.get(rid)
        if desc:
            lines += wrap(desc.replace("\n", " ")) + [""]
        lines += ["```", bird_export.algorithm(rid), "```", ""]
    write(out / rel, "\n".join(lines).rstrip() + "\n")
    prov[str(rel).replace("\\", "/")] = {"provenance": "bird_official", "source": "routine.csv"}


def render_annex_extracts(out, legal, prov):
    cfg, _, _, paras = legal
    s = cfg["source"]
    rel = REG_DIR / "annex_v_extracts.md"
    lines = [f"# Annex V extracts: {s['annex_title']}", ""]
    lines += wrap(f"Quoted from {s['title']}, Annex V. Version: {s['version']}. Source: {s['url']}. Register entry: "
                  f"{reg_link(s['register_id'])}.") + [""]
    for e in cfg["extracts"]:
        key = (e["part"], e["paragraph"])
        lines += [anchor(f"part-{key[0]}-paragraph-{key[1]}"),
                  f"## Part {key[0]}, paragraph {key[1]}: {e['topic']}", ""]
        for t in paragraph_text(paras[key]):
            lines += ["> " + t, ">"]
        lines[-1] = ""
        prov[f"{rel}#part-{key[0]}-paragraph-{key[1]}".replace("\\", "/")] = {
            "provenance": f"legal:{s['register_id']}", "source": f"Annex V, Part {key[0]}, paragraph {key[1]}"}
    write(out / rel, "\n".join(lines).rstrip() + "\n")


def reg_number(code):
    """REG_EU_680_2014 -> 680/2014; REG_EU_534_2015 -> 2015/534 (EU numbering changed in 2015)."""
    mt = re.fullmatch(r"(?:REG|DIR)_(?:EU|EC)_(\d+)_(\d{4})", code)
    if not mt:
        return None
    num, year = mt.groups()
    return f"{year}/{num}" if int(year) >= 2015 else f"{num}/{year}"


def register_entries(m, legal):
    cfg = legal[0]
    s = cfg["source"]
    lt = bird_export.read("legal_text").set_index("LEGAL_CODE")
    fv = bird_export.read("framework_version")
    fin = fv[fv.FRAMEWORK_ID == "FINREP"].iloc[0]
    entries = {
        BIRD_ID: {"title": f"ECB BIRD metadata export, FINREP framework version {fin.VERSION_ID}",
                  "issuer": "European Central Bank (BIRD)", "version": f"{fin.VERSION_ID}, valid from {fin.VALID_FROM}",
                  "url": "https://bird.ecb.europa.eu", "file": bird_export.ZIP.name, "sha256": bird_export.zip_sha256(),
                  "status": "Source of the data model, definitions and transformation rules of this corpus.",
                  "replaced_by": None, "numbers": []},
        s["register_id"]: {"title": normalise(s["title"]), "issuer": s["issuer"], "version": s["version"],
                           "url": s["url"], "file": Path(s["file"]).name,
                           "sha256": __import__("hashlib").sha256((ROOT / s["file"]).read_bytes()).hexdigest(),
                           "status": "Applies from 28 June 2021 (Article 23). Repeals Implementing Regulation (EU) "
                                     "No 680/2014 (Article 22).",
                           "replaced_by": None, "numbers": ["2021/451"]},
    }
    for code in sorted(lt.index):
        r = lt.loc[code]
        entries.setdefault(code, {
            "title": normalise(r.LEGAL_DESCRIPTION), "issuer": None, "version": None,
            "url": r.LEGAL_TEXT_URL or None, "file": None, "sha256": None,
            "status": normalise(cfg["repeal"][code]) if code in cfg["repeal"] else
            "As listed in the BIRD export; status not verified.",
            "replaced_by": s["register_id"] if code in cfg["repeal"] else None,
            "numbers": [n for n in [reg_number(code)] if n] + re.findall(r"ECB/\d{4}/\d+", r.LEGAL_DESCRIPTION)})
    entries["CRR_REGULATION"]["numbers"] = ["575/2013"]
    return entries


CITATION = re.compile(r"(?:Regulation|Directive)\s*\((?:EU|EC|EEC)\)\s*(?:No\s*)?(\d+/\d+)|"
                      r"\(?(ECB/\d{4}/\d+)\)?")


def citations_in(text, entries, aliases):
    """Register ids cited in a text, and citations that resolve to no entry."""
    by_number = {n: k for k, e in entries.items() for n in e["numbers"]}
    found, unresolved = set(), set()
    for mt in CITATION.finditer(text):
        num = mt.group(1) or mt.group(2)
        reg = by_number.get(num) or aliases.get(num)
        (found.add(reg) if reg else unresolved.add(num))
    for k in entries:
        if re.search(rf"\b{re.escape(k)}\b", text):
            found.add(k)
    for alias, reg in aliases.items():
        if re.search(rf"(?<![\w/]){re.escape(alias)}(?![\w/])", text):
            found.add(reg)
    return found, unresolved


def render_register(out, m, legal, prov):
    """Register of every document the corpus cites; written last so 'cited in' covers every corpus file."""
    entries = register_entries(m, legal)
    aliases = legal[0]["aliases"]
    cited = {k: set() for k in entries}
    unresolved = {}
    for p in sorted((out / "corpus").rglob("*")):
        if p.is_file():
            found, bad = citations_in(p.read_text(encoding="utf-8"), entries, aliases)
            relp = p.relative_to(out).as_posix()
            for k in found:
                cited[k].add(relp)
            if bad:
                unresolved[relp] = sorted(bad)
    keep = {k: e for k, e in entries.items() if cited[k] or k in (BIRD_ID, legal[0]["source"]["register_id"])}
    data = {k: {**{f: e[f] for f in ("title", "issuer", "version", "url", "file", "sha256", "status", "replaced_by")},
                "cited_in": sorted(cited[k])} for k, e in sorted(keep.items())}
    data = {k: {f: v for f, v in e.items() if v not in (None, [])} for k, e in data.items()}
    write(out / REG_DIR / "register.yaml", dump_yaml({"documents": data}))
    lines = ["# Register of referenced documents", ""]
    lines += wrap("Every regulatory and reference document cited anywhere in this corpus. Citations are kept as "
                  "they appear in their source; where a cited document has been replaced, the entry says by which "
                  "document.") + [""]
    for k, e in data.items():
        lines += [anchor(k), f"## {k}", "", f"**{e['title']}**", ""]
        for f in ("issuer", "version", "url", "file", "sha256", "status"):
            if f in e:
                lines.append(f"- {f.replace('_', ' ').capitalize()}: {e[f]}")
        if "replaced_by" in e:
            lines.append(f"- Replaced by: {reg_link(e['replaced_by'])}")
        lines.append(f"- Cited in: {', '.join(e['cited_in']) if e['cited_in'] else 'not cited'}")
        lines.append("")
    write(out / REG_DIR / "register.md", "\n".join(lines).rstrip() + "\n")
    prov[(REG_DIR / "register.md").as_posix()] = {"provenance": "bird_official",
                                                  "source": "legal_text.csv; 2021/451 file; decision OI-14"}
    return data, unresolved


def glossary_entries(m, legal):
    """{key: {"name", "definitions": [(label, text, [register ids])]}} for terms, and code values separately."""
    cfg, _, _, paras = legal
    reg = cfg["source"]["register_id"]
    terms = {}

    def add(name, label, text, regs):
        e = terms.setdefault(name.lower(), {"name": name, "definitions": []})
        e["definitions"].append((label, normalise(text), regs))

    for v in m.variables:
        add(m.var.NAME[v], f"BIRD variable `{v}`", m.var.DESCRIPTION[v],
            [BIRD_ID] + [c for c, _ in m.legal_refs("VARIABLE", v)])
    for t in m.tables:
        add(m.cube.NAME[t["name"]], f"BIRD input layer entity `{t['name']}`", m.cube.DESCRIPTION[t["name"]], [BIRD_ID])
    hdr = bird_export.indexed("header", "HEADER_ID")
    for direction, codes in (("Y", USED_ROWS), ("X", USED_COLS)):
        for code in codes:
            hid = f"{TEMPLATE}_{direction}{code}"
            kind = "row" if direction == "Y" else "column"
            add(hdr.LABEL[hid], f"Template F 18.00.a {kind} {code}",
                f"Label of {kind} {code} of template F 18.00.a.", [BIRD_ID])
    for g in cfg["glossary_terms"]:
        text = " ".join(paragraph_text(paras[(g["part"], g["paragraph"])], g.get("point")))
        where = f"Annex V, Part {g['part']}, paragraph {g['paragraph']}" + (f"({g['point']})" if g.get("point") else "")
        add(g["term"], where, text, [reg])
    codes = {mid: {"name": m.mem.NAME[mid], "domain": m.dom.NAME[m.mem.DOMAIN_ID[mid]],
                   "text": normalise(m.mem.DESCRIPTION[mid]),
                   "regs": [BIRD_ID] + [c for c, _ in m.legal_refs("MEMBER", mid)]} for mid in m.members}
    return terms, codes


def render_glossary(out, m, legal, prov):
    terms, codes = glossary_entries(m, legal)
    lines = ["# Glossary", ""]
    lines += wrap("General vocabulary of this corpus: the business terms of the reporting data mart, the labels of "
                  "template F 18.00.a and the Annex V concepts they rely on, followed by the code values used. "
                  "Definitions are quoted from their source; each links to its entry in the register.") + [""]
    lines += ["## Terms", ""]
    for key in sorted(terms):
        e = terms[key]
        lines += [anchor(e["name"]), f"### {e['name']}", ""]
        for label, text, regs in e["definitions"]:
            lines.append(f"- {label}: {text} (Source: {', '.join(reg_link(r) for r in dict.fromkeys(regs))})")
        lines.append("")
        prov[f"{REG_DIR.as_posix()}/glossary.md#{slug(e['name'])}"] = {
            "provenance": "bird_official" if all(r != legal[0]["source"]["register_id"]
                                                 for _, _, rs in e["definitions"] for r in rs) else "bird_official+legal",
            "source": "; ".join(label for label, _, _ in e["definitions"])}
    lines += ["## Code values", ""]
    for mid in sorted(codes):
        c = codes[mid]
        lines += [anchor(mid), f"### {mid}: {c['name']}", ""]
        lines.append(f"- Code list: {c['domain']}. {c['text']} "
                     f"(Source: {', '.join(reg_link(r) for r in dict.fromkeys(c['regs']))})")
        lines.append("")
    write(out / REG_DIR / "glossary.md", "\n".join(lines).rstrip() + "\n")
    return terms, codes


def render_regulatory(out, m, prov):
    legal = load_legal()
    render_template(out, prov)
    render_bird_definitions(out, m, prov)
    render_bird_rules(out, prov)
    render_annex_extracts(out, legal, prov)
    render_glossary(out, m, legal, prov)
    return legal


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
    docs = {}
    render_data_model(out, m, docs)
    render_reporting_chain(out, m, docs)
    legal = render_regulatory(out, m, docs)
    _, unresolved = render_register(out, m, legal, docs)
    if unresolved:
        raise ValueError(f"citations without a register entry: {unresolved}")
    write(out / "answer_key" / "provenance.yaml",
          dump_yaml({"note": "Provenance of every corpus metadata asset, glossary entry and document section. "
                             "bird_official = verbatim from the BIRD export; gap_fill = written for this project; "
                             "legal:<register id> = quoted from that legal text.",
                     "metadata": prov, "documents": docs}))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default=str(ROOT))
    a = ap.parse_args()
    render(Path(a.out), a.seed)
    print(f"rendered corpus/ and answer_key/ under {a.out}")
