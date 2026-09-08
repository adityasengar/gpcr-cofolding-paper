# purnomo2026cafe

> Extraction note, SCHEMA.md v3. Quotes are verbatim from the bioRxiv PDF text layer.
> The layer breaks hyphenated words across lines and renders some en/em dashes
> oddly; inside quotes, line-break hyphenation has been rejoined and runs of
> whitespace collapsed to single spaces. One in-source grammatical error is kept and
> marked `[sic]`. No other alteration.
>
> **What this paper is.** A co-folding *method* paper, not a benchmark. It makes one
> negative finding (chemically simple fragments memorise the orthosteric site) and
> then proposes an inference-time fix (co-fold a competitive orthosteric blocker as
> an extra chain), validated by alchemical ABFE rather than by experiment.
>
> **What it is NOT.** It is not about protein conformational states. Every metric in
> the paper is about **where a ligand lands**, not what conformation the protein
> adopts. Section C is filled against binding-site placement, honestly labelled as
> such, and a conformational reading is deliberately *not* forced — see
> `state_metric` and `states_generated`.
>
> Same group as `sun2026kinconfbench` (ref 22 here, cited on p12). Extracted
> independently; nothing imported from that note.

---

## A. Identity

| Field | Value |
|---|---|
| `citekey` | `purnomo2026cafe` |
| `doi` | https://doi.org/10.64898/2026.07.19.739466 (bioRxiv; banner repeated on every page p1–p22). Matches `refs.bib` and `MANIFEST.csv`. |
| `year` | 2026. Manuscript dated "July 20, 2026" (p1); banner: "this version posted July 21, 2026" (p1). |
| `venue` | **bioRxiv preprint**, explicitly uncertified: "(which was not certified by peer review)" (p1). No journal destination is named anywhere in the PDF. Tagged `preprint`. |
| `title` | CAFE: A Co-folding Approach for Fragment Exploration of Allosteric and Cryptic Binding Sites (p1). |
| `authors` | Justin Purnomo, Kunyang Sun, Teresa Head-Gordon (corresponding: kysun@berkeley.edu, thg@berkeley.edu). Pitzer Theory Center & Dept. of Chemistry; Depts. of Bioengineering and Chemical & Biomolecular Engineering, UC Berkeley (p1). Contributions: "JP wrote the code. All authors performed analysis for the results section" (p18). Funded by NIAID U19-AI171954; NERSC/DOE DE-AC02-05CH11231 (p18). "The authors declare no competing financial interests." (p18). Code: https://github.com/THGLab/CAFE (p18, URL truncated in the text layer as `.../CAF`). |

## B. Scope

| Field | Value |
|---|---|
| `system` | **kinase + general protein (dual).** Primary stratum is five human **protein** kinases — AKT2 (P31751), CDK2 (P24941), CHEK1 (O14757), CSNK2A1 (P68400), MAPK14 (Q16539) (p3). A generality arm adds two non-kinases: PTP1B (P18031), a protein tyrosine phosphatase, and KRAS (P01116), a small GTPase (p4). Neither non-kinase is a GPCR, transporter, periplasmic-binding protein or ATPase, so both fall under `general-protein`. |
| `n_targets` | **7 proteins** — "a multi-family benchmark comprising seven diverse targets: five representative human kinases (AKT2, CDK2, CHEK1, CSNK2A1, MAPK14), a protein tyrosine phosphatase (PTP1B), and a small GTPase (KRAS)" (p6). Worth flagging against the paper's own generality claim: five of seven are protein kinases, the two non-kinase arms are each a single protein with a single blocker, and the cryptic-pocket, double-blocker, ABFE and virtual-screening sections are **kinase-only**. |
| `method_class` | **co-folding + MD (dual).** (i) Co-folding: an inference-time input intervention on Boltz-2 — a competitive pocket occupant added as an extra co-folded entity (p5). No training, no fine-tuning: "a simple and training-free inference protocol" (p2). (ii) MD: absolute binding free energies by explicit-solvent double-decoupling alchemical MD, used as the validation layer (p5–6). Also uses BRICS fragmentation (RDKit), DBSCAN clustering of fragment COMs, P2Rank/FPocket cross-reference, and PLIP interaction counting as auxiliary machinery. |
| `backbones` | **Boltz-2 only** (p2, p5). Not `multi-backbone`. The model-agnosticism claim is asserted, never tested: "although Boltz-2 was used as the co-folding engine, the blocking strategy is model-agnostic in principle. Any joint protein–ligand structure prediction model that accepts multi-chain inputs — including AlphaFold3, RoseTTAFold All-Atom, or future co-folding architectures — could implement the same orthosteric (or allosteric) exclusion logic by including an appropriate pocket occupant as an additional chain." (p17). No AF3, Chai-1 or RFAA arm is run. |
| `templates` | **NOT REPORTED.** The words "template" and "templates" never appear in connection with the Boltz-2 inputs. The full input specification is: "All other inputs were held constant between conditions, including the protein sequence, multiple sequence alignment (MSA), and fragment SMILES." (p5) — which names the sequence, the MSA and the ligand, and is silent on templates. Boltz-2 defaults are presumed but never stated. This matters: if templates were retrieved by default, deposited holo coordinates of these very targets could enter the pipeline (see `oracle_leakage` route 1). |
| `msa_handling` | **full (presumed), source and depth NOT REPORTED.** An MSA is used and is held identical across arms — "including the protein sequence, multiple sequence alignment (MSA), and fragment SMILES" (p5) — but its construction, database, and depth are never described. **No MSA manipulation of any kind is performed**: not subsampled, not clustered, not state-filtered, not pinned. The MSA is a held-constant control variable here, not a handle. |

## C. Conformational core

