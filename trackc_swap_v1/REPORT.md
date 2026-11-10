# Track C objective-swap experiment: results

Primary dose kappa_f = 4.0. Outcome label: **UNLEARNED**. H3-D supported: **False**.

rho = consumed food per 500 steps. Paid regulator rho_paid = 16.67; floor = 0.83; margin = 4.17. No-fate task accuracy (median) = 0.999.

## By dose (objective M1)

| kappa_f | task-load drop | loaded | rho fate | rho yoked | seeds over margin | S1 | acc fate | acc fate, full noise | acc yoked | in band | mean gain | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 0.015 | False | 0.14 | 0.04 | 0/9 | False | 0.993 | 0.992 | 0.985 | 0.04 | 0.94 | NOT_LOADED |
| 2.0 | 0.160 | True | 0.00 | 0.00 | 0/9 | False | 0.507 | 0.504 | 0.500 | 0.04 | 0.94 | UNLEARNED |
| 4.0 | 0.420 | True | 0.00 | 0.00 | 0/9 | False | 0.499 | 0.501 | 0.497 | 0.04 | 0.94 | UNLEARNED |

## Predictions at the primary dose

| Prediction | Holds | Detail |
| --- | --- | --- |
| PC task loaded | True | drop 0.420 (need 0.15) |
| S1 emergence | False | 0/9 seeds over margin; yoked median 0.00 |
| S2 convention | not applicable | M2: fate 0.00, yoked 0.00; M4: fate 1.93, yoked 1.90 |
| S3 specificity | False | fate M0 1.31; yoked M0 1.42 |
| S4 payment | True | paid 16.67; no-fate M1 0.05 |

## Per-seed rho, objective M1

| kappa_f | seed | fate | yoked |
| --- | --- | --- | --- |
| 1.0 | 100 | 0.20 | 0.04 |
| 1.0 | 101 | 0.01 | 0.01 |
| 1.0 | 102 | 0.14 | 0.04 |
| 1.0 | 103 | 0.21 | 0.03 |
| 1.0 | 104 | 0.00 | 0.23 |
| 1.0 | 105 | 0.15 | 0.04 |
| 1.0 | 106 | 0.12 | 0.04 |
| 1.0 | 107 | 0.15 | 0.01 |
| 1.0 | 108 | 0.00 | 0.00 |
| 2.0 | 100 | 0.00 | 0.00 |
| 2.0 | 101 | 0.00 | 0.03 |
| 2.0 | 102 | 0.00 | 0.00 |
| 2.0 | 103 | 0.09 | 0.04 |
| 2.0 | 104 | 0.00 | 0.04 |
| 2.0 | 105 | 0.18 | 0.07 |
| 2.0 | 106 | 0.12 | 0.00 |
| 2.0 | 107 | 0.00 | 0.00 |
| 2.0 | 108 | 0.00 | 0.00 |
| 4.0 | 100 | 0.00 | 0.00 |
| 4.0 | 101 | 0.00 | 0.00 |
| 4.0 | 102 | 0.00 | 0.00 |
| 4.0 | 103 | 0.00 | 0.00 |
| 4.0 | 104 | 0.00 | 0.00 |
| 4.0 | 105 | 0.00 | 0.00 |
| 4.0 | 106 | 0.00 | 0.00 |
| 4.0 | 107 | 0.00 | 0.00 |
| 4.0 | 108 | 0.00 | 0.00 |
