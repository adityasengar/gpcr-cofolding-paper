#!/usr/bin/env python3
"""Task A — same-complex vs must-generalise stratification.

Splits Class-A receptors by whether the arm's ligand `bound_pdb`
matches the active/inactive scoring reference PDB (post role_specific
selection), then recomputes the 2x2 interaction test per (backbone x
arm x reference-role x stratum) cell.

Writes:
  verification/stage3b_v2_same_complex_split.json
"""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import (
    REPO, to_float, load_rows, load_ref_set, load_ligand_bound_pdbs,
    cluster_bootstrap_interaction, cluster_bootstrap_diff,
    cluster_bootstrap_two_group_diff, build_recon_meta, _mean,
)


def _active_pdbs(refs):
    return {x["pdb_id"].strip().upper() for x in refs.get("active", [])
            if x.get("pdb_id")}


def _inactive_pdbs_role_aware(refs):
    ins = refs.get("inactive", [])
    preferred = [x for x in ins
                 if (x.get("role_specific") or "").strip().lower()
                 == "inactive_neutral_antagonist"]
    if preferred:
        return {x["pdb_id"].strip().upper() for x in preferred if x.get("pdb_id")}
    return {x["pdb_id"].strip().upper() for x in ins if x.get("pdb_id")}


def build_split(receptors, ref_set, lig_pdbs):
    """Return {rec: {"agonist_stratum": "same"|"different"|"missing",
                     "antag_stratum": ..., detail dicts}}."""
    out = {}
    for rec in sorted(receptors):
        refs = ref_set.get(rec, {})
        ag_pdb = lig_pdbs.get((rec, "full_agonist"), "")
        active_set = _active_pdbs(refs)
        if not ag_pdb:
            ag_stratum, ag_reason = "missing", "no_agonist_bound_pdb"
        elif not active_set:
            ag_stratum, ag_reason = "missing", "no_active_ref_in_reference_set"
        else:
            ag_stratum = "same" if ag_pdb in active_set else "different"
            ag_reason = ""
        an_pdb = ""
        for role in ("neutral_antagonist", "inverse_agonist"):
            p = lig_pdbs.get((rec, role), "")
            if p:
                an_pdb = p; break
        inactive_set = _inactive_pdbs_role_aware(refs)
        if not an_pdb:
            an_stratum, an_reason = "missing", "no_antag_bound_pdb"
        elif not inactive_set:
            an_stratum, an_reason = "missing", "no_inactive_ref_in_reference_set"
        else:
            an_stratum = "same" if an_pdb in inactive_set else "different"
            an_reason = ""
        out[rec] = {
            "agonist": {"stratum": ag_stratum, "bound_pdb": ag_pdb,
                        "active_ref_pdbs": sorted(active_set),
                        "reason": ag_reason},
            "antag":   {"stratum": an_stratum, "bound_pdb": an_pdb,
                        "inactive_ref_pdbs": sorted(inactive_set),
                        "reason": an_reason},
        }
    return out


def per_receptor_pocket_metrics(rows, split, class_only="A"):
    """Return {backbone: {stratum_agonist: {rec: [values]}, ...}}
    for every combination we care about."""
    by_bb = {}
    for r in rows:
        if str(r.get("passed", "")).lower() != "true":
            continue
        if (r.get("receptor_class") or "").upper() != class_only:
            continue
        rec = (r.get("receptor_slug") or "").upper()
        if rec not in split:
            continue
        bb = (r.get("backbone") or "").lower()
        if not bb:
            continue
        role = (r.get("ligand_role") or "").strip()
        row_slot = None
        if role == "full_agonist":
            row_slot = ("agonist", split[rec]["agonist"]["stratum"])
        elif role in ("neutral_antagonist", "inverse_agonist"):
            row_slot = ("antag", split[rec]["antag"]["stratum"])
        else:
            continue
        arm, stratum = row_slot
        if stratum == "missing":
            continue
        pa = to_float(r.get("pocket_ca_rmsd_active"))
        pi = to_float(r.get("pocket_ca_rmsd_inactive"))
        sa = to_float(r.get("pocket_sidechain_rmsd_active"))
        si = to_float(r.get("pocket_sidechain_rmsd_inactive"))
        d = by_bb.setdefault(bb, {})
        for kind, ref_role, val in [("ca", "active", pa),
                                     ("ca", "inactive", pi),
                                     ("sc", "active", sa),
                                     ("sc", "inactive", si)]:
            if math.isnan(val):
                continue
            key = (kind, arm, stratum, ref_role)
            d.setdefault(key, {}).setdefault(rec, []).append(val)
    return by_bb


