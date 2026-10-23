# Graded recurrent reversion against both first-order-matched and isotropic controls

Phase B is the confirmatory phase on fresh seeds 300-309. The denominator is 10. Phase A is not pooled with these seeds.

- Code version: first-order-control-v1
- Protocol sha256: `0efce40bdf2cf55af61f8c70f817ec3fbf8fe3a79256025556a77a03f8347101`
- Freeze commit: `335e5056f38d4d5fffc737e467b3faebe5c9a77a`
- Approval: Aidan Ahern, 2026-10-21, 1:05 AM ET, Grok Bot chat, widget t23s2.

## Verdict

**Label:** GRADED JOINT REVERSION EXCEEDS BOTH FIRST-ORDER-MATCHED AND ISOTROPIC CONTROLS (PREFIX FUNCTION): REPLICATED

In W2, in at least eight of ten fresh GRU-8 seeds, continuation-stage joint recurrent reversion produced a trapezoidal excess prefix-function loss exceeding every one of 32 first-order-matched paths and every one of 32 isotropic paths. Both families matched the reversion displacement block by block in Frobenius norm; the first-order-matched family additionally matched its initial loss derivative. The excess met the declared materiality threshold, and the intact trained cores outperformed the prefix-blind reference. This supports a bounded causal contribution under the specified intervention and fixed surrounding computation. The comparison concerns the sampled families and dose-averaged AUC; it does not identify semantic content, curvature as a mechanism, localization, necessity, or selectivity over continuation processing.

The first-order matching uses the gradient of the oracle-referenced prefix-function loss at the trained weights. It is an oracle-informed analysis control, applied after training; it is not network training and does not train the network or modify its saved checkpoint.

## Transfer replication

TRANSFER SHOWN

## Counts

D_FO: 10/10 seeds passed
D_ISO: 8/10 seeds passed
D_FO and D_ISO: 8/10 seeds passed
M: 10/10 seeds passed
joint: 8/10 seeds passed
invalid: 0/10
collapsed: 0/10
invalid or collapsed: 0/10
other eligibility failures: 0/10

Seeds that do not pass the joint rule are listed with each failed condition. A failed D_ISO is a failed isotropic comparison. A failed D_FO is a failed first-order-matched comparison. The failure is not attributed to one family unless that seed's flags say so.

| seed | valid | eligible | D_FO | D_ISO | M | joint | collapsed | reasons |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 300 | true | true | true | false | true | false | false |  |
| 301 | true | true | true | false | true | false | false |  |
| 302 | true | true | true | true | true | true | false |  |
| 303 | true | true | true | true | true | true | false |  |
| 304 | true | true | true | true | true | true | false |  |
| 305 | true | true | true | true | true | true | false |  |
| 306 | true | true | true | true | true | true | false |  |
| 307 | true | true | true | true | true | true | false |  |
| 308 | true | true | true | true | true | true | false |  |
| 309 | true | true | true | true | true | true | false |  |

## Margins against both families

2 of 8 joint-passing seeds exceed the most damaging sampled first-order-matched path by less than 10% of that path's AUC (0 seeds with this percentage undefined because that family's maximum AUC is ≤ eps0). At alpha = 1, at least one sampled first-order-matched path causes strictly greater loss than reversion in 3/10 seeds, and at least one ties it within eps0 in 0/10 seeds. The preregistered directional criterion concerns trapezoidal AUC over the dose grid; an endpoint-only directional comparison against this family would pass in 7/10 seeds. These descriptive findings do not change the frozen labels.

1 of 8 joint-passing seeds exceed the most damaging sampled isotropic path by less than 10% of that path's AUC (0 seeds with this percentage undefined because that family's maximum AUC is ≤ eps0). At alpha = 1, at least one sampled isotropic path causes strictly greater loss than reversion in 5/10 seeds, and at least one ties it within eps0 in 0/10 seeds. The preregistered directional criterion concerns trapezoidal AUC over the dose grid; an endpoint-only directional comparison against this family would pass in 5/10 seeds. These descriptive findings do not change the frozen labels.

