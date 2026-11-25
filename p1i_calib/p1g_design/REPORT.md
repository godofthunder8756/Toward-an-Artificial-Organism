# P1i: replication of P1g's design (seeds 3400-3427): self-monitoring with exposure fixed by design and graded damage (Layer 0 -> Layer 4)

**Overall: MONITOR_SECOND_ORDER.** L0 reading: EXPOSURE_SUFFICES. Hardened (PFATE accuracy under the conflict probe > 0.75): False. Holm-adjusted p: P1G_1 0.0000, P1G_2 0.0000, P1G_3 0.8450.

Valid: True (phase 1: clear correct 0.999, needed >= 0.8; accuracy under the conflict probe 0.511, needed <= 0.7 (same probe 1.000); PFATE clear trials with a conflict event 0.072, needed >= 0.02). Parameters: 34449. Damage: per-step probability min(0.3, base 0.012 + 1.0 x gain), K units from a donor with K in [9, 18, 26, 35], once per trial. Split probe A (K 35, drain on half) and graded probe B (K in [9, 18, 26, 35], no drain) at delay step 1 (early) and 8 (late) on 0.667 of the trials. Caliper 0.05 pooled SD, at least 20 pairs. Drain shift 0.15.

| updates | arm | M | M_early | M_late | M2_nn_own | M2_nn_own_early | M2_nn_own_late | coverage_nn_own | balance_own | M2_nn_lda | M2_bins_own | own_conflict | own_same | M_k9 | M_k18 | M_k26 | M_k35 | Q_early | acc_conflict | drain_effect | share_conflict | in_band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 0.500 | 0.638 | 0.340 | 0.004 | 0.001 | 0.006 | 0.396 | -0.002 | 0.003 | 0.009 | 6.721 | 11.024 | 0.070 | 0.243 | 0.413 | 0.526 | 0.000 | 0.514 | 0.000 | 0.080 | 0.890 |
| 1800 | PYOKED | 0.507 | 0.609 | 0.334 | 0.004 | 0.002 | 0.003 | 0.424 | -0.003 | 0.002 | 0.009 | 7.277 | 11.306 | 0.040 | 0.195 | 0.374 | 0.509 | 0.000 | 0.514 | 0.000 | 0.082 | 0.870 |
| 1800 | PNOFATE | 0.001 | 0.001 | 0.001 | 0.000 | 0.000 | 0.000 | 0.637 | -0.001 | 0.000 | 0.000 | 7.749 | 9.291 | 0.000 | 0.001 | 0.001 | 0.001 | 0.000 | 0.507 | 0.001 | 0.000 | 0.894 |
| 3600 | PFATE | 0.532 | 0.673 | 0.372 | 0.004 | 0.003 | 0.006 | 0.435 | -0.003 | 0.001 | 0.017 | 7.764 | 11.961 | 0.027 | 0.185 | 0.424 | 0.550 | 0.000 | 0.524 | 0.000 | 0.072 | 0.918 |
| 3600 | PYOKED | 0.544 | 0.699 | 0.415 | 0.003 | 0.003 | 0.002 | 0.428 | -0.004 | 0.002 | 0.007 | 8.104 | 12.474 | 0.011 | 0.146 | 0.417 | 0.585 | 0.000 | 0.524 | 0.000 | 0.073 | 0.876 |
| 3600 | PNOFATE | 0.002 | 0.001 | 0.002 | 0.000 | 0.000 | 0.000 | 0.645 | -0.001 | 0.000 | 0.000 | 7.955 | 9.403 | 0.000 | 0.001 | 0.002 | 0.001 | 0.000 | 0.506 | 0.000 | 0.000 | 0.890 |

## At 1800

