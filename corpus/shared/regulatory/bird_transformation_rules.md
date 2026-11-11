# BIRD transformation rules

Official algorithm text of the BIRD routines behind the non-performing loans ratio, verbatim from the ECB BIRD
metadata (FINREP 4.3). The algorithms are written in the BIRD pseudo-code and are not directly executable.

<a id="r-idt-der"></a>
## R_IDT_DER

Identity routine

```
Transfer the variable from the input cube to the variable with the same name in the output cube.
```

<a id="r-der-grss-crryng-amnt-3"></a>
## R_DER_GRSS_CRRYNG_AMNT_3

Derivation rule for Gross carrying amount in INSTRMNT_RL_EIL cube

```
update cubes --(destination cubes: INSTRMNT_RL_EIL)
-- The derivation logic is defined in accordance with Annex V
(
set
GRSS_CRRYNG_AMNT =
case when
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_2, ACCNTNG_CLSSFCTN_3)
or
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_41, ACCNTNG_CLSSFCTN_4, ACCNTNG_CLSSFCTN_7, ACCNTNG_CLSSFCTN_49)
and
PRFRMNG_STTS = CRDT_QLTY_11
)
or
(
ACCNTNG_CLSSFCTN = ACCNTNG_CLSSFCTN_9
and
SBJCT_IMPRMNT_INDCTR = SBJCT_IMPRMNT_INDCTR_2
and
PRFRMNG_STTS = CRDT_QLTY_11
)
)
and
FV <> null
then
FV
)
or
(
set
GRSS_CRRYNG_AMNT =
case when
(
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_41, ACCNTNG_CLSSFCTN_4, ACCNTNG_CLSSFCTN_7, ACCNTNG_CLSSFCTN_49)
and
PRFRMNG_STTS = CRDT_QLTY_1
)
or
(
ACCNTNG_CLSSFCTN = ACCNTNG_CLSSFCTN_9
and
SBJCT_IMPRMNT_INDCTR = SBJCT_IMPRMNT_INDCTR_2
and
PRFRMNG_STTS = CRDT_QLTY_1
)
)
and
FV <> null
and
ACCMLTD_CHNGS_FV_CR < 0
then
FV - ACCMLTD_CHNGS_FV_CR
)
or
(
set
GRSS_CRRYNG_AMNT =
case when
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_8, ACCNTNG_CLSSFCTN_6)
or
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_76, ACCNTNG_CLSSFCTN_77, ACCNTNG_CLSSFCTN_44)
and
IMPRMNT_STTS = CRDT_QLTY_26
)
or
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_9, ACCNTNG_CLSSFCTN_73, ACCNTNG_CLSSFCTN_74)
and
SBJCT_IMPRMNT_INDCTR = SBJCT_IMPRMNT_INDCTR_1
and
IMPRMNT_STTS = CRDT_QLTY_26
)
)
and
CRRYNG_AMNT <> null
and
ACCMLTD_IMPRMNT <> null
then
CRRYNG_AMNT + ACCMLTD_IMPRMNT
)
or
(
set
GRSS_CRRYNG_AMNT =
case when
(
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_76, ACCNTNG_CLSSFCTN_77, ACCNTNG_CLSSFCTN_44)
and
IMPRMNT_STTS in (CRDT_QLTY_211, CRDT_QLTY_212)
)
or
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_9, ACCNTNG_CLSSFCTN_73, ACCNTNG_CLSSFCTN_74)
and
SBJCT_IMPRMNT_INDCTR = SBJCT_IMPRMNT_INDCTR_1
and
IMPRMNT_STTS in (CRDT_QLTY_211, CRDT_QLTY_212)
)
)
and
CRRYNG_AMNT <> null
and
(
GNRL_ALLWNCS_CRDT_RSK <> null
or
GNRL_ALLWNCS_BNK_RSK <> null
)
then
CRRYNG_AMNT + GNRL_ALLWNCS_CRDT_RSK + GNRL_ALLWNCS_BNK_RSK
)
or
(
set
GRSS_CRRYNG_AMNT =
case when
(
(
ACCNTNG_CLSSFCTN_73
and
SBJCT_IMPRMNT_INDCTR = SBJCT_IMPRMNT_INDCTR_2 -- Measured at cost
)
or
(
ACCNTNG_CLSSFCTN_44
and
IMPRMNT_STTS not in (CRDT_QLTY_26, CRDT_QLTY_211, CRDT_QLTY_212) -- Measured at cost
)
)
and
CRRYNG_AMNT <> null
then
CRRYNG_AMNT
);
or
(
set
GRSS_CRRYNG_AMNT =
case when
(
FV = null
and
CRRYNG_AMNT = null
)
then
null;
```

