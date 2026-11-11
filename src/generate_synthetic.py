"""
Generate a small, seeded synthetic input layer for the NPL ratio reference implementation.

    python src/generate_synthetic.py [--seed 42] [--out data/synthetic] [--random 100]

Output (one CSV per input table, plus):
  contexts.csv        reporting contexts to evaluate
  expected_cases.csv  hand-written expected outcome of every named edge case

The data has two parts:
  * named edge cases (fixed), each with the sector rows it must land in, its gross carrying amount and whether it
    counts in column 0010 / 0060. Expected values are written by hand from the official algorithms, read literally
    (decisions OI-09, OI-11), so they are an oracle independent of both the SQL and the pandas check.
  * random positions (seeded), used only to reconcile the SQL with the pandas check.
"""
import argparse
import random
from decimal import Decimal
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

DT = "2026-06-30"
CTX = {
    "IFRS": {"DT_RFRNC": DT, "RPRTNG_AGNT_ID": "RA001", "ACCNTNG_CNSLDTN_LVL": "ACCNTNG_CNSLDTN_LVL_1",
             "ACCNTNG_STNDRD": "ACCNTNG_FRMWRK_2"},
    "NGAAP": {"DT_RFRNC": DT, "RPRTNG_AGNT_ID": "RA001", "ACCNTNG_CNSLDTN_LVL": "ACCNTNG_CNSLDTN_LVL_1",
              "ACCNTNG_STNDRD": "ACCNTNG_FRMWRK_1"},
    "SCHEME4": {"DT_RFRNC": DT, "RPRTNG_AGNT_ID": "RA002", "ACCNTNG_CNSLDTN_LVL": "ACCNTNG_CNSLDTN_LVL_1",
                "ACCNTNG_STNDRD": "ACCNTNG_FRMWRK_2"},
}
SCHEME = {"IFRS": "FNRP_RPRTNG_SCHM_1", "NGAAP": "FNRP_RPRTNG_SCHM_2", "SCHEME4": "FNRP_RPRTNG_SCHM_4"}

MAIN_FLAG = {"ENTTY_RL_TYP_28": "MN_DBTR_INDCTR", "ENTTY_RL_TYP_20": "MN_DBTR_INDCTR",
             "ENTTY_RL_TYP_19": "MN_LSS_INDCTR", "ENTTY_RL_TYP_27": "MN_DPST_TKNG_CRPRTN_INDCTR"}

# sector members used by the six sector rows (leaves only), by row
ROW_SECTORS = {
    "R0080": ["INSTTTNL_SCTR_S121"],
    "R0090": ["INSTTTNL_SCTR_S1311", "INSTTTNL_SCTR_S1312", "INSTTTNL_SCTR_S1313", "INSTTTNL_SCTR_S1314"],
    "R0100": ["INSTTTNL_SCTR_S122_A_1", "INSTTTNL_SCTR_S122_A_2"],
    "R0110": ["INSTTTNL_SCTR_S123", "INSTTTNL_SCTR_S124", "INSTTTNL_SCTR_S125_I", "INSTTTNL_SCTR_S125_C",
              "INSTTTNL_SCTR_S125_A", "INSTTTNL_SCTR_S125_E", "INSTTTNL_SCTR_S125_D", "INSTTTNL_SCTR_S125_B",
              "INSTTTNL_SCTR_S125_W", "INSTTTNL_SCTR_S126", "INSTTTNL_SCTR_S127", "INSTTTNL_SCTR_S128", "INSTTTNL_SCTR_S129",
              "INSTTTNL_SCTR_S122_B1", "INSTTTNL_SCTR_S122_B2"],
    "R0120": ["INSTTTNL_SCTR_S11"],
    "R0150": ["INSTTTNL_SCTR_S14_A", "INSTTTNL_SCTR_S14_B", "INSTTTNL_SCTR_S15"],
}


def D(x):
    return None if x is None else Decimal(str(x)).quantize(Decimal("0.01"))


