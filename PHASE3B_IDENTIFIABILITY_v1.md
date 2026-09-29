---
description: Pretraining decision identifiability and STOP conditions for the four-factor competitive-access world
---

# Phase III-B identifiability

## Full belief and elementary reductions

For the world in `PHASE3B_ENVIRONMENT_v1.md`, let `n_j` be the number of
ones in port `j`'s two earlier readings. With fair independent priors and
flip probability 1/5, the posterior odds for `z_j=1` are
`4^(2*n_j-2)`. Thus each posterior `q_j` lies in
`{1/17, 1/2, 16/17}` and the exact evaluator belief is the product
of four Bernoulli distributions. The 81 belief configurations fit in a
four-coordinate finite-state counter, not a mysterious neural ontology.
Each specialist's minimal sufficient input is its own decision-relevant
posterior (or the parity posterior for integration) plus its local reading
and public context. A fixed real number of unbounded precision could encode
the entire belief; therefore no scalar *dimension* argument is admissible.
Capacity is defined by **eight discrete on-wire messages** instead.

## Decision-relevant competition, not just factor counting

Use the consequence-bearing specialist losses specified in
`PHASE3B_SPECIALISTS_v1.md` (these definitions are part of this gate):
immediate binary control of `z_1`, delayed `z_2` commitment with abstention
cost 0.18, and binary parity of `z_3 XOR z_4`, with a private local noisy
reading of `z_3`. Consider context zero, fix `n_4=2`, and vary
`n_1,n_2,n_3` independently through 0, 1, 2. Before receiving a common
message, the three consumers must choose *functions* of their independent
local readings, not merely three constant action bits:

* S1 requires always zero, follow-local, or always one as `n_1` varies.
* S2 requires bet only on a corroborating local bit (otherwise abstain),
  abstain regardless of local bit, or the opposite corroborating bet as
  `n_2` varies. A contradictory bit changes odds 16 to 4, yielding
  posterior error 1/5, which exceeds the 0.18 abstention loss.
* With the sign of `z_4` strongly determined, S3 requires constant parity
  one, inverse-local parity, or constant parity zero as `n_3` varies.

These are 3 x 3 x 3 = **27 distinct triples of local-to-action maps** with
positive probability in the same public context. Since a consumer gets
only its local bit and a shared eight-symbol message, no deterministic
three-bit shared encoder can tell all three which of those 27 policies to
use. Thus the fixed message budget is decision-relevant even if its address
is treated as arbitrary data. This is an exact pigeonhole proof of at least
one unavoidable policy collision, **not** proof the proposed selector is the
best eight-message code or has a positive average-reward advantage.

## Matched-history witness for a factor-specific menu

Fix context, clock, null current observation, and local signals. Set
`n_3=n_4=1` in two histories. In history A, `n_1=2,n_2=1`;
in history B, `n_1=1,n_2=2`. Every history has positive probability.
S3 remains uninformative because `z_4` has posterior 1/2. Selecting
stream 1 in A changes S1 from local-only risk 1/5 to 1/17; selecting
stream 2 in B permits S2 to exploit its strong earlier evidence instead
of always abstaining at risk 0.18. The competitor stream has conflicting
earlier readings, hence no strong factor-specific message to send.
Accordingly, under the *factor-truthful single-stream menu*, the preferred
occupancy differs even though context and present observations are identical.
A clock-only or fixed-context address cannot choose correctly in both.
At other contexts a rotation of the ports changes which inferred factors
matter; thus a globally fixed content address is not optimal.

## Reductions that survive the gate

The address is two of the three transmitted bits. A selector may encode two
aggregate Boolean decisions in it without conveying literal stream
contents. Even if source ports are separated, ordinary learned routing is
an alternative explanation. An unrestricted eight-message learned encoder
can simulate *every* candidate message by computing its address and payload
from the same observation history and context. With more encoder capacity it
may do strictly better; it is an obligatory equal-bandwidth rival. With
full belief broadcast, Bayes risk is weakly lower than under any restricted
message: the receiver can ignore extra information. An accuracy win over
ideal unlimited belief broadcast is mathematically impossible. Therefore
architectural value must be prespecified as a resource/transfer/generalization
tradeoff, **not** an absolute accuracy advantage over unconstrained access.

The 27-policy lower bound meets the H3 minimum: scarcity creates a real
decision collision, and matched histories require different factor-specific
contents. It does not identify semantic learned latents, let alone prove
that workspace occupancy beats an equal-budget arbitrary code. H6 must
include that code. If its addition leaves no falsifiable candidate-only
value claim, STOP before final training. If H3's proof fails under the
implemented specialist losses or if receivers see uncharged private state,
STOP before training and record an identifiability failure.

The calculation here is analytic, not measured neural performance. No
workspace or consciousness inference follows from it.