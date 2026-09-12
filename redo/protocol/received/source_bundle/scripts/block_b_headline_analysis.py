#!/usr/bin/env python3
"""Block B headline analysis — 2026-09-03.

Consumes:
  experiments/019_block_b_partner_selection/analysis/rows.csv
  experiments/019_block_b_partner_selection/analysis/rows.rmsd.csv

Emits:
  experiments/019_block_b_partner_selection/analysis/headline_results.md

Applies the pre-registered read-out table (BLOCK_B_DISPATCH_PLAN §"read-out"),
stratified per Decision 4 engagement branch (BLOCK_B_PRE_DISPATCH_DECISIONS).

Metrics used (all in existing rows.csv):
  * Receptor-side: d_gpcrdb_tm6_tilt_246_637_ca (Class A primary axis),
    d_npxxy_y558_y753_oh (Class A secondary), delta_to_active (RMSD).
  * Engagement (proxies — dedicated insertion-depth follow-up):
    d_ga_alpha5_r350_ca (α5 tip → receptor 3.50 CA),
    n_interface_contacts_ga_receptor (contact count).

Active call: d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å (PREREG panel threshold).
Engaged call: n_interface_contacts_ga_receptor >= 5 AND
              d_ga_alpha5_r350_ca <= 20 Å (soft-envelope proxy).

Per-cell aggregation: (receptor, arm, backbone) → 50 samples (5 seeds × 10).
Uses median of medians across samples/seeds where noted; active-fraction is
the fraction of samples that pass the receptor-side active predicate.
"""
from __future__ import annotations
import csv, sys, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANALYSIS = ROOT / "experiments/019_block_b_partner_selection/analysis"
ROWS_CSV = ANALYSIS / "rows.csv"
RMSD_CSV = ANALYSIS / "rows.rmsd.csv"
OUT_MD = ANALYSIS / "headline_results.md"

ARMS = ("cognate", "shuffled", "decoy", "apo")

# Thresholds (per PREREG)
TILT_ACTIVE_THRESHOLD = 14.932    # Å — Class A GPCRdb TM6 tilt primary
NPXXY_ACTIVE_THRESHOLD = 9.08     # Å — Class A NPxxY-OH secondary
# Engagement proxy envelope (task #167 follow-up should replace with insertion-depth)
ENGAGED_MIN_CONTACTS = 5
ENGAGED_MAX_ALPHA5_R350 = 20.0    # Å


def _f(v: str) -> float:
    try:
        return float(v)
    except Exception:
        return float("nan")


def _arm_of(path: str) -> str:
    for a in ARMS:
        if f"_{a}_" in path:
            return a
    return "?"


def _bb_of(path: str) -> str:
    for bb in ("boltz", "chai", "of3", "protenix"):
        if f"_{bb}_" in path or f"/{bb}/" in path:
            return bb
    return "?"


def load_rows() -> tuple[list[dict], list[dict]]:
    with ROWS_CSV.open() as f:
        rows = list(csv.DictReader(f))
    with RMSD_CSV.open() as f:
        rmsd = list(csv.DictReader(f))
    return rows, rmsd


def cell_key(r: dict) -> tuple[str, str, str]:
    return (r["receptor_slug"] or "?",
            _arm_of(r["input_path"]),
            _bb_of(r["input_path"]))


