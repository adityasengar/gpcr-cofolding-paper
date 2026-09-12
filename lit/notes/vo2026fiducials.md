# vo2026fiducials

> Extraction note, SCHEMA.md v3. Quotes are verbatim from the PDF text layer.
> **Greek letters are degraded in that layer:** β renders as `b`, α as `a`, π as
> `p`, μ as `µ`. Quotes are reproduced exactly as the layer emits them (so
> "b2AR", "a5 helix", "cation-p") rather than silently corrected; where a quote is
> reproduced with restored Greek this is stated inline. No other alteration.
>
> **This is a structural-biology paper with a computational design front end.**
> It is not a conformational-state predictor. Several section C fields presuppose
> a generative structure-prediction method and are marked `NOT APPLICABLE` with a
> reason. The one thing in it that a state-prediction corpus needs — an
> experimental test of whether co-folding models capture ligand-induced GPCR
> conformational change, and an experimental observation of an active-like
> intracellular arrangement without a G protein — is real and is quoted verbatim
> below.

---

## A. Identity

| Field | Value |
|---|---|
| `citekey` | `vo2026fiducials` |
| `doi` | https://doi.org/10.64898/2026.01.24.701540 (bioRxiv) (p1) |
| `year` | 2026 — "this version posted January 26, 2026" (p1) |
| `venue` | bioRxiv preprint, "which was not certified by peer review" (p1). Tagged `preprint`. |
| `title` | Designing Rigid Protein Fiducials to Visualize GPCR Conformational States |
| `authors` | Alina Vo, Yuan-En Sun, Justin G. English, Michael J. Robertson (Baylor College of Medicine; University of Utah School of Medicine). Corresponding: michael.robertson@bcm.edu (p1). |

## B. Scope

| Field | Value |
|---|---|
| `system` | GPCR. Family A (MRGPRX2, MC2R, V1AR, β2AR), family B1 (GIPR); benchmark set additionally includes FZD5 (family F, as a fiducial-fusion test case), a GABA(A)R megabody complex and an LptDE macrobody complex used only as fiducial-rigidity references (p3, p16). |
| `n_targets` | **Three distinct counts, kept separate.** (1) **Prospective design targets: 5 receptors** — MRGPRX2, MC2R, V1AR, GIPR (ICL3 fusions, p4) and β2AR (extracellular TM1 fusion, p6). (2) **Constructs designed:** "We produced 3-5 constructs for each receptor" for the four ICL3 targets (p4) and "five designs were selected" for β2AR (p6). (3) **Rigidity-benchmark set:** 5 published fiducial systems with raw EMPIAR data (FZD5-BRIL, 6DS-Fab, Fab, Mb25, Mb6; Fig. 1b p3, EMPIAR codes p16) plus further cases assessed from crystal asymmetric units or maps alone (macrobodies, megabodies, SMO-PGS2; p3–p4, Extended Data Fig. 1–2, **not in this PDF**). **Generality claim on a GPCR-only dataset:** "although we applied this framework exclusively to GPCRs, the approach should facilitate cryoEM structure determination for a broad range of proteins" (p10). |
| `method_class` | **Dual, and neither half is a state predictor.** `other` (generative protein design — RFdiffusion inpainting + ProteinMPNN — coupled to cryoEM structure determination) `+` `MD` (rigidity reference and TM6/ICL3 hypothesis test) `+` an AF2-ensemble-sampling component (dropout at inference, multiple seeds) used as a **rigidity filter on the designed fusion**, not as a receptor-state generator. `cofolding` appears **only as an evaluated comparator** (OF3, Chai-1, Boltz-2), never as the paper's own method. |
| `backbones` | **Design/ensemble:** AF2 (ref 15) via ColabFold (ref 20); RFdiffusion (ref 13); ProteinMPNN (ref 23); AlphaFold-Multistate (ref 57, Heo & Feig) for GIPR only (p17). **Comparators run and reported:** OpenFold3 (OF3), Chai-1, Boltz-2 — "the predictive power of protein-ligand 'co-folding' models (OpenFold3 (OF3), Chai-1, Boltz-2<sup>24-27</sup>)" (p2). AlphaFold3 (ref 25) is cited inside that citation bracket as background but is **never reported as run**. Three co-folding backbones compared head to head → tagged `multi-backbone`. |
| `templates` | **NOT REPORTED for the AF2/ColabFold runs** — the AF2 methods paragraph (p17) specifies seeds, dropout and MSA depth but never says whether templates were on or off. **State-annotated for one case:** AlphaFold-Multistate with "an inactive-GPCR bias" was used for GIPR (p17). **NOT REPORTED for the co-folding comparators** — the Methods contain no paragraph at all describing how OF3, Chai-1 or Boltz-2 were run (no versions, seeds, MSA settings, template settings, or whether the predictions were made before the structures were solved). |
| `msa_handling` | **full (production) + subsampled (benchmark only) — the two are not collapsed.** Production design used full-MSA AF2 with dropout at inference and 3 seeds: "Ensemble prediction for the designed sequences was performed with AF2 implemented in ColabFold with dropout enabled and three random number seeds" (p17). Subsampling was tested only in the benchmark sweep: "limiting the depth of the MSA sampling ranging from 16:32 to 256:512" with 50 seeds per approach (p17). **Not state-filtered** — no state-specific alignment is substituted anywhere. The paper explicitly rejects deep subsampling: "overly limiting the MSA component risked producing unlikely if not completely misfolded structures" (p4). |

## C. Conformational core

### `states_generated`

**Dual, and the two halves belong to different modalities.**

`ensemble (computational — fiducial/target rigid-body geometry only)` **+** `NOT APPLICABLE for receptor conformational states — the receptor states were determined experimentally by cryoEM, not generated`.

- The AF2-dropout component produces an ensemble, but of *the angle between the receptor and the fused fiducial*, not of receptor conformational states: "Analysis of the distribution of the number of structures with a given target-fiducial marker angle" (p4). Ensembles are 15 models per design ("3 random number seeds", "the top scoring ~10/15 models... all 15 models were tightly converged", p17), and 50 seeds per approach in the benchmark sweep (p17).
- The receptor states that the paper's headline rests on are **experimental**: four inactive-state antagonist complexes (p4), and β2AR-BB3 in four conditions — propranolol (antagonist), BI-167107 (high-efficacy agonist), LM-189 (Gi-biased agonist), and BI-167107 + wildtype Gs (p7).
- 3DVA on the cryoEM data produces conformational **ensembles from experimental particles** (p3, p9), a third distinct sense of "ensemble" that should not be conflated with the AF2 one.
- The one case where an *inactive receptor state* was deliberately generated computationally is GIPR, via AlphaFold-Multistate (p17) — see `oracle_leakage` routes 2 and 7.

### `structural_priors_used`

Substantial, entirely at design/interpretation time, and **not a defect** — a designed binder necessarily starts from a solved or predicted structure of its target. Recorded so that anyone reusing the pipeline inherits them knowingly.

1. **Deposited structures as the starting scaffold for fiducial design.** RFdiffusion inpainting is run onto the receptor: "Fusion proteins were designed in RFdiffusion. Designs were typically generated in 2-5 rounds of 50-150 residues. Sidechain design was performed with ProteinMPNN with the sequence for the receptor held fixed" (p17). The receptor coordinates that anchor this are not itemised per target.
2. **Deposited structures as MD starting points.** "systems were prepared from deposited PDB structures when a full structure was available (FZD5, Fabs, megabodies with crystal structures, macrobodies with crystal structures) or AF2 predictions when it was not (some megabodies)" (p16).
3. **A deposited β2AR-Gs structure as a model-building prior.** "The AF2 predicted structure was docked for all initial structures of fiducial marker complexes, while PDB:8DGZ was also used for the Gs complex" (p20).
4. **AlphaFold-Multistate with an inactive-GPCR bias for GIPR** (p17) — a state-annotated prior, described in full under `oracle_leakage` route 2.
5. **A benchmark set assembled because its answers are already known.** The rigidity test set is deliberately chosen to span known outcomes: "we assembled a test set of fiducial markers that have been imaged in cryoEM (comprised of both fully native proteins and engineered) spanning from rigid to extremely flexible, including two example pairs where an attempt was made to rigidify a fiducial marker that was found to be too dynamic" (p2–p3). EMPIAR accessions listed at p16.
6. **Deposited reference structures used throughout for interpretation** (not fed to any model): PDB 7VV6 and 7S8L/7SGL (MRGPRX2 active states, p5), 6W25 (MC4R, p5–p6), 6TPK (OTR, p6), 7RA3 (GIPR-GIP, p6), 9BUY (β2AR-LM189-Gi, p9), 8DGZ (β2AR-Gs, p20).
7. **Fiducial rigidity acceptance criterion is self-referential, not oracle-based:** "The predicted ensemble of structures was aligned and assessed for a low RMSD, particularly amongst the top scoring ~10/15 models" (p17) — RMSD among the model's own predictions, with no reference structure involved.

