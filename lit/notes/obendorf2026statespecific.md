# obendorf2026statespecific

Schema v2 extraction. Every field present; `NOT REPORTED` where the paper does not say.

---

## A. Identity

- **citekey**: `obendorf2026statespecific`
- **doi**: 10.64898/2026.05.06.723350 (bioRxiv preprint, posted May 8, 2026) — p1
- **year**: 2026
- **venue**: bioRxiv preprint. Explicitly not peer reviewed: "this version posted May 8, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder" (p1). Tagged `preprint`.
- **title**: Assessing State-Specific Accuracy of Cofolding Models for Kinases and GPCRs
- **authors**: Leon Obendorf, Niklas Piet Doering (equal contribution), Petra Knaus, Gerhard Wolber (Freie Universität Berlin) — p1

## B. Scope

- **system**: kinase + GPCR (class A). Both, in one benchmark: "We benchmark four models, AlphaFold3, RosettaFold3, Boltz-2, and Chai-1, against a set of kinases and class A G protein-coupled receptors (GPCRs)" (p1).
- **n_targets**: 7 protein–ligand systems over 6 distinct proteins (p4, p9).
  - Kinases (4 systems, 3 proteins): LRRK2 + RN277 (type II, PDB 9DMI); PI3Kα-H1047R + Zovegalisib/RLY-2608 (type III, cryptic allosteric, PDB 8TSD); ALK2 + RK783 (type I, PDB 9L04); ALK2 + AMPPNP/ATP (PDB 6UNQ) — p4.
  - GPCRs (3 systems): 5-HT2A + pimavanserin, inactive (PDB 8ZMG); adenosine A2A + CGS21680, active (PDB 8UGW); δ-opioid receptor + ADL5859, G-protein-biased agonist, active (PDB 8Y45) — p9.
  - Flag: a 7-system benchmark supporting family-general claims ("establish conformational decoupling as a fundamental limitation of current cofolding approaches", p2).
- **method_class**: benchmark-only, with template-biasing and MSA-state-filtering arms applied as treatments. No new method is proposed; four existing cofolding backbones are evaluated under 21 input conditions (Fig 4A, p14; Methods pp20–23).
- **backbones**: AlphaFold3 v3.0.1, Boltz-2 v2.2.0, Chai-1 v0.6.1, RosettaFold-3 (commit b5c9685c7, `rf_latest.pt` downloaded 08.10.2025) — pp22–23. Four compared head to head → `multi-backbone`.
- **templates**: on / off / **state-annotated**, as an explicit experimental variable. "Custom templates were chosen by using the PDB structure files of the top four hits in each individual state-specific MSAs" (p21). Chai-1 additionally has a `server` template condition from the ColabFold MMseqs2 server (p21). RF3 templates were not used at all: "As RosettaFold-3 defines templating different than the other methods, templates were not considered" (p23).
- **msa_handling**: full (default/base pipeline), none ("no MSA"), and **state-filtered** ("biased MSA"). The biased MSAs are state-substituted alignments, not depth reductions: "Multiple sequence alignments (MSAs) of each sub-database containing one conformational state were subsequently produced using MMseqs2" (p21). Note the paper's own prose sometimes calls this "shallow MSAs" (p15) — the Methods make clear it is state filtering, and the two are not collapsed here.

## C. Conformational core

- **states_generated**: one state per prediction; two-state coverage only across conditions, never within a run. Five diffusion samples per condition from a single seed (p21) constitute the only within-condition sampling; the paper reports a single displayed model per condition (Fig 4A, p14). No ensemble or continuum is produced or claimed.

- **structural_priors_used**: **New in v3. Heavy, deliberate, and the paper's own subject — this field exists because of this paper.**
  1. **Every one of the seven systems was chosen from a recently solved deposited structure**, named on p4: kinases LRRK2 + type II RN277 (**9DMI**), PI3K H1047R + type III Zovegalisib in a cryptic pocket (**8TSD**), ALK2 + type I RK783 (**9L04**), ALK2 + AMPPNP (**6UNQ**); GPCRs 5-HT2A + pimavanserin (**8ZMG**, inactive), adenosine A2A + CGS21680 (**8UGW**, active), and δ-opioid with a G-protein-biased agonist (p9).
  2. **State annotations from two curated databases drive the biasing**, p4: *"Controlled template and MSA biasing strategies, informed by state annotations from KLIFS and GPCRdb, were applied throughout."* (Superscript reference numerals 7 and 6 sit inline after "KLIFS" and "GPCRdb" in the PDF text layer and are omitted here.) Protocol at p20: GPCR active and inactive structures *"were retrieved from the PDB as mmCIF files, based on their state annotations in the GPCRdb"*.
  3. **Custom templates are derived from those state-filtered alignments**, p21: *"Custom templates were chosen by using the PDB structure files of the top four hits in each individual state-specific MSAs."* The template set is therefore a function of the state label, not an independent input.
  4. **The biasing is deliberately generic rather than hand-tuned**, and the authors say why, p16: *"Because these methods are primarily intended for applications with limited prior structural knowledge, we adopted a general, database-driven biasing strategy based on state annotations from GPCRdb"*; p19: *"custom templates were selected automatically based on the MSAs generated from the state annotated databases, and no additional criteria were applied beyond this sequence and state information."* That restraint is a genuine methodological strength and should be credited when this paper is cited.

  **One internal tension worth carrying.** The design claim at p4 is that the benchmark spans *"distinct functional states absent from all model training sets, enabling prospective rather than retrospective evaluation."* But p15 concedes that one system was not absent: Boltz-2's best result came *"for which a closely related ligand was present in the training data (ALK2 with AMPPNP in PDB 6UNQ)."* The prospectivity claim holds for six of seven systems, not all seven, and anyone quoting the p4 sentence should quote the p15 one beside it.

