# received_2026_09_12 — the file Block C pinned 18 times and never shipped

**`rows.tier3.v2.csv`** — 91,972,789 bytes, **40,801 rows, 101 columns**.
sha256 **`5ccf58acc8a6b0151250007c6b40d1f728ad4b42c2eeab22bd6509b5809e2103`**.

**Provenance verified, not assumed:** that sha256 matches the full 64-hex value
**already pinned in 18 places across the Block C drop**. This is the file those
references point at.

**Why it is here and not in `data/block_c/`.** It belongs to that drop logically,
but `data/block_<x>/` is read-only by chmod as well as by rule, and adding a
directory to it would be editing the drop. It arrived separately, months later, by
a different route, so it is recorded as a late delivery in the analysis tree rather
than retro-fitted into a pristine drop.

**Arrived by hand.** Aditya approved it in the `paper_af3` session; their platform's
classifier then refused every outbound file regardless of size, so it came directly
instead. **Nobody looked for a way around that classifier.**

**Read-only (444) and gitignored by size**, per the `lit/pdfs/` and
`data/block_a/11_structures/` precedent. A fresh clone will not have it; the hash
above is the record.

## Why this was the highest-value ask in the project

Ask 1 in `analysis/block_c/DATA_REQUESTS.md`, named in `CLAUDE.md` as the single
highest-value ask across all four request documents. It unblocks:

1. **two Block C claims** currently consistency-only;
2. **the G4 off-site gate**, which fired on 8 of 12 cells and whose remedy was
   never applied;
3. **the uncrossed ligand-class × partner-presence result** that ~18,400
   already-scored predictions are sitting on;
4. **the ligand-modality question** for the redo (`DECISIONS.md` D-2026-09-12-f).

It carries `ligand_type`, `ligand_role`, `ligand_sequence`, `ligand_smiles`, both
instrument axes (`d_npxxy_y558_y753_oh`, `d_gpcrdb_tm6_tilt_246_637_ca`), the
thresholds **as applied** (`threshold_npxxy_oh_active_lt`,
`threshold_gpcrdb_tm6_tilt_active_gt`), `receptor_class`, `seed_used`,
`confidence_flag`, `input_state_claim`, and the continuous pocket readout
`pocket_ca_rmsd_active` / `_inactive` that **SC-C-6 says to prefer over the binary
call**, because the binary predicate is floor-pinned on apo and ceiling-pinned on
cognate for ~65% of cells.

## Before computing anything on it

**There is no `arm` column.** Whether a row is apo or cognate must be derived from
`input_path` / `experiment_id`. **Establish that mapping, write it down, and check
it against the g4 census's own `arm` column before trusting any result** — the
census covers 36 receptors × 4 backbones and already carries both `arm` and
`ligand_source`, so the two files can be cross-validated against each other rather
than either being taken on faith.
