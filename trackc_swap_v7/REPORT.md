# Track C swap v7 (option K step 2: erasure also relocates the agent): results

**K1 (SAT r = 0.3, >= 7/9 regulators, bypass closed, controls hold): SUPPORTED**

Paid regulator rho_paid = 3.82, in band 0.82; margin = 0.96. No-fate task accuracy 0.998; no-fate task agent rho 0.04. Learned: True. S4: True. Task load: 0.1: 0.305 (loaded); 0.3: 0.481 (loaded).

## Labels (M1 cells)

| cell | label | regulators (needed) | bypass closed | yoked regulators <= 1 | M0 regulators <= 1 |
| --- | --- | --- | --- | --- | --- |
| M1 SAT 0.1 | BYPASS_OPEN | 7/9 (5) | False (median full-erasure acc 0.692) | True (0) | None |
| M1 GRADED 0.1 | BYPASS_OPEN | 0/9 (5) | False (median full-erasure acc 0.692) | True (0) | None |
| M1 SAT 0.3 | EMERGES | 8/9 (7) | True (median full-erasure acc 0.517) | True (0) | True |
| M1 GRADED 0.3 | EMERGES | 6/9 (5) | True (median full-erasure acc 0.515) | True (0) | True |

## Cells (medians)

| cell | regulators fate / yoked | in band fate / yoked | fate more in band | rho fate / yoked | over margin | acc fate / yoked | acc full erasure fate / yoked | bypass seeds (> 0.85) | acc erasure off fate | Spearman(in band, full-erasure acc) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M1 SAT 0.1 | 7 / 0 | 0.65 / 0.43 | 9/9 | 4.10 / 2.70 | 6/9 | 0.940 / 0.935 | 0.692 / 0.695 | 0/9 | 0.999 | -0.17 |
| M1 GRADED 0.1 | 0 / 0 | 0.52 / 0.43 | 9/9 | 3.87 / 3.18 | 3/9 | 0.906 / 0.907 | 0.692 / 0.694 | 0/9 | 0.999 | 0.27 |
| M1 SAT 0.3 | 8 / 0 | 0.76 / 0.35 | 9/9 | 4.09 / 2.24 | 9/9 | 0.923 / 0.920 | 0.517 / 0.520 | 0/9 | 0.998 | -0.28 |
| M1 GRADED 0.3 | 6 / 0 | 0.66 / 0.44 | 9/9 | 4.00 / 2.84 | 5/9 | 0.830 / 0.828 | 0.515 / 0.522 | 0/9 | 0.998 | 0.48 |
| M0 SAT 0.3 | 0 / 0 | 0.29 / 0.29 | 5/9 | 1.71 / 1.56 | 0/9 | 0.129 / 0.136 | 0.128 / 0.134 | 0/9 | 0.127 | 0.38 |
| M0 GRADED 0.3 | 0 / 0 | 0.32 / 0.30 | 7/9 | 1.68 / 1.54 | 0/9 | 0.135 / 0.137 | 0.134 / 0.139 | 0/9 | 0.134 | 0.52 |

## Checkpoints (descriptive)

| cell | updates | fate regulators | in band fate | fate more in band | acc full erasure fate |
| --- | --- | --- | --- | --- | --- |
| M1 SAT 0.1 | 1200 | 0/9 | 0.43 | 9/9 | 0.690 |
| M1 SAT 0.1 | 2400 | 0/9 | 0.52 | 9/9 | 0.692 |
| M1 SAT 0.1 | final | 7/9 | 0.65 | 9/9 | 0.692 |
| M1 GRADED 0.1 | 1200 | 0/9 | 0.42 | 9/9 | 0.692 |
| M1 GRADED 0.1 | 2400 | 0/9 | 0.46 | 9/9 | 0.693 |
| M1 GRADED 0.1 | final | 0/9 | 0.52 | 9/9 | 0.692 |
| M1 SAT 0.3 | 1200 | 0/9 | 0.50 | 9/9 | 0.516 |
| M1 SAT 0.3 | 2400 | 0/9 | 0.56 | 9/9 | 0.519 |
| M1 SAT 0.3 | final | 8/9 | 0.76 | 9/9 | 0.517 |
| M1 GRADED 0.3 | 1200 | 0/9 | 0.45 | 9/9 | 0.516 |
| M1 GRADED 0.3 | 2400 | 0/9 | 0.49 | 9/9 | 0.519 |
| M1 GRADED 0.3 | final | 6/9 | 0.66 | 9/9 | 0.515 |
| M0 SAT 0.3 | 1200 | 0/9 | 0.31 | 3/9 | 0.140 |
| M0 SAT 0.3 | 2400 | 0/9 | 0.31 | 7/9 | 0.146 |
| M0 SAT 0.3 | final | 0/9 | 0.29 | 5/9 | 0.128 |
| M0 GRADED 0.3 | 1200 | 0/9 | 0.32 | 6/9 | 0.138 |
| M0 GRADED 0.3 | 2400 | 0/9 | 0.31 | 6/9 | 0.139 |
| M0 GRADED 0.3 | final | 0/9 | 0.32 | 7/9 | 0.134 |

