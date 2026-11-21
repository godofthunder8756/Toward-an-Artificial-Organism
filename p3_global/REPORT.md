# Track C P3: global availability of the body-grounded self-state (Layer 0 -> Layer 3)

**Overall: GLOBAL_ROUTED**. Gating (C): UNGATED. Holm-adjusted p: P3_1 0.0000, P3_2 0.0000, P3_3 0.0192.

Valid: True (phase 1 clear correct A / B / C 0.987 / 0.987 / 0.999, needed >= 0.8; overwrite-probe accuracy A / B 0.531 / 0.537, needed <= 0.7; PFATE A clear trials below break-even 0.046, needed >= 0.02). Parameters: 35293. Phase 2 trial types: A only.

Usable seeds (phase 1 learned every type): 19 of 28; excluded: [2200, 2203, 2205, 2206, 2216, 2223, 2224, 2225, 2226]. Every test below is on the usable seeds.

| updates | arm | in_band | worse_A | worse_B | worse_C | retained_A | retained_B | retained_C | evidence_B | discrimination_A | discrimination_B | steer_A | steer_B | steer_C | noise_A | noise_B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 0.938 | 0.114 | 0.044 | 0.040 | 0.984 | 0.969 | 0.980 | 0.962 | 0.223 | 0.153 | 0.012 | 0.044 | 0.013 | 0.257 | 0.240 |
| 1800 | PYOKED | 0.826 | 0.002 | 0.009 | 0.008 | 0.996 | 0.982 | 0.981 | 0.975 | 0.167 | 0.151 | 0.002 | 0.001 | -0.012 | 0.252 | 0.245 |
| 1800 | PNOFATE | 0.874 | 0.001 | 0.003 | 0.003 | 1.000 | 0.998 | 0.998 | 0.995 | n/a | n/a | 0.000 | 0.001 | -0.003 | 0.259 | 0.258 |
| 3600 | PFATE | 0.945 | 0.088 | 0.041 | 0.043 | 0.987 | 0.983 | 0.985 | 0.981 | 0.211 | 0.166 | 0.000 | 0.025 | -0.002 | 0.257 | 0.240 |
| 3600 | PYOKED | 0.882 | 0.001 | 0.006 | 0.005 | 0.999 | 0.989 | 0.989 | 0.982 | 0.144 | 0.139 | 0.004 | 0.009 | -0.002 | 0.256 | 0.247 |
| 3600 | PNOFATE | 0.906 | 0.000 | 0.002 | 0.001 | 1.000 | 0.998 | 0.998 | 0.995 | n/a | n/a | -0.001 | -0.002 | -0.005 | 0.253 | 0.260 |

