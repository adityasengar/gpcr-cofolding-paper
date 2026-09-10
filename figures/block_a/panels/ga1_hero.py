"""
GA-1 - the graphical abstract: one co-input, one state change.

ONE COMPOSITION, NOT A GRID. This was five lettered panels with sub-captions
and it read as a figure, because that is what lettered panels with
sub-captions are. A graphical abstract is one image carrying one idea,
legible at thumbnail size and read left to right rather than parsed panel by
panel; the two explicit graphical abstracts in the 78-paper corpus are both
single left-to-right compositions. So: no panel letters anywhere, three scenes
that read as one sentence, and a single thin strip beneath them.

    LEFT     the receptor predicted from sequence alone. TM6 closed.
    CENTRE   the co-input arriving - the alpha5 C-terminal 21-mer in the
             intracellular cavity. Labelled with what was SUPPLIED.
    RIGHT    the same models with the partner. TM6 open. The SAME atom pair,
             so the two numbers can be subtracted by eye.
    BENEATH  every Class A prediction on that one axis, apo against cognate,
             with both rendered rows marked. Visually subordinate: it is the
             footing, not a panel. Without it the composition is two
             hand-picked pictures, which is the commonest defect in the
             corpus's 232 structure renders.

NO ARROW. Not between left and right, not anywhere. An arrow labelled
"activation" is the field's characteristic failure on exactly this claim, and
an unlabelled one is read as magnitude - which is BA-4, and BA-4 is negative
on three of four backbones. The centre scene is the connector and it is
labelled with the input, not the outcome; a green "+" carries the addition
without asserting a direction of change.

THE SAME ATOM PAIR ON BOTH, printed once. 2x46 Ca - 6x37 Ca is stated large
under the composition and each render carries only its own two residue names.
That keeps the strings short enough to survive reduction to 8 cm, and it is
the strongest available statement that it IS one pair: `hilger2020gcgr`
reports one displacement as 17.4 A and 18 A at two different residues in two
panels and never reconciles them.

WHAT IS NOT IN THE FRAME. Selection rules, percentiles and cell sizes are in
the LaTeX caption instead - `caption_block()` below prints the exact text and
it is duplicated in FIGURE_PROVENANCE.md. They are load-bearing and they are
not what a TOC thumbnail is for. What stays in frame is one footnote line:
what the composition shows, what it does not, and that the soft focus encodes
depth only.

DIFFERENT RECEPTORS, and the figure says so. `11_structures/` ships four
prediction CIFs: one apo (AA2AR) and three cognate (DRD2, and the two ACM1
rows of the broken/healthy pair). No receptor has both arms, so left and
right cannot be the same receptor. The strip beneath is what carries the
within-panel contrast.

Geometry is fixed and `constrained_layout` is off: the render crops are
computed from the cells' real aspect (`dofrender.cell_aspect`), which has to
happen before anything is drawn.

Sizes are chosen for a 150 mm figure that stays legible reduced to 80 mm.
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

C_APO = "#6E6E6E"
C_COG = fs.GREEN          # green means "the cognate Ga co-input" throughout
                          # this figure - the arm in the strip and the a5
                          # helix in the renders are the same thing
C_HEAD = "#1A1A1A"


def _density(values, lo, hi, n=320, sigma_bins=7):
    """Smoothed histogram. Deterministic, no bandwidth chosen by eye."""
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    edges = np.linspace(lo, hi, n + 1)
    h, _ = np.histogram(v, bins=edges)
    k = np.exp(-0.5 * (np.arange(-4 * sigma_bins, 4 * sigma_bins + 1)
                       / float(sigma_bins)) ** 2)
    k = k / k.sum()
    y = np.convolve(h.astype(float), k, mode="same")
    x = 0.5 * (edges[:-1] + edges[1:])
    return x, y, len(v)


def _strip(ax, cA, marks, xlo, xhi):
    """The footing: one axis, two distributions, both rendered rows marked.

    No axis furniture beyond the scale itself - no y axis, no box, no grid.
    It has to read as a ruler under the composition rather than as a fifth
    panel, and a graphical abstract that makes the reader parse a second set
    of axes has stopped being one image.
    """
    peak = 0.0
    for arm, colour, label in (("apo", C_APO, u"apo — sequence alone"),
                               ("cognate", C_COG, u"+ cognate Gα")):
        x, y, n = _density(cA[cA["arm"] == arm][XCOL], xlo, xhi)
        peak = max(peak, y.max())
        ax.fill_between(x, 0, y, color=colour, alpha=0.30, linewidth=0,
                        zorder=2)
        ax.plot(x, y, color=colour, lw=1.0, zorder=3)
        j = int(np.argmax(y))
        ax.annotate(u"%s   n=%s" % (label, "{:,}".format(n)),
                    (x[j], y[j]), xytext=(0, 1.5),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=6.8, color=colour, fontweight="bold", zorder=6)
    ax.axvline(B.THR_TILT, color="#9A9A9A", lw=0.6, ls=(0, (2.5, 2)),
               zorder=1)
    ax.annotate(u"predicate threshold %.3f Å" % B.THR_TILT,
                (B.THR_TILT, peak * 1.08), xytext=(-3, 0),
                textcoords="offset points", ha="right", va="top",
                fontsize=5.4, color="#8A8A8A", zorder=6)
    for value, colour, tag in marks:
        ax.plot([value, value], [-peak * 0.30, peak * 0.30], color=colour,
                lw=1.3, solid_capstyle="butt", zorder=7)
        ax.annotate(tag, (value, -peak * 0.33), xytext=(0, -1),
                    textcoords="offset points", ha="center", va="top",
                    fontsize=6.4, color=colour, fontweight="bold", zorder=7)
    ax.set_xlim(xlo, xhi)
    ax.set_ylim(-peak * 0.78, peak * 1.22)
    ax.set_yticks([])
    ax.tick_params(axis="x", labelsize=6.2, length=2.0, width=0.5, pad=1.5)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.spines["bottom"].set_position(("data", -peak * 0.78))


def caption_block(ia, ir, n_apo, n_cog, n_total):
    """The material that came OUT of the frame and MUST go into the caption.

    A selection rule that exists only in a script is the corpus's commonest
    render defect wearing a different hat - 59 of 232 rows are a hand-picked
    example with the rule unstated. It is out of the picture because a TOC
    thumbnail is not where it belongs, not because it stopped mattering.
    """
    return u"""GA-1 CAPTION - REQUIRED CONTENT, do not drop any line.

