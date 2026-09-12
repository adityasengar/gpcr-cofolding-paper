#!/usr/bin/env python3
"""Tier D3 matched-structure propagation probe.

Purpose: verify the MSA-depth override REACHES the model at inference.
The status-JSON echo layer has produced false-green results before
(`docs/AUDIT_TRAIL.md §10` — Chai silent single-seq; §21 — species-fix
`.pyc` bytecode false-positive). This test uses a signature the echo
layer cannot fake: Cα RMSD between two matched predictions that differ
ONLY in the MSA file.

Per backbone:
  Run A: `msa = full.a3m`         (all rows)
  Run B: `msa = depth8.a3m`       (query + 7 rows)
Identical seed, identical sample index, identical everything else.

Verdict per backbone:
  RMSD < 0.5 Å → DEPTH_NOT_REACHED_MODEL (HALT tier before smoke)
  0.5–2.0 Å   → DEPTH_REACHES_MODEL_MINOR
  ≥ 2.0 Å     → DEPTH_REACHES_MODEL_MAJOR

Probe receptor: AA2AR (479 aa, canonical adenosine A2A, well-characterised
so any depth-driven structural drift is diagnosable).

Runs on HPC. Uses the D3 plumbing landed at commit b3863bd (propose.py
msa_a3m_path kwarg + launchers + queue_ops per-row env).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

NOISE_FLOOR_AA = 0.5
MINOR_MAJOR_AA = 2.0

BACKBONES = ("boltz", "chai", "of3", "protenix")
PROBE_RECEPTOR = "AA2AR"


def parse_ca_positions(cif_path: Path) -> list[tuple[float, float, float]]:
    """Extract Cα coordinates from chain A of a CIF (order-preserving)."""
    import gemmi
    st = gemmi.read_structure(str(cif_path))
    if not st:
        return []
    ca = []
    for chain in st[0]:
        if chain.name != "A":
            continue
        for res in chain:
            a = res.find_atom("CA", "\0")
            if a is None:
                continue
            ca.append((a.pos.x, a.pos.y, a.pos.z))
    return ca


def kabsch_rmsd(coords_a, coords_b) -> float:
    """Compute Kabsch-superposed all-Cα RMSD between two matched
    coord sets. Uses gemmi's SuperposeResult for fast, correct
    superposition."""
    import gemmi
    import numpy as np
    a = np.asarray(coords_a, dtype=float)
    b = np.asarray(coords_b, dtype=float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    if n == 0:
        return float("nan")
    # Center both point clouds
    a_c = a - a.mean(axis=0)
    b_c = b - b.mean(axis=0)
    # Kabsch rotation matrix
    H = a_c.T @ b_c
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    b_rot = b_c @ R.T
    diff = a_c - b_rot
    rmsd = float(np.sqrt((diff * diff).sum() / n))
    return rmsd


def collect(pool_root: Path) -> dict:
    """Read the 8 CIFs (4 backbones × 2 depths) and compute per-backbone RMSD."""
    results = {}
    for bb in BACKBONES:
        # Convention: <pool_root>/<bb>/<full|depth8>/model.cif
        # (matches what the launcher's PRED_OUT_DIR/model_0.cif landing path is)
        candidates = {
            "full": sorted((pool_root / bb / "full").rglob("*.cif")),
            "depth8": sorted((pool_root / bb / "depth8").rglob("*.cif")),
        }
        cif_full = candidates["full"][0] if candidates["full"] else None
        cif_d8 = candidates["depth8"][0] if candidates["depth8"] else None
        if cif_full is None or cif_d8 is None:
            results[bb] = {"error": f"missing CIF; full={cif_full} depth8={cif_d8}"}
            continue
        try:
            ca_full = parse_ca_positions(cif_full)
            ca_d8 = parse_ca_positions(cif_d8)
            rmsd = kabsch_rmsd(ca_full, ca_d8)
        except Exception as exc:
            results[bb] = {"error": f"parse/superpose failed: {exc!r}"}
            continue
        if rmsd < NOISE_FLOOR_AA:
            verdict = "DEPTH_NOT_REACHED_MODEL"
        elif rmsd < MINOR_MAJOR_AA:
            verdict = "DEPTH_REACHES_MODEL_MINOR"
        else:
            verdict = "DEPTH_REACHES_MODEL_MAJOR"
        results[bb] = {
            "n_ca_full": len(ca_full),
            "n_ca_depth8": len(ca_d8),
            "rmsd_A": round(rmsd, 4),
            "verdict": verdict,
            "cif_full": str(cif_full.relative_to(pool_root)),
            "cif_depth8": str(cif_d8.relative_to(pool_root)),
        }
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pool-root", type=Path, required=True,
                    help="Root dir containing <bb>/<full|depth8>/*.cif for each backbone")
    ap.add_argument("--out", type=Path, required=True,
                    help="Output JSON path")
    args = ap.parse_args()

    results = collect(args.pool_root)
    verdict_summary = {}
    halt = []
    for bb, r in results.items():
        v = r.get("verdict", "MISSING")
        verdict_summary[bb] = v
        if v == "DEPTH_NOT_REACHED_MODEL":
            halt.append(bb)

    output = {
        "task": "d3_matched_structure_probe",
        "probe_receptor": PROBE_RECEPTOR,
        "noise_floor_A": NOISE_FLOOR_AA,
        "results": results,
        "verdict_summary": verdict_summary,
        "halt_backbones": halt,
        "overall": "HALT" if halt else "PROCEED_TO_SMOKE",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, default=str))
    print(json.dumps(output, indent=2, default=str))

    if halt:
        print(f"\nHALT: {halt} did NOT consume the depth override. Fix plumbing.")
        return 2
    print("\nAll 4 backbones responded to the depth override → PROCEED_TO_SMOKE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
