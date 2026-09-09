# aureli2026epath

> **Extraction provenance and locator caveat.** Extracted 2026-09-09 from the **Europe PMC
> full-text XML** (PMC12990105), the publisher PDF being bot-walled. **No PDF in `pdfs/`, so
> locators are SECTION names, not page numbers.** Published pagination is J Phys Chem Lett
> 17(10):2974–2983. Main text retrieved complete; the Supporting Information (Figures S1–S8) was
> not. See `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `aureli2026epath` |
| `doi` | 10.1021/acs.jpclett.5c03834 |
| `year`, `venue` | 2026 — **The Journal of Physical Chemistry Letters 17(10):2974–2983**, peer-reviewed, **CC-BY 4.0**. Received 5 Dec 2025, revised 20 Feb 2026, accepted 24 Feb 2026, collection date 12 Mar 2026. |
| `title` | A Transferable and Robust Computational Framework for Class A GPCR Activation Free Energies |
| `authors` | Simone Aureli, Nicola Piasentin, Thorben Fröhlking, Valerio Rizzi, Francesco Luigi Gervasio (University of Geneva; Gervasio also UCL) |

## B. Scope

| field | value |
|---|---|
| `system` | **GPCR, class A**, and this is the corpus's only free-energy treatment of receptor activation. Both receptors are studied **apo**. |
| `n_targets` | **2 receptors**: the β1-adrenergic receptor (ADRB1) and the μ-opioid receptor (MOR), both apo. ADRB1 is the reproduction target against the authors' earlier tailored approach; MOR is the new application. |
| `method_class` | **enhanced sampling / MD.** Multiple-replica enhanced sampling (OneOPES, with OPES Expanded on the potential energy in exploratory replicas) driven by a path collective variable. The contribution is a streamlined CV definition, "EPATH", a Euclidean variant of the PATH CV that removes the need to hand-build intermediate milestones. |
| `backbones` | **NOT APPLICABLE — no structure predictor is run.** GROMACS 2023 with PLUMED ≥ 2.8. |
| `templates` | NOT APPLICABLE. |
| `msa_handling` | NOT APPLICABLE. |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **continuum + two-state.** A continuous free-energy landscape along an activation path CV, from which inactive and active basins and the intermediates between them are read off. Nothing is "predicted" in the co-folding sense; an equilibrium is sampled. |
| `structural_priors_used` | **Substantial and by design.** The path CV is anchored on deposited inactive and active reference structures of each receptor, and parabolic restraints are placed on the PIF and NPxxY microswitches "to guide the system through the intermediate basins, which contain many metastable states and kinetic traps, to the fully active one" (Results). Legitimate for a free-energy calculation, and recorded here rather than as leakage. |
| `oracle_leakage` | **Routes 1–7 are largely NOT APPLICABLE**, because there is no prediction pipeline and no held-out answer. Recorded route by route.<br>**Route 1:** deposited endpoint structures define the path CV. Design-time, unavoidable for a path method, recorded under `structural_priors_used`.<br>**Route 2:** NONE FOUND — no curated state database drives anything.<br>**Route 3:** NONE FOUND.<br>**Route 4 — PRESENT in kind.** CV construction, restraint choice and replica schedule are refined against the resulting landscapes; the paper's own framing of the problem it solves is that the previous approach "would require a tedious and error-prone choice and refinement of the collective variables" (Abstract).<br>**Route 5:** NOT APPLICABLE — success is free-energy convergence between independent replicas, not RMSD to a held structure.<br>**Route 6:** NONE FOUND — no best-of-N selection.<br>**Route 7 — PRESENT, design-level.** Both receptors were chosen because their activation is already characterised, ADRB1 explicitly as a reproduction target. |
| `prospective` | **partial.** ADRB1 is a deliberate reproduction of a known answer. MOR is genuinely new ground: "for the μ-opioid receptor activation, we gain novel biological insights" (Abstract). |
| `state_metric` | **continuous coordinate**, and it is the most carefully constructed one in the corpus. Progress along a path CV, with the path deviation z restrained loosely, plus explicit structural descriptors for four microswitch motifs: "PIF, DRY, NPxxY, and YY, to capture local structural determinants of activation" (Methods). Two-dimensional free-energy surfaces are computed "as a function of the activation pathway and structural descriptors associated with the NPxxY, DRY, and YY motifs" (Results). **No binary predicate and no threshold anywhere**, which is the methodological contrast with every prediction paper in this corpus. |
| `metric_saturation` | **Not applicable in the usual sense**; free energies are unbounded. The reported convergence behaviour is the analogous concern: the RPATH CV "takes a rather long time to converge, with the free energy difference reaching an agreement between the independent replicas only at the end of the simulation" (Results). |
| `directional_control` | **Yes, and it is a bias potential rather than a biological co-input.** The handle is the path CV plus parabolic restraints on PIF and NPxxY. Both receptors are apo; **no ligand, no agonist, no G protein and no peptide is present in any simulation**, which is exactly why this paper is useful to us: it characterises what the apo receptor's landscape looks like with nothing bound. |
| `anti_memorization_design` | **NOT APPLICABLE** — no learned model, nothing to memorise. |
| `anti_memorization_control` | **NOT APPLICABLE.** |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT APPLICABLE** — no pLDDT analogue. Convergence between independent replicas plays the role of an internal quality check. |

### `controls_run`

| control | what it rules out | locator |
|---|---|---|
| ADRB1 reproduction against the authors' earlier tailored-CV approach | that the streamlined CV changes the answer | Abstract, Results |
| apo-MOR-OLD vs apo-MOR-Euclidean, matched | that the new CV formulation is not equivalent | Results, Figs 2–3 |
| Independent-replica convergence of ΔG | that the landscape is an artefact of one trajectory | Results |
| Microswitch rearrangement analysis along the activation coordinate | that the path CV moves the system without real activation | Results, Figs S5, S8 |
| Cavity hydration analysis | — | Fig S5 |

## D. Claims

- **`central_conclusion`**: Class A GPCR activation free energies can be computed with a path
  collective variable that is defined without hand-picking intermediate structures, using a
  Euclidean reformulation ("EPATH") inside a multiple-replica OPES scheme. Applied to apo ADRB1 it
  reproduces the landscape obtained with a bespoke, laboriously tuned CV; applied to apo MOR it
  yields a new landscape. The method is presented as transferable across class A receptors.

- **`necessity_claims`** (verbatim + section locator):
  - Abstract: "However, capturing it with molecular simulations is far from trivial, as it requires
    capturing both local and global motions."
  - Abstract: "While that approach can be applied to other receptors, it would require a tedious
    and error-prone choice and refinement of the collective variables and, in particular, of the
    main path-like variable."
  - Introduction: "Their function is tightly linked to conformational changes that span multiple
    scales, from local rearrangements of side chains and hydration sites to large-scale
    reorganizations of the transmembrane helices that define the transition between inactive and
    active states."
  - Introduction: "receptors' transitions occur on time scales that remain difficult to access
    with unbiased MD simulations, a limitation that is commonly addressed by enhanced sampling
    strategies."
  - Results, on why milestones are needed at all: "Both approaches use a similar set of parabolic
    restraints on the microswitches PIF and NPxxY to guide the system through the intermediate
    basins, which contain many metastable states and kinetic traps, to the fully active one."
  - Discussion of prior art: "a contact-map-based path CV remains difficult to build and cannot be
    transferred between systems."
  - On the prior method's transferability: "This limitation reduces the accessibility and
    transferability of the method, making it challenging to apply it across multiple receptors or
    conformational transitions systematically."

- **`novelty_claims`** (verbatim + section locator):
  - Abstract: "Herein, we introduce an effective and streamlined evolved strategy for defining CVs
    that reduces user intervention while still achieving a robust free energy convergence."
  - Abstract: "for the μ-opioid receptor activation, we gain novel biological insights."
  - Abstract: "The proposed method can be easily applied to other class A GPCRs, paving the way for
    the systematic elucidation of the activation mechanisms of many crucial drug targets."
  - Results: "Importantly, EPATH does not require a tedious definition of all of the intermediate
    milestones."
  - Results: "This yields a path that is straightforward to define as it does not depend on any
    intermediate structure."

- **`stated_limits`** (verbatim + section locator):
  - Results: "A further limitation of RPATH CV is the requirement to focus the RMSD calculation on
    specific portions of the GPCR."
  - Results, on convergence: the RPATH CV "takes a rather long time to converge, with the free
    energy difference reaching an agreement between the independent replicas only at the end of
    the simulation".
  - Scope: two receptors, both apo, both class A. Transferability beyond that is asserted, not
    demonstrated.

- **`stance`**: `background` + `precedent` — provisional, the user's call.
  - *Background*: the corpus's reference description of what the class A activation coordinate
    actually is, in free-energy terms, with the microswitch motifs (PIF, DRY, NPxxY, YY) used as
    quantitative descriptors rather than as a visual call. Useful for justifying our own state
    predicate and for the intermediate-conformation discussion.
  - *Precedent*: an apo-receptor landscape computed with nothing bound, which is the physical
    counterpart of our apo arm.

## E. Quantitative comparators

| metric | value | units | measured against | locator |
|---|---|---|---|---|
| apo-MOR-Euclidean ΔG (activation free-energy difference) | ~18 (value as printed; units and sign to be confirmed against the figure) | kcal/mol | independent-replica convergence | Results |
| Convergence time, one arm | ~800 ns | simulation time | ΔG plateau | Results |
| Replica scheme | 1 unbiased (replica 0) + 7 exploratory (replicas 1–7) | count | — | Methods |
| Microswitch CVs | 4 motifs: PIF, DRY, NPxxY, YY | count | — | Methods |

**Read the ΔG value with care.** The text-layer rendering splits the number across a sentence
boundary ("0 kcal/mol after ∼800 ns, whereas apo-MOR-Euclidean's OneOPES simulations converge to
the ΔG value of ∼18."), so the paired ADRB1 value and the exact MOR figure need the PDF before
either is quoted in the manuscript. Flagged in `unresolved`.

- **`n_predictions`**: NOT APPLICABLE. Simulation, not prediction. Replica counts above.
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **SI NOT HELD.** Figures S1–S8 include the microswitch rearrangement analyses
  (S5, S8) that support the headline agreement claim. Code at PLUMED-NEST
  `plumed-nest.org/eggs/26/002/`.

## F. Figures

Figure numbering was recoverable from the XML but captions are truncated in the text layer, and
**panels were not viewed**. Recorded conservatively rather than guessed.

| fig_no | locator | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | Results | Schematic comparison of the original PATH CV and the Euclidean variant | schematic | `SCHEMATIC \| PATH vs EPATH CV construction \| no data` | — | — | **CC-BY 4.0, no ND — redrawing permitted with attribution** |
| 2–4 | Results | Free-energy surfaces and ΔG convergence for apo-ADRB1 and apo-MOR, old vs Euclidean CV, with mean and s.d. bands across replicas | free-energy surface + line | `PLOT \| facet: receptor and CV variant \| vary: path progress CV (continuous) \| series: method (2: OLD, Euclidean) \| measure: free energy (kcal/mol) \| n: 8 replicas` | NOT EXTRACTED | — | as above |
| S5, S8 | SI (not held) | Microswitch rearrangements and cavity hydration along the activation coordinate | NOT EXTRACTED | NOT EXTRACTED | — | — | as above |

## G. Provenance

- **`extracted_on`**: 2026-09-09
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **medium.** High on identity, scope, method class, the CV design and every
  quoted claim, all read from the full XML. Low on the numeric free energies, on figure structure
  and on everything in the SI.
- **`unresolved`**:
  1. **No PDF, therefore no page numbers.** Section locators only.
  2. **The ΔG values.** The text layer breaks the sentence carrying them; both the ADRB1 and MOR
     numbers need the PDF before use.
  3. Figure captions are truncated in the XML; panel structure not established.
  4. Whether the reported ΔG is inactive-to-active and with what sign convention.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
gpcr md enhanced-sampling continuum two-state continuous-metric directed-state apo-sampling
design-level-oracle peer-reviewed background precedent comparator-numbers
```

**Tag notes.** `experimental` **deliberately not applied**: this is simulation, not wet lab, and
that tag is reserved in this corpus for papers with no structure prediction *and* no simulation
model of their own. `binary-predicate` and `visual-metric` **deliberately not applied** — there is
no threshold and no call by eye anywhere, which is the point of the paper. `anti-memorization` and
`no-anti-memorization` both **deliberately not applied**: neither is meaningful without a learned
model, and applying either would corrupt the memorization reverse lookup.
