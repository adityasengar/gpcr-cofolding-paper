# bret2025boltz2docking

> **Extraction provenance and a pagination caveat.** Extracted 2026-09-09 from the **HAL author
> version** supplied by the user ("To cite this version: ... Journal of Chemical Information and
> Modeling, 2026"), not the published ACS typesetting. **Locators are PDF pages of that author
> version and do NOT correspond to the published pagination**, which is JCIM 66(3):1511–1521.
> Convert them before any manuscript citation. Main text read; Supporting Information (Figures
> S1–S6 and the target tables) not retrieved. See `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `bret2025boltz2docking` |
| `doi` | 10.1021/acs.jcim.5c02630 |
| `year`, `venue` | **2026** — J. Chem. Inf. Model. 66(3):1511–1521, peer-reviewed. Received 28 Oct 2025, revised 5 Jan 2026, accepted 13 Jan 2026, published 27 Jan 2026. **The citekey says 2025 and the paper is 2026**; the key is a label and is left unchanged so the `diffusion_steering` superset property does not break. |
| `title` | Assessing Boltz-2 Performance for the Binding Classification of Docking Hits |
| `authors` | Guillaume Bret, François Sindt, Didier Rognan (Université de Strasbourg) |

## B. Scope

| field | value |
|---|---|
| `system` | **GPCR-heavy, plus a kinase and a transporter.** UniProt targets named in the text: CASR (P41180), CNR1 (P21554), CNR2 (P34972), DRD3 (P35462), DRD4 (P21917), MTR1A (P48039), ROCK1 (Q13464), SC6A4 (P31645), SGMR2 (Q5BJF2), plus ADRA2B in the mutation arm. Eight of the ten are GPCRs. |
| `n_targets` | **10 targets, 943 docking-based ultra-large-virtual-screening hits**, "all being annotated with experimental in vitro data" (author version, ~p2). |
| `method_class` | **benchmark-only, adversarial.** Boltz-2's affinity classifier and regressor are challenged with target mutation and target shuffling. |
| `backbones` | **Boltz-2** only, both the structure and the affinity heads. Compared against conventional docking scoring functions. |
| `templates` | NOT REPORTED. |
| `msa_handling` | NOT REPORTED. |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **NOT APPLICABLE for receptor conformational state.** The output of interest is an affinity or a binary active/inactive call, not a conformation. Poses are generated but the receptor's state is never assessed. |
| `structural_priors_used` | Target sequences from UniProt; the hit lists come from published ultra-large screens with experimental annotation. No deposited complex is supplied as input. |
| `oracle_leakage` | **Route 5 PRESENT** in the sense that classification success is scored against experimental activity labels the authors hold. **Route 7 PRESENT, design-level** — the ten target sets were chosen because their activity annotations exist. **Routes 1, 2, 3, 4, 6: NONE FOUND / NOT REPORTED**; no structure is supplied as input and no per-target tuning is described. The paper's whole design is to *remove* the possibility that the model is reading a memorised answer, so it is unusually clean on the input side. |
| `prospective` | **no.** Retrospective against published screens with known outcomes. |
| `state_metric` | **NOT APPLICABLE for conformational state.** The metric is **ROC AUC** for classifying true actives against true inactives, and a ΔROC AUC (wild type minus mutant) for the adversarial arms. |
| `metric_saturation` | **NOT EXTRACTED.** |
| `directional_control` | **NOT APPLICABLE** — nothing is steered. |
| `anti_memorization_design` | **PRESENT, and of an unusual kind: adversarial rather than temporal.** Rather than a date cutoff, the design perturbs the target itself. Binding-site residues are mutated to alanine, including "residue D92 in ADRA2B, D110 in DRD3, D115 in DRD4 ... mutated to alanine, a mutation known to suppress ligand binding to these receptors", and the ROCK1 hinge Met153 mutated to proline. A mutation-rate series is then run: "we generated a series of mutations (wild-type to alanine) for each protein, specifically targeting either the binding site or the outer shell of each target, with an increasing mutation rate". Separately, targets are **exchanged** between hit lists. |
| `anti_memorization_control` | **RUN AND ANALYSED, across all ten target sets.** ROC AUC is reported for wild type and mutant, and ΔROC AUC against increasing mutation count at randomly chosen positions. This is a stronger control than a date split, because it tests whether the model responds to the physics at all. |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT APPLICABLE** in the pLDDT sense, but the paper's central negative is the analogous one: an internal score that is supposed to reflect binding does not respond when binding is destroyed. |

### `controls_run`

| control | what it rules out | locator |
|---|---|---|
| Binding-site alanine mutation at known binding-suppressing residues | that the classifier reads the actual binding site | Results |
| Increasing-mutation-rate series, binding site vs outer shell | that the insensitivity is a threshold effect | Results |
| **Target shuffling / exchange between hit lists** | that the classifier is target-specific at all | Abstract, Results |
| Synthetic decoys "created by shuffling binders identified in hit-to-lead screens across different targets" | that the actives are trivially separable | Results |
| Chemical-similarity check against known potent compounds | that predictions are similarity lookups | Abstract |
| Pose-quality vs affinity-accuracy comparison | that good affinity requires a good pose | Abstract |
| Comparison against conventional docking scoring functions | that the gain is not real | Abstract |

## D. Claims

- **`central_conclusion`**: Boltz-2 separates true from false positives among ultra-large-screening
  docking hits far better than any conventional scoring function on raw poses, and its affinity
  predictions are largely independent of pose quality and are not explained by chemical similarity
  to known actives. But the same binary classification is insensitive to binding-site mutations
  known to abolish binding, and in some cases to exchanging the target entirely, so what the
  affinity head is reading is not the physics of the interaction.

- **`necessity_claims`** (verbatim + locator):
  - Abstract: "To ascertain that Boltz-2 truly relies on the physics of intermolecular
    interactions, we challenged affinity predictions with biologically meaningful challenges
    (target mutation and target shuffling)."
  - Abstract, the load-bearing negative: "Binary classification of active vs inactive compounds
    remains insensitive to key binding site mutations and even in some cases to target exchange,
    raising concerns on the hidden features governing Boltz-2 affinity predictions."
  - Results, on the prior AF3 result they build on: "Hence, AF3 binding poses remained largely
    unaffected by drastic binding site mutations, contradicting elementary physical principles and
    suggesting that AF3 has not yet fully learned the major laws of protein−ligand recognition."
  - Results, closing the logical escape route: "If the poses to wild type and mutants had been very
    similar, we could have understood that the relative ranking remains unchanged for a target,
    with the same interactions to the mutated amino acids being systematically ignored for every
    compound. However, since this is not the case, obtaining comparable prediction accuracy on wild
    type and mutated targets from different binding poses remains hard to understand from the
    physics of intermolecular interactions."
  - Introduction: co-folding models "still suffer from the lack of reliable training data to
    predict truly novel protein−ligand structures, to account for significant ligand-induced
    conformational changes, or to pose allosteric modulators in the right pocket." *(Superscript
    reference numerals 18, 15 and 16 sit inline after "structures", "changes" and "modulators" in
    the PDF text layer and are omitted here; the artifact is recorded so a mechanical quote check
    does not flag it as fabricated.)*
  - Introduction: "Whereas most benchmarks have been focusing on the accuracy of cofolded
    structures, Boltz-2 binding affinity predictions still need to be properly challenged."

- **`novelty_claims`** (verbatim + locator):
  - Abstract: "The recently released Boltz-2 cofolding model is generating high expectations by
    enabling both protein−ligand structure and binding affinity predictions."
  - Abstract: "When applied to a recently described and challenging data set of
    ultralarge-virtual-screening hits, Boltz-2 excels at discriminating true from false positives,
    overcoming by a large margin all scoring functions tested so far on raw docking poses."
    *(The PDF text layer renders this as "ultralarge-virtualscreening" because the hyphen falls on
    a line break; the hyphen is restored here.)*
  - Introduction: Boltz-2 is described as "the first AI framework able to simultaneously predict
    both the structure and binding affinity of" protein–ligand complexes *(attributed to the
    Boltz-2 authors, not claimed by these authors)*.

- **`stated_limits`**: **NOT FULLY EXTRACTED.** The dataset's difficulty is disclosed in the
  Results ("The data set is quite challenging for two main reasons..."), and the whole paper is a
  limitation report on someone else's model. A dedicated limitations passage on their own analysis
  was not located. Flagged in `unresolved`.

- **`stance`**: **`threat` + `precedent`** — provisional, the user's call.
  - *Threat, and a specific one.* Our decomposition rests on a **sequence-shuffled** arm: scramble
    the α5-CT sequence, keep the occupancy, and see the effect fall. This paper shows that on
    Boltz-2, one of our four backbones, a closely analogous manipulation — exchanging the target
    entirely — sometimes fails to change the model's output. Different quantity (affinity, not
    conformation) and different direction of shuffling, so it is not a refutation. But a referee
    who knows it will ask why our shuffled arm should be believed to be doing what we say, and the
    answer has to be that we measure the receptor's geometry rather than an internal score.
  - *Precedent.* It is the adversarial-control design our own decoy and shuffled arms belong to,
    it is GPCR-heavy, and it sits directly alongside `masters2025physics` (AF3 poses unaffected by
    pocket-destroying mutations) which it cites and extends to the affinity head.

## E. Quantitative comparators

| metric | value | units | measured against | locator |
|---|---|---|---|---|
| Hit set | 943 ultra-large-virtual-screening hits across 10 targets | count | experimental in vitro binding/activity | Results |
| GPCR targets among the ten | 8 (CASR, CNR1, CNR2, DRD3, DRD4, MTR1A, SC6A4*, SGMR2*, + ADRA2B in the mutation arm) | count | UniProt | Results |
| Primary metric | ROC AUC, and ΔROC AUC = ROC AUC(wt) − ROC AUC(mutant) | — | true actives vs true inactives | Results, figure captions |
| Decoy construction | one synthetic decoy per active, by shuffling binders across targets | ratio | — | Results |

\* SC6A4 is the serotonin transporter and SGMR2 the sigma-2 receptor; neither is a class A GPCR in
the strict sense. The "eight of ten" figure above should be checked against the paper's own target
table before it is quoted. Flagged in `unresolved`.

**No ROC AUC values were extracted.** They are in figures and in the SI.

- **`n_predictions`**: **NOT EXTRACTED.**
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **SI NOT HELD.** Figures S1–S6, including the ROCK1 mutation figure (S6) and
  the per-target tables.

## F. Figures

**NOT ENUMERATED.** Two figure captions were recovered from the body text and are recorded because
they define the metrics; no panel was viewed.

| fig_no | locator | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| (unnumbered in retrieved text) | Results | ROC AUC for classifying true actives vs true inactives, wild type against mutant, across ten target sets | NOT EXTRACTED | `PLOT \| facet: none \| vary: target set (10) \| series: sequence (2: WT, mutant) \| measure: ROC AUC \| n: 943 hits total` | — | — | ACS/HAL author version; check the published licence before adapting |
| (unnumbered) | Results | ΔROC AUC against increasing number of mutations at randomly chosen positions | NOT EXTRACTED | `PLOT \| facet: mutation region (2: binding site, outer shell) \| vary: mutation rate (continuous) \| series: target (10) \| measure: ΔROC AUC \| n: NOT REPORTED` | — | — | as above |
| S6 | SI (not held) | ROCK1 Met153→Pro hinge mutation | NOT EXTRACTED | NOT EXTRACTED | — | — | as above |

## G. Provenance

- **`extracted_on`**: 2026-09-09
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **medium.** High on identity, scope, the adversarial design and every quoted
  claim. Low on all numbers, on figures, and on the exact target composition. **Read from the HAL
  author version, so wording and pagination may differ from the published article.**
- **`unresolved`**:
  1. **Pagination is the author version's, not the journal's.** Convert before citing.
  2. **No ROC AUC values extracted**; the size of the effect is unknown from this note.
  3. Exact composition of the ten target sets, and how many are strictly class A GPCRs.
  4. Which targets showed insensitivity to *target exchange*, as opposed to mutation. The abstract
     says "in some cases" and this note cannot say which.
  5. `stated_limits` needs a second pass.
  6. Whether the author version differs materially from the published text.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
gpcr kinase transporter cofolding benchmark-only single-state binary-predicate continuous-metric
design-level-oracle anti-memorization ligand-driven orthosteric peer-reviewed threat precedent
negative-result comparator-numbers
```

**Tag notes.** `anti-memorization` applied for the adversarial mutation and target-exchange arms,
which serve the same purpose as a temporal split and arguably better. `confidence-as-discriminator`
**deliberately not applied**: the score interrogated is an affinity head, not a structural
confidence metric, and conflating them would pollute that reverse lookup. `gpcr` applied because
most targets are receptors, with the caveat in `metrics_reported`.
