"""
S7 - the paralogy clustering and the date-stratified holdout.

The cluster bootstrap is authoritative (C-8), so the shape of the clustering
is what its intervals rest on. The shipped map resolves to a different cluster
count from the manuscript's 26, and the README says so: the panel-slug-to-
family mapping was reconstructed heuristically.

  a  cluster sizes: how many receptors each paralog cluster holds
  b  the date-stratified holdout, receptor level and cluster level, per
     backbone, against the 48-receptor panel

FILTER: 07_clusters_and_holdout/, as shipped.
"""
exec(open(__file__.replace("s7_clusters_holdout.py", "_shead.py")).read())
import numpy as np                                          # noqa: E402
import badata as B, figstyle as fs, figpanels as fp         # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402


def main():
    fs.use_house_style()
    cm = B.load("07_clusters_and_holdout/cluster_map.csv")
    hc = B.load("07_clusters_and_holdout/holdout_counts.csv")

    fig, axes = plt.subplots(1, 2, figsize=(fs.W2, 78 * fs.MM),
                             constrained_layout=True,
                             gridspec_kw=dict(width_ratios=[1.5, 1.0]))
    ax = axes[0]
    sizes = (cm.drop_duplicates("cluster_id").set_index("cluster_id")
             .cluster_size.sort_values(ascending=False))
    pos = np.arange(len(sizes))
    singles = int((sizes == 1).sum())
    cols = [fs.GREY if s == 1 else fs.BLUE for s in sizes]
    ax.bar(pos, sizes.values, width=0.8, color=cols, edgecolor="none")
    ax.set_xticks(pos)
    ax.set_xticklabels(sizes.index, rotation=90, fontsize=4.2)
    ax.set_ylabel("receptors in the cluster")
    ax.set_yticks(np.arange(0, int(sizes.max()) + 1))
    ax.set_xlabel("paralog cluster")
    ax.set_title("%d clusters over %d receptors; %d are singletons (%.0f%%)"
                 % (len(sizes), int(sizes.sum()), singles,
                    100.0 * singles / len(sizes)), fontsize=6.5)
    ax.text(0.99, 0.98,
            "a count is not a distribution, so this is a count: each bar is\n"
            "one cluster and its height is an exact membership, not a summary.\n"
            "grey = singleton, on which the cluster bootstrap has no leverage.\n"
            "The manuscript quotes 26 clusters; this drop resolves to %d\n"
            "because the panel-slug-to-family map was reconstructed\n"
            "heuristically (see the drop README)." % len(sizes),
            transform=ax.transAxes, ha="right", va="top", fontsize=4.5,
            color=fs.GREY)
    fs.panel_label(ax, "a", dx=-0.10)

    ax = axes[1]
    labels, counts, cols2 = [], [], {}
    for bb in fs.BACKBONE_ORDER:
        r = hc[hc.backbone == bb].iloc[0]
        for tag, v in (("receptor level", r.receptor_level_count),
                       ("cluster level", r.cluster_level_count)):
            lab = "%s · %s" % (fs.BACKBONE_LABELS[bb], tag)
            labels.append(lab); counts.append(int(v))
            cols2[lab] = fs.BACKBONE_COLOURS[bb]
    fp.count_dots(ax, labels, counts, total=int(cm.receptor.nunique()),
                  colours=cols2, order_by_count=False, label_gap=0.03)
    ax.set_xlabel("held out (of %d receptors)" % cm.receptor.nunique())
    ax.set_title("date-stratified holdout", fontsize=6.5)
    ax.text(0.99, 0.99,
            "cutoff date / powered:\n" + "\n".join(
                "  %-11s %s   %s" % (fs.BACKBONE_LABELS[b],
                                     hc[hc.backbone == b].cutoff_date.iloc[0],
                                     "powered" if
                                     hc[hc.backbone == b].powered.iloc[0]
                                     else "UNDERPOWERED")
                for b in fs.BACKBONE_ORDER),
            transform=ax.transAxes, ha="right", va="top", fontsize=4.5,
            color=fs.GREY)
    fs.panel_label(ax, "b", dx=-0.55)

    paths = fs.save(fig, "s7_clusters_holdout")
    print("S7 ->", paths[0])
    print("  clusters %d over %d receptors, singletons %d"
          % (len(sizes), int(sizes.sum()), singles))
    print("  sizes: %s" % sizes.value_counts().sort_index().to_dict())
    print("  holdout: %s" % hc.to_dict("records"))
    return paths


if __name__ == "__main__":
    main()
