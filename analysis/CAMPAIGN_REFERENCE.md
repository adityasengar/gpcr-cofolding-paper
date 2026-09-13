# CAMPAIGN_REFERENCE.md — every experiment in both campaigns

**GENERATED** by `analysis/campaign_reference.py`. Do not hand-edit; re-run it.
**No number in this document was typed.** Every count is computed from the file named beside it, because every hand-written count on this project has drifted.

---

# PART 1 — THE FROZEN CAMPAIGN (Blocks A–D)

Frozen as the record. No new claim is built on it. **Every block is row-level as of 2026-09-13**, when Block D's three tables landed — before that, Block D's numbers were prose.

| block | rows | receptors | backbones | arms | note |
|---|---:|---:|---|---|---|
| **A — panel-scale apo vs cognate** | 9,490 | 48 | 4 | apo 4,795, cognate 4,695 | partner = one COMPLETE Gα subunit; no peptide of any length |
| **B — the partner ladder** | 32,000 | 40 | 4 | apo 8,000, cognate 8,000, decoy 8,000, shuffled 8,000 | apo / decoy (tail permuted IN PLACE) / shuffled / cognate |
| **C — the ligand arm** | 40,800 | 36 | 4 | Ga-coupled-active 40,800 | EVERY row carries a ligand; 'apo' here means NO PARTNER (F-23) |
| **D1 — deep apo** | 14,000 | 7 | 4 | apo 14,000 | ligand-free AND partner-free; 100 samples/seed |
| **D2 — directed inactive** | 2,370 | 4 | 4 | apo 800, Ga-coupled-active 800, Nb-inactive 400, Nb-active 370 | nanobody vs Gα steering |
| **D3 — MSA depth** | 25,810 | 26 | 4 | apo 25,810 | 5 depths; the frozen campaign's subsampling tier |
| **TOTAL** | **124,470** | | | | |


### A — panel-scale apo vs cognate

`data/block_a/01_rows/block_a_rows.csv` — **9,490 rows**
- **receptors (48):** 5HT1B, 5HT2C, 5HT5A, AA1R, AA2AR, ACM1, ACM2, ACM4, ADA2A, ADRB1, ADRB2, AGTR1, APJ, B1B1U5, CCKAR, CCR5, CNR1, CNR2, CRHR1, CXCR2, CXCR4, DRD2, DRD3, EDNRA, EDNRB, FSHR, FZD4, FZD6, FZD7, GCGR, GHSR, GLP1R, GRPR, HRH1, HRH3, LPAR1, LSHR, LT4R1, MCHR1, NPY1R, NPY2R, OPRD, OPRK, OPRX, OPSD, OX2R, PTH1R, SMO
- **backbones:** boltz 2,365, chai 2,375, of3 2,375, protenix 2,375
- **arms:** apo 4,795, cognate 4,695
- **ligand levels:** none recorded in this table
- partner = one COMPLETE Gα subunit; no peptide of any length

### B — the partner ladder

`data/block_b/01_rows/rows_tidy.csv` — **32,000 rows**
- **receptors (40):** 5HT1B, 5HT2C, 5HT5A, AA1R, AA2AR, ACM1, ACM2, ACM4, ADA2A, ADRB1, ADRB2, AGTR1, APJ, B1B1U5, CCKAR, CCR5, CNR1, CNR2, CXCR2, CXCR4, DRD2, DRD3, EDNRA, EDNRB, FSHR, GHSR, GRPR, HRH1, HRH3, LPAR1, LSHR, LT4R1, MCHR1, NPY1R, NPY2R, OPRD, OPRK, OPRX, OPSD, OX2R
- **backbones:** boltz 8,000, chai 8,000, of3 8,000, protenix 8,000
- **arms:** apo 8,000, cognate 8,000, decoy 8,000, shuffled 8,000
- **ligand levels:** none recorded in this table
- apo / decoy (tail permuted IN PLACE) / shuffled / cognate

### C — the ligand arm

