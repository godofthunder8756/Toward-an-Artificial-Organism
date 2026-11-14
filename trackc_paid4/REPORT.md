# Track C swap option R4: a paid agent with undisturbed memory, and a derived agent with added replayed erasures

Seeds 28. No-fate task accuracy 0.998 (learned: True). Regulators: DERIVED 28, YOKED 0, PAID 28, PAID0 26, DNOISE 28. Usable pairs (both regulate, in band within 0.1): DERIVED/PAID 25, PAID0/PAID 20, DERIVED/PAID0 19, DNOISE/PAID 16, DERIVED/DNOISE 18.

| arm | in band | rho | eat timing ratio | task accuracy | relocations | first sustained in band (episode) |
| --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 0.933 | 4.14 | 48.4 | 0.986 | 1314569 | 146 |
| YOKED | 0.289 | 1.16 | 1.0 | 0.985 | 1314389 | n/a |
| PAID | 0.929 | 4.15 | 22.9 | 0.985 | 1312951 | 150 |
| PAID0 | 0.912 | 4.10 | 22.7 | 1.000 | 0 | 122 |
| DNOISE | 0.832 | 3.97 | 15.9 | 0.940 | 3257200 | 226 |

**F0 (derived regulation): HOLDS.** Derived regulators 28/28 (needed 19); yoked regulators 0 (at most 1).

Sustained regulation reached sooner than PAID: DERIVED 18/28 (p 0.1849); PAID0 19/27 (p 0.0522); DNOISE 0/28 (p 0.0000).

## Claims (combined post-meal suppression K)

| comparison (first against second) | label | first ahead | sign p | Wilcoxon p | first median | second median |
| --- | --- | --- | --- | --- | --- | --- |
| **F1 (check)** derived against paid | **DERIVED_AHEAD** | 22/25 | 0.0002 | 0.0000 | 0.879 | 0.533 |
| **F2a** PAID0 against paid | **NO_DIFFERENCE_DETECTED** | 6/20 | 0.1153 | 0.1140 | 0.372 | 0.528 |
| **F2b** derived against PAID0 | **DERIVED_AHEAD** | 17/19 | 0.0007 | 0.0001 | 0.877 | 0.395 |
| **F3a** DNOISE against paid | **NO_DIFFERENCE_DETECTED** | 9/16 | 0.8036 | 0.5619 | 0.708 | 0.630 |
| **F3b** derived against DNOISE | **DERIVED_AHEAD** | 14/18 | 0.0309 | 0.0077 | 0.889 | 0.609 |

**F2 (primary; paid with undisturbed memory): REPLAY_DOES_NOT_EXPLAIN.** Share of the derived/paid gap in median K closed by PAID0: -0.30.

**F3 (derived with added replayed erasures): REPLAY_REMOVES.** Share of the gap kept by DNOISE: 0.10.

F2 and F3 are read: True (F1 must be DERIVED_AHEAD).

Holm-adjusted p over the four tests of F2 and F3: paid0_vs_paid 0.2306, derived_vs_paid0 0.0029, dnoise_vs_paid 0.8036, derived_vs_dnoise 0.0927.

## Secondary (labels are descriptive)

| flat eat readiness (first against second) | label | first | second | Fisher p |
| --- | --- | --- | --- | --- |
| derived against paid | **NO_DIFFERENCE_DETECTED** | 4/28 | 1/28 | 0.3516 |
| PAID0 against paid | **NO_DIFFERENCE_DETECTED** | 6/26 | 1/26 | 0.0993 |
| derived against PAID0 | **NO_DIFFERENCE_DETECTED** | 4/26 | 6/26 | 0.7265 |
| DNOISE against paid | **NO_DIFFERENCE_DETECTED** | 1/28 | 1/28 | 1.0000 |
| derived against DNOISE | **NO_DIFFERENCE_DETECTED** | 4/28 | 1/28 | 0.3516 |

| comparison (first against second) | label | first ahead | sign p | Wilcoxon p | first median | second median |
| --- | --- | --- | --- | --- | --- | --- |
| anticipation, derived against paid | **NO_DIFFERENCE_DETECTED** | 10/19 | 1.0000 | 0.4413 | 0.456 | 0.497 |
| anticipation, PAID0 against paid | **NO_DIFFERENCE_DETECTED** | 10/18 | 0.8145 | 0.4951 | 0.502 | 0.468 |
| anticipation, derived against PAID0 | **NO_DIFFERENCE_DETECTED** | 5/16 | 0.2101 | 0.2522 | 0.462 | 0.521 |
| anticipation, DNOISE against paid | **NO_DIFFERENCE_DETECTED** | 5/16 | 0.2101 | 0.0335 | 0.433 | 0.517 |
| anticipation, derived against DNOISE | **NO_DIFFERENCE_DETECTED** | 9/16 | 0.8036 | 0.8999 | 0.419 | 0.451 |
| S, derived against paid | **DERIVED_AHEAD** | 21/25 | 0.0009 | 0.0002 | 0.811 | 0.433 |
| M, derived against paid | **NO_DIFFERENCE_DETECTED** | 16/25 | 0.2295 | 0.0318 | 0.285 | 0.224 |
| S, PAID0 against paid | **NO_DIFFERENCE_DETECTED** | 6/20 | 0.1153 | 0.0037 | 0.045 | 0.447 |
| M, PAID0 against paid | **NO_DIFFERENCE_DETECTED** | 10/20 | 1.0000 | 0.1893 | 0.258 | 0.199 |
| S, derived against PAID0 | **DERIVED_AHEAD** | 18/19 | 0.0001 | 0.0000 | 0.774 | 0.031 |
| M, derived against PAID0 | **NO_DIFFERENCE_DETECTED** | 9/19 | 1.0000 | 0.7086 | 0.263 | 0.391 |
| S, derived against DNOISE | **DERIVED_AHEAD** | 14/18 | 0.0309 | 0.0139 | 0.814 | 0.570 |
| M, derived against DNOISE | **NO_DIFFERENCE_DETECTED** | 13/18 | 0.0963 | 0.0342 | 0.274 | 0.161 |

