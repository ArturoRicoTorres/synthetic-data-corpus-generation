/*
File: 02_carry_enriched_attributes.sql
Purpose: Passes status, classification and counterparty attributes unchanged into the enriched layer that the
reporting rules read.
Follows the official BIRD routine(s): R_IDT_DER
Creates:
  instrmnt_rl_eil
    ACCNTNG_CLSSFCTN                         Accounting classification
    PRFRMNG_STTS                             Performing status
  instrmnt_entty_rl_assgnmnt_eil
    ENTTY_RL_TYP                             Entity role type
    MN_DBTR_INDCTR                           Main debtor indicator
    MN_LSS_INDCTR                            Main lessee indicator
    MN_DPST_TKNG_CRPRTN_INDCTR               Main Deposit-taking corporation indicator
  prty_eil
    INSTTTNL_SCTR                            Institutional sector
    MLTLTRL_DVLPMNT_BNK_INDCTR               Multilateral development bank indicator
  intrnl_grp_rl_eil
    GRP_RL_TYP                               Internal group role type
    FNRP_RPRTNG_SCHM                         Finrep reporting scheme
  scrty_entty_rl_assgnmnt_eil
    ENTTY_RL_TYP                             Entity role type
    PRMRY_ISSR_INDCTR                        Primary issuer indicator
*/

/* Enriched layer: attributes carried over unchanged from the input snapshot (identity derivation). */
CREATE OR ALTER VIEW instrmnt_rl_eil AS
SELECT
  DT_RFRNC,
  RPRTNG_AGNT_ID,
  ACCNTNG_CNSLDTN_LVL,
  ACCNTNG_STNDRD,
  INSTRMNT_ID,
  INSTRMNT_RL_TYP,
  ACCNTNG_CLSSFCTN,
  PRFRMNG_STTS
FROM instrmnt_rl_il_snp
GO

CREATE OR ALTER VIEW instrmnt_entty_rl_assgnmnt_eil AS
SELECT
  DT_RFRNC,
  RPRTNG_AGNT_ID,
  ACCNTNG_CNSLDTN_LVL,
  ACCNTNG_STNDRD,
  INSTRMNT_ID,
  ENTTY_RL_TYP,
  PRTY_ID,
  MN_DBTR_INDCTR,
  MN_LSS_INDCTR,
  MN_DPST_TKNG_CRPRTN_INDCTR
FROM instrmnt_entty_rl_assgnmnt_il_snp
GO

CREATE OR ALTER VIEW prty_eil AS
SELECT
  DT_RFRNC,
  RPRTNG_AGNT_ID,
  ACCNTNG_CNSLDTN_LVL,
  ACCNTNG_STNDRD,
  PRTY_ID,
  INSTTTNL_SCTR,
  MLTLTRL_DVLPMNT_BNK_INDCTR
FROM prty_il_snp
GO

CREATE OR ALTER VIEW intrnl_grp_rl_eil AS
SELECT
  DT_RFRNC,
  RPRTNG_AGNT_ID,
  ACCNTNG_CNSLDTN_LVL,
  ACCNTNG_STNDRD,
  GRP_ID,
  GRP_RL_TYP,
  FNRP_RPRTNG_SCHM
FROM intrnl_grp_rl_il_snp
GO

CREATE OR ALTER VIEW scrty_entty_rl_assgnmnt_eil AS
SELECT
  DT_RFRNC,
  RPRTNG_AGNT_ID,
  ACCNTNG_CNSLDTN_LVL,
  ACCNTNG_STNDRD,
  SCRTY_EXCHNG_TRDBL_DRVTV_ID,
  ENTTY_RL_TYP,
  PRTY_ID,
  PRMRY_ISSR_INDCTR
FROM scrty_entty_rl_assgnmnt_il_snp
GO
