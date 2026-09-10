# -*- coding: utf-8 -*-
"""Block C loader. Small, because Block C ships almost no row-level data.

WHAT IS AND IS NOT AVAILABLE, since it shapes every panel here. Block C
delivered one row-level file -- the 40,000-row off-site census -- and summary
JSON for everything else. `rows.tier3.v2.csv`, the primary corpus behind
SC-C-1, SC-C-2, SC-C-3, SC-C-4 and SC-C-6, was not shipped.

So panels split three ways and each says which it is on its own face:
  FULL        built from row-level data (BC-4 only)
  PER-RECEPTOR  summary JSON that happens to carry per-receptor values
                (BC-2: s5_p4_ordinal.json has a tau per receptor)
  SUMMARY     four numbers and their intervals, with no distribution behind
              them (BC-1, BC-3)

A SUMMARY panel is not a lesser version of a FULL one; it is a different
object, and this project has twice found a four-value summary hiding a bimodal
population. Every SUMMARY panel here says so.

THE THREE-BAND CENSUS. in-pocket <= 8 A, entrance-bound 8-15 A, off-site > 15 A.
Entrance-bound is an ADJUDICATED VALID POSE, not a failure. Treating the
boundary as 8 A instead of 15 A reports 34.8% where the truth is 15.1%.

LIGAND TYPE IS THE LOAD-BEARING SPLIT. `ligand_source` is `hetatm` or
`peptide_chain`. In the same apo agonist/antagonist cells these are 1.52% and
66.53% off-site. Pooling them manufactures a failure rate. Filter on the column,
never on a substring of the role name.
"""
import json, os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(ROOT, "data", "block_c")

IN_POCKET_A, OFF_SITE_A = 8.0, 15.0
BACKBONES = ["boltz", "chai", "of3", "protenix"]


def J(rel):
    return json.load(open(os.path.join(C, rel)))


def census():
    return pd.read_csv(os.path.join(C, "12_g4_off_site_census",
                                    "g4_full_census_v2.csv"), low_memory=False)


def band(d):
    """The three adjudicated bands, as a categorical."""
    return pd.cut(d, [-0.01, IN_POCKET_A, OFF_SITE_A, 1e9],
                  labels=["in-pocket", "entrance-bound", "off-site"])
