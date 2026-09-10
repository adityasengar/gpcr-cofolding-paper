# BLOCK C — STATE CHECK (Section 0 of closeout dispatch)

**Date**: 2026-09-10.
**Baseline**: repo HEAD `80a5a60` (Block B closed at `block_b_final`).
**Rule**: disk wins over recall. Where disk conflicts with a recalled fact,
the conflict is logged.

---

## (a) Primary corpus

**Path**: `experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv`
**Row count**: 40,800 data rows (40,801 lines including header).
**File SHA-256**: `5ccf58acc8a6b0151250007c6b40d1f728ad4b42c2eeab22bd6509b5809e2103`.
**`scorer_git_sha` distribution**: `3d9c6faae59b5aa5881994dee4d36e36ea5367da`
on 40,800/40,800 rows (uniform, single value).
**`ref_set_csv_sha256` distribution**: single value across corpus (per
`ref_set_csv_sha256` column).
**Panel shape** (derived from `input_path` regex):
- Backbones: `boltz`, `chai`, `of3`, `protenix` (10,200 rows each).
- Arms: `apo` 20,400 / `cognate` 20,400 (equal per backbone: 5,100 each).
- Ligand roles: `full_agonist` 14,800 / `decoy_lig` 14,400 / `neutral_antagonist` 11,600.
- Receptors per backbone: **36** distinct `receptor_slug` values (NOT 40 —
  4 of the 40-receptor Class A panel dropped pre-dispatch or pre-scoring).
- `passed=True`: 40,000/40,800 (98.04 %). 800 failures cluster on OPSD
  and B1B1U5 (A5_species_match pattern per `docs/AUDIT_TRAIL.md §21`,
  a manifest-builder mis-slug that was fixed but pre-existing rows carry
  the failure flag).

