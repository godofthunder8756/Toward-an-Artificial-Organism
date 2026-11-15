# Track C swap, generality: derived against paid regulators in two new cells

**Overall: HOLDS_IN_H128_ONLY.** H128 DERIVED_AHEAD; B2 NO_DIFFERENCE_DETECTED. Holm-adjusted p: H128 0.0293, B2 0.1078.

## Cell H128 (128 units, 1 body variable)

Seeds 28. No-fate task accuracy 1.000 (learned: True). Regulators: DERIVED 28, YOKED 0, PAID 28. Usable pairs (both regulate, in band within 0.1): 25.

| arm | in band | in band, each variable | rho | eat timing ratio | task accuracy | relocations | first sustained in band (episode) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 0.947 | n/a | 4.09 | 63.0 | 0.990 | 817538 | 88 |
| YOKED | 0.283 | n/a | 1.15 | 1.0 | 0.989 | 817042 | n/a |
| PAID | 0.944 | n/a | 4.12 | 59.7 | 0.989 | 817468 | 100 |

**G0 (derived regulation): HOLDS.** Derived regulators 28/28 (needed 19); yoked regulators 0 (at most 1).

Derived reached sustained regulation sooner than paid in 22/27 (p 0.0015).

| comparison (derived against paid) | label | derived ahead | sign p | Wilcoxon p | derived median | paid median | median difference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **G1** K, usable pairs | **DERIVED_AHEAD** | 19/25 | 0.0146 | 0.0009 | 0.909 | 0.773 | 0.125 |
| K, all seeds (no matching) | **DERIVED_AHEAD** | 22/28 | 0.0037 | 0.0003 | 0.912 | 0.790 | 0.125 |
| K, pairs within 0.05 | **DERIVED_AHEAD** | 15/20 | 0.0414 | 0.0027 | 0.912 | 0.790 | 0.126 |
| S | **DERIVED_AHEAD** | 18/25 | 0.0433 | 0.1563 | 0.878 | 0.678 | 0.087 |
| M | **NO_DIFFERENCE_DETECTED** | 17/25 | 0.1078 | 0.0136 | 0.287 | 0.166 | 0.092 |

Flat eat readiness: derived 4/28, paid 0/28 (Fisher p 0.1115). In-band difference within usable pairs (median, derived minus paid): -0.003. Rank correlation of K with in-band time: derived 0.39, paid 0.28.

| arm (all seeds, erasure off) | K | K below 0.5 | K each variable | S | M | K from the other variable's meals | flat | in band | regulating |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 0.912 | 0 | 0.912 | 0.887 | 0.282 | n/a | 4 | 0.950 | 28 |
| YOKED | -0.030 | 28 | -0.030 | 0.004 | -0.024 | n/a | 0 | 0.282 | 0 |
| PAID | 0.790 | 1 | 0.790 | 0.685 | 0.180 | n/a | 0 | 0.943 | 28 |

| seed | in band DERIVED / YOKED / PAID | regulator DERIVED / PAID | usable | within 0.05 |
| --- | --- | --- | --- | --- |
| 1300 | 0.85 / 0.32 / 0.95 | y / y | y | n |
| 1301 | 0.94 / 0.33 / 0.98 | y / y | y | y |
| 1302 | 0.94 / 0.26 / 0.96 | y / y | y | y |
| 1303 | 0.94 / 0.28 / 0.93 | y / y | y | y |
| 1304 | 0.97 / 0.27 / 0.97 | y / y | y | y |
| 1305 | 0.96 / 0.23 / 0.97 | y / y | y | y |
| 1306 | 0.96 / 0.24 / 0.95 | y / y | y | y |
| 1307 | 0.96 / 0.33 / 0.96 | y / y | y | y |
| 1308 | 0.95 / 0.31 / 0.92 | y / y | y | y |
| 1309 | 0.91 / 0.21 / 0.95 | y / y | y | y |
| 1310 | 0.95 / 0.28 / 0.93 | y / y | y | y |
| 1311 | 0.95 / 0.21 / 0.95 | y / y | y | y |
| 1312 | 0.82 / 0.29 / 0.89 | y / y | y | n |
| 1313 | 0.91 / 0.27 / 0.94 | y / y | y | y |
| 1314 | 0.96 / 0.24 / 0.96 | y / y | y | y |
| 1315 | 0.95 / 0.32 / 0.86 | y / y | y | n |
| 1316 | 0.97 / 0.32 / 0.94 | y / y | y | y |
| 1317 | 0.92 / 0.31 / 0.96 | y / y | y | y |
| 1318 | 0.96 / 0.29 / 0.89 | y / y | y | n |
| 1319 | 0.96 / 0.29 / 0.92 | y / y | y | y |
| 1320 | 0.96 / 0.32 / 0.79 | y / y | n | n |
| 1321 | 0.75 / 0.25 / 0.94 | y / y | n | n |
| 1322 | 0.97 / 0.27 / 0.81 | y / y | n | n |
| 1323 | 0.96 / 0.38 / 0.94 | y / y | y | y |
| 1324 | 0.95 / 0.26 / 0.96 | y / y | y | y |
| 1325 | 0.88 / 0.28 / 0.88 | y / y | y | y |
| 1326 | 0.95 / 0.25 / 0.95 | y / y | y | y |
| 1327 | 0.92 / 0.32 / 0.98 | y / y | y | n |

## Cell B2 (64 units, 2 body variables)

Seeds 28. No-fate task accuracy 0.999 (learned: True). Regulators: DERIVED 28, YOKED 0, PAID 28. Usable pairs (both regulate, in band within 0.1): 25.

