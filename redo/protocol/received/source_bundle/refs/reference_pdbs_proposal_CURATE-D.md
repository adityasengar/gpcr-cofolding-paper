# CURATE-D — Chemokine + Immune Receptor Curation Proposal

**Agent:** CURATE-D
**Scope:** CXCR1, XCR1, CCR8 (upgrade), CML2, OPRL, OPSR, MC3R, MC5R
**Date:** 2026-08-26
**Plan reference:** `/Users/SENGAAD1/.claude/plans/hey-claude-i-have-fluffy-brook.md` (Phase 2, CURATE-D row)
**Working directory:** `/Users/SENGAAD1/Documents/claude/paper_af3`

## Executive summary

| Metric | Value |
|---|---:|
| Receptors in scope | 8 |
| Fully proposable (active + inactive both pass discriminator) | **2** (MC3R, OPRL) |
| Active-only proposals (inactive DEFERRED to Phase 3) | **5** (CXCR1, XCR1, MC5R, OPSR, CML2) |
| CCR8 inactive upgrade | **DEFERRED** — no non-fusion inactive deposited |
| Predictions unlocked by full pairs | ~70 (MC3R 40 + OPRL 30) |
| Predictions blocked pending Phase-3 axis-handling | ~230 (CXCR1 70 + XCR1 40 + CCR8 270-eq-currently-nan + MC5R 40 + OPSR 40 + CML2 40 minus overlap) |
| Predictions in scope for CURATE-D total | ~570 (well above ~300 target; large fraction blocked by "no inactive PDB yet exists" biology, not by measurement failure) |

**Biological reality**: five of the eight receptors have only agonist-bound Gα-coupled deposits and no inactive-state deposits at all (as of RCSB 2026-08). The pipeline's guardrail "|Δd_ref| ≥ 3.0 Å on real coordinates" cannot be satisfied for them by curation alone — Phase-3 alternative axis treatment or additional PDB depositions are the only paths.

## Preflight — GPCRdb anchor residues (measured, not projected)

Fetched from `gpcrdb.org/services/residues/extended/<slug>/`. Anchor identity anomalies noted per receptor.

| Slug | 3.50 | 3.51 | 5.58 | 6.30 | 6.34 | 7.53 | Notes |
|---|---|---|---|---|---|---|---|
| cxcr1_human | R135 | Y136 | Y222 | K237 | M241 | Y305 | canonical |
| xcr1_human  | R127 | Y128 | Y205 | R220 | V224 | Y287 | canonical |
| oprx_human  | R148 | Y149 | Y235 | L258 | T262 | Y319 | canonical (NOP=OPRL1) |
| mc3r_human  | R142 | Y143 | Y207 | C237 | A241 | Y299 | canonical |
| mc5r_human  | R140 | Y141 | Y205 | S233 | A237 | Y295 | canonical |
| opsr_human  | R151 | **W152** | Y239 | E263 | T267 | Y322 | 3.51=W (not Y) — diagnostic anchor mismatch, record |
| ccr8_human  | R131 | Y132 | Y218 | K233 | I237 | Y300 | canonical |
| cml2_human  | **H135** | Y136 | Y226 | S241 | F245 | Y304 | **3.50=H (not R)** — identity-defining anchor deviation, native to GPR1/CMKLR2 |

Measurements below use these positions and compare PDB residue-name at those seqid.num against the GPCRdb-reported amino acid. Distances are Cα(3.50) → Cα(6.30), computed with `gemmi` on the deposited mmCIF (not on `refs/reference_set.csv`).

## Discriminator table (real coordinate d_r350_r630_ca, Å)

