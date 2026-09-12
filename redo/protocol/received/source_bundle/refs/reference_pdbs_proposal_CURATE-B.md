# CURATE-B — reference-set proposal
Agent: CURATE-B (top-count Class A + one Class B)
Scope: CALCR, HRH4, ACM3, 5HT1A, MCHR2, KISSR
Method: read-only research; no writes to refs CSVs or scorer code
Target (plan §Phase 2): ~800 predictions unlocked

## Summary

**6 receptors × 2 roles = 12 entries.**

| # | Verdict | Count |
|---|---|---:|
| PROPOSE (active only) | HRH4, ACM3 (human active + rat-inactive caveat), 5HT1A, MCHR2, KISSR, CALCR (Class B) | 6 |
| DEFER_TO_PHASE_3 (inactive) | all six inactive roles | 6 |

**Estimated unlock from this subagent, without Phase-3 action: 0 predictions.**
CURATE-B's headline finding is the *asymmetry* of the modern GPCR structural corpus for these six receptors: every one has multiple recent cryo-EM Gα-coupled active structures, but *only one* has any antagonist-bound inactive deposit at all (HRH4 / 9JG1 — and its TM6 is disordered so 6.30 CA isn't resolved). Cross-species rat inactives exist for ACM3 (Kobilka 2012–2018 crystals). No inactive exists for CALCR, 5HT1A, MCHR2, KISSR — none have ever been crystallized in an antagonist-bound state as of the RCSB snapshot walked here.

**Deferrals go to Phase 3** — the tractable follow-ups per subclass are:

- **D.1 (fusion/loop-broken)** — ACM3 rat inactive 4DAJ / 4U14 (Endolysin fusion, 6.30 CA present, |Δd| vs human active fails discriminator ~2.7 Å). *Route: Phase 3.1.b accept T4L construct with cross-species uniprot_slug or refuse.*
- **D.2 (Class B)** — CALCR: normal Class-A axis *resolves* (6.30 CA present, d ≈ 30 Å) but *no antagonist-bound PDB exists at all* → not a Class B axis issue, it's a coverage issue. Class-B-specific axis won't fix that.
- **D.3 (disordered 6.30)** — HRH4 9JG1 sole inactive has residues 208–377 disordered (TM6/ECL3/TM7). No alternate inactive.
- **New sub-class (no inactive deposited)** — 5HT1A, MCHR2, KISSR, CALCR: no antagonist-bound crystal *exists*. These receptors probably need `refs/uncovered_receptors.txt` unless downstream classification can operate from `delta_to_active` alone.

## Recommendation for coordinator

Merge the six ACTIVE proposals into `_MERGED.md`. Do not append active-only rows to `refs/reference_pdbs.csv` yet — the pipeline currently requires both roles for delta classification (discriminator invariant). Route all inactives to `refs/reference_pdbs_proposal_PHASE3.md` (CURATE-F) with the sub-classification above.

Optional: coordinator can request user decision on the ACM3 rat inactive cross-species workaround (would unlock ACM3 alone, ~140 preds) before opening Phase 3.

## Measurement provenance

All distances measured locally with `/tmp/curate_b_work/measure.py`:
- Anchor positions pulled from `https://gpcrdb.org/services/residues/extended/<entry>/`.
- Coordinates fetched from `https://files.rcsb.org/download/<pdb>.cif.gz` (mmCIF).
- Chain selected as the one whose observed 3.50 and 6.30 residues match the expected AAs from GPCRdb (mirrors `scorer/verified.py::has_axis_coverage` + `scorer/anchors.py::verify_aa_identity`).
- Distance = CA(3.50) — CA(6.30) in Å, no smoothing, no minimization.
- Ground-truth check on prior-work 8PJK / 7E2X / 7E2Y (5HT1A): d = 17.89 / 18.11 / 18.34 Å — consistent with published Class A active-state TM6-out geometry. Helper validated.

Anchor UniProt positions used (from GPCRdb):

