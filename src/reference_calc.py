"""
Independent pandas/Python calculation of F 18.00.a R0070 C0010, C0060 and the NPL ratio.

Built from the spec (specs/npl_ratio_lineage_spec_v0.2.yaml) and the input CSVs only. It never reads sql/.
Constants come from the spec where it structures them (cell filters, products and roles, sector-row member
lists, reporting schemes); the remaining conditions are coded from the spec's logic text.

Only the in-scope logic is implemented: positions outside the R0070 portfolios get no gross carrying amount here
(spec T03: "else no value"), which cannot change the cells.

SQL null semantics are reproduced: a comparison with a missing value is false.

    python src/reference_calc.py [--data data/synthetic]
"""
import argparse
import re
from decimal import Decimal
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "npl_ratio_lineage_spec_v0.2.yaml"
CTX_KEYS = ["DT_RFRNC", "RPRTNG_AGNT_ID", "ACCNTNG_CNSLDTN_LVL", "ACCNTNG_STNDRD"]
AMOUNTS = {"CRRYNG_AMNT", "ACCMLTD_IMPRMNT", "FV", "ACCMLTD_CHNGS_FV_CR", "GNRL_ALLWNCS_CRDT_RSK",
           "GNRL_ALLWNCS_BNK_RSK"}
ROWS = ["R0080", "R0090", "R0100", "R0110", "R0120", "R0150"]


# ---------- spec constants ----------
def spec_constants(spec_path=SPEC):
    s = yaml.safe_load(open(spec_path, encoding="utf-8"))
    num, den = s["kri"]["numerator"], s["kri"]["denominator"]
    f = {x["variable"]: x for x in num["filters"]}
    T = {t["id"]: t for t in s["transformations"]}
    la = T["T04"]["logic"]["loans_and_advances_branch"]["product_and_role"]
    c = {
        "portfolios": {m["member"] for m in f["ACCNTNG_CLSSFCTN"]["leaf_members"]},
        "loans_and_advances": f["TYP_FNNCL_ASST_INSTRMNT_ANNX_V"]["member"],
        "non_performing": f["PRFRMNG_STTS"]["member"],
        "product_role": [(set(p["products"]), p["role"].split()[0], p["main_flag"]) for p in la],
        "schemes": set(re.findall(r"FNRP_RPRTNG_SCHM_\d+", T["T06"]["logic"]["official_algorithm"])),
        "rows": {},
    }
    assert {x["variable"] for x in den["filters"]} == {"ACCNTNG_CLSSFCTN", "TYP_FNNCL_ASST_INSTRMNT_ANNX_V"}
    for r, text in T["T07"]["logic"]["official_algorithms"].items():
        where = text.split("where", 1)[1]
        c["rows"][r] = {"sectors": set(re.findall(r"INSTTTNL_SCTR_\w+", where)),
                        "mdb": "MLTLTRL_DVLPMNT_BNK_INDCTR_1" in where}
    return c


# ---------- helpers: SQL three-valued comparisons ----------
def eq(x, v):
    return x is not None and x == v


def isin(x, vs):
    return x is not None and x in vs


def notin(x, vs):
    return x is not None and x not in vs


def add(*xs):
    return None if any(x is None for x in xs) else sum(xs, Decimal(0))


# ---------- data ----------
def load(data_dir):
    out = {}
    for f in Path(data_dir).glob("*_IL.csv"):
        df = pd.read_csv(f, dtype=str, keep_default_na=False)
        recs = []
        for r in df.to_dict("records"):
            recs.append({k: (None if v == "" else Decimal(v) if k in AMOUNTS else v) for k, v in r.items()})
        out[f.stem] = recs
    return out


def snapshot(data, table, ctx):
    return [r for r in data.get(table, []) if all(r[k] == ctx[k] for k in CTX_KEYS)]


