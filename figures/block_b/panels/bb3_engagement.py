# -*- coding: utf-8 -*-
"""BB-3 — engagement and activation are separable, and the interesting cell is
the one where they disagree.

Spec: data/block_b/12_narrative/figures/BB-3_2x2_engagement_activation.md
Claim: SC-B-3. Standalone panel, no manuscript figure number, no composite.

The engaged-but-inactive decoy cell is the only cell in Block B that can support
a statement about chemistry rather than occupancy, so this panel exists to show
that it is populated on every backbone and to show how much of it survives a
tighter cutoff. C-B-6 flags the 20 A cutoff as permissive -- roughly four times
the cognate median insertion depth of 12.19 A -- so the sweep is not decoration.
"""
import _shead                                                    # noqa: F401
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
import badata as B

fs.use_house_style()

FRAME = 36
#: apo supplies no partner, so p(engaged) is 0 and p(active|engaged) is undefined.
#: It is not a missing value and it is not drawn as one -- it is excluded from
#: both engagement panels and named in the note.
ARMS = ["decoy", "shuffled", "cognate"]
ARM_COL = {"apo": fs.GREY, "decoy": fs.VERM, "shuffled": fs.SKY, "cognate": fs.GREEN}


def main():
    i2 = B.table("06_interface/interface_2x2.csv")
    i2 = i2[(i2.frame == "frame_%d" % FRAME) & (i2.predicate == "two_instrument")]
    at20 = i2[i2.cutoff_A == 20]
    panel = at20[at20.backbone == "panel_all"]

    fig, (ax, axs, axn) = fs.figure(width=fs.W2, height=98 * fs.MM, ncols=3,
                                    gridspec_kw={"width_ratios": [1.0, 1.05, 0.95]})

    # ---- a: where each arm sits in the engagement x activation plane
    for arm in ARMS:
        r = panel[panel.arm == arm]
        if not len(r):
            continue
        pe, pa = float(r.p_engaged.iloc[0]), float(r.p_active_given_engaged.iloc[0])
        ax.errorbar(pe, pa,
                    xerr=[[pe - float(r.p_engaged_lo95.iloc[0])],
                          [float(r.p_engaged_hi95.iloc[0]) - pe]],
                    yerr=[[pa - float(r.p_agv_lo95.iloc[0])],
                          [float(r.p_agv_hi95.iloc[0]) - pa]],
                    marker="o", ms=7, lw=1.4, capsize=2.5, color=ARM_COL[arm],
                    zorder=3)
        ax.annotate(arm, (pe, pa), textcoords="offset points", xytext=(0, 11),
                    ha="center", fontsize=6.8, fontweight="bold",
                    color=ARM_COL[arm])
    ax.set_xlabel("p(partner engaged)")
    ax.set_ylabel("p(receptor active | engaged)")
    ax.set_xlim(0.60, 1.03); ax.set_ylim(0.60, 1.00)
    ax.set_title(u"engagement and activation move together,\nbut not by the same amount",
                 fontsize=7.2)

    # ---- b: the cutoff sweep, which is what makes 20 A a choice rather than a fact
    for arm in ARMS:
        s = i2[(i2.arm == arm) & (i2.backbone == "panel_all")].sort_values("cutoff_A")
        if not len(s):
            continue
        axs.plot(s.cutoff_A, s.p_active_given_engaged, marker="o", ms=3.2, lw=1.3,
                 color=ARM_COL[arm], label=arm)
    axs.axvline(20, color=fs.BLACK, lw=0.8, ls="--")
    axs.axvline(12.19, color=fs.GREY, lw=0.8, ls=":")
    axs.text(20, 0.42, " the 20 A cutoff\n used everywhere", fontsize=5.8,
             color=fs.BLACK, va="bottom")
    axs.text(12.19, 0.42, "cognate median\ninsertion depth ", fontsize=5.8,
             color=fs.GREY, va="bottom", ha="right")
    axs.set_xlabel(u"engagement cutoff, tip to R3.50 (Å)")
    axs.set_ylabel("p(active | engaged)")
    axs.set_ylim(0.38, 1.0)
    axs.set_title("the cognate arm is flat under the sweep;\nthe decoy arm is not",
                  fontsize=7.2)
    axs.legend(frameon=False, fontsize=6.2, loc="upper left")

    # ---- c: the mechanism cell, per backbone
    bbs = fs.BACKBONE_ORDER
    dec = at20[(at20.arm == "decoy") & (at20.backbone != "panel_all")]
    n = [int(dec[dec.backbone == b].n_engaged_but_inactive.iloc[0]) for b in bbs]
    x = np.arange(len(bbs))
    axn.bar(x, n, width=0.55, color=[fs.BACKBONE_COLOURS[b] for b in bbs],
            edgecolor="white", lw=0.7)
    for i, v in enumerate(n):
        axn.text(x[i], v + 12, "%d" % v, ha="center", fontsize=6.6, fontweight="bold")
    axn.axhline(5, color=fs.VERM, lw=1.0, ls="--")
    axn.text(len(bbs) - 0.5, 22, u"n ≥ 5 floor", fontsize=5.8, color=fs.VERM,
             ha="right")
    axn.set_xticks(x)
    axn.set_xticklabels([fs.BACKBONE_LABELS[b] for b in bbs], rotation=20, ha="right")
    axn.set_ylabel("decoy rows engaged but not active")
    axn.set_ylim(0, max(n) * 1.22)
    axn.set_title("the chemistry cell is populated\non every backbone", fontsize=7.2)

    for a, l in ((ax, "a"), (axs, "b"), (axn, "c")):
        fs.panel_label(a, l, dx=-0.22)

    tot = int(at20[(at20.arm == "decoy") &
                   (at20.backbone == "panel_all")].n_engaged_but_inactive.iloc[0])
    note = (u"Class A, frame_%d, two-instrument predicate, cluster-bootstrap 95%% "
            u"intervals over paralog clusters. Engagement is the alpha5 tip to "
            u"R3.50 Calpha distance thresholded at 20 A; it is NOT part of the "
            u"activation predicate and no panel treats it as one. "
            u"The apo arm is absent from a and b by construction, not by omission: with no "
            u"partner supplied, p(engaged) is 0 and p(active | engaged) is undefined. "
            u"a, panel-level rates for the three partner arms. b, the same quantity swept across "
            u"every cutoff the drop ships: the cognate arm barely moves "
            u"(0.897 to 0.893 from 10 to 20 A) while the decoy arm moves from "
            u"0.53 to 0.66, so the cutoff is load-bearing on decoy and permissive "
            u"on cognate (C-B-6). c, the engaged-but-inactive decoy cell, %d rows "
            u"pooled and %d-%d per backbone, far above the 5-row floor the "
            u"mechanism claim needs."
            % (FRAME, tot, min(n), max(n)))
    fig.text(0.01, -0.09, "\n".join(textwrap.wrap(note, 132)),
             fontsize=5.4, color=fs.GREY, va="top", ha="left")

    paths = fs.save(fig, "bb3_engagement")
    print("BB-3 ->", paths[0])
    for arm in ARMS:
        r = panel[panel.arm == arm]
        if len(r):
            print("  %-9s p(engaged) %.4f   p(active|engaged) %.4f"
                  % (arm, r.p_engaged.iloc[0], r.p_active_given_engaged.iloc[0]))
    print("  engaged-but-inactive decoy: %d pooled, %s per backbone"
          % (tot, dict(zip(bbs, n))))


if __name__ == "__main__":
    main()