| Field | Value |
|---|---|
| `states_generated` | **ensemble + single-state**, and the object is a *ligand-placement* ensemble, not a protein conformational ensemble. Ensemble: "Ten independent diffusion samples were generated per fragment per condition." (p5), and all localization metrics are "computed independently for each of the ten diffusion samples per fragment per condition and summarized as means across the ensemble" (p5). Single-state: without a blocker that ensemble collapses onto the one orthosteric basin — for the full kinase library, only 5.7% (orthosteric-derived) and 17.6% (allosteric-derived) of samples land anywhere but the ATP site (p7), and for 16 of 33 Enamine hits re-folded without the blocker "all ten independent trajectories route exclusively into the orthosteric pocket" (p15–16). That collapse *is* the paper's negative result. **The paper never generates, targets, scores or names a protein conformational state.** DFG-in/out, αC, activation loop and the entire kinase conformational vocabulary are absent; the one mention of conformational state is a citation to the group's own prior benchmark (p12). |
| `structural_priors_used` | **Extensive, design-time, and largely legitimate — but it is what the whole protocol is built out of.** (1) **Target selection**: "Five human kinases were selected for which multiple deposited allosteric inhibitor co-crystal structures are available" (p3), and specifically chosen to span PDB coverage: "providing a deliberate test of whether ADP-blocked co-folding generalizes across targets with varying degrees of training data coverage" (p3). (2) **Reference structures**: one orthosteric type-I co-crystal per kinase (2JDO, 2UUE, 2YEX, 3WAR, 3S3I) and 24 allosteric co-crystals across the five kinases, all enumerated by PDB ID (p3–4); 7 PTP1B and 3 KRAS allosteric references plus orthosteric references 5K9W and 4OBE (p4). (3) **The fragment library itself is built from deposited co-crystal ligands**: 22 type-I parents (19 from "a curated Modi–Dunbrack filtered type-I structure set", 3 AKT2 structures 3E88/3D0E/2JDO) and 21 of the 24 allosteric parents, BRICS-cut (p4). (4) **The blockers are known pocket occupants**: ADP for kinases, type-I inhibitor SMILES lifted from the orthosteric reference co-crystals, the DADEpYL hexapeptide for PTP1B, GDP for KRAS, and the parent allosteric ligand for the double-blocker arm (p4, p5, p14). (5) **PDB deposition statistics informed the blocker choice**: ADP over ATP "is consistent with the higher representation of ADP relative to ATP in kinase crystal structures deposited in the Protein Data Bank (PDB), which likely reflects a stronger structural prior for the ADP-bound configuration in Boltz-2." (p5). None of (1)–(5) is a methodological sin in itself; it is recorded here so that `oracle_leakage` records only what crosses into the pipeline or into the definition of success. The load-bearing consequence is stated in `oracle_leakage` route 1 and in the blocker analysis below. |
| `oracle_leakage` | **All seven routes worked below. Verdict: pipeline leakage on routes 1 (the blocker identity), 5 (success = distance to held references) and 6 (which poses got ABFE); design-level oracle on route 7; route 2 partial (curated kinase-conformation set builds the fragment library, not the model input); routes 3 and 4 clean.** The single most consequential finding for us: **the blocker is a known orthosteric binder of the target, so route 1 fires** — see the dedicated blocker section below. |
| `prospective` | **partial — prospective in chemistry and in site, retrospective in target selection, in blocker choice and in every success criterion.** Prospective half: the Enamine screen uses "an independent chemical-space probe distinct from BRICS decomposition of co-crystal parents" (p4), 300 fragments with no prior association to these targets, and the cryptic-pocket arm discovers sites with no deposited reference at all — "CAFE's exclusive discovery of the two CDK2 pockets" (p13). Retrospective half: the five kinases were chosen *because* their allosteric co-crystals exist (p3); the localization predicate is a distance to those co-crystals (p5); the type-I, PTP1B and KRAS blockers are taken from deposited complexes (p4); and the fragments in the main screen are cut from the very co-crystal ligands used as the answer key (p4). The authors call the workflow "prospective" repeatedly (Fig 1 caption p3, p14, p15) — that word describes the Enamine funnel, not the benchmark, and the note follows `oracle_leakage`, not the authors' word. No experimental validation of any kind. |
| `state_metric` | **binary predicate + RMSD-to-reference (dual) — and both are about *ligand placement*, not conformational state. Recorded as measured; a conformational reading would be a fabrication.** (i) **Binary predicate, the primary metric**: "A fragment was classified as allosterically or orthosterically localized for a given sample if d_allo ≤ 5.0 Å or d_ortho ≤ 5.0 Å, respectively." (p5), where d_allo is "the minimum Euclidean distance from the predicted fragment COM to the nearest heavy atom of any allosteric reference ligand in the per-kinase reference set" and d_ortho is the analogous distance to "the single canonical type-I reference ligand for each kinase (Cα-superposed onto the parent crystal)" (p5). The derived headline quantity is the "non-orthosteric exploration rate", "the percentage of diffusion samples in which the predicted fragment center-of-mass (COM) is at least 5.0 Å away from the canonical orthosteric pocket" (p6). **The 5.0 Å cutoff is stated but never justified** — no sensitivity analysis, no reference, no rationale. Same for the DBSCAN parameters ("ϵ = 5 Å, min_samples = 5", p12–13) and the hit threshold ("ΔG ≤ −1 kcal/mol", Fig 6 caption p15). (ii) **RMSD-to-reference, secondary**: Figure 3B reports the "Heavy-atom RMSD distribution of allosterically localizing poses relative to the crystallographic reference, with and without ADP blocking" (p10), reaching 15.4 Å for non-localizing samples (p9). (iii) Note also a **coordinate-frame dependency**: "each predicted structure was aligned to the case-specific reference protein by Cα-only superposition in PyMOL" (p5) — every distance is measured after superposing onto the held reference structure. Not `visual-metric`: the renders (Figs 2C, 5A, 6C) illustrate conclusions the predicate already established, rather than substituting for it. |
| `metric_saturation` | **Yes — genuine numeric ceiling, at 100%, acknowledged by the authors.** The primary metric is a bounded percentage of samples. Table 1 blocked column (p6): AKT2 **100.0%**, CHEK1 **100.0%**, CSNK2A1 **100.0%**, KRAS **100.0%** (from an already-saturated 99.3% unblocked), CDK2 99.7%, PTP1B 99.6% — six of seven targets sit at or within 0.4 points of the ceiling, so the with-blocker column carries almost no resolving power and no target could have exceeded it. Figure 3A: CSNK2A1 with ADP = 100.0% (p10). The cryptic arm hits the same wall and the authors say so explicitly: "CDK2, which already showed near-saturating cryptic exploration under ADP blocking alone (97.9%), was unaffected by the additional allosteric block (96.3%)" (p14), and the Figure 5 caption concedes "where cryptic sampling is already saturated under ADP alone" (p13). Consequence: the double-blocker arm is uninterpretable for CDK2 and CHEK1 by construction, and the claimed *magnitude* of the blocker effect is a floor-to-ceiling artefact for four of seven targets. **Axis issues are not recorded here** (v3 change 9) — the Fig 4 missing-uncertainty and Fig 5B overlapping-SEM problems live in `hides` on rows `4` and `5B`. |
| `directional_control` | **Yes — and this is the paper's mechanism. The handle is a competitive co-folded ligand occupying a pocket you want vacated. It is *exclusionary* (negative) and it directs *site*, not conformational state.** Handles used, in order of increasing prior knowledge required: (a) **ADP**, a family-generic endogenous cofactor, for all five kinases; (b) **a type-I inhibitor**, SMILES taken from that target's own orthosteric co-crystal; (c) **a target-specific known orthosteric binder** for non-kinases (DADEpYL hexapeptide for PTP1B, GDP for KRAS); (d) **ADP + the parent allosteric ligand together** (the "double blocker"), which requires a solved allosteric complex and steers past the allosteric site into cryptic space. Crucially, the handle says *where not to go*, never *where to go* — the model chooses the destination. The paper's own evidence that the destination is not controlled is CDK2: near-total orthosteric escape (99.7%) with near-zero canonical allosteric arrival (1.3%). Full mechanism section below. |
| `anti_memorization_design` | **NONE — no post-cutoff set, no date filter, no training-overlap analysis, and Boltz-2's training cutoff is never stated.** Every reference structure, fragment parent and blocker is a deposited PDB entry with no deposition-date constraint; the PDB IDs listed on p3–4 span 1T49 (2004) to 9C1W (2024) with no filtering. This is a striking gap for a paper whose central claim is *about memorization* — the word "memorization" appears in the abstract, the title of §3.1, and eight times in the text, yet nothing in the design separates training-set structures from non-training-set ones. The one design element that gestures at it is coverage stratification, not holdout: "providing a deliberate test of whether ADP-blocked co-folding generalizes across targets with varying degrees of training data coverage" (p3) — an ordinal proxy (CDK2 "the most structurally characterized kinase in the PDB", p7), never quantified with a count, an identity threshold or a date. The closest thing to a held-out set is chemical, not temporal: 300 Enamine fragments as "an independent chemical-space probe distinct from BRICS decomposition of co-crystal parents" (p4) — held out from the *authors'* library construction, not from Boltz-2's training. n = 300, cutoff = none. |
| `anti_memorization_control` | **NONE RUN for memorization in the training-data sense; two strong arms run for blocker-dependence, which is a different thing.** No arm anywhere compares pre- vs post-cutoff structures, high- vs low-identity-to-training targets, or holo-present vs holo-absent PDB entries. What *was* run and analysed: (i) the **blocker-removal reversal**, "we re-evaluate the 33 favorable hits by generating independent diffusion trajectories in the complete absence of the active-site blocker. Strikingly, 30 of the 33 hits (91%) immediately revert to orthosteric localization; for 16 of these fragments, all ten independent trajectories route exclusively into the orthosteric pocket." (p15–16) — this is an excellent control for *causal attribution to the blocker*, and it is simultaneously the sharpest memorization *demonstration* in the paper, but it controls nothing about training-set overlap; (ii) the **Enamine chemical-independence arm** (300 fragments × 5 kinases). Not marked `UNPOWERED` for the localization screen (n = 116 + 116 fragments × 5 kinases × 10 samples — thousands of observations). **`UNPOWERED` does apply to the ABFE arms**: CDK2 n = 1, AKT2 n = 3, CHEK1 n = 4 (p11), the trapped-fragment comparison n = 10 (p12), and the cryptic-cluster inventory n = 14 clusters (p12). Several of the paper's target-level thermodynamic conclusions rest on single-digit n. |
| `controls_run` | See the `controls_run` table below — **thirteen arms**, which is the most reusable content in this note. |
| `confidence_as_discriminator` | **Tested explicitly and rejected — a rare and genuinely useful negative result, though the paper contradicts itself on its direction.** Results: "We further evaluated whether Boltz-2's internal fragment-protein ipTM confidence metric could serve as a reliable proxy for correct allosteric placement without explicit distance scoring (Figure 3C). In unblocked runs, allosterically localized poses were assigned negligibly higher fragment-protein ipTM than orthosterically localized ones (median 0.945 vs. 0.907). We note that ADP blocking did not significantly improve the Boltz-2 the [sic] ipTM confidence score between allosteric and orthosteric placements (0.959 vs. 0.896). In fact, the orthosteric and allosteric score distributions overlap almost entirely in both the blocked and unblocked conditions, making a high ipTM value for an individual pose uninformative about which pocket it occupies." (p9), extended to the global metric: "This problem is also maintained with Boltz-2's internal global confidence metric (Supplementary Table S5)." (p9, table not held). **Validated as a use? No — validated as a *non*-use**, which is stronger than most papers manage: "native co-folding confidence scores cannot substitute for explicit geometric localization scoring in allosteric discovery screens." (p9). **Internal contradiction**: the Discussion reverses the sign — "orthosterically-localized samples consistently received higher confidence scores than allosterically-localized ones, and this bias persisted under ADP blocking at the fragment–protein interface level. Practitioners using confidence-ranked pose selection without explicit localization scoring would systematically prefer orthosteric placements" (p16) — but every number in the Results and every box in Fig 3C shows allosteric *above* orthosteric (0.945 > 0.907; 0.959 > 0.896). The Discussion's practical warning is therefore argued from a fact the paper's own data contradict. Recorded in `unresolved`. |

### The blocker mechanism, exactly as specified

This is the mechanistically important part of the paper. Everything below is verbatim with pages.

**What is supplied as a co-input.** A pocket occupant, added to the Boltz-2 YAML as an
additional co-folded entity alongside the protein and the test fragment:

> "Boltz-2 inputs were prepared in YAML format with fragment placement assessed under
> different paired co-folding conditions depending on task: a blocked arm in which an
> orthosteric pocket occupant was included as an additional co-folded entity, and an
> unblocked arm in which the fragment was co-folded with the protein alone. All other
> inputs were held constant between conditions, including the protein sequence,
> multiple sequence alignment (MSA), and fragment SMILES. Ten independent diffusion
> samples were generated per fragment per condition." — p5

> "For kinase targets, the blocker was adenosine diphosphate (ADP), which occupies the
> conserved ATP-binding site and physically excludes test fragments from that volume
> during inference. ADP was chosen over ATP as the orthosteric placeholder because the
> absence of the γ-phosphate yielded more consistent convergence of the nucleotide pose
> across diffusion samples, providing more reproducible occlusion of the ATP-binding
> site. This is consistent with the higher representation of ADP relative to ATP in
> kinase crystal structures deposited in the Protein Data Bank (PDB), which likely
> reflects a stronger structural prior for the ADP-bound configuration in Boltz-2." — p5

> "For the non-kinase targets, PTP1B and KRAS, the DADEpYL hexapeptide and GDP,
> respectively, served as the blocking chain in place of ADP (Section 2.1). All other
> protocol details were identical to the kinase screen." — p5

> "By treating the orthosteric occupant as an additional co-folded entity, the method
> physically excludes fragments from the canonical binding site during inference,
> leveraging the joint diffusion process that makes co-folding models well suited to
> capturing induced-fit effects at the fragment level." — p16

Double-blocker variant (two occupants at once, to push past the allosteric site into
cryptic space):

