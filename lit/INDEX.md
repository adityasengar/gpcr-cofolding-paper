# INDEX.md — the paper_af3 literature corpus, one block per paper

**78 papers — the whole bibliography is now extracted.** All against `SCHEMA.md` v3, except
`ingraham2023chroma`, which is `v3-partial`. Full extractions live in
`notes/<citekey>.md`; PDFs in `pdfs/<citekey>.pdf`; bibliography in `refs.bib`.

**How to read a block.** `claim` is what the paper establishes, not what it is about.
`oracle` names which of the seven `oracle_leakage` routes fire and how — it is the field
the gap argument is built from. `tags` is the reverse-lookup mechanism and is copied
verbatim from each note. `stance` is provisional until the user confirms it.

**This file is lossy by design.** Never answer a manuscript-bound question from it —
open `notes/<citekey>.md` for thresholds, n, verbatim quotes and page numbers. An index
line saying "binary predicate" does not tell you the threshold or whether it saturated.

**Licence note.** `ND licence` on a figs line means the ND clause forbids redrawing a
panel, not merely copying it. Check the note before adapting any figure.

---

### abramson2024af3 — 2024, Nature 630:493–500 (peer-reviewed)
claim: One diffusion co-folding model beats specialist tools across all PDB molecule types, yet collapses onto a single static conformational basin.
system/method: general protein + nucleic acids/ligands | co-folding | AF3, AF-M 2.3, RF2NA, RFAA
states: ensemble + single-state | metric: RMSD-to-reference + visual (LDDT/DockQ/pocket-RMSD thresholds; state called by eye) | prospective: no
oracle: routes 1,4,5,6,7 — date-filtered templates, checkpoint tuned on eval set, retrospective scoring, hand-picked showcases
figs: 31 panel-group rows
tags: general-protein cofolding templates-on single-state ensemble binary-predicate continuous-metric visual-metric saturating-metric design-level-oracle anti-memorization multi-backbone peer-reviewed background precedent comparator-numbers
stance: background + precedent — supplies the baseline; authors concede single-state collapse themselves

### aureli2026epath — 2026, J. Phys. Chem. Lett. 17(10):2974-2983, peer-reviewed (CC-BY)
claim: A Euclidean path collective variable ("EPATH") makes class A GPCR activation free energies computable without hand-picking intermediate structures; applied to apo ADRB1 and apo MOR.
system/method: GPCR class A, 2 apo receptors (ADRB1, MOR) | MD + enhanced sampling (OneOPES, path CV, microswitch restraints) | NOT APPLICABLE - no predictor run
states: continuum + two-state | metric: continuous only - path progress plus PIF/DRY/NPxxY/YY descriptors, NO threshold anywhere | prospective: partial (ADRB1 reproduction, MOR new)
oracle: routes 1-7 largely NOT APPLICABLE (no prediction pipeline); route 4 in kind (CV refinement), route 7 design-level
figs: Fig 1 schematic + free-energy surfaces; CC-BY, redrawing permitted. NO PDF HELD - section locators only
tags: gpcr md enhanced-sampling continuum two-state continuous-metric directed-state apo-sampling design-level-oracle peer-reviewed background precedent comparator-numbers
stance: background + precedent - the corpus's only free-energy account of class A activation, and its only apo-receptor landscape with nothing bound

### bryant2024cfold — 2024, Nature Communications 15:7328 (peer-reviewed)
claim: Retrained AF2 with undirected sampling recovers held-out alternative conformations for 52% of targets, but only as best-of-100 with no selection rule.
system/method: general protein (monomeric PDB) | retrained predictor + MSA-subsampling/dropout inference + benchmark construction | Cfold only (AF2 never run as baseline)
states: ensemble (~100 predictions/target, spread across states) | metric: continuous TM-score + binary predicate (TM > 0.8 success, > 0.2 TM state difference) | prospective: no
oracle: routes 4,5,6,7 — best-of-N against held reference, targets filtered by model's own TM; routes 1-3 clean
figs: 18 panel-group rows
tags: general-protein fold-switching msa-subsample ensemble continuous-metric binary-predicate anti-memorization oracle-leak design-level-oracle confidence-as-discriminator seed-only peer-reviewed precedent contrast negative-result comparator-numbers
stance: precedent + contrast — strongest anti-memorization split in corpus; headline is oracle-selected

### bugrova2026representation — 2026, bioRxiv preprint
claim: Semantically null CCD-vs-SMILES ligand encoding shifts co-folding poses more than a real protonation-state change does.
system/method: GPCR (DRD1) + bacterial histidine-kinase sensor domain (BarA) | benchmark-only | AF3 3.0.1, Boltz-2, Chai-1, Protenix-v1
states: ensemble of ligand poses, single protein conformation | metric: NOT APPLICABLE for conformation; ligand pose continuous + visual, KS on PC1 | prospective: partial
oracle: routes 5 (partial), 7 — expected binding mode declared in advance; no pipeline leakage
figs: 10 panel-group rows; ND licence
tags: gpcr general-protein cofolding benchmark-only ensemble continuous-metric visual-metric saturating-metric design-level-oracle no-anti-memorization unpowered multi-backbone ligand-driven orthosteric preprint precedent contrast negative-result comparator-numbers
stance: precedent on findings + contrast on rigour — n = 2 targets, no significance test

### chai2024chai1 — 2024, bioRxiv preprint
claim: An AF3-architecture co-folding model matches AF3 on PoseBusters and runs MSA-free at near-parity on interfaces.
system/method: general protein + nucleic acids/ligands/antibodies | co-folding | Chai-1, AF-M 2.3, AF3 (published values), RF2NA, RFAA, ESMFold
states: one (25 samples, confidence-ranked, never analysed as ensemble) | metric: NOT APPLICABLE — no conformational state assessed anywhere | prospective: no
oracle: routes 1,5,6,7 in non-headline arms — apo receptor supplied, restraints from solved complex, best-of-25 oracle curve; headline blind
figs: 13 panel-group rows
tags: general-protein cofolding no-template-no-msa templates-on single-state binary-predicate continuous-metric saturating-metric anti-memorization confidence-as-discriminator multi-backbone oracle-leak design-level-oracle preprint precedent background comparator-numbers
stance: precedent + background — MSA-free parity numbers and the 2021-01-12 training cutoff

### chakravarty2026statespace — 2026, arXiv preprint (q-bio.BM)
claim: Structure prediction should be reformulated as inference of a conformational state space p(X|S,C), not one dominant conformation.
system/method: general protein | perspective/review + roadmap (no method run) | n/a
states: NOT APPLICABLE (nothing generated) | metric: NOT APPLICABLE; prescribes rejecting RMSD/TM alone, requiring validated recovery, basin discrimination, perturbation sensitivity | prospective: NOT APPLICABLE
oracle: NOT APPLICABLE — no pipeline exists; all seven routes answered as inapplicable
figs: 5 panel-group rows; licence NOT REPORTED (treat as all rights reserved)
tags: general-protein fold-switching cryptic-pocket preprint contrast background
stance: contrast + background — sets the evidential bar any multistate claim must clear

### chen2026medchem — 2026, bioRxiv preprint
claim: Co-folding recovers orthosteric poses and ligand-linked DFG/αC kinase states, but degrades sharply at allosteric, cryptic and membrane sites.
system/method: kinases, PDE, nuclear receptor, proteases, transporters (95 entries) | benchmark-only | AF3 3.0.1, Boltz-2 2.2.0
states: ensemble + single-state (10 poses/complex) | metric: RMSD-to-reference + visual (2 Å, 1.5 Å pharmacophore, 70% volume overlap) | prospective: partial
oracle: routes 4,5,6,7 — post-hoc RMSD success, minPAE bins set on results, expected states declared in advance; route 1 not determinable
figs: 36 panel-group rows
tags: kinase transporter general-protein cofolding benchmark-only ensemble single-state continuous-metric binary-predicate visual-metric saturating-metric design-level-oracle prospective anti-memorization unpowered confidence-as-discriminator experimental-validation ligand-driven orthosteric allosteric-site cryptic-pocket preprint precedent contrast negative-result comparator-numbers
stance: precedent on findings + contrast on rigour — no matched pre-cutoff control arm

### chiesa2025templatebias — 2025, J. Chem. Inf. Model. 65(12):6298-6309, peer-reviewed
claim: Co-folding the receptor WITH its G protein reproduces the active-state intracellular rearrangement better than operator-supplied active-state templates, and the advantage survives on receptors absent from templates and training.
system/method: GPCR class A, human receptors + human Gas; 63 unique pairs / 145 structures / 55 receptors / 31 families | benchmark-only over 6 protocols spanning template-state-bias, MSA-state-filter and co-folding | AF2 + AlphaFold-Multimer. NO AF3-lineage backbone
states: two-state + single-state | metric: RMSD-to-reference per TM domain (TM6 singled out) + DockQ + per-residue binding-site RMSD < 2 A; NO operationalised activation predicate | prospective: partial (benchmark = structures released after 01 Jan 2023, vs AF2 May 2018 / AFM Oct 2021 cutoffs)
oracle: routes 1,2 present in the two template arms and ABSENT in the AFM-Ga arm - that contrast is the paper; route 5 definitional, route 7 design-level but quantified (94/145 structures have no template and are not in training)
figs: 7 figures; DockQ saturates (107 medium / 34 acceptable / 2 high). ACS, all rights reserved
tags: gpcr cofolding benchmark-only template-state-bias msa-state-filter msa-subsample templates-on state-annotated-input two-state single-state rmsd-only continuous-metric binary-predicate saturating-metric oracle-leak design-level-oracle prospective anti-memorization multi-backbone directed-state partner-driven ligand-driven orthosteric allosteric-site peer-reviewed precedent contrast comparator-numbers
stance: **precedent + contrast - THE nearest near-miss on our axis.** It supplies a biological co-input (the G protein) AND measures receptor state, which nothing else in the corpus does. Our remaining distinctions: 21-mer peptide vs whole Ga, predicate vs RMSD-to-answer, decoy/shuffled arms, AF3-lineage backbones. Read the note before writing any novelty sentence.

### chib2025gpcrstates — 2025, arXiv preprint (q-bio.QM)
claim: Sequence-only AF2 and AF3 GPCR models agree best with inactive references and worsen with activity level; AF3 worse than AF2.
system/method: GPCR (75 receptors, classes A/B1/C/F) | benchmark-only | AF2 (AFDB models), AF3 server
states: one (single-state, taken as given) | metric: RMSD-to-reference + continuous (TM-helix Cα deformation, |ΔTM3–TM6| distance), no thresholds | prospective: no
oracle: routes 5,6,7 — post-hoc deviation-to-reference scoring; targets picked for existing structure plus GPCRdb annotation
figs: 6 panel-group rows
tags: gpcr benchmark-only single-state rmsd-only continuous-metric saturating-metric design-level-oracle no-anti-memorization apo-sampling preprint precedent contrast negative-result comparator-numbers
stance: precedent on findings + contrast on rigour — inactive-bias evidence; no anti-memorization arm

