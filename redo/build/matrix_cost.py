#!/usr/bin/env python3
"""
matrix_cost.py -- the cost arithmetic behind redo/RUN_MATRIX.md.

Everything here is a count of predictions, derived from an explicit product of
axis sizes. The only empirical cost constant is the D3 drain, which is the one
measured GPU throughput anywhere in the four blocks:

    data/block_d/07_partA/HEADLINE_D3_tier_d3_full_2026_09_08.md:3-6
    "D3 full drained 2581/2600 rows (99.3 %) on 25 H100 workers in
     ~6.5 h wall ... rescored to 25,810 predictions"

    25,810 preds / 6.5 h / 25 workers = 158.8 preds per H100-hour
                                      = 22.66 s per prediction per H100

D3 is APO ONLY -- one receptor chain, median 380 Ca. A receptor + Ga complex is
roughly 380 + 394 = 774 tokens. The only other cost figure on disk is a PLANNING
estimate for a two-chain grid, never validated:

    data/block_d/05_state_check/BLOCK_D_S2_4_POST_CUTOFF_SCOPING.md:99-100
    "600 preds x ~5 min/pred on H100 = ~50 GPU-hours"

That is 13.2x the measured apo rate. The truth is somewhere between, and
closing that bracket is ask P1 in RUN_MATRIX.md.

    python3 redo/build/matrix_cost.py
"""
import os
import sys

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo

# ---------------------------------------------------------------- constants
# measured, data/block_d/07_partA/HEADLINE_D3_tier_d3_full_2026_09_08.md:3-6
D3_PREDS, D3_HOURS, D3_WORKERS = 25810, 6.5, 25
SEC_PER_PRED_APO = D3_HOURS * 3600 * D3_WORKERS / D3_PREDS

# scenarios for a two-chain (receptor + partner) prediction, as multiples of
# the measured apo rate. All three are ESTIMATES; only the apo rate is measured.
SCEN = {
    "linear  (2.0x, token count)":        2.0,
    "quadratic (4.2x, pairformer L^2)":   (774 / 380) ** 2,
    "planning (13.2x, D S2.4 5 min/pred)": 300.0 / SEC_PER_PRED_APO,
}

BLOCK_B = 32_000           # one delivered drop, the natural budget unit
DELIVERED = {"A": 9_490, "B": 32_000, "C": 40_800, "D": 42_180}

# ------------------------------------------------------------------- panels
# Sizes and cluster counts from the sibling redo/spec/PANEL.md section 5,
# except CORE-L17 which is recomputed here from Block C's delivered ligand roles
# intersected with Block B's measurable receptors (25 receptors, 17 clusters).
PANELS = {
    "CORE-32": 32,   # one receptor per paralog cluster of C1 -> 32 clusters
    "CORE-L17": 17,  # ligand-complete one-per-cluster        -> 17 clusters
    "C1": 64,        # PANEL.md tier C1, the full core        -> 32 clusters
    "C1r": 29,       # PANEL.md tier C1r, reduced core        -> 21 clusters
    "H-B": 12,       # PANEL.md tier H, Boltz-2 stratum       ->  8 clusters
    "E-pro": 8,      # PANEL.md tier E-pro, prospective       ->  8 clusters
    "E-B1": 5,       # PANEL.md tier E-B1, class B transfer   ->  4 clusters
}
CLUSTERS = {"CORE-32": 32, "CORE-L17": 17, "C1": 32, "C1r": 21,
            "H-B": 8, "E-pro": 8, "E-B1": 4}

