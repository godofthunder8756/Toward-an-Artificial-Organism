# Track C swap option R2: replication of derived against paid, with a relocation control

Seeds 28. No-fate task accuracy 0.999 (learned: True). Regulators: derived 28, paid 27, paid with own relocation 27, yoked 0. Usable pairs (both regulate, in band within 0.1): derived/paid **23**, PAIDR/paid 21, derived/PAIDR 22.

| arm | in band | rho | eat timing ratio | task accuracy | relocations | first sustained in band (episode) |
| --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 0.916 | 4.17 | 52.4 | 0.983 | 1309394 | 132 |
| YOKED | 0.315 | 1.40 | 1.0 | 0.981 | 1309642 | n/a |
| PAID | 0.920 | 4.14 | 29.6 | 0.983 | 1308741 | 154 |
| PAIDR | 0.911 | 4.09 | 30.0 | 0.983 | 1312062 | 156 |

**C0 (derived regulation, independent optimizers): HOLDS.** Derived regulators 28/28 (needed 19); yoked regulators 0 (at most 1).

## Claims

| comparison (first against second) | label | first ahead | sign p | Wilcoxon p | first median | second median |
| --- | --- | --- | --- | --- | --- | --- |
| **C1 (primary)** anticipation index, derived against paid | **NOT_REPLICATED** | 12/17 | 0.1435 | 0.2633 | 0.557 | 0.490 |
| **C3** combined post-meal suppression K, derived against paid | **DERIVED_AHEAD** | 21/23 | 0.0001 | 0.0000 | 0.894 | 0.650 |
| C4a K, PAIDR against paid | **NO_DIFFERENCE_DETECTED** | 12/21 | 0.6636 | 0.6578 | 0.634 | 0.637 |
| C4b K, derived against PAIDR | **DERIVED_AHEAD** | 20/22 | 0.0001 | 0.0000 | 0.890 | 0.622 |

**C4 (relocation control): RELOCATION_NOT_SUFFICIENT.**

| flat eat readiness (first against second) | label | first | second | Fisher p |
| --- | --- | --- | --- | --- |
| **C2** derived against paid | **DERIVED_MORE_FLAT** | 11/27 | 1/27 | 0.0022 |
| PAIDR against paid | **NO_DIFFERENCE_DETECTED** | 1/26 | 1/26 | 1.0000 |
| derived against PAIDR | **DERIVED_MORE_FLAT** | 10/26 | 1/26 | 0.0048 |

Holm-adjusted p over C1, C2, C3: C1 0.1435, C2 0.0043, C3 0.0002.

## Secondary (labels are descriptive)

| comparison (first against second) | label | first ahead | sign p | Wilcoxon p | first median | second median |
| --- | --- | --- | --- | --- | --- | --- |
| S, derived against paid | **NO_DIFFERENCE_DETECTED** | 14/23 | 0.4049 | 0.4820 | 0.661 | 0.588 |
| M, derived against paid | **NO_DIFFERENCE_DETECTED** | 15/23 | 0.2100 | 0.0196 | 0.420 | 0.229 |
| R2(h -> E), derived against paid | **NO_DIFFERENCE_DETECTED** | 14/23 | 0.4049 | 0.2345 | 0.823 | 0.713 |
| anticipation, all seeds where both regulate | **NO_DIFFERENCE_DETECTED** | 15/21 | 0.0784 | 0.1281 | 0.557 | 0.509 |
| K, all seeds where both regulate | **DERIVED_AHEAD** | 25/27 | 0.0000 | 0.0000 | 0.914 | 0.642 |
| anticipation, PAIDR against paid | **PAID_AHEAD** | 4/19 | 0.0192 | 0.0028 | 0.383 | 0.511 |
| anticipation, derived against PAIDR | **DERIVED_AHEAD** | 14/18 | 0.0309 | 0.0120 | 0.558 | 0.394 |

Decoder failures (held-out R2(h -> D) below -0.1): DERIVED 5, YOKED 0, PAID 3, PAIDR 0.

