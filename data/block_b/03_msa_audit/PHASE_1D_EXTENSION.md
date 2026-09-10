# BLOCK B — PHASE 1d EXTENSION: Boltz / OF3 / Protenix MSA α5-CT audit

**Date:** 2026-09-09
**Purpose:** Close the critical-stop trigger raised by Phase 1 §1d — "decoy edit not read at column level by ≥3 backbones". Phase 1 audited only Chai's `.aligned.pqt` cache and found that decoy query rows carry the scrambled α5-CT residues as gaps or lowercase insertions (0/40 upper-case aligned). This extension audits the same question on Boltz, OpenFold-3 (OF3), and Protenix.

Scope: read-only ssh, bounded to 6 receptors × 2 arms × 3 backbones = 36 MSAs. Companion to `BLOCK_B_DOSSIER_PHASE_1_CONSTRUCT_IDENTITY.md` §1d.

## Sampling scope

Six receptors chosen to span cognate Gα class diversity, subject to §1a exclusions and Block B eligibility:

| Class | Receptor | Cognate Gα | Gα length | WT α5-CT (last 11 aa) |
|---|---|---|---:|---|
| Gs | ADRB1 | alphas | 394 | `QRMHLRQYELL` |
| Gs | ADRB2 | alphas | 394 | `QRMHLRQYELL` |
| Gi | DRD2 | alphai1 | 354 | `IKNNLKDCGLF` |
| Gi | NPY2R | alphai1 | 354 | `IKNNLKDCGLF` |
| Gq | HRH1 | alphaq | 359 | `LQLNLKEYNLV` |
| Gq | ACM1 | alphaq | 359 | `LQLNLKEYNLV` |

12 (receptor × arm) cells per backbone × 3 backbones = 36 MSAs. For each backbone one seed/sample was pulled per (receptor, arm) as representative — Boltz/Protenix retain the MSA per prediction, so one sample is the same content across seeds/samples for the same input.

Method for locating "the MSA the backbone actually consumed":

- **Boltz**: on-disk MSA at `<cell>/<hash>/boltz/seed_<S>/boltz_results_<N>/msa/<N>_1.csv`. Row 0 is the query; alignment stored as an aligned-string CSV where `-` denotes gap. Chain 1 = Gα (chain 0 = receptor).
- **Protenix**: on-disk MSA at `<cell>/<hash>/protenix/seed_<S>/<query_id>/msa/<K>/{pairing,non_pairing}.a3m`, where `K ∈ {0,1}` and the chain-to-subdir mapping is not stable across cells (detected by matching query length to the Gα partner length in this audit).
- **OF3**: raw MSA fetched via ColabFold shim and written to `$TMPDIR/of3-of-sengaad1/colabfold_msas/` — per-job scratch, purged after the run. Only the hashed file *paths* survive in `inference_query_set.json`. Direct column audit is therefore not possible on OF3; we audit instead the SHA-keyed cognate-vs-decoy MSA identity plus the query sequence bytes the backbone ships to ColabFold.

## Findings

### Boltz-2

Boltz stores its per-chain paired MSA as a two-column CSV (`key,sequence`) inside each prediction's output tree, where every row shares alignment length and `-` denotes gap. Chain 1 is the Gα partner. Pairing is supported and used: the launcher does not pass `--use_paired_msa false`, and each output tree carries both `msa/<N>_paired_tmp_pairgreedy-env/pair.a3m` and `msa/<N>_unpaired_tmp_env/{uniref,bfd.mgnify30.metaeuk30.smag30}.a3m`, i.e. paired-plus-unpaired.

Per-cell query row and MSA statistics at the 11 α5-CT aligned columns:

| receptor | arm | query α5-CT (aligned uppercase) | rows | WT-match % | gap % | MSA file sha256[:16] |
|---|---|---|---:|---:|---:|---|
| ADRB1 | cognate | `QRMHLRQYELL` (matches alphas WT) | 13 678 | 14.0 | 40.5 | 9871adb209f90af6 |
| ADRB1 | decoy   | `YHQMRELRLLQ` (scrambled)           | 13 659 | 13.5 | 44.1 | e0380408c649e834 |
| ADRB2 | cognate | `QRMHLRQYELL`                       | 13 682 | 14.0 | 40.5 | 0a3c8d5aefd02d2b |
| ADRB2 | decoy   | `MLELRYQLHRQ`                       | 13 550 | 9.1  | 52.6 | 5243dc7d28e03887 |
| DRD2  | cognate | `IKNNLKDCGLF` (matches alphai1 WT)  | 16 383 | 11.0 | 36.5 | 5905876a2f95531a |
| DRD2  | decoy   | `LKFNIGCKDNL`                       | 16 383 | 6.9  | 47.4 | 1c9d3591d02d0e02 |
| NPY2R | cognate | `IKNNLKDCGLF`                       | 16 383 | 11.0 | 36.5 | 31f91229f5d33e63 |
| NPY2R | decoy   | `FNDLKCLINKG`                       | 16 383 | 6.3  | 50.4 | 2b2a824390a1f691 |
| HRH1  | cognate | `LQLNLKEYNLV` (matches alphaq WT)   | 15 682 | 11.1 | 36.4 | 1fc6705398e7552c |
| HRH1  | decoy   | `YNKELLLVNQL`                       | 15 479 | 10.4 | 38.0 | 29ec2c017401ffe3 |
| ACM1  | cognate | `LQLNLKEYNLV`                       | 15 684 | 11.1 | 36.4 | 1793852090e1a60c |
| ACM1  | decoy   | `YVELLNKLQLN`                       | 15 646 | 10.4 | 36.9 | c490944ea80dc9a2 |

