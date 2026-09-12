# MAP_NEW_CAMPAIGN.md — what the redo actually runs

> **GENERATED — do not hand-edit.** `python3 redo/build/map_new_campaign.py`
> rebuilds it from `redo/inputs/`. Every count below is derived from the frozen
> tables, never transcribed, because a count asserted in a header has drifted
> from its own body four times on this project.

Companion to `redo/protocol/MAP_FROZEN_CAMPAIGN.md`, which maps the campaign this
one supersedes. **The manuscript is frozen as the record; nothing here is built on it.**

---

## 0. Scope

**Class A only** — `DECISIONS.md` D-2026-09-12-d, decided on measured grounds:
F-13 found a 9 Å inter-backbone disagreement on Class B apo and no discriminating
power at all on Class F. Guarded by `g0_preflight.py` check **G0-13**.

- panel receptor classes present: **A** (64 receptors)
- calibration structure classes present: **Class A (Rhodopsin)** (1357 rows)

Dropped with the scope: `E0.5`, `G15`/tier `E-B1`, tier `E-scope`.
**Parked, not killed:** `E7.2`, the class B length ladder.

---

## 1. Receptors — the panel

**64 receptors in 32 paralog clusters.** **32** are the provisional core-32, one per cluster; the rest carry the
wide-replication arm. **The statistical unit is the cluster, not the receptor.**

`active_pdb` / `inactive_pdb` are the Rule-P reference pair, with resolution in Å.
`cognate` is the Gα family read off the Rule-R active structure, and `evidence` is
how firmly — see §2. Ligands are §4, partners §3.

