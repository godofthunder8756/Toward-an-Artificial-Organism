# Track C swap v4 (option E: erasure fate, scaffolded start, wear 0.001): results

Intake that holds the band: about 4.13 meals per 500 steps.

rho = consumed food per 500 steps. Paid regulator rho_paid = 3.90; floor = 0.19; margin = 0.97. No-fate task accuracy 0.998; no-fate task agent rho 0.03. Learned: True. S4: True.

Task load (accuracy lost by no-fate agents under imposed full erasure): rate 0.1: 0.307 (loaded); rate 0.3: 0.483 (loaded)

Any condition supports H3-D: **False**.

## Objective M1

| gain | rate | rho fate | rho yoked | seeds over margin | fate > yoked | fate more in band | in band fate / yoked | acc fate / yoked | acc fate full erasure | mean gain | S3 | label | H3-D |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GRADED | 0.1 | 2.00 | 1.54 | 1/9 | 9/9 | 8/9 | 0.36 / 0.32 | 0.952 / 0.952 | 0.869 | 0.37 | untested | PARTIAL | False |
| GRADED | 0.3 | 2.23 | 1.86 | 0/9 | 7/9 | 7/9 | 0.36 / 0.34 | 0.912 / 0.915 | 0.789 | 0.35 | True | NO_EMERGENCE | False |
| SAT | 0.1 | 2.05 | 1.82 | 0/9 | 7/9 | 8/9 | 0.37 / 0.33 | 0.865 / 0.868 | 0.755 | 0.49 | untested | NO_EMERGENCE | False |
| SAT | 0.3 | 2.54 | 2.10 | 0/9 | 8/9 | 7/9 | 0.41 / 0.36 | 0.766 / 0.770 | 0.514 | 0.45 | True | NO_EMERGENCE | False |

## Specificity cells (objective M0, rate 0.3)

| gain | rho fate | rho yoked | median paired difference | seeds over margin | fate > yoked | fate more in band |
| --- | --- | --- | --- | --- | --- | --- |
| GRADED | 0.80 | 0.82 | -0.07 | 0/9 | 2/9 | 3/9 |
| SAT | 1.05 | 1.07 | -0.02 | 0/9 | 4/9 | 4/9 |

## Onset (phase-1 agent with fate switched on, before any phase-2 update)

| objective | gain | rate | acc | rho | in band | mean gain |
| --- | --- | --- | --- | --- | --- | --- |
| M0 | GRADED | 0.3 | 0.160 | 1.24 | 0.28 | 0.45 |
| M0 | SAT | 0.3 | 0.158 | 1.20 | 0.27 | 0.61 |
| M1 | GRADED | 0.1 | 0.803 | 0.05 | 0.17 | 0.58 |
| M1 | GRADED | 0.3 | 0.641 | 0.05 | 0.17 | 0.58 |
| M1 | SAT | 0.1 | 0.768 | 0.05 | 0.17 | 0.74 |
| M1 | SAT | 0.3 | 0.631 | 0.05 | 0.17 | 0.74 |

## Per-seed rho (fate / yoked)

| condition | 400 | 401 | 402 | 403 | 404 | 405 | 406 | 407 | 408 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M0|GRADED|0.3 | 1.52 / 1.81 | 0.58 / 0.47 | 0.43 / 0.52 | 0.80 / 0.79 | 0.59 / 0.66 | 1.59 / 1.78 | 1.43 / 1.76 | 0.80 / 0.82 | 1.15 / 1.17 |
| M0|SAT|0.3 | 1.52 / 1.88 | 0.52 / 0.38 | 0.39 / 0.34 | 1.07 / 1.18 | 0.41 / 0.48 | 1.05 / 1.07 | 1.38 / 1.68 | 0.81 / 0.80 | 1.45 / 1.31 |
| M1|GRADED|0.1 | 2.80 / 2.43 | 0.50 / 0.45 | 2.06 / 1.73 | 3.18 / 2.75 | 1.61 / 1.50 | 2.97 / 1.93 | 1.66 / 1.22 | 2.00 / 1.54 | 1.44 / 1.41 |
| M1|GRADED|0.3 | 2.31 / 2.03 | 0.49 / 0.54 | 2.45 / 2.13 | 2.01 / 2.21 | 1.24 / 1.04 | 2.32 / 1.85 | 2.86 / 2.36 | 1.55 / 1.36 | 2.23 / 1.86 |
| M1|SAT|0.1 | 2.59 / 1.93 | 0.87 / 0.60 | 2.04 / 1.62 | 2.67 / 2.38 | 1.73 / 2.09 | 2.42 / 1.51 | 2.05 / 1.41 | 1.84 / 1.82 | 2.21 / 2.23 |
| M1|SAT|0.3 | 2.05 / 1.21 | 2.64 / 2.47 | 2.88 / 2.26 | 1.15 / 1.28 | 2.38 / 2.05 | 2.54 / 2.22 | 1.66 / 1.04 | 2.96 / 2.10 | 2.78 / 2.19 |
