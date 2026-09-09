# tran2026nanogs

> **Reader's warning.** This is a wet-lab synthetic-chemistry / molecular-pharmacology
> paper with an accompanying MD component. It contains **no structure prediction**.
> Several schema fields written for co-folding papers (`backbones`, `templates`,
> `msa_handling`, `oracle_leakage`, `anti_memorization_*`, `confidence_as_discriminator`)
> are `NOT APPLICABLE` here; each carries one line of why. The wet-lab analogue of the
> anti-memorization control (unstapled, staple-shifted and no-peptide arms) is recorded
> under `stated_limits` and `unresolved`.

## A. Identity

- **citekey**: `tran2026nanogs`
- **doi**: 10.1002/anie.202523510 (p.1)
- **year**: 2026. Received 26 October 2025; Revised 16 March 2026; Accepted 17 March 2026 (p.1).
- **venue**: *Angewandte Chemie International Edition* 2026, 65, e23510. **Peer-reviewed research article, not a preprint** (p.1).
- **title**: Nano-Gs Protein Peptidomimetics: Rational Design of Gα C-Terminus-Derived Peptides Mimicking Key Components of Gs-β2AR Interactions
- **authors**: Phuong Thu Tran, Mia Danielsen, Johanna K. S. Tiemann, Passainte Ibrahim (four co-first authors, p.1) et al.; corresponding: Peter W. Hildebrand (Leipzig), Daniel Sejer Pedersen (Copenhagen / Novo Nordisk), Jesper Mosolff Mathiesen (Copenhagen). Groups at U. Copenhagen, U. Leipzig, Vrije Universiteit Brussel, Vietnam National University HCMC (p.1).

## B. Scope

- **system**: **GPCR** (class A). Primary target: β2 adrenergic receptor (β2AR). Secondary counter-screens: β1AR and dopamine D1 receptor (D1R) in membrane cAMP assays (p.8, Figure S4/Table S10).
- **n_targets**: **1 primary + 2 secondary = 3 receptors.** All β2AR biophysics (bimane) is on one receptor; β1AR and D1R appear only in the cAMP selectivity panel (p.8). The paper carries a generality claim on a single deeply-characterised system: *"We envision that this generalizable approach will be enable further structural and functional exploration of other GPCRs"* (p.11) — flag this as a one-system paper claiming generality.
- **method_class**: **other — experimental peptidomimetic design + MD.** Concretely three strands: (i) structure-guided rational design of stapled peptides using two deposited β2AR structures; (ii) solid-phase peptide synthesis with CuAAC (i, i+7) stapling and non-canonical amino acids (Scheme 1, p.4; Table 1, p.5); (iii) all-atom **MD** and **metadynamics enhanced sampling** to assess the binding mode of the best peptide (p.8, p.9). No co-folding, no MSA method, no benchmark.
- **backbones**: **NOT APPLICABLE.** No structure-prediction backbone (AF2/AF3/Boltz/Chai/Protenix) is used anywhere in the paper. Structural input is deposited crystallography (PDB 3SN6, 6E67, 3P0G, 2RH1) and MD trajectories from prior work (pp.2–3, p.10).
- **templates**: **NOT APPLICABLE** in the prediction sense. The design-time structural inputs are named explicitly: *"we reviewed the available high-resolution structural information of G protein and receptor complexes with respect to the C-terminal part of α5 (PDB ID: 3SN6)"* (p.2) and *"a structure capturing the β2AR in a complex with the carboxyl terminal 14 amino acids from Gαs (β2AR-T4L-GsCT-CC, PBD ID: 6E67)"* (p.2). MD was started from *"The x-ray structure of the β2AR [PDB ID 3SN6] … bound to the high affinity agonist BI-167107"* (p.8).
- **msa_handling**: **NOT APPLICABLE.** No sequence alignment is built or used; there is no MSA anywhere in the pipeline.

## C. Conformational core

- **states_generated**: **Two, by different routes, and neither is a "generated" prediction.**
  - *Experimentally*: a population shift of β2AR along the inactive ↔ active-like axis, read out as a continuous spectral change (bimane). No discrete states are produced; a conformational **equilibrium** is displaced (p.5: *"Shifting the equilibrium toward the active state by addition of increasing isoproterenol (ISO) agonist concentrations causes TM6 to rotate and move outward"*).
  - *Computationally*: an **ensemble** from 20 × 2 μs unbiased replicates plus multiple-walker metadynamics, from which **one** dominant bound pose is reported — the *"β2AR-peptide 4 complex"* (p.9). The authors place this pose as a **third, intermediate** state, distinct from both crystal binding modes: *"we speculate that the peptidomimetics capable of stabilizing an active-like β2AR conformation in vitro, stabilize an otherwise transient, intermediate, active-like conformational state preceding that of the β2AR-Gs(empty)"* (p.10).

