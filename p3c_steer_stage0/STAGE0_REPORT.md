# P3c stage 0 (declared; not the confirmation): steering on P3b's nets at 3600

Usable P3b nets: 27; excluded: [2401]. Structure reading: NOT_APPLICABLE.

| arm | S_A | S_C | X_AC | X_CA | V_C | R_A | R_C | P_A | P_C | cos_uA_uC | rel_uA | rel_uC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PFATE | 0.060 | 0.030 | 0.040 | 0.122 | 0.006 | -0.004 | -0.002 | 0.017 | 0.008 | 0.991 | 1.000 | 1.000 |
| PYOKED | -0.001 | -0.001 | -0.001 | -0.000 | -0.001 | -0.001 | 0.000 | 0.004 | 0.002 | 0.991 | 1.000 | 1.000 |
| PNOFATE | 0.000 | 0.001 | 0.000 | -0.002 | 0.001 | 0.001 | -0.000 | 0.001 | 0.000 | 0.988 | 1.000 | 1.000 |

- SA, A's look_low direction moves A (PFATE): 22/27 (p 0.0015; median 0.060) CAUSAL
- SC, C's look_low direction releases C (PFATE): 18/27 (p 0.1221; median 0.030) NOT_DETECTED
- X_AC_PFATE: 18/27 (p 0.1221; median 0.040) NOT_DETECTED
- X_CA_PFATE: 22/27 (p 0.0015; median 0.122) CAUSAL
- V_C_PFATE: 19/27 (p 0.0522; median 0.006) NOT_DETECTED
- V_CA_PFATE: 21/27 (p 0.0059; median 0.013) CAUSAL
- R_A_PFATE: 12/27 (p 0.7011; median -0.004) NOT_DETECTED
- R_C_PFATE: 11/27 (p 0.4421; median -0.002) NOT_DETECTED
- S_A_PFATE_vs_PYOKED: 23/27 (p 0.0003; 0.060 against -0.001) DERIVED_AHEAD
- S_C_PFATE_vs_PYOKED: 19/27 (p 0.0522; 0.030 against -0.001) NO_DIFFERENCE_DETECTED
- S_A_vs_random_PFATE: 22/27 (p 0.0015; 0.060 against -0.004) DIRECTION_AHEAD
- S_C_vs_random_PFATE: 18/27 (p 0.1221; 0.030 against 0.002) NO_DIFFERENCE_DETECTED
- P_A_PFATE_vs_PYOKED: 22/27 (p 0.0015; 0.017 against 0.004) DERIVED_AHEAD
- P_C_PFATE_vs_PYOKED: 27/27 (p 0.0000; 0.008 against 0.002) DERIVED_AHEAD
- cos_uA_uC_PFATE_vs_PYOKED: 13/27 (p 1.0000; 0.991 against 0.991) NO_DIFFERENCE_DETECTED
- route S_A: PFATE 22/27 (p 0.0015; median 0.060) CAUSAL; PYOKED 12/27 (p 0.7011; median -0.001) NOT_DETECTED; PNOFATE 14/27 (p 1.0000; median 0.000) NOT_DETECTED
- route S_C: PFATE 18/27 (p 0.1221; median 0.030) NOT_DETECTED; PYOKED 12/27 (p 0.7011; median -0.001) NOT_DETECTED; PNOFATE 19/27 (p 0.0522; median 0.001) NOT_DETECTED
- route X_AC: PFATE 18/27 (p 0.1221; median 0.040) NOT_DETECTED; PYOKED 11/27 (p 0.4421; median -0.001) NOT_DETECTED; PNOFATE 16/27 (p 0.4421; median 0.000) NOT_DETECTED
- route X_CA: PFATE 22/27 (p 0.0015; median 0.122) CAUSAL; PYOKED 13/27 (p 1.0000; median -0.000) NOT_DETECTED; PNOFATE 10/27 (p 0.2478; median -0.002) NOT_DETECTED
- route V_C: PFATE 19/27 (p 0.0522; median 0.006) NOT_DETECTED; PYOKED 11/27 (p 0.4421; median -0.001) NOT_DETECTED; PNOFATE 19/27 (p 0.0522; median 0.001) NOT_DETECTED