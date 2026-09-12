# Tier 3 antagonist-side sidecar — curation notes

Companion to `refs/pending_curation_block_c_tier3.csv`. Landed 2026-09-04
by Block C Tier 3 Stage 2 (pocket-dissection prep for Tier 4). Covers all
40 Class A panel receptors listed in `refs/tier3_panel.csv`.

**Sidecar shape:** 42 rows over 40 receptors — 37 real PDB refs plus 5 `pdb_id=NA` rows.
- 18 rows mirrored from Tier 1 sidecar (Category A, 16 receptors, of which
  ADRB2 and AA2AR carry both a neutral-antagonist and inverse-agonist row).
- 20 rows newly curated (Category C, 20 receptors, all RCSB-verified).
- 4 `pdb_id=NA` rows for Category C receptors where RCSB verification
  disqualified the reference_set.csv pick and no clean orthosteric antagonist
  crystal exists in the PDB.
- 1 `pdb_id=NA` row for 5HT1B (already documented in
  `refs/reference_set_named_exclusions.md`, mirrored here for panel coverage).

**Discipline:** RMSD-driver populates `d_*_ref`, `a100_*`, `angle_class_b_kink_ref`,
`provenance_sha256` at merge time — hand-filling these was out of scope
(matches Tier 1 sidecar discipline). Anchor positions and structural-metadata
columns (`stabilising_elements`, `construct`, `fusion_partner`, `icl3_status`)
carry forward from `refs/reference_set.csv` for the same PDB where possible,
or are freshly assigned from the RCSB record.

## Category A — mirrored from Tier 1 sidecar (16 receptors, 18 rows)

Copied verbatim from `refs/pending_curation_block_c.csv` for panel receptors
that appear in both Tier 1 (Wave A ligand panel) and Tier 3 (transmission
panel). `curation_note` re-stamped `dispatch_tier=tier3;
ancestor_row=pending_curation_block_c.csv:L<n>;
merge_disposition=already_merged_into_reference_set;
sidecar_source=pending_curation_block_c_tier3.csv`.

Tier 4 consumes a single sidecar (this one); Tier 1 sidecar remains
the historical record for Wave A and is not touched.

Receptors: 5HT2C, AA1R, AA2AR (×2), ACM2, ACM4, ADRB2 (×2), CCR5, CNR1, CNR2,
DRD2, DRD3, HRH1, NPY1R, OPRD, OPRK, OX2R.

## Category C — new curation (20 receptors) + 4 `pdb_id=NA`

Each fetched from https://www.rcsb.org/structure/&lt;PDB&gt; with a WebFetch
prompt asking for resolution, ligand CCD, receptor identity, pharmacological
class, PMID/DOI, deposition date, and one supporting sentence from the record.

### 5HT5A — 7UM4 (AS2674723, NN6, 2.80 Å)
- RCSB: https://www.rcsb.org/structure/7UM4
- Ligand class: **neutral antagonist** — RCSB record title: "Crystal
  structure of inactive 5-HT5AR in complex with AS2674723".
- Primary lit: PMID 35835867, Tanaka 2022 Nat Struct Mol Biol.
- Deposited 2022-04-06 — post-AF3 training cutoff 2021-09-30.
  `prospective_candidate=true`.
- Kept.

### ACM1 — 5CXV (tiotropium, 0HK, 2.70 Å) — REPLACED reference_set.csv pick 6ZFZ
- RCSB verification of `refs/reference_set.csv`'s 6ZFZ pick returned
  ligand HTL9936 (CCD QJT) classified as **partial agonist**:
  "rationally designed the optimal properties, including selectivity and
  partial agonism, into HTL9936" (RCSB record for 6ZFZ, PMID 34822784).
- Partial agonist fails the antagonist reference criterion for
  `ligand_rmsd_to_ref`. Substituted with 5CXV (tiotropium inverse
  agonist, Thal 2016 Nature, PMID 26958838).
- RCSB record for 5CXV: "Here we report the crystal structures of the M1
  and M4 muscarinic receptors bound to the inverse agonist, tiotropium."
- **FLAG for coordinator:** `refs/reference_set.csv` currently lists
  6ZFZ as `inactive-antagonist`. Consider updating that row's role or
  swapping to 5CXV at merge time.

### ADA2A — 6KUX (E3F "RSC-decahydroisoquinolino-naphthyridine", 2.70 Å)
- RCSB: https://www.rcsb.org/structure/6KUX
- Ligand class: **neutral antagonist** — record title: "Crystal structures
  of the alpha2A adrenergic receptor in complex with an antagonist RSC".
