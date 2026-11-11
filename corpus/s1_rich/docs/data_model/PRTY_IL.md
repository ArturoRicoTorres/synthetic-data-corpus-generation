# Party (PRTY_IL)

A Party is an entity of interest.

## Columns

| Column | Business name | Type | Key | Definition |
|---|---|---|---|---|
| `DT_RFRNC` | [Reference date](../../../shared/regulatory/glossary.md#reference-date) | DATE | PK | Reporting agents shall report credit data as recorded on the following reporting reference dates: (a) for monthly transmissions, on the last day of each month; (b) for quarterly transmissions, on the last day of March, June, September and December. |
| `RPRTNG_AGNT_ID` | [Reporting agent identifier](../../../shared/regulatory/glossary.md#reporting-agent-identifier) | VARCHAR(255) | PK | Reporting agent identifier |
| `ACCNTNG_CNSLDTN_LVL` | [Accounting consolidation level](../../../shared/regulatory/glossary.md#accounting-consolidation-level) | VARCHAR(255) | PK | Accounting consolidation level is the level on which the accounting is consolidated, Solo or group. |
| `ACCNTNG_STNDRD` | [Accounting standard](../../../shared/regulatory/glossary.md#accounting-standard) | VARCHAR(255) | PK | Accounting standard |
| `PRTY_ID` | [Party identifier](../../../shared/regulatory/glossary.md#party-identifier) | VARCHAR(255) | PK | An identifier that uniquely identifies a party. |
| `INSTTTNL_SCTR` | [Institutional sector](../../../shared/regulatory/glossary.md#institutional-sector) | VARCHAR(255) |  | Institutional sectors in accordance with Regulation (EU) No 549/2013, Regulation (EU) No 575/2013 and Regulation (EU) No 1075/2013 of the European Central Bank (ECB/2013/40)(1). |
| `MLTLTRL_DVLPMNT_BNK_INDCTR` | [Multilateral development bank indicator](../../../shared/regulatory/glossary.md#multilateral-development-bank-indicator) | VARCHAR(255) |  | Multilateral development bank indicator specifies if the International organisation is a multilateral development bank or not. |

## Relationships

- has many [INSTRMNT_ENTTY_RL_ASSGNMNT_IL](INSTRMNT_ENTTY_RL_ASSGNMNT_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `PRTY_ID` = `PRTY_ID`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`
  - through BIRD entities not stored in the data mart: ENTTY_RL_IL
  - BIRD relationship(s): ASS_CRDTR_PRVDS_OTHR_LN_S_OTHR_LN_CRDTR_ASSGNMNT_25372_IL, ASS_DPST_TKNG_CRPRTN_PRVDS_DPST_S_DPST_DPST_TKNG_CRPRTN_ASSGNMNT_25372_IL, ASS_LN_DBTR_OBLGD_PY_OTHR_LN_S_OTHR_LN_LN_DBTR_ASSGNMNT_25372_IL, ASS_LSS_LSS_FNNCL_LS_S_FNNCL_LS_LSS_ASSGNMNT_25372_IL, ASS_PRTY_ACTS_PRTY_RL_68323_IL
- has many [SCRTY_ENTTY_RL_ASSGNMNT_IL](SCRTY_ENTTY_RL_ASSGNMNT_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `PRTY_ID` = `PRTY_ID`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`
  - through BIRD entities not stored in the data mart: ENTTY_RL_IL
  - BIRD relationship(s): ASS_ISSR_ISSS_SCRTY_EXCHNG_TRDBL_DRVTV_S_SCRTY_ISSR_ASSGNMNT_91707_IL, ASS_PRTY_ACTS_PRTY_RL_68323_IL

## Code lists

### INSTTTNL_SCTR: Institutional sectors

| Code value | Code | Name |
|---|---|---|
| `INSTTTNL_SCTR_IO` | IO | International organisations |
| `INSTTTNL_SCTR_S11` | S11 | Non financial corporations |
| `INSTTTNL_SCTR_S121` | S121 | Central banks |
| `INSTTTNL_SCTR_S122_A` | S122_A | Credit institutions |
| `INSTTTNL_SCTR_S122_A_1` | S122_A_1 | Credit institutions not including entities according to the article 2.5 Directive 2013/36/EU |
| `INSTTTNL_SCTR_S122_A_2` | S122_A_2 | Credit institutions according to the article 2.5 Directive 2013/36/EU |
| `INSTTTNL_SCTR_S122_B1` | S122_B1 | Electronic money institutions principally engaged in financial intermediation |
| `INSTTTNL_SCTR_S122_B2` | S122_B2 | Deposit-taking corporations except the central bank, other than credit institutions and electronic money institutions |
| `INSTTTNL_SCTR_S123` | S123 | Money Market Funds (MMFs) |
| `INSTTTNL_SCTR_S124` | S124 | Non-MMF investment funds |
| `INSTTTNL_SCTR_S125_A` | S125_A | Financial Vehicle Corporations (FVCs) |
| `INSTTTNL_SCTR_S125_B` | S125_B | Security and derivative dealers |
| `INSTTTNL_SCTR_S125_C` | S125_C | Financial corporations engaged in lending |
| `INSTTTNL_SCTR_S125_D` | S125_D | Specialised financial corporations other than CCPs |
| `INSTTTNL_SCTR_S125_E` | S125_E | Central Counterparties (CCPs) |
| `INSTTTNL_SCTR_S125_I` | S125_I | Other financial intermediaries, except insurance corporations and pension funds, other than CCPs, FVCs, security and derivative dealers, financial corporations engaged in lending and specialised financial corporations |
| `INSTTTNL_SCTR_S125_W` | S125_W | Other financial corporations excluding financial vehicle corporations |
| `INSTTTNL_SCTR_S127` | S127 | Captive financial institutions and money lenders |
| `INSTTTNL_SCTR_S128` | S128 | Insurance corporations |
| `INSTTTNL_SCTR_S129` | S129 | Pension funds |
| `INSTTTNL_SCTR_S1311` | S1311 | Central government (excluding social security funds) |
| `INSTTTNL_SCTR_S1312` | S1312 | State government (excluding social security funds) |
| `INSTTTNL_SCTR_S1313` | S1313 | Local government (excluding social security funds) |
| `INSTTTNL_SCTR_S1314` | S1314 | Social security funds |
| `INSTTTNL_SCTR_S14_A` | S14_A | Households that are sole proprietorships/partnerships without legal status |
| `INSTTTNL_SCTR_S14_B` | S14_B | Households other than sole proprietorships/partnerships without legal status |
| `INSTTTNL_SCTR_S15` | S15 | Non profit institutions serving households |

### MLTLTRL_DVLPMNT_BNK_INDCTR: Multilateral development bank indicator

| Code value | Code | Name |
|---|---|---|
| `MLTLTRL_DVLPMNT_BNK_INDCTR_1` | 1 | Multilateral development bank |
