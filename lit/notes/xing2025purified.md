# xing2025purified

> **Extraction provenance.** Extracted 2026-09-10 from the arXiv PDF (`pdfs/xing2025purified.pdf`,
> 15 pp), retrieved directly. Page numbers are PDF pages and there is no printed version, so no
> offset applies. Main text read; SI not separately held. Extracted because this paper
> **falsified a novelty claim this project was about to make** — see `stance`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `xing2025purified` |
| `doi` | none — arXiv:2506.00147 |
| `year`, `venue` | 2025, **arXiv preprint only.** OpenAlex and Crossref both show no journal version as of 2026-09-10. **Not peer-reviewed.** |
| `title` | State-aware protein-ligand complex prediction using AlphaFold3 with purified sequences |
| `authors` | Enming Xing, Junjie Zhang, Shen Wang, Xiaolin Cheng (Ohio State, Div. Medicinal Chemistry & Pharmacognosy + TDAI) |

## B. Scope

| field | value |
|---|---|
| `system` | **Kinase and cytokine — NO GPCR.** EGFR (P00533) and IL-1β. |
| `n_targets` | Small, case-study scale. EGFR: three deposited complexes named as the failure set (8A2A, 8A2B, 8A2D). Prediction counts are large but over few targets — 15,490 predictions from 28-sequence groups shuffled 10×, and 233 runs from 6-sequence groups (p.5). |
| `method_class` | method + benchmark — transfers AF-ClaSeq "purified sequence" subsets from AF2 into AF3. |
| `backbones` | **AF2** (sequence purification and protein-alone prediction) and **AF3** (protein + ligand). Boltz-1, Chai-1, Protenix, NeuralPlexer named in the intro but **not run**. |
| `templates` | **off.** p.5: "No templates were used as input for the predictions, relying solely on the MSA compiled from purified sequences". Restated p.6: "No templates were searched, and the SMILES of the ligand was input alongside the MSA." |
| `msa_handling` | **Purified / composition-selected, NOT depth-reduced.** AF-ClaSeq isolates sequence subsets that preferentially encode one structural state, by iterative enrichment, bootstrapping and voting. Mechanically it is subsetting: p.5, "we divided them into groups of 28 sequences and shuffled randomly 10 times, performing a total of 15,490 predictions"; "1,405 sequences were divided into 233 groups of 6 sequences each, resulting in 233 prediction runs". |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | two-state (EGFR active vs Src-like inactive) + ensemble over seeds; 50 structures per condition (10 seeds × 5). |
| `state_metric` | **Dual, and the pairing is the point.** Ligand RMSD to deposited *and* a receptor-state RMSD over the αC helix and A-loop (residues 756–769 and 857–863), against EGFR active 2ITP vs Src-like inactive 2GS7. Figure 1 annotates each default-AF3 failure with both, e.g. "Ligand RMSD (pred vs true): 19.1 Å / A-loop/αC helix RMSD: 7.2 Å" (8A2A), 18.9/3.2 (8A2B), 14.9/7.2 (8A2D). **No operationalised activation predicate** — RMSD to reference throughout. |
| `coinput_composition` | receptor + **one small-molecule ligand as SMILES**. No protein partner anywhere in the paper. |
| `input_factor_design` | **MSA**: varied (purified subsets vs random subsets of equal number vs default). **templates**: off throughout, not varied. **ligand**: present in the AF3 arm, absent in the AF2 arm. **partner**: never. <br>`crossings:` **MSA × ligand NOT CROSSED — the legs are in different models.** p.5: "AF2 predictions of the protein alone were performed using the purified sequences", then "These purified sequences corresponding to the inactive state were then used for AF3 predictions, where the customized input MSA was provided along with the SMILES of the ligand." Protein-alone is AF2; ligand is AF3. Same structural defect as `ye2026multistatebias`. |
| `oracle_leakage` | **Route 2 heavy.** The purification target is a *named state*, and sequences are selected by how they score against deposited active/inactive references — so the state answer drives the input construction. Route 5 definitional (RMSD to deposited). Route 7: targets chosen because deposited complexes exist. |
| `confidence_as_discriminator` | Ligand atomic pLDDT is used descriptively ("low ligand atomic pLDDT scores", p.5) but not validated as a state discriminator. |

## D. Claims

- **`central_conclusion`**: AF-ClaSeq-purified MSA subsets, transferred from AF2 into AF3 alongside a ligand SMILES, correct AF3 predictions that otherwise place the ligand wrongly and the receptor in the wrong state.

- **`necessity_claims`** (verbatim + page):
  - p.3 — **the sentence that matters most to this project**: *"Our findings reveal that the successful sampling of alternative states depends not on MSA depth but on sequence purity."*
  - p.5: *"No templates were used as input for the predictions, relying solely on the MSA compiled from purified sequences"*.

- **`stated_limits`**: kinase/cytokine only; no GPCR; single-family case studies; not peer-reviewed.

- **`stance`**: **`contrast` — a novelty-boundary paper, and the reason it was extracted.**
  On 2026-09-10 this project was considering "ligand co-input + MSA subsampling on an AF3-lineage
  model, measured on receptor state" as a novel study. An adversarial search found this preprint
  doing exactly that: **AF3, ligand SMILES as co-input, MSA subsetted, receptor state as the
  readout.** It is not a GPCR, it is not peer-reviewed, and its two legs live in different models —
  but any novelty sentence on that axis must be written against it.
  Its p.3 claim that state sampling **"depends not on MSA depth but on sequence purity"** bears
  directly on any MSA-depth ladder: a result showing depth *does* steer state contradicts a
  published claim and should be foregrounded; a result showing it does not is confirmatory.

## G. Provenance

- **`extracted_on`**: 2026-09-10
- **`extractor`**: lit session (Opus 5)
- **`schema_version`**: `v3.2-partial` — A–D and `input_factor_design` complete; **section E
  (quantitative comparators) and F (figures) NOT extracted.** Do not use this note for figure design
  or for a numeric comparison table without reading the PDF.
- **`confidence`**: high on identity, scope, MSA handling, the factor design and the two verbatim
  claims (all read directly from the retrieved PDF). No confidence offered on per-case success
  rates, which were not extracted.
- **`unresolved`**: 1. Whether any journal version has appeared since 2026-09-10. 2. Per-condition
  success rates and their n. 3. Whether the "enforced threshold" bins are tuned on the evaluation
  cases (suspected route 4).
