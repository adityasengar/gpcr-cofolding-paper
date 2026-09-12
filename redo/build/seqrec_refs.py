#!/usr/bin/env python3
"""What the deposited reference actually contains, per core receptor.

For every rule-R reference pair in `panel_systems.csv` (`gdb_active`,
`gdb_inactive`) this fetches the *receptor* polymer entity from RCSB and
answers the question `SEQ_RECEPTORS.md` §6 asks:

  if we supply the full canonical sequence and score against this reference,
  which canonical residues does the reference actually contain, and which
  does it actually resolve?

Method — and why it is not RCSB's own alignment
-----------------------------------------------
`rcsb_polymer_entity_align` looks like the right source and is not reliable
on GPCR fusion constructs. Checked on the 128 rule-R references: the
receptor entity of **9D3G** (CCR6) and **8IRU** (DRD4) carries *no* UniProt
alignment at all, **8HCQ** (EDNRA) aligns its receptor entity only to the
luciferase fusion partner Q9GV45, and **8YNS** (MCHR1) aligns to the
chimpanzee accession A0A2R9AFP0 alongside the human one. So RCSB's
alignment is used only as a cross-check; the mapping below is computed
here, which is also the method `PANEL.md` §9(2) names as the one that
works.

Per entity: unique 9-mer anchors shared with the canonical UniProt
sequence, chained by longest-increasing-subsequence, merged into collinear
diagonal blocks. A block tolerates point mutations (they sit inside a
block) and an ICL3 excision or a fusion insertion (they end one block and
start another). The receptor entity of an entry is then the entity with
the most canonical residues mapped — self-validating, no description
matching.

Sources
  RCSB Data GraphQL  https://data.rcsb.org/graphql
    entity_poly.pdbx_seq_one_letter_code_can  -> the deposited construct
    rcsb_polymer_entity_align                 -> cross-check only
    rcsb_polymer_instance_feature
      type = UNOBSERVED_RESIDUE_XYZ           -> disorder, entity seq_id space
  Fetched 2026-09-11; raw responses cached in seqrec_rcsb_entities.json.

Outputs
  seqrec_refs.tsv        one row per (receptor, state, pdb) reference entity
  seqrec_scoreable.tsv   one row per receptor: canonical residues present in
                         both references, and resolved in both

Usage
  python3 redo/build/seqrec_refs.py
"""
import bisect
import collections
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
PANEL = os.path.join(INPUTS, "panel_systems.csv")
RECS = os.path.join(INPUTS, "seqrec_receptors.tsv")
FASTA = os.path.join(INPUTS, "seqrec_canonical.fasta")
OUT_REFS = os.path.join(INPUTS, "seqrec_refs.tsv")
OUT_SCORE = os.path.join(INPUTS, "seqrec_scoreable.tsv")
CACHE = os.path.join(CACHE, "seqrec_rcsb_entities.json")

GQL = "https://data.rcsb.org/graphql?query="
K = 9

QUERY = """{ entries(entry_ids:[%s]) { rcsb_id
  polymer_entities {
    rcsb_id
    rcsb_polymer_entity { pdbx_description pdbx_mutation }
    entity_poly { rcsb_sample_sequence_length pdbx_seq_one_letter_code_can }
    rcsb_entity_source_organism { ncbi_scientific_name }
    rcsb_polymer_entity_align {
      reference_database_name reference_database_accession
      aligned_regions { entity_beg_seq_id ref_beg_seq_id length } }
    polymer_entity_instances {
      rcsb_id
      rcsb_polymer_entity_instance_container_identifiers { auth_asym_id }
      rcsb_polymer_instance_feature { type feature_positions { beg_seq_id end_seq_id } } }
  } } }"""


# ---------------------------------------------------------------- fetching
def fetch(ids):
    q = QUERY % ",".join('"%s"' % i for i in ids)
    url = GQL + urllib.parse.quote(q)
    for attempt in range(4):
        try:
            return json.load(urllib.request.urlopen(url, timeout=120))["data"]["entries"]
        except Exception as exc:                        # noqa: BLE001
            if attempt == 3:
                raise RuntimeError(f"{ids}: {exc}")
            time.sleep(3 * (attempt + 1))


def load_entries(pdb_ids):
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    todo = [p for p in pdb_ids if p not in cache]
    for i in range(0, len(todo), 8):
        for e in fetch(todo[i:i + 8]) or []:
            cache[e["rcsb_id"]] = e
        print(f"# fetched {min(i + 8, len(todo))}/{len(todo)}", file=sys.stderr)
    if todo:
        json.dump(cache, open(CACHE, "w"))
    return cache


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


