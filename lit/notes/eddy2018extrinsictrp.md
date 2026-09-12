# eddy2018extrinsictrp

## A. Identity

- **citekey**: `eddy2018extrinsictrp`
- **doi**: 10.1021/jacs.8b03805. PMID 29874058, PMC6192543.
- **year, venue**: 2018, *Journal of the American Chemical Society* **140**(26), 8228–8235. Peer-reviewed.
- **title, authors**: "Extrinsic Tryptophans as NMR Probes of Allosteric Coupling in Membrane
  Proteins: Application to the A2A Adenosine Receptor." Eddy, M. T.; Gao, Z.-G.; Mannes, P.;
  Patel, N.; Jacobson, K. A.; Katritch, V.; Stevens, R. C.; Wüthrich, K.

> **WHY THIS PAPER IS IN THE CORPUS.** It is the **primary source for the number `21`** in the
> manuscript's own title clause — the only study anywhere that supplies a 21-residue Gα α5
> C-terminal peptide to a GPCR and reads out a **receptor-side conformational response at the
> cytoplasmic end of TM6**. It was found on 2026-09-11 only by chasing an attribution in
> `georgiou2025heterogeneity`, **which cites the wrong paper** (its ref 155,
> Eddy/Martin/Wüthrich *Structure* 2021 29(2):170–176, contains no G protein, no peptide and
> no 6.35/5.62/7.55 anywhere in its full text). See the `corrections:` line on the georgiou
> block in `INDEX.md` and `lit/analysis_review/EDDY_PRIMARY_SOURCE.md`.

> **NO PDF HELD.** Extracted 2026-09-11 from the **PMC full-text XML** (`efetch db=pmc`),
> preserved at `lit/source/pending_text/eddy2018extrinsictrp.pmc.xml` and `.txt`, which is
> **not in git**. **Locators are section names, not page numbers** — cite as
> `[eddy2018extrinsictrp, Results]`. Same convention as `yu2026domainmotion`,
> `aureli2026epath`, `kohlhoff2014gpcr`, `ingraham2023chroma`.

## B. Scope

- **system**: GPCR — **human** A2A adenosine receptor (A2AAR), expressed in *Pichia pastoris*,
  in LMNG/CHS mixed micelles. One receptor.
- **n_targets**: 1 receptor; **3 engineered variants**, each with a single extrinsic
  tryptophan near the intracellular surface: **A2AAR[F201W] (TM V, 5.62)**,
  **A2AAR[K233W] (TM VI, 6.35)**, **A2AAR[Y290W] (TM VII, 7.55)**. Plus wild type.
- **method_class**: **other — experimental solution-state NMR** (800 MHz 2D [15N,1H]-TROSY),
  plus a radioligand-binding characterisation arm. **No predictor is run anywhere.**
- **backbones**: `NOT APPLICABLE` — no structure prediction.
- **templates**: `NOT APPLICABLE`.
- **msa_handling**: `NOT APPLICABLE`.

## C. Conformational core

- **states_generated**: `NOT APPLICABLE` — nothing is generated. States are **observed as NMR
  line multiplicity**: one indole 15N–1H signal per reporter = one slowly-exchanging local
  conformation; two signals = two. That multiplicity **is** the state readout.
- **structural_priors_used**: Substantial and design-time only, and the paper is explicit.
  The three reporter sites were chosen from **crystal structures of complexes of different
  ligand efficacy** — superpositions of A2AAR with the antagonist ZM241385 (**PDB 3EML**) and
  the agonist UK432097 (**PDB 3QAK**), Figure 1 — "the selection of the three variants of
  A2AAR used was guided by model considerations. A first criterion … was to ensure a strong
  response of the NMR probes to variable drug efficacy" (Results). The probes are therefore
  **placed where the answer was already known to be**, which is legitimate design but must be
  said.
- **oracle_leakage**: `NOT APPLICABLE` as pipeline leakage — there is no pipeline. **Route 7
  (design-level) PRESENT**: reporter placement selected against known structural differences,
  as above. Routes 1–6 have nothing to leak into.
- **prospective**: `NOT APPLICABLE`.
- **state_metric**: **Discrete NMR line count plus chemical-shift displacement.** No threshold,
  no RMSD, no predicate. Reported shifts are in ppm and are given in §E.
- **metric_saturation**: **None.** Chemical shift is unbounded in the relevant range and no
  axis floors or ceilings.
