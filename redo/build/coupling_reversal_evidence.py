#!/usr/bin/env python3
"""Enumerate the Ga partner in EVERY active structure of a reversal receptor.

The question this settles: four receptors -- B1B1U5, CCKAR, EDNRB, GHSR -- have a
Rule-R structural cognate that REVERSES Block B's prior.  B1B1U5 closed as D-H.
For the other three the objection was that Block B's prior (Gq in all three) is
what most annotation authorities report, so picking the structural family looked
like preferring one source over four.

It is not, and this script is the evidence.  For every ACTIVE structure of each
receptor it records the Ga entity's UniProt accession, its length, and its own
deposited description -- and the descriptions say plainly which are chimeras,
mini-G constructs and engineered subunits.  The competing families turn out to
exist ONLY as engineered constructs.

Source: RCSB Data REST API, read-only, the same source the coupling generators
already use.  Responses are cached so a re-run is offline and reproducible.

    python3 redo/build/coupling_reversal_evidence.py
    python3 redo/build/coupling_reversal_evidence.py --refresh   # re-fetch

Writes: inputs/coupling_reversal_evidence.tsv
Then:   python3 redo/build/manifest.py
"""

import csv
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, CACHE  # noqa: E402

CACHE_FILE = os.path.join(CACHE, "coupling_reversal_rcsb.json")
OUT = os.path.join(INPUTS, "coupling_reversal_evidence.tsv")

# The receptors whose Rule-R cognate reverses Block B's prior, and every ACTIVE
# structure GPCRdb holds for them (from inputs/g0_calibration_structures.csv).
# B1B1U5 is absent: it is not Class A and its reversal closed as D-H.
ACTIVES = {
    "CCKAR": ["7MBX", "7MBY", "9BKK", "9BKJ", "7EZM", "7XOV", "7EZK", "7EZH", "7XOU"],
    "EDNRB": ["8IY5", "8HBD", "8XVE", "8XGR", "8XWP", "8XVH", "8HCX", "8XWQ"],
    "GHSR": ["7NA7", "7NA8", "7W2Z", "7F9Y", "7F9Z"],
}

# The Rule-R pick per receptor, so the output says which row is the chosen one.
RULE_R = {"CCKAR": "7MBX", "EDNRB": "8IY5", "GHSR": "7NA7"}

# Canonical human Ga accessions -> family.  Only what appears in these entries.
GA_FAMILY = {
    "P63092": "Gs", "Q5JWF2": "Gs(XLas)", "P38405": "Golf",
    "P63096": "Gi1", "P04899": "Gi2", "P08754": "Gi3",
    "P09471": "GoA", "P19087": "GoB", "P63097": "Gi1", "P10824": "Gi1",
    "P50148": "Gq", "P29992": "G11", "P04896": "Gq",
    "Q03113": "G12", "Q14344": "G13",
    "P11488": "Gt1", "P19086": "Gt2", "P04695": "Gt1",
}

# Words a deposition uses when the chain is NOT a native subunit.  Matched
# case-insensitively against the entity description AND the entry title -- 9BKK's
# entity description says only "G(s) subunit alpha isoforms XLas" while its TITLE
# says "Gq chimera (mGsqi) complex".  Description alone classed it native, which
# was wrong; the first version of this script made exactly that mistake.
ENGINEERED = ("chimera", "fusion", "engineered", "mutated to match",
              "mini-g", "minig", "mgs", "dngi", "dominant negative",
              "dominant-negative")

# A native full-length Ga is ~350-395 residues.  Deposited mini-G constructs run
# 230-270.  Length is the discriminator the keyword test misses entirely: the
# 246 aa "G(q) subunit alpha-1" in 8HCX and the 261 aa "Isoform Gnas-2" in
# 8XVE/8XVH carry no engineering word anywhere and are still not native subunits.
# Canonical lengths come from inputs/seq_constructs.tsv, never hard-coded here.
MIN_NATIVE_FRACTION = 0.85


def canonical_lengths():
    """family -> canonical full length, from the frozen sequence table."""
    out = {}
    with open(os.path.join(INPUTS, "seq_constructs.tsv")) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            out[r["family"]] = int(r["full_len"])
    # the accessions seen in these entries, mapped onto those families
    out["GoA"] = out["GoB"] = out.get("Go", 354)
    out["Gs(XLas)"] = out["Gs"]          # XLas shares the Gs C terminus
    out["Gt1"] = out.get("Gt1", 350)
    return out


CANON = {}