### `oracle_leakage`

Seven routes, answered separately. Framing note: this is largely a wet-lab paper, so the routes bite mainly on (a) the AF2-based rigidity filter and (b) the co-folding comparison, which is the part of the paper our corpus cares about.

**Route 1 — structures used as input or template.**
**PRESENT, and legitimate by construction, for the design pipeline.** The receptor structure is the design substrate (RFdiffusion inpainting with "the sequence for the receptor held fixed", p17); MD systems start from deposited PDBs (p16); model building docks the AF2 prediction and, for the Gs complex, PDB:8DGZ (p20).
**NOT REPORTED for the co-folding comparison.** The Methods contain no description of how OF3, Chai-1 or Boltz-2 were run. Whether templates or the deposited relatives of each receptor (7VV6, 7S8L, 6W25, 6TPK, 7RA3, 9BUY, and the many β2AR entries) were available to those models is nowhere stated. This is the single largest reproducibility gap in the paper and it sits exactly on the claim we want to use.

**Route 2 — state annotations from a curated database driving templates or alignments.**
**PRESENT for one target, GIPR, and stated plainly.** "For GIPR the same procedure was performed with a marginally relaxed criteria for convergence (due to the predictions producing almost exclusively active conformations of TM6) followed by AlphaFold-Multistate prediction with 5 random seeds and an inactive-GPCR bias to generate an ensemble for an inactive TM6 conformation with more stringent acceptance" (p17). AlphaFold-Multistate (ref 57, Heo & Feig) is a state-annotated-template method; the paper does not name GPCRdb but the state bias is imported from that lineage. **NONE FOUND for the other four receptors** — protocol described at p17, with no database-derived state annotation.

**Route 3 — cluster labels derived from known states.**
**NONE FOUND.** No clustering step exists anywhere. 3DVA (p19) clusters cryoEM particles, but on experimental data with no state labels supplied; classification for GIPR used "a class with and without the ECD present (obtained from 3DVA)" (p20), i.e. a map feature, not a known state.

**Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states.**
**PRESENT at the level of method selection, on a known-answer benchmark, and disclosed.** The choice of dropout over MSA subsampling was made after sweeping both against a set whose cryoEM flexibility was already known: "AF2 with dropout enabled was chosen for prospective design as a balanced solution, avoiding spurious structures and potential MSA issues for our engineered proteins while enhancing sampling, although several of the tested parameters likely would have been equally effective" (p4). The sweep range itself — "50 random number seeds were used for each sampling approach, which included default AF2, the use of dropout, and limiting the depth of the MSA sampling ranging from 16:32 to 256:512" (p17) — was exercised on that evaluation set. **Mitigating and worth stating:** the benchmark targets (published fiducial complexes) are disjoint from the prospective design targets (five GPCR fusions never built before), so this is method selection on a separate set, not per-target tuning. The stopping criterion for design acceptance was then relaxed for one target, GIPR, on the basis of the answer it was producing (p17) — that is per-target criterion adjustment and belongs here as well as under route 7.

**Route 5 — success defined post hoc by RMSD or TM to a structure they had.**
**Design side: NONE FOUND.** Design success is defined by wet-lab readouts declared in advance — FSEC behaviour, then map resolution: "with every design imaged in cryoEM yielding at least a 3.4 Å map" (p4). No RMSD-to-reference gate.
**Co-folding side: PRESENT, and this is the honest kind.** Co-folding accuracy is scored by RMSD/overlay against the authors' own new cryoEM structures — "a heavy-atom RMSD for the top ranked pose with Boltz-2 of ~3.2 Å" (p6). The reference is a structure the *authors* determined, not one the predictor could have trained on, which is what makes the comparison worth anything. **But the paper never states whether the co-folding predictions were run before or after the structures were solved**, so blindness cannot be asserted.

**Route 6 — best/worst model labels assigned against a held reference.**
**PARTIALLY PRESENT and under-specified.** The paper repeatedly reports "the top Boltz-2 predicted structure" (Fig. 3c, 3f, 3g captions, p5) and "the top ranked pose with Boltz-2" (p6). Ranking appears to be by the model's own confidence rather than by agreement with the reference, but this is never stated. Nor is it stated how many predictions per system were generated, so "the top" cannot be audited. AF2 model selection on the design side is by pLDDT rank ("the top scoring ~10/15 models", p17), a self-confidence ranking with no reference involved.

**Route 7 — design-level oracle use (input conditions or systems chosen because the expected answer is known). Weaker than pipeline leakage; labelled as design-level.**
**PRESENT, in two places, both disclosed.**
(i) **GIPR:** the expected inactive state was declared before the result was accepted — the acceptance criterion was relaxed and a state-biased predictor substituted precisely because "the predictions producing almost exclusively active conformations of TM6" was judged wrong in advance (p17).
(ii) **β2AR ligand panel:** the ligands were chosen with their pharmacology known — an antagonist, a "extremely potent and efficacious agonist", and a "Gi-based agonist" (p7) — so the expected direction of the intracellular rearrangement was fixed before the maps were read. The receptor was chosen for the same reason: "given its status as one of the most prototypical and well-studied family A GPCRs with numerous well characterized ligands and extensive exploration with spectroscopic studies" (p6). This is normal structural biology, not a fault, but it means the β2AR result is a *confirmation with structural detail*, not a blind prediction.
**Not present for the four ICL3 targets**, which were genuinely prospective designs against receptors with no prior inactive-state structure of this kind.

### `prospective`

**partial — and the two halves fall on opposite sides.**
**Prospective:** the fiducial design campaign. "To test the robustness of our approach prospectively, we designed 13-25 kDa fusion proteins for four GPCRs" (p4); the outcome (map resolution) was unknown when the designs were committed, and the negative control (β2BB5) was carried through to imaging rather than dropped.
**Retrospective / not established:** (a) the AF2-sampling method choice, made on a benchmark of already-imaged fiducials (route 4); (b) the co-folding comparison, whose blindness is **NOT REPORTED** — the reference structures are new, which is the important half, but there is no statement that predictions preceded structure determination; (c) the GIPR inactive-state prediction, where the expected answer drove the protocol (route 7).

### `state_metric`

**Dual: `visual only` + `continuous coordinate`.**
- **Visual only** for every receptor-state call. Active-like vs inactive is decided by structural overlay and described in prose — "induces almost complete outward movement of TM6" (p8), "a substantial shift in the motif to nearly match the Gs-bound result" (p9), "TM6 was predicted to either occupy an entirely inward conformation (Boltz-2, OpenFold 3) or outward (Chai-1)" (p9). **No operationalised predicate, no threshold, and no RMSD is given for any of the TM6 or ICL2 comparisons.** This is the paper's principal rigour defect for our purposes: the headline co-folding failure is stated categorically but never quantified in the main text.
- **Continuous coordinate** where MD is involved: TM4–TM6 distance, "measured with VMD taking the distance between the backbone nitrogen of L6.28 and N4.40" (p17), reported as distributions peaked at ~39 Å (extended-TM6 start) and ~38 Å with a low-value shoulder (cryoEM-based start) (p9). Fig. 5b marks "TM4-TM6 distances corresponding to a fully open and fully closed extended TM6" with dashed lines (p8) — reference markers, **not thresholds, and their derivation is not stated**.
- **RMSD-to-reference** appears exactly once, for a ligand pose, not a state: "~3.2 Å" heavy-atom RMSD for the top Boltz-2 CRN04894 pose (p6).
- Fiducial rigidity, the quantity the AF2 filter actually predicts, is judged by "a low RMSD" among the model's own predictions with **no stated cutoff** (p17), and by angular spread annotated on Fig. 1b in Å (p3).

