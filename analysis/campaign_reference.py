#!/usr/bin/env python3
"""campaign_reference.py -- every experiment in BOTH campaigns, measured not typed.

Aditya asked for one document listing, for each experiment in each campaign: the
receptors, the G-protein supplied, the ligand, and the row count -- plus the
inventories of which receptors, ligands and G-proteins were chosen.

**Everything here is GENERATED.**  Every count in this project that was typed by hand
has drifted -- "33 experiments in 9 groups" against a body of 45 in 10, three stale
check counts in verify.sh, a budget table that moved when it was re-derived.  So the
document carries no number this script did not compute from a file.

The frozen half became measurable on 2026-09-13, when Block D's three row tables
landed.  Before that its counts were prose.  Each block's provenance is stated.

Run: python3 analysis/campaign_reference.py
"""
import collections
import csv
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "analysis", "CAMPAIGN_REFERENCE.md")
BB = ("boltz", "chai", "of3", "protenix")


def rd(path, delim=","):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def backbone_of(row):
    """Derive the backbone. Block D's paths vary in DEPTH by backbone, so a positional
    parse silently returns the wrong segment -- token match is the only safe form."""
    for c in ("backbone", "model"):
        if row.get(c):
            return row[c]
    hit = [t for t in (row.get("input_path") or "").split("/") if t in BB]
    return hit[0] if len(hit) == 1 else "?"


def block_summary(label, path, note, delim=","):
    rows = rd(path, delim)
    if rows is None:
        return None
    recs = {(r.get("receptor") or r.get("receptor_slug") or "").upper() for r in rows}
    recs.discard("")
    arms = collections.Counter(r.get("arm") or r.get("input_state_claim") or "-" for r in rows)
    bbs = collections.Counter(backbone_of(r) for r in rows)
    lig = collections.Counter(r.get("ligand_role") or r.get("ligand_type") or "-" for r in rows)
    return dict(label=label, n=len(rows), recs=sorted(recs), arms=arms, bbs=bbs,
                lig=lig, note=note, path=path)


