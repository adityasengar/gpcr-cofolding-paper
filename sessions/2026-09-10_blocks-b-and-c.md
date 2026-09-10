# 2026-09-10 — Blocks B and C landed, ten panels built, and four self-certifying columns

## What happened

Started with the graphical-abstract decision pending. Ended with **three blocks
written into the manuscript**, ten figure panels built, a mechanical number
sweep, and two rebuttal documents ready to send upstream.

- **Block A cleanup.** Fixed seven places where our own discrepancy report was
  wrong or overstated. Corrected the Methods predicate positions (we had named
  the ionic-lock pair 3.50/6.34 instead of GPCRdb 2×46/6×37). Added thirteen
  exclusion checks so the row counts stopped being unchecked — Block A's
  verifier went 34 → 47 checks.
- **Block B landed, verified, written.** 91 → 109 checks; 21 mismatches in 8
  groups. Results (1,220 words) and Methods (598 + 130) into `.tex`. Six
  standalone panels, BB-1..BB-6.
- **Block C landed, verified, written.** 53 of 53 reproduce — but only 23 are
  recomputed and 30 are consistency-only, because the block ships one row-level
  file. Results (957 words), Methods (515), limitations, open questions, claim
  trace. Four panels, BC-1..BC-4.
- **Two lit collaborations.** A claim audit on the two-instrument predicate, and
  a panel-expansion query that produced 19 Class A receptors with PDB pairs.
- **Machinery.** `analysis/sweep_manuscript.py` + `NUMBER_REGISTRY.md`;
  `rebuttals/` with a three-section convention; `figures/block_b/badata.py` and
  `figures/block_c/bcdata.py`, both of which encode the traps rather than
  documenting them.

## Decisions Aditya made, with their reasons

- **Prose goes into the manuscript, not into markdown drafts**, even where a
  block's dispatch asks for `BLOCK_X_RESULTS.md`. Those dispatches were written
  for agents with no repo access. Block A established that a section living
  outside the paper is a section the paper does not have.
- **Figures follow each dispatch exactly** — standalone panels, spec IDs,
  `[FIG:*]` placeholders, no manuscript figure numbers, no main-versus-SI call.
- **The figure budget is deferred to Block C** — now landed, so the call is
  available. Reason: allocating across two blocks when four exist is a decision
  that would only have to be made twice.
- **Demote a superseded figure to SI only if it is still true.** If it was
  replaced *because it was wrong*, delete it with a line in the ledger. A
  superseded panel in the SI is worse than no panel, because SI figures get
  cited.
- **The distributional reframing is parked**, not dropped, with its evidence in
  `HANDOVER.md` and `analysis/block_b/seed_variance.py`.
- **Class A only** for the panel-expansion list.

## What the verification found

**Four self-certifying columns, one per block and one twice.** Block A's
`matches_claim_sheet`; Block B's `matches_claim_sheet_bool` vouching for eight
continuous medians that reproduce from nothing; Block B's per-backbone family
shares with the panel figure copied into three of four slots; and Block C's
SC-C-2 table headed "Kendall's τ" while containing a fraction of receptors.

**The fourth was caught by drawing it.** It had passed the claim sheet, the
dispatch, and our own Results. BC-2's violins sat at 0.3 against printed values
of 0.74. **A figure is a verification step, not a presentation step** — that is
the durable lesson of this session.

**Two title clauses have no evidence in any block.** No arm anywhere supplies a
21-residue peptide or an agonist. `ligand_type` is NaN on all 32,000 Block B
rows; Block A has no ligand column at all.

**The panel is a subset, not a census.** ConfoRNets counts 51 both-state
receptors under a *stricter* rule; GPCRdb has 86. We have 40.

**4X1H, our own OPSD active reference, is rhodopsin bound to the α5-CT peptide
of Gαt alone.** The only peptide-bound entry among 80 references, and the
experimental precedent for the paper's title claim — sitting unremarked in our
own data while both campaigns supply whole subunits.

## What I got wrong and corrected

Ten this session. The pattern is now consistent enough to be the finding:
**on every block, my first run was wrong before the drop was.**

- Asserted "there is no ceiling-pinning flag anywhere in the drop" — there is,
  in a file I had not grepped. Concluded from one file that a thing did not
  exist in eighty-three.
- Wrote "28–29 pinned cells per backbone" in three places including the
  manuscript; my own script had printed 29/28/24/34 and I transcribed the first
  two.
- Wrote "0.002 Å cannot move a call". It moves five, and one of them flips a
  cell from 0.90 to 0.88. Found by BB-1's guard on its first run.
- Six decomposition checks **silently did not run** behind an `if len(...)`
  guard, because the frame label is `reproduction_36` in one file and `frame_36`
  everywhere else. The report listed them under "what reproduces".
- Copied SC-C-2's mislabelled "Kendall's τ of 65–87%" into the Results.
- Assumed Block C's off-site band began at 8 Å when it begins at 15 Å; filtered
  small-molecule rows by role name when peptide agonists sit inside
  `full_agonist`; read CIs at the wrong JSON depth; guessed key names instead of
  reading the file's own `thresholds` block.
- Said three of Block C's four panels could not be built. All four built.
- Published a page locator (`p.~2`) inferred rather than sourced, and caught it
  before the build.

## What the next session should not redo

- **Do not re-verify the blocks.** Three verifiers exist and run clean:
  `analysis/block_{a,b,c}/verify_claims.py`. Mismatch counts are expected and
  documented — 15, 21 and 0 respectively.
- **Do not rebuild the panels.** Ten exist with provenance files.
- **Do not re-derive the exclusion semantics.** Both loaders address exclusion
  sets by meaning and refuse E-B-n labels; the claim sheet mislabels three of
  four.
- **Do not re-ask lit about the predicate conjunction or the panel gap.** Both
  answered, both in `rebuttals/`.
- **Do not attempt the W-C-5 14.5% reconciliation.** The dispatch forbids it and
  the coincidence is recorded.