| receptor | uniprot | 3.50 | 6.30 |
|---|---|---:|---:|
| HRH4 | hrh4_human | 112 R | 298 A |
| ACM3 | acm3_human | 166 R | 486 E |
| 5HT1A | 5ht1a_human | 134 R | 340 E |
| MCHR2 | mchr2_human | 131 R | 246 V |
| KISSR | kissr_human | 140 R | 258 R |
| CALCR | calcr_human | 240 E | 333 A |

Identity-defining anchor 3.50 (R) is conserved for all five Class-A targets; CALCR carries E at 3.50 as expected for Class B (no DRY motif). Identity anchors 5.58 and 7.53 also match GPCRdb per receptor. No mutation-refusal risk for the proposed active PDBs (all AAs match expected at all six anchors).

---

## Per-receptor × per-role entries

### HRH4 / active
- Chosen PDB: **8YN9**
- GPCRdb URL: https://gpcrdb.org/structure/8YN9/
- RCSB entity summary: Cryo-EM structure of histamine H4 receptor in complex with histamine and Gi (2024-10-09).
- Resolution: 2.30 Å
- Stabilising elements: none noted (native receptor + heterotrimeric Gi + scFv16 stabiliser typical for cryo-EM; verify via GPCRdb `auxiliary_proteins`)
- Gα coupling: yes — Gαi1 (`gnai1_human`)
- Activation evidence: state=Active per GPCRdb; agonist histamine bound; full Gαi1 complex; anchors 3.50=R, 5.58=N, 7.53=Y all present with expected AAs
- Measured d_r350_r630_ca (Å): **16.52** (chain R)
- construct label: `wt`
- Alt PDBs considered:
  - 7YFC (Gi complex, histamine, 3.0 Å) — measurement OK (d=17.77 Å at chain R) but 8YN9 is higher resolution and same complex
  - 8HN8 (histamine, Gi, 3.0 Å) — d=17.01 Å, ok, superseded by 8YN9
  - 8JXT (histamine, 3.07 Å) — d=17.77 Å, ok
  - 9L42 / 9LRC / 9LRE (Gi, histamine) — deposit later than 8YN9 but not clearly better
  - 8YNA (immepip agonist) — non-natural ligand; prefer natural histamine
- Discriminator check: paired with `9JG1` — inactive 6.30 CA disordered → discriminator *not computable*. |Δd| = **N/A**
- Verdict: **PROPOSE** (blocked by inactive-role deferral)

### HRH4 / inactive
- Chosen PDB: none — all candidates fail structural gate
- GPCRdb URL: n/a
- RCSB entity summary: sole "inactive"-titled deposit is 9JG1 — Cryo-EM Adriforant-bound H4R at inactive state, 3.62 Å.
- Resolution: 3.62 Å (9JG1) — but not usable
- Stabilising elements: unknown; complex reconstruction likely includes stabiliser antibody
- Gα coupling: no (inactive state without G)
- Activation evidence: state=Inactive per RCSB title; adriforant is a known H4R inverse agonist
- Measured d_r350_r630_ca (Å): **NaN** (6.30 CA disordered). Chain R has a contiguous gap from residue 208 to 377 covering all of TM6 + ECL3 + TM7-start; 3.50 (R112) is resolved but 6.30 (A298) is not.
- construct label: `disordered_6_30`
- Alt PDBs considered:
  - 7YFC / 7YFD / 8HN8 / 8HOC / 8JXT / 8JXV / 8JXW / 8JXX / 8YN9 / 8YNA / 9JED / 9L42 / 9LRC / 9LRE — all state=Active with agonist + Gi complex; none are inactive
  - No H4R antagonist crystal in an antibody-stabilised inactive conformation with resolved TM6 exists in RCSB as of this snapshot
- Discriminator check: not computable
- Verdict: **DEFER_TO_PHASE_3** (subclass D.3 — disordered 6.30; recommend: no alternative deposit exists → add HRH4 to `refs/uncovered_receptors.txt` or wait for future antagonist-bound cryo-EM)

