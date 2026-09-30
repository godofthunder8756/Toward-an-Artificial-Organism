# Shared four-context R9: bounded coupled lower-bound investigation

**Status: UNRESOLVED. Stage A only. No neural training, gradient fitting,
optimizer sweep, or Stage B was run.**

The certified global bracket remains
`5159249/29296875` <= optimum <=
`8921732/29296875`.
The prospective joint gate is `21579431/117187500`
(`0.184144477867`).
The bracket straddles that limit. Neither a global lower bound excluding the
gate nor a legal shared upper satisfying it was established. Failure of the
published upper to pass is **not** proof that every deployed arm fails.

## Actual graph and the legitimate relaxation

The trunk processes the eight common readings and fixed schedule without context.
The selector is `argmax_m (r_m(H) + U[m,c])`, with lowest-index ties.
Each specialist has logits `b[a,m] + d[a,c] + s[a]*local_bit`;
all three see the same word in a given context. The word may change with context.
No claim here identifies S1/S3 words across contexts.

The MILPs replace `r_m(H)` by arbitrary scores. Eighty-one belief cells suffice
for this relaxation: for fixed U and decoders, each same-belief history has
the same **four-context total** cost for a given selector pattern. Select the
least-total-cost history's pattern and copy it to all histories in that cell.
Its arbitrary-score witness remains feasible and cannot increase expected
cost. This does not assert that the RNN itself depends only on belief counts.

For S1 and S3, both global slope orientations are included, giving four cases.
Within an orientation the complete binary local-bit policy alphabet is
constants 0/1 and follow (positive) or reverse (negative). Equal slopes are
covered by the constant maps. For S2, sharing is dropped and every policy is
replaced, when necessary, by a pointwise-dominating member of
`(0,2), (2,1), (2,2)`; the code exhaustively checks that dominance using exact
population costs. This replacement is valid only because S2 sharing is dropped.
S1/S3 sharing is retained as necessary two-cycle constraints, not falsely
asserted to be a sufficient affine-head characterization.

## Correct no-cross revealed preference

For two contexts c,d and distinct words m,n, a history choosing (m,n)
implies
`U[m,c]-U[n,c] >= U[m,d]-U[n,d]`.
A history choosing (n,m) implies the reverse inequality.
If both patterns occurred, all four selection inequalities would be ties.
Lowest-index tie-breaking would then require both m<n and n<m. Thus the two
opposite switches cannot both occur. The MILPs enforce these inequalities
with binary orientation variables, without a numerical big-M.

Binary decoder logits have difference `B[m]+D[c]+S*bit`. Their threshold
tables cannot reverse the ordering of a word pair across contexts/local bits,
or the ordering of a context pair across words/local bits. Those necessary
two-cycle constraints are also enforced. Longer revealed-preference cycles,
complete affine-decoder feasibility, S2 sharing, and the RNN constraints are
not enforced; dropping them is a relaxation, never a legal upper witness.

A legal context-changing counterexample has zero trunk and state-code weights,
`U[m,c]=2` for m=c and zero otherwise. Its chosen words are 0,1,2,3, even for
one fixed H. Zero heads always choose action 0. It is a legal width56 R9 and
invalidates any assumption that one H must keep one word across all contexts.

## Attempt 1: exact obstruction for the published fixed codebook

Using the published positive codebook identically at every context, independent
context minimizers would reach `5159249/29296875`.
There are 176 forced opposite-switch witnesses.
Each selected witness comprises four uniquely minimizing belief/context cells.
At least one cell must incur its exact minimum positive regret; the report
stores 50 cell-disjoint witnesses, whose
regret inequalities can be summed. The resulting rational conditional bound is
`343597877/1875000000`.

**This is not a global Arm lower bound.** Other shared decoder weights can
change the codebook across contexts, and even a different constant codebook
is outside this conditional result. No case-A decision uses it.

## Attempt 2: finite coupled necessary-condition MILP/LP

Each model has 73804 bounded variables,
3692 binary variables, and 101556 rows.
Policy choices and word assignments are binary; assignment/policy product
variables are continuous but forced to the correct values at binary solutions.
The solver was bounded to 30.0
seconds per MILP case. It fits no neural parameters. An initial direct large
root-LP/MILP pipeline produced no output within 240 seconds and was stopped;
no result from that aborted run was accepted. The
replacement uses exact algebraic dual-price lifting and a small symmetric
slot-capacity LP for floating primal diagnostics; its time limit is at least
10 seconds. The slot-LP proposal lifts to the large root LP with uniform word
assignment and identical fractional policy mixtures in every context/word.

| S1 slope | S3 slope | Exact checked root-LP lower | MILP status |
|---|---|---|---|
| + | + | 5159249/29296875 | 1 |
| + | - | 20482177/117187500 | 1 |
| - | + | 5159249/29296875 | 1 |
| - | - | 20482177/117187500 | 1 |

The JSON stores sparse rational LP multipliers and the bounded-variable
reduced-cost correction. For `0<=x<=1`, the verifier computes, exactly,
`offset + b*lambda + sum min(0,c-A^T*lambda)`, with nonpositive multipliers
on upper-bound inequalities and free equality multipliers. The integer
multipliers are lifted algebraically from the old root certificate; they are
not floating MILP output. The box correction makes the verification robust
even to a merely approximate dual proposal.
Rebuilding the model and replaying those witnesses requires no solver.
The minimum over all four cases is a global lower bound for the original arm.
It did not improve the replayed prior certificate sufficiently to resolve the
gate. Floating MILP incumbent/dual bounds and 'optimal' labels are diagnostics,
**not certificates**. A relaxed incumbent is not an attainable deployed arm.

## Certificate and gate bookkeeping

The old positive/negative decoder certificates are replayed with exact integer
arithmetic, yielding `5159249/29296875`. Context symmetry
and the fixed global S3 slope sign transfer that valid one-context relaxation
bound to every context, hence their mean. This argument never constrains
the encoder's word to be context-invariant.

The previously certified shared upper is independently summed over all 256
histories using its published mapping and exact posterior costs. Mean individual
specialist losses (not their contributions divided by three) are
`9208873/31250000, 26612197/156250000, 1401823/3125000`.
The gate requires joint <= R10+0.01 **and strict** individual losses below
0.2, 0.18, 0.5. The published witness does not satisfy the full gate.

Run `python -B shared4_v1\coupled_lower.py --verify-only` to replay the
persisted exact witnesses without any LP/MILP solve. Full bounded investigation:
`python -B shared4_v1\coupled_lower.py --seconds 30`.
No inference about training learnability or Stage B follows from these results.
