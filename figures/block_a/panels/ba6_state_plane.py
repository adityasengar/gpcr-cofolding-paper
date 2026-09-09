"""
BA-6 - the predicate plane, for the predictions.

BA-1b puts the 168 deposited references on the predicate plane and shows the
rule behaves on structures whose state is already known. BA-6 is the other half
of that figure: the same plane, the same two thresholds, the same axis limits,
with the 7,166 Class A predictions on it. The point a reader takes away is that
the cognate co-input does not nudge one coordinate - it moves the whole panel
diagonally across both at once, into the corner the active references occupy.

  a  the pooled plane, both arms, every observation drawn plus a density
     contour, the 69 Class A references overlaid as open anchors, and the two
     rows rendered in GA-1 ringed on their own points
  b  the same plane once per backbone, on IDENTICAL limits. Four independent
     corpus papers draw this exact plot type with per-facet axis ranges and
     per-facet colour scales; that is the defect this panel is built to avoid.
  c  the quadrant census - how many rows fire NPxxY only, tilt only, both, or
     neither. This is where the two axes are shown to agree rather than one
     carrying the result.

Population: 01_rows/block_a_rows.csv under `core` (E1+E2) restricted to Class A
(the class the predicate's two-axis form is defined for). 7,966 rows, of which
7,166 have both axes measurable and 800 have no NPxxY-OH value and are drawn as
a rug rather than dropped.

E3 is NOT applied. No reference value is a denominator or a regression
predictor anywhere in this figure - the thresholds are panel constants, not
per-receptor references.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))                     # figures/block_a
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))    # figures/

import badata as B                                            # noqa: E402
import figstyle as fs                                         # noqa: E402
import figpanels as fp                                        # noqa: E402
import matplotlib.pyplot as plt                               # noqa: E402

XCOL = "d_gpcrdb_tm6_tilt_246_637_ca"
YCOL = "d_npxxy_oh"
XLAB = u"TM6 tilt, 2×46–6×37 Cα (Å)"
YLAB = u"NPxxY, Y5.58–Y7.53 OH (Å)"

# One pair of limits for every facet in the figure. Chosen from the union of
# the predictions and the references so nothing is clipped out of frame.
XLIM = (10.3, 20.0)
YLIM = (2.0, 25.0)

ARM_ORDER = ["apo", "cognate"]

# The two rows GA-1 renders. Both verified against the CIF (see
# FIGURE_PROVENANCE.md); binding them to their own points here is what stops
# the render becoming a picture whose supporting number lives elsewhere.
RENDERED = [567, 8285]


def main():
    fs.use_house_style()

    rows = B.rows()
    core, label, n_core = B.core(rows)
    cA = core[core["gpcr_class"] == "A"].copy()
    n_class_a = len(cA)

    both = cA[cA[YCOL].notna()]
    n_both = len(both)

    refs = B.load("02_references/reference_predicates.csv")
    rmd = B.load("02_references/reference_metadata.csv")
    refs = refs.merge(rmd[["pdb_id", "receptor", "is_panel"]],
                      on=["pdb_id", "receptor"], how="left")
    ra = refs[(refs["gpcr_class"] == "A")
              & refs["d_npxxy_oh_ref"].notna()
              & refs["d_tilt_ref"].notna()].copy()
    ref_pts = ra.rename(columns={"d_tilt_ref": "x", "d_npxxy_oh_ref": "y",
                                 "state": "group"})[["x", "y", "group"]]
    # Vermillion = active, blue = inactive, exactly as in every render in
    # this figure set. The arm (grey / green) is a different variable and
    # keeps its own two colours.
    ref_style = {
        "active":   ("^", fs.VERM, "active reference"),
        "inactive": ("s", fs.BLUE, "inactive reference"),
    }

    marks = []
    for rid in RENDERED:
        r = rows[rows["row_id"] == rid]
        if len(r):
            r = r.iloc[0]
            marks.append((r[XCOL], r[YCOL],
                          "GA-1%s" % ("a" if rid == 567 else "b")))

    fig = plt.figure(figsize=(fs.W2, 148 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(3, 4, height_ratios=[1.45, 1.0, 0.62])

    # --- a: the pooled plane -------------------------------------------
    axa = fig.add_subplot(gs[0, :])
    counts = fp.density_plane(
        axa, cA, XCOL, YCOL, "arm", colours=fs.ARM_COLOURS, order=ARM_ORDER,
        xthr=B.THR_TILT, ythr=B.THR_NPXXY, xlim=XLIM, ylim=YLIM,
        xlabel=XLAB, ylabel=YLAB, refs=ref_pts, ref_style=ref_style,
        marks=marks, rug_label="no NPxxY-OH value")
    fs.panel_label(axa, "a", dx=-0.055, dy=1.10)
    axa.set_title(
        u"Class A predictions on the predicate plane — %s rows, %s with "
        u"both axes" % ("{:,}".format(n_class_a), "{:,}".format(n_both)),
        fontsize=6.5, loc="left")

    # The active corner, drawn as a box WITH ITS COORDINATES STATED. The
    # corpus's best version of this panel marks the state basins with boxes
    # whose coordinates are never given, so the state call cannot be checked
    # against the points; here the box edges ARE the two thresholds.
    axa.add_patch(plt.Rectangle(
        (B.THR_TILT, axa.get_ylim()[0]), XLIM[1] - B.THR_TILT,
        B.THR_NPXXY - axa.get_ylim()[0], facecolor=fs.GREEN, alpha=0.055,
        edgecolor="none", zorder=0))
    axa.text(B.THR_TILT + 0.12, B.THR_NPXXY - 0.35,
             u"predicate: active — tilt > %.3f Å AND NPxxY-OH < %.3f Å"
             % (B.THR_TILT, B.THR_NPXXY),
             fontsize=5.5, color=fs.GREEN, va="top", ha="left", zorder=7)

    # --- b: one facet per backbone, identical limits --------------------
    per_bb = {}
    for i, bb in enumerate(fs.BACKBONE_ORDER):
        ax = fig.add_subplot(gs[1, i])
        sub = cA[cA["backbone"] == bb]
        per_bb[bb] = fp.density_plane(
            ax, sub, XCOL, YCOL, "arm", colours=fs.ARM_COLOURS,
            order=ARM_ORDER, xthr=B.THR_TILT, ythr=B.THR_NPXXY,
            xlim=XLIM, ylim=YLIM, point_alpha=0.13, sigma=2.6,
            xlabel=XLAB, ylabel=YLAB if i == 0 else "",
            rug=False, legend=False)
        ax.set_title(fs.BACKBONE_LABELS[bb], fontsize=6.5,
                     color=fs.BACKBONE_COLOURS[bb])
        ax.text(0.03, 0.965,
                u"apo n=%d\ncognate n=%d" % (per_bb[bb].get("apo", 0),
                                             per_bb[bb].get("cognate", 0)),
                transform=ax.transAxes, va="top", ha="left", fontsize=5,
                color=fs.GREY)
        if i:
            ax.set_yticklabels([])
        if i == 0:
            fs.panel_label(ax, "b", dx=-0.30, dy=1.16)

    # --- c: the quadrant census ----------------------------------------
    axc = fig.add_subplot(gs[2, :2])
    quad_names = ["neither axis", "NPxxY only", "tilt only", "both axes"]
    quads = {}
    for arm in ARM_ORDER:
        s = both[both["arm"] == arm]
        np_a = s["npxxy_active"].astype(bool)
        ti_a = s["tilt_active"].astype(bool)
        quads[arm] = [int((~np_a & ~ti_a).sum()), int((np_a & ~ti_a).sum()),
                      int((~np_a & ti_a).sum()), int((np_a & ti_a).sum())]

    ypos = np.arange(len(quad_names))
    h = 0.36
    for k, arm in enumerate(ARM_ORDER):
        off = (k - 0.5) * h
        vals = quads[arm]
        axc.barh(ypos + off, vals, height=h * 0.92,
                 color=fs.ARM_COLOURS[arm], linewidth=0, alpha=0.9,
                 label="%s (n=%s)" % (fs.ARM_LABELS[arm],
                                      "{:,}".format(sum(vals))))
        for y, v in zip(ypos + off, vals):
            axc.text(v + n_both * 0.006, y, "{:,}".format(v), va="center",
                     ha="left", fontsize=5, color=fs.GREY)
    axc.set_yticks(ypos)
    axc.set_yticklabels(quad_names)
    axc.set_xlabel("predictions (Class A, both axes measurable)")
    axc.set_xlim(0, max(max(quads["apo"]), max(quads["cognate"])) * 1.32)
    axc.legend(loc="center right", fontsize=5.5, bbox_to_anchor=(1.0, 0.62))
    axc.spines["left"].set_visible(False)
    axc.tick_params(axis="y", length=0)
    fs.panel_label(axc, "c", dx=-0.22, dy=1.14)

    # --- the filter, printed on the figure ------------------------------
    axn = fig.add_subplot(gs[2, 2:])
    axn.axis("off")
    txt = (
        u"Filter: %s, then Class A only.\n"
        u"%s of %s rows survive E1+E2; %s of those are Class A; %s of those\n"
        u"have both axes measurable and %d have no NPxxY-OH value (rug in a).\n"
        u"Thresholds: tilt > %.3f Å, NPxxY-OH < %.3f Å — panel\n"
        u"constants, identical on every row, not per-receptor references.\n"
        u"E3 is not applied: no reference value is a denominator here.\n"
        u"References: %d Class A deposited structures with both axes\n"
        u"(%d active, %d inactive), all on the 48-receptor panel.\n\n"
        u"This plane shows the state that is REACHED. It says nothing about\n"
        u"amplitude reproduction, which is BA-4 and is negative on 3 of 4\n"
        u"backbones."
        % (label, "{:,}".format(n_core), "{:,}".format(len(rows)),
           "{:,}".format(n_class_a), "{:,}".format(n_both),
           len(cA) - n_both, B.THR_TILT, B.THR_NPXXY, len(ra),
           int((ra["state"] == "active").sum()),
           int((ra["state"] == "inactive").sum())))
    axn.text(0.0, 1.0, txt, va="top", ha="left", fontsize=5.2,
             color=fs.BLACK, linespacing=1.45)

    paths = fs.save(fig, "ba6_state_plane")
    print("BA-6 written:", *paths, sep="\n  ")
    print("\n  pooled:", counts)
    for bb in fs.BACKBONE_ORDER:
        print("  %-9s %s" % (bb, per_bb[bb]))
    print("  quadrants:", {k: dict(zip(quad_names, v))
                           for k, v in quads.items()})


if __name__ == "__main__":
    main()