# ------------------------------------------------------- the full factorial
def factorial():
    print("== 1. the full factorial, priced ==")
    axes_core = [("receptor (C1 census)", 64), ("backbone", 4),
                 ("partner rung R0-R6", 7), ("ligand class", 4),
                 ("MSA depth", 5), ("predictions per cell", 50)]
    axes_all = [("receptor (C1 census)", 64), ("backbone", 4),
                ("partner arm incl. controls", 22), ("ligand class", 4),
                ("MSA depth", 5), ("predictions per cell", 50)]
    for label, axes in (("core ladder only", axes_core),
                        ("ladder + every catalogue control arm", axes_all)):
        tot = 1
        parts = []
        for name, n in axes:
            tot *= n
            parts.append(f"{n}")
        print(f"  {label}")
        print(f"    " + " x ".join(parts) + f" = {tot:,} predictions")
        for name, n in axes:
            print(f"      {n:>4}  {name}")
        print(f"    = {tot/BLOCK_B:,.0f} Block-B drops "
              f"= {tot/sum(DELIVERED.values()):,.1f}x everything ever delivered")
        for sname, mult in SCEN.items():
            h = tot * SEC_PER_PRED_APO * mult / 3600
            print(f"      {sname:36s} {h:>10,.0f} H100-h "
                  f"= {h/D3_WORKERS/24:>6,.0f} days wall on {D3_WORKERS} H100")
        print()
    print(f"  delivered to date: " +
          " + ".join(f"{k} {v:,}" for k, v in DELIVERED.items()) +
          f" = {sum(DELIVERED.values()):,}")
    print(f"  measured apo rate: {SEC_PER_PRED_APO:.2f} s/pred/H100 "
          f"({D3_PREDS/D3_HOURS/D3_WORKERS:.1f} preds/H100-h)")
    print()


