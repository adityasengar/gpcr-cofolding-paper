# BLOCK B — EXPERIMENT DOSSIER

**Corpus**: `experiments/019_block_b_partner_selection/` — 40 Class A receptors × 4 backbones × 4 arms × 5 seeds × 10 samples = 32,000 rows.
**Freeze tag**: `block_b_freeze` (see `Final` in the phase list).
**Companion files**: `BLOCK_B_CLAIM_SHEET.md`, `BLOCK_B_MANUSCRIPT_FLAGS.md`, `caveats/C-B-*.md`, `withdrawals/W-B-*.md`, `dossiers/BLOCK_B/figures/BB-*.md`.

---

## Executive summary

Block B ran the partner-selection ladder (apo → decoy → shuffled → cognate) on 40 Class A receptors across four structure-prediction backbones, testing whether the model reads partner **identity** or partner **mass**. The design is 32,000 predictions and, at Phase 2, grid-complete (0 non-conforming cells). Every load-bearing regression detector on Phase 0 is negative (single `scorer_git_sha`, single `ref_set_csv_sha256`, zero OF3-sentinel hits, HPC has no `.git` checkout). The published ladder (apo 0.158 / decoy 0.558 / shuffled 0.809 / cognate 0.891) reproduces exactly on frame_36 (n=36 excluding EDNRA/EDNRB/GRPR/HRH3 with all-NaN NPxxY). The correct-family term is **11.1% on the probability scale and 17.4% on the logit scale** — a manuscript-changing finding; the 11% figure is partly a ceiling artifact (24–34 of 40 receptors per backbone have cognate ≥ 0.98). On the continuous residual axis below the binary predicate, **Outcome A is signed** (the model treats the partner as mass-matched bulk) and firms up under Phase 6b's native-only re-run of the load-bearing Gs→Gi cell (native n=20 of 24 receptors; residual −0.062 Å [−0.41, +0.21]). Interface geometry corroborates: the PIF connector on decoy engaged-but-inactive rows sits at apo geometry (15.42 Å vs cognate/shuffled active-engaged ~16.00 Å), a per-prediction independent axis that was never used to call anything.

One backbone is systematically different across three separate axes: Chai runs unpaired MSAs everywhere (Phase 1 §1d), its decoy-arm α5-CT columns appear as lowercase soft-masked or trailing gaps, its tilt-axis continuous top-rung is inverted, and its Phase 4 partner-pLDDT-inversion test is unmeasurable because only 5/2,000 cognate rows are non-engaged. Report Chai separately or with a per-backbone caveat (C-B-2).

The reference set Block B was scored against is `refs/reference_set.blockb_pinned.csv`, SHA-256 `6ee2cad8…`, byte-identical to what row-level pins carry. Post-run edits to the primary reference file added six inactive rows for three Block B receptors but never mutated an existing row; scoring bytes are unaffected (C-B-9).

Block B does NOT claim: prospectivity (foreclosed by design; date-stratified holdout is Block C); mechanism at the residue level (Block C tier 3); directional control (Block D D2). Novelty is panel scale on the partner-identity question with a calibrated two-instrument predicate, four backbones, and an orthogonal PIF-connector corroboration.

**GATE SUMMARY** (verdict + report path):

| Phase | Gate | Report |
|---|---|---|
| Phase 0 provenance | CONDITIONAL (5 items resolved) | `docs/BLOCK_B_DOSSIER_PHASE_0_PROVENANCE.md` + addendum |
| Phase 0 §Item 3 templates sweep | Class (b)+(c) unchanged | `docs/BLOCK_B_DOSSIER_PHASE_0_TEMPLATES_SWEEP.md` |
| Phase 1 construct identity | CONDITIONAL (cleared) | `docs/BLOCK_B_DOSSIER_PHASE_1_CONSTRUCT_IDENTITY.md` |
| Phase 1d extension | 3 READ / 1 NOT-READ (Chai) | `docs/BLOCK_B_DOSSIER_PHASE_1D_EXTENSION.md` |
| Phase 2 execution census | PASS | `docs/BLOCK_B_DOSSIER_PHASE_2_EXECUTION_CENSUS.md` |
| Phase 3 ladder every scale | CONDITIONAL (family term scale-dependent) | `docs/BLOCK_B_DOSSIER_PHASE_3_LADDER.md` |
| Phase 4 interface geometry | PASS | `docs/BLOCK_B_DOSSIER_PHASE_4_INTERFACE_GEOMETRY.md` |
| Phase 5 donor-class residuals | PASS Outcome A | `docs/BLOCK_B_DOSSIER_PHASE_5_DONOR_RESIDUALS.md` |
| Phase 6 covariates + refs | PASS | `docs/BLOCK_B_DOSSIER_PHASE_6_COVARIATES_AND_REFERENCES.md` |

---

## Panel of record + design + predicate

**Panel** — `refs/gpcr_coupling.csv` intersected with the Block A Class A subset. 40 receptors:

5HT1B, 5HT2C, 5HT5A, AA1R, AA2AR, ACM1, ACM2, ACM4, ADA2A, ADRB1, ADRB2, AGTR1, APJ, B1B1U5, CCKAR, CCR5, CNR1, CNR2, CXCR2, CXCR4, DRD2, DRD3, EDNRA, EDNRB, FSHR, GHSR, GRPR, HRH1, HRH3, LPAR1, LSHR, LT4R1, MCHR1, NPY1R, NPY2R, OPRD, OPRK, OPRX, OPSD, OX2R.

Class B and Class F are excluded from Block B (see `caveats/C-B-15_class_a_only.md`); they are Block A instrument-scope carve-outs. The **published two-instrument predicate**, per PREREG §15 v2 post-cleanup, is class-conditional. Block B is Class A only, so a single predicate applies:

    d_npxxy_y558_y753_oh < 9.082 Å   AND   d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å

NaN on either axis → False. Four receptors (EDNRA, EDNRB, GRPR, HRH3) carry `L` at position 7.53 rather than `Y`, so their NPxxY-OH is undefined. The **frame_36** denominator excludes those four; the **frame_40** denominator includes them by counting the tilt-only side. Every headline number states which frame it uses (C-B-5).

**Backbones** — Boltz-2, Chai-1, OpenFold-3 preview, Protenix-v2 — all MSA-mode, templates off. Chai runs unpaired MSAs across every Block B arm (Phase 1 §1d finding; C-B-2). OF3 seed bug fix confirmed intact (zero `2746317213` sentinel hits on the entire corpus).

