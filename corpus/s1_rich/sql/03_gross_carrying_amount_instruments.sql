/*
File: 03_gross_carrying_amount_instruments.sql
Purpose: Derives the gross carrying amount of each instrument role from the carrying amount, accumulated
impairment, fair value and general allowances, depending on the accounting portfolio and the impairment
status.
Follows the official BIRD routine(s): R_DER_GRSS_CRRYNG_AMNT_3
Creates:
  instrmnt_rl_eil_grss_crryng_amnt
    GRSS_CRRYNG_AMNT                         Gross carrying amount
*/

/* Gross carrying amount per instrument role (Annex V). Branches are evaluated in the order of the routine. */
CREATE OR ALTER VIEW instrmnt_rl_eil_grss_crryng_amnt AS
SELECT
  DT_RFRNC,
  RPRTNG_AGNT_ID,
  ACCNTNG_CNSLDTN_LVL,
  ACCNTNG_STNDRD,
  INSTRMNT_ID,
  INSTRMNT_RL_TYP,
  CASE
    WHEN (
      ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_2', 'ACCNTNG_CLSSFCTN_3')
      OR (
        ACCNTNG_CLSSFCTN IN (
          'ACCNTNG_CLSSFCTN_41',
          'ACCNTNG_CLSSFCTN_4',
          'ACCNTNG_CLSSFCTN_7',
          'ACCNTNG_CLSSFCTN_49'
        )
        AND PRFRMNG_STTS = 'CRDT_QLTY_11'
      )
      OR (
        ACCNTNG_CLSSFCTN = 'ACCNTNG_CLSSFCTN_9'
        AND SBJCT_IMPRMNT_INDCTR = 'SBJCT_IMPRMNT_INDCTR_2'
        AND PRFRMNG_STTS = 'CRDT_QLTY_11'
      )
    )
    AND NOT FV IS NULL
    THEN FV
    WHEN (
      (
        ACCNTNG_CLSSFCTN IN (
          'ACCNTNG_CLSSFCTN_41',
          'ACCNTNG_CLSSFCTN_4',
          'ACCNTNG_CLSSFCTN_7',
          'ACCNTNG_CLSSFCTN_49'
        )
        AND PRFRMNG_STTS = 'CRDT_QLTY_1'
      )
      OR (
        ACCNTNG_CLSSFCTN = 'ACCNTNG_CLSSFCTN_9'
        AND SBJCT_IMPRMNT_INDCTR = 'SBJCT_IMPRMNT_INDCTR_2'
        AND PRFRMNG_STTS = 'CRDT_QLTY_1'
      )
    )
    AND NOT FV IS NULL
    AND ACCMLTD_CHNGS_FV_CR < 0
    THEN FV - ACCMLTD_CHNGS_FV_CR
    WHEN (
      ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_8', 'ACCNTNG_CLSSFCTN_6')
      OR (
        ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_76', 'ACCNTNG_CLSSFCTN_77', 'ACCNTNG_CLSSFCTN_44')
        AND IMPRMNT_STTS = 'CRDT_QLTY_26'
      )
      OR (
        ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_9', 'ACCNTNG_CLSSFCTN_73', 'ACCNTNG_CLSSFCTN_74')
        AND SBJCT_IMPRMNT_INDCTR = 'SBJCT_IMPRMNT_INDCTR_1'
        AND IMPRMNT_STTS = 'CRDT_QLTY_26'
      )
    )
    AND NOT CRRYNG_AMNT IS NULL
    AND NOT ACCMLTD_IMPRMNT IS NULL
    THEN CRRYNG_AMNT + ACCMLTD_IMPRMNT
    WHEN (
      (
        ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_76', 'ACCNTNG_CLSSFCTN_77', 'ACCNTNG_CLSSFCTN_44')
        AND IMPRMNT_STTS IN ('CRDT_QLTY_211', 'CRDT_QLTY_212')
      )
      OR (
        ACCNTNG_CLSSFCTN IN ('ACCNTNG_CLSSFCTN_9', 'ACCNTNG_CLSSFCTN_73', 'ACCNTNG_CLSSFCTN_74')
        AND SBJCT_IMPRMNT_INDCTR = 'SBJCT_IMPRMNT_INDCTR_1'
        AND IMPRMNT_STTS IN ('CRDT_QLTY_211', 'CRDT_QLTY_212')
      )
    )
    AND NOT CRRYNG_AMNT IS NULL
    AND (
      NOT GNRL_ALLWNCS_CRDT_RSK IS NULL OR NOT GNRL_ALLWNCS_BNK_RSK IS NULL
    )
    THEN CRRYNG_AMNT + GNRL_ALLWNCS_CRDT_RSK + GNRL_ALLWNCS_BNK_RSK
    WHEN (
      (
        ACCNTNG_CLSSFCTN = 'ACCNTNG_CLSSFCTN_73' /* measured at cost */
        AND SBJCT_IMPRMNT_INDCTR = 'SBJCT_IMPRMNT_INDCTR_2'
      )
      OR (
        ACCNTNG_CLSSFCTN = 'ACCNTNG_CLSSFCTN_44' /* measured at cost */
        AND NOT IMPRMNT_STTS IN ('CRDT_QLTY_26', 'CRDT_QLTY_211', 'CRDT_QLTY_212')
      )
    )
    AND NOT CRRYNG_AMNT IS NULL
    THEN CRRYNG_AMNT
    WHEN FV IS NULL AND CRRYNG_AMNT IS NULL
    THEN NULL
  END AS GRSS_CRRYNG_AMNT
FROM instrmnt_rl_il_snp
GO