`analysis/block_c/received_2026_09_12/rows.tier3.v2.csv` — **40,800 rows**
- **receptors (36):** 5HT1B, 5HT2C, 5HT5A, AA1R, AA2AR, ACM1, ACM2, ACM4, ADA2A, ADRB1, ADRB2, AGTR1, APJ, CCKAR, CCR5, CNR1, CNR2, CXCR2, CXCR4, DRD2, DRD3, EDNRA, EDNRB, GHSR, GRPR, HRH1, HRH3, LPAR1, LT4R1, MCHR1, NPY1R, NPY2R, OPRD, OPRK, OPRX, OX2R
- **backbones:** boltz 10,200, chai 10,200, of3 10,200, protenix 10,200
- **arms:** Ga-coupled-active 40,800
- **ligand levels:** full_agonist 14,800, decoy_lig 14,400, neutral_antagonist 11,600
- EVERY row carries a ligand; 'apo' here means NO PARTNER (F-23)

### D1 — deep apo

`analysis/block_d/received_2026_09_13/rows.d1_deep_apo.csv` — **14,000 rows**
- **receptors (7):** ADRB2, CNR2, CXCR4, GHSR, LPAR1, NPY1R, OPSD
- **backbones:** boltz 3,500, chai 3,500, of3 3,500, protenix 3,500
- **arms:** apo 14,000
- **ligand levels:** apo_no_ligand 14,000
- ligand-free AND partner-free; 100 samples/seed

### D2 — directed inactive

`analysis/block_d/received_2026_09_13/rows.d2_directed_inactive.csv` — **2,370 rows**
- **receptors (4):** ACM2, ADRB2, AGTR1, OPRK
- **backbones:** boltz 600, chai 600, of3 570, protenix 600
- **arms:** apo 800, Ga-coupled-active 800, Nb-inactive 400, Nb-active 370
- **ligand levels:** apo_no_ligand 2,370
- nanobody vs Gα steering

### D3 — MSA depth

`analysis/block_d/received_2026_09_13/rows.d3_msa_depth.csv` — **25,810 rows**
- **receptors (26):** 5HT1B, 5HT2C, AA2AR, ACM2, ADRB2, AGTR1, APJ, B1B1U5, CCR5, CNR2, CXCR2, CXCR4, DRD2, EDNRB, GHSR, GRPR, HRH1, LPAR1, LT4R1, MCHR1, NPY1R, NPY2R, OPRD, OPRK, OPRX, OPSD
- **backbones:** boltz 6,500, chai 6,410, of3 6,400, protenix 6,500
- **arms:** apo 25,810
- **ligand levels:** apo_no_ligand 25,810
- 5 depths; the frozen campaign's subsampling tier

---

# PART 2 — THE REDO CAMPAIGN

| group | system rows | pooled (n=10) | per-cell (n=50) |
|---|---:|---:|---:|
| Group 1 — the partner ladder | 2,039 | 74,960 | 212,920 |
| Group 2 — the ligand arm | 350 | 8,716 | 39,872 |
| **TOTAL** | **2,389** | **83,676** | **252,792** |

**The grain is undecided and it is a 3.0× swing.** The frozen campaign used n=50. Neither figure includes the MSA arms, which are enumerated in no systems file.


### Group 1 — every arm

