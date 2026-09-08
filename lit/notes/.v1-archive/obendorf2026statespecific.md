# obendorf2026statespecific

## A. Identity

- **citekey**: `obendorf2026statespecific`
- **doi**: 10.64898/2026.05.06.723350 (bioRxiv preprint, posted May 8, 2026; "not certified by peer review", p.1)
- **year**: 2026
- **venue**: bioRxiv preprint. **Preprint — not peer reviewed** (stated on every page banner, p.1). Licence CC-BY-NC-ND 4.0.
- **title**: Assessing State-Specific Accuracy of Cofolding Models for Kinases and GPCRs
- **authors**: Leon Obendorf, Niklas Piet Doering (equal contribution), Petra Knaus, Gerhard Wolber — Freie Universität Berlin (p.1)

## B. Scope

- **system**: kinase + GPCR (class A). Both families in one benchmark. (p.1, p.4)
- **n_targets**: 7 protein–ligand systems across 6 distinct proteins (p.4, p.9):
  - Kinases (4 complexes, 3 proteins): LRRK2 + type II inhibitor RN277 (PDB 9DMI); PI3Kα-H1047R + type III allosteric inhibitor Zovegalisib/RLY-2608 (PDB 8TSD); ALK2 + type I inhibitor RK783 (PDB 9L04); ALK2 + AMPPNP/ATP (PDB 6UNQ).
  - Class A GPCRs (3): 5-HT2A + pimavanserin, inactive (PDB 8ZMG); adenosine A2A + CGS21680, active (PDB 8UGW); δ-opioid receptor + G-protein-biased agonist ADL5859, active (PDB 8Y45).
  - Flag: a 7-system benchmark that carries a general claim ("establish conformational decoupling as a fundamental limitation of current cofolding approaches", p.2).
- **method_class**: benchmark-only (cofolding benchmark). No new method is proposed; existing template-filtering and MSA-biasing strategies are applied as input conditions. (p.4, p.16)
- **backbones**: AlphaFold3 (v3.0.1), Boltz-2 (v2.2.0), Chai-1 (v0.6.1), RosettaFold-3 (commit b5c9685c7, `rf_latest.pt` downloaded 08.10.2025). Four backbones. (pp.22–23)
- **templates**: **on and off, as an experimental variable.** Conditions include no-template and custom state-annotated templates ("the top four hits in each individual state-specific MSAs", p.21). Chai-1 additionally has a template-server mode (p.21). RF3 templates were **not** used: "As RosettaFold-3 defines templating different than the other methods, templates were not considered." (p.23)
- **msa_handling**: **full / none / state-filtered ("biased"), as an experimental variable.** Three MSA regimes per model: (a) base/default MSA (AF3 internal Jackhmmer/Nhmmer pipeline; Boltz-2 and Chai-1 via ColabFold MMseqs2 server; RF3 via standalone ColabFold), (b) no MSA (empty), (c) "biased MSA" = MMseqs2 alignment built from a state-annotated sub-database (GPCRdb state annotations for GPCRs; full KLIFS database sorted by Kincore conformational state for kinases). (pp.20–23). This is **not** depth-subsampling or clustering — it is substitution of a state-filtered sequence set.
  - Condition counts (stated / read from Fig 4A, p.14): AF3 5 conditions ("AlphaFold3 does not intend to combine an unbiased MSA with biased templates within one run, which is why we only generated 5 conditions for alphaFold3", p.22), Boltz-2 6 ("six different setups", p.22), Chai-1 6 (from Fig 4A), RF3 3 (from Fig 4A) = 20 conditions per system.

## C. Conformational core

- **states_generated**: **one** (per condition). Each run uses a single seed ("0") and five diffusion samples (p.21); Fig 4A reports a single representative structure per model×condition ("for the lowest Protein pLDDt cofolding predictions", p.14 — note the caption says *lowest*, while Methods says per-residue pLDDT profiles came from "the highest-mean-protein-pLDDT prediction of each method", p.24; the two are inconsistent). No ensemble, distribution, or per-sample spread is reported anywhere. Multiple states appear only *across* input conditions, never within a run.

