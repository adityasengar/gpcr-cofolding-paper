"""Every path in the redo campaign, declared once.

Nothing under redo/ may compute a path from its own __file__ beyond importing
this module.  The reason is the one that motivated the layout: when paths are
derived ad hoc, moving a file silently changes what a script reads, and the
script keeps running.  Here a move costs one edit, in this file, and every
consumer follows.

The six kinds, and who may write them:

    spec/       a human, once.  Decisions and what to run.  Irreplaceable.
    build/      a human.  Code that turns spec into inputs.
    gates/      a human.  The checks.  Every one proved by planting a defect.
    inputs/     CODE ONLY.  Generated.  Hand-editing one is a defect that
                inputs/MANIFEST.tsv and gates/layout.py will catch.
    cache/      nobody.  Fetched from RCSB / GPCRdb / UniProt.  Committed as
                provenance -- those databases change, so a re-fetch is not the
                same data.  cache/structures/ is the exception: 297 mmCIF files,
                59 MB, regenerable bulk, gitignored.
    runs/       nobody.  Deliveries.  One directory per run, read-only once
                landed, identical shape inside.
    protocol/   what we asked paper_af3 and what they answered.
"""

import os

REDO = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(REDO)            # .../paper

SPEC       = os.path.join(REDO, "spec")
BUILD      = os.path.join(REDO, "build")
GATES      = os.path.join(REDO, "gates")
INPUTS     = os.path.join(REDO, "inputs")
CACHE      = os.path.join(REDO, "cache")
STRUCTURES = os.path.join(CACHE, "structures")
RUNS       = os.path.join(REDO, "runs")
PROTOCOL   = os.path.join(REDO, "protocol")


def repo(*parts):
    """A path relative to the repository root (block data, lit panels, ...)."""
    return os.path.join(ROOT, *parts)
