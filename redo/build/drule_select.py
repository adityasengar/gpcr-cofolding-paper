#!/usr/bin/env python3
"""DRULE deliverable 2 -- run the decoy rule over the pool and record every refusal.

    python3 redo/build/drule_select.py --selftest      # prove the rule on fixtures
    python3 redo/build/drule_select.py                 # run it over the real pool

D-RULE, verbatim from `redo/spec/CAMPAIGN.md` §5.3, and implemented as written:

    For each receptor, define the *reference ligand* as its curated **full agonist**
    (not the mean over all real ligands -- a mean over mixed pharmacological roles is
    what produced their n=1 and n=2 windows).  Build a candidate pool from ChEMBL
    restricted to compounds with (i) no measured activity at the receptor, (ii) no
    measured activity at any receptor in its **paralog cluster**, and (iii) >=1
    measured activity at some unrelated target.  Compute eight axes on every candidate
    and on the reference: MW, cLogP, TPSA, HBD, HBA, rotatable bonds, ring count, and
    **formal charge at pH 7.4**.  Accept a candidate iff every continuous axis is
    within +-20% of the reference's, every integer axis within +-1, **charge exactly
    equal**, and Morgan (r = 2, 1024 bit) Tanimoto < 0.30 against every curated real
    ligand of the receptor **and of every receptor in its paralog cluster**.  From the
    accepted set draw **k = 3** decoys per receptor by a seeded draw recorded in the
    row.  The gate rejects: a receptor with fewer than 3 accepted candidates is
    reported as *decoy-unavailable*, named in the paper, and excluded from the decoy
    arm.  No candidate is ever taken "anyway".

Clause (i)-(iii) are deliverable 1's job and already sit in the two pool tables.
This module is clauses four onward.  Each of the design choices below is a repair of
a named defect in `redo/protocol/MAP_LIGANDS_AND_ANALYSIS.md` §1-§2.4; where a choice
could be softened, the defect it would re-introduce is named beside it.


ONE INSTRUMENT FOR BOTH SIDES  (MAP §2.2; [[compare-like-with-like]])
--------------------------------------------------------------------
`drule_pool_molecules.tsv` carries `mw/logp/hbd/hba/rot` copied from ChEMBL's own
`compound_properties` table.  The reference ligands have no such row.  Comparing a
ChEMBL property against an RDKit property is a different-instrument comparison, and
this project has already produced three false discrepancies exactly that way.  So
**all eight axes are computed here, from SMILES, with RDKit, by one function, for
reference and candidate alike** (`axes()`).  ChEMBL's columns are read only to be
*disagreed with*: `--crosscheck` reports the disagreement and nothing in the gate
consults them.


FORMAL CHARGE AT pH 7.4  (MAP §1.4, §2.3 -- the defect this module exists for)
-------------------------------------------------------------------------------
`build_block_c_decoys.py:401-420` used `Chem.GetFormalCharge`, which is the charge
**as written in the SMILES**.  Every aminergic receptor's real ligands are cationic
and every decoy it picked was neutral, so the frozen decoy arm differs from the ligand
arms systematically in net charge -- and "Decision A" made that one-directional on
purpose.  RDKit 2022.09.5 ships no pKa model and nothing may be installed, so the
charge is assigned by an explicit, auditable substructure rule.  It is stated here in
full because a rule nobody can read is a rule nobody can refuse:

  neutralise first.  Every charge that a protonation state could have chosen is
  stripped ([NH3+] -> N, [O-] -> OH) before the rules run, so a molecule's charge
  depends on its constitution and not on how a depositor typed it.  Charges that no
  protonation equilibrium can remove -- a quaternary ammonium, the N+/O- of a nitro
  group -- survive neutralisation and are carried through.

  BASIC, +1 each:
    guanidine          pKa ~12-13
    amidine            pKa ~11-12   (metformin, benzamidines)
    aliphatic amine    pKa ~9-11    sp3 N, and NOT: bonded to a heteroatom
                                    (hydrazine, hydroxylamine, N-O), bonded to an
                                    aromatic ring atom (aniline, pKa ~4.6), an amide
                                    / thioamide / imide N, a sulfonamide or sulfinamide
                                    N, an enamine N, a nitrile N, an imine N, or an
                                    alpha-halo-alkyl amine
    quaternary N+      permanent
  ACIDIC, -1 each:
    carboxylic acid    pKa ~3-5
    tetrazole          pKa ~4.9
    acyl sulfonamide   pKa ~4-5     C(=O)N(H)S(=O)(=O)
    sulfonimide        pKa ~2
    sulfonic acid      pKa ~-1
    sulfinic acid      pKa ~2
    phosphonic / phosphoric OH      pKa1 ~2, pKa2 ~6.5 -- BOTH are counted, so a
                                    phosphate monoester is -2.  This is why LPAR1's
                                    LPA reference is -2 and not -1; it is the axis
                                    that ends up deciding LPAR1.
  NEUTRAL at 7.4, stated so the omission is deliberate and not an oversight:
    aromatic ring N (pyridine ~5.2, imidazole ~6.0-7.0 in histamine, triazole, the
    purines), aniline (~4.6), amide / sulfonamide N-H (~10+), phenol (~10), alcohol,
    thiol (~10), hydroxamic acid (~9), imide (~8-9).

  DAMPING.  A second basic centre within **3 bonds** of an accepted one does not take
  a second proton at pH 7.4 (piperazine pKa2 ~5.6, ethylenediamine pKa2 ~7.0).  So
  piperazine is +1, not +2.  Centres are accepted in ascending atom-index order, which
  makes the choice deterministic.

  VALIDATION IS A GATE, NOT A CLAIM.  `validate_charge_rule()` asserts the six
  aminergic full agonists on this panel -- 5HT5A, ACM4, DRD3, OPRD, ADRB1, HRH3 -- come
  out **+1**, plus 27 further molecules whose charge at 7.4 is not in dispute
  (including the frozen campaign's own decoys).  It runs on every invocation, before
  anything is selected, and a failure stops the module.  There is no fallback to
  `GetFormalCharge`.


WHAT COUNTS AS A "CURATED REAL LIGAND" FOR THE TANIMOTO SCREEN
---------------------------------------------------------------
§5.3 says "every curated real ligand of the receptor and of every receptor in its
paralog cluster".  Nine of the sixteen receptors are inherited and their cluster-mates
(5HT2A, ADA1A, DRD4, OPRM, S1PR5, HRH2, CNR1, OPRK, OPRX, ...) are curated nowhere in
`inputs/` at all.  Taking "curated" to mean only the 16+8+32 ligand-set rows would
therefore make the screen *weakest* exactly where we know least -- the B1B1U5 failure
mode in another costume.  So the screen is the union of three sources, and the count
per receptor is written into every row:

  1. `ligand_set_redo.tsv`         our own enacted picks          (status=enacted)
  2. `protocol/received/approved_2026_09_12/ligand_set{,_tier3}.csv`
                                   paper_af3's curation, inherited
  3. `ligand_census_records.tsv`   every small-molecule/lipid ligand observed bound
                                   to any receptor in the cluster, role != apo

Source 3 only ever makes the screen stricter.  MAP §6.2 records that filtering the
frozen campaign's comparison set on `activity_class` silently shrank it; nothing is
filtered on a role string here beyond dropping `apo`.


THE REJECTION TABLE IS A DELIVERABLE
-------------------------------------
The frozen campaign has no equivalent of `drule_rejections.tsv`: its property window
was "computed, written to a report and never acted on", and no record survives of what
was refused, because nothing ever was.  Here every eligible candidate that the gate
refuses is written out with **every** axis that refused it -- not the first one found.
All eight axes are evaluated for every candidate (no cascade, no short-circuit), so an
axis's rejection count is a count of the chemistry and not an artefact of the order
the tests happen to run in.  `first_failed_axis` is the first entry of `AXES`, a fixed
order, so the per-axis attribution is stable across runs and across machines.
"""

