# mazzoni2000gsctpeptide

> # ⚠ `abstract-only`. READ THIS BEFORE USING ANY FIELD BELOW.
>
> **Only the abstract was retrieved. The full text was NOT obtained, and it was not
> obtained for a reason that is worth recording so nobody re-treads it:** the paper is
> closed access (Unpaywall `oa_status: closed`; Semantic Scholar `openAccessPdf: CLOSED`;
> Europe PMC `fullTextXML` HTTP 404; no PMCID), and **every scripted route to the
> publisher returns a Cloudflare bot-detection interstitial (HTTP 403)**. Driving a
> browser past bot detection is not an acceptable retrieval method and was **deliberately
> not attempted**. This is a *library-access* problem, not a *checked-and-found-wanting*
> problem. **A future session must not read the gaps below as the paper being silent —
> they are this note being blind.**
>
> Every field that could not be established from the abstract says **`UNRESOLVED
> (abstract-only)`**, never `NOT ADDRESSED` and never `NONE`. The abstract itself is the
> publisher's own text via the Europe PMC REST API — it is not a relay or a paraphrase —
> and is preserved verbatim at `source/pending_text/mazzoni2000gsctpeptide.abstract.txt`
> (not in git). Precedent for this evidence class: `cheng2026af3cluster`.
>
> **Locators.** Every quote below is `[mazzoni2000gsctpeptide, Abstract]`. There are no
> page-level locators and there will be none until the PDF is obtained.

## ⚠ A RELAY CONTRADICTS THIS PAPER'S OWN ABSTRACT — added 2026-09-11, unresolved

A **2011 review** — `dursi2011signalpeptides` (PMC3268021, *J. Amino Acids* 2011:656051,
DOI 10.4061/2011/656051), whose **ref 77 is this paper, DOI and PMID matching exactly** —
enumerates the peptide panel that this abstract does not, and **disagrees with it**:

> "Short synthetic peptides corresponding to progressively longer segments of the Gαs
> C-terminus, **384–394, 382–394, 380–394, 378–394(C379A), 376–394(C379A), and
> 374–394(C379A), stimulate specific binding** of selective agonist CGS21680 to the
> Gs-coupled A2A-adenosine receptor in the rat striatal membranes both in the presence and
> in the absence of GTPγS"
>
> "The most effective peptides are 378–394(C379A), 376–394(C379A), and 374–394(C379A), and
> **the shortest peptide 384–394 is less active**"

**The panel is therefore 11, 13, 15, 17, 19 and 21 residues — a two-residue ladder.**

**The contradiction.** This paper's abstract says *"Shorter peptides … were **not
effective**."* The review says all six **stimulate binding** and the 11-mer is merely
**less active**. Those are different claims and **they cannot be adjudicated without the
PDF.** The likeliest reconciliation, which is a *reading* and not a finding: the abstract's
"not effective" sentence sits immediately after the adenylyl-cyclase sentence, so it may
attach to **signalling** rather than to **binding** — i.e. all six stimulate binding, but
only the long ones disrupt signal transduction. **If that is right, the paper is a graded
binding response with a functional threshold, not a single threshold.**

**Consequence, and it reverses advice given earlier in the day**: an 11-mer rung is
**NOT** safely predicted inactive. Whether R1 and R2 have knowable predicted signs is
**open**, and that is the honest state.

**Three further numbers the review attributes to this paper** — all **relay**, all to be
confirmed against the PDF, none to be cited as this paper:
- **"Peptide 374–394(C379A) inhibits agonist-stimulated AC activity by 35%** and does not
  have a significant effect on the basal and forskolin-stimulated activities." — the
  magnitude this note records as `UNRESOLVED`, still without a concentration.
- Helicity is **graded, and the 11-mer has one**: citing this paper *and* Albrizio et al.,
  *Biopolymers* 2000, 54(3):186–194, the review says the **11-mer 384–394 and the 21-mer
  374–394(C379A) both** "demonstrate a marked propensity to form α-helical structure", with
  384–394 having "the shortest α-helix between Arg389 and Leu394" and 374–394 "the longest
  α-helix spanning region from Asp381 to Leu394"; and that "the peptide containing **17 and
  more** amino acid residues have a stronger propensity to assume an α-helical
  conformation". **So "too short to be helical" is the wrong binary — it is "too short to
  form a long enough helix".**
- The α5 helix itself is defined from the Gsα crystal structure (Sunahara et al., *Science*
  1997) as **Asp368–Leu394, 27 residues**.

