# migliorini2026pairsae

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say, `NOT
APPLICABLE` + reason where the field presupposes a conformational method this paper is not.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–13)** and coincide with the
printed page numbers. Structure: p1 title/abstract/intro, p2 Fig 1 + intro cont. + §2 Background,
p3 §2.2 pairformer + §3 PairSAE method, p4 loss + §4 Results + Table 1 + §4.1 probing, p5 Fig 3 +
§4.2 hypothesis generation + §5 Conclusion, p6–p8 references, p9 Appendix A (N-mode SVD) + Appendix
B (experimental details B.1–B.3), p10 Figs B.4/B.5 + Table B.2, p11 Figs B.6/C.7 + Appendix C text,
p12 Figs C.8/C.9, p13 Fig C.10.

**What this paper is, stated up front because it governs sections C and E.** This is a
**mechanistic-interpretability paper, not a structure-prediction or conformational-sampling paper.**
It trains sparse autoencoders (SAEs) to *read out* what is encoded in Boltz-2's internal
representations. It runs Boltz-2 once per complex to harvest activations; it never samples
conformations, never assigns a conformational state, never measures an RMSD, and — critically —
**never intervenes on any internal tensor.** Section C is therefore largely `NOT APPLICABLE` by
design, not by extractor sloppiness.

**What "on the pair representation" actually means here, precisely.** The SAE is **not** run
directly on the pair tensor `Z`. The pipeline (p3, §3; p9, §B.1) is:

1. Take Boltz-2's pair tensor `Z ∈ R^(Ntok × Ntok × nz)` with `nz = 128`, at a fixed layer and
   recycling step.
2. Compute the mode-1 and mode-2 unfoldings of `Z` and take their left singular vectors
   `U(1), U(2) ∈ R^(Ntok × Ntok)` (`numpy.linalg.svd` on the flattened unfoldings).
3. Truncate each to its first `r = 64` columns and concatenate row-wise into a **token-level**
   summary `m_i = [U(1)_{i,1:r} ‖ U(2)_{i,1:r}]`, i.e. a 128-dim per-token vector encoding "how
   token i behaves as a row and as a column of Z". Zero-pad if `Ntok < r`.
4. Concatenate `m_i` with the **sequence** representation `s_i` (`ns = 384`) → 512-dim, then
   LayerNorm.
5. Encode that 512-dim vector with a BatchTopK+ReLU SAE of dictionary size `D = 16,384`.
6. Decode the shared feature vector `h_i` back into **both** spaces: `ŝ_i = D_s h_i + b_dec^s` and
   `ẑ_ij = D_z^row h_i + D_z^col h_j + b_dec^z`.

So the pair representation enters the encoder **only through a rank-64 two-sided SVD summary**, and
enters the loss directly through the pair reconstruction term. This is the honest description; "an
SAE on the pair representation" is a shorthand that loses the compression step.

---

## A. Identity

- **citekey**: `migliorini2026pairsae`
- **doi**: **arXiv:2606.27440v1 [cs.LG]** — p1, stamped in the left margin: "arXiv:2606.27440v1
  [cs.LG] 25 Jun 2026". `refs.bib` records `doi = {10.48550/arXiv.2606.27440}`, the arXiv DOI. No
  journal DOI exists in the PDF.
- **year**: **2026** (arXiv stamp 25 Jun 2026; `refs.bib` `year = {2026}`). **Note the internal
  inconsistency:** the venue line on p1 reads "Machine Learning for Structural Biology Workshop,
  NeurIPS 2025", i.e. a 2025 workshop, while the arXiv posting is stamped 2026. Recorded, not
  resolved.
- **venue**: **arXiv preprint of a NeurIPS workshop paper, not peer reviewed as a journal article.**
  p1, footer: "Machine Learning for Structural Biology Workshop, NeurIPS 2025." Tagged `preprint`.
- **title**: PairSAE: Mechanistic Interpretability from Pair Representations in Protein Co-Folding
  — p1
