# -*- coding: utf-8 -*-
"""BB-5 — the models do not read which family the partner belongs to.

Spec: data/block_b/12_narrative/figures/BB-5_donor_class_residuals.md
Claims: SC-B-6 (Outcome A signed) and SC-B-14 (Outcome B signed nowhere).
Standalone panel, no manuscript figure number, no composite.

TWO THINGS THIS PANEL MUST NOT SAY, both from the claim sheet's own r3 wording:

1. This is NOT an equivalence result. An equivalence upgrade was attempted and
   retracted: the ruler-side bootstrap gave [+0.006, +1.025], too wide to
   exclude anything, and without AA2AR it opens to [-0.047, +1.015] and spans
   zero. No phrasing here may imply a family-specific opening was "ruled out".
2. The interval that supports the conclusion SPANS ZERO. That is drawn, not
   glossed.

And one thing it must say: ONE stratum carries the conclusion. Gs->Gi is powered
at 20 native-referenced receptors; Gs->Gq collapses to 3 and Gi->Gs has none.
The panel shows all three at their true widths so the reader sees which is doing
the work.
"""
import _shead                                                    # noqa: F401
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
import badata as B

fs.use_house_style()
AXIS = "residual_tilt"


def main():
    pw = B.table("07_donor_residuals/phase5_power_analysis.csv")
    p = pw[(pw.backbone == "panel") & (pw.axis == AXIS)].copy()
    p["stratum"] = p.donor_ga_class + " donor on " + p.cognate_ga_class + " receptor"
    p = p.sort_values("native_n_rec", ascending=True)

    fig, (ax, axb) = fs.figure(width=fs.W2, height=86 * fs.MM, ncols=2,
                               gridspec_kw={"width_ratios": [1.55, 1.0]})

    y = np.arange(len(p))
    for i, r in enumerate(p.itertuples()):
        for tag, med, lo, hi, col, dy, n in (
                ("all", r.all_median, r.all_ci_lo, r.all_ci_hi, fs.GREY, +0.16,
                 r.total_n_rec),
                ("native only", r.native_median, r.native_ci_lo, r.native_ci_hi,
                 fs.BLACK, -0.16, r.native_n_rec)):
            if not np.isfinite(med):
                ax.text(-2.85, i + dy, "no native-referenced receptor here",
                        fontsize=5.8, color=fs.VERM, va="center", ha="left")
                continue
            filled = not (lo < 0 < hi)
            ax.errorbar(med, i + dy, xerr=[[med - lo], [hi - med]], fmt="o",
                        ms=5.0, lw=1.4, capsize=2.5, color=col,
                        mfc=col if filled else "white", zorder=3)
            ax.text(hi + 0.06, i + dy, "n=%d" % n, fontsize=5.8, color=col,
                    va="center")
    ax.axvline(0, color=fs.VERM, lw=1.0, zorder=1)
    ax.set_yticks(y); ax.set_yticklabels(p.stratum, fontsize=6.4)
    ax.set_ylim(-0.75, len(p) - 0.25)
    ax.set_xlim(-3.0, 0.75)
    ax.set_xlabel(u"tilt residual against the receptor's own active reference (Å)")
    ax.set_title("only the underpowered stratum signs,\nand in the wrong direction",
                 fontsize=7.4)
    ax.plot([], [], "o", ms=5, color=fs.GREY, label="all receptors")
    ax.plot([], [], "o", ms=5, color=fs.BLACK, mfc="white",
            label="open marker: interval spans zero")
    ax.plot([], [], "o", ms=5, color=fs.BLACK, label="native active reference only")
    ax.legend(frameon=False, fontsize=5.9, loc="upper center",
              bbox_to_anchor=(0.5, -0.20), ncol=3)

    # ---- b: the pre-registered alternative, and how often it signed
    counts = {"Outcome B signed": 0, "signed against B": 1, "undetermined": 8}
    col = [fs.VERM, fs.SKY, fs.GREY]
    bars = axb.bar(range(3), list(counts.values()), width=0.6, color=col,
                   edgecolor="white", lw=0.7)
    for b, v in zip(bars, counts.values()):
        axb.text(b.get_x() + b.get_width() / 2, v + 0.15, str(v), ha="center",
                 fontsize=7.4, fontweight="bold")
    axb.set_xticks(range(3))
    axb.set_xticklabels(["reads partner\nidentity", "reads it the\nother way",
                         "undetermined"], fontsize=6.2)
    axb.set_ylabel("stratum x axis combinations, of 9")
    axb.set_ylim(0, 9.4)
    axb.set_title("the pre-registered alternative\nsigned nowhere", fontsize=7.4)

    fs.panel_label(ax, "a", dx=-0.42); fs.panel_label(axb, "b", dx=-0.24)

    gsgi = p[(p.donor_ga_class == "Gs") & (p.cognate_ga_class == "Gi")].iloc[0]
    note = (u"Residual is the predicted tilt minus the tilt of that receptor's own "
            u"deposited active reference, so zero means the prediction lands where "
            u"the receptor's own active structure sits. If the models read partner "
            u"identity, a donor from the wrong family should overshoot or "
            u"undershoot; the pre-registered test asked exactly that. "
            u"Open markers are intervals spanning zero. One interval does not: "
            u"Gs on Gq over all 8 receptors, at -0.474 [-0.81, -0.08]. It signs "
            u"AGAINST the pre-registered alternative rather than for it, and it "
            u"is the stratum with 3 native references, so it is the least "
            u"trustworthy of the three. Restricted to those 3 it opens to "
            u"[-2.79, +0.14] and spans zero again. "
            u"a, the load-bearing stratum is Gs donor on Gi receptor at %d native "
            u"references, %.3f A [%.2f, %.2f]. The other two are shown at their "
            u"true widths: Gs on Gq collapses to %d native receptors, and Gi on Gs "
            u"has none at all, so ONE of three cells carries the conclusion and it "
            u"is the one that could not have contradicted it. "
            u"b, 0 of 9 stratum x axis combinations sign in the Outcome-B "
            u"direction at 95%% confidence. "
            u"THIS IS NOT AN EQUIVALENCE RESULT: an upgrade to one was attempted "
            u"and retracted because the ruler-side bootstrap gave [+0.006, +1.025], "
            u"too wide to exclude anything, and opens to [-0.047, +1.015] without "
            u"AA2AR. Nothing here rules a family-specific opening out."
            % (gsgi.native_n_rec, gsgi.native_median, gsgi.native_ci_lo,
               gsgi.native_ci_hi,
               int(p[(p.donor_ga_class == "Gs") &
                     (p.cognate_ga_class == "Gq")].native_n_rec.iloc[0])))
    fig.text(0.01, -0.10, "\n".join(textwrap.wrap(note, 132)),
             fontsize=5.4, color=fs.GREY, va="top", ha="left")

    paths = fs.save(fig, "bb5_residuals")
    print("BB-5 ->", paths[0])
    for r in p.itertuples():
        print("  %-28s all n=%-3d %+.3f [%+.2f, %+.2f]   native n=%-3d %s"
              % (r.stratum, r.total_n_rec, r.all_median, r.all_ci_lo, r.all_ci_hi,
                 r.native_n_rec,
                 "-" if not np.isfinite(r.native_median)
                 else "%+.3f [%+.2f, %+.2f]" % (r.native_median, r.native_ci_lo,
                                                r.native_ci_hi)))


if __name__ == "__main__":
    main()