- **oracle_leakage**: **PRESENT — multiple independent routes.** The target's known conformational state enters through (i) the state-annotated database used to build both MSAs and templates, (ii) the reference crystal/cryo-EM structure used for alignment and RMSD, and (iii) post-hoc definition of "best"/"worst" model by RMSD to that reference.

  1. State labels of deposited structures drive template and MSA construction (Methods, p.20):
     > "For GPCRs, active and inactive state structures were retrieved from the PDB as mmCIF files, based on their state annotations in the GPCRdb (https://gpcrdb.org/)."

  2. Kinase state labels from Kincore drive the same (p.21):
     > "PDB entries were sorted according to their conformational states, including DFG-out, DFG-inter, Active, C-Helix-out, and Salt-Bridge-out, using Kincore."

  3. Templates are deposited structures pulled from those state-specific sets (p.21):
     > "Custom templates were chosen by using the PDB structure files of the top four hits in each individual state-specific MSAs."

  4. Stated up front as the design (p.4):
     > "Controlled template and MSA biasing strategies, informed by state annotations from KLIFS 7 and GPCRdb, 6 were applied throughout."

  5. Success is defined by RMSD to the structure they already had (p.23):
     > "The generated cofolding structures were aligned to their corresponding crystal structure using PyMOL and protein RMSD was calculated simultaniously."

  6. And "best"/"worst" model labels in Figs 1, 3 and 4 are assigned post hoc against the reference (p.11):
     > "Yellow indicates the reference PDB (ground truth), blue shows the best-performing model based on ligand RMSD, red shows the worst-performing model, and all other predictions are represented in grey."

  7. One arm is explicitly a *training-set* leak, and the authors say so (p.7):
     > "Based on its deposition date, 2019, this structure was likely present in all model training datasets."
     and (p.15) "This included the ATP example, for which a closely related ligand was present in the training data (ALK2 with AMPPNP in PDB 6UNQ)."

  **Partial mitigation the authors claim** (p.16):
  > "we adopted a general, database-driven biasing strategy based on state annotations from GPCRdb (https://gpcrdb.org/) 6 and KLIFS (https://klifs.net/) 7 rather than target-specific manual curation."
  and (p.19) "custom templates were selected automatically based on the MSAs generated from the state annotated databases, and no additional criteria were applied beyond this sequence and state information."

  **Important gap**: the paper never states, for any target, *which* state sub-database was used to build the "biased MSA"/custom-template condition. If the sub-database matching the target's known state was chosen, the leak is direct; if all state sub-databases were run, that is not reported. See `unresolved`.

  Six of seven reference structures were selected as recent and outside training sets (p.4: "spanning distinct functional states absent from all model training sets"), which limits *memorization* leakage but does not remove *pipeline* leakage from the state-annotated inputs.

- **prospective**: **partial.** The authors assert prospectivity: "We curated a benchmark of kinases and Class A GPCRs spanning distinct functional states absent from all model training sets, enabling prospective rather than retrospective evaluation." (p.4) and "conditions that approximate realistic prospective use" (p.16). But: the biasing inputs are built from state-labelled deposited structures of the target family (pp.20–21), the ATP/ALK2 arm is explicitly retrospective (p.7, p.15), and every outcome measure is RMSD to a held reference (p.23). Target-state novelty is real; pipeline blindness is not.

