# Track C swap option R3: a derived agent that is also paid, and a sparse payment

Seeds 28. No-fate task accuracy 0.999 (learned: True). Regulators: DERIVED 28, YOKED 0, PAID 28, DPAID 28, PAIDS 28. Usable pairs (both regulate, in band within 0.1): DERIVED/PAID 24, DPAID/PAID 23, DERIVED/DPAID 26, PAIDS/PAID 24, DERIVED/PAIDS 25. Sparse penalties charged in training (median): 1490442.

| arm | in band | rho | eat timing ratio | task accuracy | relocations | first sustained in band (episode) |
| --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 0.938 | 4.13 | 47.6 | 0.986 | 1230576 | 128 |
| YOKED | 0.295 | 1.21 | 0.9 | 0.985 | 1230032 | n/a |
| PAID | 0.921 | 4.08 | 24.2 | 0.985 | 1230098 | 160 |
| DPAID | 0.957 | 4.14 | 97.2 | 0.991 | 834368 | 79 |
| PAIDS | 0.924 | 4.10 | 24.8 | 0.985 | 1231179 | 162 |

**E0 (derived regulation): HOLDS.** Derived regulators 28/28 (needed 19); yoked regulators 0 (at most 1).

Sustained regulation reached sooner than PAID: DERIVED 23/28 (p 0.0009); DPAID 28/28 (p 0.0000); PAIDS 11/28 (p 0.3449).

## Claims (combined post-meal suppression K)

| comparison (first against second) | label | first ahead | sign p | Wilcoxon p | first median | second median |
| --- | --- | --- | --- | --- | --- | --- |
| **E1 (check)** derived against paid | **DERIVED_AHEAD** | 23/24 | 0.0000 | 0.0000 | 0.905 | 0.499 |
| **E2a** DPAID against paid | **DPAID_AHEAD** | 21/23 | 0.0001 | 0.0000 | 0.952 | 0.466 |
| **E2b** derived against DPAID | **NO_DIFFERENCE_DETECTED** | 8/26 | 0.0755 | 0.0140 | 0.905 | 0.955 |
| **E3a** PAIDS against paid | **NO_DIFFERENCE_DETECTED** | 14/24 | 0.5413 | 0.5088 | 0.487 | 0.499 |
| **E3b** derived against PAIDS | **DERIVED_AHEAD** | 20/25 | 0.0041 | 0.0000 | 0.903 | 0.490 |

**E2 (primary; dependence with payment): DEPENDENCE_SUFFICES.** Share of the derived/paid gap in median K closed by DPAID: 1.11.

**E3 (sparse payment): SPARSE_NOT_SUFFICIENT.** Share of the gap closed by PAIDS: 0.04.

E2 and E3 are read: True (E1 must be DERIVED_AHEAD).

Holm-adjusted p over the four tests of E2 and E3: dpaid_vs_paid 0.0003, derived_vs_dpaid 0.1510, paids_vs_paid 0.5413, derived_vs_paids 0.0122.

## Secondary (labels are descriptive)

| flat eat readiness (first against second) | label | first | second | Fisher p |
| --- | --- | --- | --- | --- |
| derived against paid | **DERIVED_MORE_FLAT** | 10/28 | 0/28 | 0.0007 |
| DPAID against paid | **DPAID_MORE_FLAT** | 14/28 | 0/28 | 0.0000 |
| derived against DPAID | **NO_DIFFERENCE_DETECTED** | 10/28 | 14/28 | 0.4182 |
| PAIDS against paid | **NO_DIFFERENCE_DETECTED** | 0/28 | 0/28 | 1.0000 |
| derived against PAIDS | **DERIVED_MORE_FLAT** | 10/28 | 0/28 | 0.0007 |

| comparison (first against second) | label | first ahead | sign p | Wilcoxon p | first median | second median |
| --- | --- | --- | --- | --- | --- | --- |
| anticipation, derived against paid | **NO_DIFFERENCE_DETECTED** | 13/18 | 0.0963 | 0.0814 | 0.573 | 0.465 |
| anticipation, DPAID against paid | **DPAID_AHEAD** | 14/16 | 0.0042 | 0.0002 | 0.730 | 0.473 |
| anticipation, derived against DPAID | **NO_DIFFERENCE_DETECTED** | 4/15 | 0.1185 | 0.0637 | 0.567 | 0.708 |
| anticipation, PAIDS against paid | **NO_DIFFERENCE_DETECTED** | 8/20 | 0.5034 | 0.3488 | 0.440 | 0.467 |
| anticipation, derived against PAIDS | **NO_DIFFERENCE_DETECTED** | 12/18 | 0.2379 | 0.0599 | 0.553 | 0.439 |
| S, derived against paid | **NO_DIFFERENCE_DETECTED** | 13/24 | 0.8388 | 0.2405 | 0.625 | 0.320 |
| M, derived against paid | **DERIVED_AHEAD** | 18/24 | 0.0227 | 0.0003 | 0.373 | 0.220 |
| S, DPAID against paid | **NO_DIFFERENCE_DETECTED** | 14/23 | 0.4049 | 0.4274 | 0.207 | 0.278 |
| M, DPAID against paid | **DPAID_AHEAD** | 22/23 | 0.0000 | 0.0000 | 0.777 | 0.229 |
| S, PAIDS against paid | **NO_DIFFERENCE_DETECTED** | 12/24 | 1.0000 | 0.8774 | 0.269 | 0.320 |
| M, PAIDS against paid | **NO_DIFFERENCE_DETECTED** | 14/24 | 0.5413 | 0.7257 | 0.234 | 0.220 |

