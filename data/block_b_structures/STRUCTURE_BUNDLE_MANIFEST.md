# block_b_structures — Structure Bundle Manifest

**Baseline**: paper_af3 tag `block_b_final` at `c237120` (origin/main).
**Companion**: `block_b_figure_data.zip` (SHA-256
`cadf3467c6b0841220a2221c15f9778a1f9fce6c1a547303337bdc8f6aa92d38`).
This bundle ships selected coordinate files that accompany the figure-data
zip; it contains 13 CIFs plus ancillary text/CSV files, all under 50 MB.

Retrieval + hashing only. No rescoring. No new predictions. No
re-derivation of any measurement.

**Anchor receptor**: **GHSR** (Class A, ghrelin receptor; native active
reference 7NA7, inactive reference 7F83).
**Chosen backbone**: **boltz** (L2 distance 0.1329 from the GHSR own
4-backbone mean ladder — closest of the four).

---

## §1 — Selection rules (verbatim from `SELECTION_RULES.md`)

# block_b_structures — Selection Rules (written before selection ran)

Reproduces §4 of the dispatch verbatim. Every representative in the bundle is
selected against these rules; anti-pattern to avoid = picking "the clearest-
looking cognate structure" post-hoc.

## §4.1 Anchor receptor selection

Hard exclusions (in order):

1. **E-B-1** all-NaN-NPxxY: EDNRA, EDNRB, GRPR, HRH3.
2. **E-B-2** agonist-only actives: OPRD, CNR1.
3. **E-B-3** AA2AR (five unexplained anomalies).
4. **E-B-4-clean**: non-native active refs — prefer receptors with
   `active_stabilization_source = native` from `reference_set.blockb_pinned.csv`.
   Non-natives kept in the ranking, penalized on tie.

Then rank on:

- **Reference separation** (`reference_separation_pocket_ca.csv`): keep
  receptors NOT in the bottom quartile on any of {pocket-Cα RMSD,
  |Δ_ref NPxxY|, |Δ_ref tilt|}. Bottom quartile = 10 lowest of 40.
  5HT1B (rank 1/40, 0.53 Å pocket-Cα) is disqualified.
- **Typicality**: exclude explicit lists:
    - occupancy-dominated: ACM4, HRH1, MCHR1, CCKAR, 5HT5A
    - sequence-required: AA1R, 5HT2C, LT4R1, NPY1R
    - family-specific-heavy: NPY2R, OX2R, DRD3
- **Cell occupancy**: decoy engaged-but-inactive cell must have n ≥ 10
  rows on the chosen backbone (gates Bundle C).

## §4.2 Backbone selection

Compute the anchor's 4-arm ladder on each backbone from
`ladder_per_receptor.csv`; take the mean across backbones; pick the
backbone whose ladder is CLOSEST (L2) to that mean. If Chai wins,
re-select — Chai is systematically different (C-B-2).

## §4.3 Bundle B (ladder arms) selection rule

Per (receptor, arm, backbone) cell (50 rows): take the row whose
`delta_to_active` is CLOSEST to the cell's median value.
Not min, not best-scoring, not highest pLDDT. Tie → lower seed,
then lower sample index, deterministically.

## §4.4 Bundle C (engagement trio) selection rule

- **C1 cognate, engaged, active** — row whose α5-CT tip → R3.50 Cα
  distance (`d_ga_alpha5_r350_ca`) is CLOSEST to the median of the
  ENGAGED subset for the cognate arm.
- **C2 decoy, engaged-but-inactive** — same rule: median tip depth
  within the engaged subset of the decoy arm, restricted to
  `predicate=False` (engaged but inactive).
- **C3 decoy, not engaged but > 20 interface contacts** — row whose
  `n_interface_contacts_ga_receptor` is CLOSEST to the median of the
  non-engaged-but-contacting subset.

"Engaged" = `d_ga_alpha5_r350_ca < 20 Å`. 20 Å is permissive (4×
cognate median depth, C-B-6); use the 20 Å boolean for SET DEFINITION,
median tip depth for the SELECTION.