**Nothing above may be cited as `[mazzoni2000gsctpeptide]`.** It is
`[dursi2011signalpeptides]` reporting this paper, and on 2026-09-11 this project established
twice over that a review's account of a primary decays in transit. Text preserved at
`source/pending_text/dursi2011signalpeptides.RELAY.txt`.

## A. Identity

- **citekey**: `mazzoni2000gsctpeptide`
- **doi**: 10.1124/mol.58.1.226. PMID 10860945. No PMCID.
- **year, venue**: 2000, *Molecular Pharmacology* **58**(1), 226–236. Peer-reviewed.
- **title, authors**: "A Gαs carboxyl-terminal peptide prevents Gs activation by the A2A
  adenosine receptor." Mazzoni, M. R.; Taddei, S.; Giusti, L.; Rovero, P.; Galoppini, C.;
  D'Ursi, A.; Albrizio, S.; Triolo, A.; Novellino, E.; Greco, G.; Lucacchini, A.;
  **Hamm, H. E.**

> **WHY THIS PAPER IS IN THE CORPUS.** It is load-bearing for **two** separate things and
> was, until 2026-09-11, cited nowhere in this project. (1) It is the source of the
> **functional** half of the manuscript's title claim — the same 21-residue Gαs C-terminal
> peptide that shifts receptor geometry in `eddy2018extrinsictrp` **abolishes Gs
> signalling** here. (2) It is the **only wet-lab length series** of a Gα C-terminal
> peptide anywhere in the corpus, and it has a threshold at ≥17 residues. It reached us as
> reference 14 of `eddy2018extrinsictrp`. See
> `analysis_review/EDDY_PRIMARY_SOURCE.md`.

## B. Scope

- **system**: GPCR — **A2A adenosine receptor in RAT striatal membranes.** Native tissue
  membranes, not a purified or recombinant human construct. **The species matters**:
  `eddy2018extrinsictrp` uses **human** A2AAR, so any sentence joining the two crosses
  species. (`HANDOVER.md` standing rule: `_human` must never be a silent default.)
- **n_targets**: 1 receptor. Peptide arms: **at least 3 effective** — Gαs(374–394)C379A
  (**21-mer**), Gαs(376–394)C379A (**19-mer**), Gαs(378–394)C379A (**17-mer**) — plus an
  unstated number of shorter Gαs peptides and of Gαi1/2 C-terminal peptides, all reported
  ineffective. **`UNRESOLVED (abstract-only)`: the full peptide panel, its lengths and its
  sequences.**
- **method_class**: **other — experimental pharmacology**: radioligand binding
  ([3H]CGS21680 agonist; [3H]SCH58261 antagonist), adenylyl cyclase activity assay, and
  solution NMR **of the peptides**. **No predictor, no simulation of the receptor.**
- **backbones / templates / msa_handling**: `NOT APPLICABLE`.

## C. Conformational core

- **states_generated**: `NOT APPLICABLE` — nothing generated. **And note what is and is not
  measured**: the paper reports **receptor *affinity* states** inferred from competition-curve
  shape, and **peptide secondary structure** by NMR. **It never measures receptor geometry.**
  That is the single most important scope fact in this note.
- **structural_priors_used**: The peptide series is designed on the Gαs C-terminus, i.e. on
  prior knowledge of the receptor–Gα interface. All peptides carry a **C379A substitution**;
  **`UNRESOLVED (abstract-only)`: why, and whether an unsubstituted peptide was tested.**
  (Pattern worth noting: the nine deposited opsin α5 entries are *also* all mutants.)
- **oracle_leakage**: `NOT APPLICABLE` — no prediction pipeline.
- **prospective**: `NOT APPLICABLE`.
- **state_metric**: **Two, and neither is geometric.** (i) Competition-curve **slope and
  shift** for receptor affinity state, fitted with one- vs two-site models. (ii) Adenylyl
  cyclase activity for function. **No RMSD, no distance, no threshold, no predicate.**
- **metric_saturation**: `UNRESOLVED (abstract-only)` — no distributions or axis ranges are
  in the abstract.
- **directional_control**: **The handle is a supplied Gα C-terminal peptide, varied by
  LENGTH and by FAMILY.** This is the corpus's only wet-lab instance of both.
- **coinput_composition**: **v3.1.** Membranes + radioligand + peptide ± 100 µM GTPγS.
  **`UNRESOLVED (abstract-only)`: whether a peptide-only (no radioligand) condition exists,
  and the full arm list.**
- **binding_order**: **v3.1. Peptide added to membranes and read against agonist binding**;
  the design is a modulation assay, so it is **transducer-surrogate-modulates-ligand-binding**
  rather than a sequential-complex-formation study. `UNRESOLVED (abstract-only)` as to
  pre-incubation order and timing.