### `metric_saturation`

**NONE FOUND (numeric).** No metric reported in the main text floors or ceilings: map resolutions span 3.1–3.4 Å and better (p4, p7), the ligand RMSD is a single mid-range value, and the TM4–TM6 distributions occupy the interior of a 26–44 Å axis (Fig. 5b, p8). *The unlabelled "Population" axis of Fig. 5b is a figure defect, recorded in the `hides` column of the F table, not here.*

### `directional_control`

**The fiducial reports; it does not select — and the paper argues this is the point.** Answered in four parts because the handle differs by component.

1. **The extracellular β2AR fiducial (β2BB3) does not select a state.** Its design purpose is the opposite: to add alignable mass while "leaving the intracellular vestibule of the receptor completely native" (p10), so the receptor's own equilibrium is read out rather than displaced. Two lines of evidence are offered that it is pharmacologically inert: "testing in TRUPATH BRET assays demonstrated signaling similar to the wildtype receptor, with an EC50 for epinephrine within one log unit of the WT b2AR for both BB3 and BB5" (p6), plus surface-expression ELISA (p20–p21). The fiducial fuses to TM1 on the extracellular side, away from the intracellular motifs being measured.
2. **The conventional ICL3 fiducials that this paper is displacing DO select a state, and the paper says so:** "in the case of GPCRs, fiducial markers almost exclusively bind or fuse to intracellular loop 3 (ICL3), masking the native conformation, biasing the receptor towards the inactive state, and requiring experimental optimization" (p1). The four high-throughput structures in this paper use exactly such ICL fusions and are all inactive-state (p4) — so for those four targets the construct is a state-selecting handle, and the resulting "inactive state" is partly imposed.
3. **What actually directs the β2AR state is the ligand, and secondarily the transducer.** The named handles are: antagonist (propranolol), high-efficacy agonist (BI-167107), Gi-biased agonist (LM-189), and wildtype Gs heterotrimer (p7). No mimetic and no nanobody is used for β2AR.
4. **On the computational side there is essentially no directional control, by design.** AF2 dropout sampling is seed-driven with no state handle. The single exception is GIPR, where AlphaFold-Multistate supplied "an inactive-GPCR bias" (p17) — a state-annotated template handle, used to force the inactive TM6 conformation the design required.

### `input_factor_design`

**New in v3.2. HELD — the two MSA regimes never meet the co-input arms.**

- **MSA**: full for production design (ColabFold, dropout, 3 seeds); subsampled 16:32–256:512
  **in the benchmark sweep only** (p17). The paper rejects deep subsampling outright — "overly
  limiting the MSA component risked producing unlikely if not completely misfolded structures" (p4).
- **templates**: **NOT REPORTED** for the AF2/ColabFold runs and for the co-folding comparators;
  state-annotated for one case only (AlphaFold-Multistate with an inactive-GPCR bias, GIPR, p17).
- **ligand**: present. **partner**: present.

`crossings:` **MSA × ligand and MSA × partner both HELD.** Subsampling lives in the benchmark arm,
the co-inputs live in the production arm, and the note records that the two are "not collapsed".
Despite carrying `msa-subsample`, `ligand-driven` and `partner-driven` together, this paper crosses
none of them — it is the clearest demonstration that a tag combination in `INDEX.md` must not be
read as a crossing.

### `anti_memorization_design`

**Present in substance, absent in framing — the paper never uses the concept.**
The seven-or-so structures determined here (MRGPRX2-E23, MC2R-CRN04894, V1AR-SRX246, GIPR-GIP(5-31*), β2BB3-propranolol, β2BB3-BI-167107, β2BB3-LM189, β2BB3-BI-167107-Gs) were **not in the PDB when the co-folding models were trained**, since they are first reported here ("The atomic coordinates have been deposited in the Protein Data Bank", p11, future/at-publication). That makes the co-folding comparison a de facto post-cutoff test set of **n ≈ 4 small-molecule/peptide complexes plus 3 β2AR ligand complexes**.
**But: no cutoff is defined, no training-date argument is made, and no model versions are given** (p2, p9 — the only places co-folding is described). And the *receptors* are far from novel to those models: active-state MRGPRX2 (7VV6, 7S8L), MC4R (6W25), OTR (6TPK), GIPR-GIP (7RA3) and dozens of β2AR entries are all deposited and cited by the authors themselves (p5–p9). So the fold is memorisable even where the complex is not — which is consistent with the reported failure mode, where the receptor is predicted "fairly accurately" and the ligand-induced change is not (p6, p9).

### `anti_memorization_control`

**NONE RUN, and `UNPOWERED` if the de facto set is treated as one.**
No control arm was run: there is no pre-cutoff comparison set, no matched arm of already-deposited complexes run through the same co-folding protocol, and no per-target statistics. The de facto post-cutoff set is n ≈ 4 (small molecules) or n ≈ 7 (all complexes), well below the ~10 threshold, and the underlying receptor folds overlap training. Every co-folding conclusion in the paper rests on visual comparison of a handful of cases (p5, p6, p9), with all supporting panels in Extended Data Figures 4b,c and 7a — **which are not in this PDF**.

### `controls_run`

| control | what it rules out | page |
|---|---|---|
| Triplicate 500 ns MD as an independent rigidity reference against 3DVA | That AF2-ensemble/cryoEM agreement is coincidental; supplies a physics baseline that does not share AF2's failure modes | p3, p16–p17 |
| pLDDT in the inter-domain linker, run as a competing rigidity metric | That a cheaper confidence score would have sufficed — it fails in both directions (rigid FZD5-BRIL with poor pLDDT; flexible Fab with good linker pLDDT) | p2, p4 |
| Matched rigidified/non-rigidified pairs (Fab vs disulfide-constrained 6DS-Fab; macrobodies with engineered prolines vs parent) | That the predictor tracks protein identity or size rather than the engineered rigidification itself | p2–p3 (Fig. 1b) |
| **Prospective negative-design control: β2BB5, selected because it was predicted flexible, carried through to imaging alongside β2BB3** | That the rigidity filter is post-hoc rationalisation — a design predicted flexible failed at 2D classification as predicted: "2D class averages... suggested the fiducial for b2BB3 to be sufficiently rigid for alignment while b2BB5 was not" | p6–p7 (Fig. 4a,b) |
| TRUPATH BRET dose-response for WT β2AR vs BB3 vs BB5 | That the extracellular fiducial perturbs receptor pharmacology — EC50 within one log unit of WT | p6, p20 (Extended Data Fig. 5b, not in PDF) |
| Cell-surface expression ELISA (anti-FLAG) for WT, BB3, BB5 | That fusion effects are trafficking/expression artifacts rather than signalling | p20–p21 |
| **No-G-protein arm: β2BB3-BI-167107 solved without Gs, alongside the same complex with wildtype Gs** | That the observed intracellular rearrangement requires the transducer — isolates the ligand's contribution from the G protein's | p7–p8 (Fig. 5a) |
| Antagonist arm: β2BB3-propranolol as the matched inactive reference | That the agonist-bound arrangement is a construct artifact rather than a ligand response | p7–p8 (Fig. 5a,e) |
| MD started from the ~40° tilted fiducial conformation, in a lipid bilayer | That the tilted fiducial state is physiological — it "rapidly converted to the predicted conformation", implicating the detergent micelle | p8 (Extended Data Fig. 5d, not in PDF) |
| MD from extended-TM6 vs cryoEM-like TM5-ICL3-TM6 starting models, 5 replicates × 1 µs | That the DEER/smFRET discrepancy reflects real extra TM6 opening rather than spin-label placement plus ICL3 flexibility | p9, p17 (Fig. 5b) |
| 3DVA on the receptor–fiducial junction for all four ICL3 fusions | That residual fiducial flexibility is degrading the receptor density — "3DVA further resolved little heterogeneity in the connection between the receptor and fiducial" | p4 (Extended Data Fig. 4a, not in PDF) |
| Crystal asymmetric-unit consistency as a third, independent flexibility readout | That the flexibility ranking depends on the 3DVA method | p3 (Extended Data Fig. 1c, not in PDF) |
| Reported failure case retained rather than dropped: SMO-PGS2, where the AF2 ensemble approach failed | That the method's success rate is inflated by silent exclusions; the authors diagnose it as "a failure to predict the correct structure at all" | p4 |
| HR-HAIR reprocessing where non-uniform refinement produced apparent preferred orientation | That the reconstructions carry orientational artifacts masquerading as conformational features | p19 |
| Three co-folding backbones run rather than one (OF3, Chai-1, Boltz-2) | That the co-folding failure is one model's idiosyncrasy — though the three disagree with each other on TM6 direction, which cuts both ways | p2, p9 |

