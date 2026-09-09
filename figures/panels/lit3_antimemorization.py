"""
LF3 - A held-out set existing is not the same as a control arm being run.

Data: lit/notes/*.md fields `anti_memorization_design` and
`anti_memorization_control`, mined by mine_corpus.py and classified from each
field's opening verdict by classify_corpus.py. All 78 papers; the classifier
leaves nothing unclassified and data_lit/antimem.csv carries the note text
each rule fired on.

SCHEMA.md v3 split these two fields apart precisely because v1 could not
record "they had post-cutoff structures and never ran them as a control". This
figure is that distinction, counted.

Cells with no papers are drawn as absent rather than as a zero, because an
empty combination and a combination that occurred zero times after being
looked for mean different things on a design grid.
"""
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import figstyle as fs
import figpanels as fp

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data_lit")

# strongest first on both axes, so the top-left corner is the good corner
DESIGN = ["held-out or post-cutoff set exists", "partial / weak", "none",
          "not reported", "not applicable (nothing trained)"]
CONTROL = ["run and analysed", "run but unpowered", "partial", "none run",
           "not reported", "not applicable (nothing trained)"]
SHORT_D = {"held-out or post-cutoff set exists": "held-out / post-cutoff\nset exists",
           "partial / weak": "partial or weak",
           "none": "none",
           "not reported": "not reported",
           "not applicable (nothing trained)": "not applicable\n(nothing trained)"}
SHORT_C = {"run and analysed": "run and\nanalysed",
           "run but unpowered": "run but\nunpowered",
           "partial": "run in one arm,\nnot in another",
           "none run": "none run",
           "not reported": "not\nreported",
           "not applicable (nothing trained)": "not applicable\n(nothing trained)"}


def main():
    df = pd.read_csv(os.path.join(DATA, "antimem.csv"))
    n = len(df)
    tab = (pd.crosstab(df["design_class"], df["control_class"])
             .reindex(index=DESIGN, columns=CONTROL)
             .fillna(0))
    tab.index = [SHORT_D[i] for i in tab.index]
    tab.columns = [SHORT_C[c] for c in tab.columns]

    fs.use_house_style()
    fig, ax = fs.figure(fs.W15, 68 * fs.MM)
    fp.matrix(ax, tab, value_label="papers", cmap="Blues", annotate=True,
              vmin=0, zero_is_absent=True)
    ax.set_xlabel("was a control arm actually run and analysed?")
    ax.set_ylabel("does a held-out or post-cutoff set exist?")
    ax.set_title("anti-memorization: design against control (n=%d papers)" % n,
                 loc="left", pad=4)

    paths = fs.save(fig, "lit3_antimemorization")
    print("\n".join(paths))
    print(tab.astype(int).to_string())
    print("total = %d" % int(tab.values.sum()))
    got_set = df["design_class"] == "held-out or post-cutoff set exists"
    never = df["control_class"].isin(["none run"])
    print("set exists but no control arm run : %d" % int((got_set & never).sum()))
    print("no control arm run, any design    : %d" % int(never.sum()))
    print("run and analysed, any design      : %d"
          % int((df["control_class"] == "run and analysed").sum()))


if __name__ == "__main__":
    main()
