# Three verifications: apo-only MSA controls, the F-16 retraction, and graded length response

lit-3d, 2026-09-12, for paper-6f. Retrieval only. Corpus 83/83/87, staleness clean.

**Summary. Q1: the transfer question is unanswered, but my earlier flat "zero papers" needs a
refinement — one paper has the design and did not ask the question. Q2: the F-16 retraction is
CONFIRMED and I can now strengthen it with two pieces of evidence I did not have before; it was
not an over-correction. Q3: yes — the corpus's own mechanism statement is explicitly graded, and
it predicts the smooth curve your ladder is built to resolve.**

---

## Q1 — Does an apo-only MSA control bound the complex case? **No, and nobody has tested it**

**Refinement to my earlier answer, which said zero papers.** That was right about the *result*
and slightly too strong about the *design*. One paper applies the same MSA manipulation to the
same receptor **both alone and in complex**:

**`mitjavila2026afsample2t`.** Its state toggle *is* the partner — *"**The inactive receptor
state was predicted using only the receptor sequence**"* (active = + Gα/Gβ/Gγ) — and masking is
applied in both conditions at every level: *"For each masking probability, 250 structures were
generated, **with equal numbers of active and inactive receptors**"*. Per target: 1,000 AF2 +
1,000 AFsample2T models, "250 each at 0%, 10%, 20%, 30% masking, **with equal numbers of active
and inactive within each level**" = 2,000 models per receptor.

**But it cannot answer the transfer question, for three reasons, and it never asks it:**

1. **The state label is assigned by the input, not read off the result** — *"The active/inactive
   label is assigned to the *input condition* a priori, not read off the result."* So masking is
   never asked whether it changes state; the partner sets the state by construction.
2. **The only conformational-state check is four receptors in unheld SI** — *"comparison of the
   AF2 models with experimentally determined structures of active and inactive states of **four
   receptors** confirmed that this approach reliably captures the characteristic conformations of
   TM6 (**Table S1**)"* — and Table S1 is **not held**.
3. **The readout is binding-site side-chain RMSD**, and the note records that masking produces
   *"**local side-chain and backbone heterogeneity in the pocket, not alternative global
   states**"*, directable *"in site, not in state"*.

**Nothing in the paper compares the masking response with-partner against without-partner.** The
two cells are pooled into one ensemble for a docking application, not contrasted.

**Everything else searched, and absent:**

- **No paper states that monomer MSA behaviour predicts complex behaviour.** A sweep for
  transfer language ("alone and in complex", "monomer and multimer", "generalise/generalize",
  "does not extend") near MSA/subsampling/masking terms returns **8 hits across 83 notes, and
  all 8 are about *sequence-cluster* generalisation** (training-set homology in
  `krishna2024rfaa`, `wohlwend2024boltz1`, `waymentsteele2025reply`, `lewis2025bioemu`) — **none
  is about the monomer→complex boundary.**
- **No paper explicitly declines to generalise across that boundary either.** The boundary is not
  discussed as a boundary anywhere in the corpus.
- **And note the one GPCR state-readout test is itself apo-side.** `ye2026multistatebias`'s
  AF-Cluster/U10/U100 arm runs on **AlphaFold2** (not Multimer) — *"AlphaFold2 … as the engine
  inside the AF-Cluster / U10 / U100 baseline arm"* — which takes a single chain, so that arm is
  necessarily receptor-alone. **Flagged as a structural inference, not a quoted statement**: the
  note does not state the arm's input composition explicitly.

**So the honest position is exactly the one you proposed.** An apo-only MSA control defeats the
rival explanation *as stated* — "you starved it of data" is a claim about the receptor-alone
input, and an apo control addresses it directly. **It does not bound what MSA manipulation would
do with a partner present, and no paper in 83 has measured that.** The one paper with the design
to measure it read out pocket geometry instead, with its state labels fixed by input.

## Q2 — the F-16 retraction: **CONFIRMED, and it was not an over-correction**

### Half one: the Mazzoni ≥17 threshold is contested. **Confirmed, and now with a stronger internal argument.**

I re-read the abstract sentence by sentence from the preserved publisher text
(`source/pending_text/mazzoni2000gsctpeptide.abstract.txt`). **Two things I did not have before:**

**(a) The sentence order supports the reading.** The clause you are relying on is the *tenth*
sentence, and the *ninth* is the adenylyl-cyclase sentence:

> [9] "This same Gαs peptide was also able to **disrupt Gs-coupled signal transduction** as
> indicated by inhibition of the A2A receptor-stimulated adenylyl cyclase activity without
> affecting either basal or forskolin-stimulated enzymatic activity in the same membrane
> preparations."
> [10] "**Shorter peptides** from Gαs and Gαi1/2 carboxyl termini **were not effective**."

So "not effective" sits immediately after a signalling claim, with no intervening binding
sentence.

**(b) The abstract is internally consistent with the graded reading, independently of the
review.** Sentence [2] is general and plural — *"**The Gαs peptides stimulated specific binding**
both in the presence and absence of 100 µM GTPγS"* — and sentence [3] is a **comparative**:
*"Three peptides … were the **most effective**."* "Most effective" presupposes a field in which
the others were effective to some degree. **The abstract therefore does not assert a threshold;
it asserts a ranking.** That is an argument from the primary's own text, not from the relay.

