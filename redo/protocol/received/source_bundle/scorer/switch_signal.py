"""Switch-signal analysis for Block A — PREREG-compliant.

Implements the delta_d_tm6(cognate - apo) primary result per
`refs/PREREG.md §3`, and the two-instrument success rule per §2a-c.

Core rules from PREREG.md, made concrete here:

1. **Seed is the unit of variance.**
   For each (receptor, backbone, arm), collapse rows to per-seed means
   FIRST, then compute means / bootstrap CIs over seeds. Never subtract
   individual rows across arms (seeds are not matched between arms —
   row-wise pairing would fabricate structure).

2. **Two-instrument success.** For Class A (default), a prediction is
   "active-like" iff ≥3 of the 5 motif metrics cross their threshold in
   the active direction AND `confidence_flag != "low"`. For tier-1
   Class B / F, it's midpoint-crossing on the per-class anchor pair.

3. **Unmeasurable-metric behaviour.** NaN metric ⇒ count against the
   ≥3-of-5 threshold as a fail (never pass-by-default). ≥2 NaN metrics
   in a row ⇒ drop with `metric_coverage_insufficient`, excluded from
   the receptor's numerator AND denominator.

4. **Δd_tm6**. Per (receptor, backbone):
       cog_mu   = mean over seeds in cognate arm
       apo_mu   = mean over seeds in apo arm
       delta    = cog_mu − apo_mu
       CI       = bootstrap over seeds (10,000 resamples, 2.5/97.5 pctile)

Everything here is a **pure function** — no I/O, no CSV parsing. Test
independently. Analysis script wrapper lives at
`scripts/analyse_switch_signal.py`.
"""
from __future__ import annotations

import math
import random
import statistics
from collections import defaultdict
from typing import Iterable, Sequence


# =====================================================================
# Threshold table — populated from refs/thresholds_sourced.md by Step 2
# Placeholder values; DO NOT USE for Block A until user reviews and
# locks them in refs/PREREG.md §2b.
# =====================================================================

class MotifThresholds:
    """Per-metric threshold + direction for the motif instrument.

    direction "active_gt" means: predicted active-like iff metric > threshold.
    direction "active_lt" means: predicted active-like iff metric < threshold.

    Thresholds locked 2026-09-01 from tier-1 crystal panel — see
    `refs/thresholds_panel.csv` and `docs/BLOCK_A_STEP3_VALIDATION_2026_09_01.md`.

    **Composite collapsed to single-metric NPxxY-OH** after item-3
    validation surfaced:
    - **DRY is TM6 re-measured** (Pearson r = +0.913 vs d_tm6_r350_r630_ca).
      Not an independent axis. Kept as reported diagnostic only.
    - **NPxxY-OH and Y5.58-pack are collinear** (r = +0.784 across 70 rows).
      Y5.58-pack self-classification is 71.1% (17/37 inactive-called-active
      — high false-positive rate). Kept as reported diagnostic only.
    - **TM5 outward and ICL2 helicity are broken** on this panel
      (separation ≤ 0.1 Å / 0.02 fraction, ICL2 fractionally inverted).
      Dropped in the prior calibration pass.

    NPxxY-OH alone reaches 94.3% self-classification (32/36 A→A, 34/34 I→I)
    and covers 70/80 tier-1 rows (10 receptors have non-Tyr at 5.58 or 7.53).
    This becomes the motif instrument. Cross-validated against the midpoint-
    crossing instrument on d_tm6 (Pearson r = −0.681 — independent enough to
    carry non-redundant signal).
    """

    # Panel-derived midpoints (locked 2026-09-01).
    NPXXY_OH_OH_ACTIVE_LT = 9.08     # panel; midpoint of active/inactive means (5.28, 12.88)

    # Kept for reference/reporting but NOT in the composite:
    NPXXY_CA_CA_ACTIVE_LT = 16.57    # panel; only +4.00 Å separation
    Y558_PACK_ACTIVE_LT = 4.37       # panel; 71.1% self-classification, weak inactive-side
    DRY_IONIC_LOCK_ACTIVE_GT = 11.54 # panel; r=+0.913 with d_tm6 (not independent)

    METRIC_SPECS = (
        # (column_name, threshold, direction, human_label)
        ("d_npxxy_y558_y753_oh", NPXXY_OH_OH_ACTIVE_LT, "active_lt", "NPxxY OH-OH"),
    )
    """Single-metric motif instrument as of 2026-09-01. See docstring.

    Reported-diagnostic metrics (NOT in predicate): NPxxY CA-CA, Y5.58 pack,
    DRY ionic lock, TM5 outward, ICL2 helicity. All emitted in the scorer
    row; consult those independently, don't fold them into the success call.
    """

    K_OF_N = 1
    """With one metric in the composite, K=1 (must pass). Kept parameterized
    so re-adding metrics (A100, GPCRdb tilt, Class B kink) is a config change,
    not a code change."""

    MAX_MISSING = 0
    """No NaN tolerance with a single-metric composite — a NaN NPxxY-OH
    (non-Tyr at 5.58 or 7.53) means the receptor cannot be scored on this
    instrument and drops with `metric_coverage_insufficient`. Falls back to
    midpoint-crossing (d_tm6) as the sole active-call for those receptors."""