> "Because ADP blocking alone can still permit fragments to populate the canonical
> allosteric site rather than cryptic pockets specifically, we next tested whether
> jointly occluding both the orthosteric pocket and the canonical allosteric pocket
> could deliberately steer fragments toward cryptic sites. In this double-blocker
> condition, ADP and the parent allosteric ligand were co-folded together as competing
> occupants, leaving only cryptic and other non-canonical surface regions available to
> the fragment." — p14

**Stoichiometry.** One blocker entity per input in the single-blocker arms; two in the
double-blocker arm. The paper uses the singular throughout — "an additional co-folded
entity" (p5), "the blocking chain" (p5), "an appropriate pocket occupant as an
additional chain" (p17) — but **never states a copy number, a ratio, or any
concentration-like quantity numerically**, and no arm varies the number of blocker
copies. There is no molar stoichiometry in a co-folding input; the operative quantity
is chain count, and it is 1 (or 2). Sampling stoichiometry is stated: **ten diffusion
samples per fragment per condition** (p5). Record as: 1 protein : 1 blocker (or 2) :
1 fragment, 10 samples; copy number never numerically stated.

**What it changes, and what it does not.** It changes only the input entity list. Every
other input is held identical between the blocked and unblocked arms — "All other
inputs were held constant between conditions, including the protein sequence, multiple
sequence alignment (MSA), and fragment SMILES." (p5). No weights are touched ("a simple
and training-free inference protocol", p2), no template is supplied, no MSA is altered,
no internal tensor is edited, no seed scheme differs, and no post-hoc refinement is
applied ("without post-hoc refinement of the Boltz-2 prediction", p1). The blocker is
removed again before the ABFE stage: "Input structures contained the kinase protein and
the test fragment; the ADP blocker was removed prior to simulation." (p6).

**Does it require prior knowledge of the target's orthosteric pharmacology? YES for the
general recipe; only partially for the kinase-ADP special case.** Three tiers:

1. **ADP for kinases — family-level knowledge, not target-level.** ADP is the shared
   endogenous cofactor of the whole protein-kinase family; using it requires knowing
   the target is a kinase, not knowing any structure of *that* kinase. This is the
   weakest form of prior knowledge in the paper and is what makes the kinase arm close
   to "universal": "employing adenosine diphosphate (ADP) as a universal orthosteric
   blocker" (p2). Even here the *choice* was informed by deposited-structure statistics
   (p5 quote above).
2. **Type-I inhibitor blockers — target-specific deposited-structure knowledge.** The
   blocker SMILES are read straight off that kinase's own orthosteric co-crystal:
   > "For each kinase, one orthosteric reference structure was selected from
   > independently deposited type-I inhibitor co-crystals: 2JDO (AKT2), 2UUE (CDK2),
   > 2YEX (CHEK1), 3WAR (CSNK2A1), and 3S3I (MAPK14). These structures define the
   > orthosteric center-of-mass (COM) used for localization scoring and serve as the
   > source of the Type I blocker SMILES in the orthosteric blocker control arm." — p4
3. **Non-kinase targets — an explicitly required prerequisite.** The paper states the
   dependency in its own words, twice:
   > "extension to non-kinase targets illustrated by the phosphatase PTP1B and GTPase
   > KRAS **when appropriate orthosteric ligands are identified as blockers**" — p3
   > "we apply CAFE using Type I orthosteric blockers for kinase proteins, **known
   > orthosteric ligands as blockers** for non-kinase proteins in the RAS-MAPK
   > signaling pathway" — p1 (abstract)
   Concretely: PTP1B's blocker is the DADEpYL hexapeptide taken from PDB 5K9W, and
   KRAS's is GDP from PDB 4OBE (p4).
4. **Double blocker — requires a solved *allosteric* complex too**, since the second
   occupant is "the parent allosteric ligand" (p14). This is the strongest prior
   requirement in the paper and it is the arm that produces the cryptic-pocket enrichment.

**Verdict on the mechanism's prior-knowledge requirement.** CAFE cannot be run on a
target for which no orthosteric binder is known. For a novel target of an
uncharacterised family there is nothing to put in the blocker slot. The authors are
alert to this problem when criticising *others* — "these methods rely on whole,
full-sized ligands bound to pre-characterized sites and do not address the upstream
challenge of de novo allosteric site or cryptic site discovery in the absence of prior
structural knowledge." (p2) — and CAFE's answer is to move the prior-knowledge
requirement from the *query* ligand to the *blocker*: the fragment being placed needs no
prior association with the target, but the blocker does. That relocation is the actual
methodological contribution, and it is the reason `oracle_leakage` route 1 fires rather
than being cleared.

**Prior art acknowledged.** The blocker-as-extra-chain idea is not claimed as new; the
Introduction cites it: "other inference-time strategies include duplicating the
allosteric ligand in the input to enhance sampling, introducing known site occupants as
extra chains to block competing orthosteric pockets" (p2, refs 27–28). The novelty claim
is the *combination* with fragments and with de novo site discovery — see
`novelty_claims`.

### `oracle_leakage` — all seven routes, worked separately

| # | Route | Verdict | Evidence (verbatim + page) |
|---|---|---|---|
| 1 | Structures used as input or template | **YES — via the blocker, for three of four blocker types; and template retrieval is unstated, leaving a second channel open** | The blocker is a co-input, and for the type-I and non-kinase arms its identity is read off the target's own deposited co-crystal: "These structures define the orthosteric center-of-mass (COM) used for localization scoring and serve as the source of the Type I blocker SMILES in the orthosteric blocker control arm." (p4); "the DADEpYL hexapeptide and GDP, respectively, served as the blocking chain" (p5), from 5K9W and 4OBE (p4); the double blocker is "the parent allosteric ligand" from that target's allosteric co-crystal (p14). **What enters is chemical identity (SMILES), not coordinates** — no deposited coordinates are handed to Boltz-2 as an input structure anywhere in the paper, and that distinction matters: this is pharmacological leakage, not coordinate leakage. The ADP arm is the partial exception (family-level cofactor knowledge). **Second, unresolvable channel**: templates are never mentioned in the input spec (p5), so if Boltz-2's default template retrieval was left on, the target's own holo structures were retrievable. The paper gives no page on which templates are switched off, so this route cannot be cleared. |
| 2 | State annotations from a curated database driving templates or alignments | **NONE FOUND as a pipeline driver — but a curated kinase-conformation set does build the fragment library** | The one curated state resource used is Modi–Dunbrack: orthosteric fragments came from "22 type-I co-crystal parents: 19 from a curated Modi–Dunbrack filtered type-I structure set (wild-type, non-phosphorylated, non-covalent holo inhibitor co-crystals)" (p4, ref 40 = the Modi–Dunbrack kinase conformational nomenclature). That is a conformational-state annotation, and it selects which ligands get fragmented — it never touches a template or an alignment, and the model is never told anything about kinase conformation. Recorded here as partial, and its design-level consequence recorded at route 7. No GPCRdb, KLIFS or Kincore use. Protocol described p4–p5. |
| 3 | Cluster labels derived from known states | **NONE FOUND** | The only clustering is unsupervised and spatial, run on the model's own output with no reference labels: "we identify 14 recurrent non-orthosteric, non-allosteric clusters using density-based spatial clustering (DBSCAN on fragment center-of-mass, ϵ = 5 Å, min_samples = 5)" (p12–13). The clusters are subsequently *cross-referenced* to P2Rank/FPocket output (p13), which is an independent-tool comparison, not a label injection. Chemical clustering is likewise unsupervised: greedy max-min diversity and UMAP on Morgan fingerprints (p4–5). Protocol p4–5, p12–13. |
| 4 | Hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states | **NONE FOUND — no sweep is performed at all; two near-misses recorded** | There is no hyperparameter search anywhere: a single fixed protocol (10 diffusion samples, one blocker, one 5.0 Å cutoff) is applied to every target and every fragment (p5). No range is scanned, so v3's "tuning a *range* on the evaluation set" clause does not fire. **Near-miss (a)**: the blocker molecule was selected on an observed-behaviour criterion — "ADP was chosen over ATP as the orthosteric placeholder because the absence of the γ-phosphate yielded more consistent convergence of the nucleotide pose across diffusion samples" (p5) — i.e. tuned on model output, but on the *blocker's own* pose convergence, not on fragment-placement success against references, so it does not contaminate the metric. The accompanying justification does appeal to deposited-structure statistics (p5, quoted above), which is a prior, not a leak. **Near-miss (b)**: the decisive thresholds — 5.0 Å localization, ϵ = 5 Å, min_samples = 5, ΔG ≤ −1 kcal/mol — are all **stated without any justification, reference or sensitivity analysis** (p5, p12–13, Fig 6 caption p15). Unjustified is not the same as tuned, and the note records it as unjustified. But nothing in the paper lets a reader rule out that 5.0 Å was chosen after seeing where the fragments landed, and 5.0 Å is doing a great deal of work: it defines every headline percentage. |
| 5 | Success defined post hoc by RMSD/distance to a structure they had | **YES — explicit, and it defines every number in the paper** | "A fragment was classified as allosterically or orthosterically localized for a given sample if d_allo ≤ 5.0 Å or d_ortho ≤ 5.0 Å, respectively." (p5), where the distances are to deposited reference ligands (Eqs. 1–2, p5) after "Cα-only superposition in PyMOL" onto the reference protein (p5). The allosteric predicate is scored against the *union* of every deposited allosteric complex for that target: "Fragment localization to the allosteric region was scored against all available allosteric references simultaneously, taking the minimum COM distance across the full reference set." (p4) — a min over up to 10 references (MAPK14), which makes the allosteric predicate strictly easier to satisfy for well-characterised targets, in the direction that flatters the method. Figure 3B adds "Heavy-atom RMSD distribution of allosterically localizing poses relative to the crystallographic reference" (p10). This is unavoidable for a retrospective pose-placement study, and it is route-5 leakage on the schema's terms. |
| 6 | Best/worst labels assigned against a held reference | **YES — the ABFE cohort is selected by its reference-defined behaviour** | Which 30 complexes got the expensive validation was decided using the reference-based localization label: "Selected fragments represented cases exhibiting orthosteric localization in ≥ 60% of models in the absence of ADP but recovered the canonical allosteric pocket in at least one model upon blocking. This set was supplemented by fragments from AKT2 and CSNK2A1 that already engaged allosteric sites without ADP present, to broaden per-kinase coverage." (p10). Two distinct oracle steps: (a) the cohort is filtered on *rescue behaviour measured against the answer key*, and (b) within a fragment, the pose taken forward is "recovered the canonical allosteric pocket in at least one model" — i.e. **best-of-10 selected by proximity to the reference**, not by confidence and not blind. The paper never reports a blind top-1 ABFE number, so "Boltz poses match crystal poses thermodynamically" (p10) is a statement about oracle-selected poses. The complementary arm is selected the same way: fragments "completely trapped in the orthosteric site (10/10 diffusion samples orthosteric without ADP; zero baseline allosteric occupancy) but gained allosteric engagement under ADP blocking" (p12). |
| 7 | Design-level oracle — inputs or systems chosen because the expected answer is known | **YES — pervasive, and weaker than the pipeline routes above; labelled design-level** | (a) **Targets**: "Five human kinases were selected for which multiple deposited allosteric inhibitor co-crystal structures are available" (p3) — the panel exists because the answers exist. (b) **Fragments**: the main library is cut from the answer ligands themselves — "Allosteric fragments were derived from 21 of the 24 allosteric reference structures listed above" (p4) — so a fragment "finding" its allosteric site is a sub-structure returning to the pocket its parent occupies in a deposited structure. (c) **Blockers**: chosen because the target's orthosteric pharmacology is already known (route 1). (d) **Expected outcome declared in advance**: "providing a deliberate test of whether ADP-blocked co-folding generalizes across targets with varying degrees of training data coverage" (p3), and the hypothesis is stated before any result — "This failure is widely hypothesized to be protein-driven, reflecting learned model biases toward dominant orthosteric sites" (p2). **Nothing here contaminates the model's inputs beyond route 1**; it is study construction, and it is the ordinary way to build a retrospective method demonstration. It is recorded separately so the note does not conflate it with routes 1, 5 and 6. The Enamine arm (p14–16) and the cryptic-pocket arm (p12–14) are the two places where route 7 does *not* apply — no expected answer existed for either. |

