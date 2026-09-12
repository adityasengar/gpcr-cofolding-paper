# HANDOVER.md — for a fresh orchestrator session

Start in `paper/`. `CLAUDE.md` loads automatically; read it, then this.

## Where the project is

**Four blocks landed, verified and written. The document is wired and the
cross-references now resolve.** Main **59 pages, four figures**; SI **43 pages,
35 figures, 7 tables**; 67 bibitems; **0 undefined citations, 0 undefined
references, 0 literal `??`, 0 oversized floats.**

| block | checks | reproduce | note |
|---|---|---|---|
| A | 63 | 48 | 15 mismatches, documented |
| B | 116 | 95 | 21 mismatches, documented |
| C | 69 | 69 | 30 of them consistency-only |
| **D** | 54 | 49 | **and 12 claims recorded PROSE-ONLY** |

**The main sequence is four figures**, after BB-1 and BB-2 were merged into
BB-12 on 2026-09-11: F1 (workflow + instrument), BA-2 (arm shift), **BB-12**
(ladder + decomposition), BC-2 (ordinal). They drew the same ladder twice. The
graphical abstract `ga1_hero` sits unnumbered in `main.tex` with `\caption*`.

**Five guards, four proved by planting a defect**: the number sweep and its
coverage check, the request-document auditor, the panel auditor, and — new on
2026-09-11 — `build.sh`'s undefined-**reference** check. `audit_crossref` has
still only ever fired on a coincidence.

## The decisions waiting on Aditya

### A. Four claim-side findings that need your call

1. **The pLDDT "two of four backbones" is an arm-pooling artefact.** Scored apo
   *and* cognate against the **active** reference. Within cognate:
   −0.30 / −0.43 / −0.42 / −0.16, all four negative, OpenFold3 not an outlier.
   **Direction survives, shape does not.** `[PI]` in `results.tex`.
   *New, 2026-09-11:* the operational half of the claim is the stronger half.
   Picking the highest-confidence seed beats random by **+1.1 pp overall**, sign
   flipping across backbones (−3.1 to +4.9), and **300 of 319 cells are
   unanimous across SEEDS anyway** — only 19 cells (6.0%) show any
   seed-to-seed disagreement. (This line previously read "256 of 319"; that is
   the SAMPLE-grain count, where all 25 individual predictions agree. Quoting it
   as a seed-grain number understated how redundant the seed axis is. Recompute
   with `redo/build/matrix_power.py`.) But pooled across seeds, confidence *does* separate
   correct from incorrect calls (AUC 0.60–0.96) — and that evaporates when you
   control for receptor. Confidence tells you which **receptors** are easy, not
   which **structure** is right. Those are different claims and the sentence
   merges them.
2. **Block C's G4 gate fired on 8 of 12 cells and its remedy was never applied.**
   Still the most serious finding in any block. Needs `rows.tier3.v2.csv`.
3. **Two intervals are the wrong bootstrap** — SC-C-5's row bootstrap, and
   SC-B-2's Protenix family CI. **The evidence for the second is now drawn**
   (BB-7, SI S22); the claim is still written as "squarely positive".
4. **The 2×2's scope.** Estimate sound, scope withdrawn. See B below — it is
   narrower than it looks.

### B. The title, and what Block C can and cannot close

No arm in any block supplies a **peptide**; the manipulated segment is **eleven**
residues, not 21. So the narrowed title is about a Gα co-input and its C-terminal
determinant. The alternative is to run the arm.

**The agonist clause is closer than it looks and blocked on one file.** Block C's
2×2 has **ligand class × reference state** as its factors — the partner arm is
*not* a factor in it, and apo-only was meant to be a row filter that was never
applied. But the design grid is 50 predictions per (receptor × backbone × role ×
arm), 800 cells, so **all four of agonist/antagonist × apo/cognate exist and are
scored — roughly 18,400 predictions**. lit confirms **no paper in 81 crosses
ligand class with partner presence on one model**. It needs `rows.tier3.v2.csv`.

