"""
GA style 1 - PIPELINE SCHEMATIC. A candidate graphical abstract.

WHY THIS FORM. The corpus's Nature Communications graphical abstracts are 4 of
4 pipeline diagrams, and the form is safe for exactly the reason it is chosen:
a pipeline asserts what was DONE, not how large the effect was. Our headline
survives at full strength as a rate - 14.5% of apo rows and 79.6% of cognate
rows are called active - while the thing that does not survive, amplitude
reproduction (BA-4, negative on 3 of 4 backbones), is not a quantity a pipeline
has any slot for. A left-to-right "before / after" composition has such a slot
whether or not it is filled: two receptors side by side invite subtraction.

    1 INPUT          2 PREDICT            3 SCORE              4 CALL
    receptor seq  →  4 co-folding      →  TM6 tilt  ≥ 14.932 → called ACTIVE
    receptor seq     backbones            AND                   [render]
      + cognate Gα   25 seeds each        NPxxY-OH ≤ 9.08    → called INACTIVE
                     no template                                [render]

The two input chips CONVERGE into one process lane and the flow FORKS only at
the call. That ordering is load-bearing. If the apo lane ran along the top and
the "active" box sat at the top right, a reader would trace a straight line
from apo to active; the arms and the calls are different axes and must not be
allowed to line up. Both arms go through the same models and the same
predicate, and where they differ is inside the outcome boxes, as two rates on
one 0-100% scale.

WHAT CARRIES COLOUR. Green is the cognate Gα co-input and nothing else - the
input chip, the α5 21-mer in the render, the cognate bar in both outcome
boxes, so the eye can follow one thing across the whole width. Vermillion and
blue are the predicate's two calls and appear only on TM6 and on the outcome
headers. Everything else - scaffold, process boxes, connectors, the apo arm -
is grey. Grey means "not the subject" (RENDER_CONVENTIONS §1).

THE RENDERS ARE INSETS, NOT THE SUBJECT. Each outcome box carries one small
render pinned to that call, and beside it the rate that call fires at in each
arm. That is the corpus's second commonest render defect closed by
construction: 58 of 232 render rows have no quantitative panel standing behind
the claim the render makes. Here the quantitative panel IS the outcome box.

THE MEASUREMENT IS DEFINED ONCE AND MEASURED TWICE. The atom pairs live in the
SCORE box, where the predicate is defined - which is the pipeline form's own
answer to `hilger2020gcgr`, which prints "18 Å" and "17.4 Å" for one
displacement at two different residues and never reconciles them. Each render
then carries its own value with its own two atoms named on it, verified from
the coordinates being drawn (`cifread.verify_anchor`; four of the drop's
ALIGNMENT.md files name residues that do not reproduce the shipped distances,
D13/D20).

DIFFERENT RECEPTORS, and the figure says so. `11_structures/` ships one apo
prediction (AA2AR) and one success-case cognate prediction (DRD2); no receptor
has both arms, so the two insets cannot be one receptor. In this composition
that costs less than it does in a before/after pair, because the insets are
illustrations of a CALL rather than the two halves of a comparison - the
comparison is the bar pair, which is within-receptor-set and n = 7,966.

Selection rules, percentiles and cell sizes are in `PROV_style1.md`, not in
the frame. Geometry is fixed and `constrained_layout` is off, because the
render crops are computed from each inset axes' real aspect before anything is
drawn (`dofrender.cell_aspect` reasoning).

Sizes are for a 154 mm figure that stays readable reduced to 80 mm.

Writes: figures/out/ga_style1_pipeline.{pdf,png}
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = os.path.dirname(HERE)
FIGDIR = os.path.dirname(BLOCK)
for _p in (HERE, BLOCK, FIGDIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import badata as B                                            # noqa: E402
import cifread as CR                                          # noqa: E402
import figstyle as fs                                         # noqa: E402
import matplotlib.pyplot as plt                               # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

import dofrender as D                                         # noqa: E402
import dofscenes as S                                         # noqa: E402
import hero_renders as HR                                     # noqa: E402

# --------------------------------------------------------------------------
# palette. Three meanings, and nothing else is coloured.
# --------------------------------------------------------------------------
C_COG = fs.GREEN            # the cognate Ga co-input, everywhere it appears
C_APO = "#6E6E6E"           # the apo arm: grey, because it is the control
C_ACT = S.C_ACTIVE          # the predicate calls the row active   (vermillion)
C_INA = S.C_INACTIVE        # ... or inactive                      (blue)
C_INK = "#1A1A1A"
C_BOX = "#FAF9F7"           # process-box fill: paper, not colour
C_EDGE = "#B9B4AE"
C_FLOW = "#9C968F"          # connectors
C_MUTE = "#6F6A65"

# --------------------------------------------------------------------------
# furniture
# --------------------------------------------------------------------------
def _box(fig, x0, y0, x1, y1, fc=C_BOX, ec=C_EDGE, lw=0.6, r=0.012, z=0.3):
    """A process box. Rounded, pale, and never carrying a hue - a pipeline's
    boxes are the grammar, not the claim.

    `z` defaults BELOW an axes' zorder on purpose. matplotlib z-sorts
    figure-level artists and axes together, and an axes' default zorder is 0,
    so a box added with the usual patch default of 1 paints over any inset
    drawn inside it - which is exactly what the first build of this figure
    did: two empty outcome boxes and no renders.
    """
    p = FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                       boxstyle="round,pad=0,rounding_size=%.4f" % r,
                       transform=fig.transFigure, facecolor=fc,
                       edgecolor=ec, linewidth=lw, zorder=z)
    fig.add_artist(p)
    return p


def _arrow(fig, x0, y0, x1, y1, colour=C_FLOW, lw=1.1, z=2.0,
           rad=0.0, mut=5.0):
    """A flow connector between PROCESS boxes.

    Unlabelled, and deliberately so. An arrow in this composition means "and
    then", which is what a pipeline arrow means everywhere; the moment one
    carries a word like "activation" it is read as a magnitude, and the
    magnitude claim (BA-4) is negative on three of four backbones.
    """
    a = FancyArrowPatch((x0, y0), (x1, y1), transform=fig.transFigure,
                        arrowstyle="-|>", mutation_scale=mut,
                        connectionstyle="arc3,rad=%.3f" % rad,
                        color=colour, linewidth=lw, zorder=z,
                        shrinkA=0, shrinkB=0)
    fig.add_artist(a)
    return a


def _stage(fig, x0, y, num, title, colour=C_MUTE):
    """The stage header above a box: a numeral and three or four words."""
    fig.text(x0, y, num, ha="left", va="bottom", fontsize=7.6,
             fontweight="bold", color=colour)
    fig.text(x0 + 0.017, y, title, ha="left", va="bottom", fontsize=7.6,
             fontweight="bold", color=colour)


# --------------------------------------------------------------------------
# the two insets. Written here rather than in dofscenes.py, which other
# sessions are reading; they use only the public dofrender API plus
# dofscenes' geometry helpers, and neither module is modified.
# --------------------------------------------------------------------------
VALUE_FS = 5.8
PAIR_FS = 4.0


def _tilt_measure(ax, atoms, chain, key, frame, offset, colour=C_INK):
    """The one measurement on an inset: value, and BOTH ATOMS named.

    dofscenes' `_ga_tilt_only` prints the two residues; the hard rule is the
    atom PAIR, not the residue pair - the same two residues measured Cα-Cα and
    OH-OH give two different numbers (dofrender.measured_distance), and this
    composition prints an OH-OH threshold two boxes to the left, so leaving
    "Cα" off would be an invitation to read the wrong one.

    `offset` puts the label in the empty ground above the bundle rather than
    across it. At 16 mm wide there is one place a two-line callout can go.
    """
    a = HR.ANCHORS[key]
    t1, t2 = a["tilt"]
    n1 = CR.residue_name(atoms, chain, t1).title()
    n2 = CR.residue_name(atoms, chain, t2).title()
    x1 = CR.atom(atoms, chain, t1, "CA")
    x2 = CR.atom(atoms, chain, t2, "CA")
    p = frame.project([x1, x2])
    d = float(np.linalg.norm(x1 - x2))
    for xy in p[:, :2]:
        ax.scatter([xy[0]], [xy[1]], s=8, c=[colour], linewidths=0.4,
                   edgecolors="white", zorder=8.6)
    D.measured_distance(
        ax, p[0, :2], p[1, :2], u"%.2f Å" % d,
        u"%s%d Cα / %s%d Cα" % (n1, t1, n2, t2),
        colour, offset=offset, fontsize=VALUE_FS, pair_fontsize=PAIR_FS,
        lw=0.9)
    return d


# --------------------------------------------------------------------------
# Geometry is PREPARED for both insets before either is drawn, so that the
# two can be put on ONE SCALE.
#
# Prevents: "small multiples not on one footing", a recorded corpus camera
# defect. Two renders in one figure, each cropped to its own extent, are at
# two different Angstroms-per-millimetre; a reader comparing where TM6 sits
# in one against the other is then comparing two rulers. `frame_limits`
# frames whatever it is given, which is right for a standalone panel and
# wrong for a pair - so the half-height it would choose is computed for both
# and the LARGER is imposed on both, and a 10 A bar is drawn on each so the
# shared scale is visible rather than merely asserted.
# --------------------------------------------------------------------------
def _prep_inactive():
    """AA2AR predicted from sequence alone. TM6 closed; the predicate calls
    this row inactive, which is where an apo prediction belongs (D12)."""
    key, path, chain, lo, hi = "aa2ar", HR.AA2AR_APO, "A", 1, 316
    S._verify(path, key, "AA2AR row 567")
    atoms = CR.frame(path)
    a = HR.ANCHORS[key]
    ca = np.vstack(S._body_runs(atoms, chain, lo, hi, key))
    frame = D.camera_frame(path, (chain, lo, hi),
                           ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                           "side", ca=ca)
    return dict(key=key, path=path, chain=chain, lo=lo, hi=hi, atoms=atoms,
                frame=frame, ca=ca, pep=None, row=567, colour=C_INA,
                offset=(0.0, 16.5), name="GA-style1 inactive")


def _prep_active():
    """DRD2 predicted with the cognate Gα supplied. TM6 open, the α5 21-mer
    in the cavity; the same atom pair as the other inset."""
    key, path, chain, lo, hi = "drd2", HR.DRD2_COG, "A", 30, 443
    S._verify(path, key, "DRD2 row 8285")
    atoms = CR.frame(path)
    a = HR.ANCHORS[key]
    ca = np.vstack(S._body_runs(atoms, chain, lo, hi, key))
    frame = D.camera_frame(path, (chain, lo, hi),
                           ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                           "side", ca=ca)
    pep = np.vstack(D.ca_runs(atoms, "B", 334, 354))
    return dict(key=key, path=path, chain=chain, lo=lo, hi=hi, atoms=atoms,
                frame=frame, ca=ca, pep=pep, row=8285, colour=C_ACT,
                offset=(0.0, 15.5), name="GA-style1 active")


def _half_height(g, aspect):
    """What `frame_limits` would choose for this scene alone, in Angstrom."""
    pts = [g["frame"].project(g["ca"])[:, :2]]
    if g["pep"] is not None:
        pts.append(g["frame"].project(g["pep"])[:, :2])
    (x0, x1), (y0, y1) = D.frame_limits(pts, aspect, pad=1.04)
    return 0.5 * (y1 - y0)


def draw_inset(ax, g, aspect, half_h):
    """One inset, on the imposed scale, with its own measured distance."""
    atoms, chain, key = g["atoms"], g["chain"], g["key"]
    frame, lo, hi = g["frame"], g["lo"], g["hi"]
    a = HR.ANCHORS[key]

    P = frame.project(g["ca"])
    pts = [P[:, :2]]
    Q = None
    if g["pep"] is not None:
        Q = frame.project(g["pep"])
        pts.append(Q[:, :2])
    C = np.vstack(pts)
    cx, cy = C[:, 0].mean(), C[:, 1].mean()
    xlim = (cx - half_h * aspect, cx + half_h * aspect)
    ylim = (cy - half_h, cy + half_h)

    zs = [P[:, 2]] + ([Q[:, 2]] if Q is not None else [])
    ds = (min(z.min() for z in zs), max(z.max() for z in zs))

    tm6 = frame.project(S._tm6_run(atoms, chain, key))
    anch = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA"),
                          CR.atom(atoms, chain, a["tilt"][1], "CA")])
    claim = [tm6, anch] + ([Q] if Q is not None else [])
    focus = D.focal_plane(*claim)
    behind = D.focus_report(claim, focus, ds, g["name"])

    D.setup_axes(ax, xlim, ylim)
    S._draw_receptor(ax, frame, atoms, chain, lo, hi, key, xlim, ylim, ds,
                     focus_at=focus, trace_alpha=0.30)
    if Q is not None:
        D.blurred_layer(ax, [Q], C_COG, xlim, ylim, ds, sigma_A=1.1,
                        base_alpha=0.32, zorder=1.4)
    D.ribbon(ax, tm6, g["colour"], lw=2.6, depth_span=ds, zorder=6.0)
    if Q is not None:
        D.ribbon(ax, Q, C_COG, lw=2.8, depth_span=ds, zorder=6.6)
    d = _tilt_measure(ax, atoms, chain, key, frame, offset=g["offset"])
    D.scale_bar(ax, 10.0, colour="#6F6A65", pad=0.055, fontsize=4.0)
    return dict(row=g["row"], d_tilt=d, behind_focus=behind,
                view=frame.label,
                omitted=S._omitted(atoms, chain, lo, hi, key))

# --------------------------------------------------------------------------
# the outcome readout: two rates on one 0-100% scale
# --------------------------------------------------------------------------
def _rates(ax, rows):
    """Two bars, one per arm, on a shared 0-100% axis.

    A bar here is a PROPORTION with its numerator and denominator printed
    beside it, not a bar standing in for a distribution - the recurring plot
    defect in the corpus survey. The distribution behind the same contrast is
    BA-6/BA-7; this is a rate, and a rate is what a bar is for.
    """
    ax.set_xlim(0, 116)
    ax.set_ylim(-0.85, 1.85)
    ax.set_yticks([])
    ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.patch.set_alpha(0.0)
    for i, (label, k, n, colour) in enumerate(rows):
        y = 1.0 - i
        pct = 100.0 * k / float(n)
        ax.barh([y], [100.0], height=0.40, color="#E8E5E1", linewidth=0,
                zorder=1)
        ax.barh([y], [pct], height=0.40, color=colour, linewidth=0, zorder=2)
        ax.annotate(label, (0, y + 0.30), xytext=(0, 0),
                    textcoords="offset points", ha="left", va="bottom",
                    fontsize=5.6, color=colour, fontweight="bold")
        ax.annotate(u"%.1f%%" % pct, (102, y), ha="left", va="center",
                    fontsize=7.2, color=colour, fontweight="bold")
        ax.annotate(u"%s / %s" % ("{:,}".format(k), "{:,}".format(n)),
                    (100, y - 0.24), ha="right", va="top", fontsize=4.9,
                    color="#7A7570")
    return ax


# --------------------------------------------------------------------------
def main():
    fs.use_house_style()

    rows = B.rows()
    core, core_label, n_core = B.core(rows)
    cA = core[core["gpcr_class"] == "A"].copy()
    apo, cog = cA[cA["arm"] == "apo"], cA[cA["arm"] == "cognate"]
    n_apo, n_cog = len(apo), len(cog)
    a_act, c_act = int(apo["active"].sum()), int(cog["active"].sum())
    a_ina, c_ina = n_apo - a_act, n_cog - c_act
    n_rec = cA["receptor"].nunique()
    seeds = int(cA.groupby("cell_id").size().mode().iloc[0])

    # 154 x 70 mm. Wide enough for four stages side by side without any of
    # them being a sliver, short enough that a TOC reduction to 80 mm is only
    # x0.52 and the stage headings, the two rates and the two measured values
    # all stay above 4 pt at that size.
    #
    # EVERY BLOCK OF TEXT IS WRAPPED TO ITS BOX BY HAND. `savefig.bbox` is
    # "tight": a line wider than its box does not clip, it silently expands
    # the whole canvas and shoves the rest of the composition sideways. That
    # is what the second build of this figure did - the input chip's text ran
    # 7 mm past its own border and the canvas grew to fit it. A useful
    # arithmetic: Helvetica averages about 0.176 mm per character per point,
    # so at 5 pt a 24 mm-wide box holds 27 characters and not 30.
    fig = plt.figure(figsize=(154 * fs.MM, 76 * fs.MM))

    # ---- the budget. Fixed, and every edge is named once ----------------
    IN0, IN1 = 0.010, 0.182          # 26.5 mm
    PR0, PR1 = 0.216, 0.372          # 24.0 mm
    SC0, SC1 = 0.406, 0.582          # 27.1 mm
    OU0, OU1 = 0.616, 0.992          # 57.9 mm
    TOP, BOT = 0.915, 0.148
    MID = 0.5 * (TOP + BOT)

    # ---- 1 INPUT: two chips that CONVERGE -------------------------------
    # The arms are drawn as two chips and then merged. They must NOT run as
    # two lanes all the way to the right: if the apo lane ended level with the
    # "called ACTIVE" box the reader would trace a straight line from one to
    # the other, and arm and call are different axes.
    ia0, ia1 = 0.590, TOP
    ic0, ic1 = BOT, 0.530
    _box(fig, IN0, ia0, IN1, ia1, fc="#F7F6F4", ec="#C6C1BB")
    _box(fig, IN0, ic0, IN1, ic1, fc="#EDF7F2", ec=C_COG, lw=0.8)

    _stage(fig, IN0, TOP + 0.033, u"1", u"INPUT")
    fig.text(IN1, TOP + 0.036, u"%d Class A receptors" % n_rec,
             ha="right", va="bottom", fontsize=4.6, color=C_MUTE)

    fig.text(IN0 + 0.011, ia1 - 0.038, u"receptor sequence",
             ha="left", va="top", fontsize=6.8, fontweight="bold",
             color=C_INK)
    fig.text(IN0 + 0.011, ia1 - 0.125,
             u"apo arm — nothing\nelse supplied", ha="left", va="top",
             fontsize=5.0, color=C_MUTE, linespacing=1.35)
    fig.text(IN0 + 0.011, ia0 + 0.028, u"n = %s predictions"
             % "{:,}".format(n_apo), ha="left", va="bottom", fontsize=5.2,
             color="#3A3733", fontweight="bold")

    fig.text(IN0 + 0.011, ic1 - 0.038, u"receptor sequence",
             ha="left", va="top", fontsize=6.8, fontweight="bold",
             color=C_INK)
    fig.text(IN0 + 0.011, ic1 - 0.125, u"+ cognate Gα",
             ha="left", va="top", fontsize=6.8, fontweight="bold",
             color=C_COG)
    fig.text(IN0 + 0.011, ic1 - 0.200,
             u"cognate arm — the full Gα\nsubunit is supplied; only\n"
             u"its α5 C-terminal 21-mer\n(Gα 334–354) reaches the\ncavity",
             ha="left", va="top", fontsize=4.9, color=C_MUTE,
             linespacing=1.32)
    fig.text(IN0 + 0.011, ic0 + 0.022, u"n = %s predictions"
             % "{:,}".format(n_cog), ha="left", va="bottom", fontsize=5.2,
             color="#3A3733", fontweight="bold")

    _arrow(fig, IN1 + 0.005, 0.5 * (ia0 + ia1), PR0 - 0.005, MID + 0.055,
           rad=-0.12)
    _arrow(fig, IN1 + 0.005, 0.5 * (ic0 + ic1), PR0 - 0.005, MID - 0.055,
           rad=0.12)

    # ---- 2 PREDICT -------------------------------------------------------
    _box(fig, PR0, BOT, PR1, TOP)
    _stage(fig, PR0, TOP + 0.033, u"2", u"PREDICT")
    xm = 0.5 * (PR0 + PR1)
    fig.text(xm, TOP - 0.050, u"co-folding,\none model per seed",
             ha="center", va="top", fontsize=6.8, fontweight="bold",
             color=C_INK, linespacing=1.25)
    fig.text(xm, TOP - 0.245, u"Boltz-2\nChai-1\nOpenFold-3\nProtenix",
             ha="center", va="top", fontsize=6.4, color="#3A3733",
             linespacing=1.72)
    fig.text(xm, TOP - 0.530,
             u"%d seeds per\nreceptor × backbone × arm" % seeds,
             ha="center", va="top", fontsize=4.8, color=C_MUTE,
             linespacing=1.35)
    fig.text(xm, TOP - 0.660, u"no template supplied †",
             ha="center", va="top", fontsize=4.8, color=C_MUTE)
    fig.text(xm, BOT + 0.030, u"n = %s predictions"
             % "{:,}".format(len(cA)), ha="center", va="bottom",
             fontsize=5.2, color="#3A3733", fontweight="bold")

    _arrow(fig, PR1 + 0.005, MID, SC0 - 0.005, MID)

    # ---- 3 SCORE: where the measurement is DEFINED, once -----------------
    _box(fig, SC0, BOT, SC1, TOP)
    _stage(fig, SC0, TOP + 0.033, u"3", u"SCORE")
    xs = 0.5 * (SC0 + SC1)
    fig.text(xs, TOP - 0.050, u"state predicate\nboth axes must fire",
             ha="center", va="top", fontsize=6.8, fontweight="bold",
             color=C_INK, linespacing=1.25)

    for y, name, thr, pair in ((0.280, u"TM6 tilt", u"≥ 14.932 Å",
                                u"2×46 Cα – 6×37 Cα"),
                               (0.545, u"NPxxY", u"≤ 9.08 Å",
                                u"Tyr 5.58 OH – Tyr 7.53 OH")):
        fig.text(SC0 + 0.011, TOP - y, name, ha="left", va="center",
                 fontsize=6.2, fontweight="bold", color=C_INK)
        fig.text(SC1 - 0.011, TOP - y, thr, ha="right", va="center",
                 fontsize=6.2, fontweight="bold", color=C_INK)
        fig.text(SC0 + 0.011, TOP - y - 0.062, pair, ha="left", va="center",
                 fontsize=4.9, color=C_MUTE)

    fig.text(xs, TOP - 0.428, u"AND", ha="center", va="center",
             fontsize=6.0, fontweight="bold", color=C_MUTE)

    fig.text(xs, BOT + 0.026,
             u"one atom pair per axis,\nthe same on every row",
             ha="center", va="bottom", fontsize=4.9, color=C_MUTE,
             linespacing=1.4)

    # one predicate, two calls.
    _arrow(fig, SC1 + 0.005, MID, OU0 - 0.005, MID + 0.180, rad=-0.20)
    _arrow(fig, SC1 + 0.005, MID, OU0 - 0.005, MID - 0.180, rad=0.20)

    # ---- 4 CALL ----------------------------------------------------------
    _stage(fig, OU0, TOP + 0.033, u"4", u"CALL")
    fig.text(OU1, TOP + 0.033, u"how often the predicate fires, in each arm",
             ha="right", va="bottom", fontsize=5.0, color=C_MUTE)

    oa0, oa1 = 0.545, TOP            # called ACTIVE   (upper)
    oi0, oi1 = BOT, 0.518            # called INACTIVE (lower)
    _box(fig, OU0, oa0, OU1, oa1, fc="#FDF5F0", ec=C_ACT, lw=0.8)
    _box(fig, OU0, oi0, OU1, oi1, fc="#EFF4F9", ec=C_INA, lw=0.8)

    # PORTRAIT, not square. A 7TM bundle seen from the side is about 3 units
    # wide to 4 tall; cropping it into a square frame at this size pads a
    # third of the inset out with empty ground and shrinks the only part that
    # carries colour. 15.4 x 17.9 mm is close to the bundle's own aspect.
    RW, RH = 0.104, 0.245
    for (o0, o1), head, colour, prov in (
            ((oa0, oa1), u"called ACTIVE", C_ACT,
             u"inset: DRD2 · OpenFold-3 · cognate arm"),
            ((oi0, oi1), u"called INACTIVE", C_INA,
             u"inset: AA2AR · Boltz-2 · apo arm")):
        fig.text(OU0 + 0.012, o1 - 0.030, head, ha="left", va="top",
                 fontsize=7.4, fontweight="bold", color=colour)
        fig.text(OU1 - 0.010, o1 - 0.040, prov, ha="right", va="top",
                 fontsize=4.6, color=C_MUTE)

    # the insets: small, inside the flow, never the subject.
    ax_act = fig.add_axes([OU0 + 0.012, oa0 + 0.028, RW, RH], zorder=5)
    ax_ina = fig.add_axes([OU0 + 0.012, oi0 + 0.028, RW, RH], zorder=5)
    aspect = (RW * fig.get_figwidth()) / (RH * fig.get_figheight())
    g_act, g_ina = _prep_active(), _prep_inactive()
    half_h = max(_half_height(g_act, aspect), _half_height(g_ina, aspect))
    r_act = draw_inset(ax_act, g_act, aspect, half_h)
    r_ina = draw_inset(ax_ina, g_ina, aspect, half_h)
    for ax, colour in ((ax_act, C_ACT), (ax_ina, C_INA)):
        for s in ax.spines.values():
            s.set_visible(True)
            s.set_linewidth(0.4)
            s.set_color(colour)
            s.set_alpha(0.40)

    # the rates. THIS is the quantitative panel standing behind the two
    # renders, and it is why the renders are allowed to be one row each.
    BX = OU0 + 0.012 + RW + 0.024
    BW = OU1 - BX - 0.010
    ax_ra = fig.add_axes([BX, oa0 + 0.028, BW, RH], zorder=5)
    ax_ri = fig.add_axes([BX, oi0 + 0.028, BW, RH], zorder=5)
    _rates(ax_ra, [(u"apo", a_act, n_apo, C_APO),
                   (u"+ cognate Gα", c_act, n_cog, C_COG)])
    _rates(ax_ri, [(u"apo", a_ina, n_apo, C_APO),
                   (u"+ cognate Gα", c_ina, n_cog, C_COG)])

    # ---- the footnote. WRAPPED BY HAND ----------------------------------
    fig.text(0.5, 0.012,
             u"Rates are how often the predicate FIRES, not how far anything "
             u"moved: this composition does NOT show amplitude reproduction "
             u"(BA-4, negative on 3 of 4 backbones).\n"
             u"Soft focus encodes depth only, no interpretive meaning. Both "
             u"insets are at ONE SCALE (10 Å bars) and are DIFFERENT "
             u"RECEPTORS — the archive ships one prediction per case.\n"
             u"† templates-off is evidenced at launcher level, not per row "
             u"(D19). Population: %s; Class A. Selection rules, cell sizes "
             u"and percentiles: caption." % core_label,
             ha="center", va="bottom", fontsize=4.7, color="#7A7570",
             linespacing=1.55)

    D.raster_dpi(fig)
    paths = fs.save(fig, "ga_style1_pipeline")
    print("GA style 1 (pipeline) written:", *paths, sep="\n  ")
    print("  active   inset %.4f A (row %d) · %s · %.0f%% behind focus"
          % (r_act["d_tilt"], r_act["row"], r_act["view"],
             100 * r_act["behind_focus"]))
    print("  inactive inset %.4f A (row %d) · %s · %.0f%% behind focus"
          % (r_ina["d_tilt"], r_ina["row"], r_ina["view"],
             100 * r_ina["behind_focus"]))
    print("  %s" % r_act["omitted"])
    print("  %s" % r_ina["omitted"])
    print("  apo      %s/%s active (%.1f%%)   %s/%s inactive (%.1f%%)"
          % ("{:,}".format(a_act), "{:,}".format(n_apo),
             100.0 * a_act / n_apo, "{:,}".format(a_ina),
             "{:,}".format(n_apo), 100.0 * a_ina / n_apo))
    print("  cognate  %s/%s active (%.1f%%)   %s/%s inactive (%.1f%%)"
          % ("{:,}".format(c_act), "{:,}".format(n_cog),
             100.0 * c_act / n_cog, "{:,}".format(c_ina),
             "{:,}".format(n_cog), 100.0 * c_ina / n_cog))
    print("  population: %s; Class A n = %s of %s"
          % (core_label, "{:,}".format(len(cA)), "{:,}".format(len(rows))))


if __name__ == "__main__":
    main()

