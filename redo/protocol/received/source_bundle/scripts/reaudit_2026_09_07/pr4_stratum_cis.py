#!/usr/bin/env python3
"""PR4 — cluster-bootstrap CIs on stratum means.

Attaches per-stratum cluster-bootstrap CIs to bound / clean-bound / free /
Chai-excluded variants. Recomputes per-receptor per-backbone apo
coh-active fractions from Block A rows.pocket.csv + rows.rmsd.csv using
the two-instrument predicate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]

ROWS_POCKET = REPO / "experiments/018_block_a_switch_test/analysis/rows.pocket.csv"
ROWS_RMSD = REPO / "experiments/018_block_a_switch_test/analysis/rows.rmsd.csv"
TASK_F = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_F_v5_clean_bound_stripped.json"
OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/pr4_stratum_cis.json"

NPXXY_OH_LT = 9.082
TM6_TILT_GT = 14.932
BOOTSTRAP_N = 5000
SEED = 20260907


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def cluster_bootstrap(values: list[float], n_iter: int = BOOTSTRAP_N, seed: int = SEED) -> dict:
    if not values:
        return {"n": 0, "point": None, "ci_lo": None, "ci_hi": None}
    v = np.array(values, dtype=float)
    n = len(v)
    rng = np.random.default_rng(seed)
    reps = np.empty(n_iter, dtype=float)
    for i in range(n_iter):
        idx = rng.integers(0, n, size=n)
        reps[i] = float(np.mean(v[idx]))
    return {
        "n": int(n),
        "point": float(np.mean(v)),
        "median": float(np.median(v)),
        "ci_lo": float(np.percentile(reps, 2.5)),
        "ci_hi": float(np.percentile(reps, 97.5)),
        "bootstrap_n": n_iter,
        "seed": seed,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    task_f = json.loads(TASK_F.read_text())
    ss = task_f["stratum_stats"]
    bound_26 = ss["refined_v3_bound_26"]["receptors"]
    clean_bound_24 = ss["v5_clean_bound_24"]["receptors"]
    free_5 = ss["refined_v3_free_5"]["receptors"]
    stripped = ss["v5_stripped_receptors"]["receptors"]
    per_rec = task_f["per_receptor_apo_summary"]

    # Aggregate (all backbones) per-receptor coh_active_fraction — matches
    # task_F v5's own convention. Filter None (receptors with no valid apo
    # 2-instrument rows: EDNRB, GRPR).
    def _agg(receptors: list[str]) -> list[float]:
        out = []
        for r in receptors:
            v = per_rec.get(r, {}).get("coh_active_fraction")
            if v is not None:
                out.append(float(v))
        return out

    ci_bound_26 = cluster_bootstrap(_agg(bound_26))
    ci_clean_bound_24 = cluster_bootstrap(_agg(clean_bound_24))
    ci_free_5 = cluster_bootstrap(_agg(free_5))

    # Chai-excluded — recompute per-receptor per-backbone from Block A rows.
    print("[PR4] loading Block A rows...")
    pocket = pd.read_csv(ROWS_POCKET, low_memory=False)
    rmsd = pd.read_csv(ROWS_RMSD, low_memory=False)
    # Backbone parsed from input_path via regex; both files share input_path.
    def _bb(p: str) -> str:
        p = str(p)
        for bb in ("boltz", "chai", "of3", "protenix"):
            if f"/{bb}/" in p:
                return bb
        return ""
    pocket["backbone"] = pocket["input_path"].apply(_bb)

    # Apo filter — Block A uses `input_state_claim` == "apo".
    apo = pocket[
        (pocket["input_state_claim"].astype(str) == "apo")
        & (pocket["passed"].astype(str).str.lower() == "true")
        & (pocket["receptor_class"].astype(str).str.upper() == "A")
    ].copy()

    def _to_f(x):
        try:
            return float(x)
        except (ValueError, TypeError):
            return float("nan")

    apo["oh"] = apo["d_npxxy_y558_y753_oh"].apply(_to_f)
    apo["tilt"] = apo["d_gpcrdb_tm6_tilt_246_637_ca"].apply(_to_f)
    apo["is_active"] = (apo["oh"] < NPXXY_OH_LT) & (apo["tilt"] > TM6_TILT_GT)

    # Per (receptor, backbone) coh-active fraction on apo Class A rows.
    per_rb: dict[tuple[str, str], float] = {}
    for (rec, bb), g in apo.groupby(["receptor_slug", "backbone"]):
        valid = g[g["oh"].notna() & g["tilt"].notna()]
        if len(valid) == 0:
            continue
        per_rb[(rec.upper(), bb.lower())] = float(valid["is_active"].mean())

    # Per-receptor mean EXCLUDING Chai.
    def _mean_non_chai(receptor: str) -> float | None:
        vals = [per_rb.get((receptor.upper(), bb)) for bb in ("boltz", "of3", "protenix")]
        vals = [v for v in vals if v is not None]
        return statistics.fmean(vals) if vals else None

    def _agg_non_chai(receptors: list[str]) -> list[float]:
        out = []
        for r in receptors:
            v = _mean_non_chai(r)
            if v is not None:
                out.append(v)
        return out

    ci_bound_26_no_chai = cluster_bootstrap(_agg_non_chai(bound_26))
    ci_clean_bound_24_no_chai = cluster_bootstrap(_agg_non_chai(clean_bound_24))
    ci_free_5_no_chai = cluster_bootstrap(_agg_non_chai(free_5))

    payload = {
        "task": "PR4_stratum_bootstrap_cis",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "task_F_v5": {"path": str(TASK_F.relative_to(REPO)), "sha256": sha256_file(TASK_F)},
            "rows_pocket": {"path": str(ROWS_POCKET.relative_to(REPO)), "sha256": sha256_file(ROWS_POCKET)},
            "rows_rmsd": {"path": str(ROWS_RMSD.relative_to(REPO)), "sha256": sha256_file(ROWS_RMSD)},
        },
        "bootstrap_config": {"n_iter": BOOTSTRAP_N, "seed": SEED},
        "strata": {
            "bound_26_all_backbones": ci_bound_26,
            "clean_bound_24_all_backbones": ci_clean_bound_24,
            "free_5_all_backbones": ci_free_5,
            "bound_26_chai_excluded": ci_bound_26_no_chai,
            "clean_bound_24_chai_excluded": ci_clean_bound_24_no_chai,
            "free_5_chai_excluded": ci_free_5_no_chai,
        },
    }

    def _fmt(ci: dict) -> str:
        if ci["point"] is None:
            return f"n={ci['n']} EMPTY"
        return f"n={ci['n']:>2} {ci['point']*100:>6.2f}%  CI[{ci['ci_lo']*100:>6.2f}, {ci['ci_hi']*100:>6.2f}]  median={ci['median']*100:.2f}%"

    print()
    print("=" * 74)
    print("PR4 — stratum bootstrap CIs (cluster over receptors, 5000 iter)")
    print("=" * 74)
    print(f"  {'stratum':<32} {'all backbones':<38}  chai-excluded")
    print(f"  {'---':<32} {'---':<38}  ---")
    print(f"  {'bound n=26':<32} {_fmt(ci_bound_26):<38}  {_fmt(ci_bound_26_no_chai)}")
    print(f"  {'clean-bound n=24':<32} {_fmt(ci_clean_bound_24):<38}  {_fmt(ci_clean_bound_24_no_chai)}")
    print(f"  {'free n=5':<32} {_fmt(ci_free_5):<38}  {_fmt(ci_free_5_no_chai)}")

    verdict_lines = []
    # Well-estimated iff CI half-width < 0.5 * point estimate; loosely n>=10.
    for name, ci in (
        ("clean_bound_24", ci_clean_bound_24),
        ("free_5", ci_free_5),
    ):
        if ci["point"] is None or ci["point"] == 0:
            continue
        half = (ci["ci_hi"] - ci["ci_lo"]) / 2
        rel = half / ci["point"] if ci["point"] > 0 else float("inf")
        state = (
            "WELL_ESTIMATED" if rel < 0.4 and ci["n"] >= 10 else
            "WIDE_CI_LOW_N" if ci["n"] < 10 else "WIDE_CI"
        )
        verdict_lines.append(f"{name}: {state} (n={ci['n']}, ±half-width/point = {rel:.2f})")

    payload["verdict_lines"] = verdict_lines
    payload["verdict"] = " ; ".join(verdict_lines)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(payload, indent=2))
    print()
    print("Verdict:")
    for line in verdict_lines:
        print(f"  {line}")
    print(f"\nWrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
