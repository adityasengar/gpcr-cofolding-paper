#!/usr/bin/env python3
"""Measure the NPxxY hydroxyl distance in Block D's shipped structures.

WHY. Block D ships no row-level data at all, so the fifteen CIFs are the only
place in the drop where a number can be recomputed from something other than
prose. `10_structures/MANIFEST.json` states specific distances in its
`dossier_finding` strings -- "NPxxY-OH 4.53 A", "NPxxY-OH 19.1 A", "NPxxY
11 -> 3.4 A" -- and Block A's failure classes include exactly this: four
`ALIGNMENT.md` files named residues that did not reproduce the shipped
distances. A stated distance beside a coordinate file is a claim, not a
measurement, until someone measures it.

HOW Y7.53 IS FOUND, and why not from a numbering table. The NPxxY motif is
located in the chain's own sequence: N-P-x-x-Y, and its tyrosine is 7.53 by
definition. That needs no external residue map and cannot be knocked out of
register by a construct offset -- which matters here because these are
predicted full-length models, not deposited constructs, and their author
numbering need not match any reference. The method self-validates on OPSD:
it returns auth_seq 306, which is exactly what Block B's pinned anchor table
records for OPSD 7.53.

Y5.58 CANNOT be found the same way -- it sits in TM5 with no motif to anchor it.
The first version of this script took the tyrosine whose OH was CLOSEST to
Y7.53's among those 90-160 residues upstream. That is circular: choosing the
nearest candidate biases the distance downward by construction, and it was right
on only four of ten receptors -- it put OPSD's 5.58 at 178 (223), AGTR1's at 184
(215) and OPRK's at 219 (246), and failed outright on ACM2, whose 130-residue
ICL3 puts 5.58 more than 200 residues upstream of 7.53.

So 5.58 comes from a table, and the table is CHECKED rather than trusted: the
residue at each position must actually be a tyrosine with a modelled OH, or the
file returns a refusal instead of a number. The positions are the GPCRdb-mapped
anchors carried in Block B's pinned reference set. Using them here is a
NUMBERING lookup, not a borrowed result -- and the identity check is what makes
it safe, because a construct offset would land on some other residue and be
caught immediately.

The CIF column order is read from each file's own _atom_site loop header. It is
not the same in every file in this drop, and assuming a fixed order crashed on
the second file tried.

Usage:  python3 analysis/block_d/cifmeasure.py
"""
import glob
import json
import math
import os
import sys

AA3 = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLN': 'Q',
       'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
       'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W',
       'TYR': 'Y', 'VAL': 'V'}

# GPCRdb-mapped (5.58, 7.53) per receptor, from Block B's pinned reference set
# (`data/block_b/09_references/reference_set.blockb_pinned.csv`,
# `anchor_positions`). Every 7.53 here was reproduced independently by locating
# the NPxxY motif in the Block D coordinates themselves -- 10 of 10 agree, which
# is what licenses using the same table's 5.58.
ANCHORS = {
    "5ht1b": (228, 369), "acm2": (206, 440), "adrb2": (219, 326),
    "agtr1": (215, 302), "cnr2": (209, 299), "ghsr": (232, 323),
    "lpar1": (225, 311), "npy1r": (231, 320), "oprk": (246, 330),
    "opsd": (223, 306),
}

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
STRUCT = os.path.join(ROOT, "data", "block_d", "10_structures")


def parse_cif(path):
    """Atoms, with the column order taken from this file's own loop header."""
    cols, atoms, in_loop = [], [], False
    for line in open(path):
        if line.startswith("_atom_site."):
            cols.append(line.strip().split(".")[1])
            in_loop = True
            continue
        if in_loop and line.startswith(("ATOM", "HETATM")):
            f = line.split()
            if len(f) != len(cols):
                continue
            r = dict(zip(cols, f))
            try:
                atoms.append(dict(
                    atom=r.get("label_atom_id"), comp=r.get("label_comp_id"),
                    chain=r.get("label_asym_id"), seq=int(r.get("label_seq_id")),
                    auth=r.get("auth_seq_id"),
                    x=float(r["Cartn_x"]), y=float(r["Cartn_y"]),
                    z=float(r["Cartn_z"]), het=line.startswith("HETATM")))
            except (TypeError, ValueError):
                continue
        elif in_loop and line.strip() in ("#", ""):
            if atoms:
                in_loop = False
    return atoms


