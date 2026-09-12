# CURATE-E proposal — GPR orphans + lipid-signalling + rare aminergic receptors

Subagent: **CURATE-E**
Scope: GP101, GPR3, GPR12, GPR15, GPR34, GPR55, GPR84, GPER1, GP132, P2Y10, DRD5, FFAR2, HCAR3, SUCR1  (14 receptors)
Date: 2026-08-26

## TL;DR — headline findings

**Population reality check: this batch is structurally lopsided.** Almost every receptor in scope has *only* been solved in the Gα-coupled Active state during the 2023-2025 cryo-EM wave. There is essentially **no published inactive/antagonist-bound structure with intact 6.30 CA** for any receptor in this batch, which means the pair-discriminator gate (|Δd_active − Δd_inactive| ≥ 3.0 Å) cannot be built from experimental data for any of these 14 receptors as of the query date.

Additionally, **5 of 14 receptors have a natural (wt) sequence that violates the identity-anchor rule** (3.50 R, 5.58 Y, 7.53 Y): GPR55 (5.58 = C), GPR132 (5.58 = N), P2Y10 (5.58 = T), FFAR2 (7.53 = F), HCAR3 (5.58 = S). Per plan guardrail (1), these are refused at the receptor level — the wt does not match GPCRdb-canonical anchors, so refs_build's A1 identity gate would reject any deposit of this receptor unless the identity-anchor rule is softened. Recommend flagging these five to Phase 3 with a policy decision — this is a receptor-set scope question, not a per-PDB question.

**Realistic classifiable-prediction unlock from this batch: ~0 via full delta-discriminator path**, and **~50-150 via single-side threshold path** if the pipeline's `state_thresholds.csv` fallback accepts a `d_active_ref`-only row. Not the ~300 target — the target assumed inactive structures existed for at least half these receptors; the RCSB / GPCRdb records say they don't.

## Summary table

| Receptor | UniProt | N PDBs | States present | 3.50/5.58/7.53 (wt) | Best active PDB | d_active (Å) computed | Active verdict | Inactive verdict |
|---|---|---:|---|---|---|---:|---|---|
| **GP101** (GPR101) | Q96P66 | 3 | Active only | R/Y/Y ✓ | 8W8Q (apo-Gs) | 18.69 | PROPOSE (single-side) | REFUSED — no inactive published |
| **GPR3** | O00155 | 3 | Active only | R/Y/Y ✓ | 8WW2 (oleic-Gs) | 19.46 | PROPOSE (single-side) | REFUSED — no inactive published |
| **GPR12** | P47775 | 1 | Active only | R/Y/Y ✓ | 7Y3G (apo-Gs) | 19.01 | PROPOSE (single-side) | REFUSED — no inactive published |
| **GPR15** | P49685 | 2 | Active only | R/Y/Y ✓ | 8ZQE (GPR15L-Gi) | 15.13 | PROPOSE (single-side) | REFUSED — no inactive published |
| **GPR34** | Q9UPC5 | 9 | Active only (1 antagonist) | R/Y/Y ✓ | 8WRB (LPA-Gi) | 14.66 | PROPOSE (single-side) | REFUSED — 8IYX antagonist geometry \|Δd\|=2.96 Å fails discriminator |
| **GPR55** | Q9Y2T6 | 4 | Active only | R/**C**/Y ✗ | — | — | REFUSED — natural 5.58=Cys violates identity anchor | REFUSED — same |
| **GPR84** | Q9NQS5 | 4 | Active only | R/Y/Y ✓ | 8G05 (agonist-Gi) | 15.43 | PROPOSE (single-side) | REFUSED — no inactive published |
| **GPER1** (GPER) | Q99527 | 6 | Active only | R/Y/Y ✓ | 8XOF (agonist-Gq) | 14.72 | PROPOSE (single-side) | REFUSED — no inactive published |
| **GP132** (GPR132) | Q9UNW8 | 4 | Active only | R/**N**/Y ✗ | — | — | REFUSED — natural 5.58=Asn violates identity anchor | REFUSED — same |
| **P2Y10** | O00398 | 1 | Active only | R/**T**/Y ✗ | — | — | REFUSED — natural 5.58=Thr violates identity anchor | REFUSED — same |
| **DRD5** | P21918 | 1 | Active only | R/Y/Y ✓ | 8IRV (rotigotine-Gs) | 18.31 | PROPOSE (single-side) | REFUSED — no inactive published |
| **FFAR2** | O15552 | 5 | Active only | R/Y/**F** ✗ | — | — | REFUSED — natural 7.53=Phe violates identity anchor | REFUSED — same |
| **HCAR3** | P49019 | 4 | Active only | R/**S**/Y ✗ | — | — | REFUSED — natural 5.58=Ser violates identity anchor | REFUSED — same |
| **SUCR1** (SUCNR1) | Q9BXA5 | 7 | Active only | R/Y/Y ✓ | 8YKV (CHEMBL5430997-Gi) | 14.64 | PROPOSE (single-side) | REFUSED — no inactive published |

