# How the corpus treats agonist-bound, transducer-free structures

lit-3d, 2026-09-11, for paper-6f / Aditya. Locators are PDF pages unless marked;
`georgiou2025heterogeneity` is offset **+3690**, so its PDF p.7 is printed **p.3697** and
p.13 is printed **p.3703**.

**Short answer.** Two corpus papers state a rule and they differ. One paper reports the
geometry directly and says agonist-only structures are **bimodal**. And there is a
published, pre-registrable exclusion rule that is **not** derived from our thesis, so the
circularity you are worried about is avoidable. **You do not have to choose between
"calibrate with them in" and "exclude them because they are inconvenient".**

---

## 1. Does any corpus paper state a rule?

**Yes — `khaleq2026hyaline`, and its rule is conditional, which is the interesting part.**
Verbatim, p12:

> "Active structures included: (1) G protein-coupled or G protein-mimetic nanobody-bound
> structures; (2) arrestin-coupled structures; (3) **full agonist-bound structures with
> conformational criteria indicating activation**. Inactive structures included: (1) apo
> structures; (2) antagonist-bound structures; (3) inverse agonist-bound structures."

So agonist-only complexes **are** admitted to the active class — but only *"with
conformational criteria indicating activation"*. It is a two-part rule: pharmacology **and**
geometry must agree. That is the shape of rule you want. **Two caveats before adopting it.**
The "conformational criteria" are never specified in the paper, so the rule is not
reimplementable as written; and the note records that the ultimate ground truth is still
GPCRdb — "A structure was only retained if it had unambiguous activation state annotation in
GPCRdb" (p12), and "**a classifier trained on GPCRdb state labels reproduces GPCRdb's
operational definition of 'active'**". So khaleq inherits the same annotation you are
worried about, with a geometric filter bolted on.

**`paajanen2026activation` sidesteps the labelling question exactly as you guessed, and how
it does so is the useful part.** Its anchor classes are **"structures bound to both G
protein and agonist"** (active pole) and **"G protein-free and antagonist-bound"** (inactive
pole, N = 248), and the threshold is the GMM boundary between those two (p.4, p.11).
**Agonist-only structures are in neither anchor class.** The index is fitted unsupervised,
the labels enter only to orient it — so paajanen **calibrates on the unambiguous poles and
then reports where everything else falls**. That is a published convention and it is the one
I would copy.

## 2. Does anyone report the intermediate class separately?

**Three different treatments exist in the corpus, and all three are citable.**

- **Graded, as a continuous axis.** `chib2025gpcrstates` takes GPCRdb's **activity level
  0–100% per structure** and uses it as the **x-axis of Figure 2a–d** rather than
  binarising: "The activity level associated with each GPCR structure is obtained from the
  GPCRdb database" (p6), and TM3–TM6 distance "is highly correlated with the activity level
  of GPCRs" (p6). This is the corpus's precedent for *not* forcing a binary.
- **Filtered at the extreme.** `lee2026confornets` p15: "We selected GPCRs with both **fully
  active (100% activation degree)** and inactive structures available." A hard threshold on
  the same independent annotation.
- **Dropped, with the reason stated.** `paajanen2026activation` p.2: "Structures reported as
  'intermediate' or 'other' have been ignored **because their number is too low to be
  distinguished from the graph**." Note this is a *power* argument, not a conceptual one —
  and your snapshot has 32 Class A Intermediates plus 21 in the extension tier, which is not
  obviously too few.

## 3. The geometry itself — and this is the part that decides it

**The literature disagrees, the disagreement is quantified, and it resolves into a
selection effect rather than a contradiction.**

### Evidence that agonist-only lands short of fully active

**`paajanen2026activation` is the strongest, because it is a measurement over 1,351
structures with an unsupervised index.** Verbatim, p.1 (abstract):

> "**Agonist binding shifts this conformational ensemble towards the active state but does
> not fully stabilize it. Instead, a stable active state is only established upon G protein
> binding, which locks the receptor in its active conformation.**"

and the observation behind it:

> "This leads to a key observation, **the apo form of several class A GPCRs exists in both
> the inactive and active states, and the agonist-bound form also exists in both the inactive
> and active states.** This indicates that the conformation of class A GPCRs spontaneously
> switches between the [in]active and active states…"

**So agonist-bound transducer-free structures are not a class at all — they are bimodal on
the very coordinate you are calibrating.** Including them in either pole adds a genuinely
two-component contaminant to that pole, which is worse than a shifted threshold: it inflates
the variance of the class the GMM is trying to separate.

**`georgiou2025heterogeneity` states it as a taxonomy claim** (PDF p.7 = printed p.3697):

> "**Class A GPCRs in complex with only full agonists (without G or βarr protein) adopt an
> intermediate active conformation, which might be a preactive conformation in the activation
> pathway.** Τhe structure of class A GPCRs in such transient conformations **has not yet been
> thoroughly characterized**…"

and, in its directional-control inventory, **full agonist → "shifts toward A but does not
reach it alone"**, with A^TM6 reserved for "full agonist **plus transducer**" (pp.10, 16, 25).

**And it gives populations, which is what makes this non-circular** (all PDF p.11–16 =
printed p.3701–3706, from primary work the review cites):

| system | populations | method |
|---|---|---|
| **A2AR TM7, agonist NECA-bound** | **49% inactive / 37% intermediate I2^TM7 / 14% active A^TM7** | SMF/TIRF, nanodiscs, three-state fit (p.13) |
| A2AR TM7, apo **and** antagonist | 63% inactive / 37% active | same (p.13) |
| β2AR, balanced agonist formoterol | **~35% inactive** | ¹⁹F NMR, DDM/CHS (p.15) |
| β2AR, ultrahigh-affinity full agonist BI-167107 | inactive S1+S2 reduced by **40–50%** *from apo* | DEER (p.16) |