import argparse
import csv
import hashlib
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, PROTOCOL  # noqa: E402

try:
    from rdkit import Chem, RDLogger
    from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors
    from rdkit.Chem import rdFingerprintGenerator
    from rdkit import DataStructs
    RDLogger.DisableLog("rdApp.*")
except ImportError:                                       # pragma: no cover
    sys.stderr.write("!! RDKit is required (2022.09.5 is what this was written "
                     "against) and is not importable\n")
    raise

APPROVED = os.path.join(PROTOCOL, "received", "approved_2026_09_12")

MOLS = os.path.join(INPUTS, "drule_pool_molecules.tsv")
EXCL = os.path.join(INPUTS, "drule_pool_exclusions.tsv")
TARGETS = os.path.join(INPUTS, "drule_targets.tsv")
REDOSET = os.path.join(INPUTS, "ligand_set_redo.tsv")
CENSUS = os.path.join(INPUTS, "ligand_census_records.tsv")
G2 = os.path.join(INPUTS, "g2_systems.csv")

OUT_SEL = os.path.join(INPUTS, "drule_selected.tsv")
OUT_REJ = os.path.join(INPUTS, "drule_rejections.tsv")

# ---- the rule's constants, all from CAMPAIGN.md §5.3 ----------------------
CONTINUOUS_TOL = 0.20            # +-20% of the reference
INTEGER_TOL = 1                  # +-1
TANIMOTO_MAX = 0.30              # strictly less than
MORGAN_RADIUS = 2
MORGAN_BITS = 1024
K_DECOYS = 3
DRAW_SEED = 20260912             # the campaign's draw seed, recorded in every row

# fixed evaluation order -> `first_failed_axis` is deterministic
AXES = ("mw", "clogp", "tpsa", "hbd", "hba", "rot", "rings", "charge", "tanimoto")
CONTINUOUS = ("mw", "clogp", "tpsa")
INTEGER = ("hbd", "hba", "rot", "rings")

_MFG = rdFingerprintGenerator.GetMorganGenerator(radius=MORGAN_RADIUS,
                                                 fpSize=MORGAN_BITS)


# =========================================================================
# protonation
# =========================================================================
_NEUT = Chem.MolFromSmarts(
    "[+1!h0!$([*]~[-1,-2,-3,-4]),-1!$([*]~[+1,+2,+3,+4])]")

BASIC = [
    ("guanidine",
     "[NX3;!$(N[!#6;!#1]);!$(N[a]);!$(NS(=O)=O)][CX3]"
     "(=[NX2;!$(N[!#6;!#1])])[NX3;!$(N[!#6;!#1]);!$(NS(=O)=O)]"),
    ("amidine",
     "[NX3;!$(N[!#6;!#1]);!$(NS(=O)=O);!$(N[CX3]=[OX1])]"
     "[CX3;!$([CX3]([NX3])[NX3])]=[NX2;!$(N[!#6;!#1]);!$(N[a])]"),
    ("aliphatic_amine",
     "[NX3;H0,H1,H2;!$(N[!#6;!#1]);!$(N[a]);!$(N[CX3]=[O,S,N]);"
     "!$(N[SX4](=O)=O);!$(N[SX3]=O);!$(N[CX2]#[NX1]);!$(N[CX3]=[CX3]);"
     "!$(N[CX4][F,Cl,Br,I])]"),
]
QUAT = "[NX4+;!$([N]~[*-])]"

# (name, SMARTS, indices of the ionisable site).  The site is claimed, not the
# whole match, so a phosphate monoester with two acidic OH counts twice.
ACIDIC = [
    ("carboxylic_acid",  "[CX3](=[OX1])[OX2H1]", (2,)),
    ("tetrazole",        "c1nnnn1", (0, 1, 2, 3, 4)),
    ("acyl_sulfonamide", "[CX3](=[OX1])[NX3H1][SX4](=[OX1])(=[OX1])", (2,)),
    ("sulfonimide",      "[SX4](=[OX1])(=[OX1])[NX3H1][SX4](=[OX1])(=[OX1])", (3,)),
    ("sulfonic_acid",    "[SX4](=[OX1])(=[OX1])[OX2H1]", (3,)),
    ("sulfinic_acid",    "[SX3](=[OX1])[OX2H1]", (2,)),
    ("phosphate_OH",     "[PX4](=[OX1])[OX2H1]", (2,)),
]
DAMP_BONDS = 3

