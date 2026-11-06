# ARCHIVED - kept for traceability only. Produced specs/npl_ratio_lineage_spec_v0.1.yaml from the
# community repo regcommunity/FreeBIRD_EIL_67, which was found to contain errors (see diff_vs_v0.1 in
# specs/npl_ratio_lineage_spec_v0.2.yaml). Do not use it for new work; paths are from the original sandbox.
"""
Build a canonical lineage spec for the NPL ratio KRI from ECB BIRD artefacts.

Sources (shallow clones):
  regcommunity/FreeBIRD_EIL_67  - SMCubes metadata export, input-layer LDM, generated
                                  FINREP filter code, joins config, derivation files
Everything tagged provenance=bird_extracted is read from those files by this script.
Everything tagged gap_fill was added by hand because BIRD does not supply it
(join keys in code, KRI formula, business-group labels) and needs human sign-off.
"""
import subprocess
import pandas as pd
import yaml

REPO = "/home/claude/FreeBIRD_EIL_67"
SM = f"{REPO}/artefacts/smcubes_artefacts/"
IL = f"{REPO}/birds_nest/resources/il/"
TABLE = "FINREP_REF_F_18_00_a_REF_FINREP 3_0"
ROW, COL_TOTAL, COL_NPE = "0070", "0010", "0060"

sha = subprocess.check_output(["git", "-C", REPO, "rev-parse", "HEAD"]).decode().strip()

def rd(path, **kw):
    return pd.read_csv(path, dtype=str, encoding="utf-8-sig", **kw)

member = rd(SM + "member.csv").drop_duplicates("MEMBER_ID").set_index("MEMBER_ID").NAME
mhn = rd(SM + "member_hierarchy_node.csv")

def leaves(node, seen=None):
    seen = seen or set()
    kids = set(mhn[mhn.PARENT_MEMBER_ID == node].MEMBER_ID) - {node}
    if not kids:
        return {node}
    out = set()
    for k in kids:
        if k not in seen:
            seen.add(k)
            out |= leaves(k, seen)
    return out

def member_label(m):
    n = member.get(m, m)
    return n if isinstance(n, str) else m

def expand(m):
    return [{"member": l, "label": member_label(l)[:90]} for l in sorted(leaves(m))]

# ---------- report cells ----------
ao = rd(SM + "axis_ordinate.csv")
ax = rd(SM + "axis.csv")
ax = ax[ax.TABLE_ID == TABLE]
ao = ao[ao.AXIS_ID.isin(ax.AXIS_ID)]
tc = rd(SM + "table_cell.csv")
tc = tc[tc.TABLE_ID == TABLE]
cp = rd(SM + "cell_position.csv")
cp = cp[cp.CELL_ID.isin(tc.CELL_ID)]
oi = rd(SM + "ordinate_item.csv")
combo = rd(SM + "combination.csv")
ci = rd(SM + "combination_item.csv")

def ordinate(axis_no, code):
    oid = f"{TABLE}_{axis_no}_{code}"
    r = ao[ao.AXIS_ORDINATE_ID == oid].iloc[0]
    dpm = oi[oi.AXIS_ORDINATE_ID == oid][["VARIABLE_ID", "MEMBER_ID"]]
    return oid, r.NAME, [
        ({"dpm_dimension": v, "dpm_member": m, "label": member_label(m)} if isinstance(m, str)
         else {"dpm_dimension": v, "role": "metric (no member)"})
        for v, m in dpm.values
    ]

def cell(col_code):
    rid, rname, rdpm = ordinate(2, ROW)
    cid, cname, cdpm = ordinate(1, col_code)
    cell_id = (set(cp[cp.AXIS_ORDINATE_ID == rid].CELL_ID) & set(cp[cp.AXIS_ORDINATE_ID == cid].CELL_ID)).pop()
    comb_suffix = tc[tc.CELL_ID == cell_id].TABLE_CELL_COMBINATION_ID.iloc[0]
    comb = combo[combo.COMBINATION_ID.str.endswith("_" + comb_suffix)].iloc[0]
    items = ci[ci.COMBINATION_ID == comb.COMBINATION_ID]
    filters = []
    for r in items.itertuples():
        lv = sorted(leaves(r.MEMBER_ID))
        f = {"variable": r.VARIABLE_ID, "member": r.MEMBER_ID, "label": member_label(r.MEMBER_ID)[:90]}
        if r.MEMBER_ID.endswith("_-1"):
            f["semantics"] = "no restriction (all members)"
        elif lv != [r.MEMBER_ID]:
            f["semantics"] = "member is a hierarchy node; any leaf below it qualifies"
            f["leaf_members"] = expand(r.MEMBER_ID)
        filters.append(f)
    return {
        "template": "F 18.00.a",
        "row": {"code": ROW, "label": rname, "dpm_ordinate": rdpm},
        "column": {"code": col_code, "label": cname, "dpm_ordinate": cdpm},
        "bird_cell_id": cell_id,
        "bird_combination_id": comb.COMBINATION_ID,
        "metric": comb.METRIC,
        "bird_filters": filters,
        "provenance": "bird_extracted",
    }

