#!/usr/bin/env python3
"""P7 — does model confidence separate correct from incorrect state calls?

The pre-registered null in `paper_af3`'s own analysis
(`analyse_block_c_tier1_headline.py:383-386`) reads:

    verdicts["P7"] = {"status": "descriptive_placeholder",
                      "note": "requires per-row pLDDT column; deferred to analysis-time"}

It was never computed, anywhere, in any block. It is the paper's THIRD TITLE
CLAUSE — "model confidence does not track state correctness" — and it is free on
Block A's 9,490 delivered rows.

WHY IT IS COMPUTABLE HERE AND NOT IN THE SCORER. `switch_signal.py`'s row
classifier returns "inactive" whenever `confidence_flag == "low"`, before any
geometry is read, which makes the state call non-independent of confidence by
construction (finding F-2). Block A's shipped `active` column does NOT carry that
gate — 47 rows with `min_plddt_at_anchor < 50` are `active=True` — so on this data
the two are independent and the question is answerable.

THE DISTINCTION THAT IS THE WHOLE POINT. Pooled across receptors, confidence
separates correct from incorrect — but that can be an artefact of some receptors
being uniformly easy and well-predicted. The honest test is WITHIN receptor: given
one receptor, does confidence tell you which of ITS predictions got the state
right? Those are different claims and a pooled AUC silently merges them.

GROUND TRUTH is structural, not the predicate's own output: a prediction is
"really active" iff it is closer to the active reference than the inactive one.

EXCLUSIONS. E1 and E2 apply everywhere (29 rows). E3 is NOT applied: our own
`analysis/block_a/METHODS_DRAFT.md:115-117` records that "E3 is irrelevant to raw
distributions, predicate firing rates and confidence correlations, which never
touch a reference separation." Never `excl_any` — it removes 54% of the block.

    python3 redo/build/p7_confidence_separation.py
"""

import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, repo

ROWS = repo("data", "block_a", "01_rows", "block_a_rows.csv")
CLUS = repo("data", "block_a", "07_clusters_and_holdout", "cluster_map.csv")
OUT_CSV = os.path.join(INPUTS, "p7_confidence_separation.csv")
OUT_JSON = os.path.join(INPUTS, "p7_confidence_separation.json")

CONF = ["plddt_mean", "min_plddt_at_anchor", "plddt_at_anchors"]
BOOT = 10_000
MIN_ERR = 10   # a receptor needs >=10 wrong AND >=10 correct to carry an AUC
SEED = 20260912


