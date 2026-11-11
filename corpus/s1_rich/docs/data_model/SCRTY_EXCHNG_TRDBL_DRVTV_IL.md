# Security and exchange tradable derivative (SCRTY_EXCHNG_TRDBL_DRVTV_IL)

A Security and exchange tradable derivative is a certificate attesting credit, the ownership of stocks or
bonds, or the right to ownership connected with tradable derivatives.

## Columns

| Column | Business name | Type | Key | Definition |
|---|---|---|---|---|
| `DT_RFRNC` | [Reference date](../../../shared/regulatory/glossary.md#reference-date) | DATE | PK | Reporting agents shall report credit data as recorded on the following reporting reference dates: (a) for monthly transmissions, on the last day of each month; (b) for quarterly transmissions, on the last day of March, June, September and December. |
| `RPRTNG_AGNT_ID` | [Reporting agent identifier](../../../shared/regulatory/glossary.md#reporting-agent-identifier) | VARCHAR(255) | PK | Reporting agent identifier |
| `ACCNTNG_CNSLDTN_LVL` | [Accounting consolidation level](../../../shared/regulatory/glossary.md#accounting-consolidation-level) | VARCHAR(255) | PK | Accounting consolidation level is the level on which the accounting is consolidated, Solo or group. |
| `ACCNTNG_STNDRD` | [Accounting standard](../../../shared/regulatory/glossary.md#accounting-standard) | VARCHAR(255) | PK | Accounting standard |
| `SCRTY_EXCHNG_TRDBL_DRVTV_ID` | [Security and exchange tradable derivative identifier](../../../shared/regulatory/glossary.md#security-and-exchange-tradable-derivative-identifier) | VARCHAR(255) | PK | An identifier to uniquely identify each security. |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP` | [Security and exchange tradable derivative type](../../../shared/regulatory/glossary.md#security-and-exchange-tradable-derivative-type) | VARCHAR(255) |  | A discriminator to distinguish between securities and exchange tradable derivatives. |
| `NGTBL_SCRTY_INDCTR` | [Negotiable security indicator](../../../shared/regulatory/glossary.md#negotiable-security-indicator) | VARCHAR(255) |  | An indicator specifying is a security is listed or not. |
| `DBT_SCRTY_PRFRMNG_STTS_TYP` | [Debt security by Performing status type](../../../shared/regulatory/glossary.md#debt-security-by-performing-status-type) | VARCHAR(255) |  | Performing status in accordance with Implementing Regulation (EU) No 680/2014. |

## Relationships

- has many [LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL](LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`, `SCRTY_EXCHNG_TRDBL_DRVTV_ID` = `SCRTY_ID`
  - through BIRD entities not stored in the data mart: BLNC_SHT_RCGNSD_NN_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL, SCRTY_PSTN_IL
  - BIRD relationship(s): ASS_BLNC_SHT_RCGNSD_SCRTY_PSTN_LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_34797_IL, ASS_SCRTY_INVLVD_SCRTY_PSTN_30258_IL, ASS_SCRTY_PSTN_BLNC_SHT_NN_BLNC_SHT_RCGNSD_28454_IL
- has many [SCRTY_ENTTY_RL_ASSGNMNT_IL](SCRTY_ENTTY_RL_ASSGNMNT_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`, `SCRTY_EXCHNG_TRDBL_DRVTV_ID` = `SCRTY_EXCHNG_TRDBL_DRVTV_ID`
  - BIRD relationship(s): ASS_SCRTY_EXCHNG_TRDBL_DRVTV_ISSD_ISSR_S_SCRTY_ISSR_ASSGNMNT_74658_IL

## Code lists

### SCRTY_EXCHNG_TRDBL_DRVTV_TYP: Security or exchange tradable derivative type

| Code value | Code | Name |
|---|---|---|
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_11` | 11 | Debt security without underlying assets |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_13` | 13 | Asset backed security |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_14` | 14 | Covered bond |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_19` | 19 | Performing debt security |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20` | 20 | Non-performing debt security |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_5` | 5 | Fund security |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_6` | 6 | Equity security |

### NGTBL_SCRTY_INDCTR: Negotiable security

| Code value | Code | Name |
|---|---|---|
| `NGTBL_SCRTY_1` | 1 | Negotiable security |
| `NGTBL_SCRTY_2` | 2 | Non-negotiable security |

### DBT_SCRTY_PRFRMNG_STTS_TYP: Security or exchange tradable derivative type

| Code value | Code | Name |
|---|---|---|
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_11` | 11 | Debt security without underlying assets |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_13` | 13 | Asset backed security |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_14` | 14 | Covered bond |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_19` | 19 | Performing debt security |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20` | 20 | Non-performing debt security |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_5` | 5 | Fund security |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_6` | 6 | Equity security |
