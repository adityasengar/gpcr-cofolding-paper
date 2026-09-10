# block_b_figure_data — self-contained data package for Block B figure making

## Corpus provenance

- Repo: `paper_af3` @ commit `04531b8328ea4a71714a1b9ed7629736ec16f55a`
- Freeze tag: `block_b_freeze` — PENDING (annotated after this zip lands).
- Row-count corpus: 40 Class A GPCR receptors × 4 backbones (Boltz-2 / Chai-1 /
  OpenFold-3-preview / Protenix-v2) × 4 arms {apo, decoy, shuffled, cognate} ×
  5 dispatch seeds × 10 samples per seed = **32,000 predictions, grid-complete
  (640 / 640 cells conforming, every cell exactly 50 rows)**.
- Row source on disk: `experiments/019_block_b_partner_selection/analysis/rows.csv`
  - SHA-256: `c65b93c2e08b45992dcaa0e9f63a6874785cabab4bc08373ab35c82ad511d705`.
- RMSD side-file: `rows.rmsd.csv`, parent-pointed to the corpus rows SHA above.
- Reference set of record: `refs/reference_set.blockb_pinned.csv`, SHA-256
  `6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef` —
  byte-identical to every Block B row's `ref_set_csv_sha256` column, recovered
  from commit `a355977` and durably archived at commit `8e5ea48`. See
  `09_references/reference_set.blockb_pinned.csv` and caveat C-B-9.
- Scoring provenance: single `scorer_git_sha = 04243c45bdd2285ca195add098a7f333a0d60476`
  across all 32,000 rows (rows.csv + rows.rmsd.csv); rows.pocket.csv scored under
  later commit `fd87133` (same origin/main, same ref pin — expected for layered
  analysis).
- Bootstrap convention: 26 paralog clusters
  (`09_references/paralogy_clusters.csv`), 1,000 resamples, seed `20260909`.
  Receptor-bootstrap CIs (40 receptors treated independent) are tighter and are
  NOT the reported primary measurement (see C-B-13).

## Generation

- Generated: 2026-09-10 UTC.
- Build scripts (dropped from the shipped zip): `_build_rows_tidy.py`,
  `_build_claim_summaries.py`, `_build_manifest.py`.

## Structure

```
block_b_figure_data.zip
├── README.md                        # this file
├── DATA_DICTIONARY.md               # every column in every CSV
├── FIGURE_BRIEF.md                  # panel → source-file map for BB-1 .. BB-6
├── MANIFEST.json                    # sha256 + size + row_count per file
├── 01_rows/                         # tidy long-format 32,000 rows + exclusion flags
├── 02_constructs/                   # decoy + shuffled construct identity
├── 03_msa_audit/                    # Phase 1d + Phase 1d-extension α5-CT column audit
├── 04_ladder/                       # ladder 4 scorings, continuous distributions, threshold proximity, per-receptor, midpoint reconstruction
├── 05_decomposition/                # telescoping ladder decomposition on both scales + 30,000 bootstrap draws
├── 06_interface/                    # continuous engagement, 2x2, PIF connector, fold integrity, Chai pLDDT
├── 07_donor_residuals/              # per-row donor residuals, summaries, 180,000 bootstrap draws, phase 5 power analysis
├── 08_covariates/                   # ladder-height covariates + regressions
├── 09_references/                   # 80-row reference audit + paralog cluster map + pinned reference bytes
├── 10_exclusions/                   # E-B-1 .. E-B-4 definitions, per-receptor membership, panel-level counts
├── 11_bootstrap_draws/              # both bootstrap-draw CSVs consolidated in one place
└── 12_narrative/                    # claim sheet, flags, dossier, caveats, withdrawals, figure specs — copied verbatim
```

## Toolchain

Single pipeline needed: **pandas + matplotlib / plotly / d3 / recharts**. Every
CSV is tidy long-format with explicit identifier columns. No CIFs, no
molecular rendering — this ships data, not structures. If a Panel needs
structural context, refer to the referenced CIF paths in the row-level
`input_path` column and pull from HPC (paths preserved verbatim per C-B-4).

