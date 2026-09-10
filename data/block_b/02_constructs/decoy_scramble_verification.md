# Decoy α5-CT scramble — independent byte-level verification

Independent audit of `scripts/build_shuffled_decoy_constructs.py`'s decoy
output, run against the tracked artefacts on disk (laptop-side, no HPC).
Ground truth for cognate class/parent is `refs/gpcr_coupling.csv`
(`primary_ga_class` / `primary_ga_identity`), **not** the build script's own
manifest, report, or FASTA-header self-annotations — those are the artefact
under audit and are treated as claims to be checked, not as sources of truth.

## Verdict: **PASS** — all 40 decoys are surgically scrambled

Every one of the 40 Block B decoy FASTAs under `refs/constructs_block_b/`
differs from its correct cognate Gα parent **only** in the last 11 residues
(the α5-CT), and nowhere else. Specifically, across all 40 receptors:

- `decoy_len == cognate_len` — **40/40**
- `decoy[:-11] == cognate[:-11]` (byte-identical prefix) — **40/40**
- α5-CT tail Hamming distance in `[7, 11]` — **40/40** (min 7, max 11, mean
  9.525 — matches `construct_build_report.md`'s claimed "min 7 / max 11 /
  mean 9.53" to reported precision)
- `Counter(decoy_tail) == Counter(cognate_tail)` (scramble is a permutation,
  not a substitution) — **40/40**
- `Counter(decoy_full) == Counter(cognate_full)` (whole-sequence composition
  preserved) — **40/40**
- `sha256(decoy) != sha256(cognate)` (scramble is not a no-op) — **40/40**
- Exactly one FASTA record per decoy file, correctly formatted header —
  **40/40**
- Cognate-class → parent-slug mapping cross-checked independently via
  `gpcr_coupling.csv`'s `primary_ga_class` (mapped through the canonical
  class table) against its own `primary_ga_identity` column — **40/40
  consistent**, and every decoy's non-tail region matches that
  independently-derived parent (not a mismatched/wrong-family parent) —
  **40/40**
- Wrong-parent fallback scan (decoy prefix checked against all 5 canonical
  Gα slugs, not just the expected one) — **0/40 false-parent matches**;
  every decoy's prefix matches its expected parent and no other
- Decoy-header self-reported metadata (`alpha5_ct_original=`,
  `alpha5_ct_scrambled=`, `hamming=`, `length=`, `sha=`, `cognate_class=`)
  cross-checked against independently computed values — **0/40 mismatches**
- Hamming-category check (report claims realized floor 7, build-script
  floor 5) — **0/40** receptors in the `[5,7)` table-vs-realized-discrepancy
  band, **0/40** below the 5 build-script contract floor
- Multi-record / mixed cognate+decoy FASTA check — **0/40** files have more
  than one FASTA record

No anomalies of any kind were found. This is a clean PASS with zero
tolerance applied at every check.

## Method

1. Cognate parent per receptor: `refs/gpcr_coupling.csv[receptor]
   .primary_ga_class` → mapped via `{Gs:alphas, Gi:alphai1, Gq:alphaq,
   G12:alpha13, Gt:alphat}` → cognate sequence pulled from
   `docs/EXPERIMENT_CATALOG/sequences/partners.fasta` by that slug. This is
   independent of the build script; `primary_ga_identity` in the same CSV
   row was cross-checked for internal consistency (also 40/40 consistent).
2. Decoy sequence: parsed directly from `refs/constructs_block_b/
   <receptor_lower>_decoy.fasta` (single record per file, confirmed).
3. Byte comparison: length, `[:-11]` prefix equality, last-11 Hamming
   distance, `Counter` equality on tail and on full sequence, SHA-256
   inequality.
4. Anomaly-triggered fallback: if the prefix check had ever failed against
   the expected parent, the script would scan the decoy's non-tail region
   against all 5 canonical Gα parents to distinguish "corrupted" from
   "swapped-parent" failures. Not triggered — no receptor needed it.
5. All 40 receptors were processed in a single non-interrupted pass (no
   anomaly ever fired the stop condition).

Files read: `refs/gpcr_coupling.csv`, `refs/partner_gα_by_class.csv`,
`docs/EXPERIMENT_CATALOG/sequences/partners.fasta`,
`refs/constructs_block_b/*_decoy.fasta` (40 files),
`experiments/019_block_b_partner_selection/analysis/construct_build_report.md`
(for the receptor list and as a claims source to check against, not as
ground truth). No file under audit was modified.

## Per-receptor verification table (all 40)