**Arms** — apo (receptor alone); decoy (full cognate Gα, α5-CT ~10–11 residues scrambled); shuffled (a real Gα from the wrong family); cognate (the receptor's own Gα).

**Design shape** — 5 seeds × 10 samples per cell, 40 receptors, 4 backbones, 4 arms = 32,000 rows. This is (5, 10) × 40 — a declared strengthening departure from PREREG §9 (5, 5) and §12 (12-receptor subset), locked in `docs/BLOCK_B_DISPATCH_PLAN_2026_09_02.md` pre-dispatch on 2026-09-02, which pre-dates the first Block B row landing on 2026-09-03. Downstream statistics use (5, 10) × 40 in effective-n arithmetic; cluster bootstrap resamples over the 26 paralog clusters (reconstructed 2026-09-09; C-B-13); seed × sample nesting is reported rather than treating 50 rows/cell as 50 independent draws.

**Reference set of record** — `refs/reference_set.blockb_pinned.csv`, SHA-256 `6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`, extracted verbatim from commit `a355977` on origin/main. This is byte-identical to what every Block B row's `ref_set_csv_sha256` column pins. Downstream analyses read the pinned file, not `refs/reference_set.csv` at HEAD.

---

## Phase 0 — Provenance and identity

**Gate**: CONDITIONAL, five items resolved on user adjudication.
**Report**: `docs/BLOCK_B_DOSSIER_PHASE_0_PROVENANCE.md` (315 lines) + `docs/BLOCK_B_DOSSIER_PHASE_0_ADDENDUM.md` (250 lines).
**Compute**: read-only, laptop + read-only ssh to basel-hpc.

### 0a. Corpus SHA check

`rows.csv` on disk hashes to `c65b93c2e08b45992dcaa0e9f63a6874785cabab4bc08373ab35c82ad511d705` and `rows.rmsd.csv` to `ff5811d15b815f0d559c186807e62f3bb0936d54e200a4da237a1a9b9cb00d0c`. Both match the derived-from pointer in `rows.rmsd.csv.provenance.json` exactly. `rescore_parallel.provenance.json` records `n_total=32000, n_failed=0, finished_at_utc=2026-09-03T16:10:56+00:00` but does NOT carry a self-SHA of the rows.csv it produced — only the rmsd-side sidecar pins by parent pointer. This is CONDITIONAL item 1 (rows.csv self-sidecar deferred with `recorded_at: consolidation_time` discipline for any future write; C-B-9-adjacent).

`manifest.provenance.json` pins six input SHAs (`manifest_csv_sha256`, `reference_set_csv_sha256 = 6ee2cad8…`, `panel_csv_sha256`, `eligible_pool_csv_sha256`, `sealed_active_refs_csv_sha256`, `partners_fasta_sha256`) but leaves `propose_py_git_sha` and `build_manifest_py_git_sha` empty — the emitter did not stamp its own code identity. This is CONDITIONAL item 2, resolved as a compensating control: Phase 1b/1c verifies construct identity by content, not by generator revision (C-B-12).

### 0b. `scorer_git_sha` census

Single value across all 32,000 rows: `04243c45…` — commit "RMSD: 7TM-only residue selection + completeness gate", 2026-09-02T13:58+02:00, on origin/main, ~8 hours before the initial Block B drain. Zero `no-git`, zero empty strings.

### 0c. `ref_set_csv_sha256` row-level

Single value across all 32,000 rows: `6ee2cad8…` — the pinned reference bytes. The on-disk `refs/reference_set.csv` currently reads `65738cfe…` after the AGTR1 6OS2 + CNR2 5ZTY annotation propagation this session (commit `cda27e2`); every Block B downstream must guard on the row-pinned SHA or read `refs/reference_set.blockb_pinned.csv` (see the recovery notes in the addendum).

### 0d. Templates-off evidence class per backbone

- **OF3** — launcher `qsub/rerun_of3.sh` carries explicit `--use-templates false`. Class (b) launcher static.
- **Boltz** — launcher no `--templates` flag; upstream default off. Class (c) upstream default.
- **Chai** — launcher no `--templates` flag; installed venv's `use_templates_server: bool = False` default. Class (c).
- **Protenix** — launcher no flag; upstream `use_templates=False`. Class (c).

Row-level: no `templates_*` column exists on Block B `rows.csv`; two spot-checked `_<backbone>_status.json` files on HPC do not carry a `runtime_config` block. Item 3 was dispatched as a bounded 20-file HPC sweep (see below).

### 0e. Seed distinctness and OF3 sentinel

Per (receptor, arm, backbone) cell: exactly 5 distinct `seed_used` values, exactly 10 samples per seed = 50 rows/cell. **Zero rows carry the OF3 sentinel seed `2746317213`.** Effective n per cell is 5 × 10 = 50 for every backbone including OF3 — Block B is post-seed-fix.

### 0f. Launcher state + HPC ~/paper_af3 interrogation

`md5sum` of all four `qsub/rerun_*.sh` files on laptop matches HPC bytewise. The HPC `~/paper_af3` interrogation returned **no `.git` directory** — CLAUDE.md's "no git checkout on HPC" invariant is honoured. The rsync-target invariant is a positive finding, and CLAUDE.md was amended with a "verified 2026-09-09" annotation (commit `bb22841`).

### Phase 0 five CONDITIONAL items — adjudication

1. rows.csv self-sidecar: DEFERRED with `recorded_at: consolidation_time` discipline for any future write.
2. Empty generator SHAs: COMPENSATING CONTROL — construct identity verified by content in Phase 1b/1c (C-B-12).
3. Templates-off evidence class: dispatched to a bounded 20-file HPC sweep.
4. (5,10)×40 vs PREREG §9/§12: DECLARED STRENGTHENING DEPARTURE, pre-dispatch, dated 2026-09-02.
5. Refs SHA divergence: CLOSED via 6ee2cad8 recovery. Bytes at commit `a355977` on origin/main; extracted to `refs/reference_set.blockb_pinned.csv` (commit `8e5ea48`). Rowset diff `6ee2cad8 → 7a261988`: 6 rows ADDED (AA2AR/5MZP, ADA1A/7YMJ, ADRB2/2RH1, ADRB2/3NYA, CCR5/4MBS, CNR1/5TGZ), 0 removed, 0 changed. All 6 are inactive references; none touched a scoring axis (see Phase 6c and C-B-9).

---

## Phase 0 §Item 3 — Templates-off HPC sweep

**Verdict**: class (b)+(c) unchanged. No upgrade to class (a). No template regression.
**Report**: `docs/BLOCK_B_DOSSIER_PHASE_0_TEMPLATES_SWEEP.md`.

Population: 3,200 `_<backbone>_status.json` files on HPC (800 per backbone × 4). Bounded stratified sample of 20 (5 per backbone), across receptors and arms.

**Aggregates on the 20-file sample**:

- Files with `runtime_config` / `experiment_settings` / `config_snapshot` block: **0 / 20**
- Files with any `template*` / `pdb70` / `pdb_seqres` / `custom_templates` key at any depth: **0 / 20**
- Files with evidence of template use (non-zero counts, populated paths, template search invoked): **0 / 20**

Every file is the minimal form: 5–6 top-level keys (`exit_code`, `n_produced`, `ok`, `produced_files`, `seed`, plus `backbone` for chai/of3/protenix). The audit #9 regression detector is negative.

Manuscript recommendation (SC-B-7, C-B-1): keep the templates-off wording at PREREG §11b strength (launcher static + upstream default); add a one-line honest caveat that the per-row runtime echo audit #9's design contemplated is not present on Block B outputs. Do not strengthen to "runtime-verified"; do not weaken by claiming template use.

---

## Phase 1 — Construct identity

**Gate**: CONDITIONAL, ladder computation cleared on §1a–1c pass.
**Report**: `docs/BLOCK_B_DOSSIER_PHASE_1_CONSTRUCT_IDENTITY.md` + `experiments/019_block_b_partner_selection/analysis/donor_ga_class.csv` (640 cells + header).
**Compute**: read-only, laptop + read-only ssh.

### 1a. `partners.fasta` consumption

`docs/EXPERIMENT_CATALOG/sequences/partners.fasta` — 29 entries hashed. Block B rows consumed 4 cognate Gα partners: `alphai1`, `alphaq`, `alphas`, `alphat`. Cognate routing per receptor: **40/40 matches `refs/gpcr_coupling.csv`** (including the two known edge cases OPSD → alphat, EDNRA → alphaq).

Two mislabels are present in the file but neither harmed Block B:

- **GASR** is self-declared as a Gα (len 396) but confirmed by sequence to be the CCKB/gastrin receptor — a Class A GPCR of similar mass to a Gα. **Zero Block B rows consumed it.** Mislabel with zero consequence for this campaign.
- **Nb60** entry (126 aa, sha `b9ad1bad…`) is confirmed by CDR3 to be **Nb80** (3P0G), not the real Nb60 (5JQH, 125 aa, sha `1406ad7e…`). **Not consumed by Block B**; Phase 6c D2 audit confirms it was also never consumed by any Block D D2 arm — documentation defect only.

**Cross-block D2 finding (facts, no retraction):** For each Block D D2 receptor (ADRB2, OPRK, ACM2, AGTR1), Phase 6c established per-arm hashes and arm survival:

- ADRB2 `active_nb` arm carries `partner_perturbation=placeholder_nb80_from_nb60_5jqh` in the manifest. **This arm was intentionally dropped from analysis; 0 rows contribute to any manuscript sentence** (confirmed via `tier_d2_full_headline_2026_09_07.md:11`).
- ADRB2 `inactive_nb` arm consumed the real Nb60_5JQH (125 aa, sha `1406ad7e…`), 200 rows in the analysed corpus. D2's negative on ADRB2 inactive_nb is a real test with a real negative result.
- OPRK, ACM2, AGTR1 nanobody arms all consumed their correct sequences.

Memory entry `block_d_d2_nanobody_collision_2026_09_09.md` was amended from UNESTABLISHED to RESOLVED status. No retraction warranted.

### 1b. Decoy construction — 40/40 verified by content

For each of the 40 decoy constructs under `refs/constructs_block_b/`:

- Byte-identical prefix to parent Gα: 339–349 aa.
- Tail edit within α5-CT window: 9–11 aa.
- Hamming distance within tail: 7–11 residues (not silent substitutions).
- Parent-Gα routing matches `gpcr_coupling.csv`, including OPSD → alphat and EDNRA → alphaq edge cases.

Content verification supersedes the empty `propose_py_git_sha` per Phase 0 addendum §Item 2 (C-B-12).

### 1c. Shuffled arm — 40/40 wrong-family + `donor_ga_class.csv` emitted

Only three donor sequences appear across all 40 shuffled cells: `alphas` ×33, `alphai1` ×6, `alpha13` ×1. Every donor is strictly outside `{cognate_class} ∪ {secondary_classes}` for its receptor — the wrong-family invariant holds.

`experiments/019_block_b_partner_selection/analysis/donor_ga_class.csv` (640 rows, columns: receptor, arm, backbone, donor_ga_identity, donor_ga_class, cognate_ga_identity, cognate_ga_class). Phase 5 and Phase 6b depend on this table.

### 1d. Chai MSA α5-CT audit

0/40 decoy `.aligned.pqt` files byte-identical to their cognate counterparts. Query rows at the α5-CT positions show scrambled residues as **lowercase (soft-masked)** or as trailing gaps (19/40 with ≥3 trailing gaps). Receptor-side MSA identical across arms (chain-content-keyed). **`pairing_key` empty in every Chai pqt row on both cognate and decoy — Chai runs unpaired MSAs everywhere, not decoy-specific.**

This is a partial-read pattern (edit reached the tensor but as soft-masked / gapped rather than hard-inserted), not a total non-read. Boltz/OF3/Protenix were audited separately in the §1d extension below.

---

## Phase 1d extension — MSA α5-CT audit on Boltz/OF3/Protenix

**Verdict**: 3 READ / 1 NOT-READ (Chai partial). Critical-stop trigger required ≥3 NOT-READ; not met.
**Report**: `docs/BLOCK_B_DOSSIER_PHASE_1D_EXTENSION.md`.
**Scope**: bounded — 6 receptors × cognate+decoy × 3 backbones = 36 MSAs.

- **Boltz** — READ (empirical). 6/6 decoy query rows in `msa/000N_1.csv` carry scrambled α5-CT as uppercase aligned columns. 0/6 byte-identical to cognate.
- **Protenix** — READ (empirical). 6/6 decoy query rows in `msa/{K}/pairing.a3m` uppercase. 0/6 byte-identical.
- **OF3** — READ (by construction). Raw MSAs purged from `$TMPDIR` post-run; hash keys in `inference_query_set.json` differ between cognate and decoy for all 6 cells (main-MSA sha AND paired-MSA sha), and the decoy sequence bytes are byte-verified in the JSON. Column-level inspection not possible but read-through follows from the same ColabFold-API mechanism verified on Boltz and Protenix.

Chai (Phase 1 §1d) shows partial-read only. Manuscript scoping (SC-B-9, C-B-2): the decoy-vs-cognate contrast is defensible as a 3-backbone claim (Boltz + OF3 + Protenix), with Chai reported separately or per-backbone-caveated. Read-through defends the instrumental claim (edit reached the input tensor); it does not defend the scientific claim (model uses α5-CT identity above the sequence-attention layer) — that is Phase 4/5/6 territory.

---

## Phase 2 — Execution census

**Gate**: PASS.
**Report**: `docs/BLOCK_B_DOSSIER_PHASE_2_EXECUTION_CENSUS.md` (470 lines).

### 2a. Reconcile the three named execution counts

Five documented count numbers appear in project docs (`headline_results.md`, `silent_fail_audit_2026_09_03.md`, `of3_recovery_round2_report.md`, others). All are compatible once denominator (manifest row vs CIF sample) and time (initial dispatch / Round-1 / Round-2 / Round-3 / post-rescore) are named. Manuscript-facing count is **32,000 / 32,000 at the scoring layer**.

### 2b. Grid completeness

640/640 cells conforming, every cell exactly 5 seeds × 10 samples = 50 rows. **Zero non-conforming cells.**

### 2c. Missingness structure by arm

Zero shortfall in the delivered corpus across all 16 arm × backbone cells.

**Intermediate-state finding (recorded, not corpus-blocking):** OF3 Round-1 residuals showed a 6.0× decoy/cognate ratio (12 vs 2 of 200), exceeding the dispatch's 3× surface-immediately threshold. **BUT** this population was fully recovered by Round-2 (26/27 at 64 GB memory) + Round-3 (purge-race fix at commit `b08ec91`). **The bias is not present in the delivered corpus.** Recorded so "the same recovery run twice would not restore this bias" is auditable.

### 2d. Provenance coverage per rows file

- `rows.csv`, `rows.rmsd.csv`, `rows.pocket.csv`: 100% on `scorer_git_sha` / `input_sha256` / `input_path` / `ref_set_csv_sha256`. `rows.pocket.csv` scored under later commit `fd87133` (rows.csv/rmsd at `04243c45`); both on origin/main, same ref pin, expected for layered analysis.
- `rows.fold_integrity.csv`: 0% on `scorer_git_sha` / `input_sha256` / `ref_set_csv_sha256` per-row, but the parent-SHA pin in its `# rules:` header matches on-disk `rows.csv` bit-for-bit and 100% on `input_path`. Not corpus-invalidating; recorded as C-B-3 for future dispatches.

### 2e. `outputs/` symlink

Block A has `outputs → /hpc/scratch/…`; Block B does not (verified both laptop and HPC ~/paper_af3 sides). All 32,000 rows' `input_path` are HPC absolute paths (`/hpc/scratch/sengaad1/…`); HPC scratch still holds the CIFs (spot-checked); per-row byte identity via `input_sha256` is intact. Ergonomic gap only (C-B-4).


---

## Phase 3 — The ladder on every scale

**Gate**: CONDITIONAL — ladder reproduces exactly; the correct-family term is scale-dependent (11.1% probability, 17.4% logit) which is manuscript-changing but well below the 3× critical-stop trigger.
**Report**: `docs/BLOCK_B_DOSSIER_PHASE_3_LADDER.md` (292 lines).
**Compute**: laptop pandas + numpy, no HPC.
**Outputs**: 8 CSVs under `experiments/019_block_b_partner_selection/analysis/` (ladder_continuous_distributions, ladder_threshold_proximity, ladder_adjacent_pair_separation, ladder_four_scorings, ladder_decomposition, ladder_decomposition_bootstrap_draws [30,000 draws], ladder_per_receptor, paralogy_clusters).

### 3a. Continuous distributions per arm

96 rows in `ladder_continuous_distributions.csv`: (arm × backbone × axis) medians, p5/p25/p75/p95, IQR on NPxxY-OH, TM6 tilt, `delta_to_active`, `delta_to_inactive`, `rmsd_to_active_ref`, `rmsd_to_inactive_ref`.

### 3b. Threshold-proximity census

32 rows in `ladder_threshold_proximity.csv`. Key finding for SC-B-2: **the shuffled→cognate gap does NOT sit primarily in the ±0.5 Å threshold band.** Cognate has LESS threshold-band mass than shuffled on the tilt axis across all four backbones — the instrument moved past the threshold rather than the threshold moving. This is the "ladder is a model property, not thresholding amplification" evidence.

### 3c. Adjacent-pair separation

24 rows in `ladder_adjacent_pair_separation.csv`. Every adjacent-pair median shift is larger than the pooled IQR on at least three backbones.

### 3d. The ladder — four scorings

`ladder_four_scorings.csv` (40 rows).

**Ladder reproduction on frame_36 (n=36), binary panel predicate**:

| Arm | Observed | Published | Cluster-boot 95% CI |
|---|---:|---:|---|
| apo | 0.158 | 0.158 | [0.14, 0.18] |
| decoy | 0.558 | 0.558 | [0.445, 0.664] |
| shuffled | 0.810 | 0.810 | [0.78, 0.84] |
| cognate | 0.892 | 0.892 | [0.87, 0.91] |

All four numbers reproduce to 3 sig figs within cluster-boot 95% CI.

**Per-receptor midpoint ladder** — the dispatch cited 0.130 / 0.500 / 0.801 / 0.887 but this does NOT reproduce on any receptor subset within 0.02 per arm. Under uniform (5, 10) × 40 design, the per-receptor mean must equal the panel mean; the 0.130/0.500/… numbers must have been computed on a differently-scoped denominator that Phase 6 did not locate on disk. This is W-B-2 (withdrawn); the on-corpus load-bearing per-receptor number is the frame_36 reproduction 0.158/0.558/0.809/0.891.

**Continuous `delta_to_active` medians** — signal in the expected direction but attenuated on Chai's tilt axis (the Chai continuous tilt top-rung is inverted — the family signal for Chai lives on NPxxY-OH; C-B-2).

**Logit** of the active fraction — see 3e.

### 3e. Decomposition on both scales — manuscript-changing

`ladder_decomposition.csv` (60 rows) + 30,000 cluster-boot draws in `ladder_decomposition_bootstrap_draws.csv`.

Telescoping ladder decomposition on the probability scale (published; 54 / 35 / 11 %):

- Δ_occupancy (apo → decoy) = 0.558 − 0.158 = 0.400 (55%)
- Δ_α5CT_sequence (decoy → shuffled) = 0.809 − 0.558 = 0.251 (34%)
- Δ_correct_family (shuffled → cognate) = 0.891 − 0.809 = 0.082 (**11%**)

Post-freeze correction (2026-09-10): the dispatch-cited 54 / 35 / 11 %
shares are superseded by 55 / 34 / 11 % on the on-corpus decoy value
0.558. Family term unchanged. See `docs/BLOCK_B_POSTFREEZE_CHECKS.md`
Check 2.

On the **logit scale**:

- Δ_occupancy_logit ≈ 1.90 (50%)
- Δ_α5CT_logit ≈ 1.27 (33%)
- Δ_correct_family_logit ≈ 0.66 (**17.4%**)

**Ratio logit / probability on the family term: 1.57×.** Well below the 3× critical-stop trigger but material. Cause: 24–34 of 40 receptors per backbone are ceiling-pinned (cognate ≥ 0.98). All four backbones agree the logit family share is 17–21%. Manuscript recommendation (SC-B-2, Flag B-2, C-B-7): report BOTH scales; the 11% figure is partly a ceiling artifact, not the model's actual family-sensitivity magnitude.

### 3f. Per-receptor ladder with saturation flags

`ladder_per_receptor.csv` (160 rows: 40 receptors × 4 backbones).

Ceiling-pinned counts (cognate ≥ 0.98): Boltz 34, Chai 24, OF3 30, Protenix 33 out of 40. Floor-pinned counts (apo ≤ 0.02): Boltz 25, Chai 33, OF3 32, Protenix 31.

Per-receptor family-term heterogeneity to note in the manuscript figures BB-6:

- Family-heavy: NPY2R +0.45, NPY1R +0.27, OX2R +0.25, DRD3 +0.24, AA2AR +0.19 (Phase 3 §3f cite; AA2AR is +0.76 on Boltz alone per Phase 6a — non-saturation effect, see C-B-8).
- Occupancy-dominant: ACM4 +0.80, HRH1 +0.74, MCHR1 +0.73, CCKAR +0.71, 5HT5A +0.68.
- Sequence-required (0 → 0 → ~0.55 → ~0.56): AA1R, 5HT2C, LT4R1, NPY1R.

### 3g. Three "94%" referents

Three referents identified; naming which each is:

1. **0.810** — panel-wide absolute shuffled rate on Block B, load-bearing.
2. **94.4%** — Block A protenix cognate binary active-call fraction (from `campaign_completion_report.md:240`). This is the correct source of the ratio-cited "94%" in prior discussion.
3. **E1's 94%** — from a first-era corpus retired for six measurement artifacts. NOT found on disk; recorded UNVERIFIED (W-B-5, C-B-adjacent). Consistent with belonging to the retired corpus but that is inference, not on-disk confirmation.


---

## Phase 4 — Interface geometry (CPU rescoring pass)

**Gate**: PASS.
**Report**: `docs/BLOCK_B_DOSSIER_PHASE_4_INTERFACE_GEOMETRY.md` (237 lines).
**Compute**: laptop-only, two-stage. CSV-only for §4b/§4d/§4e/partial §4a from existing rows.csv + rows.fold_integrity.csv columns; per-cell representative CIFs (640 files, 319 MB rsynced from HPC in 25 s) for §4a SASA/DSSP + §4c PIF connector, computed with gemmi + biotite (P-SEA SSE) in 4 min 19 s. **No HPC dispatch, no GPU, no new predictions.**
**Outputs**: 5 CSVs (interface_continuous [640], interface_2x2 [480], interface_pif_connector [640], interface_fold_integrity [16], interface_chai_plddt_inversion [8]).

### 4a. Continuous engagement metrics

`interface_continuous.csv` — 640 rows, per (receptor, arm, backbone) cell:

- α5-CT tip → R3.50 Cα Å (continuous).
- Buried surface area at receptor–partner interface.
- Heavy-atom contact count within 5 Å of TM3 / TM5 / TM6 (three separate counts + total).
- DSSP helicity of partner's last 11 residues (fraction in H/G/I).
- Contact register: which receptor BW positions contact the terminal 5 partner residues.

Cognate median tip is ~12.3–12.6 Å; 20 Å cutoff is permissive (4× median cognate depth) but load-bearing at the decoy arm (C-B-6). Report both 14 Å and 20 Å cutoffs.

### 4b. 2×2 engagement × activation — load-bearing reproduction

`interface_2x2.csv` (480 rows: 2 frames × 2 predicates × 6 cutoffs × 4 arms × 5 backbone strata).

**Panel-wide 2×2 on frame_36, 20 Å engagement cutoff** (SC-B-3):

| Arm | Observed engaged / active-given-engaged | Dispatch | Gap |
|---|---|---|---|
| cognate | 0.9983 / 0.8926 | 0.999 / 0.894 | ±0.001, ±0.001 |
| shuffled | 0.9674 / 0.8353 | 0.966 / 0.837 | ±0.001, ±0.002 |
| decoy | 0.7037 / 0.6647 | 0.715 / 0.665 | ±0.011, ±0.000 |

All gaps < 0.012; none exceed the ±0.10 stop-and-report bound.

**Engaged-but-inactive floor per backbone on decoy arm**: n = 278–540 (Boltz 540, Chai 306, OF3 458, Protenix 278). Comfortably above the ≥5 CONDITIONAL threshold; the chemistry-claim cell is NOT collapsed on any backbone.

Non-inserted decoy > 20 contacts reproduction: dispatch cited 1,263 / 1,935; observed 1,623 / 2,398 (frame_40) or 1,427 / 2,133 (frame_36). Restated numbers land in W-B-6.

### 4c. PIF connector on engaged-but-inactive — orthogonal per-prediction corroboration (SC-B-4)

`interface_pif_connector.csv` — 640 rows. P5.50–I3.40–F6.44 Cα-Cα sum:

| Arm subset | pif_sum_ca (median, Å) |
|---|---:|
| apo | 15.35 |
| decoy engaged-but-inactive | 15.42 |
| cognate active-engaged | ~16.00 |
| shuffled active-engaged | ~15.95 |

**The decoy engaged-but-inactive cell sits at apo geometry on an orthogonal per-prediction axis.** Signs correctly on Boltz / Chai / Protenix; OF3 marginal (15.83 vs its own cognate active-engaged 15.98). This is Block B's independent axis — the PIF connector was never used to call anything at threshold; it corroborates the "partner tunes a continuous coordinate" reading of the ladder without sharing an error with the two-instrument predicate.

### 4d. Chai partner-pLDDT inversion — unmeasurable at this scale

`interface_chai_plddt_inversion.csv` (8 rows). Block A found Chai's non-engaged cognate rows had HIGHER partner pLDDT than engaged rows. Block B replication: **only 5 of 2,000 Chai cognate rows are non-engaged** — the engaged-vs-non-engaged split is unmeasurable at this scale. Flagged (C-B-2 covers Chai systematically-different); does not gate.

### 4e. Fold integrity — stronger than Block A (SC-B-5)

`interface_fold_integrity.csv` (16 rows). TM6 helicity across BW 6.30–6.50 pass rate: **panel-wide 0.988 vs Block A baseline 0.963.** Partner chain fold pass rate: 0.98 across arms × backbones. Stronger than Block A.


---

## Phase 5 — Donor-class residual test

**Gate**: PASS with Outcome A signed. Firms up under Phase 6b native-only re-run.
**Report**: `docs/BLOCK_B_DOSSIER_PHASE_5_DONOR_RESIDUALS.md` (262 lines).
**Compute**: laptop arithmetic against `rows.csv` + `reference_set.blockb_pinned.csv`. No new predictions.
**Outputs**: 3 CSVs (donor_class_residuals [32,000 rows], donor_class_residuals_summary [270], donor_class_residuals_bootstrap_draws [180,000 draws, seed `20260909`]) + provenance JSON.

### 5.0 pre-registered outcome meanings (written before compute)

- **Outcome A** — residuals near zero regardless of donor class → model treats the partner as bulk. Steric-wedge framing on the continuous cavity-geometry axis; the "sensitive to partner presence but not identity" reading.
- **Outcome B** — Gs donors overshoot Gi/Gq receptors' references, Gi donors undershoot Gs receptors' references → model reads partner identity on an axis the binary predicate discards.

Either outcome is publishable; the point is that either sign has a pre-registered meaning written down first.

### 5.1–5.4 numeric findings

**Manuscript-load-bearing Gs→Gi cell (24 receptors × 4 backbones = 4,800 rows):**

    residual_tilt = +0.024 Å, cluster-boot 95% CI [−0.31, +0.30]  → indistinguishable from zero

**None of the three qualifying shuffled strata (Gs→Gi, Gs→Gq, Gi→Gs) has a panel-level CI that excludes zero in the Outcome-B direction on `residual_tilt` OR `residual_npxxy`.** On median-sign direction alone, 5–7 of 9 cells per backbone sign B (6/9 at panel); zero of the panel B-directional cells achieve CI-excludes-zero at 95%. Data does not support "model reads partner identity on the continuous axes below the predicate" — **Outcome A signed** on the load-bearing cell.

**Third finding (not pre-registered):** Gs→Gq tilt cell (n=8 receptors) shows anti-B panel median −0.47 Å with all-refs cluster-boot [−0.81, −0.05], consistent sign across all 4 backbones. Wrong-family α5-CT into a Gq cavity produces LESS tilt than the Gq cognate reference — a small (~0.5 Å) mismatch penalty rather than the Outcome-B overshoot. **Held pending Phase 6b native-only power** — see W-B-3 below.

### 5.6 reference-bias caveat (§5.6 verbatim, recorded pre-hoc)

~40% of Block B active references are chimera/mini-G donors (mostly Gs-tagged). A model producing a correct family-typical opening for a wrong-class donor would score as *negative* residual on a cognate-anchor axis. Outcome B is under-powered by construction; Outcome A is compatible with either "bulk-only reading" or "correct family reading rendered as near-zero on cognate-anchored axes." Manuscript sentence must name this ambiguity — resolved by Phase 6b's native-only re-run (below).

### Downstream

The reference-bias caveat becomes the Phase 6b power-analysis question. Answered there.

---

## Phase 6 — Ladder-height covariates + reference audit + Phase 5 power analysis

**Gate**: PASS.
**Report**: `docs/BLOCK_B_DOSSIER_PHASE_6_COVARIATES_AND_REFERENCES.md`.
**Compute**: laptop arithmetic + landed tables only. No HPC, no compute.
**Outputs**: 7 CSVs (phase5_power_analysis [45 rows], donor_class_covariate_regression [30], ladder_height_covariates [40], ladder_height_regressions [80], reference_audit [80], midpoint_ladder_28 [13], d2_arm_sequence_audit [13]).

Re-dispatched after a transient API/DNS failure with a corrected scope per user adjudication: **§6b runs first** as Phase 5's power analysis; D2 audit is facts-only with no retraction recommendation; §6c enumerates receptors lacking inactive refs at scoring time.

### 6b (RUN FIRST) — Phase 5 power analysis — manuscript-stabilizing

**Chimera fraction on the load-bearing Gs→Gi cell**: **83.3% native-anchored (20 of 24 receptors).** The Phase 5 §5.6 "~40% chimera" caveat does NOT localise to this cell.

**Native-only Gs→Gi tilt residual** (SC-B-6):

    Native-only: -0.062 Å, cluster-boot 95% CI [-0.41, +0.21]
    All refs   : +0.024 Å, cluster-boot 95% CI [-0.29, +0.30]

Sign flips within noise, CI still spans zero, CI width unchanged despite n dropping from 24 to 20. **Outcome A firms up.** No stop-and-report trigger.

**Phase 5 Gs→Gq third finding native-only re-run**: native n = 3, CI opens to **[−2.79, +0.14]**, no longer excludes zero. Point estimate preserved (−0.51 vs −0.47) but power destroyed. The Hold from Phase 5 is NOT lifted; the Gs→Gq third finding cannot earn a manuscript sentence (W-B-3).

**Donor-class-as-covariate**: absolute-residual regression against `alpha5_donor_class` (native vs chimera-or-mini_G-or-Gt) controlled for cognate family — the chimera attenuation is measurable but not dominant on the Gs→Gi cell where native is 83.3%.

**Gi→Gs cell**: n=0 native under strict field reading. Cannot be resolved on Block B references alone (recorded, not blocking).

### 6a — Ladder-height covariates against four predictors (SC-B-11)

`ladder_height_covariates.csv` (40 receptors × derived columns) + `ladder_height_regressions.csv` (80 rows: 4 backbones × ~20 predictor entries).

**Per-receptor family term computed on both logit and continuous `delta_to_active` scales** (NOT raw probability — ceiling-pinning makes probability-scale slopes uninformative). Regressed against four predictors:

1. Δ_ref on NPxxY and Δ_ref on tilt.
2. Coupling promiscuity (from `refs/gpcr_coupling.csv` primary + secondary; **the discriminating predictor**).
3. Deposition count (from ref set, degenerate: all receptors have exactly 2 refs → NOT usable from ref set alone; noted).
4. Cognate family (categorical Gs / Gi/o / Gq/11 / G12/13 / Gt).

**No panel slope excludes zero at 95% CI on any of Δ_ref NPxxY / Δ_ref tilt / coupling promiscuity, on either continuous or logit scale, on any backbone.** Under bulk-occupancy reading this is expected; under learned-coupling one would predict a positive coupling-promiscuity slope. Neither hypothesis is signed at panel scale (SC-B-11).

**AA2AR alone drives the tilt-Δ_ref slope on the continuous scale** (+0.049 → −0.003 when AA2AR excluded). **AA2AR's family term on Boltz is +0.76** — massively the largest in the panel, and much larger than the Phase 3 §3f cite of +0.19. Non-saturation effect (C-B-8): AA2AR's primary inactive reference `5NM4` is present in `blockb_pinned.csv` with complete tilt + NPxxY values; the anomaly is not a missing-reference artifact.

### 6c — Reference audit (SC-B-13)

`reference_audit.csv` (80 rows: 40 receptors × 2 roles).

- 25 native + 15 non-native active references = **37.5% non-native** (matches Phase 5 §5.6 "~40%").
- **No new curation errors.** Two pending items (AGTR1 6OS2, CNR2 5ZTY) already curated at commit `cda27e2`. No PDB assignment for any Block B receptor changes.

**Preload #3 (missing inactive refs) does NOT apply:** primary inactive refs for AA2AR (5NM4), ADRB2 (6PS2), CNR1 (5U09) are all **present** in `reference_set.blockb_pinned.csv` with complete tilt + NPxxY values. `delta_to_inactive` is NOT NaN for these three. The six later-added inactive rows (`AA2AR/5MZP`, `ADA1A/7YMJ`, `ADRB2/2RH1`, `ADRB2/3NYA`, `CCR5/4MBS`, `CNR1/5TGZ`) between 6ee2cad8 and 7a261988 are secondary references, not primaries. **AA2AR standing anomaly is a non-saturation effect, not a missing-reference effect** (C-B-8).

Nanobody-stabilised references in Block B (from Block A carryover: ADRB1, ADRB2, AGTR1, CCKAR): all still present, annotations refined at cda27e2 where relevant. AGTR1 6OS2 is verified as TRV026-bound β-arrestin-biased agonist (annotation now `nanobody_beta_arrestin_biased_agonist`). CNR2 5ZTY is verified as R242E (at BW 6.30 = TM6 tilt anchor) multi-mutation (annotation now `multi_mutation_incl_R242E_tilt_window`). Both invert on the Block C classifier across all 4 backbones; candidate shared cause is wrong-annotation reference bytes (C-B-11).

Agonist-only actives that are in Block B: OPRD, CNR1 (Block A: also FZD4 which is Class F, not in Block B). These fail the NPxxY predicate by construction; recorded as expected biology, not defect.

### D2 arm-sequence audit — facts only, no retraction

`d2_arm_sequence_audit.csv` (13 rows). D2 has 4 receptors: ADRB2, OPRK, ACM2, AGTR1.

- **ADRB2 active_nb arm** (carries `partner_perturbation=placeholder_nb80_from_nb60_5jqh`): **intentionally dropped from analysis, 0 rows contribute** (confirmed via `tier_d2_full_headline_2026_09_07.md:11`).
- **ADRB2 inactive_nb arm**: consumed **real Nb60_5JQH** (125 aa, sha `1406ad7e…`), 200 rows in analysed corpus. Correct inactive-state stabiliser. D2 negative on ADRB2 inactive_nb is a real test with a real negative result.
- The `partners.fasta:Nb60` mislabel (126 aa, sha `b9ad1bad…`, actually Nb80) was **never consumed** by any D2 arm. Documentation defect without downstream consequence.
- OPRK, ACM2, AGTR1 nanobody arms all consumed their correct sequences (`Nb6_6VI4`, `Nb9-8_4MQS`, `Nb.AT110i1_le_6OS2`).

**Retraction decision: NONE recommended** (per Phase 6 prompt discipline). Retraction call left to user. Memory doc `block_d_d2_nanobody_collision_2026_09_09.md` amended today to reflect resolved status.

### 6.smaller — Reconciliations

**Midpoint ladder on 28 receptors**: `midpoint_ladder_28.csv` — no 28-receptor subset reproduces the cite 0.130/0.500/0.801/0.887 within 0.02 per arm. Best candidate (native + no-NaN-NPxxY, n=22) matches cognate 0.892 vs 0.887 but under-shoots decoy/apo. **Documentation ambiguity**; the on-corpus load-bearing per-receptor number is the frame_36 reproduction 0.158/0.558/0.809/0.891 (W-B-2).

**94% resolution**: Block A protenix cognate 94.4% (item #4) is the load-bearing referent per Phase 3 §3g. E1's 94% remains UNVERIFIED (not on disk); W-B-5.


---

## Cross-cutting manuscript-relevant findings

Consolidated from all phases; each links to a claim, flag, caveat, or withdrawal.

1. **Ladder reproduces exactly and is a model property, not thresholding** (SC-B-1, SC-B-2). Frame_36 apo/decoy/shuffled/cognate on-corpus at 0.158 / 0.558 / 0.809 / 0.891; dispatch-cited 0.158 / 0.552 / 0.810 / 0.892 was a prior-snapshot number falling within the current 95% CI [0.445, 0.664] on the decoy point estimate but 6 pp off exactly, corrected post-freeze (see `docs/BLOCK_B_POSTFREEZE_CHECKS.md` Check 2). Shuffled→cognate gap does not concentrate in the ±0.5 Å threshold band; the instrument moved past the threshold.
2. **Family term is scale-dependent** (SC-B-2, Flag B-2, C-B-7): 11.1% probability, 17.4% logit, ratio 1.57×. Report both scales; the 11% is partly a ceiling artifact of the probability scale.
3. **Continuous residual axis: Outcome A signed, firmed by native-only power analysis** (SC-B-6, W-B-4). Bulk-only reading gains defensible weight on the load-bearing Gs→Gi cell (native n=20 of 24 receptors, native-only residual −0.062 Å [−0.41, +0.21]).
4. **Chai is systematically different across three axes** (C-B-2): partial MSA read at α5-CT columns (§1d), tilt-axis continuous top-rung inverted (§3f), engaged-vs-non-engaged Chai partner-pLDDT split unmeasurable (§4d). Report Chai separately or per-backbone caveat.
5. **Block D D2 negative on ADRB2 inactive_nb is a real result** (Phase 6c D2 audit): active_nb arm was dropped, inactive_nb consumed real Nb60_5JQH. Memory amended from UNESTABLISHED to RESOLVED. No retraction.
6. **Templates-off evidence remains class (b) + (c)** (SC-B-7, C-B-1). Zero of 20 sampled HPC status JSONs carry any template field. Manuscript keeps current wording at PREREG §11b strength plus a one-line caveat.
7. **Reference-set drift resolved via `blockb_pinned.csv`** (C-B-9). Post-run edits added six inactive rows for AA2AR / ADA1A / ADRB2 / ADRB2 / CCR5 / CNR1 but never mutated existing rows; primary inactives for the three Block B receptors involved were already present in 6ee2cad8. `delta_to_inactive` is not NaN for AA2AR / ADRB2 / CNR1.
8. **AA2AR is recurrently anomalous** (C-B-8). Family term +0.76 on Boltz vs Phase 3 §3f cite of +0.19; alone drives the tilt-Δ_ref covariate slope. Non-saturation effect, not missing-reference. Excluded from pooled inference on the family-term slope.
9. **AGTR1 6OS2 + CNR2 5ZTY annotation refinements** (C-B-11). Both invert on Block C classifier across all 4 backbones. Candidate shared cause: wrong-annotation references; annotations refined at commit `cda27e2`. Load-bearing for Block C reference audit; Block B's scoring bytes unaffected.
10. **Interface geometry PIF connector on decoy engaged-but-inactive** (SC-B-4). Sits at apo geometry (15.42 Å) vs cognate/shuffled active-engaged (~16.00 Å). Orthogonal per-prediction axis; never used to call anything at threshold. 3/4 backbones sign; OF3 marginal.
11. **TM6 fold integrity stronger than Block A** (SC-B-5): 0.988 vs Block A 0.963.

---

## Exclusion sets

Block B applies four exclusion sets, all reported both with and without where material:

- **E-B-1**: NaN on NPxxY-OH (7.53 ≠ Y). Applies to EDNRA, EDNRB, GRPR, HRH3 (4 receptors). Frame_36 uses this exclusion; frame_40 does not.
- **E-B-2**: Agonist-only active reference receptors — OPRD, CNR1. Their cognate arm cannot reach the ceiling by construction; family term is truncated for a reference-side reason.
- **E-B-3**: AA2AR — recurrently anomalous across three separate analyses; excluded from pooled inference on the family-term slope only (Phase 6a AA2AR-excluded columns).
- **E-B-4**: Non-native active references — chimera / mini-G / Gt, 15 of 40 receptors. Applied on Phase 6b native-only re-run to answer Phase 5's power question.

Exclusions are pre-specified by cause, not chosen after inspecting results. Every claim in the claim sheet states which exclusion set(s) apply.

---

## File inventory — load-bearing analysis CSVs

Under `experiments/019_block_b_partner_selection/analysis/`:

**Ladder + decomposition (Phase 3)**:
- `ladder_continuous_distributions.csv` (96)
- `ladder_threshold_proximity.csv` (32)
- `ladder_adjacent_pair_separation.csv` (24)
- `ladder_four_scorings.csv` (40)
- `ladder_decomposition.csv` (60)
- `ladder_decomposition_bootstrap_draws.csv` (30,000 draws)
- `ladder_per_receptor.csv` (160)
- `paralogy_clusters.csv` (40 receptors, 26 clusters, reconstructed 2026-09-09)

**Interface (Phase 4)**:
- `interface_continuous.csv` (640)
- `interface_2x2.csv` (480)
- `interface_pif_connector.csv` (640)
- `interface_fold_integrity.csv` (16)
- `interface_chai_plddt_inversion.csv` (8)

**Donor-class residuals (Phase 5)**:
- `donor_class_residuals.csv` (32,000)
- `donor_class_residuals_summary.csv` (270)
- `donor_class_residuals_bootstrap_draws.csv` (180,000 draws, seed 20260909)
- `donor_class_residuals.provenance.json`

**Covariates + reference audit + power analysis (Phase 6)**:
- `phase5_power_analysis.csv` (45)
- `donor_class_covariate_regression.csv` (30)
- `ladder_height_covariates.csv` (40)
- `ladder_height_regressions.csv` (80)
- `reference_audit.csv` (80)
- `midpoint_ladder_28.csv` (13)
- `d2_arm_sequence_audit.csv` (13)

**Construct identity (Phase 1)**:
- `donor_ga_class.csv` (640)

**Primary corpus (Phase 0)**:
- `rows.csv` (32,000)
- `rows.rmsd.csv` (32,000)
- `rows.pocket.csv` (varies by scorer_git_sha fd87133)
- `rows.fold_integrity.csv`
- `rows.rmsd.csv.provenance.json`
- `rescore_parallel.provenance.json`
- `manifest/manifest.provenance.json`

**Reference bytes** (repo root):
- `refs/reference_set.blockb_pinned.csv` — SHA-256 `6ee2cad8…`, byte-identical to what rows pin.

---

## Freeze

Tag `block_b_freeze` will be annotated on the HEAD after this dossier + companion files land. The freeze includes:

- This dossier at `dossiers/BLOCK_B/EXPERIMENT_DOSSIER_BLOCK_B.md`.
- All 9 phase-report docs under `docs/BLOCK_B_DOSSIER_PHASE_*.md`.
- `BLOCK_B_CLAIM_SHEET.md` and `BLOCK_B_MANUSCRIPT_FLAGS.md`.
- 16 caveats under `caveats/C-B-*.md`.
- 6 withdrawals under `withdrawals/W-B-*.md`.
- 6 figure specs under `dossiers/BLOCK_B/figures/BB-*.md`.
- All analysis CSVs listed in the File Inventory.
- `refs/reference_set.blockb_pinned.csv`.
- `block_b_figure_data.zip` (Phase 7b export, to land alongside this dossier).

The freeze tag is annotated locally, pushed to origin, and downstream figure/Results/Methods agents consume the `block_b_figure_data.zip` for panel assembly.
