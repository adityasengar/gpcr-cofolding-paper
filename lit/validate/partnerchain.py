#!/usr/bin/env python3
"""
partnerchain.py - check what the NON-RECEPTOR chains of a structure actually are.

Written 2026-09-10 after 4X1H. Its active reference was annotated "native alpha5-CT
donor class Gt"; the deposited chain C is an 11-residue engineered analogue,
VLEDLKSCGLF, differing from native bovine Gat1 (P04695) at four of eleven positions.
Nothing in this project checked it, and an RCSB mutation-count check returns CLEAN,
because the peptide is deposited as its own derived-peptide molecule rather than as a
mutant of Gat1. A construct audit scoped to the receptor entity cannot see it at all.

So this asks a different question: for every polymer entity that is NOT the receptor,
what is the sequence, how long is it, and how far is it from the canonical UniProt
sequence it claims to be?

    python3 partnerchain.py 4X1H 8E9Z            # named entries
    python3 partnerchain.py --panels             # every G-protein-bound panel entry

KNOWN LIMIT, read before quoting a count. `compare()` slides a fixed-length window over
the canonical sequence; it is not an alignment. On a chimera or a fusion it reports dozens
to hundreds of "substitutions" that are alignment failure, not engineering. **Only rows
with a small substitution count are trustworthy.** In the 2026-09-10 panel sweep, 358 rows
came back ENGINEERED but just 138 had <=5 substitutions; the other 220 were artifacts. Use
`<=5` as the filter, or replace compare() with a real pairwise alignment before trusting
the rest. `LONGER-THAN-CANONICAL` and `UNRESOLVED-CHECK-BY-HAND` are honest not-checked
verdicts, not passes.

Reports per entity: length, source organism, RCSB description, mapped UniProt
accession, and - where a UniProt mapping exists - whether the deposited sequence is a
contiguous substring of the canonical one (`native-fragment`) or diverges (`ENGINEERED`),
with the substitutions named. Truncation alone is not engineering; substitution is.
"""
import json, os, sys, re, urllib.request, urllib.parse, time, csv

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uniprot_cache.json")
UNI = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
RECEPTOR_HINT = re.compile(r"receptor|rhodopsin|opsin|smoothened|frizzled", re.I)


def rcsb(ids):
    out = {}
    for i in range(0, len(ids), 40):
        chunk = ids[i:i + 40]
        q = ('{entries(entry_ids:%s){rcsb_id struct{title} polymer_entities{rcsb_id '
             'entity_poly{pdbx_seq_one_letter_code_can rcsb_sample_sequence_length '
             'rcsb_mutation_count rcsb_conflict_count} '
             'rcsb_polymer_entity{pdbx_description} '
             'rcsb_entity_source_organism{scientific_name} '
             'rcsb_polymer_entity_container_identifiers{auth_asym_ids '
             'reference_sequence_identifiers{database_accession database_name}}}}}' % json.dumps(chunk))
        req = urllib.request.Request("https://data.rcsb.org/graphql",
                                     data=json.dumps({"query": q}).encode(),
                                     headers={"Content-Type": "application/json"})
        resp = json.load(urllib.request.urlopen(req, timeout=90))
        if "errors" in resp:
            raise SystemExit("RCSB GraphQL rejected the query:\n  " +
                             "\n  ".join(e.get("message", "") for e in resp["errors"]))
        for e in (resp["data"]["entries"] or []):
            out[e["rcsb_id"]] = e
        time.sleep(0.25)
    return out


def uniprot_search(desc, organism):
    """No UniProt cross-reference is NOT a clean result - it is the failure mode that let
    4X1H through. A derived peptide is deposited as its own molecule with no xref, so any
    check keyed on the xref finds nothing to compare and returns quiet. Fall back to
    resolving the accession from the description text and source organism."""
    name = re.sub(r"^.*?peptide of ", "", desc, flags=re.I).strip()
    q = f'{name} AND (organism_name:"{organism}")' if organism else name
    try:
        url = ("https://rest.uniprot.org/uniprotkb/search?format=list&size=1&query="
               + urllib.parse.quote(q))
        hit = urllib.request.urlopen(url, timeout=30).read().decode().split("\n")[0].strip()
        time.sleep(0.2)
        return hit or ""
    except Exception:
        return ""


