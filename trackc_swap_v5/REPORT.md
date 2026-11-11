# Track C swap v5 (option G: v4 with 3600 phase-2 updates): results

Intake that holds the band: about 4.13 meals per 500 steps.

rho = consumed food per 500 steps. Paid regulator rho_paid = 3.79; floor = 0.19; margin = 0.95. No-fate task accuracy 0.998; no-fate task agent rho 0.01. Learned: True. S4: True.

Task load (accuracy lost by no-fate agents under imposed full erasure): rate 0.1: 0.315 (loaded); rate 0.3: 0.482 (loaded)

Any condition supports H3-D: **False**.

## Objective M1

| gain | rate | rho fate | rho yoked | seeds over margin | fate > yoked | fate more in band | in band fate / yoked | acc fate / yoked | acc fate full erasure | mean gain | S3 | label | H3-D |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GRADED | 0.1 | 2.15 | 1.90 | 0/9 | 6/9 | 7/9 | 0.36 / 0.34 | 0.984 / 0.983 | 0.947 | 0.36 | untested | ARMOURED | False |
| GRADED | 0.3 | 2.65 | 1.83 | 2/9 | 7/9 | 6/9 | 0.39 / 0.33 | 0.962 / 0.961 | 0.849 | 0.33 | True | NO_EMERGENCE | False |
| SAT | 0.1 | 2.05 | 1.72 | 0/9 | 9/9 | 9/9 | 0.34 / 0.31 | 0.980 / 0.977 | 0.959 | 0.53 | untested | ARMOURED | False |
| SAT | 0.3 | 4.06 | 1.91 | 5/9 | 8/9 | 9/9 | 0.69 / 0.37 | 0.969 / 0.971 | 0.775 | 0.18 | True | PARTIAL | False |

## Specificity cells (objective M0, rate 0.3)

| gain | rho fate | rho yoked | median paired difference | seeds over margin | fate > yoked | fate more in band |
| --- | --- | --- | --- | --- | --- | --- |
| GRADED | 0.52 | 0.57 | 0.00 | 0/9 | 4/9 | 5/9 |
| SAT | 0.56 | 0.62 | -0.05 | 0/9 | 3/9 | 2/9 |

## Onset (phase-1 agent with fate switched on, before any phase-2 update)

| objective | gain | rate | acc | rho | in band | mean gain |
| --- | --- | --- | --- | --- | --- | --- |
| M0 | GRADED | 0.3 | 0.107 | 1.32 | 0.27 | 0.44 |
| M0 | SAT | 0.3 | 0.107 | 1.20 | 0.28 | 0.60 |
| M1 | GRADED | 0.1 | 0.800 | 0.00 | 0.17 | 0.59 |
| M1 | GRADED | 0.3 | 0.638 | 0.00 | 0.17 | 0.59 |
| M1 | SAT | 0.1 | 0.765 | 0.00 | 0.17 | 0.75 |
| M1 | SAT | 0.3 | 0.622 | 0.00 | 0.17 | 0.75 |

## Phase-2 trajectory (exploratory checkpoints, then final)

