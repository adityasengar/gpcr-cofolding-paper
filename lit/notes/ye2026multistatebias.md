# ye2026multistatebias

## A. Identity

- **citekey**: `ye2026multistatebias`
- **doi**: 10.64898/2026.07.10.737860 (bioRxiv preprint, "this version posted July 11, 2026"; "which was not certified by peer review", banner on every page, p.1)
- **year**: 2026
- **venue**: bioRxiv preprint. **Preprint — not peer reviewed** (p.1). Licence CC-BY-NC-ND 4.0 (p.1 and every page banner).
- **title**: Benchmarking AI Protein Structure Predictors Reveals a Persistent Bias in Multi-State Proteins
- **authors**: Muhui Ye, Yu-Hong Wang, Maximilian Brogi, Jerry M. Parks, Katie M. Kuo, James C. Gumbart — Georgia Institute of Technology (Biological Sciences; Chemistry & Biochemistry; Physics) and Oak Ridge National Laboratory (p.1). Corresponding: Kuo, Gumbart.

## B. Scope

- **system**: **Four systems, four different classes.** GPCR (β2AR); transporter (PfMATE, MATE-family multidrug transporter); periplasmic binding protein (LAO); ATPase motor / translocase partner (SecA). (p.4–5)
  > "we systematically evaluate AlphaFold3, Boltz-2, Chai-1, and BioEmu across four well-characterized proteins with distinct experimentally resolved conformations: PfMATE, a multidrug transporter with inward- and outward-facing apo conformations; LAO, a periplasmic binding protein with a ligand-induced open-to-closed transition; SecA, an ATPase with nucleotide- and partner-dependent conformational states; and β2-adrenergic receptor (β2AR), a GPCR with active and inactive conformations." (pp.4–5)
- **n_targets**: **4 proteins.** Reference states per target: PfMATE 2 (6GWH OF, 6FHZ IF, p.5); LAO 2 (2LAO apo/open, 1LAF holo/closed, p.7); SecA 3 (1M74 wide-open, 1TF2 open, 8YAS closed, p.10); β2AR 2 (9CHU inactive agonist-bound, 8GEG active agonist-Gαβγ-bound, p.12). Generality claim rides on 4 proteins ("These proteins represent biological functions in which conformational switching is directly responsible for activity, regulation, ligand recognition, or a combination thereof, making them useful benchmarks", p.5).
- **method_class**: **benchmark-only**, plus a secondary comparison arm that is clustering + MSA-subsampling. No new method is proposed. The four co-folding/generative predictors are run as released; AF-Cluster (DBSCAN MSA clustering → AlphaFold2) and uniform MSA subsampling (U10, U100) are added as a baseline arm (p.15, p.18).
- **backbones**: **AlphaFold3 (v3.0.1), Boltz-2, Chai-1, BioEmu** — four, head to head (p.20 Data availability; p.18 Methods). Plus **AlphaFold2** indirectly, as the engine inside the AF-Cluster / U10 / U100 baseline arm (p.15). All run from local installations "with default parameters unless otherwise noted" (p.20). → `multi-backbone`.
- **templates**: **off.** Explicit:
  > "no distance restraints, templates, or MSAs were used." (p.18)
  Templates are discussed only as an alternative strategy the authors did *not* use: "providing state-specific templates can steer proteins such as GPCRs toward active or inactive conformations when the target state is known a priori, which is also a capability now shared by AlphaFold3, Boltz-2, and Chai-1 as well." (p.14)
- **msa_handling**: **Dual, by arm.**
  - Main arm (AF3, Boltz-2, Chai-1, BioEmu): **none** — "no distance restraints, templates, or MSAs were used." (p.18). Reiterated in Conclusions: "even without templates or MSAs, predictions frequently regress toward the dominant represented state in the PDB." (p.17)
  - Baseline arm: **clustered** (AF-Cluster/DBSCAN sub-MSAs) **and subsampled** (uniform random depth 10 and depth 100) — kept distinct by the authors themselves: "As controls, we also generated uniformly random sub-MSAs of depth 10 (U10) and 100 (U100) to test whether evolutionary structure in the clusters, as opposed to simple MSA depth reduction, drives any observed conformational shift." (p.15)
  - **Not** state-filtered anywhere. No state-annotated sequence database (no GPCRdb / KLIFS / Kincore equivalent) is used.

## C. Conformational core

- **states_generated**: **Ensemble per condition, collapsing to one dominant state in most arms.** Each model × input condition yields a population of predictions plotted as a scatter (50 per condition where stated, p.8, p.10; 20 for the BioEmu β2AR cluster, p.12), so the *output* is a distribution, but the *content* is usually a single basin:
  > "modern predictors (AlphaFold3, Boltz-2, Chai-1) show state-dependent success but repeatedly collapse toward a single dominant basin, consistent with training-distribution bias." (p.17, quoting the run-on sentence "Across PfMATE, LAO, SecA, and β2AR, modern predictors (AlphaFold3, Boltz-2, Chai-1, BioEmu) show state-dependent success but repeatedly collapse toward a single dominant basin")
  Exceptions actually produced: BioEmu on SecA sampled a **continuum** — "sampling a broad continuous distribution from wide-open to closed (45.1 ± 4.3 Å), suggesting that it captures a more complete conformational landscape, although one that is unphysiologically biased towards the closed state" (p.10); Chai-1 on apo β2AR sampled **two** states — "Chai-1 identifies clusters within both conformations without any constraints" (p.13); Chai-1 and Boltz-2 on SecA were **bimodal** but missed the middle state (p.10).

- **structural_priors_used**: **New in v3. Entirely at design time, and the paper is unusually explicit about it — the priors are part of the argument rather than a confound.**
  1. **All four targets were chosen because both states are deposited**, and the reference pairs are named: PfMATE outward-facing **6GWH** / inward-facing **6FHZ** (p.6); LAO apo-open **2LAO** / holo-closed **1LAF** (p.8); SecA states via the PBD–HWD distance and PBD–hinge–NBD2 angle (p.11); β2AR inactive **9CHU** / active **8GEG** (p.13). Every RMSD in the paper is measured to one of these.
  2. **The PDB state ratio per target was known in advance and is used as the explanatory variable.** p.7: *"Of the eleven PfMATE structures deposited in the PDB, only one (6FHZ) captures the IF state, creating a 10:1 ratio that may contribute to the observed prediction bias (Table S1)."* Restated at p.17: *"This pattern is consistent with the unequal distribution of PDB structures across conformational states for all four proteins (Table S1)."* This is the paper's central claim, and it is **correlational**: the ratio is observed alongside the bias, never manipulated. See `controls_run`.
  3. **Ligands and partners are taken from the deposited complexes** — arginine for LAO, ATP and SecYEG for SecA, agonist plus heterotrimeric Gαβγ (and GTP) for β2AR.
  4. **Expected state declared before the result is read** in every arm, which is `oracle_leakage` route 7 and is recorded there rather than duplicated here.

