# chakravarty2024memorization

> **NO PDF HELD.** Extracted 2026-09-14 from the **PMC full-text XML** (PMC11344769, NCBI
> efetch), preserved at `source/pending_text/chakravarty2024memorization.{txt,pmc.xml}` —
> **not in git**. **Locators are section names, not page numbers** — cite as
> `[chakravarty2024memorization, Results]`. Same convention as `yu2026domainmotion`,
> `eddy2018extrinsictrp`, `aureli2026epath`, `kohlhoff2014gpcr`, `ingraham2023chroma`.

## A. Identity

- **citekey**: `chakravarty2024memorization`
- **doi**: 10.1038/s41467-024-51801-z. PMCID PMC11344769.
- **year, venue**: 2024, *Nature Communications* **15**:7296. Peer-reviewed, open access.
- **title, authors**: "AlphaFold predictions of fold-switched conformations are driven by
  structure memorization." Chakravarty, D.; Schafer, J. W.; Chen, E. A.; Thole, J. F.;
  Ronish, L. A.; Lee, M.; Porter, L. L.
- **not to be confused with** `chakravarty2026statespace` (arXiv 2608.02866), the same lab's
  2026 perspective/roadmap. Different paper, already in the corpus.

> **WHY IT IS HERE.** It is **the paper the field cites** for the claim that predictor confidence does not
> discriminate correct alternative conformations from incorrect ones — `suzuki2026conforflux`
> cites it at p.8 as the authority for exactly that. **C8 is the only title clause with data behind it**, and
> until now we defended it with `bryant2024cfold`, `ku2026promise` and `sun2026kinconfbench`.
> **This paper is stronger than all three, because its finding is directional rather than
> null.** Added 2026-09-14 after a bibliography sweep of held PDFs against `refs.bib`.

## B. Scope

- **system**: general protein — **92 fold-switching proteins**, each with two experimentally
  determined conformations. No GPCR.
- **n_targets**: 92. Anti-memorization framing is built in: *"Both conformations of all 92 fold
  switchers were deposited in the Protein Data Bank (PDB) before AF2[‑training]."*
- **method_class**: **benchmark-only, adversarial.** No new method.
- **backbones**: **AF2 (several protocols, incl. AF-Cluster and shallow MSA subsampling), AF2Rank,
  and AF3.** Note the scope line: *"AF3 has also just been released as a webserver and has not
  yet been tested on fold-switching proteins."*
- **templates**: off for the AF-Cluster arm — *"All predictions following the AF_Cluster
  pipeline, were generated without templates, as in the original manuscript."*
- **msa_handling**: **subsampled and clustered.** Shallow MSA subsampling and AF-Cluster
  (ColabFold + DBSCAN, run on the NIH Biowulf cluster). *"Randomly subsampled MSAs inputted at
  each recycle."*

## C. Conformational core

- **states_generated**: two-state by construction (Fold1 / Fold2), ensembles per protocol,
  reranked by confidence into Top1 / Top10 / All.
- **structural_priors_used**: both target conformations are deposited and known in advance;
  AF2Rank is run with each fold-switched conformation supplied **as a template**, with
  *"sidechain atoms … removed to prevent AF2 from using the underlying amino acid sequence to
  influence its prediction confidence."*
- **oracle_leakage**: route 5/6 by design — success is similarity to two known deposited folds.
  The design is adversarial, so the leakage is the instrument, not a defect.
- **prospective**: no.
- **state_metric**: structural similarity to each of the two deposited folds, plus a
  **confidence-stratified success count**. Confidence bands are defined operationally:
  *"Confidences are determined by ≥70% (medium), 80% (good), 90% (high) of residues with Cα
  plDDT scores ≥70."*
- **confidence_as_discriminator**: **YES, tested directly, and it FAILS DIRECTIONALLY — this
  is the field's reference result and the reason the note exists.**

## D. Claims

- **central_conclusion**: Across 92 fold-switching proteins whose *both* conformations predate
  AF2's training data, all AF2-based methods and AF3 succeed on only a minority, and AF2's
  confidence metrics do not merely fail to rank alternative conformations — they **actively
  select against** the experimentally observed ones.

