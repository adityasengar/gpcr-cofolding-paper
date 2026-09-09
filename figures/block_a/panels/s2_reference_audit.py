"""
S2 - the reference set audit.

Every conclusion in Block A is measured against deposited structures, so what
those structures are is load-bearing. This panel is the census.

  a  what the 168 references carry: fusion partners overlapping a predicate
     window, engineered mutations, a bound transducer, a deviation from the
     deposited label - counted separately for the 98 panel PDBs
  b  resolution by deposited state, every structure drawn

CAVEAT C-11: the `construct` column is untrusted corpus-wide (40% of evaluable
PDBs), so `construct_annotation_on_disk` is NOT counted here. Panel a uses only
fields derived from coordinates or from the cached RCSB entry.

FILTER: all 168 rows of 02_references/reference_metadata.csv. No excl_* flag
applies - those are flags on predictions.
"""
exec(open(__file__.replace("s2_reference_audit.py", "_shead.py")).read())
import numpy as np, pandas as pd                            # noqa: E402
import badata as B, figstyle as fs, figpanels as fp         # noqa: E402
import matplotlib.pyplot as plt                             # noqa: E402


def main():
    fs.use_house_style()
    md = B.load("02_references/reference_metadata.csv")
    rp = B.load("02_references/reference_predicates.csv")
    md = md.merge(rp[["pdb_id", "receptor", "deviation", "predicate_call"]],
                  on=["pdb_id", "receptor"], how="left")
    panel = md[md.is_panel.astype(bool)]

    fig = plt.figure(figsize=(fs.W2, 78 * fs.MM), constrained_layout=True)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1.0])
    axa = fig.add_subplot(gs[0, 0]); axb = fig.add_subplot(gs[0, 1])

    attrs = [
        ("has a fusion partner", md.fusion_partner.notna()),
        ("fusion inside the tilt window", md.fusion_in_tilt_window.fillna(False)),
        ("fusion inside the NPxxY window",
         md.fusion_in_npxxy_window.fillna(False)),
        ("construct annotated non-wt on disk",
         md.construct_annotation_on_disk.fillna("wt") != "wt"),
        ("transducer bound", md.transducer_present.fillna(False)),
        ("a predicate window is hit", md.predicate_window_hit.fillna(False)),
        ("RCSB entry cached", md.entry_json_cached.fillna(False)),
        ("deviates from its deposited label", md.deviation.fillna(False)),
    ]
    labels = [a for a, _ in attrs]
    counts = [int(m.sum()) for _, m in attrs]
    fp.count_dots(axa, labels, counts, total=len(md), order_by_count=True,
                  label_gap=0.02,
                  highlight={"fusion inside the tilt window",
                             "fusion inside the NPxxY window",
                             "deviates from its deposited label"})
    pan = {a: int((m & md.is_panel.astype(bool)).sum()) for a, m in attrs}
    ypos = {t.get_text(): t.get_position()[1] for t in axa.get_yticklabels()}
    for lab in labels:
        axa.plot([pan[lab]], [ypos[lab]], marker="|", markersize=7,
                 markeredgewidth=1.1, color=fs.BLACK, zorder=4)
    axa.set_xlabel("reference structures (of %d)" % len(md))
    axa.set_title("what the reference set carries", fontsize=6.5)
    axa.text(0.99, 0.02,
             "| = the same count restricted to the %d panel PDBs.\n"
             "The construct annotation is untrusted corpus-wide (C-11).\n"
             "engineered_mutation_count, engineered_mutation_positions and\n"
             "construct_contradicted_by_rcsb are EMPTY in this drop (0 of 168\n"
             "non-null), so no engineered-mutation count can be shown at all."
             % len(panel), transform=axa.transAxes, ha="right", va="bottom",
             fontsize=4.5, color=fs.GREY)
    fs.panel_label(axa, "a", dx=-0.60)

    fp.strip_violin(axb, md, "state", "resolution_A",
                    order=["active", "inactive"], colours=fs.STATE_COLOURS)
    axb.set_ylabel(u"resolution (Å)")
    axb.set_xlabel("")
    axb.set_xticklabels(["active", "inactive"], rotation=0, ha="center")
    axb.set_title("resolution by deposited state", fontsize=6.5)
    axb.text(0.02, 0.98, "%d of %d references carry no resolution\n"
             "(cryo-EM / NMR entries and uncached PDBs)"
             % (int(md.resolution_A.isna().sum()), len(md)),
             transform=axb.transAxes, ha="left", va="top", fontsize=5,
             color=fs.GREY)
    fs.panel_label(axb, "b", dx=-0.24)

    paths = fs.save(fig, "s2_reference_audit")
    print("S2 ->", paths[0])
    print("  references: %d total, %d panel, %d off-panel"
          % (len(md), len(panel), len(md) - len(panel)))
    for lab, c in zip(labels, counts):
        print("   %-38s %3d/%d   (panel: %d/%d)"
              % (lab, c, len(md), pan[lab], len(panel)))
    print("  resolution: n=%d with a value, median active %.2f / inactive %.2f"
          % (int(md.resolution_A.notna().sum()),
             md[md.state == "active"].resolution_A.median(),
             md[md.state == "inactive"].resolution_A.median()))
    for c in ("engineered_mutation_count", "engineered_mutation_positions",
              "construct_contradicted_by_rcsb"):
        print("   EMPTY COLUMN %-34s non-null %d of %d"
              % (c, int(md[c].notna().sum()), len(md)))
    print("  experimental methods: %s"
          % md.experimental_method.value_counts(dropna=False).to_dict())
    return paths


if __name__ == "__main__":
    main()
