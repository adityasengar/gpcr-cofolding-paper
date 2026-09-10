#!/usr/bin/env python3
"""Loader for Block D figure panels. Every panel must go through this file.

WHY A LOADER FOR A BLOCK WITH NO DATA. Block D ships no row table -- the three
corpora its claim sheet names, 42,180 predictions, are not in the bundle. So
unlike Block A, B or C there is nothing here to filter; there are transcribed
tables. That makes the loader MORE important, not less: a transcription is a
place where a digit can change silently, so every table below is typed in once,
here, beside the file and section it came from, and no panel may hold its own
copy of a number.

THE THREE TRAPS THIS FILE ENCODES, so that no panel can hit them by accident.

1. CI METHOD IS NOT UNIFORM ACROSS TIERS (Flag D-1). D3 has 22 paralog clusters
   over 26 receptors and uses cluster-boot. D1 (7 receptors, 7 clusters) and D2
   (4, 4) are cluster-boot-DEGENERATE -- one receptor per cluster, so the two
   bootstraps are arithmetically the same thing -- and use receptor-boot. Ask
   this module for `ci_method(tier)`; it will not let a caption guess.

2. THE D3 SLOPE UNIT IS %/ln(depth), NOT %/log10 (Flag D-2, W-D-6). The four
   headline slopes reproduce only under natural log with full = 4096. Under
   log10 they are Boltz -3.877 rather than -1.684. `SLOPE_UNIT` is the only
   string a panel may use for that axis.

3. OF3 AND PROTENIX ARE NOT LEVERS (Flag D-3). They have the LARGEST apparent
   slopes and the weakest claim: the predicate clears while sub-Angstrom-to-
   active drops 20.9 points on OF3, and matched-seed backbone deviation reaches
   10-14 A on OF3 and 15-20 A on Protenix. `MECHANISM` carries the four verdicts
   and every panel with a backbone axis must annotate from it. There is no way
   to ask this module for a pooled slope.

NEVER POOL ACROSS BACKBONES. The dispatch is explicit and so is the campaign's
history: W-D-2 withdrew D1's original headline precisely because a
backbone-averaged fraction read as a finding while the per-backbone behaviour
was bimodal. There is no pooling helper in this file.

Provenance: every table names its source document and section in its own
comment. Nothing here is estimated, and nothing is carried from another block.
"""

# --------------------------------------------------------------------------
# Flag D-1 -- which bootstrap each tier actually used, and why
# --------------------------------------------------------------------------
_CI = {
    "d1": ("receptor-boot", "7 receptors in 7 paralog clusters -- cluster-boot "
                            "is degenerate at 1 receptor per cluster"),
    "d2": ("receptor-boot", "4 receptors in 4 paralog clusters -- cluster-boot "
                            "is degenerate at 1 receptor per cluster"),
    "d3": ("cluster-boot", "26 receptors in 22 paralog clusters"),
}


def ci_method(tier):
    """(method, why). Both strings belong in the caption; Flag D-1 requires it."""
    return _CI[tier.lower()]


SLOPE_UNIT = r"%/ln(depth)"          # Flag D-2. Never "%/log(depth)".
PREDICATE_NPXXY = 9.08               # A, active below
PREDICATE_TILT = 14.932              # A, active above

BACKBONES = ["Boltz-2", "Chai-1", "OpenFold-3", "Protenix2"]
_BB_KEY = {"Boltz-2": "boltz", "Chai-1": "chai",
           "OpenFold-3": "of3", "Protenix2": "protenix"}

# --------------------------------------------------------------------------
# D1 -- PARTA_D1.md section 1, the three 7 x 4 tables.
# Values are percent with a receptor-boot 95% CI. n = 500 per cell.
# --------------------------------------------------------------------------
D1_RECEPTORS = ["CNR2", "OPSD", "ADRB2", "LPAR1", "CXCR4", "GHSR", "NPY1R"]

