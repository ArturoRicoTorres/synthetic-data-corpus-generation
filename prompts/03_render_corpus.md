# Task 03 - Render the corpus layers (start in Plan mode)

Read CLAUDE.md, decisions.md, specs/npl_ratio_lineage_spec_v0.2.yaml, sql/lineage_map.yaml and
docs/Semantic_Layer_Lineage_Model.pptx (slides 2-4: test scenarios and inputs) first.

Goal: turn the verified reference SQL into the corpus the classifier sees, for the three test scenarios in
the deck, with the answer key kept outside the corpus.

## Gates - stop and ask me before planning if any is open

- **OI-14** (legal citations: 680/2014 vs 2021/451) must be DECIDED in decisions.md. The metadata, register
  and regulatory documents cite it.
- **D1-D4** are decided (see decisions.md). Follow them.

## Scenarios (from the deck)

| Scenario | Corpus SQL | Client metadata | Client docs | Regulatory docs |
|---|---|---|---|---|
| `s1_rich` | yes, with comments | full | data model + reporting chain | yes |
| `s2_limited` | yes, no comments | sparse subset | short overview only | yes |
| `s3_regulatory_only` | yes, no comments | none | none | yes |

## Layers to plan

1. **Corpus SQL** (D2: BIRD names).
   - Derived from `sql/reference/` by the renderer, never by hand.
   - s1 adds descriptive comments; s2 and s3 have no comments.
   - It must run in DuckDB and give exactly the reference C0010/C0060.
   - It must be in a form the lineage tool can ingest (D1). Ask me if the tool needs a specific dialect or
     file layout.
2. **Collibra-style metadata.**
   - Tables, columns, business terms and code values with relations, as an import-style JSON/CSV.
   - Descriptions come from the export's definitions (`bird_official`); anything added by hand is
     `gap_fill`.
   - s2 is a seeded, documented subset of s1.
3. **Data-model docs.** Wiki-style Markdown per table: purpose, keys, relationships (from the spec `joins`),
   and code lists (from the export).
4. **Reporting-chain document** (D4: close to the steps). A process description from source load to the
   F 18.00 cell and the KRI, one section per transformation step. It describes what each step does, but
   never names a step id, group or taxonomy label.
5. **Regulatory documents** (D3), shared by all scenarios:
   - from the BIRD export: template F 18.00.a row and column definitions, the variable and member definitions
     used, and the official transformation rule text for R0070, C0010 and C0060;
   - from official legal text: the relevant FINREP Annex V paragraphs (gross carrying amount, loans and
     advances, non-performing exposures, counterparty sectors) and the reporting ITS. Fetch from EUR-Lex and
     record the exact source URL and version;
   - **one register** of every referenced regulatory document: id, title, issuer, version or date, URL,
     status (in force, repealed, replaced by), and where the corpus cites it;
   - **one general vocabulary glossary**: every business term used across the corpus, with a definition and
     a link to its register entry.
6. **Lineage JSON** (D1) is out of scope. I will run the corpus SQL through the lineage tool. Checking its
   output against the spec is a later task.

## Layout

- `corpus/<scenario>/...` and `corpus/shared/regulatory/...` hold what the classifier sees. The register and
  glossary go in `corpus/shared/regulatory/`.
- `answer_key/` sits outside `corpus/`. It holds:
  - the map from every corpus SQL object to a spec node;
  - the provenance (`bird_official` / `gap_fill` / legal source) of every metadata entry, glossary term and
    document section.
- `src/render_corpus.py` is one seeded entry point that regenerates everything. Legal text fetched once is
  cached under `data/raw/legal/` with its URL and retrieval date, and is never modified. Corpus files are
  generated; never edit them by hand.

## Tests

- **Leakage (rule 6)** extends to every file under `corpus/`: no node ids, no `gap_fill`, no
  `business_group`, no taxonomy names, and nothing from `answer_key/`. Taxonomy labels are ordinary English
  words (e.g. "measurement", "aggregation"); propose how to block the labels without blocking normal prose,
  and ask me.
- **Reconciliation:** the corpus SQL gives the reference cells exactly, for every scenario.
- **Lineage:** sqlglot lineage of the corpus SQL, mapped through `answer_key/`, matches the spec graph.
- **Register and glossary:**
  - every regulatory citation in the corpus resolves to a register entry;
  - every glossary term links to a register entry;
  - every business term used in the client docs is in the glossary.
- **Coverage:**
  - s1 metadata covers every spec attribute and table;
  - s2 is a strict subset of s1;
  - s3 has no client files.
- **Determinism:** two runs with the same seed give byte-identical output.

Plan, then wait for my approval before writing code. Work on a new branch `feat/corpus-layers` from
`feat/reference-sql` (or from main once that is merged). Commit in small steps.
