# bondar2017preassembly

> **Extraction provenance and locator caveat.** Extracted 2026-09-09 from the **PMC publisher
> HTML full text** (PMC5465492), read through the browser because the Europe PMC XML endpoint
> returns empty for this record and both the JBC and PMC PDF routes are bot-walled. **No PDF in
> `pdfs/`, so locators are SECTION names, not page numbers**; published pagination is
> J Biol Chem 292(23):9690–9698. Abstract, Introduction, Results, Discussion and Materials and
> Methods were retrieved complete. Figures were read from captions only. See `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `bondar2017preassembly` |
| `doi` | 10.1074/jbc.M116.768127 |
| `year`, `venue` | 2017 — **Journal of Biological Chemistry 292(23):9690–9698**, peer-reviewed, CC-BY. Published online 24 April 2017. PMID 28438833. |
| `title` | The G protein Gi1 exhibits basal coupling but not preassembly with G protein-coupled receptors |
| `authors` | Alexey Bondar, Josef Lazar (Czech Academy of Sciences / University of South Bohemia) |

> **Why this note exists.** The manuscript's introduction argues about whether a receptor and a
> transducer associate *before* activation. This is the corpus's only paper arguing they do not,
> and it draws a distinction the rest of the literature routinely collapses. Read it against
> `georgiou2025heterogeneity` (pre-coupled I1 intermediate) and `paajanen2026activation`
> (ligand-first). See `stance`.

## B. Scope

| field | value |
|---|---|
| `system` | **GPCR** — four receptors spanning class A and class C: α2A-adrenergic (α2A-AR), GABA<sub>B</sub>, cannabinoid type 1 (CB1R), dopamine D2 (D2R), each against the G protein **Gi1**. |
| `n_targets` | 4 receptors × 2 fluorescently labelled Gαi1 constructs, in HEK293 cells. "At least 10 cells were quantitatively analyzed for each experimental condition" (Methods); n ≥ 40 cells for the CB1R inactivation arms. |
| `method_class` | **experimental** — two-photon polarization microscopy (2PPM), a live-cell imaging method the same lab developed. Not structure prediction, not MD. |
| `backbones` | NOT APPLICABLE. |
| `templates`, `msa_handling` | NOT APPLICABLE. |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **NOT APPLICABLE — equilibrium interrogated, nothing generated.** The readout is linear dichroism (LD) of a single fluorescent label, reporting orientational bias of the fluorophore and therefore protein–protein association. |
| `structural_priors_used` | Minimal, and unusually so. No deposited structure is used at any point. The one design-time prior is the choice of the **N269D non-dissociating mutation**, taken from prior work as a positive control because it "impair[s] G protein dissociation from activated GPCRs". |
| `coinput_composition` | **New in v3.1. This paper is the corpus's cleanest example of varying one thing at a time.** Arms: (i) Gαi1-FP + Gβ1 + Gγ2, no receptor; (ii) + each of four receptors, unstimulated; (iii) + each receptor, agonist-stimulated; (iv) CB1R + inverse agonist (rimonabant, 10 μM); (v) CB1R(T210A) constitutively inactive mutant. The receptor's *activation state* is the only variable between (ii), (iv) and (v). **Not `coinput-confounded`.** |
| `binding_order` | **New in v3.1. ADDRESSED HEAD-ON — this is the paper's entire subject.** It sets out the two competing models explicitly (Introduction): collision coupling, in which "non-activated GPCRs and G proteins were thought to not interact and to freely diffuse in the cell membrane"; against pre-coupling/pre-assembly, "formation of stable complexes between inactive GPCRs and G proteins", postulated because "the rates of G protein activation are characterized by rate constants of 30–50 ms ... which suggests that GPCRs and G proteins might, in fact, interact already prior to GPCR activation". Tags `pre-coupled` (as the hypothesis tested and rejected for Gi1). |
| `oracle_leakage` | **Routes 1–7 NOT APPLICABLE** — no prediction, no structure supplied, no held reference, no scored success against a deposited answer. Route 4 analogue: none found; the LD reference dataset is the FP-tagged heterotrimer expressed without receptor, fixed in advance. |
| `prospective` | **yes.** The hypothesis is stated first and the experiment can refute it, which it partly does. Nothing is scored against a known answer. |
| `state_metric` | **continuous coordinate.** Linear dichroism expressed as the maximum dichroic ratio r<sub>max</sub> and as log<sub>2</sub>(r<sub>max</sub>/r<sub>max</sub><sup>0</sup>) against a reference dataset. Significance by Student's t test, or one-way ANOVA with Bonferroni post-test for >2 groups, normality confirmed by D'Agostino-Pearson. **No threshold defines "associated"**; the call is a statistically significant difference from the no-receptor reference. |
| `metric_saturation` | **NOT REPORTED.** LD is bounded in principle but no pile-up at a bound is described. |
| `directional_control` | **NOT APPLICABLE as a generative handle.** The manipulated variable is the receptor's activation state, controlled pharmacologically (agonist, inverse agonist) and genetically (T210A). |
| `anti_memorization_design` / `_control` | **NOT APPLICABLE** — no learned model. |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT APPLICABLE.** |

### `controls_run`

**The control design is the paper**, and it is the reason its negative result is worth more than the positive results it argues against.

| control | what it rules out | locator |
|---|---|---|
| **N269D non-dissociating Gαi1 mutants** as a positive control | that 2PPM cannot detect a GPCR–G protein interaction at all. It can: LD shifts by ~0.5–0.6 in log<sub>2</sub> units with activated receptors | Results, Fig 2 |
| **Untagged receptors** (α2A-AR, D2R) and a receptor tagged only extracellularly (GABA<sub>B</sub>-Snifit) | that the interaction is an artefact of fluorescent-protein labels touching each other | Results |
| **Inverse agonist (rimonabant, 10 μM) on CB1R** | that the CB1R signal is pre-assembly rather than basal activity | Results, Fig 5 |
| **CB1R(T210A) constitutively inactive mutant**, membrane localisation verified | same, genetically rather than pharmacologically | Results, Fig 5 |
| **GIRK current recordings** confirming CB1R basal activity is real | that "basal activity" is asserted rather than measured | Results, Fig 5A |
| **Gβ1/Gγ2 co-expression check** | that the labelled Gα still forms a heterotrimer | Results, Fig 1 |
| **Four receptors, two independent Gαi1 construct designs** | that the result is one construct's or one receptor's quirk | throughout |
| **Quantitative extrapolation to endogenous expression** | that overexpression hides a real but small pre-assembled pool | Discussion + Methods appendix |

## D. Claims

- **`central_conclusion`**: Two-photon polarization microscopy, which needs only a single
  fluorescent label and therefore avoids the control problems of FRET and BRET, detects no
  pre-assembly between Gi1 and four unstimulated receptors. The one apparent interaction, at CB1R,
  is abolished by an inverse agonist or an inactivating mutation and is therefore **basal
  coupling** to a spontaneously active receptor, not pre-assembly to an inactive one. The authors
  conclude that the known speed of GPCR signalling does not require pre-assembly.

- **`necessity_claims`** (verbatim + section):
  - Abstract: "Our results demonstrate that four diverse GPCRs do not preassemble with non-active
    Gi1."
  - Abstract: "These findings suggest that Gi1 interacts only with active GPCRs and that the well
    known high speed of GPCR signal transduction does not require preassembly between G proteins
    and GPCRs."
  - Introduction, on the state of the field: "to date, experimental studies of GPCR-G protein
    coupling have yielded conflicting results, failing to provide consistent evidence supporting
    either preassembly or collision coupling", and "the issue of G protein-GPCR precoupling
    remains to be conclusively settled".
  - Introduction, **the distinction the rest of the literature collapses**: "This interaction,
    termed 'basal coupling' here, is similar to the interaction between the activated GPCRs and G
    proteins because it is dependent on the GPCR adopting an activated conformation. In contrast,
    GPCR-G protein preassembly is not caused by the basal activity of the receptor and does not
    lead to immediate G protein activation. Preassembly, unlike basal coupling, increases the rate
    of signal transfer between stimulated GPCRs and G proteins".
  - Discussion, the methodological charge against the positive literature: "A well known
    difficulty of these techniques is establishing proper positive and negative controls. In fact,
    BRET between many non-interacting proteins has been shown to occur as long as they are
    co-localized to the same cellular compartment."
  - Discussion: "our results indicate that high specificity and rate of signaling can be achieved
    without pre-existing physical interaction between a GPCR and a G protein."
  - Discussion, the alternative explanation: "the well known high rate of G protein activation
    (often cited as evidence for GPCR-G protein preassembly) is likely the result of high G protein
    concentration in the cell membrane."

- **`novelty_claims`** (verbatim + section):
  - Introduction: "It should be possible to address the issue of GPCR-G protein preassembly in a
    new, more conclusive fashion, by using the technique of two-photon polarization microscopy
    (2PPM), recently developed by our lab."
  - Introduction: "because of its reliance on only a single fluorescent label, 2PPM allows
    observations of membrane protein processes at conditions closer to natural than those allowed
    by resonant energy transfer imaging techniques that rely on two optically active moieties.
    Furthermore, 2PPM provides information on physical interaction between molecules, not just
    spatial proximity between molecules."
  - Discussion: "our results provide strong evidence against GPCR-G protein preassembly between
    Gi1 and the four studied GPCRs."

- **`stated_limits`** (verbatim + section): unusually candid, and they bound their own negative.
  - Discussion: "Although it is conceivable that preassembly occurs without detectably affecting
    the orientation of the Gαi1-FP fluorescent label and therefore cannot be detected by 2PPM, we
    find this possibility physically unlikely."
  - Discussion, **the quantitative bound**: "we estimate that our experiments with overexpressed
    proteins can reveal preassembly if more than 15% of Gαi1-FP molecules is associated with a
    GPCR. However, endogenous concentrations of GPCRs and G proteins are considerably lower than
    concentrations of the overexpressed proteins used in our experiments. Thus, we extrapolate
    that in GPCRs expressed at endogenous levels, the fraction of preassembled GPCR-G protein
    complexes, if present, consists of less than ~3% of the GPCR molecules." (derivation given
    algebraically in Methods)
  - Discussion, **scope limit that matters for reading Qin 2011**: "Although we did not find
    preassembly in the four GPCRs used in our study of the Gi1 protein, we cannot exclude the
    possibility that preassembly does occur in other GPCRs coupled to Gi/o or other families of G
    proteins. Preassembly might depend on the presence of specific motifs in GPCRs, such as the
    polybasic motif deemed to be needed for preassembly of GPCRs that couple to the Gq protein
    (not investigated in this study)."
  - Discussion: "the mode of Gi/o protein-GPCR interaction is distinct for different GPCRs."

- **`stance`**: **`contrast` + `background`** — provisional, the user's call.
  - *Contrast*: it is the corpus's only source arguing against inactive-state pre-assembly, and
    it supplies the pre-assembly / basal-coupling distinction that every other treatment in the
    corpus, including `georgiou2025heterogeneity`, leaves implicit. Any manuscript sentence
    treating a pre-coupled receptor–G protein complex as an *inactive* receptor with a transducer
    bound has to survive this paper.
  - *Background*: it bounds what a co-folding experiment can be said to model. If what is called
    pre-coupling is largely basal coupling, then a transducer supplied to a receptor with no
    agonist is not obviously the computational counterpart of a physiological pre-coupled state,
    and should be described as a controlled input condition instead.

## E. Quantitative comparators

| metric | value | units | measured against | locator |
|---|---|---|---|---|
| LD shift, GAP43-CFP-Gαi1(N269D) with activated receptors | ~ +0.5 | log<sub>2</sub>(r<sub>max</sub>/r<sub>max</sub><sup>0</sup>) | no-receptor reference | Results, Fig 2 |
| LD shift, Gαi1(N269D)-L91-YFP with activated receptors | ~ +0.6 | same | same | Results, Fig 2 |
| Detection limit for pre-assembly, overexpressed | > 15 | % of Gαi1-FP molecules associated | — | Discussion |
| Upper bound on pre-assembly at endogenous expression | < ~3 | % of GPCR molecules | extrapolated, K<sub>d</sub> derivation in Methods | Discussion |
| Cited G protein activation rate constants | 30–50 | ms | prior literature, as the motivation for pre-coupling | Introduction |
| Cells analysed per condition | ≥ 10 (≥ 40 for CB1R inactivation arms) | count | — | Methods, Discussion |

- **`n_predictions`**: NOT APPLICABLE.
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **No supplementary material is referenced.** The K<sub>d</sub> extrapolation
  is given in full in the Methods. Everything the argument rests on is in the main text.

## F. Figures

Five figures, read from captions; **panels not viewed**. All are LD bar/scatter summaries plus
2PPM images; none is a structure render.

| fig_no | locator | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A-B | Results | Gαi1-FP ± Gβ1/Gγ2, heterotrimer formation check | point with s.d. | `PLOT \| facet: construct (2) \| vary: condition (2: alone, +Gβγ) \| series: none (1) \| measure: log2(rmax/rmax0) \| n: ≥10 cells per point` | 2 | — | CC-BY |
| 2A-B | Results | 2PPM LD images, Gαi1(N269D) with five activated receptor conditions | image | `RENDER \| facet: receptor condition (5) \| views: 1 \| overlay: none \| axis: none` | 2 rows | Representative cells only; the quantification is in 2C-D | CC-BY |
| 2C-D | Results | LD for Gαi1(N269D) with activated receptors | point with s.d. | `PLOT \| facet: construct (2) \| vary: receptor (6 incl. no-GPCR reference) \| series: none (1) \| measure: log2(rmax/rmax0) \| n: ≥10 cells per point` | 2 | — | CC-BY |
| 3A-B | Results | Same, **non-stimulated** receptors | point with s.d. | as 2C-D | 2 | — | CC-BY |
| 4A-B | Results | Non-mutated Gαi1-FP with inactive receptors — the central negative | point with s.d. | as 2C-D | 2 | **This is a null for three of four receptors and is drawn as the same point-and-error-bar plot as the positive panels, which is the right choice — the reader compares like with like** | CC-BY |
| 5A-D | Results | CB1R basal activity by GIRK current; T210A localisation; LD under inverse agonist and inactivating mutation | line + image + point | `PLOT \| facet: none (1) \| vary: CB1R condition (4: untreated, +rimonabant, T210A, no-CB1R reference) \| series: none (1) \| measure: log2(rmax/rmax0) \| n: ≥40 cells` | 4 | — | CC-BY |

**Figure 4 is worth looking at for our own null panels.** It presents a negative result in the
identical visual grammar as the positive panels that precede it, so "no difference" reads as a
measurement rather than as a missing experiment.

## G. Provenance

- **`extracted_on`**: 2026-09-09
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3.1`
- **`confidence`**: **medium-high.** Identity, scope, the control design, the pre-assembly /
  basal-coupling distinction, the quantitative bounds and every quoted claim were read directly
  from the complete publisher HTML. **Low on figure internals** — captions only, no panel viewed
  — and no page numbers exist for this note.
- **`unresolved`**:
  1. **No PDF and no page numbers.** Section locators only. Convert before submission.
  2. Figure panels not viewed; per-panel n taken from the Methods statement rather than captions.
  3. The paper is 2017 and the debate has moved; `qin2011preassembly` (Gq, argues FOR) and
     `nobles2005precoupling` (argues FOR) are cited here but are **not yet extracted** in this
     corpus, so this note currently presents one side of a contested question with the other side
     bibliography-only.
  4. Whether any later work overturns the ~3% endogenous bound was not checked.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
gpcr experimental pre-coupled prospective peer-reviewed contrast background negative-result
comparator-numbers
```

**Tag notes.** `experimental` applies in the SCHEMA sense: no structure prediction anywhere.
`pre-coupled` marks the mechanism at issue, not the paper's conclusion — the reverse lookup should
return both sides of the argument, and the `binding_order` field carries the verdict.
`negative-result` applies and is the point of the paper. `no-anti-memorization` **deliberately not
applied**: there is no model that could memorise anything, and applying it would corrupt that
reverse lookup. `coinput-confounded` **deliberately not applied** — the opposite is true here.