<a id="r-der-typ-fnncl-asst-instrmnt-annx-v-2"></a>
## R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_2

Derivation rule for Type of Financial Asset Instrument according to Annex V in INSTRMNT_RL_EIL cube

```
Update EIL Cube -- Destination cube: INSTRMNT_RL_EIL
set
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = 
case
when -- Start of the Loans and Advances section
(
(
INSTRMNT_TYP_PRDCT in (TYP_INSTRMNT_1020, TYP_INSTRMNT_1022, TYP_INSTRMNT_1023, TYP_INSTRMNT_120, -- Source cube: INSTRMNT_IL; Members' name: Factoring, Other loans, Other trade receivables, Transit items
TYP_INSTRMNT_130, TYP_INSTRMNT_140, -- Members' name: Suspence items, Advances that are not loans other than transit items and suspence items
TYP_INSTRMNT_162, TYP_INSTRMNT_163, TYP_INSTRMNT_51) -- Members' name: Term repurchase agreement, Open repurchase agreement, Credit card debt
and ENTTY_RL_TYP = ENTTY_RL_TYP_28 -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Debtor
and MN_DBTR_INDCTR = MN_DBTR_INDCTR_1 -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Main debtor Indicator
)
or
(
INSTRMNT_TYP_PRDCT = TYP_INSTRMNT_80 -- Members' name: Finance leases
and ENTTY_RL_TYP = ENTTY_RL_TYP_19  -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Lesee
and MN_LSS_INDCTR = MN_LSS_INDCTR_1 -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Main Lesee Indicator
)
or
(
INSTRMNT_TYP_PRDCT in (TYP_INSTRMNT_511, TYP_INSTRMNT_512, TYP_INSTRMNT_522, TYP_INSTRMNT_1202) -- Source cube: INSTRMNT_IL; Members' name: ranferable overnight deposits, Non-transferable overnight deposits, Deposits with agreed maturity - other than counterpart liability to non-derecognised loans, On demand deposit not used for minimum reserve
and ENTTY_RL_TYP = ENTTY_RL_TYP_27 -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Deposit taking corporation
and MN_DPST_DPST_TKNG_CRPRTN_INDCTR = MN_DPST_TKNG_CRPRTN_INCTR_1 -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Main Deposit taking corporation Indicator
)
)
and
(INSTTTNL_SCTR not in (INSTTTNL_SCTR_S121, INSTTTNL_SCTR_S122_A) -- Source cube: PRTY_IL; Members' name: Central banks, Credit institution
or
(INSTTTNL_SCTR in (INSTTTNL_SCTR_S121, INSTTTNL_SCTR_S122_A) -- Source cube: PRTY_IL; Members' name: Central banks, Credit institution
and RPYMNT_RGHTS = RPYMNT_RGHTS_2)) -- Source cube: INSTRMNT_IL; Other than on demand or short notice
)
)
)
then
case
when
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_34 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP)
or
(
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_2 -- Source cube: INSTRMNT_RL_IL; Members' name: Not Held for sale
)
then TYP_INSTRMNT_1117 -- Loans and Advances
when
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_1 -- Source cube: INSTRMNT_RL_IL; Members' name: Held for sale
then TYP_INSTRMNT_1118 -- Non-current assets and disposal groups classified as held for sale
end -- End of the Loans and Advances section
when -- Start of the Cash balances at central banks section
(
(INSTRMNT_TYP_PRDCT in (TYP_INSTRMNT_511, TYP_INSTRMNT_512, TYP_INSTRMNT_522, TYP_INSTRMNT_1202) -- Source cube: INSTRMNT_IL; Members' name: ranferable overnight deposits, Non-transferable overnight deposits, Deposits with agreed maturity - other than counterpart liability to non-derecognised loans, On demand deposit not used for minimum reserve
and RPYMNT_RGHTS = RPYMNT_RGHTS_1) -- Source cube: INSTRMNT_IL; On demand or short notice
or TYP_INSTRMNT_1201 --Loan on demand used for minimum reserve
)
and ENTTY_RL_TYP = ENTTY_RL_TYP_27 -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Deposit taking corporation
and MN_DPST_DPST_TKNG_CRPRTN_INDCTR = MN_DPST_TKNG_CRPRTN_INCTR_1 -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Main Deposit taking corporation Indicator
and INSTTTNL_SCTR = INSTTTNL_SCTR_S121 -- Source cube: PRTY_IL; Members' name: Central banks
then
case
when
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_34 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP)
or
(
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_2 -- Source cube: INSTRMNT_RL_IL; Members' name: Not Held for sale
)
then TYP_INSTRMNT_1112 -- Cash balances at central banks
when
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_1 -- Source cube: INSTRMNT_RL_IL; Members' name: Held for sale
then TYP_INSTRMNT_1118 -- Non-current assets and disposal groups classified as held for sale
end -- End of the Cash balances at central banks section
when -- Start of the Other demand deposits section
INSTRMNT_TYP_PRDCT in (TYP_INSTRMNT_511, TYP_INSTRMNT_512, TYP_INSTRMNT_522, TYP_INSTRMNT_1202) -- Source cube: INSTRMNT_IL; Members' name: Tranferable overnight deposits, Non-transferable overnight deposits, Deposits with agreed maturity - other than counterpart liability to non-derecognised loans, On demand deposit not used for minimum reserve
and RPYMNT_RGHTS = RPYMNT_RGHTS_1 --Source cube: INSTRMNT_IL; On demand or short notice
and ENTTY_RL_TYP = ENTTY_RL_TYP_27 -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Deposit taking corporation
and MN_DPST_DPST_TKNG_CRPRTN_INDCTR = MN_DPST_TKNG_CRPRTN_INCTR_1 -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Main Deposit taking corporation Indicator
and INSTTTNL_SCTR = INSTTTNL_SCTR_S122_A -- Source cube: PRTY_IL; Members' name: Credit institution
then
case
when
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_34 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP)
or
(
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_2 -- Source cube: INSTRMNT_RL_IL; Members' name: Not Held for sale
)
then TYP_INSTRMNT_1113 -- Other demand deposits
when
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_1 -- Source cube: INSTRMNT_RL_IL; Members' name: Held for sale
then TYP_INSTRMNT_1118 -- Non-current assets and disposal groups classified as held for sale
end -- End of the Other demand deposits section
when -- Start of the Equity instruments section
INSTRMNT_TYP_PRDCT = TYP_INSTRMNT_2 -- Source cube: INSTRMNT_IL; Members' name: Equity instrument that is not a security
then
case
when
(
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_34 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP)
and ENTTY_RL_TYP = ENTTY_RL_TYP_8 -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL; Members' name: Issuer
and PRTY_ID <> RPRTNG_AGNT_ID -- Source cube: INSTRMNT_ENTTY_RL_ASSGNMNT_IL
)
or
(
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_2 -- Source cube: INSTRMNT_RL_IL; Members' name: Not Held for sale
)
then TYP_INSTRMNT_1115 -- Equity instruments
when
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_1 -- Source cube: INSTRMNT_RL_IL; Members' name: Held for sale
then TYP_INSTRMNT_1118 -- Non-current assets and disposal groups classified as held for sale
end -- End of the Equity instruments section
when  -- Start of the Derivatives not hedge section
INSTRMNT_TYP_PRDCT in (TYP_INSTRMNT_10, TYP_INSTRMNT_380, TYP_INSTRMNT_5, -- Source cube: INSTRMNT_IL; Members' name: OTC Option other than OTC Credit spread option, Forward, Other OTC Derivative instrument
TYP_INSTRMNT_6, TYP_INSTRMNT_7, TYP_INSTRMNT_8, TYP_INSTRMNT_9) -- Members' name: OTC Total return swap, OTC Credit default swap, Other OTC swap, OTC Credit spread option
and ACCNTNG_HDG_INDCTR = ACCNTNG_HDG_INDCTR_2 -- Source cube: OTC_DRVTV_HDG_IL; Members' name: Not accounting hedge
then
case
when
INSTRMNT_RL_TYP in (ABSTRCT_INSTRMNT_RL_TYP_34, ABSTRCT_INSTRMNT_RL_TYP_102) -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP), Non-balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP), 
or
(
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_2 -- Source cube: INSTRMNT_RL_IL; Members' name: Not Held for sale
)
then TYP_INSTRMNT_1114 -- Derivatives not hedge
when
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_1 -- Source cube: INSTRMNT_RL_IL; Members' name: Held for sale
then TYP_INSTRMNT_1118 -- Non-current assets and disposal groups classified as held for sale
end -- End of the Derivatives not hedge section
when  -- Start of the Derivatives hedge section
INSTRMNT_TYP_PRDCT in (TYP_INSTRMNT_10, TYP_INSTRMNT_380, TYP_INSTRMNT_5, -- Source cube: INSTRMNT_IL; Members' name: OTC Option other than OTC Credit spread option, Forward, Other OTC Derivative instrument
TYP_INSTRMNT_6, TYP_INSTRMNT_7, TYP_INSTRMNT_8, TYP_INSTRMNT_9) -- Members' name: OTC Total return swap, OTC Credit default swap, Other OTC swap, OTC Credit spread option
and ACCNTNG_HDG_INDCTR = ACCNTNG_HDG_INDCTR_1 -- Source cube: OTC_DRVTV_HDG_IL; Members' name: Accounting hedge
then
case
when
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_34 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to national general accepted accounting principles (nGAAP)
or
(
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_2 -- Source cube: INSTRMNT_RL_IL; Members' name: Not Held for sale
)
then TYP_INSTRMNT_1119 -- Derivatives hedge
when
INSTRMNT_RL_TYP = ABSTRCT_INSTRMNT_RL_TYP_35 -- Source cube: INSTRMNT_RL_IL; Members' name: Balance sheet recognised financial asset instrument according to International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_1 -- Source cube: INSTRMNT_RL_IL; Members' name: Held for sale
then TYP_INSTRMNT_1118 -- Non-current assets and disposal groups classified as held for sale
end -- End of the Derivatives hedge section
else null;
```

