# Track C swap option R: derived against paid regulators

Seeds 18. No-fate task accuracy 0.999 (learned: True). Regulators: derived 18, paid 18, yoked 0; both 18; **usable (both regulate, in band within 0.1) 16**.

| arm | in band | rho | eat timing ratio | task accuracy | mean erasure gain |
| --- | --- | --- | --- | --- | --- |
| DERIVED | 0.920 | 4.19 | 28.1 | 0.981 | 0.025 |
| YOKED | 0.319 | 1.56 | 1.0 | 0.981 | 0.025 |
| PAID | 0.918 | 4.08 | 27.3 | 0.983 | 0.025 |

**R0 (derived regulation with independent optimizers): HOLDS.** Derived regulators 18/18 (needed 12); yoked regulators 0 (at most 1); derived more in band than yoked in 18/18.

## Claims (usable seeds, derived against paid)

| claim | label | derived ahead | sign p (two-sided) | derived median | paid median |
| --- | --- | --- | --- | --- | --- |
| R1 anticipation in the state | **DERIVED_AHEAD** | 13/16 | 0.0213 | 0.648 | 0.467 |
| R2 post-meal suppression | **NO_DIFFERENCE_DETECTED** | 12/16 | 0.0768 | 0.490 | 0.158 |
| R3 robustness to world shifts | **NO_DIFFERENCE_DETECTED** | 7/16 | 0.8036 | 0.965 | 0.964 |

**R4 withdrawal: BOTH_FOLLOW_THEIR_GROUND.** In band at least 0.05 below the keep arm: derived (dependence removed) 16/16, median change -0.566; paid (payment removed) 16/16, median change -0.458.

| arm after withdrawal stage | in band (median) | regulating |
| --- | --- | --- |
| DKEEP | 0.948 | 16/16 |
| DCUT | 0.329 | 0/16 |
| PKEEP | 0.939 | 16/16 |
| PCUT | 0.501 | 2/16 |

## Descriptive (usable seeds, erasure off)

| arm | retention | R2(h -> E) | anticipation | S | robustness | in band base | bolus_0.10 | wear_x2 | delay_10 | noise_0.05 | regulating intact / shuffled | eats |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 1.112 | 0.755 | 0.648 | 0.490 | 0.965 | 0.933 | 0.951 | 0.860 | 0.898 | 0.914 | 16 / 0 | 2092 |
| PAID | 1.092 | 0.693 | 0.467 | 0.158 | 0.964 | 0.919 | 0.938 | 0.862 | 0.868 | 0.908 | 16 / 0 | 2096 |
| YOKED | 0.940 | 0.918 | 0.006 | 0.014 | 0.820 | 0.308 | 0.253 | 0.136 | 0.297 | 0.307 | 0 / 0 | 694 |

## Per seed (stage 1)

| seed | in band derived / paid / yoked | rho derived / paid / yoked | derived reg | paid reg | usable |
| --- | --- | --- | --- | --- | --- |
| 900 | 0.96 / 0.94 / 0.34 | 4.11 / 4.03 / 1.63 | True | True | True |
| 901 | 0.91 / 0.81 / 0.32 | 4.21 / 3.85 / 1.75 | True | True | False |
| 902 | 0.94 / 0.93 / 0.32 | 4.20 / 4.24 / 1.50 | True | True | True |
| 903 | 0.93 / 0.85 / 0.28 | 4.30 / 3.90 / 0.93 | True | True | True |
| 904 | 0.89 / 0.89 / 0.35 | 4.37 / 4.22 / 1.88 | True | True | True |
| 905 | 0.95 / 0.92 / 0.33 | 4.17 / 4.11 / 1.66 | True | True | True |
| 906 | 0.84 / 0.95 / 0.38 | 3.85 / 4.19 / 2.61 | True | True | False |
| 907 | 0.91 / 0.81 / 0.33 | 4.18 / 3.80 / 1.76 | True | True | True |
| 908 | 0.97 / 0.96 / 0.25 | 4.09 / 4.05 / 0.98 | True | True | True |
| 909 | 0.91 / 0.95 / 0.39 | 4.35 / 4.04 / 2.45 | True | True | True |
| 910 | 0.95 / 0.93 / 0.26 | 4.08 / 4.11 / 0.84 | True | True | True |
| 911 | 0.95 / 0.90 / 0.23 | 4.05 / 4.12 / 0.61 | True | True | True |
| 912 | 0.93 / 0.92 / 0.26 | 4.17 / 4.28 / 0.90 | True | True | True |
| 913 | 0.85 / 0.91 / 0.37 | 4.59 / 4.20 / 2.42 | True | True | True |
| 914 | 0.87 / 0.81 / 0.29 | 3.89 / 3.84 / 1.49 | True | True | True |
| 915 | 0.91 / 0.94 / 0.27 | 4.34 / 4.06 / 1.13 | True | True | True |
| 916 | 0.95 / 0.91 / 0.28 | 4.29 / 4.22 / 1.06 | True | True | True |
| 917 | 0.90 / 0.94 / 0.32 | 4.33 / 4.00 / 1.77 | True | True | True |
