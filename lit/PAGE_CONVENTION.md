# PAGE_CONVENTION.md — PDF page vs printed folio

**The rule: `notes/` record PDF page numbers. Manuscripts must cite printed folios.**

For most of the corpus these are the same, because preprints and article-number journals
(Nature Communications, PLOS, npj) paginate from 1. For an article printed in a continuously
paginated volume they are not, and a citation built from the PDF page sends a reader to a page
that does not exist in the published article.

This was found on 2026-09-10 only because the orchestrator queried one specific quote:
`georgiou2025heterogeneity` notes carry PDF pages, the article is printed at 3691–3728, and five
citations in `manuscript/sections/intro.tex` pointed at pages 4–9. It is exactly the class of
error that is invisible until a referee cannot find a quote.

## The standing check

```
python3 validate/pageoffset.py
```

Run it whenever a PDF is added to `pdfs/`. It samples PDF pages 2–7, finds the offset *k* such
that `pdf_page + k` appears on each, and validates it two ways:

1. **Against `refs.bib`** — if the entry has a `pages` field, *k* is confirmed only when it equals
   `first_page − 1`. This is authoritative, so **adding a `pages` field to a journal entry is the
   best thing you can do for this check.**
2. **Against the running header/footer** — used only when `refs.bib` has no page range. The folio
   must appear as a standalone token in the first or last two lines of a page, and lines carrying
   a DOI, URL or arXiv id are skipped. Without those two guards the check returns false positives:
   `tejero2024opsin` matched "24" inside `10.1038/s41467-024-53208-2`, and `liu2026ensembletests`
   matched "95" inside "0.951".

## Papers needing conversion, as of 2026-09-10

| citekey | printed = pdf + | how confirmed |
|---|---|---|
| `abramson2024af3` | **+492** | refs.bib, Nature 630:493–500 |
| `chiesa2025templatebias` | **+6297** | refs.bib, JCIM 65:6298–6309 *(this note already uses printed pages — do not convert twice)* |
| `georgiou2025heterogeneity` | **+3690** | refs.bib, ACS Pharmacol Transl Sci 8:3691–3728 |
| `yang2025statespecific` | **+11424** | refs.bib, JCIM 65:11425–11438 |
| `gilson2025casp16` | **+248** | running folio; no page range in refs.bib yet |
| `heo2022multistate` | **+1872** | running folio; no page range in refs.bib yet |
| `waymentsteele2024cluster` | **+831** | running folio; no page range in refs.bib yet |

Every other PDF in the corpus is 1-indexed or carries no folio.

**`hilger2020gcgr` is exempt and must be checked by hand.** It is the corpus's one scanned paper,
its PDF text layer is 17 bytes, and quotes come from an OCR pass cached at
`validate/pages/hilger2020gcgr.txt`. It is *Science* eaba3373, an eLocator article with no page
range at all, so PDF page **is** the article page and there is nothing to convert. Verified
against the printed page by the orchestrator on 2026-09-10.

## What was fixed on discovery

`manuscript/sections/intro.tex`, 11 citations converted 2026-09-10: `georgiou2025heterogeneity`
p.4→3694, p.6→3696 (×2), p.8→3698, p.9→3699; `abramson2024af3` p.6→498 (×2);
`heo2022multistate` p.1→1873, p.3→1875; `yang2025statespecific` p.2→11426, p.10→11434.
`results.tex` and `methods.tex` were converted separately by the orchestrator.

## Two things still open

- `gilson2025casp16`, `heo2022multistate` and `waymentsteele2024cluster` have no `pages` field in
  `refs.bib`. Adding one would move them from folio-confirmed to bib-confirmed. I did not add them
  because I could verify the first page but not the last: their PDFs include supplementary or
  extended-data pages beyond the printed article, so page count is not a safe end bound.
- The offsets above are recorded but the **notes themselves were not rewritten.** Notes still hold
  PDF pages by design; conversion happens at citation time. If that ever changes, it must change
  for all 79 at once or the two conventions will mix silently.
