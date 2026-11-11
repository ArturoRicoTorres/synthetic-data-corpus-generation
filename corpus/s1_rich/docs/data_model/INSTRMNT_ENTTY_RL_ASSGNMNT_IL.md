# Instrument Entity role assignment (INSTRMNT_ENTTY_RL_ASSGNMNT_IL)

An Instrument Entity role assignment is the combination of an Instrument and an Entity role that indicates
which Instrument is assigned to which Entity role.

## Columns

| Column | Business name | Type | Key | Definition |
|---|---|---|---|---|
| `DT_RFRNC` | [Reference date](../../../shared/regulatory/glossary.md#reference-date) | DATE | PK | Reporting agents shall report credit data as recorded on the following reporting reference dates: (a) for monthly transmissions, on the last day of each month; (b) for quarterly transmissions, on the last day of March, June, September and December. |
| `RPRTNG_AGNT_ID` | [Reporting agent identifier](../../../shared/regulatory/glossary.md#reporting-agent-identifier) | VARCHAR(255) | PK | Reporting agent identifier |
| `ACCNTNG_CNSLDTN_LVL` | [Accounting consolidation level](../../../shared/regulatory/glossary.md#accounting-consolidation-level) | VARCHAR(255) | PK | Accounting consolidation level is the level on which the accounting is consolidated, Solo or group. |
| `ACCNTNG_STNDRD` | [Accounting standard](../../../shared/regulatory/glossary.md#accounting-standard) | VARCHAR(255) | PK | Accounting standard |
| `INSTRMNT_ID` | [Instrument identifier](../../../shared/regulatory/glossary.md#instrument-identifier) | VARCHAR(255) | PK | An identifier applied by the reporting agent to uniquely identify each instrument under a single contract. Each instrument must have one instrument identifier. This value will not change over time and cannot be used as the instrument identifier for any other instrument under the same contract. |
| `ENTTY_RL_TYP` | [Entity role type](../../../shared/regulatory/glossary.md#entity-role-type) | VARCHAR(255) | PK | A discriminator to distinguish between party roles, organisation roles, central bank and private sector company roles and legal person roles. |
| `PRTY_ID` | [Party identifier](../../../shared/regulatory/glossary.md#party-identifier) | VARCHAR(255) | PK | An identifier that uniquely identifies a party. |
| `MN_DBTR_INDCTR` | [Main debtor indicator](../../../shared/regulatory/glossary.md#main-debtor-indicator) | VARCHAR(255) |  | An indicator specifying if a debtor is the main debtor. |
| `MN_LSS_INDCTR` | [Main lessee indicator](../../../shared/regulatory/glossary.md#main-lessee-indicator) | VARCHAR(255) |  | An indicator specifying if a debtor is the main debtor. |
| `MN_DPST_TKNG_CRPRTN_INDCTR` | [Main Deposit-taking corporation indicator](../../../shared/regulatory/glossary.md#main-deposit-taking-corporation-indicator) | VARCHAR(255) |  | An indicator specifying if a debtor is the main debtor. |

## Relationships

- belongs to [INSTRMNT_IL](INSTRMNT_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `INSTRMNT_ID` = `INSTRMNT_ID`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`
  - BIRD relationship(s): ASS_DPST_PRVDD_DPST_TKNG_CRPRTN_DPST_DPST_TKNG_CRPRTN_ASSGNMNT_77220_IL, ASS_FNNCL_LS_LSS_FNNCL_LS_LSS_ASSGNMNT_77220_IL, ASS_OTHR_LN_DBTR_S_OTHR_LN_LN_DBTR_ASSGNMNT_77220_IL
- belongs to [PRTY_IL](PRTY_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `PRTY_ID` = `PRTY_ID`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`
  - through BIRD entities not stored in the data mart: ENTTY_RL_IL
  - BIRD relationship(s): ASS_CRDTR_PRVDS_OTHR_LN_S_OTHR_LN_CRDTR_ASSGNMNT_25372_IL, ASS_DPST_TKNG_CRPRTN_PRVDS_DPST_S_DPST_DPST_TKNG_CRPRTN_ASSGNMNT_25372_IL, ASS_LN_DBTR_OBLGD_PY_OTHR_LN_S_OTHR_LN_LN_DBTR_ASSGNMNT_25372_IL, ASS_LSS_LSS_FNNCL_LS_S_FNNCL_LS_LSS_ASSGNMNT_25372_IL, ASS_PRTY_ACTS_PRTY_RL_68323_IL

## Code lists

### ENTTY_RL_TYP: Entity role type

| Code value | Code | Name |
|---|---|---|
| `ENTTY_RL_TYP_19` | 19 | Lessee |
| `ENTTY_RL_TYP_20` | 20 | Seller |
| `ENTTY_RL_TYP_27` | 27 | Deposit-taking corporation |
| `ENTTY_RL_TYP_28` | 28 | Loan debtor |
| `ENTTY_RL_TYP_8` | 8 | Issuer |

### MN_DBTR_INDCTR: Main debtor indicator

| Code value | Code | Name |
|---|---|---|
| `MN_DBTR_INDCTR_1` | 1 | Main debtor |

### MN_LSS_INDCTR: Main lessee indicator

| Code value | Code | Name |
|---|---|---|
| `MN_LSS_INDCTR_1` | 1 | Main lessee |

### MN_DPST_TKNG_CRPRTN_INDCTR: Main Deposit-taking corporation indicator

| Code value | Code | Name |
|---|---|---|
| `MN_DPST_TKNG_CRPRTN_INDCTR_1` | 1 | Main Deposit-taking corporation |
