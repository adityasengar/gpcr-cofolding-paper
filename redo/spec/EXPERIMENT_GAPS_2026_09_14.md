<!-- GENERATED 2026-09-14 by a 64-agent gap hunt over redo/spec/CATALOGUE.md.
     PROPOSALS, not decisions. Nothing here is authorised. 19 proposed, each screened
     three times (already-catalogued / already-published / feasible-and-powered), 13
     cleared; 19 screen verdicts rejected across DUPLICATE, INFEASIBLE, UNDERPOWERED
     and PREEMPTED, so the screens were not rubber-stamping.

     WHAT THE ORCHESTRATOR VERIFIED BY HAND AFTERWARDS, AND WHAT IT DID NOT:

     VERIFIED. g1_recording_spec.tsv is 49 rows and names NO min_plddt_at_anchor,
       plddt_mean, plddt_at_anchors, ipTM, PAE, ramachandran, chain_breaks,
       templates or recycles. It DOES name plddt_partner_chain_mean and
       plddt_ga_alpha5, so section A's "none of them is pLDDT" is WRONG -- two
       exist and both are PARTNER-side. The substantive claim survives and sharpens:
       Blocks B and D each hold FOUR confidence columns (plddt_mean,
       plddt_at_anchors, min_plddt_at_anchor, plddt_ga_alpha5) and the redo as
       specified would record fewer, while title clause 3 IS a confidence claim.
     VERIFIED. All 2,039 rows of g1_systems.csv carry ligand = none.
     VERIFIED. All 30 family_swap rows carry chain_b_sha256 = PENDING:COUPLING.md.
     VERIFIED. "template" appears 0 times in g1_recording_spec.tsv, g1_systems.csv,
       g2_systems.csv, CAMPAIGN.md and MSA_SPEC.md; and Block B's templates-off
       claim is evidence class (b)+(c), never (a).

     NOT VERIFIED. Every prediction count, GPU cost, MDE and cut figure below.
       Treat them as the agents' arithmetic until re-derived.
-->

# What else you can run — 13 experiments that are not in the catalogue

*Answer to: "what other experiments can I run?" Every count below that I state as measured, I recomputed today from the files named. Commands are given where a number is load-bearing.*

---

## The one-paragraph answer

Six of the thirteen cost **zero GPU** and three of those six **redirect real spend** — the largest redirects ~64,000 predictions of n=50 control arms. Of the seven that need inference, **every pilot fits in 7,940 predictions total** (17% of MINIMAL, 5% of INTENDED). Two of the thirteen submitted proposals are the same experiment and must be merged. One proposed arm is blocked by a defect in `redo/inputs/` that would have dispatched a mislabelled control: **all 30 `family_swap` rows in `g1_systems.csv` carry the receptor's own cognate family and `chain_b_sha256 = PENDING:COUPLING.md`** — G9 is enumerated but not built.

And the single most consequential free finding is not an experiment at all: `redo/inputs/g1_recording_spec.tsv` has **49 columns and none of them is `min_plddt_at_anchor`, whole-complex pLDDT, ipTM, PAE, `ramachandran_outlier_frac`, `chain_breaks`, `templates_used` or `recycles_realised`.** Title clause 3 is a confidence claim, and the redo as specified records strictly less confidence information than Block B already holds. Fix that before dispatch; it is impossible afterwards.

---

## A. Ranked table

Rank = decisiveness per GPU-hour. Free first, and the three that displace real spend are ranked above the three that only change interpretation. MDE for interactions = 1.218/√k; main effects 0.189–0.242.

