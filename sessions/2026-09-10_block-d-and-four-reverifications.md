# 2026-09-10 / 11 — Block D, three re-verifications, and the document getting wired

Orchestrator session. Ran through the night; the corpus session (`lit-3d`) ran
alongside on its own lane and the two exchanged fourteen messages.

## What happened

**Block D landed and was processed end to end.** 42,180 predictions across three
tiers — deep apo, directed nanobody, MSA depth. Intake, verifier, discrepancy
report, five panels, Methods and Results into the `.tex`, data requests and
rebuttal. **It is the first block that shipped no row-level data at all**, which
forced a third label into the verifier: `RECOMPUTED`, `CONSISTENCY`,
`PROSE-ONLY`, with the last printed in its own total so a pass count can never
be read as a claim count.

**The corpus session ran three independent re-verifications** on Blocks A, B and
C with agents that deliberately did not read our discrepancy reports. Verdict on
the data was unanimous and good — every aggregate rebuilds bit-exactly, 79/80
and 103/103 manifest hashes match. **Every defect was claim-side**, and four
landed on files I own.

**The document was wired.** It had zero `\label` and zero `\ref`; the prose and
the panels were not connected at all. Main sequence cut to five figures, all
placed and cited, eight SI references wired, prefix scheme documented.

## Decisions Aditya made, with their reasons

- **Two full rounds, then a complete SI, "almost publication ready".** Given to
  the corpus session directly; it superseded a hold the two sessions had agreed
  an hour earlier. The corpus session's judgement — build figures 1–4, specify
  5 and 6 without rendering, put the reason in writing — was better than the
  literal instruction and is what happened.
- **Brainstorm the next experiments together after Block D**, rather than
  receiving a plan. Recorded in memory and at the top of `HANDOVER.md`.

## What the verification found

| block | checks | reproduce |
|---|---|---|
| A | 63 | 48 |
| B | 116 | 95 |
| C | 69 | 69 |
| D | 54 | 49, plus 12 PROSE-ONLY |

Four claim-side findings still need Aditya: the pLDDT arm-pooling artefact, the
G4 gate, two wrong bootstraps, and the title. All four lead `HANDOVER.md`.

**Two manuscript claims were false and are now fixed.** The α5-CT decomposition
term was confounded — the shipped middle term swaps a whole subunit — and the
clean contrast, `decoy → cognate`, is *larger* at +0.333 [0.242, 0.432] and
telescopes exactly. And the 2×2 was asserted to hold "in the apo arm alone"; the
shipped row counts are exactly the both-arms figure on every backbone.

## What I got wrong and corrected

Seven this session, and the pattern has sharpened since yesterday: **the errors
are no longer in the data, they are in my checks.**

- **Said the 2×2 artefact ships no row counts.** It ships four. My traversal
  recursed *into* `n_rows` because it is a dict, and the cell names inside did
  not match the key filter I was printing on. *A check that runs and silently
  prints nothing is indistinguishable from a check that found nothing* — the
  third instance of that shape on this project.
- **Recorded D-A-24 as a discrepancy; it was my error.** 4,866 is
  `rows.active.sum()` exactly. I applied the Class-A two-axis rule to a
  class-conditional column. On Class A alone my rule agreed on 3,742 of 3,742.
  **The project had made this exact mistake before** and I had recorded the
  correction.
- **Changed the manuscript to say 29 clusters** where the bootstrap used 26,
  after an audit flagged the shipped map. Made Methods describe a resampling
  unit that was never resampled, and no verifier would have caught it.
- **Reported AGTR1's NPxxY as a 0.16 Å discrepancy** by comparing one shipped
  structure against a 50-sample cell median.
- **Wrote "resolution is entirely NaN"** in four documents going upstream. It is
  a placeholder *string* — non-null, so a null check passes on it.
- **Announced eighteen coupling chimeras that do not exist**, from a lexical
  tie-break: Gi1 and Gi2 have byte-identical α5-CTs, as do Gq and G11.
- **Registered numbers against "check C60"** where the verifier emits
  `C60.grid` and `C60.boltz`. The coverage guard caught it in under a minute —
  the guard working on its own author.

## What the next session should not redo

- **Do not re-verify the blocks.** Four verifiers exist and their mismatch
  counts are documented: 15, 21, 0, 5.
- **Do not rebuild the panels.** 32 ledger entries, 30 placed. The two absent are
  BA-5 (blocked on the arm-pooling artefact) and the graphical abstract
  (Aditya's pick among five candidates).
- **Do not re-derive the decomposition.** It is restated, pinned by a panel that
  refuses to draw if the shipped terms do not reproduce, and independently
  confirmed by S-T5 on four backbones in both frames.
- **Do not chase `rows.tier3.v2.csv` yourself.** It is Block C ask 1, it blocks
  two claims, and it is `free` — it exists and was not zipped.