### `confidence_as_discriminator`

**Yes, in two opposite senses, and the negative one is the more useful.**

**Used, and validated as a poor discriminator, for rigidity.** pLDDT was tested head to head against AF2-ensemble spread and lost: "Metrics like AF2 local-distance difference test (pLDDT) score were also found to be less reliable in our assessment on a panel of well-characterized fiducial markers" (p2); "This contrasts with other metrics, including pLDDT score in the region between fused domains, where we could identify examples of rigid constructs with poor pLDDT score (for example the frizzled receptor 5-BRIL fusion, Figure 1b) and flexible constructs with favorable pLDDT scores in linker regions (including Fab; where pLDDT score largely fails to predict the effect of adding disulfide crosslinks while the AF2-based ensemble captures the effect, Figure 1b)" (p4). The validation is visual/qualitative on ~5–8 systems; no AUC, correlation coefficient or threshold is reported.

**Still used as a model-ranking filter in the design loop:** "The predicted ensemble of structures was aligned and assessed for a low RMSD, particularly amongst the top scoring ~10/15 models" (p17) — "top scoring" is pLDDT rank. pLDDT is also the colour scale on the ensembles in Figs. 1b, 2 and 4a.

**Never used to judge conformational state** — no pTM/ipTM appears anywhere, and the co-folding predictions are not filtered or judged by confidence.

## D. Claims

### `central_conclusion`

Combining generative protein design (RFdiffusion/ProteinMPNN) with AF2-dropout ensemble prediction as a *rigidity* filter reliably yields GPCR fiducial markers at arbitrary fusion points, including the traditionally intractable extracellular TM1 site. This gave four inactive-state GPCR structures at ≤3.4 Å from prospective designs, and an extracellular-fiducial β2AR platform in which a high-efficacy agonist alone drives TM6 and ICL2 into nearly the G-protein-bound arrangement — with the residual difference on Gs binding attributed to ICL3 displacement and further TM6 helix folding rather than further outward TM6 movement. Co-folding models (OF3, Chai-1, Boltz-2), benchmarked against these new structures, reproduce receptor folds and some ligand poses but fail on ligand-induced conformational change.

### `necessity_claims`

**Verbatim, with pages. Greek degraded as in the text layer.**

1. **The co-folding gap claim, abstract form — THE key sentence for our corpus (p1):**
   > "Comparison with recent co-folding models highlights gaps in current methods for predicting ligand-induced GPCR conformational changes."

2. **The co-folding gap claim, discussion form (p10):**
   > "Obtaining snapshots of these systems remains incredibly valuable, as this present work has highlighted that traditionally difficult structural biology targets including GPCRs remain challenging for co-folding models, which struggle to accurately predict both ligand binding poses and ligand-induced conformational changes."

3. **The mechanism of that failure, as observed (p9):**
   > "Further, TM6 was predicted to either occupy an entirely inward conformation (Boltz-2, OpenFold 3) or outward (Chai-1) regardless of ligand identity (Extended Data Figure 7a), failing to capture the core activation responses observed here."

4. **Full activation stated as G-protein-dependent — attributed to prior spectroscopy, and the belief this paper's β2AR result pushes against (p1):**
   > "A variety of recent studies performing spectroscopic techniques suggested agonists of family A GPCRs induce a complex, multi-state conformational landscape with intermediates between the fully inactive state, with transmembrane helix 6 (TM6) swung in, and a fully activated state where TM6 is completely opened, the latter of which is proposed to largely occur only in the presence of G-protein (or mimetics)."

5. **Difficulty of visualising states without partners (p1, abstract):**
   > "G-protein coupled receptors (GPCRs) mediate precise ligand-specific signaling profiles, yet structural visualization of how ligands alter receptor conformational landscapes in the absence of signaling partners or mimetics has proven incredibly challenging."

6. **Impossibility with existing ICL fusions (p1–p2, sentence spans the page break):**
   > "Design of extracellular, rigid, pharmacologically inert fiducial markers would facilitate a structural understanding of these substates and how their populations shift in response to full, partial, and 'biased' agonists in a way that is not possible with ICL fusions."

7. **Necessity of a rigidity predictor (p2):**
   > "Generative machine learning methods for protein design have become incredibly powerful, providing a 'bespoke' solution for the production of arbitrary proteins, but a robust and computationally efficient method for predicting the degree of flexibility between target and fiducial is necessary for reliable fiducial design (Figure 1a)."

8. **Insufficiency of the standard AF2 design check (p2):**
   > "Testing whether the highest-scoring AlphaFold2 (AF2) predicted structure matches the design model has become a standard component of protein engineering pipelines, but is often insufficient for fiducial marker prediction without additional cryoEM screening."

9. **MD ruled out on cost (p2):**
   > "Molecular dynamics simulations have demonstrated good performance for rigidity filtering, but are far too resource intensive for design pipelines."

10. **Size limit on GPCR cryoEM (p1):**
    > "Several families of GPCRs, including the most extensive (family A), are too small to obtain high resolution reconstructions for the receptor alone with current technology (and indeed fall under the proposed 'theoretical size limit')."

11. **ICL3 fiducials bias the state (p1):**
    > "However, in the case of GPCRs, fiducial markers almost exclusively bind or fuse to intracellular loop 3 (ICL3), masking the native conformation, biasing the receptor towards the inactive state, and requiring experimental optimization."

12. **An impossibility claim about the tilted fiducial conformation (p8):**
    > "No structure prediction algorithm tested was able to produce this conformation (Extended Data Figure 5c), and MD simulations started from the tilted conformation in a lipid bilayer rapidly converted to the predicted conformation (Extended Data Figure 5d), further suggesting the detergent environment plays a role in stabilizing the alternative state."

### The active-like-without-G-protein observation — quoted exactly as stated

**The user's second key item. The paper does say this. Two statements, one abstract-level and one result-level, and they differ in strength; both are given so the weaker one is not lost.**

**Abstract (p1) — the framing claim:**
> "We then engineered an extracellular fiducial marker for the prototypical b2-adrenergic receptor that enabled direct structural characterization of the rearrangement of key intracellular motifs in the absence of G-protein."

**Results, p8 — the actual observation, TM6:**
> "Comparing the structures of b2BB3 bound to propranolol, BI-167107, and BI-167107 in complex with Gs reveals that the high efficacy agonist BI-167107 induces almost complete outward movement of TM6 even in the absence of G-protein, with the introduction of the Gs a5 helix shifting TM6 by less than 1 Å further outward at most positions (Figure 5a)."

**Results, p9 — the same observation for ICL2:**
> "Comparing the ICL2 region (one of the key motifs for binding G-protein) of the b2BB3-propranolol structure to b2BB3-BI-167107 with and without Gs reveals that BI-167107 alone is again sufficient to induce a substantial shift in the motif to nearly match the Gs-bound result (Figure 5e)."

**Discussion, p10 — the generalised form, with its own hedge:**
> "These b2AR structures suggest that, in contrast to some existing models of GPCR activation, the receptor in the presence of a sufficiently potent agonist undergoes almost complete rearrangement of the ordered domains to match the G-protein bound form."

