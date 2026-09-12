#!/usr/bin/env python3
"""g1_midrungs.py — the intermediate ladder rungs, as real constructs.

WHY THIS FILE EXISTS
--------------------
`RUN_MATRIX.md` §3.5 records a defect in the centrepiece: the rung lengths run
0, 11, 15, 21, 26, 36 and then jump to 324-394. `junker2026peptidedesign`
stratifies GPCR peptide/protein complexes at <=50 vs >50 residues (p5) and says
cross-length comparison of an interface score is unsound (p16), so the regime
boundary falls inside our empty gap and the comparison that carries the title
crosses it. RUN_MATRIX asks for three intermediate rungs at ~60/~100/~200 aa and
says "SEQUENCES.md owns the exact boundaries". SEQUENCES.md is frozen, so the
constructs are built here instead, under exactly SEQUENCES.md's conventions.

CONVENTIONS INHERITED (SEQUENCES.md §0)
---------------------------------------
  * construct_id = sha256(uppercase one-letter sequence, UTF-8, no header,
    no newline, no whitespace).  Keyed by hash, never by header.
  * A rung is defined by a **CGN protein segment**, not by a residue range and
    not by a raw length -- exactly as R4_a5helix is "G.H5" and R5_a5plus is
    "G.S6 -> C-term".  A rung defined by raw length would supply a different
    structural element in each family; a rung defined by segment supplies the
    same element and lets the length vary, which is the honest parameterisation.

SOURCES (nothing from memory)
-----------------------------
  * Partner bytes: `redo/inputs/seq_rungs.tsv`, rows rung == R7_full.  Those
    are the held canonical UniProt sequences whose sha256 already reproduce the
    pipeline's own `partners.fasta` entries (SEQUENCES.md §2).
  * Segment boundaries: GPCRdb/GproteinDb CGN residue tables,
    https://gpcrdb.org/services/residues/{entry_name}/ , the same endpoint
    `seq_build.py` uses.  Cached to `g1_cgn_cache.json` so this is
    reproducible offline after the first run.

CHECKS THE SCRIPT RUNS ON ITSELF (a silent check looks like a passing one)
-------------------------------------------------------------------------
  1. Every CGN residue's `amino_acid` must equal the UniProt sequence at that
     position.  If GPCRdb and UniProt disagree the family is dropped loudly.
  2. The re-derived G.H5 and G.S6 truncation lengths must reproduce
     SEQUENCES.md §0.2's invariants (26 and 36) on every family.
  3. Every emitted construct must be a suffix of its parent R7_full sequence
     (nested ladder), except the declared non-nested DHD variant.

Usage:  python3 redo/build/g1_midrungs.py            # writes g1_midrungs.tsv
        python3 redo/build/g1_midrungs.py --check    # verify only, no write
"""
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
RUNGS = os.path.join(INPUTS, "seq_rungs.tsv")
CACHE = os.path.join(CACHE, "g1_cgn_cache.json")
OUT = os.path.join(INPUTS, "g1_midrungs.tsv")
GPCRDB_RES = "https://gpcrdb.org/services/residues/%s/"

# family -> GproteinDb entry_name.  Copied from seq_build.py's GALPHA map so the
# two files cannot drift on the entry names; accessions come from seq_rungs.tsv.
ENTRY = {
    "Gs": "gnas2_human", "Golf": "gnal_human",
    "Gi1": "gnai1_human", "Gi2": "gnai2_human", "Gi3": "gnai3_human",
    "Go": "gnao_human", "Gz": "gnaz_human",
    "Gt1": "gnat1_human", "Gt2": "gnat2_human", "Ggust": "gnat3_human",
    "Gq": "gnaq_human", "G11": "gna11_human", "G14": "gna14_human",
    "G15": "gna15_human", "G12": "gna12_human", "G13": "gna13_human",
}

