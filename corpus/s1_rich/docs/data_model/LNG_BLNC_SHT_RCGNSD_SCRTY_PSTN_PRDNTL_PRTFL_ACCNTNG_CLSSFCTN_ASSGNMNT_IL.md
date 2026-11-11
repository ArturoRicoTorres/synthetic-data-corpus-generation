# Long balance sheet recognised security position prudential portfolio Accounting classification assignment (LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL)

A Long balance sheet recognised security position prudential portfolio Accounting classification assignment is
the combination between Long balance sheet recognised security position prudential portfolio assignment and
Accounting classifcation.

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
| `PRDNTL_PRTFL_TYP` | [Prudential portfolio type](../../../shared/regulatory/glossary.md#prudential-portfolio-type) | VARCHAR(255) | PK | A discriminator to distinguish between trading and banking (or non-trading) book. |
| `ACCNTNG_CLSSFCTN` | [Accounting classification](../../../shared/regulatory/glossary.md#accounting-classification) | VARCHAR(255) | PK | Accounting portfolio where the instrument is recorded in accordance with the accounting standard – IFRS or national GAAP –under Regulation (EU) 2015/534 (ECB/2015/13) applied by the observed agent's legal entity. |
| `SBJCT_IMPRMNT_INDCTR` | [Subject to impairment indicator](../../../shared/regulatory/glossary.md#subject-to-impairment-indicator) | VARCHAR(255) |  | Subject to impairment indicator indicates whether the asset is subject to impairment or not. |
| `IMPRMNT_STTS` | [Impairment status](../../../shared/regulatory/glossary.md#impairment-status) | VARCHAR(255) |  | Type of impairment recorded in accordance with the accounting standard – IFRS or national GAAP. |
| `CRRYNG_AMNT` | [Carrying amount](../../../shared/regulatory/glossary.md#carrying-amount) | NUMERIC(18, 2) |  | The carrying amount in accordance with Annex V to Implementing Regulation (EU) No 680/2014. |
| `ACCMLTD_IMPRMNT` | [Accumulated impairment](../../../shared/regulatory/glossary.md#accumulated-impairment) | NUMERIC(18, 2) |  | The amount of loss allowances that are held against or are allocated to the instrument on the reporting reference date. This data attribute applies to instruments subject to impairment under the applied accounting standard. Under IFRS, the accumulated impairment relates to the following amounts: (i) loss allowance at an amount equal to 12-month expected credit losses; (ii) loss allowance at an amount equal to lifetime expected credit losses. Under GAAP, the accumulated impairment relates to the following amounts: (i) loss allowance at an amount equal to general allowances; (ii) loss allowance at an amount equal to specific allowances. |
| `FV` | [Fair value](../../../shared/regulatory/glossary.md#fair-value) | NUMERIC(18, 2) |  | Fair value as defined in IFRS 13.9. |
| `ACCMLTD_CHNGS_FV_CR` | [Accumulated changes in fair value due to credit risk](../../../shared/regulatory/glossary.md#accumulated-changes-in-fair-value-due-to-credit-risk) | NUMERIC(18, 2) |  | Accumulated changes in fair value due to credit risk in accordance with Part 2.46 of Annex V to Implementing Regulation (EU) No 680/2014. |
| `GNRL_ALLWNCS_CRDT_RSK` | [General allowances for credit risk affecting carrying amount (nGAAP)](../../../shared/regulatory/glossary.md#general-allowances-for-credit-risk-affecting-carrying-amount-ngaap) | NUMERIC(18, 2) |  | General allowances for credit risk affecting carrying amount (nGAAP) |
| `GNRL_ALLWNCS_BNK_RSK` | [General allowances for bank risk affecting carrying amount (nGAAP)](../../../shared/regulatory/glossary.md#general-allowances-for-bank-risk-affecting-carrying-amount-ngaap) | NUMERIC(18, 2) |  | General allowances for bank risk affecting carrying amount (nGAAP) |

## Relationships

- belongs to [LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL](LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `INVSTR_ENTTY_RL_TYP` = `INVSTR_ENTTY_RL_TYP`, `INVSTR_PRTY_ID` = `INVSTR_PRTY_ID`, `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP` = `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`, `SCRTY_ID` = `SCRTY_ID`, `SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP` = `SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP`
  - through BIRD entities not stored in the data mart: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ASSGNMNT_IL
  - BIRD relationship(s): ASS_LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ASSGNMNT_ASSGND_ACCNTNG_CLSSFCTN_S_LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_39975_IL, ASS_LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_ASSGND_PRDNTL_PRTFL_S_SCRTY_PSTN_PRDNTL_PRTFL_ASSGNMNT_26869_IL

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

### ACCNTNG_CLSSFCTN: Accounting classification

| Code value | Code | Name |
|---|---|---|
| `ACCNTNG_CLSSFCTN_2` | 2 | IFRS: Financial assets held for trading |
| `ACCNTNG_CLSSFCTN_3` | 3 | nGAAP: Trading Financial assets |
| `ACCNTNG_CLSSFCTN_4` | 4 | IFRS: Financial assets designated at fair value through profit or loss |
| `ACCNTNG_CLSSFCTN_41` | 41 | IFRS: Non-trading financial assets mandatorily at fair value through profit or loss |
| `ACCNTNG_CLSSFCTN_44` | 44 | nGAAP: Financial assets designated at fair value through profit or loss, measured using the cost-based method or LOCOM |
| `ACCNTNG_CLSSFCTN_49` | 49 | nGAAP: Financial assets designated at fair value through profit or loss, not measured using the cost-based method or LOCOM |
| `ACCNTNG_CLSSFCTN_6` | 6 | IFRS: Financial assets at amortised cost |
| `ACCNTNG_CLSSFCTN_7` | 7 | nGAAP: Non-trading non-derivative financial assets measured at fair value through profit or loss |
| `ACCNTNG_CLSSFCTN_73` | 73 | nGAAP: Other non-trading non-derivative financial assets. LOCOM |
| `ACCNTNG_CLSSFCTN_74` | 74 | nGAAP: Other non-trading non-derivative financial assets. Other than LOCOM |
| `ACCNTNG_CLSSFCTN_76` | 76 | nGAAP: Non-trading non-derivative financial assets measured at a cost-based method. LOCOM |
| `ACCNTNG_CLSSFCTN_77` | 77 | nGAAP: Non-trading non-derivative financial assets measured at a cost-based method. Other than LOCOM |
| `ACCNTNG_CLSSFCTN_8` | 8 | IFRS: Financial assets at fair value through other comprehensive income |
| `ACCNTNG_CLSSFCTN_9` | 9 | nGAAP: Non-trading non-derivative financial assets measured at fair value to equity |

### SBJCT_IMPRMNT_INDCTR: Subject to impairment indicator

| Code value | Code | Name |
|---|---|---|
| `SBJCT_IMPRMNT_INDCTR_1` | 1 | Subject to impairment |
| `SBJCT_IMPRMNT_INDCTR_2` | 2 | Not subject to impairment |

### IMPRMNT_STTS: Credit quality

| Code value | Code | Name |
|---|---|---|
| `CRDT_QLTY_1` | 1 | Non-performing |
| `CRDT_QLTY_11` | 11 | Performing |
| `CRDT_QLTY_211` | 211 | General allowances for credit risk |
| `CRDT_QLTY_212` | 212 | General allowances for banking risk |
| `CRDT_QLTY_26` | 26 | Specific allowances (GAAP) |
