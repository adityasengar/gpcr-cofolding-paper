# -*- coding: utf-8 -*-
"""BC-2 — the pre-registered ordinal test, per receptor.

Spec: analysis/block_c/panels/BC-2_ordinal_recovery.md   Claim: SC-C-2.

PER-RECEPTOR PANEL. s5_p4_ordinal.json turned out to carry a Kendall's tau for
every receptor, not just the panel medians -- so unlike BC-1 and BC-3 this one
draws the distribution rather than a summary of it. That is why it is the panel
worth trusting most in this block.
"""
import _shead                                                    # noqa: F401
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
import bcdata as B

fs.use_house_style()
PANELS = [("tier3_apo_23_receptors", "23 receptors"),
          ("tier3_apo_15_receptors_selfref_excluded", "15, self-ref excluded")]


def main():
    o = B.J("07_ordinal_recovery/s5_p4_ordinal.json")
    fig, axes = fs.figure(width=fs.W2, height=92 * fs.MM, ncols=2)
    rng = np.random.default_rng(3)

    for ax, (key, lab) in zip(axes, PANELS):
        per = o[key]["per_backbone"]
        for i, bb in enumerate(B.BACKBONES):
            taus = np.array([v["tau"] for v in per[bb].values()], dtype=float)
            taus = taus[np.isfinite(taus)]
            parts = ax.violinplot([taus], positions=[i], widths=0.74,
                                  showextrema=False, showmedians=False)
            for b in parts["bodies"]:
                b.set_facecolor(fs.BACKBONE_COLOURS[bb]); b.set_alpha(0.28)
                b.set_edgecolor("none")
            ax.scatter(i + rng.uniform(-0.15, 0.15, len(taus)), taus, s=6.0,
                       color=fs.BACKBONE_COLOURS[bb], alpha=0.75, lw=0, zorder=3)
            m = float(np.median(taus))
            ax.plot([i - 0.30, i + 0.30], [m, m], lw=2.3,
                    color=fs.BACKBONE_COLOURS[bb], zorder=4)
            ax.annotate("%.2f" % m, (i, m), textcoords="offset points",
                        xytext=(21, -2), fontsize=6.2, fontweight="bold",
                        color=fs.BACKBONE_COLOURS[bb])
            fs.annotate_n(ax, i, len(taus))
            # the quantity SC-C-2's table calls "Kendall's tau" is this, and it
            # is a COUNT OF RECEPTORS, not a correlation (D-C-3)
            frac = o[key]["summary"][bb]["fraction_positive_significant"]
            ax.plot([i - 0.30, i + 0.30], [frac, frac], lw=1.3, ls=(0, (3, 2)),
                    color=fs.BLACK, zorder=6)
            ax.annotate("%.0f%%" % (100 * frac), (i, frac),
                        textcoords="offset points", xytext=(0, 5),
                        ha="center", fontsize=5.9, color=fs.BLACK)
        ax.axhline(0, color=fs.GREY, lw=0.8, zorder=1)
        ax.set_xticks(range(len(B.BACKBONES)))
        ax.set_xticklabels([fs.BACKBONE_LABELS[b] for b in B.BACKBONES],
                           rotation=20, ha="right")
        ax.set_ylim(-0.55, 1.0)
        ax.set_title(lab, fontsize=7.4)
    axes[0].set_ylabel(u"Kendall's τ, ligand-role rank against the continuous axis")
    axes[1].plot([], [], ls=(0, (3, 2)), lw=1.3, color=fs.BLACK,
                 label="fraction of receptors with positive, significant τ")
    axes[1].legend(frameon=False, fontsize=5.8, loc="lower right")

    fs.panel_label(axes[0], "a", dx=-0.20); fs.panel_label(axes[1], "b", dx=-0.14)

    note = (u"One point per receptor. τ is the rank correlation between ligand "
            u"role and the difference in pocket-Cα RMSD to the active versus the "
            u"inactive reference, computed within receptor on the apo arm. "
            u"THE THRESHOLD FOR THIS TEST WAS LOCKED BEFORE THE CAMPAIGN RAN, "
            u"which is why it carries weight the 2×2 does not: it could have "
            u"failed. Both panel definitions are shown because showing only the "
            u"more favourable one is the error the pose result in this same block "
            u"already made and corrected. Negative values are receptors where the "
            u"ordering runs backwards; they are drawn, not trimmed.")
    fig.text(0.01, -0.10, "\n".join(textwrap.wrap(note, 132)), fontsize=5.4,
             color=fs.GREY, va="top", ha="left")

    p = fs.save(fig, "bc2_ordinal")
    print("BC-2 ->", p[0])
    for key, lab in PANELS:
        per = o[key]["per_backbone"]
        s = " ".join("%s %.2f" % (b, np.median([v["tau"] for v in per[b].values()]))
                     for b in B.BACKBONES)
        print("  %-24s %s" % (lab, s))


if __name__ == "__main__":
    main()
