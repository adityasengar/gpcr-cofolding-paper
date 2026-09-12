#!/usr/bin/env python3
"""Fetch the three independent authorities on 'which Ga is cognate' for the C1 panel.

WHY THREE, AND WHY NOT ONE. The project has been routing arms by a coupling
table (`refs/gpcr_coupling.csv`) that lives on HPC and ships in no drop, so the
assignment behind 40,000 predictions has no recoverable provenance. Worse, the
natural single source does not agree with itself: GproteinDb's own paper reports
68% inter-dataset agreement on the primary transducer at FAMILY level and 22% at
SUBTYPE level (lit/notes/pandyszekeres2024gproteindb.md p.8). A single confident
answer per receptor is therefore not a thing that exists. This script fetches
three authorities separately and never merges them:

  A1  GproteinDb couplings browser (https://gproteindb.org/signprot/couplings)
      -- one row per receptor x source lab. Sources: GproteinDb (the integrated
      consensus), GtoPdb, Bouvier/GEMTA, Inoue/TGFa-shedding+NanoBiT,
      Martemyanov/FreeGbg-Nluc, Lambert/RGB-GDP, Roth. Carries primary family,
      primary subtype, family rank orders and quantitative values.

  A2  IUPHAR/BPS Guide to PHARMACOLOGY, /services/targets/{id}/transduction.
      This is the curator's prose annotation, fetched from IUPHAR direct rather
      than through GproteinDb's copy of it, so the two can be compared.

  A3  The deposited active reference structure itself, via the RCSB GraphQL
      API -- every polymer entity, its description, its UniProt cross-reference,
      its organism and its full one-letter sequence.

A3 IS THE ONLY ONE THAT IS NOT AN ANNOTATION. A1 and A2 say what a receptor is
believed to couple; A3 says what is physically in the coordinate file we score
our predictions against. If our supplied partner and the reference assembly's
partner are different Ga families, that is an internal inconsistency in our own
experiment and needs no external authority to adjudicate.

A3 IS ALSO NOT READ FROM THE ACCESSION. Following analysis/verify_alpha5ct_family.py:
coupling chimeras are a Ga backbone carrying another family's C-terminal helix,
and on those entries the UniProt cross-reference names the BACKBONE. The family
is therefore read from the DEPOSITED C-terminal 21 residues, with ties reported
as ties (Gi1==Gi2 and Gq==G11 are byte-identical over that window, so resolving
them would be inventing information).

Writes only coupling_*-prefixed files. Nothing here edits a drop.

Usage:  python3 redo/build/coupling_fetch.py [--skip-html]
"""
import csv
import json
import os
import re
import sys
import time
import urllib.request

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
PANEL = os.path.join(INPUTS, "panel_systems.csv")
SEQ_RUNGS = os.path.join(INPUTS, "seq_rungs.tsv")

GPDB_COUPLINGS = "https://gproteindb.org/signprot/couplings"
GTOP_TARGET = "https://www.guidetopharmacology.org/services/targets?accession=%s"
GTOP_TRANSD = "https://www.guidetopharmacology.org/services/targets/%d/transduction"
RCSB_GQL = "https://data.rcsb.org/graphql"
UNIPROT = "https://rest.uniprot.org/uniprotkb/%s.fasta"

ALPHA5_CT_LEN = 21

# One canonical accession per Ga family -- identical list to
# analysis/verify_alpha5ct_family.py so the two scripts cannot drift.
FAMILIES = {
    "Gs": "P63092", "Golf": "P38405",
    "Gi1": "P63096", "Gi2": "P04899", "Gi3": "P08754",
    "Go": "P09471", "Gt1": "P04695", "Gt2": "P19087", "Ggust": "P29033",
    "Gz": "P19086",
    "Gq": "P50148", "G11": "P29992", "G14": "O95837", "G15": "P30679",
    "G12": "Q03113", "G13": "Q14344",
}
FAMILY_OF = {
    "Gs": "Gs", "Golf": "Gs",
    "Gi1": "Gi/o", "Gi2": "Gi/o", "Gi3": "Gi/o", "Go": "Gi/o",
    "Gt1": "Gi/o", "Gt2": "Gi/o", "Ggust": "Gi/o", "Gz": "Gi/o",
    "Gq": "Gq/11", "G11": "Gq/11", "G14": "Gq/11", "G15": "Gq/11",
    "G12": "G12/13", "G13": "G12/13",
}


