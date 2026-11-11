# Track C swap v3 (erasure fate, scaffolded start): results

rho = consumed food per 500 steps. Paid regulator rho_paid = 16.80; floor = 0.84; margin = 4.20. No-fate task accuracy 0.998; no-fate task agent rho 0.00. Learned: True. S4: True.

Task load (accuracy lost by no-fate agents under imposed full erasure): rate 0.1: 0.308 (loaded); rate 0.3: 0.486 (loaded)

Any condition supports H3-D: **False**.

## Objective M1

| gain | rate | rho fate | rho yoked | seeds over margin | fate > yoked | in band fate / yoked | acc fate / yoked | acc fate full erasure | mean gain | S3 | label | H3-D |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GRADED | 0.1 | 0.68 | 0.74 | 0/9 | 5/9 | 0.04 / 0.04 | 0.723 / 0.724 | 0.695 | 0.89 | untested | DEGRADED | False |
| GRADED | 0.3 | 1.55 | 1.34 | 0/9 | 5/9 | 0.04 / 0.04 | 0.555 / 0.554 | 0.528 | 0.88 | True | DEGRADED | False |
| SAT | 0.1 | 0.67 | 0.66 | 0/9 | 5/9 | 0.04 / 0.04 | 0.711 / 0.716 | 0.696 | 0.94 | untested | DEGRADED | False |
| SAT | 0.3 | 1.11 | 1.11 | 0/9 | 6/9 | 0.04 / 0.04 | 0.544 / 0.546 | 0.526 | 0.93 | True | DEGRADED | False |

## Specificity cells (objective M0, rate 0.3)

| gain | rho fate | rho yoked | median paired difference | seeds over margin | fate > yoked |
| --- | --- | --- | --- | --- | --- |
| GRADED | 0.84 | 0.89 | 0.11 | 0/9 | 5/9 |
| SAT | 0.79 | 0.89 | -0.01 | 0/9 | 4/9 |

## Onset (phase-1 agent with fate switched on, before any phase-2 update)

| objective | gain | rate | acc | rho | in band | mean gain |
| --- | --- | --- | --- | --- | --- | --- |
| M0 | GRADED | 0.3 | 0.119 | 1.14 | 0.04 | 0.88 |
| M0 | SAT | 0.3 | 0.119 | 1.14 | 0.04 | 0.93 |
| M1 | GRADED | 0.1 | 0.717 | 0.00 | 0.04 | 0.90 |
| M1 | GRADED | 0.3 | 0.542 | 0.00 | 0.04 | 0.90 |
| M1 | SAT | 0.1 | 0.708 | 0.00 | 0.04 | 0.94 |
| M1 | SAT | 0.3 | 0.538 | 0.00 | 0.04 | 0.94 |

## Per-seed rho (fate / yoked)

| condition | 300 | 301 | 302 | 303 | 304 | 305 | 306 | 307 | 308 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M0|GRADED|0.3 | 0.73 / 0.92 | 1.06 / 0.89 | 0.52 / 0.41 | 1.44 / 1.69 | 0.69 / 0.54 | 1.60 / 1.26 | 0.55 / 0.57 | 0.84 / 0.88 | 2.02 / 1.67 |
| M0|SAT|0.3 | 0.64 / 0.89 | 1.11 / 1.15 | 0.43 / 0.44 | 1.58 / 1.95 | 0.59 / 0.45 | 1.30 / 1.00 | 0.61 / 0.65 | 0.79 / 0.70 | 1.93 / 1.80 |
| M1|GRADED|0.1 | 0.61 / 0.66 | 0.32 / 0.34 | 2.65 / 2.39 | 1.33 / 1.11 | 0.45 / 0.43 | 0.68 / 0.74 | 0.86 / 0.83 | 0.01 / 0.00 | 0.87 / 0.94 |
| M1|GRADED|0.3 | 1.22 / 1.05 | 1.97 / 1.86 | 0.89 / 0.67 | 0.75 / 0.79 | 0.54 / 0.56 | 1.55 / 1.67 | 1.97 / 2.08 | 1.79 / 1.76 | 1.66 / 1.34 |
| M1|SAT|0.1 | 0.52 / 0.53 | 1.57 / 1.82 | 1.22 / 1.19 | 1.04 / 0.71 | 0.47 / 0.52 | 0.67 / 0.66 | 1.10 / 1.18 | 0.00 / 0.00 | 0.21 / 0.20 |
| M1|SAT|0.3 | 1.20 / 1.12 | 1.29 / 1.20 | 1.03 / 0.78 | 1.06 / 0.86 | 1.11 / 0.93 | 1.08 / 1.11 | 2.30 / 2.52 | 1.44 / 1.54 | 1.08 / 1.02 |
