#!/usr/bin/env python3
"""Block B Gate 3 NPxxY primary-pick analysis (§8-3 of Block C plan).

Emits the per-arm × per-backbone × per-receptor comparison table that
backs `docs/BLOCK_B_GATE3_NPXXY_PRIMARY_PICK_PROPOSAL_2026_09_03.md`.

Consumes (read-only):
  experiments/019_block_b_partner_selection/analysis/rows.csv
  refs/reference_set.csv
  refs/sealed_active_refs_2026_09_01.csv

Emits:
  experiments/019_block_b_partner_selection/analysis/npxxy_primary_comparison.csv

Six scoring variants of the Class A two-instrument active-call are
computed row-by-row and aggregated per (backbone, arm, receptor):

  A. tilt-only               tilt > 14.932                          — current headline_results.md primary
  B. panel                   tilt > 14.932 AND npxxy_oh < 9.082     — PREREG §14 held-out validated
  C. per-rec-40              tilt > 14.932 AND npxxy_oh < midpoint  — unscoreable receptors default-to-inactive; denom = 40
  D. per-rec-28              tilt > 14.932 AND npxxy_oh < midpoint  — unscoreable excluded from denom
  E. composite               per-receptor midpoint where a two-sided ref exists, panel-9.082 elsewhere; denom = 40
  F. composite (span-safe)   as E, but fall back to panel on receptors whose active/inactive ref span is narrow
                              (|span| < 2.0 Å) OR sign-inverted (active_ref > inactive_ref)

Tilt term is fixed at panel 14.932 Å in all variants (per
`experiments/019_block_b_partner_selection/analysis/npxxy_threshold_dual_scoring.md`
§"Note on tilt").

Per-receptor midpoint = (d_npxxy_oh_ref[active] + d_npxxy_oh_ref[inactive]) / 2
merged from BOTH refs/reference_set.csv AND refs/sealed_active_refs_2026_09_01.csv.

Class A rows only (receptor_class == "A"). Class B/F excluded by design of
the NPxxY-OH axis. Panel = 40 Class A receptors, 5 seeds × 10 samples per
(receptor × backbone × arm) cell = 50 rows/cell, 32,000 rows total.

Reproducibility:
  python3 scripts/analyse_npxxy_primary.py \
    --rows experiments/019_block_b_partner_selection/analysis/rows.csv \
    --ref-set refs/reference_set.csv \
    --sealed refs/sealed_active_refs_2026_09_01.csv \
    --out experiments/019_block_b_partner_selection/analysis/npxxy_primary_comparison.csv
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

# Locked panel thresholds (PREREG §14; refs/thresholds_panel.csv)
PANEL_NPXXY_THRESHOLD = 9.082
TILT_THRESHOLD = 14.932

# Span-safe fallback rule for variant F
SPAN_MIN = 2.0  # |active_ref - inactive_ref| below this triggers panel fallback

ARMS = ("cognate", "shuffled", "decoy", "apo")
BACKBONES = ("boltz", "chai", "of3", "protenix")


def _f(x):
    """Parse a float that may be blank/NaN. Returns None on non-numeric."""
    if x is None:
        return None
    if isinstance(x, float):
        return None if math.isnan(x) else x
    s = str(x).strip()
    if s == "" or s.lower() in ("nan", "na", "none"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _arm_of(path: str) -> str:
    for a in ARMS:
        if f"_{a}_" in path:
            return a
    return "?"


def _bb_of(path: str) -> str:
    for bb in BACKBONES:
        if f"_{bb}_" in path or f"/{bb}/" in path:
            return bb
    return "?"


def load_npxxy_refs(ref_set_path: Path, sealed_path: Path) -> dict[str, dict[str, float]]:
    """Load per-receptor NPxxY-OH active + inactive refs merged from both files.

    Returns {slug: {"active": f, "inactive": f}} — only entries with a
    parseable numeric are kept; missing sides are simply absent.
    """
    npxxy: dict[str, dict[str, float]] = defaultdict(dict)

    with ref_set_path.open() as f:
        r = csv.DictReader(f)
        for row in r:
            v = _f(row.get("d_npxxy_oh_ref"))
            if v is not None:
                npxxy[row["receptor_slug"]][row["role"]] = v

    # sealed file has "# ..." comment header block preceding the real header
    with sealed_path.open() as f:
        hdr = None
        for line in f:
            if line.startswith("#"):
                continue
            if hdr is None:
                hdr = [c.strip() for c in line.rstrip("\n").split(",")]
                continue
            parts = line.rstrip("\n").split(",")
            # sealed rows can carry quoted CSV commas; use csv.reader instead
            break

    with sealed_path.open() as f:
        # skip comment lines, then parse rest with csv.reader
        lines = [ln for ln in f if not ln.startswith("#")]
    reader = csv.DictReader(lines)
    for row in reader:
        v = _f(row.get("d_npxxy_oh_ref"))
        if v is not None:
            npxxy[row["receptor_slug"]][row["role"]] = v

    return dict(npxxy)


def compute_midpoints_and_spans(
    npxxy: dict[str, dict[str, float]],
) -> tuple[dict[str, float], dict[str, float], dict[str, bool]]:
    """From per-receptor NPxxY-OH refs, compute midpoint, span, span-inverted flag."""
    midpoint: dict[str, float] = {}
    span: dict[str, float] = {}
    inverted: dict[str, bool] = {}
    for slug, r in npxxy.items():
        if "active" in r and "inactive" in r:
            a, i = r["active"], r["inactive"]
            midpoint[slug] = (a + i) / 2.0
            span[slug] = abs(a - i)
            inverted[slug] = a > i  # active-state OH distance greater than inactive = axis inverted
    return midpoint, span, inverted


def span_safe_slug_set(
    midpoint: dict[str, float], span: dict[str, float], inverted: dict[str, bool]
) -> set[str]:
    """Slugs whose per-receptor midpoint should trigger panel fallback in variant F."""
    return {s for s in midpoint if inverted[s] or span[s] < SPAN_MIN}


def score_row(row: dict, midpoint: dict[str, float], safe_bad: set[str]) -> dict[str, int]:
    """Return per-variant call flags (0/1) plus scoreable-flags for a single row.

    Non-scoreable (missing tilt or npxxy) returns None for all — caller filters.
    """
    tilt = _f(row.get("d_gpcrdb_tm6_tilt_246_637_ca"))
    npx = _f(row.get("d_npxxy_y558_y753_oh"))
    if tilt is None or npx is None:
        return None
    slug = row["receptor_slug"]

    tilt_ok = tilt > TILT_THRESHOLD
    panel_ok = tilt_ok and (npx < PANEL_NPXXY_THRESHOLD)
    mp = midpoint.get(slug)
    perrec_ok = (mp is not None) and tilt_ok and (npx < mp)

    call = {
        "A_tilt_only": 1 if tilt_ok else 0,
        "B_panel": 1 if panel_ok else 0,
        "C_perrec_40": 1 if perrec_ok else 0,  # unscoreable → 0 (default-inactive)
        "D_perrec_28": 1 if perrec_ok else 0,  # will be filtered by denominator
        "E_composite": (1 if perrec_ok else 0) if mp is not None else (1 if panel_ok else 0),
        # F: for unsafe per-receptor spans, fall back to panel; for scoreable-safe use per-rec; otherwise panel
        "F_composite_span_safe": (
            (1 if panel_ok else 0) if (mp is None or slug in safe_bad)
            else (1 if perrec_ok else 0)
        ),
        # scoreability
        "has_midpoint": 1 if mp is not None else 0,
        "safe_midpoint": 1 if (mp is not None and slug not in safe_bad) else 0,
    }
    return call


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--rows", required=True, type=Path)
    ap.add_argument("--ref-set", required=True, type=Path)
    ap.add_argument("--sealed", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    npxxy = load_npxxy_refs(args.ref_set, args.sealed)
    midpoint, span, inverted = compute_midpoints_and_spans(npxxy)
    safe_bad = span_safe_slug_set(midpoint, span, inverted)

    print(f"[refs] receptors with any NPxxY-OH data:                     {len(npxxy)}", file=sys.stderr)
    print(f"[refs] receptors with two-sided midpoints (variants C/D/E):  {len(midpoint)}", file=sys.stderr)
    print(f"[refs] span-narrow / inverted receptors (fall back in F):    {sorted(safe_bad)}", file=sys.stderr)
    print(f"[refs] receptors treated per-receptor in F:                  {len(midpoint) - len(safe_bad)}", file=sys.stderr)

    # Per-(backbone, arm, receptor) numerator / denominator counters for each variant.
    # For variants A, B, C, E, F: denominator is every scoreable Class A row (uniform on 40 receptors).
    # For variant D: denominator counts only rows where the receptor has a per-receptor midpoint.
    variants = ("A_tilt_only", "B_panel", "C_perrec_40", "D_perrec_28",
                "E_composite", "F_composite_span_safe")

    # cell = (bb, arm, slug) -> {variant: [num, den]}
    cell: dict[tuple, dict[str, list[int]]] = defaultdict(
        lambda: {v: [0, 0] for v in variants}
    )
    # per-row disagreement counting: (bb, arm, slug) -> {"B_vs_C": (rows where they disagree), ...}
    disagree: dict[tuple, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    total_rows = 0
    skipped_non_A = 0
    skipped_missing = 0

    with args.rows.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            if row.get("receptor_class") != "A":
                skipped_non_A += 1
                continue
            slug = row["receptor_slug"]
            arm = _arm_of(row["input_path"])
            bb = _bb_of(row["input_path"])
            if arm == "?" or bb == "?":
                continue
            call = score_row(row, midpoint, safe_bad)
            if call is None:
                skipped_missing += 1
                continue

            key = (bb, arm, slug)
            has_mp = call["has_midpoint"] == 1

            for v in variants:
                if v == "D_perrec_28" and not has_mp:
                    # exclude row from D's denominator entirely
                    continue
                cell[key][v][1] += 1
                cell[key][v][0] += call[v]

            # disagreements
            if call["B_panel"] != call["C_perrec_40"]:
                disagree[key]["B_vs_C"] += 1
            if call["B_panel"] != call["E_composite"]:
                disagree[key]["B_vs_E"] += 1
            if call["B_panel"] != call["F_composite_span_safe"]:
                disagree[key]["B_vs_F"] += 1
            if call["C_perrec_40"] != call["E_composite"]:
                disagree[key]["C_vs_E"] += 1
            if call["E_composite"] != call["F_composite_span_safe"]:
                disagree[key]["E_vs_F"] += 1

    print(f"[rows] total rows in rows.csv:  {total_rows}", file=sys.stderr)
    print(f"[rows] skipped non-Class-A:     {skipped_non_A}", file=sys.stderr)
    print(f"[rows] skipped missing tilt/npx:{skipped_missing}", file=sys.stderr)

    # Emit CSV: one row per (backbone, arm, receptor) with per-variant num/den.
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "backbone", "arm", "receptor_slug",
        "receptor_has_midpoint", "receptor_safe_midpoint",
        "midpoint_A",
        "active_ref_npxxy_oh", "inactive_ref_npxxy_oh", "npxxy_ref_span",
        "npxxy_ref_span_inverted",
        "n_rows",
    ]
    for v in variants:
        fieldnames.append(f"{v}_numer")
        fieldnames.append(f"{v}_denom")
        fieldnames.append(f"{v}_frac")
    fieldnames += ["disagree_B_vs_C", "disagree_B_vs_E", "disagree_B_vs_F",
                   "disagree_C_vs_E", "disagree_E_vs_F"]

    with args.out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for (bb, arm, slug) in sorted(cell):
            v_counts = cell[(bb, arm, slug)]
            row_out = {
                "backbone": bb,
                "arm": arm,
                "receptor_slug": slug,
                "receptor_has_midpoint": 1 if slug in midpoint else 0,
                "receptor_safe_midpoint": 1 if (slug in midpoint and slug not in safe_bad) else 0,
                "midpoint_A": f"{midpoint[slug]:.4f}" if slug in midpoint else "",
                "active_ref_npxxy_oh": f"{npxxy[slug]['active']:.4f}" if slug in npxxy and "active" in npxxy[slug] else "",
                "inactive_ref_npxxy_oh": f"{npxxy[slug]['inactive']:.4f}" if slug in npxxy and "inactive" in npxxy[slug] else "",
                "npxxy_ref_span": f"{span[slug]:.4f}" if slug in span else "",
                "npxxy_ref_span_inverted": 1 if inverted.get(slug, False) else 0,
                "n_rows": v_counts["A_tilt_only"][1],
            }
            for v in variants:
                n, d = v_counts[v]
                row_out[f"{v}_numer"] = n
                row_out[f"{v}_denom"] = d
                row_out[f"{v}_frac"] = f"{n/d:.6f}" if d > 0 else ""
            d = disagree[(bb, arm, slug)]
            row_out["disagree_B_vs_C"] = d.get("B_vs_C", 0)
            row_out["disagree_B_vs_E"] = d.get("B_vs_E", 0)
            row_out["disagree_B_vs_F"] = d.get("B_vs_F", 0)
            row_out["disagree_C_vs_E"] = d.get("C_vs_E", 0)
            row_out["disagree_E_vs_F"] = d.get("E_vs_F", 0)
            w.writerow(row_out)

    # Print aggregate per-(backbone, arm) fractions for the amendment doc
    print("\n=== Aggregate active-fraction per (backbone × arm) per variant ===")
    for v in variants:
        print(f"\n{v}")
        print(f"  {'bb':<10} {'apo':<20} {'decoy':<20} {'shuffled':<20} {'cognate':<20}")
        for bb in BACKBONES:
            cells = []
            for arm in ("apo", "decoy", "shuffled", "cognate"):
                n = d = 0
                for (bb2, arm2, slug), vc in cell.items():
                    if bb2 != bb or arm2 != arm:
                        continue
                    a, b = vc[v]
                    n += a
                    d += b
                cells.append(f"{n/d*100:5.1f}% ({n}/{d})" if d > 0 else "n/a")
            print(f"  {bb:<10} " + " ".join(f"{c:<20}" for c in cells))

    return 0


if __name__ == "__main__":
    sys.exit(main())
