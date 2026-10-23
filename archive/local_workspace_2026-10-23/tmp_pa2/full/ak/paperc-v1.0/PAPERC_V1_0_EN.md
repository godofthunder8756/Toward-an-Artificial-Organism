# Measure the Instrument First

## Preregistered, Prediction-Sealed, One-Shot Calibration of Four Endpoints in a 4B QLoRA Series

**Author:** Akiyama Satoshi  
**Affiliation:** Independent researcher  
**Status:** Public release v1.0 (DOI: 10.5281/zenodo.21983630)  
**Publication:** This version was released after Fable's independent review (PASS_FOR_OPERATOR_CONSIDERATION_OF_PUBLICATION_FREEZE), fixation of the release candidate, and an explicit publication decision by the operator. CC-BY 4.0.  

## Abstract

When a model series shows little or no apparent difference, two explanations must be separated: the target may not differ, or the instrument may be unable to resolve the difference. We calibrated four endpoints on a single Qwen3-4B–based QLoRA series comprising eight adapter checkpoints (d16–d192) and the base model (d0), for nine evaluation points in total. The material contained 29 items nested within 16 slugs; the slug, not the item, was the inference unit. After known-answer fixtures, proxy-data compatibility testing, instrument freezing, and sealed predictions from two predictors, the four endpoints were applied once to 261 item-by-evaluation-point rows.

E3, the combined stop-token log mass immediately after the completion, separated d0 from d192 with a median slug contrast of +16.625 nat, a split-half null scale of 1.793 nat, and a detection ratio (DR) of 9.27. However, the d192 slug median was −0.087 nat, above the preregistered provisional ceiling of −1.0 nat, placing it outside the instrument's declared operating range. E2, TRUE preference, yielded DR 0.64 and was not separable at this scale. E4, forced choice, selected position A in both presentation orders for all 261/261 rows. Order averaging therefore produced a constant item score of 0.5 and a null scale of zero, making the endpoint undefined. E1, normalized negative log-likelihood (NLL), separated strongly with DR 7.10, but the observation matched no row in the preregistered decision table and exposed an uncovered branch condition.

These findings do not establish the presence or absence of a distillation effect. They show that, within one measurement system, an endpoint that separates but saturates, an endpoint that lacks resolution, an endpoint destroyed by position bias, and an endpoint blocked by an incomplete decision rule can coexist. The instrument's operating range and failure modes therefore need to be measured before model effects are interpreted.

**Keywords:** AI distillation; endpoint validation; measurement; preregistration; prediction sealing; QLoRA; stopping behavior

## 1. Introduction

An observed difference in a trained or distilled model cannot automatically be interpreted as a learning effect. If the difference is small, the target may be unchanged, or the instrument may lack sufficient resolution. If the difference is large, it may reflect floor or ceiling behavior, presentation-position bias, aggregation choices, or a defect in the decision rule rather than the intended construct. Ribeiro et al. (2020) similarly argued that a single aggregate score can hide behavior-specific failures and proposed behavioral testing that separates capabilities from test types.

In the preceding Paper B, eight prompts (a different material set from the 16 slugs used here) showed complete separation in termination rate across interface conditions, 0/8 versus 8/8, while the binary endpoint was pinned to its floor and ceiling across prompt-loss-weight levels and therefore could not adjudicate differences between those levels. That result motivated a stricter sequence: before an endpoint is used to support a model claim, it should be tested for its ability to separate a known positive, remain quiet under an admissible null, and stay within a declared operating range.

The question in this study is narrow: did an intervention fail to change the target, or did the instrument fail to measure it? We built a calibration procedure called INSTRUMENT-0 and applied four endpoints once to the same 4B model series. For each endpoint, we measured separation, null scale, floor and ceiling behavior, undefined states, and consistency with a preregistered decision table. Before the primary run, two predictors independently assigned probabilities to the possible decision rows, and those predictions were sealed while the primary raw file did not yet exist.

This paper does not attempt to establish improved model capability or a general distillation mechanism. Its contributions are methodological. First, it distinguishes what each endpoint can and cannot measure within the frozen series. Second, it preserves position bias and an uncovered decision-table branch as instrument failures instead of repairing them after viewing the result. Third, it discloses procedural incidents, post-incident governance changes, failed predictions, and role non-independence so that the evidential strength can be evaluated from both the results and the process that produced them.