**What is NOT claimed, and must not be overstated on our side.** The wording is "almost complete", "nearly match", "less than 1 Å further outward at most positions" — not identity with the Gs-bound state. The residual difference is explicitly attributed to something other than TM6 outward movement (p9): "Introduction of Gs (particularly the a5 helix) to b2AR bound to a highly efficacious agonist thus likely displaces ICL3 out from under the receptor and/or induces additional folding of TM6, rather than inducing an outward movement of TM6 (Figure 5a), with ICL3 likely acting as an allosteric modulator of transducer coupling." The state is also called by eye from overlays with no operationalised active-state predicate (see `state_metric`), the ligand is one of the most efficacious β2AR agonists known, and the authors' own caveat (p10) is that "these cryoEM structures may capture subsets of lower energy state(s) with a given ligand and higher energy structures may exist at room temperature". The construct is a fusion protein, not wild-type β2AR, though BRET and ELISA controls address that.

### The co-folding comparison — exactly what was compared, on what, and what was found

**Models compared (p2):** "This protocol was highly successful for predicting rigid ICL fusion constructs, with every design subjected to cryoEM analysis leading to a map of 3.4 Å resolution or better. These structures allow not only for a rationalization of antagonist binding, but also critical assessment of the predictive power of protein-ligand 'co-folding' models (OpenFold3 (OF3), Chai-1, Boltz-2), which generally had issues with identifying GPCR-ligand poses and interactions."
→ **Three models: OpenFold3, Chai-1, Boltz-2.** AlphaFold3 is cited in the same bracket (ref 25) but is never reported as run. No versions, no run protocol, no seed counts, no blinding statement anywhere in the paper.

**Compared on (two sets):**
- The four new inactive-state complexes — MRGPRX2-E23, MC2R-CRN04894, V1AR-SRX246, GIPR-GIP(5-31*) (p4–p6; supporting panels Extended Data Fig. 4b,c, **not in this PDF**).
- The three β2AR ligand complexes — propranolol, BI-167107, LM189 (p9; supporting panel Extended Data Fig. 7a, **not in this PDF**).

**What the comparison found, verbatim, per case:**

| system | finding (verbatim) | page |
|---|---|---|
| MRGPRX2-E23 | "While co-folding models generally place the ligand near the correct binding site with the correct orientation, the protein-ligand interactions are largely incorrect due to a failure to predict the change in fold at the top of TM7 (Figure 3c, Extended Data Figure 4b,c)." | p5 |
| MC2R-CRN04894 (best case) | "Co-folding approaches performed the best for CRN04894 binding to MC2R compared to the other small molecule cases examined, however a shift of the ligand in the pocket (perhaps due to TM2 being shifted in the TM bundle to more closely resemble previous melanocortin receptor structures, Figure 3f, Extended Data Figure 4b,c) results in a heavy-atom RMSD for the top ranked pose with Boltz-2 of ~3.2 Å and a loss of the K2.57 cation-p interaction." | p6 |
| V1AR-SRX246 (worst case) | "co-folding methods generally predict the structure of V1AR fairly accurately yet perform the worst of all the ligands at predicting the bound pose of SRX246, exhibiting total rearrangement of the compound in the pocket (Figure 3g, Extended Data Figure 4b,c)." | p6 |
| β2AR, ligand poses | "While co-folding approaches were able to reliably model the ligand bound pose for propranolol and BI-167107, some models struggled with the terminal phenyl ring of LM189 (Chai-1, OpenFold 3) (Extended Data Figure 7a)." | p9 |
| β2AR, **conformational state — the load-bearing result** | "Further, TM6 was predicted to either occupy an entirely inward conformation (Boltz-2, OpenFold 3) or outward (Chai-1) regardless of ligand identity (Extended Data Figure 7a), failing to capture the core activation responses observed here." | p9 |
| GIPR | No co-folding comparison is reported for GIPR. The peptide antagonist and ECD were poorly resolved (p6), and no prediction comparison is made. | p6 |

**Summary of what this supports and what it does not.** It supports: three current co-folding models, given a receptor and a ligand, return a TM6 conformation that is a property of the *model*, not of the *ligand* — the direction is model-specific and ligand-invariant across an antagonist, a full agonist and a biased agonist. It does not support any quantitative statement — no RMSD, no per-model table, no seed counts, no success rate — because the only quantitative co-folding number in the whole paper is the single ~3.2 Å Boltz-2 ligand RMSD for MC2R (p6), and every supporting panel lives in Extended Data not held in this PDF.

### `novelty_claims`

**Verbatim, with pages. Note: the paper makes no explicit "first" or "unprecedented" claim anywhere** — the novelty language is "previously intractable", "generalizable framework", "traditionally inaccessible".

1. (p1, abstract)
   > "Here we show that by combining generative protein design with deep-learning based conformational ensemble prediction we can reliably design 'fiducial markers' to facilitate cryogenic electron microscopy (cryoEM) of GPCRs at arbitrary fusion points, enabling the visualization of previously intractable states."

2. (p1, abstract)
   > "These results present a generalizable framework for accessing traditionally inaccessible structural states of small, dynamic proteins."

3. (p2, the gap claimed in the literature)
   > "However, less attention has been paid to whether a well-converged ensemble under such AlphaFold2-based approaches correlates well with molecular rigidity in cryoEM. It is also unclear how well these approaches, particularly those reliant on MSA alterations, perform when a part of the protein is engineered."

4. (p10)
   > "This strategy allowed high-throughput determination of inactive state structures of several pharmacologically important receptors and established a platform for imaging b2AR with any arbitrary ligand while leaving the intracellular vestibule of the receptor completely native."

5. (p10)
   > "All of the fiducial designs presented here should be transferable to other receptors, which can be easily tested computationally with our AF2 dropout approach."

### `stated_limits`

1. **The structures may be a cold-biased subset of the ensemble (p10):** "We note, however, that these cryoEM structures may capture subsets of lower energy state(s) with a given ligand and higher energy structures may exist at room temperature, especially given that cryoEM vitrification is not instantaneous."
2. **Extracellular grafting will not generalise cheaply (p10):** "Our extracellular fiducial marker can also likely be grafted to other receptors, although due to the substantial structural variety of GPCR extracellular pockets further designs will likely be needed in many cases."
3. **Generality is asserted beyond the evidence, and flagged as such by the authors (p10):** "although we applied this framework exclusively to GPCRs, the approach should facilitate cryoEM structure determination for a broad range of proteins."
4. **MD overestimates motion, with a temperature explanation (p3):** "There does appear to be a consistent slight overestimation in the degree of motion, however this may be attributable to the MD simulations being performed at 27-30°C while cryoEM experiments typically begin at 4-25°C prior to flash freezing."
5. **The parameter choice was not shown to be optimal (p4):** "AF2 with dropout enabled was chosen for prospective design as a balanced solution... although several of the tested parameters likely would have been equally effective."
6. **A documented failure of the method (p4):** "The only case examined where the AF2-based ensembles failed was the SMO-PGS2 fusion (Extended Data Figure 2f), which largely seems to result from a failure to predict the correct structure at all."
7. **The fiducial itself is not fully rigid (p7–p8):** "the BB3 fiducial occupies two different conformations, one which matches the design model while the other is tilted by ~40°, a geometry that may only be allowable due to the detergent micelle."
8. **The ICL2 bias signal is at the edge of resolution (p9):** "However, a subtle shift in ICL2 could be modelled (to within the resolutions obtained, Figure 5f, Extended Data 6d)."
9. **A confound in the ICL2 comparison (p9):** "although it is also influenced by a positive allosteric modulator that may further affect ICL2 conformation."
10. **The helical ICL2 may not be the only conformation (p9):** "although it is possible the loop may represent a higher energy alternative conformation."

### `stance`

**Dual, and provisional — the user's call.**

`precedent` **+** `contrast`.

