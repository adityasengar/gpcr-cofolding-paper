# C-D-10 — D2 n=4 receptors is a small panel; F3 rests on 2

## Caveat

D2 canonical panel size: 4 receptors (ADRB2, ACM2, AGTR1, OPRK). Of
these, only 2 receptors have inactive-Nb arms in the dispatch:

- **ADRB2** × inactive_nb (5JQH/Nb60) — 200 rows across 4 backbones.
- **OPRK** × inactive_nb (6VI4/Nb6) — 200 rows across 4 backbones.

(ACM2 has only active_nb 4MQS/Nb9-8; AGTR1 has only active_nb
6OS2/Nb.AT110i1_le.)

**F3 (SC-D-6, "inactive-directing Nb is unreliable") rests on n=2
receptors × 4 backbones = 8 cells.** Panel-scale generalisation
from n=2 is fragile. The direction of the finding is
receptor-independent per the OPRK unanimous_up direction pattern,
which is informative, but any manuscript claim that generalises
across the receptor class needs the "n=2 receptors" caveat named.

A third inactive-Nb receptor (CCR5 has known inactive-Nb-bound
crystal structures; would need curation ceremony) would strengthen
F3's cross-receptor robustness. Named as ANV.

Also relevant: the panel size limits the effective test of the
Nb-B-as-active prior (F4, SC-D-7). Protenix's ADRB2 × inactive_nb
76 % active is a strong single-cell finding but resurfaces only on
the 1 receptor + backbone combination where it fires.

Joint-review §6.6-5: "Nb80 curation to un-drop ADRB2 active_nb +
third inactive-Nb receptor" both parked as future work.

## References

- `dossiers/BLOCK_D/EXPERIMENT_DOSSIER_BLOCK_D.md` §SC-D-6, §SC-D-7.
- `dossiers/BLOCK_D/partA/PARTA_D2.md` §4a (F3 dual framing).
- `refs/tier_d2_panel.csv` (panel of record).
- `refs/nanobody_state_anchors.csv` (anchor curation notes).
