# Track C P1g: self-monitoring with exposure fixed by design and graded damage (Layer 0 -> Layer 4)

**Overall: MONITOR_SECOND_ORDER.** L0 reading: EXPOSURE_SUFFICES. Hardened (PFATE accuracy under the conflict probe > 0.75): False. Holm-adjusted p: P1G_1 0.0000, P1G_2 0.0000, P1G_3 0.8506.

Valid: True (phase 1: clear correct 0.999, needed >= 0.8; accuracy under the conflict probe 0.507, needed <= 0.7 (same probe 1.000); PFATE clear trials with a conflict event 0.072, needed >= 0.02). Parameters: 34449. Damage: per-step probability min(0.3, base 0.012 + 1.0 x gain), K units from a donor with K in [9, 18, 26, 35], once per trial. Split probe A (K 35, drain on half) and graded probe B (K in [9, 18, 26, 35], no drain) at delay step 1 (early) and 8 (late) on 0.667 of the trials. Caliper 0.05 pooled SD, at least 20 pairs. Drain shift 0.15.

| updates | arm | M | M_early | M_late | M2_nn_own | M2_nn_own_early | M2_nn_own_late | coverage_nn_own | balance_own | M2_nn_lda | M2_bins_own | own_conflict | own_same | M_k9 | M_k18 | M_k26 | M_k35 | Q_early | acc_conflict | drain_effect | share_conflict | in_band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 0.496 | 0.548 | 0.380 | 0.003 | 0.005 | 0.002 | 0.455 | -0.003 | 0.003 | 0.007 | 6.846 | 10.926 | 0.049 | 0.219 | 0.391 | 0.511 | 0.000 | 0.524 | 0.001 | 0.076 | 0.906 |
| 1800 | PYOKED | 0.530 | 0.624 | 0.437 | 0.004 | 0.006 | 0.005 | 0.415 | -0.004 | 0.004 | 0.017 | 7.010 | 10.906 | 0.042 | 0.209 | 0.399 | 0.539 | 0.000 | 0.521 | 0.001 | 0.078 | 0.885 |
| 1800 | PNOFATE | 0.002 | 0.000 | 0.003 | 0.000 | 0.000 | 0.000 | 0.668 | -0.001 | 0.000 | 0.000 | 7.894 | 9.416 | 0.000 | 0.001 | 0.001 | 0.002 | 0.000 | 0.514 | 0.000 | 0.000 | 0.884 |
| 3600 | PFATE | 0.578 | 0.745 | 0.440 | 0.004 | 0.003 | 0.005 | 0.422 | -0.003 | 0.002 | 0.023 | 7.397 | 11.934 | 0.028 | 0.193 | 0.444 | 0.606 | 0.000 | 0.524 | 0.001 | 0.072 | 0.930 |
| 3600 | PYOKED | 0.581 | 0.699 | 0.494 | 0.004 | 0.001 | 0.006 | 0.421 | -0.003 | 0.003 | 0.006 | 8.287 | 11.768 | 0.015 | 0.160 | 0.423 | 0.574 | 0.000 | 0.523 | 0.001 | 0.070 | 0.889 |
| 3600 | PNOFATE | 0.001 | 0.000 | 0.002 | 0.000 | 0.000 | 0.000 | 0.651 | -0.001 | 0.000 | 0.000 | 8.153 | 9.686 | 0.000 | 0.000 | 0.001 | 0.001 | 0.000 | 0.510 | 0.000 | 0.000 | 0.888 |

## At 1800

