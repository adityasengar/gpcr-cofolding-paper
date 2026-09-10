#!/usr/bin/env python3
"""Verify Block D's claim sheet against what Block D actually shipped.

THE FACT THAT SHAPES THIS ENTIRE FILE: **Block D ships no row-level data.**

The claim sheet names three corpora --
`experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` and its D2 and D3
siblings, 42,180 predictions between them -- and not one of them is in the
bundle. Five CSVs ship in total, all of them panel or reference metadata. So
almost every number in SC-D-1..12 is a number in a sentence, and no arithmetic
performed here can turn it into a measurement.

Block C shipped one row-level file and 30 of its 53 checks were
consistency-only. Block D ships zero, and the split is worse. Every check below
therefore carries one of THREE labels, and the label is the point:

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
can never be read as "N claims are verified".

Usage:  python3 analysis/block_d/verify_claims.py [-v]
Exit 1 on any RECOMPUTED or CONSISTENCY mismatch. PROSE-ONLY never fails --
it is a census of what cannot be tested, not a test.
"""
from __future__ import print_function

import csv
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
D = os.path.join(ROOT, "data", "block_d")
VERB = "-v" in sys.argv
R = []


def check(cid, kind, what, got, want, tol=None, note=""):
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
     "D3 rows.csv + the matched-seed pairing"),
    ("SC-D-8e", "pLDDT vs ln(depth) slopes +0.05/+0.19/+0.68/+0.58",
     "D3 rows.csv"),
    ("SC-D-9", "the 5 x 6 cross-backbone Kendall tau concordance table",
     "D3 rows.csv"),
    ("SC-D-10", "OPSD x Boltz cross-tier divergence, 38.8% vs 10.0%",
     "D1 and D3 rows.csv"),
    ("SC-D-11", "the Block A cross-tier reproduction at n=25/cell",
     "Block A rows joined to the D1 outlier cells"),
    ("SC-D-12", "LPAR1/OF3 helix 60.9%, Rg 27.9 A; AGTR1 pocket-Ca 0.76 -> worse",
     "D1 and D3 rows.csv"),
    ("SC-D-8a", "the cluster-boot CIs on all four D3 slopes",
     "the bootstrap draws, which are not shipped either"),
]
for cid, what, needs in PROSE:
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
print("  BLOCK D SHIPS NO ROW-LEVEL DATA. All three corpora named in the claim")
print("  sheet -- 42,180 predictions -- are absent. Every headline fraction,")
print("  every sub-Angstrom percentage and every slope CI is PROSE-ONLY.")
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