## Per seed, M1 SAT 0.1

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 700 | 4.10 / 2.54 | 0.64 / 0.40 | 0.0116 / 0.0041 | 0.20 | 0.693 / 0.698 | True | False |
| 701 | 3.93 / 1.89 | 0.58 / 0.34 | 0.0095 / 0.0048 | 0.26 | 0.693 / 0.695 | False | False |
| 702 | 4.08 / 2.70 | 0.84 / 0.45 | 0.0138 / 0.0010 | 0.06 | 0.692 / 0.694 | True | False |
| 703 | 4.15 / 3.67 | 0.73 / 0.57 | 0.0130 / 0.0030 | 0.14 | 0.701 / 0.691 | True | False |
| 704 | 3.88 / 2.78 | 0.65 / 0.43 | 0.0098 / 0.0034 | 0.19 | 0.688 / 0.699 | True | False |
| 705 | 4.16 / 2.39 | 0.76 / 0.37 | 0.0132 / 0.0027 | 0.11 | 0.687 / 0.695 | True | False |
| 706 | 4.12 / 3.39 | 0.63 / 0.50 | 0.0103 / 0.0047 | 0.21 | 0.693 / 0.695 | False | False |
| 707 | 3.57 / 1.93 | 0.63 / 0.32 | 0.0084 / 0.0012 | 0.18 | 0.687 / 0.689 | True | False |
| 708 | 4.20 / 3.40 | 0.71 / 0.51 | 0.0122 / 0.0037 | 0.16 | 0.680 / 0.688 | True | False |

## Per seed, M1 GRADED 0.1

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 700 | 3.84 / 2.87 | 0.52 / 0.41 | 0.0090 / 0.0055 | 0.24 | 0.695 / 0.698 | False | False |
| 701 | 3.43 / 2.47 | 0.48 / 0.40 | 0.0076 / 0.0051 | 0.26 | 0.692 / 0.693 | False | False |
| 702 | 3.86 / 3.18 | 0.52 / 0.45 | 0.0090 / 0.0052 | 0.24 | 0.694 / 0.694 | False | False |
| 703 | 3.90 / 3.21 | 0.56 / 0.45 | 0.0096 / 0.0049 | 0.22 | 0.699 / 0.690 | False | False |
| 704 | 3.62 / 2.64 | 0.54 / 0.40 | 0.0084 / 0.0042 | 0.23 | 0.690 / 0.699 | False | False |
| 705 | 3.87 / 2.92 | 0.57 / 0.43 | 0.0097 / 0.0046 | 0.22 | 0.688 / 0.695 | False | False |
| 706 | 4.08 / 3.62 | 0.51 / 0.45 | 0.0091 / 0.0067 | 0.25 | 0.692 / 0.693 | False | False |
| 707 | 3.88 / 3.23 | 0.52 / 0.43 | 0.0090 / 0.0056 | 0.24 | 0.687 / 0.689 | False | False |
| 708 | 4.16 / 3.31 | 0.51 / 0.42 | 0.0097 / 0.0065 | 0.25 | 0.685 / 0.694 | False | False |

## Per seed, M1 SAT 0.3

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 700 | 4.02 / 2.12 | 0.75 / 0.33 | 0.0102 / 0.0026 | 0.11 | 0.516 / 0.519 | True | False |
| 701 | 4.57 / 2.98 | 0.64 / 0.41 | 0.0110 / 0.0063 | 0.22 | 0.523 / 0.519 | False | False |
| 702 | 4.10 / 2.25 | 0.81 / 0.37 | 0.0126 / 0.0015 | 0.08 | 0.517 / 0.520 | True | False |
| 703 | 3.99 / 2.24 | 0.73 / 0.35 | 0.0113 / 0.0030 | 0.14 | 0.523 / 0.519 | True | False |
| 704 | 4.16 / 2.72 | 0.82 / 0.39 | 0.0133 / 0.0019 | 0.08 | 0.525 / 0.530 | True | False |
| 705 | 3.92 / 2.16 | 0.83 / 0.32 | 0.0106 / 0.0008 | 0.06 | 0.516 / 0.524 | True | False |
| 706 | 4.09 / 2.95 | 0.81 / 0.44 | 0.0120 / 0.0016 | 0.09 | 0.515 / 0.528 | True | False |
| 707 | 4.08 / 1.77 | 0.67 / 0.28 | 0.0102 / 0.0038 | 0.18 | 0.520 / 0.514 | True | False |
| 708 | 4.41 / 2.05 | 0.76 / 0.29 | 0.0126 / 0.0037 | 0.13 | 0.513 / 0.521 | True | False |