### C. Still open

1. **Pick the graphical abstract.** Five candidates built; `ga1_hero` is placed.
2. The steric-exclusion observation (n = 2, needs an import).
3. The panel selection rule — 40 Class A and 40 receptors-with-both-states are
   **different sets** (the latter is 32 A + 4 B + 4 F). The "40/40 match" is a
   coincidence of two forties. `[PI]` in Methods.
4. The reference-set denominators are **resolved in the drop's own
   `denominator_populations.csv`**: 89 was the manuscript's prior number, **98 is
   empirical** (44 active + 54 inactive on the panel), 167 is the full set
   including off-panel. Two `[PI]`s in `methods.tex` can now be closed.

## The two maps — read these before anything under `redo/`

Written 2026-09-12. They exist so that the pipeline can be followed end to end
without opening seven thousand lines of protocol notes.

| map | covers |
|---|---|
| `redo/protocol/MAP_FROZEN_CAMPAIGN.md` | **how the frozen paper was actually run** — panel, references, inputs, ligands, decoys, MSAs, dispatch, scoring, analysis, the silent-failure map, and the three holes that cannot be closed from the bundle |
| `redo/spec/MAP_NEW_CAMPAIGN.md` | **what the redo runs** — 64 receptors with their reference pairs and cognate Gα, the length ladder, 782 partner constructs, ligands, the decoy rebuild, 23 arms with their prediction budgets, the 47-column recording spec |

**The second is GENERATED** — `python3 redo/build/map_new_campaign.py` rebuilds it
from `redo/inputs/`. Do not hand-edit it; edit the generator. Nothing in it is
transcribed, because a count asserted in a header has drifted from its own body
four times on this project.

## The redo campaign — where it now lives

**`redo/` at the top level**, a peer of `manuscript/` and `lit/`. It was
`analysis/redo/` until 2026-09-11; sitting beside `block_a..d` made it read as a
fifth block, which it is not. `analysis/redo/` and
`analysis/REDO_EXPERIMENT_CATALOGUE.md` are gone — the catalogue is
`redo/spec/CATALOGUE.md`. **Blocks A–D were not touched and will not be.**

Read `redo/README.md` before touching anything under it. The short version:
`spec/` is written by a human once, `build/` and `gates/` are code, **`inputs/`
is written by code only and every file is hashed in `inputs/MANIFEST.tsv`**, and
`cache/`, `runs/` and `protocol/` arrived from outside and are nobody's to edit.

`redo/gates/layout.py` enforces it — seven checks, each proved by planting the
defect it catches. A hand-edit of an input trips it and trips the manifest
check; **neither preflight gate notices**, which is the reason it is a separate
guard. `verify.sh` runs all four.

`redo/runs/README.md` is the **delivery contract, drafted and not yet sent**:
one directory per run, one row per prediction, fixed identity columns, and a
`manifest.json` naming the input hashes consumed. It goes to `paper_af3` with
the frozen `inputs/` set as one document, once their §2 blueprint says which
measured-axis columns they can actually produce. Blocks A–D each cost a bespoke
verifier — 63, 116, 69 and 54 checks — because their shape was settled after the
data existed. These runs do not exist yet.

## Where the redo stands — 2026-09-12, after D-A and D-H

**All five of Aditya's open items are closed.** Everything is committed and
pushed; the working tree is clean. Logs:
`sessions/2026-09-12_autonomous-curation-and-three-retractions.md` and
`sessions/2026-09-12b_D-A-D-H-resolved-and-the-apo-arm.md`.

### The decisions, with their reasons

**D-A — Class A keeps the conjunction** (`NPxxY < 9.08 AND tilt > 14.932`).
Group 0 calibrates **NPxxY only**. The tilt threshold is **inherited with its
provenance stated and validated on the apo/cognate contrast, not calibrated** —
because every ground truth available for that axis is circular or retracted
(GPCRdb's label is defined on the same atom pair; transducer presence is the
retracted Q0c; calibration structures carry no reference pair). We cannot claim a
calibrated tilt, and claiming one we cannot have would be worse. **Class A only.**
`DECISIONS.md` → **D-2026-09-12-c**.

