# A6 exact gate reduction: capacity is sufficient, deployed-class existence remains open

Solver-free derivation for the SAME frozen population/gate. No training,
criterion relaxation, new architecture or global R9 optimum claim.
The [independent arithmetic](a6_decision_v1/analytic_corollaries.py) derives risks
both from posterior formulas and integer enumeration over latent truths.

## Individual information floors

With all legal common observations and a consumer's own sensor available:

| Consumer | Bayes floor |
| --- | ---: |
| S1 | `13/125 = 0.104` |
| S2 | `59/625 = 0.0944` |
| S3 | `164/625 = 0.2624` |

Their mean is the frozen `96/625` full-information floor.
S1 uses three BSC(1/5) readings. S2 rejects ambiguous three-reading posteriors.
S3 combines the three-reading first-factor estimate with the two-reading
second-factor estimate. Other private sensors are NOT granted.

For the actual affine S3 head, one global own-bit slope restricts its maps to
`00,01,11` or `00,10,11`. Even granting unlimited messages and arbitrary
common-history encoding, exact pointwise minimization gives S3 floor
`182/625 = 0.2912` in BOTH orientations. Zero slope is covered by both
relaxations. This is a lower bound, not a new achievable eight-word optimum.
Its assumptions are the mathematical affine semantics of the
[frozen R9 class](R9_FUNCTION_CLASS_v1.md).

## The full R9 gate is equivalent to its joint threshold

Let `g = 21579431/117187500`. If joint mean loss is at most g, the other
two consumer floors bound each consumer's risk from above:

| Consumer | Upper under a joint-gate R9 solution | Strict baseline |
| --- | ---: | ---: |
| S1 | `6516931/39062500 = 0.1668334336` | `1/5` |
| S2 | `6141931/39062500 = 0.1572334336` | `9/50` |
| S3 | `13829431/39062500 = 0.3540334336` | `1/2` |

Each upper is `3g - sum(other consumer lower floors)` and is STRICTLY below
the corresponding baseline. Thus ANY legal shared R9 achieving the joint
threshold automatically satisfies every specialist gate. Conversely a full-gate
solution must satisfy the joint threshold.

The specialist requirements remain frozen. This theorem proves redundancy
for THIS population/architecture/threshold; it does not remove criteria after
observing learned results. Without the S3 orientation floor, the analogous
generic-information bound would not imply S2 competence.

Conditional competence inequalities cannot tighten this particular decision
past the joint gate: they are already implied. The mathematical unresolved
question is therefore existence of a legal shared R9 with joint loss at most g.

## Eight symbols already suffice in the unrestricted class

The independently replayed R10 optimum is `5101889/29296875`.
Its actual codebook also beats every specialist baseline; the new arithmetic
recomputes its components directly from the frozen certificate.

Use the SAME eight decoder policies at all contexts, and let the unrestricted
encoder rotate the belief inputs by context. Independent fair factors imply
identical risk at every context. The contextwise R10 lower applies separately,
so this is also an optimal shared unrestricted four-context construction.

This is EXTERNAL arbitrary coding, NOT the coupled recurrent/affine R9 graph.
It establishes information-capacity adequacy for the complete frozen gate.
It does not establish R9 expressivity, acquisition, credit assignment or
consciousness-relevant organization. The R9 coupling question is not solved by
calling an oracle encoder a deployed neural witness.

## Why a scalar count-collapse relaxation is now legal

In general a multi-specialist conjunction must preserve mixtures of differently
ordered histories with identical counts: one choice may improve S1 and another
S2. The initial F1 safeguard correctly kept these mixtures.

After the proved scalar-gate equivalence, a stronger dominance reduction is
available. Fix an actual shared decoder and U. For each count vector, select
ONE ordered history minimizing the SUM of four-context joint conditional risks.
Its common utility vector and the SAME U produce all four context choices.
This risk is no greater than the original average across histories of that
count. An arbitrary per-count utility relaxation can therefore dominate every
gate-passing actual encoder.

This is a dominance argument for impossibility search, not a literal RNN image
or a constructive witness. It keeps `m(n,c)` and never fixes one word across
contexts. It does not rehabilitate the discarded fixed-message bound.

## Word-label symmetry and compact formulation

Before sorting labels, break encoder ties by a sufficiently small global
lowest-index-favoring bias perturbation. There are finitely many supported
histories/contexts; preserve every positive gap and make all winners unique.
Then permute code rows and corresponding head word columns to sort S1's word
effects. The legal graph, actions, losses and parameter dimensions are unchanged.
This proves the S1 monotone-word symmetry restriction, not a heuristic box.

The compact F2 continuation represents three independent three-map choices
per word/context and shares their encoder assignment. At integer head choices,
it is the same retained joint-policy alphabet as the 27-map Cartesian product,
with fewer product variables. S2 sharing stays dropped; component-wise
dominance is NOT used after restoring it. Exact binary-head Farkas cuts can
exclude unrealizable patterns without excluding any actual-family image.

Numerical LP/MIP bounds and infeasibility are still discovery diagnostics.
Whole-family FAIL needs replayable exact coverage; PASS still needs actual
finite recurrent weights, margins and the real graph. A6 may still end
UNRESOLVED despite these valid reductions.
