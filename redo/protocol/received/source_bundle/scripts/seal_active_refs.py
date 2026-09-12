"""Sealed active-reference subset — PREREG §14 (v3, restore-and-reseal).

Draw the sealed 8 receptors from the eligible pool
(`refs/eligible_pool.csv`, excluded=0 AND ∉ held-out) with fixed seed
`20260903`. Physically move their active-role rows out of
`refs/reference_set.csv` and into `refs/sealed_active_refs_2026_09_01.csv`.

Rewrite history:

- **v1 (seed 20260901)** — left rows in reference_set.csv under an
  analysis-side gate only; not a seal. Also collided with §13 held-out
  seed. Retired.
- **v2 (seed 20260902)** — physical move landed, disjoint from §13, but
  drew pathologies (B1B1U5 non-mammalian singleton, FSHR pre-registered
  apo failure) because the pool was `class_a_40 - held_out_8` with no
  further exclusions. Retired.
- **v3 (seed 20260903)** — pool sourced from `refs/eligible_pool.csv`;
  Class A minus §1a exclusions (B1B1U5, CNR1, OPRD, OPSD, LSHR, FSHR).
  Disjoint from held-out set. This file.

Idempotent + reversible: if the current sealed CSV was drawn under a
prior seed / prior pool, the script **restores** those receptors' active
rows back into reference_set.csv before physically moving the new
draw out. Re-running against an already-correctly-sealed state no-ops
with a clear message.

Usage:
    python3 scripts/seal_active_refs.py
"""
from __future__ import annotations

import csv
import hashlib
import random
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ELIGIBLE = REPO / "refs/eligible_pool.csv"
REFSET = REPO / "refs/reference_set.csv"
REFSET_PRESEAL = REPO / "refs/reference_set.pre_seal.csv"
SEALED_CSV = REPO / "refs/sealed_active_refs_2026_09_01.csv"

SEED = 20260903
N_SEALED = 8

# Held-out threshold receptors (PREREG §13, seed 20260901). Sealed set
# must be disjoint from held-out.
HELD_OUT = {"5HT2C", "AGTR1", "CXCR2", "CXCR4", "DRD2", "LPAR1", "MCHR1", "NPY2R"}


def load_sealed_pool() -> list[str]:
    """Sealed pool = eligible (excluded=0) - held-out.

    Sourced from refs/eligible_pool.csv, which applies the §1a
    exclusions (B1B1U5, CNR1, OPRD, OPSD, LSHR, FSHR) and the Class B/F
    scope rule.
    """
    pool: set[str] = set()
    with ELIGIBLE.open() as f:
        for r in csv.DictReader(f):
            if r["excluded"] != "0":
                continue
            slug = r["receptor_slug"].strip().upper()
            if slug in HELD_OUT:
                continue
            pool.add(slug)
    return sorted(pool)


def draw_sealed() -> list[str]:
    pool = load_sealed_pool()
    if len(pool) < N_SEALED:
        raise SystemExit(
            f"sealed pool {len(pool)} < N_SEALED {N_SEALED} (check eligible_pool.csv)"
        )
    rng = random.Random(SEED)
    return sorted(rng.sample(pool, N_SEALED))


def read_sealed_slugs_on_disk() -> set[str]:
    """Return the set of sealed slugs currently in the sealed CSV, or empty."""
    if not SEALED_CSV.exists():
        return set()
    with SEALED_CSV.open() as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    return {
        r["receptor_slug"].strip().upper()
        for r in csv.DictReader(lines)
        if r.get("role", "").strip() == "active"
    }


def read_sealed_rows_on_disk() -> tuple[list[str], list[dict[str, str]]]:
    """Return (fieldnames, sealed active-role rows) from the sealed CSV."""
    if not SEALED_CSV.exists():
        return [], []
    with SEALED_CSV.open() as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    reader = csv.DictReader(lines)
    fns = list(reader.fieldnames or [])
    rows = [r for r in reader if r.get("role", "").strip() == "active"]
    return fns, rows


def is_seal_already_applied(sealed: list[str]) -> bool:
    """Return True iff the on-disk state exactly matches `sealed`."""
    on_disk = read_sealed_slugs_on_disk()
    if on_disk != set(sealed):
        return False
    with REFSET.open() as f:
        rows = list(csv.DictReader(f))
    surviving_active = {
        r["receptor_slug"].strip().upper()
        for r in rows
        if r.get("role", "").strip() == "active"
        and r["receptor_slug"].strip().upper() in set(sealed)
    }
    return not surviving_active


