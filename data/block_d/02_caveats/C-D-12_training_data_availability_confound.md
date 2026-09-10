# C-D-12 — Training-data-availability confound on D2 F3 (inactive-Nb unreliable)

## Caveat (LOCKED 2026-09-10)

All evidence for SC-D-6 (inactive-directing nanobody unreliable) comes from pre-training-cutoff reference structures (5JQH, 6VI4); memorization-availability is not distinguished from a genuine directional-steering limit. A search for a disambiguating post-cutoff test case was conducted and is documented in full at `paper_af3_release/dossiers/BLOCK_D/BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md`. No candidate was adopted; the test was not run for this manuscript. Stated as an open limitation, not a resolved question.

## Context — the two hypotheses the test would have separated

All four D2 Nb-anchor reference structures used in the dispatch predate model training cutoffs on all four backbones:

| Nb anchor | PDB | Deposited | Cutoff status |
|---|---|---|---|
| Nb60_5JQH | 5JQH | 2016-05-05 | pre-cutoff on all 4 bb |
| Nb6_6VI4 | 6VI4 | 2020-01-11 | pre-cutoff on all 4 bb |
| Nb9-8_4MQS | 4MQS | 2013-09-16 | pre-cutoff on all 4 bb |
| Nb.AT110i1_le_6OS2 | 6OS2 | 2019-05-01 | pre-cutoff on all 4 bb |

Earliest confirmed training cutoff: Chai-1 2021-01-12. All four Nb anchors are 2013–2020 depositions. Boltz-2 (2023-06-01), Protenix v2 (2021-09-30), and OF3 (TBD) also saw these anchors during training.

**Consequence for SC-D-6 (F3: inactive-Nb unreliable)**: the negative finding cannot currently be distinguished from a training-data-availability effect. Two competing hypotheses:

1. **Directional-steering limit** (what F3 is drafted to say): models can drive receptors to active via cognate Gα + active-Nb, but not reliably to inactive via inactive-Nb. This is a limitation of partner-mediated state-steering.
2. **Memorization / training-data availability**: models "recognise" the co-deposited state and reproduce it because they saw the exact (receptor + Nb + state) complex during training. An inactive-Nb that co-crystallised with an inactive state gets recalled as inactive-flanked-by-Nb-in-training, not as Nb-directs-inactive.

## Disposition

Test not dispatched for this manuscript. Search record for the four candidates evaluated + reusable filter rule for future attempts at `dossiers/BLOCK_D/BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md`. The dossier §6.5 framing paragraph is LOCKED and reports the active/inactive asymmetry as demonstrated in the active direction only, with this limitation stated rather than resolved.

## References

- `dossiers/BLOCK_D/BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md` — search record + reusable filter rule.
- `dossiers/BLOCK_D/BLOCK_D_S2_4_POST_CUTOFF_SCOPING.md` — full v3 scoping report (retained as audit trail; the search-note is the distilled reference).
- `dossiers/BLOCK_D/partA/PARTA_D2.md` §8 (training-cutoff analysis on D2 anchors).
- `refs/nanobody_state_anchors.csv` — Nb-anchor deposition dates + cutoff columns.
- `dossiers/BLOCK_D/EXPERIMENT_DOSSIER_BLOCK_D.md` §6.5 — final Discussion text (locked).