<a id="r-der-grss-crryng-amnt-1"></a>
## R_DER_GRSS_CRRYNG_AMNT_1

Derivation rule for Gross carrying amount in
LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_EIL cube

```
update cubes --(destination cubes: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_EIL) The derivation logic is defined in accordance with Annex V
(
set
GRSS_CRRYNG_AMNT =
case when
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_2, ACCNTNG_CLSSFCTN_3)
or
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_41, ACCNTNG_CLSSFCTN_4, ACCNTNG_CLSSFCTN_7, ACCNTNG_CLSSFCTN_49)
and
DBT_SCRTY_PRFRMNG_STTS_TYP = SCRTY_EXCHNG_TRDBL_DRVTV_TYP_19
)
or
(
ACCNTNG_CLSSFCTN = ACCNTNG_CLSSFCTN_9
and
SBJCT_IMPRMNT_INDCTR = SBJCT_IMPRMNT_INDCTR_2
and
DBT_SCRTY_PRFRMNG_STTS_TYP = SCRTY_EXCHNG_TRDBL_DRVTV_TYP_19
)
)
and
FV <> null
then
FV
)
or
(
set
GRSS_CRRYNG_AMNT =
case when
(
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_41, ACCNTNG_CLSSFCTN_4, ACCNTNG_CLSSFCTN_7, ACCNTNG_CLSSFCTN_49)
and
DBT_SCRTY_PRFRMNG_STTS_TYP = SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20
)
or
(
ACCNTNG_CLSSFCTN = ACCNTNG_CLSSFCTN_9
and
SBJCT_IMPRMNT_INDCTR = SBJCT_IMPRMNT_INDCTR_2
and
DBT_SCRTY_PRFRMNG_STTS_TYP = SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20
)
)
and
FV <> null
and
ACCMLTD_CHNGS_FV_CR < 0
then
FV - ACCMLTD_CHNGS_FV_CR
)
or
(
set
GRSS_CRRYNG_AMNT =
case when
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_8, ACCNTNG_CLSSFCTN_6)
or
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_76, ACCNTNG_CLSSFCTN_77, ACCNTNG_CLSSFCTN_44)
and
IMPRMNT_STTS = CRDT_QLTY_26
)
or
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_9, ACCNTNG_CLSSFCTN_73, ACCNTNG_CLSSFCTN_74)
and
SBJCT_IMPRMNT_INDCTR = SBJCT_IMPRMNT_INDCTR_1
and
IMPRMNT_STTS = CRDT_QLTY_26
)
)
and
CRRYNG_AMNT <> null
and
ACCMLTD_IMPRMNT <> null
then
CRRYNG_AMNT + ACCMLTD_IMPRMNT
)
or
(
set
GRSS_CRRYNG_AMNT =
case when
(
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_76, ACCNTNG_CLSSFCTN_77, ACCNTNG_CLSSFCTN_44)
and
IMPRMNT_STTS in (CRDT_QLTY_211, CRDT_QLTY_212)
)
or
(
ACCNTNG_CLSSFCTN in (ACCNTNG_CLSSFCTN_9, ACCNTNG_CLSSFCTN_73, ACCNTNG_CLSSFCTN_74)
and
SBJCT_IMPRMNT_INDCTR = SBJCT_IMPRMNT_INDCTR_1
and
IMPRMNT_STTS in (CRDT_QLTY_211, CRDT_QLTY_212)
)
)
and
CRRYNG_AMNT <> null
and
(
GNRL_ALLWNCS_CRDT_RSK <> null
or
GNRL_ALLWNCS_BNK_RSK <> null
)
then
CRRYNG_AMNT + GNRL_ALLWNCS_CRDT_RSK + GNRL_ALLWNCS_BNK_RSK
)
or
(
set
GRSS_CRRYNG_AMNT =
case when
(
(
ACCNTNG_CLSSFCTN_73
and
SBJCT_IMPRMNT_INDCTR = SBJCT_IMPRMNT_INDCTR_2 -- Measured at cost
)
or
(
ACCNTNG_CLSSFCTN_44
and
IMPRMNT_STTS not in (CRDT_QLTY_26, CRDT_QLTY_211, CRDT_QLTY_212) -- Measured at cost
)
)
and
CRRYNG_AMNT <> null
then
CRRYNG_AMNT
);
or
(
set
GRSS_CRRYNG_AMNT =
case when
(
FV = null
and
CRRYNG_AMNT = null
)
then
null;
```

