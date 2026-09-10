# C-B-3 — `rows.fold_integrity.csv` has 0% per-row provenance

## Caveat

`experiments/019_block_b_partner_selection/analysis/rows.fold_integrity.csv`
carries **0%** coverage on the three load-bearing per-row provenance
columns (`scorer_git_sha`, `input_sha256`, `ref_set_csv_sha256`). Only
`input_path` is 100% populated at row grain.

Provenance rests on a **header comment** on line 1:

```
# rules: {..., "input_rows_csv_sha256": "c65b93c2e08b45992dcaa0e9f63a6874785cabab4bc08373ab35c82ad511d705",
          "n_workers": 16, "wall_time_s": 29.0}
```

This SHA matches on-disk rows.csv byte-for-byte (Phase 0 §0a).

## Why it matters

- Trigger check: Phase 2 dispatch flags "provenance coverage < 80% on a
  load-bearing column" — 2 of 3 columns are below 80% on this file.
  Reported per phase brief.
- Not corpus-invalidating: every row is joinable back to a rows.csv row
  via `input_path`, and rows.csv carries per-row `scorer_git_sha` +
  `input_sha256` + `ref_set_csv_sha256`. Fold-integrity is a
  *derived-from-rows.csv* screen, not a scoring output, and doesn't
  score CIFs directly.
- Load-bearing for reproducibility: any downstream consumer that reads
  `rows.fold_integrity.csv` without joining against `rows.csv` cannot
  recover per-row scorer identity. Recommend fixing the emitter for
  future dispatches (D3 memory note reports per-row `scorer_git_sha`
  already lands on fold_integrity in D-tier).

## Affects

- SC-B-5 (fold integrity TM6 helicity 0.988). Claim is unaffected in
  substance — the join back to rows.csv works — but users must know the
  provenance path.

## Manuscript sentence

> `rows.fold_integrity.csv` carries per-row `input_path` but not per-row
> `scorer_git_sha` / `input_sha256` / `ref_set_csv_sha256`; provenance
> is anchored via a `# rules:` header comment pinning
> `input_rows_csv_sha256 = c65b93c2…` (matches on-disk rows.csv
> byte-for-byte). Every fold-integrity row is recoverable by joining
> against rows.csv via `input_path`.

## Related

- MANUSCRIPT_FLAGS.md Flag B-23.
- Phase 2 §2d provenance coverage matrix.
