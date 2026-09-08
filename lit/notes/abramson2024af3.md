# abramson2024af3

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say and
`NOT APPLICABLE` (with a reason) where the field asks something this paper never sets out to do.

**Page numbers below are PDF page numbers from `./pagetext.sh` markers (1–24).** The printed
Nature page number = PDF page + 492 for the article body: PDF p1 = Nature p493 … PDF p8 =
Nature p500. Methods (PDF p9–p11), Extended Data (PDF p12–p21) and the Nature Portfolio
Reporting Summary (PDF p22–p24) carry no printed page numbers. Layout: p1 abstract +
introduction, p2–p3 architecture, p4–p5 accuracy across complex types, p5 confidence, p5–p7
Model limitations, p7 Discussion, p8 references + licence, p9–p11 Methods + data/code
availability + references 49–73, p12–p20 Extended Data Figs 1–9, p21 Extended Data Table 1,
p22–p24 Reporting Summary.

**FRAMING.** This is a **model paper**, not a benchmark paper and not a conformational-states
study. It reports one new model (AF3) and its accuracy across biomolecular categories. Section C
fields that presuppose a states study (`directional_control`, and to a degree `state_metric` and
`metric_saturation`) are answered honestly as absent or marginal rather than forced. The two
things this note exists for in the corpus are (1) the **authoritative training/evaluation
cutoff**, in `anti_memorization_design`, and (2) **what the paper itself concedes about single
versus multiple conformations**, in `stated_limits` and `confidence_as_discriminator`. Both are
quoted verbatim with pages.

**A CONTRADICTION IN THE PRINTED METHODS, flagged up front because the corpus depends on this
number.** The Methods "Training regime" paragraph (p9) prints *30 September 2021* for the
PoseBusters model where every other statement in the paper (p5, p9 "Inference regime", p10
"PoseBusters") prints *30 September 2019*. See `anti_memorization_design` and `unresolved`. Use
**30 September 2021 for the standard AF3 model and 30 September 2019 for the PoseBusters
model**; the p9 sentence is almost certainly a typo in an article that carries "corrected
publication 2024" (p8).

**THE SI IS NOT HELD.** This 24-page PDF is the article + Methods + Extended Data only.
Supplementary Methods 1–8, Supplementary Algorithms 1–31, Supplementary Tables 3–15 and
Supplementary Fig. 2 are all cited and none is present. The training-data composition
(Supp. Methods 2.2, 2.5.1, 2.5.2), the ranking formula (5.9.3), the low-homology filter
definition (6.1) and the checkpoint-selection metric list (Supp. Table 7) therefore cannot be
checked from this PDF. See `si_in_scope`. Extended Data Table 1 *is* held (p21), so
`metrics_reported` is not emptied.

---

## A. Identity

- **citekey**: `abramson2024af3`
- **doi**: **10.1038/s41586-024-07487-w** (p1 masthead; repeated p8 "Online content" and
  "Supplementary information").
- **year**: **2024.** "Received: 19 December 2023 / Accepted: 29 April 2024 / Published online:
  8 May 2024" (p1). Footer on every article page: "Nature | Vol 630 | 13 June 2024".
  Copyright line p8: "© The Author(s) 2024, corrected publication 2024".
- **venue**: **Nature, vol. 630, pp. 493–500 (2024). Peer-reviewed, Open Access.** Explicit peer
  review statement on p11: "Peer review information Nature thanks Justas Dapkunas, Roland
  Dunbrack and Hashim Al-Hashimi for their contribution to the peer review of this work."
  Not a preprint.
- **title**: "Accurate structure prediction of biomolecular interactions with AlphaFold 3" (p1).
- **authors**: Josh Abramson, Jonas Adler, Jack Dunger, Richard Evans, Tim Green, Alexander
  Pritzel, Olaf Ronneberger, Lindsay Willmore *et al.* (equal-contribution block, alphabetical);
  jointly supervised by Victor Bapst, Pushmeet Kohli, Max Jaderberg, Demis Hassabis and John M.
  Jumper. Google DeepMind and Isomorphic Labs, London (p1). ~50 authors.
- **competing interests** (p11, recorded because it bears on how the numbers should be read):
  "Author-affiliated entities have filed US provisional patent applications including
  63/611,674, 63/611,638 and 63/546,444 … All of the authors other than A.B., Y.A.K. and E.D.Z.
  have commercial interests in the work described."
- **code availability** (p10): "AlphaFold 3 will be available as a non-commercial usage only
  server at https://www.alphafoldserver.com, with restrictions on allowed ligands and covalent
  modifications. Pseudocode describing the algorithms is available in the Supplementary
  Information. **Code is not provided.**" (Emphasis added; this is the state of affairs *as
  published*, and the note records only what the paper says.)

## B. Scope

- **system**: **general protein — and beyond protein.** The paper's scope is all of the PDB:
  "a model that is capable of high-accuracy prediction of complexes containing nearly all
  molecular types present in the Protein Data Bank32 (PDB)" (p1). Categories evaluated:
  protein–ligand, protein–protein, protein–antibody, protein monomer, protein–RNA,
  protein–dsDNA, RNA-only, DNA-only, bonded ligands, glycosylation, modified protein/DNA/RNA
  residues, ions. No GPCR, kinase or transporter arm exists; no protein family is singled out.
- **n_targets**: **heterogeneous by category, no single number; the paper never gives a total.**
  Per-arm (p2 Fig. 1c caption, p21 Extended Data Table 1, p9 Methods):
  - PoseBusters V1: **428 targets** (427 for RoseTTAFold All-Atom); PoseBusters V2: **308 targets**.
  - Recent PDB evaluation set: **8,856 PDB complexes** (p9).
  - protein–protein: **1,064 interface clusters**; protein–antibody: **65 interface clusters**
    (from 71 complexes / 166 antibody–antigen interfaces, p9); protein monomers: **338 clusters**.
  - protein–RNA: **25 structures**; protein–dsDNA: **38 structures**; RNA-only: **29 structures**;
    DNA-only: **63 structures**; CASP15 RNA: **8 targets scored** (10 of 13 available, p16).
  - bonded ligands: **66 clusters**; glycosylation: 28 (high-quality single-residue) / 167
    (all-quality single-residue) / 131 (all-quality multi-residue); modified residues: **154**
    (40 protein / 91 DNA / 23 RNA).
  - CAID 2 disorder set: **151 proteins, 46,093 residues** (p12).
  A single-system paper claiming generality is the thing to flag; this is the opposite case — a
  genuinely multi-category paper. The flag worth raising instead is that **no conformational
  category exists at all**: there is no arm in which two states of one system are both targets.
- **method_class**: **co-folding.** A single end-to-end generative model that predicts protein,
  nucleic acid, ligand, ion and modified-residue coordinates jointly: "it is possible to handle
  the wide diversity of chemical space within a general deep-learning framework and without
  resorting to an artificial separation between protein structure prediction and ligand docking"
  (p8). Architecturally it is a diffusion model — "We use a relatively standard diffusion
  approach33 in which the diffusion model is trained to receive 'noised' atomic coordinates and
  then predict the true coordinates" (p3) — but the corpus's `method_class` slot for this is
  `co-folding`; the diffusion detail is recorded here rather than invented as a class.
- **backbones**: **AF3 (this paper's own model), compared head to head against AlphaFold-Multimer
  v.2.3, RoseTTAFold2NA and RoseTTAFold All-Atom**, plus non-backbone docking baselines
  (AutoDock Vina, Gold, Vina on AF-M 2.3, EquiBind, TankBind, DiffDock, DeepDock, Uni-Mol,
  Uni-Mol Docking V2, UMol) and CASP15 RNA entrants (AIchemy_RNA, AIchemy_RNA2, RNApolis, Chen,
  Kiharalab, UltraFold). Four structure-prediction backbones compared directly (AF3, AF-M 2.3,
  RF2NA, RFAA), which is more than two — `multi-backbone` tagged, with the judgement noted in
  `unresolved`. RF2NA was run by the authors "with the same MSAs as those that were used for AF3
  predictions" (p9); RFAA and the CASP entrants were taken from published/CASP results (p5, p10).
- **templates**: **on.** The architecture contains a template module (2 blocks) fed by a template
  search (Fig. 1d, p2). Templates are date-filtered, not state-annotated: "No inference time
  templates or reference ligand position features were released after 30 September 2021, and in
  the case of PoseBusters evaluation, an earlier cut-off date of 30 September 2019 was used"
  (p9). Template search used "a version [of the PDB] downloaded 28 September 2022" (p10). There
  is **no state-annotated template selection** anywhere in the paper.
- **msa_handling**: **full** (deliberately de-emphasised, but not subsampled, clustered, filtered
  or pinned). "The system reduces the amount of multiple-sequence alignment (MSA) processing by
  replacing the AF2 evoformer with the simpler pairformer module" (p1); "Within the trunk, MSA
  processing is substantially de-emphasized, with a much smaller and simpler MSA embedding
  block… the number of blocks is reduced to four… the MSA representation is not retained and all
  information passes through the pair representation" (p2). Genetic search feeds an MSA module
  (Fig. 1d, p2). MSA databases listed p10: UniRef90 (2020_01, 2020_03, 2022_05), Uniclust30
  (2018_08, 2021_03), MGnify (2018_12, 2022_05), BFD, RFam v.14.9, RNAcentral v.21.0, NCBI
  Nucleotide DB, JASPAR 2022, and SELEX sequences from refs 72–73. **Reduced MSA *processing* is
  not MSA subsampling** — no depth reduction or clustering is applied as a state handle, and the
  two must not be collapsed. The only MSA-depth manipulation in the paper is *analytical*
  (Extended Data Fig. 7a plots accuracy against natural Neff, p18), not interventional.

## C. Conformational core

### `states_generated`

**ensemble + single-state.** This dual value is not a stretch here — it is exactly what the paper
reports about itself.

The *ensemble* half: AF3 is a generative diffusion model that produces many samples per target.
"Importantly, this is a generative training procedure that produces a distribution of answers"
(p3). "The model can be run with different random seeds to generate alternative results, with a
batch of diffusion samples per seed" (p9). Standard inference is 5 seeds × 5 diffusion samples =
25 samples; the antibody arm goes to 1,000 seeds × 5 samples (p2, p7, p9).

The *single-state* half: those samples do not spread over conformational states. Verbatim, p6:

> "A key limitation of protein structure prediction models is that they typically predict static
> structures as seen in the PDB, not the dynamical behaviour of biomolecular systems in solution.
> This limitation persists for AF3, in which multiple random seeds for either the diffusion head
> or the overall network do not produce an approximation of the solution ensemble."

and the one concrete conformational test in the paper, p6:

> "In some cases, the modelled conformational state may not be correct or comprehensive given the
> specified ligands and other inputs. For example, E3 ubiquitin ligases natively adopt an open
> conformation in an apo state and have been observed only in a closed state when bound to
> ligands, but AF3 exclusively predicts the closed state for both holo and apo systems42
> (Fig. 5c)."

with the figure caption, p7:

> "c, Conformation coverage is limited. Ground-truth structures (grey) of cereblon in open (apo,
> PDB: 8CVP; left) and closed (holo mezigdomide-bound, PDB: 8D7U; right) conformations.
> Predictions (blue) of both apo (with 10 overlaid samples) and holo structures are in the closed
> conformation."

Ten overlaid diffusion samples of the apo system all land in the closed basin. That is
sampling-that-collapses, which is precisely the case the v3 schema added the dual value for.
n = 1 system, so it is an illustration, not a measurement — see `anti_memorization_control` and
`unresolved` for how thin the quantitative support for this limitation is.

### `structural_priors_used`

What deposited structural knowledge shaped the work at design time. For a model paper this field
is large and is **not a defect**.

