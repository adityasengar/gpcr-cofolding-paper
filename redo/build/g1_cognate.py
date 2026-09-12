#!/usr/bin/env python3
"""g1_cognate.py — consume the cognate map, verify it, and resolve the keyed column.

`COUPLING.md` landed with a decision from Aditya: **read the subtype off the
structure the receptor was solved with.**  Two artefacts carry it --
`coupling_cognate_map.tsv` (64 rows) and `coupling_cognate_rungs.tsv`
(54 receptors x 7 rungs = 378 rows).  This script:

  1. **Verifies the map against our own sources before using any of it.**  A
     sibling's table is a claim sheet like any other.  Five checks, all of which
     must pass: slug set, family vocabulary, per-rung sha/sequence/length against
     `seq_rungs.tsv`, Rule-R active PDB and CORE-32 flag against
     `g1_receptors.tsv`.
  2. Emits `g1_cognate.tsv`: receptor x rung -> sha256, with the **evidence class
     carried per row** so a structure read and a convention fallback can never be
     confused in a downstream table.
  3. For the ten receptors the rule deliberately stops on -- cross-family
     chimeras -- emits the **three** options side by side rather than picking:
     A = the alpha5 tip's family, B = the mini-Gs scaffold's family, C = the
     deposited tip itself (our `g1_refchimera.tsv` arm, the matched control).
     Aditya chooses; this file makes all three hashable.
  4. Defines **G10_SCAN**, which the coupling session correctly left to us
     because it is a set definition and not a coupling question.

Usage:  python3 redo/build/g1_cognate.py
Exit:   0 if every verification check passes, 1 otherwise.
"""
import csv
import os
import sys
from collections import Counter, defaultdict

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
OUT = os.path.join(INPUTS, "g1_cognate.tsv")

# The declared representative subtype for a family, used ONLY where the map
# itself hands us a family rather than a subtype (the chimera options).  Same
# convention the coupling session used for its CONVENTION_FALLBACK rows.
FAMILY_REP = {"Gs": "Gs", "Gi/o": "Gi1", "Gq/11": "Gq", "G12/13": "G13"}

RUNGS = ["R1_ct11", "R2_ct15", "R3_ct21", "R4_a5helix", "R5_a5plus",
         "R6a_da5", "R7_full"]
# G10 (E1.5) scans 21 alanine substitutions on a 21-residue chain.  For the 21
# variants to be ONE construct series rather than five, every receptor in the
# scan must share one cognate subtype.  Rule, pre-registrable and using no
# quantity computed from any prediction:
#   the CORE-32 receptors whose cognate subtype is the panel's largest group AND
#   whose evidence class is STRUCTURE_EXACT, ranked by worse-reference
#   resolution, ties alphabetical, take 10.
G10_N = 10
G10_EVIDENCE = "STRUCTURE_EXACT"


