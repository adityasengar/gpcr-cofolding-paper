"""Gemmi-based PDB/CIF loader → UniProt-numbered residue model.

Ports one_letter / STD_AA / align_numbering verbatim from
gpcr-structure-pipeline/gpcr_pipeline.py:128-203. Adds:

  select_chain(struct, wt_seq)             — A3 (chain-identity gate)
  build_uniprot_model(path, entry_name, anchors, api)
                                            — A2 (missing-anchor gate)
"""
from __future__ import annotations

import difflib
from dataclasses import dataclass, field
from typing import Any

import gemmi

from scorer.assertions import A2FASTATrunc, A3WrongChain
from scorer.bw_numbering import Api, get_generic_numbers


STD_AA: set[str] = set("ACDEFGHIKLMNPQRSTVWY")
_ONE: dict[str, str] = {}


def one_letter(name: str) -> str:
    """3-letter residue -> upper-case 1-letter code ('?' if not amino acid).

    Ported verbatim from gpcr_pipeline.py:132-138.
    """
    if name not in _ONE:
        info = gemmi.find_tabulated_residue(name)
        _ONE[name] = (info.one_letter_code.upper()
                      if info and info.is_amino_acid() else "?")
    return _ONE[name]


def align_numbering(residues: list[Any], wt_seq: dict[int, str],
                    *, max_gap_fill: int = 30) -> dict[int, int]:
    """Map residue-list indices -> UniProt positions by aligning the observed
    one-letter sequence to the WT sequence. Short unaligned runs (mutations,
    modified residues) are filled from the flanking anchors; long unaligned
    runs (fusion inserts like T4L=164 aa, BRIL=106 aa) are left UNMAPPED.

    Ported from gpcr_pipeline.py:163-203 with one correction: the original
    extrapolated across every gap regardless of size, which pushes real
    receptor residues downstream of a T4L insert past their correct UniProt
    positions. The AA-identity check at each anchor then compares the wrong
    physical residue — audit finding #4 in miniature.

    ``max_gap_fill=30`` bracket: covers point-mutation runs (typical
    thermostabilised constructs have <=10 mutations); rejects fusion
    inserts (>=100 residues).
    """
    wt_pos = sorted(wt_seq)
    wt_str = "".join(wt_seq[p] for p in wt_pos)
    obs = [one_letter(r.name) for r in residues]
    obs_str = "".join(a if a in STD_AA else "X" for a in obs)
    sm = difflib.SequenceMatcher(a=obs_str, b=wt_str, autojunk=False)
    mapping: dict[int, int] = {}
    for i, j, n in sm.get_matching_blocks():
        if n >= 3:  # ignore spurious 1-2 residue matches
            for k in range(n):
                mapping[i + k] = wt_pos[j + k]
    if not mapping:
        return mapping

    # Short-gap extrapolation only. Long gaps (fusion inserts) stay
    # unmapped — their residues don't get UniProt numbers and are
    # excluded from the UniProt-numbered model downstream.
    for i in range(len(obs)):
        if i in mapping:
            continue
        left = i - 1
        while left >= 0 and left not in mapping:
            left -= 1
        right = i + 1
        while right < len(obs) and right not in mapping:
            right += 1
        gap_left = i - left if left >= 0 else float("inf")
        gap_right = right - i if right < len(obs) else float("inf")
        gap_span = (right - left - 1) if (left >= 0 and right < len(obs)) else max(gap_left, gap_right)
        if gap_span > max_gap_fill:
            continue  # fusion insert — leave unmapped

        # Flank-consistency check. When both flanks are known, only
        # extrapolate linearly if the flank positions are exactly
        # (right - left) apart in UniProt. If flank_delta != (right - left),
        # the gap contains an insert or deletion — extrapolating would
        # fabricate false positions that then get amplified by the
        # strictly-increasing enforcer below, corrupting downstream matches
        # (w40/w47 TEV-insert constructs: identity drops to ~12% because
        # every residue past the insert lands +N off). See
        # refs/a3_chain_picker_diag_report.md for the full trace.
        if left >= 0 and right < len(obs):
            flank_delta = mapping[right] - mapping[left]
            if flank_delta != (right - left):
                continue  # insert/deletion in gap — leave unmapped

        if left >= 0:
            mapping[i] = mapping[left] + (i - left)
        elif right < len(obs):
            mapping[i] = mapping[right] - (right - i)
    # enforce strictly increasing numbers over the mapped subset. With the
    # flank-consistency check above, real difflib match blocks and
    # consistent extrapolations are already monotone by construction; this
    # enforcer stays as belt-and-braces for pathological inputs where two
    # match blocks happened to overlap.
    last = None
    for i in sorted(mapping):
        if last is not None and mapping[i] <= last:
            mapping[i] = last + 1
        last = mapping[i]
    return mapping


