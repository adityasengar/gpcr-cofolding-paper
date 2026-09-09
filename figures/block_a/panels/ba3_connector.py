"""
BA-3 - orthogonal corroboration: the P5.50-F6.44 (PIF) connector.

The connector was never used to call a state. If predictions the predicate
calls active also sit where active references sit on this third, unused
coordinate, that is corroboration the predicate cannot have manufactured.

The figure LEADS with the row-level agreement counts (panel a), because that
is the strong part of this result. The pooled magnitude difference (panel c)
has a cluster interval of [-1.196, +0.026] which INCLUDES ZERO, and every
per-backbone interval includes zero as well, so the null is drawn on that
panel and the point estimates are drawn hollow. The claim sheet's "magnitude
ratio 0.37, CI [0.04, 0.77]" reads as a signed effect and is not one: the
ratio is computed from the ABSOLUTE value of the delta, so its interval
cannot cross zero by construction (DISCREPANCY_REPORT D2). No ratio is
plotted here for that reason.

  a  agreement counts, per backbone, against the fixed denominator of 64
  b  the connector distance itself, by predicate call, as an ECDF
  c  the pooled and per-backbone delta with cluster CIs, zero marked

FILTER. 05_connector/connector_predictions.csv, all 512 rows. This is the T2
scale-up: a balanced stratified sample of 32 rows per
(backbone x arm x predicate call), not the 9,490-row corpus, so the excl_*
flags do not apply and none is used. Reference values are the aggregate
medians in connector_references.csv (active 10.48 A, inactive 11.99 A,
delta -1.51 A, n=77 Class A reference CIFs); the per-reference distances are
NOT in the archive, which is why panel b marks reference medians as lines
rather than drawing a reference distribution.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

import badata as B                                          # noqa: E402
import figstyle as fs                                       # noqa: E402
import figpanels as fp                                      # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402
import matplotlib.lines as mlines                           # noqa: E402


def main():
    fs.use_house_style()
    cp = B.load("05_connector/connector_predictions.csv")
    cs = B.load("05_connector/connector_summary.csv")

    fig = plt.figure(figsize=(fs.W2, 84 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 1.0, 1.15])
    axa = fig.add_subplot(gs[0, 0])
    axb = fig.add_subplot(gs[0, 1])
    axc = fig.add_subplot(gs[0, 2])

    pooled = cs[cs.scope == "pooled"].iloc[0]

    # ---- a: the agreement counts (the strong part) ------------------------
    labels, counts, cols = [], [], {}
    for bb in fs.BACKBONE_ORDER:
        r = cs[cs.scope == "backbone_" + bb].iloc[0]
        for tag, num in ((u"· pred-active below inactive-ref",
                          r.n_pred_active_below_inactive_median),
                         (u"· pred-inactive above active-ref",
                          r.n_pred_inactive_above_active_median)):
            lab = "%s %s" % (fs.BACKBONE_LABELS[bb], tag)
            labels.append(lab)
            counts.append(int(num))
            cols[lab] = fs.BACKBONE_COLOURS[bb]
    fp.count_dots(axa, labels, counts, total=64, colours=cols,
                  order_by_count=False, label_gap=0.03)
    axa.set_xlabel("predictions agreeing (of 64 per backbone)")
    axa.set_title("agreement with the reference medians", fontsize=6.5)
    axa.set_xlim(0, 64 * 1.35)
    axa.text(0.99, 0.99,
             "pooled: %d/%d (%.1f%%) and %d/%d (%.1f%%)"
             % (pooled.n_pred_active_below_inactive_median,
                pooled.n_pred_active_total, pooled.pct_active_below_inactive,
                pooled.n_pred_inactive_above_active_median,
                pooled.n_pred_inactive_total, pooled.pct_inactive_above_active),
             transform=axa.transAxes, ha="right", va="top", fontsize=5,
             color=fs.BLACK,
             bbox=dict(facecolor="white", edgecolor="none", pad=1.0))
    fs.panel_label(axa, "a", dx=-0.62)

    # ---- b: the connector distance itself ---------------------------------
    cp = cp.copy()
    cp["call"] = cp.active_predicate_call.map(
        {True: "predicate-active", False: "predicate-inactive"})
    fp.ecdf(axb, cp, "call", "p550_f644_ca_distance",
            order=["predicate-active", "predicate-inactive"],
            colours={"predicate-active": fs.VERM,
                     "predicate-inactive": fs.BLUE})
    for v, lab, c in ((B.CONN_REF_ACTIVE, "active refs", fs.VERM),
                      (B.CONN_REF_INACTIVE, "inactive refs", fs.BLUE)):
        axb.axvline(v, color=c, lw=0.7, ls=(0, (3, 2)), zorder=1)
        axb.text(v, 0.52 if lab.startswith("active") else 0.40,
                 u" %s median %.2f Å" % (lab, v), fontsize=4.5,
                 color=c, ha="left", va="center",
                 bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
    axb.set_xlabel(u"P5.50–F6.44 Cα distance (Å)")
    axb.set_xscale("log")
    import matplotlib.ticker as mticker
    axb.set_xticks([8, 10, 12, 15, 20, 30, 44])
    axb.xaxis.set_major_formatter(mticker.ScalarFormatter())
    axb.xaxis.set_minor_formatter(mticker.NullFormatter())
    axb.tick_params(axis="x", which="minor", length=1.2)
    axb.set_title("the unused coordinate", fontsize=6.5)
    axb.legend(loc="lower right", fontsize=5, borderpad=0.2)
    axb.text(0.44, 0.30, u"reference medians are aggregates over 77 Class A\n"
             u"reference CIFs; per-reference distances are not in\n"
             u"the archive, so no reference distribution is drawn.\n"
             u"log x: the upper tail reaches 43.8 Å and the axis\n"
             u"is not truncated.",
             transform=axb.transAxes, ha="left", va="top", fontsize=4.2,
             color=fs.GREY)
    fs.panel_label(axb, "b", dx=-0.24)

    # ---- c: the delta, with zero marked -----------------------------------
    order = ["pooled"] + ["backbone_" + b for b in fs.BACKBONE_ORDER]
    rows = cs.set_index("scope").loc[order]
    labs = ["pooled"] + [fs.BACKBONE_LABELS[b] for b in fs.BACKBONE_ORDER]
    cols2 = [fs.BLACK] + [fs.BACKBONE_COLOURS[b] for b in fs.BACKBONE_ORDER]
    fres = fp.forest(
        axc, labs, rows.delta_pred_median.values,
        rows.delta_cluster_ci_lo.values, rows.delta_cluster_ci_hi.values,
        colours=cols2, null=0.0, null_label="no difference",
        reference=B.CONN_REF_DELTA,
        reference_label=u"reference Δ (−1.51 Å)",
        ns=[int(rows.n_pred_active_total.iloc[i] +
                rows.n_pred_inactive_total.iloc[i]) for i in range(len(rows))],
        group_gaps={1},
        xlabel=u"median connector distance,\npredicate-active − predicate-inactive (Å)")
    axc.legend(handles=fres["handles"], loc="upper center",
               bbox_to_anchor=(0.5, -0.26), fontsize=4.5, borderpad=0.2,
               ncol=2)
    axc.set_title("magnitude: every interval includes zero", fontsize=6.5)
    fs.panel_label(axc, "c", dx=-0.34)

    paths = fs.save(fig, "ba3_connector")
    print("BA-3 ->", paths[0])
    print("  source        : 05_connector/, n=%d rows (T2 scale-up), no excl_* "
          "flag applies" % len(cp))
    print("  strata        : %d, %d rows each" % (cp.stratum.nunique(),
                                                  cp.stratum.value_counts()[0]))
    print("  pooled delta  : %.3f A, cluster CI [%.3f, %.3f] -> includes zero: %s"
          % (pooled.delta_pred_median, pooled.delta_cluster_ci_lo,
             pooled.delta_cluster_ci_hi,
             pooled.delta_cluster_ci_lo <= 0 <= pooled.delta_cluster_ci_hi))
    print("  per-backbone excludes zero: %s"
          % dict(zip(labs, fres["excludes_null"])))
    print("  agreement     : %d/%d and %d/%d pooled"
          % (pooled.n_pred_active_below_inactive_median,
             pooled.n_pred_active_total,
             pooled.n_pred_inactive_above_active_median,
             pooled.n_pred_inactive_total))
    print("  connector max : %.2f A (axis is log, not truncated)"
          % cp.p550_f644_ca_distance.max())
    return paths


if __name__ == "__main__":
    main()
