# lu2026twostages

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NOT APPLICABLE` + reason where the field presupposes a conformational generator this paper is not.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–35)** and coincide with the
printed page numbers. Structure: p1 title + **Fig 1** + abstract + §1 Introduction, p2 §2 background +
**Fig 2** (ESMFold architecture), p3 **Fig 3** (patching setup) + §3 patching + dataset construction,
p4 **Fig 4** + single-block patching result, p5 **Fig 5** + §4.1 information flow + §4.2 charge,
p6 **Fig 6** + charge steering + controls, p7 **Fig 7** + §5.1 downstream pathways + §5.2 distance,
p8 **Fig 8** + §6 cross-model alignment, p9 cross-model patching + §7 Related Work + §8 Discussion,
p10–12 references, p13 App A protein background (**Figs 9, 10**), p14 **App B Limitations** + App C
impact, p14–15 App D compute (**Table 1**), p15 App E motif-detection algorithms + App F licenses,
p15–16 App G datasets, p16 App H recycling, p17 **Figs 11, 12** + App I.1 module patching,
p18 **Fig 13** + App I.2 touch masking, p19 **Fig 14** + App J cross-architecture information flow,
p20 App J cont., p21 **Figs 15, 16** + App K.1–K.2 charge, p22 **Fig 17** + App K.3 dose–response,
p23 **Fig 18** + App L late-block generalization, p24 **Fig 19** + App L.1 + App M, p25 **Figs 21, 22**,
p26 **Fig 23** + all-pairs results, p27 **Fig 24**, p28 **Fig 25**, p29–35 NeurIPS Paper Checklist.

---

## What this paper is, stated up front because it governs sections B, C and E

This is a **mechanistic-interpretability paper about the folding trunks of three structure-prediction
models**. It is not a conformational-sampling method, not a co-folding method, not a benchmark, and
it proposes no predictor. It runs three stock models (recycling disabled) tens of thousands of times
under activation patching, pathway ablation, representation steering and cross-model representation
substitution, and reads out **secondary-structure motif identity (β-hairpin vs helix-loop-helix) from
DSSP on the model's own output**.

**Two facts govern how this note should be cited.**

1. **The work is genuinely causal, not observational.** Unlike most interpretability papers in this
   corpus, the load-bearing results here are interventions: activation patching (~10,000 experiments),
   pathway freezing, sliding-window ablation, two steering directions with sign-controlled variants and
   a dose–response sweep, representation scaling, and cross-model patching in all six donor→receiver
   directions. Linear probes and CKA are present but are used as *descriptions* that the interventions
   then test.
2. **All three models are AlphaFold-lineage.** The paper says so itself for two of the three pairings.
   The convergence claim is therefore convergence *within* a design family, not across genuinely
   independent designs. See the dedicated section below — this is the single most important caveat
   for anyone using this paper to argue that a trunk-level intervention transfers between models.

### Exactly which models were examined, and how independent they are

| model | what it is, in the paper's words | trunk | input modality | seq2pair location |
|---|---|---|---|---|
| **ESMFold** [Lin et al. 2023] | PLM front-end (ESM-2, 33 layers) + folding trunk + IPA structure module; the trunk's triangular updates and the IPA structure module are both cited to Jumper et al. 2021 (p2) | 48 blocks (p2) | **single sequence, no MSA** (p3) | every block, bidirectional (p3) |
| **OpenFold** [Ahdritz et al. 2024] | "a faithful reimplementation of AlphaFold2 with a 48-block Evoformer trunk" (p3) | 48 blocks | MSA (p3) | every block, bidirectional (p3) |
| **Boltz-1** [Wohlwend et al. 2024] | "an AlphaFold-3-style architecture with an MSA module followed by a 48-block Pairformer" (p3) | MSA module treated as blocks 0–3 + 48 Pairformer blocks (indexed 4–51, p20) | MSA (p3) | **confined to the upstream MSA module, blocks 0–3; no seq2pair write-back inside the Pairformer** (p3, p19) |

**Verbatim, p3:** "OpenFold [Ahdritz et al., 2024] is a faithful reimplementation of AlphaFold2 with a
48-block Evoformer trunk. Boltz-1 [Wohlwend et al., 2024] is an AlphaFold-3-style architecture with an
MSA module followed by a 48-block Pairformer."

**Verbatim, p3:** "ESMFold and OpenFold update both representations bidirectionally throughout the
trunk (seq2pair and pair2seq in every block), Boltz-1 confines seq2pair to its upstream MSA module
(which we treat as blocks 0–3 of the trunk). Within the remaining Pairformer blocks, the only
cross-representation pathway is pair2seq: sequence representations are updated by pair-biased
self-attention and an MLP, but never write back into the pairwise track."

**The paper itself attributes the strongest cross-model similarity to shared lineage.** Verbatim, p24:
"ESMFold ↔ OpenFold shows the highest overall similarity (CKA > 0.8 throughout the middle of the
trunk), **consistent with their shared lineage from the AlphaFold2 architecture**." And verbatim, p8:
"OpenFold aligns to ESMFold more tightly (R² ≈ 0.9) than Boltz-1 does (R² ≈ 0.75), **consistent with
their closer architectural relationship**."

**Assessment of architectural independence — the sceptical read this note exists to preserve.**
The three models are *not* architecturally independent. All three are built on the same AF2/AF3
template: paired sequence + pairwise (`s`, `z`) tracks, 48 trunk blocks in every case, triangular
multiplicative and triangular-attention pairwise updates, pair-biased sequence self-attention, and an
IPA-style structure module. OpenFold *is* AlphaFold2. Boltz-1 is an AlphaFold3-style Pairformer.
ESMFold's folding trunk is an AF2-derived trunk with a PLM in place of the MSA front-end. The genuine
axes of variation the paper exploits are (i) **input modality** (single sequence vs MSA), (ii) **where
seq2pair sits** (in-trunk vs upstream MSA module), and (iii) **training data and procedure**. Those are
real but they are variations *within* the AlphaFold design family, not across families.

The paper is honest that the family boundary is untested — verbatim, p14: "Our analysis applies to
folding models built around an iterative sequence/pairwise trunk. Recent architectures such as
SimpleFold [Wang et al., 2025] predict structure without an explicit pairwise representation. Whether
such models implement an analogous two-stage computation of biochemistry and geometry in some other
form is an open question."

**Consequence for the corpus.** The finding is strong evidence that a trunk-level intervention
transfers *among AF2/AF3-style trunks* — which is most of the corpus (AF2, AF3, OpenFold, Boltz, Chai,
Protenix, OF3 all share this template). It is **not** evidence of architecture-independence in the
general sense, and it should not be cited as such. There is also no null model for what CKA/Procrustes
alignment two *untrained* trunks of these architectures would show (see `controls_run`, missing
controls).

### The two-stage claim, and where in the trunk each thing lives

**Stage 1 (early blocks, ESMFold/OpenFold k≈0–7, Boltz-1 blocks 0–3):** sequence-side computation
commits motif identity, and biochemical features (charge) are written from `s` into `z` via `seq2pair`.
**Stage 2 (middle-to-late blocks, k≈25–40):** `z` carries geometry; distance and contact information are
linearly decodable from it, `pair2seq` broadcasts the contact map into sequence attention, and the
structure module renders `z`'s magnitudes into 3D distances.

Verbatim locality claims, with pages — **this is the field to read if you want to know where an
intervention should act**:

| claim | verbatim | page |
|---|---|---|
| the trunk, not the encoder or structure module, is the decision site | "In ESMFold, patching at the encoder or structure module is substantially less effective (App. I.1), establishing the trunk as the critical site of structural decision-making." | p3–4 |
| same, sharper | "Patching in the folding trunk is the only place where hairpins consistently transfer." | p17, Fig 12 caption |
| the two windows | "Sequence patches are effective in early blocks (k ∈ {0, . . . , 7}), with success rates peaking around 40% at block 0 and declining sharply thereafter. Pairwise patches show the opposite pattern, becoming effective starting around block 25 and peaking near block 35 in ESMFold and OpenFold." | p4 |
| cross-architecture generality of the windows | "This pattern arises in all three models despite differences in training data, architectural details, and input modality, suggesting folding trunks share a common computational strategy: early blocks commit to motif identity through sequence-side computation, later blocks refine motif geometry through pairwise computation." | p4 |
| the write-in window | "After sequence patching at block 0, z rapidly becomes donor-like within the first ≈10 blocks, then changes only gradually (Fig. 4a). Blocking seq2pair during blocks 0–10 prevents this shift entirely, while directly patching z at block 0 does not persist: the pairwise state returns toward the target trajectory. This confirms a short early \"write-in\" window during which sequence information is consolidated into z via seq2pair." | p4–5 |
| pathway magnitudes | "The seq2pair contribution to z peaks in the first ten blocks and declines through the middle of the trunk, while pair2seq is small in early blocks and rises sharply in late blocks (Fig. 4b)." | p5 |
| where charge enters z | "The location of the rise tracks each model's seq2pair pathway: blocks 0–15 in ESMFold and OpenFold, and the narrower window of blocks 0–3 in Boltz-1, where the seq2pair pathway lives in the MSA module before the Pairformer trunk begins." | p22 |
| charge leaves again late | "In all three models, z probe accuracy declines somewhat in late blocks (35–47), suggesting charge information is progressively transformed into more geometric features as the trunk shifts to stage 2 computation." | p22 |
| where distance lives | "Probe accuracy is low at block 0 in all three models, where z is initialized primarily with positional embeddings, but rises through the trunk and plateaus at R² ≈ 0.9 in late blocks (Fig. 7a). Distance is therefore linearly accessible from z in late blocks across all three architectures." | p7 |
| where distance steering works | "Hairpin induction peaks when steering middle-to-late blocks, where high probe accuracy coincides with the stage 2 effective window." | p8 |
| where contacts are readable | "In middle and late blocks, the bias cleanly separates contacts from non-contacts (Fig. 6a) … Late-block sequence attention is therefore preferentially routed along the contact map encoded in z." | p7 |
| where cross-model patches act | "In every direction, patching reproduces the late-block pairwise window observed in within-model patching: cross-model patches induce the target motif only when applied to blocks 25–40 of the receiving model, matching the pairwise stage identified in §3 and App. J." | p26 |
| stage 1 locus is architecture-dependent | "…these results support the interpretation that stage 1, the biochemical write-in from sequence into pairwise space, is a shared property of all three folding trunks, with its location varying based on where each architecture implements its seq2pair pathway." | p20 |
| Boltz-1's stage-2 window is anomalously wide | "Boltz-1's pairwise patching window is broader than ESMFold's or OpenFold's, extending across nearly the entire trunk." (attributed on p19–20 to the absence of seq2pair write-back in the Pairformer) | p19 |

### REPRESENTED vs CAUSALLY ESTABLISHED

**Established causally (intervention run, effect measured on the model's own output):**

| intervention | what was manipulated | readout | page |
|---|---|---|---|
| Full-trunk activation patching (seq + pair, all 48 blocks) | donor `s` and `z` over the motif region | DSSP motif presence in output | p3, p17 |
| Single-block patching, sequence-only or pairwise-only | `s` or `z` at one block | DSSP motif presence | p4, p19 |
| Module-level patching (ESM-2 encoder 33 layers; IPA structure module 8 iterations) | module activations | DSSP motif presence | p17 |
| Freezing `seq2pair` during blocks 0–10 (Boltz-1: 0–3) | pathway disabled | interpolation coefficient α of `z` (Eq. 3) | p4–5, p20 |
| Sliding-window ablation of `seq2pair` (window 15) | pathway removed over a window | DSSP motif formation rate | p5, p20 |
| Sliding-window ablation of `pair2seq` (control) | pathway removed | DSSP motif formation rate | p5, p20 |
| Charge steering, `s'ᵢ = sᵢ ± α v_charge`, α = 3σ, window 15 | difference-in-means charge direction in `s` | DSSP hairpin induction rate | p6 |
| Same-charge / opposite-charge steering (4 sign conditions) | as above, sign-controlled | cross-strand Cα distance (Å) | p6, p22 |
| Charge steering dose–response sweep | α from ~0 to ~1 std-DoM | cross-strand Cα distance (Å) | p22 |
| Distance steering, `z'ᵢⱼ = zᵢⱼ − α ŵ`, α = 20σ, window 10, target 5.5 Å | linear distance-probe weight direction in `z` | DSSP hairpin induction + cross-strand distance | p8 |
| Scaling `z` (or `s`) by a factor in [0,2] before the structure module | representation magnitude | mean pairwise Cα distance (Å) | p7, p23 |
| Cross-model patching after whitened Procrustes projection, all 6 directions | donor `z` from another model | DSSP motif presence | p9, p26 |
| Input-intervention baseline (literal donor-sequence substitution) | raw amino acid sequence | DSSP hairpin presence | p18 |

