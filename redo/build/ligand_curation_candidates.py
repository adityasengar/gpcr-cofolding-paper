#!/usr/bin/env python3
"""Extract candidate small-molecule agonist/antagonist pairs for the D-C worklist.

Decision D-C (2026-09-12): curate small-molecule pairs for the seven receptors
that have the modality but not the curation, taking the interaction arm from
k = 8 clusters (MDE 0.431) to k = 15 (MDE 0.314) for zero GPU.

This does not curate. It assembles the CANDIDATES a human curator chooses from,
from a source that is already frozen and already cited elsewhere in the panel
work: `lit/panels/cache/gpcrdb_structures.json`, the GPCRdb snapshot whose sha256
`PANEL.md` §10 pins. Reaching for a live database would introduce a second,
unpinned provenance for one column of one arm.

WHAT COUNTS. A candidate is a ligand recorded on a deposited structure of that
receptor with `type == "small-molecule"` and a non-empty SMILES. Function is read
from GPCRdb's own `function` field; anything that is not clearly agonist-like or
antagonist-like is reported under `other` rather than guessed at.

WHAT THIS DELIBERATELY DOES NOT DO. It does not pick. Affinity, assay provenance
and the agonist/antagonist call are curation judgements, and `ligand_set.csv`'s
schema wants `affinity_metric`, `affinity_value_nM` and `affinity_source` — none
of which are in the snapshot. The output is a worksheet, not a result.

    python3 redo/build/ligand_curation_candidates.py
"""

import csv
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, repo

SNAP = repo("lit", "panels", "cache", "gpcrdb_structures.json")
OUT = os.path.join(INPUTS, "ligand_curation_candidates.tsv")

# D-C worklist. OPSD and B1B1U5 are carried but flagged: both are retinal
# receptors whose agonist and antagonist are the same molecule in different
# isomers, covalently bound. PANEL.md §10 records them among four Block C could
# not run, "and the reason is chemical, not operational."
WORKLIST = {
    "S1PR1":  ("both",       ""),
    "CCKAR":  ("agonist",    "curated agonist is CCK-8 peptide"),
    "GHSR":   ("both",       "curated agonist is ghrelin peptide"),
    "ADRB1":  ("antagonist", "placeholder row, no SMILES/PDB"),
    "HRH3":   ("agonist",    "placeholder row, no SMILES/PDB"),
    "OPSD":   ("antagonist", "RETINAL - agonist/antagonist are isomers of one covalent ligand"),
    # D-H CLOSED 2026-09-12 (c'): 9EPP is the reference. That UNBLOCKS the
    # reference question and NARROWS the chemistry one -- it does not close it.
    # 9EPP's agonist is 11,20-ethanoretinal, CCD A1H6M, which is a DIFFERENT CCD
    # from the 11-cis retinal (RET) inverse agonist on our inactive reference
    # 6I9K, so F-11's "one CCD, two pharmacologies" trap does not bite this pair.
    # What is still open is the standing curation policy, not the chemistry: the
    # delivered ligand_set carries B1B1U5's antagonist as a deliberate NA under
    # amendment C-1 ("inverse_agonist state dropped from Tier 3"), and 11-cis
    # retinal is an inverse agonist, not a neutral antagonist.
    "B1B1U5": ("antagonist",
               "RETINAL - D-H closed on 9EPP, so the reference is settled and the "
               "9EPP agonist (11,20-ethanoretinal, CCD A1H6M) is a DIFFERENT CCD "
               "from the 6I9K inverse agonist (11-cis retinal, CCD RET). Residual "
               "blocker is policy, not chemistry: amendment C-1 dropped "
               "inverse_agonist from Tier 3 and this receptor has no neutral "
               "antagonist. Curate by ISOMER, never by CCD (F-11)"),
}

AGO = ("agonist", "partial agonist", "full agonist", "agonist-partial")
ANT = ("antagonist", "inverse agonist", "antagonist-inverse")


def role_of(fn):
    f = (fn or "").strip().lower()
    if not f:
        return "unknown"
    if any(a in f for a in ANT):          # check antagonist first: "inverse agonist"
        return "antagonist"
    if any(a in f for a in AGO):
        return "agonist"
    return "other"


