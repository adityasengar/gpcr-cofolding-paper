"""
S1 - the exclusion flags: what each one covers and what applying it does.

This is the supplementary that exists because `excl_any` is a trap. It fires
on 5,093 of 9,490 rows (54%) and is the wrong filter for almost every panel,
because the five sets have different scopes and only E1 and E2 are about the
row itself. E1+E2 alone keeps 99.7% of the corpus.

  a  what each flag covers, against the 9,490-row denominator
  b  what each exclusion combination does to each headline metric, per
     backbone: percentage shift from the baseline value

FILTER: none. This panel is ABOUT the filters, so it shows the unfiltered
population and the shipped sweep (08_exclusions/exclusion_sweep.csv, 160 rows
= 5 metrics x 4 backbones x 8 combinations).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import numpy as np, pandas as pd                            # noqa: E402
import badata as B, figstyle as fs, figpanels as fp         # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402

METRIC_LABEL = {"median_tilt_shift": u"Δtilt",
                "fraction_of_way_to_active": "fraction*",
                "apo_active_rate": "apo rate",
                "cognate_active_rate": "cognate rate",
                "tilt_active_rate": "tilt rate"}
FLAG_RULE = {"E1": "cell mean pLDDT < 50 (one broken cell, ACM1/cognate/Protenix)",
             "E2": u"NPxxY-OH < 2.4 Å, impossible geometry",
             "E3": "the receptor's reference fails its own predicate",
             "E4": "Class B or Class F",
             "E5": "agonist-only actives (OPRD, CNR1, FZD4)"}
SETS = ["baseline", "E1", "E2", "E1+E2", "E4", "E1+E2+E4", "E1+E2+E4+E5",
        "all_E1-E5"]


def main():
    fs.use_house_style()
    rows = B.rows()
    defs = B.load("08_exclusions/exclusion_definitions.csv")
    sweep = B.load("08_exclusions/exclusion_sweep.csv")

    fig = plt.figure(figsize=(fs.W2, 150 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(2, 1, height_ratios=[0.85, 1.3])
    axa = fig.add_subplot(gs[0, 0])
    axb = fig.add_subplot(gs[1, 0])

    # ---- a: coverage of each flag -----------------------------------------
    labels, counts, cols = [], [], {}
    for _, d in defs.iterrows():
        lab = d["name"] + (" (union)" if d["name"] == "E3" else "")
        labels.append(lab)
        counts.append(int(rows["excl_" + d["name"]].sum()))
        cols[lab] = fs.VERM if d["name"] in ("E1", "E2") else fs.BLUE
    for extra, key, c in ((u"E3 NPxxY", "excl_E3_npxxy", fs.GREY),
                          (u"E3 tilt", "excl_E3_tilt", fs.GREY),
                          (u"excl_any (never filter on this)",
                           "excl_any", fs.BLACK)):
        labels.append(extra); counts.append(int(rows[key].sum()))
        cols[extra] = c
    labels.append(u"E1 or E2 (the default here)")
    counts.append(int((rows.excl_E1 | rows.excl_E2).sum()))
    cols[labels[-1]] = fs.VERM
    fp.count_dots(axa, labels, counts, total=len(rows), colours=cols,
                  order_by_count=True, label_gap=0.010)
    axa.set_xlabel("rows the flag covers (of %d)" % len(rows))
    axa.set_title("what each exclusion flag actually covers", fontsize=6.5)
    axa.text(1.0, 1.0, "\n".join("%s  %s" % (k, v)
                                  for k, v in sorted(FLAG_RULE.items())),
             transform=axa.transAxes, ha="right", va="top", fontsize=5,
             color=fs.GREY)
    axa.text(0.99, 0.02,
             "E1+E2 keeps %d of %d rows (%.1f%%).\n"
             "excl_any removes %d (%.0f%%) and is the union of five sets with "
             "different scopes."
             % (len(rows) - (rows.excl_E1 | rows.excl_E2).sum(), len(rows),
                100 * (1 - (rows.excl_E1 | rows.excl_E2).mean()),
                int(rows.excl_any.sum()), 100 * rows.excl_any.mean()),
             transform=axa.transAxes, ha="right", va="bottom", fontsize=5,
             color=fs.BLACK)
    fs.panel_label(axa, "a", dx=-0.30)

    # ---- b: the sweep ------------------------------------------------------
    metrics = list(METRIC_LABEL)
    vmax = float(np.nanmax(np.abs(sweep.pct_shift_from_baseline)))
    sweep = sweep.copy()
    sweep["row"] = [METRIC_LABEL[m] + u" · " + fs.BACKBONE_LABELS[b]
                    for m, b in zip(sweep.metric, sweep.backbone)]
    row_order = [METRIC_LABEL[m] + u" · " + fs.BACKBONE_LABELS[b]
                 for m in metrics for b in fs.BACKBONE_ORDER]
    tab = (sweep.pivot_table(index="row", columns="exclusion_set",
                             values="pct_shift_from_baseline")
           .reindex(index=row_order, columns=SETS))
    fp.matrix(axb, tab, value_label="% shift from the baseline value",
              cmap="RdBu_r", annotate=True, vmin=-vmax, vmax=vmax,
              zero_is_absent=False, annotate_fmt="%.3g")
    axb.set_xticklabels(SETS, rotation=25, ha="right", fontsize=5.5)
    for y in (3.5, 7.5, 11.5, 15.5):
        axb.axhline(y, color=fs.BLACK, lw=0.6)
    axb.set_title("what each exclusion combination does to each headline "
                  "metric (no sign flip anywhere: %d of %d cells)"
                  % (int(sweep.sign_flip.sum()), len(sweep)), fontsize=6.5)
    axb.text(0.0, -0.13, "* the fraction appears in Table T2 only, never in a "
             "figure (hard rule); it is in this sweep because the sweep is "
             "about the filters, not about the value",
             transform=axb.transAxes, fontsize=5, color=fs.GREY, va="top")
    fs.panel_label(axb, "b", dx=-0.30, dy=1.06)

    paths = fs.save(fig, "s1_exclusions")
    print("S1 ->", paths[0])
    for lab, c in zip(labels, counts):
        print("   %-58s %5d  (%.1f%%)" % (lab[:58], c, 100.0 * c / len(rows)))
    big = sweep.reindex(sweep.pct_shift_from_baseline.abs()
                        .sort_values(ascending=False).index).head(5)
    print("  largest shifts:")
    for _, r in big.iterrows():
        print("     %-26s %-9s %-12s %+.1f%%"
              % (r.metric, r.backbone, r.exclusion_set,
                 r.pct_shift_from_baseline))
    print("  sign flips anywhere in the sweep: %d" % int(sweep.sign_flip.sum()))
    return paths


if __name__ == "__main__":
    main()
