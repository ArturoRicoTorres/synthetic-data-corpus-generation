-- Long balance sheet recognised security positions per prudential portfolio and accounting portfolio:
-- performing status of the security, gross carrying amount and type of financial asset per Annex V.

CREATE OR REPLACE VIEW scrty_exchng_trdbl_drvtv_eil AS
SELECT DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL, ACCNTNG_STNDRD, SCRTY_EXCHNG_TRDBL_DRVTV_ID,
       DBT_SCRTY_PRFRMNG_STTS_TYP
FROM scrty_exchng_trdbl_drvtv_il_snp;

CREATE OR REPLACE VIEW lng_scrty_pstn_eil_grss_crryng_amnt AS
SELECT c.DT_RFRNC, c.RPRTNG_AGNT_ID, c.ACCNTNG_CNSLDTN_LVL, c.ACCNTNG_STNDRD, c.SCRTY_ID, c.INVSTR_PRTY_ID,
       c.INVSTR_ENTTY_RL_TYP, c.SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP, c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP,
       c.PRDNTL_PRTFL_TYP, c.ACCNTNG_CLSSFCTN,
       CASE
           WHEN (
                   c.ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_2', 'ACCNTNG_CLSSFCTN_3')
                   OR (c.ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_41', 'ACCNTNG_CLSSFCTN_4', 'ACCNTNG_CLSSFCTN_7',
                                              'ACCNTNG_CLSSFCTN_49')
                       AND s.DBT_SCRTY_PRFRMNG_STTS_TYP = 'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_19')
                   OR (c.ACCNTNG_CLSSFCTN = 'ACCNTNG_CLSSFCTN_9'
                       AND c.SBJCT_IMPRMNT_INDCTR = 'SBJCT_IMPRMNT_INDCTR_2'
                       AND s.DBT_SCRTY_PRFRMNG_STTS_TYP = 'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_19')
                )
                AND c.FV IS NOT NULL
               THEN c.FV
           WHEN (
                   (c.ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_41', 'ACCNTNG_CLSSFCTN_4', 'ACCNTNG_CLSSFCTN_7',
                                           'ACCNTNG_CLSSFCTN_49')
                    AND s.DBT_SCRTY_PRFRMNG_STTS_TYP = 'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20')
                   OR (c.ACCNTNG_CLSSFCTN = 'ACCNTNG_CLSSFCTN_9'
                       AND c.SBJCT_IMPRMNT_INDCTR = 'SBJCT_IMPRMNT_INDCTR_2'
                       AND s.DBT_SCRTY_PRFRMNG_STTS_TYP = 'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20')
                )
                AND c.FV IS NOT NULL
                AND c.ACCMLTD_CHNGS_FV_CR < 0
               THEN c.FV - c.ACCMLTD_CHNGS_FV_CR
           WHEN (
                   c.ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_8', 'ACCNTNG_CLSSFCTN_6')
                   OR (c.ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_76', 'ACCNTNG_CLSSFCTN_77', 'ACCNTNG_CLSSFCTN_44')
                       AND c.IMPRMNT_STTS = 'CRDT_QLTY_26')
                   OR (c.ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_9', 'ACCNTNG_CLSSFCTN_73', 'ACCNTNG_CLSSFCTN_74')
                       AND c.SBJCT_IMPRMNT_INDCTR = 'SBJCT_IMPRMNT_INDCTR_1'
                       AND c.IMPRMNT_STTS = 'CRDT_QLTY_26')
                )
                AND c.CRRYNG_AMNT IS NOT NULL
                AND c.ACCMLTD_IMPRMNT IS NOT NULL
               THEN c.CRRYNG_AMNT + c.ACCMLTD_IMPRMNT
           WHEN (
                   (c.ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_76', 'ACCNTNG_CLSSFCTN_77', 'ACCNTNG_CLSSFCTN_44')
                    AND c.IMPRMNT_STTS IN ('CRDT_QLTY_211', 'CRDT_QLTY_212'))
                   OR (c.ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_9', 'ACCNTNG_CLSSFCTN_73', 'ACCNTNG_CLSSFCTN_74')
                       AND c.SBJCT_IMPRMNT_INDCTR = 'SBJCT_IMPRMNT_INDCTR_1'
                       AND c.IMPRMNT_STTS IN ('CRDT_QLTY_211', 'CRDT_QLTY_212'))
                )
                AND c.CRRYNG_AMNT IS NOT NULL
                AND (c.GNRL_ALLWNCS_CRDT_RSK IS NOT NULL OR c.GNRL_ALLWNCS_BNK_RSK IS NOT NULL)
               THEN c.CRRYNG_AMNT + c.GNRL_ALLWNCS_CRDT_RSK + c.GNRL_ALLWNCS_BNK_RSK
           WHEN (
                   (c.ACCNTNG_CLSSFCTN = 'ACCNTNG_CLSSFCTN_73'              -- measured at cost
                    AND c.SBJCT_IMPRMNT_INDCTR = 'SBJCT_IMPRMNT_INDCTR_2')
                   OR (c.ACCNTNG_CLSSFCTN = 'ACCNTNG_CLSSFCTN_44'           -- measured at cost
                       AND c.IMPRMNT_STTS NOT IN ('CRDT_QLTY_26', 'CRDT_QLTY_211', 'CRDT_QLTY_212'))
                )
                AND c.CRRYNG_AMNT IS NOT NULL
               THEN c.CRRYNG_AMNT
           WHEN c.FV IS NULL AND c.CRRYNG_AMNT IS NULL
               THEN NULL
       END AS GRSS_CRRYNG_AMNT