def _get(url, parse=json.loads, timeout=60):
    for attempt in range(3):
        try:
            return parse(urllib.request.urlopen(url, timeout=timeout).read().decode(
                "utf-8", "replace"))
        except Exception as exc:                                    # noqa: BLE001
            if attempt == 2:
                return {"_err": str(exc)}
            time.sleep(1.5 * (attempt + 1))


def strip(html):
    t = re.sub(r"<[^>]+>", " ", html or "")
    t = t.replace("&nbsp;", " ").replace("&amp;", "&")
    return " ".join(t.split())


# ---------------------------------------------------------------- the panel

def c1_receptors():
    rows = [r for r in csv.DictReader(open(PANEL))
            if "C1" in r["tier"].split("|")]
    out = []
    for r in rows:
        act = []
        for k in ("strict_active_pdb", "our_active", "gdb_active", "cn_active"):
            v = (r.get(k) or "").strip().upper()
            if v and v not in act:
                act.append(v)
        inact = []
        for k in ("strict_inactive_pdb", "our_inactive", "gdb_inactive", "cn_inactive"):
            v = (r.get(k) or "").strip().upper()
            if v and v not in inact:
                inact.append(v)
        out.append({
            "slug": r["slug"], "gene": r["gene"], "acc": r["uniprot_acc"],
            "uniprot_entry": r["uniprot_entry"], "gpcrdb_slug": r["gpcrdb_slug"],
            "organism": r["organism"], "tier": r["tier"],
            "active_pdbs": act, "inactive_pdbs": inact,
        })
    return out


# ------------------------------------------------- A1: GproteinDb couplings

GPDB_COLS = [
    "_sel", "uniprot", "gtopdb_name", "gpcrdb", "rec_family", "cls",
    "other_protein", "lab", "biosensor", "downstream_steps", "n_gprots_tested",
    "ref", "ligand_name", "phys_surr",
    "nds_Gs", "nds_Gio", "nds_Gq11", "nds_G1213",
    "primary_family", "n_fam",
    "rank_Gs", "rank_Gio", "rank_Gq11", "rank_G1213",
    "pct_Gs", "pct_Gio", "pct_Gq11", "pct_G1213",
    "fam_parameter", "val_Gs", "val_Gio", "val_Gq11", "val_G1213",
    "primary_subtype",
    "pct_GsL", "pct_GsS", "pct_Golf", "pct_Gi1", "pct_Gi2", "pct_Gi3",
    "pct_Ggust", "pct_Gz", "pct_GoA", "pct_GoB", "pct_Gq", "pct_G11",
    "pct_G14", "pct_G15", "pct_G12", "pct_G13",
    "sub_parameter",
    "val_GsL", "val_GsS", "val_Golf", "val_Gi1", "val_Gi2", "val_Gi3",
    "val_Ggust", "val_Gz", "val_GoA", "val_GoB", "val_Gq", "val_G11",
    "val_G14", "val_G15", "val_G12", "val_G13",
]


def fetch_gproteindb(cache_html):
    if os.path.exists(cache_html):
        html = open(cache_html, encoding="utf-8", errors="replace").read()
    else:
        html = _get(GPDB_COUPLINGS, parse=lambda b: b, timeout=300)
        if isinstance(html, dict):
            print("GproteinDb fetch failed: %s" % html["_err"], file=sys.stderr)
            return []
        open(cache_html, "w", encoding="utf-8").write(html)

    i, j = html.find("<tbody"), html.find("</tbody>")
    body = html[i:j]
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(cells) != len(GPDB_COLS):
            continue
        row = dict(zip(GPDB_COLS, [strip(c) for c in cells]))
        m = re.search(r"uniprot\.org/uniprot/(\w+)", cells[1])
        row["acc"] = m.group(1) if m else ""
        m = re.search(r'href="/protein/([\w\-]+)"', cells[3])
        row["gpcrdb_slug"] = m.group(1) if m else ""
        m = re.search(r"doi\.org/([^']+)'", cells[11])
        row["ref_doi"] = m.group(1) if m else ""
        row["ref_text"] = strip(re.sub(r"&lt;[^&]*&gt;", " ",
                                       re.search(r"data-content=\"(.*?)\"", cells[11], re.S).group(1)
                                       if re.search(r"data-content=\"(.*?)\"", cells[11], re.S) else ""))
        row.pop("_sel", None)
        out.append(row)
    return out


