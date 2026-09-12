#!/usr/bin/env python3
"""T4 — receptor accounting + stratum arithmetic.

  T4.1 FSHR + LSHR per-receptor apo coherent-active fraction from Block A rows.
  T4.2 Reconcile v3 bound=11.8% (n=26) with v5 clean-bound=6.84% (n=24) after
       stripping FSHR + LSHR. Arithmetic implies each stripped receptor
       averages ~71 % coherent-active. Verify empirically.
  T4.3 Canonical receptor membership table.
  T4.4 2×2 without FSHR / LSHR — determine whether they are in the n=23
       common set at all (they are Class C / F for FSHR / LSHR respectively —
       likely not in Class A pocket 2×2 by construction).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from stage3_post_audit_analysis import stage3a_2x2  # type: ignore  # noqa: E402

OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/reaudit_2026_09_07"
OUT = OUT_DIR / "t4_stratum_arithmetic.json"

# Two-instrument predicate literals (scripts/analyse_block_c_tier3_headline.py:58-59;
# also duplicated in _task2_p4_ties.py:30-42 and _task6_p0_correlation.py:36-42).
NPXXY_OH_LT = 9.082
TM6_TILT_GT = 14.932

ROWS_TIER3 = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_TIER3 = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
ROWS_POCKET = REPO / "experiments/018_block_a_switch_test/analysis/rows.pocket.csv"
ROWS_RMSD = REPO / "experiments/018_block_a_switch_test/analysis/rows.rmsd.csv"

V_JSONS = {
    "task_A_v2": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_A_v2_agonist_vs_decoy_apo_same_complex.json",
    "task_A_v3": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_A_v3_composition_check.json",
    "stage3b_v2": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/stage3b_v2_same_complex_split.json",
    "task_E_v3": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_E_v3_scoped_finding.json",
    "task_F_v3": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_F_v3_reference_state_stratification.json",
    "task_F_v5": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_F_v5_clean_bound_stripped.json",
    "task6_p0": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task6_p0_correlation.json",
    "cohens_d": REPO / "experiments/018_block_a_switch_test/analysis/verification/cohens_d_block_a_d_tm6.json",
}


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _f(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return float("nan")


def is_active(oh, tilt) -> bool | None:
    oh_f = _f(oh)
    tilt_f = _f(tilt)
    if math.isnan(oh_f) or math.isnan(tilt_f):
        return None
    return (oh_f < NPXXY_OH_LT) and (tilt_f > TM6_TILT_GT)


def block_a_apo_coherent_active(rows_pocket_csv: Path, receptors: set[str]) -> dict:
    """Per (receptor, backbone) coherent-active fraction on Block A apo arm.

    Follows the pattern of Task F v3/v5: for a given receptor, coherent-active
    fraction = fraction of apo rows where is_active is True. Task F reads the
    ``rows.pocket.csv`` corpus and stratifies by receptor.
    """
    counts: dict = defaultdict(lambda: {"n": 0, "n_active": 0})
    with rows_pocket_csv.open() as f:
        for r in csv.DictReader(f):
            rec = (r.get("receptor_slug") or "").upper()
            if rec not in receptors:
                continue
            if str(r.get("passed", "")).lower() != "true":
                continue
            # Block A input_path pattern encodes backbone as a subdirectory.
            input_path = r.get("input_path", "")
            bb = ""
            for candidate in ("boltz", "chai", "of3", "protenix", "af2mm"):
                if f"_{candidate}_" in input_path or f"/{candidate}/" in input_path:
                    bb = candidate
                    break
            input_state = (r.get("input_state_claim") or "").strip()
            # Block A apo rows use state=Ga-coupled-active with partner=apo;
            # arm inferred from partner_type. Fallback: check input_path for /apo/.
            if "/apo/" not in input_path:
                continue
            v = is_active(r.get("d_npxxy_y558_y753_oh", ""), r.get("d_gpcrdb_tm6_tilt_246_637_ca", ""))
            if v is None:
                continue
            key = (rec, bb)
            counts[key]["n"] += 1
            if v:
                counts[key]["n_active"] += 1
    return {
        f"{rec}|{bb}": {"n": c["n"], "n_active": c["n_active"],
                        "fraction": (c["n_active"] / c["n"] if c["n"] else float("nan"))}
        for (rec, bb), c in counts.items()
    }


def load_block_a_apo_per_receptor(rows_pocket_csv: Path) -> dict:
    """Per-receptor apo coherent-active fraction (mean across backbones).

    Block A input_path pattern:
      .../018_block_a_switch_test_<recep>_<arm>_<bb>/<hash>/<bb>/seed_.../...
    where arm ∈ {apo, cognate}. Extract via _apo_ / _cognate_ substring.
    """
    per_bb = defaultdict(lambda: {"n": 0, "n_active": 0})
    with rows_pocket_csv.open() as f:
        for r in csv.DictReader(f):
            rec = (r.get("receptor_slug") or "").upper()
            if str(r.get("passed", "")).lower() != "true":
                continue
            input_path = r.get("input_path", "")
            # Block A path encodes arm as "_apo_" or "_cognate_" segment.
            if "_apo_" not in input_path:
                continue
            bb = ""
            for candidate in ("boltz", "chai", "of3", "protenix", "af2mm"):
                if f"_{candidate}/" in input_path or f"/{candidate}/" in input_path:
                    bb = candidate
                    break
            v = is_active(r.get("d_npxxy_y558_y753_oh", ""), r.get("d_gpcrdb_tm6_tilt_246_637_ca", ""))
            if v is None:
                continue
            per_bb[(rec, bb)]["n"] += 1
            if v:
                per_bb[(rec, bb)]["n_active"] += 1
    per_rec: dict[str, list[float]] = defaultdict(list)
    for (rec, bb), c in per_bb.items():
        if c["n"]:
            per_rec[rec].append(c["n_active"] / c["n"])
    per_rec_mean = {rec: (sum(v) / len(v) if v else float("nan")) for rec, v in per_rec.items()}
    return {"per_bb": {f"{r}|{b}": {"n": v["n"], "n_active": v["n_active"],
                                     "fraction": (v["n_active"] / v["n"] if v["n"] else float("nan"))}
                        for (r, b), v in per_bb.items()},
            "per_rec_mean_across_bb": per_rec_mean}


def build_canonical_table() -> list[dict]:
    task_A_v3 = json.loads(V_JSONS["task_A_v3"].read_text())
    task_F_v5 = json.loads(V_JSONS["task_F_v5"].read_text())
    task_E_v3 = json.loads(V_JSONS["task_E_v3"].read_text())
    task6 = json.loads(V_JSONS["task6_p0"].read_text())
    cohens = json.loads(V_JSONS["cohens_d"].read_text())

    recallable = set(task_A_v3["strata"]["recallable_receptors"])
    mustgen = set(task_A_v3["strata"]["must_generalise_receptors"])

    v5_stats = task_F_v5["stratum_stats"]
    v5_bound = set(v5_stats["v5_clean_bound_24"]["receptors"])
    v5_free = set(v5_stats["refined_v3_free_5"]["receptors"])

    # Task E n=4,500 scoped: OF3+Protenix × neutral_antag × ref-matched.
    # Task E v3 doesn't enumerate per-receptor membership — the JSON just
    # rolls up per-cell (backbone × ligand_role × partner_type) totals.
    # Leave the set empty; the aggregate n=4,500 across 4 cells is the
    # scope, not a receptor list. Fall back to marking receptors "unknown"
    # for this axis.
    e_receptors = set()  # not enumerable from task_E_v3.json alone

    p0_receptors = set(task6["receptors_used"])
    cohens_receptors = set(cohens["receptors_in_common"])

    # Compute the 2×2 n=23 receptor set from the corpus (stage3_2x2 common set
    # is agonist × antagonist common — we don't have it enumerated in any
    # JSON, so we compute it in the main flow later and pass down.)
    # Placeholder — will be filled by caller.
    return {
        "recallable_15": sorted(recallable),
        "mustgen_13": sorted(mustgen),
        "v5_clean_bound_24": sorted(v5_bound),
        "v5_free_5": sorted(v5_free),
        "p0_correlation_35": sorted(p0_receptors),
        "cohens_d_block_a": sorted(cohens_receptors),
        "task_e_receptors_from_cells": sorted(e_receptors),
    }


def compute_2x2_common_receptor_set(records: list[dict]) -> set[str]:
    """Replicate stage3a_2x2's common_receptors logic for boltz backbone —
    same universe across backbones since receptor list is fixed by data."""
    common_per_bb: dict[str, set[str]] = {}
    for bb in sorted({(r.get("backbone") or "").lower() for r in records if r.get("backbone")}):
        ag_a, ag_i, an_a, an_i = set(), set(), set(), set()
        for r in records:
            if (r.get("backbone") or "").lower() != bb:
                continue
            if str(r.get("passed", "")).lower() != "true":
                continue
            if (r.get("receptor_class") or "").upper() != "A":
                continue
            rec = (r.get("receptor_slug") or "").upper()
            role = (r.get("ligand_role") or "").strip()
            va = _f(r.get("pocket_ca_rmsd_active"))
            vi = _f(r.get("pocket_ca_rmsd_inactive"))
            if math.isnan(va) or math.isnan(vi):
                continue
            if role == "full_agonist":
                ag_a.add(rec); ag_i.add(rec)
            elif role in ("neutral_antagonist", "inverse_agonist"):
                an_a.add(rec); an_i.add(rec)
        common_per_bb[bb] = ag_a & ag_i & an_a & an_i
    # Take intersection across all backbones (same n_common=23 for all in campaign).
    if not common_per_bb:
        return set()
    common = set.intersection(*common_per_bb.values())
    return common


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("[T4] loading Block A rows.pocket.csv...")
    ba = load_block_a_apo_per_receptor(ROWS_POCKET)

    fshr_lshr_recompute = {
        "FSHR": {
            "per_backbone": {
                b: v for kb, v in ba["per_bb"].items()
                for r, b in [kb.split("|", 1)] if r == "FSHR"
            },
            "mean_across_backbones": ba["per_rec_mean_across_bb"].get("FSHR", float("nan")),
        },
        "LSHR": {
            "per_backbone": {
                b: v for kb, v in ba["per_bb"].items()
                for r, b in [kb.split("|", 1)] if r == "LSHR"
            },
            "mean_across_backbones": ba["per_rec_mean_across_bb"].get("LSHR", float("nan")),
        },
    }

    # Read v3 and v5 stratum stats.
    v3 = json.loads(V_JSONS["task_F_v3"].read_text())
    v5 = json.loads(V_JSONS["task_F_v5"].read_text())
    v3_bound = v3.get("stratified_refined_3", {}).get("g_protein_bound", {})
    v5_bound = v5["stratum_stats"]["v5_clean_bound_24"]
    v3_bound_stats = v3_bound if isinstance(v3_bound, dict) else {}
    v3_bound_mean = v3_bound_stats.get("mean_coherent_active_fraction_v2_convention_div_by_all") \
        or v3_bound_stats.get("mean_coherent_active_fraction_valid_only")
    v3_bound_n = v3_bound_stats.get("n_receptors")

    v5_bound_mean = v5_bound["mean_v2_convention_div_by_all"]
    v5_bound_n = v5_bound["n_receptors"]

    # Arithmetic reconciliation:
    # v3 mean × v3_n − v5 mean × v5_n = sum-of-fractions of stripped receptors
    if v3_bound_mean is not None and v5_bound_mean is not None and v3_bound_n and v5_bound_n:
        implied_sum = v3_bound_mean * v3_bound_n - v5_bound_mean * v5_bound_n
        n_stripped = v3_bound_n - v5_bound_n
        implied_per_stripped = implied_sum / n_stripped if n_stripped else float("nan")
    else:
        implied_sum = implied_per_stripped = float("nan")
        n_stripped = None

    # Empirical FSHR + LSHR apo coherent-active from Block A rows (mean across backbones)
    fshr_mean = fshr_lshr_recompute["FSHR"]["mean_across_backbones"]
    lshr_mean = fshr_lshr_recompute["LSHR"]["mean_across_backbones"]
    fshr_lshr_avg = ((fshr_mean if not math.isnan(fshr_mean) else 0)
                     + (lshr_mean if not math.isnan(lshr_mean) else 0)) / 2

    # But — task_F v5 uses rows.pocket + rows.rmsd COMBINED coherent-active
    # (coherent-active = passes NPXXY-OH AND TM6-tilt AND close-to-active-crystal-RMSD).
    # Task F's number is a stricter predicate. So my "apo coherent-active" from
    # block A rows.pocket is on the two-instrument predicate; if v5 uses coh_active
    # (with the RMSD condition), the numbers can differ meaningfully.
    #
    # To reconcile properly, read the per-receptor breakdown from task_F_v5.

    per_rec_v5 = v5.get("per_receptor_apo_summary", {})
    fshr_v5 = per_rec_v5.get("FSHR", {})
    lshr_v5 = per_rec_v5.get("LSHR", {})

    reconciliation = {
        "v3_bound_mean_pct": v3_bound_mean * 100 if v3_bound_mean else None,
        "v3_bound_n": v3_bound_n,
        "v5_bound_mean_pct": v5_bound_mean * 100 if v5_bound_mean else None,
        "v5_bound_n": v5_bound_n,
        "n_stripped": n_stripped,
        "implied_sum_of_stripped_fractions": implied_sum,
        "implied_average_per_stripped_receptor_pct": implied_per_stripped * 100 if not math.isnan(implied_per_stripped) else None,
        "empirical_FSHR_apo_coh_active_from_block_A_rows_pocket_pct": fshr_mean * 100 if not math.isnan(fshr_mean) else None,
        "empirical_LSHR_apo_coh_active_from_block_A_rows_pocket_pct": lshr_mean * 100 if not math.isnan(lshr_mean) else None,
        "fshr_lshr_task_F_v5_per_receptor_entry": {
            "FSHR": fshr_v5,
            "LSHR": lshr_v5,
        },
        "note": (
            "task_F uses coherent-active (two-instrument predicate AND best-of-100 "
            "RMSD to active crystal below a threshold) — a stricter definition than "
            "the two-instrument predicate alone. The Block A rows.pocket recompute is "
            "on the two-instrument predicate. See task_F_v5_clean_bound_stripped.json "
            "for the coh_active fractions used in the stratum mean."
        ),
    }

    # Canonical receptor table from JSONs — v5 provides the definitive membership.
    canonical_sets = build_canonical_table()

    # Compute the 2×2 common receptor set from rows.tier3.v2.
    print("[T4] loading tier3 rows + manifest, computing 2×2 common receptor set...")
    rows = pd.read_csv(ROWS_TIER3, low_memory=False)
    manifest = pd.read_csv(MANIFEST_TIER3, low_memory=False)
    m_idx = manifest.set_index("prediction_path")
    rows["backbone"] = rows["input_path"].map(m_idx["backbone"].to_dict()).fillna("")
    rows["partner_type"] = rows["input_path"].map(m_idx["partner_type"].to_dict()).fillna("")
    if "ligand_role" in m_idx.columns:
        fb = rows.get("ligand_role", pd.Series([""] * len(rows)))
        rows["ligand_role"] = rows["input_path"].map(m_idx["ligand_role"].to_dict()).fillna(fb)
    records = rows.astype(str).to_dict("records")
    common_2x2 = compute_2x2_common_receptor_set(records)
    canonical_sets["two_by_two_common_n23"] = sorted(common_2x2)

    # Assemble the canonical receptor table.
    all_receptors = set()
    for k, v in canonical_sets.items():
        all_receptors |= set(v)
    # Also union in FSHR/LSHR + everything in cohens_d panel:
    all_receptors |= {"FSHR", "LSHR"}
    table = []
    for rec in sorted(all_receptors):
        row = {"receptor_slug": rec}
        for k, v in canonical_sets.items():
            row[k] = (rec in set(v))
        table.append(row)

    # Reason-for-exclusion column — a compact string per receptor listing analyses that omit it.
    for row in table:
        excluded_from = [k for k in canonical_sets if not row[k]]
        row["excluded_from"] = excluded_from
        row["n_excluded"] = len(excluded_from)

    # T4.4 — 2×2 without FSHR / LSHR.
    fshr_in_2x2 = "FSHR" in common_2x2
    lshr_in_2x2 = "LSHR" in common_2x2
    if fshr_in_2x2 or lshr_in_2x2:
        excluded = frozenset({"FSHR", "LSHR"})
        result_ex = stage3a_2x2(records, excluded_receptors=excluded)
    else:
        result_ex = {
            "not_run": True,
            "reason": (
                f"FSHR in 2×2 common: {fshr_in_2x2}; LSHR in 2×2 common: {lshr_in_2x2}. "
                "Both are NOT in the Class A pocket-Cα 2×2 common set — likely because "
                "FSHR is Class C and LSHR is Class C (both are glycoprotein hormone receptors, "
                "which are Class A per GPCRdb but may fail the pocket_positions Class A short-circuit). "
                "The 2×2 excluding FSHR/LSHR is therefore identical to the published 2×2."
            ),
        }

    verdict = []
    # Verdict on FSHR/LSHR arithmetic:
    if implied_per_stripped is not None and not math.isnan(implied_per_stripped):
        if abs(implied_per_stripped - 0.713) < 0.05:
            verdict.append(
                f"ARITHMETIC_CONSISTENT: implied ~{implied_per_stripped*100:.1f}% per stripped receptor "
                "matches the 26×0.118 − 24×0.068 arithmetic expectation."
            )
        else:
            verdict.append(
                f"ARITHMETIC_ANOMALY: implied per-stripped fraction "
                f"({implied_per_stripped*100:.1f}%) does not match the expected ~71%. "
                "One of v3/v5 stratum means may be wrong."
            )
    # Empirical verdict:
    fshr_v5_frac = fshr_v5.get("coh_active_fraction") if isinstance(fshr_v5, dict) else None
    lshr_v5_frac = lshr_v5.get("coh_active_fraction") if isinstance(lshr_v5, dict) else None
    if fshr_v5_frac is not None and lshr_v5_frac is not None:
        verdict.append(
            f"TASK_F_V5_ENTRY: FSHR coh_active={fshr_v5_frac:.3f}, LSHR coh_active={lshr_v5_frac:.3f}"
        )

    report = {
        "task": "T4_stratum_arithmetic",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "_provenance": {
            "inputs": {
                str(p.relative_to(REPO)): sha(p) for p in [
                    ROWS_TIER3, MANIFEST_TIER3, ROWS_POCKET, ROWS_RMSD,
                    *V_JSONS.values(),
                ]
            },
            "script": {
                "path": str(Path(__file__).relative_to(REPO)),
                "sha256": sha(Path(__file__)),
            },
            "git_head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                                        capture_output=True, text=True).stdout.strip(),
            "rng_seed_used": "n/a (deterministic recomputation)",
        },
        "fshr_lshr_recompute": fshr_lshr_recompute,
        "stratum_reconciliation": reconciliation,
        "canonical_receptor_table": table,
        "canonical_membership_sets": {k: sorted(v) for k, v in canonical_sets.items()},
        "two_by_two_without_fshr_lshr": {
            "fshr_in_2x2_common": fshr_in_2x2,
            "lshr_in_2x2_common": lshr_in_2x2,
            "result": result_ex,
        },
        "verdict": verdict,
    }
    OUT.write_text(json.dumps(report, indent=2, default=str))
    print(f"[T4] wrote {OUT.relative_to(REPO)}")
    print()
    print("=" * 78)
    print("T4 summary")
    print("=" * 78)
    print(f"FSHR apo coh_active (empirical, block A two-instrument): "
          f"{reconciliation['empirical_FSHR_apo_coh_active_from_block_A_rows_pocket_pct']}")
    print(f"LSHR apo coh_active (empirical, block A two-instrument): "
          f"{reconciliation['empirical_LSHR_apo_coh_active_from_block_A_rows_pocket_pct']}")
    print(f"Task F v5 FSHR entry: {fshr_v5}")
    print(f"Task F v5 LSHR entry: {lshr_v5}")
    print(f"v3 bound mean × n26 = {v3_bound_mean * v3_bound_n if v3_bound_mean else 'n/a'}")
    print(f"v5 bound mean × n24 = {v5_bound_mean * v5_bound_n}")
    print(f"implied avg per stripped receptor: {implied_per_stripped*100:.1f}%" if not math.isnan(implied_per_stripped) else "n/a")
    print(f"n_2x2_common = {len(common_2x2)}, FSHR in set: {fshr_in_2x2}, LSHR in set: {lshr_in_2x2}")
    print(f"Canonical table has {len(table)} receptors across {len(canonical_sets)} membership axes.")
    for v in verdict:
        print(f"  - {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