# =====================================================================
# Row-level classifier
# =====================================================================

def prediction_is_active_like(row: dict) -> str:
    """Returns "active" / "inactive" / "insufficient".

    Applies PREREG §2a k-of-n rule with NaN-as-fail semantics.
    """
    if (row.get("confidence_flag") or "").lower() == "low":
        return "inactive"     # conservative: low-conf never counts as active-like

    n_pass = 0
    n_nan = 0
    for col, thr, direction, _ in MotifThresholds.METRIC_SPECS:
        val = _to_float(row.get(col, ""))
        if math.isnan(val):
            n_nan += 1
            continue
        if direction == "active_gt" and val > thr:
            n_pass += 1
        elif direction == "active_lt" and val < thr:
            n_pass += 1
    if n_nan > MotifThresholds.MAX_MISSING:
        return "insufficient"
    return "active" if n_pass >= MotifThresholds.K_OF_N else "inactive"


def _to_float(x) -> float:
    try:
        v = float(x)
        return v if not math.isnan(v) else math.nan
    except (ValueError, TypeError):
        return math.nan


# =====================================================================
# Per-seed aggregation
# =====================================================================

def per_seed_mean(rows: Sequence[dict], value_col: str,
                  seed_col: str = "seed_used") -> dict[str, float]:
    """Group rows by seed_used, mean over samples within a seed.

    Returns {seed_id: mean_over_samples}. Seeds with all-NaN values
    are dropped (not returned).
    """
    by_seed: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        seed = r.get(seed_col, "").strip()
        if not seed:
            continue
        val = _to_float(r.get(value_col, ""))
        if not math.isnan(val):
            by_seed[seed].append(val)
    return {s: statistics.mean(vs) for s, vs in by_seed.items() if vs}


# =====================================================================
# Bootstrap CI over seeds
# =====================================================================

def bootstrap_ci(values: Sequence[float], n_boot: int = 10000,
                 alpha: float = 0.05, rng_seed: int = 42) -> tuple[float, float]:
    """Percentile bootstrap CI over the seed-level values.

    Not row-level. Values here are per-seed means (see `per_seed_mean`).
    """
    if len(values) < 2:
        return float("nan"), float("nan")
    rng = random.Random(rng_seed)
    n = len(values)
    means = []
    for _ in range(n_boot):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo_idx = int(n_boot * (alpha / 2))
    hi_idx = int(n_boot * (1 - alpha / 2))
    return means[lo_idx], means[hi_idx - 1]


# =====================================================================
# Δd_tm6(cognate − apo) per (receptor, backbone)
# =====================================================================