Decoder failures (held-out R2(h -> D) below -0.1): DERIVED 7, YOKED 0, PAID 3, DPAID 5, PAIDS 1.

## Descriptive (all seeds, erasure off)

| arm | anticipation | S | M | K | R2(h -> E) | flat | in band | regulating intact / shuffled |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 0.556 | 0.744 | 0.373 | 0.905 | 0.783 | 10 | 0.933 | 28 / 0 |
| YOKED | 0.007 | 0.007 | -0.021 | -0.005 | 0.923 | 0 | 0.285 | 0 / 0 |
| PAID | 0.465 | 0.320 | 0.205 | 0.470 | 0.696 | 0 | 0.923 | 28 / 0 |
| DPAID | 0.708 | 0.147 | 0.888 | 0.952 | 0.804 | 14 | 0.958 | 28 / 0 |
| PAIDS | 0.442 | 0.315 | 0.234 | 0.487 | 0.694 | 0 | 0.926 | 28 / 0 |

## Per seed (stage 1)

| seed | in band DERIVED / YOKED / PAID / DPAID / PAIDS | regulator DERIVED / PAID / DPAID / PAIDS | usable D_P / X_P / D_X / S_P / D_S |
| --- | --- | --- | --- |
| 1100 | 0.94 / 0.30 / 0.94 / 0.78 / 0.93 | y / y / y / y | y / n / n / y / y |
| 1101 | 0.94 / 0.31 / 0.94 / 0.97 / 0.92 | y / y / y / y | y / y / y / y / y |
| 1102 | 0.92 / 0.30 / 0.89 / 0.95 / 0.91 | y / y / y / y | y / y / y / y / y |
| 1103 | 0.85 / 0.25 / 0.89 / 0.80 / 0.91 | y / y / y / y | y / y / y / y / y |
| 1104 | 0.92 / 0.31 / 0.88 / 0.93 / 0.92 | y / y / y / y | y / y / y / y / y |
| 1105 | 0.88 / 0.39 / 0.68 / 0.95 / 0.94 | y / y / y / y | n / n / y / n / y |
| 1106 | 0.87 / 0.26 / 0.91 / 0.96 / 0.92 | y / y / y / y | y / y / y / y / y |
| 1107 | 0.95 / 0.28 / 0.96 / 0.96 / 0.93 | y / y / y / y | y / y / y / y / y |
| 1108 | 0.93 / 0.26 / 0.91 / 0.93 / 0.92 | y / y / y / y | y / y / y / y / y |
| 1109 | 0.97 / 0.27 / 0.78 / 0.98 / 0.91 | y / y / y / y | n / n / y / n / y |
| 1110 | 0.92 / 0.30 / 0.93 / 0.91 / 0.67 | y / y / y / y | y / y / y / n / n |
| 1111 | 0.94 / 0.34 / 0.87 / 0.94 / 0.92 | y / y / y / y | y / y / y / y / y |
| 1112 | 0.96 / 0.32 / 0.95 / 0.94 / 0.92 | y / y / y / y | y / y / y / y / y |
| 1113 | 0.87 / 0.26 / 0.91 / 0.97 / 0.94 | y / y / y / y | y / y / y / y / y |
| 1114 | 0.86 / 0.32 / 0.90 / 0.96 / 0.92 | y / y / y / y | y / y / y / y / y |
| 1115 | 0.98 / 0.24 / 0.79 / 0.97 / 0.87 | y / y / y / y | n / n / y / y / n |
| 1116 | 0.94 / 0.33 / 0.91 / 0.98 / 0.93 | y / y / y / y | y / y / y / y / y |
| 1117 | 0.95 / 0.27 / 0.95 / 0.96 / 0.90 | y / y / y / y | y / y / y / y / y |
| 1118 | 0.93 / 0.28 / 0.93 / 0.98 / 0.90 | y / y / y / y | y / y / y / y / y |
| 1119 | 0.94 / 0.24 / 0.93 / 0.97 / 0.95 | y / y / y / y | y / y / y / y / y |
| 1120 | 0.95 / 0.37 / 0.97 / 0.95 / 0.96 | y / y / y / y | y / y / y / y / y |
| 1121 | 0.96 / 0.38 / 0.96 / 0.98 / 0.82 | y / y / y / y | y / y / y / n / n |
| 1122 | 0.98 / 0.26 / 0.95 / 0.98 / 0.95 | y / y / y / y | y / y / y / y / y |
| 1123 | 0.88 / 0.32 / 0.94 / 0.72 / 0.94 | y / y / y / y | y / n / n / y / y |
| 1124 | 0.96 / 0.29 / 0.94 / 0.93 / 0.94 | y / y / y / y | y / y / y / y / y |
| 1125 | 0.93 / 0.29 / 0.90 / 0.98 / 0.93 | y / y / y / y | y / y / y / y / y |
| 1126 | 0.97 / 0.27 / 0.84 / 0.94 / 0.90 | y / y / y / y | n / y / y / y / y |
| 1127 | 0.94 / 0.30 / 0.93 / 0.97 / 0.95 | y / y / y / y | y / y / y / y / y |