- **oracle_leakage**: **PRESENT, but by only two routes — and several classic routes are genuinely absent here.** Enumerated separately:

  1. **Success is defined post hoc by RMSD (and by domain-geometry distance) to deposited reference structures the authors already held.** Methods, p.18:
     > "Conformational similarity was quantified primarily by Cα RMSD in PyMOL using CEAlign and sequence-based align, and conformational preferences were visualized by paired-reference RMSD scatter plots."
     and, for SecA, p.18:
     > "For SecA, where three reference states and large domain motions can make RMSD ambiguous, we additionally classified states using domain-level geometric descriptors (PBD–HWD distance and a PBD–hinge–NBD2 angle)."
     Reference values for those descriptors are read straight off the deposited structures, p.10:
     > "Reference values were taken from experimental structures representing three key states: wide-open (1M74; distance = 26.7 Å, angle = 135.0°), open (1TF2; 39.3 Å, 106.0°), and closed (8YAS; 49.9 Å, 76.1°)."
     Reference structures were also curated before use, p.18: "Reference structures were preprocessed to retain only the target protein chains and remove non-protein components."

  2. **The input conditions themselves are chosen because the answer is known — the expected state is declared before the result is read.** This is oracle knowledge in the *experimental design*, not in the model input (the models receive only sequence + SMILES + partner sequence). Verbatim:
     > "With ATP included as a ligand, a wide-open conformation is expected." (p.10)
     > "Upon providing SecYEG and ADP, clamp closure is expected, as exemplified by the structure in PDB 8YAS." (p.11)
     > "When provided with the partners and ligands required for activation of β2AR (i.e., agonist and G protein), all predictions clustered tightly toward the active conformation" (p.13)
     > "Among the four input conditions (apo [inactive], agonist [inactive], agonist-Gαβγ [active], and agonist-Gαβγ-GTP [active]), the active and inactive states are the main conformations of interest as they are the most distinct." (p.13) — the state label is assigned to the condition a priori.

  3. **Training-set overlap is acknowledged and used as an explanatory variable, not controlled for.** p.7:
     > "This bias occurred despite the IF-state structure being released in 2019 and therefore present in the training data for all models tested."
     > "Of the eleven PfMATE structures deposited in the PDB, only one (6FHZ) captures the IF state, creating a 10:1 ratio that may contribute to the observed prediction bias (Table S1)." (p.7)
     This is a leak *diagnosis*, not a leak into the pipeline — recorded here because it means every reference state is inside the training window.

  **Routes explicitly NOT present** (protocol described on p.18, Methods):
  - No deposited structure used as model input: "no distance restraints, templates, or MSAs were used." (p.18)
  - No state-annotated database (GPCRdb / KLIFS / Kincore or equivalent) driving templates or alignments — none is mentioned anywhere in the paper.
  - No cluster labels derived from known states: AF-Cluster's DBSCAN partitions on *sequence similarity only* — "AF-Cluster uses DBSCAN to partition the MSA into sequence-similarity clusters, each reflecting a distinct evolutionary subfamily that may encode a different conformational state" (p.15).
  - No hyperparameter / seed / stopping-criterion tuning against known states reported: "with default parameters unless otherwise noted" (p.20).
  - No best/worst model label assigned against a held reference (no per-model best/worst selection is performed anywhere; all samples are plotted).

- **prospective**: **no.** Fully retrospective. Every reference state is a deposited structure released before the models' training cutoffs (explicitly for PfMATE IF, p.7), the outcome measure is agreement with those structures (p.18), and no post-cutoff or blind target is used. Mitigating: the **model inputs** are clean — sequence, SMILES ligand, full-length partner sequence, no templates/MSAs/restraints (p.18) — so there is no state-biasing pipeline leak of the kind a template- or MSA-biasing paper carries. Prospective in *input hygiene*, retrospective in *targets and scoring*.

- **state_metric**: **RMSD-to-reference (primary) + a continuous two-descriptor coordinate for SecA + TM-score as a fold sanity check.**
  - Primary: Cα RMSD to each of two reference structures, plotted as paired-reference scatter with a y=x diagonal; side of the diagonal is the state call — "Points below the diagonal line are closer to the OF state, while those above are closer to the IF state." (p.6, Fig 1 caption; identical device in Figs 2, 4, 5).
  - SecA: PBD–HWD distance (Å) and PBD–hinge–NBD2 angle (°), because "Because SecA conformational changes are primarily localized to the rotation of the PBD domain rather than global structural rearrangements, RMSD of the entire protein is insufficient to distinguish between open and closed clamp states." (p.10)
  - Global fold check: "TM-scores were computed with TM-align to confirm global fold preservation." (p.18) — no TM-score values appear in the main text.
  - **Thresholds: none defined, none justified.** Success is described in ad hoc prose thresholds: "most RMSD values to the IF state exceeded 3.5 Å" (pp.6–7); "Except BioEmu, which generated one structure 1.8 Å away, no tool successfully predicted structures resembling the IF reference state" (p.6) — 1.8 Å is treated as approaching success with no stated criterion; "some frames displaying intermediate RMSD values" (p.9); "some BioEmu frames approached intermediate RMSD values (2-3 Å to both reference structures)" (p.6). No cutoff is declared, no tolerance or power analysis is given.

- **metric_saturation**: **Yes — a hard RMSD floor in the converged arms, plus axis truncation in two figures.**
  - **Floor.** LAO holo-converged arms sit at the resolution limit of the metric: AlphaFold3 "RMSD to holo = 0.20 ± 0.01 Å", Chai-1 "0.29 ± 0.03 Å", holo runs "AlphaFold3: RMSD to holo = 0.22 ± 0.02 Å; Chai-1: RMSD to holo = 0.24 ± 0.02 Å" (p.7). The authors read the floor correctly as non-sampling — "The very low standard deviations (0.01-0.06 Å) across all conditions indicate minimal conformational sampling" (p.7) — but it also means apo and holo conditions are **unresolvable from each other** by this metric, which is the paper's own conclusion for those arms.
  - Same floor for PfMATE: AF3 "RMSD to OF: 0.57 ± 0.03 Å; RMSD to IF: 5.42 ± 0.05 Å" (p.5).
  - **Axis truncation.** Fig 3B (p.11): x-axis starts at ~20 Å and y-axis at ~70°, not zero — the truncation is not flagged in the caption. Fig 5C (p.16): same pair of truncated axes (x from ~30 Å, y from ~75°). Fig 5B (LAO) truncates the y-axis at 6 Å where Fig 2B used 7 Å, so the two LAO panels are not on the same scale.
  - **Zoom insets instead of a break.** Fig 4B AlphaFold3 panel (p.12) carries two magnified insets to resolve clusters that are otherwise a single dot at plot scale; the main panel therefore visually understates the separation the insets contain.
  - No metric ceiling is reported.