**Represented only (correlational, read-out, no intervention):** the linear charge direction ROC-AUC
across blocks (p20–21); charge probes on `z` and on `seq2pair` output (p21–22); linear distance probes
on `z` (p7); `pair2seq` bias contact ROC-AUC and bias heatmaps (p7, p23–25); pathway contribution
norms (p5); CKA between models (p8, p24); Procrustes projection R² (p8, p25).

**Note the paper's own framing, p9, verbatim:** "These representations are not merely correlational:
they are causally operative and shared across architectures." That statement is supported for charge
and distance in the sense that steering along those directions changes the output motif. It is *not*
supported by a norm-matched random-direction control (never run — see `controls_run`), so
"the model uses *this* direction" is stronger than what was tested; what was tested is "perturbing
along this direction, with the predicted sign, produces the predicted geometric effect."

---

## A. Identity

| field | value |
|---|---|
| `citekey` | `lu2026twostages` |
| `doi` | **arXiv:2602.06020v3 [cs.LG]**, 24 Jun 2026 (stamped in the left margin of p1). No journal DOI. |
| `year` | 2026 |
| `venue` | **Preprint** — the footer of p1 reads "Preprint." Formatted for NeurIPS and carries the full NeurIPS Paper Checklist (pp29–35), and the code link is anonymized (`anonymous.4open.science`, p14), so this is an under-review NeurIPS submission posted to arXiv. Tagged `preprint`. |
| `title` | Two Stages of Folding: Convergent Mechanisms in AI Protein Folding Trunks |
| `authors` | Kevin Lü (Northeastern, lead), Jannik Brinkmann (Northeastern / TU Clausthal), Stefan Huber (Harvard), Aaron Mueller (Boston University), Yonatan Belinkov (Harvard / Technion), David Bau (Northeastern), Chris Wendler (Northeastern, corresp.) — p1 |

## B. Scope

