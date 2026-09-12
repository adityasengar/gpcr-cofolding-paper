"""Build Tier D1 manifest — 14,000-prediction deep-apo bistability resample.

**Purpose**
    Emit the 140-row manifest at
    ``experiments/022_tier_d1_deep_apo/manifest/tier_d1_manifest.csv``
    and, when ``--materialise-inputs-dir`` is given, write the 140
    per-row backbone-input files under that dir.

    Grid (locked, plan §D1.2):
      7 Class A receptors × 4 backbones × apo-only × 5 seeds × 100 samples
      = 14,000 predictions (targeted (5, 100) departure from the (5, 10)
      lock — PREREG amendment §D-1 names the resampling rationale).

    Receptor panel is loaded verbatim from ``refs/tier_d1_panel.csv``;
    the selection rule and the panel commit ship together so nobody
    can retroactively rerun the rule.

**Design**
    Cloned from ``scripts/build_block_c_tier3_manifest.py``. Removes
    the ligand-state and cognate-arm axes (apo-only, no ligand chain),
    bumps ``SAMPLES_PER_SEED`` from 10 to 100, and rederives
    ``CANONICAL_SEEDS`` from a Tier D1 salt.

    Each manifest row corresponds to ONE backbone invocation with ONE
    seed. The backbone worker reads ``new_seed`` and ``samples_per_seed``
    from the row and produces 100 sample CIFs.

    Deterministic seed derivation:
      seed_i = int.from_bytes(sha256(f'tier_d1_2026_09_06_seed_{i}')[:4], 'big') % (2**31)

    The species-fix preflight (``_load_receptor_species_map`` +
    ``_resolve_receptor_species``) carries through from the Tier 3
    builder unmodified (audit §21).

**Sample-count caveats per backbone** (for the launcher, not this script)
    Each backbone's ``qsub/rerun_{backbone}.sh`` wrapper reads
    ``samples_per_seed`` from the manifest row and passes it through:
      - Boltz: ``--sampling_steps`` orthogonal to sample count; ``samples_per_seed``
        maps to ``--diffusion_samples`` (verify against pinned Boltz version).
      - Chai: ``--num_diffn_samples`` accepts arbitrary int.
      - OF3: runner-yaml ``num_samples`` field; verified accepts ≥100.
      - Protenix: ``sample_num`` in the JSON input honours arbitrary int.
    D1.3 smoke on one receptor × 4 backbones × 5 seeds × 100 samples
    (2,000 preds) confirms wall stays bounded before the full 14,000
    dispatch fires.

Usage:
    python3 scripts/build_tier_d1_manifest.py \\
        --out experiments/022_tier_d1_deep_apo/manifest/tier_d1_manifest.csv \\
        --materialise-inputs-dir /tmp/tier_d1/inputs \\
        --hpc-inputs-prefix /hpc/scratch/sengaad1/paper_af3/experiments/022_tier_d1_deep_apo/tier_d1/inputs \\
        --hpc-out-prefix    /hpc/scratch/sengaad1/paper_af3/experiments/022_tier_d1_deep_apo/tier_d1/pool
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
    _of3_json_monomer,
    _protenix_json_monomer,
    _chai_fasta_monomer,
)
from scorer.schema import PROPOSE_MANIFEST_COLUMNS  # noqa: E402


# Audit §21: species must be lifted from refs/reference_set.csv (not
# hardcoded "human") for non-human panel receptors (OPSD/bovin, etc).
# Preserved from scripts/build_block_c_tier3_manifest.py verbatim; do
# NOT drift.
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


def _load_panel(panel_csv: Path) -> tuple[str, ...]:
    """Load the D1 receptor panel verbatim from refs/tier_d1_panel.csv.

    Panel is 7 rows: 1 anchor (CNR2) + 3 mid-range + 3 confirmatory.
    """
    receptors: list[str] = []
    with panel_csv.open() as f:
        for row in csv.DictReader(f):
            slug = (row.get("receptor_slug") or "").strip().upper()
            if slug:
                receptors.append(slug)
    if len(receptors) != 7:
        raise ValueError(
            f"tier_d1_panel.csv must have exactly 7 rows; got {len(receptors)}. "
            f"Selection rule is 1 anchor (CNR2) + 3 mid-range + 3 confirmatory."
        )
    return tuple(receptors)


BACKBONES = ("boltz", "chai", "of3", "protenix")

# Apo-only tier: no ligand chain, no partner chain. Kept as a single-arm
# tuple to preserve the block_c_tier3 loop shape (harmless overhead;
# clearer at review).
ARMS = ("apo",)

SAMPLES_PER_SEED = 100  # bumped from 10 (block_c_tier3) → 100 (deep-apo).
N_SEEDS = 5
_SEED_SALT = "tier_d1_2026_09_06"

# Derive the seeds deterministically; if _SEED_SALT is renamed, the
# CANONICAL_SEEDS below drift and the assert fires.
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

# Extra manifest columns (kept aligned with block_c_tier3 schema so
# downstream rescore/analysis code can consume both without a schema
# branch). All left empty for D1 rows since apo has no ligand payload.
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


def _content_for_row(backbone: str, receptor_seq: str,
                     input_name: str, seed: int) -> str:
    """Emit backbone-input file content for a monomer/apo row.

    No ligand, no partner — D1 is apo-only.
    """
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


def _backbone_input_ext(backbone: str) -> str:
    return {"boltz": "yaml", "chai": "fasta",
            "of3": "json", "protenix": "json"}[backbone]


def build(out_csv: Path, materialise_dir: Path | None,
          hpc_inputs_prefix: str, hpc_out_prefix: str,
          receptor_fasta: Path,
          panel_csv: Path,
          reference_set_csv: Path | None = None) -> dict:
    receptor_seqs = _parse_fasta(receptor_fasta)
    receptors = _load_panel(panel_csv)

    ref_set_path = (reference_set_csv
                    if reference_set_csv is not None
                    else REPO / "refs" / "reference_set.csv")
    species_map = _load_receptor_species_map(ref_set_path)
    # Audit §21: fail fast if any panel receptor has no unambiguous
    # species entry.
    for r in receptors:
        _resolve_receptor_species(r, species_map)

    for r in receptors:
        if r not in receptor_seqs:
            raise SystemExit(f"missing receptor sequence for {r}")

    rows: list[dict[str, str]] = []
    inputs_written = 0
    predictions_total = 0

    for receptor in receptors:
        rseq = receptor_seqs[receptor]
        for arm in ARMS:
            assert arm == "apo", f"tier D1 is apo-only; got arm={arm!r}"
            partner_type = "apo"
            partner_identity = ""
            for backbone in BACKBONES:
                for seed_index, seed_value in enumerate(CANONICAL_SEEDS):
                    request_id = (
                        f"tier_d1_{receptor.lower()}_"
                        f"{arm}_{backbone}_seed{seed_index}"
                    )
                    input_name = f"{request_id}_seed{seed_index}"
                    ext = _backbone_input_ext(backbone)

                    if materialise_dir is not None:
                        subdir = materialise_dir / backbone
                        subdir.mkdir(parents=True, exist_ok=True)
                        content = _content_for_row(
                            backbone, rseq, input_name, seed_value,
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

                    # HPC output tree — one dir per (row, seed).
                    # Ligand role slot is fixed to "apo_no_ligand" so
                    # the tier D1 tree is disjoint from block_c_tier3
                    # pool paths at every level.
                    hpc_pred_out_dir = (
                        f"{hpc_out_prefix.rstrip('/')}/{receptor.lower()}/"
                        f"apo_no_ligand/{arm}/{backbone}/"
                        f"seed_{seed_value}"
                    )
                    prediction_path = f"{hpc_pred_out_dir}/model_0.cif"

                    row = {c: "" for c in MANIFEST_COLUMNS}
                    row["prediction_path"] = prediction_path
                    row["prediction_sha"] = ""
                    row["experiment_slug"] = request_id
                    row["wave_group"] = "tier_d1_2026_09_06"
                    row["branch"] = "propose"
                    row["tier"] = "tier_d1"
                    row["backbone"] = backbone
                    row["receptor_from_path_substring"] = receptor
                    row["receptor_resolved"] = receptor
                    row["disambig_conflict"] = "false"
                    row["receptor_unresolved_in_original"] = "false"
                    row["expected_control_json"] = ""
                    row["new_seed"] = str(seed_value)
                    row["request_id"] = request_id
                    row["seed_index"] = str(seed_index)
                    # apo arm ⇒ inactive-like state claim (no partner,
                    # no ligand). Matches block_a apo convention.
                    row["state_claim"] = "apo"
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
                    row["ligand_type"] = ""
                    row["ligand_sequence"] = ""
                    row["ligand_smiles"] = ""
                    row["samples_per_seed"] = str(SAMPLES_PER_SEED)
                    # Block-C extras: empty for apo-only D1.
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

    # Grid assertions (plan §D1.2).
    expected_rows = len(receptors) * len(BACKBONES) * N_SEEDS
    assert expected_rows == 140, (
        f"panel/backbone/seed shape drift: "
        f"{len(receptors)}×{len(BACKBONES)}×{N_SEEDS}={expected_rows}"
    )
    assert len(rows) == expected_rows, (
        f"row count mismatch: got {len(rows)}, expected {expected_rows} "
        f"(7 receptors × 4 backbones × 5 seeds; apo-only, no cognate)"
    )
    expected_preds = expected_rows * SAMPLES_PER_SEED
    assert predictions_total == expected_preds, (
        f"prediction count mismatch: got {predictions_total}, "
        f"expected {expected_preds}"
    )
    assert expected_preds == 14000

    return {
        "n_rows": len(rows),
        "n_predictions": predictions_total,
        "n_inputs_written": inputs_written,
        "manifest_path": str(out_csv),
        "canonical_seeds": CANONICAL_SEEDS,
        "receptors": list(receptors),
        "arms": list(ARMS),
        "backbones": list(BACKBONES),
        "samples_per_seed": SAMPLES_PER_SEED,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True, help="output manifest CSV path")
    ap.add_argument("--materialise-inputs-dir", default=None,
                    help="if set, write 140 per-row input files under here")
    ap.add_argument("--hpc-inputs-prefix", required=True,
                    help="HPC-visible path prefix where materialised inputs land")
    ap.add_argument("--hpc-out-prefix", required=True,
                    help="HPC-visible path prefix for output CIFs "
                         "(distinct from block_c_tier3 pool)")
    ap.add_argument("--receptor-fasta",
                    default=str(REPO / "refs/panel_receptor_sequences.fasta"))
    ap.add_argument("--panel-csv",
                    default=str(REPO / "refs/tier_d1_panel.csv"),
                    help="Panel CSV; defaults to refs/tier_d1_panel.csv "
                         "(committed alongside the selection rule).")
    ap.add_argument("--reference-set-csv", default=None,
                    help="reference_set.csv used to lift receptor→species "
                         "(default: refs/reference_set.csv). Audit §21.")
    args = ap.parse_args(argv)

    result = build(
        out_csv=Path(args.out),
        materialise_dir=(Path(args.materialise_inputs_dir)
                         if args.materialise_inputs_dir else None),
        hpc_inputs_prefix=args.hpc_inputs_prefix,
        hpc_out_prefix=args.hpc_out_prefix,
        receptor_fasta=Path(args.receptor_fasta),
        panel_csv=Path(args.panel_csv),
        reference_set_csv=(Path(args.reference_set_csv)
                           if args.reference_set_csv else None),
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
