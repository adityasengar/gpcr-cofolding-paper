#!/usr/bin/env python3
"""Stage 0 gate for the 2026-09-07 Block C v5 re-audit.

Parses the SHA pins in ``docs/BLOCK_C_PAPER_DRAFT_v1.md`` and verifies every
file's on-disk SHA-256 against the manuscript. Two appendix paths are known-bare
(``verification/cohens_d_block_a_d_tm6.json`` and
``verification/aa2ar_unimodal_block_a_counter.json``); those files actually live
under ``experiments/018_block_a_switch_test/analysis/verification/``. The
verifier tries both locations and records which resolved.

Also records the current SHA-256 of the load-bearing driver scripts so downstream
tasks can pin against the same code state.

Exits non-zero on any manuscript-pin mismatch (excluding the ceremony-gated
``refs/reference_set.csv`` line, which the appendix flags as expected to move).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

MANUSCRIPT = REPO / "docs" / "BLOCK_C_PAPER_DRAFT_v1.md"

PINS: list[tuple[str, str, str]] = [
    # (kind, appendix_path, sha256)
    (
        "verification",
        "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_F_v5_clean_bound_stripped.json",
        "524672ee87f6d93aa169dc5120f34cb49f42cfad90b85ea5913f91d3e39f4cfe",
    ),
    (
        "verification",
        "verification/task_A_v3_composition_check.json",
        "f7a8c199b5beed19c3d128729ea2ee5241e38af4396c7639b1fa08e7455c237b",
    ),
    (
        "verification",
        "verification/task_E_v3_scoped_finding.json",
        "caa0226e19ccb3eb1faf69ab067dfcd635bc3b60145d828c075d1de7c16a17d0",
    ),
    (
        "verification",
        "verification/stage3_2x2_ligand_state_specificity.json",
        "0cf2707b52c70c57397ea89346ff0a9acc8109fb220d1be2b56b37de385c4401",
    ),
    (
        "verification",
        "verification/task6_p0_correlation.json",
        "d4193bf62672287a343461d507fd1e0ed9d1ff59e1381fc8106d17d53b7b98c7",
    ),
    (
        "verification",
        "verification/STAGE_POST_AUDIT_REPORT_v5.md",
        "2e764ddc87abaf8b44431a12b833653bb76bd8bf24f86b65a8e0cd85383442f3",
    ),
    (
        "verification",
        "verification/cohens_d_block_a_d_tm6.json",
        "0adb183a4e6efe9bbc062acce5f40c2078875ef1fff4a0aba717dc4eb9b9d443",
    ),
    (
        "verification",
        "verification/aa2ar_unimodal_block_a_counter.json",
        "5e873270d9826a6d8c907783a0ce1c43e9f9f117e595ab0526c9cc2d02b54513",
    ),
    (
        "verification",
        "verification/p4_p5_v2_corpus_recompute.json",
        "3731175baf27461a10877764cf19b566b81b3fd172a8be471130ff075f8b06b8",
    ),
    (
        "csv",
        "experiments/018_block_a_switch_test/analysis/rows.pocket.csv",
        "49d19da9a916939bb9a1429ea11aef0b43d6f8242beaa03e309a2755eff2bc58",
    ),
    (
        "csv",
        "experiments/018_block_a_switch_test/analysis/rows.rmsd.csv",
        "a82ad56076bb48edcd8723d6fbd52349a409fc4e09b1be170fa4df62914f302e",
    ),
    (
        "csv",
        "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv",
        "5ccf58acc8a6b0151250007c6b40d1f728ad4b42c2eeab22bd6509b5809e2103",
    ),
    (
        "csv_ceremony_gated",
        "refs/reference_set.csv",
        "7a261988ff73eedc9d21e5cc2a9eaf0436b9f38e3827a87493295a8d8382b90c",
    ),
    (
        "csv",
        "refs/tier3_panel.csv",
        "63cdd49c3380b89202fadc6439e06e5e412452c1c96c6105a66dcf897fc76e6f",
    ),
]

# Bare ``verification/...`` paths in the appendix that must be resolved
# against Block A's verification dir when the Tier 3 dir doesn't hold the file.
BLOCK_A_VERIFICATION_FILES = {
    "verification/cohens_d_block_a_d_tm6.json",
    "verification/aa2ar_unimodal_block_a_counter.json",
}

DRIVER_SCRIPTS = [
    "scripts/stage3_post_audit_analysis.py",
    "scripts/post_audit_corrections/lib_common.py",
    "scripts/post_audit_corrections/task_f_v5_clean_bound.py",
    "scripts/post_audit_corrections/task_e_v3_scoped_finding.py",
    "scripts/post_audit_corrections/task_a_v3_composition_check.py",
    "scripts/post_audit_corrections/task_p4_p5_v2_corpus_recompute.py",
    "experiments/021_block_c_tier3_pharmacology/analysis/verification/_task6_p0_correlation.py",
    "scorer/pocket_metrics.py",
    "scorer/references.py",
    "scripts/analyse_block_c_tier3_headline.py",
    "scripts/analyse_block_c_tier1_headline.py",
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_appendix_path(app_path: str) -> Path | None:
    """Resolve an appendix-relative path to a concrete filesystem path.

    Handles the two known bare ``verification/...`` cases for Block A files.
    Returns None if nothing resolves.
    """
    if app_path.startswith("experiments/") or app_path.startswith("refs/"):
        candidate = REPO / app_path
        return candidate if candidate.exists() else None

    if app_path in BLOCK_A_VERIFICATION_FILES:
        # Try Block A first (known location); fall through to Tier 3 otherwise.
        block_a = (
            REPO
            / "experiments"
            / "018_block_a_switch_test"
            / "analysis"
            / app_path
        )
        if block_a.exists():
            return block_a
        tier3 = (
            REPO
            / "experiments"
            / "021_block_c_tier3_pharmacology"
            / "analysis"
            / app_path
        )
        return tier3 if tier3.exists() else None

    # Generic bare `verification/...` → Tier 3.
    if app_path.startswith("verification/"):
        candidate = (
            REPO
            / "experiments"
            / "021_block_c_tier3_pharmacology"
            / "analysis"
            / app_path
        )
        return candidate if candidate.exists() else None

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default=str(
            REPO
            / "experiments"
            / "021_block_c_tier3_pharmacology"
            / "analysis"
            / "reaudit_2026_09_07"
            / "stage0_provenance.json"
        ),
    )
    parser.add_argument(
        "--allow-ceremony-drift",
        action="store_true",
        help=(
            "Do not treat a ``refs/reference_set.csv`` SHA drift as a gate "
            "failure. The manuscript appendix flags this pin as expected "
            "to move on the pending Gate 2 ceremony commit."
        ),
    )
    args = parser.parse_args()

    results: list[dict] = []
    mismatches = 0
    missing = 0
    ceremony_drift = 0

    print("=" * 70)
    print("Stage 0 — manuscript-pin verification")
    print("=" * 70)

    for kind, app_path, expected in PINS:
        resolved = resolve_appendix_path(app_path)
        row = {
            "kind": kind,
            "appendix_path": app_path,
            "resolved_path": str(resolved.relative_to(REPO)) if resolved else None,
            "expected_sha256": expected,
            "actual_sha256": None,
            "status": None,
        }
        if resolved is None:
            row["status"] = "MISSING"
            missing += 1
            print(f"MISSING  {app_path}")
        else:
            actual = sha256_file(resolved)
            row["actual_sha256"] = actual
            if actual == expected:
                row["status"] = "MATCH"
                print(
                    f"MATCH    {app_path}"
                    + (
                        f"  (resolved -> {resolved.relative_to(REPO)})"
                        if resolved != REPO / app_path
                        else ""
                    )
                )
            else:
                row["status"] = "MISMATCH"
                if kind == "csv_ceremony_gated":
                    ceremony_drift += 1
                    print(
                        f"CEREMONY-DRIFT  {app_path}\n"
                        f"    expected: {expected}\n"
                        f"    actual:   {actual}"
                    )
                else:
                    mismatches += 1
                    print(
                        f"MISMATCH {app_path}\n"
                        f"    expected: {expected}\n"
                        f"    actual:   {actual}"
                    )
        results.append(row)

    print()
    print("-" * 70)
    print("Driver script SHA snapshot (informational)")
    print("-" * 70)
    scripts: list[dict] = []
    for rel in DRIVER_SCRIPTS:
        p = REPO / rel
        if not p.exists():
            scripts.append({"path": rel, "sha256": None, "status": "MISSING"})
            print(f"MISSING  {rel}")
            continue
        actual = sha256_file(p)
        scripts.append({"path": rel, "sha256": actual, "status": "PRESENT"})
        print(f"{actual}  {rel}")

    print()
    print("=" * 70)
    print(
        f"Verification pins: {len(PINS)}   "
        f"MATCH: {sum(1 for r in results if r['status'] == 'MATCH')}   "
        f"MISMATCH: {mismatches}   "
        f"CEREMONY-DRIFT: {ceremony_drift}   "
        f"MISSING: {missing}"
    )
    print("=" * 70)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "task": "stage0_provenance",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "manuscript": str(MANUSCRIPT.relative_to(REPO)),
        "n_pins": len(PINS),
        "n_match": sum(1 for r in results if r["status"] == "MATCH"),
        "n_mismatch": mismatches,
        "n_ceremony_drift": ceremony_drift,
        "n_missing": missing,
        "pins": results,
        "driver_scripts": scripts,
        "allow_ceremony_drift": args.allow_ceremony_drift,
    }
    out.write_text(json.dumps(payload, indent=2))
    print(f"\nWrote {out.relative_to(REPO)}")

    if missing > 0 or mismatches > 0:
        return 1
    if ceremony_drift > 0 and not args.allow_ceremony_drift:
        print("\nCeremony-gated drift detected. Pass --allow-ceremony-drift to continue.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