- **input_factor_design**: **v3.2.** **partner**: varied — by **length** (17/19/21 and
  shorter) and by **family** (Gαs vs Gαi1/2). **ligand**: present throughout as the
  radioligand; not varied as a factor. **nucleotide**: varied (± 100 µM GTPγS).
  `crossings:` **partner-length × nucleotide CROSSED at least partially** — "The Gαs peptides
  stimulated specific binding **both in the presence and absence** of 100 µM GTPγS" — but
  **partner × ligand HELD** (the agonist is the readout, never removed or varied as a
  condition). Do **not** tag `factors-crossed`: the crossed pair is nucleotide, not a
  co-input, and the balance is `UNRESOLVED (abstract-only)`.
- **anti_memorization_design / _control**: `NOT APPLICABLE`.
- **controls_run**:

  | control | what it rules out | locator |
  |---|---|---|
  | **Shorter Gαs C-terminal peptides** | that any Gαs-derived peptide works — a **length** control, and it is negative: "Shorter peptides from Gαs … were not effective" | Abstract |
  | **Gαi1/2 C-terminal peptides** | that any Gα C-terminus works — a **family-specificity** control on a Gs-coupled receptor, also negative | Abstract |
  | **Basal adenylyl cyclase activity** | that the peptide inhibits the enzyme rather than the receptor–Gs step — unaffected | Abstract |
  | **Forskolin-stimulated adenylyl cyclase activity** | that the peptide acts downstream of the receptor — unaffected | Abstract |
  | **± 100 µM GTPγS** | that the effect requires the nucleotide-free state | Abstract |
  | **Antagonist radioligand ([3H]SCH58261) competition alongside agonist binding** | that the effect is an agonist-specific artefact | Abstract |
  | **NMR of the peptide in solution** | that length acts through mass rather than conformation — supports a **helicity** mechanism | Abstract |
  | **`UNRESOLVED (abstract-only)`: scrambled / reversed / composition-matched peptide** | sequence specificity at fixed length. **The abstract does not say whether one was run. Do not record this as absent.** | — |

- **confidence_as_discriminator**: `NOT APPLICABLE`.

## D. Claims

- **central_conclusion**: Synthetic peptides spanning the Gαs carboxyl terminus modulate
  agonist binding to rat A2A adenosine receptors and block receptor-stimulated adenylyl
  cyclase activity. Activity requires **sufficient length** — the 17-, 19- and 21-residue
  peptides work and shorter ones do not — and the authors attribute the requirement to the
  peptide's ability to adopt a **compact C-terminal α-helix**, measured by NMR in solution.

- **THE QUOTES THIS NOTE EXISTS FOR** (all verbatim, `[mazzoni2000gsctpeptide, Abstract]`):
  1. > "Three peptides, Galpha(s)(378-394)C(379)A, Galpha(s)(376-394)C(379)A, and
     > Galpha(s)(374-394)C(379)A, were the most effective."
  2. > "Shorter peptides from Galpha(s) and Galpha(i1/2) carboxyl termini were not effective."
  3. > "This same Galpha(s) peptide was also able to disrupt G(s)-coupled signal transduction
     > as indicated by inhibition of the A(2A) receptor-stimulated adenylyl cyclase activity
     > without affecting either basal or forskolin-stimulated enzymatic activity in the same
     > membrane preparations."
  4. > "However, the peptide did not stabilize the high-affinity state of the A(2A) adenosine
     > receptor for [(3)H]CGS21680."
  5. > "In the presence of GTPgammaS, the displacement curve was right-shifted, whereas the
     > addition of Galpha(s)(374-394)C(379)A caused a partial left-shift. Both curves were
     > fitted by one-site models."
  6. > "NMR spectroscopy showed the strong propensity of peptide Galpha(s)(374-394)C(379)A to
     > assume a compact carboxyl-terminal alpha-helical conformation in solution."
  7. > "Overall, our results point out the conformation requirement of Galpha(s)
     > carboxyl-terminal peptides to modulate agonist binding to rat A(2A) adenosine receptors
     > and disrupt signal transduction."

- **necessity_claims**: quote 7 is the paper's own necessity statement — a **"conformation
  requirement"**. Quote 2 is a negative-result necessity claim about length. No
  impossibility claim about other methods appears in the abstract; **`UNRESOLVED
  (abstract-only)` for the body.**
- **novelty_claims**: **`UNRESOLVED (abstract-only)`.** No "first"/"novel" string appears in
  the abstract, but a 2000 abstract is not where one would be.
