#!/usr/bin/env python3
"""The run receipt — does a delivered run contain what was asked for?

Finding F-9: **nothing in the delivered pipeline compares output to input.** Not
sequence, not chain count, not seed-used against seed-requested, not MSA depth. A
monomer returned where a receptor + Ga dimer was requested passes every existing
check, because `ok = exit_code == 0 and len(produced) > 0`. `paper_af3` confirmed
this, and separately found two guards inspecting artefacts their own run never
consumed.

`layout.py`'s L5/L6 check that a run has the right FILES and that its declared
input hashes are ones we hold. That is bookkeeping. This checks the CONTENT:

    R1  every row's requested chain count matches what came back
    R2  every row's partner identity matches what was dispatched
    R3  every row's seed_used matches seed_requested
    R4  the partner MSA depth is what the arm declares (the F-5 ladder needs
        depth 1 at every rung; a run that cannot report depth fails loudly
        rather than silently passing)

**Why these four and not more.** Each is an equality between something we sent and
something that came back. None needs a model, a threshold or a judgement call, so
none can drift into an opinion. F-9's estimate was three assertions; R4 is the
fourth because F-5 made the alignment regime a designed quantity rather than an
incidental one.

Runs are read-only once landed, so a failure here is never repaired in place — it
is reported, and the run is re-requested or accepted with the defect recorded.

    python3 redo/gates/run_receipt.py                 # every run under runs/
    python3 redo/gates/run_receipt.py <run_dir>       # just one
"""

import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import RUNS

REQUIRED = ("manifest.json", "rows.csv", "README.md")


def check_run(d):
    """Returns (passes, failures) as lists of human-readable strings."""
    name = os.path.basename(d)
    ok, bad = [], []

    miss = [f for f in REQUIRED if not os.path.exists(os.path.join(d, f))]
    if miss:
        return ok, [f"{name}: missing {miss}"]

    try:
        man = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
    except Exception as exc:                                      # noqa: BLE001
        return ok, [f"{name}: manifest.json unreadable — {exc}"]

    with open(os.path.join(d, "rows.csv"), encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return ok, [f"{name}: rows.csv has no data rows"]

    cols = set(rows[0])

    def need(*names):
        """The column that is present, or None. A missing column is a FAILURE,
        not a skip — a check that quietly does nothing when its input is absent
        is the exact defect this gate exists to catch."""
        for n in names:
            if n in cols:
                return n
        return None

    # -- R1  chain count ----------------------------------------------------
    a, b = need("n_chains_requested"), need("n_chains_returned")
    if not a or not b:
        bad.append(f"{name}: R1 cannot run — rows.csv has no chain-count columns")
    else:
        m = [r for r in rows if str(r[a]).strip() != str(r[b]).strip()]
        (ok if not m else bad).append(
            f"{name}: R1 chain count matches on all {len(rows)} rows" if not m
            else f"{name}: R1 chain count DIFFERS on {len(m)} of {len(rows)} rows "
                 f"(first: requested {m[0][a]}, returned {m[0][b]})")

    # -- R2  partner identity ------------------------------------------------
    a, b = need("partner_requested"), need("partner_returned")
    if not a or not b:
        bad.append(f"{name}: R2 cannot run — rows.csv has no partner-identity columns")
    else:
        m = [r for r in rows if str(r[a]).strip() != str(r[b]).strip()]
        (ok if not m else bad).append(
            f"{name}: R2 partner identity matches on all {len(rows)} rows" if not m
            else f"{name}: R2 partner identity DIFFERS on {len(m)} rows "
                 f"(first: sent {m[0][a]!r}, got {m[0][b]!r})")

    # -- R3  seed ------------------------------------------------------------
    a, b = need("seed_requested"), need("seed_used")
    if not a or not b:
        bad.append(f"{name}: R3 cannot run — rows.csv has no seed columns")
    else:
        m = [r for r in rows if str(r[a]).strip() != str(r[b]).strip()]
        (ok if not m else bad).append(
            f"{name}: R3 seed matches on all {len(rows)} rows" if not m
            else f"{name}: R3 seed DIFFERS on {len(m)} rows "
                 f"(first: requested {m[0][a]}, used {m[0][b]})")

    # -- R4  partner MSA depth vs the arm's declaration ----------------------
    col = need("partner_msa_depth_observed")
    want = man.get("partner_msa_depth_expected")
    if col is None:
        bad.append(f"{name}: R4 cannot run — no partner_msa_depth_observed column "
                   f"(F-6: the delivered campaign recorded no MSA metadata at all)")
    elif want is None:
        bad.append(f"{name}: R4 cannot run — manifest declares no "
                   f"partner_msa_depth_expected")
    else:
        m = [r for r in rows if str(r[col]).strip() != str(want).strip()]
        (ok if not m else bad).append(
            f"{name}: R4 partner MSA depth == {want} on all {len(rows)} rows" if not m
            else f"{name}: R4 partner MSA depth DIFFERS from the declared {want} on "
                 f"{len(m)} rows (first: {m[0][col]})")
    return ok, bad


def main(argv):
    targets = ([os.path.abspath(argv[0])] if argv else
               sorted(os.path.join(RUNS, e) for e in os.listdir(RUNS)
                      if os.path.isdir(os.path.join(RUNS, e)) and not e.startswith(".")))
    sys.stdout.write("\n=== run receipt ===\n\n")
    if not targets:
        sys.stdout.write("  no runs yet — nothing to check\n\n")
        return 0
    allbad = []
    for d in targets:
        ok, bad = check_run(d)
        for line in ok:
            sys.stdout.write(f"  PASS  {line}\n")
        for line in bad:
            sys.stdout.write(f"  FAIL  {line}\n")
        allbad += bad
    if allbad:
        sys.stdout.write(f"\n  RECEIPT REFUSED — {len(allbad)} check(s) failed.\n\n")
        return 1
    sys.stdout.write(f"\n  ACCEPTED — {len(targets)} run(s).\n\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
