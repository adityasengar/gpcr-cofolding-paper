# MANUSCRIPT_FLAGS

**Purpose**: central index of every claim, phrasing, or Methods-line item that
requires attention in the manuscript. Each flag names what changes if the item
is not addressed. Flags are load-bearing across the paper; a reviewer who
reads the manuscript without seeing the corresponding correction will surface
the issue.

**Provenance**: this list was compiled from two sources — (a) the initial
scientific review (post-Block-A-dossier, pre-`pre-scientific-review` tag),
14 items, and (b) the post-review execution pass (P0, P1a, P1b, P2, curation,
P6, P3, P7), which produced 26 additional items. All are listed here in the
order they were surfaced.

**Status legend**:
- `text_only` — a Methods/Results sentence needs to be written or amended; no data change.
- `data_pending` — a rescore or curation-file edit would resolve this; not yet done.
- `open_decision` — pending user adjudication among 2+ options.
- `resolved` — addressed elsewhere in the archive (dossier phase, withdrawal, or caveat).

---

## Flags from the scientific review (14 items)

### Flag 1 — Water-mediated NPxxY bridge wording
**Source**: review Q1.
**Content**: The 4.32 Å NPxxY-OH median sits at the tight end of the water-bridged Y5.58–Y7.53 range (~4.3–5.5 Å). None of the four backbones models the bridging water. The paper must say "consistent with a water-bridged arrangement", NOT "the water-mediated bridge forms".
**Status**: `text_only`.

### Flag 2 — Threshold provenance one-liner
**Source**: review Q1.
**Content**: 9.082 and 14.932 are optimizer output. The Methods paragraph must state what set they were fit on and by what objective. **Resolved in the data** by P0: fit set = 80 tier-1 crystal reference rows; objective = midpoint(mean_active_ref, mean_inactive_ref). SHA-pinned output at `refs/thresholds_panel.csv::242b509f7b7a`.
**Status**: `resolved` (P0 CLEAN) — `text_only` for the Methods sentence.

### Flag 3 — Prospectivity foreclosure at Block A abstract-level
**Source**: review Q4. **Amended by P6**: the review's specific "7 receptors with no active reference" line was inaccurate (48/48 have active refs — see Flag 31). The prospectivity concern is real but the mechanism is different: the `fraction-of-way-to-active` metric requires an active reference; every receptor has one by design; nothing is truly held out at the reference level. **Prospectivity must come from the date-stratified holdout** (P6, Flag 31) or from Block C.
**Status**: `text_only` — Abstract-level Methods flag.

### Flag 4 — Ceiling-saturation caveat on the 94%
**Source**: review Q1. Class A cognate tilt 5/50/95 = 12.95 / 17.48 / 18.68 shows a pileup against a bound (lower half 4.5 Å, upper half 1.2 Å). Model cognate tilt sits at or near reference-tilt values on the same metric. Part of the 94% is the metric topping out. The continuous headline (delta_to_active) is insulated; the "94% predicate-active" binary quote is not.
**Status**: `text_only`.

### Flag 5 — CNR2 re-anchoring
**Source**: review Q2. **Curation task confirmed**: 5ZTY is the Janus structure per Li 2019 Cell (inactive at cytoplasmic end, agonist-like pocket). Block A cytoplasmic-endpoint numbers ARE legitimate (P1a: inactive fails as expected; Phase 1d tilt Δ = 4.89 Å well-separated). Block C pocket-shape claims using 5ZTY are compromised. Three options: swap 5ZTY, keep + move bistability anchor to CCR5, or keep + heavy caveat.
**Status**: `open_decision` (three options presented; user picks).

