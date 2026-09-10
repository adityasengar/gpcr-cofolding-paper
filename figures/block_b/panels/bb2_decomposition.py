#!/usr/bin/env python3
"""BB-2 -- the ladder decomposes into TWO contrasts that telescope exactly.

Claim: SC-B-1's decomposition, restated 2026-09-10.

WHY THIS PANEL WAS REBUILT. The version this replaces drew the campaign's three
telescoping terms as shipped: occupancy (apo->decoy), "alpha5-CT sequence"
(decoy->shuffled) and family (shuffled->cognate). The middle term is
mislabelled. `shuffled` is a subunit from a DIFFERENT Ga family, so
decoy->shuffled changes the tail, the scaffold, the length and the family at
once. It is arithmetically correct and interpretively confounded, and drawing it
under the name `delta_a5ct_sequence_decoy_to_shuffled` put a confound in the
figure that carries the paper's decomposition.

THE CLEAN CONTRAST WAS ALREADY IN THE DROP. decoy->cognate holds the family, the
length and the entire scaffold fixed and varies only the eleven C-terminal
residues -- and varies them by a PERMUTATION, so even amino-acid composition is
held constant. It is the only contrast in the campaign that isolates the alpha5
C-terminus, and it is LARGER than the confounded term it replaces:

    occupancy   apo   -> decoy    +0.400 [0.334, 0.464]
    alpha5-CT   decoy -> cognate  +0.333 [0.242, 0.432]
                                  ------
                                   0.733 = apo -> cognate, exactly

Family (shuffled->cognate, +0.082) sits INSIDE the second step and is drawn
inside it, not beside it, because that is where it lives.

EVERY NUMBER HERE IS RECOMPUTED from 04_ladder/ladder_per_receptor.csv on the
frame_36 population, including the intervals: a 1,000-resample cluster bootstrap
over the 24 paralog clusters that survive frame_36. The shipped file is used only
to check the recomputation, never as the source. That matters because the shipped
decomposition's own middle term is the thing this panel exists to replace.
"""
import os
import sys
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

import figstyle as fs                                          # noqa: E402
import badata as bd                                            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
LADDER = os.path.join(ROOT, "data", "block_b", "04_ladder",
                      "ladder_per_receptor.csv")
SHIPPED = os.path.join(ROOT, "data", "block_b", "05_decomposition",
                       "ladder_decomposition.csv")
SEED = 20260909
NBOOT = 1000


def load():
    l = pd.read_csv(LADDER)
    f = l[~l.receptor.isin(bd.NPXXY_UNDEFINED)]
    return f.groupby(["receptor", "cluster"])[
        ["apo_rate", "decoy_rate", "shuffled_rate", "cognate_rate"]].mean().reset_index()


def boot(per, a, b):
    rng = np.random.default_rng(SEED)
    cl = per.cluster.unique()
    idx = {c: per.index[per.cluster == c] for c in cl}
    out = []
    for _ in range(NBOOT):
        rows = per.loc[np.concatenate([idx[c] for c in
                                       rng.choice(cl, len(cl), replace=True)])]
        out.append((rows[b] - rows[a]).mean())
    return float((per[b] - per[a]).mean()), np.percentile(out, [2.5, 97.5])


