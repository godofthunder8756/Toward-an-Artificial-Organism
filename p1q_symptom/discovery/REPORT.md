# P1q discovery: the integrity monitor and self-maintenance with a blind body, P1g's seeds (3200-3207)

**Overall: INVALID** (P1o's frozen rules, with P1g's validity on the trained agents). Interoceptive noise SD 100.0. Seeds: 8.

- P1g on these agents: valid True (memory True, damage True, exposure True; phase-1 clear correct 1.000, exposure 0.313); P1g overall UNDETERMINED, arrow UNDETERMINED.
- P1G_1 monitor learned: M, PFATE against PNOFATE: 8/8 (sign p 0.0078, Holm n/a; 0.7064 against 0.0011) UNDETERMINED
- P1G_3 monitor, PFATE against PYOKED: 4/8 (sign p 1.0000, Holm n/a; 0.7064 against 0.6885) UNDETERMINED
- regulation: in band, PFATE against PYOKED: 2/8 (sign p 0.2891, Holm n/a; 0.3565 against 0.3524) UNDETERMINED
- regulation: in band, PFATE against PNOFATE: 0/8 (sign p 0.0078, Holm n/a; 0.3565 against 0.3963) UNDETERMINED
- in band, PFATE / PYOKED / PNOFATE: 0.357 / 0.352 / 0.396

## Coupling (P1o's analysis and rules)

**Overall: INVALID.** Valid: False (fitted seeds {'PFATE': 8, 'PYOKED': 8, 'PNOFATE': 8}, needed >= 20 for PFATE and PYOKED; room, PFATE median >= 0.05: False). Seeds: 8. Point: 3600. Foraging drive f per delay step in [-1, 1]; F = mean over delay steps 2-8; low side: true energy at delay step 1 below 0.5; signed = low side - high side.

| measure | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| M_signed | 0.0051 | 0.0056 | -0.0037 |
| steer_signed | -0.0023 | -0.0002 | -0.0015 |
| M_conf | 0.0098 | 0.0018 | 0.0015 |
| M_conf_high | 0.0055 | -0.0017 | 0.0029 |
| M_none | 0.0088 | -0.0008 | 0.0017 |
| F_conflict | 0.0347 | 0.0291 | 0.0444 |
| F_same | 0.0274 | 0.0302 | 0.0437 |
| F_none | 0.0255 | 0.0307 | 0.0459 |
| M_nat | 0.0140 | -0.0042 | n/a |
| steer | 0.0042 | -0.0010 | -0.0042 |
| induce | 0.0061 | 0.0022 | -0.0000 |
| rescue | 0.0017 | -0.0004 | -0.0073 |
| random_none | -0.0001 | -0.0010 | -0.0008 |
| steer_high | 0.0089 | -0.0028 | 0.0005 |
| room | 0.0979 | 0.0307 | n/a |
| p_out_event | 0.9460 | 0.7419 | n/a |
| p_out_all | 0.4391 | 0.5880 | n/a |
| norm_d | 1.8868 | 1.7284 | 0.2607 |

## Tests

- P1O_1 body-appropriate coupling: M_signed = M_conf(low) - M_conf(high), PFATE: 5/8 > 0 (sign p 0.7266, Holm 1.0000; median 0.0051) UNDETERMINED
- P1O_2 precarity: M_signed, PFATE against PYOKED: 3/8 (sign p 0.7266, Holm 1.0000; 0.0051 against 0.0056) UNDETERMINED
- P1O_3 cause: steer_signed = steer(low) - steer(high), PFATE: 4/8 > 0 (sign p 1.0000, Holm 1.0000; median -0.0023) UNDETERMINED
- room: P(out of band | event) - P(out | no event) at the shown reading, PFATE: 8/8 > 0 (sign p 0.0078, Holm n/a; median 0.0979) UNDETERMINED
- v1_P1O_1_M_conf_PFATE: 6/8 > 0 (sign p 0.2891, Holm n/a; median 0.0098) UNDETERMINED
- v1_P1O_2_M_conf_PFATE_vs_PYOKED: 6/8 (sign p 0.2891, Holm n/a; 0.0098 against 0.0018) UNDETERMINED
- v1_P1O_3_steer_PFATE: 5/8 > 0 (sign p 0.7266, Holm n/a; median 0.0042) UNDETERMINED
- M_signed_PYOKED: 5/8 > 0 (sign p 0.7266, Holm n/a; median 0.0056) UNDETERMINED
- M_signed_PNOFATE: 3/8 > 0 (sign p 0.7266, Holm n/a; median -0.0037) UNDETERMINED
- M_signed_PFATE_vs_PNOFATE: 4/8 (sign p 1.0000, Holm n/a; 0.0051 against -0.0037) UNDETERMINED
- steer_signed_PFATE_vs_PYOKED: 3/8 (sign p 0.7266, Holm n/a; -0.0023 against -0.0002) UNDETERMINED
- steer_signed_PYOKED: 4/8 > 0 (sign p 1.0000, Holm n/a; median -0.0002) UNDETERMINED
- steer_signed_PNOFATE: 4/8 > 0 (sign p 1.0000, Holm n/a; median -0.0015) UNDETERMINED
- steer_high_PFATE: 6/8 > 0 (sign p 0.2891, Holm n/a; median 0.0089) UNDETERMINED
- M_conf_PYOKED: 5/8 > 0 (sign p 0.7266, Holm n/a; median 0.0018) UNDETERMINED
- M_conf_PNOFATE: 4/8 > 0 (sign p 1.0000, Holm n/a; median 0.0015) UNDETERMINED
- M_conf_PFATE_vs_PNOFATE: 6/8 (sign p 0.2891, Holm n/a; 0.0098 against 0.0015) UNDETERMINED
- M_nat_PFATE: 7/8 > 0 (sign p 0.0703, Holm n/a; median 0.0140) UNDETERMINED
- M_nat_PYOKED: 3/8 > 0 (sign p 0.7266, Holm n/a; median -0.0042) UNDETERMINED
- M_nat_PFATE_vs_PYOKED: 8/8 (sign p 0.0078, Holm n/a; 0.0140 against -0.0042) UNDETERMINED
- steer_PFATE_vs_PYOKED: 6/8 (sign p 0.2891, Holm n/a; 0.0042 against -0.0010) UNDETERMINED
- induce_PFATE: 5/8 > 0 (sign p 0.7266, Holm n/a; median 0.0061) UNDETERMINED
- rescue_PFATE: 6/8 > 0 (sign p 0.2891, Holm n/a; median 0.0017) UNDETERMINED
- steer_PYOKED: 4/8 > 0 (sign p 1.0000, Holm n/a; median -0.0010) UNDETERMINED
- steer_PNOFATE: 2/8 > 0 (sign p 0.2891, Holm n/a; median -0.0042) UNDETERMINED
- M_conf_high_PFATE: 5/8 > 0 (sign p 0.7266, Holm n/a; median 0.0055) UNDETERMINED
- M_none_PFATE: 5/8 > 0 (sign p 0.7266, Holm n/a; median 0.0088) UNDETERMINED
- room_PYOKED: 8/8 > 0 (sign p 0.0078, Holm n/a; median 0.0307) UNDETERMINED
- room_PFATE_vs_PYOKED: 8/8 (sign p 0.0078, Holm n/a; 0.0979 against 0.0307) UNDETERMINED
