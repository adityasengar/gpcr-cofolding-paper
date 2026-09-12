#!/usr/bin/env python3
"""Task A v3 — chemotype composition check + honest framing.

Two follow-ups on Task A v2:

  (1) Composition check — do the recallable (n=15) and must-generalise
      (n=13) strata differ in chemotype (small-molecule vs peptide)?
      If recallable is >2 SDs heavier on small-molecules than
      must-generalise, the anti-memorisation signal could be a
      peptide-vs-small-mol confound. User pre-hypothesis: recallable
      9/6, must-generalise 6/7.

  (2) Honest framing — the observation is that the must-generalise
      stratum shows LARGER effect than recallable. No-memorisation
      predicts EQUAL. Memorisation predicts LARGER on RECALLABLE.
      Observing LARGER on must-generalise is directionally
      anti-memorisation but is not what physics predicts either. So we
      need the magnitude difference (must-gen minus recallable) with
      cluster-bootstrap CI, and a verdict for whether it is
      within-noise or significantly non-zero at n=13/15.
"""
from __future__ import annotations
import argparse, csv, json, math, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import (
    REPO, to_float, load_rows, load_ref_set, load_ligand_bound_pdbs,
    cluster_bootstrap_two_group_diff, _mean, git_sha, now_utc, sha256,
)


def _active_pdbs(refs):
    return {x["pdb_id"].strip().upper() for x in refs.get("active", [])
            if x.get("pdb_id")}


def _load_ligand_metadata(paths):
    """Combine ligand_set.csv + ligand_set_tier3.csv; per (receptor,
    ligand_role) row keep is_peptide, ligand_smiles, peptide_sequence,
    ligand_variant, ccd_code. Later files WIN (tier3 overrides base)."""
    out = {}
    for path in paths:
        with open(path) as f:
            for r in csv.DictReader(f):
                rec = r["receptor"].strip().upper()
                role = r["ligand_role"].strip().lower()
                if role != "full_agonist":
                    continue
                is_pep_raw = (r.get("is_peptide") or "").strip().upper()
                is_pep = is_pep_raw == "TRUE"
                smiles = (r.get("smiles") or "").strip()
                pep_seq = (r.get("peptide_sequence") or "").strip()
                ccd = (r.get("ccd_code") or "").strip()
                variant = (r.get("ligand_variant") or "").strip()
                # Skip empty/placeholder rows
                if not smiles and not pep_seq:
                    continue
                out[(rec, role)] = {
                    "is_peptide": is_pep,
                    "ligand_smiles": smiles,
                    "ligand_peptide_sequence": pep_seq,
                    "ccd_code": ccd,
                    "ligand_variant": variant,
                    "chemotype": "peptide" if is_pep else "small_mol",
                    "source_file": path.name,
                }
    return out


def _prop_diff_z(k_a, n_a, k_b, n_b):
    """Two-proportion z-test using pooled variance. Returns z-score
    for k_a/n_a > k_b/n_b (positive z = recallable heavier on smallmol
    when k = small_mol count)."""
    p_a = k_a / n_a if n_a else 0.0
    p_b = k_b / n_b if n_b else 0.0
    p_p = (k_a + k_b) / (n_a + n_b) if (n_a + n_b) else 0.0
    se = math.sqrt(p_p * (1 - p_p) * (1 / n_a + 1 / n_b)) if n_a and n_b else float("nan")
    if not se or math.isnan(se) or se == 0:
        return float("nan")
    return (p_a - p_b) / se


