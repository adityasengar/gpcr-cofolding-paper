#!/bin/bash
#
# qsub/apply_vendored_of3_patch.sh — idempotently apply the paper_af3
# vendored patch for the OF3 start_seed=42 hardcode (audit trail #13).
#
# Root cause is in
#   <of3_venv>/lib/python3.13/site-packages/openfold3/entry_points/
#     experiment_runner.py:611
# where `if num_model_seeds:` hardcodes `start_seed = 42` and overwrites
# any launcher-provided seeds via `generate_seeds(42, N)`. See
# refs/of3_seed_bug_mechanism.md for the full mechanism.
#
# The current `qsub/rerun_of3.sh` avoids the bug by passing runner-yaml
# seeds and omitting --num-model-seeds. This vendored patch is
# belt-and-braces: any future launcher that inadvertently re-adds
# --num-model-seeds hard-fails at experiment_runner.py:611 instead of
# silently reactivating the seed collapse.
#
# Usage
# -----
#     bash qsub/apply_vendored_of3_patch.sh [/path/to/of3/venv]
#
# The venv path defaults to $OF3_VENV or /home/sengaad1/software/venvs/openfold3.
#
# Exit codes
# ----------
#   0  patch applied (or already applied — idempotent)
#   1  venv/target missing, patch input malformed, or hunk did not apply

set -euo pipefail

OF3_VENV="${1:-${OF3_VENV:-/home/sengaad1/software/venvs/openfold3}}"
TARGET="$OF3_VENV/lib/python3.13/site-packages/openfold3/entry_points/experiment_runner.py"
DIFF_PATH="$(cd "$(dirname "$0")" && pwd)/openfold3_vendored_patch.diff"
SENTINEL="paper_af3 vendored patch"

if [ ! -f "$TARGET" ]; then
    echo "FATAL: target file missing at $TARGET" >&2
    echo "       OF3_VENV=$OF3_VENV; is the venv installed?" >&2
    exit 1
fi
if [ ! -f "$DIFF_PATH" ]; then
    echo "FATAL: patch file missing at $DIFF_PATH" >&2
    exit 1
fi

# Already applied?
if grep -qF "$SENTINEL" "$TARGET"; then
    echo "[apply_vendored_of3_patch] already applied at $TARGET"
    exit 0
fi

# Detect that the pre-patch line is present before applying.
if ! grep -q "start_seed = 42" "$TARGET"; then
    echo "FATAL: neither sentinel nor pre-patch marker present in $TARGET." >&2
    echo "       Upstream may have changed; patch aborted." >&2
    exit 1
fi

BACKUP="${TARGET}.pre_paper_af3_patch"
cp -f "$TARGET" "$BACKUP"

# Apply. The diff was written against site-packages/openfold3/entry_points/
# experiment_runner.py; use -p1 with cwd at .../site-packages so the a/…
# b/… prefixes strip cleanly.
SITE_PACKAGES="$OF3_VENV/lib/python3.13/site-packages"
(cd "$SITE_PACKAGES" && patch -p1 --forward < "$DIFF_PATH") || {
    echo "FATAL: patch did not apply cleanly. Restoring $BACKUP → $TARGET." >&2
    cp -f "$BACKUP" "$TARGET"
    exit 1
}

# Verify sentinel now present.
if ! grep -qF "$SENTINEL" "$TARGET"; then
    echo "FATAL: post-apply verification failed — sentinel not found in $TARGET." >&2
    cp -f "$BACKUP" "$TARGET"
    exit 1
fi

echo "[apply_vendored_of3_patch] applied at $TARGET (backup: $BACKUP)"
exit 0
