"""
A minimal mmCIF `_atom_site` reader, and the anchor-verification routine.

Biopython's MMCIFParser refuses the prediction files in `11_structures/` -
they carry no `_atom_site.occupancy` column - and gemmi is not installed here,
so the loop is read directly. Only the columns a figure needs are kept.

The reason this module exists at all is `verify_anchor`. Three of the shipped
`ALIGNMENT.md` files name residues that are not the residues the scorer
measured (DISCREPANCY_REPORT D13): the tilt anchors are given as L124/F282 on
2RH1 where the pair reproducing the stored `d_tilt_ref` is L75/L275, and the
AA2AR file says L88 and Y213 where the file's own coordinates say L48 and
Y197. So no residue number reaches a render until the pair has been shown to
reproduce the distance stored for that row, from that row's own coordinates.
"""
import numpy as np


def read_atoms(path):
    cols, rows, in_loop = [], [], False
    with open(path) as fh:
        for line in fh:
            s = line.strip()
            if s.startswith("_atom_site."):
                cols.append(s.split(".", 1)[1].split()[0])
                in_loop = True
                continue
            if in_loop:
                if s.startswith("ATOM") or s.startswith("HETATM"):
                    f = s.split()
                    if len(f) >= len(cols):
                        rows.append(dict(zip(cols, f[:len(cols)])))
                elif rows and (s.startswith("#") or s == ""):
                    in_loop = False
    return rows


def frame(path):
    """[{chain, resi, resn, name, elem, bfac, xyz, group}] for every atom."""
    out = []

    def g(r, *names):
        for n in names:
            if n in r and r[n] not in ("?", "."):
                return r[n]
        return None

    for r in read_atoms(path):
        try:
            out.append(dict(
                chain=g(r, "auth_asym_id", "label_asym_id"),
                resi=int(g(r, "auth_seq_id", "label_seq_id")),
                resn=g(r, "auth_comp_id", "label_comp_id"),
                name=g(r, "auth_atom_id", "label_atom_id"),
                elem=g(r, "type_symbol"),
                bfac=float(g(r, "B_iso_or_equiv") or 0.0),
                xyz=np.array([float(r["Cartn_x"]), float(r["Cartn_y"]),
                              float(r["Cartn_z"])]),
                group=r["group_PDB"]))
        except (TypeError, ValueError, KeyError):
            continue
    return out


def atom(atoms, chain, resi, name):
    for a in atoms:
        if (a["chain"] == chain and a["resi"] == resi and a["name"] == name
                and a["group"] == "ATOM"):
            return a["xyz"]
    raise KeyError("no %s of %s%d in the file" % (name, chain, resi))


def residue_name(atoms, chain, resi):
    for a in atoms:
        if a["chain"] == chain and a["resi"] == resi and a["name"] == "CA":
            return a["resn"]
    raise KeyError("no CA of %s%d" % (chain, resi))


def distance(atoms, a1, a2):
    """a1, a2 are (chain, resi, atom_name)."""
    return float(np.linalg.norm(atom(atoms, *a1) - atom(atoms, *a2)))


def verify_anchor(path, a1, a2, expected, tol=2e-3, what=""):
    """
    Measure a pair and REFUSE if it does not reproduce the stored value.

    Returns the measured distance. Raises otherwise - a render may not draw a
    number it has not reproduced from the coordinates it is drawing.
    """
    atoms = frame(path)
    d = distance(atoms, a1, a2)
    if abs(d - expected) > tol:
        raise ValueError(
            "%s: %s%d %s - %s%d %s measures %.4f A but the tidy data stores "
            "%.4f A for this row. The residue pair is wrong; do not draw it. "
            "(This is exactly DISCREPANCY_REPORT D13.)"
            % (what or path, a1[0], a1[1], a1[2], a2[0], a2[1], a2[2],
               d, expected))
    return d


def find_pair(path, target, name_a="CA", name_b="CA", tol=2e-3, chain=None):
    """Brute-force search for the residue pair that reproduces `target`."""
    atoms = frame(path)
    A = [a for a in atoms if a["name"] == name_a and a["group"] == "ATOM"
         and (chain is None or a["chain"] == chain)]
    Bb = [a for a in atoms if a["name"] == name_b and a["group"] == "ATOM"
          and (chain is None or a["chain"] == chain)]
    hits = []
    for x in A:
        for y in Bb:
            if (x["chain"], x["resi"]) >= (y["chain"], y["resi"]):
                continue
            d = float(np.linalg.norm(x["xyz"] - y["xyz"]))
            if abs(d - target) < tol:
                hits.append(((x["chain"], x["resi"], x["resn"]),
                             (y["chain"], y["resi"], y["resn"]), d))
    return hits
