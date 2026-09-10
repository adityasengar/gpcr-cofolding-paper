# §2.4 — Post-cutoff inactive-Nb scoping (v3, reverted 2026-09-10)

> **STATUS 2026-09-10: CLOSED — test not dispatched for this manuscript.** The distilled record + reusable filter rule lives at `BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md` (that is the canonical reference for future readers). This scoping doc is retained as an audit trail of the full search process, including the v1 → v2 → v3 revision path and the mechanism-check reasoning that surfaced the fiducial-Nb pattern on three of four candidates. §6.5's Discussion paragraph is LOCKED per the closeout dispatch and reports the active/inactive asymmetry as demonstrated only in the active direction, with the memorization confound stated rather than resolved.

**Deliverable (as it stood before closure)**: a candidate + rough cost. **No dispatch.**

**Revision history**:
- **v1 (this file, first draft)**: proposed 9PXU (MOR + Nanobody6) as primary.
- **v2 (superseded)**: swapped 9PXU → 9HB3 (V2R + "Mambaquaretin1") on novelty-of-family + novelty-of-Nb-framework grounds. **Retracted.** The 141-aa VHH-shaped chain I promoted was NOT Mambaquaretin1 (a 57-residue Kunitz-fold peptide from mamba venom is what "Mambaquaretin1" actually is); it was the anti-BRIL-Fab fiducial Nb from a standardised cryo-EM scaffolding toolkit that has become field-default for GPCR structures 2023–2025. The RCSB metadata filter I used tagged the fiducial-Nb as "the Nb" without a mechanism check. Same error hit the three backups (9EKH/9EE5 DP1 and 9EHS AA3R) — all use the same anti-BRIL-Fab-Nb fiducial construct; the state determinants there are their small-molecule antagonists (ONO-series / LUF7602), not the Nb chain. All four candidates and both backups **disqualified** as post-cutoff-inactive-Nb-test targets.
- **v3 (this pass)**: 9PXU restored as primary with the cousin-Nb + same-opioid-family caveat carried explicitly, not as a footnote. Filter rule for future candidate searches added below (§"Fiducial-Nb filter rule going forward").

## Fiducial-Nb filter rule going forward

An `Nb` chain co-occurring with `BRIL` OR `Fab` in a deposition's polymer-entity list is **presumptively a scaffolding aid, not a state-directing partner**, until literature/mechanism verification. Modern cryo-EM GPCR practice standardised on the anti-BRIL-Fab-Nb fiducial toolkit (Manglik/Kobilka lineage variants) around 2022–2023 to add particle-alignment mass; the "Nb" in these structures is not bound to the receptor's functional intracellular surface and has nothing to do with its conformational state. Any future post-cutoff-inactive-Nb search must:

1. **Screen for co-occurring `BRIL` or `Fab` chains** in the RCSB polymer-entity metadata; disqualify by default.
2. **Read the primary-citation abstract** or figure caption to confirm the Nb's mechanistic role.
3. **Look at the CIF** if step 2 is ambiguous — a state-directing Nb docks on the intracellular half of the receptor and binds either 3.50 / TM6 kink or the α5-like helix bundle; a fiducial Nb sits away from the receptor's functional surface, binding the Fab or BRIL only.

Named as C-D-13 (add on next commit if we want it as a persistent flag; currently in-body here).

## Primary candidate — PDB **9PXU** (MOR + Nanobody6)

