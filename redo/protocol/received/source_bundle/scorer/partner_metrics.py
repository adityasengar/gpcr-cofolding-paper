"""Partner-interface metrics — the receptor↔Gα geometry that PREREG §10
Block A depends on.

Without these columns a shuffled/decoy-partner arm cannot distinguish
"partner rejected" (Gα floats away from the receptor) from "partner
mis-docked" (Gα binds but into the wrong pocket). Emitted on every
scored row alongside the frozen axes; NaN when the input is
single-chain (apo / no-partner) — never 0, so an apo run does not
alias a coupled-but-non-contacting run in downstream analysis.

Public API (imported by ``scorer.orchestrator``):

  compute_partner_metrics(struct, vmodel, bw_map, *, receptor_chain_name,
                          input_state_claim, partner_identity=None)
      -> dict[str, float]

Returns a dict with exactly four keys:

  "d_ga_alpha5_r350_ca"
  "n_interface_contacts_ga_receptor"
  "plddt_ga_alpha5"

  (``d_npxxy_y558_y753_oh`` lives in scorer.axes because it is a
   receptor-only axis.)

The Gα chain is picked by ``pick_ga_chain``: a length-based heuristic
that accepts any non-receptor chain in [200, 500] amino acids and picks
the largest such chain. This covers two-chain predictions (receptor +
Gα, the common case) directly. Heterotrimeric predictions would need
partner_identity to disambiguate Gα from Gβ (both ~340 aa); the
heuristic silently prefers whichever is longer, which is Gα for every
alpha_* variant in ``docs/EXPERIMENT_CATALOG/sequences/partners.fasta``
except alphagust / alphao / alphai2 / alphaz (354–355 aa, ties with
Gβ). partner_identity is accepted as an override but not currently
consumed — the Block-A first-cut manifests are all two-chain, so the
disambiguation is unused. When heterotrimeric runs enter the corpus
this helper will need an explicit sequence-match path.
"""
from __future__ import annotations

import math
from typing import Optional

import gemmi

from scorer.axes import _residue_plddt
from scorer.schema import StateClaim
from scorer.structure import STD_AA, one_letter
from scorer.verified import VerifiedModel


NaN = float("nan")

_APO_STATE = StateClaim.APO.value

# Interface cutoff — heavy-atom contact under this distance counts.
INTERFACE_CUTOFF_A: float = 5.0

# α5 window at the Gα C-terminus. 20 residues covers the α5 helix + α5-CT
# per the Class A GPCR literature (Rasmussen 2011, Draper-Joyce 2018).
ALPHA5_WINDOW: int = 20


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _chain_aa_residues(chain: gemmi.Chain) -> list[gemmi.Residue]:
    """Standard amino acid residues in chain order (no waters / ligands)."""
    return [r for r in chain if one_letter(r.name) in STD_AA]


def pick_ga_chain(
    struct: gemmi.Structure,
    receptor_chain_name: str,
    partner_identity: Optional[str] = None,  # noqa: ARG001 — reserved for hetero-trimer
) -> Optional[gemmi.Chain]:
    """Pick the Gα chain from a receptor-containing structure.

    ``partner_identity`` is accepted for future disambiguation (heterotrimeric
    receptor+Gα+Gβ+Gγ predictions where Gα must be told apart from Gβ by
    sequence) and is currently unused; the docstring on the module explains
    why.

    Returns ``None`` when no plausible Gα chain is present — an apo run,
    or a receptor-only structure. Callers propagate that as NaN.
    """
    if len(struct) == 0:
        return None
    model = struct[0]
    candidates: list[tuple[int, gemmi.Chain]] = []
    for ch in model:
        if ch.name == receptor_chain_name:
            continue
        residues = _chain_aa_residues(ch)
        n = len(residues)
        # 200..500 covers alphas (394), alpha11/alphaq (359), alpha13 (377),
        # alphai/alphao/alphagust/alphaz (354–355). Also admits a truncated
        # Gα or an α5-only mini-partner used in some decoy arms.
        if 200 <= n <= 500:
            candidates.append((n, ch))
    if not candidates:
        return None
    # Deterministic tie-break: largest AA count, then by chain name.
    candidates.sort(key=lambda t: (-t[0], t[1].name))
    return candidates[0][1]


def _tm3_5_6_positions(bw_map: dict[int, dict[str, str]]) -> set[int]:
    """UniProt positions whose GPCRdb ``protein_segment`` is TM3/TM5/TM6.

    Used to scope the interface-contact count to the intracellular Gα
    binding face (per PREREG §10). Empty set on a class-B receptor whose
    bw_map lacks TM* segments would collapse the count to 0 — but then
    n_interface_contacts_ga_receptor is class-inapplicable anyway; the
    class-aware annotation column carries that reading.
    """
    return {
        int(pos)
        for pos, info in bw_map.items()
        if info.get("segment") in ("TM3", "TM5", "TM6")
    }


def _heavy_atoms(residue: gemmi.Residue) -> list[gemmi.Atom]:
    """Non-hydrogen atoms of ``residue``. gemmi elements carry a name
    attribute; ``H`` marks a hydrogen."""
    return [at for at in residue if at.element.name != "H"]


def _min_pos(atoms: list[gemmi.Atom]) -> Optional[gemmi.Position]:
    return atoms[0].pos if atoms else None


