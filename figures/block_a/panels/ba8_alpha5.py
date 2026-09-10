"""
BA-8 - the alpha5 C-terminal helix in the intracellular cavity, with the cell
it was drawn from beside it.

The render is the point of the figure and the panel beside it is the reason the
render is allowed to exist: 58 of the corpus's 232 structure renders carry a
claim with no quantitative panel behind them, and the 33 small-multiple render
grids are worse still at 32 of 33. So the DRD2 x OpenFold-3 x cognate cell is
drawn in full - all 25 seeds, both predicate axes - with the rendered row marked
on it, and the render's caption says which of the 25 it is and why.

The receptor is a depth-weighted heavy-atom DENSITY rather than a cartoon or a
PyMOL surface, because the subject is a cavity: a cartoon of a cavity reads as
a docking picture, and a semi-transparent surface renders the near and far
walls at once and fills the cavity in. Only the alpha5 C-terminal 21 residues
of the supplied Ga are drawn: the heterotrimer is not what this panel is
about, and drawing it would put an experiment in the figure that the figure is
not reporting.

The soft focus in panel a encodes DEPTH ONLY and carries no interpretive
meaning. Nothing in the 78-paper corpus uses the technique, so it gets no
benefit of the doubt: the focal plane is placed behind every state-defining
element, and the caption says what the blur means.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

import badata as B                                            # noqa: E402
import figstyle as fs                                         # noqa: E402
import matplotlib.pyplot as plt                               # noqa: E402

import dofrender as dof                                       # noqa: E402
import dofscenes as scenes                                    # noqa: E402

XCOL = "d_gpcrdb_tm6_tilt_246_637_ca"
YCOL = "d_npxxy_oh"
ROW = 8285


def main():
    fs.use_house_style()
    rows = B.rows()
    cell = rows[(rows["receptor"] == "DRD2") & (rows["backbone"] == "of3")
                & (rows["arm"] == "cognate")]
    r = cell[cell["row_id"] == ROW].iloc[0]

    # constrained_layout OFF: the render crop is computed from the cell's real
    # aspect, which needs the geometry fixed before anything is drawn.
    fig = plt.figure(figsize=(fs.W2, 96 * fs.MM))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.85, 0.90, 0.90],
                          left=0.045, right=0.995, top=0.905, bottom=0.235,
                          wspace=0.42)

    axa = fig.add_subplot(gs[0, 0])
    info = scenes.ba8_cavity(axa, aspect=dof.cell_aspect(fig, gs, 0,
                                                         slice(0, 1)))
    axa.set_title(u"a   the α5 C-terminal 21-mer in the intracellular cavity",
                  fontsize=7, loc="left", fontweight="bold", pad=3.0)

    # --- b, c: the cell the render came from, on both predicate axes ----
    for k, (col, thr, name, colour, rule) in enumerate([
            (XCOL, B.THR_TILT, u"TM6 tilt, 2×46 Cα – 6×37 Cα (Å)",
             fs.BLACK, "above"),
            (YCOL, B.THR_NPXXY, u"NPxxY, Y5.58 OH – Y7.53 OH (Å)",
             fs.PURPLE, "below")]):
        ax = fig.add_subplot(gs[0, k + 1])
        v = cell[col].dropna().values
        rng = np.random.RandomState(1)
        ax.scatter(rng.uniform(-0.16, 0.16, len(v)), v, s=9, color=colour,
                   alpha=0.5, linewidths=0, zorder=2)
        ax.plot([-0.28, 0.28], [np.median(v)] * 2, color=colour, lw=1.4,
                zorder=3, solid_capstyle="butt")
        ax.axhline(thr, color=fs.GREY, lw=0.7, ls=(0, (2.5, 2)), zorder=1)
        lo, hi = min(v.min(), thr), max(v.max(), thr)
        pad = (hi - lo) * 0.14
        ax.set_ylim(lo - pad, hi + pad * 1.6)
        ax.scatter([0], [r[col]], s=48, facecolors="none", edgecolors=fs.BLACK,
                   linewidths=1.0, zorder=5)
        ax.annotate("row 8285", (0, r[col]), xytext=(10, -6),
                    textcoords="offset points", fontsize=5.2, va="center")
        ax.text(0.97, 0.02,
                u"threshold %.3f Å\nactive = %s it" % (thr, rule),
                transform=ax.transAxes, ha="right", va="bottom", fontsize=5,
                color=fs.GREY)
        ax.set_xlim(-0.6, 0.9)
        ax.set_xticks([])
        ax.set_ylabel(name)
        ax.set_title(u"%s   %s over the cell's %d seeds"
                     % ("bc"[k], name.split(",")[0], len(v)),
                     fontsize=7, loc="left", fontweight="bold")
        ax.text(0.03, 0.955,
                u"median %.2f Å · range %.2f–%.2f\nrow 8285 = %.2f Å"
                % (np.median(v), v.min(), v.max(), r[col]),
                transform=ax.transAxes, va="top", ha="left", fontsize=5,
                color=fs.GREY)
        if k == 0:
            ax.text(0.03, 0.22,
                    u"all %d seeds are called active" % int(cell["active"].sum()),
                    transform=ax.transAxes, va="top", ha="left", fontsize=5,
                    color=fs.VERM)

    axa.text(0.0, -0.055,
             u"Selection rule: the row with the MEDIAN rmsd_to_active_ref in the "
             u"DRD2 × OpenFold-3 × cognate cell (1.218 Å; rank 13 of 25, 50th "
             u"percentile) — a typical row of its cell, not a best case.\n"
             u"No exclusion applies: neither E1 nor E2 fires anywhere in this "
             u"cell. Both anchor pairs were verified by reproducing this row's "
             u"stored 17.2766 Å and 3.9883 Å from its own coordinates, and the "
             u"3.16 Å\ncontact was measured on this model rather than taken from "
             u"a published complex. Grey is the invariant receptor; colour is "
             u"TM6 and the α5 21-mer. Every distance drawn is labelled with the "
             u"two atoms\nit was measured between. THE SOFT FOCUS ENCODES DEPTH "
             u"ONLY and carries no interpretive meaning: the focal plane sits "
             u"behind TM6, the four anchor residues and the α5, so no part of "
             u"the claim is blurred\n(%.0f%% of the panel's depth range is behind "
             u"it). %s."
             % (100 * info["behind_focus"], info["omitted"]),
             transform=axa.transAxes, fontsize=4.6, color=fs.GREY,
             ha="left", va="top", linespacing=1.5)

    dof.raster_dpi(fig)
    paths = fs.save(fig, "ba8_alpha5")
    print("BA-8 written:", *paths, sep="\n  ")
    print("  cell n=%d, active=%d, tilt med %.3f, npxxy med %.3f"
          % (len(cell), int(cell["active"].sum()),
             cell[XCOL].median(), cell[YCOL].median()))


if __name__ == "__main__":
    main()
