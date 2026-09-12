"""Build Block C Tier 3 manifest — 48,000-prediction panel-scale confirmation.

**Purpose**
    Emit the 4,800-row manifest at
    ``experiments/021_block_c_tier3_pharmacology/manifest/tier3_manifest.csv``
    and, when ``--materialise-inputs-dir`` is given, write the 4,800
    per-row backbone-input files under that dir.

    Nominal grid (locked, plan §5 + amendment §C-1):
      40 Class A receptors × 3 ligand states × 2 partner arms × 4 backbones
      × 5 seeds × 10 samples = 48,000 predictions.

    Effective grid after NA-row exclusion (Stage 1 curation):
      A subset of (receptor × role) cells are marked activity_class=NA in
      refs/ligand_set_tier3.csv (Stage 1) — e.g. B1B1U5/OPSD/FSHR/LSHR for
      decoy_lig (per Stage 3 rules); many aminergic + peptide receptors
      for neutral_antagonist. These are skipped from dispatch.

**Design**
    Cloned from scripts/build_block_c_tier1_manifest.py. Six constant
    changes: RECEPTORS (8→40), LIGAND_STATES (5→3, drop `none` and
    `inverse_agonist`), _SEED_SALT (tier1→tier3), CANONICAL_SEEDS
    (re-derived), wave_group / tier / request_id prefixes.

    `none` state dropped: Block B has clean (5,10) apo baselines per
    receptor per backbone already; analysis script joins Block B apo
    baselines by (receptor, backbone, seed) rather than duplicating
    ~11 h wall for Tier 3 none-state.

    `inverse_agonist` state dropped: only 5 of 40 receptors have clean
    inverse-ag crystal; P3 (inverse < antag) untestable at panel scale.

    Each manifest row corresponds to ONE backbone invocation with ONE
    seed. The backbone worker reads ``new_seed`` and ``samples_per_seed``
    from the row and produces 10 sample CIFs.

    Deterministic seed derivation:
      seed_i = int.from_bytes(sha256(f'block_c_tier3_2026_09_04_seed_{i}')[:4], 'big') % (2**31)
      → seeds = [524593679, 1607363019, 1779092953, 1393717870, 262604171]

**Panel** (locked in refs/tier3_panel.csv, 40 Class A original)
    5HT1B, 5HT2C, 5HT5A, AA1R, AA2AR, ACM1, ACM2, ACM4, ADA2A, ADRB1,
    ADRB2, AGTR1, APJ, B1B1U5, CCKAR, CCR5, CNR1, CNR2, CXCR2, CXCR4,
    DRD2, DRD3, EDNRA, EDNRB, FSHR, GHSR, GRPR, HRH1, HRH3, LPAR1, LSHR,
    LT4R1, MCHR1, NPY1R, NPY2R, OPRD, OPRK, OPRX, OPSD, OX2R.

**Cognate partner** = ``partner_type=g_alpha, partner_identity=alphas``
    (Gα alone, matching Block A/B convention). Apo = no partner.

**Ligand set** loaded from BOTH refs/ligand_set.csv (Tier 1's 8 receptors)
    AND refs/ligand_set_tier3.csv (32 new receptors). Union keyed by
    (receptor, ligand_role).

Usage:
    python3 scripts/build_block_c_tier3_manifest.py \\
        --out experiments/021_block_c_tier3_pharmacology/manifest/tier3_manifest.csv \\
        --materialise-inputs-dir /tmp/block_c_tier3/inputs \\
        --hpc-inputs-prefix /hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/tier3/inputs \\
        --hpc-out-prefix    /hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/tier3/pool
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
    _boltz_yaml_monomer, _boltz_yaml_two_chain, _boltz_ligand_block,
    _of3_json_monomer, _of3_json_two_chain, _of3_ligand_chain,
    _protenix_json_monomer, _protenix_json_two_chain, _protenix_ligand_entry,
    _chai_fasta_monomer, _chai_fasta_two_chain, _chai_ligand_fasta,
)
from scorer.schema import PROPOSE_MANIFEST_COLUMNS  # noqa: E402

# Tier 3 decoys live in the DECOY_SMILES / PEPTIDE_DECOYS dicts in
# build_block_c_decoys.py (not in refs/ligand_set_tier3.csv). Import them
# so the manifest builder can construct decoy_lig rows in-memory.
from scripts.build_block_c_decoys import (  # noqa: E402
    DECOY_SMILES, PEPTIDE_DECOYS, TIER3_NA_RECEPTORS, scramble_peptide,
    min_hamming_for, seed_from,
)


# Audit §21: species must be lifted from refs/reference_set.csv (not
# hardcoded "human") for non-human panel receptors (OPSD/bovin,
# B1B1U5/9arac). See scripts/build_block_c_tier3_rescore_manifest.py
# for the sibling helper — kept in sync.
def _load_receptor_species_map(ref_set_csv: Path) -> dict[str, str]:
    """{receptor_upper: species_lower} from reference_set.csv; ambiguous
    (multi-species) receptors map to ``"AMBIGUOUS:sp1|sp2|..."``.
    Empty species rows are skipped."""
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
    """Return the species for a panel receptor. Raises if unknown or
    ambiguous — the caller must fix the reference_set entry first."""
    rec_u = receptor.strip().upper()
    sp = species_map.get(rec_u, "")
    if not sp:
        raise ValueError(
            f"No species entry for receptor={rec_u!r} in "
            f"refs/reference_set.csv. Add one before dispatching a "
            f"manifest that includes this receptor (audit §21)."
        )
    if sp.startswith("AMBIGUOUS:"):
        raise ValueError(
            f"Ambiguous species for receptor={rec_u!r} in "
            f"refs/reference_set.csv ({sp.split(':', 1)[1]}). Pick a "
            f"canonical entry before dispatching (audit §21)."
        )
    return sp


# 40 Class A original panel, sorted alphabetically per refs/tier3_panel.csv
RECEPTORS = (
    "5HT1B", "5HT2C", "5HT5A", "AA1R", "AA2AR",
    "ACM1", "ACM2", "ACM4", "ADA2A", "ADRB1",
    "ADRB2", "AGTR1", "APJ", "B1B1U5", "CCKAR",
    "CCR5", "CNR1", "CNR2", "CXCR2", "CXCR4",
    "DRD2", "DRD3", "EDNRA", "EDNRB", "FSHR",
    "GHSR", "GRPR", "HRH1", "HRH3", "LPAR1",
    "LSHR", "LT4R1", "MCHR1", "NPY1R", "NPY2R",
    "OPRD", "OPRK", "OPRX", "OPSD", "OX2R",
)
assert len(RECEPTORS) == 40, f"panel-count drift: {len(RECEPTORS)}"

LIGAND_STATES = ("decoy_lig", "neutral_antagonist", "full_agonist")
BACKBONES = ("boltz", "chai", "of3", "protenix")
PARTNER_ARMS = ("apo", "cognate")
COGNATE_PARTNER_IDENTITY = "alphas"

SAMPLES_PER_SEED = 10
N_SEEDS = 5
CANONICAL_SEEDS = [524593679, 1607363019, 1779092953, 1393717870, 262604171]
_SEED_SALT = "block_c_tier3_2026_09_04"

# Sanity check — derive seeds and compare. If someone renames _SEED_SALT
# (e.g. cloning to Tier 4), the assert fires rather than emitting a
# manifest with the wrong seeds silently.
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


def _load_ligand_set(csv_paths: list[Path]) -> dict[tuple[str, str], dict]:
    """Load ligand rows from one or more CSVs, keyed by (receptor, ligand_role).

    Later CSVs override earlier ones on collision (union with last-wins).

    Also injects decoy_lig rows for every receptor in DECOY_SMILES /
    PEPTIDE_DECOYS that isn't already covered by a CSV row. NA-listed
    Tier 3 receptors (B1B1U5, OPSD, FSHR, LSHR) get NA decoy rows.
    """
    out: dict[tuple[str, str], dict] = {}
    for csv_path in csv_paths:
        with csv_path.open() as f:
            for row in csv.DictReader(f):
                key = (row["receptor"].strip().upper(),
                       row["ligand_role"].strip())
                out[key] = row
    # Inject decoy_lig rows for Tier 3 receptors not already in CSVs.
    for slug, (smi, name, source) in DECOY_SMILES.items():
        key = (slug.upper(), "decoy_lig")
        if key not in out:
            out[key] = {
                "receptor": slug.upper(),
                "ligand_role": "decoy_lig",
                "is_peptide": "FALSE",
                "smiles": smi,
                "peptide_sequence": "",
                "iupac_name": name,
                "bound_pdb": "",
                "activity_class": "decoy_none_known",
                "notes": f"decoy_lig from DECOY_SMILES; {source}",
                "ccd_code": "",
                "ccd_smiles": "",
                "smiles_source": f"scripts/build_block_c_decoys.py::DECOY_SMILES[{slug!r}]",
            }
    # Inject peptide decoys.
    for slug, (native_seq, common_name, salt) in PEPTIDE_DECOYS.items():
        key = (slug.upper(), "decoy_lig")
        if key not in out and slug.upper() not in {r.upper() for r in TIER3_NA_RECEPTORS}:
            # Generate scrambled sequence deterministically
            min_h = min_hamming_for(native_seq)
            scrambled, _seed_used, _variant = scramble_peptide(
                native_seq, slug, salt=salt, min_hamming=min_h,
            )
            out[key] = {
                "receptor": slug.upper(),
                "ligand_role": "decoy_lig",
                "is_peptide": "TRUE",
                "smiles": "",
                "peptide_sequence": scrambled,
                "iupac_name": f"scrambled {common_name}",
                "bound_pdb": "",
                "activity_class": "decoy_none_known",
                "notes": (f"scrambled peptide decoy from PEPTIDE_DECOYS "
                          f"under salt {salt!r} (min_hamming={min_h})"),
                "ccd_code": "",
                "ccd_smiles": "",
                "smiles_source": f"scripts/build_block_c_decoys.py::PEPTIDE_DECOYS[{slug!r}]",
            }
    # Inject NA rows for Tier 3 NA-listed receptors' decoy_lig cells.
    for slug in TIER3_NA_RECEPTORS:
        key = (slug.upper(), "decoy_lig")
        if key not in out:
            out[key] = {
                "receptor": slug.upper(),
                "ligand_role": "decoy_lig",
                "is_peptide": "FALSE",
                "smiles": "",
                "peptide_sequence": "",
                "activity_class": "NA",
                "notes": f"Tier 3 NA decoy: {TIER3_NA_RECEPTORS[slug]}",
            }
    return out


def _content_for_row(backbone: str, apo: bool,
                     receptor_seq: str, partner_seq: str,
                     ligand_type: str, ligand_smiles: str,
                     ligand_sequence: str,
                     input_name: str, seed: int) -> str:
    """Emit backbone-input file content (string) for one row.

    For peptide-agonist rows, ligand_type is 'peptide' and ligand_sequence
    is the L-alpha sequence; backbones receive it as a second protein
    chain rather than as a small-molecule ligand.
    """
    is_peptide = (ligand_type == "peptide")
    if backbone == "boltz":
        base = _boltz_yaml_monomer(receptor_seq) if apo else \
               _boltz_yaml_two_chain(receptor_seq, partner_seq)
        if is_peptide:
            # Peptide ligand as a small extra protein chain
            base = base + f'  - protein:\n      id: L\n      sequence: {ligand_sequence}\n'
            return base
        return base + _boltz_ligand_block(ligand_type, "", ligand_smiles,
                                          ligand_chain_id="L")
    if backbone == "of3":
        if is_peptide:
            lig = {
                "molecule_type": "protein",
                "chain_ids": ["L"],
                "sequence": ligand_sequence,
            }
        else:
            lig = _of3_ligand_chain(ligand_type, "", ligand_smiles)
        if apo:
            return _of3_json_monomer(input_name, receptor_seq, seed,
                                     ligand_chain=lig)
        return _of3_json_two_chain(input_name, receptor_seq, partner_seq,
                                   seed, ligand_chain=lig)
    if backbone == "protenix":
        if is_peptide:
            lig = {"proteinChain": {"sequence": ligand_sequence, "count": 1}}
        else:
            lig = _protenix_ligand_entry(ligand_type, "", ligand_smiles)
        if apo:
            return _protenix_json_monomer(input_name, receptor_seq,
                                          ligand_entry=lig)
        return _protenix_json_two_chain(input_name, receptor_seq,
                                        partner_seq, ligand_entry=lig)
    if backbone == "chai":
        if is_peptide:
            lig_fa = f">protein|name=lig\n{ligand_sequence}\n"
        else:
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
          ligand_csvs: list[Path],
          reference_set_csv: Path | None = None) -> dict:
    receptor_seqs = _parse_fasta(receptor_fasta)
    partner_seqs = _parse_fasta(partners_fasta)
    ligand_set = _load_ligand_set(ligand_csvs)

    ref_set_path = (reference_set_csv
                    if reference_set_csv is not None
                    else Path(__file__).resolve().parent.parent
                    / "refs" / "reference_set.csv")
    species_map = _load_receptor_species_map(ref_set_path)
    # Audit §21: fail fast if any panel receptor has no unambiguous
    # species entry — refuse to dispatch a manifest that would carry
    # the hardcoded "human" default for a non-human panel receptor.
    for r in RECEPTORS:
        _resolve_receptor_species(r, species_map)

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
            peptide_seq = (lig_row.get("peptide_sequence") or "").strip()
            is_peptide_flag = (lig_row.get("is_peptide") or "").strip().upper() in ("TRUE", "T", "1", "YES")
            ccd_code = (lig_row.get("ccd_code") or "").strip()
            bound_pdb = (lig_row.get("bound_pdb") or "").strip()
            smiles_source = (lig_row.get("smiles_source") or "").strip()
            activity_class = (lig_row.get("activity_class") or "").strip()

            # Skip NA rows. A row is NA if its activity_class is 'NA' OR
            # if it has neither SMILES nor a peptide_sequence (both blank
            # = no ligand payload; would collapse to apo-shaped input
            # producing duplicate prediction_sha and phantom
            # pharmacology signal).
            has_payload = bool(smiles) or bool(peptide_seq)
            if activity_class == "NA" or not has_payload:
                skipped_na.append((receptor, ligand_role))
                continue

            if is_peptide_flag or (peptide_seq and not smiles):
                ligand_type = "peptide"
            elif smiles:
                ligand_type = "small_molecule"
            else:
                ligand_type = ""

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
                        request_id = (
                            f"blockc_tier3_{receptor.lower()}_"
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
                                ligand_type, smiles, peptide_seq,
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
                        row["wave_group"] = "block_c_tier3_2026_09_04"
                        row["branch"] = "propose"
                        row["tier"] = "tier3"
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
                        # Audit §21 — lift from reference_set instead of
                        # hardcoding "human". OPSD→bovin, B1B1U5→9arac,
                        # etc. Ambiguous receptors raise upstream.
                        row["species"] = _resolve_receptor_species(
                            receptor, species_map,
                        )
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
                        row["ligand_sequence"] = peptide_seq if ligand_type == "peptide" else ""
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
                    help="if set, write ~4800 per-row input files under here")
    ap.add_argument("--hpc-inputs-prefix", required=True,
                    help="HPC-visible path prefix where materialised inputs land")
    ap.add_argument("--hpc-out-prefix", required=True,
                    help="HPC-visible path prefix for output CIFs")
    ap.add_argument("--receptor-fasta",
                    default=str(REPO / "refs/panel_receptor_sequences.fasta"))
    ap.add_argument("--partners-fasta",
                    default=str(REPO / "docs/EXPERIMENT_CATALOG/sequences/partners.fasta"))
    ap.add_argument("--ligand-csv", action="append", default=None,
                    help="Ligand CSV path(s); pass multiple times for union. "
                         "Default: refs/ligand_set.csv + refs/ligand_set_tier3.csv")
    ap.add_argument("--reference-set-csv", default=None,
                    help="reference_set.csv used to lift receptor→species "
                         "(default: refs/reference_set.csv). Audit §21.")
    args = ap.parse_args(argv)

    if args.ligand_csv:
        ligand_csvs = [Path(p) for p in args.ligand_csv]
    else:
        ligand_csvs = [
            REPO / "refs/ligand_set.csv",
            REPO / "refs/ligand_set_tier3.csv",
        ]

    result = build(
        out_csv=Path(args.out),
        materialise_dir=(Path(args.materialise_inputs_dir)
                         if args.materialise_inputs_dir else None),
        hpc_inputs_prefix=args.hpc_inputs_prefix,
        hpc_out_prefix=args.hpc_out_prefix,
        receptor_fasta=Path(args.receptor_fasta),
        partners_fasta=Path(args.partners_fasta),
        ligand_csvs=ligand_csvs,
        reference_set_csv=(Path(args.reference_set_csv)
                           if args.reference_set_csv else None),
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
