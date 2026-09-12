"""Build rescore manifest for Block C smoke.

Walks the smoke output tree on HPC (or a fetched-back mirror) and emits
one row per CIF file for rescore_parallel.py — the driver expects
columns ``prediction_path, receptor_slug, state_claim, input_species``.

Each smoke cell (80 total) produced ~5 CIFs (samples_per_seed=5), so
the rescore manifest has ~400 rows.

Emits, alongside standard columns, the Block C provenance fields
carried through from smoke_manifest.csv so rescored rows carry
ligand_role, ligand_bound_pdb, ligand_ccd, ligand_smiles_source (see
end-of-file for scorer round-trip caveat).

Usage:
    # On HPC login node (or laptop with HPC ssh):
    python3 scripts/build_block_c_smoke_rescore_manifest.py \\
        --hpc-pool-root /hpc/scratch/sengaad1/paper_af3/experiments/020_block_c_ligand_pharmacology/smoke/pool \\
        --manifest experiments/020_block_c_ligand_pharmacology/manifest/smoke_manifest.csv \\
        --out experiments/020_block_c_ligand_pharmacology/analysis/rescore_manifest.smoke.csv \\
        [--emit-on-hpc /hpc/.../rescore_manifest.smoke.csv]
"""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path


def discover_cifs_hpc(hpc_pool_root: str) -> list[str]:
    """Enumerate every produced CIF under the pool tree via one SSH call."""
    r = subprocess.run(
        ["ssh", "basel-hpc",
         f"find {hpc_pool_root} -maxdepth 10 -type f "
         f"\\( -name '*.cif' -o -name 'model_*.pdb' -o -name 'pred.model_idx_*.cif' \\) 2>/dev/null | sort"],
        capture_output=True, text=True, timeout=60,
    )
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip() and "/logs/" not in ln]


def index_manifest_by_seeddir(manifest: list[dict]) -> dict[str, dict]:
    """Key manifest rows by their HPC seed-dir suffix.

    prediction_path in smoke_manifest.csv looks like
        /hpc/.../pool/adrb2/full_agonist/apo/boltz/seed_1544158306/model_0.cif
    so the last-4-segments-before-file uniquely identify the row.
    """
    by_dir: dict[str, dict] = {}
    for r in manifest:
        pp = r.get("prediction_path", "")
        if not pp:
            continue
        # take the seed_ dir path
        seed_dir = pp.rsplit("/", 1)[0]
        by_dir[seed_dir] = r
    return by_dir


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hpc-pool-root", required=True)
    ap.add_argument("--manifest", type=Path, required=True,
                    help="smoke_manifest.csv (Block C smoke input)")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    manifest = list(csv.DictReader(args.manifest.open()))
    manifest_by_dir = index_manifest_by_seeddir(manifest)

    cifs = discover_cifs_hpc(args.hpc_pool_root)
    print(f"discovered {len(cifs)} CIFs", file=sys.stderr)

    rows: list[dict] = []
    n_matched = 0
    n_orphan = 0
    BACKBONES = {"boltz", "chai", "of3", "protenix"}
    for cif in cifs:
        # Walk up until we hit a seed_-prefixed dir WHOSE PARENT IS A
        # backbone name. protenix nests seed_/name/seed_/predictions/ —
        # we want the OUTER seed_ (protenix/seed_...), not the inner one.
        cur = cif.rsplit("/", 1)[0]
        found = None
        while cur and "/" in cur:
            last = cur.rsplit("/", 1)[-1]
            parent = cur.rsplit("/", 1)[0].rsplit("/", 1)[-1]
            if last.startswith("seed_") and parent in BACKBONES:
                found = cur
                break
            up = cur.rsplit("/", 1)[0]
            if up == cur:
                break
            cur = up
        if not found or found not in manifest_by_dir:
            n_orphan += 1
            continue
        cur = found
        mrow = manifest_by_dir[cur]
        n_matched += 1
        rows.append({
            "prediction_path": cif,
            "receptor_slug": mrow["receptor_resolved"],
            "state_claim": mrow["state_claim"],
            "input_species": mrow["species"],
            # Block C provenance passthrough (scorer's DictReader ignores
            # unknown columns; enrich_partner_metadata reads them later).
            "backbone": mrow["backbone"],
            "ligand_role": mrow["ligand_role"],
            "partner_type": mrow["partner_type"],
            "partner_identity": mrow["partner_identity"],
            "ligand_bound_pdb": mrow.get("ligand_bound_pdb", ""),
            "ligand_ccd": mrow.get("ligand_ccd", ""),
            "ligand_smiles_source": mrow.get("ligand_smiles_source", ""),
        })

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else
                           ["prediction_path", "receptor_slug", "state_claim",
                            "input_species"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {args.out} : {len(rows)} rows "
          f"({n_matched} matched, {n_orphan} orphans)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
