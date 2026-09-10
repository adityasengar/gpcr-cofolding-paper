#!/usr/bin/env python3
"""BD-5 -- the same predicate result, reached two opposite ways.

Spec: dispatch Fig. D3-2.   Claim: SC-D-12.   Binding: Flag D-6.

THIS IS THE CLEAREST SINGLE ARGUMENT IN BLOCK D and it needs no statistics.
Take two cells. In both, dropping the MSA to depth 8 makes the two-instrument
predicate fire: NPxxY collapses from ~11 A to under 5 A and the TM6 tilt opens
past 14.932 A. On Boltz/OPSD the pocket ALSO moves toward the deposited active
reference, 1.25 A to 0.41 A. On Protenix/AGTR1 the pocket moves AWAY, 0.76 A to
1.24 A -- it starts closer to active at full depth and ends further from it,
while the coarse predicate reports success.

A binary predicate cannot tell those apart, and that is why D3's original
headline was withdrawn (W-D-5). This panel is the reason the paper reports a
per-backbone mechanism rather than a single depth effect.

EVIDENTIAL CLASS: SUMMARY, and the numbers are CELL MEDIANS over 50 samples each
(GATE-3's table columns are headed "med pca_active", "med NPxxY", "med tilt").
The shipped coordinate file for each cell is ONE sample and is plotted
separately, in its own colour, precisely so the two are never confused -- an
earlier version of our own checker compared a single file against the cell
median and reported a discrepancy that did not exist (DISCREPANCY_REPORT D-D-4).
"""
import os
import sys
import textwrap

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

import figstyle as fs                                          # noqa: E402
import bddata as bd                                            # noqa: E402

CELLS = [("boltz_opsd", "d3_boltz_opsd_depth8.cif", fs.GREEN),
         ("protenix_agtr1", "d3_protenix_agtr1_depth8.cif", fs.VERM)]


