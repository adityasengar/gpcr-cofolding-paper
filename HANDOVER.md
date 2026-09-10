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

## The three decisions waiting on Aditya

1. **The title outruns Block A.** The title and intro claim a 21-residue α5
   C-terminal *peptide* co-input; Block A supplies the *whole cognate Gα*.
   Either a later block carries the titular claim with Block A as groundwork, or
   the title and intro are rewritten. See the top of `CLAIMS.md`. **Do not let
   this close quietly.**
2. **D9** — the reference-set denominator: 89 as previously stated, 98
   empirical, 167 total. Two `[PI]` placeholders sit in `methods.tex`.
3. **D19** — were the 80 threshold rows selected by crystallographic tier, or by
   curated state label? The first leaves the instrument independent of the
   annotation; the second does not. Costs no compute; someone knows.

`analysis/block_a/DATA_REQUESTS.md` is paste-ready for the pipeline agent and
holds these plus six more.

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

## When Block B arrives

Invoke the **`blockintake`** skill. It encodes what Block A converged on and
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
| `SESSIONS.md` | why something changed and what not to redo |
