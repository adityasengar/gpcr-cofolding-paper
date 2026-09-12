#!/usr/bin/env python3
"""The alpha5-null full-subunit controls (R6a / R6b / R6c), with their hashes.

WHY THIS FILE EXISTS. `seq_a5null.tsv` was originally produced by an inline
heredoc rather than a script on disk, so the seed convention was not
reproducible from the artefact alone. That is the defect this file closes. The
convention is recovered verbatim below and is PROVED against every row already
in `seq_a5null.tsv` before anything new is emitted (`--verify`, run by default).

THE SEED KEY, and why it is easy to guess wrong. The peptide-rung controls in
`seq_controls.py` key on

    (family, rung, control, "redo_v1", k)

because at peptide length a construct is one rung of one family. The alpha5-null
constructs are NOT rungs -- there is exactly one per family -- so the rung term
is absent and the control term is split in two:

    (family, "a5null", "permute", "redo_v1", 1)

Any key that carries a rung name, or that spells the control "a5perm" or
"scramble", produces different bytes. That is the difference that cost the
Group 1 agent eight attempts.

THE THREE CONSTRUCTS.
  R6a_da5      full subunit with CGN G.H5 deleted      -> removes the contact,
                                                          keeps the object
  R6b_a5perm   G.H5 replaced by a seeded permutation   -> removes identity,
               of itself                                  keeps bulk, length,
                                                          composition and
                                                          helical propensity
  R6c_a5polyA  G.H5 replaced by poly-Ala               -> removes composition too

G.H5 is the C-terminal 26 residues in every one of the 16 human Ga subunits
(verified in `seq_rungs.py` against GproteinDb CGN), so the slice is written as
`seq[-26:]` and the CGN invariant is re-asserted here rather than re-fetched.

Usage:
    python3 redo/build/seq_a5null.py               # verify, then print the table
    python3 redo/build/seq_a5null.py --verify-only # just prove the reproduction
    python3 redo/build/seq_a5null.py > redo/inputs/seq_a5null.tsv
"""
import csv
import hashlib
import json
import os
import random
import sys
import time
import urllib.request

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo

UNIPROT = "https://rest.uniprot.org/uniprotkb/%s.json"
TSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seq_a5null.tsv")

ALPHA5_LEN = 26          # CGN G.H5, invariant across all 16 human Ga subunits
HAMMING_FLOOR = 18       # on a 26-mer permutation; the original run's floor

# The five families the original run covered, in the original order, followed by
# the two the frozen cognate-Ga rule added: SSR2 -> Gi3, and five receptors -> Go.
# Order matters only for the output; the seed does not depend on it.
FAMILIES = [
    ("Gs",   "P63092"),
    ("Gi1",  "P63096"),
    ("Gq",   "P50148"),
    ("G13",  "Q14344"),
    ("Gt1",  "P11488"),
    ("Gi3",  "P08754"),      # added: SSR2 cognate under the frozen rule
    ("Go",   "P09471"),      # added: five receptors cognate under the frozen rule
]
ORIGINAL = {"Gs", "Gi1", "Gq", "G13", "Gt1"}

HEADER = ["construct", "family", "accession", "len", "rule",
          "alpha5_26_supplied", "sha256"]

_cache = {}


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def rng_for(*parts):
    """The original heredoc's generator, byte-for-byte.

    int(sha256("|".join(parts))[:16], 16) -> random.Random seed.
    Note `map(str, parts)`: the trailing 1 is an int and is stringified here,
    so the keyed string ends "...|redo_v1|1".
    """
    return random.Random(int(sha("|".join(map(str, parts)))[:16], 16))


def fetch(acc):
    if acc in _cache:
        return _cache[acc]
    for attempt in range(4):
        try:
            body = urllib.request.urlopen(UNIPROT % acc, timeout=45).read().decode()
            _cache[acc] = json.loads(body)["sequence"]["value"]
            return _cache[acc]
        except Exception as exc:                       # noqa: BLE001
            if attempt == 3:
                raise RuntimeError(f"UniProt {acc}: {exc}")
            time.sleep(2 * (attempt + 1))