- **oracle_leakage**: **PRESENT — six distinct routes.**

  1. **State annotations from curated databases drive the MSAs (GPCRdb, KLIFS).**
     "For GPCRs, active and inactive state structures were retrieved from the PDB as mmCIF files, based on their state annotations in the GPCRdb (https://gpcrdb.org/). For kinases, the entire KLIFS database (https://klifs.net/) was downloaded, representing the most comprehensive collection of human kinases." (p20)
     Also: "Controlled template and MSA biasing strategies, informed by state annotations from KLIFS and GPCRdb, were applied throughout." (p4)

  2. **Kincore state labels used to partition kinase structures into per-state sub-databases.**
     "PDB entries were sorted according to their conformational states, including DFG-out, DFG-inter, Active, C-Helix-out, and Salt-Bridge-out, using Kincore." (pp20–21)

  3. **Deposited structures used directly as templates, selected from the state-filtered alignments.**
     "Custom templates were chosen by using the PDB structure files of the top four hits in each individual state-specific MSAs." (p21)
     And, for Chai-1, template boundaries were set using KLIFS domain definitions: "Because the custom templates from KLIFs database consist only of the kinase domains, the subject start and end indices were set to the kinase domain boundaries (0-based)." (p23)

  4. **Success defined post hoc by RMSD to the held reference structure, after aligning to it.**
     "The generated cofolding structures were aligned to their corresponding crystal structure using PyMOL and protein RMSD was calculated simultaniously. For GPCRs, alignment and protein RMSD calculations were restricted to the folded receptor core to exclude highly flexible terminal and loop regions. Subsequently, the aligned complexes were saved as a PDB file. Ligand RMSD was evaluated with MDAnalysis based on the aligned PDB structures." (pp23–24)

  5. **Best/worst model labels assigned against the reference.**
     Fig 1 caption: "Superposition of all predicted RN277 ligand conformations (transparent) with the cryo-EM reference structure (PDB: 9DMI; yellow), highlighting the structurally closest (red) and farthest (blue) structure." (p6)
     Fig 3 caption: "Yellow indicates the reference PDB (ground truth), blue shows the best-performing model based on ligand RMSD, red shows the worst-performing model, and all other predictions are represented in grey." (p11)
     Fig 4 caption: "Blue bars: close to groundtruth predictions, darker blue showing the lowest ligand RMSD models. In magenta, the structurally most deviating model considering both ligand RMSD but also local pocket environment." (p14)

  6. **Knowledge of the target-state complex used to attempt steering in the allosteric case.**
     "Efforts to guide sampling, including blocking the ATP site sterically, introducing known protein interaction partners associated with the allosteric conformation, and using Boltz-2 binding contact flags to bias the ligand toward the cryptic pocket, did not lead to recovery of the allosteric site." (pp8–9)

  Adjacent (training-set overlap rather than pipeline leakage, recorded here because it bears on the same claim): "Based on its deposition date, 2019, this structure was likely present in all model training datasets." (p7, ALK2–AMPPNP 6UNQ); "This included the ATP example, for which a closely related ligand was present in the training data (ALK2 with AMPPNP in PDB 6UNQ)." (p15)

  Note in the paper's favour: the state biasing is class-level and automated, not target-specific hand curation — "we adopted a general, database-driven biasing strategy based on state annotations from GPCRdb and KLIFS rather than target-specific manual curation" (p16), and "custom templates were selected automatically based on the MSAs generated from the state annotated databases, and no additional criteria were applied beyond this sequence and state information" (p19). The leak is that the *target state to be recovered* is the state whose sub-database supplies the alignment and templates.

- **prospective**: **partial.** Prospective in target selection — six of the seven reference structures are recent and the authors claim "a benchmark of kinases and Class A GPCRs spanning distinct functional states absent from all model training sets, enabling prospective rather than retrospective evaluation" (p4). Retrospective in the biasing pipeline and in scoring: the state-specific sub-database that supplies the MSAs and templates is chosen to match the reference state (routes 1–3 above), best/worst is assigned against the reference (route 5), and one system (ALK2–AMPPNP, PDB 6UNQ, 2019) is stated to be inside the training sets (p7). The authors' own softer phrasing: "conditions that approximate realistic prospective use" (p16).