<a id="r-der-typ-fnncl-asst-instrmnt-annx-v-3"></a>
## R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_3

Derivation rule for Type of Financial Asset Instrument according to Annex V in
LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_EIL cube

```
Update EIL Cube -- Destination cube: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_EIL
set
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = 
case
when -- Start of the Loans and Advances section 
SCRTY_EXCHNG_TRDBL_DRVTV_TYP in (SCRTY_EXCHNG_TRDBL_DRVTV_TYP_11, SCRTY_EXCHNG_TRDBL_DRVTV_TYP_14,  -- Source cube: SCRTY_EXCHNG_TRDBL_DRVTV_IL; Members' name: Debt security without underlying assets, Covered bond
SCRTY_EXCHNG_TRDBL_DRVTV_TYP_13, SCRTY_EXCHNG_TRDBL_DRVTV_TYP_5) -- Members' name: Asset backed security, Fund securities
and NGTBL_SCRTY_INDCTR = NGTBL_SCRTY_2 -- Source cube: SCRTY_EXCHNG_TRDBL_DRVTV_IL; Members' name: Non-negotiable security
then
case
when
LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP =  LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4  -- Source cube: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL; Members' name: Long balance sheet recognised security position national general accepted accounting principles (nGAAP)
or
(
LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP =  LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3 -- Source cube: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL; Members' name: Long balance sheet recognised security position International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_2 -- Source cube: EXCHNG_TRDBL_SCRTY_PSTN_IL; Members' name: Not Held for sale
)
then TYP_INSTRMNT_1117 -- Loans and Advances
when
LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP =  LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3 -- Source cube: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL; Members' name: Long balance sheet recognised security position International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_1 -- Source cube: EXCHNG_TRDBL_SCRTY_PSTN_IL; Members' name: Held for sale
then TYP_INSTRMNT_1118 -- Non-current assets and disposal groups classified as held for sale
end -- End of the Loans and Advances section
when -- Start of the Debt securities section
SCRTY_EXCHNG_TRDBL_DRVTV_TYP in (SCRTY_EXCHNG_TRDBL_DRVTV_TYP_11, SCRTY_EXCHNG_TRDBL_DRVTV_TYP_14,  -- Source cube: SCRTY_EXCHNG_TRDBL_DRVTV_IL; Members' name: Debt security without underlying assets, Covered bond
SCRTY_EXCHNG_TRDBL_DRVTV_TYP_13, SCRTY_EXCHNG_TRDBL_DRVTV_TYP_5) -- Members' name: Asset backed security, Fund securities
and NGTBL_SCRTY_INDCTR = NGTBL_SCRTY_1 -- Source cube: SCRTY_EXCHNG_TRDBL_DRVTV_IL; Members' name: Negotiable security
then
case
when
LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP =  LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4  -- Source cube: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL; Members' name: Long balance sheet recognised security position national general accepted accounting principles (nGAAP)
or
(
LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP =  LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3 -- Source cube:LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL; Members' name: Long balance sheet recognised security position International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_2 -- Source cube: EXCHNG_TRDBL_SCRTY_PSTN_IL; Members' name: Not Held for sale
)
then TYP_INSTRMNT_1116 -- Debt securities
when
LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP =  LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3 -- Source cube: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL; Members' name: Long balance sheet recognised security position International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_1 -- Source cube: EXCHNG_TRDBL_SCRTY_PSTN_IL; Members' name: Held for sale
then TYP_INSTRMNT_1118 -- Non-current assets and disposal groups classified as held for sale
end -- End of the Debt securities section
when -- Start of the Equity instruments section
SCRTY_EXCHNG_TRDBL_DRVTV_TYP = SCRTY_EXCHNG_TRDBL_DRVTV_TYP_6  -- Source cube: SCRTY_EXCHNG_TRDBL_DRVTV_IL; Members' name: Equity security
then
case
when
(
LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP =  LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4  -- Source cube: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL; Members' name: Long balance sheet recognised security position national general accepted accounting principles (nGAAP)
and
and ENTTY_RL_TYP = ENTTY_RL_TYP_8 -- Source cube: SCRTY_ENTTY_RL_ASSGNMNT_IL; Members' name: Issuer
and PRTY_ID <> RPRTNG_AGNT_ID -- Source cube: SCRTY_ENTTY_RL_ASSGNMNT_IL
)
or
(
LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP =  LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3 -- Source cube: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL; Members' name: Long balance sheet recognised security position International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_2 -- Source cube: EXCHNG_TRDBL_SCRTY_PSTN_IL; Members' name: Not Held for sale
)
then TYP_INSTRMNT_1115 -- Equity instruments
when
LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP =  LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3 -- Source cube: LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL; Members' name: Long balance sheet recognised security position International Financial Reporting Standard (IFRS)
and HLD_SL_INDCTR = HLD_SL_INDCTR_1 -- Source cube: EXCHNG_TRDBL_SCRTY_PSTN_IL; Members' name: Held for sale
then TYP_INSTRMNT_1118 -- Non-current assets and disposal groups classified as held for sale
end -- End of the Equity instruments section
else null;
```

