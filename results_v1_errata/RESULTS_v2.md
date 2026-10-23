# Recurrent-core transfer results, presentation v2

Additive errata E-1 through E-6. The protocol, freeze commit `d118ae18d592d6ddf1de111752b2d4d0671d91af`, and `recurrent_core_results_v1/` are unchanged. Nothing was retrained or rerun. Counts below were read back from the committed JSON.

Protocol sha256 `63c463c7b2df96d6feec49cfa34d1ec0f010ce017d4b31aab051f06af76e9506`.

## Claim

In W2, recurrent training produced a GRU-8 core whose predictive advantage over its matched initialization survived replacement and retraining of the readout in 10/10 fresh seeds. Hidden-to-hidden matrix reversion did not meet the prespecified joint criterion for any matrix. Advantage over the selected tuned frozen GRU-8 with 843 trainable readout parameters was observed in 10/10 seeds. That rival met A-FIT in 0/10 seeds within the declared grid. Selective variation reduction was not demonstrated under the gated criterion.

Transfer is demonstrated. The stronger, preregistered matrix-specific claim is not. The formatting repair in `assemble_claim_v2.py` is recorded in E-1 and is not this paragraph.

## Corrected labels

Literal verdicts are unchanged. Both tuned-rival labels are qualified within the declared grid. SPECIFIC counts are joint passes. Variation counts are descriptive.

| label | value |
| --- | --- |
| E1 | E1 REPLICATED (10/10) |
| Transfer | TRANSFER SHOWN (10/10 passes, 0 invalid) |
| F-INIT A-FIT on TEST | 0/10 |
| F-TUNED32 A-FIT on TEST | 0/10, descriptive |
| §4 (i) | ADVANTAGE OVER TUNED FROZEN GRU-8 (843 TRAINABLE) OBSERVED (10/10), within the declared grid |
| §4 (ii) | TUNED FROZEN GRU-8 MEETS A-FIT AT THIS BUDGET: not met (0/10), within the declared grid |
| SPECIFIC(r) | SPECIFIC(r) NOT DEMONSTRATED: 1/10 joint passes; directional 8/10; materiality 1/10 |
| SPECIFIC(z) | SPECIFIC(z) NOT DEMONSTRATED: 3/10 joint passes; directional 9/10; materiality 3/10 |
| SPECIFIC(n) | SPECIFIC(n) NOT DEMONSTRATED: 3/10 joint passes; directional 3/10; materiality 10/10 |
| Variation r / z / n | selective variation reduction not demonstrated. Descriptive condition counts 1/10, 1/10, 9/10. The positive label additionally requires REPLICATED SPECIFIC |
| P1 | not met, 0/10 for each distinct core (trained core = CAND = F-TRAINED; initial core = F-INIT) |
| P2 | PIPELINE VALID (E3-v2). Meaning narrowed: validates detection, not subspace recovery or specificity |

Invalid seeds: none for §3, §4, or §5.

## Joint passes

| k | directional | materiality (≥ B/4) | joint SPECIFIC |
| --- | --- | --- | --- |
| r | 8/10 | 1/10 | 1/10 |
| z | 9/10 | 3/10 | 3/10 |
| n | 3/10 | 10/10 | 3/10 |

For r and z, most seeds are below the declared materiality threshold. For n, sensitivity is also elicited by matched-norm random perturbations in 7/10 seeds. The learned n direction passed the joint criterion in seeds 101, 106, and 107. Controlled interventions changed forecasts and loss. What failed is the replicated directional-plus-materiality criterion.

## Grid

Selection chose the upper tested gain, g=2, in 10/10 seeds and the lower tested offset, b=−2, in 9/10. Both tuned-rival conclusions concern the declared grid and training procedure. Performance outside that grid is unmeasured. Boundary selection motivates further investigation but does not establish the location or performance of an unrestricted optimum.

About 4.8–17.1× improvement would be needed to beat the ≤ 1/2 advantage threshold. About 10–34× would be needed to match CAND. Neither estimate justifies "very unlikely to be grid-limited."

## P1

CAND and F-TRAINED share the same recurrent core and therefore identical P1 states and results. The specified cross-fitted linear decoder failed the predictive-and-stability criterion on both trained and initial cores. This does not establish absence of covariance information, a nonlinear predictive representation, or a low-dimensional causal mechanism.

## P2

The frozen label remains PIPELINE VALID (E3-v2). Its meaning is narrowed: it validates detection, not subspace recovery or specificity.

Known-Q was LOCALIZED in 100/100 draws at every nuisance scale. The fitted decoder was LOCALIZED in 100/100 at s ∈ {0, 0.03, 0.1, 0.3, 1.0}, including s = 1, where the median largest angle to the true subspace is about 52°. Passing the forecast-ratio criterion at that angle does not validate recovery of the true subspace or specificity across arbitrary representations.

Coverage and rank were not per-draw gates. They are reported here from the committed P2 records. Rank is the cross-fitted decoder rank on the two folds. The angle is the fitted fold's largest principal angle to span(Q), and the median is over the 200 fold values stored for that scale.

| s | fitted LOCALIZED | fitted coverage_ok | fitted rank_ok | median coverage fraction | median largest angle to span(Q) | max largest angle to span(Q) |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 100/100 | 100/100 | 100/100 | 0.308 | 8.5×10⁻⁷° | 2.3×10⁻⁶° |
| 0.03 | 100/100 | 100/100 | 100/100 | 0.308 | 5.63° | 22.3° |
| 0.1 | 100/100 | 100/100 | 100/100 | 0.308 | 13.7° | 35.7° |
| 0.3 | 100/100 | 100/100 | 100/100 | 0.306 | 27.1° | 61.1° |
| 1 | 100/100 | 94/100 | 100/100 | 0.302 | 52.4° | 79.2° |

Known-Q coverage_ok and rank_ok are 100/100 at every scale. Fitted rank is 3 on both folds in every draw. At s = 1, six fitted draws fail coverage_ok while remaining LOCALIZED.

P2− zero-effect is True (maximum absolute change 0) for the cache-assisted implementation only. It is descriptive and does not determine the P2+ label. See E-5.

## Q ledger

| question | status |
| --- | --- |
| Q-LEARN | learned recurrent contribution that transfers to fresh readouts. |
| Q-CAUSE, basic intervention dependence | demonstrated forecast/loss sensitivity to the specified weight changes. |
| Q-CAUSE, preregistered specific organization | not demonstrated. |
| Q-NECESSITY | not tested. |

No localized content, C4, consciousness, or organism conclusion follows.

## Approval

Neural training for this study was approved by Aidan Ahern on 2026-10-20 at 8:55 PM ET ('Yes, approve it once Astra clears it'). Consult #12 had cleared the protocol with named edits, applied in FINAL sha 63c463c7. The hashed header's 'pending' wording predates that approval and is retained unedited.