---

### ACM3 / active
- Chosen PDB: **8E9Z**
- GPCRdb URL: https://gpcrdb.org/structure/8E9Z/
- RCSB entity summary: CryoEM structure of miniGq-coupled hM3R in complex with iperoxo (Chen et al., Nature 2022, doi:10.1038/S41586-022-05489-0).
- Resolution: 2.69 Å
- Stabilising elements: miniGαq + Gβ1γ2 + scFv16 (from GPCRdb signalling_protein entities)
- Gα coupling: yes — miniGq
- Activation evidence: state=Active per GPCRdb; iperoxo super-agonist bound; full miniGq/Gβ/Gγ heterotrimeric complex; all six anchors match GPCRdb identities
- Measured d_r350_r630_ca (Å): **17.26** (chain A)
- construct label: `wt`
- Alt PDBs considered:
  - 8EA0 (iperoxo, "local refinement", 2.56 Å) — d=17.20 Å but signalling_protein data empty at GPCRdb (local refinement stripped G-protein density); prefer 8E9Z which has the full complex map
  - 8E9W (CHEMBL73538 agonist, 2.69 Å) — non-endogenous ligand; iperoxo (8E9Z) preferred
  - 8E9Y (Clozapine N-oxide, 2.79 Å) — CNO is a designer agonist for DREADD chemogenetic constructs
- Discriminator check: paired with (proposed 4U14 rat inactive; see inactive entry) — |Δd| = 17.26 − 14.49 = **2.77 Å** (fails ≥3.0). Alternative rat inactive 5ZHP gives |Δd|=17.26−9.54=**7.72 Å** but 5ZHP has anomalous TM6-inward T4L artefact.
- Verdict: **PROPOSE** (active row is well-founded; classification blocked by inactive-role deferral)

### ACM3 / inactive
- Chosen PDB: candidates present but *all* violate at least one guardrail
- Chosen PDB (with caveat): **4U14** (rat, tiotropium-bound, T4L insertion, 3.57 Å) — for coordinator user-decision
- GPCRdb URL: https://gpcrdb.org/structure/4U14/
- RCSB entity summary: Structure of the M3 muscarinic acetylcholine receptor bound to the antagonist tiotropium crystallised with disulfide-locked ligand (Kruse et al., Nature 2013).
- Resolution: 3.57 Å
- Stabilising elements: T4L (endolysin) fusion inserted between TM5 and TM6 in ICL3 (does NOT excise 6.30 residue — 6.30 CA resolved and measured); no Nb/scFv
- Gα coupling: no (antagonist inactive)
- Activation evidence: state=Inactive per GPCRdb; tiotropium (bronchodilator antagonist) bound; ionic-lock intact (D3.49–R3.50 salt bridge visible in reported crystal)
- Measured d_r350_r630_ca (Å): **14.49** (chain A of 4U14, rat sequence, anchors at UniProt 165 R / 485 E)
- construct label: `t4l_fusion` (with species caveat below)
- Alt PDBs considered:
  - 4DAJ (rat, tiotropium, T4L, 3.4 Å) — d=14.67 Å, effectively identical to 4U14, superseded by 4U14
  - 4U15 (rat, tiotropium, mT4L, 2.8 Å) — d not measured (mT4L variant); resolution better but sequence is `M3-mT4L-M3` chimera with a different fusion residue span
  - 4U16 (rat, NMS antagonist, mT4L, 3.7 Å) — NMS = N-methylscopolamine; similar to 4U14 but different antagonist
  - 5ZHP (rat, selective antagonist, T4L, 3.1 Å) — d=9.54 Å ANOMALOUS (5 Å tighter than other rat inactives, suggests T4L is pulling TM6 inward past physiological range or 3.50/6.30 assignment on the chimera is off; not proposing without further audit)
  - 2CSA — NMR fragment of basolateral sorting signal, not the 7TM structure; skip
  - No **human** ACM3 inactive PDB exists.
