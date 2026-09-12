"""Step 3 — cross-validate motif-based vs midpoint-based success on tier-1 receptors.

Runs on the (m,n) consensus predictions already in `experiments/mn_consensus/`.
The motif-based rule requires the new NPxxY OH-OH column (agent-in-flight) and
panel-derived thresholds (agent-in-flight). Until both are ready, the script
gracefully reports "PENDING" per metric and exits.

Purpose (PREREG §3): on tier-1 receptors, both success definitions are
computable. If they agree, motif-based scoring is validated for extension
to tier-2. If they disagree, that surfaces BEFORE Block A dispatch.

Usage:
    python3 scripts/step3_cross_validate_instruments.py \\
        --experiments-root experiments/mn_consensus \\
        --reference-set refs/reference_set.csv \\
        --thresholds refs/thresholds_sourced.md \\
        --out docs/BLOCK_A_STEP3_CROSSVAL_2026_09_01.md
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scorer.switch_signal import (
    MotifThresholds,
    prediction_is_active_like,
)


def _to_float(x) -> float:
    try:
        v = float(x)
        return v if not math.isnan(v) else math.nan
    except (ValueError, TypeError):
        return math.nan


# =====================================================================
# Panel-threshold derivation (once NPxxY refs are populated)
# =====================================================================

def derive_panel_thresholds(reference_set_csv: Path) -> dict[str, dict]:
    """Compute panel-derived thresholds per motif metric from tier-1 crystals.

    For each metric that has a `<column>_ref` column in reference_set.csv:
    - Collect ACTIVE values across all tier-1 active refs.
    - Collect INACTIVE values across all tier-1 inactive refs.
    - Threshold = midpoint((mean(active), mean(inactive))).
    - Report ±20% sensitivity range.

    Returns dict: {metric_name: {"threshold": float, "direction": str,
                                 "n_active": int, "n_inactive": int,
                                 "active_mean": float, "inactive_mean": float,
                                 "sensitivity_lo": float, "sensitivity_hi": float,
                                 "status": "ok" | "missing_data"}}
    """
    rows = list(csv.DictReader(reference_set_csv.open()))
    active_rows = [r for r in rows if r["role"] == "active"]
    inactive_rows = [r for r in rows if r["role"] == "inactive"]

    metric_ref_cols = {
        "d_npxxy_y558_y753_oh": "d_npxxy_oh_ref",
        "d_npxxy_y558_y753_ca": "d_npxxy_ca_ref",
        "d_y558_pack_min_heavy": "d_y558_pack_ref",
        "d_dry_sidechain_r350cz_e630oe1": "d_dry_ref",
        "d_tm5_outward_r350_r558_ca": "d_tm5_out_ref",
        "icl2_helical_frac": "icl2_helical_ref",
    }

    directions = dict(
        (col, dr) for col, thr, dr, _ in MotifThresholds.METRIC_SPECS
    )
    directions["d_npxxy_y558_y753_ca"] = "active_lt"

    result = {}
    for metric, ref_col in metric_ref_cols.items():
        if ref_col is None:
            result[metric] = {"status": "no_ref_column_in_schema"}
            continue

        active_vals = [_to_float(r.get(ref_col, "")) for r in active_rows]
        active_vals = [v for v in active_vals if not math.isnan(v)]
        inactive_vals = [_to_float(r.get(ref_col, "")) for r in inactive_rows]
        inactive_vals = [v for v in inactive_vals if not math.isnan(v)]

        if not active_vals or not inactive_vals:
            result[metric] = {
                "status": "missing_data",
                "n_active": len(active_vals),
                "n_inactive": len(inactive_vals),
            }
            continue

        active_mean = statistics.mean(active_vals)
        inactive_mean = statistics.mean(inactive_vals)
        threshold = (active_mean + inactive_mean) / 2.0

        result[metric] = {
            "status": "ok",
            "threshold": threshold,
            "direction": directions.get(metric, "unknown"),
            "n_active": len(active_vals),
            "n_inactive": len(inactive_vals),
            "active_mean": active_mean,
            "inactive_mean": inactive_mean,
            "active_std": statistics.stdev(active_vals) if len(active_vals) > 1 else 0.0,
            "inactive_std": statistics.stdev(inactive_vals) if len(inactive_vals) > 1 else 0.0,
            "sensitivity_lo": threshold * 0.8,
            "sensitivity_hi": threshold * 1.2,
        }
    return result


# =====================================================================
# Apply panel thresholds to MotifThresholds and re-invoke k-of-n
# =====================================================================

def install_panel_thresholds(panel: dict[str, dict]):
    """Overwrite MotifThresholds placeholders with panel-derived values.

    Skips metrics where panel data is unavailable — those metrics won't
    contribute to the k-of-n predicate below.
    """
    active_metrics = []
    for col, thr, dr, label in MotifThresholds.METRIC_SPECS:
        info = panel.get(col, {})
        if info.get("status") == "ok":
            new_thr = info["threshold"]
            active_metrics.append((col, new_thr, dr, label))
    if active_metrics:
        MotifThresholds.METRIC_SPECS = tuple(active_metrics)
        MotifThresholds.K_OF_N = min(3, len(active_metrics))


# =====================================================================
# Midpoint-based success (single-instrument, TM6-axis)
# =====================================================================

def midpoint_active_like(row: dict) -> str:
    d_tm6 = _to_float(row.get("d_tm6_r350_r630_ca", ""))
    midpoint = _to_float(row.get("receptor_midpoint", ""))
    conf = (row.get("confidence_flag", "") or "").lower()
    if math.isnan(d_tm6) or math.isnan(midpoint):
        return "insufficient"
    if conf == "low":
        return "inactive"    # conservative parallel to motif
    return "active" if d_tm6 > midpoint else "inactive"


# =====================================================================
# GPCRdb TM6 tilt success (single-instrument, cross-class mechanics axis)
# =====================================================================
#
# PREREG §2c-locked replacement for the d_tm6 midpoint instrument.
# Panel-derived threshold from refs/thresholds_panel.csv (fc430fa lock).
# Direction: active_gt (TM6 tilts outward on activation; the |Δ| between
# active and inactive means is 5.33 Å over the 80-row tier-1 panel).
# =====================================================================

GPCRDB_TILT_ACTIVE_GT = 14.932  # refs/thresholds_panel.csv, 2026-09-01

def gpcrdb_tilt_active_like(row: dict,
                            threshold: float = GPCRDB_TILT_ACTIVE_GT) -> str:
    """Panel-threshold classifier on d_gpcrdb_tm6_tilt_246_637_ca.

    Mirrors midpoint_active_like's semantics: NaN → insufficient,
    confidence_flag == 'low' → inactive.
    """
    tilt = _to_float(row.get("d_gpcrdb_tm6_tilt_246_637_ca", ""))
    conf = (row.get("confidence_flag", "") or "").lower()
    if math.isnan(tilt):
        return "insufficient"
    if conf == "low":
        return "inactive"
    return "active" if tilt > threshold else "inactive"


# =====================================================================
# Agreement matrix on tier-1 receptors from existing (m,n) predictions
# =====================================================================

def cross_validate(experiments_root: Path,
                   panel_thresholds: dict[str, dict],
                   *, dual: bool = False) -> dict:
    """For every prediction with both motif metrics AND midpoint data,
    compute both success labels and build the agreement matrix.

    When dual=True, also compute the NPxxY-vs-GPCRdb-tilt matrix
    (the PREREG §2c post-swap instrument pair).
    """
    install_panel_thresholds(panel_thresholds)

    matrix = defaultdict(int)  # (motif, midpoint) -> count
    matrix_tilt = defaultdict(int)  # (motif, gpcrdb_tilt) -> count
    n_examined = 0
    per_backbone = defaultdict(lambda: defaultdict(int))
    per_receptor = defaultdict(lambda: defaultdict(int))
    per_backbone_tilt = defaultdict(lambda: defaultdict(int))
    per_receptor_tilt = defaultdict(lambda: defaultdict(int))

    for rows_csv in sorted(experiments_root.rglob("rows.csv")):
        if "_legacy" in rows_csv.parts:
            continue
        # Guard against empty per-experiment marker files.
        try:
            reader = csv.DictReader(rows_csv.open())
        except Exception:
            continue
        for row in reader:
            motif = prediction_is_active_like(row)
            mid = midpoint_active_like(row)
            key = (motif, mid)
            matrix[key] += 1
            per_backbone[row.get("backbone", "unknown")][key] += 1
            per_receptor[row.get("receptor_slug", "unknown")][key] += 1
            n_examined += 1
            if dual:
                tilt = gpcrdb_tilt_active_like(row)
                key_t = (motif, tilt)
                matrix_tilt[key_t] += 1
                per_backbone_tilt[row.get("backbone", "unknown")][key_t] += 1
                per_receptor_tilt[row.get("receptor_slug", "unknown")][key_t] += 1

    out = {
        "n_examined": n_examined,
        "matrix": dict(matrix),
        "per_backbone": {k: dict(v) for k, v in per_backbone.items()},
        "per_receptor": {k: dict(v) for k, v in per_receptor.items()},
    }
    if dual:
        out["matrix_tilt"] = dict(matrix_tilt)
        out["per_backbone_tilt"] = {k: dict(v) for k, v in per_backbone_tilt.items()}
        out["per_receptor_tilt"] = {k: dict(v) for k, v in per_receptor_tilt.items()}
    return out


# =====================================================================
# Report
# =====================================================================

def _format_matrix(matrix: dict, title: str, col_label: str) -> list[str]:
    lines = [
        f"### {title}",
        "",
        f"|  | {col_label}: active | {col_label}: inactive | {col_label}: insufficient |",
        "|---|---:|---:|---:|",
    ]
    for motif_label in ("active", "inactive", "insufficient"):
        row = f"| **motif: {motif_label}** "
        for other_label in ("active", "inactive", "insufficient"):
            row += f"| {matrix.get((motif_label, other_label), 0)} "
        row += "|"
        lines.append(row)
    n_matrix = sum(matrix.values())
    if n_matrix:
        agree = (matrix.get(("active", "active"), 0) +
                 matrix.get(("inactive", "inactive"), 0))
        lines += ["",
                  f"**Overall agreement** (active↔active + inactive↔inactive): "
                  f"{agree}/{n_matrix} = {100*agree/n_matrix:.1f}%"]
    n_insuf = sum(v for (a, b), v in matrix.items()
                  if a == "insufficient" or b == "insufficient")
    if n_insuf:
        lines += [f"**insufficient rows** (motif OR {col_label} NaN/insufficient): "
                  f"{n_insuf}/{n_matrix}"]
    return lines


def write_report_dual(out_path: Path, panel: dict, xval: dict,
                      reference_set_csv: Path, experiments_root: Path) -> None:
    """Post-swap report: emits BOTH agreement matrices side-by-side —
    (NPxxY vs d_tm6 midpoint) and (NPxxY vs GPCRdb tilt panel threshold).
    """
    lines = [
        "# Block A Step 3 (POST-SWAP) — dual-instrument cross-validation",
        "",
        "**Date**: 2026-09-01",
        f"**Inputs**: {reference_set_csv}, predictions under {experiments_root}",
        "**Predicate lock**: PREREG §2c — NPxxY-OH motif + GPCRdb TM6 tilt mechanics",
        "",
        "This is the post-swap variant of the PREREG §3 cross-validation. It",
        "compares the OLD mechanics axis (per-receptor d_tm6 midpoint from the",
        "reference_set) against the NEW mechanics axis (single panel-derived",
        "threshold on GPCRdb TM6 tilt) using the same NPxxY-OH motif call",
        "on both sides.",
        "",
        "## 1. Panel-derived thresholds (motif instrument + new mechanics axes)",
        "",
        "| Metric | Direction | Threshold | Sensitivity | Source |",
        "|---|---|---:|---|---|",
    ]
    with (REPO / "refs" / "thresholds_panel.csv").open() as f:
        for row in csv.DictReader(f):
            lines.append(
                f"| {row['metric_col']} | {row['direction']} | "
                f"{row['threshold']} | {row['sensitivity_lo']}–{row['sensitivity_hi']} | "
                f"panel n={row['n_active']}A/{row['n_inactive']}I |"
            )

    lines += ["",
              f"## 2. Agreement matrices (N = {xval['n_examined']} predictions)",
              "",
              "Both matrices use the SAME NPxxY-OH motif call on the rows axis.",
              "The columns axis differs between the two:",
              "  * OLD: per-receptor d_tm6 midpoint from reference_set.",
              "  * NEW: panel-derived threshold (14.932 Å) on d_gpcrdb_tm6_tilt.",
              ""]
    lines += _format_matrix(xval["matrix"], "2a. OLD instrument (NPxxY vs d_tm6 midpoint)",
                            "d_tm6 midpoint")
    lines += [""]
    lines += _format_matrix(xval["matrix_tilt"],
                            "2b. NEW instrument (NPxxY vs GPCRdb TM6 tilt)",
                            "GPCRdb tilt")

    # Delta summary
    old = xval["matrix"]
    new = xval["matrix_tilt"]
    n_old = sum(old.values())
    n_new = sum(new.values())
    a_old = old.get(("active", "active"), 0) + old.get(("inactive", "inactive"), 0)
    a_new = new.get(("active", "active"), 0) + new.get(("inactive", "inactive"), 0)
    lines += ["",
              "## 3. Swap-effect delta",
              "",
              f"| Instrument | N | Agreement | % |",
              f"|---|---:|---:|---:|",
              f"| OLD (NPxxY vs d_tm6 midpoint) | {n_old} | {a_old} | {100*a_old/n_old:.1f}% |" if n_old else "",
              f"| NEW (NPxxY vs GPCRdb tilt)    | {n_new} | {a_new} | {100*a_new/n_new:.1f}% |" if n_new else "",
              f"| Δ (new − old)                 | – | {a_new - a_old:+d} | {100*(a_new-a_old)/max(n_old,1):+.1f}pp |",
              ]

    lines += ["",
              "## 4. Per-backbone (post-swap NEW instrument)",
              ""]
    for bb in ("boltz", "of3", "protenix", "chai"):
        m = xval.get("per_backbone_tilt", {}).get(bb, {})
        if not m:
            continue
        n = sum(m.values())
        agree = m.get(("active", "active"), 0) + m.get(("inactive", "inactive"), 0)
        pct = 100 * agree / n if n else 0
        lines.append(f"- **{bb}**: {agree}/{n} = {pct:.1f}% agreement")

    lines += ["",
              "## 5. Per-backbone (OLD instrument, for reference)",
              ""]
    for bb in ("boltz", "of3", "protenix", "chai"):
        m = xval.get("per_backbone", {}).get(bb, {})
        if not m:
            continue
        n = sum(m.values())
        agree = m.get(("active", "active"), 0) + m.get(("inactive", "inactive"), 0)
        pct = 100 * agree / n if n else 0
        lines.append(f"- **{bb}**: {agree}/{n} = {pct:.1f}% agreement")

    lines += ["",
              "## 6. Interpretation",
              "",
              "- ≥90 % agreement on the new instrument confirms the PREREG §2c",
              "  swap does not degrade cross-validation.",
              "- Δ close to 0 means the two mechanics axes classify the (m,n)",
              "  predictions the same way — the swap is a lateral move on this",
              "  panel; the *methodological* advantage is that GPCRdb tilt is",
              "  cross-class and panel-normalised (no per-receptor midpoint).",
              "- A large Δ would be the surprise finding; report the sign.",
              ""]
    out_path.write_text("\n".join(l for l in lines if l is not None))
    print(f"wrote {out_path}")


def write_report(out_path: Path, panel: dict, xval: dict,
                 reference_set_csv: Path, experiments_root: Path) -> None:
    lines = [
        "# Block A Step 3 — cross-validation of motif vs midpoint success rules",
        "",
        f"**Date**: 2026-09-01",
        f"**Inputs**: {reference_set_csv}, predictions under {experiments_root}",
        "",
        "This is the PREREG §3 cross-validation. On tier-1 receptors, both",
        "motif-based (k-of-n) and midpoint-based success rules are computable.",
        "Agreement between the two validates extending motif scoring to tier-2.",
        "",
        "## 1. Panel-derived thresholds (per PREREG §2b)",
        "",
        "| Metric | Status | Active mean | Inactive mean | Threshold | Sensitivity |",
        "|---|---|---:|---:|---:|---|",
    ]
    for col, thr, dr, label in MotifThresholds.METRIC_SPECS:
        info = panel.get(col, {})
        if info.get("status") == "ok":
            lines.append(
                f"| {label} | ok (n={info['n_active']}A/{info['n_inactive']}I) "
                f"| {info['active_mean']:.2f} | {info['inactive_mean']:.2f} "
                f"| {info['threshold']:.2f} "
                f"| {info['sensitivity_lo']:.2f}–{info['sensitivity_hi']:.2f} |"
            )
        else:
            lines.append(
                f"| {label} | **PENDING** ({info.get('status','no data')}) | – | – | – | – |"
            )

    lines.extend([
        "",
        f"## 2. Agreement matrix (N = {xval['n_examined']} predictions)",
        "",
        "|  | midpoint: active | midpoint: inactive | midpoint: insufficient |",
        "|---|---:|---:|---:|",
    ])
    for motif_label in ("active", "inactive", "insufficient"):
        row = f"| **motif: {motif_label}** "
        for mid_label in ("active", "inactive", "insufficient"):
            row += f"| {xval['matrix'].get((motif_label, mid_label), 0)} "
        row += "|"
        lines.append(row)

    n_matrix = sum(xval["matrix"].values())
    if n_matrix:
        agree = (xval['matrix'].get(('active', 'active'), 0) +
                 xval['matrix'].get(('inactive', 'inactive'), 0))
        lines.extend([
            "",
            f"**Overall agreement (active↔active + inactive↔inactive)**: "
            f"{agree}/{n_matrix} = {100*agree/n_matrix:.1f}%",
        ])

    lines.extend([
        "",
        "## 3. Interpretation",
        "",
        "- ≥90% agreement → motif and midpoint measure the same latent property.",
        "  Motif-based rule can be extended to Class B/F tier-1 receptors with",
        "  confidence.",
        "- 70-90% agreement → the two instruments carry non-redundant information;",
        "  the composite two-instrument rule (PREREG §2) captures both.",
        "- <70% agreement → one instrument is unreliable. Investigate before dispatch.",
        "",
        "## 4. Per-backbone breakdown",
        "",
    ])
    for bb in ("boltz", "of3", "protenix", "chai"):
        m = xval["per_backbone"].get(bb, {})
        if not m:
            continue
        n = sum(m.values())
        agree = m.get(('active', 'active'), 0) + m.get(('inactive', 'inactive'), 0)
        pct = 100 * agree / n if n else 0
        lines.append(f"- **{bb}**: {agree}/{n} = {pct:.1f}% agreement")

    out_path.write_text("\n".join(lines))
    print(f"wrote {out_path}")


def write_thresholds_panel_csv(panel: dict[str, dict], out_csv: Path) -> None:
    """Emit ``refs/thresholds_panel.csv`` in the schema Step 3 committed on
    2026-09-01 (commit bb567e2). One row per motif metric, active/inactive
    means + panel-derived threshold + ±20 % sensitivity band. A metric with
    ``status != ok`` writes empty numeric fields with the observed n_active /
    n_inactive so a downstream reader can distinguish "not derived yet" from
    "derived, zero separation".
    """
    ref_col_lookup = {
        "d_npxxy_y558_y753_oh": "d_npxxy_oh_ref",
        "d_npxxy_y558_y753_ca": "d_npxxy_ca_ref",
        "d_y558_pack_min_heavy": "d_y558_pack_ref",
        "d_dry_sidechain_r350cz_e630oe1": "d_dry_ref",
        "d_tm5_outward_r350_r558_ca": "d_tm5_out_ref",
        "icl2_helical_frac": "icl2_helical_ref",
    }
    directions = {
        "d_npxxy_y558_y753_oh": "active_lt",
        "d_npxxy_y558_y753_ca": "active_lt",
        "d_y558_pack_min_heavy": "active_lt",
        "d_dry_sidechain_r350cz_e630oe1": "active_gt",
        "d_tm5_outward_r350_r558_ca": "active_gt",
        "icl2_helical_frac": "active_gt",
    }
    ordering = list(ref_col_lookup)

    def _fmt(v):
        if v is None:
            return ""
        try:
            return f"{float(v):.3f}"
        except (TypeError, ValueError):
            return ""

    header = [
        "metric_col", "ref_col", "direction", "status",
        "n_active", "n_inactive",
        "active_mean", "inactive_mean",
        "threshold", "sensitivity_lo", "sensitivity_hi",
    ]
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for metric in ordering:
            info = panel.get(metric, {})
            status = info.get("status", "missing_data")
            w.writerow([
                metric,
                ref_col_lookup[metric],
                directions[metric],
                status if status == "ok" else "PENDING",
                info.get("n_active", 0),
                info.get("n_inactive", 0),
                _fmt(info.get("active_mean")),
                _fmt(info.get("inactive_mean")),
                _fmt(info.get("threshold")),
                _fmt(info.get("sensitivity_lo")),
                _fmt(info.get("sensitivity_hi")),
            ])
    print(f"wrote {out_csv}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--experiments-root", type=Path,
                   default=REPO / "experiments/mn_consensus")
    p.add_argument("--reference-set", type=Path,
                   default=REPO / "refs/reference_set.csv")
    p.add_argument("--out", type=Path, default=None,
                   help="report output path; default depends on --variant")
    p.add_argument("--thresholds-panel-csv", type=Path,
                   default=REPO / "refs/thresholds_panel.csv")
    p.add_argument("--variant", choices=("legacy", "post-swap"), default="legacy",
                   help="legacy: NPxxY vs d_tm6 midpoint only. "
                        "post-swap: also NPxxY vs GPCRdb tilt panel threshold "
                        "(PREREG §2c-locked instrument pair).")
    p.add_argument("--skip-panel-rewrite", action="store_true",
                   help="do not overwrite refs/thresholds_panel.csv "
                        "(the scorer-extension pass already wrote the "
                        "9-metric panel; re-running with the 6-metric "
                        "derivation here would truncate it).")
    args = p.parse_args()

    if args.out is None:
        args.out = (
            REPO / "docs/BLOCK_A_STEP3_CROSSVAL_POST_SWAP_2026_09_01.md"
            if args.variant == "post-swap"
            else REPO / "docs/BLOCK_A_STEP3_CROSSVAL_2026_09_01.md"
        )

    panel = derive_panel_thresholds(args.reference_set)
    if not args.skip_panel_rewrite:
        write_thresholds_panel_csv(panel, args.thresholds_panel_csv)
    dual = args.variant == "post-swap"
    xval = cross_validate(args.experiments_root, panel, dual=dual)
    if dual:
        write_report_dual(args.out, panel, xval, args.reference_set,
                          args.experiments_root)
    else:
        write_report(args.out, panel, xval, args.reference_set,
                     args.experiments_root)

    n_ok = sum(1 for v in panel.values() if v.get("status") == "ok")
    print(f"panel thresholds: {n_ok}/{len(panel)} metrics OK; "
          f"cross-validation over {xval['n_examined']} predictions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
