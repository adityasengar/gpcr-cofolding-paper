# Introduction

> **Draft status, 2026-09-08.** This replaces the shorter draft written earlier the same day
> (kept at `/tmp/intro_short_v1.md` for one session only). The literature sections below are
> written at the length of a *Nature Structural & Molecular Biology* or *Nature Methods*
> introduction: continuous prose, grouped by what the work does rather than one paper per
> sentence, and carrying its own gap argument rather than deferring it to the Discussion.
>
> Everything down to and including the gap is lit-only and durable: every claim about prior work
> rests on `lit/notes/` with a citekey, and no sentence depends on our numbers. The two closing
> sections are a marked provisional stub, per the instruction that the introduction stay general
> enough to survive a change in the story. No `[R-*]` ledger id appears anywhere, and no sentence
> depends on a `STATUS.md` planned block (D1, D2, D3, T1.5).
>
> Written against `lit/SCHEMA.md` v3, `lit/INDEX.md` at **71 papers**, and `lit/refs.bib` at 78
> entries with all metadata verified the same day.

---

The pharmacology of a G protein-coupled receptor is defined by its conformational state rather
than by its fold. Two ligands that bind the same pocket of the same receptor can produce opposite
physiology, and the difference is carried not by the backbone the receptor adopts on average but
by which cytoplasmic conformation it populates and for how long. That conformational description
has become steadily less binary as the experimental methods have improved. A recent survey of
class A receptors sets out the modern picture directly, describing receptors that occupy "three
different conformational states (active, inactive, intermediate-active) that can be interconverted
for the activation/inactivation process according to a multistate, rheostat-like model, instead of
a binary (on/off) switch model" [georgiou2025heterogeneity p.6], with conformational heterogeneity
present even within what is conventionally called the inactive ensemble
[georgiou2025heterogeneity p.9]. The same conclusion emerges from the structural databank when it
is analysed without supervision. Projecting the deposited class A structures onto a single learned
activation coordinate shows that apo and agonist-bound receptors are each bimodal, populating both
inactive and active conformations, while transducer-bound structures fall almost entirely on the
active side [paajanen2026activation].

Which input sets that state is therefore a substantive biological question rather than a modelling
convention, and the answer is not simply the ligand. Occupancy of the orthosteric pocket and
occupancy of the active state are distinct variables whose coupling varies from receptor to
receptor, strongly in A2AR and weakly in beta1AR, beta2AR and the mu-opioid receptor
[georgiou2025heterogeneity p.8]. In class B GCGR the two decouple almost entirely: "agonist binding
alone is insufficient to promote TM6 opening", and the outward movement of TM6 appears only once
Gs engages [hilger2020gcgr p.1]. Read across the databank the same asymmetry holds, with "agonist
binding shifts this conformational ensemble towards the active state but does not fully stabilize
it. Instead, a stable active state is only established upon G protein binding, which locks the
receptor in its active conformation" [paajanen2026activation p.1]. The contact that carries this is
specific rather than diffuse. It is the alpha5 helix of Galpha, and in particular its distal
C-terminal segment, which "must be inserted into the receptor's cytoplasmic cleft to couple with
the GPCR" [georgiou2025heterogeneity p.4]. A receptor's state is set by what is bound at the
intracellular face at least as much as by what is bound in the pocket.

Structure prediction has meanwhile become accurate enough to be used as a working instrument in
receptor pharmacology, and it represents none of this. Co-folding models of the AlphaFold 3 lineage
return one structure per input, a limitation their authors state plainly: such models "typically
predict static structures as seen in the PDB, not the dynamical behaviour of biomolecular systems
in solution", and "this limitation persists for AF3, in which multiple random seeds for either the
diffusion head or the overall network do not produce an approximation of the solution ensemble"
[abramson2024af3 p.6]. The failure is not merely one of breadth. On the paired apo and ligand-bound
forms of cereblon, "AF3 exclusively predicts the closed state for both holo and apo systems"
[abramson2024af3 p.6], which is to say the model returns whichever state dominates its training
data regardless of what the input specifies. Independent work has since established that this is
the general behaviour rather than an anecdote. On a PDB-wide, mechanism-stratified benchmark, four
co-folding models and one ensemble emulator recover all known intrinsic states in only about 8 to
29% of sequence clusters, and the bottleneck is traced to the structure module rather than to any
loss of diversity in the pair representation [ku2026promise]. Across four multi-state proteins the
models "default to a dominant state represented in the PDB", and the bias survives every
architecture tested [ye2026multistatebias p.2]. On human protein kinases, state accuracy plateaus
near 65 to 75%, ensembles are bimodally all-correct or all-incorrect across samples, and the usual
geometric quality scores do not predict which [sun2026kinconfbench]. On SLC transporters the
deposited state is returned whatever the sampling intervention, to the point that "the ESM-AF2
protocols described here fail to generate the alternative conformational state when one
conformational state was available in the PDB at the time of AF2 training"
[swapna2025memorization p.11].