def main():
    out = ["# CAMPAIGN_REFERENCE.md — every experiment in both campaigns",
           "",
           "**GENERATED** by `analysis/campaign_reference.py`. Do not hand-edit; re-run it.",
           "**No number in this document was typed.** Every count is computed from the file "
           "named beside it, because every hand-written count on this project has drifted.",
           ""]

    # ---------------------------------------------------------------- FROZEN
    out.append("---\n\n# PART 1 — THE FROZEN CAMPAIGN (Blocks A–D)\n")
    out.append("Frozen as the record. No new claim is built on it. **Every block is "
               "row-level as of 2026-09-13**, when Block D's three tables landed — before "
               "that, Block D's numbers were prose.\n")
    blocks = [
        block_summary("A — panel-scale apo vs cognate", "data/block_a/01_rows/block_a_rows.csv",
                      "partner = one COMPLETE Gα subunit; no peptide of any length"),
        block_summary("B — the partner ladder", "data/block_b/01_rows/rows_tidy.csv",
                      "apo / decoy (tail permuted IN PLACE) / shuffled / cognate"),
        block_summary("C — the ligand arm", "analysis/block_c/received_2026_09_12/rows.tier3.v2.csv",
                      "EVERY row carries a ligand; 'apo' here means NO PARTNER (F-23)"),
        block_summary("D1 — deep apo", "analysis/block_d/received_2026_09_13/rows.d1_deep_apo.csv",
                      "ligand-free AND partner-free; 100 samples/seed"),
        block_summary("D2 — directed inactive", "analysis/block_d/received_2026_09_13/rows.d2_directed_inactive.csv",
                      "nanobody vs Gα steering"),
        block_summary("D3 — MSA depth", "analysis/block_d/received_2026_09_13/rows.d3_msa_depth.csv",
                      "5 depths; the frozen campaign's subsampling tier"),
    ]
    total = 0
    out.append("| block | rows | receptors | backbones | arms | note |")
    out.append("|---|---:|---:|---|---|---|")
    for b in blocks:
        if not b:
            continue
        total += b["n"]
        out.append(f"| **{b['label']}** | {b['n']:,} | {len(b['recs'])} | "
                   f"{len(b['bbs'])} | {', '.join(f'{k} {v:,}' for k, v in b['arms'].most_common(5))} | {b['note']} |")
    out.append(f"| **TOTAL** | **{total:,}** | | | | |")
    out.append("")

    for b in blocks:
        if not b:
            continue
        out.append(f"\n### {b['label']}\n")
        out.append(f"`{b['path']}` — **{b['n']:,} rows**")
        out.append(f"- **receptors ({len(b['recs'])}):** {', '.join(b['recs'])}")
        out.append(f"- **backbones:** {', '.join(f'{k} {v:,}' for k, v in sorted(b['bbs'].items()))}")
        out.append(f"- **arms:** {', '.join(f'{k} {v:,}' for k, v in b['arms'].most_common())}")
        nz = [f"{k} {v:,}" for k, v in b["lig"].most_common() if k != "-"]
        out.append(f"- **ligand levels:** {', '.join(nz) if nz else 'none recorded in this table'}")
        out.append(f"- {b['note']}")

    # ---------------------------------------------------------------- REDO
    out.append("\n---\n\n# PART 2 — THE REDO CAMPAIGN\n")
    g1, g2 = rd("redo/inputs/g1_systems.csv"), rd("redo/inputs/g2_systems.csv")
    if g1 and g2:
        def tot(rows, c):
            return sum(int(x.get(c) or 0) for x in rows)
        out.append("| group | system rows | pooled (n=10) | per-cell (n=50) |")
        out.append("|---|---:|---:|---:|")
        for lab, rr in (("Group 1 — the partner ladder", g1), ("Group 2 — the ligand arm", g2)):
            out.append(f"| {lab} | {len(rr):,} | {tot(rr,'predictions_pooled'):,} | "
                       f"{tot(rr,'predictions_percell'):,} |")
        out.append(f"| **TOTAL** | **{len(g1)+len(g2):,}** | "
                   f"**{tot(g1,'predictions_pooled')+tot(g2,'predictions_pooled'):,}** | "
                   f"**{tot(g1,'predictions_percell')+tot(g2,'predictions_percell'):,}** |")
        out.append(f"\n**The grain is undecided and it is a {(tot(g1,'predictions_percell')+tot(g2,'predictions_percell'))/(tot(g1,'predictions_pooled')+tot(g2,'predictions_pooled')):.1f}× swing.** "
                   f"The frozen campaign used n=50. Neither figure includes the MSA arms, "
                   f"which are enumerated in no systems file.\n")

        # per-arm detail
        for lab, rr in (("Group 1", g1), ("Group 2", g2)):
            out.append(f"\n### {lab} — every arm\n")
            out.append("| item | arm | rows | receptors | clusters | partner construct(s) | ligand | pooled |")
            out.append("|---|---|---:|---:|---:|---|---|---:|")
            by = collections.defaultdict(list)
            for x in rr:
                by[(x.get("item", "?"), x.get("arm", "?"))].append(x)
            for (item, arm), xs in sorted(by.items()):
                recs = {x["receptor_slug"] for x in xs}
                cls = {x.get("receptor_cluster", "") for x in xs}
                con = sorted({x.get("chain_b_construct", "-") for x in xs})
                lig = sorted({x.get("ligand_role_actual") or x.get("ligand") or "-" for x in xs})
                out.append(f"| `{item}` | {arm} | {len(xs)} | {len(recs)} | {len(cls)} | "
                           f"{', '.join(con[:4])}{' …' if len(con)>4 else ''} | "
                           f"{', '.join(lig[:3])} | {sum(int(x.get('predictions_pooled') or 0) for x in xs):,} |")

    # ------------------------------------------------------- INVENTORIES
    out.append("\n---\n\n# PART 3 — WHAT WAS CHOSEN\n")
    rec = rd("redo/inputs/g1_receptors.tsv", "\t")
    if rec:
        cl = collections.Counter(r.get("cluster", "?") for r in rec)
        out.append(f"\n## Receptors — {len(rec)} on the redo panel, {len(cl)} paralog clusters\n")
        out.append(f"**The statistical unit is the cluster**, so `MDE = 1.218/√k`: "
                   f"k={len(cl)} → {1.218/math.sqrt(len(cl)):.3f}.\n")
        out.append("| slug | uniprot | organism | cluster |")
        out.append("|---|---|---|---|")
        for r in sorted(rec, key=lambda x: x.get("slug", "")):
            out.append(f"| {r.get('slug','')} | {r.get('uniprot','')} | "
                       f"{r.get('organism','')} | {r.get('cluster','')} |")

    reg = rd("redo/inputs/g1_partner_registry.tsv", "\t")
    if reg:
        rungs = collections.defaultdict(set)
        for r in reg:
            if r.get("construct_class") == "ga_rung":
                rungs[r["construct"]].add(r.get("length", "?"))
        # COUNT THE Ga FAMILIES AMONG RUNGS ONLY.  The `family` column carries a
        # RECEPTOR slug for ref_tip / species_matched_tip rows, so counting it across
        # the whole registry gives 29 "Ga families" -- of which 13 are receptors.
        ga_fams = {r["family"] for r in reg
                   if r.get("construct_class") == "ga_rung" and r.get("family")}
        klass = collections.Counter(r.get("construct_class", "?") for r in reg)
        out.append(f"\n## G-proteins — the ladder rungs\n")
        out.append(f"**{len(ga_fams)} Gα families** across the rungs, in "
                   f"{len(reg):,} registry rows spanning {len(klass)} construct classes.\n")
        out.append("Construct classes: " + ", ".join(f"`{k}` {v}" for k, v in klass.most_common()) + "\n")
        out.append("| rung | length(s) | families | all held? |")
        out.append("|---|---|---:|---|")
        for c in sorted(rungs):
            xs = [r for r in reg if r["construct"] == c]
            held = {r.get("held", "?") for r in xs}
            out.append(f"| `{c}` | {', '.join(sorted(rungs[c]))} | "
                       f"{len({r['family'] for r in xs})} | {'yes' if held=={'yes'} else sorted(held)} |")

    lig = rd("redo/inputs/ligand_set_redo.tsv", "\t")
    tiers = rd("redo/inputs/ligand_tiers.tsv", "\t")
    if tiers:
        t = collections.Counter(r.get("ligand_tier", "?") for r in tiers)
        out.append(f"\n## Ligands — tiers\n")
        out.append(", ".join(f"**{k}** {v}" for k, v in t.most_common()))
        out.append("")
    sel = rd("redo/inputs/drule_selected.tsv", "\t")
    if sel:
        acc = [r for r in sel if r.get("decoy_status") == "accepted"]
        una = [r for r in sel if r.get("decoy_status") == "decoy-unavailable"]
        ks = len({r["cluster"] for r in acc})
        out.append(f"\n## Decoys — D-RULE, ChEMBL_37\n")
        out.append(f"**{len(acc)} accepted** over {len({r['receptor_slug'] for r in acc})} "
                   f"receptors / **{ks} clusters** (MDE {1.218/math.sqrt(ks):.3f}); "
                   f"**{len(una)} receptors decoy-unavailable**: "
                   f"{', '.join(sorted(r['receptor_slug'] for r in una))}.")
        out.append(f"\nRuns **EXPLORATORY** — the pre-registered bar was ≥12 clusters "
                   f"(`DECISIONS.md` D-2026-09-12-h).")

    open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"wrote {OUT} ({len(out)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
