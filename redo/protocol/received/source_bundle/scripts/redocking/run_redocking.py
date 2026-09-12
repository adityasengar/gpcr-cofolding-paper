"""T1.5 redocking runner — three-way Vina/Smina comparison.

Reads `refs/redocking_targets.csv` (34 pre-registered targets), extracts
the predicted co-folded structures from the Block C Tier 3 corpus, and
runs Vina or Smina against three receptor states per (receptor, backbone):

    - CRYSTAL ceiling: dock into the receptor extracted from crystal_pose_pdb
    - PREDICTED test: dock into the predicted structure at predicted_state_family
    - WRONG-STATE floor: dock into the predicted structure at wrong_state_family

Requires:
    - AutoDock Vina 1.2+ binary on PATH (or --vina-binary path)
    - Smina binary on PATH (or --smina-binary path)
    - Meeko for ligand PDBQT prep (pip install meeko)
    - RDKit for SMILES parsing + MCS RMSD
    - The Block C Tier 3 output CIFs on HPC pool

Usage:

    # Dry-run: list all (receptor, backbone, arm) cells that would dock
    python3 scripts/redocking/run_redocking.py --dry-run

    # Run one cell (development / smoke)
    python3 scripts/redocking/run_redocking.py --receptor ADRB2 --backbone protenix

    # Full sweep (34 receptors × 4 backbones × 3 arms = 408 CPU jobs)
    python3 scripts/redocking/run_redocking.py --output-csv experiments/025_redocking/analysis/redocking_results.csv

Output CSV columns:
    receptor_slug, backbone, arm, docker (vina|smina), rmsd_to_crystal_A,
    docker_score, receptor_source_path, ligand_smiles, ligand_ccd,
    run_ts_utc, docker_binary_sha256, error_note

Pre-registered per `experiments/025_redocking/PRE_REGISTRATION.md`. NO
post-hoc modifications to target list or fire-gate criterion without
`AMENDMENTS.md` entry.

STATUS: skeleton — end-to-end pipeline needs Vina/Smina binaries on the
execution machine + Meeko installed + Block C Tier 3 output CIFs
accessible locally (either mounted or rsync'd from HPC).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
TARGETS_CSV = REPO / "refs/redocking_targets.csv"
DEFAULT_OUTPUT = REPO / "experiments/025_redocking/analysis/redocking_results.csv"

BACKBONES = ["boltz", "chai", "of3", "protenix"]


def load_targets() -> list[dict]:
    """Load pre-registered target list. Verify against pinned SHA."""
    if not TARGETS_CSV.is_file():
        raise FileNotFoundError(f"pre-registered targets missing: {TARGETS_CSV}")
    got_sha = hashlib.sha256(TARGETS_CSV.read_bytes()).hexdigest()
    expected_sha = "0483319651f6bbba14388da192c1b6e0b189dd87e0b4ca4cc563a5c6f22df1a5"
    if got_sha != expected_sha:
        raise RuntimeError(
            f"targets file SHA-256 changed! Pre-registration violated.\n"
            f"  expected: {expected_sha}\n"
            f"  got:      {got_sha}\n"
            f"  See experiments/025_redocking/PRE_REGISTRATION.md §Rules on modification."
        )
    with TARGETS_CSV.open() as fh:
        return list(csv.DictReader(fh))


def resolve_receptor_pdbqt(
    receptor_slug: str, backbone: str, arm: str, targets: list[dict]
) -> tuple[Path, str]:
    """Locate the receptor structure for a docking cell.

    Returns (path_to_cif_or_pdb, source_kind) where source_kind is one of:
        "crystal_ceiling", "predicted_test", "wrong_state_floor".

    For "crystal_ceiling": fetch from RCSB the crystal_pose_pdb entry, strip
        HETATM records, return receptor chain PDB.
    For "predicted_*": locate the corresponding Block C Tier 3 output CIF.

    Deferred: this depends on the Block C Tier 3 output tree being locally
    accessible. Implementation slot below.
    """
    raise NotImplementedError(
        "Receptor resolution depends on Block C Tier 3 output tree access. "
        "TODO: implement based on --tier3-pool-dir CLI argument."
    )


def prepare_ligand_pdbqt(smiles: str, out_dir: Path) -> Path:
    """Convert SMILES to PDBQT via Meeko.

    Returns path to the PDBQT file. Deterministic per SMILES (Meeko's
    default embedding is deterministic given the same RDKit version).
    """
    raise NotImplementedError(
        "Requires meeko. `pip install meeko` in the redocking venv."
    )


def run_vina(
    receptor_pdbqt: Path,
    ligand_pdbqt: Path,
    center: tuple[float, float, float],
    box_size: tuple[float, float, float],
    seed: int = 42,
    vina_binary: str = "vina",
) -> dict:
    """Run AutoDock Vina; return top-pose PDBQT path + docking score."""
    raise NotImplementedError("Requires AutoDock Vina 1.2+ binary on PATH.")


def run_smina(
    receptor_pdbqt: Path,
    ligand_pdbqt: Path,
    center: tuple[float, float, float],
    box_size: tuple[float, float, float],
    seed: int = 42,
    smina_binary: str = "smina",
) -> dict:
    """Run Smina; return top-pose PDBQT path + docking score."""
    raise NotImplementedError("Requires Smina binary on PATH.")


def compute_pose_rmsd(
    docked_pdbqt: Path, crystal_ligand_pdb: Path
) -> float:
    """Compute Cα-heavy-atom RMSD between docked pose and crystal pose.

    Uses the MCS-based atom matcher from `scorer.pocket_metrics`. Handles
    SMILES-derived atom name differences via RDKit MCS fallback.
    """
    raise NotImplementedError(
        "Delegate to scorer.pocket_metrics MCS matcher; T1.3 loose end #4 "
        "landed in scorer/pocket_metrics.py:501-624 (commit 54c6d10)."
    )


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="List cells, no docking")
    p.add_argument("--receptor", type=str, help="Single receptor slug (for smoke)")
    p.add_argument("--backbone", type=str, choices=BACKBONES + [""], default="",
                   help="Single backbone (smoke); empty = all four")
    p.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--tier3-pool-dir", type=Path,
                   help="Local mount path of Block C Tier 3 output tree")
    p.add_argument("--vina-binary", type=str, default="vina")
    p.add_argument("--smina-binary", type=str, default="smina")
    p.add_argument("--seed", type=int, default=42, help="Vina/Smina RNG seed (fixed at 42 per pre-reg)")
    args = p.parse_args()

    targets = load_targets()
    print(f"loaded {len(targets)} pre-registered targets from {TARGETS_CSV}")

    if args.receptor:
        targets = [t for t in targets if t["receptor_slug"] == args.receptor]
        if not targets:
            print(f"no target for receptor {args.receptor}", file=sys.stderr)
            return 1

    backbones = [args.backbone] if args.backbone else BACKBONES

    total_cells = len(targets) * len(backbones) * 3
    print(f"grid: {len(targets)} receptors × {len(backbones)} backbones × 3 arms = {total_cells} docking cells")

    if args.dry_run:
        for t in targets:
            for bb in backbones:
                for kind in ("crystal_ceiling", "predicted_test", "wrong_state_floor"):
                    print(f"  {t['receptor_slug']}/{bb}/{kind}")
        return 0

    if not args.tier3_pool_dir:
        print("ERROR: --tier3-pool-dir required for real docking runs", file=sys.stderr)
        print("       (Block C Tier 3 output tree must be locally accessible)", file=sys.stderr)
        return 2

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "receptor_slug", "backbone", "arm", "docker",
        "rmsd_to_crystal_A", "docker_score", "receptor_source_path",
        "ligand_smiles", "ligand_ccd", "run_ts_utc",
        "docker_binary_sha256", "error_note",
    ]
    with args.output_csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for t in targets:
            for bb in backbones:
                for arm_kind in ("crystal_ceiling", "predicted_test", "wrong_state_floor"):
                    try:
                        # Placeholder: full pipeline not yet implemented
                        raise NotImplementedError(
                            "run_redocking.py skeleton — pipeline stages "
                            "resolve_receptor_pdbqt, prepare_ligand_pdbqt, "
                            "run_vina/run_smina, compute_pose_rmsd need "
                            "implementation. See NotImplementedError body per stage."
                        )
                    except NotImplementedError as e:
                        w.writerow({
                            "receptor_slug": t["receptor_slug"],
                            "backbone": bb,
                            "arm": arm_kind,
                            "docker": "vina",
                            "rmsd_to_crystal_A": "",
                            "docker_score": "",
                            "receptor_source_path": "",
                            "ligand_smiles": t.get("target_ligand_smiles", ""),
                            "ligand_ccd": t.get("target_ligand_ccd", ""),
                            "run_ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            "docker_binary_sha256": "",
                            "error_note": f"NOT_IMPLEMENTED: {e}",
                        })
                        break  # only emit one placeholder per cell
    print(f"wrote {args.output_csv} (skeleton rows)")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