- **authors**: Giosue Migliorini (University of California, Irvine; "*Work done during an internship
  at Flagship Pioneering*", p1 footnote), Aristofanis Rontogiannis, Grigori Guitchounts, Nicholas
  Franklin, Axel Elaldi, Olivia Viessmann (all Flagship Pioneering) — p1. This is an industry
  (Flagship Pioneering) paper with one academic intern first author.

## B. Scope

- **system**: **general protein** — specifically **protein–ligand complexes**, not a conformational
  family. p4: "We evaluate PairSAE on Boltz-2 representations for protein–ligand complexes from
  PLINDER [Durairaj et al., 2024]." The three showcased examples (p2, Fig 1) span a membrane protein
  (*E. coli* Complex II, PDB 1NEK), a glycoprotein with disulfides (influenza N2 neuraminidase chain
  B, PDB 4K1I) and a homodimeric protease (HIV-1 protease with inhibitor, PDB 1HPS). No GPCR,
  kinase, transporter or fold-switch analysis anywhere.
- **n_targets**: **Reported as counts of PLINDER *systems/complexes*, never as counts of distinct
  proteins.** All numbers p9 (§B.1–B.3) unless noted:
  - SAE training: **40,000 systems** sampled from the PLINDER training set, with at most 512
    residues.
  - Linear probing: **7,680** complexes (threshold fitting) + **2,560** (validation / feature
    selection) + **5,120** (test) = 15,360 complexes.
  - Affinity regression: **980** PLINDER complexes (train, held out from SAE training) → **PoseBusters**
    as test (n = 299, inferable from Fig 3 centre: off n=47 + on n=252, p5).
  - **Number of distinct proteins, distinct UniProt entries, or sequence-identity redundancy across
    these sets: NOT REPORTED.** This matters — a "40,000 systems" figure with unstated redundancy
    cannot be converted into a count of independent proteins.
- **method_class**: **other** — mechanistic interpretability / sparse dictionary learning on the
  internal activations of a co-folding model. It is *not* co-folding, MSA-subsampling,
  MSA-state-filtering, template-biasing, MD, enhanced sampling, clustering, or benchmark-only. It
  *consumes* co-folding inference (Boltz-2 forward passes) as its data source.
- **backbones**: **Boltz-2, single backbone** (p4: "We evaluate PairSAE on Boltz-2
  representations"; cited as Passaro et al., 2025). Architectural constants taken from Boltz-2 (p9):
  `ns = 384` sequence dim, `nz = 128` pair dim. **ESM2-650M** (Lin et al., 2023) appears as a
  *probe baseline on last-layer neurons* (p4–p5, Table 1, Fig 2) — it is a protein language model,
  **not** a second structure backbone, so this is **not** a multi-backbone comparison and is not
  tagged as one. No AF2/AF3/Chai/OF3/Protenix anywhere.
- **templates**: **NOT REPORTED.** The paper states the MSA setting explicitly (below) but never
  states whether Boltz-2 templates were on or off, for either activation harvesting or the affinity
  predictions. Protocol described p9 §B.1 and §B.3; templates are simply absent from it.
- **msa_handling**: **none — MSA explicitly disabled**, for both SAE training and evaluation.
  Verbatim, p9: "Due to compute constraints, we do not use the MSA when training and evaluating the
  PairSAE." Reinforced p10: "As mentioned in Section B, we did not use the MSA for our analysis."
  They then **quantify what this costs** (Fig B.6, p11; text p10): "we compare the Boltz-2 output
  with and without MSA, and note a substantial difference in predicted affinity values and affinity
  probability. As MSA-based predictions are conditioned on more information, we expect these to be
  more accurate. In future work, we aim at replicating our analysis using MSA inputs." So every
  feature and every affinity number in this paper is from a **no-MSA Boltz-2**, which the authors
  themselves expect to be the less accurate regime.

## C. Conformational core

**Blanket note for this section.** This paper contains no conformational analysis of any kind. It
does not generate ensembles, does not enumerate states, does not compare an active to an inactive
structure, and does not report a single structural accuracy number (no RMSD, no TM-score, no lDDT,
no DockQ). Fields below that presuppose a conformational method are marked `NOT APPLICABLE` **with
the reason**, per the v3 rule; the fields that still carry meaning (`structural_priors_used`,
`oracle_leakage`, `prospective`, `anti_memorization_*`, `controls_run`,
`confidence_as_discriminator`) are filled in full, because for an interpretability paper those are
exactly the fields the claim rests on.

- **states_generated**: **NOT APPLICABLE — no conformational sampling and no state assignment
  anywhere in the paper.** Boltz-2 is run to produce activations (and, for the affinity task, its
  affinity outputs); the resulting predicted complexes appear only as renders (Figs 1 top, 3 right,
  C.8, C.10). The paper never produces, clusters, scores or names a conformational state. Protocol
  where this would have appeared: p9 §B.1 and §B.3. The nearest thing to a structural observation is
  a **visual, unquantified** remark on pose plausibility, p11: "In these examples, the predicted
  complexes do not appear to present a plausible docked pose: the small molecule is displaced from
  the protein interface and does not form stable contacts."
- **structural_priors_used**: **Extensive, and entirely legitimate for this kind of paper.** All of
  the following are deposited-structure-derived knowledge used at design time:
  1. **PLINDER** (Durairaj et al., 2024) — the entire activation corpus is experimentally determined
     protein–ligand complexes from the PDB. p4: "protein–ligand complexes from PLINDER"; p9: "40,000
     systems sampled from the PLINDER training set … with at most 512 residues".
  2. **UniProt residue annotations** (UniProt, 2025) as the interpretability ground truth. p9: "We
     consider annotations from UniProt [UniProt, 2025], and binarize them by one-hot encoding each
     annotation."
  3. **SIFTS** (Velankar et al., 2012) to map PDB chains to UniProt. p9: "We map each chain in a
     PLINDER system to its UniProt annotation using the SIFTS database [Velankar et al., 2012], and
     match sequences with a minimum of 95% correspondance between the two databases, ignoring
     sequences that can't be matched."
  4. **PLIP interaction fingerprints** (Salentin et al., 2015), computed on deposited complexes, as
     an additional concept set. p9: "We also consider a subset of the system-level annotations found
     in PLINDER, as well as the PLIP interaction fingerprints [Salentin et al., 2015] that are also
     found in PLINDER."
  5. **PoseBusters** (Buttenschoen et al., 2024) as the held-out affinity test set. p5: "We test our
     results on Posebusters".
  6. **Specific PDB entries chosen to display features** whose concept identity is already known:
     1NEK, 4K1I, 1HPS (p2, Fig 1).
  7. **Boltz-2 itself**, trained on the PDB, is the object of study.
  None of this is a methodological sin; it is the data the interpretability claim is measured
  against. It is recorded here so it is not silently re-labelled as leakage.
- **oracle_leakage**: **The paper has no "target state", so the classical routes are vacuous. Where
  a route has a meaningful analogue — knowledge of the ground-truth *annotation* entering feature
  selection or reporting — it is answered against that analogue and labelled as such.** Each route
  separately:

  1. **Structures used as input or template — NOT APPLICABLE / NONE FOUND as leakage.** Deposited
     structures are the *subject* (activations are harvested by running Boltz-2 on PLINDER systems),
     not a template biasing an outcome. Protocol p9 §B.1: "We train for 250,000 steps on 40,000
     systems sampled from the PLINDER training set". Whether Boltz-2 templates were on is
     **NOT REPORTED** (see `templates`), so this route cannot be fully closed from the PDF.
  2. **State annotations from a curated state database (GPCRdb, KLIFS, Kincore) driving templates or
     alignments — NONE FOUND.** No conformational-state database is used or cited anywhere; the
     annotation sources are UniProt, SIFTS, PLINDER and PLIP, none of which is state-annotated.
     Protocol p9 §B.2.
  3. **Cluster labels derived from known states — NONE FOUND.** No clustering of any kind is
     performed. The only unsupervised decomposition is the N-mode SVD of `Z` (p3, p9), which is
     computed per system from the activations themselves with no external labels.
  4. **Hyperparameters, sweep ranges, seeds or stopping criteria tuned against the evaluation
     set — NONE FOUND on the reported test sets; the split discipline is explicit and clean.**
     Verbatim, p9: "We pick the best threshold τij on a training set of 7,680 complexes from the
     PLINDER training set, we select the best feature i for each concept j based on F1 scores on a
     validation set of 2,560 complexes, and finally report F1 scores on a test set comprised of
     5,120 randomly selected complexes." Threshold fitting, feature selection and reporting are on
     three disjoint sets — this is the right design. LASSO `λ` is likewise chosen by
     cross-validation on the training set only (p5: "by choosing λ using cross-validation"; Table
     B.2, p10, gives λ(CV) = 0.009 / 0.006). **Two residual caveats, neither disqualifying:** (i)
     the SAE hyperparameters themselves (`r = 64`, `D = 16,384`, `lr = 2e-4`, 250,000 steps, three
     nested Matryoshka widths) are stated as fixed choices with **no sweep reported at all** (p9), so
     there is no sweep range to have been tuned — but equally no evidence they were not chosen by
     looking at results; (ii) `r = 64` and the token-length cap of 512 residues interact (p9: "if
     Ntok < r we fill the remaining entries with zeroes"), and that interaction is never examined.
  5. **Success defined post hoc by RMSD/TM to a structure they held — NONE FOUND, and the deeper
     point is that no structural success criterion exists at all.** Success is (a) F1 of a
     single-threshold classifier against UniProt/PLINDER/PLIP annotations (p4 §4.1, p9 §B.2), and
     (b) R² / Spearman ρ against **Boltz-2's own predicted affinity**, not against measured affinity.
     Verbatim, p9: "We build a training set for LASSO regression by obtaining Boltz-2 predictions for
     affinity values in 980 systems from PLINDER, held out from the PairSAE training set." **This is
     the single most important qualification on the affinity result: the regression target is the
     model's output, so R² = 0.528 measures how well SAE features explain Boltz-2, not how well they
     predict binding.** The authors are consistent about this ("predict Boltz-2 affinity values",
     abstract p1) and it is not a defect — but it is trivially mis-cited as an affinity-prediction
     result.
  6. **Best/worst labels assigned against a held reference — NONE FOUND in the metrics; a
     presentation-level analogue exists.** The three features displayed in Fig 1 (889, 55, 885) are
     selected out of 16,384 and each is shown against the UniProt annotation that it already scores
     well on (token F1 0.58 / 0.79 / 0.93, p2). No selection rule for these three is stated. Same
     for features 1770/1774 (Fig C.8, p12) and 3888 (Figs C.9–C.10, pp. 12–13). The *aggregate*
     numbers (Table 1, Fig 2) are not affected by this; only the qualitative displays are.
  7. **Design-level oracle use (route 7, weaker than pipeline leakage) — PRESENT, and it is the only
     route that fires.** The showcase systems are chosen because the expected concept is already
     known: 1NEK is displayed for a *transmembrane* feature, 4K1I for a *disulfide bond* feature,
     1HPS for a *protease active site* feature (p2, Fig 1 caption). The answer is declared before
     the panel is read. This is **design-level, presentational, and does not touch the held-out F1
     or R² numbers** — it must not be conflated with pipeline leakage.

  **Summary: no pipeline oracle leakage; one design-level (route 7) instance confined to the
  qualitative figures. Two genuine open holes are not leakage but limit checkability: template
  status is unreported (route 1), and no SAE hyperparameter sweep is reported (route 4).**
- **prospective**: **no.** Entirely retrospective: deposited PLINDER/PoseBusters complexes, existing
  UniProt/SIFTS/PLIP annotations, and a regression onto Boltz-2's own outputs. Nothing is predicted
  ahead of an unknown, and no new measurement of any kind is made. Held-out *splits* exist and are
  respected (p9), which is good practice but is not prospectivity.
- **state_metric**: **NOT APPLICABLE — no conformational state is ever called, by any means.** For
  the record, the *concept* metric (the thing this paper measures instead) is a **binary predicate**:
  p9, eq. (9), "ŷj = 1{hi > τij}", with τ grid-searched "at increments of 0.1 across the unit
  interval" after each feature is normalised to [0,1] (p4). Reporting threshold: F1 ≥ 0.50, applied
  twice (complex-level recall and token-level recall). That threshold is asserted, never justified
  (p4, p9).
- **metric_saturation**: **Yes, in one arm — the ESM2-650M baseline floors at the token level.**
  Table 1, p4: ESM2-650M token F1 = **0.8%**, i.e. 8 of 1,053 concepts clear F1 ≥ 0.5. In Fig 2
  right (p4) the ESM2 bars are 2, 1, 2, 0, 3, 0, 0, 0, 0 across the nine categories — six of nine
  are exactly zero, so the baseline is at or near the floor across most of the axis and cannot
  register any further degradation. A floored baseline makes the headline gap (0.8% → 29.1%) look
  larger than a non-floored comparator would. **Second, separate saturation: the PLIP (15) category
  scores 0 for all three methods in both panels** (Fig 2, p4) — a complete floor, i.e. no method
  recovers a single PLIP interaction-fingerprint concept. This null is never discussed in the text.
  PairSAE's own numbers do not saturate (29.1% / 53.2% are far from 100%; test R² 0.528 far from 1).
  Axis-truncation and thresholding issues in Fig 2 are recorded in `hides`, not here, per v3 rule 9.
- **directional_control**: **NOT APPLICABLE — and this is the load-bearing negative finding of this
  note.** There is no handle of any kind. The method is read-only: it decodes activations, it never
  writes them back. No partner, ligand, nanobody, template, MSA filter, seed or subsample depth is
  used to direct anything, and **no SAE feature is ever clamped, ablated, amplified or otherwise
  intervened upon**. The authors say so themselves, listing it as future work — verbatim, p5: "Future
  work includes scaling up the study to more layers and recycling steps, integrating PairSAE features
  into automated interpretability pipelines to accelerate concept discovery, and **developing
  steering methods for interpretable protein design via feature interventions.**" See section D and
  the Tags note for why `latent-steering` is therefore **not** applied.
- **anti_memorization_design**: **Held-out splits exist and are specified; no post-cutoff or
  time-based set exists anywhere.** Two things must be kept apart:
  - **SAE/probe level — design present, n given.** p9: threshold set 7,680 complexes, validation set
    2,560, test set 5,120 "randomly selected complexes"; concepts restricted to those "that appear on
    at least five different complexes". Affinity: 980 PLINDER complexes "held out from the PairSAE
    training set" (p9), external test set PoseBusters (n = 299). Splits inherit PLINDER's train
    partition; **how PLINDER's splits were defined (sequence identity? pocket similarity? date?) is
    never described in this paper**, and the probe test set is described only as "randomly selected",
    which implies random, not similarity-aware, splitting.
  - **Backbone level — NONE.** There is **no cutoff of any kind**, no post-cutoff structure set, and
    no acknowledgement that Boltz-2's own training data plausibly contains the PLINDER and
    PoseBusters complexes being probed. Every complex analysed may be a complex Boltz-2 memorised.
    This possibility is not raised anywhere in the PDF.
- **anti_memorization_control**: **RUN at the SAE/probe level; NONE RUN at the backbone level.**
  - Run and analysed: test-set F1 is what Table 1 and Fig 2 report (p4); test R² = 0.528 / 0.367 and
    test Spearman ρ = 0.805 / 0.706 are reported alongside train (Table B.2, p10); the feature-3888
    group difference is **replicated on the PoseBusters test set** (Fig C.9 bottom, p12: Welch
    t = −7.83, p = 8.70e-14, Δμ = −1.01, 95% CI [−1.26, −0.753]) as well as on train, and feature
    2299 likewise has both a train panel (Fig C.9 left, p12) and a test panel (Fig 3 centre, p5).
    These are real held-out arms, actually run.
  - Not run: no arm addresses whether Boltz-2 has memorised the probed complexes. **NONE RUN.**
  - Powered, not `UNPOWERED`: n = 5,120 test complexes for probing, 299 for affinity; the smallest
    subgroup in any test panel is n = 137 (Fig C.9 bottom).
- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| **ESM2-650M last-layer neurons** probed identically (same threshold search, same F1 ≥ 0.5 criterion) | That any high-dimensional protein embedding trivially yields these concept F1s — i.e. that the concepts are easy. Complex-level 19.7% vs 53.2%; token-level 0.8% vs 29.1% | p4 (Table 1), p4 (Fig 2) |
| **Two independently trained PairSAEs at different depths** (R3-L33 and R3-L64, both third recycling step) | That the result is an artefact of one arbitrarily chosen layer; also exposes the layer dependence (L33 better on concepts, L64 better on affinity) | p4 (Table 1), p10 (Table B.2), p11 (Fig C.7) |
| **Three-way disjoint split for probing**: threshold on 7,680, feature selection on 2,560, F1 reported on 5,120 | That the reported F1s are inflated by fitting the threshold and picking the best of 16,384 features on the same data they are scored on | p9 (§B.2) |
| **Affinity regression trained on 980 complexes explicitly held out from PairSAE training** | Contamination between SAE dictionary learning and the downstream affinity regression | p9 (§B.3) |
| **External test set for affinity: PoseBusters, a different corpus from the PLINDER training pool** | That the affinity signal is a within-PLINDER idiosyncrasy; gives a genuine distribution-shift test | p5, p9 (§B.3), p10 (Table B.2) |
| **Cross-validated λ for LASSO** (λ = 0.009 for R3-L64, 0.006 for R3-L33) | Overfitting the sparsity level to the training fit; also yields the 291 / 237 nonzero-feature counts | p5, p10 (Table B.2) |
| **Full LASSO regularisation path** over log10 λ, all 16,384 coefficients plotted | That the "most influential features" are an artefact of one λ; shows which features survive as λ grows | p11 (Fig C.7) |
| **Welch t-tests with Δμ and 95% CIs** on affinity split by feature-on vs feature-off (unequal-variance, so unequal group sizes are handled) | That the feature/affinity group difference is chance. f2299 test: t = 11.23, p = 2.17e-19, Δμ = 1.44, CI [1.19, 1.7], n = 47/252 | p5 (Fig 3 centre), p12 (Fig C.9) |
| **Train-and-test replication of the group difference for feature 3888** | That the group difference is a training-set artefact. Train t = −15.27, p = 7.51e-47, n = 405/575; test t = −7.83, p = 8.70e-14, n = 162/137 | p12 (Fig C.9 right + bottom) |
| **Opposite-sign counterpart feature** (f2299 activates on *higher* affinity, f3888 on *lower*) | That the effect is a one-directional artefact of the max-pooling or of feature sparsity | p11 (§C text), p12 (Fig C.9) |
| **Train/test label-shift diagnostic** on the affinity response variable | Mistaking distribution shift for model error; explains why residuals grow at high predicted affinity | p5, p10 (Fig B.4) |
| **MSA-on vs MSA-off comparison of Boltz-2 outputs** across six affinity output heads on PoseBusters | Quantifies (does not remove) the confound introduced by running the whole study without MSAs | p10 (text), p11 (Fig B.6) |
| **Concept-frequency floor: concepts restricted to those appearing on ≥ 5 complexes** | F1 inflation on ultra-rare concepts where a single lucky match saturates the score | p9 (§B.2) |
| **95% sequence-correspondence requirement for SIFTS mapping**, unmatched sequences dropped | Mis-assigned UniProt annotations from loose PDB→UniProt mapping | p9 (§B.2) |

  **Controls conspicuously *absent*** (recorded here because for an interpretability paper the
  missing nulls are as informative as the run ones; each is a genuine gap, not a paraphrase of a
  stated limitation):
  - **No shuffled-label / permutation null.** The probe never scores a feature against randomised
    annotations, so there is no empirical null distribution for "F1 ≥ 0.5 by chance" given 16,384
    features searched per concept. With 16,384 candidate features per concept, a multiple-comparison
    null is exactly what the design calls for and it is not run.
  - **No random-feature or untrained-SAE baseline.** ESM2 neurons are the only comparator; a random
    projection of the same 512-dim input, or an untrained/randomly-initialised PairSAE, is never
    probed.
  - **No ablation of the pair-representation contribution.** *This is the most important omission for
    anyone citing this paper as evidence about the pair tensor:* the paper never trains a
    sequence-only SAE (i.e. on `s_i` alone, without `m_i` and without the `L(z_ij)` term) and
    compares it. There is therefore **no evidence in this paper that the pair representation
    contributes anything over the sequence representation alone** — the ESM2 baseline is a different
    model entirely and does not isolate this. The whole architectural argument rests on the
    quadratic-blow-up motivation (p1, p2), not on a measured ablation.
  - **No sweep of `r` (SVD truncation rank), `D` (dictionary size), or the Matryoshka nested
    widths.** The Matryoshka loss is adopted on the strength of a citation — p3: "It has recently
    been shown that a Matryoshka SAE loss [Bussmann et al., 2025] exhibits robust performance across
    dictionary sizes" — and no dictionary-size sweep is run here to check it.
  - **No reconstruction-quality numbers.** Neither sequence nor pair reconstruction error, nor
    explained variance, nor the achieved L0 / BatchTopK k, nor dead-feature counts, are reported
    anywhere — despite an auxiliary loss being included specifically to "revitalize dead features"
    (p4). The SAE is never evaluated *as an autoencoder*.
  - **No intervention/causal arm of any kind** (see `directional_control` and section D).
- **confidence_as_discriminator**: **No — pLDDT, pTM and ipTM are never mentioned, let alone used or
  validated.** No confidence measure gates any analysis. Two adjacent points worth having: (i) the
  Boltz-2 *affinity probability* head appears only as one of six output distributions in the MSA-on/off
  diagnostic (Fig B.6, p11) and is never used as a filter or discriminator; (ii) where the paper does
  judge prediction quality — the docked poses in Fig C.10 — it does so **purely visually and without
  any metric**, p11: "the predicted complexes do not appear to present a plausible docked pose: the
  small molecule is displaced from the protein interface and does not form stable contacts." An
  obvious missed control: they had feature 3888 flagging exactly these complexes and never checked it
  against Boltz-2's own confidence or against a PoseBusters validity check.

## D. Claims

- **central_conclusion**: Naively applying a sparse autoencoder to a pairformer's pair tensor scales
  quadratically and splits concepts across the sequence and pair spaces, so PairSAE first compresses
  the pair tensor into a per-token rank-64 two-sided SVD summary of each token's row/column
  interaction role, concatenates it with the sequence embedding, and learns a **single shared
  dictionary that decodes back into both spaces**. Applied to Boltz-2 at two depths, the resulting
  features are (a) far more predictive of UniProt/PLINDER residue and system annotations than
  ESM2-650M last-layer neurons (53.2% vs 19.7% of concepts at complex-level F1 ≥ 0.5; 29.1% vs 0.8%
  at token level), and (b) sparsely predictive of Boltz-2's own affinity output (test R² = 0.528 with
  291 of 16,384 features), with individual features showing large, test-set-replicated group
  differences in predicted affinity. **The paper demonstrates that these concepts are *legible* in
  the representation; it does not demonstrate that any feature is *causally* used by the model.**
- **necessity_claims** — verbatim, with pages. No sentence in the paper uses "necessary", "essential"
  or "required" of the method itself; the necessity-shaped claims are all *impossibility/inadequacy*
  claims about the naive alternative, which are what motivate the architecture:
  - p1 (Abstract): "Standard sparse autoencoders (SAEs), effective on transformer-style sequence
    embeddings, do not transfer cleanly to pairformer-like architectures: naïvely operating on
    pairwise representations yields a quadratic blow-up of features and obscures concepts distributed
    jointly across sequence and pair representations."
  - p1 (Introduction): "Answering this requires interpretability – explanations that let researchers
    assess prediction reliability and biophysical plausibility – yet the highly nonlinear
    architectures of deep models make such analysis challenging."
  - p2: "However, applying SAEs naively to structure prediction models is nontrivial."
  - p2: "Learning separate dictionaries per pair scales quadratically and obscures analysis, and
    repeated pair–sequence interactions suggest features may be superposed across both spaces."
  - p3: "Pairwise embeddings impose no structure, so we first compress them into a token-wise summary
    that preserves row/column interaction roles."
  - p3 (mechanistic premise about the pair tensor, load-bearing for anything that manipulates it):
    "Pair representations control the information flow in the updates of the sequence-level
    embeddings at each layer of the pairformer, by biasing the attention logits Abramson et al.
    [2024]."
- **novelty_claims** — verbatim, with pages. **The paper makes no explicit "first", "novel" or
  "unprecedented" claim anywhere.** The strongest formulations are introduction-of-method sentences:
  - p1 (Abstract): "We introduce PairSAE, which summarizes pairwise tensors via an N -mode SVD into
    token-wise interaction roles, then uses a sparse autoencoder to learn a shared set of token-level
    features that decode into both sequence and pair representations."
  - p1 (Abstract): "These results indicate that PairSAE links the latent space of foundation models
    for structural biology to interpretable structural concepts, clarifying what the model "knows"
    while avoiding pairformer-induced pitfalls that limit conventional SAEs."
  - p2: "To address this, we introduce PairSAE, which reconstructs both sequence-level and pairwise
    embeddings from a shared feature set."
  - p5 (Conclusion): "We introduced PairSAE, a sparse dictionary learning method that discovers a
    shared feature basis jointly explaining sequence and pair representations in pairformer-style
    models."
  - The paper explicitly situates itself after prior SAE work on pLMs and on structure prediction
    (p2 cites Simon and Zou 2024, Adams et al. 2025, Garcia and Ansuini 2025, Gujral et al. 2025, and
    **Parsan et al. 2025, "Towards interpretable protein structure prediction with sparse
    autoencoders"**, LMRL @ ICLR 2025, p7) — i.e. it does not claim to be the first SAE applied to a
    structure predictor, only the first to handle the pair representation jointly.
- **stated_limits** — the authors' own, verbatim:
  - p5 (Conclusion): "A key limitation is that we did not map ligand-activating sparse features to
    specific concepts, due to the lack of ligand annotations." This is significant because the
    affinity result rests on ligand-activating features: p5, "By looking at the top 10 most
    influential features at both layers we find most of them to be activated on ligands, for which we
    have very limited annotations." So **the features that carry the affinity signal are precisely
    the ones that could not be interpreted.**
  - p9 (§B.1): "Due to compute constraints, we do not use the MSA when training and evaluating the
    PairSAE."
  - p10 (§B.3 text): "As MSA-based predictions are conditioned on more information, we expect these
    to be more accurate. In future work, we aim at replicating our analysis using MSA inputs."
  - p5 (text): "Errors increase at higher predicted affinity, partly due to label shift (fewer
    high-affinity examples in training than in PoseBusters; see Fig. 3)."
  - p5 (Conclusion, future work implying present absence): "Future work includes scaling up the study
    to more layers and recycling steps, integrating PairSAE features into automated interpretability
    pipelines to accelerate concept discovery, and developing steering methods for interpretable
    protein design via feature interventions."
  - p9 (Appendix A, an honest caveat on their own SVD step): "Unlike matrices, truncating the ordered
    left-singular vectors to their rk < nk columns and fitting a new, smaller core tensor does not
    yield an optimal (r1 , r2 , . . . , rN )-rank approximation of T in the Frobenius norm [De
    Lathauwer et al., 2000b]." They use the naive truncation regardless (p9, §B.1).
  - Not stated by the authors but implied by their own construction, recorded so it is not lost: the
    Monte Carlo approximation of the pair loss uses **a single j per i** (p4: "We speed up training by
    we computing a Monte Carlo approximation of the second summation and only consider a single j for
    each i" [sic, "by we computing"]), i.e. the pair reconstruction term sees `O(Ntok)` of the
    `O(Ntok²)` pairs per step.
- **stance** — **provisional; the user's call, not the extractor's.** Dual:
  - **`background`** — on subject matter. This paper is about concept legibility in a co-folding
    model's internals, and contains nothing conformational: no states, no ensembles, no RMSD, no
    GPCR/kinase/transporter. It cannot be cited for or against any conformational claim, and it
    supplies no comparator number that sits next to a conformational metric.
  - **`precedent`** — on the narrower point that the **pair representation of a co-folding model
    carries linearly-decodable, human-nameable structural concepts** (transmembrane region, disulfide
    bond, protease active site) at specific layers, and that a sparse dictionary over a compressed
    form of that tensor recovers them far better than a pLM embedding does. That is a precedent for
    treating the pair tensor as a structured, addressable object rather than an opaque activation.
    **Note the precedent is bounded: it is read-out, never write-in** (see `directional_control`).

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Concepts with complex-level F1 ≥ 0.50, PairSAE-R3-L32 | 53.2 | % of test concepts | UniProt/PLINDER/PLIP annotations, 5,120-complex test set | p4 (Table 1) |
| Concepts with complex-level F1 ≥ 0.50, PairSAE-R3-L64 | 49.6 | % of test concepts | same | p4 (Table 1) |
| Concepts with complex-level F1 ≥ 0.50, ESM2-650M | 19.7 | % of test concepts | same | p4 (Table 1) |
| Concepts with token-level F1 ≥ 0.50, PairSAE-R3-L32 | 29.1 | % of test concepts | same | p4 (Table 1) |
| Concepts with token-level F1 ≥ 0.50, PairSAE-R3-L64 | 24.0 | % of test concepts | same | p4 (Table 1) |
| Concepts with token-level F1 ≥ 0.50, ESM2-650M | 0.8 | % of test concepts | same (floored — see `metric_saturation`) | p4 (Table 1) |
| Implied denominator for Table 1 | 1,053 | concepts | derived: Fig 2 bar counts ÷ Table 1 percentages reconcile exactly at 1,053 (complex L32 561/1053 = 53.2%; token L32 307/1053 = 29.2%; complex L64 521/1053 = 49.5%; token L64 252/1053 = 23.9%; complex ESM2 207/1053 = 19.7%; token ESM2 8/1053 = 0.8%). **Fig 2's own parenthesised category counts sum to 1,253** | p4 (Table 1 + Fig 2); see `unresolved` |
| Feature 889 (R3-L33), transmembrane proteins | token F1 0.58; complex F1 0.65 | F1 | UniProt transmembrane annotation, PDB 1NEK | p2 (Fig 1) |
| Feature 55 (R3-L33), disulfide bonds | token F1 0.79; complex F1 0.81 | F1 | UniProt disulfide annotation, PDB 4K1I | p2 (Fig 1) |
| Feature 885 (R3-L64), protease active sites | token F1 0.93; complex F1 0.93 | F1 | UniProt active-site annotation, PDB 1HPS | p2 (Fig 1) |
| LASSO test R², R3-L64 | 0.528 | R² | Boltz-2 predicted affinity (nAV) on PoseBusters | p5, p10 (Table B.2) |
| LASSO test R², R3-L33 | 0.367 | R² | same | p10 (Table B.2) |
| LASSO train R², R3-L64 / R3-L33 | 0.816 / 0.770 | R² | Boltz-2 nAV, 980 PLINDER complexes | p10 (Table B.2) |
| LASSO test MAE, R3-L64 / R3-L33 | 0.607 / 0.713 | nAV units | Boltz-2 nAV on PoseBusters | p10 (Table B.2) |
| LASSO train MAE, R3-L64 / R3-L33 | 0.275 / 0.302 | nAV units | Boltz-2 nAV, train | p10 (Table B.2) |
| LASSO train RMSE, R3-L64 / R3-L33 | 0.131 / 0.164 | nAV units | Boltz-2 nAV, train | p10 (Table B.2) |
| Spearman ρ train, R3-L64 / R3-L33 | 0.913 / 0.893 | ρ | Boltz-2 nAV ranking, train | p10 (Table B.2) |
| Spearman ρ test, R3-L64 / R3-L33 | 0.805 / 0.706 | ρ | Boltz-2 nAV ranking, PoseBusters | p10 (Table B.2) |
| Nonzero LASSO coefficients at CV λ, R3-L64 / R3-L33 | 291 / 237 | features (of 16,384) | sparsity of the affinity explanation | p5, p10 (Table B.2) |
| CV-selected λ, R3-L64 / R3-L33 | 0.009 / 0.006 | LASSO λ | cross-validation on the 980-complex train set | p10 (Table B.2) |
| Feature 2299 (R3-L64) affinity group difference, **test (PoseBusters)** | Welch t = 11.23, p = 2.17e-19, Δμ = 1.44, 95% CI [1.19, 1.70]; off n = 47, on n = 252 | nAV | complexes where the feature activates vs not | p5 (Fig 3 centre) |
| Feature 2299 (R3-L64) affinity group difference, **train** | Welch t = 13.32, p = 3.71e-34, Δμ = 0.715, 95% CI [0.610, 0.821]; off n = 220, on n = 760 | nAV | same | p12 (Fig C.9 left) |
| Feature 3888 (R3-L33) affinity group difference, **train** | Welch t = −15.27, p = 7.51e-47, Δμ = −0.75, 95% CI [−0.846, −0.654]; off n = 405, on n = 575 | nAV | same (opposite sign) | p12 (Fig C.9 right) |
| Feature 3888 (R3-L33) affinity group difference, **test (PoseBusters)** | Welch t = −7.83, p = 8.70e-14, Δμ = −1.01, 95% CI [−1.26, −0.753]; off n = 162, on n = 137 | nAV | same | p12 (Fig C.9 bottom) |
| PLIP concept category recovery, all three methods, both recall levels | 0 of 15 | concepts with F1 ≥ 0.5 | PLIP interaction fingerprints | p4 (Fig 2) — never discussed in text |
| Dictionary size / expansion factor | 16,384 / 32× | features / ratio | SAE architecture (input dim 512) | p9 (§B.1) |
| SVD truncation rank r | 64 (per mode; 128-dim `m_i`) | singular vectors | pair-tensor compression | p9 (§B.1) |
| Boltz-2 representation dims | `ns` = 384 (sequence), `nz` = 128 (pair) | dimensions | Boltz-2 standard implementation | p9 (§B.1) |
| Training budget | 250,000 steps × 2,048 tokens/minibatch; Adam, lr 2e-4 | steps / tokens | SAE optimisation | p9 (§B.1) |
| **Structural accuracy (RMSD / TM / lDDT / DockQ / PoseBusters validity)** | **NOT REPORTED — none exists anywhere in the paper** | — | — | — |
| **SAE reconstruction quality (sequence or pair error, explained variance, L0, dead features)** | **NOT REPORTED** | — | — | — |
| **Experimental binding affinity** | **NOT REPORTED — the regression target is Boltz-2's *predicted* affinity, not measured affinity** | — | — | p9 (§B.3) |

- **n_predictions**: recorded separately as required.
  - **Systems for SAE training**: 40,000 PLINDER systems, ≤ 512 residues (p9). Tokens seen:
    250,000 steps × 2,048 tokens per minibatch = **512,000,000 token samples**, sampled at random
    (p9). One Boltz-2 forward pass per system, at recycling step 3, with layers 33 and 64 tapped.
  - **Complexes for linear probing**: 7,680 (threshold) + 2,560 (validation) + 5,120 (test) =
    **15,360** (p9).
  - **Complexes for affinity regression**: **980** train (PLINDER, held out from SAE training) +
    **299** test (PoseBusters; n inferred from Fig 3 centre and Fig C.9 bottom group sizes, p5/p12 —
    the paper never states the PoseBusters n in text) (p9).
  - **Samples per target**: **1.** A single Boltz-2 prediction per complex; no seeds, no replicates,
    no ensemble. The word "seed" does not appear in the paper. There is no notion of "predictions
    per target" in this design.
  - **Concepts evaluated**: 1,253 by Fig 2's parenthesised category counts, 1,053 by the denominator
    Table 1 implies (see `unresolved`).
  - **SAE models trained**: **2** (R3-L33, R3-L64). No seed replicates of the SAE itself.
- **comparable_to_ours**: *(left empty by the extractor, per v3 — populated by whoever holds
  `STATUS.md` and the manuscript)*
- **si_in_scope**: **SI HELD.** Appendices A (N-mode SVD), B (experimental details B.1–B.3) and C
  (additional results) are **inside this 13-page PDF**, pp. 9–13, and carry Table B.2 and Figures
  B.4–B.6 and C.7–C.10. **No external supplementary file is referenced anywhere**, and no data or
  code availability statement, repository link, or model-weights release appears in the PDF. So
  nothing is missing to an external SI — but note that **per-concept F1 values are never tabulated
  anywhere**, at any level of detail: only thresholded counts (Fig 2) and aggregate percentages
  (Table 1) exist, plus three hand-picked features in Fig 1. Recovering which specific concepts are
  learned is therefore impossible from the paper as published.

## F. Figures

One row per panel group. Split on `mark` or `measure`, not on `facet` (v3 rule 8).

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 2 | Three cherry-picked PairSAE features colour-mapped onto the Boltz-2 predicted cartoon of three PDB complexes | structure render | `RENDER \| facet: feature × system (3: f889 R3-L33 on 1NEK transmembrane, f55 R3-L33 on 4K1I disulfide, f885 R3-L64 on 1HPS protease site) \| views: 1 \| overlay: 1 Boltz-2 prediction on 0 references (per-residue activation colour-mapped, white→red) \| axis: none` | 3, varying by feature × system (not by camera angle) | Three features shown out of 16,384 with **no stated selection rule**; no indication how many were inspected. No colour scale on the render itself (the scale lives in the 1B strips below). | No licence statement in the PDF (checked p1 and p13); arXiv preprint, workshop paper. Reuse terms NOT REPORTED. |
| 1B | 2 | Per-residue activation strips for the same three features with UniProt ground truth marked | heatmap | `MATRIX \| rows: wrapped sequence line (4–5 per system) \| cols: residue position within line (~100) \| value: PairSAE feature activation, white→red, colourbars 0–1.562 / 0–2.440 / 0–6.648 \| facet: feature × system (3)` | 3 strips, each internally wrapped into 4–5 lines; letters overlaid are the residue codes | Ground-truth positives (blue) and activations (red) are on the **same glyphs**, so a residue that is both a true positive and highly activated is hard to read; per-strip colourbars have **different maxima** (1.562 / 2.440 / 6.648), so activation intensity is not comparable across the three panels. | as 1A |
| 2 | 4 | Count of annotation concepts recovered at F1 ≥ 0.5, by category, for three methods | bar | `PLOT \| facet: recall level (2: complex-level, token-level) \| vary: annotation category (9: Molecule processing 228, Regions 314, PLINDER labels 190, Sites 173, Amino acid modifications 175, Experimental info 134, Amino acid 21, Secondary structure 3, PLIP 15) \| series: method (3: ESM2-650M, PairSAE-R3-L32, PairSAE-R3-L64) \| measure: count of concepts with F1 ≥ 0.50 \| mark: bar \| n: 5,120 test complexes behind each bar; 1,253 concepts per panel by the axis labels (but the counts reconcile with Table 1 only at 1,053)` | 2 (same mark and measure, so one row per v3 rule 8) | **Reports a thresholded count, not the F1 distribution** — the underlying per-concept F1s are never shown, so a category could sit at 0.49 throughout and score zero. **Counts are not normalised to the wildly unequal category denominators** (3 to 314 concepts), so "Regions" and "Secondary structure" share a count axis with a 100× difference in opportunity. **Bar counts do not reconcile with Table 1's percentages against the parenthesised denominators** (see `unresolved`). No error bars, no CIs. | as 1A |
| 3A | 5 | LASSO-predicted vs actual Boltz-2 nAV, R3-L64 | scatter | `PLOT \| facet: none (1) \| vary: Boltz-2 nAV, −3.5 to +3 (continuous) \| series: split (2: Train, Test) \| measure: LASSO-predicted nAV \| mark: point \| n: 1 per mark; 980 train + 299 test per panel` | 1 | n per series not printed in the panel (recoverable only from §B.3 and other figures); train and test heavily overplotted with no transparency ordering stated. | as 1A |
| 3B | 5 | Distribution of nAV split by whether feature 2299 activates, PoseBusters test set | histogram (overlaid density) | `PLOT \| facet: none (1) \| vary: Boltz-2 nAV, −3.5 to +2.5 (continuous) \| series: feature 2299 state (2: off n=47, on n=252) \| measure: density \| mark: bar \| n: 47 and 252 complexes per series, 299 per panel` | 1 | Densities are normalised per group, so the 5.4× group-size imbalance (47 vs 252) is invisible in the bar heights; the n's are given in the legend, which mitigates this. | as 1A |
| 3C | 5 | Feature 2299 activation overlaid on a ligand in its binding site | structure render | `RENDER \| facet: none (1) \| views: 1 (close-up of the ligand in the pocket) \| overlay: 1 Boltz-2 predicted complex on 0 references (activation colour-mapped onto ligand atoms) \| axis: none` | 1 | One example, no colour scale, no indication of how representative it is of the 252 activating complexes. | as 1A |
| B.4 | 10 | Distribution of the Boltz-2 affinity response variable in train vs test | histogram (overlaid) | `PLOT \| facet: none (1) \| vary: Boltz-2 nAV, −4 to +3 (continuous) \| series: split (2: Train, Test (PoseBusters)) \| measure: relative frequency \| mark: bar \| n: 980 train, 299 test per series` | 1 | n's not printed in the panel. | as 1A |
| B.5 | 10 | LASSO-predicted vs actual Boltz-2 nAV, R3-L33 (the weaker layer) | scatter | `PLOT \| facet: none (1) \| vary: Boltz-2 nAV, −3.5 to +2.5 (continuous) \| series: split (2: Train, Test) \| measure: LASSO-predicted nAV \| mark: point \| n: 1 per mark; 980 + 299 per panel` | 1 | Same shape as 3A but plotted separately rather than as a two-panel facet, so the L33/L64 comparison the reader wants must be made across pages 5 and 10. n not printed. | as 1A |
| B.6 | 11 | Boltz-2 affinity outputs with MSA on vs off, six output heads, PoseBusters | histogram (overlaid) | `PLOT \| facet: Boltz-2 affinity output head (6: affinity_pred_value, _value1, _value2, affinity_probability_binary, _binary1, _binary2) \| vary: output value (continuous; ≈ −4 to +4 for value heads, 0–1 for probability heads) \| series: MSA setting (2: with MSA, no MSA) \| measure: count \| mark: bar \| n: PoseBusters complexes, NOT REPORTED per panel` | 6 (2 rows × 3 cols), varying by output head | **The text calls the difference "substantial" (p10) but no test statistic, effect size or CI is given for any of the six panels** — a claimed result with no quantitative panel. Counts (not densities) are used with no n stated, and the y-axis maximum differs per panel. The six output heads are never defined in the paper. | as 1A |
| C.7 | 11 | LASSO coefficient paths over the regularisation sweep, both layers | line | `PLOT \| facet: PairSAE layer (2: R3-L33, R3-L64) \| vary: log10(λ), ≈ −0.5 to −3.5 (continuous, plotted decreasing left to right) \| series: PairSAE feature (16,384 traces; ~6–8 labelled by feature id) \| measure: LASSO coefficient β_j \| mark: line \| n: 1 fit per λ; 980 training complexes per fit` | 2 | The λ axis runs **decreasing** left to right (−0.5 → −3.5), which inverts the usual reading direction for a regularisation path. y-ranges differ between panels (−0.2…0.6 left, −0.15…0.20 right), so the apparently larger coefficients in the left panel are partly an axis artefact. | as 1A |
| C.8 | 12 | Ligands activating the two top positive affinity features in R3-L33 | structure render | `RENDER \| facet: feature (2: 1770, 1774) \| views: 1 \| overlay: 1 Boltz-2 predicted complex on 0 references (activation colour-mapped onto ligand atoms) \| axis: none` | 2, varying by feature | One example per feature; no colour scale; **feature ids conflict with the body text** (p11 says "feature 1744 and 1770", the caption says "feature 1770 (left) and feature 1774 (right)"). | as 1A |
| C.9 | 12 | Affinity group differences for an up-feature and a down-feature, train and test | histogram (overlaid density) | `PLOT \| facet: feature × split (3: f2299 R3-L64 train, f3888 R3-L33 train, f3888 R3-L33 test) \| vary: Boltz-2 nAV, ≈ −3.5 to +3 (continuous) \| series: feature state (2: off, on) \| measure: density \| mark: bar \| n: 220/760, 405/575, 162/137 complexes per series` | 3 (2 top + 1 bottom) | Asymmetric coverage: f2299 gets train here and test in Fig 3, f3888 gets both here — so the two features are not presented on the same footing, and a reader comparing them must cross figures. Per-group density normalisation again hides the group-size imbalance (n's are in the legends). | as 1A |
| C.10 | 13 | Four complexes where feature 3888 activates, all with implausible ligand placement | structure render | `RENDER \| facet: example complex (4) \| views: 1 \| overlay: 1 Boltz-2 predicted complex on 0 references (feature 3888 activation on ligand atoms) \| axis: none` | 4, varying by example complex | **A claimed result with no quantitative panel at all.** The text asserts (p11) "the predicted complexes do not appear to present a plausible docked pose: the small molecule is displaced from the protein interface and does not form stable contacts" — a purely visual judgement over 4 hand-chosen examples, with no contact count, no PoseBusters validity check, no distance metric, and no comparison against feature-3888-inactive complexes. If true, this is the paper's most interesting finding (a feature that detects failed docking) and it is the least evidenced. | as 1A |

**13 panel-group rows across 11 figures** (Figs 1, 2, 3, B.4, B.5, B.6, C.7, C.8, C.9, C.10 — Fig 1
splits into 1A/1B, Fig 3 into 3A/3B/3C). Tables 1 (p4) and B.2 (p10) are tables, not figure rows.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), session 2026-09-08
- **schema_version**: v3
- **confidence**: **high** for method, data, splits, numbers, claims, and for the central negative
  finding (no intervention). The paper is short (5 pages of body text) and unusually explicit about
  its protocol. Specific reservations:
  - Figure axis category labels and the small in-panel statistics (Welch t, p, Δμ, CI, group n's)
    were read from **300 dpi and 110 dpi renders** of pp. 2, 4, 5, 10, 11, 12, 13 because the
    captions do not carry panel structure or in-panel annotations. Fig 2's nine category labels and
    all 54 bar values were confirmed at 300 dpi. The Fig 1 colourbar maxima (1.562 / 2.440 / 6.648)
    were read at 110 dpi and are the least certain numbers in this note.
  - The PoseBusters test n = 299 is **inferred** from group sizes (47+252 in Fig 3 centre; 162+137
    in Fig C.9 bottom, both summing to 299), not stated in text.
  - The implied Table 1 denominator of 1,053 is **derived arithmetic**, shown in full in
    `metrics_reported` so it is checkable; the paper states neither 1,053 nor 1,253.
- **unresolved**:
  1. **Layer 33 or layer 32?** The body text (p4) says "at layers 33 and 64 (R3-L33, R3-L64)", and
     Fig 1 (p2), Fig B.5 (p10), Table B.2 (p10) and Fig C.7 (p11) all label it **R3-L33**. But
     **Table 1 (p4) and the Fig 2 legend (p4) both say "PairSAE-R3-L32"**. Two of the paper's
     headline artefacts use L32 and everything else uses L33. Almost certainly a typo in Table 1 and
     Fig 2, but it is unresolvable from the PDF. This note uses the paper's own label wherever a
     number is quoted, so Table 1 numbers are attributed to "R3-L32" and Table B.2 numbers to
     "R3-L33". **A citation of "layer 33" should carry this caveat.**
  2. **How many pairformer layers does Boltz-2 have?** Never stated. Layers 33 and 64 cannot be
     placed as "early/middle/late" from this PDF alone, which weakens any depth-dependence claim.
     Likewise "third recycling step" — the total number of recycles is never given.
  3. **Table 1 and Fig 2 do not reconcile against Fig 2's own denominators.** Fig 2's parenthesised
     test-set concept counts sum to **1,253**, but the Fig 2 bar counts divided by Table 1's
     percentages give a denominator of **1,053**, consistently for all six method × recall-level
     cells (ratio 0.838–0.842 throughout). Either the parenthesised counts include ~200 concepts
     excluded from Table 1, or the categories overlap, or one of the two artefacts is wrong. Not
     resolvable from the PDF.
  4. **Feature 1744 or 1774?** p11 text: "we highlight how feature 1744 and 1770 from R3-L33 activate
     in two ligands in Figure C.8". Fig C.8 caption (p12): "Ligands activating on feature 1770 (left)
     and feature 1774 (right)."
  5. **Boltz-2 template setting is never stated** (see `templates`). MSA is explicitly off; templates
     are simply not mentioned.
  6. **The six Boltz-2 affinity output heads in Fig B.6** (`affinity_pred_value`, `_value1`,
     `_value2`, `affinity_probability_binary`, `_binary1`, `_binary2`) are never defined, and it is
     never said which one `AV` / `nAV` in eq. (8) refers to.
  7. **"nAV" is used in every figure axis label but defined nowhere**; from Fig 3's caption
     ("negative affinity values from Boltz-2 (higher means more affine)") it is the negated affinity
     value, while eq. (8) writes the target as `AV`. The sign convention is inferable, not stated.
  8. **No code, data or weights availability statement** anywhere in the PDF; no repository URL.
  9. **Venue year conflict**: "NeurIPS 2025" workshop footer (p1) vs arXiv stamp 25 Jun 2026 (p1) and
     `refs.bib` `year = {2026}`.
  10. **Typo in the body text, quoted [sic] above**: p4, "We speed up training by we computing a
      Monte Carlo approximation".
  11. **Tag I needed and could not use — none invented.** See the Tags section below for four
      vocabulary gaps I hit (an interpretability/probing method tag; a `read-only` vs `intervention`
      distinction; a way to record MSA-off without asserting no-templates; and a way to record a
      non-state binary predicate metric). All four are recorded there rather than resolved by
      inventing a tag.
- **why_it_matters**: *(left empty by the extractor — the user's call)*

---

## Tags

`general-protein` `cofolding` `preprint` `anti-memorization` `background` `precedent`

### Tag notes — every decision, especially the declines

**`latent-steering` — DELIBERATELY NOT APPLIED. This is the single most important tag decision in
this note and it is a decline.** The v3 definition is "any inference-time intervention on an internal
tensor — pair representation, trunk embedding, distogram head, conditioning embedding". **PairSAE
performs no intervention of any kind.** It is a read-out method end to end: activations are harvested
from a frozen Boltz-2, compressed, encoded, decoded, and probed. No feature is clamped, ablated,
scaled, added to a residual stream, or written back; no modified activation is ever fed forward; no
Boltz-2 output is ever shown to change as a result of anything the authors did to its internals. The
decoder matrices `D_s`, `D_z^row`, `D_z^col` (eq. 4, p3) exist only to define the reconstruction loss,
not to inject anything into the model. The authors state the absence themselves and place it in future
work — verbatim, p5: "**Future work includes** scaling up the study to more layers and recycling
steps, integrating PairSAE features into automated interpretability pipelines to accelerate concept
discovery, and **developing steering methods for interpretable protein design via feature
interventions.**" Applying `latent-steering` here would put a read-only paper into every reverse
lookup for intervention methods, which is exactly the drift the fixed vocabulary exists to prevent.
**Causal control is not demonstrated in this paper: interpretability only.** Anything this paper is
cited for must stay on the read-out side of that line.

**`cofolding` — APPLIED, with a caveat.** The paper is not a co-folding method, but it runs a
co-folding model (Boltz-2, on protein–ligand complexes) tens of thousands of times as its data source
(p4, p9), and its entire subject is the internals of a co-folding architecture. A reverse lookup for
co-folding papers should return this. `method_class` in section B correctly records it as `other`.

**`general-protein` — APPLIED.** PLINDER protein–ligand complexes with no family restriction (p4).
Explicitly **not** `gpcr` / `kinase` / `transporter` / `fold-switching` — none appears. The Fig 1
examples (a membrane respiratory complex, a viral neuraminidase, a viral protease) are incidental
showcases, not a studied system class.

**`preprint` — APPLIED.** arXiv:2606.27440v1 [cs.LG], 25 Jun 2026 (p1). Not `peer-reviewed`: it is a
NeurIPS workshop submission, and no journal or conference proceedings entry exists.

**`anti-memorization` — APPLIED, but read the caveat before using it.** Applied because the schema
field asks "Is there a held-out or post-cutoff set at all?" and there is: three disjoint probe splits
with n given, plus an external PoseBusters test set, and those arms were **actually run and analysed**
(p9, p10, p12), which is what `anti_memorization_control` asks for. **The caveat: this is
SAE-and-probe-level holdout, not a post-cutoff control against the structure model.** There is no
date cutoff anywhere, and the possibility that Boltz-2 memorised the PLINDER and PoseBusters
complexes being probed is never raised. A query using this tag to find papers that guard against
*backbone* memorisation will get a false positive here. `no-anti-memorization` was considered and
rejected as the worse of the two errors, since genuine held-out arms were run.

**`background` + `precedent` — APPLIED, both provisional (the user's call, per schema D).** Rationale
in `stance`. `contrast` was considered and rejected: the paper makes no claim this manuscript would
need to argue against, and its rigour is generally good within its own frame (clean three-way splits,
an external test set, a real baseline, replicated group differences). `threat` rejected for the same
reason — it competes with nothing conformational. `negative-result` rejected: the two null-ish
findings (PLIP category at 0/15; ligand features uninterpretable for lack of annotations) are
incidental, not the paper's result.

**Tags considered and DECLINED, with reasons — these are the decisions a future query will depend on:**

- **State handling (`single-state` / `two-state` / `ensemble` / `continuum`) — none applied.** There
  is no conformational sampling and no state assignment (see `states_generated`). Boltz-2 does emit
  one predicted structure per complex, so `single-state` is superficially tempting, but that tag
  family exists to describe what a *conformational* method produces, and applying it would
  false-positive every conformational-state query with a paper that has no state analysis in it.
- **Metric (`binary-predicate` / `continuous-metric` / `rmsd-only` / `visual-metric` /
  `saturating-metric`) — none applied.** The corpus's only metric field is `state_metric`, and there
  is no state. For the record the paper *does* use a binary predicate (eq. 9, p9), *does* use
  continuous metrics (R², ρ), *does* make one purely visual claim (Fig C.10, p13), and *does* have a
  floored baseline arm (ESM2 token-level, 0.8%) — so under a *non-state* reading, four of the five
  would fire. **This is a genuine v3 gap: the Metric tag family is implicitly scoped to conformational
  state but the vocabulary section does not say so**, and an extractor reading the tag list alone
  would tag all four. Recorded, not resolved by invention.
- **Protocol (`no-template-no-msa` / `templates-on` / `state-annotated-input`) — none applied.**
  MSA-off is stated flatly and repeatedly (p9, p10), but **template status is never stated**, so
  `no-template-no-msa` — a compound tag asserting both — cannot be applied without inferring the
  template half, which the field rules forbid. `templates-on` is likewise unsupported.
  **Second genuine v3 gap: there is no atomic tag for "MSA disabled", so the single most
  consequential protocol fact about this paper is untaggable.** It is recorded in `msa_handling`
  instead, where only a full-text query will find it.
- **`multi-backbone` — declined.** One structure backbone (Boltz-2). ESM2-650M is a protein *language*
  model used as a probe baseline on last-layer neurons (p4), not a second structure predictor.
- **`msa-subsample` / `msa-state-filter` — declined.** The MSA is switched off entirely, not
  subsampled and not substituted. Per the schema's own warning these are different things, and
  "absent" is a third thing again.
- **`oracle-leak` — declined.** No pipeline route fires (see `oracle_leakage`, routes 1–6).
- **`design-level-oracle` — declined, narrowly, and this is the closest call after `latent-steering`.**
  Route 7 *does* fire (the Fig 1 showcase systems are chosen because the expected concept is already
  known, p2). But it fires only on three qualitative panels and touches no reported metric — the
  held-out F1s and R² are unaffected. Tagging it would put this paper alongside papers whose *result*
  depends on a declared-in-advance answer, which would misrepresent it. The instance is recorded in
  full under `oracle_leakage` route 7 so a full-text query still finds it.
- **`prospective` — declined.** Entirely retrospective (see `prospective`).
- **`unpowered` — declined.** n = 5,120 test complexes for probing, 299 for affinity, smallest
  subgroup 137.
- **`confidence-as-discriminator` — declined.** pLDDT/pTM/ipTM never used or mentioned.
- **`experimental` / `experimental-validation` — declined.** No wet-lab work; and `experimental` is
  wrong because the paper *does* run structure prediction (Boltz-2 forward passes are its whole data
  source). **Third v3 gap: `experimental` is described as "a paper with no structure prediction in it
  at all, whose section C will be mostly NOT APPLICABLE by design rather than by sloppiness" — that
  second clause describes this paper exactly, but the first clause excludes it.** There is no tag for
  "computational paper whose section C is legitimately empty because it is not a conformational
  method". An `interpretability` or `probing` method tag would fix this cleanly.
- **Control tags (`directed-state`, `partner-driven`, `ligand-driven`, `peptide-driven`,
  `g-protein-mimetic`, `nanobody`, `apo-sampling`, `seed-only`) — none applied.** There is no control
  handle at all (see `directional_control`). Note `ligand-driven` is tempting because every system is
  a protein–ligand complex, but that tag means using a ligand to drive a *conformational state*, and
  nothing is driven here.
- **Site tags (`orthosteric`, `allosteric-site`, `cryptic-pocket`, `allosteric-failure`) — none
  applied.** Feature 885 recovers "protease active sites" (p2) and the PLINDER complexes are ligand
  sites generally, but these tags mark conformational study of a site, not concept recovery at one.
- **`md`, `md-emulator`, `enhanced-sampling`, `af-cluster`, `benchmark-only`,
  `template-state-bias` — declined**, none present.
- **`figure-exemplar` — declined.** The definition is "kept mainly for its figures … must be excluded
  from gap analysis". This paper is held for its content (what the pair representation encodes), not
  its figures, and it should **not** be excluded from gap analysis. Fig 1B's sequence-activation strip
  paired with a colour-mapped render, and Fig C.7's labelled LASSO path, are nonetheless reusable
  designs and are fully specified in section F for that purpose.
- **`comparator-numbers` — declined.** Its numbers (concept F1 counts, R² against a model's own
  output) have no conformational counterpart to sit beside. `si_in_scope` records that per-concept
  F1s are never tabulated at all, so even the numbers it has are not extractable at per-item
  granularity.

**Fourth v3 gap, stated plainly since the schema is still being tuned:** the Method tag family has no
entry for interpretability/probing/representation-analysis work, so the defining property of this
paper — that it *reads* an internal tensor without touching it — is expressible only as the *absence*
of `latent-steering`. Absence is not searchable. A `probing` or `interpretability` tag, paired with
`latent-steering` for the write-in case, would make the read-out/write-in distinction a first-class
query, which is precisely the distinction this paper turns on.