- **state_metric**: dual and asymmetric.
  - Quantitative: RMSD-to-reference — ligand RMSD (MDAnalysis, after alignment) and protein backbone RMSD (PyMOL, restricted to the folded receptor core for GPCRs) — pp23–24.
  - State recovery itself: **visual / binary predicate on named markers, judged by eye.** Kinases: orientation of the DYG-motif Y2018 in LRRK2 (p5, Fig 1B), outward rotation of P-loop Y219 in ALK2 (p7, Fig 1H), D354 rotation and the D354–R375 salt bridge (p7). GPCRs: ICL3 fold called "correct active-state", "inactive-like", or "hybrid" (p12). No numeric threshold, no rule, no justification is given for any of these calls: "This novel Y2018 orientation (Figure 1B) was recovered only in a subset of predictions" (p5); "Often, ICL3 adopted an inactive-like fold or a 'hybrid' configuration" (p12).
  - Thresholds quoted in the text are descriptive, not decision rules: "ligand RMSDs were general below 0.8 Å" (p5), "backbone RMSDs were generally below 1.5 Å" (p8), "backbone RMSD values exceeding 17 Å" for globally misfolded runs (p12). No justification is offered for any of these values.

- **metric_saturation**: **Yes, in two ways.**
  - Ligand RMSD floors for the orthosteric kinase systems: essentially all non-misfolded predictions fall in a narrow band (~0.4–1.4 Å), so the metric cannot separate conditions — the paper says this itself: "Across all three systems, low ligand RMSDs were also observed in models that differed in residue orientation and local interaction networks, indicating that accurate ligand placement can occur without recovery of the experimental binding-site geometry." (p7). Best-in-class differences are ~0.15 Å (0.42 vs 0.57 vs 0.58 Å; pp5, 7).
  - **Broken y-axis in Fig 4A** (p14, verified by rendering): each of the four sub-panels has a discontinuous RMSD axis with ticks at 0.5 / 1.0 / 1.5 and then a break to 10 / 20. The globally misfolded arms (>17 Å, p12) are compressed above the break, so the failures and the sub-Ångström band are not on a common scale.

- **directional_control**: Yes, weakly, and the paper's conclusion is that the handles do not reliably work. Named handles actually used:
  - **State-annotated templates** from KLIFS/GPCRdb/Kincore-partitioned PDB entries (p21).
  - **State-filtered MSAs** built per conformational state (p21).
  - **MSA presence/absence** ("no MSA" condition) as a strength knob (pp22–23).
  - **Ligand identity** as an implicit handle (the cofolding premise itself); found insufficient — "ligands exert only a modest influence on the global fold prediction and primarily shape the local environment of the binding pocket" (p18).
  - **Boltz-2 binding contact flags**, steric blocking of the ATP site, and known interaction partners (pp8–9) — all failed for the allosteric case.
  - Seed is fixed, not a handle: "the general inference settings were kept similar using one seed ('0') and five diffusion samples" (p21).
  - Verdict quoted: "Attempts to guide predictions through MSA editing or templating proved to be insufficient, especially for the active-state conformation" (p18).

- **anti_memorization_design**: **Partial, informal, undefined cutoff.** The benchmark is asserted to be post-training: "We curated a benchmark of kinases and Class A GPCRs spanning distinct functional states absent from all model training sets" (p4), and "For kinases, we selected structures that were recently solved" (p4). n = 6 systems intended as unseen (9DMI, 8TSD, 9L04, 8ZMG, 8UGW, 8Y45; p24) plus 1 deliberately-seen system (6UNQ, 2019). **No cutoff date is stated for any of the four models**, no per-model cutoff table, and no evidence is given for the "absent from all model training sets" assertion beyond deposition recency. The one leakage check that is made is by deposition date and hedged: "Based on its deposition date, 2019, this structure was likely present in all model training datasets." (p7)

- **anti_memorization_control**: **Effectively NONE RUN — UNPOWERED.** The seen system (ALK2–AMPPNP, 6UNQ) is included and commented on twice (p7, p15), but no seen-vs-unseen contrast is analysed: there is no arm, no grouped comparison, no statistic. The only mention of its performance is descriptive and confounded — "in two conditions Boltz-2 with base settings yielded the most accurate structure (for ALK2-ATP and Adenosie A2A Receptor). This included the ATP example, for which a closely related ligand was present in the training data (ALK2 with AMPPNP in PDB 6UNQ)." (p15) — which hints at memorization without testing it. n = 1 seen vs 6 unseen; both far below any powered comparison. Mark `UNPOWERED`.

