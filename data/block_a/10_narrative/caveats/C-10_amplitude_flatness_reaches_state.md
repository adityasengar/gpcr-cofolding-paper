# C-10 — Amplitude: tilt-axis instrument limitation; NPxxY genuine null; state-reached corroborated orthogonally

## The caveat, rewritten post-T1 + post-T2

Two findings in tension, both true, both load-bearing for the manuscript.
Both are downgraded from stronger claims that appeared in the
`pre-scientific-review` version:

### 1. Amplitude reproduction: the tilt axis cannot resolve it; NPxxY-OH returns a clean null.

**Tilt axis is an INSTRUMENT LIMITATION, not a result.** T1 established that
Class-A-only Δ_tilt_ref has **SD = 1.19 Å across 40 receptors** (range
[+2.29, +7.89] Å; median +5.33 Å). This is severe restriction of range: the
reference structures themselves barely differ in tilt amplitude. Known
receptor heterogeneity does not survive translation into this coordinate.
Attenuation correction under a plausible reference-error variance
(σ_err = 1 Å, so var(err) = 1 Å² against var(Δref) = 1.417 Å²) explodes
because 70% of predictor variance is error at that assumption. Corrected
slopes under σ_err = 1.0 Å: OF3 tilt → +1.06 (near unity, but physically
unstable); Chai tilt → −1.77 (mathematically negative, physically impossible).
The impossible negative is the diagnostic — the correction has no signal to
work with. **The tilt axis lacks the dynamic range to test amplitude
reproduction at panel scale.** State it as an instrument property; do not
report a corrected slope as evidence either way.

**NPxxY-OH axis returns a clean null.** SD(Δ_npxxy_ref) = 4.71 Å across n=34
receptors after P1a exclusions (well-powered). Cluster-boot slopes (post-T1
+ post-P7): boltz +0.12 [−0.25, +0.80]; chai +0.55 [−0.04, +1.58]; of3 +0.21
[−0.06, +0.52]; protenix +0.21 [−0.11, +0.83]. All CIs cross zero.
Attenuation correction is small (var-inflation ratio ~1.05 under σ_err =
1 Å; ~1.24 under σ_err = 2 Å) — the finding is robust. **Amplitude is
genuinely not reproduced on NPxxY.**

**One capable axis, one clean answer.**

### 2. State-reached, corroborated at reduced magnitude.

P2's orthogonal signature (P5.50–F6.44 Cα-Cα connector, PIF motif, never
used to call anything) was scaled up in T2 from n=43 to n=512 (stratified
across 16 (backbone × arm × predicate) strata). At scale:

| Quantity | P2 (n=43) | T2 (n=512, cluster-boot) |
|---|---|---|
| Δ_pred (Å) | −1.27 | **−0.56 [−1.16, −0.06]** |
| Magnitude ratio |Δ_pred / Δ_ref| | 0.84 | **0.37 [0.04, 0.77]** |
| Pred-active below ref-inactive median | 21/22 (95%) | **204/256 (80%)** |
| Pred-inactive above ref-active median | 20/21 (95%) | **205/256 (80%)** |
| Per-backbone direction | 4/4 same-signed | **4/4 same-signed** |
| Per-backbone signed at n_backbone | 3/4 | **1/4** (Chai only at n=128) |

**The P2 magnitude of 0.84 was a mixed-convenience-sample artefact** — the
curated 25 CIFs oversampled cell extremes and AA2AR. Scaled numbers should
REPLACE P2 numbers in the manuscript. The direction unanimity across all 4
backbones survives; the magnitude drops to ~one-third of reference amplitude.

## What this means for the paper

The correct headline is **NOT "the model reproduces receptor-specific
activation amplitude"**. It IS **"the model reaches active-state geometry
across the panel; the NPxxY axis returns a clean null on amplitude
reproduction; the tilt axis is instrument-limited and cannot resolve
amplitude at panel scale"**.

The 89–95%-of-way-to-active fraction on `delta_to_active` is a valid summary
of the arm shift on the cross-axis carrier (E1–E5 exclusion sweep confirms
this is invariant to every exclusion, shift ≤0.5% under every combination).
It should not be read as "the model reproduces reference amplitude". The
two axes answer different questions (MANUSCRIPT_FLAGS.md Flag 22).

## Manuscript sentence

> Across the four backbones the cognate arm reaches 89–95% of the way from
> the apo baseline to the active reference on `delta_to_active` (invariant
> to every specified exclusion set). This reflects a shift toward
> active-state geometry, corroborated by an independent structural criterion
> (P5.50–F6.44 Cα-Cα connector separation on n=512 stratified predictions:
> Δ_pred = −0.56 Å [−1.16, −0.06] vs reference Δ = −1.51 Å; magnitude ratio
> 0.37 [0.04, 0.77]; four-backbone direction unanimity). At reference-
> amplitude scale, the NPxxY-OH axis returns a clean null on amplitude
> reproduction (Class-A cluster-boot slopes 0.12–0.55, all CIs crossing
> zero, attenuation-robust). The tilt axis has too narrow a predictor
> variance across the panel (SD = 1.19 Å across 40 Class A references) to
> resolve amplitude, and no strong conclusion can be drawn there. The
> paper's headline is that predictions reach the active-state basin, not
> that they hit each receptor's specific amplitude.

## Related

- MANUSCRIPT_FLAGS.md Flags 21, 22, 25, 27, 37, 38 (all refined post-T1/T2/P7)
- P1b, P2, P7 fork reports (pre-T1/T2)
- T1 restriction-of-range diagnostic; T2 scale-up