For receptors the collapse has a direction, and it runs against the state that matters most for
agonist pharmacology. Sequence-only AF2 and AF3 models agree best with inactive references and
agree progressively less well as the reference becomes more active [chib2025gpcrstates]; the
earlier statement of the same phenomenon is that AF2 "only predicts one state and is biased toward
either the active or inactive conformation depending on the GPCR class" [heo2022multistate p.1].
Nor is this a problem that could be solved by generating many structures and selecting among them,
because the models' own confidence does not track conformational correctness. Cfold reports "no
clear relationship between the plDDT and known conformations from the PDB suggesting that
confidence metrics can't be used to select for certain conformations" [bryant2024cfold p.5]; the
multi-state survey concludes that pLDDT and PAE "are not reliable selectors of biologically or
physically meaningful alternative states" [ye2026multistatebias p.15]; and on GPCR peptide
complexes specifically, PAE over-estimates confidence precisely where the peptide has been placed
incorrectly, so confidence-first filtering cannot separate correct from incorrect placement
[junker2026peptidedesign]. Sampling harder and ranking by confidence is therefore not a route to a
chosen state, and this constrains everything that follows: any method claiming a state must supply
a state criterion independent of the model that produced the structure.

Attempts to recover more than one state divide cleanly by where they intervene, and the oldest
family intervenes on the input. The simplest version samples harder without steering at all, either
by injecting dropout at inference and generating thousands of models per target
[wallner2023afsample], or by retraining a predictor on a conformationally split databank and
drawing on the order of a hundred samples per target, which recovers a held-out conformation for
52% of targets but only as a best-of-N result with no rule for picking the right sample
[bryant2024cfold]. The alignment has been manipulated in most of the ways available: clustered by
edit distance so that different subsets favour different conformations [waymentsteele2024cluster],
a mechanism subsequently challenged as no better than random shallow subsampling
[schafer2025confounds] and then defended with column-shuffling controls [waymentsteele2025reply];
subsampled below the depth at which coevolutionary signal survives [lee2025seqassoc]; edited by
in-silico alanine mutagenesis of alignment columns [stein2022speachaf]; and masked at a tuned
column fraction [kalakoti2025afsample2, kalakoti2026afsample3], including masking restricted to the
neighbourhood of the orthosteric pocket in class A receptors [mitjavila2026afsample2t]. Tested head
to head against the same targets, however, "MSA-level manipulation alone, whether through
evolutionary clustering or random subsampling, is largely insufficient to overcome the systematic
conformational bias observed across the deep learning tools evaluated in this study"
[ye2026multistatebias pp.16-17].

The other input-side family supplies the answer rather than perturbing the question.
State-annotated GPCRdb templates combined with deletion of the alignment allow an operator to
obtain either activation state at near-experimental accuracy [heo2022multistate], and that route
has since been used to pin active-state templates for ranking peptide agonists and deorphanising
receptors [ferguson2026deorphann], and to condition a fine-tuned co-folding model on a declared
state for peptide design [yang2025statespecific]. Its limits are documented by the people who use
it. Templates alone do not move a prediction when a deep alignment is present, because "using such
curated template databases was not sufficient to make meaningful changes" [heo2022multistate p.3];
in transporters a correct alternative-state template is flipped back to the memorised state
[swapna2025memorization]; and on a panel spanning kinases and class A receptors both handles
together fall short, where "attempts to guide predictions through MSA editing or templating proved
to be insufficient, especially for the active-state conformation" [obendorf2026statespecific p.18].