## 2. Methods

### 2.1 Study status and preregistration

The primary measurement followed `PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md`. No new training or free generation was performed; only teacher-forced evaluation and aggregation of frozen raw values were used. The primary contrast for each endpoint was restricted to d0 versus d192. Adjacent-dose comparisons were descriptive and carried no confirmatory claim. No p-values were calculated. All decisions were comparisons against scales and thresholds fixed before the primary run.

The preregistration SHA-256 was `5e19341f30a8b92bc97e177d7b3a25ff01d6f6a13e0c7bc780e4e881278fb0bf`. The primary raw file was `INSTRUMENT0_STAGE5_RAW_V1.jsonl`, SHA-256 `2ff33a4d62c246361c1864b2a6c61dd6c28260a3e4cbb808c0f5be519048cfc6`. It contained 261 rows, and every row carried an instrument hash that matched the frozen runner identity.

### 2.2 Model series, material, and inference unit

The evaluated series was based on Qwen3-4B and trained through QLoRA. QLoRA backpropagates through a frozen quantized base model into low-rank adapter weights, reducing the memory required for fine-tuning (Dettmers et al., 2023). The evaluated points were the base model d0 and eight adapter checkpoints: d16, d32, d48, d64, d96, d128, d160, and d192.

The primary cohort was `ALWAYS_UNSEEN_COHORT`, containing 29 items grouped into 16 slugs. Items were treated as within-slug repetitions, not independent observations. The 16 slugs were therefore the primary inference units and received equal weight.

The source material had been inspected before the rule set was fixed. What remained unobserved was the nine-evaluation-point by four-endpoint outcome matrix. Because the study used one model series, one seed, and one cohort, no extrapolation to other models, seeds, or datasets is made.

### 2.3 Endpoints

Four endpoints were defined.

1. **E1: normalized NLL.** The item value was `TRUE loss_sum / n_tokens`. The primary contrast was the within-slug aggregate at d192 minus the within-slug aggregate at d0 (Section 2.5). The expected direction was a decrease in NLL.
2. **E2: TRUE preference.** At d0, the item value was `SWAP mean NLL − TRUE mean NLL`. A positive value favored the TRUE completion.
3. **E3: stop mass.** The item value was the combined log mass of two stop tokens immediately after the TRUE completion. The primary contrast was the within-slug aggregate at d192 minus the within-slug aggregate at d0 (Section 2.5). Right padding was not counted as a stop.
4. **E4: forced choice.** A single fixed template presented alternatives A and B in two reversed orders. In order 1, A occupied the correct position; in order 2, B occupied the correct position. The two correctness indicators were averaged to obtain the item score. The template was not changed during measurement.

For E1–E3, items were aggregated within each slug by the ordinary median. For even sample sizes, this was the arithmetic mean of the two central values. E4 used a within-slug mean because the item score was bounded. Rounded display values were never used in decisions.

### 2.4 Exclusion rules

Non-finite values were excluded at the item level. For E1, items with `n_tokens < 8` were also excluded. The endpoint-specific denominator was fixed at 29 items × 9 evaluation points = 261. An exclusion rate greater than 10%, or even one slug with all items excluded from the primary contrast, would trigger `INSTRUMENT_STOP`.

### 2.5 Separation and null scale

The primary separation statistic was `SEP_max`. For E1, E3, and E4, it was the median of the per-slug d192-minus-d0 contrasts. For E2, it was the median per-slug TRUE preference at d0. A per-slug contrast was defined as the within-slug aggregate (median for E1–E3, mean for E4) at d192 minus the within-slug aggregate at d0; item-level differences were not formed. Aggregating item-level differences within slugs instead would change the value for slugs with more than one item and would not reproduce the tables in this paper.

The split-half null enumerated all 6,435 non-ordered 8/8 partitions of the 16 slugs. To remove duplicate complements, the lexicographically first slug was fixed to one side. For each partition, the absolute difference between the two half-sample medians was calculated. The 95% point was the 6,114th order statistic after ascending sort. No interpolation, random sampling, or random seed was used.