### `controls_run`

| control | what it rules out | page |
|---|---|---|
| **Unblocked arm** — identical input minus the blocker entity (protein sequence, MSA, fragment SMILES held constant), 10 samples | That the redirection is a property of the fragment, the protein, the MSA or the sampler rather than of the blocker. This is the paper's baseline and the source of every "without blocker" number. | p5 (protocol), Table 1 p6, Fig 2A p8 |
| **Type-I inhibitor blocker arm** — a synthetic co-crystal inhibitor substituted for ADP | That the effect is specific to ADP, to a natural cofactor, or to a nucleotide chemotype. Cross-kinase mean rises to 91.0%, slightly *above* ADP's 85.0%. | p9, Fig 2A p8, Supp. Table S3 (not held) |
| **Cross-cohort co-folding** — all 116 orthosteric-derived and 116 allosteric-derived fragments folded against every kinase "regardless of native origin" | That redirection only works for fragments whose parent was already an allosteric binder of that target. Both cohorts are redirected (5.7%→80.4% and 17.6%→89.6%). | p7, Fig 2A p8 |
| **Double blocker** — ADP plus the parent allosteric ligand | That cryptic-site sampling is merely allosteric-site spillover; also tests whether site selection is tunable beyond a single exclusion. | p14, Fig 5B p13 |
| **Non-kinase targets** — PTP1B (peptide blocker) and KRAS (GDP blocker) | That the mechanism is a kinase-specific artefact of the ATP-site attractor. | p6–7, Table 1 p6 |
| **Blocker-removal re-fold of the 33 Enamine hits** — independent diffusion trajectories with no blocker | That non-orthosteric engagement is an artefact of fragment selection or of pose scoring rather than of the blocker: "30 of the 33 hits (91%) immediately revert to orthosteric localization". Simultaneously the paper's cleanest memorization demonstration. | p15–16 |
| **Paired orthosteric ABFE** — same fragment, orthosteric pose vs non-orthosteric pose | That redirection buys site change at the cost of affinity. Trapped-fragment set: allosteric ≥ orthosteric for 5/10, Wilcoxon p = 0.92. Enamine set: 14/23 (61%) favour non-orthosteric, mean −2.10 vs −0.62 kcal/mol. | p12, p16 |
| **Crystal-pose ABFE reference** (n = 30) — the same alchemical protocol run on the experimental pose | That co-folded poses are thermodynamically inferior to experimental ones. 21/30 equal or better; Wilcoxon p = 0.22. | p10–11, Fig 4 p11 |
| **P2Rank + FPocket cross-reference** of the 14 DBSCAN clusters | That CAFE's "cryptic" clusters are just cavities any static geometric tool would find. 10/14 (71%) are found; the CDK2 exceptions (4/8) are the discovery claim. | p12–13 |
| **INX-315 orthosteric-selectivity control**, run *unblocked* on a clinical CDK2-selective inhibitor and its BRICS fragments, CDK2 vs CDK6 | That the CAFE pipeline has traded away correct orthosteric molecular recognition. The heterocyclic core recapitulates >200-fold CDK2 selectivity; two peripheral fragments bind neither. | p12, Supp. Table S5 (not held) |
| **Chemical-space separation check** — Morgan fingerprints (r = 2, 2048 bits) + UMAP on the two 116-fragment cohorts | That the "orthosteric-derived" and "allosteric-derived" cohorts are the same molecules under two labels: "no cross-panel SMILES overlap". | p4, Supp. Fig. S1 (not held) |
| **ipTM confidence discriminator test** — ortho- vs allo-localizing poses, blocked and unblocked | That internal model confidence can substitute for explicit geometric localization scoring. It cannot; distributions "overlap almost entirely". | p9, Fig 3C p10 |
| **Activation-state control** — phosphorylated vs unphosphorylated CDK2 for the INX-315 core fragment | That fragment-level selectivity is robust to receptor activation state. It is not: "unphosphorylated structures reversed the selectivity direction". | p12, Supp. Table S5 (not held) |

## D. Claims

| Field | Value |
|---|---|
| `central_conclusion` | Co-folding models (here Boltz-2) place ligands at the canonical orthosteric site by default, and this bias survives fragmentation — even minimal fragments carrying only an aromatic ring, hydrogen-bond acceptors or nitrogens are pulled into the kinase ATP pocket regardless of where their parent ligand binds. Adding a competitive orthosteric occupant (ADP, a type-I inhibitor, a phosphotyrosine peptide, or GDP) as an extra co-folded chain physically excludes fragments from that pocket at inference time, raising the cross-kinase mean non-orthosteric sampling rate from 11.7% to 85.0%, redirecting fragments into canonical allosteric pockets and into cryptic pockets that P2Rank and FPocket miss, at binding free energies that match or exceed crystallographic references without any post-hoc refinement. Removing the blocker reverts 91% of hits to the orthosteric site, which both proves the mechanism and confirms the memorization. |
| `necessity_claims` | **Verbatim, with pages.** <br>1. "physical active-site occlusion serves as an essential, target-agnostic intervention that can override chemical bias and restore non-orthosteric pocket exploration, and is largely agnostic to the blocker used to do so." (p9) <br>2. "native co-folding confidence scores cannot substitute for explicit geometric localization scoring in allosteric discovery screens." (p9) <br>3. "Explicit center-of-mass localization scoring against crystallographic reference pockets is therefore a necessary complement to internal model confidence metrics in allosteric fragment screening workflows." (p16) <br>4. "activation state matching is not optional for fragment-level selectivity calculations, where every interaction is load-bearing." (p12) <br>5. On prior work, i.e. what CAFE claims others *cannot* do: "these methods rely on whole, full-sized ligands bound to pre-characterized sites and do not address the upstream challenge of de novo allosteric site or cryptic site discovery in the absence of prior structural knowledge." (p2) <br>6. "non-trivial pose quality requires structural priors that go beyond model confidence alone." (p16) <br>7. On CDK-A026, where no crystal comparison is possible: "demonstrates the utility of this approach when a classical crystal-pose comparison is fundamentally impossible." (p12) <br>8. On the method's own failure mode: "For harder targets, where co-folding models struggle to assemble the poses of the protein based on sequences which lack sufficient structural representation in the PDB, CAFE will also struggle." (p17) |
| `novelty_claims` | **Verbatim, with pages.** <br>1. "we introduce CAFE (Co-folding Approach for Fragment Exploration), a simple and training-free inference protocol designed to break fragment memorization and discover allosteric and cryptic binding sites de novo." (p2) <br>2. "CAFE establishes orthosteric blocking and fragment screening as a training-free, inference-time protocol that helps overcome some of the limitations of current co-folding models while elevating their great promise for allosteric and cryptic binding drug discovery." (p1, abstract; repeated near-verbatim p2) <br>3. The memorization finding claimed as new: "Unfortunately, our study reveals that orthosteric memorization using co-folding models is still a problem even with fragments, such that even minimal probes containing only aromatic rings, hydrogen bond acceptors, and/or nitrogen atoms default to the orthosteric site regardless of their parent ligand's origin or chemical context." (p2) <br>4. "CAFE's exclusive discovery of the two CDK2 pockets heavily populated by fragment probes underscores its prospective power, demonstrating that generative co-folding can successfully map highly plastic, non-orthosteric landscapes that remain inherently elusive to static, geometry-based prediction." (p13) <br>5. "A central finding is that ABFE calculations on raw Boltz-2-predicted poses without structural relaxation, refinement, or pose optimization return binding free energies comparable to or exceeding those from crystallographically derived reference poses. This is a non-trivial result" (p16–17) <br>6. "in summary, CAFE establishes orthosteric blocking and fragment screening as a training-free inference-time protocol that converts co-folding bias from a fundamental limitation into a powerful engine for AI-driven allosteric drug discovery." (p3) <br>7. "The CAFE framework thus provides the blueprint that can be adopted across the evolving landscape of structure prediction models, with the blocking strategy itself remaining unchanged regardless of which model is used." (p17) <br>**Note on scope**: the paper does *not* claim the blocker-as-extra-chain idea itself as novel, and cites prior art for it — "introducing known site occupants as extra chains to block competing orthosteric pockets" (p2, ref 28). The claimed novelty is blocker + *fragments* + de novo site discovery. |
| `stated_limits` | 1. Coverage dependence, stated as a hard limit: "For harder targets, where co-folding models struggle to assemble the poses of the protein based on sequences which lack sufficient structural representation in the PDB, CAFE will also struggle." (p17). 2. Target-specific escape failure: MAPK14 "displayed a more moderate response to ADP blocking (52.5% non-orthosteric vs. the 85.0% cross-kinase mean), pointing to target-specific active-site pocket geometries that can partially accommodate co-folded fragments alongside the ADP blocker." (p7). 3. Escape ≠ arrival: "Strikingly, CDK2 yielded near-zero canonical allosteric localization under both conditions despite achieving near-complete escape from the orthosteric site." (p9). 4. Confidence metrics are useless as a placement discriminator (p9, p16). 5. ABFE protocol limits: AKT2's "sole available AKT2 crystal reference (PDB 9C1W) contains zinc-mediated coordination contacts that standard non-covalent, restraint-based ABFE protocols are not designed to capture" (p11); CDK2's ABFE n = 1 "precluding direct crystallographic comparison" (p11–12). 6. Reference-side variance, not model-side: MAPK14 crystal-vs-Boltz preference "tracked strictly with parental crystal origin rather than fragment chemistry" (p11). 7. Activation-state sensitivity as "a practical warning" (p12). 8. Model-agnosticism asserted "in principle" only (p17). **Not stated by the authors as limits, and recorded here for completeness**: the total absence of a training-cutoff control; the ceiling saturation of the primary metric; the unjustified 5.0 Å cutoff; the single-backbone design; and the fact that the blocker requires prior knowledge of the target's orthosteric pharmacology. |
| `stance` | **Provisional — the user's call. `precedent` + `contrast`, and the precedent half is the more important one.** <br>**`precedent` on mechanism and on findings**: this paper does, with a competitive ligand co-input, the thing our approach does — it steers a co-folding model's placement decision by what else it puts in the box, at inference time, with no retraining and no template. It also independently establishes the memorization signature we rely on (simple fragments default to the canonical site; removing the blocker reverts 91% of hits), and independently establishes that internal confidence cannot discriminate placement. <br>**`contrast` on rigour**: no post-cutoff or training-overlap control despite a memorization thesis; success defined entirely by distance to structures they hold; the ABFE cohort selected by reference-based labels; primary metric saturated at 100% for four of seven targets; one backbone; no wet-lab validation; and the mechanism itself requires a known orthosteric binder, which is prior pharmacological knowledge of exactly the kind the paper criticises others for needing. |