## Per seed, M1 GRADED 0.3

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 700 | 4.00 / 2.41 | 0.66 / 0.38 | 0.0116 / 0.0034 | 0.17 | 0.513 / 0.520 | True | False |
| 701 | 4.05 / 2.83 | 0.71 / 0.44 | 0.0112 / 0.0029 | 0.16 | 0.518 / 0.524 | True | False |
| 702 | 4.20 / 2.72 | 0.59 / 0.40 | 0.0107 / 0.0052 | 0.21 | 0.514 / 0.522 | False | False |
| 703 | 3.79 / 2.84 | 0.70 / 0.40 | 0.0098 / 0.0018 | 0.16 | 0.522 / 0.518 | True | False |
| 704 | 3.97 / 3.05 | 0.68 / 0.50 | 0.0114 / 0.0031 | 0.17 | 0.524 / 0.528 | True | False |
| 705 | 3.98 / 3.16 | 0.65 / 0.50 | 0.0111 / 0.0035 | 0.18 | 0.513 / 0.526 | False | False |
| 706 | 4.14 / 3.14 | 0.61 / 0.46 | 0.0104 / 0.0050 | 0.20 | 0.520 / 0.522 | False | False |
| 707 | 4.13 / 2.38 | 0.61 / 0.36 | 0.0105 / 0.0048 | 0.20 | 0.514 / 0.513 | True | False |
| 708 | 4.00 / 3.16 | 0.68 / 0.48 | 0.0112 / 0.0027 | 0.17 | 0.515 / 0.519 | True | False |

## Per seed, M0 SAT 0.3

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 700 | 1.11 / 1.30 | 0.25 / 0.27 | 0.0022 / 0.0014 | 0.63 | 0.125 / 0.121 | False | False |
| 701 | 1.52 / 1.40 | 0.28 / 0.28 | 0.0031 / 0.0028 | 0.59 | 0.116 / 0.136 | False | False |
| 702 | 2.49 / 1.94 | 0.37 / 0.32 | 0.0050 / 0.0046 | 0.48 | 0.163 / 0.155 | False | False |
| 703 | 1.51 / 1.56 | 0.28 / 0.29 | 0.0030 / 0.0029 | 0.59 | 0.130 / 0.122 | False | False |
| 704 | 1.32 / 1.43 | 0.27 / 0.28 | 0.0027 / 0.0019 | 0.62 | 0.125 / 0.134 | False | False |
| 705 | 1.71 / 1.46 | 0.29 / 0.28 | 0.0035 / 0.0030 | 0.57 | 0.140 / 0.151 | False | False |
| 706 | 2.11 / 2.06 | 0.35 / 0.35 | 0.0044 / 0.0028 | 0.51 | 0.140 / 0.161 | False | False |
| 707 | 2.86 / 2.44 | 0.40 / 0.35 | 0.0059 / 0.0051 | 0.45 | 0.128 / 0.125 | False | False |
| 708 | 1.91 / 1.79 | 0.32 / 0.32 | 0.0038 / 0.0036 | 0.54 | 0.116 / 0.114 | False | False |

## Per seed, M0 GRADED 0.3

| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | acc full erasure fate / yoked | fate regulator | yoked regulator |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 700 | 1.56 / 1.25 | 0.30 / 0.28 | 0.0032 / 0.0026 | 0.41 | 0.121 / 0.119 | False | False |
| 701 | 1.05 / 1.26 | 0.24 / 0.27 | 0.0022 / 0.0009 | 0.47 | 0.122 / 0.133 | False | False |
| 702 | 2.12 / 1.82 | 0.35 / 0.32 | 0.0043 / 0.0038 | 0.36 | 0.155 / 0.147 | False | False |
| 703 | 1.68 / 1.54 | 0.32 / 0.29 | 0.0034 / 0.0033 | 0.40 | 0.134 / 0.127 | False | False |
| 704 | 1.30 / 1.35 | 0.27 / 0.27 | 0.0026 / 0.0020 | 0.45 | 0.116 / 0.129 | False | False |
| 705 | 1.50 / 1.52 | 0.29 / 0.30 | 0.0030 / 0.0027 | 0.42 | 0.151 / 0.164 | False | False |
| 706 | 2.17 / 1.88 | 0.37 / 0.33 | 0.0044 / 0.0041 | 0.35 | 0.131 / 0.139 | False | False |
| 707 | 2.41 / 2.18 | 0.39 / 0.33 | 0.0050 / 0.0041 | 0.34 | 0.146 / 0.152 | False | False |
| 708 | 1.96 / 1.87 | 0.34 / 0.34 | 0.0040 / 0.0032 | 0.37 | 0.144 / 0.144 | False | False |
