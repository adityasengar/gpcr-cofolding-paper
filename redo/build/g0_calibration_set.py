#!/usr/bin/env python3
"""Group 0 — enumerate the calibration population for the activation predicate.

WHY THIS FILE EXISTS.  `manuscript/sections/methods.tex:95` concedes that "our
thresholds derive from 80 annotated reference rows" — the same rows the arms are
graded against.  E0.1 (`redo/spec/CATALOGUE.md:387`) rebuilds the
ruler on Class A structures the panel will never predict on, so the threshold is
independent of what it grades.  This script enumerates that population *by name*,
from frozen inputs, before any threshold is fitted.

WHAT IT DOES NOT DO.  It measures nothing.  Neither activation axis can be
computed from the files this repository holds: no coordinates are present for any
off-panel structure (see `GROUP0_SYSTEMS.md` §3).  This script produces the work
list that the measurement build step consumes, plus every count that
`GROUP0_SYSTEMS.md` quotes, so that a reader can re-derive each one.

INPUTS (frozen; sha256 printed on every run):
  lit/panels/cache/gpcrdb_structures.json          1,716 structure entries
  redo/inputs/panel_systems.csv                  75 receptors x 138 columns
  redo/cache/panel_rcsb_cache.json              962 cached RCSB entries
  data/block_b/09_references/reference_set.blockb_pinned.csv   162 reference rows

OUTPUTS (all g0_-prefixed, all in redo/):
  g0_calibration_structures.csv   one row per Class A structure with a state
                                  annotation (Active/Inactive/Intermediate),
                                  carrying panel membership under three panel
                                  definitions and every pre-declared filter flag
  g0_panel_exclusions.csv         the receptor slugs excluded from calibration,
                                  and why
  g0_filter_ladder.csv            each pre-declared exclusion applied in a fixed
                                  order, with the count it removes
  g0_class_variants.csv           per-class census for the B1 / B2 / C / F
                                  instrument decision (E0.5)
  g0_reference_axis_gap.csv       the 162 pinned reference rows: which axis is
                                  populated, which anchors are resolvable, and
                                  therefore what the build step must measure
  g0_label_conflicts.csv          structures whose GPCRdb state label disagrees
                                  with their own ligand pharmacology / transducer

USAGE:  python3 redo/build/g0_calibration_set.py
        (writes into redo/; reads nothing under data/ except the pinned
        reference CSV, which it does not modify)
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import os
import statistics
import sys

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
ROOT = os.path.dirname(os.path.dirname(INPUTS))

SNAPSHOT = os.path.join(ROOT, "lit", "panels", "cache", "gpcrdb_structures.json")
PANEL = os.path.join(INPUTS, "panel_systems.csv")
RCSB = os.path.join(CACHE, "panel_rcsb_cache.json")
PINNED = os.path.join(
    ROOT, "data", "block_b", "09_references", "reference_set.blockb_pinned.csv"
)
# GPCRdb's own GRADED activation annotation, 0-100, one row per structure for all
# 1,716.  This is the external, published, pre-existing criterion that rule Q0c
# uses; see GROUP0_SYSTEMS.md sec.5.6.  Retrieved by the panel session.
DEGREE = os.path.join(INPUTS, "panel_gpcrdb_degree.csv")

# ---------------------------------------------------------------------------
# Pre-declared rules.  Every one of these is a rule stated in advance.  None of
# them may be changed after a threshold has been fitted; if one is changed, the
# fit is re-run from scratch and both fits are reported.
# ---------------------------------------------------------------------------

# Q1 — resolution floor.  Precedent: khaleq2026hyaline p.12 uses <= 4.0 A X-ray /
# <= 4.5 A cryo-EM.  We adopt a single floor across methods because GPCRdb's
# snapshot carries one `resolution` field and does not distinguish FSC from
# crystallographic resolution.  RES_FLOOR is the primary; RES_SENSITIVITY is the
# declared sensitivity sweep required by E0.1.
RES_FLOOR = 3.5
RES_SENSITIVITY = (2.5, 3.0, 3.2, 3.5, 4.0, None)

# Q2 — ligand-pharmacology conflict.  A structure annotated Active whose only
# ligands are antagonist-class AND which carries no transducer in the deposited
# assembly is a label we cannot defend.  Likewise a structure annotated Inactive
# whose only ligands are agonist-class.  Both classes are FLAGGED here and the
# decision to drop them is a PI decision (GROUP0_SYSTEMS.md §5, rule Q2).
ANTAGONIST_FUNCS = frozenset({
    "Antagonist", "Inverse agonist", "NAM", "Allosteric antagonist",
})
AGONIST_FUNCS = frozenset({
    "Agonist", "Agonist (partial)", "Allosteric agonist", "PAM",
    "Allosteric agonist (partial)",
})

# ---------------------------------------------------------------------------
# RETRACTED RULE -- Q0c, "restrict the Active class to GPCRdb activation degree
# = 100".  Applied 2026-09-11 and WITHDRAWN the same day.  DO NOT REINSTATE IT.
# The degree columns are still emitted, because the DATA is sound and worth
# having; only the INFERENCE was wrong.
#
# Why.  GPCRdb's own documentation
# (`lit/panels/cache/gpcrdb_activation_degree_definition.txt`, from
# docs.gpcrdb.org/structures.html) defines the active pole as:
#
#     "structures in complex with a signaling protein are set as the reference
#      structures for the active state (100% degree activation)"
#
# So "activation degree = 100" MEANS "a transducer is bound".  It is not an
# independent geometric criterion.  Calibrating the active pole on partner
# presence and then using the predicate to test whether supplying a Ga co-input
# drives the active state is circular -- the exact circularity E0.1 exists to
# escape.
#
# Verified here rather than taken on trust: of 807 degree-100 Class A actives,
# 795 (98.5%) carry a transducer; of the 158 below 100, 155 (98.1%) carry none.
# The "97% agreement between GPCRdb's degree and transducer presence" reported
# on 2026-09-11 as independent corroboration was ONE SIGNAL COUNTED TWICE.
#
# Two further properties barring casual reuse.  The degree is min-max normalised
# WITHIN CLASS, so it is a relative rank that rescales as GPCRdb grows -- a
# structure's degree today is not the degree `lee2026confornets` selected on.
# And GPCRdb's text defines the activation score as "substracting the mean
# distance to the inactive-state structures from the mean distance to the
# active-state structures", which read literally has the SIGN INVERTED.  Do not
# build on the score's direction without checking it against a known pair.
#
# WHAT SURVIVES is the inactive pole, and only for one axis: see
# GROUP0_SYSTEMS.md sec.5.1.
# ---------------------------------------------------------------------------

# GPCRdb's published maximum Ca-Ca distance used to SELECT inactive reference
# structures, per class (2x46-6x37; class F uses 2x44-6x31).  Carried as a
# reported landmark, NOT applied as a filter -- GROUP0_SYSTEMS.md sec.5.1 gives
# the reason it cannot calibrate the tilt axis.
GPCRDB_INACTIVE_REF_MAX_A = {"A": 11.9, "B": 13.0, "C": 14.5, "F": 13.0}

# Q3 — transducer class admitted as "Active".  See GROUP0_SYSTEMS.md §5 rule Q3.
# GPCRdb's `signalling_protein.type` takes values {G protein, Arrestin, None}.
ARRESTIN_TYPE = "Arrestin"

# Q4 — species.  Non-human orthologs are retained by default because dropping
# them costs receptors we cannot replace; the flag lets the sensitivity arm run.
HUMAN = "Homo sapiens"


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def entry_slug(entry_name: str) -> str:
    """`5ht1b_human` -> `5ht1b`.  Species-collapsed receptor identity.

    Species collapse is deliberate and is the rule that reproduces the
    catalogue's 726/610 split (E0.1, catalogue:387).  A receptor is off-panel
    only if NO ortholog of it is on the panel: calibrating on bovine rhodopsin
    while predicting on human rhodopsin would not be independent.
    """
    return entry_name.rsplit("_", 1)[0]


def panel_entries(row: dict) -> list[str]:
    return [x.strip() for x in (row.get("gpcrdb_proteins") or "").split("|") if x.strip()]


def panel_slug_set(rows: list[dict], predicate) -> set[str]:
    """Union of species-collapsed slugs and the raw `gpcrdb_slug` column.

    Both are needed: `gpcrdb_proteins` is empty or multi-valued on some rows and
    `gpcrdb_slug` carries composite values such as `opsd_bovin;opsd_human;opsd`.
    Including both is what makes the membership test total.
    """
    out: set[str] = set()
    for r in rows:
        if not predicate(r):
            continue
        for e in panel_entries(r):
            out.add(entry_slug(e))
        if r.get("gpcrdb_slug"):
            out.add(r["gpcrdb_slug"])
    return out


def _int_or_blank(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return ""


def transducer(struct: dict) -> str:
    sig = struct.get("signalling_protein")
    if not sig:
        return "none"
    return sig.get("type") or "none"


def ligand_funcs(struct: dict) -> list[str]:
    return sorted({(l.get("function") or "?") for l in (struct.get("ligands") or [])})


def main() -> int:
    print("# g0_calibration_set.py — frozen inputs")
    for p in (SNAPSHOT, PANEL, RCSB, PINNED, DEGREE):
        print(f"  {sha256(p)[:8]}…{sha256(p)[-6:]}  {os.path.relpath(p, ROOT)}")
    print()

    snapshot = json.load(open(SNAPSHOT))
    panel = list(csv.DictReader(open(PANEL)))
    rcsb = json.load(open(RCSB))
    pinned = list(csv.DictReader(open(PINNED)))
    degree = {d["pdb"].upper(): d for d in csv.DictReader(open(DEGREE))}

    # ---- panel definitions -------------------------------------------------
    # P48  the 48 receptors the campaign has already predicted on.  This is the
    #      definition the catalogue used and the one that reproduces 726/610.
    # P75  every receptor named anywhere in panel_systems.csv, i.e. the widest
    #      set the redo could predict on including the E-scope / E-B1 additions.
    # P_CN the 51 ConfoRNets receptors, carried only so the overlap is visible.
    p48 = panel_slug_set(panel, lambda r: r["in_our48"] == "1")
    p75 = panel_slug_set(panel, lambda r: True)
    pcn = panel_slug_set(panel, lambda r: r["in_confornets"] == "1")

    # ---- the Class A population -------------------------------------------
    classA = [s for s in snapshot if s["class"].startswith("Class A")]
    scored = [s for s in classA if s["state"] in ("Active", "Inactive")]
    intermediate = [s for s in classA if s["state"] == "Intermediate"]

    rows = []
    for s in sorted(classA, key=lambda x: (x["state"], x["protein"], x["pdb_code"])):
        if s["state"] not in ("Active", "Inactive", "Intermediate"):
            continue
        slug = entry_slug(s["protein"])
        funcs = ligand_funcs(s)
        fset = set(funcs)
        trans = transducer(s)
        res = s.get("resolution")
        conflict = ""
        if s["state"] == "Active" and trans == "none" \
                and (fset & ANTAGONIST_FUNCS) and not (fset & AGONIST_FUNCS):
            conflict = "active_label_antagonist_only_no_transducer"
        elif s["state"] == "Inactive" and (fset & AGONIST_FUNCS) \
                and not (fset & ANTAGONIST_FUNCS):
            conflict = "inactive_label_agonist_bound"
        rows.append({
            "pdb_id": s["pdb_code"],
            "gpcrdb_entry": s["protein"],
            "receptor_slug": slug,
            "gpcr_class": s["class"],
            "state": s["state"],
            "species": s["species"],
            "method": s["type"],
            "resolution": "" if res is None else res,
            "publication_date": s["publication_date"] or "",
            "preferred_chain": s.get("preferred_chain") or "",
            "transducer_type": trans,
            "ligand_functions": "|".join(funcs) if funcs else "(no ligand)",
            "on_panel48": int(slug in p48),
            "on_panel75": int(slug in p75),
            "in_confornets": int(slug in pcn),
            "role": "application" if slug in p48 else "calibration",
            "rcsb_metadata_cached": int(s["pdb_code"] in rcsb),
            "flag_res_missing": int(res is None),
            "flag_res_above_floor": int(res is not None and res > RES_FLOOR),
            "flag_non_human": int(s["species"] != HUMAN),
            "flag_arrestin_active": int(s["state"] == "Active" and trans == ARRESTIN_TYPE),
            "flag_no_transducer_active": int(s["state"] == "Active" and trans == "none"),
            "flag_label_conflict": conflict,
            "activation_degree": _int_or_blank(
                degree.get(s["pdb_code"].upper(), {}).get("degree_active")),
            "pct_seq_modelled": _int_or_blank(
                degree.get(s["pdb_code"].upper(), {}).get("pct_seq")),
            "flag_active_not_fully_active": int(
                s["state"] == "Active"
                and _int_or_blank(degree.get(s["pdb_code"].upper(), {})
                                  .get("degree_active")) != 100),
        })

    out = os.path.join(INPUTS, "g0_calibration_structures.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {os.path.relpath(out, ROOT)}  ({len(rows)} rows)")

    # ---- headline split ----------------------------------------------------
    def split(key: str):
        off = [r for r in rows if r["state"] != "Intermediate" and not r[key]]
        on = [r for r in rows if r["state"] != "Intermediate" and r[key]]
        return off, on

    print()
    print("## The split, under each panel definition")
    print(f"{'definition':>12} | {'calib n':>7} {'A':>5} {'I':>5} {'A:I':>6} {'recept':>6}"
          f" | {'appl n':>6} {'A':>5} {'I':>5} {'recept':>6}")
    for name, key in (("panel48", "on_panel48"), ("panel75", "on_panel75")):
        off, on = split(key)
        oa = sum(r["state"] == "Active" for r in off)
        oi = sum(r["state"] == "Inactive" for r in off)
        na = sum(r["state"] == "Active" for r in on)
        ni = sum(r["state"] == "Inactive" for r in on)
        ratio = f"{oa / oi:.1f}:1" if oi else "inf"
        print(f"{name:>12} | {len(off):>7} {oa:>5} {oi:>5} {ratio:>6}"
              f" {len({r['receptor_slug'] for r in off}):>6}"
              f" | {len(on):>6} {na:>5} {ni:>5}"
              f" {len({r['receptor_slug'] for r in on}):>6}")

    # ---- panel exclusion list ---------------------------------------------
    excl = []
    for r in panel:
        slugs = {entry_slug(e) for e in panel_entries(r)}
        if r.get("gpcrdb_slug"):
            slugs.add(r["gpcrdb_slug"])
        n48 = sum(1 for x in rows if x["receptor_slug"] in slugs and x["state"] != "Intermediate")
        excl.append({
            "panel_row_slug": r["slug"],
            "gpcrdb_slug": r["gpcrdb_slug"],
            "gpcr_class": r["gpcr_class"],
            "in_our48": r["in_our48"],
            "in_confornets": r["in_confornets"],
            "tier": r["tier"],
            "excluded_under_panel48": int(r["in_our48"] == "1"),
            "excluded_under_panel75": 1,
            "n_snapshot_structures_withdrawn": n48,
        })
    out = os.path.join(INPUTS, "g0_panel_exclusions.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(excl[0].keys()))
        w.writeheader()
        w.writerows(excl)
    print(f"\nwrote {os.path.relpath(out, ROOT)}  ({len(excl)} rows)")

    # ---- filter ladder -----------------------------------------------------
    # Applied in a FIXED order.  The order is declared here and does not change.
    ladder = []
    pool = [r for r in rows if r["state"] != "Intermediate" and not r["on_panel48"]]

    def record(step: str, rule: str, pool_after: list[dict]):
        a = sum(r["state"] == "Active" for r in pool_after)
        i = sum(r["state"] == "Inactive" for r in pool_after)
        ladder.append({
            "step": step,
            "rule": rule,
            "n_remaining": len(pool_after),
            "n_active": a,
            "n_inactive": i,
            "active_to_inactive": f"{a / i:.2f}" if i else "inf",
            "n_receptors": len({r["receptor_slug"] for r in pool_after}),
            "n_receptors_both_states": sum(
                1 for _, v in _by_receptor(pool_after).items()
                if v["Active"] and v["Inactive"]
            ),
        })

    def _by_receptor(pop):
        d = collections.defaultdict(collections.Counter)
        for r in pop:
            d[r["receptor_slug"]][r["state"]] += 1
        return d

    record("F0", "Class A, GPCRdb state in {Active, Inactive}, receptor not on panel48", pool)
    # F0b -- the axis-definability gate.  d(Y5.58 OH, Y7.53 OH) is a hydroxyl
    # distance and exists only where BOTH positions are tyrosine.  They are not
    # conserved across Class A: `g0_anchor_conservation.py` finds 5.58 is Tyr on
    # 164 of 199 entries and 7.53 on 189, both Tyr on 157.  This gate is a fact
    # about the predicate, not a quality judgement, and it comes FIRST because a
    # structure on which the axis is undefined was never a calibration candidate.
    cons_path = os.path.join(INPUTS, "g0_anchor_conservation.csv")
    if os.path.exists(cons_path):
        meas = {r["gpcrdb_entry"]: r["npxxy_measurable"] == "1"
                for r in csv.DictReader(open(cons_path))}
        pool = [r for r in pool if meas.get(r["gpcrdb_entry"], True)]
        record("F0b", "NPxxY axis defined: Tyr at BOTH 5.58 and 7.53 "
                      "(g0_anchor_conservation.csv)", pool)
    else:
        ladder.append({"step": "F0b", "rule": "NPxxY axis defined -- RUN "
                       "g0_anchor_conservation.py first", "n_remaining": -1,
                       "n_active": -1, "n_inactive": -1, "active_to_inactive": "?",
                       "n_receptors": -1, "n_receptors_both_states": -1})
    pool = [r for r in pool if not r["flag_res_missing"]]
    record("F1", "resolution reported in the snapshot", pool)
    pool = [r for r in pool if not r["flag_res_above_floor"]]
    record("F2", f"resolution <= {RES_FLOOR} A (khaleq2026hyaline p.12 precedent, tightened)", pool)
    pool_q2 = [r for r in pool if not r["flag_label_conflict"]]
    record("F3", "GPCRdb state label not contradicted by the entry's own ligand pharmacology", pool_q2)
    pool_q3 = [r for r in pool_q2 if not r["flag_arrestin_active"]]
    record("F4", "Active label not defined solely by arrestin coupling", pool_q3)
    pool_q4 = [r for r in pool_q3 if not r["flag_non_human"]]
    record("F5", "human ortholog only (SENSITIVITY ARM, not the primary rule)", pool_q4)

    out = os.path.join(INPUTS, "g0_filter_ladder.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ladder[0].keys()))
        w.writeheader()
        w.writerows(ladder)
    print(f"wrote {os.path.relpath(out, ROOT)}  ({len(ladder)} rows)")
    print()
    print("## Filter ladder (panel48 calibration pool)")
    for l in ladder:
        print(f"  {l['step']}  n={l['n_remaining']:>4}  A={l['n_active']:>4}"
              f"  I={l['n_inactive']:>4}  A:I={l['active_to_inactive']:>5}"
              f"  receptors={l['n_receptors']:>3}"
              f"  both-state={l['n_receptors_both_states']:>3}   {l['rule']}")

    # ---- resolution sensitivity -------------------------------------------
    print()
    print("## Resolution sensitivity on the panel48 calibration pool (F0 + reported res)")
    base = [r for r in rows if r["state"] != "Intermediate"
            and not r["on_panel48"] and not r["flag_res_missing"]]
    for cut in RES_SENSITIVITY:
        keep = base if cut is None else [r for r in base if float(r["resolution"]) <= cut]
        a = sum(r["state"] == "Active" for r in keep)
        i = sum(r["state"] == "Inactive" for r in keep)
        byr = _by_receptor(keep)
        both = sum(1 for v in byr.values() if v["Active"] and v["Inactive"])
        ratio = f"{a / i:.2f}" if i else "inf"
        print(f"  <= {(str(cut) + ' A') if cut else 'no cut':>7}: n={len(keep):>4}"
              f"  A={a:>4} I={i:>4}  A:I={ratio:>5}"
              f"  receptors={len(byr):>3}  both-state={both:>3}")

    # ---- the independence ladder ------------------------------------------
    # How much independence can be bought, and what it costs in inactives.
    # This is the table the PI decision in GROUP0_SYSTEMS.md sec.4 turns on.
    fam3 = {s["pdb_code"]: "_".join((s.get("family") or "").split("_")[:3])
            for s in snapshot}
    panel_fams = {fam3[r["pdb_id"]] for r in rows
                  if r["state"] != "Intermediate" and r["on_panel48"]}
    cons_path = os.path.join(INPUTS, "g0_anchor_conservation.csv")
    meas = {}
    if os.path.exists(cons_path):
        meas = {r["gpcrdb_entry"]: r["npxxy_measurable"] == "1"
                for r in csv.DictReader(open(cons_path))}
    base_q = [r for r in rows
              if r["state"] != "Intermediate" and not r["on_panel48"]
              and meas.get(r["gpcrdb_entry"], True)
              and not r["flag_res_above_floor"] and not r["flag_label_conflict"]
              and not r["flag_arrestin_active"]]
    ladders = [
        ("I1  receptor-strict vs panel48 (+F0b,F2,F3,F4)", base_q),
        ("I2  I1 and not a redo-expansion receptor",
         [r for r in base_q if not r["on_panel75"]]),
        ("I3  I1 and not sharing a GPCRdb level-3 family with panel48",
         [r for r in base_q if fam3[r["pdb_id"]] not in panel_fams]),
        ("I4  I2 and I3",
         [r for r in base_q
          if not r["on_panel75"] and fam3[r["pdb_id"]] not in panel_fams]),
    ]
    ind = []
    for name, pop in ladders:
        a = sum(r["state"] == "Active" for r in pop)
        i = sum(r["state"] == "Inactive" for r in pop)
        byr = _by_receptor(pop)
        ind.append({
            "rule": name,
            "n": len(pop), "n_active": a, "n_inactive": i,
            "active_to_inactive": f"{a / i:.2f}" if i else "inf",
            "n_receptors": len(byr),
            "n_receptors_both_states": sum(
                1 for v in byr.values() if v["Active"] and v["Inactive"]),
        })
    out = os.path.join(INPUTS, "g0_independence_ladder.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ind[0].keys()))
        w.writeheader()
        w.writerows(ind)
    print(f"\nwrote {os.path.relpath(out, ROOT)}  ({len(ind)} rows)")
    print("## Independence ladder — what each degree of independence costs")
    for r in ind:
        print(f"  {r['rule']:<48} n={r['n']:>4} A={r['n_active']:>4}"
              f" I={r['n_inactive']:>3} A:I={r['active_to_inactive']:>5}"
              f" receptors={r['n_receptors']:>3} both-state={r['n_receptors_both_states']:>3}")
    # Where the inactive signal actually lives.
    byrec_i = collections.defaultdict(collections.Counter)
    for r in base_q:
        byrec_i[r["receptor_slug"]][r["state"]] += 1
        byrec_i[r["receptor_slug"]]["expansion"] = max(
            byrec_i[r["receptor_slug"]]["expansion"], int(bool(r["on_panel75"])))
    print("  inactive contributors in I1, ranked:")
    for k, v in sorted(byrec_i.items(), key=lambda kv: -kv[1]["Inactive"]):
        if not v["Inactive"]:
            continue
        print(f"    {k:<10} A={v['Active']:>3} I={v['Inactive']:>3}"
              f"  redo_expansion_receptor={v['expansion']}")

    # ---- class variants (E0.5) --------------------------------------------
    cv = []
    for cls in sorted({s["class"] for s in snapshot}):
        sub = [s for s in snapshot if s["class"] == cls]
        st = collections.Counter(s["state"] for s in sub)
        recs = collections.defaultdict(collections.Counter)
        for s in sub:
            recs[entry_slug(s["protein"])][s["state"]] += 1
        on = {entry_slug(s["protein"]) for s in sub if entry_slug(s["protein"]) in p48}
        cv.append({
            "gpcr_class": cls,
            "n_structures": len(sub),
            "n_active": st["Active"],
            "n_inactive": st["Inactive"],
            "n_intermediate": st["Intermediate"],
            "n_receptors": len(recs),
            "n_receptors_both_states": sum(1 for v in recs.values() if v["Active"] and v["Inactive"]),
            "n_receptors_on_panel48": len(on),
            "n_inactive_off_panel48": sum(
                1 for s in sub
                if s["state"] == "Inactive" and entry_slug(s["protein"]) not in p48
            ),
            "n_active_off_panel48": sum(
                1 for s in sub
                if s["state"] == "Active" and entry_slug(s["protein"]) not in p48
            ),
        })
    out = os.path.join(INPUTS, "g0_class_variants.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cv[0].keys()))
        w.writeheader()
        w.writerows(cv)
    print(f"\nwrote {os.path.relpath(out, ROOT)}  ({len(cv)} rows)")
    print()
    print("## Per-class census (E0.5)")
    for c in cv:
        print(f"  {c['gpcr_class']:<36} n={c['n_structures']:>4}"
              f"  A={c['n_active']:>4} I={c['n_inactive']:>3} Int={c['n_intermediate']:>2}"
              f"  receptors={c['n_receptors']:>3} both={c['n_receptors_both_states']:>2}"
              f"  off-panel I={c['n_inactive_off_panel48']:>3}")

    # ---- the axis gap: what the build step must measure ---------------------
    gap = []
    p48_upper = {r["slug"].upper() for r in panel if r["in_our48"] == "1"}
    for r in pinned:
        anchors = json.loads(r["anchor_positions"] or "{}")
        gap.append({
            "receptor_slug": r["receptor_slug"],
            "role": r["role"],
            "pdb_id": r["pdb_id"],
            "uniprot_slug": r["uniprot_slug"],
            "species": r["species"],
            "on_panel48": int(r["receptor_slug"].upper() in p48_upper),
            "npxxy_oh_populated": int(bool(r["d_npxxy_oh_ref"].strip())),
            "npxxy_ca_populated": int(bool(r["d_npxxy_ca_ref"].strip())),
            "tm6_tilt_populated": int(bool(r["d_gpcrdb_tm6_tilt_ref"].strip())),
            "kink_populated": int(bool(r["angle_class_b_kink_ref"].strip())),
            "anchor_5_58": anchors.get("5.58", ""),
            "anchor_7_53": anchors.get("7.53", ""),
            "anchor_2_46": anchors.get("2.46", ""),
            "anchor_6_37": anchors.get("6.37", ""),
            "anchors_present": "|".join(sorted(anchors)),
            "construct_offset": r["construct_offset"],
            "icl3_status": r["icl3_status"],
            "icl3_residues_missing_count": r["icl3_residues_missing_count"],
            "fusion_partner": r["fusion_partner"],
            "must_measure_npxxy": int(not r["d_npxxy_oh_ref"].strip()),
            "anchor_5_58_known": int("5.58" in anchors),
            "anchor_7_53_known": int("7.53" in anchors),
        })
    out = os.path.join(INPUTS, "g0_reference_axis_gap.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(gap[0].keys()))
        w.writeheader()
        w.writerows(gap)
    print(f"\nwrote {os.path.relpath(out, ROOT)}  ({len(gap)} rows)")
    on = [g for g in gap if g["on_panel48"]]
    off = [g for g in gap if not g["on_panel48"]]
    print("## The blocker, recomputed from the pinned reference set")
    print(f"  pinned rows                          {len(gap)}")
    print(f"  on-panel48 rows                      {len(on)}   NPxxY populated {sum(g['npxxy_oh_populated'] for g in on)}"
          f"   tilt populated {sum(g['tm6_tilt_populated'] for g in on)}")
    print(f"  off-panel48 rows                     {len(off)}   NPxxY populated {sum(g['npxxy_oh_populated'] for g in off)}"
          f"   tilt populated {sum(g['tm6_tilt_populated'] for g in off)}")
    print(f"  rows needing an NPxxY measurement     {sum(g['must_measure_npxxy'] for g in gap)}")
    print(f"  ...of those, 5.58 anchor already known {sum(g['must_measure_npxxy'] and g['anchor_5_58_known'] for g in gap)}")
    print(f"  ...of those, 7.53 anchor already known {sum(g['must_measure_npxxy'] and g['anchor_7_53_known'] for g in gap)}")
    print(f"  rows carrying a 2.46 anchor            {sum(1 for g in gap if g['anchor_2_46'] != '')}")
    print(f"  rows carrying a 6.37 anchor            {sum(1 for g in gap if g['anchor_6_37'] != '')}")
    bothaxes = collections.defaultdict(set)
    for g in gap:
        if g["npxxy_oh_populated"] and g["tm6_tilt_populated"]:
            bothaxes[g["receptor_slug"]].add(g["role"])
    print(f"  receptors with BOTH axes on BOTH roles {sum(1 for v in bothaxes.values() if len(v) > 1)}")

    # ---- label conflicts ---------------------------------------------------
    lc = [r for r in rows if r["flag_label_conflict"]]
    out = os.path.join(INPUTS, "g0_label_conflicts.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(lc)
    print(f"\nwrote {os.path.relpath(out, ROOT)}  ({len(lc)} rows)")
    print("## Label-versus-pharmacology conflicts, Class A, all receptors")
    for kind, grp in sorted(collections.Counter(r["flag_label_conflict"] for r in lc).items()):
        offn = sum(1 for r in lc if r["flag_label_conflict"] == kind and not r["on_panel48"])
        print(f"  {kind:<44} total {grp:>3}   off-panel48 {offn:>3}")

    # ---- transducer audit (the coordinator's circularity check) ------------
    print()
    print("## Transducer audit — what defines 'Active' in each population")
    for name, key in (("calibration (off panel48)", False), ("application (on panel48)", True)):
        pop = [r for r in rows if r["state"] != "Intermediate" and bool(r["on_panel48"]) == key]
        for st in ("Active", "Inactive"):
            c = collections.Counter(r["transducer_type"] for r in pop if r["state"] == st)
            print(f"  {name:<28} {st:<9} n={sum(c.values()):>4}  {dict(c)}")
    arr = [r for r in rows if r["flag_arrestin_active"] and not r["on_panel48"]]
    print(f"  off-panel arrestin-defined actives: {len(arr)} -> "
          f"{sorted((r['pdb_id'], r['gpcrdb_entry']) for r in arr)}")
    byrec = collections.defaultdict(list)
    for r in rows:
        if r["state"] == "Active" and not r["on_panel48"]:
            byrec[r["receptor_slug"]].append(r["transducer_type"])
    only_arr = sorted(k for k, v in byrec.items() if v and all(t == ARRESTIN_TYPE for t in v))
    only_none = sorted(k for k, v in byrec.items() if v and all(t == "none" for t in v))
    print(f"  off-panel receptors whose EVERY active is arrestin-defined: {len(only_arr)} {only_arr}")
    print(f"  off-panel receptors whose EVERY active has no transducer:   {len(only_none)} {only_none}")

    # ---- the activation-degree axis (Q0c, and E0.4's continuous reporting) --
    # `chib2025gpcrstates` Fig 2a-d reports GPCRdb activity level 0-100 as a
    # CONTINUOUS x-axis rather than binarising it.  The excluded classes are
    # therefore reported here, not discarded silently.
    dg = []
    for label, pop in (
            ("calibration (off panel48)",
             [r for r in rows if r["state"] != "Intermediate" and not r["on_panel48"]]),
            ("application (on panel48)",
             [r for r in rows if r["state"] != "Intermediate" and r["on_panel48"]]),
            ("intermediate (all)", [r for r in rows if r["state"] == "Intermediate"])):
        for st in ("Active", "Inactive", "Intermediate"):
            sub = [r for r in pop if r["state"] == st]
            if not sub:
                continue
            ds = [r["activation_degree"] for r in sub if r["activation_degree"] != ""]
            dg.append({
                "population": label, "state": st, "n": len(sub),
                "degree_min": min(ds) if ds else "",
                "degree_max": max(ds) if ds else "",
                "n_degree_100": sum(1 for d in ds if d == 100),
                "n_degree_lt_100": sum(1 for d in ds if d < 100),
                "degree_histogram": ";".join(
                    f"{k}:{v}" for k, v in sorted(collections.Counter(ds).items())),
            })
    out = os.path.join(INPUTS, "g0_activation_degree.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dg[0].keys()))
        w.writeheader()
        w.writerows(dg)
    print(f"\nwrote {os.path.relpath(out, ROOT)}  ({len(dg)} rows)")
    print("## GPCRdb activation degree — the axis rule Q0c cuts on")
    for d in dg:
        print(f"  {d['population']:<28} {d['state']:<13} n={d['n']:>4}"
              f"  range {d['degree_min']}-{d['degree_max']}"
              f"  at 100: {d['n_degree_100']:>4}   below 100: {d['n_degree_lt_100']:>4}")
    # Does Q0c subsume the Active half of Q2?
    after = [r for r in rows if r["state"] != "Intermediate" and not r["on_panel48"]
             ]
    A_all = [r for r in rows if r["state"] == "Active"]
    d100 = [r for r in A_all if r["activation_degree"] == 100]
    dlt = [r for r in A_all if r["activation_degree"] != 100]
    print("  CIRCULARITY AUDIT -- GPCRdb defines degree 100 as 'in complex with a "
          "signaling protein':")
    print(f"    of {len(d100)} degree-100 Class A actives, "
          f"{sum(1 for r in d100 if r['transducer_type'] != 'none')} have a transducer "
          f"({100 * sum(1 for r in d100 if r['transducer_type'] != 'none') / len(d100):.1f}%)")
    print(f"    of {len(dlt)} below-100 Class A actives, "
          f"{sum(1 for r in dlt if r['transducer_type'] == 'none')} have none "
          f"({100 * sum(1 for r in dlt if r['transducer_type'] == 'none') / len(dlt):.1f}%)")
    print("    => degree and transducer presence are ONE signal, not two. "
          "Rule Q0c is retracted; see GROUP0_SYSTEMS.md sec.5.1.")
    print("  label conflicts in the calibration set: "
          f"{dict(collections.Counter(r['flag_label_conflict'] for r in after if r['flag_label_conflict']))}")
    nt = [r for r in rows if r["state"] == "Active" and not r["on_panel48"]
          and r["transducer_type"] == "none"]
    print(f"  of the {len(nt)} no-transducer off-panel actives, "
          f"{sum(1 for r in nt if r['activation_degree'] != 100)} are below degree 100 "
          f"and {sum(1 for r in nt if r['activation_degree'] == 100)} are at 100")

    # ---- intermediates (E0.3) ---------------------------------------------
    inter = [r for r in rows if r["state"] == "Intermediate"]
    out = os.path.join(INPUTS, "g0_intermediates.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(sorted(inter, key=lambda r: (r["receptor_slug"], r["pdb_id"])))
    print(f"\nwrote {os.path.relpath(out, ROOT)}  ({len(inter)} rows)")
    print("## E0.3 — the 21 Class A Intermediates are 21 structures but not 21 receptors")
    c = collections.Counter(r["receptor_slug"] for r in inter)
    for k, v in c.most_common():
        onp = any(x["on_panel48"] for x in inter if x["receptor_slug"] == k)
        onp75 = any(x["on_panel75"] for x in inter if x["receptor_slug"] == k)
        print(f"  {k:<10} n={v:>2}  on_panel48={int(onp)}  on_panel75={int(onp75)}")
    print(f"  receptors={len(c)}  off-panel48 structures="
          f"{sum(1 for r in inter if not r['on_panel48'])}"
          f"  off-panel75 structures={sum(1 for r in inter if not r['on_panel75'])}")

    # ---- what still has to be fetched --------------------------------------
    need = [r for r in rows if r["state"] != "Intermediate"
            and not r["on_panel48"] and not r["rcsb_metadata_cached"]]
    print()
    print("## Build-step cost")
    print(f"  off-panel48 structures                       {len([r for r in rows if r['state'] != 'Intermediate' and not r['on_panel48']])}")
    print(f"  ...already have RCSB metadata cached          "
          f"{len([r for r in rows if r['state'] != 'Intermediate' and not r['on_panel48'] and r['rcsb_metadata_cached']])}"
          f"  (redo/cache/panel_rcsb_cache.json)")
    print(f"  ...still need an RCSB metadata fetch          {len(need)}")
    print(f"  coordinate files held in this repo for any of them: 0")
    ures = sorted({r["gpcrdb_entry"] for r in rows if r["state"] != "Intermediate"})
    print(f"  distinct GPCRdb entries needing residues/extended: "
          f"{len({r['gpcrdb_entry'] for r in rows if r['state'] != 'Intermediate' and not r['on_panel48']})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
