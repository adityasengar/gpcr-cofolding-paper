"""
BA-1 b/c/d - the instrument and its calibration.

The predicate is a rule over two distances. Before it is applied to a single
prediction it has to be shown behaving on structures whose state is already
known, which is what the 168 deposited references are for. Three panels:

  b  the predicate plane: both axes, both thresholds, every reference, with the
     nine that disagree with their own deposited label named and shaped.
  c  the per-receptor gap between the active and the inactive reference on each
     axis - the instrument's dynamic range, and the reason the tilt axis cannot
     resolve amplitude later.
  d  the census of predicate calls over all 168 references.

BA-1a is the structural schematic and is built by render_struct.py; see
FIGURE_PROVENANCE.md for the command.

Population: all 168 rows of 02_references/reference_predicates.csv. No excl_*
flag applies here - those are row-level flags on PREDICTIONS, and this figure
contains no prediction.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))          # figures/block_a
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))   # figures/

import badata as B                                          # noqa: E402
import figstyle as fs                                       # noqa: E402
import figpanels as fp                                      # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402


def main():
    fs.use_house_style()

    rp = B.load("02_references/reference_predicates.csv")
    md = B.load("02_references/reference_metadata.csv")
    sep = B.load("02_references/reference_separation.csv")

    rp = rp.merge(md[["pdb_id", "receptor", "is_panel"]],
                  on=["pdb_id", "receptor"], how="left")
    rp["is_panel"] = rp["is_panel"].fillna(False)

    fig = plt.figure(figsize=(fs.W2, 78 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.75, 0.85, 1.05])
    axb = fig.add_subplot(gs[0, 0])
    axc = fig.add_subplot(gs[0, 1])
    axd = fig.add_subplot(gs[0, 2])

    # ---- b: the predicate plane -------------------------------------------
    counts = fp.predicate_plane(
        axb, rp, "d_tilt_ref", "d_npxxy_oh_ref", group="state",
        colours=fs.STATE_COLOURS, xthr=B.THR_TILT, ythr=B.THR_NPXXY,
        marker_col="deviation_class", marker_order=fs.DEVIATION_ORDER,
        marker_shapes=fs.DEVIATION_MARKERS,
        marker_colours=fs.DEVIATION_COLOURS,
        label_col="receptor", open_col="is_panel",
        xlabel=u"TM6 tilt, 2×46–6×37 Cα (Å)",
        ylabel=u"NPxxY-OH, Y5.58–Y7.53 (Å)",
        rug_label="NPxxY axis undefined")
    # Room on the right for the two legends. The axis is EXTENDED, never
    # truncated: no datum is pushed out of view.
    x0, x1 = axb.get_xlim()
    axb.set_xlim(x0, x0 + (x1 - x0) * 1.60)
    axb.set_title("reference predicate plane", fontsize=6.5)
    state_leg = axb.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0),
                           fontsize=5, handletextpad=0.3, borderpad=0.2,
                           title="deposited label (drawn of total)",
                           title_fontsize=5)
    axb.add_artist(state_leg)
    axb.annotate(u"active predicate:  tilt > %.2f Å\nAND NPxxY-OH < %.2f Å"
                 % (B.THR_TILT, B.THR_NPXXY),
                 xy=(0.995, 0.44), xycoords="axes fraction", va="top",
                 ha="right", fontsize=5, color=fs.GREY)
    axb.annotate("filled = on the 48-receptor panel\nopen = off-panel reference",
                 xy=(0.995, 0.34), xycoords="axes fraction", va="top",
                 ha="right", fontsize=4.5, color=fs.GREY)
    fs.panel_label(axb, "b", dx=-0.20)

    # deviation legend, drawn separately so shape and colour stay paired
    import matplotlib.lines as mlines
    dev_handles = [
        mlines.Line2D([], [], lw=0, marker=fs.DEVIATION_MARKERS[k],
                      markerfacecolor="none",
                      markeredgecolor=fs.DEVIATION_COLOURS[k],
                      markeredgewidth=1.0, markersize=5,
                      label="%s (%d)" % (k.replace("_", " "),
                                         counts.get("marked:" + k, 0)))
        for k in fs.DEVIATION_ORDER]
    axb.legend(handles=dev_handles, loc="upper right",
               bbox_to_anchor=(1.0, 0.83), fontsize=4.5,
               title="deviates from its own deposited label (9 of 168)",
               title_fontsize=4.5, handletextpad=0.3, borderpad=0.2,
               labelspacing=0.25)

    # ---- c: the dynamic range of each axis --------------------------------
    long = []
    for col, axis, thr_note in (("delta_tilt_ref", "tilt", None),
                                ("delta_npxxy_ref", "NPxxY-OH", None)):
        v = sep[col].dropna()
        long.append(np_frame(axis, v.values))
    import pandas as pd
    longdf = pd.concat(long, ignore_index=True)
    fp.strip_violin(axc, longdf, "axis", "gap",
                    order=["tilt", "NPxxY-OH"],
                    colours={"tilt": fs.BLUE, "NPxxY-OH": fs.VERM})
    axc.axhline(0, color=fs.GREY, lw=0.5, zorder=0)
    axc.set_ylabel(u"reference gap, active − inactive (Å)")
    axc.set_xlabel("")
    for i, (axis, col) in enumerate((("tilt", "delta_tilt_ref"),
                                     ("NPxxY-OH", "delta_npxxy_ref"))):
        v = sep[col].dropna()
        axc.text(i, axc.get_ylim()[1], "SD %.2f" % v.std(ddof=1),
                 ha="center", va="top", fontsize=5.5, color=fs.BLACK)
    axc.set_title("dynamic range per receptor", fontsize=6.5)
    fs.panel_label(axc, "c", dx=-0.28)

    # ---- d: the census of predicate calls ---------------------------------
    order = ["expected_pass", "expected_fail", "missing_axis",
             "active_fails_predicate", "inactive_passes_predicate"]
    vc = rp["predicate_call"].value_counts()
    labels = [o.replace("_", " ") for o in order]
    vals = [int(vc.get(o, 0)) for o in order]
    fp.count_dots(axd, labels, vals, total=len(rp),
                  order_by_count=True, label_gap=0.035,
                  highlight={"active fails predicate",
                             "inactive passes predicate"})
    axd.set_xlabel("reference structures (of %d)" % len(rp))
    axd.set_title("predicate call on known-state references", fontsize=6.5)
    fs.panel_label(axd, "d", dx=-0.55)

    paths = fs.save(fig, "ba1_reference_landscape")

    n_dev = int(rp["deviation"].sum())
    n_dev_panel = int((rp["deviation"] & rp["is_panel"].astype(bool)).sum())
    print("BA-1b/c/d ->", paths[0])
    print("  references drawn        : %d (panel PDBs %d, off-panel %d)"
          % (len(rp), int(rp.is_panel.astype(bool).sum()),
             int((~rp.is_panel.astype(bool)).sum())))
    print("  both axes measurable    : %d ; NPxxY undefined (rug): %d"
          % (counts["_plotted"], counts.get("_rug", 0)))
    print("  deviations              : %d total, %d on panel PDBs"
          % (n_dev, n_dev_panel))
    print("  deviation classes       : %s"
          % rp.loc[rp.deviation, "deviation_class"].value_counts().to_dict())
    print("  panel-only classes      : %s"
          % rp.loc[rp.deviation & rp.is_panel.astype(bool),
                   "deviation_class"].value_counts().to_dict())
    print("  gap SD tilt / NPxxY     : %.3f (n=%d) / %.3f (n=%d)"
          % (sep.delta_tilt_ref.std(ddof=1), sep.delta_tilt_ref.notna().sum(),
             sep.delta_npxxy_ref.std(ddof=1),
             sep.delta_npxxy_ref.notna().sum()))
    print("  predicate calls         : %s" % dict(zip(order, vals)))
    return paths


def np_frame(axis, values):
    import pandas as pd
    return pd.DataFrame({"axis": [axis] * len(values), "gap": values})


if __name__ == "__main__":
    main()
