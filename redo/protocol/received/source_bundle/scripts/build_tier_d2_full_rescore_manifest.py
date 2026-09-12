#!/usr/bin/env python3
"""Build D2 full rescore manifest by walking the pool.

Path convention: <pool>/pool/<receptor>/<arm>/<backbone>/seed_<seed>/…/*.cif
Emits one row per CIF prediction.
"""
from __future__ import annotations
import csv, re, sys
from pathlib import Path

POOL = Path("/hpc/scratch/sengaad1/paper_af3/experiments/023_tier_d2_directed_inactive/full/pool/pool")
OUT = Path("/home/sengaad1/paper_af3/experiments/023_tier_d2_directed_inactive/analysis/rescore_manifest.tier_d2_full.csv")

ARM_TO_STATE = {
    "apo":           ("apo",              "apo",       ""),
    "cognate_ga":    ("Ga-coupled-active", "g_alpha",  "alphas"),
    "active_nb":     ("Nb-active",         "nanobody", ""),
    "inactive_nb":   ("Nb-inactive",       "nanobody", ""),
}

# For each backbone, we know where predictions land. Use CIF suffix patterns:
# Use rglob to catch every CIF; filter out non-prediction artefacts (e.g. inputs)
BB_CIF_PATTERNS = {"boltz": "**/*.cif", "chai": "**/*.cif", "of3": "**/*.cif", "protenix": "**/*.cif"}
_SKIP_TOKENS = ("input", "reference", "_ref.cif")

rows = []
for rec_dir in sorted(POOL.iterdir()):
    if not rec_dir.is_dir(): continue
    rec = rec_dir.name
    for arm_dir in sorted(rec_dir.iterdir()):
        if not arm_dir.is_dir(): continue
        arm = arm_dir.name
        state_claim, partner_type, partner_identity = ARM_TO_STATE.get(arm, ("apo","apo",""))
        for bb_dir in sorted(arm_dir.iterdir()):
            if not bb_dir.is_dir(): continue
            bb = bb_dir.name
            for seed_dir in sorted(bb_dir.iterdir()):
                if not seed_dir.is_dir(): continue
                pattern = BB_CIF_PATTERNS.get(bb)
                if not pattern: continue
                # Use glob relative to seed_dir; recursive for '**'
                for cif in seed_dir.glob(pattern):
                    n = cif.name.lower()
                    if any(tok in n for tok in _SKIP_TOKENS): continue
                    rows.append({
                        "prediction_path": str(cif),
                        "receptor_slug": rec,
                        "state_claim": state_claim,
                        "input_species": "human",
                        "backbone": bb,
                        "ligand_role": "apo_no_ligand",
                        "partner_type": partner_type,
                        "partner_identity": partner_identity,
                        "ligand_bound_pdb": "",
                        "ligand_ccd": "",
                        "ligand_smiles_source": "",
                    })

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print(f"wrote {OUT} ({len(rows)} rows)")

# Break-down census
from collections import Counter
c = Counter((r["receptor_slug"], r["backbone"]) for r in rows)
print(f"unique (receptor × backbone) cells: {len(c)}")