- **stated_limits**: **`UNRESOLVED (abstract-only)`.**
- **stance**: **background + threat.** Background because it supplies the biology under our
  title's number. **Threat** because the *same peptide that produces the active geometry in
  `eddy2018extrinsictrp` abolishes signalling here.** Any sentence of the form "a 21-residue
  α5-CT peptide drives the receptor into the active state" must be written so it cannot be
  read as a functional claim. See also: it "**did not stabilize the high-affinity state**"
  and both competition curves fit **one site**, so it does **not** reconstitute the textbook
  ternary complex either.

## E. Quantitative comparators

| quantity | value | units | scope | locator |
|---|---|---|---|---|
| Effective peptide lengths | **21, 19, 17** (Gαs 374–394, 376–394, 378–394, all C379A) | residues | "the most effective" | Abstract |
| Ineffective peptides | shorter Gαs; Gαi1/2 C-termini | — | length and family controls | Abstract |
| GTPγS concentration | **100** | µM | binding assays | Abstract |
| Competition-curve fit | **one-site**, both ± peptide | — | [3H]SCH58261 vs NECA | Abstract |
| **Peptide concentration / EC50 / IC50** | **`UNRESOLVED (abstract-only)`** | — | **the dose question — nothing may assume the binding and cyclase effects occur at comparable doses** | — |
| Magnitude of binding stimulation | **`UNRESOLVED (abstract-only)`** | — | "dose-dependent" is all the abstract gives | — |
| Magnitude of cyclase inhibition | **`UNRESOLVED (abstract-only)`** | — | — | — |
| n / replicates | **`UNRESOLVED (abstract-only)`** | — | — | — |

- **n_predictions**: `NOT APPLICABLE`.
- **comparable_to_ours**: **Directly, and in two ways.** (i) It fixes the **wet-lab length
  threshold** our in-silico ladder should be pre-registered against: ≥17 active, shorter
  inactive, so an 11-mer rung is predicted **negative** and a 15-mer rung sits in the
  transition. (ii) It supplies the **functional** counterweight to `eddy2018extrinsictrp`'s
  structural result. **What it cannot do**: it never measures receptor geometry, so it does
  not contradict the structural claim — the two papers measure different observables, on
  different species.
- **si_in_scope**: **`UNRESOLVED (abstract-only)`** — whether the paper has supplementary
  material is unknown.

## F. Figures

**`UNRESOLVED (abstract-only)` — no figure could be seen or counted.** The abstract implies
at least a dose–response, competition curves, a cyclase bar/series and peptide NMR spectra,
but **nothing here may be used for figure-design queries.** Excluded from
`figure-exemplar`-style lookups by construction.

## G. Provenance

- **extracted_on, by**: 2026-09-11, lit-3d, from the Europe PMC REST API
  (`search?query=EXT_ID:10860945&resultType=core`), abstract field only.
- **schema_version**: `v3.2-abstract-only`
- **confidence**: **high for the seven quoted strings** — all 7 machine-verified against the
  retrieved abstract by `validate/quotecheck_plaintext.py` (7/7, self-tested both
  directions). **Nil for everything the abstract does not state**, which is most of sections
  C, E and all of F, and is marked `UNRESOLVED (abstract-only)` throughout rather than left
  blank.
- **unresolved**:
  1. **The peptide concentration for the cyclase effect, and whether the binding and
     signalling effects occur at comparable doses.** Highest priority. (A relay gives the
     *magnitude* as 35% inhibition; the *concentration* is still unknown.) Blocks any sentence
     that treats the two as a single phenomenon.
  2. **Whether a full-length (21-residue) Gαi C-terminal peptide was tested**, or only
     shorter Gαi ones. The abstract bundles "shorter" with "Gαi1/2" and the distinction
     decides whether this is a clean family-specificity control or only a suggestive one —
     which in turn decides whether E1.4 has a positive wet-lab prediction.
  3. **Whether "not effective" attaches to BINDING or to SIGNALLING.** A relay says all
     six peptides stimulate binding and the 11-mer is only "less active", which contradicts
     this abstract's "not effective" if read as binding. **This is now the single most
     decision-relevant unresolved item**, because it decides whether a short rung is
     predicted inactive or merely weaker. See the banner above.
  4. **Why C379A**, and whether an unsubstituted peptide was tested.
  5. **Whether any scrambled / reversed / composition-matched control peptide was run.**
  6. **All figures, all numbers beyond those in §E, all stated limits, all novelty claims.**
  7. **The PDF itself.** Needs a library route; see the banner at the top of this note.
- **why_it_matters**: *(user's call — left empty per SCHEMA)*