## Descriptive (all seeds, erasure off)

| arm | anticipation | S | M | K | R2(h -> E) | flat | in band | regulating intact / shuffled |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 0.557 | 0.700 | 0.451 | 0.905 | 0.825 | 11 | 0.920 | 28 / 0 |
| YOKED | 0.007 | 0.011 | -0.022 | -0.008 | 0.920 | 0 | 0.292 | 0 / 0 |
| PAID | 0.511 | 0.504 | 0.231 | 0.640 | 0.710 | 1 | 0.924 | 27 / 0 |
| PAIDR | 0.384 | 0.513 | 0.208 | 0.657 | 0.847 | 1 | 0.891 | 26 / 0 |

## Per seed (stage 1)

| seed | in band derived / paid / PAIDR / yoked | regulator derived / paid / PAIDR | usable D-P / R-P / D-R |
| --- | --- | --- | --- |
| 1000 | 0.89 / 0.94 / 0.91 / 0.32 | y / y / y | y / y / y |
| 1001 | 0.96 / 0.91 / 0.91 / 0.25 | y / y / y | y / y / y |
| 1002 | 0.95 / 0.95 / 0.77 / 0.35 | y / y / y | y / n / n |
| 1003 | 0.91 / 0.83 / 0.93 / 0.34 | y / y / y | y / y / y |
| 1004 | 0.88 / 0.93 / 0.91 / 0.27 | y / y / y | y / y / y |
| 1005 | 0.92 / 0.97 / 0.83 / 0.35 | y / y / y | y / n / y |
| 1006 | 0.95 / 0.95 / 0.95 / 0.34 | y / y / y | y / y / y |
| 1007 | 0.91 / 0.93 / 0.92 / 0.26 | y / y / y | y / y / y |
| 1008 | 0.88 / 0.90 / 0.84 / 0.30 | y / y / y | y / y / y |
| 1009 | 0.96 / 0.87 / 0.95 / 0.33 | y / y / y | y / y / y |
| 1010 | 0.80 / 0.91 / 0.90 / 0.38 | y / y / y | n / y / n |
| 1011 | 0.68 / 0.95 / 0.90 / 0.36 | y / y / y | n / y / n |
| 1012 | 0.97 / 0.84 / 0.95 / 0.31 | y / y / y | n / n / y |
| 1013 | 0.94 / 0.93 / 0.94 / 0.29 | y / y / y | y / y / y |
| 1014 | 0.93 / 0.86 / 0.76 / 0.34 | y / y / y | y / n / n |
| 1015 | 0.91 / 0.88 / 0.90 / 0.28 | y / y / y | y / y / y |
| 1016 | 0.88 / 0.94 / 0.92 / 0.29 | y / y / y | y / y / y |
| 1017 | 0.91 / 0.95 / 0.94 / 0.33 | y / y / y | y / y / y |
| 1018 | 0.61 / 0.90 / 0.82 / 0.37 | y / y / y | n / y / n |
| 1019 | 0.96 / 0.47 / 0.90 / 0.28 | y / n / y | n / n / y |
| 1020 | 0.91 / 0.92 / 0.91 / 0.24 | y / y / y | y / y / y |
| 1021 | 0.95 / 0.91 / 0.52 / 0.27 | y / y / n | y / n / n |
| 1022 | 0.95 / 0.86 / 0.92 / 0.30 | y / y / y | y / y / y |
| 1023 | 0.93 / 0.91 / 0.93 / 0.31 | y / y / y | y / y / y |
| 1024 | 0.94 / 0.97 / 0.92 / 0.32 | y / y / y | y / y / y |
| 1025 | 0.91 / 0.90 / 0.89 / 0.39 | y / y / y | y / y / y |
| 1026 | 0.92 / 0.97 / 0.92 / 0.36 | y / y / y | y / y / y |
| 1027 | 0.84 / 0.93 / 0.82 / 0.29 | y / y / y | y / n / y |
