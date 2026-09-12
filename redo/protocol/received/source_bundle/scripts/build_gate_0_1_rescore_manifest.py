#!/usr/bin/env python3
"""Build the Block C Gate 0.1 rescore manifest.

Combines input_path rows from three corpora:

1. Block A: experiments/018_block_a_switch_test/analysis/rows.csv
2. Block B: experiments/019_block_b_partner_selection/analysis/rows.csv
3. mn_consensus: 20 subfolders under experiments/mn_consensus/*/rows.csv

Emits a manifest with columns:

    prediction_path, receptor_slug, state_claim, input_species, corpus

The `corpus` column is B1-added (extends the schema
scripts/rescore_parallel.py's _load_manifest accepts — it reads
prediction_path/receptor_slug/state_claim/input_species and ignores
unknown columns per csv.DictReader semantics). It is used post-rescore
to split rows.csv into three per-corpus rows.pocket.csv sidecars.

Species resolution:

- Block A / Block B: from the corpus's queue.csv (rsync'd from HPC
  into experiments/020_block_c_ligand_pharmacology/manifest/). This
  is the same discipline that fixed the Block B species bug in
  `0e7ee0d` — never hard-code "human"; look up per-receptor.
- mn_consensus: 3 receptors (AA2AR, ADRB2, DRD2), all human per
  refs/reference_set.csv.

Discipline (per CLAUDE.md "RMSD driver reads input_path verbatim"):
input_path is copied byte-verbatim from each corpus's rows.csv. No
path derivation.

Usage:

    python3 scripts/build_gate_0_1_rescore_manifest.py
"""
from __future__ import annotations

import csv
import collections
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

MANIFEST_DIR = REPO / "experiments" / "020_block_c_ligand_pharmacology" / "manifest"
OUT_PATH = MANIFEST_DIR / "gate_0_1_rescore_manifest.csv"

BLOCK_A_ROWS = REPO / "experiments" / "018_block_a_switch_test" / "analysis" / "rows.csv"
BLOCK_B_ROWS = REPO / "experiments" / "019_block_b_partner_selection" / "analysis" / "rows.csv"
MN_CONSENSUS_ROOT = REPO / "experiments" / "mn_consensus"

BLOCK_A_QUEUE = MANIFEST_DIR / "block_a_queue.csv"
BLOCK_B_QUEUE = MANIFEST_DIR / "block_b_queue.csv"


def _species_map_from_queue(queue_path: Path) -> dict[str, str]:
    """Build receptor→species map from a queue.csv, warning on conflicts.

    Same approach as scripts/build_block_b_rescore_manifest.py:34 —
    read receptor_resolved + species per row, prefer one per receptor.
    Conflicts halt (per Block B species-bug discipline).
    """
    species: dict[str, str] = {}
    with queue_path.open() as f:
        for row in csv.DictReader(f):
            rec = (row.get("receptor_resolved") or "").upper().strip()
            sp = (row.get("species") or "").strip()
            if not rec:
                continue
            if not sp:
                continue
            if rec in species and species[rec] != sp:
                raise SystemExit(
                    f"species conflict for {rec} in {queue_path}: "
                    f"{species[rec]!r} vs {sp!r} — refusing to build manifest"
                )
            species[rec] = sp
    return species


# mn_consensus is 3 receptors (all human); no queue.csv exists locally.
_MN_CONSENSUS_SPECIES = {"AA2AR": "human", "ADRB2": "human", "DRD2": "human"}


def _rescore_row(input_path: str, receptor: str, state_claim: str,
                 species: str, corpus: str) -> dict[str, str]:
    return {
        "prediction_path": input_path,
        "receptor_slug": receptor,
        "state_claim": state_claim,
        "input_species": species,
        "corpus": corpus,
    }


def _read_corpus_rows_csv(path: Path, species_map: dict[str, str],
                          corpus: str) -> list[dict[str, str]]:
    """Read a corpus rows.csv, emit one manifest row per input_path."""
    out: list[dict[str, str]] = []
    missing_species: set[str] = set()
    with path.open() as f:
        for row in csv.DictReader(f):
            ip = row.get("input_path", "")
            rec = (row.get("receptor_slug") or "").upper()
            state = row.get("input_state_claim") or "Ga-coupled-active"
            if not ip:
                continue
            sp = species_map.get(rec)
            if not sp:
                missing_species.add(rec)
                continue
            out.append(_rescore_row(ip, rec, state, sp, corpus))
    if missing_species:
        raise SystemExit(
            f"receptors missing from species map for {corpus}: "
            f"{sorted(missing_species)}"
        )
    return out


def main() -> int:
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    if not BLOCK_A_QUEUE.exists() or not BLOCK_B_QUEUE.exists():
        print(
            f"missing queue.csv sidecars: expected {BLOCK_A_QUEUE} and "
            f"{BLOCK_B_QUEUE} — rsync from basel-hpc first",
            file=sys.stderr,
        )
        return 2

    species_a = _species_map_from_queue(BLOCK_A_QUEUE)
    species_b = _species_map_from_queue(BLOCK_B_QUEUE)
    print(f"Block A species map: {len(species_a)} receptors")
    print(f"Block B species map: {len(species_b)} receptors")

    all_rows: list[dict[str, str]] = []

    # --- Block A ---
    ba = _read_corpus_rows_csv(BLOCK_A_ROWS, species_a, "block_a")
    print(f"Block A: {len(ba)} rows")
    all_rows.extend(ba)

    # --- Block B ---
    bb = _read_corpus_rows_csv(BLOCK_B_ROWS, species_b, "block_b")
    print(f"Block B: {len(bb)} rows")
    all_rows.extend(bb)

    # --- mn_consensus (20 subdirs) ---
    mn_total = 0
    for sub in sorted(MN_CONSENSUS_ROOT.iterdir()):
        rows_csv = sub / "rows.csv"
        if not rows_csv.exists():
            continue
        mn_rows = _read_corpus_rows_csv(rows_csv, _MN_CONSENSUS_SPECIES,
                                         "mn_consensus")
        mn_total += len(mn_rows)
        all_rows.extend(mn_rows)
    print(f"mn_consensus: {mn_total} rows across subdirs")

    # --- Write combined manifest ---
    fieldnames = ["prediction_path", "receptor_slug", "state_claim",
                  "input_species", "corpus"]
    with OUT_PATH.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(all_rows)

    print(f"\nwrote {len(all_rows)} rows to {OUT_PATH}")

    # Sanity check: per-corpus breakdown, per-state_claim breakdown,
    # per-receptor-class breakdown.
    per_corpus = collections.Counter(r["corpus"] for r in all_rows)
    per_state = collections.Counter(r["state_claim"] for r in all_rows)
    print("per corpus:", dict(per_corpus))
    print("per state_claim:", dict(per_state))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