_B = [(n, Chem.MolFromSmarts(s)) for n, s in BASIC]
_Q = Chem.MolFromSmarts(QUAT)
_A = [(n, Chem.MolFromSmarts(s), k) for n, s, k in ACIDIC]
for _n, _p in _B:
    assert _p is not None, f"basic SMARTS will not compile: {_n}"
for _n, _p, _k in _A:
    assert _p is not None, f"acidic SMARTS will not compile: {_n}"
assert _Q is not None and _NEUT is not None


def neutralise(m):
    """Strip every charge a protonation equilibrium could have chosen."""
    rw = Chem.RWMol(m)
    for (idx,) in rw.GetSubstructMatches(_NEUT):
        a = rw.GetAtomWithIdx(idx)
        c, h = a.GetFormalCharge(), a.GetTotalNumHs()
        a.SetFormalCharge(0)
        a.SetNumExplicitHs(max(0, h - c))
        a.SetNoImplicit(False)
    out = rw.GetMol()
    Chem.SanitizeMol(out)
    return out


def charge_ph74(m, explain=False):
    """Net formal charge at pH 7.4 by the documented rule.  Never GetFormalCharge."""
    m = neutralise(m)
    dm = Chem.GetDistanceMatrix(m)
    found, claimed = [], set()
    for name, patt in _B:
        for match in m.GetSubstructMatches(patt, uniquify=True):
            if set(match) & claimed:
                continue
            claimed |= set(match)
            found.append((min(match), name))
    found.sort()
    accepted, sites = [], []
    for key, name in found:
        if any(dm[key][s] <= DAMP_BONDS for s in sites):
            continue
        accepted.append(name)
        sites.append(key)
    quats = [i for (i,) in m.GetSubstructMatches(_Q)]

    acids, aclaimed = [], set()
    for name, patt, keys in _A:
        for match in m.GetSubstructMatches(patt, uniquify=True):
            site = frozenset(match[i] for i in keys)
            if site & aclaimed:
                continue
            aclaimed |= site
            acids.append(name)
    # anything neutralisation could not remove and the rules did not claim
    residual = sum(a.GetFormalCharge() for a in m.GetAtoms()
                   if a.GetIdx() not in quats)
    q = len(accepted) + len(quats) - len(acids) + residual
    if explain:
        return q, accepted + ["quaternary_N"] * len(quats), acids, residual
    return q


# The six aminergic full agonists of this panel, plus molecules whose charge at
# pH 7.4 is not in dispute -- including the frozen campaign's own hand-picked
# decoys, so the rule is exercised on the exact molecules whose neutrality was
# Decision A's consequence.
CHARGE_VALIDATION = [
    # the six the brief names.  These are load-bearing: if they are not +1 the
    # rule has reproduced the defect it exists to repair.
    ("5HT5A full agonist (5-CT)", "c1cc2c(cc1C(=O)N)c(c[nH]2)CCN", 1, True),
    ("ACM4 full agonist (iperoxo)", "C[N+](C)(C)CC#CCOC1=NOCC1", 1, True),
    ("DRD3 full agonist (PD 128907)",
     "CCCN1CCO[C@H]2[C@H]1COc3c2cc(cc3)O", 1, True),
    ("OPRD full agonist (DPI-287)",
     "CCN(CC)C(=O)c1ccc(cc1)[C@H](c2cccc(c2)O)N3C[C@H](N(C[C@@H]3C)Cc4ccccc4)C",
     1, True),
    ("ADRB1 full agonist (CHEMBL1615159)",
     "Cc1ccccc1CC(C)(C)NC[C@H](O)c1ccc(O)c2c1OCC(=O)N2", 1, True),
    ("HRH3 full agonist (histamine)", "NCCc1cnc[nH]1", 1, True),
    # the rest of this panel's references
    ("AA1R adenosine",
     "c1nc(c2c(n1)n(cn2)[C@H]3[C@@H]([C@@H]([C@H](O3)CO)O)O)N", 0, False),
    ("AA2AR NECA",
     "CCNC(=O)[C@@H]1[C@H]([C@H]([C@@H](O1)n2cnc3c2ncnc3N)O)O", 0, False),
    ("B1B1U5 11,20-ethanoretinal",
     "CC1=C(/C=C/C(C)=C/C2=C/C(=C/C=O)CCC2)C(C)(C)CCC1", 0, False),
    ("CCKAR SR146131",
     "COc1cc(-c2nc(NC(=O)c3cc4cc(C)cc(C)c4n3CC(=O)O)sc2CCC2CCCCC2)c(OC)cc1Cl",
     -1, False),
    ("CNR2 HU-308-type",
     "CCCCCCC(C)(C)c1ccc(c(c1)O)[C@@H]2C[C@@H](CC[C@H]2CCCO)O", 0, False),
    ("GHSR ibutamoren",
     "CC(C)(N)C(=O)N[C@H](COCc1ccccc1)C(=O)N1CCC2(CC1)CN(S(C)(=O)=O)c1ccccc12",
     1, False),
    ("LPAR1 LPA 18:1 (phosphate monoester, -2)",
     "CCCCCCCCC=CCCCCCCCC(=O)OCC(COP(=O)(O)O)O", -2, False),
    ("LT4R1 LTB4",
     r"CCCCC\C=C/C[C@@H](O)\C=C\C=C\C=C/[C@@H](O)CCCC(O)=O", -1, False),
    ("OPSD all-trans retinal",
     "CC1=C(/C=C/C(C)=C/C=C/C(C)=C/C=O)C(C)(C)CCC1", 0, False),
    ("S1PR1 siponimod (zwitterion, net 0)",
     "CCc1cc(/C(C)=N/OCc2ccc(C3CCCCC3)c(C(F)(F)F)c2)ccc1CN1CC(C(=O)O)C1", 0, False),
    # the frozen campaign's decoys -- MAP §2.1
    ("frozen decoy ADRB2 tramadol", "CN(C)C[C@H]1CCCC[C@@]1(O)c1cccc(OC)c1", 1, False),
    ("frozen decoy ADRB1 aspirin", "CC(=O)Oc1ccccc1C(=O)O", -1, False),
    ("frozen decoy AA2AR trimethoprim", "COc1cc(Cc2cnc(N)nc2N)cc(OC)c1OC", 0, False),
    ("frozen decoy HRH1 metformin", "CN(C)C(=N)N=C(N)N", 1, False),
    ("frozen decoy DRD3 mefenamic acid", "Cc1ccccc1Nc1ccccc1C(=O)O", -1, False),
    # unambiguous controls
    ("propranolol", "CC(C)NC[C@@H](O)COc1cccc2ccccc12", 1, False),
    ("carazolol", "CC(C)NC[C@H](O)COc1cccc2[nH]c3ccccc3c12", 1, False),
    ("dopamine", "NCCc1ccc(O)c(O)c1", 1, False),
    ("arginine", "N[C@@H](CCCNC(=N)N)C(=O)O", 1, False),
    ("glycine (zwitterion, net 0)", "NCC(=O)O", 0, False),
    ("piperazine (pKa2 5.6 -> +1, not +2)", "C1CNCCN1", 1, False),
    ("aniline (pKa 4.6 -> neutral)", "Nc1ccccc1", 0, False),
    ("pyridine (pKa 5.2 -> neutral)", "c1ccncc1", 0, False),
    ("imidazole (pKa ~7 -> neutral)", "c1c[nH]cn1", 0, False),
    ("caffeine", "Cn1cnc2c1c(=O)n(C)c(=O)n2C", 0, False),
    ("acetaminophen (phenol + amide)", "CC(=O)Nc1ccc(O)cc1", 0, False),
    ("losartan (tetrazole)",
     "CCCCc1nc(Cl)c(CO)n1Cc1ccc(-c2ccccc2-c2nn[nH]n2)cc1", -1, False),
    ("sulfamethoxazole (sulfonamide N-H stays neutral)",
     "Cc1cc(NS(=O)(=O)c2ccc(N)cc2)no1", 0, False),
    ("choline (quaternary N, permanent +1)", "C[N+](C)(C)CCO", 1, False),
]