# -------------------------------------------------------------------- items
# (id, label, panel_or_n, backbones, arms/cells-per-receptor, n_per_cell)
# Rung names follow redo/spec/SEQUENCES.md section 1:
#   ladder      R0_apo R1_ct11 R2_ct15 R3_ct21 R4_a5helix R5_a5plus R7_full  (7)
#   a5-null     R6a_da5 R6b_a5perm R6c_a5polyA                               (3)
#   additive    R8_hetero                                                    (1)
ITEMS = [
    # STAGE 1 -- gated pilot, reference backbone only
    ("P1", "ladder pilot, 7 rungs",            "CORE-32", 1,  7, 10),
    ("P2", "depth x rung x ligand cube pilot", "CORE-L17", 1, 2*3*2, 10),
    ("P3", "MSA-preparation drift control",     6,        1,  2, 50),
    ("P3b", "subsample-draw variance probe",    6,        1,  3, 50),
    ("P4", "bulk/biological control pilot",    "CORE-32", 1,  3, 10),
    ("P1b", "mid-rung pilot, 60/100/200 aa",   "CORE-32", 1,  3, 10),
    # STAGE 2 -- the graded grid
    ("G1a", "headline ladder, pooled",         "CORE-32", 4,  7, 10),
    ("G1b", "headline ladder, per-cell",       "CORE-32", 4,  7, 50),
    ("G1c", "intermediate rungs x3, pooled",   "CORE-32", 4,  3, 10),
    ("G1d", "intermediate rungs x3, per-cell",  "CORE-32", 4,  3, 50),
    ("G2",  "wide replication on all of C1, R0/R3/R7", 32, 4, 3, 10),
    ("G3a", "a5-null + bulk controls x6, pooled",  "CORE-32", 4, 6, 10),
    ("G3b", "a5-null + bulk controls x6, per-cell","CORE-32", 4, 6, 50),
    ("G3c", "exposure-paired cluster-mates for G3", 12, 4, 6, 50),
    ("G4a", "composition controls at R3_ct21, x4", "CORE-32", 4, 4, 10),
    ("G4b", "composition controls at R3_ct21, x4", "CORE-32", 4, 4, 50),
    ("G5a", "depth cube 3x3x2",                "CORE-L17", 4, 3*3*2, 10),
    ("G5b", "depth cube 5x3x2",                "CORE-L17", 4, 5*3*2, 10),
    ("G6a", "ligand x partner 2x4, pooled",    "CORE-L17", 4, 4*2, 10),
    ("G6b", "ligand x partner 2x4, per-cell",  "CORE-L17", 4, 4*2, 50),
    ("G7",  "deep-apo floor / bistability",     4,        4,  1, 500),
    ("G8",  "date-stratified holdout (tier H-B)", "H-B",  4,  3, 50),
    ("G9",  "family swap at R3_ct21",          "CORE-32", 4,  1, 50),
    ("G10", "per-position Ala scan",            10,       1, 21, 20),
    ("G11", "heterotrimer rung R8",            "CORE-32", 4,  1, 50),
    ("G12", "Gi/Gt single-residue pair",       "CORE-32", 4,  1, 50),
    ("G13", "post-cutoff inactive nanobody",    1,        4,  3, 50),
    ("G14", "prospective, tier E-pro",         "E-pro",   4,  3, 50),
    ("G15", "class B1 transfer, tier E-B1",    "E-B1",    4,  4, 50),
    # ---- added 2026-09-12: g1_preflight listed E1.8 and E1.9 as having no line
    # item here, and G18/G19/G20 were absent too.  Every row below was DERIVED
    # from inputs/g1_systems.csv -- receptors x constructs x backbones x n -- and
    # check_against_systems() asserts each reproduces that file's own totals, so
    # the two cannot drift apart silently.  Counts are explicit integers rather
    # than panel names because these arms run on the frozen 30-receptor primary
    # panel, not on the 32 that CORE-32 names.
    ("G16a", "uncoupling nulls, full-length (E1.8)",        6, 4,  2, 50),
    ("G16b", "uncoupling nulls, peptide rungs (E1.8+E1.1)", 6, 4,  4, 50),
    ("G17a", "partner MSA on/off, pooled (E1.9)",          30, 4,  3, 10),
    ("G17b", "partner MSA on/off, per-cell (E1.9)",        30, 4,  3, 50),
    ("G18a", "wet-lab length series, per-cell",            30, 4,  3, 50),
    ("G18b", "wet-lab matched peptides (boltz2 only)",      6, 1,  3, 10),
    ("G19",  "reference-matched tip, 23 cells",            23, 4,  1, 10),
    ("G20",  "chimeric-reference extension tier",          10, 4,  3, 10),
    # B18 found these four when it was first made to actually look: the standing
    # WAIT named only E1.8 and E1.9, and four more arms had no line here either.
    ("G1c-opt", "intermediate rung, optional 4th",          30, 4,  1, 10),
    ("G1e",  "helical-domain deletion companion",           30, 4,  1, 10),
    ("G1f",  "deposited mini-G anchor (boltz2 only)",       30, 1,  3, 10),
    ("G10b", "Gi->Gs stepwise substitution series",         10, 1, 15, 20),
]

# (item id in matrix_cost) -> (item, arm, grain) in inputs/g1_systems.csv
SYSTEMS_LINK = {
    "G16a": ("G16(proposed)", "uncoupling_full", "pooled"),
    "G16b": ("G16(proposed)", "uncoupling_peptide", "pooled"),
    "G17a": ("G17(proposed)", "partner_msa_on", "pooled"),
    "G17b": ("G17(proposed)", "partner_msa_on", "percell"),
    "G18a": ("G18a(proposed)", "wetlab_length_series", "percell"),
    "G18b": ("G18b(proposed)", "wetlab_matched_peptides", "pooled"),
    "G19":  ("G19(proposed)", "reference_matched_tip", "pooled"),
    "G20":  ("G20(extension)", "chimeric_ref_extension", "pooled"),
    "G1c-opt": ("G1c-opt", "intermediate_optional", "pooled"),
    "G1e":  ("G1e", "hd_deletion_companion", "pooled"),
    "G1f":  ("G1f", "deposited_minig_anchor", "pooled"),
    "G10b": ("G10b", "gi_to_gs_series", "pooled"),
}


