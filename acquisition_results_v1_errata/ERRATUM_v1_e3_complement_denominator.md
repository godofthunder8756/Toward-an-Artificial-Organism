# ERRATUM v1 — E3 complement denominator

**Status:** Record only. No E3 label, seed JSON, verdict, or frozen function is changed.
**Applies to:** the frozen `_rho` in `twostream_acquisition_metrics.py` at results commit `b25a30a` (function starts at L218; the undefined return is L225–L226). The LOCALIZED conjunction is L383–L397. The prespecified rule is `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md` L275 and L401–L402.

## The defect

`_rho` returns no value when the denominator is at or below `RATIO_TIE` (10⁻¹²). LOCALIZED(seed) requires the partial, complement, and wrong-donor ratios, both vector and XOR, to be defined and to meet their thresholds. An undefined complement ratio therefore counts as not localized.

A perfect positive control hits that branch. If the complement forecast equals the recipient oracle q*(a) on the eligible trials, both complement denominators are zero. A defined ratio would be infinite, which would satisfy the complement gate ρ ≥ ¾. The frozen code returns no value, so that seed cannot be labeled localized. The same control's partial transplant can still have ratio 0, because its denominator is ‖q*(b) − q*(a)‖².

This is the protocol sentence, not an extra gate. L275 and L401–L402 say a denominator at or below 10⁻¹² is undefined and cannot pass. The code follows that sentence. The defect is the sentence's effect on an ideal complement: the rule that rejects a numerical tie also rejects a complement that does not move the forecast at all.

## What it did not do

It did not decide the recorded GRU-8 verdict. All 10 CAND complement ratios are finite. The vector ratios run from 0.1274675229968734 to 0.6408903839359313, all below ¾, so those seeds fail the complement gate on the value of the ratio. No file in `acquisition_results_v1/runs/` has a null ratio. E3 stays **NOT LOCALIZED BY THIS INTERVENTION**. K-FR E3 stays **UNRESOLVED** because coverage fails on 9 of 10 seeds, which is a different rule.

No verdict is revised.