The REPLICATED label depends on at least one seed whose directional margin against at least one family is below 10% of that family's most damaging sampled path; robustness to additional draws is untested.

AUC is the integral of the piecewise-linear interpolant through the six measured dose-excess values. It is not a certified integral of the network's continuous dose response. Negative excesses are retained; no clipping or absolute-value transformation is applied.

At alpha=1, only the hidden-to-hidden matrices during updates 5–8 equal their initialization. Input-to-hidden weights, biases, updates 1–4 and the fresh readout remain trained. This condition is not F-INIT, even apart from the readout difference.

Holding the same readout fixed in REV and random conditions controls readout identity, but does not eliminate differential disruption of compatibility among recurrent matrices, input weights, biases and the readout.

## Secondary blocks

Secondary results are correlated with the primary and with each other. They do not substitute for the primary and there is no any-block upgrade.

- Secondary (block-wise), r: JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET (0/10 joint)
- Secondary (block-wise), z: JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET (0/10 joint)
- Secondary (block-wise), n: JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET (5/10 joint)

The primary effect was not reproduced by any single block at the declared criterion.


## First-order diagnostics

The residual after subtracting the initial tangent contribution is reported for each seed. It is not a curvature estimate.
Sampled non-decreasing values do not imply a continuously monotonic path.

| seed | <G, delta> | cos | FO_AUC | residual_REV | negligible | fixed |
| --- | --- | --- | --- | --- | --- | --- |
| 300 | -0.0015665883 | -0.26066488 | -0.00078329417 | 0.0063716768 | none | none |
| 301 | 0.00027215223 | 0.05865062 | 0.00013607611 | 0.0055300978 | none | none |
| 302 | -0.0010934904 | -0.24460175 | -0.00054674521 | 0.0049263787 | none | none |
| 303 | -0.00066358759 | -0.16669655 | -0.00033179379 | 0.0058466481 | none | none |
| 304 | -0.0017996918 | -0.30884215 | -0.00089984592 | 0.0052708134 | none | none |
| 305 | -0.00030733258 | -0.083777711 | -0.00015366629 | 0.0055375063 | none | none |
| 306 | -0.0010769237 | -0.30839976 | -0.00053846185 | 0.0058884611 | none | none |
| 307 | -0.00090555516 | -0.22993306 | -0.00045277758 | 0.0056445156 | none | none |
| 308 | -0.00086756127 | -0.21725518 | -0.00043378063 | 0.0060888686 | none | none |
| 309 | -0.0006561099 | -0.15049835 | -0.00032805495 | 0.0052536243 | none | none |

## Descriptive L_cont, XOR and E_total

These quantities are descriptive. Vector success does not establish an XOR-specific effect.

| seed | L_cont AUC | L_prefix XOR AUC | delta E_total(1) | delta E_XOR(1) |
| --- | --- | --- | --- | --- |
| 300 | 0.016409852 | 0.0037766667 | 0.064863015 | 0.036451374 |
| 301 | 0.014452295 | 0.0040354992 | 0.05580442 | 0.029046478 |
| 302 | 0.013108896 | 0.0029472534 | 0.077270836 | 0.044098966 |
| 303 | 0.010459203 | 0.0036562717 | 0.045086373 | 0.028811786 |
| 304 | 0.016919042 | 0.0030217371 | 0.06638495 | 0.032161605 |
| 305 | 0.013325032 | 0.0036369793 | 0.062657806 | 0.035752217 |
| 306 | 0.014489436 | 0.0037236372 | 0.065654884 | 0.029514703 |
| 307 | 0.015985925 | 0.0035295497 | 0.06972435 | 0.03763971 |
| 308 | 0.0096595215 | 0.0038869316 | 0.040931115 | 0.024059667 |
| 309 | 0.016053689 | 0.0033114464 | 0.072722908 | 0.035496285 |

## Development history

Exploratory phase A curves for seeds 100-109 and 200-209 are in `first_order_control_phaseA_exploratory/`. They are development-only and are not confirmatory. They are not pooled with seeds 300-309, and they do not set this label.

Freeze commit: `335e5056f38d4d5fffc737e467b3faebe5c9a77a`.