### bret2025boltz2docking — 2026, J. Chem. Inf. Model. 66(3):1511-1521, peer-reviewed
claim: Boltz-2 discriminates true from false virtual-screening hits far better than any docking scoring function, yet its binary classification is insensitive to binding-site mutations that abolish binding and sometimes to exchanging the target entirely.
system/method: 10 targets, mostly GPCRs (CASR, CNR1, CNR2, DRD3, DRD4, MTR1A, SGMR2, ADRA2B) + ROCK1 kinase + SC6A4 transporter; 943 screening hits with in vitro data | benchmark-only, adversarial | Boltz-2 (structure + affinity heads) vs conventional scoring functions
states: NOT APPLICABLE - receptor conformation never assessed | metric: ROC AUC and dROC AUC (wild type minus mutant) | prospective: no
oracle: routes 1,2,3,4,6 none found or not reported - no structure is supplied as input; route 5 (labels held) and route 7 design-level
figs: not enumerated; ROC/dROC panels and SI Figs S1-S6. **Read from the HAL author version - pagination differs from the published article**
tags: gpcr kinase transporter cofolding benchmark-only single-state binary-predicate continuous-metric design-level-oracle anti-memorization ligand-driven orthosteric peer-reviewed threat precedent negative-result comparator-numbers
stance: **threat** + precedent - target shuffling and binding-site mutation sometimes fail to change Boltz-2's output, on one of our four backbones. Adjacent to our shuffled arm; the answer is that we measure geometry, not an internal score. Sits alongside masters2025physics.

### chitsazi2025gpcrdock4 — 2025, bioRxiv preprint
claim: In a genuinely blind GPCR-ligand assessment, AF2-Multimer peptide co-folding drove all successes; small-molecule poses still lag 2010 results.
system/method: GPCR (5 complexes, 886 models, 45 groups) | benchmark-only + small assessor co-folding arm | AF2/AF2-Multimer, RoseTTAFold, RosettaCM/MODELLER; assessors ran AF3, Boltz-1, Chai-1, NeuralPLexer
states: one per submitted model (up to 5 per target) | metric: RMSD-to-reference + continuous (ligand heavy-atom RMSD, receptor fold), never a conformational state | prospective: partial (assessment yes, assessor AF3 arm no)
oracle: routes 5,6 by design (post-hoc RMSD); route 7 only in retrospective assessor arm; participants fully blind
figs: 11 panel-group rows; ND licence
tags: gpcr benchmark-only cofolding multi-backbone state-annotated-input single-state continuous-metric saturating-metric prospective anti-memorization unpowered confidence-as-discriminator peptide-driven apo-sampling orthosteric preprint precedent background comparator-numbers
stance: precedent + background — the corpus's only blind, prospective GPCR-ligand assessment

### ekstromkelvinius2024discriminator — 2024, AISTATS (PMLR 238:3403-3411), peer-reviewed
claim: Discriminator guidance transfers to discrete autoregressive diffusion; an optimal discriminator gives exact sampling, and SMC variants handle a suboptimal one.
system/method: 2-D molecular graphs, QM9 + MOSES (NOT protein, NOT 3-D) | inference-time discriminator guidance + SMC | ARDM; DiGress comparator
states: NOT APPLICABLE — generates graphs, no conformation | metric: NOT APPLICABLE for state (validity/uniqueness/novelty/FCD) | prospective: NOT APPLICABLE
oracle: routes 1,2,3,5,6,7 NOT APPLICABLE — no target structure; route 4 present, discriminator LR tuned on a validation set
figs: 1 figure + 8 tables (unusually figure-poor; nothing reusable for figure design)
tags: enhanced-sampling anti-memorization peer-reviewed background
stance: background — definitional source for discriminator guidance in DISCRETE diffusion; no system tag exists for a non-biomolecular paper, see note

### feldman2026alphainterp — 2026, bioRxiv preprint
claim: AF3's pair track, not the single track, is the causal geometric substrate; distances, contacts and confidence decode linearly from it.
system/method: general protein (400 monomers, SABmark, 46 fold-switch pairs) | linear probing + activation patching + MSA ablation | AF3 only
states: one (single diffusion sample per run) | metric: RMSD-to-reference + continuous (Kabsch Cα RMSD at annotated fold-switch indices) | prospective: partial
oracle: routes 4,6,7 — patching source and targets chosen by TM-score to reference; probe family picked on test metric
figs: 28 panel-group rows; ND licence
tags: general-protein fold-switching latent-steering msa-subsample no-template-no-msa single-state rmsd-only continuous-metric saturating-metric oracle-leak design-level-oracle anti-memorization preprint precedent contrast negative-result comparator-numbers
stance: precedent + contrast — mechanistic basis for trunk intervention; oracle sits inside causal experiment

### ferguson2026deorphann — 2026, bioRxiv preprint (Molecular Cell 2026)
claim: Active-state-biased AF-Multimer pair representations rank peptide agonists better than confidence metrics; two orphan GPCRs deorphanised and confirmed experimentally.
system/method: GPCR (peptide-activated, 20,035 experimentally labelled pairs) | co-folding + template-state-bias + supervised classifier | AF2/AF-Multimer via local ColabFold
states: two pipeline arms, single-state per run | metric: binary predicate (12.5 Å peptide-to-pocket cutoff); NONE for conformation | prospective: partial
oracle: routes 1,2,4,7 — AF-Multistate state-annotated active templates pinned in, thresholds fixed on evaluation set; routes 5,6 clean
figs: 30 panel-group rows
tags: gpcr cofolding template-state-bias msa-state-filter templates-on state-annotated-input single-state binary-predicate continuous-metric saturating-metric oracle-leak design-level-oracle prospective anti-memorization unpowered confidence-as-discriminator experimental-validation directed-state peptide-driven orthosteric preprint precedent contrast negative-result comparator-numbers
stance: precedent on findings + contrast on rigour — clearest template route to a directed active state

### georgiou2025heterogeneity — 2025, ACS Pharmacol. Transl. Sci. 8:3691–3728 (peer-reviewed review)
claim: Class A GPCRs are not two-state switches: apo receptors already occupy several inactive and active-region states on a rheostat continuum.
system/method: GPCR class A (4 receptors in depth) | narrative literature review | n/a
states: NOT APPLICABLE (review); asserts multistate ensemble/continuum, S1/S2/I1/I2/A per TM6 and TM7 | metric: NOT APPLICABLE; collates others' structural and NMR state criteria | prospective: NOT APPLICABLE
oracle: NOT APPLICABLE — no pipeline, no prediction, no scored outcome; all seven routes inapplicable
figs: 6 panel-group rows
tags: gpcr experimental ensemble continuum ligand-driven partner-driven g-protein-mimetic nanobody orthosteric allosteric-site peer-reviewed background comparator-numbers
stance: background — authoritative reference for state definitions and state-calling criteria
### gilson2025casp16 — 2025 (issued 2026), Proteins: Structure, Function, and Bioinformatics (Wiley), peer-reviewed
claim: best blind pose predictions were template-based; a non-blind AF3 baseline beat every blind entry; affinity stayed modest and structure-independent.
system/method: general protein (5 pharma targets, no GPCR/kinase) | benchmark-only + assessor-run co-folding/docking baselines | AF3, Boltz-1, RFAA, AutoDock Vina
states: one (single static complex per model) | metric: RMSD-to-reference + continuous, ligand pose only — receptor conformation deliberately unassessed | prospective: partial
oracle: routes 1,5,6,7 — two real leaks found and excised; 5/6 assessor-side post-seal; 7 baseline arm
figs: 12 panel-group rows
tags: general-protein benchmark-only cofolding multi-backbone templates-on single-state continuous-metric binary-predicate saturating-metric prospective anti-memorization unpowered confidence-as-discriminator design-level-oracle orthosteric peer-reviewed precedent background comparator-numbers
stance: precedent + background — rigorous blind-assessment design; no conformational-state handle

### heo2022multistate — 2022, Proteins: Structure, Function, and Bioinformatics (Wiley), peer-reviewed
claim: state-annotated GPCRdb templates plus total MSA deletion let an operator direct AF2 to either activation state at near-experimental accuracy.
system/method: GPCR (classes A, B1, B2, C, F) | template-biasing + MSA ablation | AF2, RoseTTAFold, MODELLER, AlphaFold-Multimer
states: two (one per operator-selected run) + ensemble side arm | metric: Cα TM-RMSD to reference + binary predicate; no geometric state criterion | prospective: partial
oracle: routes 1,2,4,5,7 present, 6 partial — state-annotated templates and MSA removal are the mechanism
figs: 9 panel-group rows; ND licence
tags: gpcr template-state-bias msa-state-filter templates-on state-annotated-input two-state single-state rmsd-only binary-predicate visual-metric saturating-metric oracle-leak design-level-oracle anti-memorization multi-backbone confidence-as-discriminator directed-state apo-sampling orthosteric peer-reviewed precedent contrast comparator-numbers
stance: precedent on method + contrast on rigour — state is instructed, not predicted

### hilger2020gcgr — 2020, Science, peer-reviewed
claim: in class B GCGR agonist binding alone produces no TM6 opening; the active state appears only on G-protein engagement.
system/method: GPCR (GCGR head-to-head with β2AR, 9-receptor kinetic panel) | experimental structural biology/biophysics + MD | n/a
states: NOT APPLICABLE — equilibrium displaced, nothing generated (1 cryo-EM structure; apo and agonist DEER indistinguishable) | metric: continuous coordinate + visual (DEER distances, kinetics) | prospective: NOT APPLICABLE
oracle: routes 1,7 — deposited starting models for cryo-EM refinement; design-level expectation contradicted by result
figs: 20 panel-group rows; no-reuse licence (Science 2020, all rights reserved)
tags: gpcr experimental md single-state continuous-metric visual-metric ligand-driven partner-driven nanobody apo-sampling orthosteric peer-reviewed precedent background comparator-numbers
stance: precedent on findings + background on method — agonist occupancy is not the active state

