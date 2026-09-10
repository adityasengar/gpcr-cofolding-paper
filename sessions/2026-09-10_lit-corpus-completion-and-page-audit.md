# 2026-09-10 — lit session: corpus completion, schema v3.1, page-convention audit

Lit session. Owns `lit/**` and `manuscript/sections/intro.tex`. Ran no git; the
orchestrator (paper-6f) committed as `5be77d9`.

## What happened

**The corpus is now fully extracted.** 79 notes against 83 bibliography entries, every
note on schema v3 or v3.1, INDEX/notes/MANIFEST symmetric, zero PDFs without an
extraction. It started this session at 66.

- Aditya supplied the three paywalled PDFs (`chiesa2025templatebias`,
  `bret2025boltz2docking`, `nittinger2025cofolding`), closing the last of the
  bibliography-only entries.
- Extracted four more obtained by other routes: `yu2026domainmotion`,
  `aureli2026epath`, `kohlhoff2014gpcr`, `ingraham2023chroma` (partial).
- Closed the schema-v2 backlog: all five re-passed against their PDFs, not patched —
  `tran2026nanogs`, `ye2026multistatebias`, `obendorf2026statespecific`,
  `waymentsteele2024cluster`, `suzuki2026pairscaling`.
- Extracted `bondar2017preassembly` from a balanced binding-order sweep.
- **SCHEMA v3.1**: added `coinput_composition` and `binding_order`, plus five tags
  (`coinput-confounded`, `conformational-selection`, `induced-fit`, `pre-coupled`,
  `order-agnostic`). Populated for 5 notes of 79 — thin, and recorded as thin.
- Wrote the intro (`manuscript/sections/intro.tex`), then rewrote its gap argument twice
  as the corpus contradicted it.
- Built two durable references from surveys rather than from notes:
  `RENDER_CONVENTIONS.md` (from *viewing* panels) and `PAGE_CONVENTION.md` (from a
  mechanical audit).

## Decisions Aditya made, with reasons

- **Block A is groundwork; Block B carries the titular claim.** The title claims a
  21-residue α5 peptide co-input; Block A's cognate arm supplies the *whole* Gα subunit.
  Consequence: the decoy-arm distinction is Block B's and must not be claimed in Block A.
- **Length does not matter yet; build it properly and trim later.** The intro is a source
  draft at ~4,700 words with ~31 direct quotations, which is 4× a Nature-family
  introduction and carries a verification layer that journals do not. Compression is a
  later, separate pass.
- **Add the binding-order phenomenon to schema and intro.** Prompted the v3.1 fields.
- **Do not run git; the orchestrator commits.** And do not edit `paper/CLAUDE.md` — the
  lit brief is `lit/CLAUDE.md`. Two earlier edits to `paper/CLAUDE.md` were left in place
  as factually correct and mostly superseded.

## What the verification found

- Build green throughout: 38 pages, 65 bibitems, 0 undefined. `verify.sh` all green.
- **Mechanical quote verification caught real errors that reading did not.** Across the
  new notes, ~5 quotes failed and every failure was run down: two were genuine misquotes
  of mine (a paraphrase inside quotation marks in `richman2025conformix`, a mis-transcribed
  sentence in `singhal2025fksteering`); the rest were extraction artifacts — inline
  superscript reference numerals, hyphens lost at line breaks — each annotated in place.
- **The page-convention audit found seven papers** whose printed folio differs from their
  PDF page, three of them cited in sections both sessions had already reviewed. The error
  is invisible by construction: plausible locators, green build, nothing surfaces it until
  a referee cannot find a quote.
- Two false positives in the first version of that check were instructive: a DOI fragment
  (`10.1038/s41467-`**`024`**`-53208-2`) and a decimal (`0.9`**`51`**) both read as folios.
  The check had to be built, not eyeballed.

## What I got wrong and corrected

- **Told the orchestrator `chiesa2025templatebias` has no apo arm. It does.** Its
  AFM-receptor protocol runs the receptor alone through the same model, and AF2/AFM cannot
  accept small molecules, so both its arms are ligand-free. I had conflated its *reference
  structures* (16 of 145 ligand-free) with its *input arms*. My own note flagged AFM-receptor
  as "the one genuinely matched comparison in the paper" and I read past it.
- **Said six notes were on schema v2. It was five** — I miscounted `ingraham2023chroma`,
  which is `v3-partial`, a different thing.
- **Introduced 11 wrong page locators into `intro.tex`** by taking PDF pages from notes.
  Found only because the orchestrator queried one specific quote.
- **Altered a quote and handed it on**: gave `georgiou2025heterogeneity`'s coupling clause
  as "strengthen[s] … stabiliz[es]" with bracketed conjugation. It reached the manuscript
  before being caught. I have stopped bracketing conjugation in quotes.
- **Overstated pre-coupling in the intro**, citing only `georgiou2025heterogeneity`, before
  finding `bondar2017preassembly` — which distinguishes pre-assembly from *basal coupling*
  and bounds any endogenous pre-assembled fraction below ~3%. The passage now presents the
  question as contested.
- **Wrote a wrong system tag** onto `singhal2025fksteering` (`general-protein`, for a
  paper about images and text) and had to remove it; the vocabulary gap is now recorded
  instead of papered over.

## What the next session should not redo

- Do not re-extract anything. 79/79 are done and quote-verified.
- Do not re-audit page offsets by hand — `python3 lit/validate/pageoffset.py` does both
  halves now: which PDFs have an offset, and which *citations* are therefore wrong.
- Do not re-fetch `mafi2022precoupled` or `youngyang2024tas2r5`; full text is parked in
  `lit/source/pending_text/` with provenance.
- Do not treat `hilger2020gcgr` page numbers as convertible — it is an eLocator article
  with no folio, verified by the orchestrator against the printed page.
- Do not re-litigate the four Block A distinctions against `chiesa2025templatebias`: one
  is withdrawn, one reframed to architecture-independence, one (predicate vs
  RMSD-to-reference) survives and is load-bearing, one moved to Block B.