**Totals:** 9 PROPOSE-active / 5 REFUSED-both / 0 pairs discriminator-eligible / 0 predictions unlocked via full delta path.

## Query methodology

- Structure enumeration: GPCRdb `/services/structure/protein/<slug>/` for each receptor, cross-checked with RCSB full-text search for GPR101 / GPR132 / GPER1 (GPCRdb missed some — RCSB canonical).
- Anchor residue positions: GPCRdb `/services/residues/extended/<slug>/` with `display_generic_number` field, matched against canonical 3.50/5.58/7.53 identity anchors + 3.51/6.34 diagnostic + 6.30 CA target.
- d_r350_r630_ca measurements: mmCIF ATOM records downloaded from files.rcsb.org, CA-CA distance computed on `auth_seq_id` + `auth_asym_id` selection for the receptor chain of each proposed deposit. Full script trace in this doc's provenance section.

---

## Per-receptor × per-role entries

### GP101 (GPR101) / active

- Chosen PDB: **8W8Q**
- GPCRdb URL: https://gpcrdb.org/structure/8W8Q/
- RCSB entity summary: Cryo-EM structure of the GPR101–Gs complex, apo. Receptor is a BRIL–GPR101 N-terminal fusion (Soluble cytochrome b562 fused N-terminally as fiducial; not excising 6.30).
- Resolution: 2.89 Å
- Stabilising elements: N-terminal BRIL fusion (fiducial only), Nb35 (Gα stabiliser)
- Gα coupling: yes, Gαs (P63092) + Gβ1γ2
- Activation evidence: GPCRdb `state=Active`; Gs-coupled heterotrimeric complex resolved; TM6 in outward conformation as measured (d_r350_r630_ca = 18.7 Å — well above the ~10-12 Å inactive baseline for Class A).
- Measured d_r350_r630_ca (Å): **18.69** (chain C, R129 CA to Q394 CA; GPCRdb positions 3.50 = R129, 6.30 = Q394)
- construct label: `bril_fusion_nterm` (BRIL at N-term; 6.30 intact; NOT an ICL3-fusion — safe)
- Alt PDBs considered:
  - 8W8R (agonist AA-14 + Gs, res 3.3): usable secondary; picked 8W8Q for higher resolution.
  - 8W8S (agonist AA-14, no G, res 3.3): no Gα coupling; passed over.
- Discriminator check: no inactive counterpart available → **CANNOT PAIR**. |Δd| undefined.
- Verdict: **PROPOSE (single-side active reference only)**. Refs_build.py should compute d_active_ref from 8W8Q; downstream classification uses `state_thresholds.csv` fallback (no delta-pair possible).

### GP101 (GPR101) / inactive

- Verdict: **REFUSED**. Reason: no experimental inactive-state or non-Gα-coupled antagonist-bound structure of GPR101 published as of 2026-08-26 query. All three RCSB entries (8W8Q, 8W8R, 8W8S) are Gs-active or agonist-bound. Recommend Phase 3 escalation to consider whether single-side `d_active_ref`-only classification is acceptable for this receptor's ~30-70 predictions.

---

### GPR3 / active

- Chosen PDB: **8WW2**
- GPCRdb URL: https://gpcrdb.org/structure/8WW2/
- RCSB entity summary: Cryo-EM structure of GPR3–Gs complex with oleic acid (agonist).
- Resolution: 2.79 Å (best of GPR3 catalog)
- Stabilising elements: none reported (no Nb / no scFv beyond standard Gα-stabilizing chaperone)
- Gα coupling: yes, Gαs + Gβ1γ2
- Activation evidence: GPCRdb `state=Active`, Gs-coupled, agonist-bound (oleic acid, endogenous lipid), TM6 opened (d = 19.5 Å)
- Measured d_r350_r630_ca (Å): **19.46** (chain R, R134–T242)
- construct label: `wt`
- Alt PDBs considered:
  - 8U8F (palmitic acid + Gs, 3.49 Å): lower resolution.
  - 8X2K (N-oleoylethanolamide + Gs, 3.03 Å): third-choice.
