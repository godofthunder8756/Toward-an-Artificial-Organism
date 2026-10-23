# When Internal Signals Mislead: Sensing and Preference in Artificial Homeostasis

**Author:** Jonathan D Faeth

**Affiliation:** Independent Researcher

**Protocol version:** 1.0, 29 September 2026

**Status:** Prepared for public preregistration; registration record pending. No confirmatory data have been collected. Development results informed this design and are disclosed below.

## Question and scope

When internal readings become misleading, does coupled improvement of sensing and assumed likelihood precision differ from preference reweighting in its effect on artificial homeostasis?

This is an empirical extension using the AffectWorld reproducibility snapshot at revision `2657a982c5ae59a0f0fa9cdf941f82a71eba3cd9`. Credit the original authors and their previously identified open comparison. This is not a claim to invent artificial homeostasis or establish subjective experience. The virtual body uses physiological counters, not actual hardware temperatures or memory usage.

## Design

Use all 12 original layouts: six easy, three medium, three far. Report individual layouts and tiers. No removal of hard or unfavorable layouts based on these results.

Compare three agents: uniform reference; coupled selective sensing and likelihood precision; preference-only reweighting. Use the same external-need selector, action space, body, and planning routine. Keep the original candidate strengths: attended correctness probability 0.90 with total correctness-probability budget 2.6; selected preference weight 2.0 with other weights 2/3. These are different units, not an exact match of behavioral strength. The uniform reference uses the same external-selector class with selective effects disabled.

Use known resource maps, two-step planning, no online resource-model learning, and fresh initial beliefs on every episode. Each episode lasts at most 40 steps. Physical fatigue accumulation remains disabled, while the fourth sensor/modality remains present as in the previous pilots. No oracle body-state access is enabled for the agent. Evaluators may read true body states solely for measurement.

Three sensor conditions: clean, positive bias, and symmetric perturbation. This gives 12 layouts × 3 agents × 3 conditions = 108 episodes per seed.

## Corrected intervention

At decision times 5 through 14, consider the raw categorical thirst reading, on a scale from 0 to 5.

- If the reading is 1, 2, 3, or 4: positive bias adds one; symmetric perturbation adds +1 or −1 with equal probability; clean adds zero.
- If the reading is 0 or 5: all conditions leave it unchanged.
- Outside that interval: all conditions leave the reading unchanged.

There is no clipping. Conditional on the same eligible raw reading, bias and symmetric perturbation have exactly the same absolute increment, and symmetric perturbation has expected increment zero. This claim concerns the added increment, not the total error relative to true physiology. It also concerns expectation, not exact zero mean in a finite sample.

Eligibility depends on the raw reading. In closed loops, different sensing allocations and actions can produce different eligibility rates. Record raw readings, eligibility, applied increments, and realized exposure. Do not claim equal intervention dose across agents; do not adjust the primary contrast for these post-treatment variables. Report exposure descriptively. The primary estimand is the total response of the complete agent to this intervention rule.

Underlying physiology is not changed directly by the intervention. Actions can subsequently change it. Use paired, pre-generated sensor-noise and perturbation draws, including draws for sham/boundary cases, so intervention conditions do not change random-stream consumption. Reset learned state, beliefs, physiological state, and environment randomness for each episode.

## Primary outcome and estimand

Retain the previously defined regulation-loss score: for each executed step, average `1 - nutrient/15` and `1 - hydration/15` after the action. Average over the 40-step horizon, assigning loss 1 to remaining steps after terminal failure. Lower is better. This is an engineered score, not a validated measure of feeling.

For each seed and layout, compute bias-minus-clean loss separately for coupled and preference agents. Subtract the preference change from the coupled change. Average equally across the 12 layouts within seed. The primary estimate is the mean of those seed-level contrasts; positive values favor preference on this robustness contrast, and negative values favor coupled.

The primary test is two-sided; the development results do not justify a one-sided superiority claim. Report the mean, seed-level values, a two-sided 95% Student-t confidence interval, and its assumptions. Seeds are the independent replication units. Layouts belong to a fixed bank; the inferential target concerns simulation randomness over that bank, not all possible environments. Do not treat individual steps as independent observations.

## Secondary reporting

Report survival at 40 steps, restricted time to failure, mean resource deficits during observed steps, body-state estimation error, and intervention exposure. Report clean-condition comparisons with uniform, noise-minus-clean changes, and bias-minus-noise changes descriptively with intervals, without declaring additional confirmatory discoveries from unadjusted multiple tests.

As a prespecified scoring sensitivity analysis, recompute regulation loss by holding the terminal observed deficit constant for remaining steps instead of assigning loss 1. This has a different interpretation and can under-penalize death; keep the original score primary and report both. Report results by layout and tier, including far-layout failures. Mechanistic claims about identical evidence should refer separately to the fixed-input diagnostic, not be inferred solely from divergent closed-loop histories.

