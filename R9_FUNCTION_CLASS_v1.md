# R9 function class v1 — bounded analytic R10A A1/A2

Scope: exact deterministic decoder capacity and two decoder upgrades only.
No training, encoder optimization, certificate replacement, or full-program
claim is made. Existing Phase3b code and prior R10 results remain untouched.

## A1. Live decoder and tie convention

`phase3b/models.py`, `Arm.read()` concatenates `one_hot(shared, 8)`,
`one_hot(context, 4)`, and scalar `own_bit` and passes the resulting 13
features to an `nn.Linear` consumer head. Heads have respectively 2, 3, and 2
actions. Its bias can be absorbed into the word coefficients.

For a binary head, subtract action-zero logits from action-one logits:

    delta(m,c,l) = u_m + v_c + s*l.
    output = 1 iff delta > 0; otherwise output = 0.

For S2, logits can be written

    z_a(m,c,l) = b_am + d_ac + s_a*l.

The deterministic convention is lowest-index argmax. Thus a winner `w`
requires `z_w-z_a > 0` for `a<w` and `z_w-z_a >= 0` for `a>w`.
These are mathematical real/rational capacities, not counts of finite
floating-point parameter bit patterns.

### One context: complete codebook characterization

A word's map is the ordered pair `(output at bit 0, output at bit 1)`.
Binary heads can realize all four individual pairs. With `s>0`, an entire
codebook uses only `{00,01,11}`; with `s<0`, only `{00,10,11}`; with `s=0`,
only `{00,11}`. In particular, identity and inverse cannot occur at different
words of the **same head** simultaneously. Separate consumer heads have
independent slopes.

For M distinguishable words, the two orientation classes have `3^M` maps
each and overlap in `2^M` constant-pair maps. Therefore

    N_binary(M) = 2*3^M - 2^M,
    N_binary(8) = 12,866.

This counts all eight words jointly at **one context**, not four contexts.
A fixed nonnegative/nonpositive orientation alone has `3^8 = 6,561` maps.
For three independent consumer heads at one context, the decoder-only
Cartesian count is `N_binary(8)^2 * N_ternary(8)`; this makes no encoder or
task-performance claim.

For K actions, a changing pair `i -> j` requires `s_j > s_i`. Indeed, writing
`q = z_j(m,c,0)-z_i(m,c,0)`, the endpoint comparisons give `q <= 0` and
`q+s_j-s_i >= 0`, with at least one strict inequality because the two
different winners cannot both receive tie preference. Hence slopes strictly
increase along every change. Equal slopes allow only constant pairs between
those actions. Opposite transitions and directed cycles are impossible,
including cycles distributed across words or contexts.

Conversely, given any strict global slope order, all constant pairs and all
forward pairs are simultaneously realizable at one context: for a forward
pair choose its two intercepts to cross between bits 0 and 1, and place all
other actions sufficiently low at both endpoints. Word intercepts are
independent. A set of changing pairs is realizable iff its directed graph
is acyclic (extend its partial order to a total slope order).

S2 has 13 weak slope orders (ordered partitions of three actions). Their
pair alphabets are subsets of the six strict-order alphabets; therefore
they add no deterministic maps, including on tie boundaries. Each strict
alphabet contains three loops and three forward pairs, not all nine pairs.
The union of their M-fold Cartesian powers has exact inclusion/exclusion:

    N_ternary(M) = sum over nonempty subsets T of the six orders:
                  (-1)^(|T|+1) * |intersection of their pair alphabets|^M
                = 6*6^M - 6*5^M + 3^M, for M >= 1.
    N_ternary(8) = 7,740,507.

Every one-word ternary pair is individually possible, but choosing pairs
independently for all words would incorrectly give `9^8`. The polynomial
above accounts for codebook simultaneity. For example `(0,1),(1,2),(2,0)`
cannot be a three-word codebook.

### Four shared contexts: extra additive restrictions

All contexts share the **same word coefficients and slopes**. They are not
four independent heads. Global slope consistency is necessary but not
sufficient. At a fixed bit, the binary 2-word/2-context checkerboard

    context 0: word 0 -> 1, word 1 -> 0
    context 1: word 0 -> 0, word 1 -> 1

is impossible. It would imply `u_0 > u_1` from context 0 and `u_1 > u_0`
from context 1. Making each pair constant at both bits produces a
slope-consistent table which still fails shared-context feasibility. This
also obstructs a ternary head restricted to winners 0 and 1.

An exact necessary-and-sufficient characterization of any full table `y`
is feasibility of the following finite rational inequalities:

    (b_y,m - b_a,m) + (d_y,c - d_a,c) + (s_y - s_a)*l
        >= 1 if a < y(m,c,l), otherwise >= 0, for every a != y.

The strict inequalities may be replaced by margin 1 because there are
finitely many constraints and no inhomogeneous parameter constraints:
scale all coefficients by the reciprocal of the smallest positive margin.
Conversely margin 1 implies the strict inequalities. Feasibility over reals
equals feasibility over rationals for this rational polyhedron.