# ---------------------------------------------------- A2: IUPHAR direct API

# IUPHAR curates by gene, not by species record, and three C1 receptors are not
# human. Their own accession 404s, so the HUMAN ORTHOLOG is looked up instead and
# the substitution is recorded per row -- never silently. B1B1U5 (jumping-spider
# Kumopsin1) has no human ortholog and stays unresolved, which is the finding.
ORTHOLOG = {
    "P02699": ("P08100", "bovine RHO -> human RHO; IUPHAR has no bovine record"),
    "P42866": ("P35372", "mouse Oprm1 -> human OPRM1; IUPHAR has no mouse record"),
}


def fetch_gtopdb(receptors):
    out = []
    for r in receptors:
        rec = {"slug": r["slug"], "acc": r["acc"], "queried_acc": r["acc"],
               "ortholog_note": "", "gtopdb_target_id": "",
               "gtopdb_name": "", "transducers": "", "effectors": "",
               "comment_head": "", "status": ""}
        query_acc = r["acc"]
        hits = _get(GTOP_TARGET % query_acc)
        if (not hits or (isinstance(hits, dict) and "_err" in hits)) \
                and r["acc"] in ORTHOLOG:
            query_acc, note = ORTHOLOG[r["acc"]]
            rec["queried_acc"], rec["ortholog_note"] = query_acc, note
            hits = _get(GTOP_TARGET % query_acc)
        if isinstance(hits, dict) and "_err" in hits:
            rec["status"] = "lookup-failed: " + hits["_err"][:60]
            out.append(rec)
            continue
        if not hits:
            rec["status"] = "NO-GTOPDB-TARGET-FOR-ACCESSION"
            out.append(rec)
            continue
        tid = hits[0]["targetId"]
        rec["gtopdb_target_id"] = tid
        rec["gtopdb_name"] = strip(hits[0]["name"])
        td = _get(GTOP_TRANSD % tid)
        if isinstance(td, dict) and "_err" in td:
            rec["status"] = "transduction-failed"
        elif not td:
            rec["status"] = "NO-TRANSDUCTION-RECORD"
        else:
            rec["transducers"] = " || ".join(strip(x.get("transducers")) for x in td)
            rec["effectors"] = " || ".join(strip(x.get("effectors")) for x in td)
            rec["comment_head"] = strip(td[0].get("comments"))[:300]
            rec["status"] = "ok"
        out.append(rec)
        time.sleep(0.15)
    return out


# ------------------------------------------ A3: the deposited reference itself

GQL = """
query($ids:[String!]!){
  entries(entry_ids:$ids){
    rcsb_id
    struct{title}
    rcsb_entry_info{resolution_combined experimental_method}
    polymer_entities{
      rcsb_id
      rcsb_polymer_entity{pdbx_description pdbx_mutation}
      entity_poly{pdbx_seq_one_letter_code_can rcsb_sample_sequence_length}
      rcsb_entity_source_organism{ncbi_scientific_name}
      rcsb_polymer_entity_container_identifiers{
        auth_asym_ids
        reference_sequence_identifiers{database_name database_accession}}
    }
  }
}"""


def fetch_rcsb(pdb_ids, chunk=20):
    entries = {}
    ids = sorted(set(pdb_ids))
    for k in range(0, len(ids), chunk):
        batch = ids[k:k + chunk]
        payload = json.dumps({"query": GQL, "variables": {"ids": batch}}).encode()
        req = urllib.request.Request(RCSB_GQL, data=payload,
                                     headers={"Content-Type": "application/json"})
        for attempt in range(3):
            try:
                d = json.load(urllib.request.urlopen(req, timeout=120))
                break
            except Exception as exc:                                # noqa: BLE001
                if attempt == 2:
                    print("RCSB batch failed %s: %s" % (batch, exc), file=sys.stderr)
                    d = {"data": {"entries": []}}
                time.sleep(2 * (attempt + 1))
        for e in (d.get("data", {}) or {}).get("entries", []) or []:
            entries[e["rcsb_id"].upper()] = e
    missing = [p for p in ids if p not in entries]
    if missing:
        print("RCSB returned nothing for: %s" % missing, file=sys.stderr)
    return entries


# -------------------------------------------------- classifying an entity

RECEPTOR_HINTS = ("receptor", "rhodopsin", "opsin")
GA_HINTS = ("subunit alpha", "g-alpha", "galpha", "mini-g", "minig")
BETA_HINTS = ("subunit beta",)
GAMMA_HINTS = ("subunit gamma",)


