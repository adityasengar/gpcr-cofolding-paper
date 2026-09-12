#!/usr/bin/env python3
"""Fetch and hash chain A — the receptor sequence — for every panel receptor.

Companion to `redo/build/seq_build.py`, which did the same job for chain B
(the Gα partner). Same conventions, deliberately:

  * every sequence comes from a fetched UniProt record, never from memory;
  * accession + sequence version + last-sequence-update date recorded;
  * sha256 of the uppercase one-letter bytes is the construct key.

Sources
  UniProt REST  https://rest.uniprot.org/uniprotkb/{acc}.json
    -> canonical sequence, sequence version, entry version, audit dates,
       and the full feature table (SIGNAL, CHAIN, TRANSMEM, TOPO_DOM,
       CARBOHYD, DISULFID, LIPID, MOD_RES, VAR_SEQ) plus ALTERNATIVE
       PRODUCTS comments (isoform census).

Roster
  redo/inputs/panel_systems.csv, column `uniprot_acc`, all 75 rows.
  Plus the human orthologues of the three non-human panel entries, fetched
  so the substitution question in SEQ_RECEPTORS.md §5 is costed on real
  records rather than asserted.

Usage
  python3 redo/build/seqrec_build.py            # writes the three outputs
  python3 redo/build/seqrec_build.py --stdout   # TSV to stdout instead
"""
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
OUT_TSV = os.path.join(INPUTS, "seqrec_receptors.tsv")
OUT_FASTA = os.path.join(INPUTS, "seqrec_canonical.fasta")
OUT_FEAT = os.path.join(INPUTS, "seqrec_features.tsv")

UNIPROT_JSON = "https://rest.uniprot.org/uniprotkb/%s.json"

# Human orthologues of the three non-human panel entries. Fetched so that the
# "should we substitute?" decision is costed against a real record. NOT a
# substitution — SEQ_RECEPTORS.md presents it as a PI decision.
ORTHOLOGUES = {
    "OPSD": ("P08100", "human orthologue of OPSD_BOVIN P02699"),
    "OPRM": ("P35372", "human orthologue of OPRM_MOUSE P42866"),
    # B1B1U5 (Kumopsin1, Hasarius adansoni) has no human orthologue; the
    # nearest human relatives are the opsins, which are already on the panel.
}

_cache = {}


def get(url):
    if url in _cache:
        return _cache[url]
    for attempt in range(4):
        try:
            body = urllib.request.urlopen(url, timeout=60).read().decode()
            _cache[url] = json.loads(body)
            return _cache[url]
        except Exception as exc:                       # noqa: BLE001
            if attempt == 3:
                raise RuntimeError(f"{url}: {exc}")
            time.sleep(2 * (attempt + 1))


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def _pos(f, key):
    try:
        return f["location"][key]["value"]
    except (KeyError, TypeError):
        return None


def parse(acc):
    d = get(UNIPROT_JSON % acc)
    seq = d["sequence"]["value"]
    feats = d.get("features", [])

    def ranges(ftype):
        out = []
        for f in feats:
            if f["type"] != ftype:
                continue
            s, e = _pos(f, "start"), _pos(f, "end")
            if s is None or e is None:
                continue
            out.append((s, e, f.get("description", "")))
        return sorted(out)

    signal = ranges("Signal")
    propep = ranges("Propeptide")
    chain = ranges("Chain")
    tm = ranges("Transmembrane")
    topo = ranges("Topological domain")
    glyc = ranges("Glycosylation")
    ss = ranges("Disulfide bond")
    lipid = ranges("Lipidation")
    modres = ranges("Modified residue")
    varseq = ranges("Alternative sequence")

    # isoform census from ALTERNATIVE PRODUCTS
    iso_names, n_iso, canon_iso = [], 1, ""
    for c in d.get("comments", []):
        if c.get("commentType") == "ALTERNATIVE PRODUCTS":
            isos = c.get("isoforms", [])
            n_iso = len(isos)
            for i in isos:
                nm = (i.get("name") or {}).get("value", "")
                ids = ",".join(i.get("isoformIds", []))
                seqstat = i.get("isoformSequenceStatus", "")
                iso_names.append(f"{ids}:{nm}:{seqstat}")
                if seqstat == "Displayed":
                    canon_iso = ids

    # derived construct boundaries
    tm1_start = tm[0][0] if tm else None
    tm7_end = tm[-1][1] if tm else None
    sig_end = signal[0][1] if signal else 0
    mature_start = (chain[0][0] if chain else 1)

    rec = {
        "accession": d["primaryAccession"],
        "uniprot_id": d["uniProtkbId"],
        "protein_name": (d.get("proteinDescription", {}).get("recommendedName", {})
                         .get("fullName", {}).get("value", "")),
        "gene": (d.get("genes") or [{}])[0].get("geneName", {}).get("value", ""),
        "organism": d["organism"]["scientificName"],
        "taxid": d["organism"]["taxonId"],
        "length": len(seq),
        "seq_version": d["entryAudit"]["sequenceVersion"],
        "entry_version": d["entryAudit"]["entryVersion"],
        "last_seq_update": d["entryAudit"]["lastSequenceUpdateDate"],
        "last_entry_update": d["entryAudit"]["lastAnnotationUpdateDate"],
        "sha256": sha(seq),
        "signal": f"{signal[0][0]}-{signal[0][1]}" if signal else "none",
        "signal_len": sig_end if signal else 0,
        "propeptide": ";".join(f"{a}-{b}" for a, b, _ in propep) or "none",
        "chain_range": f"{chain[0][0]}-{chain[0][1]}" if chain else "NA",
        "n_tm": len(tm),
        "tm1_start": tm1_start if tm1_start else "NA",
        "tm7_end": tw if (tw := tm7_end) else "NA",
        "nterm_len_before_tm1": (tm1_start - 1) if tm1_start else "NA",
        "nterm_len_after_signal": (tm1_start - 1 - sig_end) if tm1_start else "NA",
        "cterm_len_after_tm7": (len(seq) - tm7_end) if tm7_end else "NA",
        "core_tm1_tm7_len": (tm7_end - tm1_start + 1) if tm else "NA",
        "n_isoforms": n_iso,
        "canonical_isoform": canon_iso,
        "isoforms": "|".join(iso_names) or "single",
        "n_varseq_features": len(varseq),
        "n_glyc": len(glyc),
        "n_disulfide": len(ss),
        "n_lipid": len(lipid),
        "lipid_sites": ";".join(f"{a}:{c}" for a, b, c in lipid) or "none",
        "n_modres": len(modres),
        "seq": seq,
        "_tm": tm,
        "_topo": topo,
        "_glyc": glyc,
        "_ss": ss,
        "_signal": signal,
        "_chain": chain,
    }
    # mature construct (signal peptide removed), if there is one
    if signal:
        mat = seq[mature_start - 1:]
        rec["mature_len"] = len(mat)
        rec["mature_sha256"] = sha(mat)
    else:
        rec["mature_len"] = len(seq)
        rec["mature_sha256"] = rec["sha256"]
    # 7TM-core-only construct, TM1 start .. TM7 end (a costing reference, not a
    # recommendation: SEQ_RECEPTORS.md §4 argues against supplying it)
    if tm:
        core = seq[tm1_start - 1:tm7_end]
        rec["core_sha256"] = sha(core)
    else:
        rec["core_sha256"] = "NA"
    return rec


