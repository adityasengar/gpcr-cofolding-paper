# GATE-1 — D2 nanobody per-row sequence SHA audit

**Scope**: For all four D2 receptors (ADRB2, ACM2, AGTR1, OPRK) and every
nanobody arm that landed rows in the analysed corpus, hash the literal
nanobody chain sequence the prediction job actually consumed and compare
against the two candidate references (real Nb60 vs the 126-aa Nb80 mislabel).

**Verdict**: **False alarm — all 4 D2 nanobody arms, across all 4 backbones,
consumed the correct real reference sequences.** F3 ("inactive-Nb unreliable")
stands as currently drafted. The `partners.fasta:Nb60` mislabel (126 aa) is
confirmed as a documentation defect that was never ingested by any D2 launcher.

---

## Reference SHAs (computed from refs, verified)

| Name | Source file | Length | SHA-256 |
|---|---|---:|---|
| real Nb60 (5JQH, inactive, ADRB2) | `refs/nanobody_sequences.fasta` | 125 | `1406ad7ea26451149ea73339e2282ef0f77f52d693c680cbf790db7af767db62` |
| real Nb6 (6VI4, inactive, OPRK) | `refs/nanobody_sequences.fasta` | 133 | `a7b413fe44dba2a72187b519f26b7312d90ac964e408f0ae607e915e1830a2ab` |
| real Nb9-8 (4MQS, active, ACM2) | `refs/nanobody_sequences.fasta` | 125 | `4888b3976a25b1529b9f2d12f52528e5f81a14a4d56cd091569d3e791e84806f` |
| real Nb.AT110i1_le (6OS2, active, AGTR1) | `refs/nanobody_sequences.fasta` | 128 | `d8c31820ac1bb8784867b0192e97d9efcea90a80218e53a831de7b45f644595a` |
| **Nb60 MISLABEL (=Nb80 sequence)** | `docs/EXPERIMENT_CATALOG/sequences/partners.fasta` | **126** | `b9ad1bad7a2933d8e3cebd59519ac77c5f516e9d20ebf3a5c02860c59695f868` |

Memory `block_d_d2_nanobody_collision_2026_09_09.md` sha prefixes (`1406ad7e…`, `b9ad1bad…`) both confirmed.

## D2 landed corpus — (receptor, arm) bucket census

Counted from `experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv`, 2,370 rows:

| Receptor | Arm | Rows | Manifest partner_identity | partner_perturbation |
|---|---|---:|---|---|
| ACM2 | active_nb | 200 | 4MQS | wt |
| ACM2 | apo | 200 | (none) | wt |
| ACM2 | cognate_ga | 200 | alphas | wt |
| ADRB2 | apo | 200 | (none) | wt |
| ADRB2 | cognate_ga | 200 | alphas | wt |
| ADRB2 | inactive_nb | 200 | 5JQH | wt |
| **ADRB2** | **active_nb** | **0 (dropped)** | not in dispatch manifest | — |
| AGTR1 | active_nb | 170 (3 samples short on OF3) | 6OS2 | wt |
| AGTR1 | apo | 200 | (none) | wt |
| AGTR1 | cognate_ga | 200 | alphas | wt |
| OPRK | apo | 200 | (none) | wt |
| OPRK | cognate_ga | 200 | alphas | wt |
| OPRK | inactive_nb | 200 | 6VI4 | wt |

**ADRB2 active_nb dropped** — confirmed 0 rows in the analysed corpus and 0
rows in `tier_d2_manifest.dispatch.csv` (no such row ever entered the
dispatch pool). Consistent with memory `block_d_d2_nanobody_collision_2026_09_09.md`.
No `partner_perturbation=placeholder_nb80_from_nb60_5jqh` flag survives in the
dispatch manifest — the flag was on the pre-dispatch curation pass, and the
row was removed before dispatch.

## Per-arm × per-backbone consumed sequence hash

For each (receptor, nanobody-arm) bucket, one representative input file per
backbone was pulled directly from HPC pool
`/hpc/scratch/sengaad1/paper_af3/experiments/023_tier_d2_directed_inactive/full/pool/inputs/{boltz,chai,of3,protenix}/`
and the chain-B (nanobody) sequence was extracted and hashed.

Cross-seed stability: the manifest points to the same `<launcher>/tier_d2_<rec>_<arm>_<backbone>_seed0.<ext>` file for every seed within a (receptor, arm, backbone) cell (the seed is a prediction-side parameter; the input sequence file is shared). No per-seed hash drift possible by construction.

### ACM2 active_nb (expected: real Nb9-8, 125 aa, `4888b397…`)

| Backbone | Length | SHA-256 | Verdict |
|---|---:|---|---|
| Boltz | 125 | `4888b3976a25b152…` | ✓ MATCH real Nb9-8_4MQS |
| Chai | 125 | `4888b3976a25b152…` | ✓ MATCH real Nb9-8_4MQS |
| OF3 | 125 | `4888b3976a25b152…` | ✓ MATCH real Nb9-8_4MQS |
| Protenix | 125 | `4888b3976a25b152…` | ✓ MATCH real Nb9-8_4MQS |

### ADRB2 inactive_nb (expected: real Nb60, 125 aa, `1406ad7e…`) — **critical arm for F3**