def classify(desc, length, acc, seq):
    """What KIND of chain is this. Deliberately coarse; family comes separately."""
    d = (desc or "").lower()
    if "nanobody" in d or re.search(r"\bnb\d", d) or "single-chain variable" in d \
            or "scfv" in d or "fab " in d or "fragment antigen" in d \
            or "antibody" in d or "immunoglobulin" in d or "vhh" in d:
        return "nanobody/antibody"
    if "arrestin" in d:
        return "arrestin"
    if "lysozyme" in d or "rubredoxin" in d or "bril" in d or "apocytochrome" in d \
            or "thermostabili" in d:
        return "fusion-partner"
    if "subunit beta" in d and "g(" in d or any(h in d for h in BETA_HINTS):
        return "G-beta"
    if any(h in d for h in GAMMA_HINTS):
        return "G-gamma"
    if "g(i)/g(s)/g(t)" in d or "g(i)/g(s)/g(o)" in d:
        # these descriptions are beta / gamma despite naming alpha families
        return "G-beta" if (length or 0) > 200 else "G-gamma"
    if any(h in d for h in GA_HINTS) or "nucleotide-binding protein" in d:
        return "G-alpha"
    if "scaffold" in d or "dngas" in d:
        return "G-alpha"
    if any(h in d for h in RECEPTOR_HINTS):
        return "receptor"
    if "peptide" in d and (length or 0) <= 40:
        return "peptide-ligand-or-ga-peptide"
    return "other"


def canonical_termini():
    """Last-21 of every canonical family. Cached to a coupling_ file."""
    cache = os.path.join(CACHE, "coupling_family_termini.json")
    if os.path.exists(cache):
        return json.load(open(cache))
    out = {}
    for name, acc in FAMILIES.items():
        fa = _get(UNIPROT % acc, parse=lambda b: b)
        if isinstance(fa, dict):
            print("UniProt fetch failed for %s/%s" % (name, acc), file=sys.stderr)
            continue
        seq = "".join(l for l in fa.split("\n") if not l.startswith(">"))
        out[name] = {"acc": acc, "len": len(seq), "ct21": seq[-ALPHA5_CT_LEN:],
                     "ct11": seq[-11:]}
    json.dump(out, open(cache, "w"), indent=1)
    return out


def ga_family_from_cterm(seq, termini):
    """Best-matching family/families by the deposited last 21. Ties kept as ties.

    Returns (best_names, identity, note). A partner whose deposited C-terminus is
    truncated -- very common for mini-G and for scaffolded constructs -- is
    reported as such rather than scored, because its last 21 residues are not
    its alpha5-CT at all.
    """
    if not seq or len(seq) < ALPHA5_CT_LEN:
        return [], 0.0, "too-short-to-score"
    ct = seq[-ALPHA5_CT_LEN:]
    scored = sorted(((sum(1 for a, b in zip(ct, t["ct21"]) if a == b) / float(ALPHA5_CT_LEN), n)
                     for n, t in termini.items()), reverse=True)
    best_id = scored[0][0]
    best = sorted(n for i, n in scored if i == best_id)
    note = "" if best_id >= 0.80 else "C-TERMINUS-UNRECOGNISED"
    return best, best_id, note


