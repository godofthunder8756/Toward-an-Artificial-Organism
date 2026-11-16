# Track C swap, option T: training length in the base cell

**Overall: CLOSES.** T1 (at 3600) DERIVED_AHEAD; T2 (at 10800) NO_DIFFERENCE_DETECTED; T3 (change) NARROWS. Holm-adjusted p: T2 1.0000, T3 0.0000.

**T0 (derived regulation at the first and last point): HOLDS.** Derived regulators 28/28 then 28/28 (needed 19); yoked 0 then 0. Regulating at every point: DERIVED 28, YOKED 0, PAID 28.

| updates | regulators D / Y / P | usable | in band D / Y / P | K D / Y / P | K below 0.5 D / P | derived ahead | sign p | Wilcoxon p | median difference | interval | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3600 | 28 / 0 / 28 | 26 | 0.913 / 0.299 / 0.913 | 0.865 / -0.014 / 0.528 | 1 / 12 | 24/26 | 0.0000 | 0.0000 | 0.313 | 0.065 to 0.413 | DERIVED_AHEAD |
| 7200 | 28 / 0 / 28 | 25 | 0.953 / 0.309 / 0.960 | 0.918 / 0.001 / 0.887 | 1 / 2 | 16/25 | 0.2295 | 0.1135 | 0.036 | -0.008 to 0.076 | NO_DIFFERENCE_DETECTED |
| 10800 | 28 / 0 / 28 | 27 | 0.969 / 0.318 / 0.960 | 0.933 / 0.012 / 0.936 | 1 / 0 | 13/27 | 1.0000 | 0.6790 | -0.004 | -0.064 to 0.044 | NO_DIFFERENCE_DETECTED |

**T3 (change in the within-pair difference, 3600 to 10800): NARROWS.** Seeds usable at both points: 25. Smaller at the end in 24/25 (sign p 0.0000, Wilcoxon p 0.0000); median difference 0.284 then -0.004; median change -0.259.

All seeds, no matching: smaller at the end in 27/28 (sign p 0.0000); median change -0.308.

| arm (regulating at first and last point) | K higher at the end | sign p | K at the end | K at the first point | median change | label |
| --- | --- | --- | --- | --- | --- | --- |
| DERIVED | 22/28 | 0.0037 | 0.933 | 0.865 | 0.070 | LAST_AHEAD |
| PAID | 27/28 | 0.0000 | 0.936 | 0.528 | 0.365 | LAST_AHEAD |

At 3600 updates: K on all seeds derived ahead 26/28 (p 0.0000); pairs within 0.05 18/20 (p 0.0004); S 18/26 (0.752 against 0.361); M 16/26 (0.331 against 0.240); flat derived 6/28, paid 2/28; in-band difference in usable pairs 0.010; K against in-band time, rank correlation derived 0.27, paid 0.29; erasure off, regulating derived 28, paid 28.

At 7200 updates: K on all seeds derived ahead 18/28 (p 0.1849); pairs within 0.05 14/21 (p 0.1892); S 14/25 (0.885 against 0.825); M 16/25 (0.375 against 0.294); flat derived 5/28, paid 0/28; in-band difference in usable pairs -0.001; K against in-band time, rank correlation derived 0.15, paid 0.42; erasure off, regulating derived 28, paid 28.

At 10800 updates: K on all seeds derived ahead 14/28 (p 1.0000); pairs within 0.05 11/22 (p 1.0000); S 12/27 (0.852 against 0.899); M 15/27 (0.430 against 0.411); flat derived 4/28, paid 0/28; in-band difference in usable pairs 0.000; K against in-band time, rank correlation derived -0.20, paid 0.14; erasure off, regulating derived 28, paid 28.

Derived reached sustained regulation sooner than paid in 21/27 (p 0.0059). No-fate task accuracy 0.999 (learned: True).
