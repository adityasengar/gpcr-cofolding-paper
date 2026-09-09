# Results — Block A (draft)

Follows the five beats of FIGURE_BRIEF §1.3. Every number traces to a file in
`data/block_a/`; `analysis/block_a/verify_claims.py` re-derives the checkable
ones. `[PI]` marks a wording decision that needs the principal investigator —
each corresponds to an entry in `DISCREPANCY_REPORT.md`.

Register is deliberately flat. Supplying a co-folding model with a G protein and
obtaining an active receptor is **not novel** (§1.5); the contribution is panel
scale, four independent backbones, a calibrated instrument, and explicit
characterisation of what fails.

---

## Beat 1 — The instrument, and its calibration as a finding

Before applying them to predictions, both measurements were run on the deposited
reference structures, where the answer is already known. Across 167 unique
reference entries the two-instrument predicate returned the expected call on 159
and deviated on **9** — five annotated active, four annotated inactive.

The deviations are informative rather than a nuisance. Several entries annotated
active were solved with an agonist bound but **no transducer**, and these never
form the NPxxY network: the hydrogen-bond arrangement requires Gα clamping, so
the predicate declines to call them active, correctly. Others reflect construct
engineering inside the measurement window rather than receptor conformation.

Five of the nine deviations are **unclassified** as to cause; the remainder split
between expected biology, curation error, a measurement artifact, and one entry
that could be either (D10). We report the unclassified fraction rather than
resolving it by assertion.

The practical consequence is that *"active structure"* is not one thing. A panel
built on the assumption that every entry annotated active is geometrically
equivalent would inherit that heterogeneity silently. **Figure BA-1.**

## Beat 2 — The main effect

Given the receptor sequence alone, predictions are predominantly inactive. Given
the receptor sequence together with its cognate Gα, they are predominantly
active. The direction is consistent on all four backbones across the 40 Class A
receptors.

| backbone | median TM6 tilt shift (cognate − apo) | 95% CI (cluster) | active, apo | active, cognate |
|---|---:|---|---:|---:|
| Boltz-2 | +5.04 Å | [3.53, 5.55] | 16.0% | 83.4% |
| Chai-1 | +1.05 Å | [0.36, 3.76] | 32.7% | 75.0% |
| OpenFold3 | +4.81 Å | [3.95, 5.21] | 24.2% | 79.9% |
| Protenix2 | +5.31 Å | [4.63, 5.74] | 14.5% | 87.1% |

The two rate columns are **pooled row-level rates**, not means over receptors;
on this panel the two agree to three decimal places except for Protenix cognate,
where the shipped value (0.871) differs from both (0.890) and is unexplained.
All intervals are cluster bootstraps over 26 paralog clusters and are the
authoritative ones (D5); the cluster interval is up to 2.2× wider than the
receptor interval, not 1.1× (D17). Chai-1 is the soft predictor throughout — a smaller
shift with a much wider interval — which recurs across metrics (C-4).

The apo arm is a computational reference condition, not a physical state: no
ligand, no membrane, no basal-activity equivalent (C-7). It should not be read as
a physiological inactive receptor.

In the cognate arm the Gα is physically docked rather than merely present: 98.2%
of samples meet the interface-contact criterion, with a median of 66
receptor–Gα contacts. **Figure BA-2.**

## Beat 3 — Independent corroboration

The obvious objection is that two thresholds were chosen and the models happened
to cross them. Predictions were therefore additionally scored on the P5.50–F6.44
PIF connector — a different structural rearrangement, in a different region,
never used to set a threshold or to call anything.

The strong result is agreement at row level. Of predictions the predicate called
active, **204 of 256 (79.7%)** fall below the reference-inactive median on the
connector; of predictions it called inactive, **205 of 256 (80.1%)** fall above
the reference-active median. The direction is the same as the references on
**all four backbones**.