1. **The PDB is the training set.** "Training used a version of the PDB downloaded 12 January
   2023" (p10); structures "were used for training and as templates
   (https://files.wwpdb.org/pub/pdb/data/assemblies/mmCIF/; sequence clusters are available at
   https://cdn.rcsb.org/resources/sequence/clusters/clusters-by-entity-40.txt …)" (p10). The
   40%-identity RCSB entity clusters are used for clustering (p10, and cluster-weighted scoring
   p9). Date-bounded: "No structural data used during training were released after 30 September
   2021" (p9).
2. **Predicted structures were used in training — yes, distillation.** This is the field's
   headline answer for this paper. "The biggest issue is that generative models are prone to
   hallucination35, whereby the model may invent plausible-looking structure even in unstructured
   regions. To counteract this effect, **we use a cross-distillation method in which we enrich
   the training data with structures predicted by AlphaFold-Multimer (v.2.3)7,8**. In these
   structures, unstructured regions are typically represented by long extended loops instead of
   compact structures, and training on them 'teaches' AF3 to mimic this behaviour. This
   cross-distillation greatly reduced the hallucination behaviour of AF3" (p4). Restated p6: "To
   encourage ribbon-like predictions in AF3, we use distillation training from AF2 predictions".
   Extended Data Fig. 1 names it "the disordered protein PDB cross distillation set" (p12), which
   suggests the distillation set is scoped to disordered proteins; the main text says only
   "enrich the training data", and Supp. Methods 2.5 is not held. See `unresolved`.
3. **Templates from the PDB**, date-filtered (see `templates` above), plus a template module in
   the architecture (Fig. 1d, p2).
4. **Reference conformers / the Chemical Components Dictionary.** "We also used the Chemical
   Components Dictionary downloaded on 19 October 2023" (p10); the architecture includes
   "Conformer generation" feeding the input embedder (Fig. 1d, p2), and "the model receiv[es]
   reference structures with correct chirality as input features" (p5). Ligand geometry priors
   are therefore explicit inputs; note the CCD snapshot (Oct 2023) postdates both training
   cutoffs, which is a chemical-dictionary prior, not a structural one, but is worth recording.
5. **Sequence/MSA databases** (p10, listed under `msa_handling`), plus JASPAR 2022 and SELEX
   sequence sets for DNA-binding specificity.
6. **Choice of showcase systems from what is deposited.** "In selecting these examples, we
   considered novelty in terms of the similarity of individual chains and interfaces to the
   training set (additional information is provided in Supplementary Methods 8.1)" (p4) — Fig. 3's
   six examples were picked with training-set similarity in hand. Also design-level: the cereblon
   open/closed pair (Fig. 5c) was chosen precisely because both states are deposited (8CVP, 8D7U)
   and the failure was already characterised in ref. 42.
7. **Training-mixture weights were adjusted using observed per-capability behaviour**: "we
   observed that some model abilities topped out relatively early and started to decline (most
   likely due to overfitting to the limited number of training samples for this capability),
   while other abilities were still undertrained. We addressed this by increasing or decreasing
   the sampling probability for the corresponding training sets" (p4). This is a *design-time*
   use of structural knowledge; the *leakage* aspect of it (that the observation was made on the
   evaluation set) is recorded under `oracle_leakage` route 4, not here.

### `oracle_leakage`

**The key field.** Seven routes, each answered separately. Summary: **no state-oracle leakage of
the kind this corpus hunts (routes 2, 3 clean), one real and consequential model-selection
leakage (route 4), the normal retrospective-scoring situation (route 5), a narrow reference-
assisted assignment (route 6), and clearly-labelled design-level and privileged-information arms
(routes 1, 7).** The paper is unusually explicit about which of its baselines use privileged
information, and about the fact that AF3 itself does not.

**Route 1 — structures used as input or template. PARTIALLY PRESENT, date-filtered, and one
arm is explicitly privileged.**

- Templates are used, date-bounded: "No inference time templates or reference ligand position
  features were released after 30 September 2021, and in the case of PoseBusters evaluation, an
  earlier cut-off date of 30 September 2019 was used" (p9). Templates are searched, not supplied
  per-target by hand, and are not state-annotated. This is standard AF-family template use, not
  target-state leakage.
- The **main AF3 protein–ligand arm takes no structural input**, and the paper says so
  repeatedly: "AF3 greatly outperforms classical docking tools such as Vina37,38 **even while not
  using any structural inputs**" (p4); "The baseline models come in two categories: those that
  use only protein sequence and ligand SMILES as an input and **those that additionally leak
  information from the solved protein–ligand test structure**. Traditional docking methods use
  the latter privileged information, even though that information would not be available in
  real-world use cases" (p4); "While AlphaFold models are 'blind' to the protein pocket, docking
  is often performed with knowledge of the protein pocket residues" (p10). The word *leak* is the
  authors' own.
- **One AF3 arm is deliberately privileged and labelled as such**: "To evaluate the ability of
  AF3 to dock ligands accurately when given pocket information, we fine-tuned a 30 September 2019
  cut-off AF3 model with an additional token feature specifying pocket–ligand pairs… an
  additional token feature was introduced, set to true for a ligand entity of interest and any
  pocket residues with heavy atoms within 6 Å of the ligand entity" (p10). Those 6 Å pocket
  residues come from the ground-truth complex. Extended Data Fig. 4a classifies every method "by
  the extent of ground truth information used to make predictions" (p15). This arm is the 90.2%
  (V1) / 93.2% (V2) number in Extended Data Table 1 — **not the headline 76.4% / 80.5%.** Anyone
  quoting AF3's PoseBusters number must not quote the pocket-specified row as blind.
- **Ground-truth-informed input preparation on PoseBusters**: "Inference was performed on the
  asymmetric unit from specified PDBs, with the following minor modifications. In several PDB
  files, chains clashing with the ligand of interest were removed (7O1T, 7PUV, 7SCW, 7WJB, 7ZXV,
  8AIE). Another PDB entry (8F4J) was too large to inference the entire system (over 5,120
  tokens), so we included only protein chains within 20 Å of the ligand of interest" (p10).
  Deciding which chains clash with, or lie within 20 Å of, the ligand requires the deposited
  coordinates. Seven of 428 targets; small, honestly disclosed, and it concerns *which chains are
  in the input*, not where the ligand goes — but it is route 1 and is recorded as such.

**Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates
or alignments. NONE FOUND.** No state-annotated database appears anywhere in the paper. The
complete list of databases used is given on p10 ("Data availability") and comprises PDB, the RCSB
40% entity sequence clusters, the Chemical Components Dictionary, UniRef90, Uniclust30, MGnify,
BFD, RFam, RNAcentral, the NCBI Nucleotide Database, JASPAR 2022 and two SELEX sequence sets —
all sequence, chemistry or raw-structure resources, none carrying conformational-state labels.
Protocol described p9 ("Training regime", "Inference regime") and p10 ("Data availability").

**Route 3 — cluster labels derived from known states. NONE FOUND.** Clustering exists throughout
but is **sequence-identity clustering for score aggregation**, never state clustering:
"clustering was then applied to chains and interfaces so that scores could be aggregated first
within clusters and then across clusters for mean scores, or using a weighting of inverse cluster
size for distributional statistics" (p9); the cluster source is
"clusters-by-entity-40.txt" (p10). Antibody identification is likewise by sequence cluster size,
not by annotation: "we filter the low homology recent PDB set to complexes that contain at least
one protein–protein interface where one of the protein chains is in one of the two largest PDB
chain clusters (these clusters are representative of antibodies)" (p9). Protocol p9.

**Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known
structures. PRESENT, and this is the substantive rigour finding of the note.** Not tuned against
*states* (there are none), but tuned against the *evaluation set that is then used to report
accuracy*:

> "During AF3 development, we observed that some model abilities topped out relatively early and
> started to decline (most likely due to overfitting to the limited number of training samples
> for this capability), while other abilities were still undertrained. We addressed this by
> increasing or decreasing the sampling probability for the corresponding training sets
> (Supplementary Methods 2.5.1) and by **performing early stopping using a weighted average of
> all of the above metrics and some additional metrics to select the best model checkpoint**
> (Supplementary Table 7)." (p4)

The metrics in question are computed on the evaluation set, as Fig. 2d states outright: "Training
curves for initial training and fine-tuning stages, showing **the LDDT on our evaluation set** as
a function of optimizer steps" (p3; identically Extended Data Fig. 2, p13). So checkpoint
selection *and* training-set mixture weights were chosen against the recent-PDB evaluation set,
and the recent-PDB evaluation set then supplies the protein–protein, antibody, monomer, nucleic
acid and modified-residue headline numbers. Under the v3 rule that **tuning a range on the
evaluation set is leakage even when no single value is picked per target**, this qualifies. Two
mitigations, both real: the selection is global (one checkpoint for all categories, not per
target), and the PoseBusters arm is genuinely insulated from it because PoseBusters is not the
evaluation set and the PoseBusters model was retrained from scratch with a 2019 cutoff.
Supplementary Table 7, which would say exactly which metrics drove checkpoint selection, is not
held.

A second, narrower route-4 instance: the ranking formula was modified in response to a defect
observed on the benchmark being reported. "To address this in the PoseBusters benchmark, **we
included a penalty for chirality violation in our ranking formula for model predictions**.
Despite this, we still observe a chirality violation rate of 4.4% in the benchmark" (p5); also
"Penalizing clashes during ranking (Supplementary Methods 5.9.3) reduces the occurrence of this
failure mode but does not eliminate them" (p5); "Unless otherwise stated, predictions are
top-ranked by our global complex ranking metric with chiral mismatch and steric clash penalties"
(p7). The penalties use only properties of the prediction itself (chirality against the input
reference conformer, atom overlaps), not the ground-truth pose — so the *ranking signal* is not
an oracle. What is benchmark-informed is the *decision to add the terms*.

**Route 5 — success defined post hoc by RMSD or TM to a structure they had. PRESENT BY
CONSTRUCTION, and normal for a retrospective structure-prediction benchmark; one instance is
conformationally interesting.** All metrics compare to held ground truth: "Evaluation compares a
predicted structure to the corresponding ground-truth structure" (p9); success criteria are
pocket-aligned ligand r.m.s.d. < 2 Å, DockQ > 0.23, LDDT, iLDDT (p2 Fig. 1c caption, p9). The
thresholds are inherited standards (DockQ > 0.23 = "correct", > 0.8 = "very high accuracy",
ref. 40; r.m.s.d. < 2 Å = PoseBusters convention, ref. 30), not tuned here. The one instance that
matters to a conformational corpus:

> "We compare the top-1 ranked predictions and, **where multiple ground-truth structures exist
> (R1136), the prediction is scored against the closest state**." (p10)

That is best-of-reference scoring: the single place in the paper where more than one state of a
target exists, and it is resolved by scoring against whichever the prediction is nearest. n = 1
target, disclosed, in a CASP15 RNA arm — small, but it is exactly the practice the corpus tracks.

**Route 6 — best/worst model labels assigned against a held reference. LARGELY NONE FOUND, with
one mechanical exception.** Sample selection is by *predicted confidence*, not against the
reference: "All scores are reported from the top confidence-ranked sample out of five model seeds
(each with five diffusion samples)" (p2); "Results are shown for the top-ranked sample and sample
ranking depends on whether trying to select the overall best output globally, or the best output
for some chain, interface or modified residue. Global ranking uses a mix of pTM and ipTM along
with terms to reduce cases with large numbers of clashes and increase rates of disorder;
individual chain ranking uses a chain specific pTM measure; interface ranking uses a bespoke ipTM
measure for the relevant chain pair; and modified residue ranking uses average pLDDT over the
residue of interest" (p9); Extended Data Fig. 7b: "Predictions are ranked by confidence, and only
the most confident per interface is scored" (p18). Fig. 5a explicitly ranks by predicted ipTM,
not by DockQ (p7). **This is the honest configuration** and is the reason `confidence_as_
discriminator` below is a genuine finding rather than an artefact.

The exception is chain/atom **assignment**, which is resolved against the ground truth: "If the
complex contains multiple identical entities, assignment of the predicted units to the
ground-truth units is found by **maximizing LDDT**. Assignment in local symmetry groups of atoms
in ligands is solved by exhaustive search over the first 1,000 per-residue symmetries as given by
RDKit" (p9); and during training "This predicted structure is then used to permute the symmetric
ground-truth chains" (p4). Symmetry resolution against the reference is standard practice and
does not select which *model* is scored, only which labelling of an already-chosen model — but it
is a reference-assisted step and is recorded.

**Route 7 — design-level oracle use (systems or input conditions chosen because the expected
answer is already known). PRESENT AND MILD; label it design-level, not pipeline leakage.**

- Fig. 3 showcase selection: "In selecting these examples, we considered novelty in terms of the
  similarity of individual chains and interfaces to the training set" (p4). Six hand-picked
  successes, chosen with training-set similarity known.
- Fig. 5b–e failure showcase: four hand-picked failures, chosen after the fact (chirality on
  7CTM, conformation coverage on cereblon, hallucination on 7F60, clashes on 7PEU) (p7).
- The cereblon conformational test itself: both states were already deposited and the open/closed
  ligand dependence already published (ref. 42, Watson *et al.*, *Science* 2022). The expected
  answer was known before the prediction was read. This does not invalidate the observation — the
  model failed the test — but a corpus reading Fig. 5c as evidence should know it is one
  pre-selected system, not a survey.
- Extended Data Fig. 3 selects "PoseBusters examples for which Vina and Gold were inaccurate"
  (p14): three cases chosen by the baseline's failure.
- The PoseBusters input modifications and the pocket-specified arm (route 1 above) are also
  design-level in that the ligand of interest is declared in advance from the deposited entry.

### `prospective`

**no — date-held-out but not prospective, and the model-selection step is retrospective.**

The strongest claim available is temporal hold-out, and the paper makes it correctly: the
PoseBusters model was retrained with a 2019 cutoff so that the 2021+ PoseBusters targets are
post-cutoff (p4, p5, p10), and the recent-PDB evaluation set (1 May 2022 – 12 January 2023)
postdates the 30 September 2021 training cutoff by seven months (p9). But every reference
structure already existed and was already deposited when the predictions were made and scored;
nothing was predicted before the experiment was done; there is no blind community assessment arm
(CASP15 RNA is scored retrospectively from downloaded submissions, p10: "All entrants'
predictions were downloaded from the CASP website and scored internally"). And per route 4 the
checkpoint was selected against the evaluation set. So: **retrospective throughout, with a
well-executed date-based hold-out for the ligand arm and a homology-based hold-out for the
polymer arms.**

### `state_metric`

**RMSD-to-reference + visual only** — dual, and the split is informative.

- For *accuracy*, everywhere: continuous and thresholded distance measures against the reference —
  pocket-aligned ligand r.m.s.d. with a 2 Å threshold, DockQ with 0.23 and 0.8 thresholds, LDDT,
  iLDDT, GDT, TM-score (p2 caption, p9 Methods, p21 Extended Data Table 1). Thresholds are stated
  and are inherited from the cited sources (DockQ ref. 40, PoseBusters convention ref. 30); the
  paper also reports the mapping it uses between them: "DockQ categories correct (>0.23), and
  very high accuracy (>0.8) correspond to iLDDTs of 23.6 and 77.6 respectively" (p20).
- For *conformational state* — the one place a state is called, Fig. 5c — the call is **visual,
  with no operationalised predicate**. The caption offers a geometric cue but no number and no
  threshold: "The dashed lines indicate the distance between the N-terminal Lon protease-like and
  C-terminal thalidomide-binding domain" (p7). No open/closed cut-off, no measured distance, no
  count of how many of the 10 apo samples fell on each side. The claim "AF3 exclusively predicts
  the closed state for both holo and apo systems" (p6) rests on inspection of a render.

That second half is a rigour defect *in the conformational claim only*, and it is why
`visual-metric` is tagged. It is not a criticism of the paper's accuracy machinery, which is
quantitative throughout.

### `metric_saturation`

**Numeric saturation is present but marginal, in two places; it does not threaten the headline
numbers.** (Axis-truncation and rendering defects are recorded in `hides` in section F, not here.)

1. **Extended Data Fig. 4f (p15), PoseBusters V2 validity checks:** of 18 checks, roughly a dozen
   sit at or essentially at **100% for both DiffDock and AF3** (file loads, sanitization,
   molecular formula, bonds, bond lengths, bond angles, planar aromatic rings, planar double
   bonds, internal steric clash, volume overlap with inorganic cofactors). A bounded percentage
   metric at its ceiling for both arms carries no information; the informative checks are the
   handful that do not saturate (tetrahedral chirality, minimum protein–ligand distance where
   DiffDock is ~30% and AF3 ~100%, minimum distance to organic cofactors, volume overlap with
   protein/organic cofactors).
2. **Fig. 4a top-left (p6):** in the highest ipTM band (0.95+, n = 229) the DockQ box sits at
   ~0.93 with whiskers touching the 1.0 ceiling, so the calibration curve necessarily flattens in
   the top bin. Same effect in the ligand panel, where the 0.95+ bin is ~43% in the 0–0.5 Å band
   and the stacked bar is bounded at 100%. This is a property of bounded metrics, not a defect,
   but it means the top confidence bin cannot demonstrate further discrimination.
3. **Protein monomer LDDT is close to ceiling and the AF3-vs-AF-M2.3 gap is correspondingly
   small:** 86.9 vs 85.5 (p21) — statistically significant (P = 1.7 × 10⁻³⁴, p5) and practically
   ~1.4 LDDT. Worth recording because a corpus quoting "AF3 beats AF-Multimer on monomers" should
   quote the size of the gap.

No metric floors. No arm reports 0% or 100% for AF3 itself.

### `directional_control`

**NOT APPLICABLE — AF3 offers no handle for instructing which conformational state to produce,
and the paper does not claim one.** This is recorded as a negative rather than forced into a
value, because the absence is itself the finding this corpus needs.

What handles exist, and what each does:

- **Random seeds / diffusion samples** — sample only, do not direct: "The model can be run with
  different random seeds to generate alternative results" (p9), but "multiple random seeds for
  either the diffusion head or the overall network do not produce an approximation of the
  solution ensemble" (p6). More seeds buy accuracy on antibodies (Fig. 5a, p7), not state
  coverage.
- **Ligand identity / holo vs apo input** — the obvious candidate handle, and the paper reports
  it **failing**: "AF3 exclusively predicts the closed state for both holo and apo systems"
  (p6, Fig. 5c). Specifying the ligand did not move the conformation.
- **Pocket conditioning** (the fine-tuned pocket-specified variant, p10) directs *where the
  ligand binds*, not which protein conformation is produced.
- **Partner chains** are inputs to a joint prediction, but no arm tests whether adding or removing
  a partner switches a state; there is no G-protein-mimetic, nanobody or peptide state-handle
  experiment in the paper.
- **Templates** are searched and date-filtered, never state-selected (p9).

The paper's own forward-looking sentence is the closest it comes, and it points at other people's
methods, p6: "Many methods have been developed, particularly around MSA resampling, that assist
in generating diversity from previous AlphaFold models43–45 and may also assist in multistate
prediction with AF3." (refs 43–45 = Wayment-Steele 2024, del Alamo 2022, Heo & Feig 2022 — all in
this corpus.)

### `anti_memorization_design`

**PRESENT AND STRONG — this is the field the corpus needs from this paper. Two different cutoffs,
a retrained model, a date-bounded evaluation window, and a 40%-sequence-identity homology
filter.** Everything below is verbatim with pages.

**(i) The standard training cutoff — 30 September 2021.** Methods, "Training regime", p9:

> "No structural data used during training were released after 30 September 2021 and, for the
> model used in PoseBusters evaluations, we filtered out PDB32 structures released after
> 30 September 2021."

*(The second date in that sentence contradicts the rest of the paper and is treated as a typo —
see the contradiction note at the head of this file and `unresolved`. The first date, 30 September
2021, is corroborated three times over and is the authoritative standard cutoff.)*

Corroboration, main text p4:

> "As our standard training cut-off date is in 2021, we trained a separate AF3 model with an
> earlier training-set cutoff (Methods)."

Corroboration, Methods "Inference regime", p9:

> "No inference time templates or reference ligand position features were released after
> 30 September 2021, and in the case of PoseBusters evaluation, an earlier cut-off date of
> 30 September 2019 was used."

Corroboration, Methods "PoseBusters", p10:

> "While other analyses used an AlphaFold model trained on PDB data released before a cut-off of
> 30 September 2021, our PoseBusters analysis was conducted on a model (with identical
> architecture and similar training schedule) differing only in the use of an earlier
> 30 September 2019 cut-off. This analysis therefore did not include training data, inference
> time templates or 'ref_pos' features released after this date."

**So: standard AF3 = 30 September 2021. PoseBusters AF3 = 30 September 2019, a separately trained
model, not a filtered evaluation of the 2021 model.** Note that the cutoff bounds training data,
inference-time templates *and* reference-conformer ('ref_pos') features alike.

Main text p5, on why the second model exists:

> "PoseBusters analysis was performed using a training cut-off of 30 September 2019 for AF3 to
> ensure that the model was not trained on any PoseBusters structures."

and the reason that is necessary, p4:

> "Performance on protein–ligand interfaces was evaluated on the PoseBusters benchmark set, which
> is composed of 428 protein–ligand structures **released to the PDB in 2021 or later**."

**(ii) How the PDB snapshot was defined.** Data availability, p10:

> "Structures from the PDB were used for training and as templates
> (https://files.wwpdb.org/pub/pdb/data/assemblies/mmCIF/; sequence clusters are available at
> https://cdn.rcsb.org/resources/sequence/clusters/clusters-by-entity-40.txt; sequence data are
> available at https://files.wwpdb.org/pub/pdb/derived_data/). **Training used a version of the
> PDB downloaded 12 January 2023, while template search used a version downloaded 28 September
> 2022.** We also used the Chemical Components Dictionary downloaded on 19 October 2023
> (https://www.wwpdb.org/data/ccd)."

So there are **three distinct PDB dates and they must not be conflated**: the *download* snapshot
(12 January 2023) bounds what could physically be in the corpus; the *release-date cutoff*
(30 September 2021, or 30 September 2019 for the PoseBusters model) bounds what was actually used
for training; and the *template-search* snapshot (28 September 2022) bounds the template
database, itself further filtered by the same release-date cutoffs at inference (p9). Assemblies
were taken as mmCIF assemblies, not asymmetric units, for training; PoseBusters inference used
"the asymmetric unit from specified PDBs" (p10).

**(iii) The evaluation-set cutoff — a date window, not a single date.** Methods, "Recent PDB
evaluation set", p9:

> "General model evaluation was performed on our recent PDB set consisting of **8,856 PDB
> complexes released between 1 May 2022 and 12 January 2023**. The set contains almost all PDB
> complexes released during that period that are less than 5,120 model tokens in size
> (Supplementary Methods 6.1)."

The window opens **seven months after** the 30 September 2021 training cutoff, leaving a buffer
rather than butting up against it; it closes on the same day as the training PDB download
(12 January 2023). **This is the evaluation set behind every non-PoseBusters number in the
paper** — protein–protein, protein–antibody, monomers, protein–RNA, protein–dsDNA, RNA-only,
DNA-only, bonded ligands, glycosylation and modified residues.

**(iv) Filtering by similarity.** Methods, p9, verbatim and in full because other papers in this
corpus define their held-out sets against exactly this rule:

> "The recent PDB set is filtered to a low homology subset (Supplementary Methods 6.1) for some
> results where stated. **Homology is defined as sequence identity to sequences in the training
> set and is measured by template search (Supplementary Methods 2.4). Individual polymer chains
> in evaluation complexes are filtered out if the maximum sequence identity to chains in the
> training set is greater than 40%, where sequence identity is the percentage of residues in the
> evaluation set chain that are identical to the training set chain. Individual peptide chains
> (protein chains with less than 16 residues) are always filtered out. For polymer–polymer
> interfaces, if both polymers have greater than 40% sequence identity to two chains in the same
> complex in the training set, then the interface is filtered out. For interfaces to a peptide,
> the interface is filtered out if the non-peptide entity has greater than 40% sequence identity
> to any chain in the training set.**"

Further restrictions layered on the low-homology set for particular comparisons (all p9): "<20
protein chains and <2,560 tokens" for the AF-M 2.3 protein comparison and the MSA-depth analysis;
"<1,536 tokens" for the seeds analysis (p18); "<1,000 total residues and nucleotides" for the
RF2NA comparison (p9–p10, imposed because "RoseTTAFold2NA is validated only on structures below
1,000 residues", p5); and for antibodies, "complexes with at most 2,560 tokens and with no
unknown amino acids in the PDB… That leaves 71 antibody–antigen complexes, containing 166
antibody–antigen interfaces spanning 65 interface clusters".

**(v) Where the filter is NOT applied — read this before quoting any number as homology-controlled.**

- Covalent modifications, p5: "As with the PoseBusters set, **the bonded ligands and glycosylation
  datasets are not filtered by homology to the training dataset.** Filtering on the basis of the
  bound polymer chain homology (using polymer template similarity < 40) yielded only five
  clusters for bonded ligands and seven clusters for glycosylation." So the 78.5% bonded-ligand
  and 72.1%/46.0%/42.4% glycosylation numbers are *not* homology-filtered, and the authors say
  the filtered version would be underpowered (n = 5 and n = 7 clusters).
- Confidence calibration, p5: "Our confidence analysis is performed on the recent PDB evaluation
  set, **with no homology filtering and including peptides.**" Every number in Fig. 4 and Extended
  Data Fig. 8 is therefore un-filtered.
- PoseBusters itself is not homology-filtered — instead the whole model was retrained with an
  earlier cutoff, which is the stronger control (p10), and homology is analysed post hoc as a
  stratification (Extended Data Fig. 4c; see `anti_memorization_control`).
- Modified residues *are* filtered: "The modified residues dataset is filtered similarly to our
  other polymer test sets: it contains only modified residues in polymer chains with low homology
  to the training set" (p5).
- CAID 2 disorder proteins are stated to be low-homology: "proteins in the CAID 2 set, which are
  also low homology to the AF3 training set" (p12).

**One-line answer for the corpus:** *AlphaFold 3's standard training cutoff is 30 September 2021
(PDB snapshot downloaded 12 January 2023; template-search snapshot 28 September 2022); a
separately trained model with a 30 September 2019 cutoff was used for all PoseBusters results;
the general evaluation set is 8,856 PDB complexes released 1 May 2022 – 12 January 2023, filtered
where stated to ≤40% sequence identity to any training chain, with peptides (<16 residues) always
excluded.*

### `anti_memorization_control`

**RUN AND ANALYSED — genuinely, in three separate ways. Not merely a held-out set that exists.**
This is a stronger answer than most papers in this corpus can give.

1. **A retrained earlier-cutoff model.** The PoseBusters arm does not filter an existing model's
   test set; it uses "a model (with identical architecture and similar training schedule)
   differing only in the use of an earlier 30 September 2019 cut-off" (p10). Retraining to
   guarantee the benchmark is post-cutoff is the strongest form of this control, and the
   comparison it enables is the headline 76.4% (V1) / 80.5% (V2).
2. **Explicit homology stratification of the result — Extended Data Fig. 4c (p15).** PoseBusters
   V2 success for AF3 2019, split by maximum sequence identity to training-set proteins:
   **(0, 30] n = 38 ≈ 89%; (30, 95] n = 83 ≈ 82%; (95, 100] n = 187 ≈ 78%** (bar heights read
   from the rendered panel; the numeric values are not printed, and the error bars on the n = 38
   bin are wide). Caption: "c, PoseBusters V2 results of AF3 2019 on targets with low, moderate,
   and high protein sequence homology (integer ranges indicate maximum sequence identity with
   proteins in the training set)". **The trend runs the opposite way to memorisation** — the
   lowest-homology bin is the most accurate — which is the single most useful anti-memorization
   datapoint in the paper. Not `UNPOWERED`: the smallest bin is n = 38, above the ~10 threshold,
   though the CIs are visibly wide and the bins are not equal in size.
3. **A ligand-frequency control — Extended Data Fig. 4d (p15).** PoseBusters V2 split by whether
   the ligand is a "common natural" ligand (occurring >100 times in the PDB): common natural
   n = 50, **92.0%** RMSD < 2 Å (82.0% also PB-valid); others n = 258, **78.3%** (71.3% PB-valid).
   A ~14-point gap in favour of frequently-seen ligands. This is the one control that *does*
   show a familiarity effect, and a corpus arguing about ligand memorisation should cite it.
4. **A distillation ablation that doubles as a hallucination control — Extended Data Fig. 1
   (p12).** "AlphaFold 3 trained without the disordered protein PDB cross distillation set" is run
   as a third arm on CAID 2 (n = 151 proteins, 46,093 residues): disorder-detection ROC AUC by
   RASA is **0.95 for AF3, 0.94 for AF-M 2.3, and 0.67 for AF3 without cross-distillation**
   (pLDDT-based: 0.91 / 0.93 / 0.89). The ablation confirms the mechanism claimed on p4.

**Caveats that belong with the answer:** the confidence-calibration analysis (Fig. 4, Extended
Data Fig. 8) and the bonded-ligand/glycosylation arms carry **no homology control at all** (p5,
quoted above), and no control arm anywhere addresses *conformational* memorisation — there is no
test of whether AF3 reproduces the deposited state because it has seen it. Fig. 5c is the closest,
and it is n = 1 with a visual read-out.

### `controls_run`

Every control arm actually run and analysed, and what each rules out.

| control | what it rules out | page |
|---|---|---|
| Separate AF3 model retrained with a 30 Sep 2019 cutoff for all PoseBusters results | Training on the PoseBusters targets themselves (all released 2021+) | p4, p5, p10 |
| PoseBusters V2 stratified by max sequence identity to training proteins ((0,30] n=38 / (30,95] n=83 / (95,100] n=187) | That accuracy is driven by sequence similarity to training; trend runs opposite to memorisation | p15 (ED Fig. 4c) |
| PoseBusters V2 split by "common natural" ligand (>100 PDB occurrences) vs others (92.0% n=50 vs 78.3% n=258) | Nothing — this one *shows* a familiarity effect on frequently-deposited ligands | p15 (ED Fig. 4d) |
| ≤40% sequence-identity low-homology filter on evaluation chains, plus an interface-level variant and unconditional removal of peptides (<16 residues) | Trivially memorised chains and interfaces in the protein, antibody, monomer, nucleic-acid and modified-residue arms | p9 |
| PoseBusters V1 (Aug 2023) vs V2 (Nov 2023, crystal contacts removed) reported side by side | That the ligand result is an artefact of crystal-contact-mediated poses | p5, p15, p21 |
| PoseBusters physical-validity checks (PB-valid; 18 individual checks vs DiffDock) | That low RMSD is being achieved with chemically or sterically invalid poses | p15 (ED Fig. 4e,f) |
| AF3 trained *without* the disordered-protein cross-distillation set, evaluated on CAID 2 (RASA AUC 0.95 → 0.67) | That cross-distillation from AF-M 2.3 is not what suppresses hallucination in disordered regions | p12 (ED Fig. 1) |
| AF3 with vs without modelling phosphorylation (parent residue substituted), n = 76 clusters, P = 1.6 × 10⁻⁴ | That modelling the modification is unnecessary for backbone accuracy | p17 (ED Fig. 6a) |
| Blind AF3 vs pocket-specified fine-tuned AF3 (76.4% → 90.2% V1; 80.5% → 93.2% V2) | How much of the docking-baseline gap is attributable to the pocket information those baselines receive | p10, p15 (ED Fig. 4a), p21 |
| Seeds ablation, 1 → 1,000 seeds per target on antibodies (P = 2.0 × 10⁻⁵ correct, P = 0.009 very high accuracy) | That antibody accuracy has already converged at the standard 5-seed budget | p7 (Fig. 5a) |
| 1 vs 5 diffusion samples per seed, antibodies | That the seed gain is really a diffusion-sample gain: "Using only one diffusion sample per model seed … does not change the results significantly" | p7 |
| Seeds ablation across seven molecule-type classes (1 → 30 seeds) | That the antibody seed effect generalises — it does not: "This large improvement with many seeds is not observed in general for other classes of molecules" | p7, p18 (ED Fig. 7b) |
| RF2NA re-run in-house "with the same MSAs as those that were used for AF3 predictions" | That the nucleic-acid margin comes from a better MSA rather than a better model | p9 |
| RF2NA comparison restricted to <1,000 residues/nucleotides and to single nucleic-acid types | Penalising the baseline outside its validated regime | p5, p9–p10 |
| MSA-depth (Neff) dependence of AF3 vs AF-M 2.3, using AF3's MSA depth for both | That AF3's MSA de-emphasis has silently changed its shallow-MSA behaviour — it has not: "AF3 has a very similar dependence on MSA depth to AlphaFold-Multimer v.2.3" | p5, p18 (ED Fig. 7a) |
| DockQ vs iLDDT correlation across 4,182 clusters, Huber fit, with translated thresholds (0.23 → 23.6; 0.8 → 77.6) | That iLDDT results are not comparable with the DockQ literature | p9, p20 (ED Fig. 9) |
| Chirality penalty and clash penalty added to the ranking formula, with the residual failure rate reported (4.4% chirality violations remain) | An unqualified claim that ranking fixed the stereochemistry problem — the authors report that it does not | p5, p7 |
| Confidence-vs-accuracy binning across ipTM and pLDDT bands for protein, nucleic acid, ligand, ion, bonded-ligand and bonded-glycan interfaces | That the confidence heads are uncalibrated | p6 (Fig. 4a), p19 (ED Fig. 8) |
| **NOT run:** any conformational control — no second-state arm, no apo/holo survey, no ensemble comparison against NMR/MD/cryo-EM heterogeneity | — | (absence; limitations section p6) |
| **NOT run:** homology filtering for the confidence analysis and for bonded ligands/glycosylation | — | p5 |

### `confidence_as_discriminator`

**Confidence is validated as an accuracy predictor, and is used everywhere as the *sample
selector*. It is never validated — or even tested — as a discriminator of conformational
correctness.** Both halves matter to the corpus and both are quoted.

**What the paper claims and shows.** p5:

> "As with AF2, AF3 confidence measures are well calibrated with accuracy. Our confidence analysis
> is performed on the recent PDB evaluation set, with no homology filtering and including
> peptides."

The measures themselves, p4:

> "We also developed confidence measures that predict the atom-level and pairwise errors in our
> final structures… The confidence head uses the pairwise representation to predict a modified
> local distance difference test (pLDDT) and a predicted aligned error (PAE) matrix as in AF2, as
> well as a distance error matrix (PDE), which is the error in the distance matrix of the
> predicted structure as compared to the true structure."

Fig. 4 (p6) is the evidence: chain-pair ipTM against DockQ (protein–protein), against iLDDT
(nucleic–protein) and against banded pocket r.m.s.d. (ligand–protein); and chain pLDDT against a
bespoke LDDT_to_polymer for protein, nucleic acid and ligand entities. All bands are monotone.
Extended Data Fig. 8 (p19) repeats it for ions, bonded ligands and bonded glycans. The metric used
for the pLDDT panels is deliberately matched to the training target: "For confidence calibration
assessment, we use a bespoke LDDT (LDDT_to_polymer) metric… This is closely related to how the
confidence prediction is trained" (p9) — a self-consistent choice the paper is open about.

**What confidence is used for.** Sample ranking, throughout: "All scores are reported from the top
confidence-ranked sample out of five model seeds" (p2); the four-way ranking scheme (global
pTM/ipTM mix plus clash and disorder terms; chain pTM; interface ipTM; per-residue pLDDT) is on
p9; Fig. 5a ranks antibody samples by protein–protein ipTM over up to 1,000 seeds (p7); Extended
Data Fig. 7b ranks by confidence across molecule classes (p18). **Confidence is the only selection
signal AF3 has**, which is why the seeds result matters: more samples help only to the extent that
ranking can find the good one.

**What confidence does NOT do, per the paper itself.**

- It does not discriminate conformational states. There is no analysis anywhere relating
  confidence to which conformation was produced. In the one conformational test, all 10 apo
  samples were closed (Fig. 5c, p7), so confidence was never asked to choose between states — the
  ensemble offered it only one.
- It flags hallucinated regions, but imperfectly and in a way that is easy to miss. p5–p6:

> "Although hallucinated regions are typically marked as very low confidence, they can lack the
> distinctive ribbon-like appearance that AF2 produces in disordered regions."

  i.e. pLDDT still fires, but the *visual* cue a human would use is gone. Quantified on p12:
  disorder-prediction AUC on CAID 2 is 0.91 for AF3 pLDDT versus 0.95 for AF3 RASA — RASA (a
  geometric property of the prediction) is the better disorder signal, not pLDDT.
- It does not catch stereochemical failure by itself: the chirality and clash penalties had to be
  added to the ranking formula as separate terms, and "we still observe a chirality violation rate
  of 4.4%" and clashes that ranking "reduces … but does not eliminate" (p5).
- Its calibration is demonstrated **without homology filtering** (p5, quoted above), so calibration
  on chains similar to training data is not separated from calibration on novel ones.
- No confidence threshold is proposed or validated for any decision. Bands are descriptive
  (0–0.4, 0.4–0.6, 0.6–0.8, 0.8–0.95, 0.95+ for ipTM; 0–50, 50–70, 70–90, 90+ for pLDDT), not
  operational.

**Bottom line for the corpus:** AF3's confidence metrics measure *expected coordinate error
against the single structure the model is trying to produce*. They are not, and are not claimed
to be, a measure of whether the produced conformational state is the right one, and this paper
provides no evidence either way on that question.

## D. Claims

### `central_conclusion`

A single diffusion-based model, trained on the PDB with a de-emphasised MSA trunk and a
coordinate-space diffusion head replacing AF2's frame-based structure module, predicts the joint
structure of complexes spanning proteins, nucleic acids, ligands, ions and modified residues, and
beats specialist tools in every category it was tested in except human-expert-aided CASP15 RNA
(protein–ligand vs docking, protein–nucleic vs RoseTTAFold2NA, antibody–antigen and protein–protein
vs AlphaFold-Multimer v.2.3). The authors also state plainly that the model predicts static,
single conformational states, that ligand specification does not reliably select the right state,
that seeds do not approximate a solution ensemble, and that the generative architecture introduces
hallucination in disordered regions which they suppress by distilling AF-M 2.3 predictions into
the training data.

### `necessity_claims`

Verbatim, with pages. Statements that X is required/necessary/essential, or that Y cannot be done.

- p1 — on the prior art's incapacity:
  > "Almost all of these methods are also highly specialized to particular interaction types and
  > **cannot predict** the structure of general biomolecular complexes containing many types of
  > entities."
- p1 — the possibility claim the paper is built to establish:
  > "Together, these results show that high-accuracy modelling across biomolecular space **is
  > possible** within a single unified deep-learning framework."
- p4 — architectural non-necessity:
  > "we find that **no invariance or equivariance with respect to global rotations and translation
  > of the molecule are required** in the architecture and we therefore omit them to simplify the
  > machine learning architecture."
- p4 — a method-level impossibility that forced the rollout design:
  > "In AF2, this was done directly by regressing the error in the output of the structure module
  > during training. However, **this procedure is not applicable to diffusion training**, as only a
  > single step of the diffusion is trained instead of a full-structure generation (Fig. 2c)."
- p6 — the conformational impossibility, and the single most load-bearing sentence in this note:
  > "This limitation persists for AF3, in which multiple random seeds for either the diffusion head
  > or the overall network **do not produce an approximation of the solution ensemble**."
- p6–p7 — necessity of large sampling budgets:
  > "To obtain the highest accuracy, **it may be necessary to generate a large number of
  > predictions and rank them**, which incurs an extra computational cost."
- p7 — necessity of *seeds* specifically, not diffusion samples:
  > "Using only one diffusion sample per model seed for the AF3 predictions rather than five (not
  > illustrated) does not change the results significantly, indicating that **running more model
  > seeds is necessary for antibody score improvements**, rather than just more diffusion samples."
- p8 — the negative-necessity claim about evolutionary information:
  > "We also demonstrate that **the lack of cross-entity evolutionary information is not a
  > substantial blocker** to progress in predicting these interactions and, moreover, substantial
  > improvement in antibody results suggests AlphaFold-derived methods are able to model the
  > chemistry and physics of classes of molecular interactions **without dependence on MSAs**."
- p10 — absence of a comparator:
  > "**No system was publicly available at time of writing** for baseline comparisons on data with
  > arbitrary combinations of biomolecular types in PDB."
- p5 — a bounded failure claim about clashes:
  > "Penalizing clashes during ranking (Supplementary Methods 5.9.3) reduces the occurrence of
  > this failure mode **but does not eliminate them**. **Almost all remaining clashes occur for
  > protein–nucleic complexes with both greater than 100 nucleotides and greater than 2,000
  > residues in total.**"

### `novelty_claims`

Verbatim, with pages. **Note what is absent: the paper never uses the words "first",
"unprecedented" or "for the first time" about its own contribution, and it explicitly concedes a
concurrent generalist method.** The claims are comparative-superiority and capability claims, not
priority claims — which is itself worth knowing for anyone weighing a priority argument.

- p1, abstract:
  > "Here we describe our AlphaFold 3 model with a substantially updated diffusion-based
  > architecture that is capable of predicting the joint structure of complexes including proteins,
  > nucleic acids, small molecules, ions and modified residues. The new AlphaFold model
  > demonstrates **substantially improved accuracy over many previous specialized tools**: far
  > greater accuracy for protein–ligand interactions compared with state-of-the-art docking tools,
  > much higher accuracy for protein–nucleic acid interactions compared with nucleic-acid-specific
  > predictors and substantially higher antibody–antigen prediction accuracy compared with
  > AlphaFold-Multimer v.2.37,8."
- p1, main text:
  > "Here we present AlphaFold 3 (AF3)—a model that is capable of high-accuracy prediction of
  > complexes containing **nearly all molecular types present in the Protein Data Bank32 (PDB)**
  > (Fig. 1a,b). **In all but one category, it achieves a substantially higher performance than
  > strong methods that specialize in just the given task** (Fig. 1c and Extended Data Table 1),
  > including higher accuracy at protein structure and the structure of protein–protein
  > interactions."
- p1 — the explicit priority hedge:
  > "A wide range of predictors for various specific interaction types has been developed16–28, **as
  > well as one generalist method developed concurrently with the present work29**, but the accuracy
  > of such deep-learning attempts has been mixed and often below that of physics-inspired
  > methods30,31." (ref. 29 = RoseTTAFold All-Atom, Krishna *et al.*, *Science* 2024.)
- p7, Discussion:
  > "The AF3 model takes a large step in this direction, **demonstrating that it is possible** to
  > accurately predict the structure of a wide range of biomolecular systems in a unified
  > framework."
- p8, Discussion:
  > "Finally, the large improvement in protein–ligand structure prediction shows that **it is
  > possible to handle the wide diversity of chemical space within a general deep-learning
  > framework and without resorting to an artificial separation between protein structure
  > prediction and ligand docking**."
- p8 — a claim about what the results imply for the field:
  > "the performance of AF3 shows that developing the right deep-learning frameworks can
  > **massively reduce the amount of data required** to obtain biologically relevant performance on
  > these tasks and amplify the impact of the data already collected."
- The only literal use of "novel" in the paper is about a *target*, not the method — p4, Fig. 3
  caption: "e, (5S,6S)-O7-sulfo DADH bound to the AziU3/U2 complex **with a novel fold** (PDB 7WUX;
  ligand r.m.s.d., 1.92 Å)." Recorded so a keyword search does not misread it as a priority claim.

### `stated_limits`

The authors devote a titled section to this ("Model limitations", p5–p7) plus scattered
concessions. Reproduced at length because this section is one of the two reasons the note exists.

**The framing sentence, p5:**
> "We note model limitations of AF3 with respect to **stereochemistry, hallucinations, dynamics and
> accuracy for certain targets**."

**On conformational states and dynamics — the passage the corpus needs, p6, in full and in order:**

> "A key limitation of protein structure prediction models is that they typically predict static
> structures as seen in the PDB, not the dynamical behaviour of biomolecular systems in solution.
> This limitation persists for AF3, in which multiple random seeds for either the diffusion head or
> the overall network do not produce an approximation of the solution ensemble."

> "In some cases, the modelled conformational state may not be correct or comprehensive given the
> specified ligands and other inputs. For example, E3 ubiquitin ligases natively adopt an open
> conformation in an apo state and have been observed only in a closed state when bound to ligands,
> but AF3 exclusively predicts the closed state for both holo and apo systems42 (Fig. 5c). Many
> methods have been developed, particularly around MSA resampling, that assist in generating
> diversity from previous AlphaFold models43–45 and may also assist in multistate prediction with
> AF3."

Figure 5c caption, p7:
> "c, Conformation coverage is limited. Ground-truth structures (grey) of cereblon in open (apo,
> PDB: 8CVP; left) and closed (holo mezigdomide-bound, PDB: 8D7U; right) conformations. Predictions
> (blue) of both apo (with 10 overlaid samples) and holo structures are in the closed conformation.
> The dashed lines indicate the distance between the N-terminal Lon protease-like and C-terminal
> thalidomide-binding domain."

