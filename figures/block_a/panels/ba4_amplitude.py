"""
BA-4 - amplitude: does a receptor with further to travel travel further?

This is the negative result, and the null it has to be judged against is
slope = 1, not slope = 0. So the UNITY LINE is drawn on every regression panel
and marked on every forest.

Three things this figure must not do, all of them things the claim sheet does
(DISCREPANCY_REPORT D1 and D3):

  - say "all CIs cross zero". Protenix on NPxxY has a cluster interval of
    [0.074, 0.552], which does not, in any of the three shipped inclusion
    sets. Its interval is drawn clear of zero and its marker is filled.
  - quote a positive tilt slope range. Under `class_a_only` the tilt slopes
    for Boltz (-0.298) and Chai (-0.659) are NEGATIVE. They are drawn.
  - mix inclusion sets in one statement. Every panel here names its set.

  a  NPxxY-OH, four backbones, fit + slope-CI fan + unity line
  b  the slopes as a forest, BOTH axes, zero and unity marked
  c  why the tilt axis cannot answer the question: SD of the predictor is
     1.17 A on tilt against 5.22 A on NPxxY
  d  attenuation sensitivity - the correction diverges on tilt and does
     nothing on NPxxY

FILTER. `class_a_only` throughout the primary panels: Class A (E4) with the
per-axis E3 already applied upstream in amplitude_points.csv - E3 belongs here
because the reference gap IS the regression predictor. n=28 receptors on
NPxxY, 32 on tilt. All three inclusion sets are shown in S5. E1 and E2 are
applied upstream in the per-receptor aggregation.
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

SET = "class_a_only"
INCL = {"baseline": "included_baseline",
        "class_a_only": "included_class_a_only",
        "class_a_no_holds": "included_no_holds"}


def main():
    fs.use_house_style()
    pts = B.load("04_amplitude/amplitude_points.csv")
    fits = B.load("04_amplitude/amplitude_fits.csv")
    att = B.load("04_amplitude/attenuation_sensitivity.csv")

    fig = plt.figure(figsize=(fs.W2, 160 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 1.15, 0.95],
                          width_ratios=[1.0, 1.0])
    suba = gs[0, :].subgridspec(1, 4, wspace=0.06)
    axa = []
    for i in range(4):
        axa.append(fig.add_subplot(suba[0, i], sharex=axa[0] if axa else None,
                                   sharey=axa[0] if axa else None))
    axb = fig.add_subplot(gs[1, 0])
    axc = fig.add_subplot(gs[1, 1])
    subd = gs[2, :].subgridspec(1, 2, wspace=0.16)
    axd = [fig.add_subplot(subd[0, i]) for i in range(2)]

    # ---- a: the NPxxY regressions -----------------------------------------
    p = pts[(pts.axis == "npxxy") & pts[INCL[SET]]]
    xlo, xhi = p.x.min(), p.x.max()
    ylo, yhi = min(p.y.min(), xlo), max(p.y.max(), xhi)
    for i, bb in enumerate(fs.BACKBONE_ORDER):
        ax = axa[i]
        d = p[p.backbone == bb]
        f = fits[(fits.axis == "npxxy") & (fits.inclusion_set == SET) &
                 (fits.backbone == bb)].iloc[0]
        excl = not (f.cluster_ci_lo <= 0 <= f.cluster_ci_hi)
        ax.set_xlim(xlo - 1, xhi + 1)
        ax.set_ylim(ylo - 1, yhi + 1)
        n = fp.regression_with_unity(
            ax, d.x.values, d.y.values, f.slope, f.intercept,
            f.cluster_ci_lo, f.cluster_ci_hi,
            colour=fs.BACKBONE_COLOURS[bb],
            xlabel=u"reference gap Δ (Å)",
            ylabel=u"predicted shift,\ncognate − apo (Å)" if i == 0 else "",
            annotate="slope %.3f\n95%% CI [%.3f, %.3f]%s"
                     % (f.slope, f.cluster_ci_lo, f.cluster_ci_hi,
                        "\nexcludes zero" if excl else ""))
        ax.set_title(fs.BACKBONE_LABELS[bb], fontsize=6)
        ax.set_xlim(xlo - 1, xhi + 1)
        ax.set_ylim(ylo - 1, yhi + 1)
        if i:
            ax.tick_params(labelleft=False)
    fs.panel_label(axa[0], "a", dx=-0.40, dy=1.22)
    fig.text(0.06, 0.995,
             "NPxxY-OH amplitude, inclusion set `%s` (n=%d receptors); "
             "dashed line is unity"
             % (SET, int(fits[(fits.axis == "npxxy") &
                              (fits.inclusion_set == SET)].n_receptors.iloc[0])),
             fontsize=6.5, ha="left", va="top")

    # ---- b: the slopes, both axes -----------------------------------------
    labs, est, lo, hi, cols, ns, gaps = [], [], [], [], [], [], set()
    for ax_i, axis in enumerate(("npxxy", "tilt")):
        for bb in fs.BACKBONE_ORDER:
            f = fits[(fits.axis == axis) & (fits.inclusion_set == SET) &
                     (fits.backbone == bb)].iloc[0]
            labs.append("%s — %s" % (
                "NPxxY-OH" if axis == "npxxy" else "tilt",
                fs.BACKBONE_LABELS[bb]))
            est.append(f.slope); lo.append(f.cluster_ci_lo)
            hi.append(f.cluster_ci_hi); ns.append(int(f.n_receptors))
            cols.append(fs.BACKBONE_COLOURS[bb])
        if ax_i == 0:
            gaps.add(4)
    fres = fp.forest(axb, labs, est, lo, hi, colours=cols, null=0.0,
                     null_label="no amplitude reproduction",
                     reference=1.0, reference_label="unity (full reproduction)",
                     ns=ns, group_gaps=gaps,
                     xlabel="regression slope, predicted shift on reference gap")
    axb.legend(handles=fres["handles"], loc="upper center",
               bbox_to_anchor=(0.5, -0.20), fontsize=4.5, borderpad=0.2,
               ncol=2)
    axb.set_title("slopes, inclusion set `%s`, cluster-bootstrap 95%% CI" % SET,
                  fontsize=6.5)
    fs.panel_label(axb, "b", dx=-0.40)

    # ---- c: restriction of range ------------------------------------------
    long = []
    for axis, lab in (("tilt", "tilt"), ("npxxy", "NPxxY-OH")):
        d = pts[(pts.axis == axis) & pts[INCL[SET]] & (pts.backbone == "boltz")]
        long.append(pd.DataFrame({"axis": [lab] * len(d), "gap": d.x.values}))
    longdf = pd.concat(long, ignore_index=True)
    fp.strip_violin(axc, longdf, "axis", "gap", order=["tilt", "NPxxY-OH"],
                    colours={"tilt": fs.BLUE, "NPxxY-OH": fs.VERM})
    axc.axhline(0, color=fs.GREY, lw=0.5, zorder=0)
    axc.set_ylabel(u"reference gap Δ, the regression predictor (Å)")
    axc.set_xlabel("")
    axc.set_xticklabels(["tilt", "NPxxY-OH"], rotation=0, ha="center")
    y0, y1 = axc.get_ylim()
    axc.set_ylim(y0, y1 + (y1 - y0) * 0.18)
    for i, axis in enumerate(("tilt", "npxxy")):
        f = fits[(fits.axis == axis) & (fits.inclusion_set == SET)].iloc[0]
        axc.text(i, axc.get_ylim()[1],
                 u"SD %.3f Å\nn=%d" % (f.sd_predictor, f.n_receptors),
                 ha="center", va="top", fontsize=5.5, color=fs.BLACK)
    axc.set_title("the tilt axis has no dynamic range to regress on",
                  fontsize=6.5)
    axc.text(0.5, -0.16, "a predictor with SD 1.17 A cannot resolve a slope; "
             "this is an\ninstrument property, not a result about the models "
             "(C-10)",
             transform=axc.transAxes, ha="center", va="top", fontsize=5,
             color=fs.GREY)
    fs.panel_label(axc, "c", dx=-0.26)

    # ---- d: attenuation ----------------------------------------------------
    for i, axis in enumerate(("npxxy", "tilt")):
        ax = axd[i]
        d = att[att.axis == axis]
        base = fits[(fits.axis == axis) & (fits.inclusion_set == SET) &
                    (fits.backbone == "boltz")].iloc[0].slope
        lo_ = float(np.nanmin(d.slope_corrected))
        hi_ = float(np.nanmax(d.slope_corrected))
        pad = (hi_ - lo_) * 0.10
        ax.set_ylim(min(lo_ - pad, -0.2), max(hi_ + pad, 1.25))
        fp.curve_family(ax, d, "sigma_err", "slope_corrected", "backbone",
                        invalid_col="unstable", colours=fs.BACKBONE_COLOURS,
                        labels=fs.BACKBONE_LABELS,
                        xlabel=u"assumed measurement error σ on the reference gap (Å)",
                        ylabel="attenuation-corrected slope" if i == 0 else "")
        ax.axhline(1.0, color=fs.BLACK, lw=0.6, ls=(0, (4, 2)), zorder=1)
        ax.set_title("NPxxY-OH" if axis == "npxxy" else "tilt", fontsize=6)
        nun = int(d.unstable.sum())
        ax.text(0.99, 0.02, "%d of %d swept points unstable" % (nun, len(d)),
                transform=ax.transAxes, ha="right", va="bottom", fontsize=5,
                color=fs.GREY)
        if i == 0:
            ax.legend(loc="lower left", fontsize=5, ncol=2, borderpad=0.2)
    fs.panel_label(axd[0], "d", dx=-0.17)

    paths = fs.save(fig, "ba4_amplitude")
    print("BA-4 ->", paths[0])
    print("  inclusion set : %s" % SET)
    for axis in ("npxxy", "tilt"):
        f = fits[(fits.axis == axis) & (fits.inclusion_set == SET)]
        print("  %-6s n=%d receptors, SD(predictor)=%.3f"
              % (axis, f.n_receptors.iloc[0], f.sd_predictor.iloc[0]))
        for _, r in f.iterrows():
            print("      %-9s slope %+.3f  cluster CI [%+.3f, %+.3f]  %s"
                  % (r.backbone, r.slope, r.cluster_ci_lo, r.cluster_ci_hi,
                     "EXCLUDES ZERO" if not (r.cluster_ci_lo <= 0 <=
                                             r.cluster_ci_hi) else ""))
    print("  attenuation   : unstable points npxxy %d/%d, tilt %d/%d"
          % (int(att[att.axis == "npxxy"].unstable.sum()),
             len(att[att.axis == "npxxy"]),
             int(att[att.axis == "tilt"].unstable.sum()),
             len(att[att.axis == "tilt"])))
    return paths


if __name__ == "__main__":
    main()
