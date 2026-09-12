"""Pre-generate Chai's `.aligned.pqt` MSA cache for the Block A panel.

Reads `refs/panel_receptor_sequences.fasta` + `docs/EXPERIMENT_CATALOG/sequences/partners.fasta`,
deduplicates by SHA-256, and invokes `chai_lab.data.dataset.msas.colabfold.generate_colabfold_msas`
once per unique sequence. That function:
  1. submits to ColabFold public API (cache is server-warm from the earlier
     msa_prewarm pass — expect fast returns)
  2. downloads the A3M + template hits
  3. converts to Chai's DataFrame(sequence, source_database, pairing_key, comment) parquet
  4. writes `<sha256(seq.upper()).hex>.aligned.pqt` under `--msa-dir`

Purpose: close the `chai_aligned_pqt` gate in `scripts/step7_dispatch_gate.py`.
Chai-lab 0.6.1 silently falls back to single-sequence inference when its
`--msa-directory` lacks the expected hash-named file. Without this cache,
the Block A chai arm would silently duplicate `chai_singleseq` across ~4,000
predictions and we'd only discover it at scoring.

Runs on HPC (chai-lab venv, network egress to api.colabfold.com). Idempotent —
skips sequences whose `.aligned.pqt` already exists in the cache dir.

Usage (on basel-hpc):
    source /home/sengaad1/software/venvs/chai1/bin/activate
    python3 scripts/build_chai_msa_cache.py \\
        --receptor-fasta refs/panel_receptor_sequences.fasta \\
        --partners docs/EXPERIMENT_CATALOG/sequences/partners.fasta \\
        --msa-dir /hpc/scratch/sengaad1/paper_af3/msa_cache/chai
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def parse_fasta(path: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    header, seq_lines = None, []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith(">"):
            if header is not None:
                entries.append((header, "".join(seq_lines)))
            header = line[1:]
            seq_lines = []
        elif line:
            seq_lines.append(line)
    if header is not None:
        entries.append((header, "".join(seq_lines)))
    return entries


def seq_sha(seq: str) -> str:
    return hashlib.sha256(seq.upper().encode()).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--receptor-fasta", type=Path,
                   default=REPO / "refs/panel_receptor_sequences.fasta")
    p.add_argument("--partners", type=Path,
                   default=REPO / "docs/EXPERIMENT_CATALOG/sequences/partners.fasta")
    p.add_argument("--msa-dir", type=Path,
                   default=Path("/hpc/scratch/sengaad1/paper_af3/msa_cache/chai"))
    p.add_argument("--msa-server-url", default="https://api.colabfold.com")
    p.add_argument("--limit", type=int, default=None,
                   help="cap number of sequences (for testing)")
    args = p.parse_args()

    args.msa_dir.mkdir(parents=True, exist_ok=True)

    # Collect unique sequences (dedup by SHA)
    all_entries = parse_fasta(args.receptor_fasta) + parse_fasta(args.partners)
    unique: dict[str, tuple[str, str]] = {}
    for header, seq in all_entries:
        unique.setdefault(seq_sha(seq), (header, seq))
    all_seqs = list(unique.values())
    if args.limit:
        all_seqs = all_seqs[:args.limit]

    # Filter to only sequences whose .aligned.pqt is missing
    to_generate = []
    for header, seq in all_seqs:
        pqt = args.msa_dir / f"{seq_sha(seq)}.aligned.pqt"
        if pqt.exists():
            print(f"skip  {seq_sha(seq)[:8]} len={len(seq)} — already cached")
        else:
            to_generate.append((header, seq))
            print(f"queue {seq_sha(seq)[:8]} len={len(seq)}", flush=True)

    if not to_generate:
        print(f"\nAll {len(all_seqs)} sequences already cached under {args.msa_dir}. "
              f"Nothing to do.")
        return 0

    print(f"\ngenerating {len(to_generate)} .aligned.pqt files → {args.msa_dir}")
    print("(server-warm from msa_prewarm; expect ~30-60 s per sequence)")
    print()

    # Chai-lab's generate_colabfold_msas asserts its msa_dir is empty at
    # start of each call. Work around by giving it a fresh tempdir per
    # sequence, then copy the produced .aligned.pqt into the shared cache.
    from chai_lab.data.dataset.msas.colabfold import generate_colabfold_msas
    from chai_lab.data.dataset.msas.colabfold import expected_basename

    n_ok = 0
    n_fail = 0
    for i, (header, seq) in enumerate(to_generate, 1):
        expected_name = expected_basename(seq)
        target = args.msa_dir / expected_name
        try:
            with tempfile.TemporaryDirectory(prefix="chai_msa_") as tmpdir:
                tmp_path = Path(tmpdir)
                generate_colabfold_msas(
                    protein_seqs=[seq],
                    msa_dir=tmp_path,
                    msa_server_url=args.msa_server_url,
                    search_templates=False,
                    write_a3m_to_msa_dir=False,
                )
                produced = tmp_path / expected_name
                if produced.exists():
                    shutil.copy2(produced, target)
                    n_ok += 1
                    print(f"[{i:>3}/{len(to_generate)}] ok   "
                          f"{seq_sha(seq)[:8]} → {expected_name}", flush=True)
                else:
                    # Search tempdir for any .aligned.pqt (defensive)
                    hits = list(tmp_path.glob("*.aligned.pqt"))
                    if hits:
                        shutil.copy2(hits[0], target)
                        n_ok += 1
                        print(f"[{i:>3}/{len(to_generate)}] ok*  "
                              f"{seq_sha(seq)[:8]} → {expected_name} "
                              f"(via {hits[0].name})", flush=True)
                    else:
                        n_fail += 1
                        print(f"[{i:>3}/{len(to_generate)}] FAIL "
                              f"{seq_sha(seq)[:8]} — no .aligned.pqt in "
                              f"tempdir after generate_colabfold_msas",
                              flush=True)
        except Exception as e:  # noqa: BLE001
            n_fail += 1
            print(f"[{i:>3}/{len(to_generate)}] FAIL {seq_sha(seq)[:8]} — "
                  f"{type(e).__name__}: {e}", flush=True)

    print()
    print(f"summary: {n_ok} generated, {n_fail} failed, "
          f"{len(all_seqs) - len(to_generate)} already cached, "
          f"total cache size {len(list(args.msa_dir.glob('*.aligned.pqt')))} files")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
