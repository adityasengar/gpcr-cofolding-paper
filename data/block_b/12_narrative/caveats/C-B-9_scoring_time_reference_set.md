# C-B-9 — Block B was scored against `6ee2cad8`; 6 inactive rows added post-run but not primaries

## Caveat

Block B rows.csv self-pins `ref_set_csv_sha256 =
6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef` on 100%
of 32,000 rows. On-disk `refs/reference_set.csv` at HEAD is a superset
of these bytes: commit `d9c646a` (2026-09-06) added 6 inactive rows for
5 receptors (AA2AR/5MZP, ADA1A/7YMJ, ADRB2/2RH1, ADRB2/3NYA, CCR5/4MBS,
CNR1/5TGZ); commit `cda27e2` (this session) landed 2 annotation-only
edits (AGTR1 6OS2 β-arrestin-biased; CNR2 5ZTY multi-mutation).

**Rowset diff on `(receptor_slug, role, pdb_id)`**:

| Transition | Rows added | Rows removed | Same-key mutation |
|---|---:|---:|---:|
| 6ee2cad8 → 7a261988 (d9c646a) | 6 | 0 | 0 |
| 7a261988 → 65738cfe (cda27e2) | 0 | 0 | 0 (annotation-only) |

**No PDB ID moved. No numeric or anchor column was overwritten for a
same-key row.** Block B was scored against a strict subset of the current
HEAD reference set.

## Preload check — the three Block B receptors that gained an inactive ref

Of the 6 added inactive rows, three cover Block B receptors:

| receptor | primary inactive in blockb_pinned | tilt_ref (Å) | npxxy_ref (Å) | axis affected |
|---|---|---:|---:|---|
| AA2AR | **5NM4** (present) | 11.99 | 9.73 | none — computable on both axes |
| ADRB2 | **6PS2** (present) | 11.75 | 11.33 | none — computable |
| CNR1 | **5U09** (present) | 11.10 | 11.61 | none — computable |

**The "missing inactive at scoring time" preload does not correspond to
the primary inactive references for these three receptors.** The added
inactive refs are secondaries; the primaries were always present in
`6ee2cad8`; scoring produced valid `delta_to_inactive` and
`rmsd_to_inactive_ref` on all three receptors' rows.

## Why it matters

- Any Block B downstream analysis that reads `refs/reference_set.csv`
  at HEAD without SHA verification is reading a different file than
  Block B was scored against. The archived
  `refs/reference_set.blockb_pinned.csv` (SHA-verified byte-identical
  to `6ee2cad8`, 163 lines, commit `8e5ea48`) is the file downstream
  consumers should read.
- Not corpus-invalidating: rows self-pin `ref_set_csv_sha256`
  row-by-row, so the correct reference set is recoverable via that SHA
  from git history (commit `a355977`).

## Affects

- SC-B-6 (Outcome A, residual test): reads the archived pinned file
  and asserts its SHA rather than reading `refs/reference_set.csv`
  at HEAD.
- SC-B-13 (reference audit).

## Manuscript sentence

> Block B was scored against `ref_set_csv_sha256 = 6ee2cad8…`, the
> reference set as of commit `a355977` (durably archived at
> `refs/reference_set.blockb_pinned.csv` at commit `8e5ea48`). Six
> inactive references were added to `refs/reference_set.csv` after
> Block B's rescore finished (commit `d9c646a`, 2026-09-06); none of the
> six shifts the primary inactive reference of any Block B receptor,
> so all `delta_to_inactive` and `rmsd_to_inactive_ref` values on Block
> B rows are computable and stable. Downstream consumers of Block B
> read the archived pinned file, not `refs/reference_set.csv` at HEAD.

## Related

- MANUSCRIPT_FLAGS.md Flag B-6.
- Phase 0 §0c, Phase 0 addendum Q-A/Q-B, Phase 6c preload check #3.
- Commit `8e5ea48` (blockb_pinned archive).