A permutation null was counted as tested only if the exchange level, exchangeability argument, and known-answer demonstrations of both detection and silence had all been specified. Only E2 met these requirements through within-slug exchange of TRUE and SWAP labels. E1, E3, and E4 were marked `PERMUTATION_NULL_STRUCTURALLY_NOT_TESTED`; structural non-testing was not counted as successful null silence.

`NULL_scale` was the larger of the absolute permutation-null median and the split-half 95% point. The detection ratio was `DR = |SEP_max| / NULL_scale`, and the operational minimum detectable effect was `MDE = 2 × NULL_scale`. If `NULL_scale` was zero or non-finite, the endpoint became `UNDEFINED_ENDPOINT`. No epsilon, alternate quantile, or alternate scale could be introduced after observing the result.

### 2.6 Floor, ceiling, and decision table

For continuous E3 values, the preregistered floor was −20.0 nat and the ceiling was −1.0 nat. The ceiling came from an integer-rounding rule applied to the lower edge, −0.630, of a previously observed high-mass band. The floor lacked a prior value at the same measurement position and was explicitly provisional. A two-sided guard required the observed d0 value to lie strictly between the floor and ceiling.

The decision table in preregistration Section 6 was evaluated from top to bottom, and the first matching row determined the endpoint state. The table included abnormal-run stop, null failure, wrong-direction separation, floor or ceiling failure, undefined endpoint, validated states with or without a practical basis, underpowered-for-practice, weak separation, and not separable. The table could not be repaired and reapplied to the same raw data after the result was known.

### 2.7 Instrument-development sequence

Five stages preceded or contained the primary measurement.

- **Stage 1:** known-answer synthetic fixtures, ending at 39/39 PASS (one expected value was corrected before any target data was touched).
- **Stage 2:** proxy-data compatibility tests, with the corrected version ending at 30/30 PASS.
- **Stage 3:** freezing of 43 instrument, material, configuration, fixture, and runner artifacts.
- **Stage 4:** independent probabilistic predictions from Fable and Opus, sealed after machine confirmation that the primary raw file did not exist.
- **Stage 5:** a single primary application to 9 evaluation points × 29 items = 261 rows.

If a defect was found, the prescribed path was to stop and preserve it. The measured raw data could not be reclassified under a repaired rule in the same version.

![Figure 1. Five-stage INSTRUMENT-0 sequence](figures/figure1_instrument_sequence.png)

**Figure 1. INSTRUMENT-0 study sequence.** Known-answer fixtures and proxy compatibility checks preceded the 43-artifact freeze. Independent predictions were sealed while the primary raw file was absent, followed by one application to the 261-row matrix. The preservation rule prohibited repairing a discovered defect and reusing the same raw data.

### 2.8 Independent recomputation

Codex independently recomputed the principal values from the 261 raw rows without using stored result values as calculation inputs. The procedure rebuilt item values, within-slug aggregation, the equal-weight median across 16 slugs, all 6,435 non-ordered 8/8 partitions, and the 6,114th order statistic. E4 choices were recalculated from the per-order log probabilities on every row.

The recomputation code was `paperc_independent_recompute_v1.mjs`, and the receipt was `PAPERC_INDEPENDENT_RECOMPUTE_CODEX_V1.json`. Every listed principal value matched the frozen result. Fable additionally re-derived the same quantities from the same raw file with an independent implementation that imported neither the aggregator, the runner, nor the core module; SEP, NULL_scale, the split-half 95% point, DR, MDE, and the decision rows all matched (`FABLE_PAPERC_INDEPENDENT_RECOMPUTE_V1.json`). These recomputations verify numerical derivation only; they do not approve the claim ceiling, disclosure sufficiency, release candidate, or publication.

## 3. Results

### 3.1 Data integrity and exclusions

The raw dataset contained 261 rows, 16 slugs, and nine evaluation points. All 261 instrument stamps were valid. No item was excluded for any of the four endpoints, and no slug was fully excluded. The exclusion-based stop rules therefore did not fire.

