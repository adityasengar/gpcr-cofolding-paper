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

        start = max(1, tm1 - N_CAP) if tm1 else 1
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
            "trim_start": start, "trim_end": end,
            "trim_len": len(trimmed),
            "n_removed_nterm": start - 1,
            "n_removed_cterm": L - end,
            "n_removed_total": (start - 1) + (L - end),
            "pct_removed": round(100 * ((start - 1) + (L - end)) / L, 1),
            "cap_binds_nterm": "yes" if start > 1 else "no",
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


def selftest():
    """The cap must be a cap: idempotent, and inert on a short terminus."""
    ok = True
    seq = "M" * 500
    for tm1, h8end, exp_start, exp_end in [
        (400, 450, 350, 500),      # long N-term: cap binds at 400-50
        (10, 450, 1, 500),         # short N-term: cap inert, start stays 1
        (60, 380, 10, 480),        # both bind
        (51, 399, 1, 499),         # exactly at the cap: start 1, end 499
    ]:
        start = max(1, tm1 - N_CAP)
        end = min(len(seq), h8end + C_CAP)
        got = (start, end)
        print(f"  TM1={tm1:3d} H8end={h8end:3d} -> {got} (expect "
              f"{(exp_start, exp_end)})")
        ok &= got == (exp_start, exp_end)
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