denominator = cell(COL_TOTAL)
numerator = cell(COL_NPE)
diff = [
    (a["variable"], a["member"], b["member"])
    for a, b in zip(denominator["bird_filters"], numerator["bird_filters"])
    if a["member"] != b["member"]
]

# ---------- product slices (joins configuration) ----------
jdef = rd(f"{REPO}/artefacts/joins_configuration/join_for_product_il_definitions_FINREP_REF.csv")
loan_slices = ["Advances that are not loans", "Other loans", "Credit card debt", "Trade receivables",
               "Finance leases", "On demand and short notice", "Reverse repurchase agreements"]
slices = []
for s in loan_slices:
    r = jdef[jdef.Name == s].iloc[0]
    slices.append({"slice": s, "main_table": r["Main Table"], "product_filter_code": r["Filter"],
                   "related_tables": r["Related Tables"].split(":")})

# ---------- input-layer attributes ----------
cols = rd(IL + "DM_Columns.csv")
used = {
    "INSTRMNT": ["INSTRMNT_ID", "INSTRMNT_TYP_PRDCT", "RPYMNT_RGHTS"],
    "INSTRMNT_RL": ["INSTRMNT_ID", "INSTRMNT_RL_TYP", "GRSS_CRRYNG_AMNT", "CRRYNG_AMNT", "ACCMLTD_IMPRMNT",
                    "ACCMLTD_CHNGS_FV", "FV", "GNRL_ALLWNCS_BNK_RSK", "GNRL_ALLWNCS_CRDT_RSK",
                    "BLNC_SHT_RCGNSD_FNNCL_ASST_INSTRMNT_FR_VL_TYP", "ACCNTNG_CLSSFCTN", "HLD_SL_INDCTR",
                    "SBJCT_IMPRMNT_INDCTR", "IMPRMNT_STTS", "PRFRMNG_STTS", "DFLT_STTS", "PRPS"],
    "INSTRMNT_ENTTY_RL_ASSGNMNT": ["INSTRMNT_ID", "PRTY_ID", "ENTTY_RL_TYP", "MN_DBTR_INDCTR"],
    "ENTTY_RL": ["PRTY_ID", "ENTTY_RL_TYP"],
    "PRTY": ["PRTY_ID", "INSTTTNL_SCTR", "MLTLTRL_DVLPMNT_BNK_INDCTR", "PRFRMNG_STTS", "DFLT_STTS", "ENTRPRS_SZ"],
}
CONTEXT_KEY = ["DT_RFRNC", "RPRTNG_AGNT_ID", "ACCNTNG_CNSLDTN_LVL", "ACCNTNG_STNDRD"]
attributes = []
for t, cl in used.items():
    sub = cols[cols.Table_Name == t]
    for c in CONTEXT_KEY + cl:
        r = sub[sub.Column_Name == c]
        if c in CONTEXT_KEY and t != "INSTRMNT":
            continue
        if len(r):
            r = r.iloc[0]
            attributes.append({"id": f"{t}.{c}", "table": t, "column": c,
                               "bird_domain": r.Domain_Name, "logical_type": r.Logical_Type_Name,
                               "mandatory": r.Mandatory == "Y", "provenance": "bird_extracted",
                               "business_definition": None})
        else:
            attributes.append({"id": f"{t}.{c}", "table": t, "column": c, "provenance": "bird_extracted",
                               "note": "key column present in FK constraints, not in column export"})

