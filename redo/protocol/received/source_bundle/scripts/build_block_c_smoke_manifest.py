"""Build Block C 400-prediction smoke manifest + materialise inputs.

**Purpose**
    Emit the 400-row (2 receptors × 5 ligand states × 2 partner arms
    × 4 backbones × 1 seed × 5 samples) manifest at
    ``experiments/020_block_c_ligand_pharmacology/manifest/smoke_manifest.csv``
    and, when ``--materialise-inputs-dir`` is given, write the 400
    per-row backbone-input files under that dir.

**Design**
    Reuses ``scorer.propose._row_input_content`` per row so ligand
    plumbing (Boltz ``ligand: smiles:``, OF3 ``molecule_type=LIGAND``,
    Protenix ``sequences: ligand:``, Chai ``>ligand|smiles``) is
    identical to the frozen Block A / Block B pipeline.

    Receptor sequences pulled from
    ``refs/panel_receptor_sequences.fasta`` (matching Block A/B
    empirical convention — NOT the GPCRdb WT fetch used by
    ``scorer.propose.materialise_inputs`` since we do not depend on the
    live GPCRdb API for a smoke).

    Partner sequences pulled from
    ``docs/EXPERIMENT_CATALOG/sequences/partners.fasta``.

    Ligand rows drawn from ``refs/ligand_set.csv`` (post-1.1 CCD-source).

**Column schema**
    Strict superset of Block B's manifest schema
    (``scorer.schema.PROPOSE_MANIFEST_COLUMNS``, 30 cols) plus 4 Block-C
    additions:

        ligand_role         ∈ {none, decoy_lig, neutral_antagonist,
                                inverse_agonist, full_agonist}
        ligand_bound_pdb    ligand co-crystal PDB (may be empty)
        ligand_ccd          CCD 3-letter code (may be empty)
        ligand_smiles_source e.g. "CCD:3NYA:JTZ" or "PubChem:CID10117987"

**Cognate partner** = ``partner_type=g_alpha, partner_identity=alphas``
    (Gα alone, matching Block A/B convention per coordinator Decision 2
    of 2026-09-04). Apo = ``partner_type=apo, partner_identity=""``.

Usage:
    python3 scripts/build_block_c_smoke_manifest.py \\
        --out experiments/020_block_c_ligand_pharmacology/manifest/smoke_manifest.csv \\
        --materialise-inputs-dir /tmp/block_c_smoke/inputs \\
        --hpc-inputs-prefix /hpc/scratch/sengaad1/paper_af3/experiments/020_block_c_ligand_pharmacology/smoke/inputs \\
        --hpc-out-prefix    /hpc/scratch/sengaad1/paper_af3/experiments/020_block_c_ligand_pharmacology/smoke/pool \\
        --seed-value 1544158306
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


RECEPTORS = ("ADRB2", "AA2AR")
LIGAND_STATES = ("none", "decoy_lig", "neutral_antagonist",
                 "inverse_agonist", "full_agonist")
BACKBONES = ("boltz", "chai", "of3", "protenix")
PARTNER_ARMS = ("apo", "cognate")
SAMPLES_PER_SEED = 5
COGNATE_PARTNER_IDENTITY = "alphas"  # Decision 2 — Gα alone

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
    """Emit backbone-input file content (string) for one row.

    Mirrors scorer.propose._row_input_content but with explicit
    (receptor_seq, partner_seq) — we bypass the live GPCRdb lookup.
    """
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
          seed_value: int,
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

    for receptor in RECEPTORS:
        rseq = receptor_seqs[receptor]
        for ligand_role in LIGAND_STATES:
            lig_row = ligand_set.get((receptor, ligand_role), {})
            smiles = (lig_row.get("smiles") or "").strip()
            ccd_code = (lig_row.get("ccd_code") or "").strip()
            bound_pdb = (lig_row.get("bound_pdb") or "").strip()
            smiles_source = (lig_row.get("smiles_source") or "").strip()
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
                    # request_id uniquely identifies (receptor, ligand,
                    # arm, backbone) — the smoke has one seed_index=0
                    request_id = (f"blockc_smoke_{receptor.lower()}_"
                                  f"{ligand_role}_{arm}_{backbone}")
                    input_name = f"{request_id}_seed0"
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
                        input_sha = hashlib.sha256(content.encode()).hexdigest()
                        # HPC-visible path (worker reads from HPC scratch)
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
                        f"{ligand_role}/{arm}/{backbone}/seed_{seed_value}"
                    )
                    prediction_path = f"{hpc_pred_out_dir}/model_0.cif"

                    row = {c: "" for c in MANIFEST_COLUMNS}
                    row["prediction_path"] = prediction_path
                    row["prediction_sha"] = ""
                    row["experiment_slug"] = request_id
                    row["wave_group"] = "block_c_smoke_2026_09_04"
                    row["branch"] = "propose"
                    row["tier"] = ""
                    row["backbone"] = backbone
                    row["receptor_from_path_substring"] = receptor
                    row["receptor_resolved"] = receptor
                    row["disambig_conflict"] = "false"
                    row["receptor_unresolved_in_original"] = "false"
                    row["expected_control_json"] = ""
                    row["new_seed"] = str(seed_value)
                    row["request_id"] = request_id
                    row["seed_index"] = "0"
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
                    # Block C additions
                    row["ligand_role"] = ligand_role
                    row["ligand_bound_pdb"] = bound_pdb
                    row["ligand_ccd"] = ccd_code
                    row["ligand_smiles_source"] = smiles_source

                    rows.append(row)

    # Emit manifest
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(MANIFEST_COLUMNS))
        w.writeheader()
        w.writerows(rows)

    return {
        "n_rows": len(rows),
        "n_inputs_written": inputs_written,
        "manifest_path": str(out_csv),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True, help="output manifest CSV path")
    ap.add_argument("--materialise-inputs-dir", default=None,
                    help="if set, write 400 per-row input files under here")
    ap.add_argument("--hpc-inputs-prefix", required=True,
                    help="HPC-visible path prefix where materialised inputs land")
    ap.add_argument("--hpc-out-prefix", required=True,
                    help="HPC-visible path prefix for output CIFs")
    ap.add_argument("--seed-value", type=int, default=1544158306,
                    help="deterministic seed for all 400 rows (one seed × 5 samples)")
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
        seed_value=args.seed_value,
        receptor_fasta=Path(args.receptor_fasta),
        partners_fasta=Path(args.partners_fasta),
        ligand_csv=Path(args.ligand_csv),
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
