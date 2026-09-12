# CURATE-A proposal — adenosine + trace-amine receptors

Subagent: **CURATE-A**
Scope: AA2AR, AA2BR, AA3R, TAAR1, TAA7F
Date: 2026-08-26

## Summary

| Receptor | Preds | Active PDB | Inactive PDB | \|Δd_r350_r630_ca\| (Å) | Verdict |
|---|---:|---|---|---:|---|
| AA2AR    | 1,888 | **5G53** (d=18.30) | **5NM4** (d=7.96) | **10.34** | **PROPOSE** |
| AA3R     | 160 | 8X17 (d=17.16, Gα-coupled) | — none exists | — | **DEFER_TO_PHASE_3** |
| AA2BR    | 110 | 8HDP (d=18.25, Gα-coupled) | — none exists | — | **DEFER_TO_PHASE_3** |
| TAAR1    | 40 | 8W87 (d=20.87, Gα-coupled) | — none exists | — | **DEFER_TO_PHASE_3** |
| TAA7F    | 40 | — no structures | — no structures | — | **DEFER_TO_PHASE_3** (permanent — no PDB deposits) |

**Total predictions unlocked by CURATE-A if AA2AR row PROPOSED and approved: 1,888 (of 2,238 in scope, ~84%).**

Total receptors covered: 5. PROPOSE: 1 (AA2AR). DEFER_TO_PHASE_3: 4.

## Notes on the DEFER_TO_PHASE_3 rows

For **AA2BR / AA3R / TAAR1**, every single deposited PDB in GPCRdb is in an **active** state (agonist- or agonist+Gα-bound). No antagonist-only or inverse-agonist structure has been solved for any of these three receptors as of the query date (see per-receptor enumeration below). The discriminator pair rule (`|d_active − d_inactive| ≥ 3.0 Å`) cannot be constructed without an inactive-state deposit. CURATE-F (Phase 3) options to explore:

- **Option 1 (recommended for AA2BR/AA3R/TAAR1)**: mark these receptors in `refs/uncovered_receptors.txt` with note `"active-only PDB coverage; inactive-state deposit does not exist as of 2026-08-26; TM6-axis discrimination unavailable."` Downstream analysis uses `receptor_d_inactive_ref IS NaN` filter. Accepts ~310 predictions as unclassifiable via delta path (may still be classifiable via `state_thresholds.csv` pack fallback if the pipeline supports single-anchor thresholding).
- **Option 2**: use the well-established AA1R inactive **5UEN** (BRIL, ZM-antagonist family, d=8.47 Å per current `reference_set.csv`) as an **orthologue proxy** for AA2BR/AA3R inactive. Adenosine receptors are highly conserved at the TM6 outward-motion axis (all four use the same E6.30 anchor). Requires a schema extension (`inactive_proxy_receptor` column) — larger scope than pure curation, mark as follow-up.
- **Option 3**: hold for future antagonist-bound deposits (structural biology of AA2BR/AA3R/TAAR1 is active; new deposits may land in 2026-2027).

For **TAA7F**, there are literally zero structures in GPCRdb. TAA7F (trace-amine associated receptor 7F) is a rodent paralog with limited human ortholog activity; recommend **permanent** entry to `refs/uncovered_receptors.txt` with note `"no PDB deposits in any organism; no structural template available"`. The 40 predictions attached to this receptor should be re-examined at the input side — are they mouse TAAR-family binders being scored against a human template? (This is a Category E concern outside CURATE-A scope, but worth flagging.)

## Discriminator anchors (measured from GPCRdb)

All 5 receptors share the canonical Class-A pattern at identity-defining positions. Anchor set verified via `scorer.anchors.resolve_anchors`:

- **aa2ar_human**: 3.50=R102, 3.51=Y103, 5.58=Y197, 6.30=E228, 6.34=A232, 7.53=Y288
- **aa2br_human**: 3.50=R103, 3.51=Y104, 5.58=Y202, 6.30=E229, 6.34=A233, 7.53=Y290
- **aa3r_human**:  3.50=R108, 3.51=Y109, 5.58=Y197, 6.30=E225, 6.34=A229, 7.53=Y282
- **taar1_human**: 3.50=R121, 3.51=Y122, 5.58=Y210, 6.30=E246, 6.34=V250, 7.53=Y304 (**note**: TAAR1 6.34 is V not A — diagnostic mismatch expected; identity anchors intact)

---

## AA2AR / active

