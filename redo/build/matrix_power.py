#!/usr/bin/env python3
"""
matrix_power.py -- the power arithmetic behind redo/RUN_MATRIX.md.

Every number in RUN_MATRIX.md's power section is produced here, from
data/block_a/01_rows/block_a_rows.csv and data/block_b/01_rows/rows_tidy.csv.
Nothing is read from a claim sheet.

    python3 redo/build/matrix_power.py            # all sections
    python3 redo/build/matrix_power.py unanimity  # one section

Sections
  unanimity  seed- vs sample-grain unanimity in Block A (the 256/319 number)
  clusters   paralog-cluster structure of the Block B panel
  depth      95% CI half-width as a function of samples per cell   <- headline
  kcurve     95% CI half-width as a function of paralog clusters run
  floor      the deep-apo floor, per backbone, Block A vs Block B
  cell       Wilson half-widths for a single cell at various n

Read-only on data/. Writes nothing.
"""
import os
import sys, math
import numpy as np
import pandas as pd

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo


A_ROWS = f"{ROOT}/data/block_a/01_rows/block_a_rows.csv"
B_ROWS = f"{ROOT}/data/block_b/01_rows/rows_tidy.csv"
SEED = 20260911

# Block A thresholds as used by analysis/block_a/verify_claims.py:141-142.
A_NPXXY_LT, A_TILT_GT = 9.08, 14.932


def load_b():
    """Block B rows, restricted to rows where BOTH axes were measured.

    3,200 of 32,000 rows have no NPxxY axis (EDNRA EDNRB GRPR HRH3, all four
    backbones, all four arms). A row that cannot be measured has not 'failed
    the predicate'. Restricting to measurable rows is what reproduces the
    catalogue's pooled fractions .158/.558/.809/.891 exactly; using all 32,000
    gives .142/.502/.728/.802 instead. Same data, different denominator.
    """
    r = pd.read_csv(B_ROWS, low_memory=False)
    r = r[r.d_npxxy_y558_y753_oh.notna() &
          r.d_gpcrdb_tm6_tilt_246_637_ca.notna()].copy()
    r["fire"] = ((r.d_npxxy_y558_y753_oh < r.threshold_npxxy_oh_active_lt) &
                 (r.d_gpcrdb_tm6_tilt_246_637_ca >
                  r.threshold_gpcrdb_tm6_tilt_active_gt)).astype(int)
    return r


def load_a():
    """Block A rows on the caption filter E1+E2 then Class A (CAP3: 7,966)."""
    r = pd.read_csv(A_ROWS, low_memory=False)
    r = r[~(r.excl_E1.astype(bool) | r.excl_E2.astype(bool))]
    r = r[r.gpcr_class == "A"].copy()
    r["fire"] = ((r.d_npxxy_oh < A_NPXXY_LT) &
                 (r.d_gpcrdb_tm6_tilt_246_637_ca > A_TILT_GT)).astype(int)
    return r


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


# ---------------------------------------------------------------- unanimity
def sec_unanimity():
    print("== unanimity (Block A, E1+E2, Class A) ==")
    a = load_a()
    cells = a.groupby(["receptor", "backbone", "arm"])["fire"].agg(["mean", "size"])
    n_unan_sample = int(((cells["mean"] == 0) | (cells["mean"] == 1)).sum())
    s = a.groupby(["receptor", "backbone", "arm", "seed_outer"])["fire"].mean().reset_index()
    s["call"] = s.fire > 0.5
    u = s.groupby(["receptor", "backbone", "arm"])["call"].nunique()
    print(f"  cells                                : {len(cells)}")
    print(f"  unanimous at SAMPLE grain (all 25)   : {n_unan_sample}  "
          f"({100*n_unan_sample/len(cells):.1f}%)")
    print(f"  unanimous at SEED grain (5 majorities): {int((u == 1).sum())}  "
          f"({100*(u == 1).mean():.1f}%)")
    print(f"  cells with ANY seed-to-seed disagreement: {int((u > 1).sum())}  "
          f"({100*(u > 1).mean():.1f}%)")
    print("  -> the widely quoted '256 of 319 unanimous across seeds' is the")
    print("     SAMPLE-grain count. At seed grain it is 300 of 319.")