| # | experiment | what it answers | cost | scale | clusters + MDE | what a NULL lets the paper say |
|---|---|---|---|---|---|---|
| **R0** | **Recording-contract amendment** (precondition, not an experiment) | Can the redo reproduce its own title clause 3? | free | 8 columns added to a 49-column spec | n/a | n/a — this is a gate. Without it X1, X3, T1, T3 and half of Group 3 are unrunnable in the redo |
| **X1** | **Anchor admissibility census + sensitivity** | What fraction of state calls rest on anchor atoms the model cannot place, and is that fraction arm-dependent? | free | 32,000 Block B rows (replicates on C, D1–D3) | k=26, MDE 0.239 | "State calls are insensitive to anchor-local confidence at every gate tested." One Methods line, and **E9.2/G7 dispatch at full size instead of being gated** |
| **X2** | **Instrument noise floor** (replicate depositions, same receptor, same state) | How far apart do the two axes read on two structures of the same thing? | free | 1,357 measured structures; 164 tilt groups / 143 NPxxY groups with n≥2 | k≈51 for dispersion; **the construct arm is 33 paired groups and is NOT well powered — report the two k's separately** | "The instrument is more precise than the class separation, the third decimal is harmless." Q4 and Q6 get dropped with a measured justification instead of a cited one |
| **X5** | **Placebo axes** — a control on the readout, not the input | Does the co-input move the activation coordinate, or the whole receptor? | free\* (CPU + an extension to `redo/build/g0_measure_axes.py`, ~20 axes on 3,114 cached mmCIFs) | 0 predictions; 6 frozen columns added before dispatch | inherits the arm's k (29 on the ladder, MDE 0.226) | Specificity interval covers 1: "the co-input drives a large conformational change that the predicate reads as active." **And it is the only way to distinguish a bulk control that did nothing from one that distorted** — today those are the same number |
| **X3** | **Fold-integrity confound** (Ramachandran, chain breaks) | Does supplying a partner change stereochemical quality, and does the arm effect survive conditioning on it? | free | 32,000 Block B rows | k=26, MDE 0.239 | "The confound is real but small and the adjusted effect sits inside the unadjusted interval" — a sentence a referee who knows `yu2026domainmotion` will demand |
| **X4** | **Does one NPxxY cut transfer across paralog clusters?** (coverage table, no refit) | Is 9.08 a property of Class A or of the clusters that dominate the calibration set? | free | 1,016 measured Class A structures; per-cluster held-out sens/spec with Clopper-Pearson | k=26 both-state clusters (calibration-only arm is k=7 — report it separately and say it is underpowered) | "Few clusters' intervals exclude the pooled rate": one global cut is defensible, cluster-disjoint — which **neither published GPCR state instrument does at all** |
| **X6** | **Cross-architecture state concordance** | When four architectures get an identical input, how often do they agree, and is that better than four independent draws at their own floors? | free | 32,000 Block B rows; 50 of 128 receptor-arm units disagree | k=23 | Concordance at or below the independent-draw null: "confirmed on all four backbones" is weaker than it reads. **A genuinely useful negative about this project's own strongest structural argument** |
| **T2** | **The register slide** — native α5, wrong end (off6 = Gs 368–388, off10 = Gs 364–384) | Is it the α5 **C-terminus**, or is any 21-residue α5 window enough? | real | pilot 600 (2 constructs × 30 rec × Boltz-2 × n=10); full 2,400 | k=29, main-effect MDE 0.098–0.126 | Slid windows match ct21: **the title must read "an α5-derived peptide", not "the α5 C-terminus"**. That is the finding, not a failure |
| **T3** | **Recycles × partner** (recycles {1,3} × {R0_apo, R3_ct21}) | Does the published shallow-sampling route to alternative conformers reach the active state without a transducer, at recycles=1 as published? | real | 1,160 gross on OpenFold3 alone, fewer net (apo/R=3 cells coincide with Pillar 3) | k=29, interaction MDE 0.226 | Recycles=1 does not lift the apo floor: "the published alternative-state protocol, transferred to four AF3-lineage backbones on 29 class A clusters, does not produce active GPCRs without a transducer." Materially stronger than "we varied depth" |
| **T1** | **Template state × partner presence** (MERGED — see §C) | Does the α5 co-input still drive the active state when the model is handed a deposited **inactive** template of the same receptor? | real **+ a pipeline ask** | plumbing proof ~60; 2×2 at 1 backbone 600; 4-backbone 2,400. Zero new structures | k=22 on the both-state-clean subset (MDE 0.260); k=29 if template availability is not the selector | Interaction covers zero: the co-input's effect is **independent of retrieved structural context**, converting "templates were off" from a convenience into a measured boundary condition. Second null (template moves nothing) is a methods finding about four tools |
| **T4** | **Helix-propensity manipulation at fixed length and byte-identical contact face** (`proPunch` primary) | Does the peptide have to *be* a helix, or does the model build one from whatever it is handed? | real | gated pilot 1,200 (3 constructs × 10 rec × **4 backbones** × n=10); +2,400 on release | k=29 on release; the pilot is a backbone property, not a panel property | Measured helicity does not drop: **the models impose an ideal helix on anything, the ladder measures reach not recognition**, and CATALOGUE §6 item 5 — currently listed as unanswerable from this repo — closes |
| **T5** | **Partner cognacy × ligand class** | Does the models' ligand response depend on which transducer tip occupies the cleft? | real | 1,280 (2 new cells × 16 rec × 4 bb × n=10); **budget 1,920** — G9 is not built | k=15, MDE 0.314 — the tightest here, and the interaction is expected small if benign. **E7.4 must run on this design first** so a null is bounded, not absent | Ligand classes separate by the same amount cognate or not: a **specificity statement about the four models that nobody has made**, reported as bounded by 0.314 |
| **T6** | **Receptor-side socket ablation** (SOCKET-A / SHAM-A × apo/ct21, receptor-MSA shallow replicate mandatory) | Does the partner effect require the receptor's own α5 socket, or just a Gα-like chain in the input? | real | pilot 2,400; primary 24,000 (4 bb, n=50) — **gate the primary on the pilot** | k=29, interaction MDE 0.226. WT apo→cognate is 0.733, so abolition is 3.2× MDE | Shift survives ablation **and** the sham does nothing: the title's verb weakens from "drives" to "co-presence of a Gα-like chain is sufficient". If the sham kills it too, the arm is uninformative — **and the sham arm is the reason we can say so rather than guess** |

