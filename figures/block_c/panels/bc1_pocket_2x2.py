# -*- coding: utf-8 -*-
"""BC-1 — agonist and antagonist pockets separate. INTENDED apo arm only.

The apo-only scope was the design intent and is NOT what shipped: the row counts
in stage3_2x2_ligand_state_specificity.json are 2,800 and 2,300 per backbone
against an apo-only expectation of 28x50=1,400 and 23x50=1,150, at a grid the
placement census fixes at exactly 50 rows per receptor x backbone x role x arm
(800 cells, unique size 50). Both arms are pooled. Pinned by check C60.

Spec: analysis/block_c/panels/BC-1_pocket_2x2.md   Claim: SC-C-1.
Standalone, spec ID only, no manuscript figure number, no composite.

SUMMARY PANEL. rows.tier3.v2.csv was not shipped, so the 23 per-receptor values
behind each mean do not exist here. The panel says so on its face rather than
letting four tidy intervals imply a distribution nobody has seen.
"""
import _shead                                                    # noqa: F401
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
import bcdata as B

fs.use_house_style()
CELLS = [("agonist_active", "agonist\nvs active ref", fs.VERM),
         ("agonist_inactive", "agonist\nvs inactive ref", fs.VERM),
         ("antag_active", "antagonist\nvs active ref", fs.BLUE),
         ("antag_inactive", "antagonist\nvs inactive ref", fs.BLUE)]


