# caveats/

Live limitations that were disclosed, not retracted. These belong in the
manuscript's Methods and Limitations sections — not the Results section,
not the Withdrawals section.

**Format**: `C-<N>_<slug>.md`. Content: what the caveat is, why it matters,
which claims it affects, what the manuscript sentence looks like.

## Distinction from withdrawals/

A **withdrawal** was believed at some point, is no longer supported, and
should not appear in the manuscript. A **caveat** is a real limitation of
a surviving claim — the claim holds under stated conditions, but the
reader needs the condition to interpret it correctly.

## Block A caveats

- `C-1_bug4_matcher_path.md` — Bug #4 (5-atom-name fast-path preempts MCS on ~2,300 rows across the campaign) — pose-accuracy claims affected on Block C tier 3, not Block A
- `C-2_class_b_tilt_ceiling.md` — Class B cognate tilt is 100% ceiling-saturated; kink is the sole discriminator
- `C-3_class_f_weak_predicate.md` — Class F tilt-only predicate has median cognate−apo shift 0.27 Å < IQR
- `C-4_chai_softness.md` — Chai is systematically softer than the other three backbones on tilt, delta_to_active, two-instrument agreement, and partner engagement confidence
- `C-5_pre_freeze_no_git_subtrees.md` — 8 subtrees (smoke_tests, diversity_pilot, chai_msa_pilots, cache_verify, timing_boltz_50_vs_200, plus A_of3_rerun) carry `scorer_git_sha=no-git` at row level; motivational not headline
- `C-6_manuscript_pdb_count.md` — the reference PDB set is 89 unique (40 unique active + 48 unique inactive + 1 sealed-active-only per SHA), not 48; state clearly

## Added post-scientific-review

- `C-7_apo_not_physical.md` — "apo" is a computational reference condition, not a physical state; direct mapping to physical basal activity is deferred
- `C-8_cluster_bootstrap_authoritative.md` — receptor-bootstrap is ~1.10× tighter than cluster-bootstrap; report cluster-boot (26 paralog clusters) as authoritative
- `C-9_prospectivity_foreclosure.md` — Block A's fraction-of-way metric requires an active reference by design; prospectivity comes from the date-stratified holdout (24–26 receptors post-2021-09-30; 11–12 receptors post-2023-01-13) and Block C tier 3, not from Block A's headline metric
- `C-10_amplitude_flatness_reaches_state.md` — model reaches active-state geometry (corroborated by P5.50–F6.44 orthogonal signature) but does NOT reproduce receptor-specific amplitude (P1b slopes far from 1, all CIs cross zero under cluster-boot); the paper's headline is state-reached, not amplitude-reproduced

## Added during freeze batch

- `C-11_construct_column_untrusted.md` — `construct` column in reference_set.csv contradicts RCSB `pdbx_mutation` on 40% of evaluable PDBs; not a wild-type guarantee across the reference set
- `C-12_broken_cell_a1a6_gap.md` — ACM1-cognate-Protenix is a 25-row broken cell (mean pLDDT 39, unfolded TM6, displaced TM7); all 25 rows pass A1–A6 because assertion suite has no pLDDT floor; E1 exclusion set