## E. Quantitative comparators

### `metrics_reported`

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Non-orthosteric exploration rate, native allosteric-derived fragments, **no blocker** | AKT2 6.0 (n=15); CDK2 8.2 (n=38); CHEK1 27.4 (n=19); CSNK2A1 96.4 (n=11); MAPK14 24.2 (n=33); PTP1B 55.7 (n=23); KRAS 99.3 (n=14) | % of diffusion samples | d_ortho > 5.0 Å from the target's orthosteric reference ligand | Table 1, p6 |
| Non-orthosteric exploration rate, same fragments, **with blocker** | AKT2 100.0; CDK2 99.7; CHEK1 100.0; CSNK2A1 100.0; MAPK14 69.7; PTP1B 99.6; KRAS 100.0 | % of diffusion samples | same predicate; blockers ADP (kinases), DADEpYL (PTP1B), GDP (KRAS) | Table 1, p6 |
| Mean cross-kinase non-orthosteric rate, no blocker | 32.4 (16.5 excluding CSNK2A1) | % of samples | 5 kinases, allosteric-derived fragments | p7 |
| **Full-library, allosteric-derived cohort** | 17.6 → 89.6 (no blocker → ADP) | % of samples | n = 116 fragments × 5 kinases × 10 samples | p7, Fig 2A p8 |
| **Full-library, orthosteric-derived cohort** | 5.7 → 80.4 (no blocker → ADP) | % of samples | n = 116 fragments × 5 kinases × 10 samples | p7, Fig 2A p8 |
| Headline abstract figure | 11.7 → 85.0 | % mean non-orthosteric rate | "Across kinome targets, CAFE increases the mean rate of fragment co-folding to non-orthosteric sites from 11.7% up to 85.0%." The 11.7% is the mean of the two cohort rates above (5.7 and 17.6); the paper does not say so. | p2 (also p1 abstract, p7) |
| **Orthosteric-default fraction — the memorization number, stated as the complement of the paper's own metric** (arithmetic is 100 − the row above; the paper never prints it this way) | **orthosteric-derived cohort: 94.3% → 19.6%; allosteric-derived cohort: 82.4% → 10.4%** (no blocker → ADP) | % of diffusion samples landing within 5.0 Å of the orthosteric reference ligand | n = 116 fragments per cohort × 5 kinases × 10 samples each | derived from p7 |
| CDK2, the most PDB-characterised kinase | 2.2 → 80.2 | % of samples non-orthosteric | no blocker → ADP; "the lowest non-orthosteric exploration rate" | p7 |
| MAPK14, weakest responder | 52.5 (vs 85.0 cross-kinase mean) | % of samples non-orthosteric under ADP | pocket partially accommodates fragment alongside ADP | p7 |
| Cross-kinase mean under **type-I inhibitor** blocker | 91.0 | % of samples, all fragment types | vs 85.0 under ADP | p9 |
| PTP1B, text vs table (**they disagree — see `unresolved`**) | text: 50.4 → 96.2; Table 1: 55.7 → 99.6 | % of samples non-orthosteric | same arm, same n = 23 | text p7 vs Table 1 p6 |
| Fragment chemistry ↔ orthosteric capture | Spearman ρ ≥ 0.330, p < 0.0001 | correlation | aromatic ring count, HBA count, N count vs orthosteric placement, all 5 kinases | p7, Supp. Table S2 + Fig. S3 (not held) |
| Nitrogen-count split, unblocked | N > 2: 6.2 vs N ≤ 2: 21.9 | % non-orthosteric | "orthosteric memorization is partially encoded in the fragment chemistry" | p7 |
| **On-target allosteric localization** (d_allo ≤ 5.0 Å), no ADP → ADP | AKT2 42.7 → 93.3; CDK2 0.0 → 1.3; CHEK1 21.6 → 37.9; CSNK2A1 91.8 → 100.0; MAPK14 19.4 → 44.5 | mean % of models allosteric-localized | native allosteric-derived fragments, n = 15/38/19/11/33 | Fig 3A panel labels, p10 |
| Max RMSD of non-localizing samples | 15.4 | Å heavy-atom RMSD | vs crystallographic reference; "global surface exploration" | p9 |
| Fragment–protein ipTM, allo- vs ortho-localizing | unblocked 0.945 vs 0.907; ADP-blocked 0.959 vs 0.896 | median ipTM | "distributions overlap almost entirely" | p9, Fig 3C p10 |
| ABFE agreement with crystal poses | 21 of 30 equal or more favourable; Wilcoxon signed-rank p = 0.22 | count; p-value | Boltz allosteric pose ΔG_bind vs crystal pose ΔG_bind | p10, Fig 4 p11 |
| ABFE per-kinase breakdown | CSNK2A1 10/10 ΔΔG ≤ 0; CHEK1 3/4; MAPK14 7 allo-favourable / 5 crystal-favourable (n = 12); AKT2 n = 3 broad variance; CDK2 n = 1 | counts | same comparison | p11 |
| MAPK14 parent-structure effect | all 4 from PDB 5N63 favour crystal; all 4 from 5N64 favour Boltz | counts | ΔΔG sign vs parent PDB origin | p11 |
| Trapped-fragment allo-vs-ortho ABFE | 5 of 10 allosteric equal or better; Wilcoxon p = 0.92 | counts; p-value | fragments 10/10 orthosteric unblocked, zero baseline allosteric occupancy | p12 |
| Cryptic clusters found | 14 recurrent clusters; 10/14 (71%) matched by P2Rank or FPocket | count | DBSCAN ϵ = 5 Å, min_samples = 5, across 5 kinases | p12–13 |
| Per-target static-tool recovery | CHEK1 3/3; MAPK14 2/2; AKT2 1/1; CDK2 4/8 | count | vs P2Rank/FPocket on static receptors | p13 |
| CDK-A017 (PDB 8VQ3) ABFE | cryptic −3.42; orthosteric +1.42; crystal-native −0.36 | kcal/mol | same fragment, three pockets | p13 (Fig 5 caption), p14 |
| CDK-A026 (PDB 8VQ4) ABFE | cryptic −3.83; orthosteric −2.97 | kcal/mol | same fragment, two pockets; no crystal comparison possible | p14 |
| **Double-blocker cryptic exploration** (no blocker → ADP → ADP+allosteric) | AKT2 0.0 → 6.7 → 63.3; CDK2 1.1 → 97.9 → 96.3; CHEK1 8.9 → 66.8 → 66.8; CSNK2A1 9.1 → 9.1 → 90.0; MAPK14 4.5 → 24.5 → 37.6 | % of samples in neither canonical site | n = 15/38/19/11/33 fragments × 10 samples | Fig 5B panel labels p13; text p14 |
| Enamine prospective screen | 300 fragments × 5 kinases; 107 retained after filtering; 33 (31%) with ΔG ≤ −1 kcal/mol (AKT2 4, CDK2 5, CHEK1 6, CSNK2A1 7, MAPK14 11) | counts | ADP-blocked co-folding + PLIP ranking + ABFE | p14–15 |
| **Blocker-removal reversion** | 30 of 33 (91%) revert to orthosteric; 16 of those with 10/10 trajectories orthosteric | counts | re-folded with no blocker, independent trajectories | p15–16 |
| Enamine selectivity | 23/30 orthosteric poses stable; 14/23 (61%) non-orthosteric equal or better; mean ΔG −2.10 (non-ortho) vs −0.62 (ortho) | counts; kcal/mol | paired ABFE, ΔΔG = ΔG_allo/cryptic − ΔG_ortho | p16 |
| Orthosteric–allosteric pocket separation | 12.8 (AKT2) to 38.0 (CDK2) | Å between reference COMs | "confirming sufficient geometric separation for unambiguous localization scoring" | p4 |
| Localization cutoff | 5.0 | Å | d_allo / d_ortho classification threshold; **no justification given** | p5 |
| Fragment library filters | ≥ 8 heavy atoms, MW ≥ 150 Da (BRICS cohorts); MW < 250 Da (Enamine) | atoms; Da | single-cut BRICS on RDKit; greedy max-min Morgan diversity for Enamine | p4–5 |
| ABFE protocol | 16 λ windows; 5.0 ns complex and solvent legs, 2.5 ns restraint leg; 4 fs timestep (HMR 3.024 amu); Boresch restraints 10 kcal mol⁻¹ Å⁻²; MBAR at 298.15 K; ff14SB / GAFF2 / AM1-BCC / TIP3P / 0.15 M | simulation parameters | double-decoupling ABFE | p6 |

