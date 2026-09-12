# The primary source under "21 residues" — retrieved, and it is not the paper we were told

lit-3d, 2026-09-11, for paper-6f. Full texts preserved in `lit/source/pending_text/`
(not in git; re-fetch instructions in its `README_eddy.md`).

## Headline

**The relay was broken, and chasing it was right.** `georgiou2025heterogeneity` attributes
the 21-residue result to *"Eddy and collaborators in 2021"*, its **ref 155** —
Eddy, Martin & Wüthrich, *Structure* 2021, 29(2):170–176.e3, DOI `10.1016/j.str.2020.11.005`.
**That paper does not contain the result.** I retrieved its complete full text
(PMC7867584, NCBI efetch — Introduction through STAR Methods, 25,799 characters of body)
and counted:

| string | occurrences in the whole body |
|---|---|
| `Gs` | **0** |
| `Gα` / `Galpha` | **0** |
| `mini-G` / `miniG` / `mini G` | **0** |
| `21-residue` / `21 residue` | **0** |
| `6.35`, `5.62`, `7.55` | **0, 0, 0** |
| `W246`, `6.48` | 7, 34 |

Its construct is *"human A2AAR (1-316) containing a point mutation to remove the only
glycosylation site N154Q, an N-terminal FLAG tag, and a 10 X C-terminal His tag"* — no G
protein, no peptide, anywhere. It is about the W246^6.48 toggle switch and partial agonism.

**The real source is three years earlier and in a different journal:**

> **Eddy, M. T.; Gao, Z.-G.; Mannes, P.; Patel, N.; Jacobson, K. A.; Katritch, V.;
> Stevens, R. C.; Wüthrich, K.** "Extrinsic Tryptophans as NMR Probes of Allosteric
> Coupling in Membrane Proteins: Application to the A2A Adenosine Receptor."
> *J. Am. Chem. Soc.* **2018**, 140(26), 8228–8235. DOI `10.1021/jacs.8b03805`.
> PMID 29874058, PMC6192543.

So georgiou is wrong on the **year** and on the **reference**; "Eddy and collaborators" is
the only part that survives. Cite the JACS paper directly and never the review for this.

---

## Your four questions, answered from the primary

### 1. Is it genuinely 21 residues, and genuinely the Gαs C-terminus? **Yes, and the range is stated.**

> "we added a **10-fold molar excess of a 21-residue synthetic polypeptide corresponding
> to residues 374–394 of the carboxy terminus of the intracellular partner protein GαS**."

Human GNAS long isoform is 394 residues, so **374–394 is exactly the last 21**. That is the
construct our title's number refers to, and it now has a residue range rather than a number.

### 2. Is the W233^6.35 collapse Eddy's own observation, and at what concentration? **Yes. 10-fold molar excess.**

The primary's own data, and it is **richer and more careful than the review's version**:

> "**A single indole 15N–1H signal was observed for W233 in the ternary complex with
> UK432097 and the polypeptide, in contrast to the two signals observed for W233 in complex
> with UK432097 alone.** The chemical shift of the single resonance for W233 was slightly
> shifted in both the 1H and 15N dimensions, by **~0.06 and ~0.2 ppm**, respectively,
> **from either of the two resonances observed in the absence of the polypeptide**."

That last clause is important and georgiou drops it: the surviving peak is **not** simply
one of the two pre-existing populations. It sits slightly off both. So "the peptide selects
the active conformer" is one reading; fast exchange between the two on peptide binding is
another, and the paper does not adjudicate.

The intracellular/extracellular asymmetry is quantified, not asserted:

> "**W29 and W32, located in helix I at the intracellular surface**, both show chemical
> shift changes … of **~0.15 ppm in the 1H dimension and ~0.4 ppm in the 15N dimension**.
> In contrast, **W143 and W268, located near the A2AAR extracellular surface, show at most
> a very small response** to the addition of the polypeptide."

### 3. Is there a length series? **No. 21 is the only length tried.**