Three things a citing sentence should not blur: (a) the ensemble-inadequacy claim is about
**seeds and diffusion samples**, made generally; (b) the ligand-conditioning failure is
**n = 1 system**, called visually; (c) the authors themselves point at MSA resampling (refs 43–45)
as the likely remedy, i.e. they do not claim the limitation is intrinsic.

**On hallucination and disorder, p4 (cause and mitigation):**
> "The biggest issue is that generative models are prone to hallucination35, whereby the model may
> invent plausible-looking structure even in unstructured regions. To counteract this effect, we use
> a cross-distillation method in which we enrich the training data with structures predicted by
> AlphaFold-Multimer (v.2.3)7,8. In these structures, unstructured regions are typically represented
> by long extended loops instead of compact structures, and training on them 'teaches' AF3 to mimic
> this behaviour. This cross-distillation greatly reduced the hallucination behaviour of AF3
> (Extended Data Fig. 1 for disorder prediction results on the CAID 236 benchmark set)."

**and p5–p6 (residual problem):**
> "We note that the switch from the non-generative AF2 model to the diffusion-based AF3 model
> introduces the challenge of spurious structural order (hallucinations) in disordered regions
> (Fig. 5d and Extended Data Fig. 1). Although hallucinated regions are typically marked as very low
> confidence, they can lack the distinctive ribbon-like appearance that AF2 produces in disordered
> regions. To encourage ribbon-like predictions in AF3, we use distillation training from AF2
> predictions, and we add a ranking term to encourage results with more solvent accessible surface
> area36."

