#!/usr/bin/env python3
"""g1_minig.py — what a deposited mini-G construct actually is, block by block.

The lit session's answer to "is there a standard partner truncation between 50 and
350 residues" is: nothing in the prediction literature, three independent recorded
absences, and one convention in structural biology -- the engineered mini-G
GTPase-domain construct, deposited in **6FUF** (rhodopsin-mini-Go), **5G53**
(NECA-A2AR-mini-Gs) and **8F76** (OR51E2-miniGs399).  Its recommendation is to take
the mid-gap rung from a deposited complex rather than from a round number.

Before that can be done, one thing has to be measured rather than assumed: **a
mini-G is not a truncation.**  This script fetches the three deposited Galpha
entities, aligns each to its canonical UniProt parent, and prints the block
structure -- which canonical residues are present, what is deleted, and how many
positions are engineered substitutions.  If the answer is "a deletion plus point
mutations", then a mini-G rung is not a rung on a length ladder at all, and saying
so is the useful output.

The naming trap, recorded so the spec cannot fall into it:
`georgiou2025heterogeneity` (printed pp.3700-3701) uses "mini-Gs" for BOTH the
~200-260-residue engineered construct AND "a mini-Galphas consisting of a
21-residue polypeptide from the Galphas carboxy terminus", two sentences apart.
**A rung named "mini-G" is ambiguous by a factor of ten.**  Every rung in
GROUP1_SYSTEMS.md is named by its length rule and carries a sha256; no construct
name is ever allowed to stand in for a length.

Usage:  python3 redo/build/g1_minig.py
"""
import csv
import difflib
import hashlib
import json
import os
import sys
import time
import urllib.request

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
CACHE = os.path.join(CACHE, "g1_fetch_cache.json")
OUT = os.path.join(INPUTS, "g1_minig.tsv")

# pdb, entity id, canonical family in seq_rungs.tsv, what the depositor calls it
CASES = [
    ("6FUF", "2", "Go", "mini-Go, rhodopsin complex"),
    ("5G53", "2", "Gs", "mini-Gs, NECA-A2AR complex"),
    ("8F76", "3", "Gs", "miniGs399, OR51E2-propionate complex"),
]
ENTITY = "https://data.rcsb.org/rest/v1/core/polymer_entity/%s/%s"


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def get(url):
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    if url in cache:
        return cache[url]
    for attempt in range(4):
        try:
            cache[url] = json.loads(urllib.request.urlopen(url, timeout=60).read())
            json.dump(cache, open(CACHE, "w"))
            return cache[url]
        except Exception as exc:  # noqa: BLE001
            if attempt == 3:
                raise RuntimeError(f"{url}: {exc}")
            time.sleep(2 * (attempt + 1))


def parents():
    out = {}
    with open(os.path.join(INPUTS, "seq_rungs.tsv")) as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        for r in rd:
            if r["rung"] == "R7_full":
                out[r["family"]] = (r["accession"], r["sequence"])
    return out


def main():
    par = parents()
    rows = []
    for pdb, ent, fam, label in CASES:
        d = get(ENTITY % (pdb, ent))
        dep = d["entity_poly"]["pdbx_seq_one_letter_code_can"].replace("\n", "")
        acc, can = par[fam]
        sm = difflib.SequenceMatcher(None, can, dep, autojunk=False)
        blocks = [b for b in sm.get_matching_blocks() if b.size >= 8]
        covered = sorted(set(i for b in blocks for i in range(b.a + 1, b.a + b.size + 1)))
        # contiguous canonical ranges actually present
        ranges, start, prev = [], None, None
        for i in covered:
            if start is None:
                start = prev = i
            elif i == prev + 1:
                prev = i
            else:
                ranges.append((start, prev))
                start = prev = i
        if start is not None:
            ranges.append((start, prev))
        ident = sum(b.size for b in blocks)
        rows.append(dict(
            pdb=pdb, entity=ent, label=label, family=fam, accession=acc,
            dep_len=len(dep), canonical_len=len(can),
            canonical_blocks="; ".join(f"{a}-{b}" for a, b in ranges),
            n_residues_matched=ident,
            n_dep_not_matched=len(dep) - ident,
            is_pure_c_terminal_truncation="yes" if len(ranges) == 1 and
            ranges[0][1] == len(can) and ident == len(dep) else "NO",
            c_term_reached="yes" if ranges and ranges[-1][1] == len(can) else "no",
            dep_sha256=sha(dep), dep_sequence=dep))
        sys.stderr.write(
            f"\n== {pdb} entity {ent} -- {label}\n"
            f"   deposited {len(dep)} aa vs canonical {fam}/{acc} {len(can)} aa\n"
            f"   canonical residue blocks present: "
            f"{'; '.join(f'{a}-{b}' for a, b in ranges)}\n"
            f"   matched {ident} residues; {len(dep)-ident} deposited residues do not "
            f"match the canonical (engineered substitutions, linkers or tags)\n"
            f"   pure C-terminal truncation? {rows[-1]['is_pure_c_terminal_truncation']}\n")

    cols = ["pdb", "entity", "label", "family", "accession", "dep_len",
            "canonical_len", "canonical_blocks", "n_residues_matched",
            "n_dep_not_matched", "is_pure_c_terminal_truncation", "c_term_reached",
            "dep_sha256", "dep_sequence"]
    with open(OUT, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[c]) for c in cols) + "\n")
    sys.stderr.write(f"\n# wrote {OUT}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
