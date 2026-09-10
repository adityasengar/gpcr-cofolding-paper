# C-B-4 — No `outputs/` symlink for Block B (ergonomic)

## Caveat

`experiments/019_block_b_partner_selection/` on the laptop has no
`outputs -> /hpc/scratch/sengaad1/paper_af3/experiments/019_block_b_partner_selection`
symlink of the kind Block A carries
(`experiments/018_block_a_switch_test/outputs -> /hpc/scratch/…`).

Every Block B `input_path` in rows.csv is an HPC absolute path:

```
/hpc/scratch/sengaad1/paper_af3/experiments/019_block_b_partner_selection/
  019_block_b_partner_selection_<rec>_<arm>_<bb>/<hash>/<bb>/seed_<N>/…/*.cif
```

## Why it matters

- Every Block B row is byte-addressable via `input_sha256` regardless
  of the symlink — this is an ergonomic gap, not a provenance gap.
- On the laptop, CIF resolution requires either the HPC scratch mount
  to be active (in which case the absolute path works directly), or an
  ssh/scp round-trip.
- HPC scratch is scratch; deletion policy is external. Block A's rows.csv
  presumably points to the same scratch prefix, so the symlink doesn't
  buy resilience — only ergonomic addressing.

## Affects

- SC-B-10 (grid-complete corpus). Claim substance unaffected; downstream
  laptop-side path-based tooling assumes the symlink exists on Block A
  and finds it missing on Block B.

## Manuscript sentence

*None required in the manuscript.* If a Methods paragraph documents
laptop-side reproducibility ergonomics, a one-line addition:

> Block B CIFs live at `/hpc/scratch/sengaad1/paper_af3/experiments/019_block_b_partner_selection/…`
> and are byte-addressable via `input_sha256` on `rows.csv`; laptop-side
> path resolution assumes the HPC scratch mount is available.

## Related

- MANUSCRIPT_FLAGS.md Flag B-22 (add symlink for laptop-side convenience).
- Phase 2 §2e.
