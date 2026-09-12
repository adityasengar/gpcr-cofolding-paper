#!/usr/bin/env python3
"""Build and hash every sequence the redo would supply. Ground truth only.

Sources, all named in the output:
  * UniProt REST  https://rest.uniprot.org/uniprotkb/{acc}  -> canonical sequence,
    sequence version (`sequence.version`), entry version, last modified date.
  * GPCRdb/GproteinDb REST https://gpcrdb.org/services/residues/{entry_name}/
    -> per-residue CGN segment assignment (G.H5 = alpha5 helix, G.S6 = beta6).

Nothing here is written from memory. Every construct is derived by slicing a
fetched sequence and is keyed by sha256 of its one-letter bytes.

Usage:  python3 redo/build/seq_build.py  > redo/inputs/seq_constructs.tsv
"""
import os
import hashlib
import json
import sys
import time
import urllib.request

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo

UNIPROT_JSON = "https://rest.uniprot.org/uniprotkb/%s.json"
GPCRDB_RES = "https://gpcrdb.org/services/residues/%s/"

# family -> (uniprot accession, gpcrdb/gproteindb entry_name)
GALPHA = {
    "Gs":    ("P63092", "gnas2_human"),
    "Golf":  ("P38405", "gnal_human"),
    "Gi1":   ("P63096", "gnai1_human"),
    "Gi2":   ("P04899", "gnai2_human"),
    "Gi3":   ("P08754", "gnai3_human"),
    "Go":    ("P09471", "gnao_human"),
    "Gz":    ("P19086", "gnaz_human"),
    "Gt1":   ("P11488", "gnat1_human"),
    "Gt1_bovine": ("P04695", None),
    "Gt2":   ("P19087", "gnat2_human"),
    "Ggust": ("A8MTJ3", "gnat3_human"),
    "Gq":    ("P50148", "gnaq_human"),
    "G11":   ("P29992", "gna11_human"),
    "G14":   ("O95837", "gna14_human"),
    "G15":   ("P30679", "gna15_human"),
    "G12":   ("Q03113", "gna12_human"),
    "G13":   ("Q14344", "gna13_human"),
}
OTHER = {
    "Gbeta1": "P62873",
    "Ggamma2": "P59768",
}

_cache = {}


def get(url, raw=False):
    if url in _cache:
        return _cache[url]
    for attempt in range(4):
        try:
            body = urllib.request.urlopen(url, timeout=45).read().decode()
            _cache[url] = body if raw else json.loads(body)
            return _cache[url]
        except Exception as exc:                       # noqa: BLE001
            if attempt == 3:
                raise RuntimeError(f"{url}: {exc}")
            time.sleep(2 * (attempt + 1))


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def uniprot(acc):
    d = get(UNIPROT_JSON % acc)
    seq = d["sequence"]["value"]
    return {
        "accession": acc,
        "id": d["uniProtkbId"],
        "seq": seq,
        "length": len(seq),
        "seq_version": d["entryAudit"]["sequenceVersion"],
        "entry_version": d["entryAudit"]["entryVersion"],
        "last_seq_update": d["entryAudit"]["lastSequenceUpdateDate"],
        "last_entry_update": d["entryAudit"]["lastAnnotationUpdateDate"],
        "organism": d["organism"]["scientificName"],
        "gene": (d.get("genes") or [{}])[0].get("geneName", {}).get("value", ""),
    }


def cgn_segments(entry_name):
    """Return {segment: (first_resnum, last_resnum)} from GPCRdb CGN residues."""
    rows = get(GPCRDB_RES % entry_name)
    out = {}
    for r in rows:
        seg = r["protein_segment"]
        n = r["sequence_number"]
        lo, hi = out.get(seg, (n, n))
        out[seg] = (min(lo, n), max(hi, n))
    return out, rows


def main():
    recs = {}
    for fam, (acc, entry) in GALPHA.items():
        u = uniprot(acc)
        segs, rows = ({}, [])
        if entry:
            try:
                segs, rows = cgn_segments(entry)
            except RuntimeError as exc:
                print(f"# GPCRDB FETCH FAILED {entry}: {exc}", file=sys.stderr)
        recs[fam] = {"u": u, "segs": segs, "res": rows}

    print("\t".join([
        "family", "accession", "uniprot_id", "organism", "gene", "full_len",
        "seq_version", "entry_version", "last_seq_update",
        "H5_range", "H5_len", "S6_range", "S6_len", "hgS6H5_range",
        "ct11_range", "ct11_seq", "ct11_sha256",
        "ct21_range", "ct21_seq", "ct21_sha256",
        "H5_seq", "H5_sha256",
        "full_sha256",
    ]))
    for fam, r in recs.items():
        u, segs = r["u"], r["segs"]
        seq, L = u["seq"], u["length"]
        h5 = segs.get("G.H5")
        s6 = segs.get("G.S6")
        hg = segs.get("G.hgS6H5") or segs.get("G.HG")
        ct11, ct21 = seq[-11:], seq[-21:]
        h5seq = seq[h5[0] - 1:h5[1]] if h5 else ""
        print("\t".join(map(str, [
            fam, u["accession"], u["id"], u["organism"], u["gene"], L,
            u["seq_version"], u["entry_version"], u["last_seq_update"],
            f"{h5[0]}-{h5[1]}" if h5 else "NA", (h5[1] - h5[0] + 1) if h5 else "NA",
            f"{s6[0]}-{s6[1]}" if s6 else "NA", (s6[1] - s6[0] + 1) if s6 else "NA",
            f"{hg[0]}-{hg[1]}" if hg else "NA",
            f"{L-10}-{L}", ct11, sha(ct11),
            f"{L-20}-{L}", ct21, sha(ct21),
            h5seq, sha(h5seq) if h5seq else "NA",
            sha(seq),
        ])))

    # segment inventory for one subunit, so the CGN vocabulary is on the record
    print("\n# CGN segments present for gnas2_human / gnai1_human:", file=sys.stderr)
    for fam in ("Gs", "Gi1"):
        print(f"#   {fam}: " + ", ".join(
            f"{k}:{v[0]}-{v[1]}" for k, v in sorted(
                recs[fam]["segs"].items(), key=lambda kv: kv[1][0])), file=sys.stderr)

    # the other chains
    print("\n# non-alpha chains", file=sys.stderr)
    for name, acc in OTHER.items():
        u = uniprot(acc)
        print(f"# {name}\t{acc}\t{u['id']}\tlen={u['length']}\tSV={u['seq_version']}"
              f"\tsha256={sha(u['seq'])}", file=sys.stderr)
        print(f"# {name}_SEQ\t{u['seq']}", file=sys.stderr)

    # full sequences, dumped to stderr so the TSV stays narrow
    print("\n# full canonical sequences", file=sys.stderr)
    for fam, r in recs.items():
        print(f"# {fam}\t{r['u']['accession']}\t{r['u']['seq']}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