COLS = ["slug", "tier", "gpcr_class", "accession", "uniprot_id", "gene", "organism",
        "taxid", "length", "seq_version", "entry_version", "last_seq_update",
        "sha256", "signal", "signal_len", "propeptide", "chain_range",
        "mature_len", "mature_sha256", "n_tm", "tm1_start", "tm7_end",
        "nterm_len_before_tm1", "nterm_len_after_signal", "cterm_len_after_tm7",
        "core_tm1_tm7_len", "core_sha256", "n_isoforms", "canonical_isoform",
        "n_varseq_features", "n_glyc", "n_disulfide", "n_lipid", "lipid_sites",
        "n_modres", "protein_name", "isoforms"]


def main():
    rows = list(csv.DictReader(open(PANEL)))
    recs = []
    for r in rows:
        acc = r["uniprot_acc"].strip()
        if not acc:
            print(f"# NO ACCESSION {r['slug']}", file=sys.stderr)
            continue
        rec = parse(acc)
        rec["slug"] = r["slug"]
        rec["tier"] = r["tier"]
        rec["gpcr_class"] = r["gpcr_class"]
        recs.append(rec)
        print(f"# {r['slug']:8s} {acc} {rec['length']:4d} SV{rec['seq_version']}",
              file=sys.stderr)

    for slug, (acc, note) in ORTHOLOGUES.items():
        rec = parse(acc)
        rec["slug"] = slug + "_HUMAN_ORTHOLOGUE"
        rec["tier"] = "orthologue-candidate"
        rec["gpcr_class"] = "A"
        recs.append(rec)
        print(f"# {rec['slug']:26s} {acc} {rec['length']:4d}  ({note})",
              file=sys.stderr)

    out = sys.stdout if "--stdout" in sys.argv else open(OUT_TSV, "w")
    w = csv.DictWriter(out, fieldnames=COLS, delimiter="\t", extrasaction="ignore")
    w.writeheader()
    for rec in recs:
        w.writerow(rec)
    if out is not sys.stdout:
        out.close()

    with open(OUT_FASTA, "w") as fh:
        for rec in recs:
            fh.write(f">{rec['slug']}|{rec['accession']}|{rec['uniprot_id']}"
                     f"|SV{rec['seq_version']}|len={rec['length']}"
                     f"|sha256={rec['sha256']}\n")
            for i in range(0, len(rec["seq"]), 60):
                fh.write(rec["seq"][i:i + 60] + "\n")

    with open(OUT_FEAT, "w") as fh:
        fh.write("slug\taccession\tfeature\tstart\tend\tdescription\n")
        for rec in recs:
            for key, label in (("_signal", "SIGNAL"), ("_chain", "CHAIN"),
                               ("_tm", "TRANSMEM"), ("_topo", "TOPO_DOM"),
                               ("_glyc", "CARBOHYD"), ("_ss", "DISULFID")):
                for a, b, desc in rec[key]:
                    fh.write(f"{rec['slug']}\t{rec['accession']}\t{label}\t{a}\t{b}\t{desc}\n")

    print(f"\n# wrote {OUT_TSV}, {OUT_FASTA}, {OUT_FEAT} "
          f"({len(recs)} records)", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
