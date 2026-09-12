#!/usr/bin/env python3
"""PR5 — Fast-path match-count census on Boltz/Chai ligand rows.

Concern: `ligand_rmsd_to_ref` values in `rows.tier3.v2.csv` were computed
under the pre-MCS scorer (no `pocket_ligand_atom_map_method` column
exists in the CSV — the MCS refactor landed AFTER rescore). Under that
pre-MCS regime:
  - >= 5 (atom_name, element) matches → fast path returned an RMSD
  - <  5 matches                     → NaN

Question: on Boltz/Chai (SMILES-derived atom names, expected atom-name
mismatch), how many rows nonetheless returned a value, and what's the
match-count distribution? If Boltz/Chai rows land in the low-match tail
(5-8 matches) on ligands with 20-30 heavy atoms, the RMSDs are likely
spurious partial overlaps.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]

ROWS_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
OUT_JSON = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/pr5_matchcount_census.json"

MATCH_RE = re.compile(r"matched_(\d+)_of_pred_(\d+)_ref_(\d+)")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    print("[PR5] loading data...")
    rows = pd.read_csv(ROWS_CSV, low_memory=False)
    manifest = pd.read_csv(MANIFEST_CSV, low_memory=False)
    m_idx = manifest.set_index("prediction_path")
    rows["backbone"] = rows["input_path"].map(m_idx["backbone"].to_dict()).fillna("")
    rows["partner_type"] = rows["input_path"].map(m_idx["partner_type"].to_dict()).fillna("")
    for col in ("ligand_role",):
        fb = rows.get(col, pd.Series([""] * len(rows)))
        rows[col] = rows["input_path"].map(m_idx[col].to_dict()).fillna(fb)
    rows["arm"] = rows["partner_type"].apply(
        lambda p: "apo" if str(p).lower() == "apo" else "cognate"
    )

    passed = rows["passed"].astype(str).str.lower() == "true"
    class_a = rows["receptor_class"].fillna("").astype(str).str.upper() == "A"
    rows = rows[passed & class_a].copy()
    print(f"[PR5] {len(rows)} passing Class-A rows")

    # Parse the "matched_X_of_pred_Y_ref_Z" tag from pocket_notes.
    def parse_note(note):
        s = str(note) if note is not None else ""
        m = MATCH_RE.search(s)
        if not m:
            return (None, None, None)
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))

    parsed = rows["pocket_notes"].apply(parse_note)
    rows["fastpath_matched"] = [p[0] for p in parsed]
    rows["fastpath_pred_n"] = [p[1] for p in parsed]
    rows["fastpath_ref_n"] = [p[2] for p in parsed]

    # ligand_rmsd_to_ref populated vs NaN
    rows["lig_rmsd_valued"] = pd.to_numeric(
        rows["ligand_rmsd_to_ref"], errors="coerce"
    ).notna()

    # ============================================================
    # 1. Per (backbone × ligand_role × arm × valued/NaN) counts.
    # ============================================================
    counts = (
        rows.groupby(["backbone", "ligand_role", "arm", "lig_rmsd_valued"])
        .size()
        .reset_index(name="n")
    )
    counts_records = counts.to_dict("records")

    # ============================================================
    # 2. Boltz/Chai fast-path match-count distribution.
    # ============================================================
    bc = rows[rows["backbone"].isin(["boltz", "chai"])].copy()
    of3_pnx = rows[rows["backbone"].isin(["of3", "protenix"])].copy()

    def dist_summary(df, name):
        matched = df["fastpath_matched"].dropna().astype(int)
        pred_n = df["fastpath_pred_n"].dropna().astype(int)
        if len(matched) == 0:
            return {"name": name, "n_rows_with_match_note": 0}
        bins = {
            "0": int((matched == 0).sum()),
            "1-4": int(((matched >= 1) & (matched <= 4)).sum()),
            "5-8": int(((matched >= 5) & (matched <= 8)).sum()),
            "9-15": int(((matched >= 9) & (matched <= 15)).sum()),
            "16-25": int(((matched >= 16) & (matched <= 25)).sum()),
            "26+": int((matched >= 26).sum()),
        }
        return {
            "name": name,
            "n_rows_with_match_note": int(len(matched)),
            "match_count_bins": bins,
            "match_count_mean": float(matched.mean()),
            "match_count_median": float(matched.median()),
            "match_count_p5": float(np.percentile(matched, 5)),
            "match_count_p95": float(np.percentile(matched, 95)),
            "pred_n_mean": float(pred_n.mean()) if len(pred_n) else None,
            "pred_n_median": float(pred_n.median()) if len(pred_n) else None,
        }

    dist_boltz = dist_summary(rows[rows["backbone"] == "boltz"], "boltz")
    dist_chai = dist_summary(rows[rows["backbone"] == "chai"], "chai")
    dist_of3 = dist_summary(rows[rows["backbone"] == "of3"], "of3")
    dist_pnx = dist_summary(rows[rows["backbone"] == "protenix"], "protenix")

    # ============================================================
    # 3. Rows-at-risk: Boltz/Chai with 5-8 matches AND pred_n >= 15
    #    (suggesting partial spurious overlap on a substantial ligand).
    # ============================================================
    at_risk = bc[
        bc["fastpath_matched"].between(5, 8)
        & (bc["fastpath_pred_n"] >= 15)
    ]
    at_risk_count = int(len(at_risk))
    at_risk_by_bb = at_risk.groupby("backbone").size().to_dict()

    # Also: any row where fastpath succeeded (has a "matched_" note) is
    # by definition >= 5 matches (else the code produced no RMSD). But we
    # want to break the >= 5 group into low (5-8) vs high (>=9) fast-path
    # cases, because the low-match case is the spurious-fastpath risk.
    bc_valued = bc[bc["lig_rmsd_valued"]]
    bc_populated_low_match = bc_valued[bc_valued["fastpath_matched"].between(5, 8)]
    bc_populated_low_match_n = int(len(bc_populated_low_match))
    bc_valued_n = int(len(bc_valued))
    bc_frac_low_match_of_valued = (
        bc_populated_low_match_n / bc_valued_n if bc_valued_n else 0.0
    )

    # ============================================================
    # 4. Verdict.
    # ============================================================
    total_bc = int(len(bc))
    frac_bc_valued = bc_valued_n / total_bc if total_bc else 0.0

    if bc_valued_n == 0:
        verdict = "BOLTZ_CHAI_ALL_NAN_AS_EXPECTED"
        verdict_note = (
            "Zero Boltz/Chai rows carry a valid ligand_rmsd_to_ref. "
            "This matches the SMILES-atom-name divergence expectation. "
            "MCS matcher (post-scorer landing) needed to unlock any "
            "Boltz/Chai pose evidence — this is T7b territory."
        )
    elif bc_populated_low_match_n / max(bc_valued_n, 1) > 0.5:
        verdict = "FAST_PATH_SUSPECT_ON_BOLTZ_CHAI"
        verdict_note = (
            f"{bc_populated_low_match_n} of {bc_valued_n} valued "
            f"Boltz/Chai rows have 5-8 fast-path matches. That's "
            f"{bc_frac_low_match_of_valued * 100:.1f}% low-match. "
            f"Spurious partial overlap is likely on many of these; "
            f"MCS-based recompute will change these values."
        )
    else:
        verdict = "FAST_PATH_LOOKS_CLEAN"
        verdict_note = (
            f"Most valued Boltz/Chai rows have ≥ 9 fast-path matches; "
            f"low-match tail = {bc_populated_low_match_n} / {bc_valued_n} "
            f"({bc_frac_low_match_of_valued * 100:.1f}%)."
        )

    # ============================================================
    # 5. Also flag: no `pocket_ligand_atom_map_method` column present.
    #    That means the MCS matcher (in current source) has NOT been
    #    applied to this corpus.
    # ============================================================
    has_method_col = "pocket_ligand_atom_map_method" in pd.read_csv(
        ROWS_CSV, nrows=0
    ).columns
    mcs_applied_to_corpus = has_method_col

    report = {
        "task": "PR5_matchcount_census",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows": {"path": str(ROWS_CSV.relative_to(REPO)), "sha256": sha256_file(ROWS_CSV)},
            "manifest": {"path": str(MANIFEST_CSV.relative_to(REPO)), "sha256": sha256_file(MANIFEST_CSV)},
        },
        "corpus_state": {
            "pocket_ligand_atom_map_method_column_present": has_method_col,
            "mcs_matcher_applied_to_corpus": mcs_applied_to_corpus,
            "note": (
                "MCS matcher landed post-rescore; corpus values reflect "
                "pre-MCS fast-path-only scorer. T7b (HPC recompute) would "
                "regenerate ligand_rmsd_to_ref with the new matcher."
            ) if not has_method_col else None,
        },
        "per_backbone_ligand_role_arm_valued_counts": counts_records,
        "per_backbone_match_count_distribution": {
            "boltz": dist_boltz,
            "chai": dist_chai,
            "of3": dist_of3,
            "protenix": dist_pnx,
        },
        "boltz_chai_summary": {
            "n_rows_total": total_bc,
            "n_rows_ligand_rmsd_valued": bc_valued_n,
            "frac_valued": frac_bc_valued,
            "n_rows_valued_low_match_5_to_8": bc_populated_low_match_n,
            "frac_low_match_of_valued": bc_frac_low_match_of_valued,
            "n_rows_at_risk_low_match_and_pred_n_ge_15": at_risk_count,
            "at_risk_by_backbone": at_risk_by_bb,
        },
        "verdict": verdict,
        "verdict_note": verdict_note,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, default=str))
    print(f"wrote {OUT_JSON.relative_to(REPO)}")
    print()
    print("=" * 74)
    print("PR5 verdict:", verdict)
    print("=" * 74)
    print(f"  Corpus mcs_applied_to_corpus: {mcs_applied_to_corpus}")
    print(f"  Boltz+Chai total: {total_bc}")
    print(f"  Boltz+Chai valued (fastpath >= 5): {bc_valued_n} ({frac_bc_valued*100:.1f}%)")
    print(f"  Boltz+Chai low-match (5-8): {bc_populated_low_match_n} "
          f"({bc_frac_low_match_of_valued*100:.1f}% of valued)")
    print(f"  At-risk (5-8 matches on ligand w/ >=15 heavy atoms): {at_risk_count}")
    print()
    print(f"  Match-count distribution (nonzero-only cells):")
    for name, d in [("boltz", dist_boltz), ("chai", dist_chai),
                    ("of3", dist_of3), ("protenix", dist_pnx)]:
        bins = d.get("match_count_bins", {})
        print(f"    {name:<10} n_with_note={d.get('n_rows_with_match_note', 0):>6} "
              f"bins={bins} mean={d.get('match_count_mean', 0):.1f}")
    print()
    print(verdict_note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
