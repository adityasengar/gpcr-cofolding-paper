#!/usr/bin/env python3
"""BD-3 -- MSA depth moves the predicate on all four backbones, by two mechanisms.

Spec: dispatch Fig. D3-1.   Claim: SC-D-8.   Binding: Flag D-2, Flag D-3.

THE WHOLE FIGURE IS THE GAP BETWEEN TWO LINES. Where the predicate-active line
and the sub-Angstrom-to-active line move together, shallow MSAs are steering the
model toward the active state (Boltz, Chai). Where they diverge -- the predicate
clears while the pocket moves AWAY from the active reference -- shallow MSAs are
degrading the model into something the coarse predicate happens to accept (OF3,
Protenix). One axis cannot tell those apart, which is why the original D3
headline was withdrawn as W-D-5.

FLAG D-3 IS ENFORCED HERE, NOT TRUSTED TO THE CAPTION. OF3 and Protenix carry
the LARGEST slopes and the WEAKEST claim, so every panel prints its own
mechanism verdict from `bddata.MECHANISM`, and the two degradation panels are
shaded. A reader who looks only at the slope numbers would rank the backbones
exactly backwards.

FLAG D-2: the unit is %/ln(depth). Under log10 Boltz reads -3.877 rather than
-1.684, a factor of 2.303. The axis label comes from `bddata.SLOPE_UNIT` and
there is no other string available.

EVIDENTIAL CLASS: SUMMARY. Transcribed from PARTA_D3 section 1 and GATE-3
section 1; Block D shipped no row table. The four slopes were independently
refitted by GATE-2 and reproduce exactly under ln with full=4096 -- but their
cluster-boot intervals rest on draws that are not shipped, so the intervals are
drawn as stated values, not as recomputed ones.
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
    fig = plt.figure(figsize=(fs.W2, 132 * fs.MM))
    gs = fig.add_gridspec(2, 4, height_ratios=[1.0, 0.62], hspace=0.75,
                          wspace=0.24, left=0.068, right=0.985,
                          top=0.90, bottom=0.235)

    depths = bd.D3_DEPTHS
    xlab = ["8", "32", "128", "512", bd.D3_FULL_LABEL]

    for j, b in enumerate(fs.BACKBONE_ORDER):
        ax = fig.add_subplot(gs[0, j])
        lad = bd.D3_LADDER[b]
        verdict, why = bd.MECHANISM[b]
        degrading = "DEGRAD" in verdict or "MIXED" in verdict
        if degrading:
            ax.set_facecolor("#fdf1ec")

        ax.plot(depths, lad["predicate"], "-o", ms=3.4, lw=1.5,
                color=fs.VERM, label="predicate-active")
        ax.plot(depths, lad["suba_active"], "-s", ms=3.2, lw=1.5,
                color=fs.BLUE, label="sub-Å pocket-Cα to active")
        ax.set_xscale("log")
        ax.set_xticks(depths)
        ax.set_xticklabels(xlab, fontsize=6.2)
        ax.minorticks_off()
        ax.set_ylim(-4, 78)
        if j:
            ax.set_yticklabels([])
        else:
            ax.set_ylabel("% of 50 samples per cell", fontsize=7.0)
        ax.set_title(fs.BACKBONE_LABELS[b], fontsize=7.4, pad=13)

        sl, lo, hi, signed = bd.D3_SLOPES[b]
        ax.text(0.5, 1.055, "%.2f [%.2f, %.2f] %s" % (sl, lo, hi, bd.SLOPE_UNIT),
                transform=ax.transAxes, ha="center", fontsize=5.9,
                color="black" if signed else fs.GREY)
        ax.text(0.5, -0.235, verdict, transform=ax.transAxes, ha="center",
                fontsize=6.3, weight="bold",
                color=fs.VERM if degrading else fs.GREEN)
        if j == 0:
            ax.legend(fontsize=5.6, frameon=False, loc="upper right")
        fs.panel_label(ax, "abcd"[j], dx=-0.12, dy=1.20)

    # ---- e: the structural-integrity view of the same split ----------------
    ax = fig.add_subplot(gs[1, :2])
    y = np.arange(4)
    for i, b in enumerate(fs.BACKBONE_ORDER):
        lo, hi = bd.D3_MATCHED_SEED_CA[b]
        ax.barh(y[i], hi - lo, left=lo, height=0.55,
                color=fs.BACKBONE_COLOURS[b], alpha=0.85)
        ax.text(hi + 0.5, y[i], "%d–%d Å" % (lo, hi), va="center", fontsize=6.0)
    ax.set_yticks(y)
    ax.set_yticklabels([fs.BACKBONE_LABELS[b] for b in fs.BACKBONE_ORDER],
                       fontsize=6.6)
    ax.invert_yaxis()
    ax.set_xlim(0, 26)
    ax.set_xlabel("matched-seed 7TM Cα deviation, full $\\rightarrow$ depth 8 (Å)",
                  fontsize=6.8)
    ax.set_title("the same split, seen structurally", fontsize=7.2, pad=5)
    fs.panel_label(ax, "e", dx=-0.155, dy=1.16)

    # ---- f: sub-A delta and pLDDT delta, the two converging lines ----------
    ax = fig.add_subplot(gs[1, 2:])
    w = 0.34
    for i, b in enumerate(fs.BACKBONE_ORDER):
        sd = bd.D3_SUBA_DELTA[b]
        if sd is not None:
            ax.bar(i - w / 2, sd, width=w, color=fs.BLUE)
            ax.text(i - w / 2, sd + (1.4 if sd > 0 else -1.4), "%+.1f" % sd,
                    ha="center", va="bottom" if sd > 0 else "top", fontsize=5.8)
        else:
            ax.text(i - w / 2, 1.5, "n/r", ha="center", fontsize=5.8,
                    color=fs.GREY)
        pd = bd.D3_PLDDT_DELTA[b]
        ax.bar(i + w / 2, pd, width=w, color=fs.GREY)
        ax.text(i + w / 2, pd - 1.4, "%+.1f" % pd, ha="center", va="top",
                fontsize=5.8)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(range(4))
    ax.set_xticklabels([fs.BACKBONE_LABELS[b] for b in fs.BACKBONE_ORDER],
                       fontsize=6.4, rotation=18, ha="right")
    ax.set_ylabel("change, full $\\rightarrow$ depth 8", fontsize=6.8)
    ax.set_ylim(-26, 16)
    ax.set_title("blue: sub-Å-to-active (pts).   grey: median pLDDT",
                 fontsize=6.6, pad=5)
    fs.panel_label(ax, "f", dx=-0.135, dy=1.16)

    method, why_ci = bd.ci_method("d3")
    note = (
        "a-d: 26 receptors, apo arm only, 50 samples per (receptor, backbone, depth) "
        "cell, transcribed from PARTA_D3 section 1 -- SUMMARY values; Block D shipped "
        "no row table. Depth 'full' is fitted as 4096, which is the only value under "
        "which the four headline slopes reproduce (GATE-2). Slope unit is %s, NOT "
        "%%/log10: the same fits under common log read -3.877 for Boltz, a factor of "
        "2.303. Intervals above each panel are %s over %s. Chai's crosses zero and is "
        "printed grey; its slope is a point estimate only. SHADED PANELS ARE NOT "
        "LEVERS. OpenFold-3 and Protenix carry the two largest slopes and the two "
        "weakest claims: on OpenFold-3 the predicate rises while sub-Å-to-active "
        "falls 20.9 points, and e shows the backbone moving 10-14 Å and 16-20 Å "
        "between matched seeds while Boltz moves 1-4 Å. f: the two deltas that "
        "separate steering from degradation -- the backbones whose pLDDT tracks depth "
        "most strongly are exactly the two whose pockets move away from the active "
        "reference. Nothing in this figure is pooled across backbones."
        % (bd.SLOPE_UNIT, method, why_ci))
    fig.text(0.012, 0.008, "\n".join(textwrap.wrap(note, 152)), fontsize=5.3,
             va="bottom", color="0.25")

    fs.save(fig, "bd3_depth_ladder")
    print("BD-3 written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
