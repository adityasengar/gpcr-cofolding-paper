#!/usr/bin/env python3
"""Analysis driver — build the fold-integrity report for a Block A- or
Block B-shaped campaign.

Reads rows.csv + rows.fold_integrity.csv (joined on input_path), optionally
merges in RMSD-to-active/inactive from rows.rmsd.csv for the "off-pathway"
diagnostic (RMSD-to-active > 3 A AND RMSD-to-inactive > 3 A per Block C
plan §7 confound #4), and emits a per-arm x per-backbone artefact-rate
report as Markdown.

Block A shape (2 arms: apo, cognate) and Block B shape (4 arms: apo,
cognate, shuffled, decoy) are BOTH supported via CLI. Arm label can be
sourced from either the `input_state_claim` column (Block A: two-value
column) or from the `input_path` (Block B: single value collapses three
arms into 'Ga-coupled-active', so we regex the arm out of the experiment
directory name). `--arm-source path|column` picks between the two.

Legacy CLI-free invocation is preserved: running with no args reproduces
the Block A analysis exactly (defaults point at
`experiments/018_block_a_switch_test/analysis/`).

The RMSD merge is OPTIONAL — pass `--rmsd <path>` to include the
off-pathway table. Default: skipped, no rmsd import needed.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


UNWOUND_THRESHOLD = 0.80  # candidate "TM6 unwound" cut on task-defined helicity
PANEL_NPXXY_THRESHOLD = 9.082  # per BLOCK_B_PRE_DISPATCH_DECISIONS_2026_09_02.md
TILT_ACTIVE_THRESHOLD = 14.932  # per PREREG §16 lock — Block B active-call primary
OFF_PATHWAY_RMSD_THRESHOLD = 3.0  # per Block C plan §7 confound #4


# Regex extracts arm + backbone from Block-B-style experiment directory
# names like `019_block_b_partner_selection_5ht1b_apo_boltz`.
BLOCK_B_ARM_RE = re.compile(
    r"019_block_b_partner_selection_[^/_]+_(apo|cognate|shuffled|decoy)_"
    r"(boltz|chai|of3|protenix)"
)

# All Block B arms in canonical order.
BLOCK_B_ARMS = ("apo", "decoy", "shuffled", "cognate")

# All Block A arms (in `input_state_claim` values).
BLOCK_A_ARMS = ("apo", "Ga-coupled-active")

BACKBONES = ("boltz", "chai", "of3", "protenix")


def _f(x: str) -> float:
    try:
        return float(x)
    except Exception:
        return float("nan")


def _bb(path: str) -> str:
    for b in BACKBONES:
        if f"/{b}/" in path:
            return b
    return "?"


def _arm_from_path(path: str) -> str:
    """Recover the arm label from a Block-B-style input_path."""
    m = BLOCK_B_ARM_RE.search(path)
    return m.group(1) if m else "?"


def load(
    rows_csv: Path,
    fi_csv: Path,
    arm_source: str,
    rmsd_csv: Path | None,
) -> list[dict]:
    """Join rows.csv + rows.fold_integrity.csv (+ optional rows.rmsd.csv).

    Emits one dict per input_path present in BOTH rows.csv and fi_csv.
    Rows in rows.csv without a fold-integrity entry are silently skipped
    (the driver either processed them and they surfaced load errors, or
    the driver has not caught up — either case the report should not
    fabricate values). The final row count is emitted at load time.
    """
    fi: dict[str, dict[str, str]] = {}
    with fi_csv.open() as f:
        first = f.readline()
        assert first.startswith("# rules:"), first[:40]
        for row in csv.DictReader(f):
            fi[row["input_path"]] = row

    rmsd_by_path: dict[str, dict[str, str]] = {}
    if rmsd_csv is not None:
        with rmsd_csv.open() as f:
            for row in csv.DictReader(f):
                rmsd_by_path[row["input_path"]] = row

    out: list[dict] = []
    n_missing_fi = 0
    n_missing_rmsd = 0
    with rows_csv.open() as f:
        for row in csv.DictReader(f):
            p = row["input_path"]
            r = fi.get(p)
            if r is None:
                n_missing_fi += 1
                continue
            if r.get("load_error"):
                # a CIF that failed to load has no meaningful metrics; skip
                # rather than propagate NaN as a "silently missing" signal.
                continue
            row["tm6_helicity_6_30_6_50"] = _f(r["tm6_helicity_6_30_6_50"])
            try:
                row["chain_breaks"] = int(r["chain_breaks"])
            except Exception:
                row["chain_breaks"] = -1
            row["ramachandran_outlier_frac"] = _f(r["ramachandran_outlier_frac"])
            row["icl3_modelled_count"] = _f(r["icl3_modelled_count"])
            row["backbone"] = _bb(p)

            # arm resolution
            if arm_source == "column":
                row["arm"] = row.get("input_state_claim", "?")
            elif arm_source == "path":
                row["arm"] = _arm_from_path(p)
            else:
                raise ValueError(f"invalid arm_source: {arm_source}")

            # NPxxY-OH active-call predicate (Block A precedent; strict
            # comparability to the 2.11% baseline number).
            row["d_npxxy_oh"] = _f(row.get("d_npxxy_y558_y753_oh", ""))
            # GPCRdb TM6 tilt active-call predicate (Block B primary,
            # per PREREG §16).
            row["d_tilt"] = _f(row.get("d_gpcrdb_tm6_tilt_246_637_ca", ""))

            # optional RMSD merge for off-pathway diagnostic
            if rmsd_csv is not None:
                rr = rmsd_by_path.get(p)
                if rr is None:
                    n_missing_rmsd += 1
                    row["rmsd_to_active"] = float("nan")
                    row["rmsd_to_inactive"] = float("nan")
                else:
                    row["rmsd_to_active"] = _f(rr.get("rmsd_to_active_ref", ""))
                    row["rmsd_to_inactive"] = _f(
                        rr.get("rmsd_to_inactive_ref", "")
                    )
            out.append(row)

    print(
        f"loaded {len(out)} rows "
        f"(fi_missing={n_missing_fi}, rmsd_missing={n_missing_rmsd})"
    )
    return out


def _pct(n: int, d: int) -> str:
    if d == 0:
        return "n/a"
    return f"{100.0*n/d:5.2f}%"


def _quantiles(vals: list[float]) -> str:
    v = sorted(x for x in vals if not (isinstance(x, float) and math.isnan(x)))
    if not v:
        return "empty"
    q = lambda p: v[max(0, min(len(v) - 1, int(round(p * (len(v) - 1)))))]
    return (
        f"min={v[0]:.4f}  p10={q(0.10):.4f}  p25={q(0.25):.4f}  "
        f"p50={q(0.50):.4f}  p75={q(0.75):.4f}  p90={q(0.90):.4f}  "
        f"max={v[-1]:.4f}  mean={st.mean(v):.4f}  n={len(v)}"
    )


def dist_helicity(rows: list[dict]) -> dict:
    v = [r["tm6_helicity_6_30_6_50"] for r in rows]
    defined = [x for x in v if not (isinstance(x, float) and math.isnan(x))]
    n = len(defined)
    bins = [0.5, 0.6, 0.7, 0.8, 0.9]
    counts = {t: sum(1 for x in defined if x < t) for t in bins}
    return {
        "quantiles": _quantiles(v),
        "n": n,
        "below": counts,
    }


def dist_breaks(rows: list[dict]) -> tuple[Counter, int]:
    c = Counter(r["chain_breaks"] for r in rows)
    total = sum(c.values())
    return c, total


def dist_rama(rows: list[dict]) -> str:
    v = [r["ramachandran_outlier_frac"] for r in rows]
    return _quantiles(v)


def dist_icl3(rows: list[dict]) -> str:
    v = [r["icl3_modelled_count"] for r in rows]
    return _quantiles(v)


def _active_called(row: dict, predicate: str) -> bool:
    if predicate == "npxxy":
        oh = row["d_npxxy_oh"]
        return (not math.isnan(oh)) and oh < PANEL_NPXXY_THRESHOLD
    elif predicate == "tilt":
        t = row["d_tilt"]
        return (not math.isnan(t)) and t > TILT_ACTIVE_THRESHOLD
    else:
        raise ValueError(f"invalid predicate: {predicate}")


def _artefact(row: dict) -> bool:
    h = row["tm6_helicity_6_30_6_50"]
    return (not math.isnan(h)) and h < UNWOUND_THRESHOLD


def per_arm_backbone_artefact(
    rows: list[dict],
    class_filter: str,
    arms: tuple[str, ...],
    predicate: str,
) -> dict:
    """Return a dict keyed by (arm, backbone) with called + artefact counts."""
    by = defaultdict(lambda: {"called": 0, "artefact": 0})
    for r in rows:
        if r["receptor_class"] != class_filter:
            continue
        if r["arm"] not in arms:
            continue
        if not _active_called(r, predicate):
            continue
        cell = (r["arm"], r["backbone"])
        by[cell]["called"] += 1
        if _artefact(r):
            by[cell]["artefact"] += 1
    return dict(by)


def per_cell_artefact(
    rows: list[dict],
    class_filter: str,
    arm: str,
    predicate: str,
) -> dict:
    """(receptor, backbone) -> {called, artefact}."""
    per = defaultdict(lambda: {"called": 0, "artefact": 0})
    for r in rows:
        if r["receptor_class"] != class_filter:
            continue
        if r["arm"] != arm:
            continue
        if not _active_called(r, predicate):
            continue
        cell = (r["receptor_slug"], r["backbone"])
        per[cell]["called"] += 1
        if _artefact(r):
            per[cell]["artefact"] += 1
    return dict(per)


def per_arm_backbone_off_pathway(
    rows: list[dict],
    class_filter: str,
    arms: tuple[str, ...],
) -> dict:
    """(arm, backbone) -> {n_scored, n_off_pathway} using RMSD-to-both-refs.

    A structure is off-pathway when both RMSD-to-active and
    RMSD-to-inactive exceed OFF_PATHWAY_RMSD_THRESHOLD. Rows with either
    NaN are skipped from the denominator.
    """
    by = defaultdict(lambda: {"scored": 0, "off": 0})
    for r in rows:
        if r["receptor_class"] != class_filter:
            continue
        if r["arm"] not in arms:
            continue
        ra = r.get("rmsd_to_active", float("nan"))
        ri = r.get("rmsd_to_inactive", float("nan"))
        if math.isnan(ra) or math.isnan(ri):
            continue
        cell = (r["arm"], r["backbone"])
        by[cell]["scored"] += 1
        if ra > OFF_PATHWAY_RMSD_THRESHOLD and ri > OFF_PATHWAY_RMSD_THRESHOLD:
            by[cell]["off"] += 1
    return dict(by)


def top_offending(per_cell: dict, k: int = 20, min_artefact: int = 1) -> list:
    items = [
        (cell, v["called"], v["artefact"])
        for cell, v in per_cell.items()
        if v["artefact"] >= min_artefact
    ]
    items.sort(key=lambda x: (-x[2], -x[1]))
    return items[:k]


def _fmt_predicate_table(
    per_ab: dict,
    arms: tuple[str, ...],
) -> list[str]:
    """Emit a per-arm x per-backbone table (rows=backbones, cols=arms)."""
    lines: list[str] = []
    header = "| backbone | " + " | ".join(arms) + " |"
    sep = "|:---|" + "|".join([":---:"] * len(arms)) + "|"
    lines.append(header)
    lines.append(sep)
    for bb in BACKBONES:
        cells: list[str] = []
        for arm in arms:
            v = per_ab.get((arm, bb), {"called": 0, "artefact": 0})
            called = v["called"]
            art = v["artefact"]
            rate = _pct(art, called).strip() if called else "n/a"
            cells.append(f"{art}/{called} ({rate})")
        lines.append(f"| {bb} | " + " | ".join(cells) + " |")
    return lines


def _totals_by_arm(per_ab: dict, arms: tuple[str, ...]) -> dict:
    out = {}
    for arm in arms:
        called = sum(v["called"] for (a, _), v in per_ab.items() if a == arm)
        art = sum(v["artefact"] for (a, _), v in per_ab.items() if a == arm)
        out[arm] = {"called": called, "artefact": art}
    return out


def _stop_trigger_lines(
    per_ab_npxxy: dict,
    per_ab_tilt: dict,
    arms: tuple[str, ...],
) -> list[str]:
    """Emit the stop-trigger evaluation block."""
    lines: list[str] = []
    lines.append("### Stop-trigger evaluation")
    lines.append("")
    triggers = []
    # Trigger 1: any arm > 5% on primary predicate (NPxxY)
    for arm in arms:
        called = sum(
            v["called"] for (a, _), v in per_ab_npxxy.items() if a == arm
        )
        art = sum(
            v["artefact"] for (a, _), v in per_ab_npxxy.items() if a == arm
        )
        rate = (art / called) if called else 0.0
        marker = "TRIP" if rate > 0.05 else "ok"
        triggers.append(
            f"- Arm-wide artefact rate on `{arm}` (NPxxY predicate): "
            f"{art}/{called} = {rate*100:.2f}% -- **{marker}** "
            f"(threshold: 5%)"
        )
    # Trigger 2: decoy vs apo per backbone (>2x)
    if "decoy" in arms and "apo" in arms:
        for bb in BACKBONES:
            d = per_ab_npxxy.get(("decoy", bb), {"called": 0, "artefact": 0})
            a = per_ab_npxxy.get(("apo", bb), {"called": 0, "artefact": 0})
            drate = (d["artefact"] / d["called"]) if d["called"] else 0.0
            arate = (a["artefact"] / a["called"]) if a["called"] else 0.0
            if arate > 0.0:
                ratio = drate / arate
                marker = "TRIP" if ratio > 2.0 else "ok"
                triggers.append(
                    f"- `decoy/{bb}` vs `apo/{bb}` (NPxxY): "
                    f"{drate*100:.2f}% vs {arate*100:.2f}% "
                    f"(ratio {ratio:.2f}x) -- **{marker}** "
                    f"(threshold: 2x)"
                )
            else:
                # apo rate 0: cannot form a ratio; report absolute diff
                marker = "TRIP" if drate > 0.05 else "ok"
                triggers.append(
                    f"- `decoy/{bb}` vs `apo/{bb}` (NPxxY): "
                    f"{drate*100:.2f}% vs {arate*100:.2f}% "
                    f"(apo=0, ratio undefined) -- **{marker}** "
                    f"(absolute-threshold: 5%)"
                )
    lines.extend(triggers)
    lines.append("")
    return lines


def _off_pathway_lines(
    off_ab: dict,
    arms: tuple[str, ...],
) -> list[str]:
    """Emit the off-pathway (rmsd-to-both-refs > 3 A) table."""
    lines: list[str] = []
    lines.append(
        "Rule: a row is off-pathway if `rmsd_to_active_ref > "
        f"{OFF_PATHWAY_RMSD_THRESHOLD} A` AND `rmsd_to_inactive_ref > "
        f"{OFF_PATHWAY_RMSD_THRESHOLD} A`. Neither Block A nor Block B "
        "measured this (Block C plan §7 confound #4)."
    )
    lines.append("")
    lines.extend(_fmt_predicate_table(_wrap_scored(off_ab), arms))
    lines.append("")
    # cognate stop trigger
    triggers = []
    if "cognate" in arms:
        for bb in BACKBONES:
            v = off_ab.get(("cognate", bb), {"scored": 0, "off": 0})
            rate = (v["off"] / v["scored"]) if v["scored"] else 0.0
            marker = "TRIP" if rate > 0.10 else "ok"
            triggers.append(
                f"- `cognate/{bb}` off-pathway: "
                f"{v['off']}/{v['scored']} = {rate*100:.2f}% -- "
                f"**{marker}** (threshold: 10%)"
            )
    lines.append("**Cognate off-pathway stop-trigger evaluation:**")
    lines.append("")
    lines.extend(triggers)
    lines.append("")
    return lines


def _wrap_scored(off_ab: dict) -> dict:
    """Re-key off_ab dict from (scored/off) to (called/artefact) so the
    same _fmt_predicate_table renderer works."""
    return {
        k: {"called": v["scored"], "artefact": v["off"]}
        for k, v in off_ab.items()
    }


def build_report(
    rows: list[dict],
    arms: tuple[str, ...],
    block_label: str,
    have_rmsd: bool,
    out_path: Path,
) -> None:
    """Emit the fold-integrity report for a Block-A- or Block-B-shaped run."""
    dh = dist_helicity(rows)
    dbreaks, total_breaks = dist_breaks(rows)
    dr = dist_rama(rows)
    di = dist_icl3(rows)

    per_ab_npxxy = per_arm_backbone_artefact(rows, "A", arms, "npxxy")
    per_ab_tilt = per_arm_backbone_artefact(rows, "A", arms, "tilt")

    off_ab: dict = {}
    if have_rmsd:
        off_ab = per_arm_backbone_off_pathway(rows, "A", arms)

    lines: list[str] = []
    n_rows = len(rows)
    lines.append(f"# {block_label} — Fold-integrity report")
    lines.append("")
    lines.append(
        f"**Generated:** `scripts/analyze_fold_integrity.py`, based on "
        f"`rows.fold_integrity.csv` ({n_rows:,} rows, CPU-only compute)."
    )
    lines.append("")
    lines.append(
        "**Note:** PREVIOUS VERSION of this file (visible in `git log`) "
        "computed the Block A calibration; this version reports the actual "
        "Block B 32,000-row rescore."
    )
    lines.append("")
    lines.append(
        f"**Method:** four fold-integrity axes computed via "
        f"`scorer/fold_integrity.py`. Artefact predicate: "
        f"`tm6_helicity_6_30_6_50 < {UNWOUND_THRESHOLD}` on rows called "
        f"active by the specified predicate. Two active-call predicates "
        f"reported side-by-side: NPxxY-OH `< {PANEL_NPXXY_THRESHOLD}` "
        f"(Block A precedent, strict cross-block comparability), and "
        f"GPCRdb TM6 tilt `> {TILT_ACTIVE_THRESHOLD}` (Block B active-call "
        f"primary per PREREG §16). Class A subset only (Class B/F excluded "
        f"from the artefact rate: the NPxxY predicate does not apply)."
    )
    lines.append("")
    lines.append(
        "**Block A calibration** (from `POST_BLOCK_A_CLEANUP_2026_09_02.md` "
        "§Fold-integrity + `experiments/018_block_a_switch_test/analysis/"
        "fold_integrity_report.md`): apo-active artefact rate 2.11% "
        "(19/899 Class A apo NPxxY-called rows). Cognate 1.00% (32/3186)."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # §1 distributions
    lines.append(f"## 1. Column distributions across {n_rows:,} rows")
    lines.append("")
    lines.append("### 1.1 `tm6_helicity_6_30_6_50`")
    lines.append("")
    lines.append(
        "Rule: fraction of BW 6.30–6.50 (21 UniProt positions) with "
        "(φ, ψ) in the tight α-box φ ∈ [-90, -35], ψ ∈ [-70, -15]. "
        "Denominator = residues where BOTH φ and ψ are defined."
    )
    lines.append("")
    lines.append(f"    {dh['quantiles']}")
    lines.append("")
    lines.append("Fraction of rows below candidate thresholds:")
    lines.append("")
    lines.append("| threshold | count | rate |")
    lines.append("| :-------: | ----: | ---: |")
    for t in [0.5, 0.6, 0.7, 0.8, 0.9]:
        c = dh["below"][t]
        lines.append(f"| < {t:.2f} | {c:>4d} | {_pct(c, dh['n'])} |")
    lines.append("")

    # §1.2 chain breaks
    lines.append("### 1.2 `chain_breaks`")
    lines.append("")
    lines.append(
        "Rule: count of CA-CA distances > 4.5 Å between residues at "
        "consecutive integer seq numbers. Missing-CA pairs skipped."
    )
    lines.append("")
    lines.append("| chain_breaks | rows |")
    lines.append("| :----------: | ---: |")
    for k in sorted(dbreaks):
        lines.append(f"| {k} | {dbreaks[k]} |")
    nonzero = sum(v for k, v in dbreaks.items() if k > 0)
    lines.append("")
    lines.append(
        f"Panel median 0; total non-zero rows: {nonzero} / {total_breaks} "
        f"({_pct(nonzero, total_breaks)})."
    )
    lines.append("")

    # §1.3 rama
    lines.append("### 1.3 `ramachandran_outlier_frac`")
    lines.append("")
    lines.append(
        "Rule (Lovell-inspired, rectangular; three allowed boxes α, β, "
        "L-α). Terminal residues excluded from the denominator."
    )
    lines.append("")
    lines.append(f"    {dr}")
    lines.append("")

    # §1.4 icl3
    lines.append("### 1.4 `icl3_modelled_count`")
    lines.append("")
    lines.append(
        "Rule: number of UniProt positions in the GPCRdb-defined ICL3 "
        "range with a CA atom present in the selected chain. NaN when "
        "the GPCRdb cache lacks an ICL3 segment (e.g. FZD6, no ICL3 "
        "annotation)."
    )
    lines.append("")
    lines.append(f"    {di}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # §2 headline
    lines.append(
        "## 2. Per-arm × per-backbone artefact rate — Class A "
        f"(TM6 helicity < {UNWOUND_THRESHOLD})"
    )
    lines.append("")
    lines.append(
        "Each cell is `n_artefact / n_active_called (rate)`. Active-called "
        "rows are those where the specified predicate fires; the artefact "
        "predicate is `tm6_helicity_6_30_6_50 < 0.80` on those rows."
    )
    lines.append("")

    # Table A — NPxxY predicate
    lines.append(
        f"### 2.1 NPxxY predicate (`d_npxxy_y558_y753_oh < "
        f"{PANEL_NPXXY_THRESHOLD}` Å) — Block A cross-comparability"
    )
    lines.append("")
    lines.extend(_fmt_predicate_table(per_ab_npxxy, arms))
    lines.append("")
    # arm totals
    totals_n = _totals_by_arm(per_ab_npxxy, arms)
    lines.append("Arm totals (all backbones, Class A only):")
    lines.append("")
    for arm in arms:
        v = totals_n[arm]
        rate = _pct(v["artefact"], v["called"]).strip() if v["called"] else "n/a"
        lines.append(f"- **{arm}**: {v['artefact']}/{v['called']} = {rate}")
    lines.append("")

    # Table B — tilt predicate
    lines.append(
        f"### 2.2 Tilt predicate (`d_gpcrdb_tm6_tilt_246_637_ca > "
        f"{TILT_ACTIVE_THRESHOLD}` Å) — Block B active-call primary"
    )
    lines.append("")
    lines.extend(_fmt_predicate_table(per_ab_tilt, arms))
    lines.append("")
    totals_t = _totals_by_arm(per_ab_tilt, arms)
    lines.append("Arm totals (all backbones, Class A only):")
    lines.append("")
    for arm in arms:
        v = totals_t[arm]
        rate = _pct(v["artefact"], v["called"]).strip() if v["called"] else "n/a"
        lines.append(f"- **{arm}**: {v['artefact']}/{v['called']} = {rate}")
    lines.append("")

    # §2.3 stop triggers
    lines.extend(_stop_trigger_lines(per_ab_npxxy, per_ab_tilt, arms))

    # §2.4 top-offending cells per arm (using NPxxY predicate)
    lines.append("### Top-offending (receptor × backbone) cells per arm "
                 "(NPxxY predicate)")
    lines.append("")
    for arm in arms:
        pc = per_cell_artefact(rows, "A", arm, "npxxy")
        top = top_offending(pc, k=15)
        n_cells = sum(1 for v in pc.values() if v["called"] > 0)
        n_bad = sum(1 for v in pc.values() if v["artefact"] > 0)
        lines.append(f"**arm = `{arm}`** "
                     f"({n_bad}/{n_cells} cells contribute any artefact rows)")
        lines.append("")
        if not top:
            lines.append("_(no cell has any artefact rows)_")
            lines.append("")
            continue
        lines.append("| receptor | backbone | called | artefact | rate |")
        lines.append("| :------- | :------- | -----: | -------: | ---: |")
        for (rec, bb), called, art in top:
            lines.append(
                f"| {rec} | {bb} | {called} | {art} | {_pct(art, called)} |"
            )
        lines.append("")

    lines.append("---")
    lines.append("")

    # §3 off-pathway (optional)
    if have_rmsd:
        lines.append(
            "## 3. Off-pathway rate — Class A "
            f"(RMSD-to-active > {OFF_PATHWAY_RMSD_THRESHOLD} Å AND "
            f"RMSD-to-inactive > {OFF_PATHWAY_RMSD_THRESHOLD} Å)"
        )
        lines.append("")
        lines.append(
            "Independent of the active-call predicate: this is the rate at "
            "which the prediction lands far from BOTH references — neither "
            "active nor inactive. Cell format: `n_off / n_scored (rate)`."
        )
        lines.append("")
        lines.extend(_off_pathway_lines(off_ab, arms))
        lines.append("---")
        lines.append("")

    # §4 verdict
    lines.append(f"## {'4' if have_rmsd else '3'}. Verdict")
    lines.append("")
    # composite verdict on the primary NPxxY predicate, apo arm (Block A parity)
    if "apo" in arms:
        apo_tot = totals_n.get("apo", {"called": 0, "artefact": 0})
        apo_rate = (
            100.0 * apo_tot["artefact"] / apo_tot["called"]
            if apo_tot["called"] else 0.0
        )
        if apo_rate < 5.0:
            verdict = "**FOLD INTEGRITY OK** (Class A apo artefact rate < 5%)"
        elif apo_rate <= 10.0:
            verdict = "**MARGINAL** (Class A apo artefact rate 5-10%)"
        else:
            verdict = "**FAIL** (Class A apo artefact rate > 10%)"
        lines.append(verdict)
        lines.append("")
        lines.append(
            f"Class A apo artefact rate (NPxxY predicate): "
            f"{apo_tot['artefact']}/{apo_tot['called']} = {apo_rate:.2f}%. "
            f"Block A calibration was 2.11% (19/899)."
        )
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))
    print(f"wrote {out_path}")


def _default_paths(block: str) -> tuple[Path, Path, Path]:
    """Legacy defaults — Block A analysis dir."""
    if block == "block_a":
        d = REPO / "experiments/018_block_a_switch_test/analysis"
    elif block == "block_b":
        d = REPO / "experiments/019_block_b_partner_selection/analysis"
    else:
        raise ValueError(block)
    return d / "rows.csv", d / "rows.fold_integrity.csv", d / "fold_integrity_report.md"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="analyze_fold_integrity",
        description=(
            "Report generator for the fold-integrity rescore. Supports "
            "Block A (2 arms via input_state_claim column) and Block B "
            "(4 arms via input_path regex). Optionally merges "
            "rows.rmsd.csv to add the off-pathway (rmsd-to-both-refs) "
            "diagnostic."
        ),
    )
    p.add_argument(
        "--block",
        choices=("block_a", "block_b"),
        default="block_a",
        help="Which block's default paths + arm set to use. Overridable "
             "with the explicit --rows / --fi / --out / --arms flags.",
    )
    p.add_argument("--rows", type=Path, default=None)
    p.add_argument("--fi", type=Path, default=None,
                   help="rows.fold_integrity.csv path")
    p.add_argument("--out", type=Path, default=None,
                   help="output report path")
    p.add_argument(
        "--arm-source",
        choices=("column", "path"),
        default=None,
        help="How to derive the arm label. Default: 'column' for block_a, "
             "'path' for block_b.",
    )
    p.add_argument(
        "--arms",
        default=None,
        help="Comma-separated list of arm labels to include. Default: "
             "the block's canonical set.",
    )
    p.add_argument(
        "--rmsd",
        type=Path,
        default=None,
        help="Optional rows.rmsd.csv path — when passed, add the "
             "off-pathway diagnostic (rmsd-to-active > 3 A AND "
             "rmsd-to-inactive > 3 A).",
    )
    p.add_argument(
        "--label",
        default=None,
        help="Block label used in the report title. Default derived from "
             "--block.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    dfl_rows, dfl_fi, dfl_out = _default_paths(args.block)
    rows_csv = args.rows or dfl_rows
    fi_csv = args.fi or dfl_fi
    out = args.out or dfl_out
    arm_source = args.arm_source or (
        "path" if args.block == "block_b" else "column"
    )
    if args.arms:
        arms = tuple(a.strip() for a in args.arms.split(",") if a.strip())
    else:
        arms = BLOCK_B_ARMS if args.block == "block_b" else BLOCK_A_ARMS
    label = args.label or (
        "Block B Stage 0 §8-2 (32,000-row rescore)"
        if args.block == "block_b"
        else "Block A calibration (9,490-row Stage 0 Gate 1)"
    )
    rows = load(rows_csv, fi_csv, arm_source, args.rmsd)
    build_report(rows, arms, label, args.rmsd is not None, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
