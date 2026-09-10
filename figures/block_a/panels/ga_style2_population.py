"""
GA-STYLE-2 - "population first": the data is the hero, the structures are
callouts hanging off it.

THE INVERSION. GA-1 leads with three structure renders and puts every Class A
prediction in a thin strip underneath. This is the same evidence with the
hierarchy turned over. The dominant object is the population itself - 7,966
Class A predictions on one axis, apo against cognate - drawn across the whole
frame as a mirrored raincloud, and the two renders are small cards pinned by
leader lines to the exact tilt values their rows sit at.

The argument for doing it this way. The population IS the result. Two renders
are two draws; the claim is about four thousand of each. The commonest defect
in the corpus's 232 structure renders is a hand-picked example with no
quantitative panel behind it (58 rows) or no stated selection rule (59 rows) -
both are defects of *hierarchy*, a picture standing where a distribution should
be. Leading with the distribution makes them structurally impossible: the
render cannot be the evidence when the evidence is drawn ten times larger
around it, and each card is labelled with where in its own arm's distribution
that row falls (20th and 39th percentile - typical rows, not best cases).

WHAT THE READER SHOULD SEE, IN ORDER
  1  two separated populations, ~4,000 predictions each, on one axis
  2  a threshold line, and how much of each population is on which side
  3  only then: here is what one prediction from each side looks like

HOW THE LANES ARE BUILT. Mirrored about a central baseline: the cognate arm
opens upward, apo downward. Each lane is `rain` (every prediction, jittered,
so the reader can see the n rather than being told it) then `cloud` (a
deterministic smoothed histogram of the same rows). Both clouds are scaled by
ONE shared factor, so a taller hump means more predictions per Angstrom and
not a renormalised lane. The median and the interquartile range are drawn in
the rain band.

WHY THE CARDS SIT WHERE THEY DO. Each render's tilt value falls at its own
arm's mode, so a card placed near its value is placed on top of its own data.
The only empty regions of the frame are the two cross-lane corners - the
cognate lane below 13 A, the apo lane above 17.9 A - and that is where the
cards go, each connected to its value by a leader line that crosses the
baseline into its own lane. Nothing in either card overlaps a drawn
observation; the two minor modes (apo above the threshold, cognate below it)
are real and stay visible.

THE SECOND MEASURE, AND WHY IT EARNS ITS PLACE. The threshold marked on the
hero axis is only half the predicate. On tilt alone 94.0% of cognate rows
clear the line; the predicate calls 79.6% of them active, because it is an AND
over tilt and NPxxY. A figure that marks one threshold and reports the
predicate rate without showing the other axis is quietly mis-stating its own
rule, so NPxxY is drawn as a deliberately subordinate strip beneath the frame,
on its own axis with its own threshold and its own direction. It is not on the
hero axis: two measures sharing one axis is a named plot defect.

NO ARROW ANYWHERE, and no claim of amplitude. Two separated populations is a
statement about which state is REACHED. It is not a statement that a receptor
with further to travel travels further - that is BA-4, and BA-4 is negative on
three of four backbones. The composition therefore contains no arrow between
the lanes, no delta, and no line joining the two card values.

Sizes are for a 152 mm figure that survives reduction to the 80 mm a TOC
thumbnail gets (x0.53). `constrained_layout` is off: the card rectangles are
computed from the main axes' data coordinates, which has to happen after the
limits are fixed and before anything is drawn into them.
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

import badata as B                                             # noqa: E402
import cifread as CR                                           # noqa: E402
import figstyle as fs                                          # noqa: E402
import matplotlib.pyplot as plt                                # noqa: E402

import dofrender as D                                          # noqa: E402
import dofscenes as S                                          # noqa: E402
import hero_renders as HR                                      # noqa: E402

XCOL = "d_gpcrdb_tm6_tilt_246_637_ca"
NCOL = "d_npxxy_oh"

C_APO = "#6E6E6E"          # apo arm. Darker than figstyle.GREY, which
                           # disappears under 4,000 alpha-blended points.
C_COG = fs.GREEN           # the cognate Ga co-input, everywhere in this paper
C_ACTIVE = fs.VERM         # the predicate calls this row active
C_INACTIVE = fs.BLUE       # ... or inactive
C_HEAD = "#1A1A1A"
C_MUTE = "#7A7A7A"

XLO, XHI = 10.35, 20.05    # the full observed range, 10.67-19.67, unbroken
YLO, YHI = -1.62, 1.44

RAIN = (0.055, 0.245)      # |y| band the individual predictions live in
CLOUD0 = 0.300             # |y| the smoothed density starts from
CLOUDH = 0.560             # |y| the TALLEST cloud adds; both share this scale

CARD_W, CARD_H = 21.0, 26.0   # mm. Portrait, because a 7TM bundle seen from
                              # the side is portrait and a square frame would
                              # be a third empty ground.


# --------------------------------------------------------------------------
# the population
# --------------------------------------------------------------------------
def _density(values, lo, hi, n=420, sigma_bins=9):
    """Smoothed histogram on a fixed grid. Deterministic - no bandwidth
    chosen by eye, and the same grid for both arms so the two curves are
    comparable rather than merely adjacent."""
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    edges = np.linspace(lo, hi, n + 1)
    h, _ = np.histogram(v, bins=edges)
    k = np.exp(-0.5 * (np.arange(-4 * sigma_bins, 4 * sigma_bins + 1)
                       / float(sigma_bins)) ** 2)
    k = k / k.sum()
    y = np.convolve(h.astype(float), k, mode="same")
    return 0.5 * (edges[:-1] + edges[1:]), y


def _lane(ax, values, colour, sign, scale, rng, lo, hi, rain_alpha=0.11,
          rain_size=0.9, cloud_alpha=0.30):
    """One arm: every prediction as a jittered point, then its density.

    The points come FIRST and nearer the axis on purpose. A reader who is told
    n = 3,992 has to trust the caption; a reader who can see four thousand
    marks does not. `bounded_fraction_hist`-style counts and a bare violin
    both hide exactly this, which is why the corpus's plot defects are led by
    'bars standing in for distributions'.
    """
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    y = sign * rng.uniform(RAIN[0], RAIN[1], len(v))
    ax.scatter(v, y, s=rain_size, c=colour, alpha=rain_alpha, linewidths=0,
               zorder=2.0, rasterized=True)

    x, d = _density(v, lo, hi)
    top = sign * (CLOUD0 + d * scale)
    base = np.full_like(top, sign * CLOUD0)
    ax.fill_between(x, base, top, color=colour, alpha=cloud_alpha,
                    linewidth=0, zorder=2.4)
    ax.plot(x, top, color=colour, lw=0.9, zorder=2.6)

    q1, med, q3 = np.percentile(v, [25, 50, 75])
    yc = sign * 0.5 * (RAIN[0] + RAIN[1])
    ax.plot([q1, q3], [yc, yc], color="white", lw=3.0,
            solid_capstyle="butt", zorder=3.0)
    ax.plot([q1, q3], [yc, yc], color=colour, lw=1.6,
            solid_capstyle="butt", zorder=3.1)
    ax.scatter([med], [yc], s=11, c="white", linewidths=0.9,
               edgecolors=colour, zorder=3.2)
    return dict(n=len(v), median=float(med), q1=float(q1), q3=float(q3),
                peak=float(d.max()))


# --------------------------------------------------------------------------
# the two callout cards
# --------------------------------------------------------------------------
def _card(ax, key, path, chain, lo, hi, tm6_colour, aspect, peptide=None,
          name=""):
    """One prediction, side view, at callout size.

    Everything a full panel would carry - the selection-rule chip, the second
    measurement, the four-residue ball-and-stick, the colour key - is out. At
    21 mm the chip is a smudge; the rule belongs in the caption and in
    PROV_style2.md, and it is quoted there in full.

    THE VALUE AND ITS ATOM PAIR ARE PRINTED BESIDE THE CARD, NOT ON IT. This
    is the one place this composition departs from `dofrender.measured_distance`
    and it is a legibility decision, not a relaxation: at 21 mm the value's
    white label box covers half the receptor, and after reduction to 80 mm its
    atom-pair line is under 2 pt. So the card draws the dash and its two
    endpoint atoms in the house grammar, and the label block immediately
    beside it carries "TM6 tilt 11.73 A (Leu48 Ca - Leu235 Ca)" at a size that
    survives. Every measured distance still carries its value and its atom
    pair; they are one leader line away instead of on top of the dash.
    """
    dt, dn = HR.verify(path, key, name)
    atoms = CR.frame(path)
    a = HR.ANCHORS[key]
    ca = np.vstack(S._body_runs(atoms, chain, lo, hi, key))
    frame = D.camera_frame(path, (chain, lo, hi),
                           ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                           "side", ca=ca)
    P = frame.project(ca)
    pts = [P[:, :2]]
    Q = None
    if peptide is not None:
        Q = frame.project(np.vstack(D.ca_runs(atoms, *peptide)))
        pts.append(Q[:, :2])
    xlim, ylim = D.frame_limits(pts, aspect, pad=1.05)
    zs = [P[:, 2]] + ([Q[:, 2]] if Q is not None else [])
    ds = (min(z.min() for z in zs), max(z.max() for z in zs))

    tm6 = frame.project(S._tm6_run(atoms, chain, key))
    anch = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA"),
                          CR.atom(atoms, chain, a["tilt"][1], "CA")])
    claim = [tm6, anch] + ([Q] if Q is not None else [])
    focus = D.focal_plane(*claim)
    behind = D.focus_report(claim, focus, ds, "GA-style2 %s" % name)

    D.setup_axes(ax, xlim, ylim)
    # Lighter blur and a stronger hairline than the full-size panels use. At
    # 21 mm the panel-strength density is a smudge with a coloured worm on it
    # and the seven-helix bundle stops being legible AS a bundle, which is the
    # one thing the grey scaffold is there to say.
    S._draw_receptor(ax, frame, atoms, chain, lo, hi, key, xlim, ylim, ds,
                     focus_at=focus, blur_alpha=(0.34, 0.56), trace_alpha=0.52)
    if Q is not None:
        D.blurred_layer(ax, [Q], C_COG, xlim, ylim, ds, sigma_A=1.2,
                        base_alpha=0.34, zorder=1.4)
    D.ribbon(ax, tm6, tm6_colour, lw=2.1, halo_extra=1.0, depth_span=ds,
             zorder=6.0)
    if Q is not None:
        D.ribbon(ax, Q, C_COG, lw=2.3, halo_extra=1.0, depth_span=ds,
                 zorder=6.6)

    names = dict((r, CR.residue_name(atoms, chain, r)) for r in a["tilt"])
    p, q = anch[0, :2], anch[1, :2]
    ax.plot([p[0], q[0]], [p[1], q[1]], color="white", lw=2.1,
            solid_capstyle="butt", zorder=8.3)
    ax.plot([p[0], q[0]], [p[1], q[1]], color="#111111", lw=0.95,
            ls=(0, (2.4, 1.9)), solid_capstyle="butt", zorder=8.5)
    for xy in (p, q):
        ax.scatter([xy[0]], [xy[1]], s=9, c=["#111111"], linewidths=0.45,
                   edgecolors="white", zorder=8.6)
    D.scale_bar(ax, length=10.0, fontsize=3.9, pad=0.055)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_linewidth(0.55)
        s.set_color("#C6C1BA")
    return dict(d_tilt=dt, d_npxxy=dn, view=frame.label, behind_focus=behind,
                pair=u"%s%d Cα – %s%d Cα"
                     % (names[a["tilt"][0]].title(), a["tilt"][0],
                        names[a["tilt"][1]].title(), a["tilt"][1]),
                omitted=S._omitted(atoms, chain, lo, hi, key))


def _rect(ax, fig, x_data, y_data, w_mm, h_mm, anchor="sw"):
    """A figure-coordinate rectangle anchored at a point in the main axes'
    DATA coordinates, sized in millimetres.

    Two coordinate systems have to meet here: the card has to sit at a stated
    place in the population (data) and be a stated physical size on the page
    (mm), because a card sized as a fraction of the axes changes size whenever
    the x range does. Requires the limits to be final.
    """
    x0, y0 = fig.transFigure.inverted().transform(
        ax.transData.transform((x_data, y_data)))
    w = w_mm * fs.MM / fig.get_figwidth()
    h = h_mm * fs.MM / fig.get_figheight()
    if "e" in anchor:
        x0 -= w
    if "n" in anchor:
        y0 -= h
    return [x0, y0, w, h]


def _stack(fig, x, y_top, lines, ha="left", gap=1.55):
    """Lines of different size and colour, stacked downward from `y_top`.

    matplotlib cannot vary size or colour inside one text object, and this
    block has to: the VALUE is what the eye must land on, the atom pair has to
    be right under it rather than in a caption, and the predicate call has to
    be printed in the colour TM6 is drawn in - otherwise the card shows a blue
    helix and the label calls it something in grey, and the reader has no way
    to learn the encoding from the figure.
    """
    y = y_top
    for text, size, colour, weight in lines:
        h = size * gap / 72.0 / fig.get_figheight()
        fig.text(x, y, text, ha=ha, va="top", fontsize=size, color=colour,
                 fontweight=weight)
        y -= h
    return y_top - y


def _stack_height(fig, lines, gap=1.55):
    return sum(s * gap / 72.0 / fig.get_figheight() for _, s, _, _ in lines)


# --------------------------------------------------------------------------
def caption_block(info):
    """The material that is NOT in the frame and must be in the caption."""
    return u"""GA-STYLE-2 CAPTION - REQUIRED CONTENT, do not drop any line.