A newer family leaves the inputs untouched and intervenes inside the generative process. Its
machinery comes from the diffusion literature rather than from structural biology: twisted
sequential Monte Carlo for asymptotically exact conditional sampling [wu2023tds], reward-weighted
particle steering that requires no differentiable objective [singhal2025fksteering], and
discriminator guidance in both the continuous [kim2023refining] and the discrete
[ekstromkelvinius2024discriminator] settings. None of those four papers contains a conformational
experiment and two contain no biomolecule at all, so they establish the mechanism rather than any
structural result. Applied to structure models, the same machinery takes several forms.
Interventions have been placed on the coordinates during denoising, by adding the gradient of a
differentiable collective variable to the sampler update [lam2026metadiffusion], or by running
particles under a bias away from the model's own default prediction and reweighting them
[richman2025conformix]. Others act on the trunk representation, by perturbing the conditioning
tensors [jung2026boltzperturb], scaling the pair representation with a single scalar
[suzuki2026pairscaling], applying a mutual repulsion between parallel samples
[suzuki2026conforflux], or learning an affine transform of the pair representation
[lee2026confornets]. Others still act on the conditioning embedding by gradient ascent
[li2026embedding], or on the alignment feature through a gradient taken back through the model's
own distogram [tang2026steeraf]. Mechanistic work supports the choice of site, identifying the pair
track rather than the single track as the causal geometric substrate [feldman2026alphainterp] and
showing that trunk representations are steerable across model families [lu2026twostages], with the
caveat that a concept being linearly decodable does not establish that the model uses it causally
[jedryszek2026probing]. Sampling and steering machinery of this general kind now ships in
production co-folding code [wohlwend2024boltz1, passaro2025boltz2]. A parallel strategy abandons
the predictor altogether and trains a generative emulator on molecular dynamics, which produces
quantitative equilibrium ensembles but was trained on soluble single chains rather than on membrane
proteins [lewis2025bioemu].

A smaller and, for the present purpose, more relevant body of work uses a biological co-input as
the handle. Supplying the cognate ligand of a cryptic site shifts AF3 ensembles onto the open
pocket while ligand-free runs return the closed one [lazou2026cryptic]; co-folding a competitive
blocker restores discovery of allosteric and cryptic sites that the orthosteric pocket otherwise
overwrites [purnomo2026cafe]; and across four multi-state proteins, including beta2AR,
"small-molecule ligands have weak or inconsistent effects, while large protein partners drive clear
conformational switching between states" [ye2026multistatebias p.2]. Running alongside all of this
is a growing measurement literature: multi-state benchmarks [ku2026promise, sun2026kinconfbench],
receptor-specific evaluations [chib2025gpcrstates, zhang2026generalization,
obendorf2026statespecific], and explicit proposals for the evidential bar that a multi-state claim
should have to clear [chakravarty2026statespace, liu2026ensembletests].

Surveying this work by what it does rather than by what it studies exposes a consistent shape.
Prospectivity is close to absent. Of the 71 papers surveyed here, exactly two report an unqualified
prospective result, and neither is of the relevant kind: one is a wet-lab peptide study that
generates no structures [tran2026nanogs], the other a blind CASP submission that defines no
conformational state at all [wallner2023afsample]. Where a method does direct the state, the
direction is usually obtained from a structure of the answer. Cfold's recovery rate is a best-of-N
selected by TM-score against the held-out structure, and the paper demonstrates that no
confidence-based substitute exists [bryant2024cfold p.5]. ConforNets achieves transferable state
control, but the supervision signal for its transfer task is itself a deposited target structure
[lee2026confornets], so it cannot be pointed at a receptor whose target state has never been
solved. Trunk-scaling and repulsion strengths are swept on the same benchmarks that report the
results [suzuki2026pairscaling, suzuki2026conforflux]. The cleanest exception is ConforMix, which
biases away from the model's own default prediction and so needs no reference structure at all, on
the explicit claim that prior conditional sampling on biomolecular diffusion models "has required
additional input information, such as experimentally measured pairwise distances"
[richman2025conformix p.2]. Even there, coverage is scored against deposited references and both
reported rows are selected as the closest sample to one [richman2025conformix p.6].

Where a directional handle exists at all, it is usually the operator's rather than the biology's.
Fifteen of the 71 papers carry one. Restricting to prediction pipelines applied to receptors, the
state is supplied by the operator in every case: as a state-annotated template [heo2022multistate],
as a pinned active-state template [ferguson2026deorphann], as a declared state label routed through
state-matched templates [yang2025statespecific], or as a learned transform supervised by a
reference structure [lee2026confornets]. Where the handle is instead a biological co-input, one of
three things is true. The system is not a receptor [lazou2026cryptic, purnomo2026cafe,
richman2025conformix]; or the demonstration rests on four targets with no memorization control
[ye2026multistatebias]; or the quantity measured is binding-site geometry for docking rather than
the receptor's activation state [mitjavila2026afsample2t].

