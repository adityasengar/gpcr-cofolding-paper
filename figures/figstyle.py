"""
House style for every figure in this manuscript.

One place decides sizes, fonts, colours and output format, so that panels made
months apart by different scripts still look like they belong to one paper.
Import this before doing anything else with matplotlib.

The numbers here are Nature Communications submission specs:
  - column widths 88 mm (single) / 180 mm (double); 170 mm max height
  - sans-serif type, 5-7 pt, nothing below 5 pt after reduction
  - line weights at or above 0.25 pt
  - vector PDF for submission, 600 dpi PNG for looking at on screen

Palette is Okabe-Ito, which stays distinguishable under all three common forms
of colour blindness. Do not add colours to it without checking that.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

MM = 1 / 25.4                     # mm -> inches

# --- canvas sizes -----------------------------------------------------------
W1  = 88  * MM                    # single column
W15 = 120 * MM                    # one and a half
W2  = 180 * MM                    # double column / full width
HMAX = 170 * MM                   # tallest a figure may be on one page

# --- Okabe-Ito, colour-blind safe ------------------------------------------
BLACK   = "#000000"
ORANGE  = "#E69F00"
SKY     = "#56B4E9"
GREEN   = "#009E73"
YELLOW  = "#F0E442"
BLUE    = "#0072B2"
VERM    = "#D55E00"
PURPLE  = "#CC79A7"
GREY    = "#999999"
PALETTE = [BLUE, VERM, GREEN, ORANGE, SKY, PURPLE, YELLOW, BLACK]

# Fixed meanings, so a colour means the same thing in every panel of the paper.
# Anything not listed falls through to PALETTE in order.
PARTNER_COLOURS = {
    "apo":            GREY,
    "ligand":         SKY,
    "antagonist":     BLUE,
    "α5_ct_fragment": VERM,
    "α5_ct_variant":  ORANGE,
    "cognate_ga":     GREEN,
    "shuffled_ga":    PURPLE,
    "decoy_scaffold": BLACK,
}
STATE_COLOURS = {"active": VERM, "inactive": BLUE, "borderline": GREY}

# Block A encodings. Four backbones and two arms recur in almost every Block A
# panel, so they get fixed colours for the same reason the partner arms do: a
# reader who has learnt "green = OpenFold-3" in figure 2 must not have to relearn
# it in figure 5.
BACKBONE_COLOURS = {
    "boltz":    BLUE,
    "chai":     VERM,
    "of3":      GREEN,
    "protenix": ORANGE,
}
BACKBONE_ORDER = ["boltz", "chai", "of3", "protenix"]
BACKBONE_LABELS = {"boltz": "Boltz-2", "chai": "Chai-1",
                   "of3": "OpenFold-3", "protenix": "Protenix"}

ARM_COLOURS = {"apo": GREY, "cognate": GREEN}
ARM_LABELS  = {"apo": "apo", "cognate": "cognate Gα"}

# Reference-set predicate outcomes (BA-1). `unclassified` is deliberately a
# neutral grey and NOT folded into a named class: 5 of the 9 deviations in
# reference_predicates.csv carry no classification, and an encoding that hid
# that would hide the majority of the thing the panel exists to show.
DEVIATION_COLOURS = {
    "expected_biology":                   GREEN,
    "curation_error":                     VERM,
    "measurement_artifact":               PURPLE,
    "curation_error_or_expected_biology": ORANGE,
    "unclassified":                       GREY,
}
DEVIATION_MARKERS = {
    "expected_biology":                   "^",
    "curation_error":                     "s",
    "measurement_artifact":               "D",
    "curation_error_or_expected_biology": "P",   # compound label, own slot
    "unclassified":                       "X",
}
DEVIATION_ORDER = ["unclassified", "curation_error", "expected_biology",
                   "measurement_artifact", "curation_error_or_expected_biology"]


def _sans():
    """Pick the best sans face actually installed, rather than hoping."""
    have = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Helvetica", "Arial", "Helvetica Neue", "DejaVu Sans"):
        if name in have:
            return name
    return "sans-serif"


def use_house_style():
    """Apply the style globally. Call once, at the top of a figure script."""
    plt.rcParams.update({
        "font.family":       _sans(),
        "font.size":         7,
        "axes.labelsize":    7,
        "axes.titlesize":    7,
        "xtick.labelsize":   6,
        "ytick.labelsize":   6,
        "legend.fontsize":   6,
        "figure.titlesize":  8,

        "axes.linewidth":    0.5,
        "grid.linewidth":    0.4,
        "lines.linewidth":   0.9,
        "lines.markersize":  2.5,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.major.size":  2.5,
        "ytick.major.size":  2.5,
        "xtick.direction":   "out",
        "ytick.direction":   "out",

        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.grid":         False,
        "legend.frameon":    False,
        "figure.facecolor":  "white",
        "savefig.facecolor": "white",

        # Keep text as text in the PDF so the typesetter can restyle it.
        "pdf.fonttype":      42,
        "ps.fonttype":       42,
        "svg.fonttype":      "none",
        "savefig.bbox":      "tight",
        "savefig.pad_inches": 0.01,
    })


def figure(width=W1, height=None, **kw):
    """A figure at a legal width. height defaults to a 3:2 panel."""
    if height is None:
        height = width * 2 / 3
    if height > HMAX:
        raise ValueError(
            "%.0f mm exceeds the 170 mm page limit; split the figure instead"
            % (height / MM))
    return plt.subplots(figsize=(width, height), constrained_layout=True, **kw)


def panel_label(ax, letter, dx=-0.16, dy=1.06):
    """Bold lower-case panel letter, Nature house position."""
    ax.text(dx, dy, letter, transform=ax.transAxes,
            fontsize=8, fontweight="bold", va="top", ha="left")


def annotate_n(ax, x, n, y=None, fmt="n=%d"):
    """
    Print the count behind a mark.

    Not decoration. 18 of the 232 structure renders in our corpus, and a long
    tail of the bar charts, were flagged in `hides` precisely because the
    reader cannot tell whether a mark stands on 500 observations or on one.
    """
    if y is None:
        y = ax.get_ylim()[0]
    ax.annotate(fmt % n, (x, y), xytext=(0, 2), textcoords="offset points",
                ha="center", va="bottom", fontsize=5, color=GREY)


def save(fig, stem, outdir=None, formats=("pdf", "png")):
    """
    Write the figure to figures/out/<stem>.<ext> and return the paths.

    PDF is the submission artefact; PNG at 600 dpi is for looking at.
    """
    if outdir is None:
        outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(outdir, exist_ok=True)
    paths = []
    for ext in formats:
        p = os.path.join(outdir, "%s.%s" % (stem, ext))
        fig.savefig(p, dpi=600 if ext == "png" else None)
        paths.append(p)
    plt.close(fig)
    return paths
