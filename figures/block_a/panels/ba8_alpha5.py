"""
BA-8 - the alpha5 C-terminal helix in the intracellular cavity, with the cell
it was drawn from beside it.

The render is the point of the figure and the panel beside it is the reason the
render is allowed to exist: 58 of the corpus's 232 structure renders carry a
claim with no quantitative panel behind them, and the 33 small-multiple render
grids are worse still at 32 of 33. So the DRD2 x OpenFold-3 x cognate cell is
drawn in full - all 25 seeds, both predicate axes - with the rendered row marked
on it, and the render's caption says which of the 25 it is and why.

The receptor is a surface rather than a cartoon because the subject is a cavity,
and a cartoon of a cavity reads as a docking picture. Only the alpha5 C-terminal
21 residues of the supplied Ga are drawn: the heterotrimer is not what this
panel is about, and drawing it would put an experiment in the figure that the
figure is not reporting.
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
import matplotlib.image as mpimg                              # noqa: E402

from ga1_hero import trim                                     # noqa: E402

XCOL = "d_gpcrdb_tm6_tilt_246_637_ca"
YCOL = "d_npxxy_oh"
ROW = 8285


def main():
    fs.use_house_style()
    rows = B.rows()
    cell = rows[(rows["receptor"] == "DRD2") & (rows["backbone"] == "of3")
                & (rows["arm"] == "cognate")]
    r = cell[cell["row_id"] == ROW].iloc[0]

    fig = plt.figure(figsize=(fs.W2, 104 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.75, 0.95, 0.95])

    axa = fig.add_subplot(gs[0, 0])
    axa.imshow(trim(os.path.join(B.OUT, "ba8_alpha5_cavity.png")))
    axa.axis("off")
    axa.set_title(u"a   the α5 C-terminal 21-mer in the intracellular cavity",
                  fontsize=7, loc="left", fontweight="bold")
    axa.text(0.5, -0.02,
             u"DRD2 · cognate Gα · OpenFold-3 · row 8285 · view from the "
             u"cytoplasm\nreceptor surface grey · α5 C-terminal 21 residues "
             u"(Gα 334–354) green\nblack: L76 (2×46) Cα – L375 (6×37) Cα, "
             u"17.28 Å   ·   purple: Y209 (5.58) OH – Y426 (7.53) OH, 3.99 Å\n"
             u"R132 (3.50) reaches the α5 backbone O of C351 at 3.16 Å, "
             u"measured on this model",
             transform=axa.transAxes, ha="center", va="top", fontsize=4.9,
             color=fs.GREY, linespacing=1.5)

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
            ax.text(0.03, 0.60,
                    u"all %d seeds are called active" % int(cell["active"].sum()),
                    transform=ax.transAxes, va="top", ha="left", fontsize=5,
                    color=fs.VERM)

    axa.text(0.0, -0.22,
             u"Selection rule: the row with the MEDIAN rmsd_to_active_ref in "
             u"the DRD2 × OpenFold-3 ×\ncognate cell (1.218 Å; rank 13 of 25, "
             u"50th percentile) — a typical row of its cell,\nnot a best case. "
             u"No exclusion applies: neither E1 nor E2 fires anywhere in this\n"
             u"cell. Both anchor pairs were verified by reproducing this row's "
             u"stored 17.2766 Å\nand 3.9883 Å from its own coordinates.",
             transform=axa.transAxes, fontsize=4.6, color=fs.GREY,
             ha="left", va="top", linespacing=1.5)

    paths = fs.save(fig, "ba8_alpha5")
    print("BA-8 written:", *paths, sep="\n  ")
    print("  cell n=%d, active=%d, tilt med %.3f, npxxy med %.3f"
          % (len(cell), int(cell["active"].sum()),
             cell[XCOL].median(), cell[YCOL].median()))


if __name__ == "__main__":
    main()
