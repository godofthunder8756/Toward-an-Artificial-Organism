# ERRATUM v1 — E3-v2 ratio rule

**Status:** Additive rule. The frozen E3 rule and its verdict stay exactly as recorded. They remain the historical diagnostic.
**Applies to:** PR #5, results commit `b25a30ab014355aaec123258031b597c5a78ba55`. No file under `acquisition_results_v1/` is edited. `twostream_acquisition_metrics._rho` is not edited.
**Source:** consult #12, as specified for this erratum. The earlier note `ERRATUM_v1_e3_complement_denominator.md` records the frozen behavior. This file does not replace that note and does not revise its conclusion.

## The frozen rule, kept

`_rho` returns no value when the denominator is at or below 10⁻¹². A missing value cannot pass. That is the protocol sentence at `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md` L275 and L401–L402, and it is what the recorded E3 label used.

Recorded labels, unchanged:

- E3: **NOT LOCALIZED BY THIS INTERVENTION**
- K-FR E3: **UNRESOLVED**
- Study: **ADMIT**

## E3-v2

E3-v2 is a separate versioned rule. It is not substituted into the frozen study. For any ratio N/D:

- If D ≤ 10⁻¹² and N > 10⁻¹², the value is +∞.
- If D ≤ 10⁻¹² and N ≤ 10⁻¹², the value is UNDEFINED. UNDEFINED never counts as a pass.
- Otherwise the value is N/D.

The helper is `e3_v2_ratio` in `twostream_acquisition_e3_v2.py`. `e3_v2_meets` applies a threshold. UNDEFINED fails both an at-least gate and an at-most gate. +∞ passes an at-least gate and fails an at-most gate. The same function applies to every ratio statistic: partial, complement, and wrong-donor, vector and XOR, and the descriptive donor-tracking and random-probe ratios.

A perfect complement, whose forecast equals q*(a), has N > 0 and D = 0. E3-v2 returns +∞, which meets the complement gate ρ ≥ ¾. The frozen rule still returns no value and still fails that seed. E3-v2 does not rewrite that seed's recorded flag.

## What was not done

No arm was retrained. No forecast was recomputed. The saved run JSON was not edited. Whether the recorded runs would have carried a different label under E3-v2 is answered only by the separate descriptive audit.