- **structural_priors_used**: **New in v3. Extensive, disclosed, and committing no methodological sin — this field exists precisely for a case like this one.** The peptide was designed from deposited structures of the answer, which for a wet-lab design paper is a legitimate starting point rather than leakage. Four distinct priors:
  1. **Two deposited β2AR–GαsCT complexes, used to pick the staple position.** Verbatim, p.1: *"By rational design, integrating the information of two crystal structures showing different binding modes of Gαs CT with β2 AR, an appropriate staple position was identified."* Named on p.3 (Fig 1 caption): **PDB 3SN6** (β2AR–Gs empty) and **PDB 6E67** (β2AR-T4L-GsCT-CC). The two structures disagree about which residue contacts R131^3.50 — Y391 in 3SN6, E392 in 6E67 — and the design exploits that disagreement rather than resolving it (p.5: *"In the two crystal structures, it is evident that either Y391 or E392 can interact with R131"*).
  2. **Helical geometry of GαsCT15 taken from those same complexes**, to set staple positions computationally (p.3: *"To mimic the helical conformation of Gαs CT15 in the crystal structures ... we sought to identify the optimal positions for stapling by computational methods."*).
  3. **Prior MD of the solved complexes**, used to rank α5 C-terminal interactions by stability (p.3), and prior published MD showing Gs(GDP) binding an extended interface of the activated receptor (p.2).
  4. **Prior GαCT peptide literature as the design precedent** (p.2): *"Proteinogenic peptides derived from the α5 C-terminus of G proteins (GαCT) were initially reported by Hamm and coworkers as GPCR modulators binding to the intracellular receptor crevice to stabilize an active-like receptor conformation and prevent G protein coupling"*, and more recent (i, i+4)-stapled peptides from Ballet and coworkers active at β2AR and D1R (p.2).

  **Why this matters to us.** Our own co-input is the same 21-residue region these authors staple, and the structural basis they draw on is the same pair of complexes. Anything we say about the α5 C-terminus as a handle inherits the **6E67 register ambiguity** recorded above: the two deposited structures place different peptide residues against R131^3.50. That is a real caveat on any claim that a particular α5 contact is *the* one that matters.

- **oracle_leakage**: **NOT APPLICABLE as a rigour defect** — there is no prediction whose success could be scored against a withheld structure, and no learned model whose training set could contain the answer. **But the design is openly and deliberately built on deposited structures of the target's active state**, and for corpus purposes that route should be visible, so it is enumerated here as *design-time structural knowledge*, not as leakage:
  1. Both binding modes used to choose the staple position come from solved β2AR–GαsCT complexes (p.2): *"By rational design, integrating the information of two crystal structures showing different binding modes of GαsCT with β2AR, an appropriate staple position was identified"* (Abstract, p.1).
  2. Staple ranking used MD trajectories of those same solved complexes (p.3): *"we ranked the interactions of the α5 C-terminus according to their stability in context of the receptor, obtained from previously performed MD simulations of these structures [33]"*.
  3. The MD that validates the binding mode starts from the agonist-bound active receptor with the ionic lock deliberately preserved (p.8): *"we started our simulations with the D1303.49–R1313.50 ionic interaction preserved in the receptor, to facilitate intracellular binding of peptide 4."* This is a hand-set starting condition chosen to make the desired event happen; it is disclosed.
  4. Conclusion states the dependency outright (p.11): *"we applied a computational design strategy based on pre-existing x-ray crystallographic data."*
  - Crucially, the **experimental** readouts (bimane, cAMP) are independent of all of the above: the peptides are new molecules, tested in an assay whose answer was not known in advance. The design used prior structures; the result was not scored against them.

- **prospective**: **yes, on the pharmacology; retrospective on the structural rationale.** Ten stapled peptides plus linear counterparts and native GαsCT15 were synthesised and *then* tested; the assay outcome is a genuine forward test (peptides 5, 6, 7 and 8 failed — a prospective design campaign with real negatives, pp.7–8). The MD is retrospective consistency-checking: it was run *after* peptide 4 was identified as the best (p.8: *"Having identified peptide 4 as a potent Gαs protein mimetic … we simulated spontaneous binding"*).

- **state_metric**: **continuous coordinate, no threshold, no fitted structural coordinate.** Two independent readouts:
  1. **Bimane fluorescence** at C265^6.27 in lower TM6: bathochromic shift of λmax plus decrease in fluorescence intensity (p.5, Figure 2B). Reports TM6 rotation/outward movement. **No numerical threshold for "active-like" is defined anywhere**; the main-text figures show normalised emission spectra and the reader judges by eye. Quantification is deferred to Table S9 (SI, not in the PDF).
  2. **cAMP accumulation** in β2AR membranes: ISO concentration-response curves, with Emax and EC50 as parameters (p.8, Figure 4G–I; Table S8 in SI).
  3. MD-side descriptors: Rg, RMSF, TM6 local tilt angle in degrees, residue-contact analysis (p.8, p.10).

- **metric_saturation**: **Yes, in three distinguishable ways.**
  1. **True assay saturation, stated**: *"In presence of agonist (10 μM ISO) both peptides 2 and 4 showed saturable responses when tested up to 50 μM"* (p.8).
  2. **A hard solubility ceiling that caps the dose range**: *"testing at peptide concentrations higher than 50 μM was not possible due to limited peptide solubility"* (Fig. 4 caption, p.9). The no-agonist arms (Fig. 4A–C) therefore cannot distinguish "no intrinsic activity" from "intrinsic activity below the solubility limit" — this is a ceiling that limits the negative result, not the positive one.
  3. **Normalisation ceilings**: all bimane spectra are normalised to a 1.0 peak (Figs 2C, 3, 4A–F) and cAMP is plotted as *"% of max ISO response"* with a 100% dotted reference line (Fig. 4G–I, p.9). Fluorescence intensity axes start at ~0.3–0.4 rather than 0, i.e. **the y-axes of every bimane panel are truncated at the bottom**, which visually magnifies the shift. No broken axes were seen.

- **directional_control**: **Yes — the method is instructed, not merely sampled, and there are two required handles acting together.**
  - **Handle 1: the peptide** (a stapled 15-mer GαsCT mimetic, added exogenously) — a G-protein-surrogate handle in the same class as a nanobody. Nb80 is used as the benchmark surrogate throughout (Fig. 2C, Fig. 4A/D/G).
  - **Handle 2: the orthosteric agonist** (isoproterenol, 10 μM) — required in every arm where conformational stabilisation was observed.
  - Direction is toward the **active-like** state only; nothing in the paper steers toward the inactive state.

