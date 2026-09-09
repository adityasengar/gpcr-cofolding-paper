"""
BA-2 - the main effect: the cognate Ga arm against the apo arm.

  a  the raw TM6 tilt distributions, four backbones x two arms, with the
     predicate threshold drawn. Every observation, no summarising bar.
  b  the same contrast within receptor - one line per receptor per backbone,
     so a receptor that moves the wrong way is visible rather than averaged.
  c  the median cognate-apo tilt shift with its CLUSTER-bootstrap interval.
  d  the per-cell predicate firing rate, apo against cognate.

FILTER. Panels a, b, c: E1+E2 only (broken cell, impossible geometry) - 9,461
of 9,490 rows, 99.7%. E3 is NOT applied: no reference value is a denominator
or a predictor anywhere in this figure. E4/E5 are not applied either; panel a
separates the classes by colour instead of dropping them, and S1 shows what
every exclusion combination does to the headline.

Panel d is Class A only, because it uses `both_fire_rate` from cell_summary,
which is the (NPxxY and tilt) rate; that equals the class-aware `active`
predicate on Class A rows exactly and does NOT on Class B/F, which are called
on tilt alone.

CIs are the *_cluster_ci_* columns. The claim sheet's SC-1 table quotes the
receptor-bootstrap numbers under a "cluster-boot" heading (DISCREPANCY_REPORT
D5); the cluster interval is the authoritative and wider one and is what is
drawn here. Receptor intervals appear in S3 and nowhere else.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

import numpy as np                                          # noqa: E402
import pandas as pd                                         # noqa: E402
import badata as B                                          # noqa: E402
import figstyle as fs                                       # noqa: E402
import figpanels as fp                                      # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402

TILT = "d_gpcrdb_tm6_tilt_246_637_ca"


def main():
    fs.use_house_style()
    raw = B.rows()
    rows, filt, n = B.core(raw)
    head = B.load("03_aggregates/headline_by_backbone.csv")
    rsum = B.load("03_aggregates/receptor_summary.csv")
    cells = B.load("03_aggregates/cell_summary.csv")

    fig = plt.figure(figsize=(fs.W2, 148 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.45, 1.0],
                          height_ratios=[1.0, 1.0])
    axa = fig.add_subplot(gs[0, 0])
    axc = fig.add_subplot(gs[0, 1])
    sub = gs[1, 0].subgridspec(1, 4, wspace=0.08)
    axb = [fig.add_subplot(sub[0, i]) for i in range(4)]
    axd = fig.add_subplot(gs[1, 1])

    # ---- a: raw tilt distributions ---------------------------------------
    counts = fp.grouped_strip(
        axa, rows, "backbone", "arm", TILT,
        outer_order=fs.BACKBONE_ORDER, inner_order=["apo", "cognate"],
        inner_colours=fs.ARM_COLOURS, outer_labels=fs.BACKBONE_LABELS,
        ylabel=u"TM6 tilt, 2×46–6×37 Cα (Å)")
    axa.axhline(B.THR_TILT, color=fs.BLACK, lw=0.6, ls=(0, (3, 2)), zorder=1)
    axa.text(axa.get_xlim()[1], B.THR_TILT,
             u" tilt threshold %.2f Å" % B.THR_TILT, fontsize=5,
             color=fs.BLACK, va="bottom", ha="right")
    import matplotlib.patches as mpatches
    axa.legend(handles=[mpatches.Patch(color=fs.ARM_COLOURS[a],
                                       label=fs.ARM_LABELS[a])
                        for a in ("apo", "cognate")],
               loc="upper left", fontsize=5.5, ncol=2)
    axa.set_title("raw TM6 tilt, every prediction", fontsize=6.5)
    fs.panel_label(axa, "a", dx=-0.11)

    # ---- c: the headline shift, cluster intervals -------------------------
    eff_n = [int(rsum[(rsum.backbone == b)]
                 .delta_cognate_minus_apo_tilt.notna().sum())
             for b in fs.BACKBONE_ORDER]
    h = head.set_index("backbone").loc[fs.BACKBONE_ORDER]
    fres = fp.forest(
        axc, [fs.BACKBONE_LABELS[b] for b in fs.BACKBONE_ORDER],
        h.median_tilt_shift.values,
        h.median_tilt_shift_cluster_ci_lo.values,
        h.median_tilt_shift_cluster_ci_hi.values,
        colours=[fs.BACKBONE_COLOURS[b] for b in fs.BACKBONE_ORDER],
        null=0.0, null_label="no shift", ns=eff_n,
        xlabel=u"median cognate − apo TM6 tilt shift (Å)")
    axc.legend(handles=fres["handles"], loc="lower right", fontsize=5,
               borderpad=0.2)
    axc.set_title("headline shift, cluster-bootstrap 95% CI", fontsize=6.5)
    axc.text(0.5, -0.30, "cluster bootstrap over paralog clusters "
             "(authoritative, C-8);\nreceptor-bootstrap intervals are in S3",
             transform=axc.transAxes, ha="center", va="top", fontsize=5,
             color=fs.GREY)
    fs.panel_label(axc, "c", dx=-0.30)

    # ---- b: within receptor ----------------------------------------------
    long = []
    for _, r in rsum.iterrows():
        for arm, col in (("apo", "apo_" + TILT + "_median"),
                         ("cognate", "cognate_" + TILT + "_median")):
            long.append((r.receptor, r.backbone, arm, r[col]))
    longdf = pd.DataFrame(long, columns=["receptor", "backbone", "arm", "tilt"])
    ylo = np.nanmin(longdf.tilt) - 0.6
    yhi = np.nanmax(longdf.tilt) + 0.6
    for i, bb in enumerate(fs.BACKBONE_ORDER):
        ax = axb[i]
        d = longdf[longdf.backbone == bb]
        piv = fp.paired_slope(ax, d, "receptor", "arm", "tilt",
                              "apo", "cognate", colour=fs.GREY)
        down = int((piv["cognate"] < piv["apo"]).sum())
        ax.axhline(B.THR_TILT, color=fs.BLACK, lw=0.5, ls=(0, (3, 2)),
                   zorder=0)
        ax.set_ylim(ylo, yhi)
        ax.set_title(fs.BACKBONE_LABELS[bb], fontsize=6)
        ax.set_xticklabels([fs.ARM_LABELS[a] for a in ("apo", "cognate")],
                           rotation=20, ha="right")
        ax.text(0.5, 0.985, "%d of %d move down" % (down, len(piv)),
                transform=ax.transAxes, ha="center", va="top", fontsize=5,
                color=fs.VERM if down else fs.GREY)
        if i:
            ax.set_ylabel("")
            ax.set_yticklabels([])
        else:
            ax.set_ylabel(u"median TM6 tilt per receptor (Å)")
    fs.panel_label(axb[0], "b", dx=-0.42)

    # ---- d: predicate firing rate, per cell ------------------------------
    ca = cells[cells.gpcr_class == "A"]
    fp.grouped_strip(axd, ca, "backbone", "arm", "both_fire_rate",
                     outer_order=fs.BACKBONE_ORDER,
                     inner_order=["apo", "cognate"],
                     inner_colours=fs.ARM_COLOURS,
                     outer_labels=fs.BACKBONE_LABELS,
                     ylabel="predicate-active fraction within a cell")
    _y0, _y1 = axd.get_ylim()
    axd.set_ylim(_y0, max(_y1, 1.08))
    # the pooled row-level rate, which is what headline_by_backbone reports
    pos = 0.0
    for bb in fs.BACKBONE_ORDER:
        for arm in ("apo", "cognate"):
            d = rows[(rows.backbone == bb) & (rows.arm == arm) &
                     (rows.gpcr_class == "A")]
            axd.plot([pos], [(d.npxxy_active & d.tilt_active).mean()],
                     marker="D", markersize=3.2, color=fs.BLACK,
                     markerfacecolor="none", markeredgewidth=0.8, zorder=5)
            pos += 1.0
        pos += 0.55
    axd.set_title("predicate firing, per (receptor, backbone, arm) cell",
                  fontsize=6.5, pad=18)
    import matplotlib.lines as mlines
    axd.legend(handles=[mlines.Line2D([], [], lw=0, marker="D", markersize=3.2,
                                      color=fs.BLACK, markerfacecolor="none",
                                      markeredgewidth=0.8,
                                      label="pooled row-level rate over all "
                                            "Class A rows\n(the number "
                                            "headline_by_backbone.csv reports)")],
               loc="lower center", bbox_to_anchor=(0.5, 1.005), fontsize=5,
               borderpad=0.2, handletextpad=0.4)
    fs.panel_label(axd, "d", dx=-0.30)

    paths = fs.save(fig, "ba2_arm_shift")
    print("BA-2 ->", paths[0])
    print("  filter (a,b,c) : %s" % B.describe_filter(filt, n))
    print("  panel a cells  : %s" % {k: v for k, v in counts.items()})
    print("  panel c        : cluster CIs, effective n receptors %s"
          % dict(zip(fs.BACKBONE_ORDER, eff_n)))
    print("  panel d filter : Class A cells only, n=%d of %d cells"
          % (len(ca), len(cells)))
    for bb in fs.BACKBONE_ORDER:
        d = ca[ca.backbone == bb]
        print("     %-9s per-cell median apo %.3f cognate %.3f | pooled row "
              "apo %.3f cognate %.3f"
              % (bb,
                 d[d.arm == "apo"].both_fire_rate.median(),
                 d[d.arm == "cognate"].both_fire_rate.median(),
                 (rows[(rows.backbone == bb) & (rows.arm == "apo") &
                       (rows.gpcr_class == "A")].npxxy_active &
                  rows[(rows.backbone == bb) & (rows.arm == "apo") &
                       (rows.gpcr_class == "A")].tilt_active).mean(),
                 (rows[(rows.backbone == bb) & (rows.arm == "cognate") &
                       (rows.gpcr_class == "A")].npxxy_active &
                  rows[(rows.backbone == bb) & (rows.arm == "cognate") &
                       (rows.gpcr_class == "A")].tilt_active).mean()))
    return paths


if __name__ == "__main__":
    main()
