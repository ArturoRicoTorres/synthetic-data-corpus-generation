# Glossary

General vocabulary of this corpus: the business terms of the reporting data mart, the labels of template F
18.00.a and the Annex V concepts they rely on, followed by the code values used. Definitions are quoted from
their source; each links to its entry in the register.

## Terms

<a id="accounting-classification"></a>
### Accounting classification

- BIRD variable `ACCNTNG_CLSSFCTN`: Accounting portfolio where the instrument is recorded in accordance with the accounting standard – IFRS or national GAAP –under Regulation (EU) 2015/534 (ECB/2015/13) applied by the observed agent's legal entity. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_534_2015](register.md#reg-eu-534-2015))

<a id="accounting-consolidation-level"></a>
### Accounting consolidation level

- BIRD variable `ACCNTNG_CNSLDTN_LVL`: Accounting consolidation level is the level on which the accounting is consolidated, Solo or group. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accounting-hedge-indicator"></a>
### Accounting hedge indicator

- BIRD variable `ACCNTNG_HDG_INDCTR`: An indicator specifying if the hedge is considered an accounting hedge or not. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accounting-portfolios"></a>
### Accounting portfolios

- Annex V, Part 1, paragraph 13: For the purposes of Annexes III and IV as well as this Annex, ‘accounting portfolios’ means financial instruments aggregated by valuation rules. Those aggregations shall not include investments in subsidiaries, joint ventures and associates, balances receivable on demand classified as ‘Cash, cash balances at central banks and other demand deposits’, nor financial instruments classified as ‘Held for sale’ presented in the items ‘Non-current assets and disposal groups classified as held for sale’ and ‘Liabilities included in disposal groups classified as held for sale’. (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="accounting-standard"></a>
### Accounting standard

- BIRD variable `ACCNTNG_STNDRD`: Accounting standard (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accumulated-changes-in-fair-value-due-to-credit-risk"></a>
### Accumulated changes in fair value due to credit risk

- BIRD variable `ACCMLTD_CHNGS_FV_CR`: Accumulated changes in fair value due to credit risk in accordance with Part 2.46 of Annex V to Implementing Regulation (EU) No 680/2014. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_680_2014](register.md#reg-eu-680-2014))

<a id="accumulated-impairment"></a>
### Accumulated impairment

- BIRD variable `ACCMLTD_IMPRMNT`: The amount of loss allowances that are held against or are allocated to the instrument on the reporting reference date. This data attribute applies to instruments subject to impairment under the applied accounting standard. Under IFRS, the accumulated impairment relates to the following amounts: (i) loss allowance at an amount equal to 12-month expected credit losses; (ii) loss allowance at an amount equal to lifetime expected credit losses. Under GAAP, the accumulated impairment relates to the following amounts: (i) loss allowance at an amount equal to general allowances; (ii) loss allowance at an amount equal to specific allowances. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="carrying-amount"></a>
### Carrying amount

- BIRD variable `CRRYNG_AMNT`: The carrying amount in accordance with Annex V to Implementing Regulation (EU) No 680/2014. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_680_2014](register.md#reg-eu-680-2014))
- Annex V, Part 1, paragraph 27: For the purposes of Annexes III and IV as well as this Annex, "the carrying amount" means the amount to be reported in the balance sheet. The carrying amount of financial instruments shall include accrued interest. Under the relevant national GAAP based on BAD, the carrying amount of derivatives either shall be the carrying amount under national GAAP including accruals, premium values and provisions if applicable, or it shall be equal to zero where derivatives are not recognised on-balance sheet. (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="cash-balances-at-central-banks"></a>
### Cash balances at central banks

- Annex V, Part 2, paragraph 2: ‘Cash balances at central banks’ shall include ‘loans and advances’ that are balances receivable on demand at central banks. (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="central-banks"></a>
### Central banks

- Template F 18.00.a row 0080: Label of row 0080 of template F 18.00.a. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))
- Annex V, Part 1, paragraph 42(a): (a) central banks; (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="credit-institutions"></a>
### Credit institutions

- Template F 18.00.a row 0100: Label of row 0100 of template F 18.00.a. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))
- Annex V, Part 1, paragraph 42(c): (c) credit institutions: any institution covered by the definition in point (1) of Article 4(1) CRR (‘undertaking the business of which is to take deposits or other repayable funds from the public and to grant credits for its own account’) and multilateral development banks (MDBs); (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="debt-instruments"></a>
### Debt instruments

- Annex V, Part 1, paragraph 33: In FINREP, ‘debt instruments’ shall include ‘loans and advances’ and ‘debt securities’. (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="debt-securities"></a>
### Debt securities

- Annex V, Part 1, paragraph 31: ‘Debt securities’ are debt instruments held by the institution issued as securities that are not loans, as defined in the Table of Part 2 of Annex II to the ECB BSI Regulation. (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="debt-security-by-performing-status-type"></a>
### Debt security by Performing status type

- BIRD variable `DBT_SCRTY_PRFRMNG_STTS_TYP`: Performing status in accordance with Implementing Regulation (EU) No 680/2014. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="entity-role-type"></a>
### Entity role type

- BIRD variable `ENTTY_RL_TYP`: A discriminator to distinguish between party roles, organisation roles, central bank and private sector company roles and legal person roles. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="fair-value"></a>
### Fair value

- BIRD variable `FV`: Fair value as defined in IFRS 13.9. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="finrep-reporting-scheme"></a>
### Finrep reporting scheme

- BIRD variable `FNRP_RPRTNG_SCHM`: Finrep reporting scheme (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="general-allowances-for-bank-risk-affecting-carrying-amount-ngaap"></a>
### General allowances for bank risk affecting carrying amount (nGAAP)

- BIRD variable `GNRL_ALLWNCS_BNK_RSK`: General allowances for bank risk affecting carrying amount (nGAAP) (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="general-allowances-for-credit-risk-affecting-carrying-amount-ngaap"></a>
### General allowances for credit risk affecting carrying amount (nGAAP)

- BIRD variable `GNRL_ALLWNCS_CRDT_RSK`: General allowances for credit risk affecting carrying amount (nGAAP) (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="general-governments"></a>
### General governments

- Template F 18.00.a row 0090: Label of row 0090 of template F 18.00.a. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))
- Annex V, Part 1, paragraph 42(b): (b) general governments: central governments, state or regional governments, and local governments, including administrative bodies and non-commercial undertakings, but excluding public companies and private companies held by these administrations that have a commercial activity (which shall be reported under ‘credit institutions’, ‘other financial corporations’ or ‘non-financial corporations’ depending on their activity); social security funds; and international organisations, such as institutions of the European Union, the International Monetary Fund and the Bank for International Settlements; (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="gross-carrying-amount"></a>
### Gross carrying amount

- BIRD variable `GRSS_CRRYNG_AMNT`: Gross carrying amount as defined in Annex V 5.2. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))
- Annex V, Part 1, paragraph 34: Gross carrying amount of debt instruments shall have the following meaning: (a) under IFRS and national GAAP based on BAD for debt instruments measured at fair value through profit or loss without being included in the held for trading or trading portfolio, the gross carrying amount shall depend on whether those debt instruments are classified as performing or non-performing. For performing debt instruments, the gross carrying amount shall be the fair value. For non-performing debt instruments, the gross carrying amount shall be the fair value after adding back any accumulated negative changes in fair value due to credit risk, as defined in paragraph 69 of Part 2 of this Annex. For the purposes of the measurement of the gross carrying amount, the valuation of the debt instruments shall be performed on the level of single financial instruments; (b) under IFRS for debt instruments at amortised cost, the gross carrying amount shall be the carrying amount before adjusting for any loss allowance and for debt instruments at fair value through other comprehensive income, the amortised cost before adjusting for any loss allowance; (c) under national GAAP based on BAD, for debt instruments classified as ‘non-trading non-derivative financial assets measured at a cost-based method’, the gross carrying amount of impaired assets shall be equal to the carrying amount before adjusting for specific allowances for credit risk. The gross carrying amount of unimpaired assets shall be the carrying amount before adjusting for general allowances for credit risk and general allowances for banking risk, where affecting the carrying amount; (d) under national GAAP based on BAD, the gross carrying amount of debt instruments classified as ‘Non-trading non-derivative financial assets measured at fair value to equity’ shall depend on whether those financial assets are subject to impairment requirements. Where they are subject to impairment requirements, the gross carrying amount shall be the carrying amount before adjusting for any accumulated impairment, following the requirements in point (c) above for impaired and unimpaired assets, or any accumulated amount of fair value adjustment that is considered as impairment loss. When those financial assets are not subject to impairment requirements, the gross carrying amount of those financial assets shall be the fair value for performing exposures, and for non-performing exposures the fair value after adding back any accumulated negative fair value adjustment due to credit risk; (e) under national GAAP based on BAD, the gross carrying amount of debt instruments measured at strict or moderate LOCOM shall be the cost where measured at cost during the reporting reference period. Where those debt instruments are measured at market value, the gross carrying amount shall be the market value before adjusting for credit-risk induced value adjustments; (f) under national GAAP based on BAD, for debt instruments reported under ‘Other non-trading non-derivative financial assets’ under measurement methods other than LOCOM, the gross carrying amount shall be the carrying amount before taking into account any valuation adjustment that qualifies as impairment; (g) for trading financial assets under GAAP based on BAD or held for trading financial assets under IFRS, the gross carrying amount shall be the fair value. Where GAAP based on BAD require haircuts on trading and fair valued instruments, the carrying amount of the financial instruments shall be the fair value before those haircuts. (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="gross-carrying-amount-nominal-amount"></a>
### Gross carrying amount/Nominal amount

- Template F 18.00.a column 0010: Label of column 0010 of template F 18.00.a. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="group-id"></a>
### Group ID

- BIRD variable `GRP_ID`: RIAD Code of the head entity of group concatenated with the type of group, for example DE00001.A (Entity with RIAD Code DE00001 is the head of the Type A group). (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="held-for-sale-indicator"></a>
### Held for sale indicator

- BIRD variable `HLD_SL_INDCTR`: A variable indicating the Non-current assets and instruments in disposal groups classified as held for sale in accordance with IFRS5. Is not applicable under national GAAP based on BAD. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="households"></a>
### Households

- Template F 18.00.a row 0150: Label of row 0150 of template F 18.00.a. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))
- Annex V, Part 1, paragraph 42(f): (f) households: individuals or groups of individuals as consumers and producers of goods and non-financial services exclusively for their own final consumption, and as producers of market goods and non-financial and financial services provided that their activities are not those of quasi-corporations. Non-profit institutions which serve households (‘NPISH’) and which are principally engaged in the production of non-market goods and services intended for particular groups of households shall be included. (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="impairment-status"></a>
### Impairment status

- BIRD variable `IMPRMNT_STTS`: Type of impairment recorded in accordance with the accounting standard – IFRS or national GAAP. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="institutional-sector"></a>
### Institutional sector

- BIRD variable `INSTTTNL_SCTR`: Institutional sectors in accordance with Regulation (EU) No 549/2013, Regulation (EU) No 575/2013 and Regulation (EU) No 1075/2013 of the European Central Bank (ECB/2013/40)(1). (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [CRR_REGULATION](register.md#crr-regulation), [REG_EU_549_2013](register.md#reg-eu-549-2013), [REG_EU_1075_2013](register.md#reg-eu-1075-2013))

<a id="instrument"></a>
### Instrument

- BIRD input layer entity `INSTRMNT_IL`: An Instrument is a product that establishes a financial relationship between a bank and its customer. In the context of accounting such a financial relationship may be considered a financial asset or a financial liabilty or an off-balance sheet item. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="instrument-entity-role-assignment"></a>
### Instrument Entity role assignment

- BIRD input layer entity `INSTRMNT_ENTTY_RL_ASSGNMNT_IL`: An Instrument Entity role assignment is the combination of an Instrument and an Entity role that indicates which Instrument is assigned to which Entity role. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="instrument-identifier"></a>
### Instrument identifier

- BIRD variable `INSTRMNT_ID`: An identifier applied by the reporting agent to uniquely identify each instrument under a single contract. Each instrument must have one instrument identifier. This value will not change over time and cannot be used as the instrument identifier for any other instrument under the same contract. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="instrument-role"></a>
### Instrument role

- BIRD input layer entity `INSTRMNT_RL_IL`: An Instrument role is a role an Instrument may act in. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="instrument-role-type"></a>
### Instrument role type

- BIRD variable `INSTRMNT_RL_TYP`: A discriminator to distinguish between different roles an instrument may act in. Examples are financial asset instrument, financial liability instrument. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="instrument-type-by-product"></a>
### Instrument type by product

- BIRD variable `INSTRMNT_TYP_PRDCT`: A discriminator to distinguish instruments by product. Examles are loans and advances, securities financing transactions, financial guarantees and other commitments or over the counter derivatives. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="internal-group-role"></a>
### Internal group role

- BIRD input layer entity `INTRNL_GRP_RL_IL`: A Internal group role is a role an Internal group may act in. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="internal-group-role-type"></a>
### Internal group role type

- BIRD variable `GRP_RL_TYP`: A discriminator to distinguish between different roles a group may act in. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="investor-entity-role-type"></a>
### Investor Entity role type

- BIRD variable `INVSTR_ENTTY_RL_TYP`: The investor role. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="investor-party-identifier"></a>
### Investor Party identifier

- BIRD variable `INVSTR_PRTY_ID`: The party identifier of the involved investor. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="loans-and-advances"></a>
### Loans and advances

- Template F 18.00.a row 0070: Label of row 0070 of template F 18.00.a. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))
- Annex V, Part 1, paragraph 32: ‘Loans and advances’ are debt instruments held by the institutions that are not securities. That item includes loans as defined in the Table of Part 2 of Annex II to the ECB BSI Regulation (including demand deposits at credit institutions and central banks, irrespective of their classification as per the applicable accounting framework) as well as advances that cannot be classified as ‘loans’ defined in the Table of Part 2 of Annex II to the ECB BSI Regulation. ‘Advances that are not loans’ are further characterized in paragraph 85(g) of Part 2 of this Annex. (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="long-balance-sheet-recognised-security-position-prudential-portfolio-accounting-classification-assignment"></a>
### Long balance sheet recognised security position prudential portfolio Accounting classification assignment

- BIRD input layer entity `LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL`: A Long balance sheet recognised security position prudential portfolio Accounting classification assignment is the combination between Long balance sheet recognised security position prudential portfolio assignment and Accounting classifcation. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="long-short-balance-sheet-recognised-security-position"></a>
### Long/Short balance sheet recognised security position

- BIRD input layer entity `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL`: A Long/Short balance sheet recognised security position is a balance sheet recognised security position that is either long or short. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="long-short-balance-sheet-recognised-security-position-type"></a>
### Long/Short balance sheet recognised security position type

- BIRD variable `LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP`: Long/Short balance sheet recognised security position type defines whether a long/short balance sheet recognised security position is long or short. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="main-debtor-indicator"></a>
### Main debtor indicator

- BIRD variable `MN_DBTR_INDCTR`: An indicator specifying if a debtor is the main debtor. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="main-deposit-taking-corporation-indicator"></a>
### Main Deposit-taking corporation indicator

- BIRD variable `MN_DPST_TKNG_CRPRTN_INDCTR`: An indicator specifying if a debtor is the main debtor. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="main-lessee-indicator"></a>
### Main lessee indicator

- BIRD variable `MN_LSS_INDCTR`: An indicator specifying if a debtor is the main debtor. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="multilateral-development-bank-indicator"></a>
### Multilateral development bank indicator

- BIRD variable `MLTLTRL_DVLPMNT_BNK_INDCTR`: Multilateral development bank indicator specifies if the International organisation is a multilateral development bank or not. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="negotiable-security-indicator"></a>
### Negotiable security indicator

- BIRD variable `NGTBL_SCRTY_INDCTR`: An indicator specifying is a security is listed or not. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="non-financial-corporations"></a>
### Non-financial corporations

- Template F 18.00.a row 0120: Label of row 0120 of template F 18.00.a. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))
- Annex V, Part 1, paragraph 42(e): (e) non-financial corporations (NFCs): corporations and quasi-corporations not engaged in financial intermediation but principally in the production of market goods and non-financial services, as defined in the Table of Part 3 of Annex II to the ECB BSI Regulation; (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="non-performing"></a>
### Non-performing

- Template F 18.00.a column 0060: Label of column 0060 of template F 18.00.a. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="non-performing-exposures"></a>
### Non-performing exposures

- Annex V, Part 2, paragraph 213: For the purposes of template 18, non-performing exposures shall be exposures listed in Article 47a(3) CRR. (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="other-demand-deposits"></a>
### Other demand deposits

- Annex V, Part 2, paragraph 3: ‘Other demand deposits’ shall include ‘loans and advances’ that are balances receivable on demand with credit institutions. (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="other-financial-corporations"></a>
### Other financial corporations

- Template F 18.00.a row 0110: Label of row 0110 of template F 18.00.a. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))
- Annex V, Part 1, paragraph 42(d): (d) other financial corporations: all financial corporations and quasi-corporations, other than credit institutions, such as investment firms, investment funds, insurance companies, pension funds, collective investment undertakings, and clearing houses as well as remaining financial intermediaries, financial auxiliaries and captive financial institutions and money lenders; (Source: [REG_EU_2021_451](register.md#reg-eu-2021-451))

<a id="over-the-counter-otc-derivative-as-a-hedge"></a>
### Over the counter (OTC) Derivative as a hedge

- BIRD input layer entity `OTC_DRVTV_HDG_IL`: An Over the counter (OTC) Derivative as a hedge is an Over the counter (OTC) Derivative role where the Over the counter (OTC) Derivative instrument acts as a hedge. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="party"></a>
### Party

- BIRD input layer entity `PRTY_IL`: A Party is an entity of interest. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="party-identifier"></a>
### Party identifier

- BIRD variable `PRTY_ID`: An identifier that uniquely identifies a party. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="performing-status"></a>
### Performing status

- BIRD variable `PRFRMNG_STTS`: Performing status in accordance with Implementing Regulation (EU) No 680/2014. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_680_2014](register.md#reg-eu-680-2014))

<a id="primary-issuer-indicator"></a>
### Primary issuer indicator

- BIRD variable `PRMRY_ISSR_INDCTR`: Primary issuer indicator (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="prudential-portfolio-type"></a>
### Prudential portfolio type

- BIRD variable `PRDNTL_PRTFL_TYP`: A discriminator to distinguish between trading and banking (or non-trading) book. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="reference-date"></a>
### Reference date

- BIRD variable `DT_RFRNC`: Reporting agents shall report credit data as recorded on the following reporting reference dates: (a) for monthly transmissions, on the last day of each month; (b) for quarterly transmissions, on the last day of March, June, September and December. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="repayment-rights"></a>
### Repayment rights

- BIRD variable `RPYMNT_RGHTS`: Classification of credit exposures according to the creditor's rights to claim the repayment of the exposure. On demand or at short notice (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="reporting-agent-identifier"></a>
### Reporting agent identifier

- BIRD variable `RPRTNG_AGNT_ID`: Reporting agent identifier (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="security-and-exchange-tradable-derivative"></a>
### Security and exchange tradable derivative

- BIRD input layer entity `SCRTY_EXCHNG_TRDBL_DRVTV_IL`: A Security and exchange tradable derivative is a certificate attesting credit, the ownership of stocks or bonds, or the right to ownership connected with tradable derivatives. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="security-and-exchange-tradable-derivative-identifier"></a>
### Security and exchange tradable derivative identifier

- BIRD variable `SCRTY_EXCHNG_TRDBL_DRVTV_ID`: An identifier to uniquely identify each security. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="security-and-exchange-tradable-derivative-type"></a>
### Security and exchange tradable derivative type

- BIRD variable `SCRTY_EXCHNG_TRDBL_DRVTV_TYP`: A discriminator to distinguish between securities and exchange tradable derivatives. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="security-entity-role-assignment"></a>
### Security Entity role assignment

- BIRD input layer entity `SCRTY_ENTTY_RL_ASSGNMNT_IL`: A Security or Exchange tradable derivative Entity role assignment is the combination of a Security or Exchange tradable derivative and an Entity role that indicates which Security or Exchange tradable derivative is associated with which Entity role. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="security-identifier"></a>
### Security identifier

- BIRD variable `SCRTY_ID`: An identifier to uniquely identify each security. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="security-position-balance-sheet-recognised-type"></a>
### Security position Balance sheet recognised type

- BIRD variable `SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP`: Security position Balance sheet recognised indicator defines whether a security position is recognised in the balance sheet or non recognised in the balance sheet (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="subject-to-impairment-indicator"></a>
### Subject to impairment indicator

- BIRD variable `SBJCT_IMPRMNT_INDCTR`: Subject to impairment indicator indicates whether the asset is subject to impairment or not. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="type-of-financial-asset-instrument-according-to-annex-v"></a>
### Type of Financial Asset Instrument according to Annex V

- BIRD variable `TYP_FNNCL_ASST_INSTRMNT_ANNX_V`: Type of Financial Asset Instrument according to Annex V (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

## Code values

<a id="abstrct-instrmnt-rl-typ-102"></a>
### ABSTRCT_INSTRMNT_RL_TYP_102: Non-balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP)

- Code list: Abstract instrument role type. Non-balance sheet recognised financial asset instrument national general accepted accounting principles (nGAAP) (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="abstrct-instrmnt-rl-typ-34"></a>
### ABSTRCT_INSTRMNT_RL_TYP_34: Balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP)

- Code list: Abstract instrument role type. Balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP) (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="abstrct-instrmnt-rl-typ-35"></a>
### ABSTRCT_INSTRMNT_RL_TYP_35: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)

- Code list: Abstract instrument role type. Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS) (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-2"></a>
### ACCNTNG_CLSSFCTN_2: IFRS: Financial assets held for trading

- Code list: Accounting classification. Financial assets held for trading in accordance with IFRS. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-3"></a>
### ACCNTNG_CLSSFCTN_3: nGAAP: Trading Financial assets

- Code list: Accounting classification. Trading financial assets in accordance with national GAAP. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-4"></a>
### ACCNTNG_CLSSFCTN_4: IFRS: Financial assets designated at fair value through profit or loss

- Code list: Accounting classification. Financial assets measured at fair value through profit and loss and designated as such upon initial recognition or subsequently in accordance with IFRS, except those classified as financial assets held for trading. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-41"></a>
### ACCNTNG_CLSSFCTN_41: IFRS: Non-trading financial assets mandatorily at fair value through profit or loss

- Code list: Accounting classification. Non-trading financial assets mandatorily at fair value through profit or loss in accordance with IFRS. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-44"></a>
### ACCNTNG_CLSSFCTN_44: nGAAP: Financial assets designated at fair value through profit or loss, measured using the cost-based method or LOCOM

- Code list: Accounting classification. nGAAP: Financial assets designated at fair value through profit or loss, measured using the cost-based method or LOCOM (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-49"></a>
### ACCNTNG_CLSSFCTN_49: nGAAP: Financial assets designated at fair value through profit or loss, not measured using the cost-based method or LOCOM

- Code list: Accounting classification. nGAAP: Financial assets designated at fair value through profit or loss, measured using the cost-based method or LOCOM (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-6"></a>
### ACCNTNG_CLSSFCTN_6: IFRS: Financial assets at amortised cost

- Code list: Accounting classification. Financial assets measured at amortised cost in accordance with IFRS. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-7"></a>
### ACCNTNG_CLSSFCTN_7: nGAAP: Non-trading non-derivative financial assets measured at fair value through profit or loss

- Code list: Accounting classification. Non-trading non-derivative financial assets measured at fair value to equity in accordance with national GAAP. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-73"></a>
### ACCNTNG_CLSSFCTN_73: nGAAP: Other non-trading non-derivative financial assets. LOCOM

- Code list: Accounting classification. nGAAP: Other non-trading non-derivative financial assets at LOCOM (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-74"></a>
### ACCNTNG_CLSSFCTN_74: nGAAP: Other non-trading non-derivative financial assets. Other than LOCOM

- Code list: Accounting classification. nGAAP: Other non-trading non-derivative financial assets. Other than LOCOM (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-76"></a>
### ACCNTNG_CLSSFCTN_76: nGAAP: Non-trading non-derivative financial assets measured at a cost-based method. LOCOM

- Code list: Accounting classification. nGAAP: Non-trading non-derivative financial assets measured at a cost-based method at LOCOM (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-77"></a>
### ACCNTNG_CLSSFCTN_77: nGAAP: Non-trading non-derivative financial assets measured at a cost-based method. Other than LOCOM

- Code list: Accounting classification. nGAAP: Non-trading non-derivative financial assets measured at a cost-based method. Other than LOCOM (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-8"></a>
### ACCNTNG_CLSSFCTN_8: IFRS: Financial assets at fair value through other comprehensive income

- Code list: Accounting classification. Financial assets measured at fair value through other comprehensive income due to business model and cash-flows characteristics in accordance with IFRS. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-clssfctn-9"></a>
### ACCNTNG_CLSSFCTN_9: nGAAP: Non-trading non-derivative financial assets measured at fair value to equity

- Code list: Accounting classification. Non-trading non-derivative financial assets measured at fair value to equity in accordance with national GAAP. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-hdg-indctr-1"></a>
### ACCNTNG_HDG_INDCTR_1: Accounting hedge

- Code list: Accounting hedge indicator. Accounting hedge (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="accntng-hdg-indctr-2"></a>
### ACCNTNG_HDG_INDCTR_2: Not accounting hedge

- Code list: Accounting hedge indicator. Not accounting hedge (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="crdt-qlty-1"></a>
### CRDT_QLTY_1: Non-performing

- Code list: Credit quality. Non-performing (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="crdt-qlty-11"></a>
### CRDT_QLTY_11: Performing

- Code list: Credit quality. Performing (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="crdt-qlty-211"></a>
### CRDT_QLTY_211: General allowances for credit risk

- Code list: Credit quality. General allowances for credit risk (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="crdt-qlty-212"></a>
### CRDT_QLTY_212: General allowances for banking risk

- Code list: Credit quality. General allowances for banking risks (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="crdt-qlty-26"></a>
### CRDT_QLTY_26: Specific allowances (GAAP)

- Code list: Credit quality. To be used if the instrument is subject to impairment in accordance with an applied accounting standard other than IFRS 9 and specific loss allowances are raised, irrespective of whether these allowances are individually or collectively assessed (impaired). (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="entty-rl-typ-19"></a>
### ENTTY_RL_TYP_19: Lessee

- Code list: Entity role type. Lessee (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="entty-rl-typ-20"></a>
### ENTTY_RL_TYP_20: Seller

- Code list: Entity role type. Seller (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="entty-rl-typ-27"></a>
### ENTTY_RL_TYP_27: Deposit-taking corporation

- Code list: Entity role type. Deposit taking corporation (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="entty-rl-typ-28"></a>
### ENTTY_RL_TYP_28: Loan debtor

- Code list: Entity role type. Loan debtor (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="entty-rl-typ-8"></a>
### ENTTY_RL_TYP_8: Issuer

- Code list: Entity role type. Issuer (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="fnrp-rprtng-schm-1"></a>
### FNRP_RPRTNG_SCHM_1: Full

- Code list: Finrep reporting scheme. Full (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="fnrp-rprtng-schm-2"></a>
### FNRP_RPRTNG_SCHM_2: Simplified

- Code list: Finrep reporting scheme. Simplified (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="fnrp-rprtng-schm-3"></a>
### FNRP_RPRTNG_SCHM_3: Over-simplified

- Code list: Finrep reporting scheme. Over-simplified (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="grp-rl-typ-1"></a>
### GRP_RL_TYP_1: Reporting agent internal group role

- Code list: Group role type. Reporting agent internal group role (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="hld-sl-indctr-1"></a>
### HLD_SL_INDCTR_1: Held for sale

- Code list: Held for sale. The member indicates that the instrument is held for sale (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="hld-sl-indctr-2"></a>
### HLD_SL_INDCTR_2: Not held for sale

- Code list: Held for sale. The member indicates that the instrument is not held for sale (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="instttnl-sctr-io"></a>
### INSTTTNL_SCTR_IO: International organisations

- Code list: Institutional sectors. International organisations (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="instttnl-sctr-s11"></a>
### INSTTTNL_SCTR_S11: Non financial corporations

- Code list: Institutional sectors. It corresponds to sector S.11, as defined in Regulation (EU) No 549/2013 (paragraphs 2.45 to 2.50 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s121"></a>
### INSTTTNL_SCTR_S121: Central banks

- Code list: Institutional sectors. It corresponds to subsector S.121, as defined in Regulation (EU) No 549/2013 (paragraphs 2.72 to 2.74 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s122-a"></a>
### INSTTTNL_SCTR_S122_A: Credit institutions

- Code list: Institutional sectors. Credit institutions as defined in Article 4(1)(1) of Regulation (EU) No 575/2013. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [CRR_REGULATION](register.md#crr-regulation))

<a id="instttnl-sctr-s122-a-1"></a>
### INSTTTNL_SCTR_S122_A_1: Credit institutions not including entities according to the article 2.5 Directive 2013/36/EU

- Code list: Institutional sectors. Credit institutions not including entities according to the article 2.5 Directive 2013/36/EU (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_1071_2013](register.md#reg-eu-1071-2013))

<a id="instttnl-sctr-s122-a-2"></a>
### INSTTTNL_SCTR_S122_A_2: Credit institutions according to the article 2.5 Directive 2013/36/EU

- Code list: Institutional sectors. Credit institutions according to the article 2.5 Directive 2013/36/EU (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [CRD_IV_DIRECTIVE](register.md#crd-iv-directive))

<a id="instttnl-sctr-s122-b1"></a>
### INSTTTNL_SCTR_S122_B1: Electronic money institutions principally engaged in financial intermediation

- Code list: Institutional sectors. Electronic money institutions, as defined in Directive 2009/110/EC [article 2(1)], that are principally engaged in financial intermediation, as defined in Regulation (EU) no 549/2013 (paragraph 2.56 of Annex A). (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [DIR_EC_110_2009](register.md#dir-ec-110-2009))

<a id="instttnl-sctr-s122-b2"></a>
### INSTTTNL_SCTR_S122_B2: Deposit-taking corporations except the central bank, other than credit institutions and electronic money institutions

- Code list: Institutional sectors. It corresponds to subsector S.122, as defined in Regulation (EU) No 549/2013 (paragraphs 2.75 to 2.78 of Annex A), extended to the rest of the world, other than credit institutions, as defined in Article 4(1)(1) of Regulation (EU) No 575/2013, and electronic money institutions, as defined in Directive 2009/110/EC [article 2(1)]. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s123"></a>
### INSTTTNL_SCTR_S123: Money Market Funds (MMFs)

- Code list: Institutional sectors. It corresponds to subsector S.123, as defined in Regulation (EU) No 549/2013 (paragraphs 2.79 to 2.81 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s124"></a>
### INSTTTNL_SCTR_S124: Non-MMF investment funds

- Code list: Institutional sectors. It corresponds to subsector S.124, as defined in Regulation (EU) No 549/2013 (paragraphs 2.82 to 2.85 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s125-a"></a>
### INSTTTNL_SCTR_S125_A: Financial Vehicle Corporations (FVCs)

- Code list: Institutional sectors. FVCs as defined in Article 1 of Regulation (EU) No 1075/2013. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_1075_2013](register.md#reg-eu-1075-2013))

<a id="instttnl-sctr-s125-b"></a>
### INSTTTNL_SCTR_S125_B: Security and derivative dealers

- Code list: Institutional sectors. Security and derivative dealers as defined in Regulation (EU) No 549/2013 (paragraph 2.91 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s125-c"></a>
### INSTTTNL_SCTR_S125_C: Financial corporations engaged in lending

- Code list: Institutional sectors. Financial corporations engaged in lending as defined in Regulation (EU) No 549/2013 (paragraph 2.92 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s125-d"></a>
### INSTTTNL_SCTR_S125_D: Specialised financial corporations other than CCPs

- Code list: Institutional sectors. Specialised financial corporations, as defined in Regulation (EU) No 549/2013 (paragraph 2.93 of Annex A), extended to the rest of the world, other than CCPs, as defined in point (1) of Article 2 of Regulation (EU) No 648/2012. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s125-e"></a>
### INSTTTNL_SCTR_S125_E: Central Counterparties (CCPs)

- Code list: Institutional sectors. CCPs as defined in point (1) of Article 2 of Regulation (EU) No 648/2012. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_648_2012](register.md#reg-eu-648-2012))

<a id="instttnl-sctr-s125-i"></a>
### INSTTTNL_SCTR_S125_I: Other financial intermediaries, except insurance corporations and pension funds, other than CCPs, FVCs, security and derivative dealers, financial corporations engaged in lending and specialised financial corporations

- Code list: Institutional sectors. It corresponds to subsector S.125, as defined in Regulation (EU) No 549/2013 (paragraphs 2.86 to 2.94 of Annex A), extended to the rest of the world, other than CCPs, as defined in point (1) of Article 2 of Regulation (EU) No 648/2012, FVCs, as defined in Article 1 of Regulation (EU) No 1075/2013, and security and derivative dealers, financial corporations engaged in lending and specialised financial corporations, as defined in Regulation (EU) No 549/2013 (paragraphs 2.91, 2.92 and 2.93, respectively, of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s125-w"></a>
### INSTTTNL_SCTR_S125_W: Other financial corporations excluding financial vehicle corporations

- Code list: Institutional sectors. Other financial corporations excluding financial vehicle corporations (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="instttnl-sctr-s126"></a>
### INSTTTNL_SCTR_S126: Financial auxiliaries

- Code list: Institutional sectors. It corresponds to subsector S.126, as defined in Regulation (EU) No 549/2013 (paragraphs 2.63 and 2.95 to 2.97 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s127"></a>
### INSTTTNL_SCTR_S127: Captive financial institutions and money lenders

- Code list: Institutional sectors. It corresponds to subsector S.127, as defined in Regulation (EU) No 549/2013 (paragraphs 2.98 to 2.99 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s128"></a>
### INSTTTNL_SCTR_S128: Insurance corporations

- Code list: Institutional sectors. It corresponds to subsector S.128, as defined in Regulation (EU) No 549/2013 (paragraphs 2.100 to 2.104 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s129"></a>
### INSTTTNL_SCTR_S129: Pension funds

- Code list: Institutional sectors. It corresponds to subsector S.129, as defined in Regulation (EU) No 549/2013 (paragraphs 2.105 to 2.110 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s1311"></a>
### INSTTTNL_SCTR_S1311: Central government (excluding social security funds)

- Code list: Institutional sectors. It corresponds to subsector S.1311, as defined in Regulation (EU) No 549/2013 (paragraph 2.114 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s1312"></a>
### INSTTTNL_SCTR_S1312: State government (excluding social security funds)

- Code list: Institutional sectors. It corresponds to subsector S.1312, as defined in Regulation (EU) No 549/2013 (paragraph 2.115 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s1313"></a>
### INSTTTNL_SCTR_S1313: Local government (excluding social security funds)

- Code list: Institutional sectors. It corresponds to subsector S.1313, as defined in Regulation (EU) No 549/2013 (paragraph 2.116 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s1314"></a>
### INSTTTNL_SCTR_S1314: Social security funds

- Code list: Institutional sectors. It corresponds to subsector S.1314, as defined in Regulation (EU) No 549/2013 (paragraph 2.117 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s14-a"></a>
### INSTTTNL_SCTR_S14_A: Households that are sole proprietorships/partnerships without legal status

- Code list: Institutional sectors. Sole proprietorships and partnerships without legal status included in the sector S.14, as defined in Regulation (EU) No 549/2013 (paragraphs 2.118 to 2.121 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s14-b"></a>
### INSTTTNL_SCTR_S14_B: Households other than sole proprietorships/partnerships without legal status

- Code list: Institutional sectors. It corresponds to sector S.14, as defined in Regulation (EU) No 549/2013 (paragraphs 2.118 to 2.121 of Annex A), extended to the rest of the world, other than sole proprietorships and partnerships without legal status. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="instttnl-sctr-s15"></a>
### INSTTTNL_SCTR_S15: Non profit institutions serving households

- Code list: Institutional sectors. It corresponds to sector S.15, as defined in Regulation (EU) No 549/2013 (paragraphs 2.129 to 2.130 of Annex A), extended to the rest of the world. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="lng-shrt-blnc-sht-rcgnsd-scrty-pstn-typ-3"></a>
### LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3: Long balance sheet recognised security position International Financial Reporting Standard (IFRS)

- Code list: Long balance sheet recognised security position accounting standard type. Long balance sheet recognised security position International Financial Reporting Standard (IFRS) (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="lng-shrt-blnc-sht-rcgnsd-scrty-pstn-typ-4"></a>
### LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4: Long balance sheet recognised security position national general accepted accounting principles (nGAAP)

- Code list: Long balance sheet recognised security position accounting standard type. Long balance sheet recognised security position national general accepted accounting principles (nGAAP) (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="mltltrl-dvlpmnt-bnk-indctr-1"></a>
### MLTLTRL_DVLPMNT_BNK_INDCTR_1: Multilateral development bank

- Code list: Multilateral development bank indicator.  (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="mn-dbtr-indctr-1"></a>
### MN_DBTR_INDCTR_1: Main debtor

- Code list: Main debtor indicator. Main debtor (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="mn-dpst-tkng-crprtn-indctr-1"></a>
### MN_DPST_TKNG_CRPRTN_INDCTR_1: Main Deposit-taking corporation

- Code list: Main Deposit-taking corporation indicator. Main Deposit-taking corporation (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="mn-lss-indctr-1"></a>
### MN_LSS_INDCTR_1: Main lessee

- Code list: Main lessee indicator. Main lessee (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="ngtbl-scrty-1"></a>
### NGTBL_SCRTY_1: Negotiable security

- Code list: Negotiable security.  (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="ngtbl-scrty-2"></a>
### NGTBL_SCRTY_2: Non-negotiable security

- Code list: Negotiable security.  (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="prmry-issr-indctr-1"></a>
### PRMRY_ISSR_INDCTR_1: Primary issuer

- Code list: Primary issuer indicator. Primary issuer (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="rpymnt-rghts-1"></a>
### RPYMNT_RGHTS_1: On demand or short notice

- Code list: Repayment rights. Instruments which are repayable on demand or at short notice at the request of the creditor. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="rpymnt-rghts-2"></a>
### RPYMNT_RGHTS_2: Other than on demand or short notice

- Code list: Repayment rights. Instruments subject to repayment rights other than on demand or at short notice. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="sbjct-imprmnt-indctr-1"></a>
### SBJCT_IMPRMNT_INDCTR_1: Subject to impairment

- Code list: Subject to impairment indicator. The member indicates that the financial asset is subject to impairment (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="sbjct-imprmnt-indctr-2"></a>
### SBJCT_IMPRMNT_INDCTR_2: Not subject to impairment

- Code list: Subject to impairment indicator. The member indicates that the financial asset is not subject to impairment (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="scrty-exchng-trdbl-drvtv-typ-11"></a>
### SCRTY_EXCHNG_TRDBL_DRVTV_TYP_11: Debt security without underlying assets

- Code list: Security or exchange tradable derivative type. Debt security without underlying assets (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="scrty-exchng-trdbl-drvtv-typ-13"></a>
### SCRTY_EXCHNG_TRDBL_DRVTV_TYP_13: Asset backed security

- Code list: Security or exchange tradable derivative type. Asset backed security (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="scrty-exchng-trdbl-drvtv-typ-14"></a>
### SCRTY_EXCHNG_TRDBL_DRVTV_TYP_14: Covered bond

- Code list: Security or exchange tradable derivative type. Covered bond (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="scrty-exchng-trdbl-drvtv-typ-19"></a>
### SCRTY_EXCHNG_TRDBL_DRVTV_TYP_19: Performing debt security

- Code list: Security or exchange tradable derivative type.  (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="scrty-exchng-trdbl-drvtv-typ-20"></a>
### SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20: Non-performing debt security

- Code list: Security or exchange tradable derivative type.  (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="scrty-exchng-trdbl-drvtv-typ-5"></a>
### SCRTY_EXCHNG_TRDBL_DRVTV_TYP_5: Fund security

- Code list: Security or exchange tradable derivative type. Fund security (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="scrty-exchng-trdbl-drvtv-typ-6"></a>
### SCRTY_EXCHNG_TRDBL_DRVTV_TYP_6: Equity security

- Code list: Security or exchange tradable derivative type. Equity security (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-10"></a>
### TYP_INSTRMNT_10: Over the counter (OTC) Option other than Over the counter (OTC) Credit spread option

- Code list: Type of instrument. OTC Option other than OTC Credit spread option (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1020"></a>
### TYP_INSTRMNT_1020: Factoring

- Code list: Type of instrument. Factoring (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1022"></a>
### TYP_INSTRMNT_1022: Other loan

- Code list: Type of instrument. Loans as defined in point 5(112) to (138) of Annex A to Regulation (EU) No 549/2013 other than financial leases, reverse repurchase loans, credit card debt, current accounts (that are assets), factoring and other trade receivables. Please note that it also does not include Other deposits (w.r.t. ESA classification). (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="typ-instrmnt-1023"></a>
### TYP_INSTRMNT_1023: Other trade receivable

- Code list: Type of instrument. Trade receivables as defined in Regulation (EU) No 680/2014, Annex V, Part 2.41 (c) other than factoring. Among other things, this category includes outright purchase of trade receivables and discounting of invoices, bills of exchange and other claims. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_680_2014](register.md#reg-eu-680-2014))

<a id="typ-instrmnt-1112"></a>
### TYP_INSTRMNT_1112: Cash balances at central banks

- Code list: Type of instrument. Cash balances at central banks (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1113"></a>
### TYP_INSTRMNT_1113: Other demand deposits

- Code list: Type of instrument. Other demand deposits (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1114"></a>
### TYP_INSTRMNT_1114: Derivatives not hedge

- Code list: Type of instrument. Derivatives not hedge (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1115"></a>
### TYP_INSTRMNT_1115: Equity instruments

- Code list: Type of instrument. Equity instruments (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1116"></a>
### TYP_INSTRMNT_1116: Debt securities

- Code list: Type of instrument. Debt securities (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1117"></a>
### TYP_INSTRMNT_1117: Loans and Advances

- Code list: Type of instrument. Loans and Advances (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1118"></a>
### TYP_INSTRMNT_1118: Non-current assets and disposal groups classified as held for sale

- Code list: Type of instrument. Non-current assets and disposal groups classified as held for sale (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1119"></a>
### TYP_INSTRMNT_1119: Derivatives hedge

- Code list: Type of instrument. Derivatives hedge (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-120"></a>
### TYP_INSTRMNT_120: Transit item

- Code list: Type of instrument. Transit items (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1201"></a>
### TYP_INSTRMNT_1201: On demand deposit used for minimum reserve

- Code list: Type of instrument. Loan on demand used for minimum reserve (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-1202"></a>
### TYP_INSTRMNT_1202: On demand deposit not used for minimum reserve

- Code list: Type of instrument. On demand deposit not used for minimum reserve (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-130"></a>
### TYP_INSTRMNT_130: Suspense item

- Code list: Type of instrument. Suspence items (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-140"></a>
### TYP_INSTRMNT_140: Other advance

- Code list: Type of instrument. Advances that are not loans other than transit items and suspence items (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-162"></a>
### TYP_INSTRMNT_162: Open repurchase transaction

- Code list: Type of instrument. Open repurchase transaction (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-163"></a>
### TYP_INSTRMNT_163: Term repurchase transaction

- Code list: Type of instrument. Term Repurchase transaction (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-2"></a>
### TYP_INSTRMNT_2: Equity instrument that is not a security

- Code list: Type of instrument. Equity instrument that is not a security (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-380"></a>
### TYP_INSTRMNT_380: Over the counter (OTC) Forward

- Code list: Type of instrument. Forwards are derivative contracts between two parties to buy or to sell an asset at a specified future time at a price agreed upon today (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-5"></a>
### TYP_INSTRMNT_5: Other over the counter (OTC) Derivative instrument

- Code list: Type of instrument. Other OTC Derivative instrument (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-51"></a>
### TYP_INSTRMNT_51: Credit card debt

- Code list: Type of instrument. Credit card debt according to Regulation (EU) 1071/2013 concerning the balance sheet of the monetary financial institutions sector, Annex II, Part 2, Instrument categories: "...this category comprises credit granted [...] either via delayed debit cards, i.e. cards providing convenience credit as defined below, or via credit cards, i.e. cards providing convenience credit and extended credit. .Credit card debt is recorded on dedicated card accounts and therefore not evident on current or overdraft accounts. Convenience credit is defined as the credit granted at an interest rate of 0 % in the period between the payment transactions effectuated with the card during one billing cycle and the date at which the debit balances from this specific billing cycle become due. Extended credit is defined as the credit granted after the due dates of the previous billing cycles have passed, i.e. debit amounts on the card account that have not been settled when this was first possible, for which an interest rate or tiered interest rates usually greater than 0 % are charged. Often minimum instalments per month have to be made, to at least partially repay extended credit. The counterpart to these forms of credit is the entity liable to eventually repay the amounts outstanding in accordance with the contractual agreement, which coincides with the cardholder in the case of privately used cards, but not in the case of company cards;" (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_1071_2013](register.md#reg-eu-1071-2013))

<a id="typ-instrmnt-511"></a>
### TYP_INSTRMNT_511: Tranferable overnight deposits

- Code list: Type of instrument.  (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-512"></a>
### TYP_INSTRMNT_512: Non-transferable overnight deposits

- Code list: Type of instrument. Non-transferable overnight deposits (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-522"></a>
### TYP_INSTRMNT_522: Deposit with agreed maturity

- Code list: Type of instrument. Deposits with agreed maturity - other than counterpart liability to non-derecognised loans (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-6"></a>
### TYP_INSTRMNT_6: Over the counter (OTC) Total return swap

- Code list: Type of instrument. OTC Total return swap (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-7"></a>
### TYP_INSTRMNT_7: Over the counter (OTC) Credit default swap

- Code list: Type of instrument. OTC Credit default swap (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-8"></a>
### TYP_INSTRMNT_8: Other over the counter (OTC) Swap

- Code list: Type of instrument. Other OTC Swap (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))

<a id="typ-instrmnt-80"></a>
### TYP_INSTRMNT_80: Financial lease

- Code list: Type of instrument. Financial leases as defined in paragraphs 5.134 to 5.135 of Annex A to Regulation (EU) No 549/2013. (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3), [REG_EU_549_2013](register.md#reg-eu-549-2013))

<a id="typ-instrmnt-9"></a>
### TYP_INSTRMNT_9: Over the counter (OTC) Credit spread option

- Code list: Type of instrument. OTC Credit spread option (Source: [BIRD_FINREP_4_3](register.md#bird-finrep-4-3))