### ingraham2023chroma — 2023, Nature 623(7989):1070-1078, peer-reviewed (CC-BY)
claim: A programmable protein diffusion model samples novel structures and sequences and is steerable at sampling time by constraints including classifier and natural-language conditioning; 310 designs assayed.
system/method: general protein, de novo design (NOT conformational states) | generative diffusion + Bayesian conditioning | Chroma only; no co-folding comparison
states: NOT APPLICABLE - designs new proteins, never two states of one sequence | metric: backbone RMSD ~1.0 A to 2 solved designs | prospective: yes (310 characterised, no down-selection)
oracle: routes 1,2,3,5,6 NOT APPLICABLE; route 4 NOT EXTRACTED; route 7 mild and disclosed
figs: NOT EXTRACTED. **PARTIAL NOTE (schema_version v3-partial): Results and Methods never read, no PDF held.** Do not use for novelty or figure queries
tags: general-protein directed-state prospective experimental-validation peer-reviewed background
stance: background - the 2023 precedent that a protein diffusion model can be classifier-conditioned at sampling time; no receptor, no state, no co-folding

### jedryszek2026probing — 2026, preprint (arXiv)
claim: geometric concepts are linearly decodable in Boltz-1's trunk yet steering them barely moves output — decodability does not imply causal use.
system/method: general protein (486-protein evaluation set) | other — interpretability probes + sparse-autoencoder latent steering | Boltz-1
states: NOT APPLICABLE — no conformational states generated or sought | metric: DSSP-fraction shift (continuous) + steers/null verdict (binary) | prospective: partial
oracle: route 4 only — concepts filtered by evaluation-set score; routes 1,2,3,5,6,7 NONE FOUND
figs: 21 panel-group rows; licence NOT REPORTED (treat as all rights reserved)
tags: general-protein latent-steering single-state continuous-metric binary-predicate saturating-metric no-anti-memorization preprint precedent contrast negative-result comparator-numbers
stance: precedent on method + contrast on control — steers secondary structure, not conformational state

### jung2026boltzperturb — 2026, bioRxiv preprint
claim: Boltz-2 pose failure is a sampling failure, not missing knowledge; conditioning-tensor perturbations lift oracle success 19.3% to 26.3%.
system/method: general protein (57 post-cutoff RnP targets) | co-folding + latent steering (TCP on single, TBP on pair bias) | Boltz-2
states: ensemble + single-state — vanilla sampling collapses (ligand RMSF < 2.3 Å across 180 samples) | metric: ligand RMSD to deposited + binary success < 2 Å | prospective: no
oracle: routes 1,4,5,6,7 — noise scale tuned against the test set; oracle best-of-N is the headline metric
figs: 18 panel-group rows
tags: general-protein cofolding latent-steering msa-subsample ensemble single-state rmsd-only binary-predicate saturating-metric oracle-leak design-level-oracle anti-memorization unpowered confidence-as-discriminator orthosteric preprint threat precedent comparator-numbers
stance: threat on argument + precedent on findings — asserts correct basins pre-exist in the landscape

### junker2026peptidedesign — 2026, PLOS One 21(8):e0355549, peer-reviewed
claim: PAE confidence over-estimates for misplaced GPCR peptides in all three predictors, so confidence-first filtering cannot separate correct from incorrect placement.
system/method: GPCR (113 peptide/protein complexes, class A and B1) | benchmark-only (reproduction + generative design arms) | AF2-initial-guess, Boltz-2, RF3, BoltzGen
states: one receptor (template-imposed, identical across 50 seeds) + ensemble over seeds | metric: DockQ-family RMSD + borrowed category thresholds; receptor state never assessed | prospective: no
oracle: routes 1,4,5 present; 7 strong at design level — crystal receptors as input, seed budget tuned
figs: 12 panel-group rows
tags: gpcr benchmark-only cofolding templates-on single-state continuous-metric saturating-metric oracle-leak design-level-oracle anti-memorization confidence-as-discriminator multi-backbone seed-only orthosteric peer-reviewed precedent contrast negative-result comparator-numbers
stance: precedent + contrast — confidence fails on our system class; no state axis

### kalakoti2025afsample2 — 2025, Communications Biology 8:373 (Nature Portfolio), peer-reviewed
claim: replacing 15% of MSA columns with X inside AF2 improves alternate-state models on open/closed and transporter sets; the optimum is target-specific.
system/method: general protein + transporter + fold-switching (62 targets) | other — random MSA column masking at AF2 inference (nearest: enhanced sampling) | AF2 v2.3.1 only
states: ensemble (1,000 models/target) + two extracted end states | metric: TM-score to reference + threshold predicate + continuous open/closed coordinate | prospective: no
oracle: routes 4,5,6,7 — masking fraction tuned on the benchmark itself; best-of-1000 labelled by TM to reference
figs: 35 panel-group rows
tags: general-protein transporter fold-switching enhanced-sampling msa-subsample af-cluster ensemble two-state continuous-metric binary-predicate saturating-metric oracle-leak design-level-oracle no-anti-memorization unpowered confidence-as-discriminator seed-only peer-reviewed precedent contrast comparator-numbers
stance: precedent on findings + contrast on rigour — origin of column masking, tuned on evaluation set

### kalakoti2026afsample3 — 2026, bioRxiv preprint
claim: MSA-column masking transfers to AF3 (40% optimal) and a reference-free clustering selector recovers both states without any reference structure.
system/method: general protein (238 two-state Cfold targets) | MSA masking + clustering-based reference-free selection | AF2 and AF3 (AFsample2 v1.1, AFsample3 v1.0)
states: ensemble (1,000/target) + two end states plus an analysed intermediate population | metric: TM-score to reference + thresholds (TM > 0.8, ΔTM ≥ 0.05) | prospective: no
oracle: routes 4,5,6,7 — masking percentage and k tuned on the evaluation set; best-of-1000 versus deposited states
figs: 28 panel-group rows
tags: general-protein enhanced-sampling msa-subsample ensemble two-state continuous-metric binary-predicate saturating-metric oracle-leak design-level-oracle no-anti-memorization confidence-as-discriminator seed-only preprint precedent contrast comparator-numbers
stance: precedent on findings + contrast on rigour — closest reference-free selector; hyperparameters leak

### khaleq2026hyaline — 2026, bioRxiv preprint
claim: a Cα-graph EGNN with ESM3 embeddings classifies deposited GPCR structures as active or inactive at AuROC 0.99.
system/method: GPCR (classes A, B1, C, F; 1,590 structures) | other — supervised binary structure classifier / state predicate | n/a (ESM3-Open used only for embeddings)
states: NOT APPLICABLE — classifies, generates nothing (two implicit state classes) | metric: binary predicate (activation probability; decision threshold NOT REPORTED) | prospective: no
oracle: routes 1,2 by construction, 4 partial, 6,7 present — GPCRdb labels supervise; ambiguous cases purged
figs: 15 panel-group rows; ND licence
tags: gpcr binary-predicate saturating-metric anti-memorization design-level-oracle preprint precedent contrast comparator-numbers
stance: precedent + contrast — operational state predicate, but no family-level holdout

### kim2023refining — 2023, ICML, peer-reviewed
claim: A discriminator trained after the score network is frozen corrects the pre-trained score at sampling time and improves precision and recall together.
system/method: images only — CIFAR-10, CelebA, FFHQ, ImageNet 256 (NO protein anywhere) | inference-time score correction | EDM, LSGM, ADM, DiT-XL/2
states: NOT APPLICABLE | metric: NOT APPLICABLE for state (FID/sFID/IS/precision/recall) | prospective: NOT APPLICABLE
oracle: routes 1,2,3,5,6,7 NOT APPLICABLE; route 4 present — guidance weight, noise range and discriminator epoch swept on benchmark FID
figs: 51 figures, 10 tables; Fig 11 (loss contribution by noise scale, p8) is the one panel worth a second look
tags: peer-reviewed background
stance: background — definitional source for discriminator guidance in CONTINUOUS score-based diffusion; the discriminator separates real from generated, not one class from another

### kim2026mac1 — 2026, bioRxiv preprint
claim: co-folding places ligands accurately on 557 never-deposited Mac1 structures without memorisation, yet reproduces none of the receptor's conformational changes.
system/method: general protein (SARS-CoV-2 Mac1 pose arm; 3 unrelated screen targets) | benchmark-only (co-folding versus physics docking) + rescoring | AF3, Chai-1, Boltz-2, DOCK3.7
states: one per ligand; receptor does not move (global Cα RMSD 0.1–0.4 Å) | metric: ligand heavy-atom RMSD < 2 Å (binary) + RMSD-to-reference | prospective: partial
oracle: routes 4,5,6,7 — thresholds tuned on eval set, RMSD-to-crystal success, target chosen for known answer
figs: 30 panel-group rows
tags: general-protein gpcr cofolding benchmark-only multi-backbone single-state rmsd-only binary-predicate prospective anti-memorization design-level-oracle confidence-as-discriminator orthosteric ligand-driven preprint comparator-numbers precedent contrast
stance: precedent on findings + contrast on scope — strict temporal holdout; honest conformational null

### kohlhoff2014gpcr — 2014, Nature Chemistry 6(1):15-21, peer-reviewed (corrigendum Nat Chem 7:759, 2015)
claim: Two milliseconds of cloud-run beta2AR dynamics, aggregated by Markov state models, resolve activation pathways; agonist samples active-state conformations while inverse agonist and apo do not.
system/method: GPCR class A (beta2AR), 3 ligand conditions incl. apo | MD + Markov state models + Transition Path Theory | NOT APPLICABLE - no predictor run
states: ensemble + continuum | metric: continuous, four structural criteria simultaneously, no threshold | prospective: partial
oracle: routes 1-7 largely NOT APPLICABLE; route 7 design-level (beta2AR chosen for known endpoints and canonical ligands)
figs: Fig 1b-d only resolvable; SI to S22 not held. NO PDF HELD - read as NIH author manuscript, section locators only
tags: gpcr md enhanced-sampling af-cluster ensemble continuum continuous-metric ligand-driven apo-sampling orthosteric design-level-oracle peer-reviewed background precedent comparator-numbers
stance: background + precedent - canonical MD evidence for activation intermediates; NOTE its apo arm does NOT reach the active state, which must be reconciled with any apo prediction result