def main():
    ap = argparse.ArgumentParser()
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
    ap.add_argument("--task-a-v2", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/task_A_v2_agonist_vs_decoy_apo_same_complex.json")
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/task_A_v3_composition_check.json")
    args = ap.parse_args()

    rows = load_rows(args.rows, manifest_csv=args.manifest)
    ref_set = load_ref_set(args.ref_set)
    lig_pdbs = load_ligand_bound_pdbs(args.ligand_sets)
    lig_meta = _load_ligand_metadata(args.ligand_sets)

    # Reproduce Task A v2's stratum split — bound_pdb ∈ active_refs → recallable.
    # Restrict to Class A receptors with common agonist_apo + decoy_apo cells,
    # by intersecting with the receptor set that produced deltas in v2.
    with open(args.task_a_v2) as f:
        v2 = json.load(f)
    # v2 doesn't emit the receptor list per stratum. Re-derive from ref_set +
    # ligand_pdbs + observed rows.
    ag_receptors = set()
    dec_receptors = set()
    for r in rows:
        if str(r.get("passed", "")).lower() != "true":
            continue
        if (r.get("receptor_class") or "").upper() != "A":
            continue
        pt = (r.get("partner_type") or "").lower()
        role = (r.get("ligand_role") or "").strip()
        if pt != "apo":
            continue
        rec = (r.get("receptor_slug") or "").upper()
        if role == "full_agonist":
            ag_receptors.add(rec)
        elif role == "decoy_lig":
            dec_receptors.add(rec)
    common_recs = ag_receptors & dec_receptors

    recallable = []
    must_generalise = []
    for rec in sorted(common_recs):
        ag_pdb = lig_pdbs.get((rec, "full_agonist"), "")
        active_set = _active_pdbs(ref_set.get(rec, {}))
        if not ag_pdb or not active_set:
            continue
        if ag_pdb in active_set:
            recallable.append(rec)
        else:
            must_generalise.append(rec)

    # Compose the composition table
    def compose(names):
        smol = []
        pep = []
        missing = []
        for rec in names:
            meta = lig_meta.get((rec, "full_agonist"))
            if meta is None:
                missing.append(rec)
                continue
            (smol if not meta["is_peptide"] else pep).append({
                "receptor": rec,
                "ccd_code": meta.get("ccd_code", ""),
                "ligand_variant": meta.get("ligand_variant", ""),
                "smiles_head": (meta.get("ligand_smiles", "") or "")[:40],
                "peptide_seq_len": len(meta.get("ligand_peptide_sequence", "") or ""),
                "source_file": meta["source_file"],
            })
        return {"small_mol": smol, "peptide": pep, "missing_metadata": missing}

    comp_recallable = compose(recallable)
    comp_mustgen = compose(must_generalise)

    n_r_sm = len(comp_recallable["small_mol"])
    n_r_pep = len(comp_recallable["peptide"])
    n_m_sm = len(comp_mustgen["small_mol"])
    n_m_pep = len(comp_mustgen["peptide"])
    total_r = n_r_sm + n_r_pep
    total_m = n_m_sm + n_m_pep

    # Two-proportion z on P(small_mol) — positive z means recallable more small-mol
    z_smallmol = _prop_diff_z(n_r_sm, total_r, n_m_sm, total_m)

    # Confound verdict
    if math.isnan(z_smallmol):
        confound_verdict = "INDETERMINATE_INSUFFICIENT_DATA"
    elif abs(z_smallmol) >= 2.0:
        confound_verdict = "SEVERE_CONFOUND" if z_smallmol > 0 else "SEVERE_CONFOUND_INVERTED"
    elif abs(z_smallmol) >= 1.0:
        confound_verdict = "PARTIAL_CONFOUND"
    else:
        confound_verdict = "NO_CONFOUND"

    # Match against user pre-hypothesis (9 sm / 6 pep recallable; 6 sm / 7 pep must-gen)
    user_hypothesis_match = {
        "user_expected_recallable_smallmol_peptide": [9, 6],
        "user_expected_mustgen_smallmol_peptide": [6, 7],
        "observed_recallable_smallmol_peptide": [n_r_sm, n_r_pep],
        "observed_mustgen_smallmol_peptide": [n_m_sm, n_m_pep],
        "matches_user_hypothesis_exactly": (
            [n_r_sm, n_r_pep] == [9, 6]
            and [n_m_sm, n_m_pep] == [6, 7]
        ),
    }

    # ------------------------------------------------------------------
    # Magnitude-difference framing: rebuild the per-receptor per-backbone
    # delta arrays and bootstrap (must_gen − recallable) magnitude
    # ------------------------------------------------------------------
    from lib_common import to_float as _tf
    per_bb = defaultdict(lambda: {
        "ca": {"ag": defaultdict(list), "dec": defaultdict(list)},
        "sc": {"ag": defaultdict(list), "dec": defaultdict(list)},
    })
    for r in rows:
        if str(r.get("passed", "")).lower() != "true":
            continue
        if (r.get("receptor_class") or "").upper() != "A":
            continue
        rec = (r.get("receptor_slug") or "").upper()
        bb = (r.get("backbone") or "").lower()
        if not bb:
            continue
        role = (r.get("ligand_role") or "").strip()
        pt = (r.get("partner_type") or "").lower()
        if pt != "apo":
            continue
        if role == "full_agonist":
            grp = "ag"
        elif role == "decoy_lig":
            grp = "dec"
        else:
            continue
        pca = _tf(r.get("pocket_ca_rmsd_active"))
        psc = _tf(r.get("pocket_sidechain_rmsd_active"))
        if not math.isnan(pca):
            per_bb[bb]["ca"][grp][rec].append(pca)
        if not math.isnan(psc):
            per_bb[bb]["sc"][grp][rec].append(psc)

    magnitude_diff = {}
    for bb in ("boltz", "chai", "of3", "protenix"):
        d = per_bb[bb]
        bb_out = {}
        for axis, pretty in (("ca", "pocket_ca_rmsd_active"),
                             ("sc", "pocket_sidechain_rmsd_active")):
            ag = d[axis]["ag"]
            dec = d[axis]["dec"]
            recall_delta = {}
            mustgen_delta = {}
            for rec in sorted(set(ag) & set(dec)):
                delta = _mean(ag[rec]) - _mean(dec[rec])
                if math.isnan(delta):
                    continue
                if rec in set(recallable):
                    recall_delta[rec] = [delta]
                elif rec in set(must_generalise):
                    mustgen_delta[rec] = [delta]

            # Signed delta comparison: bootstrap (must_gen_group_mean
            # − recallable_group_mean) on signed per-receptor deltas.
            # Both groups' point estimates are expected to be negative
            # under anti-memorisation. If (must_gen − recallable) CI is
            # entirely NEGATIVE, must_gen is MORE NEGATIVE (larger
            # magnitude effect). If entirely POSITIVE, recallable is
            # more negative. Note: this is the sign-flipped mirror of
            # v2's `same_minus_diff_of_deltas` (which was recallable −
            # must_gen).
            mag_stat = cluster_bootstrap_two_group_diff(
                mustgen_delta, recall_delta, seed=hash((bb, axis)) % 65536
            )
            # Verdict per (backbone × axis) — anti-memorisation frame:
            # est < 0 → must_gen MORE negative (larger magnitude).
            if mag_stat["signed_nonzero"]:
                if mag_stat["est"] < 0:
                    verdict = "MUST_GEN_SIGNIFICANTLY_LARGER"
                else:
                    verdict = "RECALLABLE_SIGNIFICANTLY_LARGER"
            else:
                if abs(mag_stat["est"]) > 0.001:
                    if mag_stat["est"] < 0:
                        verdict = "MUST_GEN_LARGER_WITHIN_NOISE"
                    else:
                        verdict = "RECALLABLE_LARGER_WITHIN_NOISE"
                else:
                    verdict = "WITHIN_NOISE"
            bb_out[pretty] = {
                "mustgen_minus_recallable_signed_delta_A": mag_stat,
                "n_receptors_recall": len(recall_delta),
                "n_receptors_mustgen": len(mustgen_delta),
                "verdict": verdict,
                "direction_note": (
                    "SIGNED delta = mean(agonist_apo pocket_rmsd_active) "
                    "− mean(decoy_apo pocket_rmsd_active) per receptor. "
                    "Both group means expected negative under anti-mem. "
                    "(must_gen − recallable) < 0 => must_gen more negative "
                    "=> larger anti-memorisation effect on must-generalise. "
                    "This is the sign-flipped mirror of v2's "
                    "`same_minus_diff_of_deltas`."
                ),
            }
        magnitude_diff[bb] = bb_out

    out = {
        "task": "A_v3_composition_check_and_honest_framing",
        "reconstruction": {
            "reconstruction_script": str(Path(__file__).resolve()),
            "reconstruction_script_git_sha": git_sha(),
            "generated_at_utc": now_utc(),
            "inputs": {
                "rows_csv": {"path": str(args.rows), "sha256": sha256(args.rows)},
                "manifest_csv": {"path": str(args.manifest), "sha256": sha256(args.manifest)},
                "ref_set_csv": {"path": str(args.ref_set), "sha256": sha256(args.ref_set)},
                "ligand_set_0": {"path": str(args.ligand_sets[0]), "sha256": sha256(args.ligand_sets[0])},
                "ligand_set_1": {"path": str(args.ligand_sets[1]), "sha256": sha256(args.ligand_sets[1])},
                "task_a_v2_json": {"path": str(args.task_a_v2), "sha256": sha256(args.task_a_v2)},
            },
        },
        "strata": {
            "recallable_receptors": sorted(recallable),
            "must_generalise_receptors": sorted(must_generalise),
            "n_recallable": len(recallable),
            "n_must_generalise": len(must_generalise),
        },
        "composition_table": {
            "recallable": {
                "small_mol": len(comp_recallable["small_mol"]),
                "peptide": len(comp_recallable["peptide"]),
            },
            "must_generalise": {
                "small_mol": len(comp_mustgen["small_mol"]),
                "peptide": len(comp_mustgen["peptide"]),
            },
        },
        "composition_detail": {
            "recallable": comp_recallable,
            "must_generalise": comp_mustgen,
        },
        "chemotype_confound_test": {
            "definition": (
                "Two-proportion z-test on P(small_mol). Positive z = "
                "recallable stratum is more small-molecule-heavy than "
                "must-generalise. |z| >= 2.0 -> SEVERE_CONFOUND. "
                "|z| >= 1.0 -> PARTIAL_CONFOUND. |z| < 1.0 -> NO_CONFOUND."
            ),
            "z_smallmol_recallable_minus_mustgen": z_smallmol,
            "p_smallmol_recallable": (n_r_sm / total_r) if total_r else None,
            "p_smallmol_mustgen": (n_m_sm / total_m) if total_m else None,
            "verdict": confound_verdict,
            "user_hypothesis_check": user_hypothesis_match,
        },
        "honest_framing": {
            "no_memorisation_predicts": "EQUAL discrimination on recallable vs must-generalise",
            "memorisation_predicts": "LARGER on RECALLABLE",
            "observed_direction_v2": "LARGER on MUST_GENERALISE for 6 of 8 tests (CA: 4/4; SC: 2/4)",
            "interpretation": (
                "Must-gen-larger is directionally anti-memorisation but is "
                "NOT what a physics-only-null predicts. At n=13/15 per "
                "stratum, the magnitude difference must be bootstrapped to "
                "state whether it is within-noise or significantly non-zero. "
                "The magnitude_difference_bootstrap block below tests each "
                "(backbone x axis) cell."
            ),
            "magnitude_difference_bootstrap": magnitude_diff,
            "summary_verdicts_per_backbone_ca_axis": {
                bb: magnitude_diff[bb]["pocket_ca_rmsd_active"]["verdict"]
                for bb in magnitude_diff
            },
            "summary_verdicts_per_backbone_sc_axis": {
                bb: magnitude_diff[bb]["pocket_sidechain_rmsd_active"]["verdict"]
                for bb in magnitude_diff
            },
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {args.out}")
    print(f"Composition: recallable {n_r_sm}sm/{n_r_pep}pep, "
          f"must-gen {n_m_sm}sm/{n_m_pep}pep, z={z_smallmol:.3f}, "
          f"verdict={confound_verdict}")
    print("Magnitude verdicts (CA axis):")
    for bb in ("boltz", "chai", "of3", "protenix"):
        v = magnitude_diff[bb]["pocket_ca_rmsd_active"]
        m = v["mustgen_minus_recallable_signed_delta_A"]
        print(f"  {bb:<10} mustgen-recall signed = {m['est']:+.3f} A "
              f"CI [{m['ci_lo']:+.3f}, {m['ci_hi']:+.3f}]  {v['verdict']}")


if __name__ == "__main__":
    main()
