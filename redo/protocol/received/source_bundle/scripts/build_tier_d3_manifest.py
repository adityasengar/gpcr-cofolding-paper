"""Build Tier D3 manifest — MSA-depth conformational-generation sweep.

Grid (PREREG §D-3.2, spec at experiments/024_tier_d3_msa_depth/spec/):
  26 Class A receptors × 4 backbones × 5 depths × 5 seeds × 10 samples
  = 26,000 predictions total; 2,600 dispatch rows (samples_per_seed=10).

Depths: full (upstream default; no subsample), 512, 128, 32, 8.
For non-full depths, MSA is subsampled from full.a3m via
scripts/subsample_msa.py with a per-row `msa_subsample_seed`.

The manifest populates two Tier-D3-specific columns (backwards-
compatible: empty on non-D3 tiers, only populated here):

  msa_a3m_path         — absolute path to the depth-subsampled .a3m
                         (used by Boltz-2 / OpenFold-3 / Protenix v2
                         via the propose.py msa_a3m_path kwarg landed
                         at commit b3863bd).
  chai_msa_directory   — absolute path to the depth-specific dir
                         containing Chai's .aligned.pqt cache (used
                         via the CHAI_MSA_DIRECTORY env var, per-row
                         plumbed through queue_ops.py).

Smoke mode (--smoke): 5 discriminator receptors × 4 backbones × 5
depths × 1 seed = 100 rows (1,000 predictions).

Usage:
    python3 scripts/build_tier_d3_manifest.py \\
        --out experiments/024_tier_d3_msa_depth/manifest/tier_d3_manifest.csv \\
        --materialise-inputs-dir /tmp/tier_d3_inputs \\
        --hpc-inputs-prefix /hpc/scratch/sengaad1/paper_af3/experiments/024_tier_d3_msa_depth/full/pool/inputs \\
        --hpc-out-prefix    /hpc/scratch/sengaad1/paper_af3/experiments/024_tier_d3_msa_depth/full/pool/pool \\
        --msa-cache-root    /hpc/scratch/sengaad1/paper_af3/d3_msa_cache
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
    _boltz_yaml_monomer,
    _of3_json_monomer,
    _protenix_json_monomer,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BACKBONES = ("boltz", "chai", "of3", "protenix")

# Depths (PREREG §D-3.2). "full" means live-fetch or no subsample.
DEPTHS = ("full", 512, 128, 32, 8)

N_SEEDS = 5
SAMPLES_PER_SEED = 10

# Smoke-mode discriminator subset — 5 receptors covering the D1-overlap
# discriminators plus AA2AR as canonical adenosine benchmark.
SMOKE_PANEL = ("AA2AR", "CNR2", "ADRB2", "OPRK", "OPSD")

# D3 seed salt (per PREREG §D-3.7 msa_subsample_seed record)
D3_SEED_SALT = "tier_d3_2026_09_07"


def canonical_seeds(salt: str, n: int) -> list[int]:
    """Deterministic seeds derived from a salt."""
    out = []
    for i in range(n):
        h = hashlib.sha256(f"{salt}_{i}".encode()).digest()
        out.append(int.from_bytes(h[:4], "big") % (2**31))
    return out


def parse_panel(csv_path: Path) -> list[str]:
    receptors: list[str] = []
    with csv_path.open() as f:
        for line in f:
            if line.startswith("#") or line.startswith("receptor_slug"):
                continue
            slug = line.split(",")[0].strip()
            if slug:
                receptors.append(slug)
    return receptors


def parse_fasta(path: Path) -> dict[str, str]:
    seqs, key, buf = {}, None, []
    for line in path.read_text().splitlines():
        if line.startswith(">"):
            if key:
                seqs[key] = "".join(buf)
            key = line[1:].split("|", 1)[0].strip().upper()
            buf = []
        else:
            buf.append(line.strip())
    if key:
        seqs[key] = "".join(buf)
    return seqs


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def msa_a3m_path_for(cache_root: str, receptor: str, depth, seed: int) -> str:
    """Per-receptor subdir path containing `colabfold_main.a3m` (name is what
    OF3's registry accepts; other backbones don't care about the basename)."""
    r = receptor.lower()
    if depth == "full":
        return f"{cache_root}/a3m/full/{r}/colabfold_main.a3m"
    return f"{cache_root}/a3m/seed_{seed}/depth_{depth}/{r}/colabfold_main.a3m"


def chai_dir_for(cache_root: str, depth, seed: int) -> str:
    if depth == "full":
        return f"{cache_root}/chai/full"
    return f"{cache_root}/chai/seed_{seed}/depth_{depth}"


# ---------------------------------------------------------------------------
# Row builder
# ---------------------------------------------------------------------------

MANIFEST_COLUMNS = [
    "prediction_path", "prediction_sha", "experiment_slug", "wave_group",
    "branch", "tier", "backbone", "receptor_from_path_substring",
    "receptor_resolved", "disambig_conflict", "receptor_unresolved_in_original",
    "expected_control_json", "new_seed", "request_id", "seed_index",
    "state_claim", "species", "partner_type", "partner_identity",
    "partner_perturbation", "receptor_class", "input_path", "input_sha",
    "pre_check_status", "pre_check_details_json", "seed_used", "ligand_type",
    "ligand_sequence", "ligand_smiles", "samples_per_seed", "ligand_role",
    "ligand_bound_pdb", "ligand_ccd", "ligand_smiles_source",
    # D3-specific
    "msa_depth", "msa_subsample_seed", "msa_a3m_path", "chai_msa_directory",
]


def build(out_csv: Path, materialise_dir: Path | None,
          hpc_inputs_prefix: str, hpc_out_prefix: str,
          msa_cache_root: str,
          panel_csv: Path, fasta_path: Path,
          smoke: bool = False) -> dict:
    receptors = parse_panel(panel_csv)
    if smoke:
        receptors = [r for r in receptors if r in SMOKE_PANEL]
    seqs = parse_fasta(fasta_path)
    missing = [r for r in receptors if r not in seqs]
    if missing:
        raise SystemExit(f"missing sequences for: {missing}")

    seeds = canonical_seeds(D3_SEED_SALT, N_SEEDS if not smoke else 1)

    rows: list[dict[str, str]] = []
    inputs_written = 0
    for receptor in receptors:
        rseq = seqs[receptor].upper()
        for backbone in BACKBONES:
            for depth in DEPTHS:
                for seed_index, seed_value in enumerate(seeds):
                    depth_tag = "full" if depth == "full" else f"depth{depth}"
                    request_id = (
                        f"tier_d3_{receptor.lower()}_"
                        f"{depth_tag}_{backbone}_seed{seed_index}"
                    )
                    ext = {"boltz": "yaml", "chai": "fasta",
                           "of3": "json", "protenix": "json"}[backbone]
                    msa_path = msa_a3m_path_for(msa_cache_root, receptor, depth, seed_value)
                    chai_dir = chai_dir_for(msa_cache_root, depth, seed_value)
                    # For non-chai backbones, the propose emitter takes
                    # msa_a3m_path directly.
                    propose_msa = None if backbone == "chai" else msa_path

                    if materialise_dir is not None:
                        subdir = materialise_dir / backbone
                        subdir.mkdir(parents=True, exist_ok=True)
                        if backbone == "boltz":
                            content = _boltz_yaml_monomer(rseq, msa_a3m_path=propose_msa)
                        elif backbone == "chai":
                            content = f">protein|name={request_id}\n{rseq}\n"
                        elif backbone == "of3":
                            content = _of3_json_monomer(
                                request_id, rseq, seed=seed_value,
                                msa_a3m_path=propose_msa,
                            )
                        elif backbone == "protenix":
                            content = _protenix_json_monomer(
                                request_id, rseq, msa_a3m_path=propose_msa,
                            )
                        else:
                            raise ValueError(backbone)
                        input_file = subdir / f"{request_id}.{ext}"
                        input_file.write_text(content)
                        inputs_written += 1
                        input_sha = hashlib.sha256(content.encode()).hexdigest()
                        hpc_input_path = (
                            f"{hpc_inputs_prefix.rstrip('/')}/{backbone}/"
                            f"{request_id}.{ext}"
                        )
                    else:
                        input_sha = ""
                        hpc_input_path = ""

                    hpc_pred_out_dir = (
                        f"{hpc_out_prefix.rstrip('/')}/{receptor.lower()}/"
                        f"{depth_tag}/{backbone}/seed_{seed_value}"
                    )
                    prediction_path = f"{hpc_pred_out_dir}/model_0.cif"

                    row = {c: "" for c in MANIFEST_COLUMNS}
                    row.update({
                        "prediction_path": prediction_path,
                        "prediction_sha": "",
                        "experiment_slug": request_id,
                        "wave_group": D3_SEED_SALT,
                        "branch": "propose",
                        "tier": "tier_d3",
                        "backbone": backbone,
                        "receptor_from_path_substring": receptor,
                        "receptor_resolved": receptor,
                        "disambig_conflict": "false",
                        "receptor_unresolved_in_original": "false",
                        "new_seed": str(seed_value),
                        "request_id": request_id,
                        "seed_index": str(seed_index),
                        "state_claim": "apo",
                        "species": "human",
                        "partner_type": "apo",
                        "partner_identity": "",
                        "receptor_class": "A",
                        "input_path": hpc_input_path,
                        "input_sha": input_sha,
                        "pre_check_status": "pass",
                        "seed_used": str(seed_value),
                        "ligand_role": "apo_no_ligand",
                        "samples_per_seed": str(SAMPLES_PER_SEED),
                        "msa_depth": str(depth),
                        "msa_subsample_seed": str(seed_value) if depth != "full" else "",
                        "msa_a3m_path": "" if backbone == "chai" else msa_path,
                        "chai_msa_directory": chai_dir if backbone == "chai" else "",
                    })
                    rows.append(row)

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    summary = {
        "n_rows": len(rows),
        "n_predictions": len(rows) * SAMPLES_PER_SEED,
        "n_receptors": len(receptors),
        "n_backbones": len(BACKBONES),
        "n_depths": len(DEPTHS),
        "n_seeds": len(seeds),
        "smoke": smoke,
        "inputs_materialised": inputs_written,
        "manifest_path": str(out_csv),
    }
    print(json.dumps(summary, indent=2))
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--materialise-inputs-dir", type=Path, default=None)
    ap.add_argument("--hpc-inputs-prefix", required=True)
    ap.add_argument("--hpc-out-prefix", required=True)
    ap.add_argument("--msa-cache-root", required=True,
                    help="Root of the MSA cache tree containing a3m/{full,seed_S/depth_D}/*.a3m + chai/{full,seed_S/depth_D}/*.aligned.pqt")
    ap.add_argument("--panel-csv", type=Path,
                    default=REPO / "refs/tier_d3_panel.csv")
    ap.add_argument("--fasta", type=Path,
                    default=REPO / "refs/panel_receptor_sequences.fasta")
    ap.add_argument("--smoke", action="store_true",
                    help="Smoke mode: 5 receptors × 1 seed (100 rows).")
    args = ap.parse_args()

    build(args.out, args.materialise_inputs_dir,
          args.hpc_inputs_prefix, args.hpc_out_prefix,
          args.msa_cache_root,
          args.panel_csv, args.fasta, smoke=args.smoke)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
