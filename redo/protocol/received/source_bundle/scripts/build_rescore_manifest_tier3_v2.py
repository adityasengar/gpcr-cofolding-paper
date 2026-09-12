#!/usr/bin/env python3
"""Build the Tier 3 v2 rescore manifest — Post-Audit Stage 1 (2026-09-05).

Regenerates the per-sample rescore manifest with the ligand annotation
columns (``ligand_type`` / ``ligand_smiles`` / ``ligand_sequence`` /
``ligand_role``) joined in from the campaign manifest
(``experiments/021_block_c_tier3_pharmacology/manifest/tier3_manifest.csv``).

The original ``rescore_manifest.tier3.csv`` was built without ligand
smiles/type/sequence, so ``scorer.orchestrator._lift_provenance_from_sidecar``
returned empty on every scored row (Block C Tier 3 dispatch does NOT
emit ``_rerun_plan.json`` sidecars) and every ligand field on
``rows.tier3.csv`` landed NaN. This driver produces
``rescore_manifest.tier3.v2.csv`` with the full field set so
``scripts/rescore_parallel.py``'s manifest-fallback kwargs (added in
the same Post-Audit landing) can populate them per-row.

Join key: the campaign manifest is keyed by seed-dir (one row per
seed × backbone × arm × role × receptor), while the rescore manifest
is per-sample (10 samples per seed). We map every rescore sample to
its parent seed-dir by extracting the ``.../pool/<receptor>/<role>/
<arm>/<backbone>/seed_<N>/...`` prefix — the join is exact-string on
that prefix and every rescore row's parent must appear in the campaign
manifest.

Assertion at build time: every input row's join key must resolve to
exactly one manifest row. Missing / ambiguous / duplicate keys halt
the build with a non-zero exit.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


_SEED_DIR_RE = re.compile(
    r"(?P<prefix>.*/pool/(?P<receptor>[A-Za-z0-9_-]+)/"
    r"(?P<ligand_role>[A-Za-z0-9_-]+)/"
    r"(?P<partner_arm>[A-Za-z0-9_-]+)/"
    r"(?P<backbone>[A-Za-z0-9_-]+)/seed_(?P<seed>\d+))"
)


def _pool_prefix(path: str) -> str | None:
    """Return the ``.../pool/<r>/<lrole>/<arm>/<bb>/seed_<N>`` prefix
    from a prediction path, or None when the path doesn't match the
    Tier 3 pool shape."""
    m = _SEED_DIR_RE.search(path)
    if m is None:
        return None
    return m.group("prefix")


def _sha256(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def build(
    rescore_manifest: Path,
    campaign_manifest: Path,
    out_path: Path,
    provenance_out: Path,
) -> dict[str, object]:
    """Emit ``out_path`` = enriched rescore manifest. Returns a summary
    dict for logging; raises on any join-integrity failure."""
    # --- load campaign manifest, index by seed-dir prefix ---
    campaign_rows: dict[str, dict[str, str]] = {}
    with campaign_manifest.open() as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            key = _pool_prefix(row["prediction_path"])
            if key is None:
                raise RuntimeError(
                    f"campaign manifest row has non-pool prediction_path: "
                    f"{row['prediction_path']!r}"
                )
            if key in campaign_rows:
                raise RuntimeError(
                    f"duplicate campaign-manifest key {key!r}: "
                    f"two rows collide on the seed-dir prefix"
                )
            campaign_rows[key] = row

    # --- load rescore manifest, produce enriched shape ---
    with rescore_manifest.open() as f:
        original_rdr = csv.DictReader(f)
        original_columns = list(original_rdr.fieldnames or [])
        rescore_rows = list(original_rdr)

    # Additional columns to emit (order-stable). Some MAY already be in
    # the input manifest — dedupe.
    extra_cols = [
        "ligand_type", "ligand_smiles", "ligand_sequence", "ligand_role",
    ]
    out_cols = list(original_columns)
    for c in extra_cols:
        if c not in out_cols:
            out_cols.append(c)

    n_joined = 0
    n_missing = 0
    missing_keys: list[str] = []
    per_receptor_smiles: dict[str, set[str]] = {}

    for row in rescore_rows:
        key = _pool_prefix(row["prediction_path"])
        if key is None:
            raise RuntimeError(
                f"rescore manifest row has non-pool prediction_path: "
                f"{row['prediction_path']!r}"
            )
        parent = campaign_rows.get(key)
        if parent is None:
            n_missing += 1
            if len(missing_keys) < 20:
                missing_keys.append(key)
            # Emit the row unchanged so downstream sees the gap
            for c in extra_cols:
                row.setdefault(c, "")
            continue
        n_joined += 1
        # Sidecar values from the campaign manifest — sidecar wins over
        # what the rescore manifest might already carry (the rescore
        # manifest's ligand_role was correct but ligand_smiles/type were
        # absent). Preserve the campaign manifest as the source of
        # truth for all four.
        row["ligand_type"] = parent.get("ligand_type", "") or ""
        row["ligand_smiles"] = parent.get("ligand_smiles", "") or ""
        row["ligand_sequence"] = parent.get("ligand_sequence", "") or ""
        row["ligand_role"] = (
            parent.get("ligand_role", "")
            or row.get("ligand_role", "")
            or ""
        )
        recep = (row.get("receptor_slug") or "").upper()
        # Identity key: SMILES for small molecules, sequence for
        # peptides (APJ / GHSR / GLP1R). Prevents false-positive
        # "constant SMILES" flags on peptide-ligand receptors.
        identity = row["ligand_smiles"] or row["ligand_sequence"]
        if recep:
            per_receptor_smiles.setdefault(recep, set()).add(identity)

    if n_missing > 0:
        raise RuntimeError(
            f"{n_missing} rescore rows have no matching campaign manifest "
            f"row on the seed-dir prefix (first {len(missing_keys)} shown): "
            f"{missing_keys}"
        )

    # --- write enriched rescore manifest ---
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_cols)
        w.writeheader()
        for row in rescore_rows:
            w.writerow({c: row.get(c, "") for c in out_cols})

    # --- also write a compact provenance JSON ---
    provenance = {
        "rescore_manifest_in": str(rescore_manifest.resolve()),
        "campaign_manifest_in": str(campaign_manifest.resolve()),
        "out_manifest": str(out_path.resolve()),
        "rescore_manifest_sha256": _sha256(rescore_manifest),
        "campaign_manifest_sha256": _sha256(campaign_manifest),
        "out_manifest_sha256": _sha256(out_path),
        "n_rescore_rows": len(rescore_rows),
        "n_joined": n_joined,
        "n_missing": n_missing,
        "n_receptors_with_ligand": len(per_receptor_smiles),
        "receptors_with_constant_smiles": sorted(
            r for r, s in per_receptor_smiles.items() if len({x for x in s if x}) < 2
        ),
    }
    provenance_out.parent.mkdir(parents=True, exist_ok=True)
    provenance_out.write_text(json.dumps(provenance, indent=2) + "\n")
    return provenance


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="build_rescore_manifest_tier3_v2",
        description=__doc__,
    )
    p.add_argument("--rescore-manifest", type=Path,
                   default=REPO / "experiments" / "021_block_c_tier3_pharmacology"
                   / "analysis" / "rescore_manifest.tier3.csv")
    p.add_argument("--campaign-manifest", type=Path,
                   default=REPO / "experiments" / "021_block_c_tier3_pharmacology"
                   / "manifest" / "tier3_manifest.csv")
    p.add_argument("--out", type=Path,
                   default=REPO / "experiments" / "021_block_c_tier3_pharmacology"
                   / "analysis" / "rescore_manifest.tier3.v2.csv")
    p.add_argument("--provenance-out", type=Path,
                   default=REPO / "experiments" / "021_block_c_tier3_pharmacology"
                   / "analysis" / "verification"
                   / "rescore_manifest_tier3_v2.provenance.json")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    provenance = build(
        rescore_manifest=args.rescore_manifest,
        campaign_manifest=args.campaign_manifest,
        out_path=args.out,
        provenance_out=args.provenance_out,
    )
    print(json.dumps(provenance, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
