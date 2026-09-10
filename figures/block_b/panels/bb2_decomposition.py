# -*- coding: utf-8 -*-
"""BB-2 — the ladder decomposition, on both scales.

Spec: data/block_b/12_narrative/figures/BB-2_ladder_decomposition_both_scales.md
Claim: SC-B-2. Standalone panel, no manuscript figure number, no composite.

DEPARTURE FROM THE SPEC, and it is the whole reason panel b looks the way it
does. The spec's panel B.ii asks for the per-backbone family term, and SC-B-2
describes it as "all four backbones agree, 17-21%: boltz 17.4, chai 17.5, of3
20.9, protenix 17.5". THOSE FOUR NUMBERS ARE IN NO SHIPPED FILE. The
term_share column of ladder_decomposition.csv gives 14.2 / 22.9 / 23.6 / 10.9 --
a factor of two, with Protenix the low outlier -- and the panel share of 17.4%
appears to have been copied into three of the four per-backbone slots. This
panel draws what the file says and marks the claimed values so the difference
is visible rather than silently corrected. See D-B-6, D-B-7.
"""
import _shead                                                    # noqa: F401
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
import badata as B

fs.use_house_style()

FRAME = 36
CONTRAST = [("delta_occupancy_apo_to_decoy",        "occupancy\napo to decoy"),
            ("delta_a5ct_sequence_decoy_to_shuffled", u"α5-CT sequence\ndecoy to shuffled"),
            ("delta_correct_family_shuffled_to_cognate", "correct family\nshuffled to cognate")]
TERM_COLOUR = [fs.SKY, fs.GREEN, fs.VERM]
CLAIMED_PER_BB = {"boltz": 17.4, "chai": 17.5, "of3": 20.9, "protenix": 17.5}


