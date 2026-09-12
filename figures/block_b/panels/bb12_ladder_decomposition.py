# -*- coding: utf-8 -*-
"""BB-12 -- the four-arm ladder AND its decomposition, in one figure.

WHY THIS EXISTS. BB-1 and BB-2 shipped as main-text Figures 3 and 4, and they
drew the same ladder twice: BB-2's left panel is titled "the ladder, and the two
steps that telescope" and redraws the four rungs BB-1 had already drawn, forty-
five lines earlier in the prose. Merging them was Aditya's call on 2026-09-11.

THE MERGE HAD TO REMOVE THE DUPLICATION, NOT CARRY IT INSIDE ONE FLOAT. A 2x2
built by dropping BB-1's two panels beside BB-2's two would put two ladders in
one figure, which is the defect it was supposed to fix. So the ladder is drawn
ONCE, at full width, doing both jobs: the per-backbone traces and panel interval
that were BB-1's argument, and the two telescoping step brackets that were
BB-2's. The logit companion and the contrast audit sit below it.

    a   the ladder: four arms, four backbones, panel with cluster-boot CIs,
        and the two clean steps bracketed on the same axes
    b   the same fractions on the logit scale, because probability saturates
    c   what each contrast actually varies, including the shipped one

WHAT MUST NOT BE LOST IN THE MERGE, and is not. BB-2's caption carries the
paper's most consequential claim-side correction: the campaign ships
decoy->shuffled under the name `delta_a5ct_sequence_decoy_to_shuffled`, and it
is NOT an alpha5-CT contrast, because `shuffled` is a subunit from a DIFFERENT
Ga family -- that step changes the tail, the scaffold, the length and the family
at once. The clean contrast is decoy->cognate, which holds family, length and
scaffold fixed and varies only the eleven C-terminal residues, by a permutation,
so even composition is constant. It is LARGER than the term it replaces:

    occupancy   apo   -> decoy    +0.400 [0.334, 0.464]
    alpha5-CT   decoy -> cognate  +0.333 [0.242, 0.432]
                                  ------
                                   0.733 = apo -> cognate, exactly

TWO SOURCES, AND THEY ARE CHECKED AGAINST EACH OTHER. The per-backbone rates
come from rows_tidy.csv with the predicate recomputed per row (BB-1's path); the
decomposition terms come from 04_ladder/ladder_per_receptor.csv (BB-2's path).
Both are frame_36. They describe the same four rungs by two different routes, so
this file asserts that they AGREE before drawing a single ladder that claims to
be both. If they ever diverge, one ladder cannot honestly carry both arguments
and the script refuses to draw rather than pick a winner.

Both original guards are kept: BB-1's tolerance check against
ladder_four_scorings.csv, and BB-2's 1e-3 check against ladder_decomposition.csv.

SUPERSEDES bb1_ladder.py and bb2_decomposition.py as a MAIN-TEXT figure. Those
two scripts are untouched and still render; they remain the SI versions.
"""
import _shead                                                    # noqa: F401
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

import figstyle as fs
import badata as B

fs.use_house_style()

FRAME = 36
ARMS = B.ARM_ORDER
BB = fs.BACKBONE_ORDER
SEED = 20260909
NBOOT = 1000

#: BB-1's tolerance, unchanged and for the same reason: one row of fifty in one
#: receptor moves the 36-receptor panel mean by 5.6e-4. The shipped aggregates
#: used the untruncated NPxxY threshold 9.082 while every row carries 9.08.
TOL = 1.1e-3

#: The two routes to the same four rungs must agree this closely. It is looser
#: than TOL by design: the two paths average over backbones in a different
#: order, which is exact in infinite precision and not in float.
ROUTE_TOL = 5e-3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
LADDER = os.path.join(ROOT, "data", "block_b", "04_ladder",
                      "ladder_per_receptor.csv")
SHIPPED_DEC = os.path.join(ROOT, "data", "block_b", "05_decomposition",
                           "ladder_decomposition.csv")


def cluster_boot(df, n_boot=NBOOT, seed=SEED):
    """Resample paralog CLUSTERS, not receptors -- paralogues are not
    independent evidence. Lifted unchanged from BB-1."""
    rng = np.random.default_rng(seed)
    per_recep = df.groupby(["cluster_id", "receptor_slug"]).active.mean()
    clusters = per_recep.index.get_level_values(0).unique().to_numpy()
    draws = np.empty(n_boot)
    for i in range(n_boot):
        take = rng.choice(clusters, size=len(clusters), replace=True)
        draws[i] = np.mean([per_recep.loc[c].mean() for c in take])
    return np.percentile(draws, [2.5, 97.5])


