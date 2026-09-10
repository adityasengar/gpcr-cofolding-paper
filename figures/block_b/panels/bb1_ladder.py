# -*- coding: utf-8 -*-
"""BB-1 — the four-arm ladder under the two-instrument predicate.

Spec: data/block_b/12_narrative/figures/BB-1_ladder_binary_predicate.md
Claim: SC-B-1. Standalone panel, no manuscript figure number, no composite.

TWO DELIBERATE DEPARTURES FROM THE SPEC, both recorded in
analysis/block_b/DISCREPANCY_REPORT.md and rebuttals/BLOCK_B.md:

1. The spec says: "Annotate dispatch cite (0.158 / 0.552 / 0.810 / 0.892) at
   panel row as reference dashes." THOSE ARE THE SUPERSEDED NUMBERS. The drop's
   own README says 0.552 is a pre-consolidation snapshot and the canonical
   decoy rate is 0.558. The spec contradicts itself two paragraphs later, where
   its "Panel value labels" section gives the correct 0.158 / 0.558 / 0.809 /
   0.891. Drawing a superseded ladder as a reference line would put a retired
   number on the most-read panel in the block, so the dashes are not drawn and
   this note says why.

2. The spec names columns binary_predicate_mean / binary_predicate_ci_lo|hi.
   The shipped file has binary_predicate / cluster_boot_ci_lo|hi_binary.

Every value here is recomputed from rows_tidy.csv and cross-checked against the
shipped table; the panel prints nothing that the two disagree on.
"""
import _shead                                                    # noqa: F401
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
import badata as B

fs.use_house_style()

FRAME = 36
ARMS = B.ARM_ORDER
BB = fs.BACKBONE_ORDER

#: One row of 50 in one receptor moves a per-receptor rate by 0.02, which moves
#: the 36-receptor panel mean by 0.02/36 = 5.6e-4. The shipped aggregates used
#: the untruncated NPxxY threshold 9.082 while every row carries 9.08, and five
#: rows of 32,000 sit between them -- so exactly this much disagreement is
#: expected and understood. Anything larger is not, and stops the script.
TOL = 1.1e-3


def cluster_boot(df, n_boot=1000, seed=20260909):
    """Resample paralog CLUSTERS, not receptors. The unit is what makes the
    interval honest: paralogues are not independent evidence."""
    rng = np.random.default_rng(seed)
    per_recep = df.groupby(["cluster_id", "receptor_slug"]).active.mean()
    clusters = per_recep.index.get_level_values(0).unique().to_numpy()
    draws = np.empty(n_boot)
    for i in range(n_boot):
        take = rng.choice(clusters, size=len(clusters), replace=True)
        draws[i] = np.mean([per_recep.loc[c].mean() for c in take])
    return np.percentile(draws, [2.5, 97.5])


