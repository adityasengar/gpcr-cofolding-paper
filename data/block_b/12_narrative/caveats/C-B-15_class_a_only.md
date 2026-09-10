# C-B-15 — Block B runs Class A only (40 receptors)

## Caveat

Block B's panel is 40 Class A receptors × 4 backbones × 4 arms
{apo, decoy, shuffled, cognate} × 5 seeds × 10 samples = 32,000 rows.
**Class B and Class F receptors are not in Block B.**

Class A stratum is the same 40 receptors present in Block A's Class A
stratum (Block A panel of record: 48 receptors = 40 Class A + 4 Class
B + 4 Class F per CLAUDE.md and `refs/gpcr_coupling.csv`).

**Class B/F omission is scoped**, not accidental:

- Class B secretin receptors use Wootten numbering (BW 2.46 / 6.37 not
  defined). The Class A two-instrument predicate does not translate.
- Class F Frizzled/Smoothened receptors have a different Gα-coupling
  geometry (dimer-interface activation for Class C is a further-out
  case); the α5-CT-tail construct-family framework does not apply the
  same way.
- Class-B/F expansion of Block B was deferred at dispatch time
  (`docs/BLOCK_B_DISPATCH_PLAN_2026_09_02.md`).

## Why it matters

- The 4 all-NaN NPxxY receptors in Block B (EDNRA, EDNRB, GRPR, HRH3;
  see C-B-5) are all Class A — their 7.53 is L not Y (intrinsic
  biology, not a class artefact).
- Any panel-level claim in Block B is a Class A claim; the manuscript
  must not accidentally extend to Class B/F.
- Block A's Class B / Class F caveats (Block A C-2, C-3) do not carry
  over — Block B has no Class B/F to make them relevant.

## Affects

- Every SC-B-* claim. Scope is Class A only.

## Manuscript sentence

> Block B's panel is 40 Class A receptors. Class B (secretin) and Class
> F (Frizzled/Smoothened) receptors are not in the Block B panel; the
> α5-CT construct-family framework used here is Class A-scoped. Class B
> and Class F results from Block A are not re-tested in Block B.

## Related

- Block A caveat C-2 (Class B tilt ceiling) — does not apply to Block B.
- Block A caveat C-3 (Class F weak predicate) — does not apply to Block B.
- `docs/BLOCK_B_DISPATCH_PLAN_2026_09_02.md`.