<a id="r-f-18-00-a-all"></a>
## R_F_18.00.a_ALL

Generating common rules for F_18.00.a - Information on performing and non-performing exposures (I)

```
Select *
where
FNRP_RPRTNG_SCHM in 
(
FNRP_RPRTNG_SCHM_1, 
FNRP_RPRTNG_SCHM_2, 
FNRP_RPRTNG_SCHM_3
);
```

<a id="r-f-18-00-a-r0070"></a>
## R_F_18.00.a_R0070

Generating F_18.00.a - DEBT INSTRUMENTS AT COST OR AT AMORTISED COST: Loans and advances

```
SUM(R0080, R0090, R0100, R0110, R0120, R0150)
```

<a id="r-f-18-00-a-r0080"></a>
## R_F_18.00.a_R0080

Generating F_18.00.a - DEBT INSTRUMENTS AT COST OR AT AMORTISED COST: Loans and advances: Central banks

```
Update DataPointCube
set
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117,
ACCNTNG_CLSSFCTN = ACCNTNG_CLSSFCTN_531,
INSTTTNL_SCTR = INSTTTNL_SCTR_S121
where
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117
and ACCNTNG_CLSSFCTN in 
(
ACCNTNG_CLSSFCTN_6, 
ACCNTNG_CLSSFCTN_74, 
ACCNTNG_CLSSFCTN_76, 
ACCNTNG_CLSSFCTN_77
)
and INSTTTNL_SCTR = INSTTTNL_SCTR_S121
and (
(ENTTY_RL_TYP in 
(
ENTTY_RL_TYP_20,
ENTTY_RL_TYP_28
) -- Seller; Loan debtor [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DBTR_INDCTR = MN_DBTR_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_27  -- Deposit taking corporation [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DPST_TKNG_CRPRTN_INDCTR = MN_DPST_TKNG_CRPRTN_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_19  -- Lessee [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_LSS_INDCTR = MN_LSS_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_8 -- Issuer [Cube: SCRTY_ENTTY_RL_ASSGNMNT_EIL]
and PRMRY_ISSR_INDCTR = PRMRY_ISSR_INDCTR_1));
```

