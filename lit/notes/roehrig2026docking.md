# roehrig2026docking

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NOT APPLICABLE` with a reason where the field presupposes something this paper does not do.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–21), and coincide with the
printed page numbers (`n/21` footer).** Layout: p1 title + abstract + start of Introduction,
p2–3 Introduction, p3 Methods 2.1 Data Sets, p3–4 2.2 Structure Preparation, p4 2.3 Docking with
AC, p4 2.4 Docking with Vina and derivatives, p4–5 2.5 Analysis, p5–10 Results 3.1 (benchmark-set
analysis), p11–12 Results 3.2 (docking results), p13–15 Results 3.3 (docking vs co-folding),
p16–17 Summary and Conclusions, p17 Data and Software Availability, p18–21 references (58 entries).
Figures: Fig 1 p6, Fig 2 p7, Fig 3 p9, Fig 4 p11, Fig 5 p14. Tables: Tab 1 p12, Tab 2 p15.
**Supplementary Figs S1–S7 and Tabs S1–S3 are cited throughout but are NOT in this 21-page PDF.**

**RELATIONSHIP TO THE `skrinjar2026generalization` CORPUS ENTRY — read this before reusing any
number.** This paper is a *consumer* of the Runs N' Poses (RNP) benchmark, not a re-derivation of
it. Extracted independently from this PDF only; nothing below is imported from that note. What
this paper adopts, unmodified, from RNP (all from p3 and p5):
- the **set itself**: "2,600 protein-ligand systems with 3,047 'proper ligands' from the protein
  data bank (PDB) released between the training cutoff date for the co-folding methods (October 1,
  2021) and before January 9, 2025" (p3); "For 2,812 proper ligand-protein systems, the ligand and
  pocket similarity scores were provided" (p3);
- the **similarity annotation**, verbatim: "Similarity to the training set was defined as in
  RNP,10 using the product of binding pocket coverage30 for binding site similarity and the
  Combined Overlap Score (SuCOS)31 for ligand similarity." (p5). Component definitions restated on
  p3: pocket coverage = "the percentage of residues within 6 Å of the ligand in the query system
  which align with residues within 6 Å of the ligand in the target system (regardless of amino
  acid identity)"; ligand pose similarity = SuCOS; "Overall similarity was defined as the product
  of these two measures, divided by 100 to obtain a parameter in the interval 0–100" (p3);
- the **clustering**: "This set was divided into 921 clusters based on graph community clustering
  at ligand/pocket similarity > 50.10" (p3);
- the **"prevalent ligand" annotation**: "defined as ligands with more than 100 ligands in the
  training set having a >0.9 RDKit topological fingerprint Tanimoto similarity" (p8);
- the **AlphaFold 3 predictions and their scores**, not re-run here: "For AlphaFold 3, the values
  provided by the authors of the RNP set were used." (p5);
- the **plotting convention** of the stratified figure: Fig 5A caption, "plotted as in Ref.10" (p14).

What this paper **modifies or adds**:
- a **new derived set, RNP-F**, defined by five filters applied in order (p9–10) — EDIA_m of
  ligand ≥ 0.4; EDIA_m of ligand environment within 5 Å ≥ 0.4; maximally 100 analogous ligands in
  the training set; maximally one complex per PDB ID (keeping lowest similarity); maximally 5
  complexes per cluster (keeping lowest similarity) — yielding "the RNP-F set of 919 cases spread
  across 516 clusters" (p10);
- **new per-complex annotations not in RNP**: X-ray resolution, R-free, R-work, ligand B-factors,
  net ligand charge, recomputed RDKit rotatable dihedrals, ligand burial (CHARMM SASA), EDIA_m for
  ligand / 5 Å environment / 7.5 Å environment, OiiSTER "molecular beauty" values (p4–5);
- a **changed success criterion for the cross-method comparison**: "For comparing co-folding and
  docking results, success was defined as a combination of a ligand pose RMSD ≤ 2 Å and a
  LDDT-PLI > 0.8." (p5) — plus, for docking-only analysis, RMSD cutoffs of 1.0/1.5/2.0 Å (p5);
- the **docking arm itself**, which RNP did not have: "No comparison to physics-based docking
  methods was provided by the authors." (p16).
So the two entries are **not measuring the same thing**: RNP as adopted here is the same set with
the same similarity axis, but this paper (a) restricts the co-folding side to AlphaFold 3 alone,
(b) adds a second, quality/balance-filtered set, and (c) evaluates on a combined RMSD+LDDT-PLI
predicate rather than whatever RNP's headline predicate was. Any joint claim across the two notes
must be stated at the level of the shared similarity axis, not at the level of headline numbers.

---

## A. Identity

- **citekey**: `roehrig2026docking`
- **doi**: **10.64898/2025.12.09.693161** — bioRxiv, printed in the header of every page
  (p1–21). This matches `MANIFEST.csv` line 48 and `refs.bib`.
- **year**: **2026** for this version. **Version and posting date, recorded exactly as the paper
  states them:** the header on every page reads "this version posted **April 20, 2026**". The PDF
  **nowhere prints a version number** (no "v2" string appears anywhere in the text). The DOI stem
  encodes the original posting date `2025.12.09`, so this April 2026 file is a **revision of a
  9 December 2025 original** — consistent with the assignment's description of it as bioRxiv v2,
  but the "v2" label is external to the document and is recorded here as such, not as a quote.
  **Note a corpus inconsistency**: `refs.bib` gives `year = {2025}` for this key while the citekey
  and the posted version are 2026. Flagged under `unresolved`.
- **venue**: **bioRxiv preprint, not peer reviewed.** p1–21 header: "The copyright holder for this
  preprint (which was not certified by peer review) is the author/funder". No journal named
  anywhere; typeset in a Scientific Reports / `sn`-style single-column template. Tagged `preprint`.
- **title**: Comparative Assessment of the Utility of Co-Folding and Docking for Small-Molecule
  Drug Design — p1
- **authors**: Ute F. Röhrig (corresponding, ute.roehrig@sib.swiss), Marine Mathieu-Bugnon,
  Vincent Zoete (corresponding, vincent.zoete@unil.ch) — p1. Affiliations: SIB Swiss Institute of
  Bioinformatics, Molecular Modeling Group, Lausanne; Department of Fundamental Oncology,
  University of Lausanne / Ludwig Institute for Cancer Research Lausanne Branch, Epalinges.
  **This is the Attracting Cavities / SwissDock group evaluating its own docking program** against
  a third-party co-folding benchmark — ref 16, 17, 18, 24, 38 and 56 are all self-citations to AC,
  SwissParam, SwissDock and their own curated benchmark data. Record that: the docking arm is not
  a disinterested baseline, and the paper says so implicitly by describing AC as "our algorithm"
  (p2) and "our Attracting Cavities algorithm" (p16).

## B. Scope

- **system**: **general protein — small-molecule ligand–protein complexes, unrestricted by
  family.** The evaluation unit is a protein–ligand complex from the PDB, not a protein family.
  No family stratification is performed anywhere. The only compositional statements about what is
  in the set are chemical, not biological: "The RNP set contains a high proportion of co-factors,
  often featuring phosphate groups… i.e. 672 out of 2,812 ligands (24%) contain at least one
  phosphorus atom" (p8), and "26% of all RNP cases belong to the 10 most populated structural
  clusters alone, demonstrating an imbalance in the data set" (p8). Which 10 clusters, and what
  proteins they are, is **NOT REPORTED**. The 14 AC failures are attributed to "issues in the
  treatment of protein/nucleic acid complexes" (p4), the only hint that nucleic-acid-containing
  systems are present.
- **n_targets**: **This is a complex-count, not a target-count, paper — record all four numbers
  separately.**
  - 2,812 annotated proper ligand–protein systems downloaded, spanning **2,488 different PDB IDs**
    (p3). PDB IDs, not distinct proteins.
  - **921 RNP clusters** (graph community clustering at ligand/pocket similarity > 50), p3 — the
    closest thing to a target count for RNP.
  - **878 clusters** covered by the AC docking results (p4).
  - **516 clusters** in RNP-F (p10, p16).
  - Number of **distinct UniProt entries / distinct proteins is NOT REPORTED** anywhere.
  - Benchmark comparators: Astex Diverse 85 complexes; PDBbind core v2016 (CASF-2016) 57 target
    clusters × 5 = 285 complexes (p3).
- **method_class**: **benchmark-only + other (physics-based docking).** Dual, and the duality
  matters. The paper introduces no new predictor: the AC scoring function is explicitly unchanged
  ("The scoring function is identical to the one in the latest published version17 and the one
  used on the SwissDock webserver,38 so that the conclusions are independent of the employed AC
  version", p4), and the sampling improvements are deferred ("the latest version of AC with
  improved and accelerated sampling capabilities, which will be described in a forthcoming
  publication", p4). What is new is (i) a filtered benchmark set RNP-F, (ii) a physics-based
  docking arm on RNP, and (iii) the head-to-head against AlphaFold 3. **No co-folding model was
  run by these authors** — the AF3 numbers are taken from RNP (p5).
- **backbones**: **AlphaFold 3 only**, and only as a set of pre-computed predictions imported from
  RNP (p5). The choice is stated and justified on p3: "we compare the docking results to the
  AlphaFold 3 binding pose predictions provided with the RNP set.10 We limit comparison to
  AlphaFold 3 as all co-folding methods were shown to behave similarly and in order to keep as
  many cases as possible in the common subset solved with all methods." Chai-1, Protenix, Boltz-1,
  Boltz-2 and RoseTTAFold All-Atom are named on p2 as *available* in RNP but are **not analysed**.
  **Therefore NOT `multi-backbone`** — one co-folding backbone is actually measured, and the
  multi-backbone claim is inherited from RNP, not made here.
  The four **docking** engines actually run here (the real "backbones" of this paper) are listed
  under `controls_run` and in the docking-setup block below.
- **templates**: **NOT REPORTED.** This paper never states the template setting used for the
  AlphaFold 3 predictions it imports; the word "template" does not appear in the methods. For the
  docking arm the concept does not apply — but note the *structural* analogue, recorded under
  `oracle_leakage` route 1: the docking receptor is the target's own deposited structure, which is
  a stronger prior than any template.
- **msa_handling**: **NOT REPORTED.** No MSA, sequence-database or seed setting for the AF3 arm is
  stated anywhere in this paper; the predictions were taken as delivered by RNP (p5). Not
  applicable to the docking arm.

### Docking setup, recorded in full because the like-for-like question turns on it

**AC (Attracting Cavities), p4:** latest unpublished version, sampling improved, "The scoring
function is identical to the one in the latest published version17". CHARMM36 all-atom additive
force field, CHARMM v48b1. Standard AC scoring function = total force-field energy with FACTS
implicit solvation. Initial ligand rotation 90°, **4 random initial conditions**, **rigid
protein**, **cubic search box of edge length 25 Å centred on the centre of mass of the ligand in
the corresponding PDB model**. Two sampling budgets: **AC_norm** = max 3,072 initial ligand poses,
45 min CPU average; **AC_long** = max 12,288 initial ligand poses, 165 min CPU average (single
Intel Core i9 4.7 GHz). Results obtained for **2,597 of 2,611 cases (99.5%), 878 clusters**;
14 failures "mainly being due to issues in the treatment of protein/nucleic acid complexes".

**AutoDock Vina and derivatives, p4:** "For all dockings, the same search space definition as for
AC was used, namely a cubic search box with an edge length of 25 Å centered on the center of mass
of the ligand pose in the PDB model." AutoDock Vina **v1.2.3**; **Smina** fork (Oct 15, 2019
build) with the **Vinardo** scoring function; **GNINA v1.3.2** with a CNN scoring function.
Exhaustivity **1 / 8 / 100** tried for Vina; **default 8** for Smina/Vinardo and GNINA. 1 min
average at exhaustivity 8, 15 min at 100. Vina and Smina on a single Intel Core i9 4.7 GHz CPU,
GNINA on an Nvidia A100 GPU.

**Receptor preparation (p3–4), i.e. where the receptor structure came from:** mmCIF files
downloaded from the PDB for all 2,812 annotated systems. ChimeraX used to delete solvent, generate
all symmetry copies making crystal contacts ≤ 4.5 Å, keep only chains within 8 Å of the ligand,
delete cofactors > 8 Å from the ligand, delete crystallisation agents, **determine the centre of
mass of the ligand**, add hydrogens to the ligand, save the ligand in mol2, remove uncoordinated
ions, remove alternate-location atoms, complete missing sidechains, and **"delete the ligand of
interest before saving the target structure"**. Success for 2,806/2,812. Then CHARMM
topology/parameter generation via SwissParam + in-house CHARMMER succeeded for **2,611**; the
**195 failures (7%)** were "mainly due to missing ligand or cofactor parameters, for example for
boron-containing compounds or polymeric compounds, and to missing co-factor atoms in the PDB
model." Vina-family receptors built from the same prepared files via ChimeraX mmCIF→pdb and
MGLTools `prepare_receptor4.py`.

**So: the receptor is the *holo* deposited structure of the very complex being predicted, with the
ligand deleted, sidechains completed, and crystal contacts rebuilt. The site is the centre of mass
of the deposited ligand. This is re-docking, and the authors say so plainly (p2, p16).** The one
genuine de-novo element on the docking side is the ligand conformer: "we generated randomized
ligand conformations with RDKit35" (p4) — the deposited ligand *conformation* is not used as a
starting point, only its position (as box centre) and its identity.

**Asymmetry, acknowledged by the authors (p17):** "The big advantage of co-folding methods over
docking methods is that the first need only the protein sequence and chemical ligand structure as
input, while the latter necessitate a 3D target structure and, at least for practical purposes,
information on the localization of the binding site."

## C. Conformational core

- **states_generated**: **one.** The protein is held rigid throughout ("a rigid protein", p4), so
  **no protein conformational state is generated at all** — the single protein conformation is the
  deposited one, supplied as input. What *is* generated is an ensemble of **ligand** poses within
  that fixed protein conformation (max 3,072 / 12,288 initial poses for AC_norm / AC_long, p4),
  collapsed to a single top-ranked pose for the headline metric. Written as `one` rather than
  `ensemble + single-state` because the ensemble is over ligand placement, not over protein
  states, and calling it `ensemble` would false-positive every conformational-state query. The AF3
  arm's number of samples/seeds per target is **NOT REPORTED** in this paper.
- **structural_priors_used**: **Extensive, and by design — this is the field where the docking
  arm's inputs honestly belong, separately from the leakage assessment below.**
  1. **The deposited holo structure of every evaluated complex is the docking receptor** (p3–4,
     preparation pipeline above). Not a homolog, not a predicted model, not an apo structure — the
     target's own crystal structure.
  2. **The deposited ligand's centre of mass defines the search site** for all four docking
     engines (p4, twice).
  3. **Crystallographic environment is reconstructed**: symmetry copies making contacts ≤ 4.5 Å
     are generated, cofactors within 8 Å retained (p3). The set is thus evaluated in its
     crystallographic, not its biological, context.
  4. **Experimental electron density maps** are used to compute EDIA_m for the ligand and its 5 Å
     and 7.5 Å environments (p5), and then used to *filter* the benchmark (p9).
  5. **PDB metadata** — resolution, R-free, R-work, ligand B-factors — extracted and used for
     benchmark characterisation (p4).
  6. **The RNP similarity annotation**, which is itself computed against the co-folding models'
     training structures (p5).
  None of 1–6 is a methodological sin on its own; 1 and 2 are what makes the comparison
  non-like-for-like, and that is recorded as leakage below.
- **oracle_leakage**: **PRESENT AND SEVERE ON THE DOCKING SIDE, ROUTE 1 FIRST AND FOREMOST — and
  fully disclosed by the authors, who bound their own result as an upper limit.** Each route
  answered separately.

  **Route 1 — structures used as input or template: PRESENT, and it is the defining feature of the
  docking arm.** The receptor for each case is that case's own deposited structure with the ligand
  removed, and the binding site is the deposited ligand's centre of mass.
  - p2, verbatim: "We deliberately chose to perform re-docking and not cross-docking calculations
    and to locally dock to a predefined ligand binding site and not blindly on the full protein
    surface. The first choice was motivated by a better standardization and comparability of
    docking results, but the provided success rates should be considered an upper bound of what
    can be expected in a predictive cross-docking setting. The second choice makes sense in a drug
    design perspective, where a specific ligand binding site is usually targeted and may be
    predicted beforehand with dedicated pocket prediction algorithms."
  - p4, verbatim (AC): "a rigid protein, and a cubic search box with an edge length of 25 Å
    centered on the center of mass of the ligand in the corresponding PDB model."
  - p4, verbatim (Vina family): "For all dockings, the same search space definition as for AC was
    used, namely a cubic search box with an edge length of 25 Å centered on the center of mass of
    the ligand pose in the PDB model."
  - p3, verbatim (receptor construction): "…complete missing sidechains, and delete the ligand of
    interest before saving the target structure in mmCIF format."
  - p16, verbatim (the authors' own bound): "As we do local re-docking on predefined binding
    pockets, success rates should be considered an upper bound to what can be expected in
    cross-docking."
  **Consequence for the corpus: the comparison in Fig 5 is NOT like-for-like.** AlphaFold 3 is
  given sequence + ligand chemistry; AC/Vina are given the answer's receptor conformation and the
  answer's pocket location. The paper states the asymmetry (p17, quoted in section B) but does not
  correct for it, does not run a cross-docking or apo-receptor arm, and does not run a
  blind/whole-surface docking arm.
  *Partial mitigation, recorded for fairness:* the ligand conformer is randomised with RDKit
  before docking (p4), so ligand internal geometry is not leaked; and the receptor sidechains are
  rigid, so the docking cannot exploit induced fit beyond what the crystal already provides — it
  is also handed it for free.

  **Route 2 — state annotations from a curated database driving templates or alignments: NONE
  FOUND.** No GPCRdb, KLIFS or Kincore; no conformational-state annotation of any kind appears in
  the paper. The curated annotations that *are* used — PLINDER "proper ligand" labels (p3), RNP
  pocket coverage and SuCOS (p3, p5), RNP "prevalent ligand" labels (p8) — are similarity and
  ligand-type annotations, not state annotations, and they drive **stratification and filtering**,
  not model inputs. Protocol described p3–p5.

  **Route 3 — cluster labels derived from known states: NONE FOUND for states; PRESENT in a
  weaker, benchmark-construction form.** The RNP graph-community clusters (p3, "921 clusters based
  on graph community clustering at ligand/pocket similarity > 50") are used to build RNP-F:
  "Maximally 5 complexes belonging to the same cluster, keeping the ones with lowest similarity
  score" (p10). Those clusters are defined by similarity to the training data, so the composition
  of the evaluation set is shaped by knowledge of what the co-folding models saw. This is applied
  identically to both arms and is disclosed, but it is not neutral: the tie-break rule explicitly
  **retains the lowest-similarity members**, shifting RNP-F toward the regime in which the paper's
  headline claim lives. See also route 7.

  **Route 4 — hyperparameters / sweep ranges / seeds / stopping criteria tuned against the
  evaluation set: PRESENT, mild, and squarely the case the v3 schema calls out.** Settings were
  swept on the evaluation set itself and the results of the sweep are reported on that same set:
  - p4, verbatim: "We tried different exhaustivity values (1/8/100) for Vina and the default value
    of 8 for the other algorithms."
  - p4, verbatim: "We used two different sets of sampling parameters, denoted in the following as
    ACnorm and AClong, resulting in maximally 3,072/12,288 initial ligand poses…"
  No single value is selected per target, and all swept settings are reported side by side in
  Fig 4A/B rather than a best one being cherry-picked — which is the honest form of this. But the
  head-to-head figure (Fig 5) shows only one AC setting and one Vina setting, and **the paper never
  states which** (see `unresolved`); Fig 4's caption implies AC_norm and Vina exh 100 for its own
  panels C–F but says nothing about Fig 5. Selecting the displayed settings after seeing the sweep
  is route 4. **No leakage found in the opposite direction:** no per-target parameter, no seed
  selection, no stopping criterion tied to the reference.

  **Route 5 — success defined post hoc by RMSD/TM to a structure they held: PRESENT, and it is the
  primary metric.** p5, verbatim: "For comparing co-folding and docking results, success was
  defined as a combination of a ligand pose RMSD ≤ 2 Å and a LDDT-PLI > 0.8. For analyzing docking
  results alone, we used different ligand RMSD cutoff values (1.0, 1.5, 2.0 Å) as in our earlier
  works.17" And p5, verbatim: "For analysis of docking results, root mean square deviation (RMSD)
  values to the ligand pose in the PDB model were calculated with spyrmsd,44 taking molecular
  symmetry into account." The reference is the deposited pose in every case. Also, the entire
  scoring-failure analysis is defined against the held reference, p5, verbatim: "To determine
  scoring failures, we relaxed the PDB binding modes and calculated their score with each scoring
  function. If we obtained any docking pose with a lower score and a RMSD > 2 Å with respect to the
  ligand binding mode in the PDB model, a scoring failure was defined." This is unavoidable for a
  pose-prediction benchmark and is applied identically to both arms; recorded because the schema
  requires it, not as a differential defect.
  *Important nuance the paper itself raises:* it argues the reference is not trustworthy —
  "docking results yield insight into the validity of structural data in the PDB, which are
  error-prone models fitted to experimental data and which should not be considered as 'ground
  truth.'" (p16); "a poor ligand density fit does not allow to define docking successes and
  failures, as shown for example in Fig. 2B" (p7). So the paper is simultaneously using route 5
  and arguing route 5's reference is unreliable for 19% of RNP.

  **Route 6 — best/worst model labels assigned against a held reference: PRESENT for one reported
  metric, ABSENT for the headline metric.** The headline top-pose metric ranks by the scoring
  function alone, which is clean. But Fig 4A/B additionally reports **"All Poses 2.0 Å" —
  "success rates … at 2.0 Å for all poses independent of their rank"** (Fig 4 caption, p11), i.e.
  a case counts as a success if *any* generated pose is within 2 Å of the deposited pose. That is
  selection against the held reference, and it is what produces the ~80–87% (RNP) and ~85–88%
  (RNP-F) bars for AC. **These "all poses" numbers must never be compared against AF3's
  top-1 numbers.** The Fig 5 comparison against AF3 uses the top-pose criterion (Fig 5 caption,
  p14, and the success definition on p5), so the head-to-head itself is not contaminated by
  route 6.

  **Route 7 — design-level oracle use (weaker than pipeline leakage; labelled as such): PRESENT.**
  Three separable instances:
  1. The **expected direction of the result was known before the comparison was run**, from the
     source benchmark: "The authors showed that the performance of co-folding methods strongly
     depends on similarity to the training data and that they generalize poorly to novel
     complexes." (p2). The stated purpose of the work is to place a docking baseline against that
     known gradient (p2, p16).
  2. **The evaluation set was filtered using the co-folding models' training-set statistics**:
     "Maximally 100 analogous ligands in the training set" (p9) removes exactly the ligands RNP
     defines as memorisable ("prevalent" ligands with >100 near-duplicates in training, p8), and
     the two cluster/PDB-ID filters keep "the ones with lowest similarity score" (p10). Every one
     of these filters is defensible on quality/balance grounds, and the authors argue them on those
     grounds — but their net effect is to enrich the set in the regime where co-folding is already
     known to fail, and the paper reports that "For the cleaned RNP-F set, these trends are even
     more evident" (p13) without noting that the filter selects for that outcome.
  3. **The co-folding arm was reduced to one model on the basis of prior knowledge**: "We limit
     comparison to AlphaFold 3 as all co-folding methods were shown to behave similarly" (p3).
  Label: **design-level, not pipeline-level.** The AF3 predictions themselves are untouched
  imports; nothing leaky was fed to any model on the co-folding side.

- **prospective**: **no.** Entirely retrospective. Every case is a solved PDB complex; the docking
  is re-docking into that complex's own receptor at that complex's own site (p2, p4); the AF3
  predictions are pre-computed and imported (p5); success is scored against the deposited pose
  (p5). The set is *post-training-cutoff* for the co-folding models (p3), which makes the
  **co-folding arm temporally held out** — that is anti-memorization, not prospectivity — but the
  docking arm has no training cutoff to be held out from and is handed the answer's structure.
  The authors are explicit that the real prospective test has not been done: "their assessment on
  known ligand–protein complexes from the PDB has always been just a necessary first step in their
  development, but their true value is shown by their predictive capabilities in real-world
  utilization." (p16).
- **state_metric**: **binary predicate + continuous coordinate.** Dual, and both halves are used.
  - **Binary predicate**, thresholds stated: cross-method success = "ligand pose RMSD ≤ 2 Å **and**
    LDDT-PLI > 0.8" (p5); docking-only success at RMSD ≤ 1.0 / 1.5 / 2.0 Å (p5); scoring failure
    = any pose scoring better than the relaxed PDB pose at RMSD > 2 Å (p5). Threshold
    justification: the 2 Å/1.5 Å/1.0 Å cutoffs are justified only by precedent ("as in our earlier
    works17", p5). The LDDT-PLI > 0.8 threshold's *validity for a rigid receptor* is explicitly
    checked: "As the protein structure is rigid, the LDDT-PLI is assumed to be correct at low RMSD
    values. The validity of this assumption is demonstrated in Fig. S2, showing that almost all
    docking poses with a RMSD below 2 Å have a LDDT-PLI above 0.65." (p5) — **note the check is
    reported at 0.65, not at the 0.8 used as the criterion**; the supporting figure is not in this
    PDF. The 0.4 / 0.8 EDIA_m thresholds are justified from the EDIA source paper: "An EDIA_m
    score above 0.8 implies that the molecule is well covered with electron density, a value
    between 0.4 and 0.8 implies minor inconsistencies with the electron density fit, and a value
    below 0.4 implies substantial inconsistencies.40" (p7).
  - **Continuous coordinate**: top-pose RMSD distributions as violins in Fig 4C–F (p11), and the
    five continuous logistic-regression predictors (ligand SuCOS, pocket coverage, burial, rotatable
    dihedrals, EDIA_m), all min-max scaled to [0,1] (p5, Tab 2 p15).
  - **No visual-only state calls.** Fig 2 renders are used to illustrate data-quality pathologies,
    not to adjudicate success.
- **metric_saturation**: **Numeric saturation is present in one input variable and absent in the
  headline outcome metric.**
  - **Ligand burial is compressed against its ceiling.** Fig 1 panel I (p6) gives medians of
    0.94 / 0.90 / 0.92 / 0.93 for Astex / PDBbind / RNP-F / RNP on a 0–1 scale with the plotted
    range roughly 0.5–1.0 — i.e. the majority of every set sits in the top 10% of the scale. The
    authors flag the effect themselves, p5: "For ligand burial we tested both the solvent
    accessible surface algorithms implemented in ChimeraX32,33 and in CHARMM21 and found the latter
    to yield more meaningful results when the two algorithms diverged (see Fig. S1), although its
    **absolute values are higher than intuitively expected**." This matters because burial is the
    largest coefficient in the AC and Vina regression models (3.457 and 3.656, Tab 2 p15) — a
    ceiling-compressed predictor carrying the strongest coefficient.
  - **The success-rate outcome does not saturate**: the highest bin reaches ~87% for AF3 on RNP
    and ~79% on RNP-F (Fig 5A/B, p14), and Table 1 scoring-failure rates span 6.2–51.6% (p12).
  - **Pocket coverage is not a saturating *metric* but a saturating *distribution*** in this set:
    "More than 80% of the complexes have a binding site similarity above 80%" (p9), and Fig 3's
    first panel shows 48.0% of RNP in the top pocket-coverage column alone. That is set imbalance,
    recorded here because it directly limits the resolution of the pocket-similarity axis; the
    figure-level consequence is in the Fig 3 and Fig 5C-D `hides` entries.
- **directional_control**: **NOT APPLICABLE for protein conformational state** — the receptor is
  rigid and supplied (p4), so no state can be instructed or sampled. **The one directional handle
  that exists is over ligand placement**: the 25 Å cubic search box centred on the deposited
  ligand's centre of mass (p4), which is the "predefined ligand binding site" of p2. The authors
  note this handle is user-suppliable in practice — "a specific ligand binding site is usually
  targeted and may be predicted beforehand with dedicated pocket prediction algorithms" (p2) — but
  no pocket-prediction arm is run here. Secondary handles that are *not* directional in the state
  sense: sampling budget (AC_norm/AC_long, Vina exhaustivity 1/8/100, p4) and choice of scoring
  function (4 of them, p4).
- **anti_memorization_design**: **YES — inherited wholesale from RNP, and it is the axis of the
  whole paper.**
  - **Temporal held-out set**: 2,600 systems / 3,047 proper ligands "released between the training
    cutoff date for the co-folding methods (October 1, 2021) and before January 9, 2025" (p3). The
    cutoff is **the co-folding models' stated training cutoff, adopted from RNP, not independently
    verified here.**
  - **Similarity annotation**: overall similarity = pocket coverage × SuCOS / 100, on 0–100 (p3,
    p5), available for 2,812 systems.
  - **Prevalence annotation**: >100 training ligands at >0.9 RDKit topological fingerprint Tanimoto
    (p8).
  - **Sets actually analysed**: RNP-F = 919 cases / 516 clusters after the five filters (p9–10);
    docking common subsets 2,580 (RNP) and 891 (RNP-F) across all six docking runs (Fig 4A/B
    titles, p11); **AF3-vs-docking common subsets 2,448 (RNP) and 854 (RNP-F)** (Fig 5 caption,
    p14, and Tab 2 caption, p15).
  - **Applies to the co-folding arm only.** AC and Vina have no training set to be held out from;
    Vinardo is a fitted empirical function and GNINA carries a CNN trained on structural data, and
    **the paper never asks whether Vinardo's or GNINA's training data overlaps RNP.** Recorded
    under `unresolved`.
- **anti_memorization_control**: **RUN AND ANALYSED — this is the paper's central experiment, not
  a held-out set left sitting.** Three independent analyses of the stratified arm:
  1. **1-D stratification by overall similarity**, 8 bins, Fig 5A (RNP, 2,448 cases) and Fig 5B
     (RNP-F, 854 cases), p14, with **bootstrap 95% confidence intervals from 1,000 resamples per
     bin per method** (Fig 5 caption, p14) and **n printed on every tick label**.
  2. **2-D stratification** decomposing similarity into its two factors, Fig 5C (pocket coverage ×
     ligand SuCOS, 7×7 bins) and Fig 5D (ligand burial × rotatable dihedrals), p14, one heatmap per
     method plus a cases-per-bin reference heatmap.
  3. **Descriptive logistic regression** on 2,448 common RNP cases with five [0,1]-scaled
     predictors, one model per method, Tab 2 p15, with SEs, accuracy and AUC.
  **Powering**: not `UNPOWERED` by the schema's n < ~10 rule — the smallest stratum is n = 36
  (RNP-F, similarity 0–20). But **the strata carrying the headline claim are the smallest ones**:
  RNP 0–20 n = 63 and 20–30 n = 110 against 80–100 n = 738; RNP-F 0–20 n = 36 and 20–30 n = 58
  against 40–50 n = 156. The bootstrap CIs in the lowest RNP-F bins are visibly ±15–20 percentage
  points and the AC/Vina/AF3 ribbons overlap there — so the *lowest* bin does not on its own carry
  the claim; the claim rests on the monotone trend across bins, which is what the regression
  formalises. Record it that way, not as a per-bin significance claim, which the paper never makes.
  **Not controlled for**: no arm exists in which the docking side is deprived of the deposited
  receptor or site, so "docking wins at low similarity" is measured under an input asymmetry that
  is itself never varied.
- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| Four independent scoring functions run on the same set (AC/CHARMM+FACTS, Vina, Smina+Vinardo, GNINA CNN) | That the docking result is an artefact of one scoring function or of the authors' own program | p4, Fig 4A/B p11, Tab 1 p12 |
| Two AC sampling budgets, AC_norm (3,072 initial poses) vs AC_long (12,288) | That AC's failures are undersampling rather than scoring; also that the AC result depends on compute budget | p4, Fig 4A/B p11 |
| Vina exhaustivity sweep 1 / 8 / 100 | Same, for the Vina family; that the Vina baseline was handicapped by a low default | p4, Fig 4A/B p11 |
| "All poses at 2.0 Å" reported alongside "top pose at 2.0 Å" | Separates *sampling* failure (correct pose never generated) from *ranking* failure (generated but not scored best) | Fig 4A/B + caption p11 |
| Scoring-failure test: relax the deposited pose, score it, and declare a scoring failure if any docked pose scores better at RMSD > 2 Å | That docking failures are sampling failures; isolates the scoring function as the cause | p5 (definition), Tab 1 p12 |
| Intersection of scoring failures (∩ScFail) and of scoring successes (∩ScSucc) across all four scoring functions | That a scoring failure is function-specific rather than a property of the complex (or of the PDB model) | Tab 1 p12 |
| Same protocol run on Astex Diverse (85) and PDBbind core v2016 (285) | That the low RNP success rates reflect method weakness rather than benchmark difficulty/quality | p3, Fig 1 p6, Tab 1 p12 |
| RNP-F (919/516) analysed alongside unfiltered RNP (2,812) | That the result is driven by ill-defined electron density, prevalent ligands, or cluster imbalance | p9–10, Fig 4B p11, Fig 5B p14, Tab 1 p12 |
| Two solvent-accessible-surface algorithms compared (ChimeraX vs CHARMM) for ligand burial | That the burial variable is an artefact of one SASA implementation | p4–5, Fig S1 (**SI not held**) |
| LDDT-PLI validity check for a rigid receptor (almost all poses with RMSD < 2 Å have LDDT-PLI > 0.65) | That the combined RMSD+LDDT-PLI criterion is unfairly strict on rigid-receptor docking | p5, Fig S2 (**SI not held**) |
| Bootstrap 95% CIs, 1,000 resamples per bin per method | That per-bin differences between AF3 and docking are sampling noise | Fig 5 caption p14 |
| Multivariate logistic regression with two similarity + three physical predictors, per method | That the similarity effect for AF3 is confounded with density fit, burial or flexibility (and vice versa for docking) | p5, Tab 2 p15, Tabs S1–S3 (**SI not held**) |
| Property profiling of consistent scoring failures vs consistent scoring successes | That scoring failures are random rather than concentrated in small, exposed, charged, ill-defined ligands | p12, Fig S5 (**SI not held**) |
| Randomised RDKit starting ligand conformers rather than the deposited conformer | That docking success comes from starting at the answer's internal geometry | p4 |
| **NOT RUN — cross-docking arm** | Would have ruled out receptor-conformation leakage; explicitly declined ("We deliberately chose to perform re-docking and not cross-docking") | p2, p16 |
| **NOT RUN — blind / whole-surface docking arm** | Would have ruled out site leakage; explicitly declined | p2 |
| **NOT RUN — any arm giving docking an apo, predicted or homolog receptor** | Would have made the AF3 comparison like-for-like | absent; protocol p3–4 |
| **NOT RUN — co-folding models other than AF3** | Would have ruled out AF3-specific behaviour; declined on the basis of RNP's prior finding | p3 |

- **confidence_as_discriminator**: **No pLDDT/pTM/ipTM analysis of any kind — the AF3 confidence
  scores are neither used nor discussed**, despite the predictions being imported wholesale from
  RNP (p5). The word pLDDT does not appear in the paper. **The analogous question is asked of the
  docking side and answered rigorously**, which is worth recording as the transferable idea: the
  *scoring function* is the docking analogue of a confidence head, and the paper validates it
  directly by testing whether it ranks the deposited pose best. p5, verbatim: "Scoring failures
  occur when a scoring function does not attribute the best score to the ligand binding pose
  defined in the PDB model. They are more likely to be detected with extensive sampling and can be
  divided into three classes according to their underlying cause: an issue in (1) the scoring
  function, (2) the structure preparation, or (3) the structural model in the PDB." Result: 24.2%
  (GNINA) to 51.6% (Vina) of RNP cases are scoring failures (Tab 1, p12), and p16: "One fourth to
  one half of docking failures are not due to insufficient sampling but to the scoring functions
  ranking an alternative ligand binding pose better than the one described in the PDB model." So:
  **the discriminator is used and is explicitly validated, and it fails a quarter to a half of the
  time.**

## D. Claims

- **central_conclusion**: On a training-similarity-stratified benchmark of post-cutoff PDB
  complexes, AlphaFold 3 beats physics-based docking only for complexes similar to its training
  data, while Attracting Cavities and (less clearly) AutoDock Vina beat it in the low-similarity
  regime; AF3's success rate is governed by pocket and ligand-pose similarity to training whereas
  docking success is governed by physical ligand properties (burial, flexibility) and by
  crystallographic data quality. The authors additionally argue RNP is unsuitable as-is for
  benchmarking pose prediction — 19% of ligands are poorly supported by electron density, 24% are
  phosphorus-containing cofactors, 26% of cases sit in 10 clusters — and supply a filtered
  919-case subset, RNP-F, on which the same conclusions are sharper. The docking arm is re-docking
  into each target's own deposited receptor at the deposited site, which the authors state is an
  upper bound.
- **necessity_claims** (verbatim, with page):
  - p17: "The big advantage of co-folding methods over docking methods is that the first need only
    the protein sequence and chemical ligand structure as input, while the latter **necessitate a
    3D target structure and, at least for practical purposes, information on the localization of
    the binding site**."
  - p16: "In summary, ligand binding pose prediction for small-molecule drug design, which is
    concerned with novel ligands and novel binding pockets, **is a problem not yet solved by
    co-folding methods** and better tackled with physics-based methods."
  - p2: "Predicted interactions **are essential** for supporting drug design projects, because they
    allow for rational chemical modifications to improve ligand properties such as affinity or
    specificity."
  - p7: "This is problematic, as **a poor ligand density fit does not allow to define docking
    successes and failures**, as shown for example in Fig. 2B."
  - p12: "Here, the protein binding site displays a strongly negative electrostatic potential,
    further enhanced by the cofactor carrying a net charge of -4, **making it impossible for the
    negatively charged ligand to bind to this site in the absence of additional cations**."
  - p16: "We give examples showing how docking results yield insight into the validity of
    structural data in the PDB, which are error-prone models fitted to experimental data and
    **which should not be considered as 'ground truth.'**"
  - p2, on the RNP prerequisite: "**as co-folding methods claim to be better at predicting
    ligand–protein structures, a comparison is warranted**."
  - p16, restating the same as an obligation: "However, **a comparison is warranted** because both
    are used for ligand binding pose prediction in structure-based drug design, and a user should
    be able to make an informed choice of method."
- **novelty_claims**: **No explicit first/novel/unprecedented claim is made about this work
  anywhere in the paper — NOT REPORTED as such.** The nearest thing is a gap statement about the
  source benchmark, recorded verbatim because it is what the paper's contribution is defined
  against:
  - p16: "To this end, we used the recently published and highly annotated Runs N' Poses set of
    ligand–protein complexes, with which it was shown that current co-folding methods work well for
    predicting complexes similar to the training data but fail to generalize to novel data.10
    **No comparison to physics-based docking methods was provided by the authors.**"
  - p2, the framing that positions the work: "**Co-folding and docking are fundamentally different
    techniques and therefore difficult to compare.** However, as co-folding methods claim to be
    better at predicting ligand–protein structures, a comparison is warranted."
  - Also recorded because the paper's rhetorical target is a novelty claim by *others*, quoted
    here verbatim from p1–2: "AlphaFold 3 has been advertised as providing 'far greater accuracy
    for protein–ligand interactions compared with stat-of-the-art docking tools.'1" [sic,
    "stat-of-the-art" is the paper's own typo].
- **stated_limits** (all authors' own):
  - **Re-docking is an upper bound**, stated twice — p2: "the provided success rates should be
    considered an upper bound of what can be expected in a predictive cross-docking setting";
    p16: "As we do local re-docking on predefined binding pockets, success rates should be
    considered an upper bound to what can be expected in cross-docking."
  - **Local docking to a predefined site is a choice, not a neutral setting** — p2: "to locally
    dock to a predefined ligand binding site and not blindly on the full protein surface… The
    second choice makes sense in a drug design perspective".
  - **The reference structures are unreliable for a substantial fraction of the set** — p7: "19%
    of cases in the RNP have a ligand with an EDIA_m value below 0.4, compared to 2% in the Astex
    set and 8% in the PDBbind set"; p16: PDB models "should not be considered as 'ground truth.'"
  - **RNP is unbalanced and unrepresentative for drug design** — p16: "it contains (1) many ligands
    and binding pockets ill-defined by the electron density, (2) a very high percentage of
    non-druglike ligands, and (3) many complexes belonging to just a few clusters of similar
    structures."
  - **RNP-F is still harder than the classical sets** — p10: "RNP-F removes a number of problematic
    cases but remains more challenging than both Astex and PDBbind sets in terms of ligand
    flexibility and solvent exposure."
  - **Set properties predict lower docking scores independently of method quality** — p7: "These
    observations are unproblematic but likely to lead to lower success rates for physics-based
    docking tools on the RNP set than on the Astex and PDBbind sets."
  - **Confounding among stratification variables is acknowledged** — p9: "The analysis shows a
    strong data heterogeneity and hidden correlations in the dataset, complicating one-dimensional
    analyses"; p15: "The large coefficient of the AlphaFold 3 model for the ligand density fit is
    due to the positive correlation of this variable to complex similarity."
  - **A specific dip in the stratified curve is explained rather than claimed** — p13: "The small
    decrease of AC and Vina success rates for the second similarity bin (20-30) in Fig. 5A is due
    to the fact that complexes in this bin have ligands that are on average ill-defined by the
    electron density (low ligand EDIA_m value) and very solvent exposed".
  - **Comparison restricted to one co-folding model** — p3: "We limit comparison to AlphaFold 3…"
  - **Docking's static approximation** — p2: "The main shortcoming of docking is the static
    approach to the dynamic ligand-binding process, leading to a reasonable accuracy in predicting
    binding poses but difficulties in predicting binding affinities and in separating binders from
    non-binders."
  - **The AC version used is unpublished** — p4: "the latest version of AC with improved and
    accelerated sampling capabilities, which will be described in a forthcoming publication."
  - **7% of systems could not be prepared** — p3: "The 195 failures (7%) were mainly due to missing
    ligand or cofactor parameters…"
  - **Benchmarking is not the real test** — p16: "their assessment on known ligand–protein
    complexes from the PDB has always been just a necessary first step in their development, but
    their true value is shown by their predictive capabilities in real-world utilization."
- **stance**: **PROVISIONAL — the user's call, presented as two stances, not settled.**
  `contrast` + `precedent`.
  - **`contrast`** on the utility of co-folding: this is the strongest available statement in the
    corpus that co-folding's advantage over classical methods evaporates outside the
    training-similarity envelope, and it is stated as a conclusion about drug design practice, not
    only about benchmarks (p16). It also contrasts on *rigour of comparison*: it shows what a
    physics baseline does to a memorization argument.
  - **`precedent`** on method: similarity-stratified evaluation with per-bin n, bootstrap CIs, a
    2-D decomposition of the similarity axis, and a multivariate regression separating similarity
    effects from physical confounders is a template worth reusing. Also precedent for
    *quality-filtering a leakage benchmark* and reporting both filtered and unfiltered.
  - **Counterweight the user must weigh**: the docking arm is re-docking with the target's own
    receptor and site (`oracle_leakage` route 1), and the authors are the authors of one of the
    two docking programs. Neither invalidates the trend, both bound how the numbers can be cited.

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Top-pose success rate, RMSD ≤ 2.0 Å, AC (AC_norm / AC_long) | 54–59 | % | deposited ligand pose; RNP common cases (2,580) | p11, Fig 4A |
| Top-pose success rate, RMSD ≤ 2.0 Å, Vina + Smina/Vinardo + GNINA | 33–43 | % | deposited ligand pose; RNP common cases (2,580) | p11, Fig 4A |
| Top-pose success rate, RMSD ≤ 2.0 Å, AC (AC_norm / AC_long) | 63–68 | % | deposited ligand pose; RNP-F common cases (891) | p11, Fig 4B |
| Top-pose success rate, RMSD ≤ 2.0 Å, Vina + derivatives | 40–48 | % | deposited ligand pose; RNP-F common cases (891) | p11, Fig 4B |
| Top-pose success rate, RMSD ≤ 1.0 Å and ≤ 1.5 Å, all six docking runs | ~16–37 (1.0 Å) and ~25–52 (1.5 Å) on RNP; ~21–46 (1.0 Å) and ~31–61 (1.5 Å) on RNP-F | % | deposited ligand pose | Fig 4A/B p11 — **bar heights only, not tabulated** |
| Any-pose (rank-independent) success rate at 2.0 Å, all six docking runs | ~58–84 (RNP); ~63–88 (RNP-F) | % | deposited ligand pose — **route-6 selection; not comparable to AF3 top-1** | Fig 4A/B p11 — bar heights only |
| **Stratified success rate vs training similarity — the paper's central result** | see the two dedicated tables below | % | RMSD ≤ 2 Å **and** LDDT-PLI > 0.8, vs deposited pose | Fig 5A/B p14 |
| Scoring-failure rate, AC | 10.6 / 24.2 / 33.4 / 26.0 | % | Astex / PDBbind / RNP / RNP-F | Tab 1 p12 |
| Scoring-failure rate, Vina | 30.6 / 40.4 / 51.6 / 42.0 | % | Astex / PDBbind / RNP / RNP-F | Tab 1 p12 |
| Scoring-failure rate, Vinardo | ND / ND / 33.1 / 29.2 | % | Astex / PDBbind / RNP / RNP-F | Tab 1 p12 |
| Scoring-failure rate, GNINA | ND / ND / 24.2 / 26.3 | % | Astex / PDBbind / RNP / RNP-F | Tab 1 p12 |
| Intersection of scoring failures across all 4 functions (∩ScFail) | 7.2 (RNP) / 6.2 (RNP-F) | % | all four scoring functions simultaneously | Tab 1 p12 |
| Intersection of scoring successes across all 4 functions (∩ScSucc) | 30.7 (RNP) / 38.4 (RNP-F) | % | all four scoring functions simultaneously | Tab 1 p12 |
| Logistic regression coefficient, **ligand pose similarity (SuCOS)** | AF3 **4.106** (SE 0.29) / AC 0.327 (0.25) / Vina 0.056 (0.28) | logit, predictors scaled to [0,1] | binary success on 2,448 common RNP cases | Tab 2 p15 |
| Logistic regression coefficient, **binding pocket similarity** | AF3 **2.210** (0.35) / AC −0.004 (0.30) / Vina **−0.859** (0.32) | logit, scaled | same | Tab 2 p15 |
| Logistic regression coefficient, **ligand burial** | AF3 0.548 (0.29) / AC **3.457** (0.29) / Vina **3.656** (0.35) | logit, scaled | same | Tab 2 p15 |
| Logistic regression coefficient, **ligand flexibility (rotatable dihedrals)** | AF3 0.753 (0.28) / AC **−1.435** (0.23) / Vina **−1.045** (0.25) | logit, scaled | same | Tab 2 p15 |
| Logistic regression coefficient, **ligand density fit (EDIA_m)** | AF3 **2.032** (0.21) / AC **1.444** (0.20) / Vina **1.053** (0.22) | logit, scaled | same | Tab 2 p15 |
| Logistic regression constant | AF3 −5.947 (0.42) / AC −3.446 (0.35) / Vina −3.541 (0.39) | logit | same | Tab 2 p15 |
| Logistic model accuracy | AF3 0.744 / AC 0.637 / Vina 0.668 | fraction | 2,448 common RNP cases | Tab 2 p15 |
| Logistic model AUC | AF3 0.79 / AC 0.70 / Vina 0.67 | AUC | 2,448 common RNP cases | Tab 2 p15 |
| Fraction of ligands with EDIA_m < 0.4 | 2 / 8 / 19 | % | Astex / PDBbind / RNP | p7 |
| Fraction of ligands containing ≥1 phosphorus atom | 2 (2 ligands) / 4 (12 ligands) / 24 (672 of 2,812) / 9 | % | Astex / PDBbind / RNP / RNP-F | p8, p10, p16 |
| Concentration of the set in its largest clusters | 26 | % of RNP cases in the 10 most populated clusters | RNP | p8 |
| Fraction of complexes with binding site similarity > 80% | >80 | % | RNP | p9 |
| Median X-ray resolution | 2.00 / 1.90 / 1.95 / 1.95 | Å | Astex (n=85) / PDBbind (n=285) / RNP-F (n=919) / RNP (n=2812) | Fig 1A p6 |
| Median R-free | 0.24 / 0.23 / 0.23 / 0.22 | — | Astex (83) / PDBbind (279) / RNP-F (919) / RNP (2812) | Fig 1B p6 |
| Median number of heavy atoms | 23.00 / 23.00 / 27.00 / 26.00 | atoms | Astex (85) / PDBbind (285) / RNP-F (919) / RNP (2679) | Fig 1C p6 |
| Median number of rotatable dihedrals | 5.00 / 4.00 / 7.00 / 6.00 | count | Astex (85) / PDBbind (285) / RNP-F (919) / RNP (2679) | Fig 1D p6 |
| Median ligand burial | 0.94 / 0.90 / 0.92 / 0.93 | fraction 0–1 | Astex (85) / PDBbind (285) / RNP-F (919) / RNP (2610) | Fig 1I p6 |
| Median mean ligand B-factor | 25.21 / 24.70 / 36.01 / 34.35 | Å² | Astex (85) / PDBbind (282) / RNP-F (919) / RNP (2611) | Fig 1H p6 |
| Median ligand EDIA_m | 0.82 / 0.79 / 0.69 / 0.72 | EDIA_m | Astex (85) / PDBbind (277) / RNP-F (919) / RNP (2603) | Fig 1E p6 |
| Median EDIA_m of ligand environment (5.0 Å) | 0.88 / 0.87 / 0.80 / 0.83 | EDIA_m | Astex (85) / PDBbind (277) / RNP-F (919) / RNP (2604) | Fig 1F p6 |
| Median ligand net charge | −0.07 / −0.08 / −0.72 / −0.29 | e | Astex (85) / PDBbind (285) / RNP-F (919) / RNP (2679) | Fig 1G p6 |
| Median top-pose RMSD by ligand flexibility, AC_norm vs Vina(exh 100), RNP-F | AC 1.81→2.10, Vina 2.44→3.69 across dihedral bins (0,4] n=263 → (12,30] n=71 | Å | deposited pose | Fig 4C p11 |
| Median top-pose RMSD by ligand burial, AC_norm vs Vina(exh 100), RNP-F | AC 3.12→0.82, Vina 6.79→1.75 across burial bins (0.0,0.8] n=96 → (0.95,1.0] n=374 | Å | deposited pose | Fig 4D p11 |
| Median top-pose RMSD by ligand density fit, AC_norm vs Vina(exh 100), RNP-F | AC 2.01→0.78, Vina 3.20→1.66 across EDIA_m bins (0.0,0.5] n=117 → (0.9,1.2] n=161 | Å | deposited pose | Fig 4E p11 |
| Median top-pose RMSD by ligand charge, AC_norm vs Vina(exh 100), RNP-F | AC 1.83→3.60, Vina 4.34→5.33 across charge bins (−4,−2] n=78 → (1,4] n=16 | Å | deposited pose | Fig 4F p11 |
| Docking wall-clock cost | AC_norm 45 min; AC_long 165 min; Vina/Smina exh 8 ~1 min; exh 100 ~15 min | CPU minutes per complex | single Intel Core i9 4.7 GHz (GNINA on Nvidia A100) | p4 |
| Structure-preparation yield | 2,806/2,812 (99.8%) prepared; 2,611 parameterised (195 failures, 7%); AC results for 2,597/2,611 (99.5%) | complexes | RNP | p3–4 |

  **Stratified comparison — n per stratum (the point of the paper).** Bin edges are overall
  similarity to the training set (pocket coverage × SuCOS / 100), read from the Fig 5A/B tick
  labels, p14. Bin n values are printed on the axis; success-rate values are **not tabulated
  anywhere in the paper** and are read off the plotted markers (±1–2 percentage points).

| similarity bin | RNP common subset, n | AF3 (%) | AC (%) | Vina (%) | RNP-F common subset, n | AF3 (%) | AC (%) | Vina (%) |
|---|---|---|---|---|---|---|---|---|
| 0–20 | 63 | ~19 | ~44.5 | ~38 | 36 | ~17 | ~47 | ~50.5 |
| 20–30 | 110 | ~21 | ~28 | ~19.5 | 58 | ~24 | ~40 | ~24 |
| 30–40 | 153 | ~28 | ~45.5 | ~28 | 74 | ~24.5 | ~66 | ~40.5 |
| 40–50 | 274 | ~41.5 | ~47 | ~30 | 156 | ~41 | ~52 | ~38.5 |
| 50–60 | 328 | ~53.5 | ~48 | ~28.5 | 134 | ~49 | ~54 | ~36.5 |
| 60–70 | 390 | ~68.5 | ~48.5 | ~24 | 135 | ~72.5 | ~61 | ~33.5 |
| 70–80 | 391 | ~75 | ~43 | ~26 | 106 | ~77.5 | ~62 | ~33 |
| 80–100 | 738 | ~87 | ~56 | ~30 | 155 | ~79.5 | ~70 | ~33.5 |
| **total** | **2,448** | | | | **854** | | | |

  Crossover point: **AF3 overtakes AC between the 40–50 and 50–60 bins on RNP, and between the
  50–60 and 60–70 bins on RNP-F** — i.e. the filtered, higher-quality set pushes the crossover to
  *higher* similarity, which is the "trends are even more evident" of p13. AC beats AF3 in the
  four lowest RNP-F bins (n = 36 + 58 + 74 + 156 = 324 of 854 cases). Vina's advantage over AF3 is
  confined to the lowest two bins and is within the overlapping bootstrap CIs there.
  **Success criterion for this table: RMSD ≤ 2 Å AND LDDT-PLI > 0.8, top pose (p5).**
  **Which AC and Vina settings feed Fig 5 is never stated** — see `unresolved`.

- **n_predictions**: recorded as separate quantities, per the schema.
  - **Systems**: 2,812 annotated proper ligand–protein systems available (p3); 2,806 prepared;
    2,611 parameterised for both pipelines; **2,597 with AC results** (p4).
  - **Common subsets actually plotted**: **2,580** (RNP) and **891** (RNP-F) for the six docking
    runs (Fig 4A/B panel titles, p11); **2,448** (RNP) and **854** (RNP-F) for the AF3-vs-docking
    comparison (Fig 5 caption p14, Tab 2 caption p15).
  - **Clusters**: 921 (RNP), 878 (AC results), 516 (RNP-F). PDB IDs: 2,488.
  - **Samples per target, docking**: AC_norm max **3,072** initial ligand poses; AC_long max
    **12,288**; 4 random initial conditions; 90° initial ligand rotation (p4). **The number of
    output poses retained per complex is NOT REPORTED**, and the Vina/Smina/GNINA `num_modes`
    setting is **NOT REPORTED** (only exhaustivity is given) — which matters because the
    "all poses" metric depends on it.
  - **Samples per target, co-folding**: **NOT REPORTED** — the AF3 predictions were imported from
    RNP and the number of seeds/samples behind each is never stated here (p5).
  - **Total docking runs**: six configurations (AC_norm, AC_long, Vina exh 8, Vina exh 100,
    Smina/Vinardo exh 8, GNINA exh 8) × ~2,600 systems ≈ 1.5 × 10⁴ dockings, **not stated as a
    total by the paper**; Vina exhaustivity 1 was also tried (p4) but does not appear in Fig 4.
- **comparable_to_ours**: *(left empty by the extractor, per v3)*
- **si_in_scope**: **SI NOT HELD — and it holds real content, not just extras.** The 21-page PDF
  contains no supplementary material. Cited and missing: **Fig S1** (ChimeraX vs CHARMM SASA
  comparison, p5), **Fig S2** (the LDDT-PLI validity check that underwrites the combined success
  criterion, p5), **Fig S3** (OiiSTER molecular-beauty categories, p7), **Fig S4** (the Fig 3
  property analysis repeated for RNP-F, p9), **Fig S5** (property profile of consistent scoring
  failures vs successes, p12), **Fig S6** (the density/exposure explanation for the 20–30 bin dip,
  p13, and the density–similarity correlation, p15), **Fig S7** (the Fig 5C/D 2-D stratification
  repeated for RNP-F, p14), **Tabs S1–S3** (the per-model logistic regression detail behind Tab 2,
  p15). Also not held: the **full per-complex results, input files and annotations**, deposited at
  Zenodo **10.5281/zenodo.17865538** (p3, p17), which is where any per-target number would have to
  come from. Consequence: the stratified success rates themselves exist in this corpus only as
  values read off Fig 5A/B.

## F. Figures

Seven panel-group rows across five figures. Splits follow the v3 rule (split on `mark` or
`measure`, not on `facet`): Fig 1's nine panels share a mark and are one row with a compound
measure; Fig 3's nine heatmaps likewise; Fig 4 splits into a bar row and a violin row; Fig 5
splits into a line row and a matrix row. Panel structure for Figs 1, 3, 4 and 5 was confirmed by
rendering pages 6, 9, 11 and 14 (four renders, since those captions do not carry the panel grid;
renders deleted after reading).

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 6 | Nine physicochemical / crystallographic properties of the Astex, PDBbind, RNP and RNP-F sets side by side, establishing that RNP is larger-ligand, more flexible, more charged and worse-resolved than the classical benchmarks | violin with overlaid strip of individual points | `PLOT \| facet: property (9: X-ray resolution, R-free, heavy atoms, rotatable dihedrals, ligand burial, mean ligand B-factor, ligand EDIA_m, EDIA_m of 5 Å environment, ligand charge) \| vary: benchmark set (4: Astex, PDBbind, RNP-F, RNP) \| series: none (1) \| measure: the panel's property, in its own units \| mark: violin \| n: printed per violin, 83–2812 depending on panel and set; 36 violins total` | 9 lettered A–I; panels vary by property only, the same 4 sets in every panel; **panel letters run out of reading order (A,B,C / D,I,H / E,F,G)** | Only medians and means are annotated numerically; **no dispersion statistic, no test, no CI** for any of the 36 distributions, so "RNP has larger and more flexible ligands" is asserted from two black markers. n differs *between panels for the same set* (RNP is 2812, 2679, 2611, 2610, 2604, 2603 depending on panel) with no explanation of the drop-out in the figure itself | CC-BY 4.0 International, **no ND clause** — redrawing permitted with attribution. License line printed in the header of every page, p1–21 |
| 2 | 7 | Six hand-picked RNP complexes illustrating data-quality pathologies: a well-defined ligand, two ligands only partially covered by density, a dual-conformation case entered twice, a −12-charge phosphorylated ligand, and a complex the authors argue cannot physically bind as modelled | structure render with electron density mesh | `RENDER \| facet: pathology class (6: well-defined 8icz/S93; partially defined 8fz1/YVB; partially defined 8eqz/WQB; alternative conformations 7wdg/IC6; non-druglike −12 charge 7mog/KDJ; unphysical model 8cpb/AH0) \| views: 1 \| overlay: 1 docking pose on 1 reference in panel B (AC best pose, cyan, vs PDB model); 0 in the other five \| axis: none` | 6 lettered A–F; panels vary by system/pathology, not by camera angle. Density maps contoured at 1σ | The argument that 19% of RNP is unusable rests quantitatively on the EDIA_m distribution (Fig 1E), not on this figure; **these six are chosen exemplars with no indication of how representative they are**, and panel B's claim ("displays as good a density fit as the ligand conformation in the PDB model") is made by eye with no EDIA_m value given for the docked pose | CC-BY 4.0, no ND, p7 (license header) |
| 3 | 9 | RNP composition and ligand properties resolved simultaneously along the two axes of the similarity annotation, showing that the low-similarity corner is systematically populated by large, flexible, exposed, poorly-resolved ligands | heatmap grid | `MATRIX \| rows: ligand pose similarity, SuCOS bins (7: (0,40], (40,50], (50,60], (60,70], (70,80], (80,90], (90,100]) \| cols: pocket coverage bins (7, same edges) \| value: compound — % of cases; count of training systems with a similar ligand; median X-ray resolution; median dihedrals; median heavy atoms; median burial; median EDIA_m; median absolute charge; median charge \| facet: quantity displayed (9)` | 9 heatmaps of 7×7 cells; marginal % of cases printed along both axes of the first panel | **"Bins with less than 5 cases are omitted for clarity in the other plots"** (caption) — the omitted cells are simply blank and indistinguishable from cells that were never possible, and **no per-cell n is shown in any of the eight property panels**, so a cell median may rest on 5 observations or 1,400. The marginal distribution shows 48.0% of all cases in one pocket-coverage column and 59.3% in the top column overall, which the colour scale (capped at 10%) visually flattens | CC-BY 4.0, no ND, p9 |
| 4A-B | 11 | Head-to-head docking success rates for six configurations of four programs, at three RMSD thresholds for the top pose plus a rank-independent any-pose rate, on RNP and on RNP-F | grouped bar | `PLOT \| facet: benchmark set (2: RNP 2,580 common cases; RNP-F 891) \| vary: success criterion (4: top pose ≤1.0 Å, ≤1.5 Å, ≤2.0 Å, any pose ≤2.0 Å) \| series: docking configuration (6: Vina exh 8, Vina exh 100, Smina/Vinardo exh 8, GNINA exh 8, AC_norm, AC_long) \| measure: RMSD success rate (%) \| mark: bar \| n: 2,580 per bar in A and 891 per bar in B; 48 bars total` | 2 panels, A and B, differing only by benchmark set | **No error bars or confidence intervals on any of the 48 bars**, while Fig 5 computes bootstrap CIs for the same quantity — so the 54–59% vs 33–43% gap is presented without uncertainty. **No numeric labels**; every value in the text ("54–59%", "33–43%") must be read off bar heights. The "All Poses 2.0 Å" group is a rank-independent oracle-selected rate sitting in the same axes as three top-1 rates, inviting exactly the comparison it must not be used for | CC-BY 4.0, no ND, p11 |
| 4C-F | 11 | Top-pose RMSD distributions for AC_norm and Vina (exh 100) on RNP-F, stratified by four physical properties, showing degradation with flexibility, exposure, poor density and high charge | violin with overlaid points and annotated medians | `PLOT \| facet: stratifying property (4: rotatable dihedrals; ligand burial; ligand density fit EDIA_m; ligand charge) \| vary: property bin (6 bins in C, 5 in D, 6 in E, 5 in F — bin edges printed) \| series: docking program (2: AC_norm orange, Vina exh 100 green) \| measure: top-pose RMSD (Å) \| mark: violin \| n: printed under every bin, 16–457 per bin; 2 violins per bin, 44 violins total` | 4 panels C–F; only 2 of the 6 configurations from A/B are carried forward, stated in the caption | Only RNP-F is shown, so the reader cannot check whether the same property dependence holds on unfiltered RNP. Medians are annotated but **no dispersion, no test, no CI**; the lowest-n bins (charge (1,4] n=16, dihedrals (10,12] n=56) carry annotated medians with the same visual authority as n=457 bins. Panel F's y-axis extends to −5 Å, below the physical floor of an RMSD | CC-BY 4.0, no ND, p11 |
| 5A-B | 14 | **The central result**: success rate of AlphaFold 3, Attracting Cavities and AutoDock Vina as a function of similarity to the training set, on RNP and on the filtered RNP-F, showing AF3 rising monotonically through the docking baselines while the docking curves stay flat | line with shaded 95% bootstrap CI ribbon | `PLOT \| facet: benchmark set (2: RNP common subset 2,448 cases; RNP-F common subset 854) \| vary: similarity to the training set, 8 bins (0–20, 20–30, 30–40, 40–50, 50–60, 60–70, 70–80, 80–100) \| series: method (3: AlphaFold3, AC, Vina) \| measure: success rate (%), RMSD ≤ 2 Å and LDDT-PLI > 0.8, top pose \| mark: line+point with CI ribbon \| n: per bin printed on tick labels — RNP 63/110/153/274/328/390/391/738; RNP-F 36/58/74/156/134/135/106/155` | 2 panels A and B, differing only by benchmark set; 3 series each; ribbon = 95% CI from 1,000 bootstrap resamples per bin per method | The bins are **unequal by more than an order of magnitude (n = 63 to n = 738) but evenly spaced on a categorical axis**, so the eye weights the 63-case bin as heavily as the 738-case one; n is printed but small. The first bin is 20 units wide and the last 20 units wide while the middle six are 10 units wide, again evenly spaced. **The legend says "AC" and "Vina" without stating which of the six configurations from Fig 4 is plotted** — the single most consequential omission in the figure. Success-rate values are never tabulated anywhere in the paper, in the SI, or in the text | CC-BY 4.0, no ND, p14 |
| 5C-D | 14 | The same comparison decomposed into two dimensions: success rate per method across pocket-coverage × ligand-SuCOS bins (C) and across ligand-burial × rotatable-dihedral bins (D), showing AF3's success tracking the similarity axes and docking's tracking the physical axes | heatmap grid | `MATRIX \| rows: ligand pose similarity SuCOS (7 bins) in C, number of rotatable dihedrals (7 bins) in D \| cols: pocket coverage (7 bins) in C, ligand burial (6 bins) in D \| value: compound — % of cases per bin in the leftmost panel of each row, success rate (%) in the other three \| facet: row × method (2 stratification schemes × 4 panels: cases-per-bin, AlphaFold 3, Attracting Cavities, AutoDock Vina)` | 8 heatmaps in 2 rows of 4; each row's first panel is the cases-per-bin reference for that row's axes | **No per-cell n in any success-rate panel.** Cells reading exactly 0.0 and 100.0 appear in all three methods' panels — these are necessarily tiny-n cells, and they are coloured at full saturation, giving single-observation cells the same visual weight as the 41.4%-of-cases cell. The cases-per-bin panels are on a colour scale capped at 10% while single cells hold 15.1% and 23.1%, flattening the imbalance the paper elsewhere argues is a defect of RNP. The RNP-F equivalents are deferred to Fig S7, which is not in the PDF | CC-BY 4.0, no ND, p14 |