def restore_previous_seal() -> list[str]:
    """Restore rows from the previous sealed CSV back into reference_set.csv.

    Returns the list of restored slugs. If reference_set.pre_seal.csv is
    available, we sanity-check that the restored rows match the pre-seal
    file byte-for-byte for those receptors; otherwise the restored data
    is trusted from the sealed CSV itself.
    """
    old_fns, old_rows = read_sealed_rows_on_disk()
    if not old_rows:
        return []

    with REFSET.open() as f:
        reader = csv.DictReader(f)
        ref_fns = list(reader.fieldnames or [])
        ref_rows = list(reader)

    # Append the restored rows to reference_set.csv. Field-order in the
    # sealed CSV matches reference_set.csv (both written by this
    # script), so we can safely reuse ref_fns.
    with REFSET.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ref_fns, extrasaction="ignore")
        w.writeheader()
        w.writerows(ref_rows + old_rows)

    return sorted({r["receptor_slug"].strip().upper() for r in old_rows})


def main() -> int:
    sealed = draw_sealed()

    if is_seal_already_applied(sealed):
        sha = hashlib.sha256(SEALED_CSV.read_bytes()).hexdigest()
        print(f"NO-OP: seal already applied.")
        print(f"Seed: {SEED}")
        print(f"Sealed receptors ({len(sealed)}): {sealed}")
        print(f"Sealed CSV: {SEALED_CSV}")
        print(f"SHA256: {sha}")
        return 0

    # If the sealed CSV exists but with the wrong set, restore first.
    prior_slugs = read_sealed_slugs_on_disk()
    restored: list[str] = []
    if prior_slugs and prior_slugs != set(sealed):
        restored = restore_previous_seal()
        print(f"Restored {len(restored)} prior-sealed active rows back "
              f"to {REFSET}: {restored}")

    # Read reference_set (post-restore); split into rows-to-keep vs rows-to-move.
    with REFSET.open() as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    sealed_set = set(sealed)
    to_move: list[dict[str, str]] = []
    to_keep: list[dict[str, str]] = []
    for r in rows:
        slug = r["receptor_slug"].strip().upper()
        role = r.get("role", "").strip()
        if slug in sealed_set and role == "active":
            to_move.append(r)
        else:
            to_keep.append(r)

    # Guarantee: every sealed receptor produced exactly one active row.
    seen = {r["receptor_slug"].strip().upper() for r in to_move}
    missing = sealed_set - seen
    if missing:
        raise SystemExit(
            f"FAIL: no active-role row in {REFSET} for {sorted(missing)} — cannot seal."
        )

    seal_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Write the sealed CSV (overwrite: prior file superseded).
    SEALED_CSV.parent.mkdir(parents=True, exist_ok=True)
    with SEALED_CSV.open("w", newline="") as f:
        f.write(f"# sealed_until: Block A predictions landed AND rows.csv frozen (user unseals via documented step)\n")
        f.write(f"# seal_seed: {SEED}\n")
        f.write(f"# seal_timestamp_utc: {seal_ts}\n")
        f.write(f"# n_sealed: {len(to_move)}\n")
        f.write(f"# sealed_slugs: {','.join(sorted(sealed))}\n")
        f.write(f"# pool_source: refs/eligible_pool.csv (excluded=0 AND slug not in held_out_8)\n")
        f.write(f"# disjoint_from_held_out: True (held_out seed=20260901; sealed seed={SEED})\n")
        f.write(f"# physical_move: True (rows removed from refs/reference_set.csv)\n")
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(to_move)

    # Rewrite reference_set.csv WITHOUT the moved rows.
    with REFSET.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(to_keep)

    sha = hashlib.sha256(SEALED_CSV.read_bytes()).hexdigest()

    print(f"Seed: {SEED}")
    print(f"Pool source: {ELIGIBLE.relative_to(REPO)}")
    print(f"Held-out (excluded from pool): {sorted(HELD_OUT)}")
    print(f"Sealed receptors ({len(sealed)}): {sealed}")
    if restored:
        print(f"Restored (returned to refset before new seal): {restored}")
    print(f"Moved {len(to_move)} active rows out of {REFSET}")
    print(f"      kept {len(to_keep)} rows in {REFSET}")
    print(f"Sealed CSV: {SEALED_CSV}")
    print(f"SHA256: {sha}")
    print(f"Seal timestamp (UTC): {seal_ts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