# ---------- derivations from the spec ----------
def gross_carrying_amount(r, c):
    """Spec T03 in_scope_branches_for_R0070 (also used for security positions, T05: 'mirrors T03')."""
    acc, imp, sbj = r["ACCNTNG_CLSSFCTN"], r["IMPRMNT_STTS"], r["SBJCT_IMPRMNT_INDCTR"]
    if acc not in c["portfolios"]:
        return None
    ca, ai = r["CRRYNG_AMNT"], r["ACCMLTD_IMPRMNT"]
    specific = (eq(acc, "ACCNTNG_CLSSFCTN_6")
                or (isin(acc, {"ACCNTNG_CLSSFCTN_76", "ACCNTNG_CLSSFCTN_77"}) and eq(imp, "CRDT_QLTY_26"))
                or (eq(acc, "ACCNTNG_CLSSFCTN_74") and eq(sbj, "SBJCT_IMPRMNT_INDCTR_1") and eq(imp, "CRDT_QLTY_26")))
    if specific and ca is not None and ai is not None:
        return ca + ai
    general = ((isin(acc, {"ACCNTNG_CLSSFCTN_76", "ACCNTNG_CLSSFCTN_77"})
                and isin(imp, {"CRDT_QLTY_211", "CRDT_QLTY_212"}))
               or (eq(acc, "ACCNTNG_CLSSFCTN_74") and eq(sbj, "SBJCT_IMPRMNT_INDCTR_1")
                   and isin(imp, {"CRDT_QLTY_211", "CRDT_QLTY_212"})))
    gc, gb = r["GNRL_ALLWNCS_CRDT_RSK"], r["GNRL_ALLWNCS_BNK_RSK"]
    if general and ca is not None and (gc is not None or gb is not None):
        return add(ca, gc, gb)
    return None


def instrument_is_loan(rl, instr, assignments, parties, c):
    """Spec T04 loans_and_advances_branch: product and role with its main flag, sector condition, result."""
    if not (eq(rl["INSTRMNT_RL_TYP"], "ABSTRCT_INSTRMNT_RL_TYP_34")
            or (eq(rl["INSTRMNT_RL_TYP"], "ABSTRCT_INSTRMNT_RL_TYP_35") and eq(rl["HLD_SL_INDCTR"], "HLD_SL_INDCTR_2"))):
        return False
    for a in assignments:
        sector = parties.get(a["PRTY_ID"], {}).get("INSTTTNL_SCTR")
        for products, role, flag in c["product_role"]:
            var = flag.rsplit("_", 1)[0]
            if isin(instr["INSTRMNT_TYP_PRDCT"], products) and eq(a["ENTTY_RL_TYP"], role) and eq(a.get(var), flag):
                cb = {"INSTTTNL_SCTR_S121", "INSTTTNL_SCTR_S122_A"}
                if notin(sector, cb) or (isin(sector, cb) and eq(instr["RPYMNT_RGHTS"], "RPYMNT_RGHTS_2")):
                    return True
    return False


def security_is_loan(pos, sec, long_pos):
    """Spec T05: debt securities (types 11, 13, 14, 5) that are non-negotiable, long nGAAP or IFRS not held for sale."""
    if not (isin(sec["SCRTY_EXCHNG_TRDBL_DRVTV_TYP"], {f"SCRTY_EXCHNG_TRDBL_DRVTV_TYP_{i}" for i in (11, 13, 14, 5)})
            and eq(sec["NGTBL_SCRTY_INDCTR"], "NGTBL_SCRTY_2")):
        return False
    t = pos["LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP"]
    return eq(t, "LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_4") or (
        eq(t, "LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP_3") and eq((long_pos or {}).get("HLD_SL_INDCTR"), "HLD_SL_INDCTR_2"))


def debtor_role(d):
    """Spec T07 debtor_role."""
    role = d.get("ENTTY_RL_TYP")
    return ((isin(role, {"ENTTY_RL_TYP_20", "ENTTY_RL_TYP_28"}) and eq(d.get("MN_DBTR_INDCTR"), "MN_DBTR_INDCTR_1"))
            or (eq(role, "ENTTY_RL_TYP_27") and eq(d.get("MN_DPST_TKNG_CRPRTN_INDCTR"), "MN_DPST_TKNG_CRPRTN_INDCTR_1"))
            or (eq(role, "ENTTY_RL_TYP_19") and eq(d.get("MN_LSS_INDCTR"), "MN_LSS_INDCTR_1"))
            or (eq(role, "ENTTY_RL_TYP_8") and eq(d.get("PRMRY_ISSR_INDCTR"), "PRMRY_ISSR_INDCTR_1")))


def sector_rows(d, c):
    """Spec T07 rows, sector member lists read from the official row algorithms."""
    if not (d["loan"] and isin(d["ACCNTNG_CLSSFCTN"], c["portfolios"]) and debtor_role(d)):
        return []
    out = []
    for r in ROWS:
        rule = c["rows"][r]
        if isin(d.get("INSTTTNL_SCTR"), rule["sectors"]) or (
                rule["mdb"] and eq(d.get("MLTLTRL_DVLPMNT_BNK_INDCTR"), "MLTLTRL_DVLPMNT_BNK_INDCTR_1")):
            out.append(r)
    return out