| field | value |
|---|---|
| `system` | **general protein** — no protein family is targeted. Datasets are CATH Class 1 ("mainly α") domains and PISCES-culled X-ray chains (p15–16). Named examples are only PDB 6rwc (β-sheet) and 1l0s (left-handed β-helix), used for bias-map visualisation (p26). |
| `n_targets` | **200 activation-patching targets** (100 α-helical + 100 hairpin, lengths 100–400 residues, p16), drawn against **≈130,000 donor motif regions** from the PDB (p3), with 10 donors sampled per motif giving **≈10,000 patching experiments** (p3). Other sets: 200 α-helical proteins for the charge direction (p5), filtered from 5,000 CATH Class 1 chains (p16); 11,652 PISCES chains for hairpin mining (p16); 400 train / 200 eval proteins for distance probes (p7); ~500 steering cases per model (p6); 500 sampled β-hairpins for same-charge steering (p6); 600 proteins for the structure-module scaling analysis (p7); ≤40-residue single-motif proteins for the dose–response (p22). **No claim of generality beyond the two motifs studied is made** — the authors bound it themselves on p14. |
| `method_class` | **other** — mechanistic interpretability: activation patching + linear probing + representation steering + cross-model representational alignment (whitened Procrustes) and cross-model activation substitution. Not any of the corpus's conformational method classes. |
| `backbones` | **ESMFold, OpenFold, Boltz-1** — three head to head, in every analysis. Tag `multi-backbone`. Architectural relationships recorded in full in the section above; all three are AlphaFold-lineage. |
| `templates` | **NOT REPORTED** — templates are never mentioned as an input anywhere in the paper. ESMFold is template-free by construction; for OpenFold and Boltz-1 the template setting is never stated (protocol described p3, datasets p15–16). Do not assume off. |
| `msa_handling` | **DUAL — none + full (unspecified).** ESMFold takes a single sequence with no MSA; OpenFold and Boltz-1 take an MSA: "Both take a multiple sequence alignment (MSA) as input rather than a single sequence" (p3). **How those MSAs were built — search tool, database, depth, date — is NOT REPORTED anywhere**, which is a real reproducibility gap for the two MSA models given that MSA depth is known to move trunk representations. Not subsampled, not clustered, not state-filtered. Recycling is disabled throughout: "To simplify causal analysis, we disable recycling; for the short proteins considered, recycling provides minimal improvements (App. H)." (p3) |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **NOT APPLICABLE — no conformational generator.** The paper produces one deterministic structure per intervention condition (recycling disabled, p3); it never samples an ensemble, never targets two conformational states of one protein, and never scores state assignment. The two "states" toggled are **secondary-structure motifs of a local window** (β-hairpin vs helix-loop-helix, 12–25 residues, p14), not conformational states of a protein. If a single value is needed for the index: single-state per condition. |
| `structural_priors_used` | Substantial and entirely legitimate — all at design time, none in a prediction pipeline. (1) **PDB deposited structures** define every motif region: DSSP is run on deposited structures to identify motifs and align intervention windows (p3, p15). (2) **CATH Class 1 ("mainly α") domain list** selects the helical dataset (p15–16). (3) **PISCES culling set** `cullpdb_pc25.0_res0.0-2.5_len40-10000_R0.3_Xray_d2025_02_19_chains11652` (25% identity, X-ray, ≤2.5 Å, R ≤ 0.3) selects hairpin-bearing chains (p16). (4) **Deposited Cα coordinates supply the probe labels** — true pairwise Cα distance for distance probes and the 8 Å Cα contact definition (p7, p23). (5) **Structural-biology literature fixes two constants**: the 5.5 Å cross-strand Cα target distance is taken from Brändén & Tooze 1999 (p8), and the salt-bridge rationale for charge complementarity from Ciani et al. 2003 (p5). (6) **Motif-detection thresholds** (App E, p15) encode textbook hairpin/HLH geometry. None of this is a defect; it is what makes the intervention interpretable. |
| `oracle_leakage` | **Overall: NONE FOUND on pipeline routes 1–5; a genuine selection effect on route 6; design-level (route 7) use is present and explicit.** Route by route: <br>**(1) Structures used as input or template — NONE FOUND.** No structure is given to any model as input; templates are never mentioned. What crosses into the forward pass is a *donor activation tensor*, computed by running the donor's **sequence** through the model, not the donor's coordinates. Protocol described p3: "We run both proteins through the folding trunk, extracting the sequence representation s^(k) and pairwise representation z^(k) at each block k. During the target's forward pass, we replace representations in the target's motif region with the donor's." <br>**(2) State annotations from a curated database driving templates or alignments — NONE FOUND as a pipeline route; present as dataset curation only.** DSSP, CATH and PISCES are used to *select and label* the protein sets (p15–16), not to bias any prediction. No GPCRdb/KLIFS/Kincore-style state annotation is used, and no alignment or template is state-annotated. <br>**(3) Cluster labels derived from known states — NONE FOUND.** No clustering is performed anywhere; protocol p3, p15–16. <br>**(4) Hyperparameters, sweeps, seeds or stopping criteria tuned against known states — NONE FOUND for the evaluation-set sense, but with a caveat that must be recorded.** The two constants that could have been tuned are not: the 5.5 Å distance target is taken from a textbook ("We choose 5.5Å as our target, the typical Cα–Cα spacing for cross-strand contacts in antiparallel β-sheets [Brändén and Tooze, 1999]", p8) and the 8 Å contact threshold is standard. **However, how the steering strengths α = 3σ (charge, p6) and α = 20σ (distance, p8) and the ablation/steering window sizes (15, 15, 10) were chosen is NOT REPORTED.** The dose–response sweep (p22) is run on a *separate* small single-motif set, explicitly to isolate the effect, so the sweep range itself is not fitted on the reported evaluation set — but the absence of any stated selection protocol for α means a reader cannot verify that the reported α was not picked because it worked. <br>**(5) Success defined post hoc by RMSD or TM to a structure they had — NONE FOUND, and this is the paper's cleanest rigour property.** Success is presence of the donor motif in the model's own output under an explicitly specified algorithm — DSSP codes, strand ≥2 residues, loop 0–5, adjacency for hairpins; DSSP code H, helix ≥4 residues, loop 2–8, adjacency for helix-loop-helix (App E, p15). No reference structure of a "correct answer" is ever compared against. <br>**(6) Best/worst model labels assigned against a held reference — NONE FOUND against a reference, but a real outcome-conditioned selection is present.** The single-block localisation analysis is run only on cases that already succeeded under a different intervention: verbatim, p4, "we repeat the patching experiment but intervene at a single block, patching either sequence or pairwise representations alone (**restricted to the ≈4,000 donor–target pairs where full patching was successful**)." The detailed §4.1 flow analysis narrows further: "We present the analysis in detail for ESMFold using **400 successful cases of block-0 sequence patching**" (p4). This is selection on the outcome of a prior intervention, not on a deposited structure, so it is not oracle leakage in the corpus sense — but every reported single-block success rate is conditional on full-trunk patching having worked, and the unconditional rate is lower and never given. <br>**(7) Design-level oracle use — PRESENT and explicit.** The expected answer is declared before the result is read, throughout. The donor→target design fixes what should appear ("we observe whether the output structure contains the donor motif in the patched region", p3); the charge intervention is constructed to reproduce a known biophysical effect ("the construction mimics the cross-strand electrostatic complementarity found in natural hairpins", p6); and the control conditions state their expected signs in advance ("**expecting** strands to repel … **expecting** strands to attract", p22). This is hypothesis-driven experimental design and is the *weaker*, design-level form — it is not pipeline leakage and must not be conflated with it. Tag `design-level-oracle`, not `oracle-leak`. |
| `prospective` | **no** — retrospective throughout. Every protein comes from an already-deposited PDB/CATH/PISCES set (p15–16); the models are pre-trained checkpoints; nothing is predicted ahead of an unknown answer and nothing is tested experimentally. The axis is partly ill-fitting: this paper makes no structural predictions to be prospective *about*. Its interventional design does mean the *effects* are not cherry-picked post hoc from an observational sweep, but the expected direction of every effect was declared in advance (route 7). |
| `state_metric` | **DUAL — binary predicate + continuous coordinate.** (a) **Binary predicate**, fully operationalised with stated thresholds, App E p15: hairpin = DSSP E/B, each strand ≥2 residues, connecting loop 0–5 residues, strands sequentially adjacent; helix-loop-helix = DSSP H, each helix ≥4 residues, loop 2–8 residues, helices sequentially adjacent. Justification of the thresholds is **NOT REPORTED** — they are asserted, not derived or sensitivity-tested. (b) **Continuous coordinates** used alongside: mean cross-strand Cα distance in Å (p6, p22), mean pairwise Cα distance in Å (p7, p23), interpolation coefficient α of `z` toward the donor (Eq. 3, p4), probe R² and ROC-AUC (p7, p20–21, p23). No `visual-metric` call anywhere — even the structure renders (Fig 18, p23) are backed by the quantified dose–response of Fig 17. |
| `metric_saturation` | **Yes, numerically, in two places, and both are acknowledged by the authors.** (1) **Charge steering dose–response saturates**, verbatim p22 (Fig 17 caption): "All three models show effects emerging above a threshold around 0.4 std-DoM units and **saturating thereafter**, indicating that charge functions as a continuous biochemical signal…" — so the reported α = 3σ operating point sits far into the saturated regime, and effect sizes reported at α = 3σ are ceiling values, not slopes. (2) **Charge-direction ROC-AUC ceilings**: ESMFold and OpenFold "rise to near 1.0 within the first 5–10 blocks" and stay there for the rest of the trunk (p21), so that curve carries no information about blocks 10–47. Non-saturating: patching success rates (max ≈62.5%, p17), Procrustes R² (plateau ≈0.9), CKA (max ≈0.9). Figure-level obscuring is recorded in `hides`, not here. |
| `directional_control` | **Yes — the paper's whole point is that the output motif can be instructed, and it names four independent handles.** (1) **Donor activation at a chosen block** — sequence patch in blocks 0–7 or pairwise patch in blocks 25–40 sets which motif appears; the reverse direction (helix donor into hairpin target) works too: "The reverse setup (helix donor, hairpin target) is identical with motif roles swapped" (p3) and "The two-stage structure holds for both hairpin and helix induction" (p9). (2) **Charge direction with per-strand sign** — `s'ᵢ = sᵢ + αv_charge` on one flank and `− αv_charge` on the other induces hairpins; same-sign on both flanks pushes strands apart (p6). (3) **Distance-probe weight direction with sign and target distance** — steering `z` toward 5.5 Å pulls cross-strand pairs into contact (p8). (4) **Scalar magnitude of `z` before the structure module** — expands or contracts the whole predicted structure monotonically (p7, p23). None of these is a conformational-state handle in the corpus's sense (no partner, ligand, nanobody, template or MSA manipulation is used anywhere). |
| `anti_memorization_design` | **NONE.** There is no post-cutoff set, no date-based holdout, and no training-cutoff discussion for any of the three models. Model training cutoffs are never stated. What *does* exist is ordinary train/test hygiene for the probes, which is a different thing: 400 training / 200 evaluation proteins for the distance probes (p7); a probing test set of held-out hairpins disjoint from the training hairpins; and, verbatim p16, "Hairpin sequences were further filtered to ensure ≤ 25% pairwise sequence identity to any α-helical sequence or previously selected hairpin, and to exclude exact matches to donor sequences used in activation patching." That guards against probe overfitting and donor/target overlap, not against the models having memorised the PDB. |
| `anti_memorization_control` | **NONE RUN.** No arm of this paper tests whether the effects survive on structures the models cannot have seen. Given that the entire dataset is X-ray PDB entries culled up to 2025-02-19 (p16), essentially every protein used is plausibly in-training for all three models. Whether the two-stage structure would appear on post-cutoff or synthetic sequences is untested and unmentioned. |
| `controls_run` | See the dedicated table below — 17 rows, plus a list of the controls that are missing. |
| `confidence_as_discriminator` | **No — pLDDT is never used to judge correctness, and this is deliberate.** Success is DSSP-based throughout (App E, p15). pLDDT appears exactly once, as a limitation on the *products* of the interventions, verbatim p14: "The counterfactual structures we produce show low pLDDT, and inverse folding fails to recover sequences that fold to these structures. Interventions can also create unrealistic proteins with steric clashes or chain breaks." No pTM, ipTM, or confidence filtering anywhere. Not tagged `confidence-as-discriminator`. **Read this carefully before citing the paper for transferable interventions: the intervention reliably changes the motif DSSP reports, and reliably produces a structure the model itself is not confident in.** |

### `controls_run` — every control arm actually run

| control | what it rules out | page |
|---|---|---|
| `pair2seq` sliding-window ablation, run alongside the `seq2pair` ablation | Generic disruption: that removing *any* inter-representation pathway kills motif formation. Verbatim p5: "ablating pair2seq has little effect at early window positions, confirming that the loss of structure is specific to the sequence-to-pairwise pathway rather than a generic disruption from ablating either inter-representation pathway." Replicated in all three models. | p5, p20 |
| ESM-2 encoder patching (all 33 layers) | That structural commitment happens in the sequence encoder. Encoder patching induces hairpins in **0.6%** of cases. | p17 (Fig 12), p17 |
| Structure-module (IPA) patching at each of 8 iterations | That the decision is made downstream of the trunk. Structure-module patching: **4.6%**. | p17 (Fig 12), p17 |
| Input-intervention baseline: literal substitution of the donor's amino acid sequence into the target before the forward pass | That trunk patching merely reproduces what the raw sequence already carries. Input intervention: **2.6%**, far below trunk patching's 38.3%/62.5%. Verbatim p18: "input intervention induces hairpins at a lower rate than trunk patching, indicating that the learned representations in the trunk carry information beyond what is present in the raw sequence." | p17 (Fig 12), p18 |
| Direct pairwise patch at block 0, compared against sequence patch at block 0 | That the early shift in `z` is a trivial consequence of writing into `z`. The direct `z` patch "does not persist: the pairwise state returns toward the target trajectory." | p4–5, p19–20 |
| `seq2pair` freeze during the write-in window (blocks 0–10; Boltz-1 0–3) | That `z` would drift donor-ward regardless of the pathway. "Blocking seq2pair during blocks 0–10 prevents this shift entirely." | p4–5, p20 |
| Charge direction trained on **helical proteins only** | Confounding the charge direction with hairpin-specific geometry. Verbatim p5: "using helical proteins avoids confounding charge with the specific distance patterns present in beta hairpins". | p5 |
| Sign-controlled steering: same-charge on β-hairpins (Pos-Pos, Neg-Neg) and opposite-charge on α-helices (Pos-Neg, Neg-Pos) | That any perturbation of `s` collapses/creates strands. The four conditions produce the *predicted signs*: same-charge increases cross-strand distance ≈10 Å; opposite-charge decreases it. | p6, p22 |
| Charge dose–response sweep on ≤40-residue single-motif proteins | An all-or-nothing artefact, and structural-context confounds. Produces a smooth monotonic curve with a threshold ≈0.4 std-DoM in all three models. | p22 (Fig 17) |
| Scaling `s` instead of `z` before the structure module | That any magnitude change moves output distances. Verbatim p23: "scaling z produces a monotonic, approximately linear change in output distance, while scaling s produces no detectable change… z is the geometric channel; s is not." | p7, p23 |
| Shuffled-correspondence Procrustes baseline, every block, every pairing, both directions | That cross-model R² comes from matched dimensionality or marginal statistics. Shuffled R² sits near the random-orthogonal floor (≈ −1 for whitened Procrustes). | p8, p25–26 |
| Five-way alignment-method comparison under shuffling (ridge, CCA, unwhitened Procrustes, whitened Procrustes, random orthogonal) | Method-specific artefact fitting. Ridge and CCA reach shuffled R² 0.1–0.25, i.e. they *do* fit artefacts; whitened Procrustes does not, which is why it was chosen. | p26–27 (Fig 25, p28) |
| Within-model patching (ESMFold→ESMFold) run as the reference arm for cross-model patching | That cross-model rates are meaningful in isolation. Gives the ceiling: 22% within-model vs 15%/10% cross-model. | p9, p26 |
| Recycling-impact study (App H) | That disabling recycling distorts the results for the protein sizes used. Short (<100 aa) proteins converge within one recycle; medium/long do not — so the control supports the choice only for short proteins, and targets here run to 400 residues. | p3, p16, p17 (Fig 11) |
| Reverse-direction motif induction (helix donor → hairpin target as well as hairpin donor → helix target) | That the two-stage pattern is a β-hairpin idiosyncrasy. "The two-stage structure holds for both hairpin and helix induction." | p3, p9 |
| Standard-intra vs touch pairwise masking | That the late-block window boundary is a fact about the motif rather than about how far patched information must propagate. Touch masking widens the effective window to blocks 25–47 and raises success 38.3% → 62.5%. | p18 (Fig 13) |
| Probing-dataset identity filtering (≤25% pairwise identity; donor sequences excluded) | That probe accuracy reflects sequence overlap with the patching donors/targets rather than general representational structure. | p16 |

**Controls that are missing, ordered by how much they matter for the claims this paper is cited for:**

1. **No untrained / randomly-initialised model baseline for the convergence claim.** This is the most
   important gap. The convergence argument rests on CKA and Procrustes R² between three trunks that
   share an architectural template (48 blocks, `s`/`z` tracks, triangular updates). The shuffled-
   correspondence control rules out *dimensional* artefacts; it does **not** rule out
   *architecture-induced* similarity. Two randomly-initialised trunks of these architectures, or two
   OpenFold checkpoints trained from different seeds, would be the controls that separate "converged
   through learning" from "similar because built the same way." Neither is run.
2. **No norm-matched random-direction steering control.** Charge and distance steering are never
   compared against steering along a random unit direction of the same magnitude. The sign-controlled
   conditions (row 8 above) are a good partial substitute — a random direction would not produce
   sign-consistent repulsion/attraction — but they do not establish that the *specific* probe/DoM
   direction is privileged over an arbitrary one of matched norm.
3. **No null-donor patching arm.** Patching a donor region that contains neither motif, or a shuffled/
   noise tensor of matched statistics, is never reported. The module comparison (encoder 0.6%,
   structure module 4.6%, input intervention 2.6%) supplies a de facto low baseline, but not a
   same-site null.
4. **No anti-memorization arm at all** (see `anti_memorization_control`).
5. **No architecture outside the AlphaFold family** — acknowledged by the authors as open (p14).
6. **No MSA-depth control** for the two MSA-driven models, despite MSA construction being unreported.

## D. Claims

| field | value |
|---|---|
| `central_conclusion` | Across ESMFold, OpenFold and Boltz-1, the folding trunk runs the same two-stage computation: early blocks write biochemical information (specifically residue charge) from the sequence track into the pairwise track through each architecture's `seq2pair` pathway and thereby commit motif identity, while middle-to-late blocks develop the pairwise representation into an approximate distance/contact map that the `pair2seq` bias and the structure module read out geometrically. Both stages are established by intervention, not only by probing, and the pairwise representations of the three models are linearly alignable (whitened Procrustes) and functionally substitutable at the corresponding stage in all six donor→receiver directions. The authors read this as convergence on a shared representational organisation despite differing architectures, inputs and training. |
| `necessity_claims` | **Verbatim, with pages.** <br>• p5: "When the ablation window starts in early blocks (0–7), ablating seq2pair during block-0 sequence patching reduces hairpin formation to near zero; the effect recovers fully once the window starts past block 12, **indicating that seq2pair is specifically required during the early write-in phase**." <br>• p4–5: "**Blocking seq2pair during blocks 0–10 prevents this shift entirely**, while directly patching z at block 0 does not persist: the pairwise state returns toward the target trajectory." <br>• p20: "In all three models, sequence patching at block 0 shifts z toward the donor within the first ≈10 blocks, while **freezing seq2pair during this window prevents the shift entirely**; direct pairwise patches at block 0 do not persist." <br>• p18: "The result highlights that **successful structural transfer requires not only the correct intra-motif geometry but also sufficient time (i.e., remaining blocks) for the model to integrate the patched region with the rest of the chain**." <br>• p17: "Despite replacing the encoder's learned sequence representations, encoder patching rarely induced hairpin formation (Fig. 12), suggesting that **the encoder representations alone do not determine secondary structure**." <br>• p17: "Structure module patching was similarly ineffective: the IPA operates on representations that have already been shaped by the trunk, and **patching at this late stage cannot override the geometric information established earlier**." <br>• p17 (Fig 12 caption): "**Patching in the folding trunk is the only place where hairpins consistently transfer.**" <br>• p3–4: "In ESMFold, patching at the encoder or structure module is substantially less effective (App. I.1), **establishing the trunk as the critical site of structural decision-making**." <br>• p23: "The direction and qualitative shape are preserved across architectures: **z is the geometric channel; s is not**." <br>• p14 (limitation, impossibility form): "The counterfactual structures we produce show low pLDDT, and **inverse folding fails to recover sequences that fold to these structures**." <br>• p14: "**Standard folding models predict a single static structure and do not naturally capture this kind of conditional behavior**, but our finding that charge is encoded along a manipulable linear direction suggests a path forward". |
| `novelty_claims` | **Verbatim, with pages.** <br>• p1: "We ask whether physically interpretable decisions can be identified within the internal computations of these models, **conducting the first cross-architectural mechanistic account of three modern folding models**: ESMFold [Lin et al., 2023a], OpenFold [Ahdritz et al., 2024], and Boltz-1 [Wohlwend et al., 2024]." <br>• p9: "**We have conducted the first cross-architectural mechanistic analysis of protein folding trunks**, revealing a two-stage computational structure that arises consistently across ESMFold, OpenFold, and Boltz-1." <br>• p9: "**These representations are not merely correlational: they are causally operative and shared across architectures.**" <br>• p9: "…**our finding that pairwise representations are linearly alignable across folding architectures provides evidence for this convergence in a domain beyond vision and language**." <br>• p9 (novelty framed against prior work): "Prior interpretability work on protein folding models has focused largely on sequence encoders… Gut and Lemmin [2025] analyzed AlphaFold2 behaviorally rather than mechanistically. **We instead analyze the folding trunk itself through causal interventions, localizing where in the trunk structural decisions are made rather than only what features encoders represent.**" <br>• p1 (abstract, the convergence claim itself): "Together, these results suggest that folding trunks with different architectures, inputs, and training procedures converge on a shared representational organization for mapping sequence chemistry into spatial geometry." |
| `stated_limits` | All in App B, p14, plus two more elsewhere. (1) **Motif scope**: "We study hairpins and helices: relatively local motifs within 12–25 residue windows. Whether the two-stage structure extends to larger motifs (beta sheets, long-range domain contacts) remains to be tested; long-range contacts might require different mechanisms." (2) **Architecture scope**: "Our analysis applies to folding models built around an iterative sequence/pairwise trunk. Recent architectures such as SimpleFold [Wang et al., 2025] predict structure without an explicit pairwise representation. Whether such models implement an analogous two-stage computation… is an open question." (3) **Physical viability**: "Our patching experiments demonstrate that representations can be transplanted, but translating patched structures back to viable sequences remains open. The counterfactual structures we produce show low pLDDT, and inverse folding fails to recover sequences that fold to these structures. Interventions can also create unrealistic proteins with steric clashes or chain breaks." (4) **Unexplained asymmetry**, p26: "For each pairing, the two directions of patching produce slightly different success rates even when projection R² is similar in both directions. We do not have a definitive explanation for this asymmetry… We leave a more careful investigation of cross-model patching asymmetry to future work." (5) **Partial code release**, p31: "We release code for a single model to keep the reproduction environment lightweight; the OpenFold and Boltz-1 replications apply the same methodology to publicly available model checkpoints, and the full multi-model pipeline will be released upon publication." |
| `stance` | **`precedent` on findings + `contrast` on rigour** (provisional; the user's call). **Precedent**: it is the closest thing in the corpus to a direct demonstration that a trunk-level activation intervention localises to the same block window across models and that a pairwise-track representation from one model can be linearly mapped into another and still do its job — exactly the load-bearing premise for cross-model trunk interventions. **Contrast**: the convergence claim is made across three AlphaFold-lineage trunks with no untrained/architecture-matched null and no non-AF architecture; cross-model patching succeeds at only 10–17%; and the intervention's outputs are explicitly low-pLDDT and not sequence-realisable, so "the intervention transfers" is true at the representation level and unproven at the level of usable structures. |

## E. Quantitative comparators

| field | value |
|---|---|
| `n_predictions` | **Samples per target**: 10 donors sampled per motif per target (p3). **Targets**: 200 for patching (100 helical + 100 hairpin, p16). **Total**: "yielding ≈10,000 patching experiments" (p3), of which "Approximately 40% of patches (≈4,000 cases) successfully produce the donor motif" (p3); the detailed flow analysis uses "400 successful cases of block-0 sequence patching" (p4). Other totals: ~500 steering cases per model (p6); 500 sampled β-hairpins for same-charge steering (p6); 600 proteins for structure-module scaling (p7); 400 train / 200 eval for distance probes (p7). All three models receive the same sweeps (p14). Compute: ~1,000–1,500 GPU-hours, 2–3 weeks wall-clock on 2× RTX A6000 (p15). |
| `comparable_to_ours` | *(left empty by extractor per v3)* |
| `si_in_scope` | **SI HELD** — Appendices A–M (pp13–28) and the NeurIPS checklist (pp29–35) are all inside this 35-page PDF; there is no external supplement. **But note a distinct gap: the paper contains no numeric results table at all.** The only table is Table 1 (p15), which reports wall-clock times. Every quantitative result below is either an approximate value stated in prose (with the authors' own "≈", "around", "near" hedges) or read off a figure axis; per-model, per-block values are not tabulated anywhere and cannot be recovered from the PDF. |

### `metrics_reported`

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Full-trunk patching success (seq+pair, all 48 blocks, ESMFold, standard intra mask) | ≈40% (≈4,000 of ≈10,000); exact bar value 38.3% | % of donor–target pairs | DSSP donor-motif presence in target region | p3, p17 (Fig 12), p18 |
| Full-trunk patching success, touch mask | 62.5% | % | same | p17 (Fig 12) |
| Structure-module (IPA) patching success | 4.6% | % | same | p17 (Fig 12) |
| Input-intervention baseline (literal donor sequence substitution) | 2.6% | % | same | p17 (Fig 12) |
| ESM-2 encoder patching success | 0.6% | % | same | p17 (Fig 12) |
| Single-block **sequence** patching, peak | ≈40% at block 0 (ESMFold); 40–45% across the three models; effective window k ∈ {0,…,7} (0–8 in Fig 13) | % | same | p4, p19 |
| Single-block **pairwise** patching, effective window | onset ≈block 25, peak ≈block 35 (ESMFold, OpenFold); Boltz-1 broad across nearly the whole trunk; touch-mask window 25–47 | block index | same | p4, p18, p19 |
| Charge-direction ROC-AUC, ESMFold / OpenFold | ≈0.85–0.90 at block 0 → near 1.0 by blocks 5–10, held throughout | ROC-AUC | {K,R,H} vs {D,E} residue classes | p20–21 |
| Charge-direction ROC-AUC, Boltz-1 | ≈0.75 at earliest MSA block → ≈0.95 by Pairformer block 0 | ROC-AUC | same | p20–21 |
| Charge probes on `z` — rise window | blocks 0–15 (ESMFold, OpenFold); blocks 0–3 (Boltz-1); decline in blocks 35–47 in all three | block index; balanced accuracy | positive/negative charge class of residue *i* from `z_ij`, \|i−j\| ≥ 4 | p21–22 |
| Same-charge steering effect on cross-strand distance | ≈+10 Å (increase) in early blocks | Å | unsteered baseline | p6 |
| Charge steering dose–response threshold / saturation | onset ≈0.4; saturating above | std-DoM units | unsteered baseline | p22 |
| Charge steering effect-size ordering across models | OpenFold largest > ESMFold intermediate > Boltz-1 smallest | Å | unsteered baseline | p22 |
| Charge steering operating strength | α = 3σ, window size 15 | σ of the charge projection | — | p6 |
| Distance probe R², late blocks | ≈0.9 (all three models); low at block 0 | R² | true Cα–Cα distance, 200 held-out proteins | p7 |
| Distance steering target / strength / window | 5.5 Å; α = 20σ; window size 10 | Å; σ; blocks | textbook antiparallel β-sheet Cα spacing | p8 |
| `pair2seq` bias contact ROC-AUC, ESMFold | approaching 1.0 in late blocks | ROC-AUC | Cα < 8 Å contacts vs non-contacts | p7, p23 |
| `pair2seq` bias contact ROC-AUC, OpenFold / Boltz-1 | ≈0.9 over a similar block range | ROC-AUC | same | p23 |
| Structure-module `z`-scaling effect on mean pairwise Cα distance (scale 0→2) | ESMFold ≈15 Å swing; OpenFold ≈20 Å; Boltz-1 ≈13 Å (most of it below scale = 1) | Å | unscaled baseline, scale = 1.0 | p7, p23 |
| Structure-module `s`-scaling effect | "no detectable change" / "virtually no effect" | Å | same | p23, p24 |
| CKA, ESMFold vs OpenFold | > 0.8 through middle and late blocks | CKA | — | p8, p24 |
| CKA, ESMFold vs Boltz-1 | > 0.7 | CKA | — | p8 |
| CKA, pairings involving Boltz-1 (all pairs) | typically 0.5–0.8 | CKA | — | p24–25 |
| Whitened-Procrustes test R², ESMFold ↔ OpenFold | ≈0.9 (both directions) | R² | true residue-pair correspondences, held-out | p8, p25 |
| Whitened-Procrustes test R², OpenFold ↔ Boltz-1 | ≈0.8–0.9 | R² | same | p25 |
| Whitened-Procrustes test R², ESMFold ↔ Boltz-1 | ≈0.7–0.8 (≈0.75 quoted in §6) | R² | same | p8, p25 |
| Shuffled-correspondence R², whitened Procrustes | ≈ −1 (at the random-orthogonal floor) | R² | shuffled residue-pair correspondences | p26 |
| Shuffled-correspondence R², ridge and CCA | 0.1–0.25 | R² | same | p26 |
| Cross-model patching peak, ESMFold → ESMFold (within-model reference) | ≈22% | % | DSSP target-motif presence | p9 |
| Cross-model patching peak, OpenFold → ESMFold | ≈15% (§6, p9) / ≈17% (App M, p26) — **the paper gives two different numbers** | % | same | p9, p26 |
| Cross-model patching peak, Boltz-1 → ESMFold | ≈10% | % | same | p9 |
| Cross-model patching peak, ESMFold → OpenFold | ≈11% | % | same | p26 |
| Cross-model patching, pairings involving Boltz-1 | 5–12% | % | same | p26 |
| Cross-model patching effective block window | blocks 25–40 of the receiving model, all six directions | block index | same | p26 |
| Recycling convergence (ESMFold, App H) | short (<100 aa) proteins: sharp RMSD drop 0→1 recycle, small thereafter; medium/long continue to refine | Å Cα RMSD | highest-recycle prediction | p16, p17 |
| Compute | ~1,000–1,500 GPU-hours; 2–3 weeks wall-clock on 2× RTX A6000 (48 GB); <24 GB per GPU | GPU-hours | — | p14–15 (Table 1) |
| Statistical reporting | 95% CIs reported for Fig 5c (charge steering controls) and Fig 6c (scaling); other results are aggregate rates over hundreds of proteins with no stated interval | — | — | p31 |

## F. Figures

One row per panel group. **The paper assigns no panel letters to Figure 1; the `1A`/`1B` split below is
this note's labelling and is flagged in `panels`.** `reuse` for every row: the **paper's own license is
NOT REPORTED in the PDF** — it is an arXiv preprint (arXiv:2602.06020v3, p1) and arXiv licenses live on
the abstract page, not in the document, so an ND clause cannot be ruled out from the PDF alone; check
the arXiv abstract page before redrawing. **App F (p15) licenses only the assets the authors *used***,
not this paper: ESMFold/ESM MIT, OpenFold Apache 2.0, Boltz-1 MIT, PDB CC0 1.0, CATH and UniProt
CC BY 4.0, DSSP under its published usage terms. Rows below abbreviate this as `NOT REPORTED; p15`.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 1 | Cartoon strip: unstructured chain → hairpin → helix, above the result panels | schematic | `SCHEMATIC \| chain-to-motif cartoon strip introducing the hairpin/helix contrast \| no data` | 1 unlettered strip spanning the figure width | | NOT REPORTED; p15 |
| 1B | 1 | The headline result: sequence patches work early, pairwise patches work late, in all three models | line (filled area) | `PLOT \| facet: model (3: ESMFold, OpenFold, Boltz-1) \| vary: trunk block index, 0–47 (continuous) \| series: patch type (2: sequence patch/stage 1, pairwise patch/stage 2) \| measure: % of outputs with donor motif \| mark: line (filled) \| n: NOT REPORTED per point; ≈4,000 successful donor–target pairs per panel (p4)` | 3 unlettered panels varying by model; y-axis 0–40+% | n per block never shown; no error band on any curve despite these being proportions over a few thousand cases; y-axis top is clipped just above the peak so the ESMFold sequence peak is at the frame edge | NOT REPORTED; p15 |
| 2 | 2 | ESMFold's three modules and the internals of one folding block | schematic | `SCHEMATIC \| (a) ESM-2 encoder → 48-block folding trunk → IPA structure module; (b) sequence update (Pair2Seq + transformer) then pairwise update (Seq2Pair + triangular updates + MLP) \| no data` | 2 (a, b) | | NOT REPORTED; p15 |
| 3 | 3 | Donor/target activation patching protocol, sequence and pairwise routes | schematic | `SCHEMATIC \| donor hairpin protein's s and z extracted at block k and written into a helix-turn-helix target's motif region \| no data` | 1 composite | | NOT REPORTED; p15 |
| 4A | 4 | Sequence patching drags `z` donor-ward early; freezing seq2pair stops it; a block-0 `z` patch decays | line | `PLOT \| facet: none (1) \| vary: trunk block index, 0–47 (continuous) \| series: intervention (3: seq patch @ block 0, seq patch + seq2pair frozen 0–10, pairwise patch @ block 0) \| measure: interpolation coefficient α of z toward donor (Eq. 3) \| mark: line \| n: NOT REPORTED per point; 400 successful block-0 sequence-patch cases per panel (p4)` | 1 (a) | n per curve not annotated on the figure | NOT REPORTED; p15 |
| 4B | 4 | seq2pair dominates early, pair2seq late, without any intervention | line | `PLOT \| facet: none (1) \| vary: trunk block index, 0–47 (continuous) \| series: pathway (2: seq2pair, pair2seq) \| measure: normalized update contribution magnitude \| mark: line \| n: NOT REPORTED` | 1 (b) | Each pathway is normalized *within itself* across the trunk (p5), so the two curves are not on a comparable scale and their crossing point carries no meaning — the normalization is stated in the text but not on the axis | NOT REPORTED; p15 |
| 4C | 4 | Ablating seq2pair in an early window destroys motif formation; recovery past block 12 | line | `PLOT \| facet: none (1) \| vary: ablation window start block, 0–47 (continuous, window size 15) \| series: ablated pathway (2: seq2pair, pair2seq) \| measure: % of outputs with donor motif \| mark: line \| n: NOT REPORTED` | 1 (c) | | NOT REPORTED; p15 |
| 5A | 5 | Charge-steering construction: opposite charges on the two helical flanks | schematic | `SCHEMATIC \| target helix-turn-helix, +charge on helix 1 and −charge on helix 2, producing an output hairpin \| no data` | 1 (a) | | NOT REPORTED; p15 |
| 5B | 5 | Charge steering induces hairpins, concentrated in early blocks, in all three models | line (filled area) | `PLOT \| facet: none (1) \| vary: steering window start block, 0–~33 (continuous, window size 15) \| series: model (3: ESMFold, OpenFold, Boltz) \| measure: % of outputs with hairpin \| mark: line (filled) \| n: ≈500 cases per model (p6); per-point n NOT REPORTED` | 1 (b), three models overlaid | No error band, despite p31 claiming 95% CIs for Fig 5c only; per-block n not shown | NOT REPORTED; p15 |
| 5C | 5 | The sign-controlled ESMFold control: same-charge repels strands, opposite-charge attracts | line | `PLOT \| facet: none (1) \| vary: steering window start block, 0–~33 (continuous) \| series: steering condition (4: Pos-Pos, Neg-Neg, Pos-Neg, Neg-Pos) \| measure: cross-strand Cα distance change Δ (Å) \| mark: line \| n: 500 sampled β-hairpins for the same-charge arm (p6); per-point n NOT REPORTED` | 1 (c) | | NOT REPORTED; p15 |
| 6A | 6 | pair2seq bias separates contacts from non-contacts in middle/late blocks (ESMFold) | line | `PLOT \| facet: none (1) \| vary: trunk block index, 0–47 (continuous) \| series: none (1: hairpin AUC) \| measure: contact-prediction ROC-AUC \| mark: line \| n: NOT REPORTED` | 1 (a) | y-axis starts at 0.4, not at the 0.5 chance line, so blocks performing at chance are not visually identifiable as such | NOT REPORTED; p15 |
| 6B | 6 | Head-averaged pair2seq bias at block 32, with 8 Å contact contours over it | heatmap | `MATRIX \| rows: residue index (~80) \| cols: residue index (~80) \| value: head-averaged pair2seq attention bias (signed, red positive / blue negative), with green 8 Å contact contours overlaid \| facet: none (1)` | 1 (b), one representative protein | Single hand-picked protein at a single hand-picked block; no quantification of how typical it is (6A carries that) | NOT REPORTED; p15 |
| 6C | 6 | Scaling `z` before the structure module scales output distances; scaling `s` does nothing | line | `PLOT \| facet: none (1) \| vary: scaling factor applied before the structure module, 0–2 (continuous) \| series: representation scaled (2: pairwise z, sequence s) \| measure: Δ mean pairwise Cα distance from the scale=1.0 baseline (Å) \| mark: line with shaded band \| n: 600 proteins (p7)` | 1 (c) | | NOT REPORTED; p15 |
| 6D | 6 | Predicted structures at three pairwise-scaling factors, with the gradient annotated | structure render | `RENDER \| facet: pairwise scaling factor (3) \| views: 1 \| overlay: NOT REPORTED predictions on 0 references \| axis: none` | 1 (d), 3 renders | Which protein is shown is not stated; no reference structure for comparison | NOT REPORTED; p15 |
| 7A | 7 | Linear distance probes on `z` reach R² ≈ 0.9 in late blocks in all three models | line (points+line) | `PLOT \| facet: none (1) \| vary: trunk block index, 0–47 (continuous) \| series: model (3) \| measure: test R² of a linear Cα-distance probe \| mark: point+line \| n: 200 evaluation proteins per point (p7)` | 1 (a), three models overlaid | | NOT REPORTED; p15 |
| 7B | 7 | Distance steering induces hairpins, peaking in middle-to-late blocks, in all three models | line (filled area) | `PLOT \| facet: none (1) \| vary: steering window start block, 0–~35 (continuous, window size 10) \| series: model (3) \| measure: % of outputs with hairpin (DSSP) \| mark: line (filled) \| n: NOT REPORTED` | 1 (b), three models overlaid | No n, no error band | NOT REPORTED; p15 |
| 7C | 7 | Distance-steering setup: baseline vs steered cross-strand distance matrix, and the resulting structures | schematic | `SCHEMATIC \| baseline and steered 5×5 cross-strand distance sub-matrices with the steering rule z'ij = zij − αw, beside cartoon input helix and output hairpin \| no data` | 1 (c) composite | The distance sub-matrices are illustrative, not measured data, but are drawn with a quantitative Å colourbar | NOT REPORTED; p15 |
| 8A | 8 | CKA between every block pair, ESMFold vs OpenFold and ESMFold vs Boltz-1 | heatmap | `MATRIX \| rows: ESMFold block (48) \| cols: other-model block (48) \| value: CKA \| facet: model pairing (2: vs OpenFold, vs Boltz-1)` | 1 (a), 2 heatmaps sharing a colourbar | | NOT REPORTED; p15 |
| 8B | 8 | Procrustes alignment R² per block, with shuffled baselines pinned near zero | line | `PLOT \| facet: none (1) \| vary: trunk block index, 0–47 (continuous) \| series: donor model × correspondence (4: OpenFold true, Boltz-1 true, OpenFold shuffled, Boltz-1 shuffled) \| measure: projection test R² \| mark: line (dotted for shuffled) \| n: NOT REPORTED` | 1 (b) | y-axis floored at 0 while the shuffled whitened-Procrustes R² is reported in App M.1 as ≈ −1 (p26) — the control curve is therefore clipped to the axis bottom and its true depth is invisible here | NOT REPORTED; p15 |
| 8C | 8 | Cross-model patching reproduces the late-block window, at reduced strength | line (filled area) | `PLOT \| facet: none (1) \| vary: trunk block index, 0–47 (continuous) \| series: donor model (3: ESMFold self, OpenFold, Boltz-1) \| measure: % of outputs with target motif \| mark: line (filled) \| n: NOT REPORTED` | 1 (c), three donors overlaid into ESMFold | No n or error band on rates that peak at only 10–22% | NOT REPORTED; p15 |
| 9 | 13 | A β-hairpin sequence with strand–loop–strand braces | schematic | `SCHEMATIC \| single-letter amino acid sequence annotated with strand 1 / loop / strand 2 braces \| no data` | 1 | | NOT REPORTED; p15 |
| 10 | 13 | 3D cartoon of a β-hairpin with two side chains labelled | structure render | `RENDER \| facet: none (1) \| views: 1 \| overlay: 0 predictions on 1 reference \| axis: none` | 1 | | NOT REPORTED; p15 |
| 11 | 17 | Recycling matters for long proteins, not short ones — the justification for disabling it | line | `PLOT \| facet: none (1) \| vary: number of recycles, 0–4 (continuous) \| series: protein length class (3: <100 aa, 100–300 aa, >300 aa) \| measure: mean Cα RMSD to the highest-recycle prediction (Å) \| mark: point+line \| n: NOT REPORTED (a "randomly sampled subset of UniProt protein sequences", p16)` | 1 | Subset size never stated; no error bars. The panel shows medium and long proteins still refining at 4 recycles, yet recycling is disabled for targets up to 400 residues | NOT REPORTED; p15 |
| 12 | 17 | Where in ESMFold patching works: trunk ≫ structure module ≈ input substitution ≈ encoder | bar | `PLOT \| facet: none (1) \| vary: intervention site (5: folding trunk touch mask, folding trunk standard intra mask, structure module, input intervention, ESM encoder) \| series: none (1) \| measure: % of outputs with hairpin \| mark: bar (horizontal; measure runs along the horizontal axis) \| n: NOT REPORTED per bar` | 1 | Bars over what are certainly heterogeneous per-case distributions, with no n, no CI, and no distribution shown — the single clearest example in this paper of a bar hiding a distribution | NOT REPORTED; p15 |
| 13 | 18 | Touch masking widens the pairwise window to blocks 25–47 | line (filled area) | `PLOT \| facet: none (1) \| vary: trunk block index, 0–47 (continuous) \| series: patch type (2: sequence patch, pairwise patch with touch mask) \| measure: % of outputs with hairpin \| mark: line (filled) \| n: NOT REPORTED` | 1 | No n or error band | NOT REPORTED; p15 |
| 14A | 19 | Single-block patching success by block, replicated in all three models | line (filled area) | `PLOT \| facet: model (3) \| vary: trunk block index (continuous; 0–47, Boltz-1 0–51) \| series: patch type (2: sequence, pairwise) \| measure: % of outputs with donor motif \| mark: line (filled) \| n: NOT REPORTED` | 3 (a, one per model) | | NOT REPORTED; p15 |
| 14B | 19 | The early write-in window, replicated: seq patch shifts `z`, freezing seq2pair blocks it | line | `PLOT \| facet: model (3) \| vary: trunk block index (continuous) \| series: intervention (3: seq patch @0, seq patch + seq2pair frozen, pairwise patch @0) \| measure: interpolation coefficient α of z toward donor \| mark: line, with the write-in window shaded yellow \| n: NOT REPORTED` | 3 (b) | | NOT REPORTED; p15 |
| 14C | 19 | Pathway contribution magnitudes, replicated; Boltz-1's seq2pair collapses to blocks 0–3 | line | `PLOT \| facet: model (3) \| vary: trunk block index (continuous) \| series: pathway (2: seq2pair, pair2seq) \| measure: normalized update contribution magnitude \| mark: line \| n: NOT REPORTED` | 3 (c) | Same within-pathway normalization issue as 4B | NOT REPORTED; p15 |
| 14D | 19 | Sliding-window ablation, replicated; pair2seq ablation is inert everywhere | line | `PLOT \| facet: model (3) \| vary: ablation window start block (continuous, window size 15) \| series: ablated pathway (2: seq2pair, pair2seq) \| measure: % of outputs with donor motif \| mark: line \| n: NOT REPORTED` | 3 (d) | | NOT REPORTED; p15 |
| 15 | 21 | Charge is linearly separable along the DoM direction throughout every trunk | line | `PLOT \| facet: model (3) \| vary: trunk block index (continuous) \| series: none (1) \| measure: ROC-AUC separating {K,R,H} from {D,E} \| mark: line \| n: NOT REPORTED` | 3, one per model | AUC near 1.0 for most of every trunk — the curve is at ceiling and carries no block-resolved information after block ~10 | NOT REPORTED; p15 |
| 16A-B | 21 | Charge enters `z` during the early window, tracking each model's seq2pair locus | line | `PLOT \| facet: probe source (2: seq2pair output, pairwise representation z) × model (3) \| vary: trunk block index (continuous) \| series: charge class probed (2: positive K/R/H, negative D/E) \| measure: balanced accuracy \| mark: line \| n: NOT REPORTED` | 6 (2 rows a–b × 3 models); a and b share mark and measure, so one row per the v3 split rule | Chance level for a balanced-accuracy probe is 0.5 but no chance line is drawn | NOT REPORTED; p15 |
| 17 | 22 | Charge steering dose–response: threshold ≈0.4 std-DoM, then saturation, all three models | line | `PLOT \| facet: model (3) \| vary: steering magnitude, 0–~1 std-DoM (continuous) \| series: steering condition (4: Both+, Both−, +/−, −/+) \| measure: mean cross-strand Cα distance change (Å) \| mark: line \| n: NOT REPORTED (≤40-residue single-motif proteins, p22)` | 3, one per model | n per condition never given; the saturating plateau means the reported α = 3σ operating point is off the right-hand end of this axis and cannot be located on it | NOT REPORTED; p15 |
| 18 | 23 | Strands progressively separate as same-charge steering increases | structure render | `RENDER \| facet: steering magnitude (4: 0.2, 0.4, 0.6, 0.8 std-DoM) \| views: 1 \| overlay: 0 predictions on 0 references \| axis: none` | 4 (a–d) | One hand-picked protein; no reference or unsteered overlay, so the reader cannot judge how much of the change is the intervention | NOT REPORTED; p15 |
| 19A | 24 | Contact-separating pair2seq bias in middle/late blocks, all three models | line | `PLOT \| facet: model (3) \| vary: trunk block index (continuous) \| series: none (1: hairpin AUC) \| measure: contact-prediction ROC-AUC \| mark: line \| n: NOT REPORTED` | 3 (a) | y-axes start at 0.4/0.5 and differ between panels; the 0.5 chance line is not marked | NOT REPORTED; p15 |
| 19B | 24 | Head-averaged pair2seq bias maps with contact contours, one representative protein per model | heatmap | `MATRIX \| rows: residue index (~80–110) \| cols: residue index (~80–110) \| value: head-averaged pair2seq attention bias (signed), with green 8 Å contact contours and the hairpin region marked \| facet: model (3)` | 3 (b) | One hand-picked protein and block per model; colourbar ranges differ across panels, so the three maps are not directly comparable | NOT REPORTED; p15 |
| 19C | 24 | Scaling `z` moves output distances in all three models; scaling `s` never does | line | `PLOT \| facet: model (3) \| vary: scaling factor before the structure module, 0–2 (continuous) \| series: representation scaled (2: pairwise, sequence) \| measure: Δ mean pairwise Cα distance from the scale=1.0 baseline (Å) \| mark: line with ±1 SD band \| n: 600 proteins (p7)` | 3 (c) | y-axis ranges differ per panel (ESMFold ~−15→+5, OpenFold ~−15→+5, Boltz-1 ~−15→+2.5), so the "OpenFold largest, Boltz-1 smallest" claim cannot be read off the panels without checking axes | NOT REPORTED; p15 |
| 21 | 25 | Per-head pair2seq bias at block 32 for β-sheet protein 6rwc | heatmap | `MATRIX \| rows: residue index (~85) \| cols: residue index (~85) \| value: per-head pair2seq attention bias (signed), green 8 Å contact contours \| facet: attention head (8)` | 8 (heads 0–7) | Purely qualitative; head specialisation is asserted from these maps with no quantitative summary | NOT REPORTED; p15 |
| 22 | 25 | Per-head pair2seq bias at block 32 for β-helix protein 1l0s | heatmap | `MATRIX \| rows: residue index (~85) \| cols: residue index (~85) \| value: per-head pair2seq attention bias (signed), green 8 Å contact contours \| facet: attention head (8)` | 8 (heads 0–7) | as above | NOT REPORTED; p15 |
| 23 | 26 | PyMOL views of the two example proteins used for the bias maps | structure render | `RENDER \| facet: protein (2: 6rwc, 1l0s) \| views: 1 \| overlay: 0 predictions on 1 reference each \| axis: none` | 2 | | NOT REPORTED; p15 |
| 24A | 27 | CKA across all three model pairings | heatmap | `MATRIX \| rows: model A block (48) \| cols: model B block (48) \| value: CKA \| facet: model pairing (3: ESM↔OF, ESM↔Boltz, OF↔Boltz)` | 3 (top row) | | NOT REPORTED; p15 |
| 24B | 27 | Procrustes R² in both directions of each pairing, with shuffled baselines | line | `PLOT \| facet: model pairing (3) \| vary: trunk block index (continuous) \| series: direction × correspondence (4: A→B true, B→A true, A→B shuffled, B→A shuffled) \| measure: projection test R² \| mark: line (solid/dashed true, dotted shuffled) \| n: NOT REPORTED` | 3 (middle row) | Same clipped-floor problem as 8B: shuffled whitened-Procrustes R² is ≈ −1 (p26) but the panels bottom out near 0 | NOT REPORTED; p15 |
| 24C | 27 | Cross-model patching in all six donor→receiver directions | line (filled area) | `PLOT \| facet: model pairing (3) \| vary: trunk block index (continuous) \| series: donor→receiver direction (2 per pairing) \| measure: % of outputs with target motif \| mark: line (filled) \| n: NOT REPORTED` | 3 (bottom row), 6 curves total | No n, no CI, on rates of 5–17%; the direction asymmetry the text flags as unexplained (p26) is presented without any uncertainty estimate that would say whether it is real | NOT REPORTED; p15 |
| 25 | 28 | Under shuffling, ridge and CCA still score; whitened Procrustes sits at the floor | line | `PLOT \| facet: none (1) \| vary: trunk block index (continuous) \| series: alignment method (5: ridge, CCA, unwhitened Procrustes, whitened Procrustes, random orthogonal) \| measure: test R² under shuffled correspondences \| mark: line \| n: NOT REPORTED` | 1 | | NOT REPORTED; p15 |