| condition | updates | rho fate | median paired diff | over margin | fate > yoked | more in band | in band fate | acc full erasure fate / yoked |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M0|GRADED|0.3 | 1200 | 0.91 | 0.10 | 0/9 | 8/9 | 5/9 | 0.28 | 0.133 / 0.129 |
| M0|GRADED|0.3 | 2400 | 0.73 | 0.11 | 0/9 | 6/9 | 5/9 | 0.27 | 0.156 / 0.158 |
| M0|GRADED|0.3 | final | 0.52 | 0.00 | 0/9 | 4/9 | 5/9 | 0.24 | 0.162 / 0.157 |
| M0|SAT|0.3 | 1200 | 0.81 | 0.04 | 0/9 | 7/9 | 6/9 | 0.25 | 0.133 / 0.125 |
| M0|SAT|0.3 | 2400 | 0.55 | -0.05 | 0/9 | 4/9 | 4/9 | 0.25 | 0.128 / 0.134 |
| M0|SAT|0.3 | final | 0.56 | -0.05 | 0/9 | 3/9 | 2/9 | 0.23 | 0.148 / 0.137 |
| M1|GRADED|0.1 | 1200 | 2.28 | 0.16 | 0/9 | 7/9 | 7/9 | 0.37 | 0.696 / 0.693 |
| M1|GRADED|0.1 | 2400 | 1.80 | 0.19 | 0/9 | 9/9 | 7/9 | 0.34 | 0.927 / 0.926 |
| M1|GRADED|0.1 | final | 2.15 | 0.05 | 0/9 | 6/9 | 7/9 | 0.36 | 0.947 / 0.945 |
| M1|GRADED|0.3 | 1200 | 2.50 | 0.31 | 0/9 | 7/9 | 8/9 | 0.38 | 0.518 / 0.527 |
| M1|GRADED|0.3 | 2400 | 2.78 | 0.50 | 1/9 | 8/9 | 8/9 | 0.40 | 0.786 / 0.791 |
| M1|GRADED|0.3 | final | 2.65 | 0.61 | 2/9 | 7/9 | 6/9 | 0.39 | 0.849 / 0.855 |
| M1|SAT|0.1 | 1200 | 2.52 | 0.46 | 0/9 | 9/9 | 9/9 | 0.39 | 0.698 / 0.694 |
| M1|SAT|0.1 | 2400 | 2.89 | 0.34 | 0/9 | 8/9 | 8/9 | 0.43 | 0.928 / 0.931 |
| M1|SAT|0.1 | final | 2.05 | 0.33 | 0/9 | 9/9 | 9/9 | 0.34 | 0.959 / 0.960 |
| M1|SAT|0.3 | 1200 | 2.44 | 0.29 | 0/9 | 9/9 | 9/9 | 0.38 | 0.518 / 0.522 |
| M1|SAT|0.3 | 2400 | 3.96 | 1.09 | 6/9 | 9/9 | 9/9 | 0.51 | 0.607 / 0.614 |
| M1|SAT|0.3 | final | 4.06 | 1.34 | 5/9 | 8/9 | 9/9 | 0.69 | 0.775 / 0.776 |

## Per-seed rho (fate / yoked)

| condition | 500 | 501 | 502 | 503 | 504 | 505 | 506 | 507 | 508 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M0|GRADED|0.3 | 1.18 / 1.58 | 0.84 / 0.83 | 0.52 / 0.57 | 0.43 / 0.50 | 0.49 / 0.43 | 0.52 / 0.52 | 1.08 / 0.82 | 1.20 / 0.89 | 0.44 / 0.52 |
| M0|SAT|0.3 | 0.70 / 0.91 | 1.37 / 1.20 | 0.46 / 0.46 | 0.40 / 0.50 | 0.33 / 0.38 | 0.53 / 0.52 | 0.93 / 0.91 | 0.56 / 0.62 | 0.56 / 0.68 |
| M1|GRADED|0.1 | 2.29 / 2.07 | 2.73 / 2.12 | 4.17 / 4.12 | 2.71 / 2.23 | 0.94 / 0.94 | 0.46 / 0.44 | 0.52 / 0.54 | 2.15 / 1.60 | 1.88 / 1.90 |
| M1|GRADED|0.3 | 2.65 / 1.83 | 3.33 / 2.07 | 2.55 / 1.95 | 0.66 / 0.51 | 1.29 / 1.49 | 3.20 / 1.03 | 2.84 / 2.15 | 0.62 / 0.66 | 3.14 / 2.55 |
| M1|SAT|0.1 | 2.51 / 2.00 | 3.56 / 3.20 | 3.58 / 2.97 | 2.17 / 1.79 | 0.54 / 0.44 | 1.19 / 1.06 | 0.79 / 0.73 | 2.05 / 1.72 | 0.91 / 0.77 |
| M1|SAT|0.3 | 4.17 / 3.28 | 4.15 / 1.63 | 0.87 / 0.87 | 2.97 / 2.14 | 4.09 / 1.59 | 3.88 / 2.44 | 2.16 / 1.61 | 4.06 / 1.91 | 4.20 / 2.86 |
