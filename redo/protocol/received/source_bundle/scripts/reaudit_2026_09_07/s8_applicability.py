#!/usr/bin/env python3
"""S8 — applicability domain (short-cut version).

Reads per-receptor AUROCs directly from the already-computed
``s1_loro_classifier.json`` (variant C_no_selfref_apo × F_iii × 4 backbones)
rather than re-running LORO — the LORO in the parent's S1 output is the
one we need, no re-computation required.

Correlates per-receptor AUROC with:
  - deposition count (RCSB, refs/cache/deposition_counts_by_receptor.json)
  - Block A cognate-vs-apo d_tm6 effect size (from rows.pocket.csv)
  - primary Gα coupling class (refs/gpcr_coupling.csv)
  - ligand chemotype (peptide vs small-mol from refs/ligand_set_tier3.csv)

LORO drop-one-receptor sensitivity + AA2AR leverage flag on each continuous
covariate.

Pre-reg: e63692f.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
S1_JSON = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s1_loro_classifier.json"
OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s8_applicability.json"


def spearman_rho(x: np.ndarray, y: np.ndarray) -> float:
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 5:
        return float("nan")
    xr = pd.Series(x[m]).rank().to_numpy()
    yr = pd.Series(y[m]).rank().to_numpy()
    if np.std(xr) == 0 or np.std(yr) == 0:
        return float("nan")
    return float(np.corrcoef(xr, yr)[0, 1])


def bootstrap_ci(x, y, n_iter=1000, seed=20260907):
    rng = np.random.default_rng(seed)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = np.asarray(x)[m], np.asarray(y)[m]
    if len(x) < 5:
        return (float("nan"), float("nan"), float("nan"))
    n = len(x)
    rho = spearman_rho(x, y)
    reps = np.empty(n_iter)
    for i in range(n_iter):
        idx = rng.integers(0, n, n)
        reps[i] = spearman_rho(x[idx], y[idx])
    reps = reps[np.isfinite(reps)]
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return (rho, float(lo), float(hi))


def main() -> int:
    print("[S8-short] reading per-receptor AUROCs from S1 output...", flush=True)
    s1 = json.loads(S1_JSON.read_text())
    per_receptor_auroc = {}  # {bb: {receptor: auroc}}
    for v in s1.get("variants", []):
        if v.get("variant") == "C_no_selfref_apo" and v.get("feature_set") == "F_iii_pocket_plus_axes":
            per_receptor_auroc[v["backbone"]] = v.get("per_receptor_auroc", {})
    for bb, prs in per_receptor_auroc.items():
        print(f"  {bb:<9} {len(prs)} receptors, pooled context:{'—' if not prs else ''}", flush=True)
        for r, a in sorted(prs.items(), key=lambda x: -x[1])[:3]:
            print(f"    top: {r} {a:.3f}", flush=True)

    # Aggregated (median across 4 backbones) per-receptor AUROC.
    all_recs = sorted(set().union(*[set(per_receptor_auroc[bb].keys()) for bb in per_receptor_auroc]))
    per_rec_summary = {}
    for r in all_recs:
        aus = [per_receptor_auroc[bb][r] for bb in per_receptor_auroc if r in per_receptor_auroc[bb]]
        per_rec_summary[r] = {
            "n_backbones": len(aus),
            "median_auroc": float(np.median(aus)),
            "min_auroc": float(np.min(aus)),
            "max_auroc": float(np.max(aus)),
        }

    # Covariates.
    print("[S8-short] loading covariates...", flush=True)
    depo = json.loads((REPO / "refs/cache/deposition_counts_by_receptor.json").read_text())
    depo = {k.upper(): int(v) for k, v in depo.items()}
    gp = pd.read_csv(REPO / "refs/gpcr_coupling.csv")
    gp["receptor_slug"] = gp["receptor_slug"].str.upper()
    coupling = dict(zip(gp["receptor_slug"], gp["primary_ga_class"]))
    lg = pd.read_csv(REPO / "refs/ligand_set_tier3.csv",
                     on_bad_lines="skip", engine="python")
    lg["receptor"] = lg["receptor"].str.upper()
    lg["is_peptide"] = lg["is_peptide"].astype(str).str.upper().eq("TRUE")
    lg_agonist = lg[lg["ligand_role"] == "full_agonist"]
    chemotype = {row["receptor"]: ("peptide" if row["is_peptide"] else "small_mol")
                 for _, row in lg_agonist.iterrows()}

    # Block A cognate−apo d_tm6 effect.
    print("[S8-short] Block A effect size...", flush=True)
    ba = pd.read_csv(REPO / "experiments/018_block_a_switch_test/analysis/rows.pocket.csv", low_memory=False)
    ba = ba[(ba["receptor_class"].fillna("").astype(str).str.upper() == "A")
            & (ba["passed"].astype(str).str.lower() == "true")]
    ba["receptor_slug"] = ba["receptor_slug"].str.upper()
    ba["d_tm6"] = pd.to_numeric(ba["d_tm6_r350_r630_ca"], errors="coerce")
    ba["input_state_claim"] = ba["input_state_claim"].astype(str)
    ba["arm"] = ba["input_state_claim"].apply(lambda s: "apo" if "apo" in s.lower() else "cognate")
    per_rec_ba = ba.groupby(["receptor_slug", "arm"])["d_tm6"].mean().unstack("arm")
    if "cognate" not in per_rec_ba.columns:
        per_rec_ba["cognate"] = float("nan")
    if "apo" not in per_rec_ba.columns:
        per_rec_ba["apo"] = float("nan")
    per_rec_ba["cognate_minus_apo"] = per_rec_ba["cognate"] - per_rec_ba["apo"]
    block_a_effect = per_rec_ba["cognate_minus_apo"].dropna().to_dict()

    # Correlations.
    covariate_correlations = []
    for bb in ["boltz", "chai", "of3", "protenix"]:
        rec_auroc = per_receptor_auroc.get(bb, {})
        for cov_name, cov_dict in [
            ("deposition_count", depo),
            ("block_a_cognate_minus_apo_effect", block_a_effect),
        ]:
            paired = [(r, cov_dict.get(r), rec_auroc[r]) for r in all_recs
                      if r in cov_dict and r in rec_auroc]
            if len(paired) < 5:
                covariate_correlations.append({
                    "backbone": bb, "covariate": cov_name,
                    "n_pairs": len(paired), "rho": None,
                })
                continue
            rs, xs, ys = zip(*paired)
            xs = np.asarray(xs, dtype=float); ys = np.asarray(ys, dtype=float)
            rho, lo, hi = bootstrap_ci(xs, ys)
            aa_lev = None
            if "AA2AR" in rs:
                m = np.array([r != "AA2AR" for r in rs])
                rho_no_aa = spearman_rho(xs[m], ys[m])
                aa_lev = {"rho_drop_aa2ar": rho_no_aa,
                          "delta_from_full": rho_no_aa - rho,
                          "flag": bool(abs(rho_no_aa - rho) > 0.15)}
            covariate_correlations.append({
                "backbone": bb, "covariate": cov_name,
                "n_pairs": len(paired), "rho": rho, "ci_lo": lo, "ci_hi": hi,
                "ci_clears_zero": bool((lo > 0 and hi > 0) or (lo < 0 and hi < 0)),
                "aa2ar_leverage": aa_lev,
            })
        for cov_name, cov_dict in [
            ("primary_ga_class", coupling),
            ("chemotype", chemotype),
        ]:
            groups = defaultdict(list)
            for r, a in rec_auroc.items():
                g = cov_dict.get(r)
                if g:
                    groups[g].append(a)
            summary = {g: {"n": len(v), "median_auroc": float(np.median(v))} for g, v in groups.items()}
            covariate_correlations.append({
                "backbone": bb, "covariate": cov_name, "type": "categorical",
                "per_group": summary,
            })

    # Applicability domain.
    reliable = [r for r, s in per_rec_summary.items() if s["median_auroc"] >= 0.7]
    unreliable = [r for r, s in per_rec_summary.items() if s["median_auroc"] < 0.7]
    reliable_sorted = sorted(reliable, key=lambda x: -per_rec_summary[x]["median_auroc"])
    unreliable_sorted = sorted(unreliable, key=lambda x: -per_rec_summary[x]["median_auroc"])

    applicability = {
        "reliable_receptors_median_auroc_gte_07": reliable_sorted,
        "unreliable_receptors_median_auroc_lt_07": unreliable_sorted,
        "n_reliable": len(reliable),
        "n_unreliable": len(unreliable),
        "domain_statement": (
            f"The apo × F_iii × logreg readout is reliable "
            f"(median per-backbone AUROC ≥ 0.70) on {len(reliable)} of "
            f"{len(per_rec_summary)} evaluated receptors. Unreliable "
            f"({len(unreliable)}): {', '.join(unreliable_sorted)}."
        ),
    }

    payload = {
        "task": "S8_applicability_domain_shortcut",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "prereg_git_sha": "e63692f",
        "source_s1_json": str(S1_JSON.relative_to(REPO)),
        "per_receptor_auroc_per_backbone": per_receptor_auroc,
        "per_receptor_summary": per_rec_summary,
        "covariate_correlations": covariate_correlations,
        "applicability": applicability,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, default=str))
    print(f"[S8-short] wrote {OUT.relative_to(REPO)}", flush=True)
    print()
    print("=" * 78)
    print("S8 — per-receptor median AUROC (sorted)")
    print("=" * 78)
    for r in sorted(per_rec_summary.keys(), key=lambda x: -per_rec_summary[x]["median_auroc"]):
        s = per_rec_summary[r]
        print(f"  {r:<10} median={s['median_auroc']:.3f} range=[{s['min_auroc']:.3f}, {s['max_auroc']:.3f}] n_bb={s['n_backbones']}")
    print()
    print("Continuous covariate correlations:")
    for c in covariate_correlations:
        if c.get("type") == "categorical": continue
        if c.get("rho") is None: continue
        aa = c.get("aa2ar_leverage") or {}
        print(f"  {c['backbone']:<9} {c['covariate']:<40} ρ={c['rho']:+.3f} CI=[{c['ci_lo']:+.3f},{c['ci_hi']:+.3f}] "
              f"clears0={c['ci_clears_zero']} aa2ar_delta={aa.get('delta_from_full','NA'):+.3f}"
              if isinstance(aa.get('delta_from_full'), float) else f"  {c['backbone']:<9} {c['covariate']:<40} ρ={c['rho']:+.3f}")
    print()
    print("Categorical group medians:")
    for c in covariate_correlations:
        if c.get("type") != "categorical": continue
        print(f"  {c['backbone']:<9} {c['covariate']}: "
              + "; ".join([f"{g}: n={x['n']}, med={x['median_auroc']:.3f}" for g, x in c["per_group"].items()]))
    print()
    print(applicability["domain_statement"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