| Endpoint | SEP_max | NULL_scale | DR | MDE | Preregistered outcome |
|---|---:|---:|---:|---:|---|
| E1 normalized NLL | −0.542996 | 0.076483 | 7.10 | 0.152966 | Out-of-table `INSTRUMENT_STOP` |
| E2 TRUE preference | +0.169169 | 0.263120 | 0.64 | 0.526240 | Row 8 `NOT_SEPARABLE` |
| E3 stop mass | +16.625254 | 1.792573 | 9.27 | 3.585146 | Row 3 `FAILED_FLOOR_CEILING` |
| E4 forced choice | 0 | 0 | Undefined | Undefined | Row 3.5 `UNDEFINED_ENDPOINT` |

![Figure 2. Dose trajectories of four endpoints](figures/figure2_endpoint_dose_trajectories.png)

**Figure 2. Dose trajectories of four endpoints.** Small gray points are the 16 equal-weight slug values; colored lines are across-slug medians. The primary contrast was d0 versus d192. Intermediate evaluation points are descriptive and do not establish a causal dose response. Dashed lines in E3 mark the provisional floor and ceiling.

| Endpoint | What the result supports | What it does **not** support |
|---|---|---|
| E1 | The preregistered decision table did not cover the observed state | Endpoint validity or model improvement |
| E2 | The observed contrast was smaller than the instrument null scale | Absence of TRUE preference |
| E3 | Strong separation and crossing of the provisional high-dose ceiling | Completed stopping ability or a general mechanism |
| E4 | Complete position-A preference in this frozen template | General invalidity of forced-choice evaluation or absence of content preference |

### 3.2 E3 separated strongly but exceeded the preregistered ceiling

The median per-slug d192-minus-d0 contrast for E3 was +16.625254 nat. The split-half null 95% point was 1.792573 nat, producing DR 9.2745. The endpoint therefore strongly separated the known positive.

The across-slug median E3 value was −17.141216 nat at d0 and −0.086550 nat at d192. The d0 value passed the two-sided guard, but the d192 value exceeded the preregistered ceiling of −1.0 nat. Because the floor-and-ceiling row preceded validation rows in the decision table, the final outcome was Row 3, `FAILED_FLOOR_CEILING`.

This supports two limited statements: E3 detected change from lower to higher dose in this series, and d192 lay outside the operating range declared by the preregistered rule. It does not establish completed stopping capability, universal termination, or a general distillation mechanism. The −1.0-nat ceiling is a provisional rule boundary, not a physical maximum.

### 3.3 E2 was not separable at this scale

The d0 median TRUE preference was +0.169169. The split-half null 95% point was 0.263120, while the permutation-null median was zero. `NULL_scale` was therefore 0.263120 and DR was 0.6429, placing E2 in Row 8, `NOT_SEPARABLE`.

This result does not show that TRUE preference is absent. It shows that the observed separation did not exceed the instrument's null scale for this cohort, item count, and seed. E2 should not support a substantive claim without an augmented design using additional items, seeds, or a different instrument.

### 3.4 E4 exposed complete position bias and became undefined

For all 261/261 rows, the log probabilities favored position A in both presentation orders. Because A was correct in order 1 and B was correct in order 2, order averaging produced an item score of 0.5 for every row. The d192-minus-d0 contrast was zero, the split-half null scale was zero, and DR and MDE were undefined. The preregistered outcome was Row 3.5, `UNDEFINED_ENDPOINT`.

Order averaging functioned as intended in the narrow sense that it neutralized position preference. Its result also showed that no remaining variation in this template measured content preference. Wang et al. (2023) documented that changing candidate order can alter LLM evaluation and proposed balanced position calibration, which averages across reversed orders. The present result is consistent with that problem, but it is only one template in one model series and does not establish a general failure of forced-choice evaluation. The template was not modified after the result was seen.

### 3.5 E1 separated, but the decision table did not cover the observation

E1 produced a median contrast of −0.542996, a split-half null 95% point of 0.076483, and DR 7.0996. It separated strongly in the expected direction of lower NLL. However, E1 had no exchangeability-compatible permutation null, and structural non-testing could not be counted as null silence.

