#!/usr/bin/env python3
"""BD-2 -- steering works in the active direction and does not work in the other.

Spec: dispatch Fig. D2-1.   Claims: SC-D-4, SC-D-5, SC-D-6, SC-D-7.

THE POINT IS THE ASYMMETRY BETWEEN THE TWO PANELS, not any single bar. Left:
supply a partner that should drive the receptor active, and it does. Right:
supply a nanobody that locks the inactive state, and nothing moves -- or it
moves the wrong way. Both panels are on the same axis and the same scale so the
comparison is visual rather than asserted.

THE CAPTION CARRIES C-D-12 AND THAT IS NOT DECORATION. All four nanobody anchor
structures were deposited 2013-2020 and predate every dated backbone cutoff, so
the right-hand panel has a memorization-availability confound that this campaign
could not close. A reader who takes the right panel as "directed inactive
generation is impossible" has read something the data does not support. The
caveat is in the caption, not deferred to a limitations paragraph.

TWO THINGS THIS PANEL MUST NOT SAY, and does not:
  - it must not report the OPRK x Boltz inversion as a majority. The cell is
    48% at n=50 with an exact interval of [33.7, 62.6], which spans 50. The
    interval is drawn and the annotation says "approaches half".
  - it must not present the two OF3 positive-control misses as a failure of the
    control. 14 of 16 cells clear 96%; the control works, and OF3 is the
    exception worth naming.

EVIDENTIAL CLASS: SUMMARY for the rates -- Block D shipped no row table. But the
intervals ARE recomputed: every Clopper-Pearson interval drawn here was
reproduced from k and n by analysis/block_d/verify_claims.py, and all six match
the shipped values to the stated decimal.
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


def main():
    fs.use_house_style()
    fig = plt.figure(figsize=(fs.W2, 120 * fs.MM))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.30,
                          left=0.075, right=0.985, top=0.87, bottom=0.30)
    bbs = fs.BACKBONE_ORDER
    method, why = bd.ci_method("d2")

    # ---- a: the active direction ------------------------------------------
    ax = fig.add_subplot(gs[0, 0])
    x, ticks, labels = 0, [], []
    for i, b in enumerate(bbs):
        d = bd.D2_ACM2_ACTIVE_NB[b]
        c = fs.BACKBONE_COLOURS[b]
        ax.plot([x, x + 0.55], [d["apo"], d["nb"]], color=c, lw=1.4, zorder=2)
        ax.scatter([x], [d["apo"]], s=26, facecolor="white", edgecolor=c,
                   lw=1.2, zorder=3)
        ax.scatter([x + 0.55], [d["nb"]], s=30, color=c, zorder=3)
        lab = ("+%d" % d["delta"]) if d["delta"] else "0 (refuses)"
        ax.text(x + 0.275, max(d["apo"], d["nb"]) + 4, lab, fontsize=6.3,
                ha="center", va="bottom",
                color=c if d["delta"] else fs.GREY)
        ticks.append(x + 0.275)
        labels.append(fs.BACKBONE_LABELS[b])
        x += 1.35
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, fontsize=6.8, rotation=20, ha="right")
    ax.set_ylabel("% of 50 samples called active", fontsize=7.2)
    ax.set_ylim(-6, 124)
    ax.set_title("ACTIVE direction: ACM2, apo (open) $\\rightarrow$ "
                 "active-Nb (filled)", fontsize=7.2, pad=6)
    fs.panel_label(ax, "a", dx=-0.10, dy=1.09)

    # the Ga positive control, as a reference band
    ax.axhspan(96, 100, color=fs.GREEN, alpha=0.13, zorder=0)
    ax.text(0.0, 116, "G$\\alpha$ cognate control (shaded): 14 of 16 cells "
            "$\\geq$96%; both misses are OpenFold-3, ACM2 58% and OPRK 36%",
            fontsize=5.8, ha="left", va="top", color="0.30")

    # ---- b: the inactive direction ----------------------------------------
    ax = fig.add_subplot(gs[0, 1])
    x, ticks, labels = 0, [], []
    for rec in ("ADRB2", "OPRK"):
        for b in bbs:
            apo, nb, delta, verdict = bd.D2_INACTIVE_NB[rec][b]
            c = fs.BACKBONE_COLOURS[b]
            ax.plot([x, x + 0.55], [apo[0], nb[0]], color=c, lw=1.4, zorder=2)
            ax.errorbar([x + 0.55], [nb[0]],
                        yerr=[[nb[0] - nb[1]], [nb[2] - nb[0]]],
                        fmt="o", ms=4, color=c, lw=1.0, capsize=1.8, zorder=3)
            ax.scatter([x], [apo[0]], s=24, facecolor="white", edgecolor=c,
                       lw=1.1, zorder=3)
            if "INVERT" in verdict:
                ax.text(x + 0.275, nb[2] + 4, "+%d" % delta, fontsize=6.3,
                        ha="center", color=fs.VERM, weight="bold")
            ticks.append(x + 0.275)
            labels.append(fs.BACKBONE_LABELS[b])
            x += 1.05
        x += 0.7
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, fontsize=6.0, rotation=38, ha="right")
    ax.set_ylim(-6, 124)
    ax.set_yticklabels([])
    ax.axvline(4.0, color="0.75", lw=0.8)
    ax.text(1.6, 112, "ADRB2", fontsize=7.0, ha="center")
    ax.text(6.0, 112, "OPRK", fontsize=7.0, ha="center")
    ax.text(6.0, 104, "all four move UP", fontsize=5.9, ha="center",
            color=fs.VERM, style="italic")
    ax.set_title("INACTIVE direction: apo $\\rightarrow$ inactive-Nb",
                 fontsize=7.2, pad=6)
    fs.panel_label(ax, "b", dx=-0.06, dy=1.09)

    f = bd.D2_FLAGSHIP
    ax.annotate("%.0f%% [%.1f, %.1f]\nspans 50: %s,\nnot %s"
                % (f["pct"], f["lo"], f["hi"], f["sentence_allowed"],
                   f["sentence_forbidden"]),
                xy=(4.55, f["pct"]), xytext=(2.0, 30), fontsize=5.7,
                ha="left", color="0.25",
                arrowprops=dict(arrowstyle="-", lw=0.7, color="0.55"))

    note = (
        "Both panels: 50 samples per cell, percent called active by the "
        "two-instrument predicate; intervals are exact binomial (Clopper-Pearson) "
        "and every one drawn here was RECOMPUTED from k and n and matches the "
        "shipped value. Tier CI convention is %s -- %s. a: ACM2 is the clean "
        "per-receptor test because AGTR1's apo is already active-biased; Chai does "
        "not move at all. b: the two receptors carrying an inactive-Nb arm. Three "
        "of four ADRB2 cells do not move and Protenix inverts to 76%%; on OPRK all "
        "four move toward ACTIVE under a nanobody that locks the INACTIVE state -- "
        "a systematic Nb-B-as-active prior, not noise. "
        "MEMORIZATION CAVEAT (C-D-12), which bounds every reading of panel b: all "
        "four nanobody anchor structures (5JQH 2016, 6VI4 2020, 4MQS 2013, 6OS2 "
        "2019) predate every DATED backbone training cutoff, and OpenFold-3's "
        "cutoff is recorded as TBD in the shipped table. Whether directed inactive "
        "generation is unachievable, or merely unachievable for complexes the "
        "models have already seen, IS NOT SETTLED BY THIS FIGURE. The post-cutoff "
        "test was attempted and documented, not completed."
        % (method, why))
    fig.text(0.012, 0.008, "\n".join(textwrap.wrap(note, 150)), fontsize=5.3,
             va="bottom", color="0.25")

    fs.save(fig, "bd2_direction_asymmetry")
    print("BD-2 written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
