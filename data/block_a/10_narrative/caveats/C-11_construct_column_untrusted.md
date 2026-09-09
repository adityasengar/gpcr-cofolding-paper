# C-11 — The `construct` column in reference_set.csv is corpus-wide untrusted

## Caveat

The `construct` column in `panel/refs/reference_set.csv` records what the
crystallographer called the receptor's construct — nominally "wt" (wild
type) or something like "T4L_ICL3". T4 audited this column against RCSB's
authoritative `pdbx_mutation` metadata and found:

- **52 / 127 evaluable PDBs (40%)** have `construct = wt` on-disk contradicted
  by RCSB (RCSB reports engineered receptor mutations)
- **41 / 127 (32%)** after excluding 11 refs with the recurring
  `{S47N, G203A, E245A, A326S}` mini-Gs fusion signature that RCSB
  incorrectly attributes to the receptor entity in mini-Gs-fused constructs

**Two specific mutations that matter for Block A's predicate windows**:
- **CNR2 5ZTY inactive**: R242E (BW 6.30 exact — INSIDE tilt window). Confirmed by RCSB. Post-review annotation fixed to `multi_mutation_incl_R242E_tilt_window` (see `POST_REVIEW_ANNOTATIONS.md`).
- **CNR1 5XRA active**: R340E (BW 7.53 exact — INSIDE NPxxY window). Not previously flagged.
- **AGTR1 6OS2 active**: BRIL insertion at 227–229 (ICL3, adjoining TM6; per T4's rough tilt-predicate residue-range window 220–265). Not previously flagged.
- **CCR5 5UIW inactive** (T5's original re-anchor candidate for CNR2): A233D + K303E receptor mutations + fusion 224–226, all in predicate windows.

**Corpus-wide scope**: the audit was on 127 of 167 total reference-set PDBs.
40 PDBs' `_entry.json` was fetched in the freeze batch but their per-PDB
`polymer_entity` mutation data was NOT (out of budget). If the 32–40% rate
holds on the remaining 40, expected ~13–16 additional contradictions. **T4's
authoritative rate is 52/127 on 76% coverage.**

## Two denominators — reconcile

- **89 unique PDBs** for the 48-receptor Block A panel (per C-6). This is
  the panel-only reference count that appears in Methods.
- **167 unique PDBs** in `refs/reference_set.csv` (T4's total). This
  includes off-panel refs used by other blocks.
- **127 evaluable** (76% cache coverage) is the audit denominator T4 used.

The `construct` contradiction rate applies to the audit denominator (127);
panel-only rate (of 89) may be higher or lower depending on which of the
52 are panel-relevant. This has not been broken out.

## Affects

- Any manuscript sentence relying on the `construct` column for a
  wild-type claim across the reference set. There is no wild-type
  guarantee for 32–40% of the references.
- Widened-O-4 audit was requested by the scientific review as Flag 14; T4
  did the deposit-date + fusion audit but did NOT complete the mutation
  audit on all 167 PDBs. Corpus-wide `construct`-column repair is a
  deferred limitation (MANUSCRIPT_FLAGS.md Flag 42).

## Manuscript sentence

> The `construct` annotation column in the reference set records the
> deposited protein-only construct type and does not distinguish
> wild-type-observed sequences from wild-type-plus-engineered-mutations
> that reach the modelled polymer entity. An RCSB-based audit (T4)
> found 52/127 = 40% of evaluable PDBs' `construct = wt` values are
> contradicted by RCSB `pdbx_mutation` metadata (32% excluding a mini-Gs
> fusion signature that RCSB attributes to the receptor entity). Specific
> corrections for Block A analyses are logged in
> `POST_REVIEW_ANNOTATIONS.md`; the wider corpus-repair is a deferred
> limitation.

## Related

- MANUSCRIPT_FLAGS.md Flag 14 (inactive-reference construct audit, review original)
- MANUSCRIPT_FLAGS.md Flag 42 (construct column corpus-wide untrusted; this caveat is the substance)
- T4 fork report
- `panel/refs/POST_REVIEW_ANNOTATIONS.md` for the specific edits made
