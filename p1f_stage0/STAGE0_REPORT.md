# Track C P1f stage 0: the second-order test on P1e's nets (declared; not the confirmation)

**Stage 0: SECOND_ORDER_SIGNAL (thin overlap).** P1e's saved weights at 3600, seeds 2800-2827 (28). P1e's run was INVALID on exposure.

Matched confidence: 10 quantile bins, at least 5 conflict and 5 same trials per kept bin; split probe on 0.667 of the trials at delay step 1 and 8; no drain; evaluation tag 140.

| arm | M2_own | M2_own_early | M2_own_late | M2_lda | M2_lda_early | M2_lda_late | coverage_own | coverage_lda | raw_own | conf_conflict_own | conf_same_own | conf_conflict_lda | conf_same_lda |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PFATE | 0.116 | 0.188 | 0.035 | 0.239 | 0.337 | 0.085 | 0.207 | 0.213 | 0.554 | 2.693 | 10.411 | 56.158 | 136.361 |
| PYOKED | 0.269 | 0.486 | 0.057 | 0.313 | 0.491 | 0.133 | 0.197 | 0.196 | 0.631 | 2.391 | 10.706 | 67.751 | 147.572 |
| PNOFATE | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.603 | 0.601 | 0.002 | 6.753 | 9.369 | 65.640 | 87.355 |

- M2_own_PFATE_vs_PNOFATE: 28/28 (p 0.0000; 0.116 against 0.000) DERIVED_AHEAD
- M2_own_PYOKED_vs_PNOFATE: 28/28 (p 0.0000; 0.269 against 0.000) DERIVED_AHEAD
- M2_lda_PFATE_vs_PNOFATE: 28/28 (p 0.0000; 0.239 against 0.000) DERIVED_AHEAD
- M2_lda_PYOKED_vs_PNOFATE: 28/28 (p 0.0000; 0.313 against 0.000) DERIVED_AHEAD
- M2_own_PFATE_vs_PYOKED: 2/28 (p 0.0000; 0.116 against 0.269) YOKED_AHEAD
- route M2_own: PFATE 27/28 (p 0.0000; median 0.116) PRESENT; PYOKED 28/28 (p 0.0000; median 0.269) PRESENT; PNOFATE 10/20 (p 1.0000; median 0.000) NOT_DETECTED
- route M2_own_early: PFATE 28/28 (p 0.0000; median 0.188) PRESENT; PYOKED 28/28 (p 0.0000; median 0.486) PRESENT; PNOFATE 8/16 (p 1.0000; median 0.000) NOT_DETECTED
- route M2_own_late: PFATE 22/28 (p 0.0037; median 0.035) PRESENT; PYOKED 25/28 (p 0.0000; median 0.057) PRESENT; PNOFATE 5/13 (p 0.5811; median -0.000) UNDETERMINED
- route M2_lda: PFATE 28/28 (p 0.0000; median 0.239) PRESENT; PYOKED 28/28 (p 0.0000; median 0.313) PRESENT; PNOFATE 15/21 (p 0.0784; median 0.000) NOT_DETECTED
