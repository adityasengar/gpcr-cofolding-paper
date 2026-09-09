"""
S3 - cluster bootstrap against receptor bootstrap.

The ONLY panel in this figure set that draws receptor-bootstrap intervals.
Methods 7.4 makes the cluster bootstrap over paralog clusters authoritative
and the receptor bootstrap secondary and ~1.10x tighter; 8.4 confines receptor
intervals to the supplement. The claim sheet's SC-1 table nevertheless quotes
the RECEPTOR intervals under a "95% CI (cluster-boot)" heading
(DISCREPANCY_REPORT D5) - for Boltz an exact byte-for-byte match to the
receptor interval - so this panel exists to show the reader what the two
bootstraps actually differ by.

FILTER: 03_aggregates/headline_by_backbone.csv as shipped, both metrics that
are legal to draw. The fraction is excluded: Table T2 only, by the hard rule.
"""
exec(open(__file__.replace("s3_bootstrap_comparison.py", "_shead.py")).read())
import numpy as np                                          # noqa: E402
import badata as B, figstyle as fs, figpanels as fp         # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402
import matplotlib.lines as mlines                           # noqa: E402

METRICS = [("median_tilt_shift", u"median cognate − apo TM6 tilt shift (Å)",
            "n_receptors_tilt", "delta_cognate_minus_apo_tilt"),
           ("median_delta_to_active_shift",
            u"median cognate − apo delta-to-active shift (Å)",
            "n_receptors_delta", "delta_cognate_minus_apo_delta_to_active")]


def main():
    fs.use_house_style()
    h = B.load("03_aggregates/headline_by_backbone.csv").set_index("backbone")
    rsum = B.load("03_aggregates/receptor_summary.csv")

    fig, axes = plt.subplots(1, 2, figsize=(fs.W2, 78 * fs.MM),
                             constrained_layout=True)
    report = []
    for k, (metric, xlab, ncol, effcol) in enumerate(METRICS):
        ax = axes[k]
        ypos = np.arange(len(fs.BACKBONE_ORDER))
        ax.axvline(0, color=fs.GREY, lw=0.8, zorder=0)
        for i, bb in enumerate(fs.BACKBONE_ORDER):
            r = h.loc[bb]
            c = fs.BACKBONE_COLOURS[bb]
            for dy, lo, hi, lw, alpha in (
                    (-0.16, r[metric + "_cluster_ci_lo"],
                     r[metric + "_cluster_ci_hi"], 1.4, 1.0),
                    (+0.16, r[metric + "_receptor_ci_lo"],
                     r[metric + "_receptor_ci_hi"], 1.4, 0.45)):
                ax.plot([lo, hi], [i + dy] * 2, color=c, lw=lw, alpha=alpha,
                        solid_capstyle="butt")
                for b in (lo, hi):
                    ax.plot([b, b], [i + dy - 0.09, i + dy + 0.09], color=c,
                            lw=1.0, alpha=alpha)
            ax.plot([r[metric]], [i], marker="o", markersize=4, color=c,
                    zorder=4)
            wc = r[metric + "_cluster_ci_hi"] - r[metric + "_cluster_ci_lo"]
            wr = r[metric + "_receptor_ci_hi"] - r[metric + "_receptor_ci_lo"]
            ax.text(ax.get_xlim()[1], i, u"  ×%.2f" % (wc / wr), fontsize=5,
                    color=fs.GREY, va="center", clip_on=False)
            eff = int(rsum[rsum.backbone == bb][effcol].notna().sum())
            report.append((metric, bb, wc, wr, wc / wr, int(r[ncol]), eff))
        ax.set_yticks(ypos)
        ax.set_yticklabels([fs.BACKBONE_LABELS[b] for b in fs.BACKBONE_ORDER])
        ax.set_ylim(len(ypos) - 0.5, -0.5)
        ax.set_xlabel(xlab)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ratios = [r[4] for r in report if r[0] == metric]
        ax.set_title(u"cluster / receptor width ratio %.2f–%.2f"
                     % (min(ratios), max(ratios)), fontsize=6.5)
        fs.panel_label(ax, "ab"[k], dx=-0.30)
    axes[0].legend(handles=[
        mlines.Line2D([], [], color=fs.BLACK, lw=1.4,
                      label="cluster bootstrap (authoritative)"),
        mlines.Line2D([], [], color=fs.BLACK, lw=1.4, alpha=0.45,
                      label="receptor bootstrap (secondary, tighter)")],
        loc="upper center", bbox_to_anchor=(0.5, -0.20), fontsize=5,
        borderpad=0.2, ncol=2)
    axes[1].text(0.5, -0.20,
                 "the ratio beside each row is cluster width / receptor width;\n"
                 "the claim sheet and the drop README both describe the "
                 "receptor bootstrap as ~1.10x tighter, which holds on 2 of "
                 "these 8 rows",
                 transform=axes[1].transAxes, ha="center", va="top",
                 fontsize=5, color=fs.GREY)

    paths = fs.save(fig, "s3_bootstrap_comparison")
    print("S3 ->", paths[0])
    for m, bb, wc, wr, ratio, ncsv, eff in report:
        print("   %-30s %-9s cluster width %.3f  receptor %.3f  ratio %.2f  "
              "| n_receptors column says %d, non-null per-receptor values %d"
              % (m, bb, wc, wr, ratio, ncsv, eff))
    return paths


if __name__ == "__main__":
    main()
