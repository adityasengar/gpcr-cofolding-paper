# ibrahim2019a100

> # ✅ UPGRADED TO FULL TEXT 2026-09-14 — the relay is CLOSED and it VERIFIED
>
> This note was `v3.2-abstract-only` for one day. **Aditya supplied the PDF through
> institutional access on 2026-09-14** and it is now held at `pdfs/ibrahim2019a100.pdf`
> (8 pp).
>
> **The critical result: our pipeline's implementation of A100 matches the published
> definition exactly.** All five Ballesteros–Weinstein pairs, all five coefficients, the
> intercept and both threshold schemes are correct, and the 50-receptor figure I had flagged
> as unverified is also correct. **The concordance numbers computed against it on 36,860
> predictions are safe.** The verification is in §C.
>
> **PAGE OFFSET +3937** — PDF p1 = printed p.3938. Detected and confirmed automatically by
> `validate/pageoffset.py` against `refs.bib`. **All locators below are PRINTED folios.**

## A. Identity

- **citekey**: `ibrahim2019a100`
- **doi**: 10.1021/acs.jcim.9b00604. PMID 31findable via Europe PMC; no PMCID.
- **year, venue**: 2019, *Journal of Chemical Information and Modeling* **59**(9), 3938–3945.
  Peer-reviewed.
- **title, authors**: "Universal Activation Index for Class A GPCRs."
  Ibrahim, P.; Wifling, D.; Clark, T.

> **WHY IT IS HERE, AND IT CHANGES AN INSTRUMENT ARGUMENT.** This project has been recording
> that **almost nobody in this literature uses an operationalised activation predicate** rather
> than RMSD-to-the-deposited-answer, and that the two nearest indices are not reimplementable —
> `paajanen2026activation` ships no weight vector, no residue list and no repository, and
> `khaleq2026hyaline` never reports its decision threshold. **This paper is a published,
> operationalised, class A activation predicate that the authors say ships as runnable code.**
> It was reached only as a secondhand mention inside `paajanen2026activation`; that note's
> description of it is a report of a report and is **not** quotable as an extraction.
> Added 2026-09-14.

## B. Scope

- **system**: GPCR, **class A**, explicitly universal across the class.
- **n_targets**: **268 published X-ray structures** for testing; training is on *"a series of
  microsecond molecular-dynamics simulations"* — **`UNRESOLVED (abstract-only)`: how many
  receptors, which ones, and how much simulation.**
- **method_class**: **other — a trained structural index / classifier**, not a structure
  predictor. No generation of any kind.
- **backbones / templates / msa_handling**: `NOT APPLICABLE`.

## C. Conformational core

- **states_generated**: `NOT APPLICABLE` — nothing generated; deposited and simulated
  structures are **classified**.
