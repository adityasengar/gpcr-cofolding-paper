# caveats/ (Block B)

Live limitations that were disclosed, not retracted. These belong in the
manuscript's Methods and Limitations sections — not the Results section,
not the Withdrawals section.

**Format**: `C-B-<N>_<slug>.md`. Content: what the caveat is, why it
matters, which claims it affects, what the manuscript sentence looks like.

## Distinction from withdrawals/

A **withdrawal** was believed at some point, is no longer supported, and
should not appear in the manuscript. A **caveat** is a real limitation of
a surviving claim — the claim holds under stated conditions, but the
reader needs the condition to interpret it correctly.

## Distinction from Block A caveats

Block A's caveats (paper_af3_release/caveats/C-*.md) are numbered C-1..C-12
without a block prefix. Block B's caveats use the C-B-N prefix to keep
the two archives distinguishable on-disk and in cross-references. Some
Block-B caveats are Block-B-specific (C-B-2 Chai partial MSA read;
C-B-13 reconstructed paralog cluster map); others are structurally
similar to Block A caveats (e.g. C-B-8 AA2AR anomaly ≈ Block A's AA2AR
line in Q1/E1 exclusion) but re-derived on Block B evidence rather than
inherited from Block A.

## Block B caveats

- `C-B-1_templates_evidence_class.md` — Templates-off evidence class (b) launcher static analysis + (c) upstream defaults, not (a) per-row runtime echo. 20-file HPC sample carries no `runtime_config` block.
- `C-B-2_chai_systematically_different.md` — Chai partial MSA read on decoy α5-CT (0 of 40 pqt query rows uppercase-aligned); tilt-axis inversion on top rung; pLDDT test unmeasurable on Block B.
- `C-B-3_fold_integrity_provenance_gap.md` — `rows.fold_integrity.csv` 0% per-row `scorer_git_sha` / `input_sha256` / `ref_set_csv_sha256`; parent-SHA pin in header comment.
- `C-B-4_no_outputs_symlink.md` — Block B lacks the laptop-side `outputs/` symlink Block A carries; ergonomic gap, not a provenance gap.
- `C-B-5_frame_36_vs_40.md` — Every published two-instrument Block B number uses frame_36; every published tilt-only number uses frame_40; convention must be named in every table.
- `C-B-6_engagement_cutoff_sensitivity.md` — 20 Å engagement cutoff is 4× median cognate depth; cognate p(active|engaged) flat 10–20 Å, decoy moves 0.13; report both 14 Å and 20 Å.
- `C-B-7_ceiling_pinning_on_family_term.md` — 24–34 of 40 receptors × backbones ceiling-pinned at cognate; probability-scale family term is bimodal; logit share is the interpretable statistic.
- `C-B-8_aa2ar_standing_anomaly.md` — AA2AR is anomalous by non-saturation (only receptor with unpinned shuffled + cognate on boltz), not by missing reference; excluded from pooled inference where AA2AR alone drives a slope.
- `C-B-9_scoring_time_reference_set.md` — Block B was scored against `ref_set_csv_sha256 = 6ee2cad8…`; 6 inactive rows added post-run (2026-09-06); none of the added rows shifts the primary inactive reference for any Block B receptor.
- `C-B-10_reference_bias_caveat_does_not_localise.md` — Phase 5 §5.6 reference-bias caveat (37.5% non-native panel-wide) does NOT localise to the manuscript-load-bearing Gs→Gi cell (83.3% native there).
- `C-B-11_agtr1_cnr2_annotation_refinements.md` — AGTR1 6OS2 (β-arrestin-biased) + CNR2 5ZTY (multi-mutation incl R242E at BW 6.30) annotations refined at `cda27e2` after Block B ran; no PDB moves, no numeric-column shifts.
- `C-B-12_empty_generator_shas.md` — `manifest.provenance.json` empty `propose_py_git_sha` / `build_manifest_py_git_sha`; compensating control by content (Phase 1b/1c hash checks).
- `C-B-13_paralog_cluster_map_reconstructed.md` — 26-cluster paralog map at `experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv` was reconstructed 2026-09-09; not a canonical shipped file.
- `C-B-14_no_covariate_slope_excludes_zero.md` — Ladder-height covariates (Δ_ref NPxxY, Δ_ref tilt, coupling promiscuity) have no panel slope excluding zero at 95% CI on either scale, with or without AA2AR.
- `C-B-15_class_a_only.md` — Block B runs Class A only (40 receptors); Class B and Class F not included.
- `C-B-16_of3_effective_n_asymmetry.md` — Block A OF3 rows carry constant seed (bug); Block B carries 5 distinct seeds per cell. Effective-n asymmetry ~10×; pooled A+B statistics must account.
