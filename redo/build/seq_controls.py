#!/usr/bin/env python3
"""Peptide-rung control constructs: exact construction rules, sequences, hashes.

Every control is derived from a fetched sequence. Nothing is typed from memory.

Seed rule (deterministic, reproducible, and stated so a reader can regenerate):
    seed = int(sha256(f"{family}|{rung}|{control}|redo_v1|{k}").hexdigest()[:16], 16)
    rng  = random.Random(seed)
This is the Block B convention (`SHA-256(slug + '|block_b_decoy_v1|' + variant)`)
with the per-receptor term replaced by the per-family term, because at peptide
length the construct no longer depends on the receptor.

Usage: python3 redo/build/seq_controls.py > redo/inputs/seq_controls.tsv
"""
import os
import hashlib
import json
import random
import sys
import urllib.request

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo

UNIPROT = "https://rest.uniprot.org/uniprotkb/%s.json"

# The five families the current 40-receptor panel actually needs, plus Golf
# because it is one substitution from Gs at every rung.
PARENTS = [("Gs", "P63092"), ("Gi1", "P63096"), ("Gq", "P50148"),
           ("G13", "Q14344"), ("Gt1", "P11488")]
RUNGS = {"ct11": 11, "ct15": 15, "ct21": 21, "a5helix": 26}

# Hydrophobic set used by the face-preserving scramble. Kyte-Doolittle positive
# plus the aromatics, stated explicitly so the partition is auditable.
HYDROPHOBIC = set("AVLIMFWYC")

GCN4_ACC = "P03069"          # GCN4_YEAST; leucine-zipper 249-281 (33 aa) is the
GCN4_START = 249             # entry the pipeline already carries, hash-verified


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def rng_for(*parts):
    return random.Random(int(sha("|".join(map(str, parts)))[:16], 16))


def fetch(acc):
    d = json.loads(urllib.request.urlopen(UNIPROT % acc, timeout=45).read().decode())
    return d["sequence"]["value"]


def scramble(seq, rng, floor=None):
    floor = floor if floor is not None else max(5, len(seq) // 2)
    for _ in range(256):
        cand = list(seq)
        rng.shuffle(cand)
        cand = "".join(cand)
        if sum(a != b for a, b in zip(cand, seq)) >= floor:
            return cand
    raise RuntimeError("no draw cleared the Hamming floor")


def face_scramble(seq, rng, floor=None):
    """Permute WITHIN the hydrophobic set and WITHIN the polar set.

    Length, composition, net charge and the hydrophobic/polar pattern along the
    chain -- and therefore the amphipathic face and the hydrophobic moment of an
    ideal helix -- are all preserved. Only residue identity moves.
    """
    floor = floor if floor is not None else max(3, len(seq) // 3)
    hidx = [i for i, c in enumerate(seq) if c in HYDROPHOBIC]
    pidx = [i for i, c in enumerate(seq) if c not in HYDROPHOBIC]
    for _ in range(256):
        out = list(seq)
        hv = [seq[i] for i in hidx]
        pv = [seq[i] for i in pidx]
        rng.shuffle(hv)
        rng.shuffle(pv)
        for i, v in zip(hidx, hv):
            out[i] = v
        for i, v in zip(pidx, pv):
            out[i] = v
        out = "".join(out)
        if sum(a != b for a, b in zip(out, seq)) >= floor:
            return out
    raise RuntimeError("no face-preserving draw cleared the Hamming floor")


def main():
    gcn4_full = fetch(GCN4_ACC)
    print("\t".join(["rung", "family", "control", "k", "len", "sequence",
                     "sha256", "hamming_to_wt", "preserves", "destroys",
                     "provenance"]))
    for fam, acc in PARENTS:
        parent = fetch(acc)
        for rname, n in RUNGS.items():
            wt = parent[-n:]
            emit = [("wt", "", wt, "-", "-",
                     f"UniProt {acc} last {n}")]
            emit.append(("reversed", "", wt[::-1],
                         "length, composition, net charge, aa content",
                         "order and register (N->C direction)",
                         f"reverse of UniProt {acc} last {n}"))
            emit.append(("polyA", "", "A" * n,
                         "length only",
                         "composition, charge, identity; RAISES helical propensity",
                         "constructed"))
            for k in range(1, 6):
                emit.append((f"scramble", str(k),
                             scramble(wt, rng_for(fam, rname, "scramble", "redo_v1", k)),
                             "length, composition, net charge",
                             "order, register, hydrophobic face",
                             f"seeded permutation of UniProt {acc} last {n}"))
            for k in range(1, 4):
                emit.append((f"face_scramble", str(k),
                             face_scramble(wt, rng_for(fam, rname, "face", "redo_v1", k)),
                             "length, composition, net charge, hydrophobic/polar "
                             "pattern (amphipathic face, helical moment)",
                             "residue identity only",
                             f"class-restricted permutation of UniProt {acc} last {n}"))
            # helicity-matched, sequence-unrelated: a window of the GCN4 zipper
            emit.append(("gcn4_window", "",
                         gcn4_full[GCN4_START - 1:GCN4_START - 1 + n],
                         "length; strong helical propensity; no evolutionary "
                         "relationship to Ga",
                         "composition, charge, identity",
                         f"UniProt {GCN4_ACC} residues {GCN4_START}-{GCN4_START + n - 1}"))
            for cname, k, s, keeps, kills, prov in emit:
                ham = "-" if cname == "wt" else (
                    sum(a != b for a, b in zip(s, wt)) if len(s) == len(wt) else "NA")
                print("\t".join(map(str, [rname, fam, cname, k, len(s), s,
                                          sha(s), ham, keeps, kills, prov])))
    print("# gcn4_leucine_zipper_33 (the entry already in partners.fasta) = "
          f"{GCN4_ACC} {GCN4_START}-{GCN4_START+32} "
          f"sha256={sha(gcn4_full[GCN4_START-1:GCN4_START+32])}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
