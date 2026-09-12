#!/usr/bin/env python3
"""Block C Step 3.3 — apo/cognate ceiling headroom from Block B landed rows.

For each of the 8 Class A Tier 1 panel receptors × 4 backbones (32 cells),
compute:

  - apo_active_frac     — fraction of apo predictions that already pass the
                          Class A class-conditional two-instrument predicate
                          (`d_npxxy_y558_y753_oh < NPXXY_LT` AND
                          `d_gpcrdb_tm6_tilt_246_637_ca > TM6_GT`).
                          Ceiling-locked at >= APO_CEIL → P1 untestable.
  - cognate_active_frac — same predicate on the cognate arm.
                          Cognate at ~1.00 with zero variance = P2
                          sensitivity-limited but not untestable.

Denominator = every landed prediction in the cell (50 = 5 seeds × 10 samples
in Block B). NaN on either predicate axis counts as inactive (conservative
deflation, PREREG §2c-revised: "if you cannot measure it, you cannot call
it active").

Arm and backbone are recovered from `input_path` under the segment
`019_block_b_partner_selection_{receptor_lower}_{arm}_{backbone}/`; there
is no standalone arm column in rows.csv. Confirmed clean partition
(8000 rows × 4 arms × 4 backbones = 32000).

Inputs:
    experiments/019_block_b_partner_selection/analysis/rows.csv
        SHA256 = c65b93c2e08b45992dcaa0e9f63a6874785cabab4bc08373ab35c82ad511d705

Outputs:
    experiments/020_block_c_ligand_pharmacology/analysis/
        ceiling_headroom_2026_09_04.csv
        ceiling_headroom_2026_09_04.provenance.json
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BLOCK_B_ROWS = REPO / "experiments/019_block_b_partner_selection/analysis/rows.csv"
OUT_DIR = REPO / "experiments/020_block_c_ligand_pharmacology/analysis"
OUT_CSV = OUT_DIR / "ceiling_headroom_2026_09_04.csv"
OUT_PROV = OUT_DIR / "ceiling_headroom_2026_09_04.provenance.json"

EXPECTED_ROWS_SHA = "c65b93c2e08b45992dcaa0e9f63a6874785cabab4bc08373ab35c82ad511d705"

PANEL = ["ADRB2", "DRD3", "AA2AR", "ACM4", "OX2R", "ACM2", "5HT1B", "AA1R"]
BACKBONES = ["boltz", "chai", "of3", "protenix"]

# Class A class-conditional two-instrument predicate (PREREG §2c-revised)
NPXXY_LT = 9.082
TM6_GT = 14.932

# Ceiling threshold for auto-hold / per-backbone exclusion flag
APO_CEIL = 0.80

ARM_RE = re.compile(
    r"019_block_b_partner_selection_([a-z0-9]+)_([a-z]+)_([a-z0-9]+)/"
)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
        ).strip()
    except Exception:
        return "no-git"


def is_active(row: dict) -> bool:
    """Class A two-instrument predicate. NaN on either axis → inactive."""
    try:
        npxxy = float(row["d_npxxy_y558_y753_oh"])
        tm6 = float(row["d_gpcrdb_tm6_tilt_246_637_ca"])
    except (ValueError, KeyError):
        return False
    return npxxy < NPXXY_LT and tm6 > TM6_GT


def main() -> int:
    if not BLOCK_B_ROWS.exists():
        print(f"ERROR: {BLOCK_B_ROWS} missing", file=sys.stderr)
        return 1

    observed_sha = sha256_of(BLOCK_B_ROWS)
    if observed_sha != EXPECTED_ROWS_SHA:
        print(
            f"ERROR: rows.csv SHA drift.\n  expected {EXPECTED_ROWS_SHA}\n  observed {observed_sha}",
            file=sys.stderr,
        )
        return 2

    # Accumulate per (receptor, backbone, arm)
    # We track apo and cognate; shuffled/decoy computed but not the primary
    # output.
    counts: dict[tuple[str, str, str], dict[str, int]] = defaultdict(
        lambda: {"n": 0, "active": 0, "nan_npxxy": 0, "nan_tm6": 0}
    )

    total_rows = 0
    with BLOCK_B_ROWS.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            m = ARM_RE.search(row["input_path"])
            if not m:
                print(f"ERROR: unparseable input_path: {row['input_path']}",
                      file=sys.stderr)
                return 3
            _rec_lower, arm, backbone = m.groups()
            slug = row["receptor_slug"]
            if slug not in PANEL:
                continue
            if backbone not in BACKBONES:
                continue
            key = (slug, backbone, arm)
            c = counts[key]
            c["n"] += 1
            if row["d_npxxy_y558_y753_oh"] in ("", "nan", "NaN"):
                c["nan_npxxy"] += 1
            if row["d_gpcrdb_tm6_tilt_246_637_ca"] in ("", "nan", "NaN"):
                c["nan_tm6"] += 1
            if is_active(row):
                c["active"] += 1

    # Emit 32-cell matrix — one row per (receptor, backbone), with apo and
    # cognate fractions side by side.
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cells_at_ceiling_apo: list[tuple[str, str, float]] = []
    cells_at_ceiling_cognate: list[tuple[str, str, float]] = []
    per_receptor_p1_usable: dict[str, list[str]] = {}
    per_receptor_p1_excluded: dict[str, list[str]] = {}

    with OUT_CSV.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "receptor", "backbone",
            "n_apo_rows", "n_apo_active", "apo_active_frac",
            "n_apo_nan_npxxy", "n_apo_nan_tm6",
            "n_cognate_rows", "n_cognate_active", "cognate_active_frac",
            "n_cognate_nan_npxxy", "n_cognate_nan_tm6",
            "p1_flag", "p2_flag",
        ])
        for slug in PANEL:
            usable = []
            excluded = []
            for bb in BACKBONES:
                apo = counts[(slug, bb, "apo")]
                cog = counts[(slug, bb, "cognate")]
                apo_frac = apo["active"] / apo["n"] if apo["n"] else 0.0
                cog_frac = cog["active"] / cog["n"] if cog["n"] else 0.0

                p1_flag = ""
                if apo_frac >= APO_CEIL:
                    p1_flag = "CEILING_LOCKED_EXCLUDE_FROM_P1"
                    cells_at_ceiling_apo.append((slug, bb, apo_frac))
                    excluded.append(bb)
                else:
                    usable.append(bb)

                p2_flag = ""
                if cog_frac >= 0.999:
                    p2_flag = "COGNATE_AT_UNITY_SENSITIVITY_LIMITED"
                    cells_at_ceiling_cognate.append((slug, bb, cog_frac))
                elif cog_frac <= 0.05:
                    p2_flag = "COGNATE_NEAR_ZERO_P2_INVERTED"
                    cells_at_ceiling_cognate.append((slug, bb, cog_frac))

                writer.writerow([
                    slug, bb,
                    apo["n"], apo["active"], f"{apo_frac:.4f}",
                    apo["nan_npxxy"], apo["nan_tm6"],
                    cog["n"], cog["active"], f"{cog_frac:.4f}",
                    cog["nan_npxxy"], cog["nan_tm6"],
                    p1_flag, p2_flag,
                ])
            per_receptor_p1_usable[slug] = usable
            per_receptor_p1_excluded[slug] = excluded

    # Auto-fire / auto-hold gate
    n_receptors_usable_ge3 = sum(
        1 for slug in PANEL if len(per_receptor_p1_usable[slug]) >= 3
    )
    n_receptors_ceiling_ge3 = sum(
        1 for slug in PANEL if len(per_receptor_p1_excluded[slug]) >= 3
    )
    auto_fire_1 = n_receptors_usable_ge3 >= 6
    auto_fire_2 = n_receptors_ceiling_ge3 == 0
    auto_hold = n_receptors_ceiling_ge3 > 0
    verdict = "GO" if (auto_fire_1 and auto_fire_2 and not auto_hold) else "HOLD"

    provenance = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "script": str(Path(__file__).relative_to(REPO)),
        "repo_head": git_head(),
        "input_rows_csv": str(BLOCK_B_ROWS.relative_to(REPO)),
        "input_rows_csv_sha256": observed_sha,
        "expected_rows_sha256": EXPECTED_ROWS_SHA,
        "input_total_rows": total_rows,
        "panel_receptors": PANEL,
        "backbones": BACKBONES,
        "predicate": {
            "class_A_conditional": "d_npxxy_y558_y753_oh < NPXXY_LT AND d_gpcrdb_tm6_tilt_246_637_ca > TM6_GT",
            "NPXXY_LT": NPXXY_LT,
            "TM6_GT": TM6_GT,
            "nan_convention": "NaN on either axis → inactive (PREREG §2c-revised conservative deflation)",
        },
        "apo_ceiling_threshold": APO_CEIL,
        "output_csv": str(OUT_CSV.relative_to(REPO)),
        "n_receptors_p1_usable_ge3_backbones": n_receptors_usable_ge3,
        "n_receptors_p1_ceiling_ge3_backbones": n_receptors_ceiling_ge3,
        "auto_fire_1_ge6_receptors_usable_on_ge3_backbones": bool(auto_fire_1),
        "auto_fire_2_no_receptor_at_ceiling_on_ge3_backbones": bool(auto_fire_2),
        "auto_hold_any_receptor_at_ceiling_on_ge3_backbones": bool(auto_hold),
        "verdict": verdict,
        "cells_at_apo_ceiling": [
            {"receptor": r, "backbone": b, "apo_active_frac": round(f, 4)}
            for r, b, f in cells_at_ceiling_apo
        ],
        "cells_flagged_cognate": [
            {"receptor": r, "backbone": b, "cognate_active_frac": round(f, 4)}
            for r, b, f in cells_at_ceiling_cognate
        ],
        "per_receptor_p1_usable_backbones": per_receptor_p1_usable,
        "per_receptor_p1_excluded_backbones": per_receptor_p1_excluded,
    }
    OUT_PROV.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")

    # Human-readable summary to stdout
    print(f"input rows.csv SHA256 : {observed_sha}")
    print(f"total rows scanned    : {total_rows}")
    print(f"panel                 : {' '.join(PANEL)}")
    print(f"backbones             : {' '.join(BACKBONES)}")
    print(f"predicate             : d_npxxy < {NPXXY_LT} AND d_gpcrdb_tm6_tilt > {TM6_GT}")
    print(f"apo ceiling threshold : {APO_CEIL}")
    print()
    print(f"cells at apo ceiling (P1 excluded)     : {len(cells_at_ceiling_apo)}")
    for r, b, fr in cells_at_ceiling_apo:
        print(f"    {r} x {b}: apo_active_frac = {fr:.4f}")
    print(f"cells flagged on cognate               : {len(cells_at_ceiling_cognate)}")
    for r, b, fr in cells_at_ceiling_cognate:
        print(f"    {r} x {b}: cognate_active_frac = {fr:.4f}")
    print()
    print("per-receptor P1 usability (backbones with apo_frac < 0.80):")
    for slug in PANEL:
        u = per_receptor_p1_usable[slug]
        e = per_receptor_p1_excluded[slug]
        tag = "" if not e else f"  [EXCLUDE {','.join(e)}]"
        print(f"    {slug:<8} usable={len(u)}/4 ({','.join(u)}){tag}")
    print()
    print(f"auto-fire 1 (>=6/8 receptors testable on >=3/4 backbones for P1) : "
          f"{'GREEN' if auto_fire_1 else 'RED'} ({n_receptors_usable_ge3}/8)")
    print(f"auto-fire 2 (no receptor >=0.80 apo on >=3 backbones)             : "
          f"{'GREEN' if auto_fire_2 else 'RED'} ({n_receptors_ceiling_ge3} at-ceiling)")
    print(f"auto-hold   (any receptor >=0.80 apo on >=3 backbones triggers)   : "
          f"{'GREEN (not triggered)' if not auto_hold else 'RED (triggered)'}")
    print()
    print(f"VERDICT: {verdict}")
    print(f"wrote  : {OUT_CSV.relative_to(REPO)}")
    print(f"wrote  : {OUT_PROV.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