**D-H — (c′), with (e′) as an extension arm.** B1B1U5 stays PRIMARY on 9EPP.
Panel unchanged at 30/29. **Rule 4 is inapplicable, not unimplemented** — neither
candidate is native. (e′) builds free but stops at 18 residues.

**Affinity is not needed** for the seven ligand picks. Ligand identity is evidenced
structurally; the decoy side still needs ChEMBL for presence/absence only.

### What is still open — 2026-09-12, after the scope decision

1. **The measurement pass** — Group 0's largest outstanding dependency; the gate
   now lists 8. It must record axis values for the **F3-removed** structures too,
   or that filter stays permanently unauditable (F-12). **Not started without
   Aditya's word.**
2. **D2's regeneration.** Decided at (c): expand onto `cxcr3`, `mtr1a`, `mtr1b`;
   reserve the other 17. **Held until the pass is authorised** so the population
   freezes once rather than twice. It changes `on_panel48`, hence the frozen
   constants in G0-2, G0-5 and G0-7 — a generator re-run plus a manifest restamp,
   never an edit.
3. **`MSA_SPEC.md` implementation** — with `paper_af3`, gated on their review.
   Their review already found a defect in our spec; see F-13 and the spec's §3.
4. **Amendment C-1** — whether to reopen it so an **inverse agonist** can fill a
   `neutral_antagonist` slot. It blocks **ADRB1** and **B1B1U5**, and it is the
   only thing standing between the ligand arm and 8 picks instead of 6. Aditya's
   call, not a curation judgement (F-15).
5. **The decoy pool** — deliverables 1 and 3 are **built and proved**; 2 and 4
   are not. `drule_targets.tsv` resolves **63 of 64 receptors** to a ChEMBL target
   against **ChEMBL_37**, 31 of 32 clusters; B1B1U5 has no ChEMBL target and is
   recorded rather than dropped. `drule_pool.py` is written and its rule is proved
   on a fixture, and it **refuses the live API by design** — it needs a downloaded
   release with `--release` and `--sha256`. **That download is your decision**, and
   it is the only thing between here and a pool report.
6. **`lit/corpus_check.sh`** — proposed fix below, not actioned; it is lit's file.

**Closed since the last handover:** the redo's scope (Class A only,
D-2026-09-12-d), D2 (the split, D-2026-09-12-e), the three coupling reversals
(F-14), and D-C's ligand picks (F-15). **Class B and Class F instruments are no
longer owed** — they left with the scope, and F-13 is the measured reason.

### Proposed for the lit session

`corpus_check.sh` classifies the four deliberately-unread `refs.bib` entries as
**hard** drift, so it can never exit 0. **This does NOT fail `verify.sh`** — both
branches of that line call `ok()`, not `bad()` (`verify.sh:26-27`), so it prints
without failing. Cosmetic, but a permanently-present warning is one everyone learns
to skip. Fix: demote that one report from hard to soft, as the "note with no PDF"
report already is.

### The bridge

`~/.ntfy-bridge/` — **session-local, dies with the session.** Re-arm exactly ONE
`recv.sh` and ONE `sweep.sh`, then `pgrep` to confirm: one receiver chain is 3
processes, one sweep is 2. More than that and messages can be silently swallowed —
every instance shares `.seen`.

**Reply on the BRIDGE, not cross-session.** `paper_af3`'s session goes idle and
cross-session messages queue unread; that cost us three messages. Their bridge is a
**separate instance** (`/Users/SENGAAD1`, own dedup state) — the single-receiver
rule applies within an instance, not across machines.

Limits, measured: text ~12 h, **attachments ~3 h**, practical cap **~1.5 MB** (not
the documented 15 MB). Both `send.sh` and `recv.sh` now persist to `sent/` and
`received/`.