- **anti_memorization_design**: **NOT APPLICABLE.** There is no trained model, no training cut-off, and nothing that could be memorised. No held-out set exists or could exist. (See `stated_limits` for the wet-lab control arms that play the analogous role.)

- **anti_memorization_control**: **NOT APPLICABLE**, same reason. The wet-lab analogue — negative-control peptides actually synthesised and run — **was** done and is recorded under `stated_limits`; note that a **scrambled-sequence peptide control was NOT run** (see `unresolved`).

- **controls_run**: **New in v3, and this is the most reusable content in the note.** The v2 pass had nowhere to put these and recorded them inside `stated_limits`, which is exactly the smuggling the v3 changelog was written to stop. Every arm below was actually run and analysed.

| control | what it rules out | page |
|---|---|---|
| **Linear (unstapled) GαsCT15, 20 μM + 10 μM ISO** | that the native α5 C-terminal sequence alone is sufficient. Verbatim p.5: *"Unlike the linear Gαs CT15 peptide, which at 20 μM did not potentiate the response of 10 μM ISO toward an active conformational state, the stapled peptide 1 potentiated the ISO response"*; restated p.6 | p.5, p.6 |
| **Unstapled linear counterpart of the best peptide (9)** | that the effect survives without the macrocycle in the optimised series. p.8: *"The potentiation was also lost in the unstapled linear counterpart to peptide 9"* | p.8, Figs S1 and 3 |
| **Peptide alone, no agonist** (peptides 2, 4 and Nb80) | **that a G-protein-mimetic peptide can stabilise the active state by itself.** p.8: *"In absence of agonist, both peptides 2 and 4, as well as Nb80 showed only minor responses in the bimane assay suggesting they were unable to stabilize an active receptor conformation alone"* | p.8, Fig 4A–C |
| **Nb80 as a positive-control surrogate** | that the assay cannot detect a genuine active-state stabiliser. p.6: Nb80 *"can potentiate a submaximal ISO response (10 μM), whereas it has minimal endogenous effect when tested alone at 1 μM"* | p.6 |
| **Staple position moved (I383-Q390 → I382-R389)** | that any staple anywhere works | p.4, p.7 |
| **Substitution variants that failed** (peptide 5, Y391dmPhe) | that every designed substitution helps | p.6, Fig S1 |
| **Off-target receptor counter-screens: β1AR and D1R** | that the peptides are indiscriminate across Gs-coupled receptors. p.8: *"While peptides 2 and 4 were also potent at the β1 AR they were less efficient for inhibition of D1 R-induced cAMP formation"* | p.8, Fig S4, Table S10 |
| **Whole-cell cAMP on cultured HEK293** | that the membrane-preparation result implies cell activity. p.8: peptides 2 and 4 *"did not show any effect on ISO-induced cAMP formation on cultured HEK293 cells expressing the β2 AR ... indicating that the peptides do not readily cross the cell membrane"* | p.8, Fig S3 |
| **ABSENT — scrambled-sequence peptide** | sequence identity versus mere occupancy of the crevice. Every negative control is *structural* (unstapled, staple moved, substitution removed); none scrambles the sequence while preserving length and charge | — |
| **ABSENT — Gi- and Gq-coupled receptor selectivity**, and the authors say so | coupling-class selectivity. p.8: *"Although of high importance to inform on selectivity of the peptides toward Gs -coupled receptors over Gi - and Gq -coupled receptors, it was not possible to develop membrane-based assays for Gi - and Gq -coupled receptors."* | p.8 |

  **The absent scrambled control is the one that matters to us.** Our own decoy and sequence-shuffled arms are exactly the control this paper could not run, which makes the two designs complementary rather than redundant, and is worth stating in the Discussion.

- **confidence_as_discriminator**: **NOT APPLICABLE.** No pLDDT/pTM/ipTM or any model-confidence score exists in this work. The nearest analogue is the metadynamics free-energy surface used to argue the reported pose is a low-energy state (p.9: *"To confirm this binding pose of peptide 4 as its lowest energy binding mode, we used metadynamics enhanced sampling"*), and it is used for pose ranking, not for a correctness claim; it is not externally validated against any reference.

## D. Claims

- **central_conclusion**: A 15-mer peptide of the Gαs α5 C-terminus, **conformationally locked into an α-helix by an (i, i+7) staple at one specific position (I382–R389) and improved at two contact residues (Y391Nal, E392hGlu)**, is sufficient to stabilise β2AR in an active-like conformation (TM6 outward, measured by bimane) and to block ISO-induced cAMP formation — with efficacy comparable to or exceeding the nanobody surrogate Nb80. **The isolated peptide does this only in the presence of an orthosteric agonist**: alone, at every concentration testable, it produced no conformational stabilisation. MD places the peptide-bound receptor in an intermediate active-like state distinct from both the β2AR-Gs(empty) and β2AR-T4L-GsCT-CC binding modes.