# ---------------------------------------------------------------------------
# individual metrics
# ---------------------------------------------------------------------------


def d_ga_alpha5_r350_ca(vmodel: VerifiedModel, ga_chain: Optional[gemmi.Chain]) -> float:
    """CA-CA distance from the Gα C-terminal residue to receptor R3.50.

    NaN in the no-partner case, or when either CA is missing.
    """
    if ga_chain is None:
        return NaN
    p350 = None
    a = vmodel.anchor_set.anchors.get("3.50")
    if a is not None:
        p350 = a.uniprot_pos
    if p350 is None:
        return NaN
    r350 = vmodel.residues.get(p350)
    if r350 is None:
        return NaN
    ca_r350 = r350.find_atom("CA", "\0")
    if ca_r350 is None:
        return NaN
    ga_res = _chain_aa_residues(ga_chain)
    if not ga_res:
        return NaN
    ct_residue = ga_res[-1]
    ca_ct = ct_residue.find_atom("CA", "\0")
    if ca_ct is None:
        return NaN
    return ca_r350.pos.dist(ca_ct.pos)


def n_interface_contacts_ga_receptor(
    vmodel: VerifiedModel,
    ga_chain: Optional[gemmi.Chain],
    bw_map: dict[int, dict[str, str]],
    cutoff: float = INTERFACE_CUTOFF_A,
) -> float:
    """Count Gα heavy atoms within ``cutoff`` Å of any receptor TM3/TM5/TM6
    heavy atom. Each Gα atom is counted at most once (an atom in contact
    with several TM atoms still contributes 1).

    Returns NaN on the no-partner case (see module docstring for the
    NaN-vs-0 design decision).
    """
    if ga_chain is None:
        return NaN
    tm_positions = _tm3_5_6_positions(bw_map)
    if not tm_positions:
        # Nothing to compare against — signal "not measurable" rather than
        # a bogus 0.
        return NaN
    tm_atoms: list[gemmi.Atom] = []
    for pos in tm_positions:
        r = vmodel.residues.get(pos)
        if r is None:
            continue
        tm_atoms.extend(_heavy_atoms(r))
    if not tm_atoms:
        return NaN
    ga_residues = _chain_aa_residues(ga_chain)
    if not ga_residues:
        return NaN
    cutoff_sq = cutoff * cutoff
    contacts = 0
    for r in ga_residues:
        for ga_at in _heavy_atoms(r):
            ga_pos = ga_at.pos
            for tm_at in tm_atoms:
                # gemmi Position lacks a squared-distance shortcut; use
                # component subtraction so we skip the sqrt on every atom
                # pair (this is the hot loop — thousands of comparisons).
                dx = ga_pos.x - tm_at.pos.x
                dy = ga_pos.y - tm_at.pos.y
                dz = ga_pos.z - tm_at.pos.z
                if dx * dx + dy * dy + dz * dz <= cutoff_sq:
                    contacts += 1
                    break  # per-Gα-atom contribution counted; move on
    return float(contacts)


def plddt_ga_alpha5(
    ga_chain: Optional[gemmi.Chain],
    n_terminal_residues: int = ALPHA5_WINDOW,
) -> float:
    """Mean per-residue pLDDT over the last ``n_terminal_residues`` of Gα.

    Per-residue pLDDT is the mean B-factor of the residue's atoms —
    matching the convention already used by ``scorer.axes._residue_plddt``
    for co-folding outputs (Boltz, OF3, Protenix, AF2).
    NaN when the chain is absent or none of the terminal residues carry
    a resolvable B-factor.
    """
    if ga_chain is None:
        return NaN
    residues = _chain_aa_residues(ga_chain)
    if not residues:
        return NaN
    window = residues[-n_terminal_residues:]
    vals: list[float] = []
    for r in window:
        v = _residue_plddt(r)
        if not math.isnan(v):
            vals.append(v)
    if not vals:
        return NaN
    return sum(vals) / len(vals)


# ---------------------------------------------------------------------------
# public entry point
# ---------------------------------------------------------------------------


def compute_partner_metrics(
    struct: gemmi.Structure,
    vmodel: VerifiedModel,
    bw_map: dict[int, dict[str, str]],
    *,
    receptor_chain_name: str,
    input_state_claim: str,
    partner_identity: Optional[str] = None,
) -> dict[str, float]:
    """Compute the three Gα-dependent partner-interface metrics.

    NaN in the no-partner case (apo state claim, or no plausible Gα
    chain in the structure). See module docstring for the NaN-vs-0
    design decision on the contact count.
    """
    # Explicit apo → NaN short-circuit. Consistent with the state-claim
    # semantics (an APO-declared run should not have partner metrics even
    # if some upstream artifact left a chain in the file).
    ga_chain: Optional[gemmi.Chain]
    if input_state_claim == _APO_STATE:
        ga_chain = None
    else:
        ga_chain = pick_ga_chain(struct, receptor_chain_name, partner_identity)
    return {
        "d_ga_alpha5_r350_ca": d_ga_alpha5_r350_ca(vmodel, ga_chain),
        "n_interface_contacts_ga_receptor": n_interface_contacts_ga_receptor(
            vmodel, ga_chain, bw_map
        ),
        "plddt_ga_alpha5": plddt_ga_alpha5(ga_chain),
    }