### krishna2024rfaa — 2024 (PDF is the 2023 bioRxiv preprint), Science
claim: one three-track all-atom network predicts protein/nucleic-acid/ligand/metal assemblies in a single pass and, fine-tuned, designs experimentally validated ligand binders.
system/method: general biomolecular assemblies | co-folding + generative design (RFdiffusionAA) | RFAA versus AF2, RF2, RFNA, DiffDock, Uni-Mol, DeepDock, TankBind, EquiBind, AutoDock Vina
states: one — deterministic single structure per input, no ensemble, no state sampling | metric: RMSD-to-reference (< 2 Å ligand, < 2.5 Å modification) + visual only | prospective: partial
oracle: routes 5,6,7 present; 1,4 partial — best-model labels assigned against the held reference
figs: 45 panel-group rows; ND licence
tags: general-protein cofolding templates-on single-state binary-predicate continuous-metric rmsd-only visual-metric oracle-leak design-level-oracle prospective anti-memorization confidence-as-discriminator multi-backbone experimental-validation ligand-driven preprint precedent background comparator-numbers
stance: precedent + background — reference non-DeepMind co-folding model; no conformational-state axis
### ku2026promise — 2026, bioRxiv preprint (PMLR/ICML footer)
claim: Five co-folding/emulator models recover all known states in only ~8-29% of clusters; collapse traced to the structure module, not the distogram.
system/method: general protein (PDB-wide, family-agnostic) | benchmark-only | AF3, Boltz-1, Boltz-2, Chai-1, BioEmu
states: ensemble + single-state | metric: binary predicate + TM/RMSD-to-reference, saturating | prospective: no
oracle: routes 3,5,6,7 design-level — both states deposited by construction, expected state declared first; no pipeline leak
figs: 22 panel-group rows
tags: general-protein benchmark-only multi-backbone md-emulator ensemble single-state binary-predicate continuous-metric rmsd-only saturating-metric design-level-oracle no-anti-memorization unpowered confidence-as-discriminator ligand-driven partner-driven apo-sampling orthosteric preprint precedent threat negative-result comparator-numbers
stance: precedent + threat — headline negative result constrains any multi-state claim

### lam2026metadiffusion — 2026, bioRxiv preprint
claim: A differentiable collective-variable bias added to frozen Boltz-2's denoiser converts a single-structure co-folder into a controllable ensemble generator without retraining.
system/method: general protein + nucleic acid + protein-ligand | other (inference-time gradient guidance) + enhanced-sampling on co-folding | Boltz-2
states: ensemble | metric: continuous coordinate + RMSD-to-reference + visual only | prospective: no
oracle: routes 1,2,3,6 absent; route 4 benign, route 5 partial, route 7 design-level present
figs: 15 panel-group rows
tags: general-protein periplasmic-binding cofolding enhanced-sampling ensemble continuous-metric visual-metric saturating-metric design-level-oracle no-anti-memorization directed-state preprint precedent contrast comparator-numbers
stance: precedent + contrast — cleanest inference-time steering precedent; rigour weaker

### lazou2026cryptic — 2026, Communications Biology 9:1010
claim: Supplying the cognate cryptic-site ligand shifts AF3 ensembles onto pocket-open; ligand-free runs give closed — ligand is a working directional handle.
system/method: general protein, cryptic pockets | benchmark-only on a co-folding backbone | AF3 only
states: ensemble + single-state | metric: binary predicate + RMSD-to-reference (half open-closed RMSD cutoff) | prospective: partial (no for 16-protein main set; partial for 8 post-cutoff)
oracle: routes 4,5,7 present, 6 partial — classification criterion amended for four proteins to match expectation
figs: 12 panel-group rows; ND licence
tags: general-protein kinase cofolding benchmark-only ensemble single-state binary-predicate rmsd-only saturating-metric oracle-leak design-level-oracle anti-memorization unpowered confidence-as-discriminator directed-state ligand-driven apo-sampling cryptic-pocket orthosteric peer-reviewed precedent contrast negative-result comparator-numbers
stance: precedent + contrast — peer-reviewed ligand-handle demonstration; criteria tuned post hoc

### lee2025seqassoc — 2025, Nature Communications 16:5622
claim: Random MSA subsampling below the coevolution threshold yields alternative fold-switcher conformations with ~6x less sampling; mechanism is sequence association, not coevolution.
system/method: general protein — fold-switching primary, transporters and periplasmic binding secondary | MSA-subsampling plus clustering of predicted structures | AF2 via ColabFold 1.5.5, AF3 comparator
states: ensemble + two-state | metric: TM/RMSD-to-reference + binary predicate + visual only | prospective: partial (E. coli blind arm only)
oracle: routes 4,5,6,7 present, 1-3 clean — leakage entirely in evaluation, stopping rules, target selection
figs: 18 panel-group rows
tags: general-protein fold-switching transporter periplasmic-binding msa-subsample no-template-no-msa state-annotated-input two-state ensemble continuous-metric binary-predicate visual-metric saturating-metric oracle-leak design-level-oracle prospective no-anti-memorization confidence-as-discriminator peer-reviewed precedent contrast comparator-numbers
stance: precedent + contrast — proteome-scale head-to-head win; stopping rules read the answer

### lee2026confornets — 2026, arXiv preprint
claim: A learned affine transform of AF3's pair representation before the Pairformer gives transferable directional state control, beating MSA and diffusion-guidance baselines.
system/method: GPCR, kinase, transporter, fold-switching, general protein | other — inference-time latent steering | OpenFold3-preview; AF3 server check, BioEmu comparator
states: ensemble + two-state + single-state | metric: RMSD-to-reference + binary predicate, coverage curves | prospective: no
oracle: routes 1,4,5,6,7 present — supervised transfer label IS a deposited target structure; route 3 clean
figs: 26 panel-group rows; licence NOT REPORTED (treat as all rights reserved)
tags: gpcr kinase transporter fold-switching general-protein latent-steering state-annotated-input ensemble two-state single-state rmsd-only binary-predicate continuous-metric saturating-metric oracle-leak design-level-oracle anti-memorization unpowered directed-state apo-sampling cryptic-pocket preprint precedent contrast comparator-numbers
stance: precedent + contrast — closest methodological competitor; oracle enters via training label

### lee2026foldswitch — 2026, Annual Review of Biomedical Data Science
claim: Deep models predict alternative folds by training-set association, not physics; CFold gave 0 of 1200 experimentally consistent fold-switch structures.
system/method: fold-switching (metamorphic) proteins | review/survey + small benchmark-only re-analysis | CFold run by authors; AF2/AF3/Chai-1/Boltz-2/ESM surveyed
states: two-state + single-state (Fig 3 arm only; NOT APPLICABLE for the review) | metric: continuous TM-score + visual only | prospective: no
oracle: routes 3,5,6,7 present, 1,2 none found — result is negative, so leakage is conservative
figs: 8 panel-group rows
tags: fold-switching general-protein af-cluster msa-subsample cofolding md enhanced-sampling md-emulator benchmark-only no-template-no-msa two-state single-state continuous-metric visual-metric design-level-oracle anti-memorization unpowered multi-backbone seed-only peer-reviewed contrast background negative-result comparator-numbers
stance: contrast + background — authoritative sceptical position plus best map of the territory

### lewis2025bioemu — 2025, bioRxiv preprint
claim: A sequence-conditioned diffusion model trained on ~208 ms of MD emits 300 K equilibrium ensembles to ~1 kcal/mol, orders of magnitude cheaper than MD.
system/method: general protein — soluble single chains at 300 K | other — MD-emulator diffusion (biomolecular emulator) | AlphaFold2 as frozen sequence encoder
states: ensemble + continuum | metric: RMSD-to-reference + binary predicate + continuous coordinate | prospective: no
oracle: routes 3,4,5,6,7 present but none at inference; routes 1,2 clean for the target's own structure
figs: 23 panel-group rows; ND licence
tags: general-protein kinase periplasmic-binding md-emulator ensemble continuum continuous-metric binary-predicate rmsd-only saturating-metric oracle-leak design-level-oracle anti-memorization unpowered apo-sampling cryptic-pocket preprint precedent contrast comparator-numbers
stance: precedent + contrast — reference quantitative-ensemble demonstration; scoring picks best against reference

### li2026embedding — 2026, arXiv preprint
claim: Gradient ascent on a diffusion model's conditioning embedding steers structure generation more robustly than coordinate guidance, holding across a 100x guidance-strength range.
system/method: general protein | other — inference-time latent steering of conditioning embedding | Protenix; Boltz-1 only under a published comparator
states: one | metric: binary predicate (restraint satisfaction) + continuous coordinate + RMSD-to-reference | prospective: partial (real experimental-map arm)
oracle: routes 1,4,5,6,7 present, structural in the synthetic arms; routes 2,3 none found
figs: 19 panel-group rows; licence NOT REPORTED (treat as all rights reserved)
tags: general-protein latent-steering single-state binary-predicate continuous-metric saturating-metric oracle-leak design-level-oracle no-anti-memorization directed-state preprint precedent contrast comparator-numbers
stance: precedent + contrast — direct methodological neighbour; synthetic arms are oracle-built

### liu2026ensembletests — 2026, bioRxiv preprint
claim: Ensemble-agreement metrics are invariant to frame shuffling, so no ensemble-level score can evidence learned dynamics; a kinetic layer recovers the signal.
system/method: general protein | benchmark-only + MD | NOT APPLICABLE — no prediction backbone; nine public conformational generators scored
states: ensemble + continuum | metric: continuous coordinate + binary predicate, four layers plus a gate | prospective: partial (Lockbox-36 selected after checkpoints fixed)
oracle: routes 1,2,3,5,6 clean; route 4 thresholds calibrated on eval data; route 7 declared in control arms
figs: 29 panel-group rows
tags: general-protein benchmark-only md md-emulator ensemble continuum binary-predicate continuous-metric saturating-metric oracle-leak prospective anti-memorization preprint threat background negative-result comparator-numbers
stance: threat + background — bars dynamics claims from ensemble-level agreement, but protects ensemble-only claims

### lu2026twostages — 2026, arXiv preprint (NeurIPS submission)
claim: ESMFold, OpenFold and Boltz-1 share one two-stage trunk: early blocks write biochemistry into the pair track, later blocks read geometry.
system/method: general protein | other — mechanistic interpretability (activation patching, linear probing, representation steering, cross-model alignment) | ESMFold, OpenFold, Boltz-1
states: NOT APPLICABLE — no conformational generator, one deterministic structure per condition | metric: binary predicate (DSSP motif) + continuous coordinate | prospective: no
oracle: routes 1-5 none found; route 6 genuine selection effect; route 7 design-level explicit
figs: 43 panel-group rows
tags: general-protein latent-steering single-state binary-predicate continuous-metric saturating-metric design-level-oracle no-anti-memorization multi-backbone directed-state preprint precedent contrast comparator-numbers
stance: precedent + contrast — cross-model trunk intervention transfers; motif scope stays local

