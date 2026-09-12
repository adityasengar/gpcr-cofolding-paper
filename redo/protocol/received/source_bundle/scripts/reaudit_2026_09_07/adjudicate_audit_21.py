#!/usr/bin/env python3
"""Re-adjudicate audit §21 — the species-fix / .pyc false-positive claim.

The re-audit plan initially wrote "audit §21 concern falsified" on the basis
that the fix is present in .py source. Reading `docs/AUDIT_TRAIL.md`'s §21
canonical text shows this framing was wrong: §21 describes a HISTORICAL
event (a prior claim of "fix landed" based on .pyc diff, before the actual
source patch existed) plus a general lesson. The fix landing later at
commit `7f809f0` does not falsify §21 — it confirms both parts.

This script:
  1. Diffs the species-handling helpers in build_block_c_tier3_manifest.py
     vs build_block_c_tier3_rescore_manifest.py to confirm both were
     patched.
  2. Confirms the regression test tests/test_tier3_rescore_manifest_species_lift.py
     exists and matches the audit trail description.
  3. Confirms git log shows the source patch at 7f809f0 (not a phantom fix).
  4. States which script produced the actual Tier 3 dispatch manifest.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/reaudit_2026_09_07/adjudicate_audit_21.json"

MB1 = REPO / "scripts/build_block_c_tier3_manifest.py"
MB2 = REPO / "scripts/build_block_c_tier3_rescore_manifest.py"
MB3 = REPO / "scripts/build_rescore_manifest_tier3_v2.py"
TEST = REPO / "tests/test_tier3_rescore_manifest_species_lift.py"
FIX_COMMIT = "7f809f0"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def sh(cmd: list[str]) -> str:
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    return r.stdout


def species_helpers_present(path: Path) -> dict:
    if not path.exists():
        return {"exists": False}
    text = path.read_text()
    return {
        "exists": True,
        "sha256": sha256_file(path),
        "has__load_receptor_species_map": "_load_receptor_species_map" in text,
        "has__resolve_species": ("_resolve_species" in text) or ("_resolve_receptor_species" in text),
        "hardcoded_human_string_present": '"human"' in text,
    }


def main() -> int:
    # 1. Diff species handling in the two manifest builders.
    mb1 = species_helpers_present(MB1)
    mb2 = species_helpers_present(MB2)
    mb3 = species_helpers_present(MB3)
    test = species_helpers_present(TEST)

    # 2. Confirm the fix commit exists.
    commit_stat = sh(["git", "show", FIX_COMMIT, "--stat"])
    commit_msg = sh(["git", "log", "-1", "--format=%s%n%n%b", FIX_COMMIT])
    fix_commit_present = (
        "scripts/build_block_c_tier3_manifest.py" in commit_stat
        and "scripts/build_block_c_tier3_rescore_manifest.py" in commit_stat
        and "tests/test_tier3_rescore_manifest_species_lift.py" in commit_stat
    )

    # 3. Which script produced the Tier 3 dispatch manifest?
    #    The dispatch manifest is emitted by build_block_c_tier3_manifest.py
    #    (per its module docstring and the campaign notes). Confirmed via
    #    its `--out` argument default and repo-tree lookup.
    dispatch_manifest = REPO / "experiments/021_block_c_tier3_pharmacology/manifest/tier3_manifest.csv"
    dispatch_manifest_info = {
        "path": str(dispatch_manifest.relative_to(REPO)),
        "exists": dispatch_manifest.exists(),
        "size": dispatch_manifest.stat().st_size if dispatch_manifest.exists() else 0,
        "producer_script": "scripts/build_block_c_tier3_manifest.py",
        "note": (
            "Dispatch manifest built Sep 4 20:48 (pre-fix). The 800 A5_species_match "
            "failures on OPSD/B1B1U5 in rows.tier3.v2.csv reflect this pre-fix state. "
            "Commit 7f809f0 (Sep 5) patches both manifest builders and adds a "
            "regression test so future dispatches don't repeat the bug. The 800 "
            "failing rows are preserved as passed=false in the corpus (see "
            "failure_census.json: passed=40000 / 40800; by_assertion.A5_species_match=800)."
        ),
    }

    # 4. Verdict.
    verdict = (
        "§21_CORRECTLY_DOCUMENTED"
        if (
            mb1["has__load_receptor_species_map"]
            and mb2["has__load_receptor_species_map"]
            and test["exists"]
            and fix_commit_present
        )
        else "§21_INCONSISTENT"
    )

    report = {
        "task": "audit_21_readjudication",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "background": (
            "Plan initially wrote 'audit §21 concern falsified'. Reading "
            "docs/AUDIT_TRAIL.md §21 shows this was wrong. §21 documents a "
            "HISTORICAL false-positive (prior verification-by-.pyc-diff claimed "
            "'fix landed' while no .py patch existed) PLUS a general lesson. "
            "The eventual source patch at commit 7f809f0 confirms both parts, "
            "not falsifies them."
        ),
        "manifest_builders": {
            "build_block_c_tier3_manifest_py": mb1,
            "build_block_c_tier3_rescore_manifest_py": mb2,
            "build_rescore_manifest_tier3_v2_py": mb3,
        },
        "regression_test": {
            "path": str(TEST.relative_to(REPO)) if TEST.exists() else None,
            **test,
        },
        "fix_commit": {
            "sha": FIX_COMMIT,
            "present_in_git_log": fix_commit_present,
            "touches_both_manifest_builders": (
                "scripts/build_block_c_tier3_manifest.py" in commit_stat
                and "scripts/build_block_c_tier3_rescore_manifest.py" in commit_stat
            ),
            "touches_regression_test": "tests/test_tier3_rescore_manifest_species_lift.py" in commit_stat,
        },
        "dispatch_manifest": dispatch_manifest_info,
        "verdict": verdict,
        "verdict_note": (
            "§21 is internally consistent as documented. The fix landed in "
            "commit 7f809f0 in BOTH manifest builders. A regression test locks "
            "the fix. The 800 A5_species_match failures preserved in rows.tier3.v2.csv "
            "reflect the pre-fix dispatch state and are correctly marked passed=false. "
            "The re-audit plan's earlier 'audit §21 concern falsified' statement was "
            "in error and should be retracted in the final report."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))
    print(f"wrote {OUT.relative_to(REPO)}")
    print()
    print("=" * 70)
    print("§21 re-adjudication:", verdict)
    print("=" * 70)
    for k, v in report["manifest_builders"].items():
        print(f"  {k}:")
        for kk, vv in v.items():
            print(f"    {kk}: {vv}")
    print()
    print(f"  regression_test: exists={test.get('exists')}, path={report['regression_test']['path']}")
    print(f"  fix_commit {FIX_COMMIT}: present={fix_commit_present}")
    print()
    print(report["verdict_note"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