| # | slug | UniProt | cluster | core32 | active | Å | inactive | Å | cognate | evidence |
|---:|---|---|---|:-:|---|---:|---|---:|---|---|
| 1 | **5HT1B** | P28222 | `001_001_001` | · | 6G79 | 3.78 | 5V54 | 3.9 | Gi/o | STRUCTURE_NEAR |
| 2 | **5HT2A** | P28223 | `001_001_001` | ● | 8UWL | 2.8 | 7WC7 | 2.6 | Gq/11;Gs | CHIMERA_SPLIT |
| 3 | **5HT2C** | P28335 | `001_001_001` | · | 8DPF | 2.84 | 6BQH | 2.7 | Gq/11;Gs | CHIMERA_SPLIT |
| 4 | **5HT5A** | P47898 | `001_001_001` | · | 7X5H | 3.1 | 7UM4 | 2.8 | Gi/o | STRUCTURE_EXACT |
| 5 | **AA1R** | P30542 | `001_006_001` | ● | 7LD3 | 3.2 | 5UEN | 3.2 | Gi/o | STRUCTURE_EXACT |
| 6 | **AA2AR** | P29274 | `001_006_001` | · | 8WDT | 3.34 | 6S0L | 2.65 | Gs | CONVENTION_FALLBACK |
| 7 | **ACM1** | P11229 | `001_001_002` | · | 6OIJ | 3.3 | 6WJC | 2.55 | Gq/11 | STRUCTURE_EXACT |
| 8 | **ACM2** | P08172 | `001_001_002` | · | 7T94 | 3.16 | 5ZK8 | 3.0 | Gi/o | STRUCTURE_EXACT |
| 9 | **ACM4** | P08173 | `001_001_002` | ● | 7TRP | 2.4 | 5DSG | 2.6 | Gi/o | STRUCTURE_EXACT |
| 10 | **ADA1A** | P35348 | `001_001_003` | · | 7YM8 | 2.92 | 8HN1 | 2.9 | Gq/11;Gs | CHIMERA_SPLIT |
| 11 | **ADA2A** | P08913 | `001_001_003` | · | 7EJ8 | 3.0 | 6KUX | 2.7 | Gi/o | STRUCTURE_EXACT |
| 12 | **ADRB1** | P08588 | `001_001_003` | ● | 7BU7 | 2.6 | 7BVQ | 2.5 | Gs | CONVENTION_FALLBACK |
| 13 | **ADRB2** | P07550 | `001_001_003` | · | 8GG0 | 2.9 | 2R4R | 3.4 | Gs | STRUCTURE_EXACT |
| 14 | **AGTR1** | P30556 | `001_002_001` | ● | 6OS2 | 2.7 | 8TH3 | 3.0 | Gq/11 | CONVENTION_FALLBACK |
| 15 | **APJ** | P35414 | `001_002_002` | ● | 8XZH | 2.6 | 5VBL | 2.6 | Gi/o | STRUCTURE_EXACT |
| 16 | **B1B1U5** | B1B1U5 | `001_009_001_inv` | ● | 9EPP | 4.06 | 6I9K | 2.15 | Gq/11 | STRUCTURE_NEAR |
| 17 | **C5AR1** | P21730 | `001_002_006` | ● | 7Y66 | 2.9 | 6C1R | 2.2 | Gi/o | STRUCTURE_EXACT |
| 18 | **CCKAR** | P32238 | `001_002_005` | ● | 7MBX | 1.95 | 7F8U | 2.8 | Gs | STRUCTURE_EXACT |
| 19 | **CCR2** | P41597 | `001_003_002` | ● | 7XA3 | 2.9 | 6GPX | 2.7 | Gi/o | STRUCTURE_EXACT |
| 20 | **CCR5** | P51681 | `001_003_002` | · | 7O7F | 3.15 | 6MEO | 3.9 | Gi/o | STRUCTURE_EXACT |
| 21 | **CCR6** | P51684 | `001_003_002` | · | 6WWZ | 3.34 | 9D3G | 3.26 | Gi/o | STRUCTURE_NEAR |
| 22 | **CCR8** | P51685 | `001_003_002` | · | 8KFX | 2.96 | 8TLM | 2.9 | Gi/o | STRUCTURE_EXACT |
| 23 | **CNR1** | P21554 | `001_004_005` | · | 8GHV | 2.8 | 9BA0 | 3.13 | Gi/o | STRUCTURE_EXACT |
| 24 | **CNR2** | P34972 | `001_004_005` | ● | 8GUR | 2.84 | 5ZTY | 2.8 | Gi/o | STRUCTURE_EXACT |
| 25 | **CXCR2** | P25025 | `001_003_002` | · | 6LFO | 3.4 | 6LFL | 3.2 | Gi/o | STRUCTURE_EXACT |
| 26 | **CXCR3** | P49682 | `001_003_002` | · | 8HNM | 2.94 | 8K2W | 3.0 | Gi/o | STRUCTURE_EXACT |
| 27 | **CXCR4** | P61073 | `001_003_002` | · | 8U4N | 2.72 | 8U4R | 3.1 | Gi/o | STRUCTURE_EXACT |
| 28 | **DRD2** | P14416 | `001_001_004` | · | 8TZQ | 3.2 | 6CM4 | 2.87 | Gi/o | STRUCTURE_EXACT |
| 29 | **DRD3** | P35462 | `001_001_004` | ● | 8IRT | 2.7 | 3PBL | 2.89 | Gi/o | STRUCTURE_EXACT |
| 30 | **DRD4** | P21917 | `001_001_004` | · | 8IRU | 3.2 | 5WIU | 1.96 | Gi/o | CHIMERA_SPLIT |
| 31 | **EDNRA** | P25101 | `001_002_007` | · | 8HCQ | 3.01 | 8XVK | 3.21 | Gq/11;Gs | CHIMERA_SPLIT |
| 32 | **EDNRB** | P24530 | `001_002_007` | ● | 8IY5 | 2.8 | 5GLI | 2.5 | Gi/o | STRUCTURE_EXACT |
| 33 | **FSHR** | P23945 | `001_003_003` | · | 8I2G | 2.8 | 8I2H | 6.0 | Gs | STRUCTURE_EXACT |
| 34 | **GHSR** | Q92847 | `001_002_010` | ● | 7NA7 | 2.7 | 6KO5 | 3.3 | Gi/o | STRUCTURE_EXACT |
| 35 | **GPR52** | Q9Y2T5 | `001_010_001` | ● | 8HMP | 2.77 | 6LI2 | 2.8 | Gs | STRUCTURE_NEAR |
| 36 | **GPR6** | P46095 | `001_010_001` | · | 8TYW | 3.43 | 8T1V | 2.6 | Gs | STRUCTURE_EXACT |
| 37 | **GRPR** | P30550 | `001_002_003` | ● | 8H0Q | 3.3 | 7W41 | 2.95 | Gq/11;Gs | CHIMERA_SPLIT |
| 38 | **HRH1** | P35367 | `001_001_005` | · | 8YN2 | 2.66 | 8X5Y | 3.0 | Gq/11;Gs | CHIMERA_SPLIT |
| 39 | **HRH2** | P25021 | `001_001_005` | · | 8YN3 | 2.56 | 7UL3 | 3.0 | Gs | STRUCTURE_NEAR |
| 40 | **HRH3** | Q9Y5N1 | `001_001_005` | ● | 8YN5 | 2.7 | 7F61 | 2.6 | Gi/o | STRUCTURE_EXACT |
| 41 | **LPAR1** | Q92633 | `001_004_003` | ● | 7TD0 | 2.83 | 4Z36 | 2.9 | Gi/o | STRUCTURE_EXACT |
| 42 | **LSHR** | P22888 | `001_003_003` | · | 7FII | 4.3 | 7FIJ | 3.8 | Gs | STRUCTURE_NEAR |
| 43 | **LT4R1** | Q15722 | `001_004_002` | ● | 7VKT | 2.9 | 7K15 | 2.88 | Gi/o | STRUCTURE_EXACT |
| 44 | **MCHR1** | Q99705 | `001_002_013` | ● | 8WWK | 2.61 | 8YNS | 3.33 | Gi/o | STRUCTURE_EXACT |
| 45 | **MTR1A** | P48039 | `001_005_001` | ● | 7VGY | 3.1 | 6ME2 | 2.8 | Gi/o | STRUCTURE_EXACT |
| 46 | **MTR1B** | P49286 | `001_005_001` | · | 7VH0 | 3.46 | 6ME6 | 2.8 | Gi/o | STRUCTURE_EXACT |
| 47 | **NK1R** | P25103 | `001_002_029` | ● | 8U26 | 2.5 | 6E59 | 3.4 | Gs | STRUCTURE_NEAR |
| 48 | **NPY1R** | P25929 | `001_002_020` | ● | 7X9A | 3.2 | 5ZBQ | 2.7 | Gi/o | STRUCTURE_EXACT |
| 49 | **NPY2R** | P49146 | `001_002_020` | · | 8K6N | 3.2 | 7DDZ | 2.8 | Gi/o | STRUCTURE_EXACT |
| 50 | **NTR1** | P30989 | `001_002_021` | ● | 8JPF | 3.02 | 7UL2 | 2.4 | Gi/o | CONVENTION_FALLBACK |
| 51 | **OPRD** | P41143 | `001_002_022` | ● | 6PT2 | 2.8 | 4N6H | 1.8 | Gi/o | CONVENTION_FALLBACK |
| 52 | **OPRK** | P41145 | `001_002_022` | · | 8FEG | 2.54 | 6VI4 | 3.3 | Gi/o | STRUCTURE_EXACT |
| 53 | **OPRM** | P42866 | `001_002_022` | · | 5C1M | 2.07 | 7UL4 | 2.8 | Gi/o | CONVENTION_FALLBACK |
| 54 | **OPRX** | P41146 | `001_002_022` | · | 8F7X | 3.28 | 5DHH | 3.0 | Gi/o | STRUCTURE_EXACT |
| 55 | **OPSD** | P02699 | `001_009_001_vert` | ● | 4X1H | 2.29 | 7ZBC | 1.8 | Gi/o | PEPTIDE_ENTITY |
| 56 | **OX2R** | O43614 | `001_002_023` | ● | 7L1V | 3.0 | 7XRR | 2.89 | Gq/11;Gs | CHIMERA_SPLIT |
| 57 | **OXYR** | P30559 | `001_002_032` | ● | 7RYC | 2.9 | 6TPK | 3.2 | Gq/11;Gs | CHIMERA_SPLIT |
| 58 | **PD2R2** | Q9Y5Y4 | `001_004_008` | ● | 8XXV | 2.33 | 7M8W | 2.61 | Gi/o | STRUCTURE_EXACT |
| 59 | **PE2R4** | P35408 | `001_004_008` | · | 8GDB | 3.1 | 5YHL | 4.2 | Gs | STRUCTURE_EXACT |
| 60 | **S1PR1** | P21453 | `001_004_004` | ● | 7TD4 | 2.6 | 3V2Y | 2.8 | Gi/o | STRUCTURE_EXACT |
| 61 | **S1PR5** | Q9H228 | `001_004_004` | · | 7EW1 | 3.4 | 7YXA | 2.2 | Gi/o | STRUCTURE_EXACT |
| 62 | **SSR2** | P30874 | `001_002_028` | ● | 7T10 | 2.5 | 7XN9 | 2.6 | Gi/o | STRUCTURE_EXACT |
| 63 | **TA2R** | P21731 | `001_004_008` | · | 8XJN | 3.06 | 6IIU | 2.5 | Gq/11;Gs | CHIMERA_SPLIT |
| 64 | **TSHR** | P16473 | `001_003_003` | ● | 7UTZ | 2.4 | 7T9M | 3.1 | Gs | STRUCTURE_NEAR |

