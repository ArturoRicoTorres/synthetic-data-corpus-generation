/*
File: 10_non_performing_cell.sql
Purpose: Cell row 0070, column 0060 of template F 18.00.a: gross carrying amount of non-performing loans and
advances.
Follows the official BIRD routine(s): R_F_18.00.a_C0060
Creates:
  f_18_00_a_r0070_c0060
    GRSS_CRRYNG_AMNT                         Gross carrying amount
*/

/* F 18.00.a row 0070, column 0060: gross carrying amount of non-performing exposures. */
CREATE OR ALTER VIEW f_18_00_a_r0070_c0060 AS
SELECT
  SUM(GRSS_CRRYNG_AMNT) AS GRSS_CRRYNG_AMNT
FROM f_18_00_a_r0070
WHERE
  GRSS_CRRYNG_AMNT > 0
  AND (
    PRFRMNG_STTS = 'CRDT_QLTY_1'
    OR DBT_SCRTY_PRFRMNG_STTS_TYP = 'SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20'
  )
GO