def dist(a, b):
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2
                     + (a["z"] - b["z"]) ** 2)


def receptor_chain(atoms):
    """The longest polymer chain. In D2 the nanobody is a second chain."""
    n = {}
    for a in atoms:
        if a["comp"] in AA3:
            n.setdefault(a["chain"], set()).add(a["seq"])
    return max(n, key=lambda c: len(n[c])) if n else None


def npxxy_oh(path, receptor):
    """d(Y5.58 OH, Y7.53 OH), with both anchors identity-checked.

    Returns a refusal, never a guess, if either position is not a modelled
    tyrosine hydroxyl. `motif_y753` is the position found independently from the
    NPxxY motif and is reported so the two can be compared on every file.
    """
    atoms = parse_cif(path)
    ch = receptor_chain(atoms)
    if ch is None:
        return dict(note="no polymer chain")
    res = {}
    for a in atoms:
        if a["chain"] == ch and a["comp"] in AA3:
            res.setdefault(a["seq"], {})["comp"] = a["comp"]
            if a["atom"] == "OH":
                res[a["seq"]]["OH"] = a
    order = sorted(res)
    seq = "".join(AA3[res[k]["comp"]] for k in order)
    hits = [i for i in range(len(seq) - 4)
            if seq[i] == "N" and seq[i + 1] == "P" and seq[i + 4] == "Y"]
    motif = order[hits[-1] + 4] if hits else None

    anc = ANCHORS.get(receptor)
    if anc is None:
        return dict(chain=ch, motif_y753=motif,
                    note="no anchor table entry for %s" % receptor)
    p558, p753 = anc
    for pos, label in ((p558, "5.58"), (p753, "7.53")):
        r = res.get(pos)
        if r is None or r["comp"] != "TYR":
            return dict(chain=ch, motif_y753=motif,
                        note="position %d (%s) is %s, not TYR -- refusing"
                             % (pos, label, (r or {}).get("comp", "absent")))
        if "OH" not in r:
            return dict(chain=ch, motif_y753=motif,
                        note="position %d (%s) has no OH modelled" % (pos, label))
    return dict(chain=ch, y558=p558, y753=p753, motif_y753=motif,
                motif_agrees=(motif == p753),
                npxxy_oh=round(dist(res[p558]["OH"], res[p753]["OH"]), 2))


def main():
    man = json.load(open(os.path.join(STRUCT, "MANIFEST.json")))
    stated = {e["filename"]: e.get("dossier_finding", "")
              for e in man["spot_check"] + man["random"]}

    print("=" * 96)
    print("BLOCK D STRUCTURES -- NPxxY hydroxyl distance, recomputed from coordinates")
    print("=" * 96)
    print("%-40s %5s %5s %6s %8s  %s"
          % ("file", "Y5.58", "Y7.53", "motif?", "d(OH-OH)", "stated in MANIFEST"))
    print("-" * 96)

    out = {}
    for p in sorted(glob.glob(os.path.join(STRUCT, "*", "*.cif"))):
        fn = os.path.basename(p)
        rec = next((e["receptor"] for e in man["spot_check"] + man["random"]
                    if e["filename"] == fn), "")
        m = npxxy_oh(p, rec) or {}
        out[fn] = m
        claim = ""
        for tok in ("NPxxY-OH", "NPxxY"):
            if tok in stated.get(fn, ""):
                seg = stated[fn][stated[fn].index(tok):]
                claim = seg[:34].replace("\n", " ")
                break
        print("%-40s %5s %5s %6s %8s  %s"
              % (fn[:40], m.get("y558", "-"), m.get("y753", "-"),
                 {True: "yes", False: "NO", None: "-"}.get(m.get("motif_agrees"), "-"),
                 m.get("npxxy_oh", m.get("note", "-")), claim))

    json.dump(out, open(os.path.join(HERE, "cif_measurements.json"), "w"),
              indent=1)
    print("-" * 96)
    print("Written to analysis/block_d/cif_measurements.json.")
    print("motif? compares the tabled 7.53 against the position found "
          "independently\nfrom this file's own NPxxY motif. A NO means the "
          "anchor table and the\ncoordinates disagree and no distance from that "
          "row should be used.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