@dataclass
class ChainMatch:
    name: str                                # chain identifier from the PDB/CIF
    n_residues_matched: int
    identity: float                          # 0..1
    # index-in-chain -> UniProt position
    index_to_uniprot: dict[int, int] = field(default_factory=dict)


def _load_structure(path: str) -> gemmi.Structure:
    # gemmi raises RuntimeError on a variety of coord-file load failures
    # ("no structural models", unrecognised format, corrupt data). The
    # batch driver's sanctioned catch site only trips on
    # ScorerAssertionError, so a raw RuntimeError from here would abort
    # the entire batch. Recast as A3WrongChain: semantically it's the
    # same class of problem (can't pick a receptor chain from this
    # coord file). The specific gemmi message is preserved so the
    # failure_census.json retains diagnostic info.
    try:
        st = gemmi.read_structure(str(path), merge_chain_parts=True)
    except (RuntimeError, ValueError, OSError) as e:  # lint-allow: capture-and-recast — gemmi load failure → A3
        raise A3WrongChain(f"gemmi coord-file load failed: {e}") from e
    st.setup_entities()
    return st


def _score_deposited(residues: list[Any], wt_seq: dict[int, str]) -> ChainMatch | None:
    """Score identity using deposited residue numbers directly.

    Most modern GPCR crystals deposit with UniProt-canonical numbering for
    the receptor chain and either put fusion residues at 1001+ or on a
    different chain letter. In that case, walking ``r.seqid.num`` and
    checking ``r.seqid.num in wt_seq`` gives a clean identity — the T4L
    residues at 1001+ simply don't intersect wt_seq. This is the pattern
    the frozen ``coord_mutations`` in gpcr_pipeline.py:141-160 used.
    """
    matched = 0
    aligned = 0
    mapping: dict[int, int] = {}
    for i, r in enumerate(residues):
        n = r.seqid.num
        if n not in wt_seq:
            continue
        aligned += 1
        mapping[i] = n
        if one_letter(r.name) == wt_seq[n]:
            matched += 1
    if aligned == 0:
        return None
    return ChainMatch(
        name="",
        n_residues_matched=matched,
        identity=matched / aligned,
        index_to_uniprot=mapping,
    )


def _score_aligned(residues: list[Any], wt_seq: dict[int, str]) -> ChainMatch | None:
    """Fallback: align observed sequence to WT and score identity.

    Used when deposited numbering doesn't cleanly cover wt_seq — older
    PDBs, constructs with unusual numbering offsets, and AI predictions
    on a truncated FASTA where the emitted PDB is numbered 1..N instead
    of the UniProt canonical range. select_chain runs BOTH paths and
    picks by identity (see Trap-1 comment there).
    """
    mapping = align_numbering(residues, wt_seq)
    if not mapping:
        return None
    matched = 0
    aligned = 0
    for i, uniprot_pos in mapping.items():
        wt_aa = wt_seq.get(uniprot_pos)
        if wt_aa is None:
            continue
        aligned += 1
        if one_letter(residues[i].name) == wt_aa:
            matched += 1
    if aligned == 0:
        return None
    return ChainMatch(
        name="",
        n_residues_matched=matched,
        identity=matched / aligned,
        index_to_uniprot=mapping,
    )