| receptor | cognate class | parent slug | cognate len | decoy len | prefix-match len | tail hamming | composition match | verdict |
|---|---|---|---|---|---|---|---|---|
| 5HT1B | Gi | alphai1 | 354 | 354 | 343 | 10 | yes | PASS |
| 5HT2C | Gq | alphaq | 359 | 359 | 348 | 9 | yes | PASS |
| 5HT5A | Gi | alphai1 | 354 | 354 | 343 | 10 | yes | PASS |
| AA1R | Gi | alphai1 | 354 | 354 | 343 | 11 | yes | PASS |
| AA2AR | Gs | alphas | 394 | 394 | 383 | 9 | yes | PASS |
| ACM1 | Gq | alphaq | 359 | 359 | 348 | 9 | yes | PASS |
| ACM2 | Gi | alphai1 | 354 | 354 | 343 | 9 | yes | PASS |
| ACM4 | Gi | alphai1 | 354 | 354 | 343 | 7 | yes | PASS |
| ADA2A | Gi | alphai1 | 354 | 354 | 343 | 9 | yes | PASS |
| ADRB1 | Gs | alphas | 394 | 394 | 383 | 10 | yes | PASS |
| ADRB2 | Gs | alphas | 394 | 394 | 383 | 10 | yes | PASS |
| AGTR1 | Gq | alphaq | 359 | 359 | 348 | 10 | yes | PASS |
| APJ | Gi | alphai1 | 354 | 354 | 343 | 7 | yes | PASS |
| B1B1U5 | Gi | alphai1 | 354 | 354 | 343 | 10 | yes | PASS |
| CCKAR | Gq | alphaq | 359 | 359 | 348 | 8 | yes | PASS |
| CCR5 | Gi | alphai1 | 354 | 354 | 343 | 10 | yes | PASS |
| CNR1 | Gi | alphai1 | 354 | 354 | 343 | 8 | yes | PASS |
| CNR2 | Gi | alphai1 | 354 | 354 | 343 | 9 | yes | PASS |
| CXCR2 | Gi | alphai1 | 354 | 354 | 343 | 10 | yes | PASS |
| CXCR4 | Gi | alphai1 | 354 | 354 | 343 | 9 | yes | PASS |
| DRD2 | Gi | alphai1 | 354 | 354 | 343 | 9 | yes | PASS |
| DRD3 | Gi | alphai1 | 354 | 354 | 343 | 9 | yes | PASS |
| EDNRA | Gq | alphaq | 359 | 359 | 348 | 11 | yes | PASS |
| EDNRB | Gq | alphaq | 359 | 359 | 348 | 10 | yes | PASS |
| FSHR | Gs | alphas | 394 | 394 | 383 | 11 | yes | PASS |
| GHSR | Gq | alphaq | 359 | 359 | 348 | 8 | yes | PASS |
| GRPR | Gq | alphaq | 359 | 359 | 348 | 9 | yes | PASS |
| HRH1 | Gq | alphaq | 359 | 359 | 348 | 9 | yes | PASS |
| HRH3 | Gi | alphai1 | 354 | 354 | 343 | 9 | yes | PASS |
| LPAR1 | Gi | alphai1 | 354 | 354 | 343 | 10 | yes | PASS |
| LSHR | Gs | alphas | 394 | 394 | 383 | 9 | yes | PASS |
| LT4R1 | Gi | alphai1 | 354 | 354 | 343 | 11 | yes | PASS |
| MCHR1 | Gi | alphai1 | 354 | 354 | 343 | 11 | yes | PASS |
| NPY1R | Gi | alphai1 | 354 | 354 | 343 | 11 | yes | PASS |
| NPY2R | Gi | alphai1 | 354 | 354 | 343 | 11 | yes | PASS |
| OPRD | Gi | alphai1 | 354 | 354 | 343 | 9 | yes | PASS |
| OPRK | Gi | alphai1 | 354 | 354 | 343 | 10 | yes | PASS |
| OPRX | Gi | alphai1 | 354 | 354 | 343 | 11 | yes | PASS |
| OPSD | Gt | alphat | 350 | 350 | 339 | 10 | yes | PASS |
| OX2R | Gq | alphaq | 359 | 359 | 348 | 9 | yes | PASS |

`prefix-match len` is `cognate_len - 11` in every row, i.e. every position
before the α5-CT boundary matched exactly — confirming the scramble boundary
sits precisely at `N-11`, not `N-10` or `N-12`, for all 40 receptors. File
inventory also cross-checked: exactly 40 `*_decoy.fasta` files exist under
`refs/constructs_block_b/`, and their receptor-slug set is an exact 1:1
match (no extras, none missing) against the 40-receptor list in
`construct_build_report.md`.

## Anomalies

**None.** Zero deviations from expectation across all 40 receptors, all
checks, and the bonus checks (header-metadata cross-check, wrong-parent
fallback scan, hamming-category discrepancy check, multi-record scan).

## Sample walkthrough (3 receptors)

For each, the cognate parent sequence and decoy sequence are shown with the
α5-CT region isolated and character-by-character aligned. `.` = identical
position, `X` = differing position (scrambled). The non-tail region (not
shown in full — hundreds of residues) was confirmed byte-identical via the
`prefix_ok` check in the table above; only the tail alignment is shown here
for readability.