D1_PREDICATE_ACTIVE = {           # PARTA_D1 section 1, table 1
    "CNR2":  {"boltz": (2.2, 1.0, 3.4),   "chai": (99.8, 99.4, 100.0),
              "of3": (1.8, 0.8, 3.0),     "protenix": (1.6, 0.6, 2.8)},
    "OPSD":  {"boltz": (38.8, 34.6, 43.0), "chai": (98.6, 97.4, 99.6),
              "of3": (9.4, 6.8, 12.2),    "protenix": (0.0, 0.0, 0.0)},
    "ADRB2": {"boltz": (0.0, 0.0, 0.0),   "chai": (100.0, 100.0, 100.0),
              "of3": (4.0, 2.4, 5.8),     "protenix": (0.0, 0.0, 0.0)},
    "LPAR1": {"boltz": (0.2, 0.0, 0.6),   "chai": (0.0, 0.0, 0.0),
              "of3": (91.8, 89.2, 94.0),  "protenix": (0.0, 0.0, 0.0)},
    "CXCR4": {"boltz": (0.0, 0.0, 0.0),   "chai": (0.0, 0.0, 0.0),
              "of3": (3.8, 2.2, 5.6),     "protenix": (0.0, 0.0, 0.0)},
    "GHSR":  {"boltz": (0.0, 0.0, 0.0),   "chai": (0.0, 0.0, 0.0),
              "of3": (0.0, 0.0, 0.0),     "protenix": (0.0, 0.0, 0.0)},
    "NPY1R": {"boltz": (0.2, 0.0, 0.6),   "chai": (0.0, 0.0, 0.0),
              "of3": (6.6, 4.6, 9.0),     "protenix": (0.0, 0.0, 0.0)},
}

D1_SUBA_ACTIVE = {                # PARTA_D1 section 1, table 2
    "CNR2":  {"boltz": 100.0, "chai": 100.0, "of3": 100.0, "protenix": 100.0},
    "OPSD":  {"boltz": 65.0,  "chai": 75.8,  "of3": 0.0,   "protenix": 0.0},
    "ADRB2": {"boltz": 82.8,  "chai": 100.0, "of3": 84.4,  "protenix": 1.4},
    "LPAR1": {"boltz": 0.0,   "chai": 0.0,   "of3": 0.4,   "protenix": 0.0},
    "CXCR4": {"boltz": 1.2,   "chai": 0.0,   "of3": 56.6,  "protenix": 0.0},
    "GHSR":  {"boltz": 55.2,  "chai": 13.8,  "of3": 33.2,  "protenix": 14.0},
    "NPY1R": {"boltz": 0.0,   "chai": 0.6,   "of3": 65.8,  "protenix": 1.4},
}

D1_SUBA_INACTIVE = {              # PARTA_D1 section 1, table 3
    "CNR2":  {"boltz": 86.0,  "chai": 91.6,  "of3": 99.8,  "protenix": 96.8},
    "OPSD":  {"boltz": 26.8,  "chai": 1.2,   "of3": 95.8,  "protenix": 100.0},
    "ADRB2": {"boltz": 100.0, "chai": 16.8,  "of3": 100.0, "protenix": 100.0},
    "LPAR1": {"boltz": 99.8,  "chai": 100.0, "of3": 5.6,   "protenix": 100.0},
    "CXCR4": {"boltz": 84.0,  "chai": 10.0,  "of3": 0.6,   "protenix": 59.6},
    "GHSR":  {"boltz": 22.2,  "chai": 19.8,  "of3": 52.0,  "protenix": 51.6},
    "NPY1R": {"boltz": 98.8,  "chai": 99.4,  "of3": 99.8,  "protenix": 100.0},
}

# SC-D-1 / Flag D-5. Delta is against the max of the OTHER three backbones, and
# the Block A column is the independent cross-tier reproduction at n = 25/cell.
D1_OUTLIERS = [                   # claim sheet SC-D-1; Flag D-5 for Block A
    ("CNR2",  "chai", 98.4, "+96.0"),
    ("OPSD",  "chai", 60.2, "+52.0"),
    ("ADRB2", "chai", 98.0, "+96.0"),
    ("LPAR1", "of3",  91.6, "+88.0"),
]