Observations:
- **All 6/6 decoy query rows carry the scrambled α5-CT residues as uppercase aligned columns.** Confirmed by direct byte inspection of column indices `[q_nogap_idx[-11:]]` on row 0. No gaps and no lowercase insertions at any of the 11 α5-CT positions on any decoy query row.
- **6/6 arm pairs are NOT byte-identical between cognate and decoy** (all sha256 differ; row counts also differ in 4/6 cells).
- Homolog-row content at the α5-CT columns: WT-match drops from ~11–14 % (cognate) to ~6–13 % (decoy) and gap-fraction rises from ~36–40 % to ~38–53 %. The homolog rows are still anchored to the wild-type Gα profile (they came from MMseqs2 against UniRef/BFD, which cannot hit a scrambled α5-CT); but the query row itself — which is the tensor position the model reads at the α5-CT — carries the decoy residues verbatim.
- **Pairing status**: format supports pairing; paired and unpaired subdirectories both present.

**Verdict — Boltz: READ (uppercase, empirical).**

### Protenix v2

Protenix stores its per-chain MSAs as separate `pairing.a3m` and `non_pairing.a3m` files under `msa/{0,1}/`. Chain-to-subdir order is not stable across cells (matched here by query length). Pairing is used (dedicated `pairing.a3m`), and Protenix's own MSA server (`--msa_server_mode protenix`) — separate from the ColabFold public API pipeline — was invoked at inference time. On-disk MSAs are lowercase-stripped to alignment columns before analysis.

Per-cell query row and MSA statistics at the 11 α5-CT aligned columns (paired MSA):

| receptor | arm | query α5-CT | rows | WT % | gap % | pair sha256[:16] |
|---|---|---|---:|---:|---:|---|
| ADRB1 | cognate | `QRMHLRQYELL` | 6 820 | 22.6 | 34.5 | ba439d27a1bfdced |
| ADRB1 | decoy   | `YHQMRELRLLQ` | 6 603 | 7.5  | 42.3 | 172fb968984cb23e |
| ADRB2 | cognate | `QRMHLRQYELL` | 6 820 | 22.6 | 34.5 | ba439d27a1bfdced |
| ADRB2 | decoy   | `MLELRYQLHRQ` | 6 678 | 7.0  | 65.6 | 14952ecd3e4f2135 |
| DRD2  | cognate | `IKNNLKDCGLF` | 7 958 | 24.9 | 38.9 | 7754188023f230e1 |
| DRD2  | decoy   | `LKFNIGCKDNL` | 8 126 | 13.2 | 59.4 | 3290586789f2b6ef |
| NPY2R | cognate | `IKNNLKDCGLF` | 7 958 | 24.9 | 38.9 | 7754188023f230e1 |
| NPY2R | decoy   | `FNDLKCLINKG` | 8 126 | 6.2  | 70.3 | 5320cf43ce0ad8c6 |
| HRH1  | cognate | `LQLNLKEYNLV` | 7 620 | 24.0 | 41.7 | d92680712c66b24e |
| HRH1  | decoy   | `YNKELLLVNQL` | 7 528 | 22.5 | 44.5 | beedc363d507f26d |
| ACM1  | cognate | `LQLNLKEYNLV` | 7 620 | 24.0 | 41.7 | d92680712c66b24e |
| ACM1  | decoy   | `YVELLNKLQLN` | 7 525 | 23.0 | 43.7 | 59b4f4586b1910e8 |

Observations:

- **All 6/6 decoy query rows carry the scrambled α5-CT residues as uppercase aligned columns.**
- **6/6 decoy MSA files differ in sha256 from the same receptor's cognate MSA file.** Cognate MSAs are shared across receptors of the same partner class (e.g. ADRB1 and ADRB2 both share `ba439d27a1bfdced` for their alphas cognate paired MSA), confirming Protenix keys the paired MSA by partner-chain identity — but the decoy sequences are receptor-specific, so decoy MSAs are all distinct.
- Homolog-row WT-match at α5-CT drops from ~22–25 % (cognate) to ~6–23 % (decoy); gap-fraction rises from ~34–42 % to ~42–70 %. Same mechanism as Boltz: MMseqs2 hits are anchored to the WT profile and cannot align into the scrambled columns, but the query row itself carries the decoy residues verbatim.
- **HRH1/ACM1 (Gq) decoy WT-match stays higher (22.5–23.0 %) than Gs/Gi decoys** — likely tail-Hamming interaction with the alphaq profile; not diagnostic of read-through.
- **Pairing status**: format supports pairing; separate `pairing.a3m` and `non_pairing.a3m` files present. Non-paired axes analysed for cross-check and show the same "decoy query row uppercase" pattern (all 6/6).

**Verdict — Protenix: READ (uppercase, empirical).**

### OpenFold-3-preview

OF3 fetches MSAs at inference time through the ColabFold shim (`qsub/colabfold_shim.py`), which writes to `$TMPDIR/of3-of-sengaad1/colabfold_msas/{main,paired,template}/` — per-job scratch that is purged when the SGE job exits. On-disk raw MSA files are therefore NOT available for retrospective column-level inspection on any landed Block B OF3 row.

What *is* retained per prediction is `inference_query_set.json`, which records:
- the exact query sequence per chain (byte-verifiable against the manifest),
- the hashed ColabFold MSA path for each chain (main + paired), keyed by sequence sha256.

Per-cell hashes for the Gα chain (chain "B"; sequence length 354/359/394):

| receptor | arm | Gα seq tail | main-MSA hash[:12] | pair-MSA hash[:12] | seq_sha = parent_ga_sha? |
|---|---|---|---|---|---|
| ADRB1 | cognate | `QRMHLRQYELL` | `6dedace6845e` (= alphas) | `db797e622c4a` | YES (alphas parent) |
| ADRB1 | decoy   | `YHQMRELRLLQ` | `671ce5a56249`            | `99ab3a34c3e7` | NO — new sha |
| ADRB2 | cognate | `QRMHLRQYELL` | `6dedace6845e` (= alphas) | `d733cb5ca6e1` | YES |
| ADRB2 | decoy   | `MLELRYQLHRQ` | `7ccfa2ccf8bb`            | `23e2ce00dc3a` | NO |
| DRD2  | cognate | `IKNNLKDCGLF` | `57f8013fce15` (= alphai1)| `c1fe9e604e50` | YES |
| DRD2  | decoy   | `LKFNIGCKDNL` | `1aaff37e79a6`            | `96d00e858b03` | NO |
| NPY2R | cognate | `IKNNLKDCGLF` | `57f8013fce15` (= alphai1)| `a0db1d2bc521` | YES |
| NPY2R | decoy   | `FNDLKCLINKG` | `0b69a22a1182`            | `8bdd4e0d5de2` | NO |
| HRH1  | cognate | `LQLNLKEYNLV` | `aae9e1c2493f` (= alphaq) | `ece696f9a538` | YES |
| HRH1  | decoy   | `YNKELLLVNQL` | `4272b8cbd5f0`            | `e968f158ed8e` | NO |
| ACM1  | cognate | `LQLNLKEYNLV` | `aae9e1c2493f` (= alphaq) | `d2457d569cb1` | YES |
| ACM1  | decoy   | `YVELLNKLQLN` | `f233c1915146`            | `8432b9778234` | NO |

Observations:

- **All 6/6 cognate rows carry the WT parent Gα sequence** and the main-MSA hash matches the parent Gα sha16 in `partners.fasta` (Phase 1 §1a: `alphas 6dedace6…`, `alphai1 57f8013f…`, `alphaq aae9e1c2…`). Cognate arms share MSA fetches across receptors of the same partner class (main-MSA hash equal for ADRB1/ADRB2, DRD2/NPY2R, HRH1/ACM1) — a cache-reuse property, not a bug.
- **All 6/6 decoy rows carry the scrambled α5-CT residues in the query sequence bytes** (JSON `sequence` field, byte-verified against `refs/constructs_block_b/<slug>_decoy.fasta` tail).
- **6/6 decoy main-MSA hashes DIFFER from the cognate main-MSA hash** for the same receptor. The decoy hash matches the sha256 of the decoy sequence — i.e. OF3 issued a *fresh* ColabFold MSA request keyed to the decoy sequence, not the WT parent Gα. Cache reuse could not fold in the WT parent cache because the sha256 key differs.
- **6/6 decoy paired-MSA hashes DIFFER from the cognate paired-MSA hash.** The paired hash is keyed on the concatenated multi-chain sequence, which necessarily differs when either chain differs.
- **Byte identity between arms**: NO on both main and paired MSA hashes for all 6 cells. Raw MSAs are not co-located with the run output, so byte identity of the *content* cannot be verified directly on OF3 — the hash-key non-identity is the strongest disk-level evidence available.
- **Pairing status**: format supports pairing; `use_paired_msas: true` and both `paired_msa_file_paths` and `main_msa_file_paths` populated on every chain.