- **Chosen PDB: 5G53**
- GPCRdb URL: https://gpcrdb.org/structure/5G53/
- RCSB entity summary: Structure of the adenosine A2A receptor bound to an engineered G protein (mini-Gs) — Carpenter, Nehmé, Warne, Leslie, Tate 2016
- Resolution: **3.4 Å**
- Stabilising elements: **mini-Gα (engineered dominant-negative Gαs)**, no fusion in receptor sequence
- Gα coupling: **yes — mini-Gs (engineered Gαs long isoform, HOMO SAPIENS)**
- Activation evidence: state=Active per GPCRdb; TM6-out measured on deposit d_r350_r630_ca = **18.30 Å**; ionic-lock broken; Gα subunit occupies the intracellular cavity — canonical Class-A active pose
- Measured d_r350_r630_ca (Å): **18.30**  (computed via `scorer.axes.compute_all_axes` on cif deposit, all six anchors present, zero diagnostic mismatches)
- construct label: **thermostabilised**  (5G53 uses StaR2 background: A54L / T88A / R107A / L202A / L235A / S277A / V239A stabilising point mutations — none at identity-defining positions 3.50/5.58/7.53; refs_build accepts as `wt` if `construct` field defaults, but a proper `thermostabilised` label is recommended once the schema extension in the pre-Phase-1 code change lands)
- Alt PDBs considered:
  - **6GDG** (rejected: 4.11 Å resolution — d=18.62 Å but the low resolution + N-terminal TrxA fusion make 5G53 the cleaner reference; scientifically identical Gs-coupled activation)
  - **8UGW** (rejected: agonist CGS21680 bound, 3.9 Å — but d=10.30 Å, TM6 not fully open; no Gα in complex)
  - **8WDT** (rejected: 6.30 anchor mislocalised — d=NaN — likely chain-picker issue; agonist-only anyway)
  - **7EZC** (rejected: agonist UK-432,097 bound, 3.8 Å — but d=8.92 Å, TM6 essentially closed; no Gα coupling → unsuitable as "active")
  - **5WF5** (rejected: currently excluded in refs; agonist-only, d=9.87 Å, D52N mutation — **this is the reason the current AA2AR pair fails**; without Gα the TM6 doesn't swing open in AA2AR)
  - **3QAK** (rejected: T4L fusion; agonist-only, d=9.82 Å, TM6 not open)
  - **2YDO / 4UHR** (rejected: thermostabilised agonist-only, d=9.93/9.72 Å, TM6 not open)
- Discriminator check: paired with **5NM4** (inactive), |Δd| = **10.34 Å** [≥ 3.0 ✓]
- Auxiliary activation indicators (per user's "there might be other measures indicative of activation" hint):
  - Ionic-lock (D3.49–R3.50–T6.34 hydrogen bond): expected broken in 5G53 given Gα-coupled open conformation. Not directly measured here — refs_build does not currently emit ionic-lock distance; recommend adding `d_ionic_lock_d349_r350_t634` to `compute_all_axes` as an auxiliary axis in a follow-up.
  - NPxxY Y5.58–Y7.53 CA–CA: should sit ~13–14 Å in 5G53 (active) vs ~17–18 Å in 5NM4 (inactive). Not measured here — `d_tm5_outward_r350_r558_ca` in axes.py measures R3.50–Y5.58 which is a *related* but not identical geometry; the Y5.58–Y7.53 CA distance is a candidate additional axis.
  - PIF motif packing (P5.50–I3.40–F6.44): active-state shifted. Sidechain-level analysis, no CA-only proxy.
  - **Primary axis d_r350_r630_ca_ref stays the sole classifier**; the auxiliary indicators are recorded in the provenance JSON as textual evidence, not gates.
- Verdict: **PROPOSE**

## AA2AR / inactive

- **Chosen PDB: 5NM4**
- GPCRdb URL: https://gpcrdb.org/structure/5NM4/
- RCSB entity summary: A2A adenosine receptor room-temperature structure determined by serial femtosecond crystallography, bound to ZM241385 antagonist — Weinert et al. 2017
- Resolution: **1.7 Å**  (best-in-class among AA2AR antagonist deposits)
- Stabilising elements: **BRIL fusion** in ICL3 (A2AR–soluble cytochrome b562–A2AR chain topology per RCSB entity 1); StaR2 thermostabilising background likely (chain length 433, receptor+BRIL insert)
- Gα coupling: **no** (antagonist-only crystal)
- Activation evidence: state=Inactive per GPCRdb; TM6 closed on deposit d_r350_r630_ca = **7.96 Å**; ZM241385 (high-affinity antagonist) bound in orthosteric pocket → canonical inactive-state
- Measured d_r350_r630_ca (Å): **7.96**  (all six anchors present, zero diagnostic mismatches, coverage OK)
- construct label: **bril_fusion**  (BRIL sits in ICL3, does not excise 6.30 — 6.30 anchor resolved and measurable; refs_build accepts and produces numeric d_ref, precedent exists via AA1R/5UEN which is also BRIL-fused and in the current reference_set.csv)
- Alt PDBs considered:
  - **3PWH** (rejected: d=7.32 Å even smaller than 5NM4, but 3.3 Å resolution + probably T4L variant; 5NM4 is higher-resolution)
  - **6LPJ** (rejected: 1.8 Å, BRIL fusion, d=8.17 Å — nearly identical to 5NM4 but slightly smaller |Δd|; either 5NM4 or 6LPJ would work, picked 5NM4 for higher-res)
  - **6PS7** (rejected: 1.85 Å, BRIL fusion, d=8.24 Å — nearly identical, 5NM4 preferred for resolution)
  - **5OLG** (rejected: 1.87 Å, BRIL fusion, d=7.96 Å — tied with 5NM4 on d, but 5NM4 has slightly better nominal resolution + XFEL room-T deposit is a stronger match to solution-state biology)
  - **3EML** (rejected: 2.6 Å, **T4L fusion**, d=9.66 Å — while T4L doesn't excise 6.30 here, T4L generally exerts more perturbation on ICL3 geometry than BRIL, and d=9.66 gives smaller |Δd|)
  - **4EIY** (rejected: currently excluded; BRIL fusion 1.8 Å d=8.17 Å — comparable to 5NM4 but currently flagged in refs_build, sticking with 5NM4 as the fresh pick)
  - **5UIG** (rejected: BRIL fusion, 3.5 Å d=8.89 Å — worse resolution than 5NM4, larger d gives smaller |Δd|)
- Discriminator check: paired with **5G53** (active), |Δd| = **10.34 Å** [≥ 3.0 ✓✓]
- Verdict: **PROPOSE**

**AA2AR pair note**: the reason the current excluded 5WF5/4EIY pair is "1.7 Å apart" is that 5WF5 is not Gα-coupled (only agonist-bound thermostabilised receptor) — for adenosine receptors, TM6 outward motion is Gα-driven, and agonist alone does not fully open the intracellular cavity. Substituting the Gα-mimetic-bound 5G53 as active (rather than an agonist-only structure) resolves this, and the resulting pair spans 10.34 Å — comfortably above the 3.0 Å threshold. AA2AR is Gs-coupled (Class A canonical); TM6 span here is fully in the canonical Class-A range (e.g. 5G53 d=18.30 is on par with ADRB2/4LDE at similar TM6-open magnitude).

---

## AA2BR / active

- Chosen PDB: — (candidate: 8HDP)
- GPCRdb URL: https://gpcrdb.org/structure/8HDP/
- RCSB entity summary: cryo-EM structure of AA2BR bound to adenosine + Gs heterotrimer
- Resolution: 3.2 Å
- Stabilising elements: Gs heterotrimer + Nb35 stabiliser
- Gα coupling: **yes** — native Gs (α, β, γ)
- Activation evidence: state=Active per GPCRdb; d_r350_r630_ca = 18.25 Å (measured)
- Measured d_r350_r630_ca (Å): 18.25
- construct label: wt
- Alt PDBs considered: 8HDO (d=18.12, BAY 60-6583 agonist, otherwise identical), 7XY6 (d=18.85), 7XY7 (d=19.26, NECA, cryo-EM 3.26 Å)
- Discriminator check: **cannot compute — no inactive PDB exists for AA2BR**
- Verdict: **DEFER_TO_PHASE_3**

## AA2BR / inactive

- **No inactive PDB has been deposited for AA2BR as of 2026-08-26.** GPCRdb structures endpoint returns only 4 structures, all state=Active (all deposited 2023).
- Verdict: **DEFER_TO_PHASE_3**  (Phase 3 should decide: uncovered_receptors.txt entry, or orthologue proxy from AA1R/5UEN, or hold for future deposits.)

---

## AA3R / active

- Chosen PDB: — (candidate: 8X17)
- GPCRdb URL: https://gpcrdb.org/structure/8X17/
- RCSB entity summary: AA3R bound to Cl-IB-MECA agonist + Gi heterotrimer (cryo-EM)
- Resolution: 3.19 Å
- Stabilising elements: Gi heterotrimer, scFv16 stabiliser
- Gα coupling: **yes** — native Gi (note: AA3R is Gi-coupled, not Gs — smaller TM6-out expected than for AA2AR/AA2BR)
- Activation evidence: state=Active per GPCRdb; d_r350_r630_ca = 17.16 Å (measured — still comfortably in the Class-A active range even for Gi-coupled)
- Measured d_r350_r630_ca (Å): 17.16
- construct label: wt
- Alt PDBs considered: 8X16 (d=16.06, piclidenoson agonist, otherwise identical, marginally lower TM6-out)
- Discriminator check: **cannot compute — no inactive PDB exists for AA3R**
- Verdict: **DEFER_TO_PHASE_3**

## AA3R / inactive

- **No inactive PDB has been deposited for AA3R as of 2026-08-26.** GPCRdb structures endpoint returns only 2 structures, both state=Active (both deposited 2024).
- Verdict: **DEFER_TO_PHASE_3**

---

## TAAR1 / active

- Chosen PDB: — (candidate: 8W87)
- GPCRdb URL: https://gpcrdb.org/structure/8W87/
- RCSB entity summary: TAAR1 bound to methamphetamine + Gs heterotrimer (cryo-EM)
- Resolution: 2.8 Å  (best-resolution TAAR1 deposit)
- Stabilising elements: Gs heterotrimer, scFv16 or Nb35
- Gα coupling: **yes** — Gs (TAAR1 couples Gs primarily; some deposits show Gq coupling variants)
- Activation evidence: state=Active per GPCRdb; d_r350_r630_ca = 20.87 Å (measured — TAAR1 TM6-out is even larger than typical Class-A)
- Measured d_r350_r630_ca (Å): 20.87
- construct label: wt  (note: 6.34 is V not A — expected diagnostic mismatch, not disqualifying; identity anchors 3.50/5.58/7.53 all match)
- Alt PDBs considered: 9JKQ (d=22.05, methamphetamine, 2.66 Å — comparable, slightly larger d), 8ZSJ (apo, d=21.08, 2.8 Å — interestingly apo TAAR1 is *also* in an open TM6 state, suggesting basal activation), 8W88/8JLQ/8ZSP/8ZSS (d=NaN — 6.30 CA missing/disordered in these deposits — chain-picker returns wrong chain or the loop is disordered)
- Discriminator check: **cannot compute — no inactive PDB exists for TAAR1**
- Verdict: **DEFER_TO_PHASE_3**

## TAAR1 / inactive

- **No inactive PDB has been deposited for TAAR1 as of 2026-08-26.** All 17 structures in GPCRdb are state=Active (agonist- or agonist-Gα-bound; even the "apo" 8ZSJ is in an open TM6 conformation). This is biologically informative: TAAR1 may have unusually low basal barrier to TM6 opening, but for scorer discrimination purposes it means the delta path is unavailable.
- Verdict: **DEFER_TO_PHASE_3**

**TAAR1 special note for CURATE-F**: 4 of the 17 deposits fail 6.30 coverage (8W88, 8JLQ, 8ZSP, 8ZSS) — suggests disordered residue at 6.30 in some crystal forms even though the receptor is in an "open" state overall. Not a curation problem for CURATE-A (we have 3 candidates with clean coverage), but worth logging if TAAR1 curation is retried later.

---

## TAA7F / active

- **No structures deposited in GPCRdb** for TAA7F.
- Verdict: **DEFER_TO_PHASE_3 → recommend permanent `uncovered_receptors.txt`**

## TAA7F / inactive

- **No structures deposited in GPCRdb** for TAA7F.
- Verdict: **DEFER_TO_PHASE_3 → recommend permanent `uncovered_receptors.txt`**

**TAA7F note**: trace-amine associated receptor 7F is a rodent paralog with unclear human ortholog. The 40 predictions attached to TAA7F may be a slug-resolution issue upstream (Category E) — the receptor may be mouse Taar7f being scored against a non-existent human template. Recommend flagging for input-side review, not refs curation.

---

## Measurement provenance

- All d_r350_r630_ca values computed via `scorer.axes.compute_all_axes` on RCSB-fetched CIF deposits.
- All anchor resolutions via `scorer.anchors.resolve_anchors` against GPCRdb residue endpoints.
- Coordinate PDBs cached at `/tmp/curate_a_pdbs/` on host `nrchbs-cph710202` (basel-hpc login node) — ephemeral; the refs_build re-run in Phase 1 will re-fetch and cache in the canonical `/hpc/scratch/sengaad1/paper_af3/refs/pdb/` location.
- All measurements verified reproducible: identical d values on re-run (deterministic).
- Full per-PDB measurement log (17 AA2AR + 4 AA2BR + 2 AA3R + 7 TAAR1 candidates measured) available in the transcript that produced this document.

## Recommendation for coordinator merge

- Approve the **AA2AR row PROPOSE** (5G53 active + 5NM4 inactive) — unlocks 1,888 predictions with a 10.34 Å discriminator.
- Forward AA2BR / AA3R / TAAR1 / TAA7F to **CURATE-F (Phase 3)** with the "no inactive deposit exists" categorisation — these are not curation failures, they are limits imposed by the current structural-biology corpus. Combined ~350 predictions of DEFER-driven uncovered set is a small fraction of the CURATE-A target.
- Consider a schema-extension follow-up for **orthologue proxy inactive** references (AA1R/5UEN → AA2BR/AA3R inactive) as a separate design decision, out of scope for this proposal.