Decoder failures (held-out R2(h -> D) below -0.1): DERIVED 4, YOKED 0, PAID 2, PAID0 0, DNOISE 1.

## Descriptive (all seeds, erasure off)

| arm | anticipation | S | M | K | R2(h -> E) | flat | in band | regulating intact / shuffled |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 0.449 | 0.801 | 0.263 | 0.877 | 0.784 | 4 | 0.921 | 28 / 0 |
| YOKED | 0.007 | 0.009 | -0.040 | -0.016 | 0.930 | 0 | 0.276 | 0 / 0 |
| PAID | 0.488 | 0.429 | 0.214 | 0.528 | 0.705 | 1 | 0.931 | 28 / 0 |
| PAID0 | 0.450 | 0.032 | 0.258 | 0.356 | 0.626 | 6 | 0.908 | 27 / 0 |
| DNOISE | 0.445 | 0.522 | 0.133 | 0.563 | 0.939 | 1 | 0.738 | 22 / 0 |

## Per seed (stage 1)

| seed | in band DERIVED / YOKED / PAID / PAID0 / DNOISE | regulator DERIVED / PAID / PAID0 / DNOISE | usable D_P / Z_P / D_Z / N_P / D_N |
| --- | --- | --- | --- |
| 1200 | 0.93 / 0.29 / 0.96 / 0.90 / 0.87 | y / y / y / y | y / y / y / y / y |
| 1201 | 0.93 / 0.38 / 0.97 / 0.95 / 0.93 | y / y / y / y | y / y / y / y / y |
| 1202 | 0.86 / 0.30 / 0.95 / 0.96 / 0.87 | y / y / y / y | y / y / n / y / y |
| 1203 | 0.92 / 0.28 / 0.93 / 0.93 / 0.72 | y / y / y / y | y / y / y / n / n |
| 1204 | 0.96 / 0.31 / 0.95 / 0.93 / 0.75 | y / y / y / y | y / y / y / n / n |
| 1205 | 0.89 / 0.23 / 0.82 / 0.92 / 0.89 | y / y / y / y | y / n / y / y / y |
| 1206 | 0.92 / 0.29 / 0.92 / 0.94 / 0.85 | y / y / y / y | y / y / y / y / y |
| 1207 | 0.96 / 0.27 / 0.91 / 0.55 / 0.96 | y / y / n / y | y / n / n / y / y |
| 1208 | 0.96 / 0.30 / 0.92 / 0.76 / 0.91 | y / y / y / y | y / n / n / y / y |
| 1209 | 0.93 / 0.28 / 0.93 / 0.86 / 0.75 | y / y / y / y | y / y / y / n / n |
| 1210 | 0.84 / 0.24 / 0.81 / 0.94 / 0.75 | y / y / y / y | y / n / n / y / y |
| 1211 | 0.91 / 0.27 / 0.89 / 0.83 / 0.81 | y / y / y / y | y / y / y / y / y |
| 1212 | 0.94 / 0.23 / 0.94 / 0.92 / 0.90 | y / y / y / y | y / y / y / y / y |
| 1213 | 0.96 / 0.36 / 0.85 / 0.76 / 0.82 | y / y / y / y | n / y / n / y / n |
| 1214 | 0.93 / 0.31 / 0.66 / 0.91 / 0.80 | y / y / y / y | n / n / y / n / n |
| 1215 | 0.89 / 0.40 / 0.93 / 0.88 / 0.77 | y / y / y / y | y / y / y / n / n |
| 1216 | 0.97 / 0.28 / 0.94 / 0.65 / 0.90 | y / y / y / y | y / n / n / y / y |
| 1217 | 0.93 / 0.29 / 0.94 / 0.87 / 0.84 | y / y / y / y | y / y / y / y / y |
| 1218 | 0.94 / 0.28 / 0.90 / 0.59 / 0.89 | y / y / n / y | y / n / n / y / y |
| 1219 | 0.94 / 0.30 / 0.95 / 0.90 / 0.87 | y / y / y / y | y / y / y / y / y |
| 1220 | 0.91 / 0.35 / 0.93 / 0.92 / 0.83 | y / y / y / y | y / y / y / n / y |
| 1221 | 0.81 / 0.29 / 0.93 / 0.96 / 0.75 | y / y / y / y | n / y / n / n / y |
| 1222 | 0.94 / 0.35 / 0.94 / 0.93 / 0.84 | y / y / y / y | y / y / y / n / n |
| 1223 | 0.96 / 0.29 / 0.89 / 0.92 / 0.94 | y / y / y / y | y / y / y / y / y |
| 1224 | 0.94 / 0.25 / 0.94 / 0.90 / 0.82 | y / y / y / y | y / y / y / n / n |
| 1225 | 0.89 / 0.29 / 0.92 / 0.91 / 0.81 | y / y / y / y | y / y / y / n / y |
| 1226 | 0.96 / 0.34 / 0.94 / 0.79 / 0.79 | y / y / y / y | y / n / n / n / n |
| 1227 | 0.97 / 0.40 / 0.93 / 0.93 / 0.82 | y / y / y / y | y / y / y / n / n |