# ---------- foreign keys ----------
fk = rd(IL + "DM_ForeignKeys.csv")
ic = rd(IL + "DM_Constr_Index_Columns.csv")
def fk_cols(child, parent):
    r = fk[(fk.Child_Table_Name == child) & (fk.Referred_Table_Name == parent)].iloc[0]
    return {"fk": r.FK_Name, "child": child, "parent": parent,
            "columns": ic[ic.Index_Name == r.FK_Name].sort_values("Sequence").Column_Name.tolist(),
            "provenance": "bird_extracted"}
joins = [fk_cols("INSTRMNT_RL", "INSTRMNT"),
         fk_cols("INSTRMNT_ENTTY_RL_ASSGNMNT", "INSTRMNT"),
         fk_cols("INSTRMNT_ENTTY_RL_ASSGNMNT", "ENTTY_RL"),
         fk_cols("ENTTY_RL", "PRTY")]

def F(var):
    return next(f for f in numerator["bird_filters"] if f["variable"] == var)

def leaf_codes(var, strip):
    f = F(var)
    return [l["member"].replace(strip, "") for l in f.get("leaf_members", [])]

# ---------- transformations ----------
T = []
def node(**kw):
    T.append(kw)

node(id="T01", name="Load instrument master", layer="source",
     inputs=["INSTRMNT.*"], outputs=["stg_instrument"],
     logic={"type": "select", "filter": "DT_RFRNC = :reporting_date AND RPRTNG_AGNT_ID = :reporting_agent"},
     business_group="SOURCE_ACQUISITION", provenance="gap_fill",
     description="Snapshot of all instruments held by the reporting agent at the reference date.")
node(id="T02", name="Load instrument role (accounting view)", layer="source",
     inputs=["INSTRMNT_RL.*"], outputs=["stg_instrument_role"],
     logic={"type": "select", "filter": "DT_RFRNC = :reporting_date AND RPRTNG_AGNT_ID = :reporting_agent"},
     business_group="SOURCE_ACQUISITION", provenance="gap_fill")
node(id="T03", name="Derive gross carrying amount", layer="enrichment",
     inputs=["INSTRMNT_RL." + c for c in ["INSTRMNT_RL_TYP", "ACCNTNG_CLSSFCTN", "CRRYNG_AMNT", "ACCMLTD_IMPRMNT",
             "FV", "ACCMLTD_CHNGS_FV", "GNRL_ALLWNCS_BNK_RSK", "GNRL_ALLWNCS_CRDT_RSK", "IMPRMNT_STTS",
             "PRFRMNG_STTS", "SBJCT_IMPRMNT_INDCTR", "BLNC_SHT_RCGNSD_FNNCL_ASST_INSTRMNT_FR_VL_TYP"]],
     outputs=["stg_instrument_role.GRSS_CRRYNG_AMNT"],
     logic={"type": "case",
            "guard": "only INSTRMNT_RL_TYP in ('10','34','35') feed carrying amount, impairment and status; "
                     "FV inputs only when the fair-value type flag is set; general allowances only when INSTRMNT_RL_TYP = '34'",
            "branches": [
                {"when": "ACCNTNG_CLSSFCTN in ('4','41','47','7') and PRFRMNG_STTS = '11'", "then": "FV"},
                {"when": "ACCNTNG_CLSSFCTN in ('4','41','47','7') and PRFRMNG_STTS = '1'", "then": "FV + ACCMLTD_CHNGS_FV"},
                {"when": "ACCNTNG_CLSSFCTN in ('6','8','9')", "then": "CRRYNG_AMNT - ACCMLTD_IMPRMNT",
                 "flag": "OI-01"},
                {"when": "ACCNTNG_CLSSFCTN = '77' and IMPRMNT_STTS = '26'", "then": "CRRYNG_AMNT - ACCMLTD_IMPRMNT"},
                {"when": "ACCNTNG_CLSSFCTN = '77' and IMPRMNT_STTS = '211'", "then": "CRRYNG_AMNT - GNRL_ALLWNCS_CRDT_RSK"},
                {"when": "ACCNTNG_CLSSFCTN = '77' and IMPRMNT_STTS = '212'", "then": "CRRYNG_AMNT - GNRL_ALLWNCS_BNK_RSK"},
                {"when": "ACCNTNG_CLSSFCTN in ('76','73')", "then": "CRRYNG_AMNT"},
                {"when": "ACCNTNG_CLSSFCTN = '74'", "then": "CRRYNG_AMNT + ACCMLTD_IMPRMNT"},
                {"when": "ACCNTNG_CLSSFCTN in ('2','3')", "then": "FV"},
                {"else": "0"}]},
     business_group="MEASUREMENT", provenance="bird_extracted",
     source_file="artefacts/derivation_files/manually_generated/INSTRMNT_RL_GRSS_CRRYNG_AMNT_derived.py",
     open_issues=["OI-01", "OI-02"])
