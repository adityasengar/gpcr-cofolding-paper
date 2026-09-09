"""
LF2 - Leakage, and what is done about it, paper by paper.

Data: the `tags:` line of lit/INDEX.md, copied verbatim from each note and
drawn from SCHEMA.md's fixed vocabulary, mined into data_lit/tags.csv.
All 78 papers carry a tags line, so there are no missing cells.

The nine rows are SCHEMA.md's whole "Rigour" tag group. `oracle-leak` is
pipeline leakage (routes 1-6); `design-level-oracle` is route 7, where the
pipeline is clean but the expected answer was declared before the result was
read. The schema keeps them distinct and so does this panel.
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

RIGOUR = [
    "oracle-leak",
    "design-level-oracle",
    "prospective",
    "anti-memorization",
    "no-anti-memorization",
    "unpowered",
    "confidence-as-discriminator",
    "multi-backbone",
    "experimental-validation",
]
LABEL = {
    "oracle-leak": "oracle-leak  (pipeline, routes 1-6)",
    "design-level-oracle": "design-level-oracle  (route 7)",
    "prospective": "prospective",
    "anti-memorization": "anti-memorization set exists",
    "no-anti-memorization": "no anti-memorization set",
    "unpowered": "unpowered",
    "confidence-as-discriminator": "confidence used as discriminator",
    "multi-backbone": "multi-backbone",
    "experimental-validation": "experimental validation",
}


def main():
    tags = pd.read_csv(os.path.join(DATA, "tags.csv"))
    papers = sorted(tags["citekey"].unique())
    have = {(r.citekey, r.tag) for r in tags.itertuples()}
    codes = np.array([[1 if (p, t) in have else 0 for p in papers]
                      for t in RIGOUR], dtype=int)
    n = len(papers)

    fs.use_house_style()
    fig, ax = fs.figure(fs.W2, 62 * fs.MM)
    cats = [("tag absent", "#E9E9E9"), ("tag present", fs.BLUE)]
    order = sorted(range(n), key=lambda j: (-codes[:, j].sum(),
                                            tuple(-codes[:, j])))
    fp.presence_matrix(ax, codes, [LABEL[t] for t in RIGOUR], cats,
                       col_label="papers, sorted by how many rigour tags they carry",
                       row_total_of="tag present", col_order=order)
    fp.category_legend(ax, cats, bbox=(0.5, -0.20))
    ax.set_title("rigour tags across the corpus, one column per paper",
                 loc="left", pad=3)

    paths = fs.save(fig, "lit2_rigour_landscape")
    print("\n".join(paths))
    print("n papers = %d" % n)
    for i, t in enumerate(RIGOUR):
        print("  %-30s %d" % (t, codes[i].sum()))
    ol = codes[RIGOUR.index("oracle-leak")]
    dl = codes[RIGOUR.index("design-level-oracle")]
    pr = codes[RIGOUR.index("prospective")]
    am = codes[RIGOUR.index("anti-memorization")]
    print("  neither oracle-leak nor design-level-oracle : %d"
          % int(((ol == 0) & (dl == 0)).sum()))
    print("  oracle-leak AND called prospective          : %d"
          % int(((ol == 1) & (pr == 1)).sum()))
    print("  anti-memorization set AND oracle-leak       : %d"
          % int(((am == 1) & (ol == 1)).sum()))


if __name__ == "__main__":
    main()
