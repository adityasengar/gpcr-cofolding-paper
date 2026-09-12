# chiesa2025templatebias

> **Extraction provenance.** Extracted 2026-09-09 from the **published ACS PDF**, supplied by the
> user through institutional access after every automated route failed. Page numbers below are
> **journal pages**: PDF page *N* maps to journal page 6297+*N*, verified against the printed
> footers. Main text read in full; the Supporting Information (Table S1, Figures S1–S2) was not
> retrieved. See `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `chiesa2025templatebias` |
| `doi` | 10.1021/acs.jcim.5c00489 |
| `year`, `venue` | 2025 — **J. Chem. Inf. Model. 65(12):6298–6309**, peer-reviewed. Online 29 May 2025, in issue 23 June 2025. |
| `title` | Modeling Active-State Conformations of G-Protein-Coupled Receptors Using AlphaFold2 via Template Bias and Explicit Protein Constrains (*sic*, "Constrains" is the published spelling) |
| `authors` | Luca Chiesa, Dina Khasanova, Esther Kellenberger (Université de Strasbourg) |

> **Read this note before writing any sentence about our own novelty.** This is the closest
> published work to the axis this manuscript occupies: it supplies a **G protein as a co-input**
> to a co-folding model and then **measures the receptor's activation state**. Both halves. It is
> a nearer near-miss than `yang2025statespecific` on the co-input axis, and the gap paragraph must
> be written against it rather than around it. See `stance`.

## B. Scope

| field | value |
|---|---|
| `system` | **GPCR, class A**, human receptors bound to human Gαs. |
| `n_targets` | **63 unique GPCR–Gα pairs, 145 experimental structures, 55 receptors, 31 receptor families** (p6302, Table S1). Restricted: "The benchmark data set was limited to structures of human GPCRs bound to human Gαs to reduce the complexity of the study." (p6302). Only **16** of the 145 structures represent "the receptor bound only to G-protein" (p6302), so nearly all carry a ligand as well. |
| `method_class` | **benchmark-only**, comparing six prediction protocols head to head; spans template-state-bias, MSA-state-filter and co-folding. |
| `backbones` | **AF2** and **AlphaFold-Multimer**. Six protocols (Table 1, p6299): AF2-default; AF2-multistate (Heo & Feig); AF2_GPCR_Kinase; **AFM-Gα** (receptor co-folded with Gα); **AFM-GProteinDB** (models taken from the GproteinDB resource, some with the full heterotrimer, some Gα alone); AFM-receptor (free receptor through AFM). The AF3-lineage models are discussed but **not run**. |
| `templates` | **on and state-annotated in some arms.** "Both methods use active-state templates, based on GPCRdb annotation, to model the structures in the desired activation state, while also removing part of the MSA information by masking (AF-multistate) or subsampling (AF2_GPCR_kinase)." (p6299) |
| `msa_handling` | **dual by arm**: full, subsampled, or masked, depending on protocol (Table 1, p6299). |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **two-state + single-state.** Each protocol produces one model per target; the comparison across protocols is what spans the two states. Not an ensemble method. |
| `structural_priors_used` | **Substantial and stratified, which is what makes the paper useful.** Active-state templates from GPCRdb annotation feed two arms. Reference complexes come from GProteinDB and GPCRdb (both 16 July 2024 releases). Critically, the authors **quantify** the prior rather than merely disclosing it: "Out of the 145 experimental structures in the benchmark set, **94 represent a receptor with no template structure and are not in the training set of the two models**" (p6302), and "Six receptor families in the benchmark data set were not present as either a template or in any training set (bombesin, hydroxycarboxylic acid, relaxin family peptide, olfactory, chemerin, trace amine)" (p6302). |
| `oracle_leakage` | **Seven routes.**<br>**Route 1 — PRESENT by design in two arms**, absent in others. AF2-multistate and AF2_GPCR_Kinase pin active-state templates; AFM-Gα and AFM-receptor do not. The paper's contribution is the contrast between them.<br>**Route 2 — PRESENT.** GPCRdb activation-state annotation drives the template selection in the two multistate arms (p6299).<br>**Route 3 — NONE FOUND.**<br>**Route 4 — NOT REPORTED.** No hyperparameter sweep is described; default pipelines are used per protocol.<br>**Route 5 — PRESENT, definitionally.** Every quality number is an RMSD or DockQ against the deposited complex.<br>**Route 6 — PARTIAL.** Model selection within a protocol is not described in the retrieved text; flagged in `unresolved`.<br>**Route 7 — PRESENT, design-level and unusually well bounded.** Targets are complexes with deposited structures, but the temporal split and the 94/145 no-template-no-training figure quantify how much of the answer was actually available. |
| `prospective` | **partial, and better bounded than most of this corpus.** "The benchmark data set was defined as formed by all experimental structures of class A GPCRs bound to G-protein released after 01 Jan 2023" (p6302), against training cutoffs of May 2018 (AF2) and October 2021 (AFM) (p6302). Prospective in target selection, retrospective in scoring. |
| `state_metric` | **RMSD-to-reference + continuous coordinate**, resolved per structural element rather than globally, which is the methodological strength. Per-TM Cα-RMSD, with TM6 singled out; per-ICL RMSD; **per-residue binding-site RMSD with an explicit threshold**: "The per-residue RMSD of all residues forming this binding site was measured, and a side chain was considered as well as predicted if all heavy-atom RMSDs were below 2 Å." (p6303). Interface quality by **DockQ** against the receptor–Gα interface (p6302). **There is no operationalised activation predicate**: the receptor is not called active or inactive by a geometric rule, it is scored by distance to the deposited active reference. That distinction is the one our own design turns on. |
| `metric_saturation` | **Yes, at the DockQ end.** "Most of the predicted structures were of medium quality (107), followed by acceptable structures (34), and only two complexes were described as of high quality." (p6302) — 141 of 143 sit in two adjacent bins, so DockQ cannot separate protocols. The discriminating signal is in the per-TM RMSDs, not the interface score. Anyone quoting this paper on interface quality should quote the distribution, not a mean. |
| `directional_control` | **Yes, and by two different handles that the paper compares directly.** Handle A is the operator's: state-annotated active templates plus MSA masking or subsampling. **Handle B is biological: the G protein itself, supplied as a co-input.** The finding is that B beats A on the large rearrangements. "TM5, TM6, and TM7 present three distinct groups, with the models explicitly modeling G-protein binding outperforming the others, AFM-receptor and multistate modeling approaches presenting higher RMSD values but generally reproducing an active-like conformation, and default AF2 generating [inactive-like models]" (p6302). |
| `coinput_composition` | **New in v3.1. PARTIALLY CONFOUNDED.** AFM-Gα and AFM-GProteinDB arms supply receptor + Gα (some GProteinDB models carry the full heterotrimer); AFM-receptor supplies the receptor alone through the same model, which is the one genuinely matched comparison in the paper and the reason its partner claim is worth more than most. **But only 16 of the 145 benchmark structures represent the receptor bound to G protein alone** (p6302) — the other 129 also carry a ligand, and the ligand is never varied as an arm. No decoy, truncated or scrambled partner is run. So the partner-versus-no-partner contrast is clean; the partner-versus-occupancy contrast does not exist. Tag `coinput-confounded`. |
| `binding_order` | **New in v3.1. ORDER-AGNOSTIC by construction** — AF2 and AlphaFold-Multimer receive all chains at once. NOT ADDRESSED as a question in the text. |
| `input_factor_design` | **New in v3.2. PARTIALLY CROSSED, and confounded with backbone.** **MSA**: varied by arm (full / subsampled / masked). **templates**: varied by arm (state-annotated on, or off). **ligand**: present in 129 of 145 reference structures but **never varied as an arm**. **partner**: **VARIED** — AFM-Ga vs AFM-receptor is the matched contrast. <br>`crossings:` **templates x partner is approached but not cleanly crossed**: the template arms are AF2 and the partner arms are AlphaFold-Multimer, so the template/partner contrast is confounded with the backbone change. **MSA x ligand HELD; partner x ligand HELD** — the ligand is never removed, so the partner-versus-occupancy contrast does not exist (already recorded in `coinput_composition`). |
| `anti_memorization_design` | **PRESENT and well constructed.** Temporal split at 01 Jan 2023 against two separate model cutoffs, plus an explicit accounting of template availability and training-set membership per structure, plus six receptor families with no template and no training presence at all (p6302). |
| `anti_memorization_control` | **RUN AND ANALYSED, and it is load-bearing for their main claim.** The 94-of-145 no-template-no-training subset and the six unseen families are used to argue that the AFM advantage is not merely a training-set artefact: "The better performances of AFM compared to AF2 should not be attributed only to a more recent and active-state biased training set, but rather to its ability in modeling allosteric effects during the cofolding process." (p6305). Powered (n = 94). |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT REPORTED as a state discriminator.** pLDDT/ipTM are not used to judge conformational correctness anywhere in the retrieved text. DockQ is used for interface quality, not for state. |

### `controls_run`

| control | what it rules out | page |
|---|---|---|
| AF2-default arm | that any protocol would produce active-like models | p6302 |
| AFM-receptor (free receptor through the same model) | **that the gain comes from AFM's training set rather than from supplying the partner** | pp6302, 6305 |
| AF2-multistate and AF2_GPCR_Kinase arms | that operator-supplied templates are equivalent to the partner | p6302 |
| AFM-GProteinDB arm | that a public resource's models are equivalent | p6302 |
| Temporal split at 01 Jan 2023 against two cutoffs | training-set memorisation | p6302 |
| 94/145 no-template-no-training subset; six unseen families | that the effect needs a seen receptor | p6302 |
| Cross-docking into predicted vs experimental structures | that backbone accuracy implies usable binding sites | pp6303–6304 |
| **Absent:** decoy or scrambled partner arm | — | — |
| **Absent:** any AF3-lineage backbone | — | — |

## D. Claims

- **`central_conclusion`**: Across six AlphaFold protocols on a post-cutoff set of 63 class A
  GPCR–Gαs pairs, explicitly co-folding the receptor with its G protein reproduces the large
  intracellular rearrangements of activation more accurately and more reliably than
  operator-supplied active-state templates with MSA masking or subsampling. The advantage survives
  on receptors absent from templates and training, so it is attributed to co-folding rather than
  to a state-biased training set. The extracellular ligand-binding site, however, is not improved
  by supplying the partner, and its quality tracks training-set composition instead, so the
  modelled allosteric effect is local rather than global.

- **`necessity_claims`** (verbatim + page):
  - p6298 (abstract): "AlphaFold2 and other deep learning tools represent the state of the art for
    protein structure prediction; however, they are still **limited in their ability to model
    multiple protein conformations**."
  - p6298: "Since the function of many proteins depends on their ability to assume different stable
    conformational states, **different approaches are required to access these alternative
    conformations**."
  - p6298, and this is the sentence our work is positioned against: "Retrospective studies have
    demonstrated that, for many receptors, the inactive state is the favored conformation generated
    by AlphaFold2 when the receptor is modeled alone, while **active-state structures can only be
    modeled by introducing a conformational bias in the template information used for the
    prediction or by explicitly incorporating the binding of a ligand into the modeled system**."
  - p6305: "and inactive-like conformation of the binding site, or **the conformation of the
    binding site cannot be predicted with sufficient accuracy, regardless of the used templates**."
  - p6305: "Despite the good performances of the prediction protocols, **there is still a
    significant gap compared to that of experimental structures**."

- **`novelty_claims`** (verbatim + page):
  - p6299: "The modeling of active-state conformations of GPCRs has mostly focused on the use of
    AlphaFold2 to model state-specific conformations of the receptor, **while the use of
    AlphaFold-Multimer to explicitly model the allosteric effects triggered by G-protein binding
    has not been fully investigated**." *(the priority claim, and it is a narrow one. The PDF text
    layer renders "state-specific" as "statespecific" because the hyphen falls on a line break;
    the hyphen is restored here and the artifact recorded so a mechanical quote check does not
    flag it as fabricated.)*
  - p6299: "Here, we propose to compare different modeling strategies using AlphaFold aimed at
    predicting the active-state structure of class A GPCRs, evaluating both the larger structural
    rearrangements at the Intracellular side linked to G-protein binding, as well as the smaller
    rearrangements in [the extracellular site]."
  - p6305: "The better performances of AFM compared to AF2 should not be attributed only to a more
    recent and active-state biased training set, but rather to **its ability in modeling allosteric
    effects during the cofolding process**."

- **`stated_limits`** (verbatim + page):
  - p6302, scope: "The benchmark data set was limited to structures of human GPCRs bound to human
    Gαs to reduce the complexity of the study."
  - p6305, the negative half of their own result: "the quality of the extracellular transmembrane
    binding site seems to be determined mostly by the quality of the training set, rather than by
    better modeling conditions or by a conformation-biased input, **suggesting that allosteric
    effects could only be predicted at a local level**."
  - p6298 (abstract): "while also revealing limitations in the modeling of allosteric effects,
    particularly the reduced accuracy of predictions at the receptor extracellular site, which may
    impact their applicability in structure-based drug design."
  - p6304: "no correlation was observed between the RMSD of poses obtained in the experimental
    structure and in the AlphaFold structural models; therefore, the poor performances should be
    attributed only to the quality of the structure".
  - p6299, on generality: "We believe that the benchmark analysis proposed here for AlphaFold2
    could also be applied to these more recent models, forming a baseline" — i.e. AF3, Boltz, Chai
    and RFAA are explicitly **not** evaluated.

- **`stance`**: **`contrast` + `precedent`** — provisional, the user's call, and **this is the most
  important stance call in the corpus for our novelty argument.**
  - *Precedent, and it narrows our claim.* This paper already establishes, on 63 post-cutoff class A
    pairs, that supplying the G protein as a co-input drives the receptor toward the active state
    better than operator-supplied templates do, and that the effect survives on receptors absent
    from templates and training. Any sentence of ours implying that nobody has induced a GPCR's
    active state with a biological co-input and then measured the receptor is **false**, and would
    be caught immediately by this paper's authors.
  - *Contrast, and this is where our work still stands.* Four differences, all real and all
    checkable. (i) **The co-input is the whole Gα subunit or heterotrimer**, not a 21-residue α5
    C-terminal peptide, so the paper cannot separate the α5 contact from the rest of the interface.
    (ii) **The state is scored by RMSD to the deposited active reference of that same complex**,
    not by an operationalised predicate applied blind, so it cannot be run on a receptor whose
    active structure is unsolved. (iii) **There is no decoy or scrambled-partner arm**, so
    occupancy and identity are not separated. (iv) **No AF3-lineage backbone is run**; AF2 and
    AlphaFold-Multimer only, and the authors say so themselves (p6299).
  - **Action required:** the gap paragraph in `draft/intro.md` must be rewritten to name this paper
    and state the four differences. `C4` and `C5` in `../CLAIMS.md` both need qualification.

## E. Quantitative comparators

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Benchmark size | 63 unique GPCR–Gα pairs / 145 experimental structures | count | post-01 Jan 2023 release | p6302 |
| Receptors / families covered | 55 receptors / 31 families | count | GPCRdb classification | p6302 |
| Structures with no template and not in training | 94 of 145 | count | AF2 and AFM cutoffs | p6302 |
| Receptor families absent from templates and all training | 6 | count | — | p6302 |
| Structures with receptor bound to G protein only (no ligand) | 16 of 145 | count | — | p6302 |
| DockQ quality distribution | 107 medium / 34 acceptable / 2 high | count | receptor–Gα interface | p6302 |
| Binding-site side-chain criterion | all heavy-atom RMSD < 2 Å | Å | per-residue vs reference | p6303 |
| Class A structures in GPCRdb at study time | 1022 structures / 161 receptors / 49 families | count | GPCRdb 16 Jul 2024 | p6302 |

**The per-TM RMSD values are the paper's real result and are reported in figures, not in the text
that was read.** They are the numbers our own comparison would need. Flagged in `unresolved`.

- **`n_predictions`**: **NOT REPORTED in the retrieved text.** Models per protocol per target and
  seed counts are not stated. This matters: with one model per target there is no ensemble and no
  best-of-N, but the note cannot confirm it.
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **PARTIALLY HELD as of 2026-09-10.** The SI PDF was obtained
  (`../source/si/chiesa2025templatebias_SI.pdf`, 12 pp) and **Table S1, the full benchmark
  list, is extracted** to `../panels/si_tables/chiesa2025templatebias_tableS1.csv`: 145 PDB
  entries, 55 receptors, 31 families — all four published counts reproduce exactly, and all
  145 join to GPCRdb. Tables S2–S12 (per-domain Pearson R between protocols) and Figures
  S1–S2 are in the file but **not extracted**.

  **Table S1 resolves an ambiguity in the `n_targets` quote that this note had not flagged:
  "human GPCRs bound to human Gαs" means Gα subunits, PLURAL, not Gα-s the stimulatory
  subtype.** The 145 structures carry nine Gα subtypes and
  are dominated by **Gαi1 (77)**, with Gαs second at 44, then Gαo 9, Gαq 7, Gαi2 4, and one
  each of Gα13, Gαz, Gαt3, Gα11. This is why the paper's 63 receptor–Gα pairs exceed its 55
  receptors. **Do not describe this benchmark as Gs-coupled.**

  Two further facts only the table shows: **every one of the 145 is active-state and every
  one is G-protein-bound**, so the target set contains no inactive arm; and the panel shares
  only **20 receptors** with `zhang2026generalization`'s 253-complex benchmark.

  **The stated selection rule under-determines the panel.** Re-running "class A GPCRs bound
  to G protein released after 01 Jan 2023, human receptor and human Gα" against GPCRdb admits
  152 further structures in the same window across 23 receptors the panel omits entirely,
  with identical method (100% cryo-EM) and near-identical resolution. No date bound separates
  them. Cite the table, never the rule.

## F. Figures

Seven figures identified from the main text; **panels not viewed in detail.**

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 6299 | The six prediction protocols, drawn | schematic | `SCHEMATIC \| six protocol pipelines side by side \| no data` | 6 | — | ACS, all rights reserved; check before adapting |
| 3 | 6302 | Template and training-set availability per receptor family across the benchmark | NOT EXTRACTED | NOT EXTRACTED | — | — | as above |
| (A–D) | 6301 | TM RMSD distributions, TM6 RMSD, per-family average TM RMSD, and count of binding-site residues with RMSD > 2 Å | box or bar with error bars | `PLOT \| facet: quantity (4) \| vary: protocol (6) \| series: none \| measure: Cα-RMSD (Å) / residue count \| n: 145 structures per panel` | 4 (A–D) | Error bars are s.d.; per-protocol distributions pooled across 31 families | as above |
| 7 | 6303 | Cross-docking pose RMSD in experimental vs predicted structures | NOT EXTRACTED | NOT EXTRACTED | — | — | as above |
| S1–S2 | SI (not held) | Per-TM RMSD detail | NOT EXTRACTED | NOT EXTRACTED | — | — | as above |

## G. Provenance

- **`extracted_on`**: 2026-09-09
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **high** on identity, scope, protocol design, the anti-memorization
  construction, the conclusions and every quoted claim, all read from the published PDF with
  verified page mapping. **Low** on the per-TM RMSD numbers, on model/seed counts, and on
  everything in the SI.
- **`unresolved`**:
  1. **Per-TM and TM6 RMSD values** are in figures, not in the text that was read. These are the
     numbers a comparison against our own results would need.
  2. **Models per target and seed count NOT REPORTED** in the retrieved text.
  3. **Oracle route 6**: whether a single model or a best-of-N was scored per protocol.
  4. ~~SI Table S1 (benchmark composition) not held.~~ **RESOLVED 2026-09-10** — SI obtained
     and Table S1 extracted; see `si_in_scope`. Tables S2–S12 remain unextracted.
  5. Whether "explicitly incorporating the binding of a ligand" in the abstract's necessity claim
     is meant to include a protein partner or only a small molecule. The rest of the paper treats
     them separately, so the abstract sentence is looser than the body.
- **`why_it_matters`**: *(left empty by the extractor — the user's call. But see `stance`: this
  paper narrows our novelty claim and the intro must be rewritten against it.)*

## Tags

```
gpcr cofolding benchmark-only template-state-bias msa-state-filter msa-subsample templates-on
state-annotated-input two-state single-state rmsd-only continuous-metric binary-predicate
saturating-metric oracle-leak design-level-oracle prospective anti-memorization multi-backbone
directed-state partner-driven ligand-driven orthosteric allosteric-site peer-reviewed
precedent contrast comparator-numbers
```

**Tag notes.** `partner-driven` **and** `directed-state` are both applied, and this is the only
paper in the corpus where `partner-driven` co-occurs with a verified receptor-state measurement:
`matic2023gpcrome`, `miglionico2026atlas` and `pandyszekeres2024gproteindb` all supply the partner
and never check the state. That distinction is exactly what a reverse lookup on this axis needs to
surface, so read the `state_metric` field, not just the tags. `confidence-as-discriminator`
**deliberately not applied** — confidence is never used to judge state here.