Fig. 5d caption, p7: "d, A nuclear pore complex with **1,854 unresolved residues** (PDB: 7F60). The
ground truth (left) and predictions from AlphaFold-Multimer v.2.3 (middle) and AF3 (right) are
shown."

**On stereochemistry, p5:**
> "On stereochemistry, we note two main classes of violations. The first is that **the model outputs
> do not always respect chirality** (Fig. 5b), despite the model receiving reference structures with
> correct chirality as input features. To address this in the PoseBusters benchmark, we included a
> penalty for chirality violation in our ranking formula for model predictions. **Despite this, we
> still observe a chirality violation rate of 4.4% in the benchmark.** The second class of
> stereochemical violations is a tendency of the model to occasionally produce overlapping (clashing)
> atoms in the predictions. **This sometimes manifests as extreme violations in homomers in which
> entire chains have been observed to overlap** (Fig. 5e)."

**On hard targets and cost, p6–p7:**
> "Despite the large advance in modelling accuracy in AF3, there are still many targets for which
> accurate modelling can be challenging. To obtain the highest accuracy, it may be necessary to
> generate a large number of predictions and rank them, which incurs an extra computational cost. A
> class of targets in which we observe this effect strongly is antibody–antigen complexes, similar to
> other recent work46. Figure 5a shows that, for AF3, top-ranked predictions keep improving with more
> model seeds, even at as many as 1,000."

