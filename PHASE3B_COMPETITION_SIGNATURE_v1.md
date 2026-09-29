---
description: Phase III-B H8 prospective competitive-access signature and falsifiers
ms.date: 2026-09-28
---

# Phase III-B competition signature v1

## Status and referent

H8 is a design-only signature. No candidate or rival has been trained or scored.
The referent is the four-factor world in [the environment](PHASE3B_ENVIRONMENT_v1.md),
the three losses in [the specialists](PHASE3B_SPECIALISTS_v1.md), and the
eight-symbol channel in [the access definition](COMPETITIVE_ACCESS_DEFINITION_v1.md).
The [H3 proof](PHASE3B_IDENTIFIABILITY_v1.md) is a prerequisite, not a result of
H8: in one public context there are 27 distinct triples of local-sensor-to-action
response functions but only eight common messages. It proves an unavoidable
collision for any deterministic eight-message encoder, **not** that an address
has semantic provenance or that a selected stream is optimal.

## The prospective signature

The candidate has four port-specific acquired private states, one learned
selector, and one shared three-bit word per decision tick: two address bits
and one bit from the selected port. The word is overwritten each tick; all
three specialists read the same word simultaneously. A result is competitive
access only if all of the following hold on planned-denominator evaluations:

1. At fixed tick, public context, null current observation, and fixed local
   sensor bits, varying *earlier* observations can change the transmitted word
   and which earlier source influences the three separate decisions. The
   prespecified witness family includes context 0, `n_3=n_4=1`, with
   `(n_1,n_2)=(2,1)` versus `(1,2)`; all histories have positive probability.
   Under a truthful single-stream menu the preferred source changes from 1
   to 2. A raw address flip alone is not evidence of a better policy.
2. On that family, evaluate all three *local-to-action functions* (both possible
   local bits per consumer), not only the observed action. A content-specific
   source swap must yield the prespecified changed response map and conditional
   loss improvement relative to the R4 fixed-selector workspace's best
   training-selected contextual/clock route. Count
   matched pairs before observing model outputs; report ties and zero-effect
   pairs, never select only histories where the candidate changes its address.
3. The joint normalized loss includes immediate S1 error, S2's irreversible
   delayed bet/abstention loss, and end-of-episode S3 parity error. Report each
   separately; S2 abstention is **0.18**, not zero. Evaluate S2's settlement at
   the following tick, including a terminal settlement after decision tick 11.
   No settlement truth enters later inputs.
4. Conditional source influence and per-consumer message cuts follow the
   I1-I7 surgical plan in [the protocol](ACI_PHASE3B_PROTOCOL_v1.md),
   including I2 blank W preserve L with an out-of-band ablation token and
   I6 specialist-specific cut. Optional leakage and same-word controls
   test for an uncharged read path.
   Intact replay must be byte-identical first. Address, payload, timing,
   readout history, and all other potential side channels are audited. Decoder
   alignment of a learned state to a factor is a reported probe, not a premise.
5. A positive **value** signature additionally clears the protocol's
   prespecified held-out-context primary endpoint against the strongest
   independently trained eligible comparators: R1 unlimited learned broadcast;
   R2 monolithic recurrent; R3 private-state specialists;
   R4 fixed-selector workspace; R8 learned shared encoder without bottleneck;
   and R9 equal-budget unrestricted learned eight-symbol encoder.
   R4 is a workspace ablation, not a no-workspace architecture;
   the other five are no-workspace rivals. Neither the EXTERNAL oracle
   controls R5/R6/R7 nor optional R10 count as autonomous wins.

The witness is an exact statement about a restricted factor-truthful menu,
not a claim that the candidate implements that menu. For the actual learned
candidate, measure both the observed policy and a separately labelled
counterfactual oracle under the menu. A source name or a favorable action
under intervention cannot be counted as a rival-exclusive benefit.

## Failure and attribution

* If local inputs, hidden recurrence, feedback, or address timing carry an
  uncharged history signal to a consumer, the channel contract fails. STOP
  before training if the violation is in the design; if discovered after a
  freeze, invalidate that version rather than re-label its result.
* If R4 fixed routing matches the candidate on matched histories or final
   value, the state-dependent selection hypothesis fails; preserve the world
   and report the fixed-router reduction.
* If R9 or another eligible no-workspace rival matches the primary endpoint,
  the rival-exclusive empirical value hypothesis fails even if source swaps
  move outputs. A common-message causal effect is not architectural value.
* If the candidate's address acts as arbitrary aggregate data, classify the
  mechanism as an eight-symbol code/router. The address is charged, but its
  name does not make it occupancy. Source-specific effects require controls
  that preserve the on-wire code and isolate actual port-specific evidence.
* If R5 oracle belief broadcast or R7 independent sufficient-statistic copies
   have lower loss, that is expected: each is EXTERNAL with full evaluator
   belief and can ignore extra information. A candidate win over their ideal
   Bayes risk is a leakage/scoring error.
   R6 oracle selector over learned latents is EXTERNAL and probes selection
   headroom, not autonomous learning.

## Ceiling

At most, a future *empirical* pass can support a conditional training-budget
or held-out-context value of an acquired, port-partitioned access policy in
this world. It cannot prove a necessary workspace, unique semantic latents,
an advantage over optimal unrestricted eight-symbol coding, unlimited
broadcast, N1 maintenance, N3 regulation, O3, or consciousness.