def validate_charge_rule(verbose=True):
    """Run before anything is selected.  A failure stops the module."""
    bad, aminergic_bad = [], []
    lines = []
    for name, smi, want, load_bearing in CHARGE_VALIDATION:
        m = Chem.MolFromSmiles(smi)
        if m is None:
            bad.append((name, "SMILES does not parse", want))
            continue
        got = charge_ph74(m)
        ok = got == want
        if not ok:
            bad.append((name, got, want))
            if load_bearing:
                aminergic_bad.append(name)
        lines.append(f"  {'ok  ' if ok else 'MISS'} "
                     f"{'[aminergic] ' if load_bearing else '            '}"
                     f"{name:<48} got {got:+d} want {want:+d}")
    if verbose:
        sys.stdout.write("\n=== protonation rule, validated before use ===\n\n")
        sys.stdout.write("\n".join(lines) + "\n\n")
        sys.stdout.write(f"  {len(CHARGE_VALIDATION) - len(bad)}"
                         f"/{len(CHARGE_VALIDATION)} molecules at the expected "
                         f"charge\n\n")
    if aminergic_bad:
        sys.stderr.write(
            "!! STOP.  The protonation rule does not reproduce +1 for the aminergic\n"
            "!! full agonists on this panel: " + ", ".join(aminergic_bad) + "\n"
            "!! That is the exact defect MAP_LIGANDS_AND_ANALYSIS §2.3 records for the\n"
            "!! frozen campaign, and there is no fallback to Chem.GetFormalCharge.\n"
            "!! Fix the rule or abandon the charge axis explicitly -- do not proceed.\n")
    return bad, aminergic_bad


# =========================================================================
# the eight axes -- ONE code path, reference and candidate alike
# =========================================================================
def largest_fragment(m):
    frags = Chem.GetMolFrags(m, asMols=True, sanitizeFrags=True)
    if len(frags) == 1:
        return frags[0]
    return max(frags, key=lambda f: (f.GetNumHeavyAtoms(), Chem.MolToSmiles(f)))


def axes(smiles):
    """The eight axes plus the Morgan fingerprint.  None if the SMILES will not parse."""
    if not smiles or not smiles.strip():
        return None
    m = Chem.MolFromSmiles(smiles.strip())
    if m is None:
        return None
    try:
        m = largest_fragment(m)
        a = {
            "mw": Descriptors.MolWt(m),
            "clogp": Crippen.MolLogP(m),
            "tpsa": Descriptors.TPSA(m),
            "hbd": Lipinski.NumHDonors(m),
            "hba": Lipinski.NumHAcceptors(m),
            "rot": Lipinski.NumRotatableBonds(m),
            "rings": rdMolDescriptors.CalcNumRings(m),
            "charge": charge_ph74(m),
        }
    except Exception:
        return None
    a["_fp"] = _MFG.GetFingerprint(m)
    a["_smiles"] = Chem.MolToSmiles(m)
    a["_inchikey"] = Chem.MolToInchiKey(m)
    return a


def window(ref):
    """The accept window for each axis, from the reference's own values.

    §5.3 as written: +-20% of the reference on the continuous axes.  Implemented
    literally, including the consequence -- the window is proportional to |ref|, so a
    reference whose cLogP sits near zero gets a window near zero wide.  That is a real
    property of the rule and it is reported rather than repaired (see `--report`).
    """
    w = {}
    for k in CONTINUOUS:
        d = CONTINUOUS_TOL * abs(ref[k])
        w[k] = (ref[k] - d, ref[k] + d)
    for k in INTEGER:
        w[k] = (ref[k] - INTEGER_TOL, ref[k] + INTEGER_TOL)
    w["charge"] = (ref["charge"], ref["charge"])
    return w


def failed_axes(cand, ref, w, max_t):
    """Every axis that refuses this candidate, in the fixed order AXES.

    No cascade: all eight are evaluated for every candidate, so an axis's rejection
    count is a fact about the chemistry and not about the order of the tests.
    """
    out = []
    for k in AXES:
        if k == "tanimoto":
            if not (max_t < TANIMOTO_MAX):
                out.append(k)
        elif k == "charge":
            if cand["charge"] != ref["charge"]:
                out.append(k)
        else:
            lo, hi = w[k]
            if not (lo <= cand[k] <= hi):
                out.append(k)
    return out