**Figure 20 does not exist in this PDF.** Numbering runs 19 (p24) → 21 (p25) with no Figure 20 caption,
image, or in-text reference anywhere. App L.1 "Bias Maps" (p24) describes a per-block bias-map
visualisation and cites no figure number, so Figure 20 was most likely dropped in this version without
renumbering. Recorded under `unresolved`.

**Panel-group rows: 43.**

## G. Provenance

| field | value |
|---|---|
| `extracted_on` | 2026-09-07 |
| `extractor` | claude subagent (Opus 5) |
| `schema_version` | v3 |
| `confidence` | **high** on identity, scope, the model list and their architectural relationships, the intervention inventory, oracle routes, controls, and the claim quotes — the paper is unusually explicit and its appendices are all in the PDF. **medium** on `metrics_reported`: the paper contains no numeric results table, so most values are the authors' own approximations in prose ("≈40%", "near 22%", "R² ≈ 0.9") or read off figure axes, and per-block/per-model values cannot be recovered exactly. **medium** on figure `n` fields: almost every panel omits n, and I have marked NOT REPORTED rather than back-inferring from the dataset sizes. Six pages (1, 5, 6, 7, 8, 17, 18, 24, 25) were rendered to read panel structure the captions did not carry; all renders deleted after reading. |
| `unresolved` | 1. **Figure 20 is missing** — numbering jumps 19 → 21, with no caption or cross-reference (p24–25). 2. **The OpenFold → ESMFold cross-model patching peak is given twice with different values: "near 15%" (p9, §6) and "peaking near 17%" (p26, App M).** Neither is flagged as a correction. 3. **How the steering strengths α = 3σ (charge) and α = 20σ (distance) and the window sizes 15/15/10 were selected is never stated.** 4. **MSA construction for OpenFold and Boltz-1 is never described** — no tool, database, depth, or date. 5. **Template usage for OpenFold and Boltz-1 is never stated.** 6. Model **training cutoffs** are never stated, so the memorization exposure of a 2025-culled PISCES set cannot be assessed. 7. The Boltz-1 block indexing is inconsistent between "48-block Pairformer" (p3) and "blocks 4–51" (p20); the MSA module is "treated as blocks 0–3" (p3), so Boltz-1's trunk has 52 indices while the other two have 48 — figures with a shared block axis are therefore not strictly commensurable across models, and this is never addressed. 8. Only **ESMFold code** is released; the OpenFold and Boltz-1 pipelines are promised "upon publication" (p31). 9. **Tags I needed but the v3 vocabulary does not have**, all declined rather than invented: (a) a method tag for **activation patching / causal mediation** — `latent-steering` is the closest legal tag and I used it, but it is defined as an inference-time intervention on an internal tensor and does cover patching by that definition, while the paper's *probing* and *CKA/Procrustes alignment* work has no tag at all; (b) a tag for **cross-model representational alignment / convergence**, which is this paper's headline claim and is unfindable by any existing tag; (c) a tag distinguishing **causal/interventional** from **observational** interpretability work, which is the single most useful axis for querying this part of the corpus; (d) a tag for **mechanistic-interpretability** as a `method_class` (I wrote `other`); (e) a tag for a **single-sequence / PLM-front-end** model regime — `no-template-no-msa` fits ESMFold exactly but would be false for OpenFold and Boltz-1, so I omitted it and flag the judgement call here. 10. **v3 ambiguity worth fixing**: the panel-split rule ("split when `mark` or `measure` differs; do not split when only `facet` differs") is silent about `vary` and `series`. Fig 14a and 14d share mark (line) and measure (% motif formation) but differ in `vary` (patch block vs ablation window start) and in what the series means; a literal reading forces them into one row with a compound `vary`, which is exactly the unjoinable-compound-string defect the rule exists to prevent. I split them and am flagging it. The same issue arises for Figs 5b/5c and 8b/8c. Recommend the rule become "split when `mark`, `measure`, or `vary` differs." 11. **Second v3 ambiguity**: `hides` is specified for figures that obscure their own result, but three of this paper's normalization choices (within-pathway normalization in 4B/14C, per-panel colourbar ranges in 19B, per-panel y-ranges in 19C) obscure *cross-panel comparison* rather than the panel's own result. I recorded them in `hides` as the nearest fit; the schema could say explicitly whether cross-panel incomparability belongs there. 12. `states_generated`, `prospective` and `directional_control` all assume a conformational generator; I filled them with NOT APPLICABLE-plus-reason or an adapted reading, but a mechanistic-interpretability paper is a recurring shape in this corpus now (`feldman2026alphainterp`, `migliorini2026pairsae`, this one) and section C could use a stated convention for it. |
| `why_it_matters` | *(left empty by extractor)* |