- **directional_control**: **Two handles, and both are supplied co-inputs.** (i) **Orthosteric
  ligand graded by efficacy** — antagonist ZM241385 vs agonist UK432097, with theophylline as
  the low-affinity antagonist used throughout purification and later exchanged. (ii) **A
  21-residue Gαs C-terminal peptide** added to the pre-formed agonist complex. The second is
  the corpus's **only** instance of a peptide-length partner supplied to a GPCR with a
  receptor-side conformational readout.
- **coinput_composition**: **v3.1. NOT confounded, and this is the paper's value to us.**
  - arm 1: receptor + antagonist (ZM241385), alone
  - arm 2: receptor + agonist (UK432097), alone
  - arm 3: receptor + agonist (UK432097) + **21-residue GαS C-terminal peptide**, added to
    arm 2's sample
  **The peptide is added to an existing agonist complex, so the ligand is held constant and
  the partner is the only thing that changes.** That is a clean partner-alone contrast of
  exactly the kind `chiesa2025templatebias`, `zhang2026generalization` and
  `ye2026multistatebias` all lack. **There is no peptide-without-agonist arm**, so the
  peptide's effect in the absence of ligand is not measured.
- **binding_order**: **v3.1. ADDRESSED BY CONSTRUCTION, and it is sequential, not
  simultaneous.** The agonist complex is formed first and the peptide is titrated in
  afterwards — "To a sample of [u-15N, ~70% 2H]-A2AAR[K233W] **in complex with the agonist
  UK432097**, we added a 10-fold molar excess of a 21-residue synthetic polypeptide"
  (Results). This is **agonist-first, transducer-second** — conformational selection at the
  ligand level, induced fit at the transducer level. **Directly relevant to us: co-folding has
  no notion of order at all**, so a predictor handed receptor + agonist + peptide simultaneously
  cannot reproduce this design, only its endpoint.
- **input_factor_design**: **v3.2.** **ligand**: varied (antagonist / agonist). **partner**:
  varied (absent / 21-mer present). **MSA, templates**: `NOT APPLICABLE`.
  `crossings:` **ligand × partner NOT CROSSED** — the peptide is added only to the agonist
  complex, never to the antagonist complex and never alone. So the paper cannot estimate an
  interaction, and it is one more instance of the corpus-wide absence recorded for E2.2.
  Do **not** tag `factors-crossed`.
- **anti_memorization_design**: `NOT APPLICABLE`.
- **anti_memorization_control**: `NOT APPLICABLE`.
- **controls_run**:

  | control | what it rules out | locator |
  |---|---|---|
  | **Ligand-binding activity and overall fold of all three Trp variants vs native A2AAR** | That the engineered tryptophan changes the receptor. "the ligand binding activity of the three A2AAR variants and their overall protein fold are highly similar to those of the native protein" | Abstract, Results |
  | **All samples purified with the same low-affinity antagonist (theophylline), exchanged later** | That the absence of W201 and W290 agonist signals is a back-protonation artefact of different sample histories — explicitly ruled out | Discussion |
  | **Endogenous tryptophans read alongside the extrinsic ones** | That the extrinsic probe reports something the native protein does not; the endogenous response "was highly similar for A2AAR and the variant proteins" | Results |
  | **Endogenous Trp at the extracellular surface (W143, W268) as an internal spatial control for the peptide** | That the peptide perturbs the receptor globally — it does not; they "show at most a very small response" | Results |
  | **LMNG/CHS vs DDM/CHS mixed micelles** | That the membrane mimetic drives the spectra (Figure S9) | Experimental |
  | **ABSENT — peptide without agonist** | whether the peptide acts on the apo/antagonist-bound receptor. Never run. | — |
  | **ABSENT — scrambled, reversed or composition-matched peptide** | whether the effect is sequence-specific. **No negative-control peptide of any kind is run.** | — |
  | **ABSENT — any other peptide length** | whether 21 is a threshold. Only one length is used. | — |

- **confidence_as_discriminator**: `NOT APPLICABLE` — no computational confidence measure.

## D. Claims

- **central_conclusion**: Single tryptophans introduced at the intracellular ends of TM V, VI
  and VII of human A2AAR give resolved indole 15N–1H NMR signals that respond to the efficacy
  of the orthosteric drug, and — for the TM VI probe W233 (6.35) — to the addition of a
  21-residue Gαs C-terminal peptide. In the agonist complex W233 shows **two** signals; adding
  the peptide leaves **one**. The response is confined to the intracellular surface.

- **necessity_claims** (verbatim, section locators):
  - **NONE of the "X is required" form.** This is a methods paper and makes no impossibility
    claim. The nearest is a scope statement, Discussion: *"extrinsic tryptophan NMR probes
    could be broadly applicable to GPCRs, and possibly to other membrane proteins, **as long as
    the NMR probes are introduced near the intracellular surface**, as observed in previous
    19F-NMR studies of GPCRs."*