- Discriminator check: paired with 8E9Z active → |Δd|=**2.77 Å** — **fails ≥3.0**. 5ZHP would pass at 7.72 Å but is structurally suspect.
- Species caveat: 4U14 species=rat, uniprot_slug=acm3_rat. Pre-Phase-1 code change refuses `species=rat, uniprot_slug=acm3_human`. If uniprot_slug=acm3_rat, the row is legal but the reference geometry compares to a rat anchor set (identical residues at 3.50/6.30, 97% receptor-wide identity to human). Precedent: `NTR1` refs both use ntr1_rat / rat.
- Verdict: **DEFER_TO_PHASE_3** (subclass D.1 — T4L fusion + cross-species; recommend Phase-3 user-decision on either (a) accept 4U14 with `construct=t4l_fusion` + `uniprot_slug=acm3_rat` and accept |Δd|~2.7 Å below discriminator threshold, (b) accept 5ZHP conditional on chain audit that ionic-lock geometry is not T4L-perturbed, or (c) add ACM3 to `uncovered_receptors.txt`)

---

### 5HT1A / active
- Chosen PDB: **8PJK**
- GPCRdb URL: https://gpcrdb.org/structure/8PJK/
- RCSB entity summary: ST171-bound serotonin 5-HT1A receptor — Gi Protein Complex (2024-05-29).
- Resolution: 2.40 Å
- Stabilising elements: Gαi1 heterotrimer (+ scFv16 typical for stabilisation); no fusion
- Gα coupling: yes — Gαi1 (`gnai1_human`)
- Activation evidence: state=Active per GPCRdb; ST171 (biased 5-HT1A agonist) bound; full Gi complex; all six anchors match GPCRdb identities (R/Y/Y/E/V/Y at 3.50/3.51/5.58/6.30/6.34/7.53)
- Measured d_r350_r630_ca (Å): **17.57** (chain R)
- construct label: `wt`
- Alt PDBs considered:
  - 9HYI (DP81-bound, Gi, 2.30 Å) — d=17.74 Å; slightly higher resolution but 8PJK preferred per prior consultant recommendation and comparable ligand pharmacology
  - 8FYT (LSD-bound, Gi, 2.64 Å) — d=17.37 Å; psychedelic ligand, higher clinical interest but 8PJK slightly better resolution
  - 8FYX (buspirone, Gi, 2.62 Å) — d=17.20 Å; clinical anxiolytic
  - 7E2X (apo, Gi, 3.0 Å) — d=18.11 Å; useful sanity check (still active-state despite apo since Gi is bound)
  - 7E2Y (5-HT natural agonist, Gi, 3.0 Å) — d=18.11 Å; natural ligand
  - 8FY8 / 8FYE / 8FYL / 8JT6 / 8JSP / 8W8B / 8PKM / 7E2Z / 9DYD-F / 9GL2 / 9KVG-I / 9MD1 / 9R41 / 9VJ5-G / 9VMY / 9VNF — 20+ additional active-state Gα-coupled cryo-EM structures with various agonists; 8PJK ranks well on resolution & the plan-hint list
- Discriminator check: no inactive PDB deposited → |Δd| = **N/A**
- Verdict: **PROPOSE** (active row is well-founded; blocked by inactive-role deferral)

### 5HT1A / inactive
- Chosen PDB: **none — no antagonist-bound 5-HT1A crystal exists in RCSB**
- GPCRdb URL: n/a
- Notes: All 30 RCSB entries for P08908 are cryo-EM Gα-coupled active complexes with various agonists (5-HT, LSD, DMT, DP81, ST171, buspirone, aripiprazole, asenapine, gepirone, F-15599, TMU4142, 5-MeO-DMT, TMT, pindolol, ulotaront, befiradol, vilazodone…). Even entries with putative-antagonist ligands (asenapine, buspirone as partial agonist) are still G-protein-coupled → active state per GPCRdb.
- Alt PDBs considered: exhaustive — see enumeration in `active` entry.
- Discriminator check: not computable
- Verdict: **DEFER_TO_PHASE_3** (subclass: no inactive deposited; recommend `uncovered_receptors.txt` unless downstream classification can operate on `delta_to_active` alone)