- **state_metric**: **an operationalised index built on five interhelix Cα–Cα distances**, with
  both a **three-class** (active / intermediate / inactive) and a **two-state** model.
  Verbatim **from the publisher's abstract as served by Europe PMC** (this exact string is not
  recoverable from the PDF text layer — see the extraction note in §G): *"The five interhelix
  C<sub>α</sub>-C<sub>α</sub> distances that occur in the model relate clearly to the established
  activation mechanism."*

  **VERIFIED AGAINST THE PAPER 2026-09-14. The relay is closed.** Published equation,
  verbatim from **p.3940**:

  > "A100 = −14.43 × r(V1.53−L7.55) − 7.62 × r(D2.50−T3.37)"
  > … "+ 9.11 × r(N3.42−I 4.42) − 6.32 × r(W 5.66−A6.34)"
  > … "− 5.22 × r(L6.58−Y7.35) + 278.88"

  *(**Reconstruction note.** The paper is two-column and `pdftotext` interleaves equation (1)
  with the adjacent column, so the equation does not exist as one contiguous string in any
  extraction. The three fragments above are each verbatim and each machine-verified; the
  single-line form in the table below is **assembled from them**, not quoted. Flagged because
  an assembled equation is exactly the kind of thing that should not pass as a quotation.)*

  | component | BW pair | **residues (new — not in our pipeline)** | coefficient |
  |---|---|---|---:|
  | c1 | 1.53 – 7.55 | **V1.53 – L7.55** | −14.43 |
  | c2 | 2.50 – 3.37 | **D2.50 – T3.37** | −7.62 |
  | c3 | 3.42 – 4.42 | **N3.42 – I4.42** | +9.11 |
  | c4 | 5.66 – 6.34 | **W5.66 – A6.34** | −6.32 |
  | c5 | 6.58 – 7.35 | **L6.58 – Y7.35** | −5.22 |
  | intercept | | | +278.88 |

  **Every pair, every coefficient and the intercept match `redo/protocol/received/axes.d9c646af.py`
  exactly.** The residue identities are new information the pipeline comment does not carry, and
  they are worth having: they let the BW resolution be checked per receptor rather than assumed.

  **Thresholds, verified.** Three-state, **p.3941**: *"Inactive: A100 < 0"* … *"Active: A100 >
  55"*. Two-state, **p.3941**: *"model in which the A100 border lies at 25 classifies both the
  active and the inactive structures assigned experimentally extremely well (94% and 99%
  accuracy, respectively)"*.

  **Direction of motion, p.3940** — useful because it explains the signs: *"All but one of the
  distances (N3.42−I4.42) becomes shorter on"* activation; TM6 *"moves closer to TM1
  (V1.53−L7.55)"*, TM3 moves *"away from TM4 (N3.42− I4.42) and"* … *"toward TM2 (D2.50−T3.37)"* — **the two
  halves are separated by an interleaved column in the text layer; joined here, not quoted as
  one span.**

  **What the abstract withheld and the paper gives.** Training set is **9 receptors**, validation **50** (p.3944). **Stated as fact, not quoted:**
  the sentence reads *"Alignment of the 9 receptors in the training set and the"* … *"50 unique
  ones in the X-ray structures"* with an interleaved column between the halves, so there is no
  contiguous span to quote. The index is trained on nine receptors and validated on fifty — a
  real separation, and larger than the abstract let me assume. Validation set confirmed at **p.3941**: *"the sequences of 50 receptors in 268
  GPCR crystal structures were aligned as described above."*

- **structural_priors_used**: the index is trained on MD and validated against the
  experimental activation-state assignment of deposited structures, so the deposited labels
  are the target. **`UNRESOLVED (abstract-only)`** as to which annotation source.
- **oracle_leakage**: `UNRESOLVED (abstract-only)`. Route 5/6 are live in principle — success
  is agreement with deposited state assignments — but the split between training (MD) and test
  (X-ray) is a genuine separation and is the paper's design.
- **prospective**: `NOT APPLICABLE`.
- **directional_control**: `NOT APPLICABLE` — it measures state, it does not produce one.
- **confidence_as_discriminator**: `NOT APPLICABLE`.
- **controls_run**: `UNRESOLVED (abstract-only)`, except the nanobody check below, which is
  reported as a result rather than a control.

## D. Claims

- **central_conclusion**: A five-distance index trained on microsecond MD reproduces the
  experimental activation-state assignment of 268 deposited class A GPCR structures — 94%
  of actives and 99% of inactives under a two-state model — and is distributed as runnable code.

- **THE QUOTES THIS NOTE EXISTS FOR** (verbatim, `[ibrahim2019a100, Abstract]`):
  1. > "An index of the activation of Class A G-protein-coupled receptors (GPCRs) has been
     > trained using interhelix distances from a series of microsecond molecular-dynamics
     > simulations and tested for 268 published X-ray structures."
  2. > "In a three-class model that includes intermediate structures, 63% of the active
     > structures are classified in agreement with the experimental assignment, 81% of the
     > intermediate structures, and 89% of the inactives."
  3. > "An alternative two-state model classifies 94% of the actives and 99% of the inactives
     > correctly."
  4. > "The intermediate structures are distributed 2:1 between actives and inactives."
  5. > "X-ray structures with protein nanobodies give good agreement between the assigned
     > activation state and the predictions of the model, whereby many active nanobody
     > structures are predicted to be weakly active."
  6. > "The model is available as a Python script or via an interactive web page. It can thus be
     > used to classify both experimental and computational GPCR structures."

