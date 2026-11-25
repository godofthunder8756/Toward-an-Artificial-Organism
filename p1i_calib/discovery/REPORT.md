# P1i discovery: the P1i analysis on P1g's seeds (3200-3227)

**Overall: CALIBRATED_DISCOUNT_CONFIRMED.** Valid: True (evidence decoder held-out accuracy, PFATE: none 1.000, same 1.000, needed >= 0.95; P1g design valid: True). Seeds: 28. Point: 3600.

P1g replication on these seeds: overall MONITOR_SECOND_ORDER; L0 EXPOSURE_SUFFICES; P1G_1 28/28 DERIVED_AHEAD; P1G_2 25/27 PRESENT; P1G_3 15/28 NO_DIFFERENCE_DETECTED.

| arm | M2_E | rel_gap | own_gap | type2_resid | type2_raw | type2_ev_raw | type2_resid_pabs | trace_rho | coverage | dec_acc_conflict | agent_acc_conflict | M2_E_k9 | M2_E_k18 | M2_E_k26 | M2_E_k35 | rel_k9 | rel_k18 | rel_k26 | rel_k35 | dose_rho |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PFATE | 0.0995 | 0.0986 | 2.0604 | 0.6651 | 0.8094 | 0.5351 | 0.6408 | -0.6569 | 0.4736 | 0.7738 | 0.8199 | 0.0072 | 0.0736 | 0.1982 | 0.3349 | 0.9960 | 0.9646 | 0.8466 | 0.5128 | 1.0000 |
| PYOKED | 0.0743 | 0.0747 | 1.7465 | 0.6662 | 0.8181 | 0.5307 | 0.6367 | -0.5390 | 0.4823 | 0.7895 | 0.8303 | 0.0050 | 0.0502 | 0.1703 | 0.3139 | 0.9973 | 0.9766 | 0.8777 | 0.5041 | 1.0000 |
| PNOFATE | 0.0000 | 0.1991 | 0.2385 | 0.4959 | 0.6826 | 0.6892 | 0.4895 | -0.1270 | 0.6665 | 0.7239 | 0.7190 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.9674 | 0.8865 | 0.7527 | 0.5100 | 0.3000 |

- P1I_1 learned discount: M2_E, PFATE against PNOFATE: 28/28 (sign p 0.0000, Holm 0.0000; 0.0995 against 0.0000) DERIVED_AHEAD
- P1I_2 calibrated: type-2 AUC beyond evidence, PFATE against PNOFATE: 28/28 (sign p 0.0000, Holm 0.0000; 0.6651 against 0.4959) DERIVED_AHEAD
- P1I_3 warranted: reliability gap at matched evidence, PFATE against 0: 28/28 > 0 (sign p 0.0000, Holm 0.0000; median 0.0986) PRESENT
- M2_E_PFATE_vs_PYOKED: 18/28 (sign p 0.1849, Holm n/a; 0.0995 against 0.0743) NO_DIFFERENCE_DETECTED
- M2_E_PYOKED_vs_PNOFATE: 28/28 (sign p 0.0000, Holm n/a; 0.0743 against 0.0000) DERIVED_AHEAD
- type2_resid_PYOKED_vs_PNOFATE: 28/28 (sign p 0.0000, Holm n/a; 0.6662 against 0.4959) DERIVED_AHEAD
- type2_resid_pabs_PFATE_vs_PNOFATE: 28/28 (sign p 0.0000, Holm n/a; 0.6408 against 0.4895) DERIVED_AHEAD
- own_gap_PFATE_vs_PNOFATE: 28/28 (sign p 0.0000, Holm n/a; 2.0604 against 0.2385) DERIVED_AHEAD
- trace_rho_PFATE_more_negative: 28/28 (sign p 0.0000, Holm n/a; -0.1270 against -0.6569) DERIVED_AHEAD
- route M2_E: PFATE 28/28 (p 0.0000; median 0.0995) PRESENT; PYOKED 28/28 (p 0.0000; median 0.0743) PRESENT; PNOFATE 15/28 (p 0.8506; median 0.0000) NOT_DETECTED
- route rel_gap: PFATE 28/28 (p 0.0000; median 0.0986) PRESENT; PYOKED 28/28 (p 0.0000; median 0.0747) PRESENT; PNOFATE 28/28 (p 0.0000; median 0.1991) PRESENT
- route own_gap: PFATE 28/28 (p 0.0000; median 2.0604) PRESENT; PYOKED 28/28 (p 0.0000; median 1.7465) PRESENT; PNOFATE 20/28 (p 0.0357; median 0.2385) PRESENT
- route dose_rho: PFATE 28/28 (p 0.0000; median 1.0000) PRESENT; PYOKED 28/28 (p 0.0000; median 1.0000) PRESENT; PNOFATE 16/28 (p 0.5716; median 0.3000) NOT_DETECTED
- route M2_E_k9: PFATE 27/28 (p 0.0000; median 0.0072) PRESENT; PYOKED 28/28 (p 0.0000; median 0.0050) PRESENT; PNOFATE 14/28 (p 1.0000; median 0.0000) NOT_DETECTED
- route M2_E_k18: PFATE 28/28 (p 0.0000; median 0.0736) PRESENT; PYOKED 28/28 (p 0.0000; median 0.0502) PRESENT; PNOFATE 14/28 (p 1.0000; median 0.0000) NOT_DETECTED
- route M2_E_k26: PFATE 28/28 (p 0.0000; median 0.1982) PRESENT; PYOKED 28/28 (p 0.0000; median 0.1703) PRESENT; PNOFATE 14/28 (p 1.0000; median 0.0000) NOT_DETECTED
- route M2_E_k35: PFATE 28/28 (p 0.0000; median 0.3349) PRESENT; PYOKED 28/28 (p 0.0000; median 0.3139) PRESENT; PNOFATE 16/28 (p 0.5716; median 0.0000) NOT_DETECTED
- route type2_resid: PFATE 28/28 (p 0.0000; median 0.1651) ABOVE_CHANCE; PYOKED 28/28 (p 0.0000; median 0.1662) ABOVE_CHANCE; PNOFATE 13/28 (p 0.8506; median -0.0041) NOT_DETECTED
- route type2_raw: PFATE 28/28 (p 0.0000; median 0.3094) ABOVE_CHANCE; PYOKED 28/28 (p 0.0000; median 0.3181) ABOVE_CHANCE; PNOFATE 28/28 (p 0.0000; median 0.1826) ABOVE_CHANCE
- route type2_resid_pabs: PFATE 28/28 (p 0.0000; median 0.1408) ABOVE_CHANCE; PYOKED 28/28 (p 0.0000; median 0.1367) ABOVE_CHANCE; PNOFATE 13/28 (p 0.8506; median -0.0105) NOT_DETECTED