| Field | Value |
|---|---|
| `n_predictions` | **Reported per unit, never as a total.** Samples per fragment per condition: **10** ("Ten independent diffusion samples were generated per fragment per condition", p5). Targets: **7**. Fragment cohorts: 116 unique orthosteric-derived + 116 unique allosteric-derived kinase fragments (p4); 23 PTP1B; 14 KRAS; 300 Enamine (selected from 1,920 plated compounds, MW < 250 Da) (p4–5). Conditions: none / ADP / type-I for kinases, none / blocker for non-kinases, plus a double-blocker arm and a blocker-removal re-fold of 33 hits. **The paper never states a total number of Boltz-2 predictions anywhere.** For scale only, and flagged as *the extractor's arithmetic, not the paper's*: 232 × 5 × 3 × 10 = 34,800 (kinase library) + 300 × 5 × 10 = 15,000 (Enamine) + 116 × 10 = 1,160 (double blocker) + 460 + 280 (PTP1B, KRAS) + 330 (reversion) ≈ **52,000 predictions**. ABFE is the expensive layer and is small: 30 fragment–kinase complexes in the main arm (p5), plus orthosteric/cryptic legs for CDK-A017 and CDK-A026, the 10-fragment trapped set, the INX-315 set, and 107 → 30 + 23 in the Enamine funnel. |
| `comparable_to_ours` | *(left empty by the extractor, per v3)* |
| `si_in_scope` | **SI NOT HELD.** "Details of the data formats and usage notes are provided in the Supplementary Information." (p17) — no SI is present in the 22-page PDF. Six tables and five figures are cited and unavailable: **Table S1** (all fragment IDs and SMILES — so no fragment in this paper can be identified chemically from what we hold), **S2** (Spearman correlations of fragment chemistry vs placement, both the unblocked correlations and the residual HBD correlation), **S3** (per-target type-I blocker rates — only the 91.0% mean is in the main text), **S4** (per-complex ABFE values behind Fig 4, n = 30), **S5** (Boltz-2 global confidence metric *and*, separately, the INX-315 CDK2/CDK6 selectivity results — both cited as "S5", see `unresolved`), **S6** (per-hit ABFE values for the Enamine campaign); **Figs S1** (UMAP of the two fragment cohorts), **S2** (full fragment-to-orthosteric-pocket distance distributions for all seven targets — the distributions the Fig 2A/3A bars hide), **S3** (chemistry-vs-placement), **S4** (hinge pharmacophore), **S5** (orthosteric-derived fragments redirected into allosteric pockets). Net effect: **no per-complex ABFE value and no per-fragment identity is recoverable from the held PDF** — only the aggregate counts, the panel-label percentages, and the four ΔG values quoted in the Fig 5 caption and text. |

## F. Figures

Six main-text figures, on pages 3, 8, 10, 11, 13 and 15. Split into **13 panel-group
rows** by the v3 rule (split on `mark` or `measure`, not on `facet`). Figure 6B occupies
two rows because its top and bottom halves carry different marks and different measures.

| `fig_no` | `page` | `gist` | `plot_type` | `data_shape` | `panels` | `hides` | `reuse` |
|---|---|---|---|---|---|---|---|
| 1 | p3 | The CAFE workflow: BRICS a parent library, co-fold each fragment with the target under an orthosteric blocker, filter for non-orthosteric localization, compare ABFE with and without blocking (ΔΔG = ΔG_allo/cryptic − ΔG_ortho). | schematic | `SCHEMATIC \| fragment-library → blocked co-folding → non-orthosteric filter → paired-ABFE workflow diagram \| no data` | Single unlettered workflow diagram; no panel structure. | Its caption is **word-for-word identical** to Figure 6's caption ("The CAFE prospective screening workflow and pocket-selective fragment recovery"), including the "pocket-selective fragment recovery" clause which Figure 1 does not depict. A copy-paste defect, recorded in `unresolved`. | CC-BY-NC 4.0 International (banner, p1 and every page p1–p22). **No ND clause** — redrawing and derivative figures are permitted; commercial reuse is not. |
| 2A | p8 | Non-orthosteric exploration rate for both fragment cohorts under three blocking conditions, per kinase. The paper's core result panel. | bar | `PLOT \| facet: kinase (5: AKT2, CDK2, CHEK1, CSNK2A1, MAPK14) \| vary: blocking condition (3: None, ADP, Type I) \| series: fragment cohort (2: orthosteric-derived, allosteric-derived) \| measure: non-orthosteric exploration rate (% of Boltz-2 samples with COM > 5 Å from the orthosteric reference ligand COM) \| mark: bar (SEM error bars) \| n: 1,160 samples per bar (116 fragments × 10 diffusion samples); 6,960 per panel` | 5 panels, one per kinase; panels vary by system. Series legend below the panel row gives n = 116 per cohort. | Bar + SEM over a **strongly bimodal** underlying distribution — the paper's own thesis is that individual fragments go 10/10 orthosteric or 0/10 (p7, p16), which a mean and an SEM erase completely. The distributions exist only in Supplementary Figure S2, which is not held. n is in the legend, not on the panels. | as above (CC-BY-NC 4.0, p1–p22, no ND) |
| 2B.i | p8 | BRICS cleavage of the CHEK1 allosteric parent AGY (PDB 3JVS) into CHK-A016 (N count 1) and CHK-A018 (N count 3), as 2D structures. | schematic | `SCHEMATIC \| 2D chemical structures of one parent ligand and its two BRICS products, annotated with nitrogen count \| no data` | One panel; a two-product cleavage tree. | | as above |
| 2B.ii–C | p8 | Structural context of the CHEK1 orthosteric (blue) and allosteric (pink) pockets (B.ii); fragment MAP-A005 on MAPK14 under no blocker, ADP, and the type-I inhibitor CQ0 (C). | structure render | `RENDER \| facet: blocker condition (3: none, ADP, Type-I CQ0) for C; B.ii unfaceted pocket-context view of 1 system \| views: 1 \| overlay: NOT REPORTED predictions on 1 reference \| axis: none` | 4 renders across two panel letters; B.ii varies by pocket annotation, C varies by blocker condition. Grouped in one row: same mark and no measure, only `facet` differs. | A single representative pose is shown where 10 diffusion samples exist, and **the selection rule is never stated** — `1 of 10 (selection rule NOT REPORTED)`. The visual impression of clean redirection is therefore not the ensemble's behaviour (MAPK14 under ADP is only 69.7% non-orthosteric, Table 1 p6). | as above |
| 3A | p10 | On-target allosteric localization rate, with and without ADP, per kinase. | bar | `PLOT \| facet: kinase (5) \| vary: blocker condition (2: No ADP, With ADP) \| series: blocker condition (2, colour carries the same variable) \| measure: mean % of models allosteric-localized (COM within 5.0 Å of the nearest heavy atom of any allosteric reference ligand) \| mark: bar (error bars, type not stated) \| n: per panel AKT2 15, CDK2 38, CHEK1 19, CSNK2A1 11, MAPK14 33 fragments × 10 samples; printed on each panel header` | 5 panels, one per kinase; n printed per panel header, which is good practice. | Error-bar definition is not given in the caption (Fig 2A and 5B say SEM; this one says nothing). CSNK2A1's with-ADP bar sits exactly at the 100.0% ceiling — cross-ref `metric_saturation`. The CDK2 panel (0.0% → 1.3%), which is the paper's most informative negative, is rendered as two invisible bars with no distributional detail. | as above |
| 3B | p10 | RMSD of allosterically-localizing poses to the crystallographic reference, with and without ADP, pooled over all kinases. | histogram | `PLOT \| facet: none (1) \| vary: heavy-atom RMSD to crystallographic reference, 0–16 Å (continuous) \| series: blocker condition (2: No ADP, With ADP) \| measure: % of predicted poses \| mark: bar (overlaid, semi-transparent histogram) \| n: NOT REPORTED per series or in total` | Single panel, two overlaid series. | **n behind each histogram is never stated**, so the two series cannot be weighted against each other — and the No-ADP series is drawn from a much smaller pool (allosteric localization without ADP is near-zero for 3 of 5 kinases). Pooled across all five kinases, so the CDK2 anomaly is invisible here. | as above |
| 3C | p10 | Fragment–protein ipTM for ortho- vs allo-localizing poses, blocked and unblocked. The panel that kills confidence-as-discriminator. | box | `PLOT \| facet: blocker condition (2: No ADP, With ADP) \| vary: pose localization class (2: ortho-localizing, allo-localizing) \| series: pocket class (2: orthosteric, allosteric) \| measure: fragment–protein ipTM score \| mark: box (whiskers + mean diamond) \| n: NOT REPORTED per box` | 2 facets × 2 boxes. | n per box never stated. Otherwise this is the best-constructed panel in the paper: it shows the overlap rather than asserting it, which is exactly what the claim needs. | as above |
| 4 | p11 | ABFE of the Boltz allosteric pose vs the crystal pose for 30 fragment–kinase complexes. | bar | `PLOT \| facet: kinase (5, laid out on two stacked axes: AKT2/CDK2/CHEK1/CSNK2A1 above, MAPK14 below) \| vary: fragment ID (30) \| series: pose source (2: Boltz allosteric pose, crystal pose) \| measure: ΔG_bind (kcal/mol) \| mark: bar + point (bars = Boltz pose with error bars, diamonds = crystal pose) \| n: 1 ABFE per mark; per panel AKT2 3, CDK2 1, CHEK1 4, CSNK2A1 10, MAPK14 12` | 30 fragment positions grouped into 5 kinase groups across 2 axes; groups vary by system. | **The crystal-pose diamonds carry no uncertainty at all** while the Boltz bars carry error bars, so the headline "equal or better for 21 of 30" is a comparison of error-barred bars against unquantified point estimates. Per-kinase n is recoverable only by counting bars (CDK2 is a single bar). Fragments are labelled by numeric suffix only, resolvable solely via Supplementary Table S1, which is not held. | as above |
| 5A.i–A.iii | p13 | CDK-A017 (PDB 8VQ3) on CDK2: reference ligands with predicted pocket surfaces; the unblocked orthosteric pose; the ADP-blocked cryptic pose. | structure render | `RENDER \| facet: pose condition (3: references + pocket surfaces, unblocked pose, ADP-blocked pose) \| views: 1 \| overlay: NOT REPORTED predictions on 1 reference (crystal-native CDK-A017) \| axis: none` | 3 renders sharing one legend (three pocket surfaces + four ligand colours). | One representative pose per condition out of 10 samples, **selection rule NOT REPORTED**. The three ΔG values that carry the panel's whole claim (−3.42 / +1.42 / −0.36 kcal/mol) are printed as caption text with no error bars and no quantitative panel. | as above |
| 5B | p13 | Cryptic exploration rate under no blocker, ADP alone, and ADP + parent allosteric ligand, per kinase. | bar | `PLOT \| facet: kinase (5) \| vary: blocking condition (3: no blocker, ADP, double blocker) \| series: blocking condition (3, colour carries the same variable) \| measure: cryptic exploration rate (% of samples localized to neither orthosteric nor allosteric sites) \| mark: bar (SEM error bars) \| n: per panel AKT2 15, CDK2 38, CHEK1 19, CSNK2A1 11, MAPK14 33 fragments × 10 samples; printed on each panel header` | 5 panels, one per kinase; n printed per panel header. | MAPK14's 24.5% → 37.6% is claimed in the text as a substantial increase (p14) with **visibly overlapping SEM bars and no statistical test reported anywhere**. CDK2's 97.9% / 96.3% pair sits at the ceiling, so the double-blocker comparison is uninformative there by construction — cross-ref `metric_saturation`. | as above |
| 6A | p15 | The prospective screening funnel: Screen (Enamine library → co-fold with ADP) → Validate (non-orthosteric filter, ΔG ≤ −1 kcal/mol) → Downselect (re-fold without ADP, paired-ABFE selectivity, anchor candidates). | schematic | `SCHEMATIC \| three-stage screening funnel with an inset cartoon of the paired allosteric/cryptic-vs-orthosteric ABFE comparison \| no data` | One flow diagram with 6 stages bracketed into 3 phases, plus an inset. | The ΔG ≤ −1 kcal/mol hit threshold appears here as a box in a flowchart and is **never justified in the text**. | as above |
| 6B-top | p15 | Per-kinase localization rate of Enamine fragments across the three site classes. | bar | `PLOT \| facet: kinase (5) \| vary: pocket assignment (3: orthosteric, allosteric, cryptic) \| series: pocket assignment (3, colour carries the same variable) \| measure: pocket localization rate (%) \| mark: bar (error bars) \| n: NOT REPORTED per bar` | Top half of panel B; 5 facets. Panel letter B appears in two rows (this and the next) because top and bottom differ in both mark and measure. | **No n on any bar and none in the caption** — the reader cannot tell whether a bar rests on 300 fragments, on the 107 retained, or on the 33 hits. Error-bar definition unstated. | as above |
| 6B-bottom | p15 | PLIP interaction counts for the same fragments by site class. | box | `PLOT \| facet: kinase (5) \| vary: pocket assignment (3: orthosteric, allosteric, cryptic) \| series: pocket assignment (3) \| measure: number of PLIP protein–ligand interactions \| mark: box (whiskers + mean diamond) \| n: NOT REPORTED per box` | Bottom half of panel B; 5 facets. See note above on the split. | n per box never stated. The panel is used to justify the PLIP-based ranking that drives down-selection, but no threshold or decision rule is shown on it. | as above |
| 6C | p15 | Six CHEK1 Enamine fragments engaging the allosteric (pink) and cryptic (purple) pockets, with the ADP blocker in the orthosteric pocket (blue). | structure render | `RENDER \| facet: none (1) \| views: 1 \| overlay: 6 fragment poses + 1 blocker on 1 receptor \| axis: none` | Single render, 6 fragments co-displayed on one CHEK1 surface. | Six fragments are shown simultaneously on one receptor, which reads as a co-occupancy that was never predicted — each was co-folded separately. Which of the 10 samples per fragment is drawn is not stated. | as above |

