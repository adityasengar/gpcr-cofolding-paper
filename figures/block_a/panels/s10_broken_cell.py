"""
S10 - what E1 removes, and why the identity gates did not catch it.

E1 is one line in S1a: 25 rows, 0.3% of the corpus, always excluded. This is
the picture of those 25 rows, beside a comparator from the same receptor and
the same arm on a different backbone, on one camera and one colour rule. The
quantitative panel is c: both cells' pLDDT distributions with the E1 rule drawn
on them, and both rendered rows marked.

The caveat it exists to make visible is C-12: the A1-A6 scorer gates check
sequence identity, chain assignment, reference class and species, and carry no
pLDDT floor at all. Every one of these 25 rows has `passed = True`. Nothing in
the identity gates would have removed a structure whose NPxxY hydroxyls are
26.6 A apart.
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

from ga1_hero import trim                                     # noqa: E402

XCOL = "d_gpcrdb_tm6_tilt_246_637_ca"
YCOL = "d_npxxy_oh"


def cell_panel(fig, gs, png, title, sub, lines, letter):
    ax = fig.add_subplot(gs)
    ax.imshow(trim(os.path.join(B.OUT, png)))
    ax.axis("off")
    ax.set_title(u"%s   %s\n%s" % (letter, title, sub), fontsize=7,
                 loc="left", fontweight="bold")
    y = -0.015
    for text, colour in lines:
        ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="top",
                fontsize=5.0, color=colour, linespacing=1.45)
        y -= 0.055 * (1 + text.count("\n"))
    return ax


def main():
    fs.use_house_style()
    rows = B.rows()
    broken = rows[(rows["receptor"] == "ACM1") & (rows["arm"] == "cognate")
                  & (rows["backbone"] == "protenix")]
    healthy = rows[(rows["receptor"] == "ACM1") & (rows["arm"] == "cognate")
                   & (rows["backbone"] == "chai")]
    rb = broken[broken["row_id"] == 967].iloc[0]
    rh = healthy[healthy["row_id"] == 948].iloc[0]
    e1 = int(rows["excl_E1"].sum())

    fig = plt.figure(figsize=(fs.W2, 108 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 1.12])

    cell_panel(
        fig, gs[0, 0], "s10a_broken_cell.png",
        u"the broken cell — every row of it is E1",
        u"ACM1 · cognate Gα · Protenix · row 967",
        [(u"TM6 tilt  21.55 Å   L67 (2×46) Cα – L367 (6×37) Cα", fs.BLACK),
         (u"NPxxY  26.63 Å   Y208 (5.58) OH – Y418 (7.53) OH", fs.PURPLE),
         (u"pLDDT 38.38 — the median row of its 25-row cell.\n"
          u"Both predicate axes are geometrically meaningless\n"
          u"here; the tilt axis would have fired.", fs.GREY)],
        "a")

    cell_panel(
        fig, gs[0, 1], "s10b_healthy_cell.png",
        u"the comparator — same receptor, same arm",
        u"ACM1 · cognate Gα · Chai-1 · row 948",
        [(u"TM6 tilt  17.17 Å   same atom pair", fs.BLACK),
         (u"NPxxY   4.02 Å   same atom pair", fs.PURPLE),
         (u"pLDDT 69.23 — the highest-pLDDT row of its cell.\n"
          u"Same camera rule, same colour rule; only the\n"
          u"backbone differs.", fs.GREY)],
        "b")

    # --- c: the quantitative panel behind both renders -------------------
    ax = fig.add_subplot(gs[0, 2])
    rng = np.random.RandomState(2)
    ns = []
    for i, (sub, name, colour, marked) in enumerate([
            (broken, "Protenix\n(the E1 cell)", fs.ORANGE, rb),
            (healthy, "Chai-1\n(comparator)", fs.VERM, rh)]):
        v = sub["plddt_mean"].values
        ax.scatter(np.full(len(v), i) + rng.uniform(-0.14, 0.14, len(v)), v,
                   s=10, color=colour, alpha=0.55, linewidths=0, zorder=2)
        ax.plot([i - 0.26, i + 0.26], [np.median(v)] * 2, color=colour,
                lw=1.4, zorder=3, solid_capstyle="butt")
        ax.plot([i - 0.30, i + 0.30], [v.mean()] * 2, color=colour, lw=0.8,
                ls=(0, (2, 1.5)), zorder=3)
        ax.scatter([i], [marked["plddt_mean"]], s=48, facecolors="none",
                   edgecolors=fs.BLACK, linewidths=1.0, zorder=5)
        ax.annotate("row %d" % marked["row_id"], (i, marked["plddt_mean"]),
                    xytext=(10, -7), textcoords="offset points", fontsize=5.2)
        ns.append((i, len(v)))
    ax.set_ylim(30, 78)
    for i, n in ns:
        fs.annotate_n(ax, i, n, y=31.0)
    ax.axhline(50, color=fs.GREY, lw=0.8, ls=(0, (3, 2)), zorder=1)
    ax.text(0.98, 50, u" E1: cell MEAN pLDDT < 50 ", ha="right", va="bottom",
            fontsize=5, color=fs.GREY, transform=ax.get_yaxis_transform())
    ax.set_xticks([0, 1])
    ax.set_xticklabels([u"Protenix\n(the E1 cell)", u"Chai-1\n(comparator)"],
                       fontsize=5.5)
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylabel("mean pLDDT of the prediction")
    ax.set_title(u"c   the rule that removes them, drawn\n"
                 u"      dashed bar = the cell mean E1 tests",
                 fontsize=7, loc="left", fontweight="bold")
    ax.text(0.03, 0.62,
            u"E1 fires on %d rows in the whole corpus (0.3%%), and they are\n"
            u"this one cell. Every one of them has passed = True on the\n"
            u"A1–A6 identity gates, which carry no pLDDT floor (C-12)."
            % e1,
            transform=ax.transAxes, va="top", ha="left", fontsize=5,
            color=fs.BLACK, linespacing=1.5)

    paths = fs.save(fig, "s10_broken_cell")
    print("S10 written:", *paths, sep="\n  ")
    print("  E1 rows corpus-wide: %d; broken cell mean pLDDT %.2f, "
          "comparator %.2f" % (e1, broken["plddt_mean"].mean(),
                               healthy["plddt_mean"].mean()))
    print("  passed=True on all E1 rows:",
          bool(rows[rows["excl_E1"]]["passed"].all()))


if __name__ == "__main__":
    main()
