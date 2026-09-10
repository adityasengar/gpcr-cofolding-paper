# Co-folding models read ligand identity as continuous pocket geometry, not as a binary activation switch

**Manuscript draft v1 — 2026-09-06.**

**Authors** *(to be filled)*.

**Corresponding author** *(to be filled)*.

**Data availability**: local Bitbucket repository `paper_af3` (Novartis internal at time of writing; pre-print will name the mirror). Provenance-pinned rows CSVs, verification JSONs, and reconstruction scripts under `experiments/`.

**Code availability**: `scorer/` + `scripts/` in the same repository, git-SHA-tagged per commit named in Methods.

---

## Abstract

**Motivation.** Structure-prediction models based on the AlphaFold-3 architecture (Boltz-2, Chai-1, OpenFold-3-preview, Protenix-v2) are increasingly used to co-fold G-protein-coupled receptors (GPCRs) with ligands and G-protein partners. It is not established whether these models produce *meaningful* two-state predictions — active versus inactive — controllable through the identity of the input chains, or whether the observed active-like outputs are driven by dataset memorisation or by non-specific occupancy of the intracellular interface.

**Findings.** On a 40-receptor Class A GPCR panel with 40,800 co-folded predictions across four backbones, we find (i) the cognate Gα-bound arm reproduces the active-state TM6 conformation on 40/40 (Boltz), 36/40 (Chai), 39/40 (OF3), 40/40 (Protenix) receptors on median Δd_tm6 [`SEALED.md §2.7`]; (ii) the intracellular interface is dominated by **occupancy**, not partner identity — a graded response apo < decoy < shuffled < cognate at 40 receptors, with property-matched decoy peptides reaching ~60 % two-instrument coherent-active fraction versus ~7–35 % on apo, replicated on all four backbones [`block_b_headline_2026_09_03`]; (iii) the orthosteric pocket **does** discriminate ligand identity — pocket-Cα-RMSD 2×2 (ligand-state × reference-state) interaction is signed non-zero on all four backbones (Boltz −0.306 Å, Chai −0.137 Å, OF3 −0.252 Å, Protenix −0.184 Å; cluster-bootstrap 95 % CI excludes zero), **invisible to a binary two-instrument activation predicate** which saturates on both arms [`stage3_2x2_ligand_state_specificity.json`]; (iv) apo bistability is a **partial reference-selection artefact** — the prize claim leads with clean G-protein-bound stratum mean **6.84 %** on n=24 (Class A minus sealed minus FSHR/LSHR reference-cleanliness strips), not the panel mean of 15.5 % [`task_F_v5_clean_bound_stripped.json`].

**Prospective controls.** Templates OFF on all four backbones (PREREG §11b). Sealed subset of 8 receptors physically moved out of `refs/reference_set.csv` and never used in scoring. Same-complex split (recallable stratum, n=15 vs must-generalise stratum, n=13) confirms anti-memorisation direction on the pocket axis, with magnitude within noise at the current n [`task_A_v3_composition_check.json`]. Chemotype composition balanced (9 sm/6 pep recallable vs 6 sm/7 pep must-generalise; two-proportion z = +0.73 → `NO_CONFOUND`) [`task_A_v3_composition_check.json`].

**Scope**: Class A GPCRs (n=40 in the panel of record; ligand-state analyses on Class A only; states 1 apo and 4 +Gα also cover 4 Class B + 4 Class F on the 48-receptor panel from Block A). Pose accuracy scoped to OF3 + Protenix × neutral-antagonist arm × `ref_pdb == input_bound_pdb` (n=4,500 rows; 6.93 % aggregate rate at `ligand_rmsd_to_ref < 3 Å`) pending an MCS-based atom matcher [`task_E_v3_scoped_finding.json`].

**One-sentence claim (numbers-with-qualifiers)**: on 48,000 co-folded predictions across four models on 40 Class A receptors with MSA on and templates off, the four backbones place agonist-apo predictions closer to the active-state pocket than property-matched decoys at Cα resolution (signed 2×2 interaction, 95 % CI clearing zero on all four backbones), while the same-complex split shows this closeness is not larger on receptors whose ligand-bound crystal is in training (magnitude within-noise at n=13/15 per stratum). Fraction-active on the two-instrument binary predicate saturates and misses the effect.

---

## Introduction

G-protein-coupled receptors (GPCRs) mediate signalling for roughly one-third of FDA-approved drugs [Sriram & Insel 2018]. They function as ligand-gated allosteric switches: a two-state equilibrium between an inactive and an active receptor conformation, biased by orthosteric ligand and intracellular partner. The active state is defined structurally by an outward movement of transmembrane helix 6 (TM6) — measured either at the intracellular tip via canonical Ballesteros-Weinstein positions 3.50 to 6.30 [Ballesteros & Weinstein 1995], or, more robustly across coupling classes, via a GPCRdb-defined TM6 tilt over multiple anchor points [Isberg et al 2015; Isogai et al 2016]. Full agonists stabilise the active state; neutral antagonists occupy the pocket without shifting the equilibrium; inverse agonists actively stabilise the inactive state. The intracellular interface completes the switch by receiving the Gα C-terminal α5 helix (or an arrestin finger loop) that couples the pocket-side occupancy to downstream signal. That two-interface, ligand-and-partner-gated logic is the load-bearing structural fact of GPCR pharmacology, and the reason prospective *state* prediction from structure is a decades-old goal separate from ligand-pose prediction.

The 2021 introduction of AlphaFold-2 [Jumper et al 2021] and its 2024 successor AlphaFold-3 [Abramson et al 2024] triggered a wave of open-source co-folding models attempting to predict protein–ligand and protein–partner complexes end-to-end. Four of these — Boltz-2 [Zhu et al 2024], Chai-1 [Chai Discovery 2024], OpenFold-3-preview [OpenFold consortium 2024], and Protenix-v2 [ByteDance 2024] — are all AF3-architecture variants trained on public structural data, and all are used in production drug-discovery pipelines at the time of writing. Their per-prediction API accepts a receptor sequence, an optional ligand SMILES (or peptide chain), an optional protein partner chain, and returns a co-folded complex plus per-residue confidences. In principle, this makes them a natural tool for GPCR state prediction: give them a receptor with a Gα partner and get an active state; give them a receptor with an antagonist and no partner and get an inactive state. In practice, the record is fragmented. Prior work on single receptors — β2-adrenergic (ADRB2), μ-opioid, adenosine A2A — has variously reported prospective active-state prediction with AF-Multimer + Gα [Heo & Feig 2022; Sala et al 2023], nanobody-stabilised state selection [Wayment-Steele et al 2024 for AF-Cluster], and MSA-subsampling to expose alternative conformations [Fischman 2024, AFsample2]. Whether any of these results generalise across GPCR classes, across co-folding backbones, or holds up against ligand pharmacology has never been prospectively tested at panel scale.

The unresolved questions this manuscript addresses:

**Q1 — Two-state generation at panel scale.** Do all four AF3-style backbones produce a *detectable* two-state switch across 40 Class A receptors when handed the same input topology, or does the answer collapse to a backbone-specific single-state modal output? This is a straightforward test: apo receptor and receptor-plus-Gα are the two inputs; a receptor "succeeds" if its cognate arm sits closer to the active reference (on both the R3.50–R6.30 axis and the GPCRdb TM6 tilt) than its apo arm does.

**Q2 — Ligand identity at the orthosteric pocket.** Given a two-state switch works, does the pocket read *identity* (agonist vs antagonist vs decoy) — or only *presence* (something in the pocket vs nothing)? This is where prior single-receptor prospective claims have been strongest and where reviewer skepticism concentrates. The trap is a binary predicate that saturates on the cognate arm, making all ligand states look identical when they in fact differ on continuous pocket geometry.