| item | arm | rows | receptors | clusters | partner construct(s) | ligand | pooled |
|---|---|---:|---:|---:|---|---|---:|
| `G10` | ala_scan | 210 | 10 | 10 | ct21@ala_pos01, ct21@ala_pos02, ct21@ala_pos03, ct21@ala_pos04 … | none | 4,200 |
| `G10b` | gi_to_gs_series | 150 | 10 | 10 | ct21@gi2gs_sub01, ct21@gi2gs_sub02, ct21@gi2gs_sub03, ct21@gi2gs_sub04 … | none | 3,000 |
| `G11` | heterotrimer | 30 | 30 | 29 | R8_hetero | none | 6,000 |
| `G12` | gi_gt_single_residue | 30 | 30 | 29 | R1_ct11 | none | 6,000 |
| `G16(proposed)` | uncoupling_full | 12 | 6 | 6 | alphas_F376A_L388A_R380A_triple_null, alphas_F376A_L388A_mutant | none | 2,400 |
| `G16(proposed)` | uncoupling_peptide | 24 | 6 | 6 | R3_ct21@F376A+L388A, R3_ct21@F376A+R380A+L388A, R4_a5helix@F376A+L388A, R4_a5helix@F376A+R380A+L388A | none | 4,800 |
| `G17(proposed)` | partner_msa_on | 90 | 30 | 29 | R3_ct21, R5_a5plus, R7_full | none | 3,600 |
| `G18a(proposed)` | wetlab_length_series | 90 | 30 | 29 | R1b_ct13, R2b_ct17, R2c_ct19 | none | 3,600 |
| `G18b(proposed)` | wetlab_matched_peptides | 18 | 6 | 6 | R2b_ct17@C379A, R2c_ct19@C379A, R3_ct21@C379A | none | 180 |
| `G19(proposed)` | reference_matched_tip | 23 | 12 | 11 | reftip_ct11, reftip_ct21 | none | 920 |
| `G1a/G1b` | ladder | 210 | 30 | 29 | R0_apo, R1_ct11, R2_ct15, R3_ct21 … | none | 8,400 |
| `G1c-opt` | intermediate_optional | 30 | 30 | 29 | M3_h3 | none | 1,200 |
| `G1c/G1d` | intermediate_nested | 90 | 30 | 29 | M1_h4s6, M2_h4, M4_he | none | 3,600 |
| `G1e` | hd_deletion_companion | 30 | 30 | 29 | M5_dHD | none | 1,200 |
| `G1f` | deposited_minig_anchor | 90 | 30 | 29 | MG_5g53, MG_6fuf, MG_8f76 | none | 900 |
| `G2` | wide_replication | 72 | 24 | 14 | R0_apo, R3_ct21, R7_full | none | 2,880 |
| `G20(extension)` | chimeric_ref_extension | 30 | 10 | 9 | R0_apo, R3_ct21, R7_full | none | 1,200 |
| `G3a/G3b` | a5null | 90 | 30 | 29 | R6a_da5, R6b_a5perm, R6c_a5polyA | none | 3,600 |
| `G3a/G3b` | non_ga_bulk | 90 | 30 | 29 | KaiB_2QKEE, ct21@gcn4_window, ubiquitin | none | 3,600 |
| `G4a/G4b` | composition_controls | 300 | 30 | 29 | ct21@face_scramble#1/3, ct21@face_scramble#2/3, ct21@face_scramble#3/3, ct21@polyA … | none | 4,680 |
| `G9` | family_swap | 30 | 30 | 29 | R3_ct21 | none | 6,000 |
| `P1` | ladder_pilot | 210 | 30 | 29 | R0_apo, R1_ct11, R2_ct15, R3_ct21 … | none | 2,100 |
| `P1b` | intermediate_pilot | 90 | 30 | 29 | M1_h4s6, M2_h4, M4_he | none | 900 |

### Group 2 — every arm

| item | arm | rows | receptors | clusters | partner construct(s) | ligand | pooled |
|---|---|---:|---:|---:|---|---|---:|
| `G21(proposed)` | efficacy_ladder_inverse_agonist | 6 | 3 | 3 | R0_apo, R3_ct21 | inverse_agonist | 240 |
| `G6-T2` | ligand_x_partner_peptide_tier | 12 | 2 | 2 | R0_apo, R3_ct21 | full_agonist, neutral_antagonist, none | 160 |
| `G6-T3` | ligand_x_partner_mixed_tier | 42 | 7 | 7 | R0_apo, R3_ct21 | full_agonist, inverse_agonist, neutral_antagonist | 1,200 |
| `G6a/G6b` | ligand_x_partner | 96 | 16 | 15 | R0_apo, R3_ct21 | full_agonist, inverse_agonist, neutral_antagonist | 3,840 |
| `G6d` | decoy_third_role | 32 | 16 | 15 | R0_apo, R3_ct21 | decoy_lig | 264 |
| `G6f(option)` | ligand_x_partner_full_subunit | 48 | 16 | 15 | R7_full | full_agonist, inverse_agonist, neutral_antagonist | 1,920 |
| `G6fd(option)` | decoy_third_role_full_subunit | 16 | 16 | 15 | R7_full | decoy_lig | 132 |
| `G6x` | blocked_ligand_identity | 2 | 1 | 1 | R0_apo, R3_ct21 | full_agonist | 0 |
| `P2b` | ligand_x_partner_pilot | 96 | 16 | 15 | R0_apo, R3_ct21 | full_agonist, inverse_agonist, neutral_antagonist | 960 |