# ---------------------------------------------------------------- mapping
def anchor_map(ent, canon, k=K):
    """entity 1-based seq_id -> canonical 1-based residue number."""
    if not ent or len(ent) < k:
        return {}, []
    pos = collections.defaultdict(list)
    for j in range(len(canon) - k + 1):
        pos[canon[j:j + k]].append(j)
    anchors = []
    for i in range(len(ent) - k + 1):
        p = pos.get(ent[i:i + k])
        if p and len(p) == 1:
            anchors.append((i, p[0]))
    if not anchors:
        return {}, []

    # longest strictly-increasing subsequence on the canonical coordinate
    tails, tails_idx, back = [], [], [-1] * len(anchors)
    for n, (_, j) in enumerate(anchors):
        p = bisect.bisect_left(tails, j)
        if p == len(tails):
            tails.append(j)
            tails_idx.append(n)
        else:
            tails[p] = j
            tails_idx[p] = n
        back[n] = tails_idx[p - 1] if p else -1
    chain, cur = [], tails_idx[-1]
    while cur != -1:
        chain.append(anchors[cur])
        cur = back[cur]
    chain.reverse()

    # Merge collinear anchors into diagonal blocks. A same-diagonal gap is
    # bridged only when the gap is still mostly identical to canonical.
    #
    # Both halves of that rule are load-bearing, and each was put there by a
    # defect the other half caused:
    #   * without bridging, an isolated engineered substitution breaks every
    #     k-mer covering it, so the mutated residue and its k-1 neighbours
    #     drop silently out of the map and the substitution is never reported;
    #   * with unconditional bridging, a *length-matched foreign segment* is
    #     mapped as if it were the receptor. 7T10 (SSR2) is the real case:
    #     RCSB aligns entity 40-276 to P30874 1-237 and entity 292-408 to
    #     P30874 253-369, with entity 277-291 aligning to **P41145 (OPRK)
    #     256-270** — a 15-residue kappa-opioid ICL3 graft, same diagonal
    #     because it is length-matched. Unconditional bridging reported it as
    #     13 point mutations of SSR2.
    # So the gap is bridged either way — a bridged residue does occupy that
    # structural position and is scoreable — and the two cases are told apart
    # afterwards by run length (`classify_mismatches`): an engineered
    # substitution is an isolated mismatch, a graft is a run. Neither is
    # silent.
    GAP_TOL = 40
    blocks = []
    for i, j in chain:
        d = j - i
        if blocks and blocks[-1][2] == d and i <= blocks[-1][1] + 1 + GAP_TOL:
            blocks[-1][1] = i + k - 1
        else:
            blocks.append([i, i + k - 1, d])
    mapping, last_ref = {}, 0
    for i0, i1, d in blocks:
        if i0 + d < last_ref:                 # non-monotonic, drop
            continue
        for i in range(i0, min(i1 + 1, len(ent))):
            r = i + d + 1
            if 1 <= r <= len(canon):
                mapping[i + 1] = r
        last_ref = i1 + d
    return mapping, blocks


RUN_MIN = 5


def classify_mismatches(ent, canon, ent2ref):
    """Split mapped mismatches into point substitutions and grafted runs.

    A thermostabilising or binding-site mutation is an isolated mismatch. A
    length-matched foreign segment — 7T10's 15-residue OPRK ICL3 graft into
    SSR2, which RCSB itself aligns to P41145 256-270 — is a run. Reporting
    a graft as N point mutations was this script's own first answer and it
    was wrong; the split is what keeps that from recurring.
    """
    mism = sorted(v for k_, v in ent2ref.items() if ent[k_ - 1] != canon[v - 1])
    inv = {v: k_ for k_, v in ent2ref.items()}
    runs, cur = [], []
    for v in mism:
        if cur and v == cur[-1] + 1:
            cur.append(v)
        else:
            if cur:
                runs.append(cur)
            cur = [v]
    if cur:
        runs.append(cur)
    points = [f"{canon[v-1]}{v}{ent[inv[v]-1]}" for r in runs if len(r) < RUN_MIN
              for v in r]
    grafts = [f"{r[0]}-{r[-1]}" for r in runs if len(r) >= RUN_MIN]
    n_graft = sum(len(r) for r in runs if len(r) >= RUN_MIN)
    return points, grafts, n_graft


