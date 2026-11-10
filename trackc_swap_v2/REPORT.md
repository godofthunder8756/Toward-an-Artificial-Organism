# Track C swap v2 (2x2: start x gain rule): results

rho = consumed food per 500 steps. Paid regulator rho_paid = 16.87; floor = 0.84; margin = 4.22. No-fate task accuracy 1.000; no-fate task agent rho 0.00. Learned: True. S4: True.

Task load (accuracy lost by no-fate agents under imposed full noise): kappa_f 2.0: 0.148 (not loaded); kappa_f 4.0: 0.422 (loaded)

Any condition supports H3-D: **False**.

## Objective M1

| gain | start | kappa_f | rho fate | rho yoked | seeds over margin | in band fate / yoked | acc fate | acc fate full noise | mean gain | S3 | label | H3-D |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GRADED | NAIVE | 2.0 | 0.01 | 0.01 | 0/9 | 0.04 / 0.04 | 0.762 | 0.756 | 0.90 | untested | NOT_LOADED | False |
| GRADED | NAIVE | 4.0 | 0.00 | 0.00 | 0/9 | 0.04 / 0.04 | 0.501 | 0.499 | 0.90 | True | UNLEARNED | False |
| GRADED | SCAFFOLD | 2.0 | 0.16 | 0.18 | 0/9 | 0.04 / 0.04 | 0.995 | 0.991 | 0.90 | untested | NOT_LOADED | False |
| GRADED | SCAFFOLD | 4.0 | 0.21 | 0.16 | 0/9 | 0.04 / 0.04 | 0.980 | 0.975 | 0.90 | True | ARMOURED | False |
| SAT | NAIVE | 2.0 | 0.03 | 0.06 | 0/9 | 0.04 / 0.04 | 0.802 | 0.804 | 0.94 | untested | NOT_LOADED | False |
| SAT | NAIVE | 4.0 | 0.00 | 0.00 | 0/9 | 0.04 / 0.04 | 0.502 | 0.500 | 0.94 | True | UNLEARNED | False |
| SAT | SCAFFOLD | 2.0 | 0.17 | 0.19 | 0/9 | 0.04 / 0.04 | 0.997 | 0.993 | 0.93 | untested | NOT_LOADED | False |
| SAT | SCAFFOLD | 4.0 | 0.18 | 0.20 | 0/9 | 0.04 / 0.04 | 0.965 | 0.964 | 0.94 | True | ARMOURED | False |

## Specificity cells (objective M0, kappa_f 4)

| gain | start | rho fate | rho yoked | median paired difference | seeds over margin |
| --- | --- | --- | --- | --- | --- |
| GRADED | NAIVE | 2.66 | 0.80 | 1.22 | 0/9 |
| GRADED | SCAFFOLD | 2.43 | 1.73 | 0.35 | 0/9 |
| SAT | NAIVE | 1.71 | 1.14 | 0.54 | 0/9 |
| SAT | SCAFFOLD | 1.07 | 0.88 | 0.01 | 0/9 |

## Scaffold onset (phase-1 agent with fate switched on, before any phase-2 update)

| objective | gain | kappa_f | acc at onset | rho at onset | mean gain at onset |
| --- | --- | --- | --- | --- | --- |
| M0 | GRADED | 4.0 | 0.153 | 0.35 | 0.89 |
| M0 | SAT | 4.0 | 0.153 | 0.35 | 0.93 |
| M1 | GRADED | 2.0 | 0.874 | 0.00 | 0.90 |
| M1 | GRADED | 4.0 | 0.632 | 0.03 | 0.90 |
| M1 | SAT | 2.0 | 0.860 | 0.00 | 0.94 |
| M1 | SAT | 4.0 | 0.609 | 0.02 | 0.94 |

## Per-seed rho (fate / yoked)

| condition | 200 | 201 | 202 | 203 | 204 | 205 | 206 | 207 | 208 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M0|GRADED|NAIVE|4.0 | 2.98 / 0.69 | 3.16 / 1.93 | 2.68 / 0.71 | 2.65 / 0.79 | 1.47 / 0.77 | 2.66 / 0.80 | 1.84 / 1.15 | 2.70 / 1.48 | 2.05 / 1.01 |
| M0|GRADED|SCAFFOLD|4.0 | 2.43 / 2.08 | 2.45 / 1.97 | 2.95 / 1.73 | 0.62 / 0.71 | 0.89 / 0.74 | 0.61 / 0.55 | 2.52 / 1.80 | 2.83 / 2.48 | 2.08 / 1.30 |
| M0|SAT|NAIVE|4.0 | 1.72 / 1.18 | 2.18 / 1.27 | 1.30 / 0.56 | 1.30 / 1.00 | 0.62 / 1.14 | 1.71 / 1.52 | 1.35 / 0.69 | 1.77 / 2.09 | 1.88 / 0.93 |
| M0|SAT|SCAFFOLD|4.0 | 0.68 / 0.72 | 2.42 / 2.41 | 1.89 / 1.58 | 0.45 / 0.46 | 0.39 / 0.36 | 0.76 / 0.68 | 1.88 / 2.09 | 2.12 / 2.25 | 1.07 / 0.88 |
| M1|GRADED|NAIVE|2.0 | 0.00 / 0.00 | 0.00 / 0.00 | 0.20 / 0.01 | 0.00 / 0.05 | 0.20 / 0.23 | 0.01 / 0.00 | 0.04 / 0.22 | 0.01 / 0.07 | 0.02 / 0.00 |
| M1|GRADED|NAIVE|4.0 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 |
| M1|GRADED|SCAFFOLD|2.0 | 0.23 / 0.18 | 0.16 / 0.20 | 0.16 / 0.18 | 0.12 / 0.15 | 0.14 / 0.12 | 0.27 / 0.30 | 0.15 / 0.18 | 0.11 / 0.12 | 0.49 / 0.35 |
| M1|GRADED|SCAFFOLD|4.0 | 0.41 / 0.25 | 0.41 / 0.32 | 0.10 / 0.12 | 0.19 / 0.14 | 0.29 / 0.26 | 0.06 / 0.08 | 0.12 / 0.15 | 0.21 / 0.16 | 0.31 / 0.26 |
| M1|SAT|NAIVE|2.0 | 0.00 / 0.00 | 0.16 / 0.00 | 0.29 / 0.02 | 0.00 / 0.38 | 0.09 / 0.06 | 0.01 / 0.00 | 0.05 / 0.08 | 0.01 / 0.09 | 0.03 / 0.14 |
| M1|SAT|NAIVE|4.0 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 |
| M1|SAT|SCAFFOLD|2.0 | 0.27 / 0.34 | 0.15 / 0.19 | 0.20 / 0.19 | 0.17 / 0.16 | 0.34 / 0.41 | 0.01 / 0.01 | 0.14 / 0.13 | 0.12 / 0.12 | 0.25 / 0.29 |
| M1|SAT|SCAFFOLD|4.0 | 0.48 / 0.41 | 0.29 / 0.27 | 0.18 / 0.20 | 0.31 / 0.27 | 0.32 / 0.41 | 0.09 / 0.13 | 0.16 / 0.17 | 0.18 / 0.20 | 0.18 / 0.19 |