def main():
    scratch = os.environ.get("COUPLING_SCRATCH", "/tmp")
    recs = c1_receptors()
    print("C1 receptors: %d" % len(recs))

    # ---- A1
    gp = fetch_gproteindb(os.path.join(scratch, "gproteindb_couplings.html"))
    print("GproteinDb coupling rows parsed: %d" % len(gp))
    if gp:
        wanted = {x["acc"] for x in recs}
        wanted |= {ORTHOLOG[a][0] for a in wanted if a in ORTHOLOG}
        keep = [r for r in gp if r["acc"] in wanted]
        print("  rows matching a C1 accession: %d (%d receptors)"
              % (len(keep), len({r['acc'] for r in keep})))
        cols = ["acc", "uniprot", "gpcrdb_slug", "lab", "biosensor",
                "primary_family", "primary_subtype", "n_fam",
                "rank_Gs", "rank_Gio", "rank_Gq11", "rank_G1213",
                "pct_Gs", "pct_Gio", "pct_Gq11", "pct_G1213",
                "fam_parameter", "val_Gs", "val_Gio", "val_Gq11", "val_G1213",
                "n_gprots_tested", "ligand_name", "phys_surr", "ref_doi", "ref_text"] + \
               [c for c in GPDB_COLS if c.startswith("pct_G") and c not in
                ("pct_Gs", "pct_Gio", "pct_Gq11", "pct_G1213")]
        with open(os.path.join(INPUTS, "coupling_gproteindb.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for r in sorted(keep, key=lambda x: (x["uniprot"], x["lab"])):
                w.writerow(r)

    # ---- A2
    gt = fetch_gtopdb(recs)
    with open(os.path.join(INPUTS, "coupling_gtopdb.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(gt[0].keys()))
        w.writeheader()
        w.writerows(gt)
    print("GtoPdb transduction fetched: %d ok, %d problem"
          % (sum(1 for r in gt if r["status"] == "ok"),
             sum(1 for r in gt if r["status"] != "ok")))

    # ---- A3
    termini = canonical_termini()
    pdbs = sorted({p for r in recs for p in r["active_pdbs"]})
    inact = sorted({p for r in recs for p in r["inactive_pdbs"]})
    entries = fetch_rcsb(pdbs + inact)
    print("RCSB entries fetched: %d of %d" % (len(entries), len(set(pdbs + inact))))
    json.dump({k: v for k, v in entries.items()},
              open(os.path.join(CACHE, "coupling_rcsb_entities.json"), "w"), indent=1)

    rows = []
    for r in recs:
        for role, plist in (("active", r["active_pdbs"]), ("inactive", r["inactive_pdbs"])):
            for pdb in plist:
                e = entries.get(pdb)
                if not e:
                    rows.append({"slug": r["slug"], "role": role, "pdb": pdb,
                                 "entity": "", "kind": "FETCH-FAILED"})
                    continue
                for pe in e.get("polymer_entities") or []:
                    meta = pe.get("rcsb_polymer_entity") or {}
                    poly = pe.get("entity_poly") or {}
                    seq = (poly.get("pdbx_seq_one_letter_code_can") or "").replace("\n", "")
                    ids = pe.get("rcsb_polymer_entity_container_identifiers") or {}
                    acc = ""
                    for ref in ids.get("reference_sequence_identifiers") or []:
                        if ref.get("database_name") == "UniProt":
                            acc = ref.get("database_accession")
                            break
                    orgs = sorted({(o or {}).get("ncbi_scientific_name") or ""
                                   for o in pe.get("rcsb_entity_source_organism") or []})
                    desc = meta.get("pdbx_description") or ""
                    n = poly.get("rcsb_sample_sequence_length")
                    kind = classify(desc, n, acc, seq)
                    row = {
                        "slug": r["slug"], "receptor_acc": r["acc"],
                        "receptor_organism": r["organism"], "role": role, "pdb": pdb,
                        "title": (e.get("struct") or {}).get("title", ""),
                        "method": (e.get("rcsb_entry_info") or {}).get("experimental_method", ""),
                        "entity": pe["rcsb_id"], "chains": "/".join(ids.get("auth_asym_ids") or []),
                        "description": desc, "length": n, "uniprot": acc,
                        "organism": ";".join(x for x in orgs if x),
                        "pdbx_mutation": meta.get("pdbx_mutation") or "",
                        "kind": kind, "ct21_family": "", "ct21_identity": "",
                        "ct21_note": "", "xref_family": "",
                    }
                    if kind in ("G-alpha", "peptide-ligand-or-ga-peptide"):
                        best, ident, note = ga_family_from_cterm(seq, termini)
                        row["ct21_family"] = "/".join(best)
                        row["ct21_identity"] = "%.2f" % ident
                        row["ct21_note"] = note
                        row["xref_family"] = next(
                            (n2 for n2, a in FAMILIES.items() if a == acc), "")
                        row["ct21"] = seq[-ALPHA5_CT_LEN:] if len(seq) >= ALPHA5_CT_LEN else seq
                    rows.append(row)

    cols = ["slug", "receptor_acc", "receptor_organism", "role", "pdb", "method",
            "entity", "chains", "kind", "description", "length", "uniprot",
            "organism", "xref_family", "ct21_family", "ct21_identity", "ct21_note",
            "ct21", "pdbx_mutation", "title"]
    with open(os.path.join(INPUTS, "coupling_refstructures.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("reference entity rows: %d" % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
