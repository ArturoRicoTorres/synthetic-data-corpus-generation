-- Input snapshot for one reporting date, reporting agent, consolidation level and accounting standard.
-- Session variables: dt_rfrnc (DATE), rprtng_agnt_id, accntng_cnsldtn_lvl, accntng_stndrd.

CREATE OR REPLACE VIEW instrmnt_il_snp AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, INSTRMNT_ID,
       INSTRMNT_TYP_PRDCT, RPYMNT_RGHTS
FROM INSTRMNT_IL
WHERE DT_RFRNC = getvariable('dt_rfrnc')
  AND RPRTNG_AGNT_ID = getvariable('rprtng_agnt_id')
  AND ACCNTNG_CNSLDTN_LVL = getvariable('accntng_cnsldtn_lvl')
  AND ACCNTNG_STNDRD = getvariable('accntng_stndrd');

CREATE OR REPLACE VIEW instrmnt_rl_il_snp AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, INSTRMNT_ID, INSTRMNT_RL_TYP,
       ACCNTNG_CLSSFCTN, HLD_SL_INDCTR, SBJCT_IMPRMNT_INDCTR, IMPRMNT_STTS, PRFRMNG_STTS,
       CRRYNG_AMNT, ACCMLTD_IMPRMNT, FV, ACCMLTD_CHNGS_FV_CR, GNRL_ALLWNCS_CRDT_RSK, GNRL_ALLWNCS_BNK_RSK
FROM INSTRMNT_RL_IL
WHERE DT_RFRNC = getvariable('dt_rfrnc')
  AND RPRTNG_AGNT_ID = getvariable('rprtng_agnt_id')
  AND ACCNTNG_CNSLDTN_LVL = getvariable('accntng_cnsldtn_lvl')
  AND ACCNTNG_STNDRD = getvariable('accntng_stndrd');

CREATE OR REPLACE VIEW instrmnt_entty_rl_assgnmnt_il_snp AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, INSTRMNT_ID, ENTTY_RL_TYP, PRTY_ID,
       MN_DBTR_INDCTR, MN_LSS_INDCTR, MN_DPST_TKNG_CRPRTN_INDCTR
FROM INSTRMNT_ENTTY_RL_ASSGNMNT_IL
WHERE DT_RFRNC = getvariable('dt_rfrnc')
  AND RPRTNG_AGNT_ID = getvariable('rprtng_agnt_id')
  AND ACCNTNG_CNSLDTN_LVL = getvariable('accntng_cnsldtn_lvl')
  AND ACCNTNG_STNDRD = getvariable('accntng_stndrd');

CREATE OR REPLACE VIEW prty_il_snp AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, PRTY_ID,
       INSTTTNL_SCTR, MLTLTRL_DVLPMNT_BNK_INDCTR
FROM PRTY_IL
WHERE DT_RFRNC = getvariable('dt_rfrnc')
  AND RPRTNG_AGNT_ID = getvariable('rprtng_agnt_id')
  AND ACCNTNG_CNSLDTN_LVL = getvariable('accntng_cnsldtn_lvl')
  AND ACCNTNG_STNDRD = getvariable('accntng_stndrd');

CREATE OR REPLACE VIEW intrnl_grp_rl_il_snp AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, GRP_ID, GRP_RL_TYP, FNRP_RPRTNG_SCHM
FROM INTRNL_GRP_RL_IL
WHERE DT_RFRNC = getvariable('dt_rfrnc')
  AND RPRTNG_AGNT_ID = getvariable('rprtng_agnt_id')
  AND ACCNTNG_CNSLDTN_LVL = getvariable('accntng_cnsldtn_lvl')
  AND ACCNTNG_STNDRD = getvariable('accntng_stndrd');

CREATE OR REPLACE VIEW otc_drvtv_hdg_il_snp AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, INSTRMNT_ID, ACCNTNG_HDG_INDCTR
FROM OTC_DRVTV_HDG_IL
WHERE DT_RFRNC = getvariable('dt_rfrnc')
  AND RPRTNG_AGNT_ID = getvariable('rprtng_agnt_id')
  AND ACCNTNG_CNSLDTN_LVL = getvariable('accntng_cnsldtn_lvl')
  AND ACCNTNG_STNDRD = getvariable('accntng_stndrd');

CREATE OR REPLACE VIEW scrty_exchng_trdbl_drvtv_il_snp AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, SCRTY_EXCHNG_TRDBL_DRVTV_ID,
       SCRTY_EXCHNG_TRDBL_DRVTV_TYP, NGTBL_SCRTY_INDCTR, DBT_SCRTY_PRFRMNG_STTS_TYP
FROM SCRTY_EXCHNG_TRDBL_DRVTV_IL
WHERE DT_RFRNC = getvariable('dt_rfrnc')
  AND RPRTNG_AGNT_ID = getvariable('rprtng_agnt_id')
  AND ACCNTNG_CNSLDTN_LVL = getvariable('accntng_cnsldtn_lvl')
  AND ACCNTNG_STNDRD = getvariable('accntng_stndrd');

CREATE OR REPLACE VIEW scrty_entty_rl_assgnmnt_il_snp AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, SCRTY_EXCHNG_TRDBL_DRVTV_ID,
       ENTTY_RL_TYP, PRTY_ID, PRMRY_ISSR_INDCTR
FROM SCRTY_ENTTY_RL_ASSGNMNT_IL
WHERE DT_RFRNC = getvariable('dt_rfrnc')
  AND RPRTNG_AGNT_ID = getvariable('rprtng_agnt_id')
  AND ACCNTNG_CNSLDTN_LVL = getvariable('accntng_cnsldtn_lvl')
  AND ACCNTNG_STNDRD = getvariable('accntng_stndrd');

CREATE OR REPLACE VIEW lng_shrt_blnc_sht_rcgnsd_scrty_pstn_il_snp AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, SCRTY_ID, INVSTR_PRTY_ID,
       INVSTR_ENTTY_RL_TYP, SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP, LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP, HLD_SL_INDCTR
FROM LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL
WHERE DT_RFRNC = getvariable('dt_rfrnc')
  AND RPRTNG_AGNT_ID = getvariable('rprtng_agnt_id')
  AND ACCNTNG_CNSLDTN_LVL = getvariable('accntng_cnsldtn_lvl')
  AND ACCNTNG_STNDRD = getvariable('accntng_stndrd');

CREATE OR REPLACE VIEW lng_blnc_sht_rcgnsd_scrty_pstn_accntng_il_snp AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, SCRTY_ID, INVSTR_PRTY_ID,
       INVSTR_ENTTY_RL_TYP, SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP, LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP,
       PRDNTL_PRTFL_TYP, ACCNTNG_CLSSFCTN, SBJCT_IMPRMNT_INDCTR, IMPRMNT_STTS,
       CRRYNG_AMNT, ACCMLTD_IMPRMNT, FV, ACCMLTD_CHNGS_FV_CR, GNRL_ALLWNCS_CRDT_RSK, GNRL_ALLWNCS_BNK_RSK
FROM LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL
WHERE DT_RFRNC = getvariable('dt_rfrnc')
  AND RPRTNG_AGNT_ID = getvariable('rprtng_agnt_id')
  AND ACCNTNG_CNSLDTN_LVL = getvariable('accntng_cnsldtn_lvl')
  AND ACCNTNG_STNDRD = getvariable('accntng_stndrd');
