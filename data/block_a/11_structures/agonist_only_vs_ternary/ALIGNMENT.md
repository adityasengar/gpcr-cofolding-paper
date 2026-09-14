# agonist_only_vs_ternary — OPRD 6PT2 (agonist-only, BRIL) vs DOR-Gi complex

## Files
- `6PT2.cif` — δ-opioid (OPRD) active, BRIL-stabilised, no G-protein.
  Both Y5.58 OH and Y7.53 OH resolved; NPxxY-OH = 16.75 Å (honest geometry).
- `8FZQ.cif` — 8FZQ (δOR–Gi complex).

## Purpose
Show that OPRD's "active" reference lacks a transducer and lacks the tight
Y5.58–Y7.53 packing that the campaign's active predicate rewards. This is
the E5 rationale: agonist-only actives fail the NPxxY predicate by construction.

## OPRD numbering (uniprot P41143)
- Y5.58, Y7.53 positions to be extracted from CIF header residue numbering.
- BW anchors: 3.50 = R131, 5.58 = Y226 (varies by paralog),
  6.30 = R241, 7.53 = Y308 (verify against structure).

## Superpose on
Receptor Cα only, chain A. Exclude BRIL (fusion partner on 6PT2, typical
residue range 220–265 in inserted chain).

## Measured values
6PT2 OH-OH distance ≈ 16.75 Å (from reference_set.csv: `d_npxxy_oh_ref`
for OPRD active).
