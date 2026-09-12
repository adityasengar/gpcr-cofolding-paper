# Named reference exclusions

Landed 2026-09-04 by Block C Step 1 sidecar merge (subagent 1.6). This
file enumerates every (receptor × ligand-state) for which
`refs/reference_set.csv` intentionally carries **no reference PDB**.
Downstream scorers (`scorer/pocket_metrics.py::compute_pocket_axes_bundle`)
that request the missing reference will emit `NaN` for `ligand_rmsd_to_ref`
and `pocket_ca_rmsd` (unless a same-receptor active reference is
usable as a proxy for `pocket_ca_rmsd`). This is **by design**, not
data-hunt-later work.

## Class-A receptors with no antagonist-side reference

### 5HT1B — no clean neutral-antagonist crystal

No usable neutral-antagonist or inverse-agonist crystal exists for
5HT1B in the PDB. Every 5HT1B inactive-side entry (4IAR, 4IAQ, 5V54,
6G79, 7C61) is bound to ergotamine or a related ergot alkaloid, all
of which are **partial agonists** at 5HT1B, not neutral antagonists.
Coordinator resolved via option (c) — `ligand_rmsd_to_ref = NaN` on
antagonist and inverse-agonist ligand states; 5HT1B remains in the
Tier 1 panel as a non-discriminator control per Block-C plan §3.3.

- Panel role in Block C: non-discriminator control (family term 0.00).
- `pocket_ca_rmsd`: computable against 5HT1B active reference 6G79
  (mini-Gα-stabilised) for the agonist and apo ligand states.
- `ligand_rmsd_to_ref`: **NaN** on antagonist and inverse-agonist
  ligand states.

Source: A2 curation notes 2026-09-03, Block-C stop-report accepted.

### GLP1R — Class B secretin, dropped from Tier 1 panel

GLP1R was dropped from the Tier 1 antagonist panel in Block C Step 1.5.
The only inactive-side GLP1R crystal (5VEW) carries the negative
allosteric modulator PF-06372222 bound outside the orthosteric peptide
pocket — using it as an antagonist orthosteric reference would poison
`ligand_rmsd_to_ref`.

- Panel role in Block C: not in Tier 1 antagonist panel.
- `ligand_rmsd_to_ref`: **NaN** on neutral-antagonist and
  inverse-agonist ligand states.
- `pocket_ca_rmsd`: computable against active GLP1R reference 6X18
  (native Gs heterotrimer) for the agonist and apo ligand states.

Source: Block-C plan Step 1.5.

## Class-A receptors with neutral-antagonist reference but no inverse-agonist crystal

For these receptors the sidecar landed a **neutral-antagonist** reference
but no inverse-agonist crystal exists in the PDB. `ligand_rmsd_to_ref`
on the inverse-agonist ligand state is **NaN** by design.

| Receptor | Neutral-antagonist reference | Inverse-agonist state |
|---|---|---|
| DRD3 | 3PBL (eticlopride) | NaN — no inverse-ag crystal exists |
| ACM4 | 5DSG (tiotropium) | NaN — no inverse-ag crystal exists |
| OX2R | 5WQC (suvorexant) | NaN — no inverse-ag crystal exists |
| AA1R | 5UEN (DU-172, covalent) | NaN — no inverse-ag crystal exists (5N2R is A2AR, not A1R) |

Source: A2 evidence log, `experiments/020_block_c_ligand_pharmacology/analysis/refpdb_curation_notes.md`.

## Class-A receptors with sidecar row above existing inactive on d_tm6

Landed but flagged for coordinator review at Block C interpretation
time — the receptor's inactive reference has an unusual d_tm6 span:

| Receptor | Sidecar PDB | d_tm6 (Å) | Existing inactive PDB | d_tm6 (Å) | Note |
|---|---|---:|---|---:|---|
| ADA1A | 7YMJ (tamsulosin, Nb6-stabilised) | 18.13 | 8HN1 (AdTx1 toxin, nanobody) | 16.89 | ADA1A has no active-side reference in `refs/reference_set.csv`; span-inversion cannot be computed against active-side. Both inactive references sit high on the d_tm6 axis relative to other Class A inactive references (typical 7-11 Å). 7YMJ has small-molecule antagonist (tamsulosin) so is preferred over 8HN1 for `ligand_rmsd_to_ref`. Interpretation of ADA1A results should note this. |

## Convention

Every "NaN by design" case above must be **excluded** from cross-receptor
pocket-metric distribution reports; downstream analysis code should
filter on `role_specific IS NOT NULL AND ligand_rmsd_to_ref IS NOT NULL`
before computing distributional statistics for the antagonist-side
Block-C metrics.

## Provenance

- Coordinator decision: Block-C plan §3.3 (5HT1B option (c)), §1.5 (GLP1R
  drop), A2 evidence log (DRD3 / ACM4 / OX2R / AA1R inverse-ag absence).
- Landed by: subagent 1.6, Block C Step 1 pre-dispatch remediation
  (2026-09-04).
- Sidecar source: `refs/pending_curation_block_c.csv` — 21 rows, 19
  receptors, all merged.
- Merge log: `experiments/020_block_c_ligand_pharmacology/analysis/sidecar_merge_2026_09_04.md`.