class Book:
    """Collects input-layer rows per table."""

    def __init__(self):
        self.t = {}
        self.parties = set()
        self.cases = []

    def add(self, table, row):
        self.t.setdefault(table, []).append(row)

    def party(self, ctx, prty_id, sector, mdb=None):
        key = (tuple(ctx.values()), prty_id)
        if key not in self.parties:
            self.parties.add(key)
            self.add("PRTY_IL", {**ctx, "PRTY_ID": prty_id, "INSTTTNL_SCTR": sector,
                                 "MLTLTRL_DVLPMNT_BNK_INDCTR": mdb or "MLTLTRL_DVLPMNT_BNK_INDCTR_2"})

    # ---- instrument positions -------------------------------------------------------------------------------
    def instrument(self, ctx_name, iid, *, prod="TYP_INSTRMNT_1022", rpy="RPYMNT_RGHTS_2", acc=None, rl=None, hld=None,
                   sbjct="SBJCT_IMPRMNT_INDCTR_1", imp=None, prf="CRDT_QLTY_11", ca=None, ai=None, fv=None,
                   chfv=None, gc=None, gb=None, roles=(), hedge=None, ctx=None):
        """roles: list of (ENTTY_RL_TYP, is_main, sector, mdb)."""
        ctx = dict(ctx or CTX[ctx_name])
        ifrs = ctx["ACCNTNG_STNDRD"] == "ACCNTNG_FRMWRK_2"
        acc = acc or ("ACCNTNG_CLSSFCTN_6" if ifrs else "ACCNTNG_CLSSFCTN_77")
        rl = rl or ("ABSTRCT_INSTRMNT_RL_TYP_35" if ifrs else "ABSTRCT_INSTRMNT_RL_TYP_34")
        if hld is None and ifrs:
            hld = "HLD_SL_INDCTR_2"
        if imp is None and not ifrs:
            imp = "CRDT_QLTY_26"
        self.add("INSTRMNT_IL", {**ctx, "INSTRMNT_ID": iid, "INSTRMNT_TYP_PRDCT": prod, "RPYMNT_RGHTS": rpy})
        self.add("INSTRMNT_RL_IL", {**ctx, "INSTRMNT_ID": iid, "INSTRMNT_RL_TYP": rl, "ACCNTNG_CLSSFCTN": acc,
                                    "HLD_SL_INDCTR": hld, "SBJCT_IMPRMNT_INDCTR": sbjct, "IMPRMNT_STTS": imp,
                                    "PRFRMNG_STTS": prf, "CRRYNG_AMNT": D(ca), "ACCMLTD_IMPRMNT": D(ai), "FV": D(fv),
                                    "ACCMLTD_CHNGS_FV_CR": D(chfv), "GNRL_ALLWNCS_CRDT_RSK": D(gc),
                                    "GNRL_ALLWNCS_BNK_RSK": D(gb)})
        for n, (role, main, sector, mdb) in enumerate(roles):
            pid = f"P-{iid}-{n}"
            self.party(ctx, pid, sector, mdb)
            row = {**ctx, "INSTRMNT_ID": iid, "ENTTY_RL_TYP": role, "PRTY_ID": pid}
            if role in MAIN_FLAG:
                row[MAIN_FLAG[role]] = f"{MAIN_FLAG[role]}_{1 if main else 2}"
            self.add("INSTRMNT_ENTTY_RL_ASSGNMNT_IL", row)
        if hedge:
            self.add("OTC_DRVTV_HDG_IL", {**ctx, "INSTRMNT_ID": iid, "ACCNTNG_HDG_INDCTR": hedge})

    # ---- security positions ---------------------------------------------------------------------------------
    def security(self, ctx_name, sid, *, styp="SCRTY_EXCHNG_TRDBL_DRVTV_TYP_11", ngtbl="NGTBL_SCRTY_2",
                 dbt="SCRTY_EXCHNG_TRDBL_DRVTV_TYP_19", pstn=None, hld=None, acc=None, sbjct="SBJCT_IMPRMNT_INDCTR_1",
                 imp=None, ca=None, ai=None, fv=None, chfv=None, gc=None, gb=None, issuer=None, ctx=None):
        """issuer: (is_primary, sector, mdb) or None."""
        ctx = dict(ctx or CTX[ctx_name])
        ifrs = ctx["ACCNTNG_STNDRD"] == "ACCNTNG_FRMWRK_2"
        acc = acc or ("ACCNTNG_CLSSFCTN_6" if ifrs else "ACCNTNG_CLSSFCTN_76")
        pstn = pstn or ("LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3" if ifrs else "LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4")
        if hld is None and ifrs:
            hld = "HLD_SL_INDCTR_2"
        if imp is None and not ifrs:
            imp = "CRDT_QLTY_26"
        pkey = {"SCRTY_ID": sid, "INVSTR_PRTY_ID": ctx["RPRTNG_AGNT_ID"], "INVSTR_ENTTY_RL_TYP": "ENTTY_RL_TYP_33",
                "SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP": "SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP_1",
                "LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP": pstn}
        self.add("SCRTY_EXCHNG_TRDBL_DRVTV_IL", {**ctx, "SCRTY_EXCHNG_TRDBL_DRVTV_ID": sid,
                                                 "SCRTY_EXCHNG_TRDBL_DRVTV_TYP": styp, "NGTBL_SCRTY_INDCTR": ngtbl,
                                                 "DBT_SCRTY_PRFRMNG_STTS_TYP": dbt})
        self.add("LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL", {**ctx, **pkey, "HLD_SL_INDCTR": hld})
        self.add("LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL",
                 {**ctx, **pkey, "PRDNTL_PRTFL_TYP": "PRDNTL_PRTFL_TYP_2", "ACCNTNG_CLSSFCTN": acc,
                  "SBJCT_IMPRMNT_INDCTR": sbjct, "IMPRMNT_STTS": imp, "CRRYNG_AMNT": D(ca), "ACCMLTD_IMPRMNT": D(ai),
                  "FV": D(fv), "ACCMLTD_CHNGS_FV_CR": D(chfv), "GNRL_ALLWNCS_CRDT_RSK": D(gc),
                  "GNRL_ALLWNCS_BNK_RSK": D(gb)})
        if issuer:
            primary, sector, mdb = issuer
            pid = f"P-{sid}-ISSR"
            self.party(ctx, pid, sector, mdb)
            self.add("SCRTY_ENTTY_RL_ASSGNMNT_IL", {**ctx, "SCRTY_EXCHNG_TRDBL_DRVTV_ID": sid,
                                                    "ENTTY_RL_TYP": "ENTTY_RL_TYP_8", "PRTY_ID": pid,
                                                    "PRMRY_ISSR_INDCTR": f"PRMRY_ISSR_INDCTR_{1 if primary else 2}"})

    def case(self, case_id, ctx, src, pstn_id, rows, gca, c0010, c0060, note):
        self.cases.append({"case_id": case_id, "ctx": ctx, "pstn_src": src, "pstn_id": pstn_id,
                           "rows": ";".join(rows), "gca": "" if gca is None else str(D(gca)),
                           "c0010": int(c0010), "c0060": int(c0060), "note": note})


