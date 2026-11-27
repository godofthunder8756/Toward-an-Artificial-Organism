# P1o discovery: the integrity monitor and self-maintenance, P1g's seeds (3200-3227)

**Overall: COUPLED_NOT_CAUSAL.** Valid: True (fitted seeds {'PFATE': 28, 'PYOKED': 28, 'PNOFATE': 28}, needed >= 20 for PFATE and PYOKED; room, PFATE median >= 0.05: True). Seeds: 28. Point: 3600. Foraging drive f per delay step in [-1, 1]; F = mean over delay steps 2-8; low side: true energy at delay step 1 below 0.5; signed = low side - high side.

| measure | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| M_signed | 0.0109 | 0.0031 | 0.0020 |
| steer_signed | 0.0023 | -0.0049 | -0.0014 |
| M_conf | 0.0059 | -0.0190 | 0.0005 |
| M_conf_high | -0.0048 | -0.0195 | -0.0003 |
| M_none | 0.0004 | -0.0307 | -0.0096 |
| F_conflict | 0.0886 | 0.0664 | 0.0795 |
| F_same | 0.0796 | 0.0839 | 0.0805 |
| F_none | 0.0867 | 0.0948 | 0.0910 |
| M_nat | -0.0005 | -0.0105 | n/a |
| steer | 0.0025 | -0.0101 | 0.0009 |
| induce | 0.0055 | -0.0069 | 0.0003 |
| rescue | -0.0077 | -0.0116 | -0.0011 |
| random_none | -0.0052 | -0.0024 | 0.0015 |
| steer_high | 0.0005 | -0.0042 | 0.0021 |
| room | 0.3009 | 0.0014 | n/a |
| p_out_event | 0.3710 | 0.1128 | n/a |
| p_out_all | 0.0479 | 0.1038 | n/a |
| norm_d | 1.1558 | 1.1733 | 0.1229 |

## Tests

- P1O_1 body-appropriate coupling: M_signed = M_conf(low) - M_conf(high), PFATE: 25/28 > 0 (sign p 0.0000, Holm 0.0001; median 0.0109) PRESENT
- P1O_2 precarity: M_signed, PFATE against PYOKED: 21/28 (sign p 0.0125, Holm 0.0251; 0.0109 against 0.0031) FATE_AHEAD
- P1O_3 cause: steer_signed = steer(low) - steer(high), PFATE: 15/28 > 0 (sign p 0.8506, Holm 0.8506; median 0.0023) NOT_DETECTED
- room: P(out of band | event) - P(out | no event) at the shown reading, PFATE: 28/28 > 0 (sign p 0.0000, Holm n/a; median 0.3009) PRESENT
- v1_P1O_1_M_conf_PFATE: 19/28 > 0 (sign p 0.0872, Holm n/a; median 0.0059) NOT_DETECTED
- v1_P1O_2_M_conf_PFATE_vs_PYOKED: 25/28 (sign p 0.0000, Holm n/a; 0.0059 against -0.0190) FATE_AHEAD
- v1_P1O_3_steer_PFATE: 17/28 > 0 (sign p 0.3449, Holm n/a; median 0.0025) NOT_DETECTED
- M_signed_PYOKED: 15/28 > 0 (sign p 0.8506, Holm n/a; median 0.0031) NOT_DETECTED
- M_signed_PNOFATE: 18/28 > 0 (sign p 0.1849, Holm n/a; median 0.0020) NOT_DETECTED
- M_signed_PFATE_vs_PNOFATE: 25/28 (sign p 0.0000, Holm n/a; 0.0109 against 0.0020) FATE_AHEAD
- steer_signed_PFATE_vs_PYOKED: 18/28 (sign p 0.1849, Holm n/a; 0.0023 against -0.0049) NO_DIFFERENCE_DETECTED
- steer_signed_PYOKED: 7/28 > 0 (sign p 0.0125, Holm n/a; median -0.0049) REVERSED
- steer_signed_PNOFATE: 13/28 > 0 (sign p 0.8506, Holm n/a; median -0.0014) NOT_DETECTED
- steer_high_PFATE: 16/28 > 0 (sign p 0.5716, Holm n/a; median 0.0005) NOT_DETECTED
- M_conf_PYOKED: 8/28 > 0 (sign p 0.0357, Holm n/a; median -0.0190) REVERSED
- M_conf_PNOFATE: 17/28 > 0 (sign p 0.3449, Holm n/a; median 0.0005) NOT_DETECTED
- M_conf_PFATE_vs_PNOFATE: 19/28 (sign p 0.0872, Holm n/a; 0.0059 against 0.0005) NO_DIFFERENCE_DETECTED
- M_nat_PFATE: 14/28 > 0 (sign p 1.0000, Holm n/a; median -0.0005) NOT_DETECTED
- M_nat_PYOKED: 10/28 > 0 (sign p 0.1849, Holm n/a; median -0.0105) NOT_DETECTED
- M_nat_PFATE_vs_PYOKED: 20/28 (sign p 0.0357, Holm n/a; -0.0005 against -0.0105) FATE_AHEAD
- steer_PFATE_vs_PYOKED: 22/28 (sign p 0.0037, Holm n/a; 0.0025 against -0.0101) FATE_AHEAD
- induce_PFATE: 20/28 > 0 (sign p 0.0357, Holm n/a; median 0.0055) PRESENT
- rescue_PFATE: 10/28 > 0 (sign p 0.1849, Holm n/a; median -0.0077) NOT_DETECTED
- steer_PYOKED: 9/28 > 0 (sign p 0.0872, Holm n/a; median -0.0101) NOT_DETECTED
- steer_PNOFATE: 16/28 > 0 (sign p 0.5716, Holm n/a; median 0.0009) NOT_DETECTED
- M_conf_high_PFATE: 7/28 > 0 (sign p 0.0125, Holm n/a; median -0.0048) REVERSED
- M_none_PFATE: 14/28 > 0 (sign p 1.0000, Holm n/a; median 0.0004) NOT_DETECTED
- room_PYOKED: 17/28 > 0 (sign p 0.3449, Holm n/a; median 0.0014) NOT_DETECTED
- room_PFATE_vs_PYOKED: 28/28 (sign p 0.0000, Holm n/a; 0.3009 against 0.0014) FATE_AHEAD
