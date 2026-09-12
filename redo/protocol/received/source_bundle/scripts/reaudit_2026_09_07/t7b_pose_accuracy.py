#!/usr/bin/env python3
"""T7b — cross-backbone pose accuracy on v3 corpus.

Merges the OF3+Protenix rows from `rows.tier3.v2.csv` (pre-MCS but atom-name
fast path works on those two backbones — captured 76%) with the newly rescored
Boltz+Chai rows from `rescore_t7b/rows.csv` (MCS-enabled).

Reports:
  - Coverage census: numeric `ligand_rmsd_to_ref` per (backbone × ligand_role
    × arm) cell.
  - Dock rate <3Å per cell.
  - Cross-backbone comparison: was the pre-audit's scoped 6.93% dock rate
    (OF3+Protenix × neutral_antagonist × ref-matched) reproduced?
    What does Boltz+Chai add?
  - Per-backbone (pooled across cells) dock rate.

Also verifies the MCS-vs-atom-name method mix per row and per cell.
"""
from __future__ import annotations

import argparse, hashlib, json, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import numpy as np

REPO = Path(__file__).resolve().parents[2]
ROWS_V2 = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_V2 = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _to_float(x) -> float:
    try:
        return float(x)
    except (ValueError, TypeError):
        return float("nan")


def load_v2_of3_protenix(rows_v2_path: Path, manifest_path: Path) -> pd.DataFrame:
    """v2 corpus, keep OF3+Protenix (pre-MCS but fast path works there)."""
    rows = pd.read_csv(rows_v2_path, low_memory=False)
    manifest = pd.read_csv(manifest_path, low_memory=False)
    m_idx = manifest.set_index("prediction_path")
    rows["backbone"] = rows["input_path"].map(m_idx["backbone"].to_dict()).fillna("")
    rows["partner_type"] = rows["input_path"].map(m_idx["partner_type"].to_dict()).fillna("")
    for col in ("ligand_role",):
        if col in m_idx.columns:
            fb = rows.get(col, pd.Series([""] * len(rows)))
            rows[col] = rows["input_path"].map(m_idx[col].to_dict()).fillna(fb)
    rows["arm"] = rows["partner_type"].apply(
        lambda p: "apo" if str(p).lower() == "apo" else "cognate"
    )
    sub = rows[rows["backbone"].str.lower().isin(["of3", "protenix"])].copy()
    return sub


def load_t7b_boltz_chai(t7b_rows_path: Path, manifest_path: Path) -> pd.DataFrame:
    rows = pd.read_csv(t7b_rows_path, low_memory=False)
    manifest = pd.read_csv(manifest_path, low_memory=False)
    m_idx = manifest.set_index("prediction_path")
    # rows.csv from rescore_parallel has 'input_path' identical to
    # manifest 'prediction_path'.
    rows["backbone"] = rows["input_path"].map(m_idx["backbone"].to_dict()).fillna("")
    rows["partner_type"] = rows["input_path"].map(m_idx["partner_type"].to_dict()).fillna("")
    if "ligand_role" in m_idx.columns:
        fb = rows.get("ligand_role", pd.Series([""] * len(rows)))
        rows["ligand_role"] = rows["input_path"].map(m_idx["ligand_role"].to_dict()).fillna(fb)
    rows["arm"] = rows["partner_type"].apply(
        lambda p: "apo" if str(p).lower() == "apo" else "cognate"
    )
    return rows


def coverage_and_dock_rate(df: pd.DataFrame, dock_threshold_A: float = 3.0) -> pd.DataFrame:
    """Per (backbone × ligand_role × arm) cell:
    - n_total
    - n_numeric (ligand_rmsd_to_ref populated)
    - n_dock (ligand_rmsd_to_ref < threshold)
    - dock_rate = n_dock / n_numeric
    """
    df = df.copy()
    df["lrmsd_num"] = pd.to_numeric(df["ligand_rmsd_to_ref"], errors="coerce")
    df["is_numeric"] = df["lrmsd_num"].notna()
    df["is_dock"] = (df["lrmsd_num"] < dock_threshold_A) & df["is_numeric"]

    # Filter to passing rows only (assertions all ok).
    if "passed" in df.columns:
        df = df[df["passed"].astype(str).str.lower() == "true"].copy()

    grp = df.groupby(["backbone", "ligand_role", "arm"], dropna=False).agg(
        n_total=("is_numeric", "size"),
        n_numeric=("is_numeric", "sum"),
        n_dock=("is_dock", "sum"),
    ).reset_index()
    grp["coverage"] = grp["n_numeric"] / grp["n_total"]
    grp["dock_rate_numeric"] = grp.apply(
        lambda r: r["n_dock"] / r["n_numeric"] if r["n_numeric"] > 0 else float("nan"),
        axis=1,
    )
    grp["dock_rate_all"] = grp["n_dock"] / grp["n_total"]
    return grp