def delta_d_tm6_per_cell(cognate_rows: Sequence[dict],
                         apo_rows: Sequence[dict],
                         *, value_col: str = "d_tm6_r350_r630_ca",
                         seed_col: str = "seed_used"
                         ) -> dict[str, float]:
    """Compute Δd_tm6(cognate − apo) with seed as unit of variance.

    Returns dict with:
      cog_mu, cog_n_seeds, cog_ci_lo, cog_ci_hi
      apo_mu, apo_n_seeds, apo_ci_lo, apo_ci_hi
      delta_mu, delta_ci_lo, delta_ci_hi

    Bootstrap CIs are computed over seeds independently for cognate and
    apo, and over seed-pairs for delta (each bootstrap round samples
    seeds from both arms independently, computes both arm means,
    subtracts). This mirrors PREREG §3 — no cross-arm seed pairing.
    """
    cog_per_seed = per_seed_mean(cognate_rows, value_col, seed_col)
    apo_per_seed = per_seed_mean(apo_rows, value_col, seed_col)

    result = {
        "cog_n_seeds": len(cog_per_seed),
        "apo_n_seeds": len(apo_per_seed),
    }

    if not cog_per_seed or not apo_per_seed:
        for k in ("cog_mu", "cog_ci_lo", "cog_ci_hi", "apo_mu", "apo_ci_lo",
                  "apo_ci_hi", "delta_mu", "delta_ci_lo", "delta_ci_hi"):
            result[k] = float("nan")
        return result

    cog_vals = list(cog_per_seed.values())
    apo_vals = list(apo_per_seed.values())

    result["cog_mu"] = statistics.mean(cog_vals)
    result["apo_mu"] = statistics.mean(apo_vals)
    result["delta_mu"] = result["cog_mu"] - result["apo_mu"]

    result["cog_ci_lo"], result["cog_ci_hi"] = bootstrap_ci(cog_vals)
    result["apo_ci_lo"], result["apo_ci_hi"] = bootstrap_ci(apo_vals)

    # Delta CI: bootstrap seeds independently in each arm, subtract, repeat.
    rng = random.Random(43)
    deltas = []
    for _ in range(10000):
        c = [cog_vals[rng.randrange(len(cog_vals))] for _ in range(len(cog_vals))]
        a = [apo_vals[rng.randrange(len(apo_vals))] for _ in range(len(apo_vals))]
        deltas.append(sum(c) / len(c) - sum(a) / len(a))
    deltas.sort()
    result["delta_ci_lo"] = deltas[250]     # 2.5 percentile
    result["delta_ci_hi"] = deltas[9749]    # 97.5 percentile

    return result


# =====================================================================
# Panel-level rollup
# =====================================================================

def per_receptor_backbone_rollup(all_rows: Iterable[dict], *,
                                 arm_col: str = "arm",
                                 receptor_col: str = "receptor_slug",
                                 backbone_col: str = "backbone",
                                 cognate_arm_val: str = "cognate",
                                 apo_arm_val: str = "apo",
                                 ) -> dict[tuple[str, str], dict[str, float]]:
    """Roll up rows into per-(receptor, backbone) Δd_tm6 statistics.

    Rows must carry an `arm` column with values including 'cognate'
    and 'apo' (customizable). Shuffled/decoy arm rows are ignored by
    this function — analyse them separately.
    """
    by_cell: dict[tuple[str, str], dict[str, list[dict]]] = defaultdict(
        lambda: {"cognate": [], "apo": []})
    for r in all_rows:
        arm = (r.get(arm_col) or "").strip()
        rcp = (r.get(receptor_col) or "").strip()
        bb = (r.get(backbone_col) or "").strip()
        if not (rcp and bb):
            continue
        if arm == cognate_arm_val:
            by_cell[(rcp, bb)]["cognate"].append(r)
        elif arm == apo_arm_val:
            by_cell[(rcp, bb)]["apo"].append(r)

    out: dict[tuple[str, str], dict[str, float]] = {}
    for cell, arms in by_cell.items():
        out[cell] = delta_d_tm6_per_cell(arms["cognate"], arms["apo"])
    return out