<a id="r-f-18-00-a-r0090"></a>
## R_F_18.00.a_R0090

Generating F_18.00.a - DEBT INSTRUMENTS AT COST OR AT AMORTISED COST: Loans and advances: General governments

```
Update DataPointCube
set
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117,
ACCNTNG_CLSSFCTN = ACCNTNG_CLSSFCTN_531,
INSTTTNL_SCTR = INSTTTNL_SCTR_S13_IO
where
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117
and ACCNTNG_CLSSFCTN in 
(
ACCNTNG_CLSSFCTN_6, 
ACCNTNG_CLSSFCTN_74, 
ACCNTNG_CLSSFCTN_76, 
ACCNTNG_CLSSFCTN_77
)
and  INSTTTNL_SCTR in 
(
INSTTTNL_SCTR_S1311, 
INSTTTNL_SCTR_S1312, 
INSTTTNL_SCTR_S1313, 
INSTTTNL_SCTR_S1314, 
INSTTTNL_SCTR_IO
)
and (
(ENTTY_RL_TYP in 
(
ENTTY_RL_TYP_20,
ENTTY_RL_TYP_28
) -- Seller; Loan debtor [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DBTR_INDCTR = MN_DBTR_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_27  -- Deposit taking corporation [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DPST_TKNG_CRPRTN_INDCTR = MN_DPST_TKNG_CRPRTN_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_19  -- Lessee [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_LSS_INDCTR = MN_LSS_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_8  -- Issuer [Cube: SCRTY_ENTTY_RL_ASSGNMNT_EIL]
and PRMRY_ISSR_INDCTR = PRMRY_ISSR_INDCTR_1));
```