Tables (not figure rows, listed for retrieval): **Tab 1 p12** — scoring-failure percentages for
4 scoring functions × 4 benchmark sets plus the two intersections; ND for Vinardo/GNINA on Astex
and PDBbind. **Tab 2 p15** — logistic regression coefficients and SEs for AF3/AC/Vina on 2,448
common RNP cases, with accuracy and AUC; coefficients with P < 0.001 in bold.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), single-paper extraction, schema v3
- **schema_version**: v3
- **confidence**: **high** for everything stated in text, Tab 1 and Tab 2; **medium** for the
  stratified success-rate values in section E, which are read off the Fig 5A/B markers because the
  paper tabulates them nowhere (the per-bin **n** values, by contrast, are printed on the tick
  labels and are high-confidence); **medium** for the Fig 4A/B bar heights quoted for the 1.0 Å,
  1.5 Å and any-pose criteria, same reason. What was hard: (i) the paper reports six docking
  configurations in Fig 4 but only "AC" and "Vina" in Fig 5, and never says which; (ii) three
  different "common subset" sizes are in play (2,597 AC results, 2,580 six-way docking common,
  2,448 AF3-inclusive common; and 919 RNP-F / 891 / 854) and the paper does not tabulate the
  reconciliation; (iii) every supporting analysis is in an SI that is not in this PDF.
