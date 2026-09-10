"""
GA style 4 - THE MEASUREMENT IS THE SPINE. A candidate graphical abstract.

THE IDEA. The organising element is the measured axis itself, drawn as a real
ruler running down the page in Angstrom. Everything hangs off it. The two
predictions are not labelled with their values - they are PLACED at them, so
the vertical distance between them on the page is 5.54 A of TM6 tilt at the
ruler's own scale, and the predicate threshold, drawn edge to edge, physically
separates them. The population sits on the same ruler as a back-to-back
density, apo to the left and cognate to the right, so the two rendered rows are
visibly drawn out of it.

What that buys, in order of importance:

  1. THE THRESHOLD AND THE SEPARATION ARE READABLE WITHOUT READING A NUMBER.
     The apo render is wholly below the threshold rule and the cognate render
     wholly above it. That is the claim, and at thumbnail size it survives when
     every string on the page has become illegible.
  2. DISHONESTY BECOMES GEOMETRICALLY IMPOSSIBLE. A structure cannot be put
     anywhere except at its measured value, because its position IS the value;
     there is no free parameter to nudge. Compare the field's habit, recorded
     in RENDER_CONVENTIONS s6: `hilger2020gcgr` prints 17.4 A and 18 A for one
     displacement in two panels and never reconciles them.
  3. ONE AXIS, ONE MEANING. `figures/README.md` lists "two measures sharing one
     axis" as a recurring plot failure. Here there is exactly one axis in the
     whole composition and everything - threshold, density, both structures -
     is on it.

THE DANGER THIS STYLE CREATES, and what is done about it. A metric axis with
two structures on it invites the reading "the models reproduce this scale".
They do not: amplitude reproduction is negative on three of four backbones
(BA-4, DISCREPANCY_REPORT D3 - the tilt slopes even go negative under
`class_a_only`). So:

  * NO ARROW and NO CALIPER between the two structures. The vertical gap is
    left unlabelled on purpose. Labelling it would turn "where two predictions
    fall" into "how far a receptor moved", which is the claim this figure is
    forbidden from making - and doubly so because the two renders are
    DIFFERENT RECEPTORS.
  * No deposited reference value is marked on the ruler. Putting 7JVR's
    17.586 A beside DRD2's 17.277 A would be a magnitude-tracking picture in
    miniature.
  * The footnote says both things in words, at the top of the footnote rather
    than buried at the end of it.

DIFFERENT RECEPTORS, said plainly. `11_structures/` ships one apo prediction
(AA2AR) and three cognate ones; no receptor has both arms, so left and right
cannot be the same receptor. This style makes that limitation MORE visible
than a side-by-side composition does, because a shared axis invites subtraction
by eye. The answer is not to hide it: each render is titled with its own
receptor, and the footnote states that the population - not the pair - carries
the within-condition contrast.

TWO SCALES ON ONE PAGE, and how they are kept apart. The ruler is 10.1 mm per
Angstrom; the renders are about 0.4 mm per Angstrom. Positions on the ruler are
at ruler scale; anything inside a render box is at render scale and carries its
own 10 A bar. The footnote says so. Nothing is measured across the boundary.

WHAT THE HEADLINE MAY NOT SAY, and this is the one that nearly shipped. Block A
supplies the FULL cognate Ga subunit as the co-input. The alpha5 C-terminal 21
residues are what is DRAWN, not what was supplied, and the two are not the same
statement: the paper's title claims a 21-residue peptide co-input, Block A does
not test it, Block B will, and CLAIMS.md carries the rule "No Block A sentence
may imply the peptide result." The first build of this figure headlined "Supply
the Ga alpha5 C-terminal 21-mer ..." - the forbidden claim, in the largest type
on the page, two inches above an annotation that said it correctly. The headline
now names the INPUT ("Supply the cognate Ga"); the colour key names the DRAWN
element ("alpha5 C-terminal 21-mer, Ga 334-354"); and the footnote states the
gap between them explicitly. Any future edit to the headline has to keep that
split.

WHAT IS DRAWN AND WHAT IS NOT. Grey is the invariant receptor bundle. Colour is
TM6 (blue where the predicate calls the row inactive, vermillion where active)
and the alpha5 C-terminal 21-mer only. The heterotrimer is never drawn: Block
A's cognate arm supplies the full Ga subunit and only Ga 334-354 is shown,
which is also what this literature does (`tejero2024opsin` Fig 5).

ANCHORS. Every distance is re-verified from the coordinates being drawn before
it is used, through `hero_renders.verify` -> `cifread.verify_anchor`, which
refuses a pair that does not reproduce the value stored for that row. Four of
the drop's ALIGNMENT.md files name residues that do not (D13, D20).

Run: python3 figures/block_a/panels/ga_style4_axis.py
Writes: figures/out/ga_style4_axis.{pdf,png}; provenance in PROV_style4.md.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = os.path.dirname(HERE)
FIGDIR = os.path.dirname(BLOCK)
for p in (HERE, BLOCK, FIGDIR):
    if p not in sys.path:
        sys.path.insert(0, p)

import matplotlib.pyplot as plt                                # noqa: E402

import badata as B                                             # noqa: E402
import cifread as CR                                           # noqa: E402
import dofrender as dof                                        # noqa: E402
import dofscenes as scenes                                     # noqa: E402
import figstyle as fs                                          # noqa: E402
import hero_renders as HR                                      # noqa: E402

# The receptor-drawing helpers, the ICL3 window rule and the anchors are
# BORROWED, not re-implemented: forking the ICL3 rule or the anchor table into
# this file would create a second place where a correctness-bearing rule lives.
# The names are private to dofscenes, so the dependency is asserted here rather
# than discovered as an AttributeError in the middle of a render.
for _n in ("_body_runs", "_body_heavy", "_tm6_run", "_draw_receptor",
           "_omitted", "C_ACTIVE", "C_INACTIVE", "C_PEPTIDE", "C_TILT"):
    if not hasattr(scenes, _n):
        raise ImportError(
            "dofscenes has no %r: this panel borrows the receptor-drawing "
            "helpers and the ICL3 rule from it rather than forking them. If "
            "that module was refactored, re-point this file at the new names "
            "instead of copying the rule." % _n)

XCOL = "d_gpcrdb_tm6_tilt_246_637_ca"

# --------------------------------------------------------------------------
# GEOMETRY. Everything is in millimetres of the final figure, because the
# whole point of this style is that a position on the page is a measured
# quantity - so the mapping from Angstrom to millimetre is stated once, at the
# top, and never re-derived.
#
# 100 x 130 mm. A TOC image is usually wanted tall, and reduction to the 80 mm
# a TOC entry gets is x0.615 on the long edge - the same factor GA-1 was built
# for, so the load-bearing type (the two values, the threshold, the headings)
# stays at or above 5 pt after reduction.
# --------------------------------------------------------------------------
FIGW, FIGH = 100.0, 130.0

VLO, VHI = 10.4, 19.9         # the ruler's range, Angstrom
YLO, YHI = 20.0, 112.0        # where VLO and VHI sit, mm from the bottom
                              # => 9.68 mm per Angstrom

RULER_X0, RULER_X1 = 47.0, 53.0          # the ruler strip itself
DENS_W = 11.5                            # how far a density may reach out
REND_W, REND_H = 30.0, 37.0              # each render box
REND_L_X = 4.0                           # left (apo) box left edge
REND_R_X = FIGW - REND_W - 4.0           # right (cognate) box left edge

C_APO = "#6E6E6E"             # the apo arm, and the apo density
C_COG = fs.GREEN              # green is the cognate Ga co-input everywhere in
                              # this paper: the arm, the density, and the a5
                              # helix in the render are the same thing
C_HEAD = "#1A1A1A"
C_RULE = "#3A3A3A"
RULER_FILL = "#EFECE8"
RULER_EDGE = "#B5AFA7"


def mm(v):
    """Angstrom on the ruler -> millimetres up the page. The one mapping."""
    return YLO + (float(v) - VLO) / (VHI - VLO) * (YHI - YLO)


# --------------------------------------------------------------------------
# the population, on the same axis
# --------------------------------------------------------------------------
def _density(values, lo, hi, n=400, sigma_bins=9):
    """Smoothed histogram on a fixed grid. No bandwidth chosen by eye."""
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    edges = np.linspace(lo, hi, n + 1)
    h, _ = np.histogram(v, bins=edges)
    k = np.exp(-0.5 * (np.arange(-4 * sigma_bins, 4 * sigma_bins + 1)
                       / float(sigma_bins)) ** 2)
    k = k / k.sum()
    y = np.convolve(h.astype(float), k, mode="same")
    return 0.5 * (edges[:-1] + edges[1:]), y, len(v)


# --------------------------------------------------------------------------
# the renders. Local, so that nothing in dofscenes/ga1_hero has to change:
# other candidates are reading those files right now.
#
# These are deliberately barer than the figure-panel scenes. No value is
# printed inside a render box - the value is the box's POSITION, read off the
# ruler - so what stays in the box is the dashed segment, the two atoms it was
# measured between, and the atom pair that names them.
# --------------------------------------------------------------------------
def _pair_dash(ax, p, q, pair_text, colour, offset, fontsize=4.6):
    """The measured segment, named by its ATOM PAIR, with no value on it.

    Prevents the corpus's mirror pair of failures at once: a magnitude drawn as
    an arrow with no number anywhere (`ye2026multistatebias` Fig 4A), and a
    number printed with no statement of which atoms it was measured between
    (`hilger2020gcgr` Fig 1B). The number is on the ruler, tied to this segment
    by a leader that starts at this box; the atoms are named here.
    """
    p, q = np.asarray(p, float), np.asarray(q, float)
    # white underlay first: a black dashed segment over a blurred grey density
    # is nearly invisible at 27 mm, which would leave the panel asserting a
    # measurement it does not show
    ax.plot([p[0], q[0]], [p[1], q[1]], color="white", lw=2.4, alpha=0.85,
            solid_capstyle="round", zorder=8.4)
    ax.plot([p[0], q[0]], [p[1], q[1]], color=colour, lw=1.1,
            ls=(0, (2.2, 1.7)), solid_capstyle="butt", zorder=8.5)
    for e in (p, q):
        ax.scatter([e[0]], [e[1]], s=9.0, c=[colour], linewidths=0.4,
                   edgecolors="white", zorder=8.7)
    mid = 0.5 * (p + q)
    ax.plot([mid[0], mid[0] + offset[0]], [mid[1], mid[1] + offset[1]],
            color=colour, lw=0.35, alpha=0.55, zorder=8.4)
    ax.annotate(pair_text, (mid[0] + offset[0], mid[1] + offset[1]),
                ha="center", va="center", fontsize=fontsize, color="#2B2B2B",
                linespacing=1.25, zorder=9.0,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.86,
                          boxstyle="round,pad=0.18"))


def _box(ax, colour="#C9C3BB"):
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_linewidth(0.5)
        s.set_color(colour)


def render_apo(ax, aspect):
    """AA2AR predicted from sequence alone. TM6 closed; predicate INACTIVE."""
    key, path, chain = "aa2ar", HR.AA2AR_APO, "A"
    dt, dn = HR.verify(path, key, "AA2AR row 567")
    atoms = CR.frame(path)
    a = HR.ANCHORS[key]
    ca = np.vstack(scenes._body_runs(atoms, chain, 1, 316, key))
    frame = dof.camera_frame(path, (chain, 1, 316),
                             ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                             "side", ca=ca)
    P = frame.project(ca)
    xlim, ylim = dof.frame_limits([P[:, :2]], aspect, pad=1.05)
    ds = (P[:, 2].min(), P[:, 2].max())

    tm6 = frame.project(scenes._tm6_run(atoms, chain, key))
    anch = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA"),
                          CR.atom(atoms, chain, a["tilt"][1], "CA")])
    focus = dof.focal_plane(tm6, anch)
    behind = dof.focus_report([tm6, anch], focus, ds, "style4 apo")

    dof.setup_axes(ax, xlim, ylim)
    scenes._draw_receptor(ax, frame, atoms, chain, 1, 316, key, xlim, ylim, ds,
                          focus_at=focus, trace_alpha=0.34)
    dof.ribbon(ax, tm6, scenes.C_INACTIVE, lw=3.0, depth_span=ds, zorder=6.0)

    names = dict((r, CR.residue_name(atoms, chain, r)) for r in a["tilt"])
    _pair_dash(ax, anch[0, :2], anch[1, :2],
               u"%s%d (2×46) Cα\n%s%d (6×37) Cα"
               % (names[a["tilt"][0]].title(), a["tilt"][0],
                  names[a["tilt"][1]].title(), a["tilt"][1]),
               scenes.C_TILT, offset=(-11.0, 8.0))
    dof.scale_bar(ax, length=10.0, fontsize=4.2, pad=0.05)
    _box(ax)
    return dict(row=567, d_tilt=dt, d_npxxy=dn, behind_focus=behind,
                view=frame.label, omitted=scenes._omitted(atoms, chain, 1, 316,
                                                          key))


def render_cognate(ax, aspect):
    """DRD2 with the cognate Ga supplied. TM6 open; predicate ACTIVE."""
    key, path, chain = "drd2", HR.DRD2_COG, "A"
    dt, dn = HR.verify(path, key, "DRD2 row 8285")
    atoms = CR.frame(path)
    a = HR.ANCHORS[key]
    ca = np.vstack(scenes._body_runs(atoms, chain, 30, 443, key))
    frame = dof.camera_frame(path, (chain, 30, 443),
                             ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                             "side", ca=ca)
    pep = np.vstack(dof.ca_runs(atoms, "B", 334, 354))
    P, Q = frame.project(ca), frame.project(pep)
    xlim, ylim = dof.frame_limits([P[:, :2], Q[:, :2]], aspect, pad=1.05)
    ds = (min(P[:, 2].min(), Q[:, 2].min()),
          max(P[:, 2].max(), Q[:, 2].max()))

    tm6 = frame.project(scenes._tm6_run(atoms, chain, key))
    anch = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA"),
                          CR.atom(atoms, chain, a["tilt"][1], "CA")])
    focus = dof.focal_plane(tm6, anch, Q)
    behind = dof.focus_report([tm6, anch, Q], focus, ds, "style4 cognate")

    dof.setup_axes(ax, xlim, ylim)
    scenes._draw_receptor(ax, frame, atoms, chain, 30, 443, key, xlim, ylim,
                          ds, focus_at=focus, trace_alpha=0.34)
    # the co-input gets its own soft glow before the sharp tube, or a 21-mer
    # disappears into a 400-residue bundle at 27 mm wide
    dof.blurred_layer(ax, [Q], scenes.C_PEPTIDE, xlim, ylim, ds, sigma_A=1.1,
                      base_alpha=0.34, zorder=1.4)
    dof.ribbon(ax, tm6, scenes.C_ACTIVE, lw=3.0, depth_span=ds, zorder=6.0)
    dof.ribbon(ax, Q, scenes.C_PEPTIDE, lw=3.4, depth_span=ds, zorder=6.6)

    names = dict((r, CR.residue_name(atoms, chain, r)) for r in a["tilt"])
    _pair_dash(ax, anch[0, :2], anch[1, :2],
               u"%s%d (2×46) Cα\n%s%d (6×37) Cα"
               % (names[a["tilt"][0]].title(), a["tilt"][0],
                  names[a["tilt"][1]].title(), a["tilt"][1]),
               scenes.C_TILT, offset=(-12.0, 8.5))
    dof.scale_bar(ax, length=10.0, fontsize=4.2, pad=0.05)
    _box(ax)
    return dict(row=8285, d_tilt=dt, d_npxxy=dn, behind_focus=behind,
                view=frame.label, omitted=scenes._omitted(atoms, chain, 30,
                                                          443, key))


# --------------------------------------------------------------------------
# the spine
# --------------------------------------------------------------------------
def draw_ruler(ax):
    """A real ruler: a strip, ticks from both edges, numbers down the middle.

    Drawn as an instrument rather than as a matplotlib axis on purpose. A
    reader who sees a ruler expects positions on it to mean something, which is
    the one thing this composition needs them to assume.
    """
    ax.add_patch(plt.Rectangle((RULER_X0, mm(VLO)), RULER_X1 - RULER_X0,
                               mm(VHI) - mm(VLO), facecolor=RULER_FILL,
                               edgecolor=RULER_EDGE, lw=0.5, zorder=2.0))
    # Ticks are anchored on the INTEGERS, not stepped from VLO. Stepping 0.5
    # from 10.4 lands on 10.9, 11.4, ... - never an integer - so the
    # major/minor test never fired and the first build shipped a ruler with no
    # numbers on it at all.
    for v in np.arange(np.ceil(VLO * 2.0) / 2.0, VHI + 1e-9, 0.5):
        y = mm(v)
        major = abs(v - round(v)) < 1e-6
        L = 1.7 if major else 0.85
        for x0, s in ((RULER_X0, +1), (RULER_X1, -1)):
            ax.plot([x0, x0 + s * L], [y, y], color="#6F6960",
                    lw=0.7 if major else 0.4, solid_capstyle="butt",
                    zorder=2.4)
        if major and VLO + 0.3 < v < VHI - 0.3:
            ax.text(0.5 * (RULER_X0 + RULER_X1), y, "%d" % round(v),
                    ha="center", va="center", fontsize=6.2, color="#433E37",
                    zorder=2.6,
                    bbox=dict(facecolor=RULER_FILL, edgecolor="none",
                              pad=0.7))
    ax.text(0.5 * (RULER_X0 + RULER_X1), mm(VLO) - 2.6, u"Å", ha="center",
            va="top", fontsize=6.2, color="#4A443C", fontweight="bold",
            zorder=2.6)


def draw_density(ax, values, side, colour, norm):
    """One arm's density, hugging the ruler. Back-to-back, so both are on the
    SAME axis rather than in two stacked panels that only look aligned."""
    x, y, n = _density(values, VLO, VHI)
    w = y / norm * DENS_W
    base = RULER_X0 if side < 0 else RULER_X1
    xs = base + side * w
    ys = np.array([mm(t) for t in x])
    ax.fill_betweenx(ys, base, xs, facecolor=colour, alpha=0.26, lw=0,
                     zorder=1.4)
    ax.plot(xs, ys, color=colour, lw=0.8, zorder=1.6)
    return n, (x, w, base, side)


def density_x(dcurve, value):
    """Where a value's leader meets its own density curve."""
    x, w, base, side = dcurve
    return base + side * float(np.interp(value, x, w))


