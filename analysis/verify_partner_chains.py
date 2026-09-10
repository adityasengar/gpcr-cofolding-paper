#!/usr/bin/env python3
"""Check the partner (non-receptor) chains of our own reference set against UniProt.

WHY THIS EXISTS. Nothing else in this project reads the sequence of a
non-receptor chain. The construct audit behind Block A caveat C-11 compares the
drop's `construct` column against RCSB `pdbx_mutation` **on the receptor
entity**, so a substitution in the Ga partner is outside its scope by
construction. D-B-9 found the consequence: OPSD/4X1H is annotated
`active_stabilization_source = native` with the note "native alpha5-CT donor
class Gt", and the deposited peptide is an engineered 11-mer.

WHY IT DOES NOT USE pdbx_mutation. That field is the obvious shortcut and it is
not reliable. Of the seven references below that carry the canonical
dominant-negative Gai1 substitutions in their DEPOSITED SEQUENCE, RCSB's
`pdbx_mutation` records them on **two**. It is null on the other five. A check
built on that field would have passed all five. So this script diffs the
deposited one-letter sequence against the canonical UniProt sequence and treats
a missing cross-reference as a FLAG, never as a pass.

WHY IT DOES NOT SLIDE A WINDOW. The lit session's first version compared
fixed-length windows rather than aligning, which reports dozens to hundreds of
false substitutions on any chimera or fusion. This script refuses to report
substitutions when the lengths differ, and says UNRESOLVED instead. An honest
"not checked" is worth more than a wrong count.

THE QUESTION THAT DECIDES SEVERITY is not "is the partner engineered" but "is
the ALPHA5-CT engineered", because the alpha5-CT is what the paper's title is
about. Gai1 is 354 residues, so the alpha5 C-terminal 21-mer is 334-354. All
four dominant-negative positions (47, 203, 245, 326) fall outside it. The script
reports the two separately and never collapses them.

Usage:  python3 analysis/verify_partner_chains.py [--all]
        (default checks the 25 references annotated `native`; --all does 80)
"""
import csv
import json
import sys
import time
import urllib.request

REF_AUDIT = "data/block_b/09_references/reference_audit.csv"
ALPHA5_CT_LEN = 21          # the length the paper's title claims
RCSB_ENTRY = "https://data.rcsb.org/rest/v1/core/entry/%s"
RCSB_ENTITY = "https://data.rcsb.org/rest/v1/core/polymer_entity/%s/%s"
UNIPROT = "https://rest.uniprot.org/uniprotkb/%s.fasta"

_cache = {}


def _get(url, parse=json.loads):
    if url in _cache:
        return _cache[url]
    for attempt in range(3):
        try:
            body = urllib.request.urlopen(url, timeout=30).read().decode()
            _cache[url] = parse(body)
            return _cache[url]
        except Exception as exc:                       # noqa: BLE001
            if attempt == 2:
                return {"_err": str(exc)}
            time.sleep(1.5 * (attempt + 1))


def canonical(accession):
    fasta = _get(UNIPROT % accession, parse=lambda b: b)
    if isinstance(fasta, dict):
        return None
    return "".join(l for l in fasta.split("\n") if not l.startswith(">"))


def partner_entities(pdb_id):
    """Every polymer entity that is not the receptor, with its UniProt accession."""
    entry = _get(RCSB_ENTRY % pdb_id)
    if "_err" in entry:
        return [], entry["_err"]
    ids = entry.get("rcsb_entry_container_identifiers", {}).get("polymer_entity_ids", [])
    out = []
    for eid in ids:
        ent = _get(RCSB_ENTITY % (pdb_id, eid))
        if "_err" in ent:
            continue
        meta = ent.get("rcsb_polymer_entity", {}) or {}
        desc = meta.get("pdbx_description") or ""
        seq = (ent.get("entity_poly", {}) or {}).get("pdbx_seq_one_letter_code_can", "")
        seq = seq.replace("\n", "").strip()
        acc = None
        for ref in ent.get("rcsb_polymer_entity_container_identifiers", {}).get(
                "reference_sequence_identifiers", []) or []:
            if ref.get("database_name") == "UniProt":
                acc = ref.get("database_accession")
                break
        out.append({
            "entity_id": eid,
            "description": desc,
            "sequence": seq,
            "uniprot": acc,
            "pdbx_mutation": meta.get("pdbx_mutation"),
        })
    return out, None


