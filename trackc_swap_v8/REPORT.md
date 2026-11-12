# Track C swap v8 (option M: confirmation in the relocation world): results

**Claims (each: >= 6/9 fate regulators, bypass closed at the cell's rate, yoked and M0 controls <= 1):**

- MA (M1 SAT 0.1): **CONFIRMED** (CONFIRMED)
- MB (M1 GRADED 0.3): **CONFIRMED** (CONFIRMED)

Paid regulator rho_paid = 3.62, in band 0.73; margin = 0.91. No-fate task accuracy 0.999; no-fate task agent rho 0.01. Learned: True. S4: True. Task load: 0.1: 0.312 (loaded; no-fate full-erasure acc 0.687); 0.3: 0.479 (loaded; no-fate full-erasure acc 0.519).

## Labels (M1 cells)

| cell | label | regulators (needed) | bypass closed (median excess over no-fate; max; seeds > 0.10) | yoked regulators <= 1 | M0 regulators <= 1 |
| --- | --- | --- | --- | --- | --- |
| M1 SAT 0.1 | CONFIRMED | 9/9 (6) | True (+0.007; +0.021; 0) | True (0) | True (0) |
| M1 GRADED 0.1 | NOT_CONFIRMED | 3/9 (6) | True (+0.010; +0.020; 0) | True (0) | True (0) |
| M1 GRADED 0.3 | CONFIRMED | 9/9 (6) | True (+0.005; +0.011; 0) | True (0) | True (0) |

## Cells (medians)

| cell | regulators fate / yoked | in band fate / yoked | fate more in band | rho fate / yoked | over margin | acc fate / yoked | acc full erasure fate / yoked | acc erasure off fate | Spearman(in band, full-erasure acc) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M1 SAT 0.1 | 9 / 0 | 0.72 / 0.39 | 9/9 | 4.04 / 2.35 | 9/9 | 0.954 / 0.954 | 0.694 / 0.695 | 0.999 | 0.07 |
| M1 GRADED 0.1 | 3 / 0 | 0.55 / 0.41 | 9/9 | 3.78 / 2.77 | 8/9 | 0.911 / 0.911 | 0.695 / 0.695 | 1.000 | -0.27 |
| M1 GRADED 0.3 | 9 / 0 | 0.69 / 0.44 | 9/9 | 3.96 / 3.04 | 6/9 | 0.833 / 0.835 | 0.522 / 0.519 | 0.999 | 0.23 |
| M0 SAT 0.1 | 0 / 0 | 0.29 / 0.29 | 5/9 | 1.39 / 1.52 | 0/9 | 0.116 / 0.120 | 0.119 / 0.127 | 0.121 | -0.17 |
| M0 GRADED 0.1 | 0 / 0 | 0.30 / 0.29 | 5/9 | 1.59 / 1.48 | 0/9 | 0.124 / 0.129 | 0.119 / 0.123 | 0.124 | -0.10 |
| M0 GRADED 0.3 | 0 / 0 | 0.31 / 0.31 | 4/9 | 1.85 / 1.84 | 0/9 | 0.132 / 0.131 | 0.128 / 0.129 | 0.131 | -0.37 |

## Checkpoints (descriptive)

| cell | updates | fate regulators | in band fate | fate more in band | acc full erasure fate |
| --- | --- | --- | --- | --- | --- |
| M1 SAT 0.1 | 1200 | 0/9 | 0.43 | 9/9 | 0.691 |
| M1 SAT 0.1 | 2400 | 0/9 | 0.52 | 9/9 | 0.695 |
| M1 SAT 0.1 | final | 9/9 | 0.72 | 9/9 | 0.694 |
| M1 GRADED 0.1 | 1200 | 0/9 | 0.42 | 8/9 | 0.690 |
| M1 GRADED 0.1 | 2400 | 0/9 | 0.46 | 9/9 | 0.694 |
| M1 GRADED 0.1 | final | 3/9 | 0.55 | 9/9 | 0.695 |
| M1 GRADED 0.3 | 1200 | 0/9 | 0.46 | 9/9 | 0.515 |
| M1 GRADED 0.3 | 2400 | 1/9 | 0.51 | 9/9 | 0.518 |
| M1 GRADED 0.3 | final | 9/9 | 0.69 | 9/9 | 0.522 |
| M0 SAT 0.1 | 1200 | 0/9 | 0.28 | 4/9 | 0.122 |
| M0 SAT 0.1 | 2400 | 0/9 | 0.29 | 5/9 | 0.128 |
| M0 SAT 0.1 | final | 0/9 | 0.29 | 5/9 | 0.119 |
| M0 GRADED 0.1 | 1200 | 0/9 | 0.28 | 1/9 | 0.127 |
| M0 GRADED 0.1 | 2400 | 0/9 | 0.28 | 7/9 | 0.130 |
| M0 GRADED 0.1 | final | 0/9 | 0.30 | 5/9 | 0.119 |
| M0 GRADED 0.3 | 1200 | 0/9 | 0.33 | 4/9 | 0.117 |
| M0 GRADED 0.3 | 2400 | 0/9 | 0.31 | 5/9 | 0.134 |
| M0 GRADED 0.3 | final | 0/9 | 0.31 | 4/9 | 0.128 |

## Per seed, M1 SAT 0.1

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | excess over no-fate | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 800 | 4.23 / 2.18 | 0.72 / 0.39 | 0.0135 / 0.0034 | 0.15 | 0.695 / 0.695 | +0.002 | True | False |
| 801 | 3.79 / 2.15 | 0.72 / 0.34 | 0.0092 / 0.0014 | 0.11 | 0.701 / 0.702 | +0.011 | True | False |
| 802 | 4.48 / 3.32 | 0.65 / 0.46 | 0.0123 / 0.0052 | 0.20 | 0.691 / 0.699 | -0.007 | True | False |
| 803 | 3.92 / 2.43 | 0.63 / 0.40 | 0.0097 / 0.0037 | 0.20 | 0.693 / 0.692 | -0.002 | True | False |
| 804 | 3.95 / 2.59 | 0.78 / 0.37 | 0.0112 / 0.0011 | 0.09 | 0.691 / 0.693 | +0.021 | True | False |
| 805 | 4.12 / 2.35 | 0.64 / 0.39 | 0.0110 / 0.0043 | 0.21 | 0.694 / 0.689 | +0.007 | True | False |
| 806 | 3.91 / 1.54 | 0.74 / 0.29 | 0.0103 / 0.0020 | 0.12 | 0.690 / 0.692 | +0.006 | True | False |
| 807 | 4.16 / 1.84 | 0.82 / 0.37 | 0.0157 / 0.0018 | 0.07 | 0.701 / 0.696 | +0.016 | True | False |
| 808 | 4.04 / 2.88 | 0.74 / 0.45 | 0.0119 / 0.0028 | 0.13 | 0.700 / 0.700 | +0.014 | True | False |

## Per seed, M1 GRADED 0.1

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | excess over no-fate | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 800 | 4.09 / 2.98 | 0.51 / 0.43 | 0.0094 / 0.0065 | 0.25 | 0.695 / 0.695 | +0.002 | False | False |
| 801 | 3.74 / 2.79 | 0.58 / 0.41 | 0.0090 / 0.0043 | 0.21 | 0.701 / 0.702 | +0.011 | False | False |
| 802 | 3.45 / 2.97 | 0.55 / 0.45 | 0.0081 / 0.0035 | 0.22 | 0.690 / 0.701 | -0.008 | False | False |
| 803 | 3.76 / 2.77 | 0.49 / 0.41 | 0.0081 / 0.0065 | 0.26 | 0.702 / 0.694 | +0.007 | False | False |
| 804 | 3.78 / 2.59 | 0.62 / 0.40 | 0.0096 / 0.0034 | 0.19 | 0.690 / 0.693 | +0.020 | True | False |
| 805 | 3.82 / 2.68 | 0.52 / 0.40 | 0.0088 / 0.0055 | 0.24 | 0.688 / 0.692 | +0.001 | False | False |
| 806 | 3.90 / 2.46 | 0.61 / 0.38 | 0.0097 / 0.0040 | 0.20 | 0.694 / 0.692 | +0.010 | True | False |
| 807 | 4.10 / 3.17 | 0.62 / 0.44 | 0.0107 / 0.0041 | 0.19 | 0.701 / 0.697 | +0.016 | True | False |
| 808 | 3.30 / 2.36 | 0.49 / 0.37 | 0.0074 / 0.0047 | 0.25 | 0.701 / 0.699 | +0.015 | False | False |

## Per seed, M1 GRADED 0.3

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | excess over no-fate | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 800 | 4.20 / 3.26 | 0.65 / 0.45 | 0.0113 / 0.0042 | 0.18 | 0.528 / 0.526 | +0.011 | True | False |
| 801 | 4.09 / 3.04 | 0.73 / 0.44 | 0.0124 / 0.0025 | 0.15 | 0.528 / 0.522 | +0.007 | True | False |
| 802 | 4.07 / 2.62 | 0.68 / 0.40 | 0.0115 / 0.0030 | 0.16 | 0.521 / 0.536 | +0.004 | True | False |
| 803 | 3.96 / 3.22 | 0.69 / 0.52 | 0.0111 / 0.0031 | 0.16 | 0.522 / 0.515 | +0.003 | True | False |
| 804 | 3.95 / 3.04 | 0.69 / 0.44 | 0.0108 / 0.0027 | 0.17 | 0.515 / 0.519 | -0.004 | True | False |
| 805 | 3.84 / 3.09 | 0.64 / 0.44 | 0.0098 / 0.0030 | 0.18 | 0.516 / 0.517 | +0.005 | True | False |
| 806 | 3.89 / 3.08 | 0.72 / 0.49 | 0.0111 / 0.0020 | 0.15 | 0.514 / 0.519 | -0.006 | True | False |
| 807 | 3.96 / 2.80 | 0.79 / 0.36 | 0.0124 / 0.0015 | 0.13 | 0.529 / 0.522 | +0.008 | True | False |
| 808 | 3.75 / 2.82 | 0.64 / 0.40 | 0.0093 / 0.0030 | 0.18 | 0.528 / 0.517 | +0.008 | True | False |

## Per seed, M0 SAT 0.1

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 800 | 2.01 / 1.59 | 0.34 / 0.29 | 0.0041 / 0.0032 | 0.52 | 0.107 / 0.112 | False | False |
| 801 | 1.21 / 1.72 | 0.25 / 0.33 | 0.0024 / 0.0019 | 0.63 | 0.147 / 0.151 | False | False |
| 802 | 1.37 / 1.39 | 0.27 / 0.29 | 0.0027 / 0.0028 | 0.61 | 0.140 / 0.158 | False | False |
| 803 | 1.26 / 1.36 | 0.27 / 0.28 | 0.0026 / 0.0016 | 0.60 | 0.093 / 0.095 | False | False |
| 804 | 1.75 / 1.41 | 0.32 / 0.27 | 0.0036 / 0.0029 | 0.56 | 0.173 / 0.179 | False | False |
| 805 | 1.39 / 1.17 | 0.26 / 0.25 | 0.0028 / 0.0029 | 0.62 | 0.119 / 0.127 | False | False |
| 806 | 1.71 / 1.59 | 0.29 / 0.30 | 0.0035 / 0.0027 | 0.58 | 0.106 / 0.100 | False | False |
| 807 | 1.72 / 1.81 | 0.32 / 0.30 | 0.0036 / 0.0021 | 0.55 | 0.140 / 0.141 | False | False |
| 808 | 1.39 / 1.52 | 0.29 / 0.28 | 0.0029 / 0.0019 | 0.59 | 0.089 / 0.089 | False | False |

## Per seed, M0 GRADED 0.1

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 800 | 1.66 / 1.48 | 0.32 / 0.29 | 0.0035 / 0.0019 | 0.40 | 0.108 / 0.108 | False | False |
| 801 | 1.13 / 1.55 | 0.25 / 0.31 | 0.0023 / 0.0019 | 0.46 | 0.144 / 0.149 | False | False |
| 802 | 1.23 / 1.17 | 0.26 / 0.26 | 0.0025 / 0.0021 | 0.46 | 0.119 / 0.140 | False | False |
| 803 | 1.86 / 1.84 | 0.32 / 0.32 | 0.0038 / 0.0032 | 0.38 | 0.123 / 0.123 | False | False |
| 804 | 1.52 / 1.06 | 0.29 / 0.25 | 0.0031 / 0.0023 | 0.42 | 0.158 / 0.164 | False | False |
| 805 | 1.14 / 0.88 | 0.25 / 0.23 | 0.0023 / 0.0019 | 0.46 | 0.108 / 0.117 | False | False |
| 806 | 1.59 / 1.39 | 0.30 / 0.28 | 0.0032 / 0.0026 | 0.41 | 0.115 / 0.116 | False | False |
| 807 | 1.82 / 1.82 | 0.31 / 0.33 | 0.0038 / 0.0023 | 0.39 | 0.147 / 0.149 | False | False |
| 808 | 1.59 / 1.66 | 0.30 / 0.33 | 0.0032 / 0.0028 | 0.40 | 0.093 / 0.091 | False | False |

## Per seed, M0 GRADED 0.3

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 800 | 1.95 / 1.88 | 0.32 / 0.32 | 0.0039 / 0.0040 | 0.39 | 0.117 / 0.129 | False | False |
| 801 | 1.85 / 2.12 | 0.32 / 0.34 | 0.0037 / 0.0034 | 0.39 | 0.150 / 0.147 | False | False |
| 802 | 1.25 / 1.28 | 0.27 / 0.27 | 0.0025 / 0.0017 | 0.45 | 0.129 / 0.155 | False | False |
| 803 | 1.61 / 1.61 | 0.31 / 0.30 | 0.0032 / 0.0030 | 0.40 | 0.128 / 0.123 | False | False |
| 804 | 1.47 / 1.57 | 0.29 / 0.29 | 0.0030 / 0.0025 | 0.42 | 0.167 / 0.174 | False | False |
| 805 | 1.97 / 1.86 | 0.30 / 0.31 | 0.0039 / 0.0043 | 0.40 | 0.115 / 0.120 | False | False |
| 806 | 1.73 / 1.97 | 0.29 / 0.35 | 0.0035 / 0.0033 | 0.41 | 0.118 / 0.123 | False | False |
| 807 | 1.89 / 1.53 | 0.33 / 0.30 | 0.0038 / 0.0037 | 0.39 | 0.145 / 0.154 | False | False |
| 808 | 2.31 / 1.84 | 0.38 / 0.33 | 0.0047 / 0.0043 | 0.35 | 0.099 / 0.110 | False | False |
