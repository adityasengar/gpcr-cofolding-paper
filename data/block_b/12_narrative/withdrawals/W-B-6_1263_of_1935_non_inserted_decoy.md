# W-B-6 — "1,263 of 1,935 non-inserted decoy rows make > 20 contacts"

## Claim as previously stated

Dispatch narrative cited a specific pair: **1,263 of 1,935 non-inserted
decoy rows** (~65%) carry > 20 interface contacts, supporting the
"occupancy without insertion" reading of the decoy arm.

## Retraction

**Withdrawn as an exact reproducible pair on the delivered 32,000-row
corpus.** Phase 4b non-inserted decoy check on the final Block B rows.csv:

| frame | denominator (non-inserted decoy) | > 20 contacts | > 30 contacts |
|---|---:|---:|---:|
| frame_40 (tip ≥ 20 Å) | 2,398 | 1,623 (67.7%) | 1,253 (52.3%) |
| frame_36 (tip ≥ 20 Å) | 2,133 | 1,427 (66.9%) | — |

**The (1,263, > 30) count is close numerically to 1,263 but the
1,935-denominator is not reproducible.** Most likely the cited pair
counted at a mid-Phase-2 pre-drop layer of the corpus (before all silent
fails and OF3 recoveries landed).

## What supersedes it

Restate the figure as **1,623 of 2,398 non-inserted decoy rows carry
> 20 interface contacts (frame_40; 1,427 of 2,133 in frame_36)**.
Story unchanged: a majority of non-inserted decoys still make substantial
receptor contact — occupancy is present without insertion.

## What the manuscript should say instead

> "Of the 2,398 non-inserted decoy rows (frame_40, tip ≥ 20 Å from
> R3.50 Cα), 1,623 (68%) carry > 20 receptor interface contacts,
> and 1,253 (52%) carry > 30. A majority of decoy rows that do not
> insert into the cavity still make substantial receptor-face contact
> — occupancy without insertion is the dominant decoy behaviour."

## Evidence

- `docs/BLOCK_B_DOSSIER_PHASE_4_INTERFACE_GEOMETRY.md §4b` (non-inserted decoy check on final corpus).
- Source CSV: `interface_2x2.csv` and derived counts.

## Related

- MANUSCRIPT_FLAGS.md Flag B-13.
- SC-B-3 (2×2 engagement × activation).
- C-B-6 (engagement-cutoff sensitivity — the "non-inserted" set is
  cutoff-defined at 20 Å).
