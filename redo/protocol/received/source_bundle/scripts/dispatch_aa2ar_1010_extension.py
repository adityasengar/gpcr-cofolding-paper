"""Dispatch Round 3 (m,n) extension for AA2AR + Gαs + NECA.

Fills in 5 additional (m,n) cells to enrich the grid, skipping OF3
(already HIGH confidence, and (10,10) OF3 = 100 preds at ~14 min each
would blow the 4-hour budget).

Priority order (queued in this order — workers pop FIFO-ish):
    029_aa2ar_gs_neca_mn_10_10  (10, 10)  100 preds/bb × 3 bb = 300  — big cell
    030_aa2ar_gs_neca_mn_10_1   (10, 1)   10 preds/bb  × 3 bb =  30  — extreme seeds
    031_aa2ar_gs_neca_mn_1_10   ( 1, 10)  10 preds/bb  × 3 bb =  30  — extreme samples
    032_aa2ar_gs_neca_mn_10_2   (10, 2)   20 preds/bb  × 3 bb =  60  — better-std seeds axis
    033_aa2ar_gs_neca_mn_2_10   ( 2, 10)  20 preds/bb  × 3 bb =  60  — better-std samples axis

Total: 480 predictions, ~4 hours on 12 H100s at ~7 min/pred avg.

Ligand: NECA (SMILES from existing 013_aa2ar_gs_neca_mn_5_1/spec.yaml).
Partner: `alphas` (Gs).
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

AA2AR_LAYOUT = [
    ("029_aa2ar_gs_neca_mn_10_10", 10, 10),  # big cell, ~3 hrs
    ("030_aa2ar_gs_neca_mn_10_1",  10,  1),  # cheap, extreme seeds
    ("031_aa2ar_gs_neca_mn_1_10",   1, 10),  # cheap, extreme samples
    ("032_aa2ar_gs_neca_mn_10_2",  10,  2),  # better-std seeds
    ("033_aa2ar_gs_neca_mn_2_10",   2, 10),  # better-std samples
]

NECA_SMILES = "Nc1ncnc2n(cnc12)[C@@H]1O[C@H](CNC(=O)N)[C@@H](O)[C@H]1O"


def build_spec(slug: str, m: int, n: int) -> dict:
    return {
        "request_id": slug,
        "biological_question": (
            f"Round 3 (m,n) extension: AA2AR + Gαs + NECA "
            f"({m}, {n}). Fills the (m,n) grid to test whether "
            f"(5,5) captures the diversity of (10,10), and whether "
            f"AA2AR-Protenix samples-winner outlier holds at higher N. "
            f"Skips OF3 (HIGH confidence already, expensive)."
        ),
        "receptor": "AA2AR",
        "partner": {"type": "g_alpha", "identity": "alphas"},
        "ligand": {"type": "small_molecule", "smiles": NECA_SMILES},
        "state_claim": "Ga-coupled-active",
        "backbones": ["boltz", "protenix", "chai"],
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
    for slug, m, n in AA2AR_LAYOUT:
        spec = build_spec(slug, m, n)
        rows = _expand_rows(spec)
        run_pre_checks(spec, rows, api, ref_species_map)
        materialise_inputs(spec, rows, output_root, api)
        for r in rows:
            if not r.get("prediction_sha", "").strip():
                r["prediction_sha"] = propose_row_key(r) or r.get("input_sha", "")[:12]
        n_pass = sum(1 for r in rows if r["pre_check_status"] == "pass")
        print(f"[{slug}] {len(rows)} rows, {n_pass}/{len(rows)} pass", flush=True)
        all_new_rows.extend(rows)

    existing = list(csv.DictReader(QUEUE.open()))
    existing_shas = {r["prediction_sha"] for r in existing}
    new_unique = [r for r in all_new_rows if r["prediction_sha"] not in existing_shas]
    print(f"appending {len(new_unique)} new rows "
          f"(dropped {len(all_new_rows) - len(new_unique)} duplicates)")

    fields = list(PROPOSE_MANIFEST_COLUMNS)
    with QUEUE.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(existing)
        w.writerows(new_unique)

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
