# Track C P3c: confirmation and cause of the differentiated body readout (Layer 3 -> Layer 4)

**Overall: CONFIRMED_CAUSAL**. Structure reading: ONE_DIRECTION_TWO_READOUTS. Holm-adjusted p: P3C_B1 0.0000, P3C_B2 0.0018, P3C_SA 0.0001, P3C_SC 0.0357.

P3b's rules on these seeds: DIFFERENTIATED (partial reading NOT_APPLICABLE).

Valid: True (phase 1 clear correct A / C 0.980 / 0.999; overwrite-probe accuracy A 0.536; PFATE clear trials below break-even A / C 0.029 / 0.059). Parameters: 35293.

Usable seeds: 28 of 28; excluded: none. Every test below is on the usable seeds.

| updates | arm | in_band | A_low | A_high | C_low | C_high | D | S | G | discrimination_A | discrimination_C |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 0.921 | 0.152 | -0.014 | -0.093 | 0.017 | 0.392 | 1.652 | -0.052 | 0.253 | 0.152 |
| 1800 | PYOKED | 0.847 | -0.000 | -0.000 | -0.001 | 0.001 | 0.001 | 1.125 | -0.000 | 0.206 | 0.121 |
| 1800 | PNOFATE | 0.902 | -0.001 | 0.000 | -0.001 | 0.001 | 0.000 | 1.010 | -0.000 | n/a | n/a |
| 3600 | PFATE | 0.938 | 0.156 | -0.011 | -0.266 | 0.048 | 0.558 | 1.719 | -0.143 | 0.219 | 0.133 |
| 3600 | PYOKED | 0.878 | -0.001 | 0.001 | -0.002 | 0.001 | 0.002 | 2.824 | -0.001 | 0.162 | 0.103 |
| 3600 | PNOFATE | 0.916 | -0.000 | 0.000 | -0.001 | 0.001 | 0.001 | 1.434 | -0.000 | n/a | n/a |

## At 1800

Gate PASS (yoked evidence positive A 28/28, C 28/28, needed 19).
- P3C-B1 memory referent A_low, PFATE against PYOKED: 27/28 (p 0.0000; 0.152 against -0.000) DERIVED_AHEAD
- P3C-B2 C release (-C_low), PFATE against PYOKED: 25/28 (p 0.0000; 0.093 against 0.001) DERIVED_AHEAD
- P3C-SA steering along u_A, directional effect on A, PFATE: 27/28 (p 0.0000; median 0.124) CAUSAL
- P3C-SC steering along u_C, directional release on C, PFATE: 20/28 (p 0.0357; median 0.074) CAUSAL
- Structure reading: PARTLY_SHARED

| arm | S_A | S_C | X_AC | X_CA | V_C | R_A | R_C | P_A | P_C | cos_uA_uC | rel_uA | rel_uC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PFATE | 0.124 | 0.074 | 0.082 | 0.190 | 0.004 | -0.012 | 0.010 | 0.031 | 0.014 | 0.992 | 1.000 | 1.000 |
| PYOKED | 0.003 | -0.002 | -0.002 | 0.002 | -0.001 | 0.003 | -0.000 | 0.008 | 0.002 | 0.991 | 1.000 | 1.000 |
| PNOFATE | -0.001 | 0.000 | 0.001 | -0.004 | -0.001 | 0.000 | 0.000 | 0.002 | 0.000 | 0.990 | 1.000 | 1.000 |

