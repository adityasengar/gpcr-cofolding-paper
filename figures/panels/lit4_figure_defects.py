"""
LF4 - The corpus's own figure-defect landscape.

Data: the `## F. Figures` table of all 78 notes - 1,226 panel-group rows -
mined by mine_corpus.py. `hides` is filled only where a figure obscures its
own result, so a blank cell means no defect was recorded. The defect classes
in panel b are keyword rules over that text; rows matching no rule are kept as
`other / uncategorised` rather than dropped, so panel b's parts sum to more
than 968 only through rows carrying several defects at once, never less.

This is the figure the house rules in figpanels.py were written from, so it
belongs in the paper as the justification for them.
"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import figstyle as fs
import figpanels as fp

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data_lit")

CLASSES = ["hand-picked or k-of-N example, rule unstated",
           "n or counts not shown",
           "axis broken, truncated or pinned",
           "axes not comparable across panels",
           "bar or mean standing in for a distribution",
           "no dispersion, error bar, CI or test",
           "pooled where per-system was needed",
           "two measures on one axis",
           "claim with no quantitative panel",
           "oracle-selected model displayed",
           "failures not shown beside successes",
           "other / uncategorised"]
# barh puts index 0 at the bottom, so list the forms bottom-up
FORM_ORDER = ["form not parsed", "TREE", "SCHEMATIC", "MATRIX", "PLOT", "RENDER"]


def main():
    fd = pd.read_csv(os.path.join(DATA, "figdefects.csv"))
    tags = pd.read_csv(os.path.join(DATA, "tags.csv"))
    fd["form"] = fd["form"].replace({"unclassified": "form not parsed"})
    fd["defect"] = np.where(fd["has_defect"] == 1,
                            "a defect is recorded", "none recorded")
    forms = [f for f in FORM_ORDER if f in set(fd["form"])]
    n_rows = len(fd)
    n_def = int(fd["has_defect"].sum())

    fs.use_house_style()
    fig, (ax_a, ax_b, ax_c) = fs.figure(
        fs.W2, 130 * fs.MM, nrows=3,
        gridspec_kw={"height_ratios": [0.75, 1.25, 0.9]})

    # a - how often each figure form hides its own result
    fp.state_composition(ax_a, fd, "form", "defect", order=forms,
                         state_order=["a defect is recorded", "none recorded"],
                         colours={"a defect is recorded": fs.VERM,
                                  "none recorded": "#E9E9E9"},
                         horizontal=True)
    ax_a.legend(loc="upper center", bbox_to_anchor=(0.5, -0.34), ncol=2,
                frameon=False, fontsize=5.5, handlelength=1.0)
    ax_a.set_xlabel("fraction of panel-group rows")
    ax_a.set_title("a defect is recorded for %d of %d panel-group rows, "
                   "by figure form" % (n_def, n_rows), loc="left", pad=3)
    fs.panel_label(ax_a, "a", dx=-0.13)

    # b - which defects
    counts = [int(fd[c].sum()) for c in CLASSES]
    fp.count_dots(ax_b, CLASSES, counts, n_def,
                  colours={"other / uncategorised": fs.GREY},
                  highlight=["hand-picked or k-of-N example, rule unstated",
                             "claim with no quantitative panel"])
    ax_b.set_xlim(0, n_def * 1.05)
    ax_b.set_xticks([0, 200, 400, 600, 800, n_def])
    ax_b.set_xlabel("panel-group rows (of %d carrying a recorded defect)" % n_def)
    ax_b.set_title("which defect, over the rows that carry one "
                   "(a row may carry several)", loc="left", pad=3)
    fs.panel_label(ax_b, "b", dx=-0.13)

    # c - is it a few bad papers, or the field? one point per paper, and an
    # ECDF rather than a violin because the measure is a bounded fraction and
    # a kernel density would put visible mass outside [0, 1].
    venue = {}
    for r in tags.itertuples():
        if r.tag in ("preprint", "peer-reviewed"):
            venue[r.citekey] = r.tag
    per = (fd.groupby("citekey")["has_defect"]
             .agg(["mean", "size"]).reset_index())
    per["fraction of a paper's own panel groups with a recorded defect"] = per["mean"]
    per["venue"] = per["citekey"].map(venue).fillna("venue not recorded")
    fp.ecdf(ax_c, per, "venue",
            "fraction of a paper's own panel groups with a recorded defect",
            order=["peer-reviewed", "preprint"],
            colours={"peer-reviewed": fs.BLUE, "preprint": fs.GREEN})
    ax_c.set_xlim(0, 1)
    ax_c.legend(loc="upper left", frameon=False, fontsize=5.5)
    ax_c.set_title("per paper, not pooled - one paper per step", loc="left",
                   pad=3)
    fs.panel_label(ax_c, "c", dx=-0.13)

    paths = fs.save(fig, "lit4_figure_defects")
    print("\n".join(paths))
    print("panel-group rows = %d over %d papers"
          % (n_rows, fd["citekey"].nunique()))
    for f in forms:
        sub = fd[fd["form"] == f]
        print("  %-13s %4d of %4d" % (f, int(sub["has_defect"].sum()), len(sub)))
    print("rows with a recorded defect = %d" % n_def)
    for c, k in zip(CLASSES, counts):
        print("  %-38s %4d" % (c, k))
    print("median within-paper defect rate = %.2f (n=%d papers)"
          % (per["mean"].median(), len(per)))


if __name__ == "__main__":
    main()