- **directional_control**: **Yes, partially — the working handle is the protein binding partner; the small-molecule ligand handle is unreliable; the MSA handles fail.** Handles actually tested:
  - **Full-length protein binding partner supplied as a co-folded chain** — the one handle that works. "protein binding partners (SecYEG; heterotrimeric G protein) were provided as full-length sequences" (p.18). Result: β2AR active state recovered by all three co-folding models (p.13); SecA closed state recovered by Chai-1 and Boltz-2 but not AF3 (p.11).
  - **Small-molecule ligand supplied as canonical SMILES** — "Small-molecule ligands (L-arginine, ATP/ADP, norepinephrine, and GTP) were provided as canonical SMILES strings where supported" (p.18). Verdict: weak/idiosyncratic (see `necessity_claims`).
  - **MSA clustering (AF-Cluster) and MSA depth subsampling (U10/U100)** — both fail: "MSA-level manipulation alone, whether through evolutionary clustering or random subsampling, is largely insufficient to overcome the systematic conformational bias observed across the deep learning tools evaluated in this study" (pp.16–17).
  - **Not used as handles**: state-annotated templates (discussed as an alternative, p.14, but "no ... templates ... were used", p.18); distance restraints (available in Chai-1 and Boltz-2 and explicitly declined, p.18); nanobody; peptide; seed sweeps; subsample depth applied to the AF3-generation models.

- **anti_memorization_design**: **NONE.** There is no held-out set, no post-cutoff target set, and no cutoff definition anywhere in the paper. The opposite is stated — the reference states are known to be inside the training data: "This bias occurred despite the IF-state structure being released in 2019 and therefore present in the training data for all models tested." (p.7) The one deposition-date-relevant reference, SecA-SecYEG 8YAS (Cell 2025, ref. 44, pp.10, 26), is never discussed as post-cutoff or used as a held-out probe. Table S1 (PDB state-composition counts per target, cited pp.7, 17) is a *bias diagnosis*, not an anti-memorization design. Note the paper raises memorization as the motivating question and then does not test it directly: "an important question is whether they have memorized training data rather than learned generalizable molecular interaction features" (p.4).

- **anti_memorization_control**: **NONE RUN.** No control arm addresses memorization. The only control arm in the paper is a different control entirely — evolutionary signal vs. depth reduction:
  > "As controls, we also generated uniformly random sub-MSAs of depth 10 (U10) and 100 (U100) to test whether evolutionary structure in the clusters, as opposed to simple MSA depth reduction, drives any observed conformational shift." (p.15)
  Correlational evidence is offered in place of a control: the PDB apo/holo or state ratio per target ("a 10:1 ratio that may contribute to the observed prediction bias (Table S1)", p.7; "This pattern is consistent with the unequal distribution of PDB structures across conformational states for all four proteins (Table S1)", p.17), plus an appeal to an external study of 82 enzymes (ref. 69, pp.17–18). Neither is an arm the authors ran.

- **controls_run**: **New in v3, and for this paper it is the field that decides how much weight the headline can carry.** v2 recorded the U10/U100 arm inside `anti_memorization_control` and had nowhere for the rest.

| control | what it rules out | page |
|---|---|---|
| **Apo arm, every target** | that the models need no co-input to reach the dominant state; it is the baseline every other arm is read against | pp.7–13 |
| **Small-molecule ligand arm** (LAO + arginine; SecA + ATP; β2AR + agonist) | that any co-input suffices. This arm is what makes the headline asymmetry visible: ligands move the prediction weakly and inconsistently | pp.7–13 |
| **Protein-partner arm** (SecA + SecYEG/ADP; β2AR + Gαβγ, ± GTP) | that the ligand result generalises to all co-inputs. p.13: *"predictions with the G protein partner (blue, purple) achieved substantially lower RMSD to the active reference structure than baseline apo and agonist-only predictions (yellow, pink) did to the inactive reference."* | p.13 |
| **Four independent backbones** (AF3, Boltz-2, Chai-1, BioEmu) | that the bias is one architecture's artefact | throughout |
| **AF-Cluster applied to all four targets** | that the bias is specific to the newer AF3-lineage architectures. p.15: *"To provide a baseline comparison using an AlphaFold2-based MSA manipulation approach distinct from the newer architectures evaluated above, we applied AF-Cluster to all four target proteins."* (An inline superscript reference numeral 51 sits after "AF-Cluster" in the PDF text layer and is omitted here; recorded so a mechanical quote check does not flag it as fabricated.) | p.15, p.19 |
| **Uniformly random sub-MSAs at depth 10 and 100 (U10, U100)** | that plain MSA depth reduction, rather than evolutionary structure in the clusters, drives any shift. p.15: *"As controls, we also generated uniformly random sub-MSAs of depth 10 (U10) and 100 (U100) to test whether evolutionary structure in the clusters, as opposed to simple MSA depth reduction, drives any observed conformational shift."* | p.15, p.19 |
| **BioEmu as a purpose-trained ensemble comparator** | that a model trained for conformational sampling would trivially solve it — it does not; it disperses more but stays biased | pp.6, 9, 12 |
| **ABSENT — any memorization control** | nothing separates memorisation from generalisation. The PDB state ratio (Table S1) is offered as a *correlate* of the bias, not as a manipulated variable: no temporal split, no post-cutoff arm, no held-out targets, no matched seen/unseen comparison. **With n = 4 targets, no such arm could have been powered even if run.** | — |
| **ABSENT — partner without agonist** | whether the partner alone is sufficient. Every β2AR partner condition supplies the agonist *and* the heterotrimer together, so the partner's independent contribution is never isolated. **This is the control our own design supplies and theirs does not**, and it is the single most important gap in this paper for our purposes | p.18 |
| **ABSENT — reduced or partial partner construct** | whether the whole transducer is needed, or only the α5 contact. No truncated, decoy or scrambled partner is run | p.18 |

  **How to cite this paper's strength honestly.** The controls that *were* run are good ones and they establish the direction of the effect across four architectures and two MSA-manipulation baselines. What they do not establish is that the partner is acting as itself rather than as an occupant, or that the effect survives outside four hand-picked targets whose state ratios were known in advance.