def leader(ax, value, x_from, x_to, colour, dcurve, label):
    """A horizontal tie from a render box to the ruler, at the row's value.

    This is the join that makes the composition honest: the box's centre line,
    the marked point on its own arm's density, and the tick on the ruler are
    all at one y, and that y is the measured number. There is no way to move
    the picture without moving the measurement.
    """
    y = mm(value)
    # a short tick on the render box's own edge: the box CENTRE is the value,
    # and without this a reader has no cue about which height of a 37 mm box
    # the leader is speaking for
    ax.plot([x_from, x_from], [y - 1.6, y + 1.6], color=colour, lw=1.2,
            solid_capstyle="butt", zorder=5.1)
    ax.plot([x_from, x_to], [y, y], color="white", lw=2.0, alpha=0.7,
            solid_capstyle="butt", zorder=4.9)
    ax.plot([x_from, x_to], [y, y], color=colour, lw=0.85, zorder=5.0,
            solid_capstyle="butt")
    # the tick that crosses the ruler strip: the value, marked on the scale
    ax.plot([RULER_X0 - 1.0, RULER_X1 + 1.0], [y, y], color=colour, lw=1.6,
            solid_capstyle="butt", zorder=5.4)
    # the point on the population it was drawn from
    xd = density_x(dcurve, value)
    ax.scatter([xd], [y], s=9.0, c=[colour], linewidths=0.45,
               edgecolors="white", zorder=5.6)
    ax.text(0.5 * (x_from + x_to), y + 1.3, label, ha="center", va="bottom",
            fontsize=7.4, color=colour, fontweight="bold", zorder=5.8,
            bbox=dict(facecolor="white", edgecolor=colour, lw=0.4,
                      alpha=0.94, boxstyle="round,pad=0.22"))


