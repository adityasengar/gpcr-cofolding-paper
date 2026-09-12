#!/usr/bin/env python3
"""Task C — verify + document the ligand-present receipt predicate.

Reads scorer/post_run_receipts.py, states plainly what it checks, and
runs a LOCAL PROXY census of ligand-presence signal from the v2 rows
(the CIFs live on HPC scratch and are not available here). The proxy
uses `ligand_rmsd_to_ref` populated + `pocket_ca_rmsd_active`
populated as an indirect signal that a ligand chain was parseable and
scoreable in the output CIF."""
from __future__ import annotations
import argparse, csv, json, math, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import REPO, build_recon_meta, load_rows


PREDICATE_DESCRIPTION = (
    "scorer/post_run_receipts.py::check_ligand_present GATES on "
    "_manifest_declared_ligand(row) — a row qualifies iff "
    "ligand_type in {peptide, small_molecule} OR ligand_smiles is "
    "non-empty OR ligand_sequence is non-empty. When gated, the "
    "receipt PARSES THE OUTPUT CIF (via gemmi) and counts non-buffer "
    "HETATM heavy atoms — for a small_molecule / SMILES-declared row, "
    "raises ALigandPresence when n_heavy == 0; for a peptide-declared "
    "row, counts standard-AA residues on chains other than the receptor "
    "chain and raises when that count == 0. \n\n"
    "This is OPTION (b) partial per the task spec — the receipt DOES "
    "physically parse the output CIF and count atoms; it is NOT "
    "tautological. HOWEVER, the threshold is n_heavy >= 1 (a floor), "
    "not n_heavy ≈ expected. A ligand whose SMILES expects 25 heavy "
    "atoms but whose CIF only writes 1 non-buffer HETATM heavy atom "
    "would PASS this receipt — it detects the Chai silent-apo shape "
    "(zero atoms) but not a 'ligand present but severely mis-modeled' "
    "shape. The 100.00% ligand_present_rate across all 24 cells means "
    "no row hit n_heavy == 0 — it does NOT mean every ligand was "
    "atomistically complete."
)


