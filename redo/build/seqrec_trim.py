#!/usr/bin/env python3
"""Apply the miglionico2026atlas terminal cap to every panel receptor.

The rule, quoted verbatim from `miglionico2026atlas` p.19 via the lit
session: *"N-termini were truncated to a maximum of 50 residues upstream of
TM1, and C-termini to 100 residues downstream of helix H8, to reduce
terminal disorder."*

It is a **cap**, not a fixed boundary: a receptor whose N-terminus is
already shorter than 50 residues upstream of TM1 is unchanged. That is why
it needs no per-receptor special case, and it is why applying it is a
mechanical operation rather than a judgement — except at FSHR/LSHR/TSHR,
where the cap amputates a folded LRR ectodomain as a side effect. Those
three are reported here and decided in SEQ_RECEPTORS.md §4.3, not here.

Two segment sources, and they do not agree, so both are recorded:
  * UniProt TRANSMEM features (already fetched by seqrec_build.py). UniProt
    annotates seven transmembrane helices and does **not** annotate H8.
  * GPCRdb generic-numbering residue tables
    https://gpcrdb.org/services/residues/{entry_name}/  — these do carry an
    `H8` segment, which is the one the rule names. Same service and same
    convention `seq_build.py` used for the Gα CGN segments, so the two
    halves of the spec rest on the same authority.

Where GPCRdb has no H8 (it is genuinely absent or unmodelled in some
entries) the C-terminal cap falls back to TM7 end + 100 and the row is
flagged, rather than guessing an H8.

Outputs
  seqrec_trim.tsv      per receptor: TM1/H8 boundaries from both sources,
                       the capped construct range, its length and sha256,
                       and how many residues the cap removes at each end
  seqrec_trimmed.fasta the capped chain A sequences

Usage
  python3 redo/build/seqrec_trim.py
  python3 redo/build/seqrec_trim.py --selftest
"""
import collections
import csv
import hashlib
import json
import os
import sys
import time
import urllib.request

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
PANEL = os.path.join(INPUTS, "panel_systems.csv")
RECS = os.path.join(INPUTS, "seqrec_receptors.tsv")
FASTA = os.path.join(INPUTS, "seqrec_canonical.fasta")
FEATS = os.path.join(INPUTS, "seqrec_features.tsv")
CACHE = os.path.join(CACHE, "seqrec_gpcrdb_residues.json")
OUT = os.path.join(INPUTS, "seqrec_trim.tsv")
OUT_FASTA = os.path.join(INPUTS, "seqrec_trimmed.fasta")

GPCRDB_RES = "https://gpcrdb.org/services/residues/%s/"

N_CAP = 50      # residues upstream of TM1
C_CAP = 100     # residues downstream of H8


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def read_fasta(path):
    seqs, name, buf = {}, None, []
    for line in open(path):
        if line.startswith(">"):
            if name:
                seqs[name] = "".join(buf)
            name, buf = line[1:].split("|")[0], []
        else:
            buf.append(line.strip())
    if name:
        seqs[name] = "".join(buf)
    return seqs


def gpcrdb(entry, cache):
    if entry in cache:
        return cache[entry]
    for attempt in range(4):
        try:
            body = urllib.request.urlopen(GPCRDB_RES % entry, timeout=60).read().decode()
            cache[entry] = json.loads(body)
            return cache[entry]
        except Exception as exc:                        # noqa: BLE001
            if attempt == 3:
                print(f"# GPCRDB FETCH FAILED {entry}: {exc}", file=sys.stderr)
                cache[entry] = []
                return []
            time.sleep(2 * (attempt + 1))


def segments(rows):
    out = {}
    for r in rows:
        seg, n = r.get("protein_segment"), r.get("sequence_number")
        if not seg or n is None:
            continue
        lo, hi = out.get(seg, (n, n))
        out[seg] = (min(lo, n), max(hi, n))
    return out


def uniprot_tm():
    tm = collections.defaultdict(list)
    for r in csv.DictReader(open(FEATS), delimiter="\t"):
        if r["feature"] == "TRANSMEM":
            tm[r["slug"]].append((int(r["start"]), int(r["end"])))
    return {k: sorted(v) for k, v in tm.items()}