## Exclusion flag semantics

`01_rows/rows_tidy.csv` (32,000 rows) carries four boolean exclusion flags
(`excl_E_B_1` … `excl_E_B_4`), an `excl_any` aggregate, and an `excl_reason`
text label. **These are flags, never applied.** Every downstream table
exposes the same 640 cells / 32,000 rows so the figure agent can toggle each
set on/off. See `10_exclusions/exclusion_definitions.csv`.

Frame convention (C-B-5):

- **frame_36** — n=36 after excluding E-B-1 (EDNRA, EDNRB, GRPR, HRH3, whose
  NPxxY-OH is intrinsically NaN because 7.53 = L not Y). **Every published
  two-instrument Block B number uses frame_36.**
- **frame_40** — n=40, naïve denominator. Reported only when explicitly named,
  and typically only for tilt-only computations.

## Class-conditional predicate (Class A)

    d_npxxy_y558_y753_oh < 9.082 Å   AND   d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å

NaN on either axis → False. Thresholds are echoed on every row in
`threshold_npxxy_oh_active_lt` and `threshold_gpcrdb_tm6_tilt_active_gt`.

## The four numbers a figure agent will get wrong without warning

1. **Family term is scale-dependent.** 11.1% on the probability scale
   [0.047, 0.125], **17.4% on the logit scale [0.39, 1.09]**, ratio 1.57×.
   Ceiling-pinning at cognate (24–34 of 40 receptors × backbones) compresses
   the probability-scale family term. When contrasting occupancy vs
   α5-CT-sequence vs family, use the logit share (17%). See Flag B-1, C-B-7,
   SC-B-2 in `12_narrative/`.
2. **Chai is systematically different on three axes.** Partial MSA read at the
   scrambled α5-CT (0 of 40 pqt query rows uppercase-aligned; Boltz/OF3/Protenix
   all 6/6); tilt-axis inversion on the shuffled→cognate rung (Chai's family
   signal lives on NPxxY-OH); Block A's pLDDT-inversion tell is unmeasurable
   in Block B (0.25 % non-engaged cognate rows). Report per-backbone, or note
   Chai's deviation in any pooled statement. See C-B-2, Flag B-2.
3. **Cluster-bootstrap CIs are authoritative.** Paralog-cluster resampling
   (26 clusters, seed 20260909) is the reported measurement. The cluster map
   was reconstructed on 2026-09-09 from standard GPCR-family taxonomy
   (`09_references/paralogy_clusters.csv`); no canonical on-disk map was found
   pre-reconstruction. C-B-13.
4. **AA2AR is recurrently anomalous.** Family term +0.76 on Boltz (vs Phase 3
   §3f cite +0.19); alone drives the tilt-Δ_ref covariate slope. Non-saturation
   effect (primary inactive `5NM4` is present and complete), not
   missing-reference. Excluded from pooled inference where AA2AR alone drives
   a slope. C-B-8, SC-B-11.

## Row counts (spot check)

- `01_rows/rows_tidy.csv`: **32,000 rows**, 640 cells × 50 rows/cell exactly.
  - E-B-1 fires: 3,200 rows (4 receptors × 800)
  - E-B-2 fires: 1,600 rows (2 receptors × 800)
  - E-B-3 fires: 800 rows (AA2AR × 800)
  - E-B-4 fires: 12,000 rows (15 receptors × 800)
  - E-B-any: 14,400 rows.
- `05_decomposition/ladder_decomposition_bootstrap_draws.csv`: 30,000 rows.
- `07_donor_residuals/donor_class_residuals_bootstrap_draws.csv`: 180,000 rows.
- `06_interface/interface_2x2.csv`: 480 rows (2 frames × 2 predicates × 6 cutoffs × 4 arms × 5 backbone strata).
- `09_references/reference_audit.csv`: 80 rows (40 receptors × 2 roles).

## Answer-beside-data discipline (13 SC-B claims)

Each directory that owns SC-B claims carries a `claim_answers.csv` with columns
`claim_id, metric, observed_value, ci_lo, ci_hi, source_file,
matches_claim_sheet_bool`. Recompute from the tidy source and diff against
these to verify each panel:

| Claim | Directory | Source CSV(s) |
|---|---|---|
| SC-B-1 | `04_ladder/` | ladder_four_scorings.csv, ladder_continuous_distributions.csv |
| SC-B-2 | `05_decomposition/` | ladder_decomposition.csv (+ bootstrap draws) |
| SC-B-3, SC-B-4, SC-B-5, SC-B-12 | `06_interface/` | interface_2x2.csv, interface_pif_connector.csv, interface_fold_integrity.csv, interface_continuous.csv |
| SC-B-6 | `07_donor_residuals/` | donor_class_residuals_summary.csv (+ bootstrap draws) |
| SC-B-7, SC-B-9 | `03_msa_audit/` | Phase 1 / Phase 1d docs |
| SC-B-8 | `02_constructs/` | donor_ga_class.csv, construct_build_report.md |
| SC-B-10 | `01_rows/` | rows_tidy.csv |
| SC-B-11 | `08_covariates/` | ladder_height_regressions.csv |
| SC-B-13 | `09_references/` | reference_audit.csv, reference_set.blockb_pinned.csv |

Spot-check reproductions were run at build time — see `MANIFEST.json` and
"Known gaps" below.

## Known gaps

- **Chai partial MSA read at α5-CT columns** (§1d). 0 of 40 decoy `.aligned.pqt`
  files carry the scrambled α5-CT as uppercase aligned columns. Decoy-vs-cognate
  contrast at the MSA-column layer is defensible on 3 of 4 backbones (Boltz +
  OF3 + Protenix); Chai reported separately (SC-B-9, C-B-2).
- **`rows.fold_integrity.csv` 0 % per-row provenance columns** — no
  `scorer_git_sha` / `input_sha256` / `ref_set_csv_sha256` per row; parent-SHA
  pin lives in the file's `# rules:` header comment (stripped on join into
  `rows_tidy.csv` — see C-B-3). Join is by `input_path` (100 % coverage).
- **No `outputs/` symlink** for Block B. Block A has `outputs → /hpc/scratch/…`;
  Block B does not. All 32,000 rows' `input_path` are HPC absolute paths;
  per-row byte identity via `input_sha256` is intact. Ergonomic gap only
  (C-B-4).
- **Missing-inactive-reference preload does NOT apply.** Primary inactives for
  the three Block B receptors intersected with the six post-run inactive-row
  additions (AA2AR / 5NM4, ADRB2 / 6PS2, CNR1 / 5U09) are all present in
  `6ee2cad8`. `delta_to_inactive` is not NaN for these three (C-B-9, SC-B-13).
- **28-receptor midpoint ladder does NOT reproduce.** The dispatch cite
  0.130 / 0.500 / 0.801 / 0.887 has no on-disk 28-receptor subset that
  reproduces it within 0.02 per arm. `04_ladder/midpoint_ladder_28.csv`
  documents the enumeration; the on-corpus load-bearing per-receptor number
  is the frame_36 reproduction 0.158 / 0.558 / 0.809 / 0.891 (W-B-2).
- **OF3 raw MSAs purged post-run.** `$TMPDIR/of3-of-sengaad1/colabfold_msas/`
  is purged after each job; column-level MSA inspection for OF3 is not
  possible after the fact. Read-through follows from the same ColabFold-API
  mechanism verified empirically on Boltz and Protenix. See
  `03_msa_audit/PHASE_1D_EXTENSION.md`.

## What Block B does NOT claim

- Prospectivity — foreclosed by design; date-stratified holdout is Block C.
- Mechanism at the residue level — Block C tier 3 territory.
- Directional control — Block D D2 territory.
- Class B / F receptors — not in Block B (C-B-15).

## Bootstrap seed / convention

- Seed: `20260909` across all bootstrap tables (both ladder_decomposition and
  donor_class_residuals). Recorded in each provenance JSON.
- Cluster count: 26 (see `09_references/paralogy_clusters.csv`).
- Draws per statistic: 1,000.

---

## What a figure agent will get wrong without warning (post-freeze update)