def _better(a: ChainMatch | None, b: ChainMatch | None) -> ChainMatch | None:
    """Pick the ChainMatch with more matched residues; None if both None.

    Ties broken by identity. This is the correct comparator for
    Trap-1: on a truncated-FASTA AI prediction, ``_score_deposited``
    may hit ~40 residues by coincidence (passing any bare
    ``>=30`` gate) while ``_score_aligned`` correctly maps all 300
    residues. Picking by matched count selects the alignment path
    where it actually finds the receptor.
    """
    if a is None:
        return b
    if b is None:
        return a
    if b.n_residues_matched > a.n_residues_matched:
        return b
    if b.n_residues_matched == a.n_residues_matched and b.identity > a.identity:
        return b
    return a


def select_chain(
    struct: gemmi.Structure,
    wt_seq: dict[int, str],
    *,
    min_matched: int = 200,
    min_identity: float = 0.70,
) -> ChainMatch:
    """Pick the chain whose sequence identity to `wt_seq` is highest.

    For each chain, try TWO scoring paths:
      1. Deposited numbering (frozen coord_mutations pattern) — reliable
         when the PDB deposits with UniProt-canonical numbering and puts
         fusions at 1001+ or on a different chain.
      2. Alignment via difflib SequenceMatcher (align_numbering) — used
         when deposited numbering doesn't intersect wt_seq at all.

    The higher-identity path wins per chain; the best chain across the
    structure is returned.

    ``min_identity`` default is 0.70 because reference crystals are almost
    always engineered constructs — thermostabilised (5–25 point mutations),
    ligand-binding-site mutants, or chimeras. Wild-type β2AR (3SN6) hits
    ~99% by deposit; 4LDE (β2AR + T4L, several mutations) sits at ~89%;
    7BU7 (thermostabilised β1AR) at ~85%. Partner subunits (Gα, Gβ, Gγ,
    arrestin, nanobody, T4L standalone chain) sit at <20% and never pass.

    A1 downstream still verifies each anchor's observed AA against the
    canonical, so mutant constructs where the DRY/NPxxY anchors are
    themselves mutated fail A1 rather than passing here.
    """
    # A structure with no models (empty / corrupt input coord file) would
    # IndexError on ``struct[0]``. Recast as A3 so the batch driver's
    # sanctioned catch site (scorer.orchestrator.score_and_capture)
    # captures it and records a failure row rather than aborting the run.
    if len(struct) == 0:
        raise A3WrongChain("input coordinate file contains no models")
    model = struct[0]
    best: ChainMatch | None = None
    for ch in model:
        residues = [r for r in ch if one_letter(r.name) in STD_AA]
        if len(residues) < 30:
            continue

        # Trap-1 fix (see docs/RESIDUE_CHECKS.md): always score BOTH paths,
        # pick the winner by identity — never short-circuit on the deposit
        # path.
        #
        # The prior gate "fall back to aligned only if deposited < 30
        # matched" was wrong for AI predictions on a TRUNCATED FASTA
        # (Boltz-style input residues 50..350 -> output PDB numbered
        # 1..301). Deposited scoring can hit ~40 residues by chance at
        # each position (some AA-at-shifted-position happens to match
        # by coincidence), passing the >=30 gate and hiding the real
        # 300-residue alignment. Downstream A1 then compares wrong
        # atoms and either fires garbage mismatches or silently
        # produces off-by-N axes.
        #
        # Running both and picking max(matched) selects the deposit path
        # only when it's *genuinely* the better mapping.
        m_dep = _score_deposited(residues, wt_seq)
        m_aln = _score_aligned(residues, wt_seq)
        m = _better(m_dep, m_aln)
        if m is None:
            continue
        m.name = ch.name
        if best is None or m.n_residues_matched > best.n_residues_matched:
            best = m

    if best is None:
        raise A3WrongChain(
            "no chain in the input structure has ≥30 standard amino acids",
        )
    if best.n_residues_matched < min_matched or best.identity < min_identity:
        raise A3WrongChain(
            f"best chain {best.name!r} matched {best.n_residues_matched} "
            f"residues at {best.identity:.2%} identity (need >= {min_matched} "
            f"at >= {min_identity:.0%})",
            chain=best.name,
            n_residues_matched=best.n_residues_matched,
            identity=best.identity,
        )
    return best


