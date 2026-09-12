# GNAT1 vs GNAI1 α5-CT diff — Block A OPSD substitution

Purpose: quantify the mechanism-level impact of replacing the previously-used Gαi1 proxy (P63096) with the real Gαt/transducin (P11488) sequence for OPSD in the Block A cognate arm.

Sources: UniProt P11488 (GNAT1_HUMAN, 350 aa, sha256[:8]=`61cc7bb7`), UniProt P63096 (GNAI1_HUMAN, 354 aa).

## Full C-terminal 21-mer (α5-CT) alignment

Numbering convention: position index runs N→C over the 21-mer; the C-terminal residue is position 21, per audit spec.

```
α5-CT position (N→C)         1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21
GNAT1  (P11488)              F  V  F  D  A  V  T  D  I  I  I  K  E  N  L  K  D  C  G  L  F
GNAI1  (P63096)              F  V  F  D  A  V  T  D  V  I  I  K  N  N  L  K  D  C  G  L  F
match                        =  =  =  =  =  =  =  =  X  =  =  =  X  =  =  =  =  =  =  =  =
```

## Position-by-position mismatches

Using α5-CT-relative numbering (C-terminal residue = position 21, counting back):

| α5-CT position | GNAT1 | GNAI1 | Category | Chemistry note |
|---:|:-:|:-:|---|---|
| 13 | **E** | **N** | non-conservative (acidic ↔ amide) | Net charge lost (−1 → 0); H-bond donor/acceptor pattern altered; side-chain length nearly identical. |
| 9  | **I** | **V** | conservative (β-branched aliphatic ↔ β-branched aliphatic) | Both hydrophobic; volume difference ≈24 Å³ side chain (Ile > Val by one methyl). |

Positions 1–8, 10–12, 14–21 are **identical** between GNAT1 and GNAI1.

## Chemistry-claim residues (L15 / E19 / L21)

Per mechanism convention using α5-CT-relative numbering (position 21 = C-terminal):

| Position | Gαs reference | GNAT1 (Gt) | GNAI1 (Gi) | GNAT1 vs GNAI1 |
|---:|:-:|:-:|:-:|:-:|
| 15 | L | L | L | identical |
| 19 | E | G | G | identical (class-level Gs-vs-Gi/t difference; not affected by proxy swap) |
| 21 | L | F | F | identical (class-level Gs-vs-Gi/t difference; not affected by proxy swap) |

## One-line summary

**2 substitutions in the last 21 residues of GNAT1 vs GNAI1, 0 of which fall on the L15/E19/L21 chemistry-claim positions.**

## Sensitivity implication for OPSD Block A

Both mismatches (α5-CT positions 9 and 13) sit **outside** the three positions the mechanism claim is built on. The α5-CT residues that make the receptor-Gα contact discriminating Gs vs Gi/t/o (L15, E19, L21) are **byte-identical** between GNAT1 and GNAI1. Under the mechanism model where coupling specificity is dominated by α5-CT positions 15/19/21, swapping the Gαi1 proxy for the real Gαt should produce a **near-zero** shift in the predicted α5-CT-receptor interface — differences would come from bulk Gα (Ras-like domain / helical domain) or the mid-α5 pos-9/pos-13 residues, not from the mechanism-defining contact positions.

**Prediction (register before Block A dispatch)**: Δd_tm6(cognate−apo) for OPSD should change by less than the OPSD-per-seed noise floor when moving from `alphai1` proxy to `alphat`. If the observed shift exceeds that, the mechanism model has more residues implicated than the L15/E19/L21 story admits.