def main():
    fs.use_house_style()
    fig = plt.figure(figsize=(fs.W2, 92 * fs.MM))
    gs = fig.add_gridspec(1, 3, wspace=0.42, left=0.075, right=0.985,
                          top=0.84, bottom=0.30)

    # ---- a: the pocket, which is the axis that disagrees ------------------
    ax = fig.add_subplot(gs[0, 0])
    for i, (key, fn, c) in enumerate(CELLS):
        d = bd.D3_FLAGSHIP_CELLS[key]
        ax.plot([0, 1], [d["full"]["pca"], d["d8"]["pca"]], "-o", ms=5, lw=2.0,
                color=c, label=d["cell"])
        ax.annotate("%.2f" % d["full"]["pca"], (0, d["full"]["pca"]),
                    textcoords="offset points", xytext=(-4, 5), fontsize=6.2,
                    ha="right", color=c)
        ax.annotate("%.2f" % d["d8"]["pca"], (1, d["d8"]["pca"]),
                    textcoords="offset points", xytext=(5, 0), fontsize=6.2,
                    ha="left", color=c)
        arrow = "improves" if d["d8"]["pca"] < d["full"]["pca"] else "WORSENS"
        ax.text(0.5, (d["full"]["pca"] + d["d8"]["pca"]) / 2 + 0.07, arrow,
                fontsize=6.2, ha="center", color=c, weight="bold")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["full MSA", "depth 8"], fontsize=6.8)
    ax.set_xlim(-0.42, 1.42)
    ax.set_ylabel("median pocket-Cα RMSD to the ACTIVE reference (Å)",
                  fontsize=6.8)
    ax.set_title("the axis that disagrees", fontsize=7.4, pad=6)
    ax.legend(fontsize=5.9, frameon=False, loc="upper center")
    fs.panel_label(ax, "a", dx=-0.24, dy=1.12)

    # ---- b: the predicate, which agrees ----------------------------------
    ax = fig.add_subplot(gs[0, 1])
    for key, fn, c in CELLS:
        d = bd.D3_FLAGSHIP_CELLS[key]
        ax.plot([0, 1], [d["full"]["npxxy"], d["d8"]["npxxy"]], "-o", ms=5,
                lw=2.0, color=c)
        ax.annotate("%.2f" % d["d8"]["npxxy"], (1, d["d8"]["npxxy"]),
                    textcoords="offset points", xytext=(5, -2), fontsize=6.2,
                    ha="left", color=c)
        v = bd.measured_npxxy(fn)
        if v is not None:
            ax.scatter([1.28], [v], s=44, marker="D", facecolor="white",
                       edgecolor=c, lw=1.3, zorder=4)
            ax.text(1.34, v, "%.2f\nshipped\nsample" % v, fontsize=5.4,
                    va="center", ha="left", color=c)
    ax.axhline(bd.PREDICATE_NPXXY, color="black", lw=1.0, ls="--")
    ax.text(-0.40, bd.PREDICATE_NPXXY + 0.4, "threshold %.2f Å, active below"
            % bd.PREDICATE_NPXXY, fontsize=5.9, va="bottom")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["full MSA", "depth 8"], fontsize=6.8)
    ax.set_xlim(-0.45, 2.05)
    ax.set_ylabel("median NPxxY d(OH, OH) (Å)", fontsize=6.8)
    ax.set_title("the axis that agrees", fontsize=7.4, pad=6)
    fs.panel_label(ax, "b", dx=-0.26, dy=1.12)

    # ---- c: the verdicts, side by side -----------------------------------
    ax = fig.add_subplot(gs[0, 2])
    ax.axis("off")
    y = 0.95
    for key, fn, c in CELLS:
        d = bd.D3_FLAGSHIP_CELLS[key]
        ax.text(0, y, d["cell"], fontsize=7.2, weight="bold", color=c,
                transform=ax.transAxes)
        y -= 0.085
        rows = [("pocket-Cα to active", "%.2f $\\rightarrow$ %.2f Å"
                 % (d["full"]["pca"], d["d8"]["pca"])),
                ("NPxxY d(OH,OH)", "%.2f $\\rightarrow$ %.2f Å"
                 % (d["full"]["npxxy"], d["d8"]["npxxy"])),
                ("TM6 tilt", "%.2f $\\rightarrow$ %.2f Å"
                 % (d["full"]["tilt"], d["d8"]["tilt"])),
                ("predicate at depth 8", "FIRES")]
        for lab, val in rows:
            ax.text(0.02, y, lab, fontsize=5.9, color="0.35",
                    transform=ax.transAxes)
            ax.text(0.62, y, val, fontsize=5.9, transform=ax.transAxes)
            y -= 0.068
        ax.text(0.02, y - 0.01, "\n".join(textwrap.wrap(d["verdict"], 46)),
                fontsize=5.9, color=c, va="top", transform=ax.transAxes,
                style="italic")
        y -= 0.24
    ax.set_title("same predicate call, opposite geometry", fontsize=7.4, pad=6)
    fs.panel_label(ax, "c", dx=-0.06, dy=1.12)

    note = (
        "Two (receptor, backbone) cells from the D3 depth ladder, 50 samples each; "
        "a and b plot CELL MEDIANS from GATE-3, whose columns are headed 'med "
        "pca_active', 'med NPxxY' and 'med tilt'. Block D shipped no row table, so "
        "these are SUMMARY values. The open diamonds in b are the single shipped "
        "coordinate file for each cell, measured here from the atoms -- plotted "
        "apart from the medians on purpose, because a one-sample value and a "
        "50-sample median are different objects and confusing them produced a "
        "phantom discrepancy in our own first checker. Both cells clear the "
        "predicate at depth 8. Only one of them has moved toward the active "
        "reference; the other started closer to it and ended further away. Neither "
        "cell is evidence about any other receptor: the depth-8 pocket behaviour is "
        "receptor-dependent on Protenix, which is why Flag D-3 forbids calling it "
        "a lever."
    )
    fig.text(0.012, 0.012, "\n".join(textwrap.wrap(note, 150)), fontsize=5.3,
             va="bottom", color="0.25")

    fs.save(fig, "bd5_lever_vs_degradation")
    print("BD-5 written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