### masters2025physics — 2025, Nature Communications 16:8854
claim: Co-folding models keep the crystallographic ligand pose after the pocket is made incapable of binding; MSA/template retrieval, not physics, drives placement.
system/method: general protein-ligand, CDK2 and MEK1 kinases | benchmark-only (adversarial) + enhanced sampling (funnel metadynamics) | AF3, RoseTTAFold All-Atom, Chai-1, Boltz-1
states: one | metric: binary predicate (ligand RMSD < 2 A) + RMSD-to-reference + visual only | prospective: no
oracle: routes 1,5,7 present, 2,3,4,6 none found — wild-type templates re-enter for mutated inputs, and that is the finding
figs: 8 panel-group rows
tags: kinase general-protein cofolding benchmark-only md enhanced-sampling templates-on single-state binary-predicate rmsd-only visual-metric saturating-metric oracle-leak design-level-oracle anti-memorization unpowered confidence-as-discriminator multi-backbone orthosteric peer-reviewed contrast threat negative-result comparator-numbers
stance: contrast + threat — ligand handle may be cosmetic; sets the adversarial control bar
### matic2023gpcrome — 2023, Nature Communications
claim: GPCR–G-protein interface contact fingerprints encode coupling specificity; AF-Multimer reproduces them ligand-free without ever verifying receptor state.
system/method: GPCR + heterotrimeric G protein | co-folding + benchmark-only + interface bioinformatics/Rosetta multistate design | AF-Multimer v2.3.1
states: one (5 models, best by AF ranking score) | metric: NOT REPORTED — no activation criterion defined anywhere | prospective: partial
oracle: routes 1,3,4,5,7 — templates-on, coupling-label-filtered contacts, thresholds and DockQ on references; 2,6 clean
figs: 30 panel-group rows
tags: gpcr cofolding benchmark-only templates-on single-state continuous-metric oracle-leak design-level-oracle no-anti-memorization confidence-as-discriminator experimental-validation partner-driven peer-reviewed background contrast comparator-numbers
stance: background + contrast — comparator source; 825 ligand-free models, state never verified

### mattsson2026leakage — 2026, bioRxiv preprint
claim: Sequence-identity splitting cannot stop affinity-benchmark leakage; a ligand-only model matches Boltz-2 on FEP+ 4, invalidating those comparisons.
system/method: general protein (kinase, GPCR arms) | benchmark-only + ligand-only ML leakage probe | Boltz-2 (two illustrative poses only)
states: NOT APPLICABLE — no conformational states generated | metric: NOT APPLICABLE — continuous Pearson r and MAE | prospective: no
oracle: route 7 only — case studies chosen because correlation known; no pipeline leakage
figs: 13 panel-group rows
tags: general-protein kinase gpcr benchmark-only continuous-metric saturating-metric anti-memorization design-level-oracle preprint threat precedent negative-result comparator-numbers
stance: threat + precedent — our split-based generalisation claims are directly exposed

### miglionico2026atlas — 2026, bioRxiv preprint
claim: Ligand-free AF3 co-folding of the whole GPCRome with all Gα subunits yields interfaces (median DockQ 0.73) that predict coupling.
system/method: GPCR + heterotrimeric G protein | co-folding + supervised ML (TabPFN "Precog3D") | AF3 v3.0.1
states: one (5 samples, seed 0, best ranking score) | metric: binary DockQ > 0.23 + visual plausibility; no state criterion | prospective: partial
oracle: routes 1,4,5,7 — date-fenced templates, threshold swept then changed, best-selected DockQ reference; 2,3,6 clean
figs: 33 panel-group rows; ND licence
tags: gpcr cofolding templates-on single-state binary-predicate continuous-metric visual-metric saturating-metric oracle-leak design-level-oracle prospective anti-memorization confidence-as-discriminator experimental-validation partner-driven preprint precedent contrast comparator-numbers
stance: precedent + contrast — largest AF3 GPCR run; state never verified

### migliorini2026pairsae — 2026, arXiv preprint (NeurIPS 2025 MLSB workshop)
claim: A shared sparse dictionary over Boltz-2's compressed pair+sequence representations decodes human-nameable structural concepts far better than ESM2 last-layer neurons.
system/method: general protein (protein–ligand, PLINDER) | other — sparse-autoencoder interpretability on co-folding activations | Boltz-2 (ESM2-650M probe baseline)
states: NOT APPLICABLE — no sampling, no state assignment | metric: NOT APPLICABLE — concept binary predicate, swept threshold | prospective: no
oracle: route 7 only — showcase systems chosen for known concepts; no pipeline leakage
figs: 13 panel-group rows; licence NOT REPORTED
tags: general-protein cofolding preprint anti-memorization background precedent
stance: background + precedent — no conformational content; precedent for pair-tensor concept legibility

### mitjavila2026afsample2t — 2026, Journal of Chemical Information and Modeling
claim: Masking MSA columns only around the orthosteric pocket captures 73.8% of experimental binding sites at 1.5 Å versus 60.7% for default AF2.
system/method: GPCR class A | other — targeted MSA column masking + retrospective virtual-screening benchmark | AF2 v2.3.1 and AF2-Multimer
states: two (receptor-alone inactive vs G-protein active) + ensemble pooled over 0/10/20/30% masking | metric: binding-site RMSD-to-reference, thresholds 1.0–2.0 Å | prospective: no
oracle: routes 1,4,5,7 — docking sites transferred from holo references, operating point tuned on evaluation set
figs: 10 panel-group rows
tags: gpcr msa-subsample two-state ensemble rmsd-only continuous-metric saturating-metric oracle-leak design-level-oracle no-anti-memorization unpowered directed-state partner-driven apo-sampling orthosteric peer-reviewed precedent contrast comparator-numbers
stance: precedent + contrast — closest spatially-targeted MSA masking precedent; operating point tuned on evaluation set

### nittinger2025cofolding — 2025, Artificial Intelligence in the Life Sciences 8:100136, peer-reviewed (CC BY-NC-ND)
claim: On a deliberately balanced set of matched orthosteric and allosteric ligands, co-folding places orthosteric ligands well and allosteric ones poorly, across three independent backbones.
system/method: general protein, 17 proteins with 40 ligands (20 orthosteric, 20 allosteric) | benchmark-only | NeuralPLexer, RoseTTAFold All-Atom, Boltz-1/1x. AF3 discussed, not run
states: single-state, ligand poses only - receptor conformation never assessed | metric: ligand-pose RMSD to reference + site identification | prospective: no
oracle: route 5 definitional, route 7 design-level; routes 1-4 and 6 NOT REPORTED (templates and MSA handling never described)
figs: NOT ENUMERATED. ND licence - redrawing forbidden
tags: general-protein kinase cofolding benchmark-only multi-backbone single-state rmsd-only binary-predicate design-level-oracle no-anti-memorization ligand-driven orthosteric allosteric-site allosteric-failure peer-reviewed precedent contrast negative-result
stance: precedent + contrast - the cleanest matched orthosteric-vs-allosteric design in the corpus (same proteins, same models, only the site type varies). No GPCR, no conformational axis. Note is thin: cite for the design, not for a number.

### obendorf2026statespecific — 2026, bioRxiv preprint
claim: Ligand placement is accurate but decoupled from global conformational state; state-annotated templates and state-filtered MSAs fail to enforce a state.
system/method: kinase + GPCR class A | benchmark-only, with template-state-bias and MSA-state-filter treatment arms | AF3 v3.0.1, Boltz-2 v2.2.0, Chai-1 v0.6.1, RoseTTAFold3
states: one per prediction (5 diffusion samples, single seed); two-state coverage only across conditions | metric: RMSD-to-reference plus visual marker calls by eye, no rule | prospective: partial
oracle: six routes — GPCRdb/KLIFS-driven MSAs, Kincore state-partitioned templates, RMSD and best/worst labels against held reference
figs: 8 panel-group rows; ND licence
tags: kinase gpcr cofolding msa-state-filter template-state-bias benchmark-only single-state binary-predicate rmsd-only saturating-metric oracle-leak no-anti-memorization unpowered confidence-as-discriminator multi-backbone ligand-driven orthosteric allosteric-site cryptic-pocket preprint precedent contrast negative-result comparator-numbers
stance: precedent + contrast — documents the decoupling; state calls visual, unblinded, n=7

### paajanen2026activation — 2026, bioRxiv preprint
claim: A learned PC1 index over 1351 class A structures shows apo and agonist-bound receptors are bimodal; only transducer binding locks active state.
system/method: GPCR class A | clustering + other (unsupervised PCA over deposited structures) | NOT APPLICABLE — no predictor run
states: NOT APPLICABLE — nothing generated; 1351 deposited structures partitioned two-state by 1-D GMM | metric: continuous G_CA coordinate + binary GMM cut at −1.72 ± 0.44 | prospective: partial
oracle: routes 2,4,6,7 — PC1 chosen because it separates labelled classes; anomalies adjudicated by eye
figs: 16 panel-group rows; no-reuse licence (all rights reserved, stricter than ND)
tags: gpcr experimental state-annotated-input two-state continuous-metric binary-predicate visual-metric oracle-leak design-level-oracle prospective anti-memorization orthosteric preprint precedent contrast comparator-numbers
stance: precedent + contrast — transducer-not-agonist evidence; index selected against the labels

### pandyszekeres2024gproteindb — 2024, Nucleic Acids Research (Database issue)
claim: 5,595 AF2-Multimer GPCR–G protein complexes released gated purely on self-confidence, with no state annotation and no validation against experimental structures.
system/method: GPCR + G protein | other (curated database resource) + production co-folding | AF2-Multimer v2.3.1
states: one per receptor–Gα pair; how many generated and the selection rule NOT REPORTED | metric: NOT REPORTED — no activation state assigned to any model | prospective: NOT APPLICABLE
oracle: routes 1,4,7 — templates-on to 2023, coupling threshold fitted to maximise agreement; 2,3,5,6 clean
figs: 9 panel-group rows
tags: gpcr cofolding templates-on single-state oracle-leak design-level-oracle no-anti-memorization confidence-as-discriminator partner-driven peer-reviewed background precedent comparator-numbers
stance: background + precedent — canonical coupling resource; precedent for unvalidated confidence-gated release

### parikh2026allosteric — 2026, bioRxiv preprint (submitted Cell Reports Physical Science)
claim: Five co-folding models all degrade roughly twofold on allosteric versus orthosteric sites; authors attribute it to frustration neutrality, not training data.
system/method: general protein + kinase | benchmark-only + other (local frustration analysis on experimental structures) | AF3, Protenix, Boltz-2, Chai-1, DynamicBind
states: ensemble of 25 predictions per complex, collapsed to best-by-RMSD | metric: symmetry-corrected ligand RMSD + pocket backbone RMSD, thresholded; unacknowledged visual component | prospective: no
oracle: routes 5,6 severe — best-of-25 selected by RMSD to reference; route 1 partial, route 7 design-level
figs: 12 panel-group rows; no-reuse licence (all rights reserved, stricter than ND)
tags: general-protein kinase benchmark-only cofolding multi-backbone templates-on ensemble single-state binary-predicate continuous-metric saturating-metric visual-metric oracle-leak design-level-oracle no-anti-memorization ligand-driven seed-only orthosteric allosteric-site cryptic-pocket allosteric-failure preprint precedent contrast negative-result comparator-numbers
stance: contrast + precedent — clearest large-n allosteric gap; measured between oracle-selected poses