- P1G-1 monitor confirmed, M PFATE against PNOFATE: 28/28 (p 0.0000; 0.496 against 0.002) DERIVED_AHEAD
- P1G-2 second order, M2_nn_own PFATE against 0: 20/28 (p 0.0357; median 0.003) PRESENT
- P1G-3 the L0 arrow, M PFATE against PYOKED: 10/28 (p 0.1849; 0.496 against 0.530) NO_DIFFERENCE_DETECTED
- M_early_PFATE_vs_PNOFATE: 28/28 (p 0.0000; 0.548 against 0.000) DERIVED_AHEAD
- M_PYOKED_vs_PNOFATE: 27/28 (p 0.0000; 0.530 against 0.002) DERIVED_AHEAD
- M2_nn_own_PFATE_vs_PYOKED: 11/28 (p 0.3449; 0.003 against 0.004) NO_DIFFERENCE_DETECTED
- M_conf_early_PFATE_vs_PNOFATE: 4/12 (p 0.3877; -0.002 against 0.000) UNDETERMINED
- drain_PFATE_vs_PYOKED: 16/28 (p 0.5716; 0.001 against 0.001) NO_DIFFERENCE_DETECTED
- regulation_PFATE_vs_PYOKED: 22/28 (p 0.0037; 0.906 against 0.885) FATE_AHEAD
- regulation_PFATE_vs_PNOFATE: 17/28 (p 0.3449; 0.906 against 0.884) NO_DIFFERENCE_DETECTED
- route M: PFATE 28/28 (p 0.0000; median 0.496) PRESENT; PYOKED 28/28 (p 0.0000; median 0.530) PRESENT; PNOFATE 24/26 (p 0.0000; median 0.002) PRESENT
- route M2_nn_own: PFATE 20/28 (p 0.0357; median 0.003) PRESENT; PYOKED 22/28 (p 0.0037; median 0.004) PRESENT; PNOFATE 11/13 (p 0.0225; median 0.000) UNDETERMINED
- route M2_nn_own_early: PFATE 23/27 (p 0.0003; median 0.005) PRESENT; PYOKED 23/26 (p 0.0001; median 0.007) PRESENT; PNOFATE 8/11 (p 0.2266; median 0.001) UNDETERMINED
- route M2_nn_own_late: PFATE 16/25 (p 0.2295; median 0.003) NOT_DETECTED; PYOKED 20/26 (p 0.0094; median 0.006) PRESENT; PNOFATE 7/8 (p 0.0703; median 0.001) UNDETERMINED
- route M2_nn_lda: PFATE 21/28 (p 0.0125; median 0.003) PRESENT; PYOKED 24/28 (p 0.0002; median 0.004) PRESENT; PNOFATE 12/16 (p 0.0768; median 0.000) NOT_DETECTED
- route M2_bins_own: PFATE 23/28 (p 0.0009; median 0.007) PRESENT; PYOKED 27/28 (p 0.0000; median 0.017) PRESENT; PNOFATE 16/22 (p 0.0525; median 0.000) NOT_DETECTED
- route Q_early: PFATE 13/26 (p 1.0000; median 0.000) NOT_DETECTED; PYOKED 14/26 (p 0.8450; median 0.000) NOT_DETECTED; PNOFATE 6/9 (p 0.5078; median 0.001) UNDETERMINED
- route nat_M: PFATE 28/28 (p 0.0000; median 0.380) PRESENT; PYOKED 28/28 (p 0.0000; median 0.346) PRESENT; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route M_k9: PFATE 27/27 (p 0.0000; median 0.049) PRESENT; PYOKED 28/28 (p 0.0000; median 0.042) PRESENT; PNOFATE 12/16 (p 0.0768; median 0.001) NOT_DETECTED
- route M_k18: PFATE 28/28 (p 0.0000; median 0.219) PRESENT; PYOKED 27/28 (p 0.0000; median 0.209) PRESENT; PNOFATE 19/23 (p 0.0026; median 0.002) PRESENT
- route M_k26: PFATE 28/28 (p 0.0000; median 0.391) PRESENT; PYOKED 28/28 (p 0.0000; median 0.399) PRESENT; PNOFATE 18/20 (p 0.0004; median 0.001) PRESENT
- route M_k35: PFATE 28/28 (p 0.0000; median 0.511) PRESENT; PYOKED 28/28 (p 0.0000; median 0.539) PRESENT; PNOFATE 20/21 (p 0.0000; median 0.002) PRESENT

## At 3600