def main():
    panel = {r["slug"]: r for r in csv.DictReader(open(PANEL))}
    recs = list(csv.DictReader(open(RECS), delimiter="\t"))
    seqs = read_fasta(FASTA)
    utm = uniprot_tm()
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

    rows = []
    for rec in recs:
        slug = rec["slug"]
        if slug not in panel:            # orthologue candidates, no GPCRdb row
            continue
        seq = seqs[slug]
        L = len(seq)
        entry = (panel[slug]["gpcrdb_primary_protein"]
                 or panel[slug]["gpcrdb_proteins"].split(";")[0])
        segs = segments(gpcrdb(entry, cache))
        tm = utm.get(slug, [])

        tm1_up = segs.get("TM1", (None, None))[0]
        tm1_u = tm[0][0] if tm else None
        tm7_u = tm[-1][1] if tm else None
        h8 = segs.get("H8")

        tm1 = tm1_up or tm1_u
        if h8:
            c_anchor, c_src = h8[1], "GPCRdb H8 end"
        else:
            c_anchor, c_src = tm7_u, "FALLBACK TM7 end (no GPCRdb H8)"

        # OPTION (b), enacted 2026-09-13 (DECISIONS.md D-2026-09-13-a, closing
        # D-OPEN-2026-09-12-j).  The signal peptide is removed BEFORE the cap, and
        # only where UniProt annotates a CHAIN start.
        #
        # Previously this read `start = max(1, tm1 - N_CAP) if tm1 else 1`, which is
        # SEQ_RECEPTORS.md sec.3.1's option (c) -- the cap applied with no separate
        # signal rule -- and sec.3.1 calls it "the worst option and the numbers say
        # so".  It left FRAGMENTS: 5HT2C kept 29 of its 32 signal residues because
        # the cap began at 4, and EDNRA kept 1 of 20.  A fragment of a signal peptide
        # is neither the leader nor its absence; it is an artefact of an unrelated
        # rule.  Using the CHAIN start as a FLOOR removes the fragment case outright
        # and is a no-op for the entries with no annotated signal.
        # A malformed chain_range must FAIL, not silently fall back to 1 -- falling
        # back IS option (c), the thing this change overturned, and it would do so
        # invisibly. "A missing input FAILS, it does not skip."
        raw = rec.get("chain_range", "").strip()
        if raw in ("", "none", "NA"):
            chain_lo = 1
        else:
            try:
                chain_lo = int(raw.split("-")[0])
            except (ValueError, IndexError):
                sys.exit(f"FAIL: {slug} has an unparseable chain_range {raw!r}. "
                         f"Falling back to 1 would silently restore option (c) for "
                         f"this receptor -- see DECISIONS.md D-2026-09-13-a.")

        # TWO starts, and keeping them apart is what stops the columns lying.
        # cap_start is what the terminal cap ALONE would do; start is what we supply.
        # Every existing column keeps its original meaning -- the CAP's effect --
        # and the signal peptide's removal is attributed separately.  Without this
        # split, n_removed_nterm / n_removed_total / pct_removed / cap_binds_nterm
        # all silently absorb signal removal while still being named and read as cap
        # effects: 5HT2C would report cap_binds_nterm=yes and n_removed_nterm=32 when
        # the cap alone removes 3.  It is also what keeps seqrec_verify.py's frozen
        # constant (1,294 core residues removed by the cap) TRUE rather than needing
        # to be bumped -- a frozen constant you bump to match new behaviour has
        # stopped being a check.
        cap_start, start = starts(tm1, chain_lo)
        # THREE values, not two.  "false" on a receptor that HAS no signal peptide
        # reads as "the signal peptide was retained", which is the opposite of the
        # truth -- so the no-signal case is `none`, and `false` is reserved for a
        # receptor that HAS one and still carries part of it.  Under option (b) that
        # is unreachable, because chain_lo is a floor; if it ever appears, the floor
        # has stopped being applied.  seqrec_verify.py's signal checks assert it never does.
        has_signal = rec.get("signal", "").strip() not in ("", "none", "NA")
        if not has_signal:
            signal_state = "none"
        else:
            sig_end = int(rec["signal"].split("-")[1])
            signal_state = "true" if start > sig_end else "false"
        n_removed_signal = start - cap_start        # what the CHAIN floor added
        sig_residues_left = 0
        if has_signal:
            sig_residues_left = max(0, int(rec["signal"].split("-")[1]) - start + 1)
        end = min(L, c_anchor + C_CAP) if c_anchor else L
        trimmed = seq[start - 1:end]

        rows.append({
            "slug": slug, "tier": rec["tier"], "gpcr_class": rec["gpcr_class"],
            "accession": rec["accession"], "gpcrdb_entry": entry,
            "canon_len": L,
            "tm1_start_uniprot": tm1_u or "NA",
            "tm1_start_gpcrdb": tm1_up or "NA",
            "tm1_start_used": tm1 or "NA",
            "tm7_end_uniprot": tm7_u or "NA",
            "h8_gpcrdb": f"{h8[0]}-{h8[1]}" if h8 else "NA",
            "c_anchor_used": c_anchor or "NA",
            "c_anchor_source": c_src,
            "signal": rec["signal"],
            "trim_start": start, "trim_end": end, "cap_start": cap_start,
            # Required by SEQ_RECEPTORS.md sec.3.1 INDEPENDENT of which option is
            # chosen: "no block has ever carried it and the question cannot be
            # answered afterwards from a length."
            "signal_peptide_removed": signal_state,
            # the CHAIN floor's contribution, kept OUT of every n_removed_* column
            # so those keep meaning "what the cap did"
            "n_removed_signal": n_removed_signal,
            "signal_residues_retained": sig_residues_left,
            "trim_len": len(trimmed),
            "n_removed_nterm": cap_start - 1,
            "n_removed_cterm": L - end,
            "n_removed_total": (cap_start - 1) + (L - end),
            "pct_removed": round(100 * ((cap_start - 1) + (L - end)) / L, 1),
            "cap_binds_nterm": "yes" if cap_start > 1 else "no",
            "cap_binds_cterm": "yes" if end < L else "no",
            "trim_sha256": sha(trimmed),
            "canon_sha256": rec["sha256"],
            "_seq": trimmed,
        })
    json.dump(cache, open(CACHE, "w"))

    cols = [c for c in rows[0] if not c.startswith("_")]
    with open(OUT, "w") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    with open(OUT_FASTA, "w") as fh:
        for r in rows:
            fh.write(f">{r['slug']}|{r['accession']}|{r['trim_start']}-{r['trim_end']}"
                     f"|len={r['trim_len']}|sha256={r['trim_sha256']}\n")
            for i in range(0, len(r["_seq"]), 60):
                fh.write(r["_seq"][i:i + 60] + "\n")

    core = [r for r in rows if "C1" in r["tier"].split("|")]
    print(f"# wrote {OUT}, {OUT_FASTA} ({len(rows)} receptors, {len(core)} core)",
          file=sys.stderr)
    print(f"#   core: N cap binds on {sum(1 for r in core if r['cap_binds_nterm']=='yes')}, "
          f"C cap binds on {sum(1 for r in core if r['cap_binds_cterm']=='yes')}, "
          f"neither on {sum(1 for r in core if r['n_removed_total']==0)}",
          file=sys.stderr)
    print(f"#   core residues removed: total "
          f"{sum(r['n_removed_total'] for r in core)}, "
          f"max {max(core, key=lambda r: r['n_removed_total'])['slug']} "
          f"{max(r['n_removed_total'] for r in core)}", file=sys.stderr)
    miss = [r["slug"] for r in rows if r["h8_gpcrdb"] == "NA"]
    if miss:
        print(f"#   NO GPCRdb H8, C cap fell back to TM7+100: {miss}", file=sys.stderr)