def main():
    dec = B.pick_frame(B.table("05_decomposition/ladder_decomposition.csv"), FRAME)
    panel = dec[dec.backbone == "panel"]

    fig, (ax, axb) = fs.figure(width=fs.W2, height=104 * fs.MM, ncols=2,
                               gridspec_kw={"width_ratios": [1.35, 1.0]})

    # ---- a: the three shares, both scales, side by side
    xs = np.arange(2)
    bottom = np.zeros(2)
    for (key, lab), col in zip(CONTRAST, TERM_COLOUR):
        vals = []
        for scale in ("probability", "logit"):
            r = panel[(panel.scale == scale) & (panel.contrast == key)]
            vals.append(100.0 * float(r.term_share.iloc[0]))
        ax.bar(xs, vals, bottom=bottom, width=0.52, color=col,
               edgecolor="white", lw=0.7, label=lab.replace("\n", " "))
        for i, v in enumerate(vals):
            ax.text(xs[i], bottom[i] + v / 2.0, "%.1f%%" % v, ha="center",
                    va="center", fontsize=7.2, fontweight="bold",
                    color="white" if v > 14 else fs.BLACK)
        bottom += np.asarray(vals)

    ax.set_xticks(xs); ax.set_xticklabels(["probability scale", "logit scale"])
    ax.set_ylabel("share of the apo-to-cognate rise (%)")
    ax.set_ylim(0, 104)
    ax.set_title("the same ladder, decomposed on two scales", fontsize=7.4)
    ax.legend(frameon=False, fontsize=6.2, loc="lower center",
              bbox_to_anchor=(0.5, -0.30), ncol=3)
    ax.annotate("", xy=(1.30, 82.6), xytext=(1.30, 88.9),
                arrowprops=dict(arrowstyle="<->", lw=0.9, color=fs.VERM))
    ax.text(1.36, 85.8, u"the family term is the\nonly share that moves:\n"
                        u"11.1% to 17.4%",
            fontsize=6.0, color=fs.VERM, va="center")

    # ---- b: the per-backbone family term, as shipped against as claimed
    fam = "delta_correct_family_shuffled_to_cognate"
    bbs = fs.BACKBONE_ORDER
    got = [100.0 * float(dec[(dec.backbone == b) & (dec.scale == "logit") &
                             (dec.contrast == fam)].term_share.iloc[0]) for b in bbs]
    lo = [float(dec[(dec.backbone == b) & (dec.scale == "logit") &
                    (dec.contrast == fam)].ci_lo.iloc[0]) for b in bbs]
    x = np.arange(len(bbs))
    axb.bar(x, got, width=0.55, color=[fs.BACKBONE_COLOURS[b] for b in bbs],
            edgecolor="white", lw=0.7, zorder=2)
    for i, b in enumerate(bbs):
        axb.plot([x[i] - 0.30, x[i] + 0.30], [CLAIMED_PER_BB[b]] * 2, ls=(0, (2, 1.6)),
                 lw=1.2, color=fs.BLACK, zorder=4)
        axb.text(x[i], got[i] + 0.8, "%.1f" % got[i], ha="center", fontsize=6.4,
                 fontweight="bold")
        if lo[i] <= 0:
            axb.text(x[i], 1.0, u"CI spans 0", ha="center", fontsize=5.6,
                     color="white", rotation=90, va="bottom", fontweight="bold")
    axb.axhline(100.0 * float(panel[(panel.scale == "logit") &
                                    (panel.contrast == fam)].term_share.iloc[0]),
                color=fs.GREY, lw=0.8, ls=":", zorder=1)
    axb.set_xticks(x); axb.set_xticklabels([fs.BACKBONE_LABELS[b] for b in bbs],
                                           rotation=20, ha="right")
    axb.set_ylabel("family term, logit share (%)")
    axb.set_ylim(0, 27)
    axb.set_title("the family term is not a consensus", fontsize=7.4)
    axb.plot([], [], ls=(0, (2, 1.6)), lw=1.2, color=fs.BLACK,
             label="value claimed in SC-B-2")
    axb.plot([], [], ls=":", lw=0.8, color=fs.GREY, label="panel value, 17.4%")
    axb.legend(frameon=False, fontsize=6.0, loc="upper left")

    fs.panel_label(ax, "a", dx=-0.14)
    fs.panel_label(axb, "b", dx=-0.20)

    note = (u"Class A, frame_%d (n=36 receptors; EDNRA, EDNRB, GRPR and HRH3 "
            u"excluded because NPxxY position 7.53 is Leu not Tyr). Shares are "
            u"read from ladder_decomposition.csv, which labels this frame "
            u"reproduction_36 where every other table says frame_36. "
            u"a, the three telescoping terms as a share of the total rise; the "
            u"probability and logit columns describe the same ladder. The family "
            u"share differs between them because cognate rates are at or above "
            u"0.98 in 24-34 of 40 cells per backbone, leaving a probability-scale "
            u"difference little room to move (C-B-7). Neither scale is the "
            u"correct one and every mention of this term names its scale."
            % FRAME)
    warn = (u"b, dashed lines are the four per-backbone shares SC-B-2 states "
            u"(17.4 / 17.5 / 20.9 / 17.5, described there as "all four "
            u"backbones agree, 17-21%"). The bars are what the shipped file "
            u"contains: 14.2 / 22.9 / 23.6 / 10.9, a factor of two, with Protenix "
            u"lowest. The panel share of 17.4% reproduces exactly and appears to "
            u"have been copied into three of the four per-backbone slots. Three "
            u"of the four intervals span zero, OpenFold3's alone excludes it, and "
            u"Protenix's runs to [-0.047, +5.148] against a claimed "[0.35, "
            u"1.05] squarely positive". D-B-6, D-B-7.")
    fig.text(0.01, -0.10, "\n".join(textwrap.wrap(note, 130)),
             fontsize=5.4, color=fs.GREY, va="top", ha="left")
    fig.text(0.01, -0.215, "\n".join(textwrap.wrap(warn, 130)),
             fontsize=5.4, color=fs.VERM, va="top", ha="left")

    paths = fs.save(fig, "bb2_decomposition")
    print("BB-2 ->", paths[0])
    for scale in ("probability", "logit"):
        row = ["%s %.1f%%" % (k.split("_")[1], 100 * float(
            panel[(panel.scale == scale) & (panel.contrast == k)].term_share.iloc[0]))
            for k, _ in CONTRAST]
        print("  %-12s %s" % (scale, "  ".join(row)))
    print("  per-backbone family logit share, shipped : %s"
          % dict(zip(bbs, [round(g, 1) for g in got])))
    print("  per-backbone family logit share, claimed : %s" % CLAIMED_PER_BB)


if __name__ == "__main__":
    main()