### Flag 6 — AGTR1 PDB annotation verification
**Source**: review Q2. **Curation task confirmed**: 6OS2 IS nanobody-stabilised (Wingler 2020 Science) — annotation is technically correct — but 6OS2 is the β-arrestin-biased entry, not the "distinctive activation mechanism" paper (that's 6DO1, Wingler 2019 Cell, AngII-partial-agonist). Two options: keep 6OS2 + refine annotation, or swap to 6DO1.
**Status**: `open_decision`.

### Flag 7 — OPRD swap to Gi complex
**Source**: review Q2. **P1a + curation task confirmed**: 6PT2 (agonist-only + BRIL) fails its own predicate at NPxxY = 16.75 Å (well above 9.082 threshold). Not a bona-fide active-state DOR-Gi complex. Curation task DEFERRED the specific DOR-Gi PDB identification — likely one of Wang et al. 2023 Cell's 8F7* series; needs directed RCSB search.
**Status**: `open_decision` + `data_pending` (post-decision rescore of 200 OPRD rows).

### Flag 8 — Class B as explicit scope limitation
**Source**: review Q3. **Confirmed in Phase 4d**: kink apo-active is 73–100% across all backbones — kink does NOT discriminate arm. **Confirmed in Phase 3c**: cognate tilt is 100% ceiling-saturated. Neither predicate works on Class B with n=4 receptors. The instrument is Class A-calibrated. Class B should be reported as an explicit scope limitation.
**Status**: `text_only`.

### Flag 9 — Class F as curator-call with sensitivity analysis
**Source**: review Q3. FZD6/FZD7 Gs coupling is a curator call, structurally-motivated by 8JHB/8YY8 (XLas Gα-bound), not IUPHAR-locked. Recommend sensitivity analysis: recompute headline with Class F dropped. With 4/48 receptors, the number almost certainly doesn't move.
**Status**: `text_only` + one small computation.

### Flag 10 — Permutation null vs Block B wrong-partner null
**Source**: review Q6. Shuffling arm labels tests "does adding a G protein change structure" — trivially yes. The load-bearing null is wrong-partner, which lives in Block B (shuffled Gα reaches high active rates). Phase 4h's p<0.001 permutation nulls are measuring the wrong thing. **W-9 (new withdrawal) covers this.**
**Status**: `resolved` (see `withdrawals/W-9`).

### Flag 11 — Cluster-bootstrap for paralogs
**Source**: review Q6. **P7 confirmed**: 26-cluster paralog bootstrap widens CIs by median 1.10×. Three barely-signed findings flip to null (P1b Protenix tilt slope; P3 Chai anchor_mean; P3 Protenix anchor_min). Load-bearing findings survive. **Cluster-boot is authoritative going forward.**
**Status**: `resolved` (P7).

### Flag 12 — "Apo" as computational reference condition
**Source**: review Q6. "Apo" is not a physical state — no ligand, no partner, no membrane, no basal-activity equivalent. Either the constitutive-activity correlation from review Q1 (P5, demoted to opportunistic) supports treating it as a physical baseline, or describe it as a computational reference condition. **New caveat C-9 covers this.**
**Status**: `text_only` (see `caveats/C-9`).

### Flag 13 — Sealed-8 pre-registration documentation
**Source**: review Q6. What was the criterion, when fixed, is it documented before results were seen? Sealed subset is `refs/sealed_active_refs_2026_09_01.csv` (SHA `879046326c6b`, matches CLAUDE.md pin), documented in PREREG §14 v3 with deterministic seed `20260903`. Pre-registration is on record.
**Status**: `text_only` — one Methods sentence pointing at PREREG §14.

### Flag 14 — Inactive-reference construct audit
**Source**: dispatch correction. The R242(6.32)E in 5ZTY shows the class of problem is real; CB2 is unlikely to be the only case. Column in the widened O-4: which inactive references carry ICL3 fusions or engineered residues inside the 6.30–6.50 or 7.49–7.53 windows the predicates read.
**Status**: `data_pending` (widened O-4 audit; scope defined; execution deferred).

---

## Flags from P0 (threshold provenance) — 1 item

### Flag 15 — Derivation-set self-consistency is not held-out
**Source**: P0. The 98.8% (tilt) and 94.3% (NPxxY-OH) figures in PREREG §2c-revised are derivation-set accuracy — the thresholds were fit on the same 80 rows they are tested against. Not held-out predictive accuracy.
**Status**: `text_only`.

---

## Flags from P1a (predicates on refs) — 5 items

### Flag 16 — OPRD 6PT2 curation error (formalized)
**Source**: P1a + curation task. Same as Flag 7 restated with concrete numbers: NPxxY = 16.75 Å, tilt = 15.78 Å. Agonist-only + BRIL. Swap to a DOR-Gi complex.
**Status**: merged with Flag 7 (`open_decision` + `data_pending`).

### Flag 17 — AGTR1 6OS2 vs 6DO1 (formalized)
**Source**: P1a + curation task. Same as Flag 6 restated.
**Status**: merged with Flag 6 (`open_decision`).

### Flag 18 — FZD6 reference-pair tilt degeneracy
**Source**: P1a. FZD6 8JHB (active, tilt 15.53) vs 8JH7 (inactive, tilt 14.50) is only 1.03 Å separated on Class F's single axis. The inactive passes the active-side threshold. Class F cannot distinguish this pair.
**Status**: `text_only`.

### Flag 19 — Derivation-set self-calibration is 88% NPxxY (35/40), not 100%
**Source**: P1a. 4 of 40 Class A actives fail their own predicate on NPxxY: 5HT2C (chimeric mini_G, measurement artifact), B1B1U5 (jellyfish opsin, expected biology), MCHR1 (HOLD pending Phase 1a 353-vs-422 aa resolution), OPRD (curation error). Report itemized deviations.
**Status**: `text_only`.

### Flag 20 — 6 Class A receptors are effectively tilt-only
**Source**: P1a. EDNRA, EDNRB, GRPR, HRH3 (7.53=L not Y — no OH), FSHR, LSHR (inactive OH unresolved). The Class A stratum is heterogeneous on axis coverage; a Class A analysis pooled across all axes cannot include these on the NPxxY axis.
**Status**: `text_only`.

---

## Flags from P1b (amplitude regression) — 4 items

### Flag 21 — Amplitude flatness is campaign-wide, not Chai-specific
**Source**: P1b. 7/8 amplitude regression CIs cross zero on tilt at receptor-boot; **8/8 cross zero at cluster-boot (P7)**. All slopes far from unity (+0.035 to +0.550). Models reach a generic active-state geometry but do NOT reproduce receptor-specific amplitude. This holds on ALL FOUR backbones, not just Chai. The review's specific Chai prediction is confirmed AND generalizes.
**Status**: `text_only` — load-bearing manuscript-flag: the "reproduces amplitude" claim, if any, must be retracted.

### Flag 22 — Two axes, two fractions
**Source**: P1b. Phase 4's `delta_to_active` fraction (0.89–0.95) and P1b's raw-tilt fraction (0.44–0.98) answer different questions. Same data. Both are legitimate. The manuscript must state which it means.
**Status**: `text_only`.

### Flag 23 — Amplitude regression robust to HOLD receptors
**Source**: P1b. Including MCHR1 + OPRD (curation HOLDs) moves the slope by ≤ 0.034 per backbone. The load-bearing finding is not driven by the HOLD receptors.
**Status**: `text_only`.

### Flag 24 — ACM1-Protenix outlier
**Source**: P1b. Protenix per-receptor residual on ACM1 = +8.77 Å (largest residual anywhere in P1b). Protenix over-predicts ACM1 tilt shift.
**Status**: `text_only` (may become an investigation open-item if it interacts with the Protenix pLDDT collapse finding at Flag 34).

---

## Flags from P2 (orthogonal signature) — 3 items

### Flag 25 — Orthogonal signature corroborates the two-instrument predicate
**Source**: P2. P5.50–F6.44 Cα-Cα (PIF motif connector) — never used to call anything, orthogonal by construction. Reference active median 10.48 Å vs inactive 11.99 Å (Δ = −1.51 Å, non-overlapping 95% CIs). Prediction predicate-active median 10.35 vs predicate-inactive 11.62 (Δ = −1.27 Å). **21 of 22 predicate-active predictions land below reference-inactive median; 20 of 21 predicate-inactive predictions land above reference-active median. Magnitude ratio 0.84.** The instrument is corroborated by something outside itself.
**Status**: `text_only` — load-bearing: this is the "reaches active-state geometry" evidence that survives P1b's amplitude flatness. Should be a headline claim.

### Flag 26 — P2 orthogonal signature is Class A only
**Source**: P2. The 5.58-8 residue offset for P5.50 is Class A specific; Class B/F use different numbering. Corroboration verdict scoped to Class A only. Class B/F orthogonal corroboration is a future scope.
**Status**: `text_only`.

### Flag 27 — Chai's P2 signal is LARGEST despite being softest on P1b
**Source**: P2. Chai per-backbone connector Δ = −1.65 Å (matches reference Δ = −1.51 Å within noise). Boltz softest (−0.52); OF3 (−1.05); Protenix (−0.91). **Chai reproduces reference-scale connector rearrangement while pushing tilt to a generic active geometry.** Per-backbone story: Chai is different, but not simply "softer" — it captures one axis and misses another.
**Status**: `text_only`.

---

## Flags from curation task — 3 items (partial merges with 5, 6, 7)

### Flag 28 — AGTR1 curation options
**Source**: curation task. Options A/B/C presented; user picks.
**Status**: `open_decision` (merged with Flag 6/17).

### Flag 29 — OPRD DOR-Gi PDB identification deferred
**Source**: curation task. Candidates by name (Wang et al. 2023 Cell 8F7* series; Yin/Chen 2023-24 Nature/Cell); specific PDB identification needs directed RCSB search.
**Status**: `open_decision` + `data_pending` (merged with Flag 7/16).

### Flag 30 — CNR2 5ZTY `construct=wt` annotation is stale
**Source**: curation task. RCSB metadata says 7 mutations on 5ZTY; on-disk annotation says `construct=wt`. The specific R242(6.32)E mutation the review cited is not confirmed via RCSB metadata but the count matches. At minimum: fix the annotation.
**Status**: `data_pending` (annotation-only column edit) OR `open_decision` (if bundled with re-anchor).

---

## Flags from P6 (training-cutoff feasibility) — 3 items

### Flag 31 — Panel is 48/48 with active refs; review's "7 no-active-ref" was inaccurate
**Source**: P6. All 48 panel receptors have an active reference in `refs/reference_set.csv`. Prospectivity comes from the date-stratified holdout (Flag 33 candidate: **run the analysis** — n=24-26 for AF3-lineage, n=11-12 for extended cutoffs, all above the ≥ 10 threshold).
**Status**: `text_only` correction + one new analysis (P6-run) is available and unblocked.

### Flag 32 — 6/48 active refs are not Gα-coupled
**Source**: P6. ADRB1 (7BU7, nanobody-only), ADRB2 (4LDE, Nb80-stabilised), AGTR1 (6OS2, nanobody+β-arrestin-biased), CNR1 (5XRA, agonist-only), FZD4 (8WMA, agonist-only), OPRD (6PT2, agonist-only+BRIL). Widened O-4 audit candidates. ADRB1/2/AGTR1 are nanobody-stabilised active states and defensible; CNR1/FZD4/OPRD are agonist-only and weaker.
**Status**: `data_pending` (widened O-4 audit).

### Flag 33 — 4 PDBs missing from `refs/cache/rcsb/`
**Source**: P6. 6X18 (GLP1R), 6LMK (GCGR), 8FLQ (PTH1R), 8JHB (FZD6). Backfill from RCSB for release completeness.
**Status**: `data_pending` (backfill).

---

## Flags from P3 (anchor pLDDT redo) — 3 items

### Flag 34 — plddt_mean is the wrong aggregation
**Source**: P3. `plddt_mean` is diluted by Gα chain, loops, termini. The right question ("did the model produce the correct conformational state?") lives at the anchor residues 3.50, 3.51, 5.58, 6.30, 6.34, 7.53. Anchor pLDDT is the right metric and it changes the answer materially on Protenix and Boltz.
**Status**: `text_only` — **W-2 needs restatement** (see `withdrawals/W-2`, updated in this pass).

### Flag 35 — OF3 anchor-pLDDT r = −0.626 is the strongest signal in the campaign
**Source**: P3. OF3 anchor_mean Pearson r = −0.626 [−0.736, −0.497] (receptor-boot); [−0.827, −0.601] (cluster-boot). Effect roughly doubles vs plddt_mean. **Manuscript-flag: this is the load-bearing "pLDDT tracks correctness" evidence, on OF3 specifically.**
**Status**: `text_only`.

### Flag 36 — AA1R positive correlation on all 4 backbones
**Source**: P3. AA1R shows positive Pearson r on all 4 backbones (0.82–0.98). Cross-backbone consistency is unusual and may relate to published high constitutive activity of the A1 receptor. Deserves a Methods flag; may connect to the demoted P5 (constitutive-activity correlation).
**Status**: `text_only`.

---

## Flags from P7 (cluster-bootstrap) — 4 items

### Flag 37 — Cluster-bootstrap is authoritative going forward
**Source**: P7. 26-cluster paralog bootstrap widens CIs by median 1.10× (much less than the review's 30-100% expectation). Report cluster-boot CI as the authoritative measurement. Receptor-boot mildly overstated precision.
**Status**: `resolved` — but LEDGER.csv CIs should be updated to cluster-boot values before submission.

### Flag 38 — All 4 backbones null on tilt amplitude under cluster-boot
**Source**: P7. P1b Protenix tilt slope (+0.503) was the only signed amplitude regression at receptor-boot; flips to null at cluster-boot ([−0.049, +0.737]). **The "no receptor-specific amplitude reproduction" story is reinforced, not weakened.**
**Status**: `text_only`.

### Flag 39 — Chai anchor_mean flips to null under cluster-boot
**Source**: P7. P3 Chai anchor_mean r = −0.241 flips to [−0.457, +0.003] under cluster-boot. Was barely signed at receptor-boot. **Anchor_min still signed for Chai.** Report anchor_min as Chai's evidence for pLDDT-tracks-correctness, not anchor_mean.
**Status**: `text_only`.

### Flag 40 — Anchor pLDDT signed-neg authoritative on Boltz + OF3 only
**Source**: P7. After cluster-boot: Boltz (signed neg) + OF3 (signed strongly neg) survive on anchor_mean. Chai holds anchor_min only. Protenix null on both. The confidence-vs-correctness story shrinks slightly but keeps its two strongest backbones.
**Status**: `text_only`.

---

## Freeze-batch updates (post `post-review-analysis-batch`; landed for `block_a_freeze`)

### Refinements to earlier flags

**Flag 21 (amplitude flatness) — REFINED per T1**. On the tilt axis, the campaign panel's SD(Δ_tilt_ref) = 1.19 Å across 40 Class A receptors is severe restriction of range; the axis cannot resolve amplitude at panel scale. Attenuation correction under σ_err = 1.0 Å gives Chai −1.77 (physically impossible) and OF3 +1.06 (near unity, numerically unstable). Report as instrument property, not result. On the NPxxY-OH axis, SD = 4.71 Å (well-powered), all Class-A-only cluster-boot slopes 0.12–0.55 with CIs crossing zero, attenuation-robust (var-inflation ~1.05). **Amplitude genuinely NOT reproduced on NPxxY.** See caveat C-10 (rewritten).

**Flag 25 (P2 orthogonal signature) — REFINED per T2 scale-up**. n=43 → n=512. Magnitude ratio 0.84 → **0.37 [0.04, 0.77]**. Load-bearing counts 21/22 + 20/21 (95%) → **204/256 + 205/256 (80%)**. Δ_pred −1.27 Å → **−0.56 Å [−1.16, −0.06]**. Direction unanimity across 4 backbones survives; per-backbone signing collapses from 3/4 to 1/4 (Chai only at n=128). P2 original numbers were a mixed-convenience-sample artefact.

**Flag 27 (Chai P2 leading) — REFINED**. Chai per-backbone Δ was −1.65 (n=43); at n=128 becomes **−0.86**. Still largest per backbone but less dramatic. Chai reproduces reference-scale connector direction while pushing tilt to a generic geometry.

**Flag 40 (anchor pLDDT signed) — CLARIFIED**. Under cluster-boot + post-hoc primary designation of `anchor_mean`: **2 of 4 backbones signed** (Boltz + OF3), not 3. Chai signs only on `anchor_min` (secondary sensitivity). Protenix null on both aggregations. See W-2 restatement.

### Dropped

**Flag 41 — DROPPED.** The attenuation-corrected OF3 tilt slope +1.06 at σ_err = 1 Å is not a defensible hedge. The Chai slope of −1.77 at the same σ_err is physically impossible; the impossible value is the diagnostic that the correction is numerically unstable at that noise assumption. Report the sensitivity as evidence the tilt axis cannot resolve amplitude, not as a hedge on OF3.

### New flags 42–50

**Flag 42 — `construct` column corpus-wide untrusted**. T4 audit: **52 / 127 = 40%** of evaluable PDBs have `construct = wt` on-disk contradicted by RCSB `pdbx_mutation`; **41 / 127 = 32%** after excluding a recurring mini-Gs fusion signature. This is CORPUS-WIDE across the full reference-set file.

**Three denominators — the Methods sentence must name the population**:

| Population | n | What it is |
|---|---:|---|
| Panel unique PDBs | 89 | The 48-receptor Block A panel's active + inactive PDBs (C-6) |
| Reference-set total | 167 | Every unique PDB in `panel/refs/reference_set.csv` incl. off-panel refs used by other blocks |
| **Evaluable audit set** | **127** (76% of 167) | PDBs with cached RCSB `_entry.json` sufficient for the contradiction check. **The 40% (52/127) runs on this population.** |

**The 40% Methods sentence describes the evaluable audit set** (n=127), which comprises the whole reference-set file (both panel-relevant and off-panel PDBs). The panel-only subset audit (contradictions among the 89 panel PDBs specifically) is NOT broken out; that requires filtering T4's 52 flagged PDBs to panel-only membership. Deferred.

Post-review fixes to CNR2 5ZTY and AGTR1 6OS2 annotations are in `panel/refs/POST_REVIEW_ANNOTATIONS.md`; corpus-wide repair (all 52 or 41 contradictions, whichever excluding-rule the paper adopts) is deferred. Caveat C-11 covers.

**Flag 43 — AGTR1 6OS2 BRIL insertion at 227–229 in tilt-predicate residue-range window**. Not previously flagged. In ICL3 adjoining TM6 (rough tilt-predicate window 220–265). AGTR1 6.30 anchor is at seq 235; BRIL is 6 residues below 6.30, effectively in the ICL3-TM6 junction. Reference cleanly discriminates apo vs cognate at Δtilt = 12.5 Å per P1a; number-integrity intact but the reference has a fusion structural perturbation adjacent to the predicate window.

**Flag 44 — OPRD 6PT2 not-an-artifact but limited**. OPRD artifact-check verified: both OH atoms present, chain A OH-OH = 16.749 Å bit-exact to scorer's stored 16.75 Å, scorer's OH-fallback path was not triggered (verified to return NaN correctly). The 16.75 Å is HONEST GEOMETRY — 6PT2 is agonist-only + BRIL, agonist-engaged but NOT Gα-engaged; the NPxxY H-bond network does not form without Gα clamping. Per dispatch: HOLD, no swap. Handled via E5 exclusion set. Systemic issue: agonist-only actives (OPRD, CNR1, FZD4) fail NPxxY by construction — this is a finding about reference-set completeness, not a scoring bug.

**Flag 45 — 4 rows with NPxxY-OH < 2.4 Å (model-side atom clashes)**. Physically impossible geometry: two OH atoms cannot sit within 2.4 Å. Independent recompute (T6 Part 3) verified real coordinates, not scoring artifact. Rows: CNR2 apo chai (2.36), CNR2 apo protenix (2.21), AA2AR cognate of3 (2.38), FSHR apo of3 (2.10). E2 exclusion set. 4 / 9,490 = 0.042%. Methods sentence: 0.04% of rows have OH-OH distances below covalent limits (model-side clashing artifact).

**Flag 46 — ACM1-cognate-Protenix broken cell**. 25 rows with mean plddt_mean ≈ 38.66, tilt > 30 Å median, NPxxY-OH > 20 Å median. All `passed=True` because A1–A6 has no pLDDT floor. E1 exclusion set. Caveat C-12 covers. 25 / 9,490 = 0.263%.

**Flag 47 — Threshold 9.08 vs 9.082 truncation**. Row-level `threshold_npxxy_oh_active_lt` is stored as 9.08 (2-decimal truncation of 9.082); 1 borderline row flips predicate between the two representations. Not material for headline; cite in Methods for reproducibility.

**Flag 48 — `anchor_6_30_uniprot_pos = -1` sentinel on 200 GCGR rows**. Legitimate "not applicable" marker (GCGR is Class B, no canonical 6.30 anchor position). Already documented in Phase 3d. Methods sentence: −1 is the encoded not-applicable marker, distinct from NaN.

**Flag 49 — Tilt-axis independent recompute (T7a) — VERIFIED CLEAN**. T7a re-derived `d_gpcrdb_tm6_tilt_246_637_ca` on n=45 Class A samples with gemmi + stdlib only (no `scorer/` import). Result: median |Δ| = 0.0000 Å, max |Δ| = 0.0000 Å, Pearson r = 1.000000 against stored values. 5 Class B rows skipped (BW 2.46/6.37 undefined in Wootten numbering; expected biology). **Both predicate axes (tilt + NPxxY-OH) are independently verified against non-scorer implementations. Last unverified dependency in the corpus is closed.**

**Flag 50 — Block C stale ρ (Block A-adjacent, not Block A blocker)**. `docs/BLOCK_C_PAPER_DRAFT_v1.md:276` cites ρ = 0.129 for a Block-B-vs-Block-C receptor contribution correlation. v2 corpus recompute is ρ = 0.180. Both fall inside published 95% CI [−0.213, +0.443]. Documented at `experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/pr1_stale_corpus_sweep.md`. Block C manuscript hygiene issue; NOT a Block A freeze blocker.

### Post-review annotation edits (in `panel/refs/POST_REVIEW_ANNOTATIONS.md`)

- AGTR1 6OS2: `stabilising_elements` `nanobody` → `nanobody_beta_arrestin_biased_agonist`. No PDB swap, no reference-axis rescore.
- CNR2 5ZTY: `construct` `wt` → `multi_mutation_incl_R242E_tilt_window` (RCSB confirmed 7 receptor mutations including R242E at BW 6.30). No PDB swap.
- OPRD 6PT2: no annotation change. HOLD per dispatch. Handled via E5.

### Deferred to MANUSCRIPT_FLAGS.md as stated limitations

- Full-corpus P2 rescore (permanent `d_connector_p550_f644_ca` column in `scorer/anchors.py`)
- Corpus-wide `construct`-column repair across all 167 reference-set PDBs
- Extended-cutoff cluster-level date-stratified holdout (n=8, underpowered; descriptive not inferential)
- PAE analysis (not laptop-recoverable at row grain)
- Class B / Class F rescue on the amplitude regression (instrument-scope limitation, not a defect)
- Panel-only subset audit of T4's 52/127 contradictions (denominator reconciliation deferred)
- Mutation-verification on the 40 newly-fetched PDB `_entry.json` (deposition dates verified; per-PDB `polymer_entity` mutation lookup deferred)

## Summary counts

| Category | n |
|---|---:|
| Total flags | 49 (Flag 41 dropped) |
| `text_only` | ~30 |
| `data_pending` | 4 |
| `open_decision` | 0 (curation decisions settled) |
| `resolved` | 6 |

**Load-bearing manuscript changes**:
1. Retract Protenix-overconfident-across-panel claim (Flag 34 + W-2 restatement)
2. Retract "reproduces receptor-specific amplitude" if implicit anywhere (Flag 21 + Flag 38)
3. Retract permutation-null p-values as the load-bearing null (Flag 10 + W-9)
4. Add "reaches active-state geometry via orthogonal PIF-connector signature" as the surviving positive claim (Flag 25 + LEDGER SC-11 candidate)
5. Reframe prospectivity claim to rest on the date-stratified holdout (Flag 3 + Flag 31), not on the fraction metric which forecloses prospectivity by design
6. Report cluster-boot as authoritative CI throughout (Flag 37)
7. Fix threshold provenance sentence (Flag 2)
8. Fix pLDDT aggregation choice throughout (Flag 34, use anchor pLDDT)

**Pending user decisions**:
- Flag 5/28 (CNR2 re-anchor)
- Flag 6/17/28 (AGTR1 6OS2 vs 6DO1)
- Flag 7/16/29 (OPRD Gi swap)
- Flag 30 (CNR2 annotation-only fix vs re-anchor)