| Backbone | Length | SHA-256 | Verdict |
|---|---:|---|---|
| Boltz | 125 | `1406ad7ea2645114…` | ✓ MATCH real Nb60_5JQH |
| Chai | 125 | `1406ad7ea2645114…` | ✓ MATCH real Nb60_5JQH |
| OF3 | 125 | `1406ad7ea2645114…` | ✓ MATCH real Nb60_5JQH |
| Protenix | 125 | `1406ad7ea2645114…` | ✓ MATCH real Nb60_5JQH |

None of the 4 backbones ingested the 126-aa collision sequence.

### AGTR1 active_nb (expected: real Nb.AT110i1_le, 128 aa, `d8c31820…`)

| Backbone | Length | SHA-256 | Verdict |
|---|---:|---|---|
| Boltz | 128 | `d8c31820ac1bb878…` | ✓ MATCH real Nb.AT110i1_le_6OS2 |
| Chai | 128 | `d8c31820ac1bb878…` | ✓ MATCH real Nb.AT110i1_le_6OS2 |
| OF3 | 128 | `d8c31820ac1bb878…` | ✓ MATCH real Nb.AT110i1_le_6OS2 |
| Protenix | 128 | `d8c31820ac1bb878…` | ✓ MATCH real Nb.AT110i1_le_6OS2 |

### OPRK inactive_nb (expected: real Nb6, 133 aa, `a7b413fe…`) — **critical arm for F3**

| Backbone | Length | SHA-256 | Verdict |
|---|---:|---|---|
| Boltz | 133 | `a7b413fe44dba2a7…` | ✓ MATCH real Nb6_6VI4 |
| Chai | 133 | `a7b413fe44dba2a7…` | ✓ MATCH real Nb6_6VI4 |
| OF3 | 133 | `a7b413fe44dba2a7…` | ✓ MATCH real Nb6_6VI4 |
| Protenix | 133 | `a7b413fe44dba2a7…` | ✓ MATCH real Nb6_6VI4 |

## Outcome assignment per dispatch table

Per the dispatch's four-outcome map:

| Outcome | Applies to |
|---|---|
| All 4 receptors' nanobody-arm rows used the real reference sequence | **✓ ALL 4 D2 nanobody arms across all 4 backbones (2 inactive-Nb + 2 active-Nb)** |
| Some subset used the 126 aa collision | (none) |
| All 4 used the collision | (none) |
| Label was wrong upstream but actual job input traced to the correct sequence — false alarm, but log the mislabel | **✓ `partners.fasta:Nb60` (126 aa, sha `b9ad1bad…`) is a real documentation defect; it was never consumed by D2** |

## Downstream impact on F3 ("inactive-Nb unreliable")

**F3 stands as currently drafted.** The panel-scale finding that no backbone
is a reliable inactive-directing partner rests on two receptors with
`inactive_nb` arms (ADRB2 with Nb60, OPRK with Nb6). Both consumed the
correct real reference sequences on all 4 backbones. The result is a real
scientific finding, not a curation artefact.

**No rerun of any D2 cell is required by GATE-1's evidence.** The
cost/benefit question in dispatch §6.2 is moot for the GATE-1 axis (there
is no contaminated cell to rerun). Separate motivations for D2 augmentation
— curating a real Nb80/4LDE reference to restore the intentionally-dropped
ADRB2 active_nb arm, or adding a third receptor with an inactive_nb anchor
— remain open as follow-up experiments, not remediation.

## Residual documentation defect (not remediation)

The `Nb60` header in `docs/EXPERIMENT_CATALOG/sequences/partners.fasta`
(126 aa, sha `b9ad1bad…`) is actually the Nb80 sequence — CDR3 signature
matches 3P0G Nb80, not 5JQH Nb60. The file has never been consumed by any
D2 launcher (D2 launchers ingest from `refs/nanobody_sequences.fasta`
directly). The mislabel remains a live risk for any future experiment that
copies from `partners.fasta` by header name; flag for a header-fix commit
as a separate housekeeping task, not a D2 remediation.

## Evidence trail

- D2 corpus: `experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv`
  (2,370 rows).
- D2 dispatch manifest: `experiments/023_tier_d2_directed_inactive/manifest/tier_d2_manifest.dispatch.csv`
  (240 rows: 4 rec × 3-4 arms × 4 bb × 5 seeds).
- HPC input files inspected (16 files total = 4 nb-arms × 4 backbones,
  seed0 representatives):
  - `/hpc/scratch/sengaad1/paper_af3/experiments/023_tier_d2_directed_inactive/full/pool/inputs/{boltz,chai,of3,protenix}/tier_d2_{acm2_active_nb,adrb2_inactive_nb,agtr1_active_nb,oprk_inactive_nb}_<bb>_seed0.<ext>`
- Reference file: `refs/nanobody_sequences.fasta`.
- Mislabel documentation source: `docs/EXPERIMENT_CATALOG/sequences/partners.fasta`.

## What this gate did not resolve

Out of scope for GATE-1 (deferred to §6 or to Part A analyses):
- Whether to curate Nb80/4LDE and rerun the dropped ADRB2 active_nb arm.
- Whether to add a third inactive_nb receptor to distinguish
  model-specific from receptor-specific inversion (per D2 headline §Next moves).
- The `partners.fasta:Nb60` header rename (housekeeping, not D2 remediation).