## §4.5 Bundle D (per-backbone companion) selection rule

Apply the C2 rule on all 4 backbones for the anchor. If any
backbone's C2 cell has n < 10, ship nothing for that backbone and
record the shortfall.

## §4.6 Fold-integrity guard

Before finalising each selected row, check its (receptor, arm,
backbone) cell's fold-integrity in `interface_fold_integrity.csv`.
If the cell fails TM6 helicity BW 6.30–6.50 pass rate (< 0.8), take
the next-closest-to-median row and record the substitution.

## Tie-breaking (deterministic)

1. Absolute difference from cell median value (smallest wins).
2. Lower `seed_used` (numeric).
3. Lower sample index parsed from `input_path` (numeric).
4. Lower input_sha256 (lexicographic) — final fallback.

## Corpus pins

- `scorer_git_sha = 04243c45bdd2285ca195add098a7f333a0d60476`
- `ref_set_csv_sha256 = 6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`
- tag `block_b_final` at HEAD `c237120`
- pinned reference set = `refs/reference_set.blockb_pinned.csv`

---

## §2 — Anchor-receptor ranked table

The full 40-receptor evaluation. Every column above is derived from
`experiments/019_block_b_partner_selection/analysis/`; the
`n_dei_<backbone>` columns are the per-cell count of decoy rows with
`d_ga_alpha5_r350_ca < 20 Å AND two_instrument_predicate = False`
(the C2 pool).

**Legend**:

- `asrc`: active_stabilization_source from `refs/reference_set.blockb_pinned.csv`.
- `pca_rank`, `np_rank`, `tilt_rank`: rank of this receptor's reference
  separation on pocket-Cα RMSD / |Δ_ref NPxxY-OH| / |Δ_ref TM6 tilt|;
  1 = smallest (hardest separation). Bottom-quartile disqualifier fires
  at rank ≤ 10 on any axis.
- `typicality_flag`: occ / seq / fam per the dispatch's explicit
  exclusion lists.
- `hard_excl`: E-B-1 (all-NaN NPxxY), E-B-2 (agonist-only actives),
  E-B-3 (AA2AR), or `bot(...)` for bottom-quartile.
- `filter_verdict`: SURVIVOR if all four filters pass; excluded otherwise.

Anchor selection audit — full 40-receptor evaluation table