- **stance**: **precedent, and it is an instrument we may adopt rather than only cite.**
  Quote 6 is the one that matters: *"available as a Python script"* plus *"can thus be used to
  classify both experimental and **computational** GPCR structures"* — the authors state our
  exact use case. **If the script is obtainable, this is a reimplementable third-party predicate
  we can report concordance against, which is what E0.2 has been unable to find.**

## D2. Concordance against our own predicate — measured 2026-09-14

**Reported by paper-6f from held Block D data; not computed here.** The A100 call against our
two-instrument conjunction, per prediction:

| block | n | agreement | ours ACTIVE / A100 inactive | ours inactive / A100 ACTIVE |
|---|---:|---:|---:|---:|
| D1 | 14,000 | **88.3%** | 2.3% | **9.4%** |
| D3 | 22,860 | **90.8%** | 3.9% | **5.4%** |

`a100_index` is present on 100% of D1 rows and 96.2% of D3. **The asymmetry is consistent in
both blocks: the published index calls MORE predictions active than our conjunction does.**

**Three things bound this and all three must travel with the number.**
1. **A100 is NOT axis-independent from our tilt instrument** — `r = +0.846 / +0.764` against
   TM6 tilt on our own data. It is an **independently published** index, which is a different
   and weaker kind of independence. **Any sentence must say which one it means.**
2. **Ibrahim validated on X-ray structures; these are predictions.** The comparison is worth
   making and is not the validation the paper did.
3. **The definition we computed with is a relay** (see `state_metric`) — our pipeline's reading
   of the paper, unchecked against the PDF.

**Two hooks from the abstract are now directly testable on held data**, and neither has been run:
- *"many active nanobody structures are predicted to be weakly active"* → against **Block D2's
  nanobody arms**, held at row level.
- the **2:1 intermediate split toward active** → against the **21 Class A Intermediate
  structures** measured by E0.1.

## D3. The nanobody hook — now sourced from the paper, and sharper than the abstract

**The pre-registered test (see `DECISIONS.md`, and `CLAIMS.md`) can now be stated with the
paper's own numbers rather than from its abstract.**

- **p.3938 (abstract):** *"X-ray structures with protein nanobodies give good agreement between
  the assigned activation state and the predictions of the model, whereby **many active nanobody
  structures are predicted to be weakly active**."*
- **p.3942** carries **Table 3, "Details of GPCR X-ray Structures with Nanobodies and Their
  Calculated A100 Values"** — per-structure PDB IDs, resolutions, assigned state, G-protein,
  antibody and A100. **That table is a ready-made external comparator for our own nanobody
  arms.**
- The labelling premise is the same one our corpus records: *"these structures have been
  assigned to the active state, as protein nanobodies were"* used as surrogates for bound G
  proteins (p.3942). **The phrase "surrogates for bound / G-proteins" is split by an interleaved
  column and is paraphrased here rather than quoted.**
- **The quantitative form of "weakly active", and this is the part the abstract hides:** the
  A100 histogram for nanobody structures has *"a maximum in the A100 = 35−40 bin and some skew
  toward active structures"* (p.3942), and *"nanobody-stabilized structures tend to be weakly
  active"*.

**So "weakly active" is precise: above the two-state cut (25) but well below the three-state
active cut (55) — i.e. peaking inside the three-state INTERMEDIATE band (0–55).** A nanobody-
stabilised structure is called active by the two-state model and intermediate by the
three-state model, **from the same index, on the same structure**.

**Why that matters to us.** `khaleq2026hyaline` p12 counts *"G protein-coupled or G
protein-mimetic nanobody-bound structures"* as active **by construction**. A published
geometric index puts the same structures in the intermediate band. **That is the measured gap
between a pharmacological and a geometric convention, and this paper already reports it on
X-ray structures — so our Block D2 test would be the first measurement of it on PREDICTED
structures, not the first measurement at all.** The pre-registration should say so; claiming
novelty for the gap itself would be wrong.

**And the paper has a section we should read before designing that test:** *"Differences Between
G-Protein-Stabilized Agonist−GPCR Complexes and their Nanobody-Stabilized Equivalents."* It is
the exact contrast our reference sets collapse.

