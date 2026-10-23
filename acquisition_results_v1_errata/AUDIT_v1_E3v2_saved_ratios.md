# DESCRIPTIVE AUDIT, NOT A VERDICT CHANGE

**Label:** DESCRIPTIVE AUDIT, NOT A VERDICT CHANGE.
**Rule:** E3-v2, in `ERRATUM_v1_E3v2_ratio_rule.md` and `twostream_acquisition_e3_v2.py`.
**Input:** the 120 saved files in `acquisition_results_v1/runs/`. Saved values only. No retraining and no recomputation of forecasts, numerators, or denominators.
**Frozen verdicts kept:** E3 **NOT LOCALIZED BY THIS INTERVENTION**. K-FR E3 **UNRESOLVED**. Study **ADMIT**.

## Outcome

**No label would differ.**

E3-v2 applied to the saved statistics produces the same per-block localized flags and the same two study labels as the frozen rule.

| quantity | saved frozen rule | E3-v2 on saved values |
| --- | --- | --- |
| GRU-8 CAND E3 | NOT LOCALIZED BY THIS INTERVENTION | NOT LOCALIZED BY THIS INTERVENTION |
| GRU-8 K-FR E3 | UNRESOLVED | UNRESOLVED |
| localized flags that differ | — | 0 of 300 |
| saved ratio components that are null | 0 of 2400 | — |

## Why the saved numbers already are the E3-v2 numbers

The frozen `_rho` stores a float only when D > 10⁻¹², and it stores null when D ≤ 10⁻¹². E3-v2 uses that same cutoff. A stored float is therefore already N/D, which is the ordinary branch of E3-v2. A stored null would not say whether N was above 10⁻¹² (+∞) or not (UNDEFINED). None of the 2400 saved ratio components is null, so that branch is not exercised and nothing is left unauditable.

The 2400 components are the partial, complement, and wrong-donor vector and XOR ratios, the donor-tracking ratios, and the random-probe ratios, on every run that stored them.

## Flags

300 saved `localized` flags were compared (120 primary blocks, 90 all-16 blocks, 90 PCA blocks). 290 have a saved ratio block. Re-applying the six gates to those saved floats leaves every flag unchanged. The other 10 are the K-TAB runs. Their intervention block is inapplicable because the state is a history index, and they have no ratio block. Those flags stay as recorded. They are not denominator events.

GRU-8 CAND primary ratios, all finite, seeds 0–9:

- partial vector 1.6488812765979646–14.210014822978598, all above ½
- complement vector 0.1274675229968734–0.6408903839359313, all below ¾
- wrong-donor vector 2.173220947960307–11.363078611806797, all above ½

Those seeds fail the partial and wrong-donor gates on the stored values. They would stay not localized even if a complement denominator had been turned into +∞. K-FR E3 stays UNRESOLVED because coverage fails on 9 of 10 seeds, which this ratio rule does not touch.

This audit is not a new verdict.