# ----------------------------------------------------------------- clusters
def sec_clusters():
    print("== paralog-cluster structure (Block B panel) ==")
    r = pd.read_csv(B_ROWS, low_memory=False)
    m = r.drop_duplicates("receptor_slug")[["receptor_slug", "cluster_id"]]
    g = m.groupby("cluster_id")["receptor_slug"].apply(lambda s: sorted(s))
    print(f"  receptors {len(m)}   clusters {len(g)}   "
          f"singletons {int((g.apply(len) == 1).sum())}   max size {g.apply(len).max()}")
    for k, v in sorted(g.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print(f"    {len(v)}  {k:32s} {' '.join(v)}")
    miss = sorted(r[r.d_npxxy_y558_y753_oh.isna()].receptor_slug.unique())
    print(f"  receptors with NO NPxxY axis: {miss}")
    print(f"  -> effective clusters for a two-axis predicate: "
          f"{load_b().cluster_id.nunique()}")


def cluster_contrasts(r, nsamp=None, rng=None):
    """Per-cluster mean of per-receptor arm contrasts, optionally on a
    subsample of nsamp predictions per (receptor, arm, backbone) cell."""
    key = ["cluster_id", "receptor_slug", "arm", "backbone"]
    if nsamp is None:
        cellf = r.groupby(key)["fire"].mean().reset_index(name="f")
    else:
        rec = []
        for k, v in r.groupby(key):
            arr = v["fire"].to_numpy()
            idx = rng.permutation(len(arr))[:nsamp]
            rec.append((*k, arr[idx].mean()))
        cellf = pd.DataFrame(rec, columns=key + ["f"])
    w = cellf.groupby(["cluster_id", "receptor_slug", "arm"])["f"].mean().unstack("arm")
    d = pd.DataFrame({
        "cog_apo":  w.cognate - w.apo,
        "dec_apo":  w.decoy - w.apo,
        "cog_dec":  w.cognate - w.decoy,
        "cog_shuf": w.cognate - w.shuffled,
    })
    return d.groupby(level=0).mean()


def boot_hw(v, rng, B=3000):
    K = len(v)
    bs = v[rng.integers(0, K, (B, K))].mean(axis=1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return (hi - lo) / 2


CONTRASTS = ["cog_apo", "dec_apo", "cog_dec", "cog_shuf"]


# -------------------------------------------------------------------- depth
def sec_depth():
    print("== 95% CI half-width vs SAMPLES PER CELL (Block B, cluster boot) ==")
    rng = np.random.default_rng(SEED)
    r = load_b()
    fr = r.groupby(["receptor_slug", "arm", "backbone"])["fire"].mean().to_numpy()
    pq = float(np.mean(fr * (1 - fr)))
    print(f"  cells {len(fr)};  at 0 or 1: {int(((fr==0)|(fr==1)).sum())} "
          f"({100*((fr==0)|(fr==1)).mean():.1f}%)")
    print(f"  mean within-cell p(1-p) = {pq:.4f}  ->  binomial variance "
          f"{pq/50:.5f} at n=50, {pq/10:.5f} at n=10")
    cl = cluster_contrasts(r)
    bv = {c: cl[c].var(ddof=1) for c in CONTRASTS}
    print("  between-cluster variance: " +
          "  ".join(f"{c} {bv[c]:.4f}" for c in CONTRASTS))
    print(f"  -> at n=50 the sampling term is {100*(pq/50)/min(bv.values()):.1f}-"
          f"{100*(pq/50)/max(bv.values()):.1f}% of the smallest/largest "
          "between-cluster variance")
    print()
    print(f"  {'n/cell':>7} {'preds(576 cells)':>17} " +
          " ".join(f"{c:>17}" for c in CONTRASTS))
    for n in (3, 5, 10, 20, 50):
        ests = {c: [] for c in CONTRASTS}
        hws = {c: [] for c in CONTRASTS}
        for _ in range(40):
            cl = cluster_contrasts(r, nsamp=n, rng=rng)
            for c in CONTRASTS:
                v = cl[c].to_numpy()
                ests[c].append(v.mean())
                hws[c].append(boot_hw(v, rng, B=2000))
        print(f"  {n:>7} {n*576:>17,} " +
              " ".join(f"{np.mean(ests[c]):+.3f} +- {np.mean(hws[c]):.3f}"
                       for c in CONTRASTS))
    print("  -> 50 -> 10 samples/cell costs <=0.002 of half-width and saves 80%")


# ------------------------------------------------------------------- kcurve
def sec_kcurve():
    print("== 95% CI half-width vs NUMBER OF PARALOG CLUSTERS run ==")
    rng = np.random.default_rng(SEED)
    cl = cluster_contrasts(load_b())
    allc = cl.index.to_numpy()
    K = len(allc)
    print(f"  full panel K = {K} clusters, 36 receptors")
    print("  cluster-grain contrast    mean     SD    MDE80@k=24 @k=17 @k=12 @k=8")
    for c in CONTRASTS:
        sd = cl[c].std(ddof=1)
        mde = "  ".join(f"{2.80*sd/math.sqrt(k):.3f}" for k in (24, 17, 12, 8))
        print(f"    {c:9s} {cl[c].mean():+.3f}  {sd:.3f}    {mde}")
    print()
    print(f"  {'k':>4} " + " ".join(f"{c:>9}" for c in CONTRASTS))
    for k in (4, 6, 8, 10, 12, 14, 17, 20, 24):
        hw = {c: [] for c in CONTRASTS}
        for _ in range(80):
            sub = cl.loc[rng.choice(allc, size=k, replace=False)]
            for c in CONTRASTS:
                hw[c].append(boot_hw(sub[c].to_numpy(), rng, B=500))
        print(f"  {k:>4} " + " ".join(f"{np.median(hw[c]):9.3f}" for c in CONTRASTS))
    base = {c: boot_hw(cl[c].to_numpy(), rng, B=6000) for c in CONTRASTS}
    print("  ESTIMATE, sqrt(K/k) extrapolation beyond the panel:")
    for k in (30, 36, 40):
        print(f"  {k:>4} " + " ".join(f"{base[c]*math.sqrt(K/k):9.3f}"
                                     for c in CONTRASTS) + "   <- estimate")


# -------------------------------------------------------------------- floor
def sec_floor():
    print("== the deep-apo floor, per backbone, on two independent corpora ==")
    b = load_b()
    a = load_a()
    tb = b[b.arm == "apo"].groupby("backbone")["fire"].agg(["mean", "size"])
    ta = a[a.arm == "apo"].groupby("backbone")["fire"].agg(["mean", "size"])
    print("  pooled apo predicate-active fraction")
    print(f"  {'backbone':>9} {'Block A':>18} {'Block B':>18}")
    for bb in sorted(tb.index):
        print(f"  {bb:>9} {ta.loc[bb,'mean']:9.3f} (n={int(ta.loc[bb,'size']):>4})"
              f" {tb.loc[bb,'mean']:9.3f} (n={int(tb.loc[bb,'size']):>4})")
    print("  ADRB2 apo, per backbone -- the cell the redo brief names")
    xa = a[(a.arm == "apo") & (a.receptor == "ADRB2")].groupby("backbone")["fire"].agg(["mean", "size"])
    xb = b[(b.arm == "apo") & (b.receptor_slug == "ADRB2")].groupby("backbone")["fire"].agg(["mean", "size"])
    for bb in sorted(xb.index):
        print(f"  {bb:>9} {xa.loc[bb,'mean']:9.2f} (n={int(xa.loc[bb,'size']):>3})"
              f" {xb.loc[bb,'mean']:9.2f} (n={int(xb.loc[bb,'size']):>3})")
    c = b[b.arm == "apo"].groupby(["receptor_slug", "backbone"])["fire"].mean().unstack()
    print("  apo cells pinned at 0 / at 1, of 36 per backbone:")
    print("   ", {bb: (int((c[bb] == 0).sum()), int((c[bb] == 1).sum()))
                  for bb in c.columns})


# --------------------------------------------------------------------- cell
def sec_cell():
    print("== single-cell Wilson 95% half-width (points) ==")
    print(f"  {'n':>5} {'p=0.5':>8} {'p=0.9':>8} {'0 of n upper bound':>20}")
    for n in (10, 20, 25, 50, 100, 200, 500):
        lo1, hi1 = wilson(n // 2, n)
        lo2, hi2 = wilson(int(round(0.9 * n)), n)
        _, hi0 = wilson(0, n)
        print(f"  {n:>5} {100*(hi1-lo1)/2:8.1f} {100*(hi2-lo2)/2:8.1f} "
              f"{100*hi0:19.1f}%")
    print("  -> n=50 reproduces Block D's stated 8-14 point per-cell half-width")
    print("  -> the ONLY thing n=500 buys over n=50 is the 0-of-n upper bound,")
    print("     i.e. 'no minority basin above 0.8%' instead of 'above 7.1%'")


SECTIONS = {"unanimity": sec_unanimity, "clusters": sec_clusters,
            "depth": sec_depth, "kcurve": sec_kcurve,
            "floor": sec_floor, "cell": sec_cell}

if __name__ == "__main__":
    want = sys.argv[1:] or list(SECTIONS)
    for name in want:
        if name not in SECTIONS:
            sys.exit(f"unknown section {name}; choose from {list(SECTIONS)}")
        SECTIONS[name]()
        print()