**The receiver's stream drops every few minutes, not hourly — this is normal and
not a fault.** Measured 2026-09-12: the `curl` PID turned over three times inside
about two hours, once only 23 s after the previous reconnect. It is ntfy closing
the JSON stream, not the `-m 3600` timeout (I first assumed the timeout, wrongly).
Nothing is lost: `recv.sh` reconnects with `since=15m`, so it re-fetches the gap,
and `.seen` dedupes what it re-reads. `sweep.sh` is the 5-minute backstop.

**The one real risk is the watcher, not the bridge.** A Monitor that emits enough
events gets stopped automatically, and a stopped receiver looks exactly like a quiet
channel. If the bridge matters for what you are doing, `pgrep -f recv.sh` should
print **3** and `pgrep -f sweep.sh` **2** — check that rather than trusting silence.

## How the sessions work

Three, on one laptop. **Content versus machinery.**

| | writes | never |
|---|---|---|
| **lit** (`paper/lit/`) | `lit/**`, `sections/intro.tex` | git |
| **figures** (`paper/figures/`) | `figures/**`, figure captions | git |
| **orchestrator** (`paper/`) | `main.tex`, `analysis/**`, all git | — |

`lit-3d` is reachable directly with `SendMessage` — check `ListAgents`. It has
been the most valuable correspondent in the project: it caught novelty claimed
by omission, disproved my theory about `ku2026promise`, and established the
render conventions by *viewing* panels rather than reading captions.

**For Block A the two-pass rule was restored and it must stay restored: lit
retrieves and never drafts; the orchestrator drafts and never retrieves.**
Numbers are in sentences now, and a session that does both writes the paragraph
first and finds support afterwards.

## Open, and not ours to close

- **The panel selection rule.** Aditya told the lit session his criterion was
  *"unique GPCRs with both active and inactive, and I picked 40 out of them"* —
  authorial intent, matching our 40/40 observation, and a likely resolution of
  the 48/46/40 discrepancy in `lit/CLAUDE.md`. **Pending his confirmation, not
  resolved.** A `[PI]` marker sits in the Methods Panel subsection.
- **Block C's 66 named-but-unshipped files.** Four matter:
  `rows.tier3.v2.csv` (without it, 30 of 53 checks are consistency-only),
  `s4_bw_decomposition.json` (the only residue-level analysis named in any
  block), `task6_p0_correlation.json` (the only quantitative cross-block link,
  n=35), and `task_D_species_match_root_cause.json`.
- **Two rebuttal documents are written and unsent**: `rebuttals/BLOCK_A.md`,
  `BLOCK_B.md`, plus `PANEL_EXPANSION_CLASS_A.md` with 19 Class A receptors and
  their PDB pairs.

## The corpus, as the lit session left it (2026-09-10)

- **Citations carry PRINTED pages, not PDF pages.** Seven of 74 PDFs have an
  offset; `abramson2024af3` +492, `chiesa2025templatebias` +6297 (already
  recorded as printed --- do not convert twice), `georgiou2025heterogeneity`
  +3690, `yang2025statespecific` +11424, `gilson2025casp16` +248,
  `heo2022multistate` +1872, `waymentsteele2024cluster` +831. `hilger2020gcgr`
  is exempt: it is an eLocator article with no folio anywhere, so PDF page is
  the article page.
  **`cd lit && python3 validate/pageoffset.py`** answers both halves --- which
  PDFs have an offset, and which `\citep[p.~N]{key}` locators in
  `manuscript/**/*.tex` are still PDF pages, with file, line and the correction.
  Run it before any commit that adds citations. I negative-tested part 2 by
  planting two bad locators in a scratch file: it caught both, named the lines,
  gave the right corrections, and ignored the good one.
