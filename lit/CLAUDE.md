# CLAUDE.md — the literature corpus for the α5-CT conformational-control manuscript

Everything in this folder supports one manuscript. Read this file, then `SCHEMA.md`
and `INDEX.md`, before answering anything about prior work.

## The claim the corpus exists to defend

For GPCRs, a 21-residue Gα α5 C-terminal peptide supplied as a **co-input** drives
Boltz-2 / OpenFold3 / Protenix / Chai-1 into the **active** state; the agonist alone
does not; and model confidence does not track state correctness.

Three things follow. The corpus must be able to show what prior work did and did not
do on that axis. It must supply verbatim necessity and novelty claims to argue
against. And it must never let a general-knowledge answer masquerade as a corpus
finding — that failure is invisible on the page and is caught by a reviewer instead.

## Layout

```
lit/
  SCHEMA.md         field definitions + the fixed 60-tag vocabulary   (load always)
  INDEX.md          78 blocks, one per paper, lossy by design         (load always)
  STATUS.md         landed vs planned experiments                     (load for anything draft-facing)
  GAPS.md           358 unresolved items — what the corpus can't answer
  notes/<key>.md    full extraction, verbatim quotes with pages       (open one at a time)
  pdfs/<key>.pdf    source PDF, filename = citekey                    (open only when the note is too coarse)
  refs.bib          78 entries, **all 78 extracted**. No bibliography-only entries
                    remain: the last three were supplied by the user on 2026-09-09.
                    All 78 entries' metadata verified 2026-09-08/09 against
                    Crossref, arXiv, PMLR, OpenReview or OpenAlex. Every entry now has
                    a note. Four have no PDF - see below.
  MANIFEST.csv      citekey, DOI, pages, sha256, fulltext
  validate/         quote and page verifiers + cached text
  source/           the original download folder, kept for provenance
  draft/            manuscript sections — EMPTY, and see the two-pass rule below
  staleness.sh      lists PDFs with no extraction (currently zero)
  pagetext.sh       prints a paper with ===== PAGE n of N ===== markers
```

`source/pdf` and `source/gap` hold the same files as `pdfs/` under their original
download names, as **hard links** — same inodes, no duplicated disk. Do not "clean
up" one side expecting to reclaim space, and do not delete `pdfs/` names.
`source/extra` holds two PDFs that were **never extracted** and are not in the corpus.

## How to query

Use the `litquery` skill. It resolves the corpus root itself and works whether the
session starts in `paper/` or in `paper/lit/`. The tiering is the whole design:
`SCHEMA.md` + `INDEX.md` fit in context together and answer most questions in one
hop; open one note when the index is too coarse; open a PDF only when the note is.
Never load the whole `notes/` directory.

## Rules that produced this corpus and still apply

- Every claim about a paper carries a locator: `[citekey]` or `[citekey p.N]`.
- Quote necessity and novelty claims **verbatim** from the note. Paraphrase softens
  exactly the sentences the manuscript argues against.
- **Never answer a manuscript-bound question from `INDEX.md` alone.** An index line
  saying "binary predicate" does not carry the threshold or whether it saturated.
- If the corpus does not contain the answer, say so. "The corpus does not cover this;
  the closest is X" is a useful answer. An invented one is not distinguishable from a
  real one on the page.
- **Read `STATUS.md` before any sentence that touches the draft.** Blocks A, B and C
  have landed. D1, D2, D3 have not run. No draft sentence may depend on a planned
  block — that error is well-formed, internally consistent, and nearly impossible to
  catch by rereading.
- **Two-pass rule: never extract and draft in the same session.** A session that does
  both writes the paragraph first and retrieves whatever supports it. `draft/` is
  empty on purpose; `PROMPTS.md` holds the drafting prompt to run separately.

## Known limits — check these before citing

- **Page citations are ~76% exact, ~80% within one page.** Verify by searching the
  PDF text, not by turning to the cited page.
- **Quote accuracy is high.** 1,043 necessity/novelty strings were checked
  mechanically against the PDF text: 99.2% verified. Every residual was run down and
  was a text-extraction artifact — OCR on the one scanned paper (`hilger2020gcgr`),
  `ﬁ` ligatures, inserted spaces, or dropped superscript reference numerals. **No
  fabricated quote was found anywhere in the corpus.**
- **The schema-v2 backlog is closed. All 78 notes are v3** and all 78 carry
  `structural_priors_used`, `controls_run` and `si_in_scope`. The five that were v2 were
  re-passed on 2026-09-09 by re-reading each PDF, not by patching: `tran2026nanogs`,
  `ye2026multistatebias`, `obendorf2026statespecific`, `waymentsteele2024cluster`,
  `suzuki2026pairscaling`. In every case the A–E content of the original pass was checked
  and stands; nothing in it needed correcting. Every added quote was machine-verified
  against the PDF text, and the handful that failed were run down and were all
  extraction artifacts (inline superscript reference numerals, hyphens lost at line
  breaks), each annotated in place. The one exception to full v3 is
  `ingraham2023chroma`, which is `v3-partial` for a different reason: its Results and
  Methods were never retrieved.

  Two corpus defects were fixed as part of that work. **`suzuki2026pairscaling` gained
  `latent-steering`**, which it had always lacked despite being a pair-representation
  intervention whose own abstract calls it *"systematic latent space steering"*; that
  reverse lookup now returns 10 papers instead of 9.
  **`tran2026nanogs` was re-passed to v3 on 2026-09-09** — re-read against the PDF, not
  patched. Its A–E content was checked and stands; the three missing fields were
  extracted fresh and all eleven added quotes machine-verified. Its `controls_run` table
  is the most reusable content in the note, and it records two *absent* controls: no
  scrambled-sequence peptide, and no Gi/Gq selectivity assay (the authors say why).