- Primary lit: "To be published" as of RCSB fetch (2026-09-04). PDB
  entry data confirms antagonist classification.
- BRIL fusion at ICL3.
- Kept.

### ADRB1 — 7BVQ (carazolol, CAU, 2.50 Å)
- RCSB: https://www.rcsb.org/structure/7BVQ
- Ligand class: **antagonist** (carazolol is a canonical beta-blocker;
  historically classified as partial inverse agonist at β1, but the
  reference_set.csv row `inactive-inverse-agonist` and RCSB's classification
  as "antagonist" are consistent within the drift class).
- Sidecar `role` set to `inactive_neutral_antagonist` (conservative;
  matches RCSB's own classification).
- Primary lit: PMID 33093660, Su 2020 Cell Res.
- Full-length ICL3 with T4L chimera.
- Kept.

### AGTR1 — 4ZUD (olmesartan, OLM, 2.80 Å)
- RCSB: https://www.rcsb.org/structure/4ZUD
- Ligand class: **inverse agonist** — record explicitly states "crystal
  structure of the human AT1R in complex with an inverse agonist
  olmesartan (Benicar™)".
- Primary lit: PMID 26420482, Zhang 2015 JBC.
- BRIL chimera at ICL3.
- Kept.

### APJ — `pdb_id=NA` — no clean orthosteric antagonist crystal exists
- RCSB verification of `refs/reference_set.csv`'s 8S4D pick returned
  ligand CMF-019 classified as **G-protein-biased agonist**, not
  antagonist: "Crystal structure of a peptidergic GPCR in complex with a
  small synthetic G protein-biased agonist" (RCSB record for 8S4D, PMID
  39730334).
- Other candidate APJ inactive-side crystals in the PDB (5VBL, 6KNM) are
  also agonist- or partial-agonist-bound.
- **Precedent:** GLP1R 5VEW drop, Block C Step 1.5 — same pattern
  (reference_set pick is agonist/PAM, not antagonist).
- Downstream: `ligand_rmsd_to_ref` NaN on antagonist ligand state; append
  to `refs/reference_set_named_exclusions.md` at merge time.
- **FLAG for coordinator:** `refs/reference_set.csv` currently lists
  8S4D as `inactive-antagonist`. Recommend reclassification or leaving
  the row and noting the RCSB classification mismatch.

### B1B1U5 — 6I9K (9-cis-retinal, RET, 2.15 Å)
- RCSB: https://www.rcsb.org/structure/6I9K
- Ligand class: **inverse agonist** — record: "protein bound to the
  inverse agonist 9-cis retinal".
- Species: **non-human** — jumping spider *Hasarius adansoni*
  (`species=9arac`, `uniprot_slug=b1b1u5_9arac`). Retained per panel of
  record (`refs/gpcr_coupling.csv` class_a_original, PREREG).
- Bistable rhodopsin — 9-cis-retinal covalent inverse agonist analogous
  to 11-cis-retinal in vertebrate opsins (OPSD/1U19).
- Primary lit: PMID 31249143, Varma 2019 PNAS.
- Kept, flagged in `curation_note` as `species=non_human_9arac;
  retained_per_panel_of_record_pre_reg`.

### CCKAR — 7F8Y (devazepide, 1OZ, 2.50 Å)
- RCSB: https://www.rcsb.org/structure/7F8Y
- Ligand class: **neutral antagonist** — "small-molecule antagonist".
- Primary lit: PMID 34556863, Ding 2022 Nat Chem Biol.
- T4L fusion.
- Kept.

### CXCR2 — `pdb_id=NA` — 6LFL is intracellular allosteric antagonist
- RCSB verification of `refs/reference_set.csv`'s 6LFL pick returned
  ligand EBX classified as "allosteric antagonist" bound at the
  **intracellular** allosteric site, outside the extracellular chemokine
  orthosteric pocket: "Crystal structure of CXCR2 bound to a designed
  allosteric antagonist" (RCSB record for 6LFL, PMID 32610344).
- **Precedent:** GLP1R 5VEW drop, Block C Step 1.5 — the NAM ligand
  binds "outside the orthosteric peptide pocket", exact same pattern
  here. Using 6LFL as an antagonist reference for `ligand_rmsd_to_ref`
  would poison the metric if the Tier 4 antagonist panel targets
  orthosteric chemokine-mimetic ligands.
- **Coordinator override path:** if the Tier 4 panel intentionally
  targets intracellular allosteric small molecules (CXCR2 has no
  small-molecule orthosteric antagonist crystal; all published CXCR2
  small-mol antagonists bind the intracellular pocket), 6LFL would be
  the correct reference. Flagged in the row's `curation_note` under
  `alt_use_case`.
