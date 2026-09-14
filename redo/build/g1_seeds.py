#!/usr/bin/env python3
"""g1_seeds.py -- the prediction seeds, pinned per receptor, before dispatch.

**Why this exists.** There was no seed column anywhere in `redo/inputs/`. The only
`seed` columns in the whole tree were `draw_seed`/`receptor_seed` in
`drule_selected.tsv`, which are the decoy-selection RNG and have nothing to do with
predictions. What existed instead was a REQUIREMENT on the receiving pipeline --
`RUN_MATRIX.md:294`, "seeds must be paired across every arm within a receptor" --
and `run_registry.tsv` marks E6.4 `NOT_ENUMERATED` / `NEEDS_PI_DECISION` with the
note "free before dispatch, impossible after".

Blocks A and B both failed exactly this: **1,898 distinct `seed_outer` across Block
A's 380 cells**. With unpaired seeds no within-seed contrast is readable, because
arm A's seed 3 and arm B's seed 3 are different numbers and nothing can pair them
afterwards. A seed allocated by the pipeline at dispatch time cannot be paired after
the fact; it has to be decided here.

**The design, and the one thing it deliberately does NOT decide.**

Seeds are a property of the RECEPTOR, not of the row. So this emits one ordered seed
list per receptor, and every arm for that receptor draws from the same list in the
same order. Pairing is then STRUCTURAL rather than checked: arm A's seed 1 *is* arm
B's seed 1, by construction, and there is no way to get it wrong at dispatch.

That also keeps the file small and honest -- 64 receptors x 5 seeds = 320 rows,
rather than stamping 10,195 duplicated values across 2,039 system rows.

What this does **not** decide is how many seeds a given cell consumes. `RUN_MATRIX`
declares the split for exactly two cell sizes -- the core tier at **5 seeds x 10
samples** (:58) and the wide tier at **2 seeds x 5 samples** (:160) -- and
`g1_systems.csv` carries six distinct (n_pooled, n_percell) pairs. The other four are
undeclared. Inventing a split for them is precisely the failure this project keeps
recording, so `--report` names them instead and they stay a stated spec gap.

The rule is a cell takes the FIRST k seeds of its receptor's list. So a 2-seed cell
and a 5-seed cell on the same receptor still agree on seeds 1 and 2, and the gap
above cannot break pairing -- only the count is open, never the identity.

Run:    python3 redo/build/g1_seeds.py
Check:  python3 redo/build/g1_seeds.py --check     (regenerate and diff)
Gap:    python3 redo/build/g1_seeds.py --report    (cell sizes with no declared split)
"""
import csv
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS                                     # noqa: E402

OUT = os.path.join(INPUTS, "g1_seeds.tsv")

# Pinned 2026-09-14, the day seeds were allocated, and NEVER to be changed once a
# single prediction has run. Same shape as drule_selected.tsv's draw_seed, which
# uses 20260912 -- a date, so a reader can tell when the allocation was frozen.
SALT = "20260914"

# The largest seed count any declared cell size consumes (core tier, RUN_MATRIX:58).
# A cell needing fewer takes a prefix of the list.
N_SEEDS = 5

# The cell sizes whose seeds x samples split RUN_MATRIX actually declares.
DECLARED_SPLIT = {
    (50, 50): (5, 10),      # core tier,  RUN_MATRIX.md:58
    (10, 50): (2, 5),       # wide tier,  RUN_MATRIX.md:160 -- pooled grain
}


def seed_for(slug, k):
    """Seed k of receptor `slug`. Keyed on the receptor and the index ONLY.

    Deliberately not on arm, construct, backbone or item: that omission is what
    makes the seed identical across arms, which is the whole point. Adding any of
    them to the key would silently reintroduce the Block A defect.
    """
    h = hashlib.sha256(f"redo|seed|{slug}|{k}|{SALT}".encode()).hexdigest()
    return int(h[:8], 16)                      # 32-bit, the usual seed range


def receptors():
    """Every receptor either systems file dispatches, in a stable order."""
    seen = []
    for fn in ("g1_systems.csv", "g2_systems.csv"):
        p = os.path.join(INPUTS, fn)
        if not os.path.exists(p):
            sys.exit(f"FAIL: {fn} is absent. A missing input is a FAILURE, not a "
                     f"skip -- seeds allocated over a partial panel would be wrong "
                     f"in a way nothing downstream could detect.")
        for r in csv.DictReader(open(p, encoding="utf-8")):
            s = r["receptor_slug"]
            if s not in seen:
                seen.append(s)
    return sorted(seen)


def build():
    rows = []
    for slug in receptors():
        for k in range(1, N_SEEDS + 1):
            rows.append([slug, str(k), str(seed_for(slug, k)), SALT])
    return rows


def report():
    """Name the cell sizes whose seeds x samples split is undeclared."""
    p = os.path.join(INPUTS, "g1_systems.csv")
    sizes = {}
    for r in csv.DictReader(open(p, encoding="utf-8")):
        try:
            key = (int(r["n_pooled"]), int(r["n_percell"]))
        except ValueError:
            continue
        sizes.setdefault(key, set()).add(r["arm"])
    print("\n  cell size            split            arms")
    print("  -------------------  ---------------  ----")
    gaps = 0
    for key in sorted(sizes):
        if key in DECLARED_SPLIT:
            s, n = DECLARED_SPLIT[key]
            split = f"{s} seeds x {n}"
        else:
            split = "UNDECLARED"
            gaps += 1
        print(f"  n_pooled={key[0]:<3} percell={key[1]:<3}  {split:<15}  "
              f"{len(sizes[key])}")
    print(f"\n  {gaps} of {len(sizes)} cell sizes have no declared seeds x samples "
          f"split.\n  Seed IDENTITY is pinned regardless -- a cell takes the first k "
          f"of its\n  receptor's list, so 2-seed and 5-seed cells still agree on "
          f"seeds 1-2.\n  Only the COUNT is open, and it is a spec decision, not a "
          f"generator default.\n")
    return 0


def main(argv):
    if "--report" in argv:
        return report()
    rows = build()
    header = ["receptor_slug", "seed_index", "seed", "salt"]
    body = "\t".join(header) + "\n" + "\n".join("\t".join(r) for r in rows) + "\n"

    # pairing is structural, but assert it anyway rather than trusting the argument
    by_idx = {}
    for slug, k, seed, _ in rows:
        by_idx.setdefault((slug, k), set()).add(seed)
    collide = [k for k, v in by_idx.items() if len(v) != 1]
    if collide:
        sys.exit(f"FAIL: {len(collide)} (receptor, index) pairs map to more than one "
                 f"seed. Pairing across arms is broken at the source.")
    if len({r[2] for r in rows}) != len(rows):
        dupes = len(rows) - len({r[2] for r in rows})
        sys.stderr.write(f"  note: {dupes} seed value(s) collide across receptors. "
                         f"That is harmless -- seeds are only ever compared WITHIN a "
                         f"receptor -- but worth seeing.\n")

    if "--check" in argv:
        have = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if have != body:
            sys.exit("FAIL: g1_seeds.tsv does not match this generator. Re-run "
                     "without --check, then restamp the manifest.")
        print(f"OK  {len(rows)} seeds, {len(rows) // N_SEEDS} receptors x {N_SEEDS}, "
              f"salt {SALT}, file matches the generator")
        return 0
    open(OUT, "w", encoding="utf-8").write(body)
    print(f"wrote {OUT}  ({len(rows)} rows: {len(rows) // N_SEEDS} receptors x "
          f"{N_SEEDS} seeds, salt {SALT})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
