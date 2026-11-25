# P1h stage 1: residue at matched evidence, P1g's saved weights

**Overall: SECOND_ORDER_SURVIVES.** Valid: True (evidence decoder held-out accuracy, PFATE: none 1.000, same 1.000, needed >= 0.95; reproduction: {'runs': 168, 'mismatches': 0}). Thin (PFATE joint coverage < 0.25): False. Residue as a share of PFATE's unmatched conflict-same gap in p_abs (0.3088): 0.0022; within the leak range (< 0.005): True. Seeds: 28. Point: 3600.

| arm | M2_joint_p | coverage_joint | M2_E | M2_E_early | M2_E_late | coverage_E | balance_E | M2_E_sampled | M2_E_alt | M2_own_p | M2_own_sampled | M2_lda_p | ev_conflict | ev_same | pabs_conflict | pabs_same | dec_acc_conflict | trace_auc | trace_pair_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PFATE | 0.0007 | 0.2979 | 0.0995 | 0.1061 | 0.0893 | 0.4736 | -0.0017 | 0.0990 | 0.0995 | 0.0019 | 0.0040 | 0.0001 | 6.4948 | 7.8683 | 0.3095 | 0.0007 | 0.7738 | 0.9533 | 0.8827 |
| PYOKED | 0.0008 | 0.3173 | 0.0743 | 0.0621 | 0.0851 | 0.4823 | -0.0022 | 0.0787 | 0.0861 | 0.0017 | 0.0035 | 0.0001 | 6.6866 | 7.9124 | 0.2971 | 0.0008 | 0.7895 | 0.9552 | 0.8985 |
| PNOFATE | -0.0000 | 0.5778 | 0.0000 | -0.0000 | 0.0000 | 0.6665 | -0.0008 | 0.0000 | 0.0000 | -0.0000 | 0.0000 | 0.0000 | 6.3378 | 7.6746 | 0.0012 | 0.0002 | 0.7239 | 0.7816 | 0.6370 |

- P1H_1 residue at matched own margin and evidence: M2_joint_p of PFATE against 0: 24/28 > 0 (sign p 0.0002, Holm 0.0004; median 0.0007) PRESENT
- P1H_2 specific to damage training: M2_joint_p, PFATE against PNOFATE: 24/28 (sign p 0.0002, Holm 0.0004; 0.0007 against -0.0000) DERIVED_AHEAD
- M2_E_PYOKED_vs_PNOFATE: 28/28 (sign p 0.0000, Holm n/a; 0.0743 against 0.0000) DERIVED_AHEAD
- M2_E_PFATE_vs_PYOKED: 18/28 (sign p 0.1849, Holm n/a; 0.0995 against 0.0743) NO_DIFFERENCE_DETECTED
- route M2_E: PFATE 28/28 (p 0.0000; median 0.0995) PRESENT; PYOKED 28/28 (p 0.0000; median 0.0743) PRESENT; PNOFATE 15/28 (p 0.8506; median 0.0000) NOT_DETECTED
- route M2_E_sampled: PFATE 28/28 (p 0.0000; median 0.0990) PRESENT; PYOKED 28/28 (p 0.0000; median 0.0787) PRESENT; PNOFATE 10/14 (p 0.1796; median 0.0005) NOT_DETECTED
- route M2_E_alt: PFATE 28/28 (p 0.0000; median 0.0995) PRESENT; PYOKED 28/28 (p 0.0000; median 0.0861) PRESENT; PNOFATE 19/28 (p 0.0872; median 0.0000) NOT_DETECTED
- route M2_own_p: PFATE 24/28 (p 0.0002; median 0.0019) PRESENT; PYOKED 24/28 (p 0.0002; median 0.0017) PRESENT; PNOFATE 6/28 (p 0.0037; median -0.0000) REVERSED
- route M2_own_sampled: PFATE 25/27 (p 0.0000; median 0.0047) PRESENT; PYOKED 25/27 (p 0.0000; median 0.0035) PRESENT; PNOFATE 8/16 (p 1.0000; median -0.0000) NOT_DETECTED
- route M2_lda_p: PFATE 15/28 (p 0.8506; median 0.0001) NOT_DETECTED; PYOKED 18/28 (p 0.1849; median 0.0001) NOT_DETECTED; PNOFATE 18/28 (p 0.1849; median 0.0000) NOT_DETECTED
- route M2_joint_p: PFATE 24/28 (p 0.0002; median 0.0007) PRESENT; PYOKED 21/28 (p 0.0125; median 0.0008) PRESENT; PNOFATE 6/28 (p 0.0037; median -0.0000) REVERSED
- route M2_E_early: PFATE 28/28 (p 0.0000; median 0.1061) PRESENT; PYOKED 28/28 (p 0.0000; median 0.0621) PRESENT; PNOFATE 12/28 (p 0.5716; median -0.0000) NOT_DETECTED
- route M2_E_late: PFATE 27/28 (p 0.0000; median 0.0893) PRESENT; PYOKED 28/28 (p 0.0000; median 0.0851) PRESENT; PNOFATE 19/28 (p 0.0872; median 0.0000) NOT_DETECTED
- route trace_auc: PFATE 28/28 (p 0.0000; median 0.4533) ABOVE_CHANCE; PYOKED 28/28 (p 0.0000; median 0.4552) ABOVE_CHANCE; PNOFATE 28/28 (p 0.0000; median 0.2816) ABOVE_CHANCE
- route trace_pair_auc: PFATE 28/28 (p 0.0000; median 0.3827) ABOVE_CHANCE; PYOKED 28/28 (p 0.0000; median 0.3985) ABOVE_CHANCE; PNOFATE 28/28 (p 0.0000; median 0.1370) ABOVE_CHANCE