| receptor | asrc | pca_A | pca_rank | np_rank | tilt_rank | typicality_flag | n_dei_boltz | n_dei_chai | n_dei_of3 | n_dei_protenix | hard_excl | filter_verdict |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---|---|
| 5HT1B | mini_G | 0.532 | 1 | 6 | 6 | - | 8 | 26 | 2 | 0 | -; bot(pca:1,np:6,tl:6) | excluded |
| 5HT2C | chimera | 0.908 | 7 | 8 | 14 | seq | 18 | 50 | 25 | 10 | -; bot(pca:7,np:8) | excluded |
| 5HT5A | mini_G | 0.842 | 6 | 9 | 32 | occ | 9 | 0 | 27 | 0 | -; bot(pca:6,np:9) | excluded |
| AA1R | native | 1.252 | 21 | 22 | 17 | seq | 42 | 48 | 33 | 37 | - | excluded |
| AA2AR | mini_G | 1.619 | 34 | 34 | 31 | - | 36 | 5 | 9 | 0 | E-B-3 | excluded |
| ACM1 | ? | 1.315 | 23 | 16 | 11 | - | 44 | 0 | 48 | 0 | - | SURVIVOR |
| ACM2 | native | 1.068 | 13 | 4 | 25 | - | 8 | 0 | 40 | 41 | -; bot(np:4) | excluded |
| ACM4 | native | 1.111 | 18 | 21 | 27 | occ | 0 | 0 | 17 | 2 | - | excluded |
| ADA2A | ? | 1.036 | 11 | 32 | 40 | - | 0 | 0 | 6 | 5 | - | SURVIVOR |
| ADRB1 | ? | 0.920 | 8 | 20 | 34 | - | 0 | 0 | 35 | 10 | -; bot(pca:8) | excluded |
| ADRB2 | nanobody | 1.054 | 12 | 15 | 26 | - | 10 | 0 | 27 | 0 | - | SURVIVOR |
| AGTR1 | nanobody | 1.872 | 39 | 30 | 39 | - | 0 | 0 | 32 | 20 | - | SURVIVOR |
| APJ | native | 0.629 | 2 | 28 | 1 | - | 44 | 40 | 14 | 0 | -; bot(pca:2,tl:1) | excluded |
| B1B1U5 | native | 1.546 | 30 | 10 | 37 | - | 38 | 29 | 0 | 0 | -; bot(np:10) | excluded |
| CCKAR | ? | 1.478 | 28 | 31 | 8 | occ | 0 | 0 | 0 | 0 | -; bot(tl:8) | excluded |
| CCR5 | native | 0.987 | 9 | 39 | 36 | - | 0 | 50 | 0 | 30 | -; bot(pca:9) | excluded |
| CNR1 | agonist_only | 1.555 | 32 | 13 | 29 | - | 1 | 0 | 0 | 0 | E-B-2 | excluded |
| CNR2 | native | 0.780 | 3 | 14 | 13 | - | 35 | 0 | 1 | 0 | -; bot(pca:3) | excluded |
| CXCR2 | native | 1.734 | 37 | 33 | 20 | - | 0 | 0 | 0 | 0 | - | SURVIVOR |
| CXCR4 | native | 1.474 | 27 | 40 | 12 | - | 0 | 0 | 2 | 0 | - | SURVIVOR |
| DRD2 | native | 1.489 | 29 | 37 | 33 | - | 9 | 4 | 17 | 0 | - | SURVIVOR |
| DRD3 | ? | 1.095 | 16 | 36 | 22 | fam | 24 | 0 | 2 | 22 | - | excluded |
| EDNRA | ? | 1.677 | 35 | 5 | 5 | - | 40 | 34 | 9 | 9 | E-B-1; bot(np:5,tl:5) | excluded |
| EDNRB | native | 0.820 | 5 | 2 | 2 | - | 0 | 33 | 10 | 36 | E-B-1; bot(pca:5,np:2,tl:2) | excluded |
| FSHR | mini_G | 0.798 | 4 | 1 | 18 | - | 0 | 0 | 0 | 0 | -; bot(pca:4,np:1) | excluded |
| GHSR | native | 1.710 | 36 | 18 | 19 | - | 12 | 50 | 24 | 30 | - | SURVIVOR |
| GRPR | native | 1.316 | 24 | 26 | 21 | - | 49 | 50 | 47 | 50 | E-B-1 | excluded |
| HRH1 | mini_G | 1.169 | 19 | 12 | 16 | occ | 0 | 1 | 47 | 1 | - | excluded |
| HRH3 | ? | 1.580 | 33 | 25 | 4 | - | 50 | 50 | 37 | 31 | E-B-1; bot(tl:4) | excluded |
| LPAR1 | native | 1.324 | 25 | 24 | 35 | - | 14 | 48 | 25 | 0 | - | SURVIVOR |
| LSHR | mini_G | 1.900 | 40 | 19 | 38 | - | 0 | 0 | 0 | 0 | - | SURVIVOR |
| LT4R1 | native | 1.079 | 14 | 35 | 28 | seq | 48 | 50 | 5 | 27 | - | excluded |
| MCHR1 | native | 1.549 | 31 | 7 | 9 | occ | 1 | 3 | 5 | 0 | -; bot(np:7,tl:9) | excluded |
| NPY1R | native | 1.205 | 20 | 27 | 15 | seq | 9 | 0 | 2 | 27 | - | excluded |
| NPY2R | native | 1.422 | 26 | 11 | 23 | fam | 9 | 6 | 0 | 0 | - | excluded |
| OPRD | agonist_only | 1.082 | 15 | 3 | 3 | - | 27 | 0 | 36 | 0 | E-B-2; bot(np:3,tl:3) | excluded |
| OPRK | native | 1.016 | 10 | 23 | 24 | - | 0 | 0 | 36 | 10 | -; bot(pca:10) | excluded |
| OPRX | native | 1.279 | 22 | 29 | 30 | - | 9 | 5 | 2 | 0 | - | SURVIVOR |
| OPSD | native | 1.849 | 38 | 38 | 7 | - | 0 | 0 | 1 | 0 | -; bot(tl:7) | excluded |
| OX2R | ? | 1.100 | 17 | 17 | 10 | fam | 9 | 2 | 20 | 6 | -; bot(tl:10) | excluded |

