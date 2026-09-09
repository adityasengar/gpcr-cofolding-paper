"""
S5 - the amplitude slopes under all three shipped inclusion sets.

DISCREPANCY_REPORT D3 diagnoses the claim sheet's tilt line as a MIXTURE of
three inclusion sets: its all-positive range resembles `baseline`, its
SD of 1.19 matches `class_a_no_holds` (1.195), and its n = 40 matches none of
the three. The fix is to name one set and quote it consistently, so this panel
draws all three side by side and lets a reader see what the choice does.

Note also that for NPxxY, `baseline` and `class_a_only` are byte-identical
(same slopes, same n=28, same SD) - so no shipped inclusion set produces the
claim sheet's n=34 / SD=4.71.

FILTER: 04_amplitude/amplitude_fits.csv, all 24 rows.
"""
exec(open(__file__.replace("s5_inclusion_sets.py", "_shead.py")).read())
import numpy as np                                          # noqa: E402
import badata as B, figstyle as fs, figpanels as fp         # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402

SETS = ["baseline", "class_a_only", "class_a_no_holds"]


def main():
    fs.use_house_style()
    fits = B.load("04_amplitude/amplitude_fits.csv")

    fig, axes = plt.subplots(1, 2, figsize=(fs.W2, 96 * fs.MM),
                             constrained_layout=True)
    for k, axis in enumerate(("npxxy", "tilt")):
        labs, est, lo, hi, cols, ns, gaps = [], [], [], [], [], [], set()
        i = 0
        for iset in SETS:
            if i:
                gaps.add(i)
            for bb in fs.BACKBONE_ORDER:
                f = fits[(fits.axis == axis) & (fits.inclusion_set == iset) &
                         (fits.backbone == bb)].iloc[0]
                labs.append("%s · %s" % (iset, fs.BACKBONE_LABELS[bb]))
                est.append(f.slope); lo.append(f.cluster_ci_lo)
                hi.append(f.cluster_ci_hi); ns.append(int(f.n_receptors))
                cols.append(fs.BACKBONE_COLOURS[bb])
                i += 1
        res = fp.forest(axes[k], labs, est, lo, hi, colours=cols, null=0.0,
                        null_label="no amplitude reproduction", reference=1.0,
                        reference_label="unity", ns=ns, group_gaps=gaps,
                        xlabel="regression slope")
        sds = {s: fits[(fits.axis == axis) &
                       (fits.inclusion_set == s)].sd_predictor.iloc[0]
               for s in SETS}
        axes[k].set_title(u"%s\nSD(predictor) %s"
                          % ("NPxxY-OH" if axis == "npxxy" else "tilt",
                             " / ".join(u"%.2f Å" % sds[s] for s in SETS)),
                          fontsize=6.5)
        fs.panel_label(axes[k], "ab"[k], dx=-0.62, dy=1.12)
        if k == 0:
            axes[k].legend(handles=res["handles"], loc="upper center",
                           bbox_to_anchor=(1.05, -0.28), fontsize=4.5, ncol=4,
                           borderpad=0.2)
        print("  %s excludes zero: %s"
              % (axis, dict(zip(labs, res["excludes_null"]))))

    lo_all = min(a.get_xlim()[0] for a in axes)
    hi_all = max(a.get_xlim()[1] for a in axes)
    for a in axes:
        a.set_xlim(lo_all, hi_all)   # one scale, so the two axes are comparable
    axes[0].text(0.5, -0.20,
                 "SD(predictor) is quoted in the order "
                 "baseline / class_a_only / class_a_no_holds;\n"
                 "both panels share one x scale so the two measurement axes "
                 "can be compared directly",
                 transform=axes[0].transAxes, ha="center", va="top",
                 fontsize=5, color=fs.GREY)
    paths = fs.save(fig, "s5_inclusion_sets")
    print("S5 ->", paths[0])
    same = (fits[(fits.axis == "npxxy") & (fits.inclusion_set == "baseline")]
            .set_index("backbone")[["slope", "n_receptors", "sd_predictor"]]
            .equals(fits[(fits.axis == "npxxy") &
                         (fits.inclusion_set == "class_a_only")]
                    .set_index("backbone")[["slope", "n_receptors",
                                            "sd_predictor"]]))
    print("  NPxxY baseline == class_a_only (byte-identical): %s" % same)
    print("  n_receptors by (axis, set): %s"
          % fits.groupby(["axis", "inclusion_set"]).n_receptors.first()
          .to_dict())
    print("  sd_predictor by (axis, set): %s"
          % fits.groupby(["axis", "inclusion_set"]).sd_predictor.first()
          .round(3).to_dict())
    return paths


if __name__ == "__main__":
    main()
