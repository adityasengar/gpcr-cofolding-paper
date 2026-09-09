#!/usr/bin/env python3
"""
Recompute every checkable number in BLOCK_A_CLAIM_SHEET.md from the tidy files
and report whether each reproduces.

This is the evidence behind DISCREPANCY_REPORT.md. Re-run it after any refresh
of data/block_a/ — a claim that reproduces today can stop reproducing.

    python3 analysis/block_a/verify_claims.py            # table
    python3 analysis/block_a/verify_claims.py --json     # machine readable
"""
import json, os, sys
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                    "data", "block_a")
R = lambda *p: os.path.join(ROOT, *p)
TOL = 5e-3                      # what counts as "reproduces"

results = []
def check(cid, what, claimed, found, ok=None, note=""):
    if ok is None:
        try:    ok = abs(float(claimed) - float(found)) <= TOL
        except (TypeError, ValueError): ok = (claimed == found)
    results.append(dict(id=cid, what=what, claimed=claimed, found=found,
                        reproduces=bool(ok), note=note))

rows = pd.read_csv(R("01_rows", "block_a_rows.csv"))
head = pd.read_csv(R("03_aggregates", "headline_by_backbone.csv")).set_index("backbone")
fits = pd.read_csv(R("04_amplitude", "amplitude_fits.csv"))
conn = pd.read_csv(R("05_connector", "connector_summary.csv"))
pldd = pd.read_csv(R("06_confidence", "plddt_correlations.csv"))

# ---- corpus shape -------------------------------------------------------
check("CORPUS", "rows x cols", "9490x55", "%dx%d" % rows.shape)
check("CORPUS", "receptors", 48, rows.receptor.nunique())
check("CORPUS", "predicate-active rows", 4866, int(rows.active.sum()))

# ---- SC-1 tilt shift, and WHICH bootstrap the quoted CI is -------------
sc1 = {"boltz": (5.036, (4.403, 5.502)), "chai": (1.047, (0.373, 3.452)),
       "of3": (4.814, (4.072, 4.998)), "protenix": (5.307, (4.909, 5.603))}
for b, (v, ci) in sc1.items():
    r = head.loc[b]
    check("SC-1", "%s median tilt shift" % b, v, round(r.median_tilt_shift, 3))
    dc = abs(ci[0]-r.median_tilt_shift_cluster_ci_lo) + abs(ci[1]-r.median_tilt_shift_cluster_ci_hi)
    dr = abs(ci[0]-r.median_tilt_shift_receptor_ci_lo) + abs(ci[1]-r.median_tilt_shift_receptor_ci_hi)
    check("SC-1", "%s CI labelled cluster-boot" % b, "cluster",
          "receptor" if dr < dc else "cluster", ok=(dc <= dr),
          note="|d_cluster|=%.3f |d_receptor|=%.3f" % (dc, dr))

# ---- SC-2 fraction ------------------------------------------------------
for b, v in {"boltz":0.9456,"chai":0.8878,"of3":0.9152,"protenix":0.9118}.items():
    check("SC-2", "%s fraction_of_way_to_active" % b, v,
          round(head.loc[b].fraction_of_way_to_active, 4))
check("SC-2", "fraction denominator (receptors)", "38-39",
      int(head.n_receptors_fraction.max()),
      ok=(head.n_receptors_fraction.max() in (38, 39)))
lo, hi = head.fraction_of_way_to_active.min(), head.fraction_of_way_to_active.max()
check("SC-2", "stated range '89-95%'", "0.89-0.95",
      "%.3f-%.3f" % (lo, hi), ok=(lo >= 0.89 and hi <= 0.95))

# ---- SC-3 amplitude + connector ----------------------------------------
n = fits[(fits.axis=="npxxy") & (fits.inclusion_set=="class_a_only")]
check("SC-3", "NPxxY: all CIs cross zero", True,
      bool(((n.cluster_ci_lo < 0) & (n.cluster_ci_hi > 0)).all()))
check("SC-3", "NPxxY n_receptors", 34, int(n.n_receptors.iloc[0]))
check("SC-3", "NPxxY SD(dref)", 4.71, round(float(n.sd_predictor.iloc[0]), 2))
t = fits[(fits.axis=="tilt") & (fits.inclusion_set=="class_a_only")]
check("SC-3", "tilt slopes all positive (0.03-0.50)", True,
      bool((t.slope > 0).all()), note="slopes %s" % [round(x,3) for x in t.slope])
check("SC-3", "tilt SD(dref)", 1.19, round(float(t.sd_predictor.iloc[0]), 2))
pooled = conn[conn.scope=="pooled"].iloc[0]
check("SC-3", "connector delta signed (CI excludes 0)", True,
      not (pooled.delta_cluster_ci_lo < 0 < pooled.delta_cluster_ci_hi),
      note="CI [%.3f, %.3f]" % (pooled.delta_cluster_ci_lo, pooled.delta_cluster_ci_hi))
check("SC-3", "connector agreement 204/256", 204,
      int(pooled.n_pred_active_below_inactive_median))

# ---- SC-6 predicate calibration ----------------------------------------
act = rows[rows.active == True]
for b, (nn, far) in {"boltz":(1167,1),"chai":(1273,0),
                     "of3":(1229,1),"protenix":(1197,0)}.items():
    s = act[act.backbone == b]
    check("SC-6", "%s predicate-active n" % b, nn, len(s))
    check("SC-6", "%s rows >3A from active" % b, far,
          int((s.rmsd_to_active_ref > 3.0).sum()))
fp = (act.rmsd_to_active_ref > 3.0).sum() / len(act) * 100
check("SC-6", "headline false-positive rate", "0.02%", "%.3f%%" % fp,
      ok=(abs(fp - 0.02) <= 0.005), note="body of SC-6 says 0.04%")

# ---- SC-11 confidence ---------------------------------------------------
prim = pldd[pldd.primary_or_secondary == "primary"]
check("SC-11", "signed at cluster boot on primary", 2,
      int(prim.signed_at_cluster_boot.sum()))

# ---- report -------------------------------------------------------------
if "--json" in sys.argv:
    print(json.dumps(results, indent=2, default=str)); sys.exit(0)

bad = [r for r in results if not r["reproduces"]]
print("%-7s %-42s %-14s %-14s %s" % ("claim","quantity","claim sheet","data",""))
print("-" * 100)
for r in results:
    print("%-7s %-42s %-14s %-14s %s%s" % (
        r["id"], r["what"][:42], str(r["claimed"])[:14], str(r["found"])[:14],
        "ok" if r["reproduces"] else "MISMATCH",
        ("  (%s)" % r["note"]) if r["note"] and not r["reproduces"] else ""))
print("-" * 100)
print("%d of %d reproduce; %d mismatches" % (len(results)-len(bad), len(results), len(bad)))
sys.exit(1 if bad else 0)
