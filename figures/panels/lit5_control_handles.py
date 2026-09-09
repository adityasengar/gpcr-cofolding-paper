"""
LF5 - What handle is used to choose the state, and in which system.

Data: the `tags:` line of lit/INDEX.md for all 78 papers (data_lit/tags.csv),
drawn from SCHEMA.md's fixed Method / Protocol / Control tag vocabulary.

The rows are split into two blocks. The upper block is the OPERATOR-SUPPLIED
handles: the state, or a proxy for it, is chosen by whoever runs the method -
a state-annotated template, a state-filtered alignment, a cluster label, a
steering vector, a seed budget. The lower block is the BIOLOGICAL CO-INPUT
handles: something that would occupy the receptor in a cell - a ligand, a
transducer, a peptide, a nanobody - is supplied and the state is whatever
comes out. That split is the distinction claim C4 turns on.

Counts are papers, and the tags overlap, so a paper appears in every cell it
qualifies for and the columns do not sum to 78. Empty cells are drawn absent
rather than as zero.
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

OPERATOR = [
    ("state-annotated-input", "state-annotated input"),
    ("template-state-bias", "state-biased template"),
    ("msa-state-filter", "state-filtered MSA"),
    ("msa-subsample", "MSA subsampling"),
    ("af-cluster", "MSA clustering"),
    ("latent-steering", "latent steering"),
    ("seed-only", "seed / sample budget only"),
    ("directed-state", "directed state (any handle)"),
]
BIOLOGICAL = [
    ("ligand-driven", "ligand"),
    ("partner-driven", "protein partner"),
    ("g-protein-mimetic", "G-protein mimetic"),
    ("peptide-driven", "peptide"),
    ("nanobody", "nanobody"),
    ("apo-sampling", "nothing bound (apo)"),
]
SYSTEMS = [
    ("gpcr", "GPCR"),
    ("kinase", "kinase"),
    ("transporter", "transporter"),
    ("fold-switching", "fold-switching"),
    ("periplasmic-binding", "periplasmic\nbinding"),
    ("general-protein", "general\nprotein"),
]


def main():
    tags = pd.read_csv(os.path.join(DATA, "tags.csv"))
    n_papers = tags["citekey"].nunique()
    by_tag = tags.groupby("tag")["citekey"].apply(set).to_dict()

    rows = [("operator-supplied", t, lab) for t, lab in OPERATOR] + \
           [("biological co-input", t, lab) for t, lab in BIOLOGICAL]
    mat = np.zeros((len(rows), len(SYSTEMS)))
    for i, (_, t, _) in enumerate(rows):
        for j, (s, _) in enumerate(SYSTEMS):
            mat[i, j] = len(by_tag.get(t, set()) & by_tag.get(s, set()))
    labels = ["%s  (%d)" % (lab, len(by_tag.get(t, set())))
              for _, t, lab in rows]
    tab = pd.DataFrame(mat, index=labels,
                       columns=["%s\n(%d)" % (lab, len(by_tag.get(s, set())))
                                for s, lab in SYSTEMS])

    fs.use_house_style()
    fig, ax = fs.figure(fs.W15, 92 * fs.MM)
    fp.matrix(ax, tab, value_label="papers", cmap="Blues", annotate=True,
              vmin=0, zero_is_absent=True)
    # separate the two blocks; the block headers live in the left margin so
    # they cannot sit on top of a cell
    nop, nbio = len(OPERATOR), len(BIOLOGICAL)
    ax.axhline(nop - 0.5, color=fs.BLACK, lw=0.9)
    ax.text(-0.40, 1 - (nop / 2.0) / (nop + nbio), "operator\nsupplies\nthe state",
            transform=ax.transAxes, fontsize=6, fontweight="bold",
            ha="center", va="center", rotation=90, linespacing=1.3)
    ax.text(-0.40, (nbio / 2.0) / (nop + nbio), "a biological\nco-input\nis supplied",
            transform=ax.transAxes, fontsize=6, fontweight="bold",
            ha="center", va="center", rotation=90, linespacing=1.3)
    ax.set_xlabel("system studied (papers carrying the tag)")
    ax.set_title("state handle against system, %d papers, tags overlap"
                 % n_papers, loc="left", pad=4)

    paths = fs.save(fig, "lit5_control_handles")
    print("\n".join(paths))
    print(tab.astype(int).to_string())
    gp = by_tag.get("gpcr", set())
    bio = set()
    for t, _ in BIOLOGICAL:
        bio |= by_tag.get(t, set())
    op = set()
    for t, _ in OPERATOR:
        op |= by_tag.get(t, set())
    print("papers = %d" % n_papers)
    print("GPCR papers                                   : %d" % len(gp))
    print("GPCR + any biological co-input handle         : %d" % len(gp & bio))
    print("GPCR + any operator-supplied handle           : %d" % len(gp & op))
    print("GPCR + peptide-driven                         : %d"
          % len(gp & by_tag.get("peptide-driven", set())))
    print("GPCR + g-protein-mimetic                      : %d"
          % len(gp & by_tag.get("g-protein-mimetic", set())))
    print("papers with no state handle tag at all        : %d"
          % (n_papers - len(op | bio)))


if __name__ == "__main__":
    main()
