#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recompute every checkable number in Block B's claim sheet from the shipped
tidy files. Exits 1 on any mismatch.

The point is not that everything reproduces. Block A ran 34 checks and 15 did
not reproduce; four of those were named in the brief and eleven were not. A
mismatch is a FINDING and goes in DISCREPANCY_REPORT.md. It is never silently
reconciled and the drop is never edited.

Usage:  python3 analysis/block_b/verify_claims.py [-v]
"""
from __future__ import print_function
import os, sys, json, hashlib
import pandas as pd
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B    = os.path.join(ROOT, "data", "block_b")
S    = os.path.join(ROOT, "data", "block_b_structures")
VERB = "-v" in sys.argv

RESULTS = []


def check(cid, what, got, want, tol=None, note=""):
    """Record one check. tol=None means exact/equality comparison."""
    if tol is None:
        ok = (got == want)
    else:
        try:
            ok = abs(float(got) - float(want)) <= tol
        except (TypeError, ValueError):
            ok = False
    RESULTS.append(dict(id=cid, what=what, got=got, want=want, ok=bool(ok),
                        tol=tol, note=note))
    return ok


def load(rel):
    return pd.read_csv(os.path.join(B, rel), low_memory=False)


# ---------------------------------------------------------------- the corpus
rows = load("01_rows/rows_tidy.csv")

check("B01", "rows_tidy row count", len(rows), 32000)
cells = rows.groupby(["receptor_slug", "arm", "backbone"]).size()
check("B02", "distinct (receptor,arm,backbone) cells", len(cells), 640)
check("B03", "every cell has exactly 50 rows", sorted(cells.unique().tolist()), [50])
seeds = rows.groupby(["receptor_slug", "arm", "backbone"]).seed_used.nunique()
check("B04", "every cell has 5 distinct seeds", sorted(seeds.unique().tolist()), [5])
check("B05", "rows carrying the OF3 sentinel seed 2746317213",
      int((rows.seed_used.astype(str) == "2746317213").sum()), 0)
check("B06", "rows with scorer_git_sha == 'no-git'",
      int((rows.scorer_git_sha.astype(str) == "no-git").sum()), 0)
check("B07", "single scorer_git_sha across all rows",
      rows.scorer_git_sha.nunique(), 1)
check("B08", "ref_set_csv_sha256 pinned to 6ee2cad8...",
      sorted(rows.ref_set_csv_sha256.astype(str).unique())[0][:8], "6ee2cad8")
check("B09", "receptors on the panel", rows.receptor_slug.nunique(), 40)
check("B10", "backbones", sorted(rows.backbone.unique().tolist()),
      sorted(["boltz", "chai", "of3", "protenix"]))
check("B11", "arms", sorted(rows.arm.unique().tolist()),
      sorted(["apo", "cognate", "decoy", "shuffled"]))
check("B12", "paralog clusters", rows.cluster_id.nunique(), 26)

# ------------------------------------------------------- the exclusion flags
# Claim sheet header (BLOCK_B_CLAIM_SHEET.md, "Exclusion sets applied") says:
#   E-B-1 all-NaN NPxxY (4) | E-B-2 AA2AR | E-B-3 non-native active ref (15)
#   E-B-4 ceiling-pinned cells (cognate rate >= 0.98)
# exclusion_definitions.csv and README.md say something different for 2/3/4.
CLAIM_SHEET_HEADER = {
    "excl_E_B_1": ["EDNRA", "EDNRB", "GRPR", "HRH3"],
    "excl_E_B_2": ["AA2AR"],
    "excl_E_B_3": None,   # "15 of 40, non-native active reference"
    "excl_E_B_4": None,   # "ceiling-pinned cells (cognate rate >= 0.98)"
}
defs = load("10_exclusions/exclusion_definitions.csv")
defmap = {r.flag: sorted(str(r.members).split(",")) for r in defs.itertuples()
          if r.flag != "excl_any"}

for flag, n_expected_rows in [("excl_E_B_1", 3200), ("excl_E_B_2", 1600),
                              ("excl_E_B_3", 800), ("excl_E_B_4", 12000)]:
    fired = int(rows[flag].astype(bool).sum())
    check("B13." + flag[-1], "%s fires on n rows (README)" % flag,
          fired, n_expected_rows)
    members = sorted(rows.loc[rows[flag].astype(bool), "receptor_slug"].unique().tolist())
    check("B14." + flag[-1], "%s membership == exclusion_definitions.csv" % flag,
          members, defmap[flag])

check("B15", "excl_any fires on n rows",
      int(rows.excl_any.astype(bool).sum()), 14400)

# The header's own mapping, tested against the data.
check("B16", "claim-sheet header: E-B-2 == {AA2AR}",
      sorted(rows.loc[rows.excl_E_B_2.astype(bool), "receptor_slug"].unique().tolist()),
      ["AA2AR"],
      note="header says E-B-2 is AA2AR; data says E-B-2 is the agonist-only pair")
check("B17", "claim-sheet header: E-B-3 covers 15 receptors (non-native)",
      int(rows.loc[rows.excl_E_B_3.astype(bool), "receptor_slug"].nunique()), 15,
      note="header says E-B-3 is the 15 non-native; data says E-B-3 is AA2AR alone")

# Is there ANY column behind "ceiling-pinned cells (cognate rate >= 0.98)"?
cog = rows[rows.arm == "cognate"]
pred_cog = ((cog.d_npxxy_y558_y753_oh < cog.threshold_npxxy_oh_active_lt) &
            (cog.d_gpcrdb_tm6_tilt_246_637_ca > cog.threshold_gpcrdb_tm6_tilt_active_gt))
cog_rate = pred_cog.groupby([cog.receptor_slug, cog.backbone]).mean()
pinned_per_bb = (cog_rate >= 0.98).groupby(level=1).sum()
check("B18", "cognate cells pinned >= 0.98, per backbone, C-B-7 says 24-34 of 40",
      bool(pinned_per_bb.min() >= 24 and pinned_per_bb.max() <= 34), True,
      note="observed %s" % pinned_per_bb.to_dict())

# ------------------------------------------------------------ the instrument
th_n = rows.threshold_npxxy_oh_active_lt.dropna().unique()
th_t = rows.threshold_gpcrdb_tm6_tilt_active_gt.dropna().unique()
check("B19", "one NPxxY threshold on every row", len(th_n), 1)
check("B20", "NPxxY threshold value", round(float(th_n[0]), 3), 9.082, tol=1e-9)
check("B21", "one tilt threshold on every row", len(th_t), 1)
check("B22", "tilt threshold value", round(float(th_t[0]), 3), 14.932, tol=1e-9)

E1 = ["EDNRA", "EDNRB", "GRPR", "HRH3"]
check("B23", "E-B-1 receptors have all-NaN NPxxY-OH",
      int(rows.loc[rows.receptor_slug.isin(E1), "d_npxxy_y558_y753_oh"].notna().sum()), 0)


def predicate(df):
    return ((df.d_npxxy_y558_y753_oh < df.threshold_npxxy_oh_active_lt) &
            (df.d_gpcrdb_tm6_tilt_246_637_ca > df.threshold_gpcrdb_tm6_tilt_active_gt))


f36 = rows[~rows.receptor_slug.isin(E1)].copy()
check("B24", "frame_36 receptor count", f36.receptor_slug.nunique(), 36)
f36["active"] = predicate(f36)

# ------------------------------------------------ SC-B-1, the ladder itself
LADDER = {"apo": 0.158, "decoy": 0.558, "shuffled": 0.809, "cognate": 0.891}
# panel-level = mean over receptors of the per-receptor rate (per-receptor
# normalised, as the claim sheet and FIGURE_BRIEF describe it)
for arm, want in LADDER.items():
    sub = f36[f36.arm == arm]
    per_recep = sub.groupby("receptor_slug")["active"].mean()
    check("B25." + arm, "SC-B-1 %s binary predicate (frame_36, per-receptor mean)" % arm,
          round(float(per_recep.mean()), 3), want, tol=0.0005)

check("B26", "SC-B-1 decoy is 0.558 and NOT the superseded 0.552",
      round(float(f36[f36.arm == "decoy"].groupby("receptor_slug")["active"].mean().mean()), 3)
      != 0.552, True)

mono_ok = True
for bb in sorted(f36.backbone.unique()):
    sub = f36[f36.backbone == bb]
    r = {a: sub[sub.arm == a].groupby("receptor_slug")["active"].mean().mean()
         for a in ["apo", "decoy", "shuffled", "cognate"]}
    ordered = r["apo"] < r["decoy"] < r["shuffled"] < r["cognate"]
    check("B27." + bb, "SC-B-1 ladder monotonic on %s independently" % bb,
          bool(ordered), True,
          note="%.3f < %.3f < %.3f < %.3f" % (r["apo"], r["decoy"], r["shuffled"], r["cognate"]))
    mono_ok = mono_ok and ordered

CONT_NPXXY = {"apo": 11.30, "decoy": 8.19, "shuffled": 7.31, "cognate": 6.60}
CONT_TILT  = {"apo": 13.05, "decoy": 15.61, "shuffled": 16.42, "cognate": 16.75}
cont = load("04_ladder/ladder_continuous_distributions.csv")
check("B27z", "ladder_continuous_distributions.csv carries a panel row",
      "panel" in [str(x) for x in cont.backbone.unique()], True,
      note="claim_answers.csv names this file as the source of the 8 medians; "
           "it holds only the four per-backbone strata")
for arm in CONT_NPXXY:
    sub = f36[f36.arm == arm]
    # best of every defensible aggregation, so a miss is not an aggregation choice
    cands_n = [sub.d_npxxy_y558_y753_oh.median(),
               sub.groupby("receptor_slug").d_npxxy_y558_y753_oh.median().median(),
               sub.groupby("receptor_slug").d_npxxy_y558_y753_oh.median().mean(),
               cont[(cont.arm == arm) & (cont.axis == "d_npxxy_y558_y753_oh")].p50.median()]
    cands_t = [sub.d_gpcrdb_tm6_tilt_246_637_ca.median(),
               sub.groupby("receptor_slug").d_gpcrdb_tm6_tilt_246_637_ca.median().median(),
               sub.groupby("receptor_slug").d_gpcrdb_tm6_tilt_246_637_ca.median().mean(),
               cont[(cont.arm == arm) & (cont.axis == "d_gpcrdb_tm6_tilt_246_637_ca")].p50.median()]
    bn = min(cands_n, key=lambda v: abs(float(v) - CONT_NPXXY[arm]))
    bt = min(cands_t, key=lambda v: abs(float(v) - CONT_TILT[arm]))
    check("B28." + arm, "SC-B-1 continuous NPxxY-OH median, %s (closest of 4 aggregations)" % arm,
          round(float(bn), 2), CONT_NPXXY[arm], tol=0.005,
          note="all four: %s" % [round(float(v), 2) for v in cands_n])
    check("B29." + arm, "SC-B-1 continuous tilt median, %s (closest of 4 aggregations)" % arm,
          round(float(bt), 2), CONT_TILT[arm], tol=0.005,
          note="all four: %s" % [round(float(v), 2) for v in cands_t])

# the shipped ladder table should agree with the recomputation
lfs = load("04_ladder/ladder_four_scorings.csv")
lfs36 = lfs[(lfs.frame == "frame_36") & (lfs.backbone.astype(str).str.lower() == "panel")]
if len(lfs36) == 0:                      # panel rows may be labelled differently
    lfs36 = lfs[(lfs.frame == "frame_36")]
for arm, want in LADDER.items():
    r = lfs36[lfs36.arm == arm]
    if len(r):
        check("B30." + arm, "ladder_four_scorings.csv binary_predicate, %s" % arm,
              round(float(r.binary_predicate.iloc[0]), 3), want, tol=0.0005)

# ------------------------------------------- SC-B-2, the decomposition shares
dec = load("05_decomposition/ladder_decomposition.csv")
# NOTE: this file labels its frames all_40 / reproduction_36, NOT frame_40 /
# frame_36 as the claim sheet and every other table do. An earlier version of
# this script filtered on "frame_36", got an empty frame, and every
# decomposition check below SILENTLY DID NOT RUN behind an `if len(m):` guard.
# A check that vanishes is worse than a check that fails. Missing rows now fail.
check("B30z", "ladder_decomposition.csv uses the claim sheet's frame labels",
      sorted(dec.frame.unique().tolist()), ["frame_36", "frame_40"],
      note="it ships all_40 / reproduction_36; every other table says frame_36")
d36 = dec[dec.frame == "reproduction_36"]
CONTRAST = {"occupancy": "delta_occupancy_apo_to_decoy",
            "alpha5ct": "delta_a5ct_sequence_decoy_to_shuffled",
            "family": "delta_correct_family_shuffled_to_cognate"}
PROB = {"occupancy": (0.400, 54.6), "alpha5ct": (0.252, 34.3), "family": (0.082, 11.1)}
LOGIT = {"occupancy": (1.907, 50.5), "alpha5ct": (1.214, 32.1), "family": (0.656, 17.4)}

for scale, TAB in (("probability", PROB), ("logit", LOGIT)):
    for key, (est, share) in TAB.items():
        m = d36[(d36.scale == scale) & (d36.contrast == CONTRAST[key]) &
                (d36.backbone == "panel")]
        tag = "B31" if scale == "probability" else "B33"
        if len(m) != 1:
            check(tag + "." + key, "SC-B-2 %s panel row for %s exists" % (scale, key),
                  len(m), 1)
            continue
        check(tag + "." + key, "SC-B-2 %s-scale term, %s" % (scale, key),
              round(float(m.term_estimate.iloc[0]), 3), est, tol=0.0015)
        check(tag + "b." + key, "SC-B-2 %s-scale share %%, %s" % (scale, key),
              round(100.0 * float(m.term_share.iloc[0]), 1), share, tol=0.15)

# the per-backbone claim: "all four backbones agree, 17-21%"
PER_BB = {"boltz": 17.4, "chai": 17.5, "of3": 20.9, "protenix": 17.5}
for bb, want in PER_BB.items():
    m = d36[(d36.scale == "logit") & (d36.contrast == CONTRAST["family"]) &
            (d36.backbone == bb)]
    check("B32." + bb, "SC-B-2 per-backbone logit family share %%, %s" % bb,
          round(100.0 * float(m.term_share.iloc[0]), 1) if len(m) else None,
          want, tol=0.15)

# "Protenix logit CI [0.35, 1.05] squarely positive"
m = d36[(d36.scale == "logit") & (d36.contrast == CONTRAST["family"]) &
        (d36.backbone == "protenix")]
check("B32z", "SC-B-2 Protenix logit family CI excludes zero",
      bool(float(m.ci_lo.iloc[0]) > 0) if len(m) else None, True,
      note=("shipped CI is [%.3f, %.3f]" % (m.ci_lo.iloc[0], m.ci_hi.iloc[0]))
           if len(m) else "no row")

check("B35", "SC-B-2 shares are 55/34/11 and NOT the superseded 54/35/11",
      [round(PROB[k][1]) for k in ["occupancy", "alpha5ct", "family"]],
      [55, 34, 11])

# ------------------------------------------------------- SC-B-3, the 2x2
i2 = load("06_interface/interface_2x2.csv")
sel = i2[(i2.frame == "frame_36") & (i2.cutoff_A == 20)]
TRIPLES = {"cognate": (0.9983, 0.8926), "shuffled": (0.9674, 0.8353),
           "decoy": (0.7037, 0.6647)}
for arm, (pe, pa) in TRIPLES.items():
    r = sel[(sel.arm == arm) & (sel.backbone == "panel_all") &
            (sel.predicate == "two_instrument")]
    if len(r):
        check("B36." + arm, "SC-B-3 p(engaged), %s" % arm,
              round(float(r.p_engaged.iloc[0]), 4), pe, tol=0.0006)
        check("B37." + arm, "SC-B-3 p(active|engaged), %s" % arm,
              round(float(r.p_active_given_engaged.iloc[0]), 4), pa, tol=0.0006)

dec_ebi = sel[(sel.arm == "decoy") & (sel.predicate == "two_instrument")]
tot_ebi = dec_ebi[dec_ebi.backbone == "panel_all"].n_engaged_but_inactive
check("B38", "SC-B-3 decoy engaged-but-inactive, panel_all",
      int(tot_ebi.iloc[0]) if len(tot_ebi) else -1, 1699)
per_bb = dec_ebi[dec_ebi.backbone != "panel_all"].n_engaged_but_inactive
if len(per_bb):
    check("B39", "SC-B-3 engaged-but-inactive per backbone within 278-540",
          bool(per_bb.min() >= 278 and per_bb.max() <= 540), True,
          note="observed %d-%d" % (per_bb.min(), per_bb.max()))

# -------------------------------------------------- SC-B-4, the PIF connector
pif = load("06_interface/interface_pif_connector.csv")
PIF = {
    "apo_all":               (160, 15.35),
    "cognate_active_engaged": (130, 16.04),
    "shuffled_active_engaged": (118, 16.00),
    "decoy_active_engaged":   (69, 16.03),
    "decoy_engaged_but_inactive": (47, 15.42),
}
subsets = {
    "apo_all": pif[pif.arm == "apo"],
    "cognate_active_engaged": pif[(pif.arm == "cognate") & pif.cell_active.astype(bool) & pif.cell_engaged_20.astype(bool)],
    "shuffled_active_engaged": pif[(pif.arm == "shuffled") & pif.cell_active.astype(bool) & pif.cell_engaged_20.astype(bool)],
    "decoy_active_engaged": pif[(pif.arm == "decoy") & pif.cell_active.astype(bool) & pif.cell_engaged_20.astype(bool)],
    "decoy_engaged_but_inactive": pif[(pif.arm == "decoy") & pif.cell_engaged_but_inactive.astype(bool)],
}
for k, (n, med) in PIF.items():
    sub = subsets[k]
    check("B40." + k, "SC-B-4 n cells, %s" % k, int(len(sub)), n)
    if len(sub):
        check("B41." + k, "SC-B-4 median pif_sum_ca, %s" % k,
              round(float(sub.pif_sum_ca.median()), 2), med, tol=0.005)

# --------------------------------------------------- SC-B-5, fold integrity
fi = load("06_interface/interface_fold_integrity.csv")
if "tm6_helicity_6_30_6_50" in rows.columns:
    passrate = float((rows.tm6_helicity_6_30_6_50 >= 0.80).mean())
    check("B42", "SC-B-5 panel-wide TM6 helicity pass rate",
          round(passrate, 3), 0.988, tol=0.0015)
    cellmin = (rows.assign(p=rows.tm6_helicity_6_30_6_50 >= 0.80)
               .groupby(["arm", "backbone"]).p.mean().min())
    check("B43", "SC-B-5 worst arm x backbone cell pass rate",
          round(float(cellmin), 3), 0.941, tol=0.0015)

# ----------------------------------------------- SC-B-6, the donor residuals
pw = load("07_donor_residuals/phase5_power_analysis.csv")
g = pw[(pw.backbone == "panel") & (pw.donor_ga_class == "Gs") &
       (pw.cognate_ga_class == "Gi") & (pw.axis == "residual_tilt")]
if len(g):
    g = g.iloc[0]
    check("B44", "SC-B-6 Gs->Gi tilt residual, all receptors",
          round(float(g.all_median), 3), 0.024, tol=0.0015)
    check("B45", "SC-B-6 Gs->Gi n_receptors, all", int(g.total_n_rec), 24)
    check("B46", "SC-B-6 Gs->Gi tilt residual, native only",
          round(float(g.native_median), 3), -0.062, tol=0.0015)
    check("B47", "SC-B-6 Gs->Gi n_receptors, native only", int(g.native_n_rec), 20)
    check("B47b", "SC-B-6 native-only CI [-0.41, +0.21]",
          [round(float(g.native_ci_lo), 2), round(float(g.native_ci_hi), 2)],
          [-0.41, 0.21])
    check("B47c", "SC-B-6 CI spans zero, so NOT an equivalence result",
          bool(g.native_ci_lo < 0 < g.native_ci_hi), True)

# ------------------------------------------------- SC-B-13, reference audit
ra = load("09_references/reference_audit.csv")
check("B48", "SC-B-13 reference audit row count", len(ra), 80)
act = ra[ra.role.astype(str).str.lower() == "active"]
cls = act.activation_class.value_counts().to_dict()
for name, want in [("Ga-complexed-native", 25), ("Ga-complexed-chimera-or-miniG", 10),
                   ("nanobody-stabilised", 3), ("agonist-only-no-partner", 2)]:
    check("B49." + name, "SC-B-13 activation_class count, %s" % name,
          int(cls.get(name, 0)), want)
nonnat = int((act.active_stabilization_source.astype(str) != "native").sum())
check("B50", "SC-B-13 non-native active references", nonnat, 15)
check("B51", "SC-B-13 non-native fraction %", round(100.0 * nonnat / max(len(act), 1), 1), 37.5,
      tol=0.05)

# no native heterotrimeric Gs anywhere in the Class A active set (Methods claim)
check("B52", "no native heterotrimeric Gs among Class A active references (dispatch 2.4)",
      int(((act.active_stabilization_source.astype(str) == "native") &
           (act.alpha5_donor_class.astype(str).str.lower().str.contains("gs|alphas"))).sum()),
      0)

# ------------------------------------- the structure bundle (second zip)
sm = os.path.join(S, "03_engagement_trio", "per_structure_metrics.csv")
if os.path.exists(sm):
    psm = pd.read_csv(sm)
    check("B53", "structure bundle: engagement trio metrics present", len(psm) > 0, True)

# GHSR's own decoy rate, which the addendum forbids using as the panel ladder
ghsr = rows[(rows.receptor_slug == "GHSR") & (rows.arm == "decoy")].copy()
if len(ghsr):
    ghsr["active"] = predicate(ghsr)
    check("B54", "GHSR decoy arm rate (four-backbone mean), addendum says 0.175",
          round(float(ghsr.groupby("backbone")["active"].mean().mean()), 3), 0.175, tol=0.0015)

# ------------------- the structure addendum's own numbers, panel vs GHSR
import glob, hashlib
n_ok = n_bad = 0
for f in sorted(glob.glob(os.path.join(S, "0[2-4]*", "**", "*.cif"), recursive=True)):
    h = hashlib.sha256(open(f, "rb").read()).hexdigest()
    stem = os.path.basename(f).replace(".cif", "").split("_")[-1]
    n_ok += h.startswith(stem)
    n_bad += (not h.startswith(stem))
check("B55", "every predicted CIF's own sha256 matches its filename stem",
      [n_ok, n_bad], [11, 0])

dec = rows[rows.arm == "decoy"].copy()
dec["active"] = predicate(dec)
c2 = dec[(dec.d_ga_alpha5_r350_ca < 20) & (~dec["active"])]
c2_boltz_panel = float(c2[c2.backbone == "boltz"].d_ga_alpha5_r350_ca.median())
c2_boltz_ghsr = float(c2[(c2.backbone == "boltz") &
                         (c2.receptor_slug == "GHSR")].d_ga_alpha5_r350_ca.median())
check("B56", "addendum 3: C2 median tip depth on boltz = 18.81 A, read PANEL-wide",
      round(c2_boltz_panel, 2), 18.81, tol=0.005,
      note="GHSR-only boltz C2 median is %.2f, which is where 18.81 comes from"
           % c2_boltz_ghsr)
check("B57", "addendum 3: the same number read as GHSR-only",
      round(c2_boltz_ghsr, 2), 18.81, tol=0.005)

cogtip = rows[rows.arm == "cognate"]
check("B58", "addendum 3: cognate median depth 12.3-12.6 A, read PANEL-wide",
      bool(12.3 <= float(cogtip.d_ga_alpha5_r350_ca.median()) <= 12.6), True,
      note="panel cognate median is %.2f (SC-B-3 says 12.19); GHSR-only is %.2f"
           % (cogtip.d_ga_alpha5_r350_ca.median(),
              cogtip[cogtip.receptor_slug == "GHSR"].d_ga_alpha5_r350_ca.median()))
check("B59", "SC-B-3 cognate median depth 12.19 A", 
      round(float(cogtip.d_ga_alpha5_r350_ca.median()), 2), 12.19, tol=0.005)

b_c2 = c2[c2.backbone == "boltz"].d_ga_alpha5_r350_ca
check("B60", "the shipped boltz C2 structure (18.730 A) is typical of the PANEL C2 subset",
      bool(30 <= 100.0 * float((b_c2 < 18.730).mean()) <= 70), True,
      note="it sits at the %.1fth percentile of the panel boltz C2 rows, "
           "and at the 50.0th of GHSR's own" % (100.0 * (b_c2 < 18.730).mean()))

# ------------------------------------------------------------------- report
ok = [r for r in RESULTS if r["ok"]]
bad = [r for r in RESULTS if not r["ok"]]

print("=" * 78)
print("BLOCK B CLAIM VERIFICATION  --  %d checks, %d reproduce, %d do not"
      % (len(RESULTS), len(ok), len(bad)))
print("=" * 78)
if bad:
    print("\nDO NOT REPRODUCE (each is a finding for DISCREPANCY_REPORT.md):\n")
    for r in bad:
        print("  [%-12s] %s" % (r["id"], r["what"]))
        print("      claim sheet : %s" % (r["want"],))
        print("      data        : %s" % (r["got"],))
        if r["note"]:
            print("      note        : %s" % r["note"])
        print("")
if VERB:
    print("\nREPRODUCE:\n")
    for r in ok:
        print("  [%-12s] %s  = %s" % (r["id"], r["what"], r["got"]))

json.dump(RESULTS, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "verify_claims_results.json"), "w"),
          indent=1, default=str)
sys.exit(1 if bad else 0)
