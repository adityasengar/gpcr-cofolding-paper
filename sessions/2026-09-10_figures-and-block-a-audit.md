# 2026-09-10 — figures rebuilt, Block A audited, the old export retired

## What happened

Block A's section was audited against the corpus and rewritten; the pre-Block-A
export was deleted; the structural renders were rebuilt on a depth-of-field
technique; four graphical-abstract candidates were built in parallel. Main text
36 pages, SI 18, build clean, `verify.sh` green.

## Decisions Aditya made, and why

- **Blocks supersede.** One zip per block, each replacing the last for new
  claims. *Why:* the earlier export turned out to be a different campaign — 28
  of 48 receptors shared, no shared prediction paths, different arms. Two
  unrelated datasets in one tree is how a wrong number reaches a sentence.
- **Block A is groundwork; Block B carries the titular peptide claim.** *Why:*
  the title claims a 21-residue α5 peptide co-input and Block A supplies the
  whole cognate Gα. Rather than rewrite the title, Block A becomes the
  instrument-and-scale section that Block B rests on — which is a better paper
  than either half alone.
- **No lettered panels in the graphical abstract.** *Why:* a/b/c is figure
  grammar; an abstract is one composition.
- **Four candidate styles built in parallel** rather than one plus a description
  of alternatives.

## What the verification found

23 discrepancy groups; four were named in the shipped brief, **nineteen were
found here**. The five that would have put something false or unsupported in the
paper:

- `8FZQ.cif` is CFTR, not an opioid complex (D18)
- the "confidently wrong" structure is confidently *right* (D12)
- SC-1's "cluster-boot" intervals are the receptor column (D5)
- four `ALIGNMENT.md` files name anchors that do not reproduce (D13, D20)
- no template or MSA column exists, while Methods asserted both (D19)

Two later ones came out of drawing: `rmsd_to_active_ref` does not reproduce from
coordinates (D22), and `*_active_rate_panel_mean` is a pooled rate, not a mean
(D23).

## What I got wrong and corrected

- Asserted **MSAs were pinned**. No such column exists. Removed.
- Published that **chiesa2025templatebias has no apo arm**. It does — the
  AFM-receptor protocol. Withdrawn, and the four distinctions restructured.
- Left Block A's prose as **markdown outside the manuscript**, so the paper had
  no Block A section until it was `.tex`.
- Our `camera.py` **bent the membrane normal by 35.5°** on every DRD2 render
  shipped before today, by fitting through a 147-residue pLDDT-38 ICL3.
- Accepted "correct" as done for figures until Aditya supplied exemplars.

## What the next session should not redo

- The pre-Block-A export is gone deliberately. Do not resurrect it.
- BA-8 and BA-1a renders are good. Do not rebuild them.
- The 23 discrepancies are recorded; re-derive only if the drop is replaced.
- **Two of four agents independently wrote that the 21-mer was supplied**, both
  with `CLAIMS.md` in their brief. The framing pulls that way. Before Block B,
  give it a mechanical guard rather than another sentence in a file.

## Open, carried forward

The steric-exclusion observation — α5 heavy atoms within 4 Å of TM6: 52% and 39%
against deposited *inactive* structures, 11% against active, 2–4% against the
prediction's own TM6. It is a mechanical account of why the co-input works, but
n = 2 receptors and the active control is not zero. Needs an import.
