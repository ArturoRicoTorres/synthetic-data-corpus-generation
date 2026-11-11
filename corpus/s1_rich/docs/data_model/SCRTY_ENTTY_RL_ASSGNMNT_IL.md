# Security Entity role assignment (SCRTY_ENTTY_RL_ASSGNMNT_IL)

A Security or Exchange tradable derivative Entity role assignment is the combination of a Security or Exchange
tradable derivative and an Entity role that indicates which Security or Exchange tradable derivative is
associated with which Entity role.

## Columns

| Column | Business name | Type | Key | Definition |
|---|---|---|---|---|
| `DT_RFRNC` | [Reference date](../../../shared/regulatory/glossary.md#reference-date) | DATE | PK | Reporting agents shall report credit data as recorded on the following reporting reference dates: (a) for monthly transmissions, on the last day of each month; (b) for quarterly transmissions, on the last day of March, June, September and December. |
| `RPRTNG_AGNT_ID` | [Reporting agent identifier](../../../shared/regulatory/glossary.md#reporting-agent-identifier) | VARCHAR(255) | PK | Reporting agent identifier |
| `ACCNTNG_CNSLDTN_LVL` | [Accounting consolidation level](../../../shared/regulatory/glossary.md#accounting-consolidation-level) | VARCHAR(255) | PK | Accounting consolidation level is the level on which the accounting is consolidated, Solo or group. |
| `ACCNTNG_STNDRD` | [Accounting standard](../../../shared/regulatory/glossary.md#accounting-standard) | VARCHAR(255) | PK | Accounting standard |
| `SCRTY_EXCHNG_TRDBL_DRVTV_ID` | [Security and exchange tradable derivative identifier](../../../shared/regulatory/glossary.md#security-and-exchange-tradable-derivative-identifier) | VARCHAR(255) | PK | An identifier to uniquely identify each security. |
| `ENTTY_RL_TYP` | [Entity role type](../../../shared/regulatory/glossary.md#entity-role-type) | VARCHAR(255) | PK | A discriminator to distinguish between party roles, organisation roles, central bank and private sector company roles and legal person roles. |
| `PRTY_ID` | [Party identifier](../../../shared/regulatory/glossary.md#party-identifier) | VARCHAR(255) | PK | An identifier that uniquely identifies a party. |
| `PRMRY_ISSR_INDCTR` | [Primary issuer indicator](../../../shared/regulatory/glossary.md#primary-issuer-indicator) | VARCHAR(255) |  | Primary issuer indicator |

## Relationships

- belongs to [PRTY_IL](PRTY_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `PRTY_ID` = `PRTY_ID`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`
  - through BIRD entities not stored in the data mart: ENTTY_RL_IL
  - BIRD relationship(s): ASS_ISSR_ISSS_SCRTY_EXCHNG_TRDBL_DRVTV_S_SCRTY_ISSR_ASSGNMNT_91707_IL, ASS_PRTY_ACTS_PRTY_RL_68323_IL
- belongs to [SCRTY_EXCHNG_TRDBL_DRVTV_IL](SCRTY_EXCHNG_TRDBL_DRVTV_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`, `SCRTY_EXCHNG_TRDBL_DRVTV_ID` = `SCRTY_EXCHNG_TRDBL_DRVTV_ID`
  - BIRD relationship(s): ASS_SCRTY_EXCHNG_TRDBL_DRVTV_ISSD_ISSR_S_SCRTY_ISSR_ASSGNMNT_74658_IL

## Code lists

### ENTTY_RL_TYP: Entity role type

| Code value | Code | Name |
|---|---|---|
| `ENTTY_RL_TYP_19` | 19 | Lessee |
| `ENTTY_RL_TYP_20` | 20 | Seller |
| `ENTTY_RL_TYP_27` | 27 | Deposit-taking corporation |
| `ENTTY_RL_TYP_28` | 28 | Loan debtor |
| `ENTTY_RL_TYP_8` | 8 | Issuer |

### PRMRY_ISSR_INDCTR: Primary issuer indicator

| Code value | Code | Name |
|---|---|---|
| `PRMRY_ISSR_INDCTR_1` | 1 | Primary issuer |
