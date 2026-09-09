"""
F1 - the workflow: what is measured, on what, and where every row goes.

Venue norm decided this one. In the corpus's Nature Communications papers,
Figure 1 is a pipeline schematic in 4 of 4 cases; the corpus is 11% schematic
overall and this figure set had none. A pipeline is also the safe form for this
particular claim, because a pipeline makes no amplitude assertion: there is no
arrow labelled "activation" anywhere in it, and no magnitude is drawn.

  a  the two predicates. The atom pairs are named here ONCE, authoritatively,
     for the whole paper, with the threshold and the direction of each rule.
     The field's characteristic failure on this claim is a displacement drawn
     as an arrow and measured nowhere; its mirror is a number printed with no
     atom pair. This panel is the fix for both, and every other panel in the
     paper measures the same two pairs.
  b  the 168 deposited references scored on those two axes - the instrument
     tested on structures whose state is already known, before it is pointed
     at a single prediction.
  c  the design: 48 receptors x 2 arms x 4 backbones x 25 seeds, and what is
     and is not recorded about how they were run.
  d  where the 9,490 rows go: the exclusions, the class split, and the
     predicate call.

Population: 01_rows/block_a_rows.csv (all 9,490 rows; the panel is about where
they go, so nothing is filtered before panel d says so) and
02_references/reference_predicates.csv (all 168).
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
from matplotlib.patches import FancyBboxPatch, Rectangle      # noqa: E402

C_TILT = fs.BLACK
C_NPXXY = fs.PURPLE


def box(ax, x, y, w, h, text, fc="white", ec=fs.GREY, fontsize=5.2,
        weight="normal", tc=fs.BLACK, lw=0.6, align="center"):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2))
    ax.text(x + (w / 2.0 if align == "center" else 0.012),
            y + h / 2.0, text, ha=align if align != "center" else "center",
            va="center", fontsize=fontsize, color=tc, fontweight=weight,
            zorder=3, linespacing=1.35)


def flow(ax, x0, y0, x1, y1, colour=fs.GREY, lw=0.7):
    """A plain connector. Deliberately not an annotated arrow: an arrow that
    carries a word carries a claim, and the only claims this figure makes are
    the counts printed in its boxes."""
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=colour, lw=lw,
                                shrinkA=1.5, shrinkB=1.5,
                                mutation_scale=6), zorder=1)


def panel_a(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title(u"a   the two predicates, and the atoms they are measured "
                 u"between", fontsize=7, loc="left", fontweight="bold")

    box(ax, 0.02, 0.70, 0.96, 0.28,
        u"TM6 tilt   d( L2×46 Cα , L6×37 Cα )   >  14.932 Å\n"
        u"the two Cα that open as TM6 swings out; GPCRdb generic numbering, "
        u"one residue pair per receptor",
        fc="#f4f4f4", ec=C_TILT, tc=C_TILT, fontsize=5.6, align="left")
    box(ax, 0.02, 0.40, 0.96, 0.26,
        u"NPxxY     d( Y5.58 OH , Y7.53 OH )   <  9.080 Å\n"
        u"the two hydroxyls that pack together as the NPxxY motif rearranges",
        fc="#faf2f7", ec=C_NPXXY, tc=C_NPXXY, fontsize=5.6, align="left")
    ax.text(0.02, 0.33,
            u"Class A: active when BOTH rules fire.   Class B substitutes a TM6 "
            u"kink angle < 159.95° for the NPxxY rule; Class F uses tilt alone.",
            fontsize=5.0, color=fs.BLACK, va="top", ha="left")
    ax.text(0.02, 0.24,
            u"Both thresholds are panel constants, identical on all 9,490 "
            u"rows. Worked examples of the pairs: ADRB2 L75/L275 and Y219/Y326 · "
            u"AA2AR L48/L235 and\nY197/Y288 · DRD2 L76/L375 and Y209/Y426 · "
            u"ACM1 L67/L367 and Y208/Y418. Each was verified by reproducing "
            u"the value stored for that structure\nfrom its own coordinates; "
            u"three of the archive's ALIGNMENT.md files name different "
            u"residues and do not reproduce (DISCREPANCY_REPORT D13).",
            fontsize=4.5, color=fs.GREY, va="top", ha="left", linespacing=1.5)


def panel_b(ax, rp):
    sub = rp[rp["d_tilt_ref"].notna()].copy()
    has_y = sub["d_npxxy_oh_ref"].notna()
    ax.axhline(B.THR_NPXXY, color=fs.GREY, lw=0.6, ls=(0, (2.5, 2)), zorder=0)
    ax.axvline(B.THR_TILT, color=fs.GREY, lw=0.6, ls=(0, (2.5, 2)), zorder=0)
    for state, mk in (("active", "^"), ("inactive", "s")):
        m = has_y & (sub["state"] == state)
        ax.scatter(sub["d_tilt_ref"][m], sub["d_npxxy_oh_ref"][m], marker=mk,
                   s=13, facecolors="none",
                   edgecolors=fs.VERM if state == "active" else fs.BLUE,
                   linewidths=0.6, zorder=3,
                   label="%s reference (n=%d)" % (state, int(m.sum())))
    rug = sub[~has_y]
    y0 = 1.2
    for state, mk in (("active", "^"), ("inactive", "s")):
        m = rug["state"] == state
        ax.scatter(rug["d_tilt_ref"][m], np.full(int(m.sum()), y0),
                   marker="|", s=16, linewidths=0.5,
                   color=fs.VERM if state == "active" else fs.BLUE,
                   alpha=0.75, zorder=3)
    ax.text(0.985, 0.01,
            u"no NPxxY-OH value (n=%d, drawn as a rug)" % len(rug),
            transform=ax.transAxes, ha="right", va="bottom", fontsize=4.5,
            color=fs.GREY, zorder=6,
            bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none",
                      alpha=0.9))
    ax.set_xlim(10.3, 20.0)
    ax.set_ylim(0.4, 26.0)
    ax.set_xlabel(u"TM6 tilt (Å)")
    ax.set_ylabel(u"NPxxY-OH (Å)")
    ax.legend(loc="center right", fontsize=4.8, handlelength=1.0,
              labelspacing=0.2, borderpad=0.2)
    ax.set_title(u"b   %d references of known state" % len(sub),
                 fontsize=7, loc="left", fontweight="bold", pad=3)
    return len(sub), int(has_y.sum()), len(rug)


def panel_c(ax, df):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.0, 1.0, u"c   what was run", fontsize=7, ha="left", va="top",
            fontweight="bold", transform=ax.transAxes)
    n_rec = df["receptor"].nunique()
    cls = df.groupby("gpcr_class")["receptor"].nunique().to_dict()
    cells = df["cell_id"].nunique()

    box(ax, 0.01, 0.62, 0.21, 0.24,
        u"%d receptors\n%d A · %d B · %d F"
        % (n_rec, cls.get("A", 0), cls.get("B", 0), cls.get("F", 0)),
        fc="#eef4f8", ec=fs.BLUE)
    box(ax, 0.27, 0.62, 0.21, 0.24,
        u"2 arms\napo   ·   cognate Gα", fc="#eef8f2", ec=fs.GREEN)
    box(ax, 0.53, 0.62, 0.21, 0.24,
        u"4 backbones\nBoltz-2 · Chai-1\nOpenFold-3 · Protenix",
        fc="#fdf4e8", ec=fs.ORANGE)
    box(ax, 0.79, 0.62, 0.20, 0.24, u"25 seeds\nper cell", fc="#f6f6f6")
    for x in (0.22, 0.48, 0.74):
        flow(ax, x, 0.74, x + 0.05, 0.74)

    box(ax, 0.01, 0.30, 0.98, 0.20,
        u"%d nominal cells,  %d run  (4 absent: FZD4 cognate on all four "
        u"backbones),  %s rows of a nominal %s"
        % (n_rec * 2 * 4, cells,
           "{:,}".format(len(df)), "{:,}".format(n_rec * 2 * 4 * 25)),
        fc="white", ec=fs.BLACK, fontsize=5.4, weight="bold")

    ax.text(0.01, 0.22,
            u"Recorded per row and used here: input SHA-256, the launcher and "
            u"inner seed, the scorer's git SHA and version, and the A1–A6\n"
            u"identity gates. NOT recorded per row: template usage — the "
            u"archive's SC-9 asserts templates were off on all four backbones "
            u"from\nlauncher static analysis, source defaults and a 5/5 "
            u"propagation test, but there is no row-level echo — and no MSA "
            u"setting appears\nin the drop at all. No reference structure is "
            u"supplied to any prediction; references enter only at scoring.",
            fontsize=4.6, color=fs.BLACK, va="top", ha="left", linespacing=1.5)


def panel_d(ax, df):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.0, 1.0, u"d   where every row goes", fontsize=7, ha="left",
            va="top", fontweight="bold", transform=ax.transAxes)
    n = len(df)
    e1 = int(df["excl_E1"].sum())
    e2 = int(df["excl_E2"].sum())
    core = df[~(df["excl_E1"] | df["excl_E2"])]
    by_class = core.groupby("gpcr_class").size().to_dict()
    act = int(core["active"].sum())
    ina = int((~core["active"]).sum())
    cA = core[core["gpcr_class"] == "A"]
    rates = cA.groupby("arm")["active"].mean().to_dict()

    box(ax, 0.02, 0.74, 0.30, 0.16, u"%s predictions" % "{:,}".format(n),
        fc="white", ec=fs.BLACK, fontsize=5.8, weight="bold")
    box(ax, 0.40, 0.74, 0.56, 0.16,
        u"always excluded: E1 broken cell %d rows · E2 impossible geometry "
        u"%d rows\nE3/E4/E5 are scope flags, not quality flags, and are "
        u"applied per panel" % (e1, e2),
        fc="#f6f6f6", ec=fs.GREY, fontsize=4.9)
    flow(ax, 0.32, 0.82, 0.40, 0.82)

    box(ax, 0.02, 0.52, 0.30, 0.16,
        u"%s scored rows" % "{:,}".format(len(core)), fc="white",
        ec=fs.BLACK, fontsize=5.8, weight="bold")
    flow(ax, 0.17, 0.74, 0.17, 0.68)

    xs = [0.44, 0.62, 0.80]
    for x, (k, lab) in zip(xs, [("A", "Class A"), ("B", "Class B"),
                                ("F", "Class F")]):
        box(ax, x, 0.52, 0.16, 0.16,
            u"%s\n%s rows" % (lab, "{:,}".format(by_class.get(k, 0))),
            fc="#eef4f8" if k == "A" else "#f6f6f6",
            ec=fs.BLUE if k == "A" else fs.GREY, fontsize=5.0)
    flow(ax, 0.32, 0.60, 0.44, 0.60)

    box(ax, 0.02, 0.28, 0.30, 0.16,
        u"predicate: ACTIVE\n%s rows" % "{:,}".format(act),
        fc="#fdf0e8", ec=fs.VERM, tc=fs.VERM, fontsize=5.2, weight="bold")
    box(ax, 0.36, 0.28, 0.30, 0.16,
        u"predicate: INACTIVE\n%s rows" % "{:,}".format(ina),
        fc="#eaf1f7", ec=fs.BLUE, tc=fs.BLUE, fontsize=5.2, weight="bold")
    flow(ax, 0.14, 0.52, 0.14, 0.44)
    flow(ax, 0.20, 0.52, 0.48, 0.44)

    ax.text(0.02, 0.20,
            u"Within Class A the predicate fires on %.1f%% of apo rows and "
            u"%.1f%% of cognate rows. That contrast is the result; this figure "
            u"only\nestablishes the instrument and the population it is "
            u"applied to. The predicate is never given a reference structure — "
            u"it is a rule\nover two distances measured on the prediction "
            u"itself, and the references in b are used to check the rule, not "
            u"to make the call."
            % (100 * rates.get("apo", np.nan), 100 * rates.get("cognate", np.nan)),
            fontsize=4.6, color=fs.BLACK, va="top", ha="left", linespacing=1.5)
    return dict(n=n, e1=e1, e2=e2, core=len(core), active=act, inactive=ina,
                by_class=by_class, rates=rates)


def main():
    fs.use_house_style()
    df = B.rows()
    rp = B.load("02_references/reference_predicates.csv")

    fig = plt.figure(figsize=(fs.W2, 172 * fs.MM), constrained_layout=True)
    fig.set_constrained_layout_pads(h_pad=0.05, hspace=0.06)
    gs = fig.add_gridspec(3, 3, height_ratios=[0.84, 1.05, 1.02],
                          width_ratios=[1.0, 1.0, 1.0])

    panel_a(fig.add_subplot(gs[0, :]))
    nb = panel_b(fig.add_subplot(gs[1, 0]), rp)
    panel_c(fig.add_subplot(gs[1, 1:]), df)
    stats = panel_d(fig.add_subplot(gs[2, :]), df)

    paths = fs.save(fig, "f1_workflow")
    print("F1 written:", *paths, sep="\n  ")
    print("  references drawn: %d total, %d with both axes, %d on the rug" % nb)
    print("  flow:", stats)


if __name__ == "__main__":
    main()
