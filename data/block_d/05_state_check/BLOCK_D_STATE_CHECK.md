# BLOCK D — STATE CHECK (§3 of autonomous closeout dispatch)

**Date**: 2026-09-10.
**Baseline**: paper_af3 working repo HEAD `c29d5a8` (Block C wrap); paper_af3_release HEAD `297d97b` (block_c_freeze, pushed).
**Rule**: disk wins over recall. Where disk conflicts with a recalled fact or a headline doc, the conflict is logged.
**Gate**: GATES-1..4 all logged in `draft/gates/GATE_[1-4]_*.md`. §3 unblocked.

---

## Q1 — Panel of record per tier

| Tier | Recs dispatched | Recs landed | Preds landed | Grid | Delta |
|---|---:|---:|---:|---|---|
| D1 (deep apo bistability) | 7 | 7 | 14,000 | 7 × 4 bb × apo × 5 seeds × 100 samples | 0 short (100 %) |
| D2 (directed inactive) | 4 | 4 | 2,370 | 4 × {3–4 arms} × 4 bb × 5 seeds × 10 samples | 30 short (AGTR1 × active_nb × OF3 stragglers) |
| D3 (MSA-depth ladder) | 26 | 26 | 25,810 | 26 × 4 bb × 5 depths × 5 seeds × 10 samples | 190 short (Chai 90 + OF3 100) |

**Sources**: `refs/tier_d1_panel.csv` (7 rows), `refs/tier_d2_panel.csv` (4 rows), `refs/tier_d3_panel.csv` (26 rows). All three panel CSVs land in a single commit alongside the manifest builder per the selection-rule-freeze convention.

**D1 receptors**: CNR2 (anchor), OPSD, ADRB2, LPAR1 (mid-range); CXCR4, GHSR, NPY1R (confirmatory). Selection rule cited in the panel CSV header.

**D2 receptors + arms** (from `input_state_claim` column of rows.csv):
- ADRB2: apo, `Ga-coupled-active`, `Nb-inactive` (5JQH/Nb60) — 200 rows × 3 arms = 600 rows. Fourth `Nb-active` (4LDE/Nb80 placeholder) **intentionally dropped**; 0 rows in corpus. Confirmed via SHA collision (GATE-1) + dispatch manifest.
- ACM2: apo, `Ga-coupled-active`, `Nb-active` (4MQS/Nb9-8) — 200 × 3 = 600 rows.
- AGTR1: apo, `Ga-coupled-active`, `Nb-active` (6OS2/Nb.AT110i1_le) — 200 + 200 + 170 = 570 rows (30 short on Nb-active × OF3 per headline).
- OPRK: apo, `Ga-coupled-active`, `Nb-inactive` (6VI4/Nb6) — 200 × 3 = 600 rows.

**D3 receptors** (26): 5HT1B, 5HT2C, AA2AR, ACM2, ADRB2, AGTR1, APJ, B1B1U5, CCR5, CNR2, CXCR2, CXCR4, DRD2, EDNRB, GHSR, GRPR, HRH1, LPAR1, LT4R1, MCHR1, NPY1R, NPY2R, OPRD, OPRK, OPRX, OPSD. Stratified from 40 Class A minus 8 sealed = 32; further reduced to 26 to preserve budget after adding the 512 rung.

**Panel-of-record parity vs Block C**:
- D3's 26-receptor panel overlaps Block C's 36-landed Class A panel on 26 recs (D3 is a subset).
- D1's 7 receptors are all in Block C's 36 landed and in D3's 26.
- D2's 4 receptors are all in Block C's 36 and in D3's 26 (ADRB2, ACM2, AGTR1, OPRK — the "matched pair + 3 single-anchor" pattern per `refs/nanobody_state_anchors.csv`).

**Verdict**: no panel drift. D1/D2/D3 all consume subsets of Block C's landed Class A panel; the four D2 receptors overlap D1 (ADRB2) and D3 (all four).

---

## Q2 — Corpus SHAs + scorer version

**Uniform scorer across all three D-tier corpora** (per GATE-4 + spot recompute this pass):

| Tier | rows.csv path | Rows | `scorer_git_sha` | `ref_set_csv_sha256` (16-hex) |
|---|---|---:|---|---|
| D1 | `experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` | 14,000 | `d9c646af5f89861c16062bf256de96a8389d9915` | `7a261988ff73eedc` |
| D2 | `experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv` | 2,370 | `d9c646af5f89861c16062bf256de96a8389d9915` | `7a261988ff73eedc` |
| D3 | `experiments/024_tier_d3_msa_depth/analysis/full/rows.csv` | 25,810 | `d9c646af5f89861c16062bf256de96a8389d9915` | `7a261988ff73eedc` |