def auc(scores, labels):
    """Mann-Whitney AUC with tie-corrected ranks. nan unless both classes present.

    Pure numpy: this runs inside a 10,000-iteration bootstrap, and a pandas
    groupby here made the whole analysis take over half an hour.
    """
    s = np.asarray(scores, float)
    y = np.asarray(labels, bool)
    ok = ~np.isnan(s)
    s, y = s[ok], y[ok]
    n1 = int(y.sum()); n0 = int(len(y) - n1)
    if n1 == 0 or n0 == 0 or len(s) < 2:
        return np.nan
    order = np.argsort(s, kind="mergesort")
    ss = s[order]
    ranks = np.empty(len(s), float)
    ranks[order] = np.arange(1, len(s) + 1)
    # average ranks within tied runs, or ties inflate the statistic
    i = 0
    while i < len(ss):
        j = i + 1
        while j < len(ss) and ss[j] == ss[i]:
            j += 1
        if j - i > 1:
            ranks[order[i:j]] = (i + 1 + j) / 2.0
        i = j
    return (ranks[y].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def cluster_boot_auc(vals, lab, cid, rng, n=BOOT):
    """Cluster bootstrap of an AUC, resampling INDEX BLOCKS not dataframes.

    The statistical unit on this project is the paralog CLUSTER: paralogs inside
    one cluster are not independent observations of the same question, so a row
    or receptor bootstrap understates the interval.
    """
    blocks = [np.flatnonzero(cid == c) for c in np.unique(cid)]
    k = len(blocks)
    out = np.empty(n)
    for b in range(n):
        pick = rng.integers(0, k, k)
        idx = np.concatenate([blocks[i] for i in pick])
        out[b] = auc(vals[idx], lab[idx])
    out = out[~np.isnan(out)]
    return (np.nan, np.nan) if out.size == 0 else tuple(np.percentile(out, [2.5, 97.5]))


def cluster_boot_mean(vals, cid, rng, n=BOOT):
    """Cluster bootstrap of a simple mean (used for the within-receptor AUCs)."""
    blocks = [np.flatnonzero(cid == c) for c in np.unique(cid)]
    k = len(blocks)
    out = np.empty(n)
    for b in range(n):
        pick = rng.integers(0, k, k)
        idx = np.concatenate([blocks[i] for i in pick])
        out[b] = np.nanmean(vals[idx])
    out = out[~np.isnan(out)]
    return (np.nan, np.nan) if out.size == 0 else tuple(np.percentile(out, [2.5, 97.5]))


def main():
    d = pd.read_csv(ROWS, low_memory=False)
    cl = pd.read_csv(CLUS)[["receptor", "cluster_id"]]
    d = d.merge(cl, on="receptor", how="left")

    # E1 + E2 only. Never excl_any.
    keep = ~((d.get("excl_E1") == True) | (d.get("excl_E2") == True))
    d = d[keep]

    d = d[d.rmsd_to_active_ref.notna() & d.rmsd_to_inactive_ref.notna() & d.active.notna()]
    d = d[d.cluster_id.notna()]

    d["truth_active"] = d.rmsd_to_active_ref < d.rmsd_to_inactive_ref
    d["correct"] = d.active.astype(bool) == d.truth_active

    # SENSITIVITY ARM, added 2026-09-12 after finding F-10's mechanical-error
    # trace. Class A's rule is `npxxy AND tilt`, so a receptor with NO NPxxY axis
    # has NaN propagate to False and is called inactive on EVERY row regardless of
    # geometry. EDNRB and GRPR are those receptors: 400 rows, zero called active,
    # 43% of them truly active, and together 28% of the campaign's entire error
    # budget from 5% of its rows.
    #
    # Those rows cannot answer "does confidence separate correct from incorrect
    # calls", because no call was made from the geometry -- so including them risks
    # measuring "does confidence predict being an unevaluable receptor" instead.
    # Reported BOTH ways: excluding them is the honest primary, and the difference
    # is itself the finding.
    d["forced_inactive"] = (d.gpcr_class == "A") & d.d_npxxy_oh.isna()

    rng = np.random.default_rng(SEED)
    rows, summary = [], {}
    d_all = d
    d = d[~d.forced_inactive]        # primary analysis excludes the unevaluable

    for metric in CONF:
        if metric not in d.columns:
            continue

        vals = d[metric].to_numpy(float)
        lab = d.correct.to_numpy(bool)
        cid = d.cluster_id.to_numpy()
        pooled = auc(vals, lab)
        lo, hi = cluster_boot_auc(vals, lab, cid, rng)

        # Within-receptor: one AUC per receptor, then the mean over receptors.
        #
        # MIN_ERR exists because the first run of this analysis did not have it and
        # was wrong. Accuracy is 92.3%, so errors are rare AND concentrated: 10 of
        # 40 receptors have ZERO wrong calls (AUC undefined) and 22 have fewer than
        # five (AUC is noise). An unweighted mean over all evaluable receptors gives
        # a receptor with one error the same weight as one with a hundred, and that
        # is what produced the first, too-confident number.
        per = []
        for r, g in d.groupby("receptor"):
            nw = int((~g.correct).sum())
            nc = int(g.correct.sum())
            v = auc(g[metric], g.correct)
            if not np.isnan(v):
                per.append({"receptor": r, "cluster_id": g.cluster_id.iloc[0],
                            "auc": v, "n": len(g), "n_wrong": nw, "n_correct": nc,
                            "evaluable": nw >= MIN_ERR and nc >= MIN_ERR})
        per = pd.DataFrame(per)
        ev = per[per.evaluable] if len(per) else per
        within = ev.auc.mean() if len(ev) else np.nan
        wlo, whi = (cluster_boot_mean(ev.auc.to_numpy(float), ev.cluster_id.to_numpy(), rng)
                    if len(ev) else (np.nan, np.nan))

        summary[metric] = {
            "pooled_auc": pooled, "pooled_ci": [lo, hi],
            "within_receptor_mean_auc": within, "within_receptor_ci": [wlo, whi],
            "n_receptors_with_any_errors": int(len(per)),
            "n_receptors_evaluable": int(len(ev)),
            "min_errors_required": MIN_ERR,
            "shrinkage": (pooled - within) if not np.isnan(within) else None,
        }
        rows.append({"metric": metric, "scope": "pooled", "auc": pooled, "ci_lo": lo, "ci_hi": hi,
                     "n_rows": len(d), "n_receptors": d.receptor.nunique(),
                     "n_clusters": d.cluster_id.nunique()})
        rows.append({"metric": metric, "scope": "within_receptor_mean", "auc": within,
                     "ci_lo": wlo, "ci_hi": whi, "n_rows": len(d),
                     "n_receptors": int(len(ev)), "n_clusters": int(ev.cluster_id.nunique()) if len(ev) else 0})

        for bb, g in d.groupby("backbone"):
            v = auc(g[metric], g.correct)
            rows.append({"metric": metric, "scope": f"pooled:{bb}", "auc": v,
                         "ci_lo": np.nan, "ci_hi": np.nan, "n_rows": len(g),
                         "n_receptors": g.receptor.nunique(),
                         "n_clusters": g.cluster_id.nunique()})

    # the sensitivity comparison: same pooled AUC computed on all rows
    for metric in CONF:
        if metric in d_all.columns:
            rows.append({"metric": metric, "scope": "pooled:INCLUDING_forced_inactive",
                         "auc": auc(d_all[metric].to_numpy(float),
                                    d_all.correct.to_numpy(bool)),
                         "ci_lo": np.nan, "ci_hi": np.nan, "n_rows": len(d_all),
                         "n_receptors": d_all.receptor.nunique(),
                         "n_clusters": d_all.cluster_id.nunique()})
    pd.DataFrame(rows).to_csv(OUT_CSV, index=False)
    if len(per):
        per.to_csv(os.path.join(INPUTS, 'p7_per_receptor.csv'), index=False)
    meta = {
        "question": "does model confidence separate correct from incorrect state calls?",
        "prereg_id": "P7",
        "ground_truth": "rmsd_to_active_ref < rmsd_to_inactive_ref",
        "predicate": "block_a `active` column (class A: npxxy AND tilt; B/F: tilt alone)",
        "exclusions_applied": ["excl_E1", "excl_E2"],
        "exclusions_deliberately_not_applied": ["excl_E3*", "excl_E4", "excl_E5", "excl_any"],
        "n_rows": int(len(d)), "n_rows_including_forced_inactive": int(len(d_all)),
        "forced_inactive_receptors": sorted(d_all.loc[d_all.forced_inactive, "receptor"].unique().tolist()),
        "n_receptors": int(d.receptor.nunique()),
        "n_clusters": int(d.cluster_id.nunique()),
        "overall_accuracy": float(d.correct.mean()),
        "bootstrap": {"unit": "cluster", "resamples": BOOT, "seed": SEED},
        "results": summary,
    }
    with open(OUT_JSON, "w") as fh:
        json.dump(meta, fh, indent=2, default=float)

    print(f"  n = {len(d):,} rows (excluding {len(d_all)-len(d)} forced-inactive), "
          f"{d.receptor.nunique()} receptors, {d.cluster_id.nunique()} clusters")
    print(f"  predicate accuracy vs structural truth: {d.correct.mean()*100:.1f}%\n")
    ev_n = summary[CONF[0]]["n_receptors_evaluable"] if summary else 0
    print(f"  receptors carrying an AUC (>={MIN_ERR} wrong AND >={MIN_ERR} correct): {ev_n} of 40\n")
    print(f"  {'metric':<22}{'pooled AUC':>22}{'within-receptor':>24}{'shrinkage':>12}")
    for m, v in summary.items():
        p = f"{v['pooled_auc']:.3f} [{v['pooled_ci'][0]:.3f},{v['pooled_ci'][1]:.3f}]"
        w = f"{v['within_receptor_mean_auc']:.3f} [{v['within_receptor_ci'][0]:.3f},{v['within_receptor_ci'][1]:.3f}]"
        print(f"  {m:<22}{p:>22}{w:>24}{v['shrinkage']:>12.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
