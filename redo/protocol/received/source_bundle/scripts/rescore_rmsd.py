"""Rescore Block A predictions with backbone RMSD to the active + inactive
reference crystals — plan §1(a) primary deliverable.

Design
------
The delivered analysis reports Δd_tm6 (a signed scalar on one axis) and
never computed structural RMSD to the reference PDBs, even though those
CIFs are on disk. This script fills the gap.

Per prediction we compute:

    rmsd_to_active_ref     — CA RMSD to the receptor's active reference
    rmsd_to_inactive_ref   — CA RMSD to the receptor's inactive reference
    rmsd_pos               — rmsd_to_inactive / (rmsd_to_inactive + rmsd_to_active)
                             0 = at the active crystal
                             1 = at the inactive crystal

The RMSD is over the **common CA residue set** of prediction, active
reference, and inactive reference — that is, residues resolved in ALL
THREE structures. This automatically excises:

  - ICL3 wherever excised in either reference (nine Class A receptors
    have >50 ICL3 residues cut in one ref — the intersection drops
    them from the metric),
  - N-terminus and C-terminus wherever unresolved,
  - Fusion partners (T4L, BRIL, mini-G) which live on a different
    chain / at residues 1001+ and never overlap the receptor's UniProt
    numbering.

Chain selection uses ``scorer.structure.build_uniprot_model``: the
chain with the best UniProt-sequence identity, renumbered to UniProt
positions. Reference PDBs at ``refs/cache/pdb/<pdb_id>.cif``.

Output
------
A CSV mirroring the input rows plus four columns:
``rmsd_to_active_ref``, ``rmsd_to_inactive_ref``, ``rmsd_pos``,
``rmsd_n_residues_used``. The residue selection (min UniProt position,
max, count) is printed once per (receptor × arm × backbone) to stderr
for the audit log.

Class B/F portion of this rescore is dispatched by the same script —
the KNOWN_RECEPTORS gap for CRHR1/GCGR/FZD6 landed at 01ccdee.

Usage
-----
    python3 scripts/rescore_rmsd.py \
        --rows-csv experiments/018_block_a_switch_test/analysis/rows.csv \
        --reference-set refs/reference_set.csv \
        --refs-cache /home/sengaad1/paper_af3/refs/cache/pdb \
        --out-csv    experiments/018_block_a_switch_test/analysis/rows.rmsd.csv \
        [--limit N] [--class-filter A]

Runs CPU-only. Estimate ~20 min for 8,000 Class A predictions on one
qsub slot with warm caches.
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Optional

import gemmi

# scorer package is importable from repo root — the HPC venv has it
# installed editable; local dev tree has it on PYTHONPATH via
# pyproject.toml.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scorer.receptors import (
    EXPLICIT_DISAMBIG,
    KNOWN_RECEPTORS,
    UnresolvedReceptorError,
    receptor_class,
    resolve_receptor,
    uniprot_slug,
)


# =====================================================================
# Reference-set lookup
# =====================================================================


def load_reference_set(path: Path) -> dict[str, dict[str, str]]:
    """Return {receptor_slug_upper: {'active': pdb_id, 'inactive': pdb_id,
    'uniprot_slug': entry_name}}. Two rows per receptor (active +
    inactive) fold into one entry."""
    out: dict[str, dict[str, str]] = defaultdict(dict)
    with path.open() as f:
        for row in csv.DictReader(f):
            slug = (row.get("receptor_slug") or "").strip().upper()
            role = (row.get("role") or "").strip().lower()
            pdb = (row.get("pdb_id") or "").strip().lower()
            us = (row.get("uniprot_slug") or "").strip().lower()
            if not slug or not pdb or role not in ("active", "inactive"):
                continue
            out[slug][role] = pdb
            out[slug]["uniprot_slug"] = us
    return dict(out)


# =====================================================================
# CA extraction
# =====================================================================


def _load_ca_by_uniprot(
    path: Path,
    entry_name: str,
    build_model,
    api,
    warn_prefix: str = "",
) -> Optional[dict[int, gemmi.Position]]:
    """Load a structure and return {uniprot_pos: CA atom position}.
    Returns None on any load / chain-selection failure, printing a
    warning to stderr."""
    try:
        model = build_model(str(path), entry_name, api)
    except Exception as exc:
        print(f"WARN {warn_prefix} load-failed: {exc}", file=sys.stderr)
        return None
    ca: dict[int, gemmi.Position] = {}
    for uniprot_pos, residue in model.residues.items():
        # Use the same call scorer/axes.py uses:
        # find_atom(name, altloc_char). altloc "\0" picks the primary.
        atom = residue.find_atom("CA", "\0")
        if atom is None:
            for a in residue:
                if a.name == "CA":
                    atom = a
                    break
        if atom is None:
            continue
        ca[int(uniprot_pos)] = atom.pos
    if not ca:
        print(f"WARN {warn_prefix} no CA atoms extracted", file=sys.stderr)
        return None
    return ca


# Segments kept for the 7TM-only residue selection. Excludes N-terminus,
# C-terminus, all ECLs/ICLs, ECD (glycoprotein hormone receptors — FSHR,
# LSHR — carry ~290 leucine-rich-repeat residues N-terminal to TM1 that
# survive the current bidirectional intersection since references also
# include them), and H8 (helix-8, downstream of TM7).
_TM_SEGMENTS: frozenset[str] = frozenset({"TM1", "TM2", "TM3", "TM4", "TM5", "TM6", "TM7"})

# Cache: entry_name -> {uniprot_pos: segment_str}. Populated on demand
# from GPCRdb via bw_numbering.Api. Same api instance is threaded through.
_TM_RESIDUE_SET: dict[str, frozenset[int]] = {}


def _tm_residue_set(entry_name: str, api) -> frozenset[int]:
    """Return the set of UniProt positions annotated as TM1..TM7 for a
    receptor. Empty set if GPCRdb cannot resolve the entry — the caller
    treats "empty" as "no restriction" so residue selection degrades to
    the full common set (documented in `--restrict-to-tm`).
    """
    if entry_name in _TM_RESIDUE_SET:
        return _TM_RESIDUE_SET[entry_name]
    try:
        from scorer.bw_numbering import get_generic_numbers
        data = get_generic_numbers(api, entry_name)
    except Exception as exc:  # noqa: BLE001
        print(f"WARN TM-set fetch failed for {entry_name}: {exc}", file=sys.stderr)
        _TM_RESIDUE_SET[entry_name] = frozenset()
        return _TM_RESIDUE_SET[entry_name]
    tm = frozenset(
        int(pos) for pos, info in data.items()
        if (info.get("segment") or "").upper() in _TM_SEGMENTS
    )
    _TM_RESIDUE_SET[entry_name] = tm
    return tm


# =====================================================================
# Superposition + RMSD
# =====================================================================


def _superpose_rmsd(
    pred_ca: dict[int, gemmi.Position],
    ref_ca: dict[int, gemmi.Position],
    common: list[int],
) -> Optional[float]:
    """Return CA-RMSD of prediction onto reference over the given
    UniProt positions. Uses gemmi.superpose_positions (Kabsch)."""
    if len(common) < 20:
        return None
    pred_pts = [pred_ca[p] for p in common]
    ref_pts = [ref_ca[p] for p in common]
    try:
        # gemmi's Kabsch: aligns list[Position] against list[Position].
        sup = gemmi.superpose_positions(ref_pts, pred_pts)
    except Exception as exc:
        print(f"WARN superpose failed: {exc}", file=sys.stderr)
        return None
    return float(sup.rmsd)


# =====================================================================
# Per-row processing
# =====================================================================


def rescore_row(
    input_path: str,
    receptor_slug: str,
    ref_set: dict[str, dict[str, str]],
    refs_cache: Path,
    ref_ca_cache: dict[tuple[str, str], Optional[dict[int, gemmi.Position]]],
    build_model,
    api,
    residue_selection_log: dict[tuple[str, str], tuple[int, int, int]],
    restrict_to_tm: bool = True,
) -> dict[str, object]:
    """Return {'rmsd_to_active_ref', 'rmsd_to_inactive_ref', 'rmsd_pos',
    'rmsd_n_residues_used', 'rmsd_note'} for one prediction row."""
    out = {
        "rmsd_to_active_ref": "",
        "rmsd_to_inactive_ref": "",
        "rmsd_pos": "",
        "rmsd_n_residues_used": "",
        "rmsd_note": "",
    }
    slug = (receptor_slug or "").strip().upper()
    if not slug:
        out["rmsd_note"] = "empty_receptor_slug"
        return out
    if slug not in ref_set or "active" not in ref_set[slug] or "inactive" not in ref_set[slug]:
        out["rmsd_note"] = f"no_ref_pair_for_{slug}"
        return out
    entry_name = ref_set[slug]["uniprot_slug"]
    active_pdb = ref_set[slug]["active"]
    inactive_pdb = ref_set[slug]["inactive"]

    # Load references (cached across calls to amortise GPCRdb + file
    # I/O across the thousands of predictions per receptor).
    if (entry_name, active_pdb) not in ref_ca_cache:
        p = refs_cache / f"{active_pdb}.cif"
        ref_ca_cache[(entry_name, active_pdb)] = _load_ca_by_uniprot(
            p, entry_name, build_model, api,
            warn_prefix=f"active-ref {slug} {active_pdb}",
        )
    if (entry_name, inactive_pdb) not in ref_ca_cache:
        p = refs_cache / f"{inactive_pdb}.cif"
        ref_ca_cache[(entry_name, inactive_pdb)] = _load_ca_by_uniprot(
            p, entry_name, build_model, api,
            warn_prefix=f"inactive-ref {slug} {inactive_pdb}",
        )
    active_ca = ref_ca_cache[(entry_name, active_pdb)]
    inactive_ca = ref_ca_cache[(entry_name, inactive_pdb)]
    if active_ca is None or inactive_ca is None:
        out["rmsd_note"] = "ref_load_failed"
        return out

    # Load prediction
    pred_ca = _load_ca_by_uniprot(
        Path(input_path), entry_name, build_model, api,
        warn_prefix=f"pred {slug} {Path(input_path).name}",
    )
    if pred_ca is None:
        out["rmsd_note"] = "pred_load_failed"
        return out

    common = set(pred_ca) & set(active_ca) & set(inactive_ca)
    # Class-agnostic 7TM restriction. Per plan §14 step 4: FSHR/LSHR
    # carried 568/542 residues in the pre-fix RMSD, dominated by the
    # LRR ectodomain. Restrict to positions annotated as TM1..TM7 by
    # GPCRdb — auto-excises ECD (glycoprotein-hormone receptors),
    # ICL3 wherever excised, N/C-term, and H8. Applies uniformly to
    # Class A / B / F. If GPCRdb cannot resolve the entry, the TM set
    # comes back empty and we fall back to the full intersection with
    # a warning.
    if restrict_to_tm:
        tm_positions = _tm_residue_set(entry_name, api)
        if tm_positions:
            common = common & tm_positions
    common = sorted(common)
    if not common:
        out["rmsd_note"] = "no_common_residues"
        return out

    rmsd_a = _superpose_rmsd(pred_ca, active_ca, common)
    rmsd_i = _superpose_rmsd(pred_ca, inactive_ca, common)
    if rmsd_a is None or rmsd_i is None:
        out["rmsd_note"] = "superpose_failed"
        return out

    denom = rmsd_a + rmsd_i
    pos = (rmsd_i / denom) if denom > 0 else math.nan

    out["rmsd_to_active_ref"] = f"{rmsd_a:.4f}"
    out["rmsd_to_inactive_ref"] = f"{rmsd_i:.4f}"
    out["rmsd_pos"] = f"{pos:.4f}" if not math.isnan(pos) else ""
    out["rmsd_n_residues_used"] = str(len(common))

    # Log residue selection once per receptor
    key = (slug, entry_name)
    if key not in residue_selection_log:
        residue_selection_log[key] = (min(common), max(common), len(common))

    return out


# =====================================================================
# Main
# =====================================================================


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rows-csv", required=True, type=Path)
    ap.add_argument("--reference-set", required=True, type=Path)
    ap.add_argument("--refs-cache", required=True, type=Path,
                    help="dir with lowercase-<pdb_id>.cif reference files")
    ap.add_argument("--out-csv", required=True, type=Path)
    ap.add_argument("--limit", type=int, default=0,
                    help="process only the first N rows (0=all)")
    ap.add_argument("--class-filter", default="",
                    help="only rescore rows whose receptor is in this class (A/B/F)")
    ap.add_argument("--progress-every", type=int, default=200)
    ap.add_argument("--no-tm-restriction", action="store_true",
                    help="disable per-class 7TM-only residue filter "
                         "(plan §14 step 4). Not recommended.")
    args = ap.parse_args(argv)

    # Late import — scorer.structure requires gemmi + gpcrdb API and
    # only needs to be imported once we know we're going to run.
    from scorer.bw_numbering import Api
    from scorer.structure import build_uniprot_model

    # bw_numbering.Api requires a cache dir. The scorer standard is
    # refs/cache/gpcrdb — same as scorer/orchestrator.py.
    repo_root = Path(__file__).resolve().parent.parent
    api = Api(repo_root / "refs" / "cache" / "gpcrdb")
    build_model = build_uniprot_model

    ref_set = load_reference_set(args.reference_set)
    print(f"loaded {len(ref_set)} receptors from {args.reference_set}", file=sys.stderr)

    class_filter = args.class_filter.strip().upper()
    if class_filter and class_filter not in ("A", "B", "F"):
        raise SystemExit(f"--class-filter must be A/B/F; got {class_filter!r}")

    ref_ca_cache: dict[tuple[str, str], Optional[dict[int, gemmi.Position]]] = {}
    residue_selection_log: dict[tuple[str, str], tuple[int, int, int]] = {}

    with args.rows_csv.open() as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = list(reader.fieldnames or [])
        extra = ["rmsd_to_active_ref", "rmsd_to_inactive_ref", "rmsd_pos",
                 "rmsd_n_residues_used", "rmsd_note"]
        for e in extra:
            if e not in fieldnames:
                fieldnames.append(e)

        args.out_csv.parent.mkdir(parents=True, exist_ok=True)
        with args.out_csv.open("w", newline="") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()

            n_processed = 0
            n_ok = 0
            n_skipped_class = 0
            for row in reader:
                if args.limit and n_processed >= args.limit:
                    break
                slug = (row.get("receptor_slug") or "").strip().upper()
                if class_filter and slug:
                    try:
                        cls = receptor_class(slug)
                    except UnresolvedReceptorError:
                        cls = "?"
                    if cls != class_filter:
                        n_skipped_class += 1
                        row.update({k: "" for k in extra})
                        row["rmsd_note"] = f"class_filter_skipped_{cls}"
                        writer.writerow(row)
                        n_processed += 1
                        continue

                input_path = row.get("input_path") or ""
                try:
                    result = rescore_row(
                        input_path, slug, ref_set, args.refs_cache,
                        ref_ca_cache, build_model, api,
                        residue_selection_log,
                        restrict_to_tm=(not args.no_tm_restriction),
                    )
                except Exception as exc:
                    print(f"ERROR row {n_processed}: {exc}", file=sys.stderr)
                    traceback.print_exc(limit=2, file=sys.stderr)
                    result = {k: "" for k in extra}
                    result["rmsd_note"] = f"exception:{type(exc).__name__}"
                row.update(result)
                writer.writerow(row)
                n_processed += 1
                if result.get("rmsd_to_active_ref"):
                    n_ok += 1
                if n_processed % args.progress_every == 0:
                    print(
                        f"progress: {n_processed} rows processed, "
                        f"{n_ok} rescored, "
                        f"{n_skipped_class} class-skipped, "
                        f"{len(ref_ca_cache)} refs cached",
                        file=sys.stderr, flush=True,
                    )

    print(f"done: {n_processed} rows, {n_ok} rescored, "
          f"{n_skipped_class} class-skipped", file=sys.stderr)
    restriction = "7TM-only (GPCRdb-annotated TM1..TM7)" if not args.no_tm_restriction else "no restriction (full intersection)"
    print(f"residue selection rule: {restriction}", file=sys.stderr)
    print("residue selection per receptor (min-max, n):", file=sys.stderr)
    for (slug, entry), (lo, hi, n) in sorted(residue_selection_log.items()):
        print(f"  {slug:10s} {entry:20s} {lo:4d}-{hi:4d} n={n}", file=sys.stderr)
    # Write a header note to the output CSV so downstream analysis knows
    # the residue selection rule. Prepend a comment row via post-open
    # (csv.DictWriter doesn't do comments natively — inject at file top).
    header_path = args.out_csv.with_suffix(args.out_csv.suffix + ".selection_rule.txt")
    header_path.write_text(
        f"RMSD residue selection rule (plan §14 step 4):\n"
        f"  {restriction}\n"
        f"Uniform across Class A / B / F. Auto-excises ECD (glycoprotein-\n"
        f"hormone receptors), ICL3 wherever excised, N/C-terminus, H8.\n"
        f"Fallback to full intersection when GPCRdb cannot resolve the entry.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