---

# PART 3 — WHAT WAS CHOSEN


## Receptors — 64 on the redo panel, 32 paralog clusters

**The statistical unit is the cluster**, so `MDE = 1.218/√k`: k=32 → 0.215.

| slug | uniprot | organism | cluster |
|---|---|---|---|
| 5HT1B | P28222 | Homo sapiens (Human) | 001_001_001 |
| 5HT2A | P28223 | Homo sapiens (Human) | 001_001_001 |
| 5HT2C | P28335 | Homo sapiens (Human) | 001_001_001 |
| 5HT5A | P47898 | Homo sapiens (Human) | 001_001_001 |
| AA1R | P30542 | Homo sapiens (Human) | 001_006_001 |
| AA2AR | P29274 | Homo sapiens (Human) | 001_006_001 |
| ACM1 | P11229 | Homo sapiens (Human) | 001_001_002 |
| ACM2 | P08172 | Homo sapiens (Human) | 001_001_002 |
| ACM4 | P08173 | Homo sapiens (Human) | 001_001_002 |
| ADA1A | P35348 | Homo sapiens (Human) | 001_001_003 |
| ADA2A | P08913 | Homo sapiens (Human) | 001_001_003 |
| ADRB1 | P08588 | Homo sapiens (Human) | 001_001_003 |
| ADRB2 | P07550 | Homo sapiens (Human) | 001_001_003 |
| AGTR1 | P30556 | Homo sapiens (Human) | 001_002_001 |
| APJ | P35414 | Homo sapiens (Human) | 001_002_002 |
| B1B1U5 | B1B1U5 | Hasarius adansoni | 001_009_001_inv |
| C5AR1 | P21730 | Homo sapiens (Human) | 001_002_006 |
| CCKAR | P32238 | Homo sapiens (Human) | 001_002_005 |
| CCR2 | P41597 | Homo sapiens (Human) | 001_003_002 |
| CCR5 | P51681 | Homo sapiens (Human) | 001_003_002 |
| CCR6 | P51684 | Homo sapiens (Human) | 001_003_002 |
| CCR8 | P51685 | Homo sapiens (Human) | 001_003_002 |
| CNR1 | P21554 | Homo sapiens (Human) | 001_004_005 |
| CNR2 | P34972 | Homo sapiens (Human) | 001_004_005 |
| CXCR2 | P25025 | Homo sapiens (Human) | 001_003_002 |
| CXCR3 | P49682 | Homo sapiens (Human) | 001_003_002 |
| CXCR4 | P61073 | Homo sapiens (Human) | 001_003_002 |
| DRD2 | P14416 | Homo sapiens (Human) | 001_001_004 |
| DRD3 | P35462 | Homo sapiens (Human) | 001_001_004 |
| DRD4 | P21917 | Homo sapiens (Human) | 001_001_004 |
| EDNRA | P25101 | Homo sapiens (Human) | 001_002_007 |
| EDNRB | P24530 | Homo sapiens (Human) | 001_002_007 |
| FSHR | P23945 | Homo sapiens (Human) | 001_003_003 |
| GHSR | Q92847 | Homo sapiens (Human) | 001_002_010 |
| GPR52 | Q9Y2T5 | Homo sapiens (Human) | 001_010_001 |
| GPR6 | P46095 | Homo sapiens (Human) | 001_010_001 |
| GRPR | P30550 | Homo sapiens (Human) | 001_002_003 |
| HRH1 | P35367 | Homo sapiens (Human) | 001_001_005 |
| HRH2 | P25021 | Homo sapiens (Human) | 001_001_005 |
| HRH3 | Q9Y5N1 | Homo sapiens (Human) | 001_001_005 |
| LPAR1 | Q92633 | Homo sapiens (Human) | 001_004_003 |
| LSHR | P22888 | Homo sapiens (Human) | 001_003_003 |
| LT4R1 | Q15722 | Homo sapiens (Human) | 001_004_002 |
| MCHR1 | Q99705 | Homo sapiens (Human) | 001_002_013 |
| MTR1A | P48039 | Homo sapiens (Human) | 001_005_001 |
| MTR1B | P49286 | Homo sapiens (Human) | 001_005_001 |
| NK1R | P25103 | Homo sapiens (Human) | 001_002_029 |
| NPY1R | P25929 | Homo sapiens (Human) | 001_002_020 |
| NPY2R | P49146 | Homo sapiens (Human) | 001_002_020 |
| NTR1 | P30989 | Homo sapiens (Human) | 001_002_021 |
| OPRD | P41143 | Homo sapiens (Human) | 001_002_022 |
| OPRK | P41145 | Homo sapiens (Human) | 001_002_022 |
| OPRM | P42866 | Mus musculus (Mouse) | 001_002_022 |
| OPRX | P41146 | Homo sapiens (Human) | 001_002_022 |
| OPSD | P02699 | Bos taurus (Bovine) | 001_009_001_vert |
| OX2R | O43614 | Homo sapiens (Human) | 001_002_023 |
| OXYR | P30559 | Homo sapiens (Human) | 001_002_032 |
| PD2R2 | Q9Y5Y4 | Homo sapiens (Human) | 001_004_008 |
| PE2R4 | P35408 | Homo sapiens (Human) | 001_004_008 |
| S1PR1 | P21453 | Homo sapiens (Human) | 001_004_004 |
| S1PR5 | Q9H228 | Homo sapiens (Human) | 001_004_004 |
| SSR2 | P30874 | Homo sapiens (Human) | 001_002_028 |
| TA2R | P21731 | Homo sapiens (Human) | 001_004_008 |
| TSHR | P16473 | Homo sapiens (Human) | 001_003_003 |