**Survivor summary** (11 receptors after hard exclusions + bottom-quartile
+ typicality; not yet cell-occupancy):

| receptor | asrc | pca_A | n_dei on boltz/chai/of3/protenix | all ≥ 10 ? |
|---|---|---:|---|---|
| LSHR | mini_G | 1.900 | 0 / 0 / 0 / 0 | no |
| AGTR1 | nanobody | 1.872 | 0 / 0 / 32 / 20 | no |
| CXCR2 | native | 1.734 | 0 / 0 / 0 / 0 | no |
| **GHSR** | **native** | 1.710 | **12 / 50 / 24 / 30** | **YES** |
| DRD2 | native | 1.489 | 9 / 4 / 17 / 0 | no |
| CXCR4 | native | 1.474 | 0 / 0 / 2 / 0 | no |
| LPAR1 | native | 1.324 | 14 / 48 / 25 / 0 | no |
| ACM1 | ? | 1.315 | 44 / 0 / 48 / 0 | no |
| OPRX | native | 1.279 | 9 / 5 / 2 / 0 | no |
| ADRB2 | nanobody | 1.054 | 10 / 0 / 27 / 0 | no |
| ADA2A | ? | 1.036 | 0 / 0 / 6 / 5 | no |

**Declared anchor**: **GHSR** — the only survivor with n ≥ 10 on all four
backbones for the decoy engaged-but-inactive cell (native asrc, active
7NA7 / inactive 7F83).

**Note on typicality vs panel**: GHSR's 4-backbone mean ladder is
(0.000 / 0.175 / 0.880 / 0.965), vs the frame_36 panel ladder
(0.158 / 0.558 / 0.809 / 0.891). GHSR sits FAR below panel on the
decoy arm (0.175 vs 0.558): decoys rarely activate GHSR. Since GHSR
survived the explicit typicality-exclusion lists (occupancy /
sequence-required / family-specific-heavy) and passes every other
filter, the SELECTION_RULES rule set anoints it as the anchor. This is
a **finding, not a re-pick trigger** — GHSR is a receptor where the
decoy arm's typical outcome is "engaged but not activating", which is
exactly the C2 population the Bundle-C engagement trio is designed to
illustrate. Rule §4 was written before selection ran; every substitution
would be an anti-pattern per §2 of the dispatch.

---

## §3 — Backbone selection

GHSR per-backbone ladders (from `ladder_per_receptor.csv`):

| backbone | apo | decoy | shuffled | cognate | L2 to own mean |
|---|---:|---:|---:|---:|---:|
| boltz | 0.00 | 0.22 | 1.00 | 1.00 | **0.1329** |
| chai | 0.00 | 0.00 | 0.92 | 0.86 | 0.2080 |
| of3 | 0.00 | 0.08 | 0.60 | 1.00 | 0.2977 |
| protenix | 0.00 | 0.40 | 1.00 | 1.00 | 0.2574 |
| mean | 0.000 | 0.175 | 0.880 | 0.965 | — |

**Chosen backbone**: **boltz** (L2 distance 0.1329 to GHSR's own
4-backbone mean — closest). Chai is not the winner, so the C-B-2
re-selection clause does not fire.

---

## §4 — Shipped files with SHA verification