A 21-residue Ga alpha5 C-terminal co-input separates the predicted population
into two. Every Class A prediction in Block A is plotted on one axis, the TM6
tilt 2x46 Ca - 6x37 Ca: %s apo predictions (grey, below the line) against
%s with the cognate Ga supplied (green, above it), from %d receptors x 4
backbones x 25 seeds. Each point is one prediction; the smoothed density above
it is the same rows, and both densities are drawn on ONE shared vertical scale.
Median and interquartile range are marked in each band. The dashed vertical is
the tilt half of the state predicate, %.3f A.

FILTER. %s;
n = %s of %s rows. Never excl_any: E3 is a property of the receptor's
REFERENCE and is irrelevant to a raw distribution, which divides by nothing,
and E5 is a sensitivity set.

THE PREDICATE IS AN AND, AND BOTH HALVES ARE DRAWN. tilt > %.3f A AND NPxxY
(Y5.58 OH - Y7.53 OH) < %.3f A. On tilt alone %.1f%% of cognate rows and
%.1f%% of apo rows clear the line; the full predicate calls %.1f%% of cognate
and %.1f%% of apo rows active. The NPxxY strip beneath the frame is that
second axis, on its own scale.

THE TWO CARDS ARE SINGLE PREDICTIONS, AND THEY ARE DIFFERENT RECEPTORS.
11_structures/ ships one apo prediction and three cognate ones and no receptor
has both arms, so the within-condition contrast is the population, not the two
cards. Left card: adenosine A2A (AA2AR) x Boltz-2 x apo, row 567 - the row
with the highest plddt_mean in its 25-seed cell (73.93; cell median 72.04),
i.e. the 100th percentile on confidence, and the %.0fth percentile of the apo
arm on tilt. It sits 0.95 A from AA2AR's INACTIVE reference and the predicate
calls it inactive, which is where an apo prediction belongs; the directory
name 'confidently_wrong' is wrong (DISCREPANCY_REPORT D12). Right card:
dopamine D2 (DRD2) x OpenFold-3 x cognate, row 8285 - the MEDIAN
rmsd_to_active_ref in its 25-seed cell (1.218 A shipped; rank 13 of 25, cell
range 1.020-1.507 A), the %.0fth percentile of the cognate arm on tilt. A
typical row of its cell, not a best case; all 25 seeds of that cell are called
active.