- **`precedent` on findings.** This paper supplies the experimental observation that a high-efficacy agonist alone drives β2AR TM6 and ICL2 into nearly the Gs-bound arrangement without any G protein, mimetic or nanobody present (p8–p9). Any argument that an active-like state can be observed or generated without a transducer has a wet-lab precedent here, with an explicit no-G-protein control arm.
- **`contrast` on co-folding.** The paper is an external, experimentally grounded demonstration that OF3, Chai-1 and Boltz-2 return a ligand-invariant TM6 conformation (p9). That is a contrast point against co-folding-as-state-predictor, made from new structures rather than from re-analysis of deposited ones.
- **Not `threat`:** the paper predicts nothing our corpus predicts and makes no priority claim in the state-prediction space.
- **Caveat that cuts both ways:** its own state calls are visual, its co-folding comparison is n ≈ 7 and unquantified, and every supporting panel for the co-folding claim is in Extended Data absent from this PDF. It is strong as an observation and weak as a benchmark, and should be cited accordingly.

## E. Quantitative comparators

### `metrics_reported`

| metric | value | units | measured against | page |
|---|---|---|---|---|
| CryoEM map resolution, four prospective ICL3-fusion designs | ≤ 3.4 (every design) | Å | Gold-standard FSC (details in Extended Data Tables 1–2, not in PDF) | p2, p4 |
| CryoEM map resolution, β2BB3 receptor TM bundle | up to 3.1 | Å | as above | p7 |
| Boltz-2 top-ranked pose, CRN04894 in MC2R | ~3.2 | Å heavy-atom RMSD | This paper's cryoEM MC2R structure | p6 |
| TM6 outward shift added by introducing the Gs α5 helix | < 1 (at most positions) | Å | β2BB3-BI-167107 without Gs vs with Gs | p8 |
| TM4–TM6 distance, MD from extended-TM6 start | ~39 (peak) | Å (N4.40–L6.28 backbone N) | MD distribution, 5 replicates × 1 µs | p9 (Fig. 5b) |
| TM4–TM6 distance, MD from cryoEM-based start | ~38 (peak, with low-value shoulder) | Å | as above | p9 (Fig. 5b) |
| BB3 alternative fiducial conformation, tilt from design model | ~40 | degrees | β2BB3 design model | p7 |
| EC50 for epinephrine, β2BB3 and β2BB5 | within one log unit of WT β2AR | — | WT β2AR, TRUPATH BRET | p6 |
| Fiducial fusion size range designed | 13–25 | kDa | — | p4 |
| Fiducial motion amplitude, FZD5-BRIL (rigid exemplar) | ~2 (3DVA) / ~9 (MD) / ~5 (AF2 dropout) | Å, annotated on figure | 3DVA vs MD vs AF2 ensemble spread | p3 (Fig. 1b) |
| Fiducial motion amplitude, 6DS-Fab (disulfide-rigidified) | ~8 (3DVA) / ~11 (MD) / ~4 (AF2 dropout) | Å, annotated on figure | as above | p3 (Fig. 1b) |
| Fiducial motion amplitude, Fab (flexible parent) | ~21 (3DVA) / ~33 (MD) / ~20 (AF2 dropout) | Å, annotated on figure | as above | p3 (Fig. 1b) |
| Fiducial motion amplitude, megabodies Mb25 / Mb6 | too flexible for 3DVA; MD and AF2 annotations span ~50–120 Å | Å, annotated on figure | as above; **individual values not confidently legible at 150 dpi** | p3 (Fig. 1b) |
| MD production length, fiducial-marker systems | 500 ns × 3 replicates | ns | — | p17 |
| MD production length, β2AR/β2BB3 systems | 1 µs × 5 replicates | µs | — | p17 |

**Everything else quantitative is in material this PDF does not contain** — see `si_in_scope`.

### `n_predictions`

Recorded separately rather than as one total.

- **AF2 sampling sweep (benchmark):** "50 random number seeds were used for each sampling approach, which included default AF2, the use of dropout, and limiting the depth of the MSA sampling ranging from 16:32 to 256:512" (p17). Number of distinct sampling approaches is not enumerated precisely (≥3 named plus multiple MSA depths), so the total is not computable.
- **AF2 sampling in production design:** "three random number seeds" per design, giving 15 models per design (5 per seed, inferred from "the top scoring ~10/15 models") (p17). Runtime "approximately 5-10 minutes per design on a single GPU" (p17).
- **AlphaFold-Multistate, GIPR only:** 5 random seeds (p17).
- **Designs generated vs tested:** "3-5 constructs for each receptor" for four receptors (p4) and "five designs were selected" for β2AR (p6) — i.e. 17–25 constructs taken to FSEC; **the number of RFdiffusion designs generated before this filter is NOT REPORTED** ("Designs were typically generated in 2-5 rounds of 50-150 residues", p17, describes rounds, not counts). 5 constructs (one per receptor, plus β2BB3) went to full cryoEM.
- **Co-folding predictions: NOT REPORTED.** Number of models per system, per backbone, and the ranking basis for "the top" are never stated.
- **Structures determined:** 4 inactive-state complexes + 4 β2BB3 datasets (propranolol, BI-167107, LM189, BI-167107+Gs) = 8 reconstructions in the main text.
- **MD:** 3 replicates × 500 ns per fiducial system; 5 replicates × 1 µs per β2AR/β2BB3 condition (p17).

### `comparable_to_ours`

*(left empty — removed from extraction in v3)*

### `si_in_scope`

**SI NOT HELD, and it matters more here than usual.** The 21-page PDF contains the main text, main Figures 1–5, references and Methods only. Absent: **Extended Data Figures 1–7** (which carry the entire MSA-sweep analysis, all 3DVA junction controls, **and every panel supporting the co-folding comparison — ED Fig. 4b,c and ED Fig. 7a**), **Extended Data Tables 1–2** (cryoEM collection/refinement statistics — so no per-structure resolution, FSC, model-to-map or clash/Ramachandran number is available), **Supplementary Table 1**, **Supplementary Figures 1–4** (Euler angle distributions, FSC curves, local resolution, map-model agreement) and **Supplementary Videos 1–3**.
**Consequence:** `metrics_reported` looks nearly empty for a paper reporting eight cryoEM structures and a three-model co-folding benchmark. That is an artifact of the held material, not of the paper. The strongest claim in the paper for our purposes — ligand-invariant TM6 in all three co-folding models — is supported by a single Extended Data panel we do not have.

## F. Figures