- **`lit/source/pending_text/` is NOT IN GIT** --- `lit/source/` is excluded for
  size, so it exists on this laptop only. It holds Europe PMC full text for
  `mafi2022precoupled` and `youngyang2024tas2r5`, which otherwise survived only
  in `/tmp`. A fresh clone will not have it; do not re-fetch without checking
  here first.
- **The four uncited `refs.bib` entries are deliberate.**
  `mafi2022precoupled`, `youngyang2024tas2r5`, `qin2011preassembly`,
  `nobles2005precoupling` have their `@` stripped so citing one fails loudly.
  They exist because the binding-order sweep was built balanced:
  `bondar2017preassembly` argues *against* pre-assembly and needed the other
  side of a contested question present. `session_start.sh` listing them as
  "no paper behind it" is the guard working, not drift.
- **`lit/GAPS.md` is CURRENT and can be trusted.** (This entry used to say the
  opposite — it was stale at 66 papers. Fixed 2026-09-11 after the lit session
  pointed out that the warning had itself gone stale.) It is now generated by
  `lit/build_gaps.py` from the `unresolved` and `confidence` fields of all 81
  notes — **769 OPEN items across 73 papers**, 20 further items marked RESOLVED
  and excluded — and `lit/corpus_check.sh` fails on drift, so it cannot silently
  age again.
- `lit/MANIFEST.csv` was one row short and is now 79, matching `notes/`.
- **`lit/panels/` is new and committed**, including its 1 MB GPCRdb cache. The
  cache is in *deliberately*: `rebuttals/PANEL_EXPANSION_CLASS_A.md` cites it for
  38 PDB IDs and goes to another team, and a document nobody downstream can check
  is not a rebuttal. Size is not the rule here; provenance is.
- **`lit/source/si/` is 14 MB and correctly excluded** by the existing
  `lit/source/` rule. Re-downloadable: zhang from the npj article page, chiesa
  from the ACS SI link, heo from bioRxiv 10.1101/2021.11.26.470086 **v2** — v1 is
  the wrong file, 55 receptors rather than 68.
- **Never let `_human` be a silent default when resolving a receptor slug.** That
  bug made the lit session report our OPSD pair as cross-species when both
  entries are `opsd_bovin`. Three known non-human resolutions: OPSD bovine,
  B1B1U5 `b1b1u5_9arac` (jumping spider), OPRM `oprm_mouse`.

## When Block D arrives

**Aditya's stated sequence, 2026-09-10: land and audit D, then BRAINSTORM THE
NEXT EXPERIMENTS TOGETHER.** Do not arrive with a chosen experimental programme.
The deliverable at that point is material for a decision — what each title clause
still lacks, the `real`-class suggestions already written (Block B S1, S2, S3 are
the bulk control, the isolated 21-mer arm and the agonist arm), each with its
cost and what it would close. He picks. New predictions are the expensive class
here and almost everything else we have asked for is free or cheap.

Produce D's two ask documents as for the others —
`analysis/block_d/DATA_REQUESTS.md` for the pipeline team and
`rebuttals/BLOCK_D.md` for the orchestrator agent. The convention is in
`CLAUDE.md` under "What we ask the pipeline for".

Invoke the **`blockintake`** skill, and run it in its stated order: **verify the
claim sheet against the data before any panel or sentence.** That order has now
caught something in all three blocks, including one defect that had already
passed a claim sheet, a dispatch and a written draft.

**Block B did not carry the titular peptide claim after all** — this section
used to say it would. Neither A nor B supplies a peptide or an agonist, which is
recorded at the top of `CLAIMS.md`. Whether D closes that gap is Aditya's call.

**Give that distinction a mechanical guard before you start.** Two of four
independent figure agents, both with `CLAIMS.md` in their brief, wrote that the
21-mer was supplied when the whole Gα was — and a third recurrence appeared in
our own outgoing `DATA_REQUESTS.md`, which asked the pipeline agent for "the
α5-CT 21-mer coordinates as supplied to the model". The framing pulls that way — we draw
the α5, name the α5, and the title is about the α5. A written rule catches it at
review; it does not prevent it. It encodes what Block A converged on and
names the eight failure classes that recurred. The order matters: verify the
claim sheet against the data *before* any panel or sentence.

