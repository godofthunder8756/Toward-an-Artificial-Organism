---
description: Independently reviewed Phase III-B engineering execution freeze
ms.date: 2026-09-29
---

# Phase III-B H16 execution freeze v1

The starting repository HEAD was
`3a7605233436479084fa178dc8b3902ac2bad927`. The exact executable
working-tree sources and governing design documents are identified by the
per-file SHA-256 inventory in the [execution freeze](phase3b_results_v1/finals/execution_freeze.json).
The frozen record's SHA-256 is
`ba6a2969f04423781e818b5961e5d20528148e8586e59b3691bfaa72fc78a98d`;
its preflight snapshot SHA-256 is
`68ea4b862352a2a5a09955122d21330ecae4e0bdb4984ed55151424e2495b554`.
The independent H16 engineering approval was verified against the pinned
Ed25519 public key and this freeze, with approval-file SHA-256
`8b4768940626fc66e6f665d46b86cd291f41cc77bc14a735c52809857ff2b244`.
The signing private key was generated outside the repository and removed
after the phase approvals. Neither the source
snapshot nor an approval by itself is an empirical result.

The freeze embeds installed dependency versions and entry-point hashes,
all seven six-configuration grids, engineering seeds `0..3`, final seeds
`1000..1015`, the draw-seed formula, optimizer/update allowance, training
contexts `0..2`, held-out context `3`, 4,096 final episodes per seed,
the six-member independently trained rival envelope, R4's training-only
route search, and the [three-level resource contract](PHASE3B_RESOURCE_CONTRACT_v1.md).
The binding whole-arm limits are 4,096 trainable parameters and 80,000
declared linear forward MACs per complete episode, with 8,192 training
episodes and 256 optimizer updates per fit. Physical memory-bus traffic,
energy and isolated model peak are **unmeasured**, not inferred from
allocation counts or process high-water marks.

The primary effect is a strict `>0.02` joint-loss reduction against the
**within-seed best of all six** independently fitted comparators, in at
least 14 of 16 final seeds, plus a two-sided exact sign-test `p<=0.01`.
In integer loss units this requires the rival-minus-candidate total to
exceed `12,288` over 4,096 held-out episodes. At 14 wins and two losses
the exact p-value is `137/32768 = 0.004180908203125`; at 13 wins and
three losses it is `697/32768 = 0.021270751953125`. Ties are not wins
and are omitted only from the sign-test denominator. Sixteen seeds make
the prespecified gate attainable; no power claim near the threshold is
made from that fact. Episodes and contexts are repeated measures, not
independent replications.

H15's wiring, H3 scarcity and exact R9 candidate-clone checks passed
unscored tests. The clone is an expressivity control, not an empirical
R9 win. Independent H16 review found no protocol-consistency blocker to
**engineering-only** execution and approved this exact frozen source;
the signed final-phase approval remains absent. Engineering may assess
runability and select configurations using training contexts only. It
cannot modify the endpoint, effect, losses, rival set, resource caps,
or significance rule. Finals require a separate check of untouched
final seeds, selected configurations, source hashes and fresh result
directory, then a separately signed final approval.