**With a full agonist and no transducer, A2AR's TM7 — the NPxxY axis — is 14% active.**

**`hilger2020gcgr` supplies the class B case**, p.1: glucagon "induces conformational change
on the extracellular side of the receptor (ECD, TM1, TM2, TM6, and TM7) **without inducing
outward movement of TM6 on the intracellular side**", and "**The outward movement of TM6 of
GCGR is only observed upon interaction with Gs**".

### Evidence that agonist-only reaches nearly all the way

**`vo2026fiducials` is the serious counter-case and it is on β2AR, from new cryo-EM
structures** (p8–p9):

> "the high efficacy agonist BI-167107 **induces almost complete outward movement of TM6 even
> in the absence of G-protein**, with the introduction of the Gs α5 helix shifting TM6 by
> **less than 1 Å further outward at most positions**"

> "BI-167107 alone is again sufficient to induce a substantial shift in the [ICL2] motif to
> **nearly match the Gs-bound result**"

Its INDEX claim line is blunt: *"Agonist alone drives β2AR TM6 nearly to the Gs-bound
arrangement."* The note already warns against overstating it — the wording is "almost
complete" and "nearly match", not identity.

*(Outside the corpus, pointing the same way: Ferré et al., Cell Rep 2022, 41:111844 — A2AR
with mini-Gs vs agonist alone, "the two conformations are similar… supporting a model whereby
**agonist binding alone is sufficient to populate a conformation resembling the active
state**." Abstract-level only, not extracted.)*

### The reconciliation, and it is the load-bearing point

**Both are true, and they are measurements of different things.** `vo2026fiducials` reports a
**deposited structure**; `georgiou2025heterogeneity` reports **ensemble populations** — and
for the *same agonist*, BI-167107, the ensemble is only 40–50% shifted out of the inactive
states. A deposited structure is **the conformer that crystallised, not the ensemble mean**.

So the physical statement is: *an agonist-only receptor populates a broad ensemble in which
the fully-active conformer is a minority (14% on A2AR TM7), and a structure of that conformer
can nevertheless be solved and deposited and will look almost fully active.*

**That is exactly why agonist-only deposited structures are the worst calibration class**:
they are the group whose ensemble is most heterogeneous, so the deposited member is the least
representative of its own pharmacological label. **And this argument does not use our thesis
at any step** — it rests on paajanen's bimodality over 1,351 structures, on single-molecule
and DEER populations from primary work, and on the general fact that deposition selects
conformers.

---

## What I would actually do, and why it is not circular

**Adopt `lee2026confornets`'s published rule, and report everything else.** Calibrate the
thresholds on **GPCRdb activation degree = 100%** (active pole) and the corresponding
inactive extreme, exactly as lee did — "We selected GPCRs with both fully active (100%
activation degree) and inactive structures available" (p15). Then:

1. **The exclusion is made on an independent database's graded annotation, decided before
   you look at our geometry, and by somebody else's published criterion.** Your 25
   antagonist-bound "Active" and 34 agonist-bound "Inactive" structures are excluded — or
   retained — by GPCRdb's own activation degree, not by whether they suit the claim. That is
   the pre-registrable, non-circular ground you asked for.
2. **Corroborate with `paajanen2026activation`'s anchor convention** — ternary as the active
   pole, antagonist-with-no-transducer as the inactive pole — which independently excludes
   agonist-only from both poles and is the other published precedent.
3. **Then report where the excluded classes fall**, on the continuous axes, following
   `chib2025gpcrstates`'s treatment of activity level as an axis rather than a label.
   Agonist-only, arrestin-complexed and Intermediate each get a reported distribution.
4. **And do exactly what you proposed anyway: report the calibration with them in as a
   sensitivity.** If the thresholds move materially, that is a result — "the cut moves X Å
   when partially-activated structures are admitted" is a publishable statement about the
   instrument, and it is the honest answer to a referee who asks why they were excluded.

**The one thing to avoid** is excluding them on the grounds that *our* thesis says an agonist
alone does not activate. That is the circular move, and it is unnecessary — three
independent, published, pre-dating reasons are available above.

**A bonus that falls out of this.** If you report the agonist-only class rather than
discarding it, `georgiou2025heterogeneity` supplies a falsifiable expectation to test it
against: those structures should sit **between** the two poles and, on A2AR at least, should
be predominantly nearer the inactive one. **If our own reference set shows agonist-only
structures piled at the active pole, that is evidence the GPCRdb annotation is doing
something we do not understand** — which is worth knowing before, not after, the campaign.

## What the corpus does not settle

- **No paper states a geometric threshold for "fully active" that we could adopt directly.**
  khaleq's "conformational criteria" are unspecified; paajanen's index is not reimplementable
  (no weight vector, no residue list, no repository); GPCRdb's activation degree is a
  database output whose internal rule is not in any corpus note.
- **Whether GPCRdb's activation degree and khaleq's rule agree** on the specific 59
  structures in question. That is checkable on your side and is the fastest way to know
  whether this matters at all.
- **The class B / class F case.** `hilger2020gcgr` covers B1 and says TM6 does not move
  without Gs — so a class B agonist-only structure is a *stronger* exclusion candidate than a
  class A one, and the instrument decision (E0.5) should note it.