At 1800: usable pairs 9; regulators {'PFATE': 19, 'PYOKED': 19, 'PNOFATE': 19}; gate PASS (yoked B evidence effect positive 19/19, needed 13; B retained medians {'PFATE': '0.969', 'PYOKED': '0.982', 'PNOFATE': '0.998'}, needed >= 0.6).
- P3-0 referent in A, PFATE against PYOKED: 19/19 (p 0.0000; 0.114 against 0.002) DERIVED_AHEAD
- P3-1 B worse effect, PFATE against PYOKED: 16/19 (p 0.0044; 0.044 against 0.009) DERIVED_AHEAD
- P3-2 B worse effect, PFATE against PNOFATE: 19/19 (p 0.0000; 0.044 against 0.003) DERIVED_AHEAD
- P3-3 steering along A's worse direction, B trials, PFATE: 11/19 (p 0.6476; median 0.044) NOT_DETECTED
- Transfer ratio in PFATE (B worse effect / A worse effect), median: 0.350
- C_worse_PFATE_vs_PYOKED: 17/19 (p 0.0007; 0.040 against 0.008) DERIVED_AHEAD
- C_worse_PFATE_vs_PNOFATE: 18/19 (p 0.0001; 0.040 against 0.003) DERIVED_AHEAD
- C_steer_PFATE: 11/19 (p 0.6476; median 0.013) NOT_DETECTED
- A_worse_PFATE_vs_PNOFATE: 18/19 (p 0.0001; 0.114 against 0.001) DERIVED_AHEAD
- A_steer_PFATE: 11/19 (p 0.6476; median 0.012) NOT_DETECTED
- B_worse_usable_pairs: 9/9 (p 0.0039; 0.059 against 0.013) UNDETERMINED
- B_discrimination_PFATE_vs_PYOKED: 10/19 (p 1.0000; 0.153 against 0.151) NO_DIFFERENCE_DETECTED
- A_discrimination_PFATE_vs_PYOKED: 14/19 (p 0.0636; 0.223 against 0.167) NO_DIFFERENCE_DETECTED
- B_minus_C_worse_PFATE: 9/19 (p 1.0000; median -0.006) NOT_DETECTED
- worse_route A: PFATE 18/19 (p 0.0001; median 0.114) PRESENT; PYOKED 13/19 (p 0.1671; median 0.002) NOT_DETECTED; PNOFATE 13/15 (p 0.0074; median 0.001) PRESENT
- worse_route B: PFATE 19/19 (p 0.0000; median 0.044) PRESENT; PYOKED 17/19 (p 0.0007; median 0.009) PRESENT; PNOFATE 17/19 (p 0.0007; median 0.003) PRESENT
- worse_route C: PFATE 18/19 (p 0.0001; median 0.040) PRESENT; PYOKED 15/19 (p 0.0192; median 0.008) PRESENT; PNOFATE 17/19 (p 0.0007; median 0.003) PRESENT
- steer_route A: PFATE 11/19 (p 0.6476; median 0.012) NOT_DETECTED; PYOKED 12/19 (p 0.3593; median 0.002) NOT_DETECTED; PNOFATE 11/19 (p 0.6476; median 0.000) NOT_DETECTED
- steer_route B: PFATE 11/19 (p 0.6476; median 0.044) NOT_DETECTED; PYOKED 10/19 (p 1.0000; median 0.001) NOT_DETECTED; PNOFATE 10/19 (p 1.0000; median 0.001) NOT_DETECTED
- steer_route C: PFATE 11/19 (p 0.6476; median 0.013) NOT_DETECTED; PYOKED 6/19 (p 0.1671; median -0.012) NOT_DETECTED; PNOFATE 8/19 (p 0.6476; median -0.003) NOT_DETECTED
- monitor_route A: PFATE 19/19 (p 0.0000; median 0.257) PRESENT; PYOKED 19/19 (p 0.0000; median 0.252) PRESENT; PNOFATE 19/19 (p 0.0000; median 0.259) PRESENT
- monitor_route B: PFATE 19/19 (p 0.0000; median 0.240) PRESENT; PYOKED 19/19 (p 0.0000; median 0.245) PRESENT; PNOFATE 19/19 (p 0.0000; median 0.258) PRESENT
- regulation_PFATE_vs_PNOFATE: 15/19 (p 0.0192; 0.938 against 0.874) FATE_AHEAD
- regulation_PFATE_vs_PYOKED: 19/19 (p 0.0000; 0.938 against 0.826) FATE_AHEAD

