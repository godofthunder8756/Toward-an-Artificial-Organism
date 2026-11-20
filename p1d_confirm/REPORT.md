# Track C P1d: confirmation of the two-sided body referent (fresh seeds, pre-registered probes)

**Overall: CONFIRMED_ROUTED.** Natural discrimination (P1d-4): CONFIRMED. Holm-adjusted p: P1D_1 0.0000, P1D_2 0.0000, P1D_3 0.0125, P1D_4 0.0000.

Valid: True (phase 1: clear correct-report rate 0.999, needed >= 0.8; report accuracy under the overwrite probe 0.524, needed <= 0.7; PFATE clear trials below break-even 0.038, needed >= 0.02). Parameters: 34449. Overwrite probability per step: min(0.3, 1.0 x gain). Probe shift: 0.15.

| updates | arm | regulators | in band | below break-even | evidence effect | discrimination | worse effect | relief effect (out of band) | down effect | down: looks worse | down: looks better | overwrite effect | steer effect (worse direction) | in band under worse / relief / down |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 28 | 0.925 | 0.067 | 0.925 | 0.288 | 0.274 | -0.112 | 0.074 | 0.236 | -0.075 | 0.215 | 0.082 | 0.850 / 0.894 / 0.618 |
| 1800 | PYOKED | 28 | 0.799 | 0.067 | 0.991 | 0.154 | 0.002 | 0.000 | -0.000 | 0.001 | -0.002 | 0.234 | 0.012 | 0.829 / 0.734 / 0.718 |
| 1800 | PNOFATE | 28 | 0.889 | 0.000 | 0.998 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.242 | 0.001 | 0.875 / 0.813 / 0.633 |
| 3600 | PFATE | 28 | 0.956 | 0.038 | 0.933 | 0.225 | 0.242 | -0.056 | 0.031 | 0.182 | -0.061 | 0.223 | 0.067 | 0.834 / 0.934 / 0.514 |
| 3600 | PYOKED | 28 | 0.851 | 0.040 | 0.995 | 0.132 | 0.002 | 0.000 | 0.000 | 0.001 | -0.001 | 0.234 | 0.009 | 0.860 / 0.798 / 0.670 |
| 3600 | PNOFATE | 28 | 0.916 | 0.000 | 0.998 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.246 | -0.000 | 0.880 / 0.847 / 0.640 |