**The residual ambiguity is real and I am not claiming it is settled.** [10] can still be read as
"not effective at anything", and it bundles the length control with the Gαi1/2 family control,
which makes a single scope harder to pin. **Unresolvable without the PDF**, which is closed
access and bot-walled.

### Half two: the 2011 review's six-peptide panel. **Confirmed verbatim, and it transcribed the panel accurately.**

From `source/pending_text/dursi2011signalpeptides.RELAY.txt` (PMC3268021, its ref 77 = Mazzoni,
DOI and PMID matching):

> "Short synthetic peptides corresponding to progressively longer segments of the Gαs C-terminus,
> **384–394, 382–394, 380–394, 378–394(C379A), 376–394(C379A), and 374–394(C379A), stimulate
> specific binding** of selective agonist CGS21680 to the Gs-coupled A2A-adenosine receptor in
> the rat striatal membranes both in the presence and in the absence of GTPγS (**Table 1**)."
>
> "The most effective peptides are 378–394(C379A), 376–394(C379A), and 374–394(C379A), and **the
> shortest peptide 384–394 is less active** [77]."

**Those are 11, 13, 15, 17, 19, 21 residues**, and **all six are said to stimulate binding**,
with the 11-mer **less active** rather than inactive.

**A consistency check that materially raises confidence in this relay, which I did not have
before.** The `(C379A)` substitution is annotated on **exactly** the three peptides that contain
residue 379 — 378–394, 376–394, 374–394 — and **not** on 384–394, 382–394 or 380–394, which all
begin after 379. **A garbled transcription would not reproduce that pattern.** Given today's
georgiou episode, I checked this deliberately.

### Half three: AF3's 16 governs set construction, not inference. **Confirmed from the note.**

`abramson2024af3`, Methods (printed p.502): *"Individual peptide chains (protein chains with less
than 16 residues) are **always filtered out**"* — in the **low-homology evaluation subset**. And
peptides are **included** elsewhere, p497: *"Our confidence analysis is performed on the recent
PDB evaluation set, **with no homology filtering and including peptides**."* Chai-1's boundary is
**9 residues and it keeps them** (clustered at 100% identity rather than 40%, §5.6 p11);
Boltz-2 has no peptide/protein taxonomy line (only a "fewer than 4 resolved residues" curation
filter); Protenix inherits AF3's set by reference. **I cannot corroborate the OpenFold3 claim —
that is `paper_af3`'s package grep, not a corpus finding, and the corpus holds no OpenFold3
paper at all.** Attribute it to them.

**Verdict: F-16 stands. Both halves confirmed, neither over-corrected, and the standing
instruction — do not build a 16-mer rung to resolve a taxonomy boundary — is correct on the
evidence. Repeat it.**

## Q3 — Does the helicity mechanism predict a graded curve? **Yes, explicitly**

The mechanism statement in the corpus is **graded in its own wording**, not a threshold. From the
same 2011 review passage, attributing to Mazzoni [77] and Albrizio et al. *Biopolymers* 2000,
54(3):186–194 [153]:

> "Thus, the peptide containing **17 and more amino acid residues have a stronger propensity to
> assume an α-helical conformation compared with the shortest peptides**."

> "The NMR analysis of **11-mer 384–394 and 21-mer 374–394(C379A)** peptides … showed that **both
> peptides demonstrate a marked propensity to form α-helical structure** in
> hexafluoroacetone/water … peptide **384–394 having the shortest α-helix between Arg389 and
> Leu394**, and peptide **374–394(C379A), the longest α-helix spanning region from Asp381 to
> Leu394** [77, 153]."

**So: both ends of the ladder form a helix; they differ in helix *length*; and the propensity is
"stronger", not present-versus-absent.** The predicted observable is **helix length increasing
with peptide length**, which is a continuous covariate — so a **smooth, monotone-in-length
response is the shape the mechanism predicts**, and a sharp step at any particular residue count
is what would be surprising.

**One structural anchor that bounds the top of the ladder.** The same passage gives the α5 helix
from the Gsα crystal structure (Sunahara et al., *Science* 1997 [152]): *"the α5-helix responsible
for effective interaction with the receptors involves the region from **Asp368 to Leu394**"* —
**27 residues**. So a length ladder has a principled ceiling at 27, beyond which you are no longer
adding α5.

**Caveat on all of Q3: this is the relay, not the primary.** The helicity data is the review's
account of Mazzoni [77] plus Albrizio [153]; **neither primary is held.** The graded claim is
well-sourced within the review and internally consistent, but it should be cited as
`[dursi2011signalpeptides]` reporting them, never as Mazzoni directly.

---

## Negatives, for direct use

1. **No paper reports whether an MSA manipulation's effect differs between a protein alone and the same protein in a complex.** One paper (`mitjavila2026afsample2t`) has both cells and does not contrast them.
2. **No paper states that monomer MSA behaviour predicts complex behaviour**, and none explicitly declines to generalise either — the boundary is never discussed.
3. **No paper reports a cross-chain MSA effect or an interface effect of subsampling** (unchanged from the earlier answer).
4. **The OpenFold3 inference claim is not corroborable from the corpus** — no OpenFold3 paper is held.
5. **Mazzoni's "not effective" scope remains unresolvable without the PDF** (closed access, bot-walled).