A 21-residue Ga alpha5 C-terminal co-input drives the predicted receptor into
the active state. Left: adenosine A2A (AA2AR) predicted by Boltz-2 from
sequence alone; TM6 closed, 2x46 Ca - 6x37 Ca = %.2f A. Centre: the cognate
Ga supplied as a co-input, with its alpha5 C-terminal 21 residues (Ga
334-354) seated in the intracellular cavity. Right: dopamine D2 (DRD2)
predicted by OpenFold-3 with the cognate Ga supplied; TM6 open, the same atom
pair = %.2f A. Grey is the invariant receptor, drawn as a depth-weighted
heavy-atom density; colour is TM6 and the alpha5 21-mer only. Soft focus
encodes depth only and carries no interpretive meaning.

LEFT AND RIGHT ARE DIFFERENT RECEPTORS. 11_structures/ ships one apo
prediction and three cognate ones and no receptor has both arms, so the
within-condition contrast is the strip beneath, not the two renders.

SELECTION RULES. Left: AA2AR x Boltz-2 x apo cell, n = 25 seeds; the row with
the highest plddt_mean in the cell (73.93; cell median 72.04), i.e. the 100th
percentile on confidence. It sits 0.95 A from AA2AR's INACTIVE reference and
the predicate calls it inactive, which is where an apo prediction belongs;
the directory name 'confidently_wrong' is wrong (DISCREPANCY_REPORT D12).
Right: DRD2 x OpenFold-3 x cognate cell, n = 25 seeds; the row with the
MEDIAN rmsd_to_active_ref in the cell (1.218 A shipped; rank 13 of 25, cell
range 1.020-1.507 A) - a typical row of its cell, not a best case. All 25
seeds of that cell are called active.

BOTH ANCHOR PAIRS WERE VERIFIED against the tidy data from the coordinates
drawn: Leu48 / Leu235 reproduces AA2AR row 567's stored
d_gpcrdb_tm6_tilt_246_637_ca = 11.7347 A, and Leu76 / Leu375 reproduces DRD2
row 8285's 17.2766 A. Four of the drop's ALIGNMENT.md files name residues
that do not reproduce the shipped distances (D13, D20).

STRIP. All Class A predictions under E1+E2 (broken cell, impossible
geometry): %s apo and %s cognate rows of %s total, smoothed on the tilt axis,
with the two rendered rows marked. Block A's cognate arm supplies the FULL
cognate Ga subunit; only its alpha5 C-terminal 21 residues are drawn, because
the heterotrimer is an input this figure is not reporting.

