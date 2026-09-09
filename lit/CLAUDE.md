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
  INDEX.md          71 blocks, one per paper, lossy by design         (load always)
  STATUS.md         landed vs planned experiments                     (load for anything draft-facing)
  GAPS.md           358 unresolved items — what the corpus can't answer
  notes/<key>.md    full extraction, verbatim quotes with pages       (open one at a time)
  pdfs/<key>.pdf    source PDF, filename = citekey                    (open only when the note is too coarse)
  refs.bib          78 entries (71 held + 4 never obtained + 3 bibliography-only).
                    Updated 2026-09-08: five of the eight steering entries were
                    obtained and extracted; every entry's metadata was verified
                    against Crossref, arXiv, PMLR or OpenReview that day.
                    Still citable for venue and identifier ONLY (no note, no PDF):
                    ingraham2023chroma, aureli2026epath, kohlhoff2014gpcr.
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
- **Six notes are still on schema v2** and lack `structural_priors_used`,
  `controls_run` and `si_in_scope` entirely: `obendorf2026statespecific`,
  `suzuki2026pairscaling`, `tran2026nanogs`, `waymentsteele2024cluster`,
  `ye2026multistatebias`. Their A–E content is sound; those three fields are absent,
  not empty. `tran2026nanogs` records its structural priors inside `oracle_leakage`.
- **`g-protein-mimetic` fires on one paper only** (`georgiou2025heterogeneity`, a
  review), because the tag was added in v3 and `tran2026nanogs` — the stapled Gαs α5
  peptide paper, the closest wet-lab analogue of our co-input — predates it. The most
  manuscript-relevant reverse lookup in the vocabulary does not work yet. `atpase`
  fires on zero papers.
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
- **The five notes added 2026-09-08 are v3 but partial on figures.**
  `richman2025conformix`, `singhal2025fksteering`, `wu2023tds`, `kim2023refining` and
  `ekstromkelvinius2024discriminator` carry every schema field, and every claim quote in
  them was machine-verified against the PDF text. Their figure tables were built from
  captions and page positions rather than from viewing the panels, and rows say
  `NOT EXTRACTED (panel not viewed)` where that is so. Do not use them for figure-design
  queries without opening the PDF. Three also carry **no system tag at all**, because the
  fixed vocabulary has no value for a non-biomolecular paper and SCHEMA v3 forbids
  inventing one. **A `non-biomolecular` tag is the outstanding vocabulary decision.**

- **24 of 71 papers carry a reuse restriction** flagged on their `figs:` line — 15 ND,
  3 all-rights-reserved, 6 with no licence statement at all. ND forbids redrawing, not
  just copying. Check before adapting any panel.

## Open — these are the user's calls, not an agent's

- `why_it_matters` in `MANIFEST.csv` and `stance` in `INDEX.md` are unfilled/provisional.
- Seven papers have a verified bibliography entry but no note and no PDF, so they are
  citable for venue and identifier only. Four were never obtained and all four are
  paywalled: `chiesa2025templatebias` (JCIM 65(12):6298-6309), `bret2025boltz2docking`
  (JCIM 66(3):1511-1521), `nittinger2025cofolding` (AILSCI 8:100136, gold OA but the
  publisher blocks scripted download), `yu2026domainmotion` (PNAS 123(10):e2530709123).
  Three more are the steering/MD entries that could not be fetched: `ingraham2023chroma`
  (Nature 623(7989):1070-1078), `aureli2026epath` (JPC Lett 17(10):2974-2983),
  `kohlhoff2014gpcr` (Nature Chem 6(1):15-21). All seven need institutional access; the
  metadata is verified, only the full text is missing.
- `STATUS.md` says Block A is 48 receptors; other notes reference a 46-receptor panel
  and 40 reference pairs. Unreconciled, and not resolvable from the corpus.
- The five v2 notes need a real re-pass, not a patch: the three missing fields require
  reading the papers again.
