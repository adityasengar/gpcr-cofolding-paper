# reference/ — figure scripts to learn from, not to run

Provided by Aditya on 2026-09-10 (`paper_figure_scripts_2026_09_06.zip`). These
are **exemplars**, not part of the build. They reference paths and a conda
environment that do not exist here. Read them, take the techniques, and
implement against `figures/figstyle.py`.

## The technique that matters: real depth of field, in matplotlib

`side_quest_nsb_closeups.py:blurred_backbone()` does what PyMOL users spend
hours faking:

1. rasterise the Cα trace into a scalar canvas as a polyline,
   weighting each segment by its **depth** so far atoms deposit less ink;
2. `scipy.ndimage.gaussian_filter` it;
3. convert to RGBA with a state tint, `alpha = blurred**0.6 * base_alpha`;
4. `imshow` it at `zorder=1`, underneath everything;
5. draw sharp ball-and-stick side chains on top at `zorder=6-7`.

`render_closeup()` layers **two** blur passes per state — `sigma=9.0,
base_alpha=0.30` for the far context and `sigma=3.2, base_alpha=0.55` for the
near — which is what produces the sense of a focal plane rather than a flat wash.

Two more details worth copying:

- **State-tinted halo behind each atom** (`draw_residue_2d`): a large soft
  `scatter` in the state colour at `alpha≈0.32` under the CPK ball, so active
  and inactive read apart at a glance without recolouring the atoms themselves.
- **Camera from geometry, not by eye** (`orient_frame`): the view is derived
  from the motif coordinates, so it is reproducible and identical across panels.

Only `Bio.PDB`, `scipy`, `matplotlib`, `numpy` and `pandas` are needed for
these two — all installed. `gemmi`, `biotite`, `py3Dmol` and `playwright` are
required only by the pose-grid variants and are absent.

## What is here

| file | what to take from it |
|---|---|
| `side_quest_nsb_closeups.py` | **the depth-of-field renderer** — the most valuable thing in the archive |
| `side_quest_nsb_figures.py` | Cα-trace overlays and class-conditional landscapes at panel scale |
| `side_quest_pose_grid.py` | a ligand × backbone grid with a 2D-chemistry column |
| `side_quest_pose_grid_pymol.py` | the same grid ray-traced and in OpenGL, for comparison |
| `side_quest_pose_grid_biotite.py` | wire rendering with the same blur-for-depth idea |
| `side_quest_pose_grid_py3dmol.py` | WebGL via headless Chromium |
| `_pose_grid_common.py` | Kabsch alignment and per-backbone ligand-naming quirks |

The four pose-grid variants are the same figure in four renderers, which is
itself instructive: the choice of renderer is a style decision, not a
correctness one.