At 3600: usable pairs 15; regulators {'PFATE': 19, 'PYOKED': 19, 'PNOFATE': 19}; gate PASS (yoked B evidence effect positive 19/19, needed 13; B retained medians {'PFATE': '0.983', 'PYOKED': '0.989', 'PNOFATE': '0.998'}, needed >= 0.6).
- P3-0 referent in A, PFATE against PYOKED: 18/19 (p 0.0001; 0.088 against 0.001) DERIVED_AHEAD
- P3-1 B worse effect, PFATE against PYOKED: 19/19 (p 0.0000; 0.041 against 0.006) DERIVED_AHEAD
- P3-2 B worse effect, PFATE against PNOFATE: 19/19 (p 0.0000; 0.041 against 0.002) DERIVED_AHEAD
- P3-3 steering along A's worse direction, B trials, PFATE: 15/19 (p 0.0192; median 0.025) CAUSAL
- Transfer ratio in PFATE (B worse effect / A worse effect), median: 0.526
- C_worse_PFATE_vs_PYOKED: 18/19 (p 0.0001; 0.043 against 0.005) DERIVED_AHEAD
- C_worse_PFATE_vs_PNOFATE: 19/19 (p 0.0000; 0.043 against 0.001) DERIVED_AHEAD
- C_steer_PFATE: 9/19 (p 1.0000; median -0.002) NOT_DETECTED
- A_worse_PFATE_vs_PNOFATE: 18/19 (p 0.0001; 0.088 against 0.000) DERIVED_AHEAD
- A_steer_PFATE: 10/19 (p 1.0000; median 0.000) NOT_DETECTED
- B_worse_usable_pairs: 15/15 (p 0.0001; 0.040 against 0.006) DERIVED_AHEAD
- B_discrimination_PFATE_vs_PYOKED: 15/19 (p 0.0192; 0.166 against 0.139) DERIVED_AHEAD
- A_discrimination_PFATE_vs_PYOKED: 14/19 (p 0.0636; 0.211 against 0.144) NO_DIFFERENCE_DETECTED
- B_minus_C_worse_PFATE: 11/19 (p 0.6476; median 0.006) NOT_DETECTED
- worse_route A: PFATE 18/19 (p 0.0001; median 0.088) PRESENT; PYOKED 12/19 (p 0.3593; median 0.001) NOT_DETECTED; PNOFATE 8/11 (p 0.2266; median 0.001) UNDETERMINED
- worse_route B: PFATE 19/19 (p 0.0000; median 0.041) PRESENT; PYOKED 18/19 (p 0.0001; median 0.006) PRESENT; PNOFATE 16/19 (p 0.0044; median 0.002) PRESENT
- worse_route C: PFATE 19/19 (p 0.0000; median 0.043) PRESENT; PYOKED 14/19 (p 0.0636; median 0.005) NOT_DETECTED; PNOFATE 14/19 (p 0.0636; median 0.001) NOT_DETECTED
- steer_route A: PFATE 10/19 (p 1.0000; median 0.000) NOT_DETECTED; PYOKED 10/19 (p 1.0000; median 0.004) NOT_DETECTED; PNOFATE 8/18 (p 0.8145; median -0.001) NOT_DETECTED
- steer_route B: PFATE 15/19 (p 0.0192; median 0.025) CAUSAL; PYOKED 11/19 (p 0.6476; median 0.009) NOT_DETECTED; PNOFATE 8/19 (p 0.6476; median -0.002) NOT_DETECTED
- steer_route C: PFATE 9/19 (p 1.0000; median -0.002) NOT_DETECTED; PYOKED 9/19 (p 1.0000; median -0.002) NOT_DETECTED; PNOFATE 7/18 (p 0.4807; median -0.008) NOT_DETECTED
- monitor_route A: PFATE 19/19 (p 0.0000; median 0.257) PRESENT; PYOKED 19/19 (p 0.0000; median 0.256) PRESENT; PNOFATE 19/19 (p 0.0000; median 0.253) PRESENT
- monitor_route B: PFATE 19/19 (p 0.0000; median 0.240) PRESENT; PYOKED 19/19 (p 0.0000; median 0.247) PRESENT; PNOFATE 19/19 (p 0.0000; median 0.260) PRESENT
- regulation_PFATE_vs_PNOFATE: 19/19 (p 0.0000; 0.945 against 0.906) FATE_AHEAD
- regulation_PFATE_vs_PYOKED: 19/19 (p 0.0000; 0.945 against 0.882) FATE_AHEAD
