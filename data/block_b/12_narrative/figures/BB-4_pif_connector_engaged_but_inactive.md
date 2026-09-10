# BB-4 — Panel D: PIF connector on engaged-but-inactive

## Purpose

Show that the decoy engaged-but-inactive cells sit at apo PIF-connector
geometry, not active — a per-prediction structural corroboration that
partner engagement without receptor activation does not push the
transmission axis. Direct evidence for the "partner is bulk; both
engagement + activation are needed" reading.

Load-bearing for **SC-B-4**.

## Data source

Primary CSV: `experiments/019_block_b_partner_selection/analysis/interface_pif_connector.csv`.

- Rows: 640 (one per cell = receptor × arm × backbone).
- Columns used: `receptor`, `arm`, `backbone`,
  `pif_p550_i340_ca_median`, `pif_i340_f644_ca_median`,
  `pif_sum_ca_median`, `cell_engaged_20`,
  `cell_active_predicate`, `bw_register` (JSON).

Derived subsetting:

- **apo (all)** — 160 cells.
- **cognate active_engaged** — 130 cells where `cell_engaged_20 AND
  cell_active_predicate`.
- **shuffled active_engaged** — 118 cells.
- **decoy active_engaged** — 69 cells.
- **decoy engaged-but-inactive** — 47 cells where `cell_engaged_20 AND
  NOT cell_active_predicate` on the decoy arm.

## Panels

**Panel D.i — box or violin of `pif_sum_ca` (Å) per subset**

- x-axis: 5 subsets: apo (all), cognate act_eng, shuffled act_eng,
  decoy act_eng, **decoy eng-but-inactive** (highlighted).
- y-axis: `pif_sum_ca` (Å), ~14 → 17.
- Median markers with IQR whiskers or box.
- Median labels: apo 15.35, cog_act_eng 16.04, shuf_act_eng 16.00,
  dec_act_eng 16.03, **dec_eng_but_inactive 15.42**.

**Panel D.ii — per-backbone dot plot for decoy engaged-but-inactive**

- x-axis: backbone ∈ {boltz, chai, of3, protenix}.
- y-axis: `pif_sum_ca` (Å), matched scale.
- Show cell-count per backbone (n = 11, 13, 13, 10).
- Reference lines: apo panel median (15.35 Å) as one dashed line;
  cognate active-engaged panel median (16.04 Å) as another.
- Values: boltz 15.09, chai 15.18, of3 15.83, protenix 15.40.
- Annotate that 3 of 4 backbones (all but OF3) sit below their own
  cognate active-engaged median cleanly; OF3 15.83 vs its own
  cognate active-engaged 15.98 is 0.15 Å below, same signed direction
  but smaller magnitude.

## Annotations

- Note "PIF connector = P5.50 Cα → I3.40 Cα + I3.40 Cα → F6.44 Cα
  distances (orthogonal axis — not used to call activation)".
- The apo–vs–active reference lines make the "engaged but at apo
  geometry" reading immediate.

## Exclusion flags to render as annotations

- Per-cell representative CIF pick: row minimizing joint (NPxxY-OH, tilt)
  z-distance to cell centroid. 640 CIFs (mean 500 KB each). Not an
  exclusion.
- Class A only (C-B-15).

## Qualified by

C-B-6 (engagement cutoff), C-B-15.