- **necessity_claims** (verbatim, with page):

  1. **The unstapled peptide does nothing — helicity is required.** (p.5)
     > "Unlike the linear GαsCT15 peptide, which at 20 μM did not potentiate the response of 10 μM ISO toward an active conformational state, the stapled peptide 1 potentiated the ISO response and had no effect when tested in the absence of ISO (Figure 2C). These data indicated that stapling of the GαsCT15 peptide in an extended helical conformation is indeed beneficial for stabilization of an active-like conformation in presence of an orthosteric agonist."

  2. **Staple AND side-chain modification both required.** (p.6)
     > "Importantly, the linear counterpart of peptide 2 lost its effect entirely indicating that both stapling and introduction of Nal are critical for the stabilization of an active conformation (Figure 3)."

  3. **Figure 3 caption, same point plus staple-position necessity.** (p.7)
     > "Stapling was required for activity as the linear precursor of peptide 2 was not able to potentiate the ISO response. The staple position was also essential as moving the staple position from I383-Q390 to I382-R389 resulted in an inactive peptide (peptide 8)."
     *(Note: the caption states the staple move in the opposite direction to the body text and Table 1 — see `unresolved`.)*

  4. **Summary necessity statement for the whole design.** (p.8)
     > "Taken together, these data indicate that the combination of stapling of GαsCT15 to conserve the α-helical conformation at a specific position and strengthening of key interactions are required to efficiently stabilize an active-like conformation of β2AR."

  5. **THE KEY ONE for our purposes — the peptide alone is NOT sufficient; agonist is required.** (p.8)
     > "In absence of agonist, both peptides 2 and 4, as well as Nb80 showed only minor responses in the bimane assay suggesting they were unable to stabilize an active receptor conformation alone (Figure 4A–C)."

  6. **Same claim in the Figure 4 caption, with the ceiling that qualifies it.** (p.9)
     > "In absence of ISO, Nb80 had marginal effects (A), whereas peptides 2 (B) and 4 (C) were unable to stabilize an active receptor conformation at the concentrations tested (testing at peptide concentrations higher than 50 μM was not possible due to limited peptide solubility)."

  7. **Staple position and length essential; stapling alone insufficient.** (p.11)
     > "We found that the positioning and length of the staple was essential to achieve favorable interactions with the β2AR. However, stapling alone only resulted in a small active conformation-stabilizing effect."

  8. **Conformational premise of the whole design: the α5 C-terminus must be helical to be recognised.** (p.2)
     > "This suggests that the Gs α5 C-terminus can be recognized by and bind to the receptor in an α-helical and not the unfolded conformation."

  9. **The isolated native peptide, as a free entity, is disordered** (their own prior finding, restated here as the premise). (p.2)
     > "In addition, secondary structure analysis using CD spectrometry shows that a GαsCT15 peptide, as a separate entity, adopts a disordered conformation corresponding to that of a random coil [28]."

  10. **Impossibility statement — assay coverage.** (p.8)
      > "Although of high importance to inform on selectivity of the peptides toward Gs-coupled receptors over Gi- and Gq-coupled receptors, it was not possible to develop membrane-based assays for Gi- and Gq-coupled receptors."

  11. **Impossibility statement — their own prior attempts failed.** (p.2)
      > "However, only weak effects of the peptides for inhibiting agonist-induced cAMP signaling were observed and no signs of active-like conformation-state stabilization by the peptides were identified using these two approaches."

- **novelty_claims** (verbatim, with page):

  1. (Abstract, p.1)
     > "Here we develop highly active Gαs CT-derived peptidomimetics that stabilize the β2 adrenergic receptor (β2AR) in an active-like conformation when the helical conformation of GαsCT is preserved by a covalent tether ("staple")."

  2. (Abstract, p.1)
     > "Optimization resulted in the identification of a potent peptidomimetic capable of stabilizing an active-like receptor conformation, whilst blocking receptor-mediated cAMP formation. Molecular dynamics simulations indicated a peptidomimetic binding mode that may represent another intermediate state preceding that of β2AR-Gs (empty)."

  3. (p.2 — the methodological novelty, an (i, i+7) staple spanning two helical turns rather than the usual (i, i+4))
     > "Here, we explore stapling over two helical turns using a (i, i+7)-staple as a strategy to reduce the entropic cost during peptide-receptor complex formation, using methodology previously developed by us [29]."

  4. **Explicit differentiation from the closest prior art (Ballet and coworkers, ref [23]).** (p.8)
     > "However, unlike in the present study, neither incorporation of Nal at position 391 nor hGlu at position E392 improved the ability to stabilize the active conformation of β2AR [23]."

  5. **"First indication" claim.** (p.7)
     > "The lack of effect by these substitutions provided the first indication that the peptides bind in a manner different from the pose in the β2AR-Gs (empty) structure."

  6. (Conclusion, p.11)
     > "Herein, we demonstrate that short 15-mer peptidomimetics of the C-terminal α5 helix of the Gα subunit in the Gs protein can be designed to effectively stabilize an active receptor conformation and block intracellular signaling of the β2AR receptor."

  7. (Conclusion, p.11 — novel structural feature)
     > "MD simulations of peptide 4 with the β2AR suggest a binding mode closer to the intermediate conformation seen in the β2AR-T4L-GsCT-CC complex with E392hGlu interacting with R1313.50, while including components from the β2AR-Gs(empty) complex and novel features such as a TM6 kink, the latter also captured in the receptor bimane conformational change assay."

  8. (Conclusion, p.11 — generality)
     > "In conclusion, we have shown that a computationally driven peptide design approach based on structural information could identify a potent nano Gs protein mimic that blocks the receptor from interacting with intracellular binding partners while stabilizing an active-like conformation. … We envision that this generalizable approach will be enable further structural and functional exploration of other GPCRs and possibly opens gateways toward novel therapeutics."

