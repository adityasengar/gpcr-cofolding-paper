"""
BA-5 - does confidence track correctness?

  a  Pearson r between pLDDT and RMSD-to-active, ALL THREE aggregations x four
     backbones, cluster-bootstrap CIs, zero marked, the primary aggregation
     banded. `plddt_at_anchors` was designated primary POST HOC, after all
     three had been computed (W-2); the caption says so, because the
     disclosure is what protects the result, not the label.
  b  what the choice of aggregation does: the global mean against the anchor
     mean, per backbone. OpenFold-3 strengthens (-0.258 -> -0.626); Protenix
     collapses (+0.327 -> +0.068).
  c  the scatter itself - confidence on one axis, the thing it is supposed to
     predict on the other, no smoothing.
  d  the per-receptor sign census: how many of the 32 receptors have a
     negative within-receptor r, per backbone and aggregation.

BA-5e is the `confidently_wrong` render, built by render_struct.py; see
FIGURE_PROVENANCE.md.

FILTER. Panels a, b, d quote 06_confidence/plddt_correlations.csv and
plddt_per_receptor.csv as shipped. Their population is Class A rows carrying
an RMSD to an active reference: n = 1,595-1,600 per backbone over 32 distinct
receptors, verified by reproducing all twelve Pearson r values to 1e-4. Note
that the shipped correlations do NOT apply E1/E2; panel c does apply them,
which removes 4 further rows and moves r by at most 0.0001.

`plddt_correlations.csv` records `n_receptors = 40` on every row, but the
population contains 32 distinct receptors and plddt_per_receptor.csv itself
carries 32 per (backbone, aggregation). The panel quotes 32.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

import numpy as np                                          # noqa: E402
import badata as B                                          # noqa: E402
import figstyle as fs                                       # noqa: E402
import figpanels as fp                                      # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402

AGG_ORDER = ["plddt_mean", "plddt_at_anchors", "min_plddt_at_anchor"]
AGG_LABEL = {"plddt_mean": "global mean",
             "plddt_at_anchors": "anchor mean  (primary, post hoc)",
             "min_plddt_at_anchor": "anchor min"}


def main():
    fs.use_house_style()
    pc = B.load("06_confidence/plddt_correlations.csv")
    pr = B.load("06_confidence/plddt_per_receptor.csv")
    raw = B.rows()
    pop, popfilt, popn = B.confidence_population(raw)
    scat, corefilt, _ = B.core(pop)

    fig = plt.figure(figsize=(fs.W2, 152 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1.0])
    axa = fig.add_subplot(gs[0, 0])
    axb = fig.add_subplot(gs[0, 1])
    subc = gs[1, 0].subgridspec(1, 4, wspace=0.08)
    axc = []
    for i in range(4):
        axc.append(fig.add_subplot(subc[0, i], sharex=axc[0] if axc else None,
                                   sharey=axc[0] if axc else None))
    axd = fig.add_subplot(gs[1, 1])

    # ---- a: all three aggregations ----------------------------------------
    labs, est, lo, hi, cols, ns, gaps, bands = [], [], [], [], [], [], set(), []
    k = 0
    for bi, bb in enumerate(fs.BACKBONE_ORDER):
        if bi:
            gaps.add(k)
        for agg in AGG_ORDER:
            r = pc[(pc.backbone == bb) & (pc.aggregation == agg)].iloc[0]
            labs.append("%s — %s" % (fs.BACKBONE_LABELS[bb], AGG_LABEL[agg]))
            est.append(r.pearson_r)
            lo.append(r.cluster_ci_lo); hi.append(r.cluster_ci_hi)
            cols.append(fs.BACKBONE_COLOURS[bb])
            ns.append(int(r.n_rows))
            if r.primary_or_secondary == "primary":
                bands.append(k)
            k += 1
    fres = fp.forest(axa, labs, est, lo, hi, colours=cols, null=0.0,
                     null_label="no relationship", ns=ns, group_gaps=gaps,
                     bands=bands, band_label="primary aggregation (post hoc)",
                     xlabel="Pearson r, pLDDT against RMSD to the active reference")
    axa.legend(handles=fres["handles"], loc="upper center",
               bbox_to_anchor=(0.5, -0.16), fontsize=4.5, ncol=2, borderpad=0.2)
    axa.set_title("confidence against correctness, cluster-bootstrap 95% CI "
                  "(32 receptors)", fontsize=6.5)
    fs.panel_label(axa, "a", dx=-0.52)

    # ---- b: what the aggregation choice does ------------------------------
    for bb in fs.BACKBONE_ORDER:
        y = [pc[(pc.backbone == bb) & (pc.aggregation == a)].pearson_r.iloc[0]
             for a in AGG_ORDER]
        axb.plot(range(3), y, marker="o", markersize=3.4,
                 color=fs.BACKBONE_COLOURS[bb], lw=1.0,
                 label=fs.BACKBONE_LABELS[bb])
        for xi, (a, yi) in enumerate(zip(AGG_ORDER, y)):
            prim = pc[(pc.backbone == bb) &
                      (pc.aggregation == a)].primary_or_secondary.iloc[0]
            signed = pc[(pc.backbone == bb) &
                        (pc.aggregation == a)].signed_at_cluster_boot.iloc[0]
            axb.plot([xi], [yi], marker="o", markersize=3.4,
                     color=fs.BACKBONE_COLOURS[bb],
                     markerfacecolor=fs.BACKBONE_COLOURS[bb] if signed
                     else "white", markeredgewidth=0.9, zorder=4)
    axb.axhline(0, color=fs.GREY, lw=0.8, zorder=0)
    axb.axvspan(0.6, 1.4, color=fs.YELLOW, alpha=0.30, linewidth=0, zorder=0)
    axb.set_xticks(range(3))
    axb.set_xticklabels(["global\nmean", "anchor mean\n(primary,\npost hoc)",
                         "anchor\nmin"])
    axb.set_ylabel("Pearson r")
    axb.set_xlim(-0.35, 2.35)
    axb.legend(loc="upper left", bbox_to_anchor=(0.0, 0.86), fontsize=5,
               ncol=1, borderpad=0.2, labelspacing=0.3)
    axb.set_title("the result depends on which pLDDT you aggregate",
                  fontsize=6.5)
    axb.text(0.99, 0.985, "filled = signed at cluster bootstrap\n"
             "open = interval includes zero",
             transform=axb.transAxes, ha="right", va="top", fontsize=4.5,
             color=fs.GREY)
    fs.panel_label(axb, "b", dx=-0.22)

    # ---- c: the scatter ----------------------------------------------------
    for i, bb in enumerate(fs.BACKBONE_ORDER):
        ax = axc[i]
        d = scat[scat.backbone == bb]
        fp.confidence_vs_measure(
            ax, d, "plddt_at_anchors", "rmsd_to_active_ref",
            max_points=2000)
        ax.collections[0].set_color(fs.BACKBONE_COLOURS[bb])
        r = np.corrcoef(d.plddt_at_anchors, d.rmsd_to_active_ref)[0, 1]
        ax.set_title("%s   r = %+.3f" % (fs.BACKBONE_LABELS[bb], r),
                     fontsize=6)
        ax.set_xlabel("")
        ax.set_ylabel(u"RMSD to the active reference (Å)" if i == 0 else "")
        if i:
            ax.tick_params(labelleft=False)
        ax.text(0.03, 0.03, "n=%d" % len(d), transform=ax.transAxes,
                fontsize=5, color=fs.GREY)
    axc[1].set_xlabel("mean pLDDT at the state anchors")
    axc[1].xaxis.set_label_coords(1.04, -0.115)
    fs.panel_label(axc[0], "c", dx=-0.36)

    # ---- d: the per-receptor sign census -----------------------------------
    labels, counts, cols2 = [], [], {}
    for bb in fs.BACKBONE_ORDER:
        for agg in AGG_ORDER:
            d = pr[(pr.backbone == bb) & (pr.aggregation == agg)]
            lab = "%s — %s" % (fs.BACKBONE_LABELS[bb],
                               AGG_LABEL[agg].split("  ")[0])
            labels.append(lab)
            counts.append(int((d["sign"] == "neg").sum()))
            cols2[lab] = fs.BACKBONE_COLOURS[bb]
    total = int(pr[(pr.backbone == "boltz") &
                   (pr.aggregation == "plddt_mean")].receptor.nunique())
    fp.count_dots(axd, labels, counts, total=total, colours=cols2,
                  order_by_count=False, label_gap=0.03)
    axd.axvline(total / 2.0, color=fs.GREY, lw=0.6, ls=(0, (2, 2)), zorder=0)
    axd.set_xlabel("receptors with a NEGATIVE within-receptor r (of %d)"
                   % total)
    axd.set_title("the pooled r is not the typical receptor", fontsize=6.5)
    axd.text(total / 2.0, -0.9, " half", fontsize=5, color=fs.GREY,
             ha="left", va="bottom")
    fs.panel_label(axd, "d", dx=-0.55)

    paths = fs.save(fig, "ba5_confidence")
    print("BA-5 ->", paths[0])
    print("  a,b,d population : %s (n=%d rows, %d receptors)"
          % (popfilt, popn, pop.receptor.nunique()))
    print("  c population     : the same, plus %s -> n=%d"
          % (corefilt, len(scat)))
    print("  csv n_receptors  : %s   (actual distinct receptors: %d)"
          % (sorted(pc.n_receptors.unique()), pop.receptor.nunique()))
    print("  signed at cluster boot, primary aggregation: %s"
          % pc[pc.primary_or_secondary == "primary"]
          .set_index("backbone").signed_at_cluster_boot.to_dict())
    for bb in fs.BACKBONE_ORDER:
        d = pc[pc.backbone == bb].set_index("aggregation")
        print("     %-9s global %+.3f -> anchor mean %+.3f -> anchor min %+.3f"
              % (bb, d.loc["plddt_mean"].pearson_r,
                 d.loc["plddt_at_anchors"].pearson_r,
                 d.loc["min_plddt_at_anchor"].pearson_r))
    print("  per-receptor negative counts: %s" % dict(zip(labels, counts)))
    return paths


if __name__ == "__main__":
    main()