I swept the whole body for `\d{1,3}[- ]?(residue|mer|aa)`. Two hits only: the **21**-residue
Gαs peptide (twice), and the **86**-residue αMF secretion signal, which is a construct
artefact of the *Pichia* expression system and unrelated.

**So our ladder would be the first titration of a biological co-input's length, and the
wet-lab literature offers one point on it, not a curve.** With `tran2026nanogs`'s stapled
15-mers and the nine opsin 11-mers, the literature has three lengths across three
receptors, three partners and three assays — which is not a series, and cannot be read as
one.

### 4. A2AR only, or more? **A2AR only.** No other receptor is studied (`β2`, `β1AR` appear only as literature contrast; `rhodopsin` once, in passing).

---

## Three things that came out of it that you did not ask for

### A. "Mini-G" is **georgiou's** conflation. The primary literature is clean.

The primary calls the 21-mer *"the polypeptide derived from the GαS carboxy terminus"*
throughout, and in the same Discussion paragraph reserves the other term, in scare quotes,
for the protein:

> "the data in Figure 4 appear to be consistent with recent crystallographic studies of
> A2AAR binary and ternary complexes involving an agonist and an **engineered "mini GαS"
> protein**, where changes of A2AAR in the ternary complex relative to the complex with
> agonist alone were observed in the intracellular region but not in the extracellular
> region."

`mini-G` occurs **0 times** in the JACS body as a name for the 21-mer. So the factor-of-ten
ambiguity I flagged last round is an artefact of the review, not of the field. **The "last
N residues" rule still holds — but the reason changes**: it is not that the literature is
ambiguous, it is that this review is, and we should not propagate its label.

### B. The number's own source says the peptide **blocks signalling**. This is the finding that matters most.

Immediately after introducing the peptide, the primary reports, citing Mazzoni et al.,
*Mol. Pharmacol.* 2000, 58:226–236 (its ref 14):

> "An earlier study reported an **increase of the specific binding of A2AAR agonists** upon
> addition of this polypeptide **and inability of A2AAR to signal through Gαs after
> addition of the polypeptide**, suggesting that the polypeptide and full length GαS
> protein bind at similar locations in A2AAR."

So the 21-mer occupies the Gαs site, **enhances agonist affinity**, and **abolishes
downstream signalling**. It is a competitive occupant, not an activator.

**Consequence for the title, and it is a real one.** *"A 21-residue α5 C-terminal peptide
drives the receptor into the active state"* is supportable as a **structural** claim — that
is exactly what the W233^6.35 data show. As a **functional** claim it is contradicted by
the very literature the number comes from. Our predicate measures geometry, so the
structural reading is the one we can defend, but the sentence has to be written so it
cannot be read the other way. A referee who knows Mazzoni 2000 will test that sentence.

This does not weaken the experiment. It arguably strengthens the framing: a co-input that
produces the active *geometry* while abolishing *signalling* is precisely the case where a
structure predictor's output and biological meaning come apart — which is the paper's
broader point about confidence and correctness.

### C. Partner type changes **where** in the receptor the effect appears.

> "This is in apparent contrast with NMR studies of the β1-adrenergic receptor (β1AR),
> which reported changes in the chemical shifts of amide signals of valine residues
> **located near the extracellular surface** upon complex formation with a
> **G-protein-mimicking nanobody**."

A nanobody perturbs β1AR extracellularly; the 21-mer perturbs A2AR intracellularly only.
Two different partner types, two different spatial footprints. That bears directly on
E1.1's premise — short rungs may act more locally than long ones, which is a *predicted*
length effect independent of whether the state flips — and on how our nanobody arms should
be compared with our Gα arms. It should be a stated expectation of the ladder, not a
surprise in the results.

---

## What I did not resolve