- Downstream default: `ligand_rmsd_to_ref` NaN on antagonist ligand
  state; append to `refs/reference_set_named_exclusions.md` at merge time.

### CXCR4 — 3ODU (IT1t, ITD, 2.50 Å)
- RCSB: https://www.rcsb.org/structure/3ODU
- Ligand class: **neutral antagonist** — "small molecule antagonist IT1t".
- Primary lit: PMID 20929726, Wu 2010 Science.
- T4L fusion, full-length ICL3.
- Kept.

### EDNRA — 8XVK (ambrisentan, A1D5J, 3.21 Å)
- RCSB: https://www.rcsb.org/structure/8XVK
- Ligand class: **neutral antagonist** — ambrisentan is the therapeutic
  ETA-selective antagonist. Record: "molecular mechanisms of antagonist
  selectivity".
- Primary lit: PMID 39075075, Nat Rev Drug Discov 2024.
- Deposited 2024-01-15 — post-AF3 cutoff 2021-09-30, likely post-Boltz1
  and Chai training-data cutoffs (verify before Tier 4 dispatch if
  prospectivity claim is downstream-critical). `prospective_candidate=true`.
- Endoglucanase-H / BRIL fusion, anti-BRIL Fab + nanobody stabilised.
- Kept, flagged for training-cutoff verification.

### EDNRB — 5X93 (K-8794 bosentan-analog, K87, 2.20 Å) — REPLACED reference_set.csv pick 6IGK
- RCSB verification of `refs/reference_set.csv`'s 6IGK pick returned
  ligand **endothelin-3** (an agonist peptide, not an antagonist).
  RCSB record for 6IGK: "The structure of the endothelin-3-bound
  receptor reveals..." — this is an agonist-bound crystal, not
  antagonist-bound.
- Substituted with 5X93 (K-8794, a bosentan-scaffold antagonist).
  RCSB record: "bosentan sterically prevents the inward movement of
  transmembrane helix 6 (TM6), and thus exerts its antagonistic activity."
- Primary lit: PMID 28805809, Shihoya 2017 Nat Struct Mol Biol.
- **FLAG for coordinator:** `refs/reference_set.csv` currently lists
  6IGK as `inactive-antagonist`. Recommend swap to 5X93 at merge time.

### FSHR — `pdb_id=NA` — no clean orthosteric antagonist crystal + poor resolution
- RCSB verification of `refs/reference_set.csv`'s 8I2H pick returned:
  - Resolution **6.00 Å** — over the 3.5 Å cutoff for `pocket_ca_rmsd`.
  - Bound to **FSH hormone** (agonist) plus **compound-21f** classified
    as a **PAM** (positive allosteric modulator) that DIRECTLY ACTIVATES
    the receptor: "Compound 21f formed extensive interactions with the
    TMD to directly activate FSHR" (RCSB record for 8I2H, PMID 36720854).
- Both classification (activator, not antagonist) and resolution fail
  the antagonist-reference criteria. No clean orthosteric antagonist
  crystal exists for FSHR in the PDB as of this fetch.
- **Precedent:** GLP1R 5VEW drop.
- Downstream: `ligand_rmsd_to_ref` NaN on antagonist ligand state;
  append to `refs/reference_set_named_exclusions.md` at merge time.
- **FLAG for coordinator:** `refs/reference_set.csv`'s 8I2H
  `inactive-antagonist` row is misclassified; recommend reclassification.

### GHSR — 7F83 (PF-05190457, 1KQ, 2.94 Å)
- RCSB: https://www.rcsb.org/structure/7F83
- Ligand class: **inverse agonist** — "bound to the inverse agonist
  PF-05190457".
- Primary lit: PMID 35027551, Liu 2022 Nat Commun.
- Deposited 2021-07-01 (before AF3 cutoff 2021-09-30) but released
  2022-01-19 (after). Flagged for training-cutoff verification.
  `prospective_candidate=true`.
- BRIL fusion.
- Kept.

### GRPR — 7W41 (PD176252, 8B8, 2.95 Å)
- RCSB: https://www.rcsb.org/structure/7W41
- Ligand class: **neutral antagonist** — "inactive state crystal
  structure of human GRPR in complex with the non-peptide antagonist
  PD176252".
- Primary lit: PMID 36724251, Liu 2023 PNAS.
- Deposited 2021-11-26 — post-AF3 cutoff. `prospective_candidate=true`.
- Kept.

