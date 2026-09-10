# HANDOVER.md — for a fresh orchestrator session

Start in `paper/`. `CLAUDE.md` loads automatically; read it, then this.

## Where the project is

A manuscript on GPCR co-folding. **Block A is written**: Results, Methods, 5 main
figures including a graphical abstract, 16 SI figures, 8 tables. Main text 35
pages, SI 18. Build is clean — 65 bibitems, zero undefined citations.

```bash
./verify.sh                          # everything, and it should be all green
./manuscript/build.sh                # main.pdf and si.pdf
python3 analysis/block_a/verify_claims.py      # 34 checks; 15 mismatches are EXPECTED
./analysis/block_a/check_deliverables.sh       # 7/7
```

## The decisions waiting on Aditya

1. **Pick the graphical abstract.** Five candidates, all built and open:
   `ga1_hero` (three-scene composition, warmest), `ga_style1_pipeline` (safest,
   least memorable by its own account), `ga_style2_population` (most defensible
   — the renders cannot be read as the evidence), `ga_style3_superposition` (the
   only true within-receptor contrast), `ga_style4_axis` (most striking at
   thumbnail; threshold as a place on the page). The two best ideas —
   population-as-hierarchy and threshold-as-place — are separable and could be
   combined.
2. **The steric-exclusion observation** — α5 heavy atoms within 4 Å of TM6:
   52% and 39% against deposited *inactive* structures, 11% against active,
   2–4% against the prediction's own TM6. A mechanical account of why the
   co-input works, but n = 2 receptors and the active control is not zero.
   Needs an import before it can enter Results.

3. **D9** — the reference-set denominator: 89 as previously stated, 98
   empirical, 167 total. Two `[PI]` placeholders sit in `methods.tex`.
4. **D19** — were the 80 threshold rows selected by crystallographic tier, or by
   curated state label? The first leaves the instrument independent of the
   annotation; the second does not. Costs no compute; someone knows.

`analysis/block_a/DATA_REQUESTS.md` is paste-ready for the pipeline agent and
holds these plus six more.

## Parked — raise again later, do not act on it now

**Reframing the study around the distribution of structures the models produce.**
Aditya's idea, 2026-09-10; he asked for it to be parked and brought back.

The case for it, in one paragraph. The introduction argues these models collapse
onto one basin — `abramson2024af3`'s own concession that multiple random seeds do
not approximate the solution ensemble — and then the Results answer that
distributional setup with a scalar. Meanwhile every cell holds 50 predictions
(5 seeds × 10 samples in Block B, 25 seeds in Block A) that get collapsed to one
rate, and that rate is saturated: 115 of 160 cognate cells sit at ≥ 0.98, which
is precisely why the family term is invisible per backbone. A rate hits a
ceiling; a distribution does not.

**The free result that makes it worth raising.** Block B's 5 × 10 is a *nested*
design, so between-seed and within-seed variance separate. Share of within-cell
variance living between seeds, tilt axis:

| backbone | apo | cognate | decoy | shuffled |
|---|---:|---:|---:|---:|
| Boltz-2 | 0.12 | 0.06 | 0.07 | 0.09 |
| Chai-1 | 0.11 | 0.09 | 0.10 | 0.16 |
| OpenFold3 | 0.13 | 0.45 | 0.27 | 0.35 |
| Protenix2 | 0.19 | 0.33 | **0.82** | **0.70** |

NPxxY gives the same pattern, so it is not an axis artefact. The four models
differ in *where their variability comes from*: Boltz-2 explores within a seed,
Protenix2's decoy arm is 82% seed-determined and its ten samples are near
redundant. That is a practical recommendation — more seeds for Protenix, more
samples for Boltz — and a quantitative form of the ensemble-collapse claim the
introduction rests on. The partner also *changes* this on two backbones and not
on the other two.

Reproduce with `python3 analysis/block_b/seed_variance.py`. Nothing in the
manuscript uses it.

**If it is taken up: add a layer, do not replace the instrument.** The binary
predicate is the only part calibrated against deposited structures of known
state, and lit confirmed no paper in 79 conjoins the two axes; dropping it loses
the grounding and the novelty at once.

**The trap that would sink it.** 50 samples from a generative model are **not a
conformational ensemble**. No Boltzmann weighting, no claim to one. It is the
sampling distribution of a generator, and a structural-biology referee stops
reading at the word "ensemble" used loosely.

**Two free checks before committing:** whether cells are genuinely *bimodal*
(some seeds active, some not) rather than merely broad, and whether the same
decomposition holds in Block A's 25-seed design.

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
- **`lit/GAPS.md` is stale and should not be trusted.** It was generated at 66
  papers and reports "358 items across 51 papers"; the corpus is 79. It is the
  pre-citation check, so a stale count is worse than none. Regenerating it is a
  lit job and has not been done.
- `lit/MANIFEST.csv` was one row short and is now 79, matching `notes/`.

## When Block B arrives

Invoke the **`blockintake`** skill. **Block A is groundwork and Block B carries
the titular 21-mer peptide claim** — decided 2026-09-10, recorded at the top of
`CLAIMS.md` with two rules: no Block A sentence may imply the peptide result,
and none may depend on Block B having run.

**Give that distinction a mechanical guard before you start.** Two of four
independent figure agents, both with `CLAIMS.md` in their brief, wrote that the
21-mer was supplied when the whole Gα was. The framing pulls that way — we draw
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
