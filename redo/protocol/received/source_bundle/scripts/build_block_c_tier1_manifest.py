"""Build Block C Tier 1 manifest — 14,800-prediction pharmacology ladder.

**Purpose**
    Emit the 1,480-row manifest at
    ``experiments/020_block_c_ligand_pharmacology/manifest/tier1_manifest.csv``
    and, when ``--materialise-inputs-dir`` is given, write the 1,480
    per-row backbone-input files under that dir (one per manifest row;
    the backbone generates 10 samples per row from a single seed).

    Nominal grid (full):
      8 receptors × 5 ligand states × 2 partner arms × 4 backbones
      × 5 seeds × 10 samples = 16,000 predictions.

    Effective grid (after NA-row exclusion per amendment § C-2):
      OX2R, 5HT1B, AA1R have `activity_class=NA` on their
      inverse_agonist row (no clean CAM-assay-classified inverse
      agonist with < 100 nM affinity meeting the amendment criteria).
      These 3 (receptor × role) tuples × 2 arms × 4 backbones × 5
      seeds = 120 manifest rows are skipped from dispatch: their
      backbone input would collapse to the receptor's `none` state
      (blank SMILES → apo-shaped input), producing duplicate
      prediction_sha at the queue builder AND masquerading as
      pharmacology signal on a row that carried no ligand.

      Effective totals: 296 cells → 1,480 manifest rows → 14,800
      predictions. P3 (inverse < antagonist) becomes a 5-receptor
      test rather than an 8-receptor test — pre-registered per
      amendment § C-6 line "P3 ... untestable for OX2R, 5HT1B ...
      NA rows".

**Design**
    Adapts scripts/build_block_c_smoke_manifest.py (which shipped 400
    predictions from 2 receptors × 5 states × 2 arms × 4 backbones × 1
    seed × 5 samples = 80 manifest rows). Tier 1 scales to 8 receptors
    and 5 seeds × 10 samples per cell → 320 cells, 5 rows per cell,
    1,600 manifest rows, 16,000 predictions.

    Each manifest row corresponds to ONE backbone invocation with ONE
    seed. The backbone worker reads ``new_seed`` and ``samples_per_seed``
    from the row and produces 10 sample CIFs (samples share the seed
    per backbone convention — Boltz/Chai/Protenix/OF3 all interpret
    ``samples`` as diffusion-sampled realisations of the same seed).

    Cross-cell seed sharing: the same 5 canonical seed values are used
    across every (receptor, state, arm, backbone) cell. This is not
    for paired analysis (parent PREREG §3 forbids cross-arm row
    pairing) but for provenance simplicity — a Tier-1 seed index maps
    to a stable seed integer regardless of which cell it came from.

    Deterministic derivation:
      seed_i = int.from_bytes(sha256(f'block_c_tier1_2026_09_04_seed_{i}')[:4], 'big') % (2**31)
      → seeds = [554068910, 2095051020, 1854187058, 189590006, 1623169759]

**Panel** (locked, plan §3.3 + PREREG amendment § C-1.1)
    ADRB2, DRD3, AA2AR, ACM4, OX2R, ACM2, 5HT1B, AA1R.
    5 discriminators (ADRB2, DRD3, AA2AR, ACM4, OX2R) + 3 controls
    (ACM2, 5HT1B, AA1R).

**Pre-registered per-backbone exclusion** (Step 3, 2026-09-04)
    ADRB2 × Chai is P1-excluded (apo active fraction = 1.00 on Block B
    landing, ceiling-locked). This is a REPORTING exclusion — the
    manifest still emits ADRB2 × Chai × apo rows so downstream analysis
    can verify the observation prospectively. P0 / P2 / P3 / P4 / P6 /
    P7 are unaffected; only P1's ADRB2 × Chai cell is skipped in the
    fire-gate evaluation. See ceiling_headroom_2026_09_04.csv.

**Cognate partner** = ``partner_type=g_alpha, partner_identity=alphas``
    (Gα alone, matching Block A/B convention). Apo = no partner.

Usage:
    python3 scripts/build_block_c_tier1_manifest.py \\
        --out experiments/020_block_c_ligand_pharmacology/manifest/tier1_manifest.csv \\
        --materialise-inputs-dir /tmp/block_c_tier1/inputs \\
        --hpc-inputs-prefix /hpc/scratch/sengaad1/paper_af3/experiments/020_block_c_ligand_pharmacology/tier1/inputs \\
        --hpc-out-prefix    /hpc/scratch/sengaad1/paper_af3/experiments/020_block_c_ligand_pharmacology/tier1/pool
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scorer.propose import (  # noqa: E402
    _boltz_yaml_monomer, _boltz_yaml_two_chain, _boltz_ligand_block,
    _of3_json_monomer, _of3_json_two_chain, _of3_ligand_chain,
    _protenix_json_monomer, _protenix_json_two_chain, _protenix_ligand_entry,
    _chai_fasta_monomer, _chai_fasta_two_chain, _chai_ligand_fasta,
)
from scorer.schema import PROPOSE_MANIFEST_COLUMNS  # noqa: E402


RECEPTORS = ("ADRB2", "DRD3", "AA2AR", "ACM4",
             "OX2R", "ACM2", "5HT1B", "AA1R")
LIGAND_STATES = ("none", "decoy_lig", "neutral_antagonist",
                 "inverse_agonist", "full_agonist")
BACKBONES = ("boltz", "chai", "of3", "protenix")
PARTNER_ARMS = ("apo", "cognate")
COGNATE_PARTNER_IDENTITY = "alphas"

SAMPLES_PER_SEED = 10
N_SEEDS = 5
CANONICAL_SEEDS = [554068910, 2095051020, 1854187058, 189590006, 1623169759]
_SEED_SALT = "block_c_tier1_2026_09_04"

# Sanity check — derive seeds and compare to the pinned list. If someone
# renames _SEED_SALT (e.g. re-uses this script for Tier 2 without
# updating), the assert fires rather than emitting a manifest with the
# wrong seeds silently.
_derived = []
for _i in range(N_SEEDS):
    _h = hashlib.sha256(f'{_SEED_SALT}_seed_{_i}'.encode()).digest()
    _derived.append(int.from_bytes(_h[:4], 'big') % (2**31))
assert _derived == CANONICAL_SEEDS, (
    f"Seed derivation drift! derived={_derived} vs pinned={CANONICAL_SEEDS}. "
    f"If you meant to re-derive, update CANONICAL_SEEDS."
)

BLOCK_C_EXTRA_COLS = (
    "ligand_role", "ligand_bound_pdb", "ligand_ccd", "ligand_smiles_source",
)
MANIFEST_COLUMNS = tuple(PROPOSE_MANIFEST_COLUMNS) + BLOCK_C_EXTRA_COLS


def _parse_fasta(path: Path) -> dict[str, str]:
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


def _load_ligand_set(csv_path: Path) -> dict[tuple[str, str], dict]:
    """Load refs/ligand_set.csv keyed by (receptor, ligand_role)."""
    out: dict[tuple[str, str], dict] = {}
    with csv_path.open() as f:
        for row in csv.DictReader(f):
            key = (row["receptor"].strip().upper(),
                   row["ligand_role"].strip())
            out[key] = row
    return out


def _content_for_row(backbone: str, apo: bool,
                     receptor_seq: str, partner_seq: str,
                     ligand_type: str, ligand_smiles: str,
                     input_name: str, seed: int) -> str:
    """Emit backbone-input file content (string) for one row."""
    if backbone == "boltz":
        base = _boltz_yaml_monomer(receptor_seq) if apo else \
               _boltz_yaml_two_chain(receptor_seq, partner_seq)
        return base + _boltz_ligand_block(ligand_type, "", ligand_smiles,
                                          ligand_chain_id="L")
    if backbone == "of3":
        lig = _of3_ligand_chain(ligand_type, "", ligand_smiles)
        if apo:
            return _of3_json_monomer(input_name, receptor_seq, seed,
                                     ligand_chain=lig)
        return _of3_json_two_chain(input_name, receptor_seq, partner_seq,
                                   seed, ligand_chain=lig)
    if backbone == "protenix":
        lig = _protenix_ligand_entry(ligand_type, "", ligand_smiles)
        if apo:
            return _protenix_json_monomer(input_name, receptor_seq,
                                          ligand_entry=lig)
        return _protenix_json_two_chain(input_name, receptor_seq,
                                        partner_seq, ligand_entry=lig)
    if backbone == "chai":
        lig_fa = _chai_ligand_fasta(ligand_type, "", ligand_smiles,
                                    name="lig")
        if apo:
            return _chai_fasta_monomer("receptor", receptor_seq,
                                       ligand_fasta=lig_fa)
        return _chai_fasta_two_chain("receptor", receptor_seq,
                                     "partner", partner_seq,
                                     ligand_fasta=lig_fa)
    raise ValueError(f"unknown backbone {backbone!r}")


def _backbone_input_ext(backbone: str) -> str:
    return {"boltz": "yaml", "chai": "fasta",
            "of3": "json", "protenix": "json"}[backbone]


def build(out_csv: Path, materialise_dir: Path | None,
          hpc_inputs_prefix: str, hpc_out_prefix: str,
          receptor_fasta: Path, partners_fasta: Path,
          ligand_csv: Path) -> dict:
    receptor_seqs = _parse_fasta(receptor_fasta)
    partner_seqs = _parse_fasta(partners_fasta)
    ligand_set = _load_ligand_set(ligand_csv)

    for r in RECEPTORS:
        if r not in receptor_seqs:
            raise SystemExit(f"missing receptor sequence for {r}")
    if COGNATE_PARTNER_IDENTITY not in partner_seqs:
        raise SystemExit(f"missing partner {COGNATE_PARTNER_IDENTITY}")

    rows: list[dict[str, str]] = []
    inputs_written = 0
    predictions_total = 0
    skipped_na: list[tuple[str, str]] = []

    for receptor in RECEPTORS:
        rseq = receptor_seqs[receptor]
        for ligand_role in LIGAND_STATES:
            lig_row = ligand_set.get((receptor, ligand_role), {})
            smiles = (lig_row.get("smiles") or "").strip()
            ccd_code = (lig_row.get("ccd_code") or "").strip()
            bound_pdb = (lig_row.get("bound_pdb") or "").strip()
            smiles_source = (lig_row.get("smiles_source") or "").strip()
            activity_class = (lig_row.get("activity_class") or "").strip()

            # Skip rows where the ligand-set entry is NA (no clean
            # ligand for this receptor × role combination per amendment
            # § C-2 / § C-13(f)). Currently affects: OX2R inverse,
            # 5HT1B inverse, AA1R inverse. If we emitted these, the
            # backbone input would be identical to the receptor's `none`
            # state (blank SMILES → apo-shaped input), producing a
            # duplicate prediction_sha and (worse) a manifest row
            # claiming pharmacology signal from a row that carried none.
            if activity_class == "NA" or (ligand_role != "none" and not smiles):
                skipped_na.append((receptor, ligand_role))
                continue

            ligand_type = ("small_molecule" if smiles and ligand_role != "none"
                           else "")

            for arm in PARTNER_ARMS:
                apo = (arm == "apo")
                if apo:
                    partner_type = "apo"
                    partner_identity = ""
                    partner_seq = ""
                else:
                    partner_type = "g_alpha"
                    partner_identity = COGNATE_PARTNER_IDENTITY
                    partner_seq = partner_seqs[COGNATE_PARTNER_IDENTITY]

                for backbone in BACKBONES:
                    for seed_index, seed_value in enumerate(CANONICAL_SEEDS):
                        # request_id uniquely identifies (receptor,
                        # ligand, arm, backbone, seed). seed_index makes
                        # the request_id unique per manifest row.
                        request_id = (
                            f"blockc_tier1_{receptor.lower()}_"
                            f"{ligand_role}_{arm}_{backbone}_"
                            f"seed{seed_index}"
                        )
                        input_name = f"{request_id}_seed{seed_index}"
                        ext = _backbone_input_ext(backbone)

                        # Materialise input file
                        if materialise_dir is not None:
                            subdir = materialise_dir / backbone
                            subdir.mkdir(parents=True, exist_ok=True)
                            content = _content_for_row(
                                backbone, apo, rseq, partner_seq,
                                ligand_type, smiles,
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

                        # HPC-visible output tree — one dir per (row, seed)
                        hpc_pred_out_dir = (
                            f"{hpc_out_prefix.rstrip('/')}/{receptor.lower()}/"
                            f"{ligand_role}/{arm}/{backbone}/"
                            f"seed_{seed_value}"
                        )
                        prediction_path = f"{hpc_pred_out_dir}/model_0.cif"

                        row = {c: "" for c in MANIFEST_COLUMNS}
                        row["prediction_path"] = prediction_path
                        row["prediction_sha"] = ""
                        row["experiment_slug"] = request_id
                        row["wave_group"] = "block_c_tier1_2026_09_04"
                        row["branch"] = "propose"
                        row["tier"] = "tier1"
                        row["backbone"] = backbone
                        row["receptor_from_path_substring"] = receptor
                        row["receptor_resolved"] = receptor
                        row["disambig_conflict"] = "false"
                        row["receptor_unresolved_in_original"] = "false"
                        row["expected_control_json"] = ""
                        row["new_seed"] = str(seed_value)
                        row["request_id"] = request_id
                        row["seed_index"] = str(seed_index)
                        row["state_claim"] = "Ga-coupled-active"
                        row["species"] = "human"
                        row["partner_type"] = partner_type
                        row["partner_identity"] = partner_identity
                        row["partner_perturbation"] = "wt"
                        row["receptor_class"] = "A"
                        row["input_path"] = hpc_input_path
                        row["input_sha"] = input_sha
                        row["pre_check_status"] = "pass"
                        row["pre_check_details_json"] = ""
                        row["seed_used"] = str(seed_value)
                        row["ligand_type"] = ligand_type
                        row["ligand_sequence"] = ""
                        row["ligand_smiles"] = smiles
                        row["samples_per_seed"] = str(SAMPLES_PER_SEED)
                        row["ligand_role"] = ligand_role
                        row["ligand_bound_pdb"] = bound_pdb
                        row["ligand_ccd"] = ccd_code
                        row["ligand_smiles_source"] = smiles_source

                        rows.append(row)
                        predictions_total += SAMPLES_PER_SEED

    # Emit manifest
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(MANIFEST_COLUMNS))
        w.writeheader()
        w.writerows(rows)

    # NA rows are skipped per receptor × role (not per arm/backbone/seed);
    # each unique (receptor, role) skip removes 1 role from that receptor's
    # cell grid → 1 role × 2 arms × 4 backbones = 8 cells removed per
    # unique (receptor, role). Then × 5 seeds = 40 manifest rows.
    unique_na = set(skipped_na)
    n_cells_full = (len(RECEPTORS) * len(LIGAND_STATES)
                    * len(PARTNER_ARMS) * len(BACKBONES))
    n_cells_dropped = (len(unique_na)
                       * len(PARTNER_ARMS) * len(BACKBONES))
    n_cells = n_cells_full - n_cells_dropped
    expected_rows = n_cells * N_SEEDS
    expected_preds = expected_rows * SAMPLES_PER_SEED
    assert len(rows) == expected_rows, (
        f"row count mismatch: got {len(rows)}, expected {expected_rows} "
        f"({n_cells} cells × {N_SEEDS} seeds; {len(unique_na)} NA "
        f"(receptor, role) skipped)"
    )
    assert predictions_total == expected_preds, (
        f"prediction count mismatch: got {predictions_total}, expected {expected_preds}"
    )

    return {
        "n_rows": len(rows),
        "n_cells": n_cells,
        "n_cells_full_grid": n_cells_full,
        "n_cells_dropped_na": n_cells_dropped,
        "unique_na_rows": sorted(unique_na),
        "n_predictions": predictions_total,
        "n_inputs_written": inputs_written,
        "manifest_path": str(out_csv),
        "canonical_seeds": CANONICAL_SEEDS,
        "receptors": list(RECEPTORS),
        "ligand_states": list(LIGAND_STATES),
        "partner_arms": list(PARTNER_ARMS),
        "backbones": list(BACKBONES),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True, help="output manifest CSV path")
    ap.add_argument("--materialise-inputs-dir", default=None,
                    help="if set, write 1600 per-row input files under here")
    ap.add_argument("--hpc-inputs-prefix", required=True,
                    help="HPC-visible path prefix where materialised inputs land")
    ap.add_argument("--hpc-out-prefix", required=True,
                    help="HPC-visible path prefix for output CIFs")
    ap.add_argument("--receptor-fasta",
                    default=str(REPO / "refs/panel_receptor_sequences.fasta"))
    ap.add_argument("--partners-fasta",
                    default=str(REPO / "docs/EXPERIMENT_CATALOG/sequences/partners.fasta"))
    ap.add_argument("--ligand-csv",
                    default=str(REPO / "refs/ligand_set.csv"))
    args = ap.parse_args(argv)

    result = build(
        out_csv=Path(args.out),
        materialise_dir=(Path(args.materialise_inputs_dir)
                         if args.materialise_inputs_dir else None),
        hpc_inputs_prefix=args.hpc_inputs_prefix,
        hpc_out_prefix=args.hpc_out_prefix,
        receptor_fasta=Path(args.receptor_fasta),
        partners_fasta=Path(args.partners_fasta),
        ligand_csv=Path(args.ligand_csv),
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
