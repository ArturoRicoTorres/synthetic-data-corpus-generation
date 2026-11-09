-- Type of financial asset per Annex V, per instrument role.
-- The routine reads attributes of the instrument, its role, its entity-role assignments, the counterparty and
-- the hedge record. One instrument role can have several assignments; the derived type is taken over all of them.

CREATE OR REPLACE VIEW instrmnt_rl_eil_typ_fnncl_asst AS
SELECT rl.DT_RFRNC, rl.RPRTNG_AGNT_ID, rl.ACCNTNG_CNSLDTN_LVL, rl.ACCNTNG_STNDRD, rl.INSTRMNT_ID, rl.INSTRMNT_RL_TYP,
       MAX(
       CASE
           WHEN (   -- loans and advances
                   (
                       (i.INSTRMNT_TYP_PRDCT IN ('TYP_INSTRMNT_1020', 'TYP_INSTRMNT_1022', 'TYP_INSTRMNT_1023',
                                                 'TYP_INSTRMNT_120', 'TYP_INSTRMNT_130', 'TYP_INSTRMNT_140',
                                                 'TYP_INSTRMNT_162', 'TYP_INSTRMNT_163', 'TYP_INSTRMNT_51')
                        AND a.ENTTY_RL_TYP = 'ENTTY_RL_TYP_28'
                        AND a.MN_DBTR_INDCTR = 'MN_DBTR_INDCTR_1')
                       OR
                       (i.INSTRMNT_TYP_PRDCT = 'TYP_INSTRMNT_80'
                        AND a.ENTTY_RL_TYP = 'ENTTY_RL_TYP_19'
                        AND a.MN_LSS_INDCTR = 'MN_LSS_INDCTR_1')
                       OR
                       (i.INSTRMNT_TYP_PRDCT IN ('TYP_INSTRMNT_511', 'TYP_INSTRMNT_512', 'TYP_INSTRMNT_522',
                                                 'TYP_INSTRMNT_1202')
                        AND a.ENTTY_RL_TYP = 'ENTTY_RL_TYP_27'
                        AND a.MN_DPST_TKNG_CRPRTN_INDCTR = 'MN_DPST_TKNG_CRPRTN_INDCTR_1')
                   )
                   AND
                   (p.INSTTTNL_SCTR NOT IN ('INSTTTNL_SCTR_S121', 'INSTTTNL_SCTR_S122_A')
                    OR (p.INSTTTNL_SCTR IN ('INSTTTNL_SCTR_S121', 'INSTTTNL_SCTR_S122_A')
                        AND i.RPYMNT_RGHTS = 'RPYMNT_RGHTS_2'))
                )
               THEN CASE
                        WHEN rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_34'
                             OR (rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                                 AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_2')
                            THEN 'TYP_INSTRMNT_1117'
                        WHEN rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                             AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_1'
                            THEN 'TYP_INSTRMNT_1118'
                    END
           WHEN (   -- cash balances at central banks
                   (
                       (i.INSTRMNT_TYP_PRDCT IN ('TYP_INSTRMNT_511', 'TYP_INSTRMNT_512', 'TYP_INSTRMNT_522',
                                                 'TYP_INSTRMNT_1202')
                        AND i.RPYMNT_RGHTS = 'RPYMNT_RGHTS_1')
                       OR i.INSTRMNT_TYP_PRDCT = 'TYP_INSTRMNT_1201'
                   )
                   AND a.ENTTY_RL_TYP = 'ENTTY_RL_TYP_27'
                   AND a.MN_DPST_TKNG_CRPRTN_INDCTR = 'MN_DPST_TKNG_CRPRTN_INDCTR_1'
                   AND p.INSTTTNL_SCTR = 'INSTTTNL_SCTR_S121'
                )
               THEN CASE
                        WHEN rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_34'
                             OR (rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                                 AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_2')
                            THEN 'TYP_INSTRMNT_1112'
                        WHEN rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                             AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_1'
                            THEN 'TYP_INSTRMNT_1118'
                    END
           WHEN (   -- other demand deposits
                   i.INSTRMNT_TYP_PRDCT IN ('TYP_INSTRMNT_511', 'TYP_INSTRMNT_512', 'TYP_INSTRMNT_522',
                                            'TYP_INSTRMNT_1202')
                   AND i.RPYMNT_RGHTS = 'RPYMNT_RGHTS_1'
                   AND a.ENTTY_RL_TYP = 'ENTTY_RL_TYP_27'
                   AND a.MN_DPST_TKNG_CRPRTN_INDCTR = 'MN_DPST_TKNG_CRPRTN_INDCTR_1'
                   AND p.INSTTTNL_SCTR = 'INSTTTNL_SCTR_S122_A'
                )
               THEN CASE
                        WHEN rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_34'
                             OR (rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                                 AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_2')
                            THEN 'TYP_INSTRMNT_1113'
                        WHEN rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                             AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_1'
                            THEN 'TYP_INSTRMNT_1118'
                    END
           WHEN i.INSTRMNT_TYP_PRDCT = 'TYP_INSTRMNT_2'      -- equity instruments
               THEN CASE
                        WHEN (rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_34'
                              AND a.ENTTY_RL_TYP = 'ENTTY_RL_TYP_8'
                              AND a.PRTY_ID <> a.RPRTNG_AGNT_ID)
                             OR (rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                                 AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_2')
                            THEN 'TYP_INSTRMNT_1115'
                        WHEN rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                             AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_1'
                            THEN 'TYP_INSTRMNT_1118'
                    END
           WHEN i.INSTRMNT_TYP_PRDCT IN ('TYP_INSTRMNT_10', 'TYP_INSTRMNT_380', 'TYP_INSTRMNT_5', 'TYP_INSTRMNT_6',
                                         'TYP_INSTRMNT_7', 'TYP_INSTRMNT_8', 'TYP_INSTRMNT_9')
                AND h.ACCNTNG_HDG_INDCTR = 'ACCNTNG_HDG_INDCTR_2'  -- derivatives, not a hedge
               THEN CASE
                        WHEN rl.INSTRMNT_RL_TYP IN ('ABSTRCT_INSTRMNT_RL_TYP_34', 'ABSTRCT_INSTRMNT_RL_TYP_102')
                             OR (rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                                 AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_2')
                            THEN 'TYP_INSTRMNT_1114'
                        WHEN rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                             AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_1'
                            THEN 'TYP_INSTRMNT_1118'
                    END
           WHEN i.INSTRMNT_TYP_PRDCT IN ('TYP_INSTRMNT_10', 'TYP_INSTRMNT_380', 'TYP_INSTRMNT_5', 'TYP_INSTRMNT_6',
                                         'TYP_INSTRMNT_7', 'TYP_INSTRMNT_8', 'TYP_INSTRMNT_9')
                AND h.ACCNTNG_HDG_INDCTR = 'ACCNTNG_HDG_INDCTR_1'  -- derivatives, hedge accounting
               THEN CASE
                        WHEN rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_34'
                             OR (rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                                 AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_2')
                            THEN 'TYP_INSTRMNT_1119'
                        WHEN rl.INSTRMNT_RL_TYP = 'ABSTRCT_INSTRMNT_RL_TYP_35'
                             AND rl.HLD_SL_INDCTR = 'HLD_SL_INDCTR_1'
                            THEN 'TYP_INSTRMNT_1118'
                    END
           ELSE NULL
       END) AS TYP_FNNCL_ASST_INSTRMNT_ANNX_V
FROM instrmnt_rl_il_snp AS rl
JOIN instrmnt_il_snp AS i
  ON  i.DT_RFRNC = rl.DT_RFRNC AND i.RPRTNG_AGNT_ID = rl.RPRTNG_AGNT_ID
  AND i.ACCNTNG_CNSLDTN_LVL = rl.ACCNTNG_CNSLDTN_LVL AND i.ACCNTNG_STNDRD = rl.ACCNTNG_STNDRD
  AND i.INSTRMNT_ID = rl.INSTRMNT_ID
LEFT JOIN instrmnt_entty_rl_assgnmnt_il_snp AS a
  ON  a.DT_RFRNC = rl.DT_RFRNC AND a.RPRTNG_AGNT_ID = rl.RPRTNG_AGNT_ID
  AND a.ACCNTNG_CNSLDTN_LVL = rl.ACCNTNG_CNSLDTN_LVL AND a.ACCNTNG_STNDRD = rl.ACCNTNG_STNDRD
  AND a.INSTRMNT_ID = rl.INSTRMNT_ID
LEFT JOIN prty_il_snp AS p
  ON  p.DT_RFRNC = a.DT_RFRNC AND p.RPRTNG_AGNT_ID = a.RPRTNG_AGNT_ID
  AND p.ACCNTNG_CNSLDTN_LVL = a.ACCNTNG_CNSLDTN_LVL AND p.ACCNTNG_STNDRD = a.ACCNTNG_STNDRD
  AND p.PRTY_ID = a.PRTY_ID
LEFT JOIN otc_drvtv_hdg_il_snp AS h
  ON  h.DT_RFRNC = rl.DT_RFRNC AND h.RPRTNG_AGNT_ID = rl.RPRTNG_AGNT_ID
  AND h.ACCNTNG_CNSLDTN_LVL = rl.ACCNTNG_CNSLDTN_LVL AND h.ACCNTNG_STNDRD = rl.ACCNTNG_STNDRD
  AND h.INSTRMNT_ID = rl.INSTRMNT_ID
GROUP BY rl.DT_RFRNC, rl.RPRTNG_AGNT_ID, rl.ACCNTNG_CNSLDTN_LVL, rl.ACCNTNG_STNDRD, rl.INSTRMNT_ID,
         rl.INSTRMNT_RL_TYP;