### 1. 5HT1B — cognate class Gi, parent `alphai1` (GNAI1, P63096), length 354

```
cognate α5-CT (positions 344-354): I K N N L K D C G L F
decoy   α5-CT (positions 344-354): C N L K D I L F G K N
diff mask                        : X X X X X X X X . X X   (hamming = 10)
```
- `Counter("IKNNLKDCGLF")` = `{I:1,K:2,N:2,L:2,D:1,C:1,G:1,F:1}`
- `Counter("CNLKDILFGKN")` = `{C:1,N:2,L:2,K:2,D:1,I:1,F:1,G:1}` — equal ✓
  (confirms a permutation of the same 11 letters, not a substitution)
- Cognate SHA-256: `57f8013fce15aa580c1c618f1fb4f45d76af5361d9190eb56bbbebf5997999d1`
- Decoy SHA-256:   `fcaf9cbb4d232da581fb41f8f855edcbaa818eb6c8e8cfd26ef67fcc15bc8af2`
  (differ, as expected — confirmed independently, not read off the decoy
  header's `sha=fcaf9cbb` field, though that field's prefix agrees)
- Positions 1-343: byte-identical (verified programmatically; both begin
  `MGCTLSAEDKAAVERSKMIDRNLREDGEKAAREVKLLLLGAGESGKSTIVKQMKIIHEAG...` and end
  the shared region `...QFVFDAVTDVI` immediately before the tail).

### 2. EDNRA — cognate class Gq, parent `alphaq` (GNAQ, P50148), length 359

(Note: EDNRA's *shuffled*-arm partner is G12 per the antagonist-swap rule in
`construct_build_report.md`, but the *decoy* arm always scrambles the
receptor's own cognate parent — Gq here — regardless of which class the
shuffled arm borrows from. Confirmed this is what's on disk: the decoy's
non-tail 348 residues match `alphaq`, not `alpha13`.)

```
cognate α5-CT (positions 349-359): L Q L N L K E Y N L V
decoy   α5-CT (positions 349-359): Q N Y E N L L K L V L
diff mask                        : X X X X X X X X X X X   (hamming = 11, maximum observed)
```
- `Counter("LQLNLKEYNLV")` = `{L:4,Q:1,N:2,K:1,E:1,Y:1,V:1}`
- `Counter("QNYENLLKLVL")` = `{Q:1,N:2,Y:1,E:1,L:4,K:1,V:1}` — equal ✓
- Every one of the 11 tail positions differs — still a valid permutation
  (a derangement), consistent with the build script's Hamming-≥5 floor and
  this receptor happening to land at the observed maximum of 11.
- Cognate SHA-256: `aae9e1c2493fd38402f4ff11436a321d9eae94449b07c61568995565cdcdefc0`
- Decoy SHA-256:   `584c8caf13d332a6abb41e2f80f4a24085ef64b888c0261dbd6fd2541095dcd2`

### 3. OPSD — cognate class Gt, parent `alphat` (GNAT1, P11488), length 350

(The only Gt receptor in the panel — checked specifically to confirm the
class→slug mapping table's Gt row (`alphat`, not accidentally `alphai1`
despite Gt/Gi visual/sequence similarity) is exercised correctly.)

```
cognate α5-CT (positions 340-350): I K E N L K D C G L F
decoy   α5-CT (positions 340-350): G D F C N K L L K E I
diff mask                        : X X X X X . X X X X X   (hamming = 10)
```
- `Counter("IKENLKDCGLF")` = `{I:1,K:2,E:1,N:1,L:2,D:1,C:1,G:1,F:1}`
- `Counter("GDFCNKLLKEI")` = `{G:1,D:1,F:1,C:1,N:1,K:2,L:2,E:1,I:1}` — equal ✓
- Position 6 of the tail (`K`, global position 345) is the single fixed
  point of this permutation — matches in both cognate and decoy, correctly
  contributing to hamming=10 rather than 11.
- Cognate SHA-256: `61cc7bb7a310e3f27cba5c004577361eb07c1791de6527a97f7e762001a67157`
- Decoy SHA-256:   `450ca3732c84a96906a2e86ff0843eceb94b465225769af2fe487586821ee7eb`

## Conclusion

The decoy α5-CT scramble is confirmed **surgical** for all 40 Block B
receptors: the scramble touches exactly the last 11 residues of each
receptor's correctly-identified cognate Gα parent, is a true permutation
(composition-preserving) in every case, clears the intended Hamming floor,
and leaves the remaining ~340-383 residues of each Gα byte-identical to the
canonical parent in `partners.fasta`. No accidental byte-flip, mid-sequence
permutation, header/file corruption, or wrong-parent mapping was found
anywhere in the 40-decoy set. Block B Wide can proceed on this artefact
without a scramble-mechanism concern.