def _arm_label(ax, side, value, colour, head, sub, fontsize=6.6):
    """One arm named, with a swatch flush against its own edge of the ruler."""
    y = mm(value)
    base = RULER_X0 if side < 0 else RULER_X1
    sw = 3.2
    x0 = base - sw if side < 0 else base
    ax.add_patch(plt.Rectangle((x0, y - 1.6), sw, 3.2, facecolor=colour,
                               alpha=0.26, lw=0, zorder=8.8))
    ax.add_patch(plt.Rectangle((x0, y - 1.6), sw, 3.2, facecolor="none",
                               edgecolor=colour, lw=0.6, zorder=8.9))
    tx = x0 - 1.4 if side < 0 else x0 + sw + 1.4
    ha = "right" if side < 0 else "left"
    ax.text(tx, y + 0.4, head, ha=ha, va="bottom", fontsize=fontsize,
            color=colour, fontweight="bold", zorder=9)
    ax.text(tx, y - 0.5, sub, ha=ha, va="top", fontsize=fontsize - 0.6,
            color=colour, zorder=9)


def draw_threshold(ax, peak_note):
    """The predicate threshold, edge to edge.

    Edge to edge and not merely across the density, because the whole payoff of
    this style is that the rule visibly passes BETWEEN the two structures: one
    render is entirely below it, the other entirely above it, and that is
    readable at thumbnail size with every string on the page illegible.
    """
    y = mm(B.THR_TILT)
    ax.plot([2.0, FIGW - 2.0], [y, y], color=C_RULE, lw=0.9,
            ls=(0, (3.2, 2.2)), zorder=5.2, alpha=0.9)
    ax.plot([RULER_X0, RULER_X1], [y, y], color=C_RULE, lw=1.3, zorder=5.3)
    ax.text(3.0, y + 1.1, u"predicate threshold  %.3f Å" % B.THR_TILT,
            ha="left", va="bottom", fontsize=6.4, color=C_RULE,
            fontweight="bold", zorder=5.9,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85,
                      boxstyle="round,pad=0.16"))
    if peak_note:
        ax.text(3.0, y - 1.1, peak_note, ha="left", va="top", fontsize=5.0,
                color="#7A7A7A", zorder=5.9,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.85,
                          boxstyle="round,pad=0.16"))
    # Triangles as MARKERS, not as glyphs: the house sans has no U+25B2, and a
    # missing glyph prints as an empty box in the PDF with only a warning.
    for dy, mk, col, txt in ((+2.0, "^", scenes.C_ACTIVE,
                              u"above — active on this axis"),
                             (-2.0, "v", scenes.C_INACTIVE,
                              u"below — inactive")):
        t = ax.text(FIGW - 3.0, y + dy, txt, ha="right",
                    va="center", fontsize=5.8, color=col, fontweight="bold",
                    zorder=5.9,
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.85,
                              boxstyle="round,pad=0.16"))
        w = _text_w_mm(ax.figure, ax, txt, 5.8, "bold")
        ax.plot([FIGW - 4.6 - w], [y + dy], marker=mk, ms=2.6, color=col,
                zorder=6.0)


