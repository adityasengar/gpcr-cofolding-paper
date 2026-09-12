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
    # --- C-1 RELAXED 2026-09-12: these three were blocked solely because their
    # --- off-state ligand is an inverse agonist and amendment C-1 excluded those.
    ("ADRB1", "full_agonist", "P0G", "7BU7",
     "our ACTIVE reference; human. ADRB1 has no plain antagonist at all, only "
     "inverse agonists -- that is why C-1 blocked it, and why relaxing C-1 is "
     "the only thing that could have unblocked it"),
    ("ADRB1", "inverse_agonist", "CAU", "7BVQ",
     "our INACTIVE reference; carazolol, human. Every candidate GPCRdb types a "
     "true 'Antagonist' for ADRB1 is Meleagris gallopavo, so the alternative to "
     "C-1 relaxation was a cross-species pick"),
    ("B1B1U5", "full_agonist", "A1H6M", "9EPP",
     "our ACTIVE reference; 11,20-ethanoretinal, a ring-locked analogue"),
    ("B1B1U5", "inverse_agonist", "RET", "6I9K",
     "our INACTIVE reference; 11-cis retinal. Different CCD from the agonist, so "
     "F-11's one-CCD trap does not bite this pair"),
    ("OPSD", "full_agonist", "RET", "5DYS",
     "all-trans retinal. OFF-REFERENCE by necessity: our active reference 4X1H "
     "carries a detergent (BNG) and no agonist at all. SHARES THE CCD 'RET' with "
     "the inverse agonist and is a DIFFERENT MOLECULE -- key by InChIKey, never "
     "by CCD (F-11)"),
    ("OPSD", "inverse_agonist", "RET", "7ZBC",
     "our INACTIVE reference; 11-cis retinal. Same CCD as the agonist, different "
     "isomer, different InChIKey. GPCRdb also labels this exact molecule "
     "'Agonist' at 8A6D -- one molecule, two opposite labels, so the ROLE must "
     "come from this row and never from the ligand name"),
    # --- T2, the peptide tier. Never curated before: the candidates generator
    # --- filtered type == small-molecule, so it returned nothing for these.
    ("C5AR1", "full_agonist", "", "7Y66",
     "BM213 on our ACTIVE reference. A peptide CHAIN -- no SMILES, supplied as a "
     "sequence. T2 by construction"),
    ("C5AR1", "neutral_antagonist", "", "6C1R",
     "PMX53 on our INACTIVE reference. Note 6C1R also carries avacopan as a NAM; "
     "the allosteric co-ligand is NOT supplied and is recorded here so that is "
     "a decision rather than an omission"),
    ("SSR2", "full_agonist", "", "7T10",
     "somatostatin on our ACTIVE reference; a chain"),
    ("SSR2", "neutral_antagonist", "", "7XNA",
     "CYN 154806, a peptide chain, OFF-REFERENCE by necessity: our inactive "
     "reference 7XN9 carries an AGONIST (L-054,522), one of the agonist-bound "
     "inactive structures F-11 warns about"),
    ("CCKAR", "full_agonist", "IA1", "7XOV",
     "OFF-REFERENCE and the only small-molecule agonist candidate on the panel's "
     "receptor. 7MBX's ligand is typed protein by GPCRdb (the CCK-8 peptide), so "
     "no on-reference small molecule exists. Needs the most scrutiny of the seven"),
]

# Not enacted, and why.  Carried in the output so the absence is legible.
BLOCKED = [
    ("PD2R2", "full_agonist",
     "LIGAND IDENTITY CONFLICT. The GPCRdb snapshot's record for 9IYB reads "
     "{name: PGD2, type: lipid, function: Agonist, PDB: A1D5Q} -- but CCD A1D5Q "
     "is C43 H81 O13 P, a phosphatidylinositol, while PGD2 (prostaglandin D2) is "
     "C20 H32 O5. The name and the CCD are different molecules, there is no "
     "SMILES in the snapshot to arbitrate, and enacting it would have supplied a "
     "membrane lipid as the agonist. PD2R2 stays TIER-ELIGIBLE and UNCURATED "
     "until the agonist's identity is resolved from the deposition itself. This "
     "is the failure class that gave the frozen campaign a measured 40-46% "
     "curation error rate on name-sourced ligands.\n"
     "UPDATE 2026-09-12, from paper_af3: the two ligand_set files would NOT have "
     "arbitrated this -- PD2R2 is in NEITHER (40 and 64 ligands respectively); "
     "they never curated a PD2R2 ligand at all. Their PD2R2 references are 8XXV "
     "(Ga-coupled-active) and 7M8W (inactive-antagonist), which are OUR panel's "
     "references too, and are conflict-free on their side. 9IYB is off-reference "
     "for both of us. So the real shape of the problem is narrower than it "
     "looked: the panel's own active reference 8XXV carries no orthosteric "
     "agonist record in the GPCRdb snapshot, and the only agonist record that "
     "exists is the conflicted off-reference one. Resolving PD2R2 means getting "
     "an agonist identity for 8XXV, not getting a file."),
]


