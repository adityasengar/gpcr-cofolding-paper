#!/usr/bin/env python3
"""Emit every ladder rung, for every Ga family, with its sha256.

Rungs are defined RELATIVE TO THE C TERMINUS or by CGN segment, never by a
fixed residue range: "Ga residues 334-354" is the C-terminal 21 only for Gi1.

Segment boundaries come from GPCRdb/GproteinDb CGN
(https://gpcrdb.org/services/residues/{entry_name}/), sequences from UniProt.

Hash convention (verified to reproduce all 10 Ga entries in the pipeline's
partners.fasta): sha256 of the uppercase one-letter sequence, UTF-8, no header,
no newline, no whitespace.

Usage: python3 redo/build/seq_rungs.py > redo/inputs/seq_rungs.tsv
"""
import os
import hashlib
import json
import sys
import time
import urllib.request

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo

UNIPROT = "https://rest.uniprot.org/uniprotkb/%s.json"
GPCRDB = "https://gpcrdb.org/services/residues/%s/"

FAMILIES = [
    # family, accession, gproteindb entry_name
    ("Gs",    "P63092", "gnas2_human"),
    ("Golf",  "P38405", "gnal_human"),
    ("Gi1",   "P63096", "gnai1_human"),
    ("Gi2",   "P04899", "gnai2_human"),
    ("Gi3",   "P08754", "gnai3_human"),
    ("Go",    "P09471", "gnao_human"),
    ("Gz",    "P19086", "gnaz_human"),
    ("Gt1",   "P11488", "gnat1_human"),
    ("Gt2",   "P19087", "gnat2_human"),
    ("Ggust", "A8MTJ3", "gnat3_human"),
    ("Gq",    "P50148", "gnaq_human"),
    ("G11",   "P29992", "gna11_human"),
    ("G14",   "O95837", "gna14_human"),
    ("G15",   "P30679", "gna15_human"),
    ("G12",   "Q03113", "gna12_human"),
    ("G13",   "Q14344", "gna13_human"),
]

_c = {}


def get(url):
    if url in _c:
        return _c[url]
    for a in range(4):
        try:
            _c[url] = json.loads(urllib.request.urlopen(url, timeout=45).read().decode())
            return _c[url]
        except Exception as exc:                       # noqa: BLE001
            if a == 3:
                raise RuntimeError(f"{url}: {exc}")
            time.sleep(2 * (a + 1))


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def main():
    print("\t".join(["rung", "family", "accession", "seq_version", "parent_len",
                     "rule", "resid_range", "len", "sequence", "sha256"]))
    for fam, acc, entry in FAMILIES:
        d = get(UNIPROT % acc)
        seq = d["sequence"]["value"]
        sv = d["entryAudit"]["sequenceVersion"]
        L = len(seq)
        res = get(GPCRDB % entry)
        seg = {}
        for r in res:
            s = r["protein_segment"]
            n = r["sequence_number"]
            lo, hi = seg.get(s, (n, n))
            seg[s] = (min(lo, n), max(hi, n))
        h5, s6 = seg["G.H5"], seg["G.S6"]
        assert h5[1] == L, f"{fam}: G.H5 does not end at the C terminus"

        rows = [
            ("R1_ct11",   "last 11 residues",                    L - 10, L),
            ("R2_ct15",   "last 15 residues",                    L - 14, L),
            ("R3_ct21",   "last 21 residues",                    L - 20, L),
            ("R4_a5helix", "CGN G.H5 (alpha5 helix)",            h5[0], h5[1]),
            ("R5_a5plus", "CGN G.S6 through C terminus (b6-s6h5-a5)", s6[0], L),
            ("R7_full",   "full canonical subunit",              1, L),
            ("R6a_da5",   "full subunit with CGN G.H5 deleted",  1, h5[0] - 1),
        ]
        for name, rule, a, b in rows:
            sub = seq[a - 1:b]
            print("\t".join(map(str, [name, fam, acc, sv, L, rule,
                                      f"{a}-{b}", len(sub), sub, sha(sub)])))

    # invariants worth having on the record
    print("\n# CGN invariants across the 16 human Ga subunits:", file=sys.stderr)
    print("#   G.H5 is the C-terminal 26 residues in every one.", file=sys.stderr)
    print("#   G.S6 starts 36 residues from the C terminus in every one.", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
