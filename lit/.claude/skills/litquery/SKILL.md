---
name: litquery
description: Query the paper_af3 literature corpus while writing the manuscript. Use this skill whenever the user asks anything that touches prior work — which papers did X, what did paper Y measure, show me their figures, what figure should I make for this data, does the corpus contradict a claim I am about to make, or which sentences in a draft need citations. Trigger it even when the user does not mention the corpus by name: any question about what other papers have done, any request to check or support a claim about prior work, and any figure-design question while drafting results should go through this skill rather than being answered from general knowledge.
---

# litquery

Answer questions about the literature corpus while the manuscript is being
written. This skill **retrieves and verifies**. It does not draft prose — see
"What this skill does not do" below.

## Resolve the corpus root first

Every path below is written `$LIT/...`. Set it once per session so the skill works
whether you started in the project root or inside the corpus folder:

```bash
LIT=$( [ -f INDEX.md ] && echo . || echo lit ); echo "corpus root: $LIT"
```

If neither resolves, you are not in this project — say so rather than guessing.

## Corpus layout

```
$LIT/            (= ./lit from the project root, or . from inside it)
  SCHEMA.md        field definitions + fixed tag vocabulary   (load always)
  INDEX.md         4–6 lines per paper, all papers            (load always)
  STATUS.md        which blocks have landed vs. planned       (load for any draft-facing query)
  notes/<key>.md   full extraction, quotes with page numbers  (load one at a time)
  pdfs/<key>.pdf   source                                     (open only when the note is insufficient)
  refs.bib
  draft/           manuscript sections in progress
```

The tiering is the point. `SCHEMA.md` + `INDEX.md` fit in context together; most
questions are answerable there in one hop. Open a note when the index is too
coarse. Open a PDF only when the note is too coarse or the claim is
manuscript-bound. Never load the whole `notes/` directory.

## Before answering anything: the staleness check

Run this first, every session:

```bash
comm -23 <(ls $LIT/pdfs/*.pdf | xargs -n1 basename | sed 's/\.pdf$//' | sort) \
         <(ls $LIT/notes/*.md  | xargs -n1 basename | sed 's/\.md$//'  | sort)
```

Any citekey printed is a paper on disk with no extraction. Say so before
answering, and treat every "no paper does X" answer as provisional until the gap
is closed. This matters more than it looks: the corpus grows continuously, and an
un-extracted paper is invisible to every query. Answering "nothing in the corpus
does X" while the paper that does X sits unextracted is the highest-cost failure
this skill can produce, because the answer is confident, well-formed, and wrong
in the direction that most flatters the manuscript's novelty claim.

## Provenance rules

These apply to every answer, in every query class.

- Every factual claim about a paper carries a locator: `[citekey]` for
  index-level, `[citekey p.N]` for note- or PDF-level.
- **Never answer from the index when the answer will become a manuscript
  sentence.** Index entries are compressed and lossy. An entry that says
  "binary predicate, TM6 distance" does not tell you the threshold, its
  justification, or whether it saturated. Open the note; if the note does not
  have it, open the PDF.
- If the corpus does not contain the answer, say so plainly. Do not reason from
  general knowledge of the literature and present it as a corpus finding. An
  answer of "the corpus does not cover this; the closest is X" is useful. An
  invented answer is indistinguishable from a real one on the page and is
  discovered by a reviewer instead.
- Quote necessity and impossibility claims verbatim from the note. These are the
  sentences the manuscript argues against, and paraphrase reliably softens them.

## Query classes

### 1. Point lookup — "what did paper X do"

Index first. If the question is about a specific value, threshold, control or
method detail, go to the note. Answer with the fields, not with a summary of the
paper.

### 2. Reverse lookup — "which papers did X"

Grep `INDEX.md` on tags and field values. This is the most common query while
drafting and the one the tag vocabulary exists for.

```bash
grep -B4 -A2 'oracle-leak' $LIT/INDEX.md
```