**On RNA, p5:**
> "**We did not reach the performance of the best human-expert-aided CASP15 submission
> AIchemy_RNA239** (Fig. 1c (centre left)). Owing to limited dataset sizes, we do not report
> significance test statistics here."

**On MSA depth, p5:**
> "AF3 has a very similar dependence on MSA depth to AlphaFold-Multimer v.2.3; **proteins with
> shallow MSAs are predicted with lower accuracy**."

**On evaluation coverage, p5 and p10:**
> "the bonded ligands and glycosylation datasets are not filtered by homology to the training
> dataset" (p5); "Our confidence analysis is performed on the recent PDB evaluation set, with no
> homology filtering and including peptides" (p5); "Note we do not compare directly to RoseTTAFold
> All-Atom, but benchmarks indicate that RoseTTAFold All-Atom is slightly less accurate than
> RoseTTAFold2NA for nucleic acid predictions" (p5); "No system was publicly available at time of
> writing for baseline comparisons on data with arbitrary combinations of biomolecular types in PDB"
> (p10).

**On availability, p10:** "AlphaFold 3 will be available as a non-commercial usage only server…
with restrictions on allowed ligands and covalent modifications… **Code is not provided.**"

### `stance`

**`background` + `precedent`. Provisional — the user's call.**

- **`background`**: this is the model, the training/evaluation cutoff and the accuracy baseline
  that the rest of the corpus is defined against. Papers in this corpus construct post-AF3-cutoff
  held-out sets, run AF3 as a backbone, or measure against its PoseBusters/DockQ numbers. Nothing
  here competes with a conformational-states paper; it supplies the substrate.
- **`precedent`**: Fig. 5c and the p6 limitations passage are the authors' own, first-party
  documentation of the exact phenomenon a state-prediction paper exists to address — that AF3
  collapses onto a single conformational basin regardless of ligand, and that seeds do not
  approximate an ensemble. Citing DeepMind's own admission is stronger than citing a third party's
  measurement of it. It is a precedent *observation*, at n = 1 with a visual read-out, which leaves
  the systematic version of the claim open.
- Explicitly **not `threat`**: the paper claims nothing about multistate prediction and in fact
  points at MSA resampling (refs 43–45) as the remedy, ceding the ground.
- Explicitly **not `contrast` on rigour**: apart from the route-4 checkpoint-selection issue and
  the unfiltered confidence analysis, the anti-memorization design here is better than most of the
  corpus, not worse.

## E. Quantitative comparators

### `metrics_reported`

One row per metric. Values from Extended Data Table 1 (p21) unless another page is given; "n"
means structures for ligands and nucleic acids, clusters for covalent modifications and proteins
(p21 caption), targets for PoseBusters (p2 caption). 95% CIs are from Extended Data Table 1.

| metric | value | units | measured against | page |
|---|---|---|---|---|
| PoseBusters V1 success, AF3 (2019 cutoff), blind | **76.4** (95% CI 72.1–80.3) | % of targets with pocket-aligned ligand r.m.s.d. < 2 Å | PoseBusters V1 (Aug 2023 release), n = 428 targets; vs RoseTTAFold All-Atom 42.0 (n = 427) and AutoDock Vina 52.3; Fisher's exact P = 2.27 × 10⁻¹³ vs Vina, P = 4.45 × 10⁻²⁵ vs RFAA | p2, p4, p5, p21 |
| PoseBusters V1 success, AF3 pocket-specified (privileged) | **90.2** (87.0–92.8) | % r.m.s.d. < 2 Å | PoseBusters V1, n = 428; vs Uni-Mol Docking V2 77.6, Vina 52.3, Gold 51.2 | p10, p15, p21 |
| PoseBusters V2 success, AF3 (2019 cutoff), blind | **80.5** (75.6–84.8) | % r.m.s.d. < 2 Å | PoseBusters V2 (Nov 2023, crystal contacts removed), n = 308 targets; vs Vina 59.7; Fisher's exact P = 2.3 × 10⁻⁸ | p15, p21 |
| PoseBusters V2 success, AF3 pocket-specified (privileged) | **93.2** (89.8–95.7) | % r.m.s.d. < 2 Å | PoseBusters V2, n = 308; vs Vina 59.7, Gold 58.1 | p15, p21 |
| PoseBusters V2 success **and** PB-valid, AF3 2019 | **73.1** | % r.m.s.d. < 2 Å and passing all PoseBusters validity checks | PoseBusters V2, n = 308; vs DiffDock 12.7, Vina 58.1 | p15 |
| PoseBusters V2, homology-stratified success, AF3 2019 | **≈89 / ≈82 / ≈78** (bar heights; exact values not printed) | % r.m.s.d. < 2 Å | Max sequence identity to training proteins (0,30] n = 38 / (30,95] n = 83 / (95,100] n = 187 | p15 (ED Fig. 4c) |
| PoseBusters V2, ligand-familiarity split, AF3 2019 | **92.0** (82.0 PB-valid) vs **78.3** (71.3 PB-valid) | % r.m.s.d. < 2 Å | "Common natural" ligands (>100 PDB occurrences) n = 50 vs others n = 258 | p15 (ED Fig. 4d) |
| Chirality violation rate, AF3 on PoseBusters | **4.4** | % of benchmark predictions, after the ranking chirality penalty | PoseBusters set | p5 |
| Protein–RNA interface accuracy, AF3 | **39.4** (28.5–51.9) | iLDDT | Recent PDB eval set, <1,000 residues, n = 25 structures; vs RoseTTAFold2NA 19.0 (15.6–23.2); Wilcoxon P = 2.57 × 10⁻³ | p2, p5, p21 |
| Protein–dsDNA interface accuracy, AF3 | **64.8** (56.4–71.7) | iLDDT | Recent PDB eval set, <1,000 residues, n = 38 structures; vs RoseTTAFold2NA 28.3 (20.7–37.5); Wilcoxon P = 2.78 × 10⁻³ | p2, p5, p21 |
| RNA-only structures, AF3 | (AF3 > RF2NA) | LDDT | Low-homology recent PDB set, n = 29 structures; paired Wilcoxon P = 1.6 × 10⁻⁷; medians ≈ 75 (AF3) vs ≈ 68 (RF2NA), read from ED Fig. 5b — **numeric values not printed** | p16 (ED Fig. 5b) |
| DNA-only structures, AF3 | (AF3 > RF2NA) | LDDT | Low-homology recent PDB set, n = 63 structures; paired two-sided Wilcoxon P = 5.2 × 10⁻¹²; medians ≈ 86 vs ≈ 64, read from ED Fig. 5b — **numeric values not printed** | p16 (ED Fig. 5b) |
| CASP15 RNA, AF3 | **47.3** (41.7–55.2) | RNA LDDT | CASP15 RNA, n = 8 targets; vs RoseTTAFold2NA 35.5, AIchemy_RNA 40.9–ish (see table), **AIchemy_RNA2 (human input) 54.5** — AF3 loses to the human-aided entrant | p5, p21 |
| Bonded ligands, AF3 | **78.5** (68.3–86.2) | % pocket r.m.s.d. < 2 Å | Recent PDB eval, high-quality experimental filter, **not homology-filtered**, n = 66 clusters | p5, p21 |
| Glycosylation, AF3, high-quality single-residue | **72.1** (53.1–85.7) | % pocket r.m.s.d. < 2 Å | Recent PDB eval, ranking_model_fit > 0.5, **not homology-filtered**, n = 28 clusters | p5, p21 |
| Glycosylation, AF3, all-quality single-residue | **46.0** (40.0–52.1) | % pocket r.m.s.d. < 2 Å | Recent PDB eval, n = 167 clusters | p5, p21 |
| Glycosylation, AF3, all-quality multi-residue glycans | **42.4** (35.4–49.3) | % pocket r.m.s.d. < 2 Å | Recent PDB eval, n = 131 clusters (p5 quotes 42.1 for the same quantity — see `unresolved`) | p5, p21 |
| Modified residues, AF3 (all) | **59.9** (52.4–67.0) | % pocket r.m.s.d. < 2 Å | Low-homology recent PDB eval, n = 154 clusters | p21 |
| Modified protein residues, AF3 | **51.0** (36.0–65.6) | % pocket r.m.s.d. < 2 Å | Low-homology recent PDB eval, n = 40 clusters | p2, p21 |
| Modified DNA residues, AF3 | **68.6** (59.0–76.9) | % pocket r.m.s.d. < 2 Å | Low-homology recent PDB eval, n = 91 clusters | p2, p21 |
| Modified RNA residues, AF3 | **40.9** (23.4–59.9) | % pocket r.m.s.d. < 2 Å | Low-homology recent PDB eval, n = 23 clusters | p2, p21 |
| **All protein–protein interfaces, AF3** | **76.6** (74.0–78.9) | % of interface clusters with DockQ > 0.23 | Low-homology recent PDB eval, <20 chains, <2,560 tokens, n = 1,064 clusters; vs AlphaFold-Multimer v.2.3 **67.5** (64.7–70.1); paired Wilcoxon P = 1.8 × 10⁻¹⁸ | p2, p5, p21 |
| **Protein–antibody interfaces, AF3** | **62.9** (51.4–73.5) | % of interface clusters with DockQ > 0.23 | Low-homology recent PDB eval, n = 65 interface clusters (71 complexes, 166 interfaces); vs AF-M 2.3 **29.6** (19.6–40.4); paired Wilcoxon P = 6.5 × 10⁻⁵; **top-ranked across 1,000 seeds for both models**, not the standard 5 | p2, p5, p21 |
| **Protein monomers, AF3** | **86.9** (86.2–87.6) | LDDT | Low-homology recent PDB eval, n = 338 clusters; vs AF-M 2.3 **85.5** (84.7–86.1); paired Wilcoxon P = 1.7 × 10⁻³⁴ | p2, p5, p21 |
| Antibody accuracy vs seeds, AF3 | 5 → 1,000 seeds improves top-ranked quality | % DockQ > 0.23 and % DockQ > 0.8 | n = 65 clusters, 1,200 seeds sampled 1,000× with replacement; Wilcoxon P = 2.0 × 10⁻⁵ (correct) and P = 0.009 (very high accuracy) | p7 |
| Disorder detection on CAID 2, AF3 | **AUC 0.95** (RASA), **0.91** (pLDDT) | ROC AUC | CAID 2, n = 151 proteins / 46,093 residues, low homology to training; vs AF-M 2.3 0.94 / 0.93 and **AF3 without cross-distillation 0.67 / 0.89** | p12 (ED Fig. 1b) |
| Phosphorylation modelled vs not, AF3 | modelled is better (P = 1.6 × 10⁻⁴) | pocket-aligned backbone accuracy | Recent PDB eval, SEP/TPO/PTR/NEP/HIP, n = 76 clusters, paired two-sided Wilcoxon | p17 (ED Fig. 6a) |
| DockQ ↔ iLDDT correspondence | DockQ 0.23 ≡ iLDDT **23.6**; DockQ 0.8 ≡ iLDDT **77.6** | threshold translation, Huber fit | 4,182 protein–protein interface clusters | p9, p20 (ED Fig. 9) |
| Training-speed landmark | intrachain metrics reach 97% of maximum by **20,000** steps; protein–protein interface LDDT only after **60,000** steps | optimizer steps | AF3 evaluation set during initial training | p4, p3 (Fig. 2d) |
| Example full-complex accuracies (showcase, not benchmark) | 7PZB LDDT 82.8 / GDT 90.1; 7PNM LDDT 83.0 / GDT 83.1; 7TQL LDDT 87.7 / GDT 86.9; 7AU2 r.m.s.d. 1.10 Å; 7U8C DockQ 0.85; 7URD 1.00 Å; 7WUX 1.92 Å; 7QIE 0.37 Å | LDDT / GDT / DockQ / ligand r.m.s.d. (Å) | Single hand-picked complexes — **not a sample**; see `oracle_leakage` route 7 | p2, p4 |

