# Instrument (INSTRMNT_IL)

An Instrument is a product that establishes a financial relationship between a bank and its customer. In the
context of accounting such a financial relationship may be considered a financial asset or a financial
liabilty or an off-balance sheet item.

## Columns

| Column | Business name | Type | Key | Definition |
|---|---|---|---|---|
| `DT_RFRNC` | [Reference date](../../../shared/regulatory/glossary.md#reference-date) | DATE | PK | Reporting agents shall report credit data as recorded on the following reporting reference dates: (a) for monthly transmissions, on the last day of each month; (b) for quarterly transmissions, on the last day of March, June, September and December. |
| `RPRTNG_AGNT_ID` | [Reporting agent identifier](../../../shared/regulatory/glossary.md#reporting-agent-identifier) | VARCHAR(255) | PK | Reporting agent identifier |
| `ACCNTNG_CNSLDTN_LVL` | [Accounting consolidation level](../../../shared/regulatory/glossary.md#accounting-consolidation-level) | VARCHAR(255) | PK | Accounting consolidation level is the level on which the accounting is consolidated, Solo or group. |
| `ACCNTNG_STNDRD` | [Accounting standard](../../../shared/regulatory/glossary.md#accounting-standard) | VARCHAR(255) | PK | Accounting standard |
| `INSTRMNT_ID` | [Instrument identifier](../../../shared/regulatory/glossary.md#instrument-identifier) | VARCHAR(255) | PK | An identifier applied by the reporting agent to uniquely identify each instrument under a single contract. Each instrument must have one instrument identifier. This value will not change over time and cannot be used as the instrument identifier for any other instrument under the same contract. |
| `INSTRMNT_TYP_PRDCT` | [Instrument type by product](../../../shared/regulatory/glossary.md#instrument-type-by-product) | VARCHAR(255) |  | A discriminator to distinguish instruments by product. Examles are loans and advances, securities financing transactions, financial guarantees and other commitments or over the counter derivatives. |
| `RPYMNT_RGHTS` | [Repayment rights](../../../shared/regulatory/glossary.md#repayment-rights) | VARCHAR(255) |  | Classification of credit exposures according to the creditor's rights to claim the repayment of the exposure. On demand or at short notice |

## Relationships

- has many [INSTRMNT_ENTTY_RL_ASSGNMNT_IL](INSTRMNT_ENTTY_RL_ASSGNMNT_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `INSTRMNT_ID` = `INSTRMNT_ID`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`
  - BIRD relationship(s): ASS_DPST_PRVDD_DPST_TKNG_CRPRTN_DPST_DPST_TKNG_CRPRTN_ASSGNMNT_77220_IL, ASS_FNNCL_LS_LSS_FNNCL_LS_LSS_ASSGNMNT_77220_IL, ASS_OTHR_LN_DBTR_S_OTHR_LN_LN_DBTR_ASSGNMNT_77220_IL
- has many [INSTRMNT_RL_IL](INSTRMNT_RL_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `INSTRMNT_ID` = `INSTRMNT_ID`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`
  - BIRD relationship(s): ASS_INSTRMNT_ACTS_INSTRMNT_RL_S_85476_IL
- has many [OTC_DRVTV_HDG_IL](OTC_DRVTV_HDG_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `INSTRMNT_ID` = `INSTRMNT_ID`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`
  - BIRD relationship(s): ASS_OTC_DRVTV_INSTRMNT_OTC_DRVTV_HDG_60023_IL

## Code lists

### INSTRMNT_TYP_PRDCT: Type of instrument

| Code value | Code | Name |
|---|---|---|
| `TYP_INSTRMNT_10` | 10 | Over the counter (OTC) Option other than Over the counter (OTC) Credit spread option |
| `TYP_INSTRMNT_1020` | 1020 | Factoring |
| `TYP_INSTRMNT_1022` | 1022 | Other loan |
| `TYP_INSTRMNT_1023` | 1023 | Other trade receivable |
| `TYP_INSTRMNT_1112` | 1112 | Cash balances at central banks |
| `TYP_INSTRMNT_1113` | 1113 | Other demand deposits |
| `TYP_INSTRMNT_1114` | 1114 | Derivatives not hedge |
| `TYP_INSTRMNT_1115` | 1115 | Equity instruments |
| `TYP_INSTRMNT_1116` | 1116 | Debt securities |
| `TYP_INSTRMNT_1117` | 1117 | Loans and Advances |
| `TYP_INSTRMNT_1118` | 1118 | Non-current assets and disposal groups classified as held for sale |
| `TYP_INSTRMNT_1119` | 1119 | Derivatives hedge |
| `TYP_INSTRMNT_120` | 120 | Transit item |
| `TYP_INSTRMNT_1201` | 1201 | On demand deposit used for minimum reserve |
| `TYP_INSTRMNT_1202` | 1202 | On demand deposit not used for minimum reserve |
| `TYP_INSTRMNT_130` | 130 | Suspense item |
| `TYP_INSTRMNT_140` | 140 | Other advance |
| `TYP_INSTRMNT_162` | 162 | Open repurchase transaction |
| `TYP_INSTRMNT_163` | 163 | Term repurchase transaction |
| `TYP_INSTRMNT_2` | 2 | Equity instrument that is not a security |
| `TYP_INSTRMNT_380` | 380 | Over the counter (OTC) Forward |
| `TYP_INSTRMNT_5` | 5 | Other over the counter (OTC) Derivative instrument |
| `TYP_INSTRMNT_51` | 51 | Credit card debt |
| `TYP_INSTRMNT_511` | 511 | Tranferable overnight deposits |
| `TYP_INSTRMNT_512` | 512 | Non-transferable overnight deposits |
| `TYP_INSTRMNT_522` | 522 | Deposit with agreed maturity |
| `TYP_INSTRMNT_6` | 6 | Over the counter (OTC) Total return swap |
| `TYP_INSTRMNT_7` | 7 | Over the counter (OTC) Credit default swap |
| `TYP_INSTRMNT_8` | 8 | Other over the counter (OTC) Swap |
| `TYP_INSTRMNT_80` | 80 | Financial lease |
| `TYP_INSTRMNT_9` | 9 | Over the counter (OTC) Credit spread option |

### RPYMNT_RGHTS: Repayment rights

| Code value | Code | Name |
|---|---|---|
| `RPYMNT_RGHTS_1` | 1 | On demand or short notice |
| `RPYMNT_RGHTS_2` | 2 | Other than on demand or short notice |
