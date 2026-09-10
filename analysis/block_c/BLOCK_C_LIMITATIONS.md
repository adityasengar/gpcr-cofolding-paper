# Block C — limitations

Drawn from `02_caveats/`. **Distinct from `03_withdrawals/`**: a caveat is a live
limitation on a claim we are making; a withdrawal is a claim we retracted. Ten
were withdrawn across five audit rounds and they are not repeated here.

## Limitations that bound what Block C can claim

**The activation predicate does not work on this panel** (C-C-1). Floor-pinned in
apo, ceiling-pinned in cognate, ~65% of cells unresolvable. Every Block C result
is on continuous pocket-Cα geometry, and no Block C number is comparable with a
Block A or Block B predicate rate.

**Chai-1 is the softest backbone here, as elsewhere** (C-C-2). Its 2×2 interval
reaches within 0.045 Å of zero; its classifier interval spans 0.5; its far-mode
ligand tail is 175 of the 176 rows beyond 60 Å in the whole corpus. Three
separate weaknesses, one backbone.

**The classifier rests on 15 receptors** (C-C-5), not the 23 of the 2×2 or the 36
of the panel. Self-reference exclusion is what removes the rest. The three counts
are different inclusion rules on the same campaign and are not reconciled into
one number.

**Coverage is asymmetric** (C-C-8). The antagonist arm is ~93% covered; agonist
and decoy arms are ~50% NaN. Any pooled pose statistic inherits that asymmetry.

**Reference routing collapses** (C-C-10). Routing labels differ by ligand role
but resolve to the same PDB per receptor. This is what makes reference-identity
leakage impossible by construction — and it also means a target reference may
not carry the same ligand class as the input row.

**Four receptors did not land** (C-C-9), two on species mismatch and two because
their inactive reference carries an allosteric rather than orthosteric
antagonist. Systematic, not random.

**AGTR1 is a curation-scope case, not a model failure** (C-C-4). Its active
reference is stabilised by a β-arrestin-biased agonist and a
biased-state-selective nanobody, with no Gα and no Gβγ — unique among the 15.

**CXCR4's apo pocket reference** is a known scope limit (C-C-7).

**The matcher path affects `ligand_rmsd_to_ref` only** (C-C-6), not pocket-Cα, so
it bounds the pose result and not the 2×2 or the classifier.

**Deferred gates remain open** (C-C-11), including the absence of a functional
rebuild-and-diff harness. Integrity was checked by SHA; reproduction was not
demonstrated.

## Limitations we found rather than inherited

**Most of this block cannot be independently verified.** Two source corpora were
not delivered. 30 of our 53 checks compare shipped summaries to one another
rather than recomputing from rows, and both surviving positives fall in that
group. See `DISCREPANCY_REPORT.md` D-C-1 and D-C-2.

**The applicability domain was refuted, not established** (SC-C-5). Stated in the
Results as a failure of a pre-registered hypothesis, because a reader who meets
an empirical failure list without that framing will assume it is predictive.