- Discriminator check: **no inactive** — cannot pair.
- Verdict: **PROPOSE (single-side)**.

### GPR3 / inactive

- Verdict: **REFUSED**. Reason: no inactive/antagonist-bound structure of GPR3 published. All three deposits are Gs-active with an endogenous fatty-acid agonist. Recommend Phase 3 note.

---

### GPR12 / active

- Chosen PDB: **7Y3G**
- GPCRdb URL: https://gpcrdb.org/structure/7Y3G/
- RCSB entity summary: Cryo-EM structure of the apo GPR12–Gs complex (constitutive activity).
- Resolution: 2.77 Å
- Stabilising elements: none reported
- Gα coupling: yes, Gαs + Gβ1γ2
- Activation evidence: GPCRdb `state=Active`, Gs-coupled heterotrimer; TM6 outward (d = 19.0 Å)
- Measured d_r350_r630_ca (Å): **19.01** (chain R, R138–T246)
- construct label: `wt`
- Alt PDBs considered: none — 7Y3G is the only deposit.
- Discriminator check: **no inactive** — cannot pair.
- Verdict: **PROPOSE (single-side)**.

### GPR12 / inactive

- Verdict: **REFUSED**. Reason: only 1 GPR12 deposit exists (7Y3G, active); no inactive published.

---

### GPR15 / active

- Chosen PDB: **8ZQE**
- GPCRdb URL: https://gpcrdb.org/structure/8ZQE/
- RCSB entity summary: Cryo-EM of GPR15 in complex with peptide agonist GPR15LG and Gi heterotrimer.
- Resolution: 2.9 Å
- Stabilising elements: none reported
- Gα coupling: yes, Gαi1 + Gβ1γ2
- Activation evidence: GPCRdb `state=Active`, Gi-coupled, agonist peptide bound; d = 15.1 Å (moderate but active per GPCRdb)
- Measured d_r350_r630_ca (Å): **15.13** (chain R, R131–L236)
- construct label: `wt`
- Alt PDBs considered:
  - 9WXM (full-length GPR15L + Gi, 3.3 Å): lower resolution.
- Discriminator check: **no inactive** — cannot pair.
- Verdict: **PROPOSE (single-side)**. Note: 15.1 Å is relatively low for a Gi-coupled state — the 6.30 residue is L, not the canonical polar residue, which may compress the ionic-lock geometry.

### GPR15 / inactive

- Verdict: **REFUSED**. Reason: both 8ZQE and 9WXM are Gi-coupled active; no inactive published.

---

### GPR34 / active

- Chosen PDB: **8WRB**
- GPCRdb URL: https://gpcrdb.org/structure/8WRB/
- RCSB entity summary: Cryo-EM of GPR34–Gi complex with LPA (lysophosphatidic acid, endogenous agonist).
- Resolution: 2.91 Å
- Stabilising elements: none major
- Gα coupling: yes, Gαi1 + Gβ1γ2
- Activation evidence: GPCRdb `state=Active`, Gi-coupled, endogenous lipid agonist bound; d = 14.7 Å (active-consistent, ionic lock broken)
- Measured d_r350_r630_ca (Å): **14.66** (chain R, R152–Y261)
- construct label: `wt`
- Alt PDBs considered: 8K4N, 8SAI, 8XBH, 8XBI, 8IZ4, 8XBE, 8XBG — all Gi-coupled agonist-bound actives. 8WRB picked for endogenous ligand + tied-best resolution.
- Discriminator check: **paired against 8IYX (below); |Δd|=2.96 Å < 3.0 → FAILS**.
- Verdict: **PROPOSE (single-side)**.

### GPR34 / inactive (attempted)