### passaro2025boltz2 — 2025, bioRxiv preprint
claim: Boltz-2 approaches FEP-level affinity correlation at >1000× lower cost; structure accuracy only modestly beats Boltz-1 and still trails AF3.
system/method: general protein + kinase (also DNA/RNA, antibody) | co-folding + affinity head + inference-time physics steering | Boltz-2 vs AF3, Chai-1, Protenix, Boltz-1/1x
states: ensemble (MD-conditioned, 100 samples) + single-state default (5 samples, single seed) | metric: continuous lDDT/DockQ/RMSF plus binary predicates with unjustified thresholds | prospective: partial
oracle: routes 4,5,7 — calibration fitted on validation, RMSD-to-held-reference scoring, target chosen for known validator; 1,2,3,6 clean
figs: 23 panel-group rows
tags: general-protein kinase cofolding latent-steering ensemble single-state binary-predicate continuous-metric saturating-metric anti-memorization design-level-oracle prospective confidence-as-discriminator multi-backbone unpowered orthosteric preprint background precedent comparator-numbers
stance: background + precedent — backbone spec sheet; precedent for inference-time steering machinery

### protenix2025 — 2025, bioRxiv preprint
claim: A fully open from-scratch AF3 reproduction matches AF3 on ligand docking and nucleic acids; authors admit accuracy may partly reflect memorisation.
system/method: general biomolecular (protein, ligand, DNA, RNA) | co-folding, secondarily benchmark | Protenix vs AF3, AF2.3, RF2NA, AIchemy_RNA2
states: one ranked structure reported per target (25 generated; pool never treated as a conformational ensemble) | metric: NOT APPLICABLE — no conformational-state predicate defined | prospective: no
oracle: routes 5,6 only, evaluation-side and author-labelled; no pipeline leakage of target-state knowledge
figs: 11 panel-group rows
tags: general-protein cofolding single-state continuous-metric saturating-metric anti-memorization confidence-as-discriminator multi-backbone seed-only preprint background precedent comparator-numbers
stance: background + precedent — backbone origin paper; authors' own memorisation admission
### protenix2026v2 — 2026, bioRxiv preprint
claim: Antibody-antigen interface prediction gains 9-13 DockQ points over v1; zero-shot design yields BLI-confirmed hits on all 13 antigens including four GPCRs.
system/method: general biomolecular complexes, antibody-antigen + GPCR antigens | co-folding + generative binder design (TFG guidance) | Protenix-v2 vs Protenix-v1, AF3, Boltz-1/1x/2/2x, OpenFold3-preview2
states: one (ranked top-1 at 5 seeds) | metric: NOT APPLICABLE — no conformational state ever called | prospective: partial (design arm wet-lab; prediction arm retrospective)
oracle: no pipeline leak; route 7 design-level — availability-sampled panel, epitope rule fixed after an experimental result; route 1 unstated
figs: 14 panel-group rows; ND licence
tags: general-protein gpcr cofolding single-state binary-predicate saturating-metric design-level-oracle prospective anti-memorization unpowered confidence-as-discriminator multi-backbone experimental-validation preprint background contrast comparator-numbers
stance: background + contrast — capability report; state never modelled, single ranked structure per target

### purnomo2026cafe — 2026, bioRxiv preprint
claim: Co-folding pulls even minimal fragments into the canonical orthosteric pocket; co-folding a competitive blocker restores allosteric and cryptic site discovery.
system/method: five human kinases + PTP1B, KRAS | co-folding input intervention + alchemical MD (ABFE) | Boltz-2 only
states: ensemble (10 diffusion samples/fragment) + single-state — a ligand-placement ensemble, not a protein ensemble | metric: binary predicate (COM within 5.0 Å of reference ligand) + RMSD-to-reference; placement, not state | prospective: partial (chemistry and site prospective; targets, blocker, criteria retrospective)
oracle: routes 1,5,6 — blocker identity, success = distance to held references, ABFE pose selection; route 2 partial, 7 design-level
figs: 14 panel-group rows
tags: kinase general-protein cofolding md ensemble single-state binary-predicate continuous-metric saturating-metric oracle-leak design-level-oracle no-anti-memorization unpowered confidence-as-discriminator ligand-driven orthosteric allosteric-site cryptic-pocket allosteric-failure preprint precedent contrast negative-result comparator-numbers
stance: precedent + contrast — closest published inference-time steering by co-folded competitor; rigour caveats

### richman2025conformix — 2025, NeurIPS 2025, peer-reviewed (arXiv:2512.03312)
claim: Twisted SMC applied at inference time to a frozen Boltz-1 recovers deposited alternative conformations that default sampling never reaches, with no reference structure and no retraining.
system/method: general protein — domain motion (38), transporters (15), cryptic pockets (31), fold switching (15); NO GPCR, NO kinase | inference-time enhanced sampling (twisted SMC + guidance potentials + MBAR) | Boltz-1 primary, BioEmu second implementation
states: ensemble + continuum | metric: RMSD-to-reference + TM/fill-ratio + binary coverage (matching threshold NOT REPORTED) | prospective: no
oracle: routes 5,6,7 present — coverage scored to deposited references, best/worst-matched rows both oracle-selected; route 1 genuinely NONE FOUND, which is the paper's contribution; route 4 not determined
figs: 5 main + 11 supplementary panel groups; Table 1 best-matched row is at ceiling for 2 of 4 datasets including the unguided baseline
tags: general-protein transporter fold-switching cryptic-pocket cofolding enhanced-sampling md-emulator msa-subsample af-cluster ensemble continuum rmsd-only continuous-metric binary-predicate saturating-metric design-level-oracle oracle-leak no-anti-memorization multi-backbone directed-state confidence-as-discriminator peer-reviewed precedent contrast comparator-numbers
stance: precedent + contrast — cleanest route-1 answer in the corpus; but no receptor, no biological co-input, and an explicit admission that targets were "likely present in the Boltz training set" (p6)

### roehrig2026docking — 2026, bioRxiv preprint
claim: Co-folding beats docking only for training-similar complexes; physics-based docking wins in the low-similarity regime, with the receptor and site given.
system/method: general protein-ligand complexes (post-cutoff PDB, RNP/RNP-F) | benchmark-only + physics-based docking | AlphaFold 3 only, predictions imported from RNP
states: one (rigid receptor; ligand poses only) | metric: binary predicate (RMSD <= 2 A and LDDT-PLI > 0.8; also 1.0/1.5 A) + continuous coordinate | prospective: no
oracle: routes 1,5,6 — docking receptor and site are the answer's own, disclosed as an upper bound; 7 design-level
figs: 7 panel-group rows
tags: general-protein cofolding benchmark-only single-state binary-predicate continuous-metric oracle-leak design-level-oracle anti-memorization preprint contrast precedent negative-result comparator-numbers
stance: contrast + precedent — strongest corpus statement that co-folding's edge vanishes off-distribution

### schafer2025confounds — 2025 (PDF posted 2024), bioRxiv preprint
claim: AF-cluster is no better than random shallow-MSA subsampling at fold-switch prediction, its mechanism unsupported, and it confidently calls single folders metamorphic.
system/method: fold-switching / metamorphic globular proteins (KaiB, Mad2, RfaH) | MSA-subsampling (CF-random) + benchmark-only rebuttal | AF2 only, via ColabFold 1.5.3
states: ensemble + two | metric: RMSD-to-reference (all-atom, to both endpoints) + binary predicate + visual | prospective: no
oracle: routes 4,5,6 pipeline — MSA depth tuned on reference-scored results, success and best-model calls vs held references; 7 design-level
figs: 4 panel-group rows
tags: general-protein fold-switching msa-subsample af-cluster benchmark-only ensemble two-state binary-predicate continuous-metric visual-metric saturating-metric oracle-leak design-level-oracle confidence-as-discriminator anti-memorization unpowered preprint precedent contrast negative-result comparator-numbers
stance: precedent + contrast — reusable negative-control design; plDDT shown non-discriminating for state

### singh2026moredata — 2026, Current Opinion in Structural Biology 98 (peer-reviewed)
claim: Data, not architecture, is the bottleneck; benchmarks leak into training sets and current models largely memorize rather than generalize.
system/method: general protein (small-molecule drug targets) | other — perspective/opinion piece, no method of its own | none run (AlphaFold, Boltz-2 discussed; Fig 4 re-presented from ref [67])
states: NOT APPLICABLE — nothing generated | metric: NOT APPLICABLE — no conformational state scored | prospective: NOT APPLICABLE for the piece; partial for the re-presented Fig 4 (affinity arm prospective, pose arm not)
oracle: NOT APPLICABLE — no pipeline; route 7 weakly, viral families chosen by known data situation
figs: 7 panel-group rows; licence NOT REPORTED (treat as all rights reserved)
tags: general-protein experimental continuous-metric visual-metric saturating-metric prospective anti-memorization unpowered design-level-oracle peer-reviewed background contrast negative-result comparator-numbers
stance: background + contrast — canonical data-bottleneck framing; sets rigour demands our claims must meet

### singhal2025fksteering — 2025, ICML 2025 (poster), peer-reviewed (arXiv:2501.06848)
claim: Feynman-Kac interacting-particle steering redirects a frozen diffusion model with any reward at inference time, letting a 0.8B model beat a 2.6B fine-tuned one on prompt fidelity.
system/method: images and text ONLY — no protein, no structure, no molecule is generated or evaluated | inference-time particle steering (reward as particle weight, gradient-free) | Stable Diffusion family + discrete text diffusion
states: NOT APPLICABLE | metric: NOT APPLICABLE for state (GenEval/ImageReward/HPS/perplexity/toxicity) | prospective: NOT APPLICABLE
oracle: routes 1,2,3,5,6,7 NOT APPLICABLE — no target structure; route-4 analogue present (potentials and schedules compared on the reporting benchmarks)
figs: 9 figures + 11 tables; Fig 5 (p15) correlates intermediate-state reward with final-state reward, the direct analogue of a readability-vs-noise curve
tags: peer-reviewed background
stance: background ONLY — cite for the mechanism's existence and provenance. It is routinely cited as steering precedent for structure models; that citation is correct about the algorithm and false about the evidence.