- **novelty_claims** (verbatim, section locators):
  - Introduction: *"Here, we **extend the utility** of tryptophan indole signals by introducing
    exogenous tryptophans in judiciously selected sequence locations of human A2AAR. **This new
    approach** is attractive and broadly applicable due to an efficient protocol for production
    of stable-isotope-labeled wild-type and variant GPCRs for NMR studies in solution."*
  - No "first", "unprecedented" or priority claim is made.

- **THE QUOTES THIS NOTE EXISTS FOR** (verbatim, Results):
  1. > "we added a **10-fold molar excess of a 21-residue synthetic polypeptide corresponding
     > to residues 374–394 of the carboxy terminus of the intracellular partner protein GαS**."
  2. > "An earlier study reported an **increase of the specific binding of A2AAR agonists** upon
     > addition of this polypeptide **and inability of A2AAR to signal through Gαs** after
     > addition of the polypeptide, suggesting that the polypeptide and full length GαS protein
     > bind at similar locations in A2AAR." — *their ref 14 =* `mazzoni2000gsctpeptide`
  3. > "**A single indole 15N–1H signal was observed for W233 in the ternary complex with
     > UK432097 and the polypeptide, in contrast to the two signals observed for W233 in complex
     > with UK432097 alone** … "The chemical shift of the single resonance for W233 was slightly
     > shifted in both the 1H and 15N dimensions, by ~0.06 and ~0.2 ppm, respectively, **from
     > either of the two resonances observed in the absence of the polypeptide**."
  4. > "**W29 and W32, located in helix I at the intracellular surface**, both show chemical
     > shift changes … of **~0.15 ppm in the 1H dimension and ~0.4 ppm in the 15N dimension**.
     > In contrast, **W143 and W268, located near the A2AAR extracellular surface, show at most
     > a very small response** to the addition of the polypeptide."
  5. > "the data in Figure 4 appear to be consistent with recent crystallographic studies of
     > A2AAR binary and ternary complexes involving an agonist and an **engineered "mini GαS"
     > protein**, where changes of A2AAR in the ternary complex relative to the complex with
     > agonist alone were observed in the intracellular region but not in the extracellular
     > region."
  6. > "This is in apparent contrast with NMR studies of the β1-adrenergic receptor (β1AR),
     > which reported changes in the chemical shifts of amide signals of valine residues
     > **located near the extracellular surface** upon complex formation with a
     > **G-protein-mimicking nanobody**."

- **stated_limits**: W201 (5.62) and W290 (7.55) give **no observable signal at all** in agonist
  complexes — attributed to exchange broadening, so the peptide experiment could only be done at
  W233. The authors rationalise the efficacy response as "multiple local polymorphisms, with
  variable rates of exchange", i.e. the number of lines is an exchange-regime observable and not
  a direct population count.

- **stance**: **precedent + background.** It is the *only* peptide-length partner experiment with
  a receptor-side conformational readout in the corpus, and it is the primary evidence under our
  own "21 residues". It is **not** a contrast paper — it runs no predictor and claims no priority.

## E. Quantitative comparators

- **metrics_reported**:

  | quantity | value | units | scope | locator |
  |---|---|---|---|---|
  | Peptide length | **21** | residues | GαS 374–394 | Results |
  | Peptide : receptor ratio | **10-fold molar excess** | — | added to the UK432097 complex | Results |
  | W233 (6.35) signals, agonist alone | **2** | indole 15N–1H lines | A2AAR[K233W] + UK432097 | Results, Fig 3 |
  | W233 (6.35) signals, agonist + peptide | **1** | indole 15N–1H lines | ternary | Results, Fig 4 |
  | W233 shift of the surviving line, **from either** prior line | **~0.06 / ~0.2** | ppm (1H / 15N) | ternary vs binary | Results |
  | W29, W32 (helix I, intracellular) shift on peptide addition | **~0.15 / ~0.4** | ppm (1H / 15N) | endogenous Trp | Results |
  | W143, W268 (extracellular) shift on peptide addition | "at most a very small response" | — | endogenous Trp | Results |
  | W233 signals, antagonist complex | **1** | indole 15N–1H lines | ZM241385 | Results, Fig 2 |
  | NMR field | **800** | MHz | 2D [15N,1H]-TROSY | Results |
  | Labelling | [u-15N, **~70%** 2H] | — | *P. pastoris* | Experimental |