- **coinput_composition**: **New in v3.1. CONFOUNDED — the paper's headline cannot be attributed to the partner alone.**
  - apo arm: receptor only.
  - ligand arm: receptor + one small molecule (arginine for LAO, ATP for SecA, agonist for β2AR).
  - partner arm, β2AR: receptor + **agonist AND heterotrimeric Gαβγ supplied together**, with a further arm adding GTP. There is no agonist-free partner condition and no partial or truncated partner anywhere in the paper (p.18).
  - partner arm, SecA: receptor + SecYEG + ADP together.
  **Consequence.** The finding that "large protein partners drive clear conformational switching" (p.2) is measured against an apo or agonist-only baseline, never against a partner-alone condition, so the partner's independent contribution is not isolated. Tag `coinput-confounded`.

- **binding_order**: **ORDER-AGNOSTIC by construction, and NOT ADDRESSED as a question.** Every co-input is supplied simultaneously to a co-folding model, which has no representation of binding sequence, so nothing here can distinguish agonist-first from pre-coupled routes. The paper does not raise the question.

- **confidence_as_discriminator**: **Reported alongside results and read as commentary, but never used as the state call and never validated — and the authors explicitly disclaim the practice.**
  - Reported: LAO Boltz-2 holo "high model confidence (pTM 0.929–0.952)" vs apo "markedly lower confidence (pTM 0.729–0.856, Table S4)" (p.8); SecA "Model confidence was generally lower under SecYEG+ADP conditions (pLDDT 72–81) compared to apo predictions (pLDDT 76–86, Table S4), consistent with the increased structural complexity of the multiprotein complex" (p.12).
  - Disclaimed: "Confidence metrics such as pLDDT and PAE are useful for local geometry and uncertainty, but they are not reliable selectors of biologically or physically meaningful alternative states." (p.15)
  - No validation of pLDDT/pTM against state correctness is performed. State calls come from RMSD/geometry only.

## D. Claims

- **central_conclusion**: Across four multi-state proteins, AlphaFold3, Boltz-2, Chai-1 and BioEmu collapse onto whichever conformational state is over-represented in the PDB, and this bias is not fixed by MSA clustering or subsampling (i.e. it is architecture-independent). Conditioning inputs on small-molecule ligands moves predictions weakly and inconsistently; conditioning on a large protein binding partner moves them decisively and reproducibly toward the partner-associated state.

- **necessity_claims** (verbatim + page):

  **On small molecules being insufficient / large partners being what drives the change** — the load-bearing set:
  1. p.2 (Abstract):
     > "Models frequently default to a dominant state represented in the PDB; small-molecule ligands have weak or inconsistent effects, while large protein partners drive clear conformational switching between states."
  2. p.13:
     > "Agonist binding alone stabilizes intermediate receptor conformations but is generally insufficient to induce the fully active state; the binding pocket exhibits only around a 1-Å shift upon agonist binding."
  3. p.13:
     > "Full activation requires engagement with the heterotrimeric G protein, which allosterically stabilizes the outward displacement of TM6 at around 14 Å."
  4. p.17:
     > "Small-molecule ligand conditioning is generally weak and sometimes idiosyncratic."
  5. p.18:
     > "For SecA, ATP produced the expected wide-open shift for AlphaFold3 but not for Boltz-2 or Chai-1 (Figure 3), indicating that small-molecule inputs do not reliably steer predictions toward the expected functional state."
  6. p.18:
     > "Together with prior evidence of limited multimer performance in positioning small-molecule ligands, these results suggest that current predictors do not consistently encode small-molecule-driven induced-fit mechanisms at the level needed for state control."
  7. p.18:
     > "In contrast, protein-binding partners provide a stronger and more reproducible control signal, consistent with models responding more robustly to protein–protein interface geometry/contact density than to small-molecule chemistry."
  8. p.18:
     > "For β2AR, providing the agonist together with the heterotrimeric G protein shifted predictions toward the expected active conformation across predictors."
  9. p.18:
     > "with partner success likely reflecting sensitivity to the large translocase interface, rather than consistently encoding the mechanochemical coupling between nucleotide state and translocase engagement that drives the conformational cycle of SecA."
  10. p.18:
      > "even for canonical proteins in our benchmark, Boltz-2 does not reliably sample alternative conformational states without additional binding/affinity information."

  **On what cannot be done / what is insufficient (method-level):**
  11. pp.16–17:
      > "These results indicate that MSA-level manipulation alone, whether through evolutionary clustering or random subsampling, is largely insufficient to overcome the systematic conformational bias observed across the deep learning tools evaluated in this study."
  12. p.10:
      > "their predictions are bimodally distributed between closed and wide-open conformations, with no structures near the open reference state, indicating that these models cannot reproduce the conformational heterogeneity characteristic of apo SecA."
  13. p.6:
      > "Except BioEmu, which generated one structure 1.8 Å away, no tool successfully predicted structures resembling the IF reference state; most RMSD values to the IF state exceeded 3.5 Å"
  14. p.9:
      > "These two successful predictions represent the only instances across all tested models in which apo structure predictions approached the correct open conformation."
  15. p.9:
      > "However, despite this broader sampling, BioEmu did not predict the open apo state."
  16. p.17:
      > "Although BioEmu samples broader conformational distributions than the other predictors, its ensembles remain biased toward dominant states and generally fail to recover the alternative experimental conformations, complicating functional interpretation."
  17. p.15:
      > "Confidence metrics such as pLDDT and PAE are useful for local geometry and uncertainty, but they are not reliable selectors of biologically or physically meaningful alternative states."
  18. p.15:
      > "Deep-learning approaches now offer useful heuristics for ensemble generation, but these ensembles do not necessarily improve downstream docking and cannot yet provide thermodynamically consistent conformational landscapes."
  19. p.15:
      > "CASP15 and CASP16 showed that detailed multi-state prediction remains substantially weaker than single-state prediction, especially without templates and for larger assemblies or nucleic-acid-containing systems."
  20. p.10 (metric necessity):
      > "Because SecA conformational changes are primarily localized to the rotation of the PBD domain rather than global structural rearrangements, RMSD of the entire protein is insufficient to distinguish between open and closed clamp states."
  21. p.3 (framing, on AF2):
      > "However, AlphaFold2 and related predictors often return a single dominant conformational state, limiting their ability to capture conformational heterogeneity."

- **novelty_claims**: **NONE FOUND.** No claim to be first, novel, or unprecedented appears anywhere in the paper. The words "novel", "first", "unprecedented" and "to our knowledge" do not occur in the main text (searched full extracted text, pp.1–19). The strongest self-positioning statements are non-priority framings:
  > "We are therefore motivated to test whether these predictors can recover experimentally observed conformational states, and whether ligand or binding-partner specification improves conformational sampling beyond biases inherited from training data." (p.4)
  > "Here, we benchmark AlphaFold3, Boltz-2, Chai-1, and BioEmu on four canonical multi-state proteins (PfMATE, LAO, SecA, and β2AR), quantifying state bias and sampling breadth against experimental reference structures." (p.2)
  Notably the paper credits AF-Cluster, not itself, with the strongest demonstration in the area: "making it one of the strongest demonstrations that AlphaFold2 can be redirected toward functionally relevant alternative substates." (p.14)

