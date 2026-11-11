/*
File: 06_reporting_scheme_scope.sql
Purpose: Keeps a reporting context only when the reporting agent reports FINREP on a full, simplified or
over-simplified basis.
Follows the official BIRD routine(s): R_F_18.00.a_ALL
Creates:
  f_18_00_a_scp
*/

/* Reporting contexts that report the template: full, simplified or over-simplified FINREP scheme */
/* of the reporting agent's internal group role. */
CREATE OR ALTER VIEW f_18_00_a_scp AS
SELECT DISTINCT
  DT_RFRNC,
  RPRTNG_AGNT_ID,
  ACCNTNG_CNSLDTN_LVL,
  ACCNTNG_STNDRD
FROM intrnl_grp_rl_eil
WHERE
  GRP_RL_TYP = 'GRP_RL_TYP_1'
  AND FNRP_RPRTNG_SCHM IN ('FNRP_RPRTNG_SCHM_1', 'FNRP_RPRTNG_SCHM_2', 'FNRP_RPRTNG_SCHM_3')
GO
