"""Diversity study analysis — per-experiment structural diversity stats.

Given one or more experiments' `rows.csv` files and the on-disk prediction
CIFs, emit:

    diversity_stats.csv     — one row per (system, backbone, strategy)
                              carrying:
        n_rows              (usually 10 per backbone-per-strategy)
        d_tm6_mean, _std, _min, _max, _range
        d_npxxy_mean, _std, _min, _max, _range
        n_above_midpoint    (# rows with d_tm6 > receptor midpoint)
        n_below_midpoint
        pairwise_rmsd_ca_median  — receptor-Cα-only pairwise RMSD median
        pairwise_rmsd_ca_max     — largest pairwise RMSD (Å)
        pairwise_rmsd_ca_min     — smallest pairwise RMSD (Å)
        pairwise_rmsd_ca_pairs   — number of pairs (n*(n-1)/2)

Pairwise Cα RMSD is computed via gemmi's superpose_positions on chain A
Cα only. Structures with different residue counts are aligned on their
UniProt-numbered overlap (per scorer.structure.build_uniprot_model
conventions — but here we skip the full UniProt renumber, we just take
chain A CA in residue-number order and cross-align on min-length).

Purely offline post-processing (no HPC, no scorer rerun) — feed the same
rows.csv the framework already emitted plus scratch access to the CIFs.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import gemmi


REPO = Path(__file__).resolve().parent.parent
DEFAULT_MIDPOINT = 13.13  # AA2AR midpoint per refs/state_thresholds.csv


# ---------------------------------------------------------------------------
# Chain-A Cα extraction
# ---------------------------------------------------------------------------


def _first_model(path: Path) -> gemmi.Model:
    """Read the first model from a CIF/PDB. Raises FileNotFoundError /
    RuntimeError on parse failure."""
    struct = gemmi.read_structure(str(path))
    if not struct:
        raise RuntimeError(f"could not parse {path}")
    return struct[0]


def chain_a_ca_positions(path: Path,
                         *, chain_id: str = "A",
                         resnum_lo: int | None = None,
                         resnum_hi: int | None = None,
                         ) -> tuple[list[gemmi.Position], list[int]]:
    """Return (Cα positions, residue-number list) for chain `chain_id`.

    Only picks up standard amino-acid residues with a real CA atom. Falls
    back to the FIRST chain if the requested chain isn't present (some
    backbones emit different chain letters — Chai in particular numbers
    the receptor chain "B" when the first FASTA record isn't chain A).

    When ``resnum_lo`` / ``resnum_hi`` are set (INCLUSIVE), residues
    outside the [lo, hi] range are dropped. This is how we exclude the
    intrinsically-disordered AA2AR N-terminus (residues 1-6) and
    C-terminus (~311-412) from the RMSD — those flexible tails wave
    around across seeds and dominate the raw all-CA RMSD by 8-10 Å even
    when the 7TM bundle is essentially identical. Restricting to the
    TM window gives a meaningful "how similar is the fold?" number.
    """
    model = _first_model(path)
    chain = None
    for ch in model:
        if ch.name == chain_id:
            chain = ch
            break
    if chain is None:
        chain = next(iter(model), None)
    if chain is None:
        raise RuntimeError(f"no chains in {path}")

    positions: list[gemmi.Position] = []
    resnums: list[int] = []
    for res in chain:
        # Skip non-amino-acid residues (waters, ligands)
        info = gemmi.find_tabulated_residue(res.name)
        if info is None or not info.is_amino_acid():
            continue
        num = int(res.seqid.num)
        if resnum_lo is not None and num < resnum_lo:
            continue
        if resnum_hi is not None and num > resnum_hi:
            continue
        ca = res.find_atom("CA", "\0")
        if ca is None:
            continue
        positions.append(ca.pos)
        resnums.append(num)
    return positions, resnums


# ---------------------------------------------------------------------------
# Pairwise Cα RMSD
# ---------------------------------------------------------------------------


def rmsd_ca_superposed(pos_a: list[gemmi.Position],
                       pos_b: list[gemmi.Position]) -> float:
    """Cα RMSD after Kabsch superposition on the shared prefix.

    Both structures must have the same Cα count for gemmi.superpose_positions
    to accept them. We take the min-length prefix — a safe default for
    same-sequence predictions where numbering shifts happen at the tails.
    Returns math.nan if the overlap is <4 residues (no sensible fit).
    """
    n = min(len(pos_a), len(pos_b))
    if n < 4:
        return math.nan
    a = pos_a[:n]
    b = pos_b[:n]
    sup = gemmi.superpose_positions(a, b)
    return float(sup.rmsd)


def pairwise_rmsd_ca(cif_paths: list[Path],
                     *, chain_id: str = "A",
                     resnum_lo: int | None = None,
                     resnum_hi: int | None = None,
                     ) -> dict[str, Any]:
    """Return the pairwise Cα-RMSD spread across a set of CIFs.

    Output dict:
        n_structures, n_pairs, median, max, min, all_pairs (list of
        (i, j, rmsd) tuples for the report), failed (paths that
        couldn't be parsed).
    """
    positions: list[tuple[Path, list[gemmi.Position]]] = []
    failed: list[str] = []
    for p in cif_paths:
        try:
            pos, _ = chain_a_ca_positions(
                p, chain_id=chain_id,
                resnum_lo=resnum_lo, resnum_hi=resnum_hi,
            )
        except (RuntimeError, OSError) as e:
            failed.append(f"{p}: {e}")
            continue
        positions.append((p, pos))

    n = len(positions)
    n_pairs = n * (n - 1) // 2
    pair_rmsds: list[float] = []
    all_pairs: list[tuple[int, int, float]] = []
    for i, j in itertools.combinations(range(n), 2):
        r = rmsd_ca_superposed(positions[i][1], positions[j][1])
        if not math.isnan(r):
            pair_rmsds.append(r)
            all_pairs.append((i, j, r))

    return {
        "n_structures": n,
        "n_pairs": len(pair_rmsds),
        "median": statistics.median(pair_rmsds) if pair_rmsds else math.nan,
        "max": max(pair_rmsds) if pair_rmsds else math.nan,
        "min": min(pair_rmsds) if pair_rmsds else math.nan,
        "mean": statistics.mean(pair_rmsds) if pair_rmsds else math.nan,
        "stdev": statistics.stdev(pair_rmsds) if len(pair_rmsds) > 1 else math.nan,
        "failed": failed,
        "all_pairs": all_pairs,
    }


# ---------------------------------------------------------------------------
# Diversity aggregator
# ---------------------------------------------------------------------------


@dataclass
class GroupStats:
    system: str
    backbone: str
    strategy: str        # "A_seeds" or "B_samples"
    n_rows: int
    d_tm6_values: list[float] = field(default_factory=list)
    d_npxxy_values: list[float] = field(default_factory=list)
    prediction_paths: list[str] = field(default_factory=list)
    midpoint: float = DEFAULT_MIDPOINT

    @staticmethod
    def _finite(xs: list[float]) -> list[float]:
        return [x for x in xs if isinstance(x, float) and not math.isnan(x)]

    def _agg(self, xs: list[float]) -> dict[str, float]:
        finite = self._finite(xs)
        if not finite:
            return {"n": 0, "mean": math.nan, "std": math.nan,
                    "min": math.nan, "max": math.nan, "range": math.nan}
        return {
            "n": len(finite),
            "mean": statistics.mean(finite),
            "std": statistics.stdev(finite) if len(finite) > 1 else 0.0,
            "min": min(finite),
            "max": max(finite),
            "range": max(finite) - min(finite),
        }

    def summary_row(self, rmsd_stats: dict[str, Any] | None = None
                    ) -> dict[str, Any]:
        tm6 = self._agg(self.d_tm6_values)
        npx = self._agg(self.d_npxxy_values)
        above = sum(1 for v in self._finite(self.d_tm6_values)
                    if v > self.midpoint)
        below = sum(1 for v in self._finite(self.d_tm6_values)
                    if v <= self.midpoint)
        row: dict[str, Any] = {
            "system": self.system,
            "backbone": self.backbone,
            "strategy": self.strategy,
            "n_rows": self.n_rows,
            "n_scored": tm6["n"],
            "d_tm6_mean": tm6["mean"],
            "d_tm6_std": tm6["std"],
            "d_tm6_min": tm6["min"],
            "d_tm6_max": tm6["max"],
            "d_tm6_range": tm6["range"],
            "d_npxxy_mean": npx["mean"],
            "d_npxxy_std": npx["std"],
            "d_npxxy_min": npx["min"],
            "d_npxxy_max": npx["max"],
            "d_npxxy_range": npx["range"],
            "n_above_midpoint": above,
            "n_below_midpoint": below,
        }
        if rmsd_stats is not None:
            row.update({
                "rmsd_ca_n_pairs": rmsd_stats["n_pairs"],
                "rmsd_ca_median": rmsd_stats["median"],
                "rmsd_ca_max": rmsd_stats["max"],
                "rmsd_ca_min": rmsd_stats["min"],
                "rmsd_ca_mean": rmsd_stats["mean"],
                "rmsd_ca_stdev": rmsd_stats["stdev"],
            })
        return row


# ---------------------------------------------------------------------------
# rows.csv → groups
# ---------------------------------------------------------------------------


def _to_float(x: str) -> float:
    try:
        return float(x)
    except (ValueError, TypeError):
        return math.nan


def load_group(rows_csv: Path, *, system: str, strategy: str,
               midpoint: float = DEFAULT_MIDPOINT
               ) -> dict[str, GroupStats]:
    """Return {backbone: GroupStats} from an experiments/<slug>/rows.csv."""
    if not rows_csv.exists() or rows_csv.stat().st_size == 0:
        return {}
    groups: dict[str, GroupStats] = {}
    with rows_csv.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            # ScorerRow writes the CIF path as `input_path` (that's the
            # column name in scorer/schema.py::ScorerRow). Detect backbone
            # from that; fall back to a `prediction_path` column if some
            # future consumer emits that alias.
            path = row.get("input_path") or row.get("prediction_path") or ""
            backbone = _detect_backbone(path)
            if not backbone:
                continue
            g = groups.setdefault(backbone, GroupStats(
                system=system, backbone=backbone, strategy=strategy,
                n_rows=0, midpoint=midpoint,
            ))
            g.n_rows += 1
            g.d_tm6_values.append(_to_float(row.get("d_tm6_r350_r630_ca", "")))
            g.d_npxxy_values.append(_to_float(row.get("d_npxxy_y558_y753_ca", "")))
            g.prediction_paths.append(path)
    return groups


_BACKBONE_HINTS = ("boltz", "of3", "protenix", "chai", "af2mm")


def _detect_backbone(path: str) -> str:
    """Detect backbone from the prediction path — e.g.
    `.../boltz/seed_N/...` or `.../of3/seed_N/...`. Returns "" when
    no known backbone segment is present."""
    parts = [p.lower() for p in path.split("/")]
    for hint in _BACKBONE_HINTS:
        if hint in parts:
            return hint
    return ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


# Experiments to analyse — (slug, system_label, strategy_label)
DEFAULT_EXPERIMENTS: list[tuple[str, str, str]] = [
    ("009_aa2ar_gs_seeds_diversity",       "aa2ar_gs",       "A_seeds"),
    ("010_aa2ar_gs_samples_diversity",     "aa2ar_gs",       "B_samples"),
    ("011_aa2ar_gs_neca_seeds_diversity",  "aa2ar_gs_neca",  "A_seeds"),
    ("012_aa2ar_gs_neca_samples_diversity","aa2ar_gs_neca",  "B_samples"),
    # (m, n) consensus study 2026-08-27 — same AA2AR+Gs+NECA system,
    # sweeping the (seeds × samples-per-seed) surface.
    ("013_aa2ar_gs_neca_mn_5_1",           "aa2ar_gs_neca",  "mn_5_1"),
    ("014_aa2ar_gs_neca_mn_1_5",           "aa2ar_gs_neca",  "mn_1_5"),
    ("015_aa2ar_gs_neca_mn_5_5",           "aa2ar_gs_neca",  "mn_5_5"),
    ("016_aa2ar_gs_neca_mn_20_1",          "aa2ar_gs_neca",  "mn_20_1"),
    ("017_aa2ar_gs_neca_mn_1_20",          "aa2ar_gs_neca",  "mn_1_20"),
]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Emit diversity_stats.csv from the diversity study experiments."
    )
    p.add_argument("--experiments-root",
                   default=str(REPO / "experiments"),
                   type=Path)
    p.add_argument("--out",
                   default=str(REPO / "docs" / "diversity_stats.csv"),
                   type=Path)
    p.add_argument("--out-json",
                   default=str(REPO / "docs" / "diversity_stats.json"),
                   type=Path)
    p.add_argument("--midpoint", type=float, default=DEFAULT_MIDPOINT,
                   help=f"AA2AR d_tm6 active/inactive midpoint (default {DEFAULT_MIDPOINT})")
    p.add_argument("--skip-rmsd", action="store_true",
                   help="Skip the pairwise Cα RMSD computation (much faster).")
    p.add_argument("--tm-window-lo", type=int, default=7,
                   help="Inclusive lower residue number for Cα RMSD "
                        "restriction (default 7 — AA2AR TM1 start). "
                        "Set to 0 to include everything.")
    p.add_argument("--tm-window-hi", type=int, default=311,
                   help="Inclusive upper residue number for Cα RMSD "
                        "restriction (default 311 — AA2AR TM7 end). "
                        "Set to a very large number to include the "
                        "flexible C-tail.")
    p.add_argument("--experiment", action="append", default=None,
                   help="Restrict to one or more experiment slugs.")
    args = p.parse_args(argv)

    exp_list = list(DEFAULT_EXPERIMENTS)
    if args.experiment:
        wanted = set(args.experiment)
        exp_list = [t for t in exp_list if t[0] in wanted]

    rows_out: list[dict[str, Any]] = []
    json_out: dict[str, Any] = {}
    for slug, system, strategy in exp_list:
        exp_dir = args.experiments_root / slug
        rows_csv = exp_dir / "rows.csv"
        groups = load_group(rows_csv, system=system, strategy=strategy,
                            midpoint=args.midpoint)
        if not groups:
            print(f"[warn] no groups extracted from {rows_csv}",
                  file=sys.stderr)
            json_out[slug] = {"warning": "empty or missing rows.csv"}
            continue
        for backbone, g in sorted(groups.items()):
            rmsd_stats = None
            if not args.skip_rmsd:
                cif_paths = [Path(p) for p in g.prediction_paths]
                # Chai's Cα chain letter is inconsistent — accept first
                # chain fallback (chain_a_ca_positions handles it).
                lo = args.tm_window_lo if args.tm_window_lo > 0 else None
                hi = args.tm_window_hi if args.tm_window_hi > 0 else None
                rmsd_stats = pairwise_rmsd_ca(
                    cif_paths, chain_id="A",
                    resnum_lo=lo, resnum_hi=hi,
                )
            summary = g.summary_row(rmsd_stats)
            rows_out.append(summary)
            json_out.setdefault(slug, {})[backbone] = summary
            print(f"{slug:44s} {backbone:10s} n={summary['n_scored']:2d} "
                  f"d_tm6_std={summary['d_tm6_std']:.3f} "
                  f"d_npxxy_std={summary['d_npxxy_std']:.3f}"
                  + (f" rmsd_med={summary.get('rmsd_ca_median', float('nan')):.3f}"
                     if rmsd_stats is not None else ""),
                  file=sys.stderr)

    if rows_out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        cols = list(rows_out[0].keys())
        with args.out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows_out:
                w.writerow(r)
        print(f"wrote {args.out}", file=sys.stderr)
    if json_out:
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(json.dumps(json_out, indent=2, default=str))
        print(f"wrote {args.out_json}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
