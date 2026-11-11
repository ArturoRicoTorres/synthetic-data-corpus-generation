# BIRD definitions

Definitions of the BIRD variables and code values used in the reporting data mart, verbatim from the ECB BIRD
metadata (FINREP 4.3). Legal references are given as published there; see the register for the status of each
document.

## Variables

<a id="accmltd-chngs-fv-cr"></a>
### Accumulated changes in fair value due to credit risk (`ACCMLTD_CHNGS_FV_CR`)

Accumulated changes in fair value due to credit risk in accordance with Part 2.46 of Annex V to Implementing
Regulation (EU) No 680/2014.

- Domain: Monetary (`MNTRY`)
- Legal reference: [REG_EU_680_2014](register.md#reg-eu-680-2014) Part 2.46 of Annex V to Implementing Regulation (EU) No 680/2014

<a id="accmltd-imprmnt"></a>
### Accumulated impairment (`ACCMLTD_IMPRMNT`)

The amount of loss allowances that are held against or are allocated to the instrument on the reporting
reference date. This data attribute applies to instruments subject to impairment under the applied accounting
standard. Under IFRS, the accumulated impairment relates to the following amounts: (i) loss allowance at an
amount equal to 12-month expected credit losses; (ii) loss allowance at an amount equal to lifetime expected
credit losses. Under GAAP, the accumulated impairment relates to the following amounts: (i) loss allowance at
an amount equal to general allowances; (ii) loss allowance at an amount equal to specific allowances.

- Domain: Monetary (`MNTRY`)

<a id="accntng-clssfctn"></a>
### Accounting classification (`ACCNTNG_CLSSFCTN`)

Accounting portfolio where the instrument is recorded in accordance with the accounting standard – IFRS or
national GAAP –under Regulation (EU) 2015/534 (ECB/2015/13) applied by the observed agent's legal entity.

- Domain: Accounting classification (`ACCNTNG_CLSSFCTN`)
- Legal reference: [REG_EU_534_2015](register.md#reg-eu-534-2015) Regulation (EU) 2015/534 (ECB/2015/13)

<a id="accntng-cnsldtn-lvl"></a>
### Accounting consolidation level (`ACCNTNG_CNSLDTN_LVL`)

Accounting consolidation level is the level on which the accounting is consolidated, Solo or group.

- Domain: Accounting consolidation level (`ACCNTNG_CNSLDTN_LVL`)

<a id="accntng-hdg-indctr"></a>
### Accounting hedge indicator (`ACCNTNG_HDG_INDCTR`)

An indicator specifying if the hedge is considered an accounting hedge or not.

- Domain: Accounting hedge indicator (`ACCNTNG_HDG_INDCTR`)

<a id="accntng-stndrd"></a>
### Accounting standard (`ACCNTNG_STNDRD`)

Accounting standard

- Domain: Accounting framework (`ACCNTNG_FRMWRK`)

<a id="crryng-amnt"></a>
### Carrying amount (`CRRYNG_AMNT`)

The carrying amount in accordance with Annex V to Implementing Regulation (EU) No 680/2014.

- Domain: Monetary (`MNTRY`)
- Legal reference: [REG_EU_680_2014](register.md#reg-eu-680-2014) Annex V to Implementing Regulation (EU) No 680/2014

<a id="dbt-scrty-prfrmng-stts-typ"></a>
### Debt security by Performing status type (`DBT_SCRTY_PRFRMNG_STTS_TYP`)

Performing status in accordance with Implementing Regulation (EU) No 680/2014.

- Domain: Security or exchange tradable derivative type (`SCRTY_EXCHNG_TRDBL_DRVTV_TYP`)

<a id="dt-rfrnc"></a>
### Reference date (`DT_RFRNC`)

Reporting agents shall report credit data as recorded on the following reporting reference dates: (a) for
monthly transmissions, on the last day of each month; (b) for quarterly transmissions, on the last day of
March, June, September and December.

- Domain: Date (`DT`)

<a id="entty-rl-typ"></a>
### Entity role type (`ENTTY_RL_TYP`)

A discriminator to distinguish between party roles, organisation roles, central bank and private sector
company roles and legal person roles.

- Domain: Entity role type (`ENTTY_RL_TYP`)

<a id="fnrp-rprtng-schm"></a>
### Finrep reporting scheme (`FNRP_RPRTNG_SCHM`)

Finrep reporting scheme

- Domain: Finrep reporting scheme (`FNRP_RPRTNG_SCHM`)

<a id="fv"></a>
### Fair value (`FV`)

Fair value as defined in IFRS 13.9.

- Domain: Monetary (`MNTRY`)

<a id="gnrl-allwncs-bnk-rsk"></a>
### General allowances for bank risk affecting carrying amount (nGAAP) (`GNRL_ALLWNCS_BNK_RSK`)

General allowances for bank risk affecting carrying amount (nGAAP)

- Domain: Monetary (`MNTRY`)

<a id="gnrl-allwncs-crdt-rsk"></a>
### General allowances for credit risk affecting carrying amount (nGAAP) (`GNRL_ALLWNCS_CRDT_RSK`)

General allowances for credit risk affecting carrying amount (nGAAP)

- Domain: Monetary (`MNTRY`)

<a id="grp-id"></a>
### Group ID (`GRP_ID`)

RIAD Code of the head entity of group concatenated with the type of group, for example DE00001.A (Entity with
RIAD Code DE00001 is the head of the Type A group).

- Domain: String (`STRNG`)

<a id="grp-rl-typ"></a>
### Internal group role type (`GRP_RL_TYP`)

A discriminator to distinguish between different roles a group may act in.

- Domain: Group role type (`GRP_RL_TYP`)

<a id="grss-crryng-amnt"></a>
### Gross carrying amount (`GRSS_CRRYNG_AMNT`)

Gross carrying amount as defined in Annex V 5.2.

- Domain: Monetary (`MNTRY`)

<a id="hld-sl-indctr"></a>
### Held for sale indicator (`HLD_SL_INDCTR`)

A variable indicating the Non-current assets and instruments in disposal groups classified as held for sale in
accordance with IFRS5. Is not applicable under national GAAP based on BAD.

- Domain: Held for sale (`HLD_SL_INDCTR`)

<a id="imprmnt-stts"></a>
### Impairment status (`IMPRMNT_STTS`)

Type of impairment recorded in accordance with the accounting standard – IFRS or national GAAP.

- Domain: Credit quality (`CRDT_QLTY`)

<a id="instrmnt-id"></a>
### Instrument identifier (`INSTRMNT_ID`)

An identifier applied by the reporting agent to uniquely identify each instrument under a single contract.
Each instrument must have one instrument identifier. This value will not change over time and cannot be used
as the instrument identifier for any other instrument under the same contract.

- Domain: String (`STRNG`)

<a id="instrmnt-rl-typ"></a>
### Instrument role type (`INSTRMNT_RL_TYP`)

A discriminator to distinguish between different roles an instrument may act in. Examples are financial asset
instrument, financial liability instrument.

- Domain: Abstract instrument role type (`ABSTRCT_INSTRMNT_RL_TYP`)

<a id="instrmnt-typ-prdct"></a>
### Instrument type by product (`INSTRMNT_TYP_PRDCT`)

A discriminator to distinguish instruments by product. Examles are loans and advances, securities financing
transactions, financial guarantees and other commitments or over the counter derivatives.

- Domain: Type of instrument (`TYP_INSTRMNT`)

<a id="instttnl-sctr"></a>
### Institutional sector (`INSTTTNL_SCTR`)

Institutional sectors in accordance with Regulation (EU) No 549/2013, Regulation (EU) No 575/2013 and
Regulation (EU) No 1075/2013 of the European Central Bank (ECB/2013/40)(1).

- Domain: Institutional sectors (`INSTTTNL_SCTR`)
- Legal reference: [CRR_REGULATION](register.md#crr-regulation) Regulation (EU) No 575/2013
- Legal reference: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013
- Legal reference: [REG_EU_1075_2013](register.md#reg-eu-1075-2013) Regulation (EU) No 1075/2013 of the European Central Bank (ECB/2013/40)(1)

<a id="invstr-entty-rl-typ"></a>
### Investor Entity role type (`INVSTR_ENTTY_RL_TYP`)

The investor role.

- Domain: Entity role type (`ENTTY_RL_TYP`)

<a id="invstr-prty-id"></a>
### Investor Party identifier (`INVSTR_PRTY_ID`)

The party identifier of the involved investor.

- Domain: String (`STRNG`)

<a id="lng-shrt-blnc-sht-rcgnsd-scrty-pstn-typ"></a>
### Long/Short balance sheet recognised security position type (`LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP`)

Long/Short balance sheet recognised security position type defines whether a long/short balance sheet
recognised security position is long or short.

- Domain: Long balance sheet recognised security position accounting standard type (`LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP`)

<a id="mltltrl-dvlpmnt-bnk-indctr"></a>
### Multilateral development bank indicator (`MLTLTRL_DVLPMNT_BNK_INDCTR`)

Multilateral development bank indicator specifies if the International organisation is a multilateral
development bank or not.

- Domain: Multilateral development bank indicator (`MLTLTRL_DVLPMNT_BNK_INDCTR`)

<a id="mn-dbtr-indctr"></a>
### Main debtor indicator (`MN_DBTR_INDCTR`)

An indicator specifying if a debtor is the main debtor.

- Domain: Main debtor indicator (`MN_DBTR_INDCTR`)

<a id="mn-dpst-tkng-crprtn-indctr"></a>
### Main Deposit-taking corporation indicator (`MN_DPST_TKNG_CRPRTN_INDCTR`)

An indicator specifying if a debtor is the main debtor.

- Domain: Main Deposit-taking corporation indicator (`MN_DPST_TKNG_CRPRTN_INDCTR`)

<a id="mn-lss-indctr"></a>
### Main lessee indicator (`MN_LSS_INDCTR`)

An indicator specifying if a debtor is the main debtor.

- Domain: Main lessee indicator (`MN_LSS_INDCTR`)

<a id="ngtbl-scrty-indctr"></a>
### Negotiable security indicator (`NGTBL_SCRTY_INDCTR`)

An indicator specifying is a security is listed or not.

- Domain: Negotiable security (`NGTBL_SCRTY`)

<a id="prdntl-prtfl-typ"></a>
### Prudential portfolio type (`PRDNTL_PRTFL_TYP`)

A discriminator to distinguish between trading and banking (or non-trading) book.

- Domain: Prudential portfolio (`PRDNTL_PRTFL_TYP`)

<a id="prfrmng-stts"></a>
### Performing status (`PRFRMNG_STTS`)

Performing status in accordance with Implementing Regulation (EU) No 680/2014.

- Domain: Credit quality (`CRDT_QLTY`)
- Legal reference: [REG_EU_680_2014](register.md#reg-eu-680-2014) Regulation (EU) No 680/2014

<a id="prmry-issr-indctr"></a>
### Primary issuer indicator (`PRMRY_ISSR_INDCTR`)

Primary issuer indicator

- Domain: Primary issuer indicator (`PRMRY_ISSR_INDCTR`)

<a id="prty-id"></a>
### Party identifier (`PRTY_ID`)

An identifier that uniquely identifies a party.

- Domain: String (`STRNG`)

<a id="rprtng-agnt-id"></a>
### Reporting agent identifier (`RPRTNG_AGNT_ID`)

Reporting agent identifier

- Domain: String (`STRNG`)

<a id="rpymnt-rghts"></a>
### Repayment rights (`RPYMNT_RGHTS`)

Classification of credit exposures according to the creditor's rights to claim the repayment of the exposure.
On demand or at short notice

- Domain: Repayment rights (`RPYMNT_RGHTS`)

<a id="sbjct-imprmnt-indctr"></a>
### Subject to impairment indicator (`SBJCT_IMPRMNT_INDCTR`)

Subject to impairment indicator indicates whether the asset is subject to impairment or not.

- Domain: Subject to impairment indicator (`SBJCT_IMPRMNT_INDCTR`)

<a id="scrty-exchng-trdbl-drvtv-id"></a>
### Security and exchange tradable derivative identifier (`SCRTY_EXCHNG_TRDBL_DRVTV_ID`)

An identifier to uniquely identify each security.

- Domain: String (`STRNG`)

<a id="scrty-exchng-trdbl-drvtv-typ"></a>
### Security and exchange tradable derivative type (`SCRTY_EXCHNG_TRDBL_DRVTV_TYP`)

A discriminator to distinguish between securities and exchange tradable derivatives.

- Domain: Security or exchange tradable derivative type (`SCRTY_EXCHNG_TRDBL_DRVTV_TYP`)

<a id="scrty-id"></a>
### Security identifier (`SCRTY_ID`)

An identifier to uniquely identify each security.

- Domain: String (`STRNG`)

<a id="scrty-pstn-blnc-sht-rcgnsd-typ"></a>
### Security position Balance sheet recognised type (`SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP`)

Security position Balance sheet recognised indicator defines whether a security position is recognised in the
balance sheet or non recognised in the balance sheet

- Domain: Security position Balance sheet recognised type (`SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP`)

<a id="typ-fnncl-asst-instrmnt-annx-v"></a>
### Type of Financial Asset Instrument according to Annex V (`TYP_FNNCL_ASST_INSTRMNT_ANNX_V`)

Type of Financial Asset Instrument according to Annex V

- Domain: Type of instrument (`TYP_INSTRMNT`)

## Code values

### Abstract instrument role type (`ABSTRCT_INSTRMNT_RL_TYP`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `ABSTRCT_INSTRMNT_RL_TYP_102` | 102 | Non-balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP) | Non-balance sheet recognised financial asset instrument national general accepted accounting principles (nGAAP) |
| `ABSTRCT_INSTRMNT_RL_TYP_34` | 34 | Balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP) | Balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP) |
| `ABSTRCT_INSTRMNT_RL_TYP_35` | 35 | Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS) | Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS) |

### Accounting classification (`ACCNTNG_CLSSFCTN`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `ACCNTNG_CLSSFCTN_2` | 2 | IFRS: Financial assets held for trading | Financial assets held for trading in accordance with IFRS. |
| `ACCNTNG_CLSSFCTN_3` | 3 | nGAAP: Trading Financial assets | Trading financial assets in accordance with national GAAP. |
| `ACCNTNG_CLSSFCTN_4` | 4 | IFRS: Financial assets designated at fair value through profit or loss | Financial assets measured at fair value through profit and loss and designated as such upon initial recognition or subsequently in accordance with IFRS, except those classified as financial assets held for trading. |
| `ACCNTNG_CLSSFCTN_41` | 41 | IFRS: Non-trading financial assets mandatorily at fair value through profit or loss | Non-trading financial assets mandatorily at fair value through profit or loss in accordance with IFRS. |
| `ACCNTNG_CLSSFCTN_44` | 44 | nGAAP: Financial assets designated at fair value through profit or loss, measured using the cost-based method or LOCOM | nGAAP: Financial assets designated at fair value through profit or loss, measured using the cost-based method or LOCOM |
| `ACCNTNG_CLSSFCTN_49` | 49 | nGAAP: Financial assets designated at fair value through profit or loss, not measured using the cost-based method or LOCOM | nGAAP: Financial assets designated at fair value through profit or loss, measured using the cost-based method or LOCOM |
| `ACCNTNG_CLSSFCTN_6` | 6 | IFRS: Financial assets at amortised cost | Financial assets measured at amortised cost in accordance with IFRS. |
| `ACCNTNG_CLSSFCTN_7` | 7 | nGAAP: Non-trading non-derivative financial assets measured at fair value through profit or loss | Non-trading non-derivative financial assets measured at fair value to equity in accordance with national GAAP. |
| `ACCNTNG_CLSSFCTN_73` | 73 | nGAAP: Other non-trading non-derivative financial assets. LOCOM | nGAAP: Other non-trading non-derivative financial assets at LOCOM |
| `ACCNTNG_CLSSFCTN_74` | 74 | nGAAP: Other non-trading non-derivative financial assets. Other than LOCOM | nGAAP: Other non-trading non-derivative financial assets. Other than LOCOM |
| `ACCNTNG_CLSSFCTN_76` | 76 | nGAAP: Non-trading non-derivative financial assets measured at a cost-based method. LOCOM | nGAAP: Non-trading non-derivative financial assets measured at a cost-based method at LOCOM |
| `ACCNTNG_CLSSFCTN_77` | 77 | nGAAP: Non-trading non-derivative financial assets measured at a cost-based method. Other than LOCOM | nGAAP: Non-trading non-derivative financial assets measured at a cost-based method. Other than LOCOM |
| `ACCNTNG_CLSSFCTN_8` | 8 | IFRS: Financial assets at fair value through other comprehensive income | Financial assets measured at fair value through other comprehensive income due to business model and cash-flows characteristics in accordance with IFRS. |
| `ACCNTNG_CLSSFCTN_9` | 9 | nGAAP: Non-trading non-derivative financial assets measured at fair value to equity | Non-trading non-derivative financial assets measured at fair value to equity in accordance with national GAAP. |

### Accounting consolidation level (`ACCNTNG_CNSLDTN_LVL`)

| Code value | Code | Name | Description |
|---|---|---|---|

### Accounting framework (`ACCNTNG_FRMWRK`)

| Code value | Code | Name | Description |
|---|---|---|---|

### Accounting hedge indicator (`ACCNTNG_HDG_INDCTR`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `ACCNTNG_HDG_INDCTR_1` | 1 | Accounting hedge | Accounting hedge |
| `ACCNTNG_HDG_INDCTR_2` | 2 | Not accounting hedge | Not accounting hedge |

### Credit quality (`CRDT_QLTY`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `CRDT_QLTY_1` | 1 | Non-performing | Non-performing |
| `CRDT_QLTY_11` | 11 | Performing | Performing |
| `CRDT_QLTY_211` | 211 | General allowances for credit risk | General allowances for credit risk |
| `CRDT_QLTY_212` | 212 | General allowances for banking risk | General allowances for banking risks |
| `CRDT_QLTY_26` | 26 | Specific allowances (GAAP) | To be used if the instrument is subject to impairment in accordance with an applied accounting standard other than IFRS 9 and specific loss allowances are raised, irrespective of whether these allowances are individually or collectively assessed (impaired). |

### Entity role type (`ENTTY_RL_TYP`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `ENTTY_RL_TYP_19` | 19 | Lessee | Lessee |
| `ENTTY_RL_TYP_20` | 20 | Seller | Seller |
| `ENTTY_RL_TYP_27` | 27 | Deposit-taking corporation | Deposit taking corporation |
| `ENTTY_RL_TYP_28` | 28 | Loan debtor | Loan debtor |
| `ENTTY_RL_TYP_8` | 8 | Issuer | Issuer |

### Finrep reporting scheme (`FNRP_RPRTNG_SCHM`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `FNRP_RPRTNG_SCHM_1` | 1 | Full | Full |
| `FNRP_RPRTNG_SCHM_2` | 2 | Simplified | Simplified |
| `FNRP_RPRTNG_SCHM_3` | 3 | Over-simplified | Over-simplified |

### Group role type (`GRP_RL_TYP`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `GRP_RL_TYP_1` | 1 | Reporting agent internal group role | Reporting agent internal group role |

### Held for sale (`HLD_SL_INDCTR`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `HLD_SL_INDCTR_1` | 1 | Held for sale | The member indicates that the instrument is held for sale |
| `HLD_SL_INDCTR_2` | 2 | Not held for sale | The member indicates that the instrument is not held for sale |

### Institutional sectors (`INSTTTNL_SCTR`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `INSTTTNL_SCTR_IO` | IO | International organisations | International organisations |
| `INSTTTNL_SCTR_S11` | S11 | Non financial corporations | It corresponds to sector S.11, as defined in Regulation (EU) No 549/2013 (paragraphs 2.45 to 2.50 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S121` | S121 | Central banks | It corresponds to subsector S.121, as defined in Regulation (EU) No 549/2013 (paragraphs 2.72 to 2.74 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S122_A` | S122_A | Credit institutions | Credit institutions as defined in Article 4(1)(1) of Regulation (EU) No 575/2013. |
| `INSTTTNL_SCTR_S122_A_1` | S122_A_1 | Credit institutions not including entities according to the article 2.5 Directive 2013/36/EU | Credit institutions not including entities according to the article 2.5 Directive 2013/36/EU |
| `INSTTTNL_SCTR_S122_A_2` | S122_A_2 | Credit institutions according to the article 2.5 Directive 2013/36/EU | Credit institutions according to the article 2.5 Directive 2013/36/EU |
| `INSTTTNL_SCTR_S122_B1` | S122_B1 | Electronic money institutions principally engaged in financial intermediation | Electronic money institutions, as defined in Directive 2009/110/EC [article 2(1)], that are principally engaged in financial intermediation, as defined in Regulation (EU) no 549/2013 (paragraph 2.56 of Annex A). |
| `INSTTTNL_SCTR_S122_B2` | S122_B2 | Deposit-taking corporations except the central bank, other than credit institutions and electronic money institutions | It corresponds to subsector S.122, as defined in Regulation (EU) No 549/2013 (paragraphs 2.75 to 2.78 of Annex A), extended to the rest of the world, other than credit institutions, as defined in Article 4(1)(1) of Regulation (EU) No 575/2013, and electronic money institutions, as defined in Directive 2009/110/EC [article 2(1)]. |
| `INSTTTNL_SCTR_S123` | S123 | Money Market Funds (MMFs) | It corresponds to subsector S.123, as defined in Regulation (EU) No 549/2013 (paragraphs 2.79 to 2.81 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S124` | S124 | Non-MMF investment funds | It corresponds to subsector S.124, as defined in Regulation (EU) No 549/2013 (paragraphs 2.82 to 2.85 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S125_A` | S125_A | Financial Vehicle Corporations (FVCs) | FVCs as defined in Article 1 of Regulation (EU) No 1075/2013. |
| `INSTTTNL_SCTR_S125_B` | S125_B | Security and derivative dealers | Security and derivative dealers as defined in Regulation (EU) No 549/2013 (paragraph 2.91 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S125_C` | S125_C | Financial corporations engaged in lending | Financial corporations engaged in lending as defined in Regulation (EU) No 549/2013 (paragraph 2.92 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S125_D` | S125_D | Specialised financial corporations other than CCPs | Specialised financial corporations, as defined in Regulation (EU) No 549/2013 (paragraph 2.93 of Annex A), extended to the rest of the world, other than CCPs, as defined in point (1) of Article 2 of Regulation (EU) No 648/2012. |
| `INSTTTNL_SCTR_S125_E` | S125_E | Central Counterparties (CCPs) | CCPs as defined in point (1) of Article 2 of Regulation (EU) No 648/2012. |
| `INSTTTNL_SCTR_S125_I` | S125_I | Other financial intermediaries, except insurance corporations and pension funds, other than CCPs, FVCs, security and derivative dealers, financial corporations engaged in lending and specialised financial corporations | It corresponds to subsector S.125, as defined in Regulation (EU) No 549/2013 (paragraphs 2.86 to 2.94 of Annex A), extended to the rest of the world, other than CCPs, as defined in point (1) of Article 2 of Regulation (EU) No 648/2012, FVCs, as defined in Article 1 of Regulation (EU) No 1075/2013, and security and derivative dealers, financial corporations engaged in lending and specialised financial corporations, as defined in Regulation (EU) No 549/2013 (paragraphs 2.91, 2.92 and 2.93, respectively, of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S125_W` | S125_W | Other financial corporations excluding financial vehicle corporations | Other financial corporations excluding financial vehicle corporations |
| `INSTTTNL_SCTR_S127` | S127 | Captive financial institutions and money lenders | It corresponds to subsector S.127, as defined in Regulation (EU) No 549/2013 (paragraphs 2.98 to 2.99 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S128` | S128 | Insurance corporations | It corresponds to subsector S.128, as defined in Regulation (EU) No 549/2013 (paragraphs 2.100 to 2.104 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S129` | S129 | Pension funds | It corresponds to subsector S.129, as defined in Regulation (EU) No 549/2013 (paragraphs 2.105 to 2.110 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S1311` | S1311 | Central government (excluding social security funds) | It corresponds to subsector S.1311, as defined in Regulation (EU) No 549/2013 (paragraph 2.114 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S1312` | S1312 | State government (excluding social security funds) | It corresponds to subsector S.1312, as defined in Regulation (EU) No 549/2013 (paragraph 2.115 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S1313` | S1313 | Local government (excluding social security funds) | It corresponds to subsector S.1313, as defined in Regulation (EU) No 549/2013 (paragraph 2.116 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S1314` | S1314 | Social security funds | It corresponds to subsector S.1314, as defined in Regulation (EU) No 549/2013 (paragraph 2.117 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S14_A` | S14_A | Households that are sole proprietorships/partnerships without legal status | Sole proprietorships and partnerships without legal status included in the sector S.14, as defined in Regulation (EU) No 549/2013 (paragraphs 2.118 to 2.121 of Annex A), extended to the rest of the world. |
| `INSTTTNL_SCTR_S14_B` | S14_B | Households other than sole proprietorships/partnerships without legal status | It corresponds to sector S.14, as defined in Regulation (EU) No 549/2013 (paragraphs 2.118 to 2.121 of Annex A), extended to the rest of the world, other than sole proprietorships and partnerships without legal status. |
| `INSTTTNL_SCTR_S15` | S15 | Non profit institutions serving households | It corresponds to sector S.15, as defined in Regulation (EU) No 549/2013 (paragraphs 2.129 to 2.130 of Annex A), extended to the rest of the world. |

Legal references:
- `INSTTTNL_SCTR_S11`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013 (paragraphs 2.45 to 2.50 of Annex A)
- `INSTTTNL_SCTR_S121`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Subsector S.121, as defined in Regulation (EU) No 549/2013 (paragraphs 2.72 to 2.74 of Annex A)
- `INSTTTNL_SCTR_S122_A`: [CRR_REGULATION](register.md#crr-regulation) Article 4(1)(1) of Regulation (EU) No 575/2013
- `INSTTTNL_SCTR_S122_A_1`: [REG_EU_1071_2013](register.md#reg-eu-1071-2013) Article 9(1) of Regulation ECB/2013/33
- `INSTTTNL_SCTR_S122_A_2`: [CRD_IV_DIRECTIVE](register.md#crd-iv-directive) Article 2.5 Directive 2013/36/EU
- `INSTTTNL_SCTR_S122_B1`: [DIR_EC_110_2009](register.md#dir-ec-110-2009) Directive 2009/110/EC [article 2(1)]
- `INSTTTNL_SCTR_S122_B2`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Subsector S.122, as defined in Regulation (EU) No 549/2013 (paragraphs 2.75 to 2.78 of Annex A)
- `INSTTTNL_SCTR_S123`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Subsector S.123, as defined in Regulation (EU) No 549/2013 (paragraphs 2.79 to 2.81 of Annex A)
- `INSTTTNL_SCTR_S124`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Subsector S.127, as defined in Regulation (EU) No 549/2013 (paragraphs 2.98 to 2.99 of Annex A)
- `INSTTTNL_SCTR_S125_A`: [REG_EU_1075_2013](register.md#reg-eu-1075-2013) Article 1 of Regulation (EU) No 1075/2013
- `INSTTTNL_SCTR_S125_B`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013
- `INSTTTNL_SCTR_S125_C`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013
- `INSTTTNL_SCTR_S125_D`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013 (paragraph 2.93 of Annex A)
- `INSTTTNL_SCTR_S125_E`: [REG_EU_648_2012](register.md#reg-eu-648-2012) Point (1) of Article 2 of Regulation (EU) No 648/2012
- `INSTTTNL_SCTR_S125_I`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013
- `INSTTTNL_SCTR_S127`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Subsector S.127, as defined in Regulation (EU) No 549/2013 (paragraphs 2.98 to 2.99 of Annex A)
- `INSTTTNL_SCTR_S128`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Subsector S.127, as defined in Regulation (EU) No 549/2013 (paragraphs 2.98 to 2.99 of Annex A)
- `INSTTTNL_SCTR_S129`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Subsector S.129, as defined in Regulation (EU) No 549/2013 (paragraphs 2.105 to 2.110 of Annex A)
- `INSTTTNL_SCTR_S1311`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013
- `INSTTTNL_SCTR_S1312`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013
- `INSTTTNL_SCTR_S1313`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Subsector S.1313, as defined in Regulation (EU) No 549/2013 (paragraph 2.116 of Annex A)
- `INSTTTNL_SCTR_S1314`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013
- `INSTTTNL_SCTR_S14_A`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Sector S.14, as defined in Regulation (EU) No 549/2013 (paragraphs 2.118 to 2.121 of Annex A)
- `INSTTTNL_SCTR_S14_B`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013
- `INSTTTNL_SCTR_S15`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Regulation (EU) No 549/2013 (paragraphs 2.129 to 2.130 of Annex A

### Long balance sheet recognised security position accounting standard type (`LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3` | 3 | Long balance sheet recognised security position International Financial Reporting Standard (IFRS) | Long balance sheet recognised security position International Financial Reporting Standard (IFRS) |
| `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4` | 4 | Long balance sheet recognised security position national general accepted accounting principles (nGAAP) | Long balance sheet recognised security position national general accepted accounting principles (nGAAP) |

### Multilateral development bank indicator (`MLTLTRL_DVLPMNT_BNK_INDCTR`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `MLTLTRL_DVLPMNT_BNK_INDCTR_1` | 1 | Multilateral development bank |  |

### Main debtor indicator (`MN_DBTR_INDCTR`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `MN_DBTR_INDCTR_1` | 1 | Main debtor | Main debtor |

### Main Deposit-taking corporation indicator (`MN_DPST_TKNG_CRPRTN_INDCTR`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `MN_DPST_TKNG_CRPRTN_INDCTR_1` | 1 | Main Deposit-taking corporation | Main Deposit-taking corporation |

### Main lessee indicator (`MN_LSS_INDCTR`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `MN_LSS_INDCTR_1` | 1 | Main lessee | Main lessee |

### Negotiable security (`NGTBL_SCRTY`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `NGTBL_SCRTY_1` | 1 | Negotiable security |  |
| `NGTBL_SCRTY_2` | 2 | Non-negotiable security |  |

### Prudential portfolio (`PRDNTL_PRTFL_TYP`)

| Code value | Code | Name | Description |
|---|---|---|---|

### Primary issuer indicator (`PRMRY_ISSR_INDCTR`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `PRMRY_ISSR_INDCTR_1` | 1 | Primary issuer | Primary issuer |

### Repayment rights (`RPYMNT_RGHTS`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `RPYMNT_RGHTS_1` | 1 | On demand or short notice | Instruments which are repayable on demand or at short notice at the request of the creditor. |
| `RPYMNT_RGHTS_2` | 2 | Other than on demand or short notice | Instruments subject to repayment rights other than on demand or at short notice. |

### Subject to impairment indicator (`SBJCT_IMPRMNT_INDCTR`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `SBJCT_IMPRMNT_INDCTR_1` | 1 | Subject to impairment | The member indicates that the financial asset is subject to impairment |
| `SBJCT_IMPRMNT_INDCTR_2` | 2 | Not subject to impairment | The member indicates that the financial asset is not subject to impairment |

### Security or exchange tradable derivative type (`SCRTY_EXCHNG_TRDBL_DRVTV_TYP`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_11` | 11 | Debt security without underlying assets | Debt security without underlying assets |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_13` | 13 | Asset backed security | Asset backed security |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_14` | 14 | Covered bond | Covered bond |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_19` | 19 | Performing debt security |  |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20` | 20 | Non-performing debt security |  |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_5` | 5 | Fund security | Fund security |
| `SCRTY_EXCHNG_TRDBL_DRVTV_TYP_6` | 6 | Equity security | Equity security |

### Security position Balance sheet recognised type (`SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP`)

| Code value | Code | Name | Description |
|---|---|---|---|

### Type of instrument (`TYP_INSTRMNT`)

| Code value | Code | Name | Description |
|---|---|---|---|
| `TYP_INSTRMNT_10` | 10 | Over the counter (OTC) Option other than Over the counter (OTC) Credit spread option | OTC Option other than OTC Credit spread option |
| `TYP_INSTRMNT_1020` | 1020 | Factoring | Factoring |
| `TYP_INSTRMNT_1022` | 1022 | Other loan | Loans as defined in point 5(112) to (138) of Annex A to Regulation (EU) No 549/2013 other than financial leases, reverse repurchase loans, credit card debt, current accounts (that are assets), factoring and other trade receivables. Please note that it also does not include Other deposits (w.r.t. ESA classification). |
| `TYP_INSTRMNT_1023` | 1023 | Other trade receivable | Trade receivables as defined in Regulation (EU) No 680/2014, Annex V, Part 2.41 (c) other than factoring. Among other things, this category includes outright purchase of trade receivables and discounting of invoices, bills of exchange and other claims. |
| `TYP_INSTRMNT_1112` | 1112 | Cash balances at central banks | Cash balances at central banks |
| `TYP_INSTRMNT_1113` | 1113 | Other demand deposits | Other demand deposits |
| `TYP_INSTRMNT_1114` | 1114 | Derivatives not hedge | Derivatives not hedge |
| `TYP_INSTRMNT_1115` | 1115 | Equity instruments | Equity instruments |
| `TYP_INSTRMNT_1116` | 1116 | Debt securities | Debt securities |
| `TYP_INSTRMNT_1117` | 1117 | Loans and Advances | Loans and Advances |
| `TYP_INSTRMNT_1118` | 1118 | Non-current assets and disposal groups classified as held for sale | Non-current assets and disposal groups classified as held for sale |
| `TYP_INSTRMNT_1119` | 1119 | Derivatives hedge | Derivatives hedge |
| `TYP_INSTRMNT_120` | 120 | Transit item | Transit items |
| `TYP_INSTRMNT_1201` | 1201 | On demand deposit used for minimum reserve | Loan on demand used for minimum reserve |
| `TYP_INSTRMNT_1202` | 1202 | On demand deposit not used for minimum reserve | On demand deposit not used for minimum reserve |
| `TYP_INSTRMNT_130` | 130 | Suspense item | Suspence items |
| `TYP_INSTRMNT_140` | 140 | Other advance | Advances that are not loans other than transit items and suspence items |
| `TYP_INSTRMNT_162` | 162 | Open repurchase transaction | Open repurchase transaction |
| `TYP_INSTRMNT_163` | 163 | Term repurchase transaction | Term Repurchase transaction |
| `TYP_INSTRMNT_2` | 2 | Equity instrument that is not a security | Equity instrument that is not a security |
| `TYP_INSTRMNT_380` | 380 | Over the counter (OTC) Forward | Forwards are derivative contracts between two parties to buy or to sell an asset at a specified future time at a price agreed upon today |
| `TYP_INSTRMNT_5` | 5 | Other over the counter (OTC) Derivative instrument | Other OTC Derivative instrument |
| `TYP_INSTRMNT_51` | 51 | Credit card debt | Credit card debt according to Regulation (EU) 1071/2013 concerning the balance sheet of the monetary financial institutions sector,  Annex II, Part 2, Instrument categories: "...this category comprises credit granted [...] either via delayed debit cards, i.e. cards providing convenience credit as defined below, or via credit cards, i.e. cards providing convenience credit and extended credit. .Credit card debt is recorded on dedicated card accounts and therefore not evident on current or overdraft accounts. Convenience credit is defined as the credit granted at an interest rate of 0 % in the period between the payment transactions effectuated with the card during one billing cycle and the date at which the debit balances from this specific billing cycle become due. Extended credit is defined as the credit granted after the due dates of the previous billing cycles have passed, i.e. debit amounts on the card account that have not been settled when this was first possible, for which an interest rate or tiered interest rates usually greater than 0 % are charged. Often minimum instalments per month have to be made, to at least partially repay extended credit. The counterpart to these forms of credit is the entity liable to eventually repay the amounts outstanding in accordance with the contractual agreement, which coincides with the cardholder in the case of privately used cards, but not in the case of company cards;" |
| `TYP_INSTRMNT_511` | 511 | Tranferable overnight deposits |  |
| `TYP_INSTRMNT_512` | 512 | Non-transferable overnight deposits | Non-transferable overnight deposits |
| `TYP_INSTRMNT_522` | 522 | Deposit with agreed maturity | Deposits with agreed maturity - other than counterpart liability to non-derecognised loans |
| `TYP_INSTRMNT_6` | 6 | Over the counter (OTC) Total return swap | OTC Total return swap |
| `TYP_INSTRMNT_7` | 7 | Over the counter (OTC) Credit default swap | OTC Credit default swap |
| `TYP_INSTRMNT_8` | 8 | Other over the counter (OTC) Swap | Other OTC Swap |
| `TYP_INSTRMNT_80` | 80 | Financial lease | Financial leases as defined in paragraphs 5.134 to 5.135 of Annex A to Regulation (EU) No 549/2013. |
| `TYP_INSTRMNT_9` | 9 | Over the counter (OTC) Credit spread option | OTC Credit spread option |

Legal references:
- `TYP_INSTRMNT_1022`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Point 5(112) to (138) of Annex A to Regulation (EU) No 549/2013
- `TYP_INSTRMNT_1023`: [REG_EU_680_2014](register.md#reg-eu-680-2014) Regulation (EU) No 680/2014, Annex V, Part 2.41 (c)
- `TYP_INSTRMNT_51`: [REG_EU_1071_2013](register.md#reg-eu-1071-2013) Regulation (EU) 1071/201
- `TYP_INSTRMNT_80`: [REG_EU_549_2013](register.md#reg-eu-549-2013) Paragraphs 5.134 to 5.135 of Annex A to Regulation (EU) No 549/2013
