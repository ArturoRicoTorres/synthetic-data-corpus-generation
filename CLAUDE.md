# CLAUDE.md

## What this project is

We are building a synthetic test corpus for an AI classifier that clusters data-lineage transformation steps
into business-logic groups. The corpus starts from a canonical lineage spec (the answer key) and renders
artifacts from it: SQL, Collibra-style metadata, data-model docs and reporting-chain documents.

The first KRI is the NPL ratio for loans and advances: FINREP F 18.00.a row 0070, column 0060 divided by
column 0010, from the official ECB BIRD metadata (FINREP 4.3).

## Layout

- `data/raw/entities-*.zip` - official BIRD metadata export from bird.ecb.europa.eu. Source of truth. Read-only.
- `data/raw/bird_official/` - extracted export, created by the builder. Git-ignored.
- `src/build_spec_official.py` - builds `specs/npl_ratio_lineage_spec_v0.2.yaml` from the export.
- `specs/npl_ratio_lineage_spec_v0.2.yaml` - current spec (answer key). Generated; never edit by hand.
- `specs/npl_ratio_lineage_spec_v0.1.yaml` - superseded spec from a community repo. Reference only.
- `legacy/` - archived code. Do not use for new work.
- `decisions.md` - log of decisions on open issues.
- `sql/`, `tests/` - rendered SQL and tests (to be built).
- `docs/` - project deck.
- `prompts/` - task prompts for Claude Code sessions.

## Commands

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/build_spec_official.py                      # regenerates specs/npl_ratio_lineage_spec_v0.2.yaml
pytest                                                  # once tests exist
```

## Rules

1. **The official export is the only source of truth for BIRD logic.** Never take logic from `legacy/` or the
   v0.1 spec. Never modify anything in `data/raw/`.
2. **Change the spec only through the builder.** Edit `src/build_spec_official.py`, rerun it, and review the
   git diff of the YAML.
3. **Every spec element keeps a provenance tag:** `bird_official` (read from the export) or `gap_fill`
   (added by hand). New hand-added content is always `gap_fill`.
4. **Do not resolve open issues yourself.** Open issues are listed in the spec's `open_issues` block. Only the
   user decides them. When the user decides, record the decision in `decisions.md` (issue, decision, date)
   and then implement it. If a task depends on an undecided issue, stop and ask.
5. **Log every correction to an official algorithm (OI-09).** The official algorithms are pseudo-SQL with known
   defects (unknown identifiers, members used without their variable). When rendering SQL, record each fix in
   `sql/corrections.yaml` with the routine id, the original text, the corrected text and the reason.
6. **Do not leak the answer key into the corpus.** Rendered SQL, metadata and documents that the classifier
   will see must not contain spec node ids (T01...), `business_group` labels, taxonomy names or the word
   "gap_fill". Keep the mapping from SQL objects to spec nodes in a separate file (`sql/lineage_map.yaml`).
7. **Verify, don't assume.** Any SQL you render must run in DuckDB on synthetic data and reconcile with an
   independent Python (pandas) calculation of the same cells. Lineage parsed from the SQL (sqlglot) must
   match the spec's transformation graph.
8. **Keep changes small and reviewable.** One task per branch; explain what changed and why in the commit
   message.

## Pending decisions (check decisions.md for current status)

- OI-07: KRI scope - this cell ratio, or a wider headline NPL ratio?
- OI-11: treatment of null accumulated impairment on amortised-cost loans.
- OI-09, OI-10, OI-12, OI-13, OI-14: see the spec's `open_issues`.
