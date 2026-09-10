# -*- coding: utf-8 -*-
"""BC-3 — prospective ligand-class discrimination, on two backbones of four.

Spec: analysis/block_c/panels/BC-3_loro_classifier.md   Claim: SC-C-4.

SUMMARY PANEL: g1_bootstrap_s1_auroc.json ships intervals and the permutation
null but not the per-receptor LORO folds.

THE ONE THING THIS PANEL MUST NOT DO is let a reader read Chai-1 and OpenFold3
as negative. Their intervals span 0.5, which means the test cannot distinguish
them from chance. That is not the same as showing they carry no signal, and the
difference decides whether the paper says two backbones work or two fail.
"""
import _shead                                                    # noqa: F401
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
import bcdata as B

fs.use_house_style()


def main():
    g = B.J("04_classifier/g1_bootstrap_s1_auroc.json")["per_backbone"]
    order = sorted(B.BACKBONES, key=lambda b: -g[b]["observed_pooled_auroc"])
    fig, ax = fs.figure(width=fs.W15, height=76 * fs.MM)
    y = np.arange(len(order))[::-1]

    for i, bb in enumerate(order):
        r = g[bb]; k = r["cluster_boot"]; obs = r["observed_pooled_auroc"]
        pn = r["permutation_null"]["ci_95"]
        scoped = k["ci_95"][0] > 0.5
        ax.plot(pn, [y[i]] * 2, lw=5.0, color="#D8D4CE", solid_capstyle="butt",
                zorder=1)
        ax.errorbar(obs, y[i], xerr=[[obs - k["ci_95"][0]], [k["ci_95"][1] - obs]],
                    fmt="o", ms=6.5, lw=1.9, capsize=3.0,
                    color=fs.BACKBONE_COLOURS[bb],
                    mfc=fs.BACKBONE_COLOURS[bb] if scoped else "white", zorder=4)
        ax.plot(k["median"], y[i], marker="|", ms=9, mew=1.6,
                color=fs.BACKBONE_COLOURS[bb], zorder=5)
        ax.text(1.005, y[i], "%.3f  [%.3f, %.3f]" % (obs, k["ci_95"][0], k["ci_95"][1]),
                fontsize=6.1, va="center")
        ax.text(0.30, y[i], "scoped in" if scoped else "inconclusive",
                fontsize=6.1, va="center", ha="right", fontweight="bold",
                color=fs.BLACK if scoped else fs.VERM)

    ax.axvline(0.5, color=fs.VERM, lw=1.1, zorder=2)
    ax.set_yticks(y); ax.set_yticklabels([fs.BACKBONE_LABELS[b] for b in order],
                                         fontsize=7)
    ax.set_xlim(0.30, 1.30); ax.set_xticks(np.arange(0.4, 1.01, 0.1))
    ax.set_xlabel("LORO AUROC, ligand class from a single predicted structure")
    ax.set_title(u"prospective discrimination on two backbones of four", fontsize=7.6)
    ax.plot([], [], lw=5, color="#D8D4CE", label="permutation null, 95%")
    ax.plot([], [], marker="|", ls="none", ms=9, mew=1.6, color=fs.GREY,
            label="bootstrap median")
    ax.plot([], [], "o", ms=6, mfc="white", color=fs.GREY,
            label="open marker: interval spans 0.5")
    ax.legend(frameon=False, fontsize=5.9, loc="lower left", ncol=3,
              bbox_to_anchor=(0.0, -0.30))

    note = (u"n=15 receptors, self-reference excluded — not the 23 of the 2×2 nor "
            u"the 36 of the panel; the three counts are different inclusion rules "
            u"on the same campaign and are not reconciled. Cluster bootstrap over "
            u"12 paralog clusters, 500 iterations. "
            u"CHAI-1 AND OPENFOLD3 ARE INCONCLUSIVE, NOT NEGATIVE: their intervals "
            u"reach 0.351 and 0.382, so the test cannot distinguish them from "
            u"chance, which is a different statement from showing they carry no "
            u"signal. Both scoped backbones exclude the permutation null, which is "
            u"a stronger claim than clearing 0.5. Boltz-2's bootstrap median "
            u"(0.809, tick) sits below its point estimate (0.852): if one number "
            u"leaves this panel, it should be the interval.")
    fig.text(0.01, -0.16, "\n".join(textwrap.wrap(note, 120)), fontsize=5.4,
             color=fs.GREY, va="top", ha="left")

    p = fs.save(fig, "bc3_classifier")
    print("BC-3 ->", p[0])
    for bb in order:
        k = g[bb]["cluster_boot"]
        print("  %-9s %.3f  [%.3f, %.3f]  median %.3f  %s"
              % (bb, g[bb]["observed_pooled_auroc"], k["ci_95"][0], k["ci_95"][1],
                 k["median"], "scoped" if k["ci_95"][0] > 0.5 else "INCONCLUSIVE"))


if __name__ == "__main__":
    main()
