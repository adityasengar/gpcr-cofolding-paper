"""Convert a depth-limited .a3m file to Chai's .aligned.pqt format.

Tier D3 subsampling helper for the Chai backbone. `scripts/subsample_msa.py`
produces the depth-limited .a3m; this script converts it to the parquet
format Chai's `--msa-directory` reads (per
`chai_lab/data/parsing/msas/aligned_pqt.py:34-64`).

The .aligned.pqt schema Chai requires:
- Column `sequence`: str
- Column `source_database`: str, row 0 MUST be "query"
- Column `pairing_key`: str (empty string for unpaired)
- Column `comment`: str

Chai identifies MSA files by SHA-256 of the receptor sequence in uppercase:
`<sha256(seq.upper()).hexdigest()>.aligned.pqt`.

Usage:

    python3 scripts/subsample_msa_chai.py \\
        --input msa_cache/a3m/seed42/depth32/aa2ar.a3m \\
        --output-dir /hpc/scratch/sengaad1/paper_af3/msa_cache/chai_d3/seed42/depth32/ \\
        --seed 42

Requires: pyarrow (or pandas w/ pyarrow backend).

Design intent — from `experiments/024_tier_d3_msa_depth/spec/D3_BACKBONE_PLUMBING_SPEC.md`
§ Chai-1:

    scripts/subsample_msa_chai.py must produce a .aligned.pqt whose row 0
    is source_database="query" and whose row count matches the depth
    passed to the parent scripts/subsample_msa.py. Same seed → same
    sequences → byte-identical parquet.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def parse_a3m(text: str) -> list[tuple[str, str]]:
    """Same as scripts/subsample_msa.parse_a3m; duplicated to avoid import."""
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
        raise RuntimeError("empty .a3m: no header lines")
    return entries


def write_chai_pqt(
    entries: list[tuple[str, str]],
    output_path: Path,
) -> dict[str, object]:
    """Write entries to a Chai .aligned.pqt.

    Row 0 becomes source_database='query'. Subsequent rows become
    source_database='uniref90' (Chai accepts any non-'query' string,
    but 'uniref90' is the canonical bucket).

    Returns a small dict with row count + output SHA-256.
    """
    try:
        import pyarrow as pa  # type: ignore
        import pyarrow.parquet as pq  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "pyarrow required for Chai .aligned.pqt write; "
            f"install pyarrow in the Chai venv. Original error: {e}"
        ) from e

    sequences: list[str] = []
    source_databases: list[str] = []
    pairing_keys: list[str] = []
    comments: list[str] = []
    for idx, (header, seq) in enumerate(entries):
        sequences.append(seq)
        source_databases.append("query" if idx == 0 else "uniref90")
        pairing_keys.append("")
        comments.append(header[1:])

    table = pa.table(
        {
            "sequence": pa.array(sequences, type=pa.string()),
            "source_database": pa.array(source_databases, type=pa.string()),
            "pairing_key": pa.array(pairing_keys, type=pa.string()),
            "comment": pa.array(comments, type=pa.string()),
        }
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    pq.write_table(table, tmp_path)
    tmp_path.replace(output_path)

    sha = hashlib.sha256(output_path.read_bytes()).hexdigest()
    return {
        "output_path": str(output_path),
        "n_rows": len(entries),
        "sha256": sha,
    }


def sequence_sha_hex(seq: str) -> str:
    """SHA-256 hex of seq.upper() — Chai's file-naming convention."""
    return hashlib.sha256(seq.upper().encode()).hexdigest()


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True, help="Input .a3m path")
    p.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory. Chai reads files named <sha256>.aligned.pqt",
    )
    p.add_argument(
        "--seed",
        type=int,
        required=True,
        help="Deterministic subsample seed (recorded in output; must match "
             "the --seed passed to scripts/subsample_msa.py)",
    )
    p.add_argument(
        "--output-name",
        type=str,
        default=None,
        help="Override output filename (default: SHA-256 of query sequence "
             "+ '.aligned.pqt')",
    )
    p.add_argument(
        "--print-stats",
        action="store_true",
        help="Print row count + SHA-256 to stdout",
    )
    args = p.parse_args()

    if not args.input.is_file():
        p.error(f"input not found: {args.input}")

    entries = parse_a3m(args.input.read_text())
    query_seq = entries[0][1]
    if args.output_name is None:
        filename = f"{sequence_sha_hex(query_seq)}.aligned.pqt"
    else:
        filename = args.output_name
    output_path = args.output_dir / filename

    result = write_chai_pqt(entries, output_path)
    result["input_path"] = str(args.input)
    result["query_seq_sha256"] = sequence_sha_hex(query_seq)
    result["subsample_seed"] = args.seed

    if args.print_stats:
        print(
            f"chai .aligned.pqt written: {result['output_path']}\n"
            f"  rows={result['n_rows']} sha256={result['sha256']}\n"
            f"  query_seq_sha256={result['query_seq_sha256']}\n"
            f"  subsample_seed={result['subsample_seed']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
