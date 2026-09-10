# -*- coding: utf-8 -*-
"""BB-4 — the PIF connector: engaged-but-inactive sits at apo geometry.

Spec: data/block_b/12_narrative/figures/BB-4_pif_connector_engaged_but_inactive.md
Claim: SC-B-4. Standalone panel, no manuscript figure number, no composite.

Why this panel carries weight out of proportion to its size: the P5.50-I3.40-F6.44
connector is NOT one of the two axes the predicate reads. So when decoy cells
that are engaged but not active land on apo geometry, that is an independent
axis agreeing with the call rather than a restatement of it.

THE ADDENDUM FORBIDS RENDERING THIS AS STRUCTURE, and it is right. The whole
spread is apo 15.35 to cognate 16.04, i.e. 0.7 A, which cannot be drawn honestly
at a legible scale. It is a distribution result and it is plotted as one.
"""
import _shead                                                    # noqa: F401
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
import badata as B

fs.use_house_style()

SUBSETS = [
    ("apo (all cells)",              lambda d: d.arm == "apo",                       fs.GREY),
    ("cognate\nactive + engaged",    lambda d: (d.arm == "cognate") & d.A & d.E,     fs.GREEN),
    ("shuffled\nactive + engaged",   lambda d: (d.arm == "shuffled") & d.A & d.E,    fs.SKY),
    ("decoy\nactive + engaged",      lambda d: (d.arm == "decoy") & d.A & d.E,       fs.BLUE),
    ("decoy\nENGAGED, NOT ACTIVE",   lambda d: (d.arm == "decoy") & d.EBI,           fs.VERM),
]


def main():
    pif = B.table("06_interface/interface_pif_connector.csv")
    pif["A"] = pif.cell_active.astype(bool)
    pif["E"] = pif.cell_engaged_20.astype(bool)
    pif["EBI"] = pif.cell_engaged_but_inactive.astype(bool)

    fig, (ax, axb) = fs.figure(width=fs.W2, height=100 * fs.MM, ncols=2,
                               gridspec_kw={"width_ratios": [1.5, 1.0]})

    meds, ns = [], []
    for i, (lab, sel, col) in enumerate(SUBSETS):
        v = pif.loc[sel(pif), "pif_sum_ca"].dropna().to_numpy()
        meds.append(np.median(v)); ns.append(len(v))
        parts = ax.violinplot([v], positions=[i], widths=0.72, showextrema=False,
                              showmedians=False)
        for b in parts["bodies"]:
            b.set_facecolor(col); b.set_alpha(0.30); b.set_edgecolor("none")
        rng = np.random.default_rng(7)
        ax.scatter(i + rng.uniform(-0.13, 0.13, len(v)), v, s=4.0, color=col,
                   alpha=0.65, lw=0, zorder=3)
        ax.plot([i - 0.30, i + 0.30], [np.median(v)] * 2, lw=2.4, color=col, zorder=4)
        ax.annotate("%.2f" % np.median(v), (i, np.median(v)),
                    textcoords="offset points", xytext=(20, -2), fontsize=6.4,
                    fontweight="bold", color=col)
        fs.annotate_n(ax, i, len(v))

    apo_med = meds[0]
    ax.axhline(apo_med, color=fs.GREY, lw=0.8, ls=":", zorder=1)
    ax.text(4.45, apo_med, " apo geometry", fontsize=6.0, color=fs.GREY, va="center")
    ax.set_xticks(range(len(SUBSETS)))
    ax.set_xticklabels([s[0] for s in SUBSETS], fontsize=6.2)
    ax.set_ylabel(u"PIF connector, P5.50-I3.40 + I3.40-F6.44 Cα (Å)")
    ax.set_title(u"an axis the predicate never reads agrees with it anyway",
                 fontsize=7.4)

    # ---- b: per backbone, because a pooled panel needs a per-backbone companion
    bbs = fs.BACKBONE_ORDER
    w = 0.36
    x = np.arange(len(bbs))
    for k, (lab, sel, col, off) in enumerate([
            ("decoy engaged, not active", lambda d: d.EBI & (d.arm == "decoy"), fs.VERM, -w/2),
            ("cognate active + engaged", lambda d: (d.arm == "cognate") & d.A & d.E, fs.GREEN, +w/2)]):
        vals = [pif.loc[sel(pif) & (pif.backbone == b), "pif_sum_ca"].median() for b in bbs]
        axb.bar(x + off, vals, width=w, color=col, edgecolor="white", lw=0.6,
                label=lab, zorder=2)
    axb.set_ylim(14.6, 16.6)
    axb.axhline(apo_med, color=fs.GREY, lw=0.8, ls=":", zorder=1)
    axb.set_xticks(x)
    axb.set_xticklabels([fs.BACKBONE_LABELS[b] for b in bbs], rotation=20, ha="right")
    axb.set_ylabel(u"median PIF connector (Å)")
    axb.set_title("three of four backbones separate cleanly", fontsize=7.4)
    axb.legend(frameon=False, fontsize=6.0, loc="upper left")

    fs.panel_label(ax, "a", dx=-0.11); fs.panel_label(axb, "b", dx=-0.20)

    note = (u"One point per receptor x arm x backbone cell, 640 cells in total; "
            u"the value is that cell's median connector distance. Engagement is "
            u"the alpha5 tip to R3.50 distance below 20 A. The connector is "
            u"P5.50-I3.40-F6.44 and is NOT one of the two axes the activation "
            u"predicate reads, which is the point of the panel: an independent "
            u"axis lands where the predicate says it should. Decoy cells that are "
            u"engaged but not active sit at %.2f A against apo at %.2f A and "
            u"active-engaged cells at %.2f-%.2f A. "
            u"b, OpenFold3 signs in the same direction as the other three but at "
            u"smaller magnitude. No structural render of this exists and none "
            u"should: the entire spread is %.2f A, which cannot be drawn honestly "
            u"at a legible scale. It is a distribution result and it is plotted "
            u"as one."
            % (meds[4], meds[0], min(meds[1:4]), max(meds[1:4]), max(meds) - min(meds)))
    fig.text(0.01, -0.085, "\n".join(textwrap.wrap(note, 132)),
             fontsize=5.4, color=fs.GREY, va="top", ha="left")

    paths = fs.save(fig, "bb4_connector")
    print("BB-4 ->", paths[0])
    for (lab, _, _), m, n in zip(SUBSETS, meds, ns):
        print("  %-32s n=%3d  median %.2f" % (lab.replace("\n", " "), n, m))


if __name__ == "__main__":
    main()
