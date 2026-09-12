# COUPLING_REVERSALS.md — CCKAR, EDNRB and GHSR, closed

**The question.** Four receptors have a Rule-R structural cognate that reverses Block
B's prior. B1B1U5 closed as D-H. The other three — **CCKAR, EDNRB, GHSR** — all had
Block B prior **Gq**, and in all three the Rule-R active structure reads something
else. The objection that kept them open was real: *most annotation authorities also
say Gq/11, so preferring the structure looks like preferring one source over four.*

**It is not, and this document is the evidence.** Reproduce with:

```bash
python3 redo/build/coupling_reversal_evidence.py     # writes inputs/coupling_reversal_evidence.tsv
```

---

## The method

For **every** active structure GPCRdb holds for each receptor — not only the chosen
reference — record the Gα entity's UniProt accession, its length, and the deposition's
own description, then classify it:

| class | rule |
|---|---|
| `engineered` | the entity description **or the entry title** names a chimera, fusion, engineered or dominant-negative construct, **or** the entity carries accessions from two different Gα families |
| `truncated_or_mini` | length below 85% of that family's canonical length (from `seq_constructs.tsv`), or below 85% of the shortest canonical Gα when no family resolves |
| `unverifiable` | no reference accession at all |
| `native` | everything else |

**The title test is load-bearing.** `9BKK`'s entity description says only *"G(s) subunit
alpha isoforms XLas"*; its **title** says *"Gq chimera (mGsqi) complex"*. Description
alone classed it native — my first run did exactly that, and so did the 246 aa and
261 aa mini-G entries, which carry no engineering word anywhere. **Length is the
discriminator the keyword test misses entirely.**

---

## The result

### CCKAR — 9 active structures

| PDB | Gα | len / canonical | class |
|---|---|---|---|
| **7MBX** ← Rule-R | Gs | 394 / 394 | **native** |
| 7XOU, 7XOV | Gs (Isoform Gnas-2) | 380 / 394 | native |
| 7EZH | Gi1 | 354 / 354 | native |
| 7EZM | Gi1;Gq — *"fusion protein of … G(i)α1 and … G(q)α"* | 353 | engineered |
| 7EZK | Gi1;Gs — *"Chimera of …"* | 361 | engineered |
| 7MBY, 9BKJ | Gi1;Gs *"with certain residues mutated to match G(q)"* (mGsqi) | 253 | engineered |
| 9BKK | Gs(XLas), title *"Gq chimera (mGsqi)"* | 253 | engineered |

**Every Gq-labelled CCKAR structure is an mGsqi chimera or a Gi/Gq fusion. There is no
native Gq-bound CCKAR structure at all.** Block B's prior could not have been supplied
as a native partner even in principle.

Two families remain natively represented — Gs and Gi1 — and Gs wins both tiebreaks:
`7MBX` is the **best-resolution active of all nine (1.95 Å)**, and Gs is in IUPHAR's
own transducer list (`G q /G 11 family || G s family`), while Gi/o appears only as
`family_secondary_annotated`.

> **CCKAR = Gs.** Unchanged in outcome, **changed in basis**: not "the structure beats
> four authorities", but "the family those authorities name has no native structural
> representative, and the one we supply does".

### EDNRB — 10 active structures

| PDB | Gα | len / canonical | class |
|---|---|---|---|
| **8IY5** ← Rule-R | Gi1 | 354 / 354 | **native** |
| 8HBD | Gi1 | 354 / 354 | native |
| 8XWP, 8XWQ | Gi1, "DNGI" dominant-negative | 354 | engineered |
| 8XVE, 8XVH | Gs (Isoform Gnas-2) | 261 / 394 | truncated_or_mini |
| 8HCX | *"G(q) subunit alpha-1"*, no accession | 246 | truncated_or_mini |
| 8XGR | eGt fusion — no Gα entity resolves | — | no Gα entity matched |

**Gi/o is the only family with a native full-length representative.** And
independently, `coupling_assignments.csv` records Gi/o as **the only family compatible
with all five authorities**.

> **EDNRB = Gi/o.** Two independent grounds, no tension with any authority.

### GHSR — 5 active structures

| PDB | Gα | len / canonical | class |
|---|---|---|---|
| **7NA7** ← Rule-R | Gi1 | 354 / 354 | **native** |
| 7NA8 | Gi1 | 354 / 354 | native |
| 7F9Y, 7F9Z | *"Engineered G-alpha-q"* | 362 | engineered |
| 7W2Z | GoA | 236 / 354 | truncated_or_mini |

**Gi/o is the only family with a native representative**, and it is present twice.
Block B's Gq exists only as a subunit the depositors themselves label *engineered*.

> **GHSR = Gi/o.**

---

## What generalises

**In all three receptors, the family the Rule-R structure reads is the only family with
a native, full-length, non-engineered Gα anywhere in that receptor's active structures.
Every competing family — Gq in all three, Gs and Go besides — exists only as a mini-G,
a chimera, or a subunit the depositors call engineered.**

So the three reversals were never a conflict between a structure and four annotations.
They are a conflict between **what a receptor couples to in an assay** and **what
anyone has managed to deposit it bound to** — two different questions, exactly as with
the four Block C "cognate disagreements" that turned out to sit in a *secondary*
coupling column.

And it aligns the three with the project's standing chimera policy: a chimeric partner
is excluded from the primary panel. Supplying Block B's Gq would have meant supplying a
chimera at three of thirty-two core receptors.

---

## Limits, stated

- **This says nothing about the biology.** CCKAR really does signal through Gq/11; that
  is not in dispute. The claim is narrower and structural: *of the partners we could
  supply and score against, only one family is native.*
- **Structural availability is a publication artefact.** mGsqi exists because native Gq
  complexes are hard to resolve. A native Gq-CCKAR structure appearing later would
  reopen this, and `coupling_reversal_evidence.py` re-run against a newer snapshot is
  how that gets noticed.
- **`8XGR` resolves no Gα entity** — its α subunit is fused into the γ chain
  (`"…gamma-2,eGt-alpha"`). It is recorded as unresolved rather than skipped, because a
  row that quietly disappears is the failure mode this project keeps finding.
