# Introduction

> **Draft status.** Sections 1–3 are written in full and are lit-only: every sentence
> rests on `lit/notes/` with a citekey, and none depends on our numbers. Sections 4–5
> are a deliberate provisional stub, per the instruction that the introduction stay
> general enough to survive a change in the story. No `[R-*]` ledger id appears
> anywhere below, and no sentence depends on a `STATUS.md` planned block (D1, D2, D3,
> T1.5). Written 2026-09-08 against `SCHEMA.md` v3, `INDEX.md` (66 papers) and
> `refs.bib` (78 entries).

---

## 1. Problem

G protein-coupled receptors are pharmacological targets whose behaviour is defined by
conformational state rather than by fold, and the state is not a binary one. A recent
survey of class A receptors describes them as occupying "three different conformational
states (active, inactive, intermediate-active) that can be interconverted for the
activation/inactivation process according to a multistate, rheostat-like model, instead
of a binary (on/off) switch model" [georgiou2025heterogeneity p.6], with heterogeneity
present even inside the inactive ensemble [georgiou2025heterogeneity p.9]. An
unsupervised activation index built over the deposited class A structures recovers the
same picture from the databank itself: apo and agonist-bound receptors are both bimodal,
populating inactive and active conformations, while transducer-bound structures are
almost exclusively active [paajanen2026activation].

Which input sets that state is therefore a substantive question rather than a modelling
convention. Occupancy of the orthosteric site and occupancy of the active state are
distinct variables, coupled to a degree that varies by receptor, strongly in A2AR and
weakly in β1AR, β2AR and μOR [georgiou2025heterogeneity p.8]. In class B GCGR they
decouple almost completely, since "agonist binding alone is insufficient to promote TM6
opening" and the outward movement appears only on Gs engagement [hilger2020gcgr p.1].
The statement drawn from the deposited structures is the same: "Agonist binding shifts
this conformational ensemble towards the active state but does not fully stabilize it.
Instead, a stable active state is only established upon G protein binding, which locks
the receptor in its active conformation" [paajanen2026activation p.1]. The contact that
carries this is specific rather than diffuse. The Gα α5 helix, and particularly its
distal C-terminal segment, "must be inserted into the receptor's cytoplasmic cleft to
couple with the GPCR" [georgiou2025heterogeneity p.4].

Co-folding models of the AlphaFold 3 lineage cannot express any of this, and their
authors say so. Structure prediction models "typically predict static structures as seen
in the PDB, not the dynamical behaviour of biomolecular systems in solution", and "this
limitation persists for AF3, in which multiple random seeds for either the diffusion head
or the overall network do not produce an approximation of the solution ensemble"
[abramson2024af3 p.6]. On the paired apo and ligand-bound forms of cereblon, "AF3
exclusively predicts the closed state for both holo and apo systems" [abramson2024af3
p.6]. That collapse has since been characterised independently. Across a PDB-wide,
mechanism-stratified benchmark, four co-folding models and one ensemble emulator recover
all known intrinsic states in only about 8 to 29% of clusters, and the bottleneck is
traced to the structure module rather than to pair-representation diversity
[ku2026promise]. On four multi-state proteins the models "default to a dominant state represented in the PDB", and the bias is
reproduced by every architecture tested [ye2026multistatebias p.2]. On human kinases,
state accuracy plateaus at roughly 65 to 75%, ensembles are bimodally all-right or
all-wrong across samples, and geometric quality does not predict whether the state is
right [sun2026kinconfbench]. On SLC transporters the deposited state is returned
whatever the sampling intervention, and "the ESM-AF2 protocols described here fail to
generate the alternative conformational state when one conformational state was
available in the PDB at the time of AF2 training" [swapna2025memorization p.11].

For receptors specifically the collapse has a direction. Sequence-only AF2 and AF3
models agree best with inactive references and agree less well as the reference becomes
more active [chib2025gpcrstates], and the earlier statement of the same result is that
AF2 "only predicts one state and is biased toward either the active or inactive
conformation depending on the GPCR class" [heo2022multistate p.1]. Nor can the model's
own confidence be used to select the correct state after the fact. Cfold reports "no
clear relationship between the plDDT and known conformations from the PDB suggesting
that confidence metrics can't be used to select for certain conformations"
[bryant2024cfold p.5]; the multi-state survey concludes that pLDDT and PAE "are not
reliable selectors of biologically or physically meaningful alternative states"
[ye2026multistatebias p.15]; and on GPCR peptide complexes PAE over-estimates confidence
precisely for misplaced peptides, so confidence-first filtering cannot separate correct
from incorrect placement [junker2026peptidedesign].