- **stated_limits**: Authors' own limits, as stated:
  - Their central negative result is stated as a limitation of the field, not solved by them: "These results underscore current limitations for multi-state protein structure prediction and structure-guided ligand discovery." (p.2)
  - Partner-driven success may be an interface-size artefact rather than mechanism: "with partner success likely reflecting sensitivity to the large translocase interface, rather than consistently encoding the mechanochemical coupling between nucleotide state and translocase engagement" (p.18).
  - Model-dependence prevents a general statement: "For SecA, partner-driven effects were strongly model-dependent: Chai-1 and Boltz-2 succeeded only with SecYEG and ADP bound, whereas AlphaFold3 captured open and wide-open states under apo and ATP-bound conditions. This complementary failure pattern suggests that each model responds to different structural cues" (p.18).
  - The AF-Cluster baseline was underpowered for one target by MSA composition: "reflecting the low sequence diversity of the SecA MSA, which yielded only four DBSCAN clusters of size four to five sequences each." (pp.15–16)
  - Whole-protein RMSD is inadequate for SecA (p.10, quoted above) — a limitation of their own primary metric, acknowledged and worked around only for that one target.
  - Details deferred: "Complete protocols, parameters, and sampling details are provided in the Supporting Information." (p.18) — the SI is not part of this 30-page PDF; Tables S1 and S4 are cited (pp.7, 8, 12, 17) but not readable here.
  - **Not** stated as limits by the authors: the absence of any anti-memorization control; the n=4 target base under a general claim; the absence of a partner-without-agonist arm.