This section supersedes any earlier draft of the same warnings. Refreshed
after the four post-freeze checks + E1 external-ruler pass + Items 1–3
of the closeout dispatch (2026-09-10).

1. **Decoy panel rate is 0.558, not 0.552.** The older 0.552 appears in
   superseded documents (dispatch prompt, some Phase 3 report cites) and
   is a pre-consolidation snapshot value. Canonical on-corpus: 0.558.
   Downstream decomposition shares: 55 / 34 / 11 % (probability scale),
   17.4 % logit-scale family term. See `docs/BLOCK_B_POSTFREEZE_CHECKS.md`
   Check 2 and `12_narrative/BLOCK_B_POSTFREEZE_CHECKS.md`.
2. **Cluster-boot intervals are authoritative; receptor-boot secondary**
   (per Block A convention `C-8_cluster_bootstrap_authoritative.md`).
   Row-boot values (treating 50 rows per cell as 50 independent draws)
   are NOT admissible and give artificially tight CIs. The Item 2 audit
   at `11_bootstrap_draws/ci_convention_audit_readme.md` shows cluster-boot
   vs proper receptor-boot width ratios of 0.90–1.26; no SC-B claim's
   signed status changes under either convention.
3. **The family term is 11 % on the probability scale AND 17 % on the
   logit scale.** Both are correct. Panels showing the term must name
   the scale. Ceiling-pinning on 24–34 receptors per backbone drives
   the probability-scale figure down; see `C-B-7_ceiling_pinning_on_family_term.md`.
4. **Frame_36 vs frame_40 differ by 0.06–0.09 on p(active | engaged).**
   Every panel and every table row must name its frame. See `C-B-5_frame_36_vs_40.md`.
5. **SC-B-6 is Outcome A signed with a CI spanning zero — NOT an
   equivalence result.** The equivalence upgrade was attempted at r2
   (block_b_freeze_r2) and retracted at r3 after the ruler-side bootstrap
   showed insufficient power on the native-only stratum. See
   `12_narrative/BLOCK_B_POSTFREEZE_CHECKS.md` Check 1 (revised) and
   `12_narrative/BLOCK_B_FOLLOWUP_E1_E4.md`. The claim wording in
   `BLOCK_B_CLAIM_SHEET.md` § SC-B-6 is the r3 wording; use verbatim.
6. **Chai is systematically different on three axes**: partial α5-CT MSA
   read (§1d + §1d extension), tilt-axis continuous top-rung inversion
   (Phase 3), engaged-vs-non-engaged pLDDT split unmeasurable
   (Phase 4 §4d). Report per-backbone or per-backbone-caveated; never
   average Chai in silently. See `C-B-2_chai_systematically_different.md`.
7. **AA2AR is recurrently anomalous but the five appearances are
   independent, not a single structural cause.** Pocket-Cα RMSD
   1.62 Å ranks 34/40 (top third of separation, not bottom); AA2AR
   is not in the bottom-5 on any of pocket-Cα RMSD, |Δ NPxxY|, or
   |Δ tilt|. Report AA2AR-included and AA2AR-excluded numbers side by
   side for pooled inferences (C-B-8), but do not collapse the five
   appearances into one footnote — they need separate wording. See
   `12_narrative/BLOCK_B_ITEM3_AA2AR_AND_POCKET_CA.md`.
8. **Block D D2 has been RESOLVED** — the ADRB2 active_nb arm was
   intentionally dropped (0 rows); the inactive_nb arm ran with real
   Nb60_5JQH (200 rows). The D2 negative on ADRB2 inactive_nb is a real
   test with a real result. **No retraction.** Memory doc trail on the
   cross-block audit is at `12_narrative/...` and Phase 6c report.
9. **The Class A Gs Ga-complexed reference set is entirely
   mini-G/nanobody/chimera stabilised — zero native heterotrimers.**
   This is a CURATION CHOICE (Item 1 verdict, 2026-09-10): 3SN6 for
   ADRB2 exists and was not selected. Any manuscript sentence about
   "Gs-anchored reference geometry on TM6 tilt" is a claim about
   engineered constructs, not native Gs biology.
