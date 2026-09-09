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
import matplotlib.image as mpimg                              # noqa: E402

OUT = B.OUT
XCOL = "d_gpcrdb_tm6_tilt_246_637_ca"
YCOL = "d_npxxy_oh"

C_TILT = fs.BLACK
C_NPXXY = fs.PURPLE
C_ACTIVE = fs.VERM
C_INACTIVE = fs.BLUE
C_PEPTIDE = fs.GREEN


def trim(path, pad=6):
    """Crop the white margin PyMOL leaves, so three panels can be placed on a
    common scale instead of three different amounts of empty space."""
    im = mpimg.imread(path)
    rgb = im[..., :3] if im.ndim == 3 else im
    ink = (rgb < 0.985).any(axis=2) if rgb.ndim == 3 else (rgb < 0.985)
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if not len(rows) or not len(cols):
        return im
    r0, r1 = max(0, rows[0] - pad), min(im.shape[0], rows[-1] + pad + 1)
    c0, c1 = max(0, cols[0] - pad), min(im.shape[1], cols[-1] + pad + 1)
    return im[r0:r1, c0:c1]


def render_cell(fig, gs_img, gs_txt, png, title, subtitle, lines, letter,
                letter_dx=-0.02):
    ax = fig.add_subplot(gs_img)
    ax.imshow(trim(os.path.join(OUT, png)))
    ax.axis("off")
    ax.set_title(u"%s\n%s" % (title, subtitle), fontsize=7,
                 fontweight="bold", pad=2.0)
    fs.panel_label(ax, letter, dx=letter_dx, dy=1.16)

    axt = fig.add_subplot(gs_txt)
    axt.axis("off")
    total = sum(1 + t.count("\n") for t, _, _ in lines)
    step = 1.0 / (total + 0.6)
    y = 1.0
    for text, colour, weight in lines:
        axt.text(0.0, y, text, transform=axt.transAxes, va="top", ha="left",
                 fontsize=4.9, color=colour, fontweight=weight,
                 linespacing=1.25)
        y -= step * (1 + text.count("\n"))
    return ax


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

    fig = plt.figure(figsize=(fs.W2, 152 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(3, 6, height_ratios=[1.55, 0.62, 1.05])

    # ---------------- a: the receptor predicted alone -------------------
    render_cell(
        fig, gs[0, 0:2], gs[1, 0:2], "hero_a_apo_alone.png",
        u"receptor alone",
        u"AA2AR · apo · Boltz-2 · row 567",
        [(u"TM6 tilt  11.73 Å   L48 (2×46) Cα – L235 (6×37) Cα", C_TILT, "bold"),
         (u"NPxxY     9.61 Å   Y197 (5.58) OH – Y288 (7.53) OH", C_NPXXY, "bold"),
         (u"below the tilt threshold (14.932 Å) and above the\n"
          u"NPxxY threshold (9.080 Å): predicate calls it INACTIVE",
          C_INACTIVE, "normal"),
         (u"highest pLDDT of the 25 rows in its cell (100th pct);\n"
          u"0.95 Å from AA2AR's INACTIVE reference, 1 of 25 seeds\n"
          u"in this cell fires the predicate", fs.GREY, "normal")],
        "a", letter_dx=-0.05)

    # ---------------- b: the same models, cognate Ga supplied -----------
    render_cell(
        fig, gs[0, 2:4], gs[1, 2:4], "hero_b_cognate.png",
        u"+ cognate Gα",
        u"DRD2 · cognate · OpenFold-3 · row 8285",
        [(u"TM6 tilt  17.28 Å   L76 (2×46) Cα – L375 (6×37) Cα", C_TILT, "bold"),
         (u"NPxxY     3.99 Å   Y209 (5.58) OH – Y426 (7.53) OH", C_NPXXY, "bold"),
         (u"above the tilt threshold and below the NPxxY\n"
          u"threshold: predicate calls it ACTIVE", C_ACTIVE, "normal"),
         (u"median RMSD-to-active row of its 25-row cell (50th pct);\n"
          u"the full cognate Gα was supplied, only its α5 C-terminal\n"
          u"21 residues are drawn", fs.GREY, "normal")],
        "b")

    # ---------------- c: over the deposited active reference ------------
    render_cell(
        fig, gs[0, 4:6], gs[1, 4:6], "hero_c_over_reference.png",
        u"over the deposited active state",
        u"row 8285 on 7JVR · view from the cytoplasm",
        [(u"prediction TM6 vermillion · 7JVR TM6 grey", fs.BLACK, "normal"),
         (u"7JVR  tilt 17.59 Å · NPxxY 4.25 Å, same atom pairs", C_TILT, "bold"),
         (u"1.218 Å Cα RMSD to 7JVR over receptor residues 34–441\n"
          u"(cell range 1.020–1.507 Å over 25 seeds)", fs.GREY, "normal"),
         (u"state reached — NOT amplitude reproduction, which is\n"
          u"negative on 3 of 4 backbones (BA-4)", C_ACTIVE, "normal")],
        "c")

    # ---------------- d: the population the renders came from -----------
    axd = fig.add_subplot(gs[2, 0:4])
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
    axe = fig.add_subplot(gs[2, 4:6])
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
             u"draws the %s with both axes\nmeasurable and rugs the %d "
             u"without an NPxxY-OH value; %d Class A deposited references (%d "
             u"active,\n%d inactive) are overlaid as open marks. e: %d paired "
             u"cells, 25 seeds each. In every render grey is the\ninvariant "
             u"bundle, colour is TM6 (vermillion where the predicate fires, "
             u"blue where it does not),\ngreen is the α5 C-terminal 21-mer, "
             u"and every distance is measured on the coordinates drawn. "
             u"a and b are DIFFERENT RECEPTORS —\nthe archive ships one "
             u"prediction per case; the within-panel contrast is d and e."
             % (label, "{:,}".format(len(cA)), "{:,}".format(len(rows)),
                "{:,}".format(len(both)), len(cA) - len(both), len(ra),
                int((ra["state"] == "active").sum()),
                int((ra["state"] == "inactive").sum()), len(paired)),
             transform=axd.transAxes, fontsize=4.6, color=fs.GREY,
             ha="left", va="top", linespacing=1.4)

    paths = fs.save(fig, "ga1_hero")
    print("GA-1 written:", *paths, sep="\n  ")
    print("  plane:", counts)
    print("  paired cells: %d up / %d same / %d down" % (up, same, down))


if __name__ == "__main__":
    main()
