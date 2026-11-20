# Track C P1c: unhardenable precarious computation and the referent of self-evaluation

**Overall: NOT_ESTABLISHED.** Holm-adjusted p: P1C_1 0.3699, P1C_2 0.3699, P1C_3 0.0005.

Valid: True (phase 1: clear correct-report rate 0.999, needed >= 0.8; report accuracy under the overwrite probe 0.528, needed <= 0.7; PFATE clear trials below break-even 0.047, needed >= 0.02). Parameters: 34449. Overwrite probability per step: min(0.3, 1.0 x gain).

| updates | arm | regulators | in band | mean gain | below break-even | abstain | correct | wrong | evidence effect | drain effect | overwrite effect | accuracy under overwrite | steer effect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 28 | 0.937 | 0.024 | 0.059 | 0.512 | 0.476 | 0.012 | 0.890 | 0.040 | 0.225 | 0.525 | 0.143 |
| 1800 | PYOKED | 28 | 0.789 | 0.024 | 0.059 | 0.504 | 0.480 | 0.013 | 0.990 | 0.000 | 0.236 | 0.530 | -0.004 |
| 1800 | PNOFATE | 27 | 0.880 | 0.000 | 0.000 | 0.502 | 0.498 | 0.000 | 0.998 | 0.000 | 0.233 | 0.528 | 0.014 |
| 3600 | PFATE | 28 | 0.947 | 0.016 | 0.047 | 0.507 | 0.483 | 0.009 | 0.913 | 0.018 | 0.226 | 0.523 | 0.087 |
| 3600 | PYOKED | 28 | 0.856 | 0.016 | 0.045 | 0.504 | 0.486 | 0.010 | 0.995 | -0.000 | 0.236 | 0.527 | -0.023 |
| 3600 | PNOFATE | 27 | 0.892 | 0.000 | 0.000 | 0.502 | 0.498 | 0.000 | 0.998 | 0.000 | 0.240 | 0.526 | 0.019 |

At 1800: usable pairs 9; P1c-0 gate PASS (yoked evidence effect positive in 28/28, needed 19).
- P1c-1 drain effect, PFATE against PYOKED, all seeds: 20/28 (p 0.0357; 0.040 against 0.000) DERIVED_AHEAD
- P1c-2 drain effect, PFATE against PNOFATE: 20/28 (p 0.0357; 0.040 against 0.000) DERIVED_AHEAD
- P1c-3 steering in PFATE: 23/28 (p 0.0009; median 0.143) CAUSAL
- Monitoring route (overwrite effect), per arm: PFATE 28/28 (p 0.0000; median 0.225) PRESENT; PYOKED 28/28 (p 0.0000; median 0.236) PRESENT; PNOFATE 28/28 (p 0.0000; median 0.233) PRESENT
- Monitoring, PFATE against PYOKED: 14/28 (p 1.0000; 0.225 against 0.236) NO_DIFFERENCE_DETECTED
- Monitoring, PYOKED against PNOFATE: 11/28 (p 0.3449; 0.236 against 0.233) NO_DIFFERENCE_DETECTED
- Drain route, per arm: PFATE 20/28 (p 0.0357; median 0.040) PRESENT; PYOKED 14/28 (p 1.0000; median 0.000) NOT_DETECTED; PNOFATE 9/19 (p 1.0000; median -0.000) NOT_DETECTED
- Drain effect, PFATE against PYOKED, usable pairs: 8/9 (p 0.0391; 0.048 against 0.000) UNDETERMINED
- In-band time, PFATE against PNOFATE: 24/28 (p 0.0002; 0.937 against 0.880) FATE_AHEAD
- In-band time, PFATE against PYOKED: 26/28 (p 0.0000; 0.937 against 0.789) FATE_AHEAD

At 3600: usable pairs 16; P1c-0 gate PASS (yoked evidence effect positive in 28/28, needed 19).
- P1c-1 drain effect, PFATE against PYOKED, all seeds: 18/28 (p 0.1849; 0.018 against -0.000) NO_DIFFERENCE_DETECTED
- P1c-2 drain effect, PFATE against PNOFATE: 18/28 (p 0.1849; 0.018 against 0.000) NO_DIFFERENCE_DETECTED
- P1c-3 steering in PFATE: 24/28 (p 0.0002; median 0.087) CAUSAL
- Monitoring route (overwrite effect), per arm: PFATE 28/28 (p 0.0000; median 0.226) PRESENT; PYOKED 28/28 (p 0.0000; median 0.236) PRESENT; PNOFATE 28/28 (p 0.0000; median 0.240) PRESENT
- Monitoring, PFATE against PYOKED: 11/28 (p 0.3449; 0.226 against 0.236) NO_DIFFERENCE_DETECTED
- Monitoring, PYOKED against PNOFATE: 13/28 (p 0.8506; 0.236 against 0.240) NO_DIFFERENCE_DETECTED
- Drain route, per arm: PFATE 18/28 (p 0.1849; median 0.018) NOT_DETECTED; PYOKED 13/28 (p 0.8506; median -0.000) NOT_DETECTED; PNOFATE 18/25 (p 0.0433; median 0.000) PRESENT
- Drain effect, PFATE against PYOKED, usable pairs: 9/16 (p 0.8036; 0.031 against 0.000) NO_DIFFERENCE_DETECTED
- In-band time, PFATE against PNOFATE: 23/28 (p 0.0009; 0.947 against 0.892) FATE_AHEAD
- In-band time, PFATE against PYOKED: 27/28 (p 0.0000; 0.947 against 0.856) FATE_AHEAD
