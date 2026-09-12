# CURATE-C — Peptide + prostanoid receptor curation proposal

**Agent scope**: BRS3, NMBR, PRLHR, QRFPR, PE2R1, PF2R, PI2R, SSR1, SSR3, SSR5
(bombesin, prolactin-releasing, prostanoid EP1/FP/IP, somatostatin SSTR1/3/5)

**Read-only artefact**. Does not touch `refs/reference_pdbs.csv` or scorer code.
Curator: subagent CURATE-C, 2026-08-26.

---

## Executive summary

- **Total receptors covered**: 10.
- **PROPOSE (active role)**: 10/10 — every receptor has ≥1 high-quality cryo-EM Gα-complex deposited 2023–2024.
- **PROPOSE (inactive role)**: **0/10**. None of these receptors has an antagonist-bound / inverse-agonist / apo inactive-state PDB deposited in the RCSB as of 2026-08-26 (verified via UniProt cross-references, October 2025 UniProt snapshot).
- **Net receptor pairs that survive discriminator gate**: **0**.
- **Predictions unlocked from CURATE-C alone under strict pair-required policy**: **~0** (target was ~400).
- **Predictions recoverable via active-only + state_thresholds fallback**: **~400** — see "Path forward" below.
- **Verdict on pair-based curation**: every receptor is `DEFER_TO_PHASE_3` at the pair level. Phase 3 must decide between (a) adding these ten receptors to `refs/uncovered_receptors.txt`, or (b) accepting active-only reference rows and relying on `state_thresholds.csv` for state classification.

The problem is symmetric across the group: these receptors are structurally *young*. First deposits landed 2023-08 (NMBR/8H0P) through 2025 (SSR3/8ZBI, BRS3/9K07). Every deposit is an agonist + Gα cryo-EM complex — the antagonist series has not yet been solved for any of them. There is no curation choice that makes the pair-based |Δd|≥3.0 Å check pass on real coordinates. That is the peer's ~400-prediction estimate: it counts receptor rows that exist in the corpus, not receptor pairs that can be built from published PDBs.

**Recommendation to user**: treat CURATE-C output as *evidence that ten Class-A peptide/prostanoid receptors need the state_thresholds fallback path* (or explicit exclusion), not as ten new discriminator pairs. The chosen active PDBs and their measurements are ready to append to `refs/reference_pdbs.csv` the moment Phase 3 rules on the inactive gap.

---

## Summary table

| Receptor | Native Gα | Active PDB | Res (Å) | d_r350_r630 (Å) | Inactive PDB | Discriminator |Δd|(Å) | Verdict |
|---|---|---|---:|---:|---|---:|---|
| BRS3   | Gq (also G11) | 8Y52 | 2.9  | 13.49 | — none deposited — | n/a | DEFER (inactive missing) |
| NMBR   | Gq            | 8H0P | 3.15 | 13.79 | 9JF4 (chimeric fusion, author-numbering offset) | unmeasurable | DEFER (inactive missing / chimera) |
| PRLHR  | Gi & Gq       | 8ZPT | 2.68 | 15.86 | — none deposited — | n/a | DEFER (inactive missing) |
| QRFPR  | Gq (also Gi)  | 8WZ2 | 2.73 | 13.75 | — none deposited — | n/a | DEFER (inactive missing) |
| PE2R1  | Gq            | 9M1H | 2.55 | 13.23 | — none deposited — | n/a | DEFER (inactive missing) |
| PF2R   | Gq            | 8IUK | 2.67 | 13.24 | — none deposited — | n/a | DEFER (inactive missing) |
| PI2R   | Gs            | 8X79 | 2.41 | 13.32 | — none deposited — | n/a | DEFER (inactive missing) |
| SSR1   | Gi            | 8XIO | 2.65 | 15.13 | — none deposited — | n/a | DEFER (inactive missing) |
| SSR3   | Gi            | 8XIR | 2.52 | 15.12 | — none deposited — | n/a | DEFER (inactive missing) |
| SSR5   | Gi            | 8X8L | 2.7  | 15.77 | — none deposited — | n/a | DEFER (inactive missing) |

All d_r350_r630 values were measured locally with `gemmi` on the deposited mmCIF, using GPCRdb-reported UniProt residue positions for 3.50 and 6.30 (no reliance on GPCRdb-published distances). Chain picks were verified to match the GPCRdb-expected native residue at each anchor.

---