- **Title**: Inactive-state naloxone-mu opioid receptor nanobody6 complex.
- **Deposited**: 2025-08-06. **26 months post-Boltz-2 cutoff.**
- **Receptor**: Mu opioid receptor (OPRM1, UniProt `P35372`, human). Class A GPCR.
- **Nanobody**: `Nanobody6`, 131 aa, synthetic construct. State-directing per primary citation (Nature 2025, DOI `10.1038/s41586-025-09677-6`, "Structural snapshots capture nucleotide release at the mu-opioid receptor"). Nb docks at the intracellular half; naloxone is the orthosteric antagonist ligand.
- **Method**: cryo-EM.
- **No BRIL/Fab fiducial** (per polymer-entity metadata: only the primary Nb + an anti-fab Nb + Nab-fab HL chains — the last three are cryo-EM chaperones for the primary Nb, not the receptor. This distinguishes 9PXU from the disqualified group's construct pattern.).

### Caveats carried explicitly (main text, not footnotes)

The 9PXU test is a **same-paralog-family + cousin-Nb transfer test**, not a fully novel one. State that plainly:

1. **Cousin-Nb transfer within Nb framework** — 9PXU's Nanobody6 (131 aa, sha `5cce1ef6…`) is **not sequence-identical** to `refs/nanobody_sequences.fasta:Nb6_6VI4` (133 aa, sha `a7b413fe…`) but shares **87 % framework overlap** on the tag-stripped 121-residue core. CDR1 (`IFRLYDMGW`) and CDR2 (`ITSGGSTKY`) are **identical** between the two; CDR3 is distinct. Both are likely from the same immunization library / shared framework backbone. A model that memorised 6VI4-Nb6 → inactive during training may recognise the shared CDR1 + CDR2 + framework signature on 9PXU-Nanobody6, potentially recapitulating a "seen Nb-fold → inactive" signal without integrating the novel CDR3 as the state cue.
2. **Same paralog family** — MOR (OPRM1) is the mu opioid receptor. D2's OPRK is the kappa opioid receptor. Both are in the `opioid` paralog cluster (see `experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`). Testing MOR × Nb-inactive after D2 already tested OPRK × Nb-inactive is same-family transfer, not novel-family test. A model with a family-level inactive prior for opioid receptors could reproduce inactive-state MOR on 9PXU-Nb6-input via family-level generalisation rather than integrating the specific Nb-input signal.

**Consequence for the manuscript claim**: if 9PXU test returns "inactive-Nb-Nb6-9PXU steers inactive on ≥ 3/4 backbones" on MOR, the finding is **cousin-Nb-within-opioid-family transfer succeeds** — a strictly weaker claim than "genuinely novel-family + novel-Nb steering succeeds". Discussion sentence must state this explicitly. The C-D-12 confound is **partially** dischargeable (novel-CDR3 test succeeds where prior anchors' CDR3 was fully training-visible) but **not fully** (cousin-Nb + same-family paths still open).

A fully-novel test (novel receptor family + novel Nb framework) is not currently available among the 204 hits screened. See §"What a fully-novel test would require".

## What a fully-novel test would require

- A post-Boltz-2 (≥ 2023-06-01) deposited GPCR × inactive-Nb structure where:
  - Receptor is in a paralog family NOT covered by D2 (i.e., not adrenergic, muscarinic, angiotensin, opioid) AND ideally not in Block C's landed 37 either (rules out AA2AR/AT1R/ADRB2/DRD2/etc. as previously trained-visible targets).
  - The Nb chain is **state-directing** (docks at the receptor's intracellular functional surface, not on a fiducial BRIL/Fab).
  - The Nb sequence's CDR1/CDR2/framework does not overlap the four D2 Nb-anchor sequences (`Nb60 / Nb6_6VI4 / Nb9-8 / Nb.AT110i1_le`) beyond generic humanised-VHH backbone signal.

The 204-hit deep-dive from this pass surfaced zero such candidate. Every apparent post-cutoff inactive-Nb hit that passed keyword filtering was either (a) a fiducial-Nb + BRIL + Fab construct with a small-molecule state determinant (9HB3, 9EKH, 9EE5, 9EHS), (b) a same-Nb-as-D2 case (9W3F Nb60 on β2AR), (c) an orphan-receptor + hinge-Nb (9YFU, 9LMO, 9JFU), (d) a same-receptor-as-D2 + cousin-Nb case (8TH4 AGTR1 + AT118-L).

Alternative avenues, out of scope for autonomous adoption but nameable:
- **Wider search filter**: search on `nanobody AND (intracellular OR ICL2 OR ICL3)` AND NOT `BRIL AND Fab` — more targeted keyword pattern. May surface state-directing Nb structures the current filter missed.
- **Non-VHH state-directing tools**: minibinders, DARPins, monobody scaffolds — different structural class, different training-visibility profile. Would require an amendment to the D2 test protocol (§D-2.7 assumes VHH nanobody).
- **Wait for a genuinely-novel deposition**: RCSB deposition rate for GPCR + state-directing Nb structures is ~10–20 per year; a fully-novel candidate may arrive in the next 6–12 months as follow-up manuscripts on receptors outside the D2 four (V1AR, DP2, ATP1R1, MRGPRX2, etc.) hit deposition.

## Disqualified candidates (previously in v2 as primary + backups)

**All four use standardised cryo-EM fiducial-Nb + BRIL/Fab constructs, verified via polymer-entity metadata + primary-citation abstract wording.** State determinants are the small-molecule ligands (or in one case a Kunitz-fold peptide toxin), not the Nb chain the RCSB metadata surfaced.

- **9HB3** (V2R + Mambaquaretin1 + anti-BRIL-Fab-Nb). The 141-aa VHH chain I promoted in v2 as "Mambaquaretin1" is the anti-BRIL fiducial-Nb from the deposition's scaffolding toolkit. Actual Mambaquaretin1 is a **57-residue Kunitz-fold antagonist peptide** from *Dendroaspis angusticeps* (green mamba) venom — three disulfide bridges, no immunoglobulin domain, no VHH scaffold. The Mambaquaretin1 peptide IS the state determinant for V2R inactive; but a 57-aa Kunitz toxin is not what the D2 protocol was designed to test (D2 tests Nb VHH partners, not peptide toxins), and mixing it into the D2 test would require a protocol extension. Not adopted.
- **9HAP** (V2R + tolvaptan + Mambaquaretin1 + anti-BRIL-Fab-Nb). Same fiducial issue; state determinants are tolvaptan (small molecule) + Mambaquaretin1 (Kunitz peptide). Not a nanobody test.
- **9EKH / 9EE5** (Prostaglandin D2 receptor + ONO-antagonist + anti-BRIL-Fab-Nb). State determinant is the ONO-series small-molecule antagonist. The paper's own wording: "anti-bRIL Fab (BAG2) … and stabilising nanobody" — the Nb is BAG2-anti-Fab, not a state-directing partner. Not adopted.
- **9EHS** (Adenosine A3 receptor + LUF7602 covalent antagonist + anti-BAG2-Nb). State determinant is LUF7602 covalent binding. The paper: "anti-BAG2 nanobody … to facilitate structure determination, serving as fiducial markers." Not adopted.

## Cost estimate for 9PXU test (unchanged from v1)

Grid (matches D2 per-receptor allocation shape):
- MOR × {apo, cognate_Gi, inactive_nb_9PXU} × 4 backbones × 5 seeds × 10 samples = **600 predictions**.
- No active_nb arm on MOR from this candidate.
- Rescore + analysis: parallel-driver ~30 min; per-cell + cluster-boot CIs ~30 min.

Curation ceremony required (per Block D PREREG §D-2.7; larger than a within-panel add because MOR is not in Block C's landed 37):

1. **Add human OPRM1 (P35372) receptor sequence** to `refs/panel_receptor_sequences.fasta`. New receptor entry. MOR is common enough that a reference sequence is trivially available (UniProt FASTA), but the entry itself needs adding.

2. **MOR active reference** — candidate **PDB 8EFQ** (verified this pass):
   - Title: DAMGO-bound mu-opioid receptor-Gi complex.
   - Deposited: 2022-09-08. **Post-Chai (2021-01) and Post-Protenix (2021-09) cutoffs**; pre-Boltz-2 (2023-06) cutoff. Boltz saw this reference during training; Chai and Protenix did not. OF3 status pending.
   - Species: **human OPRM1 P35372** ✓ (367 aa receptor chain confirmed).
   - Partners: DAMGO (4 aa peptide agonist) + Gαi1 (human P63096) + Gβ1 (rat P54311) + Gγ2 (bovine P63212). Standard heterotrimeric G-protein cryo-EM construct.
   - Method: cryo-EM. Citation: Cell 2022 "Molecular recognition of morphine and fentanyl by the human mu-opioid receptor".
   - **Not disqualified as a reference** — reference visibility during training is orthogonal to the training-cutoff test element (which is 9PXU-Nb6-input geometry, post-cutoff for all four backbones).
   - Curation task: add 8EFQ row to `refs/reference_set.csv` as MOR active reference; verify BW-anchor completeness (see §5 open item).

3. **MOR inactive reference** — the current entry `OPRM inactive 4DKL oprm_mouse` is **mouse** (P42866, not human P35372). Species mismatch is a documented failure mode in this campaign; do not reuse. Options:
   - **9PXU itself as the inactive reference** — the test's inactive-Nb arm consumes MOR + naloxone + Nb6-9PXU; using 9PXU as the reference for `pocket_ca_rmsd_inactive` is consistent with D2's convention (which uses the Nb-anchor PDB as the state reference for that arm). Post-cutoff status of 9PXU as a REFERENCE is fine — reference visibility doesn't disable the test.
   - Alternative: search for a human MOR-inactive-antagonist crystal without an Nb (e.g. human β-FNA-bound or human naloxone-bound MOR pre-9PXU). Deferred — 9PXU-as-inactive-reference is cleaner.

4. **Nb6_9PXU nanobody sequence** — add 131-aa sequence from 9PXU's polymer entity to `refs/nanobody_sequences.fasta`. **Must NOT collide with existing `Nb6_6VI4` label** — use `Nb6_MOP_9PXU` or `Nb6_OPRM_9PXU` as the disambiguated header. Sha256 = `5cce1ef6fc9e707b7456ebf5352ae7fe33691e4d191e66d21fc0b28bf49a564e` (verified this pass, does not collide with any existing partner entry).

5. **`refs/nanobody_state_anchors.csv`** — add row for MOR × 9PXU inactive.

6. **Chai `.aligned.pqt` cache warm** for the new Nb sequence (~5 min on HPC).

7. **Panel**: add MOR to `refs/tier_d2_expansion_panel.csv` (new file) or amend `refs/tier_d2_panel.csv` with `panel_extension=post_cutoff_test` column.

8. **`docs/BLOCK_D_PREREG_AMENDMENT_2026_09_XX.md`** — §D-2 amendment logging the added test AND the cousin-Nb + same-family caveats explicitly.

Compute wall-time:
- **HPC**: 600 preds × ~5 min/pred on H100 = ~50 GPU-hours. On 4 H100 workers concurrent: **~12–13 h wall**. On the elastic pool per D2 precedent: ~10–14 h.
- **Rescore**: <1 h on 16-CPU parallel driver.
- **Curation ceremony**: ~2–3 h human-side (subagent-assisted) — heavier than a within-panel add because MOR + 8EFQ + 9PXU + Nb6_9PXU + panel-CSV are all new to the campaign.
- **Total wall (excluding queue)**: **~1.5 days** if H100 pool is free; ~2 days with modest queue.

## Open questions before adoption (unchanged from v2 + one new)

1. **OF3 training cutoff `TBD`** — external release-notes lookup still needed (WebFetch attempts on `aqlaboratory/openfold`, `aqlaboratory/openfold3-preview`, and `openfold.readthedocs.io` returned no answer). If OF3 saw entries deposited after 2025-08-06, the test does not discriminate for OF3 alone (still discriminates for Boltz + Chai + Protenix). Applies identically to any post-cutoff candidate — not decision-differentiating.

2. **8EFQ BW-anchor completeness on MOR chain** — fetch 8EFQ CIF from RCSB, apply `scorer/pocket_metrics.py::pocket_ca_rmsd` receptor-side, confirm the 3.50 / 5.58 / 6.30 / 6.34 / 7.53 (or full-20) BW anchor residues resolve for the human MOR chain. ~15 min check.

3. **9PXU BW-anchor completeness on MOR chain** — same check on the inactive-reference PDB. ~15 min.

## Recommendation to Aditya (v3)

**Adopt 9PXU as the primary post-cutoff inactive-Nb test target with the cousin-Nb + same-family caveats stated in the dossier's main text**, subject to:
- (a) OF3 cutoff clears 2025-08-06 (still-open external check);
- (b) 8EFQ BW-anchor completeness passes on MOR chain (still-open CIF check);
- (c) 9PXU BW-anchor completeness passes on MOR chain (still-open CIF check);
- (d) Amendment PREREG names the cousin-Nb + same-family caveats explicitly.

If (a) fails → 3-backbone test result (Boltz-2 + Chai-1 + Protenix v2), reported as such.
If (b) or (c) fails → the specific check that failed determines whether MOR is still testable at all or needs a different reference PDB pair.

## §6.5 finalisation contingency (unchanged)

- **9PXU test returns "inactive-Nb-Nb6-9PXU steers inactive on ≥ 3/4 bb on MOR"** → cousin-Nb-within-opioid-family transfer succeeds; C-D-12 confound partially dischargeable; Discussion sentence: "demonstrated for a same-family + cousin-Nb transfer; a fully-novel-family test remains outstanding."
- **9PXU returns "inactive-Nb-Nb6-9PXU fails to steer inactive"** → training-availability + framework-transfer paths BOTH insufficient; directional-steering limit becomes more likely the genuine finding; Discussion sentence: "steering fails on cousin-Nb same-family test; a fully-novel test (V1AR / DP2 / MRGPRX2 / etc.) would settle whether the limit is intrinsic to VHH-mediated steering as a mechanism."
- **9PXU returns mixed / receptor-specific** → mirrors D2's per-receptor pattern; framing stays provisional; potentially motivates the wider fully-novel test.
