"""
S6 - is the predicate calibrated? What a predicate-active call is worth.

SC-6 claims a 0.02% false-positive rate in its heading and 0.04% in its body;
DISCREPANCY_REPORT D7 corrects it to 2 of 4,866 = 0.041%. Both denominators
are wrong in the same way: of the 4,866 predicate-active rows, only 4,256
carry an RMSD to an active reference at all, so 610 cannot be tested. The
testable rate is 2 of 4,256 = 0.047%. This panel draws the whole distribution
and states both denominators.

  a  RMSD-to-active for every predicate-active row, by backbone, with the 3 A
     line and the untestable rows counted separately
  b  the same for predicate-INACTIVE rows, which is the comparison the
     one-sided FP rate leaves out

FILTER: E1+E2 (9,461 of 9,490). No E3/E4/E5: the predicate's calibration is a
property of the instrument over the whole corpus it was run on, and the
reference-side E3 does not enter, since RMSD-to-active is not a ratio.
"""
exec(open(__file__.replace("s6_predicate_calibration.py", "_shead.py")).read())
import numpy as np                                          # noqa: E402
import badata as B, figstyle as fs, figpanels as fp         # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402


def main():
    fs.use_house_style()
    rows, filt, n = B.core(B.rows())

    rows = rows.copy()
    rows["model"] = rows.backbone.map(fs.BACKBONE_LABELS)
    fig, axes = plt.subplots(1, 2, figsize=(fs.W2, 76 * fs.MM),
                             constrained_layout=True, sharex=True)
    stats = {}
    for k, (call, title) in enumerate(
            ((True, "predicate-ACTIVE rows"),
             (False, "predicate-INACTIVE rows"))):
        ax = axes[k]
        d = rows[rows.active == call]
        testable = d.dropna(subset=["rmsd_to_active_ref"])
        fp.ecdf(ax, testable, "model", "rmsd_to_active_ref",
                order=[fs.BACKBONE_LABELS[b] for b in fs.BACKBONE_ORDER],
                colours={fs.BACKBONE_LABELS[b]: fs.BACKBONE_COLOURS[b]
                         for b in fs.BACKBONE_ORDER})
        ax.axvline(3.0, color=fs.BLACK, lw=0.7, ls=(0, (3, 2)), zorder=1)
        ax.text(3.0, 0.5, u"  3 Å", fontsize=5, color=fs.BLACK, ha="left")
        ax.set_xlabel(u"RMSD to the active reference (Å)")
        gt3 = int((testable.rmsd_to_active_ref > 3).sum())
        stats[title] = dict(rows=len(d), testable=len(testable),
                            untestable=len(d) - len(testable), gt3=gt3)
        ax.set_title(title, fontsize=6.5)
        ax.legend(loc="lower right", fontsize=5, borderpad=0.2,
                  title="testable rows", title_fontsize=5)
        ax.text(0.02, 0.98,
                u"%d rows called %s\n"
                u"%d carry an active reference and are testable\n"
                u"%d carry none and CANNOT be tested\n"
                u"%d exceed 3 Å  =  %.3f%% of the testable rows\n"
                u"(%.3f%% if the untestable rows are counted in\n"
                u"the denominator, as SC-6 does)"
                % (len(d), "active" if call else "inactive", len(testable),
                   len(d) - len(testable), gt3,
                   100.0 * gt3 / max(len(testable), 1),
                   100.0 * gt3 / max(len(d), 1)),
                transform=ax.transAxes, ha="left", va="top", fontsize=5,
                color=fs.BLACK)
        fs.panel_label(ax, "ab"[k], dx=-0.16)

    axes[0].text(0.02, 0.30, "both panels share one x scale; the axis is not\n"
                 "truncated at either end",
                 transform=axes[0].transAxes, ha="left", va="top", fontsize=5,
                 color=fs.GREY)
    paths = fs.save(fig, "s6_predicate_calibration")
    print("S6 ->", paths[0])
    print("  filter: %s" % B.describe_filter(filt, n))
    for t, s in stats.items():
        print("   %-24s rows %5d  testable %5d  untestable %4d  >3A %d  "
              "rate(testable) %.4f%%  rate(all) %.4f%%"
              % (t, s["rows"], s["testable"], s["untestable"], s["gt3"],
                 100.0 * s["gt3"] / max(s["testable"], 1),
                 100.0 * s["gt3"] / max(s["rows"], 1)))
    a = rows[rows.active].dropna(subset=["rmsd_to_active_ref"])
    print("   per backbone, predicate-active >3A: %s"
          % a.groupby("backbone").apply(
              lambda g: "%d/%d" % (int((g.rmsd_to_active_ref > 3).sum()),
                                   len(g))).to_dict())
    return paths


if __name__ == "__main__":
    main()