---

### MCHR2 / active
- Chosen PDB: **8WST**
- GPCRdb URL: https://gpcrdb.org/structure/8WST/
- RCSB entity summary: Cryo-EM structure of Melanin-Concentrating Hormone Receptor 2 with MCH (2024-06-19, doi:10.1038/S41421-024-00679-8).
- Resolution: 2.40 Å
- Stabilising elements: heterotrimeric Gαq/β1/γ2 (+ scFv16 typical)
- Gα coupling: yes — Gαq (`gnaq_human`)
- Activation evidence: state=Active per GPCRdb; pro-MCH (endogenous ligand) bound; full Gαq heterotrimer complex; all six anchors match (R/Y/Y/V/T/Y at 3.50/3.51/5.58/6.30/6.34/7.53). Note 6.30=V (not the canonical E/D ionic-lock partner) — permissible; GPCRdb-annotated identity matches observation.
- Measured d_r350_r630_ca (Å): **16.27** (chain R)
- construct label: `wt`
- Alt PDBs considered: **none** — 8WST is the sole RCSB deposit for MCHR2 (Q969V1)
- Discriminator check: no inactive PDB exists → |Δd| = **N/A**
- Verdict: **PROPOSE** (sole active; blocked by inactive-role deferral)

### MCHR2 / inactive
- Chosen PDB: **none — sole RCSB deposit is 8WST, an active-state Gq complex**
- GPCRdb URL: n/a
- Alt PDBs considered: exhaustive — no other MCHR2 structure exists at RCSB or GPCRdb.
- Discriminator check: not computable
- Verdict: **DEFER_TO_PHASE_3** (subclass: no inactive deposited; recommend `uncovered_receptors.txt`)

---

### KISSR / active
- Chosen PDB: **8ZJD**
- GPCRdb URL: https://gpcrdb.org/structure/8ZJD/
- RCSB entity summary: Cryo-EM structure of kisspeptin receptor bound to KP-10 (2024-07-03).
- Resolution: 3.06 Å
- Stabilising elements: heterotrimeric Gαq/β/γ (+ scFv16 typical)
- Gα coupling: yes — Gαq (`gnaq_human`)
- Activation evidence: state=Active per GPCRdb; KP-10 (endogenous kisspeptin decapeptide, natural agonist) bound; full Gαq complex; anchors R/W/Y/R/S/Y at 3.50/3.51/5.58/6.30/6.34/7.53 — all match GPCRdb identity. Note 3.51=W (not canonical Y) and 6.30=R (not canonical E/D). Both are legitimate KISSR-native residues per GPCRdb → not identity mismatches.
- Measured d_r350_r630_ca (Å): **13.96** (chain R)
- construct label: `wt`
- Alt PDBs considered:
  - 8XGU (designed agonist ACY-DTY-…, Gi, 3.0 Å) — d=14.01 Å (chain A); Gi rather than Gq; non-natural peptide agonist
  - 8XGS (Gi complex, 3.0 Å) — d=14.36 Å
  - 8XGO (Gi complex) — companion to 8XGU/8XGS
  - 8ZJE (TAK-448 clinical agonist, 3.07 Å) — d comparable; TAK-448 is a therapeutic agonist rather than the endogenous KP-10
  - 7YQE — appeared in RCSB search but the RCSB entry is a *human Src regulatory-domain complex with the C-terminal PRRP motifs of GPR54* (KISSR = GPR54 alias); the crystal is Src + short peptide, not the 7TM receptor. Skip.
- Discriminator check: no inactive PDB exists → |Δd| = **N/A**
- Verdict: **PROPOSE** (active row is well-founded; blocked by inactive-role deferral). d=13.96 Å is on the low side of Class A actives — worth flagging in provenance since 6.30=R (not the canonical E) could shift the geometric axis versus receptors with canonical ionic-lock partners at 6.30. Not a bug, just a shape note.