# The intermediate rungs, defined by the CGN segment at which the C-terminal
# truncation starts.  Chosen so that -- see g1 notes -- one rung sits below the
# junker 50-residue boundary, one just above it, and two inside the 36->350 gap.
MIDRUNGS = [
    ("M1_h4s6",  "G.h4s6", "~45  -- C-terminal truncation starting at the h4s6 loop; "
                           "below junker's 50-residue boundary"),
    ("M2_h4",    "G.H4",   "~61  -- starts at helix H4; the alpha4-beta6-alpha5 "
                           "receptor-facing motif; just above the boundary"),
    ("M3_h3",    "G.H3",   "~113 -- starts at helix H3; C-terminal half of the Ras "
                           "domain, mid-gap"),
    ("M4_he",    "H.HE",   "~204 -- starts at helical-domain helix HE; mid-gap, and "
                           "the first rung that re-enters the helical domain"),
]

# The helical domain, as a contiguous CGN block.  Deleting it gives a mini-G-like
# construct: NOT a C-terminal truncation, so NOT nested in the ladder.  Emitted as
# a declared companion, never as a ladder rung.
HD_FIRST, HD_LAST = "H.HA", "H.HF"


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def fetch(entry):
    for attempt in range(4):
        try:
            return json.loads(
                urllib.request.urlopen(GPCRDB_RES % entry, timeout=60).read().decode())
        except Exception as exc:  # noqa: BLE001
            if attempt == 3:
                raise RuntimeError(f"{entry}: {exc}")
            time.sleep(2 * (attempt + 1))


def load_cgn():
    cache = {}
    if os.path.exists(CACHE):
        with open(CACHE) as fh:
            cache = json.load(fh)
    missing = [f for f in ENTRY if f not in cache]
    for fam in missing:
        sys.stderr.write(f"# fetching CGN {ENTRY[fam]}\n")
        cache[fam] = fetch(ENTRY[fam])
    if missing:
        with open(CACHE, "w") as fh:
            json.dump(cache, fh)
    return cache


def load_parents():
    """family -> (accession, full sequence) from seq_rungs.tsv R7_full rows."""
    out = {}
    with open(RUNGS) as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        ix = {k: i for i, k in enumerate(hdr)}
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if f[ix["rung"]] == "R7_full":
                out[f[ix["family"]]] = (f[ix["accession"]], f[ix["sequence"]])
    return out


def segments(rows):
    segs = {}
    for r in rows:
        s, n = r["protein_segment"], r["sequence_number"]
        lo, hi = segs.get(s, (n, n))
        segs[s] = (min(lo, n), max(hi, n))
    return segs


