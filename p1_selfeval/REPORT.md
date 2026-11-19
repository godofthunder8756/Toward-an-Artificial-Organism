# Track C P1: does a precarious substrate give self-evaluation a referent?

**Overall: REFERENT_SUPPORTED_ROUTED.** Holm-adjusted p: P1_1 0.0010, P1_2 0.0005, P1_3 0.0010.

Valid: True (phase-1 correct-report rate, median: RTSS 0.997, plain 0.999). Parameters: RTSS 34233, plain 34449.

| updates | arm | regulators | in band | abstain | correct | wrong | evidence effect | drain effect (clear) | drain effect (unclear) | steer effect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3600 | PFATE | 9 | 0.480 | 0.691 | 0.278 | 0.019 | 0.601 | 0.234 | 0.002 | 0.237 |
| 3600 | PLOSS | 28 | 0.838 | 0.821 | 0.156 | 0.017 | 0.297 | 0.027 | 0.001 | 0.039 |
| 3600 | PYOKED | 0 | 0.278 | 0.779 | 0.193 | 0.019 | 0.423 | 0.008 | 0.001 | 0.004 |
| 3600 | FATE | 0 | 0.194 | 0.997 | 0.002 | 0.001 | 0.000 | 0.001 | 0.000 | 0.000 |
| 7200 | PFATE | 28 | 0.944 | 0.502 | 0.494 | 0.004 | 0.990 | 0.051 | 0.000 | 0.096 |
| 7200 | PLOSS | 28 | 0.889 | 0.500 | 0.494 | 0.006 | 0.997 | 0.001 | -0.000 | 0.003 |
| 7200 | PYOKED | 0 | 0.294 | 0.499 | 0.495 | 0.005 | 0.998 | -0.000 | -0.000 | -0.000 |
| 7200 | FATE | 7 | 0.244 | 0.868 | 0.120 | 0.006 | 0.248 | 0.011 | 0.000 | 0.000 |

At 3600: usable pairs 7; P1-0 gate PASS (yoked evidence effect positive in 28/28, needed 19).
- P1-1 drain effect, PFATE against PLOSS, usable pairs: 7/7 (p 0.0156; 0.193 against 0.016) UNDETERMINED
- P1-2 drain effect, PFATE against PYOKED: 28/28 (p 0.0000; 0.234 against 0.008) DERIVED_AHEAD
- P1-3 steering in PFATE: 28/28 (p 0.0000; median 0.237) CAUSAL
- P1-4 (secondary) drain effect, RTSS-FATE against PFATE: 0/28 (p 0.0000; 0.001 against 0.234) PLAIN_AHEAD
- RTSS-FATE regulators: 0; drain route among them 0/0 (p n/a; median n/a) UNDETERMINED; steering 0/0 (p n/a; median n/a) UNDETERMINED

At 7200: usable pairs 23; P1-0 gate PASS (yoked evidence effect positive in 28/28, needed 19).
- P1-1 drain effect, PFATE against PLOSS, usable pairs: 20/23 (p 0.0005; 0.054 against 0.001) DERIVED_AHEAD
- P1-2 drain effect, PFATE against PYOKED: 24/28 (p 0.0002; 0.051 against -0.000) DERIVED_AHEAD
- P1-3 steering in PFATE: 23/28 (p 0.0009; median 0.096) CAUSAL
- P1-4 (secondary) drain effect, RTSS-FATE against PFATE: 7/28 (p 0.0125; 0.011 against 0.051) PLAIN_AHEAD
- RTSS-FATE regulators: 7; drain route among them 3/7 (p 1.0000; median -0.016) UNDETERMINED; steering 3/7 (p 1.0000; median -0.000) UNDETERMINED