@dataclass
class UnverifiedUniProtModel:
    """A single receptor chain, renumbered to UniProt positions.

    Renamed from ``UniProtModel`` at M1 — the founding premise is that
    A1/A2/A3 cannot be bypassed. The scorer must never call
    ``compute_all_axes`` (or any downstream classifier) on a raw model.
    Every axis-consuming site takes ``scorer.verified.VerifiedModel`` —
    which can only be constructed via ``verify()``, running A2 + A1.

    ``UnverifiedUniProtModel`` is the raw structure-loader output. To
    reach the scoring path, call ``scorer.verified.verify(model, anchor_set)``.

    ``residues[uniprot_pos] = gemmi.Residue`` — direct handle so
    axis-code gets CA coords via ``r.find_atom("CA", "\\0")``.
    """

    entry_name: str
    chain_name: str
    residues: dict[int, gemmi.Residue] = field(default_factory=dict)
    identity: float = 0.0
    matched: int = 0
    numbering_source: str = "aligned-to-uniprot"

    def observed_positions(self) -> set[int]:
        return set(self.residues.keys())

    def observed_aa_at(self, uniprot_pos: int) -> str | None:
        r = self.residues.get(uniprot_pos)
        if r is None:
            return None
        return one_letter(r.name)

    def ca(self, uniprot_pos: int) -> gemmi.Position | None:
        r = self.residues.get(uniprot_pos)
        if r is None:
            return None
        atom = r.find_atom("CA", "\0")
        return atom.pos if atom is not None else None


# Back-compat alias — a few sites still import `UniProtModel` from
# scorer.structure. Keep the name pointing at the unverified type so it's
# unambiguous that axis paths need `VerifiedModel`.
UniProtModel = UnverifiedUniProtModel


def build_uniprot_model(
    path: str,
    entry_name: str,
    api: Api,
) -> UnverifiedUniProtModel:
    """Load PDB/CIF, pick the receptor chain (A3), renumber to UniProt.

    Returns an UNVERIFIED model — the caller must pass it through
    ``scorer.verified.verify()`` before invoking any axis-computing
    function. This is the founding premise of the scorer: assertions
    cannot be bypassed.

    ``entry_name`` — the GPCRdb entry name (e.g. ``"adrb2_human"``). We
    build the WT sequence by querying GPCRdb residues/extended once and
    materialising ``{uniprot_pos: one_letter_aa}``.
    """
    bw_map = get_generic_numbers(api, entry_name)
    if not bw_map:
        raise A2FASTATrunc(
            f"GPCRdb returned no residues for {entry_name!r}",
            entry_name=entry_name,
        )
    wt_seq: dict[int, str] = {
        int(pos): str(info["aa"])
        for pos, info in bw_map.items()
        if info.get("aa") and info["aa"] in STD_AA
    }
    struct = _load_structure(path)
    match = select_chain(struct, wt_seq)

    # materialise the renumbered residue map
    model = struct[0]
    ch = next(c for c in model if c.name == match.name)
    residues = [r for r in ch if one_letter(r.name) in STD_AA]
    renumbered: dict[int, gemmi.Residue] = {}
    for idx, r in enumerate(residues):
        uniprot_pos = match.index_to_uniprot.get(idx)
        if uniprot_pos is None:
            continue
        renumbered[uniprot_pos] = r
    return UnverifiedUniProtModel(
        entry_name=entry_name,
        chain_name=match.name,
        residues=renumbered,
        identity=match.identity,
        matched=match.n_residues_matched,
    )