## E. Quantitative comparators

| quantity | value | scope | locator |
|---|---|---|---|
| Test set | **268** | published X-ray structures | Abstract |
| Index dimensionality | **5** | interhelix Cα–Cα distances | Abstract |
| Three-class agreement, actives | **63%** | vs experimental assignment | Abstract |
| Three-class agreement, intermediates | **81%** | | Abstract |
| Three-class agreement, inactives | **89%** | | Abstract |
| Two-state agreement, actives | **94%** | | Abstract |
| Two-state agreement, inactives | **99%** | | Abstract |
| Intermediates split | **2:1** | actives : inactives | Abstract |
| Which five distances / thresholds | **`UNRESOLVED (abstract-only)`** | — | — |

- **comparable_to_ours**: **Three ways, and one of them is a warning.**
  (i) It is a **candidate independent index for E0.2's concordance check**, and unlike
  `paajanen2026activation` it claims to ship code.
  (ii) **Its three-class model reports intermediates explicitly and splits them 2:1 towards
  active** — directly relevant to the agonist-only / intermediate calibration question, where
  `paajanen2026activation` dropped intermediates for low n.
  (iii) **The warning, quote 5: "many active nanobody structures are predicted to be weakly
  active."** Our reference sets and several corpus panels treat nanobody-bound structures as
  fully active — `khaleq2026hyaline`'s rule does so explicitly. **An independent index
  disagrees with that convention on exactly those structures.** That is checkable against our
  own panel and should be.
- **si_in_scope**: `UNRESOLVED (abstract-only)`.

## F. Figures

**`UNRESOLVED (abstract-only)` — no figure seen or counted.** Not usable for figure design.

## G. Provenance

- **extracted_on, by**: 2026-09-14, lit-3d, Europe PMC REST (`DOI:"10.1021/acs.jcim.9b00604"`,
  `resultType=core`), abstract field only.
- **schema_version**: `v3.2` (upgraded from `v3.2-abstract-only` on 2026-09-14 when the PDF was supplied)
- **confidence**: **high for every quoted string, and the caveat below is the reason to trust
  that rather than a reason to doubt it.** All blockquoted spans machine-verified against the
  PDF text layer (9/9). A second pass over **every** `"…"` span in the note — not just
  blockquoted ones, which is all `validate/quotecheck_plaintext.py` covers — found **four**
  affected by the artifact below; all four are now marked or de-quoted.

  **⚠ EXTRACTION ARTIFACT, and it is systematic for this PDF.** The paper is **two-column**, and
  `pdftotext -layout` **interleaves the columns**, so sentences spanning a column break do not
  exist as contiguous strings in any extraction. Equation (1), the training/validation sentence
  on p.3944, the TM3-motion sentence on p.3940 and the "surrogates for bound G-proteins" phrase
  on p.3942 are all split this way. **Anything read from this PDF's text layer must be checked
  for interleaving before it is quoted**, and reconstructions must be marked as such — I made
  three unmarked ones before catching it.

  One string — *"The five interhelix Cα-Cα distances…"* — is **not recoverable from the PDF at
  all** and is attributed to the publisher's abstract via Europe PMC, where it was originally
  taken.

- **unresolved**:
  1. ~~The five interhelix distances and thresholds.~~ **RESOLVED 2026-09-14 from our own
     pipeline implementation — see `state_metric`. Now a RELAY, not an unknown: the numbers
     should be checked against the PDF before any of them is printed in the manuscript, because
     a transposed coefficient would be invisible to every check available to us.**
  2. **Whether the Python script and web page are still obtainable** seven years on. Cheap to
     check and decides whether this is an adoptable instrument or only a citation.
  3. Training-set composition — which receptors, how many trajectories, how long.
  4. Which database supplied the experimental activation-state assignments for the 268.
  5. Whether the nanobody observation (quote 5) is quantified anywhere in the body.
  6. **The PDF.** Needs a library route; ACS is bot-walled and that was not circumvented.
- **why_it_matters**: *(user's call — left empty per SCHEMA)*
