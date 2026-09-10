# ASSUMED-NOT-VERIFIED — E1 to E4 follow-up

Items on which the E1..E4 dispatch demands verification that this pass
did not accomplish. Recorded so future readers can distinguish "claim
based on verified data" from "claim resting on plausible-looking
proxies".

## E1 external-ruler enumeration is a subset of the deposited record

**Status**: CLOSED 2026-09-10 by Item 1 of the closeout dispatch. The
"zero native Class A Gs Ga-complexed structures" finding turned out to
be a CURATION CHOICE, not a property of the deposited record. **ADRB2**
in the curated set is `pdb=4LDE, asrc=nanobody`; the canonical native
β2AR-Gs heterotrimer **3SN6** (deposited 2011, well before any
backbone's training cutoff) exists in the PDB and was not selected.
The Discussion framing "the deposited record contains no native Class
A Gs complexes" is downgraded to a Methods sentence: "the campaign's
curated reference set contains no native Class A Gs heterotrimer;
candidates exist in the PDB and were not selected." The claim about
the deposited PDB as a whole is not supported by this pass.

**Bin-classification note** (Item 1b): the campaign's schema has bins
`{native, mini_G, chimera, nanobody, agonist_only, DVL_DEP}`. No
explicit dominant-negative-Gαs (DNGαs) bin. Since DNGαs entries carry
wild-type α5-CT sequence, they should fall under `native` by
convention, but the campaign's Class A × Gs × native subset is empty,
so either no DNGαs entries were curated or they were binned elsewhere.
The distinction between wild-type Gαs and DNGαs is not captured in the
current schema; a fresh dispatch would need to inspect construct
strings PDB-by-PDB.

**What was actually done in the E1 pass**: enumerated the campaign's
curated reference set (`refs/reference_set.blockb_pinned.csv` +
`refs/sealed_active_refs_2026_09_01.csv`), which contains one active
reference per campaign-panel receptor. 103 total active rows across
Block A + Block B panel receptors. After Class A + Gα-complexed
filters, 45 structures remained.

**What was NOT done**: a comprehensive query against GPCRdb's own
database for every Class A + Gα-complexed active-state PDB. Item 1
retires the specific "zero natives" claim; the broader "the curated
set is a subset of GPCRdb" observation stands and remains an
honest-instrument-limitation flag in the Methods paragraph.

## Method + resolution not recorded for reference structures

**Claim in dispatch**: "Record: PDB ID, receptor, Ga family, alpha5
donor class (native / mini_G / chimera), method, resolution."

**What was actually done**: PDB ID, receptor, family, α5 donor class,
`active_stabilization_source`, `stabilising_elements`, `construct`
recorded in `external_ruler.csv`. Method and resolution are NOT
columns in the current `reference_set.blockb_pinned.csv` schema; they
would need to be pulled from RCSB per PDB ID via API.

**Consequence**: E1's audit table columns for method and resolution
are empty in `external_ruler.csv`. If they are load-bearing for a
manuscript sentence, a fresh dispatch with RCSB fetches populates
them. Twenty spot-checks against RCSB would be sufficient to
characterise the distribution.

## Class A / Class B / Class F assignment inferred from Block A's PREREG

**Claim in dispatch**: "Class A receptor" filter.

**What was actually done**: filtered out the 4 Class B receptors
{CRHR1, GCGR, GLP1R, PTH1R} and 4 Class F receptors {FZD4, FZD6, FZD7,
SMO} named in Block A's PREREG §1 v2. Every other receptor treated
as Class A.

**What was not done**: a per-receptor GPCRdb class lookup on the
receptors beyond the 48-receptor Block A panel. Some campaign-curated
active refs are for receptors not in the Block A panel (e.g., BRS3,
CALCR, NK1R, S1PR1, etc.); these are Class A by default assumption in
this pass, but a GPCRdb class check would be more defensible.

**Consequence**: if any receptor in the ruler set is actually Class B
or Class F but not on Block A's exclusion list, the tilt values may
not be biologically comparable. Approximately 45 receptors are in the
ruler set beyond the 48-panel; each is defaulted-Class-A. Low prior
risk (Class B is a small set; Class F is smaller), but not verified.

## Family assignment for `alpha5_donor_class=""` uses cognate coupling

**Claim in dispatch**: "Ga family resolvable (Gs, Gi/o, Gq/11, G12/13)".

**What was actually done**: for structures where `alpha5_donor_class`
is empty (typical for native asrc), family = the receptor's cognate
Gα family from `refs/gpcr_coupling.csv`. This assumes native active
complexes were determined with the receptor's cognate transducer —
which is the standard experimental design, but not verified
per-structure.

**What was not done**: per-PDB inspection to confirm the α-subunit
family in the deposited complex matches the receptor's canonical
cognate.

**Consequence**: rare cases (e.g., a receptor solved in complex with a
non-cognate Gα) would be miscoded. Low prior; the biology of the field
is such that native Class A active complexes are almost always
cognate-Gα.

## Bootstrap unit is receptor, not structure — the dispatch's caution

**Claim in dispatch**: "Bootstrap unit is the RECEPTOR, not the
structure — multiple PDBs of one receptor are not independent."

**What was actually done**: receptor-level bootstrap. Because the
campaign's curated set has one active reference per receptor, the
bootstrap unit coincides with structure count in this specific
computation. The dispatch's caution is honoured, but the caution
becomes distinguishable only under a full GPCRdb enumeration where
some receptors have multiple entries.

**Consequence**: this is a non-issue for the campaign set. It becomes
a real design choice under the deferred full-GPCRdb enumeration
mentioned above.