WHAT THIS FIGURE DOES NOT SHOW: amplitude reproduction - whether a receptor
with further to travel travels further - which is BA-4 and is negative on
three of four backbones. There is no arrow anywhere in the composition for
that reason.""" % (ia["d_tilt"], ir["d_tilt"],
                   "{:,}".format(n_apo), "{:,}".format(n_cog),
                   "{:,}".format(n_total))


def main():
    fs.use_house_style()

    rows = B.rows()
    core, label, n_core = B.core(rows)
    cA = core[core["gpcr_class"] == "A"].copy()

    # The vertical budget is tight and every number in it is doing work. The
    # render cells have to come out NARROWER than they are tall or the crop
    # rule pads a tall 7TM bundle out to a square frame and a third of each
    # cell is empty ground - which is what the first two attempts did. 37 mm
    # wide by 49.5 mm tall is close to the bundles' own aspect.
    # 130 x 76 mm, so a reduction to the 80 mm a TOC entry gets is only
    # x0.62 and the load-bearing type - the two values and the three headings
    # - stays above 5 pt. Drawing this at full double-column width and letting
    # the journal shrink it by 2.25x puts every label under 4 pt.
    fig = plt.figure(figsize=(130 * fs.MM, 76 * fs.MM))
    gs = fig.add_gridspec(1, 3, left=0.025, right=0.975,
                          top=0.895, bottom=0.369, wspace=0.43)
    aspect = dof.cell_aspect(fig, gs, 0, 0)

    axl = fig.add_subplot(gs[0, 0])
    ia = scenes.ga_left(axl, aspect=aspect)
    axc = fig.add_subplot(gs[0, 1])
    ic = scenes.ga_centre(axc, aspect=aspect)
    axr = fig.add_subplot(gs[0, 2])
    ir = scenes.ga_right(axr, aspect=aspect)

    # --- the three headings, read as one sentence left to right ----------
    # Both lines sit OUTSIDE the axes. Putting the second one inside, at the
    # top of the frame, is what the first version did and it landed on TM6.
    for ax, head, sub, colour in (
            (axl, u"no co-input — sequence alone",
             u"AA2AR · Boltz-2", C_HEAD),
            (axc, u"+ cognate Gα supplied",
             u"α5 C-terminal 21-mer · Gα 334–354", C_COG),
            (axr, u"with the co-input",
             u"DRD2 · OpenFold-3", C_HEAD)):
        ax.text(0.5, 1.105, head, transform=ax.transAxes, ha="center",
                va="bottom", fontsize=9.5, fontweight="bold", color=colour)
        ax.text(0.5, 1.020, sub, transform=ax.transAxes, ha="center",
                va="bottom", fontsize=6.5, color=colour)

    # A "+" between the receptor and the thing added to it, and NOTHING
    # between the co-input and the outcome. No arrow, and no "=" either: left
    # and right are different receptors, so an equation would be literally
    # false. The headings carry the reading order.
    fig.text(0.327, 0.632, u"+", ha="center", va="center", fontsize=16,
             color=C_COG, fontweight="bold")

    # --- the one measurement, named once, shared by both renders ---------
    fig.text(0.5, 0.362, u"TM6 tilt · 2×46 Cα – 6×37 Cα · "
                         u"the same atom pair on both",
             ha="center", va="top", fontsize=7.8, color=C_HEAD,
             fontweight="bold")

    # --- the footing -----------------------------------------------------
    axs = fig.add_axes([0.070, 0.212, 0.865, 0.092])
    _strip(axs, cA,
           [(ia["d_tilt"], fs.BLUE, u"%.2f Å" % ia["d_tilt"]),
            (ir["d_tilt"], fs.VERM, u"%.2f Å" % ir["d_tilt"])],
           10.3, 20.0)
    axs.set_xlabel(u"TM6 tilt (Å) — every Class A prediction, both arms",
                   fontsize=6.8, labelpad=1.0)

    n_apo = int((cA["arm"] == "apo").sum())
    n_cog = int((cA["arm"] == "cognate").sum())

    # WRAPPED BY HAND, and it has to stay wrapped. `savefig.bbox` is "tight":
    # a single line wider than the figure silently expands the canvas to fit
    # it, and everything else is then squeezed into the left two-thirds. That
    # is what the first version of this composition did.
    fig.text(0.5, 0.014,
             u"Shows the state REACHED when a Gα co-input is supplied. Does "
             u"NOT show amplitude reproduction (BA-4, negative on 3 of 4 "
             u"backbones).\nSoft focus encodes depth only and carries no "
             u"interpretive meaning. Left and right are different receptors — "
             u"the archive ships one prediction per case, so the\nstrip, not "
             u"the two renders, is the within-condition contrast. Selection "
             u"rules, cell sizes and percentiles are in the caption.",
             ha="center", va="bottom", fontsize=5.2, color="#7A7A7A",
             linespacing=1.5)

    dof.raster_dpi(fig)
    paths = fs.save(fig, "ga1_hero")
    print("GA-1 written:", *paths, sep="\n  ")
    print("  left  %.4f A (row 567) · %s · %.0f%% behind focus"
          % (ia["d_tilt"], ia["view"], 100 * ia["behind_focus"]))
    print("  right %.4f A (row 8285) · %s · %.0f%% behind focus"
          % (ir["d_tilt"], ir["view"], 100 * ir["behind_focus"]))
    print("  centre %s · %.0f%% behind focus"
          % (ic["view"], 100 * ic["behind_focus"]))
    print("  strip: %d apo / %d cognate Class A rows of %d"
          % (n_apo, n_cog, len(rows)))
    print("\n" + caption_block(ia, ir, n_apo, n_cog, len(rows)))


if __name__ == "__main__":
    main()
