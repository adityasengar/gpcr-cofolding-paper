# cheng2026af3cluster

> **PDF SUPPLIED 2026-09-14 and now held at `pdfs/cheng2026af3cluster.pdf` (13 pp).**
> Title confirmed: *"Generalized Multi-State Protein Design with AlphaFold3"*, Cheng, Guo, Seo,
> Goverde & Jin, GEM workshop @ ICLR 2026. **The `abstract-only` restriction below is now
> LIFTED in principle — the body is readable — but this note has NOT yet been re-passed, so
> every body-level field in it is still UNVERIFIED and must not be quoted.** A full v3.2 pass is
> owed and is the highest-value one outstanding, because this is the novelty-boundary paper for
> "MSA clustering + AF3, best on binder-mediated transitions".


> **EXTRACTION PROVENANCE — READ BEFORE CITING.** Extracted 2026-09-10 from the **OpenReview
> abstract page only**, read directly in a browser. **The PDF was NOT retrieved**: openreview.net
> returns 403 to scripted requests and its in-browser viewer rendered blank; the download link did
> not produce a file. Every statement below sourced to the abstract is verbatim and verified by me.
> Every statement marked `[SUBAGENT — UNVERIFIED]` came from a subagent that reconstructed the PDF
> text layer through a browser and could not be checked against the PDF by this session.
> **`schema_version: v3.2-abstract-only`.** Per `../CLAUDE.md`, a note this thin must not be used
> for a figure-design argument, and its unverified lines must not be quoted in a manuscript or a
> rebuttal. It is recorded now because it bears on a live novelty decision.

## A. Identity — verified

| field | value |
|---|---|
| `citekey` | `cheng2026af3cluster` |
| `doi` | none found; OpenReview `d2AeLFbBm1` |
| `year`, `venue` | **Published 02 Mar 2026, last modified 26 May 2026. GEM 2026 workshop (ICLR).** Submission number 93. CC BY 4.0. Workshop track — reviewed, but not a full conference or journal paper. |
| `title` | Generalized Multi-State Protein Design with AlphaFold3 |
| `authors` | Xiwei Cheng, Pengkang Guo, Seonghwan Seo, Casper A. Goverde, Wengong Jin |
| `keywords` | Multi-State Protein Design, Protein Ensemble Generation |

## B–C. Scope and conformational core — abstract-level only

**Verbatim from the abstract, verified by direct read:**

> "We first introduce AF3-Cluster, an evaluation framework that synergizes Multiple Sequence
> Alignment (MSA) clustering with AlphaFold3 to resolve complex structural ensembles across diverse
> biochemical contexts. Validation on a benchmark of ten multi-state proteins demonstrates that
> AF3-Cluster robustly recovers alternative conformations, **particularly for binder-mediated
> transitions where previous single-chain methods often fail.**"

> "Building on this, we propose AF3-MSD, an evolutionary framework that utilizes AlphaFold3 as a
> computationally efficient scoring proxy to guide the sculpting of multi-basin energy landscapes.
> AF3-MSD successfully drives candidates toward higher scores to design functional sequences for
> seven multi-state proteins".

What that establishes without the PDF: **MSA clustering + AlphaFold3 + binder-mediated transitions,
in one framework, on ten multi-state proteins, with alternative-conformation recovery as the
readout.** That is the whole of the break; the details below are not needed to establish it.

`[SUBAGENT — UNVERIFIED]` DBSCAN edit-distance clustering of ColabFold MSAs, each cluster fed
independently to AF3; four protein-binding systems (XCL1, KaiB, FliC, CaM) and three ligand-binding
systems (MBP 1OMP/1ANF, RBP 1URP/1DRK, GBP 1GGG/1WDN); readout is minimum RMSD to apo and holo
targets, e.g. MBP apo 1.27→0.54, holo 2.35→0.44 for AF-Cluster vs AF3-Cluster.

`input_factor_design`: **CANNOT BE ASSIGNED from the abstract.** If the unverified detail holds, MSA
clustering and binder presence are varied inside one AF3 model, which would make this the first
`factors-crossed` paper on an AF3-lineage backbone and the only one where the crossing involves a
co-input. **Do not tag `factors-crossed` until the PDF is read.**

## D. Claims

- **`central_conclusion`**: MSA clustering combined with AF3's co-folding recovers alternative
  conformations across ten multi-state proteins, and does so especially where the transition is
  driven by a binder — the case single-chain methods handle worst.

- **`stance`**: **`contrast` — the novelty-boundary paper on this axis, pending verification.**
  This project was considering "ligand co-input + MSA manipulation on an AF3-lineage model, measured
  on conformational state" as novel. The abstract alone shows that combination published and
  working, with binder-mediated transitions as its *strongest* case rather than an afterthought.
  A narrowed claim may survive — this is not a GPCR paper, its ligands are sugars rather than
  drug-like small molecules, its readout is RMSD to reference rather than an operationalised
  activation predicate, and it is a workshop paper — but the unnarrowed claim is dead.
  See also `xing2025purified`, which breaks the same claim on a kinase.

## G. Provenance

- **`extracted_on`**: 2026-09-10
- **`extractor`**: lit session (Opus 5), abstract read directly; body via subagent, unverified
- **`schema_version`**: `v3.2-abstract-only`
- **`confidence`**: **high** on identity, venue, date and the two quoted abstract passages —
  read from the page myself. **none** on anything in the `[SUBAGENT — UNVERIFIED]` block.
- **`unresolved`**:
  1. **Retrieve the PDF.** openreview.net/pdf?id=d2AeLFbBm1 — 403 to curl, blank in the viewer,
     download link inert. Try an authenticated session, or ask the authors.
  2. Whether the ligand systems are co-folded with the ligand present, or whether "binder-mediated"
     refers only to the four protein binders. **This is the single question that decides how much of
     our novelty survives** and it cannot be answered from the abstract.
  3. Whether a full-conference or journal version exists.