def main():
    with open(os.path.join(INPUTS, "ligand_curation_candidates.tsv")) as fh:
        cands = list(csv.DictReader(fh, delimiter="\t"))
    # ligand_curation_candidates.tsv only ever covered a hard-coded 7-receptor
    # worklist. The census covers all 64, so picks outside that worklist validate
    # against it instead -- with the SAME identity test, (receptor, ccd, pdb).
    with open(os.path.join(INPUTS, "ligand_census_records.tsv")) as fh:
        census = [dict(r, receptor=r["receptor"], ligand_ccd=r["ligand_ccd"],
                       bound_pdb=r["pdb"], state=r["structure_state"],
                       role_gpcrdb=("agonist" if r["role"] in ("agonist", "partial_agonist")
                                    else "antagonist" if r["role"] in ("antagonist", "inverse_agonist")
                                    else r["role"]),
                       function_raw=r["function_raw"], species=r["structure_species"],
                       resolution=r["resolution"], is_our_reference="")
                  for r in csv.DictReader(fh, delimiter="\t")]
    with open(os.path.join(INPUTS, "g1_receptors.tsv")) as fh:
        organism = {r["slug"]: r["organism"] for r in csv.DictReader(fh, delimiter="\t")}

    try:
        from rdkit import Chem
        from rdkit import RDLogger
        RDLogger.DisableLog("rdApp.*")
    except ImportError:
        Chem = None
        print("NOTE: rdkit unavailable -- inchikey and canonical_smiles left blank")

    with open(os.path.join(INPUTS, "g1_receptors.tsv")) as fh:
        refs = {r["slug"]: {r["active_pdb"].upper(), r["inactive_pdb"].upper()}
                for r in csv.DictReader(fh, delimiter="\t")}

    rows, problems = [], []
    for rec, role, ccd, pdb, why in PICKS:
        pool = cands if any(c["receptor"] == rec for c in cands) else census
        hits = [c for c in pool if c["receptor"] == rec
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
                "neutral_antagonist": ("antagonist",),
                # C-1 RELAXED 2026-09-12 (Aditya). An inverse agonist is now an
                # admissible off-state ligand. It is recorded as its own role,
                # never relabelled "neutral_antagonist" -- they are different
                # pharmacology and the distinction has to survive into analysis.
                "inverse_agonist": ("inverse agonist",)}[role]
        if fn not in want:
            problems.append(
                f"{rec}/{ccd}@{pdb}: assigned {role} but GPCRdb function_raw is "
                f"'{c['function_raw']}' -- these must agree")
            continue
        smiles = c.get("smiles", "")
        is_chain = c.get("is_chain_coinput", "0") == "1"
        canon = inchikey = ""
        if Chem and smiles and not is_chain:
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
            "is_our_reference": ("yes" if pdb.upper() in refs.get(rec, set())
                                 else "no"),
            "ligand_species_context": c["species"],
            "gpcrdb_role": c["role_gpcrdb"],
            "gpcrdb_function_raw": c["function_raw"],
            "is_peptide": "1" if is_chain else "0",
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

    # A receptor whose two roles share a CCD is the F-11 trap: anything keying on
    # the CCD resolves both arms to one molecule. Flag it so nothing downstream
    # has to notice on its own.
    byrec = {}
    for r in rows:
        byrec.setdefault(r["receptor_slug"], []).append(r)
    for rec, rs in byrec.items():
        ccds = [x["ligand_ccd"] for x in rs if x["ligand_ccd"]]
        for x in rs:
            dup = x["ligand_ccd"] and ccds.count(x["ligand_ccd"]) > 1
            x["shares_ccd_with_other_role"] = "1" if dup else "0"
            x["must_key_by"] = "inchikey" if dup else "ccd"

    # Second pass: the CCD verification table is the authority on keying. A pick
    # whose CCD resolves to a DIFFERENT ISOMER than the one we mean must be keyed
    # by InChIKey even when its two roles do not share a CCD within the receptor.
    # RCSB's canonical "RET" is ALL-TRANS retinal -- the agonist form -- so both
    # our 11-cis inverse-agonist picks would silently become agonists in any
    # CCD-keyed pipeline. B1B1U5 needs this and the within-receptor test misses it.
    vpath = os.path.join(INPUTS, "ligand_ccd_verification.tsv")
    if os.path.exists(vpath):
        with open(vpath) as fh:
            stereo = {(v["receptor_slug"], v["ligand_role"])
                      for v in csv.DictReader(fh, delimiter="\t")
                      if v["verdict"] == "STEREO_DIFFERS"}
        for r in rows:
            if (r["receptor_slug"], r["ligand_role"]) in stereo:
                r["must_key_by"] = "inchikey"
                r["ccd_resolves_to_other_isomer"] = "1"
        for r in rows:
            r.setdefault("ccd_resolves_to_other_isomer", "0")

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