---

## 2. G proteins — the cognate map

**Read off the structure the receptor was solved with**, so that the partner we
supply and the tip we score against are the same molecule. Two columns, never one:
`cognate_family` is the biology (what we supply), `reference_tip` is the structure
(what we score against). Conflating them was a real error.

| cognate family | receptors |
|---|---:|
| Gi/o | 40 |
| Gs | 12 |
| Gq/11;Gs | 9 |
| Gq/11 | 3 |

| evidence class | receptors | meaning |
|---|---:|---|
| `STRUCTURE_EXACT` | 39 | the Rule-R active structure carries this exact Gα subtype |
| `CHIMERA_SPLIT` | 10 | the reference partner is a cross-family chimera — tip and scaffold disagree |
| `STRUCTURE_NEAR` | 8 | same family, a near subtype |
| `CONVENTION_FALLBACK` | 6 | no Gα in the Rule-R active reference; family assigned by convention |
| `PEPTIDE_ENTITY` | 1 | the partner is a deposited peptide entity, not a subunit |

**10 receptors carry `needs_decision`** — every one is a `CHIMERA_SPLIT`, excluded from the primary panel and carried in the extension tier with G19 as the
matched control: `5HT2A`, `5HT2C`, `ADA1A`, `DRD4`, `EDNRA`, `GRPR`, `HRH1`, `OX2R`, `OXYR`, `TA2R`.

