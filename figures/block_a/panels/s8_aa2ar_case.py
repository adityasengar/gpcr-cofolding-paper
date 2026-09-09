"""
S8 - the AA2AR case, and the structure BA-5e is drawn from.

SC-5 claims AA2AR resolves the paired switch cleanly on all four backbones:
apo lands on the inactive reference, cognate on the active one. This is that
claim as a picture, over all 200 AA2AR rows, and it is also the quantitative
panel that BA-5e's render must sit beside - without it, the render is the
corpus's second commonest defect (a claim with no quantitative panel, 58 of
232 render rows).

  a  RMSD to the ACTIVE reference (y) against RMSD to the INACTIVE one (x),
     one point per row, coloured by arm. The diagonal is "equally far from
     both": a row ABOVE it is closer to the INACTIVE reference, a row BELOW it
     is closer to the ACTIVE one. Apo should sit above, cognate below.
  b  confidence against RMSD-to-active for the same rows, with the row the
     render is drawn from marked.

FILTER: 06_confidence/aa2ar_case.csv, all 200 rows (4 backbones x 2 arms x 25
seeds). The file carries excl_any; none of these rows has any flag set except
the one E2 row, which is marked rather than dropped.
"""
exec(open(__file__.replace("s8_aa2ar_case.py", "_shead.py")).read())
import numpy as np                                          # noqa: E402
import badata as B, figstyle as fs, figpanels as fp         # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402

RENDER_ROW = 567


def main():
    fs.use_house_style()
    aa = B.load("06_confidence/aa2ar_case.csv")
    rows = B.rows()
    flagged = set(rows[(rows.receptor == "AA2AR") &
                       (rows.excl_E1 | rows.excl_E2)].row_id)

    fig, axes = plt.subplots(1, 2, figsize=(fs.W2, 78 * fs.MM),
                             constrained_layout=True)

    ax = axes[0]
    lim = [0, max(aa.rmsd_to_active_ref.max(), aa.rmsd_to_inactive_ref.max())
           * 1.08]
    ax.plot(lim, lim, color=fs.BLACK, lw=0.6, ls=(0, (4, 2)), zorder=1)
    for arm in ("apo", "cognate"):
        d = aa[aa.arm == arm]
        ax.scatter(d.rmsd_to_inactive_ref, d.rmsd_to_active_ref, s=5,
                   color=fs.ARM_COLOURS[arm], alpha=0.7, linewidths=0,
                   label="%s (n=%d)" % (fs.ARM_LABELS[arm], len(d)), zorder=3)
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel(u"RMSD to the INACTIVE reference (Å)")
    ax.set_ylabel(u"RMSD to the ACTIVE reference (Å)")
    ax.legend(loc="upper left", fontsize=5, borderpad=0.2)
    ncorrect = int(((aa.arm == "apo") &
                    (aa.rmsd_to_inactive_ref < aa.rmsd_to_active_ref)).sum() +
                   ((aa.arm == "cognate") &
                    (aa.rmsd_to_active_ref < aa.rmsd_to_inactive_ref)).sum())
    ax.set_title("AA2AR: %d of %d rows sit nearer their arm's reference"
                 % (ncorrect, len(aa)), fontsize=6.5)
    ax.text(0.98, 0.02, "dashed: equally far from both references",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=5,
            color=fs.GREY)
    fs.panel_label(ax, "a", dx=-0.20)

    ax = axes[1]
    for arm in ("apo", "cognate"):
        d = aa[aa.arm == arm]
        ax.scatter(d.plddt_at_anchors, d.rmsd_to_active_ref, s=5,
                   color=fs.ARM_COLOURS[arm], alpha=0.7, linewidths=0,
                   label="%s (n=%d)" % (fs.ARM_LABELS[arm], len(d)), zorder=3)
    r = aa[aa.row_id == RENDER_ROW]
    if len(r):
        ax.scatter(r.plddt_at_anchors, r.rmsd_to_active_ref, s=52,
                   facecolors="none", edgecolors=fs.BLACK, linewidths=1.0,
                   zorder=5)
        ax.annotate("row %d — the BA-5e render\n"
                    u"pLDDT %.2f, %.2f Å from active, %.2f Å from inactive"
                    % (RENDER_ROW, float(r.plddt_at_anchors.iloc[0]),
                       float(r.rmsd_to_active_ref.iloc[0]),
                       float(r.rmsd_to_inactive_ref.iloc[0])),
                    (float(r.plddt_at_anchors.iloc[0]),
                     float(r.rmsd_to_active_ref.iloc[0])),
                    xytext=(-6, -14), textcoords="offset points", fontsize=5,
                    ha="right", color=fs.BLACK)
    ax.set_xlabel("mean pLDDT at the state anchors")
    ax.set_ylabel(u"RMSD to the ACTIVE reference (Å)")
    ax.legend(loc="center left", fontsize=5, borderpad=0.2)
    ax.set_title("the most confident AA2AR row is an apo row on the\n"
                 "inactive reference, not a confidently wrong model",
                 fontsize=6.5)
    fs.panel_label(ax, "b", dx=-0.20)

    paths = fs.save(fig, "s8_aa2ar_case")
    print("S8 ->", paths[0])
    print("  rows %d (%s), flagged by E1/E2 among AA2AR: %s"
          % (len(aa), aa.groupby(["backbone", "arm"]).size().to_dict(),
             sorted(flagged)))
    print("  nearer own reference: %d of %d" % (ncorrect, len(aa)))
    for arm in ("apo", "cognate"):
        d = aa[aa.arm == arm]
        print("   %-8s RMSD to active %.2f-%.2f, to inactive %.2f-%.2f"
              % (arm, d.rmsd_to_active_ref.min(), d.rmsd_to_active_ref.max(),
                 d.rmsd_to_inactive_ref.min(), d.rmsd_to_inactive_ref.max()))
    if len(r):
        print("  render row %d: plddt_mean %.2f, at_anchors %.2f, "
              "rmsd_active %.3f, rmsd_inactive %.3f, arm %s, backbone %s"
              % (RENDER_ROW, r.plddt_mean.iloc[0], r.plddt_at_anchors.iloc[0],
                 r.rmsd_to_active_ref.iloc[0], r.rmsd_to_inactive_ref.iloc[0],
                 r.arm.iloc[0], r.backbone.iloc[0]))
    return paths


if __name__ == "__main__":
    main()
