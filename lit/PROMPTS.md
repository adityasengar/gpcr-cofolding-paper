# PROMPTS.md — what to paste, and in what order

Two prompts, run as **separate turns**. Do not merge them. If one session both
extracts and writes the intro, it writes the intro from what it remembers of the
PDFs and backfills the index to agree with it. The result reads well and is not
grounded in anything.

---

## Prompt 1 — build the corpus

Paste into the lit-review chat that already holds the papers.

> You are building a queryable literature corpus, not writing prose. Nothing you
> produce in this turn is a draft of anything.
>
> Read `SCHEMA.md` first. It defines the fields and the fixed tag vocabulary.
>
> **Step 0 — inventory.** List every paper you have. For each: citekey, DOI,
> whether you hold the full text or only an abstract. Papers where you have only
> an abstract get extracted anyway but are marked `confidence: low` and listed
> separately at the end. Show me this list and the count before extracting.
>
> **Step 1 — extract.** One paper at a time. For each, write
> `notes/<citekey>.md` containing every field in `SCHEMA.md` in schema order.
> Rules that matter more than completeness:
>
> - Read only the paper you are extracting. Do not fill a field from memory of
>   the literature or from what a similar paper did.
> - `NOT REPORTED` is a correct and expected answer. A note where every field is
>   populated is more suspicious than one with gaps.
> - `oracle_leakage` and `necessity_claims` are quoted **verbatim with page
>   numbers**. Paraphrase softens exactly the sentences whose strength matters.
> - The figure table needs a row per figure with `page` and `data_shape` filled.
>   `data_shape` is written as `<n conditions> × <n levels> → <what is on each
>   axis>`. This field is what later lets me ask "I have data shaped like X, what
>   figure should I make" — a plot-type label alone cannot answer that.
> - Tags come only from the fixed vocabulary in `SCHEMA.md`. If a paper needs a
>   tag that does not exist, stop and tell me rather than inventing one.
>
> **Step 2 — index.** Write `INDEX.md`: one block per paper, 4–6 lines, in this
> shape. Keep it terse — this file loads on every future query, so it must stay
> small enough that the whole corpus fits at once.
>
> ```
> ### <citekey> — <year>, <venue>
> claim: <one line>
> system/method: <system> | <method_class> | <backbones>
> states: <states_generated> | metric: <state_metric> | prospective: <yes/no/partial>
> oracle: <one line, or NONE FOUND>
> figs: <n> (exemplars: <fig nos worth revisiting>)
> tags: <tags>
> stance: <precedent|contrast|threat|background> — <why, one line>
> ```
>
> **Step 3 — bibliography.** Write `refs.bib` with one entry per citekey, built
> only from DOIs you actually resolved. If you cannot resolve a DOI, put the entry
> in a `UNRESOLVED.md` list instead of guessing. A fabricated reference in a
> submitted preprint is expensive to discover late.
>
> **Step 4 — report.** Tell me: how many papers extracted; which are
> `confidence: low`; every `unresolved` item; any paper where `oracle_leakage`
> was hard to determine. Do not summarise the literature. Do not tell me what the
> gap is. That is the next turn's job and I want it done against the index, not
> against your memory of reading.

---

## Prompt 2 — the two-page introduction

Run only after Prompt 1 has finished and you have skimmed `INDEX.md` yourself.

> Write `draft/intro.md`, targeting two printed pages.
>
> Work **only from `INDEX.md` and `notes/`**. Do not reopen the PDFs. If the
> index does not support a sentence you want to write, the sentence does not go
> in — tell me what was missing instead.
>
> Read `STATUS.md` before writing. It lists which experimental blocks have landed
> and which are planned. Do not write a single clause that depends on a planned
> block. This is the easiest error to make and the hardest to catch by rereading,
> because the sentence will be well-formed and consistent with everything else in
> the draft.
>
> Structure:
>
> 1. **Problem.** Why conformational state matters for this receptor class, and
>    why single-structure prediction is insufficient.
> 2. **What has been tried.** Grouped by approach, not one-paper-per-sentence.
>    Every group cites specific citekeys.
> 3. **The gap.** Built by reading down the `oracle_leakage`, `prospective`,
>    `states_generated` and `anti_memorization` columns. State it as what the
>    corpus does and does not contain, and name the nearest counterexample
>    explicitly. A gap paragraph that names no near-miss is not credible.
> 4. **What we do.** Landed blocks only.
> 5. **Contributions.** Three or four, each falsifiable.
>
> Every sentence carrying a claim about prior work ends with `[citekey]` or
> `[citekey p.N]`. When contrasting against a necessity claim, quote the original
> verbatim from the note rather than characterising it.
>
> When finished, list every citekey used and confirm each exists in `refs.bib`
> and has a note file. Then tell me which sentences you were least confident in.