def compute_cells(rows, split):
    """For each backbone × stratum, compute:
      - 2x2 interaction (pocket_ca_rmsd)
      - per-cell means with cluster-bootstrap CI
      - sidechain interaction as secondary
    """
    per_bb_map = per_receptor_pocket_metrics(rows, split)
    result = {}
    for bb, bins in per_bb_map.items():
        result[bb] = {}
        for stratum in ("same", "different"):
            for kind in ("ca", "sc"):
                agA = bins.get((kind, "agonist", stratum, "active"), {})
                agI = bins.get((kind, "agonist", stratum, "inactive"), {})
                anA = bins.get((kind, "antag",   stratum, "active"), {})
                anI = bins.get((kind, "antag",   stratum, "inactive"), {})
                # per-cell contrasts (agonist − antag on active_ref)
                # and (agonist − antag on inactive_ref)
                d_active   = cluster_bootstrap_diff(agA, anA)
                d_inactive = cluster_bootstrap_diff(agI, anI)
                interaction = cluster_bootstrap_interaction(agA, agI, anA, anI)
                n_agonist_rec = len(set(agA) | set(agI))
                n_antag_rec = len(set(anA) | set(anI))
                n_common = interaction.get("n_clusters", 0)
                # verdict on the interaction — matches Stage 3a shape
                verdict = _verdict(interaction, n_common)
                result[bb][f"{kind}_{stratum}"] = {
                    "interaction": interaction,
                    "d_agonist_minus_antag_active":   d_active,
                    "d_agonist_minus_antag_inactive": d_inactive,
                    "n_receptors_agonist": n_agonist_rec,
                    "n_receptors_antag":   n_antag_rec,
                    "n_receptors_common_all_cells": n_common,
                    "verdict": verdict,
                }
    return result


def _verdict(interaction, n_common):
    if n_common < 5:
        return "UNDERPOWERED_ON_MUST_GENERALISE" if n_common > 0 else "NO_RECEPTORS"
    return ("HOLDS_ON_STRATUM" if interaction.get("signed_nonzero")
            else "NULL_ON_STRATUM")


