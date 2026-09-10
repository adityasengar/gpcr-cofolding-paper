#!/usr/bin/env python3
"""
Does the INACTIVE TM6 position occupy the volume the alpha5 helix binds in?

This came out of building the GA-style-3 graphical abstract. Superposing a
cognate prediction on the SAME receptor's deposited inactive structure put the
deposited TM6 straight through the alpha5 helix, and the question is whether
that is a property of one pair of files or a general fact about the two states.

WHAT IS MEASURED, AND WHAT IT IS NOT
    It is NOT a contact. The closest separations here are far below van der
    Waals contact - a 0.22 A heavy-atom separation is a clash, not a bond - and
    reporting them as contacts invites the obvious objection. The quantity is
    MUTUAL EXCLUSION OF VOLUME: how many heavy atoms of the alpha5 helix, as
    placed by the prediction, fall inside the space the deposited inactive TM6
    occupies. The reported statistic is the count of alpha5 heavy atoms with a
    deposited-TM6 heavy atom within 4.0 A (roughly two carbon van der Waals
    radii + slack) and within 3.0 A (unambiguous overlap), expressed as a
    fraction of the alpha5's heavy atoms.

THE ATOM SETS, stated because the number is meaningless without them
    A  the alpha5 C-terminal 21 residues of the prediction's partner chain, all
       non-hydrogen ATOM records, in the prediction's own frame.
    B  residues `tm6` of the deposited structure, all non-hydrogen ATOM
       records, moved onto the prediction by a Kabsch fit over receptor CA in a
       set that EXCLUDES TM6 and ICL3 - so the fit is on the invariant
       scaffold and cannot be accused of having pushed TM6 into the peptide.
    Distances are all-against-all between A and B.

THE CONTROLS, which are the point
    1. The SAME measurement against the deposited ACTIVE structure of the same
       receptor, superposed by the same rule.
    2. The same measurement against the PREDICTION's OWN TM6. A model does not
       clash with itself, so this is a floor: whatever it returns is the value
       "no exclusion" looks like on this scale.
    Without those two, a large count against the inactive structure could just
    mean the alpha5 is drawn somewhere crowded.

    The active control is NOT zero and the report must not pretend it is. DRD2
    row 8285 buries 18 of its 166 alpha5 heavy atoms in 7JVR's TM6 against 86
    in 6CM4's, i.e. 11% versus 52%, on a 1.04 A and a 2.57 A fit respectively.
    Some of that 11% is the fit residual and some is a real difference between
    where this model puts the alpha5 and where 7JVR's own Ga sits. The claim
    the numbers support is an ORDERING - inactive >> active > self - not that
    the active state is clash-free.

EVERY DEPOSITED STRUCTURE IS VERIFIED FIRST against the two values
`02_references/reference_predicates.csv` stores for it, from its own
coordinates, at the residue numbers the scorer used. Four of the drop's
ALIGNMENT.md files name residues that do not reproduce their own distances
(D13, D20) and one shipped CIF is the wrong protein entirely (D18), so no file
is trusted because of where it came from.

Run: python3 figures/block_a/steric_exclusion.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.dirname(HERE)
ROOT = os.path.dirname(FIGDIR)
for p in (HERE, os.path.join(HERE, "panels"), FIGDIR):
    if p not in sys.path:
        sys.path.insert(0, p)

import cifread as CR                                           # noqa: E402
import dofrender as D                                          # noqa: E402
import hero_renders as HR                                      # noqa: E402

ST = os.path.join(FIGDIR, "structures")

# (label, prediction cif, receptor chain, peptide chain + span, receptor
#  window, anchors of the prediction, deposited structures to test)
CASES = [
    dict(
        name="DRD2 · row 8285 · OpenFold-3 · cognate",
        pred=HR.DRD2_COG, chain="A", pep=("B", 334, 354), window=(30, 443),
        fit=(34, 441),   # the same window ga_style3_superposition.py fits on
        anch=HR.ANCHORS["drd2"],
        deposited=[
            ("6CM4", os.path.join(ST, "6CM4.cif"), "A", "inactive",
             dict(tilt=(76, 375), npxxy=(209, 426), tm6=(366, 398),
                  d_tilt=11.445926, d_npxxy=10.030448)),
            ("7JVR", HR.DRD2_REF, "R", "active", HR.ANCHORS["7jvr"]),
        ]),
    dict(
        name="ACM1 · row 948 · Chai-1 · cognate",
        pred=HR.ACM1_HEALTHY, chain="A", pep=("B", 339, 359), window=(1, 460),
        fit=(20, 439),   # 6ZFZ models the receptor over 20-219 and 354-439
        anch=HR.ANCHORS["acm1_healthy"],
        deposited=[
            ("6ZFZ", os.path.join(ST, "6ZFZ.cif"), "A", "inactive",
             dict(tilt=(67, 367), npxxy=(208, 418), tm6=(358, 390),
                  d_tilt=13.041540, d_npxxy=13.663578)),
        ]),
]

CUT4, CUT3 = 4.0, 3.0


def _ca_map(atoms, chain):
    return dict((a["resi"], a["xyz"]) for a in atoms
                if a["name"] == "CA" and a["chain"] == chain
                and a["group"] == "ATOM")


def _fit(mob, tgt, mc, tc, resids):
    m, t = _ca_map(mob, mc), _ca_map(tgt, tc)
    pairs = [(m[r], t[r]) for r in resids if r in m and r in t]
    if len(pairs) < 80:
        raise ValueError("only %d shared CA" % len(pairs))
    A = np.array([p[0] for p in pairs])
    Bt = np.array([p[1] for p in pairs])
    ca_, cb_ = A.mean(0), Bt.mean(0)
    U, _, Vt = np.linalg.svd((A - ca_).T @ (Bt - cb_))
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    t_ = cb_ - ca_ @ R.T
    rms = float(np.sqrt((((A @ R.T + t_) - Bt) ** 2).sum(1).mean()))
    return R, t_, len(pairs), rms


def _heavy(atoms, chain, lo, hi):
    return [a for a in atoms if a["chain"] == chain and a["elem"] != "H"
            and a["group"] == "ATOM" and lo <= a["resi"] <= hi]


def _overlap(X, Y, xa, ya):
    """X = deposited TM6 heavy atoms (moved), Y = alpha5 heavy atoms."""
    d = np.linalg.norm(np.asarray(X)[:, None, :] - np.asarray(Y)[None, :, :],
                       axis=2)
    i, j = np.unravel_index(np.argmin(d), d.shape)
    near = d.min(axis=0)
    return dict(
        pairs4=int((d < CUT4).sum()), pairs3=int((d < CUT3).sum()),
        pep4=int((near < CUT4).sum()), pep3=int((near < CUT3).sum()),
        n_pep=len(Y), dmin=float(d.min()),
        pair=u"%s%d %s – %s%d %s" % (xa[i]["resn"].title(), xa[i]["resi"],
                                     xa[i]["name"], ya[j]["resn"].title(),
                                     ya[j]["resi"], ya[j]["name"]))


def run_case(case):
    a = case["anch"]
    pred = CR.frame(case["pred"])
    icl3 = (a["npxxy"][0] + 10, a["tm6"][0] - 1)
    fit_res = [r for r in range(case["fit"][0], case["fit"][1] + 1)
               if not (icl3[0] <= r <= icl3[1])
               and not (a["tm6"][0] <= r <= a["tm6"][1])]

    pep_atoms = _heavy(pred, case["pep"][0], case["pep"][1], case["pep"][2])
    Y = [x["xyz"] for x in pep_atoms]

    print("\n=== %s" % case["name"])
    print("    alpha5 %s %d-%d : %d heavy atoms"
          % (case["pep"][0], case["pep"][1], case["pep"][2], len(Y)))

    # control 2: the prediction's own TM6, no superposition involved
    own = _heavy(pred, case["chain"], a["tm6"][0], a["tm6"][1])
    o = _overlap([x["xyz"] for x in own], Y, own, pep_atoms)
    print("    CONTROL  own predicted TM6 %d-%d           "
          "pairs<4 %5d  <3 %4d   alpha5 atoms<4 %3d/%d   closest %.2f A  (%s)"
          % (a["tm6"][0], a["tm6"][1], o["pairs4"], o["pairs3"], o["pep4"],
             o["n_pep"], o["dmin"], o["pair"]))

    rows = []
    for pdb, path, chain, state, anch in case["deposited"]:
        # verify before use - both stored values, from the file's own coords
        CR.verify_anchor(path, (chain, anch["tilt"][0], "CA"),
                         (chain, anch["tilt"][1], "CA"), anch["d_tilt"],
                         what="%s tilt" % pdb)
        CR.verify_anchor(path, (chain, anch["npxxy"][0], "OH"),
                         (chain, anch["npxxy"][1], "OH"), anch["d_npxxy"],
                         what="%s NPxxY" % pdb)
        dep = CR.frame(path)
        R, t, npair, rms = _fit(dep, pred, chain, case["chain"], fit_res)
        tm6 = _heavy(dep, chain, anch["tm6"][0], anch["tm6"][1])
        X = D.apply_rt([x["xyz"] for x in tm6], R, t)
        r = _overlap(X, Y, tm6, pep_atoms)
        r.update(pdb=pdb, state=state, npair=npair, rms=rms)
        rows.append(r)
        print("    %-6s %-8s TM6 %d-%d  fit %3d CA %.2f A   "
              "pairs<4 %5d  <3 %4d   alpha5 atoms<4 %3d/%d   closest %.2f A  (%s)"
              % (pdb, state, anch["tm6"][0], anch["tm6"][1], npair, rms,
                 r["pairs4"], r["pairs3"], r["pep4"], r["n_pep"], r["dmin"],
                 r["pair"]))
    return rows


def main():
    print(__doc__.split("Run:")[0].strip()[:0] or "", end="")
    print("STERIC EXCLUSION: does the deposited INACTIVE TM6 occupy the alpha5 "
          "site?")
    print("counts are heavy-atom pairs; 'alpha5 atoms<4' is how many of the "
          "peptide's own heavy atoms are buried in the TM6 volume")
    for case in CASES:
        run_case(case)
    print("\nRead: the quantity is MUTUAL EXCLUSION OF VOLUME, not a contact "
          "distance. What the\nnumbers support is an ordering - the deposited "
          "INACTIVE TM6 buries roughly half\nthe alpha5's heavy atoms, the "
          "deposited ACTIVE one about a fifth of that, and the\nmodel's own "
          "TM6 almost none. The active control is not zero and must not be "
          "reported\nas though it were.")


if __name__ == "__main__":
    main()
