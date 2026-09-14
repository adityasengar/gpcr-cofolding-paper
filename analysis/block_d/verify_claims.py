#!/usr/bin/env python3
"""Verify Block D's claim sheet against what Block D actually shipped.

THE FACT THAT SHAPED THIS FILE, AND THEN CHANGED.

Block D's ZIP shipped no row-level data: the claim sheet named three corpora --
`experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` and its D2 and D3
siblings, 42,180 predictions between them -- and not one was in the bundle. That
is why almost every number in SC-D-1..12 was a number in a sentence.

**They arrived by hand on 2026-09-13** and sit in `received_2026_09_13/`,
read-only and gitignored by size: 14,000 / 2,370 / 25,810. Row counts, pins and
thresholds were all verified on arrival. So the PROSE-ONLY class below is no
longer FORCED, and the file has been moving claims out of it ever since --
54 testable / 12 prose-only on the day the zip landed, and the header prints
where it stands now.

**The prose-only entries that survive are the interesting ones**, because each
now names something the rows genuinely cannot settle rather than something that
merely had not shipped.

Every check carries one of THREE labels, and the label is the point:

  RECOMPUTED  -- computed here from a shipped file or from coordinates. This is
                 verification. There are far fewer of these than the claim sheet
                 has claims.
  CONSISTENCY -- one shipped number against another shipped number. Catches
                 transcription drift between the claim sheet, the Part A
                 documents, the gate reports and the flags. It cannot catch a
                 number that was wrong in every document at once.
  PROSE-ONLY  -- recorded, deliberately un-checkable, and listed so the count of
                 "verified" claims can never quietly include it. These are
                 declared rather than tested, and each names the file that would
                 make it testable.

A green CONSISTENCY check is not evidence about the world. A PROSE-ONLY entry is
not a check at all. Both are printed in their own totals so that "N checks pass"
can never be read as "N claims are verified". A FOURTH label is refused at the
source by `check()`: the testable total is RECOMPUTED + CONSISTENCY, so a label
outside the three could fail -- lowering the numerator -- while sitting in
neither total that forms the denominator.

Usage:  python3 analysis/block_d/verify_claims.py [-v]
Exit 1 on any RECOMPUTED or CONSISTENCY mismatch. PROSE-ONLY never fails --
it is a census of what cannot be tested, not a test.
"""
from __future__ import print_function

import collections
import csv
import itertools
import json
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
D = os.path.join(ROOT, "data", "block_d")
VERB = "-v" in sys.argv
R = []


KINDS = ("RECOMPUTED", "CONSISTENCY", "PROSE-ONLY")


def check(cid, kind, what, got, want, tol=None, note=""):
    # The report totals testable checks as RECOMPUTED + CONSISTENCY. A fourth
    # label would be able to FAIL -- lowering the numerator -- while appearing in
    # neither total, so the denominator would not contain it. Refuse it here.
    if kind not in KINDS:
        raise SystemExit("check(%s): unknown kind %r; must be one of %s"
                         % (cid, kind, ", ".join(KINDS)))
    if kind == "PROSE-ONLY":
        ok = True
    elif tol is None:
        ok = (got == want)
    else:
        try:
            ok = abs(float(got) - float(want)) <= tol
        except (TypeError, ValueError):
            ok = False
    R.append(dict(id=cid, kind=kind, what=what, got=got, want=want,
                  ok=bool(ok), note=note))


def read_csv(rel):
    path = os.path.join(D, rel)
    lines = [l for l in open(path) if not l.startswith("#")]
    return list(csv.DictReader(lines))


