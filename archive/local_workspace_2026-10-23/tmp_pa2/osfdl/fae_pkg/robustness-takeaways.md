# What the next tests established

The 128-trial development round completed in approximately 12 CPU minutes for the trials themselves, excluding validation and analysis. All 2,936 recorded steps passed the parameter-aware data audit. No paid compute service or model API was used.

## Findings

On the complete 12-layout bank with development seeds 10 and 11, uniform control survived 2/24 trials, coupled sensing/model precision survived 7/24, and preference weighting survived 10/24. Mean regulation loss was 0.7223, 0.5992, and 0.5358 respectively; lower is better. Preference's earlier descriptive advantage therefore persisted in this broader default-setting comparison.

That ordering did not hold everywhere. On the four-layout sensitivity subset with seeds 12 and 13, the original coupled setting had mean loss 0.5450, compared with 0.5667 for the original preference setting. Both survived 2/8 trials. This comparison changed layouts and seeds relative to the broad-bank test, so it cannot attribute the ranking change to either one alone.

Across the scanned strengths, mean coupled loss ranged from 0.5629 to 0.5039, and preference loss from 0.5777 to 0.5572. These ranges are across settings, not confidence intervals. The strongest coupled setting survived 3/8 sensitivity trials; every tested preference strength survived 2/8. None of the three methods survived a far-tier trial in the broad-bank check.

The defensible conclusion is that performance depends on scenarios and settings. There is no established universally superior mechanism. These results are exploratory, based on two seed clusters per phase and a small fixed environment bank.

## Recommended main-study choices to finalize

1. Retain continuous regulation loss as a candidate primary outcome, with survival and time to failure reported alongside it. It was already defined before the earlier pilots and remains informative when survival is near zero or one. Justify the post-failure penalty and plan a sensitivity check for that scoring choice.
2. Preserve the original coupled precision of 0.90 and preference weight of 2.0 as primary candidate settings rather than declaring a grid winner validated. Report the sensitivity grid. The parameters are not equivalent in units or effect strength.
3. Keep layout-level results and distance tiers explicit. Do not silently remove far or otherwise unfavorable layouts. If the primary population is narrowed for task competence, state that rule and retain the excluded cases as a separate boundary analysis.
4. Finalize the misleading-signal intervention and its control, including how clipping affects magnitude and mean. These clean-signal tests have not confirmed robustness to bias.
5. Define a practically meaningful effect and the required precision, estimate an affordable fixed sample size, and reserve a new seed set. Preregister the frozen comparison before collecting those confirmatory data.

The broader research question remains useful: when does better sensing or stronger assumed confidence help regulation, and when is changing behavioral priorities sufficient or better? None of these outcomes tests subjective experience.

The full tables, trajectories, configuration, source snapshots, validation records, and charts are in `robustness-002/`. `robustness-plan.md` records the plan and the corrected pre-trial numerical mismatch. No public registration or submission has occurred.