def main():
    st = B.J("06_2x2_interaction/stage3_2x2_ligand_state_specificity.json")["per_backbone"]
    cb = B.J("06_2x2_interaction/g_scc1_cluster_boot.json")["per_backbone"]

    fig, (ax, axi) = fs.figure(width=fs.W2, height=94 * fs.MM, ncols=2,
                               gridspec_kw={"width_ratios": [1.5, 1.0]})

    # ---- a: the four cells, per backbone
    w, x = 0.19, np.arange(len(CELLS))
    for k, bb in enumerate(B.BACKBONES):
        c = st[bb]["cells"]
        off = (k - 1.5) * w
        est = [c[n]["est"] for n, _, _ in CELLS]
        lo = [c[n]["est"] - c[n]["ci_lo"] for n, _, _ in CELLS]
        hi = [c[n]["ci_hi"] - c[n]["est"] for n, _, _ in CELLS]
        ax.errorbar(x + off, est, yerr=[lo, hi], fmt="o", ms=4.0, lw=1.1,
                    capsize=2.0, color=fs.BACKBONE_COLOURS[bb],
                    label=fs.BACKBONE_LABELS[bb])
    ax.axvline(1.5, color=fs.GREY, lw=0.7, ls=":")
    ax.set_xticks(x); ax.set_xticklabels([l for _, l, _ in CELLS], fontsize=6.2)
    ax.set_ylabel(u"pocket-Cα RMSD to that reference (Å)")
    ax.set_title(u"the 2×2: which reference each ligand class lands nearer",
                 fontsize=7.4)
    ax.legend(frameon=False, fontsize=6.0, loc="upper left", ncol=2)

    # ---- b: the interaction, cluster-boot primary
    y = np.arange(len(B.BACKBONES))[::-1]
    for i, bb in enumerate(B.BACKBONES):
        r = cb[bb]; k = r["cluster_boot"]; rb = r["receptor_boot_recomputed"]
        est = r["point_estimate"]
        axi.errorbar(est, y[i] + 0.13,
                     xerr=[[est - k["ci_lo"]], [k["ci_hi"] - est]], fmt="o",
                     ms=5.2, lw=1.8, capsize=2.6, color=fs.BACKBONE_COLOURS[bb],
                     zorder=3)
        axi.errorbar(est, y[i] - 0.16,
                     xerr=[[est - rb["ci_lo"]], [rb["ci_hi"] - est]], fmt="o",
                     ms=2.8, lw=0.8, capsize=1.6, color=fs.GREY, zorder=2)
        axi.text(k["ci_hi"] + 0.012, y[i] + 0.13, "%.3f" % est, fontsize=6.2,
                 va="center", fontweight="bold")
    axi.axvline(0, color=fs.VERM, lw=1.1, zorder=1)
    axi.set_yticks(y); axi.set_yticklabels([fs.BACKBONE_LABELS[b] for b in B.BACKBONES],
                                           fontsize=6.6)
    axi.set_xlabel(u"2×2 interaction (Å)")
    axi.set_title("all four sign, Chai-1 by 0.045 Å", fontsize=7.4)
    axi.plot([], [], "o", ms=5, color=fs.BLACK, label="cluster bootstrap (primary)")
    axi.plot([], [], "o", ms=3, color=fs.GREY, label="receptor bootstrap")
    axi.legend(frameon=False, fontsize=5.8, loc="lower left")

    fs.panel_label(ax, "a", dx=-0.12); fs.panel_label(axi, "b", dx=-0.30)

    # THE APO-ONLY SCOPE IS CONTRADICTED BY THE SHIPPED COUNTS.
    #
    # This comment has been wrong twice and the second version was mine.
    #   v1 asserted "APO ARM ONLY" as fact.
    #   v2 said the question was unconfirmable, because I walked the 2x2 JSON
    #      with a traversal that RECURSED INTO `n_rows` -- it is a dict, and the
    #      keys inside it are cell names, which did not match the filter I was
    #      printing on. The container was visited and never reported. A check
    #      that runs and silently prints nothing looks exactly like a check that
    #      found nothing.
    #
    # What the files actually say:
    #   stage3_2x2_ligand_state_specificity.json carries `n_rows` on all four
    #   backbones: agonist cells 2,800, antagonist cells 2,300.
    #   The census fixes the design grid at EXACTLY 50 rows per
    #   (receptor, backbone, role, arm) -- 800 cells, unique size [50], no
    #   exceptions across 40,000 rows.
    #   So apo-only predicts 28 x 50 = 1,400 and 23 x 50 = 1,150; both arms
    #   predict 2,800 and 2,300. The shipped counts are the both-arms figure,
    #   exactly, on every backbone.
    #
    # The grid constant is what closes it. It does not matter that the census's
    # 35 and 29 receptors are supersets of the 2x2's 28 and 23 -- the constant
    # applies to whichever subset was drawn.
    note = (u"INTENDED SCOPE: APO ARM ONLY — AND THE SHIPPED ROW COUNTS ARE TWICE "
            u"THE APO-ONLY EXPECTATION on every backbone: 2,800 against 28×50 and "
            u"2,300 against 23×50, at a design grid the census fixes at exactly 50 "
            u"rows per receptor × backbone × role × arm. The filter appears not to "
            u"have been applied, and the interaction below is estimated on both "
            u"arms pooled. The design reason for wanting the apo scope stands: "
            u"with a cognate Gα in the complex the contrast cannot "
            u"be attributed to the ligand, because the partner supplies both mass "
            u"and a strong conformational preference of its own; the apo scope is "
            u"what makes this a statement about the ligand. n=23 receptors "
            u"carrying all four cells, resampled as 16 paralog clusters, 5,000 "
            u"iterations, seed 1234. The interaction is (agonist active − agonist "
            u"inactive) − (antagonist active − antagonist inactive), so a negative "
            u"value means agonists land nearer the active reference and "
            u"antagonists nearer the inactive one.")
    # THE CAVEAT IS READER-FACING AND STAYS ON THE PANEL. What changed on
    # 2026-09-10 is the colour and the last sentence.
    #
    # It was drawn in fs.VERM, and red on a figure reads as a developer warning
    # rather than as content. BB-1 was found shipping an actual build note in
    # the same colour on a MAIN-TEXT figure the same evening; this one is not a
    # build note, but a submission should not contain red annotation either way.
    # It is now dark ink, which is emphasis rather than alarm.
    #
    # And it ended "Add the per-receptor points when the rows arrive" -- an
    # instruction to us, not information for a reader. That sentence moved to
    # the console, where the person who could act on it will see it.
    warn = (u"SUMMARY PANEL. rows.tier3.v2.csv was not delivered with this "
            u"campaign, so the 23 per-receptor values behind each mean are not "
            u"available and no distribution is drawn. Four intervals are not "
            u"evidence about a population: this project has twice found a "
            u"four-value summary concealing a bimodal one — Block A's amplitude "
            u"fits and Block C's own pose result.")
    todo = ("BC-1 build note: add the per-receptor points when "
            "rows.tier3.v2.csv arrives (Block C DATA_REQUESTS ask 1).")
    fig.text(0.01, -0.085, "\n".join(textwrap.wrap(note, 132)), fontsize=5.4,
             color=fs.GREY, va="top", ha="left")
    fig.text(0.01, -0.205, "\n".join(textwrap.wrap(warn, 132)), fontsize=5.4,
             color=fs.BLACK, va="top", ha="left", weight="bold")

    p = fs.save(fig, "bc1_pocket_2x2")
    print(todo)
    print("BC-1 scope note: the apo-only filter was NOT applied.\n"
          "  stage3_2x2 n_rows = 2,800 agonist / 2,300 antagonist on all four "
          "backbones.\n  Census grid is exactly 50 rows per "
          "(receptor, backbone, role, arm), 800 cells, no exceptions.\n"
          "  apo-only predicts 1,400 and 1,150. Both arms predict 2,800 and "
          "2,300. Shipped = both arms.\n  rows.tier3.v2.csv is needed to "
          "RESTATE the result, not to establish this. Block C ask 1.")
    print("BC-1 ->", p[0])
    for bb in B.BACKBONES:
        k = cb[bb]["cluster_boot"]
        print("  %-9s %+.3f  [%+.3f, %+.3f]" % (bb, cb[bb]["point_estimate"],
                                                k["ci_lo"], k["ci_hi"]))


if __name__ == "__main__":
    main()