def check_against_systems():
    """Assert every linked item reproduces g1_systems.csv's own prediction count.

    A cost table that disagrees with the system table is worse than no cost
    table: both look authoritative and only one is read.
    """
    import csv as _csv
    path = os.path.join(INPUTS, "g1_systems.csv")
    if not os.path.exists(path):
        print("  g1_systems.csv absent -- cannot cross-check")
        return 1
    with open(path) as fh:
        rows = list(_csv.DictReader(fh))
    bad = 0
    print("== 2b. cross-check against g1_systems.csv ==")
    for cid, (item, arm, grain) in SYSTEMS_LINK.items():
        sub = [r for r in rows if r["item"] == item and r["arm"] == arm]
        col = "predictions_pooled" if grain == "pooled" else "predictions_percell"
        theirs = sum(int(r[col] or 0) for r in sub)
        ours = size(BY_ID[cid])
        flag = "ok " if ours == theirs else "MISMATCH"
        if ours != theirs:
            bad += 1
        print(f"  {flag} {cid:>5}  matrix_cost {ours:>7,}  g1_systems {theirs:>7,}"
              f"   ({item}/{arm}, {grain})")
    print(f"\n  {len(SYSTEMS_LINK) - bad}/{len(SYSTEMS_LINK)} linked items agree.\n")
    return 1 if bad else 0

TIERS = {
    "MINIMAL":  ["P1", "P1b", "P2", "P3", "P3b", "P4",
                 "G1a", "G1c", "G3a", "G5a", "G6a"],
    "INTENDED": ["P1", "P1b", "P2", "P3", "P3b", "P4",
                 "G1b", "G1c", "G3b", "G4a", "G5a", "G6b", "G7", "G8", "G13"],
    "EXPANSIVE": ["P1", "P1b", "P2", "P3", "P3b", "P4",
                  "G1b", "G1d", "G2", "G3b", "G3c", "G4b", "G5b", "G6b",
                  "G7", "G8", "G9", "G10", "G11", "G12", "G13", "G14", "G15"],
}


def size(item):
    _id, _lab, panel, bb, arms, n = item
    p = PANELS[panel] if isinstance(panel, str) else panel
    return p * bb * arms * n


BY_ID = {i[0]: i for i in ITEMS}


def items():
    print("== 2. item costs ==")
    print(f"  {'id':>4} {'panel':>8} {'bb':>3} {'cells/rec':>10} {'n':>4} "
          f"{'preds':>9}  label")
    for it in ITEMS:
        _id, lab, panel, bb, arms, n = it
        p = PANELS[panel] if isinstance(panel, str) else panel
        print(f"  {_id:>4} {str(panel):>8} {bb:>3} {arms:>10} {n:>4} "
              f"{size(it):>9,}  {lab}")
    print()


def tiers():
    print("== 3. budget tiers ==")
    for name, ids in TIERS.items():
        tot = sum(size(BY_ID[i]) for i in ids)
        print(f"  {name:<10} {tot:>9,} predictions "
              f"= {tot/BLOCK_B:>4.1f} Block-B drops "
              f"= {100*tot/1_120_000:>4.1f}% of the core full factorial")
        for sname, mult in SCEN.items():
            h = tot * SEC_PER_PRED_APO * mult / 3600
            print(f"      {sname:36s} {h:>8,.0f} H100-h "
                  f"= {h/D3_WORKERS/24:>5.1f} days wall on {D3_WORKERS} H100")
        print(f"      items: {' '.join(ids)}")
        print()
    full = sum(DELIVERED.values())
    for name, ids in TIERS.items():
        tot = sum(size(BY_ID[i]) for i in ids)
        print(f"  {name:<10} = {tot/full:.2f}x the whole A-D campaign "
              f"({full:,} predictions)")


if __name__ == "__main__":
    factorial()
    items()
    check_against_systems()
    tiers()
