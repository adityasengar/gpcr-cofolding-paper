#!/usr/bin/env python3
"""Task D — root-cause the 800 A5_species_match failures on OPSD +
B1B1U5. Emits a JSON with the exact check logic, the mechanism, the
Step 1.3 finding, and a recommendation."""
from __future__ import annotations
import argparse, csv, json, re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import REPO, build_recon_meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rescore_v2/rows.csv")
    ap.add_argument("--manifest", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rescore_manifest.tier3.v2.csv")
    ap.add_argument("--ref-set", type=Path,
                    default=REPO / "refs/reference_set.csv")
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/task_D_species_match_root_cause.json")
    args = ap.parse_args()

    # Count failed rows by receptor (using input_path since receptor_slug
    # is empty on A5 raises).
    pattern = re.compile(r'/tier3/pool/([a-zA-Z0-9]+)/')
    failed_by_rec = Counter()
    with args.rows.open() as f:
        for r in csv.DictReader(f):
            if str(r.get("passed", "")).lower() != "true":
                m = pattern.search(r.get("input_path", ""))
                if m:
                    failed_by_rec[m.group(1).upper()] += 1

    # Manifest species assignment for OPSD/B1B1U5
    manifest_species = Counter()
    with args.manifest.open() as f:
        for r in csv.DictReader(f):
            rec = (r.get("receptor_slug") or "").strip().upper()
            if rec in ("OPSD", "B1B1U5"):
                manifest_species[(rec, r.get("input_species", ""))] += 1

    # Reference species per receptor
    ref_species = {}
    with args.ref_set.open() as f:
        for r in csv.DictReader(f):
            rec = (r.get("receptor_slug") or "").strip().upper()
            if rec not in ("OPSD", "B1B1U5"):
                continue
            role = (r.get("role") or "").strip().lower()
            ref_species.setdefault(rec, {})[role] = {
                "pdb_id": r.get("pdb_id"),
                "species": r.get("species"),
            }

    payload = {
        "task": "D_species_match_root_cause",
        "reconstruction": {
            "reconstruction_script": __file__,
            **build_recon_meta({
                "rescore_v2_rows_csv": args.rows,
                "rescore_manifest_v2_csv": args.manifest,
                "ref_set_csv": args.ref_set,
            }),
        },
        "failure_signature": {
            "assertion_id": "A5_species_match",
            "n_failed_rows": sum(failed_by_rec.values()),
            "failed_by_receptor": dict(failed_by_rec),
        },
        "check_source_and_logic": {
            "location": "scorer/references.py::check_species (lines 285-306)",
            "logic_prose": (
                "The check compares row.input_species (case-insensitive) "
                "against the reference PDB's species field (from "
                "refs/reference_set.csv). If they differ, raises "
                "A5SpeciesMismatch. The reference role selected is "
                "the role for the input_state_claim — 'active' for "
                "Ga-coupled-active / arrestin-coupled, 'inactive' for "
                "inactive-antagonist / inactive-inverse-agonist."
            ),
            "gate_source_line": (
                "if ref.species.lower() != input_species.lower(): raise "
                "A5SpeciesMismatch(...)"
            ),
        },
        "mechanism_diagnosis": {
            "reference_species_per_receptor": ref_species,
            "manifest_input_species_assignments": {
                f"{rec}::{sp!r}": n
                for (rec, sp), n in manifest_species.items()
            },
            "root_cause": (
                "The Tier 3 dispatch manifest builder "
                "(scripts/build_block_c_tier3_rescore_manifest.py:108) "
                "reads `species` from the pool queue metadata and "
                "falls back to 'human' when that field is empty. For "
                "OPSD and B1B1U5, the queue metadata's `species` field "
                "is empty, so the manifest assigns input_species='human' "
                "to all 400 rows per receptor. Meanwhile, "
                "refs/reference_set.csv correctly labels OPSD's PDBs "
                "(4X1H, 7ZBC) as species='bovin' and B1B1U5's PDBs "
                "(9EPR, 6I9K) as species='9arac'. The check is doing "
                "its job — a 'human' construct cannot be validly "
                "scored against a bovine / spider reference."
            ),
        },
        "verdict_legitimate_vs_bug": (
            "LEGITIMATE — the A5 check is CORRECTLY rejecting the "
            "mismatch. The bug is not in the scorer; it is in the "
            "Tier 3 dispatch manifest, which failed to tag OPSD and "
            "B1B1U5 with their true species. In Block A "
            "(experiments/018_block_a_switch_test/analysis/rows.pocket.csv), "
            "OPSD and B1B1U5 rows all pass — meaning Block A's "
            "manifest DID tag them correctly. Only Block C Tier 3 has "
            "the mis-tag."
        ),
        "step_1_3_finding": (
            "The Post-Audit Task 9a search "
            "(verification/task9_provenance.json::9a_species_fix_propagation) "
            "grep'd for A5_species_match fix commits and found NONE. "
            "The 'MISMATCH_INSTANCE_OF_AUDIT_10_PATTERN' verdict-string "
            "was a false-positive from __pycache__/*.pyc bytecode diffs "
            "only. No code fix under 'A5_species_match' was ever "
            "landed. The 'Step 1.3 fixed species-match' phrasing in "
            "prior handoffs is not supported by the commit history — "
            "it refers to a task that did not produce a code change. "
            "The 800 failures are the third occurrence because the "
            "root cause (Tier 3 manifest species defaulting to 'human') "
            "was never patched."
        ),
        "recommendation": (
            "(a) ACCEPT the exclusion for the current v2 corpus: the "
            "800 rows are legitimately excluded from the human Class-A "
            "activation predicate; OPSD and B1B1U5 are non-human "
            "controls and should not enter a human-only aggregate. "
            "(b) BEFORE any future Tier-3-like dispatch: patch "
            "scripts/build_block_c_tier3_rescore_manifest.py to lift "
            "`species` from a receptor→species lookup (e.g. keyed off "
            "refs/reference_set.csv's active/inactive rows) rather "
            "than defaulting to 'human'. Add a preflight assertion "
            "that raises when any manifest row has 'human' for OPSD, "
            "B1B1U5, TAA7F, or any other non-human panel receptor. "
            "(c) STOP CALLING the 'species fix' landed — task 183's "
            "line item was a task-tracker entry, not a code commit; "
            "no assertion or manifest builder has been patched."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print("wrote", args.out)


if __name__ == "__main__":
    raise SystemExit(main() or 0)