- **state_metric**: **RMSD-to-reference + visual inspection of named state markers.** No binary state predicate, no continuous state coordinate.
  - Protein backbone RMSD (PyMOL alignment; for GPCRs "alignment and protein RMSD calculations were restricted to the folded receptor core to exclude highly flexible terminal and loop regions", pp.23–24).
  - Ligand RMSD via MDAnalysis on the aligned structures (p.24).
  - State markers judged **visually** from structure renders: LRRK2 DYG-motif Y2018 orientation (p.5), ALK2 P-loop Y219 outward rotation (p.7), ALK2 D354–R375 salt bridge (p.7), GPCR ICL3 fold (pp.11–12), plus the RN277 phenyl ring "non-physical chair deformation" (p.5).
  - **Thresholds are descriptive, not defined, and never justified**: "ligand RMSDs were general below 0.8 Å" (p.5), "backbone RMSDs were generally below 1.5 Å" (p.8), "protein backbone RMSDs below 0.5 Å" (p.7), "backbone RMSD values exceeding 17 Å" for globally misfolded (p.12). No cutoff is declared as a success criterion; no power or tolerance analysis.

- **metric_saturation**: **Yes, in three places.**
  1. **Floor.** Ligand RMSD is compressed near its floor across all successful orthosteric arms (LRRK2 "general below 0.8 Å", p.5; ALK2-RK783 "below 0.8 Å", p.7; ALK2-ATP 0.58–1.40 Å, p.7), so it cannot discriminate between conditions that differ in state — which is precisely the paper's finding: "low ligand RMSDs were also observed in models that differed in residue orientation and local interaction networks" (p.7).
  2. **Ceiling / broken axis.** Fig 4A (p.14) uses a broken y-axis with a compressed 10–20 Å upper band for the globally misfolded arms (>17 Å, p.12); everything above the break is unresolvable.
  3. **Hard-pinned confidence.** RF3's ligand pLDDT is constant (p.15): "This analysis could not be performed for RF3, as the ligand pLDDT value in its outputs is fixed at 1.0, preventing meaningful comparison." RF3 is therefore dropped from Fig 4C entirely.

- **directional_control**: **Attempted, mostly failed. No reliable handle identified.** Handles tried:
  - State-filtered MSAs ("biased MSA") and state-annotated custom templates (top-4 hits) — the primary handles (pp.20–23). Verdict: "Template and MSA biasing affect prediction quality but do not reliably enforce correct conformations" (section heading, p.12).
  - Ligand identity itself as a handle — rejected: "ligands exert only a modest influence on the global fold prediction and primarily shape the local environment of the binding pocket" (pp.17–18).
  - For the allosteric case specifically, three further handles (p.8): "blocking the ATP site sterically, introducing known protein interaction partners associated with the allosteric conformation, and using Boltz-2 binding contact flags to bias the ligand toward the cryptic pocket" — all failed (p.9).
  - Seed is **not** a handle here: one seed only (p.21).
  - Single reported success: "the DOR model generated with AF3 using custom MSAs and templates, which closely approached the correct active-state intracellular geometry" (p.12) — 1 of 3 GPCRs, and only in AF3.

- **anti_memorization**: **UNPOWERED.** The control is the benchmark-selection design itself: recently solved structures "spanning distinct functional states absent from all model training sets" (p.4), with LRRK2 Y2018 described as "a geometry not observed in PDB entries released before the 2025 cryo-EM structure" (p.5). That is 6 held-out systems plus 1 deliberate in-training positive control (ALK2/AMPPNP 6UNQ, p.7) — n = 7 total, below the ~10 threshold, and no matched comparison is run between the held-out and in-training arms. No training-set membership was verified against the models' actual cutoffs; membership is inferred from deposition dates ("likely present in all model training datasets", p.7). No sequence-identity or scaffold-overlap analysis. No shuffled/decoy/negative-control arm anywhere.

- **confidence_as_discriminator**: **Yes, tested — but only against ligand placement, not against state.** Section "Model confidence metrics do not report state fidelity" (p.15):
  > "we observed that protein pLDDT showed no association with pose accuracy (Pearson r = +0.04, Figure 4B), whereas ligand pLDDT correlated moderately (r = -0.46, Figure 4C) indicating that local ligand confidence, but not overall fold quality, is informative for co-folding predictions."
  The regression is pLDDT vs **ligand RMSD**, i.e. pose accuracy. Despite the section title, **no correlation between any confidence metric and a state-fidelity measure is reported anywhere in the paper.** The validation of confidence-as-state-discriminator is therefore claimed by section heading, not by data. pLDDT is also used as the *selection* criterion for which of the five diffusion samples is shown (Fig 4A caption p.14; Methods p.24) — i.e. it is simultaneously the selector and the thing evaluated. ipTM/pTM are not used. Per-residue pLDDT profiles are relegated to Supplementary S1/S2 (p.18, p.24) and were used to decide which regions to exclude from analysis: "per-residue pLDDT profiles were generally highest across the receptor core and decreased in flexible peripheral regions which we omitted in further analyses" (p.18).

