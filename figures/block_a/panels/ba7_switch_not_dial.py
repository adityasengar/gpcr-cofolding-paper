"""
BA-7 - a switch, not a dial.

Every receptor x backbone x arm cell in Block A was run with 25 seeds. That
makes a per-cell quantity nobody has drawn yet: the fraction of seeds whose
prediction the predicate calls active. If the cognate co-input were nudging a
continuous coordinate, those fractions would spread out over (0, 1). They do
not. 111 of 160 apo cells never fire on any seed and 108 of 159 cognate cells
fire on every seed. The co-input flips a switch.

That matters for two separate reasons. It says the arm effect is not an average
over a wide within-cell distribution, so BA-2's medians are not hiding a
bimodal panel; and it bounds what seed variance can be blamed for, which is the
thing a reader reaches for first when a model changes its answer.

  a  the distribution of per-cell active fraction, both arms, ONE shared
     vertical scale, counts printed on the two closed end bins
  b  the same cells paired: apo fraction against cognate fraction, one point
     per receptor x backbone, the identity line drawn. 120 up, 37 unchanged,
     2 down, and the two that go down are named
  c  the per-cell matrix, receptor x backbone, so the U-shape in a and the
     identity of every cell in b are both recoverable from one figure

Population: 01_rows/block_a_rows.csv under `core` (E1+E2), Class A only.
319 cells; 314 carry 25 seeds, 4 carry 24 and 1 carries 20, and the seed budget
is printed on panel a because a fraction of 25 and a fraction of 20 are not the
same measurement. 159 receptor x backbone pairs have both arms.

E3/E4/E5 are not applied beyond the Class A restriction: no reference value is
a denominator or a predictor here, and the predicate call is not divided by
anything.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

import badata as B                                            # noqa: E402
import figstyle as fs                                         # noqa: E402
import figpanels as fp                                        # noqa: E402
import matplotlib.pyplot as plt                               # noqa: E402

ARM_ORDER = ["apo", "cognate"]


def main():
    fs.use_house_style()

    rows = B.rows()
    core, label, n_core = B.core(rows)
    cA = core[core["gpcr_class"] == "A"].copy()

    cells = (cA.groupby(["receptor", "backbone", "arm"])
             .agg(seeds=("active", "size"), fired=("active", "sum"))
             .reset_index())
    cells["frac"] = cells["fired"] / cells["seeds"]

    wide = cells.pivot_table(index=["receptor", "backbone"], columns="arm",
                             values="frac").dropna()
    paired = wide.reset_index()

    up = int((paired["cognate"] > paired["apo"]).sum())
    same = int((paired["cognate"] == paired["apo"]).sum())
    down = paired[paired["cognate"] < paired["apo"]]

    fig = plt.figure(figsize=(fs.W2, 150 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 1.0, 1.30],
                          width_ratios=[1.25, 1.0])

    # --- a: the U-shape --------------------------------------------------
    axa = fig.add_subplot(gs[0, 0])
    budget = int(round(cells["seeds"].median()))
    edges = (np.arange(budget + 2) - 0.5) / float(budget)
    hist_max = 0
    for arm in ARM_ORDER:
        h, _ = np.histogram(cells[cells["arm"] == arm]["frac"], bins=edges)
        hist_max = max(hist_max, h.max())
    stats = fp.bounded_fraction_hist(
        axa, cells, "arm", "frac", n_col="seeds", colours=fs.ARM_COLOURS,
        order=ARM_ORDER, labels=fs.ARM_LABELS,
        xlabel="fraction of seeds the predicate calls active",
        ylabel="receptor × backbone cells", share_max=hist_max * 1.18)
    axa.legend(loc="upper center", fontsize=5.5)
    fs.panel_label(axa, "a", dx=-0.14, dy=1.10)
    axa.set_title(u"%d of %d apo cells never fire; %d of %d cognate cells "
                  u"fire on every seed"
                  % (stats["apo"]["at_zero"], stats["apo"]["n"],
                     stats["cognate"]["at_one"], stats["cognate"]["n"]),
                  fontsize=6.5, loc="left")

    # --- b: paired, with the identity line -------------------------------
    axb = fig.add_subplot(gs[0, 1])
    jit = np.random.RandomState(0).uniform(-0.016, 0.016, (len(paired), 2))
    axb.plot([0, 1], [0, 1], color=fs.GREY, lw=0.6, ls=(0, (3, 2)), zorder=1)
    # 13 corpus papers draw a diagonal and every one of them uses it as a
    # state-call boundary, so a reader of this literature will read an
    # unlabelled diagonal as a classifier. Say in words what it is.
    axb.text(0.52, 0.485, "identity: cognate = apo\n(no change)", fontsize=5,
             color=fs.GREY, rotation=45, rotation_mode="anchor", va="top")
    for i, bb in enumerate(fs.BACKBONE_ORDER):
        m = (paired["backbone"] == bb).values
        axb.scatter(paired["apo"][m] + jit[m, 0], paired["cognate"][m] + jit[m, 1],
                    s=13, facecolors=fs.BACKBONE_COLOURS[bb], edgecolors="none",
                    alpha=0.75, zorder=3,
                    label="%s (%d cells)" % (fs.BACKBONE_LABELS[bb], int(m.sum())))
    for _, r in down.iterrows():
        axb.annotate("%s/%s" % (r["receptor"], fs.BACKBONE_LABELS[r["backbone"]]),
                     (r["apo"], r["cognate"]), xytext=(4, -7),
                     textcoords="offset points", fontsize=4.8, color=fs.BLACK)
    axb.set_xlabel("apo: fraction of seeds called active")
    axb.set_ylabel("cognate Gα: fraction called active")
    axb.set_xlim(-0.06, 1.06)
    axb.set_ylim(-0.06, 1.06)
    axb.legend(loc="lower right", fontsize=5, handlelength=0.8,
               labelspacing=0.2, borderpad=0.2)
    axb.text(0.035, 0.60,
             u"%d of %d cells up\n%d unchanged · %d down\njitter ±0.016 so "
             u"coincident\ncells are countable" % (up, len(paired), same, len(down)),
             transform=axb.transAxes, va="top", ha="left", fontsize=5,
             color=fs.GREY)
    fs.panel_label(axb, "b", dx=-0.17, dy=1.10)

    # --- c: the per-cell matrix, both arms -------------------------------
    order = (wide["cognate"] - wide["apo"]).groupby(level=0).mean() \
        .sort_values(ascending=False).index.tolist()
    for k, arm in enumerate(ARM_ORDER):
        ax = fig.add_subplot(gs[1 + k, :])
        tab = (cells[cells["arm"] == arm]
               .pivot_table(index="backbone", columns="receptor", values="frac")
               .reindex(index=fs.BACKBONE_ORDER, columns=order))
        # An absent cell must not look like a zero cell. On a sequential map
        # zero is nearly white, so "white for missing" would make the two
        # identical - the exact defect a coverage grid exists to prevent. So
        # absent cells get a grey fill AND a drawn cross.
        import copy as _copy
        import matplotlib as _mpl
        cmap = _copy.copy(_mpl.cm.get_cmap("BuGn"))
        cmap.set_bad("#c9c9c9")
        masked = np.ma.masked_invalid(tab.values)
        im = ax.imshow(masked, aspect="auto", cmap=cmap, vmin=0.0, vmax=1.0)
        for rr, cc in zip(*np.where(np.isnan(tab.values))):
            ax.plot([cc - 0.34, cc + 0.34], [rr - 0.34, rr + 0.34],
                    color="white", lw=0.9, zorder=4)
            ax.plot([cc - 0.34, cc + 0.34], [rr + 0.34, rr - 0.34],
                    color="white", lw=0.9, zorder=4)
        ax.set_xticks(np.arange(tab.shape[1]))
        ax.set_xticklabels(tab.columns, rotation=90, fontsize=4.6)
        ax.set_yticks(np.arange(tab.shape[0]))
        ax.set_yticklabels([fs.BACKBONE_LABELS[b] for b in tab.index],
                           fontsize=5.5)
        ax.set_xticks(np.arange(-0.5, tab.shape[1], 1), minor=True)
        ax.set_yticks(np.arange(-0.5, tab.shape[0], 1), minor=True)
        ax.grid(which="minor", color="white", linewidth=0.5)
        ax.tick_params(which="minor", length=0)
        n_absent = int(np.isnan(tab.values).sum())
        ax.set_title(u"%s — %d cells, %d absent (grey and crossed, not zero)"
                     % (fs.ARM_LABELS[arm], int(tab.notna().values.sum()),
                        n_absent),
                     fontsize=6.5, loc="left",
                     color=fs.ARM_COLOURS[arm])
        if k == 0:
            fs.panel_label(ax, "c", dx=-0.055, dy=1.38)
        if k == len(ARM_ORDER) - 1:
            ax.set_xlabel(
                u"Filter: %s, then Class A only. %s of %s rows survive E1+E2; "
                u"%s are Class A, forming %d cells (25 seeds each except 4 at "
                u"24 and 1 at 20) and %d receptor × backbone pairs with both "
                u"arms.\nPredicate: TM6 tilt (2×46 Cα–6×37 Cα) > %.3f Å AND "
                u"NPxxY (Y5.58 OH–Y7.53 OH) < %.3f Å. Receptors ordered by "
                u"mean cognate−apo change. The colour scale is identical in "
                u"both rows."
                % (label, "{:,}".format(n_core), "{:,}".format(len(rows)),
                   "{:,}".format(len(cA)), len(cells), len(paired),
                   B.THR_TILT, B.THR_NPXXY),
                fontsize=4.8, color=fs.GREY, labelpad=6)
        cb = fig.colorbar(im, ax=ax, fraction=0.014, pad=0.006)
        cb.set_label("fraction active", fontsize=5.5)
        cb.ax.tick_params(labelsize=5)
        cb.outline.set_linewidth(0.4)

    paths = fs.save(fig, "ba7_switch_not_dial")
    print("BA-7 written:", *paths, sep="\n  ")
    print("\n  cells:", len(cells), " paired:", len(paired))
    for arm in ARM_ORDER:
        print("  %-8s %s" % (arm, stats[arm]))
    print("  up %d  unchanged %d  down %d" % (up, same, len(down)))
    print(down.to_string())


if __name__ == "__main__":
    main()