The nearest near-miss is worth stating precisely, because it is close. A GPCR-specialised
co-folding model conditioned on activation state ranks designed peptides into agonists and
antagonists, with nanomolar hits assayed, and its authors identify state control as exactly what
prior peptide-design methods lack, writing that "these methods do not allow for precise control
over the GPCR's functional state (e.g., active or inactive)" [yang2025statespecific p.2]. What
separates that work from the question asked here is the direction of the dependency. The state is
declared before any peptide is scored, and the authors are explicit that this is the operating
mode: "HF-Multistate, when specifying the GPCR state, can partially capture functional shifts in
peptide design" [yang2025statespecific p.10]. The peptide there is the designed output. No
experiment in that work varies a peptide sequence with the state conditioning held fixed and
reports the resulting receptor conformation.

Where the co-input is a G protein and the scale is large, the receptor's state is not measured at
all. Interface contact fingerprints have been extended to 825 modelled receptor and G protein
complexes with no activation criterion defined anywhere in the work [matic2023gpcrome]; the entire
GPCRome has been co-folded against all Galpha subunits with the receptor's state assumed from the
presence of the partner and no activation predicate applied [miglionico2026atlas]; and 5,595
AF2-Multimer complexes have been released gated purely on self-confidence, with no activation state
assigned to any model [pandyszekeres2024gproteindb]. This is not a small oversight in a corner of
the field, because these are the resources that downstream work treats as sources of active-state
structures. The instrument needed to close the loop already exists: a learned classifier separates
active from inactive deposited GPCR structures with near-perfect discrimination, and its authors
propose the missing experiment themselves, that "By applying HYALINE to AlphaFold 3-generated GPCR
models, researchers can obtain rapid, quantitative estimates of whether the predicted structure
represents an active, inactive, or intermediate conformation" [khaleq2026hyaline p.11]. No such
experiment is reported there or anywhere else in this corpus.

The benchmarks that might otherwise have settled the question exclude receptor activation by
construction, and they now do so three times over by three different mechanisms. ProMiSE states it
in its own Limitations: "Our pair-extraction criterion, TM-score < 0.8, is also stringent and
preferentially captures large conformational changes. Consequently, localized but biologically
important motions, such as GPCR TM6 displacement or transporter pocket rearrangements, may be
excluded" [ku2026promise p.9]. The same TM-score 0.8 rule defines the structural clusters of the
Cfold benchmark [bryant2024cfold p.7] and is inherited without comment by work built on it
[kalakoti2026afsample3]. The strongest inference-time sampling result to date arrives at the same
place by a third route, importing its four evaluation sets wholesale from earlier benchmark papers,
none of which contains a receptor [richman2025conformix]. ProMiSE additionally reports that
protein-induced conformational changes are predicted less well than ligand-induced ones
[ku2026promise], a result that runs opposite to the axis examined here and that is addressed
directly in the Discussion.

The last column separates two questions that are usually merged, and it is where the receptor
literature is weakest. Forty-one of the 71 papers have some held-out or post-cutoff set in their
design; far fewer run that set as an analysed control arm, and among the papers that actually
address GPCR conformational state the control is absent, unpowered or unmatched
[chib2025gpcrstates, ye2026multistatebias, obendorf2026statespecific, yang2025statespecific]. Even
the cleanest inference-time result concedes the point, noting that its evaluated proteins "were
likely present in the Boltz training set" [richman2025conformix p.6]. The omission is consequential
rather than pedantic. Co-folding's advantage over physics-based methods is concentrated near the
training distribution and largely disappears in the least-similar stratum
[skrinjar2026generalization, roehrig2026docking]; splitting on sequence identity does not by itself
stop benchmark leakage [mattsson2026leakage]; and predicted ligand placement can survive a pocket
being mutated until it cannot bind, which shows retrieval rather than physics driving the result
[masters2025physics]. A conformational claim carrying no matched control arm is therefore not yet
distinguishable from a lookup.