<a id="r-f-18-00-a-r0100"></a>
## R_F_18.00.a_R0100

Generating F_18.00.a - DEBT INSTRUMENTS AT COST OR AT AMORTISED COST: Loans and advances: Credit institutions

```
Update DataPointCube
set
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117,
ACCNTNG_CLSSFCTN = ACCNTNG_CLSSFCTN_531,
INSTTTNL_SCTR = INSTTTNL_SCTR_S1_MDB
where
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117
and ACCNTNG_CLSSFCTN in 
(
ACCNTNG_CLSSFCTN_6, 
ACCNTNG_CLSSFCTN_74, 
ACCNTNG_CLSSFCTN_76, 
ACCNTNG_CLSSFCTN_77
)
and (INSTTTNL_SCTR in 
(
INSTTTNL_SCTR_S122_A_1, 
INSTTTNL_SCTR_S122_A_2
)
or MLTLTRL_DVLPMNT_BNK_INDCTR = MLTLTRL_DVLPMNT_BNK_INDCTR_1)
and (
(ENTTY_RL_TYP in 
(
ENTTY_RL_TYP_20,
ENTTY_RL_TYP_28
) -- Seller; Loan debtor [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DBTR_INDCTR = MN_DBTR_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_27 -- Deposit taking corporation [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DPST_TKNG_CRPRTN_INDCTR = MN_DPST_TKNG_CRPRTN_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_19 -- Lessee [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_LSS_INDCTR = MN_LSS_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_8 -- Issuer [Cube: SCRTY_ENTTY_RL_ASSGNMNT_EIL]
and PRMRY_ISSR_INDCTR = PRMRY_ISSR_INDCTR_1));
```

<a id="r-f-18-00-a-r0110"></a>
## R_F_18.00.a_R0110

Generating F_18.00.a - DEBT INSTRUMENTS AT COST OR AT AMORTISED COST: Loans and advances: Other financial
corporations

```
Update DataPointCube
set
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117,
ACCNTNG_CLSSFCTN = ACCNTNG_CLSSFCTN_531,
INSTTTNL_SCTR  = INSTTTNL_SCTR_S12_D
where
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117
and ACCNTNG_CLSSFCTN in 
(
ACCNTNG_CLSSFCTN_6, 
ACCNTNG_CLSSFCTN_74, 
ACCNTNG_CLSSFCTN_76, 
ACCNTNG_CLSSFCTN_77
)
and  INSTTTNL_SCTR in 
(
INSTTTNL_SCTR_S123, 
INSTTTNL_SCTR_S124, 
INSTTTNL_SCTR_S125_I, 
INSTTTNL_SCTR_S125_C, 
INSTTTNL_SCTR_S125_A, 
INSTTTNL_SCTR_S125_E, 
INSTTTNL_SCTR_S125_D, 
INSTTTNL_SCTR_S125_B, 
INSTTTNL_SCTR_S125_W, 
INSTTTNL_SCTR_S127, 
INSTTTNL_SCTR_S128, 
INSTTTNL_SCTR_S129,  
INSTTTNL_SCTR_S122_B1, 
INSTTTNL_SCTR_S122_B2
)
and (
(ENTTY_RL_TYP in 
(
ENTTY_RL_TYP_20,
ENTTY_RL_TYP_28
) -- Seller; Loan debtor [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DBTR_INDCTR = MN_DBTR_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_27 -- Deposit taking corporation [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DPST_TKNG_CRPRTN_INDCTR = MN_DPST_TKNG_CRPRTN_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_19 -- Lessee [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_LSS_INDCTR = MN_LSS_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_8 -- Issuer [Cube: SCRTY_ENTTY_RL_ASSGNMNT_EIL]
and PRMRY_ISSR_INDCTR = PRMRY_ISSR_INDCTR_1));
```