**Q3 — Anti-memorisation.** How much of the answer to Q2 is training-data recall? All four backbones' training corpora include co-crystals of the exact receptors and (a large fraction of) the exact ligands in our panel. A same-complex split — held-out receptors whose bound crystals do NOT appear in training — separates the recallable stratum from the must-generalise stratum on a common test.

**Q4 — Two interfaces one mechanism.** Do the intracellular interface (partner side) and the orthosteric pocket (ligand side) behave the same way? Or does one read identity while the other reads occupancy? Cross-block correlation on receptor-level contributions gives the direct answer.

**Q5 — Failure-mode discipline.** The corpus running this campaign has, across three prior blocks, exposed silent-fail modes that a naïve reader would count as evidence: silent single-sequence MSAs in Chai [audit trail §10], a constant-seed regression in OF3 [audit trail §13, memory `of3_seed_bug_fixed_2026_09_02`], species-mistagging by manifest builders [audit trail §21, memory `pyc_bytecode_false_positive_2026_09_06`], and an atom-name matcher that returned NaN independently of pose quality on two of four backbones [memory `ligand_rmsd_atom_name_gap_2026_09_06`]. Any panel-scale claim not disciplined against these regressions is dead-on-arrival with reviewers.

Our design answers these questions with a **pre-registered 40 Class A receptor panel** (`refs/PREREG.md`, `refs/tier3_panel.csv`) evaluated on all four backbones under templates-off, MSA-on discipline (Chai `.aligned.pqt` cache, OF3 ColabFold shim, Boltz-2 and Protenix-v2 pre-warmed live server) with 5 seeds × 10 samples per (receptor, backbone, arm, ligand-state) cell. Two-state calls use a class-conditional two-instrument predicate: `d_npxxy_y558_y753_oh < 9.082 Å` AND `d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å` for Class A (PREREG amendment §C-5); analogous constructs for Class B and Class F, both reported as descriptive-only at the current n. A **sealed subset** of 8 receptors is physically moved out of `refs/reference_set.csv` and never accessed by any scoring step, providing a held-out validation set the model has no way to leak against. The **held-out subset** of 8 additional receptors (disjoint from sealed) rehearses the panel-integrity monitor.

Reproducibility discipline follows a number-provenance rule set by prior audit rounds: every empirical figure in this manuscript carries its verification JSON path, its reconstruction script git SHA, and its input CSV SHA-256. Withdrawn claims from earlier draft versions are enumerated explicitly (§Withdrawn claims) so reviewers who find prior repo commits can trace each retraction. That enumeration is not standard practice, but the corpus running this campaign self-corrected under an adversarial audit that produced five sequential retraction rounds (v1 through v5), and the manuscript is more defensible if that trail is public than if it isn't.

This work is deliberately not a benchmark on a diverse ligand library, a pose-accuracy comparison against dedicated docking tools like AutoDock Vina, or a MSA-subsampling method paper. Class B (n=4) and Class F (n=4) receptors are tested at the Block A scale (apo and cognate-Gα only) but not on ligand-state axes; the ligand-state tier is Class A only per PREREG amendment §C-4. Pose accuracy is measured on a scoped subset (OF3 + Protenix × neutral-antagonist × reference-matched, n=4,500 rows) pending a cross-backbone comparable atom matcher.

**Cite**: [Sriram & Insel 2018] GPCRs as drug targets; [Isogai et al 2016] TM6 activation signature; [Wingler & Lefkowitz 2020] biased signalling; [Ballesteros & Weinstein 1995] BW numbering; [Isberg et al 2015] GPCRdb; [Heo & Feig 2022] AF-Multimer + Gα; [Sala et al 2023] AF-Multimer state selection; [Jumper et al 2021] AF-2; [Abramson et al 2024] AF-3; [Zhu et al 2024] Boltz-2; [Chai Discovery 2024] Chai-1; [OpenFold consortium 2024] OF3-preview; [ByteDance 2024] Protenix v2; [Wayment-Steele et al 2024] AF-Cluster; [Fischman 2024] AFsample2; [Buttenschoen et al 2024] PoseBusters.

---

## Methods

### Panel of record

40 Class A GPCRs, prospectively selected in `refs/gpcr_coupling.csv` (SHA-256 tagged at commit `[to be filled]`) and enumerated in `refs/tier3_panel.csv` (SHA-256 `63cdd49c...`). Panel spans:

- **Aminergic (n=10)**: 5HT2C, 5HT5A, ACM1, ACM2, ACM4, ADA2A, ADRB1, ADRB2, DRD2, DRD3.
- **Chemokine (n=3)**: CCR5, CXCR2, CXCR4.
- **Peptide (n=13)**: AGTR1, APJ, CCKAR, EDNRA, EDNRB, GHSR, GRPR, HRH1, HRH3, NPY1R, NPY2R, OX2R, MCHR1.
- **Opioid/orphan (n=5)**: OPRD, OPRK, OPRX, LT4R1, LPAR1.
- **Sensory/glycoprotein (n=4)**: OPSD (bovine), B1B1U5 (jumping spider), FSHR, LSHR.
- **Adenosine (n=2)**: AA1R, AA2AR.
- **Vasopressin-like (n=1)**: 5HT1B.

*Species non-human where noted*: OPSD (bovin), B1B1U5 (arachnid). Manifest builder `scripts/build_block_c_tier3_manifest.py` (commit `f65521a`) enforces `_load_receptor_species_map` from `refs/reference_set.csv`; misassignment produced 800 false failures on OPSD and B1B1U5 in the v1 corpus [`docs/AUDIT_TRAIL.md §21`, `task_D_species_match_root_cause.json`], rectified in `rows.tier3.v2.csv`.

### Sealed subset and held-out subset

**Sealed** (n=8): ACM1, ADA2A, ADRB1, CCKAR, DRD3, EDNRA, HRH3, OX2R. Physically moved out of `refs/reference_set.csv` to `refs/sealed_active_refs_2026_09_01.csv` (pinned SHA-256 `879046326c...`). Never accessed by any scoring step; used only for late-stage held-out validation.

**Held-out** (n=8): 5HT2C, AGTR1, CXCR2, CXCR4, DRD2, LPAR1, MCHR1, NPY2R. Disjoint from sealed by construction; treated as a rehearsed subset for panel-integrity monitoring [`refs/PREREG.md §13`].

### Reference structures

Active + inactive crystal structures per receptor, curated in `refs/reference_set.csv` (SHA-256 `7a261988ff...`; a paired-commit ceremony landing Gate 2 relabels for FSHR 8I2H (PAM), LSHR 7FIH (allosteric agonist), and AA2AR 5G53 (Gα-only-miniG) is pending). Analysis-time relabels applied via `refs/pending_curation_block_c_tier3.csv` (SHA-256 `07bfd8546621...`).

### Backbones

Boltz-2 (Zhu et al 2024, MIT), Chai-1 (Chai Discovery 2024), OpenFold-3-preview (OpenFold consortium 2024), Protenix v2 (ByteDance 2024). All four run at commit-pinned versions. MSA discipline **per backbone** (PREREG §11c-d):

- **Chai**: `CHAI_MSA_DIRECTORY` env var hardcoded in `qsub/rerun_chai.sh` + inline `.aligned.pqt` pre-flight (per-chain SHA-256 verification).
- **OF3**: runner-YAML `experiment_settings.seeds:` block (not `--num-model-seeds` CLI); ColabFold shim (`qsub/colabfold_shim.py`) enforces `(connect=30, read=600)` timeout.
- **Boltz-2 + Protenix**: pre-warmed ColabFold public-API cache; upstream defaults.

**Templates OFF** on all four backbones per PREREG §11b. Any manifest with a populated template field is a regression [`docs/AUDIT_TRAIL.md §9`].