def tsv(name):
    with open(os.path.join(INPUTS, name)) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main():
    problems = []
    for f in ("coupling_cognate_map.tsv", "coupling_cognate_rungs.tsv",
              "seq_rungs.tsv", "g1_receptors.tsv", "g1_refchimera.tsv"):
        if not os.path.exists(os.path.join(INPUTS, f)):
            problems.append(f"{f}: absent")
    if problems:
        sys.stderr.write("!! " + "\n!! ".join(problems) + "\n")
        return 1

    cmap = {r["receptor_slug"]: r for r in tsv("coupling_cognate_map.tsv")}
    crungs = tsv("coupling_cognate_rungs.tsv")
    seq = {(r["family"], r["rung"]): r for r in tsv("seq_rungs.tsv")}
    rec = {r["slug"]: r for r in tsv("g1_receptors.tsv")}
    chim = {r["slug"]: r for r in tsv("g1_refchimera.tsv")
            if r["is_rule_r_reference"] == "active"}

    # ---- VERIFY (1) ------------------------------------------------------
    if set(cmap) != set(rec):
        problems.append(f"slug set differs from g1_receptors.tsv: "
                        f"only-map={sorted(set(cmap)-set(rec))} "
                        f"only-ours={sorted(set(rec)-set(cmap))}")
    fams = {f for f, _ in seq}
    orphan = sorted({r["seq_rungs_family"] for r in cmap.values()
                     if r["seq_rungs_family"]} - fams)
    if orphan:
        problems.append(f"seq_rungs_family values with no rung table: {orphan}")
    for r in crungs:
        src = seq.get((r["seq_rungs_family"], r["rung"]))
        if src is None:
            problems.append(f"{r['receptor_slug']}/{r['rung']}: "
                            f"({r['seq_rungs_family']},{r['rung']}) not in seq_rungs.tsv")
            continue
        for col, ours in (("sha256", src["sha256"]), ("sequence", src["sequence"]),
                          ("len", src["len"])):
            if r[col] != ours:
                problems.append(f"{r['receptor_slug']}/{r['rung']}: {col} disagrees "
                                f"with seq_rungs.tsv")
    for slug, r in cmap.items():
        p = rec[slug]
        if r["rule_r_active_pdb"] and r["rule_r_active_pdb"] != p["active_pdb"]:
            problems.append(f"{slug}: map Rule-R active {r['rule_r_active_pdb']} vs "
                            f"PANEL.md {p['active_pdb']}")
        if r["in_core32_provisional"] != p["core32_provisional"]:
            problems.append(f"{slug}: CORE-32 flag disagrees")

    # ---- G10_SCAN --------------------------------------------------------
    core = [s for s in rec if rec[s]["core32_provisional"] == "yes"]
    biggest = Counter(cmap[s]["seq_rungs_family"] for s in core
                      if cmap[s]["seq_rungs_family"]).most_common(1)[0][0]
    pool = [s for s in core if cmap[s]["seq_rungs_family"] == biggest
            and cmap[s]["evidence_class"] == G10_EVIDENCE]
    g10 = sorted(sorted(pool, key=lambda s: (float(rec[s]["worse_res"]), s))[:G10_N])
    if len(g10) < G10_N:
        problems.append(f"G10_SCAN has only {len(g10)} members")

    # ---- emit ------------------------------------------------------------
    rows = []
    bysl = defaultdict(dict)
    for r in crungs:
        bysl[r["receptor_slug"]][r["rung"]] = r
    for slug in sorted(cmap):
        m = rec[slug]
        c = cmap[slug]
        opt = {}
        if c["verdict"] == "needs_decision":
            # " (Gq/11)" -> family Gq/11 ; "Gs (Gs)" -> family Gs
            def fam_of(field):
                v = c[field]
                return v[v.find("(") + 1:v.find(")")] if "(" in v else v.strip()
            opt = {"A": FAMILY_REP.get(fam_of("chimera_option_a_tip"), ""),
                   "B": FAMILY_REP.get(fam_of("chimera_option_b_scaffold"), "")}
        for rung in RUNGS:
            src = bysl.get(slug, {}).get(rung)
            row = dict(
                receptor_slug=slug, rung=rung,
                in_core32_provisional=m["core32_provisional"],
                in_g10_scan="yes" if slug in g10 else "no",
                cognate_family=c["cognate_family"],
                cognate_subtype=c["seq_rungs_family"],
                cognate_accession=c["cognate_accession"],
                evidence_class=c["evidence_class"], verdict=c["verdict"],
                rule_r_active_pdb=c["rule_r_active_pdb"],
                reverses_blockb_prior="yes" if c["reverses_prior"] else "no",
                blockb_prior=c["blockb_prior"],
                len=src["len"] if src else "",
                sha256=src["sha256"] if src else "PENDING:PI-DECISION",
                option_a_tip_subtype=opt.get("A", ""),
                option_a_sha256=(seq[(opt["A"], rung)]["sha256"]
                                 if opt.get("A") else ""),
                option_b_scaffold_subtype=opt.get("B", ""),
                option_b_sha256=(seq[(opt["B"], rung)]["sha256"]
                                 if opt.get("B") else ""),
                option_c_deposited_tip_sha256="",
                # 2026-09-12: raised from 200.  A silent truncation looks exactly
                # like a complete note, and coupling_cognate_map.py's R-COG-9
                # notes now lead with the CAUSE of a non-canonical tip, which is
                # the half a reader most needs and the half 200 chars cut off.
                caveat=c["note"][:600])
            if opt and slug in chim:
                if rung == "R1_ct11" and chim[slug]["ct11"]:
                    row["option_c_deposited_tip_sha256"] = "see g1_partner_registry "
                    row["option_c_deposited_tip_sha256"] += f"reftip_ct11/{slug}"
                elif rung == "R3_ct21" and chim[slug]["ct21"].isalpha():
                    row["option_c_deposited_tip_sha256"] = f"reftip_ct21/{slug}"
            rows.append(row)

    cols = list(rows[0].keys())
    with open(OUT, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[c]) for c in cols) + "\n")

    # ---- report ----------------------------------------------------------
    w = sys.stderr.write
    w(f"# wrote {len(rows)} receptor x rung resolutions -> {OUT}\n")
    w(f"# verdicts: {dict(Counter(c['verdict'] for c in cmap.values()))}\n")
    w(f"# evidence: {dict(Counter(c['evidence_class'] for c in cmap.values()))}\n")
    w(f"# subtypes: {dict(Counter(c['seq_rungs_family'] or 'PENDING' for c in cmap.values()))}\n")
    hashable = {r['receptor_slug'] for r in rows if not r['sha256'].startswith('PENDING')}
    w(f"# hashable receptors: {len(hashable)} of {len(cmap)}\n")
    nd = sorted({r['receptor_slug'] for r in rows if r['sha256'].startswith('PENDING')})
    w(f"# needs_decision: {nd}\n")
    w(f"#   of which in CORE-32: {sorted(s for s in nd if rec[s]['core32_provisional']=='yes')}\n")
    w(f"# reverses Block B prior: "
      f"{sorted(s for s,c in cmap.items() if c['reverses_prior'])}\n")
    w(f"# CORE-32 by subtype: "
      f"{dict(Counter(cmap[s]['seq_rungs_family'] or 'PENDING' for s in core))}\n")
    w(f"# CORE32_GS = {sorted(s for s in core if cmap[s]['seq_rungs_family']=='Gs')}\n")
    w(f"# CORE32_Gio = {len([s for s in core if cmap[s]['seq_rungs_family'] in ('Gi1','Gi3','Go','Gz','Gt1')])}\n")
    w(f"# G10_SCAN ({biggest}, {G10_EVIDENCE}, best worse-reference resolution): {g10}\n")

    if problems:
        w("\n!! PROBLEMS\n" + "\n".join("  " + p for p in problems) + "\n")
        return 1
    w("# MAP VERIFIED: slug set, family vocabulary, per-rung sha/sequence/length,\n"
      "#   Rule-R active PDB and CORE-32 flags all reproduce against our sources\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