- SA, A's look_low direction moves A (PFATE): 27/28 (p 0.0000; median 0.124) CAUSAL
- SC, C's look_low direction releases C (PFATE): 20/28 (p 0.0357; median 0.074) CAUSAL
- X_AC_PFATE: 17/28 (p 0.3449; median 0.082) NOT_DETECTED
- X_CA_PFATE: 26/28 (p 0.0000; median 0.190) CAUSAL
- V_C_PFATE: 15/28 (p 0.8506; median 0.004) NOT_DETECTED
- V_CA_PFATE: 23/28 (p 0.0009; median 0.030) CAUSAL
- R_A_PFATE: 12/28 (p 0.5716; median -0.012) NOT_DETECTED
- R_C_PFATE: 15/28 (p 0.8506; median 0.010) NOT_DETECTED
- S_A_PFATE_vs_PYOKED: 26/28 (p 0.0000; 0.124 against 0.003) DERIVED_AHEAD
- S_C_PFATE_vs_PYOKED: 20/28 (p 0.0357; 0.074 against -0.002) DERIVED_AHEAD
- S_A_vs_random_PFATE: 26/28 (p 0.0000; 0.124 against -0.012) DIRECTION_AHEAD
- S_C_vs_random_PFATE: 18/28 (p 0.1849; 0.074 against -0.010) NO_DIFFERENCE_DETECTED
- P_A_PFATE_vs_PYOKED: 22/28 (p 0.0037; 0.031 against 0.008) DERIVED_AHEAD
- P_C_PFATE_vs_PYOKED: 28/28 (p 0.0000; 0.014 against 0.002) DERIVED_AHEAD
- cos_uA_uC_PFATE_vs_PYOKED: 16/28 (p 0.5716; 0.992 against 0.991) NO_DIFFERENCE_DETECTED
- route S_A: PFATE 27/28 (p 0.0000; median 0.124) CAUSAL; PYOKED 17/28 (p 0.3449; median 0.003) NOT_DETECTED; PNOFATE 6/28 (p 0.0037; median -0.001) REVERSED_CAUSAL
- route S_C: PFATE 20/28 (p 0.0357; median 0.074) CAUSAL; PYOKED 10/28 (p 0.1849; median -0.002) NOT_DETECTED; PNOFATE 18/28 (p 0.1849; median 0.000) NOT_DETECTED
- route X_AC: PFATE 17/28 (p 0.3449; median 0.082) NOT_DETECTED; PYOKED 7/28 (p 0.0125; median -0.002) REVERSED_CAUSAL; PNOFATE 15/28 (p 0.8506; median 0.001) NOT_DETECTED
- route X_CA: PFATE 26/28 (p 0.0000; median 0.190) CAUSAL; PYOKED 18/28 (p 0.1849; median 0.002) NOT_DETECTED; PNOFATE 6/28 (p 0.0037; median -0.004) REVERSED_CAUSAL
- route V_C: PFATE 15/28 (p 0.8506; median 0.004) NOT_DETECTED; PYOKED 8/28 (p 0.0357; median -0.001) REVERSED_CAUSAL; PNOFATE 12/28 (p 0.5716; median -0.001) NOT_DETECTED

P3b measures on these seeds:
- P3B_0_referent_C: 23/28 (p 0.0009; 0.017 against 0.001) DERIVED_AHEAD
- P3B_1: 28/28 (p 0.0000; median 0.392) DIFFERENTIATED
- P3B_2: 28/28 (p 0.0000; 0.392 against 0.001) DERIVED_AHEAD
- P3B_A: 27/28 (p 0.0000; median 0.174) PRESENT
- P3B_C: 27/28 (p 0.0000; median 0.100) PRESENT
- selectivity_PFATE: 1.652
- G_cross_side_PFATE_vs_PYOKED: 0/28 (p 0.0000; -0.052 against -0.000) YOKED_AHEAD
- A_high_PFATE_vs_PYOKED: 3/28 (p 0.0000; -0.014 against -0.000) YOKED_AHEAD
- A_discrimination_PFATE_vs_PYOKED: 23/28 (p 0.0009; 0.253 against 0.206) DERIVED_AHEAD
- C_discrimination_PFATE_vs_PYOKED: 22/28 (p 0.0037; 0.152 against 0.121) DERIVED_AHEAD
- regulation_PFATE_vs_PYOKED: 24/28 (p 0.0002; 0.921 against 0.847) FATE_AHEAD
- regulation_PFATE_vs_PNOFATE: 20/28 (p 0.0357; 0.921 against 0.902) FATE_AHEAD

## At 3600

Gate PASS (yoked evidence positive A 28/28, C 28/28, needed 19).
- P3C-B1 memory referent A_low, PFATE against PYOKED: 26/28 (p 0.0000; 0.156 against -0.001) DERIVED_AHEAD
- P3C-B2 C release (-C_low), PFATE against PYOKED: 23/28 (p 0.0009; 0.266 against 0.002) DERIVED_AHEAD
- P3C-SA steering along u_A, directional effect on A, PFATE: 25/28 (p 0.0000; median 0.108) CAUSAL
- P3C-SC steering along u_C, directional release on C, PFATE: 20/28 (p 0.0357; median 0.286) CAUSAL
- Structure reading: ONE_DIRECTION_TWO_READOUTS

| arm | S_A | S_C | X_AC | X_CA | V_C | R_A | R_C | P_A | P_C | cos_uA_uC | rel_uA | rel_uC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PFATE | 0.108 | 0.286 | 0.276 | 0.100 | 0.034 | -0.008 | 0.009 | 0.033 | 0.021 | 0.993 | 1.000 | 1.000 |
| PYOKED | 0.001 | -0.001 | -0.002 | -0.001 | -0.002 | 0.001 | -0.000 | 0.006 | 0.002 | 0.991 | 1.000 | 1.000 |
| PNOFATE | 0.000 | 0.001 | 0.000 | -0.002 | -0.000 | 0.001 | 0.000 | 0.001 | 0.000 | 0.991 | 1.000 | 1.000 |