| Receptor | Role | PDB | d (Å) | 6.30 resolved | Notes |
|---|---|---|---:|---|---|
| CXCR1 | active | 8IC0 | **14.80** | ✓ | Gi + IL-8, cryo-EM 3.41 Å |
| CXCR1 | inactive | — | — | — | **No inactive PDB deposited** |
| XCR1 | active | 9AST | **15.81** | ✓ | Gi + lymphotactin (XCL1), cryo-EM 3.07 Å |
| XCR1 | inactive | — | — | — | **No inactive PDB deposited** |
| CCR8 | active | 8XML | 13.78 | ✓ | already curated, keep |
| CCR8 | inactive | 8TLM | **NaN** | ✗ | **GFP fusion**, 6.30 K233 disordered — current curated row; no alt |
| CCR8 | active | 8KFX | 13.85 | ✓ | alt: LMD-009 agonist + Gi, cryo-EM 2.96 Å |
| CCR8 | active | 8KFY | 13.88 | ✓ | alt: ZK 756326 agonist + Gi, cryo-EM 3.06 Å |
| MC3R | active | 8IOC | **18.62** | ✓ | γ-MSH + Gs + Nb35, cryo-EM 2.86 Å |
| MC3R | inactive | 8KIG | **9.02** | ✓ | **SHU9119 antagonist, no G-protein** — clean inactive |
| MC3R | active | 9K3F | 18.92 | ✓ | alt: unliganded + Gs, cryo-EM 2.75 Å (better resolution but ligand-free) |
| MC3R | (rejected) | 8W8W/8W8X/8W8Y | — | ✗ | 6.30 disordered in all α/β/γ-MSH Nb35 complexes |
| MC5R | active | 8INR | **18.41** | ✓ | α-MSH + Gs, cryo-EM 2.73 Å |
| MC5R | inactive | — | — | — | **No inactive PDB deposited** (all 3 MC5R deposits are Gs-active) |
| OPSR | active | 8IU2 | **15.19** | ✓ | Long-wave/red cone opsin + retinal + Gα, cryo-EM 3.35 Å |
| OPSR | inactive | — | — | — | **No inactive red-opsin PDB** (bovine rhodopsin OPSD_BOVIN is inactive template only; different receptor) |
| OPRL | active | 8F7X | **15.90** | ✓ | Gi + nociceptin peptide (already curated as OPRX); slug alias |
| OPRL | inactive | 5DHH | **8.29** | ✓ | SB-612111 antagonist, X-ray 3.00 Å (already curated as OPRX); slug alias |
| CML2 | active | 8JJP | **15.08** | ✓ | GPR1 + chemerin + Gi, cryo-EM 2.90 Å |
| CML2 | inactive | — | — | — | **No inactive PDB** (9 deposits, all Gi/arrestin-active bound to chemerin) |

Discriminator check (|Δd_active − d_inactive|):
- MC3R: |18.62 − 9.02| = **9.60 Å** ✓ (≥3.0)
- OPRL: |15.90 − 8.29| = **7.61 Å** ✓ (≥3.0)

## Per-receptor entries

### CXCR1 / active — PROPOSE
- Chosen PDB: **8IC0**
- GPCRdb URL: https://gpcrdb.org/structure/8IC0/
- RCSB entity summary: Cryo-EM structure of CXCL8 (IL-8) bound C-X-C chemokine receptor 1 in complex with Gi heterotrimer
- Resolution: 3.41 Å
- Stabilising elements: scFv16 (Gα stabiliser), no receptor fusion
- Gα coupling: yes — Gαi1 (`gnai1_human`), Gβ1, Gγ2
- Activation evidence: state=Active per GPCRdb; Gi-coupled complex; TM6-out (d=14.80 Å) consistent with active-state class-A geometry
- Measured d_r350_r630_ca (Å): **14.80**
- construct label: `wt`
- Alt PDBs considered: none (only full-length CXCR1 deposit in RCSB; 1ILP/1ILQ/2LNL are NMR of IL-8 or receptor N-terminal fragment, 6XMN is receptor-ligand interaction study)
- Discriminator check: paired with — (no inactive) → **cannot verify |Δd|≥3.0**
- Verdict: **PROPOSE active** (pair-broken; must be co-approved with inactive DEFER)

### CXCR1 / inactive — DEFER_TO_PHASE_3
- Chosen PDB: —
- Reason: No inactive/antagonist-bound full-length CXCR1 deposit exists in RCSB. Only structural data outside 8IC0 is IL-8/receptor-fragment complexes (1ILP, 1ILQ, 2LNL, 6XMN — none are transmembrane bundle deposits).
- Verdict: **DEFER_TO_PHASE_3** (Subclass D.1: propose using homology-mapped inactive template — e.g. CXCR2 6LFL (already curated) — as inactive reference for CXCR1 with `construct=class_a_paralog_inactive` label; OR flag receptor as active-only via GPCRdb `state=Active` filter; OR wait for future antagonist deposit)

