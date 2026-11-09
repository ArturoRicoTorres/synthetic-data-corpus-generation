# Decisions log

Only the project owner decides open issues. Claude Code records a decision here, then implements it.
Issue details are in `specs/npl_ratio_lineage_spec_v0.2.yaml` under `open_issues`.

| Issue | Topic | Status | Decision | Date | Decided by |
|-------|-------|--------|----------|------|------------|
| OI-07 | KRI scope: F 18.00.a R0070 cell ratio vs wider headline NPL ratio | DECIDED | KRI is the cell ratio F 18.00.a R0070 C0060 / R0070 C0010 (loans and advances at cost or amortised cost). No wider headline ratio. | 2026-11-09 | project owner |
| OI-09 | Normalising defects in official pseudo-SQL algorithms | DECIDED | Fix only unambiguous defects (unknown identifiers, typos, members used without their variable, duplicated keywords, `<> null`, non-existent cube names, pseudo-SQL structure). Everything else stays literal, including parent members and NULL arithmetic. Each fix is logged in `sql/corrections.yaml`. New semantic questions become new open issues. | 2026-11-09 | project owner |
| OI-10 | Model R0070 as sum of sector rows to complete lineage | DECIDED | R0070 = sum of sector rows R0080, R0090, R0100, R0110, R0120, R0150, as in official routine R_F_18.00.a_R0070. Side effects found (S126 omission, MDB double count) are raised as OI-15 and OI-16. | 2026-11-09 | project owner |
| OI-11 | Null ACCMLTD_IMPRMNT on amortised-cost loans | DECIDED | Follow the official algorithm: no gross carrying amount, so the position is excluded from C0010 and C0060. Synthetic data includes such a loan, and a test asserts it is excluded. | 2026-11-09 | project owner |
| OI-12 | Out-of-scope branches kept verbatim only | DECIDED | Translate the full official CASE text of each derivation routine, including branches outside R0070 scope. Out-of-scope rows are tested as excluded. | 2026-11-09 | project owner |
| OI-13 | Join for FNRP_RPRTNG_SCHM gate (which GRP_RL_TYP row) | DECIDED | Join on the 4-part context key (DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD) with GRP_RL_TYP = GRP_RL_TYP_1 (the only member in the export). Exactly one such row per context key, enforced by a data check. | 2026-11-09 | project owner |
| OI-14 | Legal citations: 680/2014 vs 2021/451 | PENDING | | | |