## What was learnt the hard way

- **The claim sheet and the data disagree.** Block A: 21 groups, seventeen of
  which nobody had flagged. The data wins, always, and the disagreement is
  recorded rather than smoothed.
- **Never `git add -A`.** Sessions share one working tree; a commit once
  swallowed another session's five extractions and a 319-line draft. Stage
  explicit paths, and wait for Aditya to say a session has finished.
- **Never filter on `excl_any`** — it removes 54% of Block A.
- **Write prose into the manuscript, not into a markdown draft.** I wrote Block
  A's Results and Methods as `.md` first; from the reader's side the paper had
  no Block A at all until they were `.tex`.
- **"Correct" is not "done" for figures.** The renders were geometrically right
  and visually flat until Aditya supplied exemplars. The depth-of-field
  technique now in `figures/reference/README.md` is the fix.
- **A relayed quote is not a verified quote.** A quote that reached the
  manuscript through a message from another session carried bracketed
  conjugation the source did not have, and two page numbers that were PDF pages
  rather than printed ones. Once one fragment from a relay proves altered, none
  of it can stand as verbatim --- re-source it or de-quote it. Numbers with
  locators are usually stronger than fragmentary quotes anyway.
- **A figure is a verification step, not a presentation step.** Four times, a
  number passed a claim sheet, a dispatch and a written draft and was caught only
  when plotted. Build the panel before trusting the value, and put a guard in the
  panel script that recomputes from rows and refuses to draw what the shipped
  table disagrees with — one such guard fired on its first run.
- **Every apparent discrepancy is your own checker bug until proven otherwise.**
  On all three blocks, the first run was wrong before the drop was. Keep a
  "checked and NOT a finding" section; it is what makes the real findings
  believable.
- **Scope is asserted where it is most read and qualified where it is least
  read.** On 2026-09-11 a section heading, an SI caption title and a build-note
  comment each carried a scope the body text underneath correctly withdrew. When
  a scope changes, grep the SHORT text: headings, caption titles, panel titles,
  ledger status lines.
- **A green build is not a checked build.** `build.sh` reported undefined
  CITATIONS from the day it was written and never undefined REFERENCES, so eight
  `\ref` printed as `??` in `main.pdf` while this file claimed zero. It now
  reports both and greps the built PDF for a literal `??`. `main.tex` uses `xr`
  to import `si.aux`, which is why **build.sh builds the SI first** — that order
  is load-bearing.
- **Never pipe a search through `head` when the question is whether something
  EXISTS.** A peer reported a caveat file absent because `head -2` kept two
  other files' matches; the directory sorted C-C-10 and C-C-11 ahead of C-C-3.
  Count first, look second.
- **Check, don't assume.** Every serious find this session — the CFTR file, the
  receptor-bootstrap mislabelling, the missing MSA column, the title gap — came
  from recomputing something that looked settled.

## Where the state lives

Messages are for asking; files are for remembering.

| file | holds |
|---|---|
| `CLAIMS.md` | the argument spine and the claim-to-block map |
| `analysis/block_a/DISCREPANCY_REPORT.md` | 21 groups where the drop disagrees with itself |
| `analysis/block_a/DATA_REQUESTS.md` | what to ask the pipeline agent for, and open questions |
| `analysis/block_a/LIT_COORDINATION.md` | the five rounds with the lit session |
| `figures/FIGURES.md` | the figure ledger |
| `figures/block_a/FIGURE_PROVENANCE.md` | per-panel source, filter, n, claim |
| `lit/RENDER_CONVENTIONS.md` | how this literature actually draws these figures |
| `lit/PAGE_CONVENTION.md` | the PDF-vs-printed page rule and the seven offsets |
| `SESSIONS.md` | why something changed and what not to redo |
