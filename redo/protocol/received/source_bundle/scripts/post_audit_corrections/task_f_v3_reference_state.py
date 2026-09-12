#!/usr/bin/env python3
"""Task F v3 — reference-state stratification audit.

Follow-up on Task F v2. Reproduces the arithmetic of three load-bearing
apo-bistability figures but stratifies each by the ACTIVE reference's
G-protein state:

  - G-protein-bound (heterotrimer / chimera)
  - Gα-only-partial (mini-G alpha alone, no beta/gamma)
  - G-protein-free (nanobody, agonist-only, α5-CT-peptide-only)

Prior finding (docs/BLOCK_B_PLAN_v4_2026_09_02.md §"reference-state
confound"): G-protein-free active references sit 3.8 Å lower on TM6
than G-protein-containing (11.60 vs 15.36 Å) and the four G-protein-free
receptors (ADRB2, AGTR1, CNR1, OPRD) show 0.430 median apo coherent-
active fraction vs 0.030 for the other 26 — a 14× difference.

Post Stage 0 Gate 2 refinement (docs/BLOCK_B_STAGE0_COMPLETE_2026_09_02.md
§"OPRD, OPSD, LSHR label fixes"):
  - OPSD 4X1H → α5-CT-peptide-only (from `native`); moves OPSD into
    G-protein-free
  - LSHR 7FIH → Gα-heterotrimer-native (from `mini_G`); stays in
    G-protein-bound
  - AA2AR 5G53 → Gα-only-miniG (from `mini_G`); moves into partial

These relabels were proposed but not yet committed to
refs/reference_set.csv (per Stage 0 §"Not-yet-done"). This script:
  - reads the CSV as-is (with SHA-256 pin)
  - reports the RAW label
  - applies the Gate 2 relabels as a SECONDARY view
  - and reports BOTH strata verdicts.

Load-bearing question: does the "10 of 32 receptors within 1.0 Å"
signal concentrate in the G-protein-free group?
"""
from __future__ import annotations
import argparse, csv, json, math, statistics, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import REPO, sha256, git_sha, now_utc

# Panel-wide two-instrument thresholds (from rows.pocket.csv header — uniform).
NPXXY_OH_LT = 9.082
TM6_TILT_GT = 14.932
RMSD_THRESHOLD_A = 1.0
SEALED = {"ACM1", "ADA2A", "ADRB1", "CCKAR", "DRD3", "EDNRA", "HRH3", "OX2R"}

# Stage 0 Gate 2 label refinements (docs/BLOCK_B_STAGE0_COMPLETE_2026_09_02.md).
# Not yet committed to refs/reference_set.csv, but load-bearing for this audit.
GATE2_RELABELS = {
    # (receptor_slug, pdb_id) -> refined active_stabilization_source
    ("OPSD", "4X1H"): "alpha5_CT_peptide_only",  # from "native"
    ("LSHR", "7FIH"): "native_heterotrimer",     # from "mini_G"
    ("AA2AR", "5G53"): "Ga_only_miniG",          # from "mini_G"
}

BACKBONE_TAG = ("boltz", "chai", "of3", "protenix")


def _f(x):
    if x is None or x == "" or str(x).lower() in ("nan", "none"):
        return None
    try:
        return float(x)
    except (ValueError, TypeError):
        return None


def _backbone(p):
    for bb in BACKBONE_TAG:
        if f"/{bb}/" in p:
            return bb
    return ""


def _classify_g_protein_state_raw(source, stab_elements, notes):
    """Two-stratum split following BLOCK_B_PLAN_v4_2026_09_02.md:
    - G-protein-containing: native, mini_G, chimera, DVL_DEP
    - G-protein-free: nanobody, agonist_only
    Uses source (active_stabilization_source) as the primary key."""
    s = (source or "").strip().lower()
    if s in ("nanobody", "agonist_only", "agonist-only"):
        return "g_protein_free_raw"
    if s in ("native", "mini_g", "chimera", "dvl_dep", ""):
        return "g_protein_bound_raw"
    return f"other_raw:{s}"