## 2. What has been tried

Interventions on the input have been the dominant route. The simplest is to sample
harder without directing: inference-time dropout with thousands of models per target
[wallner2023afsample], or a retrained predictor sampling on the order of a hundred
structures per target, which recovers a held-out conformation for 52% of targets but
only as a best-of-N result with no selection rule [bryant2024cfold]. The alignment
itself has been manipulated in several ways: clustering it by edit distance so that
different subsets favour different conformations [waymentsteele2024cluster], a
mechanism contested as no better than random shallow subsampling [schafer2025confounds]
and then defended by column-shuffling controls [waymentsteele2025reply]; random
subsampling below the coevolution threshold [lee2025seqassoc]; in-silico alanine
mutagenesis of alignment columns [stein2022speachaf]; and column masking at a tuned
fraction [kalakoti2025afsample2, kalakoti2026afsample3], including masking restricted to
the neighbourhood of the orthosteric pocket in class A receptors
[mitjavila2026afsample2t]. Tested head to head on multi-state targets, however,
"MSA-level manipulation alone, whether through evolutionary clustering or random
subsampling, is largely insufficient to overcome the systematic conformational bias
observed across the deep learning tools evaluated in this study"
[ye2026multistatebias pp.16–17].

The other input-side route supplies the answer as a template or an annotation. State-
annotated GPCRdb templates combined with total MSA deletion allow an operator to obtain
either activation state at near-experimental accuracy [heo2022multistate], and the same
route has since been used to pin active-state templates for peptide-agonist ranking and
orphan receptor deorphanisation [ferguson2026deorphann] and to condition a fine-tuned
co-folding model on a declared state for peptide design [yang2025statespecific]. The
limits of the route are documented by its own practitioners. Templates alone do not move
predictions when a deep alignment is present, since "using such curated template
databases was not sufficient to make meaningful changes" [heo2022multistate p.3]; in
transporters a correct alternative-state template is flipped back to the memorised state
[swapna2025memorization]; and on a kinase and class A GPCR panel both handles together
fall short, where "attempts to guide predictions through MSA editing or templating proved
to be insufficient, especially for the active-state conformation"
[obendorf2026statespecific p.18].

A newer family intervenes inside the model at inference time, leaving the inputs alone.
Interventions have been placed on the coordinates during denoising, by adding the
gradient of a differentiable collective variable to the sampler update
[lam2026metadiffusion]; on the trunk representation, by perturbing the conditioning
tensors [jung2026boltzperturb], by scaling the pair representation with a single scalar
[suzuki2026pairscaling], by applying a mutual repulsion between parallel samples
[suzuki2026conforflux], or by learning an affine transform of the pair representation
[lee2026confornets]; on the conditioning embedding by gradient ascent [li2026embedding];
and on the alignment feature by a gradient taken through the model's own distogram
[tang2026steeraf]. Interpretability work supports the choice of site, identifying the
pair track rather than the single track as the causal geometric substrate
[feldman2026alphainterp] and showing that trunk representations are steerable across
model families [lu2026twostages], though decodability of a concept does not by itself
imply that the model uses it causally [jedryszek2026probing]. Sampling and steering
machinery of this general kind now ships in production co-folding code
[wohlwend2024boltz1, passaro2025boltz2]. A separate line replaces the predictor
altogether with a generative emulator trained on molecular dynamics, which produces
equilibrium ensembles but was trained on soluble single chains rather than membrane
proteins [lewis2025bioemu].

A smaller body of work uses a biological co-input as the handle instead of an operator
setting. Supplying the cognate ligand of a cryptic site shifts AF3 ensembles onto the
open pocket while ligand-free runs give the closed one [lazou2026cryptic]; co-folding a
competitive blocker restores discovery of allosteric and cryptic sites that are
otherwise overwritten [purnomo2026cafe]; and across four multi-state proteins,
"small-molecule ligands have weak or inconsistent effects, while large protein partners
drive clear conformational switching between states" [ye2026multistatebias p.2].
Alongside these sit the instruments: multi-state benchmarks [ku2026promise,
sun2026kinconfbench], receptor-specific evaluations [chib2025gpcrstates,
zhang2026generalization, obendorf2026statespecific], and proposals for the evidential
bar any multi-state claim should clear [chakravarty2026statespace,
liu2026ensembletests].

## 3. The gap