## D. Claims

- **central_conclusion**: Across four cofolding backbones and seven kinase/GPCR systems, ligand placement in orthosteric sites is generally accurate (sub-Ångström ligand RMSD) while recovery of the protein's functional conformational state — kinase state-marker residue orientations and GPCR intracellular/ICL3 geometry — frequently fails, and the two are decoupled. State-annotated templates and state-filtered MSAs help in isolated cases but do not reliably enforce the correct state; allosteric/cryptic pockets are never recovered by any model under any condition tested.

- **necessity_claims** (verbatim, with page):
  - p.2: "When aiming to work with structural data of kinases or GPCRs in in silico investigations, it is crucial to model the correct state for the bound ligands."
  - p.3 (characterising ref. 5, Heo & Feig): "Heo and Feig demonstrated that state-annotated templates alone are insufficient when deep MSAs are present, whereas no or shallow MSA sampling allows templates to reliably enforce active and inactive GPCR states with near-experimental accuracy."
  - p.3: "Together, these studies show that state-aware prediction is achievable, but remains highly sensitive to careful manual template selection combined with MSA control rather than emerging robustly from the models themselves."
  - p.4: "providing a stringent test of whether ligand guidance alone is sufficient to enforce global conformational states."
  - p.8: "However, across all models and parameter settings tested, none of the predicted structures placed the ligand in this allosteric pocket; instead, every model positioned it within the ATP binding site"
  - p.9: "These observations indicate that while cofolding reliably reproduces global protein architecture, it does not spontaneously sample cryptic or allosteric binding modes, even when guided."
  - p.12: "However, it does not allow one to reliably infer the functional outcome of a ligand, since accurate modeling of the intracellular signaling interfaces is still largely beyond reach without additional structural guidance."
  - p.12: "The importance of the presence of either MSA or of biased templates becomes clear across systems as omitting MSAs and templates in AlphaFold3 and RosettaFold-3 results in globally misfolded structures with backbone RMSD values exceeding 17 Å and misplaced ligands"
  - p.15: "This analysis could not be performed for RF3, as the ligand pLDDT value in its outputs is fixed at 1.0, preventing meaningful comparison."
  - p.17: "Binding of RN277 in LRRK2 or ATP in ALK2 both require a defined orientation of a tyrosine, which was only resolved in a subset of predictions"
  - p.17: "The strong misfolding when omitting MSAs in RF3 and AF3 implies that MSA modifications influences AF3 and RF3 more strongly and would need to be applied with particular care to avoid destabilizing their predictions."
  - p.17: "The limitation of relying solely on filtered template databases becomes evident here: these datasets are enriched for canonical conformations (DFG-in/out), constraining cofolding models to familiar structural states."
  - p.18: "Attempts to guide predictions through MSA editing or templating proved to be insufficient, especially for the active-state conformation, as there seems to be a preference for ICL3 conformations resembling the inactive state."
  - p.19: "Furthermore, conformational states that are rare, mutation-dependent, or only accessible through dynamic reorganization are not recovered without explicit conditioning."
  - p.20: "Moreover, careful ligand selection is crucial, as cofolding performs rather robustly for orthosteric ligands, it tends to fail for allosteric binders, highlighting a current limitation that must be considered when interpreting the results."
  - p.22 (a methodological impossibility that constrained the design): "AlphaFold3 does not intend to combine an unbiased MSA with biased templates within one run, which is why we only generated 5 conditions for alphaFold3."
  - p.23: "As RosettaFold-3 defines templating different than the other methods, templates were not considered."

