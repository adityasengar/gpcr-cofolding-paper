"""
S4 - every receptor, every backbone: nothing hides in the pooling.

The headline is a median over receptors. This is the matrix behind it: the
cognate-minus-apo TM6 tilt shift for each of the 48 receptors on each of the
four backbones, with absent cells drawn as absent rather than as zero.

FILTER: 03_aggregates/receptor_summary.csv as shipped (E1/E2 applied upstream
in the per-cell aggregation). No E3, E4 or E5: the point of the panel is to
show every receptor including the Class B and Class F ones, which are marked
on the axis rather than dropped.
"""
exec(open(__file__.replace("s4_per_receptor.py", "_shead.py")).read())
import numpy as np                                          # noqa: E402
import badata as B, figstyle as fs, figpanels as fp         # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402


def main():
    fs.use_house_style()
    rsum = B.load("03_aggregates/receptor_summary.csv")
    cls = rsum.drop_duplicates("receptor").set_index("receptor").gpcr_class
    order = (rsum.groupby("receptor").delta_cognate_minus_apo_tilt.median()
             .sort_values(ascending=False).index.tolist())

    tab = (rsum.pivot_table(index="receptor", columns="backbone",
                            values="delta_cognate_minus_apo_tilt")
           .reindex(index=order, columns=fs.BACKBONE_ORDER))
    tab.columns = [fs.BACKBONE_LABELS[b] for b in tab.columns]
    tab.index = ["%s  [%s]" % (r, cls.get(r, "?")) for r in tab.index]

    fig, ax = plt.subplots(figsize=(fs.W15, 168 * fs.MM),
                           constrained_layout=True)
    v = float(np.nanmax(np.abs(rsum.delta_cognate_minus_apo_tilt)))
    fp.matrix(ax, tab, value_label=u"cognate − apo TM6 tilt shift (Å)",
              cmap="RdBu_r", annotate=True, vmin=-v, vmax=v,
              zero_is_absent=False, annotate_fmt="%.1f")
    ax.set_xticklabels(tab.columns, rotation=0, ha="center")
    ax.tick_params(axis="y", labelsize=5)
    n_missing = int(tab.isna().sum().sum())
    neg = int((rsum.delta_cognate_minus_apo_tilt < 0).sum())
    tot = int(rsum.delta_cognate_minus_apo_tilt.notna().sum())
    ax.set_title("cognate-minus-apo tilt shift, every receptor x backbone\n"
                 "%d of %d cells negative; %d cells absent (drawn white, "
                 "not zero)" % (neg, tot, n_missing), fontsize=6.5)
    ax.set_xlabel("")
    ax.set_ylabel("receptor  [GPCR class]")

    paths = fs.save(fig, "s4_per_receptor")
    print("S4 ->", paths[0])
    print("  receptors %d, backbones %d, cells %d (%d absent)"
          % (len(tab), tab.shape[1], tab.size, n_missing))
    print("  negative shifts: %d of %d non-null cells" % (neg, tot))
    print("  most negative: %s"
          % rsum.nsmallest(5, "delta_cognate_minus_apo_tilt")[
              ["receptor", "backbone", "gpcr_class",
               "delta_cognate_minus_apo_tilt"]].to_dict("records"))
    print("  absent cells: %s"
          % rsum[rsum.delta_cognate_minus_apo_tilt.isna()][
              ["receptor", "backbone"]].to_dict("records"))
    return paths


if __name__ == "__main__":
    main()