BOTH ANCHOR PAIRS WERE VERIFIED against the tidy data from the coordinates
drawn: Leu48 Ca / Leu235 Ca reproduces AA2AR row 567's stored
d_gpcrdb_tm6_tilt_246_637_ca = 11.7347 A, and Leu76 Ca / Leu375 Ca reproduces
DRD2 row 8285's 17.2766 A. Four of the drop's ALIGNMENT.md files name residues
that do not reproduce the shipped distances (D13, D20).

RENDERS. %s; camera from camera.py's rule. Grey is the invariant
receptor drawn as a depth-weighted heavy-atom density; colour is TM6 only,
vermillion where the predicate fires and blue where it does not, plus the
alpha5 21-mer in green on the cognate card. Block A's cognate arm supplies the
FULL cognate Ga subunit; only its alpha5 C-terminal 21 residues (Ga 334-354)
are drawn, because the heterotrimer is an input this figure is not reporting.
Soft focus encodes depth only and carries no interpretive meaning. The
predicted ICL3 is dropped from both cards by one rule (%s; %s).

WHAT THIS FIGURE DOES NOT SHOW: amplitude reproduction - whether a receptor
with further to travel travels further - which is BA-4 and is negative on
three of four backbones. There is no arrow anywhere in the composition and no
line joining the two card values, for that reason.""" % (
        "{:,}".format(info["n_apo"]), "{:,}".format(info["n_cog"]),
        info["n_receptors"], B.THR_TILT,
        info["label"], "{:,}".format(info["n_core"]),
        "{:,}".format(info["n_rows"]),
        B.THR_TILT, B.THR_NPXXY,
        100 * info["cog_tilt"], 100 * info["apo_tilt"],
        100 * info["cog_act"], 100 * info["apo_act"],
        info["pct_apo"], info["pct_cog"],
        info["view"], info["omit_apo"], info["omit_cog"])


def main():
    fs.use_house_style()

    rows = B.rows()
    cA, label, n_core = B.core_class_a(rows)
    apo = cA[cA["arm"] == "apo"]
    cog = cA[cA["arm"] == "cognate"]

    d_apo = 11.734713          # row 567, verified below from coordinates
    d_cog = 17.276566          # row 8285
    pct_apo = 100.0 * (apo[XCOL] < d_apo).mean()
    pct_cog = 100.0 * (cog[XCOL] < d_cog).mean()

    fig = plt.figure(figsize=(152 * fs.MM, 126 * fs.MM))

    # --- headline --------------------------------------------------------
    fig.text(0.042, 0.988, u"One co-input splits the predicted population "
                           u"in two",
             ha="left", va="top", fontsize=11.0, fontweight="bold",
             color=C_HEAD)
    seeds = int(cA.groupby(["receptor", "backbone", "arm"]).size().median())
    fig.text(0.042, 0.947,
             u"every Class A prediction in Block A, on the TM6 tilt axis "
             u"— %d receptors × %d backbones × %d seeds"
             % (cA["receptor"].nunique(), cA["backbone"].nunique(), seeds),
             ha="left", va="top", fontsize=6.4, color=C_MUTE)

    # --- the hero --------------------------------------------------------
    ax = fig.add_axes([0.042, 0.262, 0.950, 0.633])
    ax.set_xlim(XLO, XHI)
    ax.set_ylim(YLO, YHI)

    # the active side of the tilt threshold, tinted rather than outlined: an
    # outline would read as a second data element.
    ax.axvspan(B.THR_TILT, XHI, color=C_ACTIVE, alpha=0.035, linewidth=0,
               zorder=0.5)
    ax.axhline(0.0, color="#C9C4BC", lw=0.5, zorder=1.0)

    rng = np.random.RandomState(11)
    xg, da = _density(apo[XCOL].values, XLO, XHI)
    _, dc = _density(cog[XCOL].values, XLO, XHI)
    scale = CLOUDH / max(da.max(), dc.max())      # ONE scale for both lanes

    s_cog = _lane(ax, cog[XCOL].values, C_COG, +1, scale, rng, XLO, XHI)
    s_apo = _lane(ax, apo[XCOL].values, C_APO, -1, scale, rng, XLO, XHI)

    ax.axvline(B.THR_TILT, color="#8C8781", lw=0.7, ls=(0, (2.6, 2.0)),
               zorder=4.0)

    # --- what each lane is, printed on the lane --------------------------
    # Every number in these two labels is recomputed here from the same frame
    # the lane was drawn from. Nothing in this figure is a typed-in constant.
    f_cog = 100.0 * (cog[XCOL] > B.THR_TILT).mean()
    f_apo = 100.0 * (apo[XCOL] > B.THR_TILT).mean()
    ax.text(17.45, 0.905, u"+ cognate Gα",
            ha="center", va="bottom", fontsize=9.5, fontweight="bold",
            color=C_COG, zorder=6)
    ax.text(17.45, 1.195, u"%s predictions  ·  %.1f%% above the threshold"
            % ("{:,}".format(s_cog["n"]), f_cog),
            ha="center", va="bottom", fontsize=6.6, color=C_COG, zorder=6)

    ax.text(11.95, -0.905, u"apo — sequence alone",
            ha="center", va="top", fontsize=9.5, fontweight="bold",
            color=C_APO, zorder=6)
    ax.text(12.30, -1.195, u"%s predictions  ·  %.1f%% above the threshold"
            % ("{:,}".format(s_apo["n"]), f_apo),
            ha="center", va="top", fontsize=6.6, color=C_APO, zorder=6)

    # Low and to the LEFT of the line: at 14.9 the vertical run is occupied
    # from the cognate cloud to the bottom text, and the y = -1.47 row is the
    # only band of the frame with nothing drawn in it.
    ax.annotate(u"tilt half of the state predicate — active is above %.3f Å"
                % B.THR_TILT,
                (B.THR_TILT, -1.47), xytext=(-3, 0),
                textcoords="offset points", ha="right", va="center",
                fontsize=5.2, color="#7E7972", zorder=6)

    # --- the scale -------------------------------------------------------
    ax.set_yticks([])
    ax.set_xticks(np.arange(11, 21, 1))
    ax.tick_params(axis="x", labelsize=6.0, length=2.2, width=0.5, pad=2.0)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.spines["bottom"].set_position(("data", YLO))
    ax.set_xlabel(u"TM6 tilt (Å)  ·  2×46 Cα – 6×37 Cα, the same atom pair "
                  u"on every prediction",
                  fontsize=7.0, labelpad=1.5, color=C_HEAD)

    # --- the two cards, in the only two empty corners of the frame -------
    # Placed cross-lane on purpose: each render's value falls at its own
    # arm's mode, so a card near its value would sit on its own data. The
    # leader line, not the card's x position, is what pins it.
    r_apo = _rect(ax, fig, 10.46, 0.400, CARD_W, CARD_H)
    r_cog = _rect(ax, fig, 19.94, -0.400, CARD_W, CARD_H, anchor="ne")

    ax_apo = fig.add_axes(r_apo)
    ia = _card(ax_apo, "aa2ar", HR.AA2AR_APO, "A", 1, 316, C_INACTIVE,
               r_apo[2] * fig.get_figwidth() / (r_apo[3] * fig.get_figheight()),
               name="AA2AR row 567")
    ax_cog = fig.add_axes(r_cog)
    ic = _card(ax_cog, "drd2", HR.DRD2_COG, "A", 30, 443, C_ACTIVE,
               r_cog[2] * fig.get_figwidth() / (r_cog[3] * fig.get_figheight()),
               peptide=("B", 334, 354), name="DRD2 row 8285")

    assert abs(ia["d_tilt"] - d_apo) < 1e-4 and abs(ic["d_tilt"] - d_cog) < 1e-4

    # --- pin each card to the exact value its row sits at -----------------
    for value, colour, sign, rect, side in (
            (d_apo, C_APO, -1, r_apo, "se"),
            (d_cog, C_COG, +1, r_cog, "nw")):
        # the mark: a tick standing in the row's OWN lane, so a card drawn in
        # the opposite corner cannot be read as belonging to the wrong arm
        ax.plot([value, value], [0.0, sign * 0.285], color="white", lw=2.2,
                solid_capstyle="butt", zorder=5.0)
        ax.plot([value, value], [0.0, sign * 0.285], color=colour, lw=1.1,
                solid_capstyle="butt", zorder=5.1)
        ax.scatter([value], [0.0], s=13, c=[colour], linewidths=0.6,
                   edgecolors="white", zorder=5.3)
        # NO value label at the mark. A white label box here lands on the
        # rising flank of the arm's own density - it would hide the very
        # observations the mark exists to sit among. The value is printed
        # once, large, at the other end of the leader line.
        # the leader: the card CORNER nearest the mark, so the line is short
        # and does not cut across the opposite lane's density
        cx = rect[0] + (rect[2] if "e" in side else 0.0)
        cy = rect[1] + (rect[3] if "n" in side else 0.0)
        px, py = fig.transFigure.inverted().transform(
            ax.transData.transform((value, 0.0)))
        fig.add_artist(plt.Line2D([cx, px], [cy, py], transform=fig.transFigure,
                                  color=colour, lw=0.5, alpha=0.85,
                                  zorder=0.9, solid_capstyle="butt"))

    # --- what each card is, beside it, not on it -------------------------
    apo_lines = [
        (u"AA2AR · apo · Boltz-2 · row 567", 5.6, C_APO, "bold"),
        (u"TM6 tilt %.2f Å" % ia["d_tilt"], 7.4, C_HEAD, "bold"),
        (ia["pair"], 5.0, "#555555", "normal"),
        (u"ONE of %s apo predictions — %.0fth percentile of the apo arm"
         % ("{:,}".format(s_apo["n"]), pct_apo), 5.2, C_APO, "normal"),
        (u"TM6 — predicate: INACTIVE", 5.2, C_INACTIVE, "bold"),
        (u"grey = the invariant receptor bundle, not the subject", 4.7,
         "#8A8A8A", "normal"),
    ]
    cog_lines = [
        (u"DRD2 · + cognate Gα · OpenFold-3 · row 8285", 5.6, C_COG, "bold"),
        (u"TM6 tilt %.2f Å" % ic["d_tilt"], 7.4, C_HEAD, "bold"),
        (ic["pair"], 5.0, "#555555", "normal"),
        (u"ONE of %s cognate predictions — %.0fth percentile of the cognate "
         u"arm" % ("{:,}".format(s_cog["n"]), pct_cog), 5.2, C_COG, "normal"),
        (u"TM6 — predicate: ACTIVE", 5.2, C_ACTIVE, "bold"),
        (u"α5 C-terminal 21-mer (Gα 334–354) — the FULL cognate Gα was the "
         u"input; only the 21-mer is drawn", 4.7, C_COG, "normal"),
    ]
    _stack(fig, r_apo[0] + r_apo[2] + 0.013, r_apo[1] + r_apo[3], apo_lines)
    _stack(fig, r_cog[0] - 0.013,
           r_cog[1] + _stack_height(fig, cog_lines), cog_lines, ha="right")

    # --- the second predicate axis, deliberately subordinate -------------
    axn = fig.add_axes([0.042, 0.120, 0.235, 0.068])
    nlo, nhi = 2.0, 24.0
    _, na = _density(apo[NCOL].values, nlo, nhi)
    _, nc = _density(cog[NCOL].values, nlo, nhi)
    nscale = 0.62 / max(na.max(), nc.max())
    axn.axvspan(nlo, B.THR_NPXXY, color=C_ACTIVE, alpha=0.045, linewidth=0,
                zorder=0.5)
    for vals, colour, sign in ((cog[NCOL].values, C_COG, +1),
                               (apo[NCOL].values, C_APO, -1)):
        x, d = _density(vals, nlo, nhi)
        top = sign * d * nscale
        axn.fill_between(x, 0, top, color=colour, alpha=0.34, linewidth=0)
        axn.plot(x, top, color=colour, lw=0.7)
    axn.axvline(B.THR_NPXXY, color="#8C8781", lw=0.6, ls=(0, (2.4, 1.8)))
    axn.set_xlim(nlo, nhi)
    axn.set_ylim(-0.72, 0.72)
    axn.set_yticks([])
    axn.set_xticks([5, 10, 15, 20])
    axn.tick_params(axis="x", labelsize=5.0, length=1.8, width=0.4, pad=1.2)
    for side in ("left", "right", "top"):
        axn.spines[side].set_visible(False)
    axn.spines["bottom"].set_linewidth(0.4)
    axn.spines["bottom"].set_position(("data", -0.72))
    fig.text(0.042, 0.092,
             u"the OTHER half of the predicate: NPxxY (Å),\n"
             u"Y5.58 OH – Y7.53 OH. Active is BELOW %.3f Å.\n"
             u"Same %s rows, same two arms, its own axis."
             % (B.THR_NPXXY, "{:,}".format(len(cA))),
             ha="left", va="top", fontsize=4.8, color=C_MUTE, linespacing=1.55)

    # --- the sentence the two strips together support --------------------
    apo_act = float(apo["active"].mean())
    cog_act = float(cog["active"].mean())
    fig.text(0.305, 0.196,
             u"Predicate = tilt > %.3f Å AND NPxxY < %.3f Å. Both halves must "
             u"fire, so the AND is stricter than the\nline above: %.1f%% of "
             u"cognate predictions are called active against %.1f%% of apo — "
             u"a %.1f× rate."
             % (B.THR_TILT, B.THR_NPXXY, 100 * cog_act, 100 * apo_act,
                cog_act / apo_act),
             ha="left", va="top", fontsize=6.2, color=C_HEAD, linespacing=1.6)

    # WRAPPED BY HAND. savefig.bbox is "tight": one line wider than the figure
    # silently expands the canvas and squeezes everything else left.
    fig.text(0.305, 0.140,
             u"Filter: %s; n = %s of %s rows. Never excl_any — E3 is a "
             u"property of the receptor's reference and\ndoes not apply to a "
             u"raw distribution. The two cards are single predictions and "
             u"DIFFERENT receptors: the archive\nships one prediction per "
             u"case, so the population, not the two cards, is the "
             u"within-condition contrast. Selection\nrules, cell sizes and "
             u"percentiles are in the caption. Soft focus encodes depth only "
             u"and carries no interpretive\nmeaning. Shows which state is "
             u"REACHED. Does NOT show amplitude reproduction (BA-4, negative "
             u"on 3 of 4\nbackbones) — hence no arrow anywhere and no line "
             u"joining the two card values."
             % (label, "{:,}".format(len(cA)), "{:,}".format(len(rows))),
             ha="left", va="top", fontsize=4.7, color=C_MUTE, linespacing=1.55)

    D.raster_dpi(fig)
    paths = fs.save(fig, "ga_style2_population")

    info = dict(n_apo=s_apo["n"], n_cog=s_cog["n"],
                n_receptors=int(cA["receptor"].nunique()),
                label=label, n_core=len(cA), n_rows=len(rows),
                apo_tilt=float((apo[XCOL] > B.THR_TILT).mean()),
                cog_tilt=float((cog[XCOL] > B.THR_TILT).mean()),
                apo_act=apo_act, cog_act=cog_act,
                pct_apo=pct_apo, pct_cog=pct_cog,
                view=ia["view"] + u" (both cards)",
                omit_apo=ia["omitted"], omit_cog=ic["omitted"])

    print("GA-style2 written:", *paths, sep="\n  ")
    print("  apo      n=%d median %.3f IQR %.3f-%.3f"
          % (s_apo["n"], s_apo["median"], s_apo["q1"], s_apo["q3"]))
    print("  cognate  n=%d median %.3f IQR %.3f-%.3f"
          % (s_cog["n"], s_cog["median"], s_cog["q1"], s_cog["q3"]))
    print("  card apo  %.4f A (row 567)  %s  %.0f%% behind focus  p%.1f"
          % (ia["d_tilt"], ia["view"], 100 * ia["behind_focus"], pct_apo))
    print("  card cog  %.4f A (row 8285) %s  %.0f%% behind focus  p%.1f"
          % (ic["d_tilt"], ic["view"], 100 * ic["behind_focus"], pct_cog))
    print("  tilt>thr  apo %.4f  cognate %.4f"
          % (info["apo_tilt"], info["cog_tilt"]))
    print("  active    apo %.4f  cognate %.4f" % (apo_act, cog_act))
    print("\n" + caption_block(info))


if __name__ == "__main__":
    main()
