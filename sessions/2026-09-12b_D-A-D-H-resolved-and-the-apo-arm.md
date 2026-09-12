# 2026-09-12 — D-A and D-H resolved, and three claims of mine retracted

Continuation of the overnight autonomous run. Curation-only: no inference
commissioned, no GPU. **Eight commits pushed** — the first time this project's
work has been saved in two days.

**The retractions are the most important content here.** Three claims I had made —
one to `paper_af3` about their own code, one underpinning a decision Aditya took,
one about our own ligand data — were wrong, and the corrections are worth more than
the originals.

## What happened

| | |
|---|---|
| **D-A** | **RESOLVED** — conjunction kept for Class A, NPxxY calibrated, tilt inherited and validated rather than calibrated |
| **D-H** | **RESOLVED and implemented** — (c′) primary, (e′) scoped as an extension arm |
| **item 3, affinity** | **DISSOLVED** — we do not need it; I had imported the requirement |
| **item 4, the commit** | **DONE** — 8 commits, pushed |
| **item 5, the apo arm** | **DELIVERED** after Aditya signed off in their session |
| `MSA_SPEC.md` | reviewed by `paper_af3`; **they found a defect in our spec** |

## Decisions Aditya made, with their reasons

**D-A — keep the conjunction, calibrate one axis, inherit the other.** Reason: the
conjunction is what ran, so it stays comparable; but **every ground truth available
to Group 0 for the tilt is circular or retracted** — GPCRdb's state label is
*defined* on the same atom pair, transducer presence is the Q0c circularity he
already retracted, and calibration structures carry no reference pair. So the tilt
is inherited with provenance stated and **validated on the apo/cognate contrast**,
where no label participates. Cost accepted: we cannot claim a calibrated tilt, and
claiming one we cannot have would be worse. **Class A only.**

**D-H — (c′) with (e′) as an extension.** Reason: it is the framework already
adopted for this problem (the `cognate_family` / `reference_tip` split), and it is
the only option that neither contradicts our own rule nor scores a ladder rung
against an engineered sequence. (e′) is scientifically cleaner but introduces a
non-human partner into a human-partner ladder — a design choice, not curation.

**Affinity is not needed.** He asked why we needed it at all. We don't: ligand
identity is evidenced *structurally* — the molecule is co-crystallised in an active
or inactive receptor — which is a stronger claim than an assay number. The decoy
side still needs ChEMBL, but only for presence/absence of activity.

## What I got wrong and corrected

1. **F-1 — the two-instrument predicate DID run.** I told Aditya and `paper_af3`
   that the manuscript describes a predicate that never scored a row. Block A
   reproduces Class A as `npxxy AND tilt` at **100.0%** on 7,995 rows. There are
   **two instruments** and `MotifThresholds` is only one; the 2026-09-01 collapse
   was *within* the motif instrument. I read one function in isolation and
   generalised. **D-A had been decided on this false premise.**
2. **My D-A option (c) was unimplementable.** I proposed calibrating the tilt
   against RMSD-nearest-reference "subject to checking the data exists". It does
   not: calibration structures are off-panel and carry no reference pair, and
   choosing which reference is active is itself a state label. **Circular one step
   removed.** Withdrawn.
3. **F-11 — I reported the candidate pool's property as the reference pair's.** I
   wrote that OPSD and B1B1U5 both carry `RET` in both roles. True of every
   structure of those receptors; **false of the pairs we score against.** B1B1U5's
   are `A1H6M` and `RET` — chemically distinct, so it is **not** blocked. OPSD is
   blocked because its active reference carries a *detergent* and no agonist.
   Found by the D-H agent.
4. **The corpus check never failed `verify.sh`.** Both branches call `ok()`, not
   `bad()` (`verify.sh:26-27`). I had attributed the red to it for two days; the
   red was **unpushed commits**. The line is still worth fixing — cosmetic, not a
   broken build.
5. **My D-H §1 framing was the wrong diagnosis.** "Rule 3 ran and rule 4 never
   did" — but Rule 4 is **inapplicable**, because neither candidate is native.
6. **`CATALOGUE.md` said "33 experiments in 9 groups".** It holds **45 in 10**
   (E0–E9). Asserted in three headers, matching none of them. And my first
   recount said "1 group" because my regex took only the leading letter — a wrong
   number inside a correction about wrong numbers, caught before it landed.

## What paper_af3 found in our specification

**They caught a defect inside the mechanism `MSA_SPEC.md` recommended**, which
would have silently destroyed the ladder:

```
propose.py:462  OF3       .get(cid)          → CHAIN ID
propose.py:595  Protenix  .get(protein_idx)  → INTEGER POSITION
```

`{"A": receptor, "B": ""}` works on OF3 and **fails silently on Protenix** — no MSA
set, launcher default, **live fetch at full depth on both chains**, invisible in
every status JSON. We wrote a section arguing against exactly that failure mode and
then specified a mechanism producing it.

Also: we specified the *unpaired* slot and inherited the paired one; and our
alternatives table carried a **false choice** ("Chai excluded") that would have let
someone weaken the design for nothing.

## What the apo arm found — F-13

Requested to settle one question, answered three. **Class B is not saturated.** But:

- **Boltz and Protenix put Class B apo at ~12 Å; Chai and OF3 at ~20 Å.** A **9 Å
  disagreement about the same receptors with no partner** — larger than the
  separation the threshold detects. **No pooled Class B rate is meaningful.**
- **Class F apo medians (14.20–16.12) straddle the 14.932 cut on every backbone.**
  No discriminating power. Confirms the standing gate WAIT by measurement.
- ~~**SMO gets *less* open when the partner is added** (−2.14 Å).~~
  **RETRACTED 2026-09-12c.** OF3-only. SMO is +0.22 / +0.04 / −2.14 / +0.19 across
  boltz / chai / of3 / protenix — slightly positive on three of four. Caught by
  `paper_af3`, reproduced here from the tables we hold. It was the same
  pooling-across-disagreeing-backbones error flagged for Class B two bullets above.
  What survives is stronger and receptor-independent: Class F deltas span −2.14 to
  +2.41 with inconsistent sign. See `DECISIONS.md` F-13(c).

## What the next session should not redo

- **Do not re-open D-A or D-H.** Both resolved, with reasons, in `DECISIONS.md`
  (D-2026-09-12-b and -c). `CAMPAIGN.md` carries superseded banners in place.
- **Do not chase affinity data for the seven ligand picks.** Not needed.
- **Do not calibrate the tilt.** Every available ground truth is circular; that is
  the decision, not an oversight.
- **Do not trust a count asserted in a header.** Three said "33 in 9"; it is 45 in
  10. Count the body.
- **`paper_af3`'s bridge instance is separate** (`/Users/SENGAAD1`, own dedup
  state). Reply on the **bridge**, not cross-session — their session goes idle and
  cross-session messages queue unread. That cost us three messages.
