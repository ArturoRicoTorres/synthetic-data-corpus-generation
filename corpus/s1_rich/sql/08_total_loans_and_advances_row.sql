/*
File: 08_total_loans_and_advances_row.sql
Purpose: Row 0070 "Loans and advances" of template F 18.00.a: all positions of the counterparty sector rows.
Follows the official BIRD routine(s): R_F_18.00.a_R0070
Creates:
  f_18_00_a_r0070
    PSTN_SRC                                 Origin of the position (instrument or security position)
    PSTN_ID                                  Identifier of the instrument or security
    GRSS_CRRYNG_AMNT                         Gross carrying amount
    PRFRMNG_STTS                             Performing status
    DBT_SCRTY_PRFRMNG_STTS_TYP               Debt security by Performing status type
    SRC_RW                                   Counterparty sector row the position comes from
*/

/* Row 0070 (loans and advances) is the sum of the counterparty-sector rows. */
CREATE OR ALTER VIEW f_18_00_a_r0070 AS
SELECT
  DT_RFRNC,
  RPRTNG_AGNT_ID,
  ACCNTNG_CNSLDTN_LVL,
  ACCNTNG_STNDRD,
  PSTN_SRC,
  PSTN_ID,
  GRSS_CRRYNG_AMNT,
  PRFRMNG_STTS,
  DBT_SCRTY_PRFRMNG_STTS_TYP,
  RW AS SRC_RW
FROM f_18_00_a_sctr_rw
WHERE
  RW IN ('R0080', 'R0090', 'R0100', 'R0110', 'R0120', 'R0150')
GO