| arm | in band | in band, each variable | rho | eat timing ratio | task accuracy | relocations | first sustained in band (episode) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 0.866 | 0.930 / 0.932 | 8.18 | 38.5 | 0.970 | 7604408 | 625 |
| YOKED | 0.176 | 0.308 / 0.312 | 3.20 | 1.0 | 0.971 | 7608414 | n/a |
| PAID | 0.867 | 0.931 / 0.933 | 8.09 | 40.7 | 0.969 | 7606400 | 454 |

**G0 (derived regulation): HOLDS.** Derived regulators 28/28 (needed 19); yoked regulators 0 (at most 1).

Derived reached sustained regulation sooner than paid in 0/28 (p 0.0000).

| comparison (derived against paid) | label | derived ahead | sign p | Wilcoxon p | derived median | paid median | median difference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **G1** K, usable pairs | **NO_DIFFERENCE_DETECTED** | 8/25 | 0.1078 | 0.1485 | 0.853 | 0.883 | -0.030 |
| K, all seeds (no matching) | **PAID_AHEAD** | 8/28 | 0.0357 | 0.0426 | 0.844 | 0.896 | -0.039 |
| K, pairs within 0.05 | **NO_DIFFERENCE_DETECTED** | 7/22 | 0.1338 | 0.0684 | 0.848 | 0.889 | -0.039 |
| K, variable 0 | **NO_DIFFERENCE_DETECTED** | 8/25 | 0.1078 | 0.1817 | 0.862 | 0.883 | -0.026 |
| K, variable 1 | **NO_DIFFERENCE_DETECTED** | 9/25 | 0.2295 | 0.0903 | 0.870 | 0.901 | -0.035 |
| S | **NO_DIFFERENCE_DETECTED** | 11/25 | 0.6900 | 0.3388 | 0.788 | 0.820 | -0.056 |
| M | **NO_DIFFERENCE_DETECTED** | 13/25 | 1.0000 | 0.7510 | 0.320 | 0.291 | 0.012 |
| K from the other variable's meals | **PAID_AHEAD** | 5/25 | 0.0041 | 0.0031 | 0.665 | 0.788 | -0.131 |

Flat eat readiness: derived 0/28, paid 0/28 (Fisher p 1.0000). In-band difference within usable pairs (median, derived minus paid): 0.003. Rank correlation of K with in-band time: derived 0.37, paid 0.36.

| arm (all seeds, erasure off) | K | K below 0.5 | K each variable | S | M | K from the other variable's meals | flat | in band | regulating |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 0.844 | 0 | 0.853 / 0.862 | 0.777 | 0.275 | 0.652 | 0 | 0.838 | 28 |
| YOKED | -0.000 | 28 | 0.003 / -0.004 | 0.010 | -0.007 | 0.004 | 0 | 0.177 | 0 |
| PAID | 0.896 | 0 | 0.886 / 0.903 | 0.864 | 0.304 | 0.792 | 0 | 0.870 | 28 |

| seed | in band DERIVED / YOKED / PAID | regulator DERIVED / PAID | usable | within 0.05 |
| --- | --- | --- | --- | --- |
| 1400 | 0.86 / 0.15 / 0.88 | y / y | y | y |
| 1401 | 0.88 / 0.17 / 0.89 | y / y | y | y |
| 1402 | 0.88 / 0.17 / 0.82 | y / y | y | n |
| 1403 | 0.70 / 0.16 / 0.78 | y / y | y | n |
| 1404 | 0.87 / 0.17 / 0.89 | y / y | y | y |
| 1405 | 0.89 / 0.16 / 0.86 | y / y | y | y |
| 1406 | 0.90 / 0.17 / 0.87 | y / y | y | y |
| 1407 | 0.87 / 0.20 / 0.83 | y / y | y | y |
| 1408 | 0.86 / 0.19 / 0.87 | y / y | y | y |
| 1409 | 0.91 / 0.16 / 0.91 | y / y | y | y |
| 1410 | 0.89 / 0.18 / 0.89 | y / y | y | y |
| 1411 | 0.92 / 0.17 / 0.84 | y / y | y | n |
| 1412 | 0.73 / 0.21 / 0.86 | y / y | n | n |
| 1413 | 0.86 / 0.19 / 0.84 | y / y | y | y |
| 1414 | 0.86 / 0.16 / 0.87 | y / y | y | y |
| 1415 | 0.87 / 0.21 / 0.91 | y / y | y | y |
| 1416 | 0.86 / 0.22 / 0.86 | y / y | y | y |
| 1417 | 0.86 / 0.16 / 0.84 | y / y | y | y |
| 1418 | 0.86 / 0.19 / 0.87 | y / y | y | y |
| 1419 | 0.88 / 0.22 / 0.89 | y / y | y | y |
| 1420 | 0.87 / 0.18 / 0.84 | y / y | y | y |
| 1421 | 0.80 / 0.16 / 0.77 | y / y | y | y |
| 1422 | 0.89 / 0.17 / 0.92 | y / y | y | y |
| 1423 | 0.81 / 0.18 / 0.91 | y / y | n | n |
| 1424 | 0.74 / 0.18 / 0.87 | y / y | n | n |
| 1425 | 0.85 / 0.18 / 0.84 | y / y | y | y |
| 1426 | 0.88 / 0.20 / 0.90 | y / y | y | y |
| 1427 | 0.88 / 0.22 / 0.88 | y / y | y | y |