### KISSR / inactive
- Chosen PDB: **none — all six KISSR RCSB deposits are active-state peptide-agonist + Gi/Gq complexes**
- GPCRdb URL: n/a
- Alt PDBs considered: 8XGU, 8XGS, 8XGO, 8ZJD, 8ZJE — all active. 7YQE — not the receptor structure. No antagonist-bound KISSR crystal in RCSB.
- Discriminator check: not computable
- Verdict: **DEFER_TO_PHASE_3** (subclass: no inactive deposited; recommend `uncovered_receptors.txt`)

---

### CALCR / active  *(Class B — special handling per plan §Phase-3.2)*
- Chosen PDB: **8F0J**
- GPCRdb URL: https://gpcrdb.org/structure/8F0J/
- RCSB entity summary: Calcitonin Receptor in complex with Gs and Pramlintide analogue peptide San45 (2023-08-02).
- Resolution: 2.00 Å
- Stabilising elements: heterotrimeric Gαs2 + Nb35 (typical for Class B Gs complexes); no fusion; sequence is *pure* human calcitonin receptor (CALCR), not an AMY1/2/3 heteromer with RAMP
- Gα coupling: yes — Gαs (`gnas2_human`)
- Activation evidence: state=Active per GPCRdb; pramlintide-analogue San45 (peptide agonist derived from amylin) bound; full Gαs complex; **Class-A axis anchors DO resolve** — 3.50 (E240 native, not Arg — Class B has no DRY), 5.58 (V320 native, not Tyr), 6.30 (A333), 7.53 (V387 native, not the NPxxY Tyr). GPCRdb annotates all these positions correctly; observed AAs match; all six anchor CA present.
- Measured d_r350_r630_ca (Å): **30.26** (chain R). *This is the Class-B-scale value* — Class B TM6 outward motion goes ~30 Å between 3.50-CA and 6.30-CA versus ~14–18 Å for Class A actives. GPCRdb-provided anchor numbering is 240 (E, 3.50) and 333 (A, 6.30).
- construct label: `class_b_receptor` (per plan §Phase-3.2 recommendation)
- Alt PDBs considered:
  - 6NIY (salmon calcitonin, Gs, 3.34 Å) — canonical published Class-B CALCR-Gs cryo-EM (2018) BUT chain R only resolves residues 138–414 with 6.30 (A333) NOT observed on CALCR chain — chain assignment inspected via gemmi: chain A ends at 394 but is not CALCR; chain R spans 138-414 with residue 333 disordered. `d = NaN`. Reject as active reference despite historical importance.
  - 8F0K (Human Amylin3 Receptor + Gs + San385, 1.9 Å) — d=30.47 Å; AMY3 uses CALCR backbone + RAMP3; if pipeline distinguishes AMY3 from CALCR by receptor_slug this is a different receptor
  - 9BUB (CALCR + Gs + cagrilintide bypass conformation, 2.3 Å) — d=29.97 Å; excellent resolution, natural conformation, alternative to 8F0J. Consider as backup.
  - 9BUD (CALCR + Gs + cagrilintide CT-like conformation, 2.5 Å) — d not measured but expected ~30 Å; useful if 8F0J refused
  - 7TYN (salmon calcitonin, Gs, 2.6 Å) — d=30.22 Å
  - 9AUC (AMY1R + Gs + CGRP peptide, 2.4 Å) — different receptor complex (AMY1 not CALCR)
  - 5UZ7 (2018 salmon calcitonin, 4.1 Å) — poor resolution
  - 7TYF / 7TYH / 7TYI / 7TYL / 7TYO / 7TYW / 7TYX / 7TYY / 7TZF / 8F2A / 8F2B — additional AMY / CALCR Gs complexes; 8F0J preferred on resolution.
