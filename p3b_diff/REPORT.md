# Track C P3b: differentiation of the body-grounded self-state (Layer 3 -> Layer 4)

**Overall: UNDETERMINED**. Partial reading: A_SIDE_SPECIFIC, NO_SPREAD. Holm-adjusted p: P3B_1 0.0000, P3B_2 0.0000, P3B_A 0.0000, P3B_C 0.0015.

Valid: True (phase 1 clear correct A / C 0.988 / 0.999, needed >= 0.8; overwrite-probe accuracy A 0.522, needed <= 0.7; PFATE clear trials below break-even A / C 0.029 / 0.054, needed >= 0.02 each). Parameters: 35293.

Usable seeds (phase 1 learned every type): 27 of 28; excluded: [2401]. Every test below is on the usable seeds.

| updates | arm | in_band | A_low | A_high | C_low | C_high | D | S | G | retained_A | retained_C | discrimination_A | discrimination_C | noise_A |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 0.919 | 0.063 | -0.008 | -0.017 | 0.005 | 0.216 | 1.359 | -0.016 | 0.957 | 0.971 | 0.227 | 0.117 | 0.264 |
| 1800 | PYOKED | 0.873 | 0.000 | 0.001 | -0.001 | 0.000 | 0.000 | 1.242 | -0.000 | 0.994 | 0.995 | 0.212 | 0.116 | 0.259 |
| 1800 | PNOFATE | 0.887 | 0.000 | 0.000 | -0.000 | 0.000 | 0.001 | 1.005 | 0.000 | 0.999 | 0.999 | n/a | n/a | 0.266 |
| 3600 | PFATE | 0.945 | 0.102 | -0.007 | -0.031 | 0.005 | 0.326 | 1.379 | -0.029 | 0.953 | 0.962 | 0.218 | 0.126 | 0.256 |
| 3600 | PYOKED | 0.882 | 0.000 | 0.001 | -0.001 | 0.000 | 0.000 | 1.238 | 0.000 | 0.995 | 0.996 | 0.185 | 0.100 | 0.262 |
| 3600 | PNOFATE | 0.899 | 0.000 | 0.000 | 0.001 | 0.000 | 0.001 | 1.054 | 0.000 | 0.999 | 0.999 | n/a | n/a | 0.249 |

At 1800: regulators {'PFATE': 27, 'PYOKED': 27, 'PNOFATE': 27}; gate PASS (yoked evidence effect positive A 27/27, C 27/27, needed 18; retained medians {'A_PFATE': '0.957', 'A_PYOKED': '0.994', 'A_PNOFATE': '0.999', 'C_PFATE': '0.971', 'C_PYOKED': '0.995', 'C_PNOFATE': '0.999'}, needed >= 0.6).
- P3B-0 referent A (look_low on A), PFATE against PYOKED: 25/27 (p 0.0000; 0.063 against 0.000) DERIVED_AHEAD
- P3B-0 referent C (look_high on C), PFATE against PYOKED: 18/27 (p 0.1221; 0.005 against 0.000) NO_DIFFERENCE_DETECTED
- P3B-1 differentiation index D in PFATE: 25/27 (p 0.0000; median 0.216) DIFFERENTIATED
- P3B-2 D, PFATE against PYOKED: 25/27 (p 0.0000; 0.216 against 0.000) DERIVED_AHEAD
- P3B-A A half (A_low - A_high) in PFATE: 25/27 (p 0.0000; median 0.065) PRESENT
- P3B-C C half (C_high - C_low) in PFATE: 19/27 (p 0.0522; median 0.023) NOT_DETECTED
- Selectivity S in PFATE, median: 1.359 (needed >= 0.5 for DIFFERENTIATED)
- G_cross_side_PFATE_vs_PYOKED: 3/27 (p 0.0000; -0.016 against -0.000) YOKED_AHEAD
- G_cross_side_PFATE_vs_PNOFATE: 3/27 (p 0.0000; -0.016 against 0.000) HOST_AHEAD
- C_low_PFATE_vs_PYOKED: 8/27 (p 0.0522; -0.017 against -0.001) NO_DIFFERENCE_DETECTED
- A_high_PFATE_vs_PYOKED: 2/27 (p 0.0000; -0.008 against 0.001) YOKED_AHEAD
- A_low_PFATE_vs_PNOFATE: 25/27 (p 0.0000; 0.063 against 0.000) DERIVED_AHEAD
- C_high_PFATE_vs_PNOFATE: 20/27 (p 0.0192; 0.005 against 0.000) DERIVED_AHEAD
- D_PFATE_vs_PNOFATE: 25/27 (p 0.0000; 0.216 against 0.001) DERIVED_AHEAD
- A_discrimination_PFATE_vs_PYOKED: 19/27 (p 0.0522; 0.227 against 0.212) NO_DIFFERENCE_DETECTED
- C_discrimination_PFATE_vs_PYOKED: 18/27 (p 0.1221; 0.117 against 0.116) NO_DIFFERENCE_DETECTED
- D_route: PFATE 25/27 (p 0.0000; median 0.216) DIFFERENTIATED; PYOKED 14/27 (p 1.0000; median 0.000) NOT_DETECTED; PNOFATE 16/27 (p 0.4421; median 0.001) NOT_DETECTED
- look_routes A_low: PFATE 25/27 (p 0.0000; median 0.063) PRESENT; PYOKED 14/27 (p 1.0000; median 0.000) NOT_DETECTED; PNOFATE 10/23 (p 0.6776; median -0.000) NOT_DETECTED
- look_routes A_high: PFATE 3/27 (p 0.0000; median -0.008) REVERSED; PYOKED 19/26 (p 0.0290; median 0.001) PRESENT; PNOFATE 10/17 (p 0.6291; median 0.000) NOT_DETECTED
- look_routes C_low: PFATE 7/27 (p 0.0192; median -0.017) REVERSED; PYOKED 7/27 (p 0.0192; median -0.001) REVERSED; PNOFATE 11/25 (p 0.6900; median -0.000) NOT_DETECTED
- look_routes C_high: PFATE 19/27 (p 0.0522; median 0.005) NOT_DETECTED; PYOKED 15/27 (p 0.7011; median 0.000) NOT_DETECTED; PNOFATE 12/23 (p 1.0000; median 0.000) NOT_DETECTED
- monitor_route A: PFATE 27/27 (p 0.0000; median 0.264) PRESENT; PYOKED 27/27 (p 0.0000; median 0.259) PRESENT; PNOFATE 27/27 (p 0.0000; median 0.266) PRESENT
- regulation_PFATE_vs_PNOFATE: 19/27 (p 0.0522; 0.919 against 0.887) NO_DIFFERENCE_DETECTED
- regulation_PFATE_vs_PYOKED: 25/27 (p 0.0000; 0.919 against 0.873) FATE_AHEAD