def permute_alpha5(h5, rng, floor=HAMMING_FLOOR, tries=256):
    """Seeded permutation of the alpha5 helix, Hamming floor against the parent.

    Reproduces the original loop exactly, including the fact that each failed
    draw still consumes rng state, so the accepted draw depends on every draw
    before it.
    """
    cand = None
    for _ in range(tries):
        chars = list(h5)
        rng.shuffle(chars)
        cand = "".join(chars)
        if sum(a != b for a, b in zip(cand, h5)) >= floor:
            return cand
    raise RuntimeError("no draw cleared the Hamming floor")


def build(family, accession):
    """The three constructs for one family, in the original emission order."""
    seq = fetch(accession)
    core, h5 = seq[:-ALPHA5_LEN], seq[-ALPHA5_LEN:]
    assert len(h5) == ALPHA5_LEN
    perm = permute_alpha5(h5, rng_for(family, "a5null", "permute", "redo_v1", 1))
    return [
        ("R6a_da5", family, accession, len(core),
         f"full subunit, CGN G.H5 deleted (1..L-{ALPHA5_LEN})", "(none)", sha(core)),
        ("R6b_a5perm", family, accession, len(core + perm),
         f"full subunit, last {ALPHA5_LEN} replaced by a seeded permutation of itself",
         perm, sha(core + perm)),
        ("R6c_a5polyA", family, accession, len(core + "A" * ALPHA5_LEN),
         f"full subunit, last {ALPHA5_LEN} replaced by poly-Ala",
         "A" * ALPHA5_LEN, sha(core + "A" * ALPHA5_LEN)),
    ]


def verify():
    """Prove the generator reproduces every row already in seq_a5null.tsv.

    Fails loudly on any mismatch. A generator that cannot reproduce the artefact
    it claims to generate is worse than no generator at all.
    """
    if not os.path.exists(TSV):
        print(f"# VERIFY SKIPPED: {TSV} not present", file=sys.stderr)
        return 0
    existing = list(csv.DictReader(open(TSV), delimiter="\t"))
    if not existing:
        print(f"# VERIFY SKIPPED: {TSV} is empty", file=sys.stderr)
        return 0
    fams = []
    for r in existing:
        if r["family"] not in fams:
            fams.append(r["family"])
    rebuilt = {}
    for fam in fams:
        acc = dict(FAMILIES).get(fam)
        if acc is None:
            print(f"# VERIFY FAIL: {fam} is in the TSV but not in FAMILIES",
                  file=sys.stderr)
            return 1
        for row in build(fam, acc):
            rebuilt[(row[0], row[1])] = row
    bad = 0
    for r in existing:
        key = (r["construct"], r["family"])
        got = rebuilt.get(key)
        if got is None:
            print(f"# VERIFY FAIL: {key} not regenerated", file=sys.stderr)
            bad += 1
            continue
        for i, col in enumerate(HEADER):
            if str(got[i]) != r[col]:
                print(f"# VERIFY FAIL: {key} column {col}: "
                      f"existing={r[col]!r} rebuilt={got[i]!r}", file=sys.stderr)
                bad += 1
    n_orig = sum(1 for r in existing if r["family"] in ORIGINAL)
    if bad:
        print(f"# VERIFY: {bad} mismatch(es) against {len(existing)} existing rows.",
              file=sys.stderr)
        return 1
    print(f"# VERIFY OK: all {len(existing)} existing rows reproduced byte-for-byte "
          f"({n_orig} of them from the original five families). Seed key = "
          f"(family, 'a5null', 'permute', 'redo_v1', 1).", file=sys.stderr)
    return 0


def main():
    if "--no-verify" not in sys.argv:
        if verify() != 0:
            print("# ABORTING: refusing to emit a table the generator cannot "
                  "reproduce.", file=sys.stderr)
            return 1
    if "--verify-only" in sys.argv:
        return 0
    print("\t".join(HEADER))
    for fam, acc in FAMILIES:
        for row in build(fam, acc):
            print("\t".join(map(str, row)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