- **`g-protein-mimetic` now fires on two papers**, `georgiou2025heterogeneity` (a
  review) and `tran2026nanogs`, which gained the tag in its 2026-09-09 v3 re-pass. That
  reverse lookup — the most manuscript-relevant one in the vocabulary — works now.
  `tran2026nanogs` also gained `experimental`. `atpase` still fires on zero papers.
- **The `oracle-leak` tag is narrower than the `oracle:` line.** Six papers name
  oracle routes but carry neither oracle tag, each declining it deliberately and with
  reasoning. Build the gap argument by reading down the `oracle:` lines, not by
  grepping the tag, or you will undercount.
- **Some INDEX numbers are derived, not printed in the paper.** `paajanen2026activation`'s
  "1351 class A structures" is the sum of Supplementary Table 1 (1006 train + 345 test),
  cross-checked against Supplementary Table 2. Correct, but a reviewer will not find
  the string "1351" in that paper.
- **Chai-1 trains on PDB *and* AlphaFoldDB.** The 2021-01-12 cutoff applies to PDB
  structures; PDB70 is the template database. Do not write "Chai-1 saw nothing after
  January 2021". The other cutoffs are corroborated by independent third-party notes:
  AF3 2021-09-30 (PoseBusters model 2019-09-30), Boltz-1 2021-09-30, Boltz-2
  2023-06-01 for structures with **no date cutoff on affinity data**, Protenix 2021-09-30.
- **Four notes have NO PDF and therefore NO page numbers.** `yu2026domainmotion`,
  `aureli2026epath`, `kohlhoff2014gpcr` and `ingraham2023chroma` were extracted on
  2026-09-09 from publisher HTML or Europe PMC full-text XML, because every scripted
  route to their PDFs is bot-walled. Their locators are **section names**, not pages:
  cite as `[yu2026domainmotion, Discussion]`. Every claim quote in them was machine-
  verified against the retrieved text, so they are searchable and checkable; they are
  simply not page-addressable. `kohlhoff2014gpcr` was read as the **NIH author
  manuscript**, not the published typesetting, and **has a 2015 corrigendum that was not
  retrieved** — check it before citing. `ingraham2023chroma` is worse: it is marked
  `schema_version: v3-partial` because its Results, Methods and all figures were never
  read. **Do not use that note for a novelty, priority or figure-design argument.**

- **`yu2026domainmotion` is a threats-table paper and is not yet in `../CLAIMS.md`.**
  It shows, on 82 enzymes at 500 models per condition, that a ligand *known not to bind*
  induces nearly the same domain motion as the native trigger, and that pLDDT does not
  reliably separate them. Any decoy-arm interpretation has to meet it.

- **The five notes added 2026-09-08 are v3 but partial on figures.**
  `richman2025conformix`, `singhal2025fksteering`, `wu2023tds`, `kim2023refining` and
  `ekstromkelvinius2024discriminator` carry every schema field, and every claim quote in
  them was machine-verified against the PDF text. Their figure tables were built from
  captions and page positions rather than from viewing the panels, and rows say
  `NOT EXTRACTED (panel not viewed)` where that is so. Do not use them for figure-design
  queries without opening the PDF. Three also carry **no system tag at all**, because the
  fixed vocabulary has no value for a non-biomolecular paper and SCHEMA v3 forbids
  inventing one. **A `non-biomolecular` tag is the outstanding vocabulary decision.**

- **Two open vocabulary decisions, both blocking clean reverse lookup.** (1) A
  `non-biomolecular` system tag: `singhal2025fksteering`, `kim2023refining` and
  `ekstromkelvinius2024discriminator` carry **no system tag at all**, because the fixed
  list has no honest value for a paper about images, text or 2-D molecular graphs.
  (2) The `af-cluster` tag now has a genuine collision: it means MSA clustering
  everywhere except `kohlhoff2014gpcr`, where it marks a Markov state model. Either
  rename it or add `markov-state-model`.

- **24 of 78 papers carry a reuse restriction** flagged on their `figs:` line — 15 ND,
  3 all-rights-reserved, 6 with no licence statement at all. ND forbids redrawing, not
  just copying. Check before adapting any panel.

## Open — these are the user's calls, not an agent's

- `why_it_matters` in `MANIFEST.csv` and `stance` in `INDEX.md` are unfilled/provisional.
- **`bret2025boltz2docking` was read from the HAL author version**, not the published
  ACS typesetting, so its locators are author-version PDF pages and do **not** match
  JCIM 66(3):1511-1521. Convert before citing. `chiesa2025templatebias` and
  `nittinger2025cofolding` are published versions and their page numbers are real.

- **`chiesa2025templatebias` narrows the manuscript's novelty claim and the intro is
  written against it.** It supplies a G protein as a co-input to a co-folding model and
  then measures the receptor's activation state - both halves, on 63 post-cutoff class A
  pairs. Nothing else in the corpus does both. Our remaining distinctions are the 21-mer
  peptide versus the whole Ga, an operationalised predicate versus RMSD to the deposited
  answer, the decoy and shuffled arms, and the AF3-lineage backbones. Read that note
  before writing any novelty sentence.
- `STATUS.md` says Block A is 48 receptors; other notes reference a 46-receptor panel
  and 40 reference pairs. Unreconciled, and not resolvable from the corpus.
- The five v2 notes need a real re-pass, not a patch: the three missing fields require
  reading the papers again.
