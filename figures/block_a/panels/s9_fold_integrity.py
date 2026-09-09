"""
S9 - fold integrity: is the thing being measured still a receptor?

A tilt distance means nothing if TM6 has stopped being a helix, so the scorer
carries a helicity fraction over BW 6.30-6.50 and a pass at >= 0.80. SC-8
claims 96.3% overall. That reproduces, but the failures are not spread evenly:
they are almost entirely Class B, which is a scoring-anchor limitation on the
secretin-family TM6 kink motif rather than a fold defect.

  a  the helicity fraction itself, by backbone and class, with the 0.80 line
  b  the pass rate as a census, per backbone and per class

FILTER: E1+E2 (9,461 of 9,490). Deliberately NOT Class-A-restricted: the point
of the panel is where the failures are.
"""
exec(open(__file__.replace("s9_fold_integrity.py", "_shead.py")).read())
import numpy as np                                          # noqa: E402
import badata as B, figstyle as fs, figpanels as fp         # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402

HEL = "tm6_helicity_6_30_6_50"
CLASS_COLOURS = {"A": fs.BLUE, "B": fs.VERM, "F": fs.GREEN}


def main():
    fs.use_house_style()
    rows, filt, n = B.core(B.rows())

    fig = plt.figure(figsize=(fs.W2, 84 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0])
    axes = [fig.add_subplot(gs[0, 0])]
    subb = gs[0, 1].subgridspec(3, 1, hspace=0.55)
    axbs = [fig.add_subplot(subb[i, 0]) for i in range(3)]
    fp.grouped_strip(axes[0], rows, "backbone", "gpcr_class", HEL,
                     outer_order=fs.BACKBONE_ORDER,
                     inner_order=["A", "B", "F"],
                     inner_colours=CLASS_COLOURS,
                     outer_labels=fs.BACKBONE_LABELS,
                     ylabel=u"TM6 helicity fraction, BW 6.30–6.50")
    axes[0].axhline(0.80, color=fs.BLACK, lw=0.7, ls=(0, (3, 2)), zorder=3)
    axes[0].text(axes[0].get_xlim()[1], 0.80, " pass at 0.80 ", fontsize=5,
                 color=fs.BLACK, ha="right", va="bottom")
    import matplotlib.patches as mpatches
    axes[0].legend(handles=[mpatches.Patch(color=CLASS_COLOURS[c],
                                           label="Class " + c)
                            for c in ("A", "B", "F")],
                   loc="lower center", bbox_to_anchor=(0.5, 1.02), fontsize=5,
                   ncol=3, borderpad=0.2)
    axes[0].set_title("fold integrity anchor, every prediction", fontsize=6.5,
                      pad=16)
    fs.panel_label(axes[0], "a", dx=-0.12)

    # One axes per class, because the three classes have different cell sizes
    # and count_dots keeps the denominator ON the axis: sharing one axis would
    # have printed "74/1999" for a cell that only has 200 rows in it.
    for i, cl in enumerate(("A", "B", "F")):
        ax = axbs[i]
        labels, counts = [], []
        tot = 0
        for bb in fs.BACKBONE_ORDER:
            d = rows[(rows.backbone == bb) & (rows.gpcr_class == cl)]
            labels.append(fs.BACKBONE_LABELS[bb])
            counts.append(int((~d.tm6_helicity_pass).sum()))
            tot = max(tot, len(d))
        fp.count_dots(ax, labels, counts, total=tot,
                      colours={l: CLASS_COLOURS[cl] for l in labels},
                      order_by_count=False, label_gap=0.03)
        ax.set_xlabel("")
        ax.set_title("Class %s — rows failing the helicity anchor "
                     "(of %d per backbone)" % (cl, tot), fontsize=6)
        ax.tick_params(axis="x", labelsize=5)
    axbs[2].set_xlabel("rows failing the helicity anchor")
    axbs[0].text(0.99, 1.62, "overall pass %.2f%% (SC-8 claims 96.3%%)"
                 % (100 * rows.tm6_helicity_pass.mean()),
                 transform=axbs[0].transAxes, ha="right", va="top",
                 fontsize=5.5, color=fs.BLACK)
    fs.panel_label(axbs[0], "b", dx=-0.30, dy=1.55)

    paths = fs.save(fig, "s9_fold_integrity")
    print("S9 ->", paths[0])
    print("  filter: %s" % B.describe_filter(filt, n))
    print("  overall pass rate %.4f" % rows.tm6_helicity_pass.mean())
    print("  by backbone: %s"
          % rows.groupby("backbone").tm6_helicity_pass.mean().round(4).to_dict())
    print("  by class:    %s"
          % rows.groupby("gpcr_class").tm6_helicity_pass.mean().round(4).to_dict())
    print("  failing rows by (backbone, class): %s"
          % rows[~rows.tm6_helicity_pass].groupby(
              ["backbone", "gpcr_class"]).size().to_dict())
    print("  failing receptors: %s"
          % sorted(rows[~rows.tm6_helicity_pass].receptor.unique()))
    return paths


if __name__ == "__main__":
    main()