- **stated_limits** (authors' own, plus the wet-lab control arms that are the analogue of an anti-memorization control):

  *Author-stated limits:*
  - No intrinsic activity without agonist at any testable concentration (p.8, p.9 — quotes 5 and 6 above).
  - Concentration range capped by solubility at 50 μM (p.9).
  - **Not cell-permeable**: *"Of note peptides 2 and 4 did not show any effect on ISO-induced cAMP formation on cultured HEK293 cells expressing the β2AR (Figure S3), indicating that the peptides do not readily cross the cell membrane and would likely require modification to enable membrane permeation, for example, with cell-penetrating motifs such as Pep-1, TAT or polyarginines"* (p.8).
  - **Selectivity untested against Gi/Gq receptors** because the assay could not be built (p.8, quote 10).
  - **Selectivity result unexplained**: *"Further studies are needed to explore the structural basis for these observations but highlights the potential for development of receptor selective peptidomimetics"* (p.8).
  - MD binding mode presented as speculation, hedged: *"we speculate that…"* (p.10); *"We further hypothesize that the additional bulkiness of Y391Nal aids to stabilize an active-like β2AR conformation with TM6 pushed outward"* (p.11).
  - ICL3 was not modelled: 25 residues of ICL3 are missing and their effect is argued only sterically (p.9).
  - MD used a hand-preserved D130^3.49–R131^3.50 ionic interaction to encourage binding (p.8).
  - Chemistry was not optimised: *"CuAAC stapling was performed according to the published procedure [29] and was not optimized"* (Scheme 1 caption, p.4).

  *Experimental control arms actually run and analysed — the wet-lab analogue of an anti-memorization control:*
  | Control arm | Where | Result |
  |---|---|---|
  | Buffer only | Figs 2C, 3, 4 (p.6, p.7, p.9) | baseline trace in every bimane panel |
  | Agonist only (10 μM ISO) | Figs 2C, 3, 4 | reference partial response |
  | **Peptide only, no agonist** (20 μM in Fig 3; full CRC to 50 μM in Fig 4A–C) | p.7, p.9 | **no effect** — this is the central negative |
  | **Native, unstapled GαsCT15** | Fig 2C (p.6) | no effect at 20 μM with 10 μM ISO |
  | **Linear (unstapled) counterpart of peptide 2** | Fig 3 (p.7) | effect lost entirely |
  | **Linear counterpart of peptide 9** | p.8, Figs S1/3 | potentiation lost |
  | **Staple-position-shifted analogue (peptide 8)** | Fig 3 (p.7) | "completely lost potentiating effects" |
  | **Failed design analogues 5, 6, 7** (dmPhe; R380Y) | Fig S1, p.7 | no improvement — real prospective negatives |
  | **Positive-control surrogate Nb80** | Figs 2C, 4A/D/G | benchmark; peptide 4 exceeded it at saturation |
  | **Cell (intact HEK293) vs membrane** | Fig S3, p.8 | no effect in cells → permeability control |
  | **Off-target receptors β1AR, D1R** | Fig S4, p.8 | partial selectivity |
  | *Scrambled-sequence peptide* | — | **NOT RUN** (see `unresolved`) |

- **stance**: **`precedent` + `background`** (provisional — the user's call).
  - **precedent**, because it is a clean experimental demonstration that a *peptide handle alone* — no full G protein, no nanobody — can act as a directional conformational selector on a GPCR, with negative controls that establish which molecular features are load-bearing. That is the wet-lab counterpart of "partner-driven / peptide-driven directional control" and is directly citable as the physical basis for peptide-partner conditioning.
  - **background**, because there is no prediction, no model, no benchmark and no rigour axis to contrast against; it cannot be a `contrast` or `threat` for a structure-prediction argument. Its necessity claims (helix required; agonist required; peptide alone insufficient) are the useful load-bearing sentences.

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Y391→R131^3.50 min. distance, β2AR-Gs(empty), PDB 3SN6 | 4.0 | Å | cation–π judged formed | p.3 (Fig 1 caption) |
| E392→R131^3.50 min. distance, β2AR-Gs(empty) | 7.2 | Å | judged too distant | p.3 |
| E392–R131^3.50 salt-bridge distance, β2AR-T4L-GsCT-CC, PDB 6E67 | 2.2 | Å | judged formed | p.3 |
| Y391→R131^3.50 min. distance, β2AR-T4L-GsCT-CC | 11.4 | Å | judged too distant | p.3 |
| Peptide purity after RP-HPLC | > 95 | % | — | p.3 |
| Linear GαsCT15 test concentration (no effect) | 20 | μM | with 10 μM ISO | p.5 |
| Standard submaximal agonist concentration | 10 | μM ISO | — | pp.5–9 |
| Nb80 minimal-endogenous-effect concentration (alone) | 1 | μM | bimane, no ISO | p.6 |
| Nb80 saturating concentration | 3.2 | μM | bimane + 10 μM ISO | p.8 |
| Peptide concentration matching Nb80 1 μM shift | 10 | μM | bimane + 10 μM ISO | p.8 |
| Maximum testable peptide concentration (solubility ceiling) | 50 | μM | — | p.8, p.9 |
| Peptide 2 / 4 effect on ISO Emax | decreased, dose-dependently | % of max ISO response | vs buffer, β2AR membranes | p.8, Fig 4H–I |
| Peptide 2 effect on ISO EC50 | right-shifted | — | vs buffer | p.8 |
| Peptide 4 and Nb80 effect on ISO EC50 | no shift (Emax decrease only) | — | vs buffer | p.8 |
| cAMP replicates | n = 3–6 experiments, in duplicate | experiments | mean ± SEM | p.9 (Fig 4 caption) |
| Unbiased MD sampling | 20 replicates × 2 | μs | peptide 4 + β2AR | p.8 |
| Peptide 4 starting distance from crevice | ~30 | Å | to avoid imposed contacts | p.8 |
| Spontaneous binding events observed | 5 | events | across the 20 replicates | p.8 |
| TM6 local kink tilt, β2AR-peptide 4 complex | 74 | ° | at G280^6.42 | p.10 |
| TM6 local kink tilt, β2AR-Gs(empty), PDB 3SN6 | 35 | ° | reference | p.10 |
| TM6 outward tilt spread across overlaid states | 9 | Å | inactive 2RH1 vs active states | p.10 (Fig 5B(i) annotation) |
| Bimane fluorophore excitation / emission | 395 / 480–500 | nm | unconjugated | p.5 |
| Peptides synthesised and tested | 9 stapled + native GαsCT15 + 2 linear counterparts | compounds | — | p.5 (Table 1), p.8 |

  Note: the quantified bimane parameters (λmax shifts) and cAMP EC50/Emax values live in **Tables S8, S9 and S10 in the Supporting Information, which is not part of this 13-page PDF**. The main text reports them only qualitatively.

- **n_predictions**: **NOT APPLICABLE in the prediction sense.** Sampling scale, recorded separately:
  - MD, unbiased: **20 replicates × 2 μs = 40 μs**, on **1** system (peptide 4 + β2AR), p.8.
  - MD, enhanced sampling: multiple-walker well-tempered metadynamics on the same single system; **walker count and aggregate time not stated in the main text** (a representative frame is cited as "MetaDynamics walker3, cluster 265", p.10) — see `unresolved`.
  - Wet lab: **12 distinct peptides** (9 stapled, 2 linear counterparts, 1 native GαsCT15) × up to **3** receptors; cAMP n = 3–6 per curve; bimane spectra "representative of several individual repeats" with n given only in Table S9 (pp.6–9).

- **comparable_to_ours**: **NONE, with one hedged exception.** No number in this paper sits beside a prediction metric — there is no RMSD, no TM-score, no success rate, no per-target sampling count of predicted structures. The single hedged comparator is **conceptual, not numerical**: if we make a claim about a peptide/partner being able to drive a receptor to an active state, this paper is the experimental anchor for the *direction* of that effect and, importantly, for its *conditionality* (agonist required). Use it as a citation, not as a table row.

- **si_in_scope**: **New in v3. SI NOT HELD, and it is material — every quantitative pharmacology number in this paper lives there.** Specifically: **Table S8** (cAMP inhibition, the correlation with bimane potentiation), **Table S9** (bimane repeats; the main text gives no numerical λmax anywhere), **Table S10** and **Figure S4** (the β1AR and D1R counter-screens), **Figure S1** (the failed Y391dmPhe variant and the unstapled counterpart of peptide 9), **Figure S3** (whole-cell cAMP). The main text carries the argument; the SI carries the evidence. Any number quoted from this paper must come from the SI, which the corpus does not hold.

## F. Figures

License note applies to all rows: **CC BY-NC** — *"This is an open access article under the terms of the Creative Commons Attribution-NonCommercial License, which permits use, distribution and reproduction in any medium, provided the original work is properly cited and is not used for commercial purposes."* (p.1). **No ND clause**, so redrawing and modification are permitted for non-commercial use.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A-B | 3 | The two crystallographic binding modes of GαsCT on β2AR (3SN6 vs 6E67), showing that Y391 or E392 — never both — reaches R131^3.50 | structure render | `RENDER \| systems: 1 (β2AR) \| views: 2 (β2AR-Gs(empty) mode, β2AR-T4L-GsCT-CC mode) \| overlay: 0 predictions on 2 reference(s) \| axis: none` | 2 panels, varying by reference structure | | CC BY-NC, p.1 |
| 1C | 3 | Per-residue RMSF of GαsCT free in water vs bound in each of the two complexes — the flexibility profile that motivates the staple placement | scatter | `PLOT \| facet: none (1) \| x: peptide residue 380–394 (15) \| y: RMSF (Å) \| mark: point \| n_per_cell: NOT REPORTED` | 1 panel, 3 overlaid simulation conditions | n per condition not shown; no error bars; data are re-used from ref [33] and the number of trajectories behind each point is never stated | CC BY-NC, p.1 |
| 1D-E | 3 | Intracellular receptor surface: solvent-exposed basic residues, and the same surface coloured by hydropathy index | structure render | `RENDER \| systems: 1 (β2AR) \| views: 2 (basic-residue sticks+surface, hydrophobicity-coloured surface) \| overlay: 0 predictions on 1 reference \| axis: none` | 2 panels, varying by surface property | | CC BY-NC, p.1 |
| 1 (right, unlettered) | 3 | "Design strategy" cartoon — receptor barrel with the stapled peptide docked below | schematic | `SCHEMATIC \| cartoon of a stapled helical peptide entering the intracellular crevice of a 7TM receptor \| no data` | 1 panel | | CC BY-NC, p.1 |
| Scheme 1A-C | 4 | Synthetic route: CuAAC (i, i+7) stapling of bis-azido peptides with 1,3-diethynylbenzene, and the (i, i+4) case | schematic | `SCHEMATIC \| three-step reaction scheme for CuAAC macrocyclisation of linear azido peptides into stapled peptides 1–9 \| no data` | 3 panels (A, B, C), varying by stapling chemistry | | CC BY-NC, p.1 |
| 2A-upper | 6 | The two candidate staple positions (I383-Q390 green, I382-R389 blue) drawn onto each of the two crystal binding modes, two views each | structure render | `RENDER \| systems: 2 (β2AR-Gs(empty), β2AR-T4L-GsCT-CC) \| views: 2 (two orientations per complex) \| overlay: 2 candidate staples on 2 reference(s) \| axis: none` | 4 sub-views in 2 groups, varying by complex and orientation | | CC BY-NC, p.1 |
| 2A-lower | 6 | Sequence bead diagram of GαsCT15 with each residue coloured by which crystal structure it contacts, and the two candidate linker spans drawn beneath | schematic | `SCHEMATIC \| 15-residue sequence track annotated with per-residue receptor contacts from 3SN6/6E67 and two alternative staple spans \| no data` | 1 panel | contact assignment is binary/coloured with no underlying quantity, so the strength of each contact is not recoverable | CC BY-NC, p.1 |
| 2B | 6 | Concept cartoon of the bimane assay: C265^6.27 probe on lower TM6 moves into a hydrophilic environment on activation | schematic | `SCHEMATIC \| membrane-embedded 7TM cartoon showing the bimane label on TM6 and its displacement on activation \| no data` | 1 panel | | CC BY-NC, p.1 |
| 2C | 6 | Bimane emission spectra: ISO dose series; Nb80; native linear GαsCT15 (no effect); stapled peptide 1 (works) | line | `PLOT \| facet: test article (4: ISO CRC, Nb80, GαsCT15, peptide 1) \| x: emission wavelength 430–510 nm (continuous) \| y: normalised fluorescence intensity \| mark: line \| n_per_cell: NOT REPORTED ("representative of several individual repeats", Table S9)` | 4 panels, varying by test article; 4–6 traces per panel by concentration/condition | **Yes.** Representative traces only — no n, no error bands, no quantified λmax shift in the main figure; the ranking claim rests on eyeballing overlaid curves. y-axis truncated (starts ~0.3–0.4, not 0), which visually amplifies the intensity drop | CC BY-NC, p.1 |
| 3 (structures) | 7 | Chemical structures of peptides 2, 3, 4, linear 2, and 8 drawn above their respective assay panels | schematic | `SCHEMATIC \| bead-and-bond chemical structures of five peptide analogues showing staple span and modified side chains \| no data` | 5 structure drawings | | CC BY-NC, p.1 |
| 3 (spectra) | 7 | The SAR panel: Nal and hGlu substitutions improve potentiation; linear peptide 2 and staple-shifted peptide 8 are dead | line | `PLOT \| facet: peptide analogue (5: 2, 3, 4, linear 2, 8) \| x: emission wavelength 430–510 nm (continuous) \| y: normalised fluorescence intensity \| mark: line \| n_per_cell: NOT REPORTED ("representative of several individual repeats", Table S9)` | 5 panels, varying by peptide; 4 traces per panel (buffer / 10 μM ISO / 20 μM peptide / ISO + peptide) | **Yes.** The paper's core SAR conclusion is delivered entirely by visual comparison of representative traces — no bar chart, no error bars, no n, and no statistic anywhere in the figure. Also note the caption reverses the staple positions relative to the body text and Table 1 | CC BY-NC, p.1 |
| 4A-F | 9 | Concentration series of Nb80, peptide 2 and peptide 4, without (A–C) and with (D–F) 10 μM ISO — the panel that establishes the peptides do nothing alone | line | `PLOT \| facet: test article × agonist present (6: {Nb80, peptide 2, peptide 4} × {no ISO, +10 μM ISO}) \| x: emission wavelength 430–510 nm (continuous) \| y: normalised fluorescence intensity \| mark: line \| n_per_cell: NOT REPORTED ("representative of several individual repeats", Table S9)` | 6 panels in a 3-column × 2-row grid; columns vary by test article, rows by agonist presence; 5–8 concentration traces per panel | **Yes.** The load-bearing negative result ("unable to stabilize an active receptor conformation alone") is shown as three panels of near-superimposed representative traces with no n, no error, and no quantified λmax — a null claim with no quantitative panel. Normalisation to peak 1.0 plus a truncated y-axis further compresses any small real effect | CC BY-NC, p.1 |
| 4G-I | 9 | ISO concentration-response for cAMP in β2AR membranes with Nb80, peptide 2, peptide 4 at two concentrations each: Emax suppression | line (dose-response) | `PLOT \| facet: test article (3: Nb80, peptide 2, peptide 4) \| x: log[ISO] (M), ~9 concentrations \| y: % of max ISO response \| mark: point + fitted curve, error bars = SEM \| n_per_cell: 3–6 experiments in duplicate` | 3 panels, varying by test article; 3 curves per panel (buffer + two blocker concentrations) | | CC BY-NC, p.1 |
| 5A-left | 10 | Radius of gyration distributions for peptide 4 bound/unbound vs GαsCT in three reference conditions — evidence the staple preserves compact helicity | box | `PLOT \| facet: none (1) \| x: Rg (Å) \| y: simulation condition (5) \| mark: box + whisker (horizontal) \| n_per_cell: NOT REPORTED (frames per condition not given)` | 1 panel, 5 conditions | n (frames or trajectories) per box not shown; boxes are drawn over MD frames, which are autocorrelated, so the whisker spread is not an independent-sample spread | CC BY-NC, p.1 |
| 5A-right | 10 | Per-residue RMSF for the same five conditions — flexibility retained only at the far C-terminus (L393/L394) when unbound | bar | `PLOT \| facet: none (1) \| x: peptide residue 381–394 (14) \| y: RMSF (Å) \| mark: grouped bar (5 series) \| n_per_cell: NOT REPORTED` | 1 panel, 14 residue groups × 5 conditions | no error bars on any bar; number of trajectories behind each bar not stated | CC BY-NC, p.1 |
| 5B-C | 10 | (i) TM6 overlay across inactive, nanobody-bound, two GsCT modes, Gs-GDP and the peptide 4 complex; (ii) peptide 4 pose vs the two crystal poses; (C) key contacts of E392hGlu and Y391Nal | structure render | `RENDER \| systems: 1 (β2AR) \| views: 3 (TM6 tilt overlay, peptide pose comparison, contact close-up) \| overlay: 1 MD pose (representative frame, MetaDynamics walker3 cluster 265) on 5 reference structure(s) (2RH1, 3P0G, 3SN6, 6E67, β2AR-Gs^GDP) \| axis: none` | 3 panels, varying by view | the MD pose is shown as **one representative frame from one metadynamics walker and one cluster**; no ensemble spread, no cluster population, no alternative low-energy poses shown, so the reader cannot judge how representative it is | CC BY-NC, p.1 |

## G. Provenance

- **extracted_on**: 2026-09-07; **re-passed to schema v3 on 2026-09-09**
- **extractor**: claude subagent (v2 pass); Claude Opus 5, session `012o2XWtza3uVnp772dQHctU` (v3 re-pass)
- **schema_version**: `v3` — re-passed 2026-09-09 against the PDF, not patched. The three fields v2 lacked (`structural_priors_used`, `controls_run`, `si_in_scope`) were extracted fresh from the paper, and two tags the v2 extractor correctly declined to invent (`g-protein-mimetic`, `experimental`) now exist in the vocabulary and are applied. **The A–E content of the original pass was checked and stands**; nothing in it needed correcting.
- **confidence**: **medium-high.** The text extracted cleanly and the argument is unambiguous. Two things reduce it: (1) **all quantitative pharmacology — λmax shifts, EC50, Emax — is in Supporting Information Tables S8–S10 that are not in this 13-page PDF**, so `metrics_reported` carries mostly design parameters and qualitative directions rather than the paper's actual potency numbers; (2) all figure panel structures were verified by rendering pages 3, 6, 7, 9 and 10 at 110 dpi, and Table 1 at 130 dpi, so the panel counts and axis descriptions are read off the images, not inferred from captions.
- **unresolved**:
  1. **Caption/text contradiction on the staple move.** Figure 3's caption (p.7) says *"moving the staple position from I383-Q390 to I382-R389 resulted in an inactive peptide (peptide 8)"*, but the body text (p.7) says peptide 8 is *"an analog of peptide 2 in which the stapling position is shifted by one position toward residues I383 and Q390"*, and Table 1 (p.5) confirms peptide 2 is stapled at 382/389 while peptide 8 is stapled at 383/390. **The caption states the direction backwards.** The body text and table agree with each other, so the caption is the error, but this should be flagged if the sentence is ever quoted.
  2. **No scrambled-sequence peptide control.** The negative controls are all *structural* (unstapled, staple moved, substitutions removed) — none is a sequence-scrambled peptide of matched composition and helicity. So "any stapled 15-mer helix of this composition would do" is not formally excluded by the data shown.
  3. **Metadynamics scale not stated in main text**: number of walkers, bias parameters, and aggregate simulation time are not given (only "walker3, cluster 265" appears, p.10). Presumably in SI section 2.3.
  4. **Quantified bimane readouts** (λmax values, shift magnitudes, n per experiment) are entirely in Table S9; the main text never gives a single numerical λmax.
  5. **Why the R380Y peptides (6, 7) are better at D1R than at β2AR** is explicitly unexplained by the authors (p.8).
  6. **Whether peptide 4 has any intrinsic (agonist-free) activity below 50 μM cannot be determined** — the solubility ceiling and the negative result are confounded (p.9).
  7. **RESOLVED 2026-09-09 by the v3 re-pass, kept for the record.** The v2 extractor listed tags they needed and correctly refused to invent. Two now exist and are applied: **`g-protein-mimetic`** (this paper is why the tag was added, and it now fires on two papers rather than one review) and **`experimental`**. Three are still genuinely absent from the vocabulary and remain open decisions for the user:
     - ~~No tag for an experimental / wet-lab paper with no structure prediction at all~~ **— `experimental` added in v3 and now applied.** (Original note: every current Method tag was a prediction method; this paper has none of them, so its Method row is empty except `md` and `enhanced-sampling`, which describe only a supporting analysis and over-represent the computational content.
     - No tag for **stapled peptide / macrocycle chemistry** (e.g. `stapled-peptide`) — `peptide-driven` covers the *control handle*, not the chemistry class.
     - ~~No tag for G-protein mimetic / G-protein surrogate as a compound class~~ **— `g-protein-mimetic` added in v3 and now applied.** This was the most manuscript-relevant reverse lookup in the corpus and it previously returned a single review.
     - No tag for **agonist-dependence / conditional state stabilisation**, which is the most citable single fact in the paper.
     - `no-anti-memorization` was **deliberately not applied**: the tag would be technically true but semantically false, since there is no model that could memorise anything. The vocabulary has no way to say "this rigour axis does not exist for this paper".
- **why_it_matters**:

## Tags

`gpcr` `experimental` `md` `enhanced-sampling` `two-state` `continuous-metric` `saturating-metric` `prospective` `directed-state` `peptide-driven` `ligand-driven` `g-protein-mimetic` `nanobody` `allosteric-site` `peer-reviewed` `precedent` `background`

Tag justifications where non-obvious:
- **`md` + `enhanced-sampling`**: all-atom MD (20 × 2 μs) plus well-tempered multiple-walker metadynamics (pp.8–9). These describe a supporting analysis, not the paper's method class — the paper's method class has no tag (see `unresolved` 7).
- **`two-state`**: the bimane readout resolves inactive vs active-like only. Flagged: the authors additionally *claim* a third, intermediate state from MD (p.10), which `two-state` does not capture and `continuum` would overstate.
- **`prospective`**: peptides were designed, synthesised, then tested, and four designs failed. Retrospective only in that the MD followed the winner.
- **`ligand-driven`**: the orthosteric agonist ISO is a required co-handle, not an incidental condition — this is the paper's own central caveat.
- **`nanobody`**: Nb80 is used throughout as the comparator G-protein surrogate (Figs 2C, 4A/D/G), and the peptides are benchmarked against it.
- **`allosteric-site`**: the target is the intracellular G-protein-binding crevice, an intracellular allosteric site distinct from the orthosteric pocket (framed as such on p.2).
- **`precedent` + `background`**: see `stance`. Provisional — the user's call.
- **NOT tagged** `no-anti-memorization`, `oracle-leak`, `unpowered`, `confidence-as-discriminator`, `multi-backbone`, `cofolding`, `msa-*`, `template-state-bias`, `benchmark-only` — none has meaning for a paper with no predictive model.