Taken together, this corpus contains no study in which a biological co-input, rather than an
operator-declared label or a reference structure, is what sets a receptor's predicted
conformational state, and in which the resulting state is then verified against an operationalised
predicate rather than assumed from the presence of the partner. That is the gap this work
addresses.

---

## What we do

> **PROVISIONAL STUB.** Landed blocks only, no numbers, and expected to be rewritten once the data
> export is complete. See `../STATUS.md` for what has landed and what has not.

We treat the Galpha alpha5 C-terminal peptide as a co-input to a frozen co-folding model and ask
what the receptor does in response, holding the model weights, the alignment and the template
settings unchanged and varying only what is supplied alongside the receptor sequence. Predictions
are run across a panel of class A receptors on four independent co-folding backbones, and the
receptor's conformational state is called by a predicate defined in advance rather than by eye.
Three arms have landed. The first compares apo receptors against receptors given their cognate
partner. The second places apo, decoy, sequence-shuffled and cognate co-inputs on a common scale,
which lets the effect be decomposed into a contribution from occupancy of the cytoplasmic cleft, a
contribution from the alpha5 C-terminal sequence itself, and a contribution from that sequence
belonging to the correct Galpha family. The third asks whether the orthosteric pocket, as distinct
from the cytoplasmic face, separates by ligand class. Alongside these we report a census of
intermediate conformations produced under partner variation, and an observation about model
confidence made across backbones on a single receptor.

## Contributions

> **PROVISIONAL STUB.** Four candidate contributions, each written so that it can be falsified.
> The wording will change with the final result set; the framing is intended to survive it.

1. A biological co-input, supplied the way a user of these models would supply it, moves the
   predicted conformational state of a receptor. Falsified if the state distribution under the
   cognate co-input is indistinguishable from the apo distribution.
2. The effect is attributable to the co-input rather than to steric occupancy alone, because the
   decoy and sequence-shuffled arms sit between the two extremes. Falsified if a decoy of matched
   size reproduces the cognate effect.
3. The state is verified rather than assumed, by a predicate defined in advance and reported with
   its threshold, applied identically to every arm and cross-checked against a second instrument.
   Falsified if the two instruments disagree on the ordering of the arms.
4. Model confidence does not track conformational correctness on this axis, so it cannot be used to
   select a state. Falsified if confidence separates correct from incorrect state calls at matched
   partner composition.

---

## Citation check

Every citekey used above, confirmed present in `../lit/refs.bib` and with a note file in
`../lit/notes/`. Checked mechanically, 2026-09-08.

abramson2024af3 - bryant2024cfold - chakravarty2026statespace - chib2025gpcrstates -
ekstromkelvinius2024discriminator - feldman2026alphainterp - ferguson2026deorphann -
georgiou2025heterogeneity - heo2022multistate - hilger2020gcgr - jedryszek2026probing -
jung2026boltzperturb - junker2026peptidedesign - kalakoti2025afsample2 - kalakoti2026afsample3 -
khaleq2026hyaline - kim2023refining - ku2026promise - lam2026metadiffusion - lazou2026cryptic -
lee2025seqassoc - lee2026confornets - lewis2025bioemu - li2026embedding - liu2026ensembletests -
lu2026twostages - masters2025physics - matic2023gpcrome - mattsson2026leakage -
miglionico2026atlas - mitjavila2026afsample2t - obendorf2026statespecific -
paajanen2026activation - pandyszekeres2024gproteindb - passaro2025boltz2 - purnomo2026cafe -
richman2025conformix - roehrig2026docking - schafer2025confounds - singhal2025fksteering -
skrinjar2026generalization - stein2022speachaf - sun2026kinconfbench - suzuki2026conforflux -
suzuki2026pairscaling - swapna2025memorization - tang2026steeraf - tran2026nanogs -
wallner2023afsample - waymentsteele2024cluster - waymentsteele2025reply - wohlwend2024boltz1 -
wu2023tds - yang2025statespecific - ye2026multistatebias - zhang2026generalization

Deliberately not cited, because each has a verified bibliography entry but no note and no PDF and
is therefore citable for venue and identifier only: chiesa2025templatebias, bret2025boltz2docking,
nittinger2025cofolding, yu2026domainmotion, ingraham2023chroma, aureli2026epath, kohlhoff2014gpcr.

**Note on Greek letters.** Written out (alpha5, beta2AR, Galpha) so the file survives round-tripping
through plain-text tooling. Restore the symbols when this goes into LaTeX.