- **Mazzoni et al. 2000** (Mol. Pharmacol. 58:226–236, PMID 10860945,
  DOI `10.1124/mol.58.1.226`) is now the load-bearing citation for the functional half and
  I have **not** retrieved it. Everything in §B above is the JACS paper's characterisation
  of it — a relay again, and it should be closed before that sentence is written.
- **Neither paper is extracted to SCHEMA v3.2.** `eddy2018extrinsictrp` should be: it is
  the primary evidence under the manuscript's own number, and it is currently reachable
  only through this file.
- `georgiou2025heterogeneity`'s note carries the bad attribution twice (its
  `directional_control` and `g-protein-mimetic` fields, both reading "p.10"). **The note
  needs a `corrections:` line**; I have not edited it in this pass.

---

# Mazzoni 2000, retrieved 2026-09-11 — and it corrects something I told you

> Mazzoni, M. R.; Taddei, S.; Giusti, L.; Rovero, P.; Galoppini, C.; D'Ursi, A.; Albrizio,
> S.; Triolo, A.; Novellino, E.; Greco, G.; Lucacchini, A.; **Hamm, H. E.**
> "A Gαs carboxyl-terminal peptide prevents Gs activation by the A2A adenosine receptor."
> *Mol. Pharmacol.* **2000**, 58(1), 226–236. DOI `10.1124/mol.58.1.226`, PMID 10860945.

**Evidence class: `abstract-only`.** The paper is closed access with no OA copy anywhere
(Unpaywall `oa_status: closed`; Semantic Scholar `openAccessPdf: CLOSED`; Europe PMC
`fullTextXML` 404), and every scripted route to the publisher returns a Cloudflare
interstitial (403). The abstract below is the **publisher's own**, retrieved from Europe
PMC — it is not a relay — but it is an abstract, and everything here inherits that limit.
Treat it the way `cheng2026af3cluster` is treated: verified at abstract level, body detail
UNVERIFIED. Getting the PDF needs a library route, not a script.

## **CORRECTION to what I told you last round**

I wrote: *"21 is the only length tried … So our ladder is the first titration of a
biological co-input's length."* **That is true of Eddy and false of the literature.**
Mazzoni ran a length series, at our rungs, and found a threshold:

> "Three peptides, **Gαs(378–394)C379A, Gαs(376–394)C379A, and Gαs(374–394)C379A**, were
> the most effective. … **Shorter peptides from Gαs and Gαi1/2 carboxyl termini were not
> effective.**"

Those are **17, 19 and 21 residues**. So the wet-lab picture is: **≥17 works, shorter does
not**, on rat A2AR by agonist binding and adenylyl cyclase.

**What that does to E1.1.** Our proposed rungs are 11, 15, 21, 26, 36. Mazzoni predicts
**R1 (11-mer) is inactive** and puts the transition between 11 and 17, which is exactly
where our 15-mer rung sits. That is a **pre-registrable prediction** — state it before the
ladder runs, and the ladder becomes a test of whether a co-folding model reproduces a
25-year-old wet-lab threshold rather than an open-ended scan. It also means the ladder is
**not** the first titration; it is the first *in silico* titration, and the honest framing
is "does the model reproduce the known threshold", which is a stronger paper.

## Your four questions

**(1) Direct measurement or inference, and by what assay? — DIRECT, with two internal
controls.**

> "This same Gαs peptide was also able to disrupt Gs-coupled signal transduction as
> indicated by **inhibition of the A2A receptor-stimulated adenylyl cyclase activity
> without affecting either basal or forskolin-stimulated enzymatic activity in the same
> membrane preparations**."

Adenylyl cyclase activity in rat striatal membranes. The two negative controls — basal and
forskolin-stimulated activity both unaffected — make it a specificity claim about the
receptor–Gs step, not a general inhibition. This is a well-controlled direct measurement.

**(2) Comparable concentrations, and how do they compare with Eddy's 10-fold molar excess?
— UNRESOLVED. This is the one I cannot close from the abstract.**