- **controls_run**: **New in v3. The condition grid is the paper's real contribution, and v2 had nowhere to put it.**

| control | what it rules out | page |
|---|---|---|
| **Base settings** (each model's own MSA and template pipeline, unmodified) | that the biased arms are being compared against a strawman; it is the reference every other arm is read against | pp15, 21–22 |
| **State-specific (biased) MSA**, built from GPCRdb/KLIFS state annotations | that a state-filtered alignment is enough on its own | pp16, 20 |
| **Custom state-annotated templates**, top four hits per state-specific MSA | that state-annotated templates are enough on their own | p21 |
| **No MSA** (explicitly disabled, p22: *"The no MSA models were produced by explicitly disabling MSA usage, setting the MSA input to ”empty”."* — the original uses two closing typographic quotes around *empty*, reproduced here) | that the models are not simply reading the alignment | p22 |
| **No templates** | the symmetric question for templates | p22 |
| **No MSA + no templates** | that anything survives with both removed — it does not; backbone RMSD exceeds 17 Å (p12) | pp7, 12, 22 |
| **Four independent backbones** (AF3, Boltz-2, Chai-1, RF3) | that a result is one implementation's artefact | throughout |
| **Confidence validated against accuracy**, not merely reported | that pLDDT can be assumed informative. Protein pLDDT r = +0.04 against pose accuracy, ligand pLDDT r = −0.46 | p15 |
| **Both inhibitor-induced and nucleotide-bound kinase states** (6UNQ added *"to probe nucleotide recognition beyond inhibitor-induced states"*) | that the kinase result is specific to inhibitor chemistry | p4 |
| **ABSENT — seen-versus-unseen contrast** | memorization. 6UNQ is identified as seen and commented on twice, but no arm, grouped comparison or statistic tests it. n = 1 seen vs 6 unseen; unpowered even if run | pp7, 15 |
| **ABSENT — any state-recovery rate** | anything quantitative about state. State calls are made visually from renders, so the paper's central negative has no number attached to it | p14 |
| **ABSENT — replicate seeds or error bars** | sampling noise. Five diffusion samples from a single seed per condition, one pLDDT-selected model reported, n = 7 systems, no CIs on any panel | p21 |

  **Note the asymmetry between the grid and the conclusion.** The condition grid is genuinely well constructed and is the reason this paper is worth citing. The state conclusion drawn from it is not measured, only seen. Cite the grid; quote the conclusion as the authors' reading rather than as a rate.

- **confidence_as_discriminator**: **Yes, used, and — unusually — explicitly validated and partly refuted.** Used as a selection rule: Fig 4A shows "the lowest Protein pLDDt cofolding predictions" (p14) and per-residue profiles came "from the highest-mean-protein-pLDDT prediction of each method" (p24) — the two statements conflict; see `unresolved`. Validated against pose accuracy: "protein pLDDT showed no association with pose accuracy (Pearson r = +0.04, Figure 4B), whereas ligand pLDDT correlated moderately (r = -0.46, Figure 4C) indicating that local ligand confidence, but not overall fold quality, is informative for co-folding predictions" (p15). Critically, the validation is against **ligand pose accuracy only, never against state correctness** — the section is titled "Model confidence metrics do not report state fidelity" (p15) but no panel tests confidence against a state marker. RF3 excluded: "This analysis could not be performed for RF3, as the ligand pLDDT value in its outputs is fixed at 1.0" (p15).

## D. Claims

- **central_conclusion**: Cofolding models place orthosteric ligands well and remodel the local pocket around them, but that local accuracy is decoupled from recovery of the global conformational state — kinase state-marker residue orientations and GPCR intracellular (ICL3) geometry are frequently wrong even when ligand RMSD is sub-Ångström. State-annotated templates and state-filtered MSAs help in some cases and not others, and no model or condition recovers a cryptic allosteric pocket. AlphaFold3 is the most reliable of the four backbones.

- **necessity_claims** (verbatim + page):
  1. "When aiming to work with structural data of kinases or GPCRs in in silico investigations, it is crucial to model the correct state for the bound ligands." (p2)
  2. "Together, these studies show that state-aware prediction is achievable, but remains highly sensitive to careful manual template selection combined with MSA control rather than emerging robustly from the models themselves." (p3)
  3. "Heo and Feig demonstrated that state-annotated templates alone are insufficient when deep MSAs are present, whereas no or shallow MSA sampling allows templates to reliably enforce active and inactive GPCR states with near-experimental accuracy." (p3) — attributed to ref 5, not their own result.
  4. "These observations indicate that while cofolding reliably reproduces global protein architecture, it does not spontaneously sample cryptic or allosteric binding modes, even when guided." (p9)
  5. "However, it does not allow one to reliably infer the functional outcome of a ligand, since accurate modeling of the intracellular signaling interfaces is still largely beyond reach without additional structural guidance." (p12)
  6. "The limitation of relying solely on filtered template databases becomes evident here: these datasets are enriched for canonical conformations (DFG-in/out), constraining cofolding models to familiar structural states." (p17)
  7. "Attempts to guide predictions through MSA editing or templating proved to be insufficient, especially for the active-state conformation, as there seems to be a preference for ICL3 conformations resembling the inactive state." (p18)
  8. "Furthermore, conformational states that are rare, mutation-dependent, or only accessible through dynamic reorganization are not recovered without explicit conditioning." (p19)
  9. "Moreover, careful ligand selection is crucial, as cofolding performs rather robustly for orthosteric ligands, it tends to fail for allosteric binders, highlighting a current limitation that must be considered when interpreting the results." (p20)
  10. "The importance of the presence of either MSA or of biased templates becomes clear across systems as omitting MSAs and templates in AlphaFold3 and RosettaFold-3 results in globally misfolded structures with backbone RMSD values exceeding 17 Å and misplaced ligands (Figure 4A)." (p12)

- **novelty_claims** (verbatim + page):
  1. "Here we show that cofolding adaptively remodels binding pockets around bound ligands, but that this local accuracy is frequently decoupled from recovery of the broader conformational state." (p1)
  2. "These findings establish conformational decoupling as a fundamental limitation of current cofolding approaches, with direct implications for state-selective drug design." (p2)
  3. "Furthermore, while orthosteric ligand placement is generally reliable, allosteric binders expose a consistent blind spot across all models." (p2)
  4. "We curated a benchmark of kinases and Class A GPCRs spanning distinct functional states absent from all model training sets, enabling prospective rather than retrospective evaluation." (p4)
  5. "the LRRK2-RN277 reference PDB structure features an upward-oriented conformation of the DYG-motif tyrosine, a geometry not observed in PDB entries released before the 2025 cryo-EM structure." (p5) — novelty of the reference conformation, not of the method.
  - No claim to be *first* to benchmark cofolding state fidelity, and no priority language ("first", "unprecedented") anywhere about their own contribution. "first-in-class" on p8 refers to the compound RLY-2608, not to this work.

- **stated_limits**:
  - Template selection ignored ligand and functional context: "In this setup, custom templates were selected automatically based on the MSAs generated from the state annotated databases, and no additional criteria were applied beyond this sequence and state information. This meant that aspects such as ligand identity or functional context were not explicitly considered during template selection." (p19)
  - RF3 excluded from the confidence analysis: "This analysis could not be performed for RF3, as the ligand pLDDT value in its outputs is fixed at 1.0" (p15).
  - RF3 templating not tested at all (p23).
  - AF3 could not combine unbiased MSA with biased templates: "AlphaFold3 does not intend to combine an unbiased MSA with biased templates within one run, which is why we only generated 5 conditions for alphaFold3." (p22)
  - Flexible peripheral regions excluded from analysis: "per-residue pLDDT profiles were generally highest across the receptor core and decreased in flexible peripheral regions which we omitted in further analyses" (p18); GPCR RMSD "restricted to the folded receptor core" (pp23–24).
  - Structural-data sparsity confounds the GPCR result: "Intracellular loops, especially ICL3, are often unresolved in PDB structures due to their inherent flexibility. This lack of structural data may make accurate modeling more difficult." (p18)
  - Single seed, five diffusion samples (p21) — stated as a setting, not flagged as a limit.
  - NOT stated as a limit anywhere: the sample size (7 systems), the absence of a seen-vs-unseen control, or the visual/unblinded nature of the state calls.

- **stance** (PROVISIONAL — user's call): `precedent on findings + contrast on rigour`.
  - *precedent on findings*: independently documents ligand-placement/state decoupling across four backbones, the failure of state-annotated templates and state-filtered MSAs to enforce a state, the active-state GPCR pull toward inactive ICL3, and the allosteric blind spot — all directly supporting a gap argument (pp7, 9, 12, 18–19).
  - *contrast on rigour*: state calls are visual and unblinded with no threshold or rule; best/worst labels are assigned against the held reference; the state-biasing pipeline is fed by the very state annotation being tested; n = 7 systems, single seed; and six post-cutoff structures plus one known-in-training structure exist but are never run as a memorization control (pp7, 15, 21, 23–24).

## E. Quantitative comparators

### `metrics_reported`

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Ligand RMSD, LRRK2–RN277, successful predictions | "general below 0.8" | Å | PDB 9DMI reference, post-alignment | 5 |
| Ligand RMSD, lowest for LRRK2–RN277 (Chai-1, no-msa + custom templates) | 0.42 | Å | PDB 9DMI | 5 |
| Ligand RMSD, ALK2–RK783, successful predictions | "below 0.8" | Å | PDB 9L04 | 7 |
| Ligand RMSD, lowest for ALK2–RK783 (AF3, biased MSAs) | 0.57 | Å | PDB 9L04 | 7 |
| Ligand RMSD, ALK2–ATP, range across successful predictions | 0.58–1.40 | Å | PDB 6UNQ (AMPPNP) | 7 |
| Ligand RMSD, lowest for ALK2–ATP (Boltz-2, standard MSA, no templates) | 0.58 | Å | PDB 6UNQ | 7 |
| Protein backbone RMSD, ALK2–ATP successful predictions | "below 0.5" | Å | PDB 6UNQ | 7 |
| Protein backbone RMSD, PI3Kα–Zovegalisib | "generally below 1.5" | Å | PDB 8TSD | 8 |
| Protein backbone RMSD, AF3 and RF3 with no MSA and no templates | ">17" | Å | respective references | 12 |
| Pearson r, mean protein pLDDT vs ligand RMSD | +0.04 (n.s.) | correlation | all evaluated predictions, AF3/Boltz-2/Chai-1 (RF3 excluded) | 15, 14 |
| Pearson r, mean ligand pLDDT vs ligand RMSD | −0.46 | correlation | all evaluated predictions (RF3 excluded) | 15, 14 |
| Systems where biased AF3 input gave the closest-to-groundtruth model | 4 of 7 | count | ground-truth PDB structures | 15 |
| Systems where cofolding recovered the allosteric pocket | 0 of all models and settings | count | PDB 8TSD | 8 |
| Ranking of backbones by reliability | AF3 > Boltz-2 > RF3 > Chai-1 | ordinal, qualitative | ground-truth PDB structures | 15–16 |
| Boltz-2 best-model / worst-model counts | 2 best, 2 worst | count of systems | ground-truth PDB structures | 15 |

- **n_predictions**:
  - Samples per condition: 5 diffusion samples, 1 seed ("0") — "the general inference settings were kept similar using one seed ('0') and five diffusion samples" (p21).
  - Conditions per system: 21 total — AF3 5 ("we only generated 5 conditions for alphaFold3", p22), Boltz-2 6 ("models were generated using six different setups", p22), Chai-1 7 and RF3 3 (counted from the Fig 4A x-axis, p14; not stated in the Methods text).
  - Targets: 7 protein–ligand systems (4 kinase, 3 GPCR) — pp4, 9.
  - Total: **not reported by the authors.** Arithmetic from the above gives 21 × 5 = 105 predictions per system and 735 overall, but the paper never states a total, never says whether all 5 diffusion samples were analysed or only the pLDDT-selected one, and Fig 4A plots one model per condition. The analysed n behind Fig 4B/C is not given (several hundred points visible; RF3 present in the legend of the shared key despite the stated RF3 exclusion).

- **comparable_to_ours**: Comparable quantities, with caveats — (i) ligand RMSD to a held reference for orthosteric kinase and GPCR complexes, per backbone and per input condition (0.42–1.40 Å band, pp5, 7); (ii) protein backbone RMSD per condition, including the >17 Å collapse with no MSA and no templates (p12); (iii) pLDDT-vs-accuracy correlations (+0.04 protein, −0.46 ligand, p15); (iv) per-backbone reliability ranking across four cofolding models (pp15–16). **Hedges that must travel with any such comparison**: their RMSDs are for one pLDDT-selected model per condition, not a distribution; single seed; n = 7 systems with no error bars, no CIs and no per-system n on any panel; GPCR backbone RMSD is core-only, excluding the very loops the paper's state claim rests on; and their state calls are visual, so no state-recovery *rate* exists to compare against. Whether these sit beside our numbers is `NONE` until our metric definitions are matched against theirs.

- **si_in_scope**: **New in v3. SI NOT HELD, but for once that costs little.** The Supporting Information listing at p24 contains only *"S1 Per-Residue pLDDT of Cofolding Kinase Predictions"* and *"S2 Per-Residue pLDDT of Cofolding GPCR Predictions"* — per-residue confidence profiles, referenced once at p18 to justify trimming flexible peripheral regions from the analysis. **Every RMSD, correlation and per-condition result quoted in this note is in the main text.** The one thing the SI would settle is which peripheral residues were omitted and on what basis, which matters because the GPCR backbone RMSD is core-only and excludes the loops the state claim rests on.

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A,D,G | 6 | Superpositions of all predicted ligand conformations on the reference for LRRK2–RN277, ALK2–RK783 and ALK2–ATP, with closest and farthest models colour-flagged | structure render | `RENDER \| systems: 3 \| views: 1 (ligand overlay in binding site) \| overlay: all predictions on 1 reference each, best and worst highlighted \| axis: none` | 3 panels, varying by system (one kinase–ligand complex each) | Number of overlaid predictions not stated in the caption or text; best/worst are chosen against the reference, so the visual spread is post-hoc labelled; no quantitative panel accompanies the Y2018 recovery claim ("recovered only in a subset of predictions", p5 — the subset is never counted) | CC-BY-NC-ND 4.0 International (p1, on every page header). **ND clause: redrawing and modification are both forbidden; NC also bars commercial reuse.** |
| 1B-C,E-F,H | 6 | Close-ups of state-defining local geometry: DYG Y2018 orientation, RN277 ring deformation, D354 rotation / RK783 ethyl orientation vs Y219, and P-loop Y219 in the nucleotide pocket | structure render | `RENDER \| systems: 3 \| views: 5 (Y2018 stick close-up, RN277 ring conformation, RK783 pocket with D354, RK783 ethyl vs Y219 in reference, Y219 in nucleotide pocket) \| overlay: selected predictions on 1 reference each \| axis: none` | 5 panels, varying by view (local marker) rather than by condition | The paper's kinase state conclusions rest entirely on these eye-judged close-ups; no threshold, no count, no per-condition tabulation of which of the 21 conditions recovered each marker | as above (p1) |
| 2A-B | 8 | PI3Kα-H1047R with Zovegalisib: overall fold and ligand placement, all predictions vs the ground truth, showing every model in the ATP site rather than the cryptic allosteric pocket | structure render | `RENDER \| systems: 1 \| views: 2 (global PI3Kα fold, ligand placement with the allosteric pocket circled) \| overlay: all model predictions (grey) on 1 reference (yellow) \| axis: none` | 2 panels, varying by view (global fold, ligand site) | Predictions are pooled into an undifferentiated grey cloud — model and input condition are not distinguishable, so the "none of the predicted structures" claim (p8) cannot be checked per condition; no n on the panel | as above (p1) |
| 3A-C | 11 | Ligand conformations in three class A GPCRs (pimavanserin/5-HT2A, CGS21680/A2A, ADL5859/DOR), best and worst model highlighted against the reference | structure render | `RENDER \| systems: 3 \| views: 1 (orthosteric ligand pose) \| overlay: all predictions (grey) on 1 reference each, best (blue) and worst (red) by ligand RMSD \| axis: none` | 3 panels, varying by system (receptor–ligand pair) | Best/worst assigned by RMSD to the reference; the remaining predictions are pooled grey with no n | as above (p1) |
| 3D-F | 11 | ICL3 backbone conformations for the same three receptors, showing active-state receptors modelled with inactive-like or hybrid ICL3 | structure render | `RENDER \| systems: 3 \| views: 1 (ICL3 backbone) \| overlay: all predictions (grey) on 1 reference each, best and worst highlighted \| axis: none` | 3 panels, varying by system (inactive 5-HT2A, active A2A, active DOR) | **The paper's central GPCR claim has no quantitative panel anywhere** — "nearly all models failed to recover the correct active-state conformation" (p12) is supported only by these renders. No ICL3 RMSD, no per-condition table, no count; GPCR systems are absent from the Fig 4A bar panels entirely; n per panel not shown | as above (p1) |
| 4A | 14 | Protein backbone RMSD (bars) and ligand RMSD (dots) for the pLDDT-selected prediction of each backbone × MSA/template condition, for the four kinase systems | bar + overlaid point | `PLOT \| facet: kinase system (4) \| x: backbone × MSA/template condition (21) \| y: RMSD (Å) \| mark: bar (protein backbone RMSD) + overlaid point (ligand RMSD) \| n_per_cell: 1 displayed model, selected by pLDDT from 5 diffusion samples` | 4 panels, varying by system (ALK2–ATP, ALK2–RK783, LRRK2–RN277, PI3Kα–Zovegalisib); x groups by backbone (AF3 5, Boltz-2 6, Chai-1 7, RF3 3) with a templates ±/server row beneath | **Broken y-axis in every panel** (0.5/1.0/1.5, then a break to 10/20), which visually compresses the >17 Å global-misfold arms onto the same bar as sub-Ångström results; one bar per condition hides the 5-sample distribution entirely (no error bars, no strip); the three GPCR systems are missing from the only quantitative figure in the paper; colour encoding of "best"/"most deviating" is assigned against the ground truth | as above (p1) |
| 4B-C | 14 | Mean protein pLDDT vs ligand RMSD, and mean ligand pLDDT vs ligand RMSD, coloured by backbone with an overall trend line | scatter | `PLOT \| facet: confidence metric (2: mean protein pLDDT, mean ligand pLDDT) \| x: mean pLDDT (continuous, 70–100) \| y: ligand RMSD (Å) \| mark: point coloured by backbone (4) + overall trend line \| n_per_cell: NOT REPORTED (several hundred points; total n never stated)` | 2 panels, varying by which confidence metric is on x | n not stated on either panel; RosettaFold3 appears in the shared colour legend although the text says the ligand-pLDDT analysis "could not be performed for RF3" (p15); a single pooled trend line across four backbones and seven systems, so system and backbone effects are pooled away; confidence is tested against ligand RMSD only, never against a state marker, despite the section heading "Model confidence metrics do not report state fidelity" (p15) | as above (p1) |
| TOC | 31 | Graphical abstract: GPCRdb/KLIFS → state-specific MSAs and templates → four cofolding models → readouts (pocket conformation, orthosteric ligand challenge, ligand RMSD, conformational states, biased MSA/template importance) | schematic | `SCHEMATIC \| workflow from state-annotated databases through MSA/template biasing into four cofolding backbones and five evaluation readouts \| no data` | 1 panel | (blank — carries no result) | as above (p1) |

Supplementary figures S1 and S2 (per-residue pLDDT for kinase and GPCR predictions) are listed on p24 but are not contained in this PDF and were not catalogued.

## G. Provenance

- **extracted_on**: 2026-09-07; **re-passed to schema v3 on 2026-09-09**
- **extractor**: claude subagent
- **schema_version**: `v3` — re-passed 2026-09-09 against the PDF, not patched. **This was the pilot paper whose v2 extraction forced the v3 schema revision**, so it should not have been the last note still on v2. The three missing fields were extracted fresh and every added quote machine-verified; the A–E content of the v2 pass was checked and stands.
- **confidence**: **medium-high.** Text extraction was clean and the Methods are unusually explicit about the biasing pipeline, so B, C and D are solid. Lower confidence on E's `n_predictions` (the paper never states a total or whether all diffusion samples enter the analysis) and on the Fig 4A condition counts for Chai-1 (7) and RF3 (3), which were counted off the rendered x-axis rather than stated in the text. Fig 4A was the only page rendered; all other figure rows are from captions plus body text, which carried the panel structure adequately since Figs 1–3 are structure renders.
- **unresolved**:
  1. **pLDDT selection direction contradicts itself.** Fig 4A caption says the plotted models are "the lowest Protein pLDDt cofolding predictions" (p14) while the Methods say "Per-residue pLDDT profiles were generated from the highest-mean-protein-pLDDT prediction of each method" (p24). One of the two is a typo; which one determines whether Fig 4A shows the best or the worst of each condition's five samples. Not resolvable from the text.
  2. **Total number of predictions never stated**, and it is not said whether all 5 diffusion samples per condition were analysed or only the selected one. n for Fig 4B/C is not given.
  3. **RF3 in Fig 4B/C legend** despite p15 stating the ligand-pLDDT analysis could not be performed for RF3 (ligand pLDDT fixed at 1.0). Unclear whether RF3 points appear in B only, in both, or in neither.
  4. **Chai-1 and RF3 condition counts** are not stated in the Methods; taken from the figure axis.
  5. **No model training cutoff dates are given** for AF3, Boltz-2, Chai-1 or RF3, so the claim that the benchmark structures are "absent from all model training sets" (p4) cannot be verified from the paper.
  6. **No rule for the state calls.** "Correct active-state conformation", "inactive-like", "hybrid" ICL3 (p12) and Y2018/Y219 "recovered" (pp5, 7) are never operationalised, so no state-recovery rate can be extracted.
  7. **Tag needed but not in the v2 vocabulary**: there is no tag for *cofolding-specific* evaluation of state fidelity as distinct from `cofolding` as a method class (all four backbones here are cofolding models, so `cofolding` is technically correct but does not mark this as a benchmark *of* cofolding state fidelity). More importantly, there is no tag for **allosteric-blind-spot / failure-to-sample-non-canonical-site as a result**; `allosteric-site` and `cryptic-pocket` mark the site studied, not the negative finding, and `negative-result` is under "Relation to us" rather than a finding tag. Also missing: a tag for **visual-only / unblinded state assessment**, which is the paper's single biggest rigour issue and is not expressible — `rmsd-only` is wrong (they use both RMSD and eye) and there is no `visual-metric`. Not invented; recorded here.
- **why_it_matters**:

## Tags

`kinase` `gpcr` `cofolding` `msa-state-filter` `template-state-bias` `benchmark-only` `single-state` `binary-predicate` `rmsd-only` `saturating-metric` `oracle-leak` `no-anti-memorization` `unpowered` `confidence-as-discriminator` `multi-backbone` `ligand-driven` `orthosteric` `allosteric-site` `cryptic-pocket` `preprint` `precedent` `contrast` `negative-result` `comparator-numbers`

Tag notes: `single-state` because each run yields one conformation and states are covered only across conditions, never within a run. `binary-predicate` and `rmsd-only` are both listed because the paper uses two metrics — eye-judged marker predicates for state and RMSD-to-reference for placement; neither tag alone is accurate and there is no `visual-metric` tag. `prospective` is deliberately **not** applied: the paper claims it (p4) but the biasing pipeline and scoring are retrospective. `no-anti-memorization` applied rather than `anti-memorization` because a held-out set exists but no control arm was run. `ligand-driven` because ligand identity is the implicit state handle under test; `directed-state` is not applied since the directional handles demonstrably failed (p18).