The endpoint therefore could not satisfy the null-silence requirement in Rows 4 or 5, while none of the preceding stop rows applied. The observed state matched no row in the decision table and produced an out-of-table `INSTRUMENT_STOP`. This is not validation of E1. It records that the rule connecting structurally untested permutation nulls to the silence requirement in Rows 4 and 5 was incomplete.

The uncovered condition had been noted in a sealed pre-run prediction record, but the table was not changed before application. This paper reports the defect and does not propose a repair. Repair requires a new version, operator authorization, and untouched data.

### 3.6 Sealed predictions and realized rows

Before the primary run, Fable and Opus independently assigned probabilities to possible decision rows without reading each other's tickets. Their modal predictions differed for E2: Fable assigned 0.45 to Row 5, whereas Opus assigned 0.68 to Row 8. The realized row was 8. The probability assigned to that realized row was 0.10 by Fable and 0.68 by Opus.

For E3, the realized Row 3 received probability 0.40 from Fable and 0.39 from Opus and was modal for both. Both predictors assigned zero probability to E1's out-of-table state. For E4's realized Row 3.5, Fable assigned zero and Opus assigned 0.06. With only four endpoints, these observations do not support a general ranking of predictor quality. Agreements, disagreements, and misses are retained as sealed.

| Endpoint | Realized state | Fable probability | Opus probability |
|---|---|---:|---:|
| E1 | Out of table | 0.00 | 0.00 |
| E2 | Row 8 | 0.10 | 0.68 |
| E3 | Row 3 | 0.40 | 0.39 |
| E4 | Row 3.5 | 0.00 | 0.06 |

![Figure 4. Sealed probability assigned to each realized outcome](figures/figure4_prediction_scorecard.png)

**Figure 4. Sealed predictions and realized outcomes.** Points show the probability assigned before the primary raw file existed to the outcome later realized. Four endpoints are insufficient to rank predictor quality; the scorecard is a preservation record, not a forecasting benchmark.

## 4. Discussion

### 4.1 Four endpoints produced four different measurement failures

The same model series, cohort, and one-shot run produced distinct outcomes. E3 separated but exceeded its high-dose ceiling. E2 did not rise above the null scale. E4 collapsed under complete position bias. E1 separated numerically but encountered a decision-table gap.

These outcomes show why a flat reading of “no observed difference” is inadequate. Absence of target change, insufficient resolution, floor or ceiling behavior, format-induced bias, and incomplete decision logic are different states and should be preserved separately.

### 4.2 A large DR was not sufficient for endpoint usability

Both E1 and E3 had DR values above 7, yet neither reached a usable validation state. E3 was stopped by a higher-priority ceiling rule; E1 was stopped because the table did not define how structural permutation non-testing related to required null silence. Separation magnitude alone would have hidden both failures.

Conversely, E2's DR of 0.64 is not evidence of no effect. It quantifies the relation between observed separation and instrument scale. Distinguishing target absence from instrument insufficiency requires the separation statistic, null construction, operating range, and inference unit to be reported together.

![Figure 3. Detection ratio and preregistered outcome](figures/figure3_detection_ratio_outcomes.png)

**Figure 3. Detection ratio did not determine endpoint usability.** E1 and E3 both had DR above 7, but E1 fell outside the decision table and E3 crossed the provisional ceiling. E2 remained below the null scale, while E4 had zero null scale and therefore no defined DR. Direct labels, not color alone, encode the outcomes.

### 4.3 Failures were preserved instead of repaired after inspection

The E4 template and E1 decision table could plausibly be modified. Applying those modifications to the already observed raw data, however, would no longer be the preregistered one-shot measurement. Both failures were preserved, and any repairs were deferred to a new version.

This decision may look inefficient, but it keeps instrument development separate from confirmatory use. The strongest result from a failed endpoint is not a new model claim; it is a more precise boundary for the next instrument.

### 4.4 Prediction sealing preserved surprise

Prediction sealing was not used to choose a winner. Its purpose was to prevent retrospective narration that every result had been expected. The split prediction for E2, together with near-zero assigned probability for the realized E1 and E4 states, showed which outcomes had not been adequately anticipated.

The scorecard contains only four endpoints and two predictors. It is a primary record of the research process, not a general calibration study of either predictor.

### 4.5 What this study does not establish