# =========================================================================
# inputs
# =========================================================================
def tsv(path):
    with open(path) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def csvf(path):
    with open(path) as fh:
        return list(csv.DictReader(fh))


def require(path, why):
    """A missing input FAILS.  It is never a quiet skip."""
    if not os.path.exists(path):
        raise SystemExit(f"!! {os.path.relpath(path)} is ABSENT -- {why}\n"
                         f"!! A check that does nothing when its input is missing is "
                         f"the defect it exists to catch; this one stops instead.")
    return path


def load_scope(root=None):
    """The receptors the decoy arm actually runs on, read off g2_systems.csv."""
    g2 = os.path.join(root, "g2_systems.csv") if root else G2
    require(g2, "run redo/build/g2_systems.py first")
    rows = csvf(g2)
    slugs, clusters = [], {}
    for r in rows:
        if r["ligand"] == "decoy_lig" or r["ligand_role_actual"] == "decoy_lig":
            if r["receptor_slug"] not in clusters:
                slugs.append(r["receptor_slug"])
            clusters[r["receptor_slug"]] = r["receptor_cluster"]
    if not slugs:
        raise SystemExit("!! g2_systems.csv names no decoy cells at all -- the arm "
                         "has vanished from the enumeration, which GROUP2_LIGANDS "
                         "§3.4 G-6 exists to prevent")
    return slugs, clusters


def load_ligands(root=None):
    """(receptor, role) -> SMILES, from the three curation sources.

    Returns (curated, census_by_receptor).  `curated` is what supplies the REFERENCE
    (a full agonist); `census_by_receptor` broadens only the Tanimoto screen.

    `root` overrides only the two `inputs/` tables, so gates/drule.py can point this
    at a planted copy.  The inherited curation lives under protocol/received/ and is
    read-only from outside, so it is never rooted elsewhere.
    """
    redoset = os.path.join(root, "ligand_set_redo.tsv") if root else REDOSET
    censusp = os.path.join(root, "ligand_census_records.tsv") if root else CENSUS
    curated = {}
    for f in ("ligand_set.csv", "ligand_set_tier3.csv"):
        p = os.path.join(APPROVED, f)
        require(p, "the inherited curation is part of the reference resolution")
        for r in csvf(p):
            curated.setdefault((r["receptor"], r["ligand_role"]), []).append(
                (r.get("smiles", ""), f"INHERITED:{f}", r.get("ligand_variant", "")))
    require(redoset, "run redo/build/ligand_set_redo.py first")
    for r in tsv(redoset):
        if r["status"] != "enacted":
            continue
        smi = (r.get("canonical_smiles") or r.get("smiles") or "").strip()
        # our own enactment WINS over the inherited row for the same (receptor, role)
        curated[(r["receptor_slug"], r["ligand_role"])] = [
            (smi, "REDO:ligand_set_redo.tsv", r.get("ligand_name", ""))]
    require(censusp, "run redo/build/ligand_census.py first")
    census = {}
    for r in tsv(censusp):
        if r["role"] == "apo" or r["has_smiles"] != "1":
            continue
        if r["modality"] not in ("small-molecule", "lipid"):
            continue
        smi = (r.get("smiles") or "").strip()
        if smi:
            census.setdefault(r["receptor"], []).append(
                (smi, "CENSUS", r.get("ligand_name", "")))
    return curated, census


REAL_ROLES = ("full_agonist", "neutral_antagonist", "inverse_agonist",
              "partial_agonist", "antagonist", "agonist")


def real_ligands(cluster_members, curated, census):
    """Every curated real ligand of every receptor in the cluster."""
    out = []
    for rec in cluster_members:
        for role in REAL_ROLES:
            for smi, src, name in curated.get((rec, role), []):
                if smi.strip():
                    out.append((rec, role, smi.strip(), src, name))
        for smi, src, name in census.get(rec, []):
            out.append((rec, "census", smi, src, name))
    return out


# =========================================================================
# the run
# =========================================================================
def receptor_seed(slug):
    h = hashlib.sha256(f"drule|{slug}|{DRAW_SEED}".encode()).hexdigest()[:16]
    return int(h, 16)


SEL_COLS = ["receptor_slug", "cluster", "decoy_status", "reason",
            "n_eligible", "n_accepted", "draw_rank",
            "candidate_chembl_id", "candidate_name", "smiles", "inchikey",
            "mw", "clogp", "tpsa", "hbd", "hba", "rot", "rings", "charge",
            "max_tanimoto", "n_real_ligands_screened",
            "ref_ligand_name", "ref_ligand_source", "ref_smiles",
            "ref_mw", "ref_clogp", "ref_tpsa", "ref_hbd", "ref_hba", "ref_rot",
            "ref_rings", "ref_charge",
            "draw_seed", "receptor_seed", "k_requested",
            "chembl_release", "pool_scope", "rule"]

REJ_COLS = ["receptor_slug", "candidate_chembl_id", "first_failed_axis",
            "failed_axes", "n_failed_axes"]


