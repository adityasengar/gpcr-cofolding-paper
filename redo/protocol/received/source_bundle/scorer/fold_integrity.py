"""Fold-integrity columns for the Block B Stage 0 Gate 1 artefact screen.

Self-contained sidecar to ``scorer/axes.py``. Adds four columns per
prediction — computed directly from the CIF, without touching the
scorer's VerifiedModel / GPCRdb path (which would re-run identity /
coverage assertions and pull the residue extensions again).

The four columns:

  tm6_helicity_6_30_6_50       — fraction of the BW 6.30-6.50 residues
                                 (21 residues in UniProt space; BW is
                                 sequential within a single TM helix)
                                 with φ,ψ inside the α-helix box:
                                 φ ∈ [-90, -35], ψ ∈ [-70, -15].
                                 Terminal residues where φ or ψ is
                                 undefined are excluded from the
                                 denominator.

  chain_breaks                 — integer count of CA-CA distances > 4.5 Å
                                 between residues at consecutive integer
                                 sequence numbers (i, i+1) in the
                                 receptor chain. Residues where either
                                 CA is absent are skipped (never
                                 counted as a break).

  ramachandran_outlier_frac    — fraction of residues with (φ,ψ) NOT
                                 in any of the three canonical allowed
                                 boxes. Cited rule (Lovell-inspired,
                                 explicitly rectangular; used as-is
                                 across all chains, no residue-type
                                 specialisation):

                                   α  : φ ∈ [-180,   0], ψ ∈ [-90,  45]
                                   β  : φ ∈ [-180, -45], ψ ∈ [90, 180] ∪ [-180, -160]
                                   L-α: φ ∈ [30,  130], ψ ∈ [-20,  90]

                                 A residue with defined φ AND ψ that
                                 falls into none of the three boxes is
                                 counted as outlier. Terminal residues
                                 (first: no φ; last: no ψ) are
                                 excluded from the denominator.

  icl3_modelled_count          — integer number of UniProt positions
                                 in the GPCRdb-defined ICL3 range of
                                 the receptor that have a CA atom in
                                 the selected chain of the CIF. NaN
                                 when the GPCRdb residues-extended
                                 payload is unavailable for the
                                 receptor entry.

Design notes:

* No scorer.verified / scorer.structure dependency. This module reads
  the CIF with gemmi, picks a chain by name, and walks residues by
  ``r.seqid.num`` interpreted directly as the UniProt position — which
  matches the boltz/chai/of3/protenix full-length-input predictions
  audited for this campaign (n_ca == canonical UniProt length in
  ``rows.csv``, residues numbered 1..N where N is the canonical length).

* No mutation of ``scorer/axes.py`` or any other scorer module. The
  driver (``scripts/rescore_fold_integrity.py``) imports this module
  and merges the four columns onto ``rows.csv`` into a NEW CSV. The
  frozen scorer / orchestrator / rows.csv are not touched.

* GPCRdb ICL3 boundaries are read from the local
  ``refs/cache/gpcrdb/residues_ext_<entry>.json`` cache the campaign
  already populated. No live GPCRdb fetch is performed; if a cache
  file is missing, ``icl3_modelled_count`` returns NaN.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import gemmi


# ---------------------------------------------------------------------------
# Ramachandran rule — recorded here so the CSV header can cite it exactly.
# ---------------------------------------------------------------------------

RAMACHANDRAN_RULE = (
    "Simplified rectangular allowed regions (Lovell-inspired, no residue-type "
    "specialisation): a residue with defined phi AND psi is NOT an outlier if "
    "it falls into any of three boxes: "
    "alpha (phi in [-180,0], psi in [-90,45]); "
    "beta (phi in [-180,-45], psi in [90,180] or psi in [-180,-160]); "
    "L-alpha (phi in [30,130], psi in [-20,90]). "
    "Otherwise counted as outlier. Terminal residues (first: no phi; "
    "last: no psi) are excluded from the denominator."
)

# TM6 helicity α-box specified by the task:
ALPHA_PHI_LO, ALPHA_PHI_HI = -90.0, -35.0
ALPHA_PSI_LO, ALPHA_PSI_HI = -70.0, -15.0
TM6_HELICITY_RULE = (
    f"Fraction of residues in the BW 6.30-6.50 UniProt range (pos_6_30 through "
    f"pos_6_30+20 inclusive, 21 positions) with phi,psi inside the canonical "
    f"alpha-helix box phi in [{ALPHA_PHI_LO},{ALPHA_PHI_HI}], "
    f"psi in [{ALPHA_PSI_LO},{ALPHA_PSI_HI}]. Denominator = residues where "
    f"BOTH phi and psi are defined. NaN when pos_6_30 is missing."
)

CHAIN_BREAK_CUTOFF_A = 4.5
CHAIN_BREAK_RULE = (
    f"Integer count of CA-CA distances > {CHAIN_BREAK_CUTOFF_A} Å between "
    f"residues at consecutive integer sequence numbers (i, i+1) inside the "
    f"selected chain. Missing CA on either side of a pair is skipped, not "
    f"counted."
)


# ---------------------------------------------------------------------------
# core dihedral / CIF helpers
# ---------------------------------------------------------------------------


def _load_structure(path: str) -> gemmi.Structure:
    """Load a CIF/PDB via gemmi. Raises FileNotFoundError / RuntimeError
    on load failure — the driver catches and records a failure row."""
    st = gemmi.read_structure(str(path), merge_chain_parts=True)
    if len(st) == 0:
        raise RuntimeError(f"no models in {path}")
    return st


def _pick_chain(model: gemmi.Model, chain_name: str) -> gemmi.Chain | None:
    for ch in model:
        if ch.name == chain_name:
            return ch
    return None


def _atom(residue: gemmi.Residue, name: str) -> gemmi.Atom | None:
    """Return the named atom, or None. Uses gemmi's find_atom (alt-loc-aware
    with the '\\0' first-altloc convention consistent with scorer/axes.py)."""
    return residue.find_atom(name, "\0")


def _build_seq_index(chain: gemmi.Chain) -> dict[int, gemmi.Residue]:
    """Map ``seqid.num`` -> residue for the FIRST protein residue at that
    seq number in the chain. Non-protein residues (waters, ligands) are
    skipped.

    Alt-loc handling: gemmi.merge_chain_parts is set at load time; each
    (seqid.num) has one canonical residue per chain in practice for these
    fold-model outputs.
    """
    out: dict[int, gemmi.Residue] = {}
    for r in chain:
        info = gemmi.find_tabulated_residue(r.name)
        if info is None or not info.is_amino_acid():
            continue
        n = r.seqid.num
        if n not in out:
            out[n] = r
    return out


def _phi_psi(
    seq_idx: dict[int, gemmi.Residue],
    pos: int,
) -> tuple[float | None, float | None]:
    """φ(pos), ψ(pos) in degrees. Either or both may be None (terminals /
    missing atoms). Uses gemmi.calculate_dihedral (radians) → converted."""
    r_i = seq_idx.get(pos)
    if r_i is None:
        return None, None
    n_i = _atom(r_i, "N")
    ca_i = _atom(r_i, "CA")
    c_i = _atom(r_i, "C")
    if n_i is None or ca_i is None or c_i is None:
        return None, None

    r_prev = seq_idx.get(pos - 1)
    r_next = seq_idx.get(pos + 1)

    phi = None
    if r_prev is not None:
        c_prev = _atom(r_prev, "C")
        if c_prev is not None:
            phi_rad = gemmi.calculate_dihedral(
                c_prev.pos, n_i.pos, ca_i.pos, c_i.pos
            )
            phi = math.degrees(phi_rad)

    psi = None
    if r_next is not None:
        n_next = _atom(r_next, "N")
        if n_next is not None:
            psi_rad = gemmi.calculate_dihedral(
                n_i.pos, ca_i.pos, c_i.pos, n_next.pos
            )
            psi = math.degrees(psi_rad)

    return phi, psi


# ---------------------------------------------------------------------------
# GPCRdb ICL3 range — read from local cache; no live fetch.
# ---------------------------------------------------------------------------


def load_icl3_range(
    gpcrdb_slug: str,
    cache_dir: Path,
) -> tuple[int, int] | None:
    """Return (icl3_first_uniprot_pos, icl3_last_uniprot_pos) inclusive, or
    None when the GPCRdb residues-extended cache file is missing or
    contains no ICL3 residues for this receptor.

    The cache file is
    ``<cache_dir>/gpcrdb/residues_ext_<gpcrdb_slug>.json``. It is the
    exact payload GPCRdb's ``/services/residues/extended/<entry>/``
    endpoint returns, cached by the campaign; the ICL3 range is
    reconstructed from residues whose ``protein_segment == "ICL3"``.
    """
    p = cache_dir / "gpcrdb" / f"residues_ext_{gpcrdb_slug}.json"
    if not p.exists():
        return None
    with p.open() as f:
        residues = json.load(f)
    icl3_positions: list[int] = [
        int(r["sequence_number"])
        for r in residues
        if r.get("protein_segment") == "ICL3" and r.get("sequence_number") is not None
    ]
    if not icl3_positions:
        return None
    return min(icl3_positions), max(icl3_positions)


# ---------------------------------------------------------------------------
# individual columns
# ---------------------------------------------------------------------------


def tm6_helicity_6_30_6_50(
    seq_idx: dict[int, gemmi.Residue],
    pos_6_30: int | None,
) -> float:
    """Fraction of residues in BW 6.30..6.50 (UniProt pos_6_30 through
    pos_6_30 + 20 inclusive, 21 positions) with (φ,ψ) inside the α-helix
    box specified in ``TM6_HELICITY_RULE``.

    Denominator = residues where BOTH φ and ψ are defined. NaN when
    pos_6_30 is missing OR when no residue in the range has both
    dihedrals defined."""
    if pos_6_30 is None or (isinstance(pos_6_30, float) and math.isnan(pos_6_30)):
        return float("nan")
    n_defined = 0
    n_alpha = 0
    for pos in range(int(pos_6_30), int(pos_6_30) + 21):
        phi, psi = _phi_psi(seq_idx, pos)
        if phi is None or psi is None:
            continue
        n_defined += 1
        if (ALPHA_PHI_LO <= phi <= ALPHA_PHI_HI
                and ALPHA_PSI_LO <= psi <= ALPHA_PSI_HI):
            n_alpha += 1
    if n_defined == 0:
        return float("nan")
    return n_alpha / n_defined


def chain_breaks(seq_idx: dict[int, gemmi.Residue]) -> int:
    """Integer count of CA-CA distances > CHAIN_BREAK_CUTOFF_A between
    residues at consecutive integer seq numbers (i, i+1). Missing-CA
    pairs are skipped — not counted as a break, since a missing atom is
    a different failure mode from a stretched backbone."""
    n = 0
    positions = sorted(seq_idx.keys())
    for i in positions:
        j = i + 1
        r_i = seq_idx.get(i)
        r_j = seq_idx.get(j)
        if r_i is None or r_j is None:
            continue
        ca_i = _atom(r_i, "CA")
        ca_j = _atom(r_j, "CA")
        if ca_i is None or ca_j is None:
            continue
        if ca_i.pos.dist(ca_j.pos) > CHAIN_BREAK_CUTOFF_A:
            n += 1
    return n


def _in_alpha(phi: float, psi: float) -> bool:
    return -180.0 <= phi <= 0.0 and -90.0 <= psi <= 45.0


def _in_beta(phi: float, psi: float) -> bool:
    if not (-180.0 <= phi <= -45.0):
        return False
    return (90.0 <= psi <= 180.0) or (-180.0 <= psi <= -160.0)


def _in_lalpha(phi: float, psi: float) -> bool:
    return 30.0 <= phi <= 130.0 and -20.0 <= psi <= 90.0


def ramachandran_outlier_frac(seq_idx: dict[int, gemmi.Residue]) -> float:
    """Fraction of residues with defined (φ,ψ) that fall in none of the
    three allowed boxes cited in ``RAMACHANDRAN_RULE``. NaN when no
    residue in the chain has both dihedrals defined."""
    n_defined = 0
    n_outlier = 0
    for pos in sorted(seq_idx.keys()):
        phi, psi = _phi_psi(seq_idx, pos)
        if phi is None or psi is None:
            continue
        n_defined += 1
        if _in_alpha(phi, psi) or _in_beta(phi, psi) or _in_lalpha(phi, psi):
            continue
        n_outlier += 1
    if n_defined == 0:
        return float("nan")
    return n_outlier / n_defined


def icl3_modelled_count(
    seq_idx: dict[int, gemmi.Residue],
    icl3_range: tuple[int, int] | None,
) -> float:
    """Number of UniProt positions in the GPCRdb-defined ICL3 range that
    have a CA atom present in the selected chain. NaN when the ICL3
    range is unavailable (cache miss)."""
    if icl3_range is None:
        return float("nan")
    lo, hi = icl3_range
    n = 0
    for pos in range(lo, hi + 1):
        r = seq_idx.get(pos)
        if r is None:
            continue
        if _atom(r, "CA") is None:
            continue
        n += 1
    return float(n)


# ---------------------------------------------------------------------------
# top-level compute per prediction
# ---------------------------------------------------------------------------


def compute_fold_integrity(
    input_path: str,
    chain_name: str,
    pos_6_30: int | None,
    icl3_range: tuple[int, int] | None,
) -> dict[str, Any]:
    """Compute the four fold-integrity columns for one CIF.

    Returns a dict with keys:
      tm6_helicity_6_30_6_50, chain_breaks,
      ramachandran_outlier_frac, icl3_modelled_count

    Any exception during CIF load or chain lookup surfaces as
    all-NaN row plus a `load_error` key carrying the exception message.
    The driver decides whether to log the row as failed.
    """
    out: dict[str, Any] = {
        "tm6_helicity_6_30_6_50": float("nan"),
        "chain_breaks": -1,
        "ramachandran_outlier_frac": float("nan"),
        "icl3_modelled_count": float("nan"),
        "load_error": "",
    }
    try:
        st = _load_structure(input_path)
    except Exception as e:
        out["load_error"] = f"load: {type(e).__name__}: {e}"
        return out
    model = st[0]
    chain = _pick_chain(model, chain_name)
    if chain is None:
        out["load_error"] = f"chain {chain_name!r} not found; available={[c.name for c in model]}"
        return out
    seq_idx = _build_seq_index(chain)
    if not seq_idx:
        out["load_error"] = f"chain {chain_name!r} has no protein residues"
        return out

    out["tm6_helicity_6_30_6_50"] = tm6_helicity_6_30_6_50(seq_idx, pos_6_30)
    out["chain_breaks"] = chain_breaks(seq_idx)
    out["ramachandran_outlier_frac"] = ramachandran_outlier_frac(seq_idx)
    out["icl3_modelled_count"] = icl3_modelled_count(seq_idx, icl3_range)
    return out
