# C-B-12 — Empty manifest generator SHAs; compensating control by content

## Caveat

`experiments/019_block_b_partner_selection/manifest/manifest.provenance.json`
carries two empty strings:

- `propose_py_git_sha = ""`
- `build_manifest_py_git_sha = ""`

These are the code that produced the decoy scrambles and shuffled-partner
assignments — load-bearing files for Phase 1b (decoy) and Phase 1c
(shuffled). The manifest emitter did not stamp its own emitter git SHAs.

## Compensating control

**Construct identity is verified by content in Phase 1b/1c**, not by
generator version. Every decoy and shuffled construct is checked against:

- Byte-identical prefix vs cognate up to the α5-CT tail (Phase 1b).
- Hamming distance within the α5-CT tail (Phase 1b; median 9.5, range 7–11).
- Length parity between decoy and cognate parent (Phase 1b; 40/40).
- Parent-Gα routing against `refs/gpcr_coupling.csv:primary_ga_identity`
  including edge cases OPSD → alphat and EDNRA → alphaq (Phase 1b, 1c;
  40/40).
- Non-cognate-family Gα strictly outside `{cognate_class} ∪
  {secondary_classes}` for shuffled (Phase 1c; 40/40).

**Content verification supersedes generator provenance for these files
on this corpus.**

## Why it matters

The exact proposal-generator revision is not cryptographically recoverable
from the sidecar. That would matter if the constructs' content was in
doubt, but the sequence-hash verification is stronger evidence than a
git-sha stamp would be (identical constructs from any generator version
produce identical hashes). Recorded as caveat, not blocker.

## Affects

- SC-B-8 (construct identity verified by hash).

## Manuscript sentence

> The Block B manifest sidecar carries empty `propose_py_git_sha` and
> `build_manifest_py_git_sha` fields — the manifest builder did not
> stamp its own emitter code identity. Construct identity is verified
> by content (byte-identical prefix, α5-CT tail Hamming, length parity,
> parent-Gα routing) on all 40 receptors × 2 arms in Phase 1b/1c.
> Content verification is stronger than a git-sha stamp for the
> constructs themselves; the empty SHA fields are recorded as a
> reproducibility caveat, not as evidence of construct-identity
> uncertainty.

## Related

- MANUSCRIPT_FLAGS.md Flag B-21.
- Phase 0 addendum §Item 2, Phase 1 §1b–§1c.