**4 assignments reverse Block B's prior** — `B1B1U5`, `CCKAR`, `EDNRB`, `GHSR` — and **all four are now closed**.
`B1B1U5` by D-H (reference 9EPP); the other three by **F-14**, which found that
in each of them *the family the Rule-R structure reads is the only family with a
native, full-length, non-engineered Ga anywhere in that receptor's active
structures*. Block B's Gq prior exists for all three only as an mGsqi chimera, a
mini-G, or a subunit the depositors themselves label engineered. Evidence in
`inputs/coupling_reversal_evidence.tsv`; guarded by `g1_preflight.py` **B17**.

---

## 3. The length ladder — what a 'partner' is at each rung

This is the manipulation the whole campaign exists to test. The frozen campaign
**never supplied a peptide at all** — every cognate arm there was a complete Gα.

| rung | rule | length |
|---|---|---:|
| `R1_ct11` | last 11 residues | 11 |
| `R2_ct15` | last 15 residues | 15 |
| `R3_ct21` | last 21 residues | 21 |
| `R4_a5helix` | CGN G.H5 (alpha5 helix) | 26 |
| `R5_a5plus` | CGN G.S6 through C terminus (b6-s6h5-a5) | 36 |
| `R7_full` | full canonical subunit | 350, 354, 355, 359, 374, 377, 381, 394 |
| `R6a_da5` | full subunit with CGN G.H5 deleted | 324, 328, 329, 333, 348, 351, 355, 368 |

Built for **16 Gα families**: `G11`, `G12`, `G13`, `G14`, `G15`, `Ggust`, `Gi1`, `Gi2`, `Gi3`, `Go`, `Golf`, `Gq`, `Gs`, `Gt1`, `Gt2`, `Gz`.

### 3.1 The partner construct registry

**782 constructs, 771 held as bytes with a full sha256.** Anything not
held is not dispatchable — `g1_preflight.py` check **B4** refuses to dispatch a
construct whose bytes we do not hold.