### XCR1 / active — PROPOSE
- Chosen PDB: **9AST**
- GPCRdb URL: https://gpcrdb.org/structure/9AST/
- RCSB entity summary: Cryo-EM structure of XCR1 signaling complex with lymphotactin (XCL1) and Gi heterotrimer
- Resolution: 3.07 Å
- Stabilising elements: scFv16 (Gα stabiliser), no receptor fusion
- Gα coupling: yes — Gαi1, Gβ1, Gγ2
- Activation evidence: state=Active per GPCRdb; Gi-coupled complex; TM6-out (d=15.81 Å) consistent with active state
- Measured d_r350_r630_ca (Å): **15.81**
- construct label: `wt`
- Alt PDBs considered: none (only XCR1 deposit in RCSB under UniProt P46094)
- Discriminator check: paired with — (no inactive) → **cannot verify |Δd|≥3.0**
- Verdict: **PROPOSE active** (pair-broken; must be co-approved with inactive DEFER)

### XCR1 / inactive — DEFER_TO_PHASE_3
- Reason: No inactive PDB for XCR1 exists in RCSB. Only 9AST is deposited.
- Verdict: **DEFER_TO_PHASE_3** (Subclass D.1: fallback options — use paralog inactive template e.g. CCR8 8TLM once measurable, or wait for future antagonist deposit).