def load_per_receptor():
    """BB-2's path: the per-receptor ladder, frame_36."""
    l = pd.read_csv(LADDER)
    f = l[~l.receptor.isin(B.NPXXY_UNDEFINED)]
    return f.groupby(["receptor", "cluster"])[
        ["apo_rate", "decoy_rate", "shuffled_rate",
         "cognate_rate"]].mean().reset_index()


def boot_contrast(per, a, b):
    """Cluster bootstrap of a paired contrast. Lifted unchanged from BB-2."""
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
    # ---- route 1: rows, predicate recomputed per row (BB-1) --------------
    raw = B.frame(B.rows(), FRAME)
    raw["active"] = B.predicate(raw)
    ship = B.pick_frame(B.table("04_ladder/ladder_four_scorings.csv"), FRAME)

    rates, cis, disagree = {}, {}, []
    for bb in BB + ["panel"]:
        sub = raw if bb == "panel" else raw[raw.backbone == bb]
        rates[bb] = [sub[sub.arm == a].groupby("receptor_slug").active.mean().mean()
                     for a in ARMS]
        if bb == "panel":
            cis[bb] = [cluster_boot(sub[sub.arm == a]) for a in ARMS]
        s = ship[ship.backbone == ("panel" if bb == "panel" else bb)]
        for a, r in zip(ARMS, rates[bb]):
            row = s[s.arm == a]
            if len(row) and abs(float(row.binary_predicate.iloc[0]) - r) > TOL:
                disagree.append((bb, a, r, float(row.binary_predicate.iloc[0])))
    if disagree:
        raise SystemExit("recomputation disagrees with ladder_four_scorings.csv "
                         "beyond the one-row tolerance: %s" % disagree)

    # ---- route 2: the per-receptor ladder (BB-2) -------------------------
    per = load_per_receptor()
    shipd = pd.read_csv(SHIPPED_DEC)
    shipd = shipd[(shipd.frame == "reproduction_36") & (shipd.backbone == "panel")
                  & (shipd.scale == "probability")]

    occ, occ_ci = boot_contrast(per, "apo_rate", "decoy_rate")
    a5, a5_ci = boot_contrast(per, "decoy_rate", "cognate_rate")
    fam, fam_ci = boot_contrast(per, "shuffled_rate", "cognate_rate")
    conf, conf_ci = boot_contrast(per, "decoy_rate", "shuffled_rate")

    for key, got in (("delta_occupancy_apo_to_decoy", occ),
                     ("delta_a5ct_sequence_decoy_to_shuffled", conf),
                     ("delta_correct_family_shuffled_to_cognate", fam)):
        want = float(shipd[shipd.contrast == key].term_estimate.iloc[0])
        if abs(got - want) > 1e-3:
            raise SystemExit("recomputation disagrees with the shipped "
                             "decomposition on %s: %.4f vs %.4f"
                             % (key, got, want))

    # ---- THE MERGE CHECK -------------------------------------------------
    # One ladder is about to carry both arguments. It may only do that if the
    # two routes describe the same rungs.
    route2 = [per[c].mean() for c in ("apo_rate", "decoy_rate",
                                      "shuffled_rate", "cognate_rate")]
    gap = [abs(p - q) for p, q in zip(rates["panel"], route2)]
    if max(gap) > ROUTE_TOL:
        raise SystemExit(
            "the two routes to the ladder disagree (max %.4f > %.4f): rows give "
            "%s, ladder_per_receptor.csv gives %s. One figure cannot honestly "
            "carry both arguments while they differ -- do not merge BB-1 and "
            "BB-2 until this is understood."
            % (max(gap), ROUTE_TOL,
               np.round(rates["panel"], 4), np.round(route2, 4)))

    # ---- layout ----------------------------------------------------------
    # The ladder is drawn ONCE, wide, on top. Dropping BB-1's pair beside
    # BB-2's pair would put two ladders in one figure, which is the duplication
    # this merge exists to remove.
    fig = plt.figure(figsize=(fs.W2, 132 * fs.MM))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.22, 1.0],
                          width_ratios=[1.0, 1.32],
                          left=0.075, right=0.985, top=0.945, bottom=0.255,
                          hspace=0.58, wspace=0.30)

    y = rates["panel"]
    x = np.arange(len(ARMS))

    # ---- a: the ladder, per backbone, with the two steps bracketed -------
    ax = fig.add_subplot(gs[0, :])
    for bb in BB:
        ax.plot(x, rates[bb], marker="o", ms=3.0, lw=1.0, alpha=0.85,
                color=fs.BACKBONE_COLOURS[bb], label=fs.BACKBONE_LABELS[bb],
                zorder=3)
    lo = [y[i] - cis["panel"][i][0] for i in range(len(ARMS))]
    hi = [cis["panel"][i][1] - y[i] for i in range(len(ARMS))]
    ax.errorbar(x, y, yerr=[lo, hi], marker="s", ms=5.5, lw=2.2, capsize=3.0,
                color=fs.BLACK, label="panel", zorder=5)
    # The shuffled rung is real data and stays on the ladder. What it is NOT
    # is a step in the decomposition, and that is said here rather than drawn
    # as a phantom alternative path.
    # lit, 2026-09-11: this literature has NO idiom for a condition that is
    # plotted but deliberately outside the analysis path -- five near-matches,
    # none of them does it. What the corpus DOES have is the colour rule in
    # lit/RENDER_CONVENTIONS.md: grey means "not the subject". Panel c already
    # greys the shipped term, so extending the same semantic here beats
    # inventing a cue -- the reader meets ONE rule in both panels. The italic
    # note this replaces was not sufficient: lit read the panel cold and still
    # saw the bracket pass under shuffled.
    ax.plot([x[2]], [y[2]], marker="s", ms=5.5, color=fs.GREY, zorder=5.5,
            markeredgecolor="white", markeredgewidth=0.6)
    for i, r in enumerate(y):
        above = r < 0.75
        ax.annotate("%.3f" % r,
                    (x[i], cis["panel"][i][1] if above else cis["panel"][i][1]),
                    textcoords="offset points",
                    xytext=(0, 8) if above else (0, 9),
                    ha="center",
                    fontsize=6.4, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white",
                              ec="none", alpha=0.85))

    for (i0, i1), est, ci, name, col in (
            ((0, 1), occ, occ_ci, "occupancy", fs.BLUE),
            ((1, 3), a5, a5_ci, u"α5-CT sequence", fs.VERM)):
        yb = 0.02 if i0 == 0 else -0.085
        ax.annotate("", xy=(x[i0], yb), xytext=(x[i1], yb),
                    arrowprops=dict(arrowstyle="<->", color=col, lw=1.3))
        ax.text(0.5 * (x[i0] + x[i1]), yb + 0.022,
                "%s  %+.3f [%.3f, %.3f]" % (name, est, ci[0], ci[1]),
                ha="center", fontsize=6.2, color=col, weight="bold",
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none",
                          alpha=0.88))
    ax.text(2.25, 0.34,
            "%.3f + %.3f = %.3f = apo $\\rightarrow$ cognate, exactly"
            % (occ, a5, occ + a5), ha="center", fontsize=6.2, style="italic")

    ax.set_xticks(x)
    ax.set_xticklabels(["apo\n(no partner)",
                        "decoy\n(correct subunit, tail permuted)",
                        u"shuffled\n(different Gα family)\nnot in either step",
                        "cognate\n(correct subunit)"], fontsize=6.2)
    ax.get_xticklabels()[2].set_color(fs.GREY)
    ax.set_ylim(-0.17, 1.08)
    # the band below zero holds the step brackets, not data, so it carries no
    # ticks -- a tick at -0.1 would read as a negative active-call fraction
    ax.set_yticks(np.arange(0, 1.01, 0.2))
    ax.spines["left"].set_bounds(0, 1.0)
    ax.set_ylabel("two-instrument active-call fraction", fontsize=7.2)
    ax.set_title("the four-arm ladder, and the two steps that telescope",
                 fontsize=7.4, pad=6)
    ax.legend(frameon=False, fontsize=6.0, loc="upper left", ncol=3)
    fs.panel_label(ax, "a", dx=-0.055, dy=1.07)

    # ---- b: the logit companion -----------------------------------------
    axl = fig.add_subplot(gs[1, 0])
    eps = 1.0 / 8000.0
    for bb in BB + ["panel"]:
        p = np.clip(np.asarray(rates[bb]), eps, 1 - eps)
        axl.plot(x, np.log(p / (1 - p)), marker="o", ms=2.6,
                 lw=2.0 if bb == "panel" else 0.9,
                 color=fs.BLACK if bb == "panel" else fs.BACKBONE_COLOURS[bb],
                 alpha=1.0 if bb == "panel" else 0.8)
    axl.axhline(0, color=fs.GREY, lw=0.6, zorder=1)
    axl.set_xticks(x)
    axl.set_xticklabels([B.ARM_LABELS[a] for a in ARMS], fontsize=6.2)
    axl.set_ylabel("logit of the same fraction", fontsize=7.2)
    axl.set_title(u"the same fractions, logit scale", fontsize=7.0, pad=6)
    fs.panel_label(axl, "b", dx=-0.16, dy=1.09)

    # ---- c: what each contrast actually varies --------------------------
    axc = fig.add_subplot(gs[1, 1])
    rows = [(u"occupancy\napo $\\rightarrow$ decoy", occ, occ_ci, fs.BLUE,
             "clean", ""),
            (u"α5-CT sequence\ndecoy $\\rightarrow$ cognate", a5, a5_ci, fs.VERM,
             "clean", ""),
            (u"family\nshuffled $\\rightarrow$ cognate", fam, fam_ci, fs.GREEN,
             "clean", ""),
            (u"as shipped\ndecoy $\\rightarrow$ shuffled", conf, conf_ci,
             fs.GREY, "CONFOUNDED", "")]
    for i, (name, est, ci, col, kind, _why) in enumerate(rows):
        yy = len(rows) - 1 - i
        axc.errorbar([est], [yy], xerr=[[est - ci[0]], [ci[1] - est]], fmt="o",
                     ms=5, color=col, lw=1.4, capsize=2.4)
        axc.text(est, yy + 0.26, "%+.3f" % est, ha="center", fontsize=6.3,
                 color=col)
        if kind == "CONFOUNDED":
            axc.text(est, yy - 0.34, u"NOT an α5-CT contrast", fontsize=5.8,
                     color=fs.VERM, weight="bold", ha="center", va="top")
    axc.axvline(0, color="black", lw=0.8)
    axc.set_yticks(range(len(rows)))
    axc.set_yticklabels([r[0] for r in rows][::-1], fontsize=6.2)
    axc.set_xlim(-0.02, 0.52)
    axc.set_ylim(-0.75, len(rows) - 0.35)
    axc.set_xlabel("change in active-call fraction", fontsize=7.0)
    axc.set_title("what each contrast actually varies", fontsize=7.4, pad=6)
    fs.panel_label(axc, "c", dx=-0.30, dy=1.09)

    n_rec = raw.receptor_slug.nunique()
    n_cl = B.n_clusters(raw)
    # The face duplicated the caption almost sentence for sentence, and
    # duplicated material is where two texts drift apart. lit's rule: the
    # caption carries filter and n; the face carries only what a reader needs
    # WHILE LOOKING AT THE PANEL. The confound argument stays in the caption at
    # full strength -- that was Aditya's condition on the merge.
    note = (
        u"Class A, frame_%d: n=%d receptors, %d paralog clusters -- NOT the 26 "
        u"that every shipped frame_36 interval is labelled with (D-B-8). "
        u"Intervals are 1,000-resample cluster bootstraps, seed %d; clusters "
        u"are the resampling unit, not receptors. Excluded from the frame: "
        u"EDNRA, EDNRB, GRPR and HRH3, whose NPxxY axis is undefined because "
        u"position 7.53 is Leu not Tyr (C-B-5). Predicate: "
        u"d(Y5.58 OH, Y7.53 OH) < 9.08 Å AND d(2×46 Cα, "
        u"6×37 Cα) > 14.932 Å, recomputed from every row rather "
        u"than read from a shipped call column. GREY IS NOT THE SUBJECT: the "
        u"shuffled arm is real data and is a step in neither contrast. Why the "
        u"campaign's shipped middle term is confounded is in the caption."
        % (FRAME, n_rec, n_cl, SEED))
    fig.text(0.012, 0.010, "\n".join(textwrap.wrap(note, 168)),
             fontsize=5.3, va="bottom", ha="left", color="0.25")

    paths = fs.save(fig, "bb12_ladder_decomposition")
    print("BB-12 ->", paths[0])
    print("  frame_%d, n=%d receptors, %d clusters" % (FRAME, n_rec, n_cl))
    for a, r, c in zip(ARMS, y, cis["panel"]):
        print("   %-9s %.3f  [%.3f, %.3f]" % (a, r, c[0], c[1]))
    print("  occupancy  %+.4f %s" % (occ, np.round(occ_ci, 3)))
    print("  alpha5-CT  %+.4f %s" % (a5, np.round(a5_ci, 3)))
    print("  family     %+.4f %s   (inside the alpha5-CT step)"
          % (fam, np.round(fam_ci, 3)))
    print("  CONFOUNDED %+.4f %s   (shipped middle term, not drawn as a step)"
          % (conf, np.round(conf_ci, 3)))
    print("  telescoping: %.4f + %.4f = %.4f" % (occ, a5, occ + a5))
    print("  the two routes agree on all four rungs, max gap %.5f"
          % max(gap))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