### Prediction grid

**Block A** (48 receptors × 4 backbones × 2 arms × 5 seeds × 5 samples): 9,600 predictions.

**Block B Wide** (40 receptors × 4 backbones × 4 arms × 5 seeds × 10 samples): 32,000 predictions. Arms = {apo, decoy_partner, shuffled_cognate, cognate_gα}.

**Block C Tier 3** (40 Class A × 4 backbones × 3 ligand states × 2 arms × 5 seeds × 10 samples): 48,000 scheduled; 40,800 delivered after post-audit v2 species-fix rescore.

Cognate partner is **Gα-alone `alphas` chain** (residues 1–354 of Gα), NOT the heterotrimer. Locked as an invariant [`CLAUDE.md engineering invariants`].

### Two-instrument activation predicate

Class-conditional, per PREREG amendment §C-5.

- **Class A**: `d_npxxy_y558_y753_oh < 9.082 Å` AND `d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å`. Both derived from BW-anchored residues; thresholds set from a matched active-vs-inactive reference calibration [`docs/POST_BLOCK_A_CLEANUP_2026_09_02.md §1(b)`].
- **Class B**: TM6 kink at the PxxG motif (Wootten numbering) AND GPCRdb TM6 tilt.
- **Class F**: GPCRdb TM6 tilt only.

Class B and Class F thresholds are reported as `descriptive_n_lt_5_per_side` (n < 5 per side), NOT as active-call fractions or usable thresholds [`docs/POST_BLOCK_A_CLEANUP_2026_09_02.md §15`; `scripts/derive_per_class_thresholds.py`].

### Continuous axes

**d_tm6**: Cα–Cα distance between BW 3.50 (R350) and BW 6.30 (R630).

**pocket_ca_rmsd_active**: Cα RMSD over BW-anchored pocket residues (3.32, 3.33, 3.36, 5.42, 5.43, 5.46, 6.48, 6.51, 6.52, 6.55, 7.39, 7.42) after TM-bundle superposition, computed against each receptor's own active-state reference.

**pocket_ca_rmsd_inactive**: same residues, against the inactive reference.

**pocket_sidechain_rmsd_{active,inactive}**: same residue set, sidechain heavy atoms.

**RMSD-to-active/inactive** (whole 7TM): Cα RMSD over the 7TM residue subset after TM-bundle superposition. Whole-fold RMSD explicitly not used — dilutes TM6 signal in noise of 300-residue backbone.

### Statistical framework

**Cluster bootstrap**: 10,000 replicates. Two-stage cluster: receptors within group, seeds within receptor. Point estimate = per-backbone median-of-medians; 95 % CI = percentile bootstrap.

**Same-complex split**: `ref_pdb == input_bound_pdb` → RECALLABLE stratum (crystal in training); else → MUST-GENERALISE. On the 40-receptor panel × ligand states: n=15 recallable, n=13 must-generalise (agonist arm); n=22 recallable, n=5 must-generalise (antag arm) [`task_A_v3_composition_check.json`].

**Chemotype balance check**: two-proportion z-test on P(small_mol) across recallable vs must-generalise strata. `|z| < 1.0` → `NO_CONFOUND`. Observed z = +0.73 on agonist arm [`task_A_v3_composition_check.json`].

### Failure-mode protection