def uniprot(acc):
    if acc not in UNI:
        try:
            txt = urllib.request.urlopen(f"https://rest.uniprot.org/uniprotkb/{acc}.fasta",
                                         timeout=30).read().decode()
            UNI[acc] = "".join(txt.split("\n")[1:])
        except Exception:
            UNI[acc] = ""
        json.dump(UNI, open(CACHE, "w"))
        time.sleep(0.2)
    return UNI[acc]


def compare(seq, canon):
    """native-fragment if the deposited sequence appears verbatim in the canonical one.
    Otherwise find the best-scoring aligned window and name the substitutions."""
    if not canon or not seq:
        return "no-reference", []
    if seq in canon:
        return "native-fragment", []
    if len(seq) > len(canon):
        # deposited chain longer than the canonical protein: a fusion or chimera, and the
        # substitution comparison below cannot be run against a single accession.
        return "LONGER-THAN-CANONICAL (fusion/chimera)", []
    best, bestdiff = None, None
    for s in range(0, len(canon) - len(seq) + 1):
        w = canon[s:s + len(seq)]
        d = [(k + 1, a, b) for k, (a, b) in enumerate(zip(w, seq)) if a != b]
        if bestdiff is None or len(d) < len(bestdiff):
            best, bestdiff = s, d
            if not d:
                break
    return ("ENGINEERED" if bestdiff else "native-fragment"), (bestdiff or [])


def check(ids):
    data = rcsb(ids)
    rows = []
    for pdb in ids:
        e = data.get(pdb.upper())
        if not e:
            print(f"{pdb}: NOT IN RCSB"); continue
        for ent in e["polymer_entities"]:
            desc = (ent["rcsb_polymer_entity"] or {}).get("pdbx_description") or ""
            if RECEPTOR_HINT.search(desc):
                continue                                    # receptor entity: out of scope
            ep = ent["entity_poly"]; seq = ep["pdbx_seq_one_letter_code_can"] or ""
            ci = ent["rcsb_polymer_entity_container_identifiers"]
            accs = [r["database_accession"] for r in (ci.get("reference_sequence_identifiers") or [])
                    if r.get("database_name") == "UniProt"]
            acc = accs[0] if accs else ""
            resolved_by = "xref"
            if not acc:
                org = (ent.get("rcsb_entity_source_organism") or [{}])[0].get("scientific_name", "")
                acc, resolved_by = uniprot_search(desc, org), "name-search"
            if acc:
                verdict, diffs = compare(seq, uniprot(acc))
            else:
                verdict, diffs = "UNRESOLVED-CHECK-BY-HAND", []
            rows.append(dict(pdb=pdb.upper(), chains=",".join(ci.get("auth_asym_ids") or []),
                             length=ep["rcsb_sample_sequence_length"], desc=desc,
                             organism=(ent.get("rcsb_entity_source_organism") or [{}])[0].get("scientific_name", ""),
                             uniprot=acc, uniprot_resolved_by=(resolved_by if acc else ""),
                             rcsb_mutation_count=ep.get("rcsb_mutation_count"),
                             verdict=verdict,
                             substitutions=";".join(f"{a}{i}{b}" for i, a, b in diffs), sequence=seq))
    return rows


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--panels" in sys.argv:
        P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "panels", "panels.csv")
        args = sorted({r["pdb_id"] for r in csv.DictReader(open(P))
                       if r["partner_type"] == "G protein" and r["pdb_id"]})
    rows = check(args)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "partnerchain_report.csv")
    if rows:
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    eng = [r for r in rows if r["verdict"] == "ENGINEERED"]
    unres = [r for r in rows if r["verdict"] == "UNRESOLVED-CHECK-BY-HAND"]
    print(f"\nnon-receptor entities checked: {len(rows)} across {len(args)} entries")
    print(f"  ENGINEERED (substitutions vs UniProt): {len(eng)}")
    print(f"  of those, RCSB pdbx_mutation_count == 0 (invisible to a mutation check): "
          f"{sum(1 for r in eng if not r['rcsb_mutation_count'])}")
    print(f"  UNRESOLVED, needs a human: {len(unres)}")
    print(f"  wrote {out}")