def _classify_g_protein_state_refined(source, stab_elements, notes,
                                       receptor, pdb):
    """Five-stratum split per Stage 0 Gate 2 refinement:
      - heterotrimer_native (real Gα + Gβγ)
      - Ga_only_miniG (mini-Gα alone, no βγ)
      - chimera (Gα class swap in scaffold)
      - alpha5_CT_peptide_only (only C-terminal peptide of Gα)
      - nanobody
      - agonist_only

    Also derives a 3-stratum super-classification:
      - bound (heterotrimer + chimera + partial mini_G)
      - partial (mini-Gα-only, if flagged)
      - free (nanobody + agonist_only + α5-CT-peptide)
    """
    # Apply Gate 2 relabels first
    key = (receptor.upper(), (pdb or "").upper())
    refined_source = GATE2_RELABELS.get(key, (source or "").strip().lower())

    s = refined_source.lower() if refined_source else ""
    if s == "alpha5_ct_peptide_only":
        cls_5 = "alpha5_CT_peptide_only"
        cls_3 = "g_protein_free"
    elif s == "ga_only_minig":
        cls_5 = "Ga_only_miniG"
        cls_3 = "g_protein_partial"
    elif s == "native_heterotrimer":
        cls_5 = "heterotrimer_native"
        cls_3 = "g_protein_bound"
    elif s in ("nanobody",):
        cls_5 = "nanobody"
        cls_3 = "g_protein_free"
    elif s in ("agonist_only", "agonist-only"):
        cls_5 = "agonist_only"
        cls_3 = "g_protein_free"
    elif s == "chimera":
        cls_5 = "chimera"
        cls_3 = "g_protein_bound"
    elif s == "native":
        # No Gate 2 override; treat as heterotrimer_native (most native
        # entries in Block B panel are Gα+Gβγ+scFv/BRIL).
        cls_5 = "heterotrimer_native"
        cls_3 = "g_protein_bound"
    elif s == "mini_g":
        # No Gate 2 override; keep as mini_G. In BLOCK_B_PLAN_v4 this went
        # to G-protein-containing; keep that pending per-receptor curation.
        cls_5 = "mini_G_ambiguous"
        cls_3 = "g_protein_bound"
    else:
        cls_5 = f"other:{s}"
        cls_3 = "unknown"
    return cls_5, cls_3, refined_source


def _load_refs(path):
    """{receptor_upper: [(role, pdb, source, stab_elements, notes)]}"""
    out = defaultdict(list)
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rec = (row.get("receptor_slug") or "").strip().upper()
            role = (row.get("role") or "").strip().lower()
            pdb = (row.get("pdb_id") or "").strip().upper()
            src = (row.get("active_stabilization_source") or "").strip()
            stab = (row.get("stabilising_elements") or "").strip()
            notes = (row.get("curation_note") or "")
            if rec and role and pdb:
                out[rec].append({
                    "role": role, "pdb": pdb,
                    "source": src, "stab_elements": stab, "notes": notes,
                    "d_tm6": _f(row.get("d_r350_r630_ca_ref")),
                    "d_tilt": _f(row.get("d_gpcrdb_tm6_tilt_ref")),
                })
    return out