- P1G-1 monitor confirmed, M PFATE against PNOFATE: 26/27 (p 0.0000; 0.501 against 0.002) DERIVED_AHEAD
- P1G-2 second order, M2_nn_own PFATE against 0: 20/27 (p 0.0192; median 0.004) PRESENT
- P1G-3 the L0 arrow, M PFATE against PYOKED: 14/27 (p 1.0000; 0.501 against 0.517) NO_DIFFERENCE_DETECTED
- M_early_PFATE_vs_PNOFATE: 26/27 (p 0.0000; 0.641 against 0.001) DERIVED_AHEAD
- M_PYOKED_vs_PNOFATE: 26/28 (p 0.0000; 0.507 against 0.001) DERIVED_AHEAD
- M2_nn_own_PFATE_vs_PYOKED: 17/27 (p 0.2478; 0.004 against 0.004) NO_DIFFERENCE_DETECTED
- M_conf_early_PFATE_vs_PNOFATE: 8/19 (p 0.6476; 0.000 against 0.000) NO_DIFFERENCE_DETECTED
- drain_PFATE_vs_PYOKED: 14/27 (p 1.0000; 0.000 against 0.000) NO_DIFFERENCE_DETECTED
- regulation_PFATE_vs_PYOKED: 18/28 (p 0.1849; 0.890 against 0.870) NO_DIFFERENCE_DETECTED
- regulation_PFATE_vs_PNOFATE: 15/28 (p 0.8506; 0.890 against 0.894) NO_DIFFERENCE_DETECTED
- route M: PFATE 26/26 (p 0.0000; median 0.503) PRESENT; PYOKED 26/27 (p 0.0000; median 0.517) PRESENT; PNOFATE 21/25 (p 0.0009; median 0.002) PRESENT
- route M2_nn_own: PFATE 20/27 (p 0.0192; median 0.004) PRESENT; PYOKED 21/27 (p 0.0059; median 0.004) PRESENT; PNOFATE 11/15 (p 0.1185; median 0.000) NOT_DETECTED
- route M2_nn_own_early: PFATE 15/23 (p 0.2100; median 0.002) NOT_DETECTED; PYOKED 22/27 (p 0.0015; median 0.003) PRESENT; PNOFATE 5/8 (p 0.7266; median 0.001) UNDETERMINED
- route M2_nn_own_late: PFATE 18/25 (p 0.0433; median 0.008) PRESENT; PYOKED 17/25 (p 0.1078; median 0.004) NOT_DETECTED; PNOFATE 9/10 (p 0.0215; median 0.001) UNDETERMINED
- route M2_nn_lda: PFATE 20/26 (p 0.0094; median 0.003) PRESENT; PYOKED 18/27 (p 0.1221; median 0.002) NOT_DETECTED; PNOFATE 11/16 (p 0.2101; median 0.001) NOT_DETECTED
- route M2_bins_own: PFATE 26/27 (p 0.0000; median 0.011) PRESENT; PYOKED 22/27 (p 0.0015; median 0.011) PRESENT; PNOFATE 12/23 (p 1.0000; median 0.000) NOT_DETECTED
- route Q_early: PFATE 12/25 (p 1.0000; median -0.000) NOT_DETECTED; PYOKED 11/21 (p 1.0000; median 0.001) NOT_DETECTED; PNOFATE 4/9 (p 1.0000; median -0.000) UNDETERMINED
- route nat_M: PFATE 26/27 (p 0.0000; median 0.401) PRESENT; PYOKED 25/26 (p 0.0000; median 0.363) PRESENT; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route M_k9: PFATE 24/26 (p 0.0000; median 0.076) PRESENT; PYOKED 25/26 (p 0.0000; median 0.041) PRESENT; PNOFATE 13/16 (p 0.0213; median 0.001) PRESENT
- route M_k18: PFATE 27/27 (p 0.0000; median 0.249) PRESENT; PYOKED 26/26 (p 0.0000; median 0.207) PRESENT; PNOFATE 18/21 (p 0.0015; median 0.002) PRESENT
- route M_k26: PFATE 26/27 (p 0.0000; median 0.418) PRESENT; PYOKED 25/27 (p 0.0000; median 0.379) PRESENT; PNOFATE 20/21 (p 0.0000; median 0.001) PRESENT
- route M_k35: PFATE 26/26 (p 0.0000; median 0.532) PRESENT; PYOKED 26/27 (p 0.0000; median 0.516) PRESENT; PNOFATE 17/19 (p 0.0007; median 0.002) PRESENT

## At 3600

