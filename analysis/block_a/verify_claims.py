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

# ---- exclusions ---------------------------------------------------------
# Added 2026-09-10 after analysis/sweep_manuscript.py found that the exclusion
# row counts quoted in Methods were checked by nothing. Block B's claim sheet
# mislabelled three of its four exclusion sets, so ours could not stay unchecked.
for flag, want in [("excl_E1", 25), ("excl_E2", 4), ("excl_E3", 4890),
                   ("excl_E3_tilt", 2000), ("excl_E3_npxxy", 4690),
                   ("excl_E4", 1495), ("excl_E5", 500), ("excl_any", 5093)]:
    check("EXCL", "%s rows" % flag, want, int(rows[flag].astype(bool).sum()))
for flag, want in [("excl_E3_npxxy", 24), ("excl_E3_tilt", 10)]:
    check("EXCL", "%s receptors" % flag, want,
          int(rows.loc[rows[flag].astype(bool), "receptor"].nunique()))
check("EXCL", "rows with no NPxxY value", 2295, int(rows.d_npxxy_oh.isna().sum()))
check("EXCL", "receptors with all-NaN NPxxY", 12,
      int(sum(1 for _, g in rows.groupby("receptor") if g.d_npxxy_oh.isna().all())))
check("EXCL", "excl_any share of corpus (%)", 53.7,
      round(100.0 * rows.excl_any.astype(bool).mean(), 1))

# ---- report -------------------------------------------------------------
if "--json" in sys.argv:
    print(json.dumps(results, indent=2, default=str)); sys.exit(0)

# --------------------------------------------------------------- CAPTIONS
# Added 2026-09-10. Until today the number sweep covered results.tex and
# methods.tex only, so every figure caption and the whole SI were unchecked --
# 112 numeric tokens. That is the worst place for a gap: a caption's
# load-bearing content IS its n, its filter and its threshold, and a caption is
# the least-read text in a paper. One SI caption was still asserting a singleton
# count that Methods had already been corrected on, because nothing propagated
# the fix.
#
# Every number below is recomputed from block_a_rows.csv on the caption's own
# stated filter. Where a caption's filter is "E1+E2", that is E1 and E2 only --
# never excl_any, which removes 54% of the corpus.

_d = rows[~(rows.excl_E1.astype(bool) | rows.excl_E2.astype(bool))].copy()
check("CAP1", "E1+E2 keeps 9,461 of 9,490 rows", 9461, int(len(_d)))
check("CAP2", "excl_any would remove 5,093 (54%)", 5093,
      int(rows.excl_any.astype(bool).sum()))

_A = _d[_d.gpcr_class == "A"].copy()
check("CAP3", "E1+E2 then Class A leaves 7,966 rows", 7966, int(len(_A)))

_A["fire"] = (_A.d_npxxy_oh < 9.08) & (_A.d_gpcrdb_tm6_tilt_246_637_ca > 14.932)
_p = _A.groupby(["receptor", "backbone", "arm"])["fire"].mean().unstack("arm").dropna()
check("CAP4", "Class A pairs with both arms", 159, int(len(_p)))
check("CAP5", "cells move up on adding the partner", 120,
      int((_p.cognate > _p.apo).sum()))
check("CAP6", "cells unchanged", 37, int((_p.cognate == _p.apo).sum()))
check("CAP7", "cells move down", 2, int((_p.cognate < _p.apo).sum()))
_ap = _A[_A.arm == "apo"].groupby(["receptor", "backbone"]).size()
_co = _A[_A.arm == "cognate"].groupby(["receptor", "backbone"]).size()
check("CAP8", "apo + cognate cells drawn", 319, int(len(_ap) + len(_co)))

# The two-axis cross-tabulation. It counts only rows where BOTH distances were
# measured: 2,295 of the 9,461 have no NPxxY axis at all, and a row that cannot
# be measured has not "fired neither". Computing it the naive way gives
# 3,318/254 instead of 2,611/157, which is how this check earned its existence.
_m = _d[_d.d_npxxy_oh.notna() & _d.d_gpcrdb_tm6_tilt_246_637_ca.notna()].copy()
_m["npx"] = _m.d_npxxy_oh < 9.08
_m["tilt"] = _m.d_gpcrdb_tm6_tilt_246_637_ca > 14.932
for _arm, _neither, _both in (("apo", 2611, 577), ("cognate", 157, 3162)):
    _g = _m[_m.arm == _arm]
    check("CAP9." + _arm, "%s rows firing neither predicate" % _arm, _neither,
          int((~_g.npx & ~_g.tilt).sum()))
    check("CAP10." + _arm, "%s rows firing both" % _arm, _both,
          int((_g.npx & _g.tilt).sum()))

# S-T5's denominator does NOT reproduce and is recorded as a mismatch rather
# than dropped. 610 predicate-active rows with no active reference reproduces
# exactly; the 4,866 it is quoted against does not, under any predicate
# definition tried (both-measured 3,739; tilt-and-NPxxY-or-NaN 5,230; tilt alone
# 5,548), and neither 4,866 nor 4,256 appears anywhere in the drop or in our
# own analysis. See DISCREPANCY_REPORT D-A-24.
_pa = _m[_m.npx & _m.tilt]
check("CAP11", "predicate-active rows with no active reference", 610,
      int(_pa.rmsd_to_active_ref.isna().sum()))
check("CAP12", "SI S-T5 denominator '4,866 predicate-active'", 4866,
      int(len(_pa)),
      note="does not reproduce; 4,866 and 4,256 are unsourced -- D-A-24")


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

# Write the results file on EVERY run, not only under a flag.
# Until 2026-09-10 this script dumped JSON to stdout under `-j` and nothing
# else, so `verify_claims_results.json` on disk was a hand-saved artefact that
# no run refreshed -- 47 stale entries while the suite had grown to 61.
# analysis/sweep_manuscript.py reads these files to confirm that a registry row
# claiming coverage names a check that ACTUALLY RAN, so a stale file there
# quietly makes real checks invisible and would let coverage rot unnoticed.
json.dump(results, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "verify_claims_results.json"), "w"),
          indent=1, default=str)
sys.exit(1 if bad else 0)
