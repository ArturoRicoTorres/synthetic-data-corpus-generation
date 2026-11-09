"""
Build canonical lineage spec v0.2 for the NPL ratio KRI from the OFFICIAL ECB BIRD metadata export
(data/raw/entities-*.zip, downloaded from bird.ecb.europa.eu), and diff it against
v0.1, which was built from the community repo regcommunity/FreeBIRD_EIL_67.

Provenance tags:
  bird_official   - read from the official export by this script (algorithm text is verbatim)
  gap_fill        - added by hand; the official export does not specify it
"""
import hashlib
import zipfile
from pathlib import Path
import re
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
ZIP = Path(sorted(RAW.glob("entities-*.zip"))[-1])       # official export from bird.ecb.europa.eu
SRC = str(RAW / "bird_official") + "/"                    # extracted on first run (git-ignored)
V01 = ROOT / "specs" / "npl_ratio_lineage_spec_v0.1.yaml"
OUT = ROOT / "specs" / "npl_ratio_lineage_spec_v0.2.yaml"

if not (RAW / "bird_official" / "cube.csv").exists():
    with zipfile.ZipFile(ZIP) as z:
        for name in z.namelist():                        # flat CSV export; refuse anything with a path
            if "/" in name or "\\" in name or name.startswith("."):
                raise SystemExit(f"unexpected entry in export: {name}")
        z.extractall(RAW / "bird_official")
NUM, DEN = "F_18.00.a_R0070_C0060_OL", "F_18.00.a_R0070_C0010_OL"
SECTOR_ROWS = ["R0080", "R0090", "R0100", "R0110", "R0120", "R0150"]

def rd(f):
    return pd.read_csv(SRC + f, dtype=str, encoding="utf-8-sig")

zip_sha = hashlib.sha256(open(ZIP, "rb").read()).hexdigest()
cube = rd("cube.csv").set_index("CUBE_ID")
csi = rd("cube_structure_item.csv")
cl = rd("cube_link.csv")
csil = rd("cube_structure_item_link.csv")
ltr = rd("logical_transformation_rule.csv").set_index("LOGICAL_TRANSFORMATION_RULE_ID")
ro = rd("routine.csv").set_index("ROUTINE_ID")
var = rd("variable.csv").drop_duplicates("VARIABLE_ID").set_index("VARIABLE_ID")
mem = rd("member.csv").drop_duplicates("MEMBER_ID").set_index("MEMBER_ID")
dom = rd("domain.csv").drop_duplicates("DOMAIN_ID").set_index("DOMAIN_ID")
mhn = rd("member_hierarchy_node.csv")
cr = rd("cube_relationship.csv")
csr = rd("cube_structure_item_relationship.csv")
fw = rd("framework_version.csv")
lr = rd("legal_reference.csv")
lt = rd("legal_text.csv").set_index("LEGAL_TEXT_ID")

def alg(rid):
    return ro.loc[rid, "ALGORITHM"].replace("\r\n", "\n").replace("\r", "\n").strip()

def mname(m):
    return mem.NAME.get(m, None)

# ---------- identifier validation of official algorithms ----------
KNOWN = set(var.index) | set(mem.index) | set(cube.index) | set(ro.index)
SQL = {"SELECT", "WHERE", "AND", "OR", "IN", "NOT", "SET", "UPDATE", "CASE", "WHEN", "THEN", "ELSE", "END",
       "NULL", "SUM", "CUBES", "EIL", "CUBE", "DATAPOINTCUBE", "IFRS", "GAAP", "LOCOM", "ANNEX", "OTC"}

