# -*- coding: utf-8 -*-
"""BB-6 — the ladder, per receptor, so the panel mean cannot hide the spread.

Spec: data/block_b/12_narrative/figures/BB-6_per_receptor_ladder.md
Claim: SC-B-1, at receptor grain. Standalone panel, no composite.

The panel-level ladder in BB-1 is a mean over receptors. This shows every
receptor's own ladder underneath it, which is the panel a reader reaches for
when they suspect a mean is carrying a bimodal population -- and here it is,
because ceiling-pinning puts 115 of 160 cognate cells at or above 0.98.
"""
import _shead                                                    # noqa: F401
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
import badata as B

fs.use_house_style()
FRAME, ARMS = 36, B.ARM_ORDER


def main():
    pr = B.table("04_ladder/ladder_per_receptor.csv")
    keep = ~pr.receptor.isin(B.NPXXY_UNDEFINED)
    pr = pr[keep]

    fig, (ax, axh) = fs.figure(width=fs.W2, height=96 * fs.MM, ncols=2,
                               gridspec_kw={"width_ratios": [1.45, 1.0]})

    x = np.arange(len(ARMS))
    cols = ["%s_rate" % a for a in ARMS]
    for bb in fs.BACKBONE_ORDER:
        sub = pr[pr.backbone == bb]
        for _, row in sub.iterrows():
            ax.plot(x, [row[c] for c in cols], lw=0.45, alpha=0.28,
                    color=fs.BACKBONE_COLOURS[bb], zorder=2)
    med = [pr[c].median() for c in cols]
    ax.plot(x, med, lw=2.6, color=fs.BLACK, marker="s", ms=5, zorder=5,
            label="median receptor")
    ax.set_xticks(x); ax.set_xticklabels(ARMS)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("input arm")
    ax.set_ylabel("that receptor's own active-call fraction")
    ax.set_title(u"every receptor's ladder, %d cells" % len(pr), fontsize=7.4)
    ax.legend(frameon=False, fontsize=6.2, loc="upper left")

    # ---- b: the distribution at each rung, which is what the mean hides
    for i, (a, c) in enumerate(zip(ARMS, cols)):
        v = pr[c].dropna().to_numpy()
        parts = axh.violinplot([v], positions=[i], widths=0.75,
                               showextrema=False, showmedians=False)
        for b in parts["bodies"]:
            b.set_facecolor(fs.SKY if a != "cognate" else fs.GREEN)
            b.set_alpha(0.35); b.set_edgecolor("none")
        rng = np.random.default_rng(11)
        axh.scatter(i + rng.uniform(-0.16, 0.16, len(v)), v, s=3.2, lw=0,
                    color=fs.BLACK, alpha=0.45, zorder=3)
        pin = int((v >= 0.98).sum())
        axh.text(i, 1.045, "%d at\nthe ceiling" % pin, ha="center", fontsize=5.6,
                 color=fs.VERM if pin > 20 else fs.GREY)
    axh.axhline(0.98, color=fs.VERM, lw=0.8, ls="--", zorder=1)
    axh.set_xticks(range(len(ARMS))); axh.set_xticklabels(ARMS)
    axh.set_ylim(-0.03, 1.14)
    axh.set_ylabel("per-receptor rate")
    axh.set_title("the mean hides a ceiling", fontsize=7.4)

    fs.panel_label(ax, "a", dx=-0.13); fs.panel_label(axh, "b", dx=-0.20)

    pinned = int((pr.cognate_rate >= 0.98).sum())
    note = (u"One line per receptor x backbone cell, %d cells over %d receptors "
            u"and four backbones; frame_%d, so EDNRA, EDNRB, GRPR and HRH3 are "
            u"absent because their NPxxY axis is undefined. Rates are read from "
            u"ladder_per_receptor.csv, whose cognate values were computed with the "
            u"untruncated NPxxY threshold 9.082 while every row carries 9.08; the "
            u"two differ on five rows of 32,000 and on one cell "
            u"(AA2AR/Chai-1/decoy, 0.90 against 0.88 recomputed). "
            u"b, %d of %d cognate cells sit at or above 0.98. That ceiling is why "
            u"the correct-family term is small on the probability scale and larger "
            u"on the logit scale, and why both are reported (C-B-7)."
            % (len(pr), pr.receptor.nunique(), FRAME, pinned,
               int(pr.cognate_rate.notna().sum())))
    fig.text(0.01, -0.095, "\n".join(textwrap.wrap(note, 132)),
             fontsize=5.4, color=fs.GREY, va="top", ha="left")

    paths = fs.save(fig, "bb6_per_receptor")
    print("BB-6 ->", paths[0])
    print("  %d cells over %d receptors" % (len(pr), pr.receptor.nunique()))
    for a, c in zip(ARMS, cols):
        print("   %-9s median %.3f  min %.3f  max %.3f  at ceiling %d"
              % (a, pr[c].median(), pr[c].min(), pr[c].max(), int((pr[c] >= 0.98).sum())))


if __name__ == "__main__":
    main()