# --------------------------------------------------------------------------
# typesetting helpers: widths are MEASURED, never estimated
# --------------------------------------------------------------------------
def _text_w_mm(fig, ax, s, fontsize, weight="normal"):
    """Width of a string in millimetres of the page, from the renderer."""
    r = fig.canvas.get_renderer()
    t = ax.text(0, 0, s, fontsize=fontsize, fontweight=weight)
    bb = t.get_window_extent(renderer=r)
    t.remove()
    return bb.width / float(fig.dpi) * 25.4


def _key_col(ax, entries, x_mm, y_mm, fontsize, leading=2.9):
    """The same key stacked vertically, for a tall figure.

    It lives in the quiet quadrant the diagonal composition leaves empty rather
    than in the footer, because the footer of a portrait figure is the one place
    where space is actually scarce - and a key beside the renders is closer to
    what it explains.
    """
    for i, (txt, col) in enumerate(entries):
        ax.plot([x_mm, x_mm + 2.6], [y_mm - i * leading + 0.55] * 2,
                color=col, lw=1.7, solid_capstyle="round", zorder=9)
        ax.text(x_mm + 3.6, y_mm - i * leading, txt, ha="left", va="baseline",
                fontsize=fontsize, color=col, zorder=9)


def _wrapped(fig, ax, text, x0, x1, y_mm, fontsize, colour, leading):
    """Greedy word wrap to a MEASURED width, top-down from `y_mm`.

    The canvas of this figure is fixed, because a position on it is a measured
    quantity. A footnote line wider than the canvas would therefore be clipped
    rather than expand the page, so the wrap has to be real rather than a hand
    guess that was right once.
    """
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and _text_w_mm(fig, ax, trial, fontsize) > (x1 - x0):
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines):
        ax.text(FIGW / 2.0, y_mm - i * leading, ln, ha="center", va="top",
                fontsize=fontsize, color=colour, zorder=9)
    return len(lines)


