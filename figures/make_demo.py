#!/usr/bin/env python3
"""
Build one of every panel type from the data actually in data/predictions.csv.

This is a SMOKE TEST, not a manuscript figure. It exists so that the toolkit is
known to run end to end on real columns before anyone depends on it, and so a
new session can see what each generator looks like without reading the code.

Nothing it writes is citable. The numbers here are a local slice of a much
larger run; `RESULTS.md` records claim by claim what does and does not
reproduce against it. Run analysis/fingerprint.py --check before believing any
number you see in these panels.

    python3 make_demo.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import figstyle as fs
import figpanels as fp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "predictions.csv")

# The contrast the paper is built on, in the order the argument runs.
PARTNER_ORDER = ["apo", "ligand", "antagonist", "α5_ct_fragment",
                 "α5_ct_variant", "cognate_ga", "shuffled_ga", "decoy_scaffold"]
STATE_ORDER = ["inactive", "borderline", "active"]


def main():
    fs.use_house_style()
    d = pd.read_csv(DATA)
    d = d[d["passed"]]                      # a failed prediction has no geometry
    sub = d[d["partner_type"].isin(PARTNER_ORDER)]
    print("loaded %d scored predictions (%d in the eight named arms)"
          % (len(d), len(sub)))

    # -- a. distribution, not a bar ---------------------------------------
    fig, ax = fs.figure(fs.W2, 62 * fs.MM)
    n = fp.strip_violin(ax, sub, "partner_type", "d_tm6",
                        order=PARTNER_ORDER, colours=fs.PARTNER_COLOURS)
    ax.set_ylabel("TM6 displacement, d$_{TM6}$ (Å)")
    ax.set_xlabel("")
    fs.panel_label(ax, "a", dx=-0.05)
    print("  a strip_violin        ", fs.save(fig, "demo_a_distribution")[0])

    # -- b. composition with n kept visible -------------------------------
    fig, ax = fs.figure(fs.W1, 62 * fs.MM)
    fp.state_composition(ax, sub, "partner_type", "classified_state",
                         order=PARTNER_ORDER, state_order=STATE_ORDER,
                         colours=fs.STATE_COLOURS)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3)
    fs.panel_label(ax, "b", dx=-0.42)
    print("  b state_composition   ", fs.save(fig, "demo_b_composition")[0])

    # -- c. does confidence track the state? ------------------------------
    fig, ax = fs.figure(fs.W1, 55 * fs.MM)
    fp.confidence_vs_measure(ax, d[d["classified_state"].notna()],
                             "plddt_at_anchors_mean", "d_tm6",
                             group="classified_state", colours=fs.STATE_COLOURS)
    ax.set_xlabel("mean pLDDT at the state anchors")
    ax.set_ylabel("d$_{TM6}$ (Å)")
    ax.legend(loc="upper left", markerscale=4)
    fs.panel_label(ax, "c")
    print("  c confidence scatter  ", fs.save(fig, "demo_c_confidence")[0])

    # -- d. within-receptor contrast --------------------------------------
    fig, ax = fs.figure(fs.W1, 60 * fs.MM)
    piv = fp.paired_slope(ax, sub, "receptor", "partner_type", "d_tm6",
                          "apo", "cognate_ga")
    ax.set_ylabel("median d$_{TM6}$ (Å)")
    fs.panel_label(ax, "d")
    print("  d paired_slope        ", fs.save(fig, "demo_d_paired")[0],
          "(%d receptors have both arms)" % len(piv))

    # -- e. what was actually run -----------------------------------------
    top = d["receptor"].value_counts().head(18).index
    tab = (d[d["receptor"].isin(top)]
             .pivot_table(index="receptor", columns="backbone",
                          values="prediction_id", aggfunc="count"))
    fig, ax = fs.figure(fs.W1, 78 * fs.MM)
    fp.matrix(ax, tab, value_label="predictions", annotate=False)
    ax.set_xlabel(""); ax.set_ylabel("")
    fs.panel_label(ax, "e", dx=-0.55)
    print("  e coverage matrix     ", fs.save(fig, "demo_e_coverage")[0])

    # -- f. cumulative, so no binning to argue about ----------------------
    fig, ax = fs.figure(fs.W1, 55 * fs.MM)
    fp.ecdf(ax, d, "backbone", "d_tm6")
    ax.set_xlabel("d$_{TM6}$ (Å)")
    ax.legend(loc="lower right")
    fs.panel_label(ax, "f")
    print("  f ecdf                ", fs.save(fig, "demo_f_ecdf")[0])

    print("\nall panels written to figures/out/ — smoke test only, not citable")


if __name__ == "__main__":
    main()