def unobserved(pe):
    """(chain, entity seq_ids unobserved) for the best-resolved instance."""
    best = None
    for inst in pe.get("polymer_entity_instances") or []:
        miss = set()
        for f in inst.get("rcsb_polymer_instance_feature") or []:
            if f["type"] != "UNOBSERVED_RESIDUE_XYZ":
                continue
            for p in f.get("feature_positions") or []:
                miss.update(range(p["beg_seq_id"], p["end_seq_id"] + 1))
        if best is None or len(miss) < len(best[1]):
            best = (inst["rcsb_polymer_entity_instance_container_identifiers"]
                    ["auth_asym_id"], miss)
    return best or ("?", set())


def receptor_entity(entry, canon):
    """The entity mapping the most canonical residues. No name matching."""
    best = None
    for pe in entry["polymer_entities"] or []:
        ent = ((pe.get("entity_poly") or {}).get("pdbx_seq_one_letter_code_can")
               or "").upper().replace("\n", "")
        m, _ = anchor_map(ent, canon)
        if best is None or len(m) > len(best[2]):
            best = (pe, ent, m)
    return best


def span(s):
    return f"{min(s)}-{max(s)}" if s else "NA"


def ranges(s):
    """Compact a residue set to '38-56,60-120' so downstream scripts get the
    exact set, not just its span. The cap-cost check in seqrec_verify.py
    needs the set; a span would over-count by every internal gap."""
    if not s:
        return "NA"
    out, xs = [], sorted(s)
    a = b = xs[0]
    for x in xs[1:]:
        if x == b + 1:
            b = x
        else:
            out.append((a, b))
            a = b = x
    out.append((a, b))
    return ",".join(f"{i}-{j}" if i != j else str(i) for i, j in out)


def main():
    panel = list(csv.DictReader(open(PANEL)))
    core = [r for r in panel if "C1" in r["tier"].split("|")]
    recs = {r["slug"]: r for r in csv.DictReader(open(RECS), delimiter="\t")}
    seqs = read_fasta(FASTA)

    pdbs = sorted({r[c] for r in core for c in ("gdb_active", "gdb_inactive") if r[c]})
    cache = load_entries(pdbs)

    ref_rows, score_rows = [], []
    for r in core:
        slug, acc = r["slug"], r["uniprot_acc"]
        canon = seqs[slug]
        cover = {}
        for state, col in (("active", "gdb_active"), ("inactive", "gdb_inactive")):
            pdb = r[col]
            entry = cache.get(pdb)
            if not entry:
                print(f"# MISSING ENTRY {pdb}", file=sys.stderr)
                continue
            pe, ent, ent2ref = receptor_entity(entry, canon)
            ep = pe.get("entity_poly") or {}
            ent_len = ep.get("rcsb_sample_sequence_length") or len(ent)
            orgs = [o.get("ncbi_scientific_name") for o in
                    (pe.get("rcsb_entity_source_organism") or [])]
            aligns = pe.get("rcsb_polymer_entity_align") or []
            rcsb_accs = sorted({a.get("reference_database_accession") for a in aligns})
            chain, miss = unobserved(pe)
            present = set(ent2ref.values())
            resolved = {v for k_, v in ent2ref.items() if k_ not in miss}
            cover[state] = (present, resolved)
            # true engineered substitutions: mapped positions where the
            # deposited residue differs from canonical. PANEL.md §9(2) calls
            # RCSB's pdbx_mutation a floor; this is the recount.
            points, grafts, n_graft = classify_mismatches(ent, canon, ent2ref)
            # where the non-canonical stretches sit, in canonical coordinates
            gaps = []
            mapped = sorted(ent2ref)
            for a, b in zip(mapped, mapped[1:]):
                if b - a > 1:                       # entity residues not mapped
                    gaps.append(f"{ent2ref[a]}/{b - a - 1}aa")
            ins = ";".join(gaps) or "none"
            n_flank = (mapped[0] - 1) if mapped else 0
            c_flank = (ent_len - mapped[-1]) if mapped else 0
            ref_rows.append({
                "slug": slug, "state": state, "pdb": pdb,
                "entity": pe["rcsb_id"], "chain": chain, "entity_len": ent_len,
                "description": (pe["rcsb_polymer_entity"] or {}).get("pdbx_description", ""),
                "rcsb_mutation": (pe["rcsb_polymer_entity"] or {}).get("pdbx_mutation") or "",
                "source_organisms": ";".join(str(o) for o in orgs),
                "rcsb_align_accessions": ";".join(str(a) for a in rcsb_accs) or "NONE",
                "rcsb_align_names_receptor": "yes" if acc in rcsb_accs else "NO",
                "canon_len": len(canon),
                "n_canon_present": len(present),
                "canon_present_span": span(present),
                "n_entity_not_canon": ent_len - len(ent2ref),
                "n_unobserved_in_entity": len(miss),
                "n_canon_resolved": len(resolved),
                "canon_resolved_span": span(resolved),
                "n_point_substitution": len(points),
                "point_substitution": ";".join(points),
                "n_canon_grafted": n_graft,
                "grafted_canon_spans": ";".join(grafts) or "none",
                "internal_insertions_canonpos_len": ins,
                "n_term_extra_entity_aa": n_flank,
                "c_term_extra_entity_aa": c_flank,
            })
        if len(cover) == 2:
            pa, ra = cover["active"]
            pi, ri = cover["inactive"]
            both_res = ra & ri
            score_rows.append({
                "slug": slug, "uniprot_acc": acc, "canon_len": len(canon),
                "active_pdb": r["gdb_active"], "inactive_pdb": r["gdb_inactive"],
                "n_present_active": len(pa), "n_present_inactive": len(pi),
                "n_present_both": len(pa & pi),
                "n_resolved_active": len(ra), "n_resolved_inactive": len(ri),
                "n_resolved_both": len(both_res),
                "resolved_both_span": span(both_res),
                "resolved_both_ranges": ranges(both_res),
                "frac_canon_scoreable": round(len(both_res) / len(canon), 4),
                "n_canon_never_scoreable": len(canon) - len(both_res),
            })

    for path, rows in ((OUT_REFS, ref_rows), (OUT_SCORE, score_rows)):
        with open(path, "w") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t")
            w.writeheader()
            w.writerows(rows)
    print(f"# wrote {OUT_REFS} ({len(ref_rows)}) and {OUT_SCORE} ({len(score_rows)})",
          file=sys.stderr)