One row per panel group. All five main figures are structure-render-dominated; the paper contains **exactly one quantitative plot panel** (Fig. 5b).

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 3 | The proposed pipeline: ML inpainting → ML ensemble prediction (accept/reject on convergence) → cryoEM reconstruction | schematic | `SCHEMATIC \| three-stage design→rigidity-filter→structure-determination workflow, drawn as cartoon receptor + fiducial with a reject/accept fork \| no data` | 1 (panel a) | — | CC-BY-NC-ND 4.0 (p1 footer, on every page) |
| 1B | 3 | Five published fiducial systems, each shown three ways: cryoEM 3DVA ensemble, MD ensemble, AF2-dropout ensemble; ordered rigid→flexible; inter-panel motion amplitudes annotated in Å | structure render (grid of small multiples) | `RENDER \| facet: fiducial system (5: FZD5-BRIL, 6DS-Fab, Fab, Mb25, Mb6) × readout (3: cryoEM 3DVA, MD, AF2 dropout) \| views: 1 \| overlay: 20 3DVA frames / 3 MD replicates at equal spacing / NOT REPORTED AF2 models, on 1 aligned reference each \| axis: none` | 15 cells in a 5×3 grid; columns vary by system, rows by readout method. Colour encodes frame index (3DVA), replicate (MD) or pLDDT (AF2) — three different meanings of colour in one figure. | **The whole rigidity argument rests on eyeballed spread.** Motion amplitudes are hand-annotated as "~2Å", "~21Å" etc. on the renders with no distribution, no error, no n per cell, and no stated measurement definition; the underlying quantitative version is deferred to Extended Data Fig. 2 (not in PDF). Megabody rows show a map instead of an ensemble, so the flexible end of the series is not on the same footing as the rigid end. Colour scale changes meaning between rows without a shared legend. | CC-BY-NC-ND 4.0 (p1) |
| 2 | 4 | The four prospective inactive-state structures: cryoEM map + model per receptor, fiducial coloured separately, AF2-dropout ensemble as an inner ring, ligand density insets | structure render (radial arrangement) | `RENDER \| facet: receptor (4: MRGPRX2, MC2R, V1AR, GIPR) × display (3: map, model, AF2 ensemble ring) \| views: 1 \| overlay: 15 AF2 models on 1 design model (inner ring); ligand-density insets overlay 1 model on 1 map \| axis: none` | Radial layout, no printed panel letters — the body text nevertheless cites "Figure 2a" (p4). 4 receptor groups × map/model/ensemble/ligand-inset. | No resolution, FSC or map-model statistic is printed on any panel; all deferred to Extended Data Tables 1–2 (not in PDF). Map contour levels not given, so the visual weight of each density is uncalibrated. | CC-BY-NC-ND 4.0 (p1) |
| 3A-I | 5 | Binding-pocket insets for all four antagonist complexes, each overlaid against a deposited reference and against the top Boltz-2 prediction; plus GIPR 3DVA maps | structure render | `RENDER \| facet: system (4: MRGPRX2, MC2R, V1AR, GIPR) × comparison (3: own structure inset, vs deposited reference, vs top Boltz-2 prediction) \| views: 1 \| overlay: 1 prediction on 1 reference per comparison (number of predictions generated NOT REPORTED) \| axis: none` | 9 lettered panels (a–i); a,d,g are own-structure insets, b,c,e,f,g are overlays against references or predictions, h is 3DVA maps, i is a GIPR overlay. Panel g carries two overlays. | **The figure titled "…Yet are Poorly Predicted by Co-Folding Models" contains no quantitative panel at all.** Only one co-folding model is shown (Boltz-2); Chai-1 and OF3 results, and any RMSD distribution across models or seeds, are deferred to Extended Data Fig. 4b,c (not in PDF). "The top" prediction is shown without stating how many were generated or how "top" was defined. | CC-BY-NC-ND 4.0 (p1) |
| 4A,C-E | 7 | β2BB3 vs β2BB5 AF2-dropout ensembles; cryoEM maps of β2BB3 with three ligands; β2BB3-BI-167107-Gs map with four resolved conformational classes | structure render | `RENDER \| facet: construct (2: β2BB3, β2BB5) for a; ligand condition (4: propranolol, BI-167107, LM189, BI-167107+Gs) for c–e × map treatment (2: unsharpened 3DVA, sharpened local refinement) \| views: 1 \| overlay: 15 AF2 models aligned on the β2 transmembrane domain (a); ligand density on 1 model (d); 4 3D-classification classes (e) \| axis: none` | a (2 ensembles), c (3 ligands × 2 map treatments), d (3 ligand densities), e (1 complex map + 4 class maps) | Panel a is the sole evidence that BB3 was "predicted rigid" and BB5 "predicted flexible", shown as pLDDT-coloured spaghetti with no spread metric and no threshold — the prospective filter's decision rule is never made numeric anywhere in the paper. | CC-BY-NC-ND 4.0 (p1) |
| 4B | 7 | 2D class averages for β2BB3 and β2BB5 from ~800 screening images on a 200 kV microscope — the prospective rigid/flexible test | grid of small multiples (2D class averages) | `RENDER \| facet: construct (2: β2BB3, β2BB5) \| views: NOT REPORTED (2D projection classes, count not stated) \| overlay: none — class averages, not overlaid models \| axis: none` | 1 lettered panel containing two galleries. Split from 4A,C-E because the image type is 2D particle class averages, not 3D structure renders — see `unresolved` on the v3 split rule for RENDER rows. | Number of classes shown vs computed is not given, nor particle counts per class, so "sufficiently rigid for alignment" vs "not" is a visual judgement on a curated selection of class averages. | CC-BY-NC-ND 4.0 (p1) |
| 5A,C-G | 8 | The activation comparison: TM6 and activation-residue overlays across propranolol / BI-167107 / BI-167107+Gs; 3DVA TM6-extension series for BI-167107 and LM189; ICL2 comparisons including against β2AR-LM189-Gi and β2AR-BI-167107-Gs | structure render | `RENDER \| facet: ligand condition (3: propranolol, BI-167107, BI-167107+Gs; +LM189 in c–g) × motif (2: TM6/activation residues, ICL2) \| views: 1 (a carries an inset zoom of the same view) \| overlay: 3–4 structures on 1 aligned reference per panel \| axis: none` | a (overlay + inset), c (3 3DVA frames for BI-167107), d (3 3DVA frames for LM189), e, f, g (ICL2 overlays) | **The paper's central conformational claim has no quantitative panel.** "Almost complete outward movement of TM6 even in the absence of G-protein" and "less than 1 Å further outward at most positions" (p8) are supported only by coloured overlays; no per-residue displacement plot, no RMSD, no error. The 3DVA series in c/d shows three selected frames out of the component with no indication of how many frames exist or how the three were chosen. | CC-BY-NC-ND 4.0 (p1) |
| 5B | 8 | MD distribution of TM4–TM6 distance for β2BB3-BI-167107 from two starting models (extended TM6 vs cryoEM-like), with dashed reference lines for fully open and fully closed extended TM6 | line (density/histogram trace) | `PLOT \| facet: none (1) \| vary: TM4-TM6 distance (N4.40–L6.28 backbone N), 26–44 Å (continuous) \| series: starting model (2: extended TM6, cryoEM-resolved TM6) \| measure: population (density, axis unlabelled and untick-marked) \| mark: line \| n: 5 replicates × 1 µs per series; frames per series NOT REPORTED` | 1 plot panel. **The same letter also carries structure renders** — an inset cartoon inside the axes plus two labelled models ("TM6 Extended", "TM6 CryoEM") to its right — which is why 5B appears here as a PLOT row while its renders are noted rather than given a third row. | **The measure axis is labelled only "Population" with no tick values and no units**, so the two distributions cannot be compared in magnitude, only in shape; no n per bin, no replicate spread, no error band, and no indication whether replicates were pooled. The dashed "fully open"/"fully closed" reference lines have no stated derivation. | CC-BY-NC-ND 4.0 (p1) |