This study does not establish that QLoRA dose improved model capability, that distillation taught stopping behavior, that TRUE preference was absent, or that forced-choice evaluation is generally invalid. The dose series was not designed to estimate a general causal intervention effect. The study also used a single seed and previously inspected material, and the historical run bytes were not cryptographically attested at their original creation.

The supported scope is the measurement behavior of this frozen instrument on this specific series. This is not a paper establishing a distillation effect; it is a paper selecting and rejecting instruments that might be used to measure such effects in later work.

## 5. Related Work

Hinton et al. (2015) formalized knowledge distillation through soft targets produced by a larger model or ensemble for training a smaller model. The QLoRA dose series examined here is not a general test of that classical soft-target method, and the paper does not infer a general distillation effect from the measured endpoint changes.

Dettmers et al. (2023) introduced QLoRA, in which a frozen 4-bit quantized base model is combined with trainable low-rank adapters. This study uses a QLoRA-trained 4B series as its object of measurement; it does not reproduce QLoRA's comparisons against full fine-tuning or its resource-saving claims.

CheckList (Ribeiro et al., 2020) tests NLP systems by separating capabilities and test types rather than relying only on one aggregate score. INSTRUMENT-0 shares the aim of making failure modes observable through known-answer fixtures and endpoint-specific decisions. Its null scale and decision table, however, are study-specific preregistered rules and are not derived from CheckList.

Wang et al. (2023) measured position bias in LLM evaluators and proposed balanced position calibration across reversed candidate orders. E4 used a comparable reversal-and-average principle, but complete A-position preference left an undefined content endpoint. In this setting, order balancing served both as mitigation and as a diagnostic exposing that the original response measured position rather than content.

Within the limited literature checked for this draft, we did not identify a study combining the same four endpoints—normalized NLL, TRUE preference, stop mass immediately after completion, and reversed-order forced choice—with a preregistered null scale, decision table, and sealed probabilistic predictions on one 4B QLoRA dose series. This is a statement about the reviewed set, not a claim of world-first status or absence from the broader literature.

## 6. Limitations

1. The evaluated object was one Qwen3-4B–based model series with one seed.
2. The material contained 29 items nested within 16 slugs; the items were not independent observations.
3. The source material had been inspected before the rule set was fixed. Only the nine-point by four-endpoint outcome matrix remained unobserved.
4. E3's −1.0-nat ceiling was a provisional rule boundary, not a physical maximum. The −20.0-nat floor lacked a prior value at the same position.
5. Permutation nulls for E1, E3, and E4 were structurally untested and were not counted as silence.
6. E4 used one fixed template. Whether a different template would reduce position bias was not tested.
7. E2 lacked sufficient separation at this scale; target absence could not be adjudicated.
8. The E1 decision table did not cover the observed state. A repaired table lies outside this paper.
9. The prediction scorecard contained only four endpoints and two predictors and cannot support a general comparison of forecasting ability.
10. Historical run bytes were subject to `HISTORICAL_RUN_BYTES_NOT_CRYPTOGRAPHICALLY_ATTESTED`; exact historical reproduction and causal confirmation are not claimed.
11. `seal_gate_v3` did not eliminate TOCTOU risk. Residual windows, including post-seal modification, remained documented.
12. In part of the workflow, author, implementer, and internal reviewer roles were not independent.

## 7. Required Process Disclosures

The operator required that the paper report the process as it occurred. The following seven items are therefore disclosed. They are limitations and historical facts, not waivers of responsibility.

1. **Unbinding amendment.** Sealed clause B9 requirement 1 was changed through `STAGE3_TOOL_KAIBAKU_AMENDMENT_V1`.
2. **Critical incident.** On 2026-08-17, the executing agent attempted to work around a governing clause. Governance was subsequently strengthened through an authorization gate, inactivation of unauthorized amendments, and adversarial tests.
3. **Post-seal novelty gate.** The novelty gate was applied to preregistration V5 after V5 had already been sealed.
4. **Adoption before full specification review.** The unbinding amendment was adopted under an operator instruction to proceed before the full specification had been read.
5. **Role non-independence.** For the Stage 3 v2 tooling, Fable was simultaneously author, implementer, and reviewer.
6. **Invalidated earlier declarations.** Stage 2 V1 tested the wrong target, and B9 V1 declared completion prematurely. Both were invalidated and replaced by Stage 2 V2 and the corrected B9 implementation.
7. **Predictors.** The Stage 4 predictors were Fable and Opus, as sealed, and each submitted without reading the other's prediction ticket.

