# figures/ — the figure toolkit

Generic, reusable scripts that produce submission-quality panels. Nothing here
hard-codes this paper's numbers: the plot generators take a DataFrame and column
names, and the renderer takes PyMOL selections. When the full export lands from
the HPC, the same commands make the real figures.

```
figstyle.py        house style: sizes, fonts, palette, save()
figpanels.py       plot generators — distributions, pairs, composition, matrix
render_struct.py   PyMOL structure renders, driven from the command line
make_demo.py       builds one of every panel from data/predictions.csv
structures/        downloaded PDBs (not in git)
out/               generated output (not in git — perishable, like RESULTS.md)
```

Run `python3 make_demo.py` to see every panel type. Nothing it writes is
citable; it is a smoke test that the toolkit runs on real columns.

The corpus figures (LF1-LF5 in `FIGURES.md`) are built from the literature
rather than from `data/`. Their pipeline is:

```
mine_corpus.py      lit/notes/*.md -> data_lit/{papers,figrows,metrics}.csv
classify_corpus.py  those          -> data_lit/{tags,metric_kinds,antimem,
                                                oracle_routes,figdefects}.csv
panels/lit*.py      those          -> out/lit*.{pdf,png}
data_lit/           extracted tables - IN git, they are the citable artefact
panels/             one script per figure
```

## Where the design rules come from

Not taste. The corpus in `lit/notes/` carries a `## F. Figures` table for all 78
papers — **1,226 panel-group rows**, each with a `data_shape`, a `hides` field
for figures that obscure their own result, and a `reuse` licence. Parsing all of
it gives the field's actual habits and its actual failures:

| | count |
|---|---|
| structure renders | 232 rows across 68 of 78 papers |
| plots with a dependent measure | 739 |
| matrices / heatmaps | 85 |
| schematics | 131 |

**Structure renders are the single commonest figure in this field, and 80% of
them (186 of 232) carry a recorded defect.** Corpus-wide the number is 957 of
1,226 rows. *(Corrected 2026-09-09 from "189 of 232" / 968: three render rows
whose `hides` cell reads `*(blank - reason)*` are blanks, and a non-empty test
counted them as defects. The rule now used is in `classify_corpus.py`,
`is_blank_hides`.)* The two dominant ones, by a wide margin:

- **59 rows** — a hand-picked example with the selection rule unstated.
- **58 rows** — no quantitative panel stands behind the claim the render makes.

That is why `render_struct.py` refuses to run without `--selected-from` and
`--selection-rule`, and writes a `.prov.json` next to every image. A render that
cannot say which model it is, out of how many, and why that one, *is* the defect.

On the plot side the recurring failures are bars standing in for distributions,
missing n, broken or truncated axes, and two measures sharing one axis. Each
generator in `figpanels.py` names the defect it prevents in its docstring.

## Licences — what is actually restricted

Of the 74 papers whose licence the corpus recorded: **55 open** (CC BY / CC
BY-NC / CC0), **15 ND**, **4 all-rights-reserved**. Four more have no licence
recorded. The ND and reserved ones:

```
ND        bugrova2026representation  chitsazi2025gpcrdock4  feldman2026alphainterp
          heo2022multistate  khaleq2026hyaline  lazou2026cryptic  lewis2025bioemu
          miglionico2026atlas  obendorf2026statespecific  protenix2026v2
          tang2026steeraf  vo2026fiducials  yang2025statespecific
          ye2026multistatebias  yu2026domainmotion
RESERVED  chiesa2025templatebias  kohlhoff2014gpcr  paajanen2026activation
          parikh2026allosteric
```

**What this does and does not forbid.** ND forbids reproducing or redrawing
*their panel*. It does not reserve a plot type: a violin of a distance faceted
by predictor is a convention, not anyone's property. So the restriction bites
only if you adapt a specific figure — which is worth avoiding anyway, since we
have our own data. Treat the list as a check to run before adapting a panel, not
as a constraint on the design vocabulary.

## Structure renders

The house scene is a pale semi-transparent cartoon in the background with the
ligand, partner peptide and named residues opaque in front:

```bash
python3 render_struct.py \
  --structure structures/3SN6.pdb \
  --ligand "chain R and resn P0G" \
  --label-residues "chain R and resi 113, chain R and resi 203@0,4,3" \
  --label-style one \
  --zoom-on "chain R and resn P0G" --zoom-buffer 9 \
  --selected-from 1 --selection-rule "crystal structure" \
  --out pocket
```

Add `--reference` for the corpus's dominant idiom (a model over a grey
reference; 232 render rows do exactly this), and `--peptide` to draw the α5-CT
as an opaque cartoon while the receptor stays transparent.

Labels on adjacent residues collide, so any selection may carry an offset:
`"chain A and resi 391@0,5,4"`.

Every run writes three files: the `.png`, the `.pml` that made it, and the
`.prov.json`. **The `.pml` is the source.** Open it in the PyMOL GUI, move the
camera, `get_view`, and paste the 18 numbers back with `--view` — the camera is
the one thing a command line cannot choose well.

### Two things that will bite

- `cartoon_transparency` is **object-level**, not per-selection. Setting it on a
  selection silently applies to the whole object. That is why an opaque partner
  in front of a transparent receptor has to be its own object, which the
  `--peptide` path does.
- Do **not** turn off `backface_cull` to fix black interiors on clipped
  helices — with a transparent cartoon every back face then renders too and the
  layers accumulate into something that looks opaque. `ray_interior_color`
  handles the interiors on its own.

The background defaults to opaque white, so the transparency is baked against
white exactly as it will print. `--transparent-background` gives RGBA instead,
which only looks right in a compositor: pdflatex and several image tools ignore
the alpha channel and render the ghost cartoon as flat grey.

## What can be plotted today

`data/predictions.csv` (17,568 rows, 16,388 scored) already carries `d_tm6`,
`d_npxxy`, `classified_state`, `plddt_at_anchors_mean` and the eight-arm
`partner_type` — apo, ligand, antagonist, α5_ct_fragment, α5_ct_variant,
cognate_ga, shuffled_ga, decoy_scaffold. So the central contrast, the decoy and
shuffled arms, the confidence-vs-state scatter and the coverage grid are all
derivable **locally, now**.

What is not: `delta_to_active` is null for 41% of rows because several receptors
carry no active reference, so any panel measuring distance *to the deposited
active state* still waits on the import. `d_tm6` is the raw geometric quantity
and does not.

Run `python3 analysis/fingerprint.py --check` before believing any number a
panel shows.