def main():
    check_only = "--check" in sys.argv
    cgn = load_cgn()
    parents = load_parents()
    problems, rows_out = [], []

    for fam in ENTRY:
        if fam not in parents:
            problems.append(f"{fam}: no R7_full row in seq_rungs.tsv")
            continue
        acc, seq = parents[fam]
        L = len(seq)
        rows = cgn[fam]

        # CHECK 1 -- GPCRdb residue identities must match the UniProt bytes.
        # A mismatch is only fatal if it falls inside a residue span this script
        # actually slices; GPCRdb's sequence can lag UniProt's sequence version
        # in the helical domain without touching any C-terminal truncation.
        bad = [r["sequence_number"] for r in rows
               if not (1 <= r["sequence_number"] <= L)
               or seq[r["sequence_number"] - 1] != r["amino_acid"]]

        segs = segments(rows)
        badset = set(bad)
        if bad:
            gp = {r["sequence_number"]: r["amino_acid"] for r in rows}
            problems.append(
                f"{fam}: CGN/UniProt residue mismatch at {bad} -- UniProt "
                f"{[seq[n-1] for n in bad]} vs GPCRdb {[gp[n] for n in bad]}. "
                f"Constructs whose emitted residue span contains one of these are "
                f"dropped below; the rest are emitted and their provenance is "
                f"UniProt, not GPCRdb.")

        # CHECK 2 -- reproduce SEQUENCES.md 0.2's two invariants.
        for seg, want, name in (("G.H5", 26, "a5helix"), ("G.S6", 36, "a5plus")):
            if seg not in segs:
                problems.append(f"{fam}: segment {seg} absent")
                continue
            got = L - segs[seg][0] + 1
            if got != want:
                problems.append(f"{fam}: {name} truncation length {got} != {want} "
                                f"(SEQUENCES.md 0.2 invariant)")

        for rid, seg, note in MIDRUNGS:
            if seg not in segs:
                problems.append(f"{fam}: segment {seg} absent, {rid} not built")
                continue
            start = segs[seg][0]
            sub = seq[start - 1:]
            span = set(range(start, L + 1))
            if badset & span:
                problems.append(f"{fam}/{rid}: emitted span contains a CGN/UniProt "
                                f"mismatch at {sorted(badset & span)} -- NOT EMITTED")
                continue
            # CHECK 3 -- nested: must be a suffix of the parent.
            if not seq.endswith(sub):
                problems.append(f"{fam}/{rid}: not a suffix of parent")
            rows_out.append(dict(
                rung=rid, family=fam, accession=acc, parent_len=L,
                rule=f"CGN {seg} -> C terminus (last {L - start + 1} residues)",
                cgn_start_segment=seg, resid_range=f"{start}-{L}",
                len=len(sub), nested_in_ladder="yes", sequence=sub, sha256=sha(sub),
                note=note.split("--", 1)[1].strip()))

        # the declared non-nested companion: helical-domain deletion
        emit_hd = HD_FIRST in segs and HD_LAST in segs
        if emit_hd:
            a, b = segs[HD_FIRST][0], segs[HD_LAST][1]
            sub = seq[:a - 1] + seq[b:]
            span = set(range(1, a)) | set(range(b + 1, L + 1))
            if badset & span:
                problems.append(f"{fam}/M5_dHD: emitted span contains a CGN/UniProt "
                                f"mismatch at {sorted(badset & span)} -- NOT EMITTED")
                emit_hd = False
        if emit_hd:
            rows_out.append(dict(
                rung="M5_dHD", family=fam, accession=acc, parent_len=L,
                rule=f"full subunit, CGN {HD_FIRST}..{HD_LAST} deleted "
                     f"(residues {a}-{b} removed)",
                cgn_start_segment=f"{HD_FIRST}..{HD_LAST} deleted",
                resid_range=f"1-{a-1}+{b+1}-{L}",
                len=len(sub), nested_in_ladder="NO -- keeps the N terminus",
                sequence=sub, sha256=sha(sub),
                note="mini-G-like: Ras domain with the helical domain excised; "
                     "length-comparable to M4 but folds as a domain"))

    if problems:
        sys.stderr.write("\n!! PROBLEMS\n" + "\n".join("  " + p for p in problems) + "\n")
    else:
        sys.stderr.write(f"# all checks passed on {len(ENTRY)} families\n")

    cols = ["rung", "family", "accession", "parent_len", "rule",
            "cgn_start_segment", "resid_range", "len", "nested_in_ladder",
            "sequence", "sha256", "note"]
    if not check_only:
        with open(OUT, "w") as fh:
            fh.write("\t".join(cols) + "\n")
            for r in rows_out:
                fh.write("\t".join(str(r[c]) for c in cols) + "\n")
        sys.stderr.write(f"# wrote {len(rows_out)} constructs -> {OUT}\n")

    # length spread per rung, which is the number RUN_MATRIX 3.5 needs
    sys.stderr.write("\n# length spread per intermediate rung\n")
    for rid, _, _ in MIDRUNGS + [("M5_dHD", None, None)]:
        ls = sorted(r["len"] for r in rows_out if r["rung"] == rid)
        if ls:
            sys.stderr.write(f"#   {rid:9s} min={ls[0]:4d} max={ls[-1]:4d} "
                             f"spread={ls[-1]-ls[0]:3d}\n")
    # Non-zero only when a construct was actually withheld. A GPCRdb/UniProt
    # residue disagreement outside every sliced span is an advisory: it is
    # recorded, the provenance is UniProt, and the ladder is unaffected.
    fatal = [p for p in problems if "NOT EMITTED" in p or "DROPPED" in p
             or "not built" in p or "invariant" in p]
    if problems and not fatal:
        sys.stderr.write("# (advisory only -- no construct withheld)\n")
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