node(id="T04", name="Assign FINREP product slice", layer="staging",
     inputs=["INSTRMNT.INSTRMNT_TYP_PRDCT"], outputs=["stg_instrument.product_slice"],
     logic={"type": "lookup", "mapping": slices},
     business_group="PRODUCT_SEGMENTATION", provenance="bird_extracted",
     source_file="artefacts/joins_configuration/join_for_product_il_definitions_FINREP_REF.csv",
     description="Loans-and-advances slices of F 18.00.a; the Debt securities slice is excluded for row 0070.")
node(id="T05", name="Attach accounting view to instrument", layer="staging",
     inputs=["stg_instrument", "stg_instrument_role"], outputs=["stg_loan_position"],
     logic={"type": "join", "kind": "inner", "on": joins[0]["columns"]},
     business_group="DATA_INTEGRATION", provenance="bird_extracted+gap_fill",
     note="Join keys from LDM foreign key; BIRD generated join code is an empty stub (OI-03).")
node(id="T06", name="Resolve main debtor counterparty", layer="staging",
     inputs=["stg_loan_position", "INSTRMNT_ENTTY_RL_ASSGNMNT", "ENTTY_RL", "PRTY"],
     outputs=["stg_loan_position.INSTTTNL_SCTR", "stg_loan_position.ENTTY_RL_TYP", "stg_loan_position.MN_DBTR_INDCTR"],
     logic={"type": "join_chain", "path": [j["fk"] for j in joins[1:]],
            "keys": {j["fk"]: j["columns"] for j in joins[1:]},
            "cardinality_guard": "MN_DBTR_INDCTR = '1' to keep one debtor per instrument"},
     business_group="COUNTERPARTY_ENRICHMENT", provenance="bird_extracted+gap_fill", open_issues=["OI-03", "OI-04"])
node(id="T07", name="Union product slices", layer="staging",
     inputs=["stg_loan_position"], outputs=["F_18_00_a_union"],
     logic={"type": "union_all", "parts": loan_slices},
     business_group="TECHNICAL", provenance="bird_extracted",
     source_file="artefacts/filter_code/staging/F_18_00_a_REF_FINREP_3_0_logic.py")
node(id="T08", name="Apply F 18.00 reporting perimeter", layer="reporting",
     inputs=["F_18_00_a_union"], outputs=["F_18_00_a_r0070_scope"],
     logic={"type": "filter", "conditions": [
         {"variable": "ACCNTNG_CLSSFCTN", "in": leaf_codes("ACCNTNG_CLSSFCTN", "ACCNTNG_CLSSFCTN_"),
          "meaning": "cost / amortised cost portfolios (node ACCNTNG_CLSSFCTN_531)"},
         {"variable": "HLD_SL_INDCTR", "eq": "2", "meaning": "not held for sale"},
         {"variable": "SBJCT_IMPRMNT_INDCTR", "eq": "1", "meaning": "subject to impairment"},
         {"variable": "TYP_INSTRMNT", "in": leaf_codes("TYP_INSTRMNT", "TYP_INSTRMNT_"),
          "meaning": "loans and advances (node TYP_INSTRMNT_251)"},
         {"variable": "PRTY_RL_TYP", "in": leaf_codes("PRTY_RL_TYP", "ENTTY_RL_TYP_"),
          "meaning": "debtor-side roles (node ENTTY_RL_TYP_46)"},
         {"variable": "MN_DBTR_INDCTR", "eq": "1", "meaning": "main debtor"},
         {"variable": "NGTBL_SCRTY_INDCTR", "eq": "2", "meaning": "non-negotiable"},
         {"variable": "IMPRMNT_STTS", "in": leaf_codes("IMPRMNT_STTS", "CRDT_QLTY_"),
          "meaning": "IFRS stage 1/2/3 or nGAAP specific allowance (node CRDT_QLTY_17)"},
         {"variable": "DFLT_STTS", "in": leaf_codes("DFLT_STTS", "CRDT_QLTY_"), "meaning": "any default status"},
         {"variable": "TYP_CLLTRL", "node": "TYP_PRTCTN_1", "meaning": "see OI-05"}]},
     business_group="REGULATORY_SCOPE", provenance="bird_extracted",
     note="Codes are BIRD reference members with the domain prefix removed; that they equal input-layer codes is "
          "an assumption (OI-06).", open_issues=["OI-05", "OI-06", "OI-07"])