- **novelty_claims** (verbatim, with page):
  - p.1 (abstract): "Here we show that cofolding adaptively remodels binding pockets around bound ligands, but that this local accuracy is frequently decoupled from recovery of the broader conformational state."
  - p.2 (abstract): "These findings establish conformational decoupling as a fundamental limitation of current cofolding approaches, with direct implications for state-selective drug design."
  - p.2 (abstract): "Furthermore, while orthosteric ligand placement is generally reliable, allosteric binders expose a consistent blind spot across all models."
  - p.4: "We curated a benchmark of kinases and Class A GPCRs spanning distinct functional states absent from all model training sets, enabling prospective rather than retrospective evaluation."
  - p.5: "the LRRK2-RN277 reference PDB structure features an upward-oriented conformation of the DYG-motif tyrosine, a geometry not observed in PDB entries released before the 2025 cryo-EM structure."
  - p.17: "This also supports the emerging view that generative structure predictors extrapolate only cautiously beyond known conformational space rather than fully sampling it."

- **stated_limits** (authors' own):
  - Template selection was purely sequence/state-based and ignored ligand identity and functional context: "This meant that aspects such as ligand identity or functional context were not explicitly considered during template selection." (p.19); they propose ligand-aware template selection as future work but caution that biased-agonist transferability "remains unclear" (p.19).
  - Filtered template databases are themselves biased toward canonical conformations (DFG-in/out) and thereby constrain the models (p.17).
  - ICL3 is often unresolved in deposited structures, so the reference itself may be weak; 5-HT2A has an "unusually long ICL3" with no comparable templates (p.18).
  - ADL5859 is a biased agonist, "a typ of ligand underrepresented in available co-crystallized structures", so the induced intracellular conformation "may be uncommon and poorly sampled in template databases" (p.18).
  - Flexible peripheral regions were excluded from analysis based on pLDDT (p.18) and GPCR RMSD was restricted to the receptor core (pp.23–24).
  - RF3 could not be assessed for ligand confidence (p.15) and was run without templates (p.23) — the RF3 arm is not comparable to the others.
  - The ALK2-ATP reference was likely in the training data (p.7, p.15).
  - NOT stated by the authors as a limit: the small n (7 systems), the single seed, the absence of any GPCR panel in the quantitative Fig 4A, and the absence of any state-fidelity-vs-confidence regression despite the section title on p.15.

- **stance**: **precedent** — *(user to confirm; see reasoning)*. Reasoning: it independently reports, on a different family pair and with four backbones, that ligand identity is a weak handle on global conformational state ("ligands exert only a modest influence on the global fold prediction and primarily shape the local environment of the binding pocket", pp.17–18) and that active-state GPCRs are "consistently pulled toward the inactive state" (p.17) — which supports rather than threatens a partner-driven state-control framing. It is simultaneously a `contrast` on rigour (n=7, single seed, RMSD-to-reference only, oracle-leaking state-annotated inputs, no anti-memorization power, no ensemble) and could be read as a mild `threat` only insofar as it claims to "establish conformational decoupling as a fundamental limitation" (p.2) on a 7-system benchmark. **This is the user's call.**

## E. Quantitative comparators

- **metrics_reported**:

| Metric | Value | Units | Measured against | Page |
|---|---|---|---|---|
| Ligand RMSD, LRRK2–RN277, successful folds | "general below 0.8" | Å | PDB 9DMI | 5 |
| Ligand RMSD, best LRRK2–RN277 (Chai-1, no-MSA + custom templates) | 0.42 | Å | PDB 9DMI | 5 |
| Ligand RMSD, ALK2–RK783, successful folds | "below 0.8" | Å | PDB 9L04 | 7 |
| Ligand RMSD, best ALK2–RK783 (AF3, biased MSAs) | 0.57 | Å | PDB 9L04 | 7 |
| Ligand RMSD, ALK2–ATP, successful predictions | 0.58 – 1.40 | Å | PDB 6UNQ | 7 |
| Ligand RMSD, best ALK2–ATP (Boltz-2, standard MSA, no templates) | 0.58 | Å | PDB 6UNQ | 7 |
| Protein backbone RMSD, ALK2–ATP successful predictions | "below 0.5" | Å | PDB 6UNQ | 7 |
| Protein backbone RMSD, PI3Kα–Zovegalisib | "generally below 1.5" | Å | PDB 8TSD | 8 |
| Protein backbone RMSD, AF3 & RF3 with no MSA and no templates | "exceeding 17" | Å | reference PDB | 12 |
| Allosteric pocket recovery rate | 0 of all models × all conditions | count | PDB 8TSD cryptic site | 8 |
| Pearson r, mean protein pLDDT vs ligand RMSD | +0.04 (n.s.) | — | pooled across all predictions | 15 (Fig 4B, p.14) |
| Pearson r, mean ligand pLDDT vs ligand RMSD | −0.46 | — | pooled across all predictions, RF3 excluded | 15 (Fig 4C, p.14) |
| RF3 ligand pLDDT | fixed at 1.0 | — | — | 15 |
| ICL3 active-state recovery | 1 case (DOR, AF3 + custom MSA + templates) out of 2 active-state GPCRs × 20 conditions | count | PDB 8Y45 | 12, 19 |
| Method ranking (qualitative) | AF3 > Boltz-2 > RF3 > Chai-1 | rank | across targets | 15–16 |
| AF3 biasing wins | "results in the models structurally closest to the ground truth in four cases" | count | across systems | 15 |

- **n_predictions**: Per model×condition: 1 seed ("0") and 5 diffusion samples — "For each method and condition, the general inference settings were kept similar using one seed ("0") and five diffusion samples." (p.21). Conditions per system: AF3 5 (p.22), Boltz-2 6 (p.22), Chai-1 6 and RF3 3 (read off Fig 4A, p.14) = 20. Across 7 systems this implies on the order of 700 sampled structures, of which one per model×condition is reported in Fig 4A. **A total prediction count is NOT REPORTED anywhere in the paper.** The Fig 4B/C scatter plots (p.14) show a few hundred points but no n is printed.

- **comparable_to_ours**: **Partially.** Their ligand-RMSD numbers are not comparable (we do not report ligand RMSD). What sits beside our numbers:
  - Their qualitative finding that active-state GPCRs are "consistently pulled toward the inactive state" (p.17) sits beside our Block A result that apo lands inactive on medians while producing active-like structures at ~14.5% mean rate — but they give no rate, only visual per-case verdicts, so the comparison is directional not numerical.
  - Their pLDDT-vs-accuracy correlations (r = +0.04 protein, −0.46 ligand, p.15) are the closest thing to a numerical comparator for any confidence-as-discriminator claim, with the caveat that their outcome is ligand pose, not state.
  - Their n (7 systems, ~20 conditions, 1 seed) sits beside our ~9,500 (Block A) and ~32,000 (Block B) predictions across 48 receptors and is the natural power contrast.
  - Their backbone set (AF3, Boltz-2, Chai-1, RF3) overlaps ours on four backbones — worth checking exact identity before asserting it.

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 6 | Kinase cofolding predictions vs ground-truth structures: ligand pose superpositions and close-ups of state-marker residues (LRRK2 Y2018; ALK2 RK783 pocket / D354; ALK2 ATP P-loop Y219) | structure render (grid of small multiples) | 3 systems × 2–3 views → per-system superposition of all predicted ligand poses on the reference, plus zoomed state-marker residue close-ups; no quantitative axis | 8 panels (A–H); panels are system × view, not conditions | All ~20 conditions are drawn as undifferentiated transparent overlays with only "best" (red) and "worst" (blue) highlighted, so which input condition produced which geometry is unreadable; no n, no axis, no per-condition identity | CC-BY-NC-ND 4.0 (p.1) — **ND clause: no derivatives; reproduction unmodified with attribution only** |
| 2 | 8 | PI3Kα-H1047R + Zovegalisib: every model places the ligand in the ATP site while the reference occupies a cryptic allosteric pocket | structure render | 1 system × 2 views → all model predictions (grey) overlaid on reference (yellow); global fold view and ligand-placement close-up with the true allosteric site circled | 2 panels (A, B); panels are views of one system | All models and all conditions pooled into a single grey overlay; n not shown; the uniform-failure result is legible but the per-model/per-condition breakdown is not, so "even when guided" (blocking, partners, contact flags) is asserted in text with no visual evidence | CC-BY-NC-ND 4.0 (p.1) |
| 3 | 11 | Three class A GPCRs: orthosteric ligand conformations (top) and ICL3 folds (bottom), predictions vs reference | structure render (grid of small multiples) | 3 systems × 2 features → per-system overlay of all predictions on the reference, top row = ligand conformation, bottom row = ICL3 backbone; no quantitative axis | 6 panels (A–F) = 3 systems × 2 rows; panels are systems, rows are features | No quantitative axis for the GPCRs anywhere in the paper — Fig 4A contains only kinases, so the central GPCR claim (ICL3 misfolding in active states) rests entirely on visual overlay with no RMSD, no n, and no distribution | CC-BY-NC-ND 4.0 (p.1) |
| 4 | 14 | (A) protein backbone RMSD bars + ligand RMSD dots for every model×input condition on four kinase systems; (B, C) pLDDT vs ligand RMSD scatter | (A) bar + overlaid dot strip; (B, C) scatter | (A) 20 conditions × 4 kinase systems → x = model × MSA/template condition (AF3 5, Boltz-2 6, Chai-1 6, RF3 3), y = RMSD (Å), bars = protein backbone RMSD, dots = ligand RMSD, one sub-panel per system; (B, C) 2 confidence metrics × ~500 pooled predictions → x = mean pLDDT (protein / ligand), y = ligand RMSD, points coloured by 1 of 4 methods, single trend line | 6 panels: A = 4 stacked sub-panels (systems), B and C = 2 scatters (conditions) | **A: one bar per condition, hiding the spread over the 5 diffusion samples that were generated** — a single pLDDT-selected representative is shown, so no distribution and no n. **A: broken y-axis** (0–1.5 Å band, then a compressed 10–20 Å band), pinning every globally misfolded arm above the break where it is unresolvable. **A: GPCR systems absent entirely** — only 4 kinase complexes have a quantitative panel. **B/C: pooled across all systems and all conditions**, so a per-system or per-condition pLDDT–accuracy relationship cannot be read; n not printed; RF3 silently absent from C (its ligand pLDDT is pinned at 1.0, p.15) | CC-BY-NC-ND 4.0 (p.1) |
| TOC | 31 | Workflow schematic: GPCRdb/KLIFS → state-filtered MSAs + templates → four cofolding models → four readouts (pocket conformation, orthosteric ligand challenge, ligand RMSD, conformational states, biased MSA/template importance) | schematic | 1 pipeline × 4 models → left-to-right flow from state-annotated databases and ColabFold through the model set to five labelled outcome icons; no data axis | 1 panel; not a data figure, no caption text in the PDF | (blank — a schematic, not a result) | CC-BY-NC-ND 4.0 (p.1) |

- Supplementary figures S1 (per-residue pLDDT, kinases) and S2 (per-residue pLDDT, GPCRs) are listed on p.24 but are **not present in this 31-page PDF**; they cannot be catalogued.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent, pilot run
- **confidence**: **medium-high.** Text layer is clean and every quote above is verbatim from `pdftotext -layout`. Reduced from high because: (a) Figs 1–3 are pure structure renders whose per-model detail cannot be read from the text layer or at 150 dpi, so all per-condition structural verdicts are taken from the authors' prose rather than checked; (b) the Fig 4A condition counts for Chai-1 (6) and RF3 (3) were read off a rendered page image, not stated in text; (c) Supplementary S1/S2 are absent from the PDF.
- **unresolved**:
  1. **Which state sub-database was used for each target's "biased MSA"/custom-template condition is never stated.** Methods (p.20–21) describe building one MSA per conformational state, and templates from the top-4 hits "in each individual state-specific MSAs", but Fig 4A shows a *single* "biased MSA" bar per model per system. If the sub-database matching the target's known state was chosen, `oracle_leakage` is direct and severe; if all sub-databases were run and only one shown, the selection criterion is unreported. This single ambiguity determines the severity of the paper's central rigour problem.
  2. **Fig 4A caption says "lowest Protein pLDDt" (p.14) while Methods says "highest-mean-protein-pLDDT prediction" (p.24).** One is a typo; which one is unknown, and it changes what the whole quantitative figure shows.
  3. **Total number of predictions is never stated** (see `n_predictions`); ~700 is my arithmetic from stated per-condition sampling, not the paper's number.
  4. **No n is printed on Figs 4B/4C** and the number of points in those scatters cannot be counted reliably at 150 dpi.
  5. **No GPCR quantitative data exists in the paper.** All three GPCR conclusions rest on visual inspection of Fig 3. Neither ligand RMSD nor backbone RMSD is tabulated or plotted for 8ZMG, 8UGW or 8Y45 anywhere in the main text.
  6. **Section title "Model confidence metrics do not report state fidelity" (p.15) is not supported by any state-fidelity analysis** — the only regressions shown are confidence vs ligand pose RMSD. Whether a state-fidelity regression exists in the Supplementary cannot be checked from this PDF.
  7. **Training-set membership is inferred, not verified** — from PDB deposition dates only (p.7). No model cutoff dates are cited.
  8. **Chai-1 and RF3 condition definitions are not written out in Methods** the way AF3's five and Boltz-2's six are; they were read from the Fig 4A x-axis.
  9. **Reuse/licence**: CC-BY-NC-ND 4.0 (p.1). The **ND (NoDerivatives)** clause means figure panels may be reproduced unmodified with attribution but **may not be recropped, recoloured or recombined**. Confirm with the user before reusing any panel. Data and models are on Zenodo (10.5281/zenodo.19481962, p.24) — licence of that deposit NOT REPORTED in the paper.
  10. **Tags wanted but absent from the fixed vocabulary** (not invented, per SCHEMA.md): a Control tag for *state-annotated-template biasing* and one for *state-filtered (not subsampled) MSA biasing* — the two primary handles in this paper have no tag; `msa-subsample` is wrong because they substitute a state-filtered alignment rather than reduce depth. Also absent: a tag for *allosteric / cryptic-pocket* targets, a tag for *multi-backbone comparison* (four backbones benchmarked head-to-head), and a *preprint / not-peer-reviewed* tag.

- **why_it_matters**: NOT FILLED — user's call.

---

## Tags

`gpcr` `kinase` `cofolding` `benchmark-only` `single-state` `rmsd-only` `saturating-metric`
`oracle-leak` `unpowered` `no-anti-memorization` `confidence-as-discriminator`
`ligand-driven` `seed-only` `precedent` `comparator-numbers`

Tag notes:
- `single-state`: one structure per model×condition; no ensemble within a run (p.21, p.14).
- `rmsd-only` **and** `saturating-metric` both apply: RMSD-to-reference is the only quantitative state measure, and it floors in every successful orthosteric arm and is axis-broken above 10 Å (p.5, p.7, p.14).
- `no-anti-memorization` rather than `anti-memorization`: the held-out-structure design (n=7, p.4) is below the ~10 threshold and is never analysed as a control arm. `unpowered` also applied.
- `ligand-driven` and `seed-only`: the ligand is the nominal state handle and is shown to be weak (pp.17–18); one seed only (p.21). No `partner-driven` — partners were tried once for PI3Kα and failed (p.8). No `directed-state` — biasing "does not reliably enforce correct conformations" (p.12).
- `precedent` is provisional; see `stance`.
- Tags I could not use because they are not in the vocabulary are listed in `unresolved` item 10.