<a id="r-f-18-00-a-r0120"></a>
## R_F_18.00.a_R0120

Generating F_18.00.a - DEBT INSTRUMENTS AT COST OR AT AMORTISED COST: Loans and advances: Non-financial
corporations

```
Update DataPointCube
set
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117,
ACCNTNG_CLSSFCTN = ACCNTNG_CLSSFCTN_531,
INSTTTNL_SCTR = INSTTTNL_SCTR_S11
where
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117
and ACCNTNG_CLSSFCTN in 
(
ACCNTNG_CLSSFCTN_6, 
ACCNTNG_CLSSFCTN_74, 
ACCNTNG_CLSSFCTN_76, 
ACCNTNG_CLSSFCTN_77
)
and INSTTTNL_SCTR = INSTTTNL_SCTR_S11
and (
(ENTTY_RL_TYP in 
(
ENTTY_RL_TYP_20,
ENTTY_RL_TYP_28
) -- Seller; Loan debtor [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DBTR_INDCTR = MN_DBTR_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_27 -- Deposit taking corporation [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DPST_TKNG_CRPRTN_INDCTR = MN_DPST_TKNG_CRPRTN_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_19 -- Lessee [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_LSS_INDCTR = MN_LSS_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_8 -- Issuer [Cube: SCRTY_ENTTY_RL_ASSGNMNT_EIL]
and PRMRY_ISSR_INDCTR = PRMRY_ISSR_INDCTR_1));
```

<a id="r-f-18-00-a-r0150"></a>
## R_F_18.00.a_R0150

Generating F_18.00.a - DEBT INSTRUMENTS AT COST OR AT AMORTISED COST: Loans and advances: Households

```
Update DataPointCube
set
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117,
ACCNTNG_CLSSFCTN = ACCNTNG_CLSSFCTN_531,
INSTTTNL_SCTR = INSTTTNL_SCTR_S1_A
where
TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117
and ACCNTNG_CLSSFCTN in 
(
ACCNTNG_CLSSFCTN_6, 
ACCNTNG_CLSSFCTN_74, 
ACCNTNG_CLSSFCTN_76, 
ACCNTNG_CLSSFCTN_77
)
and INSTTTNL_SCTR in 
(
INSTTTNL_SCTR_S14_A, 
INSTTTNL_SCTR_S14_B, 
INSTTTNL_SCTR_S15
)
and (
(ENTTY_RL_TYP in 
(
ENTTY_RL_TYP_20,
ENTTY_RL_TYP_28
) -- Seller; Loan debtor [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DBTR_INDCTR = MN_DBTR_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_27 -- Deposit taking corporation [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_DPST_TKNG_CRPRTN_INDCTR = MN_DPST_TKNG_CRPRTN_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_19 -- Lessee [Cube: INSTRMNT_ENTTY_RL_ASSGNMNT_EIL]
and MN_LSS_INDCTR = MN_LSS_INDCTR_1)
or
(ENTTY_RL_TYP = ENTTY_RL_TYP_8 -- Issuer [Cube: SCRTY_ENTTY_RL_ASSGNMNT_EIL]
and PRMRY_ISSR_INDCTR = PRMRY_ISSR_INDCTR_1));
```

<a id="r-f-18-00-a-c0010"></a>
## R_F_18.00.a_C0010

Generating F_18.00.a - Gross carrying amount/Nominal amount

```
Update DataPointCube
set
GRSS_CRRYNG_AMNT = GRSS_CRRYNG_AMNT
where
GRSS_CRRYNG_AMNT > 0;
```

<a id="r-f-18-00-a-c0060"></a>
## R_F_18.00.a_C0060

Generating F_18.00.a - Gross carrying amount/Nominal amount: Non-performing

```
Update DataPointCube
set
GRSS_CRRYNG_AMNT = GRSS_CRRYNG_AMNT,
PRFRMNG_STTS = CRDT_QLTY_1
where
GRSS_CRRYNG_AMNT > 0
and
(PRFRMNG_STTS = CRDT_QLTY_1
or
DBT_SCRTY_PRFRMNG_STTS_TYP = SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20);
```