| construct class | n | what it is |
|---|---:|---|
| `peptide_control` | 336 | reversed / polyA / scramble / face-scramble / gcn4-window controls per rung |
| `ga_rung` | 261 | the length ladder itself, per Gα family |
| `ala_scan` | 105 | single-alanine walk along ct21 |
| `ref_tip` | 23 | the α5 tip as deposited in each receptor's own active reference |
| `gi_to_gs_scan` | 15 | stepwise Gi→Gs substitution series on ct21 |
| `not_dispatchable` | 11 | declared but not held — cannot be run |
| `uncoupling_mutant` | 8 | F376A / L388A / R380A nulls, peptide and full-length |
| `ga_rung_isoform` | 6 | GoB isoform arm |
| `species_matched_tip` | 5 | the spider Gq tip for B1B1U5 |
| `non_ga_chain` | 5 | non-Gα partners: GCN4 zipper, ubiquitin, KaiB, Gβ1, Gγ2 |
| `minig_deposited` | 3 | deposited mini-G constructs as an anchor |
| `wetlab_matched` | 3 | C379A peptides matching published wet-lab work |
| `boundary_variant` | 1 | the Sunahara D368–L394 27-mer boundary test |

**11 are NOT dispatchable** and are named so the absence is legible: `spidertip_R2c_ct19`, `spidertip_R3_ct21`, `spidertip_R4_a5helix`, `spidertip_R5_a5plus`, `spidertip_R6a_da5`, `spidertip_R7_full`, `random_helix_40mer`, `arrestin_Ctail`, `DAMGO`, `Nb60`, `arrestin_FL`.

---

## 4. Ligands

**Affinity data is NOT required.** Ligand identity is evidenced *structurally* —
the molecule is co-crystallised in an active or inactive receptor — which is a
stronger claim than an assay number. Aditya, 2026-09-12.

**ENACTED** — `ligand_set_redo.tsv` holds **12 picks across 7 receptors**, **9 of them on one of our own reference structures**, plus **0 blocked** receptors each carrying its reason. Gated by `redo/gates/ligands.py`, 5 checks, each proved by planting.

| receptor | role | ligand | CCD | structure | Å | on our reference |
|---|---|---|---|---|---:|:-:|
| **S1PR1** | full_agonist | siponimod | `J8C` | 7TD4 | 2.6 | ● |
| **S1PR1** | neutral_antagonist | W146 | `ML5` | 3V2Y | 2.8 | ● |
| **HRH3** | full_agonist | histamine | `HSM` | 8YN5 | 2.7 | ● |
| **GHSR** | full_agonist | ibutamoren | `1KD` | 7NA8 | 2.7 | · |
| **GHSR** | neutral_antagonist | CHEMBL1956994 | `8QX` | 6KO5 | 3.3 | ● |
| **ADRB1** | full_agonist | CHEMBL1615159 | `P0G` | 7BU7 | 2.6 | ● |
| **ADRB1** | inverse_agonist | Carazolol | `CAU` | 7BVQ | 2.5 | ● |
| **B1B1U5** | full_agonist | 11,20-Ethanoretinal | `A1H6M` | 9EPP | 4.06 | ● |
| **B1B1U5** | inverse_agonist | Retinal (11-cis) | `RET` | 6I9K | 2.15 | ● |
| **OPSD** | full_agonist | Retinal (all-trans) | `RET` | 5DYS | 2.3 | · |
| **OPSD** | inverse_agonist | Retinal (11-cis) | `RET` | 7ZBC | 1.8 | ● |
| **CCKAR** | full_agonist | SR146131 | `IA1` | 7XOV | 3.0 | · |

**Blocked, with the reason in the table itself:**

| receptor | role | why |
|---|---|---|

`ligand_curation_candidates.tsv` holds the **59 candidate rows across 7 receptors** these were chosen from:

| receptor | needs | candidates | status |
|---|---|---:|---|
| **ADRB1** | antagonist | 19 | **BLOCKED** — carazolol is on our reference and human but is an *inverse agonist* (amendment C-1); every true antagonist candidate is turkey |
| **OPSD** | antagonist | 18 | **BLOCKED** — the active reference carries a detergent (BNG), no agonist |
| **S1PR1** | both | 9 | **enacted** — siponimod / W146, both on our own references |
| **HRH3** | agonist | 4 | **enacted** — histamine on our active reference 8YN5 |
| **B1B1U5** | antagonist | 3 | reference settled by D-H; blocker is policy not chemistry — no neutral antagonist exists |
| **CCKAR** | agonist | 3 | **enacted** — SR146131, off-reference and the only small-molecule candidate |
| **GHSR** | both | 3 | **enacted** — ibutamoren / CHEMBL1956994 |

