# Track C P1e: self-monitoring of the agent's own computation (Layer 0 -> Layer 4)

**Overall: INVALID.** L0 reading: NOT_APPLICABLE. Hardened (PFATE accuracy under the conflict probe > 0.75): False. Holm-adjusted p: P1E_1 0.0000, P1E_2 0.0000, P1E_3 0.0009.

Valid: False (phase 1: clear correct 0.999, needed >= 0.8; accuracy under the conflict probe 0.510, needed <= 0.7 (same probe 1.000); PFATE clear trials with a conflict event 0.014, needed >= 0.02). Parameters: 34449. Damage: 35 units from a donor, per-step probability min(0.3, 1.0 x gain), once per trial. Probe at delay step 1 (early) and 8 (late) on 0.667 of the trials. Drain shift 0.15.

| updates | arm | M | M_early | M_late | M_conf_early | Q_early | Q_late | acc_conflict | acc_same | decode_conflict_early | margin_conflict_early | margin_none_early | drain_effect | nat_M | share_conflict | in_band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 0.425 | 0.583 | 0.231 | 0.026 | 0.001 | -0.009 | 0.512 | 1.000 | 0.506 | 73.329 | 123.743 | -0.014 | 0.593 | 0.021 | 0.943 |
| 1800 | PYOKED | 0.372 | 0.566 | 0.158 | 0.000 | 0.000 | 0.000 | 0.500 | 1.000 | 0.501 | 83.899 | 150.121 | 0.001 | 0.564 | 0.020 | 0.878 |
| 1800 | PNOFATE | 0.001 | 0.001 | 0.002 | 0.000 | 0.000 | 0.000 | 0.504 | 1.000 | 0.499 | 91.902 | 99.434 | 0.000 | n/a | 0.000 | 0.888 |
| 3600 | PFATE | 0.557 | 0.811 | 0.298 | 0.049 | 0.003 | -0.005 | 0.513 | 1.000 | 0.517 | 53.309 | 109.362 | -0.002 | 0.812 | 0.014 | 0.956 |
| 3600 | PYOKED | 0.629 | 0.893 | 0.377 | 0.000 | 0.002 | 0.001 | 0.518 | 1.000 | 0.512 | 69.848 | 170.143 | 0.001 | 0.869 | 0.015 | 0.889 |
| 3600 | PNOFATE | 0.002 | 0.001 | 0.002 | 0.000 | 0.000 | 0.000 | 0.508 | 1.000 | 0.501 | 79.385 | 95.264 | 0.001 | n/a | 0.000 | 0.900 |

## At 1800

- P1E-1 monitor learned, M PFATE against PNOFATE: 27/28 (p 0.0000; 0.425 against 0.001) DERIVED_AHEAD
- P1E-2 monitor after settling, M_early PFATE against PNOFATE: 25/28 (p 0.0000; 0.583 against 0.001) DERIVED_AHEAD
- P1E-3 the L0 arrow, M PFATE against PYOKED: 18/28 (p 0.1849; 0.425 against 0.372) NO_DIFFERENCE_DETECTED
- M_PYOKED_vs_PNOFATE: 26/27 (p 0.0000; 0.373 against 0.001) DERIVED_AHEAD
- M_late_PFATE_vs_PNOFATE: 27/28 (p 0.0000; 0.231 against 0.002) DERIVED_AHEAD
- M_early_PFATE_vs_PYOKED: 14/28 (p 1.0000; 0.583 against 0.566) NO_DIFFERENCE_DETECTED
- M_conf_early_PFATE_vs_PNOFATE: 17/25 (p 0.1078; 0.028 against 0.000) NO_DIFFERENCE_DETECTED
- M_conf_early_PYOKED_vs_PNOFATE: 6/14 (p 0.7905; -0.003 against 0.000) NO_DIFFERENCE_DETECTED
- Q_early_PFATE_vs_PNOFATE: 16/27 (p 0.4421; 0.002 against 0.000) NO_DIFFERENCE_DETECTED
- drain_PFATE_vs_PYOKED: 6/28 (p 0.0037; -0.014 against 0.001) YOKED_AHEAD
- regulation_PFATE_vs_PYOKED: 27/28 (p 0.0000; 0.943 against 0.878) FATE_AHEAD
- regulation_PFATE_vs_PNOFATE: 25/28 (p 0.0000; 0.943 against 0.888) FATE_AHEAD
- route M: PFATE 28/28 (p 0.0000; median 0.425) PRESENT; PYOKED 27/27 (p 0.0000; median 0.373) PRESENT; PNOFATE 24/26 (p 0.0000; median 0.001) PRESENT
- route M_early: PFATE 26/28 (p 0.0000; median 0.583) PRESENT; PYOKED 26/26 (p 0.0000; median 0.597) PRESENT; PNOFATE 15/21 (p 0.0784; median 0.001) NOT_DETECTED
- route M_late: PFATE 28/28 (p 0.0000; median 0.231) PRESENT; PYOKED 26/26 (p 0.0000; median 0.186) PRESENT; PNOFATE 21/22 (p 0.0000; median 0.002) PRESENT
- route M_conf_early: PFATE 17/25 (p 0.1078; median 0.028) NOT_DETECTED; PYOKED 4/12 (p 0.3877; median -0.003) UNDETERMINED; PNOFATE 0/4 (p 0.1250; median -0.002) UNDETERMINED
- route Q_early: PFATE 17/27 (p 0.2478; median 0.002) NOT_DETECTED; PYOKED 14/22 (p 0.2863; median 0.000) NOT_DETECTED; PNOFATE 8/12 (p 0.3877; median 0.001) UNDETERMINED
- route nat_M: PFATE 27/27 (p 0.0000; median 0.619) PRESENT; PYOKED 22/23 (p 0.0000; median 0.646) PRESENT; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED

## At 3600

- P1E-1 monitor learned, M PFATE against PNOFATE: 27/28 (p 0.0000; 0.557 against 0.002) DERIVED_AHEAD
- P1E-2 monitor after settling, M_early PFATE against PNOFATE: 27/28 (p 0.0000; 0.811 against 0.001) DERIVED_AHEAD
- P1E-3 the L0 arrow, M PFATE against PYOKED: 5/28 (p 0.0009; 0.557 against 0.629) YOKED_AHEAD
- M_PYOKED_vs_PNOFATE: 28/28 (p 0.0000; 0.629 against 0.002) DERIVED_AHEAD
- M_late_PFATE_vs_PNOFATE: 27/28 (p 0.0000; 0.298 against 0.002) DERIVED_AHEAD
- M_early_PFATE_vs_PYOKED: 3/28 (p 0.0000; 0.811 against 0.893) YOKED_AHEAD
- M_conf_early_PFATE_vs_PNOFATE: 18/26 (p 0.0755; 0.054 against 0.000) NO_DIFFERENCE_DETECTED
- M_conf_early_PYOKED_vs_PNOFATE: 7/15 (p 1.0000; -0.003 against 0.000) NO_DIFFERENCE_DETECTED
- Q_early_PFATE_vs_PNOFATE: 19/28 (p 0.0872; 0.003 against 0.000) NO_DIFFERENCE_DETECTED
- drain_PFATE_vs_PYOKED: 9/28 (p 0.0872; -0.002 against 0.001) NO_DIFFERENCE_DETECTED
- regulation_PFATE_vs_PYOKED: 27/28 (p 0.0000; 0.956 against 0.889) FATE_AHEAD
- regulation_PFATE_vs_PNOFATE: 24/28 (p 0.0002; 0.956 against 0.900) FATE_AHEAD
- route M: PFATE 27/28 (p 0.0000; median 0.557) PRESENT; PYOKED 28/28 (p 0.0000; median 0.629) PRESENT; PNOFATE 23/26 (p 0.0001; median 0.002) PRESENT
- route M_early: PFATE 27/28 (p 0.0000; median 0.811) PRESENT; PYOKED 28/28 (p 0.0000; median 0.893) PRESENT; PNOFATE 15/21 (p 0.0784; median 0.001) NOT_DETECTED
- route M_late: PFATE 27/28 (p 0.0000; median 0.298) PRESENT; PYOKED 28/28 (p 0.0000; median 0.377) PRESENT; PNOFATE 23/25 (p 0.0000; median 0.002) PRESENT
- route M_conf_early: PFATE 18/26 (p 0.0755; median 0.054) NOT_DETECTED; PYOKED 4/13 (p 0.2668; median -0.003) UNDETERMINED; PNOFATE 1/6 (p 0.2188; median -0.002) UNDETERMINED
- route Q_early: PFATE 20/28 (p 0.0357; median 0.003) PRESENT; PYOKED 23/27 (p 0.0003; median 0.002) PRESENT; PNOFATE 9/13 (p 0.2668; median 0.001) UNDETERMINED
- route nat_M: PFATE 28/28 (p 0.0000; median 0.812) PRESENT; PYOKED 28/28 (p 0.0000; median 0.869) PRESENT; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