FOOTNOTE = (
    u"The ruler says WHERE these two predictions fall. It is NOT evidence that "
    u"predicted magnitude tracks reference magnitude (BA-4: negative on 3 of 4 "
    u"backbones), so nothing here measures the gap between them. The two "
    u"renders are DIFFERENT RECEPTORS — the archive ships one prediction per "
    u"case — so the density, not the pair, carries the contrast. Population: "
    u"every Class A prediction; E1+E2 excluded (broken cell, impossible "
    u"geometry), E4 Class A only. The predicate is tilt AND NPxxY-OH; only "
    u"tilt is drawn, and both rendered rows agree on both. Renders carry their "
    u"own 10 Å bars. Soft focus encodes depth only and carries no "
    u"interpretive meaning. The INPUT was the full cognate Gα subunit; only "
    u"its α5 C-terminal 21 residues are drawn."
)

# --------------------------------------------------------------------------
def caption_block(ia, ic, n_apo, n_cog, n_total, f_apo, f_cog):
    """What came out of the frame and MUST go into the LaTeX caption.

    A selection rule that lives only in a script is the corpus's commonest
    render defect wearing a different hat (59 of 232 rows). It is out of the
    picture because a TOC thumbnail is not where it belongs, not because it
    stopped mattering.
    """
    return u"""GA-STYLE-4 CAPTION - REQUIRED CONTENT, do not drop any line.

The measured axis is the figure. A vertical ruler carries TM6 tilt in Angstrom
(2x46 Ca - 6x37 Ca); the predicate's tilt threshold, %.3f A, is drawn edge to
edge; every Class A prediction is drawn as a density on the same ruler, apo to
the left and cognate to the right; and the two rendered predictions are PLACED
at their measured values rather than labelled with them. Left/below: adenosine
A2A (AA2AR) predicted by Boltz-2 from sequence alone, %.2f A, below the
threshold. Right/above: dopamine D2 (DRD2) predicted by OpenFold-3 with the
cognate Ga supplied, %.2f A, above it. Grey is the invariant receptor bundle,
drawn as a depth-weighted heavy-atom density; colour is TM6 and the alpha5
21-mer only. Soft focus encodes depth only and carries no interpretive meaning.

THE AXIS SAYS WHERE THESE TWO PREDICTIONS FALL. It is not evidence that
predicted magnitude tracks reference magnitude, which is BA-4 and is negative
on three of four backbones (and under class_a_only the tilt slopes are negative
for two of them, DISCREPANCY_REPORT D3). There is no arrow and no caliper
between the two structures for that reason, and the vertical gap between them
is deliberately left unlabelled.

THE TWO RENDERS ARE DIFFERENT RECEPTORS. 11_structures/ ships one apo
prediction and three cognate ones and no receptor has both arms, so the
within-condition contrast is the density on the ruler, not the two renders. A
shared axis invites subtraction by eye; the gap between AA2AR and DRD2 is not
one receptor moving.

TWO SCALES. The ruler is %.2f mm per Angstrom; the renders are roughly 0.4 mm
per Angstrom and each carries its own 10 A bar. Positions on the ruler are at
ruler scale; nothing is measured across the boundary.

SELECTION RULES. Below: AA2AR x Boltz-2 x apo cell, n = 25 seeds; the row with
the highest plddt_mean in the cell (73.93; cell median 72.04), i.e. the 100th
percentile on confidence. It sits 0.95 A from AA2AR's INACTIVE reference and
the predicate calls it inactive, which is where an apo prediction belongs; the
directory name 'confidently_wrong' is wrong (DISCREPANCY_REPORT D12). Above:
DRD2 x OpenFold-3 x cognate cell, n = 25 seeds; the row with the MEDIAN
rmsd_to_active_ref in the cell (1.218 A shipped; rank 13 of 25, cell range
1.020-1.507 A) - a typical row of its cell, not a best case. All 25 seeds of
that cell are called active.

BOTH ANCHOR PAIRS WERE VERIFIED from the coordinates drawn: Leu48 / Leu235 Ca
reproduces AA2AR row 567's stored d_gpcrdb_tm6_tilt_246_637_ca = 11.7347 A, and
Leu76 / Leu375 Ca reproduces DRD2 row 8285's 17.2766 A. Four of the drop's
ALIGNMENT.md files name residues that do not reproduce the shipped distances
(D13, D20).

POPULATION. All Class A predictions under E1+E2 (broken cell, impossible
geometry) plus E4 (Class A only): %s apo and %s cognate rows of %s total,
smoothed on the tilt axis, both densities normalised by one common peak. %.1f%%
of apo rows and %.1f%% of cognate rows lie above the tilt threshold. The full
predicate is tilt AND NPxxY-OH; only the tilt axis is drawn here, and both
rendered rows agree on both axes. Block A's cognate arm supplies the FULL
cognate Ga subunit; only its alpha5 C-terminal 21 residues (Ga 334-354) are
drawn, because the heterotrimer is an input this figure is not reporting.

ICL3. %s (below); %s (above).""" % (
        B.THR_TILT, ia["d_tilt"], ic["d_tilt"],
        (YHI - YLO) / (VHI - VLO),
        "{:,}".format(n_apo), "{:,}".format(n_cog), "{:,}".format(n_total),
        100 * f_apo, 100 * f_cog, ia["omitted"], ic["omitted"])