- **THE QUOTES THIS NOTE EXISTS FOR** (verbatim, `[chakravarty2024memorization, Results]`
  unless marked):
  1. > "Further, AF2's confidence metrics **select against alternatively folded protein
     > conformations** and **cannot discriminate between low and high energy conformations** of
     > fold-switching proteins."
  2. > "**Neither of AF2's confidence metrics successfully discriminated between good and
     > inaccurate fold-switch predictions**"
  3. > "Rather, both plDDT and pTM scores **assigned lower confidences to diverse correctly
     > predicted conformers and higher confidences to predictions that have not been observed
     > experimentally**."
  4. > "more experimentally unobserved conformations are selected as prediction confidence
     > increases" *(Fig. 2a caption)*
  5. > "AF2's structure module predicts the lower energy conformations of fold switchers with
     > better accuracy and higher confidence than higher energy conformations **50% of the time,
     > equal to random chance**." *(Fig. 2b caption)*
  6. > "These results strongly indicate that AF2's confidence metrics **select against
     > experimentally consistent predictions** of fold switchers, especially Fold2, in favor of
     > experimentally inconsistent predictions."
  7. > "we found that all AF2-based methods and AF3 predict fold-switching proteins likely in
     > its training set with modest success (**32/92**)."
  8. > "AF2's inability to discriminate between good and poor predictions of fold switchers
     > suggests that its confidence metrics **may have broader limitations**."
  9. > "Thus, high confidence AF2 predictions that differ from experimentally determined
     > structures **do not necessarily correspond to folding intermediates**, consistent with
     > previous observations."

- **stated_limits**: the two deposited folds are used as *"a minimalist approximation of a
  folded protein energy landscape"* — the authors concede the landscapes are *"populated by many
  more conformations than their two distinct experimentally determined conformations."*

- **stance**: **precedent + threat, and it strengthens C8.** Precedent because it is the
  citable authority for the confidence claim. Threat because **quote 8 generalises the failure
  beyond fold switchers**, which includes our receptors, and because its memorization result is
  the same shape as `yu2026domainmotion`'s training-prior finding.

## E. Quantitative comparators

| quantity | value | scope | locator |
|---|---|---|---|
| Fold switchers benchmarked | **92** | both conformations deposited pre-training | Results |
| Success across all AF2 methods + AF3 | **32 / 92** | "modest success" | Results |
| Structure module picks the lower-energy fold better/more confidently | **50%** | "equal to random chance" | Fig. 2b |
| Confidence bands | ≥70% / 80% / 90% of residues with Cα plDDT ≥ 70 | medium / good / high | Methods |
| High-confidence threshold | plDDT ≥ 90 high; 70–90 confident | per-residue | Methods |

- **comparable_to_ours**: **Directly on C8, and it is the strongest form of the claim in the
  corpus.** Our other C8 supports report *absence* of a relationship (`bryant2024cfold`
  R = 0.52 for state vs > 0.9 for accuracy; `ku2026promise` confidence ≈ random). **This paper
  reports an inverted one.** If our own confidence result is merely null, this paper is the
  contrast that says the field's best-documented case is worse than null — and our result
  should be positioned against it explicitly, not alongside it.
- **si_in_scope**: Supplementary Figs referenced in text, **not retrieved**.

## F. Figures

**NOT EXTRACTED (panels not viewed).** Figure content above is taken from caption text in the
XML. Fig. 2 is the confidence panel group (2a confidence-stratified success bars; 2b
lower-vs-higher-energy accuracy). **Do not use this note for figure-design queries** without
retrieving the figures. Licence: CC BY (Nature Communications open access) — check before
adapting.

## G. Provenance

- **extracted_on, by**: 2026-09-14, lit-3d, from PMC11344769 full-text XML via NCBI efetch.
- **schema_version**: `v3.2`
- **confidence**: **high for every quoted string** — all verified mechanically against the
  retrieved full text by `validate/quotecheck_plaintext.py`. **Medium** for section-level
  attribution: PMC XML does not carry page numbers, and I have assigned quotes to Results /
  Fig. captions / Methods by position in the body, not from a printed article.
- **unresolved**:
  1. **No page numbers.** Printed pages are Nat Commun 15:7296 (article-numbered). Section
     names are the locator.
  2. **Supplementary figures not retrieved**, including the AF2-multimer and AF3 panels.
  3. **The per-method breakdown of 32/92** — which of the AF2 protocols and AF3 contributed
     what — is not extracted here.
  4. **Figures not viewed.**
- **why_it_matters**: *(user's call — left empty per SCHEMA)*
