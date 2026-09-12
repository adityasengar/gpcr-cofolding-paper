#!/usr/bin/env python3
"""Build Block C Tier 3 rescore manifest for scripts/rescore_parallel.py.

Reads:
  - pool queue ``<pool>/queue.csv`` (one row per seed job with populated
    prediction_sha, carries all provenance columns). The dispatch manifest
    at ``experiments/021_block_c_tier3_pharmacology/manifest/tier3_manifest.csv``
    has empty prediction_sha — the shas are computed at dispatch time.
  - queue state ``<pool>/queue_state.csv`` (skip rows that are not state=done)

For each done seed, globs the seed_<N> directory for its 10 model_*.cif
files (path is backbone-specific — boltz nests under
``boltz_results_<slug>/predictions/<slug>/``; chai/protenix/of3 flatten
model_*.cif at the seed root). Emits one rescore-manifest row per CIF.

Rescore-manifest columns (per rescore_parallel.py header):
  prediction_path, receptor_slug, state_claim, input_species,
  backbone, ligand_role, partner_type, partner_identity,
  ligand_bound_pdb, ligand_ccd, ligand_smiles_source

Usage:
  python3 scripts/build_block_c_tier3_rescore_manifest.py \\
      --pool-queue /hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/tier3/pool/queue.csv \\
      --queue-state /hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/tier3/pool/queue_state.csv \\
      --out experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

RESCORE_COLUMNS = (
    "prediction_path", "receptor_slug", "state_claim", "input_species",
    "backbone", "ligand_role", "partner_type", "partner_identity",
    "ligand_bound_pdb", "ligand_ccd", "ligand_smiles_source",
)


def _load_receptor_species_map(ref_set_csv: Path) -> dict[str, str]:
    """Read ``refs/reference_set.csv`` and return {receptor_upper: species}.

    Species is taken from a receptor's rows in reference_set.csv. When
    all rows for a receptor agree on species, that species is returned.
    When rows disagree (SMO has human+mouse rows, NTR1 has human+rat)
    the receptor maps to ``"AMBIGUOUS:<sp1>|<sp2>|..."`` — the
    preflight assertion will refuse to synthesise a manifest row for
    such receptors unless the caller has already stamped an explicit
    ``species`` on the pool-queue row.

    Rationale: the pre-Sep-2026 pool queue emitted empty ``species`` for
    non-human panel receptors (OPSD/bovin, B1B1U5/9arac, OPRM/mouse);
    the manifest builder then fell back to the ``"human"`` string, which
    caused 800 downstream A5 species-mismatch failures on the Tier 3
    v2 corpus (audit trail §21). This helper lifts the correct species
    from reference_set at manifest-build time so the fallback string
    is never silently used.
    """
    per_rec: dict[str, set[str]] = defaultdict(set)
    with ref_set_csv.open() as f:
        for row in csv.DictReader(f):
            rec = (row.get("receptor_slug") or "").strip().upper()
            sp = (row.get("species") or "").strip().lower()
            if rec and sp:
                per_rec[rec].add(sp)
    out: dict[str, str] = {}
    for rec, sps in per_rec.items():
        if len(sps) == 1:
            out[rec] = next(iter(sps))
        else:
            out[rec] = "AMBIGUOUS:" + "|".join(sorted(sps))
    return out


def _resolve_species(receptor: str,
                     queue_species: str,
                     species_map: dict[str, str]) -> str:
    """Choose the species for a manifest row.

    Priority: (1) an explicit non-empty pool-queue value, (2) the
    receptor→species mapping derived from reference_set.csv when
    unambiguous. Raise otherwise. The raise carries the receptor slug
    and the reference_set species set so the failure names the exact
    fix required.
    """
    rec_u = receptor.strip().upper()
    if queue_species and queue_species.strip():
        return queue_species.strip()
    lookup = species_map.get(rec_u, "")
    if not lookup:
        raise ValueError(
            f"Cannot resolve species for receptor={rec_u!r}: pool queue "
            f"has empty `species` and refs/reference_set.csv has no "
            f"row for this receptor. Add either an explicit species on "
            f"the pool queue row or a reference_set row before "
            f"building a manifest."
        )
    if lookup.startswith("AMBIGUOUS:"):
        raise ValueError(
            f"Ambiguous species for receptor={rec_u!r}: pool queue has "
            f"empty `species` and reference_set carries multiple "
            f"species ({lookup.split(':', 1)[1]}). Stamp an explicit "
            f"species on the pool queue row before building a manifest."
        )
    return lookup


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pool-queue", type=Path, required=True,
                    help="pool queue.csv (has populated prediction_sha column)")
    ap.add_argument("--queue-state", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--reference-set-csv", type=Path,
                    default=Path(__file__).resolve().parent.parent
                    / "refs" / "reference_set.csv",
                    help="reference_set.csv used to lift receptor→species "
                         "when the pool queue row's species field is empty")
    ap.add_argument("--allow-partial", action="store_true",
                    help="emit rows even when a seed dir has < 10 CIFs "
                         "(default: skip such dirs with a warning)")
    args = ap.parse_args()

    species_map = _load_receptor_species_map(args.reference_set_csv)

    # Read the pool queue.csv into a sha → row map.
    disp: dict[str, dict[str, str]] = {}
    with args.pool_queue.open() as f:
        for r in csv.DictReader(f):
            sha = r.get("prediction_sha", "")
            if sha:
                disp[sha] = r

    # Read queue_state.csv, filter to state=done.
    done_shas: set[str] = set()
    with args.queue_state.open() as f:
        for r in csv.DictReader(f):
            if r.get("state") == "done":
                done_shas.add(r["prediction_sha"])

    print(f"dispatch rows: {len(disp)}, done rows: {len(done_shas)}",
          file=sys.stderr)

    rows_out: list[dict] = []
    dir_missing = 0
    cifs_missing = 0
    partial = 0
    by_backbone: Counter = Counter()

    for sha in sorted(done_shas):
        d = disp.get(sha)
        if d is None:
            print(f"WARN: done sha not in dispatch manifest: {sha}",
                  file=sys.stderr)
            continue
        seed_cif = Path(d["prediction_path"])
        seed_dir = seed_cif.parent  # .../seed_<N>/
        if not seed_dir.exists():
            dir_missing += 1
            continue
        # Enumerate all model_*.cif in the seed dir (handles boltz nesting).
        cifs = sorted(seed_dir.rglob("*.cif"))
        # Filter to real model output files (skip _input_used.*.cif if any).
        cifs = [c for c in cifs if "_input_used" not in c.name and "_msa" not in c.name]
        if not cifs:
            cifs_missing += 1
            continue
        if len(cifs) < 10:
            partial += 1
            if not args.allow_partial:
                print(f"WARN: partial seed dir ({len(cifs)}/10 cifs): "
                      f"{seed_dir}", file=sys.stderr)
                continue
        bb = d.get("backbone", "")
        by_backbone[bb] += len(cifs)
        receptor_slug = d.get("receptor_resolved", "")
        # Lift species from reference_set.csv when the pool queue row's
        # `species` is empty. Raises with a receptor-named error if the
        # receptor is missing from reference_set or carries multiple
        # species (SMO, NTR1). This is the audit-#21 fix — do NOT fall
        # back to a hardcoded "human" default.
        resolved_species = _resolve_species(
            receptor_slug, d.get("species", ""), species_map,
        )
        for cif in cifs:
            rows_out.append({
                "prediction_path": str(cif),
                "receptor_slug": receptor_slug,
                "state_claim": d.get("state_claim", "Ga-coupled-active"),
                "input_species": resolved_species,
                "backbone": bb,
                "ligand_role": d.get("ligand_role", ""),
                "partner_type": d.get("partner_type", ""),
                "partner_identity": d.get("partner_identity", ""),
                "ligand_bound_pdb": d.get("ligand_bound_pdb", ""),
                "ligand_ccd": d.get("ligand_ccd", ""),
                "ligand_smiles_source": d.get("ligand_smiles_source", ""),
            })

    # Preflight assertion — no row may carry `input_species="human"`
    # for a receptor whose reference PDBs are non-human. This is the
    # audit-#21 guardrail: prior to the species-lift fix, 800 Tier 3
    # rows silently landed with input_species=human for OPSD (bovin)
    # and B1B1U5 (9arac), then failed the A5_species_match assertion
    # at scoring time. Catching it at manifest-build time surfaces the
    # bug BEFORE dispatch.
    for row in rows_out:
        rec = (row["receptor_slug"] or "").strip().upper()
        sp = (row["input_species"] or "").strip().lower()
        expected = species_map.get(rec, "")
        if not expected or expected.startswith("AMBIGUOUS:"):
            continue
        if sp and sp != expected:
            raise AssertionError(
                f"Preflight species mismatch: manifest row for "
                f"receptor={rec!r} carries input_species={sp!r} but "
                f"refs/reference_set.csv species for that receptor is "
                f"{expected!r}. This is exactly the audit-#21 "
                f"OPSD/B1B1U5 mis-tag class of failure. Refusing to "
                f"write the manifest."
            )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(RESCORE_COLUMNS))
        w.writeheader()
        w.writerows(rows_out)

    print(f"wrote {len(rows_out)} rows -> {args.out}", file=sys.stderr)
    print(f"  dir_missing={dir_missing} cifs_missing={cifs_missing} "
          f"partial_seed_dirs={partial}", file=sys.stderr)
    print(f"  per backbone: {dict(by_backbone)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