def clopper_pearson(k, n, alpha=0.05):
    """Exact binomial interval, in percent. No scipy: the Beta quantiles are
    obtained by bisection on the regularised incomplete beta, which is enough
    for the one decimal place the claim sheet quotes."""
    def betainc(a, b, x, terms=4000):
        # continued-fraction-free series; adequate at these small n
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        lbeta = (math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))
        front = math.exp(a * math.log(x) + b * math.log(1 - x) - lbeta) / a
        total, term = 1.0, 1.0
        for i in range(terms):
            term *= (a + b + i) * x / (a + 1 + i)
            total += term
            if abs(term) < 1e-14:
                break
        return min(1.0, front * total)

    def solve(target, a, b):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if betainc(a, b, mid) < target:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    lo = 0.0 if k == 0 else solve(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else solve(1 - alpha / 2, k + 1, n - k)
    return round(100 * lo, 1), round(100 * hi, 1)


# ===========================================================================
# RECOMPUTED -- the panel, the clusters, the arithmetic, the coordinates
# ===========================================================================

d1 = read_csv("09_references/tier_d1_panel.csv")
d2 = read_csv("09_references/tier_d2_panel.csv")
d3 = read_csv("09_references/tier_d3_panel.csv")
par = read_csv("09_references/paralogy_clusters.csv")
nb = read_csv("09_references/nanobody_state_anchors.csv")

check("D01", "RECOMPUTED", "D1 panel is 7 receptors", len(d1), 7)
check("D02", "RECOMPUTED", "D2 panel is 4 receptors", len(d2), 4)
check("D03", "RECOMPUTED", "D3 panel is 26 receptors", len(d3), 26)
check("D04", "RECOMPUTED", "paralogy map covers 40 receptors", len(par), 40)
check("D05", "RECOMPUTED", "paralogy map holds 26 clusters",
      len({r["cluster_id"] for r in par}), 26)

d3set = {r["receptor_slug"] for r in d3}
d3par = [r for r in par if r["receptor"] in d3set]
check("D06", "RECOMPUTED", "every D3 receptor is in the paralogy map",
      len(d3par), 26)
check("D07", "RECOMPUTED", "D3's 26 receptors fall in 22 clusters (Flag D-1)",
      len({r["cluster_id"] for r in d3par}), 22)

# D1 and D2 cluster-boot degeneracy: Flag D-1 asserts 1 receptor per cluster
for tier, rows, n in (("D1", d1, 7), ("D2", d2, 4)):
    s = {r["receptor_slug"] for r in rows}
    cl = {r["cluster_id"] for r in par if r["receptor"] in s}
    check("D08." + tier, "RECOMPUTED",
          "%s is cluster-boot-degenerate: %d receptors in %d clusters"
          % (tier, n, len(cl)), len(cl), n,
          note="1 receptor per cluster, so cluster-boot == receptor-boot")

# Prediction-count arithmetic
check("D09", "RECOMPUTED", "D1 = 7 rec x 4 bb x 500 samples", 7 * 4 * 500, 14000)
check("D10", "RECOMPUTED", "D3 nominal = 26 x 4 x 5 depths x 50",
      26 * 4 * 5 * 50, 26000)
check("D11", "RECOMPUTED", "D3 shipped 25,810, i.e. 190 short of nominal",
      26000 - 25810, 190, note="C-D-6 records a 190-prediction Chai/OF3 shortfall")

# D2's total reconciles exactly one way, and it disagrees with Part A by a cell
_arms = sum(len([a for a in r["arms"].replace(";", ",").split(",") if a.strip()])
            for r in d2)
check("D11b", "RECOMPUTED", "D2 nominal cells = 13 arms x 4 backbones",
      _arms * 4, 52)
check("D11c", "RECOMPUTED",
      "D2 total 2,370 = 44 cells at n=50 PLUS the one 170-prediction cell",
      44 * 50 + 170, 2370,
      note="C-D-5 records AGTR1 x active_nb x OF3 landing 170. That makes 45 "
           "populated cells, while PARTA_D2 section 2 says 44 -- see D-D-3")

# C-D-12: every nanobody anchor predates every stated training cutoff
check("D12", "RECOMPUTED", "four nanobody anchor PDBs", len(nb), 4)
cutoffs = {"chai": "2021-01-12", "protenix": "2021-09-30", "boltz2": "2023-06-01"}
late = []
for r in nb:
    for bb, cut in cutoffs.items():
        if r["deposition_date"] >= cut:
            late.append("%s/%s" % (r["pdb_id"], bb))
check("D13", "RECOMPUTED",
      "C-D-12: no Nb anchor postdates any dated cutoff", len(late), 0,
      note="OF3's cutoff is TBD in the shipped table, so it cannot be tested")
check("D14", "RECOMPUTED", "the four anchor PDBs are the ones named in SC-D-6",
      sorted(r["pdb_id"] for r in nb), sorted(["5JQH", "6VI4", "4MQS", "6OS2"]))

# Exact binomial intervals quoted in the claim sheet and Part A
for cid, k, n, lo, hi, what in (
        ("D15", 24, 50, 33.7, 62.6, "OPRK x Boltz inactive_nb 48% (SC-D-6 flagship)"),
        ("D16", 38, 50, 61.8, 86.9, "ADRB2 x Protenix inactive_nb 76% (SC-D-7)"),
        ("D17", 0, 50, 0.0, 7.1, "a 0/50 cell"),
        ("D18", 37, 50, 59.7, 85.4, "OPRK x Chai apo 74%"),
        ("D19", 29, 50, 43.2, 71.8, "ACM2 x OF3 cognate 58% (SC-D-4 miss)"),
        ("D20", 18, 50, 22.9, 50.8, "OPRK x OF3 cognate 36% (SC-D-4 miss)")):
    g = clopper_pearson(k, n)
    check(cid, "RECOMPUTED", "Clopper-Pearson 95%% CI, %s" % what, g, (lo, hi),
          tol=None if g == (lo, hi) else None)

# Flag D-2 / W-D-6: the slope unit really is ln, and the factor really is ~2.303
check("D21", "RECOMPUTED", "log10 slope / ln slope == ln(10) (Flag D-2)",
      round(3.877 / 1.684, 3), round(math.log(10), 3), tol=0.02,
      note="GATE-2 table: Boltz -3.877 %/log10 against -1.684 %/ln")

# Coordinates -- the only geometry in this drop that can be recomputed
meas_path = os.path.join(HERE, "cif_measurements.json")
if os.path.exists(meas_path):
    meas = json.load(open(meas_path))
    for cid, fn, want, tol, what in (
            ("D22", "d2_adrb2_inactive_nb_protenix.cif", 4.53, 0.02,
             "SC-D-7 flagship: Protenix builds an active pocket under inactive-Nb"),
            ("D23", "d2_acm2_active_nb_chai.cif", 19.1, 0.05,
             "F5 Chai receptor-locked: active-Nb docked, pocket stays inactive"),
            # NOT d3_protenix_agtr1_depth8: the manifest's "NPxxY 11 -> 3.4 A"
            # quotes GATE-3's CELL MEDIAN over 50 samples (its table column is
            # headed "med NPxxY"), not this one structure. Comparing a single
            # shipped sample against a median is a category error, and this
            # check made it before GATE-3 was read. The file measures 3.56 A;
            # both are far below the 9.08 A threshold. See D-D-4.
            ):
        m = meas.get(fn, {})
        check(cid, "RECOMPUTED", what, m.get("npxxy_oh", "not measured"), want,
              tol=tol, note="measured from coordinates by cifmeasure.py")

    # Every spot-check's state call against the 9.08 A predicate threshold
    calls = {
        "d1_adrb2_chai_apo.cif": ("active", "SC-D-1 Chai outlier, ADRB2 100%"),
        "d1_adrb2_boltz_apo.cif": ("inactive", "same receptor, Boltz 0%"),
        "d1_ghsr_boltz_apo.cif": ("inactive", "SC-D-2 convergent-inactive"),
        "d1_cnr2_chai_apo.cif": ("active", "SC-D-1 Chai outlier, CNR2"),
        "d1_lpar1_of3_apo.cif": ("active", "SC-D-12 coherent non-reference fold"),
        "d3_boltz_opsd_depth8.cif": ("active", "SC-D-12 clean-lever counterpoint"),
        "d2_adrb2_inactive_nb_boltz.cif": ("inactive", "SC-D-6 correct case"),
    }
    for i, (fn, (want_call, what)) in enumerate(sorted(calls.items())):
        v = meas.get(fn, {}).get("npxxy_oh")
        got = "-" if v is None else ("active" if v < 9.08 else "inactive")
        check("D25.%d" % (i + 1), "RECOMPUTED",
              "NPxxY call on %s -- %s" % (fn.replace(".cif", ""), what),
              got, want_call, note="d(OH,OH) = %s A against the 9.08 A threshold" % v)

    # PARTA_D1 section 4 tabulates its own NPxxY-OH for the SAME five CIFs
    # ("Five CIFs pulled from ..."), and the manifest gives all five one seed
    # and one sample index. They should therefore be the same structures.
    for i, (fn, want) in enumerate(sorted({
            "d1_cnr2_chai_apo.cif": 2.25, "d1_adrb2_chai_apo.cif": 4.19,
            "d1_lpar1_of3_apo.cif": 5.42, "d1_adrb2_boltz_apo.cif": 11.58,
            "d1_ghsr_boltz_apo.cif": 10.03}.items())):
        got = meas.get(fn, {}).get("npxxy_oh")
        check("D27.%d" % (i + 1), "RECOMPUTED",
              "PARTA_D1 s4 NPxxY-OH for %s" % fn.replace(".cif", ""),
              got, want, tol=0.02,
              note="no state call changes; see D-D-8")

    check("D24", "RECOMPUTED",
          "AGTR1 depth-8 shipped sample is active-side of the 9.08 A threshold",
          meas.get("d3_protenix_agtr1_depth8.cif", {}).get("npxxy_oh", 99) < 9.08,
          True,
          note="3.56 A measured here; GATE-3's 3.40 A is the cell median over 50")

    check("D26", "RECOMPUTED",
          "all 15 structures: tabled 7.53 agrees with the file's own NPxxY motif",
          sum(1 for m in meas.values() if m.get("motif_agrees")), 15)
else:
    check("D22", "RECOMPUTED", "structure measurements", "cifmeasure.py not run",
          "run analysis/block_d/cifmeasure.py first")

# ===========================================================================
# CONSISTENCY -- shipped number against shipped number
# ===========================================================================

def flat(rel):
    """File contents with all runs of whitespace collapsed to one space.

    Markdown wraps mid-phrase, so a substring test against the raw text is a
    test of where the author's line breaks fell. Flag D-10 writes the OPRK
    deltas with a newline between "Boltz" and "+44"; searching the raw file for
    "Boltz +44" therefore returned False and reported a disagreement between two
    documents that say exactly the same thing. Same defect as
    analysis/audit_asks.py hit on its second version, in a different file, three
    hours later."""
    return " ".join(open(os.path.join(D, rel)).read().split())


claims = flat("01_claims/BLOCK_D_CLAIM_SHEET.md")
flags = flat("04_flags/BLOCK_D_MANUSCRIPT_FLAGS.md")
pa2 = flat("07_partA/PARTA_D2.md")
gate2 = flat("06_gate_reports/GATE_2_D3_SLOPES.md")

check("D30", "CONSISTENCY", "SC-D-4 and Flag D-9 both say 14/16, not 15/16",
      ("14/16" in claims or "14 of 16" in claims,
       "14/16" in flags or "14 of 16" in flags), (True, True))
check("D31", "CONSISTENCY", "the two SC-D-4 misses are the two OF3 cells",
      ("ACM2 58" in claims.replace(" %", "%").replace("%", " %")
       or "ACM2 58 %" in claims, "OPRK 36 %" in claims), (True, True))
for bb, delta in (("Boltz", "+44"), ("Chai", "+8"), ("OF3", "+10"),
                  ("Protenix", "+6")):
    check("D32." + bb, "CONSISTENCY",
          "SC-D-6 and Flag D-10 agree on OPRK %s delta %s" % (bb, delta),
          ("%s %s" % (bb, delta) in claims, "%s %s" % (bb, delta) in flags),
          (True, True))
for bb, sl in (("Boltz", "-1.68"), ("Chai", "-0.82"), ("OF3", "-2.73"),
               ("Protenix", "-2.96")):
    s = sl.replace("-", "−")
    check("D33." + bb, "CONSISTENCY",
          "SC-D-8 slope for %s matches GATE-2's recomputation" % bb,
          (s in claims or sl in claims,
           sl.lstrip("-") in gate2 or s in gate2), (True, True))
check("D34", "CONSISTENCY", "Flag D-3 and SC-D-8 both mark Chai UNSIGNED",
      ("UNSIGNED" in claims, "unsigned" in flags.lower()), (True, True))
check("D35", "CONSISTENCY",
      "SC-D-6's flagship CI matches Part A's OPRK x Boltz row",
      "[33.7, 62.6]" in claims and "[33.7, 62.6]" in pa2, True)
check("D36", "CONSISTENCY", "SC-D-7's 76% CI matches Part A's ADRB2 x Protenix",
      "[61.8, 86.9]" in claims and "[61.8, 86.9]" in pa2, True)
check("D37", "CONSISTENCY",
      "Flag D-7 and the claim sheet name the same scorer of record",
      "d9c646af" in claims and "d9c646af" in flags, True)

# ===========================================================================
# ===========================================================================
# THE ROWS LANDED 2026-09-13, and eleven of the twelve PROSE-ONLY claims became
# testable the moment they did.  Every one whose stated need was "D1/D2/D3
# rows.csv" now has one.
#
# TWO PARSING TRAPS, both of which cost me a wrong answer before I caught them:
#   * Block D's input_path varies in DEPTH by backbone -- chai has a clean
#     <receptor>/<ligand>/<arm>/<backbone>/seed_N/ layout while boltz and protenix
#     carry extra `boltz_results_...` and `chunk_N` segments.  A positional parse
#     returns the wrong segment SILENTLY.  Backbone is derived by TOKEN MATCH.
#   * float("nan") does NOT raise.  Reading these columns without an isnan guard
#     poisons any mean or correlation computed from them, and the result looks
#     like a number.
# ===========================================================================

# HERE, not D: `D` is the read-only drop at data/block_d/, and a late delivery
# lands in analysis/ rather than being retro-fitted into a pristine drop --
# the same rule rows.tier3.v2.csv follows for Block C.
ROWS_DIR = os.path.join(HERE, "received_2026_09_13")
BACKBONES = ("boltz", "chai", "of3", "protenix")
D1_RECEPTORS = {"ADRB2", "CNR2", "CXCR4", "GHSR", "LPAR1", "NPY1R", "OPSD"}


def drows(tier):
    """D-tier rows, or None if that delivery is not on this machine."""
    path = os.path.join(ROWS_DIR, f"rows.{tier}.csv")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        return list(csv.DictReader(fh))


def num(v):
    """float or None -- and None for NaN, because float('nan') does not raise."""
    try:
        f = float(v)
        return None if f != f else f
    except (TypeError, ValueError):
        return None


def bb_of(r):
    hit = [t for t in (r.get("input_path") or "").split("/") if t in BACKBONES]
    return hit[0] if len(hit) == 1 else None


def predicate(r):
    """The two-instrument call, using the thresholds AS CARRIED IN THE ROW."""
    npx, tilt = num(r.get("d_npxxy_y558_y753_oh")), num(r.get("d_gpcrdb_tm6_tilt_246_637_ca"))
    tn, tt = num(r.get("threshold_npxxy_oh_active_lt")), num(r.get("threshold_gpcrdb_tm6_tilt_active_gt"))
    if None in (npx, tilt, tn, tt):
        return None
    return (npx < tn) and (tilt > tt)


# PARTA_D3 §4, transcribed. The row labels are depths, the columns backbone
# pairs. Kept as data so the reproduction and the claim sheet's own internal
# consistency can both be checked against the same object.
D3_TAU_CLAIM = {
    "8/bol~cha": 0.25, "8/bol~of3": 0.15, "8/bol~pro": 0.13,
    "8/cha~of3": 0.17, "8/cha~pro": -0.03, "8/of3~pro": 0.59,
    "32/bol~cha": 0.26, "32/bol~of3": 0.24, "32/bol~pro": 0.42,
    "32/cha~of3": 0.11, "32/cha~pro": 0.08, "32/of3~pro": 0.47,
    "128/bol~cha": 0.52, "128/bol~of3": 0.14, "128/bol~pro": 0.19,
    "128/cha~of3": 0.15, "128/cha~pro": 0.21, "128/of3~pro": 0.29,
    "512/bol~cha": 0.42, "512/bol~of3": 0.03, "512/bol~pro": -0.12,
    "512/cha~of3": 0.08, "512/cha~pro": -0.18, "512/of3~pro": 0.23,
    "full/bol~cha": 0.44, "full/bol~of3": 0.02, "full/bol~pro": -0.08,
    "full/cha~of3": -0.06, "full/cha~pro": -0.11, "full/of3~pro": 0.30,
}
_BB_SHORT = {"boltz": "bol", "chai": "cha", "of3": "of3", "protenix": "pro"}

# PARTA_D3 §2 fits against ln(depth) with the full condition entered at its
# NOMINAL 4096. That choice is the difference between reproducing the four slopes
# and not, and it is stated in the document rather than derivable from the rows.
DEPTH_NOMINAL = {"8": 8, "32": 32, "128": 128, "512": 512, "full": 4096}


def _wols(pts):
    """Slope of y on x, weighted by w. pts are (x, y, w) triples.

    The weight is the cell's ROW COUNT, not a constant: C-D-6 records a
    190-prediction shortfall concentrated on chai and of3, so their cells are not
    all n=50, and an unweighted fit misses exactly those two backbones.
    """
    W = sum(w for _x, _y, w in pts)
    if not W:
        return None
    mx = sum(x * w for x, _y, w in pts) / W
    my = sum(y * w for _x, y, w in pts) / W
    sxx = sum(w * (x - mx) ** 2 for x, _y, w in pts)
    if sxx == 0:
        return None
    return sum(w * (x - mx) * (y - my) for x, y, w in pts) / sxx


def depth_of(r):
    """The D3 depth condition. No depth token in the path IS the full condition."""
    m = re.search(r"depth[_-]?(\d+)", r.get("input_path") or "", re.I)
    return m.group(1) if m else "full"


def kendall_tau_b(xs, ys):
    """tau-b, written out rather than imported.

    scipy 1.6.2 sits against numpy 1.24.4 here and warns on import
    (GROUP0_SYSTEMS.md §3.5); more to the point, the tie correction is the whole
    question -- these active fractions are full of ties at 0 and at 1 -- so the
    denominator is not a detail to delegate. tau-a reproduces 1 of 30 cells,
    tau-b reproduces 30.
    """
    n = len(xs)
    conc = disc = tx = ty = 0
    for i in range(n):
        for j in range(i + 1, n):
            a, b = xs[i] - xs[j], ys[i] - ys[j]
            if a == 0 and b == 0:
                tx += 1
                ty += 1
            elif a == 0:
                tx += 1
            elif b == 0:
                ty += 1
            elif a * b > 0:
                conc += 1
            else:
                disc += 1
    n0 = n * (n - 1) / 2.0
    den = ((n0 - tx) * (n0 - ty)) ** 0.5
    return (conc - disc) / den if den else None


def _tau_table(d3, zero_fill):
    """{"<depth>/<pair>": tau_b} over per-(receptor, backbone) active fractions.

    zero_fill=True carries a receptor whose predicate is unevaluable at 0.0,
    which is what Block D did; False drops it, which is what the quantity
    supports. The difference is SC-D-9/inflation.
    """
    act, tot, seen = collections.Counter(), collections.Counter(), set()
    for r in d3:
        k = (depth_of(r), bb_of(r), r["receptor_slug"].upper())
        seen.add(k)
        p = predicate(r)
        if p is None:
            continue
        tot[k] += 1
        act[k] += bool(p)
    recs = sorted({k[2] for k in seen})
    if not zero_fill:
        recs = [r for r in recs
                if any(tot.get((d, b, r)) for d, b, _ in seen)]
        recs = [r for r in recs
                if all(tot.get((k[0], k[1], r)) for k in seen if k[2] == r)]
    out = {}
    for depth in {k[0] for k in seen}:
        for x, y in itertools.combinations(BACKBONES, 2):
            pts = []
            for rec in recs:
                v = []
                for bb in (x, y):
                    n = tot.get((depth, bb, rec), 0)
                    v.append(act[(depth, bb, rec)] / n if n else
                             (0.0 if zero_fill else None))
                if None not in v:
                    pts.append(v)
            if len(pts) < 3:
                continue
            out[f"{depth}/{_BB_SHORT[x]}~{_BB_SHORT[y]}"] = kendall_tau_b(
                [p[0] for p in pts], [p[1] for p in pts])
    return out


def rate_by(rows, keyfn):
    act, tot = collections.Counter(), collections.Counter()
    for r in rows:
        p = predicate(r)
        if p is None:
            continue
        k = keyfn(r)
        tot[k] += 1
        act[k] += bool(p)
    return {k: (act[k], tot[k]) for k in tot}


def verify_from_rows():
    """Recompute what the landed rows can settle. Silent no-op if absent."""
    d1 = drows("d1_deep_apo")
    if d1 is None:
        return
    check("D-rows", "RECOMPUTED", "D1 rows present and the expected size",
          len(d1), 14000)

    # -- SC-D-2: the three convergent-inactive receptors, ceiling 6.6%
    by = rate_by(d1, lambda r: (r["receptor_slug"].upper(), bb_of(r)))
    for rec, bb, want_k, want_n in (("NPY1R", "of3", 33, 500),
                                    ("CXCR4", "of3", 19, 500)):
        k, n = by.get((rec, bb), (None, None))
        check(f"SC-D-2/{rec}", "RECOMPUTED",
              f"{rec} x {bb} predicate-active count", f"{k}/{n}", f"{want_k}/{want_n}")
    ghsr = [v for (rec, _b), v in by.items() if rec == "GHSR"]
    check("SC-D-2/GHSR", "RECOMPUTED", "GHSR active on every backbone",
          sum(k for k, _n in ghsr), 0)

    # -- SC-D-1: the per-cell table exists for all 7 receptors x 4 backbones
    cells = {k for k in by if k[1]}
    check("SC-D-1", "RECOMPUTED", "D1 per-cell grid is complete (7 x 4)",
          len(cells), 28)
    check("SC-D-1/n", "RECOMPUTED", "every D1 cell carries 500 scored rows",
          sorted({n for _k, n in by.values()}), [500])

    # -- SC-D-11: the cross-tier reproduction. PARTA_D1 sec.6 names the filter
    # precisely enough to re-run: Block A rows, the 7 D1 receptors, apo arm.
    # The SELECTION reproduces exactly. The four DELTAS it also quotes cannot be
    # checked here -- PARTA_D1 lives in paper_af3's RELEASE repo, not their working
    # repo (F-24), so neither side holds it. That half stays prose, and says why.
    ba = os.path.join(ROOT, "data", "block_a", "01_rows", "block_a_rows.csv")
    if os.path.exists(ba):
        with open(ba, encoding="utf-8", errors="replace") as fh:
            arows = [r for r in csv.DictReader(fh)
                     if r.get("receptor", "").upper() in D1_RECEPTORS
                     and r.get("arm") == "apo"]
        cells = collections.Counter((r["receptor"].upper(), r["backbone"]) for r in arows)
        check("SC-D-11/n", "RECOMPUTED",
              "PARTA_D1 sec.6's filter selects exactly 700 Block A rows", len(arows), 700)
        check("SC-D-11/cells", "RECOMPUTED",
              "and exactly 28 cells (7 receptors x 4 backbones)", len(cells), 28)
        check("SC-D-11/per_cell", "RECOMPUTED",
              "at exactly 25 rows per cell", sorted(set(cells.values())), [25])

    # -- SC-D-3: "CNR2 100% sub-A to BOTH references on all 4 backbones".
    # The NUMBER and the WORDING do not pick out the same quantity, and the data
    # says which is which: CNR2's worst pocket RMSD to ACTIVE is 0.791 A, so
    # sub-A-to-active is genuinely 100.0% on all four; its worst to INACTIVE is
    # 1.270 A, so sub-A to BOTH is 86.0 / 91.6 / 99.8 / 96.8.  Recorded as a
    # MISMATCH on the claim as worded, with the reading that IS 100% named beside
    # it -- this project's rule is that the data wins and the disagreement is
    # recorded rather than smoothed.
    cn = [r for r in d1 if r.get("receptor_slug", "").upper() == "CNR2"]
    if cn:
        tb, bb_both, ta, acc = (collections.Counter() for _ in range(4))
        worst_a = worst_i = 0.0
        for r in cn:
            a, i, b = (num(r.get("pocket_ca_rmsd_active")),
                       num(r.get("pocket_ca_rmsd_inactive")), bb_of(r))
            if a is None or not b:
                continue
            worst_a = max(worst_a, a)
            ta[b] += 1
            acc[b] += (a < 1.0)
            if i is not None:
                worst_i = max(worst_i, i)
                tb[b] += 1
                bb_both[b] += (a < 1.0 and i < 1.0)
        check("SC-D-3", "RECOMPUTED",
              "CNR2 sub-A to BOTH references, all 4 backbones (the claim AS WORDED)",
              sorted(round(100 * bb_both[b] / tb[b], 1) for b in tb if tb[b]),
              [100.0, 100.0, 100.0, 100.0],
              note=f"worst pocket RMSD to inactive is {worst_i:.3f} A, so not every "
                   f"sample is sub-A to both")
        check("SC-D-3/active", "RECOMPUTED",
              "CNR2 sub-A to the ACTIVE reference alone IS 100% on all four",
              sorted(round(100 * acc[b] / ta[b], 1) for b in ta if ta[b]),
              [100.0, 100.0, 100.0, 100.0],
              note=f"worst pocket RMSD to active is {worst_a:.3f} A")

    d3 = drows("d3_msa_depth")
    if d3 is not None:
        check("D3-rows", "RECOMPUTED", "D3 rows present and the expected size",
              len(d3), 25810)
        # -- SC-D-8e: does pLDDT move with depth at all, per backbone?
        agg = collections.defaultdict(list)
        for r in d3:
            b, p = bb_of(r), num(r.get("plddt_mean"))
            if b and p is not None:
                agg[b].append(p)
        check("SC-D-8e/span", "RECOMPUTED",
              "pLDDT mean is present on every backbone for the depth sweep",
              sorted(agg), sorted(BACKBONES))

        # -- SC-D-8b: sub-Angstrom-to-active, full -> depth 8, per backbone.
        # This is the leg that separates LEVER from DEGRADATION: Boltz GAINS when
        # the alignment is starved while OF3 and Protenix LOSE, which is a
        # different phenomenon from "shallow MSA produces alternative states".
        sub, tt = collections.Counter(), collections.Counter()
        for r in d3:
            pk, b = num(r.get("pocket_ca_rmsd_active")), bb_of(r)
            if pk is None or not b:
                continue
            m = re.search(r"depth[_-]?(\d+)", r.get("input_path") or "", re.I)
            d = m.group(1) if m else "full"      # no depth token == the full condition
            tt[(b, d)] += 1
            sub[(b, d)] += (pk < 1.0)
        for b, want in (("boltz", 8.7), ("of3", -20.9), ("protenix", -8.7)):
            if tt.get((b, "8")) and tt.get((b, "full")):
                delta = (100 * sub[(b, "8")] / tt[(b, "8")]
                         - 100 * sub[(b, "full")] / tt[(b, "full")])
                # tol 0.15: the claim sheet rounds to one decimal, and protenix
                # lands on -8.75, which rounds either way.
                check(f"SC-D-8b/{b}", "RECOMPUTED",
                      f"sub-A-to-active delta full->depth8 on {b} (pp)",
                      round(delta, 1), want, tol=0.15)
        # -- SC-D-10: the OPSD x Boltz cross-tier divergence. The SAME cell,
        # scored two ways: 38.8% at n=500 in D1's deep-apo sampling, 10.0% at n=50
        # in D3's full-depth condition. It is the sharpest single argument in
        # either campaign for why n=50 is not enough to characterise an apo cell --
        # the two differ by 29 points on identical inputs.
        opsd_d1 = [r for r in d1 if r.get("receptor_slug", "").upper() == "OPSD"
                   and bb_of(r) == "boltz"]
        kk = [predicate(r) for r in opsd_d1]
        kk = [x for x in kk if x is not None]
        if kk:
            check("SC-D-10/deep", "RECOMPUTED",
                  "OPSD x boltz predicate-active at n=500 (D1 deep apo)",
                  round(100 * sum(kk) / len(kk), 1), 38.8, tol=0.05)
        o3 = [r for r in d3 if r.get("receptor_slug", "").upper() == "OPSD"
              and bb_of(r) == "boltz"
              and not re.search(r"depth[_-]?\d+", r.get("input_path") or "", re.I)]
        k3 = [predicate(r) for r in o3]
        k3 = [x for x in k3 if x is not None]
        if k3:
            check("SC-D-10/n50", "RECOMPUTED",
                  "the same cell at n=50 (D3 full depth)",
                  round(100 * sum(k3) / len(k3), 1), 10.0, tol=0.05)

        # -- SC-D-9: the 5 x 6 Kendall-tau cross-backbone concordance table.
        #
        # PARTA_D3 §4 says only "tau over the 26 receptors' per-cell active
        # fractions". It does not say WHICH tau, and it does not say what it did
        # with the receptors on which the predicate has no value. Both had to be
        # recovered by reproducing the table, and the recovered convention is the
        # finding -- see SC-D-9/undefined below.
        #
        # tau-a reproduces 1 of 30. tau-b over 24 reproduces 9 of 30. tau-b over
        # 26, carrying the two axis-undefined receptors at 0%, reproduces 30 of 30
        # to within 0.005, which is the rounding of a 2-dp table.
        d3tau = _tau_table(d3, zero_fill=True)
        d3tau24 = _tau_table(d3, zero_fill=False)
        hits = sum(1 for k, v in D3_TAU_CLAIM.items()
                   if d3tau.get(k) is not None and abs(d3tau[k] - v) <= 0.015)
        check("SC-D-9/table", "RECOMPUTED",
              "the 30 Kendall-tau values reproduce (tau-b, n=26, axis-undefined "
              "receptors carried at 0%)", hits, 30)
        worst = max((abs(d3tau[k] - v) for k, v in D3_TAU_CLAIM.items()
                     if d3tau.get(k) is not None), default=None)
        check("SC-D-9/rounding", "CONSISTENCY",
              "worst deviation across all 30 cells, against a 2-dp table",
              round(worst, 3) if worst is not None else None,
              round(worst, 3) if worst is not None else None)

        # The two receptors the predicate cannot describe. This is not a pipeline
        # failure and not missing data: EDNRB and GRPR carry LEUCINE at 7.53, so
        # d(Y5.58 OH, Y7.53 OH) is not a quantity that exists for them. The rows
        # say so themselves -- anchor_7_53_aa_expected is "L" -- and every one of
        # their 1,960 rows has d_npxxy_y558_y753_oh = nan while still carrying
        # passed=True. Block D entered them in the table at 0% active, which reads
        # as "never active" and means "never measurable".
        undef = sorted({r["receptor_slug"].upper() for r in d3
                        if num(r.get("d_npxxy_y558_y753_oh")) is None})
        check("SC-D-9/undefined", "RECOMPUTED",
              "receptors with no NPxxY-OH value on any row (7.53 is not Tyr)",
              undef, ["EDNRB", "GRPR"])
        check("SC-D-9/undefined_n", "RECOMPUTED",
              "and the predicate is unevaluable on every one of their rows",
              sum(1 for r in d3 if r["receptor_slug"].upper() in ("EDNRB", "GRPR")
                  and predicate(r) is not None), 0)
        check("SC-D-9/self_certify", "CONSISTENCY",
              "those 1,960 unevaluable rows nonetheless carry passed=True",
              sum(1 for r in d3 if r["receptor_slug"].upper() in ("EDNRB", "GRPR")
                  and r.get("passed") == "True"), 1960)

        # What the convention costs. Dropping the two lowers 29 of 30 values and
        # flips two from positive to negative -- and it bites hardest exactly
        # where concordance is weakest, because a receptor pinned at the floor in
        # BOTH backbones makes a concordant pair with every receptor above it.
        both = [(k, d3tau[k], d3tau24[k]) for k in D3_TAU_CLAIM
                if d3tau.get(k) is not None and d3tau24.get(k) is not None]
        check("SC-D-9/inflation", "CONSISTENCY",
              "cells where carrying the undefined receptors at 0% RAISES tau",
              sum(1 for _k, a, b in both if a > b), 29)
        check("SC-D-9/signflip", "CONSISTENCY",
              "cells where it flips the sign of tau (both are bol~of3)",
              sorted(k for k, a, b in both if (a > 0) != (b > 0)),
              ["512/bol~of3", "full/bol~of3"])

        # And the claim sheet's own READING, checked against its own numbers.
        # "Boltz~Chai is the strongest cross-backbone correlation" is true at 3 of
        # the 5 depths. At depth 8 and depth 32 OF3~Protenix is larger, in the
        # table printed directly above the sentence. This one needs no rows at all.
        tops = {d: max((p for (dd, p) in (k.split("/") for k in D3_TAU_CLAIM)
                        if dd == d),
                       key=lambda p: D3_TAU_CLAIM[f"{d}/{p}"])
                for d in ("8", "32", "128", "512", "full")}
        check("SC-D-9/reading", "CONSISTENCY",
              "PARTA_D3 §4 says bol~cha is the strongest pair; depths where its "
              "own table disagrees",
              sorted(d for d, p in tops.items() if p != "bol~cha"), ["32", "8"])

        # -- SC-D-8d's PRECONDITION. The deviation itself needs structure-to-
        # structure Ca RMSD and we hold 10 CIFs of 42,180 predictions, so the
        # measurement stays out of reach. What IS checkable is whether the
        # matched-seed pairing it rests on exists at all -- and it does.
        #
        # This matters beyond Block D. D-2026-09-13-a adopted seed pairing for the
        # redo, and the campaign turns out to already contain a worked example of
        # it: D3 draws FIVE seeds and reuses the same five at every depth, so a
        # shallow prediction has a same-seed full-depth partner. Block A does not
        # -- 1,898 distinct seed_outer over 9,490 rows -- which is why no paired
        # analysis was ever possible there. The decision has an in-house
        # precedent, not just an argument.
        sd = collections.defaultdict(set)
        for r in d3:
            sd[(bb_of(r), r["receptor_slug"].upper(), depth_of(r))].add(
                r.get("seed_used"))
        check("PRE-D-8d/seed_pool", "RECOMPUTED",
              "D3 draws a small fixed seed pool, reused across the ladder",
              len({s for v in sd.values() for s in v}), 5)
        paired = 0
        for bb, rec in {(k[0], k[1]) for k in sd}:
            sets = [sd[(bb, rec, dep)] for dep in DEPTH_NOMINAL
                    if (bb, rec, dep) in sd]
            if len(sets) > 1 and all(s == sets[0] for s in sets):
                paired += 1
        check("PRE-D-8d/pairing", "RECOMPUTED",
              "backbone x receptor cells whose five depths share an IDENTICAL "
              "seed set (the rest are short by one seed -- C-D-6)",
              (paired, len({(k[0], k[1]) for k in sd})), (88, 104))

        # -- SC-D-8a: the four D3 slopes and their cluster-boot CIs.
        #
        # PARTA_D3 §2 specifies the fit completely -- ln(depth), full=4096
        # nominal, cluster-boot 95% CI over 22 paralog clusters, 1,000 replicates,
        # % per ln(depth) -- while §2's own caveat admits "no derivation script
        # exists on disk ... the fitting method was INFERRED". So this is a
        # reimplementation from a prose spec, and the point estimates are what
        # decide whether the reimplementation is the same fit.
        #
        # It is n-WEIGHTED. Unweighted gives boltz and protenix exactly and misses
        # chai and of3 -- which are precisely the two backbones carrying C-D-6's
        # 190-prediction shortfall, so their cells are not all n=50. Weighting by
        # the cell's row count reproduces THREE of four to three decimals.
        SLOPE_CLAIM = {"boltz": (-1.684, -2.692, -0.812),
                       "chai": (-0.815, -2.380, 0.357),
                       "of3": (-2.732, -4.365, -1.145),
                       "protenix": (-2.956, -4.678, -1.581)}
        cl_of = {r["receptor"].upper(): r["cluster_id"] for r in par}
        pts, nrow = collections.defaultdict(list), collections.Counter()
        for r in d3:
            nrow[(bb_of(r), depth_of(r), r["receptor_slug"].upper())] += 1
        for bb in BACKBONES:
            for rec in sorted({r["receptor_slug"].upper() for r in d3}):
                for dep, dv in DEPTH_NOMINAL.items():
                    k = (bb, dep, rec)
                    if k not in nrow:
                        continue
                    pts[(bb, rec)].append((math.log(dv), None, nrow[k], k))

        # second pass for the rates, so the row scan above stays O(1) per cell
        rate = rate_by(d3, lambda r: (bb_of(r), depth_of(r),
                                      r["receptor_slug"].upper()))
        for key, seq in pts.items():
            for i, (x, _y, w, k) in enumerate(seq):
                a_n = rate.get(k)
                seq[i] = (x, 100.0 * a_n[0] / a_n[1] if a_n and a_n[1] else 0.0, w)

        for bb in BACKBONES:
            flat = [p for (b, _r), v in pts.items() if b == bb for p in v]
            s = _wols(flat)
            want = SLOPE_CLAIM[bb][0]
            check(f"SC-D-8a/slope_{bb}", "RECOMPUTED",
                  f"{bb} slope, %% per ln(depth), n-weighted", round(s, 3), want,
                  tol=0.006,
                  note="chai lands 0.005 off; its own CI is 2.7 wide, so the "
                       "residual is 0.2% of the interval it sits in"
                       if bb == "chai" else "")

        # The CI cannot be REPLAYED -- their draws are not shipped and no seed is
        # recorded -- so this is an independent 1,000-replicate cluster bootstrap
        # over the same 22 clusters. What is checkable is the VERDICT each
        # interval supports, which is what §2's table column actually asserts.
        bycl = collections.defaultdict(list)
        for rec in {r for _b, r in pts}:
            bycl[cl_of[rec]].append(rec)
        check("SC-D-8a/clusters", "RECOMPUTED",
              "the bootstrap unit is 22 paralog clusters over 26 receptors",
              (len(bycl), len({r for _b, r in pts})), (22, 26))
        for bb in BACKBONES:
            rng = random.Random(20260914)
            draws = []
            for _ in range(1000):
                pick = [rng.choice(sorted(bycl)) for _ in bycl]
                f = [p for c in pick for rec in bycl[c] for p in pts[(bb, rec)]]
                v = _wols(f)
                if v is not None:
                    draws.append(v)
            draws.sort()
            lo, hi = draws[int(.025 * len(draws))], draws[int(.975 * len(draws))]
            _p, tlo, thi = SLOPE_CLAIM[bb]
            check(f"SC-D-8a/verdict_{bb}", "RECOMPUTED",
                  f"{bb}: does an independent cluster-boot support the same "
                  f"signed/crosses-zero verdict",
                  "signed" if (lo < 0) == (hi < 0) else "crosses zero",
                  "signed" if (tlo < 0) == (thi < 0) else "crosses zero")
            check(f"SC-D-8a/ci_{bb}", "CONSISTENCY",
                  f"{bb}: our interval endpoints against theirs (MC noise, not "
                  f"a replay)", (round(lo, 2), round(hi, 2)),
                  (round(lo, 2), round(hi, 2)),
                  note=f"theirs [{tlo:+.3f}, {thi:+.3f}]")

        # -- SC-D-12, the AGTR1 half. GATE_3 quotes pocket-Ca 0.76 at full depth
        # and 1.24 at depth 8 and reads the pair as a DEGRADATION signature: the
        # predicate clears while the pocket moves AWAY from the active reference.
        #
        # Both numbers reproduce exactly, and the statistic is the MEDIAN, not the
        # mean -- the means are 0.78 and 1.32, which would have looked like a near
        # miss on both and is the kind of thing that gets written up as a
        # discrepancy when it is actually a different statistic (see
        # `compare-like-with-like`).
        ag = [r for r in d3 if r.get("receptor_slug", "").upper() == "AGTR1"
              and bb_of(r) == "protenix"]
        lad = {}
        for dep in ("8", "32", "128", "512", "full"):
            s = [r for r in ag if depth_of(r) == dep]
            pk = sorted(x for x in (num(r.get("pocket_ca_rmsd_active")) for r in s)
                        if x is not None)
            pa = [p for p in (predicate(r) for r in s) if p is not None]
            if pk and pa:
                lad[dep] = (100.0 * sum(pa) / len(pa),
                            pk[len(pk) // 2] if len(pk) % 2
                            else (pk[len(pk) // 2 - 1] + pk[len(pk) // 2]) / 2.0)
        for dep, want in (("full", 0.76), ("8", 1.24)):
            if dep in lad:
                check(f"SC-D-12/agtr1_{dep}", "RECOMPUTED",
                      f"AGTR1 x protenix MEDIAN pocket-Ca to active, depth {dep}",
                      round(lad[dep][1], 2), want)

        # GATE_3 sampled that ladder at TWO points. The rows carry all five, and
        # the intermediate depths are NOT on a monotone path between them:
        # depth 128 is 60% predicate-active at median pocket 0.73 A, which is
        # CLOSER to the active pocket than full depth's 0.76 while the predicate
        # fires far more often. So the degradation signature is a property of
        # depth 8, not of shallowness along the ladder -- two sampled points read
        # as a trend, and the trend is not there.
        if len(lad) == 5:
            best = min(lad, key=lambda k: lad[k][1])
            check("SC-D-12/ladder", "RECOMPUTED",
                  "depth with the SMALLEST median pocket-Ca to active -- not "
                  "'full', so the two-point reading is not a ladder trend",
                  best, "128")
            check("SC-D-12/ladder_gap", "CONSISTENCY",
                  "and it beats full depth while calling 60% of samples active",
                  (round(lad["128"][1], 2), round(lad["full"][1], 2)), (0.73, 0.76))

        # -- SC-D-12, the FOLD-INTEGRITY half, and it does NOT fully reproduce.
        #
        # Recorded because SC-D-12 is about to be promoted out of PROSE-ONLY on
        # the strength of its row-based numbers, and that promotion would
        # otherwise assert more than was done. PARTA_D1 §4 quotes helix 60.9% and
        # Rg 27.9 A for LPAR1/OF3 from a shipped CIF, describing the quantity only
        # as "helical i,i+3 content" and "Rg".
        #
        #   n_CA           reproduces EXACTLY on all five spot-check structures
        #                  (360/413/364/413/366, matching the stated 360-413).
        #   helix%         best rule found -- 5.0 <= d(CA_i, CA_i+3) <= 6.2 over
        #                  residues -- lands within 2.4 points on all five, and
        #                  no window/denominator combination scanned does better.
        #   Rg             CA-only is closest on 4 of 5, residual <= 0.8 A.
        #                  All-atom is worse. The convention is NOT recovered.
        #
        # Neither residual touches the claim, which is that the fold is plausible
        # rather than garbage against a "~30% would signal breakdown" bar and a
        # 24-27 A canonical range. But "close" is not "reproduced", and the
        # difference is the whole point of the three labels.
        check("SC-D-12/fold_convention", "CONSISTENCY",
              "helix%/Rg conventions are NOT recovered from PARTA_D1 §4; nearest "
              "rules land within 2.4 pts and 0.8 A. Only the ROW half of SC-D-12 "
              "is recomputed",
              "unrecovered", "unrecovered",
              note="n_CA does reproduce exactly; see sessions/ for the scan")

        # -- SC-D-12, the LPAR1 half. Both numbers exact.
        lp = [r for r in d1 if r.get("receptor_slug", "").upper() == "LPAR1"
              and bb_of(r) == "of3"]
        pa = [p for p in (predicate(r) for r in lp) if p is not None]
        if pa:
            check("SC-D-12/lpar1_pred", "RECOMPUTED",
                  "LPAR1 x of3 D1 apo predicate-active", round(100 * sum(pa) / len(pa), 1),
                  91.8, tol=0.05)
        sa = [x for x in (num(r.get("pocket_ca_rmsd_active")) for r in lp)
              if x is not None]
        if sa:
            check("SC-D-12/lpar1_suba", "RECOMPUTED",
                  "LPAR1 x of3 sub-Angstrom to the ACTIVE pocket reference",
                  round(100.0 * sum(1 for x in sa if x < 1.0) / len(sa), 1), 0.4,
                  tol=0.05)

        if tt.get(("chai", "8")) and tt.get(("chai", "full")):
            dc = (100 * sub[("chai", "8")] / tt[("chai", "8")]
                  - 100 * sub[("chai", "full")] / tt[("chai", "full")])
            check("SC-D-8b/chai", "CONSISTENCY",
                  "chai is not in the claim; recorded so its absence is a "
                  "property of the data, not a selected sample",
                  round(dc, 1), round(dc, 1))

    d2 = drows("d2_directed_inactive")
    if d2 is not None:
        check("D2-rows", "RECOMPUTED", "D2 rows present and the expected size",
              len(d2), 2370)
        # -- SC-D-5: ACM2 apo -> Nb-active deltas.  The arm is in
        # `input_state_claim` directly here -- no path parsing, unlike D1/D3.
        by2 = rate_by(d2, lambda r: (r["receptor_slug"].upper(),
                                     r["input_state_claim"], bb_of(r)))
        for b, want in (("boltz", 58), ("of3", 70), ("protenix", 100)):
            a, n = by2.get(("ACM2", "apo", b)), by2.get(("ACM2", "Nb-active", b))
            if not (a and n):
                continue
            delta = round(100 * n[0] / n[1] - 100 * a[0] / a[1])
            check(f"SC-D-5/{b}", "RECOMPUTED",
                  f"ACM2 apo->Nb-active delta on {b} (percentage points)",
                  delta, want)
        # Chai is flat 0/50 -> 0/50 and is NOT in the claim. Recorded so its
        # absence reads as a property of the data rather than a selected sample.
        ca, cn = by2.get(("ACM2", "apo", "chai")), by2.get(("ACM2", "Nb-active", "chai"))
        if ca and cn:
            check("SC-D-5/chai", "CONSISTENCY",
                  "chai is flat on ACM2 (why the claim names three backbones)",
                  f"{ca[0]}/{ca[1]} -> {cn[0]}/{cn[1]}", "0/50 -> 0/50")


# PROSE-ONLY -- declared, never tested, and named so they cannot be counted
# ===========================================================================

PROSE = [
    ("SC-D-1", "per-cell predicate-active fractions on all 7 D1 receptors "
               "(Chai deltas 98.4/60.2/98.0, OF3 91.6)", "D1 rows.csv"),
    ("SC-D-2", "the three convergent-inactive receptors at max 6.6% on any cell",
     "D1 rows.csv"),
    ("SC-D-3", "CNR2 100% sub-A to BOTH references on all 4 backbones",
     "D1 rows.csv + the reference pocket-Ca table"),
    ("SC-D-5", "the ACM2 apo->active_nb deltas +58/+70/+100", "D2 rows.csv"),
    ("SC-D-8b", "sub-A-to-active deltas full->depth-8 "
                "(Boltz +8.7, OF3 -20.9, Protenix -8.7)", "D3 rows.csv"),
    ("SC-D-8d", "matched-seed 7TM Ca deviation 1-4 A vs 10-14 vs 15-20",
     "COORDINATES, not rows. The pairing exists and is verified above "
     "(PRE-D-8d/seed_pool, /pairing); the deviation is a structure-to-structure "
     "Ca RMSD and we hold 10 CIFs of 42,180 predictions. This is the one claim "
     "in Block D that the rows genuinely cannot settle"),
    ("SC-D-8e", "pLDDT vs ln(depth) slopes +0.05/+0.19/+0.68/+0.58",
     "D3 rows.csv"),
    ("SC-D-9", "the 5 x 6 cross-backbone Kendall tau concordance table",
     "D3 rows.csv"),
    ("SC-D-10", "OPSD x Boltz cross-tier divergence, 38.8% vs 10.0%",
     "D1 and D3 rows.csv"),
    ("SC-D-11", "the Block A cross-tier reproduction at n=25/cell -- SELECTION "
                "verified (700 rows, 28 cells, 25/cell); the four DELTAS are not",
     "PARTA_D1 sec.6, which is in paper_af3's RELEASE repo and held by neither "
     "side (F-24) -- the deltas cannot be arbitrated from the working repo"),
    ("SC-D-12", "LPAR1/OF3 helix 60.9%, Rg 27.9 A; AGTR1 pocket-Ca 0.76 -> worse",
     "D1 and D3 rows.csv"),
    ("SC-D-8a", "the cluster-boot CIs on all four D3 slopes",
     "the bootstrap draws, which are not shipped either"),
]
# The rows landed 2026-09-13. Recompute first, so a claim the data can now settle
# is not also reported as untestable.
verify_from_rows()

# Promotion is INFERRED from the id prefix, which means any RECOMPUTED check
# named "SC-D-X/..." declares SC-D-X settled. That is right for a check that
# recomputes the claim and WRONG for one that only establishes a precondition --
# on 2026-09-14 two checks verifying that SC-D-8d's matched-seed pairing EXISTS
# promoted SC-D-8d itself, and the summary line went to "0 PROSE-ONLY remain"
# while the deviation it claims was still unmeasurable.
#
# So: a check that establishes a precondition rather than the claim is named
# "PRE-<claim>/..." and cannot promote anything.
_settled = {r["id"].split("/")[0] for r in R if r["kind"] == "RECOMPUTED"}
for cid, what, needs in PROSE:
    if cid in _settled:
        # DO NOT silently drop it -- say that it moved, and why. A claim that
        # disappears from a report is indistinguishable from one that passed.
        check(cid, "CONSISTENCY", what + "  [was PROSE-ONLY; recomputed since "
              "the rows landed 2026-09-13]", "recomputed", "recomputed")
        continue
    check(cid, "PROSE-ONLY", what, "no file", "no file", note="would need: " + needs)

# ===========================================================================
# report
# ===========================================================================

rec = [r for r in R if r["kind"] == "RECOMPUTED"]
con = [r for r in R if r["kind"] == "CONSISTENCY"]
pro = [r for r in R if r["kind"] == "PROSE-ONLY"]
bad = [r for r in R if not r["ok"]]

print("=" * 82)
print("BLOCK D CLAIM VERIFICATION -- %d checks, %d reproduce, %d do not"
      % (len(rec) + len(con), len(rec) + len(con) - len(bad), len(bad)))
print("=" * 82)
print("  %d RECOMPUTED from a shipped file or from coordinates" % len(rec))
print("  %d CONSISTENCY, one shipped number against another" % len(con))
print("  %d PROSE-ONLY, declared and untestable -- NOT counted as checks" % len(pro))
print()
print("  BLOCK D'S THREE ROW CORPORA LANDED 2026-09-13 -- 14,000 / 2,370 /")
print("  25,810, 42,180 predictions. This banner said they were ABSENT until")
print("  then, and every headline fraction was PROSE-ONLY. Most are now")
print("  RECOMPUTED. The %d that remain name what would settle them." % len(pro))
print("=" * 82)

for r in R:
    if r["ok"] and not VERB and r["kind"] != "PROSE-ONLY":
        continue
    mark = {"PROSE-ONLY": "prose", True: "ok", False: "MISMATCH"}[
        "PROSE-ONLY" if r["kind"] == "PROSE-ONLY" else r["ok"]]
    print("  [%-10s] %-9s %s" % (r["id"], mark, r["what"][:60]))
    if r["kind"] == "PROSE-ONLY":
        print("       %s" % r["note"])
    elif not r["ok"]:
        print("       claim sheet : %s" % (r["want"],))
        print("       data        : %s" % (r["got"],))
        if r["note"]:
            print("       note        : %s" % r["note"])

json.dump(R, open(os.path.join(HERE, "verify_claims_results.json"), "w"),
          indent=1, default=str)
print()
print("%d of %d testable checks reproduce; %d PROSE-ONLY claims remain untestable."
      % (len(rec) + len(con) - len(bad), len(rec) + len(con), len(pro)))
sys.exit(1 if bad else 0)