### `n_predictions`

Recorded separately rather than as one total, and the paper never states a grand total.

- **Samples per target, standard**: "Unless otherwise stated, all results are generated by
  selecting the top confidence sample from running **5 seeds of the same trained model, with 5
  diffusion samples per model seed, for a total of 25 samples** to choose from" (p9); same in the
  Fig. 1 caption (p2). PoseBusters: "**Five model seeds, each with five diffusion samples**, were
  produced per target, resulting in 25 predictions" (p10).
- **Samples per target, antibody arm**: "predictions top-ranked from **1,000 rather than the
  typical 5 seeds**" (p5); Fig. 5a "Each datapoint shows the mean over 1,000 random samples (with
  replacement) of seeds to rank over, **out of 1,200 seeds**" (p7), each seed with five diffusion
  samples (p2 caption) — so up to ~6,000 structures per antibody target were generated.
- **Samples per target, seeds sweep across molecule classes**: 1 → 30 seeds (Extended Data Fig. 7b,
  p18).
- **Samples in the conformational test**: **10** overlaid diffusion samples for apo cereblon
  (Fig. 5c, p7). The holo panel's sample count is not stated.
- **Targets**: see `n_targets` in section B — 428 / 308 PoseBusters targets; 8,856 recent-PDB
  complexes; 1,064 / 65 / 338 protein clusters; 25 / 38 / 29 / 63 nucleic-acid structures; 8
  CASP15 RNA targets; 66 / 28 / 167 / 131 / 154 modification clusters; 151 CAID 2 proteins.
- **Totals**: **NOT REPORTED.** No aggregate count of structures generated, and no compute cost or
  wall-clock figure anywhere in the article, Methods or Extended Data.
- **Training-side counts** (different quantity, recorded for completeness): "One optimizer step
  uses a mini batch of 256 input data samples and during initial training 256 × 48 = **12,288
  diffusion samples**. For fine-tuning, the number of diffusion samples is reduced to 256 × 32 =
  **8,192**" (p9); three stages, crop sizes 384 → 640 → 768 tokens (p9); ~140,000 optimizer steps
  shown on the training curve (p3, Fig. 2d).

### `comparable_to_ours`

*(Left empty by the extractor per schema v3. Populated by whoever holds `STATUS.md` and the
manuscript.)*

### `si_in_scope`

**SI NOT HELD — and it holds several things this note could otherwise pin down.** The PDF is
24 pages: article (p1–p8), Methods (p9–p11), Extended Data Figs 1–9 and Table 1 (p12–p21), Nature
Portfolio Reporting Summary (p22–p24). Cited but absent: **Supplementary Methods 1–8**
(2.2 databases, 2.4 template search, 2.5.1 training-set sampling probabilities, 2.5.2 dataset
usage, 2.8 pocket conditioning, 3.x architecture, 4.3 confidence heads, 5.2 training stages,
5.9.1/5.9.3 ranking formulas, 6.1 evaluation-set construction and the low-homology filter, 6.2/6.4
clustering and weighting, 8.1 example novelty analysis), **Supplementary Algorithms 1–31**,
**Supplementary Tables 3, 4, 5, 7, 8, 9, 10, 11, 15** (notably Table 7 = checkpoint-selection
metrics and Tables 8–11 = crystallization aids, ligand exclusion list, glycans, ions), and
**Supplementary Fig. 2**.

Consequences for this note, stated so the gaps are visible rather than looking like the paper is
silent: (a) the exact composition and weighting of the training mixture cannot be verified —
`structural_priors_used` item 7 and `oracle_leakage` route 4 rest on the main-text sentence alone;
(b) the scope of the cross-distillation set (disordered proteins only, or broader?) cannot be
resolved; (c) the precise ranking formula, including how the chirality and clash penalties are
weighted, is not checkable; (d) the operational definition of the low-homology subset beyond the
quoted 40% rule is in 6.1. **`metrics_reported` is NOT emptied** — Extended Data Table 1 (p21)
carries the full per-arm accuracy table with n and 95% CIs, which is unusually generous for a
paper of this type.

## F. Figures

