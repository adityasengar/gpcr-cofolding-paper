"""Dispatch DRD2 + Gαi 5-(m,n)-cell follow-up study to h100_pool queue.

Generates 5 sub-experiments matching AA2AR/ADRB2 layout, but for DRD2
(Class A, Gi-coupled — cross-partner-class test for the UNSTABLE
backbones: protenix, chai; and cross-GPCR at 3rd data point for Boltz's
INSUFFICIENT verdict).

Appends new rows to /hpc/scratch/.../h100_pool/queue.csv and
queue_state.csv (does NOT overwrite existing rows).

Ligand: dopamine (SMILES `NCCc1ccc(O)c(O)c1`) — canonical DRD2 agonist.
Partner: `alphai1` (Gi/o).

Runs on HPC (needs write access to scratch + materialise_inputs).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scorer.bw_numbering import Api
from scorer.pre_check import load_ref_species_map
from scorer.propose import (
    DEFAULT_CACHE_DIR,
    REF_SET_CSV,
    _expand_rows,
    materialise_inputs,
    run_pre_checks,
)
from scorer.rerun_dispatch import propose_row_key
from scorer.schema import PROPOSE_MANIFEST_COLUMNS

POOL = Path("/hpc/scratch/sengaad1/paper_af3/h100_pool")
QUEUE = POOL / "queue.csv"
STATE = POOL / "queue_state.csv"

DRD2_LAYOUT = [
    ("024_drd2_gi_dopamine_mn_5_1",   5,  1),
    ("025_drd2_gi_dopamine_mn_1_5",   1,  5),
    ("026_drd2_gi_dopamine_mn_5_5",   5,  5),
    ("027_drd2_gi_dopamine_mn_20_1",  20, 1),
    ("028_drd2_gi_dopamine_mn_1_20",  1,  20),
]

DOPAMINE_SMILES = "NCCc1ccc(O)c(O)c1"


def build_spec(slug: str, m: int, n: int) -> dict:
    return {
        "request_id": slug,
        "biological_question": (
            f"(m,n) 3rd-GPCR follow-up: DRD2 + Gαi + dopamine "
            f"({m}, {n}). Resolves UNSTABLE cross-GPCR verdict for "
            f"protenix + chai on AA2AR-vs-ADRB2 (both Gs), and adds "
            f"3rd GPCR datapoint for Boltz."
        ),
        "receptor": "DRD2",
        "partner": {"type": "g_alpha", "identity": "alphai1"},
        "ligand": {"type": "small_molecule", "smiles": DOPAMINE_SMILES},
        "state_claim": "Ga-coupled-active",
        "backbones": ["boltz", "of3", "protenix", "chai"],
        "seeds": m,
        "samples_per_seed": n,
        "species": "human",
        "partner_perturbation": "wt",
    }


def main() -> int:
    api = Api(cache_dir=DEFAULT_CACHE_DIR)
    ref_species_map = load_ref_species_map(REF_SET_CSV)

    output_root = POOL / "experiments"
    output_root.mkdir(parents=True, exist_ok=True)

    all_new_rows = []
    for slug, m, n in DRD2_LAYOUT:
        spec = build_spec(slug, m, n)
        rows = _expand_rows(spec)
        run_pre_checks(spec, rows, api, ref_species_map)
        materialise_inputs(spec, rows, output_root, api)
        # Synthesise prediction_sha (empty by default on propose rows)
        for r in rows:
            if not r.get("prediction_sha", "").strip():
                r["prediction_sha"] = propose_row_key(r) or r.get("input_sha", "")[:12]
        n_pass = sum(1 for r in rows if r["pre_check_status"] == "pass")
        print(f"[{slug}] {len(rows)} rows, {n_pass}/{len(rows)} pass", flush=True)
        all_new_rows.extend(rows)

    # Append to queue.csv (preserving existing header + rows)
    existing = list(csv.DictReader(QUEUE.open()))
    existing_shas = {r["prediction_sha"] for r in existing}
    new_unique = [r for r in all_new_rows if r["prediction_sha"] not in existing_shas]
    print(f"appending {len(new_unique)} new rows (dropped {len(all_new_rows) - len(new_unique)} duplicates)")

    fields = list(PROPOSE_MANIFEST_COLUMNS)
    with QUEUE.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(existing)
        w.writerows(new_unique)

    # Append to queue_state.csv
    state_cols = ["prediction_sha", "backbone", "state", "worker",
                  "claimed_at", "finished_at", "last_reason"]
    existing_state = list(csv.DictReader(STATE.open()))
    with STATE.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=state_cols)
        w.writeheader()
        w.writerows(existing_state)
        for r in new_unique:
            w.writerow({
                "prediction_sha": r["prediction_sha"],
                "backbone": r["backbone"],
                "state": "pending",
                "worker": "",
                "claimed_at": "",
                "finished_at": "",
                "last_reason": "",
            })

    print(f"queue.csv now has {len(existing) + len(new_unique)} rows")
    print(f"queue_state.csv now has {len(existing_state) + len(new_unique)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