- **unresolved**:
  1. **Which AC and which Vina configuration is plotted in Fig 5 and modelled in Tab 2.** Fig 4's
     caption states AC_norm and Vina exh 100 for its own panels C–F; nothing states it for Fig 5
     or Tab 2. This directly affects how the headline comparison should be cited — AC_norm vs
     AC_long differ by ~4–5 points of success rate (Fig 4A/B).
  2. **Reconciliation of subset sizes.** 2,812 annotated → 2,806 prepared → 2,611 parameterised →
     2,597 AC results (878 clusters) → 2,580 six-way docking common → 2,448 AF3-inclusive common;
     and 919 RNP-F → 891 → 854. The 164-case gap between 2,612 and 2,448 is presumably cases where
     RNP has no AF3 prediction, but the paper does not say.
  3. **Whether the GNINA CNN and the Vinardo empirical function have their own training-data
     overlap with RNP.** The paper's entire framing is that RNP is post-cutoff for *co-folding*
     training. GNINA is a deep-learning scorer (ref 27) and Vinardo is fitted to PDBbind-era data
     (ref 26); neither is checked for leakage, and both appear in the "physics-based" column of
     Fig 4 and Tab 1. AC (CHARMM force field + FACTS) and Vina are the only two arms for which the
     "no training set" argument is straightforwardly true — and they are, correctly, the two shown
     in Fig 5.
  4. **The LDDT-PLI validity check is reported at a different threshold than the one used.** p5
     validates that "almost all docking poses with a RMSD below 2 Å have a LDDT-PLI above 0.65",
     but the success criterion is LDDT-PLI > 0.8. The gap is not addressed; Fig S2 is not in the
     PDF.
  5. **How many output poses per complex.** AC's *input* pose count is given (3,072 / 12,288) but
     the retained output count is not, and Vina/Smina/GNINA `num_modes` is never stated. The
     "all poses ≤ 2 Å" metric is a direct function of this.
  6. **AF3 arm settings.** Number of seeds/samples, MSA depth, template usage, and which AF3
     ranking was taken are all inherited silently from RNP (p5) and are unstated here.
  7. **Whether any RNP-F filter was chosen after seeing its effect on the comparison.** The five
     filters are each independently defensible, but three of them (max 100 analogues; one complex
     per PDB ID keeping lowest similarity; max 5 per cluster keeping lowest similarity) shift the
     set toward low similarity, and the paper reports the result as "trends are even more evident"
     (p13) without a pre-registration or a sensitivity analysis over filter choices.
  8. **`refs.bib` metadata mismatch**: `@misc{roehrig2026docking, … year = {2025} …}` while the
     citekey and this posted version are 2026 (posted April 20, 2026). Someone should decide which
     year the bibliography should carry for a v2 preprint.
  9. **The PDF does not print a version number.** "v2" is an external label; only "this version
     posted April 20, 2026" and the DOI stem `2025.12.09` are internal evidence.
  10. **Tags needed but not in the v3 vocabulary — not invented, reported here:**
      - **`docking`** (or `physics-based-docking`). There is no Method tag for classical
        small-molecule docking. This paper's entire contribution is a docking arm, and the closest
        available tag, `benchmark-only`, does not say that a physics baseline was run. A query for
        "which papers ran a docking baseline against co-folding" cannot currently be answered by
        tag. **This is the single most needed addition for this note.**
      - **`ligand-pose`** or similar, to mark that the prediction target is a small-molecule pose
        rather than a protein conformational state. Tagged `single-state` below because the
        receptor is rigid, but that tag will pull this paper into conformational-state queries
        where it does not belong.
      - **`self-benchmark`** or `author-is-method-author`, to mark that the winning method is the
        authors' own (AC / SwissDock). `contrast` does not capture it and it materially affects how
        the numbers should be cited.
      - **`training-similarity-stratified`**, to distinguish papers that *stratify* by similarity
        from papers that merely hold out by date. `anti-memorization` currently collapses both.
      - **`benchmark-refinement`**, for a paper whose contribution includes a filtered derivative
        of an existing benchmark (RNP → RNP-F).