def build_arm_verdicts(cells, split):
    """Simpler backbone × arm verdict on the CA-primary interaction."""
    n_same_ag = sum(1 for v in split.values() if v["agonist"]["stratum"] == "same")
    n_diff_ag = sum(1 for v in split.values() if v["agonist"]["stratum"] == "different")
    n_same_an = sum(1 for v in split.values() if v["antag"]["stratum"] == "same")
    n_diff_an = sum(1 for v in split.values() if v["antag"]["stratum"] == "different")
    verdicts = {}
    for bb, c in cells.items():
        v_ca_same = c.get("ca_same", {}).get("interaction", {})
        v_ca_diff = c.get("ca_different", {}).get("interaction", {})
        n_diff_common = v_ca_diff.get("n_clusters", 0)
        n_same_common = v_ca_same.get("n_clusters", 0)
        if n_diff_common < 5:
            arm_verdict = "UNDERPOWERED_ON_MUST_GENERALISE"
        elif v_ca_diff.get("signed_nonzero") and v_ca_same.get("signed_nonzero"):
            arm_verdict = "HOLDS_ON_MUST_GENERALISE"
        elif v_ca_same.get("signed_nonzero") and not v_ca_diff.get("signed_nonzero"):
            arm_verdict = "HOLDS_ON_RECALLABLE_ONLY"
        elif v_ca_diff.get("signed_nonzero"):
            arm_verdict = "HOLDS_ON_MUST_GENERALISE_ONLY"
        else:
            arm_verdict = "NULL_ON_BOTH"
        verdicts[bb] = {
            "verdict_ca_interaction": arm_verdict,
            "same_stratum": v_ca_same,
            "different_stratum": v_ca_diff,
            "n_receptors_same_common": n_same_common,
            "n_receptors_different_common": n_diff_common,
        }
    return {
        "panel_split_counts": {
            "agonist_arm": {"same": n_same_ag, "different": n_diff_ag},
            "antag_arm":   {"same": n_same_an, "different": n_diff_an},
        },
        "per_backbone": verdicts,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rows", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rows.tier3.v2.csv")
    ap.add_argument("--manifest", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rescore_manifest.tier3.v2.csv")
    ap.add_argument("--ref-set", type=Path,
                    default=REPO / "refs/reference_set.csv")
    ap.add_argument("--ligand-sets", nargs="+", type=Path,
                    default=[REPO / "refs/ligand_set.csv",
                             REPO / "refs/ligand_set_tier3.csv"])
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/stage3b_v2_same_complex_split.json")
    args = ap.parse_args()

    rows = load_rows(args.rows, manifest_csv=args.manifest)
    ref_set = load_ref_set(args.ref_set)
    lig_pdbs = load_ligand_bound_pdbs(args.ligand_sets)

    class_a_receptors = sorted({
        (r.get("receptor_slug") or "").upper() for r in rows
        if (r.get("receptor_class") or "").upper() == "A"
        and str(r.get("passed", "")).lower() == "true"
    })
    split = build_split(class_a_receptors, ref_set, lig_pdbs)
    cells = compute_cells(rows, split)
    summary = build_arm_verdicts(cells, split)

    # Supplementary per-arm marginal memorization test: for each receptor,
    # compute the agonist-arm's mean (pocket_ca_rmsd_active − pocket_ca_rmsd_inactive)
    # — this per-receptor scalar is the "how active-like is the agonist arm's
    # pocket, relative to the receptor's inactive-ref anchor". Split by
    # same/different agonist stratum and cluster-bootstrap by receptor.
    supp = {}
    for bb in cells:
        per_r_ag = {}
        per_r_an = {}
        for r in rows:
            if str(r.get("passed", "")).lower() != "true":
                continue
            if (r.get("receptor_class") or "").upper() != "A":
                continue
            if (r.get("backbone") or "").lower() != bb:
                continue
            rec = (r.get("receptor_slug") or "").upper()
            if rec not in split:
                continue
            role = (r.get("ligand_role") or "").strip()
            pa = to_float(r.get("pocket_ca_rmsd_active"))
            pi = to_float(r.get("pocket_ca_rmsd_inactive"))
            if math.isnan(pa) or math.isnan(pi):
                continue
            delta = pa - pi  # <0 = pocket is more active-like than inactive-like
            if role == "full_agonist":
                per_r_ag.setdefault(rec, []).append(delta)
            elif role in ("neutral_antagonist", "inverse_agonist"):
                per_r_an.setdefault(rec, []).append(delta)
        # Split by stratum
        supp[bb] = {}
        for arm_key, per_r in (("agonist", per_r_ag), ("antag", per_r_an)):
            same = {r: v for r, v in per_r.items()
                    if split[r][arm_key]["stratum"] == "same"}
            diff = {r: v for r, v in per_r.items()
                    if split[r][arm_key]["stratum"] == "different"}
            same_diff_contrast = cluster_bootstrap_two_group_diff(same, diff)
            supp[bb][arm_key] = {
                "metric": ("pocket_ca_rmsd_active minus pocket_ca_rmsd_inactive"
                           "; <0 = pocket more active-like than inactive-like"),
                "same_stratum_mean": _mean([v for c in same for v in same[c]]),
                "diff_stratum_mean": _mean([v for c in diff for v in diff[c]]),
                "same_minus_diff_delta_of_deltas": same_diff_contrast,
                "n_receptors_same": len(same),
                "n_receptors_diff": len(diff),
            }
    summary["supplementary_per_arm_marginal_test"] = supp

    recon = build_recon_meta({
        "rows_csv": args.rows,
        "manifest_csv": args.manifest,
        "ref_set_csv": args.ref_set,
        **{f"ligand_set_{i}": p for i, p in enumerate(args.ligand_sets)},
    })
    output = {
        "reconstruction": {
            "reconstruction_script": __file__,
            **recon,
        },
        "task": "A_same_complex_split",
        "definition": (
            "same = ligand bound_pdb matches an active (agonist arm) / "
            "inactive_neutral_antagonist-preferred (antag arm) reference "
            "PDB; different = must-generalise. Interaction is 2x2 as in "
            "Stage 3a, cluster-bootstrap CI over receptors (5000 iter). "
            "Metrics: pocket_ca_rmsd_(active|inactive) primary; "
            "pocket_sidechain_rmsd_(active|inactive) secondary."
        ),
        "n_class_a_receptors_in_v2": len(class_a_receptors),
        "receptors": sorted(class_a_receptors),
        "split": split,
        "summary": summary,
        "cells_per_backbone": cells,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, default=str) + "\n")
    print("wrote", args.out)


if __name__ == "__main__":
    raise SystemExit(main() or 0)