### HRH3 — 7F61 (PF-03654746, 1IB, 2.60 Å)
- RCSB: https://www.rcsb.org/structure/7F61
- Ligand class: **neutral antagonist** — "reveals binding modes of the
  antagonist and allosteric cholesterol". Allosteric cholesterol also
  in structure but primary antagonist PF-03654746 is orthosteric.
- Primary lit: PMID 36243875, Peng 2022 Nat Commun.
- Deposited 2021-06-23, released 2022 — near AF3 cutoff. Flagged.
- BRIL fusion.
- Kept.

### LPAR1 — 4Z36 (ONO-3080573, ON3, 2.90 Å)
- RCSB: https://www.rcsb.org/structure/4Z36
- Ligand class: **neutral antagonist** — record: "LPA1 antagonist
  ONO-3080573 binds to enable ligand access from the extracellular space".
- Note: ligand CCD is ON3, ligand name ONO-3080573 (not ONO-9910539 as
  my planning-stage guess; corrected).
- Primary lit: PMID 26091040, Chrencik 2015 Cell.
- BRIL fusion.
- Kept.

### LSHR — `pdb_id=NA` — 7FIJ is PAM allosteric agonist + hormone
- RCSB verification of `refs/reference_set.csv`'s 7FIJ pick returned:
  - Bound to **chorionic gonadotropin (CG)** — the natural hormone
    (agonist), not an antagonist.
  - Bound to **Org43553** classified as **PAM allosteric agonist**:
    "Org43553 binds to a pocket of the transmembrane domain and interacts
    directly with P10, which further stabilizes the active conformation"
    (RCSB record for 7FIJ, PMID 34552239).
  - Resolution 3.80 Å — over the 3.5 Å cutoff.
- No clean orthosteric antagonist crystal exists for LSHR in the PDB.
- **Precedent:** GLP1R 5VEW drop.
- Downstream: `ligand_rmsd_to_ref` NaN on antagonist ligand state;
  append to `refs/reference_set_named_exclusions.md` at merge time.
- **FLAG for coordinator:** `refs/reference_set.csv`'s 7FIJ
  `inactive-antagonist` row is misclassified; recommend reclassification.

### LT4R1 — 7K15 (MK-D-046, VRJ, 2.88 Å)
- RCSB: https://www.rcsb.org/structure/7K15
- Ligand class: **selective antagonist**.
- Primary lit: PMID 34016973, Michaelian 2021 Nat Commun.
- Full-length ICL3.
- Kept.

### MCHR1 — 8YNS (SNAP-94847, A1D6T, 3.33 Å)
- RCSB: https://www.rcsb.org/structure/8YNS
- Ligand class: **neutral antagonist** — "antagonism of melanin-concentrating
  hormone receptor MCHR1".
- Primary lit: PMID 39616153, Cell Discov 2024.
- Deposited 2024-03-11 — post-AF3 cutoff. `prospective_candidate=true`.
- BRIL fusion with anti-BRIL Fab 1B3 + glue molecule 4-9.
- Kept, flagged for training-cutoff verification.

### NPY2R — 7DDZ (JNJ-31020028, H46, 2.80 Å)
- RCSB: https://www.rcsb.org/structure/7DDZ
- Ligand class: **selective antagonist**.
- Primary lit: PMID 33531491, Tang 2021 Nat Commun.
- T4L fusion, full-length ICL3.
- Kept.

### OPRX — 5DHH (SB-612111, DGW, 3.00 Å)
- RCSB: https://www.rcsb.org/structure/5DHH
- Ligand class: **neutral antagonist**.
- Primary lit: PMID 26526853, Miller 2015 Structure.
- BRIL fusion, full-length ICL3.
- Kept.

### OPSD — 1U19 (11-cis-retinal, RET, 2.20 Å) — REPLACED reference_set.csv pick 7ZBC
- RCSB verification of `refs/reference_set.csv`'s 7ZBC pick returned
  ligand **all-trans-retinal** at **1 picosecond post-photoactivation**
  — this is a transient activation intermediate on the isomerization
  trajectory, NOT the dark-state inverse-agonist reference:
  "the distorted retinal at a 1-ps time delay after photoactivation has
  pulled away from half of its numerous interactions" (RCSB record for
  7ZBC, PMID 36949205).
- Substituted with 1U19 (canonical bovine rhodopsin dark state,
  11-cis-retinal covalent Schiff base at K7.43 — the classical
  inverse-agonist reference).
- RCSB record for 1U19: "configuration about the C6-C7 single bond of
  the 11-cis-retinal Schiff base".
- Primary lit: PMID 15327956, Okada 2004 JMB.
- **FLAG for coordinator:** `refs/reference_set.csv` currently lists
  7ZBC as `inactive-inverse-agonist`. Recommend swap to 1U19 at merge
  time — a photoactivation intermediate is not a valid dark-state
  reference for `ligand_rmsd_to_ref`.

