#!/usr/bin/env python3
"""T6 — apo-bistability decomposition by backbone + Chai-out (re-audit).

Does the v5 clean-bound apo bistability mean (6.84 % on n=24) survive
removal of any single backbone? Chai flagged as suspect by D1 full result
(receptor-specific active-outlier).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]

ROWS_POCKET = REPO / "experiments/018_block_a_switch_test/analysis/rows.pocket.csv"
ROWS_RMSD = REPO / "experiments/018_block_a_switch_test/analysis/rows.rmsd.csv"
D1_FULL_ROWS = REPO / "experiments/022_tier_d1_deep_apo/analysis/full/rows.csv"
TASK_F_V5 = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_F_v5_clean_bound_stripped.json"

OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/reaudit_2026_09_07"
OUT_JSON = OUT_DIR / "t6_apo_bistability_per_backbone.json"

NPXXY_OH_LT = 9.082
TM6_TILT_GT = 14.932

# Block A input_path convention:
#   .../018_block_a_switch_test_<receptor>_<arm>_<backbone>/.../<backbone>/seed_<N>/...
# We take the last-segment backbone token (between the hex prefix and seed).
BB_RE_BLOCK_A = re.compile(r"/(?P<bb>boltz|chai|of3|protenix)/seed_\d+/")
BB_RE_D1 = re.compile(r"/(?P<bb>boltz|chai|of3|protenix)/seed_\d+/")

FOUR_RECEPTORS = ("CNR2", "CXCR4", "GHSR", "NPY1R")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _to_float(x) -> float:
    try:
        return float(x)
    except (ValueError, TypeError):
        return float("nan")


def is_active(oh: float, tilt: float) -> bool | None:
    if math.isnan(oh) or math.isnan(tilt):
        return None
    return (oh < NPXXY_OH_LT) and (tilt > TM6_TILT_GT)


def load_block_a(pocket_csv: Path, rmsd_csv: Path) -> pd.DataFrame:
    """Load rows.pocket + rows.rmsd, inject backbone from input_path.

    Block A rows carry input_state_claim as the arm. NPXXY-OH lives on pocket
    file; TM6 tilt on rmsd file. Join on input_path.
    """
    pocket = pd.read_csv(pocket_csv, low_memory=False)
    rmsd = pd.read_csv(rmsd_csv, low_memory=False)
    # Both files include input_path. Merge on input_path preserving pocket rows.
    keep_pocket = [
        "input_path", "receptor_slug", "input_state_claim", "receptor_class",
        "passed", "d_npxxy_y558_y753_oh",
    ]
    keep_rmsd = ["input_path", "d_gpcrdb_tm6_tilt_246_637_ca"]
    pocket = pocket[keep_pocket].copy()
    rmsd = rmsd[keep_rmsd].copy()
    merged = pocket.merge(rmsd, on="input_path", how="inner")
    merged["backbone"] = merged["input_path"].str.extract(BB_RE_BLOCK_A.pattern)
    merged["receptor_slug_u"] = merged["receptor_slug"].str.upper().str.strip()
    return merged


def per_receptor_by_backbone(df: pd.DataFrame, receptors: list[str]) -> dict:
    """coh-active fraction per (receptor, backbone) on apo arm."""
    d = df[
        (df["input_state_claim"] == "apo")
        & (df["passed"].astype(str).str.lower() == "true")
        & (df["receptor_class"].fillna("").astype(str).str.upper() == "A")
    ].copy()
    d["oh"] = d["d_npxxy_y558_y753_oh"].apply(_to_float)
    d["tilt"] = d["d_gpcrdb_tm6_tilt_246_637_ca"].apply(_to_float)
    d["active"] = d.apply(lambda r: is_active(r["oh"], r["tilt"]), axis=1)
    d = d[d["active"].notna()]
    out = {}
    for rec in receptors:
        rec_u = rec.upper()
        sub = d[d["receptor_slug_u"] == rec_u]
        per_bb = {}
        for bb in ("boltz", "chai", "of3", "protenix"):
            sb = sub[sub["backbone"] == bb]
            n = len(sb)
            n_active = int(sb["active"].sum())
            per_bb[bb] = {
                "n": n,
                "n_active": n_active,
                "coh_active_fraction": n_active / n if n else float("nan"),
            }
        # Aggregate across backbones
        all_n = int(len(sub))
        all_active = int(sub["active"].sum())
        out[rec_u] = {
            "per_backbone": per_bb,
            "aggregate": {
                "n": all_n,
                "n_active": all_active,
                "coh_active_fraction": all_active / all_n if all_n else float("nan"),
            },
        }
    return out


def per_receptor_coh_active(df: pd.DataFrame, receptors: list[str], exclude_backbone: str | None = None) -> dict[str, float]:
    """Per-receptor coh-active fraction on apo (optionally excluding a backbone)."""
    d = df[
        (df["input_state_claim"] == "apo")
        & (df["passed"].astype(str).str.lower() == "true")
        & (df["receptor_class"].fillna("").astype(str).str.upper() == "A")
    ].copy()
    if exclude_backbone:
        d = d[d["backbone"] != exclude_backbone]
    d["oh"] = d["d_npxxy_y558_y753_oh"].apply(_to_float)
    d["tilt"] = d["d_gpcrdb_tm6_tilt_246_637_ca"].apply(_to_float)
    d["active"] = d.apply(lambda r: is_active(r["oh"], r["tilt"]), axis=1)
    d = d[d["active"].notna()]
    out = {}
    for rec in receptors:
        rec_u = rec.upper()
        sub = d[d["receptor_slug_u"] == rec_u]
        n = len(sub)
        n_active = int(sub["active"].sum())
        out[rec_u] = n_active / n if n else float("nan")
    return out


def mean_v2_convention(fracs: dict[str, float]) -> tuple[float, int]:
    """v5 uses mean of coh_active_fraction across all listed receptors,
    NaN treated as 0 for the panel mean (div-by-all convention). Return
    (mean, n_receptors_with_valid_rows)."""
    vals = list(fracs.values())
    n = len(vals)
    valid = [v for v in vals if not math.isnan(v)]
    div_by_all = [v if not math.isnan(v) else 0.0 for v in vals]
    return (sum(div_by_all) / n if n else float("nan"), len(valid))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(OUT_JSON))
    args = parser.parse_args()

    print("[T6] loading Block A rows...")
    df = load_block_a(ROWS_POCKET, ROWS_RMSD)
    print(f"[T6]   merged n={len(df)} rows")

    # Load v5 clean_bound_24 + free_5 lists (from JSON)
    v5 = json.loads(TASK_F_V5.read_text())
    clean_bound_24 = v5["stratum_stats"]["v5_clean_bound_24"]["receptors"]
    free_5 = v5["stratum_stats"]["refined_v3_free_5"]["receptors"]
    published_v5_mean = v5["stratum_stats"]["v5_clean_bound_24"]["mean_v2_convention_div_by_all"]

    # ==========================================================
    # (1) Decompose CNR2/CXCR4/GHSR/NPY1R apo coh-active by backbone.
    # ==========================================================
    four_rec = per_receptor_by_backbone(df, list(FOUR_RECEPTORS))
    print("[T6.1] Four-receptor decomposition (apo coh-active fraction):")
    print(f"    {'receptor':<10} {'boltz':>7} {'chai':>7} {'of3':>7} {'protenix':>8} {'agg':>7}")
    for rec, r in four_rec.items():
        row = [
            f"{r['per_backbone']['boltz']['coh_active_fraction']:>7.3f}"
                if not math.isnan(r['per_backbone']['boltz']['coh_active_fraction']) else "    NaN",
            f"{r['per_backbone']['chai']['coh_active_fraction']:>7.3f}"
                if not math.isnan(r['per_backbone']['chai']['coh_active_fraction']) else "    NaN",
            f"{r['per_backbone']['of3']['coh_active_fraction']:>7.3f}"
                if not math.isnan(r['per_backbone']['of3']['coh_active_fraction']) else "    NaN",
            f"{r['per_backbone']['protenix']['coh_active_fraction']:>8.3f}"
                if not math.isnan(r['per_backbone']['protenix']['coh_active_fraction']) else "     NaN",
            f"{r['aggregate']['coh_active_fraction']:>7.3f}"
                if not math.isnan(r['aggregate']['coh_active_fraction']) else "    NaN",
        ]
        print(f"    {rec:<10} " + " ".join(row))

    # ==========================================================
    # (2) Clean-bound 6.84 % with vs without Chai.
    # ==========================================================
    fracs_all = per_receptor_coh_active(df, clean_bound_24)
    fracs_no_chai = per_receptor_coh_active(df, clean_bound_24, exclude_backbone="chai")
    mean_all, valid_all = mean_v2_convention(fracs_all)
    mean_no_chai, valid_no_chai = mean_v2_convention(fracs_no_chai)
    print(f"[T6.2] Clean-bound (n=24) mean:")
    print(f"    with all 4 backbones : {mean_all*100:.3f} %  (valid_receptors={valid_all}/24)")
    print(f"    Chai excluded        : {mean_no_chai*100:.3f} %  (valid_receptors={valid_no_chai}/24)")
    print(f"    v5 published         : {published_v5_mean*100:.3f} %")

    # Also do drop-one-backbone LOO on clean-bound.
    bb_loo_cb = {}
    for drop_bb in ("boltz", "chai", "of3", "protenix"):
        f = per_receptor_coh_active(df, clean_bound_24, exclude_backbone=drop_bb)
        m, v = mean_v2_convention(f)
        bb_loo_cb[drop_bb] = {"mean": m, "n_valid_receptors": v}

    # ==========================================================
    # (3) Free-stratum LOO (receptor-out + backbone-out).
    # ==========================================================
    fracs_free = per_receptor_coh_active(df, free_5)
    free_mean, _ = mean_v2_convention(fracs_free)
    print(f"[T6.3] Free-stratum (n=5) full mean: {free_mean*100:.2f} %")
    free_loo_receptor = {}
    for drop_r in free_5:
        kept = [x for x in free_5 if x != drop_r]
        f = per_receptor_coh_active(df, kept)
        m, _ = mean_v2_convention(f)
        free_loo_receptor[drop_r] = {"remaining_receptors": kept, "mean": m}
        print(f"    drop_{drop_r:<6} mean={m*100:.2f} %")
    free_loo_backbone = {}
    for drop_bb in ("boltz", "chai", "of3", "protenix"):
        f = per_receptor_coh_active(df, free_5, exclude_backbone=drop_bb)
        m, _ = mean_v2_convention(f)
        free_loo_backbone[drop_bb] = {"drop_backbone": drop_bb, "mean": m}
        print(f"    drop_{drop_bb:<8} mean={m*100:.2f} %")

    # ==========================================================
    # (4) D1 full CNR2 apo per backbone.
    # ==========================================================
    print("[T6.4] D1 full CNR2 apo per backbone...")
    d1 = pd.read_csv(D1_FULL_ROWS, low_memory=False)
    d1["backbone"] = d1["input_path"].str.extract(BB_RE_D1.pattern)
    d1["receptor_slug_u"] = d1["receptor_slug"].str.upper().str.strip()
    # D1 is apo-only (per plan).
    d1_pass = d1[
        (d1["passed"].astype(str).str.lower() == "true")
        & (d1["receptor_class"].fillna("").astype(str).str.upper() == "A")
    ].copy()
    d1_pass["oh"] = d1_pass["d_npxxy_y558_y753_oh"].apply(_to_float)
    d1_pass["tilt"] = d1_pass["d_gpcrdb_tm6_tilt_246_637_ca"].apply(_to_float)
    d1_pass["active"] = d1_pass.apply(lambda r: is_active(r["oh"], r["tilt"]), axis=1)
    d1_pass = d1_pass[d1_pass["active"].notna()]
    d1_cnr2 = d1_pass[d1_pass["receptor_slug_u"] == "CNR2"]
    d1_cnr2_by_bb = {}
    for bb in ("boltz", "chai", "of3", "protenix"):
        sub = d1_cnr2[d1_cnr2["backbone"] == bb]
        n = len(sub)
        n_active = int(sub["active"].sum())
        d1_cnr2_by_bb[bb] = {
            "n": int(n),
            "n_active": n_active,
            "coh_active_fraction": n_active / n if n else float("nan"),
        }
        print(f"    {bb:<10} n={n:>4} coh_active={n_active/n if n else float('nan'):.3f}")

    # Compare to Block A CNR2/chai.
    ba_cnr2_chai = four_rec["CNR2"]["per_backbone"]["chai"]["coh_active_fraction"]
    d1_cnr2_chai = d1_cnr2_by_bb["chai"]["coh_active_fraction"]
    drift_note = (
        f"Chai CNR2 apo coh-active: Block A={ba_cnr2_chai:.3f}, D1 full={d1_cnr2_chai:.3f} "
        f"(Δ={d1_cnr2_chai - ba_cnr2_chai:+.3f})"
    )
    print("[T6.4]", drift_note)

    # ==========================================================
    # Verdict.
    # ==========================================================
    # Clean-bound survives removal of a backbone if the drop-bb mean stays within
    # 30% relative and above ~5 % floor. Reviewers care about direction more than magnitude.
    survives_any_drop = all(
        d["mean"] >= 0.05 for d in bb_loo_cb.values()
    )
    max_drop_shift = max(
        abs(d["mean"] - mean_all) for d in bb_loo_cb.values()
    )

    verdict = (
        "APO_BISTABILITY_SURVIVES_ANY_BACKBONE_DROP"
        if survives_any_drop
        else "APO_BISTABILITY_COLLAPSES_ON_SOME_BACKBONE_DROP"
    )

    def _git_head() -> str:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
            ).strip()
        except Exception:
            return ""

    script_path = Path(__file__)
    report = {
        "task": "T6_apo_bistability_per_backbone",
        "_provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "script_sha256": sha256_file(script_path),
            "git_head": _git_head(),
            "inputs": {
                "rows_pocket": {"path": str(ROWS_POCKET.relative_to(REPO)), "sha256": sha256_file(ROWS_POCKET)},
                "rows_rmsd":   {"path": str(ROWS_RMSD.relative_to(REPO)), "sha256": sha256_file(ROWS_RMSD)},
                "d1_full_rows":{"path": str(D1_FULL_ROWS.relative_to(REPO)), "sha256": sha256_file(D1_FULL_ROWS)},
                "task_F_v5":   {"path": str(TASK_F_V5.relative_to(REPO)), "sha256": sha256_file(TASK_F_V5)},
            },
            "predicate": {"NPXXY_OH_LT": NPXXY_OH_LT, "TM6_TILT_GT": TM6_TILT_GT},
        },
        "four_receptor_by_backbone_decomposition": four_rec,
        "clean_bound_mean_with_and_without_chai": {
            "clean_bound_24_receptors": clean_bound_24,
            "recomputed_mean_v2_convention_all_backbones": mean_all,
            "recomputed_mean_v2_convention_chai_excluded": mean_no_chai,
            "published_v5_mean": published_v5_mean,
            "recomputed_matches_published_within_0.5pp": abs(mean_all - published_v5_mean) < 0.005,
        },
        "clean_bound_loo_backbone": bb_loo_cb,
        "clean_bound_max_drop_shift_pp": max_drop_shift * 100,
        "free_stratum_full_mean": free_mean,
        "free_stratum_loo_receptor_out": free_loo_receptor,
        "free_stratum_loo_backbone_out": free_loo_backbone,
        "d1_full_cnr2_apo_by_backbone": d1_cnr2_by_bb,
        "d1_vs_block_a_cnr2_chai": {
            "block_a": ba_cnr2_chai,
            "d1_full": d1_cnr2_chai,
            "delta": d1_cnr2_chai - ba_cnr2_chai if not (math.isnan(d1_cnr2_chai) or math.isnan(ba_cnr2_chai)) else float("nan"),
            "note": drift_note,
        },
        "verdict": verdict,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[T6] wrote {Path(args.out).relative_to(REPO)}")
    print(f"[T6] verdict: {verdict}")
    print(f"[T6] max drop-one-backbone shift on clean-bound: {max_drop_shift*100:.2f} pp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