def debtor(sector, main=True, mdb=None):
    return ("ENTTY_RL_TYP_28", main, sector, mdb)


S11, S1311, S125A, S15 = "INSTTTNL_SCTR_S11", "INSTTTNL_SCTR_S1311", "INSTTTNL_SCTR_S125_A", "INSTTTNL_SCTR_S15"
MDB = "MLTLTRL_DVLPMNT_BNK_INDCTR_1"
NP, PF = "CRDT_QLTY_1", "CRDT_QLTY_11"


def edge_cases(b):
    I, S = "INSTRMNT", "SCRTY_PSTN"
    # ---- IFRS context: amortised cost (ACCNTNG_CLSSFCTN_6) -----------------------------------------------------
    b.instrument("IFRS", "C-I01", ca=1000, ai=50, roles=[debtor(S11)])
    b.case("I01", "IFRS", I, "C-I01", ["R0120"], 1050, 1, 0, "loan, amortised cost, performing, non-financial corp")
    b.instrument("IFRS", "C-I02", ca=800, ai=200, prf=NP, roles=[debtor(S11)])
    b.case("I02", "IFRS", I, "C-I02", ["R0120"], 1000, 1, 1, "loan, amortised cost, non-performing")
    b.instrument("IFRS", "C-I03", prod="TYP_INSTRMNT_80", ca=500, ai=100, prf=NP,
                 roles=[("ENTTY_RL_TYP_19", True, "INSTTTNL_SCTR_S14_A", None)])
    b.case("I03", "IFRS", I, "C-I03", ["R0150"], 600, 1, 1, "finance lease, main lessee, household")
    b.instrument("IFRS", "C-I04", prod="TYP_INSTRMNT_522", ca=300, ai=0,
                 roles=[("ENTTY_RL_TYP_27", True, "INSTTTNL_SCTR_S122_A_1", None)])
    b.case("I04", "IFRS", I, "C-I04", ["R0100"], 300, 1, 0, "term deposit at credit institution")
    b.instrument("IFRS", "C-I05", prod="TYP_INSTRMNT_522", ca=400, ai=0,
                 roles=[("ENTTY_RL_TYP_27", True, "INSTTTNL_SCTR_S121", None)])
    b.case("I05", "IFRS", I, "C-I05", ["R0080"], 400, 1, 0, "term deposit at central bank (not on demand)")
    b.instrument("IFRS", "C-I06", ca=700, ai=10, roles=[debtor(S1311)])
    b.case("I06", "IFRS", I, "C-I06", ["R0090"], 710, 1, 0, "loan to central government")
    b.instrument("IFRS", "C-I07", ca=900, ai=300, prf=NP, roles=[debtor(S125A)])
    b.case("I07", "IFRS", I, "C-I07", ["R0110"], 1200, 1, 1, "loan to financial vehicle corporation")
    b.instrument("IFRS", "C-I08", prod="TYP_INSTRMNT_51", ca=250, ai=5, roles=[debtor(S15)])
    b.case("I08", "IFRS", I, "C-I08", ["R0150"], 255, 1, 0, "credit card debt, non-profit serving households")
    b.instrument("IFRS", "C-I09", ca=600, ai=0, roles=[debtor("INSTTTNL_SCTR_S122_A_1", mdb=MDB)])
    b.case("I09", "IFRS", I, "C-I09", ["R0100"], 600, 1, 0, "development bank flag on a credit institution: once")
    b.instrument("IFRS", "C-I10", ca=1000, ai=100, hld="HLD_SL_INDCTR_1", roles=[debtor(S11)])
    b.case("I10", "IFRS", I, "C-I10", [], 1100, 0, 0, "IFRS held for sale: type 1118, excluded")
    b.instrument("IFRS", "C-I11", ca=500, ai=None, prf=NP, roles=[debtor(S11)])
    b.case("I11", "IFRS", I, "C-I11", ["R0120"], None, 0, 0, "null impairment: no gross carrying amount (OI-11)")
    b.instrument("IFRS", "C-I12", ca=0, ai=0, roles=[debtor(S11)])
    b.case("I12", "IFRS", I, "C-I12", ["R0120"], 0, 0, 0, "zero gross carrying amount")
    b.instrument("IFRS", "C-I13", ca=-100, ai=20, prf=NP, roles=[debtor(S11)])
    b.case("I13", "IFRS", I, "C-I13", ["R0120"], -80, 0, 0, "negative gross carrying amount")
    b.instrument("IFRS", "C-I14", ca=1000, ai=0, roles=[debtor(S11, main=False)])
    b.case("I14", "IFRS", I, "C-I14", [], 1000, 0, 0, "only a non-main debtor: not loans and advances")
    b.instrument("IFRS", "C-I15", ca=2000, ai=100, prf=NP, roles=[debtor(S11), debtor(S1311, main=False)])
    b.case("I15", "IFRS", I, "C-I15", ["R0120"], 2100, 1, 1, "main and non-main debtor: counted once, main sector")
    b.instrument("IFRS", "C-I16", acc="ACCNTNG_CLSSFCTN_8", ca=800, ai=8, roles=[debtor(S11)])
    b.case("I16", "IFRS", I, "C-I16", [], 808, 0, 0, "fair value through OCI portfolio: outside the cell")
    b.instrument("IFRS", "C-I17", prod="TYP_INSTRMNT_8", acc="ACCNTNG_CLSSFCTN_2", fv=50, hedge="ACCNTNG_HDG_INDCTR_1")
    b.case("I17", "IFRS", I, "C-I17", [], 50, 0, 0, "OTC swap, hedge accounting: type 1119")
    b.instrument("IFRS", "C-I18", prod="TYP_INSTRMNT_1202", rpy="RPYMNT_RGHTS_1", ca=300, ai=0,
                 roles=[("ENTTY_RL_TYP_27", True, "INSTTTNL_SCTR_S121", None)])
    b.case("I18", "IFRS", I, "C-I18", [], 300, 0, 0, "on-demand deposit at central bank: type 1112")
    b.instrument("IFRS", "C-I19", prod="TYP_INSTRMNT_1202", rpy="RPYMNT_RGHTS_1", ca=300, ai=0,
                 roles=[("ENTTY_RL_TYP_27", True, "INSTTTNL_SCTR_S122_A", None)])
    b.case("I19", "IFRS", I, "C-I19", [], 300, 0, 0, "on-demand deposit at credit institution: type 1113")
    b.instrument("IFRS", "C-I20", prod="TYP_INSTRMNT_1202", rpy="RPYMNT_RGHTS_1", ca=150, ai=0,
                 roles=[("ENTTY_RL_TYP_27", True, "INSTTTNL_SCTR_S122_A_1", None)])
    b.case("I20", "IFRS", I, "C-I20", ["R0100"], 150, 1, 0,
           "OI-17 literal: on-demand deposit, leaf sector S122_A_1 not excluded, classified as loan")
    b.instrument("IFRS", "C-I21", ca=400, ai=0, roles=[debtor("INSTTTNL_SCTR_S14")])
    b.case("I21", "IFRS", I, "C-I21", [], 400, 0, 0, "OI-17 literal: parent sector S14 matches no row")
    b.instrument("IFRS", "C-I22", ca=400, ai=0, roles=[debtor("INSTTTNL_SCTR_S126")])
    b.case("I22", "IFRS", I, "C-I22", ["R0110"], 400, 1, 0, "OI-15 decided: financial auxiliary S126 in R0110")
    b.instrument("IFRS", "C-I23", ca=1000, ai=0, prf=NP, roles=[debtor(S1311, mdb=MDB)])
    b.case("I23", "IFRS", I, "C-I23", ["R0090", "R0100"], 1000, 1, 1,
           "OI-16 literal: development bank on government sector counted twice")
    b.instrument("IFRS", "C-I24", prod="TYP_INSTRMNT_2", acc="ACCNTNG_CLSSFCTN_8", ca=100, ai=0)
    b.case("I24", "IFRS", I, "C-I24", [], 100, 0, 0, "equity instrument: type 1115")
    b.instrument("IFRS", "C-I25", ca=5000, ai=0, roles=[debtor(S11)], ctx={**CTX["IFRS"], "DT_RFRNC": "2026-03-31"})
    b.case("I25", "IFRS", I, "C-I25", [], None, 0, 0, "other reporting date: not in snapshot")
    b.instrument("IFRS", "C-I26", ca=5000, ai=0, roles=[debtor(S11)], ctx={**CTX["IFRS"], "RPRTNG_AGNT_ID": "RA009"})
    b.case("I26", "IFRS", I, "C-I26", [], None, 0, 0, "other reporting agent: not in snapshot")
    # ---- IFRS context: securities --------------------------------------------------------------------------------
    b.security("IFRS", "C-S01", ca=2000, ai=40, issuer=(True, S11, None))
    b.case("S01", "IFRS", S, "C-S01", ["R0120"], 2040, 1, 0, "non-negotiable debt security, performing")
    b.security("IFRS", "C-S02", dbt="SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20", ca=1500, ai=500, issuer=(True, S125A, None))
    b.case("S02", "IFRS", S, "C-S02", ["R0110"], 2000, 1, 1, "non-negotiable debt security, non-performing")
    b.security("IFRS", "C-S03", ngtbl="NGTBL_SCRTY_1", ca=1000, ai=0, issuer=(True, S11, None))
    b.case("S03", "IFRS", S, "C-S03", [], 1000, 0, 0, "negotiable debt security: type 1116")
    b.security("IFRS", "C-S04", hld="HLD_SL_INDCTR_1", ca=1000, ai=0, issuer=(True, S11, None))
    b.case("S04", "IFRS", S, "C-S04", [], 1000, 0, 0, "non-negotiable security held for sale: type 1118")
    b.security("IFRS", "C-S05", ca=1000, ai=0, issuer=(False, S11, None))
    b.case("S05", "IFRS", S, "C-S05", [], 1000, 0, 0, "issuer is not the primary issuer")
    # ---- national GAAP context --------------------------------------------------------------------------------
    b.instrument("NGAAP", "C-N01", acc="ACCNTNG_CLSSFCTN_76", ca=1000, ai=100, roles=[debtor(S11)])
    b.case("N01", "NGAAP", I, "C-N01", ["R0120"], 1100, 1, 0, "LOCOM portfolio, specific allowances")
    b.instrument("NGAAP", "C-N02", acc="ACCNTNG_CLSSFCTN_77", ca=500, ai=250, prf=NP, roles=[debtor(S11)])
    b.case("N02", "NGAAP", I, "C-N02", ["R0120"], 750, 1, 1, "cost-based portfolio, specific allowances, NPE")
    b.instrument("NGAAP", "C-N03", acc="ACCNTNG_CLSSFCTN_77", imp="CRDT_QLTY_211", ca=600, gc=30, gb=20,
                 roles=[debtor("INSTTTNL_SCTR_S1312")])
    b.case("N03", "NGAAP", I, "C-N03", ["R0090"], 650, 1, 0, "general allowances for credit risk")
    b.instrument("NGAAP", "C-N04", acc="ACCNTNG_CLSSFCTN_76", imp="CRDT_QLTY_212", ca=400, gc=10, gb=5, prf=NP,
                 roles=[debtor("INSTTTNL_SCTR_S14_B")])
    b.case("N04", "NGAAP", I, "C-N04", ["R0150"], 415, 1, 1, "general allowances for banking risk, NPE")
    b.instrument("NGAAP", "C-N05", acc="ACCNTNG_CLSSFCTN_74", ca=300, ai=60, prf=NP,
                 roles=[debtor("INSTTTNL_SCTR_S124")])
    b.case("N05", "NGAAP", I, "C-N05", ["R0110"], 360, 1, 1, "other non-trading portfolio, subject to impairment")
    b.instrument("NGAAP", "C-N06", acc="ACCNTNG_CLSSFCTN_74", imp="CRDT_QLTY_211", ca=200, gc=4, gb=1,
                 roles=[debtor(S11)])
    b.case("N06", "NGAAP", I, "C-N06", ["R0120"], 205, 1, 0, "portfolio 74, general allowances")
    b.instrument("NGAAP", "C-N07", acc="ACCNTNG_CLSSFCTN_74", sbjct="SBJCT_IMPRMNT_INDCTR_2", ca=200, ai=0,
                 roles=[debtor(S11)])
    b.case("N07", "NGAAP", I, "C-N07", ["R0120"], None, 0, 0, "portfolio 74 not subject to impairment: no amount")
    b.instrument("NGAAP", "C-N08", acc="ACCNTNG_CLSSFCTN_77", imp="CRDT_QLTY_23", ca=200, ai=10, roles=[debtor(S11)])
    b.case("N08", "NGAAP", I, "C-N08", ["R0120"], None, 0, 0, "impairment status without a branch: no amount")
    b.instrument("NGAAP", "C-N09", acc="ACCNTNG_CLSSFCTN_77", imp="CRDT_QLTY_211", ca=500, gc=25, gb=None,
                 roles=[debtor(S11)])
    b.case("N09", "NGAAP", I, "C-N09", ["R0120"], None, 0, 0, "OI-18 literal: one allowance null gives null amount")
    b.security("NGAAP", "C-N10", styp="SCRTY_EXCHNG_TRDBL_DRVTV_TYP_14", dbt="SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20",
               ca=1000, ai=0, issuer=(True, "INSTTTNL_SCTR_S122_A_2", None))
    b.case("N10", "NGAAP", S, "C-N10", ["R0100"], 1000, 1, 1, "non-negotiable covered bond, nGAAP, NPE")
    # ---- context whose reporting scheme is out of scope ----------------------------------------------------------
    b.instrument("SCHEME4", "C-X01", ca=1000, ai=0, prf=NP, roles=[debtor(S11)])
    b.case("X01", "SCHEME4", I, "C-X01", [], 1000, 0, 0, "reporting scheme 4 (data points): template not reported")