**Panel-group rows: 8.** Pages rendered to resolve panel structure: **3** (pages 3, 4 and 8 — Fig. 1b's facet grid, Fig. 2's unlettered radial layout, and Fig. 5b's mark type and axis labelling were all unrecoverable from the captions). Figures 3 and 4 were filled from captions plus body text, which carry full panel letters.

**License, stated identically in the footer of every page, first on p1:**
> "It is made available under a CC-BY-NC-ND 4.0 International license."

**This carries both an NC and an ND clause. The ND clause forbids derivatives — no figure or panel here may be redrawn, re-plotted, adapted, cropped for adaptation, or restyled; only whole-figure reproduction with attribution, and even that only non-commercially.** In particular, Fig. 5b may not be re-plotted from its own values, and Fig. 1b's layout may not be adapted as a template.

## G. Provenance

| Field | Value |
|---|---|
| `extracted_on` | 2026-09-07 (as specified in BATCH_PROMPT.md; session date was 2026-09-08) |
| `extractor` | claude subagent (Claude Opus 5) |
| `schema_version` | v3 |
| `confidence` | **medium-high.** The text layer is clean and every main-text number was legible. Held below high for three reasons: (1) **the entire Extended Data and Supplementary set is absent from the PDF**, and that is where the co-folding comparison's evidence, all cryoEM statistics and the MSA-sweep analysis live — so several fields rest on one-sentence summaries in the body with no way to check them; (2) the co-folding models have **no Methods paragraph at all** — no versions, seeds, MSA/template settings, model counts or blinding statement — so `templates`, route 1 and `n_predictions` are NOT REPORTED for exactly the comparison our corpus cares about; (3) Fig. 1b's per-cell Å annotations for the two megabodies were not confidently legible at 150 dpi and are recorded as a range rather than as values. Greek letters are corrupted throughout the text layer (β→b, α→a, π→p), so quotes are reproduced with that corruption intact rather than silently edited. |
| `unresolved` | See list below. |
| `why_it_matters` | *(left empty — the user's call)* |

### `unresolved`

1. **Were the co-folding predictions made before the structures were solved?** Never stated. This determines whether the comparison is a blind prospective test or a retrospective illustration, and it is the single fact that would most change how strongly we can cite the "ligand-invariant TM6" result.
2. **How the co-folding models were run.** No versions, no seed counts, no MSA settings, no template settings, no number of models generated, no definition of "top ranked". A three-model claim with no protocol cannot be reproduced or extended.
3. **How many co-folding predictions per system, and how "the top" was chosen** (Fig. 3c,f,g; p6). If ranking is by model confidence this is fine; if by agreement with the reference it is route-6 leakage. Undeterminable.
4. **Whether templates were on for the AF2/ColabFold ensemble runs.** The Methods paragraph (p17) is otherwise detailed but silent on templates, which materially affects what "ensemble" means for an engineered fusion.
5. **The rigidity acceptance rule is never made numeric.** "assessed for a low RMSD, particularly amongst the top scoring ~10/15 models" (p17) — no cutoff value, so the prospective filter that the whole pipeline turns on cannot be applied by a reader.
6. **Number of RFdiffusion designs generated before the FSEC filter.** Only the number taken forward (3–5 per receptor, 5 for β2AR) is given, so the true design success rate is unknown and the reported "every design imaged yielded ≤3.4 Å" is conditioned on two upstream filters.
7. **Which Fig. 1b Å annotations belong to Mb25 vs Mb6** in the MD and AF2 rows (values ~50, ~90, ~117, ~120 Å appear); not confidently resolvable at 150 dpi.
8. **Whether AlphaFold-Multistate's inactive bias derives from GPCRdb state annotations.** Ref 57 (Heo & Feig) is the state-annotated-template method, but this paper never names the annotation source, so `oracle_leakage` route 2 is recorded on the paper's own words ("an inactive-GPCR bias", p17) rather than on an identified database.
9. **What "almost complete" means operationally.** The central β2AR claim (p8) has no threshold, no RMSD and no per-residue displacement. Citing it requires citing the hedge with it.
10. **Tags needed that the v3 vocabulary does not contain — none invented, all recorded here:**
    - **A Method tag for generative protein design / de novo binder or fusion design.** RFdiffusion + ProteinMPNN is the paper's primary method and the Method family (`cofolding`, `msa-subsample`, `msa-state-filter`, `template-state-bias`, `af-cluster`, `latent-steering`, `md`, `md-emulator`, `enhanced-sampling`, `benchmark-only`, `experimental`) has no entry for it. `experimental` covers the wet lab but says nothing about the design engine. Something like `generative-design` is missing.
    - **A Method or System tag for cryoEM structure determination as the primary modality.** `experimental` is defined as "a paper with no structure prediction in it at all", which is not true here — this paper runs AF2, AF-Multistate and three co-folding models. It is the least-wrong tag available and is used, but the definition does not fit, and a reverse lookup for "papers with wet-lab structures" will conflate this with pure-assay papers.
    - **A Control tag for a fiducial / fusion partner.** The Control family has `nanobody` and `g-protein-mimetic` but nothing for a designed rigid fusion or fiducial marker, which is this paper's entire subject. `nanobody` would be wrong (the β2AR fiducial is a de novo design, and the four ICL3 fusions are designed fusions, not binders raised against the target).
    - **A tag distinguishing "ran co-folding models as its own method" from "evaluated co-folding models as comparators".** `cofolding` is applied here because the paper does run OF3/Chai-1/Boltz-2 and a reverse lookup for co-folding evaluations must find it — but it will also return this paper to anyone querying for co-folding *methods*, which is a false positive.
    - **A Relation tag for "supplies experimental ground truth against which predictors can be scored".** `precedent` and `contrast` are both used and both partly fit, but neither captures that the reusable asset here is eight new reference structures.
    - Deliberately **not** used, to avoid false positives: `g-protein-mimetic` (wildtype Gs heterotrimer is used, not a mimetic or nanobody); `msa-state-filter` (MSA depth was reduced in the sweep, never state-substituted); `template-state-bias` — **borderline**, since AlphaFold-Multistate's inactive-GPCR bias for GIPR is exactly that; it is applied to one target only, and is tagged, with this note; `oracle-leak` (nothing contaminates the prospective design pipeline; the honest call is `design-level-oracle`); `no-anti-memorization` (the de facto post-cutoff set exists, it is simply never analysed as one — `anti-memorization` is also wrong, so **neither anti-memorization tag is applied**, and this paper will not surface in either reverse lookup); `saturating-metric`, `rmsd-only`, `binary-predicate`, `af-cluster`, `latent-steering`, `enhanced-sampling`, `benchmark-only`, `single-state`, `continuum`, `apo-sampling`, `seed-only`, `allosteric-site`, `cryptic-pocket`, `allosteric-failure`, `figure-exemplar`, `threat`, `background`, `negative-result`, `peer-reviewed`.
11. **Points where v3 itself was still ambiguous** (reported, not worked around):
    - **The panel-split rule is undefined for non-PLOT forms.** "Split when `mark` or `measure` differs" (SCHEMA.md §F) references two slots that exist only in PLOT. RENDER rows have neither, so a figure of eight render panels has no principled split criterion. I split Fig. 4B from 4A,C-E because 2D class averages and 3D map renders are different image types that should not join, and kept Fig. 3's nine render panels as one row — but that pair of decisions is judgement, not rule.
    - **RENDER has no slot for annotated quantities.** Fig. 1b carries fifteen numeric Å annotations printed on the renders. Those are real measurements, but `RENDER` has no `measure` slot and the figure is not a PLOT. I recorded them in `metrics_reported` and described them in `hides`; a `RENDER | annotation:` slot, paralleling `TREE | annotation:`, would fix this.
    - **A single panel holding a plot and renders.** Fig. 5b is a density plot with structure renders inside and beside the same lettered panel. v3 permits a letter to appear in two rows, but the guidance is written for "a letter genuinely contains two shapes" in the sense of two data shapes; here the second shape is decorative context, and creating a `5B` RENDER row would imply a render-design precedent that does not exist. I noted it in `panels` instead.
    - **`method_class` has no value for a wet-lab paper with a computational front end.** The listed options are all prediction-side. `other` is used, spelled out.
    - **`si_in_scope` is a yes/no-shaped field carrying a load-bearing warning.** Here the absent SI contains the only evidence for the paper's most citable claim. A structured form (`held` / `partial` / `SI NOT HELD` + *what is missing* + *which fields it empties*) would make that machine-visible; I wrote it as prose.

---

## Tags

`gpcr` `experimental` `cofolding` `md` `msa-subsample` `template-state-bias` `ensemble` `two-state` `visual-metric` `continuous-metric` `templates-on` `state-annotated-input` `prospective` `design-level-oracle` `unpowered` `confidence-as-discriminator` `multi-backbone` `experimental-validation` `ligand-driven` `partner-driven` `orthosteric` `preprint` `precedent` `contrast` `comparator-numbers`

*Notes on specific tags, so a reverse lookup is not misread:*
- `cofolding` — the paper **evaluates** OF3/Chai-1/Boltz-2; it does not use co-folding as its own method. See `unresolved` item 10.
- `template-state-bias` and `state-annotated-input` — apply to **GIPR only**, via AlphaFold-Multistate's inactive-GPCR bias (p17), not to the other four receptors.
- `templates-on` — applied on the strength of AlphaFold-Multistate (which is template-based) and the deposited-structure scaffolds used for design and model building; **templates for the plain AF2/ColabFold ensemble runs are NOT REPORTED** (p17).
- `msa-subsample` — subsampling was run in the **benchmark sweep only** (16:32 to 256:512, p17) and explicitly rejected for production, which used full-MSA AF2 with dropout.
- `two-state` — refers to the **experimentally determined** inactive and agonist-bound near-active β2AR states, not to anything a model generated.
- `unpowered` — the de facto post-cutoff co-folding test set is n ≈ 4–7 with overlapping receptor folds, and no anti-memorization control arm was run.
- `experimental-validation` — the computational rigidity predictions (β2BB3 rigid, β2BB5 flexible) were tested prospectively in cryoEM, and BB3/BB5 pharmacology was tested by BRET and ELISA.
- **Neither `anti-memorization` nor `no-anti-memorization` is applied** — a post-cutoff set exists in substance but is never framed or analysed as one, and both tags would mislead.