## Sample size and cost

Use **64 seeds, numbered 10000 through 10063**, not previously used in development: **6,912 episodes**. No significance-based early stopping, seed replacement, or sample extension. These seed numbers are a documented reservation, not a technical access restriction.

The four-seed earlier bias pilot had estimated SD 0.0965 for its paired contrast. At 64 seeds, a t-based planning calculation gives a nominal interval halfwidth about 0.024 at that SD, 0.048 at twice that SD, and 0.075 at SD 0.30. The earlier pilot used only two layouts and a different perturbation, so these are scenarios, not a reliable guarantee of precision or power. A provisional practical difference is 0.05 on the loss scale; this is a study-design convention, not a biological threshold. Do not interpret an interval crossing zero as evidence of equivalence.

Measured local sweep timings project roughly 11–13 CPU hours for the episodes; allow approximately 12–16 hours including overhead and machine-load variation. No paid cloud or model API is required. Electricity and use of an existing computer remain real costs. A full confirmatory run has not been launched.

## Integrity, failures, and stopping rules

Freeze code, dependencies, configuration, and their checksums before registration and execution. Store a unique identity for each seed/layout/agent/condition combination. Checkpoint completed episodes so a wall-clock interruption can resume the predetermined remaining cases without replacing data.

Terminal physiological failures are valid outcomes. Software exceptions or nonfinite values are not physiological failures: retain logs and mark the affected record as a software failure. Infrastructure retries must use the identical seed and configuration; record every attempt. If a code defect requires changing scientific behavior, stop, document the issue, amend the plan publicly, and do not silently mix code versions or call a rerun independent confirmation. Do not report a complete primary analysis if required cells remain missing; report the reason.

## Development disclosure and registration status

Disclose the two 120-episode pilots, 14 competence-check episodes, 128 difficulty/sensitivity episodes, the six-trajectory fixed-input diagnostic, software validation runs, and the corrected-control integration checks. Their settings and outcomes informed this protocol. The original pilot had 0/120 survivors; the adjusted pilot had 66/120. The 128-episode follow-up showed condition-dependent rankings, not a universal winner. Control integration and checkpoint/resume preflights used development seeds 200 and 301; no reserved confirmatory seeds were used. Preserve the pre-trial implementation failures and fixes. None of those data enter the confirmatory estimate.

Before the main run, publish this protocol and its frozen materials, verify the registration identifier and timestamp, and record them with the run. A local file or OSF draft does not constitute completed public preregistration. Later release the manuscript, data, code, configuration, deviations, and negative results together. Subjective consciousness remains outside the measured outcomes.

## Statistical reporting details

For secondary contrasts, first form the paired contrast within each seed and layout, average equally over the fixed layouts, and report its across-seed mean and two-sided 95% Student-t interval. Clean comparisons are each selective arm minus uniform; noise-minus-clean and bias-minus-noise are within each arm. These comparisons concern regulation loss; the other secondary measures are descriptive summaries by arm, condition, layout and tier. No secondary p-value is a confirmatory test. The primary interval uses 63 degrees of freedom. Its coverage relies on independent seed-level replicates and an adequate approximation for their mean. The primary hypothesis is a zero mean paired difference-in-differences versus a nonzero mean. No equivalence claim is planned.

The frozen analyzer implements the primary analysis, scoring sensitivity, completeness audit, and basic summaries. Additional secondary reporting may be implemented after registration using the definitions above, with any deviation documented. Such additions do not change the frozen primary estimator.

## Attribution, assistance, and boundaries

This is a replication/extension of an existing simulation platform. It does not claim the first artificial homeostatic agent, novel evidence of consciousness, or guaranteed priority over all unpublished work. The main comparison addresses a question identified in the upstream work. AI assistance was used for literature searching, study planning, programming, verification, analysis of development runs, and drafting. The named human author is responsible for reviewing and approving the research and its claims. No human participants, animals, or biological substrates are involved in this simulation study. Future fungal or slime-mold experiments are outside this registration.

## Primary reference and software

Grimbly, S. J., Kuske, N., Boonstra, E. A., Bassett, B. A., van Hoof, C., Hodson, R., Rosman, B., Smith, R., Solms, M., & Shock, J. P. (2026). *Interoceptive Attention as Dynamic Homeostatic Prioritization in a Foraging Agent*. arXiv:2608.04232v1. https://doi.org/10.48550/arXiv.2608.04232

Upstream software: https://github.com/sgrimbly/attention-aif-sab2026-snapshot at commit `2657a982c5ae59a0f0fa9cdf941f82a71eba3cd9`. Preserve the upstream MIT license when redistributing its code. Its paper is not included in this package.