## G. Provenance

| Field | Value |
|---|---|
| `extracted_on` | 2026-09-07 |
| `extractor` | claude subagent (Opus 5), single-paper extraction session, 2026-09-08 run |
| `schema_version` | `v3` |
| `confidence` | **high** on identity, protocol, the blocker mechanism, oracle routes, claims and figure structure — §2.3 (p5) is short and unusually explicit about exactly what is added to the input, and the reversion control (p15–16) is stated unambiguously. **high** on the localization percentages, which are printed both in Table 1 and on the figure panels. **medium** on two things: (i) the ABFE numbers, because every per-complex value lives in Supplementary Table S4/S6 and only four ΔG values appear in the main text; (ii) the PTP1B rates, because text and table disagree (see below). **medium-low** on template handling, which is simply never stated. Five pages (8, 10, 11, 13, 15) were rendered at 150 dpi to read panel marks and per-panel n where the captions did not carry them; renders were deleted afterwards. |
| `unresolved` | 1. **PTP1B numbers contradict between text and table.** Text: "For PTP1B, introducing a phosphotyrosine-containing peptide blocker elevated non-orthosteric exploration from 50.4% to 96.2%" (p7). Table 1: 55.7% → 99.6% (p6). Same arm, same n = 23. Neither is flagged; there is no second PTP1B condition that could explain the gap. Any PTP1B number quoted from this paper must cite which of the two it is. <br>2. **The Discussion reverses the sign of the confidence result.** Results and Fig 3C: allosteric ipTM > orthosteric ipTM (0.945 vs 0.907 unblocked; 0.959 vs 0.896 blocked, p9). Discussion: "orthosterically-localized samples consistently received higher confidence scores than allosterically-localized ones" (p16), and the practitioner warning is built on that reversed claim. The *conclusion* (confidence cannot discriminate) survives either way, because the distributions overlap; the *direction* stated in the Discussion is not supported by the paper's own numbers. <br>3. **Templates never mentioned.** The input specification (p5) names sequence, MSA and SMILES only. If Boltz-2's default template retrieval was on, oracle route 1 has a second, larger channel. Not resolvable from the PDF; would need the GitHub YAMLs. <br>4. **Boltz-2's training cutoff is never stated**, so "memorization" is asserted throughout without any date being attached to it, and no post-cutoff arm exists. <br>5. **Supplementary Table S5 is cited for two different things**: the Boltz-2 global confidence metric (p9) and the INX-315 CDK2/CDK6 selectivity results (p12). One of the two citations is probably a mislabel; SI not held, so unresolvable. <br>6. **PDB ID inconsistency for a KRAS reference**: "5V71" in the allosteric reference list (p4) vs "5V7I" in the parent-ligand list (p4). 5V7I is the plausible reading. <br>7. **PTP1B parent-ligand list is internally short**: "seven allosteric ligands were curated (1T49/892, 1T4J/FRJ, 7GSA/FM0260, 7GTQ/S7S, 8G65/DES4799, 8G65 and 8G69)" (p4) — 8G65 appears twice and 8G68, listed among the allosteric references, is absent, so only six distinct PDB IDs are named where seven ligands are claimed. <br>8. **Figures 1 and 6 carry the identical caption title** ("The CAFE prospective screening workflow and pocket-selective fragment recovery", p3 and p15) though they depict different things. <br>9. **Cross-reference for the CDK2 surface-exploration claim looks mislabelled**: Supplementary Figure S2 is introduced as fragment-to-orthosteric-pocket distance distributions (p7) but is then cited for CDK2 fragments populating "unannotated surface regions or cryptic pockets" (p9). <br>10. **Tag gap — no `directed-site` in the v3 vocabulary.** CAFE is directable, but over *binding site*, not conformational state. `directed-state` was deliberately **not** applied (see tag notes) because applying it would false-positive every conformational-steering query, and there is no site-level equivalent. This is the one tag I needed and could not use. <br>11. **`method_class` has no vocabulary entry for "co-input / competitive-occupant blocking"**, which is this paper's actual contribution. It is recorded as `cofolding` because the intervention is on the co-folding input, but a query for inference-time input interventions will not find it by tag. `latent-steering` is explicitly wrong here (no internal tensor is touched). |
| `why_it_matters` | |

## Tags

`kinase` `general-protein` `cofolding` `md` `ensemble` `single-state`
`binary-predicate` `continuous-metric` `saturating-metric` `oracle-leak`
`design-level-oracle` `no-anti-memorization` `unpowered`
`confidence-as-discriminator` `ligand-driven` `orthosteric` `allosteric-site`
`cryptic-pocket` `allosteric-failure` `preprint` `precedent` `contrast`
`negative-result` `comparator-numbers`