The implementation gauges action-zero logits and context-zero offsets to
zero, leaving `(K-1)*(M+C)` unrestricted variables, splits each into two
nonnegative variables, and runs exact Fraction phase-I simplex with Bland
pivots. It returns and verifies a rational witness, or reports infeasible.
There is no numerical tolerance, random weight search, or neural training.
This test retains additive word/context restrictions and the exact tie rule.

For clarity, define `U_K(L)` to be the union of all strict-slope-order pair
alphabets raised to power L. An exact full-context map-count formula is

    N_shared(K,M,C) =
        sum over P in U_K(M*C) of
        1[the above shared-context inequalities are feasible for reshape(P,C,M)].

`shared_context_count()` implements that finite sum without duplicate
tables. For K=2 its candidates number `2*3^(M*C)-2^(M*C)`; for K=3 its
candidates number `6*6^(M*C)-6*5^(M*C)+3^(M*C)`. These are **candidate
counts**, not final shared-context counts. With M=8,C=4 the sum is enormous
and has deliberately **not been evaluated**. No numeric full-four-context
binary or ternary count is claimed. Nor is `(3^8)^4` or the single-context
ternary count raised to four the shared-context capacity.

As a bounded independent check, the exact binary count for M=2,C=2 is 104,
strictly less than its 146 globally orientation-consistent candidates.
An exhaustive integer coefficient grid `u_0,u_1,v_1,s in [-4,4]` constructs
exactly those same 104 tables; exact feasibility checks every one of the
256 unrestricted tables and establishes completeness. For K=3,M=1,C=2,
independent context intercepts leave only the common slope-order condition,
giving 75 maps.

## A2. Minimal structural decoder upgrades

### D1: word × own-bit interaction

Add features `one_hot(word)*own_bit` to the existing word, context and bit
features. At one context each action now has

    z_a(m,l) = alpha_am + beta_am*l.

This realizes **every** deterministic table on eight words and two bits:
set endpoint logits to `I[y(m,l)=a]`, then use
`alpha_am = I[y(m,0)=a]`,
`beta_am = I[y(m,1)=a] - I[y(m,0)=a]`.
The desired action has unique logit 1 and all others logit 0. Single-context
capacities become `4^8 = 65,536` for binary and `9^8 = 43,046,721` for
ternary. D1 is a minimal *structural kind* of change (word-dependent slopes),
not a claim that this redundant feature list has the minimum possible
dimension. One word×bit column may be omitted when the scalar bit remains,
since the word×bit columns sum to that scalar.

**Qualification:** shared D1 with only additive context features still has
`z_a(m,c,l)=alpha_am+beta_am*l+d_ac`. It is not universal across contexts:
the checkerboard above at bit 0 remains impossible. Arbitrary full-context
tables require word/context interaction **and** its bit-dependent version,
e.g. `one_hot(context,word)` and `one_hot(context,word)*own_bit`. Adding
word×context intercepts alone does not remove the common per-word slope
restriction across contexts. The `full_context=True` D1 feature mode includes
both interactions and is universal by the same endpoint construction.

### D2: fixed lookup-equivalent hidden representation

For one context, use 16 fixed ReLU units:

    h_(m,0) = ReLU(one_hot(word)_m - own_bit),
    h_(m,1) = ReLU(one_hot(word)_m + own_bit - 1).

On legal binary inputs these are exactly a one-hot code for `(word,bit)`.
A linear head assigning logit 1 at the desired class and 0 elsewhere is
therefore lookup-equivalent, without fitting or training hidden weights.
The minimal nonredundant D1 basis and these D2 units span the same 16
functions on the single-context legal input domain.

Again, adding context one-hots only additively to these 16 units is not
universal for arbitrary context-varying maps. Full context lookup needs 64
units indexed by `(c,m,l)`, e.g.

    h_(c,m,0) = ReLU(one_hot(word)_m + one_hot(context)_c - own_bit - 1),
    h_(c,m,1) = ReLU(one_hot(word)_m + one_hot(context)_c + own_bit - 2).

These are exact one-hot indicators on legal inputs. Full-context D1 and D2
therefore realize all `K^(2*8*4)` maps for a K-action head. These are proposed
decoder classes, **not** the live/frozen R9 decoder or previously certified
results. No performance, retraining, or new certificate follows from capacity.

## Reproduction

    python -m r10a_v1.decoder_capacity
    python -m unittest r10a_v1.test_decoder_capacity

Tests cover exact single-context counting, weak slope orders, all individual
pairs versus joint codebooks, cycle and shared-context obstructions, rational
feasibility witnesses, lowest-index ties, the exhaustive small shared count,
and constructive D1/D2 lookup realizations. Full M=8,C=4 numeric mapcounts
remain uncomputed; the finite exact algorithm/formula above is the bounded
A1 result for those dimensions.