## G-proteins — the ladder rungs

**16 Gα families** across the rungs, in 782 registry rows spanning 13 construct classes.

Construct classes: `peptide_control` 336, `ga_rung` 261, `ala_scan` 105, `ref_tip` 23, `gi_to_gs_scan` 15, `not_dispatchable` 11, `uncoupling_mutant` 8, `ga_rung_isoform` 6, `species_matched_tip` 5, `non_ga_chain` 5, `minig_deposited` 3, `wetlab_matched` 3, `boundary_variant` 1

| rung | length(s) | families | all held? |
|---|---|---:|---|
| `M1_h4s6` | 44, 45, 47, 56 | 16 | yes |
| `M2_h4` | 60, 61, 62, 63, 73 | 16 | yes |
| `M3_h3` | 112, 113, 114, 125, 130 | 16 | yes |
| `M4_he` | 203, 204, 205, 216, 221 | 16 | yes |
| `M5_dHD` | 236, 239, 240, 242, 246, 256, 261, 264, 266, 279 | 16 | yes |
| `R1_ct11` | 11 | 17 | yes |
| `R1b_ct13` | 13 | 16 | yes |
| `R2_ct15` | 15 | 17 | yes |
| `R2b_ct17` | 17 | 16 | yes |
| `R2c_ct19` | 19 | 16 | yes |
| `R3_ct21` | 21 | 17 | yes |
| `R4_a5helix` | 26 | 17 | yes |
| `R5_a5plus` | 36 | 17 | yes |
| `R6a_da5` | 324, 328, 329, 333, 348, 351, 355, 368 | 16 | yes |
| `R6b_a5perm` | 350, 354, 359, 377, 394 | 7 | yes |
| `R6c_a5polyA` | 350, 354, 359, 377, 394 | 7 | yes |
| `R7_full` | 350, 354, 355, 359, 374, 377, 381, 394 | 17 | yes |

## Ligands — tiers

**T1_small_molecule** 38, **T3_mixed** 13, **X_single_sided** 9, **T2_peptide** 4


## Decoys — D-RULE, ChEMBL_37

**33 accepted** over 11 receptors / **11 clusters** (MDE 0.367); **5 receptors decoy-unavailable**: AA1R, AA2AR, B1B1U5, HRH3, LPAR1.

Runs **EXPLORATORY** — the pre-registered bar was ≥12 clusters (`DECISIONS.md` D-2026-09-12-h).