| bundle_slot | file | receptor | arm | backbone | seed_used | sample | input_sha256 | shipped_sha256 | verification_ok |
|---|---|---|---|---|---|---|---|---|---|
| ref | `01_instrument_references/GHSR_active_7NA7.cif` | GHSR | ref_active | — | — | — | `a8426fdb48a3d65426829aa6e45f9f2ee2f28b98bc62bd9961c54332495b6ffe` | `a8426fdb48a3d65426829aa6e45f9f2ee2f28b98bc62bd9961c54332495b6ffe` | YES |
| ref | `01_instrument_references/GHSR_inactive_7F83.cif` | GHSR | ref_inactive | — | — | — | `39a6d490c1a46db34fda84189df4c020dd6f42180fccda8f7edea0066b9112c3` | `39a6d490c1a46db34fda84189df4c020dd6f42180fccda8f7edea0066b9112c3` | YES |
| B | `02_ladder_arms/apo/aa4e77c50f34.cif` | GHSR | apo | boltz | 416378270 | 3 | `aa4e77c50f3465e72c58db09c6f333a3c3d9b18713172a50cd75a41ae384dbe9` | `aa4e77c50f3465e72c58db09c6f333a3c3d9b18713172a50cd75a41ae384dbe9` | YES |
| B | `02_ladder_arms/decoy/86d2a2e19f92.cif` | GHSR | decoy | boltz | 235076600 | 3 | `86d2a2e19f928192d1ecdd231fbb005634c8ed6145d8172ad16e822c840f5ea7` | `86d2a2e19f928192d1ecdd231fbb005634c8ed6145d8172ad16e822c840f5ea7` | YES |
| B | `02_ladder_arms/shuffled/3ad9efb4824a.cif` | GHSR | shuffled | boltz | 90219270 | 2 | `3ad9efb4824a4d37eb366a9ca0e8c3e14a51936db6bf6c4fe78c00b583cc9749` | `3ad9efb4824a4d37eb366a9ca0e8c3e14a51936db6bf6c4fe78c00b583cc9749` | YES |
| B | `02_ladder_arms/cognate/0e2dfb5b8206.cif` | GHSR | cognate | boltz | 567503142 | 1 | `0e2dfb5b820685da5356ed9666f6d37785f3190aada3bc5d635f02598e7933dd` | `0e2dfb5b820685da5356ed9666f6d37785f3190aada3bc5d635f02598e7933dd` | YES |
| C1 | `03_engagement_trio/C1_cognate_engaged_active/979e9aba5913.cif` | GHSR | cognate | boltz | 1256737941 | 2 | `979e9aba5913d46c055470b1fa96552be6aea2fdff5486ee5f5eee270fba149b` | `979e9aba5913d46c055470b1fa96552be6aea2fdff5486ee5f5eee270fba149b` | YES |
| C2 | `03_engagement_trio/C2_decoy_engaged_but_inactive/b899e22eaced.cif` | GHSR | decoy | boltz | 1445040303 | 2 | `b899e22eacedb83be0d5a7091e936021fecdcc8058b6b5bbd019d54b1983a121` | `b899e22eacedb83be0d5a7091e936021fecdcc8058b6b5bbd019d54b1983a121` | YES |
| C3 | `03_engagement_trio/C3_decoy_not_engaged_high_contacts/971637daeaf2.cif` | GHSR | decoy | boltz | 1344705093 | 1 | `971637daeaf257f2b5e0e84056e4c5c38b8bef29cc005e6709078ccfaaf8af63` | `971637daeaf257f2b5e0e84056e4c5c38b8bef29cc005e6709078ccfaaf8af63` | YES |
| D | `04_per_backbone/boltz/C2_b899e22eaced.cif` | GHSR | decoy | boltz | 1445040303 | 2 | `b899e22eacedb83be0d5a7091e936021fecdcc8058b6b5bbd019d54b1983a121` | `b899e22eacedb83be0d5a7091e936021fecdcc8058b6b5bbd019d54b1983a121` | YES |
| D | `04_per_backbone/chai/C2_d0475c3af2b6.cif` | GHSR | decoy | chai | 329663906 | -1 | `d0475c3af2b67dfabb485b8b329ae5392a6a0a5882166dc307dc4d8bfae7af66` | `d0475c3af2b67dfabb485b8b329ae5392a6a0a5882166dc307dc4d8bfae7af66` | YES |
| D | `04_per_backbone/of3/C2_dd9db75b10a7.cif` | GHSR | decoy | of3 | 364381235 | -1 | `dd9db75b10a7169bac3337e15bcfaa8a15845107c7c48220d4a66aa69ebee3d9` | `dd9db75b10a7169bac3337e15bcfaa8a15845107c7c48220d4a66aa69ebee3d9` | YES |
| D | `04_per_backbone/protenix/C2_e9e84c7a1420.cif` | GHSR | decoy | protenix | 1151761242 | -1 | `e9e84c7a1420979e9563b7709e4007360c26750f482462910eec957a49f2b397` | `e9e84c7a1420979e9563b7709e4007360c26750f482462910eec957a49f2b397` | YES |

