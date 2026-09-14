# monteirodasilva2024subsampled

> **NO PDF HELD.** Extracted 2026-09-14 from the **PMC full-text XML** (PMC10973385, NCBI
> efetch), preserved at `source/pending_text/monteirodasilva2024subsampled.{txt,pmc.xml}` —
> **not in git**. **Locators are section names, not page numbers** — cite as
> `[monteirodasilva2024subsampled, Results]`.

## A. Identity

- **citekey**: `monteirodasilva2024subsampled`
- **doi**: 10.1038/s41467-024-46715-9. PMCID PMC10973385.
- **year, venue**: 2024, *Nature Communications* **15**(1):2464. Peer-reviewed, open access.
- **title, authors**: "High-throughput prediction of protein conformational distributions with
  subsampled AlphaFold2." Monteiro da Silva, G.; Cui, J. Y.; Dalgarno, D. C.; Lisi, G. P.;
  Rubenstein, B. M.

> **WHY IT IS HERE.** It is a **major peer-reviewed MSA-subsampling paper that was absent from
> an 83-paper corpus built around MSA subsampling** — found 2026-09-14 by sweeping held PDFs'
> bibliographies against `refs.bib`. And it asks a question **no other subsampling paper in the
> corpus asks**: not *can the alternative state be reached at all* but **can the relative
> populations be predicted** — the ensemble question this project has been circling.

## B. Scope

- **system**: general protein — the **Abl1 tyrosine kinase core** across the Src→Abl1
  evolutionary line, plus **GMCSF**. No GPCR.
- **n_targets**: `UNRESOLVED` — the kinase panel size is not extracted here; point and double
  mutants are the unit of the main result.
- **method_class**: MSA subsampling applied at inference, with a population readout;
  benchmark + method.
- **backbones**: **AF2** only.
- **msa_handling**: **subsampled**, with the depth swept as the method's own parameter.
  `UNRESOLVED`: the exact `max_seq`/`max_extra_seq` grid is not extracted here.

## C. Conformational core

- **states_generated**: **a distribution, not a state** — this is the distinguishing property.
  The output is a predicted population over conformational states.
- **state_metric**: **population fraction of the active state**, compared against experiment.
- **directional_control**: the handle is **sequence** (mutations), read through subsampled AF2;
  subsampling is the sampler, mutation is the perturbation.
- **input_factor_design**: **v3.2.** **MSA**: varied (subsampling depth swept).
  **sequence**: varied (point and double mutants). **templates / ligand / partner**: not varied.
  `crossings:` **MSA × sequence** — depth is swept to find an operating point and the mutation
  series is then run at it; `UNRESOLVED` whether the full grid is crossed or the depth is fixed
  first. **Do not tag `factors-crossed` without checking.**
- **anti_memorization_design**: `UNRESOLVED`.
- **confidence_as_discriminator**: `UNRESOLVED` — not extracted.

## D. Claims

- **central_conclusion**: Subsampled AF2 predicts not just which conformations a kinase core
  can adopt but how mutations shift the **relative populations** of those conformations, and the
  predictions track NMR.

- **THE QUOTES THIS NOTE EXISTS FOR** (verbatim, `[monteirodasilva2024subsampled, Results]`
  unless marked):
  1. > "we found that subsampled AF2 can qualitatively predict both the positive and negative
     > effects of mutations on the active state populations of kinase cores with up to eighty
     > percent accuracy."
  2. > "Our predictions strongly correlated with experimentally-determined NMR results, further
     > showcasing subsampled AF2's remarkable capacity to decode signals pertaining to
     > conformational changes even when sequence data is scarce."
  3. > "we focus on detecting changes in the active state population across the Src kinase to
     > Abl1 evolutionary line and test our ability to predict the effects of single and double
     > point mutations known or suspected to shift state distributions." *(Introduction)*
  4. > "methods like AF2 will need to account for the relative populations of different
     > conformations (states) since the conformational equilibrium of drug receptors is directly
     > related to their affinities for drugs" *(Introduction)*

- **stance**: **precedent + contrast.** Precedent because it is the corpus's only
  population-level subsampling result and the only one validated against NMR. Contrast because
  **it is a kinase paper and its populations are sequence-driven, not co-input-driven** — it
  does not touch partner or ligand conditioning.

## E. Quantitative comparators

| quantity | value | scope | locator |
|---|---|---|---|
| Mutation-effect sign accuracy | **up to 80%** | active-state population, kinase cores | Results |
| Validation | NMR, "strongly correlated" | `UNRESOLVED`: no r value extracted | Results |

- **comparable_to_ours**: **On the ensemble question specifically, and it is the one paper that
  makes it concrete.** This project has repeatedly had to separate a *deposited structure*
  (one conformer) from an *ensemble population* — for `vo2026fiducials` vs
  `georgiou2025heterogeneity`, and again for the C7 readouts. **This paper shows a predictor's
  sampled output being read as a population and validated against NMR**, which is the closest
  published warrant for treating our own per-cell prediction fractions as ensemble-like. It is
  a kinase result, so it transfers as method, not as biology.
- **si_in_scope**: not retrieved.

## F. Figures

**NOT EXTRACTED (panels not viewed).** Not usable for figure-design queries.

## G. Provenance

- **extracted_on, by**: 2026-09-14, lit-3d, from PMC10973385 full-text XML via NCBI efetch.
- **schema_version**: `v3.2`
- **confidence**: **high for the four quoted strings** (machine-verified 4/4 against the
  retrieved full text). **Low for sections B, C and E generally** — this is a deliberately
  partial pass taken to close a bibliography gap, and the fields that would need a full read
  are marked `UNRESOLVED` rather than guessed. **Do not treat this note as a complete
  extraction.**
- **unresolved**:
  1. **The subsampling depth grid** (`max_seq`/`max_extra_seq` values) — the reason a
     subsampling paper matters to us, and not extracted.
  2. **Panel size** — how many kinase cores, how many mutants.
  3. **The NMR correlation coefficient.**
  4. Whether MSA depth and mutation are genuinely crossed or staged.
  5. Anti-memorization design; confidence behaviour; all figures.
  6. **A full second pass is owed.** Recorded here so a future session does not mistake this
     for a finished note.
- **why_it_matters**: *(user's call — left empty per SCHEMA)*