# --------------------------------------------------------------------------
# D2 -- PARTA_D2.md sections F1, F2, F3. n = 50 per cell (every Clopper-Pearson
# interval in the claim sheet reproduces at 50 and none reproduces at 200; see
# DISCREPANCY_REPORT D-D-3). Percent with an exact binomial 95% CI.
# --------------------------------------------------------------------------
D2_COGNATE_MISSES = {             # SC-D-4: 14/16 cells reach >= 96%; both misses OF3
    ("ACM2", "of3"): (58.0, 43.2, 71.8),
    ("OPRK", "of3"): (36.0, 22.9, 50.8),
}

D2_ACM2_ACTIVE_NB = {             # PARTA_D2 F2 -- the clean per-receptor test
    "boltz":    {"apo": 42.0, "nb": 100.0, "delta": +58},
    "chai":     {"apo": 0.0,  "nb": 0.0,   "delta": 0},
    "of3":      {"apo": 12.0, "nb": 82.0,  "delta": +70},
    "protenix": {"apo": 0.0,  "nb": 100.0, "delta": +100},
}

D2_INACTIVE_NB = {                # PARTA_D2 F3, both receptors, apo vs inactive_nb
    "ADRB2": {
        "boltz":    ((0.0, 0.0, 7.1),      (0.0, 0.0, 7.1),      0,   "correct"),
        "chai":     ((100.0, 92.9, 100.0), (100.0, 92.9, 100.0), 0,   "refuses to shift"),
        "of3":      ((10.0, 3.3, 21.8),    (10.0, 3.3, 21.8),    0,   "stable"),
        "protenix": ((0.0, 0.0, 7.1),      (76.0, 61.8, 86.9),   +76, "INVERTS"),
    },
    "OPRK": {
        "boltz":    ((4.0, 0.5, 13.7),     (48.0, 33.7, 62.6),   +44, "INVERTS"),
        "chai":     ((74.0, 59.7, 85.4),   (82.0, 68.6, 91.4),   +8,  "drifts up"),
        "of3":      ((0.0, 0.0, 7.1),      (10.0, 3.3, 21.8),    +10, "near-stable"),
        "protenix": ((0.0, 0.0, 7.1),      (6.0, 1.3, 16.5),     +6,  "near-correct"),
    },
}

# Flag D-10: OPRK is unanimous_up. The flagship cell's CI spans 50%, so
# "approaches half" is supported and "majority invert" is not.
D2_FLAGSHIP = dict(receptor="OPRK", backbone="boltz", pct=48.0, lo=33.7, hi=62.6,
                   n=50, sentence_allowed="approaches half",
                   sentence_forbidden="a majority of samples invert")

# --------------------------------------------------------------------------
# D3 -- PARTA_D3.md section 1 (the depth ladder) and section 2 (the slopes).
# Depths: 8, 32, 128, 512, and "full", which the slope fit treats as 4096
# (GATE-2 section 4; the fit reproduces the headline numbers only at 4096).
# --------------------------------------------------------------------------
D3_DEPTHS = [8, 32, 128, 512, 4096]
D3_FULL_LABEL = "full"            # printed on the axis; 4096 is the fitted value

D3_LADDER = {                     # PARTA_D3 section 1
    "boltz":    {"predicate": [17.8, 7.0, 4.9, 5.4, 5.1],
                 "suba_active": [51.2, 43.8, 39.9, 41.1, 42.5],
                 "suba_inactive": [68.5, 75.8, 79.2, 81.0, 79.7],
                 "plddt": [75.73, 76.08, 76.01, 76.15, 76.26]},
    "chai":     {"predicate": [25.1, 20.2, 19.7, 18.4, 19.4],
                 "suba_active": [36.7, 36.9, 36.6, 39.1, 43.0],
                 "suba_inactive": [71.8, 74.7, 74.2, 79.1, 78.7],
                 "plddt": [74.14, 74.11, 74.89, 75.67, 75.12]},
    "of3":      {"predicate": [28.0, 26.2, 21.9, 15.4, 12.4],
                 "suba_active": [29.7, 44.8, 50.2, 50.5, 50.6],
                 "suba_inactive": [37.2, 57.5, 68.6, 73.1, 73.8],
                 "plddt": [64.60, 67.16, 67.90, 68.10, 68.45]},
    "protenix": {"predicate": [15.5, 16.8, 9.7, 2.1, 0.1],
                 "suba_active": [29.2, 42.1, 40.5, 37.6, 37.9],
                 "suba_inactive": [44.9, 68.0, 79.8, 85.8, 89.0],
                 "plddt": [72.11, 73.87, 74.78, 75.19, 75.29]},
}