The magnitude is roughly one third of the reference scale (median prediction
delta −0.56 Å against a reference delta of −1.51 Å). **The interval on that
delta, [−1.20, +0.03], includes zero**, and so do all four per-backbone
intervals. `[PI — D2]` We therefore report the connector as corroborating in
direction and in row-level agreement, and explicitly **not** as a signed
magnitude effect. The previously circulated ratio interval of [0.04, 0.77] is
computed on the absolute value of the delta and cannot cross zero by
construction; it is not evidence of sign. **Figure BA-3.**

## Beat 4 — What the models do not do

Real receptors do not all activate by the same amount. If a model had learned
activation rather than an active-looking shape, receptors whose reference
structures differ greatly should receive large predicted shifts and those whose
references differ little should receive small ones.

On the NPxxY axis — the well-powered one, with a reference separation SD of
5.22 Å — the regression of predicted shift on reference separation gives slopes
of 0.04 (Boltz-2), 0.37 (Chai-1), 0.18 (OpenFold3) and 0.26 (Protenix2) across
28 Class A receptors. **Three of four show no evidence of amplitude
reproduction. Protenix2's interval, [0.07, 0.55], excludes zero** — a weak signed
positive slope, roughly a quarter of the expected receptor-to-receptor scaling,
and far below unity. It excludes zero under all three inclusion sets, so this is
not an artefact of the restriction choice. `[PI — D1]` No backbone approaches a
slope of 1.

The tilt axis cannot answer the question at all. Its reference separation SD is
1.17 Å against NPxxY's 5.22 Å, and under Class-A restriction two of four slopes
are negative (Boltz-2 −0.30, Chai-1 −0.66). A negative slope is not physically
interpretable: it would mean a model moves receptors backwards in proportion to
how far they should move. Combined with the restricted range, this is the
signature of a predictor with essentially no dynamic range. `[PI — D3]` **We
report no tilt amplitude slope in either direction and describe the axis as
uninformative for amplitude — a property of the instrument, not a result about
the models.** **Figure BA-4.**

This is the load-bearing negative result (C-10), and it must be read alongside
the fraction in Table 2 — a median over **39** receptors, not the 40 the shipped
`n_receptors_fraction` column reports (D15). **The fraction is a mean; the regression is a
covariance.** A high mean shift with near-zero covariance against reference
separation is exactly what this corpus shows, and the two are not in conflict.

## Beat 5 — Confidence

pLDDT averaged over the whole complex is diluted by the Gα chain, by loops and by
termini. Restricted to the six state-defining anchor residues (3.50, 3.51, 5.58,
6.30, 6.34, 7.53) it carries information about conformational correctness — on
two of four backbones.

| backbone | whole-complex pLDDT | at the six anchors |
|---|---|---|
| Boltz-2 | −0.10, null | **−0.22, signed** |
| Chai-1 | +0.07, null | −0.16, null |
| OpenFold3 | −0.26, signed | **−0.63, signed** |
| Protenix2 | **+0.33, signed positive** | +0.07, null |

The Protenix2 row is the finding. Read over the whole complex its confidence
correlates *positively* with distance from the active state — apparent
overconfidence — and that reversal **disappears entirely at anchor grain**.
OpenFold3 moves the other way, strengthening from −0.26 to −0.63. Reporting a
single pooled pLDDT correlation would have produced two opposite and equally
misleading conclusions. **Figure BA-5.**

`plddt_at_anchors` was designated the primary aggregation **post hoc**, after all
three had been computed (W-2); all three are reported in Table T4. OpenFold3
seeds are 5 outer × 5 inner and are less independent than the other backbones',
which qualifies cross-backbone comparison of these magnitudes.

This is a finding about method rather than about these four models, and it
generalises beyond this corpus: a confidence score aggregated over a whole
complex can invert relative to the same score read at the residues that define
the property in question.

---

## Not claimed here

Prospectivity (the fraction metric requires an active reference, so every
receptor has one by construction — C-9), the mechanism of state selection, any
directional control toward the inactive state, two-state generation, and novelty
of partner-conditioned activation. Each has a designated home elsewhere in the
paper.
