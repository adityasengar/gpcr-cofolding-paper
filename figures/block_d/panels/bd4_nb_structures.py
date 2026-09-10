#!/usr/bin/env python3
"""BD-4 -- what the nanobody-directed models actually built, at atomic scale.

Spec: dispatch Fig. D2-2.   Claim: SC-D-7 (and the F3/F5 contrast cases).

WHY THIS PANEL IS NOT A RENDER. The dispatch asks for a four-panel structure
gallery annotated with each file's NPxxY-OH distance and its one-line verdict.
The verdicts are available; the renders are not, because `lit/RENDER_CONVENTIONS`
requires every measured distance to carry the atom pair it was measured between
and every hand-picked structure to carry its selection rule, and building four
publication renders is the figures session's work, not something to improvise
here. What this panel does instead is the part that carries the evidence: it
plots the MEASURED distance for each of the four structures against the
threshold that decides the call, so the claim "Protenix built an active pocket
underneath a correctly docked inactive nanobody" is visible as a number rather
than asserted in a caption.

EVERY VALUE HERE WAS MEASURED FROM THE COORDINATES by
analysis/block_d/cifmeasure.py -- not transcribed. That matters more in this
block than in any previous one: Block D shipped no row table, so these fifteen
files are the only place a Block D number can be checked against something other
than another sentence. Two of the manifest's three stated distances reproduce to
the decimal; the third quotes a 50-sample cell median beside a single file
(DISCREPANCY_REPORT D-D-4), which is exactly the confusion this panel avoids by
measuring.

The selection rule, stated because the corpus survey found 59 renders that omit
it: these four are the D2 spot-check files shipped in `10_structures/spot_check/`,
chosen by the pipeline to illustrate named findings, one sample each. They are
NOT a random draw and no statistic may be computed from them.
"""
import os
import sys
import textwrap

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

import figstyle as fs                                          # noqa: E402
import bddata as bd                                            # noqa: E402

CASES = [
    ("d2_adrb2_inactive_nb_protenix.cif", "ADRB2 · Protenix2", "inactive-Nb",
     "builds an ACTIVE pocket under a correctly seated inactive nanobody\n"
     "(125-aa Nb60, chain B properly docked) — SC-D-7's flagship"),
    ("d2_adrb2_inactive_nb_boltz.cif", "ADRB2 · Boltz-2", "inactive-Nb",
     "same receptor, same nanobody, correct outcome — the contrast that\n"
     "makes the Protenix cell a backbone property, not a receptor property"),
    ("d2_oprk_inactive_nb_boltz.cif", "OPRK · Boltz-2", "inactive-Nb",
     "the flagship inversion cell inverts on 48% of 50 samples; THIS sample\n"
     "is one of the 52% that did not — a single file cannot show a rate"),
    ("d2_acm2_active_nb_chai.cif", "ACM2 · Chai-1", "active-Nb",
     "active nanobody docked and the pocket stays strongly inactive —\n"
     "Chai refuses to move on this receptor (delta = 0)"),
]


def main():
    fs.use_house_style()
    fig = plt.figure(figsize=(fs.W2, 96 * fs.MM))
    ax = fig.add_axes([0.30, 0.30, 0.665, 0.60])

    ys, vals, labs = [], [], []
    for i, (fn, title, arm, verdict) in enumerate(CASES):
        v = bd.measured_npxxy(fn)
        ys.append(len(CASES) - 1 - i)
        vals.append(v)
        labs.append("%s\n%s" % (title, arm))

    for y, v, (fn, title, arm, verdict) in zip(ys, vals, CASES):
        call = bd.state_call(v)
        c = fs.STATE_COLOURS[call]
        ax.plot([0, v], [y, y], color=c, lw=1.6, alpha=0.55, zorder=1)
        ax.scatter([v], [y], s=64, color=c, zorder=3, edgecolor="white", lw=0.9)
        ax.text(v, y + 0.30, "%.2f Å  $\\rightarrow$  %s" % (v, call.upper()), fontsize=6.6,
                ha="center", va="bottom", color=c, weight="bold")
        ax.text(21.3, y, verdict, fontsize=5.6, va="center", ha="left",
                color="0.30")

    ax.axvline(bd.PREDICATE_NPXXY, color="black", lw=1.0, ls="--", zorder=2)
    ax.text(bd.PREDICATE_NPXXY, len(CASES) - 0.35,
            " NPxxY threshold %.2f Å\n active below" % bd.PREDICATE_NPXXY,
            fontsize=6.0, va="top", ha="left")

    ax.set_yticks(ys)
    ax.set_yticklabels(labs, fontsize=6.8)
    ax.set_xlim(0, 21)
    ax.set_ylim(-0.7, len(CASES) - 0.05)
    ax.set_xlabel("d(Tyr5.58 OH, Tyr7.53 OH), measured from the deposited "
                  "coordinates (Å)", fontsize=7.2)
    ax.set_title("what the four directed-nanobody models actually built",
                 fontsize=7.6, pad=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    note = (
        "One shipped structure per row, from 10_structures/spot_check/. SELECTION "
        "RULE: these are the pipeline's hand-picked D2 illustrations of named "
        "findings, one sample each -- NOT a random draw, and no rate may be read "
        "from them. Every distance was RECOMPUTED here from the coordinates by "
        "analysis/block_d/cifmeasure.py, between the hydroxyl oxygens of Tyr5.58 "
        "and Tyr7.53; Tyr7.53 was located independently in each file from its own "
        "NPxxY motif and agreed with the GPCRdb-mapped position on all fifteen "
        "shipped structures. The first row is the whole of SC-D-7: an inactive-state "
        "nanobody is correctly docked and the receptor underneath it is in the "
        "active conformation, so the Nb-B-as-active behaviour is a property of what "
        "the model built and not of how it was scored. Row 3 is the honest one: the "
        "OPRK inversion happens on 48%% of samples [33.7, 62.6] and this file is one "
        "of the ones where it did not happen."
    )
    fig.text(0.012, 0.012, "\n".join(textwrap.wrap(note, 150)), fontsize=5.3,
             va="bottom", color="0.25")

    fs.save(fig, "bd4_nb_structures")
    print("BD-4 written. measured:",
          {f.split('_')[1] + "_" + f.split('_')[-1][:-4]: bd.measured_npxxy(f)
           for f, _, _, _ in CASES})
    return 0


if __name__ == "__main__":
    sys.exit(main())