## Tags

`general-protein` `latent-steering` `single-state` `binary-predicate` `continuous-metric`
`saturating-metric` `design-level-oracle` `no-anti-memorization` `multi-backbone` `directed-state`
`preprint` `precedent` `contrast` `comparator-numbers`

Deliberately **not** tagged, with reasons: `oracle-leak` (pipeline routes 1–6 come out NONE FOUND; only
design-level use is present); `prospective` (retrospective throughout); `anti-memorization` (no such
design exists); `unpowered` (n is large — ~10,000 patching experiments, ~500 steering cases per model);
`confidence-as-discriminator` (pLDDT is never used to judge correctness); `experimental-validation`
(no wet-lab work); `cofolding` / `msa-subsample` / `msa-state-filter` / `template-state-bias` /
`af-cluster` / `md` / `md-emulator` / `enhanced-sampling` / `benchmark-only` / `experimental` (none
describe this work); `no-template-no-msa` (true for ESMFold, false for OpenFold and Boltz-1 — see
`unresolved` item 9e); `templates-on` / `state-annotated-input` (never stated / never used); `ensemble`
/ `continuum` (nothing is sampled); `rmsd-only` / `visual-metric` (success is an explicit DSSP
predicate, and every render is backed by a quantitative panel); all `Site` tags (no binding site is
studied); `figure-exemplar` (the paper is kept for its findings, not its figures).