- **n_predictions**: `NOT APPLICABLE`.
- **comparable_to_ours**: **Directly, and it is the only such paper.** The 21-mer's residue
  range (GαS 374–394) fixes the construct our title's number refers to. The readout is at the
  **cytoplasmic end of TM6**, which is one of our two predicate axes; the other, NPxxY/7.53, is
  **not** observable here because W290 (7.55) gives no agonist-complex signal. So the paper
  confirms our TM6 axis and is silent on our NPxxY axis.
- **si_in_scope**: **Figures S1–S9 are named in the text and were NOT retrieved** — S2 (secretion
  signal peptide signals), S8 (construct), S9 (LMNG/CHS vs DDM/CHS). Not required for any quote
  above.

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | n/a | Locations of the three extrinsic reporter tryptophans, on superposed A2AAR crystal structures with antagonist ZM241385 (3EML) and agonist UK432097 (3QAK) | structure render | `RENDER \| facet: reporter site (3: F201W/TM V, K233W/TM VI, Y290W/TM VII) \| views: 1 \| overlay: 2 structures (3EML, 3QAK) \| axis: none` | 3 | the structures are wild-type crystal structures, not the Trp variants | ACS — check before adapting |
| 2 | n/a | Assignment of the indole 15N–1H lines of each single extrinsic Trp; 2D TROSY contour plots plus 1D cross sections, variant (red) over wild type (blue), antagonist complex | contour + 1D trace | `MATRIX \| rows: 1H shift (continuous) \| cols: 15N shift (continuous) \| facet: variant (3) \| series: protein (2: A2AAR, variant) \| n: 1 spectrum per panel` | 3 (+3 cross sections) | — | ACS |
| 3 | n/a | NMR response of the three extrinsic Trp indoles to ligands of different efficacy — the efficacy series | contour | `MATRIX \| rows: 1H shift \| cols: 15N shift \| facet: variant (3) × ligand efficacy (several) \| n: 1 spectrum per panel` | variant × ligand grid | **dashed circles mark where W201 and W290 signals were EXPECTED and not found** — an absence drawn as a presence; read the text | ACS |
| 4 | n/a | **The peptide experiment.** A2AAR[K233W]+UK432097 before (blue) and after (red) addition of the 21-residue GαS C-terminal peptide, superposed; right panel a 15N projection | contour + projection | `MATRIX \| rows: 1H shift \| cols: 15N shift \| facet: none (1) \| series: peptide (2: absent, present) \| overlay: 2 spectra \| n: 1 sample` | 2 | **n = 1 sample, no replicate and no error estimate is shown or stated** | ACS |
| 5 | n/a | Expression/purification scheme for human A2AAR in *P. pastoris*, and the construct diagram (10×His, FLAG) | schematic | `SCHEMATIC \| no data` | 2 (A, B) | — | ACS |

## G. Provenance

- **extracted_on, by**: 2026-09-11, lit-3d, from PMC6192543 full-text XML via NCBI efetch.
- **schema_version**: `v3.2`
- **confidence**: **high for every quoted string** — **all 7 double-quoted verbatim spans in
  this note were machine-verified against the retrieved full text (7/7) by
  `validate/quotecheck_plaintext.py`, which self-tests that it can both pass and fail.** It
  caught one real defect on its first run: quote 3 originally elided "( Figure 3 )" without
  marking the elision, now marked. Every number in §E was taken from the XML body text, and the XML carries the
  full article (Introduction, Results, Discussion, Experimental Section). **Medium for §F** —
  figure rows were built from the **captions in the XML**, not from viewing the panels; the
  images were not retrieved. Rows are marked accordingly and `data_shape` for Fig 3's facet
  count is approximate.
- **unresolved**:
  1. **The exact ligand set in Figure 3 is not enumerable from the caption.** ZM241385 and
     UK432097 are named in the text; the caption says only "ligands of different efficacies
     identified in the panels on the left". Viewing the figure would settle it.
  2. **Page numbers.** No PDF is held, so no `p.N` locator exists for any quote. Printed pages
     are 8228–8235; section names are the locator.
  3. **Figures S1–S9 not retrieved.**
  4. **Whether the 21-mer carries the C379A substitution** used by `mazzoni2000gsctpeptide` is
     not stated here — the text says only "21-residue synthetic polypeptide corresponding to
     residues 374–394". Given the nine opsin α5 entries are *all* mutants, this matters and is
     worth resolving.
  5. **n = 1.** No replicate, error bar or repeat is reported for the Figure 4 peptide titration
     anywhere in the retrieved text. The result is a single spectrum pair.
- **why_it_matters**: *(user's call — left empty per SCHEMA)*
