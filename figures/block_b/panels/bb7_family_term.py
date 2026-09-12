# -*- coding: utf-8 -*-
"""BB-7 — the per-backbone correct-family term, with its intervals.

Exists because results.tex reports the per-backbone family shares (14.2 / 22.9 /
23.6 / 10.9 %) and, after the 2026-09-10 BB-2 rebuild, NO figure in either
document draws them. A number in prose with no panel is exactly the defect this
project's own corpus survey criticises in the published literature.

Claim: SC-B-2. The claim sheet states "17.4 / 17.5 / 20.9 / 17.5, all four agree".
The shipped file says otherwise, and the first of those four is the PANEL share,
not Boltz's. Drawn here rather than argued: three of four per-backbone intervals
cross zero, so the family term is signed on OpenFold-3 alone.

    python3 block_b/panels/bb7_family_term.py   -> out/bb7_family_term.{pdf,png}
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pandas as pd
import figstyle as fs
import figpanels as fp

FRAME, SCALE = "reproduction_36", "logit"
NICE = {"boltz": "Boltz-2", "chai": "Chai-1", "of3": "OpenFold-3",
        "protenix": "Protenix", "panel": "panel"}
def _root():
    """Walk up until data/ is found, rather than counting directory levels --
    this script sits three deep and a miscount fails silently at import time."""
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "data")):
            return d
        d = os.path.dirname(d)
    raise RuntimeError("could not locate the repo root from %s" % __file__)


SRC = os.path.join(_root(), "data/block_b/05_decomposition/ladder_decomposition.csv")


def main():
    d = pd.read_csv(SRC)
    d = d[(d.frame == FRAME) & (d.scale == SCALE)
          & (d.contrast.str.contains("correct_family"))]
    order = ["boltz", "chai", "of3", "protenix", "panel"]
    d = d.set_index("backbone").reindex([o for o in order if o in set(d.backbone)
                                         | set(d.index)]).dropna(subset=["term_estimate"])

    labels, est, lo, hi, cols = [], [], [], [], []
    for bb in d.index:
        share = d.loc[bb, "term_share"] * 100.0
        labels.append("%s  (%.1f%%)" % (NICE.get(bb, bb), share))
        est.append(d.loc[bb, "term_estimate"])
        lo.append(d.loc[bb, "ci_lo"]); hi.append(d.loc[bb, "ci_hi"])
        signed = d.loc[bb, "ci_lo"] > 0
        cols.append(fs.BLACK if bb == "panel" else (fs.GREEN if signed else fs.GREY))

    fig, ax = fs.figure(fs.W2, 0.46 * fs.W2)
    # fs.save() writes without bbox_inches="tight", so a fig.text at negative y is
    # clipped off the canvas entirely -- it does not shrink the figure, it vanishes.
    # Reserve the space explicitly instead of trusting the layout engine.
    fig.set_constrained_layout(False)
    fig.subplots_adjust(left=0.26, right=0.98, top=0.90, bottom=0.34)
    fp.forest(ax, labels, est, lo, hi, colours=cols, null=0.0,
              null_label="no family effect",
              xlabel="correct-family term, shuffled $\\rightarrow$ cognate (logit)")
    ax.set_title("the correct-family term, per backbone", loc="left")
    # Protenix's upper bound is 5.15 and flattens every other interval if drawn in
    # full. Clip the VIEW, never the data, and mark the clip so it cannot be misread.
    hi_clip = 2.0
    if max(hi) > hi_clip:
        ax.set_xlim(min(min(lo), -0.4), hi_clip)
        over = [NICE.get(b, b) for b, h in zip(d.index, hi) if h > hi_clip]
        ax.annotate("%s upper bound %.2f, beyond axis" % (over[0], max(hi)),
                    xy=(hi_clip, list(d.index).index(over[0].lower()[:4]) if False else 0),
                    xytext=(hi_clip * 0.62, -0.55), fontsize=5.4, color=fs.GREY,
                    annotation_clip=False)

    n_signed = sum(1 for a, b in zip(lo, labels) if a > 0 and "panel" not in b)
    note = ("Block B, frame %s, logit scale, from 05_decomposition/ladder_decomposition.csv. "
            "Grey = interval crosses zero; green = excludes it. %d of 4 backbones sign the "
            "term; the panel-level estimate does. The claim sheet's SC-B-2 reports per-backbone "
            "shares of 17.4 / 17.5 / 20.9 / 17.5 and calls them agreeing; the shipped shares are "
            "%s, and 17.4 is the PANEL share, not Boltz's. This panel exists because after the "
            "BB-2 rebuild these numbers appear in prose and in no figure."
            % (FRAME, n_signed,
               " / ".join("%.1f" % (d.loc[b, "term_share"] * 100) for b in d.index if b != "panel")))
    fig.text(0.012, 0.175, "\n".join(__import__("textwrap").wrap(note, 150)),
             fontsize=5.4, color=fs.GREY, va="top", ha="left")

    p = fs.save(fig, "bb7_family_term")
    print("BB-7 ->", p[0])
    for bb in d.index:
        print("   %-9s %+.3f [%+.3f, %+.3f]  share %.1f%%"
              % (bb, d.loc[bb, "term_estimate"], d.loc[bb, "ci_lo"],
                 d.loc[bb, "ci_hi"], d.loc[bb, "term_share"] * 100))


if __name__ == "__main__":
    main()
