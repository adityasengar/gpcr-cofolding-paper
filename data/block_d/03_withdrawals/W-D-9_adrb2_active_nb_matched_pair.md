# W-D-9 — ADRB2 as "matched-pair receptor" for D2's arm-by-arm 2×2

## Claim as previously stated

PREREG §D-2.2 named ADRB2 as the sole matched-pair receptor in the D2
panel, with all 4 arms: apo, cognate_gα, active_nb (4LDE / Nb80), and
inactive_nb (5JQH / Nb60). Anticipated as the receptor with a clean
matched-anchor 2×2 (arm × state-target).

## Retraction

**Withdrawn as-drafted.** ADRB2's active_nb arm was **intentionally
dropped** from the D2 dispatch: the Nb80 slot in the manifest was
occupied by the 126-aa `partners.fasta:Nb60` mislabel (which is
actually Nb80 sequence, per CDR3 verification) — a collision the
manifest builder's guard raised and the dispatch honored by dropping
the arm rather than firing a self-collision.

Per auto-memory `block_d_d2_nanobody_collision_2026_09_09.md` and
GATE-1, ADRB2's inactive_nb arm was NOT contaminated — 200 rows across
4 backbones consumed real 125-aa Nb60_5JQH per row-hash audit. That
data is scientifically clean.

**ADRB2 contributes 3 arms, not 4**: apo, cognate_gα, inactive_nb.
The matched-pair 2×2 framing must name the drop, or the shape becomes
a 3-arm receptor comparison rather than a 4-cell 2×2.

## Basis

- `dossiers/BLOCK_D/gates/GATE_1_D2_NB_SHA.md` — GATE-1 row-hash audit.
- Auto-memory `block_d_d2_nanobody_collision_2026_09_09.md` — collision + drop provenance.
- `experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv` — 0 rows on ADRB2 active_nb; 200 on inactive_nb.

## What the manuscript should say instead

Report ADRB2's D2 result as a 3-arm receptor (apo, cognate_gα,
inactive_nb) with a footnote naming the intentional active_nb drop.
Do NOT report ADRB2 as "the matched-pair receptor" without the caveat.

Future work: curate real Nb80 into `refs/nanobody_sequences.fasta`
under an unambiguous key and dispatch the missing ADRB2 × active_nb ×
4bb × 5 seeds × 10 samples = 200 preds cell — see §6.6-5 (parked).
