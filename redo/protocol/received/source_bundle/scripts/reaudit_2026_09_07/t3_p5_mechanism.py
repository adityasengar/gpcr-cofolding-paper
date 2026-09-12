#!/usr/bin/env python3
"""T3 (BLOCKING) — P5 mechanism on the apo arm.

Per plan line 177 (`docs/BLOCK_C_LIGAND_BLOCK_PLAN_2026_09_03.md`) the P5
null is defined as:

    | decoy_lig+apo − full_agonist+apo | < 0.15

on the two-instrument binary predicate. The v5 report attributes the P5
null to **ceiling saturation on the cognate arm** — but P5 is measured on
the apo arm. Different arms.

T3 asks:

  T3b — is the apo arm floor-pinned (fraction_active near 0) or
        dispersed?
  T3c — is the cognate arm actually ceiling-pinned (fraction_active near 1),
        as the report claims?
  T3d — if the apo arm is neither floor- nor ceiling-pinned, revive the P5
        null as a live claim with a proper CI.
  T3e — decompose the 2×2 pocket-Cα-RMSD interaction into apo-only and
        cognate-only fits. If the identity signal is present in the apo
        arm alone, that's compatible with a live apo-P5 null (different
        instrument, same rows). If cognate-only, the pocket-Cα rescue is
        narrower than reported.

Passing rows only. Two-instrument predicate literals from
``scripts/analyse_block_c_tier3_headline.py``:
    NPXXY_OH_LT = 9.082
    TM6_TILT_GT = 14.932
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
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import stage3_post_audit_analysis as s3  # type: ignore  # noqa: E402

ROWS_TIER3 = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_TIER3 = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/reaudit_2026_09_07"
OUT_JSON = OUT_DIR / "t3_p5_mechanism.json"

NPXXY_OH_LT = 9.082
TM6_TILT_GT = 14.932

P5_THRESHOLD = 0.15


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


def is_active(row) -> bool | None:
    oh = _to_float(row.get("d_npxxy_y558_y753_oh"))
    tilt = _to_float(row.get("d_gpcrdb_tm6_tilt_246_637_ca"))
    if math.isnan(oh) or math.isnan(tilt):
        return None
    return (oh < NPXXY_OH_LT) and (tilt > TM6_TILT_GT)


def load_tier3_records() -> list[dict]:
    print("[T3] loading rows.tier3.v2.csv + manifest.tier3.v2.csv...")
    rows = pd.read_csv(ROWS_TIER3, low_memory=False)
    manifest = pd.read_csv(MANIFEST_TIER3, low_memory=False)
    m_idx = manifest.set_index("prediction_path")
    rows["backbone"] = rows["input_path"].map(m_idx["backbone"].to_dict()).fillna("")
    rows["partner_type"] = rows["input_path"].map(m_idx["partner_type"].to_dict()).fillna("")
    for col in ("ligand_role", "ligand_bound_pdb"):
        if col in m_idx.columns:
            fb = rows.get(col, pd.Series([""] * len(rows)))
            rows[col] = rows["input_path"].map(m_idx[col].to_dict()).fillna(fb)
    rows["arm"] = rows["partner_type"].apply(
        lambda p: "apo" if str(p).lower() == "apo" else "cognate"
    )
    return rows.astype(str).to_dict("records")


def fraction_active_per_cell(records: list[dict]) -> dict:
    """(receptor, backbone, ligand_role, arm) -> per-cell fraction and count."""
    d: dict[tuple[str, str, str, str], list[int]] = defaultdict(list)
    for r in records:
        if str(r.get("passed", "")).lower() != "true":
            continue
        if (r.get("receptor_class") or "").upper() != "A":
            continue
        rec = (r.get("receptor_slug") or "").upper()
        bb = (r.get("backbone") or "").lower()
        lr = (r.get("ligand_role") or "").strip()
        arm = (r.get("arm") or "").strip()
        v = is_active(r)
        if v is None:
            continue
        d[(rec, bb, lr, arm)].append(1 if v else 0)
    out = {}
    for k, vs in d.items():
        out[k] = {
            "n": len(vs),
            "n_active": sum(vs),
            "fraction": sum(vs) / len(vs) if vs else float("nan"),
        }
    return out


def summarize_arm(fracs: dict, arm: str, ligand_roles: list[str]) -> dict:
    """Return per-backbone histogram + moments for the requested arm."""
    per_bb: dict[str, dict] = {}
    for bb in sorted({k[1] for k in fracs.keys()}):
        for lr in ligand_roles:
            cells = [
                cell["fraction"] for (rec, b, l, a), cell in fracs.items()
                if b == bb and l == lr and a == arm and not math.isnan(cell["fraction"])
            ]
            if not cells:
                continue
            per_bb.setdefault(bb, {})[lr] = {
                "n_cells": len(cells),
                "min": float(min(cells)),
                "max": float(max(cells)),
                "mean": float(statistics.mean(cells)),
                "median": float(statistics.median(cells)),
                "n_pinned_at_0": sum(1 for f in cells if f <= 0.01),
                "n_pinned_at_1": sum(1 for f in cells if f >= 0.99),
                "n_dispersed": sum(1 for f in cells if 0.05 < f < 0.95),
                "histogram_deciles": {
                    f"{i/10:.1f}-{(i+1)/10:.1f}": sum(
                        1 for f in cells if i / 10 <= f < (i + 1) / 10
                    ) for i in range(10)
                } | {
                    "1.0": sum(1 for f in cells if f >= 1.0),
                },
            }
    return per_bb


def cluster_bootstrap_apo_p5(
    fracs: dict, n_iter: int = 5000, seed: int = 20260907
) -> dict:
    """For each backbone, cluster-bootstrap the mean of |Δ| where
    Δ = fraction(decoy_lig+apo, receptor) − fraction(full_agonist+apo, receptor).
    """
    per_bb: dict[str, dict] = {}
    rng = np.random.default_rng(seed)
    for bb in sorted({k[1] for k in fracs.keys()}):
        deltas: list[float] = []
        per_receptor: list[dict] = []
        for rec in sorted({k[0] for k in fracs.keys() if k[1] == bb}):
            d = fracs.get((rec, bb, "decoy_lig", "apo"))
            a = fracs.get((rec, bb, "full_agonist", "apo"))
            if not d or not a:
                continue
            delta = d["fraction"] - a["fraction"]
            deltas.append(delta)
            per_receptor.append({
                "receptor": rec,
                "frac_decoy": d["fraction"],
                "frac_agonist": a["fraction"],
                "delta": delta,
                "abs_delta": abs(delta),
            })
        if not deltas:
            per_bb[bb] = {"n": 0, "reason": "no_receptors"}
            continue
        abs_deltas = np.array([abs(d) for d in deltas])
        n = len(abs_deltas)
        reps = np.empty(n_iter, dtype=float)
        for i in range(n_iter):
            idx = rng.integers(0, n, size=n)
            reps[i] = float(np.mean(abs_deltas[idx]))
        lo, hi = np.percentile(reps, [2.5, 97.5])
        pt = float(np.mean(abs_deltas))
        per_bb[bb] = {
            "n_receptors": int(n),
            "abs_delta_mean": pt,
            "ci_lo": float(lo),
            "ci_hi": float(hi),
            "ci_clears_zero_above_threshold": bool(lo > P5_THRESHOLD),
            "point_below_threshold": bool(pt < P5_THRESHOLD),
            "per_receptor": per_receptor,
        }
    return per_bb


def decompose_2x2_by_arm(records: list[dict]) -> dict:
    """Run stage3a_2x2 restricted to apo-only rows and cognate-only rows,
    and report both."""
    apo_records = [r for r in records if (r.get("arm") or "").strip() == "apo"]
    cog_records = [r for r in records if (r.get("arm") or "").strip() == "cognate"]
    return {
        "apo_only": s3.stage3a_2x2(apo_records),
        "cognate_only": s3.stage3a_2x2(cog_records),
        "n_rows_apo": len(apo_records),
        "n_rows_cognate": len(cog_records),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(OUT_JSON))
    args = parser.parse_args()

    # T3a — prereg quotation.
    prereg_quote = {
        "source": "docs/BLOCK_C_LIGAND_BLOCK_PLAN_2026_09_03.md line 177",
        "text": "P5 (null): decoy_lig+apo ≈ agonist+apo, |Δ| < 0.15",
        "arm": "apo",
        "instrument": "two-instrument binary predicate (NPXXY-OH < 9.082 AND TM6 tilt > 14.932)",
    }

    records = load_tier3_records()
    print(f"[T3] {len(records)} records loaded")

    # T3b + T3c — per-cell fraction distributions.
    print("[T3bc] per-cell fraction-active distributions...")
    fracs = fraction_active_per_cell(records)
    apo_summary = summarize_arm(
        fracs, arm="apo",
        ligand_roles=["decoy_lig", "full_agonist", "neutral_antagonist"],
    )
    cog_summary = summarize_arm(
        fracs, arm="cognate",
        ligand_roles=["decoy_lig", "full_agonist", "neutral_antagonist"],
    )

    # T3d — apo P5 |Δ| with clean-room bootstrap CI.
    print("[T3d] apo P5 |Δ| per-backbone with CI...")
    p5_apo = cluster_bootstrap_apo_p5(fracs)
    for bb, r in p5_apo.items():
        if "abs_delta_mean" not in r:
            print(f"  {bb:<10} {r}")
            continue
        print(f"  {bb:<10} n={r['n_receptors']:>2} |Δ|={r['abs_delta_mean']:.4f} "
              f"CI=[{r['ci_lo']:.4f}, {r['ci_hi']:.4f}] "
              f"point_below_threshold={r['point_below_threshold']}")

    # T3e — 2×2 arm decomposition.
    print("[T3e] decomposing 2×2 into apo-only and cognate-only...")
    arm_decomp = decompose_2x2_by_arm(records)
    for arm in ("apo_only", "cognate_only"):
        print(f"  {arm}:")
        for bb, d in arm_decomp[arm].get("per_backbone", {}).items():
            interaction = d.get("interaction", {})
            print(
                f"    {bb:<10} Δ={interaction.get('estimate', float('nan')):+.3f} "
                f"CI=[{interaction.get('ci_lo', float('nan')):+.3f}, "
                f"{interaction.get('ci_hi', float('nan')):+.3f}]  "
                f"n_common={interaction.get('n_receptors_in_common', 0)} "
                f"signed_nonzero={interaction.get('signed_nonzero', False)}"
            )

    # Diagnosis.
    diagnosis = {}
    for bb, r in p5_apo.items():
        if "abs_delta_mean" not in r:
            continue
        # Look at what the apo arm looks like.
        apo_decoy = apo_summary.get(bb, {}).get("decoy_lig", {})
        apo_agon = apo_summary.get(bb, {}).get("full_agonist", {})
        # A floor-pinned distribution has n_pinned_at_0 >> n_dispersed.
        # A ceiling-pinned distribution has n_pinned_at_1 >> n_dispersed.
        # Otherwise it's dispersed.
        def _which(s: dict) -> str:
            if not s:
                return "empty"
            n = s.get("n_cells", 0)
            if not n:
                return "empty"
            p0 = s.get("n_pinned_at_0", 0) / n
            p1 = s.get("n_pinned_at_1", 0) / n
            pd_ = s.get("n_dispersed", 0) / n
            if p0 > 0.7:
                return f"FLOOR_PINNED (p0={p0:.2f})"
            if p1 > 0.7:
                return f"CEILING_PINNED (p1={p1:.2f})"
            return f"DISPERSED (p0={p0:.2f} p1={p1:.2f} p_disp={pd_:.2f})"
        diagnosis[bb] = {
            "apo_decoy_state": _which(apo_decoy),
            "apo_agonist_state": _which(apo_agon),
            "abs_delta_apo": r["abs_delta_mean"],
            "abs_delta_ci": [r["ci_lo"], r["ci_hi"]],
            "below_threshold": r["point_below_threshold"],
        }

    # Verdict on Withdrawal #1.
    #
    # If BOTH apo cells are floor-pinned across most backbones AND the apo |Δ|
    # is below P5_THRESHOLD: withdrawal is CORRECTLY_WITHDRAWN but the report's
    # cited *mechanism* is misdescribed (floor pinning, not ceiling saturation).
    #
    # If neither pinning holds and |Δ| is above threshold: WITHDRAWN_ON_FALSE_PREMISE.
    n_floor_pinned = sum(
        1 for bb, d in diagnosis.items()
        if d["apo_decoy_state"].startswith("FLOOR_PINNED")
        and d["apo_agonist_state"].startswith("FLOOR_PINNED")
    )
    n_below_threshold = sum(1 for bb, d in diagnosis.items() if d["below_threshold"])

    if n_below_threshold == len(diagnosis):
        if n_floor_pinned >= 3:
            verdict = "WITHDRAWN_BUT_MECHANISM_MISDESCRIBED"
            verdict_note = (
                "P5 null holds on all 4 backbones (|Δ| < 0.15). But the mechanism "
                "cited in v5 §3.3/§4.1 is 'ceiling saturation on the cognate arm', "
                "and P5 is defined on the apo arm. The apo arm is FLOOR-pinned, "
                "not ceiling-pinned. Withdrawal #1 stands; its stated mechanism "
                "does not."
            )
        else:
            verdict = "CORRECTLY_WITHDRAWN"
            verdict_note = "P5 null holds on all backbones; mechanism unresolved."
    else:
        verdict = "WITHDRAWN_ON_FALSE_PREMISE"
        verdict_note = (
            "P5 null does not hold on all backbones. Withdrawal #1 was made on a "
            "false premise. Report apo-arm |Δ| with CIs as a live claim."
        )

    report = {
        "task": "T3_p5_mechanism",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows_tier3": {
                "path": str(ROWS_TIER3.relative_to(REPO)),
                "sha256": sha256_file(ROWS_TIER3),
            },
            "manifest_tier3": {
                "path": str(MANIFEST_TIER3.relative_to(REPO)),
                "sha256": sha256_file(MANIFEST_TIER3),
            },
        },
        "t3a_prereg": prereg_quote,
        "t3b_apo_arm_summary": apo_summary,
        "t3c_cognate_arm_summary": cog_summary,
        "t3d_apo_p5": p5_apo,
        "t3e_2x2_by_arm": arm_decomp,
        "diagnosis": diagnosis,
        "verdict": verdict,
        "verdict_note": verdict_note,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[T3] wrote {Path(args.out).relative_to(REPO)}")
    print()
    print("=" * 78)
    print("T3 — apo arm P5 diagnosis")
    print("=" * 78)
    for bb, d in diagnosis.items():
        print(
            f"  {bb:<10} decoy_apo: {d['apo_decoy_state']:<35} "
            f"agon_apo: {d['apo_agonist_state']:<35}  "
            f"|Δ|={d['abs_delta_apo']:.4f} CI=[{d['abs_delta_ci'][0]:.4f}, {d['abs_delta_ci'][1]:.4f}]"
        )
    print()
    print("Verdict on Withdrawal #1:", verdict)
    print(verdict_note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
