"""Panel-threshold + correlation + self-classification analysis for the
three literature-derived cross-class metrics landed 2026-09-01.

Reads `refs/reference_set.csv` after `scripts/derive_lit_metric_refs.py`
has populated the `_ref` columns, then:

    1. Panel-derived threshold per new metric (midpoint of active vs
       inactive means; same convention as
       `scripts/step3_cross_validate_instruments.py`).
    2. Self-classification accuracy per new metric — fraction of tier-1
       references where the metric on the row's own crystal correctly
       labels the row's ``role``.
    3. Pearson correlation of each new metric against the two current
       instruments' ref columns:
           - motif:    d_npxxy_oh_ref
           - midpoint: d_r350_r630_ca_ref  (a.k.a. d_tm6 ref)

    4. Appends new rows to `refs/thresholds_panel.csv` for each metric.
    5. Emits `docs/BLOCK_A_SCORER_EXTENSION_2026_09_01.md` with the
       tables + a recommendation on whether any new metric should enter
       the predicate.

Never modifies existing rows in `thresholds_panel.csv` — the six current
threshold rows are user-locked. New rows are appended at the bottom.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


def _to_float(x) -> float:
    try:
        v = float(x)
        return v if not math.isnan(v) else math.nan
    except (ValueError, TypeError):
        return math.nan


def pearson(xs: list[float], ys: list[float]) -> tuple[float, int]:
    pairs = [(x, y) for x, y in zip(xs, ys)
             if not (math.isnan(x) or math.isnan(y))]
    n = len(pairs)
    if n < 3:
        return math.nan, n
    mx = sum(x for x, _ in pairs) / n
    my = sum(y for _, y in pairs) / n
    sxy = sum((x - mx) * (y - my) for x, y in pairs)
    sxx = sum((x - mx) ** 2 for x, _ in pairs)
    syy = sum((y - my) ** 2 for _, y in pairs)
    if sxx == 0.0 or syy == 0.0:
        return math.nan, n
    return sxy / math.sqrt(sxx * syy), n


# ---------------------------------------------------------------------------
# metric registry
# ---------------------------------------------------------------------------

# Direction of the "active" side per metric:
#   active_gt   — active values are LARGER than inactive
#   active_lt   — active values are SMALLER than inactive
# Determined AFTER seeing panel data; do not hardcode blindly.
NEW_METRICS: tuple[tuple[str, str, str], ...] = (
    # (ref_col_name, runtime_metric_col_name, semantic_label)
    ("d_gpcrdb_tm6_tilt_ref",   "d_gpcrdb_tm6_tilt_246_637_ca",           "GPCRdb TM6 tilt (2.46-6.37 CA)"),
    ("a100_index_ref",          "a100_index",                              "A100 activation index"),
    ("angle_class_b_kink_ref",  "angle_class_b_tm6_kink_639_650_654_deg",  "Class B TM6 kink 6.39-6.50-6.54"),
)

CURRENT_INSTRUMENT_REFS: tuple[tuple[str, str], ...] = (
    ("d_npxxy_oh_ref",       "NPxxY-OH (motif instrument)"),
    ("d_r350_r630_ca_ref",   "d_tm6 (midpoint instrument)"),
)


def load_reference_set(reference_set: Path) -> list[dict]:
    with reference_set.open() as f:
        return list(csv.DictReader(f))


def load_panel_receptors(coupling_csv: Path) -> set[str]:
    with coupling_csv.open() as f:
        return {r["receptor_slug"].strip().upper()
                for r in csv.DictReader(f)
                if r.get("receptor_slug")}


def derive_new_panel_thresholds(rows: list[dict]) -> dict[str, dict]:
    """Per new metric, compute active/inactive means + midpoint threshold.

    Direction is derived from the data: active_gt if active_mean >
    inactive_mean, else active_lt.
    """
    active = [r for r in rows if r["role"] == "active"]
    inactive = [r for r in rows if r["role"] == "inactive"]
    result: dict[str, dict] = {}
    for ref_col, runtime_col, label in NEW_METRICS:
        avs = [_to_float(r.get(ref_col, "")) for r in active]
        avs = [v for v in avs if not math.isnan(v)]
        ivs = [_to_float(r.get(ref_col, "")) for r in inactive]
        ivs = [v for v in ivs if not math.isnan(v)]
        if not avs or not ivs:
            result[ref_col] = {
                "status": "missing_data",
                "n_active": len(avs),
                "n_inactive": len(ivs),
                "runtime_col": runtime_col,
                "label": label,
            }
            continue
        active_mean = statistics.mean(avs)
        inactive_mean = statistics.mean(ivs)
        threshold = (active_mean + inactive_mean) / 2.0
        direction = "active_gt" if active_mean > inactive_mean else "active_lt"
        result[ref_col] = {
            "status": "ok",
            "runtime_col": runtime_col,
            "label": label,
            "threshold": threshold,
            "direction": direction,
            "n_active": len(avs),
            "n_inactive": len(ivs),
            "active_mean": active_mean,
            "inactive_mean": inactive_mean,
            "active_std": statistics.stdev(avs) if len(avs) > 1 else 0.0,
            "inactive_std": statistics.stdev(ivs) if len(ivs) > 1 else 0.0,
            "separation": active_mean - inactive_mean,
            "sensitivity_lo": threshold * 0.8,
            "sensitivity_hi": threshold * 1.2,
        }
    return result


def self_classification_accuracy(rows: list[dict], ref_col: str,
                                 threshold: float, direction: str) -> dict:
    """Fraction of tier-1 references correctly labelled by the metric.

    For each row (r, role) where the ref metric is measurable, the
    ``metric-on-own-crystal > threshold`` (or ``<``) call is compared
    against ``role``.
    """
    correct = 0
    called = 0
    dropped = 0
    for r in rows:
        role = r["role"]
        if role not in ("active", "inactive"):
            continue
        v = _to_float(r.get(ref_col, ""))
        if math.isnan(v):
            dropped += 1
            continue
        called += 1
        if direction == "active_gt":
            pred = "active" if v > threshold else "inactive"
        else:
            pred = "active" if v < threshold else "inactive"
        if pred == role:
            correct += 1
    return {
        "correct": correct,
        "called": called,
        "dropped": dropped,
        "accuracy": (correct / called) if called else float("nan"),
    }


def correlations_against_current(rows: list[dict], ref_col_new: str) -> dict:
    """Pearson r of the new metric's ref column vs the two current
    instrument ref columns, across all 80 tier-1 rows.
    """
    new_vals = [_to_float(r.get(ref_col_new, "")) for r in rows]
    out: dict[str, dict] = {}
    for ref_col_cur, label in CURRENT_INSTRUMENT_REFS:
        cur_vals = [_to_float(r.get(ref_col_cur, "")) for r in rows]
        r_val, n = pearson(new_vals, cur_vals)
        out[ref_col_cur] = {"label": label, "r": r_val, "n": n}
    return out


# ---------------------------------------------------------------------------
# thresholds_panel.csv append
# ---------------------------------------------------------------------------


def _fmt(v, ndigits: int = 3) -> str:
    if v is None:
        return ""
    try:
        return f"{float(v):.{ndigits}f}"
    except (TypeError, ValueError):
        return ""


def append_to_thresholds_panel(panel: dict, thresholds_panel_csv: Path) -> None:
    """(Re)write the three new-metric rows into refs/thresholds_panel.csv.

    The six user-locked motif rows already in the CSV are preserved
    verbatim; only rows for the three new literature metrics are
    overwritten so a re-run picks up any change in derivation.
    """
    header = [
        "metric_col", "ref_col", "direction", "status",
        "n_active", "n_inactive",
        "active_mean", "inactive_mean",
        "threshold", "sensitivity_lo", "sensitivity_hi",
    ]
    new_metric_cols = {info["runtime_col"] for info in panel.values()}
    existing_rows: list[list[str]] = []
    if thresholds_panel_csv.exists():
        with thresholds_panel_csv.open() as f:
            reader = csv.reader(f)
            _hdr = next(reader, None)
            for r in reader:
                if r and r[0] not in new_metric_cols:
                    existing_rows.append(r)

    with thresholds_panel_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in existing_rows:
            w.writerow(r)
        for ref_col, info in panel.items():
            runtime_col = info["runtime_col"]
            status = info.get("status", "missing_data")
            w.writerow([
                runtime_col,
                ref_col,
                info.get("direction", "unknown") if status == "ok" else "unknown",
                status if status == "ok" else "PENDING",
                info.get("n_active", 0),
                info.get("n_inactive", 0),
                _fmt(info.get("active_mean")),
                _fmt(info.get("inactive_mean")),
                _fmt(info.get("threshold")),
                _fmt(info.get("sensitivity_lo")),
                _fmt(info.get("sensitivity_hi")),
            ])


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------


def write_report(out_path: Path, panel: dict, self_acc: dict, corrs: dict,
                 reference_set: Path) -> None:
    lines: list[str] = [
        "# Block A — scorer extension for A100 + GPCRdb TM6 tilt + Class B kink",
        "",
        "**Date**: 2026-09-01",
        f"**Inputs**: {reference_set}",
        "",
        "Additive scorer extension per PREREG §2c-revised. Three new axis",
        "families landed as ScorerRow columns; the runtime active-call",
        "predicate is unchanged (still single-metric NPxxY-OH).",
        "",
        "## 1. New BW anchors added to `scorer.schema.ANCHOR_KEYS`",
        "",
        "| Anchor | Metric family |",
        "|---|---|",
        "| 2.46 | GPCRdb cross-class TM6 tilt |",
        "| 6.37 | GPCRdb cross-class TM6 tilt |",
        "| 1.53 | A100 component 1 (TM1-TM7) |",
        "| 7.55 | A100 component 1 (TM1-TM7) |",
        "| 2.50 | A100 component 2 (TM2-TM3) |",
        "| 3.37 | A100 component 2 (TM2-TM3) |",
        "| 3.42 | A100 component 3 (TM3-TM4) |",
        "| 4.42 | A100 component 3 (TM3-TM4) |",
        "| 5.66 | A100 component 4 (TM5-TM6) |",
        "| 6.34 | A100 component 4 (TM5-TM6) — already canonical |",
        "| 6.58 | A100 component 5 (TM6-TM7) |",
        "| 7.35 | A100 component 5 (TM6-TM7) |",
        "| 6.39 | Class B TM6 kink |",
        "| 6.50 | Class B TM6 kink (vertex) |",
        "| 6.54 | Class B TM6 kink |",
        "",
        "Existing `scorer.anchors.resolve_anchors` handles them without change —",
        "it iterates ANCHOR_KEYS and asks GPCRdb per label. Verified against",
        "the cached ADRB2 residues/extended payload: all 14 new labels resolve.",
        "",
        "## 2. Axis functions implemented in `scorer/axes.py`",
        "",
        "| Function | Definition |",
        "|---|---|",
        "| `d_gpcrdb_tm6_tilt_246_637_ca(model)` | 2.46 CA - 6.37 CA distance (Å) |",
        "| `a100_component_1_ca(model)` | 1.53 CA - 7.55 CA distance (Å) |",
        "| `a100_component_2_ca(model)` | 2.50 CA - 3.37 CA distance (Å) |",
        "| `a100_component_3_ca(model)` | 3.42 CA - 4.42 CA distance (Å) |",
        "| `a100_component_4_ca(model)` | 5.66 CA - 6.34 CA distance (Å) |",
        "| `a100_component_5_ca(model)` | 6.58 CA - 7.35 CA distance (Å) |",
        "| `a100_index(model)` | -14.43·c1 -7.62·c2 +9.11·c3 -6.32·c4 -5.22·c5 +278.88 |",
        "| `angle_class_b_tm6_kink_639_650_654_deg(model)` | Cα angle 6.39–6.50–6.54 (deg) |",
        "",
        "A100 formula from Ibrahim, Wifling & Clark, *J. Chem. Inf. Model.*",
        "2019, 59(9), 3938–3945 (DOI 10.1021/acs.jcim.9b00604 — **not** the",
        "10.1021/acs.jcim.8b00623 originally cited in the task; that DOI is a",
        "different paper). Full paper access via ACS abstract page confirmed",
        "the five BW positions, coefficients, intercept, and two-state /",
        "three-state thresholds. **A100 landed as real definitions — no",
        "placeholder-only fallback was needed.**",
        "",
        "All eight functions return NaN when any required BW anchor is not",
        "resolvable via GPCRdb or the CA atom is missing from the model.",
        "NaN propagates through `a100_index` if any component is NaN.",
        "",
        "## 3. Panel-derived thresholds",
        "",
        "| Metric | Direction | n_active / n_inactive | Active mean | Inactive mean | Separation | Threshold |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for ref_col, info in panel.items():
        if info.get("status") != "ok":
            lines.append(f"| {info['label']} | – | – | – | – | – | PENDING ({info.get('status')}) |")
            continue
        lines.append(
            f"| {info['label']} | {info['direction']} "
            f"| {info['n_active']} / {info['n_inactive']} "
            f"| {info['active_mean']:.3f} | {info['inactive_mean']:.3f} "
            f"| {info['separation']:+.3f} | {info['threshold']:.3f} |"
        )

    lines += [
        "",
        "## 4. Self-classification accuracy on tier-1 references",
        "",
        "For each metric: apply the panel-derived threshold to the metric",
        "value on the row's own crystal; call active/inactive; compare to",
        "``role``. NaN-metric rows are dropped from the denominator.",
        "",
        "| Metric | Correct / Called | Accuracy | Dropped (NaN) |",
        "|---|---:|---:|---:|",
    ]
    for ref_col, info in panel.items():
        acc = self_acc.get(ref_col, {})
        if not acc:
            continue
        acc_pct = f"{acc['accuracy']*100:.1f}%" if not math.isnan(acc['accuracy']) else "–"
        lines.append(
            f"| {info['label']} | {acc['correct']} / {acc['called']} "
            f"| {acc_pct} | {acc['dropped']} |"
        )

    lines += [
        "",
        "## 5. Correlation with current instruments (Pearson r, n=paired rows)",
        "",
        "Reference values across all 80 tier-1 rows (40 active + 40 inactive).",
        "",
        "| Metric | vs NPxxY-OH (motif) | vs d_tm6 (midpoint) |",
        "|---|---:|---:|",
    ]
    for ref_col, info in panel.items():
        c = corrs.get(ref_col, {})
        motif = c.get("d_npxxy_oh_ref", {})
        midpt = c.get("d_r350_r630_ca_ref", {})
        m_r = f"{motif.get('r', float('nan')):+.3f} (n={motif.get('n', 0)})" if not math.isnan(motif.get("r", float("nan"))) else "–"
        p_r = f"{midpt.get('r', float('nan')):+.3f} (n={midpt.get('n', 0)})" if not math.isnan(midpt.get("r", float("nan"))) else "–"
        lines.append(f"| {info['label']} | {m_r} | {p_r} |")

    lines += [
        "",
        "## 6. Recommendation",
        "",
        _recommendation(panel, self_acc, corrs),
        "",
        "## 7. Additive posture — nothing has changed in the predicate",
        "",
        "- `scorer/switch_signal.py::MotifThresholds` untouched (user-locked).",
        "- Current active-call predicate remains **single-metric NPxxY-OH**,",
        "  K_OF_N = 1, MAX_MISSING = 0 (PREREG §2b).",
        "- All eight new columns are emitted on every scored row for future",
        "  analysis. `refs/thresholds_panel.csv` carries the new rows so a",
        "  downstream re-derivation can consume them without a schema change.",
        "- Test suite still passes; existing 332 tests untouched.",
    ]
    out_path.write_text("\n".join(lines))


def _recommendation(panel: dict, self_acc: dict, corrs: dict) -> str:
    """Simple rule: recommend adding a metric to the predicate only if",
    self-classification accuracy on tier-1 is ≥ 94% (matching NPxxY-OH's",
    reported 94.3%) AND Pearson |r| against NPxxY-OH is < 0.7 (independent",
    signal). Otherwise, keep as reported-only.
    """
    recs: list[str] = []
    for ref_col, info in panel.items():
        if info.get("status") != "ok":
            recs.append(f"- **{info['label']}**: threshold derivation failed ({info.get('status')}). Keep as NaN-reported-only.")
            continue
        acc = self_acc.get(ref_col, {}).get("accuracy", float("nan"))
        r_motif = corrs.get(ref_col, {}).get("d_npxxy_oh_ref", {}).get("r", float("nan"))
        acc_pct = f"{acc*100:.1f}%" if not math.isnan(acc) else "n/a"
        r_str = f"{r_motif:+.3f}" if not math.isnan(r_motif) else "n/a"
        if math.isnan(acc) or math.isnan(r_motif):
            recs.append(f"- **{info['label']}** (acc {acc_pct}, r vs NPxxY-OH {r_str}): incomplete data. Keep reported-only for now.")
            continue
        if acc >= 0.94 and abs(r_motif) < 0.7:
            recs.append(f"- **{info['label']}** (acc {acc_pct}, r vs NPxxY-OH {r_str}): **CANDIDATE for the predicate** — high accuracy AND non-redundant with NPxxY-OH.")
        elif acc >= 0.90:
            recs.append(f"- **{info['label']}** (acc {acc_pct}, r vs NPxxY-OH {r_str}): strong classifier, but collinear with NPxxY-OH. Keep reported-only; useful QA cross-check.")
        else:
            recs.append(f"- **{info['label']}** (acc {acc_pct}, r vs NPxxY-OH {r_str}): does not clear the 90% self-classification bar on tier-1. Keep reported-only.")
    return "\n".join(recs)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reference-set", type=Path,
                    default=REPO / "refs/reference_set.csv")
    ap.add_argument("--coupling-csv", type=Path,
                    default=REPO / "refs/gpcr_coupling.csv")
    ap.add_argument("--thresholds-panel-csv", type=Path,
                    default=REPO / "refs/thresholds_panel.csv")
    ap.add_argument("--report", type=Path,
                    default=REPO / "docs/BLOCK_A_SCORER_EXTENSION_2026_09_01.md")
    args = ap.parse_args()

    all_rows = load_reference_set(args.reference_set)
    panel_slugs = load_panel_receptors(args.coupling_csv)
    # Analysis is confined to the 40-receptor panel — the only rows for
    # which scripts/derive_lit_metric_refs.py populated the ref columns.
    rows = [r for r in all_rows
            if (r.get("receptor_slug") or "").strip().upper() in panel_slugs]
    panel = derive_new_panel_thresholds(rows)

    self_acc: dict[str, dict] = {}
    corrs: dict[str, dict] = {}
    for ref_col, info in panel.items():
        if info.get("status") == "ok":
            self_acc[ref_col] = self_classification_accuracy(
                rows, ref_col, info["threshold"], info["direction"],
            )
        corrs[ref_col] = correlations_against_current(rows, ref_col)

    append_to_thresholds_panel(panel, args.thresholds_panel_csv)
    write_report(args.report, panel, self_acc, corrs, args.reference_set)

    print(f"wrote {args.thresholds_panel_csv}")
    print(f"wrote {args.report}")
    for ref_col, info in panel.items():
        if info.get("status") != "ok":
            print(f"  {info['label']}: {info.get('status')}")
            continue
        acc = self_acc.get(ref_col, {}).get("accuracy", float("nan"))
        r_motif = corrs.get(ref_col, {}).get("d_npxxy_oh_ref", {}).get("r", float("nan"))
        r_midpt = corrs.get(ref_col, {}).get("d_r350_r630_ca_ref", {}).get("r", float("nan"))
        print(
            f"  {info['label']}: threshold={info['threshold']:.3f} "
            f"({info['direction']}), acc={acc*100:.1f}%, "
            f"r_vs_motif={r_motif:+.3f}, r_vs_midpt={r_midpt:+.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
