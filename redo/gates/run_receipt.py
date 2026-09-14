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
    python3 redo/gates/run_receipt.py --selftest      # 11 plants, all four checks

**The self-test was written 2026-09-14 and it found two defects immediately**, which
is the argument for it. Until then this gate had no plants and had never executed at
all -- `redo/runs/` holds only a README -- while the brief listed it under "none".

  1. The recording contract declared NONE of the seven columns R1-R4 read. A
     delivery conforming exactly to the contract we were about to ship would have
     been refused on run 1 by the gate that exists to protect run 1.
  2. R2 compared `partner_requested` against `partner_returned`. When the contract
     gained `partner_returned_sha256`, the only available pair would have compared a
     construct id against a 64-hex digest -- unequal on every row of every delivery,
     for a reason having nothing to do with the partner.

Both are the same failure: two halves of one comparison drifting apart with nothing
running that would notice. The fixture is built FROM the contract for that reason, so
a column this gate reads that the contract does not declare fails the baseline rather
than waiting for real data.
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
    # Prefer the SEQUENCE hashes over the construct ids. A partner can carry the
    # right name and the wrong bytes, and the name pair cannot see that. The id
    # pair is kept as a fallback so a delivery that records only names is still
    # checked rather than skipped.
    #
    # These two must be compared LIKE WITH LIKE. On 2026-09-14 the recording
    # contract gained `partner_returned_sha256` while this check still read
    # `partner_returned`, so the only available pair would have compared a
    # construct id ("R3_ct21") against a 64-hex digest and failed on every row of
    # every delivery, for a reason that had nothing to do with the partner.
    a, b = need("partner_seq_sha256"), need("partner_returned_sha256")
    if not (a and b):
        a, b = need("partner_requested"), need("partner_returned")
    if not a or not b:
        bad.append(f"{name}: R2 cannot run — rows.csv carries neither the sequence-hash "
                   f"pair (partner_seq_sha256 / partner_returned_sha256) nor the "
                   f"construct-id pair (partner_requested / partner_returned)")
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


def _fixture(d, rows=6):
    """A CORRECT delivery, built from the recording contract rather than by hand.

    Derived, not hand-written: the columns come from `g1_recording_spec.tsv`, so a
    column this gate reads that the contract does not declare shows up here as a
    failing baseline instead of being invisible until run 1. That is exactly how
    the 2026-09-14 gap was found -- the contract declared none of the seven columns
    R1-R4 read, so a delivery conforming exactly to it would have been REFUSED by
    the gate that exists to protect run 1.
    """
    os.makedirs(d, exist_ok=True)
    cols = ["prediction_id", "receptor_slug", "arm", "backbone",
            "n_chains_requested", "n_chains_returned",
            "partner_seq_sha256", "partner_returned_sha256",
            "seed_requested", "seed_used", "partner_msa_depth_observed"]
    sha = "a" * 64
    with open(os.path.join(d, "rows.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for i in range(rows):
            w.writerow([f"p{i:04d}", "5HT5A", "ladder", "boltz2",
                        2, 2, sha, sha, 3027216127, 3027216127, 1])
    json.dump({"run_id": "0000_fixture", "group": "G1",
               "partner_msa_depth_expected": 1,
               "input_sha256": []},
              open(os.path.join(d, "manifest.json"), "w"))
    open(os.path.join(d, "README.md"), "w").write("fixture\n")
    return d


def selftest():
    """Prove each check by planting the defect it catches, and RUN it.

    Both shapes are planted for every check: a WRONG VALUE, and a MISSING COLUMN.
    The second matters more. `need()` returns None when a column is absent and the
    gate then appends to `bad` rather than staying quiet -- that branch is the
    entire reason this gate exists, and until now nothing had ever executed it.
    """
    import shutil
    import tempfile

    def drop(col):
        def f(d):
            p = os.path.join(d, "rows.csv")
            rs = list(csv.DictReader(open(p, encoding="utf-8")))
            keep = [c for c in rs[0] if c != col]
            with open(p, "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=keep, extrasaction="ignore")
                w.writeheader()
                w.writerows(rs)
        return f

    def corrupt(col, val):
        def f(d):
            p = os.path.join(d, "rows.csv")
            rs = list(csv.DictReader(open(p, encoding="utf-8")))
            rs[0][col] = val
            with open(p, "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(rs[0]))
                w.writeheader()
                w.writerows(rs)
        return f

    def unlink(f):
        return lambda d: os.unlink(os.path.join(d, f))

    def demanifest(d):
        p = os.path.join(d, "manifest.json")
        m = json.load(open(p))
        del m["partner_msa_depth_expected"]
        json.dump(m, open(p, "w"))

    cases = [
        ("R1", "value  ", corrupt("n_chains_returned", "1")),
        ("R1", "column ", drop("n_chains_returned")),
        ("R2", "value  ", corrupt("partner_returned_sha256", "b" * 64)),
        ("R2", "column ", drop("partner_returned_sha256")),
        ("R3", "value  ", corrupt("seed_used", "999")),
        ("R3", "column ", drop("seed_used")),
        ("R4", "value  ", corrupt("partner_msa_depth_observed", "732")),
        ("R4", "column ", drop("partner_msa_depth_observed")),
        ("R4", "declare", demanifest),
        ("--", "no rows", lambda d: open(os.path.join(d, "rows.csv"), "w")
         .write("prediction_id\n")),
        ("--", "no file", unlink("manifest.json")),
    ]

    sys.stdout.write("\n=== run receipt self-test: one plant per check, "
                     "value AND missing-column ===\n\n")
    tmp = tempfile.mkdtemp(prefix="receipt_selftest_")
    bad = 0
    try:
        base = _fixture(os.path.join(tmp, "baseline"))
        ok, fails = check_run(base)
        if fails or len(ok) != 4:
            sys.stdout.write(f"  FAIL  baseline: the UNPLANTED fixture does not pass "
                             f"({len(ok)} pass, {len(fails)} fail)\n")
            for f in fails:
                sys.stdout.write(f"          {f}\n")
            sys.stdout.write("\n  A check already failing on a clean delivery cannot "
                             "be proved by planting.\n\n")
            return 1
        sys.stdout.write("  ok    baseline: the unplanted fixture gives 4 PASS, 0 FAIL\n")

        for i, (check, kind, plant) in enumerate(cases):
            d = _fixture(os.path.join(tmp, f"case{i:02d}"))
            before = open(os.path.join(d, "rows.csv"), "rb").read()
            mbefore = open(os.path.join(d, "manifest.json"), "rb").read()
            plant(d)
            after = open(os.path.join(d, "rows.csv"), "rb").read() \
                if os.path.exists(os.path.join(d, "rows.csv")) else b""
            mafter = open(os.path.join(d, "manifest.json"), "rb").read() \
                if os.path.exists(os.path.join(d, "manifest.json")) else b""
            if after == before and mafter == mbefore:
                sys.stdout.write(f"  FAIL  {check} {kind}: the plant changed NO bytes\n")
                bad += 1
                continue
            _, fails = check_run(d)
            fired = bool(fails) and (check == "--" or
                                     any(f"{check} " in f for f in fails))
            sys.stdout.write(f"  {'ok  ' if fired else 'FAIL'}  planted {check} "
                             f"{kind} -> refused={bool(fails)}"
                             f"{'' if fired else '  <- did NOT fire'}\n")
            bad += 0 if fired else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    n = len(cases)
    sys.stdout.write(f"\n  {n - bad}/{n} plants fire over R1-R4 plus two structural "
                     f"cases.\n\n")
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
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