At 3600: regulators {'PFATE': 27, 'PYOKED': 26, 'PNOFATE': 27}; gate PASS (yoked evidence effect positive A 27/27, C 27/27, needed 18; retained medians {'A_PFATE': '0.953', 'A_PYOKED': '0.995', 'A_PNOFATE': '0.999', 'C_PFATE': '0.962', 'C_PYOKED': '0.996', 'C_PNOFATE': '0.999'}, needed >= 0.6).
- P3B-0 referent A (look_low on A), PFATE against PYOKED: 25/27 (p 0.0000; 0.102 against 0.000) DERIVED_AHEAD
- P3B-0 referent C (look_high on C), PFATE against PYOKED: 18/27 (p 0.1221; 0.005 against 0.000) NO_DIFFERENCE_DETECTED
- P3B-1 differentiation index D in PFATE: 26/27 (p 0.0000; median 0.326) DIFFERENTIATED
- P3B-2 D, PFATE against PYOKED: 26/27 (p 0.0000; 0.326 against 0.000) DERIVED_AHEAD
- P3B-A A half (A_low - A_high) in PFATE: 25/27 (p 0.0000; median 0.109) PRESENT
- P3B-C C half (C_high - C_low) in PFATE: 22/27 (p 0.0015; median 0.038) PRESENT
- Selectivity S in PFATE, median: 1.379 (needed >= 0.5 for DIFFERENTIATED)
- G_cross_side_PFATE_vs_PYOKED: 2/27 (p 0.0000; -0.029 against 0.000) YOKED_AHEAD
- G_cross_side_PFATE_vs_PNOFATE: 1/27 (p 0.0000; -0.029 against 0.000) HOST_AHEAD
- C_low_PFATE_vs_PYOKED: 7/27 (p 0.0192; -0.031 against -0.001) YOKED_AHEAD
- A_high_PFATE_vs_PYOKED: 3/27 (p 0.0000; -0.007 against 0.001) YOKED_AHEAD
- A_low_PFATE_vs_PNOFATE: 25/27 (p 0.0000; 0.102 against 0.000) DERIVED_AHEAD
- C_high_PFATE_vs_PNOFATE: 20/27 (p 0.0192; 0.005 against 0.000) DERIVED_AHEAD
- D_PFATE_vs_PNOFATE: 26/27 (p 0.0000; 0.326 against 0.001) DERIVED_AHEAD
- A_discrimination_PFATE_vs_PYOKED: 20/27 (p 0.0192; 0.218 against 0.185) DERIVED_AHEAD
- C_discrimination_PFATE_vs_PYOKED: 16/27 (p 0.4421; 0.126 against 0.100) NO_DIFFERENCE_DETECTED
- D_route: PFATE 26/27 (p 0.0000; median 0.326) DIFFERENTIATED; PYOKED 14/27 (p 1.0000; median 0.000) NOT_DETECTED; PNOFATE 15/27 (p 0.7011; median 0.001) NOT_DETECTED
- look_routes A_low: PFATE 25/27 (p 0.0000; median 0.102) PRESENT; PYOKED 15/26 (p 0.5572; median 0.000) NOT_DETECTED; PNOFATE 15/24 (p 0.3075; median 0.001) NOT_DETECTED
- look_routes A_high: PFATE 5/27 (p 0.0015; median -0.007) REVERSED; PYOKED 17/25 (p 0.1078; median 0.001) NOT_DETECTED; PNOFATE 4/13 (p 0.2668; median -0.001) UNDETERMINED
- look_routes C_low: PFATE 6/27 (p 0.0059; median -0.031) REVERSED; PYOKED 7/26 (p 0.0290; median -0.001) REVERSED; PNOFATE 16/26 (p 0.3269; median 0.001) NOT_DETECTED
- look_routes C_high: PFATE 19/27 (p 0.0522; median 0.005) NOT_DETECTED; PYOKED 14/27 (p 1.0000; median 0.000) NOT_DETECTED; PNOFATE 10/20 (p 1.0000; median -0.000) NOT_DETECTED
- monitor_route A: PFATE 27/27 (p 0.0000; median 0.256) PRESENT; PYOKED 27/27 (p 0.0000; median 0.262) PRESENT; PNOFATE 27/27 (p 0.0000; median 0.249) PRESENT
- regulation_PFATE_vs_PNOFATE: 25/27 (p 0.0000; 0.945 against 0.899) FATE_AHEAD
- regulation_PFATE_vs_PYOKED: 25/27 (p 0.0000; 0.945 against 0.882) FATE_AHEAD