node(id="T09", name="Classify performing vs non-performing", layer="reporting",
     inputs=["F_18_00_a_r0070_scope.PRFRMNG_STTS"], outputs=["F_18_00_a_r0070_scope.npe_flag"],
     logic={"type": "case", "branches": [
         {"when": "PRFRMNG_STTS in leaves(CRDT_QLTY_1)", "then": "NON_PERFORMING"},
         {"else": "PERFORMING_OR_NA"}]},
     business_group="CREDIT_QUALITY_CLASSIFICATION", provenance="bird_extracted", open_issues=["OI-02", "OI-06"])
node(id="T10", name="Aggregate F 18.00.a r0070 c0010", layer="reporting",
     inputs=["F_18_00_a_r0070_scope.GRSS_CRRYNG_AMNT"], outputs=["cell.F18_00_a.r0070.c0010"],
     logic={"type": "aggregate", "function": "sum", "filter": "PRFRMNG_STTS in leaves(CRDT_QLTY_15)"},
     business_group="AGGREGATION", provenance="bird_extracted")
node(id="T11", name="Aggregate F 18.00.a r0070 c0060", layer="reporting",
     inputs=["F_18_00_a_r0070_scope.GRSS_CRRYNG_AMNT", "F_18_00_a_r0070_scope.npe_flag"],
     outputs=["cell.F18_00_a.r0070.c0060"],
     logic={"type": "aggregate", "function": "sum", "filter": "npe_flag = 'NON_PERFORMING'"},
     business_group="AGGREGATION", provenance="bird_extracted")
node(id="T12", name="Compute NPL ratio", layer="kri",
     inputs=["cell.F18_00_a.r0070.c0060", "cell.F18_00_a.r0070.c0010"], outputs=["kri.NPL_RATIO"],
     logic={"type": "expression", "expr": "c0060 / NULLIF(c0010, 0)"},
     business_group="KRI_CALCULATION", provenance="gap_fill", open_issues=["OI-07"])