Total CIF size: 6.89 MB

**All 13 CIFs verified**: shipped SHA-256 matches the source
(`input_sha256` for predictions from `rows.csv`; source-repo hash for
reference PDBs). Total CIF payload 6.89 MB.

Note the Bundle-C `C2_decoy_engaged_but_inactive` and Bundle-D `boltz/C2_*`
slots are the SAME row (input_sha256
`b899e22eacedb83be0d5a7091e936021fecdcc8058b6b5bbd019d54b1983a121`).
The C2 rule applied on the chosen backbone (boltz) is the same as the
Bundle-D boltz application by definition; the file is shipped twice, once
per slot, for a self-describing bundle tree.

---

## §5 — Per-structure measurements (accompanying Bundle-C rows and LADDER_FRAMING)

Numbers below are read verbatim from `rows.csv` for that row and from
`interface_continuous.csv` at the row's (receptor, arm, backbone) cell.
No re-derivation. Full CSV at
`03_engagement_trio/per_structure_metrics.csv`.

### Bundle B (ladder arms, GHSR × boltz, median delta_to_active)

| arm | tip_A (row) | contacts (row) | Δ_active_A | active | engaged | cell_active_frac | cell_tip_median_A |
|---|---:|---:|---:|---|---|---:|---:|
| apo | — | — | −6.048 | False | False | 0.00 | — |
| decoy | 24.741 | 16 | −5.649 | False | False | 0.22 | 20.970 |
| shuffled | 11.131 | 55 | −0.266 | True | True | 1.00 | 11.097 |
| cognate | 12.483 | 74 | −0.232 | True | True | 1.00 | 12.583 |

(apo rows carry no partner chain — tip and contacts are undefined by
construction; delta_to_active is well-defined off receptor-only geometry.)

### Bundle C (engagement trio, GHSR × boltz)

| slot | tip_A | contacts | NPxxY-OH_A | tilt_A | Δ_active_A | active | engaged | note |
|---|---:|---:|---:|---:|---:|---|---|---|
| C1_cognate_engaged_active | 12.582 | 69 | 5.250 | 17.410 | −0.390 | True | True | picked at cell tip median (12.58 Å) among engaged cognate |
| C2_decoy_engaged_but_inactive | 18.730 | 41 | 9.684 | 12.607 | −5.214 | False | True | picked at engaged-inactive tip median (18.81 Å) among 12 rows |
| C3_decoy_not_engaged_high_contacts | 23.025 | 25 | 9.932 | 12.242 | −5.440 | False | False | non-engaged-but-contacting subset (n=17); picked at ncon median 25 |

Corroborating panel-level context (from claim sheet SC-B-3):

- Panel decoy p(engaged) = 0.7037 [0.571, 0.816].
- Panel decoy p(active|engaged) = 0.6647 [0.554, 0.754].
- Engaged-but-inactive floor pooled: 1,699 rows panel-wide; 12 for
  GHSR × decoy × boltz here.

### Bundle D (C2 rule on all 4 backbones)

| backbone | n_C2 | tip median (Å) | picked tip (Å) | seed | sample | shortfall |
|---|---:|---:|---:|---:|---:|---|
| boltz | 12 | 18.811 | 18.730 | 1445040303 | 2 | none |
| chai | 50 | 12.460 | 12.453 | 329663906 | (chai path scheme) | none |
| of3 | 24 | 10.817 | 10.790 | 364381235 | (of3 path scheme) | none |
| protenix | 30 | 12.176 | 12.158 | 1151761242 | (protenix path scheme) | none |

