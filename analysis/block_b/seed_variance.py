#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nested variance decomposition on Block B's 5 seeds x 10 samples design.

PARKED IDEA, 2026-09-10. Not used by any manuscript sentence. Kept so the
result does not have to be rediscovered when the distributional framing is
raised again. See HANDOVER.md, "Parked".

The design is nested: each receptor x arm x backbone cell holds 5 dispatch
seeds and exactly 10 samples per seed. That separates variance BETWEEN seeds
from variance WITHIN a seed, which no analysis in either block currently uses.

WHAT THIS IS NOT. 50 predictions from a generative model are not a
conformational ensemble in the thermodynamic sense. There is no Boltzmann
weighting and no claim to one. This is the sampling distribution of a
generator, and calling it anything else ends a structural-biology review.
"""
from __future__ import print_function
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AXES = {"tilt": "d_gpcrdb_tm6_tilt_246_637_ca", "npxxy": "d_npxxy_y558_y753_oh"}


def decompose(rows, col):
    """Per (backbone, arm): mean over receptors of the between-seed share."""
    out = []
    for (bb, arm), g in rows.groupby(["backbone", "arm"]):
        btw, wth = [], []
        for _, cell in g.groupby("receptor_slug"):
            x = cell.dropna(subset=[col])
            if len(x) < 40:                       # a cell short of data is skipped
                continue
            per_seed = x.groupby("seed_used")[col]
            if per_seed.ngroups < 2:
                continue
            btw.append(per_seed.mean().var(ddof=1))   # variance of the seed means
            wth.append(per_seed.var(ddof=1).mean())   # mean variance inside a seed
        if btw:
            b, w = float(np.mean(btw)), float(np.mean(wth))
            out.append((bb, arm, b, w, b / (b + w) if (b + w) else np.nan))
    return pd.DataFrame(out, columns=["backbone", "arm", "between_seed_var",
                                      "within_seed_var", "frac_between"])


def main():
    rows = pd.read_csv(os.path.join(ROOT, "data", "block_b", "01_rows",
                                    "rows_tidy.csv"), low_memory=False)
    sizes = rows.groupby(["receptor_slug", "arm", "backbone",
                          "seed_used"]).size().unique()
    print("samples per (cell, seed):", sizes, "-- the nested design holds\n")
    for name, col in AXES.items():
        d = decompose(rows, col)
        print("%s: share of within-cell variance living BETWEEN seeds" % name.upper())
        print(d.pivot_table(index="backbone", columns="arm",
                            values="frac_between").round(3).to_string())
        print("")
    print("Read it as: high = the seed decides the answer and the 10 samples "
          "drawn from it are near-redundant; low = sampling within a seed is "
          "doing the exploring.")


if __name__ == "__main__":
    main()