- **stance** (PROVISIONAL — user's call): **precedent on findings + contrast on rigour and scope.**
  - *precedent*: this is the closest published statement of the partner-drives-state / ligand-does-not result, on β2AR specifically, with all four modern backbones (pp.2, 13, 18). Any claim we make about partner-driven conformational switching has to be positioned against it.
  - *contrast*: the partner arm is only ever the **full-length heterotrimeric G protein together with an agonist** (p.18); no partial construct, no partner-without-ligand, no dissection of what part of the partner carries the signal; no anti-memorization control; 4 targets; success scored entirely by RMSD to structures inside the training window (pp.7, 18).

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| PfMATE, Chai-1, RMSD to OF | 0.79 ± 0.09 | Å | 6GWH (OF ref) | 5 |
| PfMATE, Chai-1, RMSD to IF | 5.10 ± 0.21 | Å | 6FHZ (IF ref) | 5 |
| PfMATE, Boltz-2, RMSD to OF | 0.74 ± 0.11 | Å | 6GWH | 5 |
| PfMATE, Boltz-2, RMSD to IF | 4.93 ± 0.26 | Å | 6FHZ | 5 |
| PfMATE, AlphaFold3, RMSD to OF | 0.57 ± 0.03 | Å | 6GWH | 5 |
| PfMATE, AlphaFold3, RMSD to IF | 5.42 ± 0.05 | Å | 6FHZ | 5 |
| PfMATE, BioEmu, RMSD to OF | 1.22 ± 0.40 | Å | 6GWH | 5 |
| PfMATE, BioEmu, RMSD to IF | 3.56 ± 0.90 | Å | 6FHZ | 6 |
| PfMATE, BioEmu, best single prediction to IF | 1.8 | Å | 6FHZ | 6 |
| PfMATE, IF-state failure threshold (descriptive) | > 3.5 | Å | 6FHZ | 7 |
| PfMATE, PDB state composition | 11 structures total, 1 IF (10:1 OF:IF) | count | PDB (Table S1) | 7 |
| LAO, AlphaFold3 apo-input, RMSD to holo | 0.20 ± 0.01 | Å | 1LAF (holo ref) | 7 |
| LAO, AlphaFold3 apo-input, RMSD to apo | 4.63 ± 0.03 | Å | 2LAO (apo ref) | 7 |
| LAO, Chai-1 apo-input, RMSD to holo | 0.29 ± 0.03 | Å | 1LAF | 7 |
| LAO, Chai-1 apo-input, RMSD to apo | 4.60 ± 0.06 | Å | 2LAO | 7 |
| LAO, AlphaFold3 holo-input, RMSD to holo | 0.22 ± 0.02 | Å | 1LAF | 7 |
| LAO, Chai-1 holo-input, RMSD to holo | 0.24 ± 0.02 | Å | 1LAF | 7 |
| LAO, Boltz-2 holo-input, RMSD to holo | 0.27 ± 0.03 | Å | 1LAF | 8 |
| LAO, Boltz-2 holo-input, RMSD to apo | 4.62 ± 0.04 | Å | 2LAO | 8 |
| LAO, Boltz-2 apo-input, RMSD to holo | 0.58 ± 0.75 | Å | 1LAF | 8 |
| LAO, Boltz-2 apo-input, RMSD to apo | 4.48 ± 0.74 | Å | 2LAO | 8 |
| LAO, Boltz-2 holo-input, pTM | 0.929–0.952 | — | model confidence (Table S4) | 8 |
| LAO, Boltz-2 apo-input, pTM | 0.729–0.856 | — | model confidence (Table S4) | 8 |
| LAO, Boltz-2 apo-input, successes | 2 of 50 approached open apo; 48 converged holo | count | 2LAO | 8 |
| LAO, BioEmu, RMSD to apo | 4.42 ± 0.63 | Å | 2LAO | 9 |
| LAO, BioEmu, RMSD to holo | 1.04 ± 1.36 | Å | 1LAF | 9 |
| LAO, BioEmu, min RMSD to apo | 2.27 | Å | 2LAO | 9 |
| SecA reference, 1M74 wide-open | 26.7 / 135.0 | Å / ° | PBD–HWD distance / PBD–hinge–NBD2 angle | 10 |
| SecA reference, 1TF2 open | 39.3 / 106.0 | Å / ° | same descriptors | 10 |
| SecA reference, 8YAS closed | 49.9 / 76.1 | Å / ° | same descriptors | 10 |
| SecA apo, AlphaFold3 | 29.4 ± 5.4 / 126.9 ± 10.0 | Å / ° | 1M74 (26.7 / 135.0) | 10 |
| SecA apo, AlphaFold3 reaching open state | 6 of 50 | count | 1TF2 | 10 |
| SecA apo, BioEmu, PBD–HWD distance | 45.1 ± 4.3 | Å | continuous, wide-open→closed | 10 |
| SecA +ATP, AlphaFold3, PBD–HWD distance | 26.6 ± 0.1 | Å | 1M74 (26.7 Å) | 10 |
| SecA +SecYEG/ADP, Chai-1, PBD–HWD distance | 49.3 ± 0.5 | Å | 8YAS (49.9 Å) | 11 |
| SecA +SecYEG/ADP, Boltz-2, PBD–HWD distance | 47.8 ± 0.5 | Å | 8YAS (49.9 Å) | 11 |
| SecA +SecYEG/ADP, AlphaFold3, PBD–HWD distance | 46.9 ± 7.7 | Å | 8YAS (49.9 Å) | 11 |
| SecA +SecYEG/ADP, pLDDT | 72–81 | — | model confidence (Table S4) | 12 |
| SecA apo, pLDDT | 76–86 | — | model confidence (Table S4) | 12 |
| **β2AR apo, Boltz-2, RMSD to inactive** | 2.12 ± 0.33 | Å | 9CHU (inactive ref) | 13 |
| **β2AR apo, Chai-1, RMSD to inactive** | 2.91 ± 1.00 | Å | 9CHU | 13 |
| **β2AR apo, BioEmu, RMSD to inactive** | 2.15 ± 0.46 | Å | 9CHU | 13 |
| **β2AR apo, AlphaFold3, RMSD to inactive** | 1.65 ± 0.05 | Å | 9CHU | 13 |
| **β2AR agonist + Gαβγ (± GTP), Boltz-2, RMSD to active** | 1.68 ± 0.33 | Å | 8GEG (active ref) | 13 |
| **β2AR agonist + Gαβγ (± GTP), Chai-1, RMSD to active** | 1.02 ± 0.07 | Å | 8GEG | 13 |
| **β2AR agonist + Gαβγ (± GTP), AlphaFold3, RMSD to active** | 0.74 ± 0.02 | Å | 8GEG | 13 |
| β2AR, agonist-alone condition, RMSD | **NOT REPORTED numerically** (described qualitatively only, p.14) | Å | 9CHU / 8GEG | 13–14 |
| β2AR, BioEmu cluster size | 20 predicted structures | count | Fig 4 caption | 12 |
| β2AR, agonist-induced binding-pocket shift (literature value, ref. 47) | ~1 | Å | experimental, cited | 13 |
| β2AR, G-protein-induced TM6 outward displacement (literature value, refs. 47–49) | ~14 | Å | experimental, cited | 13 |
| SecA AF-Cluster DBSCAN yield | 4 clusters, 4–5 sequences each | count | — | 15–16 |
| TM-score | computed with TM-align "to confirm global fold preservation" — **no values given** | — | — | 18 |

- **n_predictions**:
  - **Samples per target × condition**: 50 where stated — "Among 50 apo predictions" (LAO, Boltz-2, p.8); "a small fraction (6 out of 50)" (SecA apo, AlphaFold3, p.10). Not stated for the other model × condition arms; scatter density in Figs 1B, 2B, 3B, 4B is consistent with tens per arm but the number is not printed. BioEmu β2AR: "The small cluster generated by BioEmu shows 20 predicted structures" (p.12).
  - **Targets**: 4 (p.4).
  - **Conditions per target**: PfMATE 1 (apo/sequence only, Fig 1); LAO 2 (apo, holo/arginine, p.7); SecA 3 (apo, +ATP, +SecYEG/ADP, p.11 Fig 3 caption); β2AR 4 (apo, agonist, Gαβγ-agonist, Gαβγ-agonist-GTP, p.12 Fig 4 caption). BioEmu is run apo-only in every case (it takes no ligand or partner input; Figs 3B and 4B show only the apo series for BioEmu).
  - **Baseline arm**: AF-Cluster clusters + U10 + U100 across all four targets; per-strategy counts not stated except the SecA cluster count (4 clusters, pp.15–16).
  - **Total predictions**: **NOT REPORTED.** Deferred to SI (p.18) and to the Zenodo deposit (https://doi.org/10.5281/zenodo.20077837, p.20).

- **comparable_to_ours**: **Directly comparable on the β2AR arm — with one caveat that is the whole point.** Their per-condition β2AR RMSD-to-reference values (apo 1.65–2.91 Å to 9CHU; agonist+Gαβγ 0.74–1.68 Å to 8GEG, p.13) are the natural table-neighbours for any β2AR state-recovery number we report, since they use the same backbones (AF3 v3.0.1, Boltz-2, Chai-1), the same paired-reference RMSD scatter framing, and no templates/MSAs/restraints (p.18). **Caveat**: their only partner condition is the complete heterotrimeric G protein supplied as full-length sequences *together with* an agonist (p.18); they never run a partner without an agonist, and never run a partial G-protein construct. So any of our numbers for a reduced or partial partner has **no counterpart** in this paper and must be presented as filling that gap rather than as beating their value. Their PfMATE/LAO/SecA numbers are `NONE` for us unless we take up those systems.

- **si_in_scope**: **New in v3. SI NOT HELD, and it carries two things the main argument depends on.** **Table S1** holds the per-target distribution of PDB structures across conformational states — the quantity the paper's whole explanation rests on, cited at p.7 and again at p.17, and never reproduced in the main text beyond the single PfMATE 10:1 figure. **Table S4** holds the pLDDT values by condition (p.12 quotes ranges 72–81 and 76–86 from it). And p.19 states plainly: *"Complete protocols, parameters, and sampling details are provided in the Supporting Information."* So the sampling budget per condition, which determines how much any per-arm scatter can bear, is outside what this note can verify.

## F. Figures

Licence for all: **CC-BY-NC-ND 4.0** (p.1 and every page banner) — **ND clause: no derivatives.** Redrawing, re-plotting or adapting any panel is forbidden by the licence, not merely modification; reproduction requires attribution and is non-commercial only.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| TOC | 2 | Conceptual contrast: an experimental conformational landscape with apo/holo/intermediate basins populated, vs. AI predictions collapsing onto the holo basin | schematic | `SCHEMATIC \| two side-by-side landscape cartoons (experimental vs AI prediction) with apo / holo / inter basins, arrow between them \| no data` | 2 (experimental vs AI predictions) | | CC-BY-NC-ND 4.0, **ND**, p.1 |
| 1A | 6 | PfMATE OF (6GWH) and IF (6FHZ) reference structures, cartoon | structure render | `RENDER \| systems: 1 \| views: 2 (outward-facing reference, inward-facing reference) \| overlay: 0 predictions on 2 reference(s) \| axis: none` | 2 stacked, vary by state | | CC-BY-NC-ND 4.0, **ND**, p.1 |
| 1B | 6 | Paired-reference RMSD scatter, one panel per predictor, PfMATE | scatter | `PLOT \| facet: predictor (4) \| x: RMSD to inward-facing reference (continuous, 0–6 Å) \| y: RMSD to outward-facing reference (0–6 Å) \| mark: point + y=x diagonal \| n_per_cell: NOT REPORTED (~13 visible for BioEmu; 50/arm stated elsewhere, p.8/p.10)` | 4 (2×2), vary by predictor | n per panel never printed; BioEmu panel visibly carries far fewer points than the others with no explanation | CC-BY-NC-ND 4.0, **ND**, p.1 |
| 2A | 8 | LAO apo/open (2LAO) and holo/closed (1LAF) reference structures | structure render | `RENDER \| systems: 1 \| views: 2 (apo/open reference, holo/closed reference) \| overlay: 0 predictions on 2 reference(s) \| axis: none` | 2 stacked, vary by state | | CC-BY-NC-ND 4.0, **ND**, p.1 |
| 2B | 8 | Paired-reference RMSD scatter per predictor, two input conditions overlaid, LAO | scatter | `PLOT \| facet: predictor (4) \| x: RMSD to apo reference (0–7 Å) \| y: RMSD to holo reference (0–7 Å) \| mark: point coloured by input condition (2: apo, holo) \| n_per_cell: 50 for Boltz-2 apo (p.8), NOT REPORTED otherwise` | 4 (2×2), vary by predictor; colour varies by input condition | n per panel not printed; the two successful Boltz-2 apo points are single markers indistinguishable in size from the 48 failures, so the 2/50 success rate is not readable off the plot | CC-BY-NC-ND 4.0, **ND**, p.1 |
| 3A | 11 | SecA three reference states, cartoon (top) and surface (bottom), PBD rotation arrowed | structure render | `RENDER \| systems: 1 \| views: 2 (cartoon, surface) \| overlay: 0 predictions on 3 reference(s) \| axis: none` | 2 stacked, vary by representation | Three reference states are named in the caption (1M74/1TF2/8YAS) but the render shows one composite per representation, so the three states are not individually visible | CC-BY-NC-ND 4.0, **ND**, p.1 |
| 3B | 11 | Domain-geometry scatter per predictor, three input conditions overlaid, with the three reference states marked, SecA | scatter | `PLOT \| facet: predictor (4) \| x: PBD–HWD distance (Å, axis starts ~20) \| y: PBD–hinge–NBD2 angle (°, axis starts ~70) \| mark: point coloured by input condition (3: apo, +ATP, +SecYEG/ADP) + 3 reference symbols \| n_per_cell: 50 for AlphaFold3 apo (p.10), NOT REPORTED otherwise` | 4 (2×2), vary by predictor; colour varies by input condition | **Both axes truncated** (x from ~20 Å, y from ~70°) with no break marks and no caption note; n per panel not printed; the BioEmu panel carries only the apo series while the other three carry all three conditions, and neither caption nor legend says BioEmu cannot take ligand/partner input | CC-BY-NC-ND 4.0, **ND**, p.1 |
| 4A | 12 | β2AR inactive (9CHU) vs active (8GEG) references aligned, TM6 shift highlighted, side and cytoplasmic views | structure render | `RENDER \| systems: 1 \| views: 2 (side, cytoplasmic) \| overlay: 0 predictions on 2 reference(s), superimposed \| axis: none` | 2 stacked, vary by viewing direction | The ~14 Å TM6 displacement quoted in text (p.13) is shown only as an arrow; no scale bar or measured distance on the figure | CC-BY-NC-ND 4.0, **ND**, p.1 |
| 4B | 12 | Paired-reference RMSD scatter per predictor, four input conditions overlaid, β2AR | scatter | `PLOT \| facet: predictor (4) \| x: RMSD to inactive reference 9CHU (0–6 Å) \| y: RMSD to active reference 8GEG (0–6 Å) \| mark: point coloured by input condition (4: apo, agonist, Gαβγ-agonist, Gαβγ-agonist-GTP) + y=x diagonal \| n_per_cell: 20 for the BioEmu cluster (caption, p.12), NOT REPORTED otherwise` | 4 (2×2), vary by predictor; colour varies by input condition; AlphaFold3 panel additionally carries 2 zoom insets | n per condition per panel not printed; **caption/text colour mismatch** — caption calls Gαβγ-agonist-GTP "green" (p.12) while the rendered legend and the text (p.13, "blue, purple") show purple, and the text calls the apo series "yellow dots" (p.13) where the caption says "orange"; the AlphaFold3 panel needs two magnified insets to resolve its clusters at all, so the main panel understates the spread it contains; the BioEmu panel carries only the apo series with no note that BioEmu takes no ligand or partner input; the agonist-only condition has no separate quantitative value anywhere in text or caption | CC-BY-NC-ND 4.0, **ND**, p.1 |
| 5A-B,D | 16 | AF-Cluster vs U10 vs U100 predictions on paired-reference RMSD axes, for PfMATE, LAO, β2AR | scatter | `PLOT \| facet: system (3: PfMATE, LAO, β2AR) \| x: RMSD to state-1 reference (Å) \| y: RMSD to state-2 reference (Å) \| mark: point by sampling strategy (3: Cluster, U10, U100) + y=x diagonal \| n_per_cell: NOT REPORTED` | 3 of a 4-panel grid, vary by system; symbol/colour varies by sampling strategy | n per strategy not printed; LAO panel y-axis capped at 6 Å where the same quantity was plotted to 7 Å in Fig 2B, so the two LAO figures cannot be visually compared | CC-BY-NC-ND 4.0, **ND**, p.1 |
| 5C | 16 | AF-Cluster vs U10 vs U100 predictions on SecA domain-geometry axes with three reference states marked | scatter | `PLOT \| facet: none (1) \| x: PBD–HWD distance (Å, axis starts ~30) \| y: PBD–hinge–NBD2 angle (°, axis starts ~75) \| mark: point by sampling strategy (3: Cluster, U10, U100) + 3 reference symbols \| n_per_cell: 4 DBSCAN clusters of 4–5 sequences (p.16); U10/U100 counts NOT REPORTED` | 1 (panel C of a 4-panel grid), no faceting within | **Both axes truncated** (x from ~30 Å, y from ~75°) with no break marks and no caption note; n per strategy not printed | CC-BY-NC-ND 4.0, **ND**, p.1 |

## G. Provenance

- **extracted_on**: 2026-09-07; **re-passed to schema v3 on 2026-09-09**
- **extractor**: claude subagent
- **schema_version**: `v3` — re-passed 2026-09-09 against the PDF, not patched. The three v2-missing fields (`structural_priors_used`, `controls_run`, `si_in_scope`) were extracted fresh; every added quote was machine-verified. **The A–E content of the v2 pass was checked and stands.** The U10/U100 arm, which v2 recorded inside `anti_memorization_control` because it had nowhere else to go, is now in `controls_run` where it belongs; the `anti_memorization_control` verdict of NONE RUN is unchanged and correct.
- **confidence**: **high** on text, claims, conditions and numbers — the paper is short (19 pages of content), the Methods are explicit, and every number in section E is printed in the running text. **medium** on figure panel counts and n-per-panel: five figure pages (2, 6, 8, 11, 12, 16) were rendered at 110 dpi and read directly, so panel structure and axis ranges are firsthand, but no figure prints n and point counts could only be eyeballed. **low** on anything routed to the Supporting Information: Tables S1 (PDB state composition per target) and S4 (pTM/pLDDT tables) are cited on pp.7, 8, 12 and 17 but the SI is **not part of this 30-page PDF**, so sampling counts, per-arm confidence values and the per-target PDB census could not be verified.
- **unresolved**:
  1. **β2AR input conditions — the absence is the finding.** The complete condition list appears twice, on **p.13** in the text and on **p.12** in the Fig 4 caption, and both give exactly four: *apo*, *agonist*, *agonist-Gαβγ*, *agonist-Gαβγ-GTP*. Therefore, explicitly:
     - **They never ran a G protein WITHOUT an agonist.** No Gαβγ-only, no partner-only condition exists in the list on p.13 or the legend on p.12. Every partner-containing condition also contains the agonist.
     - **They never ran any PARTIAL G-protein construct.** No isolated α5 helix, no α5 C-terminal peptide, no mini-G protein, no nanobody, no Gα-only or Gs-peptide arm appears anywhere in the paper. The words "nanobody", "mini-G", "α5" and "alpha5" do not occur in the text (full-text search, pp.1–19). The partner is always the complete heterotrimer: "protein binding partners (SecYEG; heterotrimeric G protein) were provided as full-length sequences" (**p.18**, Methods).
     - Consequence: the paper's partner-drives-state claim (pp.2, 13, 18) is supported only for the full heterotrimer plus agonist. Nothing in it separates "a large protein interface" from "the specific G-protein interface", and nothing in it tests whether a smaller construct suffices — despite the fact that its own necessity claim on p.13 ("Full activation requires engagement with the heterotrimeric G protein") is a claim about exactly that.
  2. **Agonist-alone β2AR outcome is qualitative only.** The apo condition gets per-model RMSD means (p.13) and the partner conditions get per-model RMSD means (p.13), but the agonist-alone condition never receives its own number. It is described only in prose: "baseline apo and agonist-only predictions (yellow, pink)" that "remained intermediate between the two reference structures rather than cleanly adopting the inactive conformation" and "a few apo and agonist-only Chai-1 predictions also fell near the active-state clusters" (pp.13–14). Whether the p.13 apo averages include or exclude the agonist-alone runs cannot be determined; "all baseline predictions (yellow dots) without user-specified ligands" (p.13) reads as apo-only, but the phrase "baseline predictions" is used for apo+agonist together one paragraph later (p.14).
  3. **Whether the p.13 partner averages pool the two partner conditions.** "When provided with the partners and ligands required for activation of β2AR (i.e., agonist and G protein), all predictions clustered tightly toward the active conformation (average RMSD: Boltz-2, 1.68 ± 0.33 Å; Chai-1, 1.02 ± 0.07 Å; AlphaFold3, 0.74 ± 0.02 Å)" (p.13) does not say whether Gαβγ-agonist and Gαβγ-agonist-GTP are pooled or whether one is quoted. The caption notes "AlphaFold3 predictions of Gαβγ-Agonist overlap with Gαβγ-Agonist-GTP" (p.12), which suggests pooling is harmless for AF3 but says nothing about Boltz-2 or Chai-1, whose Fig 4B panels show the two series in visibly different positions.
  4. **Colour key inconsistency in Fig 4.** The caption (p.12) assigns "Gαβγ-agonist-GTP (green)" and "apo (orange)"; the rendered legend shows purple and orange respectively, and the text (p.13) calls apo "yellow dots" and the partner series "(blue, purple)". The mapping is recoverable from the legend but the caption is wrong as printed.
  5. **BioEmu's condition coverage is never stated.** BioEmu appears with only the apo series in Figs 3B and 4B, and only apo numbers are quoted for it (pp.10, 13). The paper never states that BioEmu accepts no ligand or partner input; it must be inferred from the figures.
  6. **Sample counts.** n = 50 per arm is stated only twice (pp.8, 10) and n = 20 once for a BioEmu β2AR cluster (p.12). Whether 50 is the universal per-arm sample size, and what the totals are, is deferred to the SI (p.18) and Zenodo (p.20), neither of which is in this PDF.
  7. **TM-score values.** TM-align was run "to confirm global fold preservation" (p.18) but no TM-score is reported anywhere in the main text.
  8. **Tag vocabulary gaps** (needed, could not be used — reported rather than invented):
     - No tag for a **generative ensemble emulator trained on MD** (BioEmu). `md` is wrong (no simulation was run here), `enhanced-sampling` is wrong, `cofolding` is wrong. BioEmu is a fourth of this paper's backbone set and currently untaggable.
     - No tag for the **no-template / no-MSA / no-restraint input regime**, which is this paper's defining protocol choice (p.18) and the thing that distinguishes it from every template- or MSA-biasing paper in the corpus. `msa-subsample` and `msa-state-filter` both misdescribe it.
     - No **system** tag for the non-GPCR, non-kinase, non-transporter targets (LAO periplasmic binding protein; SecA ATPase). Both are folded into `general-protein`, which loses that they are specific multi-state benchmark systems.
     - No tag for **partner-without-ligand** or **partial-partner** conditions, which is precisely the axis on which this paper's coverage is empty; there is no way to record the *absence* as a searchable fact.
- **why_it_matters**:

## Tags

`gpcr` `transporter` `general-protein` `benchmark-only` `cofolding` `af-cluster` `msa-subsample` `ensemble` `single-state` `rmsd-only` `continuous-metric` `saturating-metric` `oracle-leak` `no-anti-memorization` `multi-backbone` `directed-state` `partner-driven` `ligand-driven` `apo-sampling` `orthosteric` `preprint` `precedent` `contrast` `negative-result` `comparator-numbers`

Tag notes (not tags): `ensemble` + `single-state` are both applied deliberately — the paper *produces* distributions (20–50 samples per arm) but those distributions *contain* one state in most arms; the vocabulary has no single tag for "sampled ensemble that collapses". `saturating-metric` is applied for the RMSD floor at 0.20 ± 0.01 Å in the LAO holo arms (p.7), which makes apo and holo input conditions unresolvable there. `prospective` is deliberately **not** applied. `confidence-as-discriminator` is deliberately **not** applied: pTM/pLDDT are reported (pp.8, 12) but explicitly disclaimed as state selectors (p.15) and never used to make a state call.
