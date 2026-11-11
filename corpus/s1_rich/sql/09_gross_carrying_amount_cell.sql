/*
File: 09_gross_carrying_amount_cell.sql
Purpose: Cell row 0070, column 0010 of template F 18.00.a: total gross carrying amount of loans and advances.
Follows the official BIRD routine(s): R_F_18.00.a_C0010
Creates:
  f_18_00_a_r0070_c0010
    GRSS_CRRYNG_AMNT                         Gross carrying amount
*/

/* F 18.00.a row 0070, column 0010 (gross carrying amount). */
CREATE OR ALTER VIEW f_18_00_a_r0070_c0010 AS
SELECT
  SUM(GRSS_CRRYNG_AMNT) AS GRSS_CRRYNG_AMNT
FROM f_18_00_a_r0070
WHERE
  GRSS_CRRYNG_AMNT > 0
GO