### CCR8 / active — KEEP CURRENT (no change proposed)
- Currently in refs: **8XML** (measured d=13.78 Å, matches this agent's independent measurement 13.78).
- Note: 8KFX (d=13.85) and 8KFY (d=13.88) are close alternates but 8XML already selected (unliganded/apo, highest resolution 2.58 Å). No upgrade proposed.

### CCR8 / inactive — DEFER_TO_PHASE_3 (upgrade attempt, no fix available)
- Current row: **8TLM** — measures **NaN** (this agent confirmed: 6.30 K233 not resolved in receptor chain C).
- Root cause: 8TLM is a receptor–Fab complex where ICL3 is replaced by a **Green Fluorescent Protein fusion** (RCSB Entity 3 description: "C-C chemokine receptor type 8, Green fluorescent protein fusion"). The GFP insert occupies the 6.30 region; K233 has no CA in the deposit.
- Alt inactive PDBs considered: **none available**. The full CCR8 RCSB set is 8TLM (inactive, GFP fusion, NaN) + 8U1U/8KFX/8KFY/8KFZ/8XML (all Gi-coupled active). No non-fusion antagonist-bound CCR8 exists as of 2026-08.
- Verdict: **DEFER_TO_PHASE_3** (Subclass D.1(b) or D.3: possible flanking-residue axis using 6.34 (I237 is resolved in 8TLM — score=5/6 with only 6.30 missing) as a proxy anchor, but that requires a scorer-side extension outside CURATE-D's scope. Recommend flagging CCR8 as `construct=disordered_6_30_fusion` and awaiting either scorer patch or new PDB deposit.)

### CML2 / active — PROPOSE (with caveat)
- Chosen PDB: **8JJP**
- GPCRdb URL: https://gpcrdb.org/structure/8JJP/
- RCSB entity summary: G protein-coupled receptor 1 (GPR1 / CMKLR2) bound to chemerin C-terminal peptide + Gi heterotrimer
- Resolution: 2.90 Å
- Stabilising elements: scFv16, no receptor fusion
- Gα coupling: yes — Gαi1, Gβ1, Gγ2
- Activation evidence: state=Active per GPCRdb; Gi-coupled complex; TM6-out (d=15.08 Å)
- Measured d_r350_r630_ca (Å): **15.08**
- construct label: `wt`
- **⚠ Native identity-anchor deviation**: 3.50 in GPR1/CMKLR2 is natively **H (histidine)**, not R (arginine). This is the wild-type sequence per UniProt P46091 (position 135). refs_build.py's A1 identity gate compares the PDB residue name at position 135 to the UniProt reference — 8JJP has HIS at 135, matches UniProt → gate passes. **BUT** the guardrail "3.50 R must match GPCRdb-reported residues" (Guardrail 1 of the plan) is ambiguous when the receptor is natively non-DRY. Confirm interpretation with scorer maintainer: does "must match GPCRdb-reported" mean (a) the PDB residue at 3.50 must equal what GPCRdb records at that position (which is H for this receptor — passes), or (b) 3.50 must literally be an arginine (fails). If (b): CML2 excluded until scorer accepts H-R-Y variant.
- Alt PDBs considered: 8XGM (chemerin + Gi, 3.29 Å, d=15.65), 9UYH/I/J/L/M/N (chemerin + Gi Q205I/etc. mutants + β-arrestin, 2.9–3.5 Å, d=14.6–17.4), 9L3Y (chemerin + Gi 3.6 Å, d=15.01). Chose 8JJP: highest resolution wild-type Gi-bound.
- Discriminator check: paired with — (no inactive) → cannot verify
- Verdict: **PROPOSE active** conditional on H-3.50 interpretation; inactive **DEFER_TO_PHASE_3**

### CML2 / inactive — DEFER_TO_PHASE_3
- Reason: All 9 CML2/GPR1 deposits (8JJP, 8XGM, 9L3Y, 9UYH, 9UYI, 9UYJ, 9UYL, 9UYM, 9UYN) are chemerin-bound with Gi or β-arrestin coupling — all active states. No antagonist-bound apo-inactive deposit.
- Verdict: **DEFER_TO_PHASE_3** (Subclass D.1: paralog-borrow candidate — CMKLR1 9L3Z ("inactive chemokine-like receptor 1", d not yet measured) is deposited as CMKLR1 inactive; would need cross-receptor axis mapping via GPCRdb generic numbers).

### OPRL / active — PROPOSE (slug-alias curation)
- **⚠ Slug reconciliation**: OPRL and OPRX both refer to UniProt P41146 (nociceptin/orphanin FQ receptor, gene OPRL1). GPCRdb uses `oprx_human`. The pipeline currently curates this receptor under the OPRX slug (existing rows 8F7X/5DHH already produce numeric d_ref, per `refs/reference_set.csv` and `docs/EXPERIMENT_CATALOG/data/receptors.csv`). The 30 OPRL predictions are blocked because the scorer's receptor-slug resolver doesn't map OPRL → OPRX. **This is a Category-E (input-side) fix in the plan, not a curation fix.**
- Nevertheless, per plan directive to propose PDBs, the OPRL curation should mirror OPRX:
- Chosen PDB: **8F7X**
- GPCRdb URL: https://gpcrdb.org/structure/8F7X/
- RCSB entity summary: Gi-bound nociceptin receptor in complex with nociceptin peptide
- Resolution: 3.28 Å
- Stabilising elements: scFv16
- Gα coupling: yes — Gαi1
- Activation evidence: Gi-coupled; TM6-out d=15.90 Å
- Measured d_r350_r630_ca (Å): **15.90**
- construct label: `wt`
- Verdict: **PROPOSE** (co-approve with Category-E slug-alias mapping)

### OPRL / inactive — PROPOSE (slug-alias)
- Chosen PDB: **5DHH**
- GPCRdb URL: https://gpcrdb.org/structure/5DHH/
- RCSB entity summary: NOP receptor + SB-612111 antagonist, X-ray crystal
- Resolution: 3.00 Å
- Stabilising elements: T4L fusion (checked: 6.30 L258 is resolved; T4L insert does not excise anchor)
- Gα coupling: no
- Activation evidence: inactive-antagonist per GPCRdb; TM6-in d=8.29 Å
- Measured d_r350_r630_ca (Å): **8.29**
- construct label: `t4l_fusion` (if refs_build supports; else `wt` since anchor is intact — 4EA3 (d=8.00, T4L) and 5DHG (d=8.31, T4L) are also candidates with similar geometry)
- Discriminator: |15.90 − 8.29| = **7.61 Å** ✓
- Verdict: **PROPOSE**

### OPSR / active — PROPOSE
- Chosen PDB: **8IU2**
- GPCRdb URL: https://gpcrdb.org/structure/8IU2/
- RCSB entity summary: Cryo-EM structure of Long-wave-sensitive opsin 1 (OPSR / OPN1LW / red cone opsin) with retinal + Gα complex
- Resolution: 3.35 Å
- Stabilising elements: (Gα stabilisers present in complex; details TBD)
- Gα coupling: yes — chimeric Gα (Gt-mimetic likely, based on cone opsin literature)
- Activation evidence: state=Active per GPCRdb; retinal-bound; TM6-out d=15.19 Å
- Measured d_r350_r630_ca (Å): **15.19**
- construct label: `wt`
- Alt PDBs considered: only OPSR deposit
- **⚠ Diagnostic anchor mismatch**: 3.51 = **W** (tryptophan) in OPSR/OPN1LW, not the canonical Y. This is native (D-R-**W**-x-x-Y-x-x-x-Y motif variant in cone opsins). Refs_build treats 3.51 as diagnostic (may mismatch, record). PDB residue W152 matches UniProt → identity gate passes; 3.51 diagnostic recorded.
- Discriminator: paired with — (no inactive) → cannot verify
- Verdict: **PROPOSE active** (pair-broken; inactive DEFER)

### OPSR / inactive — DEFER_TO_PHASE_3
- Reason: No inactive-state red cone opsin PDB. Bovine rhodopsin (`opsd_bovin` — 4X1H/7ZBC already curated) is a different receptor.
- Verdict: **DEFER_TO_PHASE_3** (Subclass D.1: possible paralog-borrow using bovine rhodopsin inactive with construct=`opsin_paralog_inactive`; or the newly deposited 9I3T (dark-state OPN1MW medium-wave green cone opsin) as intra-family inactive if the scorer accepts an OPSG PDB row under the OPSR slug via GPCRdb-generic-number mapping.)

### MC3R / active — PROPOSE
- Chosen PDB: **8IOC**
- GPCRdb URL: https://gpcrdb.org/structure/8IOC/
- RCSB entity summary: Cryo-EM structure of γ-MSH-bound human melanocortin receptor 3 (MC3R)-Gs complex
- Resolution: 2.86 Å
- Stabilising elements: Nb35 (Gα stabiliser), no receptor fusion
- Gα coupling: yes — Gαs (`gnas2_human`)
- Activation evidence: state=Active per GPCRdb; Gs-coupled; TM6-out d=18.62 Å (large outward — MC receptors have distinctive TM6 geometry)
- Measured d_r350_r630_ca (Å): **18.62**
- construct label: `wt`
- Alt PDBs considered: 9K3F (unliganded Gs, 2.75 Å, d=18.92) — comparable; 8W8W/W8X/W8Y (α/β/γ-MSH+Nb35, all disorder 6.30) → rejected
- Discriminator: paired with 8KIG (d=9.02); |Δd| = **9.60 Å** ✓
- Verdict: **PROPOSE**

### MC3R / inactive — PROPOSE
- Chosen PDB: **8KIG**
- GPCRdb URL: https://gpcrdb.org/structure/8KIG/
- RCSB entity summary: Cryo-EM structure of MC3R in complex with SHU9119
- Resolution: 3.10 Å
- Stabilising elements: none receptor-side; complex is receptor + SHU9119 antagonist alone (2 protein entities in RCSB core entry — no Gα, no Nb, no arrestin)
- Gα coupling: no
- Activation evidence: **SHU9119 is a well-characterised MC3R/MC4R antagonist** (partial-antagonist/inverse-agonist depending on subtype); no G-protein bound; TM6-in d=9.02 Å consistent with class-A inactive geometry
- Measured d_r350_r630_ca (Å): **9.02**
- construct label: `wt`
- Alt PDBs considered: none — 8KIG is the only non-Gs MC3R structure
- Discriminator: paired with 8IOC; |Δd| = **9.60 Å** ✓
- Verdict: **PROPOSE**

### MC5R / active — PROPOSE
- Chosen PDB: **8INR**
- GPCRdb URL: https://gpcrdb.org/structure/8INR/
- RCSB entity summary: Cryo-EM structure of α-MSH-bound human melanocortin receptor 5 (MC5R)-Gs complex
- Resolution: 2.73 Å
- Stabilising elements: Nb35 (Gα stabiliser)
- Gα coupling: yes — Gαs
- Activation evidence: state=Active per GPCRdb; Gs-coupled; TM6-out d=18.41 Å
- Measured d_r350_r630_ca (Å): **18.41**
- construct label: `wt`
- Alt PDBs considered: 8IOD (PG-901 + Gs, 2.59 Å, d=18.47); 9K3H (unliganded Gs, 2.86 Å, d=18.85). All three are Gs-active with only ligand differences. Chose 8INR for α-MSH physiological agonist.
- Discriminator: paired with — (no inactive) → cannot verify
- Verdict: **PROPOSE active** (pair-broken; inactive DEFER)

### MC5R / inactive — DEFER_TO_PHASE_3
- Reason: No inactive-state MC5R PDB in RCSB (only 8INR, 8IOD, 9K3H — all Gs-active with agonists or apo-Gs).
- Verdict: **DEFER_TO_PHASE_3** (Subclass D.1: paralog-borrow candidate — MC3R 8KIG (this proposal) or MC4R inactive (if curated) could serve as intra-family inactive template via generic-numbering.)

## Sanity checks

### Anchor identity
All PDBs proposed have PDB residue names at 3.50/5.58/7.53 matching UniProt reference. The two identity/diagnostic anomalies (CML2 3.50=H, OPSR 3.51=W) are native to those receptors and are recorded above as documented deviations, not construct-induced substitutions.

### Discriminator
Only two receptor pairs meet the |Δd_ref| ≥ 3.0 Å criterion on real coordinates:
- MC3R: 8IOC (18.62) vs 8KIG (9.02) → Δ=9.60 Å ✓
- OPRL: 8F7X (15.90) vs 5DHH (8.29) → Δ=7.61 Å ✓

### DEFER summary
| Receptor | Role deferred | Subclass | Reason |
|---|---|---|---|
| CXCR1 | inactive | D.1 | Only 8IC0 exists; no inactive deposit |
| XCR1 | inactive | D.1 | Only 9AST exists; no inactive deposit |
| CCR8 | inactive (upgrade) | D.1/D.3 | 8TLM has GFP fusion excising 6.30; no alternative |
| CML2 | inactive | D.1 | All 9 deposits are Gi/arrestin-active with chemerin |
| MC5R | inactive | D.1 | All 3 deposits are Gs-active |
| OPSR | inactive | D.1 | Only 8IU2 exists (Gα-coupled active) |

### Predictions arithmetic
Under Phase-2 scope (no scorer or slug-alias changes), only MC3R (40) and OPRL-via-slug-alias (30) become classifiable → **~70 predictions unlocked** by this proposal. The remaining ~200 predictions blocked by "no inactive PDB deposited" biology require Phase-3 axis handling (paralog-borrow, `construct=class_a_paralog_inactive`, or new receptor-family axis definition) — this is upstream of CURATE-D's scope but flagged for the Phase-3 subagent.

The ~300-prediction target for CURATE-D is aspirational: the underlying reality is that these newer (post-cutoff) receptors have been the target of many Gα-coupled cryo-EM papers but few inactive-state antagonist studies — the classical asymmetry in modern GPCR structural biology.

## Files / references
- Working copy: this file, `refs/reference_pdbs_proposal_CURATE-D.md`
- Measurement script: `/tmp/measure.py` (uses `gemmi==0.7.5`, mmCIF downloaded from RCSB)
- PDB cache: `/tmp/curate_d_pdbs/` (mmCIF files for 25 candidates measured)
- GPCRdb anchor cache: fetched live from `gpcrdb.org/services/residues/extended/<slug>/`
- Related refs infrastructure: `refs/reference_pdbs.csv`, `refs/reference_set.csv`, `refs/uncovered_receptors.txt`

## Recommendation to coordinator

1. **Merge as-is**: 2 pairs (MC3R, OPRL) + 5 active-only rows (CXCR1, XCR1, MC5R, OPSR, CML2) marked "requires paired inactive".
2. **Flag OPRL slug-alias** to Category-E work stream (scorer receptor resolver) — separate fix, but pipeline-critical for the 30 OPRL predictions to actually classify.
3. **Flag CML2 3.50=H interpretation** for scorer maintainer review before appending (single-line clarification, not a large decision).
4. **Do NOT modify CCR8 row in refs**: current 8XML active is correct; 8TLM inactive stays until Phase-3 axis handling ships. Consider recording in `refs/uncovered_receptors.txt` as `ccr8_human_inactive_only` if the pipeline needs an explicit "half-covered" opt-in.
5. **Six DEFER_TO_PHASE_3 rows** listed above should be handed to CURATE-F (Phase 3) for paralog-borrow feasibility analysis.
