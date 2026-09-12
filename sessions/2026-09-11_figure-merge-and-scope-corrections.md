# 2026-09-11 — figure merge, cross-document references, and three false scopes

Orchestrator session. No new block landed. The work was on the document itself:
one figure merged, one rebuilt, eight broken cross-references found and fixed,
and three separate places where a scope was asserted that the data does not
support.

## What happened

**Figure 1's top half cleaned up, on Aditya's list of four.** Panel headings
sentence-cased; the census line broken over two lines because it overran its
box; `constrained_layout` replaced with explicit gridspec geometry; and panel c
now says **the first of four campaigns**. That label went on panel c and not on
the figure title because panels a and b are the instrument and its calibration
and are shared by all four campaigns.

**BB-1 and BB-2 merged into BB-12, main-text Figure 3.** They drew the same
ladder twice — BB-2's left panel was titled "the ladder, and the two steps that
telescope" and redrew the four rungs BB-1 had already drawn, forty-five lines
earlier in the prose. Main sequence is now **four figures**: F1, BA-2, BB-12,
BC-2.

**BB-7 built by the lit session** to close an orphan: the per-backbone family
term was in the prose with no figure behind it, because BB-2's ledger entry
promised a panel the 2026-09-10 rebuild had silently replaced.

**A subagent produced six BA-1a backdrop variants over two rounds and Aditya
rejected all of them.** The original hairline trace stands. `ba1a_instrument.py`
was never modified; the toolkit changes were reverted and the variants parked
outside the repo.

## Decisions Aditya made, with their reasons

- **Merge Figures 3 and 4** — because Figure 4's left panel already redrew
  Figure 3's ladder. My condition, which he accepted: BB-2's caption carries the
  paper's most consequential claim-side correction and it survives the merge at
  full strength.
- **Reject all six BA-1a variants.** He liked v2's structure but not the
  backdrop treatment in any round; "revert to original" was explicit. The two
  rounds converged on treating the backdrop as a helix cartoon and that is the
  direction that was rejected, not a particular execution of it.
- **Ask lit whether the contrast panel form is acceptable** rather than trusting
  my own design sense. That was the right call and it produced a better answer
  than either of us would have reached alone.

## What the verification found

- **`build.sh` reported undefined CITATIONS from the day it was written and
  never undefined REFERENCES.** Eight `\ref{sfig:...}` in `results.tex` were
  printing as `??` in `main.pdf` — they point into `si.tex`, a separate
  document. `HANDOVER.md` claimed "0 undefined references" throughout. Fixed
  with `xr` + `\externaldocument{si}`; `build.sh` now builds the SI first so
  `si.aux` exists, reports undefined references, and independently greps the
  built PDF for a literal `??`. **Proved by planting a bad `\ref`**: both
  checks fired and named the label.
- **Three separate places asserted a scope the data does not support**, and in
  all three the body text underneath was correct. See below.
- **SC-B-2's per-backbone family shares reproduce almost not at all.** Claimed
  17.4 / 17.5 / 20.9 / 17.5; shipped 14.2 / 22.9 / 23.6 / 10.9. Three of the four
  claimed values match **nothing** in the file on either scale or either frame.
  The fourth, "boltz 17.4%", matches exactly one row: `reproduction_36 / panel /
  logit` — the **pooled** estimate. Boltz is never 17.4% anywhere. lit found
  this; I verified it exhaustively against every row.
- Verifiers unchanged: A 48/63, B 95/116, C 69/69, D 49/54 + 12 PROSE-ONLY.
- Build: main 59 pages, SI 43, 0 undefined citations, **0 undefined references**,
  0 literal `??`, 0 overfull vboxes. Four guards clean.

## The pattern worth naming: scope is asserted where it is most read

Three instances in one day, all corrected, and the body text was right in all
three:

1. `results.tex` section **heading**: "Ligand class is written into pocket
   geometry, **but only where the partner is absent**" — the body withdraws that
   scope three paragraphs later.
2. si.tex caption **title**: "Ligand class in pocket geometry, **and what the
   partner does to it**" — the partner is not a factor in that 2×2 at all.
3. `figures.tex` header comment: BC-1 "not drawn in either position" — it had
   been in the SI all along.

A heading, a caption title and a figure's own face are each read far more often
than the paragraph beneath them. lit's phrasing: the failure mode is that scope
gets **asserted where it is most read and qualified where it is least read**.

## What I got wrong and corrected

- **I described the Block C 2×2 to Aditya as "arm × ligand role".** It is
  **ligand class × reference state** — `agonist_active` means "agonist rows
  measured against the ACTIVE REFERENCE", not "agonist rows in the cognate arm".
  The partner arm is not a factor in it; apo-only was meant to be a *filter* and
  was never applied. This matters because it means there is no partial answer to
  extract from the shipped artefact. Caught by reading the artefact instead of
  the prose, after Aditya asked the question directly.
- **I nearly recorded a false discrepancy on the 2×2's intervals.** The
  manuscript quotes [−0.454, −0.164] and the JSON carries [−0.431, −0.192]. Both
  are correct: C-C-3 documents cluster-boot as authoritative and receptor-boot as
  secondary, and the manuscript quotes the right one. Found the caveat file
  before reporting.
- **I over-corrected Figure 1's spacing twice** — `hspace` 0.46 then 0.30 before
  settling at 0.24 with a reduced first row.
- **My own new guard had a bug on its first run.** `grep -c` prints `0` *and*
  exits 1, so my `|| echo 0` fallback produced "0\n0" and `[` errored. Fixed
  before the defect-planting test, not after.
- **I put a bare `→` (U+2192) in a `fig.text`.** It is missing from the house
  font and renders as a blank box. The subagent had hit exactly this an hour
  earlier and recorded it; I hit it anyway. Mathtext `$\rightarrow$` in a label
  is fine; a bare arrow in `fig.text` is not.
- **My first merged layout put the "via shuffled (confounded)" line in the
  legend without it being visible** — BB-1's ladder runs through all four arms,
  so the "route not taken" lay exactly under the panel line. A legend entry for
  something the reader cannot see is the same defect class as a check that never
  runs. Removed; panel c carries the argument in words.
- **lit reported that C-C-3 does not exist; it does**, and their mechanism is
  worth more than the correction. Their command was
  `grep -rn "C-C-3" data/block_c/02_caveats/* | head -2`. The file exists, it
  contains the string, and grep matched it — but the directory sorts C-C-10,
  C-C-11, C-C-1, C-C-2, C-C-3, so `head -2` kept the matches from C-C-2 and
  C-C-11 and cut the real hit below the fold. **Piping a search through `head`
  when the question is whether something EXISTS converts a positive result into
  a negative one.** Fifth instance of the silent-check family in one day across
  two sessions, and a fourth distinct mechanism.

## What the next session should not redo

- **Do not rebuild the BA-1a backdrop.** Six variants over two rounds, all
  rejected. The hairline trace is the treatment that stands. The rejected work
  is in the session scratchpad, not the repo.
- **Do not blanket-replace "26 paralog clusters" with 24.** Three of the five
  instances are **Block A**, whose bootstrap genuinely used 26. Only the Block B
  frame_36 statements take 24. `methods.tex` states both correctly.
- **Do not re-litigate the `xr` direction.** main → si is installed and fixed
  eight `??`. si → main was offered to lit and **declined with a good reason**:
  two references gained against a silent `??` on every build path that is not
  `./manuscript/build.sh`. Asymmetric, and their call stands.
- **Do not add a panel for SC-B-2's per-backbone family term beyond BB-7.** The
  evidence is now drawn; the *claim* is still Aditya's decision.