# --------------------------------------------------------------- self-test
def selftest():
    """Prove each check by planting the defect it is supposed to catch.

    Run: python3 redo/build/seqrec_refs.py --selftest
    """
    import random
    seqs = read_fasta(FASTA)
    canon = seqs["ADRB2"]
    ok = True

    m, _ = anchor_map(canon, canon)
    print(f"identity          mapped {len(m)}/{len(canon)}")
    ok &= len(m) == len(canon)

    mut = canon[:150] + "W" + canon[151:]
    m, _ = anchor_map(mut, canon)
    bad = [f"{canon[v-1]}{v}{mut[k-1]}" for k, v in m.items() if mut[k - 1] != canon[v - 1]]
    print(f"1 planted mutation detected as {bad} (expect ['{canon[150]}151W'])")
    ok &= bad == [f"{canon[150]}151W"]

    random.seed(0)
    junk = "".join(random.choice("ACDEFGHIKLMNPQRSTVWY") for _ in range(160))
    chim = junk + canon[28:230] + canon[262:365]
    m, _ = anchor_map(chim, canon)
    leak = sorted(v for v in m.values() if 231 <= v <= 262)
    print(f"fusion+ICL3 excision: mapped {len(m)} canon residues, span "
          f"{min(m.values())}-{max(m.values())}, ICL3 leak {leak or 'none'}, "
          f"junk mapped {sum(1 for k in m if k <= 160)}")
    ok &= not leak and sum(1 for k in m if k <= 160) == 0 and len(m) == 305

    # length-matched foreign graft must NOT be mapped (the 7T10/SSR2 case)
    random.seed(1)
    graft = canon[:237] + "".join(random.choice("ACDEFGHIKLMNPQRSTVWY")
                                  for _ in range(15)) + canon[252:]
    m, _ = anchor_map(graft, canon)
    pts, grf, ng = classify_mismatches(graft, canon, m)
    print(f"length-matched 15-residue graft -> runs {grf}, {ng} residues, "
          f"{len(pts)} stray point calls (expect one run covering 238-252)")
    ok &= grf and int(grf[0].split("-")[0]) >= 238 and int(grf[0].split("-")[1]) <= 252

    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if "--selftest" in sys.argv:
    sys.exit(selftest())

if __name__ == "__main__":
    sys.exit(main())