D3_SLOPES = {                     # SC-D-8; cluster-boot 95% CI over 22 clusters
    "boltz":    (-1.684, -2.692, -0.812, True),
    "chai":     (-0.815, -2.380, +0.357, False),     # crosses zero
    "of3":      (-2.732, -4.365, -1.145, True),
    "protenix": (-2.956, -4.678, -1.581, True),
}

# Flag D-3 -- the mechanism verdicts. A panel showing slopes MUST annotate from
# this, because the two largest slopes belong to the two weakest claims.
MECHANISM = {
    "boltz":    ("LEVER", "clean: sub-A tracks the predicate, matched-seed "
                          "Ca stays 1-4 A"),
    "chai":     ("LEVER, MUTED", "slope unsigned under cluster-boot; fold "
                                 "quality preserved"),
    "of3":      ("DEGRADATION-LEANING", "predicate clears while sub-A-to-active "
                                        "drops 20.9 pts; Ca 10-14 A; pLDDT -3.9"),
    "protenix": ("MIXED, RECEPTOR-DEPENDENT", "largest apparent slope, worst "
                                              "fold fidelity: Ca 15-20 A"),
}

# GATE-3 section 1 -- the structural-integrity view of the same split
D3_MATCHED_SEED_CA = {            # full -> depth-8 backbone deviation, A
    "boltz": (1, 4), "chai": (2, 5), "of3": (10, 14), "protenix": (16, 20),
}
D3_PLDDT_DELTA = {"boltz": -0.5, "chai": -1.0, "of3": -3.9, "protenix": -3.2}
D3_SUBA_DELTA = {                 # SC-D-8(b), full -> depth-8, percentage points
    "boltz": +8.7, "chai": None, "of3": -20.9, "protenix": -8.7,
}

# GATE-3 section, the two flagship cells for SC-D-12
D3_FLAGSHIP_CELLS = {
    "boltz_opsd": dict(cell="Boltz-2, OPSD", full=dict(pca=1.25, npxxy=13.85, tilt=12.78),
                       d8=dict(pca=0.41, npxxy=4.99, tilt=17.34),
                       verdict="clean lever: predicate clears AND the pocket "
                               "moves TOWARD the active reference"),
    "protenix_agtr1": dict(cell="Protenix2, AGTR1",
                           full=dict(pca=0.76, npxxy=10.93, tilt=11.19),
                           d8=dict(pca=1.24, npxxy=3.40, tilt=16.78),
                           verdict="degradation: predicate clears WHILE the "
                                   "pocket moves AWAY from the active reference"),
}

# --------------------------------------------------------------------------
# Structures. Measured here, not transcribed -- cifmeasure.py reads the
# coordinates. See DISCREPANCY_REPORT D-D-2 and D-D-8.
# --------------------------------------------------------------------------
import json as _json
import os as _os

_HERE = _os.path.dirname(_os.path.abspath(__file__))
_MEAS = _os.path.join(_os.path.dirname(_os.path.dirname(_HERE)),
                      "analysis", "block_d", "cif_measurements.json")


def measured_npxxy(filename):
    """d(Y5.58 OH, Y7.53 OH) measured from the shipped coordinates, or None.

    Panels must use this rather than the manifest's `dossier_finding` string.
    One of those strings quotes a 50-sample cell median beside a single file
    (D-D-4), and PARTA_D1's per-structure table disagrees with the coordinates
    by up to 0.51 A (D-D-8).
    """
    if not _os.path.exists(_MEAS):
        return None
    return _json.load(open(_MEAS)).get(filename, {}).get("npxxy_oh")


def state_call(npxxy):
    if npxxy is None:
        return "unmeasured"
    return "active" if npxxy < PREDICATE_NPXXY else "inactive"


def bb_key(label):
    return _BB_KEY[label]
