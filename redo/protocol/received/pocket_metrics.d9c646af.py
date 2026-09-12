"""Pocket-anchored geometry — Block C Gate 0.1 (plan §2.1).

Adds four BW-anchored metrics on top of the existing transmission-side
axes (NPxxY, TM6 tilt, RMSD). Every prior axis measures the receptor
~30 Å from the ligand; these four measure the orthosteric pocket where
the ligand actually sits.

The four metrics:

    pocket_ca_rmsd         — Cα RMSD over 12 BW positions:
                             3.32, 3.33, 3.36, 5.42, 5.43, 5.46,
                             6.48, 6.51, 6.52, 6.55, 7.39, 7.42
                             after 7TM-CA Kabsch alignment to the
                             role-matched reference (active for
                             Ga-coupled-active / arrestin-coupled;
                             inactive for antagonist / inverse-agonist).
    pocket_sidechain_rmsd  — Same 12 residues, sidechain heavy atoms only
                             (element != H; atom name not in
                             {N, CA, C, O}). Same alignment transform.
    w648_chi1              — W6.48 χ1 dihedral N-Cα-Cβ-Cγ (degrees).
                             The classic toggle-switch rotamer.
    ligand_rmsd_to_ref     — Ligand heavy-atom RMSD to the reference
                             crystal ligand after receptor 7TM Kabsch,
                             matched by atom name + element (bond-graph
                             free — matches the DUD-E-style comparison).

Class-conditional posture (see ``compute_pocket_axes_bundle`` docstring):

  Class A: all four metrics run.
  Class B: pocket_ca_rmsd, pocket_sidechain_rmsd, w648_chi1 → NaN + note
           (pocket residue set for the peptide-binding cavity has not
           been curated yet; see docs). ligand_rmsd_to_ref DOES run —
           the 7TM Kabsch is class-agnostic and GLP1R + peptide agonist
           reference yields a real number.
  Class F: same posture as Class B.

Ligand-alignment method (Ambiguity #2, approved 2026-09-03):

  1. Kabsch on receptor 7TM CA (GPCRdb-annotated TM1..TM7) — same
     residue-selection rule as ``scripts/rescore_rmsd.py``.
  2. Apply that transform to the prediction ligand heavy atoms.
  3. Match reference ligand atoms by (atom_name, element) exactly; if
     the ligand identity differs between reference and prediction the
     comparison is undefined and returns NaN + note.

**Consumers of ``ligand_rmsd_to_ref`` MUST filter decoy_lig rows via
the manifest / spec.** The scorer does not have a decoy flag on the
row and will happily compute a pose distance between a decoy ligand
and a real-ligand reference — that number is meaningless. This is
Ambiguity #4 (approved 2026-09-03) and is the documented posture; the
analysis layer owns the filter.

**Class B / F pocket residue definition** — the 12-position Class A
pocket set does NOT transfer to Class B receptors, whose orthosteric
site is a peptide-binding cavity with different residue geometry. The
Block C plan defers a Class B pocket definition to a follow-up; every
Class B receptor here emits NaN + ``class_B_pocket_deferred`` in
``pocket_notes``. See ``experiments/020_block_c_ligand_pharmacology/
analysis/scorer_extension_notes.md`` "Follow-up".
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Optional

import gemmi

from scorer.schema import StateClaim
from scorer.structure import STD_AA, one_letter
from scorer.verified import VerifiedModel


NaN = float("nan")


# ---------------------------------------------------------------------------
# BW anchor list
# ---------------------------------------------------------------------------

POCKET_BW_LABELS: tuple[str, ...] = (
    "3.32", "3.33", "3.36",
    "5.42", "5.43", "5.46",
    "6.48", "6.51", "6.52", "6.55",
    "7.39", "7.42",
)

# The toggle-switch tryptophan (Class A).
W648_BW: str = "6.48"

# Minimum residue count required to compute a meaningful pocket RMSD.
# Below this floor the metric is not reported (NaN + note). Six of twelve
# = 50 % — matches the spirit of the RMSD floor in scripts/rescore_rmsd.py
# (which required ≥20 residues over the whole 7TM).
MIN_POCKET_RESIDUES: int = 6

# Minimum 7TM CA count for a defensible Kabsch. rescore_rmsd.py uses 20.
MIN_KABSCH_CA: int = 20

# Backbone atom names excluded from sidechain RMSD.
_BACKBONE_ATOMS: frozenset[str] = frozenset({"N", "CA", "C", "O"})

# TM segment labels the 7TM Kabsch is built from.
_TM_SEGMENTS: frozenset[str] = frozenset({"TM1", "TM2", "TM3", "TM4", "TM5", "TM6", "TM7"})

# Ligand-code prefixes that are NOT real ligands (crystallographic /
# cryo-buffer entities). Filtered when scanning HETATM chains for the
# reference ligand. Water is already handled by residue name.
#
# Public alias ``NON_LIGAND_RESNAMES`` below re-exports this set so
# ``scorer/post_run_receipts.py`` (Block C Stage 0 Step 1.4, 2026-09-04)
# can share the same vetted exclusion list without a leading-underscore
# import. Underscore alias retained for back-compat with existing
# in-module references.
_NON_LIGAND_RESNAMES: frozenset[str] = frozenset({
    "HOH", "WAT", "DOD",                    # waters
    "NA", "K", "MG", "CA", "ZN", "MN", "FE",  # metals
    "CL", "BR", "IOD", "F",                 # halides
    "SO4", "PO4", "PEG", "GOL", "EDO",      # buffer / cryo
    "TRS", "BOG", "BME", "MPD", "DMS",
    "OLC", "OLA", "OLB", "PLM", "CLR",      # lipids commonly in GPCR structures
    "CHS", "CHD", "CLA", "PGV", "LMT",
    "STE", "PC1", "PEE", "LFA", "MPG",
    "PGE", "1PE", "P6G",                    # PEG oligomers
    "ACT", "FMT", "IPA",                    # small ions / additives
})

# Public re-export — see docstring above _NON_LIGAND_RESNAMES. Same object;
# importers should prefer this name over the leading-underscore variant.
NON_LIGAND_RESNAMES: frozenset[str] = _NON_LIGAND_RESNAMES


# ---------------------------------------------------------------------------
# PocketReferenceCache
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PocketReferenceCache:
    """One (receptor, role) reference PDB's pocket-relevant state.

    Prepared once per receptor+role at load time in the orchestrator's
    module-level cache (see scorer/orchestrator.py). The orchestrator
    passes this dataclass to ``compute_pocket_axes_bundle`` on every
    scored row, avoiding re-loads.

    Fields:

    ``pdb_id`` — provenance.
    ``ca_by_uniprot`` — {uniprot_pos: gemmi.Position} for every observed
        CA on the receptor chain of the reference PDB, renumbered to
        UniProt via the same ``build_uniprot_model`` path the scoring
        code uses.
    ``residues_by_uniprot`` — {uniprot_pos: gemmi.Residue} for the same
        residues (needed for the sidechain RMSD atom extraction).
    ``ligand_atoms_positions`` — list of gemmi.Position for every heavy
        atom of the reference ligand (empty list if no ligand present).
    ``ligand_atom_names`` — atom names in matching order.
    ``ligand_atom_elements`` — element strings in matching order.
    ``ligand_resname`` — the reference ligand's residue-code (e.g. "P0G")
        or "" if none. Kept for provenance / debug.
    """
    pdb_id: str = ""
    ca_by_uniprot: dict[int, gemmi.Position] = field(default_factory=dict)
    residues_by_uniprot: dict[int, gemmi.Residue] = field(default_factory=dict)
    ligand_atoms_positions: list[gemmi.Position] = field(default_factory=list)
    ligand_atom_names: list[str] = field(default_factory=list)
    ligand_atom_elements: list[str] = field(default_factory=list)
    ligand_resname: str = ""
    # Provenance SHA of the PDB file this cache was built from. Stamped
    # by ``build_pocket_reference_cache`` (Post-Audit Stage 2,
    # 2026-09-05) so ``compute_pocket_axes_bundle`` can emit the SHA on
    # each scored row's ``pocket_ref_pdb_sha_active`` /
    # ``pocket_ref_pdb_sha_inactive`` companion columns. Empty when the
    # cache was built without hashing (test fixtures) — downstream
    # readers treat that as "provenance not recorded".
    provenance_sha256: str = ""


# ---------------------------------------------------------------------------
# Kabsch helper
# ---------------------------------------------------------------------------


def _superpose_transform(
    pred_pts: list[gemmi.Position],
    ref_pts: list[gemmi.Position],
) -> Optional[gemmi.SupResult]:
    """Kabsch pred → ref. Returns the SupResult (which carries both
    the RMSD and the transform), or None on any degenerate input.

    gemmi's Kabsch API: ``gemmi.superpose_positions(target, mobile)``
    returns a ``SupResult`` with ``.transform`` mapping mobile → target
    and ``.rmsd`` the RMSD after transform. Mirrors the convention in
    ``scripts/rescore_rmsd.py::_superpose_rmsd``.
    """
    if len(pred_pts) != len(ref_pts) or len(pred_pts) < MIN_KABSCH_CA:
        return None
    try:
        return gemmi.superpose_positions(ref_pts, pred_pts)
    except Exception:
        return None


def _apply_transform(transform: gemmi.Transform, pos: gemmi.Position) -> gemmi.Position:
    """Apply a gemmi.Transform to a Position, returning a new Position.

    gemmi.Transform's ``.apply(Vec3)`` operates on Vec3; a Position IS
    a Vec3 in gemmi's linear algebra layer, so ``.apply(pos)`` works
    directly and returns a Vec3 that Position accepts via cons.
    """
    v = transform.apply(pos)
    return gemmi.Position(v.x, v.y, v.z)


# ---------------------------------------------------------------------------
# Class handling
# ---------------------------------------------------------------------------


def _is_pocket_supported_class(receptor_class: str) -> bool:
    """The Class A pocket residue set applies to Class A only. Class B/F
    receptors get pocket_ca_rmsd / pocket_sidechain_rmsd / w648_chi1 NaN'd
    out with a class-specific note. See module docstring."""
    return (receptor_class or "").upper() == "A"


def _class_deferred_note(receptor_class: str) -> str:
    cls = (receptor_class or "?").upper()
    return f"class_{cls}_pocket_deferred"


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------


def resolve_pocket_uniprot_positions(
    bw_map: dict[int, dict[str, str]],
    receptor_class: str,
) -> tuple[dict[str, int], tuple[str, ...]]:
    """Return ({bw_label: uniprot_pos}, missing_labels).

    For Class B / F this returns ``({}, POCKET_BW_LABELS)`` — the caller
    treats it as "pocket definition deferred for this class". For every
    other class the BW map is scanned position-by-position and any label
    that GPCRdb doesn't return is added to the ``missing`` tuple.
    """
    if not _is_pocket_supported_class(receptor_class):
        return {}, POCKET_BW_LABELS

    hits: dict[str, int] = {}
    missing: list[str] = []
    # Build a reverse index once — bw_map is UniProt-keyed.
    label_to_pos: dict[str, int] = {}
    for pos, info in bw_map.items():
        bw = info.get("bw") or ""
        if bw:
            label_to_pos[bw] = int(pos)
    for label in POCKET_BW_LABELS:
        if label in label_to_pos:
            hits[label] = label_to_pos[label]
        else:
            missing.append(label)
    return hits, tuple(missing)


# ---------------------------------------------------------------------------
# TM residue positions (for 7TM Kabsch)
# ---------------------------------------------------------------------------


def tm_positions_from_bw_map(bw_map: dict[int, dict[str, str]]) -> frozenset[int]:
    """Return the UniProt positions annotated as TM1..TM7 by GPCRdb.

    Mirrors the residue-selection rule in ``scripts/rescore_rmsd.py``
    (7TM-only per plan §14 step 4): auto-excises ECD (glycoprotein-
    hormone receptors), ICL3, N-terminus, C-terminus, and H8. Class-
    agnostic — A / B / F all use the same rule."""
    return frozenset(
        int(pos)
        for pos, info in bw_map.items()
        if (info.get("segment") or "").upper() in _TM_SEGMENTS
    )


# ---------------------------------------------------------------------------
# Individual axis functions
# ---------------------------------------------------------------------------


def pocket_ca_rmsd(
    vmodel: VerifiedModel,
    pocket_positions: dict[str, int],
    ref_ca_transformed: dict[int, gemmi.Position],
    receptor_class: str,
) -> tuple[float, str]:
    """CA RMSD over the 12 pocket BW positions.

    ``pocket_positions`` — {bw_label: uniprot_pos} for this receptor.
    Empty dict → NaN + class-deferred note (Class B / F short-circuit).

    ``ref_ca_transformed`` — {uniprot_pos: gemmi.Position} for the
    reference CAs after the caller has applied the 7TM CA Kabsch
    transform. This function does NOT re-align; the alignment lives
    in ``compute_pocket_axes_bundle`` so pocket_ca, pocket_sidechain,
    and ligand_rmsd all share one frame.

    Returns ``(rmsd_or_NaN, missing_residues_or_note)``. The second
    element is a semicolon-joined list of BW labels not present on
    either side (e.g. "3.36;7.42"), or a note like
    "class_B_pocket_deferred" / "insufficient_residues_3_of_12".
    """
    if not pocket_positions:
        return NaN, _class_deferred_note(receptor_class)

    missing: list[str] = []
    pred_pts: list[gemmi.Position] = []
    ref_pts: list[gemmi.Position] = []
    for label in POCKET_BW_LABELS:
        uniprot_pos = pocket_positions.get(label)
        if uniprot_pos is None:
            missing.append(label)
            continue
        r = vmodel.residues.get(uniprot_pos)
        if r is None:
            missing.append(label)
            continue
        pred_atom = r.find_atom("CA", "\0")
        ref_pos = ref_ca_transformed.get(uniprot_pos)
        if pred_atom is None or ref_pos is None:
            missing.append(label)
            continue
        pred_pts.append(pred_atom.pos)
        ref_pts.append(ref_pos)

    if len(pred_pts) < MIN_POCKET_RESIDUES:
        note = (
            f"insufficient_residues_{len(pred_pts)}_of_{len(POCKET_BW_LABELS)}"
            if not missing
            else ";".join(missing) + f"|n={len(pred_pts)}"
        )
        return NaN, note

    # RMSD in the shared aligned frame — direct distance sum.
    sq_sum = 0.0
    for p, r in zip(pred_pts, ref_pts):
        sq_sum += p.dist(r) ** 2
    rmsd = math.sqrt(sq_sum / len(pred_pts))
    note = ";".join(missing) if missing else ""
    return rmsd, note


def pocket_sidechain_rmsd(
    vmodel: VerifiedModel,
    pocket_positions: dict[str, int],
    ref_residues: dict[int, gemmi.Residue],
    ref_transform: Optional[gemmi.Transform],
    receptor_class: str,
) -> tuple[float, str]:
    """Sidechain-heavy-atom RMSD over the 12 pocket residues.

    An atom counts as "sidechain heavy" iff:
        atom.name NOT in {N, CA, C, O}  (backbone)
        atom.element.name != "H"        (hydrogen)

    Atoms are matched by name between prediction residue and reference
    residue at the SAME UniProt position. Atoms present on only one
    side (mutation, partial density) are excluded. A residue whose
    heavy-sidechain intersection is empty contributes nothing (e.g. two
    Gly matched, or all sidechain atoms disordered in one side).

    Reference atoms are transformed by ``ref_transform`` (the 7TM
    Kabsch mobile→target transform) so the sidechain RMSD sits in the
    same aligned frame as pocket_ca_rmsd. When ref_transform is None
    (Kabsch failed), returns NaN + "no_alignment_transform".

    Returns (rmsd_or_NaN, note).
    """
    if not pocket_positions:
        return NaN, _class_deferred_note(receptor_class)
    if ref_transform is None:
        return NaN, "no_alignment_transform"

    matched_pred: list[gemmi.Position] = []
    matched_ref: list[gemmi.Position] = []
    residues_used = 0

    for label in POCKET_BW_LABELS:
        uniprot_pos = pocket_positions.get(label)
        if uniprot_pos is None:
            continue
        pred_res = vmodel.residues.get(uniprot_pos)
        ref_res = ref_residues.get(uniprot_pos)
        if pred_res is None or ref_res is None:
            continue

        pred_sc: dict[str, gemmi.Position] = {}
        for a in pred_res:
            if a.name in _BACKBONE_ATOMS:
                continue
            if a.element.name == "H":
                continue
            pred_sc[a.name] = a.pos

        ref_sc: dict[str, gemmi.Position] = {}
        for a in ref_res:
            if a.name in _BACKBONE_ATOMS:
                continue
            if a.element.name == "H":
                continue
            ref_sc[a.name] = a.pos

        common_atoms = pred_sc.keys() & ref_sc.keys()
        if not common_atoms:
            continue
        residues_used += 1
        for name in common_atoms:
            matched_pred.append(pred_sc[name])
            v = ref_transform.apply(ref_sc[name])
            matched_ref.append(gemmi.Position(v.x, v.y, v.z))

    if residues_used < MIN_POCKET_RESIDUES or not matched_pred:
        return NaN, f"insufficient_sidechain_residues_{residues_used}_of_{len(POCKET_BW_LABELS)}"

    sq = 0.0
    for p, r in zip(matched_pred, matched_ref):
        sq += p.dist(r) ** 2
    return math.sqrt(sq / len(matched_pred)), ""


def _dihedral_deg(
    p1: gemmi.Position, p2: gemmi.Position,
    p3: gemmi.Position, p4: gemmi.Position,
) -> float:
    """Dihedral angle p1-p2-p3-p4 in degrees, in the standard
    right-handed convention (IUPAC). NaN on degenerate geometry."""
    # Vector algebra using gemmi's Vec3 arithmetic.
    b1 = gemmi.Vec3(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
    b2 = gemmi.Vec3(p3.x - p2.x, p3.y - p2.y, p3.z - p2.z)
    b3 = gemmi.Vec3(p4.x - p3.x, p4.y - p3.y, p4.z - p3.z)
    # Normal to plane (b1,b2) and (b2,b3)
    n1 = b1.cross(b2)
    n2 = b2.cross(b3)
    # b2 unit vector for signed angle
    b2_len = math.sqrt(b2.x * b2.x + b2.y * b2.y + b2.z * b2.z)
    if b2_len == 0.0:
        return NaN
    b2u = gemmi.Vec3(b2.x / b2_len, b2.y / b2_len, b2.z / b2_len)
    m1 = n1.cross(b2u)
    x = n1.dot(n2)
    y = m1.dot(n2)
    if x == 0.0 and y == 0.0:
        return NaN
    return math.degrees(math.atan2(y, x))


def w648_chi1(
    vmodel: VerifiedModel,
    pocket_positions: dict[str, int],
    receptor_class: str,
) -> tuple[float, str]:
    """W6.48 χ1 = dihedral N-Cα-Cβ-Cγ, in degrees.

    Class B / F: NaN + "class_B_no_w648" / "class_F_no_w648" (the Class
    B toggle switch is at a different position and not defined here).

    Class A but residue is NOT tryptophan (a point-mutant construct):
    NaN + "6.48_not_tryptophan_<observed>". The χ1 dihedral is defined
    for every AA with a γ-atom, but "W6.48 χ1" is a Trp-specific claim
    and the whole point of the metric is the toggle-switch tryptophan.

    NaN + "6.48_atoms_missing" when N / Cα / Cβ / Cγ is not modelled
    (rare — cryo-EM density loss on the sidechain).
    """
    if not _is_pocket_supported_class(receptor_class):
        return NaN, f"class_{(receptor_class or '?').upper()}_no_w648"

    pos = pocket_positions.get(W648_BW)
    if pos is None:
        return NaN, "6.48_not_in_bw_map"
    r = vmodel.residues.get(pos)
    if r is None:
        return NaN, f"6.48_not_modelled_uniprot_{pos}"
    aa = one_letter(r.name)
    if aa != "W":
        return NaN, f"6.48_not_tryptophan_{aa}"

    a_n = r.find_atom("N", "\0")
    a_ca = r.find_atom("CA", "\0")
    a_cb = r.find_atom("CB", "\0")
    a_cg = r.find_atom("CG", "\0")
    if a_n is None or a_ca is None or a_cb is None or a_cg is None:
        return NaN, "6.48_atoms_missing"
    d = _dihedral_deg(a_n.pos, a_ca.pos, a_cb.pos, a_cg.pos)
    if math.isnan(d):
        return NaN, "6.48_degenerate_dihedral"
    return d, ""


# Minimum atom count for the (atom_name, element) fast path. Below this
# floor the matcher falls back to RDKit MCS. Chosen to be permissive
# enough that a 5-atom fragment already-matched by name is trusted, but
# strict enough that a spurious 1-2-atom coincidence triggers MCS
# validation. See `ligand_rmsd_to_ref` docstring.
MCS_FALLBACK_MIN_MATCHED: int = 5


def _atoms_to_pdb_block(
    atoms: list[tuple[str, gemmi.Position, str]],
    resname: str = "LIG",
) -> str:
    """Serialise a list of (atom_name, position, element) tuples as a
    minimal PDB block that RDKit's ``MolFromPDBBlock`` can parse with
    ``proximityBonding=True``. Used only inside the MCS fallback path.
    """
    lines: list[str] = []
    rn = (resname or "LIG")[:3]
    for i, (name, pos, elem) in enumerate(atoms, start=1):
        # PDB atom-name column has quirky rules: 4-char names occupy
        # cols 13-16 flush-left; 1-3 char names sit in cols 14-16.
        n = (name or "X")[:4]
        if len(n) >= 4:
            name_field = n
        else:
            name_field = " " + n.ljust(3)
        el = (elem or "C")[:2].upper()
        line = (
            f"HETATM{i:5d} {name_field} {rn:<3s} A{1:4d}    "
            f"{pos.x:8.3f}{pos.y:8.3f}{pos.z:8.3f}"
            f"  1.00  0.00          {el:>2s}"
        )
        lines.append(line)
    lines.append("END")
    return "\n".join(lines)


def _rdkit_mol_from_atoms(
    atoms: list[tuple[str, gemmi.Position, str]],
    resname: str = "LIG",
):
    """Build an RDKit Mol from a heavy-atom list. Returns None on any
    parse failure. Uses distance-based bond perception (proximityBonding)
    which is what MCS-based ligand comparison needs when the source CIF
    has no CONECT records (typical of fold-model outputs)."""
    try:
        from rdkit import Chem
    except ImportError:  # pragma: no cover — env-dependent
        return None
    block = _atoms_to_pdb_block(atoms, resname)
    try:
        mol = Chem.MolFromPDBBlock(
            block, sanitize=False, removeHs=True, proximityBonding=True,
        )
    except Exception:
        return None
    if mol is None or mol.GetNumAtoms() == 0:
        return None
    # MCS with ringMatchesRingOnly=True + SubstructMatch on the MCS
    # SMARTS query both require RingInfo to be initialised. `sanitize=
    # False` above skips ring perception, so run FastFindRings
    # explicitly. UpdatePropertyCache(strict=False) fills in implicit
    # valence bookkeeping that FindMCS reads.
    try:
        mol.UpdatePropertyCache(strict=False)
        Chem.FastFindRings(mol)
    except Exception:
        return None
    return mol


def _mcs_ligand_rmsd(
    pred_atoms: list[tuple[str, gemmi.Position, str]],
    ref_atoms_transformed: list[tuple[str, gemmi.Position, str]],
) -> tuple[float, str, str]:
    """Return (rmsd, note, method) using RDKit MCS to pair prediction
    and reference ligand heavy atoms. Callers are responsible for the
    same-frame guarantee (reference positions already transformed).

    Method values:
      "mcs"             — matched, RMSD computed
      "mcs_too_small"   — MCS returned < MCS_FALLBACK_MIN_MATCHED atoms
      "parse_failure"   — one side failed to build an RDKit Mol
      "rdkit_unavailable" — import of rdkit failed at runtime
      "no_match"        — MCS returned an empty match set
    """
    try:
        from rdkit import Chem  # noqa: F401
        from rdkit.Chem import rdFMCS
    except ImportError:  # pragma: no cover — env-dependent
        return NaN, "rdkit_unavailable", "rdkit_unavailable"

    pred_mol = _rdkit_mol_from_atoms(pred_atoms, "PRD")
    if pred_mol is None:
        return NaN, "pred_ligand_parse_failure", "parse_failure"
    ref_mol = _rdkit_mol_from_atoms(ref_atoms_transformed, "REF")
    if ref_mol is None:
        return NaN, "ref_ligand_parse_failure", "parse_failure"

    try:
        mcs = rdFMCS.FindMCS(
            [pred_mol, ref_mol],
            atomCompare=rdFMCS.AtomCompare.CompareElements,
            bondCompare=rdFMCS.BondCompare.CompareOrder,
            ringMatchesRingOnly=True,
            completeRingsOnly=True,
            timeout=5,
            matchValences=False,
        )
    except Exception:
        return NaN, "mcs_exception", "no_match"
    if mcs is None or mcs.numAtoms == 0 or not mcs.smartsString:
        return NaN, "mcs_no_common_substructure", "no_match"
    if mcs.numAtoms < MCS_FALLBACK_MIN_MATCHED:
        return (
            NaN,
            f"mcs_too_small_matched_{mcs.numAtoms}",
            "mcs_too_small",
        )

    try:
        from rdkit import Chem
        q = Chem.MolFromSmarts(mcs.smartsString)
    except Exception:
        return NaN, "mcs_query_build_failed", "no_match"
    if q is None:
        return NaN, "mcs_query_build_failed", "no_match"

    # RDKit requires ring info before GetSubstructMatch on molecules built from
    # non-standard sources (PDB blocks with partial sanitization). GetSSSR
    # initializes the RingInfo without raising on marginal molecules. Do the
    # same on the query for symmetry.
    try:
        Chem.GetSSSR(pred_mol)
        Chem.GetSSSR(ref_mol)
        Chem.GetSSSR(q)
    except Exception:
        return NaN, "mcs_ring_init_failed", "no_match"

    pred_match = pred_mol.GetSubstructMatch(q)
    ref_match = ref_mol.GetSubstructMatch(q)
    if (
        not pred_match
        or not ref_match
        or len(pred_match) != len(ref_match)
    ):
        return NaN, "mcs_substruct_mismatch", "no_match"

    # Pull positions per-index in the deterministic order the query
    # yielded. Positions are already in the shared aligned frame.
    pred_conf = pred_mol.GetConformer()
    ref_conf = ref_mol.GetConformer()
    sq = 0.0
    for pi, ri in zip(pred_match, ref_match):
        p = pred_conf.GetAtomPosition(pi)
        r = ref_conf.GetAtomPosition(ri)
        sq += (p.x - r.x) ** 2 + (p.y - r.y) ** 2 + (p.z - r.z) ** 2
    n = len(pred_match)
    rmsd = math.sqrt(sq / n)
    note = (
        f"mcs_matched_{n}_of_pred_{pred_mol.GetNumAtoms()}"
        f"_ref_{ref_mol.GetNumAtoms()}"
    )
    return rmsd, note, "mcs"


def ligand_rmsd_to_ref(
    struct: gemmi.Structure,
    receptor_chain_name: str,
    ref_transform: Optional[gemmi.Transform],
    ref_ligand_positions: list[gemmi.Position],
    ref_ligand_atom_names: list[str],
    ref_ligand_atom_elements: list[str],
    input_state_claim: str,
    ligand_type: str,
) -> tuple[float, str, str]:
    """Ligand heavy-atom RMSD to the reference crystal ligand.

    Prediction ligand atoms are pulled from HETATM residues on the
    receptor chain of ``struct`` (Boltz / OF3 / Protenix / Chai all
    place small-molecule and peptide ligands as chains alongside the
    receptor; peptide ligand atoms are protein-chain residues with a
    different chain name and are picked up in the receptor-chain sweep
    only if the fold model stapled them into the receptor chain,
    which none of the four currently do). Non-ligand HETATM residues
    (waters, common metals, cryo-buffer, lipid) are excluded via
    ``_NON_LIGAND_RESNAMES``.

    Alignment: pred ligand atoms are compared to reference ligand
    atoms via ``ref_transform`` applied to the reference. The
    transform is the 7TM CA Kabsch produced upstream so this RMSD
    sits in the same aligned frame as the pocket_ca / _sidechain
    RMSDs.

    Matching (2026-09-06 MCS-fallback rework, [[ligand-rmsd-atom-name-gap-
    2026-09-06]]): a two-stage pairing —

      1. **``(atom_name, element)`` fast path** — kept verbatim so
         numerical results on OF3 / Protenix (which preserve CCD atom
         names) are byte-identical to the pre-MCS implementation. If
         this yields ``>= MCS_FALLBACK_MIN_MATCHED`` matches the RMSD
         is returned with method ``"atom_name_element"``.
      2. **RDKit MCS fallback** — triggered when the fast path
         matches 0 atoms OR fewer than ``MCS_FALLBACK_MIN_MATCHED``.
         Builds proximity-bonded RDKit Mols from both ligands, runs
         ``rdFMCS.FindMCS`` with ``CompareElements``/``CompareOrder``/
         ``ringMatchesRingOnly=True``/``completeRingsOnly=True``/
         ``timeout=5``, and pairs atoms by the MCS query match.
         Unlocks Boltz / Chai outputs, whose SMILES-derived atom names
         diverge from CCD.

    Returns ``(rmsd_or_NaN, note, method)``.

    ``method`` values:
      - ``"atom_name_element"`` — fast path succeeded (>= 5 matches).
      - ``"mcs"``                — MCS fallback succeeded.
      - ``"mcs_too_small"``      — MCS returned < 5 atoms.
      - ``"no_match"``           — MCS query construction / match failed.
      - ``"parse_failure"``      — one side failed to build an RDKit Mol.
      - ``"rdkit_unavailable"``  — RDKit not importable at runtime.
      - ``""``                    — early exit before any pairing was
                                     attempted (apo / no transform /
                                     no ref ligand / empty struct).

    NaN cases (Ambiguity #4-approved posture — decoy_lig rows still
    compute; analysis layer filters):
      - input_state_claim == "apo"                 → "apo_no_ligand"
      - ligand_type in {"apo", "none", ""}         → "ligand_type_{X}"
      - ref_transform is None                      → "no_alignment_transform"
      - no ligand atoms in prediction              → "no_pred_ligand"
      - no ligand atoms in reference               → "no_ref_ligand"
      - atom-name overlap + MCS both fail          → NaN, method carries
                                                     the failure class

    **Consumers must filter decoy_lig rows** — the pose distance
    computed against a real-ligand reference is not meaningful for a
    property-matched non-binder.
    """
    if input_state_claim == StateClaim.APO.value:
        return NaN, "apo_no_ligand", ""
    if ligand_type in ("apo", "none", ""):
        return NaN, f"ligand_type_{ligand_type or 'empty'}", ""
    if ref_transform is None:
        return NaN, "no_alignment_transform", ""
    if not ref_ligand_positions:
        return NaN, "no_ref_ligand", ""

    # Collect prediction ligand atoms.
    # `pred_by_name` retains the pre-MCS "first-name-wins" behaviour so
    # the fast path is byte-identical on OF3 / Protenix. `pred_atoms`
    # keeps the full atom list (order preserved) for the MCS fallback.
    if len(struct) == 0:
        return NaN, "empty_struct", ""
    pred_by_name: dict[str, tuple[gemmi.Position, str]] = {}
    pred_atoms: list[tuple[str, gemmi.Position, str]] = []
    model = struct[0]
    for ch in model:
        # Peptide ligands may land on a non-receptor chain; small
        # molecules almost always land on the receptor chain as HETATM.
        # Scan every chain; skip only the receptor chain's AA residues.
        for r in ch:
            # Skip receptor amino-acid residues (they are one_letter in
            # STD_AA and land on the receptor chain).
            if ch.name == receptor_chain_name and one_letter(r.name) in STD_AA:
                continue
            if r.name in _NON_LIGAND_RESNAMES:
                continue
            # Waters that don't happen to be named HOH/WAT
            if one_letter(r.name) == "?" and len(r.name) == 1:
                # Single-atom "residues" that aren't in the metal list —
                # be conservative and skip.
                continue
            for a in r:
                if a.element.name == "H":
                    continue
                pred_by_name.setdefault(a.name, (a.pos, a.element.name))
                pred_atoms.append(
                    (a.name, gemmi.Position(a.pos.x, a.pos.y, a.pos.z),
                     a.element.name)
                )

    if not pred_by_name:
        return NaN, "no_pred_ligand", ""

    # Reference atoms — apply the transform.
    ref_by_name: dict[str, tuple[gemmi.Position, str]] = {}
    ref_atoms_transformed: list[tuple[str, gemmi.Position, str]] = []
    for pos, name, elem in zip(
        ref_ligand_positions, ref_ligand_atom_names, ref_ligand_atom_elements
    ):
        if elem == "H":
            continue
        v = ref_transform.apply(pos)
        p = gemmi.Position(v.x, v.y, v.z)
        ref_by_name[name] = (p, elem)
        ref_atoms_transformed.append((name, p, elem))

    if not ref_by_name:
        return NaN, "no_ref_ligand", ""

    # --- Stage 1: (atom_name, element) fast path ---------------------
    matched_pred: list[gemmi.Position] = []
    matched_ref: list[gemmi.Position] = []
    for name, (p_pos, p_elem) in pred_by_name.items():
        if name in ref_by_name:
            r_pos, r_elem = ref_by_name[name]
            if r_elem == p_elem:
                matched_pred.append(p_pos)
                matched_ref.append(r_pos)

    if len(matched_pred) >= MCS_FALLBACK_MIN_MATCHED:
        sq = 0.0
        for p, r in zip(matched_pred, matched_ref):
            sq += p.dist(r) ** 2
        rmsd = math.sqrt(sq / len(matched_pred))
        note = (
            f"matched_{len(matched_pred)}_of_pred_{len(pred_by_name)}"
            f"_ref_{len(ref_by_name)}"
        )
        return rmsd, note, "atom_name_element"

    # --- Stage 2: RDKit MCS fallback ---------------------------------
    # Reasons the fast path missed:
    #   - Boltz / Chai emit SMILES-derived atom names (no CCD overlap).
    #   - Ref & pred use the same CCD but a different atom-name scheme.
    #   - Real chemistry mismatch (decoy against a real-lig reference).
    reason = (
        "no_atom_match"
        if not matched_pred
        else f"atom_name_matched_only_{len(matched_pred)}"
    )
    rmsd, mcs_note, method = _mcs_ligand_rmsd(pred_atoms, ref_atoms_transformed)
    combined_note = f"{reason};{mcs_note}"
    return rmsd, combined_note, method


# ---------------------------------------------------------------------------
# Reference-set role selection
# ---------------------------------------------------------------------------


def _role_for_state_claim(
    state_claim: str,
    ligand_role: str = "",
) -> tuple[Optional[str], str]:
    """Which reference role + role_specific does this row compare against?

    Returns a ``(role, role_specific)`` tuple.
      role ∈ {"active", "inactive", None}
      role_specific ∈ {"", "inactive_neutral_antagonist",
                       "inactive_inverse_agonist"}
      Empty ``role_specific`` = fall back to the generic
      role-matched reference.

    Block C extension (2026-09-04): the manifest carries
    ``ligand_role`` on every row (Block C-specific column). For rows
    with ``state_claim="Ga-coupled-active"`` (which is what Block C
    dispatches on every row so the run tests whether the model
    behaves activated-like when fed each ligand), the ligand's actual
    pharmacology determines which reference is chemistry-matched:

      - ``full_agonist``       → active reference (matches state claim)
      - ``neutral_antagonist`` → inactive with
                                 role_specific=inactive_neutral_antagonist
                                 (or generic inactive if role_specific
                                  ref is not curated for this receptor)
      - ``inverse_agonist``    → inactive with
                                 role_specific=inactive_inverse_agonist
                                 (or generic inactive)
      - ``none`` / ``decoy_lig`` / empty
                                → active (no natural
                                 antagonist-side pairing for apo /
                                 non-binding decoys)

    For explicit inactive state_claim values
    (``INACTIVE_ANTAGONIST`` / ``INACTIVE_INVERSE_AGONIST``), the
    role_specific comes from the state itself and ligand_role is
    ignored — the state_claim is already the ground truth.

    Backwards compatibility: ``ligand_role=""`` (the default) reverts
    to the pre-Block-C behaviour (returns only role; role_specific is
    empty). Existing callers that never pass ``ligand_role`` see no
    behavioural change.

    Mirrors ``scorer.references._role_for_state`` — duplicated here
    to avoid the cross-module import (partner_metrics also inlines
    its role logic). Kept in sync with references.py.
    """
    if state_claim in (
        StateClaim.Ga_COUPLED_ACTIVE.value,
        StateClaim.ARRESTIN_COUPLED.value,
    ):
        if ligand_role == "neutral_antagonist":
            return ("inactive", "inactive_neutral_antagonist")
        if ligand_role == "inverse_agonist":
            return ("inactive", "inactive_inverse_agonist")
        # full_agonist / none / decoy_lig / empty → active
        return ("active", "")
    if state_claim == StateClaim.INACTIVE_ANTAGONIST.value:
        return ("inactive", "inactive_neutral_antagonist")
    if state_claim == StateClaim.INACTIVE_INVERSE_AGONIST.value:
        return ("inactive", "inactive_inverse_agonist")
    return (None, "")


# ---------------------------------------------------------------------------
# Helper — pocket RMSDs against one specific reference
# ---------------------------------------------------------------------------


def _pocket_rmsds_against_ref(
    vmodel: VerifiedModel,
    ref: "PocketReferenceCache",
    pocket_positions: dict[str, int],
    tm_positions: frozenset[int],
    receptor_class: str,
) -> tuple[float, float, str, int]:
    """Run 7TM Kabsch to ``ref`` and return the pair
    (pocket_ca_rmsd, pocket_sidechain_rmsd, note, n_common_tm).

    Independent per reference — used by ``compute_pocket_axes_bundle``
    to emit the dual-reference companion columns
    ``pocket_ca_rmsd_active`` / ``pocket_ca_rmsd_inactive`` (Stage 2
    of the Block C Post-Audit, 2026-09-05). Each variant fits its own
    7TM Kabsch so the RMSD reflects the best-fit alignment to that
    specific reference — the (active, inactive) pair is arithmetically
    comparable for a single prediction and supports the 2×2 ligand-
    state-specificity interaction test in Stage 3a.

    ``ref`` — a PocketReferenceCache for the desired reference; None-
    checking is the caller's responsibility.

    Returns (ca_rmsd, sc_rmsd, note, n_common_tm). NaN + explanatory
    note on Kabsch failure or missing residues; note is a
    ``|``-joined summary suitable for appending to ``pocket_notes``.
    """
    # Collect common TM CAs for Kabsch.
    pred_ca: list[gemmi.Position] = []
    ref_ca: list[gemmi.Position] = []
    for pos_u in sorted(tm_positions):
        pred_res = vmodel.residues.get(pos_u)
        ref_pos = ref.ca_by_uniprot.get(pos_u)
        if pred_res is None or ref_pos is None:
            continue
        pred_atom = pred_res.find_atom("CA", "\0")
        if pred_atom is None:
            continue
        pred_ca.append(pred_atom.pos)
        ref_ca.append(ref_pos)

    n_common = len(pred_ca)
    sup = _superpose_transform(pred_ca, ref_ca)
    if sup is None:
        return NaN, NaN, f"7tm_kabsch_failed_n_{n_common}", n_common

    to_pred_frame = sup.transform.inverse()
    ref_ca_transformed: dict[int, gemmi.Position] = {}
    for label, uniprot_pos in pocket_positions.items():
        rp = ref.ca_by_uniprot.get(uniprot_pos)
        if rp is None:
            continue
        v = to_pred_frame.apply(rp)
        ref_ca_transformed[uniprot_pos] = gemmi.Position(v.x, v.y, v.z)

    ca_rmsd, _ca_miss = pocket_ca_rmsd(
        vmodel, pocket_positions, ref_ca_transformed, receptor_class,
    )
    sc_rmsd, sc_note = pocket_sidechain_rmsd(
        vmodel, pocket_positions, ref.residues_by_uniprot,
        to_pred_frame, receptor_class,
    )
    note = f"n_tm={n_common}"
    if sc_note:
        note += f"|sc:{sc_note}"
    return ca_rmsd, sc_rmsd, note, n_common


# ---------------------------------------------------------------------------
# Top-level bundle
# ---------------------------------------------------------------------------


def compute_pocket_axes_bundle(
    vmodel: VerifiedModel,
    struct: gemmi.Structure,
    bw_map: dict[int, dict[str, str]],
    receptor_class: str,
    receptor_chain_name: str,
    input_state_claim: str,
    ligand_type: str,
    *,
    ref_active: Optional[PocketReferenceCache],
    ref_inactive: Optional[PocketReferenceCache],
    ref_inactive_by_role_specific: Optional[
        dict[str, "PocketReferenceCache"]
    ] = None,
    ligand_role: str = "",
) -> dict[str, Any]:
    """Emit the six pocket-metric columns as a dict.

    Selects the role-matched reference:
      - ``full_agonist`` (or empty ligand_role) with
        ``Ga-coupled-active`` state → ACTIVE reference.
      - ``neutral_antagonist`` with ``Ga-coupled-active`` state →
        INACTIVE reference, preferring the role-specific
        ``inactive_neutral_antagonist`` entry if
        ``ref_inactive_by_role_specific`` supplies one; else the
        generic ``ref_inactive``.
      - ``inverse_agonist`` with ``Ga-coupled-active`` state →
        INACTIVE reference, preferring
        ``inactive_inverse_agonist`` if supplied; else generic
        ``ref_inactive``.
      - Explicit inactive state_claims route on the state alone.
      - apo / design / class_bc_native_no_dry — fall back to
        active if available, else inactive.

    Apo rows fall back to the ACTIVE reference for pocket_ca / _sc /
    w648_chi1 (measuring "how close is the apo pocket to the active
    conformation"); ligand_rmsd is NaN for apo (state_claim guard).

    Performs a single 7TM CA Kabsch, then calls the four axis
    functions with a shared transform.

    Returns dict with:
      - pocket_ca_rmsd (float, NaN on any failure)
      - pocket_sidechain_rmsd (float)
      - w648_chi1 (float, degrees)
      - ligand_rmsd_to_ref (float, Å)
      - pocket_ca_rmsd_missing_residues (str, ";"-joined BW labels)
      - pocket_notes (str, ";"-joined per-metric notes)
    """
    out: dict[str, Any] = {
        "pocket_ca_rmsd": NaN,
        "pocket_sidechain_rmsd": NaN,
        "w648_chi1": NaN,
        "ligand_rmsd_to_ref": NaN,
        # 2026-09-06: which atom-pairing path produced ``ligand_rmsd_to_ref``.
        # One of {"atom_name_element", "mcs", "mcs_too_small",
        # "no_match", "parse_failure", "rdkit_unavailable", ""} — see
        # ``ligand_rmsd_to_ref`` docstring.
        "pocket_ligand_atom_map_method": "",
        "pocket_ca_rmsd_missing_residues": "",
        "pocket_notes": "",
        # Post-Audit dual-reference variants (Stage 2, 2026-09-05). Each
        # of the two variants runs its own independent 7TM Kabsch fit to
        # the corresponding reference PDB, so the RMSD is best-fit and
        # comparable across the (active, inactive) pair for a given
        # prediction. Empty / NaN when the corresponding reference is
        # absent or the Kabsch fails.
        "pocket_ca_rmsd_active": NaN,
        "pocket_ca_rmsd_inactive": NaN,
        "pocket_sidechain_rmsd_active": NaN,
        "pocket_sidechain_rmsd_inactive": NaN,
        "pocket_ref_pdb_sha_active": "",
        "pocket_ref_pdb_sha_inactive": "",
        "pocket_ref_role_active": "",
        "pocket_ref_role_inactive": "",
    }
    notes: list[str] = []

    # Resolve the pocket residues (short-circuits for Class B/F).
    pocket_positions, missing_bw = resolve_pocket_uniprot_positions(
        bw_map, receptor_class,
    )

    # Pick the role-matched reference, ligand-role-aware.
    role, role_specific = _role_for_state_claim(input_state_claim,
                                                ligand_role)
    role_specific_map = ref_inactive_by_role_specific or {}
    if role == "active":
        ref = ref_active
        ref_specific_note = ""
    elif role == "inactive":
        # Prefer the role_specific-tagged inactive if the caller
        # supplied one. Fall back to the generic inactive.
        specific_ref = role_specific_map.get(role_specific) if role_specific else None
        if specific_ref is not None:
            ref = specific_ref
            ref_specific_note = f"ref_role_specific={role_specific}"
        else:
            ref = ref_inactive
            ref_specific_note = (
                f"ref_role_specific_fallback_to_generic_inactive"
                if role_specific
                else ""
            )
    else:
        # apo / design / class_bc_native_no_dry — fall back to active
        # if available, else inactive.
        ref = ref_active if ref_active is not None else ref_inactive
        ref_specific_note = ""
    if ref_specific_note:
        notes.append(ref_specific_note)

    if ref is None:
        notes.append("no_reference_available")
        out["pocket_notes"] = ";".join(notes)
        # Try w648_chi1 anyway — it doesn't need a reference.
        w_val, w_note = w648_chi1(vmodel, pocket_positions, receptor_class)
        out["w648_chi1"] = w_val
        if w_note:
            notes.append(f"w648_chi1:{w_note}")
        out["pocket_notes"] = ";".join(notes)
        return out

    # 7TM Kabsch — the shared alignment frame.
    tm_positions = tm_positions_from_bw_map(bw_map)
    pred_ca: list[gemmi.Position] = []
    ref_ca: list[gemmi.Position] = []
    common_tm_positions: list[int] = []
    for pos_u in sorted(tm_positions):
        pred_res = vmodel.residues.get(pos_u)
        ref_pos = ref.ca_by_uniprot.get(pos_u)
        if pred_res is None or ref_pos is None:
            continue
        pred_atom = pred_res.find_atom("CA", "\0")
        if pred_atom is None:
            continue
        pred_ca.append(pred_atom.pos)
        ref_ca.append(ref_pos)
        common_tm_positions.append(pos_u)

    sup = _superpose_transform(pred_ca, ref_ca)
    if sup is None:
        notes.append(f"7tm_kabsch_failed_n_{len(pred_ca)}")
        # Try w648_chi1 (no alignment dependency).
        w_val, w_note = w648_chi1(vmodel, pocket_positions, receptor_class)
        out["w648_chi1"] = w_val
        if w_note:
            notes.append(f"w648_chi1:{w_note}")
        out["pocket_notes"] = ";".join(notes)
        return out

    # `sup.transform` maps mobile (pred) → target (ref). To bring the
    # REFERENCE into the prediction frame we need its inverse. Compose
    # once and cache.
    to_pred_frame = sup.transform.inverse()

    # Transform reference CAs of the pocket residues into the pred frame.
    ref_ca_transformed: dict[int, gemmi.Position] = {}
    for label, uniprot_pos in pocket_positions.items():
        ref_pos = ref.ca_by_uniprot.get(uniprot_pos)
        if ref_pos is None:
            continue
        v = to_pred_frame.apply(ref_pos)
        ref_ca_transformed[uniprot_pos] = gemmi.Position(v.x, v.y, v.z)

    # 1. pocket_ca_rmsd
    ca_rmsd, ca_missing = pocket_ca_rmsd(
        vmodel, pocket_positions, ref_ca_transformed, receptor_class,
    )
    out["pocket_ca_rmsd"] = ca_rmsd
    out["pocket_ca_rmsd_missing_residues"] = ca_missing

    # 2. pocket_sidechain_rmsd — pass the inverse transform so the
    # function can pull raw ref sidechain atoms and move them into the
    # pred frame consistently.
    sc_rmsd, sc_note = pocket_sidechain_rmsd(
        vmodel, pocket_positions, ref.residues_by_uniprot,
        to_pred_frame, receptor_class,
    )
    out["pocket_sidechain_rmsd"] = sc_rmsd
    if sc_note:
        notes.append(f"pocket_sc:{sc_note}")

    # 3. w648_chi1 — no alignment needed.
    w_val, w_note = w648_chi1(vmodel, pocket_positions, receptor_class)
    out["w648_chi1"] = w_val
    if w_note:
        notes.append(f"w648_chi1:{w_note}")

    # 4. ligand_rmsd_to_ref
    lig_rmsd, lig_note, lig_method = ligand_rmsd_to_ref(
        struct, receptor_chain_name, to_pred_frame,
        ref.ligand_atoms_positions, ref.ligand_atom_names,
        ref.ligand_atom_elements, input_state_claim, ligand_type,
    )
    out["ligand_rmsd_to_ref"] = lig_rmsd
    out["pocket_ligand_atom_map_method"] = lig_method
    if lig_note:
        notes.append(f"lig:{lig_note}")

    # 5. Dual-reference companion RMSDs (Post-Audit Stage 2, 2026-09-05).
    # Fit an independent 7TM Kabsch to each of (active reference,
    # role_specific-selected inactive reference) so each row carries
    # pocket_ca / pocket_sc distances to BOTH state references. Enables
    # the 2×2 ligand-state-specificity interaction test at analysis
    # time. Only run on Class A (pocket residues resolved); Class B/F
    # short-circuit to NaN via `pocket_positions == {}` handling in the
    # RMSD helper. `ligand_rmsd_to_ref` intentionally stays on the
    # role-matched frame — it needs the reference ligand chemistry
    # match, which is a role-specific choice.
    if pocket_positions:
        # ACTIVE variant
        if ref_active is not None:
            ca_a, sc_a, note_a, _ = _pocket_rmsds_against_ref(
                vmodel, ref_active, pocket_positions,
                tm_positions, receptor_class,
            )
            out["pocket_ca_rmsd_active"] = ca_a
            out["pocket_sidechain_rmsd_active"] = sc_a
            out["pocket_ref_pdb_sha_active"] = getattr(
                ref_active, "provenance_sha256", ""
            )
            out["pocket_ref_role_active"] = "active"
            if note_a and not math.isnan(ca_a):
                # Only append the note when the value is populated — a
                # Kabsch failure already surfaces via the NaN.
                pass
        # INACTIVE variant — prefer role_specific if the caller supplied
        # one that matched the row's ligand_role.
        inactive_choice: Optional[PocketReferenceCache] = None
        inactive_role_tag = ""
        if role == "inactive":
            # Primary reference is inactive — reuse it (matches routing).
            inactive_choice = ref
            inactive_role_tag = role_specific or ""
            if not inactive_role_tag:
                inactive_role_tag = "generic_inactive"
        else:
            # Primary reference is active — look up an inactive companion.
            # Prefer role_specific from ligand_role; fall back to generic.
            _, expected_specific = _role_for_state_claim(
                StateClaim.Ga_COUPLED_ACTIVE.value, ligand_role,
            )
            if expected_specific and expected_specific in (
                role_specific_map or {}
            ):
                inactive_choice = role_specific_map[expected_specific]
                inactive_role_tag = expected_specific
            elif ref_inactive is not None:
                inactive_choice = ref_inactive
                inactive_role_tag = "generic_inactive_fallback"
        if inactive_choice is not None:
            ca_i, sc_i, note_i, _ = _pocket_rmsds_against_ref(
                vmodel, inactive_choice, pocket_positions,
                tm_positions, receptor_class,
            )
            out["pocket_ca_rmsd_inactive"] = ca_i
            out["pocket_sidechain_rmsd_inactive"] = sc_i
            out["pocket_ref_pdb_sha_inactive"] = getattr(
                inactive_choice, "provenance_sha256", ""
            )
            out["pocket_ref_role_inactive"] = inactive_role_tag

    # Provenance additions
    notes.append(f"ref={role or 'fallback'}:{ref.pdb_id}")
    notes.append(f"7tm_n={len(common_tm_positions)}")
    if missing_bw:
        notes.append(f"bw_missing={';'.join(missing_bw)}")

    out["pocket_notes"] = ";".join(notes)
    return out


# ---------------------------------------------------------------------------
# Reference loader — turns a PDB path into a PocketReferenceCache
# ---------------------------------------------------------------------------


def build_pocket_reference_cache(
    pdb_path: str,
    entry_name: str,
    api,
    pdb_id: str = "",
) -> Optional[PocketReferenceCache]:
    """Load a reference PDB and produce a PocketReferenceCache.

    Uses ``scorer.structure.build_uniprot_model`` for the receptor
    chain (same path scoring uses), then sweeps all chains for HETATM
    ligand atoms. Returns None on any load / chain-selection failure —
    the caller records that as "no_reference_available".

    Lipids / waters / metals / buffers are filtered from the ligand
    scan via ``_NON_LIGAND_RESNAMES``. The largest remaining HETATM
    residue by atom count becomes the reference ligand.
    """
    from scorer.structure import build_uniprot_model  # local import — avoid cycle
    import hashlib
    try:
        model = build_uniprot_model(pdb_path, entry_name, api)
    except Exception:
        return None

    # Stamp the PDB SHA at cache-build time so the orchestrator can emit
    # it on every scored row's `pocket_ref_pdb_sha_active` /
    # `pocket_ref_pdb_sha_inactive` companion columns without re-reading
    # the file. Silent empty on read failure — provenance is best-effort
    # (test fixtures may pass a nonexistent path).
    try:
        _pdb_sha = hashlib.sha256(open(str(pdb_path), "rb").read()).hexdigest()
    except OSError:
        _pdb_sha = ""

    ca_by_uniprot: dict[int, gemmi.Position] = {}
    residues_by_uniprot: dict[int, gemmi.Residue] = {}
    for uniprot_pos, r in model.residues.items():
        atom = r.find_atom("CA", "\0")
        if atom is None:
            continue
        ca_by_uniprot[int(uniprot_pos)] = atom.pos
        residues_by_uniprot[int(uniprot_pos)] = r

    # Ligand scan across all chains.
    try:
        struct = gemmi.read_structure(str(pdb_path))
    except Exception:
        struct = None

    ligand_positions: list[gemmi.Position] = []
    ligand_names: list[str] = []
    ligand_elements: list[str] = []
    ligand_resname = ""

    if struct is not None and len(struct) > 0:
        # Group HETATM residues by (chain, resname, seqid) and pick the
        # largest by heavy-atom count.
        candidates: list[tuple[int, str, list]] = []
        for ch in struct[0]:
            for r in ch:
                if r.name in _NON_LIGAND_RESNAMES:
                    continue
                if one_letter(r.name) in STD_AA:
                    continue
                heavy = [a for a in r if a.element.name != "H"]
                if not heavy:
                    continue
                candidates.append((len(heavy), r.name, heavy))
        if candidates:
            # Key by heavy-atom count only (and resname as a deterministic
            # tie-breaker) — a bare tuple sort falls through to comparing
            # the list-of-gemmi.Atom third element, which is a TypeError
            # (gemmi.Atom does not implement __lt__). B1 dispatch 2026-09-03.
            candidates.sort(key=lambda c: (c[0], c[1]), reverse=True)
            _, ligand_resname, heavy_atoms = candidates[0]
            for a in heavy_atoms:
                ligand_positions.append(gemmi.Position(a.pos.x, a.pos.y, a.pos.z))
                ligand_names.append(a.name)
                ligand_elements.append(a.element.name)

    return PocketReferenceCache(
        pdb_id=pdb_id,
        ca_by_uniprot=ca_by_uniprot,
        residues_by_uniprot=residues_by_uniprot,
        ligand_atoms_positions=ligand_positions,
        ligand_atom_names=ligand_names,
        ligand_atom_elements=ligand_elements,
        ligand_resname=ligand_resname,
        provenance_sha256=_pdb_sha,
    )
