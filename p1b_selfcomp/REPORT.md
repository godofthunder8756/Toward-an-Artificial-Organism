# Track C P1b: precarious computation and the referent of self-evaluation

**Overall: NOT_ESTABLISHED.** Holm-adjusted p: P1B_1 1.0000, P1B_2 1.0000, P1B_3 0.9808.

Valid: True (phase 1: clear correct-report rate 0.999, needed >= 0.8; report accuracy under the noise probe 0.671, needed <= 0.85). Parameters: 34449. Noise SD per unit per step at gain 1: 0.5.

| updates | arm | regulators | in band | mean gain | abstain | correct | wrong | evidence effect | drain effect | noise effect | accuracy under noise | steer effect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 27 | 0.912 | 0.023 | 0.501 | 0.498 | 0.001 | 0.998 | 0.000 | 0.013 | 0.808 | 0.000 |
| 1800 | PYOKED | 27 | 0.862 | 0.023 | 0.499 | 0.500 | 0.001 | 0.997 | 0.000 | 0.008 | 0.848 | -0.000 |
| 1800 | PNOFATE | 28 | 0.882 | 0.000 | 0.498 | 0.501 | 0.000 | 0.998 | 0.000 | 0.009 | 0.670 | 0.000 |
| 3600 | PFATE | 24 | 0.912 | 0.020 | 0.502 | 0.497 | 0.001 | 0.997 | 0.000 | 0.007 | 0.843 | -0.001 |
| 3600 | PYOKED | 24 | 0.892 | 0.020 | 0.500 | 0.500 | 0.000 | 0.997 | 0.000 | 0.007 | 0.870 | -0.000 |
| 3600 | PNOFATE | 27 | 0.895 | 0.000 | 0.499 | 0.501 | 0.000 | 0.998 | 0.000 | 0.008 | 0.672 | 0.000 |

At 1800: usable pairs 20; P1b-0 gate PASS (yoked evidence effect positive in 25/28, needed 19).
- P1b-1 drain effect, PFATE against PYOKED, usable pairs: 6/19 (p 0.1671; 0.000 against 0.000) NO_DIFFERENCE_DETECTED
- P1b-2 drain effect, PFATE against PNOFATE: 15/28 (p 0.8506; 0.000 against 0.000) NO_DIFFERENCE_DETECTED
- P1b-3 steering in PFATE: 14/27 (p 1.0000; median 0.000) NOT_DETECTED
- Monitoring route (noise effect), per arm: PFATE 27/28 (p 0.0000; median 0.013) PRESENT; PYOKED 24/28 (p 0.0002; median 0.008) PRESENT; PNOFATE 28/28 (p 0.0000; median 0.009) PRESENT
- Monitoring, PFATE against PYOKED: 23/28 (p 0.0009; 0.013 against 0.008) DERIVED_AHEAD
- Monitoring, PYOKED against PNOFATE: 14/28 (p 1.0000; 0.008 against 0.009) NO_DIFFERENCE_DETECTED
- Drain route, per arm: PFATE 17/25 (p 0.1078; median 0.000) NOT_DETECTED; PYOKED 18/23 (p 0.0106; median 0.000) PRESENT; PNOFATE 15/24 (p 0.3075; median 0.000) NOT_DETECTED
- Drain effect, PFATE against PYOKED, all seeds: 11/27 (p 0.4421; 0.000 against 0.000) NO_DIFFERENCE_DETECTED
- In-band time, PFATE against PNOFATE: 17/28 (p 0.3449; 0.912 against 0.882) NO_DIFFERENCE_DETECTED
- In-band time, PFATE against PYOKED: 22/28 (p 0.0037; 0.912 against 0.862) FATE_AHEAD

At 3600: usable pairs 19; P1b-0 gate PASS (yoked evidence effect positive in 22/28, needed 19).
- P1b-1 drain effect, PFATE against PYOKED, usable pairs: 7/17 (p 0.6291; 0.000 against 0.000) NO_DIFFERENCE_DETECTED
- P1b-2 drain effect, PFATE against PNOFATE: 14/27 (p 1.0000; 0.000 against 0.000) NO_DIFFERENCE_DETECTED
- P1b-3 steering in PFATE: 10/26 (p 0.3269; median -0.001) NOT_DETECTED
- Monitoring route (noise effect), per arm: PFATE 23/26 (p 0.0001; median 0.008) PRESENT; PYOKED 20/26 (p 0.0094; median 0.008) PRESENT; PNOFATE 28/28 (p 0.0000; median 0.008) PRESENT
- Monitoring, PFATE against PYOKED: 15/27 (p 0.7011; 0.007 against 0.007) NO_DIFFERENCE_DETECTED
- Monitoring, PYOKED against PNOFATE: 13/28 (p 0.8506; 0.007 against 0.008) NO_DIFFERENCE_DETECTED
- Drain route, per arm: PFATE 17/21 (p 0.0072; median 0.000) PRESENT; PYOKED 18/24 (p 0.0227; median 0.000) PRESENT; PNOFATE 18/26 (p 0.0755; median 0.000) NOT_DETECTED
- Drain effect, PFATE against PYOKED, all seeds: 10/26 (p 0.3269; 0.000 against 0.000) NO_DIFFERENCE_DETECTED
- In-band time, PFATE against PNOFATE: 15/28 (p 0.8506; 0.912 against 0.895) NO_DIFFERENCE_DETECTED
- In-band time, PFATE against PYOKED: 14/28 (p 1.0000; 0.912 against 0.892) NO_DIFFERENCE_DETECTED
