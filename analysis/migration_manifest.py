#!/usr/bin/env python3
"""What a `git clone` does NOT carry, and which of it is irreplaceable.

A clone of this repo is ~5 MB and looks complete.  It is not: ~2.6 GB sits on the
author laptop under .gitignore, and roughly 2.4 GB of that cannot be regenerated
anywhere.  Moving the repo without moving those directories loses the row-level
evidence behind four blocks.

This GENERATES the move list rather than stating it, because a hand-written
inventory in a migration document is exactly the kind of count that drifts -- and
on this project four header counts have already drifted from their own bodies.

    python3 analysis/migration_manifest.py            # the list, classified
    python3 analysis/migration_manifest.py --rsync    # a runnable rsync command
    python3 analysis/migration_manifest.py --check    # verify after the move

CLASSIFICATION, and the reason for each call:

  MOVE      irreplaceable, or replaceable only against a database that has moved
            since we cached it.  RCSB and GPCRdb both revise entries, so a
            re-fetch is a DIFFERENT snapshot, not the same one.
  SKIP      deterministically regenerable from something the clone does carry.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Why each path is classified as it is.  A path not listed here is reported as
# UNCLASSIFIED rather than silently dropped -- a migration list that quietly
# omits a new directory is the same defect as a check that skips a missing input.
WHY = {
    "redo/cache/structures/":
        ("MOVE", "1,357 mmCIF + 1,757 JSON, the RCSB snapshot the measurement pass "
                 "ran against. Re-fetchable only as a DIFFERENT snapshot; caching it "
                 "was the whole point"),
    "lit/pdfs/":
        ("MOVE", "78 source PDFs. lit/notes/ extractions are in git; the sources are "
                 "not, and page-numbered quotes cannot be re-verified without them"),
    "lit/source/":
        ("MOVE", "includes source/pending_text/, which HANDOVER records as existing "
                 "nowhere else -- Europe PMC full text that survived only here"),
    "analysis/block_d/received_2026_09_13/":
        ("MOVE", "Block D's three row-level corpora, 42,180 predictions. The evidence "
                 "behind 113 verified claims. Arrived by hand"),
    "analysis/block_c/received_2026_09_12/rows.tier3.v2.csv":
        ("MOVE", "THE single highest-value file in the project (CLAUDE.md): 40,800 "
                 "rows, unblocks two Block C claims, the G4 gate that fired on 8 of 12 "
                 "cells, and the uncrossed ligand-class x partner-presence result"),
    "data/block_a/11_structures/":
        ("MOVE", "Block A coordinates"),
    "data/block_c/13_structures/":
        ("MOVE", "Block C coordinates, random + targeted"),
    "data/block_d/10_structures/":
        ("MOVE", "Block D coordinates, spot_check + random"),
    "data/block_b_structures/":
        ("MOVE", "Block B per-backbone coordinates"),
    "figures/structures/":
        ("MOVE", "structural assets the render pipeline reads"),
    "gpdb_coup.html":
        ("MOVE", "a GPCRdb coupling snapshot; GPCRdb revises, so a re-fetch differs"),
    "block_a_figure_data.zip":  ("MOVE", "the pristine Block A drop as delivered"),
    "block_b_figure_data.zip":  ("MOVE", "the pristine Block B drop as delivered"),
    "block_c_figure_data.zip":  ("MOVE", "the pristine Block C drop as delivered"),
    "block_b_structures.zip":   ("MOVE", "the pristine Block B structures drop"),
    "block_c_structures.zip":   ("MOVE", "the pristine Block C structures drop"),

    "figures/out/":
        ("SKIP", "regenerable: python3 the panel scripts under figures/block_*/panels/"),
    "lit/validate/cache/":
        ("SKIP", "pdftotext cache, regenerable from lit/pdfs/"),
    "lit/validate/txt/":
        ("SKIP", "pdftotext output, regenerable from lit/pdfs/"),
    "lit/validate/txt2/":
        ("SKIP", "pdftotext output, regenerable from lit/pdfs/"),
    "lit/validate/pages/":
        ("SKIP", "per-page text, regenerable from lit/pdfs/"),
    "manuscript/main.pdf": ("SKIP", "regenerable: ./manuscript/build.sh"),
    "manuscript/si.pdf":   ("SKIP", "regenerable: ./manuscript/build.sh"),
    "overleaf/":           ("SKIP", "export target, re-clonable"),
}


def ignored_paths():
    """Every gitignored path that actually exists, with its size in KB."""
    out = subprocess.run(["git", "status", "--ignored", "--porcelain"],
                         cwd=ROOT, capture_output=True, text=True).stdout
    paths = [ln[3:].strip() for ln in out.splitlines() if ln.startswith("!!")]
    rows = []
    for p in paths:
        full = os.path.join(ROOT, p)
        if not os.path.exists(full):
            continue
        kb = int(subprocess.run(["du", "-sk", full], capture_output=True,
                                text=True).stdout.split()[0])
        n = sum(len(f) for _, _, f in os.walk(full)) if os.path.isdir(full) else 1
        rows.append((p, kb, n))
    return sorted(rows, key=lambda r: -r[1])


def classify(p):
    if p in WHY:
        return WHY[p]
    for k, v in WHY.items():                      # a file inside a classified dir
        if k.endswith("/") and p.startswith(k):
            return v
    return ("UNCLASSIFIED", "not in this script's table -- decide and add it")


def main(argv):
    rows = ignored_paths()
    keep = [(p, kb, n) for p, kb, n in rows if kb >= 512]      # ignore the trivia

    if "--rsync" in argv:
        move = [p for p, _, _ in keep if classify(p)[0] == "MOVE"]
        print("# run from the repo root; DEST is the new machine's clone")
        print("rsync -av --progress \\")
        for p in move:
            print(f"  {p} \\")
        print('  "$DEST/"')
        return 0

    if "--check" in argv:
        missing = [p for p, _, _ in
                   [(p, k, n) for p, k, n in keep] if classify(p)[0] == "MOVE"
                   and not os.path.exists(os.path.join(ROOT, p))]
        for p, kb, n in keep:
            if classify(p)[0] == "MOVE" and not os.path.exists(os.path.join(ROOT, p)):
                missing.append(p)
        if missing:
            print(f"MISSING after migration ({len(missing)}):")
            for p in sorted(set(missing)):
                print(f"  {p}")
            return 1
        print("OK  every MOVE path is present")
        return 0

    tot = {"MOVE": [0, 0], "SKIP": [0, 0], "UNCLASSIFIED": [0, 0]}
    print(f"\n=== what a git clone does NOT carry ===\n")
    print(f"  {'path':<52} {'size':>7}  {'files':>6}  class")
    print(f"  {'-' * 52} {'-' * 7}  {'-' * 6}  -----")
    for p, kb, n in keep:
        cls, _ = classify(p)
        tot[cls][0] += kb
        tot[cls][1] += n
        print(f"  {p:<52} {kb / 1024:6.0f}M  {n:6d}  {cls}")
    print()
    for cls in ("MOVE", "SKIP", "UNCLASSIFIED"):
        kb, n = tot[cls]
        if kb or cls == "UNCLASSIFIED":
            print(f"  {cls:<14} {kb / 1048576:5.2f} GB  over {n} files")
    print()
    if tot["UNCLASSIFIED"][0]:
        print("  UNCLASSIFIED is not zero. Classify it in WHY before migrating --\n"
              "  a migration list that silently omits a directory is the same defect\n"
              "  as a check that skips a missing input.\n")
        return 1
    print("  Reasons for each call: python3 analysis/migration_manifest.py --why\n")
    return 0


if __name__ == "__main__":
    if "--why" in sys.argv:
        for k, (cls, why) in sorted(WHY.items()):
            print(f"\n  {cls:<5} {k}\n        {why}")
        print()
        sys.exit(0)
    sys.exit(main(sys.argv[1:]))