- P1G-1 monitor confirmed, M PFATE against PNOFATE: 26/26 (p 0.0000; 0.544 against 0.002) DERIVED_AHEAD
- P1G-2 second order, M2_nn_own PFATE against 0: 23/25 (p 0.0000; median 0.005) PRESENT
- P1G-3 the L0 arrow, M PFATE against PYOKED: 12/26 (p 0.8450; 0.544 against 0.553) NO_DIFFERENCE_DETECTED
- M_early_PFATE_vs_PNOFATE: 26/26 (p 0.0000; 0.682 against 0.001) DERIVED_AHEAD
- M_PYOKED_vs_PNOFATE: 26/26 (p 0.0000; 0.553 against 0.002) DERIVED_AHEAD
- M2_nn_own_PFATE_vs_PYOKED: 18/27 (p 0.1221; 0.005 against 0.003) NO_DIFFERENCE_DETECTED
- M_conf_early_PFATE_vs_PNOFATE: 3/14 (p 0.0574; -0.002 against 0.000) NO_DIFFERENCE_DETECTED
- drain_PFATE_vs_PYOKED: 13/27 (p 1.0000; 0.000 against 0.000) NO_DIFFERENCE_DETECTED
- regulation_PFATE_vs_PYOKED: 23/28 (p 0.0009; 0.918 against 0.876) FATE_AHEAD
- regulation_PFATE_vs_PNOFATE: 20/28 (p 0.0357; 0.918 against 0.890) FATE_AHEAD
- route M: PFATE 26/26 (p 0.0000; median 0.544) PRESENT; PYOKED 26/26 (p 0.0000; median 0.553) PRESENT; PNOFATE 20/23 (p 0.0005; median 0.002) PRESENT
- route M2_nn_own: PFATE 23/25 (p 0.0000; median 0.005) PRESENT; PYOKED 20/26 (p 0.0094; median 0.003) PRESENT; PNOFATE 10/15 (p 0.3018; median 0.000) NOT_DETECTED
- route M2_nn_own_early: PFATE 22/24 (p 0.0000; median 0.004) PRESENT; PYOKED 21/23 (p 0.0001; median 0.004) PRESENT; PNOFATE 4/8 (p 1.0000; median -0.000) UNDETERMINED
- route M2_nn_own_late: PFATE 22/24 (p 0.0000; median 0.007) PRESENT; PYOKED 20/24 (p 0.0015; median 0.003) PRESENT; PNOFATE 8/10 (p 0.1094; median 0.001) UNDETERMINED
- route M2_nn_lda: PFATE 15/24 (p 0.3075; median 0.001) NOT_DETECTED; PYOKED 19/24 (p 0.0066; median 0.002) PRESENT; PNOFATE 12/18 (p 0.2379; median 0.001) NOT_DETECTED
- route M2_bins_own: PFATE 26/27 (p 0.0000; median 0.017) PRESENT; PYOKED 25/26 (p 0.0000; median 0.008) PRESENT; PNOFATE 11/21 (p 1.0000; median 0.000) NOT_DETECTED
- route Q_early: PFATE 11/24 (p 0.8388; median -0.000) NOT_DETECTED; PYOKED 12/17 (p 0.1435; median 0.001) NOT_DETECTED; PNOFATE 2/7 (p 0.4531; median -0.001) UNDETERMINED
- route nat_M: PFATE 26/26 (p 0.0000; median 0.383) PRESENT; PYOKED 26/26 (p 0.0000; median 0.364) PRESENT; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route M_k9: PFATE 26/27 (p 0.0000; median 0.028) PRESENT; PYOKED 26/26 (p 0.0000; median 0.011) PRESENT; PNOFATE 13/14 (p 0.0018; median 0.001) PRESENT
- route M_k18: PFATE 26/26 (p 0.0000; median 0.188) PRESENT; PYOKED 26/26 (p 0.0000; median 0.151) PRESENT; PNOFATE 20/21 (p 0.0000; median 0.002) PRESENT
- route M_k26: PFATE 26/26 (p 0.0000; median 0.427) PRESENT; PYOKED 26/27 (p 0.0000; median 0.423) PRESENT; PNOFATE 18/19 (p 0.0001; median 0.004) PRESENT
- route M_k35: PFATE 26/26 (p 0.0000; median 0.557) PRESENT; PYOKED 26/26 (p 0.0000; median 0.588) PRESENT; PNOFATE 17/20 (p 0.0026; median 0.002) PRESENT
