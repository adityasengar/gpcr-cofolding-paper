# C-B-10 — Phase 5 reference-bias caveat does NOT localise to the load-bearing Gs→Gi cell

## Caveat

Phase 5 §5.6 records the reference-bias caveat verbatim:

> Every active reference is a cognate-transducer complex. If the model
> produced a correct wrong-class complex (e.g. β2AR + Gi correctly opening
> TM6 by only ~10 Å), that structure would score as *less active than
> the reference* (β2AR + Gs opens by ~14 Å). Phase 5 residuals therefore
> understate identity sensitivity by construction. A shuffled cell that
> correctly matches its partner's family-typical opening cannot register
> as "zero residual" on the receptor's cognate-anchor axis — it can only
> register as a *negative* residual whose magnitude equals the
> family-typical opening gap.

The concern: an Outcome-A-consistent finding on the load-bearing Gs→Gi
cell could be Outcome-B-consistent-but-masked when the reference is
chimera-anchored.

## What Phase 6b actually found

**The manuscript-load-bearing Gs→Gi cell is 83.3% native-anchored**
(20 of 24 receptors have `active_stabilization_source = native`).
Native-only re-run of Phase 5 on Gs→Gi tilt:

| statistic | all refs | native only |
|---|---:|---:|
| n_receptors | 24 | 20 |
| residual_tilt median (Å) | +0.024 | **−0.062** |
| 95% CI | [-0.29, +0.30] | **[-0.41, +0.21]** |
| CI width (Å) | 0.59 | 0.62 |

Sign flips within noise, CI still spans zero, CI width unchanged despite
dropping n from 24 to 20. **Outcome A firms up rather than turning.**

Where the reference-bias caveat DOES localise:

- **Gi→Gs cell (n=5)**: 0/5 native under the strict field reading —
  cannot resolve; deferred (Flag B-27).
- **Gs→Gq cell (n=8)**: 3/8 native; third-finding point estimate
  preserved but CI blows out to [-2.79, +0.14] (W-B-3).

## Why it matters

The Phase 5 caveat is real and load-bearing at manuscript level, but
it must be reported alongside the finding that it does NOT localise to
the largest cell. Under the reference-bias caveat, the Gs→Gi ≈ 0
finding is formally ambiguous between Outcome A ("bulk-only reading")
and Outcome B ("correct family reading that renders as near-zero on
cognate-anchored axes"). **The paper should name this ambiguity.**

## Affects

- SC-B-6 (Outcome A signed and firmed).
- W-B-3 (Gs→Gq third finding).
- W-B-4 (Outcome B withdrawn).

## Manuscript sentence

> The Phase 5 reference-bias caveat — every active reference is a
> cognate-transducer complex, so a model that produces correct
> family-typical opening cannot register as unambiguously Outcome-B
> signed on cognate-anchored axes — applies at panel level (37.5% of
> Block B active references are non-native). It does NOT localise to
> the manuscript-load-bearing Gs → Gi shuffled cell: 20 of 24 receptors
> in that cell carry a native active reference (83.3%). The native-only
> Gs → Gi tilt residual is −0.062 Å with cluster-boot 95% CI [-0.41,
> +0.21] — sign flips within noise, CI still spans zero, CI width
> unchanged. Outcome A firms up on this cell, not Outcome B. The
> ambiguity between "bulk-only reading" and "correct family reading
> that renders as near-zero" remains a formal limitation of the
> Phase 5 design and is retained as a caveat in the Limitations
> section.

## Related

- MANUSCRIPT_FLAGS.md Flag B-4.
- Phase 5 §5.6 (verbatim caveat).
- Phase 6b §6b.1 (chimera fraction per stratum), §6b.2 (native-only re-run).