Surveying this work by what it does rather than by what it studies, a consistent shape
appears. Prospectivity is rare: of 66 papers surveyed here, exactly two report an
unqualified prospective result, and neither is of the relevant kind. One is a wet-lab
peptide study that generates no structures [tran2026nanogs], the other a blind CASP15
submission that defines no conformational state at all [wallner2023afsample]. Where a
method does direct the state, the direction is very often obtained from a structure of
the answer. Cfold's
recovery rate is a best-of-N selected by TM-score against the held-out structure, and
the paper demonstrates that no confidence-based substitute exists [bryant2024cfold p.5].
ConforNets obtains transferable state control, but its supervision signal for the
transfer task is itself a deposited target structure [lee2026confornets], so it cannot be
pointed at a receptor whose target state has never been solved. Trunk-scaling and
repulsion strengths are swept on the same benchmarks the methods are scored against
[suzuki2026pairscaling, suzuki2026conforflux].

Where a directional handle exists at all, it is usually the operator's. Fourteen of the
66 papers carry one. Restricting to prediction
pipelines applied to receptors, the state is supplied by the operator in every case: as a
state-annotated template
[heo2022multistate], as a pinned active-state template [ferguson2026deorphann], as a
declared state label routed through state-matched templates [yang2025statespecific], or
as a learned transform supervised by a reference structure [lee2026confornets]. Where
the handle is instead a biological co-input, one of three things is true: the system is
not a receptor [lazou2026cryptic, purnomo2026cafe]; the demonstration is four targets
with no memorization control run [ye2026multistatebias]; or the endpoint measured is
binding-site geometry for docking rather than the receptor's activation state
[mitjavila2026afsample2t].

The nearest near-miss is `yang2025statespecific`, and it is worth stating precisely what
it does. A GPCR-specialised co-folding model conditioned on activation state ranks
designed peptides into agonists and antagonists, with nanomolar hits assayed, and the
authors identify state control as exactly what prior peptide-design methods lack:
"these methods do not allow for precise control over the GPCR's functional state (e.g.,
active or inactive)" [yang2025statespecific p.2]. The direction of the dependency is the
difference. The state is declared before any peptide is scored, and the authors write
that "HF-Multistate, when specifying the GPCR state, can partially capture functional
shifts in peptide design" [yang2025statespecific p.10]. The peptide is the designed
output; no experiment there varies a peptide sequence with the state conditioning held
fixed and reports the resulting receptor conformation.

Where the co-input is a G protein and the scale is large, the state is not measured at
all. Interface fingerprints have been extended to 825 modelled receptor–G protein
complexes with no activation criterion defined anywhere in the work
[matic2023gpcrome]; the whole GPCRome has been co-folded against all Gα subunits, with
the receptor's state assumed from the presence of the partner and no activation
predicate applied [miglionico2026atlas]; and 5,595 AF2-Multimer complexes have been
released gated purely on self-confidence, with no activation state assigned to any model
[pandyszekeres2024gproteindb]. The instrument to close that loop exists. A learned
classifier separates active from inactive deposited GPCR structures with near-perfect
discrimination, and its authors propose the missing experiment themselves:
"By applying HYALINE to AlphaFold 3-generated GPCR models, researchers can obtain rapid,
quantitative estimates of whether the predicted structure represents an active, inactive,
or intermediate conformation" [khaleq2026hyaline p.11]. No such experiment is reported in
that paper or anywhere else in the corpus.

The benchmarks that would otherwise settle the question exclude the motion by
construction. ProMiSE states it in its own Limitations: "Our pair-extraction criterion,
TM-score < 0.8, is also stringent and preferentially captures large conformational
changes. Consequently, localized but biologically important motions, such as GPCR TM6
displacement or transporter pocket rearrangements, may be excluded" [ku2026promise p.9].
The same TM-score 0.8 rule defines the structural clusters of the Cfold benchmark
[bryant2024cfold p.7] and is inherited by work built on it [kalakoti2026afsample3], with
the same effect and without the acknowledgement. ProMiSE also reports that
protein-induced changes are predicted less well than ligand-induced ones
[ku2026promise], a result that runs opposite to the axis examined here and that is
addressed directly in the Discussion.

Memorization is the last column, and it separates into two questions that are usually
merged. Forty of the 66 papers have some held-out or post-cutoff set in their design;
far fewer run that set as an analysed control arm. Among the papers that
actually address GPCR conformational state, the control is absent, unpowered or
unmatched [chib2025gpcrstates, ye2026multistatebias, obendorf2026statespecific,
yang2025statespecific]. That omission is consequential rather than pedantic, because
co-folding's advantage is concentrated near the training distribution and vanishes in the
least-similar stratum [skrinjar2026generalization, roehrig2026docking], sequence-identity
splitting does not by itself stop leakage [mattsson2026leakage], and predicted ligand
placement can survive a pocket being made incapable of binding, which shows retrieval
rather than physics driving the result [masters2025physics].