**Curate retinal by ISOMER, never by CCD** (F-11). OPSD and B1B1U5 both involve
retinal, where agonist and antagonist are isomers of one covalent ligand — and
B1B1U5's reference pair carries two *different* CCDs (`A1H6M` at 9EPP, `RET` at
6I9K), so it is **not** blocked by the shared-CCD problem. I reported the candidate
pool's property as the reference pair's; that was wrong and is retracted.

---

## 5. Decoys — rebuilt from scratch, and why

The frozen campaign's decoys were **hand-picked FDA-approved drugs, one per
receptor, hard-coded in a Python dict**, verified against a single Tanimoto < 0.30
gate and *reported against* a ±20% property window that could reject nothing. There
was no candidate pool, no search and no draw. They cannot be reused.

The replacement is specified in `DRULE_CHEMBL_SCOPE.md` and is **not yet built**:

| # | deliverable | what it must do |
|---:|---|---|
| 1 | `redo/build/drule_pool.py` | extraction → `inputs/drule_candidate_pool.tsv`, one row per (receptor, candidate) with every property axis and the provenance of each activity record consulted |
| 2 | `redo/build/drule_select.py` | apply the eight axes + similarity gate; record **which axis rejected each rejection** — a rule that cannot say why it refused is not auditable |
| 3 | `redo/gates/drule.py` | proved by planting a defect: no accepted decoy has measured activity at its receptor or a cluster-mate; the pool is reproducible from the pinned release |
| 4 | a pool report **before** any threshold is fixed | how many clusters yield ≥3 accepted decoys. D-D withdrew the ≥12 figure precisely because it was set before this number existed |

ChEMBL is needed for **presence/absence of activity only** — not for affinity.

**Status: 1 and 3 are built, 2 and 4 are not.** `drule_targets.tsv` resolves
**63 of 64 receptors** to a ChEMBL SINGLE PROTEIN target against
**ChEMBL_37**, covering **31 of 32 clusters**. The one unresolved is **B1B1U5**, which has
no ChEMBL target at all — recorded with an empty target, never dropped.

`drule_pool.py` is written and its rule is **proved on a fixture** (4/4 branches:
active at the receptor, at a cluster-mate only, only elsewhere, and only in a
low-confidence assay). **It refuses to run against the live API** — an unpinned
pull is `paper_af3`'s ColabFold problem in another costume — so it needs a
downloaded release with `--release` and `--sha256` recorded into every row.
**That download is Aditya's decision.** `redo/gates/drule.py` gates what exists,
4 checks each proved by planting, and announces the unbuilt pool on every run.

---

## 6. The arms, and what they cost

**2,039 system rows in 23 arms.** Two budget columns because the
design has two grains: `pooled` shares draws within a cell, `per-cell` does not.

| item | experiment | arm | receptor set | rows | chains | partner MSA | pooled | per-cell |
|---|---|---|---|---:|:-:|---|---:|---:|
| `G1a/G1b` | E1.1 | ladder | CORE32(provisional) | 210 | 1 | n/a | 8,400 | 42,000 |
| `P1` | E1.1 | ladder_pilot | CORE32(provisional) | 210 | 1 | n/a | 2,100 | 2,100 |
| `G1c/G1d` | E1.1 | intermediate_nested | CORE32(provisional) | 90 | 2 | off | 3,600 | 18,000 |
| `P1b` | E1.1 | intermediate_pilot | CORE32(provisional) | 90 | 2 | off | 900 | 900 |
| `G1c-opt` | E1.1 | intermediate_optional | CORE32(provisional) | 30 | 2 | off | 1,200 | 6,000 |
| `G1e` | E1.1 | hd_deletion_companion | CORE32(provisional) | 30 | 2 | off | 1,200 | 6,000 |
| `G1f` | E1.1 | deposited_minig_anchor | CORE32(provisional) | 90 | 2 | off | 900 | 900 |
| `G18a(proposed)` | E1.1 | wetlab_length_series | CORE32(provisional) | 90 | 2 | off | 3,600 | 18,000 |
| `G18b(proposed)` | E1.1 | wetlab_matched_peptides | CORE32_GS(provisional) | 18 | 2 | off | 180 | 180 |
| `G19(proposed)` | E1.1 | reference_matched_tip | REFCHIMERA_CORE32(provisional) | 23 | 2 | off | 920 | 4,600 |
| `G20(extension)` | E1.1 | chimeric_ref_extension | EXT_CHIMERA(provisional) | 30 | 1 | n/a | 1,200 | 1,200 |
| `G2` | E1.1 | wide_replication | C1_REST(provisional) | 72 | 1 | n/a | 2,880 | 2,880 |
| `G3a/G3b` | E1.2 | a5null | CORE32(provisional) | 90 | 2 | off | 3,600 | 18,000 |
| `G3a/G3b` | E1.2 | non_ga_bulk | CORE32(provisional) | 90 | 2 | off | 3,600 | 18,000 |
| `G4a/G4b` | E1.3 | composition_controls | CORE32(provisional) | 300 | 2 | off | 4,680 | 23,760 |
| `G9` | E1.4 | family_swap | CORE32(provisional) | 30 | 2 | off | 6,000 | 6,000 |
| `G12` | E1.6 | gi_gt_single_residue | CORE32(provisional) | 30 | 2 | off | 6,000 | 6,000 |
| `G10` | E1.5 | ala_scan | G10_SCAN(provisional) | 210 | 2 | off | 4,200 | 4,200 |
| `G10b` | E1.5 | gi_to_gs_series | G10_SCAN(provisional) | 150 | 2 | off | 3,000 | 3,000 |
| `G11` | E1.7 | heterotrimer | CORE32(provisional) | 30 | 3 | off | 6,000 | 6,000 |
| `G16(proposed)` | E1.8 | uncoupling_full | CORE32_GS(provisional) | 12 | 2 | off | 2,400 | 2,400 |
| `G16(proposed)` | E1.8+E1.1 | uncoupling_peptide | CORE32_GS(provisional) | 24 | 2 | off | 4,800 | 4,800 |
| `G17(proposed)` | E1.9 | partner_msa_on | CORE32(provisional) | 90 | 2 | ON | 3,600 | 18,000 |
| | | | | **2039** | | | **74,960** | **212,920** |

