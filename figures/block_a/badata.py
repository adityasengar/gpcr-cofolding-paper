"""
Block A data access, and the exclusion filters spelled out.

One module owns the paths and the filters so that no panel script can quietly
invent a different population from the one its caption claims. Every loader
returns the tidy CSV untouched; every filter returns `(frame, label, n)` and
the label is the string the caption must carry.

THE EXCLUSION TRAP
------------------
`block_a_rows.csv` carries five boolean flags plus an `excl_any` aggregate.
`excl_any` fires on 5,093 of 9,490 rows (54%) and is WRONG for almost every
panel, because the five sets have different scopes and only two of them are
about the row at all:

  E1  25 rows     cell mean pLDDT < 50 (one broken cell)      always exclude
  E2  4 rows      impossible geometry, NPxxY-OH < 2.4 A       always exclude
  E3  4,890 rows  the receptor's REFERENCE fails its own predicate.
                  Relevant only where a reference value is a denominator or a
                  regression predictor - the amplitude fits and the fraction
                  metric. Use the per-axis flags `excl_E3_npxxy` (4,690 rows /
                  24 receptors) or `excl_E3_tilt` (2,000 rows / 10 receptors).
                  The `excl_E3` union is never the right filter, and E3 is
                  irrelevant to raw distributions, predicate firing rates and
                  confidence correlations, which do not divide by a reference.
  E4  1,495 rows  Class B or Class F. For a Class-A claim only.
  E5  500 rows    agonist-only actives (OPRD, CNR1, FZD4). Sensitivity only.

E1 + E2 alone keeps 9,461 of 9,490 rows, 99.7%. That is the default here and
anything narrower has to be asked for by name.
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.dirname(HERE)                     # paper/figures
ROOT = os.path.dirname(FIGDIR)                     # paper/
DATA = os.path.join(ROOT, "data", "block_a")
OUT = os.path.join(FIGDIR, "out")

# thresholds, from block_a_rows.csv (constant across all 9,490 rows)
THR_NPXXY = 9.08
THR_TILT = 14.932
THR_KINK = 159.95

# reference connector medians, 05_connector/connector_references.csv
CONN_REF_ACTIVE = 10.48
CONN_REF_INACTIVE = 11.99
CONN_REF_DELTA = -1.51
CONN_REF_N = 77


def load(relpath):
    """Read one tidy CSV out of the Block A drop, by its path in the zip."""
    return pd.read_csv(os.path.join(DATA, relpath))


def rows():
    return load("01_rows/block_a_rows.csv")


# --- the filters, each returning (frame, caption label, n) -----------------

def core(df):
    """E1+E2 only. The default population for every raw distribution."""
    keep = ~(df["excl_E1"] | df["excl_E2"])
    return df[keep], "E1+E2 excluded (broken cell, impossible geometry)", int(keep.sum())


def core_class_a(df):
    """E1+E2+E4. For any claim scoped to the Class-A-calibrated instrument."""
    keep = ~(df["excl_E1"] | df["excl_E2"]) & (df["gpcr_class"] == "A")
    return df[keep], "E1+E2 excluded, Class A only (E4)", int(keep.sum())


def core_npxxy_refs(df):
    """
    E1+E2 plus the PER-AXIS E3 for NPxxY. Only for analyses in which the
    NPxxY reference value is a denominator or a regression predictor.
    """
    keep = ~(df["excl_E1"] | df["excl_E2"] | df["excl_E3_npxxy"])
    return (df[keep],
            "E1+E2 excluded, plus per-axis E3 on NPxxY (reference fails its "
            "own predicate)", int(keep.sum()))


def core_tilt_refs(df):
    """E1+E2 plus the PER-AXIS E3 for tilt. Same restriction as above."""
    keep = ~(df["excl_E1"] | df["excl_E2"] | df["excl_E3_tilt"])
    return (df[keep],
            "E1+E2 excluded, plus per-axis E3 on tilt (reference fails its "
            "own predicate)", int(keep.sum()))


def confidence_population(df):
    """
    The exact population behind `06_confidence/plddt_correlations.csv`:
    Class A rows carrying an RMSD to an active reference. Verified to
    reproduce all 12 Pearson r values to 1e-4. n = 1,595-1,600 per backbone
    over 32 receptors (the CSV's own `n_receptors` column says 40; see
    FIGURE_PROVENANCE.md).
    """
    keep = (df["gpcr_class"] == "A") & df["rmsd_to_active_ref"].notna()
    return (df[keep],
            "Class A rows with an active reference (the population behind "
            "plddt_correlations.csv)", int(keep.sum()))


def describe_filter(label, n, total=9490):
    return "%s; n = %s of %s rows" % (label, "{:,}".format(n),
                                      "{:,}".format(total))