def _fetch(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def load(refresh=False):
    cache = {}
    if os.path.exists(CACHE_FILE) and not refresh:
        cache = json.load(open(CACHE_FILE))
    want = [p for pdbs in ACTIVES.values() for p in pdbs]
    missing = [p for p in want if p not in cache]
    for p in missing:
        entry = _fetch(f"https://data.rcsb.org/rest/v1/core/entry/{p}")
        ids = entry.get("rcsb_entry_container_identifiers", {}).get(
            "polymer_entity_ids", [])
        ents = []
        for i in ids:
            pe = _fetch(f"https://data.rcsb.org/rest/v1/core/polymer_entity/{p}/{i}")
            accs = [a.get("database_accession") for a
                    in (pe.get("rcsb_polymer_entity_container_identifiers", {})
                        .get("reference_sequence_identifiers") or [])
                    if a.get("database_accession")]
            ents.append({
                "id": i,
                "desc": pe.get("rcsb_polymer_entity", {}).get("pdbx_description", ""),
                "acc": accs,
                "len": pe.get("entity_poly", {}).get("rcsb_sample_sequence_length"),
            })
        cache[p] = {"title": entry.get("struct", {}).get("title", ""),
                    "entities": ents}
        time.sleep(0.15)
    if missing:
        os.makedirs(CACHE, exist_ok=True)
        json.dump(cache, open(CACHE_FILE, "w"), indent=1, sort_keys=True)
    return cache


def is_galpha(desc):
    d = desc.lower()
    return ("subunit alpha" in d or "g-alpha" in d or "g alpha" in d) and "beta" not in d


def main(argv):
    global CANON
    CANON = canonical_lengths()
    cache = load("--refresh" in argv)
    rows = []
    for rec, pdbs in ACTIVES.items():
        for p in pdbs:
            v = cache[p]
            gas = [e for e in v["entities"] if is_galpha(e["desc"])]
            if not gas:
                rows.append({
                    "receptor_slug": rec, "pdb": p,
                    "is_rule_r": "yes" if RULE_R[rec] == p else "no",
                    "ga_entity": "", "ga_accessions": "", "ga_family": "NONE_RESOLVED",
                    "ga_len": "", "canonical_len": "",
                    "construct_class": "no_galpha_entity_matched",
                    "ga_description": "", "entry_title": v["title"]})
                continue
            for e in gas:
                fams = sorted({GA_FAMILY.get(a, a) for a in e["acc"]})
                hay = (e["desc"] + " " + v["title"]).lower()
                eng = [w for w in ENGINEERED if w in hay]
                multi = len(fams) > 1
                canon = max((CANON.get(f, 0) for f in fams), default=0)
                short = (canon and e["len"] and e["len"] < MIN_NATIVE_FRACTION * canon)
                if eng or multi:
                    cls = "engineered"
                elif e["len"] and e["len"] < MIN_NATIVE_FRACTION * min(CANON.values()):
                    # Below the SHORTEST canonical Ga in the table, so it is
                    # truncated whichever family it turns out to be.  This branch
                    # catches 8HCX's 246 aa "G(q) subunit alpha-1", which carries
                    # no accession and so has no family-specific length to test.
                    cls = "truncated_or_mini"
                elif not e["acc"]:
                    # No reference accession at all: we cannot verify it is a
                    # native subunit, so it does not get to count as one.
                    cls = "unverifiable"
                elif short:
                    cls = "truncated_or_mini"
                else:
                    cls = "native"
                rows.append({
                    "receptor_slug": rec, "pdb": p,
                    "is_rule_r": "yes" if RULE_R[rec] == p else "no",
                    "ga_entity": f"{p}_{e['id']}",
                    "ga_accessions": ";".join(e["acc"]) or "NONE",
                    "ga_family": ";".join(fams) if fams else "UNASSIGNED",
                    "ga_len": e["len"],
                    "canonical_len": canon or "",
                    "construct_class": cls,
                    "ga_description": e["desc"],
                    "entry_title": v["title"]})

    cols = ["receptor_slug", "pdb", "is_rule_r", "ga_entity", "ga_accessions",
            "ga_family", "ga_len", "canonical_len", "construct_class",
            "ga_description", "entry_title"]
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {os.path.relpath(OUT)}  ({len(rows)} rows)")
    print()
    for rec in ACTIVES:
        sub = [r for r in rows if r["receptor_slug"] == rec]
        nat = [r for r in sub if r["construct_class"] == "native"]
        fams = sorted({r["ga_family"] for r in nat})
        print(f"  {rec:<7} {len(sub)} Ga entities across {len(ACTIVES[rec])} actives; "
              f"{len(nat)} NATIVE, families present natively: {fams or ['none']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