FROM lng_blnc_sht_rcgnsd_scrty_pstn_accntng_il_snp AS c
JOIN scrty_exchng_trdbl_drvtv_il_snp AS s
  ON  s.DT_RFRNC = c.DT_RFRNC AND s.RPRTNG_AGNT_ID = c.RPRTNG_AGNT_ID
  AND s.ACCNTNG_CNSLDTN_LVL = c.ACCNTNG_CNSLDTN_LVL AND s.ACCNTNG_STNDRD = c.ACCNTNG_STNDRD
  AND s.SCRTY_EXCHNG_TRDBL_DRVTV_ID = c.SCRTY_ID;

CREATE OR REPLACE VIEW lng_scrty_pstn_eil_typ_fnncl_asst AS
SELECT c.DT_RFRNC, c.RPRTNG_AGNT_ID, c.ACCNTNG_CNSLDTN_LVL, c.ACCNTNG_STNDRD, c.SCRTY_ID, c.INVSTR_PRTY_ID,
       c.INVSTR_ENTTY_RL_TYP, c.SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP, c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP,
       c.PRDNTL_PRTFL_TYP, c.ACCNTNG_CLSSFCTN,
       MAX(
       CASE
           WHEN s.SCRTY_EXCHNG_TRDBL_DRVTV_TYP IN ('SCRTY_EXCHNG_TRDBL_DRVTV_TYP_11', 'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_14',
                                                    'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_13', 'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_5')
                AND s.NGTBL_SCRTY_INDCTR = 'NGTBL_SCRTY_2'          -- non-negotiable: loans and advances
               THEN CASE
                        WHEN c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP = 'LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4'
                             OR (c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP = 'LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3'
                                 AND l.HLD_SL_INDCTR = 'HLD_SL_INDCTR_2')
                            THEN 'TYP_INSTRMNT_1117'
                        WHEN c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP = 'LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3'
                             AND l.HLD_SL_INDCTR = 'HLD_SL_INDCTR_1'
                            THEN 'TYP_INSTRMNT_1118'
                    END
           WHEN s.SCRTY_EXCHNG_TRDBL_DRVTV_TYP IN ('SCRTY_EXCHNG_TRDBL_DRVTV_TYP_11', 'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_14',
                                                    'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_13', 'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_5')
                AND s.NGTBL_SCRTY_INDCTR = 'NGTBL_SCRTY_1'          -- negotiable: debt securities
               THEN CASE
                        WHEN c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP = 'LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4'
                             OR (c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP = 'LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3'
                                 AND l.HLD_SL_INDCTR = 'HLD_SL_INDCTR_2')
                            THEN 'TYP_INSTRMNT_1116'
                        WHEN c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP = 'LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3'
                             AND l.HLD_SL_INDCTR = 'HLD_SL_INDCTR_1'
                            THEN 'TYP_INSTRMNT_1118'
                    END
           WHEN s.SCRTY_EXCHNG_TRDBL_DRVTV_TYP = 'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_6'   -- equity securities
               THEN CASE
                        WHEN (c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP = 'LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4'
                              AND e.ENTTY_RL_TYP = 'ENTTY_RL_TYP_8'
                              AND e.PRTY_ID <> e.RPRTNG_AGNT_ID)
                             OR (c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP = 'LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3'
                                 AND l.HLD_SL_INDCTR = 'HLD_SL_INDCTR_2')
                            THEN 'TYP_INSTRMNT_1115'
                        WHEN c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP = 'LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3'
                             AND l.HLD_SL_INDCTR = 'HLD_SL_INDCTR_1'
                            THEN 'TYP_INSTRMNT_1118'
                    END
           ELSE NULL
       END) AS TYP_FNNCL_ASST_INSTRMNT_ANNX_V