- Considered PDB: 8IYX
- Rationale for consideration: 8IYX is the only GPR34 deposit bound to a genuine antagonist (YL-365) *and* not coupled to a G-protein.
- Measured d_r350_r630_ca (Å) on 8IYX: **11.70** (chain C, R152–Y261) — consistent with an intermediate/inactive-like conformation (TM6-in).
- Discriminator check vs 8WRB active: |Δd| = 14.66 − 11.70 = **2.96 Å** — falls **below** the 3.0 Å threshold by 0.04 Å.
- Note: GPCRdb still labels 8IYX `state=Active`, but the actual geometry is inactive-like. The discriminator cutoff is (correctly) refusing to trust this pair as a resolvable state discriminator.
- Verdict: **REFUSED**. Reason: discriminator fails by 0.04 Å; propose escalating to Phase 3 with a policy question — soften threshold to 2.5 Å (would admit this pair), or accept that GPR34 needs a genuine antagonist-only crystal structure (not currently deposited).

---

### GPR55 / active

- Verdict: **REFUSED at receptor level**. Reason: natural wt sequence has **Cys at 5.58 (C201)** instead of canonical Tyr. Per plan guardrail (1) "Identity-defining anchors (3.50 R, 5.58 Y, 7.53 Y) must match GPCRdb-reported residues. No exceptions, no soft-fail." Even though 4 Gα13-coupled active PDBs exist (8ZX4, 8ZX5, 9IY8, 9IYA), refs_build's A1 gate would refuse the row because the receptor sequence itself does not carry the canonical DRY/PIF/NPxxY anchor set.
- Alt PDBs enumerated (rejected):
  - 8ZX4: LPI (agonist) + Gα13, 2.85 Å — active, but receptor-level identity mismatch.
  - 8ZX5: AM251 + Gα13, 3.03 Å — active.
  - 9IY8: apo + Gα13, 3.01 Å — active.
  - 9IYA: antagonist + no G, 3.04 Å — but 6.30 (Q221) is disordered / unresolved, so also fails 6.30-CA measurement.
- Recommend Phase 3 policy note on GPR55: receptor is a non-canonical Class A (Cys-5.58 lineage, together with GPR35 / P2RY receptors); may need a class-specific identity anchor set (e.g. R/C/Y variant tolerated) or explicit exclusion.

### GPR55 / inactive

- Verdict: **REFUSED**. Same identity-anchor reason. No usable inactive candidate anyway (9IYA has disordered 6.30).

---

### GPR84 / active

- Chosen PDB: **8G05**
- GPCRdb URL: https://gpcrdb.org/structure/8G05/
- RCSB entity summary: Cryo-EM of GPR84–Gi complex with 6-octyliminopyrimidinedione (agonist).
- Resolution: 3.0 Å (best of GPR84 catalog with resolved 6.30)
- Stabilising elements: none major
- Gα coupling: yes, Gαi1 + Gβ1γ2
- Activation evidence: GPCRdb `state=Active`, Gi-coupled, agonist bound; d = 15.4 Å
- Measured d_r350_r630_ca (Å): **15.43** (chain R, R118–F314)
- construct label: `disordered_icl3_flanking` — the receptor has a very long ICL3 (~97 residues, seq 218-314 unresolved / disordered) but the 6.30 CA (F314) is directly at the resumption of TM6 and IS resolved on this deposit. All other flanking geometry is intact.
- Alt PDBs considered:
  - 8J18 (3.23 Å, agonist HXD + Gi): **REJECTED — 6.30 CA (F314) unresolved**; TM6 begins at 315 in this deposit. Fails guardrail (3).
  - 8J1A (3.24 Å, apo + Gi): **REJECTED — 6.30 CA unresolved**, same reason as 8J18.
  - 8J19 (3.23 Å, agonist SWO + Gi): 6.30 F314 IS resolved; usable but marginally lower resolution than 8G05.
- Discriminator check: **no inactive** — cannot pair.
- Verdict: **PROPOSE (single-side)** with construct label flagged.

### GPR84 / inactive

- Verdict: **REFUSED**. Reason: no inactive published; all 4 deposits are Gi-active. Two of the four (8J18, 8J1A) additionally fail on 6.30 CA disorder — even if an inactive attempt was made, the ICL3-flanking geometry is fragile for this receptor.

---

### GPER1 (GPER) / active