**Cross-tier and cross-block comparability**: `d9c646af` matches Block C's `rescore_t7c_full/rows.csv` scorer (per Block C STATE_CHECK §(a) sibling corpus). Block C's *primary* corpus (`rows.tier3.v2.csv`) is on the older scorer `3d9c6faa`. So:

- **D1 vs Block C pose corpus**: same scorer. D1's F5 (CNR2 saturation) directly comparable to Block C's pocket-Cα results on that same sibling corpus.
- **D1 vs Block C primary corpus** (`rows.tier3.v2.csv` on `3d9c6faa`): scorer differs. `scorer/axes.py` (predicate cols) UNCHANGED between the two per GATE-4; `pocket_ca_rmsd` computation UNCHANGED. Cross-block comparability holds for the two-instrument predicate and pocket-Cα.
- **D2 vs D1 vs D3**: all uniform.

**Ref set of record**: `7a261988ff73eedc9d21e5cc2a9eaf0436b9f38e3827a87493295a8d8382b90c` — the "on-disk today" SHA per Block A VERSION.md. This is post-D-02 curation. Block A's row-level rescore-time SHA was `6ee2cad8...`; D-tier ran on the newer refs.

**Documentation drift found** (per GATE-4):
- `experiments/023_tier_d2_directed_inactive/analysis/tier_d2_full_headline_2026_09_07.md` line 6 cites scorer `891041e858f3747b…`.
- `experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md` line 6 cites the same.
- **That SHA does not exist in git** — no ref, no orphan object, not in reflog. Phantom SHA in prose only; **the row-level `d9c646af` is authoritative**. Same shape as Block C's `T7C_POST_FIX_HEADLINE.md` (documentation drift).
- **Correction pass required at dossier-authoring time**: replace `891041e858f3747b` → `d9c646af5f89861c16062bf256de96a8389d9915` in the D2 and D3 headline docs, or add a corrigendum footer.

**Retracted from memory system**: `d3_full_confirmed_2026_09_08.md` cites `Scorer SHA: 891041e858f3` — same drift; the memory is inconsistent with the on-disk row-level value.

---

## Q3 — Chain identification

`chain_selection_method = identity_match_to_wt` uniformly across all 14,000 + 2,370 + 25,810 = **42,180 rows**. This is the v2 chain-picker convention Block C settled on (anchor-hit + SIFTS/struct_ref_seq-based UniProt match), NOT the v1 longest-polymer-chain heuristic that Block C retracted at the G4 v2 census.

**Implication**: D-tier receptor-side chain identification is on the same footing as Block C's G4 v2 verified corpus. No chain-picker regression carried into D-tier.

**Anchor-hit completeness**: not explicitly verified per row in the D-tier corpora — the receptor_anchor_hits count column isn't emitted by this scorer version. But per GATE-4, `scorer/pocket_metrics.py` is UNCHANGED from `d9c646af` (the scorer these three ran) to HEAD, so the same anchor-hit logic that Block C verified applies here.

---

## Q4 — Reference set of record

**Row-level uniform**: `ref_set_csv_sha256 = 7a261988ff73eedc...` on all 42,180 D-tier rows.

**Per-receptor active + inactive reference PDBs**: distinct SHAs per row (`ref_pdb_sha_active` + `ref_pdb_sha_inactive`); not enumerated in this STATE_CHECK. Confirmed uniform within (receptor, arm) via GATE-3's cross-check step (matched-seed matched-sample structure comparisons collapse to single PDB SHA per receptor).

**Nanobody sequences (D2 only)**: `refs/nanobody_sequences.fasta` supplies the state anchors:
- Nb60_5JQH (125 aa, sha `1406ad7e…`) — ADRB2 inactive-stabiliser
- Nb6_6VI4 (133 aa, sha `a7b413fe…`) — OPRK inactive-stabiliser
- Nb9-8_4MQS (125 aa, sha `4888b3976a25b152…`) — ACM2 active-stabiliser
- Nb.AT110i1_le_6OS2 (128 aa, sha `d8c31820ac1bb878…`) — AGTR1 active-stabiliser

All four consumed correctly per GATE-1 row-hash audit; no collision with the 126-aa `partners.fasta:Nb60` mislabel.