Sample-index parse: chai/of3/protenix output-tree layouts don't expose a
zero-padded four-digit sample index in `input_path` the way boltz does;
selection tie-breaker fell through to `input_sha256` lexicographic — a
deterministic key across all backbones.

Chai's C2 median tip depth (12.46 Å) is smaller than boltz's (18.81 Å)
because Chai's decoy engaged pool is dominated by tightly-docked
partial-MSA-read rows (C-B-2 tell 1) — the median tips down. That's a
per-backbone artefact, not a mislabelled selection.

---

## §6 — Fold-integrity substitutions

None. All 4 (arm × boltz) cells for GHSR pass the panel
TM6-helicity ≥ 0.80 pass-rate check (min cell = boltz shuffled at
0.9865; interface_fold_integrity.csv). No re-picks.

Bundle-D cells (decoy × {chai, of3, protenix}) all pass:
chai 0.971, of3 0.9985, protenix 1.000. No substitutions.

---

## §7 — Cases where the selected representative does not visually match
##      the claim it illustrates (from numbers only)

None flagged. Two observations for the figure agent:

1. **GHSR × boltz × apo has active_frac = 0.00 and median
   delta_to_active = −6.045 Å** — deeply inactive. This is atypical
   vs the panel apo mean (active_frac = 0.158). The bundle's apo
   representative faithfully reflects GHSR's own apo behaviour, but a
   figure caption should say "GHSR apo, boltz backbone" rather than
   "apo, generic" to avoid over-generalisation.

2. **Bundle-C C1's cognate row has active_frac 1.00** — the cognate
   arm on GHSR × boltz is 100% two-instrument-active across 50 rows.
   Any single cognate representative will be near the class centre;
   the median-tip C1 pick (12.58 Å tip) is exactly the cell median,
   which is 4 Å looser than the panel cognate median (12.19 Å per
   SC-B-3). GHSR's cognate cell tips slightly looser than panel — again
   a receptor-specific characteristic, not a selection artefact.

---

## §8 — Corpus pins

- Working repo: `/Users/SENGAAD1/Documents/claude/paper_af3`, tag
  `block_b_final` at `c237120` (origin/main).
- `scorer_git_sha` = `04243c45bdd2285ca195add098a7f333a0d60476` (every
  row in `rows.csv` reads this SHA).
- `ref_set_csv_sha256` = `6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`
  (pinned Block B reference set, recovered from commit `a355977`,
  archived at `refs/reference_set.blockb_pinned.csv`).
- Companion figure-data zip SHA-256 =
  `cadf3467c6b0841220a2221c15f9778a1f9fce6c1a547303337bdc8f6aa92d38`.

## §9 — Notes for the figure agent

- Apply `SUPERPOSITION.md` (TM1–TM5 + TM7 Cα only; TM6 excluded) when
  aligning these CIFs for visualisation. The scorer's own alignment is
  full-7TM by contrast; do not conflate the two.
- The four Bundle-B CIFs are **arm representatives, not exemplars of
  the ladder outcome**. See `02_ladder_arms/LADDER_FRAMING.md`.
- The Bundle-C C2 CIF (decoy, engaged, inactive) is the load-bearing
  visual for the α5-CT-connector claim (SC-B-4 sits on the median PIF-sum
  connector geometry of this population). SC-B-4 panel value: median of
  cell-medians for decoy engaged-but-inactive cells = 15.42 Å (n=47
  cells). The (GHSR × decoy × boltz) cell has pif_sum_ca = 15.998 Å per
  `interface_continuous.csv` — 0.58 Å to the shuffled side of the panel
  median. That's a per-cell context number for the row's cell, not a
  per-row measurement; SC-B-4 is a cell-level claim.
- The Bundle-D chai C2 CIF is the only one where the tip median is
  small (12.46 Å) — the α5-CT slots in close. Read C-B-2 before making
  any per-backbone claim in a figure caption; Chai is systematically
  different on Block B on three independent axes.
