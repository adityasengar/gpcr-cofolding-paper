# Block D — post-cutoff inactive-Nb search record

Kept as a standing note so this search isn't repeated blind. Four
candidates were evaluated for disambiguating SC-D-6 (C-D-12) from a
memorization-availability confound. None was adopted.

## 9PXU — human MOR + Nanobody6 (2025-08-06)
Genuinely post-cutoff, genuinely a state-directing nanobody (Nb6 is an
independently published conformational-state reagent, originally
characterized on kappa opioid receptor). Two open issues stopped adoption:
(a) shares CDR1 + CDR2 with the D2 panel's own Nb6 (6VI4) — 87% framework
overlap — so it disambiguates memorization-of-exact-structure but not
memorization-of-nanobody-family; (b) deposited as a single 622-aa fused
chain (BRIL + MOR + Nb6), requiring verified residue-boundary parsing
before use as a two-chain prediction input, which was not completed. A
verified human MOR active reference was separately sourced (8EFQ, Cell
2022, confirmed human) for whichever future attempt picks this back up.

## 9HB3 / 9HAP — vasopressin V2R + "Mambaquaretin1" (2024-11)
**Disqualified.** Mambaquaretin1 is not a nanobody — it's a 57-residue
Kunitz-fold snake-venom toxin, unrelated in fold and origin to an
immunoglobulin domain. The Nb chain actually present in this deposition is
a generic anti-BRIL-Fab fiducial marker used for cryo-EM particle
alignment, not a state-directing reagent. This candidate does not test
nanobody-mediated steering at all.

## 9EKH / 9EE5 — prostaglandin DP1 + Nb + Fab (2024-11/12)
**Disqualified.** Same fiducial-Nb pattern as V2R (anti-bRIL Fab + anti-
Fab nanobody, standard cryo-EM scaffold). State determinant is
ONO3030297, a small-molecule inverse agonist.

## 9EHS — adenosine A3AR + Nb + Fab (2024-11)
**Disqualified.** Same pattern again (anti-BAG2 nanobody, explicitly
described in the source paper as a fiducial marker). State determinant is
LUF7602, a covalent small-molecule antagonist. Also one step less novel
regardless — same adenosine family as Block C's landed AA2AR.

## Reusable filter for future searches
An `Nb` chain in a GPCR cryo-EM deposition paired with `BRIL` or `Fab` in
the same construct is presumptively a scaffolding aid, not a
pharmacological partner, until the paper's own text confirms otherwise.
Three of four candidates found here fell into this trap.

## Disposition
Not pursued further for this manuscript. §6.5 reports the active/inactive
asymmetry as demonstrated only in the active direction, with this
limitation stated rather than resolved. Revisiting this is future work: a
clean test needs a post-cutoff, non-fiducial, non-cousin state-directing
nanobody on a novel receptor family — none of the four candidates checked
here satisfied all three.