- P1G-1 monitor confirmed, M PFATE against PNOFATE: 28/28 (p 0.0000; 0.578 against 0.001) DERIVED_AHEAD
- P1G-2 second order, M2_nn_own PFATE against 0: 25/27 (p 0.0000; median 0.005) PRESENT
- P1G-3 the L0 arrow, M PFATE against PYOKED: 15/28 (p 0.8506; 0.578 against 0.581) NO_DIFFERENCE_DETECTED
- M_early_PFATE_vs_PNOFATE: 28/28 (p 0.0000; 0.745 against 0.000) DERIVED_AHEAD
- M_PYOKED_vs_PNOFATE: 28/28 (p 0.0000; 0.581 against 0.001) DERIVED_AHEAD
- M2_nn_own_PFATE_vs_PYOKED: 14/28 (p 1.0000; 0.004 against 0.004) NO_DIFFERENCE_DETECTED
- M_conf_early_PFATE_vs_PNOFATE: 3/9 (p 0.5078; -0.002 against 0.000) UNDETERMINED
- drain_PFATE_vs_PYOKED: 17/28 (p 0.3449; 0.001 against 0.001) NO_DIFFERENCE_DETECTED
- regulation_PFATE_vs_PYOKED: 20/28 (p 0.0357; 0.930 against 0.889) FATE_AHEAD
- regulation_PFATE_vs_PNOFATE: 18/28 (p 0.1849; 0.930 against 0.888) NO_DIFFERENCE_DETECTED
- route M: PFATE 28/28 (p 0.0000; median 0.578) PRESENT; PYOKED 28/28 (p 0.0000; median 0.581) PRESENT; PNOFATE 23/24 (p 0.0000; median 0.001) PRESENT
- route M2_nn_own: PFATE 25/27 (p 0.0000; median 0.005) PRESENT; PYOKED 25/27 (p 0.0000; median 0.004) PRESENT; PNOFATE 8/16 (p 1.0000; median -0.000) NOT_DETECTED
- route M2_nn_own_early: PFATE 21/26 (p 0.0025; median 0.004) PRESENT; PYOKED 19/22 (p 0.0009; median 0.003) PRESENT; PNOFATE 6/14 (p 0.7905; median -0.001) NOT_DETECTED
- route M2_nn_own_late: PFATE 22/25 (p 0.0002; median 0.006) PRESENT; PYOKED 24/26 (p 0.0000; median 0.007) PRESENT; PNOFATE 7/10 (p 0.3438; median 0.001) UNDETERMINED
- route M2_nn_lda: PFATE 23/26 (p 0.0001; median 0.002) PRESENT; PYOKED 23/27 (p 0.0003; median 0.003) PRESENT; PNOFATE 12/14 (p 0.0129; median 0.001) PRESENT
- route M2_bins_own: PFATE 28/28 (p 0.0000; median 0.023) PRESENT; PYOKED 24/27 (p 0.0000; median 0.007) PRESENT; PNOFATE 12/20 (p 0.5034; median 0.000) NOT_DETECTED
- route Q_early: PFATE 12/24 (p 1.0000; median -0.000) NOT_DETECTED; PYOKED 11/22 (p 1.0000; median -0.000) NOT_DETECTED; PNOFATE 5/8 (p 0.7266; median 0.001) UNDETERMINED
- route nat_M: PFATE 28/28 (p 0.0000; median 0.362) PRESENT; PYOKED 28/28 (p 0.0000; median 0.354) PRESENT; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route M_k9: PFATE 28/28 (p 0.0000; median 0.028) PRESENT; PYOKED 27/28 (p 0.0000; median 0.015) PRESENT; PNOFATE 11/13 (p 0.0225; median 0.001) UNDETERMINED
- route M_k18: PFATE 28/28 (p 0.0000; median 0.193) PRESENT; PYOKED 27/27 (p 0.0000; median 0.161) PRESENT; PNOFATE 13/18 (p 0.0963; median 0.002) NOT_DETECTED
- route M_k26: PFATE 28/28 (p 0.0000; median 0.444) PRESENT; PYOKED 28/28 (p 0.0000; median 0.423) PRESENT; PNOFATE 17/18 (p 0.0001; median 0.002) PRESENT
- route M_k35: PFATE 28/28 (p 0.0000; median 0.606) PRESENT; PYOKED 28/28 (p 0.0000; median 0.574) PRESENT; PNOFATE 15/16 (p 0.0005; median 0.002) PRESENT