**No arm in this table carries a ligand** — Group 1 is the partner-length campaign
and runs apo. The ligand arms are Group 2 and are not frozen.

---

## 7. What every prediction row must record

**47 columns**, and the split is the point:

- `new` — 33
- `exists` — 10
- `exists (cell)` — 3
- `derived` — 1

The frozen campaign recorded **nothing about the MSA on any scored row** — not
depth, not source, not pairing, not a hash (F-6) — and **nothing anywhere compared
output to input** (F-9). `partner_msa_depth`, `n_chains`, `partner_seq_sha256` and
`seed` exist here so that `redo/gates/run_receipt.py` can ask whether a delivery is
what was requested. **There, a missing column is a FAILURE, not a skip.**

---

## 8. Frozen, and open

**Frozen** — `g0_preflight.py` 13 blocking checks, `g1_preflight.py` 16, both
proved by planting the defect each catches; `layout.py` 7; `run_receipt.py` 4.

**Open, in dependency order:**

1. **The measurement pass** — the largest outstanding dependency. It must record
   axis values for the **F3-removed** structures too, or that filter stays
   permanently unauditable (F-12). Not started without Aditya's word.
2. **D2's regeneration** — decided at (c): expand onto `cxcr3`, `mtr1a`, `mtr1b`,
   reserve the other 17. Held until the pass is authorised so the population
   freezes once (D-2026-09-12-e).
3. **`MSA_SPEC.md` implementation** — their review found a defect inside the
   mechanism our own spec proposed: OF3 keys the per-chain MSA dict by **chain ID**,
   Protenix by **integer position**, so `{"A": …, "B": ""}` fails silently on
   Protenix into a live full-depth fetch, invisible in every status JSON.
4. ~~Three coupling reversals~~ — **DONE** (F-14). CCKAR = Gs, EDNRB and GHSR
   = Gi/o, on the native-Gα evidence rather than on authority counting.
5. ~~Ligand curation~~ — **DONE** (F-15): 6 picks enacted across 4 receptors.
   Open: whether to reopen amendment C-1 so ADRB1 and B1B1U5 can use an
   inverse agonist. Aditya's call, not curation.
6. **The decoy pool** — the extraction and its gate are built and proved;
   the pool itself waits on a pinned ChEMBL release being downloaded, which
   is a decision with a cost and is Aditya's.

**Decided and not to be re-opened:** D-A (the conjunction, NPxxY calibrated, tilt
inherited and validated — every ground truth for that axis is circular), D-H
(B1B1U5 stays at 9EPP as (c′)), affinity (not needed), scope (Class A only),
D2 (the split, at the zero-cost cut).