\* X5 is free of GPU but not of work: it needs a generator change and a manifest restamp, same class as E0.1. Do not let it appear in a cost line as "free, 0 predictions" and have somebody plan against it.

**Totals.** All six pilots + T5 + T6 pilot = **7,940 predictions**. Full versions minus T6's primary ≈ **13,880**. T6 primary adds 24,000 and is conditional.

---

## B. The three that matter most

**1. T2, the register slide — 600 predictions to test a word in the title.** `GROUP1_SYSTEMS.md` §2.1 makes "every emitted construct is a suffix of its parent" a construction invariant and proves it by planting. That invariant is why the ladder cannot answer its own question: every rung, every null, every scramble shares the same C-terminal residue, so the campaign varies length, composition and identity but has never varied **register**. E1.1 varies length at a fixed anchor; this varies the anchor at fixed length; they are exact complements and neither resolves the other from inside itself. Gate it behind P1 — if ct21 shows no lift over apo there is nothing to slide — then run off6 (Gs 368–388: Sunahara's crystallographic α5 start with the hook removed, and it has a hash-verified sibling in the registry) and off10. Pre-register that a register claim requires the slid peptide to be **delivered at native-like depth (`d_ga_alpha5_r350_ca`) while failing the predicate** — reach without recognition — or the arm reports "the terminus is required" and nothing stronger. Declare it as the second exception to the suffix invariant (M5_dHD is the precedent) *before* any construct is emitted, and plant o=0 against the amended check.

**2. X1, the anchor admissibility census — free, and it decides whether you dispatch 8,800–22,000 predictions.** I recomputed it on `data/block_b/01_rows/rows_tidy.csv`: **65.5% of all 32,000 rows carry at least one predicate-defining anchor below pLDDT 70** (3.85% below 50). The gate is severely arm-imbalanced and it moves control arms in *opposite* directions — keep-rate at ≥70 is apo 28.6%, decoy 22.1%, shuffled 31.2%, cognate 55.9%, and **OpenFold3's apo cells keep 19 of 2,000 rows**. So every arm contrast in the paper is partly a survivorship contrast and nobody has looked. F-2 covers only the <50 early return (3.85%); the borderline 50–70 band is 19,736 of 32,000 rows and is untouched. Report it as (i) a Methods survivorship census, (ii) an explicitly-labelled *sensitivity* analysis with no gate adopted and `min_plddt_at_anchor` carried as a covariate rather than a filter — conditioning on a post-treatment variable is a collider — and (iii) the E9.2 predecessor diagnostic on all 44 mixed apo cells, scored twice, against the state call **and** against structural truth. If the call-AUC is centred below 0.5 while the truth-AUC is not, the mixed apo mode is placement-driven and G7/E9.2 is buying 8,000 samples of a badly-placed atom. Pre-register the gate level before dispatch or it becomes a post-hoc filter — the exact defect F-23 already cost you once.

**3. T1, template × partner — the only arm that measures your handle against the field's standard handle.** Two of the submitted proposals are this experiment; merge them (§C). It is the fifth inactive-directing input E7.1 never considered, and unlike a post-cutoff nanobody it is **guaranteed to exist for every panel slug**. Before funding it, know the dependency I verified: `redo/protocol/MAP_LIFECYCLE.md:775` records templates as `has_templates_field: false` (Boltz), *not recorded* (Chai), `use_templates: false` (OF3), two flags both false (Protenix) — the status writers **record** the flag, and no templater **writes** one. This is a pipeline engineering ask, not a knob. Buy a ~60-prediction plumbing proof first: plant a template of a *different* receptor and assert the output coordinates move, recording `n_template_hits_consumed` and FAILING — never skipping — when it is absent. That proof alone closes `CLAIM_VS_CODE` C6, which has been open since the protocol landed. Then run the single 2×2 that is not published — template {none, own strict_inactive} × partner {apo, ct21} — with both priors pre-registered: chiesa (co-input beat the template on AF2/AFM, so a template win here is a reportable reversal) and swapna (AF3 reverted a correct alternative-state template in 4 of 6 transporters, so flip-back is the *expected* outcome and is memorisation evidence, not co-input strength). Without that pre-registration, "template lost" and "template was never read" are the same observation.

Runner-up, and it would be third on a different day: **X5, the placebo axes.** It is the only proposal that adds a quantity which is supposed *not* to move, and it is the difference between "the bulk control did nothing" and "the bulk control distorted the receptor" — with the current two-column spec those produce the same number, and G3/G4 are 64,000 predictions of exactly that comparison.

---

## C. What the catalogue already has — and the merge you must make

**The merge.** "Template state × partner presence" and "State-annotated templates crossed with the partner rung" are one experiment: same factor A (template state), same factor B (partner rung), same panel (CORE-32 / the 30-receptor ladder), same 4 backbones, same decisive cell (inactive template + cognate partner), same blocking gate. Fund **one** arm: the 2×2 with the inactive level, the active level demoted to a calibration rung labelled as reproducing chiesa on AF3-lineage backbones, the 3×3 and the paralog-template level dropped (heo's 70%-identity cutoff already *is* the non-oracle experiment). Both template levels are oracle-informed by construction and must be declared so in Methods: they measure handle strength, never prospective accuracy.

Where I checked, entry by entry:

| new | nearest catalogue entry | why it is not that |
|---|---|---|
| T1 template | **none.** `grep -ci template CATALOGUE.md` → 12, all other papers' settings (:623, :892, :995) plus E6.1's `templates_used` delivery column (:1115), which records a **constant**. E4.1 (date holdout) stratifies on training exposure, which cannot be switched | a template is the one retrieval channel the operator controls: E4.1 yields a cross-receptor correlation, this yields a within-receptor intervention |
| T2 register slide | E1.1 (length at fixed C-terminal anchor), E1.2 (bulk: changes protein, fold, composition, alignment at once), E1.3 (composition at ct21) | none supplies a **native α5 peptide at the wrong register**; `seq_rungs.tsv` / `seq_controls.tsv` contain no such construct; greps for slid/offset/internal-fragment across `redo/spec/` return nothing |
| T3 recycles | E8.1 + PLAN Pillar 2 vary the **alignment**, holding recycles at 3 | `grep -ni recycl` → **one** hit in all 1,847 lines of CATALOGUE.md (:729, a quotation about an AF2 protocol) and two in RUN_MATRIX (:940, :943) where recycles appear only as an unknown in the **cost** model. Recycling is a factor in no experiment |
| T4 helix propensity | E1.3 (its five controls all **preserve or raise** propensity by design), E1.5 (Ala raises it). CATALOGUE §6 item 5 states this exact question and proposes only that helicity be **recorded** | recording an outcome is not manipulating a factor. Nothing in 241 control rows lowers propensity |
| T5 cognacy × ligand | E1.4/G9 (family swap at **ligand = none**), E2.2/G6 (ligand × partner **presence**) | the crossing with partner **identity** exists in neither campaign; all 313 READY Group 2 rows supply a cognate partner |
| T6 socket ablation | E1.5 (scans the **supplied partner**, 10 receptors, 1 backbone), E5.1 (observational, changes nothing) | no entry in any of the 10 groups mutates chain A; all ~20 dispatchable control arms in `GROUP1_SYSTEMS.md` §4 vary chain B |
| X1 anchor gate | E9.2 (assumes the mixed cells are binomially noisy and buys samples), E3.1–E3.3 (ask whether confidence predicts correctness — presupposing the geometry is measurable), F-2 (<50 only) | `grep min_plddt_at_anchor CATALOGUE.md` → **nothing**, and the column is absent from `g1_recording_spec.tsv` too |
| X2 noise floor | E0.1 (bootstraps the **cut**), E0.4 (sweeps a band). GROUP0 §5.4/§5.5 declare fusion and mutation as **exclusion rules** and explicitly never measure their effect | neither measures dispersion at fixed (receptor, state). `grep -riE "repeatab\|measurement error\|error budget" redo/spec/` → **nothing** |
| X3 fold integrity | E5.5 names its correlates explicitly and model quality is not among them; `redo/spec/` mentions fold integrity only as a prospective gate on the **supplied partner chain** | `grep -rlni ramachandran redo/spec/ analysis/ manuscript/` → **nothing** (the only hits anywhere are `figures/data_lit/*.csv` and two PDB files). Correct the proposal's claim that `redo/` returns nothing: `redo/protocol/BLUEPRINT_REQUEST.md:630` asks the pipeline team for the column's definition — a documentation ask, so the analysis gap stands |
| X4 cluster transfer | E0.1 does leave-one-**receptor**-out ROC (§7 item 1) and never holds a cluster out or refits | its own threat paragraph cites `mattsson2026leakage` as the reason receptor-disjoint splitting is not enough — an argument **for** this experiment that E0.1 does not act on |
| X5 placebo | E0.2 (a further state **index**), E0.4, E5.2 — all add quantities that **are** activation-correlated. Block A's "orthogonal signature" is the PIF connector: a third activation axis | `grep -rni placebo redo/spec/ CLAIMS.md` → **nothing**. None can distinguish a state change from a distortion |
| X6 concordance | E3.2 tests one rule (max confidence) at one grain (seed inside a cell), where 300 of 319 cells are already seed-unanimous | the headroom is **across backbones**: 50 of 128 receptor-arm units have backbones disagreeing on the majority call. Cite `kalakoti2026afsample3` for consensus-beats-confidence — it is not ours to discover |

---

## D. What to cut to make room

The new arms are affordable **inside INTENDED without raising the budget**. Here is where the room is.

| cut | predictions released | reason |
|---|---:|---|
| **G1b → 3 of 7 rungs at n=50** (apo + the two rungs the adaptation band selects) | **25,600** | §4.1 requires n≥50 only for per-cell claims. The headline is pooled and §2.1 says sampling depth is nearly free variance — 385 of 576 Block B cells are pinned at 0 or 1. You do not need per-receptor figures at all seven rungs; you need them at the rung the title takes |
| **Defer G3b (α5-null + bulk at n=50)** | **38,400** | Gated on X5. Until a placebo axis exists, "the bulk control did nothing" and "the bulk control distorted the receptor" are the same number — so 38,400 predictions would buy an unreadable control. G3a at n=10 is already funded and answers the pooled question |
| **Defer G4b (composition controls at n=50)** | **25,600** | Same gate, same reason. G4a at n=10 first |
| **Gate G7 (deep-apo, n=500 on 4 cells) on X1** | 8,000 conditional | If the within-cell AUC inversion holds, G7 is sampling the badly-placed mode 500 times. X1 costs nothing and decides whether G7 dispatches at 8,000 or at 4,800 or not at all |
| **Cut G11, the heterotrimer rung** | **6,400** | `MAP_LIFECYCLE.md` §2.3: "**There is no three-chain templater.** Every two-chain function is hardcoded to exactly two." G11 needs new pipeline code for a rung the ladder already brackets (R7_full above, ct21 below). If you are paying for exactly one templater change this campaign, buy the **template channel** (T1) — it opens a factor, not a rung |
| **Cut G10b, the Gi→Gs stepwise series** | **3,000** | 15 cells × 10 receptors × n=**20** on one backbone. §4.1 forbids per-cell claims below n=50 and every claim this arm makes is per-position. Subsumed by G10 (ala scan) plus T2 |

**≈107,000 released or deferred, against ≈13,880 for the full versions of six new arms.** Keep G12 (the Gi/Gt single-residue natural pair): it is genuinely novel, it is cheap, and it is the sensitivity floor T2 and T4 will both want to be read against.

---

## E. Proposed and rejected

| proposal | verdict |
|---|---|
| Length ladder under an agonist | **Duplicate.** `g2_systems.csv` `G6f(option)` already enumerates R7_full × 4 ligand roles as READY, and G5a crosses depth × {R0, R3_ct21, R7_full} × {none, agonist} on CORE-L17 in the MINIMAL tier. Residual increment is two rungs — an amendment to G6, not an arm. Its panel also pools T1 with T3_mixed, which D-2026-09-12-f forbids, putting a chain-count confound through the length axis |
| Scrambled partner × partner-MSA on | **Preempted.** `SEQUENCES.md` §6 tabulates the expected depth for every ct21 control as ≈1, so the new cell is probably an input-equivalent copy of the existing MSA-off cell and the interaction collapses to the already-funded G17 main effect. The scramble depths are a **zero-GPU** measurement that §6.1 item 4 already orders first. And the full-length half is answered: Block B's MSA audit shows three of four backbones read the scrambled residues as aligned uppercase |
| C7 stratified by agonist-alone-active exposure | **Underpowered.** Applies the *main-effect* cluster SD (0.189–0.242) to a difference of differences; at RUN_MATRIX's own interaction SD (0.435) the MDE is ~0.50 predicate points against a target effect of 0.09–0.18. Spends GPU on E+ receptors with 1–3 structures, and E+ is confounded with bulk deposition (point-biserial r = 0.486). The free half — stratifying the 313 READY rows — is worth doing |
| Derangement ligand decoy | **Duplicate of E2.4**, already dispatched as G6d + G6fd. D-RULE's `within_panel` pool already administers foreign GPCR agonists (DECISIONS:836). The ">=100× selectivity" filter cannot be computed from the pinned artefacts — the 28 GB ChEMBL_37 database was deleted 2026-09-12 — so "zero new curation compute" is false |
| Five unread structural axes as an instrument-independent replication | **Preempted.** `thresholds_panel.csv` carries **fitted** midpoints for four of the five; they were evaluated head-to-head with the predicate and dropped on 2026-09-01 (F-1b). The headline axis correlates r = +0.908 with the tilt axis over 16,800 Block B rows — it is TM6 opening re-measured one helical turn down the same helix pair. The two "specificity controls" separate deposited active from inactive by 0.066 Å and 0.018, **in the direction opposite to their declared polarity** |
| I1 — rebuild the deposited complex and measure the ruler offset | **Already answered by a join.** Block C's `rows.tier3.v2.csv` supplies both poles; the tilt residual is −0.159 to +0.036 Å (active) and −0.068 to +0.145 Å (inactive) across four backbones. Also mis-framed: the same code measures a crystal and a model, so there is no ruler offset to transfer — the residual **is** prediction error, which is the dependent variable |

---

## F. Blind spots — what this exercise did not look at

1. **No GPU-hour model.** Every number here is a count of predictions. RUN_MATRIX §1.4's cost bracket is **13× wide** and the two-chain rate is the unknown (:940 names recycles, diffusion steps and batching as the reason). If a 21-residue chain B is nearly free, T2/T4 are cheaper than they look; if it is 4×, T6's primary is not affordable. **One line from the pipeline team reorders this whole table.**
2. **Nothing varies the receptor construct.** `seqrec_trim.tsv` and `seqrec_icl3_audit.tsv` exist and no experiment crosses trim policy, ICL3 handling or termini with anything. T6's SHAM-A arm is the closest anyone gets to touching chain A. This is a real uncrossed factor and I could not size it today.
3. **The sampler's own stochasticity is untouched** apart from recycles — diffusion steps, noise scale, sample batching. §2.1 calls sampling depth "nearly free variance" without ever varying what generates it.
4. **Every experiment reads one prediction's state call.** Whether a single cell's 50 samples contain **both** states is asked only by G7, only at 4 cells. The ensemble-as-output question (E5.3) is in the catalogue and nothing here strengthens it.
5. **Block D's 42,180 predictions were mined only for depth.** I did not check what else those three corpora cross.
6. **Cross-species is a recording column nobody has crossed.** `g1_systems.csv` carries `receptor_organism` and `partner_species`; `g1_recording_spec.tsv` carries `cross_species_partner`. No arm varies it.
7. **The peptide-agonist receptors are excluded from every design** by D-2026-09-12-f, and they are exactly where a 21-mer partner and a 21-mer agonist compete for the same input modality (EDNRB's endothelin-1 is 21 residues and collides with ct21). Nothing examines that collision; it is excluded rather than measured.
8. **The arrestin question is untouched here.** E7.6 is built and unrun, and CATALOGUE §6 item 12 — whether our own reference set defines "active" partly by arrestin coupling, which would make that arm partly circular — is a free pass over `reference_audit.csv` that nobody has run.
9. **The 21→full-length placement-regime boundary** (§3.5) is addressed only by G1c/P1b as already designed; none of the thirteen improves on it.