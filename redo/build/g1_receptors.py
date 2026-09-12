#!/usr/bin/env python3
"""g1_receptors.py — the receptor axis for Group 1, and a PROVISIONAL CORE-32.

RUN_MATRIX.md §10.3 records that the CORE-32 slug list is owed by PANEL.md and is
"the one artefact §7 cannot run without".  It has not landed.  Rather than leave
the Group 1 system table without a receptor axis, this file applies RUN_MATRIX
§3.1's own written rule to PANEL.md's own tier-C1 table and marks the result
**PROVISIONAL**.  PANEL.md remains the authority; when its frozen list lands,
rerun `g1_systems.py` and the difference is a diff, not a rewrite.

RUN_MATRIX §3.1, quoted: "Group the survivors by the `cluster_id` paralog label
... From each cluster take exactly **one** member: the one whose *worse-resolution*
reference structure has the lowest resolution in the snapshot; ties broken by
alphabetical receptor slug."

Implemented as: for each receptor take max(active_res, inactive_res) -- the worse
of its two rule-R references -- and within each cluster take the receptor whose
max is numerically smallest; ties alphabetical.

Sources:
  * `redo/spec/PANEL.md` §6.1, the rendered tier-C1 table (64 rows), which is
    the output of PANEL.md's Rule R and carries the chosen PDB and resolution.
  * `redo/inputs/panel_systems.csv` for the cluster label, UniProt accession and
    organism -- cross-checked against the parsed table, row for row.

Usage:  python3 redo/build/g1_receptors.py
"""
import csv
import os
import re
import sys

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
PANEL_MD = os.path.join(SPEC, "PANEL.md")
PANEL_CSV = os.path.join(INPUTS, "panel_systems.csv")

REF = re.compile(r"^\s*(\S+)\s+([0-9.]+)\s*Å")


def parse_c1():
    """Rows of PANEL.md §6.1 -> list of dicts. Section-delimited, not line-counted."""
    text = open(PANEL_MD).read().splitlines()
    try:
        start = next(i for i, l in enumerate(text)
                     if l.startswith("## 6.1 Tier C1"))
        end = next(i for i, l in enumerate(text[start + 1:], start + 1)
                   if l.startswith("## "))
    except StopIteration:
        raise RuntimeError("PANEL.md §6.1 not found -- the parser is pinned to a "
                           "heading that moved; fix before trusting any output")
    out = []
    for line in text[start:end]:
        if not line.startswith("|"):
            continue
        f = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(f) < 12 or not f[0].isdigit():
            continue
        slug = f[1].replace("*", "").strip()
        am, im = REF.match(f[6]), REF.match(f[7])
        out.append(dict(
            n=int(f[0]), slug=slug, uniprot=f[2], gpcrdb=f[3].strip("`"),
            gclass=f[4], cluster=f[5].strip("`"),
            active_pdb=am.group(1) if am else "", active_res=float(am.group(2)) if am else None,
            inactive_pdb=im.group(1) if im else "", inactive_res=float(im.group(2)) if im else None,
            in_=f[8], qc=f[9], postcut=f[10], ligands=f[11]))
    return out


def main():
    c1 = parse_c1()
    problems = []
    if len(c1) != 64:
        problems.append(f"parsed {len(c1)} tier-C1 rows, expected 64")

    csvrows = {r["slug"]: r for r in csv.DictReader(open(PANEL_CSV))}
    for r in c1:
        c = csvrows.get(r["slug"])
        if c is None:
            problems.append(f"{r['slug']}: in PANEL.md §6.1 but not in panel_systems.csv")
            continue
        if not c["tier"].startswith("C1"):
            problems.append(f"{r['slug']}: panel_systems.csv tier={c['tier']!r}, not C1")
        if c["cluster_gpcrdb_fam3"] != r["cluster"]:
            problems.append(f"{r['slug']}: cluster {r['cluster']} (md) vs "
                            f"{c['cluster_gpcrdb_fam3']} (csv)")
        if c["uniprot_acc"] != r["uniprot"]:
            problems.append(f"{r['slug']}: uniprot {r['uniprot']} (md) vs "
                            f"{c['uniprot_acc']} (csv)")
        r["organism"] = c["organism"]
        r["paralog"] = c["paralog_cluster"]
        r["blockc_roles"] = sum(1 for k in ("blockc_agonist", "blockc_antagonist",
                                            "blockc_decoy") if c[k] not in ("", "0"))

    missing_res = [r["slug"] for r in c1
                   if r["active_res"] is None or r["inactive_res"] is None]
    if missing_res:
        problems.append(f"no parsed resolution for {missing_res}")

    # RUN_MATRIX §3.1: worse-of-two reference resolution, min per cluster,
    # ties alphabetical.
    clusters = {}
    for r in c1:
        if r["active_res"] is None or r["inactive_res"] is None:
            continue
        r["worse_res"] = max(r["active_res"], r["inactive_res"])
        clusters.setdefault(r["cluster"], []).append(r)
    core32 = []
    for cl, members in sorted(clusters.items()):
        pick = sorted(members, key=lambda r: (r["worse_res"], r["slug"]))[0]
        pick["core32_provisional"] = "yes"
        core32.append(pick)
    for r in c1:
        r.setdefault("core32_provisional", "no")

    if len(core32) != 32:
        problems.append(f"provisional CORE-32 has {len(core32)} members, expected 32")

    cols = ["n", "slug", "uniprot", "gpcrdb", "gclass", "cluster", "paralog",
            "organism", "active_pdb", "active_res", "inactive_pdb", "inactive_res",
            "worse_res", "core32_provisional", "qc", "postcut", "blockc_roles",
            "ligands"]
    out = os.path.join(INPUTS, "g1_receptors.tsv")
    with open(out, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in sorted(c1, key=lambda r: r["n"]):
            fh.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")

    sys.stderr.write(f"# parsed {len(c1)} tier-C1 receptors, {len(clusters)} clusters\n")
    sys.stderr.write(f"# provisional CORE-32 ({len(core32)}): "
                     + " ".join(sorted(r["slug"] for r in core32)) + "\n")
    nonhuman = [r["slug"] for r in c1 if "Homo sapiens" not in r.get("organism", "")]
    sys.stderr.write(f"# non-human on C1: {nonhuman}\n")
    sys.stderr.write(f"# non-human inside provisional CORE-32: "
                     f"{[r['slug'] for r in core32 if 'Homo sapiens' not in r.get('organism','')]}\n")
    sys.stderr.write(f"# CORE-32 with all three Block C ligand roles: "
                     f"{sum(1 for r in core32 if r.get('blockc_roles') == 3)}\n")
    if problems:
        sys.stderr.write("\n!! PROBLEMS\n" + "\n".join("  " + p for p in problems) + "\n")
        return 1
    sys.stderr.write(f"# wrote {out}\n# all cross-checks against panel_systems.csv passed\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
