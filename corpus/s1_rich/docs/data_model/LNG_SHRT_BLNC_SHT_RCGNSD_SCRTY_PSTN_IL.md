# Long/Short balance sheet recognised security position (LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL)

A Long/Short balance sheet recognised security position is a balance sheet recognised security position that
is either long or short.

## Columns

| Column | Business name | Type | Key | Definition |
|---|---|---|---|---|
| `DT_RFRNC` | [Reference date](../../../shared/regulatory/glossary.md#reference-date) | DATE | PK | Reporting agents shall report credit data as recorded on the following reporting reference dates: (a) for monthly transmissions, on the last day of each month; (b) for quarterly transmissions, on the last day of March, June, September and December. |
| `RPRTNG_AGNT_ID` | [Reporting agent identifier](../../../shared/regulatory/glossary.md#reporting-agent-identifier) | VARCHAR(255) | PK | Reporting agent identifier |
| `ACCNTNG_CNSLDTN_LVL` | [Accounting consolidation level](../../../shared/regulatory/glossary.md#accounting-consolidation-level) | VARCHAR(255) | PK | Accounting consolidation level is the level on which the accounting is consolidated, Solo or group. |
| `ACCNTNG_STNDRD` | [Accounting standard](../../../shared/regulatory/glossary.md#accounting-standard) | VARCHAR(255) | PK | Accounting standard |
| `SCRTY_ID` | [Security identifier](../../../shared/regulatory/glossary.md#security-identifier) | VARCHAR(255) | PK | An identifier to uniquely identify each security. |
| `INVSTR_PRTY_ID` | [Investor Party identifier](../../../shared/regulatory/glossary.md#investor-party-identifier) | VARCHAR(255) | PK | The party identifier of the involved investor. |
| `INVSTR_ENTTY_RL_TYP` | [Investor Entity role type](../../../shared/regulatory/glossary.md#investor-entity-role-type) | VARCHAR(255) | PK | The investor role. |
| `SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP` | [Security position Balance sheet recognised type](../../../shared/regulatory/glossary.md#security-position-balance-sheet-recognised-type) | VARCHAR(255) | PK | Security position Balance sheet recognised indicator defines whether a security position is recognised in the balance sheet or non recognised in the balance sheet |
| `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP` | [Long/Short balance sheet recognised security position type](../../../shared/regulatory/glossary.md#long-short-balance-sheet-recognised-security-position-type) | VARCHAR(255) | PK | Long/Short balance sheet recognised security position type defines whether a long/short balance sheet recognised security position is long or short. |
| `HLD_SL_INDCTR` | [Held for sale indicator](../../../shared/regulatory/glossary.md#held-for-sale-indicator) | VARCHAR(255) |  | A variable indicating the Non-current assets and instruments in disposal groups classified as held for sale in accordance with IFRS5. Is not applicable under national GAAP based on BAD. |

## Relationships

- has many [LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL](LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `INVSTR_ENTTY_RL_TYP` = `INVSTR_ENTTY_RL_TYP`, `INVSTR_PRTY_ID` = `INVSTR_PRTY_ID`, `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP` = `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`, `SCRTY_ID` = `SCRTY_ID`, `SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP` = `SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP`
  - through BIRD entities not stored in the data mart: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ASSGNMNT_IL
  - BIRD relationship(s): ASS_LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ASSGNMNT_ASSGND_ACCNTNG_CLSSFCTN_S_LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_39975_IL, ASS_LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_ASSGND_PRDNTL_PRTFL_S_SCRTY_PSTN_PRDNTL_PRTFL_ASSGNMNT_26869_IL
- belongs to [SCRTY_EXCHNG_TRDBL_DRVTV_IL](SCRTY_EXCHNG_TRDBL_DRVTV_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`, `SCRTY_EXCHNG_TRDBL_DRVTV_ID` = `SCRTY_ID`
  - through BIRD entities not stored in the data mart: BLNC_SHT_RCGNSD_NN_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL, SCRTY_PSTN_IL
  - BIRD relationship(s): ASS_BLNC_SHT_RCGNSD_SCRTY_PSTN_LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_34797_IL, ASS_SCRTY_INVLVD_SCRTY_PSTN_30258_IL, ASS_SCRTY_PSTN_BLNC_SHT_NN_BLNC_SHT_RCGNSD_28454_IL

## Code lists

### INVSTR_ENTTY_RL_TYP: Entity role type

| Code value | Code | Name |
|---|---|---|
| `ENTTY_RL_TYP_19` | 19 | Lessee |
| `ENTTY_RL_TYP_20` | 20 | Seller |
| `ENTTY_RL_TYP_27` | 27 | Deposit-taking corporation |
| `ENTTY_RL_TYP_28` | 28 | Loan debtor |
| `ENTTY_RL_TYP_8` | 8 | Issuer |

### LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP: Long balance sheet recognised security position accounting standard type

| Code value | Code | Name |
|---|---|---|
| `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3` | 3 | Long balance sheet recognised security position International Financial Reporting Standard (IFRS) |
| `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4` | 4 | Long balance sheet recognised security position national general accepted accounting principles (nGAAP) |

### HLD_SL_INDCTR: Held for sale

| Code value | Code | Name |
|---|---|---|
| `HLD_SL_INDCTR_1` | 1 | Held for sale |
| `HLD_SL_INDCTR_2` | 2 | Not held for sale |
