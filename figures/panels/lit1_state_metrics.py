"""
LF1 - How prior work decides which conformational state it got.

Data: lit/notes/*.md `state_metric`, mined by mine_corpus.py and classified
against SCHEMA.md's own four-value vocabulary by classify_corpus.py.
All 78 papers; every assignment is traceable through data_lit/metric_kinds.csv,
which carries the note text the rule fired on.
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

KINDS = ["binary predicate", "continuous coordinate", "RMSD-to-reference",
         "visual only"]
ROWS = KINDS + ["no state metric of any kind"]


def main():
    df = pd.read_csv(os.path.join(DATA, "metric_kinds.csv"))
    df["no state metric of any kind"] = df["no state metric"]
    n = len(df)

    fs.use_house_style()
    fig, (ax_a, ax_b) = fs.figure(fs.W2, 95 * fs.MM, nrows=2,
                                  gridspec_kw={"height_ratios": [1.0, 0.85]})

    counts = [int(df[r].sum()) for r in ROWS]
    fp.count_dots(ax_a, ROWS, counts, n,
                  highlight=["visual only", "no state metric of any kind"])
    ax_a.set_xlim(0, n * 1.08)
    ax_a.set_xticks([0, 20, 40, 60, n])
    ax_a.set_title("how the state is called, across the whole corpus",
                   loc="left", pad=3)
    fs.panel_label(ax_a, "a", dx=-0.28)

    codes = np.array([df[r].values for r in ROWS], dtype=int)
    # papers that call a state first, most kinds first, then by pattern; the
    # papers that never call a state at all form the block on the right
    nk = df[KINDS].sum(axis=1).values
    order = sorted(range(len(df)),
                   key=lambda j: (-int(nk[j] > 0), -nk[j],
                                  tuple(-codes[:, j])))
    fp.presence_matrix(
        ax_b, codes, ROWS,
        categories=[("not used", "#E9E9E9"), ("used", fs.BLUE)],
        col_label="papers, sorted by how many kinds co-occur",
        row_total_of="used", col_order=order)
    fp.category_legend(ax_b, [("not used", "#E9E9E9"), ("used", fs.BLUE)],
                       bbox=(0.5, -0.16))
    ax_b.set_title("the same 78 papers, one column each", loc="left", pad=3)
    fs.panel_label(ax_b, "b", dx=-0.28)

    paths = fs.save(fig, "lit1_state_metrics")
    print("\n".join(paths))
    print("n papers = %d" % n)
    for r, c in zip(ROWS, counts):
        print("  %-30s %d" % (r, c))
    print("  papers using >= 2 kinds       %d"
          % int((df[KINDS].sum(axis=1) >= 2).sum()))
    print("  papers using >= 3 kinds       %d"
          % int((df[KINDS].sum(axis=1) >= 3).sum()))


if __name__ == "__main__":
    main()
