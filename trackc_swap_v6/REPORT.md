# Track C swap v6 (option J: confirmation of SAT r = 0.3 regulators): results

**Verdict: CONFIRMED**

Paid regulator rho_paid = 3.78, in band 0.81; margin = 0.94. No-fate task accuracy 0.999; no-fate task agent rho 0.05. Learned: True. S4: True. Task load at 0.3: 0.482 (loaded).

## Confirmation criteria

| criterion | value | threshold | holds |
| --- | --- | --- | --- |
| C1 M1 fate regulators | 7/18 | >= 6 | True |
| C2 M1 fate more in band | 14/18 | >= 13 | True |
| C3 M0 fate regulators | 0/18 | <= 1 | True |
| C4 M1 yoked regulators (roles swapped) | 0/18 | <= 1 | True |

Secondary: Spearman(in band, full-erasure accuracy) over M1 fate agents = -0.95 (predicted <= -0.5): replicated True.

## Cells (medians)

| objective | rho fate / yoked | in band fate / yoked | fate > yoked rho | over margin | acc fate / yoked | acc full erasure fate / yoked | acc erasure off fate | onset in band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | 3.33 / 1.71 | 0.46 / 0.36 | 14/18 | 8/18 | 0.972 / 0.968 | 0.872 / 0.866 | 1.000 | 0.17 |
| M0 | 0.60 / 0.56 | 0.24 / 0.24 | 13/18 | 0/18 | 0.134 / 0.140 | 0.140 / 0.145 | 0.139 | 0.27 |

## Checkpoints (descriptive)

| objective | updates | fate regulators | in band fate | fate more in band |
| --- | --- | --- | --- | --- |
| M1 | 1200 | 0/18 | 0.37 | 16/18 |
| M1 | 2400 | 1/18 | 0.44 | 17/18 |
| M1 | final | 7/18 | 0.46 | 14/18 |
| M0 | 1200 | 0/18 | 0.27 | 8/18 |
| M0 | 2400 | 0/18 | 0.25 | 11/18 |
| M0 | final | 0/18 | 0.24 | 12/18 |

## Per seed, M1

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 600 | 1.54 / 0.97 | 0.33 / 0.27 | 0.0031 / 0.0026 | 0.55 | 0.945 / 0.939 | False | False |
| 601 | 2.84 / 3.04 | 0.40 / 0.41 | 0.0058 / 0.0055 | 0.46 | 0.892 / 0.883 | False | False |
| 602 | 1.78 / 1.65 | 0.35 / 0.34 | 0.0035 / 0.0037 | 0.52 | 0.964 / 0.967 | False | False |
| 603 | 1.01 / 0.79 | 0.28 / 0.26 | 0.0020 / 0.0023 | 0.61 | 0.979 / 0.977 | False | False |
| 604 | 4.01 / 1.61 | 0.90 / 0.38 | 0.0119 / 0.0007 | 0.03 | 0.522 / 0.514 | True | False |
| 605 | 4.19 / 2.41 | 0.90 / 0.43 | 0.0160 / 0.0010 | 0.04 | 0.510 / 0.517 | True | False |
| 606 | 1.27 / 1.47 | 0.30 / 0.31 | 0.0025 / 0.0024 | 0.58 | 0.953 / 0.956 | False | False |
| 607 | 2.49 / 1.31 | 0.43 / 0.32 | 0.0052 / 0.0042 | 0.42 | 0.936 / 0.942 | False | False |
| 608 | 4.12 / 2.98 | 0.83 / 0.51 | 0.0143 / 0.0020 | 0.07 | 0.520 / 0.516 | True | False |
| 609 | 3.00 / 2.64 | 0.43 / 0.39 | 0.0061 / 0.0056 | 0.42 | 0.870 / 0.854 | False | False |
| 610 | 0.71 / 0.80 | 0.27 / 0.27 | 0.0014 / 0.0020 | 0.62 | 0.974 / 0.980 | False | False |
| 611 | 0.50 / 0.53 | 0.23 / 0.24 | 0.0009 / 0.0021 | 0.67 | 0.991 / 0.992 | False | False |
| 612 | 4.36 / 1.63 | 0.81 / 0.35 | 0.0219 / 0.0021 | 0.09 | 0.517 / 0.518 | True | False |
| 613 | 3.73 / 2.41 | 0.51 / 0.37 | 0.0083 / 0.0059 | 0.33 | 0.875 / 0.878 | False | False |
| 614 | 3.68 / 1.77 | 0.66 / 0.30 | 0.0090 / 0.0027 | 0.18 | 0.826 / 0.831 | True | False |
| 615 | 3.96 / 3.21 | 0.83 / 0.53 | 0.0120 / 0.0014 | 0.07 | 0.528 / 0.529 | True | False |
| 616 | 3.66 / 2.80 | 0.49 / 0.39 | 0.0080 / 0.0059 | 0.35 | 0.862 / 0.854 | False | False |
| 617 | 4.27 / 2.72 | 0.81 / 0.45 | 0.0158 / 0.0024 | 0.09 | 0.517 / 0.517 | True | False |