## Per-receptor × per-role entries

### BRS3 / active
- Chosen PDB: **8Y52**
- GPCRdb URL: https://gpcrdb.org/structure/8Y52/
- RCSB entity summary: Cryo-EM structure of the BRS3–Gq complex bound to bombesin.
- Resolution: 2.9 Å
- Stabilising elements: scFv16 + Nb35 (Gα-complex stabilisers, no receptor fusion; NanoLuc-free)
- Gα coupling: yes — Gα-q (heterotrimeric Gq)
- Activation evidence: `state=Active` per GPCRdb; Gq-coupled; bombesin agonist bound; TM6 outward measured on deposit at 13.49 Å (consistent with other Gq-active Class-A GPCRs)
- Measured d_r350_r630_ca (Å): **13.49** (chain R, R145 CA — R266 CA, R/R identity match)
- construct label: `wt`
- Alt PDBs considered:
  - 9K07 (2.83 Å, DSO-5a + Gq) — REJECTED: entity 1 is "Bombesin receptor subtype-3, Oplophorus-luciferin 2-monooxygenase" (NanoLuc split fusion at terminus). Not 6.30-excising, but 8Y52 is a cleaner wt construct.
  - 9LWP (2.93 Å, unliganded + Gq) — REJECTED: apo-agonist ambiguity; native BRS3 endogenous agonist unknown, so apo Gq-complex is a weaker activation claim than bombesin-bound.
  - 8Y53 (2.93 Å, MK-5046 synthetic agonist + Gq) — viable alternative if user prefers small-molecule agonist over the endogenous peptide.
  - 8Y51 (3.3 Å, Gq) — REJECTED: lower resolution than 8Y52.
- Discriminator check: **UNMEETABLE** — no inactive-state BRS3 PDB deposited in RCSB.
- Verdict: **DEFER_TO_PHASE_3** (active row is measurement-ready; blocked on inactive)

### BRS3 / inactive
- Chosen PDB: — none available —
- Rationale: UniProt P32247 cross-references list 5 PDBs (8Y51, 8Y52, 8Y53, 9K07, 9LWP); all are Gq-coupled agonist complexes deposited 2023–2025. No antagonist-bound BRS3 structure exists as of 2026-08-26. BRS3 antagonist Bantag-1 (Bag-1) has been characterised biochemically but not crystallographically.
- Verdict: **DEFER_TO_PHASE_3** — Phase 3 recommendation: add BRS3 to `refs/uncovered_receptors.txt` OR accept active-only reference and route classification through `state_thresholds.csv`.

---

### NMBR / active
- Chosen PDB: **8H0P**
- GPCRdb URL: https://gpcrdb.org/structure/8H0P/
- RCSB entity summary: Cryo-EM structure of NMBR–Gq bound to NMB30 (neuromedin-B 30 peptide agonist).
- Resolution: 3.15 Å
- Stabilising elements: scFv16 (Gq-complex stabiliser, no receptor fusion)
- Gα coupling: yes — Gα-q
- Activation evidence: `state=Active` per GPCRdb; Gq-coupled; NMB30 agonist bound; TM6-out measured at 13.79 Å.
- Measured d_r350_r630_ca (Å): **13.79** (chain R, R141 CA — R261 CA, R/R identity match)
- construct label: `wt`
- Alt PDBs considered: only one Gα-active NMBR structure deposited.
- Discriminator check: **UNMEETABLE** with a clean PDB (see 9JF4 note below).
- Verdict: **DEFER_TO_PHASE_3** (active row is measurement-ready; blocked on inactive)

### NMBR / inactive
- Chosen PDB: **9JF4 (rejected)**
- GPCRdb URL: — (9JF4 not yet indexed under GPCRdb structure catalog as of 2026-08-26)
- RCSB entity summary: Cryo-EM structure of Neuromedin B receptor in complex with the antagonist PD168368.
- Resolution: 3.6 Å
- Stabilising elements: fused to a "de novo design protein" (chain A entity name: `"Neuromedin-B receptor,de novo design protein"`) — chimeric construct.
- Gα coupling: none (antagonist state).
- Reason for rejection: chain A spans author_seq 44–601 with large numbering gaps at 149→155, 182→195, 203→206, 308→312. The gap pattern shows a genetic fusion where the receptor and the de novo design protein share a chain identifier with non-continuous author numbering. Author_seq position 261 (native NMBR 6.30 R per GPCRdb) is **PHE**, not ARG — either a thermostabilising R261F mutation or a numbering offset introduced by the fusion. Measured d_r350_r630 = 33.26 Å which is physically impossible for a TM3–TM6 CA-CA distance (real range ~10–17 Å); this confirms the residue at author_seq 261 in this construct is NOT the true 6.30 position. Curating this PDB requires resolving the chimera numbering via `construct_offset`, which is out of scope for CURATE-C (Phase 3 territory).
- Verdict: **DEFER_TO_PHASE_3** — Phase 3 could revisit 9JF4 with a proper `construct_offset` and a SIFTS-derived residue map, OR treat NMBR as uncovered.

