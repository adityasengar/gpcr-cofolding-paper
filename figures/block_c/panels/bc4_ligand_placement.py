# -*- coding: utf-8 -*-
"""BC-4 — where the ligands actually are.

Spec: analysis/block_c/panels/BC-4_ligand_placement.md
Claim: SC-C-1's numerator, plus the dispatch's 4(a) retraction and 4(i)
peptide adjudication.

THE ONLY FULLY DATA-BACKED PANEL IN BLOCK C. The 40,000-row census is the one
row-level file the campaign shipped.

Two things this panel exists to prevent, both of which have already caught
someone -- including me, on my first verification run:
  1. Treating entrance-bound (8-15 A) as failure. It is 7,349 of 40,000 rows and
     adjudicated a VALID pose. Counting it as error reports 34.8% where the
     truth is 15.1%.
  2. Pooling small-molecule and peptide ligands. In the SAME apo
     agonist/antagonist cells they are 1.52% and 66.53% off-site, because
     peptide receptors bind at the extracellular vestibule.
"""
import _shead                                                    # noqa: F401
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
import bcdata as B

fs.use_house_style()
BANDS = [(0, 8, "in-pocket", "#CFE3D4"), (8, 15, "entrance-bound\n(valid pose)", "#F2E6C9"),
         (15, 200, "off-site", "#F0D5CE")]


def main():
    cen = B.census()
    d = cen.distance_A.dropna()

    fig, (ax, axb) = fs.figure(width=fs.W2, height=94 * fs.MM, ncols=2,
                               gridspec_kw={"width_ratios": [1.45, 1.0]})

    for lo, hi, lab, col in BANDS:
        ax.axvspan(lo, min(hi, 60), color=col, lw=0, zorder=0)
        ax.text((lo + min(hi, 60)) / 2.0, 0.965, lab, transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=6.0, color=fs.BLACK)
    for src, col, lab in (("hetatm", fs.BLUE, "small molecule"),
                          ("peptide_chain", fs.VERM, "peptide")):
        v = cen.loc[cen.ligand_source == src, "distance_A"].dropna()
        ax.hist(np.clip(v, 0, 60), bins=np.linspace(0, 60, 121), histtype="step",
                lw=1.5, color=col, label="%s (n=%s)" % (lab, format(len(v), ",")),
                zorder=3)
    ax.axvline(8, color=fs.GREY, lw=0.8); ax.axvline(15, color=fs.BLACK, lw=1.0)
    ax.set_xlim(0, 60); ax.set_yscale("log")
    ax.set_xlabel(u"ligand centroid to pocket centroid (Å)")
    ax.set_ylabel("predictions (log)")
    ax.set_title("the three adjudicated bands, by ligand type", fontsize=7.4)
    ax.legend(frameon=False, fontsize=6.2, loc="upper right")

    strata = [
        ("apo x {ag, antag}\nSMALL MOLECULE", (cen.arm == "apo") &
         cen.role.isin(["full_agonist", "neutral_antagonist"]) &
         (cen.ligand_source == "hetatm"), fs.BLUE),
        ("apo x {ag, antag}\nPEPTIDE", (cen.arm == "apo") &
         cen.role.isin(["full_agonist", "neutral_antagonist"]) &
         (cen.ligand_source == "peptide_chain"), fs.VERM),
        ("apo arm\nall", cen.arm == "apo", fs.GREY),
        ("cognate arm\nall", cen.arm == "cognate", fs.GREY),
        ("pooled\nall 40,000", cen.distance_A.notna(), fs.BLACK),
    ]
    x = np.arange(len(strata))
    vals, ns = [], []
    for i, (lab, m, col) in enumerate(strata):
        v = cen.loc[m, "distance_A"].dropna()
        r = 100.0 * float((v > 15).mean()); vals.append(r); ns.append(len(v))
        axb.bar(i, r, width=0.62, color=col, edgecolor="white", lw=0.7)
        axb.text(i, r + 1.4, "%.2f%%" % r, ha="center", fontsize=6.5,
                 fontweight="bold", color=col)
    axb.axhline(25.6, color=fs.VERM, lw=1.1, ls=(0, (4, 2)))
    axb.text(len(strata) - 0.4, 26.6, "retracted v1 figure, 25.6%", fontsize=5.8,
             color=fs.VERM, ha="right")
    axb.set_xticks(x); axb.set_xticklabels([s[0] for s in strata], fontsize=5.9)
    axb.set_ylabel(u"off-site (> 15 Å), % of rows")
    axb.set_ylim(0, 74)
    axb.set_title("the stratum that matters is 1.52%", fontsize=7.4)

    fs.panel_label(ax, "a", dx=-0.13); fs.panel_label(axb, "b", dx=-0.22)

    note = (u"All 40,000 predictions. Bands: in-pocket at or below 8 Å (%s rows), "
            u"entrance-bound 8-15 Å (%s), off-site above 15 Å (%s). "
            u"ENTRANCE-BOUND IS AN ADJUDICATED VALID POSE, not a failure — "
            u"shading it as error would roughly double the apparent off-site rate. "
            u"b, the stratum SC-C-1 is actually computed on is the first bar: "
            u"small-molecule, apo, agonist or antagonist, %.2f%% off-site on "
            u"n=%s. Peptide ligands in the SAME cells are %.2f%% at a median of "
            u"17.5 Å, because peptide receptors bind at the extracellular "
            u"vestibule. Pooling the two manufactures a failure rate. "
            u"The dashed line is the retracted v1 figure of 25.6%%, which came "
            u"from a receptor-chain picker that selected Gα rather than the "
            u"receptor on any chain shorter than ~394 aa; the corrected pooled "
            u"value is %.2f%%."
            % (format(int((d <= 8).sum()), ","), format(int(((d > 8) & (d <= 15)).sum()), ","),
               format(int((d > 15).sum()), ","), vals[0], format(ns[0], ","),
               vals[1], vals[4]))
    fig.text(0.01, -0.10, "\n".join(textwrap.wrap(note, 132)), fontsize=5.4,
             color=fs.GREY, va="top", ha="left")

    p = fs.save(fig, "bc4_ligand_placement")
    print("BC-4 ->", p[0])
    for (lab, _, _), r, n in zip(strata, vals, ns):
        print("  %-34s n=%-7s off-site %.2f%%" % (lab.replace("\n", " "), n, r))


if __name__ == "__main__":
    main()