- Chosen PDB: **8XOF**
- GPCRdb URL: https://gpcrdb.org/structure/8XOF/
- RCSB entity summary: Cryo-EM of GPER–Gq complex with an aminoquinoline agonist.
- Resolution: 2.60 Å (highest resolution in GPER catalog)
- Stabilising elements: none major
- Gα coupling: yes, Gαq + Gβ1γ2
- Activation evidence: GPCRdb `state=Active`, Gq-coupled, agonist bound; d = 14.7 Å (active-consistent). Note: 6.30 is R (arginine), which is non-canonical for the ionic lock — GPER has an atypical DRY/6.30 replacement.
- Measured d_r350_r630_ca (Å): **14.72** (chain R, R155–R254)
- construct label: `wt` — the non-canonical R6.30 is *native* to GPER1, not an engineering artefact.
- Alt PDBs considered:
  - 8XOG (apo + Gq, 2.9 Å): apo active — secondary.
  - 8XOH (PGE2 + Gq, 3.2 Å): PGE2-bound active.
  - 8XOI (fulvestrant + Gq, 3.2 Å): fulvestrant is reported as GPER *agonist* — still active.
  - 8XOJ (G-1 + Gq, 3.1 Å): G-1 is canonical GPER agonist.
  - 9X74 (Gq complex, 3.15 Å): additional active.
- Discriminator check: **no inactive** — cannot pair.
- Verdict: **PROPOSE (single-side)** with caveat noted on non-canonical 6.30=R (native).

### GPER1 / inactive

- Verdict: **REFUSED**. Reason: all 6 GPER deposits are Gq-coupled active with either agonist or apo (no antagonist-only structure). Additionally, the receptor has a non-canonical 6.30=R which complicates canonical-Class-A ionic-lock interpretation even if an inactive structure existed.

---

### GP132 (GPR132) / active

- Verdict: **REFUSED at receptor level**. Reason: natural wt sequence has **Asn at 5.58 (N219)** instead of canonical Tyr. Identity anchor violated. Also 3.51 = Phe instead of Tyr (diagnostic — could be recorded rather than gating, but 5.58 alone kills this receptor).
- Alt PDBs enumerated (rejected):
  - 8HQE: apo + Gi, 2.97 Å (BRIL N-term fusion) — active, but identity mismatch.
  - 8HQM: NPGLY + Gi, 2.95 Å — active.
  - 8HQN: 9(S)-HODE + Gi, 3.0 Å — active.
  - 8HVI: NOX-6-7 + Gi, 3.04 Å — active.
- Recommend Phase 3 policy note: GPR132 belongs to the small orphan cluster with non-canonical 5.58. Same policy question as GPR55.

### GP132 (GPR132) / inactive

- Verdict: **REFUSED**. Same reason. Also no inactive published.

---

### P2Y10 / active

- Verdict: **REFUSED at receptor level**. Reason: natural wt sequence has **Thr at 5.58 (T218)** instead of canonical Tyr, and Cys at 3.51 (diagnostic — recordable rather than gating). Identity anchor violated. Only 1 P2Y10 deposit exists (8KGG, Gα13-coupled active).
- Recommend Phase 3 policy note: P2Y10 shares the P2Y cluster's non-canonical 5.58 (T/C/N). Class-A anchor exception for the P2Y subfamily may be needed if these receptors are to be scored on TM6 axis at all.

### P2Y10 / inactive

- Verdict: **REFUSED**. Same reason.

---

### DRD5 / active

- Chosen PDB: **8IRV**
- GPCRdb URL: https://gpcrdb.org/structure/8IRV/
- RCSB entity summary: Cryo-EM of DRD5 (D5 dopamine receptor)–Gs complex with rotigotine (agonist).
- Resolution: 3.10 Å
- Stabilising elements: none reported
- Gα coupling: yes, Gαs + Gβ1γ2
- Activation evidence: GPCRdb `state=Active`, Gs-coupled, agonist bound; d = 18.3 Å (canonical active — 6.30 is E, the classic ionic-lock partner)
- Measured d_r350_r630_ca (Å): **18.31** (chain R, R138–E291)
- construct label: `wt`
- Alt PDBs considered: none — 8IRV is the only DRD5 deposit. UniProt-precise RCSB search (P21918) returns exactly 1 entry.
- Discriminator check: **no inactive** — cannot pair.
- Verdict: **PROPOSE (single-side)**. Note that D5 is genuinely one of the least-structurally-characterised aminergic receptors — recommend using D1 (DRD1) inactive/antagonist-bound structures as *paralog reference* only if the pipeline supports paralog fallback; refuse otherwise.

### DRD5 / inactive

