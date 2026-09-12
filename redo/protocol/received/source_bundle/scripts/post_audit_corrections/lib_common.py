"""Shared helpers for post-audit correction scripts (2026-09-05)."""
from __future__ import annotations
import csv, hashlib, math, random, statistics, subprocess, datetime as dt
from pathlib import Path
from typing import Sequence

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


def to_float(x):
    if x is None or x == "" or str(x).lower() in ("nan", "none"):
        return float("nan")
    try:
        return float(x)
    except (ValueError, TypeError):
        return float("nan")


def _mean(xs):
    xs2 = [x for x in xs if not math.isnan(x)]
    return statistics.fmean(xs2) if xs2 else float("nan")


def load_rows(rows_csv, manifest_csv=None):
    """Load rescore-v2 rows, joining backbone/partner_type/ligand_role
    from the rescore manifest keyed on input_path == prediction_path."""
    with open(rows_csv) as f:
        rows = list(csv.DictReader(f))
    if manifest_csv:
        m_by_path = {}
        with open(manifest_csv) as f:
            for r in csv.DictReader(f):
                m_by_path[r["prediction_path"]] = r
        for row in rows:
            m = m_by_path.get(row.get("input_path", ""))
            if m is None:
                continue
            row.setdefault("backbone", m.get("backbone", ""))
            row.setdefault("partner_type", m.get("partner_type", ""))
            if not row.get("ligand_role"):
                row["ligand_role"] = m.get("ligand_role", "")
            # keep original manifest ligand_bound_pdb for same-complex join
            row.setdefault("ligand_bound_pdb", m.get("ligand_bound_pdb", ""))
    return rows


def load_ref_set(path):
    """{receptor_upper: {"active": [rows], "inactive": [rows]}}"""
    out = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            recep = (row.get("receptor_slug") or "").strip().upper()
            role = (row.get("role") or "").strip().lower()
            if not recep or role not in ("active", "inactive"):
                continue
            out.setdefault(recep, {"active": [], "inactive": []})
            out[recep][role].append(row)
    return out


def load_ligand_bound_pdbs(paths):
    """Combine ligand_set.csv + ligand_set_tier3.csv; later files win.
    Returns {(receptor_upper, role_lower): bound_pdb_upper_or_empty}."""
    out = {}
    for path in paths:
        with open(path) as f:
            for r in csv.DictReader(f):
                rec = r["receptor"].strip().upper()
                role = r["ligand_role"].strip().lower()
                pdb = (r.get("bound_pdb") or "").strip().upper()
                if len(pdb) != 4 or not pdb.isalnum():
                    pdb = ""
                if pdb:
                    out[(rec, role)] = pdb
    return out


def cluster_bootstrap_diff(a_by_r, b_by_r, n_iter=5000, seed=42):
    """Bootstrap CI over receptors for (mean_a − mean_b) using
    per-receptor cell means. Returns dict with est, ci_lo, ci_hi,
    n_clusters, signed_nonzero."""
    common = sorted(set(a_by_r) & set(b_by_r))
    if len(common) < 2:
        return {"est": float("nan"), "ci_lo": float("nan"),
                "ci_hi": float("nan"), "n_clusters": len(common),
                "signed_nonzero": False,
                "n_a_rows": sum(len(v) for v in a_by_r.values()),
                "n_b_rows": sum(len(v) for v in b_by_r.values())}
    rng = random.Random(seed)
    reps = []
    for _ in range(n_iter):
        s = [rng.choice(common) for _ in range(len(common))]
        ma = _mean([v for c in s for v in a_by_r[c]])
        mb = _mean([v for c in s for v in b_by_r[c]])
        if math.isnan(ma) or math.isnan(mb):
            continue
        reps.append(ma - mb)
    reps.sort()
    pt = (_mean([v for c in common for v in a_by_r[c]])
          - _mean([v for c in common for v in b_by_r[c]]))
    lo = reps[max(0, int(len(reps)*0.025) - 1)] if reps else float("nan")
    hi = reps[min(len(reps)-1, int(len(reps)*0.975))] if reps else float("nan")
    signed = (not (math.isnan(lo) or math.isnan(hi))
              and ((lo > 0 and hi > 0) or (lo < 0 and hi < 0)))
    return {"est": pt, "ci_lo": lo, "ci_hi": hi, "n_clusters": len(common),
            "signed_nonzero": signed,
            "n_a_rows": sum(len(v) for v in a_by_r.values()),
            "n_b_rows": sum(len(v) for v in b_by_r.values())}