def unknown_identifiers(text):
    code = "\n".join(l.split("--")[0] for l in text.split("\n"))  # drop comments
    toks = set(re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", code))
    return sorted(t for t in toks if t not in KNOWN and t.upper() not in SQL and not re.fullmatch(r"R\d{4}", t))

# ---------- cells ----------
def cell(cid):
    s = csi[csi.CUBE_ID == cid]
    filters = []
    for r in s.itertuples():
        if r.ROLE_TYPE == "O":
            continue
        f = {"variable": r.VARIABLE_ID, "member": r.MEMBER_ID, "label": mname(r.MEMBER_ID)}
        kids = mhn[mhn.PARENT_MEMBER_ID == r.MEMBER_ID].MEMBER_ID.unique().tolist()
        if kids:
            f["leaf_members"] = [{"member": k, "label": mname(k)} for k in sorted(kids)]
        filters.append(f)
    rule = cl[cl.DESTINATION_CUBE_ID == cid].LOGICAL_TRANSFORMATION_RULE_ID.iloc[0]
    links = cl[cl.DESTINATION_CUBE_ID == cid].CUBE_LINK_ID
    att = csil[csil.CUBE_LINK_ID.isin(links)]
    return {
        "bird_cube_id": cid,
        "description": cube.loc[cid, "DESCRIPTION"],
        "metric": s[s.ROLE_TYPE == "O"].VARIABLE_ID.tolist(),
        "filters": filters,
        "transformation_rule": rule,
        "routine_chain": ltr.loc[rule, "ALGORITHM"].split(";"),
        "source_cubes": sorted(cl[cl.DESTINATION_CUBE_ID == cid].SOURCE_CUBE_ID.tolist()),
        "attribute_links": [{"source": a.SOURCE_CUBE_STRUCTURE_ITEM_ID,
                             "target": a.DESTINATION_CUBE_STRUCTURE_ITEM_ID.split("__")[1],
                             "routine": a.ROUTINE_ID} for a in att.itertuples()],
        "provenance": "bird_official",
    }

numerator, denominator = cell(NUM), cell(DEN)

# sector-row lineage (R0070 is the sum of these rows)
def sector_links(row):
    cid = f"F_18.00.a_{row}_C0010_OL"
    links = cl[cl.DESTINATION_CUBE_ID == cid].CUBE_LINK_ID
    return sorted({a.SOURCE_CUBE_STRUCTURE_ITEM_ID for a in csil[csil.CUBE_LINK_ID.isin(links)].itertuples()})

sector_sources = sorted(set().union(*[sector_links(r) for r in SECTOR_ROWS]))
r0070_sources = sorted({a["source"] for a in denominator["attribute_links"]})
missing_at_total = sorted(set(sector_sources) - set(r0070_sources))

# ---------- IL -> EIL attribute lineage ----------
def eil_lineage(eil_cube, v):
    links = cl[cl.DESTINATION_CUBE_ID == eil_cube].CUBE_LINK_ID
    s = csil[csil.CUBE_LINK_ID.isin(links) & (csil.DESTINATION_CUBE_STRUCTURE_ITEM_ID == f"{eil_cube}__{v}")]
    return sorted(s.SOURCE_CUBE_STRUCTURE_ITEM_ID.tolist()), sorted(s.ROUTINE_ID.unique().tolist())

# ---------- attributes (Collibra seed) ----------
used_vars = {
    "INSTRMNT_IL": ["INSTRMNT_TYP_PRDCT", "RPYMNT_RGHTS"],
    "INSTRMNT_RL_IL": ["INSTRMNT_RL_TYP", "ACCNTNG_CLSSFCTN", "HLD_SL_INDCTR", "SBJCT_IMPRMNT_INDCTR", "IMPRMNT_STTS",
                       "PRFRMNG_STTS", "CRRYNG_AMNT", "ACCMLTD_IMPRMNT", "FV", "ACCMLTD_CHNGS_FV_CR",
                       "GNRL_ALLWNCS_CRDT_RSK", "GNRL_ALLWNCS_BNK_RSK"],
    "INSTRMNT_ENTTY_RL_ASSGNMNT_IL": ["ENTTY_RL_TYP", "MN_DBTR_INDCTR", "MN_LSS_INDCTR", "MN_DPST_TKNG_CRPRTN_INDCTR",
                                      "PRTY_ID"],
    "PRTY_IL": ["INSTTTNL_SCTR", "MLTLTRL_DVLPMNT_BNK_INDCTR"],
    "INTRNL_GRP_RL_IL": ["FNRP_RPRTNG_SCHM", "GRP_ID", "GRP_RL_TYP"],      # GRP_RL_TYP filters the gate (OI-13)
    "OTC_DRVTV_HDG_IL": ["ACCNTNG_HDG_INDCTR"],
    # securities path (T05, T07, T10)
    "SCRTY_EXCHNG_TRDBL_DRVTV_IL": ["SCRTY_EXCHNG_TRDBL_DRVTV_TYP", "NGTBL_SCRTY_INDCTR", "DBT_SCRTY_PRFRMNG_STTS_TYP"],
    "LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL": [
        "LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_TYP", "ACCNTNG_CLSSFCTN", "SBJCT_IMPRMNT_INDCTR", "IMPRMNT_STTS",
        "CRRYNG_AMNT", "ACCMLTD_IMPRMNT", "FV", "ACCMLTD_CHNGS_FV_CR", "GNRL_ALLWNCS_CRDT_RSK", "GNRL_ALLWNCS_BNK_RSK"],
    "LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL": ["HLD_SL_INDCTR"],
    "SCRTY_ENTTY_RL_ASSGNMNT_IL": ["ENTTY_RL_TYP", "PRMRY_ISSR_INDCTR", "PRTY_ID"],
}
attributes = []
for t, vs in used_vars.items():
    s = csi[csi.CUBE_ID == t].set_index("VARIABLE_ID")
    for v in vs:
        d = var.loc[v] if v in var.index else None
        attributes.append({
            "id": f"{t}.{v}", "table": t, "column": v,
            "present_in_official_il": v in s.index,
            "mandatory": (s.loc[v, "IS_MANDATORY"] == "true") if v in s.index else None,
            "business_name": None if d is None else d.NAME,
            "business_definition": None if d is None else str(d.DESCRIPTION).strip(),
            "domain": None if d is None else dom.NAME.get(d.DOMAIN_ID, d.DOMAIN_ID),
            "legal_refs": [lt.loc[x.LEGAL_TEXT_ID, "LEGAL_CODE"] for x in
                           lr[(lr.OBJECT_TYPE == "VARIABLE") & (lr.OBJECT_ID == v)].itertuples()],
            "provenance": "bird_official",
        })
for v in ["GRSS_CRRYNG_AMNT", "TYP_FNNCL_ASST_INSTRMNT_ANNX_V", "DBT_SCRTY_PRFRMNG_STTS_TYP"]:
    d = var.loc[v]
    attributes.append({"id": f"derived.{v}", "table": "(EIL, derived)", "column": v, "business_name": d.NAME,
                       "business_definition": str(d.DESCRIPTION).strip(),
                       "domain": dom.NAME.get(d.DOMAIN_ID, d.DOMAIN_ID), "provenance": "bird_official"})

# ---------- joins ----------
def rel_keys(p, f, contains):
    x = cr[(cr.PRIMARY_CUBE_ID == p) & (cr.FOREIGN_CUBE_ID == f) & cr.CUBE_RELATIONSHIP_ID.str.contains(contains)]
    out = []
    for r in x.itertuples():
        k = csr[csr.CUBE_RELATIONSHIP_ID == r.CUBE_RELATIONSHIP_ID]
        j = {"relationship": r.CUBE_RELATIONSHIP_ID, "parent": p, "child": f,
             "cardinality": f"{r.PRIMARY_CUBE_CARDINALITY}:{r.FOREIGN_CUBE_CARDINALITY}",
             "keys": sorted(k.PRIMARY_CUBE_STRUCTURE_ITEM_CODE.tolist())}
        renamed = {a: b for a, b in zip(k.PRIMARY_CUBE_STRUCTURE_ITEM_CODE, k.FOREIGN_CUBE_STRUCTURE_ITEM_CODE) if a != b}
        if renamed:                                       # parent key -> child column, where the names differ
            j["key_map"] = dict(sorted(renamed.items()))
        j["provenance"] = "bird_official"
        out.append(j)
    return out

joins = (rel_keys("INSTRMNT_IL", "INSTRMNT_RL_IL", "")
         + rel_keys("INSTRMNT_IL", "INSTRMNT_ENTTY_RL_ASSGNMNT_IL", "OTHR_LN_DBTR|FNNCL_LS_LSS_|DPST_PRVDD")
         + rel_keys("ENTTY_RL_IL", "INSTRMNT_ENTTY_RL_ASSGNMNT_IL", "OTHR_LN_S_OTHR_LN|LSS_LSS|DPST_TKNG_CRPRTN_PRVDS")
         + rel_keys("PRTY_IL", "ENTTY_RL_IL", "ASS_PRTY_ACTS_PRTY_RL_")
         + rel_keys("INSTRMNT_IL", "OTC_DRVTV_HDG_IL", "")
         # securities path: security -> position chain -> accounting-classification assignment, and issuer role
         + rel_keys("SCRTY_EXCHNG_TRDBL_DRVTV_IL", "SCRTY_PSTN_IL", "")
         + rel_keys("SCRTY_PSTN_IL", "BLNC_SHT_RCGNSD_NN_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL", "")
         + rel_keys("BLNC_SHT_RCGNSD_NN_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL", "LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL", "")
         + rel_keys("LNG_SHRT_BLNC_SHT_RCGNSD_SCRTY_PSTN_IL", "LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ASSGNMNT_IL", "")
         + rel_keys("LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ASSGNMNT_IL",
                    "LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL", "")
         + rel_keys("SCRTY_EXCHNG_TRDBL_DRVTV_IL", "SCRTY_ENTTY_RL_ASSGNMNT_IL", "_ISSD_ISSR_")
         + rel_keys("ENTTY_RL_IL", "SCRTY_ENTTY_RL_ASSGNMNT_IL", "ASS_ISSR_ISSS_"))
joins.append({"relationship": "context-key join to INTRNL_GRP_RL_IL", "parent": "INTRNL_GRP_RL_IL",
              "child": "(all positions)", "keys": ["ACCNTNG_CNSLDTN_LVL", "ACCNTNG_STNDRD", "DT_RFRNC", "RPRTNG_AGNT_ID"],
              "provenance": "gap_fill", "open_issue": "OI-13"})

# ---------- transformations ----------
lin_gca = eil_lineage("INSTRMNT_RL_EIL", "GRSS_CRRYNG_AMNT")
lin_typ = eil_lineage("INSTRMNT_RL_EIL", "TYP_FNNCL_ASST_INSTRMNT_ANNX_V")
lin_ps = eil_lineage("INSTRMNT_RL_EIL", "PRFRMNG_STTS")
used_routines = ["R_DER_GRSS_CRRYNG_AMNT_3", "R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_2", "R_DER_GRSS_CRRYNG_AMNT_1",
                 "R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_3", "R_F_18.00.a_ALL", "R_F_18.00.a_R0070",
                 "R_F_18.00.a_C0010", "R_F_18.00.a_C0060"] + [f"R_F_18.00.a_{r}" for r in SECTOR_ROWS]

T = []
def node(**kw):
    for k in ("inputs", "outputs"):
        kw[k] = [x.replace("__", ".") for x in kw[k]]
    T.append(kw)

node(id="T01", name="Load input layer for reporting date", layer="source",
     inputs=["INSTRMNT_IL", "INSTRMNT_RL_IL", "INSTRMNT_ENTTY_RL_ASSGNMNT_IL", "PRTY_IL", "INTRNL_GRP_RL_IL",
             "OTC_DRVTV_HDG_IL", "SCRTY_EXCHNG_TRDBL_DRVTV_IL",
             "LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL"],
     outputs=["*_IL snapshot"], logic={"type": "select", "filter": "context key = (:dt_rfrnc, :rprtng_agnt_id, "
                                                                  ":accntng_cnsldtn_lvl, :accntng_stndrd)"},
     business_group="SOURCE_ACQUISITION", provenance="gap_fill")
node(id="T02", name="Carry status and classification attributes into the enriched layer", layer="enrichment",
     inputs=lin_ps[0] + ["INSTRMNT_RL_IL.ACCNTNG_CLSSFCTN", "PRTY_IL.INSTTTNL_SCTR",
                         "INSTRMNT_ENTTY_RL_ASSGNMNT_IL.ENTTY_RL_TYP", "INTRNL_GRP_RL_IL.FNRP_RPRTNG_SCHM"],
     outputs=["*_EIL (same attributes)"], logic={"type": "identity", "routine": "R_IDT_DER"},
     business_group="TECHNICAL", provenance="bird_official")
node(id="T03", name="Derive gross carrying amount (loans)", layer="enrichment",
     inputs=lin_gca[0], outputs=["INSTRMNT_RL_EIL.GRSS_CRRYNG_AMNT"], routine=lin_gca[1],
     logic={"type": "case", "in_scope_branches_for_R0070": [
         {"when": "ACCNTNG_CLSSFCTN in (6, 8)", "then": "CRRYNG_AMNT + ACCMLTD_IMPRMNT",
          "requires": "CRRYNG_AMNT and ACCMLTD_IMPRMNT not null"},
         {"when": "ACCNTNG_CLSSFCTN in (76, 77, 44) and IMPRMNT_STTS = CRDT_QLTY_26", "then": "CRRYNG_AMNT + ACCMLTD_IMPRMNT"},
         {"when": "ACCNTNG_CLSSFCTN in (9, 73, 74) and SBJCT_IMPRMNT_INDCTR = 1 and IMPRMNT_STTS = CRDT_QLTY_26",
          "then": "CRRYNG_AMNT + ACCMLTD_IMPRMNT"},
         {"when": "ACCNTNG_CLSSFCTN in (76, 77, 44) and IMPRMNT_STTS in (CRDT_QLTY_211, CRDT_QLTY_212)",
          "then": "CRRYNG_AMNT + GNRL_ALLWNCS_CRDT_RSK + GNRL_ALLWNCS_BNK_RSK"},
         {"when": "ACCNTNG_CLSSFCTN in (9, 73, 74) and SBJCT_IMPRMNT_INDCTR = 1 and IMPRMNT_STTS in (CRDT_QLTY_211, CRDT_QLTY_212)",
          "then": "CRRYNG_AMNT + GNRL_ALLWNCS_CRDT_RSK + GNRL_ALLWNCS_BNK_RSK"},
         {"else": "no value (fair-value branches exist but are outside ACCNTNG_CLSSFCTN_531)"}],
            "official_algorithm": alg("R_DER_GRSS_CRRYNG_AMNT_3")},
     business_group="MEASUREMENT", provenance="bird_official", open_issues=["OI-11", "OI-12"])
node(id="T04", name="Classify instrument per Annex V (loans and advances)", layer="enrichment",
     inputs=lin_typ[0], outputs=["INSTRMNT_RL_EIL.TYP_FNNCL_ASST_INSTRMNT_ANNX_V"], routine=lin_typ[1],
     logic={"type": "case", "loans_and_advances_branch": {
         "product_and_role": [
             {"products": ["TYP_INSTRMNT_1020", "TYP_INSTRMNT_1022", "TYP_INSTRMNT_1023", "TYP_INSTRMNT_120",
                           "TYP_INSTRMNT_130", "TYP_INSTRMNT_140", "TYP_INSTRMNT_162", "TYP_INSTRMNT_163",
                           "TYP_INSTRMNT_51"], "role": "ENTTY_RL_TYP_28 (loan debtor)", "main_flag": "MN_DBTR_INDCTR_1"},
             {"products": ["TYP_INSTRMNT_80"], "role": "ENTTY_RL_TYP_19 (lessee)", "main_flag": "MN_LSS_INDCTR_1"},
             {"products": ["TYP_INSTRMNT_511", "TYP_INSTRMNT_512", "TYP_INSTRMNT_522", "TYP_INSTRMNT_1202"],
              "role": "ENTTY_RL_TYP_27 (deposit-taking corporation)", "main_flag": "MN_DPST_TKNG_CRPRTN_INDCTR_1"}],
         "sector_condition": "INSTTTNL_SCTR not in (S121, S122_A), or it is and RPYMNT_RGHTS = RPYMNT_RGHTS_2",
         "result": "TYP_INSTRMNT_1117 if nGAAP balance-sheet asset, or IFRS and not held for sale; "
                   "TYP_INSTRMNT_1118 if IFRS and held for sale"},
            "official_algorithm": alg("R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_2")},
     business_group="PRODUCT_SEGMENTATION", provenance="bird_official", open_issues=["OI-12"])
node(id="T05", name="Securities branch: non-negotiable debt securities as loans and advances", layer="enrichment",
     inputs=["SCRTY_EXCHNG_TRDBL_DRVTV_IL", "LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_IL"],
     outputs=["LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_EIL.GRSS_CRRYNG_AMNT",
              "LNG_BLNC_SHT_RCGNSD_SCRTY_PSTN_PRDNTL_PRTFL_ACCNTNG_CLSSFCTN_ASSGNMNT_EIL.TYP_FNNCL_ASST_INSTRMNT_ANNX_V",
              "SCRTY_EXCHNG_TRDBL_DRVTV_EIL.DBT_SCRTY_PRFRMNG_STTS_TYP"],
     routine=["R_DER_GRSS_CRRYNG_AMNT_1", "R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_3"],
     logic={"type": "case", "summary": "debt securities (types 11, 13, 14, 5) with NGTBL_SCRTY_INDCTR = NGTBL_SCRTY_2 "
                                       "are classified TYP_INSTRMNT_1117; gross carrying amount mirrors T03",
            "official_algorithm_gca": alg("R_DER_GRSS_CRRYNG_AMNT_1"),
            "official_algorithm_type": alg("R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_3")},
     business_group="PRODUCT_SEGMENTATION", provenance="bird_official")
node(id="T06", name="Gate on FINREP reporting scheme", layer="reporting",
     inputs=["INTRNL_GRP_RL_EIL.FNRP_RPRTNG_SCHM"], outputs=["F_18.00.a scope"],
     logic={"type": "filter", "routine": "R_F_18.00.a_ALL", "official_algorithm": alg("R_F_18.00.a_ALL"),
            "meaning": "full, simplified or over-simplified FINREP reporters"},
     business_group="REGULATORY_SCOPE", provenance="bird_official", open_issues=["OI-13"])
node(id="T07", name="Resolve counterparty sector and debtor role per sector row", layer="reporting",
     inputs=[s for s in sector_sources if "INSTTTNL" in s or "ENTTY_RL" in s or "MN_" in s or "PRMRY" in s
             or "MLTLTRL" in s],
     outputs=[f"F_18.00.a_{r}_*" for r in SECTOR_ROWS],
     logic={"type": "filter_partition",
            "common": "TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117 and ACCNTNG_CLSSFCTN in (6, 74, 76, 77)",
            "debtor_role": "(ENTTY_RL_TYP in (20, 28) and MN_DBTR_INDCTR_1) or (ENTTY_RL_TYP 27 and "
                           "MN_DPST_TKNG_CRPRTN_INDCTR_1) or (ENTTY_RL_TYP 19 and MN_LSS_INDCTR_1) or "
                           "(ENTTY_RL_TYP 8 and PRMRY_ISSR_INDCTR_1)",
            "rows": {r: ro.loc[f"R_F_18.00.a_{r}", "DESCRIPTION"].split(": ")[-1] for r in SECTOR_ROWS},
            "official_algorithms": {r: alg(f"R_F_18.00.a_{r}") for r in SECTOR_ROWS}},
     business_group="COUNTERPARTY_ENRICHMENT", provenance="bird_official", open_issues=["OI-10", "OI-12"])
node(id="T08", name="Row 0070 as sum of sector rows", layer="reporting",
     inputs=[f"F_18.00.a_{r}" for r in SECTOR_ROWS], outputs=["F_18.00.a_R0070"],
     logic={"type": "aggregate", "official_algorithm": alg("R_F_18.00.a_R0070")},
     business_group="AGGREGATION", provenance="bird_official", open_issues=["OI-10"])
node(id="T09", name="Column 0010: gross carrying amount", layer="reporting",
     inputs=["GRSS_CRRYNG_AMNT"], outputs=["cell F_18.00.a R0070 C0010"],
     logic={"type": "aggregate", "function": "sum", "filter": "GRSS_CRRYNG_AMNT > 0",
            "official_algorithm": alg("R_F_18.00.a_C0010")},
     business_group="AGGREGATION", provenance="bird_official")
node(id="T10", name="Column 0060: non-performing", layer="reporting",
     inputs=["INSTRMNT_RL_EIL.PRFRMNG_STTS", "SCRTY_EXCHNG_TRDBL_DRVTV_EIL.DBT_SCRTY_PRFRMNG_STTS_TYP", "GRSS_CRRYNG_AMNT"],
     outputs=["cell F_18.00.a R0070 C0060"],
     logic={"type": "aggregate", "function": "sum",
            "filter": "GRSS_CRRYNG_AMNT > 0 and (PRFRMNG_STTS = CRDT_QLTY_1 or DBT_SCRTY_PRFRMNG_STTS_TYP = "
                      "SCRTY_EXCHNG_TRDBL_DRVTV_TYP_20)", "official_algorithm": alg("R_F_18.00.a_C0060")},
     business_group="CREDIT_QUALITY_CLASSIFICATION", provenance="bird_official")
node(id="T11", name="Compute NPL ratio", layer="kri",
     inputs=["cell F_18.00.a R0070 C0060", "cell F_18.00.a R0070 C0010"], outputs=["kri.NPL_RATIO"],
     logic={"type": "expression", "expr": "C0060 / NULLIF(C0010, 0)"},
     business_group="KRI_CALCULATION", provenance="gap_fill", open_issues=["OI-07"])

def bare_member_predicates(text):
    """Member IDs used as a whole predicate (e.g. 'or TYP_INSTRMNT_1201'), not as items of an IN list."""
    lines = [l.split("--")[0].strip() for l in text.split("\n")]
    lines = [l for l in lines if l]
    out = []
    for i, code in enumerate(lines):
        m = re.fullmatch(r"(?:or\s+|and\s+|\(\s*)?([A-Z][A-Z0-9_]+)", code)
        if not (m and m.group(1) in mem.index):
            continue
        prev = lines[i - 1] if i else ""
        prev2 = lines[i - 2] if i > 1 else ""
        in_list = prev.endswith(",") or re.search(r"\bin\s*\(?$", prev) or (prev == "(" and re.search(r"\bin$", prev2))
        if not in_list:
            out.append(m.group(1))
    return out

validation = {}
for r in used_routines:
    u, b = unknown_identifiers(alg(r)), bare_member_predicates(alg(r))
    if u or b:
        validation[r] = {"unknown_identifiers": u, "member_used_without_variable": b}

# ---------- diff vs v0.1 ----------
v01 = yaml.safe_load(open(V01, encoding="utf-8"))
v01_filters = {f["variable"]: f["member"] for f in v01["kri"]["numerator"]["bird_filters"]}
off_filters = {f["variable"]: f["member"] for f in numerator["filters"]}
v01_leaves = lambda var_: {l["member"] for f in v01["kri"]["numerator"]["bird_filters"] if f["variable"] == var_
                           for l in f.get("leaf_members", [])}
off_products = {"TYP_INSTRMNT_1020", "TYP_INSTRMNT_1022", "TYP_INSTRMNT_1023", "TYP_INSTRMNT_120", "TYP_INSTRMNT_130",
                "TYP_INSTRMNT_140", "TYP_INSTRMNT_162", "TYP_INSTRMNT_163", "TYP_INSTRMNT_51", "TYP_INSTRMNT_80",
                "TYP_INSTRMNT_511", "TYP_INSTRMNT_512", "TYP_INSTRMNT_522", "TYP_INSTRMNT_1202"}
com_products = v01_leaves("TYP_INSTRMNT")
com_roles = {m.replace("ENTTY_RL_TYP_", "") for m in v01_leaves("PRTY_RL_TYP")}

diff = [
    {"item": "framework_version", "community_v0.1": "FINREP 3.0",
     "official": "FINREP " + fw[fw.FRAMEWORK_ID == "FINREP"].VERSION_ID.iloc[0] + " (valid from "
                 + fw[fw.FRAMEWORK_ID == "FINREP"].VALID_FROM.iloc[0] + ")"},
    {"item": "cell_filters", "community_v0.1": sorted(v01_filters), "official": sorted(off_filters),
     "removed_in_official": sorted(set(v01_filters) - set(off_filters)),
     "added_in_official": sorted(set(off_filters) - set(v01_filters))},
    {"item": "instrument_type", "community_v0.1": "filter TYP_INSTRMNT under node TYP_INSTRMNT_251",
     "official": "derived TYP_FNNCL_ASST_INSTRMNT_ANNX_V = TYP_INSTRMNT_1117 (T04, T05)",
     "products_only_in_community": sorted(com_products - off_products),
     "products_only_in_official": sorted(off_products - com_products)},
    {"item": "debtor_roles", "community_v0.1": sorted(com_roles) ,
     "official": ["20", "27", "28", "19", "8"],
     "note": "official pairs each role with its own 'main' indicator; community used MN_DBTR_INDCTR for all"},
    {"item": "gca_amortised_cost", "community_v0.1": "CRRYNG_AMNT - ACCMLTD_IMPRMNT",
     "official": "CRRYNG_AMNT + ACCMLTD_IMPRMNT"},
    {"item": "gca_general_allowances", "community_v0.1": "CRRYNG_AMNT - GNRL_ALLWNCS_* (77 only)",
     "official": "CRRYNG_AMNT + GNRL_ALLWNCS_CRDT_RSK + GNRL_ALLWNCS_BNK_RSK (76, 77, 44 and 9/73/74 if subject to impairment)"},
    {"item": "gca_portfolio_74", "community_v0.1": "CRRYNG_AMNT + ACCMLTD_IMPRMNT unconditionally",
     "official": "only if SBJCT_IMPRMNT_INDCTR_1 and an impairment status applies"},
    {"item": "gca_inputs", "community_v0.1": "ACCMLTD_CHNGS_FV, INSTRMNT_RL_TYP guard",
     "official": "ACCMLTD_CHNGS_FV_CR, no INSTRMNT_RL_TYP guard"},
    {"item": "performing_status_level", "community_v0.1": "ambiguous (PRTY overrides INSTRMNT_RL in generated code)",
     "official": "INSTRMNT_RL.PRFRMNG_STTS (instrument level), plus DBT_SCRTY_PRFRMNG_STTS_TYP for securities"},
    {"item": "reporting_scheme_gate", "community_v0.1": "absent", "official": "FNRP_RPRTNG_SCHM in (1, 2, 3)"},
    {"item": "positive_amount_filter", "community_v0.1": "absent", "official": "GRSS_CRRYNG_AMNT > 0"},
    {"item": "non_negotiable_securities", "community_v0.1": "excluded from row 0070",
     "official": "included as loans and advances (T05)"},
    {"item": "sector_partition", "community_v0.1": "INSTTTNL_SCTR unrestricted at row 0070",
     "official": "row 0070 = sum of six sector rows; positions outside those sectors drop out"},
    {"item": "join_keys", "community_v0.1": "LDM foreign keys",
     "official": "identical keys in role-specific cube relationships (unchanged)"},
    {"item": "business_definitions", "community_v0.1": "empty",
     "official": "variable descriptions and legal references available (see attributes)"},
]

issues = [
    {"id": "OI-01", "status": "RESOLVED", "resolution": "Official uses CRRYNG_AMNT + ACCMLTD_IMPRMNT. The community derivation had the sign wrong."},
    {"id": "OI-02", "status": "RESOLVED", "resolution": "Official branches use IMPRMNT_STTS; the community code's duplicate case and PRFRMNG_STTS match were errors."},
    {"id": "OI-03", "status": "RESOLVED", "resolution": "Join keys confirmed by official cube relationships."},
    {"id": "OI-04", "status": "RESOLVED", "resolution": "Official attribute lineage takes PRFRMNG_STTS from INSTRMNT_RL (instrument level)."},
    {"id": "OI-05", "status": "RESOLVED", "resolution": "No collateral filter in the official cells; collateral is not part of this lineage."},
    {"id": "OI-06", "status": "RESOLVED", "resolution": "Official algorithms use member IDs directly (e.g. CRDT_QLTY_1), so no code mapping is needed."},
    {"id": "OI-07", "status": "DECIDED", "decision": "see decisions.md",
     "resolution": "Official cell description confirms row 0070 sits under 'debt instruments at cost or at amortised cost'. Still decide whether the KRI is this cell ratio or a wider headline ratio."},
    {"id": "OI-08", "status": "RESOLVED", "resolution": "Official export has algorithm text for every routine and business definitions for variables."},
    {"id": "OI-09", "status": "DECIDED", "decision": "see decisions.md", "severity": "medium",
     "issue": "Official algorithms are pseudo-SQL, not executable, and contain defects (see algorithm_validation): identifiers that exist "
              "nowhere in the export, and predicates that name a member without its variable. They must be normalised when rendering SQL; record each fix."},
    {"id": "OI-10", "status": "DECIDED", "decision": "see decisions.md", "severity": "medium",
     "issue": "Official attribute lineage for the R0070 cells omits the counterparty attributes that the sector rows "
              "use (" + str(len(missing_at_total)) + " source attributes, see lineage_gap_at_total_row). Model "
              "R0070 as the sum of sector rows (T08) so lineage is complete."},
    {"id": "OI-11", "status": "DECIDED", "decision": "see decisions.md", "severity": "low",
     "issue": "GRSS_CRRYNG_AMNT gets no value for an amortised-cost loan whose ACCMLTD_IMPRMNT is null; the "
              "C0010/C0060 filter GRSS_CRRYNG_AMNT > 0 then silently drops it. Decide whether null impairment is "
              "treated as zero in the synthetic data."},
    {"id": "OI-12", "status": "DECIDED", "decision": "see decisions.md", "severity": "low",
     "issue": "Official algorithms reference portfolios and products (e.g. ACCNTNG_CLSSFCTN_44, 8, 9, 73) outside "
              "the R0070 scope; the spec keeps only in-scope branches as structured logic and the full text verbatim."},
    {"id": "OI-13", "status": "DECIDED", "decision": "see decisions.md", "severity": "medium",
     "issue": "FNRP_RPRTNG_SCHM sits on INTRNL_GRP_RL, which has no relationship to instruments. The gate is "
              "joined on the context key; which GRP_RL_TYP row applies is not specified."},
    {"id": "OI-14", "status": "OPEN", "severity": "low",
     "issue": "Legal references cite Implementing Regulation (EU) No 680/2014, which was replaced by Implementing "
              "Regulation (EU) 2021/451. Confirm citations before writing the Collibra and regulatory documents."},
    {"id": "OI-15", "status": "OPEN", "severity": "medium",
     "issue": "INSTTTNL_SCTR_S126 (financial auxiliaries) sits under INSTTTNL_SCTR_S12_D in the member hierarchy but is "
              "missing from the member list of official routine R_F_18.00.a_R0110. Read literally, loans to financial "
              "auxiliaries fall in no sector row and drop out of R0070."},
    {"id": "OI-16", "status": "OPEN", "severity": "medium",
     "issue": "R_F_18.00.a_R0100 selects MLTLTRL_DVLPMNT_BNK_INDCTR_1 regardless of sector, and R_F_18.00.a_R0090 "
              "selects general-government sectors without excluding multilateral development banks. A development bank "
              "party with a general-government sector is counted in both rows, so the R0070 sum counts it twice."},
    {"id": "OI-17", "status": "OPEN", "severity": "medium",
     "issue": "Official algorithms compare against parent members while input data may hold their leaves (and vice "
              "versa). R_DER_TYP_FNNCL_ASST_INSTRMNT_ANNX_V_2 excludes INSTTTNL_SCTR_S122_A, but input may hold "
              "S122_A_1/S122_A_2; the sector rows list leaves only, so a party stored as parent S14 or S122_A matches "
              "no row. The SQL compares members literally (OI-09)."},
    {"id": "OI-18", "status": "OPEN", "severity": "low",
     "issue": "The general-allowances branch of R_DER_GRSS_CRRYNG_AMNT_1/_3 fires when either GNRL_ALLWNCS_CRDT_RSK or "
              "GNRL_ALLWNCS_BNK_RSK is not null, but CRRYNG_AMNT + GNRL_ALLWNCS_CRDT_RSK + GNRL_ALLWNCS_BNK_RSK is null "
              "when one of them is null, so the position drops out. The SQL keeps the literal arithmetic (OI-09)."},
]

spec = {
    "spec_version": "0.2-draft",
    "status": "DRAFT - open issues OI-14 to OI-18 are undecided; decided issues are logged in decisions.md",
    "provenance": {
        "primary_source": {"type": "official ECB BIRD metadata export", "file": ZIP.name,
                           "sha256": zip_sha, "obtained_from": "bird.ecb.europa.eu (downloaded by user)",
                           "frameworks": fw[["FRAMEWORK_ID", "VERSION_ID", "VALID_FROM"]].to_dict("records")},
        "supersedes": "v0.1 (community repo regcommunity/FreeBIRD_EIL_67)",
        "legend": {"bird_official": "read from the official export by src/build_spec_official.py",
                   "gap_fill": "added by hand; not specified in the official export"},
    },
    "kri": {
        "id": "KRI_NPL_RATIO_LA",
        "name": "Non-performing loans and advances ratio (debt instruments at cost or amortised cost)",
        "formula": "F_18.00.a R0070 C0060 / F_18.00.a R0070 C0010",
        "numerator": numerator, "denominator": denominator,
        "lineage_gap_at_total_row": missing_at_total,
    },
    "taxonomy_draft": v01["taxonomy_draft"],
    "attributes": attributes,
    "joins": joins,
    "transformations": T,
    "algorithm_validation": {"method": "identifiers in algorithm code (comments removed) checked against "
                                       "variables, members, cubes and routines in the export",
                             "findings": validation},
    "diff_vs_v0.1": diff,
    "open_issues": issues,
}

class D(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def str_rep(d, s):
    return d.represent_scalar("tag:yaml.org,2002:str", s, style="|" if "\n" in s else None)

D.add_representer(str, str_rep)
D.add_representer(type(None), lambda d, _: d.represent_scalar("tag:yaml.org,2002:null", "null"))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:      # LF on every platform
    f.write("# Canonical lineage spec v0.2 - NPL ratio - built from the official BIRD export by src/build_spec_official.py\n")
    yaml.dump(spec, f, Dumper=D, sort_keys=False, allow_unicode=True, width=120)

print("validation:", validation)
print("missing at total:", missing_at_total)
print("products only community:", sorted(com_products - off_products))
print("products only official:", sorted(off_products - com_products))
print("roles community:", com_roles)
