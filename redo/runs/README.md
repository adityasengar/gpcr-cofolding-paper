# runs/ — the delivery contract

**DRAFT — not yet agreed with `paper_af3`.** This is the shape we propose to ask
for, before the first run exists. It is the cheapest moment it will ever be.

## Why specify this in advance

Blocks A–D each arrived shaped however the pipeline chose. Each one then needed
its own bespoke verifier — **63, 116, 69 and 54 checks** — its own discrepancy
report, and Block C named 66 files it never shipped. We paid that four times
because the shape was settled *after* the data existed.

These runs do not exist yet. One row format, agreed now, means one verifier
serves every run forever and any two runs concatenate directly. It also kills
the failure that cost us an entire export: two campaigns mixed together, because
"which campaign is this from?" was answerable only from a folder name.

## One directory per run

```
runs/<YYYY-MM-DD>_<group>_<slug>/
    manifest.json     what was run, against which inputs, by whom
    rows.csv          one row per prediction — never per receptor, never pooled
    README.md         anything the manifest cannot say
```

Date-prefixed so it sorts chronologically and needs no registry to allocate.
**Read-only once landed** — the rule that already works for `data/block_a/`.

## manifest.json

```json
{
  "run_id":        "2026-09-20_g1_ladder_boltz",
  "group":         "G1",
  "spec":          "redo/spec/GROUP1_SYSTEMS.md",
  "input_sha256":  ["<sha256 of each redo/inputs/ file actually consumed>"],
  "backbone":      {"name": "boltz2", "version": "...", "commit": "..."},
  "msa":           {"receptor": "...", "partner": "...", "paired": true},
  "n_predictions": 0,
  "produced_at":   "2026-09-20T00:00:00Z",
  "produced_by":   "paper_af3"
}
```

`input_sha256` is the load-bearing field. Check **L6** refuses a run whose
declared inputs are not ones we hold, so a run against a stale or hand-altered
input set cannot land quietly.

## rows.csv

One row per prediction. The identity columns are the same in every group, so
every run is directly concatenable:

```
run_id, group, receptor, backbone, arm, rung, seed, sample
```

then the measured axes, then confidence. **No self-certifying column** — Block A
shipped a `matches_claim_sheet` field that read `True` where the value
disagreed, and nothing that vouches for itself is accepted here.

## Open, and for Aditya

The exact measured-axis columns wait on `paper_af3`'s §2 blueprint — asking for
a column they do not produce costs more credibility than it buys. This document
goes to them **with** the frozen `inputs/` set, as one contract, not before.
