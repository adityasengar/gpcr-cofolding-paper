#!/usr/bin/env python3
"""Task Cohen's d — Block A d_tm6_r350_r630_ca, cognate vs apo, Class A.

Effect-size pin for the Tier 3 headline rewrite. Tier 3 (§2.1 of
`experiments/021_block_c_tier3_pharmacology/analysis/tier3_headline_2026_09_05.md`)
quotes SEALED §2.7 Class A median Delta d_tm6 per backbone but has no
pinned Cohen's d verification JSON. This script produces that pin.

Method
------
Per backbone x receptor (Class A only, both arms present):

  d_receptor = (mean_cognate - mean_apo) / pooled_SD

  pooled_SD  = sqrt( ((n_c - 1) * s_c^2 + (n_a - 1) * s_a^2)
                     / (n_c + n_a - 2) )

Per backbone point estimate = arithmetic mean of receptor-level d.

Cluster bootstrap: 10,000 replicates, receptors sampled WITH replacement
within each backbone stratum. 95 % CI = 2.5th / 97.5th percentile of the
replicate distribution.

Verdicts (magnitude on |mean d|):

  NULL             CI includes 0
  LARGE_EFFECT     |d| >= 0.8 and CI excludes 0
  MEDIUM_EFFECT    0.5 <= |d| < 0.8 and CI excludes 0
  SMALL_EFFECT     0.2 <= |d| < 0.5 and CI excludes 0
  NEGLIGIBLE       |d| < 0.2 and CI excludes 0

Determinism: `--seed` (default 20260906) fully pins bootstrap draws so
the output JSON is byte-reproducible under the same input SHA-256s and
script git SHA.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, random, re, statistics, subprocess
import datetime as dt
from collections import defaultdict
from pathlib import Path

REPO = Path("/Users/SENGAAD1/Documents/claude/paper_af3")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def git_sha():
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return "unknown"


def now_utc():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


BACKBONE_RE = re.compile(r"/(chai|of3|boltz|protenix)/seed_")
BACKBONES = ("boltz", "chai", "of3", "protenix")
STATE_TO_ARM = {"apo": "apo", "Ga-coupled-active": "cognate"}


def _to_float(x):
    if x is None or x == "" or str(x).lower() in ("nan", "none"):
        return None
    try:
        v = float(x)
    except (ValueError, TypeError):
        return None
    if math.isnan(v):
        return None
    return v


def _pooled_sd(values_c, values_a):
    n_c, n_a = len(values_c), len(values_a)
    if n_c < 2 or n_a < 2:
        return None
    s_c = statistics.stdev(values_c)
    s_a = statistics.stdev(values_a)
    denom = n_c + n_a - 2
    if denom <= 0:
        return None
    var = ((n_c - 1) * s_c * s_c + (n_a - 1) * s_a * s_a) / denom
    if var < 0:
        return None
    sd = math.sqrt(var)
    return sd if sd > 0 else None


def _cohens_d(values_c, values_a):
    if not values_c or not values_a:
        return None
    sd = _pooled_sd(values_c, values_a)
    if sd is None:
        return None
    return (statistics.fmean(values_c) - statistics.fmean(values_a)) / sd


def _verdict(d_pt, ci_lo, ci_hi):
    if math.isnan(d_pt) or math.isnan(ci_lo) or math.isnan(ci_hi):
        return "INSUFFICIENT_DATA"
    if ci_lo <= 0 <= ci_hi:
        return "NULL"
    ad = abs(d_pt)
    if ad >= 0.8:
        return "LARGE_EFFECT"
    if ad >= 0.5:
        return "MEDIUM_EFFECT"
    if ad >= 0.2:
        return "SMALL_EFFECT"
    return "NEGLIGIBLE"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--rows-pocket", type=Path,
        default=REPO / "experiments/018_block_a_switch_test"
                       "/analysis/rows.pocket.csv",
    )
    ap.add_argument(
        "--coupling", type=Path,
        default=REPO / "refs/gpcr_coupling.csv",
    )
    ap.add_argument(
        "--out", type=Path,
        default=REPO / "experiments/018_block_a_switch_test"
                       "/analysis/verification"
                       "/cohens_d_block_a_d_tm6.json",
    )
    ap.add_argument("--n-bootstrap", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20260906)
    args = ap.parse_args()

    # per (backbone, receptor, arm) -> list of d_tm6 values
    per_cell = defaultdict(list)
    n_seeds_per_cell = defaultdict(set)
    n_samples_per_cell = defaultdict(int)
    class_a_receptors = set()

    with open(args.rows_pocket) as f:
        for r in csv.DictReader(f):
            if r.get("passed") != "True":
                continue
            if (r.get("receptor_class") or "").upper() != "A":
                continue
            state = r.get("input_state_claim") or ""
            arm = STATE_TO_ARM.get(state)
            if arm is None:
                continue
            m = BACKBONE_RE.search(r.get("input_path") or "")
            if not m:
                continue
            bb = m.group(1)
            rec = (r.get("receptor_slug") or "").upper()
            if not rec:
                continue
            v = _to_float(r.get("d_tm6_r350_r630_ca"))
            if v is None:
                continue
            per_cell[(bb, rec, arm)].append(v)
            seed = (r.get("seed_used") or "").strip()
            if seed:
                n_seeds_per_cell[(bb, rec, arm)].add(seed)
            n_samples_per_cell[(bb, rec, arm)] += 1
            class_a_receptors.add(rec)

    # Verify (5, 5) uniform stamp is at least approximately true.
    n_seeds_snapshot = statistics.median(
        len(s) for s in n_seeds_per_cell.values()) if n_seeds_per_cell else 0
    n_samples_snapshot = statistics.median(
        n_samples_per_cell.values()) if n_samples_per_cell else 0

    receptors_sorted = sorted(class_a_receptors)

    per_backbone_out = {}
    for bb in BACKBONES:
        recs_with_both = []
        per_rec_d = {}
        per_rec_delta = {}
        per_rec_stats = {}
        for rec in receptors_sorted:
            cog = per_cell.get((bb, rec, "cognate"), [])
            apo = per_cell.get((bb, rec, "apo"), [])
            d_r = _cohens_d(cog, apo)
            if d_r is None:
                continue
            recs_with_both.append(rec)
            per_rec_d[rec] = d_r
            per_rec_delta[rec] = statistics.fmean(cog) - statistics.fmean(apo)
            per_rec_stats[rec] = {
                "n_cognate": len(cog),
                "n_apo": len(apo),
                "mean_cognate": statistics.fmean(cog),
                "mean_apo": statistics.fmean(apo),
                "sd_cognate": statistics.stdev(cog) if len(cog) > 1 else 0.0,
                "sd_apo": statistics.stdev(apo) if len(apo) > 1 else 0.0,
                "cohens_d": d_r,
                "delta_d_tm6_A": per_rec_delta[rec],
            }

        d_values = [per_rec_d[r] for r in recs_with_both]
        delta_values = [per_rec_delta[r] for r in recs_with_both]

        if not d_values:
            per_backbone_out[bb] = {
                "cohens_d_point": float("nan"),
                "cohens_d_ci_low": float("nan"),
                "cohens_d_ci_high": float("nan"),
                "median_delta_d_tm6_A": float("nan"),
                "n_receptors": 0,
                "verdict": "INSUFFICIENT_DATA",
                "per_receptor": {},
            }
            continue

        point_d = statistics.fmean(d_values)
        median_delta = statistics.median(delta_values)

        # Cluster-bootstrap resample of receptors within this backbone.
        # Seed is per-backbone (base seed XORed with a stable per-backbone
        # offset) so results are deterministic AND cross-backbone
        # independent.
        bb_seed = args.seed ^ (0x9e3779b1 * (BACKBONES.index(bb) + 1)) & 0xFFFFFFFF
        rng = random.Random(bb_seed)
        replicates = []
        n = len(recs_with_both)
        for _ in range(args.n_bootstrap):
            sample = [rng.choice(recs_with_both) for _ in range(n)]
            replicates.append(statistics.fmean(per_rec_d[r] for r in sample))
        replicates.sort()
        lo_idx = max(0, int(math.floor(args.n_bootstrap * 0.025)) - 1)
        hi_idx = min(args.n_bootstrap - 1,
                     int(math.ceil(args.n_bootstrap * 0.975)) - 1)
        ci_lo = replicates[lo_idx]
        ci_hi = replicates[hi_idx]
        verdict = _verdict(point_d, ci_lo, ci_hi)

        per_backbone_out[bb] = {
            "cohens_d_point": point_d,
            "cohens_d_ci_low": ci_lo,
            "cohens_d_ci_high": ci_hi,
            "median_delta_d_tm6_A": median_delta,
            "n_receptors": n,
            "verdict": verdict,
            "bootstrap_seed": bb_seed,
            "per_receptor": per_rec_stats,
        }

    # Intersection across backbones — receptors present in every backbone
    # with both arms and both cells >= 2 samples (Cohen's d defined).
    common_receptors = set(receptors_sorted)
    for bb in BACKBONES:
        common_receptors &= set(per_backbone_out[bb].get("per_receptor", {}))
    common_sorted = sorted(common_receptors)

    out = {
        "analysis_type": "block_a_cohens_d_d_tm6_r350_r630_ca_cognate_vs_apo_class_A",
        "reconstruction": {
            "reconstruction_script": str(Path(__file__).resolve()),
            "reconstruction_script_git_sha": git_sha(),
            "generated_at_utc": now_utc(),
            "bootstrap_seed_base": args.seed,
            "n_bootstrap_replicates": args.n_bootstrap,
            "resample_scheme": (
                "Cluster bootstrap: within each backbone, resample "
                "the n_receptors receptors WITH replacement 10,000 times; "
                "each replicate's statistic is the arithmetic mean of "
                "receptor-level Cohen's d. 95% CI = percentiles [2.5, 97.5]."
            ),
            "cohens_d_definition": (
                "d_r = (mean_cognate - mean_apo) / pooled_SD; "
                "pooled_SD = sqrt( ((n_c-1)*s_c^2 + (n_a-1)*s_a^2) / "
                "(n_c + n_a - 2) )."
            ),
            "point_estimate_definition": (
                "Per-backbone Cohen's d point estimate = mean over "
                "receptors of receptor-level d. Median delta d_tm6 is the "
                "median over receptors of (mean_cognate - mean_apo)."
            ),
            "inputs": {
                "rows_pocket": {
                    "path": str(args.rows_pocket),
                    "sha256": sha256(args.rows_pocket),
                },
                "coupling_csv": {
                    "path": str(args.coupling),
                    "sha256": sha256(args.coupling),
                },
            },
        },
        "filter": {
            "receptor_class": "A",
            "passed": True,
            "arm_state_map": STATE_TO_ARM,
            "d_column": "d_tm6_r350_r630_ca",
        },
        "verdict_schema": {
            "LARGE_EFFECT": "|d| >= 0.8 and 95% CI excludes 0",
            "MEDIUM_EFFECT": "0.5 <= |d| < 0.8 and 95% CI excludes 0",
            "SMALL_EFFECT": "0.2 <= |d| < 0.5 and 95% CI excludes 0",
            "NEGLIGIBLE": "|d| < 0.2 and 95% CI excludes 0",
            "NULL": "95% CI includes 0",
        },
        "n_class_a_receptors_total": len(receptors_sorted),
        "n_receptors_in_common": len(common_sorted),
        "receptors_in_common": common_sorted,
        "n_seeds": n_seeds_snapshot,
        "n_samples": n_samples_snapshot,
        "per_backbone": per_backbone_out,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2, default=str)

    # Console table.
    print(f"wrote {args.out}")
    print()
    print("Block A Cohen's d, d_tm6_r350_r630_ca (cognate - apo), Class A")
    print("-" * 78)
    hdr = f"{'backbone':<10}{'n_rec':>6}{'median Δd_tm6 [Å]':>22}"
    hdr += f"{'Cohen d':>10}{'  95% CI':>18}   verdict"
    print(hdr)
    print("-" * 78)
    for bb in BACKBONES:
        b = per_backbone_out[bb]
        print(
            f"{bb:<10}{b['n_receptors']:>6}"
            f"{b['median_delta_d_tm6_A']:>22.3f}"
            f"{b['cohens_d_point']:>10.3f}"
            f"  [{b['cohens_d_ci_low']:>+6.3f}, {b['cohens_d_ci_high']:>+6.3f}]"
            f"   {b['verdict']}"
        )


if __name__ == "__main__":
    main()