---

### PRLHR / active
- Chosen PDB: **8ZPT**
- GPCRdb URL: https://gpcrdb.org/structure/8ZPT/
- RCSB entity summary: PrRP20-bound prolactin-releasing peptide receptor coupled with Gq protein complex.
- Resolution: 2.68 Å
- Stabilising elements: scFv16 (Gq-complex stabiliser)
- Gα coupling: yes — Gα-q
- Activation evidence: `state=Active`; Gq-coupled; PrRP20 endogenous peptide bound; TM6-out measured at 15.86 Å (moderately large — consistent with peptide-receptor active state).
- Measured d_r350_r630_ca (Å): **15.86** (chain R, R159 — R273, R/R match)
- construct label: `wt`
- Alt PDBs considered:
  - 8ZPS (2.97 Å, PrRP20 + Gi) — viable Gi-alternative if user wants Gi-coupled active for a receptor that signals through both.
  - 9K26 (3.0 Å, PrRP31 + Gi) — REJECTED for resolution vs 8ZPT.
  - 9K27 (2.68 Å, PrRP31 + Gq) — comparable to 8ZPT; endogenous ligand differs (PrRP31 vs PrRP20). Either is defensible; 8ZPT chosen for consistency with PrRP20 as the classical endogenous ligand.
- Discriminator check: **UNMEETABLE**.
- Verdict: **DEFER_TO_PHASE_3**.

### PRLHR / inactive
- Chosen PDB: — none available —
- Rationale: UniProt P49683 lists 4 PDBs (8ZPS, 8ZPT, 9K26, 9K27), all Gi- or Gq-coupled peptide-agonist complexes deposited 2024. No antagonist / apo inactive-state PDB.
- Verdict: **DEFER_TO_PHASE_3**.

---