## Per seed, M0

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 600 | 0.33 / 0.32 | 0.22 / 0.21 | 0.0007 / 0.0007 | 0.69 | 0.190 / 0.215 | False | False |
| 601 | 0.36 / 0.38 | 0.21 / 0.22 | 0.0007 / 0.0013 | 0.70 | 0.157 / 0.154 | False | False |
| 602 | 0.48 / 0.37 | 0.23 / 0.21 | 0.0009 / 0.0016 | 0.67 | 0.154 / 0.143 | False | False |
| 603 | 0.54 / 0.57 | 0.23 / 0.24 | 0.0010 / 0.0021 | 0.67 | 0.158 / 0.151 | False | False |
| 604 | 1.37 / 1.52 | 0.30 / 0.31 | 0.0027 / 0.0026 | 0.58 | 0.150 / 0.172 | False | False |
| 605 | 1.57 / 1.54 | 0.30 / 0.32 | 0.0031 / 0.0033 | 0.57 | 0.116 / 0.122 | False | False |
| 606 | 0.70 / 0.57 | 0.26 / 0.24 | 0.0014 / 0.0018 | 0.64 | 0.121 / 0.111 | False | False |
| 607 | 0.77 / 0.71 | 0.27 / 0.26 | 0.0015 / 0.0014 | 0.63 | 0.130 / 0.119 | False | False |
| 608 | 0.63 / 0.60 | 0.25 / 0.25 | 0.0013 / 0.0011 | 0.64 | 0.137 / 0.147 | False | False |
| 609 | 0.59 / 0.54 | 0.24 / 0.23 | 0.0011 / 0.0020 | 0.66 | 0.118 / 0.130 | False | False |
| 610 | 0.61 / 0.57 | 0.25 / 0.24 | 0.0012 / 0.0018 | 0.65 | 0.077 / 0.085 | False | False |
| 611 | 0.59 / 0.54 | 0.23 / 0.23 | 0.0012 / 0.0010 | 0.66 | 0.118 / 0.122 | False | False |
| 612 | 0.29 / 0.25 | 0.21 / 0.21 | 0.0006 / 0.0011 | 0.70 | 0.129 / 0.134 | False | False |
| 613 | 0.66 / 0.55 | 0.24 / 0.23 | 0.0013 / 0.0021 | 0.66 | 0.149 / 0.151 | False | False |
| 614 | 0.60 / 0.80 | 0.24 / 0.27 | 0.0012 / 0.0016 | 0.66 | 0.142 / 0.149 | False | False |
| 615 | 0.51 / 0.48 | 0.24 / 0.24 | 0.0010 / 0.0018 | 0.66 | 0.155 / 0.161 | False | False |
| 616 | 0.43 / 0.35 | 0.22 / 0.21 | 0.0009 / 0.0009 | 0.68 | 0.190 / 0.176 | False | False |
| 617 | 0.68 / 0.77 | 0.25 / 0.26 | 0.0013 / 0.0015 | 0.65 | 0.115 / 0.131 | False | False |