### skrinjar2026generalization — 2026 (preprint posted 2025), bioRxiv preprint
claim: Co-folding accuracy rises monotonically with training-set similarity: 8-25% success in the least-similar stratum versus 81-89% in the most-similar; ranking near random.
system/method: general protein-ligand complexes, 2,600 post-cutoff systems | benchmark-only | six co-folding methods plus one non-co-folding baseline, seven arms (AF3 v3.0.0 templates-on among them)
states: ensemble (25 models/system) + single-state (top-ranked reported) | metric: continuous coordinate (ligand RMSD, LDDT-PLI, LDDT-LP, pocket F1) + binary predicate | prospective: partial (predictions post-cutoff; analysis retrospective)
oracle: routes 1,4,5,6 — AF3 templates on, per-method iPTM thresholds, success and best/worst curves set against references
figs: 22 panel-group rows
tags: general-protein cofolding benchmark-only templates-on single-state ensemble continuous-metric binary-predicate saturating-metric anti-memorization multi-backbone confidence-as-discriminator prospective oracle-leak seed-only preprint precedent threat negative-result comparator-numbers
stance: precedent + threat — reference anti-memorisation design; occupies ground our generalisation claims need

### stein2022speachaf — 2022, PLOS Computational Biology 18(8):e1010483 (peer-reviewed)
claim: In-silico alanine mutagenesis of MSA columns makes AF2 emit alternative conformations spanning both deposited endpoints for 11 of 12 membrane proteins.
system/method: transporters, GPCRs, one periplasmic-binding protein, one NMP kinase | other — MSA in-silico alanine mutagenesis (column-wise substitution) | AF2 only, via ColabFold, params v2.1
states: ensemble (300-420 models/target) + two | metric: TM-score-to-reference + continuous coordinate + visual (the visual call decides the headline) | prospective: partial (inputs and 8-protein arm temporally clean; adjudication and target choice retrospective)
oracle: routes 4,5,6,7 — inputs genuinely oracle-free; filtering, TM adjudication and target selection use held structures
figs: 15 panel-group rows
tags: transporter gpcr periplasmic-binding general-protein ensemble two-state continuous-metric visual-metric oracle-leak design-level-oracle anti-memorization unpowered directed-state apo-sampling seed-only peer-reviewed precedent contrast comparator-numbers
stance: precedent + contrast — earliest MSA-manipulation method; template-free, no deposited structure enters input

### sun2026kinconfbench — 2026, bioRxiv preprint
claim: Cofolding models reach only 65-75% kinase state accuracy, ensembles mode-collapse, geometric metrics don't predict state, and holo predictions drift apo.
system/method: human protein kinase catalytic domains, 2,225 chains | benchmark-only | Boltz-2, Chai-1, Protenix (multi-backbone)
states: ensemble (N=20 samples/target) + single-state (mode collapse is the result) | metric: binary predicate (exact 8-of-8 KinCoRe label match) + continuous coordinate; RMSD as pre-filter | prospective: no
oracle: routes 3,4,5,6 — KinCoRe cluster labels at construction, reference-scored success and best-model calls; 7 design-level
figs: 8 panel-group rows
tags: kinase cofolding benchmark-only multi-backbone ensemble single-state binary-predicate continuous-metric saturating-metric oracle-leak design-level-oracle anti-memorization unpowered confidence-as-discriminator ligand-driven seed-only apo-sampling orthosteric preprint precedent background negative-result comparator-numbers
stance: precedent + background — documents the exact failure triad a conformational-control method must fix

### suzuki2026conforflux — 2026, bioRxiv preprint
claim: Trunk-embedding repulsion guidance broadens Boltz-2 coverage without retraining, but fold switching plateaus near 60% across every inference-time method tested.
system/method: general protein + membrane transporters (ConforMix, 121 rows) | other — inference-time trunk latent particle guidance | Boltz-2 v2.2.1 modified; Boltz-1, BioEmu, MSA baselines
states: ensemble (500 samples/target) + two | metric: binary per-state success at category-specific thresholds (2.0 A domain/transporter) + continuous worst-case Ca RMSD, fill ratio, DAT mechanism distances | prospective: no
oracle: routes 4,5,6,7 — hyperparameters tuned on evaluation targets, best-of-500 against deposited references, targets chosen for two known states
figs: 22 panel-group rows
tags: general-protein transporter fold-switching cryptic-pocket latent-steering msa-subsample af-cluster md-emulator ensemble two-state binary-predicate continuous-metric saturating-metric oracle-leak design-level-oracle anti-memorization preprint precedent contrast negative-result comparator-numbers
stance: precedent + contrast — nearest inference-time internal-tensor intervention; no held-out tuning split

### suzuki2026pairscaling — 2026, bioRxiv preprint
claim: A single scalar on Boltz-2's pair representation steers ensemble breadth predictably, raising dual-state recovery over vanilla inference with inputs and weights untouched.
system/method: general protein + transporters (OC23, TP16, MS15; 58 targets) | other — inference-time pair-representation scaling; MSA-subsample/mask/cluster baselines | Boltz-2 v2.1.1 modified, AF3 Server as reference
states: ensemble (500 models/target) + two | metric: continuous TM-score to both references, best-minimum TM, fill ratio + binary predicate (TM >= 0.8 both states, threshold unjustified) | prospective: partial (beta applied blind; pLDDT-only selector arm)
oracle: R1-R6 — beta range tuned on the evaluation benchmarks, best-of-500 vs held references, explicit oracle-selector arm disclosed
figs: 18 panel-group rows
tags: general-protein transporter cofolding latent-steering msa-subsample af-cluster two-state ensemble continuous-metric binary-predicate saturating-metric oracle-leak no-anti-memorization confidence-as-discriminator preprint precedent contrast comparator-numbers
stance: precedent + contrast — direct architecture-internal steering precedent; no tuning split, no memorization control

### swapna2025memorization — 2025, PLOS Computational Biology 21(10):e1013590 (peer-reviewed)
claim: AF2/AF3 return the PDB-deposited SLC transporter state regardless of sampling intervention, flipping even a correct alternative-state template back to the memorized state.
system/method: SLC solute-carrier transporters (MFS and LeuT folds) | template-state-bias (ESMfold model of sequence-flipped virtual protein) + benchmark-only | AF2, AF3, ESMFold, MODELLER (multi-backbone)
states: two (proposed protocol) + single-state (every AF2/AF3 and enhanced-sampling arm) | metric: RMSD-to-reference (Ca RMSD, GDT) + visual only — the inward/outward call is never operationalised | prospective: partial (SLC35F2/F3 have no experimental structure; rest retrospective)
oracle: routes 4,5,6,7 — route 7 dominant, targets chosen for known deposited states; template is generated, not deposited
figs: 10 panel-group rows
tags: transporter template-state-bias msa-subsample enhanced-sampling benchmark-only templates-on state-annotated-input no-template-no-msa two-state single-state continuous-metric visual-metric saturating-metric oracle-leak design-level-oracle anti-memorization unpowered confidence-as-discriminator multi-backbone directed-state peer-reviewed precedent contrast negative-result comparator-numbers
stance: precedent + contrast — clearest memorization demonstration in a homogeneous transporter family; adds flip-back control
### tang2026steeraf — 2026, bioRxiv preprint
claim: Gradient ascent on AF2's MSA feature, steered by the model's own distogram, reaches alternative states without any reference structure.
system/method: general protein + transporter | other (distogram-gradient MSA-feature steering) | AF2/OpenFold; benchmark spans AF2, AF3, Boltz-2
states: ensemble + two (420 per target) | metric: TM/RMSD to reference + distance-PCA; predicate TM>0.85 AND RMSD<3.0 Å | prospective: partial
oracle: routes 4,5,6,7 — hyperparameters swept on eval set, best-of-N scored to held references; routes 1-3 clean
figs: 23 panel-group rows; ND licence
tags: transporter fold-switching general-protein gpcr latent-steering md templates-on ensemble two-state continuous-metric binary-predicate saturating-metric oracle-leak design-level-oracle no-anti-memorization multi-backbone preprint threat contrast comparator-numbers
stance: threat + contrast — adjacent competitor steering the distogram; rigour weak

### tejero2024opsin — 2024, Nature Communications 15:8928
claim: A bistable opsin uses canonical class A microswitches yet keeps its Schiff base protonated; TM6 movement tracks G-protein subtype.
system/method: GPCR (jumping-spider rhodopsin JSR1) | other — cryo-EM structure determination + functional assay | n/a
states: NOT APPLICABLE — equilibrium displaced, nothing generated | metric: continuous pocket/interface geometry + visual TM6 call | prospective: NOT APPLICABLE
oracle: NOT APPLICABLE, no prediction pipeline; route 7 only — experiment designed so active state is the answer
figs: 8 panel-group rows
tags: gpcr experimental single-state orthosteric directed-state ligand-driven partner-driven continuous-metric visual-metric design-level-oracle peer-reviewed precedent background comparator-numbers
stance: precedent + background — clean experimental active-state GPCR-G protein reference geometry

### tran2026nanogs — 2026, Angewandte Chemie Int. Ed. 65:e23510
claim: A stapled Gαs α5 peptide stabilises active-like β2AR and blocks cAMP, but only with orthosteric agonist present.
system/method: GPCR (β2AR; β1AR, D1R counter-screens) | other — stapled-peptide design + MD/metadynamics | n/a
states: two (inactive vs active-like equilibrium shift) + MD ensemble | metric: bimane λmax shift, no threshold; cAMP Emax/EC50 | prospective: yes
oracle: NOT APPLICABLE as leakage; design built on deposited β2AR-GαsCT structures (PDB 3SN6 and 6E67, which disagree on the R131 contact) and their prior MD - now recorded under structural_priors_used
figs: 16 panel-group rows
tags: gpcr experimental md enhanced-sampling two-state continuous-metric saturating-metric prospective directed-state peptide-driven ligand-driven g-protein-mimetic nanobody allosteric-site peer-reviewed precedent background
stance: precedent + background — wet-lab proof a peptide handle alone is insufficient

