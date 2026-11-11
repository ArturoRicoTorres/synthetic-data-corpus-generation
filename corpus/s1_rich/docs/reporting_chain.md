# Reporting chain: non-performing loans ratio (FINREP F 18.00.a)

This document describes how the reporting data mart produces the non-performing loans ratio for loans and
advances at cost or amortised cost: FINREP template F 18.00.a, row 0070, column 0060 divided by column 0010.
The chain follows the ECB BIRD transformation rules for FINREP 4.3. Each section below is one step of the
chain, in the order in which the steps run. The SQL of each step is in the file named in the section.

## Step 1: Input snapshot for the reporting context

Every input table holds rows for many reporting contexts. A reporting context is the combination of reference
date, reporting agent, consolidation level and accounting standard. This step keeps only the rows of the
context being reported. The context is set once per database session; no other filter is applied and no value
is changed.

- SQL file: `01_load_input_snapshot.sql`
- Reads: `INSTRMNT_ENTTY_RL_ASSGNMNT_IL`, `INSTRMNT_IL`, `INSTRMNT_RL_IL`, `INTRNL_GRP_RL_IL`, `LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL`, `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL`, `OTC_DRVTV_HDG_IL`, `PRTY_IL`, `SCRTY_ENTTY_RL_ASSGNMNT_IL`, `SCRTY_EXCHNG_TRDBL_DRVTV_IL`
- Creates: `instrmnt_il_snp`, `instrmnt_rl_il_snp`, `instrmnt_entty_rl_assgnmnt_il_snp`, `prty_il_snp`, `intrnl_grp_rl_il_snp`, `otc_drvtv_hdg_il_snp`, `scrty_exchng_trdbl_drvtv_il_snp`, `scrty_entty_rl_assgnmnt_il_snp`, `lng_shrt_blnc_sht_rcgnsd_scrty_pstn_il_snp`, `lng_blnc_sht_rcgnsd_scrty_pstn_accntng_il_snp`
- Terms: [Reference date](../../shared/regulatory/glossary.md#reference-date), [Reporting agent identifier](../../shared/regulatory/glossary.md#reporting-agent-identifier), [Accounting consolidation level](../../shared/regulatory/glossary.md#accounting-consolidation-level), [Accounting standard](../../shared/regulatory/glossary.md#accounting-standard)

## Step 2: Status, classification and counterparty attributes for the reporting rules

The attributes that the reporting rules read are passed unchanged from the input layer into the enriched
layer: the performing status and accounting portfolio of each instrument role, the institutional sector and
the multilateral development bank flag of each party, the role and main-party flags of each instrument
assignment, the reporting scheme of the reporting agent, and the issuer role of each security. Values are not
recoded.

- SQL file: `02_carry_enriched_attributes.sql`
- Reads: `instrmnt_entty_rl_assgnmnt_il_snp`, `instrmnt_rl_il_snp`, `intrnl_grp_rl_il_snp`, `prty_il_snp`, `scrty_entty_rl_assgnmnt_il_snp`
- Creates: `instrmnt_rl_eil`, `instrmnt_entty_rl_assgnmnt_eil`, `prty_eil`, `intrnl_grp_rl_eil`, `scrty_entty_rl_assgnmnt_eil`
- Official BIRD routine(s): [R_IDT_DER](../../shared/regulatory/bird_transformation_rules.md#r-idt-der)
- Terms: [Performing status](../../shared/regulatory/glossary.md#performing-status), [Accounting classification](../../shared/regulatory/glossary.md#accounting-classification), [Institutional sector](../../shared/regulatory/glossary.md#institutional-sector), [Entity role type](../../shared/regulatory/glossary.md#entity-role-type), [Finrep reporting scheme](../../shared/regulatory/glossary.md#finrep-reporting-scheme)

## Step 3: Gross carrying amount of instrument roles

The gross carrying amount of each instrument role depends on its accounting portfolio and impairment status.
For financial assets at amortised cost under IFRS, and for national GAAP cost-based portfolios with specific
allowances, it is the carrying amount plus the accumulated impairment. For national GAAP portfolios covered by
general allowances, it is the carrying amount plus the general allowances for credit risk and for banking
risk. For national GAAP portfolios at cost that are not subject to impairment, it is the carrying amount. For
portfolios at fair value it is the fair value; for non-performing exposures the accumulated negative changes
in fair value due to credit risk are added back. The branches are evaluated in a fixed order and the first
match applies. When an input that a branch needs is missing, the instrument role gets no gross carrying amount
and is not reported.

- SQL file: `03_gross_carrying_amount_instruments.sql`
- Reads: `instrmnt_rl_il_snp`
- Creates: `instrmnt_rl_eil_grss_crryng_amnt`
- Official BIRD routine(s): [R_DER_GRSS_CRRYNG_AMNT_3](../../shared/regulatory/bird_transformation_rules.md#r-der-grss-crryng-amnt-3)
- Terms: [Gross carrying amount](../../shared/regulatory/glossary.md#gross-carrying-amount), [Carrying amount](../../shared/regulatory/glossary.md#carrying-amount), [Accumulated impairment](../../shared/regulatory/glossary.md#accumulated-impairment), [Fair value](../../shared/regulatory/glossary.md#fair-value), [Impairment status](../../shared/regulatory/glossary.md#impairment-status)
- References: [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 1, paragraph 34; [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 1, paragraph 27

## Step 4: Annex V instrument type of instrument roles

Each instrument role is assigned its type of financial asset as defined in FINREP Annex V. An instrument is a
loan or advance when its product and the role of the counterparty match: a loan product where the counterparty
is the main loan debtor, a financial lease where it is the main lessee, or a deposit where it is the main
deposit-taking corporation. Balances at central banks and credit institutions that are repayable on demand are
not loans and advances; they are cash balances at central banks or other demand deposits. Under IFRS, an
instrument held for sale is reported as a non-current asset held for sale instead. The same rule also assigns
the types for equity instruments and derivatives, which this chain does not report.

- SQL file: `04_annex_v_type_instruments.sql`
- Reads: `instrmnt_entty_rl_assgnmnt_il_snp`, `instrmnt_il_snp`, `instrmnt_rl_il_snp`, `otc_drvtv_hdg_il_snp`, `prty_il_snp`
- Creates: `instrmnt_rl_eil_typ_fnncl_asst`
- Official BIRD routine(s): [R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_2](../../shared/regulatory/bird_transformation_rules.md#r-der-typ-fnncl-asst-instrmnt-annx-v-2)
- Terms: [Type of Financial Asset Instrument according to Annex V](../../shared/regulatory/glossary.md#type-of-financial-asset-instrument-according-to-annex-v), [Instrument type by product](../../shared/regulatory/glossary.md#instrument-type-by-product), [Entity role type](../../shared/regulatory/glossary.md#entity-role-type), [Repayment rights](../../shared/regulatory/glossary.md#repayment-rights), [Held for sale indicator](../../shared/regulatory/glossary.md#held-for-sale-indicator)
- References: [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 1, paragraph 32; [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 2, paragraphs 2 and 3

## Step 5: Debt securities held as loans and advances

Long balance-sheet positions in debt securities get a gross carrying amount and an Annex V type with the same
rules as instrument roles, applied per prudential and accounting portfolio. A debt security that is not
negotiable is reported as a loan or advance; a negotiable one is a debt security and is not part of row 0070.
The performing status of a security position comes from the security itself.

- SQL file: `05_securities_positions.sql`
- Reads: `lng_blnc_sht_rcgnsd_scrty_pstn_accntng_il_snp`, `lng_shrt_blnc_sht_rcgnsd_scrty_pstn_il_snp`, `scrty_entty_rl_assgnmnt_il_snp`, `scrty_exchng_trdbl_drvtv_il_snp`
- Creates: `scrty_exchng_trdbl_drvtv_eil`, `lng_scrty_pstn_eil_grss_crryng_amnt`, `lng_scrty_pstn_eil_typ_fnncl_asst`
- Official BIRD routine(s): [R_DER_GRSS_CRRYNG_AMNT_1](../../shared/regulatory/bird_transformation_rules.md#r-der-grss-crryng-amnt-1), [R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_3](../../shared/regulatory/bird_transformation_rules.md#r-der-typ-fnncl-asst-instrmnt-annx-v-3)
- Terms: [Gross carrying amount](../../shared/regulatory/glossary.md#gross-carrying-amount), [Negotiable security indicator](../../shared/regulatory/glossary.md#negotiable-security-indicator), [Debt security by Performing status type](../../shared/regulatory/glossary.md#debt-security-by-performing-status-type)
- References: [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 1, paragraphs 31 and 32

## Step 6: FINREP reporting basis of the reporting agent

Template F 18.00.a is reported only by reporting agents that report FINREP on a full, simplified or
over-simplified basis. The reporting basis is read from the reporting agent's internal group role; each
reporting context has exactly one such role. Contexts on any other basis produce no figures.

- SQL file: `06_reporting_scheme_scope.sql`
- Reads: `intrnl_grp_rl_eil`
- Creates: `f_18_00_a_scp`
- Official BIRD routine(s): [R_F_18.00.a_ALL](../../shared/regulatory/bird_transformation_rules.md#r-f-18-00-a-all)
- Terms: [Finrep reporting scheme](../../shared/regulatory/glossary.md#finrep-reporting-scheme), [Internal group role type](../../shared/regulatory/glossary.md#internal-group-role-type)

## Step 7: Counterparty sector rows of template F 18.00.a

Instrument and security positions are combined with their counterparty. A position enters the template when
its Annex V type is loans and advances and its accounting portfolio is at amortised cost (IFRS) or cost-based
(national GAAP). The counterparty must be the main debtor, main lessee, main deposit-taking corporation or,
for securities, the primary issuer. The institutional sector of the counterparty then decides the row: central
banks (0080), general governments (0090), credit institutions (0100), other financial corporations (0110),
non-financial corporations (0120) and households (0150). Multilateral development banks are reported under
credit institutions.

- SQL file: `07_counterparty_sector_rows.sql`
- Reads: `f_18_00_a_scp`, `instrmnt_entty_rl_assgnmnt_eil`, `instrmnt_rl_eil`, `instrmnt_rl_eil_grss_crryng_amnt`, `instrmnt_rl_eil_typ_fnncl_asst`, `lng_scrty_pstn_eil_grss_crryng_amnt`, `lng_scrty_pstn_eil_typ_fnncl_asst`, `prty_eil`, `scrty_entty_rl_assgnmnt_eil`, `scrty_exchng_trdbl_drvtv_eil`
- Creates: `f_18_00_a_dtpnt`, `f_18_00_a_sctr_rw`
- Official BIRD routine(s): [R_F_18.00.a_R0080](../../shared/regulatory/bird_transformation_rules.md#r-f-18-00-a-r0080), [R_F_18.00.a_R0090](../../shared/regulatory/bird_transformation_rules.md#r-f-18-00-a-r0090), [R_F_18.00.a_R0100](../../shared/regulatory/bird_transformation_rules.md#r-f-18-00-a-r0100), [R_F_18.00.a_R0110](../../shared/regulatory/bird_transformation_rules.md#r-f-18-00-a-r0110), [R_F_18.00.a_R0120](../../shared/regulatory/bird_transformation_rules.md#r-f-18-00-a-r0120), [R_F_18.00.a_R0150](../../shared/regulatory/bird_transformation_rules.md#r-f-18-00-a-r0150)
- Terms: [Institutional sector](../../shared/regulatory/glossary.md#institutional-sector), [Multilateral development bank indicator](../../shared/regulatory/glossary.md#multilateral-development-bank-indicator), [Main debtor indicator](../../shared/regulatory/glossary.md#main-debtor-indicator), [Primary issuer indicator](../../shared/regulatory/glossary.md#primary-issuer-indicator)
- References: [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 1, paragraph 42; [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 1, paragraph 44; [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 1, paragraphs 15 and 16

## Step 8: Row 0070: loans and advances

Row 0070 "Loans and advances" holds the positions of the six counterparty sector rows together. A position
that matches no sector row is not part of row 0070.

- SQL file: `08_total_loans_and_advances_row.sql`
- Reads: `f_18_00_a_sctr_rw`
- Creates: `f_18_00_a_r0070`
- Official BIRD routine(s): [R_F_18.00.a_R0070](../../shared/regulatory/bird_transformation_rules.md#r-f-18-00-a-r0070)
- Terms: [Type of Financial Asset Instrument according to Annex V](../../shared/regulatory/glossary.md#type-of-financial-asset-instrument-according-to-annex-v)
- References: [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 2, paragraph 217; [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 2, paragraph 218

## Step 9: Column 0010: gross carrying amount

Column 0010 is the sum of the gross carrying amount of the positions in row 0070. Only positive amounts are
added.

- SQL file: `09_gross_carrying_amount_cell.sql`
- Reads: `f_18_00_a_r0070`
- Creates: `f_18_00_a_r0070_c0010`
- Official BIRD routine(s): [R_F_18.00.a_C0010](../../shared/regulatory/bird_transformation_rules.md#r-f-18-00-a-c0010)
- Terms: [Gross carrying amount](../../shared/regulatory/glossary.md#gross-carrying-amount)
- References: [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 2, paragraph 221

## Step 10: Column 0060: non-performing

Column 0060 is the same sum restricted to non-performing positions: instrument roles whose performing status
is non-performing, and security positions whose security is a non-performing debt security.

- SQL file: `10_non_performing_cell.sql`
- Reads: `f_18_00_a_r0070`
- Creates: `f_18_00_a_r0070_c0060`
- Official BIRD routine(s): [R_F_18.00.a_C0060](../../shared/regulatory/bird_transformation_rules.md#r-f-18-00-a-c0060)
- Terms: [Gross carrying amount](../../shared/regulatory/glossary.md#gross-carrying-amount), [Performing status](../../shared/regulatory/glossary.md#performing-status), [Debt security by Performing status type](../../shared/regulatory/glossary.md#debt-security-by-performing-status-type)
- References: [REG_EU_2021_451](../../shared/regulatory/register.md#reg-eu-2021-451) Annex V, Part 2, paragraph 213; [CRR_REGULATION](../../shared/regulatory/register.md#crr-regulation) Article 47a(3)

## Step 11: Non-performing loans ratio

The ratio is column 0060 divided by column 0010 of row 0070. When column 0010 is zero or missing, the ratio is
not reported.

- SQL file: `11_npl_ratio.sql`
- Reads: `f_18_00_a_r0070_c0010`, `f_18_00_a_r0070_c0060`
- Creates: `npl_ratio`
- Terms: [Gross carrying amount](../../shared/regulatory/glossary.md#gross-carrying-amount)
