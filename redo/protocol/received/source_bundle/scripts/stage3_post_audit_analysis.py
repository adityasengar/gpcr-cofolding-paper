#!/usr/bin/env python3
"""Block C Post-Audit Stage 3 — dual-ref pocket-metric analyses.

Consumes ``rows.tier3.v2.csv`` (Stage 2 output) + reference-set metadata
+ RCSB deposition dates. Emits four verification JSONs:

  1. stage3_2x2_ligand_state_specificity.json
     — per-backbone 2×2 mean±CI table + interaction term
  2. stage3_training_cutoff_stratification.json
     — pocket contrasts stratified by pre/post training cutoff
  3. stage3_effect_size_vs_deposition_count.json
     — per-receptor effect size regressed on log10(n deposited)
  4. stage3_sensitivity_flagged_receptors.json
     — recompute 3a with LPAR1 / 5HT1B / AA1R excluded

Cluster-bootstrap CIs use the receptor as the resampling unit
(5,000 iterations by default). Post-cutoff strata with n < 5 per cell
are marked ``UNDERPOWERED`` rather than reported as nulls per the
task spec.

Backbone training cutoffs (Post-Audit research 2026-09-05):

    Boltz-2:  2023-06-01  (Boltz-2 preprint Methods)
    Chai-1:   2021-01-12  (Chai-1 preprint)
    OF3:      2021-09-30  (OF3-preview technical report, inherits AF3)
    Protenix: 2021-09-30  (Protenix v2 README)
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import random
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence


REPO = Path(__file__).resolve().parent.parent


BACKBONE_TRAINING_CUTOFFS: dict[str, str] = {
    "boltz": "2023-06-01",
    "chai": "2021-01-12",
    "of3": "2021-09-30",
    "openfold3": "2021-09-30",
    "protenix": "2021-09-30",
}
BACKBONE_CUTOFF_CITATIONS: dict[str, str] = {
    "boltz": (
        "Passaro et al., bioRxiv 2025.06.14.659707 v1 Methods — "
        "\"release date cutoff of 06/01/2023\" for training-set clusters."
    ),
    "chai": (
        "Chai Discovery Chai-1 tech report v1, bioRxiv 2024.10.10.615955 "
        "— \"release date cutoff of 2021-01-12\"."
    ),
    "of3": (
        "OpenFold-3-preview technical report of3p1 — "
        "\"Date cutoffs for structural training sets were the same as "
        "AF3\" = 2021-09-30 (AlphaFold 3 Nature SI)."
    ),
    "protenix": (
        "Protenix v2 (ByteDance) README model table — "
        "\"Training Data Cutoff: 2021-09-30\", aligned with AF3."
    ),
}


# ---------------------------------------------------------------------------
# Data loading + normalisation
# ---------------------------------------------------------------------------


def _sha256(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return "unknown"


def _to_float(x: str) -> float:
    if x is None or x == "" or str(x).lower() in ("nan", "none"):
        return float("nan")
    try:
        return float(x)
    except ValueError:
        return float("nan")


def _load_rows(path, manifest_path=None) -> list[dict[str, str]]:
    """Load scorer rows. If ``manifest_path`` is provided, join in
    ``backbone`` / ``partner_type`` / ``ligand_role`` columns from the
    rescore manifest (keyed on prediction_path == input_path). The
    scorer's ScorerRow schema does NOT carry backbone or partner_type
    — they live only on the manifest side, and the analysis needs
    them to stratify."""
    with Path(path).open() as f:
        rows = list(csv.DictReader(f))
    if not manifest_path:
        return rows
    m_by_path: dict[str, dict] = {}
    with Path(manifest_path).open() as f:
        for r in csv.DictReader(f):
            m_by_path[r["prediction_path"]] = r
    # Join columns we need for analysis. `ligand_role` on the scorer
    # row is authoritative post-fix; take backbone + partner_type from
    # the manifest only.
    for row in rows:
        m = m_by_path.get(row.get("input_path", ""))
        if m is None:
            continue
        row.setdefault("backbone", m.get("backbone", ""))
        row.setdefault("partner_type", m.get("partner_type", ""))
        if not row.get("ligand_role"):
            row["ligand_role"] = m.get("ligand_role", "")
    return rows


def _load_ref_set(path) -> dict[str, dict[str, list[dict]]]:
    """Returns {receptor_upper: {"active": [rows], "inactive": [rows]}}"""
    out: dict[str, dict[str, list[dict]]] = {}
    with Path(path).open() as f:
        for row in csv.DictReader(f):
            recep = (row.get("receptor_slug") or "").strip().upper()
            role = (row.get("role") or "").strip().lower()
            if not recep or role not in ("active", "inactive"):
                continue
            out.setdefault(recep, {"active": [], "inactive": []})
            out[recep][role].append(row)
    return out


# ---------------------------------------------------------------------------
# Cluster bootstrap
# ---------------------------------------------------------------------------


def _mean(xs: Sequence[float]) -> float:
    xs2 = [x for x in xs if not math.isnan(x)]
    return statistics.fmean(xs2) if xs2 else float("nan")


def _cluster_bootstrap_ci(
    values_by_cluster: dict[str, list[float]],
    reducer,
    n_iter: int = 5000,
    seed: int = 42,
    ci_lo: float = 0.025,
    ci_hi: float = 0.975,
) -> dict[str, float]:
    """Return {"est": point_estimate, "ci_lo": ..., "ci_hi": ...}."""
    clusters = list(values_by_cluster.keys())
    if not clusters:
        return {"est": float("nan"), "ci_lo": float("nan"),
                "ci_hi": float("nan"), "n_clusters": 0}
    rng = random.Random(seed)
    # Point estimate: pool across clusters uniformly.
    flat = [v for c in clusters for v in values_by_cluster[c]]
    point = reducer(flat)
    reps: list[float] = []
    n_c = len(clusters)
    for _ in range(n_iter):
        sample = [rng.choice(clusters) for _ in range(n_c)]
        pool = [v for c in sample for v in values_by_cluster[c]]
        try:
            reps.append(reducer(pool))
        except Exception:
            continue
    reps_sorted = sorted(x for x in reps if not math.isnan(x))
    if not reps_sorted:
        return {"est": point, "ci_lo": float("nan"),
                "ci_hi": float("nan"), "n_clusters": n_c}
    lo = reps_sorted[max(0, int(len(reps_sorted) * ci_lo) - 1)]
    hi = reps_sorted[min(len(reps_sorted) - 1, int(len(reps_sorted) * ci_hi))]
    return {"est": point, "ci_lo": lo, "ci_hi": hi, "n_clusters": n_c}


# ---------------------------------------------------------------------------
# 3a — 2×2 ligand-state-specificity
# ---------------------------------------------------------------------------


def stage3a_2x2(
    rows: list[dict[str, str]],
    excluded_receptors: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    """For each backbone, compute:
      pocket_active_rmsd on agonist / antagonist arms
      pocket_inactive_rmsd on agonist / antagonist arms
    and the interaction term
      (agonist - antag on active) - (agonist - antag on inactive)

    An arm's "role" is derived from ligand_role:
      - agonist arm:    ligand_role == "full_agonist"
      - antag arm:      ligand_role in {"neutral_antagonist", "inverse_agonist"}

    Passing rows only. Cluster-bootstrap CI at receptor level.
    """
    by_backbone: dict[str, dict] = {}
    backbones = sorted({
        (r.get("backbone") or "").lower() for r in rows if r.get("backbone")
    })
    for bb in backbones:
        agonist_active: dict[str, list[float]] = {}
        agonist_inactive: dict[str, list[float]] = {}
        antag_active: dict[str, list[float]] = {}
        antag_inactive: dict[str, list[float]] = {}
        for r in rows:
            if (r.get("backbone") or "").lower() != bb:
                continue
            if str(r.get("passed", "")).lower() != "true":
                continue
            recep = (r.get("receptor_slug") or "").upper()
            if recep in excluded_receptors:
                continue
            if (r.get("receptor_class") or "").upper() != "A":
                continue  # pocket metrics are class A only
            role = (r.get("ligand_role") or "").strip()
            v_a = _to_float(r.get("pocket_ca_rmsd_active") or "")
            v_i = _to_float(r.get("pocket_ca_rmsd_inactive") or "")
            if math.isnan(v_a) or math.isnan(v_i):
                continue
            if role == "full_agonist":
                agonist_active.setdefault(recep, []).append(v_a)
                agonist_inactive.setdefault(recep, []).append(v_i)
            elif role in ("neutral_antagonist", "inverse_agonist"):
                antag_active.setdefault(recep, []).append(v_a)
                antag_inactive.setdefault(recep, []).append(v_i)

        def _reducer_mean(xs):
            return _mean(xs)

        def _interaction_reducer(_ignored, bins=(agonist_active,
                                                 antag_active,
                                                 agonist_inactive,
                                                 antag_inactive)):
            return None  # unused — we compute the interaction on cluster-mean means

        # Simple 4-cell means + interaction on pooled means.
        cell_stats: dict[str, dict] = {
            "agonist_active": _cluster_bootstrap_ci(agonist_active, _reducer_mean),
            "agonist_inactive": _cluster_bootstrap_ci(agonist_inactive, _reducer_mean),
            "antag_active": _cluster_bootstrap_ci(antag_active, _reducer_mean),
            "antag_inactive": _cluster_bootstrap_ci(antag_inactive, _reducer_mean),
        }

        # Interaction bootstrap — resample receptors and compute
        # (agonist - antag)_active - (agonist - antag)_inactive.
        common_receptors = (
            set(agonist_active) & set(antag_active)
            & set(agonist_inactive) & set(antag_inactive)
        )
        rng = random.Random(1234)
        n_iter = 5000
        reps = []
        common_list = sorted(common_receptors)
        for _ in range(n_iter):
            sample = [rng.choice(common_list) for _ in range(len(common_list))] \
                if common_list else []
            if not sample:
                continue
            ag_a = _mean([v for c in sample for v in agonist_active[c]])
            ag_i = _mean([v for c in sample for v in agonist_inactive[c]])
            an_a = _mean([v for c in sample for v in antag_active[c]])
            an_i = _mean([v for c in sample for v in antag_inactive[c]])
            if any(math.isnan(x) for x in (ag_a, ag_i, an_a, an_i)):
                continue
            interaction = (ag_a - an_a) - (ag_i - an_i)
            reps.append(interaction)
        reps_sorted = sorted(reps)
        if reps_sorted:
            # Point estimate: pool per-receptor cell means, not per-row.
            ag_a = _mean([v for c in common_list for v in agonist_active[c]])
            ag_i = _mean([v for c in common_list for v in agonist_inactive[c]])
            an_a = _mean([v for c in common_list for v in antag_active[c]])
            an_i = _mean([v for c in common_list for v in antag_inactive[c]])
            pt = (ag_a - an_a) - (ag_i - an_i)
            lo = reps_sorted[max(0, int(len(reps_sorted) * 0.025) - 1)]
            hi = reps_sorted[
                min(len(reps_sorted) - 1, int(len(reps_sorted) * 0.975))
            ]
        else:
            pt = float("nan"); lo = float("nan"); hi = float("nan")

        by_backbone[bb] = {
            "cells": cell_stats,
            "interaction": {
                "estimate": pt,
                "ci_lo": lo,
                "ci_hi": hi,
                "n_receptors_in_common": len(common_receptors),
                "signed_nonzero": (
                    (lo > 0 and hi > 0) or (lo < 0 and hi < 0)
                    if not (math.isnan(lo) or math.isnan(hi))
                    else False
                ),
                "interpretation": (
                    "signed non-zero interaction — ligand-state-specific "
                    "pocket geometry" if not (math.isnan(lo) or math.isnan(hi))
                    and ((lo > 0 and hi > 0) or (lo < 0 and hi < 0))
                    else "null interaction OR insufficient data"
                ),
            },
            "n_rows": {
                "agonist_active": sum(len(v) for v in agonist_active.values()),
                "agonist_inactive": sum(len(v) for v in agonist_inactive.values()),
                "antag_active": sum(len(v) for v in antag_active.values()),
                "antag_inactive": sum(len(v) for v in antag_inactive.values()),
            },
            "n_receptors": {
                "agonist": len(agonist_active),
                "antag": len(antag_active),
                "common": len(common_receptors),
            },
        }
    return {"per_backbone": by_backbone}


# ---------------------------------------------------------------------------
# 3b — training-cutoff stratification
# ---------------------------------------------------------------------------


def _receptor_ref_dates(
    ref_set: dict, deposit_dates: dict[str, dict]
) -> dict[str, dict[str, str]]:
    """For each receptor return {"active_date": ..., "inactive_date": ...}
    using the earliest active + earliest inactive PDB (deposit date).
    """
    out: dict[str, dict[str, str]] = {}
    for recep, rows_by_role in ref_set.items():
        earliest_active = None
        earliest_inactive = None
        for r in rows_by_role.get("active", []):
            pdb = (r.get("pdb_id") or "").strip().upper()
            info = deposit_dates.get(pdb)
            if not info or info.get("status_code") != 200:
                continue
            date = info.get("deposit_date", "")
            if date:
                if earliest_active is None or date < earliest_active:
                    earliest_active = date
        for r in rows_by_role.get("inactive", []):
            pdb = (r.get("pdb_id") or "").strip().upper()
            info = deposit_dates.get(pdb)
            if not info or info.get("status_code") != 200:
                continue
            date = info.get("deposit_date", "")
            if date:
                if earliest_inactive is None or date < earliest_inactive:
                    earliest_inactive = date
        out[recep] = {
            "active_date": earliest_active or "",
            "inactive_date": earliest_inactive or "",
        }
    return out


def stage3b_training_cutoff(
    rows: list[dict[str, str]],
    ref_set: dict,
    deposit_dates: dict[str, dict],
) -> dict[str, Any]:
    """Recompute agonist − decoy (apo arm) and agonist − antag (cognate arm)
    pocket contrasts on ``pocket_ca_rmsd_active`` and
    ``pocket_ca_rmsd_inactive``, stratified by whether the receptor's
    reference PDB was pre- or post-cutoff for the backbone."""
    per_receptor_dates = _receptor_ref_dates(ref_set, deposit_dates)

    def _relevant_date(bb: str, recep: str) -> str:
        # Use the EARLIER of active/inactive as "any reference deposited
        # for this receptor". If EITHER was in the training window,
        # memorization can leak.
        info = per_receptor_dates.get(recep, {})
        a = info.get("active_date", "")
        i = info.get("inactive_date", "")
        if a and i:
            return min(a, i)
        return a or i

    out: dict[str, Any] = {
        "backbone_cutoffs": BACKBONE_TRAINING_CUTOFFS,
        "backbone_cutoff_citations": BACKBONE_CUTOFF_CITATIONS,
        "per_backbone": {},
    }
    backbones = sorted({(r.get("backbone") or "").lower() for r in rows
                        if r.get("backbone")})

    for bb in backbones:
        cutoff = BACKBONE_TRAINING_CUTOFFS.get(bb)
        if cutoff is None:
            continue
        # Stratify each metric+arm cell.
        strata = ("pre_cutoff", "post_cutoff")
        arms_metrics = [
            # (arm_label, ligand_role_agonist_A, ligand_role_agonist_B, metric_col)
            ("agonist_minus_decoy_apo_active",
             "full_agonist", "decoy_lig", "pocket_ca_rmsd_active",
             "apo"),
            ("agonist_minus_decoy_apo_inactive",
             "full_agonist", "decoy_lig", "pocket_ca_rmsd_inactive",
             "apo"),
            ("agonist_minus_antag_cognate_active",
             "full_agonist", "antag", "pocket_ca_rmsd_active",
             "cognate"),
            ("agonist_minus_antag_cognate_inactive",
             "full_agonist", "antag", "pocket_ca_rmsd_inactive",
             "cognate"),
            # sidechain versions
            ("agonist_minus_decoy_apo_active_sc",
             "full_agonist", "decoy_lig", "pocket_sidechain_rmsd_active",
             "apo"),
            ("agonist_minus_antag_cognate_active_sc",
             "full_agonist", "antag", "pocket_sidechain_rmsd_active",
             "cognate"),
        ]
        cell_stats: dict[str, dict] = {}

        for arm_label, role_a, role_b, metric_col, partner in arms_metrics:
            per_stratum: dict[str, dict[str, list[float]]] = {
                "pre_cutoff": {"a": {}, "b": {}},
                "post_cutoff": {"a": {}, "b": {}},
            }
            for r in rows:
                if (r.get("backbone") or "").lower() != bb:
                    continue
                if str(r.get("passed", "")).lower() != "true":
                    continue
                if (r.get("receptor_class") or "").upper() != "A":
                    continue
                # `partner` values in the manifest: "g_alpha"
                # (cognate arm) / "apo" (apo arm). Normalise the
                # legacy analysis label "cognate" → "g_alpha".
                pt = (r.get("partner_type") or "").lower()
                want = "g_alpha" if partner == "cognate" else partner
                if pt != want:
                    continue
                recep = (r.get("receptor_slug") or "").upper()
                date = _relevant_date(bb, recep)
                if not date:
                    continue
                stratum = "pre_cutoff" if date <= cutoff else "post_cutoff"
                v = _to_float(r.get(metric_col) or "")
                if math.isnan(v):
                    continue
                lrole = (r.get("ligand_role") or "").strip()
                if role_a == lrole:
                    per_stratum[stratum]["a"].setdefault(recep, []).append(v)
                elif role_b == "antag" and lrole in (
                    "neutral_antagonist", "inverse_agonist"
                ):
                    per_stratum[stratum]["b"].setdefault(recep, []).append(v)
                elif role_b == lrole:
                    per_stratum[stratum]["b"].setdefault(recep, []).append(v)

            arm_stats = {}
            for stratum in strata:
                a_by_r = per_stratum[stratum]["a"]
                b_by_r = per_stratum[stratum]["b"]
                common = sorted(set(a_by_r) & set(b_by_r))
                n_a = sum(len(v) for v in a_by_r.values())
                n_b = sum(len(v) for v in b_by_r.values())
                if n_a < 5 or n_b < 5 or len(common) < 2:
                    arm_stats[stratum] = {
                        "status": "UNDERPOWERED",
                        "n_a": n_a,
                        "n_b": n_b,
                        "n_receptors_common": len(common),
                    }
                    continue
                rng = random.Random(hash((bb, arm_label, stratum)) & 0xffff)
                reps = []
                for _ in range(5000):
                    sample = [rng.choice(common) for _ in range(len(common))]
                    mean_a = _mean([v for c in sample for v in a_by_r[c]])
                    mean_b = _mean([v for c in sample for v in b_by_r[c]])
                    if math.isnan(mean_a) or math.isnan(mean_b):
                        continue
                    reps.append(mean_a - mean_b)
                reps_sorted = sorted(reps)
                pt = (
                    _mean([v for c in common for v in a_by_r[c]])
                    - _mean([v for c in common for v in b_by_r[c]])
                )
                lo = reps_sorted[max(0, int(len(reps_sorted) * 0.025) - 1)] \
                    if reps_sorted else float("nan")
                hi = reps_sorted[
                    min(len(reps_sorted) - 1, int(len(reps_sorted) * 0.975))
                ] if reps_sorted else float("nan")
                signed_nonzero = (
                    not (math.isnan(lo) or math.isnan(hi))
                    and ((lo > 0 and hi > 0) or (lo < 0 and hi < 0))
                )
                arm_stats[stratum] = {
                    "status": "ok",
                    "estimate": pt, "ci_lo": lo, "ci_hi": hi,
                    "n_a": n_a, "n_b": n_b,
                    "n_receptors_common": len(common),
                    "signed_nonzero": signed_nonzero,
                }
            cell_stats[arm_label] = arm_stats

        # Verdict per backbone — did the primary pocket contrast survive
        # the post-cutoff filter?
        primary = cell_stats.get("agonist_minus_antag_cognate_active", {})
        pre = primary.get("pre_cutoff", {})
        post = primary.get("post_cutoff", {})
        if post.get("status") == "ok" and post.get("signed_nonzero"):
            verdict = "SURVIVES_POST_CUTOFF"
        elif post.get("status") == "UNDERPOWERED":
            verdict = "UNDERPOWERED"
        elif pre.get("status") == "ok" and pre.get("signed_nonzero"):
            verdict = "PRE_CUTOFF_ONLY"
        else:
            verdict = "NO_SIGNAL_IN_EITHER_STRATUM"

        out["per_backbone"][bb] = {
            "training_cutoff": cutoff,
            "verdict": verdict,
            "cells": cell_stats,
        }

    out["per_receptor_reference_dates"] = per_receptor_dates
    return out


# ---------------------------------------------------------------------------
# 3c — effect size × deposition count
# ---------------------------------------------------------------------------


def stage3c_effect_size_vs_deposition(
    rows: list[dict[str, str]],
    deposition_counts: dict[str, int],
) -> dict[str, Any]:
    """Per receptor, per backbone: compute the pocket_ca_rmsd_active
    effect size (agonist − antag) and regress against
    ``log10(n_deposited_pdbs_for_this_receptor)``.

    Memorization prediction: positive Pearson correlation (more entries
    seen → larger contrast). Physics prediction: null.

    ``deposition_counts`` — {receptor_upper: int}. Missing keys are
    excluded from the regression."""
    per_backbone: dict[str, dict] = {}
    backbones = sorted({(r.get("backbone") or "").lower() for r in rows
                        if r.get("backbone")})
    for bb in backbones:
        # gather per receptor
        ag: dict[str, list[float]] = {}
        an: dict[str, list[float]] = {}
        for r in rows:
            if (r.get("backbone") or "").lower() != bb:
                continue
            if str(r.get("passed", "")).lower() != "true":
                continue
            if (r.get("receptor_class") or "").upper() != "A":
                continue
            # cognate arm surfaces as partner_type == "g_alpha" in the
            # Tier 3 manifest — treat both labels as equivalent.
            pt = (r.get("partner_type") or "").lower()
            if pt not in ("cognate", "g_alpha"):
                continue
            recep = (r.get("receptor_slug") or "").upper()
            v = _to_float(r.get("pocket_ca_rmsd_active") or "")
            if math.isnan(v):
                continue
            lrole = (r.get("ligand_role") or "").strip()
            if lrole == "full_agonist":
                ag.setdefault(recep, []).append(v)
            elif lrole in ("neutral_antagonist", "inverse_agonist"):
                an.setdefault(recep, []).append(v)
        pairs = []
        for recep in sorted(set(ag) & set(an)):
            eff = _mean(ag[recep]) - _mean(an[recep])
            n_dep = deposition_counts.get(recep)
            if n_dep is None or n_dep <= 0:
                continue
            pairs.append((recep, math.log10(n_dep), eff))
        # Pearson r on pairs
        n = len(pairs)
        if n < 4:
            per_backbone[bb] = {"n": n, "status": "insufficient_receptors"}
            continue
        xs = [p[1] for p in pairs]
        ys = [p[2] for p in pairs]
        mx = _mean(xs); my = _mean(ys)
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        den = math.sqrt(
            sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)
        )
        r = num / den if den > 0 else float("nan")
        # Two-tailed p from the t = r sqrt(n-2)/sqrt(1-r^2) distribution —
        # approximated via a normal cdf for reporting only.
        if not math.isnan(r) and abs(r) < 1.0:
            t = r * math.sqrt(n - 2) / math.sqrt(max(1 - r * r, 1e-9))
            # 2-sided normal-approx p
            p = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t) / math.sqrt(2.0))))
        else:
            p = float("nan")
        per_backbone[bb] = {
            "n_receptors": n,
            "pearson_r": r,
            "p_two_tailed_normal_approx": p,
            "pairs": [{"receptor": p_[0], "log10_n_deposited": p_[1],
                       "effect_size": p_[2]} for p_ in pairs],
        }
    return {
        "deposition_counts": deposition_counts,
        "per_backbone": per_backbone,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rows", type=Path, required=True,
                   help="rows.tier3.v2.csv path")
    p.add_argument("--manifest", type=Path,
                   default=REPO / "experiments"
                   / "021_block_c_tier3_pharmacology"
                   / "analysis" / "rescore_manifest.tier3.v2.csv",
                   help="rescore manifest (for backbone/partner_type "
                        "join). Optional but recommended.")
    p.add_argument("--ref-set", type=Path,
                   default=REPO / "refs" / "reference_set.csv")
    p.add_argument("--rcsb-dates", type=Path,
                   default=REPO / "refs" / "cache" / "rcsb_deposit_dates.json")
    p.add_argument("--deposition-counts", type=Path,
                   help="JSON {receptor: n_deposited}. Optional; when "
                        "absent, stage 3c uses n(active_refs) + "
                        "n(inactive_refs) from reference_set.csv as a "
                        "conservative proxy.")
    p.add_argument("--out-dir", type=Path, required=True,
                   help="Verification dir for the four JSONs")
    p.add_argument("--stage", choices=["all", "3a", "3b", "3c", "3d"],
                   default="all")
    args = p.parse_args(argv)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows = _load_rows(args.rows, manifest_path=args.manifest)
    ref_set = _load_ref_set(args.ref_set)
    dep_dates_raw = json.loads(args.rcsb_dates.read_text())
    dep_dates = dep_dates_raw.get("per_pdb", {})

    # Deposition counts — prefer explicit JSON; fall back to reference_set count.
    if args.deposition_counts and args.deposition_counts.exists():
        dep_counts_raw = json.loads(args.deposition_counts.read_text())
        dep_counts = {
            r.upper(): int(n) for r, n in dep_counts_raw.items()
        }
    else:
        dep_counts = {
            recep: len(rows_by_role.get("active", [])) + len(
                rows_by_role.get("inactive", [])
            )
            for recep, rows_by_role in ref_set.items()
        }

    reconstruction_meta = {
        "reconstruction_script": __file__,
        "reconstruction_script_git_sha": _git_sha(),
        "rows_csv": str(args.rows.resolve()),
        "rows_csv_sha256": _sha256(args.rows),
        "ref_set_csv": str(args.ref_set.resolve()),
        "ref_set_csv_sha256": _sha256(args.ref_set),
        "rcsb_deposit_dates_json": str(args.rcsb_dates.resolve()),
        "rcsb_deposit_dates_sha256": _sha256(args.rcsb_dates),
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(
            timespec="seconds"
        ),
    }

    if args.stage in ("all", "3a"):
        r3a = {"reconstruction": reconstruction_meta, **stage3a_2x2(rows)}
        (args.out_dir / "stage3_2x2_ligand_state_specificity.json").write_text(
            json.dumps(r3a, indent=2, default=str) + "\n"
        )
    if args.stage in ("all", "3b"):
        r3b = {"reconstruction": reconstruction_meta,
               **stage3b_training_cutoff(rows, ref_set, dep_dates)}
        (args.out_dir / "stage3_training_cutoff_stratification.json").write_text(
            json.dumps(r3b, indent=2, default=str) + "\n"
        )
    if args.stage in ("all", "3c"):
        r3c = {"reconstruction": reconstruction_meta,
               **stage3c_effect_size_vs_deposition(rows, dep_counts)}
        (args.out_dir / "stage3_effect_size_vs_deposition_count.json").write_text(
            json.dumps(r3c, indent=2, default=str) + "\n"
        )
    if args.stage in ("all", "3d"):
        excluded = frozenset({"LPAR1", "5HT1B", "AA1R"})
        r3d_full = stage3a_2x2(rows)
        r3d_excl = stage3a_2x2(rows, excluded_receptors=excluded)
        r3d = {
            "reconstruction": reconstruction_meta,
            "excluded_receptors": sorted(excluded),
            "rationale": (
                "LPAR1: unsourced SMILES with no C9 stereo. 5HT1B, AA1R: "
                "antag SMILES PubChem-sourced not CCD. LPAR1 was one of "
                "OF3's non-zero P5 receptors (+0.20) on the earlier binary "
                "predicate — worth knowing whether its OF3 pocket effect "
                "survives inactive-ref rescore + exclusion."
            ),
            "full_panel": r3d_full,
            "flagged_excluded": r3d_excl,
        }
        (args.out_dir / "stage3_sensitivity_flagged_receptors.json").write_text(
            json.dumps(r3d, indent=2, default=str) + "\n"
        )
    print("Stage 3 analysis complete:", args.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
