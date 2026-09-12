#!/usr/bin/env python3
"""Task B — relabel Stage 3c as UNINFORMATIVE_BOTH_DIRECTIONS and
account for the 16-receptor dropout (panel of 38 Class-A vs n=22 in
the correlation).

Recall plausibly saturates at ~1 deposited complex per receptor per
state; the absence of a dose-response is uninformative in both
directions."""
from __future__ import annotations
import argparse, csv, json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import REPO, build_recon_meta, load_rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v1", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/stage3_effect_size_vs_deposition_count.json")
    ap.add_argument("--rows", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rows.tier3.v2.csv")
    ap.add_argument("--manifest", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rescore_manifest.tier3.v2.csv")
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/stage3c_v2_relabeled.json")
    args = ap.parse_args()

    with args.v1.open() as f:
        prior = json.load(f)
    rows = load_rows(args.rows, manifest_csv=args.manifest)

    # Reconstruct the 3c pool: Class-A, cognate arm, full_agonist OR
    # neutral_antagonist/inverse_agonist, non-NaN pocket_ca_rmsd_active.
    per_receptor_ag = {}
    per_receptor_an = {}
    class_a_all = set()
    for r in rows:
        if str(r.get("passed", "")).lower() != "true":
            continue
        if (r.get("receptor_class") or "").upper() != "A":
            continue
        rec = (r.get("receptor_slug") or "").upper()
        class_a_all.add(rec)
        pt = (r.get("partner_type") or "").lower()
        if pt not in ("cognate", "g_alpha"):
            continue
        v = r.get("pocket_ca_rmsd_active")
        try:
            fv = float(v)
        except (ValueError, TypeError):
            continue
        if math.isnan(fv):
            continue
        role = (r.get("ligand_role") or "").strip()
        if role == "full_agonist":
            per_receptor_ag.setdefault(rec, []).append(fv)
        elif role in ("neutral_antagonist", "inverse_agonist"):
            per_receptor_an.setdefault(rec, []).append(fv)

    receptors_with_both_arms = set(per_receptor_ag) & set(per_receptor_an)

    # deposition counts are keyed in prior JSON at top-level "deposition_counts"
    dep_counts = prior.get("deposition_counts", {})

    # 22 receptors used in v1 — the ones with both arms AND deposition count
    used_receptors = {p["receptor"] for p in prior["per_backbone"]["boltz"]["pairs"]}
    n_class_a = len(class_a_all)

    # Panel accounting: 40 Class-A panel per PREREG (8 sealed removed). Tier 3
    # v2 has 36 Class-A receptors present. Of those, 22 have both arms of
    # scored data + valid deposition count.
    #
    # Reasons per receptor for exclusion:
    dropped = {}
    for rec in sorted(class_a_all):
        has_ag = rec in per_receptor_ag
        has_an = rec in per_receptor_an
        has_dep = rec in dep_counts and dep_counts[rec] > 0
        reasons = []
        if not has_ag:
            reasons.append("no_full_agonist_cognate_pocket_data")
        if not has_an:
            reasons.append("no_antag_cognate_pocket_data")
        if not has_dep:
            reasons.append("no_deposition_count_in_reference_set")
        if reasons:
            dropped[rec] = reasons

    # Peek at prior verdict fields
    per_bb_relabeled = {}
    for bb, v in prior.get("per_backbone", {}).items():
        rr = v.get("pearson_r", float("nan"))
        pv = v.get("p_two_tailed_normal_approx", float("nan"))
        n = v.get("n_receptors", 0)
        per_bb_relabeled[bb] = {
            "n_receptors": n,
            "pearson_r": rr,
            "p_two_tailed_normal_approx": pv,
            "old_verdict_in_v1": (
                "Result contradicts the recall interpretation "
                "(no positive r)"
            ),
            "new_verdict": "UNINFORMATIVE_BOTH_DIRECTIONS",
            "new_verdict_rationale": (
                "Recall plausibly saturates at one deposited complex "
                "per receptor per state; fifty entries are not fifty "
                "times more memorizable than one. Absence of a "
                "log10(n_deposited) dose-response neither supports nor "
                "refutes recall — it is uninformative in both "
                "directions."
            ),
        }

    payload = {
        "task": "B_relabel_stage3c",
        "reconstruction": {
            "reconstruction_script": __file__,
            **build_recon_meta({
                "prior_v1_json": args.v1,
                "rows_csv": args.rows,
                "manifest_csv": args.manifest,
            }),
        },
        "panel_accounting": {
            "panel_class_a_per_prereg": (
                "40 Class-A receptors (48-panel per PREREG §1 minus 4 "
                "Class B minus 4 Class F)."
            ),
            "sealed_removed_from_reference_set": (
                "8 receptors — ACM1, ADA2A, ADRB1, CCKAR, DRD3, EDNRA, "
                "HRH3, OX2R — moved to sealed_active_refs_2026_09_01.csv "
                "per PREREG §14. They have NO 'active' role rows in "
                "refs/reference_set.csv, so their deposition_count "
                "proxy (n(active)+n(inactive)) is 0 or based only on "
                "the inactive side."
            ),
            "n_class_a_receptors_in_tier3_v2_rows": len(class_a_all),
            "n_class_a_receptors_with_both_arms": len(receptors_with_both_arms),
            "n_receptors_in_v1_correlation": prior["per_backbone"]["boltz"].get("n_receptors", 0),
        },
        "receptors_class_a_in_v2": sorted(class_a_all),
        "receptors_included_in_v1_correlation": sorted(used_receptors),
        "receptors_excluded_from_v1_correlation": {
            "count": len(class_a_all - used_receptors),
            "per_receptor_reason": {
                rec: dropped[rec] if rec in dropped
                     else ["reason_not_diagnosed"]
                for rec in sorted(class_a_all - used_receptors)
            },
        },
        "per_backbone_relabeled": per_bb_relabeled,
        "note_saturation_argument": (
            "Recall plausibly saturates at one deposited complex per "
            "receptor per state, so absence of a dose-response is not "
            "evidence against recall."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print("wrote", args.out)


if __name__ == "__main__":
    raise SystemExit(main() or 0)