def main():
    fs.use_house_style()
    # THE CANVAS IS FIXED. Everywhere else in this repo `savefig.bbox` is
    # "tight", which trims or expands the page to fit what was drawn. Here the
    # page is the instrument: the ruler is 9.68 mm per Angstrom and the two
    # render boxes are positioned in millimetres from that. A tight bbox that
    # widened the canvas to fit a long footnote would change the figure's
    # proportions after the geometry had been fixed. So the output is exactly
    # FIGW x FIGH mm, and anything that overflows is visible rather than
    # absorbed.
    plt.rcParams["savefig.bbox"] = None

    rows = B.rows()
    core, _, _ = B.core(rows)
    cA = core[core["gpcr_class"] == "A"].copy()
    apo = cA[cA["arm"] == "apo"][XCOL].dropna()
    cog = cA[cA["arm"] == "cognate"][XCOL].dropna()
    f_apo = float((apo > B.THR_TILT).mean())
    f_cog = float((cog > B.THR_TILT).mean())

    fig = plt.figure(figsize=(FIGW * fs.MM, FIGH * fs.MM))

    # One background axes in MILLIMETRES of the page. Everything positional -
    # ruler, densities, threshold, leaders - is drawn here, so a value in
    # Angstrom converts to a page position through exactly one function.
    axb = fig.add_axes([0, 0, 1, 1])
    axb.set_xlim(0, FIGW)
    axb.set_ylim(0, FIGH)
    axb.set_facecolor("white")
    axb.set_xticks([])
    axb.set_yticks([])
    for s in axb.spines.values():
        s.set_visible(False)

    # --- the population, first, so everything else lands on top ----------
    # ONE normaliser for both arms: the two lobes are comparable in area, and
    # scaling each to its own peak would make a narrow arm look as populous as
    # a broad one.
    norm = max(_density(apo, VLO, VHI)[1].max(),
               _density(cog, VLO, VHI)[1].max())
    n_apo, d_apo = draw_density(axb, apo, -1, C_APO, norm)
    n_cog, d_cog = draw_density(axb, cog, +1, C_COG, norm)

    draw_ruler(axb)

    # --- the two renders, PLACED at their values -------------------------
    # An axes has to be positioned before it can be drawn into, so the box
    # goes at the value the TIDY DATA stores for the row and the distance
    # re-measured from the coordinates is checked against it afterwards.
    # `verify_anchor` has already refused anything more than 2e-3 A out, which
    # is 0.02 mm on this ruler; the assertion below is the same guarantee
    # restated in page units, so a box cannot end up anywhere but at its value.
    aspect = REND_W / REND_H
    y_apo = mm(HR.ANCHORS["aa2ar"]["d_tilt"]) - REND_H / 2.0
    axl = fig.add_axes([REND_L_X / FIGW, y_apo / FIGH,
                        REND_W / FIGW, REND_H / FIGH])
    ia = render_apo(axl, aspect)

    y_cog = mm(HR.ANCHORS["drd2"]["d_tilt"]) - REND_H / 2.0
    axr = fig.add_axes([REND_R_X / FIGW, y_cog / FIGH,
                        REND_W / FIGW, REND_H / FIGH])
    ic = render_cognate(axr, aspect)

    for info, y0 in ((ia, y_apo), (ic, y_cog)):
        off = abs(mm(info["d_tilt"]) - (y0 + REND_H / 2.0))
        if off > 0.03:
            raise ValueError(
                "render box centre is %.4f mm off its measured value; the box "
                "position IS the number and may not drift" % off)

    # the per-arm percentages live on the arm labels, where they are
    # colour-tied to the arm they belong to; repeating them here was clutter
    draw_threshold(axb, None)

    leader(axb, ia["d_tilt"], REND_L_X + REND_W, RULER_X0,
           scenes.C_INACTIVE, d_apo, u"%.2f Å" % ia["d_tilt"])
    leader(axb, ic["d_tilt"], REND_R_X, RULER_X1,
           scenes.C_ACTIVE, d_cog, u"%.2f Å" % ic["d_tilt"])

    # --- what each render is ----------------------------------------------
    # Titles go OUTSIDE the boxes, into the two quiet quadrants the layout
    # creates: the apo box is low-left so its title sits above it, the cognate
    # box is high-right so its title sits above it too, clear of the ruler.
    for cx, cy, head, sub, colour in (
            (REND_L_X + REND_W / 2.0, y_apo + REND_H + 1.6,
             u"no co-input \u2014 sequence alone",
             u"AA2AR \u00b7 Boltz-2\nrow 567 \u00b7 1 of 25 seeds",
             scenes.C_INACTIVE),
            (REND_R_X + REND_W / 2.0, y_cog + REND_H + 1.6,
             u"+ cognate G\u03b1 supplied",
             u"DRD2 \u00b7 OpenFold-3\nrow 8285 \u00b7 1 of 25 seeds",
             scenes.C_ACTIVE)):
        # Two lines, not one. On a FIXED canvas an over-long line is silently
        # clipped at the page edge rather than expanding the figure, and the
        # one-line version of the cognate sub-title lost its final word that
        # way. Widths are checked rather than trusted.
        for txt, fsz, dy, wt, col in (
                (sub, 5.6, 0.0, "normal", "#5A5A5A"),
                (head, 7.2, 5.2, "bold", colour)):
            w = _text_w_mm(fig, axb, txt.split(u"\n")[0], fsz, wt)
            for line in txt.split(u"\n")[1:]:
                w = max(w, _text_w_mm(fig, axb, line, fsz, wt))
            if cx - w / 2.0 < 0.8 or cx + w / 2.0 > FIGW - 0.8:
                raise ValueError("render title %r is %.1f mm wide and would be "
                                 "clipped by the fixed canvas" % (txt, w))
            axb.text(cx, cy + dy, txt, ha="center", va="bottom",
                     fontsize=fsz, fontweight=wt, color=col,
                     linespacing=1.35, zorder=9)

    # --- the two arm labels, in the quadrants each density leaves empty ----
    # Each label is anchored by a SWATCH flush against the edge of the ruler
    # that its own lobe grows out of, filled at the same colour and alpha as
    # the fill. That is what ties the words to the curve: the apo label sits
    # high on the left where the apo lobe has nothing to say, and without the
    # swatch the eye reads it against whichever lobe happens to be beside it.
    _arm_label(axb, -1, 18.9, C_APO,
               u"apo — sequence alone",
               u"n = %s   ·   %.0f%% above threshold"
               % ("{:,}".format(n_apo), 100 * f_apo))
    _arm_label(axb, +1, 12.9, C_COG,
               u"+ cognate Gα supplied as a co-input",
               u"n = %s   ·   %.0f%% above threshold"
               % ("{:,}".format(n_cog), 100 * f_cog))

    # --- title block ------------------------------------------------------
    axb.text(FIGW / 2.0, FIGH - 3.4,
             u"Supply the cognate Gα and the prediction",
             ha="center", va="top", fontsize=8.4, fontweight="bold",
             color=C_HEAD, zorder=9)
    axb.text(FIGW / 2.0, FIGH - 7.6,
             u"lands on the active side of the TM6-tilt threshold",
             ha="center", va="top", fontsize=8.4, fontweight="bold",
             color=C_HEAD, zorder=9)
    axb.text(FIGW / 2.0, FIGH - 11.6,
             u"one measured axis · TM6 tilt · 2×46 Cα – 6×37 Cα · "
             u"everything here is placed on it",
             ha="center", va="top", fontsize=5.6, color="#6A6A6A", zorder=9)

    # --- colour key, as coloured words rather than a legend box ------------
    # Widths are MEASURED from the renderer, not estimated from string length:
    # a hand-estimated advance is how the first build put four coloured phrases
    # on top of one another.
    _key_col(axb, [(u"TM6 — predicate INACTIVE", scenes.C_INACTIVE),
                   (u"TM6 — predicate ACTIVE", scenes.C_ACTIVE),
                   (u"α5 C-terminal 21-mer (Gα 334–354)", scenes.C_PEPTIDE),
                   (u"receptor bundle — not the subject", "#8A8A8A")],
             x_mm=4.0, y_mm=84.0, fontsize=5.4)

    # --- footnote ---------------------------------------------------------
    # Wrapped to a measured width, not by hand. The canvas is fixed at
    # FIGW x FIGH (savefig.bbox is disabled below) precisely because in this
    # figure a page position is a measured quantity; a line that overflowed
    # would be clipped rather than silently widening the page and rescaling
    # the ruler.
    nl = _wrapped(fig, axb, FOOTNOTE, x0=1.5, x1=FIGW - 1.5, y_mm=12.4,
                  fontsize=4.6, colour="#7A7A7A", leading=2.0)
    if 12.4 - (nl - 1) * 2.0 < 1.4:
        raise ValueError("footnote runs off the fixed canvas at %d lines; "
                         "shorten it rather than letting it clip" % nl)

    dof.raster_dpi(fig)
    paths = fs.save(fig, "ga_style4_axis")
    print("GA-style-4 written:", *paths, sep="\n  ")
    print("  ruler %.2f mm per A over %.1f-%.1f A" % ((YHI - YLO) / (VHI - VLO),
                                                      VLO, VHI))
    print("  apo   %.4f A (row 567)  · %s · %.0f%% behind focus"
          % (ia["d_tilt"], ia["view"], 100 * ia["behind_focus"]))
    print("  cog   %.4f A (row 8285) · %s · %.0f%% behind focus"
          % (ic["d_tilt"], ic["view"], 100 * ic["behind_focus"]))
    print("  page gap between the two boxes' centres: %.2f mm = %.3f A"
          % (mm(ic["d_tilt"]) - mm(ia["d_tilt"]), ic["d_tilt"] - ia["d_tilt"]))
    print("  density: %d apo / %d cognate Class A rows of %d"
          % (n_apo, n_cog, len(rows)))
    print("  above tilt threshold: apo %.1f%%  cognate %.1f%%"
          % (100 * f_apo, 100 * f_cog))
    print("\n" + caption_block(ia, ic, n_apo, n_cog, len(rows), f_apo, f_cog))


if __name__ == "__main__":
    main()
