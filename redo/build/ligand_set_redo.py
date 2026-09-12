#!/usr/bin/env python3
"""Enact D-C's ligand picks -- the redo's agonist/antagonist table.

LIGAND_CURATION_PROPOSAL.md proposed seven picks and then said every row "still
needs an affinity attached".  It does not: Aditya dissolved that requirement on
2026-09-12 -- ligand identity is evidenced STRUCTURALLY, because the molecule is
co-crystallised in an active or inactive receptor, which is a stronger claim than
an assay number.  So the picks are enactable now and this script enacts them.

The selection rule is not re-implemented here.  It ran in
ligand_curation_candidates.py and its output is the candidate table; this script
records WHICH candidate was taken and refuses any pick that is not in it.  A pick
that cannot be traced to a candidate row is a typo, and typos in a ligand table
are how a 40-46% curation error rate happens.

    python3 redo/build/ligand_set_redo.py
    python3 redo/build/manifest.py

Writes: inputs/ligand_set_redo.tsv
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS  # noqa: E402

OUT = os.path.join(INPUTS, "ligand_set_redo.tsv")

# (receptor, role, ligand_ccd, bound_pdb) -> why this one.  Every tuple must
# resolve to exactly one row of ligand_curation_candidates.tsv.
PICKS = [
    ("S1PR1", "full_agonist", "J8C", "7TD4",
     "our ACTIVE reference; siponimod, co-crystallised in the structure we score against"),
    ("S1PR1", "neutral_antagonist", "ML5", "3V2Y",
     "our INACTIVE reference; W146"),
    ("HRH3", "full_agonist", "HSM", "8YN5",
     "our ACTIVE reference; histamine. 8YUU ties on resolution (2.7 A) and is NOT "
     "our reference -- the is-our-reference tiebreak exists because of this pair"),
    ("GHSR", "full_agonist", "1KD", "7NA8",
     "ibutamoren, same deposition as our active reference 7NA7"),
    ("GHSR", "neutral_antagonist", "8QX", "6KO5",
     "our INACTIVE reference"),
    ("CCKAR", "full_agonist", "IA1", "7XOV",
     "OFF-REFERENCE and the only small-molecule agonist candidate on the panel's "
     "receptor. 7MBX's ligand is typed protein by GPCRdb (the CCK-8 peptide), so "
     "no on-reference small molecule exists. Needs the most scrutiny of the seven"),
]

# Not enacted, and why.  Carried in the output so the absence is legible.
BLOCKED = [
    ("ADRB1", "neutral_antagonist",
     "POLICY, the same blocker as B1B1U5 -- and LIGAND_CURATION_PROPOSAL.md listed "
     "this among the straightforward picks, which was wrong. Carazolol (CAU, 7BVQ, "
     "2.5 A) is on our own inactive reference and is human, but GPCRdb types it "
     "'Inverse agonist', not a neutral antagonist, and amendment C-1 dropped "
     "inverse_agonist from Tier 3. Every candidate GPCRdb types a true 'Antagonist' "
     "-- P32 4BVN 2.1 A, 3WC 3ZPR, XF5 3ZPQ, I32 2YCZ -- is Meleagris gallopavo, "
     "and our ADRB1 is human (P08588); the standing rule is that species follows "
     "the panel. So the choice is reopen C-1 for an inverse agonist, or accept a "
     "cross-species antagonist. Aditya's call, not a curation judgement."),
    ("OPSD", "both",
     "CHEMISTRY. Agonist and antagonist are the same molecule -- retinal, CCD RET "
     "-- in different isomers, covalently bound through a Schiff base. One code "
     "carries two opposite pharmacologies (F-11). Separately, the active reference "
     "4X1H carries a DETERGENT (BNG) and no agonist at all."),
    ("B1B1U5", "antagonist",
     "POLICY, not chemistry. F-11's one-CCD trap does NOT bite this pair: 9EPP's "
     "agonist is 11,20-ethanoretinal (A1H6M), a different CCD from the 11-cis "
     "retinal (RET) inverse agonist on our inactive reference 6I9K. The blocker is "
     "that amendment C-1 dropped inverse_agonist from Tier 3 and this receptor has "
     "no neutral antagonist. Reopening C-1 here is Aditya's call, not curation."),
]


def main():
    with open(os.path.join(INPUTS, "ligand_curation_candidates.tsv")) as fh:
        cands = list(csv.DictReader(fh, delimiter="\t"))
    with open(os.path.join(INPUTS, "g1_receptors.tsv")) as fh:
        organism = {r["slug"]: r["organism"] for r in csv.DictReader(fh, delimiter="\t")}

    try:
        from rdkit import Chem
        from rdkit import RDLogger
        RDLogger.DisableLog("rdApp.*")
    except ImportError:
        Chem = None
        print("NOTE: rdkit unavailable -- inchikey and canonical_smiles left blank")

    rows, problems = [], []
    for rec, role, ccd, pdb, why in PICKS:
        hits = [c for c in cands if c["receptor"] == rec
                and c["ligand_ccd"] == ccd and c["bound_pdb"] == pdb]
        if len(hits) != 1:
            problems.append(f"{rec}/{ccd}@{pdb}: {len(hits)} candidate rows, expected 1")
            continue
        c = hits[0]
        # A pick whose assigned role disagrees with GPCRdb's own function label is
        # the error that put carazolol in this table as a neutral antagonist when
        # GPCRdb calls it an inverse agonist.  Refuse it rather than record it.
        fn = c["function_raw"].strip().lower()
        want = {"full_agonist": ("agonist",),
                "neutral_antagonist": ("antagonist",)}[role]
        if fn not in want:
            problems.append(
                f"{rec}/{ccd}@{pdb}: assigned {role} but GPCRdb function_raw is "
                f"'{c['function_raw']}' -- these must agree")
            continue
        smiles = c["smiles"]
        canon = inchikey = ""
        if Chem and smiles:
            m = Chem.MolFromSmiles(smiles)
            if m is None:
                problems.append(f"{rec}/{ccd}: SMILES does not parse")
            else:
                canon = Chem.MolToSmiles(m)
                inchikey = Chem.MolToInchiKey(m)
        rows.append({
            "receptor_slug": rec,
            "receptor_organism": organism.get(rec, ""),
            "ligand_role": role,
            "ligand_name": c["ligand_name"],
            "ligand_ccd": ccd,
            "bound_pdb": pdb,
            "bound_pdb_state": c["state"],
            "bound_pdb_resolution": c["resolution"],
            "is_our_reference": c["is_our_reference"] or "no",
            "ligand_species_context": c["species"],
            "gpcrdb_role": c["role_gpcrdb"],
            "gpcrdb_function_raw": c["function_raw"],
            "is_peptide": "0",
            "smiles": smiles,
            "canonical_smiles": canon,
            "inchikey": inchikey,
            "smiles_source": f"CCD:{pdb}:{ccd}",
            "evidence": "structural",
            "affinity_required": "no",
            "status": "enacted",
            "why": why,
        })

    for rec, role, why in BLOCKED:
        rows.append({
            "receptor_slug": rec, "receptor_organism": organism.get(rec, ""),
            "ligand_role": role, "ligand_name": "", "ligand_ccd": "",
            "bound_pdb": "", "bound_pdb_state": "", "bound_pdb_resolution": "",
            "is_our_reference": "", "ligand_species_context": "",
            "gpcrdb_role": "", "gpcrdb_function_raw": "", "is_peptide": "",
            "smiles": "", "canonical_smiles": "", "inchikey": "",
            "smiles_source": "", "evidence": "", "affinity_required": "no",
            "status": "BLOCKED", "why": why,
        })

    if problems:
        for p in problems:
            print("PROBLEM:", p)
        return 1

    cols = list(rows[0].keys())
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    enacted = [r for r in rows if r["status"] == "enacted"]
    onref = [r for r in enacted if r["is_our_reference"] == "yes"]
    print(f"wrote {os.path.relpath(OUT)}  ({len(rows)} rows)")
    print(f"  enacted {len(enacted)} picks across "
          f"{len({r['receptor_slug'] for r in enacted})} receptors")
    print(f"  {len(onref)} sit ON one of our own reference structures")
    print(f"  blocked {len(BLOCKED)}: {', '.join(b[0] for b in BLOCKED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