At 1800: usable pairs 8; P1d-0 gate PASS (yoked evidence effect positive in 28/28, needed 19).
- P1d-1 worse effect, PFATE against PYOKED: 28/28 (p 0.0000; 0.274 against 0.002) DERIVED_AHEAD
- P1d-2 worse effect, PFATE against PNOFATE: 28/28 (p 0.0000; 0.274 against 0.000) DERIVED_AHEAD
- P1d-3 steering in PFATE (own worse direction): 23/28 (p 0.0009; median 0.082) CAUSAL
- P1d-4 natural discrimination, PFATE against PYOKED: 27/28 (p 0.0000; 0.288 against 0.154) DERIVED_AHEAD
- Worse effect, usable pairs: 8/8 (p 0.0078; 0.354 against 0.001) UNDETERMINED
- Relief (out-of-band cue readings; abstention reduction), PFATE against PYOKED: 27/28 (p 0.0000; 0.112 against -0.000) DERIVED_AHEAD
- Relief, PFATE against PNOFATE: 28/28 (p 0.0000; 0.112 against -0.000) DERIVED_AHEAD
- Down drain, readings where it looks worse, PFATE against PYOKED: 28/28 (p 0.0000; 0.236 against 0.001) DERIVED_AHEAD
- Down drain, readings where it looks better (abstention reduction), PFATE against PYOKED: 25/28 (p 0.0000; 0.075 against 0.002) DERIVED_AHEAD
- Down drain, all trials (P1c's frozen probe), PFATE against PYOKED: 26/28 (p 0.0000; 0.074 against -0.000) DERIVED_AHEAD
- Worse route, per arm: PFATE 28/28 (p 0.0000; median 0.274) PRESENT; PYOKED 25/28 (p 0.0000; median 0.002) PRESENT; PNOFATE 18/23 (p 0.0106; median 0.000) PRESENT
- Monitoring route, per arm: PFATE 28/28 (p 0.0000; median 0.215) PRESENT; PYOKED 28/28 (p 0.0000; median 0.234) PRESENT; PNOFATE 28/28 (p 0.0000; median 0.242) PRESENT
- Monitoring, PFATE against PYOKED: 8/28 (p 0.0357; 0.215 against 0.234) YOKED_AHEAD
- Steering, per arm: PFATE 23/28 (p 0.0009; median 0.082) CAUSAL; PYOKED 17/28 (p 0.3449; median 0.012) NOT_DETECTED; PNOFATE 15/28 (p 0.8506; median 0.001) NOT_DETECTED
- In-band time, PFATE against PNOFATE: 17/28 (p 0.3449; 0.925 against 0.889) NO_DIFFERENCE_DETECTED
- In-band time, PFATE against PYOKED: 27/28 (p 0.0000; 0.925 against 0.799) FATE_AHEAD

At 3600: usable pairs 15; P1d-0 gate PASS (yoked evidence effect positive in 28/28, needed 19).
- P1d-1 worse effect, PFATE against PYOKED: 28/28 (p 0.0000; 0.242 against 0.002) DERIVED_AHEAD
- P1d-2 worse effect, PFATE against PNOFATE: 28/28 (p 0.0000; 0.242 against 0.000) DERIVED_AHEAD
- P1d-3 steering in PFATE (own worse direction): 21/28 (p 0.0125; median 0.067) CAUSAL
- P1d-4 natural discrimination, PFATE against PYOKED: 26/28 (p 0.0000; 0.225 against 0.132) DERIVED_AHEAD
- Worse effect, usable pairs: 15/15 (p 0.0001; 0.226 against 0.002) DERIVED_AHEAD
- Relief (out-of-band cue readings; abstention reduction), PFATE against PYOKED: 26/28 (p 0.0000; 0.056 against -0.000) DERIVED_AHEAD
- Relief, PFATE against PNOFATE: 26/28 (p 0.0000; 0.056 against -0.000) DERIVED_AHEAD
- Down drain, readings where it looks worse, PFATE against PYOKED: 28/28 (p 0.0000; 0.182 against 0.001) DERIVED_AHEAD
- Down drain, readings where it looks better (abstention reduction), PFATE against PYOKED: 24/28 (p 0.0002; 0.061 against 0.001) DERIVED_AHEAD
- Down drain, all trials (P1c's frozen probe), PFATE against PYOKED: 20/28 (p 0.0357; 0.031 against 0.000) DERIVED_AHEAD
- Worse route, per arm: PFATE 28/28 (p 0.0000; median 0.242) PRESENT; PYOKED 24/28 (p 0.0002; median 0.002) PRESENT; PNOFATE 13/20 (p 0.2632; median 0.000) NOT_DETECTED
- Monitoring route, per arm: PFATE 28/28 (p 0.0000; median 0.223) PRESENT; PYOKED 28/28 (p 0.0000; median 0.234) PRESENT; PNOFATE 28/28 (p 0.0000; median 0.246) PRESENT
- Monitoring, PFATE against PYOKED: 9/28 (p 0.0872; 0.223 against 0.234) NO_DIFFERENCE_DETECTED
- Steering, per arm: PFATE 21/28 (p 0.0125; median 0.067) CAUSAL; PYOKED 15/28 (p 0.8506; median 0.009) NOT_DETECTED; PNOFATE 13/27 (p 1.0000; median -0.000) NOT_DETECTED
- In-band time, PFATE against PNOFATE: 27/28 (p 0.0000; 0.956 against 0.916) FATE_AHEAD
- In-band time, PFATE against PYOKED: 28/28 (p 0.0000; 0.956 against 0.851) FATE_AHEAD