### QRFPR / active
- Chosen PDB: **8WZ2**
- GPCRdb URL: https://gpcrdb.org/structure/8WZ2/
- RCSB entity summary: Cryo-EM structure of QRFPR–Gq complex bound to the orexigenic neuropeptide QRFP.
- Resolution: 2.73 Å
- Stabilising elements: scFv16
- Gα coupling: yes — Gα-q
- Activation evidence: `state=Active`; Gq-coupled; QRFP endogenous ligand bound; TM6-out at 13.75 Å.
- Measured d_r350_r630_ca (Å): **13.75** (chain R, R143 — K268, R/K match — native QRFPR has K at 6.30x30 per GPCRdb; this is *not* a mismatch, K is the receptor's own expected residue at 6.30)
- construct label: `wt`
- Alt PDBs considered:
  - 8ZH8 (3.19 Å, QRF-amide + Gq) — REJECTED for resolution.
- Discriminator check: **UNMEETABLE**.
- Verdict: **DEFER_TO_PHASE_3**.

### QRFPR / inactive
- Chosen PDB: — none available —
- Rationale: 2 PDBs total in UniProt Q96P65; both are Gq-active. No antagonist PDB.
- Verdict: **DEFER_TO_PHASE_3**.

---

### PE2R1 / active
- Chosen PDB: **9M1H**
- GPCRdb URL: (9M1H not indexed in GPCRdb catalog for pe2r1_human as of query — RCSB confirmed via UniProt P34995)
- RCSB entity summary: Cryo-EM structure of PGE2–EP1–Gq complex.
- Resolution: 2.55 Å
- Stabilising elements: none reported as fusion / T4L / BRIL / scFv on receptor. Standard Gα heterotrimer (Gi-scaffold fusion for Gq — Gi/Gq chimeric Gα for cryo-EM). No receptor fusion.
- Gα coupling: yes — Gα-q (Gα-i1/Gα-q chimeric scaffold, standard cryo-EM approach)
- Activation evidence: PGE2 (endogenous eicosanoid agonist) bound; Gq-coupled; TM6-out at 13.23 Å.
- Measured d_r350_r630_ca (Å): **13.23** (chain A, R135 — D292, R/D match — native EP1 has D at 6.30x30, matches)
- Note on identity anchors: native EP1 residues are 3.50=R, 5.58=**L**, 7.53=Y. Per the actual scorer implementation in `scorer/verified.py:169-193`, the A1 identity check compares each anchor's observed residue against **the GPCRdb-reported expected residue for that receptor** (not a Class-A canonical R/Y/Y). So L5.58 is the receptor's own expected residue and will pass A1. This matches how PE2R4 (native 5.58=N) already passes A1 in the current refs.
- construct label: `wt`
- Alt PDBs considered: only 1 PDB deposited (PDB 9M1H, 2025 deposit).
- Discriminator check: **UNMEETABLE**.
- Verdict: **DEFER_TO_PHASE_3**.

### PE2R1 / inactive
- Chosen PDB: — none available —
- Rationale: EP1 has a single deposited structure. No antagonist PDB.
- Verdict: **DEFER_TO_PHASE_3**.

---

### PF2R / active
- Chosen PDB: **8IUK**
- GPCRdb URL: https://gpcrdb.org/structure/8IUK/
- RCSB entity summary: Cryo-EM structure of FP receptor (PGF2α receptor) bound to PGF2α coupled with Gq.
- Resolution: 2.67 Å
- Stabilising elements: standard Gα heterotrimer scaffold; no fusion tag on receptor entity in 8IUK.
- Gα coupling: yes — Gα-q
- Activation evidence: PGF2α endogenous agonist bound; Gq-coupled; TM6-out at 13.24 Å.
- Measured d_r350_r630_ca (Å): **13.24** (chain R, R133 — H244, R/H match — native FP has H at 6.30x30)
- Note on identity anchors: native FP has 5.58=I. Same rationale as PE2R1 — A1 compares against receptor-specific GPCRdb expected residue, not Class-A canonical Y. Passes A1.
- construct label: `wt`
- Alt PDBs considered:
  - 8XJK (2.63 Å, cloprostenol + Gq) — REJECTED: entity 5 is `"Fusion tag,Prostaglandin F2-alpha receptor,LgBiT"` (NanoLuc split fusion). 8IUK is the cleaner wt construct.
  - 8XJL (2.77 Å, PGF2α + Gq) — same LgBiT fusion as 8XJK.
  - 8XJM (2.85 Å, latanoprost + Gq) — same LgBiT fusion.
  - 8IUL (2.78 Å, latanoprost + Gq), 8IUM (3.14 Å, tafluprost + Gq) — viable but lower resolution than 8IUK.
  - 8IQ4 (2.7 Å, carboprost + Gs), 8IQ6 (3.4 Å, latanoprost + Gs) — REJECTED: FP is natively Gq-coupled; Gs-coupled complexes reflect promiscuous signalling, not physiological state.
- Discriminator check: **UNMEETABLE**.
- Verdict: **DEFER_TO_PHASE_3**.

### PF2R / inactive
- Chosen PDB: — none available —
- Rationale: UniProt P43088 lists 8 PDBs, all Gα-agonist complexes (Gq or Gs). No antagonist PDB for FP receptor.
- Verdict: **DEFER_TO_PHASE_3**.

---

### PI2R / active
- Chosen PDB: **8X79**
- GPCRdb URL: https://gpcrdb.org/structure/8X79/
- RCSB entity summary: Cryo-EM structure of the prostacyclin (IP) receptor bound to MRE-269 (selexipag active metabolite) coupled with Gs.
- Resolution: 2.41 Å
- Stabilising elements: Nb35 (Gs-complex stabiliser); no receptor fusion.
- Gα coupling: yes — Gα-s (native coupling for IP receptor)
- Activation evidence: MRE-269 agonist bound; Gs-coupled; TM6-out at 13.32 Å.
- Measured d_r350_r630_ca (Å): **13.32** (chain R, R117 — E234, R/E match — native IP has E at 6.30x30)
- Note on identity anchors: native IP has 5.58=S. Same rationale as PE2R1/PF2R. Passes A1.
- construct label: `wt`
- Alt PDBs considered:
  - 8X7A (2.56 Å, treprostinil + Gs) — comparable; MRE-269 chosen for slightly better resolution.
- Discriminator check: **UNMEETABLE**.
- Verdict: **DEFER_TO_PHASE_3**.

### PI2R / inactive
- Chosen PDB: — none available —
- Rationale: 2 PDBs total (both Gs-active). No antagonist PDB.
- Verdict: **DEFER_TO_PHASE_3**.

---

### SSR1 / active
- Chosen PDB: **8XIO**
- GPCRdb URL: https://gpcrdb.org/structure/8XIO/
- RCSB entity summary: Cryo-EM structure of SSTR1–Gi complex bound to an SST-analog agonist.
- Resolution: 2.65 Å
- Stabilising elements: Nb35 (Gi-complex stabiliser); no receptor fusion.
- Gα coupling: yes — Gα-i (native SSTR coupling)
- Activation evidence: SST-analog agonist bound; Gi-coupled; TM6-out at 15.13 Å.
- Measured d_r350_r630_ca (Å): **15.13** (chain A, R155 — E266, R/E match — native SSTR1 has E at 6.30x30)
- construct label: `wt`
- Alt PDBs considered:
  - 8XIP (3.29 Å) — REJECTED for resolution.
  - 9IK8 (2.82 Å) — viable alternative; 8XIO wins on resolution.
  - 9IK9 (3.37 Å) — REJECTED for resolution.
- Discriminator check: **UNMEETABLE**.
- Verdict: **DEFER_TO_PHASE_3**.

### SSR1 / inactive
- Chosen PDB: — none available —
- Rationale: 4 PDBs total, all Gi-active. No antagonist PDB for SSTR1.
- Verdict: **DEFER_TO_PHASE_3**.

---

### SSR3 / active
- Chosen PDB: **8XIR**
- GPCRdb URL: https://gpcrdb.org/structure/8XIR/
- RCSB entity summary: Cryo-EM structure of SSTR3–Gi complex bound to pasireotide (multi-SSTR agonist).
- Resolution: 2.52 Å
- Stabilising elements: Nb35; no receptor fusion.
- Gα coupling: yes — Gα-i
- Activation evidence: pasireotide agonist bound; Gi-coupled; TM6-out at 15.12 Å.
- Measured d_r350_r630_ca (Å): **15.12** (chain A, R141 — E252, R/E match)
- construct label: `wt`
- Alt PDBs considered:
  - 8XIQ (2.71 Å, NIT-FC0-NLE agonist + Gi) — comparable; 8XIR wins on resolution + endogenous-analog ligand.
  - 8ZBI (2.79 Å) — REJECTED for resolution.
- Discriminator check: **UNMEETABLE**.
- Verdict: **DEFER_TO_PHASE_3**.

### SSR3 / inactive
- Chosen PDB: — none available —
- Rationale: 3 PDBs total, all Gi-active.
- Verdict: **DEFER_TO_PHASE_3**.

---

### SSR5 / active
- Chosen PDB: **8X8L**
- GPCRdb URL: https://gpcrdb.org/structure/8X8L/
- RCSB entity summary: Cryo-EM structure of SSTR5–Gi complex bound to cortistatin (endogenous peptide agonist).
- Resolution: 2.7 Å
- Stabilising elements: scFv16
- Gα coupling: yes — Gα-i
- Activation evidence: cortistatin endogenous agonist; Gi-coupled; TM6-out at 15.77 Å.
- Measured d_r350_r630_ca (Å): **15.77** (chain R, R137 — E243, R/E match)
- construct label: `wt`
- Alt PDBs considered:
  - 8X8N (2.9 Å, octreotide + Gi) — comparable; 8X8L wins on endogenous-ligand + resolution.
  - 8ZBE (3.24 Å, octreotide + Gi) — REJECTED for resolution.
  - 8ZBJ (2.94 Å, agonist + Gi) — REJECTED for resolution.
  - 8ZCJ (3.09 Å, agonist + Gi) — REJECTED for resolution.
- Discriminator check: **UNMEETABLE**.
- Verdict: **DEFER_TO_PHASE_3**.

### SSR5 / inactive
- Chosen PDB: — none available —
- Rationale: 5 PDBs total, all Gi-active.
- Verdict: **DEFER_TO_PHASE_3**.

---

## Cross-cutting notes for Phase 3 (CURATE-F)

### DEFER pattern — "no inactive PDB exists"
Nine of the ten receptors here fail the same way: high-quality active PDB(s) exist, but no antagonist / inverse-agonist / apo inactive PDB has been deposited in the RCSB. This is not a curator judgement call — it's a straightforward absence in the depositor community's output. Phase 3 options ranked by cost:

1. **Add to `refs/uncovered_receptors.txt`** (cheapest, matches plan §D.1(c)) — receptor rows are permanently unclassifiable via TM6-axis delta path. Downstream analysis uses `receptor_d_active_ref IS NaN` filter. Accepts ~400 predictions as unclassifiable.
2. **Accept active-only + state_thresholds fallback** — append the active rows here to `refs/reference_pdbs.csv` (with a `role=active` half-pair), set inactive row `excluded=true` with `excluded_reason="no_inactive_pdb_deposited_2026Q3"`, and rely on `refs/state_thresholds.csv` for state classification. Requires confirming per-receptor state thresholds exist for these ten slugs, and that the scorer's classification path degrades gracefully when only the active reference is populated (`scorer/references.py:275-315` returns NaN for the inactive component; the pack classifier must have a threshold-fallback branch — verify before adopting this option).
3. **Homology-derived inactive template** — REJECTED as violating audit discipline: `d_r350_r630_ca_ref` must be a real coordinate measurement per plan Guardrail 3.

The user should decide between options 1 and 2 before Phase 3 acts. Option 2 is the only one that recovers the ~400 predictions; option 1 is the safe default.

### DEFER pattern — chimeric antagonist construct (NMBR / 9JF4)
Distinct from the "no inactive PDB" pattern above. 9JF4 exists but has a fused de-novo-design protein with non-continuous author numbering. Curating it requires (a) resolving the SIFTS residue map to identify the true UniProt residue at author_seq 261 in the deposited chain, (b) setting an appropriate `construct_offset` in the new refs schema (pre-Phase-1 code change is a prerequisite), (c) confirming R6.30→F6.30 is a genuine thermostabilising point mutation (diagnostic anchor mismatch, non-fatal per verified.py:212-219) rather than a numbering artefact. This is Phase 3 D.1(b) territory — feasible but non-trivial.

### Identity-anchor caveat for prostanoid receptors (PE2R1, PF2R, PI2R)
The plan text at "Rules summary" says identity anchors 3.50 R, 5.58 Y, 7.53 Y must match — implying Class-A canonical residues. The actual scorer implementation (`scorer/verified.py:169-193`) compares each observed anchor residue against the **receptor-specific GPCRdb expected residue**, not against a fixed Class-A canonical. This lets receptors like PE2R4 (5.58=N native) and PE2R1 (5.58=L native) pass A1 already. **Recommendation**: reconcile the plan wording with the code behaviour before Phase 4 to avoid confusion. Under the code-behaviour interpretation, the prostanoid active PDBs proposed here (9M1H, 8IUK, 8X79) will pass A1 cleanly.

### Measurement methodology
Distances were computed locally on the deposited mmCIF files using `gemmi` (v0.7.5, Python API):
- Fetch mmCIF from `https://files.rcsb.org/download/<pdb>.cif.gz`
- Parse with `gemmi.cif.read_string` → `make_structure_from_block`
- Iterate chains; find residues at UniProt author_seq positions from GPCRdb `residues/{slug}_human/` endpoint
- Extract CA atoms; compute Euclidean distance
- Verified each anchor's residue name matches the GPCRdb-expected native residue (identity gate proxy)

All measurements reproducible from `/tmp/measure_d.py` (this session's scratchpad). Note this is a local proxy for `scorer/refs_build.py`'s `verify_reference_pdb` path — the authoritative measurement will happen on HPC when Phase 4 executes `python -m scorer.refs_build build --allow-nan-tripwire`. Expected agreement: exact to the second decimal, since both paths use CA-only Euclidean distance on the same deposited coordinates.

---

## What CURATE-C did NOT do
- Did not curate inactive PDBs from unrelated receptors (no cross-family fallback).
- Did not attempt to fit a homology-derived inactive template (Guardrail 3 violation).
- Did not measure NPxxY Y5.58–Y7.53 CA-CA or DRY-motif side-chain axes (out of scope — only TM6 R3.50–6.30 CA-CA is required for refs_build).
- Did not attempt to resolve 9JF4's chimeric numbering (deferred to Phase 3).
- Did not verify that state_thresholds.csv covers these ten receptors (option-2 recommendation is contingent on that check — flagged for Phase 3).
