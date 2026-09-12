#!/usr/bin/env bash
# paper_af3 — install laptop git hooks (Wave 2).
#
# Idempotent: symlinks scripts/hooks/pre-commit into .git/hooks/pre-commit.
# Re-running is safe. Backups any pre-existing non-symlink hook to
# .git/hooks/pre-commit.pre_af3_backup for review.
#
# Usage:
#   bash scripts/hooks/install.sh
set -eu

REPO_ROOT="$(git rev-parse --show-toplevel)"
SRC="$REPO_ROOT/scripts/hooks/pre-commit"
DST="$REPO_ROOT/.git/hooks/pre-commit"

if [ ! -f "$SRC" ]; then
    printf 'install: %s missing\n' "$SRC" >&2
    exit 1
fi

chmod +x "$SRC"
mkdir -p "$(dirname "$DST")"

if [ -L "$DST" ]; then
    current_target="$(readlink "$DST")"
    if [ "$current_target" = "$SRC" ]; then
        printf 'install: %s already points at %s (no-op)\n' "$DST" "$SRC"
        exit 0
    fi
    printf 'install: replacing existing symlink %s -> %s\n' "$DST" "$current_target"
    rm "$DST"
elif [ -f "$DST" ]; then
    backup="$DST.pre_af3_backup"
    printf 'install: preserving existing hook to %s\n' "$backup"
    mv "$DST" "$backup"
fi

ln -s "$SRC" "$DST"
printf 'install: symlinked %s -> %s\n' "$DST" "$SRC"