**Sibling corpus** (post-Bug-#2/#3 fix, NOT the primary):
- Path: `experiments/021_block_c_tier3_pharmacology/rescore_t7c_full/rows.csv`.
- 40,800 rows; scorer_git_sha `d9c646af5f89861c16062bf256de96a8389d9915`
  (uniform, different from primary).
- Purpose: pose accuracy corpus for T7c headline (Bug #2 tripwire +
  Bug #3 MCS-automorphism fix). Manuscript's pose-section numbers rest
  on THIS corpus; the S1 classifier and 2×2 pocket-Ca interaction rest
  on the primary. `T7C_POST_FIX_HEADLINE.md` cites scorer
  `891041e858f3747b…` in its prose text — that string does not match
  the actual `scorer_git_sha` column value (`d9c646af…`). Documentation
  drift; the row-level value is authoritative.

**Corpus vs manuscript**: `docs/BLOCK_C_PAPER_DRAFT_v1.md` cites
verification JSONs at `experiments/*/analysis/verification/`; 51 JSONs
present at `experiments/021_block_c_tier3_pharmacology/analysis/verification/`
(covers `stage3_2x2_ligand_state_specificity`, `task_A_v3_composition_check`,
`task_E_v3_scoped_finding`, `task_F_v5_clean_bound_stripped` and the
Stage-0.0 v1–v5 post-audit report chain). No cited path is missing.

## (b) Tier 1 vs Tier 3

**Tier 1** (`experiments/020_block_c_tier1_ligand/` — earlier pilot):
- 8 Class A receptors, ~14,800 predictions.
- Original claim `[Block C Tier 1 headline 2026-09-04]`: "P5 null holds on
  all 4 backbones → property-matched decoys activate apo receptor as much
  as real agonists on the two-instrument predicate".
- **Retired**. Two citable pointers:
  1. Manuscript §Withdrawn item #9: *"Chai P5 zero-CI [0.000, 0.000] on
     Tier 1 as strong evidence — predicate saturation on Tier 1's
     smaller panel (n=8), not true agonist-vs-decoy indistinguishability."*
  2. Auto-memory record `[Block C Tier 3 pocket identity 2026-09-06]`
     header line: *"SUPERSEDES [[block-c-tier1-headline-2026-09-04]]"*.
- Tier 1's P5 claim was the framing that Tier 3's saturation audit
  falsified (§Withdrawn items #1 + #2 also cite Tier 1's binary-predicate
  reading).

**Tier 3** (`experiments/021_block_c_tier3_pharmacology/` — this dispatch's
corpus):
- 40 Class A receptors dispatched, 36 landed; 40,800 predictions.
- Carries every surviving Block C claim (2×2 pocket-Ca interaction, S1
  classifier, per-receptor AUROC bimodality, cross-backbone consensus
  vs pLDDT).
- Manuscript v1's Results section rests on Tier 3.

**Verdict**: Tier 1's claims are retired via two independent citable
records (manuscript §Withdrawn + memory supersession pointer). Live
Block C claims rest on Tier 3 alone. Tier 1 rows go to `release/_internal/`.

## (c) S1 classifier receptor list

**Pin: n=15**, not 14. Disagreement resolved.

**Origin of the disagreement**: `PREREG_SIGNAL_RECOVERY.md` (locked
2026-09-07 pre-numbers) states: *"9 receptors that are 100 % self-reference
on the antag_inactive cell: ACM4, ADRB2, CCR5, CNR1, CNR2, DRD3, NPY1R,
OPRD, OPRK. S1 self-reference-excluded run: 14 receptors (23 − 9)."*

**What actually landed**: `s1_loro_classifier.json` variant
`C_no_selfref_apo` reports `n_receptors_evaluated: 15` on all four
backbones × F_ii/F_iii. Root cause: **DRD3 is on the self-ref list but
was NOT in the common 23-receptor set** (dropped in pre-classifier
curation). Actual intersection: 23 common − 8 self-ref-that-are-in-common
= **15**. Prereg text's `23 − 9 = 14` did the subtraction on the wrong
set.

**Pinned 15-receptor list** (from JSON variant 26, boltz F_iii,
`C_no_selfref_apo`):
```
5HT1B, 5HT5A, AA1R, AA2AR, ACM2, AGTR1, CXCR2, CXCR4, EDNRB,
GRPR, LPAR1, LT4R1, MCHR1, NPY2R, OPRX
```

**KILL-S1 row (pre-registered kill threshold ≥ 0.65 LORO AUROC on apo
× self-ref-excl × F_iii)**:
| backbone | F_iii AUROC | vs kill ≥ 0.65 |
|---|---:|---|
| boltz | 0.852 | PASS |
| chai | 0.706 | PASS |
| of3 | 0.656 | PASS (marginal) |
| protenix | 0.825 | PASS |

**Downstream impact of the 14 → 15 pin**: no signed AUROC changes (the
per-receptor AUROC dict simply has 15 keys, not 14). Any manuscript
text saying "14 held-out receptors" must be corrected to 15. Any
downstream analysis that iterated over 14 receptors would land on the
same 15 because the 15 is what the JSON contains.

**Notation caveat**: the manuscript draft and the SIGNAL_RECOVERY_REPORT
`S8a` per-receptor table both say "14 of 15 held-out receptors reliable
+ AGTR1/CXCR2 catastrophically inverted". That phrasing is consistent
with n=15; the "14" there is (15 − 1 AGTR1 inversion), not (23 − 9). No
edit required to that sentence.

## (d) Block C artifacts after 2026-09-05

Enumerated by mtime `newer than 2026-09-05` under
`experiments/021_block_c_tier3_pharmacology/`:

**Analysis outputs** (all under `experiments/021_block_c_tier3_pharmacology/analysis/verification/`):
- 51 verification JSONs including `stage3_2x2_ligand_state_specificity.json`,
  `task_A_v3_composition_check.json`, `task_E_v3_scoped_finding.json`,
  `task_F_v5_clean_bound_stripped.json`.
- Stage 0.0 chain: `STAGE_0_0_REPORT.md`, `STAGE_POST_AUDIT_REPORT_v1..v5.md`,
  `stage3b_v2_headline_wording.md`, `stage3f_v2_apo_bistability_reframe.md`,
  `stage3f_v3_apo_bistability_reframe.md`.
- Task chain: `task1_p4_denominator.json` .. `task9_provenance.json`;
  `task_A_of3_cutoff_verification.json`, `task_A_v2_agonist_vs_decoy_apo_same_complex.json`,
  `task_A_v3_composition_check.json`, `task_D_species_match_root_cause.json`,
  `task_E_p6_ligand_rmsd_to_ref.json`, `task_E_v2_reference_ligand_mapping.json`,
  `task_E_v3_scoped_finding.json`, `task_F_block_a_continuous_recheck.json`,
  `task_F_v2_apo_bistability_recheck.json`, `task_F_v3_reference_state_stratification.json`,
  `task_F_v5_clean_bound_stripped.json`.

**Signal-recovery outputs** (`experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/`):
- Pre-reg + report: `PREREG_SIGNAL_RECOVERY.md`, `SIGNAL_RECOVERY_REPORT.md`.
- Late checkpoint: `CHECKPOINT_2026_09_07_late.md`, `CHECKS_2026_09_07_LATE.md`,
  `DOCKING_MEASUREMENT_STATUS.md`, `PR2_PR3_PR4_SUMMARY.md`.
- Post-fix headline: `T7C_POST_FIX_HEADLINE.md`.
- PR1–PR5 sweeps: `pr1_stale_corpus_sweep.{json,md}`, `pr2_fshr_lshr_class.json`,
  `pr3_apo_coh_active_reference.json`, `pr4_stratum_cis.json`,
  `pr5_matchcount_census.json`.
- S1–S8 verification (KILL-S1..KILL-S4): `s1_loro_classifier.json`,
  `s2_sample_budget.json`, `s3_consensus_confidence.json`,
  `s3_cross_backbone_consensus.json`, `s4_bw_decomposition.json`,
  `s4_bw_position_decomposition.json`, `s5_p4_ordinal.json`,
  `s6_generalization.json`, `s7_nulls_ceilings.json`,
  `s7_s8_ceiling_domain.json`, `s7c_foldintegrity_discharge.json`,
  `s8_applicability.json`.
- T7b/T7c pose accuracy: `t7b_pose_accuracy.json`, `t7b_pose_accuracy_fix.json`,
  `check2_fi_finite_subset.json`.
- Auxiliary tables: `nan_reason_census.csv`, `nan_reason_census_by_receptor.csv`,
  `reference_survey.csv`, `reference_survey_summary.md`,
  `step3_paired_mcs_vs_fastpath.csv`, `step4_cell_receptor_distribution.csv`,
  `step4_ecdf_per_receptor.csv`, `viz_t7c_candidates.json`,
  `viz_v2_candidates.json`.

**Rescore trees** (SHA-manifested outputs):
- `rescore_t7b/rows.csv` (20,400 rows, MCS-enabled Boltz+Chai rescore).
- `rescore_t7b_fix/rows.csv` (subsequent Bug #2 tripwire fix).
- `rescore_t7b_smoke/rows.csv` (smoke pilot).
- `rescore_step3_forcemcs/rows.csv` (paired MCS-vs-fast-path 500-row sample).
- `rescore_t7c_full/rows.csv` (40,800 full corpus, post-Bug #2/#3 fixes).

**Rescore-v2 tree** (`experiments/021_block_c_tier3_pharmacology/analysis/rescore_v2/`):
- `rows.csv`, `verification/` sub-dir.

**Manuscript draft cite path**: `docs/BLOCK_C_PAPER_DRAFT_v1.md` (dated
2026-09-06 in preamble) cites every verification JSON above by relative
path. **All cited paths resolve on disk** — the compaction-summary claim
of a stale 09-04 headline is not observed (the manuscript is v1 dated
09-06; no 09-04 file is cited).

## (e) Pocket-Cα reference separation table (40 receptors)

**EXISTS.** Built during Block B's Item 3 (E4-adjacent O-3 output) per
`docs/BLOCK_B_CLOSEOUT.md` Item 3.

**Path**: `experiments/019_block_b_partner_selection/analysis/reference_separation_pocket_ca.csv`.
**SHA-256**: `ed8505771108beec1be739d12802d253b93a0dc3f5429b50bf85d065c53b57cb`.
**Rows**: 40 receptors (41 lines including header).
**Columns** (12): `receptor, active_pdb, inactive_pdb, pocket_ca_rmsd_A,
delta_ref_npxxy_A, delta_ref_tilt_A, pocket_ca_rank_of_40, cif_source_note,
n_pocket, n_common_tm, tm_kabsch_rmsd_A, status, pocket_missing`.
**Method** (per `docs/BLOCK_B_ITEM3_AA2AR_AND_POCKET_CA.md`): 12 BW
positions (3.32, 3.33, 3.36, 5.42, 5.43, 5.46, 6.48, 6.51, 6.52, 6.55,
7.39, 7.42) from `scorer/pocket_metrics.py`. 7TM Cα Kabsch alignment
via `gemmi.superpose_positions`, residue-wise pocket-Cα RMSD.
**Distribution**: min 5HT1B 0.53 Å, Q1 1.03, median 1.23, Q3 1.55,
max 1.90 Å; mean 1.25 Å.
**AA2AR rank**: 34/40 on pocket-Cα (top third of separation).

**G2 will**: join per-receptor AUROC (from `s1_loro_classifier.json`
variant 26 keys) against this table's `pocket_ca_rmsd_A` column. Build
step is join + regression; no CIF processing needed. Zero-cost input.

## (f) paper_af3_release state

**Path**: `../paper_af3_release/` (peer repo of paper_af3).
**HEAD**: `f62811c` (2026-09-10, "Block B Item 3: pocket-Cα reference
separation table + AA2AR adjudication").
**Origin**: at `e433db9` (`block_a_freeze`, 2026-09-09). **Two unpushed
local commits**: `a01d774` (Block B sync — dossier + claim sheet + 16
caveats + 6 withdrawals + 9 phase reports + analysis CSVs) and `f62811c`
(Item 3 pocket-Cα table). Not pushed per standing rule.

**Tags** (release repo): `block_a_freeze`, `post-review-analysis-batch`,
`pre-scientific-review`. **No `block_b_*` or `block_c_*` tag yet** on
release.

**Ledger schema** (`LEDGER.csv`, 10 Block A rows populated SC-1..SC-10):
`claim_id,block,claim_sentence,number,n,ci_95,null_beat,arms_backbones_supported,script_path,input_sha,dossier_phase,manuscript_sentence,status`.
This is the schema Block C rows will conform to.

**Manifest** (`MANIFEST.csv`): stub with header comments only. Populated
by `code/build_scripts/build_manifest.py`; needs a run at Block C commit.

**Directory layout** (relevant):
- `dossiers/BLOCK_A/` + `dossiers/BLOCK_B/` (`dossiers/BLOCK_C/` MISSING).
- `caveats/`: 12 Block A (C-1..C-12) + 16 Block B (C-B-1..C-B-16) files.
  No Block C caveats yet (naming convention will be `C-C-*` per prefix
  discipline).
- `withdrawals/`: Block A + Block B files. Block C withdrawals need
  landing — dispatch expects one file per withdrawal (10 in the
  manuscript, plus recovery notes).
- `analysis/block_a/`, `analysis/block_b/`. `analysis/block_c/` MISSING.
- `data/block_a/`, `data/block_b/`, `data/block_c/{tier1,tier3}` —
  the block_c subdirs already exist as stubs (empty or pending).
- `data/d_tier/`, `data/exploratory/`.
- `RECON/`: 3 rounds of recon deliverables present.
- `panel/`, `code/`, `manuscript/`, `prereg/`, `figures/`.

**Freeze table** (`VERSION.md`): Block C tier 1 + tier 3 rows say
`pending` for every column (Dossier, Data, Structures, Analysis,
Scorer commit, Launcher dispatch tag). Part B (release commit) fills
these.

---

## Gate

The three hard-stop conditions:

- (a) primary corpus: **established**. `rows.tier3.v2.csv` SHA-pinned.
- (c) S1 receptor list: **established**. n=15, pinned to a specific
  receptor list.
- (e) pocket-Cα reference-separation table: **established**. Block B's
  E4-adjacent O-3 output, SHA-pinned.

**No STOP condition triggered.** Proceeding to Part A (G1–G7).

## Deltas that should propagate to Block C write-ups

Findings from this state check that any downstream sentence must respect:

1. **Corpus scorer sha vs pose-corpus scorer sha differ.** Every
   manuscript sentence citing a pose number must cite
   `rescore_t7c_full/rows.csv` (scorer `d9c646af…`); every sentence
   citing a classifier or 2×2 interaction must cite `rows.tier3.v2.csv`
   (scorer `3d9c6fa…`). Reader will otherwise conflate.
2. **`T7C_POST_FIX_HEADLINE.md` cites a scorer SHA (`891041e858f3747b…`)
   that does not match the actual row-level column.** Documentation drift.
   Flag for correction in Part B; the row-level value is authoritative.
3. **Panel size is 36, not 40**, in the landed corpus. Four Class A
   receptors from the pre-dispatch 40-receptor panel did not survive
   into `rows.tier3.v2.csv`. Any "40-receptor Class A panel" claim in
   the paper needs a dispatch-vs-landed disambiguation footnote.
4. **S1 receptor list is 15, not 14.** Not a signed status change but
   a text-fix.
5. **Manuscript §Withdrawn already enumerates 10 retractions.** Part B's
   `release/withdrawals/` needs one file per retraction, mirroring the
   Block B convention.

---

**End STATE_CHECK. Proceeding to G1..G7 (Part A).**