spec = {
    "spec_version": "0.1-draft",
    "status": "DRAFT - requires human sign-off of open_issues before artifacts are rendered",
    "provenance": {
        "primary_source": {"repo": "https://github.com/regcommunity/FreeBIRD_EIL_67", "commit": sha,
                           "content": "BIRD SMCubes export (FINREP REF 3.0), Enriched Input Layer 6.7 LDM, "
                                      "generated FINREP filter code, joins configuration, derivation files"},
        "tooling": "https://github.com/eclipse-efbt/efbt (pybirdai)",
        "legend": {"bird_extracted": "read directly from BIRD artefacts by build_npl_spec.py",
                   "gap_fill": "added by hand; BIRD does not specify it",
                   "bird_extracted+gap_fill": "BIRD gives the structure, keys or wiring were completed by hand"},
    },
    "kri": {
        "id": "KRI_NPL_RATIO_LA",
        "name": "Non-performing loans and advances ratio",
        "definition": "Gross carrying amount of non-performing loans and advances divided by the gross carrying "
                      "amount of all loans and advances, within the F 18.00.a row 0070 perimeter.",
        "formula": "F18.00.a r0070 c0060 / F18.00.a r0070 c0010",
        "numerator": numerator, "denominator": denominator,
        "numerator_vs_denominator_filter_difference": [
            {"variable": v, "denominator_member": a, "numerator_member": b} for v, a, b in diff],
        "regulatory_references": [
            {"ref": "Commission Implementing Regulation (EU) 2021/451 (ITS on supervisory reporting), FINREP template F 18.00 "
                    "and Annex V instructions on performing and non-performing exposures", "to_confirm": True},
            {"ref": "Regulation (EU) 575/2013 (CRR) Art. 47a - definition of non-performing exposures", "to_confirm": True},
            {"ref": "EBA risk indicator for the NPL ratio of loans and advances (EBA Risk Dashboard)", "to_confirm": True},
        ],
        "framework_version_note": "BIRD artefacts are labelled FINREP 3.0; check against the EBA reporting framework "
                                  "version you test against.",
    },
    "taxonomy_draft": {
        "SOURCE_ACQUISITION": "Selecting input data for the reporting date and entity.",
        "MEASUREMENT": "Deriving monetary amounts under the applicable accounting standard.",
        "PRODUCT_SEGMENTATION": "Assigning instruments to regulatory product categories.",
        "DATA_INTEGRATION": "Joining related entities into one position record.",
        "COUNTERPARTY_ENRICHMENT": "Attaching debtor attributes such as sector, size and role.",
        "REGULATORY_SCOPE": "Restricting to the perimeter a template cell requires.",
        "CREDIT_QUALITY_CLASSIFICATION": "Classifying exposures by performing, default or impairment status.",
        "AGGREGATION": "Summing positions into report cells.",
        "KRI_CALCULATION": "Combining report cells into the key risk indicator.",
        "TECHNICAL": "Steps with no business meaning (unions, casts, deduplication).",
    },
    "attributes": attributes,
    "joins": joins,
    "transformations": T,
    "open_issues": [
        {"id": "OI-01", "node": "T03", "severity": "high",
         "issue": "For amortised cost (ACCNTNG_CLSSFCTN 6) the derivation computes CRRYNG_AMNT - ACCMLTD_IMPRMNT, "
                  "while the nGAAP branch '74' uses CRRYNG_AMNT + ACCMLTD_IMPRMNT. ACCMLTD_IMPRMNT is typed as a "
                  "non-negative amount, so gross = net + allowance would suggest '+'. Confirm the sign convention."},
        {"id": "OI-02", "node": "T03", "severity": "medium",
         "issue": "Case '9' appears twice in the derivation; the second branch is unreachable. Inside it, "
                  "PRFRMNG_STTS is matched against impairment codes ('26','211','212'), which looks like it was "
                  "meant to be IMPRMNT_STTS."},
        {"id": "OI-03", "node": "T05/T06", "severity": "medium",
         "issue": "The generated F 18.00.a staging code lists the tables to join but the calc_* methods are empty "
                  "stubs. Join keys here come from the LDM foreign keys."},
        {"id": "OI-04", "node": "T06", "severity": "high",
         "issue": "In the generated product classes PRFRMNG_STTS and DFLT_STTS are defined twice (from INSTRMNT_RL "
                  "and from PRTY). In Python the later (PRTY) definition wins, so performing status would be taken "
                  "at counterparty level, not instrument level. Decide which one the KRI uses."},
        {"id": "OI-05", "node": "T08", "severity": "high",
         "issue": "The cell filter constrains TYP_CLLTRL to node TYP_PRTCTN_1. Joining collateral with an inner join "
                  "would drop unsecured loans and a plain join can fan out amounts per collateral item. The collateral "
                  "join was left out of T06; confirm whether the filter is meant as 'any or none'."},
        {"id": "OI-06", "node": "T08/T09", "severity": "medium",
         "issue": "Member mappings from input-layer codes to reference members exist but carry no mapping IDs in this "
                  "export, so code equivalence (e.g. PRFRMNG_STTS '1' to CRDT_QLTY_1) is assumed, not extracted."},
        {"id": "OI-07", "node": "T08/T12", "severity": "medium",
         "issue": "In this BIRD release, row 0070 is restricted to cost / amortised-cost portfolios, not held for "
                  "sale and subject to impairment. Decide whether the KRI is this cell ratio or the headline "
                  "supervisory NPL ratio, which may span more portfolios."},
        {"id": "OI-08", "node": "all", "severity": "low",
         "issue": "logical_transformation_rule.csv has generated (GEN) rules for F 18.00 with no algorithm text, so "
                  "there is no VTL to cross-check against. Business definitions on attributes are empty and must "
                  "be written from Annex V for the Collibra layer."},
    ],
}

class D(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True
D.add_representer(type(None), lambda d, _: d.represent_scalar("tag:yaml.org,2002:null", "null"))

with open("/mnt/user-data/outputs/npl_ratio_lineage_spec.yaml", "w") as f:
    f.write("# Canonical lineage spec - NPL ratio (loans and advances) - generated by build_npl_spec.py\n")
    yaml.dump(spec, f, Dumper=D, sort_keys=False, allow_unicode=True, width=120)
print("transformations:", len(T), "attributes:", len(attributes), "filter diff:", diff)
