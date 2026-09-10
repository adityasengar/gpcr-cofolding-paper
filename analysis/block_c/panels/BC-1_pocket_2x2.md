# BC-1 — agonist and antagonist pockets separate, in the apo arm alone

**Claim**: SC-C-1. **Not buildable from this bundle** — needs `rows.tier3.v2.csv`
for per-receptor points. The summary values below are shipped and correct; what
is missing is the 23 per-receptor values behind each mean.

## Encoding

Per backbone, the 2x2 interaction (agonist minus antagonist, of the difference
between pocket-Ca RMSD to active and to inactive reference), with the
cluster-bootstrap interval. Zero drawn. Every interval falls left of it.

| backbone | interaction (A) | cluster-boot 95% CI | receptor-boot (secondary) |
|---|---:|---|---|
| Boltz-2 | -0.306 | [-0.454, -0.164] | [-0.431, -0.192] |
| Chai-1 | -0.137 | [-0.216, -0.045] | [-0.223, -0.055] |
| OpenFold3 | -0.252 | [-0.405, -0.099] | [-0.384, -0.129] |
| Protenix2 | -0.184 | [-0.277, -0.088] | [-0.271, -0.101] |

n = 23 receptors, resampled as **16 paralog clusters**, 5,000 iterations,
seed 1234.

## Required on the panel

- **APO ARM ONLY**, stated on the panel and not left to the caption. The scope
  is what makes the result about the ligand rather than about the partner.
- Chai-1's upper bound is **-0.045**: signed by a narrow margin, and the panel
  should not let a reader miss that.
- The cluster interval is primary; if the receptor interval is drawn at all it
  is drawn thinner and labelled secondary.

## When the rows arrive

Add the 23 per-receptor values as points behind each interval. A four-value
summary of a 23-receptor mean is exactly the shape of panel this project has
twice found to be hiding a bimodal population.
