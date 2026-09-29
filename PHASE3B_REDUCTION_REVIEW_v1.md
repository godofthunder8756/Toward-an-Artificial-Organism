---
description: Phase III-B H11 pretraining reduction audit and explicit STOP rules
ms.date: 2026-09-28
---

# Phase III-B reduction review v1

## What H3 did and did not establish

The [H3 calculation](PHASE3B_IDENTIFIABILITY_v1.md) gives posterior levels
`{1/17, 1/2, 16/17}` for each of four independent factors. At fixed public
context and `n_4=2`, independently varying `n_1,n_2,n_3` yields 27 distinct
triples of response functions to the specialists' private local bits. An
eight-symbol common word cannot implement all 27 exactly. The matched-history
pair changes the *preferred* source under a factor-truthful one-stream menu.
This establishes decision-relevant scarcity and an opportunity for adaptive
selection, not exclusivity of the proposed selector. Unlike the earlier
[Phase III verdict](PHASE3_VERDICT_v1.md), this world has no one-dimensional
LLR sufficient for all decisions. It still has an exact four-coordinate
finite-state belief: do not market a learned vector as inherently irreducible.

## Binding reductions for H6 and H11

* The independently trained primary set is R1 unlimited learned broadcast,
  R2 monolithic recurrent, R3 private-state specialists,
  R4 fixed-selector workspace, R8 learned shared encoder without bottleneck,
  and R9 equal-budget unrestricted learned eight-symbol encoder. R4 retains
  a fixed-selection workspace as an ablation; the others are no-workspace
  alternatives. The
  contextual fixed-selector sweep includes context/clock routes, not just a
  weak global constant. Compare all six at the primary resource cap.
* R5 oracle belief broadcast is EXTERNAL: the evaluator supplies exact
  four-counter beliefs without a wire limit. By information monotonicity,
  its Bayes risk cannot exceed the optimum achievable from the candidate's
  inputs. A candidate accuracy win over that ideal is a scoring or leakage
  error, not a primary success.
* R6 oracle selector over learned latents is EXTERNAL: freeze the candidate's
  learned port representations, then choose among their legal one-bit port
  messages using evaluator-only conditional loss information. It measures
  the selection gap under the *learned* contents; it neither supplies
  posterior features to the candidate nor represents an autonomous win.
* R7 independent sufficient-statistic copies are EXTERNAL evaluator-supplied
  four-counter beliefs separately delivered to each consumer, with no shared
  workspace and no eight-symbol bottleneck. These are not independently
  learned private encoders. R7 and R5 test the full-information reduction
  under separate versus shared readout; a learned-copy experiment would need
  its own explicit learned status and budget and could not inherit R7's ID.
* Optional R10 analytic bounded-code oracle, if exactly certified, is an
  EXTERNAL finite-channel lower bound on achievable risk. Optimize all three
  local-to-action maps with the actual losses, not three fixed action bits;
  an unverified solver output cannot certify an optimality gap.
* R9 sees the same common observation history and public context, emits one
  of eight unrestricted messages, and feeds identical local-input heads.
  Its allowable architecture contains the candidate computation as a
  subfamily, including the four ports, selector, and `(address,payload)`
  message. Demonstrate a byte-identical constructive clone and count actual
  parameters, forward operations, memory, samples, and training cost. The
  clone is an expressivity control, not an independently trained result;
  equal bandwidth alone does not guarantee that independently optimized
  models have equal practical cost or convergence. R9's function-class
  inclusion rules out intrinsic superiority to its optimum.

## Claim that survives the reductions

The one testable claim is **contingent, not universal**: with a fixed,
predeclared optimization recipe, training sample allowance, and measured
resource caps, the port-partitioned candidate could obtain lower
held-out-context normalized decision loss than all six independently trained
primary comparators, including fixed-selector R4 and unrestricted R9.
That is an empirical inductive-bias or
sample-efficiency result in this training regime, never a proof that an
equal-budget unrestricted encoder cannot learn or implement the same map.
Matched resource and transfer comparisons must disclose Pareto-dominated
models rather than hide them behind an architecture label.

## Stop and negative-result rules

* STOP before training if the implemented losses, local-signal visibility,
  or message alphabet break H3's 27-response-function proof or if consumers
  read uncharged state. Publish the failure as identifiability, not as an
  optimization problem.
* STOP before an executable freeze if a concrete R9 implementation cannot
  simulate the candidate's message function within the declared primary cap
  and wire budget with openly counted resources, or if the only proposed
  positive gate is candidate-only lesion behavior or ideal-accuracy dominance.
  Revise the design in a new version, not the rival away.
* If R9 simulates the candidate and matches/beats it when trained, the correct
  result is a negative *architectural* verdict. Do not alter the world, losses,
  budget, or comparator after seeing that result.
* If the primary envelope matches/beats, I1-I7 remain causal diagnostics
  only. A result against R4 but not R9 is ordinary routing or coding; a
  result against R3 but not R1/R2/R8 is generic shared inference. A result
  against independently trained R9 under one recipe is a bounded
  optimization/transfer effect, not necessity. R5/R6/R7 cannot be counted
  as independently learned rivals or candidate wins.

The previous Phase III proof described prospective tests whose later
[independent audit](PHASE3_INDEPENDENT_AUDIT_v1.md) found insufficient for
candidate-exclusive value. Here R9 and the actual behavioral endpoint are
part of the *admission* contract, not after-the-fact additions. No neural
results, new Phase III verdict, or theory-indicator inference is asserted.