Report the hits **and** the near-misses that the tag filter excluded but that a
reader might expect to see, with one line each on why they were excluded. A bare
list invites the assumption that the filter was perfect.

### 3. Figure retrieval — "show me their figure 3"

The note's figure table gives figure number → page. Extract from that page only:

```bash
# rasterize the page for viewing
pdftoppm -f <page> -l <page> -r 150 -png $LIT/pdfs/<key>.pdf /tmp/<key>_p<page>
# or pull embedded images from that page
pdfimages -f <page> -l <page> -png $LIT/pdfs/<key>.pdf /tmp/<key>_fig
```

Then view the PNG. If the figure table has no page for that figure, say so rather
than scanning the document — a missing page number means the extraction was
incomplete, and that is worth knowing.

Reproduction in the manuscript needs the `reuse` field checked. Flag it whenever
the user talks about *using* rather than *seeing* a figure.

### 4. Design by analogy — "I have this data, what figure should I make"

The hardest class and the one most likely to fail silently.

Match on `data_shape`, not on subject matter. The user describes the shape of
what they have — number of conditions, number of levels, continuous or
categorical, per-system or pooled — and the job is to find figures in the corpus
built on a similar shape, whatever protein they were about. A paper tagged
`figure-exemplar` may be from an unrelated field and is fair game here (and only
here — exclude those papers from gap analysis, where they would pollute the
novelty argument).

For each suggestion give: the citekey and figure number, the data shape it was
built on, how it maps onto the user's data, and the page so they can look at it.

**If the corpus has no close analogue, say that.** "Nothing here plots a four-way
arm comparison across four backbones; the closest is `<key>` fig 2, three
conditions on one system" is a more valuable answer than five plausible
suggestions, because it tells the user the figure is novel — which is itself
information about the manuscript. The failure mode to avoid is generating
figure ideas from general design sense and decorating them with citations; that
output is indistinguishable from a grounded answer and is worse than useless.

Also surface the `hides` field on any near-match. Figures that bury their own
result — pooled where per-system was needed, bars over distributions, axes pinned
at a ceiling — are the most instructive examples in the corpus, and this campaign
has already had one headline result inverted by exactly that class of mistake.

### 5. Claim audit — "check this against the corpus"

The highest-value class. The user states a claim they are about to write, or
points at a draft section.

For a single claim: identify which schema fields would falsify it, filter the
index on those, open the notes for every candidate, and report the **nearest
counterexample** with a verbatim quote and page — even when it does not
ultimately defeat the claim. Then state plainly whether the claim survives, and
what qualifier would make it survive if it does not.

For a draft section, report:

- sentences making a novelty, priority or contrast claim with no citation;
- citations present in the draft but absent from `refs.bib` or `notes/`
  (fabrication check — run this mechanically);
- cited papers doing no work in the argument, which can be cut;
- **any sentence depending on a block marked planned in `STATUS.md`.**

That last check exists because a draft written around results that do not exist
yet is well-formed, internally consistent, and nearly impossible to catch by
rereading. It is the same failure that has recurred throughout this campaign in
other costumes: a stage runs correctly against the wrong upstream and reports
success.

## What this skill does not do

**It does not write manuscript prose.** Hand back citekeys, page numbers, quoted
claims and gaps; the user or a separate drafting session turns those into
sentences.

The reason is structural, not stylistic. An agent that both retrieves and drafts
writes the paragraph first and then retrieves whatever supports it. The retrieval
becomes decoration for a conclusion already reached, and the output looks exactly
like the grounded version. Keeping retrieval in its own session with its own
skill means the citations came before the sentence rather than after it.

Short connective phrasing when reporting findings is fine. Paragraphs destined
for the manuscript are not.

## Answer shape

Lead with the direct answer. Then the evidence with locators. Then, only if
relevant, what the corpus does not cover.

Do not restate the question, do not summarise the corpus, and do not pad with
context the user already has — they are mid-sentence in a manuscript and want the
locator.