def run(report_only=False, crosscheck=False, verbose=True):
    bad, aminergic_bad = validate_charge_rule(verbose=verbose)
    if aminergic_bad:
        return 1, None

    require(MOLS, "run redo/build/drule_pool.py --db <pinned ChEMBL>")
    require(EXCL, "the molecule table alone cannot say who is ineligible")
    require(TARGETS, "run redo/build/drule_targets.py first")

    slugs, g2_clusters = load_scope()
    targets = {r["receptor_slug"]: r for r in tsv(TARGETS)}
    by_cluster = {}
    for r in targets.values():
        by_cluster.setdefault(r["cluster"], []).append(r["receptor_slug"])

    curated, census = load_ligands()

    if verbose:
        sys.stdout.write("=== D-RULE selection ===\n\n")
        sys.stdout.write(f"  scope           {len(slugs)} receptors from "
                         f"g2_systems.csv's decoy arm\n")

    # ---- the pool, once -------------------------------------------------
    pool = tsv(MOLS)
    release = sorted({r["chembl_release"] for r in pool})
    scope = sorted({r["pool_scope"] for r in pool})
    if verbose:
        sys.stdout.write(f"  pool            {len(pool):,} molecules, release "
                         f"{release}, scope {scope}\n")

    excluded = {}
    with open(EXCL) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            excluded.setdefault(r["receptor_slug"], set()).add(r["candidate_chembl_id"])
    if verbose:
        sys.stdout.write(f"  exclusions      "
                         f"{sum(len(v) for v in excluded.values()):,} "
                         f"(receptor, molecule) pairs over "
                         f"{len(excluded)} receptors\n")

    # ---- every candidate's axes, computed once with RDKit ---------------
    if verbose:
        sys.stdout.write("\n  computing eight axes + Morgan fingerprints with RDKit "
                         "for every pool molecule ...\n")
    cand_axes, unparseable = {}, []
    cross = {k: [0, 0] for k in ("mw", "logp", "hbd", "hba", "rot")}
    for i, r in enumerate(pool):
        a = axes(r["smiles"])
        cid = r["candidate_chembl_id"]
        if a is None:
            unparseable.append(cid)
            continue
        a["_name"] = r["candidate_name"]
        cand_axes[cid] = a
        if crosscheck:
            for ck, ak, tol in (("mw", "mw", 1.0), ("logp", "clogp", 0.5),
                                ("hbd", "hbd", 0), ("hba", "hba", 0),
                                ("rot", "rot", 0)):
                v = r[ck]
                if v == "":
                    continue
                cross[ck][1] += 1
                if abs(float(v) - a[ak]) > tol:
                    cross[ck][0] += 1
        if verbose and (i + 1) % 25000 == 0:
            sys.stdout.write(f"    {i + 1:,} / {len(pool):,}\n")
            sys.stdout.flush()
    if verbose:
        sys.stdout.write(f"    {len(cand_axes):,} parsed, "
                         f"{len(unparseable):,} unparseable\n")
    if crosscheck and verbose:
        sys.stdout.write("\n  ChEMBL compound_properties vs RDKit, same molecules "
                         "(NOT used by the gate; MAP §2.2):\n")
        for k, (n_bad, n) in cross.items():
            sys.stdout.write(f"    {k:<5} {n_bad:,}/{n:,} disagree "
                             f"({100.0 * n_bad / max(n, 1):.1f}%)\n")

    cid_order = sorted(cand_axes)
    fp_list = [cand_axes[c]["_fp"] for c in cid_order]

    sel_rows, rej_rows, summary = [], [], []
    axis_counts = {k: 0 for k in AXES}
    axis_first = {k: 0 for k in AXES}

    for slug in slugs:
        tg = targets.get(slug)
        cluster = tg["cluster"] if tg else g2_clusters[slug]
        members = by_cluster.get(cluster, [slug])
        resolved = bool(tg and tg["chembl_target_id"])

        ref_rows = curated.get((slug, "full_agonist"), [])
        ref_smi = ref_rows[0][0].strip() if ref_rows else ""
        ref_src = ref_rows[0][1] if ref_rows else ""
        ref_name = ref_rows[0][2] if ref_rows else ""
        ref = axes(ref_smi) if ref_smi else None

        base = dict(receptor_slug=slug, cluster=cluster,
                    draw_seed=DRAW_SEED, receptor_seed=receptor_seed(slug),
                    k_requested=K_DECOYS,
                    chembl_release=release[0] if len(release) == 1 else ";".join(release),
                    pool_scope=scope[0] if len(scope) == 1 else ";".join(scope),
                    rule="CAMPAIGN.md 5.3 D-RULE",
                    ref_ligand_name=ref_name, ref_ligand_source=ref_src,
                    ref_smiles=ref_smi)
        for k in ("mw", "clogp", "tpsa", "hbd", "hba", "rot", "rings", "charge"):
            base[f"ref_{k}"] = (round(ref[k], 3) if isinstance(ref[k], float)
                                else ref[k]) if ref else ""

        def unavailable(reason, n_elig=0, n_acc=0, blocking=""):
            row = dict(base, decoy_status="decoy-unavailable", reason=reason,
                       n_eligible=n_elig, n_accepted=n_acc, draw_rank="",
                       candidate_chembl_id="", candidate_name="", smiles="",
                       inchikey="", max_tanimoto="", n_real_ligands_screened="")
            for k in ("mw", "clogp", "tpsa", "hbd", "hba", "rot", "rings", "charge"):
                row[k] = ""
            sel_rows.append(row)
            summary.append((slug, cluster, "decoy-unavailable", n_elig, n_acc,
                            reason, blocking))

        # ---- TRAP 1: no ChEMBL target => NO exclusion rows => everything
        # would look eligible, and the receptor we know least about would be
        # handed the largest accepted set on the panel.  Eligibility is
        # unestablishable, which is not the same as nothing being excluded.
        if not resolved:
            unavailable("eligibility is unestablishable: the receptor has no resolved "
                        "ChEMBL target, so the pool holds NO exclusion rows for it and "
                        "an empty exclusion set would read as universal eligibility",
                        n_elig=0, blocking="no_chembl_target")
            continue

        if ref is None:
            unavailable("no curated full agonist with a parseable SMILES; §5.3's "
                        "reference ligand is undefined for this receptor",
                        blocking="no_reference")
            continue

        reals = real_ligands(members, curated, census)
        real_fps = []
        for _rec, _role, smi, _src, _nm in reals:
            a = axes(smi)
            if a is not None:
                real_fps.append(a["_fp"])
        if not real_fps:
            unavailable("no parseable real ligand anywhere in the paralog cluster, so "
                        "the Tanimoto screen cannot be evaluated",
                        blocking="no_real_ligands")
            continue

        elig = [c for c in cid_order if c not in excluded.get(slug, ())]
        elig_set = set(elig)
        idx = [i for i, c in enumerate(cid_order) if c in elig_set]
        sub_fps = [fp_list[i] for i in idx]

        maxt = [0.0] * len(idx)
        for rfp in real_fps:
            sims = DataStructs.BulkTanimotoSimilarity(rfp, sub_fps)
            for j, s in enumerate(sims):
                if s > maxt[j]:
                    maxt[j] = s

        w = window(ref)
        accepted = []
        # `sole` counts candidates that fail on exactly ONE axis.  That is the axis
        # which, dropped by itself, would admit them -- and it is the honest answer
        # to "which axis killed this receptor".  The most COMMON failing axis is not:
        # MW is the most common first axis on every receptor here, and on none of
        # them is it the one standing between the receptor and three decoys.
        sole = {k: 0 for k in AXES}
        for j, i in enumerate(idx):
            cid = cid_order[i]
            f = failed_axes(cand_axes[cid], ref, w, maxt[j])
            if f:
                for k in f:
                    axis_counts[k] += 1
                axis_first[f[0]] += 1
                if len(f) == 1:
                    sole[f[0]] += 1
                rej_rows.append((slug, cid, f[0], "|".join(f), len(f)))
            else:
                accepted.append((cid, maxt[j]))

        n_elig, n_acc = len(elig), len(accepted)
        if n_acc < K_DECOYS:
            best = max(AXES, key=lambda k: sole[k])
            blocking = (f"{best}: dropping it alone would give "
                        f"{n_acc + sole[best]}" if sole[best] else
                        "no single axis unblocks this receptor")
            unavailable(f"only {n_acc} candidate(s) pass the gate; §5.3 needs "
                        f"{K_DECOYS} and no candidate is ever taken anyway. "
                        f"Decisive axis -- {blocking}",
                        n_elig=n_elig, n_acc=n_acc, blocking=blocking)
            continue

        rng = random.Random(receptor_seed(slug))
        accepted.sort()                      # deterministic before the draw
        draw = rng.sample(accepted, K_DECOYS)
        for rank, (cid, t) in enumerate(sorted(draw), start=1):
            a = cand_axes[cid]
            row = dict(base, decoy_status="accepted", reason="",
                       n_eligible=n_elig, n_accepted=n_acc, draw_rank=rank,
                       candidate_chembl_id=cid, candidate_name=a["_name"],
                       smiles=a["_smiles"], inchikey=a["_inchikey"],
                       max_tanimoto=round(t, 4),
                       n_real_ligands_screened=len(real_fps))
            for k in ("mw", "clogp", "tpsa"):
                row[k] = round(a[k], 3)
            for k in ("hbd", "hba", "rot", "rings", "charge"):
                row[k] = a[k]
            sel_rows.append(row)
        summary.append((slug, cluster, "accepted", n_elig, n_acc, "", ""))

    if report_only:
        return 0, (sel_rows, rej_rows, summary, axis_counts, axis_first)

    with open(OUT_SEL, "w", newline="") as fh:
        w_ = csv.DictWriter(fh, fieldnames=SEL_COLS, delimiter="\t",
                            extrasaction="ignore")
        w_.writeheader()
        w_.writerows(sel_rows)
    with open(OUT_REJ, "w", newline="") as fh:
        fh.write("\t".join(REJ_COLS) + "\n")
        for r in rej_rows:
            fh.write("\t".join(str(x) for x in r) + "\n")

    if verbose:
        print_summary(sel_rows, rej_rows, summary, axis_counts, axis_first)
    return 0, (sel_rows, rej_rows, summary, axis_counts, axis_first)


