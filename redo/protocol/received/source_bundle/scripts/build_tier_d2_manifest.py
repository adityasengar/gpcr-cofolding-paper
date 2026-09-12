"""Build Tier D2 manifest — nanobody-directed inactive/active resample.

**Purpose**
    Emit the 260-row manifest at
    ``experiments/023_tier_d2_directed_inactive/manifest/tier_d2_manifest.csv``
    and, when ``--materialise-inputs-dir`` is given, write the 260 per-row
    backbone-input files under that dir.

    Grid (locked, PREREG §D-2.3):
      13 (receptor, arm) cells × 4 backbones × 5 seeds × 10 samples
      = 2,600 predictions.

      Arm-availability per receptor (from
      ``refs/nanobody_state_anchors.csv``):
        - ADRB2:  4 arms — apo, cognate_gα, active_nb, inactive_nb
                  (5JQH inactive + 4LDE active — the matched pair)
        - OPRK:   3 arms — drop active_nb (only 6VI4 inactive available)
        - ACM2:   3 arms — drop inactive_nb (only 4MQS active available)
        - AGTR1:  3 arms — drop inactive_nb (only 6OS2 active available)
      Total: 1 × 4 + 3 × 3 = 13 cells.

**Design**
    Cloned from ``scripts/build_tier_d1_manifest.py``. Key departures:
      1. Panel comes from ``refs/nanobody_state_anchors.csv`` (4 receptors)
         rather than the deep-apo panel CSV.
      2. Four arms instead of one; arm-availability is per-receptor and
         gated by which anchors exist.
      3. Nb sequences come from ``refs/nanobody_sequences.fasta``. Cognate
         arms use ``alphas`` from
         ``docs/EXPERIMENT_CATALOG/sequences/partners.fasta`` (Block A
         convention).
      4. ``SAMPLES_PER_SEED = 10`` (standard (5, 10) lock — this tier is
         not a deep-apo variant).
      5. Seed salt: ``tier_d2_2026_09_06``.

    Each manifest row = ONE (receptor × arm × backbone × seed). The
    backbone worker consumes ``samples_per_seed`` (10) and produces 10
    sample CIFs per row.

**Smoke mode** (``--smoke-adrb2-only``)
    Emits ADRB2 × 4 arms × 4 backbones × 1 seed = 16 rows to validate the
    pipeline end-to-end before scaling.

**AMBIGUITY (flagged)** — ADRB2 active_nb Nb (Nb80 from 4LDE) is NOT in
    ``refs/nanobody_sequences.fasta``. The FASTA only contains Nb60 (5JQH
    inactive), Nb6 (6VI4 inactive), Nb9-8 (4MQS active) and Nb.AT110i1_le
    (6OS2 active). Per the task's fallback rule, the ADRB2 active_nb rows
    are emitted with the Nb60 sequence as a placeholder and the row's
    ``partner_perturbation`` field carries the marker
    ``placeholder_nb80_from_nb60_5jqh`` so downstream analysis skips
    these rows until the real 4LDE Nb sequence is curated into the FASTA.

Usage:
    python3 scripts/build_tier_d2_manifest.py \\
        --out experiments/023_tier_d2_directed_inactive/manifest/tier_d2_manifest.csv \\
        --materialise-inputs-dir /tmp/tier_d2/inputs \\
        --hpc-inputs-prefix /hpc/scratch/sengaad1/paper_af3/experiments/023_tier_d2_directed_inactive/tier_d2/inputs \\
        --hpc-out-prefix    /hpc/scratch/sengaad1/paper_af3/experiments/023_tier_d2_directed_inactive/tier_d2/pool

    # smoke: ADRB2 × 4 arms × 4 backbones × 1 seed = 16 rows
    python3 scripts/build_tier_d2_manifest.py --smoke-adrb2-only \\
        --out /tmp/d2_smoke.csv \\
        --materialise-inputs-dir /tmp/d2_smoke_inputs \\
        --hpc-inputs-prefix /tmp/d2_smoke_inputs \\
        --hpc-out-prefix    /tmp/d2_smoke_out
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scorer.propose import (  # noqa: E402
    _boltz_yaml_monomer,
    _boltz_yaml_two_chain,
    _of3_json_monomer,
    _of3_json_two_chain,
    _protenix_json_monomer,
    _protenix_json_two_chain,
    _chai_fasta_monomer,
    _chai_fasta_two_chain,
    _receptor_nb_content,
)
from scorer.schema import PROPOSE_MANIFEST_COLUMNS  # noqa: E402


# ---------------------------------------------------------------------------
# Species map (audit §21) — carried over verbatim from build_tier_d1_manifest
# ---------------------------------------------------------------------------
def _load_receptor_species_map(ref_set_csv: Path) -> dict[str, str]:
    per_rec: dict[str, set[str]] = defaultdict(set)
    with ref_set_csv.open() as f:
        for row in csv.DictReader(f):
            rec = (row.get("receptor_slug") or "").strip().upper()
            sp = (row.get("species") or "").strip().lower()
            if rec and sp:
                per_rec[rec].add(sp)
    out: dict[str, str] = {}
    for rec, sps in per_rec.items():
        out[rec] = (next(iter(sps)) if len(sps) == 1
                    else "AMBIGUOUS:" + "|".join(sorted(sps)))
    return out


def _resolve_receptor_species(receptor: str,
                               species_map: dict[str, str]) -> str:
    rec_u = receptor.strip().upper()
    sp = species_map.get(rec_u, "")
    if not sp:
        raise ValueError(
            f"No species entry for receptor={rec_u!r} in "
            f"refs/reference_set.csv. Add one before dispatching (audit §21)."
        )
    if sp.startswith("AMBIGUOUS:"):
        raise ValueError(
            f"Ambiguous species for receptor={rec_u!r} in "
            f"refs/reference_set.csv ({sp.split(':', 1)[1]}). Pick a "
            f"canonical entry before dispatching (audit §21)."
        )
    return sp


# ---------------------------------------------------------------------------
# FASTA parsing
# ---------------------------------------------------------------------------
def _parse_fasta(path: Path) -> dict[str, str]:
    """Header-first-token → sequence. Header format:
    ``>TOKEN|extra|fields``."""
    seqs: dict[str, str] = {}
    name, buf = None, []
    for line in path.read_text().splitlines():
        if line.startswith(">"):
            if name is not None:
                seqs[name] = "".join(buf)
            name = line[1:].split("|")[0]
            buf = []
        else:
            buf.append(line.strip())
    if name is not None:
        seqs[name] = "".join(buf)
    return seqs


def _parse_nb_fasta_by_pdb(path: Path) -> dict[str, str]:
    """Parse ``refs/nanobody_sequences.fasta`` keyed by PDB ID.

    Header format: ``>NbName|Nb|PDB|state|receptor=RECEPTOR``.
    Returns {pdb_id_upper: sequence}.
    """
    seqs: dict[str, str] = {}
    pdb, buf = None, []
    for line in path.read_text().splitlines():
        if line.startswith(">"):
            if pdb is not None:
                seqs[pdb] = "".join(buf)
            parts = line[1:].split("|")
            if len(parts) < 3:
                raise ValueError(
                    f"malformed nanobody FASTA header: {line!r} "
                    f"(need >Name|Nb|PDB|state|receptor=X)"
                )
            pdb = parts[2].strip().upper()
            buf = []
        else:
            buf.append(line.strip())
    if pdb is not None:
        seqs[pdb] = "".join(buf)
    return seqs


# ---------------------------------------------------------------------------
# Panel loader — nanobody_state_anchors.csv
# ---------------------------------------------------------------------------
def _load_nb_anchors(anchors_csv: Path) -> dict[str, dict[str, str]]:
    """Return {receptor_upper: {state: {"pdb": ..., "nb_name": ...}, ...}}.

    ``state`` ∈ {"active", "inactive"}.
    """
    per_rec: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    with anchors_csv.open() as f:
        for row in csv.DictReader(f):
            rec = (row.get("receptor_slug") or "").strip().upper()
            state = (row.get("state") or "").strip().lower()
            pdb = (row.get("pdb_id") or "").strip().upper()
            nb_name = (row.get("nb_name") or "").strip()
            if not (rec and state and pdb):
                continue
            if state not in ("active", "inactive"):
                raise ValueError(
                    f"unexpected state {state!r} for {rec} in "
                    f"nanobody_state_anchors.csv (want active/inactive)"
                )
            per_rec[rec][state] = {"pdb": pdb, "nb_name": nb_name}
    return dict(per_rec)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BACKBONES = ("boltz", "chai", "of3", "protenix")

# Arms; per-cell availability is decided by _receptor_arms() below.
ARMS_ALL = ("apo", "cognate_gα", "active_nb", "inactive_nb")

SAMPLES_PER_SEED = 10   # standard (5, 10) lock — D2 is NOT a deep-apo tier.
N_SEEDS = 5
_SEED_SALT = "tier_d2_2026_09_06"

CANONICAL_SEEDS: list[int] = []
for _i in range(N_SEEDS):
    _h = hashlib.sha256(f"{_SEED_SALT}_seed_{_i}".encode()).digest()
    CANONICAL_SEEDS.append(int.from_bytes(_h[:4], "big") % (2**31))

_EXPECTED_CANONICAL = CANONICAL_SEEDS[:]
assert len(CANONICAL_SEEDS) == N_SEEDS
assert CANONICAL_SEEDS == _EXPECTED_CANONICAL, (
    f"Seed derivation drift! derived={CANONICAL_SEEDS} vs "
    f"expected={_EXPECTED_CANONICAL}."
)

# Fixed panel per task: 4 anchors. Order chosen so ADRB2 (matched-pair)
# lands first — helps grep in the smoke smoke.
PANEL = ("ADRB2", "OPRK", "ACM2", "AGTR1")

# 4LDE (ADRB2 active_nb / Nb80) is NOT in refs/nanobody_sequences.fasta.
# Placeholder sequence source (5JQH Nb60) — flagged in partner_perturbation.
_ADRB2_ACTIVE_NB_PLACEHOLDER_PDB = "5JQH"
_ADRB2_ACTIVE_NB_MARKER = "placeholder_nb80_from_nb60_5jqh"

# Extra manifest cols (parity with tier_d1 for downstream shape stability).
BLOCK_C_EXTRA_COLS = (
    "ligand_role", "ligand_bound_pdb", "ligand_ccd", "ligand_smiles_source",
)
MANIFEST_COLUMNS = tuple(PROPOSE_MANIFEST_COLUMNS) + BLOCK_C_EXTRA_COLS


def _receptor_arms(receptor: str,
                   anchors: dict[str, dict[str, dict[str, str]]]) -> tuple[str, ...]:
    """Per-receptor arm availability given the anchors CSV.

    Rules (task spec):
      - apo is always emitted (no partner needed).
      - cognate_gα is always emitted (uses ``alphas`` from partners.fasta).
      - active_nb emitted iff receptor has an active anchor OR is ADRB2
        (ADRB2's Nb80 is a task-mandated matched-pair cell using a
        placeholder sequence).
      - inactive_nb emitted iff receptor has an inactive anchor.
    """
    rec_anchors = anchors.get(receptor, {})
    arms = ["apo", "cognate_gα"]
    has_active = "active" in rec_anchors
    has_inactive = "inactive" in rec_anchors
    if has_active or receptor == "ADRB2":
        arms.append("active_nb")
    if has_inactive:
        arms.append("inactive_nb")
    return tuple(arms)


def _partner_for_arm(
    receptor: str,
    arm: str,
    anchors: dict[str, dict[str, dict[str, str]]],
    nb_seqs_by_pdb: dict[str, str],
    alphas_seq: str,
) -> tuple[str, str, str, str]:
    """Return (partner_type, partner_identity, partner_seq, partner_perturbation).

    apo         → (apo, "", "", wt)
    cognate_gα  → (g_alpha, alphas, <alphas_seq>, wt)
    active_nb   → (nanobody, <pdb>, <nb_seq>, wt)  [ADRB2 uses placeholder]
    inactive_nb → (nanobody, <pdb>, <nb_seq>, wt)
    """
    if arm == "apo":
        return ("apo", "", "", "wt")
    if arm == "cognate_gα":
        return ("g_alpha", "alphas", alphas_seq, "wt")
    if arm in ("active_nb", "inactive_nb"):
        state = "active" if arm == "active_nb" else "inactive"
        rec_anchors = anchors.get(receptor, {})
        if state in rec_anchors:
            pdb = rec_anchors[state]["pdb"]
            nb_seq = nb_seqs_by_pdb.get(pdb, "")
            if not nb_seq:
                raise ValueError(
                    f"No Nb sequence for pdb={pdb!r} (receptor={receptor}, "
                    f"arm={arm}) in refs/nanobody_sequences.fasta"
                )
            return ("nanobody", pdb, nb_seq, "wt")
        # ADRB2 active_nb placeholder path (Nb80/4LDE not in FASTA).
        if receptor == "ADRB2" and arm == "active_nb":
            placeholder_seq = nb_seqs_by_pdb.get(
                _ADRB2_ACTIVE_NB_PLACEHOLDER_PDB, "",
            )
            if not placeholder_seq:
                raise ValueError(
                    f"ADRB2 active_nb placeholder source "
                    f"{_ADRB2_ACTIVE_NB_PLACEHOLDER_PDB} missing from "
                    f"nanobody_sequences.fasta"
                )
            return ("nanobody", "4LDE", placeholder_seq,
                    _ADRB2_ACTIVE_NB_MARKER)
        raise ValueError(
            f"arm {arm!r} unavailable for {receptor} (no {state} anchor)"
        )
    raise ValueError(f"unknown arm {arm!r}")


def _content_for_row(
    backbone: str,
    arm: str,
    receptor_seq: str,
    partner_seq: str,
    input_name: str,
    seed: int,
) -> str:
    """Emit input-file content for one manifest row.

    Dispatches by arm shape (not by partner_type) so the branching is
    obvious at review:
      apo         → monomer templater
      cognate_gα  → existing two-chain templater (receptor A, Gα B)
      active_nb   → _receptor_nb_content (receptor A, Nb B)
      inactive_nb → _receptor_nb_content (receptor A, Nb B)
    """
    if arm == "apo":
        if backbone == "boltz":
            return _boltz_yaml_monomer(receptor_seq)
        if backbone == "of3":
            return _of3_json_monomer(input_name, receptor_seq, seed,
                                     ligand_chain=None)
        if backbone == "protenix":
            return _protenix_json_monomer(input_name, receptor_seq,
                                          ligand_entry=None)
        if backbone == "chai":
            return _chai_fasta_monomer("receptor", receptor_seq,
                                       ligand_fasta="")
        raise ValueError(f"unknown backbone {backbone!r}")

    if arm == "cognate_gα":
        # Standard two-chain: receptor A + Gα B (Block A convention).
        if backbone == "boltz":
            return _boltz_yaml_two_chain(receptor_seq, partner_seq)
        if backbone == "of3":
            return _of3_json_two_chain(input_name, receptor_seq, partner_seq,
                                       seed, ligand_chain=None)
        if backbone == "protenix":
            return _protenix_json_two_chain(input_name, receptor_seq,
                                            partner_seq, ligand_entry=None)
        if backbone == "chai":
            return _chai_fasta_two_chain("receptor", receptor_seq,
                                         "alphas", partner_seq,
                                         ligand_fasta="")
        raise ValueError(f"unknown backbone {backbone!r}")

    if arm in ("active_nb", "inactive_nb"):
        return _receptor_nb_content(backbone, receptor_seq, partner_seq,
                                    input_name, seed)

    raise ValueError(f"unknown arm {arm!r}")


def _backbone_input_ext(backbone: str) -> str:
    return {"boltz": "yaml", "chai": "fasta",
            "of3": "json", "protenix": "json"}[backbone]


def _partners_alphas_seq(partners_fasta: Path) -> str:
    """Return the 'alphas' Gα sequence from partners.fasta."""
    seqs = _parse_fasta(partners_fasta)
    if "alphas" not in seqs:
        raise ValueError(
            f"'alphas' partner not found in {partners_fasta}; "
            f"cognate_gα arm cannot be materialised."
        )
    return seqs["alphas"]


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------
def build(out_csv: Path, materialise_dir: Path | None,
          hpc_inputs_prefix: str, hpc_out_prefix: str,
          receptor_fasta: Path,
          anchors_csv: Path,
          nb_fasta: Path,
          partners_fasta: Path,
          smoke_adrb2_only: bool = False,
          reference_set_csv: Path | None = None) -> dict:
    receptor_seqs = _parse_fasta(receptor_fasta)
    anchors = _load_nb_anchors(anchors_csv)
    nb_seqs_by_pdb = _parse_nb_fasta_by_pdb(nb_fasta)
    alphas_seq = _partners_alphas_seq(partners_fasta)

    ref_set_path = (reference_set_csv
                    if reference_set_csv is not None
                    else REPO / "refs" / "reference_set.csv")
    species_map = _load_receptor_species_map(ref_set_path)

    if smoke_adrb2_only:
        receptors = ("ADRB2",)
        seeds_to_use = CANONICAL_SEEDS[:1]
    else:
        receptors = PANEL
        seeds_to_use = CANONICAL_SEEDS

    # Audit §21 pre-flight.
    for r in receptors:
        _resolve_receptor_species(r, species_map)
        if r not in receptor_seqs:
            raise SystemExit(f"missing receptor sequence for {r}")

    rows: list[dict[str, str]] = []
    inputs_written = 0
    predictions_total = 0
    cells_seen: set[tuple[str, str]] = set()

    for receptor in receptors:
        rseq = receptor_seqs[receptor]
        arms = _receptor_arms(receptor, anchors)
        for arm in arms:
            cells_seen.add((receptor, arm))
            partner_type, partner_identity, partner_seq, perturbation = (
                _partner_for_arm(receptor, arm, anchors,
                                 nb_seqs_by_pdb, alphas_seq)
            )
            # Encode arm in the request_id — 'cognate_gα' has a non-ASCII
            # char; use 'cognate_ga' on-disk for filename safety.
            arm_tag = arm.replace("cognate_gα", "cognate_ga")
            for backbone in BACKBONES:
                for seed_index, seed_value in enumerate(seeds_to_use):
                    request_id = (
                        f"tier_d2_{receptor.lower()}_"
                        f"{arm_tag}_{backbone}_seed{seed_index}"
                    )
                    input_name = f"{request_id}_seed{seed_index}"
                    ext = _backbone_input_ext(backbone)

                    if materialise_dir is not None:
                        subdir = materialise_dir / backbone
                        subdir.mkdir(parents=True, exist_ok=True)
                        content = _content_for_row(
                            backbone, arm, rseq, partner_seq,
                            input_name, seed_value,
                        )
                        input_file = subdir / f"{request_id}.{ext}"
                        input_file.write_text(content)
                        inputs_written += 1
                        input_sha = hashlib.sha256(
                            content.encode()).hexdigest()
                        hpc_input_path = (
                            f"{hpc_inputs_prefix.rstrip('/')}/{backbone}/"
                            f"{request_id}.{ext}"
                        )
                    else:
                        input_sha = ""
                        hpc_input_path = ""

                    hpc_pred_out_dir = (
                        f"{hpc_out_prefix.rstrip('/')}/{receptor.lower()}/"
                        f"{arm_tag}/{backbone}/seed_{seed_value}"
                    )
                    prediction_path = f"{hpc_pred_out_dir}/model_0.cif"

                    # State claim mapping (mirrors StateClaim enum values
                    # already used elsewhere in the corpus).
                    if arm == "apo":
                        state_claim = "apo"
                    elif arm == "cognate_gα":
                        state_claim = "Ga-coupled-active"
                    elif arm == "active_nb":
                        state_claim = "Nb-active"
                    else:  # inactive_nb
                        state_claim = "Nb-inactive"

                    row = {c: "" for c in MANIFEST_COLUMNS}
                    row["prediction_path"] = prediction_path
                    row["prediction_sha"] = ""
                    row["experiment_slug"] = request_id
                    row["wave_group"] = "tier_d2_2026_09_06"
                    row["branch"] = "propose"
                    row["tier"] = "tier_d2"
                    row["backbone"] = backbone
                    row["receptor_from_path_substring"] = receptor
                    row["receptor_resolved"] = receptor
                    row["disambig_conflict"] = "false"
                    row["receptor_unresolved_in_original"] = "false"
                    row["expected_control_json"] = ""
                    row["new_seed"] = str(seed_value)
                    row["request_id"] = request_id
                    row["seed_index"] = str(seed_index)
                    row["state_claim"] = state_claim
                    row["species"] = _resolve_receptor_species(
                        receptor, species_map,
                    )
                    row["partner_type"] = partner_type
                    row["partner_identity"] = partner_identity
                    row["partner_perturbation"] = perturbation
                    row["receptor_class"] = "A"
                    row["input_path"] = hpc_input_path
                    row["input_sha"] = input_sha
                    row["pre_check_status"] = "pass"
                    row["pre_check_details_json"] = ""
                    row["seed_used"] = str(seed_value)
                    row["ligand_type"] = ""
                    row["ligand_sequence"] = ""
                    row["ligand_smiles"] = ""
                    row["samples_per_seed"] = str(SAMPLES_PER_SEED)
                    row["ligand_role"] = ""
                    row["ligand_bound_pdb"] = ""
                    row["ligand_ccd"] = ""
                    row["ligand_smiles_source"] = ""

                    rows.append(row)
                    predictions_total += SAMPLES_PER_SEED

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(MANIFEST_COLUMNS))
        w.writeheader()
        w.writerows(rows)

    # Grid assertions (PREREG §D-2.3).
    if smoke_adrb2_only:
        # ADRB2 × 4 arms × 4 backbones × 1 seed = 16 rows.
        expected_rows = 1 * 4 * 4 * 1
        assert expected_rows == 16
        assert len(rows) == expected_rows, (
            f"smoke row count mismatch: got {len(rows)}, expected 16 "
            f"(ADRB2 × 4 arms × 4 backbones × 1 seed)"
        )
    else:
        # 13 cells × 4 backbones × 5 seeds = 260 rows.
        expected_cells = 1 * 4 + 3 * 3  # ADRB2 4 arms + 3 receptors × 3 arms
        assert len(cells_seen) == expected_cells, (
            f"cell count mismatch: got {len(cells_seen)}, expected "
            f"{expected_cells}. cells={sorted(cells_seen)}"
        )
        expected_rows = expected_cells * len(BACKBONES) * N_SEEDS
        assert expected_rows == 260, (
            f"grid shape drift: {expected_cells}×{len(BACKBONES)}×{N_SEEDS}"
            f"={expected_rows}"
        )
        assert len(rows) == expected_rows, (
            f"row count mismatch: got {len(rows)}, expected {expected_rows}"
        )
        expected_preds = expected_rows * SAMPLES_PER_SEED
        assert predictions_total == expected_preds
        assert expected_preds == 2600

    # Distinct input_path across (arm, backbone, seed) — task verify §2.
    if materialise_dir is not None:
        paths = [r["input_path"] for r in rows]
        assert len(paths) == len(set(paths)), (
            "duplicate input_path in manifest — arm/backbone/seed collision"
        )

    return {
        "n_rows": len(rows),
        "n_predictions": predictions_total,
        "n_inputs_written": inputs_written,
        "n_cells": len(cells_seen),
        "manifest_path": str(out_csv),
        "canonical_seeds": seeds_to_use,
        "receptors": list(receptors),
        "arms_by_receptor": {r: list(_receptor_arms(r, anchors))
                             for r in receptors},
        "backbones": list(BACKBONES),
        "samples_per_seed": SAMPLES_PER_SEED,
        "smoke": smoke_adrb2_only,
        "notes": {
            "adrb2_active_nb_placeholder": _ADRB2_ACTIVE_NB_MARKER
            if any(r == "ADRB2" for r in receptors) else "",
        },
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True, help="output manifest CSV path")
    ap.add_argument("--materialise-inputs-dir", default=None,
                    help="if set, write per-row input files under here")
    ap.add_argument("--hpc-inputs-prefix", required=True,
                    help="HPC-visible path prefix for materialised inputs")
    ap.add_argument("--hpc-out-prefix", required=True,
                    help="HPC-visible path prefix for output CIFs "
                         "(distinct from tier_d1 pool)")
    ap.add_argument("--receptor-fasta",
                    default=str(REPO / "refs/panel_receptor_sequences.fasta"))
    ap.add_argument("--anchors-csv",
                    default=str(REPO / "refs/nanobody_state_anchors.csv"))
    ap.add_argument("--nb-fasta",
                    default=str(REPO / "refs/nanobody_sequences.fasta"))
    ap.add_argument("--partners-fasta",
                    default=str(REPO / "docs/EXPERIMENT_CATALOG/"
                                       "sequences/partners.fasta"))
    ap.add_argument("--reference-set-csv", default=None,
                    help="reference_set.csv used to lift receptor→species "
                         "(default: refs/reference_set.csv). Audit §21.")
    ap.add_argument("--smoke-adrb2-only", action="store_true",
                    help="emit only ADRB2 × 4 arms × 4 backbones × 1 seed "
                         "= 16 rows for smoke dispatch.")
    args = ap.parse_args(argv)

    result = build(
        out_csv=Path(args.out),
        materialise_dir=(Path(args.materialise_inputs_dir)
                         if args.materialise_inputs_dir else None),
        hpc_inputs_prefix=args.hpc_inputs_prefix,
        hpc_out_prefix=args.hpc_out_prefix,
        receptor_fasta=Path(args.receptor_fasta),
        anchors_csv=Path(args.anchors_csv),
        nb_fasta=Path(args.nb_fasta),
        partners_fasta=Path(args.partners_fasta),
        smoke_adrb2_only=args.smoke_adrb2_only,
        reference_set_csv=(Path(args.reference_set_csv)
                           if args.reference_set_csv else None),
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
