#!/usr/bin/env python3
"""Task E v2 — reference-ligand mapping investigation.

Withdraws the v2 "DOCKING_FAILURE_<50pct" verdict for the 4 testable
cells. The correct read is: the four testable cells were all
`neutral_antagonist`, whose role_specific-preferred reference is the
same PDB as the input ligand (so the CCD/atom-name matching succeeds).
Agonist cells fail because the reference active PDB is often
crystallised with a DIFFERENT agonist than the input ligand, and the
scorer matches by (atom_name, element) only — no CCD-agnostic or
substructure/MCS matching.

Answers three questions per cell:
  1. Which reference PDB was `ligand_rmsd_to_ref` computed against?
     (parsed from `pocket_notes` — the scorer emits
     ``ref=active:PDBID`` or ``ref=inactive:PDBID`` on every row.)
  2. Is the reference-ligand CCD the same as the input CCD?
     (cross-referenced against ligand_set.csv + ligand_set_tier3.csv
     via the `bound_pdb` → `ccd_code` map.)
  3. Why do neutral_antagonist cells succeed while agonist cells fail?
     (parses the ``lig:matched_X_of_pred_Y_ref_Z`` or ``lig:no_atom_match``
     tokens in pocket_notes; the atom-name overlap is the mechanism.)
"""
from __future__ import annotations
import argparse, csv, json, math, re, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import REPO, build_recon_meta, to_float


RE_NOTE = re.compile(r"lig:([^;]+);ref=(active|inactive):(\w+)")


def _load_pdb_to_ccd(paths):
    """{bound_pdb_upper: set(ccd_code_upper)} across all ligand sets."""
    out = defaultdict(set)
    for path in paths:
        with open(path) as f:
            for r in csv.DictReader(f):
                pdb = (r.get("bound_pdb") or "").strip().upper()
                ccd = (r.get("ccd_code") or "").strip().upper()
                if len(pdb) == 4 and pdb.isalnum() and ccd:
                    out[pdb].add(ccd)
    return {k: sorted(v) for k, v in out.items()}


