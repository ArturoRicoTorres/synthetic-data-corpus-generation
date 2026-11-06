# Task 02 - Render reference SQL and reconcile (start in Plan mode)

Read CLAUDE.md, decisions.md and specs/npl_ratio_lineage_spec_v0.2.yaml first.
If OI-07 or OI-11 is still PENDING in decisions.md, stop and ask me to decide before planning.

Goal: a clean, executable reference implementation of the spec in DuckDB, proven correct.

Plan, then wait for my approval before writing code:

1. **Schema**: DDL for the input-layer tables the spec uses (columns from the spec's `attributes`,
   keys from `joins`). Put it in `sql/reference/00_schema.sql`.
2. **SQL per transformation**: one file per spec node, in dependency order, under `sql/reference/`.
   Translate the official algorithm text; log every fix in `sql/corrections.yaml` (rule 5).
   No node ids, business groups or taxonomy terms in the SQL (rule 6). Write the mapping to
   `sql/lineage_map.yaml`.
3. **Synthetic data**: `src/generate_synthetic.py` producing a small seeded dataset that exercises every
   branch: each in-scope accounting portfolio, performing and non-performing, each debtor role,
   each counterparty sector row, held for sale, a non-negotiable debt security, null impairment (per OI-11),
   zero and negative amounts, and out-of-scope rows that must be excluded.
4. **Independent check**: `src/reference_calc.py` computing C0010, C0060 and the ratio in pandas directly
   from the spec logic, without reading the SQL.
5. **Tests** in `tests/`: SQL result equals the pandas result exactly; each branch case lands in the
   expected cell; sqlglot lineage from the SQL matches the spec's inputs/outputs per node.

Work on a new branch `feat/reference-sql`. Commit in small steps.