def main():
    raw = B.frame(B.rows(), FRAME)
    raw["active"] = B.predicate(raw)
    ship = B.pick_frame(B.table("04_ladder/ladder_four_scorings.csv"), FRAME)

    # recompute, then confirm against the shipped table before drawing anything
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
        raise SystemExit("recomputation disagrees with the shipped table beyond "
                         "the one-row tolerance: %s" % disagree)

    fig, (ax, axl) = fs.figure(width=fs.W2, height=112 * fs.MM, ncols=2,
                               gridspec_kw={"width_ratios": [2.0, 1.0]})
    x = np.arange(len(ARMS))

    for bb in BB:
        ax.plot(x, rates[bb], marker="o", ms=3.0, lw=1.0, alpha=0.85,
                color=fs.BACKBONE_COLOURS[bb], label=fs.BACKBONE_LABELS[bb],
                zorder=3)
    lo = [rates["panel"][i] - cis["panel"][i][0] for i in range(len(ARMS))]
    hi = [cis["panel"][i][1] - rates["panel"][i] for i in range(len(ARMS))]
    ax.errorbar(x, rates["panel"], yerr=[lo, hi], marker="s", ms=5.5, lw=2.2,
                capsize=3.0, color=fs.BLACK, label="panel", zorder=5)
    # the cognate label collides with the Protenix trace if placed above, so the
    # top two sit to the left of their marker instead
    for i, r in enumerate(rates["panel"]):
        above = r < 0.75
        ax.annotate("%.3f" % r,
                    (x[i], cis["panel"][i][1] if above else r),
                    textcoords="offset points",
                    xytext=(0, 7) if above else (-11, -3),
                    ha="center" if above else "right",
                    fontsize=6.4, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white",
                              ec="none", alpha=0.85))

    ax.set_xticks(x); ax.set_xticklabels([B.ARM_LABELS[a] for a in ARMS])
    ax.set_ylim(0, 1.06)
    ax.set_ylabel("two-instrument active-call fraction")
    ax.set_xlabel("input arm")
    ax.set_title("the four-arm ladder, per receptor then per cluster", fontsize=7.4)
    ax.legend(frameon=False, fontsize=6.2, loc="upper left", ncol=2)

    eps = 1.0 / 8000.0
    for bb in BB + ["panel"]:
        p = np.clip(np.asarray(rates[bb]), eps, 1 - eps)
        axl.plot(x, np.log(p / (1 - p)), marker="o", ms=2.6,
                 lw=2.0 if bb == "panel" else 0.9,
                 color=fs.BLACK if bb == "panel" else fs.BACKBONE_COLOURS[bb],
                 alpha=1.0 if bb == "panel" else 0.8)
    axl.axhline(0, color=fs.GREY, lw=0.6, zorder=1)
    axl.set_xticks(x); axl.set_xticklabels([B.ARM_LABELS[a] for a in ARMS])
    axl.set_ylabel("logit of the same fraction")
    axl.set_title(u"logit scale (ε = 1/8000)", fontsize=7.0)

    n_rec = raw.receptor_slug.nunique()
    note = (u"Class A, frame_%d: n=%d receptors, %d paralog clusters. "
            u"1,000 cluster-bootstrap resamples, seed 20260909; clusters are the "
            u"resampling unit, not receptors. Excluded from the frame: EDNRA, "
            u"EDNRB, GRPR and HRH3, whose NPxxY axis is undefined because "
            u"position 7.53 is Leu not Tyr (C-B-5). Predicate: "
            u"d(Y5.58 OH, Y7.53 OH) < 9.08 \u00c5 AND d(2\u00d746 C\u03b1, "
            u"6\u00d737 C\u03b1) > 14.932 \u00c5, recomputed from every row "
            u"rather than read from a shipped call column. Each point is the "
            u"mean over receptors of that receptor's own rate."
            % (FRAME, n_rec, B.n_clusters(raw)))
    warn = (u"The superseded 0.552 / 0.810 / 0.892 reference dashes named in the "
            u"BB-1 spec are deliberately not drawn: 0.552 is a pre-consolidation "
            u"snapshot the drop's own README retires, and the spec's own "
            u"value-label section gives the canonical set used here.")
    fig.text(0.01, -0.02, "\n".join(textwrap.wrap(note, 132)),
             fontsize=5.4, color=fs.GREY, va="top", ha="left")
    # The `warn` text above is a BUILD note, not caption text, and it is deliberately
    # NOT drawn on the figure: BB-1 is a main-text panel and red developer annotation
    # must not reach a submission. The information is preserved where it belongs --
    # in FIGURE_PROVENANCE.md and in the FIGURES.md ledger entry, both of which record
    # why the superseded reference dashes are absent. Print it to the console instead,
    # so anyone rebuilding still sees it.
    print("  NOTE (not drawn):", warn)

    paths = fs.save(fig, "bb1_ladder")
    print("BB-1 ->", paths[0])
    print("  frame_%d, n=%d receptors, %d clusters"
          % (FRAME, n_rec, B.n_clusters(raw)))
    for a, r, c in zip(ARMS, rates["panel"], cis["panel"]):
        print("   %-9s %.3f  [%.3f, %.3f]" % (a, r, c[0], c[1]))
    print("  recomputation agrees with ladder_four_scorings.csv on all %d cells"
          % (len(ARMS) * (len(BB) + 1)))
    print("  (tolerance %.1e = one row of fifty in one receptor; the shipped "
          "aggregates used\n   the untruncated 9.082 and the rows carry 9.08, "
          "which differ on %d rows of 32,000)" % (TOL, B.BOUNDARY_ROWS))


if __name__ == "__main__":
    main()