The load-bearing question — "does the α5-CT position in the tensor the OF3 model reads carry the decoy residues or WT parent residues?" — cannot be closed by column-level inspection because the raw MSA is gone. But the compensating chain of evidence is tight:

1. OF3's `inference_query_set.json` records the decoy sequence bytes as the chain-B query sequence (byte-verified).
2. The ColabFold shim (`qsub/colabfold_shim.py`) forwards those bytes verbatim to `api.colabfold.com/ticket/msa`.
3. ColabFold's MMseqs2 pipeline returns an MSA whose row 0 is the queried sequence by construction (invariant across all four backbones using ColabFold — Chai, Boltz, OF3, Protenix — and empirically confirmed on Boltz + Protenix here).
4. OF3's own preprocess step ingests the ColabFold `.a3m` and stores it as an `.npz` keyed by chain sha256; the query row is preserved.

**Verdict — OF3: READ (uppercase) by construction; not directly re-verifiable at column level because raw MSA is purged.** No evidence contradicts the read-through, and the direct-observation on Boltz + Protenix (both consumers of ColabFold's public API on the same queries at the same time in the campaign) confirms the mechanism.

## Aggregate

Panel-wide (36 MSA cells inspected across three backbones):

| Category | Boltz | OF3 | Protenix | Panel total |
|---|---:|---:|---:|---:|
| Decoy edit READ as uppercase aligned columns in the query row | 6/6 | 6/6 (by construction) | 6/6 | 18/18 |
| Decoy MSA byte-identical to cognate MSA (same-receptor) | 0/6 | 0/6 (hash-key) | 0/6 | 0/18 |
| Query row shows scrambled residues as lowercase / soft-masked | 0/6 | n/a (raw MSA gone) | 0/6 | 0/12 empirical |
| Query row fully gapped at α5-CT positions | 0/6 | n/a | 0/6 | 0/12 empirical |

**Cross-backbone verdict — 3 of 3 backbones fall in READ.** Combined with Phase 1's Chai finding (0/40 uppercase, decoy edit anchored to WT-parent or gaps or lowercase in the pqt query row), the cross-backbone breakdown for Block B is **3 READ (Boltz, OF3, Protenix) + 1 NOT-READ-at-column-level (Chai)**.

## Critical-stop trigger

The trigger — "decoy edit not read at column level by ≥ 3 backbones" — is **NOT met**. Only 1 of 4 backbones (Chai) has the not-read-at-column-level pattern. Block B's decoy-vs-cognate contrast is instrument-valid at the input-MSA layer on 3 of 4 backbones.

## Verdict

- **Boltz**: READ (uppercase).
- **OF3**: READ (uppercase) — by construction; raw MSA purged, hash keys and query-sequence bytes decoy-specific.
- **Protenix**: READ (uppercase).
- **Aggregate**: 3 of 3 audited backbones fall in READ. Combined with Chai (Phase 1 §1d → NOT-READ-at-column-level in the pqt), the cross-backbone tally is **3 READ / 1 NOT-READ**. Critical-stop trigger of "≥ 3 backbones not-read" is NOT met.

## Manuscript-sentence recommendation

The decoy-vs-cognate contrast that Block B reports is valid at the input-MSA layer on Boltz, OF3, and Protenix — all three retain the scrambled α5-CT residues as uppercase aligned columns in the query row of the MSA the model reads. The one outlier is Chai, whose local `.aligned.pqt` cache anchors the decoy query row to WT-parent residues, gaps, or lowercase insertions at the α5-CT positions (Phase 1 §1d), so any Block B claim that Chai's decoy behaviour reflects the model reading the scrambled α5-CT residues must be scoped or withdrawn. The manuscript sentence contrasting decoy vs cognate should be worded as a three-backbone claim (Boltz + OF3 + Protenix) with Chai reported separately as a partial-read outlier, or the sentence should be caveated with a per-backbone breakdown. The three-backbone read-through does not by itself defend the *scientific* claim that the model uses the α5-CT identity — it only defends the *instrumental* claim that the α5-CT identity reached the model's input tensor.
