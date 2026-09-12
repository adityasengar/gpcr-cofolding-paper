#!/usr/bin/env python3
"""
Build Block B rescore manifest for scripts/rescore_parallel.py.

Manifest columns (per rescore_parallel.py header):
  prediction_path, receptor_slug, state_claim, input_species

For every seed dir under experiments/019_block_b_partner_selection/*/<hash>/<bb>/seed_*/,
emit one row per CIF file (pred.model_idx_{0..9}.cif or equivalent).

Metadata:
- receptor_slug: from the experiment folder name (uppercase)
- state_claim: apo → "apo"; else → "Ga-coupled-active"
- input_species: "human" for all Block B receptors

Writes CSV to argv[1].
"""
from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT = Path("/hpc/scratch/sengaad1/paper_af3/experiments/019_block_b_partner_selection")
QUEUE = ROOT / "pool" / "queue.csv"

ARMS = ("cognate", "apo", "shuffled", "decoy")
BACKBONES = ("boltz", "chai", "of3", "protenix")

# Build per-receptor species map from queue.csv — the initial rescore
# hard-coded "human" for every row, which caused A5_species_match to fire
# on the two non-human receptors (B1B1U5 turkey, OPSD bovine → 1200 rows).
_SPECIES_BY_RECEPTOR: dict[str, str] = {}
with QUEUE.open() as _f:
    for _r in csv.DictReader(_f):
        rec = _r["receptor_resolved"].upper()
        sp = _r["species"] or "human"
        if rec in _SPECIES_BY_RECEPTOR and _SPECIES_BY_RECEPTOR[rec] != sp:
            print(f"WARN: receptor {rec} has multiple species labels: "
                  f"{_SPECIES_BY_RECEPTOR[rec]!r} and {sp!r}", file=sys.stderr)
        _SPECIES_BY_RECEPTOR[rec] = sp

def parse_slug(slug: str):
    """Slug: 019_block_b_partner_selection_<receptor>_<arm>_<backbone>."""
    parts = slug.split("_")
    # backbone is last, arm is second-to-last, receptor is between prefix and arm
    if parts[-1] not in BACKBONES:
        return None
    if parts[-2] not in ARMS:
        return None
    prefix_len = len("019_block_b_partner_selection".split("_"))
    receptor_parts = parts[prefix_len:-2]
    receptor = "_".join(receptor_parts).upper()
    arm = parts[-2]
    bb = parts[-1]
    return receptor, arm, bb

if len(sys.argv) < 2:
    print("usage: build_manifest.py <output.csv>", file=sys.stderr)
    sys.exit(1)
out_path = Path(sys.argv[1])
out_path.parent.mkdir(parents=True, exist_ok=True)

rows = []
missing_meta = 0

for exp_dir in sorted(ROOT.iterdir()):
    if not exp_dir.is_dir() or not exp_dir.name.startswith("019_block_b_partner_selection_"):
        continue
    parsed = parse_slug(exp_dir.name)
    if not parsed:
        missing_meta += 1
        continue
    receptor, arm, bb = parsed
    state_claim = "apo" if arm == "apo" else "Ga-coupled-active"

    # Walk hash / bb / seed / pred*.cif
    for hash_dir in exp_dir.iterdir():
        if not hash_dir.is_dir() or hash_dir.name in ("inputs",):
            continue
        bb_dir = hash_dir / bb
        if not bb_dir.exists():
            continue
        for seed_dir in bb_dir.glob("seed_*"):
            if not seed_dir.is_dir():
                continue
            cifs = sorted(seed_dir.rglob("*.cif"))
            species = _SPECIES_BY_RECEPTOR.get(receptor, "human")
            for cif in cifs:
                rows.append({
                    "prediction_path": str(cif),
                    "receptor_slug": receptor,
                    "state_claim": state_claim,
                    "input_species": species,
                })

with out_path.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["prediction_path", "receptor_slug", "state_claim", "input_species"])
    w.writeheader()
    w.writerows(rows)

# Summary
from collections import Counter
by_bb_arm = Counter()
for r in rows:
    pth = Path(r["prediction_path"])
    # Extract bb and arm from the experiment slug in the path
    for anc in pth.parents:
        if anc.name.startswith("019_block_b_partner_selection_"):
            parsed = parse_slug(anc.name)
            if parsed:
                _, arm, bb = parsed
                by_bb_arm[(bb, arm)] += 1
            break

print(f"wrote {len(rows)} rows to {out_path}")
print(f"missing-metadata experiments skipped: {missing_meta}")
print()
print("per (backbone, arm):")
for k in sorted(by_bb_arm):
    print(f"  {k}: {by_bb_arm[k]}")