One row per panel group; split on `mark` or `measure`, not on `facet`. **31 panel-group rows**
across 5 main figures, 9 Extended Data figures and 1 Extended Data table.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A-B | 2 | Two showcase AF3 predictions: a CRP/FNR-family regulator on DNA with cGMP, and a 4,665-residue glycosylated OC43 spike with neutralizing antibodies | structure render | `RENDER \| facet: showcase complex (2: 7PZB, 7PNM) \| views: 1 \| overlay: NOT REPORTED predictions on 1 reference \| axis: none` | 2 panels; vary by system, not by condition | Sample count behind each render not given; accuracy quoted in the caption (LDDT/GDT) has no distribution behind it — these are 2 hand-picked systems standing in front of a 8,856-complex evaluation set | CC BY 4.0, **no ND clause** — redrawing and adaptation permitted with attribution (licence text p8) |
| 1C | 2 | Headline accuracy bar chart: AF3 vs specialist baselines across ligands, nucleic acids, covalent modifications and proteins | bar | `PLOT \| facet: category (4: ligands, nucleic acids, covalent modifications, proteins) \| vary: dataset × method (13 bars) \| series: method (6: AF3, RoseTTAFold2NA, AIchemy_RNA2, AF-M 2.3, AutoDock Vina, RoseTTAFold All-Atom) \| measure: success % / interface LDDT / LDDT (compound — see panels) \| mark: bar with 95% CI \| n: printed under every bar (428, 428, 427, 25, 38, 8, 66, 40, 91, 23, 28, 1064, 65, 338); per-mark n = that many targets/structures/clusters` | 4 sub-panels sharing one 0–100 axis | **Four different measures share one "Success (%)" axis** — % r.m.s.d. < 2 Å, interface LDDT, LDDT and % DockQ > 0.23 are plotted at the same scale, so bar heights are not comparable across sub-panels even though the eye reads them that way. The single "AF3 2019 cut-off" ligand bar silently comes from a **different trained model** than every other AF3 bar. The privileged pocket-specified AF3 arm (90.2%) is not shown here, only in ED Fig. 4a | as above (CC BY 4.0) |
| 1D | 2 | AF3 inference architecture: template/genetic/conformer search → input embedder → pairformer → diffusion module → confidence module | schematic | `SCHEMATIC \| inference data flow with module block counts and recycling/diffusion loops \| no data` | 1 panel | — | as above |
| 2A-C | 3 | Pairformer block, diffusion module, and the training set-up with mini-rollout and gradient stops | schematic | `SCHEMATIC \| module internals (triangle updates, attention stacks, per-atom/per-token conditioning) and the training/inference loop with permutation of ground truth \| no data` | 3 lettered panels (a, b, c) | — | as above |
| 2D | 3 | Training curves: LDDT on the evaluation set vs optimizer steps, across initial training and two fine-tuning stages, for eight intra- and inter-chain metric types | line + scatter | `PLOT \| facet: none (1) \| vary: optimizer steps, 0–140,000 (continuous) \| series: metric type (8: intraligand, intraprotein, intra-DNA, intra-RNA, protein–ligand, protein–protein, protein–DNA, protein–RNA) \| measure: LDDT \| mark: point (raw) + line (median-filtered, kernel width 9) \| n: NOT REPORTED per curve` | 1 panel with two stage boundaries and 97%-crossing crosses | **The y-axis starts at 30, not 0**, which magnifies the fine-tuning gains; the curve is on **the evaluation set that also supplies the reported accuracies** (see `oracle_leakage` route 4) and the figure does not say so; no n behind any curve | as above |
| 3A-F | 4 | Six showcase predictions overlaid on ground truth: 40S ribosome + tRNA + initiation factors, EXTL3 homodimer, mesothelin peptide–antibody, PORCN + LGK974 + WNT3A, AziU3/U2 novel fold, PI5P4Kγ allosteric-site inhibitor | structure render | `RENDER \| facet: showcase complex (6: 7TQL, 7AU2, 7U8C, 7URD, 7WUX, 7QIE) \| views: 1 \| overlay: NOT REPORTED predictions on 1 reference (grey) \| axis: none` | 6 lettered panels; vary by system | Examples were selected with training-set similarity in hand (p4) and the selection rule lives in the unheld Supp. Methods 8.1; no failure examples appear here (they are quarantined to Fig. 5) | as above |
| 4A | 6 | Interface accuracy vs chain-pair ipTM, for protein–protein (DockQ) and nucleic acid–protein (iLDDT) | box | `PLOT \| facet: interface type (2: protein–protein, nucleic acid–protein) \| vary: chain pair ipTM band (5: 0–0.4, 0.4–0.6, 0.6–0.8, 0.8–0.95, 0.95+) \| series: none (1) \| measure: DockQ / iLDDT \| mark: box (25–75% box, median line, 5–95% whiskers) \| n: clusters per box printed (834/692/1,574/1,804/229 and 277/320/449/344/108)` | 2 box panels in the top row of a | Boxes show 5–95% whiskers, so the worst 5% of each band — the cases a confidence-based decision would actually get wrong — are cut off; **no homology filtering** on this set (p5) and the caption does not say so | as above |
| 4B | 6 | Ligand pose accuracy vs chain-pair ipTM, as a stacked composition of r.m.s.d. bands | bar (stacked) | `PLOT \| facet: none (1) \| vary: chain pair ipTM band (5) \| series: pocket r.m.s.d. threshold band (5: 0–0.5, 0.5–1.0, 1.0–2.0, 2.0–5.0, 5.0+ Å) \| measure: % of clusters below threshold \| mark: bar (stacked to 100%) \| n: 7 / 29 / 92 / 299 / 481 clusters per bar` | 1 panel, top-right of a | **The lowest-confidence bar rests on n = 7 clusters** and is drawn at the same visual weight as the n = 481 bar, with no CI; the stacked-to-100% form makes every bar the same height regardless of n | as above |
| 4C | 6 | Per-entity accuracy vs chain-averaged pLDDT for protein, nucleic acid and ligand entities | box | `PLOT \| facet: entity type (3: protein, nucleic acid, ligand) \| vary: chain pLDDT band (4: 0–50, 50–70, 70–90, 90+) \| series: none (1) \| measure: LDDT to polymer \| mark: box (25–75%, median, 5–95%) \| n: clusters per box printed (107/469/2,283/1,552; 227/225/189/229; 57/136/396/934)` | 3 box panels in the bottom row of a | The measure is **LDDT_to_polymer, chosen because it is "closely related to how the confidence prediction is trained"** (p9) — a self-consistent pairing the panel does not flag; no homology filtering | as above |
| 4D | 6 | PDB 7T82 rendered twice, coloured by per-atom pLDDT and by chain | structure render | `RENDER \| facet: colouring (2: pLDDT bands, chain identity) \| views: 1 \| overlay: 1 prediction on 0 references \| axis: none` | 2 panels (b, c) | No ground-truth overlay, so the reader cannot check the pLDDT colouring against actual error on this example | as above |
| 4E | 6 | Interface DockQ scores between the four chains of 7T82 | heatmap | `MATRIX \| rows: chain (4: A, C, D, F) \| cols: chain (4) \| value: interface DockQ score \| facet: none (1)` | 1 panel (d), 4×4 with empty non-contacting cells | — | as above |
| 4F | 6 | Predicted aligned error matrix for the same 7T82 prediction | heatmap | `MATRIX \| rows: residue index (~880) \| cols: residue index (~880) \| value: expected position error (Å, 0–30+) \| facet: none (1)` | 1 panel (e) with dashed chain boundaries and chain colour bars | Colour scale saturates at 30 Å, so all badly-placed pairs render identically | as above |
| 5A | 7 | Top-ranked antibody–antigen interface quality as a function of seeds per target, AF3 vs AF-M 2.3, at two DockQ thresholds | line | `PLOT \| facet: accuracy threshold (2: DockQ > 0.23 "correct", DockQ > 0.8 "very high accuracy") \| vary: seeds per target, 1–1,000 (continuous, log axis) \| series: model (2: AF3, AF-M 2.3) \| measure: % of low-homology antibody interface clusters \| mark: line with 95% bootstrap band \| n: 65 clusters per panel; each point = mean over 1,000 resamples with replacement out of 1,200 seeds` | 2 panels inside a | Both panels' y-axes start above 0 and **the two panels use different y-ranges** (≈15–65 and 0–40), so the AF3/AF-M gap looks similar in both when it is not; the x-axis stops at 1,000 with the curve still rising, which the text concedes ("keep improving … even at as many as 1,000") | as above |
| 5B | 7 | Three failure modes rendered against ground truth: chirality inversion on 7CTM, hallucinated order in a nuclear pore complex with 1,854 unresolved residues (7F60, AF-M 2.3 vs AF3), overlapping chains in a trinucleosome (7PEU) | structure render | `RENDER \| facet: failure mode (3: chirality, hallucination/disorder, clashes) × model where shown (2 for 7F60: AF-M 2.3, AF3) \| views: 1 \| overlay: 1 prediction on 1 reference (grey), 0 references for 7PEU \| axis: none` | 3 lettered panels (b, d, e); d has 3 sub-renders | **The paper's only evidence for three of its four stated limitations is one hand-picked render each**, with no rate attached except the 4.4% chirality figure in the text; 7PEU is shown without a ground-truth overlay | as above |
| 5C | 7 | Cereblon in open (apo, 8CVP) and closed (holo mezigdomide, 8D7U) ground-truth conformations, with AF3 predictions of both apo (10 overlaid samples) and holo — all closed | structure render | `RENDER \| facet: ligand condition (2: apo, holo) \| views: 1 \| overlay: 10 predictions (apo) and NOT REPORTED predictions (holo) on 1 reference each \| axis: none` | 1 lettered panel (c) containing 4 renders; vary by ligand condition and by prediction-vs-truth | **This is the paper's entire quantitative case for its conformational limitation and it carries no quantitative panel at all** — no inter-domain distance value, no threshold, no count of how many of the 10 apo samples were closed, no confidence values, and n = 1 system. Split from row 5B because `overlay` differs (10 vs 1) — see `unresolved` on whether the v3 split rule licenses that | as above |
| ED1A | 12 | One CAID 2 disordered protein (DP02376) predicted by AF-M 2.3, AF3, and AF3 trained without the cross-distillation set, coloured by pLDDT | structure render | `RENDER \| facet: model (3: AF-M 2.3, AF3, AF3 no cross-distillation) \| views: 1 \| overlay: 1 prediction on 0 references \| axis: none` | 3 renders in panel a | No ground truth shown (there is none for a disordered protein), so "hallucination" is judged by compactness by eye; 1 protein of 151 | as above |
| ED1B | 12 | ROC curves for residue-level disorder detection on CAID 2, by RASA and by pLDDT, for three models | line (ROC) | `PLOT \| facet: none (1) \| vary: false positive rate, 0–1 (continuous) \| series: model × score (6: AF-M 2.3 RASA 0.94, AF-M 2.3 pLDDT 0.93, AF3 RASA 0.95, AF3 pLDDT 0.91, AF3 no cross-distill RASA 0.67, AF3 no cross-distill pLDDT 0.89) \| measure: true positive rate (AUC annotated in legend) \| mark: line \| n: 151 proteins / 46,093 residues per curve` | 1 panel | Five of the six curves are near-superimposed in the top-left corner, so only the ablated RASA curve is visually separable; no CI on any AUC | as above |
| ED2 | 13 | Training curves with 90% and 97% crossing lines — same shape as Fig. 2d | line + scatter | `PLOT \| facet: none (1) \| vary: optimizer steps (continuous) \| series: metric type (8) \| measure: LDDT on the evaluation set \| mark: point + line (median filter, width 9) \| n: NOT REPORTED` | 1 panel (figure image not extractable as text; caption carries the structure) | Same evaluation-set-as-training-monitor issue as Fig. 2D | as above |
| ED3 | 14 | Three PoseBusters targets where Vina and Gold were inaccurate and AF3 was not (8BTI 0.65 Å, 7KZ9 1.3 Å, 7XFA 0.44 Å) | structure render | `RENDER \| facet: target (3) \| views: 1 \| overlay: 1 prediction on 1 reference (grey) \| axis: none` | 3 lettered panels | **Cases selected by the baseline's failure** (route 7 design-level selection); no matching panel of cases where AF3 failed and the baselines did not | as above |
| ED4A-E | 15 | PoseBusters success bars: V1 method comparison by privilege class, V2 Vina-vs-AF3, V2 by homology stratum, V2 by ligand familiarity, V2 accuracy-with-validity | bar | `PLOT \| facet: analysis (5: V1 all methods, V2 head-to-head, V2 homology strata, V2 ligand class, V2 validity) \| vary: method or stratum (13 / 2 / 3 / 2 / 9 bars) \| series: validity (2: RMSD < 2 Å, RMSD < 2 Å and PB-valid — in d and e only) \| measure: % r.m.s.d. < 2 Å \| mark: bar with exact-binomial 95% CI \| n: 428 (427 RFAA) V1; 308 V2; homology bins 38 / 83 / 187; ligand classes 50 / 258` | 5 lettered panels (a–e) sharing one measure; a and e carry privilege-class dividers | Panel **c is the anti-memorization control and its bar values are not printed** (only e and d print numbers), so the most reusable result in the figure must be read off pixel heights; the n = 38 low-homology bin has a visibly wide CI that the text never quantifies | as above |
| ED4F | 15 | Per-check physical-validity pass rates, DiffDock vs AF3 2019, across 18 PoseBusters checks | bar | `PLOT \| facet: check category (3: chemical validity and consistency, intramolecular validity, intermolecular validity) \| vary: validity check (18) \| series: method (2: DiffDock, AF3 2019 cutoff) \| measure: % of all outputs passing check \| mark: bar \| n: 308 targets per bar` | 1 wide panel with 3 dashed category dividers | **~12 of 18 checks sit at or near 100% for both methods** (numeric saturation — cross-reference `metric_saturation`), so most of the panel's width carries no information; no CIs drawn on the bars | as above |
| ED5A | 16 | Per-target CASP15 RNA accuracy for AlphaFold 3, AIchemy_RNA and RoseTTAFold2NA, in LDDT, TM-score and GDT | bar | `PLOT \| facet: metric (3: RNA LDDT, RNA TM score, RNA GDT) \| vary: CASP15 target (10: R1116, R1117, R1126, R1128, R1136, R1138, R1189, R1190, R1107, R1108) \| series: method (3: AlphaFold3, AIchemy_RNA, RoseTTAFold2NA) \| measure: LDDT / TM score / GDT \| mark: bar \| n: 1 prediction per bar (top-1 ranked)` | 3 stacked panels sharing an x-axis | Missing bars are annotated as "No results from AIchemy_RNA" / "No results from RoseTTAFold2NA" for 4 of 10 targets, so **the per-method means are over different target sets**; R1136's score is against "the closest state" of multiple ground truths (p10) and the panel does not mark this | as above |
| ED5B | 16 | Nucleic-acid-only accuracy, AF3 vs RF2NA, for RNA-only and DNA-only complexes | box | `PLOT \| facet: none (1) \| vary: complex type (2: PDB RNA-only n = 29, PDB DNA-only n = 63) \| series: method (2: AlphaFold 3, RoseTTAFold2NA) \| measure: LDDT \| mark: box (25–75%, median, 5–95% whiskers, outlier points) \| n: 29 and 63 structures per box` | 1 panel, 2 grouped pairs | Medians are not printed; the caption warns that "some DNA structures in this set may not be duplexes" while RF2NA "was only trained and evaluated on duplexes" — an acknowledged out-of-regime comparison shown at equal weight | as above |
| ED5C-D | 16 | A mycobacteriophage immunity repressor on dsDNA (7R6R) coloured by pLDDT and by chain, with its PAE matrix | structure render + heatmap | `RENDER \| facet: colouring (2: pLDDT, chain) \| views: 1 \| overlay: 1 prediction on 0 references \| axis: none`; companion `MATRIX \| rows: residue (~260) \| cols: residue (~260) \| value: predicted aligned error (Å) \| facet: none (1)` | 2 renders (c) + 1 matrix (d) | "Note the disordered N-terminus not entirely shown" — part of the prediction is cropped out of the render | as above |
| ED6A | 17 | Accuracy on common phosphorylation residues, AF3 with vs without modelling the modification | bar | `PLOT \| facet: none (1) \| vary: condition (2: phosphorylation modelled, parent residue substituted) \| series: none (1) \| measure: accuracy on structures containing SEP/TPO/PTR/NEP/HIP \| mark: bar with exact-binomial 95% CI \| n: 76 clusters, paired two-sided Wilcoxon P = 1.6 × 10⁻⁴` | 1 panel | The measure's units are not stated in the caption (the y-axis label is not extractable); the effect is reported as a P value with no effect size in the text | as above |
| ED6B-D | 17 | Four modified-residue examples rendered against ground truth, with and without the modification modelled (7Z1K, 7US1, 7TNZ, 7SDW), coloured by pLDDT | structure render | `RENDER \| facet: system (4) × modification modelled (2: yes, no — for b and c only) \| views: 1 \| overlay: 1 prediction on 1 reference (grey) \| axis: none` | 3 lettered panels containing 6 renders; per-render mean pocket-aligned RMSDCα printed in the caption (2.104 vs 10.261 Å; 0.424 vs 9.706 Å; 0.840 Å; 0.502 Å) | Two hand-picked pairs carry the qualitative claim that pLDDT drops when the modification is omitted; no distribution | as above |
| ED7A | 18 | Single-chain LDDT against MSA depth (median per-residue Neff), AF3 vs AF-M 2.3 | scatter + line | `PLOT \| facet: none (1) \| vary: median per-residue Neff for the chain, 10⁰–10⁴ (continuous, log axis) \| series: model (2: AlphaFold 3, AlphaFold-Multimer 2.3) \| measure: single-chain LDDT \| mark: point (raw) + line (Gaussian kernel smoothing, window 0.2 log units) with 95% bootstrap band \| n: every protein chain in the low-homology recent PDB set with <20 chains and <2,560 tokens; count NOT REPORTED` | 1 panel | The two smoothed curves are near-indistinguishable across the whole range, which **is** the result ("very similar dependence", p5), but the point cloud is drawn in one colour family so the two models' raw points cannot be separated by eye; n never stated | as above |
| ED7B | 18 | Ranked accuracy vs number of seeds, for seven molecule-type classes | line | `PLOT \| facet: none (1) \| vary: seeds per target, 1–30 (continuous) \| series: interface class (7: protein-intra, dna-intra, rna-intra, protein-dna, protein-rna, protein–protein antibody=False, protein–protein antibody=True) \| measure: LDDT or iLDDT \| mark: line with 95% bootstrap band (1,000 samples) \| n: clusters per series printed (386, 875, 78, 307, 102, 697, 58)` | 1 panel | **Two different measures (LDDT and iLDDT) share one y-axis** with the label "LDDT or iLDDT", so intra-chain and interface curves are not comparable despite being drawn together; the axis starts at 0 but the curves occupy only the 28–85 band, compressing the one curve that actually moves (antibody, n = 58) | as above |
| ED8 | 19 | Accuracy vs chain-pair ipTM for ion, bonded-ligand and bonded-glycan interfaces, as stacked r.m.s.d. bands | bar (stacked) | `PLOT \| facet: interface type (3: ion–protein, bonded ligand–protein, bonded glycan–protein) \| vary: chain pair ipTM band (5) \| series: pocket RMSD threshold band (5: 0–0.5, 0.5–1.0, 1.0–2.0, 2.0–5.0, 5.0+ Å) \| measure: % of interface clusters below threshold \| mark: bar (stacked to 100%) \| n: printed per bar (ions 34/48/175/332/377; bonded ligands 0/0/2/30/49; glycans 0/1/1/16/12)` | 3 panels | **Full-height bars are drawn on n = 1 and n = 2 clusters** in the bonded-ligand and glycan panels, and empty bands on n = 0, with no CI anywhere — a 100% bar on one cluster reads identically to a 100% bar on 377. This set is also unfiltered for homology (p5) | as above |
| ED9 | 20 | DockQ against iLDDT for protein–protein interfaces, one point per cluster, with a Huber fit and translated thresholds | scatter | `PLOT \| facet: none (1) \| vary: iLDDT (continuous) \| series: none (1) \| measure: DockQ \| mark: point + fitted line (Huber regressor, epsilon 1) \| n: 1 per mark; 4,182 clusters per panel` | 1 panel | Heavy overplotting at 4,182 points with no density encoding; the derived equivalences (0.23 → 23.6, 0.8 → 77.6) are quoted in the caption without a residual or R² | as above |
| EDT1 | 21 | The full accuracy table: task × dataset × metric × privilege class × method, with N, mean and 95% CI | table (not a plot) | `SCHEMATIC \| tabulated per-arm accuracy with N and 95% confidence intervals across ligands, nucleic acids, covalent modifications and proteins \| no data` (a rendered table, not a data graphic) | 1 table, ~60 rows, 4 task blocks | The table is **an image in the PDF and does not extract as text** — it had to be rendered to be read, which is why a corpus quoting AF3's numbers so often quotes Fig. 1c instead. The privilege class ("Holo protein struct. given", "Pocket residues specified") is a `Notes` column that is easy to miss when quoting a row | as above |

