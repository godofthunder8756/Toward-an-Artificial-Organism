# K-EXACT precision v2 — short note

Analytic rerun only. No neural training. The frozen `quantized_exact_forecasts` and `acquisition_results_v1/reference_arms.json` are unchanged. The curve is `reference_arms_kexact_v2.json`, from `quantized_exact_forecasts_v2`.

The ordering is the attached fix, adopted as a new function: transition the previous repaired chart, observe, then quantize the post-observation chart against the post-observation TRAIN ranges.

- Smallest passing precision on TRAIN: **4**. TRAIN E_total = 0.0011912031095684407, E_XOR = 0.0005896462496796877.
- Smallest passing precision on TEST: **4**. TEST E_total = 0.0016523181037595013, E_XOR = 0.000882518843751816.
- Frozen selection rule: b_sel = 4, confirmation **CONFIRMED**. Nominal charged state 12 bits. Stage-wise charge 4, 8, 12, 12, 12, 12, 12, 12.
- At 24 bits, TRAIN E_total = 9.430249536508092e-16 and E_XOR = 4.362159278360539e-16. Maximum TRAIN |Δq| = 4.6331485203943146e-08.
- At 24 bits, TEST E_total = 0.0006702864095000391 and E_XOR = 0.0004381189940407303. That plateau is TEST charts outside the TRAIN ranges.

This number is a descriptive reference for the exact chart. It does not enter E1, E2, E3, or the study verdict.