def main():
    snap = json.load(open(SNAP))
    slugs = {r["slug"]: r.get("gpcrdb_slug", "") for r in
             csv.DictReader(open(os.path.join(INPUTS, "panel_systems.csv")))}
    ourrefs = {}
    with open(os.path.join(INPUTS, "g1_receptors.tsv")) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            ourrefs[r["slug"]] = {str(r.get("active_pdb", "")).upper(),
                                  str(r.get("inactive_pdb", "")).upper()} - {""}

    # Match on the slug PREFIX and keep EVERY species.
    #
    # HANDOVER.md: "Never let `_human` be a silent default when resolving a
    # receptor slug." That bug once made our OPSD pair look cross-species when
    # both entries are opsd_bovin. It is live here: the snapshot holds BOTH
    # `adrb1_human` and `adrb1_melga` (turkey), and PANEL.md records that
    # ConfoRNets uses the turkey entry on both sides of its ADRB1 pair. Silently
    # taking _human would curate a ligand against the wrong organism's structure.
    want = {}
    known = {e_prot for e_prot in (str(x.get("protein", "")).lower() for x in snap)}
    for s in WORKLIST:
        g = (slugs.get(s, "") or "").lower()
        if not g:
            continue
        for prot in known:
            if prot == g or prot.startswith(g + "_"):
                want[prot] = s

    found = defaultdict(list)
    for e in snap:
        prot = str(e.get("protein", "")).lower()
        if prot not in want:
            continue
        slug = want[prot]
        for lg in e.get("ligands") or []:
            if (lg.get("type") or "") != "small-molecule":
                continue
            smi = (lg.get("SMILES") or "").strip()
            if not smi:
                continue
            found[slug].append({
                "receptor": slug,
                "role_gpcrdb": role_of(lg.get("function")),
                "function_raw": lg.get("function") or "",
                "ligand_name": lg.get("name") or "",
                "ligand_ccd": lg.get("PDB") or "",
                "bound_pdb": e.get("pdb_code") or "",
                "state": e.get("state") or "",
                "resolution": e.get("resolution") or "",
                "species": e.get("species") or "",
                "smiles": smi,
                "is_our_reference": "",
            })

    rows, summary = [], []
    for slug, (need, note) in WORKLIST.items():
        cands = found.get(slug, [])
        # De-duplicate on (role, ccd, smiles). Rank by: is this one of OUR OWN
        # reference structures, then resolution.
        #
        # The reference-first tiebreak is not cosmetic. Histamine appears on HRH3's
        # 8YUU and 8YN5 at the SAME 2.7 A; a resolution-only rule kept whichever
        # came first and silently discarded 8YN5 -- which is the panel's own active
        # reference. A ligand already bound to the structure we score against is
        # strictly better provenance than an equally-resolved stranger.
        seen = {}
        for c in cands:
            k = (c["role_gpcrdb"], c["ligand_ccd"], c["smiles"])
            try:
                r = float(c["resolution"])
            except (TypeError, ValueError):
                r = 99.0
            rank = (0 if c["bound_pdb"].upper() in ourrefs.get(slug, set()) else 1, r)
            if k not in seen or rank < seen[k][0]:
                seen[k] = (rank, c)
        uniq = [c for _, c in sorted(seen.values(), key=lambda t: t[0])]
        n_ag = sum(1 for c in uniq if c["role_gpcrdb"] == "agonist")
        n_an = sum(1 for c in uniq if c["role_gpcrdb"] == "antagonist")
        for c in uniq:
            c["is_our_reference"] = ("yes" if c["bound_pdb"].upper() in ourrefs.get(slug, set())
                                     else "")
            c["needed"] = need
            c["curation_note"] = note
            rows.append(c)
        summary.append((slug, need, n_ag, n_an, len(uniq), note))

    cols = ["receptor", "needed", "role_gpcrdb", "function_raw", "ligand_name",
            "ligand_ccd", "bound_pdb", "is_our_reference", "state", "resolution",
            "species", "smiles", "curation_note"]
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"  source: {os.path.relpath(SNAP)} (frozen snapshot, {len(snap)} structures)")
    print(f"  wrote {os.path.relpath(OUT)} — {len(rows)} candidate ligands\n")
    print(f"  {'receptor':<9}{'needed':<11}{'agonist':>8}{'antag':>7}{'total':>7}  note")
    for slug, need, a, n, t, note in summary:
        flag = "" if (a or n) else "   <-- NOTHING FOUND"
        print(f"  {slug:<9}{need:<11}{a:>8}{n:>7}{t:>7}  {note[:44]}{flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