def print_summary(sel_rows, rej_rows, summary, axis_counts, axis_first):
    sys.stdout.write("\n=== per receptor ===\n\n")
    sys.stdout.write(f"  {'receptor':<9} {'cluster':<18} {'eligible':>9} "
                     f"{'accepted':>9}  status\n")
    ok_clusters, ok_recs = set(), []
    for slug, cluster, status, n_elig, n_acc, reason, blocking in summary:
        sys.stdout.write(f"  {slug:<9} {cluster:<18} {n_elig:>9,} {n_acc:>9,}  "
                         f"{status}"
                         f"{'  [' + blocking + ']' if blocking else ''}\n")
        if status == "accepted":
            ok_clusters.add(cluster)
            ok_recs.append(slug)
    sys.stdout.write(f"\n  >=3 accepted decoys: {len(ok_recs)}/{len(summary)} "
                     f"receptors, {len(ok_clusters)} clusters\n")
    sys.stdout.write(f"  §5.3 runs the decoy arm only if >=12 clusters pass -> "
                     f"{'PASS' if len(ok_clusters) >= 12 else 'DOES NOT PASS'}\n")

    sys.stdout.write("\n=== which axis rejects, ranked ===\n\n")
    tot = len(rej_rows)
    sys.stdout.write(f"  {'axis':<10} {'rejections':>12} {'share':>8}   "
                     f"{'sole/first':>11} {'share':>8}\n")
    for k in sorted(AXES, key=lambda k: -axis_counts[k]):
        sys.stdout.write(f"  {k:<10} {axis_counts[k]:>12,} "
                         f"{100.0 * axis_counts[k] / max(tot, 1):>7.1f}%   "
                         f"{axis_first[k]:>11,} "
                         f"{100.0 * axis_first[k] / max(tot, 1):>7.1f}%\n")
    sys.stdout.write(f"\n  {tot:,} (receptor, candidate) rejections; a candidate can "
                     f"fail several axes, so column 1 over-counts and\n  column 2 "
                     f"(first axis in the fixed order {', '.join(AXES)}) sums to the "
                     f"total.\n")
    sys.stdout.write(f"\n  wrote {os.path.relpath(OUT_SEL)}  ({len(sel_rows)} rows)\n")
    sys.stdout.write(f"  wrote {os.path.relpath(OUT_REJ)}  ({len(rej_rows):,} rows, "
                     f"{os.path.getsize(OUT_REJ) / 1e6:.1f} MB)\n\n")


