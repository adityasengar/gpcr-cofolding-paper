# Instrument references — how these two CIFs are used

**Anchor receptor**: GHSR (ghrelin receptor, Class A, native Gα coupling).

**Active reference**: 7NA7 (native Gα-coupled active; stabilising_elements =
none per campaign curation, alpha5_donor_class native).
**Inactive reference**: 7F83 (inactive inverse-agonist, no fusion at 7TM
core).

**Role of these references in Block B scoring**

- Each row in `rows.csv` carries a `receptor_d_active_ref`, a
  `receptor_d_inactive_ref`, and derived `delta_to_active` /
  `delta_to_inactive` columns computed against the pinned reference
  set (`refs/reference_set.blockb_pinned.csv`, SHA-256
  `6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`).
- These references were used to compute delta axes during scoring; they
  were **never shown to any predictor** — Block B is prospective per
  PREREG §11b and per the panel-wide templates-OFF audit (SC-B-7).
- Ship these CIFs in the bundle so the figure agent can overlay the
  two poles against selected predictions without going back to RCSB.

**No sealed holdout in this bundle**. The Block B campaign shipped a
sealed holdout at the receptor level for a different purpose
(cross-block audit); Block B itself scored 40 receptors including the
sealed subset. No extra sealed material is bundled here — the SEALED
header in the manifest refers only to the "used by the scorer, never
shown to any model" role of these two files.

**Files**

- `GHSR_active_7NA7.cif` — sha256 in STRUCTURE_BUNDLE_MANIFEST §4.
- `GHSR_inactive_7F83.cif` — sha256 in STRUCTURE_BUNDLE_MANIFEST §4.
- `anchor_residues.csv` — the 6 BW-numbered anchor residues used by
  the two-instrument predicate: R3.50, Y3.51, Y5.58, E/D6.30, 6.34, Y7.53.
  Tilt-axis anchors (2×46 CA and 6×37 CA) are computed via GPCRdb
  generic mapping at run time and are not tabulated here per-receptor —
  they come from `refs/gpcrdb_snapshots/` at the pinned scorer commit.
- `references.csv` — resolution / method / bound-what / transducer /
  alpha5_donor_class / two-instrument classification for both references.
