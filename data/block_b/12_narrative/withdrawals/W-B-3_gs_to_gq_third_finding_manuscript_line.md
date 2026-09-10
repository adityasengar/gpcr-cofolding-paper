# W-B-3 — Phase 5 Gs → Gq third finding (−0.47 Å tilt) as a manuscript line

## Claim as previously stated

Phase 5 §5.5 surfaced a **third finding** (not pre-registered): on the
Gs→Gq shuffled cell (n=8 receptors: 5HT2A, 5HT2C, ACM1, CCKAR, GRPR,
HRH1, LT4R1, OXYR), the panel-level residual_tilt sits at **−0.47 Å
with cluster-boot 95% CI [−0.81, −0.05]**. Anti-B on sign, CI excludes
zero. The Phase 5 draft manuscript sentence read:

> "The Gs → Gq shuffled cell (n=8 receptors) shows a −0.47 Å tilt
> residual with 3 of 4 backbones signing the same direction,
> consistent with a small (~0.5 Å) family-mismatch penalty when the
> wrong-family α5-CT is inserted into a Gq cavity."

The dispatch's decision at Phase 5 close was to HOLD this line pending
Phase 6b native-only power analysis.

## Retraction

**Held. Not converted to publication.** Phase 6b §6b.2 native-only re-run:
Gs→Gq shuffled cell has 3/8 native-anchored active references (the other
5 are non-native). Under the strict `active_stabilization_source =
native` filter, n=3. Point estimate is preserved (−0.51 Å vs −0.47 Å)
but CI blows out to **[−2.79, +0.14]** and no longer excludes zero.

**The third finding does not survive native-only power analysis at 95%
CI.** Point estimate preserved; power destroyed. Hold does not convert
to publication.

## What supersedes it

Either drop the sentence entirely, or replace it with the Phase 6b
retraction wording (Phase 6 sentence-change #2):

> "The Gs → Gq shuffled cell (n=8) has 3/8 native-anchored active
> references; restricted to the native subset (n=3), the −0.47 Å point
> estimate is preserved (−0.51 Å) but CI opens to [−2.79, +0.14] and
> no longer excludes zero. The third finding does not survive
> native-only power analysis."

## Evidence

- `docs/BLOCK_B_DOSSIER_PHASE_5_DONOR_RESIDUALS.md §5.5` (original Phase 5 third finding).
- `docs/BLOCK_B_DOSSIER_PHASE_6_COVARIATES_AND_REFERENCES.md §6b.2` (native-only re-run).
- Source CSV: `donor_class_residuals_summary.csv` +
  `phase5_power_analysis.csv`.

## Related

- MANUSCRIPT_FLAGS.md Flag B-16.
- SC-B-6 (Outcome A signed and firmed on the load-bearing Gs → Gi cell).
- Not related to W-B-4: Outcome B is withdrawn on the Gs → Gi cell
  (bulk-only reading); the Gs → Gq third finding was a different
  effect (family-mismatch penalty at −0.5 Å magnitude), which is now
  held pending sufficient native references on Gq-cognate receptors.
