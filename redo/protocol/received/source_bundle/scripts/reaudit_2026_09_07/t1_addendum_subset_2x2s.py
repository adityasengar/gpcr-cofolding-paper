#!/usr/bin/env python3
"""T1 addendum — additional 2×2 subset checks requested during audit review.

  (a) 2×2 on the 8 self-reference receptors alone: named list + row counts +
      per-backbone Δ/CI. This shows what the signal looks like on the very
      cells the T1 restriction dropped.
  (b) 2×2 on apo-only ∩ self-reference-excluded (rows.arm=="apo" AND
      neither ref matches input_bound_pdb). The cleanest possible cell —
      no cognate ceiling, no self-comparison — with clean-room CIs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
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
from stage3_post_audit_analysis import stage3a_2x2  # type: ignore  # noqa: E402

ROWS_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
REF_SET_CSV = REPO / "refs/reference_set.csv"

OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/reaudit_2026_09_07"
OUT_JSON = OUT_DIR / "t1_addendum_subset_2x2s.json"


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


def resolve_ref_pdb(lookup, receptor, role, role_specific=""):
    receptor = receptor.upper()
    role = role.lower()
    if role == "active":
        return lookup.get((receptor, "active", ""), "")
    if role == "inactive":
        if role_specific:
            hit = lookup.get((receptor, "inactive", role_specific))
            if hit:
                return hit
        return lookup.get((receptor, "inactive", ""), "")
    return ""


def build_ref_lookup(ref_set):
    d = {}
    for _, r in ref_set.iterrows():
        recep = str(r.get("receptor_slug") or "").upper().strip()
        role = str(r.get("role") or "").lower().strip()
        role_specific = str(r.get("role_specific") or "").strip()
        pdb = str(r.get("pdb_id") or "").upper().strip()
        if recep and role and pdb:
            d[(recep, role, role_specific)] = pdb
    return d


def role_pair_for_ligand(ligand_role):
    if ligand_role == "neutral_antagonist":
        return ("inactive", "inactive_neutral_antagonist")
    if ligand_role == "inverse_agonist":
        return ("inactive", "inactive_inverse_agonist")
    return ("active", "")


def clean_room_2x2_bootstrap(records, n_iter=5000, seed=20260907):
    """Same math as stage3a_2x2 but numpy-only, different seed."""
    per_bb = {}
    rng = np.random.default_rng(seed)
    for bb in sorted({(r.get("backbone") or "").lower() for r in records if r.get("backbone")}):
        ag_a, ag_i, an_a, an_i = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
        for r in records:
            if (r.get("backbone") or "").lower() != bb:
                continue
            if str(r.get("passed", "")).lower() != "true":
                continue
            if (r.get("receptor_class") or "").upper() != "A":
                continue
            recep = (r.get("receptor_slug") or "").upper()
            role = (r.get("ligand_role") or "").strip()
            v_a = _to_float(r.get("pocket_ca_rmsd_active"))
            v_i = _to_float(r.get("pocket_ca_rmsd_inactive"))
            if math.isnan(v_a) or math.isnan(v_i):
                continue
            if role == "full_agonist":
                ag_a[recep].append(v_a); ag_i[recep].append(v_i)
            elif role in ("neutral_antagonist", "inverse_agonist"):
                an_a[recep].append(v_a); an_i[recep].append(v_i)
        common = sorted(set(ag_a) & set(ag_i) & set(an_a) & set(an_i))
        n = len(common)
        if n == 0:
            per_bb[bb] = {"n": 0}
            continue

        def pool_mean(d, s):
            xs = [v for c in s for v in d[c]]
            return float(np.mean(xs)) if xs else float("nan")

        pt = (pool_mean(ag_a, common) - pool_mean(an_a, common)) \
             - (pool_mean(ag_i, common) - pool_mean(an_i, common))
        reps = np.empty(n_iter, dtype=float)
        common_arr = np.array(common)
        for i in range(n_iter):
            idx = rng.integers(0, n, size=n)
            s = list(common_arr[idx])
            a1, a2 = pool_mean(ag_a, s), pool_mean(an_a, s)
            i1, i2 = pool_mean(ag_i, s), pool_mean(an_i, s)
            reps[i] = ((a1 - a2) - (i1 - i2)) if not any(math.isnan(x) for x in (a1, a2, i1, i2)) else float("nan")
        rc = reps[~np.isnan(reps)]
        lo, hi = (float(np.percentile(rc, 2.5)), float(np.percentile(rc, 97.5))) if len(rc) else (float("nan"), float("nan"))
        per_bb[bb] = {
            "n_common": int(n),
            "n_rows_agonist": int(sum(len(v) for v in ag_a.values())),
            "n_rows_antag": int(sum(len(v) for v in an_a.values())),
            "estimate": float(pt),
            "ci_lo": lo,
            "ci_hi": hi,
            "signed_nonzero": (lo > 0 and hi > 0) or (lo < 0 and hi < 0) if not (math.isnan(lo) or math.isnan(hi)) else False,
        }
    return per_bb


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(OUT_JSON))
    args = parser.parse_args()

    print("[T1-add] loading data...")
    rows = pd.read_csv(ROWS_CSV, low_memory=False)
    manifest = pd.read_csv(MANIFEST_CSV, low_memory=False)
    ref_set = pd.read_csv(REF_SET_CSV, low_memory=False)
    m_idx = manifest.set_index("prediction_path")

    rows["input_bound_pdb"] = rows["input_path"].map(m_idx["ligand_bound_pdb"].to_dict()).fillna("")
    rows["backbone"] = rows["input_path"].map(m_idx["backbone"].to_dict()).fillna("")
    rows["partner_type"] = rows["input_path"].map(m_idx["partner_type"].to_dict()).fillna("")
    rows["arm"] = rows["partner_type"].apply(lambda p: "apo" if str(p).lower() == "apo" else "cognate")

    ref_lookup = build_ref_lookup(ref_set)
    receptors = rows["receptor_slug"].fillna("").astype(str).str.upper()
    ligand_roles = rows["ligand_role"].fillna("").astype(str)

    rows["ref_pdb_active_recomputed"] = [resolve_ref_pdb(ref_lookup, r, "active", "") for r in receptors]
    rows["ref_pdb_inactive_recomputed"] = [
        resolve_ref_pdb(ref_lookup, r, *role_pair_for_ligand(lr)) if role_pair_for_ligand(lr)[0] == "inactive"
        else resolve_ref_pdb(ref_lookup, r, "inactive", "")
        for r, lr in zip(receptors, ligand_roles)
    ]

    rows_a = rows[
        (rows["receptor_class"].fillna("").astype(str).str.upper() == "A")
        & (rows["passed"].astype(str).str.lower() == "true")
    ].copy()
    rows_a["input_bound_pdb_u"] = rows_a["input_bound_pdb"].fillna("").astype(str).str.upper().str.strip()
    rows_a["ref_matches_active"] = (
        (rows_a["ref_pdb_active_recomputed"] == rows_a["input_bound_pdb_u"])
        & (rows_a["input_bound_pdb_u"] != "")
    )
    rows_a["ref_matches_inactive"] = (
        (rows_a["ref_pdb_inactive_recomputed"] == rows_a["input_bound_pdb_u"])
        & (rows_a["input_bound_pdb_u"] != "")
    )

    # ==========================================================
    # (a) Identify the 8 self-reference receptors.
    #
    # A receptor is "self-reference-only" for the 2×2 antag_inactive cell
    # if all its neutral_antagonist rows have ref_pdb_inactive ==
    # input_bound_pdb. Same-crystal antag lookup by construction.
    # ==========================================================
    antag = rows_a[
        rows_a["ligand_role"].isin(["neutral_antagonist", "inverse_agonist"])
    ].copy()
    per_rec_self_ref = antag.groupby("receptor_slug")["ref_matches_inactive"].agg(
        ["mean", "sum", "count"]
    ).reset_index()
    per_rec_self_ref["fully_self_reference"] = per_rec_self_ref["mean"] >= 0.999
    per_rec_self_ref["partially_self_reference"] = (
        (per_rec_self_ref["mean"] > 0) & (per_rec_self_ref["mean"] < 0.999)
    )
    self_ref_receptors = sorted(
        per_rec_self_ref.loc[per_rec_self_ref["fully_self_reference"], "receptor_slug"]
        .str.upper()
        .tolist()
    )

    print(f"[T1-add] identified {len(self_ref_receptors)} fully-self-reference receptors:")
    for r in self_ref_receptors:
        row = per_rec_self_ref[per_rec_self_ref["receptor_slug"].str.upper() == r].iloc[0]
        print(f"    {r:<10} antag_rows={int(row['count'])} self_ref_rows={int(row['sum'])}")

    # 2×2 on those receptors alone. Restrict rows_a to only those receptors.
    rows_self_ref = rows_a[rows_a["receptor_slug"].str.upper().isin(self_ref_receptors)].copy()
    self_ref_records = rows_self_ref.astype(str).to_dict("records")
    print(f"[T1-add-a] 2×2 on n={len(self_ref_receptors)} self-ref receptors ({len(rows_self_ref)} rows)...")
    result_self_ref = stage3a_2x2(self_ref_records)
    result_self_ref_cleanroom = clean_room_2x2_bootstrap(self_ref_records)

    # ==========================================================
    # (b) 2×2 on apo-only ∩ self-reference-excluded.
    # ==========================================================
    rows_apo_clean = rows_a[
        (rows_a["arm"] == "apo")
        & (~rows_a["ref_matches_active"])
        & (~rows_a["ref_matches_inactive"])
    ].copy()
    apo_clean_records = rows_apo_clean.astype(str).to_dict("records")
    print(f"[T1-add-b] 2×2 on apo-only ∩ no-self-ref ({len(rows_apo_clean)} rows)...")
    result_apo_clean = stage3a_2x2(apo_clean_records)
    result_apo_clean_cleanroom = clean_room_2x2_bootstrap(apo_clean_records)

    # ==========================================================
    # Report.
    # ==========================================================
    print()
    print("=" * 78)
    print("(a) 2×2 on self-reference-only receptors")
    print("=" * 78)
    print(f"    receptors ({len(self_ref_receptors)}): {', '.join(self_ref_receptors)}")
    print(f"    n_rows_in_subset: {len(rows_self_ref)}")
    for bb in ("boltz", "chai", "of3", "protenix"):
        d = result_self_ref.get("per_backbone", {}).get(bb, {}).get("interaction", {})
        cr = result_self_ref_cleanroom.get(bb, {})
        print(
            f"    {bb:<10} campaign Δ={d.get('estimate', float('nan')):+.3f} "
            f"CI=[{d.get('ci_lo', float('nan')):+.3f}, {d.get('ci_hi', float('nan')):+.3f}] "
            f"n_common={d.get('n_receptors_in_common', 0)}   "
            f"cleanroom Δ={cr.get('estimate', float('nan')):+.3f} "
            f"CI=[{cr.get('ci_lo', float('nan')):+.3f}, {cr.get('ci_hi', float('nan')):+.3f}]"
        )

    print()
    print("=" * 78)
    print("(b) 2×2 on apo-only ∩ self-reference-excluded")
    print("=" * 78)
    print(f"    n_rows_in_subset: {len(rows_apo_clean)}")
    for bb in ("boltz", "chai", "of3", "protenix"):
        d = result_apo_clean.get("per_backbone", {}).get(bb, {}).get("interaction", {})
        cr = result_apo_clean_cleanroom.get(bb, {})
        print(
            f"    {bb:<10} campaign Δ={d.get('estimate', float('nan')):+.3f} "
            f"CI=[{d.get('ci_lo', float('nan')):+.3f}, {d.get('ci_hi', float('nan')):+.3f}] "
            f"n_common={d.get('n_receptors_in_common', 0)}   "
            f"cleanroom Δ={cr.get('estimate', float('nan')):+.3f} "
            f"CI=[{cr.get('ci_lo', float('nan')):+.3f}, {cr.get('ci_hi', float('nan')):+.3f}]"
        )

    per_rec_records = per_rec_self_ref.to_dict("records")

    report = {
        "task": "T1_addendum_subset_2x2s",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows": {"path": str(ROWS_CSV.relative_to(REPO)), "sha256": sha256_file(ROWS_CSV)},
            "manifest": {"path": str(MANIFEST_CSV.relative_to(REPO)), "sha256": sha256_file(MANIFEST_CSV)},
            "ref_set": {"path": str(REF_SET_CSV.relative_to(REPO)), "sha256": sha256_file(REF_SET_CSV)},
        },
        "self_reference_receptors": self_ref_receptors,
        "per_receptor_self_reference_fraction": per_rec_records,
        "subset_a_self_reference_only": {
            "n_receptors": len(self_ref_receptors),
            "n_rows": int(len(rows_self_ref)),
            "campaign_stage3a": result_self_ref,
            "clean_room": result_self_ref_cleanroom,
        },
        "subset_b_apo_and_no_self_reference": {
            "n_rows": int(len(rows_apo_clean)),
            "campaign_stage3a": result_apo_clean,
            "clean_room": result_apo_clean_cleanroom,
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[T1-add] wrote {Path(args.out).relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