**Licence, recorded once because it governs every row.** p8:

> "**Open Access** This article is licensed under a **Creative Commons Attribution 4.0
> International License**, which permits use, sharing, adaptation, distribution and reproduction in
> any medium or format, as long as you give appropriate credit to the original author(s) and the
> source, provide a link to the Creative Commons licence, and indicate if changes were made. The
> images or other third party material in this article are included in the article's Creative
> Commons licence, unless indicated otherwise in a credit line to the material… To view a copy of
> this licence, visit http://creativecommons.org/licenses/by/4.0/."

**CC BY 4.0 with NO ND clause and NO NC clause** — figures may be redrawn, recoloured, cropped,
adapted and reused commercially with attribution. This is the permissive case and is unusual in
this corpus; the one caveat the licence itself names is third-party material carrying a separate
credit line, and none is flagged in these figures.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), single-paper extraction against SCHEMA.md v3.
- **schema_version**: `v3`
- **confidence**: **high** for A, B, D, E and the two commissioned fields
  (`anti_memorization_design`, `stated_limits`, `confidence_as_discriminator`); **medium** for the
  parts of C and F that depend on unheld Supplementary Methods (`structural_priors_used` item 2,
  `oracle_leakage` route 4) and on values read off bar heights (Extended Data Fig. 4c, ED Fig. 5b).
  What was hard to read: Extended Data Table 1 and every Extended Data figure body are **images**
  in this PDF and do not extract as text — pages 6, 7, 12, 15, 16, 18, 19 and 21 had to be rendered
  and read visually (8 pages rendered, all deleted afterwards). The `pdftotext -layout` output
  interleaves axis labels and captions in the two-column pages, so all quotes were checked against
  the rendered page where any ambiguity existed.
- **unresolved**:
  1. **The p9 cutoff contradiction, already flagged at the top.** Methods "Training regime" (p9)
     prints "for the model used in PoseBusters evaluations, we filtered out PDB structures released
     after **30 September 2021**", contradicting p5 ("a training cut-off of 30 September 2019 for
     AF3 to ensure that the model was not trained on any PoseBusters structures"), p9 "Inference
     regime" ("an earlier cut-off date of 30 September 2019 was used") and p10 ("differing only in
     the use of an earlier 30 September 2019 cut-off"). Verified against a rendered crop of p9, so
     it is not a text-extraction artefact — it is what the printed Methods says. Three statements
     against one, and the one is internally self-contradictory (a "separate model with an earlier
     cutoff" cannot have the same cutoff), so **30 September 2019 is correct for the PoseBusters
     model**. Worth a note to the corpus in case a downstream paper has propagated the 2021 figure.
  2. **A second numeric discrepancy**: the main text (p5) says multi-residue glycan success on
     all-quality data is "**42.1%** (n = 131 clusters)", while Extended Data Table 1 (p21) gives
     **42.4** for the same arm at the same n. Likewise p5 gives single-residue all-quality as
     "46.1% (n = 167)" against the table's **46.0**. Small, but a corpus quoting either should know
     the two disagree.
  3. **Extended Data Fig. 4c values are not printed.** The homology-stratified PoseBusters result —
     the single most useful anti-memorization number in the paper — exists only as three bar
     heights (≈89 / ≈82 / ≈78%). No table, no SI held. Same for the ED Fig. 5b medians.
  4. **The scope of the cross-distillation set cannot be determined.** Main text p4 says "we enrich
     the training data with structures predicted by AlphaFold-Multimer (v.2.3)" without scope;
     Extended Data Fig. 1 (p12) calls it "the disordered protein PDB cross distillation set", which
     implies it is scoped to disordered proteins. Supp. Methods 2.5 would settle it and is not held.
     This matters for `structural_priors_used`: "AF3 was trained on AF2 predictions" is either a
     narrow disorder-specific intervention or a broad distillation regime, and the PDF does not say.
  5. **No total prediction count and no compute figure** anywhere in the article, Methods or
     Extended Data.
  6. **Fig. 1c mixes four measures on one axis** labelled "Success (%)" and the caption discloses
     this in prose only. Recorded in `hides`, but flagged here because it is the figure most likely
     to be re-quoted from this paper.
  7. **The confidence-calibration arm has no homology control** ("with no homology filtering and
     including peptides", p5), so nothing in Fig. 4 or ED Fig. 8 separates calibration on
     training-similar chains from calibration on novel ones. Not resolvable from this PDF.
  8. **SI not held** — see `si_in_scope` for the specific consequences.
- **tags needed but not in the v3 vocabulary** (recorded, not invented):
  - A **`model-release` / `foundation-model`** tag. This paper is neither a benchmark
    (`benchmark-only` is plainly wrong — it introduces a model) nor a state-handling method. The
    corpus now holds several papers that *use* AF3 and none that is *about* releasing a backbone.
    Without such a tag, "which paper introduces the backbone we all use" has no reverse lookup.
  - A **`cutoff-authority` / `training-cutoff-source`** utility tag. The stated purpose of this note
    is that other papers define their held-out sets against AF3's cutoff. `comparator-numbers` is
    close but means accuracy numbers, not dates. A query for "where does our cutoff number come
    from" currently cannot be answered by tags.
  - A **`hallucination`** or **`disorder`** topic tag. The paper's hallucination/cross-distillation
    material (p4, p5–p6, ED Fig. 1) is substantive and reusable, and there is no tag that finds it.
  - A **`diffusion`** method tag. `cofolding` is correct and was used, but it does not distinguish
    a diffusion-based generative co-folding model from a regression-based one — a distinction that
    matters directly to whether a model can produce multiple states at all.
  - A **`privileged-input`** or **`pocket-conditioned`** tag for the fine-tuned pocket-specified
    arm. `oracle-leak` overstates it (the arm is deliberate, labelled, and reported separately);
    nothing else fits.
- **schema ambiguities hit while extracting (blunt, as asked)**:
  1. **The panel-splitting rule contradicts its own worked example.** The rule says "Split when
     `mark` or `measure` differs", then immediately says "four box panels showing four metrics
     under the same faceting are one row with a compound measure". Those cannot both be followed.
     I resolved it as: *when the differing measure is itself the faceting variable, do not split;
     split only when the mark differs or when two genuinely different plot forms share a letter.*
     That is a guess. Fig. 1c (four measures, one axis, one mark) and Fig. 5a (two thresholds, one
     mark) were kept as single rows on that reading; Fig. 4 was split three ways because the marks
     differ (box vs stacked bar). State the intended rule explicitly in v4.
  2. **RENDER rows have no split criterion at all.** The rule names only `mark` and `measure`,
     neither of which exists in the RENDER form. I split Fig. 5c out of Fig. 5b–e because `overlay`
     differs (10 samples vs 1) and because 5c is the row every conformational query will want to
     hit — but nothing in v3 licenses that. If `overlay` and `facet` are legitimate split criteria
     for RENDER, say so; otherwise the single most important render in this paper gets buried in a
     four-panel compound row.
  3. **A rendered TABLE has no data_shape form.** Extended Data Table 1 is the paper's real
     comparator artefact and it is an image, not text. `SCHEMATIC | … | no data` is a false
     statement about a table carrying ~60 rows of measured data — the same objection that produced
     the TREE form in v3. A `TABLE | rows: <var> (<n>) | cols: <field list> | value: <what a cell
     holds>` form would fix it.
  4. **`metric_saturation` says "numeric only" but does not say whether a bounded metric pinned at
     its ceiling *for every arm* counts.** ED Fig. 4f has ~12 of 18 checks at 100% for both
     methods. I recorded it as saturation because it is numeric and it does destroy the comparison,
     but the field's wording ("Does the metric itself floor or ceiling in any arm they report?")
     could be read as requiring a *single* arm to saturate. Clarify.
  5. **`structural_priors_used` and `oracle_leakage` route 1 overlap badly for a model paper whose
     training set *is* the PDB.** Templates are simultaneously a design-time structural prior and a
     pipeline input. I put date-filtered template *use* under route 1 and the *training corpus*
     under `structural_priors_used`, and cross-referenced, but the boundary is arbitrary and two
     extractors would draw it differently.
  6. **No field records architecture, model size, training compute or availability.** For a model
     paper these are the first things a reader wants and the schema has nowhere for them; I put
     code availability in section A as an ad-hoc addition, which will not join against anything.
  7. **`n_targets` presupposes one number.** This paper has eleven evaluation arms with different
     units (targets, structures, clusters, complexes, interfaces). I wrote a per-arm list, which is
     not parseable as a number. A `n_targets_by_arm` sub-table, or an explicit instruction to list,
     would help.
  8. **`system` has no value for "all of the PDB".** `general protein` is the closest and
     undersells a paper whose whole point is nucleic acids, ligands, ions and modifications. The
     `general-protein` tag has the same problem.
- **why_it_matters**: *(left empty — the user's call.)*

---

## Tags

`general-protein` `cofolding` `templates-on` `single-state` `ensemble` `binary-predicate`
`continuous-metric` `visual-metric` `saturating-metric` `design-level-oracle` `anti-memorization`
`multi-backbone` `peer-reviewed` `background` `precedent` `comparator-numbers`

Justification for the non-obvious ones, so a future reverse lookup is not surprised:

- **`general-protein`** — the only system tag that fits; see ambiguity 8 above. The paper covers
  nucleic acids, ligands and modifications too, and no tag expresses that.
- **`cofolding`** — one model predicting protein, nucleic acid, ligand and ion coordinates jointly
  (p1, p8). Not `benchmark-only`: this paper introduces a model.
- **`templates-on`** — a template module and template search are part of the architecture and are
  used at inference, date-filtered (Fig. 1d p2; p9). **`no-template-no-msa` is emphatically NOT
  applicable** despite the MSA de-emphasis: MSAs are used in full.
- **`single-state` + `ensemble`** — the v3-sanctioned pair for a method that samples widely (25 to
  ~6,000 samples per target) and collapses onto one basin (p6, Fig. 5c p7). Both are needed; either
  alone misdescribes the paper.
- **`binary-predicate` + `continuous-metric`** — the paper reports both thresholded success rates
  (% r.m.s.d. < 2 Å, % DockQ > 0.23 / > 0.8) and continuous distributions (LDDT, iLDDT, DockQ
  boxes).
- **`visual-metric`** — applies *only* to the conformational claim: the open/closed call in Fig. 5c
  is made by eye from a render with a dashed distance line and no threshold or value (p7). It does
  **not** describe the accuracy machinery, which is fully quantitative. Tagged because a query for
  "papers that called a state by eye" should return this figure; the qualification is here so the
  hit is not misread as a blanket rigour criticism.
- **`saturating-metric`** — ED Fig. 4f validity checks at 100% for both arms; ceiling effects in
  the top ipTM/pLDDT bins of Fig. 4a (see `metric_saturation`).
- **`design-level-oracle`** (route 7, *not* `oracle-leak`) — showcase successes chosen with
  training-set similarity known (p4), failure cases chosen post hoc (p7, p14), the cereblon system
  chosen because both states were already deposited and the failure already published (ref. 42).
  The pipeline itself is clean of state-oracles: routes 2 and 3 are `NONE FOUND`.
  **`oracle-leak` deliberately NOT applied** — the route-4 finding (checkpoint selection and
  training-mixture weights chosen against the evaluation set, p3–p4) is real and is recorded in
  full, but applying `oracle-leak` would put AF3 in the same bucket as papers that fed the target
  state into the pipeline, which would be a false positive for every query that tag exists to serve.
  Flagged here so the decision is visible and reversible.
- **`anti-memorization`** — earlier-cutoff retrained model, a 1 May 2022–12 Jan 2023 evaluation
  window opening seven months after the training cutoff, a ≤40% identity homology filter, and a
  homology-stratified control actually run and analysed (p9, p10, p15). Emphatically not
  `no-anti-memorization`. Not `unpowered`: the smallest control bin is n = 38.
- **`multi-backbone`** — AF3, AlphaFold-Multimer v.2.3, RoseTTAFold2NA and RoseTTAFold All-Atom
  compared head to head, which is more than two. Judgement call flagged in section B.
- **`peer-reviewed`** — Nature, with named reviewers (p11). Not `preprint`.
- **`background` + `precedent`** — see `stance`. Not `threat`, not `negative-result`.
- **`comparator-numbers`** — Extended Data Table 1 (p21) is a complete per-arm accuracy table with
  n and 95% CIs, and the licence (CC BY 4.0, no ND) permits redrawing it.
- **Considered and rejected**: `prospective` (retrospective throughout — see `prospective`);
  `confidence-as-discriminator` (confidence is used as a *sample ranker* and validated against
  accuracy, never used or validated to judge conformational correctness — applying the tag would
  misrepresent the finding, which is precisely that this was never done); `experimental-validation`
  (no wet-lab arm); `msa-subsample` (MSA *processing* is reduced inside the architecture; no
  subsampling intervention is applied — collapsing these is exactly what SCHEMA.md warns against);
  `directed-state`, `ligand-driven`, `partner-driven`, `seed-only` (no state-directing handle
  exists, and the paper reports ligand conditioning failing to select the state);
  `orthosteric` / `allosteric-site` / `cryptic-pocket` (no site-focused arm; the one allosteric
  mention is a Fig. 3f showcase label, "an allosteric site of PI5P4Kγ", p4, which is not a study of
  allosteric sites); `figure-exemplar` (the figures are competent but the paper is kept for its
  cutoff, its limitations passage and its numbers, not its graphics).