FROM lng_blnc_sht_rcgnsd_scrty_pstn_accntng_il_snp AS c
JOIN scrty_exchng_trdbl_drvtv_il_snp AS s
  ON  s.DT_RFRNC = c.DT_RFRNC AND s.RPRTNG_AGNT_ID = c.RPRTNG_AGNT_ID
  AND s.ACCNTNG_CNSLDTN_LVL = c.ACCNTNG_CNSLDTN_LVL AND s.ACCNTNG_STNDRD = c.ACCNTNG_STNDRD
  AND s.SCRTY_EXCHNG_TRDBL_DRVTV_ID = c.SCRTY_ID
LEFT JOIN lng_shrt_blnc_sht_rcgnsd_scrty_pstn_il_snp AS l
  ON  l.DT_RFRNC = c.DT_RFRNC AND l.RPRTNG_AGNT_ID = c.RPRTNG_AGNT_ID
  AND l.ACCNTNG_CNSLDTN_LVL = c.ACCNTNG_CNSLDTN_LVL AND l.ACCNTNG_STNDRD = c.ACCNTNG_STNDRD
  AND l.SCRTY_ID = c.SCRTY_ID AND l.INVSTR_PRTY_ID = c.INVSTR_PRTY_ID
  AND l.INVSTR_ENTTY_RL_TYP = c.INVSTR_ENTTY_RL_TYP
  AND l.SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP = c.SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP
  AND l.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP = c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP
LEFT JOIN scrty_entty_rl_assgnmnt_il_snp AS e
  ON  e.DT_RFRNC = c.DT_RFRNC AND e.RPRTNG_AGNT_ID = c.RPRTNG_AGNT_ID
  AND e.ACCNTNG_CNSLDTN_LVL = c.ACCNTNG_CNSLDTN_LVL AND e.ACCNTNG_STNDRD = c.ACCNTNG_STNDRD
  AND e.SCRTY_EXCHNG_TRDBL_DRVTV_ID = c.SCRTY_ID
GROUP BY c.DT_RFRNC, c.RPRTNG_AGNT_ID, c.ACCNTNG_CNSLDTN_LVL, c.ACCNTNG_STNDRD, c.SCRTY_ID, c.INVSTR_PRTY_ID,
         c.INVSTR_ENTTY_RL_TYP, c.SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP, c.LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP,
         c.PRDNTL_PRTFL_TYP, c.ACCNTNG_CLSSFCTN;