def is_partner(desc):
    """Only the G-alpha chain. NOT beta, NOT gamma.

    This is narrower than it first looks and the narrowing is the point. The
    alpha5-CT is a feature of the ALPHA subunit; asking whether a substitution
    falls "inside the alpha5-CT" of a G-gamma chain is a category error. An
    earlier version of this function matched any "guanine nucleotide-binding"
    description, so it pulled in G-beta and G-gamma, and then reported the
    standard G-gamma2 C68S non-prenylation mutation as an alpha5-CT hit in two
    references, because position 68 of a 71-residue chain is inside ITS last 21.
    Three false alpha5-CT findings, from one loose string match.
    """
    d = desc.lower()
    if "subunit beta" in d or "subunit gamma" in d:
        return False
    if "g(i)/g(s)/g(t)" in d or "g(i)/g(s)/g(o)" in d:
        return False                      # these descriptions ARE beta / gamma
    if "subunit alpha" in d:
        return True
    # the derived-peptide case that started all this
    return "peptide" in d and ("subunit alpha" in d or "g(" in d)


def compare(deposited, canon):
    """Substitutions, but ONLY when the lengths match. Never a sliding window."""
    if canon is None:
        return None, "no-canonical-sequence"
    if len(deposited) != len(canon):
        return None, "LENGTH-DIFFERS (fusion, chimera, fragment or truncation)"
    subs = [f"{canon[i]}{i + 1}{deposited[i]}"
            for i in range(len(canon)) if canon[i] != deposited[i]]
    return subs, None


def main():
    every = "--all" in sys.argv
    rows = list(csv.DictReader(open(REF_AUDIT)))
    targets = [r for r in rows
               if every or r["active_stabilization_source"] == "native"]
    print(f"checking {len(targets)} references "
          f"({'all roles' if every else 'annotated `native` only'})\n")

    checked = engineered = alpha5_hit = unresolved = 0
    findings = []

    for r in targets:
        pdb, receptor = r["pdb_id"].upper(), r["receptor"]
        entities, err = partner_entities(pdb)
        if err:
            print(f"  {pdb} {receptor:8} FETCH FAILED: {err}")
            continue
        for ent in entities:
            if not is_partner(ent["description"]):
                continue
            acc = ent["uniprot"]
            if not acc:
                # 4X1H's peptide has NO UniProt cross-reference. A missing
                # reference is a FLAG, never a pass.
                unresolved += 1
                findings.append((pdb, receptor, "NO-UNIPROT-XREF",
                                 ent["description"][:46], "", ""))
                continue
            subs, why = compare(ent["sequence"], canonical(acc))
            if subs is None:
                unresolved += 1
                findings.append((pdb, receptor, "UNRESOLVED", why, "", ""))
                continue
            checked += 1
            if not subs:
                continue
            engineered += 1
            n = len(ent["sequence"])
            in_ct = [s for s in subs if int(s[1:-1]) > n - ALPHA5_CT_LEN]
            if in_ct:
                alpha5_hit += 1
            findings.append((pdb, receptor, "ENGINEERED",
                             ";".join(subs[:6]),
                             "IN ALPHA5-CT: " + ";".join(in_ct) if in_ct
                             else "all outside the alpha5-CT",
                             f"pdbx_mutation={ent['pdbx_mutation']}"))

    print(f"{'pdb':6} {'receptor':9} {'verdict':16} {'substitutions':34} where / metadata")
    print("-" * 118)
    for f in findings:
        print(f"{f[0]:6} {f[1]:9} {f[2]:16} {f[3]:34} {f[4]}  {f[5]}")

    print(f"\n  partner chains compared cleanly : {checked}")
    print(f"  carrying substitutions          : {engineered}")
    print(f"  with a substitution IN the alpha5-CT : {alpha5_hit}")
    print(f"  unresolved (flagged, NOT passed) : {unresolved}")
    print("\nA substitution outside the alpha5-CT does not touch what the title "
          "claims.\nA substitution inside it does.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