- Verdict: **REFUSED**. Reason: only 1 DRD5 deposit published (8IRV, Gs-active with rotigotine). Recommend Phase 3 policy note: could paralog-borrow DRD1 inactive (e.g. 7CKW, 7LJC family) if pipeline supports; if not, DEFER indefinitely — the ~30-50 DRD5 predictions from the corpus become permanently unclassifiable via delta axis but classifiable via single-side threshold.

---

### FFAR2 / active

- Verdict: **REFUSED at receptor level**. Reason: natural wt sequence has **Phe at 7.53 (F273)** instead of canonical Tyr of the NPxxY motif. Identity anchor violated. Note: 5.58 = Y and 3.50 = R are canonical — FFAR2 fails only on the NPxxY position.
- Alt PDBs enumerated (rejected):
  - 8J22 (Gi + CHEMBL4176503 agonist, 3.2 Å) — active.
  - 8J23 (Gi + apo, 3.2 Å) — active.
  - 8J24 (Gi + acetic acid, 2.6 Å) — best resolution.
  - 8T3S (Gaq + butyric acid, 3.07 Å) — active.
  - 9K1D (Gi + butyric acid, 3.34 Å) — active.
- Recommend Phase 3 policy note: FFAR2 (and its paralog FFAR3, HCAR2, and free-fatty-acid family members) canonically substitute F for Y at 7.53 — the NPxxF motif is a real family variant, not an anchor drift artefact. A subfamily-specific anchor set (NPxxF variant) might be required if these are to be scored.

### FFAR2 / inactive

- Verdict: **REFUSED**. Same reason. Also no inactive published.

---

### HCAR3 / active

- Verdict: **REFUSED at receptor level**. Reason: natural wt sequence has **Ser at 5.58 (S208)** instead of canonical Tyr. Identity anchor violated.
- Alt PDBs enumerated (rejected):
  - 8IHJ (Gi + P9X agonist, 3.07 Å) — active.
  - 8IHK (P9X only, 3.21 Å) — active.
  - 8JEF (Gi + 3HO agonist, 2.96 Å) — active, best resolution.
  - 8JEI (Gi + CW3 agonist, 2.73 Å) — active, tied best resolution.
- Recommend Phase 3 policy note: HCAR3 shares the hydroxycarboxylic-acid receptor family's non-canonical 5.58 (also HCAR1/2 candidates). Same subfamily-anchor question.

### HCAR3 / inactive

- Verdict: **REFUSED**. Same reason.

---

### SUCR1 (SUCNR1) / active

- Chosen PDB: **8YKV**
- GPCRdb URL: https://gpcrdb.org/structure/8YKV/
- RCSB entity summary: Cryo-EM of SUCNR1–Gi complex with CHEMBL5430997 (agonist).
- Resolution: 2.48 Å (highest resolution in SUCR1 catalog)
- Stabilising elements: none major
- Gα coupling: yes, Gαi1 + Gβ1(rat)γ2(bovine)
- Activation evidence: GPCRdb `state=Active`, Gi-coupled, agonist bound; d = 14.6 Å
- Measured d_r350_r630_ca (Å): **14.64** (chain R, R120–L227)
- construct label: `wt` (chimeric G-protein subunits but receptor is human wt)
- Alt PDBs considered:
  - 8JPN (cis-epoxysuccinate + Gi, 2.9 Å) — active, secondary.
  - 8JPP (succinate + Gs, 3.2 Å) — active with Gs (rare Gs coupling).
  - 8WOG / 8WP1 (succinate/epoxysuccinate + Gi, 2.97/3.15 Å) — actives.
  - 8YKW (succinate + Gi, 2.75 Å) — active.
  - 8YKX (maleate + Gi, 2.69 Å) — active.
- Discriminator check: **no inactive** — cannot pair.
- Verdict: **PROPOSE (single-side)**. Note: 14.6 Å is at the low end of Class-A active — 6.30 = L (leucine), a hydrophobic non-canonical residue at that position.

### SUCR1 / inactive

- Verdict: **REFUSED**. Reason: all 7 SUCR1 deposits are Gi- or Gs-coupled active with succinate-family agonists. No antagonist-bound / inactive published.

---

## Cross-cutting notes for Phase 3 / user review

### Identity-anchor policy — 5-receptor question