The abstract gives the GTPγS concentration (100 µM) and says the binding effect was
"dose-dependent", but **no peptide concentration, EC50 or IC50 appears**, and no statement
that the two effects were measured at comparable doses. **Do not write a sentence that
depends on the two effects being at the same dose.** Closing it needs the PDF.

**(3) Does it say anything about receptor conformation? — It measures receptor *affinity
states*, not receptor geometry. Its NMR is on the *peptide*, not the receptor. Your
inference is correct.**

On the receptor, all three statements are binding-level:

> "the addition of the Gαs peptide **modified the slope of the NECA competition curve,
> suggesting modulation of receptor affinity states**" … "In the presence of GTPγS, the
> displacement curve was right-shifted, whereas the addition of Gαs(374–394)C379A caused a
> partial left-shift. **Both curves were fitted by one-site models**."

And the NMR is of the peptide in solution:

> "**NMR spectroscopy showed the strong propensity of peptide Gαs(374–394)C379A to assume a
> compact carboxyl-terminal α-helical conformation in solution.**"

**So the structural and the functional claims sit on different observables, in different
papers, on different species, and neither directly contradicts the other.** Eddy measures
receptor geometry at W233^6.35 on **human** A2AR; Mazzoni measures agonist binding and
cyclase output on **rat** striatal A2AR. That is the honest statement and it is more
defensible than either "the peptide activates" or "the peptide blocks".

**One complication that must not be smoothed.** Mazzoni reports the peptide *raised*
specific agonist binding but **"did not stabilize the high-affinity state of the A2A
adenosine receptor for [3H]CGS21680"** — the classic ternary-complex signature is
**absent**, and the competition curves fit one site, not two. So whatever the peptide does
to binding, it is not the textbook G-protein-coupled high-affinity state. A sentence
implying the 21-mer reconstitutes the ternary complex would be wrong on this paper's own
evidence.

**(4) A2AR only? — Yes, and it is RAT.** "rat striatal membranes". Eddy is human A2AR.
Given `HANDOVER.md`'s standing rule that `_human` must never be a silent default, the
species difference belongs in any sentence that puts the two papers together.

## Two things you did not ask for

**A. Mazzoni is a family-specificity control, and it is relevant to E1.4.** "Shorter
peptides from Gαs **and Gαi1/2** carboxyl termini were not effective." The Gαi1/2
C-terminal peptides did not work on A2AR — a Gs-coupled receptor. That is wet-lab
precedent for partner-family specificity at peptide length, which is exactly what E1.4
asks of the models. Caveat: the sentence bundles "shorter" with "Gαi1/2", so it cannot be
determined from the abstract whether a **full-length 21-mer Gαi C-terminus** was tested.
That distinction decides whether E1.4 has a positive wet-lab prediction or only a
suggestive one — **add it to the PDF-retrieval list**.

**B. Helicity is now the literature's stated mechanism twice, 25 years apart.** Mazzoni's
own conclusion:

> "Overall, our results point out the **conformation requirement** of Gαs carboxyl-terminal
> peptides to modulate agonist binding to rat A2A adenosine receptors and disrupt signal
> transduction."

with the α-helical propensity measured by NMR as the supporting datum. `tran2026nanogs`
reaches the same conclusion by a different route — the unstapled linear peptide does
nothing, the stapled one works. **Two independent wet-lab papers, two decades apart,
different receptors, different partners, different assays, same mechanism.** The
per-row helicity requirement in the Group 1 spec is no longer a precaution; it is the
literature's own explanation for why short peptides fail, and it gives the ladder a
mechanistic hypothesis to test rather than a confound to exclude: **the length threshold
may simply be the helix-formation threshold.**

## Retrieval list, in priority order

1. **Mazzoni PDF** — the peptide concentration for the cyclase effect (question 2), and
   whether a 21-residue Gαi C-terminus was tested (item A). Needs library access.
2. Whether the C379A substitution changes anything — the construct is **not wild-type**,
   the same pattern as the nine opsin 11-mers, and it is unremarked in the abstract.