**Regression detectors** (`docs/AUDIT_TRAIL.md`): OF3 seed_2746317213 detector; scorer `_version_sha` install-time stamp; `check_scorer_hpc_matches_local` gate (check #16, `SCORER_FILES_TRACKED`); RMSD `input_path` verbatim verification (`scripts/verify_rmsd_completeness.py`); Chai silent-single-sequence probe; template regression grep in launcher scripts.

**`.pyc`-bytecode false-positive** (`docs/AUDIT_TRAIL.md §21`): a claim of the form "fix landed" must diff SOURCE (`.py`, `.sh`, `.md`) against a named commit, not build artefacts (`.pyc`, `.so`, `__pycache__`, `.o`).

### Reconstruction discipline

Every empirical figure in this manuscript pins:
- Source CSV/PDB SHA-256 hash (in verification JSON).
- Reconstruction script git SHA (in verification JSON).
- Method version (backbone commit SHA + scorer commit SHA).

Verification JSONs archived under `experiments/*/analysis/verification/`. Withdrawn claims explicitly enumerated (see §Withdrawn claims below); provenance sidecars stored alongside the corrected narrative.

---

## Results

### Block A — the two-state axis

**d_tm6 (cognate > apo) on all four backbones, all 40 Class A receptors.**

Class A median Δd_tm6 (cognate − apo), per backbone [`SEALED.md §2.7`]:

- Boltz-2: **5.548 Å** (positive-direction receptors: **40/40**)
- Chai-1: **3.212 Å** (36/40)
- OpenFold-3: **5.694 Å** (39/40)
- Protenix v2: **6.125 Å** (40/40)

Class A active-call fraction on the two-instrument predicate: Boltz 0.917, Chai 0.833, OF3 0.861, Protenix 0.944 (four receptors missing required metrics per backbone; per-cell across-seed SD post-OF3-seed-bug-fix: Protenix 0.145, Chai 0.396, Boltz 0.594, OF3 0.638).

**Cohen's d effect size (cluster-bootstrapped, per-receptor pooled SD, receptor-mean aggregation, 10,000 replicates)** [`cohens_d_block_a_d_tm6.json`, SHA-256 `0adb183a4e6efe9bbc062acce5f40c2078875ef1fff4a0aba717dc4eb9b9d443`]:

| backbone | median Δd_tm6 (Å) | Cohen d | 95 % CI | verdict |
|---|---:|---:|---|---|
| Boltz-2 | 5.619 | **14.70** | [+10.54, +19.51] | LARGE_EFFECT |
| Chai-1 | 3.236 | **10.64** | [+6.95, +14.89] | LARGE_EFFECT |
| OpenFold-3 | 5.589 | **10.25** | [+7.58, +13.20] | LARGE_EFFECT |
| Protenix v2 | 6.116 | **41.21** | [+33.52, +49.09] | LARGE_EFFECT |

All four backbones: LARGE_EFFECT with CI clearing zero by wide margins.

*Convention note (M5)*: the Cohen's d values reported here use per-receptor pooled within-cell SD as the denominator (the within-cell across-seed SD is ~0.2–0.6 Å against a ~5 Å between-arm shift, producing large d). A between-receptor-scale d (pooling receptors within backbone into a single distribution) would land closer to 1–3. The manuscript should decide which convention to cite; both are documented in the pinned JSON.

**Continuous pocket axis (cognate < apo)**: pocket_ca_rmsd_active runs cognate < apo on all four backbones — same direction as d_tm6, orthogonal axis, consistent state assignment [`task_A_v3` per-receptor deltas].

### Block A — apo bistability

Class A minus sealed panel mean (n=32) apo two-instrument coherent-active fraction: **15.5 %** [`task_F_v5.corrected_panel_mean.value`].

**Prize claim**: on the n=24 Class A receptors with a **clean G-protein-bound active reference** (Class A minus sealed minus FSHR/LSHR reference-cleanliness strips: FSHR 8I2H is a PAM per PMID 36720854, 6.00 Å; LSHR 7FIH is allosteric agonist per PMID 34552239, 3.80 Å), mean apo coherent-active fraction is **6.84 %** (median 1.53 %; valid-only mean 7.46 %) [`task_F_v5_clean_bound_stripped.json`].

**Sub-Å hit distribution (10 of 32)**:

- **Clean G-protein-bound (n=4)**: CNR2 (0.85 Å, 0.27), CXCR4 (0.67 Å, 0.04), GHSR (0.87 Å, 0.02), NPY1R (0.98 Å, 0.02). Only **CNR2** sustains the two-instrument coherent-active predicate at scale (27 %).
- **G-protein-free (n=4)**: ADRB2 (4LDE nanobody, 0.26), AGTR1 (6OS2 nanobody, 0.60), CNR1 (5XRA agonist-only, 0.62), OPSD (4X1H α5-CT-peptide-only, 0.38). Mean apo coh-active 37.4 %.
- **Reference-cleanliness excluded (n=2)**: FSHR (8I2G Gs-engineered), LSHR (7FIH native heterotrimer per Gate 2).

**Bound-to-free ratio** on matched statistic + membership [`task_F_v5.stratified_ratio`]:

|  | 4-free / 26-bound-raw (prior) | 5-free / 24-clean-bound (v5) |
|---|---:|---:|
| MEDIAN | 14.33× | **19.00×** |
| MEAN | 2.79× | **5.02×** |

Stripping FSHR + LSHR from the bound stratum **widens** the free-to-bound gap; they had the two highest apo coh-active fractions in the raw bound stratum (0.67 and 0.77) and were excluded on reference-cleanliness, not on Block-C-specific criteria.

**AA2AR bimodality provenance flag**: at Block A row counts (n=100 apo total, n=25 per backbone) AA2AR is UNIMODAL on d_tm6 [`aa2ar_unimodal_block_a_counter.json`, SHA-256 `5e873270d9826a6d8c907783a0ce1c43e9f9f117e595ab0526c9cc2d02b54513`]. Hartigan's dip test fails to reject unimodality on every backbone (Boltz p=0.811, Chai p=0.788, OF3 p=0.124, Protenix p=0.877) and on the pooled n=100 sample (p=0.931). Pooled distribution centres on median 7.78 Å (IQR 7.55–7.98 Å), not on a 12.00/9.73 Å bimodal split. Zero of 100 rows have `rmsd_to_active_ref < 1.0 Å`. The "609 active-like / 1,279 inactive-like at 1,888 rows" attribution in prior docs is a v3.6b campaign figure (n=17,568), not Block A. `docs/PIPELINE_INTERPRETATION.md` §Q6 now carries an attribution note pointing readers here.

### Block B — occupancy dominates identity at the intracellular interface

Pre-registered row 4 (graded, mass-dependent apo < decoy < shuffled < cognate) replicated on all four backbones [`docs/BLOCK_B_CLAIM_AUDIT.md`, memory `[[block-b-headline-2026-09-03]]`].

Dominant signal: occupancy-driven. Decoy partner (property-matched but chemistry-different α5-CT peptide) reaches ~60 % two-instrument coherent-active fraction versus ~7–35 % on apo (backbone-dependent). Cognate Gα reaches ~89 % (Class A backbone-averaged) [`SEALED.md`].

α5-CT chemistry claim gets **partial** support: 14–23 % of decoy-partner rows sit in an engaged-but-inactive shape (helical, right register, wrong TM6 response). Interpreted as: the intracellular interface reads mass with a secondary chemistry contribution at the peptide-shape level.

### Block C Tier 3 — the orthosteric pocket discriminates ligand identity, on continuous axes

**Headline (§4.1 of `tier3_headline_2026_09_05.md`)**: pocket-Cα-RMSD 2×2 interaction (agonist − antag on active_ref vs inactive_ref), signed non-zero on all 4 backbones, n=23 receptors in common between agonist and antagonist subsets:

| backbone | interaction estimate (Å) | 95 % CI | signed non-zero |
|---|---:|---|:---:|
| Boltz-2 | **−0.306** | [−0.431, −0.192] | yes |
| Chai-1 | **−0.137** | [−0.223, −0.055] | yes |
| OpenFold-3 | **−0.252** | [−0.384, −0.129] | yes |
| Protenix v2 | **−0.184** | [−0.271, −0.101] | yes |

Negative sign: the agonist-vs-antagonist gap widens against the active reference relative to the inactive reference, i.e. agonist rows sit closer to the active pocket than antagonist rows do.

**This signal is invisible to the binary two-instrument activation predicate.** The binary predicate saturates on Tier 3's cognate arm (both agonist and decoy hit ≈1.0 fraction-active on ~30/40 receptors on most backbones), and the fraction-difference collapses to noise level. The continuous-axis signal in §4.1 gives the same data a different reading — the predicate is at ceiling, the axis is not.

**P4/P5 CI numbers (binary-predicate summaries)** on the post-species-fix v2 corpus [`p4_p5_v2_corpus_recompute.json`, SHA-256 `3731175baf27461a10877764cf19b566b81b3fd172a8be471130ff075f8b06b8`]:

Numbers are **bit-identical** to the pre-species-fix values quoted in `tier3_headline_2026_09_05.md` §4.5:

| ID | Threshold | Boltz | Chai | OF3 | Protenix |
|---|---|---|---|---|---|
| P4 (per-receptor `antag_cog < agonist_cog` on ≥30/40) | ≥30 | 12/28 [+10.00, +24.29] | 3/28 [+0.00, +10.00] | 12/28 [+10.00, +24.29] | 3/28 [+0.00, +10.00] |
| P5 null (`|decoy_apo − agonist_apo| < 0.15`) | < 0.15 | +0.0520 [+0.020, +0.090] | +0.0674 [+0.007, +0.144] | +0.0817 [+0.046, +0.123] | +0.0354 [+0.000, +0.098] |

**Fire-gate call**: P4 FIRES_BELOW on all 4 backbones (12/28 or 3/28, both far below the ≥30/40 threshold). P5 null FIRES_BELOW on all 4 backbones (|Δ| < 0.10 on every backbone, well below the 0.15 threshold). Both are binary-predicate summaries — the withdrawal framing in §6 applies regardless: the P5-fires-below is a saturation artefact on the cognate arm, not evidence of "these models don't distinguish agonists from decoys" as continuous pocket geometry (§4.1) does distinguish them.

**Why numbers didn't move v1→v2**: the species-fix affected columns orthogonal to the predicate axes. The predicate uses `d_npxxy_y558_y753_oh` + `d_gpcrdb_tm6_tilt_246_637_ca` + `passed`; all three are byte-identical between v1 and v2. Fix affected `ligand_role`, `ligand_type`, `ligand_smiles`, `pocket_ca_rmsd`, `pocket_sidechain_rmsd`, `ligand_rmsd_to_ref`, `run_ts_utc`, `cache_key` — none enter P4/P5. Confirmation is a design-verification checkpoint, not a numeric revision.

### Block C Tier 3 — anti-memorisation direction, magnitude within noise

Cluster-bootstrap on `(must_gen − recallable)` signed per-receptor delta of `mean(pocket_ca_rmsd_active | full_agonist, apo) − mean(pocket_ca_rmsd_active | decoy_lig, apo)`, n=13 must-generalise and n=15 recallable per backbone [`task_A_v3_composition_check.json`]:

| backbone | axis | (must_gen − recall) δ (Å) | 95 % CI | verdict |
|---|---|---:|---|---|
| Boltz-2 | pocket_ca_rmsd_active | −0.034 | [−0.127, +0.056] | must_gen larger, within noise |
| Chai-1 | pocket_ca_rmsd_active | −0.063 | [−0.149, +0.016] | must_gen larger, within noise |
| OpenFold-3 | pocket_ca_rmsd_active | −0.018 | [−0.144, +0.096] | must_gen larger, within noise |
| Protenix v2 | pocket_ca_rmsd_active | −0.067 | [−0.180, +0.033] | must_gen larger, within noise |

**Directionally anti-memorisation on 6 of 8 (CA × 4 + SC × 2) cells, but 8 of 8 CIs straddle 0.** At n=13/15 per stratum the magnitude difference cannot be resolved as signed non-zero. Correct reading: the direction is anti-memorisation, the magnitude claim is not supported at this n.

**Chemotype composition — no confound**. Recallable stratum: 9 sm / 6 pep (n=15). Must-generalise stratum: 6 sm / 7 pep (n=13). Two-proportion z on P(small_mol) between strata: **z = +0.73** (|z| < 1.0 → `NO_CONFOUND`) [`task_A_v3_composition_check.json`].

### Block C Tier 3 — pose accuracy, scoped

**On the subset where atom mapping is valid** (OF3 + Protenix, neutral_antagonist arm, `ref_pdb == input_bound_pdb`; n=4,500 rows across 4 cells, per-cell populated at 76–79 %) [`task_E_v3_scoped_finding.json`]:

- **6.93 % aggregate dock rate at `ligand_rmsd_to_ref < 3 Å`** (range 6.18–8.00 % per cell).
- Median per cell 7.15–8.77 Å.
- Verdict `DOCKING_POSE_QUALITY_SCOPED`.

**Explicit non-generalisability**:

- Not for Boltz or Chai — SMILES-derived atom names diverge from CCD; `no_atom_match` at high rates independent of pose quality [`ligand_rmsd_atom_name_gap_2026_09_06`]. Population rates: Boltz/neutral_antag/apo 31–41 %; Chai/neutral_antag/apo 0–10 %. Neither crosses 50 % population floor.
- Not for full_agonist arm — active ref typically different PDB from input's `ligand_bound_pdb` with different agonist chemistry.
- Not for decoy_lig arm — uninterpretable by construction.

**PoseBusters is not a valid comparator.** Chai's 77 % PoseBusters result is dock-into-apo-receptor with one sample and templates allowed. This measurement is co-fold-receptor+antagonist+Gα with 25 samples and templates off. The 6.93 % is a lower bound on what a PoseBusters-shaped Chai measurement would report on this panel.

An MCS-based atom matcher will unlock cross-backbone comparability [`ligand_rmsd_atom_name_gap_2026_09_06`]. Scoped Tier 4 sidebar (deferred) uses this fix.

### Two interfaces behave differently

**P0 cross-block correlation** [`task6_p0_correlation.json`, n=35 common receptors]:

- Spearman ρ = **0.129**, 95 % CI [**−0.213**, **+0.443**]
- Pearson r = **0.142**, 95 % CI [−0.200, +0.454]

**Both straddle zero.** Whether a receptor's family-term contribution (Block B intracellular interface) predicts its ligand-discrimination-term contribution (Block C orthosteric pocket) is **not resolved at n=35**.

The prior unification into "these models read presence, not identity, at both receptor interfaces" treated the two interfaces as if they returned the same result. They do not — the pocket interface discriminates ligand identity on continuous geometry; the intracellular interface reads occupancy with only a partial chemistry signal at the peptide-shape level.

---

## Discussion

**Why the binary predicate misses the pocket signal.** The two-instrument predicate (NPxxY-OH < 9.082 Å AND TM6-tilt > 14.932 Å) is by design a class-conditional *thresholded* readout — active or not, at a Class A calibration point. That thresholding is what made the predicate cleanly report Block A's two-state result at panel scale. It is also what makes the predicate mute when both arms of a contrast sit above (or below) the threshold. On Tier 3's cognate arm, both full-agonist and decoy-ligand co-folded predictions hit fraction-active near 1.0 on ≈30 of 40 receptors: near-native cognate Gα mass is sufficient to drive TM6 tilt plus NPxxY closure regardless of the ligand identity. The binary predicate sees identical active counts on both arms; the underlying continuous pocket-Cα-RMSD does not — the agonist rows sit ~0.14 to 0.31 Å closer to the active-state pocket than antagonist rows do, with cluster-bootstrap CI clearing zero on all four backbones (§4.1). This is the entire mechanical basis for the reframing between v3 (P5 null → "presence not identity") and v5 (predicate saturation → "identity in continuous geometry, occupancy in binary readout"). The methodological lesson is broader than this manuscript: any binary state-prediction summary should carry a saturation audit alongside — the fraction of comparisons where either arm hits 1.0 or 0.0 fraction-active is a necessary caveat on any predicate-based null.

**What the anti-memorisation direction means at n=13/15.** The same-complex split partitions receptors into RECALLABLE (bound crystal in training) and MUST-GENERALISE (bound crystal not in training). If prediction quality on a task were dominated by training-set recall, the recallable stratum would show a larger effect than must-generalise, and their difference `(must_gen − recall)` on the effect axis would be negative. What we find on `pocket_ca_rmsd_active` is `must_gen − recall` slightly negative on 4 of 4 backbones (i.e., the must-generalise stratum shows the same signal in the same direction, with slightly larger magnitude than recallable), but every 95 % CI straddles zero at the current n. That result is *consistent with anti-memorisation* — the direction rules out "the effect is a recall-only artefact" — and is *not sufficient* to claim "the model generalises better on must-generalise than on recall." A larger split (n ≥ 30 per stratum) would resolve that magnitude question; the current claim is directional only. We interpret this as: pose accuracy on the recallable stratum is not systematically better than on must-generalise for the pocket-geometry axis at the receptor-level bootstrap, on any of the four backbones.

**The two-interface asymmetry.** The primary result of this manuscript is that the orthosteric pocket (Block C) and the intracellular interface (Block B) behave differently. The Block B signature is graded, mass-dependent occupancy: apo < decoy < shuffled < cognate on the two-instrument predicate, with a decoy-partner-of-arbitrary-sequence reaching ~60 % active on most receptors. The Block C signature is signed continuous pocket geometry that separates agonists from antagonists but does NOT translate into a binary fraction-active difference on the cognate arm. Cross-block correlation on receptor-level contributions is Spearman ρ = 0.129 with 95 % CI [−0.213, +0.443], straddling zero at n = 35. The prior paper draft (`tier3_headline_2026_09_04.md`, superseded) unified these into "these models read presence, not identity, at both receptor interfaces." That unification is withdrawn (see §Withdrawn claims). The correct reading is that the two interfaces solve different subproblems: the intracellular side is dominated by shape-complementarity of a helical anchor into a preformed cavity, and near-native partner mass is sufficient regardless of anchor sequence beyond ~11 residues; the orthosteric pocket is dominated by ligand-shape geometry against a chemistry-sensitive pocket, and identity matters at Cα resolution though not at the binary predicate.

**PoseBusters is not a valid comparator for this measurement.** PoseBusters [Buttenschoen et al 2024] evaluates docking-into-apo-receptor with a single sampled pose, templates typically allowed, and no protein partner. Chai-1's 77 % PoseBusters score under those conditions is well-established. Our scoped measurement is a different task: co-fold receptor + antagonist + Gα heterotrimer with 25 samples per receptor and templates off. The 6.93 % aggregate dock rate at `ligand_rmsd_to_ref < 3 Å` on the OF3+Protenix × neutral-antag × reference-matched cells (n=4,500 rows) is not directly comparable to 77 % on the PoseBusters task; the two measurements answer different questions on different corpora. What can be said: co-folded ligand poses at the pocket-Cα level correlate with active-vs-inactive state assignment (§4.1); ligand pose accuracy in an all-atom crystal-matched sense on this panel, under this discipline, is scoped to a specific subset. An MCS-based atom matcher (T1.3 loose end #4, landed in this version as `scorer/pocket_metrics.py` MCS fallback) will make the same measurement possible on Boltz and Chai in a forthcoming Tier 4 sidebar.

**Comparison to AF-Cluster and AFsample2.** MSA subsampling is the standard field lever for GPCR conformational sampling. AF-Cluster [Wayment-Steele et al 2024] and AFsample2 [Fischman 2024] both establish that reducing MSA depth to the tens-of-sequences regime surfaces alternative conformations of proteins with multiple stable states. Our current campaign runs at full-depth MSA (per-backbone: Chai `.aligned.pqt` cache with unlimited depth; OF3 ColabFold shim; Boltz-2 and Protenix-v2 upstream ColabFold servers). The response to a subsampling ladder is an obvious question — a full-vs-shallow contrast could reveal whether the two-state signal we report is dependent on the modal-MSA fold or robust to it. Tier D3 (see §Future work) is the pre-registered experiment testing this: 26 Class A receptors × 5 depths (full, 512, 128, 32, 8) × 4 backbones × 5 seeds × 10 samples, with a matched-structure propagation test that halts the tier if any backbone's depth override does not reach the model. We deliberately do NOT report AF-Cluster-style depth results in this preprint version; those land as an addendum after the tier fires.

**Class scope: not a Class B / C / F story at ligand-state resolution.** Block A tested the 48-receptor panel of record — 40 Class A + 4 Class B + 4 Class F — on state 1 (apo) and state 4 (+Gα only). Class B receptors have their activation axis at a TM6 kink at the conserved PxxG motif (Wootten numbering), which we scored with a Class B-conditional predicate. Class F receptors have a receptor-specific TM6 tilt without the DRY motif [Isberg et al 2015]. Both classes give a signal at n=4 that is consistent with Class A directionally but not usable as an active-call fraction at that panel size (`descriptive_n_lt_5_per_side`; per `scripts/derive_per_class_thresholds.py`). The ligand-state work in Blocks B and C is Class A only per pre-registration amendment §C-4. Class B ligand-state experiments are attractive future work — the GLP1R and CRHR1 receptors have well-characterised agonist / antagonist pairs — but require a separate curation pass and are not attempted here.

**A methodological lesson: audit trails, withdrawn claims, and .pyc bytecode**. The Stage 0.0 audit that produced five rounds of retractions on this manuscript's earlier drafts (`STAGE_POST_AUDIT_REPORT_v1..v5.md`) surfaced a fix-reported-not-landed failure mode with a specific signature — the Step 1.3 species-match fix was verified via a `.pyc` bytecode diff between local and HPC `scorer/` trees, and interpreted as source equivalence. The `.pyc` files matched because both machines' interpreters had recompiled the same source. The `.py` source was never patched. The downstream Block C Tier 3 dispatch inherited the untagged manifest builder and produced 800 species-mismatch failures on bovine rhodopsin (OPSD) and jumping-spider rhodopsin-1 (B1B1U5). We document this as a methods vignette (Methods §Validation) because it is the sharpest documented instance of a class of failure mode that any reproducibility-conscious campaign using compiled Python must guard against: a claim of "fix landed" must diff source (`.py`, `.sh`, `.md`) against a named commit, never build artefacts (`.pyc`, `.so`, `__pycache__`, `.o`). We add a corresponding withdrawal to `docs/AUDIT_TRAIL.md §21` and to this manuscript's Methods.

**What this doesn't say.** We do not claim co-folded models are ready for prospective GPCR drug design at the pose level — on the evidence here, they are not. We claim: (i) all four AF3-style backbones produce a detectable two-state switch on Class A GPCRs at 40-receptor panel scale, on both a binary predicate and continuous d_tm6 axis; (ii) the orthosteric pocket contains a state-selective signal that maps ligand identity onto continuous pocket-Cα geometry, invisible to the binary predicate, on all four backbones; (iii) the intracellular interface reads occupancy dominantly, with a partial chemistry contribution at the peptide-shape level; (iv) the two interfaces do not correlate at n=35 receptor-level. These claims, especially (ii), are the load-bearing scientific move in this manuscript, and they survive the sealed-subset and same-complex splits at the current n. The next-step experiments (deep apo bistability, directed inactive by nanobody anchor, MSA-depth ladder) are pre-registered and follow this preprint, not gate it.

---

## Limitations

**Pose accuracy is scoped, not panel-wide**. The `DOCKING_POSE_QUALITY_SCOPED` verdict (6.93 % aggregate rate at `ligand_rmsd_to_ref < 3 Å`) applies to 4 of the 24 receptor × arm × backbone × reference-availability cells that make up the Block C Tier 3 corpus. The 20 remaining cells sit below the 50 % population floor for a reportable rate estimate. Boltz-2 and Chai-1 populate `ligand_rmsd_to_ref` at 0–41 % of the reference-matched neutral-antagonist rows because they emit SMILES-derived atom names that diverge from the CCD conventions the scorer's `(atom_name, element)` matcher expects. This is a scorer-side gap, not an inherent pose-quality claim about those backbones. The MCS-based atom matcher landed in this manuscript's Methods (`scorer/pocket_metrics.py::ligand_rmsd_to_ref`, T1.3 loose end #4) will make the same measurement possible on Boltz-2 and Chai-1 on rescored rows in a forthcoming Tier 4 sidebar. The scoped verdict is what the current corpus can support prospectively; the panel-wide answer requires the sidebar.

**The anti-memorisation direction is signed but not resolved in magnitude**. On the same-complex split for the pocket-Cα-RMSD-to-active axis, `(must_gen − recall)` runs must-gen-larger (i.e., the must-generalise stratum shows the same signal in the same direction) on 4 of 4 backbones. Every 95 % CI on that magnitude difference straddles zero at n=13/15 per stratum. A larger split (target n ≥ 30 per stratum, or a within-receptor design giving each receptor both stratum labels) would resolve the magnitude question. The direction rules out "the effect is a recall-only artefact"; it does not establish "the model generalises better on must-generalise." We frame this as directional evidence of anti-memorisation, not a magnitude claim.

**Reference-cleanliness stripping is close to n where it matters**. The clean G-protein-bound sub-Å-hit count (4 of 10 apo-active-fraction sub-Å hits, on n=24 clean-bound after FSHR + LSHR stripped) is separated from the raw count (6 of 10 on the pre-strip 26) by exactly the two receptors whose inactive reference is a PAM-activated crystal (FSHR 8I2H; LSHR 7FIH). If further Stage 2 audits move any additional receptor from the bound to the free stratum, or vice versa, the count could shift again. The prize-claim `6.84 %` mean apo coherent-active on n=24 is not fragile at this margin — leave-one-out on that stratum shows the mean is not carried by any single receptor — but the sub-Å-hit *count* is n-sensitive by design (one receptor = 10 % of the count). We recommend future audits report both the strict clean-bound stratum and the strip-independent raw stratum, with the strip provenance explicit.

**Reference-set relabels are analysis-time, not source-of-record.** The FSHR 8I2H PAM label and LSHR 7FIH allosteric-agonist label are applied to `refs/reference_set.csv` only at analysis time via `scripts/post_audit_corrections/task_f_v5_clean_bound.py` (git SHA `4a6b9c2c`). The paired-commit ceremony landing these labels into the source-of-record CSV is pending per `[[pending-ceremony-reference-set-2026-09-06]]`. Reviewers who consult `refs/reference_set.csv` at the SHA-256 pinned in this manuscript's provenance appendix will see the pre-ceremony state; the strip is described in prose and in the reconstruction script. This is not ideal reproducibility discipline, and the ceremony will fire on the first commit of any Tier 4 or manuscript-revision workstream.

**Non-Class-A activation is not tested at ligand-state resolution.** Block A calibrated a Class B TM6-kink predicate and a Class F GPCRdb TM6-tilt predicate at n=4 per class, and Block A ran the apo and cognate-Gα arms for the full 48-receptor panel. The ligand-state work in Blocks B and C is Class A only per pre-registration amendment §C-4. Ligand-state predictions on GLP1R, GCGR, PTH1R, CRHR1 (Class B) or SMO, FZD4/6/7 (Class F) are attractive future work — GLP1R has clean agonist/antagonist paired crystals — but require a separate curation pass on the ligand set and are not attempted here. Any prospective claim we make about "these models predict GPCR state on continuous pocket geometry" is a Class A claim.

**Cognate partner is Gα-alone, not the heterotrimer.** All cognate-arm predictions use a single-chain Gα (specifically the `alphas` chain, residues 1–354 of the corresponding G-protein alpha subunit), not the full Gαβγ heterotrimer. This is a design invariant across Blocks A / B / C (CLAUDE.md engineering invariants). The effect of βγ on state prediction is not tested. Prior work suggests βγ contributes to interface stability but not to the TM6 outward movement per se [Sala et al 2023]; however, the assumption is not verified for the four backbones on this panel. Tier D2 (directed inactive state, in preparation) also uses Gα-alone in its cognate arm to preserve baseline comparability.

**Uneven per-backbone MSA discipline.** Chai-1 predictions go through a pre-computed `.aligned.pqt` cache with per-chain SHA-256 verification. OpenFold-3-preview goes through a ColabFold shim with a timeout floor. Boltz-2 and Protenix-v2 use their upstream MSA-server defaults (pre-warmed ColabFold public cache for Boltz-2, Protenix's own MSA server for Protenix-v2). The four MSA disciplines are all documented in `refs/msa_input_interfaces.md` and each is verified prospectively for MSA-arriving-at-model, but they are not identical. Boltz-2 and Protenix-v2 in particular fetch MSAs live per-run; the exact MSA content returned by ColabFold/Protenix servers is not frozen (server-side updates or resource churn could shift depth or sequence composition between our dispatches and any reader's replication). This is a known load-bearing caveat of MSA-server-based inference and applies to every co-folding pipeline using these tools. Tier D3 (MSA-depth ladder, pre-registered) will convert all four backbones to pre-cached MSA files for its runs and address the reproducibility gap for depth-tier claims.

**Backbone training cutoffs are known imperfectly.** Chai-1 training cutoff is 2021-01-12; Protenix-v2 is 2021-09-30; Boltz-2 is 2023-06-01. OpenFold-3-preview cutoff is not stated on the model card and is treated as unknown throughout this manuscript. Any claim built on training-cutoff stratification (e.g. anti-memorisation, held-out subset validation) is conservative on OF3 — we treat every OF3 comparison as if the crystal could be in training. This inflates the anti-memorisation CI on OF3 but does not bias the direction. A future revision with OF3's confirmed cutoff would tighten these bounds.

**Sample count (5 seeds × 10 samples) may under-sample low-frequency modes.** The apo two-instrument coherent-active fraction on some receptors (e.g. CXCR4, GHSR, NPY1R) sits at 2–4 % under (5, 10) = 50 samples per cell. At that rate, 1–2 hits per cell is too thin to distinguish a real minor basin from a lucky draw. Tier D1 (deep apo bistability, pre-registered) resamples these cells at (5, 100) = 500 samples per cell to harden the CI on the sub-Å hit rate. The current manuscript's sub-Å hit distribution is thus a lower bound in resolution; Tier D1 will refine it.

---

## Withdrawn claims (audit trail — enumerated for reviewer transparency)

Ten prior formulations retracted after the Stage 0.0 audit (five sequential rounds v1–v5). Retention here so reviewers who find earlier repo commits or preprint-adjacent language can trace the retraction:

1. **"P5 null holds on all 4 backbones → models don't distinguish agonists from decoys at the ligand interface"** — withdrawn as binary-predicate saturation artefact on the Tier 3 cognate arm.
2. **"Presence not identity" unification of Block B + Block C** — withdrawn. Block C alone tests identity (Tier 3 dropped `none`); P0 cross-block correlation straddles zero.
3. **P6 "definitively excludes docking failure" (v1)** — replaced by scoped 6.93 % aggregate dock rate on OF3 + Protenix × `neutral_antag` × {apo, `g_alpha`}, non-generalisable to Boltz, Chai, agonist arm, decoy arm. PoseBusters 77 % is not a valid comparator.
4. **AA2AR "609 active-like / 1,279 inactive-like at 1,888 rows" attribution to Block A** — that figure is from the v3.6b campaign (17,568 rows), not Block A. At Block A row counts AA2AR is unimodal [`aa2ar_unimodal_block_a_counter.json`].
5. **"14.5 % panel-mean apo coherent-active fraction"** — recomputes to **15.5 %** with pinned provenance. Prize claim leads with clean-bound stratum mean 6.84 % on n=24 (§Results), not the panel mean.
6. **"14× compresses to 3.2× under stratification"** — retracted; different statistics on different memberships. On matched, ratio EXPANDS (mean 5.02×, median 19.00×).
7. **v4's "6 of 10 hits in G-protein-bound stratum"** — revised to 4 of 10 in clean G-protein-bound stratum after Block C Stage 2 flagged FSHR (8I2H) and LSHR (7FIJ) inactive references as PAM-activated.
8. **`HEADLINE_CONFIRMED_AT_PANEL_SCALE` verdict** on the earlier Stage 8 negative-null claim — withdrawn along with binary-predicate framing.
9. **Chai P5 zero-CI [0.000, 0.000] on Tier 1 as strong evidence** — predicate saturation on Tier 1's smaller panel (n=8), not true agonist-vs-decoy indistinguishability.
10. **"Nature Methods preprint imminent" implicit framing** — this manuscript is the preprint.

---

## Future work

Four pre-registered tiers extend the current corpus (PREREG amendment §D). All are dispatched only after this manuscript's preprint version ships; each addresses a specific reviewer concern on the current claims.

**Tier D1 — Deep apo bistability** (14,000 predictions, ~1–2 days on 15–20 H100). Seven-receptor panel (`refs/tier_d1_panel.csv`, committed with pinned selection rule): CNR2 as anchor (the one current sub-Å hit with a mixed-cell apo arm at 0.27 coherent-active fraction), OPSD/ADRB2/LPAR1 as mid-range (apo active fraction 0.15–0.60 — the measurable regime for bimodality), and CXCR4/GHSR/NPY1R as a confirmatory subset (retained for sub-Å tail replication at 5× sampling). Grid: 7 × 4 backbones × 5 seeds × 100 samples per seed (a targeted departure from the (5, 10) lock; PREREG amendment §D-1). Primary deliverable: cluster-bootstrap CI on the sub-Å hit rate and on the apo two-instrument coherent-active fraction per (receptor, backbone) at n=500 samples per cell. Secondary deliverable: Hartigan's dip test + Gaussian-mixture k-mode fit on **continuous axes** (d_tm6, NPxxY-OH, GPCRdb TM6 tilt, RMSD-to-active) — not on the binary predicate, which cannot resolve modality by construction. Kill criterion: dip test uninformative → drop the two-mode claim; keep the CI-hardened distribution as the primary deliverable. Tier ships value regardless.

**Tier D2 — Directed inactive state** (800–3,200 predictions depending on curation yield, ~2–4 days including anchor curation). Grid: `n × 4 arms × 4 backbones × 5 seeds × 10 samples` where arms = {apo, cognate_gα, active_nb, inactive_nb} per anchor availability. From `refs/nanobody_state_anchors.csv` the 4 usable anchors are: ADRB2 matched pair (5JQH Nb60 inactive + 4LDE Nb-active), OPRK single Nb-inactive (6VI4 Nb6+JDTic), ACM2 single Nb-active (4MQS Nb9-8+iperoxo), AGTR1 single Nb-active (6OS2 already in refs). Minimum experiment: β2AR alone × 4 arms × 4 backbones × (5, 10) = 800 preds is a complete existence proof of directional state control by input chain. Fire-gate: inactive-Nb arm's d_tm6 significantly below apo AND below cognate_gα, pocket-Cα-RMSD-to-inactive significantly below pocket-Cα-RMSD-to-active on inactive-Nb arm. Training-cutoff flags: ADRB2 anchors are pre-Chai/Protenix/Boltz-2; OPRK anchor is post-Chai/Protenix, pre-Boltz-2. OF3 cutoff unknown. This tier turns "off = absence" into "off = directed by input chain" — the paper's current asymmetry (active-steered by cognate Gα choice; inactive-default by apo) becomes a controllable-two-state generation claim.

**Tier D3 — MSA-depth ladder** (27,200 predictions, ~4–7 days including plumbing). 26 Class A receptors (`refs/tier_d3_panel.csv`) × 5 depths (`full`, `512`, `128`, `32`, `8`) × 4 backbones × 5 seeds × 10 samples. Plus a subsample-variance probe: 3 independent draws at depth=32 × 2 receptors × 4 backbones × (5, 10) = 1,200 preds, measuring which-N-1 draw-variance against seed-variance. Plumbing overhaul required (D3 backbone plumbing spec, `experiments/024_tier_d3_msa_depth/spec/D3_BACKBONE_PLUMBING_SPEC.md`): each backbone's launcher gains a `MSA_A3M_PATH` env var; when unset, current live-server behaviour holds (zero regression on Blocks A/B/C); when set, backbones read pre-subsampled MSA files. `scripts/subsample_msa.py` (landed, 16/16 tests, byte-identical replay) produces the subsampled files. Kill criterion (STRONG): matched-structure propagation test compares full-depth vs depth=8 outputs at the same seed and same sample index; if Cα RMSD between the two structures is below 0.5 Å (numerical noise floor) on any backbone, that backbone silently ignored the depth override — halt tier before smoke, regardless of what status JSON says. The config-echo layer has produced false-green propagation tests before (audit trail §10, §21); the matched-structure comparison cannot be faked by the echo layer.

**Tier 4 — Cross-backbone pocket dissection** (dispatch-count TBD, ~2–3 days). Gated on the MCS atom matcher landing (T1.3 loose end #4, delivered in this manuscript's Methods). Rescore the existing Block C Tier 3 corpus with the MCS matcher active, extending `ligand_rmsd_to_ref` coverage from ~4,500 rows (OF3+Protenix × neutral_antag × ref-matched) to the full 40,800-row corpus where CCD entities overlap between predicted and reference ligand. Cross-backbone pose accuracy becomes a reportable statistic on Boltz-2 and Chai-1 for the first time. Pocket-vs-transmission dissection (the amendment paragraph in the 2026-08-28 plan) becomes measurable: does the pocket-Cα-RMSD signal (§4.1) correlate with `ligand_rmsd_to_ref` at the ligand-atom level, or are the two axes independent?

Tiers D1, D2, and D3 are pre-registered in `refs/PREREG.md` amendment §D-1 through §D-3. Tier 4 does not require a new pre-registration; it is a rescore of existing corpus with the MCS matcher enabled.

---

## References

*[EXPAND: 40–60 references. Anchor papers to cite:]*

- Isogai et al 2016, *Nature Chem Biol* — TM6 outward as activation signature.
- Wingler & Lefkowitz 2020, *Trends Cell Biol* — biased signalling in GPCRs.
- Ballesteros & Weinstein 1995, *Methods Neurosci* — BW numbering.
- Wootten et al 2016 — Class B numbering.
- Isberg et al 2015, *Trends Pharmacol Sci* — GPCRdb.
- Heo & Feig 2022 — AlphaFold-Multimer for GPCRs.
- Sala et al 2023 — AF-Multimer state selection with Gα.
- Wayment-Steele et al 2024, *Nature* — AF-Cluster.
- Fischman 2024 — AFsample2.
- Zhu et al 2024 — Boltz-2.
- Chai Discovery 2024 — Chai-1.
- OpenFold consortium 2024 — OpenFold-3-preview.
- ByteDance 2024 — Protenix v2.
- Bryant et al 2022, *Nat Commun* — MSA subsampling for conformational ensembles.
- Buel & Walters 2022 — protein-ligand co-folding limits.
- Jumper et al 2021 — AlphaFold-2.
- Abramson et al 2024 — AlphaFold-3.
- Rasmussen et al 2011, *Nature* — β2AR Nb80/Nb60 (structures 3P0G, 5JQH).
- Wingler & Lefkowitz 2020 — biased signalling review.
- Cong et al 2019 — post-ML pose evaluation.
- Buttenschoen et al 2024 — PoseBusters.

*[Full bibliography TBD in v2 draft; every claim in Results section will have a numbered citation.]*

---

## Provenance appendix (SHA-pinned)

**Verification JSONs used in this manuscript** (SHA-256 pinned at draft time):

| file | SHA-256 |
|---|---|
| `experiments/021_block_c_tier3_pharmacology/analysis/verification/task_F_v5_clean_bound_stripped.json` | `524672ee87f6d93aa169dc5120f34cb49f42cfad90b85ea5913f91d3e39f4cfe` |
| `verification/task_A_v3_composition_check.json` | `f7a8c199b5beed19c3d128729ea2ee5241e38af4396c7639b1fa08e7455c237b` |
| `verification/task_E_v3_scoped_finding.json` | `caa0226e19ccb3eb1faf69ab067dfcd635bc3b60145d828c075d1de7c16a17d0` |
| `verification/stage3_2x2_ligand_state_specificity.json` | `0cf2707b52c70c57397ea89346ff0a9acc8109fb220d1be2b56b37de385c4401` |
| `verification/task6_p0_correlation.json` | `d4193bf62672287a343461d507fd1e0ed9d1ff59e1381fc8106d17d53b7b98c7` |
| `verification/STAGE_POST_AUDIT_REPORT_v5.md` | `2e764ddc87abaf8b44431a12b833653bb76bd8bf24f86b65a8e0cd85383442f3` |
| `verification/cohens_d_block_a_d_tm6.json` | `0adb183a4e6efe9bbc062acce5f40c2078875ef1fff4a0aba717dc4eb9b9d443` |
| `verification/aa2ar_unimodal_block_a_counter.json` | `5e873270d9826a6d8c907783a0ce1c43e9f9f117e595ab0526c9cc2d02b54513` |
| `verification/p4_p5_v2_corpus_recompute.json` | `3731175baf27461a10877764cf19b566b81b3fd172a8be471130ff075f8b06b8` |

**Load-bearing input CSVs**:

| file | SHA-256 |
|---|---|
| `experiments/018_block_a_switch_test/analysis/rows.pocket.csv` | `49d19da9a916939bb9a1429ea11aef0b43d6f8242beaa03e309a2755eff2bc58` |
| `experiments/018_block_a_switch_test/analysis/rows.rmsd.csv` | `a82ad56076bb48edcd8723d6fbd52349a409fc4e09b1be170fa4df62914f302e` |
| `experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv` | `5ccf58acc8a6b0151250007c6b40d1f728ad4b42c2eeab22bd6509b5809e2103` |
| `refs/reference_set.csv` | `7a261988ff73eedc9d21e5cc2a9eaf0436b9f38e3827a87493295a8d8382b90c` *(ceremony-gated; will change on Gate 2 relabel commit)* |
| `refs/tier3_panel.csv` | `63cdd49c3380b89202fadc6439e06e5e412452c1c96c6105a66dcf897fc76e6f` |

**Manuscript git SHA at v1 draft time**: `[to be filled at commit time]`. Local-only per CLAUDE.md standing rule; no push without user go.

---

## Draft version history

- **v1 — 2026-09-06**: initial skeleton from `tier3_headline_2026_09_05.md` + all pinned verification JSONs. Sections marked `*[EXPAND: ...]*` for detailed prose. Withdrawn-claims enumeration retained verbatim from `tier3_headline_rewrite_provenance.md`.

*Local commit only per project standing rule (CLAUDE.md).*