Five receptors in this batch (GPR55, GPR132, P2Y10, FFAR2, HCAR3) have a natural sequence that violates one of the three canonical identity anchors (all fail 5.58=Y except FFAR2 which fails 7.53=Y). Per the strict plan guardrail these are refused wholesale. **This is a receptor-set scope decision, not a per-PDB question.** Options for user / Phase 3:

- (a) Keep the strict rule; flag these 5 receptors as permanently out-of-scope on TM6 axis (add to `refs/uncovered_receptors.txt` with note `non_canonical_identity_anchor`).
- (b) Introduce a subfamily-specific anchor set (e.g. NPxxF variant for FFAR family; 5.58={Y,C,S,T,N} tolerated for P2Y / GPR55 / GPR132 / HCAR clusters). Requires refs_build.py A1 gate to load a per-family anchor manifest.
- (c) Accept these receptors under a distinct `identity_check=subfamily_variant` flag with a soft-warning recorded in provenance rather than a hard refusal.

Total predictions affected across these 5 receptors: estimated ~100-150 (proportional to the batch total). Recommendation: (a) for the current sprint (matches the plan's audit-discipline principle), revisit as (b) later if the subfamily-specific anchor manifest is desired.

### Single-side active reference — 9-receptor question

Nine receptors pass the identity anchor check and have Active state structures, but *none* have an inactive counterpart. If the pipeline supports a single-side `d_active_ref`-only classification (via `state_thresholds.csv` fallback), all 9 unlock a subset of their predictions. If the pipeline requires a valid pair for delta classification, all 9 unlock 0 predictions via delta path.

The scorer code has both paths (per plan §Phase 3 "delta path covers most receptors and thresholds become secondary"), so the single-side entries have value — but the value materialises only through the threshold fallback, not the primary axis. Please confirm this interpretation before Phase-4 build.

### GPR34 discriminator-just-below-threshold case

GPR34 is the one receptor in this batch where an inactive-like conformation *does* exist experimentally (8IYX, antagonist-bound YL-365, no G-protein) but the pair discriminator fails at |Δd| = 2.96 Å, 0.04 Å below the 3.0 Å cutoff. Two ways forward:

- Accept the pair with an explicit `discriminator_marginal` flag recorded in provenance and downstream analyses can filter on it. This bends the plan's rule (3.0 Å is meant as hard cutoff).
- Refuse and defer indefinitely (matches plan's strict interpretation).

Recommendation: strict refuse (matches the plan's audit-discipline principle). Note this case as a candidate to revisit if a new inactive GPR34 crystal / cryo-EM structure is deposited.

## Provenance summary — measurements

All d_r350_r630_ca values in the table were computed directly on the deposited PDBs via CA-CA distance between the GPCRdb-assigned 3.50 and 6.30 sequence positions on the receptor chain (identified by matching the 3.50 Arg residue on the receptor chain of each mmCIF).

Script trace (short form): `urllib.urlretrieve(files.rcsb.org/download/<PDB>.cif.gz)` → parse `ATOM` records → filter `label_atom_id == 'CA'` → select receptor chain by 3.50=ARG marker → compute `sqrt((x1-x2)^2 + (y1-y2)^2 + (z1-z2)^2)`. Measurements verified against expected Class-A active TM6-out range (12-20 Å) — all 9 PROPOSE-active measurements fall in this window. Full per-PDB anchor residue lookup used GPCRdb `/services/residues/extended/<slug>/`.

## Corpus recovery estimate for CURATE-E batch

| Bucket | Receptors | Est. predictions | Recovery path |
|---|---|---:|---|
| PROPOSE-active (single-side) | GP101, GPR3, GPR12, GPR15, GPR34, GPR84, GPER1, DRD5, SUCR1 | ~150-200 | Via state_thresholds.csv fallback only — no delta axis |
| REFUSED — non-canonical anchor | GPR55, GP132, P2Y10, FFAR2, HCAR3 | ~100-150 | Phase 3 policy call needed (or permanently uncovered) |
| REFUSED — discriminator marginal | GPR34 inactive-side only | ~0 | Deferred; single-side handles active |
| **Total via delta axis (Phase 4 primary path)** | | **~0** | — |
| **Total via single-side threshold (fallback path)** | | **~150-200** | If scorer supports single-side reference |

The plan estimated ~300 predictions for this batch. Reality is ~150-200 recoverable *only if* the scorer's single-side fallback is used; the remaining ~100-150 are blocked by receptor-level identity-anchor policy and require a Phase-3 subfamily-anchor decision.