**Verdict**: reference set is stable and uniform across all three D-tier corpora.

---

## Q5 — Predicate scope

**Two-instrument Class A predicate** unchanged from Block C §C-5:
- `d_npxxy_y558_y753_oh < 9.082 Å` AND
- `d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å`

Both columns present + populated on all 42,180 rows. Predicate saturation risk (SC-C-6 in Block C: floor/ceiling saturation on the *2×2 pocket-Cα* interaction) is not directly triggered here — D-tier is single-arm (apo for D1/D3; multi-arm for D2 but not 2×2). Predicate SATURATION on D1's CNR2 receptor (F5: 100 % sub-Å to both refs) is a **receptor-specific RMSD-degeneracy**, distinct from the Block C 2×2 saturation. Reported in F5 as a discrete caveat.

**Reference-predicate calibration on the 4 D2 receptors** (a §3 D2 addition) — running in Part A/D2 fork. Result posts to `partA/PARTA_D2.md` §3.

---

## Q6 — Paralog cluster coverage (added; matters for §4 CI method)

| Tier | Receptors | Distinct paralog clusters | Cluster-boot defensibility |
|---|---:|---:|---|
| D1 | 7 | 7 (adrenergic_beta, cannabinoid, chemokine_cxcr, ghrelin, lysophosphatidic, npy, opsin_vertebrate) | Degenerate: 1 rec/cluster. Cluster-boot ≡ receptor-boot. State limitation. |
| D2 | 4 | 4 (adrenergic_beta, angiotensin, muscarinic, opioid) | Same degeneracy. |
| D3 | 26 | 22 (some doubled: serotonin has 5HT1B/5HT2C; chemokine_cxcr has CXCR2/CXCR4; opioid has OPRD/OPRK; opsin invertebrate+vertebrate) | **Valid**: cluster-boot adds signal beyond receptor-boot. |

**Consequence for §4 Part A**: D3 gets proper cluster-boot 95 % CIs; D1 and D2 get receptor-boot CIs with an explicit statement that at this n the paralog-cluster grouping doesn't add anything the receptor-level bootstrap doesn't already carry. Following the dispatch's "say so explicitly" rule rather than forcing cluster-boot past its range.

---

## STATE_CHECK verdict

- (a) Panel of record: **established** per tier. No panel drift. All 3 tiers consume subsets of Block C's 36-rec landed Class A panel.
- (b) Corpus SHAs: **established**. Uniform `d9c646af` across all three D-tier corpora. Documentation drift on the phantom `891041e858f3` prose SHA in two headline docs — flag for correction, no data impact.
- (c) Chain identification: **established**. Uniform `identity_match_to_wt` (v2 anchor-hit + SIFTS) across 42,180 rows. No v1 longest-polymer regression risk.
- (d) Reference set: **established**. Uniform `7a261988` across all D-tier rows; distinct per-receptor active + inactive PDBs verified indirectly via GATE-3. Nb sequences verified correct per GATE-1.
- (e) Predicate scope: **unchanged from §C-5**. Reference-predicate calibration on D2's 4 receptors pending Part A/D2.
- (f) Paralog cluster coverage: D1/D2 at n=1 rec/cluster (degenerate); D3 at 22 clusters (valid). Method-selection note carried into §4.

**No hard-stop conditions triggered.** Proceeding to §4 Part A per-tier.

## Deltas to propagate into the Block D dossier

1. **Correction pass at dossier-authoring**: `891041e858f3747b` (phantom) → `d9c646af5f89861c16062bf256de96a8389d9915` in headline docs. Also correct the auto-memory `d3_full_confirmed_2026_09_08.md`.
2. **Cluster-boot method-limitation statement** — D1 and D2 use receptor-boot with n=7/4 respectively; state this rather than forcing cluster-boot vocabulary.
3. **AGTR1 × active_nb × OF3 shortfall** (170 rows vs 200 expected) — carry as a coverage caveat, not a headline retraction.
4. **D3 backbone imbalance** (Chai 6,410 + OF3 6,400 vs Boltz/Protenix 6,500 canonical) — 90 + 100 = 190 preds short across shallow-depth cells. Carry as a coverage caveat; per-cell active-fraction denominator uses the actual landed n, not 6,500.
5. **Predicate scope statement** — unchanged from §C-5. This is a positive fact worth stating in the dossier's opening (the field-standard predicate applies across all D-tier claims).

---

**End STATE_CHECK. Proceeding to §4 Part A per-tier** (D1/D2/D3 forks running).
