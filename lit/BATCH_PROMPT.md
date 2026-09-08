Read SCHEMA.md (version 3) first, in full, including the data_shape grammar and the
v2->v3 Changelog. Then read EXTRACT_PROMPT.md for the extraction rules. Then extract
the assigned paper into notes/<citekey>.md following schema order, headings A-G plus
a Tags section.

Key v3 points that previous extractors got wrong under v2:
- data_shape slots are named by ROLE not screen position: facet / vary / series /
  measure / mark / n. Five forms: PLOT, MATRIX, RENDER, TREE, SCHEMATIC.
- series: is the colour/legend dimension inside a panel. Use it.
- Split figure rows on mark or measure, never on facet alone.
- oracle_leakage has SEVEN routes; answer each separately, NONE FOUND where absent.
  Route 4 includes tuning a sweep RANGE on the evaluation set. Route 7 is
  design-level oracle use and is weaker than pipeline leakage; label it as such.
- structural_priors_used is separate from oracle_leakage and is not a defect.
- metric_saturation is numeric only; axis truncation goes in hides.
- Leave comparable_to_ours and why_it_matters EMPTY.
- Tags only from the fixed v3 vocabulary. Never invent one; record it under unresolved.
- schema_version is v3, extracted_on 2026-09-07.