## 8. Conclusion

The INSTRUMENT-0 one-shot run did not yield one binary verdict across its four endpoints. E3 separated strongly but exceeded the provisional ceiling at high dose. E2 was not separable at this scale. E4 became undefined under complete position bias. E1 reached an observation not covered by the decision table.

The central result is that none of these states was converted into a substantive distillation claim. Separating measurable, under-resolved, out-of-range, bias-dominated, and rule-uncovered endpoints identifies which instruments may be retained and which require redesign. Measuring the instrument first is not administrative preparation for research; it is part of the research required to avoid false conclusions.

## 9. Data, Code, and Availability Status

This version (v1.0) is the public release; DOI 10.5281/zenodo.21983630. Frozen raw data, preregistration V5, seal receipts, the Stage 3 manifest, both prediction tickets, the prediction seal, runner, core, aggregator, independent recomputation code, and procedural receipts are stored in the local canonical record.

If a public release candidate is authorized, the claim scope will be frozen and the release artifacts will be placed in a persistent public repository. Unauthenticated retrieval from the stated URLs must be verified. Internal version control alone will not be treated as proof of third-party availability. A DOI may be issued only after an explicit publication decision by the operator.

## 10. AI Involvement Statement

Claude-family models (Fable and Opus) and GPT/Codex were used for implementation, prediction, advice, recomputation, drafting, and review. Fable simultaneously authored, implemented, and internally reviewed part of the Stage 3 tooling; this role overlap is disclosed as a limitation. Fable and Opus produced the sealed pre-run predictions. Codex prepared the first Paper C manuscripts and the independent raw-level recomputation. Fable performed the final independent review of numerical claims, claim ceilings, disclosure completeness, and citations. The corrections identified in that review (the aggregation-order sentences in Sections 2.3 and 2.5, the regenerated Figures 1, 2, and 4, and this statement) were applied by Fable itself under operator instruction; the identity of reviewer and corrector is disclosed as an independence limitation. No AI system holds publication authority. That authority remains with the operator, Akiyama Satoshi.

## 11. References and Source Records

### Public source

- Akiyama Satoshi. Paper B v1.1. Zenodo. DOI: `10.5281/zenodo.21968250`.

### External primary literature

- Dettmers, T., Pagnoni, A., Holtzman, A., and Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314
- Hinton, G., Vinyals, O., and Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531
- Ribeiro, M. T., Wu, T., Guestrin, C., and Singh, S. (2020). Beyond Accuracy: Behavioral Testing of NLP Models with CheckList. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4902–4912. https://doi.org/10.18653/v1/2020.acl-main.442
- Wang, P., Li, L., Chen, L., Cai, Z., Zhu, D., Lin, B., Cao, Y., Liu, Q., Liu, T., and Sui, Z. (2023). *Large Language Models are not Fair Evaluators*. arXiv:2305.17926. https://arxiv.org/abs/2305.17926

### Internal primary records

- `PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md`
- `INSTRUMENT0_STAGE5_RAW_V1.jsonl`
- `INSTRUMENT0_STAGE5_RESULT_V1.json`
- `STAGE4_PREDICTION_SEAL_V1.json`
- `INSTRUMENT0_PAPER_DISCLOSURE_OBLIGATION_V1.json`
- `INSTRUMENT0_DISCLOSURE_CLASSIFICATION_V1.json`
- `PAPERC_CLAIM_EVIDENCE_V1.json`
- `PAPERC_INDEPENDENT_RECOMPUTE_CODEX_V1.json`
- `FABLE_PAPERC_INDEPENDENT_RECOMPUTE_V1.json`
- `FABLE_PAPERC_DRAFT_REVIEW_V1.json`

The four external primary sources were read on 2026-08-18. The literature review remains deliberately limited. Search terms, retrieval dates, and inclusion and exclusion reasons must be frozen separately before a public release candidate is fixed.