def method_census(df: pd.DataFrame) -> pd.DataFrame:
    """Per (backbone × ligand_role) method breakdown."""
    if "pocket_ligand_atom_map_method" not in df.columns:
        return pd.DataFrame()
    df = df.copy()
    if "passed" in df.columns:
        df = df[df["passed"].astype(str).str.lower() == "true"].copy()
    return df.groupby(["backbone", "ligand_role", "pocket_ligand_atom_map_method"], dropna=False).size().reset_index(name="n")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--t7b-rows", default="experiments/021_block_c_tier3_pharmacology/rescore_t7b/rows.csv",
                   help="local path to T7b MCS-rescored Boltz+Chai rows.csv (rsync'd from HPC)")
    p.add_argument("--dock-threshold-a", type=float, default=3.0)
    p.add_argument("--out", default=str(OUT_DIR / "t7b_pose_accuracy.json"))
    args = p.parse_args()

    t7b_path = REPO / args.t7b_rows
    if not t7b_path.exists():
        print(f"[T7b] ERROR: T7b rows.csv not found at {t7b_path}", file=sys.stderr)
        print(f"[T7b] rsync it from HPC first, e.g.:", file=sys.stderr)
        print(f"      rsync -avz basel-hpc:/hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/rescore_t7b/rows.csv {t7b_path.parent}/", file=sys.stderr)
        return 1

    print(f"[T7b] loading v2 corpus (OF3+Protenix subset)...")
    df_v2 = load_v2_of3_protenix(ROWS_V2, MANIFEST_V2)
    print(f"      {len(df_v2)} rows across OF3+Protenix")

    print(f"[T7b] loading T7b MCS-rescored Boltz+Chai...")
    df_t7b = load_t7b_boltz_chai(t7b_path, MANIFEST_V2)
    print(f"      {len(df_t7b)} rows across Boltz+Chai")

    # Union columns; some may only exist on one side. Keep the shared subset
    # relevant to pose analysis.
    keep_cols = ["input_path", "backbone", "ligand_role", "arm",
                 "receptor_slug", "passed", "ligand_rmsd_to_ref",
                 "pocket_ligand_atom_map_method"]
    for c in keep_cols:
        if c not in df_v2.columns:
            df_v2[c] = ""
        if c not in df_t7b.columns:
            df_t7b[c] = ""
    df_v3 = pd.concat([df_v2[keep_cols], df_t7b[keep_cols]], ignore_index=True)
    print(f"[T7b] merged v3 corpus: {len(df_v3)} rows")

    coverage = coverage_and_dock_rate(df_v3, dock_threshold_A=args.dock_threshold_a)
    print("\n=== Coverage + dock rate per (backbone × ligand_role × arm) ===")
    print(coverage.to_string(index=False))

    methods = method_census(df_v3)
    print("\n=== Method census per (backbone × ligand_role) ===")
    print(methods.to_string(index=False))

    # Prior "scoped" claim: OF3+Protenix × neutral_antagonist × ref-matched
    # = 6.93% dock rate <3Å on n=4500. Verify.
    prior_cell_v2 = coverage[
        (coverage["backbone"].str.lower().isin(["of3", "protenix"]))
        & (coverage["ligand_role"] == "neutral_antagonist")
    ]
    print("\n=== Prior scoped claim cell (OF3+Protenix × neutral_antag) ===")
    print(prior_cell_v2.to_string(index=False))

    # Cross-backbone comparison on the "canonical" pose-accuracy view:
    # ligand_role == neutral_antagonist, both arms combined.
    canonical = coverage[coverage["ligand_role"] == "neutral_antagonist"]
    print("\n=== Cross-backbone canonical pose-accuracy row (neutral_antag) ===")
    print(canonical.to_string(index=False))

    payload = {
        "task": "t7b_pose_accuracy",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "prereg_git_sha": "e63692f",
        "dock_threshold_A": args.dock_threshold_a,
        "inputs": {
            "rows_v2": {"path": str(ROWS_V2.relative_to(REPO)), "sha256": sha256_file(ROWS_V2)},
            "manifest_v2": {"path": str(MANIFEST_V2.relative_to(REPO)), "sha256": sha256_file(MANIFEST_V2)},
            "rows_t7b": {"path": str(t7b_path.relative_to(REPO)), "sha256": sha256_file(t7b_path)},
        },
        "n_rows_v2_of3protenix": int(len(df_v2)),
        "n_rows_t7b_boltz_chai": int(len(df_t7b)),
        "n_rows_v3_merged": int(len(df_v3)),
        "coverage_and_dock_rate": coverage.to_dict("records"),
        "method_census": methods.to_dict("records"),
        "prior_scoped_cell_of3_protenix_neutral_antag": prior_cell_v2.to_dict("records"),
        "canonical_pose_row_neutral_antag_all_backbones": canonical.to_dict("records"),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, default=str))
    try:
        rel = out_path.resolve().relative_to(REPO)
        print(f"\n[T7b] wrote {rel}")
    except ValueError:
        print(f"\n[T7b] wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
