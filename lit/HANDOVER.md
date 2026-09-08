# HANDOVER.md — compact prompt and restart prompt

Two prompts. The first is for `/compact` in THIS session. The second is a
self-contained brief to paste into a FRESH session.

---

## 1. Paste after `/compact`

```
Compact this conversation. It was a literature-corpus build for a GPCR / co-folding
manuscript. Keep the following and discard the rest.

KEEP — corpus state:
- 66 papers extracted at /Users/aditya/Documents/tools/Novartis_projects/paper/lit
  (pdfs/, notes/, INDEX.md 66 blocks, refs.bib 70 entries, SCHEMA.md v3,
  MANIFEST.csv, validate/, staleness.sh, pagetext.sh). Zero un-extracted.
- The litquery skill at .claude/skills/litquery/SKILL.md: loads SCHEMA + INDEX,
  opens one note, opens a PDF only when the note is too coarse.
- STATUS.md distinguishes LANDED blocks A/B/C from PLANNED D1/D2/D3. No draft
  sentence may depend on a planned block.

KEEP — findings that bear on the manuscript, with their papers:
- AlphaFold3's own paper concedes ligand-blindness and ensemble collapse
  (abramson2024af3 p6). Strongest available citation.
- Three multi-state benchmarks exclude GPCR activation by a TM-score 0.8 rule
  (bryant2024cfold, kalakoti2026afsample3, ku2026promise). ProMiSE names
  "GPCR TM6 displacement" as excluded in its own text.
- The closest peptide prior art (yang2025statespecific) has the OPERATOR pick the
  state via state-matched templates; the peptide is the designed output. The
  alpha5-CT co-input claim is not pre-empted.
- Two wet-lab results complicate the mechanism story: tran2026nanogs shows the
  isolated alpha5-CT peptide does NOT stabilise the active state without agonist,
  and vo2026fiducials shows a high-efficacy agonist alone drives TM6 nearly fully
  out without G protein, with the alpha5 helix adding under 1 Angstrom.
- ku2026promise finds partner-induced changes predicted WORSE than ligand-induced,
  with different failure modes. A reviewer will reach for this.
- Model training cutoffs: AF3 2021-09-30 (PoseBusters model 2019-09-30);
  Boltz-1 2021-09-30; Boltz-2 2023-06-01 structures only, affinity data has no
  date cutoff; Chai-1 2021-01-12 (PDB/PDB70 only); Protenix 2021-09-30.

KEEP — corrections I made to my own earlier claims in this conversation:
- I first called tran2026nanogs supporting evidence; the full extraction shows it
  is a contrast.
- I first recommended khaleq2026hyaline as a state metric; its decision boundary
  is never stated and its split is temporal only with no receptor holdout.
- I first called parikh2026allosteric's architecture-independence its strength;
  four of its five models are AlphaFold3-lineage and protenix2025's own paper
  confirms Protenix is not architecturally independent of AF3.

KEEP — open items owned by the user:
- why_it_matters in MANIFEST.csv and stance in INDEX.md are both unfilled/provisional.
- Four papers not obtained: chiesa2025templatebias, bret2025boltz2docking,
  nittinger2025cofolding, yu2026domainmotion.
- STATUS.md says Block A is 48 receptors; other notes reference a 46-receptor panel
  and 40 reference pairs. Unresolved.
- Batch-1 notes carry schema v2 figure tables and tags; substance is unaffected.

KEEP — validation result:
- 3,425 quotes checked mechanically; 88.6% verified verbatim; 18/18 headline quotes
  verified; zero fabrications found. Page citations are weaker: about 76% exact,
  80% within one page, so search the PDF rather than trusting the cited page.

DISCARD: per-batch mechanics, token counts, subagent orchestration details, tool
debugging (pdftotext column splits, tesseract temp-dir failure, launchd TCC failure),
and settings.json changes.
```

---

## 2. Paste into a fresh session

Start the session in `paper/lit/`. The prompt is short now because `CLAUDE.md`
carries the detail and is loaded automatically.

```
Read CLAUDE.md in this directory first, then SCHEMA.md and INDEX.md.

I am writing a manuscript arguing that for GPCRs a 21-residue Ga alpha5 C-terminal
peptide supplied as a co-input drives Boltz-2 / OpenFold3 / Protenix / Chai-1 into
the active state, that the agonist alone does not, and that model confidence does
not track state correctness.

This folder is the literature corpus that has to defend that claim: 66 extracted
papers, one note each, with verbatim quotes and page numbers. Query it with the
litquery skill — load SCHEMA.md + INDEX.md, open ONE note, and open a PDF only when
the note is too coarse. Never answer a manuscript-bound question from INDEX.md alone,
and never answer from general knowledge and present it as a corpus finding.

Read STATUS.md before anything touching the draft: blocks A, B and C have landed,
D1, D2 and D3 have NOT run, and no draft sentence may depend on a planned block.
Read GAPS.md before citing a paper — it lists what each extraction could not
determine. The "Known limits" section of CLAUDE.md lists the caveats that will
otherwise bite: page citations are only ~76% exact, five notes are still on schema
v2, and some INDEX numbers are derived rather than printed in the paper.

Start by telling me what you have loaded and what you can answer. Then wait.
```

## Notes on using these

The compact prompt is deliberately explicit about what to DISCARD, because most of
this session was orchestration mechanics that carry no manuscript value.

The restart prompt ends with "then wait" on purpose. A fresh session that starts
answering immediately will answer from general knowledge before it has read the
corpus, which is the failure the whole two-pass design exists to prevent.

## Layout note (2026-09-08)

Everything literature-related now lives in `paper/lit/`. The old `paper/papers/`
download folder is `lit/source/` — its PDFs are hard links to `lit/pdfs`, same
inodes, so deleting either side reclaims no space. `lit/` must keep its name: the
skill, these prompts and all three shell scripts hardcode it.

`SKILL.md` exists twice on purpose — `paper/.claude/` and `lit/.claude/` — so the
skill is found whichever directory a session starts in. Edit one, copy to the other.