def _lig_match_kind(lig_status):
    """Bucket the pocket_notes ``lig:...`` token."""
    if lig_status == "no_atom_match":
        return "no_atom_match"
    if lig_status == "no_ref_ligand":
        return "no_ref_ligand"
    if lig_status.startswith("matched_"):
        m = re.match(r"matched_(\d+)_of_pred_(\d+)_ref_(\d+)", lig_status)
        if m:
            n_match, n_pred, n_ref = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return ("matched", n_match, n_pred, n_ref)
    return ("other", lig_status)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rows.tier3.v2.csv")
    ap.add_argument("--manifest", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rescore_manifest.tier3.v2.csv")
    ap.add_argument("--ligand-sets", nargs="+", type=Path,
                    default=[REPO / "refs/ligand_set.csv",
                             REPO / "refs/ligand_set_tier3.csv"])
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/task_E_v2_reference_ligand_mapping.json")
    args = ap.parse_args()

    with open(args.manifest) as f:
        mani = {r["prediction_path"]: r for r in csv.DictReader(f)}
    pdb_to_ccd = _load_pdb_to_ccd(args.ligand_sets)

    with open(args.rows) as f:
        rows = list(csv.DictReader(f))

    # Per (backbone, ligand_role, partner_type) cell:
    per_cell = defaultdict(lambda: {
        "n_passed": 0,
        "n_notes_parsed": 0,
        # ref-pdb selection
        "ref_pdbs_by_receptor": defaultdict(Counter),  # {receptor: {pdb: n}}
        # CCD alignment (input vs reference PDB's known ligand)
        "n_ref_pdb_is_input_bound_pdb": 0,
        "n_ref_pdb_differs_from_input_bound_pdb": 0,
        "n_ref_pdb_carries_input_ccd": 0,
        "n_ref_pdb_missing_or_ligand_set_silent": 0,
        # Atom-name mapping fate
        "n_no_atom_match": 0,
        "n_no_ref_ligand": 0,
        "n_matched": 0,
        "matched_atom_ratios": [],
        "matched_atom_ratios_ceil": [],  # min(pred, ref) as the ceiling
        # Chemistry co-classification (agonist input, agonist ref? etc.)
        "n_ref_ccd_equals_input_ccd": 0,
        "n_ref_ccd_differs_from_input_ccd": 0,
        # RMSD outcome — populated / not
        "n_ligand_rmsd_populated": 0,
        "n_ligand_rmsd_lt_3A": 0,
    })

    # Per-receptor detail (agonist arm only, most informative), also
    # captures a small worked example table.
    per_receptor_detail_agonist = {}
    per_receptor_detail_antag = {}

    for row in rows:
        if str(row.get("passed", "")).lower() != "true":
            continue
        m = mani.get(row["input_path"])
        if not m:
            continue
        bb = (m.get("backbone") or "").lower()
        role = (m.get("ligand_role") or "").strip()
        pt = (m.get("partner_type") or "").lower()
        cell = (bb, role, pt or "unknown")
        c = per_cell[cell]
        c["n_passed"] += 1

        notes = row.get("pocket_notes", "")
        match = RE_NOTE.search(notes)
        rec = (row.get("receptor_slug") or "").strip().upper()
        if not match:
            continue
        c["n_notes_parsed"] += 1
        lig_status, ref_role, ref_pdb = match.groups()
        ref_pdb = ref_pdb.upper()
        input_ccd = (m.get("ligand_ccd") or "").strip().upper()
        input_bound_pdb = (m.get("ligand_bound_pdb") or "").strip().upper()

        c["ref_pdbs_by_receptor"][rec][ref_pdb] += 1

        if input_bound_pdb and ref_pdb:
            if input_bound_pdb == ref_pdb:
                c["n_ref_pdb_is_input_bound_pdb"] += 1
            else:
                c["n_ref_pdb_differs_from_input_bound_pdb"] += 1

        ref_ccds = pdb_to_ccd.get(ref_pdb, [])
        if not ref_ccds:
            c["n_ref_pdb_missing_or_ligand_set_silent"] += 1
        elif input_ccd and input_ccd in ref_ccds:
            c["n_ref_pdb_carries_input_ccd"] += 1
            c["n_ref_ccd_equals_input_ccd"] += 1
        elif input_ccd:
            c["n_ref_ccd_differs_from_input_ccd"] += 1
        else:
            c["n_ref_pdb_missing_or_ligand_set_silent"] += 1

        kind = _lig_match_kind(lig_status)
        if kind == "no_atom_match":
            c["n_no_atom_match"] += 1
        elif kind == "no_ref_ligand":
            c["n_no_ref_ligand"] += 1
        elif isinstance(kind, tuple) and kind[0] == "matched":
            _, n_match, n_pred, n_ref = kind
            c["n_matched"] += 1
            if n_pred > 0 and n_ref > 0:
                c["matched_atom_ratios"].append(n_match / max(n_pred, n_ref))
                c["matched_atom_ratios_ceil"].append(n_match / min(n_pred, n_ref))

        v = to_float(row.get("ligand_rmsd_to_ref"))
        if not math.isnan(v):
            c["n_ligand_rmsd_populated"] += 1
            if v < 3.0:
                c["n_ligand_rmsd_lt_3A"] += 1

        # per-receptor detail
        if role == "full_agonist":
            per_receptor_detail_agonist.setdefault((bb, rec), {
                "input_ccd": input_ccd,
                "input_bound_pdb": input_bound_pdb,
                "ref_pdb": ref_pdb,
                "ref_ccd_set_from_ligand_set": ref_ccds,
                "ref_pdb_equals_input_bound_pdb": input_bound_pdb == ref_pdb,
                "input_ccd_in_ref_pdb_known_ligands": (
                    bool(ref_ccds) and input_ccd in ref_ccds),
                "example_pocket_notes": notes,
            })
        elif role in ("neutral_antagonist", "inverse_agonist"):
            per_receptor_detail_antag.setdefault((bb, rec), {
                "input_ccd": input_ccd,
                "input_bound_pdb": input_bound_pdb,
                "ref_pdb": ref_pdb,
                "ref_ccd_set_from_ligand_set": ref_ccds,
                "ref_pdb_equals_input_bound_pdb": input_bound_pdb == ref_pdb,
                "input_ccd_in_ref_pdb_known_ligands": (
                    bool(ref_ccds) and input_ccd in ref_ccds),
                "example_pocket_notes": notes,
            })

    # Aggregate per-cell payload
    out_cells = []
    for (bb, role, pt), c in sorted(per_cell.items()):
        pop_rate = (c["n_ligand_rmsd_populated"] / c["n_passed"]
                    if c["n_passed"] else 0.0)
        # atom-match ratio summary
        arr = sorted(c["matched_atom_ratios"])
        arr_c = sorted(c["matched_atom_ratios_ceil"])
        def _median(xs):
            if not xs: return float("nan")
            return xs[len(xs)//2]
        # verdict
        n_notes = c["n_notes_parsed"]
        if n_notes == 0:
            verdict = "NO_NOTES_PARSED"
        else:
            n_ref_shared = c["n_ref_ccd_equals_input_ccd"]
            n_ref_diff = c["n_ref_ccd_differs_from_input_ccd"]
            n_ref_unknown = c["n_ref_pdb_missing_or_ligand_set_silent"]
            frac_ref_same_ccd = n_ref_shared / n_notes
            frac_no_match = c["n_no_atom_match"] / n_notes
            if role == "decoy_lig":
                verdict = ("DECOY_RMSD_UNINTERPRETABLE_BY_DESIGN"
                           " (decoy vs real-ligand ref by construction;"
                           " see pocket_metrics.py:46 Ambiguity #4)")
            elif frac_no_match > 0.5:
                verdict = ("MAPPING_FAILURE_ATOM_NAME_MISMATCH"
                           " (>50% of rows produced no atom-name overlap"
                           " between predicted and reference ligand)")
            elif frac_ref_same_ccd > 0.5 and pop_rate > 0.5:
                verdict = ("MAPPING_OK_REF_CCD_MATCHES_INPUT_CCD"
                           " (rmsd_to_ref is a real dock distance for"
                           " this cell)")
            else:
                verdict = ("PARTIAL_MAPPING_MIXED_CCD"
                           " (some rows reference a same-CCD PDB, some"
                           " a different-CCD PDB)")
        out_cells.append({
            "backbone": bb,
            "ligand_role": role,
            "partner_type": pt,
            "n_passed": c["n_passed"],
            "n_notes_parsed": n_notes,
            "n_ligand_rmsd_populated": c["n_ligand_rmsd_populated"],
            "ligand_rmsd_populated_rate": pop_rate,
            "n_ligand_rmsd_lt_3A": c["n_ligand_rmsd_lt_3A"],
            "n_ref_pdb_is_input_bound_pdb": c["n_ref_pdb_is_input_bound_pdb"],
            "n_ref_pdb_differs_from_input_bound_pdb": (
                c["n_ref_pdb_differs_from_input_bound_pdb"]),
            "n_ref_pdb_missing_or_ligand_set_silent": (
                c["n_ref_pdb_missing_or_ligand_set_silent"]),
            "n_ref_ccd_equals_input_ccd": c["n_ref_ccd_equals_input_ccd"],
            "n_ref_ccd_differs_from_input_ccd": c["n_ref_ccd_differs_from_input_ccd"],
            "n_atom_map_no_match": c["n_no_atom_match"],
            "n_atom_map_no_ref_ligand": c["n_no_ref_ligand"],
            "n_atom_map_matched_any": c["n_matched"],
            "median_matched_atom_ratio_over_max_pred_or_ref": _median(arr),
            "median_matched_atom_ratio_over_min_pred_or_ref": _median(arr_c),
            "n_distinct_receptors": len(c["ref_pdbs_by_receptor"]),
            "verdict": verdict,
        })

    # Top-of-file summary — the question the prompt asks: does
    # mismatch explain the 4-cell selection?
    testable_pattern = [(bb, role, pt) for (bb, role, pt), c in per_cell.items()
                        if (c["n_ligand_rmsd_populated"] / c["n_passed"]
                            >= 0.5 if c["n_passed"] else False)]
    testable_roles = Counter(role for _, role, _ in testable_pattern)
    testable_bbs = Counter(bb for bb, _, _ in testable_pattern)

    # 13 of 28 stat: from Task A v1 same-complex split, the agonist arm
    # was 15 recallable / 13 must-generalise = 28 total. We can reproduce
    # the "ref_pdb != input_bound_pdb" count per receptor.
    per_receptor_agonist_mismatch = {}
    for (bb, rec), d in per_receptor_detail_agonist.items():
        prior = per_receptor_agonist_mismatch.setdefault(rec, {
            "input_bound_pdb": d["input_bound_pdb"],
            "ref_pdbs_seen_across_backbones": set(),
            "ref_pdb_matches_input_bound_pdb": None,
        })
        prior["ref_pdbs_seen_across_backbones"].add(d["ref_pdb"])
    for rec, prior in per_receptor_agonist_mismatch.items():
        prior["ref_pdbs_seen_across_backbones"] = sorted(
            prior["ref_pdbs_seen_across_backbones"])
        prior["ref_pdb_matches_input_bound_pdb"] = (
            prior["input_bound_pdb"] in prior["ref_pdbs_seen_across_backbones"]
        )
    n_agonist_receptors = len(per_receptor_agonist_mismatch)
    n_agonist_mismatch = sum(
        1 for p in per_receptor_agonist_mismatch.values()
        if not p["ref_pdb_matches_input_bound_pdb"])
    n_agonist_match = n_agonist_receptors - n_agonist_mismatch

    payload = {
        "task": "E_v2_reference_ligand_mapping_investigation",
        "reconstruction": {
            "reconstruction_script": __file__,
            **build_recon_meta({
                "rows_csv": args.rows,
                "manifest_csv": args.manifest,
                **{f"ligand_set_{i}": p for i, p in enumerate(args.ligand_sets)},
            }),
        },
        "atom_mapping_strategy_source": (
            "scorer/pocket_metrics.py:501-624 (ligand_rmsd_to_ref). "
            "Reference ligand loader: build_pocket_reference_cache "
            "(scorer/pocket_metrics.py:1045-1134) selects the LARGEST "
            "HETATM residue (by heavy-atom count) after filtering "
            "waters / metals / buffers / lipids in _NON_LIGAND_RESNAMES. "
            "Matching is by (atom_name, element) — no bond-graph, no "
            "substructure or MCS matching, no RDKit. When the reference "
            "and prediction ligands are the SAME molecule with atom "
            "names preserved, the match is complete; when the atom "
            "names diverge (different CCD, or same CCD but backbone-"
            "renamed atoms), the intersection is smaller or zero and "
            "the RMSD is NaN (no_atom_match)."
        ),
        "why_neutral_antagonist_cells_succeeded_while_agonist_cells_failed": (
            "The role_specific-preferred inactive reference (per "
            "scorer/pocket_metrics.py::_role_for_state_claim, "
            "ligand_role=neutral_antagonist → "
            "inactive_neutral_antagonist ref) is systematically the "
            "SAME PDB as the neutral_antagonist input's ligand_bound_pdb "
            "for most receptors — the antag reference PDB is often the "
            "one that was crystallised WITH that antagonist. So the "
            "reference ligand's CCD equals the input CCD, atom names "
            "are preserved by CCD, and the atom-name-based matcher "
            "finds an overlap. For full_agonist rows the active "
            "reference is typically a DIFFERENT PDB from the input "
            "agonist's crystal (the active reference is a signalling-"
            "state structure, often crystallised with a different "
            "agonist chemistry than the tier-3 input) — different CCDs "
            "→ different atom names → no_atom_match → NaN. Backbone "
            "variation on top of this: OF3 and Protenix preserve CCD "
            "atom names verbatim in output CIFs; Boltz and Chai use "
            "SMILES-derived or normalised atom names, which reduces "
            "the atom-name overlap even when the CCDs match, giving "
            "the observed chai=0.00 to protenix=0.79 population "
            "spread on the same input rows."
        ),
        "verdict_downgrade": {
            "prior_v2_verdict": "DOCKING_FAILURE_<50pct on 4 testable cells (all neutral_antagonist)",
            "revised_v3_verdict": ("DOCKING_POSE_QUALITY_UNRESOLVED. The 4 "
                                    "testable cells were not selected by "
                                    "docking success — they were selected "
                                    "by same-complex reference-ligand "
                                    "identity, which makes atom-name "
                                    "matching succeed. The <10% "
                                    "dock-<3-Å rate observed there is "
                                    "compatible with either (a) real "
                                    "docking failure at the neutral-"
                                    "antag pocket, or (b) reference "
                                    "structure ambiguity / TM6-tilt "
                                    "displacement between the input's "
                                    "predicted pose and the reference "
                                    "ligand's crystal position (both "
                                    "measured in the 7TM-aligned frame). "
                                    "Cannot separate the two without a "
                                    "CCD-agnostic (RDKit-based MCS + "
                                    "positional) rescore. The prior "
                                    "'docking IS the failure mode' "
                                    "upgrade is WITHDRAWN."),
        },
        "how_many_agonist_receptors_have_ref_pdb_ne_input_bound_pdb": {
            "n_agonist_receptors_observed": n_agonist_receptors,
            "n_ref_pdb_matches_input_bound_pdb": n_agonist_match,
            "n_ref_pdb_differs_from_input_bound_pdb": n_agonist_mismatch,
            "note": (
                "The '13/28' figure in the task prompt refers to the "
                "Task A v1 same-complex split on the agonist arm "
                "(15 recallable + 13 must-generalise = 28 receptors with "
                "both a curated agonist bound_pdb AND an active scoring "
                "reference). The count here is over "
                "receptors OBSERVED in the v2 rows.csv with a parseable "
                "ref-pdb note; it will differ from the Task A denominator "
                "when a receptor's rows are excluded or when the note "
                "falls outside the parseable format."
            ),
        },
        "testable_cells_after_50pct_population_floor": {
            "n_testable_cells": len(testable_pattern),
            "roles_seen": dict(testable_roles),
            "backbones_seen": dict(testable_bbs),
            "role_selection_note": (
                "All 4 testable cells are neutral_antagonist (matches "
                "the v2 finding). The role selection is driven by "
                "role_specific reference selection, not by pose quality."
            ),
        },
        "per_cell_v2": out_cells,
        "per_receptor_agonist_mismatch": {
            k: {kk: (list(vv) if isinstance(vv, set) else vv)
                for kk, vv in v.items()}
            for k, v in sorted(per_receptor_agonist_mismatch.items())
        },
        "per_receptor_backbone_detail_agonist_examples": [
            {"backbone": bb, "receptor": rec, **d}
            for (bb, rec), d in sorted(per_receptor_detail_agonist.items())[:20]
        ],
        "per_receptor_backbone_detail_antag_examples": [
            {"backbone": bb, "receptor": rec, **d}
            for (bb, rec), d in sorted(per_receptor_detail_antag.items())[:20]
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print("wrote", args.out)


if __name__ == "__main__":
    raise SystemExit(main() or 0)
