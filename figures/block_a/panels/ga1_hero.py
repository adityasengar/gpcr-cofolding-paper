"""
GA-1 - the graphical abstract: one co-input, one state change.

Three renders over two data panels, in one frame. The renders are built first
by `hero_renders.py`; this script trims and places them, prints each panel's
own measured numbers WITH the atom pair they were measured between, and puts
the population the renders were drawn from directly underneath, with both
rendered rows ringed on it.

Why it is built this way. Only 11 of the corpus's 1,226 panel-group rows put a
render and a measured quantity in the same frame, and 10 of those 11 carry a
recorded defect. The failure is always the same shape: the render is exempted
from the discipline applied to the plot beside it. The three forms recorded are
a rate badged onto a render with its denominator in another figure, a render
showing references rather than the predictions the number is about, and an
exemplar chosen after the metric was computed sitting next to an unselected
plot. So here:

  * every number printed on a render is measured on the coordinates of THAT
    file and reproduces the value stored for that row in the tidy data;
  * the two atoms it was measured between are named beside it, every time;
  * both rendered rows are ringed on panel d, so the picture and the
    population cannot drift apart;
  * each render's cell, its n, and the row's percentile within it are printed
    on the panel, not left to the caption.

How the renders are drawn. Panels a-c are vector renders built by
`dofscenes.py` on `dofrender.py`, not PyMOL bitmaps: a Gaussian-blurred
heavy-atom density carries the receptor, sharp vector sticks carry the claim.
The blur encodes DEPTH ONLY and has no interpretive meaning - it is a cue no
paper in the 78-paper corpus uses, so the caption has to say what it means,
and the focal plane is placed at the back of the state-defining elements so
that no part of the claim is ever on the blurred side of it. Emphasis is
carried by the rule this literature does use: grey for the invariant
scaffold, colour for what carries the claim.

What this figure may NOT say. It shows the state that is REACHED. It is not
evidence of amplitude reproduction - whether a receptor with further to travel
travels further - which is BA-4 and is negative on three of four backbones. So
there is no arrow, labelled or otherwise, between the panels: an arrow labelled
"activation" is the field's characteristic failure on exactly this claim, and
an unlabelled one would be read as magnitude.
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

import dofrender as dof                                       # noqa: E402
import dofscenes as scenes                                    # noqa: E402

OUT = B.OUT
XCOL = "d_gpcrdb_tm6_tilt_246_637_ca"
YCOL = "d_npxxy_oh"

C_TILT = fs.BLACK
C_NPXXY = fs.PURPLE
C_ACTIVE = fs.VERM
C_INACTIVE = fs.BLUE
C_PEPTIDE = fs.GREEN


def render_cell(fig, gs, row, cols, scene, title, subtitle):
    """One render panel: the scene draws itself, we only place and title it."""
    ax = fig.add_subplot(gs[row, cols])
    info = scene(ax, aspect=dof.cell_aspect(fig, gs, row, cols))
    # The subtitle is a separate artist so it can be smaller and greyer than
    # the title; the title pad has to clear it or the two overprint.
    ax.set_title(title, fontsize=7, fontweight="bold", loc="left", pad=11.0)
    ax.text(0.0, 1.006, subtitle, transform=ax.transAxes, ha="left",
            va="bottom", fontsize=5.4, color="#444444")
    return info


def main():
    fs.use_house_style()

    rows = B.rows()
    core, label, n_core = B.core(rows)
    cA = core[core["gpcr_class"] == "A"].copy()
    both = cA[cA[YCOL].notna()]

    r567 = rows[rows["row_id"] == 567].iloc[0]
    r8285 = rows[rows["row_id"] == 8285].iloc[0]

    refs = B.load("02_references/reference_predicates.csv")
    ra = refs[(refs["gpcr_class"] == "A") & refs["d_npxxy_oh_ref"].notna()
              & refs["d_tilt_ref"].notna()].copy()
    ref_pts = ra.rename(columns={"d_tilt_ref": "x", "d_npxxy_oh_ref": "y",
                                 "state": "group"})[["x", "y", "group"]]
    ref_style = {"active": ("^", fs.VERM, "active reference"),
                 "inactive": ("s", fs.BLUE, "inactive reference")}

    # constrained_layout is OFF here on purpose: the render crops are computed
    # from the cells' real aspect (dofrender.cell_aspect), which requires the
    # geometry to be fixed before anything is drawn.
    fig = plt.figure(figsize=(fs.W2, 150 * fs.MM))
    gs = fig.add_gridspec(2, 6, height_ratios=[1.42, 1.00],
                          left=0.045, right=0.995, top=0.935, bottom=0.135,
                          wspace=0.62, hspace=0.30)

    # ---------------- a: the receptor predicted alone -------------------
    ia = render_cell(fig, gs, 0, slice(0, 2), scenes.hero_a,
                     u"a   receptor alone",
                     u"AA2AR · apo · Boltz-2 · row 567 — predicate: INACTIVE")

    # ---------------- b: the same models, cognate Ga supplied -----------
    ib = render_cell(fig, gs, 0, slice(2, 4), scenes.hero_b,
                     u"b   + cognate Gα",
                     u"DRD2 · cognate · OpenFold-3 · row 8285 — ACTIVE")

    # ---------------- c: over the deposited active reference ------------
    ic = render_cell(fig, gs, 0, slice(4, 6), scenes.hero_c,
                     u"c   over the deposited active state",
                     u"row 8285 on 7JVR · view from the cytoplasm")

    # ---------------- d: the population the renders came from -----------
    axd = fig.add_subplot(gs[1, 0:4])
    marks = [(r567[XCOL], r567[YCOL], "a"), (r8285[XCOL], r8285[YCOL], "b")]
    counts = fp.density_plane(
        axd, cA, XCOL, YCOL, "arm", colours=fs.ARM_COLOURS,
        order=["apo", "cognate"], xthr=B.THR_TILT, ythr=B.THR_NPXXY,
        xlim=(10.3, 20.0), ylim=(2.0, 25.0),
        xlabel=u"TM6 tilt, 2×46 Cα – 6×37 Cα (Å)",
        ylabel=u"NPxxY, Y5.58 OH – Y7.53 OH (Å)",
        refs=ref_pts, ref_style=ref_style, marks=marks,
        rug_label="no NPxxY-OH value")
    axd.add_patch(plt.Rectangle(
        (B.THR_TILT, axd.get_ylim()[0]), 20.0 - B.THR_TILT,
        B.THR_NPXXY - axd.get_ylim()[0], facecolor=fs.GREEN, alpha=0.055,
        edgecolor="none", zorder=0))
    axd.text(B.THR_TILT + 0.12, B.THR_NPXXY - 0.4,
             u"predicate: active — tilt > %.3f Å AND NPxxY-OH < %.3f Å"
             % (B.THR_TILT, B.THR_NPXXY), fontsize=5.2, color=fs.GREEN,
             va="top", ha="left", zorder=7)
    axd.set_title(
        u"every Class A prediction, both arms — the rows drawn in a and b are "
        u"ringed", fontsize=6.5, loc="left")
    fs.panel_label(axd, "d", dx=-0.055, dy=1.11)

    # ---------------- e: it is a switch, and it is panel-wide -----------
    axe = fig.add_subplot(gs[1, 4:6])
    cells = (cA.groupby(["receptor", "backbone", "arm"])
             .agg(seeds=("active", "size"), fired=("active", "sum"))
             .reset_index())
    cells["frac"] = cells["fired"] / cells["seeds"]
    wide = cells.pivot_table(index=["receptor", "backbone"], columns="arm",
                             values="frac").dropna()
    paired = wide.reset_index()
    up = int((paired["cognate"] > paired["apo"]).sum())
    same = int((paired["cognate"] == paired["apo"]).sum())
    down = int((paired["cognate"] < paired["apo"]).sum())
    jit = np.random.RandomState(0).uniform(-0.016, 0.016, (len(paired), 2))
    axe.plot([0, 1], [0, 1], color=fs.GREY, lw=0.6, ls=(0, (3, 2)), zorder=1)
    axe.text(0.50, 0.465, "identity: no change", fontsize=4.8, color=fs.GREY,
             rotation=45, rotation_mode="anchor", va="top")
    for i, bb in enumerate(fs.BACKBONE_ORDER):
        m = (paired["backbone"] == bb).values
        axe.scatter(paired["apo"][m] + jit[m, 0],
                    paired["cognate"][m] + jit[m, 1], s=10,
                    color=fs.BACKBONE_COLOURS[bb], edgecolors="none",
                    alpha=0.8, zorder=3, label=fs.BACKBONE_LABELS[bb])
    axe.set_xlabel("apo: fraction of 25 seeds called active")
    axe.set_ylabel(u"cognate Gα: fraction called active")
    axe.set_xlim(-0.06, 1.06)
    axe.set_ylim(-0.06, 1.06)
    axe.legend(loc="lower right", fontsize=4.8, handlelength=0.8,
               labelspacing=0.18, borderpad=0.2)
    axe.text(0.035, 0.55,
             u"%d of %d receptor × backbone\ncells up\n%d unchanged · %d down"
             % (up, len(paired), same, down),
             transform=axe.transAxes, va="top", ha="left", fontsize=5,
             color=fs.GREY)
    axe.set_title(u"not anecdotal, and not a dial", fontsize=6.5, loc="left")
    fs.panel_label(axe, "e", dx=-0.20, dy=1.11)

    axd.text(0.0, -0.31,
             u"Filter for d and e: %s, then Class A only — %s of %s rows. d "
             u"draws the %s with both axes measurable and rugs the %d without "
             u"an NPxxY-OH value;\n%d Class A deposited references (%d active, "
             u"%d inactive) are overlaid as open marks. e: %d paired cells, 25 "
             u"seeds each. a and b are DIFFERENT\nRECEPTORS — the archive ships "
             u"one prediction per case; the within-panel contrast is d and e.\n"
             u"RENDERS a–c: grey is the invariant bundle, colour is TM6 "
             u"(vermillion where the predicate fires, blue where it does not), "
             u"green is the α5 C-terminal 21-mer.\nEvery distance drawn is "
             u"measured on the coordinates in that panel and is labelled with "
             u"the two atoms it was measured between. THE SOFT FOCUS ENCODES "
             u"DEPTH ONLY\nand carries no interpretive meaning: the focal "
             u"plane is placed behind the state-defining elements, so no part "
             u"of TM6, the four anchor residues or the α5 is ever blurred.\n"
             u"%s.\n%s."
             % (label, "{:,}".format(len(cA)), "{:,}".format(len(rows)),
                "{:,}".format(len(both)), len(cA) - len(both), len(ra),
                int((ra["state"] == "active").sum()),
                int((ra["state"] == "inactive").sum()), len(paired),
                ib["omitted"], ia["omitted"]),
             transform=axd.transAxes, fontsize=4.6, color=fs.GREY,
             ha="left", va="top", linespacing=1.4)

    dof.raster_dpi(fig)
    paths = fs.save(fig, "ga1_hero")
    print("GA-1 written:", *paths, sep="\n  ")
    print("  plane:", counts)
    for tag, info in (("a", ia), ("b", ib), ("c", ic)):
        print("  render %s: %s; %.0f%% of panel depth behind the focal plane"
              % (tag, info["view"], 100 * info["behind_focus"]))
    print("  paired cells: %d up / %d same / %d down" % (up, same, down))


if __name__ == "__main__":
    main()