Taken together, the corpus contains no study in which a biological co-input, rather than
an operator-declared label or a reference structure, is what sets a receptor's predicted
conformational state, and in which the resulting state is then verified against an
operationalised predicate rather than assumed from the presence of the partner. That is
the gap this work addresses.

## 4. What we do

> **PROVISIONAL STUB.** Landed blocks only, no numbers, and to be rewritten once the
> data export is complete. See `../STATUS.md` for what has landed and what has not.

We treat the Gα α5 C-terminal peptide as a co-input to a frozen co-folding model and ask
what the receptor does in response, holding the model, the alignment and the templates
unchanged. Predictions are run across a panel of class A receptors on four independent
co-folding backbones, under input conditions that vary the co-input while leaving
everything else fixed, and the receptor's conformational state is called by an
operationalised predicate rather than by eye. Three arms have landed. The first compares
apo receptors against receptors given their cognate partner. The second places apo,
decoy, sequence-shuffled and cognate co-inputs on a common scale, which allows the effect
to be decomposed into a contribution from occupancy of the cleft, a contribution from the
α5 C-terminal sequence itself, and a contribution from that sequence belonging to the
correct Gα family. The third asks whether the pocket, as distinct from the cytoplasmic
face, separates by ligand class. Alongside these we report a census of intermediate
conformations produced under partner variation, and an observation about model
confidence made across backbones on a single receptor.

## 5. Contributions

> **PROVISIONAL STUB.** Four candidate contributions, each written so that it can be
> falsified. The wording is expected to change with the final result set; the framing is
> intended to survive it.

1. A biological co-input, supplied in the same way a user of these models would supply
   it, moves the predicted conformational state of a receptor. Falsified if the state
   distribution under the cognate co-input is indistinguishable from the apo
   distribution.
2. The effect is attributable to the co-input rather than to steric occupancy alone,
   because decoy and sequence-shuffled arms sit between the two. Falsified if a decoy of
   matched size reproduces the cognate effect.
3. The state is verified rather than assumed, by a predicate defined in advance and
   reported with its threshold, applied identically to every arm and cross-checked
   against a second instrument. Falsified if the two instruments disagree on the ordering
   of the arms.
4. Model confidence does not track conformational correctness on this axis, so it cannot
   be used to select a state. Falsified if confidence separates correct from incorrect
   state calls at matched partner composition.

---

## Citation check

Every citekey used above, confirmed present in `../lit/refs.bib` and with a note file in
`../lit/notes/`. Checked mechanically, 2026-09-08.

abramson2024af3 · bryant2024cfold · chakravarty2026statespace · chib2025gpcrstates ·
feldman2026alphainterp · ferguson2026deorphann · georgiou2025heterogeneity ·
heo2022multistate · hilger2020gcgr · jedryszek2026probing · jung2026boltzperturb ·
junker2026peptidedesign · kalakoti2025afsample2 · kalakoti2026afsample3 ·
khaleq2026hyaline · ku2026promise · lam2026metadiffusion · lazou2026cryptic ·
lee2025seqassoc · lee2026confornets · lewis2025bioemu · li2026embedding ·
liu2026ensembletests · lu2026twostages · masters2025physics · matic2023gpcrome ·
mattsson2026leakage · miglionico2026atlas · mitjavila2026afsample2t ·
obendorf2026statespecific · paajanen2026activation · pandyszekeres2024gproteindb ·
passaro2025boltz2 · purnomo2026cafe · roehrig2026docking · schafer2025confounds ·
skrinjar2026generalization · stein2022speachaf · sun2026kinconfbench ·
suzuki2026conforflux · suzuki2026pairscaling · swapna2025memorization · tang2026steeraf ·
tran2026nanogs · wallner2023afsample · waymentsteele2024cluster · waymentsteele2025reply ·
wohlwend2024boltz1 · yang2025statespecific · ye2026multistatebias · zhang2026generalization

51 citekeys. Not cited, and deliberately: the four papers never obtained
(`chiesa2025templatebias`, `bret2025boltz2docking`, `nittinger2025cofolding`,
`yu2026domainmotion`) and the eight bibliography-only entries added 2026-09-08
(`singhal2025fksteering`, `richman2025conformix`, `wu2023tds`, `kim2023refining`,
`ekstromkelvinius2024discriminator`, `ingraham2023chroma`, `aureli2026epath`,
`kohlhoff2014gpcr`), none of which has a note or a PDF in the corpus.