def main() -> int:
    rows, rmsd = load_rows()
    print(f"Loaded {len(rows)} rescore rows, {len(rmsd)} RMSD rows.", file=sys.stderr)

    rmsd_by_path = {r["input_path"]: r for r in rmsd}

    # Filter passed=True — receptor-side rescore succeeded
    passed = [r for r in rows if r.get("passed") == "True"]
    print(f"passed=True: {len(passed)}", file=sys.stderr)

    # Per-sample: is it active? is it engaged?
    for r in passed:
        tilt = _f(r.get("d_gpcrdb_tm6_tilt_246_637_ca", ""))
        r["_active"] = 1 if tilt == tilt and tilt > TILT_ACTIVE_THRESHOLD else 0
        arm = _arm_of(r["input_path"])
        if arm == "apo":
            r["_engaged"] = None  # no partner — engagement N/A
        else:
            n_contacts = _f(r.get("n_interface_contacts_ga_receptor", ""))
            d_a5 = _f(r.get("d_ga_alpha5_r350_ca", ""))
            eng = (n_contacts >= ENGAGED_MIN_CONTACTS and
                   d_a5 == d_a5 and d_a5 <= ENGAGED_MAX_ALPHA5_R350)
            r["_engaged"] = 1 if eng else 0
        # RMSD
        rm = rmsd_by_path.get(r["input_path"])
        if rm:
            r["_rmsd_active"] = _f(rm.get("rmsd_to_active_ref", ""))
        else:
            r["_rmsd_active"] = float("nan")

    # Aggregate per (arm, backbone) — across all receptors + samples
    stats_by_arm_bb: dict[tuple[str, str], dict] = defaultdict(lambda: {
        "n": 0, "n_active": 0, "n_engaged": 0,
        "n_engaged_and_inactive": 0, "n_engaged_and_active": 0,
        "n_not_engaged_and_inactive": 0, "n_not_engaged_and_active": 0,
        "rmsd_active": [], "tilt": [], "contacts": [], "d_a5": [],
    })
    for r in passed:
        arm = _arm_of(r["input_path"])
        bb = _bb_of(r["input_path"])
        s = stats_by_arm_bb[(arm, bb)]
        s["n"] += 1
        s["n_active"] += r["_active"]
        tilt = _f(r.get("d_gpcrdb_tm6_tilt_246_637_ca", ""))
        if tilt == tilt:
            s["tilt"].append(tilt)
        if r["_rmsd_active"] == r["_rmsd_active"]:
            s["rmsd_active"].append(r["_rmsd_active"])
        if arm != "apo":
            n_c = _f(r.get("n_interface_contacts_ga_receptor", ""))
            d_a5 = _f(r.get("d_ga_alpha5_r350_ca", ""))
            if n_c == n_c: s["contacts"].append(n_c)
            if d_a5 == d_a5: s["d_a5"].append(d_a5)
            eng = r["_engaged"]
            act = r["_active"]
            s["n_engaged"] += (eng or 0)
            if eng and act: s["n_engaged_and_active"] += 1
            elif eng and not act: s["n_engaged_and_inactive"] += 1
            elif (not eng) and act: s["n_not_engaged_and_active"] += 1
            else: s["n_not_engaged_and_inactive"] += 1

    def med(xs: list[float]) -> float:
        return statistics.median(xs) if xs else float("nan")

    # Write the markdown report
    lines: list[str] = []
    ap = lines.append
    ap("# Block B — headline results (2026-09-03)")
    ap("")
    ap("Panel: 40 Class A receptors × 4 backbones × 4 arms × 5 seeds × 10 samples "
       f"= 32,000 predictions. Passed-rescore population: **{len(passed)} / {len(rows)}** "
       f"({100*len(passed)/len(rows):.2f}%).")
    ap("")
    ap("**Threshold definitions:**")
    ap(f"- Active call (Class A primary): `d_gpcrdb_tm6_tilt_246_637_ca > {TILT_ACTIVE_THRESHOLD} Å`.")
    ap(f"- Engaged call (engagement proxy — see follow-up task): "
       f"`n_interface_contacts_ga_receptor >= {ENGAGED_MIN_CONTACTS}` **AND** "
       f"`d_ga_alpha5_r350_ca <= {ENGAGED_MAX_ALPHA5_R350} Å`.")
    ap("")
    ap("---")
    ap("")
    ap("## §1. Active-state fraction, per (arm × backbone)")
    ap("")
    ap("| backbone | apo | cognate | shuffled | decoy |")
    ap("|---|---:|---:|---:|---:|")
    for bb in ("boltz", "chai", "of3", "protenix"):
        row = [f"| {bb} "]
        for arm in ("apo", "cognate", "shuffled", "decoy"):
            s = stats_by_arm_bb.get((arm, bb))
            if s and s["n"]:
                pct = 100 * s["n_active"] / s["n"]
                row.append(f"| {pct:5.1f}% ({s['n_active']}/{s['n']}) ")
            else:
                row.append("| n/a ")
        row.append("|")
        ap("".join(row))
    ap("")

    ap("## §2. Median RMSD-to-active (Å), per (arm × backbone)")
    ap("")
    ap("Lower is closer to the active reference. RMSD is the cross-class primary metric.")
    ap("")
    ap("| backbone | apo | cognate | shuffled | decoy |")
    ap("|---|---:|---:|---:|---:|")
    for bb in ("boltz", "chai", "of3", "protenix"):
        row = [f"| {bb} "]
        for arm in ("apo", "cognate", "shuffled", "decoy"):
            s = stats_by_arm_bb.get((arm, bb))
            if s and s["rmsd_active"]:
                row.append(f"| {med(s['rmsd_active']):5.2f} ")
            else:
                row.append("| n/a ")
        row.append("|")
        ap("".join(row))
    ap("")

    ap("## §3. Engagement metrics (proxies), per (arm × backbone) — non-apo only")
    ap("")
    ap("| backbone | arm | n | median n_contacts | median d_α5→3.50 | fraction engaged |")
    ap("|---|---|---:|---:|---:|---:|")
    for bb in ("boltz", "chai", "of3", "protenix"):
        for arm in ("cognate", "shuffled", "decoy"):
            s = stats_by_arm_bb.get((arm, bb))
            if s and s["contacts"]:
                eng_frac = 100 * s["n_engaged"] / s["n"] if s["n"] else 0
                ap(f"| {bb} | {arm} | {s['n']} | {med(s['contacts']):.0f} | "
                   f"{med(s['d_a5']):5.2f} Å | {eng_frac:5.1f}% |")
    ap("")

    ap("## §4. The pre-registered 2×2 — decoy arm")
    ap("")
    ap("Per Decision 4 (BLOCK_B_PRE_DISPATCH_DECISIONS §"
       "'Engagement-side metrics'), the decoy null splits by engagement state.")
    ap("Only the **engaged-and-inactive** cell tests the α5-CT chemistry claim.")
    ap("")
    for bb in ("boltz", "chai", "of3", "protenix"):
        s = stats_by_arm_bb.get(("decoy", bb))
        if not s or not s["n"]:
            continue
        ap(f"### {bb} decoy")
        ap("")
        ap("| receptor-side | engaged | not engaged | total |")
        ap("|---|---:|---:|---:|")
        ap(f"| active     | {s['n_engaged_and_active']} | {s['n_not_engaged_and_active']} | "
           f"{s['n_engaged_and_active']+s['n_not_engaged_and_active']} |")
        ap(f"| inactive   | **{s['n_engaged_and_inactive']}** ← α5-CT chemistry claim "
           f"| {s['n_not_engaged_and_inactive']} (physical failure) | "
           f"{s['n_engaged_and_inactive']+s['n_not_engaged_and_inactive']} |")
        ap(f"| total | {s['n_engaged']} | {s['n']-s['n_engaged']} | {s['n']} |")
        ap("")

    ap("## §5. The four-cell decision table applied")
    ap("")
    ap("Using medians across all receptors and seeds for each backbone-arm cell:")
    ap("")
    ap("**Decision rule (pre-registered, PREREG):**")
    ap("- If `decoy ≈ cognate` and `shuffled ≈ cognate`: occupancy alone activates — chemistry claim DIES.")
    ap("- If `decoy ≈ apo` and `shuffled ≈ cognate`: fold matters, sequence doesn't — conserved-anchor reading.")
    ap("- If `decoy ≈ apo` and `shuffled < cognate`: **sequence specificity real — steering paper UNBLOCKED**.")
    ap("- If `apo < decoy < shuffled`: graded, mass-dependent — partner-mass ladder next.")
    ap("")
    ap("Reading per backbone (active-fraction, %):")
    ap("")
    ap("| backbone | apo | decoy | shuffled | cognate | pattern |")
    ap("|---|---:|---:|---:|---:|---|")
    for bb in ("boltz", "chai", "of3", "protenix"):
        row_vals = {}
        for arm in ("apo", "decoy", "shuffled", "cognate"):
            s = stats_by_arm_bb.get((arm, bb))
            row_vals[arm] = (100 * s["n_active"] / s["n"]) if s and s["n"] else float("nan")
        apo, dec, shu, cog = (row_vals[k] for k in ("apo", "decoy", "shuffled", "cognate"))
        # Classify
        def near(a, b, tol=10):
            return abs(a - b) <= tol
        if near(dec, cog) and near(shu, cog):
            pat = "occupancy alone activates"
        elif near(dec, apo) and near(shu, cog):
            pat = "fold matters, sequence doesn't"
        elif near(dec, apo) and shu < cog - 10:
            pat = "**sequence specificity real — steering paper unblocked**"
        elif apo < dec < shu:
            pat = "graded, mass-dependent"
        else:
            pat = "mixed / no clean fit"
        ap(f"| {bb} | {apo:5.1f}% | {dec:5.1f}% | {shu:5.1f}% | {cog:5.1f}% | {pat} |")
    ap("")

    ap("---")
    ap("")
    ap("## Caveats")
    ap("")
    ap("1. **Engagement metric is a proxy.** The pre-registered primary was insertion depth "
       "(TM-axis-projected). This report uses `d_ga_alpha5_r350_ca` (α5-CT tip → receptor 3.50 CA) "
       "as a stand-in — well-correlated with insertion depth but not identical. Follow-up: "
       "dedicated insertion-depth + DSSP helicity + SASA (task #167 continuation).")
    ap("2. **Active call uses Class A primary axis only.** Class B/F not in Block B Wide dispatch.")
    ap("3. **Active threshold is the panel-wide GPCRdb TM6 tilt (14.932 Å).** Per-receptor "
       "thresholds would refine but are not the primary read-out (PREREG §16 lock).")
    ap("4. **B1B1U5 + OPSD** were mis-scored in the first pass (species-label bug, 1200 rows). "
       "The rescore consumed here is the corrected pass. See BLOCK_B_POST_WIDE_RUNBOOK for the fix.")
    ap("5. **Follow-up:** engagement-metric analysis (task #167) — proper TM-axis projection + DSSP.")
    ap("")

    OUT_MD.write_text("\n".join(lines))
    print(f"Wrote {OUT_MD}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
