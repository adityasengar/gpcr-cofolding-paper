# BC-3 — prospective ligand-class discrimination, on two backbones of four

**Claim**: SC-C-4. **Partly buildable**: `04_classifier/g1_bootstrap_s1_auroc.json`
ships the intervals and the permutation null, so the summary panel can be drawn.
The per-receptor LORO fold results cannot.

## Encoding

AUROC per backbone with the cluster-bootstrap interval and the permutation null
band. 0.5 drawn as the chance line.

| backbone | AUROC | cluster-boot 95% CI | permutation null | scoped in |
|---|---:|---|---|---|
| Boltz-2 | 0.852 | [0.560, 0.974] | [0.477, 0.520] | yes |
| Protenix2 | 0.825 | [0.528, 0.960] | [0.469, 0.527] | yes |
| Chai-1 | 0.706 | [0.351, 0.941] | [0.473, 0.523] | no |
| OpenFold3 | 0.656 | [0.382, 0.924] | [0.467, 0.525] | no |

n = 15 receptors, self-reference-excluded.

## Required on the panel

- Chai-1 and OpenFold3 are **inconclusive, not negative**. Their intervals span
  0.5, which means the test cannot distinguish them from chance -- a different
  statement from showing they carry no signal, and the panel must not let the
  two be confused.
- Draw the permutation null. Both scoped backbones exclude it, and that is a
  stronger statement than clearing 0.5.
- Boltz-2's bootstrap **median is 0.809**, below its 0.852 point estimate. If a
  single number leaves this panel for an abstract, it should be the interval.
- n = 15, not 23 and not 36. The three counts are different inclusion rules and
  the panel states its own.
