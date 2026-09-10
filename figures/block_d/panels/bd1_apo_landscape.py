#!/usr/bin/env python3
"""BD-1 -- the unsteered apo landscape is receptor-and-backbone specific.

Spec: dispatch Fig. D1-1.   Claims: SC-D-1, SC-D-11 (Flag D-5).

WHAT THIS PANEL EXISTS TO PREVENT. The original D1 headline was a
backbone-AVERAGED apo fraction, and it was withdrawn (W-D-2) because the
underlying behaviour is bimodal per backbone: on ADRB2, Chai calls 100% of 500
apo samples active and Boltz calls 0%. An average over those two is 50% and
describes nothing that happened. So this panel has no pooled cell anywhere, and
`bddata` provides no way to compute one.

EVIDENTIAL CLASS: SUMMARY. Block D shipped no row table, so the 28 cells here
are transcribed from PARTA_D1 section 1 rather than recomputed. The panel says
so on its face. Only the four structures marked with a ring were measured from
coordinates by this project.
"""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

import figstyle as fs                                          # noqa: E402
import bddata as bd                                            # noqa: E402

MEASURED = {                     # file -> (receptor, backbone)
    "d1_adrb2_chai_apo.cif": ("ADRB2", "chai"),
    "d1_adrb2_boltz_apo.cif": ("ADRB2", "boltz"),
    "d1_ghsr_boltz_apo.cif": ("GHSR", "boltz"),
    "d1_cnr2_chai_apo.cif": ("CNR2", "chai"),
    "d1_lpar1_of3_apo.cif": ("LPAR1", "of3"),
}


def main():
    fs.use_house_style()
    fig = plt.figure(figsize=(fs.W2, 122 * fs.MM))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 1.25, 1.0], wspace=0.55,
                          left=0.10, right=0.985, top=0.88, bottom=0.30)

    recs = bd.D1_RECEPTORS
    bbs = fs.BACKBONE_ORDER
    method, why = bd.ci_method("d1")

    # ---- a, b: the two axes, as heatmaps on one shared scale ---------------
    for k, (ax_i, table, title) in enumerate((
            (0, bd.D1_PREDICATE_ACTIVE, "two-instrument predicate-active"),
            (1, bd.D1_SUBA_ACTIVE, "sub-Å pocket-Cα to the active reference"))):
        ax = fig.add_subplot(gs[0, ax_i])
        M = np.array([[(table[r][b][0] if isinstance(table[r][b], tuple)
                        else table[r][b]) for b in bbs] for r in recs])
        im = ax.imshow(M, cmap="magma", vmin=0, vmax=100, aspect="auto")
        for i, r in enumerate(recs):
            for j, b in enumerate(bbs):
                v = M[i, j]
                ax.text(j, i, ("%.0f" % v) if v >= 1 or v == 0 else "%.1f" % v,
                        ha="center", va="center", fontsize=6.2,
                        color="white" if v < 55 else "black")
        ax.set_xticks(range(4))
        ax.set_xticklabels([fs.BACKBONE_LABELS[b] for b in bbs], rotation=32,
                           ha="right", fontsize=6.6)
        ax.set_yticks(range(len(recs)))
        ax.set_yticklabels(recs, fontsize=6.8)
        ax.set_title(title, fontsize=7.2, pad=6)
        fs.panel_label(ax, "ab"[k], dx=-0.30, dy=1.10)
        if ax_i == 0:
            # ring the cells whose structure we measured ourselves
            for fn, (r, b) in MEASURED.items():
                v = bd.measured_npxxy(fn)
                if v is None or r not in recs:
                    continue
                i, j = recs.index(r), bbs.index(b)
                ax.add_patch(plt.Circle((j, i), 0.34, fill=False,
                                        color=fs.GREEN, lw=1.3, zorder=5))
        cb = fig.colorbar(im, ax=ax, fraction=0.038, pad=0.03)
        cb.ax.tick_params(labelsize=6)
        cb.set_label("% of 500 apo samples", fontsize=6.3)

    # ---- c: the four outliers, and their cross-tier reproduction ----------
    ax = fig.add_subplot(gs[0, 2])
    labels = ["%s\n%s" % (r, fs.BACKBONE_LABELS[b]) for r, b, _, _ in bd.D1_OUTLIERS]
    d1d = [d for _, _, d, _ in bd.D1_OUTLIERS]
    blka = [float(s.replace("+", "")) for _, _, _, s in bd.D1_OUTLIERS]
    y = np.arange(len(labels))
    ax.barh(y + 0.19, d1d, height=0.36, color=fs.VERM, label="D1 (n=500/cell)")
    ax.barh(y - 0.19, blka, height=0.36, color=fs.GREY,
            label="Block A, independent (n=25/cell)")
    ax.axvline(50, color="black", lw=0.8, ls="--")
    ax.text(50, -0.72, "+50 pt", fontsize=5.8, va="bottom", ha="center")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=6.4)
    ax.set_xlabel("percentage points above the best other backbone", fontsize=6.8)
    ax.set_xlim(0, 108)
    ax.set_ylim(len(labels) - 0.5, -1.0)
    ax.legend(fontsize=5.9, frameon=False, loc="upper center",
              bbox_to_anchor=(0.5, -0.13), ncol=1)
    ax.set_title("the same four cells, on two corpora", fontsize=7.2, pad=6)
    fs.panel_label(ax, "c", dx=-0.36, dy=1.10)

    note = (
        "a, b: seven receptors x four backbones, apo arm only, 500 samples per cell, "
        "transcribed from PARTA_D1 section 1 -- Block D shipped no row table, so these "
        "are SUMMARY values, not recomputed here. Intervals in that source are "
        "%s (%s); none is drawn because the cells are point rates. Green rings mark the "
        "five cells whose shipped structure we measured from coordinates: ADRB2/Chai "
        "%.2f A and ADRB2/Boltz %.2f A on the SAME receptor, GHSR/Boltz %.2f, CNR2/Chai "
        "%.2f, LPAR1/OF3 %.2f, against the %.2f A NPxxY threshold. c: the four "
        "active-outlier cells of SC-D-1, each shown twice -- once on D1 and once on "
        "Block A's independent apo corpus at n=25. NO CELL IS AVERAGED ACROSS "
        "BACKBONES anywhere in this figure; the backbone-averaged version of this "
        "result was withdrawn as W-D-2."
        % (method, why,
           bd.measured_npxxy("d1_adrb2_chai_apo.cif") or 0,
           bd.measured_npxxy("d1_adrb2_boltz_apo.cif") or 0,
           bd.measured_npxxy("d1_ghsr_boltz_apo.cif") or 0,
           bd.measured_npxxy("d1_cnr2_chai_apo.cif") or 0,
           bd.measured_npxxy("d1_lpar1_of3_apo.cif") or 0,
           bd.PREDICATE_NPXXY))
    fig.text(0.012, 0.008, fs.wrap(note, 148) if hasattr(fs, "wrap")
             else _wrap(note, 148), fontsize=5.3, va="bottom", color="0.25")

    fs.save(fig, "bd1_apo_landscape")
    print("BD-1 written.")
    return 0


def _wrap(s, n):
    import textwrap
    return "\n".join(textwrap.wrap(s, n))


if __name__ == "__main__":
    sys.exit(main())