### vo2026fiducials — 2026, bioRxiv preprint
claim: Agonist alone drives β2AR TM6 nearly to the Gs-bound arrangement; co-folding models miss ligand-induced conformational change entirely.
system/method: GPCR (MRGPRX2, MC2R, V1AR, GIPR, β2AR) | other — fiducial design (RFdiffusion/ProteinMPNN) + cryoEM + MD + co-folding benchmark | AF2/ColabFold, AlphaFold-Multistate; OF3, Chai-1, Boltz-2 compared
states: ensemble of fiducial-target angles only; receptor states NOT APPLICABLE — determined by cryoEM | metric: visual TM6 state call + MD TM4-TM6 distance | prospective: partial
oracle: routes 1,2,4,7 present, 5 partial (co-folding scored to own new structures), 6 under-specified; route 3 none
figs: 8 panel-group rows; ND licence
tags: gpcr experimental cofolding md msa-subsample template-state-bias ensemble two-state visual-metric continuous-metric templates-on state-annotated-input prospective design-level-oracle unpowered confidence-as-discriminator multi-backbone experimental-validation ligand-driven partner-driven orthosteric preprint precedent contrast comparator-numbers
stance: precedent + contrast — new structures, but every state call made by eye

### wallner2023afsample — 2023, Bioinformatics 39(9) btad573
claim: Inference-time dropout with 6000 models per target lifts CASP15 multimer DockQ from 0.41 to 0.55, MSAs untouched.
system/method: general protein multimers (CASP15) | other — inference dropout + massive sampling | AlphaFold-Multimer v1/v2
states: ensemble (6000/target) collapsed to one reported model | metric: NOT APPLICABLE — DockQ quality score, no state predicate | prospective: yes
oracle: NONE FOUND — genuinely blind CASP15 submission with databases frozen before the season
figs: 4 panel-group rows
tags: general-protein enhanced-sampling templates-on ensemble single-state continuous-metric prospective anti-memorization unpowered confidence-as-discriminator seed-only peer-reviewed precedent contrast comparator-numbers
stance: precedent + contrast — origin of massive sampling; no conformational state defined

### waymentsteele2024cluster — 2024, Nature 625
claim: Clustering an MSA by edit distance makes AF2 sample both metamorphic states; NMR confirmed one prospective KaiB prediction.
system/method: general protein (fold-switchers) | MSA clustering (DBSCAN on edit distance) | AF2 via ColabFold
states: ensemble, one model per cluster, interpreted as two | metric: RMSD to reference with 3 Å predicate; TM-score in one arm | prospective: partial
oracle: routes 3,4 — success predicate and "top five" display both scored against held crystal structures; inputs clean
figs: 49 panel-group rows
tags: general-protein af-cluster msa-subsample two-state ensemble rmsd-only binary-predicate saturating-metric oracle-leak prospective no-anti-memorization confidence-as-discriminator peer-reviewed precedent contrast comparator-numbers
stance: precedent + contrast — origin of MSA clustering; 3 Å predicate unjustified

### waymentsteele2025reply — 2025, bioRxiv preprint
claim: Column shuffling destroys AF-Cluster's state-specific predictions, so local coevolution, not MSA depth alone, carries the signal.
system/method: general protein, fold-switching (KaiB, RfaH, Mad2) | clustering + benchmark-only | AF2 only, in DeepMind-notebook and ColabFold implementations
states: two + ensemble | metric: RMSD/TM to two deposited references, cutoffs set by inspecting models | prospective: no
oracle: routes 3,4,5,6,7 — displayed clusters and TM cutoffs chosen against known states; routes 1-2 clean
figs: 27 panel-group rows
tags: fold-switching general-protein af-cluster msa-subsample benchmark-only two-state ensemble continuous-metric binary-predicate visual-metric oracle-leak design-level-oracle anti-memorization unpowered preprint contrast background
stance: contrast + background — rebuttal; controls argued post hoc, not pre-specified

### wohlwend2024boltz1 — 2024, bioRxiv preprint
claim: Open co-folding model matches AF3 accuracy; inference-time steering raises PoseBusters validity 43% to 97% without accuracy loss.
system/method: general protein + ligands/nucleic acids | co-folding + inference-time steering | Boltz-1/Boltz-1x vs AlphaFold3 and Chai-1
states: one per prediction; 5 diffusion samples drawn, collapsed to top-1 | metric: NOT APPLICABLE — no conformational state scored | prospective: no
oracle: route 4 (hyperparameters swept on test set) and route 6 (oracle-of-5 reporting); no target state exists to leak
figs: 7 panel-group rows
tags: general-protein cofolding single-state continuous-metric binary-predicate saturating-metric anti-memorization multi-backbone preprint background precedent comparator-numbers
stance: background + precedent — origin document and definitional source for a backbone we use

### wu2023tds — 2023, NeurIPS 2023, peer-reviewed (arXiv:2306.17775)
claim: Twisted sequential Monte Carlo gives practical, asymptotically exact conditional sampling from an unconditional diffusion model, including on Riemannian protein backbones.
system/method: Gaussian simulation + ImageNet + protein motif-scaffolding (de novo design, NOT conformational state) | inference-time conditional sampling via SMC twisting | image diffusion; Riemannian protein backbone diffusion. NO co-folding model
states: NOT APPLICABLE for conformational state — scaffolds a fixed motif, never two states of one sequence | metric: designability/success-rate predicate (threshold NOT EXTRACTED) | prospective: no
oracle: route 4 present — particles, twist scale and motif rotations swept against benchmark success rate; route 7 design-level; route 5 NONE FOUND (success is self-consistency, not RMSD to a held answer)
figs: 3 figures + 1 table; Fig 3a is a single test case (5IUS)
tags: general-protein enhanced-sampling no-anti-memorization oracle-leak design-level-oracle peer-reviewed background
stance: background — algorithmic ancestor of richman2025conformix and the only SMC-family paper here with any protein arm; that arm designs backbones, it does not sample states

### yang2025statespecific — 2025, J. Chem. Inf. Model. 65:11425
claim: State-matched templates let a fine-tuned co-folding model rank designed peptides into agonists or antagonists; nanomolar hits assayed.
system/method: GPCR (class A and B) | co-folding + template biasing + inverse-folding peptide design + experimental validation | HelixFold-Multistate vs AF-Multimer, AF-Multistate, HF-Multimer
states: two (active- and inactive-conditioned, compared) then one retained | metric: DockQ/iRMS/TM-RMSD binary predicates + RMSD + visual | prospective: partial
oracle: routes 1,2,4,5,6,7 — state-matched templates at conditioning, deposited state annotation at evaluation; route 3 absent
figs: 21 panel-group rows; ND licence
tags: gpcr cofolding template-state-bias templates-on state-annotated-input two-state binary-predicate continuous-metric visual-metric saturating-metric oracle-leak design-level-oracle prospective anti-memorization confidence-as-discriminator experimental-validation directed-state orthosteric peer-reviewed precedent contrast comparator-numbers
stance: precedent + contrast — nearest peptide-state co-modelling; state is operator-supplied, not emergent

### ye2026multistatebias — 2026, bioRxiv preprint
claim: All four modern predictors collapse onto the PDB-dominant state; protein partners switch it decisively, small-molecule ligands barely do.
system/method: GPCR, transporter, general protein (β2AR, PfMATE, LAO, SecA) | benchmark-only + clustering/subsampling comparison arm | AlphaFold3, Boltz-2, Chai-1, BioEmu; AF2 inside AF-Cluster
states: ensemble per condition (20-50 samples) collapsing to one dominant basin | metric: Cα RMSD to paired references, diagonal side is the call; SecA distance/angle | prospective: no
oracle: routes 5,7 — post hoc RMSD scoring to held references, input conditions chosen with expected state declared
figs: 11 panel-group rows; ND licence
tags: gpcr transporter general-protein benchmark-only cofolding af-cluster msa-subsample ensemble single-state rmsd-only continuous-metric saturating-metric oracle-leak no-anti-memorization multi-backbone directed-state partner-driven ligand-driven apo-sampling orthosteric preprint precedent contrast negative-result comparator-numbers
stance: precedent + contrast — closest partner-drives-state result; four targets, no memorization control (n=4 could not have powered one). **Every partner arm supplies agonist AND heterotrimer together, so the partner's independent contribution is never isolated, and no reduced or scrambled partner is run** — that is the control our design supplies and theirs does not. See controls_run.

### yu2026domainmotion — 2026, PNAS 123(10):e2530709123, peer-reviewed (CC BY-NC-ND)
claim: AF3's open-vs-closed enzyme prediction is governed by the PDB apo:holo ratio, not by the ligand; nonbinder ligands induce nearly the same domain motion, and pLDDT cannot separate them.
system/method: general protein, 82 enzymes from DynDom, stratified by apo:holo ratio | benchmark-only, adversarial | AF3 primary, AF2 replication arm
states: ensemble + two-state (500 models per protein per condition, 100 seeds, NO templates) | metric: RMSD-to-reference in a 2D apo/holo coordinate, fixed domain aligned, nearest-reference rule, NO threshold; TM-score replication in SI | prospective: no
oracle: route 5 only (evaluation-side) + route 7 design-level. Routes 1,2,3,4,6 ALL CLEAN - no templates, defaults, uniform budget, full distributions not best-of-N
figs: 5 figures; Fig 5 is the non-binder arm and the best decoy-arm figure design in the corpus. ND licence, redrawing forbidden. NO PDF HELD - section locators only
tags: general-protein cofolding benchmark-only ensemble two-state rmsd-only continuous-metric no-template-no-msa design-level-oracle anti-memorization multi-backbone ligand-driven directed-state confidence-as-discriminator seed-only peer-reviewed threat precedent negative-result comparator-numbers
stance: **threat** + precedent - training-set prior (40.3%) is 3-4x the ligand effect (9.1-17.5%), and a NONBINDER ligand reproduces the conformational change. Directly exposes any decoy-arm interpretation. Belongs in the CLAIMS.md threats table.

### zhang2026generalization — 2026, npj Drug Discovery 3:30
claim: Boltz predicts GPCR backbones accurately (1.44 Å) but ligand poses poorly (5.95 Å); supplying the G protein does not fix poses.
system/method: GPCR (253 post-cutoff ligand-bound human receptors) | benchmark-only co-folding + physics refinement (Glide, IFD-MD, FEP+) | Boltz-1x primary, Boltz-2 as version arm
states: ensemble of 5 diffusion samples, collapsed to top-1 | metric: Cα and ligand RMSD to reference, every claim binarised at 2.5 Å | prospective: no
oracle: routes 5,6,7 — prediction step clean, but pose triage, docking boxes and best-model reporting are oracle-informed
figs: 7 panel-group rows
tags: gpcr cofolding benchmark-only md ensemble single-state rmsd-only saturating-metric oracle-leak design-level-oracle anti-memorization confidence-as-discriminator partner-driven orthosteric allosteric-site allosteric-failure peer-reviewed precedent threat negative-result comparator-numbers
stance: precedent + threat — independent partner result; threatens the confidence-score claim