def starts(tm1, chain_lo):
    """(cap_start, start) -- the ONE implementation of the rule.

    Extracted 2026-09-13 because `--selftest` had been re-implementing the start
    expression inline, and went on asserting the PRE-option-(b) formula
    `max(1, tm1 - N_CAP)` after production stopped using it -- printing SELFTEST PASS
    while certifying code that no longer existed.  A fixture that re-implements the
    thing it tests cannot fail when the thing changes.  Both callers now go through
    here, so the self-test exercises the production path or it exercises nothing.
    """
    cap_start = max(1, tm1 - N_CAP) if tm1 else 1
    return cap_start, max(chain_lo, cap_start)


def selftest():
    """The cap must be a cap: idempotent, and inert on a short terminus."""
    ok = True
    seq = "M" * 500
    # chain_lo=1 throughout this block: the receptors with no annotated signal
    # peptide, where option (b) must be a NO-OP.  The floor cases follow.
    for tm1, h8end, exp_start, exp_end in [
        (400, 450, 350, 500),      # long N-term: cap binds at 400-50
        (10, 450, 1, 500),         # short N-term: cap inert, start stays 1
        (60, 380, 10, 480),        # both bind
        (51, 399, 1, 499),         # exactly at the cap: start 1, end 499
    ]:
        _cap, start = starts(tm1, 1)
        end = min(len(seq), h8end + C_CAP)
        got = (start, end)
        print(f"  TM1={tm1:3d} H8end={h8end:3d} -> {got} (expect "
              f"{(exp_start, exp_end)})")
        ok &= got == (exp_start, exp_end)
    # OPTION (b): the CHAIN floor.  None of these cases existed before 2026-09-13,
    # which is how a self-test came to pass on the formula it was meant to replace.
    print("  -- option (b), the CHAIN floor --")
    for tm1, chain_lo, exp_cap, exp_start, why in [
        (54, 33, 4, 33, "5HT2C: cap would start at 4, floor lifts it to 33"),
        (70, 21, 20, 21, "EDNRA: cap 20, floor 21 -- one residue, and it matters"),
        (414, 364, 364, 364, "TSHR: cap already past the signal, floor inert"),
        (60, 1, 10, 10, "no signal peptide: floor is a no-op"),
        (None, 27, 1, 27, "no TM1: start falls to the floor, not to 1"),
    ]:
        cap_start, start = starts(tm1, chain_lo)
        got = (cap_start, start)
        print(f"  tm1={str(tm1):>4s} chain_lo={chain_lo:3d} -> {got} "
              f"(expect {(exp_cap, exp_start)})  {why}")
        ok &= got == (exp_cap, exp_start)

    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
