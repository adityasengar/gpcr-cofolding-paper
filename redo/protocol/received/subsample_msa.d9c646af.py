"""Depth-limited MSA subsampling helper for Tier D3.

Reads an `.a3m` file, keeps the query sequence at row 0, then samples N-1
aligned sequences uniformly at random with a deterministic seed. Writes a
depth-limited `.a3m` file byte-identically re-producible on rerun.

Backbone consumers (Tier D3): Boltz-2, OpenFold-3-preview, Protenix v2 all
read `.a3m`. Chai uses `.aligned.pqt` (converted separately by
`scripts/subsample_msa_chai.py`, TODO).

Design intent — from `refs/PREREG.md` amendment §D-3.7:

    scripts/subsample_msa.py must take an explicit `--seed <int>` argument,
    record it in the manifest as `msa_subsample_seed`, and be
    replay-verifiable byte-identical on rerun with the same seed. Which N-1
    sequences you draw is a variance source; unseeded means the depth arms
    are not reproducible.

Usage:

    python3 scripts/subsample_msa.py \\
        --input msa_cache/a3m/full/aa2ar.a3m \\
        --output msa_cache/a3m/seed42/depth32/aa2ar.a3m \\
        --depth 32 \\
        --seed 42

    # Selfcheck: bit-identical replay on same seed
    python3 scripts/subsample_msa.py --selfcheck \\
        --input msa_cache/a3m/full/aa2ar.a3m \\
        --depth 32 \\
        --seed 42
"""
from __future__ import annotations

import argparse
import hashlib
import os
import random
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


class A3MParseError(RuntimeError):
    """Raised when the input file cannot be parsed as .a3m."""


def parse_a3m(text: str) -> list[tuple[str, str]]:
    """Parse .a3m text into list of (header, sequence) tuples.

    Preserves order. Empty entries are skipped. First entry must be present
    (used as the query).
    """
    entries: list[tuple[str, str]] = []
    header: str | None = None
    seq_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith(">"):
            if header is not None:
                entries.append((header, "".join(seq_lines)))
            header = line
            seq_lines = []
        elif line:
            seq_lines.append(line)
    if header is not None:
        entries.append((header, "".join(seq_lines)))
    if not entries:
        raise A3MParseError("empty .a3m: no header lines found")
    return entries


def format_a3m(entries: list[tuple[str, str]]) -> str:
    """Format list of (header, sequence) back to .a3m text.

    Trailing newline preserved. One sequence per line (no wrapping).
    Byte-identical to input parse-then-format on well-formed input.
    """
    out_parts: list[str] = []
    for header, seq in entries:
        out_parts.append(header)
        out_parts.append(seq)
    return "\n".join(out_parts) + "\n"


def subsample(
    entries: list[tuple[str, str]],
    depth: int,
    seed: int,
) -> list[tuple[str, str]]:
    """Return a depth-limited entries list.

    Row 0 (query) is preserved. If `len(entries) <= depth`, all entries are
    returned unchanged. Otherwise, N-1 sequences are drawn uniformly at
    random from entries[1:] using a seeded RNG.

    Determinism guarantees:
    - `random.Random(seed)` is used (never global rng).
    - The subset is sorted by ORIGINAL POSITION in the input .a3m before
      being written back. This makes the output stable under re-sort-of-
      input and easier to diff.
    """
    if depth < 1:
        raise ValueError(f"depth must be >= 1, got {depth}")
    if len(entries) <= depth:
        return list(entries)
    rng = random.Random(seed)
    n_to_draw = depth - 1  # reserve row 0 for query
    # Get indices of rows 1..N-1
    pool_indices = list(range(1, len(entries)))
    chosen = rng.sample(pool_indices, n_to_draw)
    chosen.sort()
    result = [entries[0]]  # query first
    for idx in chosen:
        result.append(entries[idx])
    return result


def sha256_hex(path: Path) -> str:
    """Return SHA-256 hex digest of a file (streaming)."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def selfcheck_deterministic(
    input_path: Path,
    depth: int,
    seed: int,
) -> tuple[bool, str, str]:
    """Run subsample twice with the same seed to a temp file and verify
    byte-identical output.

    Returns (is_identical, first_sha, second_sha).
    """
    text = input_path.read_text()
    entries = parse_a3m(text)
    a = subsample(entries, depth, seed)
    b = subsample(entries, depth, seed)
    text_a = format_a3m(a)
    text_b = format_a3m(b)
    sha_a = hashlib.sha256(text_a.encode()).hexdigest()
    sha_b = hashlib.sha256(text_b.encode()).hexdigest()
    return (sha_a == sha_b), sha_a, sha_b


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--input", type=Path, required=True, help="Input .a3m path"
    )
    p.add_argument(
        "--output",
        type=Path,
        help="Output .a3m path (omit if --selfcheck only)",
    )
    p.add_argument(
        "--depth",
        type=int,
        required=True,
        help="Target row count (query + N-1 aligned)",
    )
    p.add_argument(
        "--seed",
        type=int,
        required=True,
        help="Deterministic RNG seed (recorded in manifest)",
    )
    p.add_argument(
        "--selfcheck",
        action="store_true",
        help="Run twice and verify byte-identical output; do NOT write to --output",
    )
    p.add_argument(
        "--print-stats",
        action="store_true",
        help="Print input/output row counts + SHA-256 to stdout",
    )
    args = p.parse_args()

    if not args.selfcheck and args.output is None:
        p.error("--output is required unless --selfcheck")

    if not args.input.is_file():
        p.error(f"input not found: {args.input}")

    if args.selfcheck:
        ok, sha_a, sha_b = selfcheck_deterministic(
            args.input, args.depth, args.seed
        )
        if not ok:
            print(
                f"SELFCHECK FAIL: two runs produced different SHA:"
                f"\n  run1 {sha_a}\n  run2 {sha_b}",
                file=sys.stderr,
            )
            return 1
        print(f"SELFCHECK PASS: byte-identical replay, SHA-256 {sha_a}")
        return 0

    text = args.input.read_text()
    entries = parse_a3m(text)
    subsampled = subsample(entries, args.depth, args.seed)
    text_out = format_a3m(subsampled)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Atomic write via temp file
    tmp_path = args.output.with_suffix(args.output.suffix + ".tmp")
    tmp_path.write_text(text_out)
    tmp_path.replace(args.output)

    if args.print_stats:
        input_sha = sha256_hex(args.input)
        output_sha = sha256_hex(args.output)
        print(
            f"input:  {args.input} rows={len(entries)} sha256={input_sha}"
        )
        print(
            f"output: {args.output} rows={len(subsampled)} "
            f"depth_target={args.depth} seed={args.seed} sha256={output_sha}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