def random_positions(b, rng, n):
    sectors = [s for v in ROW_SECTORS.values() for s in v] + ["INSTTTNL_SCTR_S14"]
    amt = lambda lo, hi: Decimal(rng.randint(lo * 100, hi * 100)) / 100
    for ctx_name in ("IFRS", "NGAAP"):
        ifrs = ctx_name == "IFRS"
        for k in range(n):
            iid = f"R-{ctx_name}-I{k:04d}"
            prod, role, rpy = rng.choice([("TYP_INSTRMNT_1022", "ENTTY_RL_TYP_28", "RPYMNT_RGHTS_2"),
                                          ("TYP_INSTRMNT_51", "ENTTY_RL_TYP_28", "RPYMNT_RGHTS_2"),
                                          ("TYP_INSTRMNT_80", "ENTTY_RL_TYP_19", "RPYMNT_RGHTS_2"),
                                          ("TYP_INSTRMNT_522", "ENTTY_RL_TYP_27", rng.choice(["RPYMNT_RGHTS_1",
                                                                                              "RPYMNT_RGHTS_2"]))])
            roles = [(role, rng.random() > 0.05, rng.choice(sectors),
                      MDB if rng.random() < 0.05 else None)]
            if rng.random() < 0.1:
                roles.append((role, False, rng.choice(sectors), None))
            kw = dict(prod=prod, rpy=rpy, prf=NP if rng.random() < 0.15 else PF, ca=amt(0, 100000),
                      ai=None if rng.random() < 0.03 else amt(0, 5000), roles=roles)
            if ifrs:
                kw.update(acc=rng.choice(["ACCNTNG_CLSSFCTN_6"] * 9 + ["ACCNTNG_CLSSFCTN_8"]),
                          hld="HLD_SL_INDCTR_1" if rng.random() < 0.05 else "HLD_SL_INDCTR_2")
            else:
                imp = rng.choice(["CRDT_QLTY_26", "CRDT_QLTY_26", "CRDT_QLTY_211", "CRDT_QLTY_212", None])
                kw.update(acc=rng.choice(["ACCNTNG_CLSSFCTN_74", "ACCNTNG_CLSSFCTN_76", "ACCNTNG_CLSSFCTN_77"]),
                          sbjct=rng.choice(["SBJCT_IMPRMNT_INDCTR_1"] * 4 + ["SBJCT_IMPRMNT_INDCTR_2"]), imp=imp,
                          gc=None if rng.random() < 0.1 else amt(0, 1000),
                          gb=None if rng.random() < 0.1 else amt(0, 1000))
            b.instrument(ctx_name, iid, **kw)
        for k in range(n // 5):
            b.security(ctx_name, f"R-{ctx_name}-S{k:04d}",
                       styp=rng.choice(["SCRTY_EXCHNG_TRDBL_DRVTV_TYP_11", "SCRTY_EXCHNG_TRDBL_DRVTV_TYP_13",
                                        "SCRTY_EXCHNG_TRDBL_DRVTV_TYP_14", "SCRTY_EXCHNG_TRDBL_DRVTV_TYP_5"]),
                       ngtbl=rng.choice(["NGTBL_SCRTY_2", "NGTBL_SCRTY_2", "NGTBL_SCRTY_1"]),
                       dbt=rng.choice(["SCRTY_EXCHNG_TRDBL_DRVTV_TYP_19"] * 4 + ["SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20"]),
                       ca=amt(0, 50000), ai=amt(0, 2000),
                       issuer=(rng.random() > 0.1, rng.choice(sectors), None))


def generate(out, seed=42, n_random=100):
    b = Book()
    edge_cases(b)
    random_positions(b, random.Random(seed), n_random)
    for name, ctx in CTX.items():
        b.add("INTRNL_GRP_RL_IL", {**ctx, "GRP_ID": f"GRP-{ctx['RPRTNG_AGNT_ID']}", "GRP_RL_TYP": "GRP_RL_TYP_1",
                                   "FNRP_RPRTNG_SCHM": SCHEME[name]})
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for table, rows in b.t.items():
        pd.DataFrame(rows).to_csv(out / f"{table}.csv", index=False)
    pd.DataFrame([{"name": k, **v} for k, v in CTX.items()]).to_csv(out / "contexts.csv", index=False)
    pd.DataFrame(b.cases).to_csv(out / "expected_cases.csv", index=False)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default=str(ROOT / "data" / "synthetic"))
    ap.add_argument("--random", type=int, default=100, help="random instrument positions per context")
    a = ap.parse_args()
    print("written to", generate(a.out, a.seed, a.random))