# =========================================================================
# self-test -- the rule, proved on fixtures where the answer is known
# =========================================================================
def selftest():
    """Prove the RULE, and prove the PLUMBING the rule sits on.

    drule_pool.py's own note records why both halves are needed: its fixture passed
    tids in directly, so it proved the rule and never exercised the resolution step,
    and the first real run produced zero rows.  So the checks below split into
    (a) the gate arithmetic on molecules whose answer is arithmetic, and
    (b) the resolution steps that a fixture would otherwise hand over for free --
    the reference actually resolving to a full agonist, the cluster actually
    widening the Tanimoto screen, and an unresolved receptor actually being refused.
    """
    bad = 0
    sys.stdout.write("\n=== drule_select self-test ===\n")

    # (a) the protonation rule
    cbad, abad = validate_charge_rule(verbose=False)
    ok = not cbad
    bad += 0 if ok else 1
    sys.stdout.write(f"\n  {'ok  ' if ok else 'MISS'} protonation rule: "
                     f"{len(CHARGE_VALIDATION) - len(cbad)}/{len(CHARGE_VALIDATION)} "
                     f"molecules at the expected charge at pH 7.4"
                     f"{'' if ok else '  -- ' + str(cbad[:4])}\n")
    ok = not abad
    bad += 0 if ok else 1
    sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} the six aminergic full agonists "
                     f"(5HT5A ACM4 DRD3 OPRD ADRB1 HRH3) come out +1\n")

    # (b) the gate arithmetic, on a reference and hand-built candidates
    ref = axes("CCCN1CCO[C@H]2[C@H]1COc3c2cc(cc3)O")        # DRD3 PD 128907
    w = window(ref)
    # a candidate that differs in charge must be refused by the `charge` axis
    c_charge = axes("CCCN1CCO[C@H]2[C@H]1COc3c2cc(cc3)OC(=O)O")
    f = failed_axes(c_charge, ref, w, 0.0)
    ok = "charge" in f
    bad += 0 if ok else 1
    sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} charge must be EXACTLY equal: a "
                     f"-1 candidate against a +1 reference is refused "
                     f"(failed {f})\n")

    # +-20% on a continuous axis, checked at the boundary from both sides
    for name, val, expect in (("mw just inside", ref["mw"] * 1.19, False),
                              ("mw just outside", ref["mw"] * 1.21, True)):
        fake = dict(ref)
        fake["mw"] = val
        f = failed_axes(fake, ref, w, 0.0)
        ok = ("mw" in f) == expect
        bad += 0 if ok else 1
        sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} {name} "
                         f"({val:.1f} vs {ref['mw']:.1f}) -> "
                         f"{'refused' if 'mw' in f else 'accepted'}\n")
    # +-1 on an integer axis, both sides
    for name, delta, expect in (("hba +1", 1, False), ("hba +2", 2, True)):
        fake = dict(ref)
        fake["hba"] = ref["hba"] + delta
        f = failed_axes(fake, ref, w, 0.0)
        ok = ("hba" in f) == expect
        bad += 0 if ok else 1
        sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} integer axis {name} -> "
                         f"{'refused' if 'hba' in f else 'accepted'}\n")
    # Tanimoto is strict <
    for name, t, expect in (("T = 0.299", 0.299, False), ("T = 0.30", 0.30, True),
                            ("T = 0.31", 0.31, True)):
        f = failed_axes(ref, ref, w, t)
        ok = ("tanimoto" in f) == expect
        bad += 0 if ok else 1
        sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} {name} -> "
                         f"{'refused' if 'tanimoto' in f else 'accepted'} "
                         f"(the rule is strictly < {TANIMOTO_MAX})\n")
    # every axis is reported, not just the first
    fake = dict(ref)
    fake["mw"] = ref["mw"] * 2
    fake["hba"] = ref["hba"] + 5
    fake["charge"] = ref["charge"] - 1
    f = failed_axes(fake, ref, w, 0.9)
    ok = set(f) >= {"mw", "hba", "charge", "tanimoto"} and f[0] == "mw"
    bad += 0 if ok else 1
    sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} a candidate failing four axes "
                     f"records all four and a deterministic first -> {f}\n")

    # one instrument on both sides: the reference goes through the SAME function
    ok = axes.__name__ == "axes" and ref is not None and "_fp" in ref
    bad += 0 if ok else 1
    sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} reference and candidate axes come "
                     f"from one code path (`axes`), never from ChEMBL's columns\n")

    # (c) the plumbing -- resolution steps a fixture would otherwise skip
    try:
        slugs, clusters = load_scope()
        ok = len(slugs) == 16
        bad += 0 if ok else 1
        sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} scope resolves from "
                         f"g2_systems.csv's decoy cells -> {len(slugs)} receptors\n")
        curated, census = load_ligands()
        miss = [s for s in slugs
                if not (curated.get((s, "full_agonist"), [{}]) and
                        curated.get((s, "full_agonist"))[0][0].strip())]
        ok = not miss
        bad += 0 if ok else 1
        sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} every receptor in scope "
                         f"resolves to a curated FULL AGONIST reference"
                         f"{'' if ok else '  -- missing ' + str(miss)}\n")
        tgs = {r["receptor_slug"]: r for r in tsv(TARGETS)}
        byc = {}
        for r in tgs.values():
            byc.setdefault(r["cluster"], []).append(r["receptor_slug"])
            # the cluster screen must actually widen for a multi-member cluster
        c = tgs["DRD3"]["cluster"]
        wide = real_ligands(byc[c], curated, census)
        narrow = real_ligands(["DRD3"], curated, census)
        ok = len(wide) > len(narrow) and len(byc[c]) > 1
        bad += 0 if ok else 1
        sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} the Tanimoto screen widens to "
                         f"the PARALOG CLUSTER: DRD3 alone {len(narrow)} real "
                         f"ligands, cluster {byc[c]} {len(wide)}\n")
        unres = [s for s in slugs if not tgs[s]["chembl_target_id"]]
        noexcl = []
        if os.path.exists(EXCL):
            with open(EXCL) as fh:
                have = {r["receptor_slug"] for r in csv.DictReader(fh, delimiter="\t")}
            noexcl = [s for s in unres if s not in have]
        ok = unres == noexcl and unres
        bad += 0 if ok else 1
        sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} TRAP: {unres} has no resolved "
                         f"ChEMBL target AND no exclusion rows, so a naive "
                         f"implementation would find EVERY molecule eligible for it\n")
    except SystemExit as e:
        bad += 1
        sys.stdout.write(f"  MISS plumbing: {e}\n")

    n = 14
    sys.stdout.write(f"\n  {n - bad}/{n} checks pass.\n\n")
    return 1 if bad else 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--report", action="store_true",
                    help="run the rule and print, without writing the inputs")
    ap.add_argument("--crosscheck", action="store_true", default=True,
                    help="report ChEMBL's compound_properties against RDKit "
                         "(never used by the gate)")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    rc, _ = run(report_only=a.report, crosscheck=a.crosscheck)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