def local_proxy_census(rows):
    """Use scorer output columns as an indirect proxy for the
    strengthened receipt. The proxy signals a ligand was ACTUALLY
    present + scoreable in the CIF when the row has:
      - ligand_rmsd_to_ref populated (requires ligand atoms + a
        reference ligand), OR
      - pocket_ca_rmsd_active populated (requires receptor + ligand
        both parseable, since pocket is defined by contact with ligand)

    Note: pocket_ca_rmsd_active is populated for essentially every
    passed row (the pocket is defined from the *reference* structure's
    ligand contacts, not the sample's), so it is NOT a discriminating
    proxy for ligand presence. `ligand_rmsd_to_ref` requires a
    reference ligand and a sample ligand — a much stronger proxy.
    """
    per_cell_tot = defaultdict(int)
    per_cell_lig_rmsd_have = defaultdict(int)
    per_cell_manifest_declared = defaultdict(int)
    for r in rows:
        if str(r.get("passed", "")).lower() != "true":
            continue
        bb = (r.get("backbone") or "").lower()
        role = (r.get("ligand_role") or "").strip()
        pt = (r.get("partner_type") or "").lower()
        # cell key
        cell = (bb, role, pt or "unknown")
        per_cell_tot[cell] += 1
        # manifest-declared ligand
        ltype = (r.get("ligand_type") or "").strip().lower()
        smi = (r.get("ligand_smiles") or "").strip()
        seq = (r.get("ligand_sequence") or "").strip()
        manifest_declared = (
            (ltype and ltype not in ("", "none", "apo"))
            or bool(smi) or bool(seq)
        )
        if manifest_declared:
            per_cell_manifest_declared[cell] += 1
        # ligand_rmsd_to_ref populated?
        v = r.get("ligand_rmsd_to_ref")
        try:
            fv = float(v)
            if not math.isnan(fv):
                per_cell_lig_rmsd_have[cell] += 1
        except (ValueError, TypeError):
            pass
    out = []
    for cell, n in sorted(per_cell_tot.items()):
        n_dec = per_cell_manifest_declared.get(cell, 0)
        n_rmsd = per_cell_lig_rmsd_have.get(cell, 0)
        out.append({
            "backbone": cell[0],
            "ligand_role": cell[1],
            "partner_type": cell[2],
            "n_passed_rows": n,
            "n_manifest_declared_ligand": n_dec,
            "n_ligand_rmsd_to_ref_populated": n_rmsd,
            "manifest_declared_rate": n_dec / n if n else float("nan"),
            "ligand_rmsd_to_ref_populated_rate": n_rmsd / n if n else float("nan"),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rows.tier3.v2.csv")
    ap.add_argument("--manifest", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rescore_manifest.tier3.v2.csv")
    ap.add_argument("--prior-census", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/post_run_receipts_census.json")
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/receipts_census_v2_true_predicate.json")
    args = ap.parse_args()

    rows = load_rows(args.rows, manifest_csv=args.manifest)
    proxy = local_proxy_census(rows)
    with args.prior_census.open() as f:
        prior_census = json.load(f)

    payload = {
        "task": "C_receipt_predicate_verification",
        "reconstruction": {
            "reconstruction_script": __file__,
            **build_recon_meta({
                "rows_csv": args.rows,
                "manifest_csv": args.manifest,
                "prior_census": args.prior_census,
                "post_run_receipts_module": REPO / "scorer/post_run_receipts.py",
            }),
        },
        "predicate_finding": {
            "receipt_predicate_option": (
                "(b) partial — REAL check, not tautological, but weak "
                "floor threshold (>=1 heavy atom rather than "
                "≈expected)."
            ),
            "predicate_prose": PREDICATE_DESCRIPTION,
            "prior_100pct_interpretation": (
                "The prior '24/24 cells at 100.00% ligand_present_rate' "
                "means every ligand-declaring row had at least one "
                "non-buffer HETATM heavy atom in the output CIF (or, "
                "for peptide rows, at least one standard-AA residue on "
                "a chain other than the receptor). It DOES rule out "
                "the Chai silent-apo failure shape. It does NOT verify "
                "atomistic completeness of the ligand."
            ),
        },
        "prior_census_summary": {
            "n_cells": len(prior_census.get("per_cell", [])),
            "n_cells_below_98pct": sum(
                1 for c in prior_census.get("per_cell", [])
                if c.get("flag_below_98pct")
            ),
        },
        "recommendation": (
            "Enhance the receipt to compare observed n_heavy against "
            "RDKit-parsed expected n_heavy from the row's ligand_smiles "
            "(threshold: observed >= 0.9 * expected for small-molecule "
            "rows; observed_peptide_residues >= 0.9 * len(sequence) for "
            "peptide rows). Enhanced receipt implemented in commit "
            "(see task_c_strengthened_receipt.py in this directory) — "
            "wire it into scorer.orchestrator.score_and_capture "
            "AFTER the existing floor check on the next HPC rescore. "
            "Cannot re-run the census locally because the 40,000 CIFs "
            "live on /hpc/scratch/sengaad1/."
        ),
        "local_proxy_census_using_ligand_rmsd_to_ref_populated": proxy,
        "local_proxy_verdict_per_cell": [
            {
                **c,
                "verdict": (
                    "PROXY_HIGH_CONFIDENCE_LIGAND_PARSED"
                    if c["ligand_rmsd_to_ref_populated_rate"] >= 0.90
                    else "PROXY_INCONCLUSIVE_NEEDS_HPC_RECHECK"
                ),
            }
            for c in proxy
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print("wrote", args.out)


if __name__ == "__main__":
    raise SystemExit(main() or 0)
