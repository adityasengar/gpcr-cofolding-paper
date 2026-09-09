---
name: figbuild
description: Build a manuscript figure from our own data. Use this skill whenever the user asks to make, change, or check a figure or panel — plot this arm, show the distribution, render the peptide in the pocket, why does this panel look wrong, is this figure ready to submit. The design question "what figure should I make for this data" belongs to litquery instead; this skill is the making side, and it refuses to build panels that carry the defects the corpus survey found. Trigger it even when the user does not name a file: any request that ends in an image should go through here rather than ad-hoc matplotlib.
---

# figbuild

Make figures. The design counterpart is `litquery` — it answers *what figure should
this be*, matching on `data_shape` across 1,226 panel-group rows in the corpus. This
skill answers *build it, and do not build it badly*.

Read `figures/FIGURES.md` first. Then `figures/README.md` for where the rules came from.

## Refuse these. They are not style preferences

Each one is a defect recorded in the corpus's `hides` column, with a count.

| refuse | because |
|---|---|
| a panel with no `FIGURES.md` entry naming its claim | a figure that defends nothing is a plot |
| a number when `analysis/fingerprint.py --check` reports drift | every `RESULTS.md` verdict is stale until re-derived |
| a render without `--selected-from` and `--selection-rule` | 59 corpus renders are hand-picked with the rule unstated |
| a render that carries a claim with no quantitative panel beside it | 58 corpus renders do exactly this |
| a bar where a distribution exists | bars hide spread; use `strip_violin` |
| a mark without its n | a 100% bar on n=1 reads like one on n=377 |
| a broken or truncated axis | the commonest single complaint in the corpus |
| two measures sharing one axis | four measures once shared a "Success (%)" axis |
| adapting a panel from an ND or reserved paper | 15 ND, 4 reserved; list in `figures/README.md` |

Say which rule fired and offer the version that passes. Do not build it anyway and
mention the problem in a caption.

## How to build

1. `python3 analysis/fingerprint.py --check` — before anything.
2. Find or write the `FIGURES.md` entry. Claim, shows, data with `[R-*]` ids, build
   command, status.
3. Build with `figures/figpanels.py` generators, never bare matplotlib — the house
   style, the palette and the n-annotation live there.
4. Renders: `figures/render_struct.py`. The `.pml` it writes to `scenes/` is the
   source. The camera is the one thing a command line chooses badly — open the
   `.pml` in the PyMOL GUI, `get_view`, paste the 18 numbers back with `--view`.
5. Look at the image before reporting it done. Several defects here are invisible in
   the code and obvious in the picture.

## Two PyMOL traps

`cartoon_transparency` is **object-level**. Setting it on a selection applies to the
whole object — an opaque partner in front of a transparent receptor needs its own
object, which the `--peptide` path does.

Do not turn off `backface_cull` to fix black interiors on clipped helices. With a
transparent cartoon every back face then renders too and the layers accumulate into
something that looks opaque. `ray_interior_color` handles interiors on its own.

## Never

Do not run git — the orchestrator does all of it. Do not edit `lit/**`,
`analysis/**` or `manuscript/main.tex`. Do not draft body prose; captions only.