def cluster_bootstrap_two_group_diff(group_a, group_b, n_iter=5000, seed=99):
    """Bootstrap CI for (mean of group_a) − (mean of group_b) where
    group_a and group_b are disjoint sets of cluster→[values] dicts.
    Each iteration resamples clusters within each group with replacement."""
    ka = list(group_a.keys())
    kb = list(group_b.keys())
    if not ka or not kb:
        return {"est": float("nan"), "ci_lo": float("nan"),
                "ci_hi": float("nan"), "n_a": len(ka), "n_b": len(kb),
                "signed_nonzero": False}
    rng = random.Random(seed)
    reps = []
    for _ in range(n_iter):
        sa = [rng.choice(ka) for _ in range(len(ka))]
        sb = [rng.choice(kb) for _ in range(len(kb))]
        ma = _mean([v for c in sa for v in group_a[c]])
        mb = _mean([v for c in sb for v in group_b[c]])
        if math.isnan(ma) or math.isnan(mb):
            continue
        reps.append(ma - mb)
    reps.sort()
    pt = (_mean([v for c in ka for v in group_a[c]])
          - _mean([v for c in kb for v in group_b[c]]))
    lo = reps[max(0, int(len(reps)*0.025) - 1)] if reps else float("nan")
    hi = reps[min(len(reps)-1, int(len(reps)*0.975))] if reps else float("nan")
    signed = (not (math.isnan(lo) or math.isnan(hi))
              and ((lo > 0 and hi > 0) or (lo < 0 and hi < 0)))
    return {"est": pt, "ci_lo": lo, "ci_hi": hi,
            "n_a": len(ka), "n_b": len(kb), "signed_nonzero": signed}


def cluster_bootstrap_interaction(agA, agI, anA, anI, n_iter=5000, seed=1234):
    """Bootstrap CI over receptors for interaction:
    (agonist_active − antag_active) − (agonist_inactive − antag_inactive)."""
    common = sorted(set(agA) & set(agI) & set(anA) & set(anI))
    if len(common) < 2:
        return {"est": float("nan"), "ci_lo": float("nan"),
                "ci_hi": float("nan"), "n_clusters": len(common),
                "signed_nonzero": False}
    rng = random.Random(seed)
    reps = []
    for _ in range(n_iter):
        s = [rng.choice(common) for _ in range(len(common))]
        ma_a = _mean([v for c in s for v in agA[c]])
        ma_i = _mean([v for c in s for v in agI[c]])
        mb_a = _mean([v for c in s for v in anA[c]])
        mb_i = _mean([v for c in s for v in anI[c]])
        if any(math.isnan(x) for x in (ma_a, ma_i, mb_a, mb_i)):
            continue
        reps.append((ma_a - mb_a) - (ma_i - mb_i))
    reps.sort()
    ma_a = _mean([v for c in common for v in agA[c]])
    ma_i = _mean([v for c in common for v in agI[c]])
    mb_a = _mean([v for c in common for v in anA[c]])
    mb_i = _mean([v for c in common for v in anI[c]])
    pt = (ma_a - mb_a) - (ma_i - mb_i)
    lo = reps[max(0, int(len(reps)*0.025) - 1)] if reps else float("nan")
    hi = reps[min(len(reps)-1, int(len(reps)*0.975))] if reps else float("nan")
    signed = (not (math.isnan(lo) or math.isnan(hi))
              and ((lo > 0 and hi > 0) or (lo < 0 and hi < 0)))
    return {"est": pt, "ci_lo": lo, "ci_hi": hi, "n_clusters": len(common),
            "signed_nonzero": signed}


def build_recon_meta(inputs: dict):
    """Common reconstruction dict — script git SHA + sha256 of every
    input file. `inputs` is {name: path}."""
    out = {"reconstruction_script_git_sha": git_sha(),
           "generated_at_utc": now_utc(),
           "inputs": {}}
    for name, path in inputs.items():
        p = Path(path)
        out["inputs"][name] = {"path": str(p.resolve()),
                               "sha256": sha256(p) if p.exists() else "missing"}
    return out