def main():
    fs.use_house_style()
    per = load()
    ship = pd.read_csv(SHIPPED)
    ship = ship[(ship.frame == "reproduction_36") & (ship.backbone == "panel")
                & (ship.scale == "probability")]

    occ, occ_ci = boot(per, "apo_rate", "decoy_rate")
    a5, a5_ci = boot(per, "decoy_rate", "cognate_rate")
    fam, fam_ci = boot(per, "shuffled_rate", "cognate_rate")
    conf, conf_ci = boot(per, "decoy_rate", "shuffled_rate")
    total = float((per.cognate_rate - per.apo_rate).mean())

    # the recomputation must agree with the shipped file on the terms it DOES
    # ship, or the panel refuses to draw
    for key, got in (("delta_occupancy_apo_to_decoy", occ),
                     ("delta_a5ct_sequence_decoy_to_shuffled", conf),
                     ("delta_correct_family_shuffled_to_cognate", fam)):
        want = float(ship[ship.contrast == key].term_estimate.iloc[0])
        if abs(got - want) > 1e-3:
            raise SystemExit("recomputation disagrees with the shipped file on "
                             "%s: %.4f vs %.4f" % (key, got, want))

    fig = plt.figure(figsize=(fs.W2, 104 * fs.MM))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0], wspace=0.30,
                          left=0.085, right=0.985, top=0.86, bottom=0.30)

    # ---- a: the ladder, with the two steps bracketed --------------------
    ax = fig.add_subplot(gs[0, 0])
    arms = ["apo_rate", "decoy_rate", "shuffled_rate", "cognate_rate"]
    labels = ["apo\n(no partner)", "decoy\n(correct subunit,\ntail permuted)",
              "shuffled\n(different Gα\nfamily)", "cognate\n(correct subunit)"]
    y = [per[a].mean() for a in arms]
    x = np.arange(4)
    ax.plot(x[[0, 1, 3]], [y[0], y[1], y[3]], "-o", ms=6, lw=2.2,
            color=fs.BLACK, zorder=3, label="the two clean steps")
    ax.plot(x[[1, 2, 3]], [y[1], y[2], y[3]], "--o", ms=4.5, lw=1.2,
            color=fs.GREY, zorder=2, label="via shuffled (confounded)")
    for i, v in enumerate(y):
        ax.annotate("%.3f" % v, (x[i], v), textcoords="offset points",
                    xytext=(0, 10 if i != 2 else -16), ha="center", fontsize=6.4)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=6.0)
    ax.set_ylim(0.03, 1.04)
    ax.set_ylabel("two-instrument active-call fraction", fontsize=7.2)
    ax.legend(fontsize=5.9, frameon=False, loc="center right", bbox_to_anchor=(1.0, 0.34))

    # brackets for the two steps
    for (i0, i1), est, ci, name, col in (
            ((0, 1), occ, occ_ci, "occupancy", fs.BLUE),
            ((1, 3), a5, a5_ci, "α5-CT sequence", fs.VERM)):
        yb = 0.34 if i0 == 0 else 0.24
        ax.annotate("", xy=(x[i0], yb), xytext=(x[i1], yb),
                    arrowprops=dict(arrowstyle="<->", color=col, lw=1.3))
        ax.text(x[i0] + 0.04, yb + 0.018,
                "%s  %+.3f [%.3f, %.3f]" % (name, est, ci[0], ci[1]),
                ha="left", fontsize=6.2, color=col, weight="bold")
    ax.text(1.5, 0.085, "%.3f + %.3f = %.3f = apo $\\rightarrow$ cognate, exactly"
            % (occ, a5, occ + a5), ha="center", fontsize=6.2, style="italic")
    ax.set_title("the ladder, and the two steps that telescope",
                 fontsize=7.4, pad=6)
    fs.panel_label(ax, "a", dx=-0.11, dy=1.09)

    # ---- b: what each contrast actually varies --------------------------
    ax = fig.add_subplot(gs[0, 1])
    rows = [("occupancy\napo $\\rightarrow$ decoy", occ, occ_ci, fs.BLUE, "clean", ""),
            ("α5-CT sequence\ndecoy $\\rightarrow$ cognate", a5, a5_ci, fs.VERM, "clean",
             "only the 11 C-terminal residues,\npermuted — composition held"),
            ("family\nshuffled $\\rightarrow$ cognate", fam, fam_ci, fs.GREEN, "clean",
             "sits inside the step above"),
            ("as shipped\ndecoy $\\rightarrow$ shuffled", conf, conf_ci, fs.GREY, "CONFOUNDED",
             "changes tail AND scaffold AND\nlength AND family at once")]
    for i, (name, est, ci, col, kind, why) in enumerate(rows):
        yy = len(rows) - 1 - i
        ax.errorbar([est], [yy], xerr=[[est - ci[0]], [ci[1] - est]], fmt="o",
                    ms=5, color=col, lw=1.4, capsize=2.4)
        ax.text(est, yy + 0.26, "%+.3f" % est, ha="center", fontsize=6.3,
                color=col)
        if kind == "CONFOUNDED":
            ax.text(est, yy - 0.34, "NOT an α5-CT contrast", fontsize=5.8,
                    color=fs.VERM, weight="bold", ha="center", va="top")
    ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=6.2)
    ax.set_xlim(-0.02, 0.52)
    ax.set_ylim(-0.75, len(rows) - 0.35)
    ax.set_xlabel("change in active-call fraction", fontsize=7.0)
    ax.set_title("what each contrast actually varies", fontsize=7.4, pad=6)
    fs.panel_label(ax, "b", dx=-0.34, dy=1.09)

    note = (
        "All values RECOMPUTED from 04_ladder/ladder_per_receptor.csv on frame_36 "
        "(36 receptors; EDNRA, EDNRB, GRPR and HRH3 have Leu at 7.53 so NPxxY is "
        "undefined), averaged over backbones within receptor. Intervals are a "
        "1,000-resample cluster bootstrap over the %d paralog clusters that survive "
        "frame_36 -- NOT the 26 that every shipped frame_36 interval is labelled "
        "with. The three shipped terms are reproduced first and the panel refuses to "
        "draw if any disagrees beyond 1e-3. "
        "The campaign ships decoy -> shuffled under the name "
        "`delta_a5ct_sequence_decoy_to_shuffled`; it is drawn here in grey and named "
        "confounded, because the shuffled arm is a different Gα family and that "
        "step changes four things at once. The clean α5-CT contrast is decoy -> "
        "cognate, and it is larger than the term it replaces."
        % per.cluster.nunique())
    fig.text(0.012, 0.012, "\n".join(textwrap.wrap(note, 150)), fontsize=5.3,
             va="bottom", color="0.25")

    fs.save(fig, "bb2_decomposition")
    print("BB-2 rebuilt. occupancy %+.4f %s | alpha5-CT %+.4f %s | "
          "family %+.4f | confounded %+.4f | total %.4f"
          % (occ, np.round(occ_ci, 3), a5, np.round(a5_ci, 3), fam, conf, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