### 5HT1B — `pdb_id=NA` — per exclusions.md, ergotamine partial agonist
- Already documented in `refs/reference_set_named_exclusions.md`
  (Block C Step 3.3 option c). Every 5HT1B inactive-side crystal (4IAR,
  4IAQ, 5V54, 6G79, 7C61) is bound to ergotamine or a related ergot
  alkaloid — all partial agonists at 5HT1B, not neutral antagonists.
- RCSB verification of 4IAR confirmed classification: "ergotamine as an
  agonist antimigraine medication" (RCSB record for 4IAR, PMID 23519210).
- Mirrored here for panel-coverage completeness.

## Cross-cutting flags for coordinator at merge time

**`refs/reference_set.csv` rows that RCSB verification disqualified as
antagonist references.** These are worth reviewing when this sidecar merges:

| Receptor | Current reference_set.csv | Reason | Sidecar action |
|---|---|---|---|
| ACM1 | 6ZFZ `inactive-antagonist` (HTL9936) | HTL9936 is partial agonist per RCSB | Replaced with 5CXV (tiotropium inverse-ag) |
| APJ | 8S4D `inactive-antagonist` (CMF-019) | CMF-019 is G-protein-biased AGONIST | `pdb_id=NA` (no clean alternative) |
| CXCR2 | 6LFL `inactive-antagonist` (EBX) | EBX is intracellular allosteric antag; poisons orthosteric metric | `pdb_id=NA` (coordinator can override for allosteric panel) |
| EDNRB | 6IGK `inactive-antagonist` | 6IGK is endothelin-3 AGONIST-bound | Replaced with 5X93 (K-8794 antag) |
| FSHR | 8I2H `inactive-antagonist` | 8I2H is PAM+FSH at 6.00 Å | `pdb_id=NA` (no clean alternative) |
| LSHR | 7FIJ `inactive-antagonist` | 7FIJ is CG+Org43553 PAM allosteric agonist | `pdb_id=NA` (no clean alternative) |
| OPSD | 7ZBC `inactive-inverse-agonist` | 7ZBC is all-trans-retinal at 1 ps post-photoactivation (intermediate) | Replaced with 1U19 (11-cis dark state) |

**Prospective-candidate rows (post-AF3 training cutoff 2021-09-30):**
5HT5A (7UM4), EDNRA (8XVK), GRPR (7W41), MCHR1 (8YNS). GHSR (7F83) and
HRH3 (7F61) are near-cutoff (deposited before, released after) — verify
Boltz1/Chai/Protenix cutoffs at Tier 4 dispatch if prospectivity claim is
downstream-critical.

**Non-human species:** B1B1U5 (jumping spider *Hasarius adansoni*,
`species=9arac`). Retained per panel of record. Flag for stratification
in downstream analysis if species-effect suspected.

## Downstream instructions

1. Sidecar is **not merged** into `refs/reference_set.csv`. Coordinator
   review required before merge.
2. Merge action per row (see `curation_note` field `merge_disposition`):
   - `pending` — new `role_specific` row to promote or replace in
     `refs/reference_set.csv`.
   - `already_merged_into_reference_set` — Cat A row, already landed by
     Tier 1 sidecar merge; mirrored here for Tier 4 sidecar completeness.
   - `append_to_reference_set_named_exclusions.md` — 4 new NA cases
     (APJ, CXCR2, FSHR, LSHR).
   - `already_documented_in_exclusions.md` — 5HT1B, no action needed.
3. RMSD-driver populates `d_*_ref`, `a100_*`, `angle_class_b_kink_ref`,
   `provenance_sha256` at merge time (matches Tier 1 discipline).
4. `refs/reference_set_named_exclusions.md` should be updated at merge
   time with the 4 new NA cases (APJ, CXCR2, FSHR, LSHR).

## Provenance

- Sidecar author: Tier 3 Stage 2 subagent, 2026-09-04.
- RCSB fetches: 23 `https://www.rcsb.org/structure/<PDB>` records
  retrieved via WebFetch, one supporting sentence quoted in each row's
  `curation_note`.
- Anchor positions carried forward from `refs/reference_set.csv`
  (verified against reference_set values before write).
- Panel of record: `refs/tier3_panel.csv` (40 rows, verified as of
  2026-09-04).
- Tier 1 sidecar: `refs/pending_curation_block_c.csv` (21 rows, of
  which 18 mirror into this Tier 3 sidecar covering 16 panel receptors).
