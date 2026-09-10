# C-B-11 — AGTR1 6OS2 + CNR2 5ZTY annotation refinements (both invert on Block C classifier)

## Caveat

Two Block B receptors have references whose annotations were refined at
commit `cda27e2` after Block B ran. Neither refinement shifts a PDB ID
or a numeric column; both alter reader interpretation.

### CNR2 5ZTY

- `active_stabilization_source`: unchanged.
- `construct`: `wt` → `multi_mutation_incl_R242E_tilt_window`.
- R242E is a charge-reversal at BW 6.30 — one of the two anchors the
  GPCRdb TM6 tilt is measured between (2.46 ↔ 6.37 CA).

**Consequence**: a reference whose tilt-measurement window is chemically
perturbed is not measuring what the Class A panel assumes. CNR2 was
identified in the campaign as inverting on the Block C classifier
across all four backbones (auto-memory
`chai_cnr2_apo_model_bias_2026_09_06.md`).

### AGTR1 6OS2

- `active_stabilization_source`: `nanobody` → `nanobody_beta_arrestin_biased_agonist`.
- The peptide TRV026 in the structure is β-arrestin-biased; the previous
  annotation obscured the biased-agonist context.

**Consequence**: interpretive shift only; AGTR1 6OS2 remains
nanobody-stabilised and the PDB assignment is correct. AGTR1 is called
inverting on the Block C classifier for the same underlying
biased-agonist reason.

## Why it matters

- Block B was scored against the **pre-correction** annotation
  (`6ee2cad8` bytes carry the older `construct=wt` on CNR2 and the
  older `stabilising_elements=nanobody` on AGTR1). Post-run annotation
  refinements do not force a rescore because they alter no PDB and no
  numeric column.
- Two of the receptors that invert on the Block C classifier have
  references whose annotations mattered for the interpretation. This
  is a Block-C-facing finding surfaced during the Block B reference
  audit, not a Block B invalidator.

## Affects

- SC-B-13 (reference audit clean).
- The recurrent-anomaly framing in the Discussion (both AGTR1 and CNR2
  are Block C classifier inverting cases).

## Manuscript sentence

> Two Block B receptors have references whose annotations were refined
> after Block B ran: CNR2 5ZTY's `construct` field changed from `wt` to
> `multi_mutation_incl_R242E_tilt_window` (R242E at BW 6.30 lies
> inside the tilt-measurement window) and AGTR1 6OS2's
> `active_stabilization_source` changed from `nanobody` to
> `nanobody_beta_arrestin_biased_agonist`. Neither refinement changes
> a PDB assignment or a numeric column; both were committed at
> `cda27e2` after Block B's rescore. Block B was scored against the
> pre-correction annotation, so downstream interpretation of these two
> receptors' reference geometry must route through the refined
> annotations.

## Related

- MANUSCRIPT_FLAGS.md (Flag B-6 preload).
- Phase 0 addendum §"AGTR1 + CNR2 pre-loaded deviations for Phase 6c".
- Phase 6c §Named Block A / Block B receptor deviations.
- Block A caveat C-11 (`construct` column corpus-wide untrusted;
  40 % of evaluable PDBs).
