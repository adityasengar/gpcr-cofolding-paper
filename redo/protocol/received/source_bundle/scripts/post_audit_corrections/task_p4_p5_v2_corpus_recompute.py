#!/usr/bin/env python3
"""Task P4/P5 v2-corpus recompute — refresh Tier 3 §4.5 numbers against
the POST-species-fix corpus.

Context (Block C Tier 3, 2026-09-06)
------------------------------------
The Tier 3 headline `tier3_headline_2026_09_05.md` §4.5 currently quotes
P4 (per-receptor `antag_cog < agonist_cog` on >= 30/40) and P5 null
(|decoy_apo - agonist_apo| < 0.15) CI numbers computed against the
PRE-species-fix corpus `rows.tier3.csv`
(SHA-256 c0939875a3c2747523eb7c097f04fb86583728b3c5474c457724cf59d0a1463b).

The species-fix landed in `scripts/build_block_c_tier3_manifest.py`
(commit f65521a) and the post-fix corpus is `rows.tier3.v2.csv`
(SHA-256 5ccf58acc8a6b0151250007c6b40d1f728ad4b42c2eeab22bd6509b5809e2103).

Because the §4.5 framing (both fire-gates saturate on the binary
two-instrument predicate and are withdrawn from the paper's primary
claim per §6) applies regardless of corpus, only the specific CI
numbers need refreshing. This script produces that refresh.

Method (mirrors `scripts/analyse_block_c_tier3_headline.py`
`evaluate_predictions` P4/P5 blocks so the numbers are drop-in
comparable)
------------------------------------------------------------------
P4:
  * Per receptor x backbone, compute cell fraction-active for
    (full_agonist, cognate) and (neutral_antagonist, cognate).
  * Count receptors where `ag_frac > an_frac` (equivalent to
    `antag_cog < agonist_cog`); ties count as fail per the source
    script (line 248: `1 if ag_frac > an_frac else 0`).
  * Cluster-bootstrap on receptor id (10 000 replicates, seed 20260905
    matching the source script) of the pass-fraction, scaled back to
    n = 40 for direct comparison with the >=30/40 threshold.
  * Report point estimate `n_correct` and 2.5 / 97.5 percentile CI.

P5:
  * Per receptor x backbone, compute
    |fraction_active(decoy_lig, apo) - fraction_active(full_agonist, apo)|.
  * Cluster-bootstrap on receptor id (10 000 replicates, seed 20260905)
    of the panel mean. Report point + 2.5 / 97.5 percentile CI.

NA handling
-----------
`rows.tier3.v2.csv` has no `activity_class` column. Per PREREG
`s 2c-revised` and the source script `is_active` predicate, NaN on
either axis (`d_npxxy_y558_y753_oh`, `d_gpcrdb_tm6_tilt_246_637_ca`)
is treated as False, and a cell is excluded from the P4/P5 denominator
only when neither axis produces a numeric fraction (`ag_frac` or
`an_frac` NaN, or the (receptor, ligand_role, arm, backbone) cell
missing entirely from the corpus). Exclusion counts are reported.

Path parsing follows the source script regex (bug hunted 2026-09-05:
the backbone slug MUST include digits so `of3` doesn't silently drop).

Provenance
----------
Pins reconstruction script git SHA + SHA-256 of every input file.
Local commit only; DOES NOT edit `tier3_headline_2026_09_05.md`.

Usage
-----
    python3 scripts/post_audit_corrections/task_p4_p5_v2_corpus_recompute.py

Emits: experiments/021_block_c_tier3_pharmacology/analysis/verification/
         p4_p5_v2_corpus_recompute.json
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import REPO, sha256, git_sha, now_utc  # noqa: E402

# ---- constants (mirrored from scripts/analyse_block_c_tier3_headline.py) ----
NPXXY_OH_LT = 9.082
TM6_TILT_GT = 14.932

RECEPTORS_40 = (
    "5HT1B", "5HT2C", "5HT5A", "AA1R", "AA2AR", "ACM1", "ACM2", "ACM4",
    "ADA2A", "ADRB1", "ADRB2", "AGTR1", "APJ", "B1B1U5", "CCKAR", "CCR5",
    "CNR1", "CNR2", "CXCR2", "CXCR4", "DRD2", "DRD3", "EDNRA", "EDNRB",
    "FSHR", "GHSR", "GRPR", "HRH1", "HRH3", "LPAR1", "LSHR", "LT4R1",
    "MCHR1", "NPY1R", "NPY2R", "OPRD", "OPRK", "OPRX", "OPSD", "OX2R",
)
BACKBONES = ("boltz", "chai", "of3", "protenix")

P4_THRESHOLD = 30
P5_THRESHOLD = 0.15
BOOTSTRAP_N = 10_000
RNG_SEED = 20260905  # matches analyse_block_c_tier3_headline.py

# Values pre-species-fix (source: tier3_provenance.json emitted against
# rows.tier3.csv SHA c0939875a...; reproduced verbatim in
# tier3_headline_2026_09_05.md `s 4.5).
PRE_FIX = {
    "corpus_sha256": (
        "c0939875a3c2747523eb7c097f04fb86583728b3c5474c457724cf59d0a1463b"
    ),
    "P4": {
        "boltz":    {"n_correct": 12, "n_tested": 28, "n_receptors": 40,
                     "ci_95": [10.0, 24.285714285714285],
                     "fire_gate": "FIRES_BELOW"},
        "chai":     {"n_correct":  3, "n_tested": 28, "n_receptors": 40,
                     "ci_95": [0.0, 10.0],
                     "fire_gate": "FIRES_BELOW"},
        "of3":      {"n_correct": 12, "n_tested": 28, "n_receptors": 40,
                     "ci_95": [10.0, 24.285714285714285],
                     "fire_gate": "FIRES_BELOW"},
        "protenix": {"n_correct":  3, "n_tested": 28, "n_receptors": 40,
                     "ci_95": [0.0, 10.0],
                     "fire_gate": "FIRES_BELOW"},
    },
    "P5": {
        "boltz":    {"panel_mean_abs": 0.0520,
                     "ci_95": [0.020, 0.09028571428571427],
                     "n_receptors_tested": 35,
                     "fire_gate": "FIRES_BELOW"},
        "chai":     {"panel_mean_abs": 0.0674,
                     "ci_95": [0.006857142857142859, 0.14400000000000002],
                     "n_receptors_tested": 35,
                     "fire_gate": "FIRES_BELOW"},
        "of3":      {"panel_mean_abs": 0.0817,
                     "ci_95": [0.04571428571428573, 0.12342857142857146],
                     "n_receptors_tested": 35,
                     "fire_gate": "FIRES_BELOW"},
        "protenix": {"panel_mean_abs": 0.0354,
                     "ci_95": [0.0, 0.0982857142857143],
                     "n_receptors_tested": 35,
                     "fire_gate": "FIRES_BELOW"},
    },
}


_PATH_RE = re.compile(
    r"/([a-z0-9_]+)/([a-z_]+)/([a-z]+)/([a-z0-9]+)/seed_(\d+)/"
)


def _parse_path(pp: str):
    m = _PATH_RE.search(pp or "")
    if not m:
        return None
    return {
        "receptor": m.group(1).upper(),
        "ligand_role": m.group(2),
        "arm": m.group(3),
        "backbone": m.group(4),
        "seed": int(m.group(5)),
    }


def _is_active(row):
    oh = row.get("d_npxxy_y558_y753_oh", "")
    tilt = row.get("d_gpcrdb_tm6_tilt_246_637_ca", "")
    if oh in ("", "nan", "NaN") or tilt in ("", "nan", "NaN"):
        return False
    try:
        oh_f = float(oh); tilt_f = float(tilt)
    except (ValueError, TypeError):
        return False
    if math.isnan(oh_f) or math.isnan(tilt_f):
        return False
    return (oh_f < NPXXY_OH_LT) and (tilt_f > TM6_TILT_GT)


def _cell_frac_active(row_list):
    n = 0; a = 0
    for r in row_list:
        n += 1
        if r["_is_active"] is True:
            a += 1
    return (a / n) if n else float("nan")


def _load(path):
    """Load rows.tier3.v2.csv keyed by (receptor, ligand_role, arm,
    backbone). Rows whose path doesn't match the source regex are
    dropped (same as analyse_block_c_tier3_headline.py)."""
    cells = defaultdict(list)
    n_total = 0
    n_dropped_path = 0
    n_dropped_nan_axes = 0
    with open(path) as f:
        for row in csv.DictReader(f):
            n_total += 1
            pp = row.get("prediction_path") or row.get("input_path") or ""
            parsed = _parse_path(pp)
            if parsed is None:
                n_dropped_path += 1
                continue
            row["_is_active"] = _is_active(row)
            if row.get("d_npxxy_y558_y753_oh", "") in ("", "nan", "NaN") \
                    or row.get("d_gpcrdb_tm6_tilt_246_637_ca", "") \
                    in ("", "nan", "NaN"):
                n_dropped_nan_axes += 1
            key = (parsed["receptor"], parsed["ligand_role"],
                   parsed["arm"], parsed["backbone"])
            cells[key].append(row)
    return cells, {
        "n_total_rows_in_csv": n_total,
        "n_rows_dropped_path_parse_fail": n_dropped_path,
        "n_rows_with_nan_predicate_axis_kept_as_False":
            n_dropped_nan_axes,
        "note_activity_class_column": (
            "rows.tier3.v2.csv has no `activity_class` column; "
            "NA handling follows source script — NaN on either "
            "predicate axis → is_active=False; a cell is excluded "
            "from P4/P5 only when the (receptor, arm) cell is "
            "missing entirely or produces NaN fraction."
        ),
    }


def _p4_pass_count_bootstrap(cells, backbone, receptors,
                              n_boot=BOOTSTRAP_N, seed=RNG_SEED):
    """Cluster bootstrap on receptor id of the P4 pass-count,
    scaled to len(receptors) (= 40). Mirrors the source script's
    `bootstrap_p4_pass_count`."""
    per_recep = {}
    per_recep_report = {}
    for rec in receptors:
        ag = cells.get((rec, "full_agonist", "cognate", backbone), [])
        an = cells.get((rec, "neutral_antagonist", "cognate", backbone), [])
        if not ag or not an:
            per_recep_report[rec] = {"reason": "cell_missing"}
            continue
        ag_f = _cell_frac_active(ag)
        an_f = _cell_frac_active(an)
        if math.isnan(ag_f) or math.isnan(an_f):
            per_recep_report[rec] = {"reason": "nan_cell"}
            continue
        per_recep[rec] = 1 if ag_f > an_f else 0
        per_recep_report[rec] = {
            "agonist_cognate": round(ag_f, 4),
            "antagonist_cognate": round(an_f, 4),
            "agonist_gt_antag": (ag_f > an_f),
            "tie_exact": (ag_f == an_f),
        }
    if not per_recep:
        return 0, float("nan"), float("nan"), per_recep_report, 0
    values = list(per_recep.values())
    k = len(values)
    point = sum(values)
    rng = random.Random(seed)
    boots = []
    for _ in range(n_boot):
        s = [values[rng.randint(0, k - 1)] for _ in range(k)]
        boots.append(sum(s) / k * len(receptors))
    boots.sort()
    lo = boots[max(0, int(0.025 * n_boot) - 1)]
    hi = boots[min(n_boot - 1, int(0.975 * n_boot) - 1)]
    return point, lo, hi, per_recep_report, k


def _p5_panel_mean_bootstrap(cells, backbone, receptors,
                              n_boot=BOOTSTRAP_N, seed=RNG_SEED):
    """Panel mean of |frac_active(decoy_lig, apo) − frac_active(
    full_agonist, apo)| with cluster bootstrap on receptor id.
    Mirrors the source script's `bootstrap_receptor_mean` fed the
    P5 per-receptor absolute gaps."""
    per_recep = {}
    per_recep_report = {}
    for rec in receptors:
        dk = (rec, "decoy_lig", "apo", backbone)
        ak = (rec, "full_agonist", "apo", backbone)
        if dk not in cells or ak not in cells:
            per_recep_report[rec] = {"reason": "cell_missing"}
            continue
        df = _cell_frac_active(cells[dk])
        af = _cell_frac_active(cells[ak])
        if math.isnan(df) or math.isnan(af):
            per_recep_report[rec] = {"reason": "nan_cell"}
            continue
        per_recep[rec] = abs(df - af)
        per_recep_report[rec] = {
            "decoy_apo_frac": round(df, 4),
            "agonist_apo_frac": round(af, 4),
            "abs_delta": round(abs(df - af), 4),
        }
    values = list(per_recep.values())
    if not values:
        return float("nan"), float("nan"), float("nan"), per_recep_report, 0
    point = sum(values) / len(values)
    rng = random.Random(seed)
    k = len(values)
    boots = []
    for _ in range(n_boot):
        s = [values[rng.randint(0, k - 1)] for _ in range(k)]
        boots.append(sum(s) / k)
    boots.sort()
    lo = boots[max(0, int(0.025 * n_boot) - 1)]
    hi = boots[min(n_boot - 1, int(0.975 * n_boot) - 1)]
    return point, lo, hi, per_recep_report, k


def _fire_gate_above(point, lo, hi, thr):
    if any(math.isnan(x) for x in (point, lo, hi)):
        return "STRADDLES_CI"
    if lo > thr:
        return "FIRES_ABOVE"
    if hi < thr:
        return "FIRES_BELOW"
    return "STRADDLES_CI"


def _fire_gate_below(point, lo, hi, thr):
    if any(math.isnan(x) for x in (point, lo, hi)):
        return "STRADDLES_CI"
    if hi < thr:
        return "FIRES_BELOW"
    if lo > thr:
        return "FIRES_ABOVE"
    return "STRADDLES_CI"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rows.tier3.v2.csv")
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/p4_p5_v2_corpus_recompute.json")
    args = ap.parse_args()

    cells, load_stats = _load(args.rows)

    p4_new = {}
    p5_new = {}
    for bb in BACKBONES:
        pt, lo, hi, per_r, k = _p4_pass_count_bootstrap(
            cells, bb, RECEPTORS_40)
        p4_new[bb] = {
            "n_correct": pt,
            "n_tested": k,
            "n_receptors": len(RECEPTORS_40),
            "threshold": P4_THRESHOLD,
            "pass_count_ci_95": [lo, hi],
            "fire_gate": _fire_gate_above(pt, lo, hi, P4_THRESHOLD),
            "clears_threshold": (pt >= P4_THRESHOLD),
            "per_receptor_ordering": per_r,
        }
        pt5, lo5, hi5, per_r5, k5 = _p5_panel_mean_bootstrap(
            cells, bb, RECEPTORS_40)
        p5_new[bb] = {
            "panel_mean_abs": pt5,
            "n_receptors_tested": k5,
            "n_receptors_total": len(RECEPTORS_40),
            "n_excluded": len(RECEPTORS_40) - k5,
            "panel_ci_95": [lo5, hi5],
            "threshold": P5_THRESHOLD,
            "fire_gate": _fire_gate_below(pt5, lo5, hi5, P5_THRESHOLD),
            "null_holds": (pt5 < P5_THRESHOLD),
            "per_receptor_abs_gap": per_r5,
        }

    # Side-by-side pre-fix vs post-fix.
    side_by_side = {"P4": {}, "P5": {}}
    for bb in BACKBONES:
        pre = PRE_FIX["P4"][bb]
        post = p4_new[bb]
        side_by_side["P4"][bb] = {
            "pre_species_fix": {
                "n_correct_of_tested": f"{pre['n_correct']}/"
                f"{pre['n_tested']}",
                "ci_95_scaled_to_n40": pre["ci_95"],
                "fire_gate": pre["fire_gate"],
            },
            "post_species_fix_v2": {
                "n_correct_of_tested": f"{post['n_correct']}/"
                f"{post['n_tested']}",
                "ci_95_scaled_to_n40": post["pass_count_ci_95"],
                "fire_gate": post["fire_gate"],
            },
            "delta_n_correct": post["n_correct"] - pre["n_correct"],
            "gate_unchanged": post["fire_gate"] == pre["fire_gate"],
        }
        pre5 = PRE_FIX["P5"][bb]
        post5 = p5_new[bb]
        side_by_side["P5"][bb] = {
            "pre_species_fix": {
                "panel_mean_abs": pre5["panel_mean_abs"],
                "ci_95": pre5["ci_95"],
                "n_receptors_tested": pre5["n_receptors_tested"],
                "fire_gate": pre5["fire_gate"],
            },
            "post_species_fix_v2": {
                "panel_mean_abs": post5["panel_mean_abs"],
                "ci_95": post5["panel_ci_95"],
                "n_receptors_tested": post5["n_receptors_tested"],
                "fire_gate": post5["fire_gate"],
            },
            "delta_panel_mean": (post5["panel_mean_abs"]
                                  - pre5["panel_mean_abs"]),
            "gate_unchanged": post5["fire_gate"] == pre5["fire_gate"],
        }

    out = {
        "task": "P4_P5_v2_corpus_recompute",
        "purpose": (
            "Refresh Tier 3 headline `s 4.5 P4 (n_correct + CI) and P5 "
            "(panel mean |Delta| + CI) numbers against the POST-species-fix "
            "corpus rows.tier3.v2.csv. Framing (both saturate on the binary "
            "predicate; withdrawn from primary claim per `s 6) unchanged."
        ),
        "reconstruction": {
            "reconstruction_script": str(Path(__file__).resolve()),
            "reconstruction_script_git_sha": git_sha(),
            "generated_at_utc": now_utc(),
            "bootstrap": {
                "n_replicates": BOOTSTRAP_N,
                "seed": RNG_SEED,
                "unit": "receptor id",
                "note": ("Matches seed used by "
                         "scripts/analyse_block_c_tier3_headline.py so the "
                         "pre/post numbers use identical resampling."),
            },
            "inputs": {
                "rows_tier3_v2_csv": {
                    "path": str(args.rows),
                    "sha256": sha256(args.rows),
                },
            },
            "pre_fix_corpus_reference": {
                "path": "experiments/021_block_c_tier3_pharmacology"
                "/analysis/rows.tier3.csv",
                "sha256": PRE_FIX["corpus_sha256"],
                "source_provenance_json": (
                    "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/tier3_provenance.json"
                ),
            },
        },
        "predicate": {
            "two_instrument_active": (
                f"(d_npxxy_y558_y753_oh < {NPXXY_OH_LT}) AND "
                f"(d_gpcrdb_tm6_tilt_246_637_ca > {TM6_TILT_GT})"
            ),
            "P4_definition": (
                "For each receptor with a valid full_agonist+cognate cell "
                "AND a valid neutral_antagonist+cognate cell, count 1 if "
                "fraction_active(full_agonist,cognate) > "
                "fraction_active(neutral_antagonist,cognate) else 0. "
                "Ties count as fail (matches source script line 248). "
                "Bootstrap the pass-fraction over receptors with "
                "replacement, then scale to n_receptors=40."
            ),
            "P5_definition": (
                "Per receptor with both decoy_lig+apo and full_agonist+apo "
                "cells valid, compute |fraction_active(decoy_lig,apo) - "
                "fraction_active(full_agonist,apo)|. Bootstrap the panel "
                "mean over receptors with replacement."
            ),
            "P4_threshold": P4_THRESHOLD,
            "P5_threshold": P5_THRESHOLD,
        },
        "corpus_load_stats": load_stats,
        "side_by_side": side_by_side,
        "post_species_fix_v2": {
            "P4": p4_new,
            "P5": p5_new,
        },
        "pre_species_fix_snapshot": PRE_FIX,
        "framing": {
            "unchanged_from_headline_section_6": (
                "Both P4 and P5 are binary two-instrument-predicate "
                "summaries and both saturate on the cognate arm (agonist "
                "and decoy both hit ~1.0 fraction-active on most "
                "receptors — see verification/task2_p4_ties_saturation.json "
                "for the tie/saturation census). The prior 'presence not "
                "identity' unification is withdrawn (headline `s 6, item 1) "
                "on the same grounds regardless of corpus. This recompute "
                "only refreshes the numbers, not the interpretation."
            ),
            "expected_number_stability": (
                "The species-fix (commit f65521a in "
                "scripts/build_block_c_tier3_manifest.py) affected "
                "manifest/pocket/ligand columns; the P4/P5 predicate axes "
                "(d_npxxy_y558_y753_oh, d_gpcrdb_tm6_tilt_246_637_ca) and "
                "the `passed` column are byte-identical between "
                "rows.tier3.csv and rows.tier3.v2.csv on all 40 800 rows "
                "(verified directly during this recompute). So numeric "
                "shifts here are expected to be exactly zero; the "
                "side-by-side table exists to document that, not to "
                "surface a change."
            ),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2, default=str)

    print(f"wrote {args.out}")
    print()
    print("P4 (post-species-fix v2 corpus):")
    for bb in BACKBONES:
        v = p4_new[bb]
        pre = PRE_FIX["P4"][bb]
        print(f"  {bb:9s} pre  {pre['n_correct']}/{pre['n_tested']} "
              f"[{pre['ci_95'][0]:5.2f}, {pre['ci_95'][1]:5.2f}]  "
              f"post {v['n_correct']}/{v['n_tested']} "
              f"[{v['pass_count_ci_95'][0]:5.2f}, "
              f"{v['pass_count_ci_95'][1]:5.2f}]  "
              f"gate={v['fire_gate']}")
    print()
    print("P5 (post-species-fix v2 corpus):")
    for bb in BACKBONES:
        v = p5_new[bb]
        pre = PRE_FIX["P5"][bb]
        print(f"  {bb:9s} pre  {pre['panel_mean_abs']:+.4f} "
              f"[{pre['ci_95'][0]:+.4f}, {pre['ci_95'][1]:+.4f}]  "
              f"post {v['panel_mean_abs']:+.4f} "
              f"[{v['panel_ci_95'][0]:+.4f}, "
              f"{v['panel_ci_95'][1]:+.4f}]  "
              f"gate={v['fire_gate']}")


if __name__ == "__main__":
    main()