def _load_rcsb_cache(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _pct_of(k, n):
    return (k / n) if n > 0 else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows-pocket", type=Path,
                    default=REPO / "experiments/018_block_a_switch_test"
                    "/analysis/rows.pocket.csv")
    ap.add_argument("--rows-rmsd", type=Path,
                    default=REPO / "experiments/018_block_a_switch_test"
                    "/analysis/rows.rmsd.csv")
    ap.add_argument("--ref-set", type=Path,
                    default=REPO / "refs/reference_set.csv")
    ap.add_argument("--rcsb-cache", type=Path,
                    default=REPO / "refs/cache/rcsb_deposit_dates.json")
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/task_F_v3_reference_state_stratification.json")
    args = ap.parse_args()

    ref_set = _load_refs(args.ref_set)
    rcsb_cache = _load_rcsb_cache(args.rcsb_cache) if args.rcsb_cache.exists() else {}

    # --- 1. Per-receptor active-ref metadata for the 32 (Class A minus sealed) ---
    #
    # The panel-32 comes from receptors with an active ref that are Class A
    # minus sealed. Class detection: use the rows.pocket.csv receptor_class,
    # but easier to identify by the 32-receptor list already used in F v2.
    # Compute per receptor from Block A rows.

    # Build set of receptors that have Block A rows (any class)
    def _load_rows(path):
        with open(path) as f:
            return list(csv.DictReader(f))
    rows_pocket = _load_rows(args.rows_pocket)
    rows_rmsd = _load_rows(args.rows_rmsd)

    # Class A receptors from rows.pocket
    class_a_receptors = set()
    for r in rows_pocket:
        if (r.get("receptor_class") or "").upper() == "A":
            rec = (r.get("receptor_slug") or "").upper()
            if rec:
                class_a_receptors.add(rec)

    panel_32 = sorted(class_a_receptors - SEALED)

    # --- 2. Active-ref classification per receptor ---
    per_receptor_meta = {}
    for rec in panel_32:
        entries = ref_set.get(rec, [])
        active = [e for e in entries if e["role"] == "active"]
        inactive = [e for e in entries if e["role"] == "inactive"]
        if not active:
            per_receptor_meta[rec] = {
                "active_pdb": None,
                "active_source_raw": None,
                "active_stabilising_elements": None,
                "raw_class_2": "no_active_ref",
                "refined_class_5": "no_active_ref",
                "refined_class_3": "no_active_ref",
                "d_tm6_active_ref": None,
                "d_tilt_active_ref": None,
                "gate2_relabel_applied": False,
            }
            continue
        # Pick the first (in practice each Class-A receptor has one active row)
        a = active[0]
        raw_c = _classify_g_protein_state_raw(a["source"], a["stab_elements"], a["notes"])
        refined_5, refined_3, refined_src = _classify_g_protein_state_refined(
            a["source"], a["stab_elements"], a["notes"], rec, a["pdb"]
        )
        rcsb = rcsb_cache.get(a["pdb"], {}) if rcsb_cache else {}
        per_receptor_meta[rec] = {
            "active_pdb": a["pdb"],
            "active_source_raw": a["source"],
            "active_stabilising_elements": a["stab_elements"],
            "active_notes_head": (a["notes"] or "")[:200],
            "raw_class_2": raw_c,
            "refined_source_gate2": refined_src,
            "refined_class_5": refined_5,
            "refined_class_3": refined_3,
            "d_tm6_active_ref": a["d_tm6"],
            "d_tilt_active_ref": a["d_tilt"],
            "gate2_relabel_applied": (rec.upper(), a["pdb"].upper()) in GATE2_RELABELS,
            "rcsb_cached_deposition": rcsb.get("deposition_date") if rcsb else None,
        }

    # --- 3. Compute panel-mean apo two-instrument fraction per receptor ---
    per_receptor_apo = defaultdict(lambda: {"n": 0, "n_coh_active": 0,
                                             "n_rmsd_lt_1A": 0,
                                             "n_rmsd_ge_0": 0,
                                             "min_rmsd_to_active": float("inf")})
    apo_rows = 0
    for r in rows_pocket:
        if str(r.get("passed", "")).lower() != "true":
            continue
        if (r.get("receptor_class") or "").upper() != "A":
            continue
        rec = (r.get("receptor_slug") or "").upper()
        if rec not in panel_32:
            continue
        # apo state: input_state_claim contains 'apo'
        claim = (r.get("input_state_claim") or "").lower()
        if "apo" not in claim:
            continue
        oh = _f(r.get("d_npxxy_y558_y753_oh"))
        tilt = _f(r.get("d_gpcrdb_tm6_tilt_246_637_ca"))
        if oh is None or tilt is None:
            continue
        per_receptor_apo[rec]["n"] += 1
        if oh < NPXXY_OH_LT and tilt > TM6_TILT_GT:
            per_receptor_apo[rec]["n_coh_active"] += 1
        apo_rows += 1

    # RMSD per receptor (min across apo predictions)
    for r in rows_rmsd:
        # apo detection: input_state_claim
        claim = (r.get("input_state_claim") or "").lower()
        if "apo" not in claim:
            continue
        if str(r.get("passed", "")).lower() != "true":
            continue
        rec = (r.get("receptor_slug") or "").upper()
        if rec not in panel_32:
            continue
        rmsd = _f(r.get("rmsd_to_active_ref"))
        if rmsd is None:
            continue
        d = per_receptor_apo[rec]
        d["n_rmsd_ge_0"] += 1
        if rmsd < d["min_rmsd_to_active"]:
            d["min_rmsd_to_active"] = rmsd
        if rmsd < RMSD_THRESHOLD_A:
            d["n_rmsd_lt_1A"] += 1

    per_receptor_summary = {}
    for rec in panel_32:
        d = per_receptor_apo.get(rec, {"n": 0, "n_coh_active": 0,
                                        "n_rmsd_lt_1A": 0, "n_rmsd_ge_0": 0,
                                        "min_rmsd_to_active": float("inf")})
        min_rmsd = (d["min_rmsd_to_active"] if d["min_rmsd_to_active"] < float("inf")
                    else None)
        per_receptor_summary[rec] = {
            "n_apo_rows_2instrument": d["n"],
            "n_coherent_active": d["n_coh_active"],
            "coherent_active_fraction": _pct_of(d["n_coh_active"], d["n"]) if d["n"] else None,
            "n_apo_rows_rmsd": d["n_rmsd_ge_0"],
            "min_rmsd_to_active_A": min_rmsd,
            "hits_1A_threshold": (min_rmsd is not None and min_rmsd < RMSD_THRESHOLD_A),
        }

    # --- 4. Panel mean, per raw group and per refined group ---
    def _stratum_stats(rec_list):
        """Mean per stratum uses v2's convention: divide by len(rec_list),
        treating receptors with no valid apo-two-instrument rows as 0.
        This reproduces the 15.5 % panel figure from Task F v2."""
        fracs_valid = [per_receptor_summary[r]["coherent_active_fraction"]
                       for r in rec_list
                       if per_receptor_summary[r]["coherent_active_fraction"] is not None]
        fracs_v2_convention = [
            per_receptor_summary[r]["coherent_active_fraction"] or 0.0
            for r in rec_list
        ]
        return {
            "n_receptors": len(rec_list),
            "n_receptors_with_valid_rows": len(fracs_valid),
            "mean_coherent_active_fraction_v2_convention_div_by_all": (
                statistics.fmean(fracs_v2_convention) if fracs_v2_convention else None
            ),
            "mean_coherent_active_fraction_valid_only": (
                statistics.fmean(fracs_valid) if fracs_valid else None
            ),
            "median_coherent_active_fraction_valid_only": (
                statistics.median(fracs_valid) if fracs_valid else None
            ),
            "n_receptors_rmsd_hit_1A": sum(
                1 for r in rec_list if per_receptor_summary[r]["hits_1A_threshold"]
            ),
            "receptors_rmsd_hit_1A": sorted(
                r for r in rec_list if per_receptor_summary[r]["hits_1A_threshold"]
            ),
        }

    # 2-stratum RAW
    raw_bound = [r for r in panel_32 if per_receptor_meta[r]["raw_class_2"] == "g_protein_bound_raw"]
    raw_free = [r for r in panel_32 if per_receptor_meta[r]["raw_class_2"] == "g_protein_free_raw"]
    raw_other = [r for r in panel_32 if per_receptor_meta[r]["raw_class_2"] not in
                  ("g_protein_bound_raw", "g_protein_free_raw")]

    stratified_raw_2 = {
        "g_protein_bound": _stratum_stats(raw_bound),
        "g_protein_free": _stratum_stats(raw_free),
        "other": _stratum_stats(raw_other),
    }
    stratified_raw_2["g_protein_bound"]["receptors"] = raw_bound
    stratified_raw_2["g_protein_free"]["receptors"] = raw_free
    stratified_raw_2["other"]["receptors"] = raw_other

    # 3-stratum REFINED
    refined_bound = [r for r in panel_32 if per_receptor_meta[r]["refined_class_3"] == "g_protein_bound"]
    refined_partial = [r for r in panel_32 if per_receptor_meta[r]["refined_class_3"] == "g_protein_partial"]
    refined_free = [r for r in panel_32 if per_receptor_meta[r]["refined_class_3"] == "g_protein_free"]
    stratified_refined_3 = {
        "g_protein_bound": _stratum_stats(refined_bound),
        "g_protein_partial": _stratum_stats(refined_partial),
        "g_protein_free": _stratum_stats(refined_free),
    }
    stratified_refined_3["g_protein_bound"]["receptors"] = refined_bound
    stratified_refined_3["g_protein_partial"]["receptors"] = refined_partial
    stratified_refined_3["g_protein_free"]["receptors"] = refined_free

    # 5-stratum breakdown
    strata_5 = defaultdict(list)
    for r in panel_32:
        strata_5[per_receptor_meta[r]["refined_class_5"]].append(r)
    stratified_refined_5 = {k: _stratum_stats(v) for k, v in strata_5.items()}
    for k, v in strata_5.items():
        stratified_refined_5[k]["receptors"] = v

    # --- 5. Focus on the 10 receptors flagged by v2's "10 of 32 within 1.0 Å" ---
    ten_of_32 = ["ADRB2", "AGTR1", "CNR1", "CNR2", "CXCR4", "FSHR", "GHSR", "LSHR", "NPY1R", "OPSD"]
    # Verify which of these still hit < 1.0 Å per this recompute
    ten_of_32_recheck = []
    for rec in ten_of_32:
        meta = per_receptor_meta.get(rec, {})
        summ = per_receptor_summary.get(rec, {})
        ten_of_32_recheck.append({
            "receptor": rec,
            "min_rmsd_to_active_A": summ.get("min_rmsd_to_active_A"),
            "hits_1A_threshold": summ.get("hits_1A_threshold"),
            "coherent_active_fraction": summ.get("coherent_active_fraction"),
            "active_pdb": meta.get("active_pdb"),
            "raw_source": meta.get("active_source_raw"),
            "raw_class_2": meta.get("raw_class_2"),
            "refined_class_5": meta.get("refined_class_5"),
            "refined_class_3": meta.get("refined_class_3"),
            "gate2_relabel_applied": meta.get("gate2_relabel_applied"),
            "d_tm6_active_ref": meta.get("d_tm6_active_ref"),
            "d_tilt_active_ref": meta.get("d_tilt_active_ref"),
        })

    n_ten_bound_raw = sum(1 for x in ten_of_32_recheck
                          if x["raw_class_2"] == "g_protein_bound_raw")
    n_ten_free_raw = sum(1 for x in ten_of_32_recheck
                         if x["raw_class_2"] == "g_protein_free_raw")
    n_ten_bound_refined = sum(1 for x in ten_of_32_recheck
                              if x["refined_class_3"] == "g_protein_bound")
    n_ten_partial_refined = sum(1 for x in ten_of_32_recheck
                                 if x["refined_class_3"] == "g_protein_partial")
    n_ten_free_refined = sum(1 for x in ten_of_32_recheck
                              if x["refined_class_3"] == "g_protein_free")

    # --- 6. Verdict per figure ---
    #
    # SURVIVES_STRATIFICATION — signal present in both G-protein-bound and
    #   G-protein-free groups.
    # REFERENCE_ARTEFACT_G_PROTEIN_FREE_DRIVEN — signal concentrates
    #   in G-protein-free.
    # PARTIAL_REFERENCE_ARTEFACT — mixed.
    #
    # We test on the refined 3-stratum: "bound" has ~24 receptors, "free"
    # has ~4-5. If the mean apo coh-active fraction of "bound" is at
    # least half that of "free" AND the "bound" group has at least one
    # 1-Å hit, the signal survives. If "bound" mean is <10 % of "free"
    # AND "bound" has zero 1-Å hits, artefact. Otherwise partial.

    bound_mean = stratified_refined_3["g_protein_bound"]["mean_coherent_active_fraction_v2_convention_div_by_all"] or 0.0
    free_mean = stratified_refined_3["g_protein_free"]["mean_coherent_active_fraction_v2_convention_div_by_all"] or 0.0
    bound_hit_1A = stratified_refined_3["g_protein_bound"]["n_receptors_rmsd_hit_1A"]
    free_hit_1A = stratified_refined_3["g_protein_free"]["n_receptors_rmsd_hit_1A"]

    def _verdict(bound_mean, free_mean, bound_hit_1A, free_hit_1A):
        if free_mean == 0 or bound_mean == 0:
            if bound_hit_1A == 0 and free_hit_1A > 0:
                return "REFERENCE_ARTEFACT_G_PROTEIN_FREE_DRIVEN"
            return "INSUFFICIENT_DATA"
        ratio = bound_mean / free_mean
        if ratio >= 0.5 and bound_hit_1A >= 1:
            return "SURVIVES_STRATIFICATION"
        if ratio < 0.1 and bound_hit_1A == 0:
            return "REFERENCE_ARTEFACT_G_PROTEIN_FREE_DRIVEN"
        return "PARTIAL_REFERENCE_ARTEFACT"

    verdict_coh_active_2 = _verdict(
        stratified_raw_2["g_protein_bound"]["mean_coherent_active_fraction_v2_convention_div_by_all"] or 0,
        stratified_raw_2["g_protein_free"]["mean_coherent_active_fraction_v2_convention_div_by_all"] or 0,
        stratified_raw_2["g_protein_bound"]["n_receptors_rmsd_hit_1A"],
        stratified_raw_2["g_protein_free"]["n_receptors_rmsd_hit_1A"],
    )
    verdict_coh_active_3 = _verdict(bound_mean, free_mean, bound_hit_1A, free_hit_1A)

    # Panel mean over all 32 — v2 convention (divide by 32, no-data → 0)
    all_fracs_v2 = [per_receptor_summary[r]["coherent_active_fraction"] or 0.0
                    for r in panel_32]
    panel_mean_all_32 = statistics.fmean(all_fracs_v2) if all_fracs_v2 else None
    n_hit_1A_total = sum(1 for r in panel_32
                         if per_receptor_summary[r]["hits_1A_threshold"])

    out = {
        "task": "F_v3_reference_state_stratification",
        "reconstruction": {
            "reconstruction_script": str(Path(__file__).resolve()),
            "reconstruction_script_git_sha": git_sha(),
            "generated_at_utc": now_utc(),
            "inputs": {
                "rows_pocket": {"path": str(args.rows_pocket), "sha256": sha256(args.rows_pocket)},
                "rows_rmsd": {"path": str(args.rows_rmsd), "sha256": sha256(args.rows_rmsd)},
                "ref_set": {"path": str(args.ref_set), "sha256": sha256(args.ref_set)},
                "rcsb_cache": {
                    "path": str(args.rcsb_cache),
                    "sha256": (sha256(args.rcsb_cache) if args.rcsb_cache.exists() else None),
                },
            },
        },
        "predicates": {
            "two_instrument_coherent_active": (
                f"(d_npxxy_y558_y753_oh < {NPXXY_OH_LT}) AND "
                f"(d_gpcrdb_tm6_tilt_246_637_ca > {TM6_TILT_GT})"
            ),
            "rmsd_threshold_A": RMSD_THRESHOLD_A,
        },
        "panel_definition": {
            "class_a_receptors": sorted(class_a_receptors),
            "sealed_excluded": sorted(SEALED),
            "panel_32": panel_32,
            "n_panel": len(panel_32),
        },
        "corrected_panel_mean": {
            "figure": "panel-mean apo two-instrument coherent-active fraction, Class A minus sealed",
            "observed": panel_mean_all_32,
            "claimed_in_prose": 0.145,
            "recomputed_task_f_v2": 0.155,
            "used_here": panel_mean_all_32,
            "provenance": (
                "docs/BLOCK_B_CLAIM_AUDIT.md §4.2 says 14.5%; Task F v2 recomputed "
                "15.5% (0.155). This v3 recomputes with pinned SHA-256 inputs; use "
                "the recomputed value going forward."
            ),
        },
        "per_receptor_active_ref_metadata": per_receptor_meta,
        "per_receptor_apo_summary": per_receptor_summary,
        "stratified_raw_2": stratified_raw_2,
        "stratified_refined_3": stratified_refined_3,
        "stratified_refined_5": stratified_refined_5,
        "ten_of_32_receptor_breakdown": {
            "receptors_hit_1A_recheck": ten_of_32_recheck,
            "n_hit_1A_total_across_32": n_hit_1A_total,
            "raw_2_stratum": {
                "n_in_g_protein_bound_group": n_ten_bound_raw,
                "n_in_g_protein_free_group": n_ten_free_raw,
            },
            "refined_3_stratum": {
                "n_in_g_protein_bound": n_ten_bound_refined,
                "n_in_g_protein_partial": n_ten_partial_refined,
                "n_in_g_protein_free": n_ten_free_refined,
            },
        },
        "verdict": {
            "figure_a_coh_active_fraction_2stratum_raw": {
                "verdict": verdict_coh_active_2,
                "bound_mean": stratified_raw_2["g_protein_bound"]["mean_coherent_active_fraction_v2_convention_div_by_all"],
                "free_mean": stratified_raw_2["g_protein_free"]["mean_coherent_active_fraction_v2_convention_div_by_all"],
            },
            "figure_a_coh_active_fraction_3stratum_refined": {
                "verdict": verdict_coh_active_3,
                "bound_mean": bound_mean,
                "partial_mean": stratified_refined_3["g_protein_partial"]["mean_coherent_active_fraction_v2_convention_div_by_all"],
                "free_mean": free_mean,
                "bound_free_ratio": (bound_mean / free_mean) if free_mean > 0 else None,
                "prior_finding_ratio_1_over_14x": "1/14 = 0.071",
            },
            "figure_b_10_of_32_within_1A": {
                "n_receptors_hit_1A_bound_raw": stratified_raw_2["g_protein_bound"]["n_receptors_rmsd_hit_1A"],
                "n_receptors_hit_1A_free_raw": stratified_raw_2["g_protein_free"]["n_receptors_rmsd_hit_1A"],
                "n_receptors_hit_1A_bound_refined": bound_hit_1A,
                "n_receptors_hit_1A_partial_refined": stratified_refined_3["g_protein_partial"]["n_receptors_rmsd_hit_1A"],
                "n_receptors_hit_1A_free_refined": free_hit_1A,
                "verdict_if_all_hits_are_free": (
                    "REFERENCE_ARTEFACT" if bound_hit_1A == 0 and free_hit_1A > 0
                    else "PARTIAL_ARTEFACT_MIXED" if bound_hit_1A > 0 and free_hit_1A > 0
                    else "SURVIVES_ON_BOUND_GROUP"
                ),
                "narrative": (
                    "If NO receptors from the G-protein-bound group cross 1.0 Å, "
                    "the claim collapses entirely to a reference-selection observation."
                ),
            },
        },
        "gate2_relabels_applied": {
            f"{rec}:{pdb}": v for (rec, pdb), v in GATE2_RELABELS.items()
        },
        "reference_notes": {
            "FSHR_flag": (
                "User note: FSHR 8I2H = FSH + compound-21f PAM (INACTIVE reference). "
                "Active ref in this analysis is 8I2G (mini-G construct)."
            ),
            "LSHR_flag": (
                "User note: LSHR 7FIJ = Org43553-bound inactive/PAM (INACTIVE reference). "
                "Active ref in this analysis is 7FIH (mini-G construct). Gate 2 "
                "proposed relabel 7FIH mini_G -> native heterotrimer; this v3 applies it."
            ),
            "OPSD_flag": (
                "User note: OPSD 7ZBC = post-photoactivation intermediate (INACTIVE reference). "
                "Active ref in this analysis is 4X1H, curated as α5-CT peptide of Gα-t only. "
                "Gate 2 proposed relabel 4X1H native -> α5-CT-peptide-only; this v3 applies it. "
                "Under refined stratification, OPSD is G-PROTEIN-FREE."
            ),
            "AA2AR_flag": (
                "AA2AR 5G53 relabeled by Gate 2 from mini_G -> Ga_only_miniG "
                "(partial G-protein). Included in Class A panel-32."
            ),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"wrote {args.out}")
    print(f"panel_32 size = {len(panel_32)}")
    print(f"panel mean coh-active (v2 conv) = {panel_mean_all_32:.4f} "
          f"(claimed 0.145, F v2 = 0.155)")
    print(f"n receptors hit 1.0 A across 32 = {n_hit_1A_total}")
    print()
    print("Refined 3-stratum:")
    for stratum in ("g_protein_bound", "g_protein_partial", "g_protein_free"):
        s = stratified_refined_3[stratum]
        print(f"  {stratum:<20} n={s['n_receptors']:2d} "
              f"mean_coh={s['mean_coherent_active_fraction_v2_convention_div_by_all']}  "
              f"n_hit_1A={s['n_receptors_rmsd_hit_1A']}")
    print(f"\nBound vs Free mean ratio = "
          f"{(bound_mean/free_mean) if free_mean > 0 else float('nan'):.3f} "
          f"(prior finding was 1/14 = 0.071)")
    print(f"Verdict (coh_active): {verdict_coh_active_3}")
    print(f"Verdict (10-of-32): "
          f"{out['verdict']['figure_b_10_of_32_within_1A']['verdict_if_all_hits_are_free']}")
    print()
    print("10-of-32 breakdown:")
    for entry in ten_of_32_recheck:
        rec = entry["receptor"]
        print(f"  {rec:<8} pdb={entry['active_pdb']} raw={entry['raw_class_2']}  "
              f"refined={entry['refined_class_3']}  "
              f"min_rmsd={entry['min_rmsd_to_active_A']} "
              f"hits_1A={entry['hits_1A_threshold']}")


if __name__ == "__main__":
    main()
