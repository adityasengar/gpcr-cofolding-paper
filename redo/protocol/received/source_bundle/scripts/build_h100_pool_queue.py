"""Build the 149-row unified queue for the h100_pool worker pool.

Two sources:
1. AA2AR retries — 21 rows from phase1_mn/status.csv where state=failed,
   joined against phase1_mn/manifest.csv by prediction_path parent dir.
2. ADRB2 mn fresh — 128 rows, 5 (m,n) sub-experiments matching AA2AR shape.
   Ligand: adrenaline (SMILES `CNC[C@H](O)c1ccc(O)c(O)c1`). Partner: alphas (Gs).
   Materialises input files under /hpc/scratch/.../h100_pool/experiments/019…023.

Emits:
- {pool}/queue.csv — merged manifest, 149 rows, propose-schema columns
- {pool}/queue_state.csv — 149 rows, all state=pending, ready for workers

MUST run on basel-hpc (materialise_inputs needs write access to /hpc/scratch).

Usage:
    ssh basel-hpc "cd /home/sengaad1/paper_af3 && \\
        source /home/sengaad1/software/venvs/openfold3/bin/activate && \\
        python3 scripts/build_h100_pool_queue.py"
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
POOL.mkdir(parents=True, exist_ok=True)

PHASE1_MANIFEST = Path("/hpc/scratch/sengaad1/paper_af3/phase1_mn/manifest.csv")
PHASE1_STATUS = Path("/hpc/scratch/sengaad1/paper_af3/phase1_mn/status.csv")

# The 5 (m,n) cells shared between AA2AR and ADRB2 studies
MN_CELLS = [
    ("019_adrb2_gs_agonist_mn_5_1",  5,  1),
    ("020_adrb2_gs_agonist_mn_1_5",  1,  5),
    ("021_adrb2_gs_agonist_mn_5_5",  5,  5),
    ("022_adrb2_gs_agonist_mn_20_1", 20, 1),
    ("023_adrb2_gs_agonist_mn_1_20", 1,  20),
]

# Adrenaline / epinephrine — canonical ADRB2 full agonist
ADRENALINE_SMILES = "CNC[C@H](O)c1ccc(O)c(O)c1"


def collect_aa2ar_retries() -> list[dict[str, str]]:
    """21 failed rows from phase1_mn, joined by prediction_path parent."""
    failed_outdirs = {}
    for r in csv.DictReader(PHASE1_STATUS.open()):
        if r["state"] == "failed":
            failed_outdirs[r["out_dir"].rstrip("/")] = r["prediction_sha"]

    print(f"[phase1] {len(failed_outdirs)} failed rows to retry", flush=True)
    rows: list[dict[str, str]] = []
    for m in csv.DictReader(PHASE1_MANIFEST.open()):
        pp = m.get("prediction_path", "").strip()
        if not pp:
            continue
        od = pp.rsplit("/", 1)[0]
        if od in failed_outdirs:
            # Force prediction_sha to match what status.csv had
            m["prediction_sha"] = failed_outdirs[od]
            rows.append(m)
    print(f"[phase1] {len(rows)} manifest rows joined", flush=True)
    return rows


def build_adrb2_spec(cell_slug: str, seeds: int, samples: int) -> dict:
    return {
        "request_id": cell_slug,
        "biological_question": (
            f"(m,n) generalization test — ADRB2 + Gαs + adrenaline "
            f"({seeds} seeds × {samples} samples per seed). "
            f"Cross-checks the AA2AR (m,n) findings in phase1_mn on a "
            f"different Class-A Gs receptor. Same partner class, "
            f"different receptor identity."
        ),
        "receptor": "ADRB2",
        "partner": {"type": "g_alpha", "identity": "alphas"},
        "ligand": {"type": "small_molecule", "smiles": ADRENALINE_SMILES},
        "state_claim": "Ga-coupled-active",
        "backbones": ["boltz", "of3", "protenix", "chai"],
        "seeds": seeds,
        "samples_per_seed": samples,
        "species": "human",
        "partner_perturbation": "wt",
    }


def collect_adrb2_fresh(api: Api, ref_species_map: dict) -> list[dict[str, str]]:
    """5 sub-experiments × 4 backbones × seeds rows each."""
    all_rows: list[dict[str, str]] = []
    output_root = POOL / "experiments"
    output_root.mkdir(parents=True, exist_ok=True)

    for slug, m, n in MN_CELLS:
        spec = build_adrb2_spec(slug, m, n)
        rows = _expand_rows(spec)
        run_pre_checks(spec, rows, api, ref_species_map)
        materialise_inputs(spec, rows, output_root, api)
        # Propose rows have empty prediction_sha by default — synthesise it
        # using the same content-hash key the supervisor would compute, so
        # each row is uniquely keyed by (input_sha, new_seed).
        for r in rows:
            if not r.get("prediction_sha", "").strip():
                r["prediction_sha"] = propose_row_key(r) or r.get("input_sha", "")[:12]
        n_pass = sum(1 for r in rows if r["pre_check_status"] == "pass")
        print(f"[adrb2 {slug}] {len(rows)} rows, {n_pass}/{len(rows)} pass",
              flush=True)
        all_rows.extend(rows)
    print(f"[adrb2] total: {len(all_rows)} rows", flush=True)
    return all_rows


def write_queue(all_rows: list[dict[str, str]]) -> None:
    queue = POOL / "queue.csv"
    state = POOL / "queue_state.csv"

    # Merge column set — extra cols from phase1 manifest are OK, worker reads by name
    fields = list(PROPOSE_MANIFEST_COLUMNS)
    with queue.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in all_rows:
            w.writerow(r)
    print(f"wrote {queue}: {len(all_rows)} rows", flush=True)

    # queue_state.csv — one row per queue row, all pending
    state_cols = ["prediction_sha", "backbone", "state",
                  "worker", "claimed_at", "finished_at", "last_reason"]
    with state.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=state_cols)
        w.writeheader()
        for r in all_rows:
            w.writerow({
                "prediction_sha": r["prediction_sha"],
                "backbone": r["backbone"],
                "state": "pending",
                "worker": "",
                "claimed_at": "",
                "finished_at": "",
                "last_reason": "",
            })
    print(f"wrote {state}: {len(all_rows)} rows, all pending", flush=True)


def main() -> int:
    api = Api(cache_dir=DEFAULT_CACHE_DIR)
    ref_species_map = load_ref_species_map(REF_SET_CSV)

    print("=== 1. AA2AR retries ===", flush=True)
    aa2ar_rows = collect_aa2ar_retries()

    print("\n=== 2. ADRB2 fresh ===", flush=True)
    adrb2_rows = collect_adrb2_fresh(api, ref_species_map)

    # Sanity check for duplicate prediction_shas
    all_rows = aa2ar_rows + adrb2_rows
    seen_shas = set()
    unique_rows = []
    dupes = 0
    for r in all_rows:
        sha = r["prediction_sha"]
        if sha in seen_shas:
            dupes += 1
            continue
        seen_shas.add(sha)
        unique_rows.append(r)
    if dupes:
        print(f"WARN: dropped {dupes} duplicate SHAs", flush=True)

    print(f"\n=== 3. writing queue: {len(unique_rows)} rows ===", flush=True)
    write_queue(unique_rows)

    print("\nDone.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
