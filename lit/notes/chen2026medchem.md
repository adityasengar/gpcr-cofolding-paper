# chen2026medchem

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–54); the preprint has no separate
printed page numbering, so these are the only page numbers that exist.** Layout: p1 title/affiliations,
p2 abstract, p3–4 Introduction, p4–6 Results preamble + metric definitions, p6–10 §1 sEH, p10–16 §2
canonical orthosteric/kinases (2.1 pose recovery, 2.2 DFG/αC states, 2.3 coregulator recruitment,
2.4 pseudo-symmetry), p16–19 §3 allosteric, p19–21 §4 PPI, p21–23 §5 PROTAC, p23–25 §6 molecular glue,
p25–28 §7 covalent, p28–29 §8 membrane protein, p29–31 §9 RNA, p31–33 §10 fragments, p33–36 §11
confidence metrics, p36–38 §12 activity ranking, p38–40 **§13 activity cliff**, p40–43 §14 practical
chemical issues, p43–44 Perspective and Conclusion, p44–46 Experimental Section, p46–47 Supporting
Information + PDB ID codes, p47–49 author info + abbreviations, p50–54 references (86 entries).
Figures 1–19 at pages 5, 7(+8), 9, 13, 15, 16, 18, 20, 22, 24, 27, 29, 30, 32, 35, 37, 38, 39, 42.
**No main-text tables.** Tables S1–S13 and Figures S1–S28 are cited throughout but are NOT in this PDF.

---

## A. Identity

| Field | Value |
|---|---|
| `citekey` | `chen2026medchem` |
| `doi` | `10.64898/2026.08.24.746785` (bioRxiv, p1). bioRxiv version posted **August 26, 2026** (p1 banner). |
| `year` | 2026 |
| `venue` | **bioRxiv preprint**, explicitly "not certified by peer review" (p1 banner). Tagged `preprint`. Formatting (Experimental Section, PDB ID Codes, Author Information, Abbreviations, ACS reference style) indicates submission to an ACS medicinal-chemistry journal, but no journal is named. |
| `title` | "A Medicinal Chemistry-Centered Evaluation of AlphaFold 3 and Boltz-2 Across Diverse Binding Modalities" (p1) |
| `authors` | Ke Chen, Zuohuang Qi (equal first), Omar Lozano Ramos, Huayu Li, Mengjiao Ma, Malla Reddy Gannarapu, Fangchao Bi, Ao Li, Hongmin Li, Rui Xiong. University of Arizona (Pharmacology & Toxicology / ECE / Chemistry & Biochemistry / BIO5 / MCB). Corresponding: Rui Xiong, Hongmin Li, Ao Li (p1, p47). |

---

## B. Scope

| Field | Value |
|---|---|
| `system` | **Mixed / general protein**, deliberately spanning modality classes rather than a protein family. Contains protein kinases (JAK2, TYK2 JH2, BRAF, EGFR, ERK2, Hck, p38α, Aurora A, CDK2), a phosphodiesterase (PDE4D), a nuclear receptor (PPARα), viral proteases (SARS-CoV-2 PLpro, Mpro), an epoxide hydrolase (sEH/EPHX2), a helicase (WRN), a phosphatase (SHP2), GTPases (KRAS, NRAS, Rac1), E3 machinery (CRBN/DDB1, VHL/elongin), **three membrane transporters** (MCT8, OATP1B1, GAT3), and **six RNA targets**. **No GPCR.** |
| `n_targets` | **95 indexed entries** in total (entry index 1–95, listed exhaustively p46–47). Of these, **entries 1–6 are the six newly determined in-house sEH co-crystals** (undeposited) and 7–95 are deposited PDB entries. **83 complexes** carry the AF3/Boltz-2 confidence analysis (p33). Distinct *proteins* is far smaller than 95 — e.g. entries 64–73 are ten SARS-CoV-2 Mpro fragment complexes and 76–95 are twenty Mpro affinity complexes, so Mpro alone accounts for ~32 of the 95 entries. **The paper never states a distinct-protein count.** See the modality breakdown table under E for per-class n. |
| `method_class` | **benchmark-only.** Off-the-shelf inference with two co-folding backbones, no method development. "No modifications were made to the model architecture, pretrained weights, or inference code." (p44) |
| `backbones` | **AF3 v3.0.1** and **Boltz-2 v2.2.0**, locally installed official GitHub implementations with released pretrained weights (p44). **Exactly two**, compared head to head — so per the v3 tag rule (`multi-backbone` requires *more than two*) this paper is **not** tagged `multi-backbone`. AF3 is the primary reporting model throughout the main text; Boltz-2 per-entry distributions are relegated to Figures S1–S10 (not in this PDF). |
| `templates` | **NOT REPORTED.** The Experimental Section says only "Unless otherwise stated, default data-processing and inference settings were used" (p44). Template usage is never named, and — critically for a post-cutoff benchmark — **the paper never states whether any structural-template database search was date-restricted to before the 30 September 2021 cutoff.** See `oracle_leakage` route 1. |
| `msa_handling` | **NOT REPORTED** — defaults implied by "default data-processing and inference settings" (p44). No subsampling, no clustering, no state filtering, no MSA depth is mentioned anywhere. |

---

## C. Conformational core

| Field | Value |
|---|---|
| `states_generated` | **ensemble + single-state** (dual, and the dual is the point). *Ensemble*: 10 structural predictions per complex per model, displayed as per-entry violin distributions (p44; Figs 2D, 4A–C, 7A–C, 8A–C, 9A–C, 10A–C, 11A–C, 12A–C, 13A–C, 14A–C). *Single-state*: each ligand input is asked for **one** ligand-associated protein conformation, and the result is scored against **one** reference; the paper never asks a model to produce two protein states of the same target, never enumerates alternative states, and treats within-run spread as pose *variability* rather than as an ensemble over states. The paper's own framing of spread is variance to be reduced: AF3 showed "lower pose variability" and "relatively narrow violin plot distributions" (p14), read as a virtue. |
| `structural_priors_used` | Extensive, and mostly legitimate design-time use rather than pipeline leakage. (1) **Six in-house sEH co-crystal structures they solved themselves**, used as the ground truth for entries 1–6 (p8, refs 22–23 "To be published"). (2) **Deposited PDB structures** for entries 7–95, chosen as references and, in every modality section, chosen *because* the structural literature already describes the binding mode ("In 7, Gandotinib **was reported** to bind the ATP site of JAK2 and stabilize a canonical DFG-in/αC helix-in active state…", p12). (3) **Pharmacophore atom sets defined from the experimental complex**: "Pharmacophore-specific RMSD was calculated using ligand atoms preferentially selected based on key recognition interactions identified from the experimental complex and relevant structural literature." (p45–46). (4) A **mechanistic 2D interaction model** for sEH substrate recognition built from prior sEH structures (Fig 2C, p7), used as the reference geometry for judging inhibitor poses. (5) **Endogenous PPI reference structures** overlaid to define the interface (KRAS 7KFZ, Nrf2 EAGE peptide 5WG1, TPX2 peptide 4C3P, Rac1 1HH4; Fig 8 caption p20–21). Items 1, 2 and 5 are legitimate priors for a benchmark; item 3 is a prior that also constitutes metric-definition leakage (see route 5). |
| `oracle_leakage` | Enumerated per route below. |

**`oracle_leakage`, route by route:**

**Route 1 — deposited structures as input or template.** **NOT DETERMINABLE, and this is the paper's
most serious protocol gap.** The full input specification is on p44–45: "Protein, peptide, and RNA
components were supplied as separate polymer chains, and small-molecule ligands were specified using
SMILES strings, CCD identifiers, or user-defined CCD components, as appropriate. Where applicable,
covalent linkages were explicitly defined using bonded atom pairs in AF3 and bond constraints in
Boltz-2." (p45). No reference structure is fed in as coordinates. **But** the only statement about
everything else is "Unless otherwise stated, default data-processing and inference settings were used"
(p44), and the paper never says whether template search was enabled, nor whether any template or MSA
database was truncated at the stated 30 September 2021 cutoff. A post-cutoff *evaluation set* with an
un-date-restricted *template database* would leak the answer for every entry whose target has close
homologues deposited after the cutoff. **The claim that entries are "outside the AF3 training set"
(p6) is therefore about the weights only, not about the inference-time inputs.** Recorded as
NOT REPORTED, not as NONE FOUND, because the protocol as written cannot rule it in or out.

**Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates or
alignments.** **NONE FOUND.** No conformational-state database is named anywhere in the paper. The
DFG/αC state descriptions on p11–12 are taken from the primary literature for each complex, not from
a state-annotated database, and they drive *narration*, not inputs. Protocol described at p44–45.

**Route 3 — cluster labels derived from known states.** **NONE FOUND.** No clustering of any kind is
performed; the 10 predictions per complex are analysed as a raw distribution (Fig 2D, 4A–C etc.).
Protocol at p44 and the analysis methods at p45–46.

**Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states.**
**PRESENT, in the metric rather than the model.** The model side is clean: fixed seeds 10 and 42,
five predictions each, defaults, no per-target tuning ("For AF3, random seeds 10 and 42 were used,
with five structural predictions generated per seed, yielding 10 predictions per complex", p44). The
*evaluation* side is not: the minPAE bin edges that carry the paper's headline triage claim were
chosen after inspecting the evaluation set — "Because the correlations between confidence scores and
pose accuracy were not uniform across the dataset, **we next grouped minPAE and ipTM values into
score ranges to determine whether particular ranges were enriched for accurate poses**" (p33). The
resulting boundary is then promoted to a recommendation: "AF3 minPAE was the most useful metric
examined, with minPAE <0.85 Å strongly enriching for accurate pose and pharmacophore recovery."
(p36) and again in the abstract, "very low minPAE values (<0.85 Å) were strongly enriched for
accurate poses" (p2). Under the v3 rule, **tuning a range on the evaluation set is leakage even where
no per-target value is picked** — and 0.85 Å is an unusual, clearly data-derived boundary. There is no
held-out split on which the 0.85 Å threshold is re-tested.

**Route 5 — success defined post hoc by RMSD or TM to a structure they had.** **PRESENT, by
construction, and additionally in the choice of scored atoms.** Every success/failure call in the
paper is an RMSD, pharmacophore RMSD or volume overlap against the reference the authors held:
"We defined chemically useful poses as those with an overall RMSD ≤ 2 Å, a pharmacophore RMSD ≤ 1.5
Å, and a volume overlap ≥ 70%." (p4). That much is unavoidable and normal for a benchmark. What is
*not* normal is that the pharmacophore metric's atom set is itself selected from the answer:
"Pharmacophore-specific RMSD was calculated using ligand atoms preferentially selected based on key
recognition interactions identified from the experimental complex and relevant structural literature.
RMSD was restricted to these predefined pharmacophore atoms" (p45–46). The paper's second headline
result — "Pharmacophore RMSD was often lower than overall ligand RMSD, indicating preservation of key
recognition features despite imperfect whole-ligand alignment" (p2) — is therefore measured on a
subset of atoms chosen, per ligand, from the reference structure. No blinded or automated
pharmacophore-perception alternative is reported. Also route-5-adjacent: for symmetric ligands the
success criterion is *relaxed* post hoc — "For symmetric or pseudosymmetric ligands, only a
pharmacophore RMSD ≤ 1.5 Å and a volume overlap ≥ 70% were required" (p4) — with symmetry status
assigned by the authors on inspection of each case (worked through for PLpro entry 24, p15–16).

**Route 6 — best/worst model labels assigned against a held reference.** **PRESENT but limited.** The
primary per-entry statistic is the distribution of all 10 poses, not a cherry-picked best, and medians
are reported ("the median RMSD across 10 generated poses for each complex was generally within 2 Å",
p10) — good practice. However the representative structural overlays that carry the qualitative claims
are single models selected against the reference with no stated selection rule: Figs 3A–F, 4D–G, 7D–I,
8D–G, 9D–G, 10G–I, 11D–I, 13D–F, 14D, 18C–D all show "Predicted structure" as one model, and no
caption states which of the 10 it is or how it was chosen. The DFG/αC state claim (p12) rests
entirely on four such unlabelled single overlays.

**Route 7 — design-level oracle use (systems or conditions chosen because the expected answer is
already known).** **PRESENT throughout, and it is the dominant leakage mode of this paper. Weaker
than pipeline leakage, and labelled here as design-level.** The expected answer is declared before the
result is read in every conformational and activity-cliff claim:
- Kinase states (p12): "In 7, Gandotinib was reported to bind the ATP site of JAK2 and stabilize a
  canonical DFG-in/αC helix-in active state with an intact regulatory salt bridge, **providing a test
  of whether the models recover** both standard Type I ligand placement and the associated fully
  active kinase conformation." Same construction for entries 14, 19 and 21 in the same paragraph.
- Activity cliff (p38): "S-Thalidomide is a well-characterized CRBN ligand and **is likely represented
  in the structural training landscape**, and both models accurately reproduced its CRBN-bound pose."
- Activity cliff (p38–39): "N-methyl-S-thalidomide was included as a near-analog negative control
  **because glutarimide N-methylation is expected to disrupt productive CRBN engagement**." and
  (p39) "The expected outcome for N-methyl-S-thalidomide is therefore loss of productive binding."
- PROTAC failure explained by training representation without testing it (p22): "Boltz-2 … was able to
  recover the individual KRAS- and VHL-binding ligands, **likely because Switch II pocket-binding KRAS
  ligand structures are represented in the training data**."
These are honest statements of prior expectation, not hidden inputs; but the four DFG/αC "successes"
and the activity-cliff arm are both cases where the answer was announced in the same paragraph that
declares the test.

| Field | Value |
|---|---|
| `prospective` | **partial.** *Prospective* for entries 1–6: six sEH co-crystals solved in house, not deposited at the time of writing ("PDB accession codes for the six newly determined sEH complexes (1–6) will be provided upon deposition", p47), so they cannot be in any training set or template database, and the matched IC50 assays are the authors' own. *Retrospective* for entries 7–95: all are deposited PDB entries, selected after deposition, with the binding mode described in the cited primary literature before the prediction was run. *Retrospective and design-level-oracled* for the conformational-state and activity-cliff arms (route 7). The paper's own framing is "post-training-cutoff" (p2), which is a weaker property than prospective and the paper does not conflate the two. |
| `state_metric` | **RMSD-to-reference + visual only** (dual, and the visual half is where the conformational claim lives). Quantitative: overall heavy-atom RMSD after protein alignment, pharmacophore-restricted RMSD, and RDKit shape-Tanimoto-derived volume overlap, with hard predicates 2 Å / 1.5 Å / 70% (p4, p45–46). **These all score the *ligand*.** The **protein conformational state is never scored at all**: the DFG-in/DFG-out and αC-in/αC-out calls in §2.2 are made by eye from four overlay renders with arrows drawn on them (Fig 4D–G, p13) — no dihedral, no Cα distance, no salt-bridge distance, no Kincore/KLIFS label, no RMSD over the DFG motif or the αC helix, no threshold, and no number of any kind. The verbatim claim (p12) is "AF3 and Boltz-2 were particularly effective in these cases, **accurately recovering** not only the ligand poses but also the associated kinase conformational features, including DFG-loop organization, αC-helix positioning (pink parts), and activation-loop arrangement" — "accurately" is not operationalised anywhere in the paper. Thresholds that *are* stated (2 Å, 1.5 Å, 70%) are given without justification beyond "predefined" (Fig 4 caption, p13); the 0.85 Å minPAE boundary is stated but was data-derived (route 4). |
| `metric_saturation` | **Yes, numerically, in three places.** (1) **Volume overlap is bounded at 100% and ceilings**: across canonical orthosteric entries it "remained relatively high across most complexes even when overall RMSD increased" (p11), and in Fig 4C most violins sit in the 85–100% band against a 70% threshold — the metric cannot discriminate among good poses. (2) **Pharmacophore RMSD floors near 0 Å** for the well-predicted classes (Fig 4B; Fig 16B lists 0.30, 0.49, 0.84 Å for sEH ligands 1–3, p37), so the ≤1.5 Å predicate is passed with large headroom and cannot rank. (3) **The headline enrichment statistic ceilings**: "100% (22/22) for minPAE <0.85 Å" (p33) — a perfect cell that cannot go higher and whose confidence interval the paper never gives. Axis-scale problems (the 0–40 Å and 0–50 Å RMSD axes that compress the 2 Å threshold line onto the baseline, and the dual left/right axis in Fig 2D) are **figure** defects and are recorded in `hides` on the relevant figure rows, not here. |
| `directional_control` | **Yes, by ligand identity only — and this is the paper's one real state-control result.** The only handle is the co-folded ligand: the same kinase fold is driven to different regulatory conformations by which inhibitor is supplied, e.g. gandotinib → DFG-in/αC-in for JAK2 (7), the paradox-breaker TXV → "a rare DFG-out/αC-helix-in conformation" for BRAF V600E (14), A-419259 → "DFG-in/αC-helix-out state with an extended activation loop" for Hck (19), BIRB796 → inhibitor-associated activation-loop conformation for dual-phosphorylated p38α (21) (all p12; Fig 4D–G, p13). No other handle exists: no partner protein toggle, no nanobody, no G-protein mimetic, no state-annotated template, no state-filtered MSA, no subsample-depth sweep, no seed sweep (seeds are fixed at 10 and 42, p44). Peptide coregulator partners are supplied for PPARα entries 22–23 but as part of the reference complex, not as a state instruction. The paper contrasts this ligand handle favourably with docking: "This ability to generate ligand-bound protein conformations highlights a key strength of diffusion-based structure prediction relative to traditional rigid-receptor docking, where the protein conformation is usually fixed or only locally relaxed." (p12) |
| `anti_memorization_design` | **Yes for the deposited set, plus a genuinely undeposited arm — but with named exceptions and one undocumented risk.** Verbatim (p6): "The structures were selected from entries released after **September 30, 2021**, to ensure they were outside the AF3 training set." Counts: **89 deposited entries (7–95)** nominally post-cutoff, plus **6 undeposited in-house sEH structures (1–6)** that are outside any training set by construction. **Cutoff caveats, all internal to the paper:** (a) the cutoff is stated for **AF3 only** — Boltz-2's training cutoff is never given, anywhere, despite Boltz-2 being half the paper; (b) at least four structures used in the paper are **pre-cutoff and are used as evidence**: 4CI1 (the CRBN/S-thalidomide reference for the entire activity-cliff arm, entries 74–75), 1W6K, 4AV4 and 7X1T (the chirality/alkene/alkyne/ring-geometry error examples, Fig 19A–D, p40–41, p42); (c) the paper itself twice states that the answer is in the training data for specific entries — "likely because Switch II pocket-binding KRAS ligand structures are represented in the training data" (p22) and "S-Thalidomide … is likely represented in the structural training landscape" (p38); (d) the release date of the large `7G*` group depositions (entries 64–72 Mpro fragments; entries 76–95 Mpro affinity set — 32 of the 95 entries) is never stated and is not checkable from the PDF; (e) as noted in route 1, **no template or MSA database date restriction is described**, so weight-level anti-memorization is not matched by input-level anti-memorization. |
| `anti_memorization_control` | **NONE RUN as a formal arm — and this is the paper's largest missed opportunity.** The post-cutoff set exists and is used as the *whole* evaluation set; there is no matched pre-cutoff comparison arm anywhere. The paper had exactly the material for one — six undeposited structures, a set of nominally post-cutoff entries, and at least four explicitly pre-cutoff/likely-memorized entries — and never contrasts them quantitatively. Instead, memorization is invoked *post hoc* as an explanation for individual successes and failures (p22, p38) without being measured. The nearest thing to a control is the modality-wise minPAE breakdown (p34, Fig S22, not in this PDF), which is a modality comparison and not a memorization comparison. **Additionally mark `UNPOWERED` for most modality classes:** activity cliff n = **1 pair**, PROTAC ternary complexes n = **2**, membrane proteins n = **3**, molecular glues n = **5**, covalent n = **5** (7 with cross-referenced entries), allosteric n = **6**, RNA n = **6**, sEH n = **6** — all far below the ~10 threshold. Only the canonical orthosteric class (n = 19), the fragment class (n = 10) and the Mpro affinity set (n = 20) are near or above it. |
| `controls_run` | Table below. |

**`controls_run`:**

| control | what it rules out | page |
|---|---|---|
| Two backbones run head to head on every entry (AF3 v3.0.1 and Boltz-2 v2.2.0) | Single-model idiosyncrasy; a failure common to both is a co-folding failure, not an AF3 bug. Used substantively (e.g. Boltz-2 recovers the KRAS Switch-II ligand where AF3 does not, p22; Boltz-2's covalent S angle 125.8° vs AF3's 162.2°, p26–27) | p44 (protocol); p22, p26–27, p28 (use) |
| 10 predictions per complex per model; AF3 across two seeds (10 and 42), 5 per seed | Single-draw chance; lets spread be shown as a violin rather than a point. Detects the case where the correct pose is *among* the 10 but not converged ("a substantial subset of generated models recovered ligand conformations with low RMSD … despite incomplete convergence across all predictions", p19) | p44 |
| Three orthogonal pose metrics (overall RMSD, pharmacophore RMSD, volume overlap) applied to every entry | Rules out the artefact where a chemically correct pose is scored as a failure by whole-ligand RMSD alone; explicitly diagnostic for symmetric ligands and flexible tails | p4, p11, p15–16 |
| Experimental 2Fo-Fc electron density inspected for the PLpro entry 24 (8UOB) | Rules out that the "wrong" predicted orientation is wrong at all — "the density does not clearly define a unique ligand orientation, suggesting that the AF3- or Boltz-2-predicted pose may not be strictly incorrect" | p16 (Fig 6C) |
| Ternary complexes aligned to each partner protein separately (CRBN vs CDK2; pVHL vs KRAS) | Separates binary sub-pocket recovery from ternary-assembly geometry — isolates the linker/interface failure from the ligand-recognition success | p22 (Fig 9D/E, 9F/G) |
| Individual binary ligands scored alongside the ternary complex they belong to (entries 43 KRAS Switch-II ligand, 44 VHL ligand vs ternary entry 42) | Rules out attributing a ternary failure to the ternary geometry when the binary pose was already wrong | p22 |
| Second, independent activity dataset with a wider dynamic range and single-assay provenance (20 Mpro complexes "from a single study to minimize assay variability") after the 6-compound sEH series failed | Rules out assay heterogeneity and a too-narrow potency range as the explanation for the sEH affinity-ranking failure | p37 |
| Near-analog negative control: N-methyl-S-thalidomide against S-thalidomide (the activity-cliff arm) | Intended to rule out that the models score any CRBN-shaped molecule as a binder. **n = 1 pair; underpowered; and the active member is a pre-cutoff, self-declared likely-memorized structure (4CI1)** | p38–40 |
| Confidence–accuracy correlation recomputed **within** each modality after the pooled correlation (Figs S12–S21, not in this PDF) | Rules out that the pooled minPAE/RMSD correlation is driven purely by between-modality differences. Result was negative: "no subclass showed a consistently strong relationship" | p33 |
| Both Pearson and Spearman reported for every correlation | Rules out a linearity assumption carrying a monotone-only relationship (or vice versa) | p46 (Statistical analysis); used p33, p37, p38 |
| Fragment set modelled as the biological dimer with multiple ligandable sites, not as a pre-defined pocket | Rules out crediting the model for pose accuracy when site selection was given away; explicitly cited as making the task harder ("creating multiple potential ligandable regions … which increased the difficulty of assigning the correct fragment-binding location") | p32 |
| — no pre-cutoff vs post-cutoff arm | **NOT RUN** (see `anti_memorization_control`) | — |
| — no decoy ligands, no scrambled sequences, no shuffled protein–ligand pairings, no apo arm | **NOT RUN.** No negative control other than the single N-methyl analog exists in the paper | — |

| Field | Value |
|---|---|
| `confidence_as_discriminator` | **Yes, heavily — and validated for pose accuracy, explicitly *not* validated for conformational state or activity.** §11 (p33–36) is a dedicated arm testing AF3 minPAE, AF3 ipTM and Boltz-2 ipTM against ligand RMSD and pharmacophore RMSD over 83 complexes. *Validated, positively*: pooled AF3 minPAE vs overall RMSD Pearson r = 0.665, Spearman r = 0.758 (p33); minPAE bins enrich monotonically for pharmacophore recovery, 100% (22/22) at <0.85 Å down to 3.3% (1/30) at >2.0 Å (p33). *Validated, negatively, and stated as such*: "we next performed the same analysis within individual ligand-binding modalities, but **no subclass showed a consistently strong relationship** between the confidence scores and overall RMSD" (p33); ipTM separates far more weakly than minPAE for both models (p36); and the paper's own conclusion is "**neither minPAE nor ipTM alone reliably identifies chemically realistic ligand poses across all target classes**" (p36). *Never validated for conformational state*: no confidence score is ever tested against DFG/αC correctness — the state claim and the confidence arm never meet. *Explicitly fails for activity*: "Model confidence scores were not associated with experimental activity" (p2, abstract); minPAE did not reproduce the sEH ranking (p36) and showed "no clear correlation" with Mpro activity (p38). **Caveat: the 0.85 Å boundary was chosen on this same evaluation set (route 4) and never re-tested on held-out data.** |

---

## D. Claims

| Field | Value |
|---|---|
| `central_conclusion` | AF3 and Boltz-2 recover chemically useful ligand poses reliably in canonical, pharmacophore-constrained enzyme and kinase active sites — including, in four selected kinase cases, the ligand-associated DFG/αC regulatory conformation — but degrade sharply for allosteric/cryptic sites, membrane proteins, RNA, and induced-proximity ternary complexes (PROTACs, molecular glues). Local pharmacophore geometry is recovered better than whole-ligand pose. AF3 minPAE is a usable pose-triage filter (minPAE <0.85 Å enriches strongly for accurate poses) but no confidence score tracks experimental activity; Boltz-2's affinity module captures relative activity trends in some series and separates one activity-cliff pair, but not reliably enough for potency prediction. Predicted poses can be locally chemically invalid (wrong stereochemistry, distorted covalent geometry, steric clashes) even when globally plausible, so the recommended use is hypothesis generation followed by chemistry-aware inspection and physics-based refinement. |
| `necessity_claims` | The paper is unusually free of hard necessity/impossibility claims about its own method; the necessity claims it does make are **prescriptive claims about how predictions must be evaluated and used**, which is the load-bearing form here. Verbatim: <br>• p4: "Because a single geometric metric cannot fully capture whether a predicted pose is useful for medicinal chemistry interpretation, we applied three complementary measures (Figure 1B) of pose similarity". <br>• p19: "For medicinal chemistry applications, predicted allosteric poses should therefore be treated primarily as hypotheses and interpreted alongside experimental structures, SAR, mutagenesis, biophysical mapping, or physics-based simulations before being used to guide analog design." <br>• p28: "Consequently, evaluation of covalent inhibitor predictions should include explicit inspection of local bond geometry in addition to conventional RMSD-based pose metrics." <br>• p28: "chemically accurate modeling of the reactive center remains an unresolved challenge for current AI-based structural prediction approaches." <br>• p36: "However, neither minPAE nor ipTM alone reliably identifies chemically realistic ligand poses across all target classes. Visual inspection, pharmacophore analysis, and local chemical-geometry validation therefore remain important before predicted structures are used for medicinal chemistry interpretation or compound-design decisions." <br>• p40: "These results emphasize that predicted structures require chemical evaluation, particularly for close analogs where small modifications can disrupt binding." <br>• p40: "Before predicted structures are used for SAR analysis or compound design, ligand stereochemistry, bond order and length, alkene planarity, alkyne linearity, ring conformation, and protein–ligand clashes should be inspected." <br>• p44: "Overall, AF3 and Boltz-2 are most useful as tools for generating and prioritizing structural hypotheses, rather than as stand-alone predictors of binding pose or activity." <br>• p28 (membrane): "accurate pose recovery remains challenging without explicit membrane context." <br>• p11 (about the field's default metric): "conventional whole-ligand RMSD may overestimate prediction errors for ligands containing flexible tails, symmetric substituents, or solvent-exposed peripheral groups." |
| `novelty_claims` | **NONE FOUND.** The paper makes **no** claim to be first, novel or unprecedented anywhere in the abstract, introduction, results or conclusion. The strongest self-positioning statements are gap statements and contribution statements, quoted verbatim for the record: <br>• p2: "whether their predictions provide useful guidance for lead optimization, SAR interpretation, and virtual screening **remains insufficiently characterized**." <br>• p3: "Existing evaluations of protein–ligand prediction models often emphasize global ligand RMSD or broad pose recovery, but medicinal chemistry applications require a more nuanced assessment of local pharmacophore preservation, ligand-induced conformational recovery, affinity ranking, and whether AI-generated confidence metrics such as ipTM or minPAE can be used to triage predictions. **This gap is particularly important** for challenging noncanonical recognition modes…" <br>• p3: "Here, we provide a medicinal chemistry-centered evaluation of AF3 and Boltz-2 across diverse ligand-binding modalities." <br>• p4: "Together, this work **defines** modality-dependent strengths and limitations of AF3 and Boltz-2 and **provides a practical framework** for their use in pose prediction, virtual screening, and SAR interpretation." <br>The words "first", "novel", "unprecedented" and "to our knowledge" appear in this paper only inside cited reference titles and in the phrases "first-in-class allosteric EGFR inhibitor" (p17) and "first-in-class" applied to BBO-8520 (ref 62, p54), i.e. describing other people's compounds, never this work. |
| `stated_limits` | The paper is candid and states most of its own weaknesses. Verbatim or near-verbatim, with pages: (1) **Small, narrow-range affinity series** — "Because all six compounds were highly active and spanned a narrow experimental IC50 range (0.009–0.115 μM), **this small series was not intended as a definitive affinity benchmark**" (p36). (2) **Affinity precision** — "the residual standard deviation of 0.63 log units indicates substantial compound-level variability around this trend… **their precision was limited for quantitative potency prediction**" (p38); "**Overall, these predictions appear more useful for compound prioritization than for estimating absolute potency**" (p38). (3) **Confidence triage is not general** — "no subclass showed a consistently strong relationship between the confidence scores and overall RMSD" (p33); "neither minPAE nor ipTM alone reliably identifies chemically realistic ligand poses across all target classes" (p36). (4) **Local chemistry is unreliable** — chirality inversion, E/Z errors, non-linear alkynes, ring-planarity distortion, wrong single-bond lengths, distorted covalent bond angles, steric clashes (p40–41, Fig 19). (5) **Flexibility ceiling** — "We observed a clear trend in which prediction accuracy decreased with increasing ligand conformational flexibility… additional rotatable bonds expand the conformational search space, input conformers generated by ETKDGv3-type methods may not represent the protein-bound state for more flexible ligands, and the models may not reliably rank multiple chemically plausible poses" (p44). (6) **Whole modality classes fail** — allosteric, cryptic-pocket, membrane, RNA, PROTAC, glue (p43). (7) **Membrane context missing** (p28–29). (8) **Ternary organization not recovered even when both binary poses are** (p22, p25). (9) **The activity-cliff pose result is a failure** — "the models can generate plausible binding modes for inactive compounds, while local chemical incompatibility may not be fully captured" (p39). <br>**Limits the paper does NOT state:** per-class n is never presented as a power limitation; the conformational-state claim is never flagged as unquantified; the 0.85 Å threshold is never flagged as data-derived; no template/MSA date restriction is discussed; Boltz-2's training cutoff is never given; the use of pre-cutoff structures (4CI1, 1W6K, 4AV4, 7X1T) is never reconciled with the stated cutoff. |
| `stance` | **`precedent` on findings + `contrast` on rigour** (provisional — the user's call, not settled here). *Precedent*: this is the most direct existing demonstration that a co-folding model's protein conformation follows the identity of the supplied ligand across DFG-in/DFG-out and αC-in/αC-out (p12, Fig 4D–G), which is the same ligand-sensitivity question asked from the medicinal-chemistry side; it also supplies a post-cutoff, modality-stratified comparator table and a genuinely undeposited six-structure prospective arm. *Contrast*: the conformational-state claim that would be the precedent is called **by eye from four unlabelled overlays with no metric, no threshold and no n**, the ligand-sensitivity arm that most resembles our question (activity cliffs) is **n = 1 pair against a pre-cutoff, self-declared likely-memorized reference**, the triage threshold is tuned on the evaluation set, and the per-entry numbers live in supplementary tables that are not in the corpus. |

---

## E. Quantitative comparators

### Modality breakdown — n per class

Entry indices are the paper's own (exhaustive list p46–47). **Class denominators marked (†) are
reconstructed arithmetically from the modality-wise minPAE percentages on p34 — the paper never
tabulates n per class in the main text.** Flag column marks classes too small to support a conclusion.

| modality class | entries | n | what it contains | powered? |
|---|---|---|---|---|
| **New sEH co-crystals** | 1–6 | **6** | Six in-house sEH inhibitor co-crystals, undeposited; ligands HP-1, HP-2, HP-3, FP-11, FP-17, FP-22 | **UNPOWERED (n=6)** — but the only prospective arm |
| **Canonical orthosteric** | 7–25 | **19** | JAK2 ×6 (7–12), TYK2 JH2 ×1 (13), BRAF ×1 (14), EGFR ×2 (15–16), ERK2 ×1 (17), PDE4D ×1 (18), Hck ×1 (19), p38α ×2 (20–21), PPARα ×2 (22–23), SARS-CoV-2 PLpro ×2 (24–25). The paper counts "**15 kinase complexes**" within 7–23, which requires counting PDE4D (a phosphodiesterase, not a kinase) among them — 7–23 minus the two PPARα entries = 15 | Adequate (n=19); the **kinase sub-count is 14 true protein kinases**, adequate |
| **Allosteric modulators** | 26–31 | **6** stated (**7†** implied by 28.6% = 2/7 on p34) | WRN/HRO761 (26), WRN/VVD-133214 covalent allosteric (27), allosteric EGFR (28), glutaminase C (29), KRAS Switch-II BI-2865 (30), SHP2 fragment (31) | **UNPOWERED (n=6)** — and one of the six (31) is the stated exception, so the "failure" verdict rests on 5 |
| **PPI inhibitors** | 32–40 | **9** | Aurora A–TPX2 (32), RhoGDI2–Rac1 (33), SOS1–KRAS (34), KEAP1–NRF2 (35), plus 36–40 (8T5G, 8T5M, 8T5R, 8UC9, 8UH0 — SOS1/SOS2–KRAS). **Entries 36–40 are double-counted: they appear in both the PPI figure caption (p21) and the fragment figure caption (p32)** | **UNPOWERED (n=9)**, and overlapping with the fragment class |
| **PROTACs / degraders** | 41–44 | **2 ternary complexes**, 4 entries (**10† ligand entities** implied by 10.0% = 1/10 on p34) | CDK2/Cyclin E1–CRBN/DDB1 cryo-EM ternary (41: 9D0X); KRAS G12D C118S–GDP–pVHL:elonginC:elonginB ternary (42: 8QVU); plus the isolated KRAS Switch-II ligand (43: 9RK8) and VHL ligand (44: 9L6F) from that system | **SEVERELY UNPOWERED (2 ternary complexes)** — one success, one failure. No conclusion is supportable |
| **Molecular glues** | 45–49 | **5** systems, **8 scored ligand entities** (Fig 10 x-axis: 45-NRAS, 45-CYPA, 46-CYPA, 46-KRAS, 47, 48-CRBN, 48-ENL, 49) | RMC-6236/daraxonrasib–NRAS–CypA (45: 9BG0), RMC-4998–KRAS G12C–CypA covalent tri-complex (46: 8G9P), IBG1–BRD4–DCAF16:DDB1ΔBPB (47: 8OV6), dHTC1–ENL–CRBN (48: 9DUR), dWIZ-1–CRBN–WIZ (49: 8TZX) | **SEVERELY UNPOWERED (n=5)** — one clear success (49), one clear failure (47), rest partial |
| **Covalent inhibitors** | 50–54 (+27, +46 cross-referenced) | **5** primary, **7** discussed (**8†** implied by 62.5% = 5/8 on p34) | PLpro (50: 8UVM), KRAS G12C–BBO-8520 ×2 (51: 8V3A, 52: 8V39), Mpro–PF-07817883 (53: 8V4U), KRAS G12D–YK-8S (54: 8JHL); plus WRN–VVD-214 (27) and RMC-4998 glue (46) | **UNPOWERED (n=5–8)**, and 2 of the 8 are re-used from other classes |
| **Membrane proteins** | 55–57 | **3** | MCT8–silychristin (55: 8ZKN), OATP1B1–atorvastatin (56: 9CY3), GAT3–GABA (57: 9LK8) | **SEVERELY UNPOWERED (n=3)** — one severe failure, one partial, one success. Literally one case per outcome bucket; no conclusion is supportable |
| **RNA binders** | 58–63 | **6** | risdiplam–SMN2/U1 helix (58: 8R62), ANP77–G2C4 repeat (59: 8QMH), SMN-CX–splice-site helix (60: 8R8P), naphthyridine-azaquinolone–ACG/AUA (61: 8ZNQ), r(CUG) repeat binder (62: 9CPD), unnamed 2025 RNA–ligand (63: 9IO0) | **UNPOWERED (n=6)** |
| **Fragments** | 64–73 (+36–40) | **10** (+5 overlapping) | Mpro fragments 64–72 (7GRE, 7GRF, 7GRJ, 7GRN, 7GRS, 7GRT, 7GRU, 7GRZ, 7GS0) + 73 (9BVE); plus the SOS1/SOS2–KRAS PPI fragments 36–40 counted again here | Borderline (n=10), inflated by class overlap |
| **Activity-cliff pair** | 74–75 | **1 pair (2 entries, one shared PDB 4CI1)** | S-thalidomide (74) and N-methyl-S-thalidomide (75), both mapped to 4CI1 | **SEVERELY UNPOWERED (n=1 pair)** — see the dedicated section below |
| **Mpro affinity-ranking set** | 76–95 | **20** | 20 SARS-CoV-2 Mpro–ligand complexes with IC50 from a single study (7GLV, 7GAW, 7GKS, 7GNT, 7GLG, 7GIU, 7GM1, 7GNA, 7GIX, 7GHM, 7GG2, 7GMR, 7GE3, 7GMP, 7GE2, 7GE4, 7GGC, 7GFJ, 7GCK, 7GBV) | Adequate (n=20) — the best-powered arm in the paper |
| **Chemistry-error exemplars** | not indexed | 4 | 1W6K, 8BPV, 4AV4, 7X1T, 8QVU (Fig 19). **1W6K, 4AV4 and 7X1T are pre-cutoff structures** | Anecdotal by design |
| **TOTAL in confidence analysis** | — | **83 complexes** (p33) | 6 + 19 + 7† + 9 + 10† + 5 + 8† + 3 + 6 + 10 = 83 exactly, using the reconstructed denominators | — |

**Classes where n is too small to support the stated conclusion:** PROTAC (2 ternary), membrane
protein (3), molecular glue (5), covalent (5 primary), allosteric (6), RNA (6), sEH (6), **activity
cliff (1 pair)**. That is eight of the twelve modality classes. The paper draws a
class-level verdict for each of them anyway (p43: "Performance was less consistent for allosteric
modulators, cryptic-pocket binders, membrane-protein ligands, RNA binders, PROTACs, and molecular
glues") without ever stating n alongside the verdict.

### Newly determined structures — count and timing

| question | answer | page |
|---|---|---|
| How many are new? | **Six** — entries 1–6, sEH co-crystals with inhibitors HP-1, HP-2, HP-3, FP-11, FP-17, FP-22, solved in house | p8, p46–47 |
| Solved by whom? | The authors; associated with two of their own manuscripts marked "(To be published)" (refs 22, 23, p51) | p8, p51 |
| Deposited before the predictions were run? | **No — not deposited at all at the time of writing.** Verbatim (p47): "**PDB accession codes for the six newly determined sEH complexes (1–6) will be provided upon deposition.** Authors will release the atomic coordinates and experimental data upon article publication." | p47 |
| Timing relative to the AF3 training cutoff (30 Sep 2021)? | Necessarily after it, by a wide margin, and stronger than post-cutoff: they were never in the PDB at all, so they cannot have entered AF3 or Boltz-2 weights **or** any template/MSA database. The paper does not state the solve dates | p6, p47 |
| Timing relative to the Boltz-2 cutoff? | **Boltz-2's training cutoff is never stated in the paper**, so this is formally NOT REPORTED — but the same never-deposited argument applies | — |
| Matched activity data? | Yes — the authors' own sEH IC50 values, 0.009–0.115 μM across the six, generated in house ("K.C. and M.M. performed the sEH assays and data analysis", p48) | p36, p37 (Fig 16B), p48 |
| Result on this arm | AF3 reproduced **4 of 6** poses (HP-2, FP-11, FP-17, FP-22); HP-1 failed by arm-swap between the LB and SB pockets while keeping the catalytic H-bonds; Boltz-2 "comparable overall performance". **None of the six reached minPAE < 0.85 Å** | p8, p34 |

### `metrics_reported`

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Chemically-useful-pose predicate — overall ligand RMSD | ≤ 2 | Å | Definition (heavy atoms, after protein alignment) | p4, p13 |
| Chemically-useful-pose predicate — pharmacophore RMSD | ≤ 1.5 | Å | Definition (reference-selected atoms) | p4, p13 |
| Chemically-useful-pose predicate — volume overlap | ≥ 70 | % | Definition (RDKit shape Tanimoto → V_intersection/V_ref) | p4, p13, p45–46 |
| AF3 pose recovery, new sEH co-crystals | 4 of 6 | count | 6 in-house sEH co-crystals (entries 1–6) | p8 |
| Boltz-2 pose recovery, new sEH co-crystals | "comparable overall performance" — **no number given** | — | same 6 | p8 |
| sEH ligand 1 (HP-2), Boltz-2 | IC50 0.01011 μM; overall RMSD 1.88 Å; pharmacophore RMSD 0.30 Å; volume overlap 78.93%; predicted affinity 0.060 μM; AF3 minPAE 1.09 Å | mixed | reference co-crystal | p37 (Fig 16B) |
| sEH ligand 2 (FP-11), Boltz-2 | IC50 0.115 μM; RMSD 2.00 Å; pharm 0.49 Å; overlap 72.13%; pred. affinity 0.021 μM; minPAE 1.27 Å | mixed | reference co-crystal | p37 |
| sEH ligand 3 (FP-17), Boltz-2 | IC50 0.01244 μM; RMSD 2.47 Å; pharm 0.84 Å; overlap 73.95%; pred. affinity 0.049 μM; minPAE 1.03 Å | mixed | reference co-crystal | p37 |
| sEH ligand 4 (FP-22), Boltz-2 | IC50 0.009106 μM; RMSD 4.81 Å; pharm 0.93 Å; overlap 63.7%; pred. affinity 0.39 μM; minPAE 1.09 Å | mixed | reference co-crystal | p37 |
| sEH ligand 5 (HP-1), Boltz-2 | IC50 0.009021 μM; RMSD 10.36 Å; pharm 3.13 Å; overlap 65.79%; pred. affinity 0.21 μM; minPAE 3.21 Å | mixed | reference co-crystal (the arm-swap failure) | p37 |
| sEH ligand 6 (HP-3), Boltz-2 | IC50 0.02072 μM; RMSD 2.83 Å; pharm 4.42 Å; overlap 71.42%; pred. affinity 0.94 μM; minPAE 2.95 Å | mixed | reference co-crystal | p37 |
| AF3 pose recovery, canonical orthosteric | all 15 "kinase" complexes + both PPARα complexes = 17 of 19; PLpro entries 24 and 25 the only exceptions | count | entries 7–25 | p10 |
| Median overall RMSD, successful canonical orthosteric cases | "generally within 2, and often below 1.5" | Å | median across 10 poses per complex | p10 |
| Pharmacophore RMSD in canonical orthosteric | "remained below ~1" even where overall RMSD exceeded 2 Å | Å | entries 7–25 | p10 |
| AF3 recovery of ligand-associated kinase states | **4 of 4 selected cases** (7 JAK2 DFG-in/αC-in; 14 BRAF DFG-out/αC-in; 19 Hck DFG-in/αC-out; 21 p38α activation-loop) — **called visually, no metric, no threshold, no number** | count | Fig 4D–G overlays | p12, p13 |
| AF3 pose recovery, PPI | **6 of 9** | count | entries 32–40 | p19 |
| AF3/Boltz-2 pose recovery, allosteric | "generally failed to reproduce the correct allosteric binding modes"; **exactly one exception (31, SHP2 fragment)** — **no success count given** | — | entries 26–31 | p17 |
| Covalent C–S–C bond angle, experimental (8UVM) | 130.8 | degrees | X-ray reference | p26 |
| Covalent C–S–C bond angle, AF3 | 162.2 (mean of 10 models) | degrees | vs 130.8° experimental | p26 |
| Covalent C–S–C bond angle, AF3 (restated in §14) | **161.7** — **inconsistent with the 162.2° on p26; the paper never reconciles the two** | degrees | vs 130.8° experimental | p41 |
| Covalent C–S–C bond angle, Boltz-2 | 125.8 (mean) | degrees | vs 130.8° experimental | p27 |
| Typical C–S–C reference range cited | ~101–109 | degrees | chemical expectation | p26 |
| RNA pose recovery, best cases | entry 58 (risdiplam) 1.73; entry 60 (SMN-CX) 2.35 | Å overall RMSD | RNA–ligand references | p31 |
| RNA pose recovery, failed cases | entry 59 (ANP77/G2C4) 16.73; entry 61 (8ZNQ) 10.88 | Å overall RMSD | RNA–ligand references | p31 |
| AF3 minPAE vs overall ligand RMSD (pooled) | Pearson r = 0.665; Spearman r = 0.758 | correlation | 83 complexes | p33 |
| AF3 ipTM and Boltz-2 ipTM vs overall RMSD | "negatively correlated … with stronger correlations by Spearman than by Pearson" — **no r values given for either** | — | 83 complexes | p33 |
| Within-modality confidence vs RMSD | "no subclass showed a consistently strong relationship" — **no r values given** | — | Figs S12–S21 (**not in this PDF**) | p33 |
| AF3 minPAE bins → fraction with pharmacophore RMSD < 1.5 Å | 100% (22/22) <0.85 Å; 72.7% (8/11) 0.85–1.0; 61.5% (8/13) 1.0–1.5; 42.9% (3/7) 1.5–2.0; 3.3% (1/30) >2.0 | % (n/N) | 83 complexes | p33, p35 |
| AF3 minPAE bins → fraction with overall RMSD accurate | 81.8% (18/22); 45.5% (5/11); 30.8% (4/13); 14.3% (1/7); 6.7% (2/30) across the same bins | % (n/N) | 83 complexes | p33 |
| AF3 ipTM bins → fraction with pharmacophore RMSD < 1.5 Å | 88.9% (24/27) >0.95; 45.5% (10/22) 0.90–0.95; 50.0% (4/8) 0.80–0.90; 20.0% (2/10) 0.70–0.80; 12.5% (2/16) <0.70 | % (n/N) | 83 complexes | p36, p35 |
| Boltz-2 ipTM bins → fraction with pharmacophore RMSD < 1.5 Å | 68.6% (24/35) >0.95; **6.7% (1/15) 0.90–0.95**; 33.3% (4/12) 0.80–0.90; 28.6% (2/7) 0.70–0.80; 7.1% (1/14) <0.70 — **non-monotonic** | % (n/N) | 83 complexes | p36, p35 |
| Fraction of predictions with minPAE < 0.85 Å, per modality | sEH **0%**; canonical orthosteric 73.7%; allosteric 28.6%; PPI 11.1%; PROTAC 10.0%; molecular glue **0%**; covalent 62.5%; membrane protein **0%**; RNA **0%**; fragment **0%**; E3 ligase ligand **0%** | % | Fig S22 (**not in this PDF**) | p34 |
| Boltz-2 predicted affinity vs experimental IC50, sEH series | Pearson r = **−0.4770**, P = 0.3387; Spearman r = **−0.3714**, P = 0.4972; residual SD = 0.6101 — **wrong sign and non-significant** | correlation | n = 6 sEH inhibitors, IC50 range 0.009–0.115 μM | p37 (Fig 16A) |
| Boltz-2 predicted affinity vs experimental activity, Mpro series | Pearson r = 0.742, P = 0.0002; Spearman r = 0.695, P = 0.0007; residual SD = 0.63 log units | correlation | n = 20 Mpro complexes, single study | p38 |
| Experimental activity range, Mpro set | log10[IC50 (μM)] from −1.70 to 1.98 (≈3.7 log units) | log10 μM | 20 Mpro complexes | p38 |
| AF3 minPAE vs experimental activity | "no clear correlation was observed" — **no r value given** | — | Fig S27 (**not in this PDF**) | p38 |
| **Activity cliff — Boltz-2 predicted affinity, S-thalidomide** | **1.7** | μM (predicted) | vs the N-methyl analog | p40, p39 (Fig 18B) |
| **Activity cliff — Boltz-2 predicted affinity, N-methyl-S-thalidomide** | **37.2** | μM (predicted) | vs S-thalidomide; ≈22-fold separation, correct direction | p40, p39 (Fig 18B) |
| **Activity cliff — AF3 minPAE** | **0.91 → 1.64** (active → inactive) | Å | within-pair change | p39 |
| **Activity cliff — Boltz-2 ipTM** | **0.99 vs 0.98** — essentially unchanged | dimensionless | within-pair change | p39 |
| **Activity cliff — steric clash in the inactive analog pose** | ~**2.0** interatomic contact, shorter than the summed van der Waals radii, generated by **both** models | Å | Fig 18C (AF3), 18D (Boltz-2) | p39 |
| **Activity cliff — experimental activity of either compound** | **NOT REPORTED.** No IC50, Kd, degradation or binding value is given for S-thalidomide or for N-methyl-S-thalidomide; inactivity is asserted from refs 80–81 as "expected" | — | — | p38–39 |
| Sampling depth | 10 predictions per complex per model; AF3 = 2 seeds (10, 42) × 5 predictions | count | protocol | p44 |
| Hardware | NVIDIA RTX 4090 (24 GB) and RTX PRO 6000 (96 GB) | — | protocol | p44 |

| Field | Value |
|---|---|
| `n_predictions` | **Samples per target:** 10 per complex per model (AF3: two seeds, 10 and 42, five predictions each; Boltz-2: 10 directly) — p44. **Targets:** 95 indexed entries; 83 complexes in the confidence analysis; 6 undeposited in-house structures; 20 in the Mpro affinity arm; 1 activity-cliff pair. **Total predictions:** **never stated by the paper.** Arithmetic on the confidence-analysis set gives 83 × 10 × 2 models = 1,660 structures, and on the full 95-entry index 95 × 10 × 2 = 1,900; neither number appears in the paper and neither is used here as a reported value. **Per-modality prediction counts are not given** except implicitly through the minPAE percentages on p34. |
| `comparable_to_ours` | *(left empty by the extractor per v3)* |
| `si_in_scope` | **SI NOT HELD — and the omission is severe for this paper specifically.** The Supporting Information listing (p47) covers "Boltz-2 prediction violin plots; summary of PDB entries, names, index numbers, and annotations; detailed tables of AF3 and Boltz-2 entries and prediction statistics; coordinate files for computational models." **None of it is in this PDF.** What is therefore missing: **Table S1** (the master entry table — PDB IDs, index numbers and annotations, i.e. the only place the modality assignment per entry is written down); **Tables S2–S12** (per-modality molecular structures and *all* per-entry numeric results, including **Table S12, the activity-cliff data**); **Table S13** (experimental and predicted activities for the 20 Mpro compounds); **Figures S1–S10** (every Boltz-2 per-entry violin plot — so **essentially all Boltz-2 quantitative results are absent**, and Boltz-2 is half the paper's subject); **Figure S11** (the minPAE/ipTM vs RMSD scatters); **Figures S12–S21** (the within-modality correlations that produced the paper's most important negative result); **Figure S22** (the per-modality minPAE breakdown behind the p34 percentages); **Figures S23–S25** (confidence-range groupings); **Figure S26** (sEH IC50 vs all other metrics); **Figure S27** (minPAE vs activity); **Figure S28** (RAS–CypA glue). Consequence: **every number in `metrics_reported` above is one the authors chose to put in the main text**; no per-entry value can be recovered for any modality other than the six sEH ligands (Fig 16B, p37). Analysis code and protocols are at https://github.com/RX-Medchem/docking-evaluation (p44) — **not retrieved or verified here.** |

---

## THE ACTIVITY-CLIFF ARM (§13, p38–40, Figure 18 p39) — extracted in full

Recorded separately because it is the arm that tests whether a model responds to a small chemical
change, and because it is small enough that summarising it would lose the whole result.

**What was tested, verbatim (p38):** "To further examine whether the models could separate active
compounds from closely related inactive analogs, we examined an activity-cliff pair, S-thalidomide and
N-methyl-S-thalidomide (Figure 18A, 18B), to determine whether the models could distinguish a positive
ligand from a closely related inactive analog when the activity separation was large."

**How a cliff pair was defined:** **There is no operational definition.** The paper gives no similarity
threshold (no Tanimoto, no MMP/matched-molecular-pair rule), no potency-fold threshold, no cliff index,
and no measured activity for either member. The pair is constructed by hand from chemical reasoning:
the active is a known CRBN ligand, the inactive is the same molecule with **one added methyl group on
the glutarimide nitrogen**, asserted to abolish binding by citation. Verbatim (p38–39):
"N-methyl-S-thalidomide was included as a near-analog negative control because glutarimide
N-methylation is expected to disrupt productive CRBN engagement.[80,81]" and (p39) "The expected
outcome for N-methyl-S-thalidomide is therefore loss of productive binding."

**How many pairs: ONE.** A single pair, entries 74 and 75, both mapped to the same PDB reference 4CI1
(p47). The whole arm is 2 predictions per model. There is no second pair anywhere in the paper.
**Note the reference is pre-cutoff and the authors say so:** "S-Thalidomide is a well-characterized
CRBN ligand and **is likely represented in the structural training landscape**, and both models
accurately reproduced its CRBN-bound pose." (p38) — so the "active" half of the cliff is a memorized
answer, and there is no experimental structure at all for the inactive half.

**Did the predicted structures differ between the two members?** **No, not usefully — the pose
prediction failed the test.** Verbatim (p39): "**The expected outcome for N-methyl-S-thalidomide is
therefore loss of productive binding. However, both AF3 and Boltz-2 still generated plausible-looking
CRBN-bound poses for the inactive analog.** Notably, the additional methyl group in
N-methyl-S-thalidomide was placed in a sterically unfavorable position, with interatomic distances
shorter than the summed van der Waals radii of nearby atoms (Figure 18C, 18D). Thus, although the
overall pose appeared reasonable, the local binding geometry contained an obvious steric clash. This
illustrates an important limitation of AF3 and Boltz-2 pose prediction: **the models can generate
plausible binding modes for inactive compounds, while local chemical incompatibility may not be fully
captured.**" And in the Figure 18 caption (p39): "Despite the loss of activity upon N-methylation,
**both models place the inactive analog in the CRBN binding pocket and additionally generate an ~2.0 Å
interatomic contact consistent with a steric clash.**" The only *structural* difference between the
two members is therefore a ~2.0 Å clash the model produced rather than avoided — the model
accommodated the chemical change by driving atoms into each other instead of by rejecting the pose or
repositioning the ligand. **No RMSD is reported for the inactive analog** (there is no reference
structure for it), so the pose difference is never quantified at all.

**Did any prediction track the activity difference?** **Partially, and only through the affinity module
— not through pose, not through ipTM, and only weakly through minPAE.** Verbatim (p39): "**AF3 minPAE
increased from 0.91 to 1.64 Å for the inactive analog, suggesting some separation, but not enough to
serve as a reliable triage criterion. In contrast, the Boltz-2 ipTM score remained nearly unchanged
(0.99 versus 0.98).**" And (p40): "**Interestingly, the Boltz-2 binding-affinity module partially
captured the activity cliff, predicting stronger binding for thalidomide than for
N-methyl-S-thalidomide. Specifically, Boltz-2 predicted an affinity of 1.7 μM for thalidomide compared
with 37.2 μM for N-methyl-S-thalidomide, providing some ability to prioritize the active ligand over
the inactive analog. Together, this example is consistent with the activity-ranking results above:
Boltz-2 affinity predictions can provide useful separation in some cases, but pose prediction alone
does not determine whether a ligand will bind productively.**" Restated in the conclusion (p43): "the
Boltz-2 affinity module captured relative activity trends in selected cases, including the Mpro dataset
and the CRBN activity-cliff pair". Note the minPAE move (0.91 → 1.64 Å) **crosses the paper's own
0.85 Å triage boundary in neither direction** — both members are above it, so the paper's headline
triage rule would not have separated them; and the 1.64 Å value sits in the 1.5–2.0 Å bin, where only
42.9% of predictions are accurate anyway.

**Verdict for this corpus.** The arm was defined and run, and it produced **one usable directional
result (Boltz-2 affinity, ≈22-fold, correct direction) and three negative results (pose plausible for
the inactive analog; ipTM flat at 0.99/0.98; minPAE separation insufficient for triage)** — all on
**n = 1 pair**, with **no measured activity for either compound**, **no cliff definition**, and a
**pre-cutoff, self-declared likely-memorized reference structure** for the active member. It is a
worked illustration, not a test with statistical content. It **cannot support** any general claim about
ligand sensitivity, and the paper is careful not to make one — it calls it "this example" (p40).

---

## F. Figures

One row per panel group. Split on `mark`/`measure`, not on `facet`. The A–C panel triple (overall
RMSD / pharmacophore RMSD / volume overlap, one violin per entry, 10 poses per violin) recurs
identically in Figures 4, 7, 8, 9, 10, 11, 12, 13 and 14, and is one row each with a compound measure.
Pages rendered to establish panel structure: **7, 8, 13, 18, 24, 35, 37, 39** (8 pages). All other rows
are from captions plus body text.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A–B | 5 | The modality taxonomy evaluated, and the four evaluation metrics with their thresholds | schematic | `SCHEMATIC \| drug-discovery modality classes (orthosteric enzyme/kinase, allosteric, PPI, PROTAC, glue, covalent, membrane, RNA, fragment) and the RMSD/pharmacophore/volume/confidence evaluation criteria \| no data` | 2 (A taxonomy, B metric definitions) | | CC-BY-NC 4.0, **no ND clause — redrawing permitted, commercial use not**. License on every page banner incl. p5 |
| 2A | 7 | Arachidonic acid → 14,15-EET → 14,15-DHET, the sEH reaction | schematic | `SCHEMATIC \| two-step enzymatic conversion with chemical structures \| no data` | 1 | | CC-BY-NC 4.0, p7 |
| 2B | 7 | AF3-predicted 14,15-EET in the sEH pocket with SB/LB pockets circled | structure render | `RENDER \| facet: none (1) \| views: 1 \| overlay: 1 predicted substrate on 0 reference (no experimental EET complex shown) \| axis: none` | 1 | Presented as a mechanistic reference but it is itself an AF3 *prediction*, and no experimental sEH–EET structure is shown alongside it | CC-BY-NC 4.0, p7 |
| 2C | 7 | 2D interaction model of sEH substrate recognition (Y383, Y466, D335) | schematic | `SCHEMATIC \| 2D protein–ligand interaction diagram with R1/R2 substituent definitions \| no data` | 1 | | CC-BY-NC 4.0, p7 |
| 2D | 7–8 | Pose recovery for the six new sEH co-crystals: three metrics per compound | violin | `PLOT \| facet: none (1) \| vary: compound (6: HP-2, FP-11, FP-17, FP-22, HP-1, HP-3) \| series: metric (3: O overall RMSD, P pharmacophore RMSD, V volume overlap) \| measure: RMSD (Å, left axis) and volume overlap (%, right axis) \| mark: violin \| n: 10 AF3 poses per violin, 18 violins per panel` | 1 panel, 18 violins | **Dual y-axis in a single panel**: O and P read against the left 0–20 Å axis, V against the right 0–100% axis, so the V violins are drawn in the same visual space as RMSD violins and invite a comparison that is meaningless. **No n stated in the caption** (10 is recoverable only from p44). **AF3 only** — Boltz-2 is exiled to Figure S1, absent from this PDF, so the head-to-head comparison the paper claims is not visible here | CC-BY-NC 4.0, p7 |
| 3A–F | 9 | AF3 vs experimental overlays for the six sEH inhibitors, each with a 2D per-atom deviation map | structure render | `RENDER \| facet: inhibitor (6) \| views: 1 \| overlay: 1 of 10 predictions (selection rule NOT REPORTED) on 1 reference \| axis: none` | 6 (vary by compound), each paired with a 2D deviation map | **One of ten models shown with no stated selection rule.** The paired 2D deviation maps use a fixed 0–10 Å colour scale (p46) that saturates for the failed case | CC-BY-NC 4.0, p9 |
| 4A–C | 13 | Pose recovery across canonical orthosteric entries 7–25, three metrics | violin | `PLOT \| facet: metric (3: overall RMSD Å, pharmacophore RMSD Å, volume overlap %) \| vary: entry (19: 7–25, grouped Kinase / PPARα / PLpro) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 AF3 poses per violin, 19 violins per panel` | 3 stacked panels, same faceting | **Y-axis of panel A runs 0–~50 Å**, which compresses the 2 Å threshold line and every successful entry onto the baseline — the discriminating region is unreadable. **n not shown.** AF3 only; Boltz-2 in Figure S2 (absent) | CC-BY-NC 4.0, p13 |
| 4D–G | 13 | Four kinase complexes showing recovered DFG and αC states, with arrows marking the motifs | structure render | `RENDER \| facet: kinase complex (4: JAK2 7/8BM2, Hck 19/9BYJ, BRAF 14/8C7Y, MAPK14-p38α 21/9CJ4) \| views: 1 \| overlay: 1 of 10 predictions (selection rule NOT REPORTED) on 1 reference \| axis: none` | 4 (vary by system) | **This is the paper's entire conformational-state evidence and it carries no quantitative panel at all** — the DFG-in/out and αC-in/out calls are made from coloured helices and hand-drawn arrows, with no dihedral, distance, RMSD or threshold anywhere. One unlabelled model of ten per system. No n | CC-BY-NC 4.0, p13 |
| 5A | 15 | Six pose metrics for the PPARα–lanifibranor–SRC1 ternary system, ligand and peptide | violin | `PLOT \| facet: none (1) \| vary: metric (6: peptide overall RMSD, peptide Cα RMSD, peptide volume overlap, ligand overall RMSD, ligand pharmacophore RMSD, ligand volume overlap) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 poses per violin` | 1 | Mixed Å and % measures on one panel. Only entry 22 is plotted although the text claims a result "across both complexes" (22 and 23) — entry 23 has no panel | CC-BY-NC 4.0, p15 |
| 5B | 15 | AF3 ternary assembly overlaid on experiment: lanifibranor in the PPARα LBD plus SRC1 peptide | structure render | `RENDER \| facet: none (1) \| views: 1 \| overlay: 1 of 10 predictions (selection rule NOT REPORTED) on 1 reference \| axis: none` | 1 + ligand inset | Single unlabelled model | CC-BY-NC 4.0, p15 |
| 6A | 16 | Three pose metrics for the pseudo-symmetric PLpro–Jun12682 complex (entry 24) | violin | `PLOT \| facet: none (1) \| vary: metric (3: overall RMSD, pharmacophore RMSD, volume overlap) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 poses per violin` | 1 | | CC-BY-NC 4.0, p16 |
| 6B | 16 | 2D interaction map of the AF3 pose with orientation-ambiguity regions circled | schematic | `SCHEMATIC \| 2D protein–ligand interaction map with hand-drawn ambiguity annotations \| no data` | 1 | Ambiguity regions circled by hand; no criterion given for what counts as ambiguous | CC-BY-NC 4.0, p16 |
| 6C | 16 | Experimental 2Fo-Fc density at 1.0σ around Jun12682, showing the two orientations are not resolved | structure render | `RENDER \| facet: none (1) \| views: 1 \| overlay: 0 predictions on 1 reference + electron density \| axis: none` | 1 | Single contour level (1.0σ) shown; no second level to test how the conclusion depends on it | CC-BY-NC 4.0, p16 |
| 7A–C | 18 | Pose recovery across the six allosteric entries 26–31, three metrics | violin | `PLOT \| facet: metric (3: overall RMSD Å, pharmacophore RMSD Å, volume overlap %) \| vary: entry (6: 26–31) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 AF3 poses per violin, 6 violins per panel` | 3 stacked panels, same faceting | **n = 6 entries carries a whole-modality verdict.** Panels A and B run 0–40 Å and 0–50 Å, flattening the 2 Å and 1.5 Å threshold lines onto the axis. In panel C entries 26, 29, 30 and 31 sit at or near 0% and are hard to separate. **n not shown.** AF3 only; Boltz-2 in Figure S3 (absent) | CC-BY-NC 4.0, p18 |
| 7D–I | 18 | Six allosteric systems as surface renders with the orthosteric site marked, plus 2D chemical structures | structure render | `RENDER \| facet: system (6: WRN 26, WRN 27, EGFR 28, glutaminase C 29, KRAS 30, SHP2 31) \| views: 1 \| overlay: 1 of 10 predictions (selection rule NOT REPORTED) on 1 reference \| axis: none` | 6 (vary by system), each with a chemical-structure inset | Single unlabelled model per system | CC-BY-NC 4.0, p18 |
| 8A–C | 20 | Pose recovery across the nine PPI entries 32–40, three metrics | violin | `PLOT \| facet: metric (3: overall RMSD Å, pharmacophore RMSD Å, volume overlap %) \| vary: entry (9: 32–40) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 AF3 poses per violin, 9 violins per panel` | 3 stacked panels, same faceting | **n not shown.** The "6 of 9" success count in the text (p19) is not marked on the figure. AF3 only; Boltz-2 in Figure S4 (absent) | CC-BY-NC 4.0, p20 |
| 8D–G | 20 | Four PPI systems with the endogenous protein–protein interface superimposed from a separate reference structure | structure render | `RENDER \| facet: system (4: Aurora A–TPX2 32, RhoGDI2–Rac1 33, SOS1–KRAS 34, KEAP1–Nrf2 35) × reference type (2: inhibitor complex, endogenous partner complex) \| views: 1 \| overlay: 1 of 10 predictions on 1 inhibitor reference + 1 endogenous-interface reference \| axis: none` | 4 (vary by system) | Single unlabelled model per system | CC-BY-NC 4.0, p20 |
| 9A–C | 22 | Pose recovery for the degrader-associated entries, three metrics | violin | `PLOT \| facet: metric (3: overall RMSD Å, pharmacophore RMSD Å, volume overlap %) \| vary: degrader entry/sub-entry (41–44 and their per-protein splits) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 AF3 poses per violin; violins per panel NOT REPORTED in the caption` | 3 stacked panels, same faceting | **The entire PROTAC verdict rests on 2 ternary complexes**, which the figure does not make visible. **n not shown.** AF3 only; Boltz-2 in Figure S5 (absent) | CC-BY-NC 4.0, p22 |
| 9D–G | 22 | The two ternary degrader complexes, each rendered twice — aligned to the E3 ligase and to the target | structure render | `RENDER \| facet: system (2: CDK2–CRBN 41/9D0X, KRAS–pVHL 42/8QVU) × alignment target (2: E3 ligase, substrate) \| views: 1 \| overlay: 1 of 10 predictions (selection rule NOT REPORTED) on 1 reference \| axis: none` | 4 (2 systems × 2 alignment frames), each with a 2D deviation map | This dual-alignment device is the paper's cleanest figure idea — it separates binary-pocket recovery from ternary-geometry recovery without needing a new metric | CC-BY-NC 4.0, p22 |
| 10A–C | 24 | Pose recovery across the molecular-glue set, three metrics, split per ligand-binding protein | violin | `PLOT \| facet: metric (3: overall RMSD Å, pharmacophore RMSD Å, volume overlap %) \| vary: glue sub-entry (8: 45-NRAS, 45-CYPA, 46-CYPA, 46-KRAS, 47, 48-CRBN, 48-ENL, 49) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 AF3 poses per violin, 8 violins per panel` | 3 stacked panels, same faceting, with 2D glue structures inset | **n = 5 systems (8 scored entities) carries a whole-modality verdict.** Panels A and B run to ~50 Å and ~60 Å, compressing the threshold lines onto the axis. **n not shown.** AF3 only; Boltz-2 in Figure S6 (absent) | CC-BY-NC 4.0, p24 |
| 10D–K | 24 | Experimental and AF3-predicted ternary assemblies for four glue systems, side by side | structure render | `RENDER \| facet: system (4: RMC-6236–NRAS–CypA 45, IBG1–BRD4–DCAF16 47, dWIZ-1–CRBN–WIZ 49, dHTC1–CRBN–ENL 48) × source (2: experimental, AF3-predicted) \| views: 1 \| overlay: 0 (shown side by side, not superimposed) \| axis: none` | 8 (4 systems × 2 sources) | Predicted and experimental shown **side by side rather than superimposed**, which makes the ternary-geometry deviation — the actual result of this section — impossible to judge from the figure | CC-BY-NC 4.0, p24 |
| 11A–C | 27 | Pose recovery across the covalent inhibitor set, three metrics | violin | `PLOT \| facet: metric (3: overall RMSD Å, pharmacophore RMSD Å, volume overlap %) \| vary: entry (covalent set 50–54 plus cross-referenced 27, 46) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 AF3 poses per violin; violins per panel NOT REPORTED in the caption` | 3 stacked panels, same faceting | **The covalent bond-angle result — the section's most specific finding — has no quantitative panel here**; the 130.8°/162.2°/125.8° comparison exists only as text (p26–27) and as a single annotated render in Fig 19E. **n not shown.** AF3 only; Boltz-2 in Figure S7 (absent) | CC-BY-NC 4.0, p27 |
| 11D–I | 27 | Six covalent complexes as overlays | structure render | `RENDER \| facet: system (6: PLpro 50, KRAS G12C 51, KRAS G12C 52, Mpro 53, KRAS G12D 54, WRN 27) \| views: 1 \| overlay: 1 of 10 predictions (selection rule NOT REPORTED) on 1 reference \| axis: none` | 6 (vary by system) | Single unlabelled model per system | CC-BY-NC 4.0, p27 |
| 12A–C | 29 | Pose recovery for the three membrane-protein systems, three metrics | violin | `PLOT \| facet: metric (3: overall RMSD Å, pharmacophore RMSD Å, volume overlap %) \| vary: entry (3: MCT8 55, OATP1B1 56, GAT3 57) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 AF3 poses per violin, 3 violins per panel` | 3 stacked panels, same faceting | **Three violins carry a modality verdict** — one severe failure, one partial, one success, i.e. one case per outcome. **No structural render is shown for the MCT8 fold failure**, although "the predicted protein architecture was substantially incorrect" (p28) is the section's main claim, so its central result has no panel. **n not shown.** AF3 only; Boltz-2 in Figure S8 (absent) | CC-BY-NC 4.0, p29 |
| 13A–C | 30 | Pose recovery across the six RNA–ligand entries, three metrics | violin | `PLOT \| facet: metric (3: overall RMSD Å, pharmacophore RMSD Å, volume overlap %) \| vary: entry (6: 58–63) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 AF3 poses per violin, 6 violins per panel` | 3 stacked panels, same faceting | Range spans 1.73–16.73 Å (p31), so panel A's axis must accommodate ~17 Å and the 2 Å line is again near the baseline. **n not shown.** AF3 only; Boltz-2 in Figure S9 (absent) | CC-BY-NC 4.0, p30 |
| 13D–E | 30 | SMN-CX splice-site RNA complex: predicted vs experimental, with the A14 stacking interaction | structure render | `RENDER \| facet: none (1) \| views: 2 (overall RNA fold, A14 recognition close-up) \| overlay: 1 of 10 predictions (selection rule NOT REPORTED) on 1 reference \| axis: none` | 2 (views of one system) | Only the best RNA case (60) gets a render; **no render is shown for the two failures (59 at 16.73 Å, 61 at 10.88 Å)** | CC-BY-NC 4.0, p30 |
| 13F | 30 | 2D per-atom deviation map for the SMN-CX ligand | schematic | `SCHEMATIC \| 2D ligand map coloured by per-atom positional deviation \| no data` | 1 | Colour scale fixed 0–10 Å (p46) | CC-BY-NC 4.0, p30 |
| 14A–C | 32 | Pose recovery across the fragment set, three metrics | violin | `PLOT \| facet: metric (3: overall RMSD Å, pharmacophore RMSD Å, volume overlap %) \| vary: entry (fragment set 64–73 plus the SOS1/SOS2–KRAS fragments 36–40) \| series: none (1) \| measure: RMSD (Å) and volume overlap (%) \| mark: violin \| n: 10 AF3 poses per violin; violins per panel NOT REPORTED in the caption` | 3 stacked panels, same faceting | **Entries 36–40 are plotted in both this figure and Figure 8, so the fragment and PPI classes share five entries** and the two class-level verdicts are not independent. **n not shown.** AF3 only; Boltz-2 in Figure S10 (absent) | CC-BY-NC 4.0, p32 |
| 14D | 32 | Mpro dimer with an active-site inhibitor, an active-site fragment and a dimerization-interface fragment superimposed on one AF3 model | structure render | `RENDER \| facet: none (1) \| views: 1 \| overlay: 1 AF3 prediction on 3 references (53/8V4U, 64/7GRE, 72/7GS0) \| axis: none` | 1 | Three references and one prediction in one image with arrow labels; which of the 10 models is shown is not stated | CC-BY-NC 4.0, p32 |
| 15A–C | 35 | Confidence score vs pharmacophore RMSD, points binned by score range, with per-bin success rates printed on the panel | scatter | `PLOT \| facet: confidence metric (3: AF3 minPAE, AF3 ipTM, Boltz-2 ipTM) \| vary: entry, rank-ordered along a "PDB ID" axis (83, effectively an index not a variable) \| series: score range (5 bins per panel) \| measure: pharmacophore RMSD (Å) \| mark: point \| n: 1 per mark, 83 per panel` | 3 stacked panels, one per confidence metric | **The independent axis is labelled "PDB ID" but carries no information** — points are sorted by their own colour bin and then by measure, so the x-position is a rank, not a variable; the plot is a sorted strip chart dressed as a scatter, and the actual predictor (the confidence value) is shown only as a colour bin. **The bin boundaries were chosen on this data** (p33). The printed cell 100% (22/22) has no confidence interval. Y-axes run 0–40 Å, so the entire ≤1.5 Å decision region is one pixel band at the baseline | CC-BY-NC 4.0, p35 |
| 16A | 37 | Experimental vs Boltz-2-predicted potency for the six sEH inhibitors, with correlation statistics | scatter | `PLOT \| facet: none (1) \| vary: experimental log10[IC50 (μM)], −2.0 to −1.0 (continuous) \| series: compound identity (6, one marker each) \| measure: Boltz-2-predicted log10[IC50 (μM)] \| mark: point \| n: 1 per mark, 6 per panel` | 1 | **n = 6, and the x-range spans only ~1.1 log units** — the paper says so itself (p36). Every point gets its own marker shape and colour, which reads as six series rather than six observations. The reported correlation is negative (r = −0.4770), i.e. the wrong direction, and this is not stated in the panel | CC-BY-NC 4.0, p37 |
| 16B | 37 | Table of IC50, Boltz-2 RMSD/pharmacophore/overlap/affinity and AF3 minPAE for the six sEH ligands | table | `SCHEMATIC \| 6-row × 7-column numeric table of per-ligand experimental and predicted values \| no data` (rendered as a table, not a plot) | 1 | The only per-entry numeric table in the entire main text; every other modality's equivalent is in the absent SI | CC-BY-NC 4.0, p37 |
| 17 | 38 | Experimental vs Boltz-2-predicted potency for 20 Mpro inhibitors | scatter | `PLOT \| facet: none (1) \| vary: experimental log10[IC50 (μM)], −1.70 to 1.98 (continuous) \| series: none (1) \| measure: Boltz-2-predicted log10[IC50 (μM)] \| mark: point \| n: 1 per mark, 20 per panel` | 1 | The best-powered arm in the paper. Residual SD 0.63 log units is reported in text (p38) but the caption does not state whether an identity line or a regression line is drawn | CC-BY-NC 4.0, p38 |
| 18A, 18C–D | 39 | The CRBN pocket: experimental S-thalidomide, then the AF3 and Boltz-2 poses of the inactive N-methyl analog overlaid on it, with the ~2.0 Å clash arrowed | structure render | `RENDER \| facet: model source (3: experimental 4CI1, AF3 prediction, Boltz-2 prediction) \| views: 1 \| overlay: 1 of 10 predictions (selection rule NOT REPORTED) on 1 reference \| axis: none` | 3 (A, C, D) | **The paper's entire activity-cliff structural evidence.** No RMSD, no distance distribution across the 10 models, no quantitative panel — the single number on the figure is a hand-annotated "2.0 Å Steric clash" arrow, and it is not stated whether 2.0 Å is the mean, minimum or a single model's value. n = 1 pair, not shown | CC-BY-NC 4.0, p39 |
| 18B | 39 | Chemical structures of the pair, with the N-methyl highlighted, and the two predicted affinities printed underneath | schematic | `SCHEMATIC \| two 2D chemical structures differing by one N-methyl group, annotated with predicted affinities 1.7 μM and 37.2 μM \| no data` | 1 | **The affinity result — the one positive finding of the arm — is printed as text on a chemical-structure panel with no error bar, no spread across the 10 predictions, and no experimental value to compare against** | CC-BY-NC 4.0, p39 |
| 19A–F | 42 | Six categories of local ligand chemistry error, each as an annotated overlay | structure render | `RENDER \| facet: error type (6: sp³ stereochemistry 1W6K, alkene E/Z + bond length 8BPV, alkyne linearity 4AV4, ring geometry 7X1T, covalent bond angle 8UVM, steric clash 8QVU) \| views: 1 \| overlay: 1 prediction (selection rule NOT REPORTED) on 1 reference \| axis: none` | 6 (vary by error type) | **A qualitative catalogue standing in for a frequency measurement**: the paper never reports how often chirality inversion, E/Z error or clash occurs across the 83 complexes, only that each can happen. Three of the six exemplars (1W6K, 4AV4, 7X1T) are **pre-cutoff structures**, used without comment in a paper whose design premise is a post-cutoff set. Panel E's 161.7° contradicts the 162.2° given on p26 | CC-BY-NC 4.0, p42 |

**Reuse summary:** the whole preprint is under **CC-BY-NC 4.0** ("It is made available under a CC-BY-NC
4.0 International license", banner on **every page**, p1–54). **No ND clause** — derivatives and
redrawing are permitted; **NC applies**, so commercial reuse is not. Attribution required.

---

## G. Provenance

| Field | Value |
|---|---|
| `extracted_on` | 2026-09-07 |
| `extractor` | claude subagent (Opus 5), single-paper extraction session |
| `schema_version` | `v3` |
| `confidence` | **high** for identity, scope, modality breakdown, the activity-cliff arm, the new-structure timing, claims, controls, and figures; **medium** for the per-class denominators marked (†), which are reconstructed arithmetically from the p34 percentages rather than stated; **low** for anything that lives in the SI. What was hard: (1) the paper indexes 95 entries and analyses 83, and never reconciles the two — the 83 is only recoverable by summing the Figure 15 bin counts and cross-checking against the p34 percentages; (2) modality class membership is defined only in Table S1, which is absent, so class boundaries had to be reconstructed from section text and figure captions; (3) entries 36–40 are counted in two classes and entries 27 and 46 in two more, so the class sizes do not partition the dataset cleanly; (4) all Boltz-2 per-entry results are in absent SI figures, so the head-to-head comparison could not be checked. |
| `unresolved` | 1. **83 vs 95.** The confidence analysis covers "83 complexes" (p33) while the PDB ID list indexes 95 (p46–47). The reconstruction 6+19+7+9+10+5+8+3+6+10 = 83 fits the p34 percentages exactly, but it requires denominators for allosteric (7), PROTAC (10) and covalent (8) that differ from the entry ranges (6, 4, 5) and it excludes the 20-compound Mpro affinity set and the 2 activity-cliff entries. The paper never states the mapping. <br>2. **Boltz-2's training cutoff is never given**, anywhere, despite Boltz-2 being half the study and the entire anti-memorization design resting on a single AF3 date. <br>3. **Template and MSA handling are never described** beyond "default … settings" (p44), and no date restriction on any template or sequence database is mentioned. A post-cutoff weight set with an unrestricted template search is not a post-cutoff experiment; this cannot be resolved from the PDF. <br>4. **Pre-cutoff structures used without comment**: 4CI1 (the whole activity-cliff arm), 1W6K, 4AV4, 7X1T (Fig 19). The paper states the cutoff on p6 and then uses these without reconciling them. <br>5. **The `7G*` group-deposition release dates** (entries 64–72 and 76–95, i.e. 32 of 95 entries) are never stated and cannot be checked from the PDF. <br>6. **Covalent bond-angle inconsistency**: AF3's angle is 162.2° on p26 and 161.7° on p41 for the same complex (8UVM). Not reconciled. <br>7. **The DFG/αC state calls have no operational definition** — no dihedral, distance, database label or threshold. "Accurately recovering … kinase conformational features" (p12) cannot be checked or reproduced. <br>8. **"15 kinase complexes"** (p10) requires counting PDE4D, a phosphodiesterase, as a kinase; the true protein-kinase count in entries 7–23 is 14. <br>9. **The success count for the allosteric class is never given** — "generally failed" with one named exception, but no n/N. Same for molecular glues, covalent, RNA, fragments and membrane proteins: only the PPI class (6 of 9), the sEH class (4 of 6) and the canonical orthosteric class (17 of 19) get explicit counts. <br>10. **Which of the 10 models each render shows is never stated**, in any figure, and no selection rule is given. <br>11. **No experimental activity for either activity-cliff compound** — inactivity is asserted by citation, so the cliff has no measured magnitude. <br>12. **Refs 22 and 23** (the sEH structures and assays) are "To be published" with no journal, no DOI and no preprint identifier (p51), so the six new structures cannot be independently checked. <br>13. **Tags I needed but could not use, and did not invent:** there is no vocabulary term for a **nucleic-acid / RNA target system** (this paper has six RNA–ligand complexes and the system list has no slot for them); none for **membrane transporter** at the modality level beyond `transporter`, which I did use; none for **induced-proximity modalities** (PROTAC, molecular glue, ternary complex); none for **covalent ligands**; none for **fragment-based / fragment screening**; none for **protein–protein-interaction inhibitor**; none for **activity cliff / matched molecular pair**, which is precisely the arm this extraction was commissioned for and which will therefore not be findable by reverse lookup; none for **binding-affinity prediction** as distinct from structure prediction (the Boltz-2 affinity module is a third of this paper); and none for **pose-prediction accuracy / docking benchmark** as distinct from conformational-state benchmarking — `benchmark-only` covers the study type but not what was benchmarked. Recorded here rather than invented. <br>14. **`allosteric-failure` was considered and deliberately not applied.** The v3 definition is "the *result* that no model or setting ever sampled the allosteric site". Here the models did sample near the allosteric sites and failed the binding *mode* ("the models generated plausible ligand placements near the correct region, but did not reproduce the experimentally observed molecular recognition pattern", p17), and one of the six allosteric entries (31, SHP2) succeeded outright. Applying the tag would misreport the result. <br>15. **`experimental-validation` applied with a caveat.** The definition is "a computational paper that tested a prediction in the lab". These authors solved six co-crystal structures and ran the matched sEH IC50 assays themselves (p8, p48), and the assays are used directly to test Boltz-2's affinity predictions (p36–37). That is lab work testing a prediction, so the tag fits — but the structures were solved as *references*, not as tests of a specific prior prediction, so this is a weaker instance than a paper that predicted first and then measured. <br>16. **`prospective` applied with a caveat.** Only entries 1–6 (6 of 95) are genuinely prospective; the other 89 are retrospective post-cutoff. The tag will produce a partial-truth hit on reverse lookup; the `prospective` field states the split. <br>17. **Schema ambiguity, v3, panel splitting.** SCHEMA.md line 186 says "**Split when `mark` or `measure` differs**" and line 189 immediately says "four box panels showing four metrics under the same faceting are **one row** with a compound measure". Those contradict: four metrics *is* four differing measures. I resolved it in favour of the worked example (one row, compound measure) for every A–C metric triple, which is what makes Figures 4, 7–14 one row each rather than three. The rule needs one sentence saying that a differing measure splits a row **only when the mark also differs**, or that a metric triple under one mark is a faceted compound measure. Two extractors will otherwise produce 9 rows where I produced 3. <br>18. **Schema ambiguity, v3, dual-axis panels.** Figure 2D plots RMSD (Å) and volume overlap (%) in one panel against left and right axes. The PLOT form has one `measure:` slot and no way to say "two measures, two axes, one panel"; I wrote a compound measure and pushed the defect into `hides`. A `measure:` convention for dual-axis panels would help — they are common and they are almost always a defect worth joining on. <br>19. **Schema ambiguity, v3, `vary:` for a non-variable axis.** Figure 15's independent axis is labelled "PDB ID" but is a sort order, not a variable. `vary: entry (83)` overstates it and `vary: none` is false. I wrote it as an index with a note. The grammar could use an explicit `index` form for rank-ordered strip charts, which recur constantly in benchmark papers. <br>20. **Schema ambiguity, v3, tables inside figures.** Figure 16B is a numeric table rendered as a figure panel. None of the five forms fits; `SCHEMATIC \| ... \| no data` is a false statement about a panel that is entirely data. I used SCHEMATIC with an explicit note. A sixth **TABLE** form would fix it, and it is the only place in the paper where per-entry numbers survive outside the missing SI. |
| `why_it_matters` | *(left empty by the extractor — user's call)* |

---

## Tags

`kinase` `transporter` `general-protein`
`cofolding` `benchmark-only`
`ensemble` `single-state`
`continuous-metric` `binary-predicate` `visual-metric` `saturating-metric`
`design-level-oracle` `prospective` `anti-memorization` `unpowered` `confidence-as-discriminator` `experimental-validation`
`ligand-driven`
`orthosteric` `allosteric-site` `cryptic-pocket`
`preprint`
`precedent` `contrast` `negative-result`
`comparator-numbers`

**Tag notes.** `multi-backbone` **deliberately withheld**: exactly two backbones are compared, and the
v3 rule requires *more than two*. `oracle-leak` **withheld in favour of `design-level-oracle`**: the
inference pipeline is clean of deposited-structure inputs as far as the paper describes it (route 1 is
NOT REPORTED, not confirmed leaky), while routes 4, 5 and 7 are all present — evaluation-set-tuned
thresholds, reference-derived pharmacophore atom sets, and expected answers declared before results
were read. `allosteric-failure` withheld — see `unresolved` item 14. `md`, `enhanced-sampling`,
`msa-subsample`, `msa-state-filter`, `template-state-bias`, `af-cluster`, `latent-steering`,
`md-emulator` all inapplicable: no MSA or template manipulation, no sampling intervention, no
simulation is performed. `templates-on` / `no-template-no-msa` / `state-annotated-input` withheld
because template and MSA handling are NOT REPORTED and inferring a protocol tag from "default
settings" would fabricate a protocol claim. `two-state` withheld: multiple kinase states appear across
*different* targets and ligands, never two states of one target. `rmsd-only` withheld because the
paper's central methodological argument is that RMSD alone is insufficient; `continuous-metric` plus
`binary-predicate` plus `visual-metric` is the accurate triple. `seed-only` withheld: seeds are fixed
at 10 and 42 and never used as a state handle. `figure-exemplar` withheld — the figures are workmanlike
and mostly carry the defects listed in `hides`.