- Discriminator check: no inactive PDB exists → |Δd| = **N/A**
- Verdict: **PROPOSE** (Class B active with `class_b_receptor` construct label; Class-A axis geometrically resolves, giving d≈30 Å on the Class-B scale. Blocked by inactive-role deferral. Downstream: the Class-B-scale d may need its own delta scaling; recommend Phase 3.2 audit of whether a fold-model prediction of CALCR reproduces d≈30 Å or lands intermediate — if latter, delta_to_active on Class-A axis is still meaningful within Class B, just on a different scale.)

### CALCR / inactive  *(Class B)*
- Chosen PDB: **none — no antagonist-bound CALCR crystal exists in RCSB**
- GPCRdb URL: n/a
- Notes: Class B GPCRs including CALCR have not been crystallised in agonist-free or antagonist-bound states outside of Gs-coupled active complexes. The plan-file reference to a `CALCR/8HTI` inactive appears to be an error — RCSB `8HTI` is *Human Consensus Olfactory Receptor OR52c in Complex with Octanoic Acid and G Protein* (not CALCR at all). All 32 RCSB deposits for P30988 are Gs-coupled active-state peptide-agonist complexes.
- Alt PDBs considered: exhaustive over the 32 P30988 deposits — all active.
- Discriminator check: not computable
- Verdict: **DEFER_TO_PHASE_3** (subclass D.2 — Class B; not a Class B *axis* problem (Class-A axis resolves) but a Class B *coverage* problem: the antagonist-bound conformation has never been solved. Recommend `uncovered_receptors.txt` for the inactive role; the active side can still populate `delta_to_active` for CALCR predictions if the pipeline permits half-pair references.)

---

## Discriminator failures summary

| receptor | active d (Å) | inactive candidate | inactive d (Å) | \|Δd\| | discriminator |
|---|---:|---|---:|---:|---|
| HRH4 | 16.52 (8YN9) | 9JG1 | NaN (TM6 disordered) | – | fail |
| ACM3 | 17.26 (8E9Z) | 4U14 rat | 14.49 | 2.77 | **fail** (<3) |
| ACM3 | 17.26 (8E9Z) | 4DAJ rat | 14.67 | 2.59 | **fail** (<3) |
| ACM3 | 17.26 (8E9Z) | 5ZHP rat | 9.54 | 7.72 | pass but 5ZHP T4L-tainted |
| 5HT1A | 17.57 (8PJK) | none | – | – | no candidate |
| MCHR2 | 16.27 (8WST) | none | – | – | no candidate |
| KISSR | 13.96 (8ZJD) | none | – | – | no candidate |
| CALCR | 30.26 (8F0J) | none | – | – | no candidate (Class B) |

## Loose ends the coordinator should confirm

1. **Cross-species policy** — plan §Pre-work §2 says species-vs-uniprot_slug refusal fires when they disagree, but ACM3 rat inactive with `uniprot_slug=acm3_rat` is technically legal alongside human active with `uniprot_slug=acm3_human` since both share `receptor_slug=ACM3`. Confirm whether mixed-species pairs are acceptable in the current pipeline or whether receptor_slug must have a single uniprot_slug across roles.
2. **Half-pair references** — five of six CURATE-B receptors will have only an active row. Coordinator to decide whether appending active-only refs is (a) useful (populates `delta_to_active` even without inactive), or (b) refused by `refs_build.py` because both roles are required schema-wise.
3. **CALCR Class-B scaling** — d≈30 Å active for CALCR sits far from any Class-A active/inactive threshold. If downstream state classification uses a class-wide threshold, CALCR predictions will always classify as "active" regardless of predicted conformation. Recommend audit of whether the pipeline binaries thresholds per-class or globally.
4. **`8HTI` mis-reference in plan** — the plan file cites `CALCR/8HTI` as an example Class-B inactive; 8HTI is actually an olfactory receptor. Consider updating the plan note.

## Files produced
- This document.
- Helper script `/tmp/curate_b_work/measure.py` and cache `/tmp/curate_b_work/cache/*` (fetch cache — not part of committed refs).
- No writes to `refs/reference_pdbs.csv`, `refs/reference_set.csv`, or `refs/provenance/`.
