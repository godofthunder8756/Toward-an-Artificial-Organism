---
description: Phase III-B post-final H3 witness and H10 information diagnostics
ms.date: 2026-09-29
---

# Phase III-B H3/H10 secondary diagnostics v1

The [standalone read-only runner](phase3b_results_v1/phase3b_h10_runner_v1.py)
has SHA-256 `24e311ea45074bc67a72e5cf49560c88b683ce806376b07ed622d534562b952b`.
Its [results](phase3b_results_v1/phase3b_h10_diagnostics_v1.json)
have SHA-256 `28c182950275364a21a694b9deaae79275e8299e1f37c1d6fdef57b96c60f37b`.
It verified the audited final manifest, source hashes, signed approvals,
candidate/R4 checkpoint file and state digests, and final decision
replay before analysis. The primary models were frozen; no primary
optimizer step or new held-out selection occurred.

## The matched-history test

At context 0, the positive-support H3 groups are posterior-count
vectors A=`(2,1,1,1)` and B=`(1,2,1,1)`, with eight complete sensory
histories each. The *analytic factor-truthful source menu* prefers
different content in these two groups. That menu is a theoretical
witness, **not** the observed learned policy.

All **64 Cartesian A/B pairs per seed** were evaluated for 16 seeds
(1,024 pairs), with both possible private-bit responses of all three
heads and exact conditional risk integrating latent truth and local
sensor noise. The candidate's selected address changed across
**0/1,024** matched pairs, and an I1 cross-pair address-only swap had
zero risk effect in **1,024/1,024** pairs. Response maps changed in
32 pairs, but so did R4's maps in 32; a changed map alone does not
identify useful competition. Candidate and R4 paired risks tied in
256 pairs. The candidate's equal-history expected joint risks were
approximately **0.291863** for A and **0.374583** for B; R4's were
**0.299951** and **0.318333**, respectively. These matched histories
were enumerated without selecting only the pairs on which the
candidate changed. I3 forced-source and all I1 alternate-address
conditional risks are retained per history/seed in the result JSON.

## Frozen representation and channel

A fixed, training-only nearest-centroid probe of each candidate
port state decoded its own two-observation posterior count on the
4,096 held-out histories at **72.89%** accuracy, versus a
**34.04%** training-majority-count baseline. This shows that
port-private states often contain usable evidence, **not** that
the selector transmitted the right source or that the workspace
had unique semantics. The decoder and evaluator count never entered
an original model's forward path.

Across the final seeds, the mean **within-seed** address entropy at
contexts 0/1/2/3 was approximately **0.00994 / 0 / 0.00301 /
0.01868 bits**. At context 3 the mean within-seed payload entropy
was approximately **0.12026 bits**. Port-use totals *pooled across
seeds* at context 3 were `[24,793, 16,384, 4,096, 20,263]`
out of 65,536 episodes. Pooled port use is not within-model
competitive switching: different models can each hold a nearly
constant but different address. Empirical address/truth mutual
information was small; the result JSON reports per-factor values
and word/truth information separately at each context.

These observations sharpen the bounded negative: evidence could be
represented privately, but the learned candidate did not show the
prospectively desired state-dependent source switch on H3's witness.
The exact 27-response-function scarcity proof still stands; it never
implied that this optimizer or candidate would exploit the available
competition. Analytic conditional risks and empirical mutual
information are secondary diagnostics, not fresh confirmatory tests.