- SA, A's look_low direction moves A (PFATE): 25/28 (p 0.0000; median 0.108) CAUSAL
- SC, C's look_low direction releases C (PFATE): 20/28 (p 0.0357; median 0.286) CAUSAL
- X_AC_PFATE: 21/28 (p 0.0125; median 0.276) CAUSAL
- X_CA_PFATE: 24/28 (p 0.0002; median 0.100) CAUSAL
- V_C_PFATE: 19/28 (p 0.0872; median 0.034) NOT_DETECTED
- V_CA_PFATE: 22/28 (p 0.0037; median 0.017) CAUSAL
- R_A_PFATE: 13/28 (p 0.8506; median -0.008) NOT_DETECTED
- R_C_PFATE: 19/28 (p 0.0872; median 0.009) NOT_DETECTED
- S_A_PFATE_vs_PYOKED: 25/28 (p 0.0000; 0.108 against 0.001) DERIVED_AHEAD
- S_C_PFATE_vs_PYOKED: 22/28 (p 0.0037; 0.286 against -0.001) DERIVED_AHEAD
- S_A_vs_random_PFATE: 20/28 (p 0.0357; 0.108 against -0.008) DIRECTION_AHEAD
- S_C_vs_random_PFATE: 23/28 (p 0.0009; 0.286 against -0.009) DIRECTION_AHEAD
- P_A_PFATE_vs_PYOKED: 27/28 (p 0.0000; 0.033 against 0.006) DERIVED_AHEAD
- P_C_PFATE_vs_PYOKED: 28/28 (p 0.0000; 0.021 against 0.002) DERIVED_AHEAD
- cos_uA_uC_PFATE_vs_PYOKED: 16/28 (p 0.5716; 0.993 against 0.991) NO_DIFFERENCE_DETECTED
- route S_A: PFATE 25/28 (p 0.0000; median 0.108) CAUSAL; PYOKED 18/28 (p 0.1849; median 0.001) NOT_DETECTED; PNOFATE 15/28 (p 0.8506; median 0.000) NOT_DETECTED
- route S_C: PFATE 20/28 (p 0.0357; median 0.286) CAUSAL; PYOKED 12/28 (p 0.5716; median -0.001) NOT_DETECTED; PNOFATE 16/28 (p 0.5716; median 0.001) NOT_DETECTED
- route X_AC: PFATE 21/28 (p 0.0125; median 0.276) CAUSAL; PYOKED 9/28 (p 0.0872; median -0.002) NOT_DETECTED; PNOFATE 14/28 (p 1.0000; median 0.000) NOT_DETECTED
- route X_CA: PFATE 24/28 (p 0.0002; median 0.100) CAUSAL; PYOKED 13/28 (p 0.8506; median -0.001) NOT_DETECTED; PNOFATE 6/28 (p 0.0037; median -0.002) REVERSED_CAUSAL
- route V_C: PFATE 19/28 (p 0.0872; median 0.034) NOT_DETECTED; PYOKED 9/28 (p 0.0872; median -0.002) NOT_DETECTED; PNOFATE 10/28 (p 0.1849; median -0.000) NOT_DETECTED

P3b measures on these seeds:
- P3B_0_referent_C: 23/28 (p 0.0009; 0.048 against 0.001) DERIVED_AHEAD
- P3B_1: 27/28 (p 0.0000; median 0.558) DIFFERENTIATED
- P3B_2: 27/28 (p 0.0000; 0.558 against 0.002) DERIVED_AHEAD
- P3B_A: 25/28 (p 0.0000; median 0.185) PRESENT
- P3B_C: 24/28 (p 0.0002; median 0.335) PRESENT
- selectivity_PFATE: 1.719
- G_cross_side_PFATE_vs_PYOKED: 2/28 (p 0.0000; -0.143 against -0.001) YOKED_AHEAD
- A_high_PFATE_vs_PYOKED: 4/28 (p 0.0002; -0.011 against 0.001) YOKED_AHEAD
- A_discrimination_PFATE_vs_PYOKED: 21/28 (p 0.0125; 0.219 against 0.162) DERIVED_AHEAD
- C_discrimination_PFATE_vs_PYOKED: 21/28 (p 0.0125; 0.133 against 0.103) DERIVED_AHEAD
- regulation_PFATE_vs_PYOKED: 26/28 (p 0.0000; 0.938 against 0.878) FATE_AHEAD
- regulation_PFATE_vs_PNOFATE: 25/28 (p 0.0000; 0.938 against 0.916) FATE_AHEAD
