# -*- coding: utf-8 -*-
"""Block B loader. One place that knows the frames, the flags and the traps.

Every Block B panel loads through here so that a filter mistake is made once
rather than six times.

THE TRAPS THIS MODULE EXISTS TO PREVENT, all verified in
analysis/block_b/DISCREPANCY_REPORT.md:

1. The claim sheet MISLABELS three of the four exclusion flags. Its header says
   E-B-2 = AA2AR, E-B-3 = the 15 non-native, E-B-4 = ceiling-pinned. The shipped
   flags say E-B-2 = OPRD+CNR1, E-B-3 = AA2AR, E-B-4 = the 15 non-native, and
   ceiling-pinning is not a row flag at all. So this module exposes exclusion
   sets BY MEANING, never by their E-B-n label, and no panel script may write
   `excl_E_B_n`.
2. `excl_any` is a convenience column and is never the right filter.
3. Frame labels are inconsistent ACROSS FILES: ladder_four_scorings.csv says
   `frame_36`, ladder_decomposition.csv says `reproduction_36`. frame() handles
   both.
4. The eight continuous panel medians in SC-B-1 reproduce from nothing (D-B-2).
   Do not read them from the claim sheet; compute from rows.
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = os.path.join(ROOT, "data", "block_b")

#: NPxxY is undefined for these: position 7.53 is Leu, not Tyr. Biology, not data loss.
NPXXY_UNDEFINED = ["EDNRA", "EDNRB", "GRPR", "HRH3"]

#: exclusion sets by MEANING. The values are the receptor lists the flags
#: actually carry, checked against exclusion_definitions.csv by verify_claims.
SETS = {
    "npxxy_undefined":   NPXXY_UNDEFINED,                 # ships as excl_E_B_1
    "agonist_only_ref":  ["OPRD", "CNR1"],                # ships as excl_E_B_2
    "aa2ar_anomaly":     ["AA2AR"],                       # ships as excl_E_B_3
    "non_native_ref":    None,                            # ships as excl_E_B_4
}

ARM_ORDER = ["apo", "decoy", "shuffled", "cognate"]
ARM_LABELS = {"apo": "apo", "decoy": "decoy", "shuffled": "shuffled",
              "cognate": "cognate"}


def rows():
    """The 32,000-row tidy table, unfiltered."""
    return pd.read_csv(os.path.join(B, "01_rows", "rows_tidy.csv"), low_memory=False)


def table(rel):
    return pd.read_csv(os.path.join(B, rel), low_memory=False)


def frame(df, n=36):
    """frame_36 or frame_40, applied by membership rather than by flag name."""
    if n == 40:
        return df
    if n != 36:
        raise ValueError("Block B publishes two frames, 36 and 40; got %r" % n)
    return df[~df.receptor_slug.isin(NPXXY_UNDEFINED)].copy()


def pick_frame(df, n=36):
    """Select the frame row from a shipped table, whichever label it uses."""
    want = {"frame_%d" % n, "reproduction_%d" % n if n == 36 else "all_%d" % n}
    got = set(df.frame.unique())
    hit = want & got
    if not hit:
        raise KeyError("no frame_%d-equivalent in %s" % (n, sorted(got)))
    return df[df.frame == sorted(hit)[0]].copy()


#: The NPxxY threshold is TRUNCATED to 9.08 in the row column while the claim
#: sheet, the README and the shipped aggregate tables all use 9.082. That is not
#: cosmetic: five rows of 32,000 fall in [9.080, 9.082), and one of them --
#: AA2AR / chai / decoy -- flips, moving that cell from 0.90 to 0.88. The panel
#: decoy rate moves 0.5578 vs 0.5579, so the headline is unaffected and
#: per-receptor cells are not. See D-B-3.
NPXXY_ROW_COLUMN = 9.08          # what every row carries
NPXXY_UNTRUNCATED = 9.082        # what the shipped aggregates were computed with
BOUNDARY_ROWS = 5


def predicate(df, npxxy_threshold=None):
    """The two-instrument call, recomputed. Never read a shipped active column.

    npxxy_threshold=None uses the per-row column (9.08). Pass
    NPXXY_UNTRUNCATED to reproduce the shipped aggregate tables exactly.
    """
    tn = (df.threshold_npxxy_oh_active_lt if npxxy_threshold is None
          else npxxy_threshold)
    return ((df.d_npxxy_y558_y753_oh < tn) &
            (df.d_gpcrdb_tm6_tilt_246_637_ca > df.threshold_gpcrdb_tm6_tilt_active_gt))


def n_clusters(df):
    """The resampling unit actually present. frame_36 has 24, not the 26 every
    shipped interval is labelled with (D-B-8)."""
    return int(df.cluster_id.nunique())


def exclude(df, *names):
    """Drop one or more exclusion sets BY MEANING."""
    out = df
    for nm in names:
        if nm not in SETS:
            raise KeyError("unknown exclusion set %r; known: %s"
                           % (nm, sorted(SETS)))
        members = SETS[nm]
        if members is None:                       # non-native: read from the data
            keep = out.active_stabilization_source.astype(str) == "native"
            out = out[keep]
        else:
            out = out[~out.receptor_slug.isin(members)]
    return out.copy()