- **why_it_matters**: *(left empty by the extractor, per v3 — the user's call)*

## Tags

`general-protein` `cofolding` `benchmark-only` `single-state` `binary-predicate`
`continuous-metric` `oracle-leak` `design-level-oracle` `anti-memorization` `preprint`
`contrast` `precedent` `negative-result` `comparator-numbers`

Tag notes, so the reverse lookups stay honest:
- **`cofolding`** because AlphaFold 3 is one of the two compared arms, even though no co-folding
  model was run by these authors (predictions imported from RNP, p5).
- **`benchmark-only`** is the closest available Method tag for the docking arm and for RNP-F; see
  `unresolved` item 10 — a `docking` tag is genuinely missing.
- **NOT `multi-backbone`**: only AlphaFold 3 is analysed (p3), despite RNP holding six co-folding
  methods. Tagging it would false-positive every multi-backbone query.
- **`single-state`** records the rigid receptor (p4); it does *not* mean this paper studied
  protein conformational states, which it does not.
- **NOT `rmsd-only`**: the success predicate is RMSD ≤ 2 Å **and** LDDT-PLI > 0.8 (p5).
- **`oracle-leak`** for pipeline routes 1, 5 and 6 (docking receptor and site taken from the
  target's own deposited structure; success and scoring-failure both defined against the deposited
  pose; the any-pose metric selected against it). **`design-level-oracle`** for route 7, kept
  distinct as the schema requires.
- **NOT `prospective`**: retrospective re-docking throughout.
- **NOT `templates-on` / `no-template-no-msa` / `state-annotated-input`**: the AF3 arm's protocol
  is not restated in this paper, so no protocol tag is supportable.
- **NOT `unpowered`**: the smallest stratum is n = 36, above the schema's n < ~10 threshold; the
  wide low-similarity CIs are recorded in `anti_memorization_control` instead.
- **NOT `figure-exemplar`**: this paper is kept for its substance, not as an out-of-field figure
  model, so tagging it would wrongly exclude it from gap analysis — even though Fig 5A/B is in
  fact the best stratified-comparison figure design in the corpus.
- **`negative-result`** records the finding *about co-folding* (AF3 loses to docking below ~50
  similarity), not a null result of the study.
- **`contrast` + `precedent`** mirror the dual `stance`, which is provisional and the user's call.
