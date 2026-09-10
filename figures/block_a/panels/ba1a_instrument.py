"""
BA-1a - the instrument: two measurements, two views, and where the two
structures it is drawn on sit among all 168 deposited references.

The predicate is a rule over two distances and nothing else. This figure shows
those two distances being taken, on structures whose state is already known -
ADRB2's panel ACTIVE reference 4LDE over its INACTIVE reference 2RH1 - and
then shows both references' values against every other reference in the drop,
so the render is not a hand-picked pair standing on its own.

Why two views rather than one. The two measures do not lie in one plane: the
NPxxY OH-OH pair is in the receptor core and reads side-on, the 2x46 / 6x37
tilt pair is a cytoplasmic measurement and reads from below. Drawing both on
one view puts one of them end-on, and an end-on distance is a dot. It is also
what the corpus does - side view plus a cytoplasmic view rotated 90 degrees is
the commonest pairing in the render survey - and it is what the depth-of-field
constraint requires: rather than blur a measure that cannot be brought into
the focal plane with the others, use a second view.

Each render's blur encodes DEPTH ONLY and carries no interpretive meaning.

Panels c and d are the quantitative panel the renders are not allowed to be
without: 58 of the corpus's 232 structure renders carry a claim with nothing
behind it.
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

PDB_ACTIVE = "4LDE"
PDB_INACTIVE = "2RH1"


def _axis_strip(ax, rp, col, thr, rule, label, letter, marked):
    """One predicate axis over every reference that carries it.

    Two measures never share an axis - that is a recorded corpus defect and
    the reason this is two panels rather than one. Points are a jittered strip
    rather than a bar: the spread is the whole content, and 9 references
    disagree with their own deposited label.
    """
    v = rp[[col, "state"]].dropna()
    rng = np.random.RandomState(3)
    ticks = []
    for i, (state, colour) in enumerate((("inactive", fs.BLUE),
                                         ("active", fs.VERM))):
        sub = v[v["state"] == state][col].values
        ax.scatter(np.full(len(sub), i) + rng.uniform(-0.17, 0.17, len(sub)),
                   sub, s=6, color=colour, alpha=0.45, linewidths=0, zorder=2)
        ax.plot([i - 0.3, i + 0.3], [np.median(sub)] * 2, color=colour,
                lw=1.3, zorder=3, solid_capstyle="butt")
        # n goes in the tick label, not as a floating annotation: a mark
        # without its n is a corpus defect, and a floating one lands on the
        # threshold caption.
        ticks.append(u"%s\nn=%d" % (state, len(sub)))
    ax.axhline(thr, color=fs.GREY, lw=0.7, ls=(0, (2.5, 2)), zorder=1)
    for x, pdb, value, colour in marked:
        ax.scatter([x], [value], s=42, facecolors="none", edgecolors=fs.BLACK,
                   linewidths=1.0, zorder=5)
        ax.annotate(u"%s\n%.3f Å" % (pdb, value), (x, value), xytext=(7, 0),
                    textcoords="offset points", fontsize=5.0, va="center",
                    ha="left", linespacing=1.25)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(ticks)
    ax.set_xlim(-0.6, 1.9)
    ax.set_ylabel(label)
    ax.set_title(u"%s   %s over all deposited references"
                 % (letter, label.split(",")[0]), fontsize=7, loc="left",
                 fontweight="bold")
    ax.text(0.5, 1.005, u"threshold %.3f Å · active = %s it" % (thr, rule),
            transform=ax.transAxes, ha="center", va="bottom", fontsize=5,
            color=fs.GREY)


def main():
    fs.use_house_style()

    rp = B.load("02_references/reference_predicates.csv")
    adrb2 = rp[rp["receptor"] == "ADRB2"].set_index("pdb_id")

    # constrained_layout OFF: the render crops are computed from the cells'
    # real aspect, which needs the geometry fixed before anything is drawn.
    fig = plt.figure(figsize=(fs.W2, 100 * fs.MM))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.06, 1.06, 0.78],
                          left=0.035, right=0.985, top=0.905, bottom=0.275,
                          wspace=0.38, hspace=0.75)

    axa = fig.add_subplot(gs[:, 0])
    ia = scenes.ba1a_side(axa, aspect=dof.cell_aspect(fig, gs, slice(0, 2), 0))
    axa.set_title(u"a   side view — the NPxxY measurement", fontsize=7,
                  loc="left", fontweight="bold", pad=3.0)

    axb = fig.add_subplot(gs[:, 1])
    ib = scenes.ba1a_cyto(axb, aspect=dof.cell_aspect(fig, gs, slice(0, 2), 1))
    axb.set_title(u"b   from the cytoplasm — the TM6 tilt measurement",
                  fontsize=7, loc="left", fontweight="bold", pad=3.0)

    axc = fig.add_subplot(gs[0, 2])
    _axis_strip(axc, rp, "d_tilt_ref", B.THR_TILT, "above",
                u"TM6 tilt, 2×46 Cα – 6×37 Cα (Å)", "c",
                [(1, PDB_ACTIVE, ia["a_tilt"], fs.VERM),
                 (0, PDB_INACTIVE, ia["i_tilt"], fs.BLUE)])

    axd = fig.add_subplot(gs[1, 2])
    _axis_strip(axd, rp, "d_npxxy_oh_ref", B.THR_NPXXY, "below",
                u"NPxxY, Y5.58 OH – Y7.53 OH (Å)", "d",
                [(1, PDB_ACTIVE, ia["a_npxxy"], fs.VERM),
                 (0, PDB_INACTIVE, ia["i_npxxy"], fs.BLUE)])

    n_tilt = int(rp["d_tilt_ref"].notna().sum())
    n_npxxy = int(rp["d_npxxy_oh_ref"].notna().sum())
    fig.text(0.035, 0.175,
             u"a, b: ADRB2 REFERENCE structures, not predictions — 4LDE, the "
             u"receptor's panel active reference, over 2RH1, the inactive one "
             u"11_structures ships; selected from 2 because ADRB2 has one "
             u"active and three inactive\npanel references. Superposed on "
             u"receptor Cα %d–%d against %d–%d (%d shared pairs, %.2f Å); "
             u"4LDE carries a +1000 auth-numbering offset and 2RH1's T4 "
             u"lysozyme occupies 1002–1161 of the same chain, so the two\n"
             u"selections are written separately. All four values reproduce "
             u"reference_predicates.csv exactly from the deposited "
             u"coordinates, and each is drawn with the atom pair it was "
             u"measured between; the tilt anchors are L75/L275, not the\n"
             u"L124/F282 that instrument_schematic/ALIGNMENT.md names (those "
             u"measure 9.03 Å on 2RH1). Grey is the invariant bundle; colour "
             u"is TM6 only. THE SOFT FOCUS ENCODES DEPTH ONLY and carries no "
             u"interpretive meaning — the\nfocal plane sits behind TM6 and all "
             u"four anchor residues in both views (%.0f%% and %.0f%% of each "
             u"panel's depth range is behind it), so no part of the claim is "
             u"blurred. c, d: all %d references carrying the tilt axis and "
             u"all %d\ncarrying NPxxY, by deposited state, with 4LDE and 2RH1 "
             u"ringed. No excl_* flag applies: those are row-level flags on "
             u"predictions, and this figure contains none."
             % (1029, 1342, 29, 342, ia["n_ca"], ia["rmsd"],
                100 * ia["behind_focus"], 100 * ib["behind_focus"],
                n_tilt, n_npxxy),
             fontsize=4.6, color=fs.GREY, ha="left", va="top",
             linespacing=1.5)

    dof.raster_dpi(fig)
    paths = fs.save(fig, "ba1a_instrument")
    print("BA-1a written:", *paths, sep="\n  ")
    print("  a: %s; %.0f%% behind focus" % (ia["view"], 100 * ia["behind_focus"]))
    print("  b: %s; %.0f%% behind focus" % (ib["view"], 100 * ib["behind_focus"]))
    print("  4LDE %.4f / %.4f   2RH1 %.4f / %.4f"
          % (ia["a_tilt"], ia["a_npxxy"], ia["i_tilt"], ia["i_npxxy"]))
    print("  references with tilt %d, with NPxxY %d" % (n_tilt, n_npxxy))
    print("  adrb2 rows:", list(adrb2.index))


if __name__ == "__main__":
    main()