**Tag notes — why each was applied, and what was deliberately withheld.**

- `kinase` + `general-protein`: five human **protein** kinases carry the whole paper (p3),
  which is squarely inside the v3 scoping of `kinase`. `general-protein` covers PTP1B (a
  protein tyrosine phosphatase) and KRAS (a small GTPase) (p4) — neither is a GPCR,
  transporter, periplasmic-binding protein or ATPase, and neither warrants its own tag.
  **`fold-switching` not applied**: no metamorphic behaviour is studied or claimed.
- `cofolding`: the method is an intervention on a co-folding model's input, and the model
  is Boltz-2 (p5). **`latent-steering` deliberately not applied** — v3 scopes it to
  inference-time intervention on an *internal tensor*, and CAFE touches nothing internal;
  it adds a chain. **`template-state-bias` and `msa-state-filter` not applied**: no
  template is supplied and the MSA is a held-constant control (p5). **`benchmark-only`
  not applied**: this paper proposes a protocol, it does not merely evaluate.
- `md`: the validation layer is genuine explicit-solvent alchemical MD — double-decoupling
  ABFE, 16 λ windows, 5 ns legs, MBAR (p6) — and a reverse lookup for MD-based validation
  should return this paper. Note for the reader: MD here is a *scoring* layer applied to
  co-folded poses, not a conformational sampling method, so it is not evidence of MD-based
  state generation. **`enhanced-sampling` not applied** (no metadynamics, no replica
  exchange); **`md-emulator` not applied** (no generative model trained on trajectories);
  **`experimental` not applied** (no wet-lab work of any kind).
- `ensemble` + `single-state`: the v3-sanctioned pair. Ten diffusion samples per fragment
  per condition (p5) is an ensemble; without a blocker it collapses onto the single
  orthosteric basin (5.7% / 17.6% non-orthosteric, p7; 16 of 33 hits at 10/10 orthosteric,
  p15–16). Flagged in `states_generated` that the ensemble is over **ligand placements**,
  not protein conformations, so a state-sampling query is not misled.
- `binary-predicate` + `continuous-metric`: the 5.0 Å localization predicate (p5) is the
  primary metric; the RMSD distribution (Fig 3B), COM distances, ipTM scores and ΔG values
  are genuine continuous axes. **`rmsd-only` deliberately not applied** — RMSD is
  secondary here, and the tag would misdescribe a paper whose main metric is a distance
  predicate on a *ligand centroid*, not a structural RMSD. **`visual-metric` deliberately
  not applied**: the renders illustrate conclusions the predicate already established;
  no claim in this paper is called by eye.
- `saturating-metric`: real numeric ceiling, not an axis artefact. Four of seven targets
  reach exactly 100.0% and two more reach 99.6–99.7% in the blocked arm (Table 1, p6), and
  the authors concede saturation in the cryptic arm — "cryptic sampling is already
  saturated under ADP alone" (Fig 5 caption, p13). See `metric_saturation`.
- `oracle-leak`: routes 1, 5 and 6 (see the route table). Route 1 is the distinctive one
  and the reason this tag is applied rather than only `design-level-oracle`: **the blocker
  is a known orthosteric binder of the target**, taken from that target's own deposited
  co-crystal for the type-I, PTP1B, KRAS and double-blocker arms (p4, p5, p14). What
  crosses into the pipeline is chemical identity, not coordinates — worth remembering when
  quoting this, because it is a weaker form of leakage than template injection, but it is
  still knowledge of the answer entering the input.
- `design-level-oracle`: route 7, kept distinct as v3 requires. Targets chosen because
  their allosteric co-crystals exist (p3); fragments cut from those same co-crystal ligands
  (p4). The Enamine and cryptic-pocket arms are the two places this does *not* apply.
- `no-anti-memorization`: applied without hesitation, and it is the sharpest rigour finding
  in the note. The paper's central subject is memorization, and it contains **no date
  filter, no training-overlap analysis, no post-cutoff arm and no statement of Boltz-2's
  training cutoff**. The coverage stratification (p3) is an ordinal proxy, never
  quantified. `anti-memorization` would be flatly wrong here.
- `unpowered`: scoped, and the scope matters. The **localization screen is well powered**
  (thousands of samples). The tag is applied for the **thermodynamic arms**: CDK2 n = 1,
  AKT2 n = 3, CHEK1 n = 4 (p11), the trapped-fragment comparison n = 10 (p12), and the
  14-cluster cryptic inventory (p12). Several per-target conclusions rest on single-digit n.
- `confidence-as-discriminator`: applied because the paper **tests** ipTM as a placement
  discriminator and reports the result (p9, Fig 3C p10) — a reverse lookup on this tag
  should surface it. Read the field, not just the tag: the finding is **negative and
  useful** — confidence does not discriminate, the distributions "overlap almost entirely",
  and the authors conclude it "cannot substitute for explicit geometric localization
  scoring" (p9). This paper is evidence *against* the practice, not an instance of it.
- `ligand-driven`: the steering handle is a small-molecule co-input in every arm but one
  (ADP, type-I inhibitors, GDP, the parent allosteric ligand). **`peptide-driven`
  deliberately not applied** although the PTP1B blocker is the DADEpYL hexapeptide (p5):
  in this corpus that tag denotes a peptide partner driving *conformational* selection,
  and one blocker in one single-target arm does not justify the false positives.
  **`partner-driven`, `g-protein-mimetic`, `nanobody` not applied** — no protein partner
  is co-folded. **`apo-sampling` not applied**: the unblocked arm is protein + fragment,
  never apo. **`seed-only` not applied**: seeds are not the handle; the blocker is.
  **`directed-state` deliberately not applied, and this is the note's one tag gap** — CAFE
  *is* directable, but it directs **binding site**, not conformational state, and it does
  so by exclusion ("go anywhere but here") rather than by specification. Tagging it
  `directed-state` would return this paper for every conformational-steering query, which
  is exactly the drift the fixed vocabulary exists to prevent. Recorded in `unresolved`
  as a request for a `directed-site` tag.
- Protocol tags: **none applied.** `templates-on` cannot be applied because templates are
  never mentioned (p5); `no-template-no-msa` is wrong because an MSA is used;
  `state-annotated-input` is wrong because the Modi–Dunbrack curated set (p4) selects which
  ligands get fragmented and is never fed to the model. Leaving all three off is the honest
  position and is recorded in `templates`.
- `orthosteric` + `allosteric-site` + `cryptic-pocket`: **what was studied**, all three
  substantively rather than in passing. Orthosteric: the reference site, the blocked site,
  and the subject of the memorization finding. Allosteric: 24 kinase + 10 non-kinase
  deposited allosteric complexes define the target sites (p3–4) and §3.2 is entirely about
  them. Cryptic: §3.4 is a cryptic-pocket discovery section with 14 DBSCAN clusters, a
  P2Rank/FPocket comparison, a dedicated double-blocker arm and two ABFE case studies
  (p12–14).
- `allosteric-failure`: **applied deliberately, and scoped — read this note before using
  it.** The v3 definition is "the *result* that no model or setting ever sampled the
  allosteric site". That holds here in two precise senses, and fails in a third. (i) **Per
  target, under every setting tested: CDK2.** Canonical allosteric localization is 0.0%
  unblocked and 1.3% with ADP (Fig 3A, p10) — "Strikingly, CDK2 yielded near-zero canonical
  allosteric localization under both conditions despite achieving near-complete escape from
  the orthosteric site." (p9). No blocking condition rescued it, and CDK2 contributed n = 1
  to the ABFE panel because of it (p11–12). (ii) **Panel-wide, in the default regime**,
  which is the paper's premise: unblocked, fragments essentially never reach allosteric
  sites for AKT2/CDK2/CHEK1/MAPK14, and 94.3% of orthosteric-derived samples stay in the
  ATP pocket (p7). That default failure is the whole reason the paper exists. (iii) **It
  does NOT hold for the paper's headline result**: with ADP, four of five kinases do reach
  their canonical allosteric sites (AKT2 93.3%, CSNK2A1 100.0%, MAPK14 44.5%, CHEK1 37.9%,
  Fig 3A p10). Anyone retrieving this paper via this tag must take the scope from here,
  not from the tag alone.
- `preprint`: bioRxiv, "(which was not certified by peer review)" (p1). No journal
  destination named. **`peer-reviewed` not applied.**
- `precedent` + `contrast`: both, per `stance`, and provisional pending the user's call.
- `negative-result`: applied for the paper's first half — the demonstration that fragment
  chemistry alone routes molecules to the orthosteric site (Spearman ρ ≥ 0.330, p < 0.0001,
  p7; N > 2 fragments at 6.2% vs 21.9% non-orthosteric, p7; 16 of 33 hits at 10/10
  orthosteric on blocker removal, p15–16) and for the ipTM discriminator failure (p9).
  Both are clean negatives about co-folding models, reported as such. The paper as a whole
  is a positive method paper, so this tag marks a component, not the conclusion.
- `comparator-numbers`: the localization percentages (Table 1 p6, Fig 3A/5B panel labels
  p10/p13) and the ABFE distributions (Fig 4 p11, four ΔG values in text) are directly
  quotable comparators — with the caveat in `si_in_scope` that no per-complex ABFE value
  is recoverable from the held PDF. **`figure-exemplar` not applied**: the figures are
  serviceable, not exemplary, and the tag would exclude the paper from gap analysis, which
  would be wrong for a paper this close to our own mechanism.
- **`multi-backbone`, `prospective`, `experimental-validation` deliberately not applied.**
  `multi-backbone`: Boltz-2 alone; model-agnosticism is asserted "in principle" (p17) and
  never tested. `prospective`: the field is `partial`, and the tag is binary — targets,
  blockers and success criteria are all retrospective, so applying it would overstate what
  the Enamine arm establishes. `experimental-validation`: no NMR, no crystallography, no
  assay; ABFE is computational validation, and conflating the two would destroy the tag's
  value as a distinguishing feature.