# ---------- R0070 ----------
def r0070(data, ctx, c=None):
    """Records of row 0070: one per (position, sector row), with gross carrying amount and non-performing flag."""
    c = c or spec_constants()
    in_scope = any(eq(g["GRP_RL_TYP"], "GRP_RL_TYP_1") and isin(g["FNRP_RPRTNG_SCHM"], c["schemes"])
                   for g in snapshot(data, "INTRNL_GRP_RL_IL", ctx))
    if not in_scope:
        return []
    parties = {p["PRTY_ID"]: p for p in snapshot(data, "PRTY_IL", ctx)}
    out = []
    # instrument positions
    instr = {i["INSTRMNT_ID"]: i for i in snapshot(data, "INSTRMNT_IL", ctx)}
    assg = {}
    for a in snapshot(data, "INSTRMNT_ENTTY_RL_ASSGNMNT_IL", ctx):
        assg.setdefault(a["INSTRMNT_ID"], []).append(a)
    for rl in snapshot(data, "INSTRMNT_RL_IL", ctx):
        iid = rl["INSTRMNT_ID"]
        a_list = assg.get(iid, [])
        loan = instrument_is_loan(rl, instr[iid], a_list, parties, c)
        gca = gross_carrying_amount(rl, c)
        for a in a_list or [{}]:
            d = {**a, **parties.get(a.get("PRTY_ID"), {}), "ACCNTNG_CLSSFCTN": rl["ACCNTNG_CLSSFCTN"], "loan": loan}
            for r in sector_rows(d, c):
                out.append({"PSTN_SRC": "INSTRMNT", "PSTN_ID": iid, "RW": r, "GRSS_CRRYNG_AMNT": gca,
                            "NP": eq(rl["PRFRMNG_STTS"], c["non_performing"])})
    # security positions
    secs = {s["SCRTY_EXCHNG_TRDBL_DRVTV_ID"]: s for s in snapshot(data, "SCRTY_EXCHNG_TRDBL_DRVTV_IL", ctx)}
    pkey = ["SCRTY_ID", "INVSTR_PRTY_ID", "INVSTR_ENTTY_RL_TYP", "SCRTY_PSTN_BLNC_SHT_RCGNSD_TYP",
            "LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP"]
    longs = {tuple(p[k] for k in pkey): p for p in snapshot(data, "LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL", ctx)}
    issuers = {}
    for e in snapshot(data, "SCRTY_ENTTY_RL_ASSGNMNT_IL", ctx):
        issuers.setdefault(e["SCRTY_EXCHNG_TRDBL_DRVTV_ID"], []).append(e)
    for pos in snapshot(data, "LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL", ctx):
        sec = secs.get(pos["SCRTY_ID"])
        if sec is None:
            continue
        loan = security_is_loan(pos, sec, longs.get(tuple(pos[k] for k in pkey)))
        gca = gross_carrying_amount(pos, c)
        for e in issuers.get(pos["SCRTY_ID"], []) or [{}]:
            d = {**e, **parties.get(e.get("PRTY_ID"), {}), "ACCNTNG_CLSSFCTN": pos["ACCNTNG_CLSSFCTN"], "loan": loan}
            for r in sector_rows(d, c):
                out.append({"PSTN_SRC": "SCRTY_PSTN", "PSTN_ID": pos["SCRTY_ID"], "RW": r, "GRSS_CRRYNG_AMNT": gca,
                            "NP": eq(sec["DBT_SCRTY_PRFRMNG_STTS_TYP"], "SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20")})
    return out


def cells(records):
    pos = [r for r in records if r["GRSS_CRRYNG_AMNT"] is not None and r["GRSS_CRRYNG_AMNT"] > 0]
    c0010 = sum((r["GRSS_CRRYNG_AMNT"] for r in pos), Decimal(0)) if pos else None
    npl = [r for r in pos if r["NP"]]
    c0060 = sum((r["GRSS_CRRYNG_AMNT"] for r in npl), Decimal(0)) if npl else None
    ratio = None if c0060 is None or not c0010 else (c0060 / c0010).quantize(Decimal("1e-12"))
    return {"C0010": c0010, "C0060": c0060, "NPL_RATIO": ratio}


def run(data_dir):
    data, c = load(data_dir), spec_constants()
    ctxs = pd.read_csv(Path(data_dir) / "contexts.csv", dtype=str).to_dict("records")
    return {ctx["name"]: cells(r0070(data, ctx, c)) for ctx in ctxs}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "data" / "synthetic"))
    a = ap.parse_args()
    for name, x in run(a.data).items():
        print(f"{name:10s} C0010={x['C0010']}  C0060={x['C0060']}  NPL_RATIO={x['NPL_RATIO']}")
