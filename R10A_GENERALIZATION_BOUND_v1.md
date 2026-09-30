# R10A analytic encoder and heldout-context non-identifiability

## Scope

This is post-final analytic work, not a neural experiment or a change to frozen
artifacts. It leaves verdict B unchanged. `r10a_v1/encoder_witness.py` constructs
finite parameters of the actual `phase3b.models.Arm("R9", 56)` graph. No optimizer,
trained weights, arbitrary 81-row encoder lookup, or context-dependent trunk is
used. Construction certifies the best context-3 history assignment **for any
supplied eight-word decoder codebook**. The published codebooks in
`r10a_v1/decoder_bounds.json` are now bound to this construction and finite legal
decoder heads for both S3 orientations. With the independently certified
decoder bound, this establishes single-context deployed-R9 achievability at
`825479840/4687500000 = 5159249/29296875 = 0.17610236586666667`.

The implementation takes eight triples of local-bit action maps. Word numbers
are their supplied order. It returns a real R9 arm and a certificate, including
its exhaustive exact-rational 256-history mapping. This mapping is verification
data, never an inference input. The arm's decoder parameters are not installed
by the generic `construct`; its scope is the encoder. `construct_published`
also installs the heads and checks the immutable published mapping and exact
population risk. The generic fixture in the encoder tests is not claimed
optimal; a separate published-codebook test covers the certified optimum.

## A3: legal finite recurrent encoder construction

### The actual graph

R9 receives eight scheduled inputs
`[one_hot(t mod 4, 4), common_bit[t]]`, starting with hidden state zero.
Every recurrent update is

`h[t+1] = tanh(A input[t] + H h[t] + d)`.

There are 56 hidden units. Word logits are `W h[8] + U one_hot(context) + b`,
followed by lowest-index argmax. There is no trunk context input, multiplicative
context interaction, or decoder access to hidden state. The construction sets
all schedule-input weights and all `U` columns to zero.

### Why no 81-entry nonlinear lookup is needed

For two BSC(1/5) observations of an independent fair factor, its conditional
probability of one given count `n` is

`p(n) = (1/17, 1/2, 16/17)[n] = 1/17 + (15/34)n`.

Write the eight raw common bits as `x[0],...,x[7]`, and set
`p[j] = 1/17 + (15/34)(x[j] + x[j+4])`.

At context 3, S1 targets factor 3; S2 targets factor 0; S3 targets
`factor 1 XOR factor 2`, with its private BSC reading observing **factor 1**.
For a fixed local-bit decoder map, the conditional S1 and S2 risks are affine
in `p[3]` and `p[0]`. S3 risk is bilinear in `p[1], p[2]`: sum the four possible
truth pairs with their independent posterior masses and the two local readings.
This remains true for either S3 slope orientation, including inverse maps.

Therefore every word's joint conditional risk has the exact form

`C + sum_i a[i] x[i] + sum_(i,j) d[i,j] x[i]x[j]`,

where the only pairs are `(1,2), (1,6), (5,2), (5,6)`. The implementation obtains
these coefficients using rational expansion of the population loss formula,
not fitting or optimization. All conditional risks lie on a rational lattice
with denominator dividing `D = 867000`.

### Twelve active hidden units

Use gain `K=32`. Hidden units 0 through 7 form a signed-bit shift register:

* unit 0: `tanh(K(2 x[t]-1))`;
* unit `d=1,...,7`: `tanh(K h_previous[d-1])`.

At the final tick, unit `7-i` represents `2 x[i]-1`.

Units 8 through 11 represent the four required conjunctions. For a pair `(i,j)`,
their preactivation at the last tick is

`K(h_previous[6-i] + h_previous[6-j] - 1)`.

Both indices refer to the state after seven readings; all pair indices are at
most 6. The sign is positive exactly when both bits equal one. These units have
no outgoing recurrent connections, so their earlier values are immaterial.
The remaining 44 units and their connections are zero. Thus the construction
respects the deployed width and eight updates, including the first zero state.

### Exact-real finite-gain margin proof, including ties

For `z >= 0`, `1-tanh(z) <= 2 exp(-2z)`. Let `E=2 exp(-62)`.
The first register unit has signed error at most `2 exp(-64) < E`.
If a delayed signed bit has error at most E, the next preactivation magnitude
is at least `32(1-E) >= 31`; induction bounds every legitimate register bit's
error by E. A conjunction's magnitude is at least `32(1-2E) >= 31`, so its
signed error also is at most E. Empty early register positions do not enter the
final conjunctions. This is a real-number proof, not a floating-point heuristic.

Let L be the least common multiple of the exact polynomial coefficient
denominators. It divides D. The minimum strictly positive conditional-risk gap
is at least `1/L`; exhaustive rational gap enumeration is reported as an
additional check, not used to fit weights. Set `epsilon = 1/(16L)`.
Word w conceptually receives logit

`-conditional_risk(w) - w epsilon`.

This preserves every strict preference because the largest lexicographic
perturbation is `7/(16L) < 1/L`, and breaks all equal-risk comparisons in favor of
the lowest word. Multiply every logit by `16L`. The scaled ideal winning margin
is at least 1 (at least 9 for strict-risk preferences). Replace each
raw bit or conjunction in the polynomial by `(corresponding_hidden_unit+1)/2`.
If `B = max_w sum_nonconstant |coefficient_w|`, each scaled logit error is at most
`16L B E/2`. The constructor verifies `16L B E < 1`, giving a strictly positive
winning margin of at least `1 - 16L B E`. These are finite weights and
biases. Thus the actual tanh recurrence realizes the exact rational Bayes
assignment on **all 256 raw histories**, including ties.

Crucially, scaling makes **all output weights and biases integers**, not rounded
rational approximations. Thus the real-number proof applies to the actual
stored parameters. The constructor checks that each output row's absolute
weight-plus-bias sum is below `2^24`; all integers and ideal signed-feature
partial sums are then exactly float32-representable. Float32 runtime is checked
separately with actual `Arm.encode` and `Arm.write`, including tanh saturation.
The test fixtures pass all 256 comparisons. A runtime check for every published
codebook remains appropriate.

The four conjunction features are enough for the bilinear posterior product;
there is no need for 16 four-bit pattern indicators. The suggested 24-unit
pattern-indicator alternative is therefore unnecessary. The smaller 12-unit
construction also computes best assignments for the unrestricted R10
codebook, including its inverse S3 map. Tests verify that encoder alone against
the published unrestricted assignment; they do not certify its mixed-slope
codebook as realizable by the original R9 decoder.

### What the construction does not prove

It does not turn an arbitrary decoder table into a legal affine decoder.
For the published optimal affine-feasible eight-map codebooks, however, the
following explicit legal head construction closes that separate requirement:

* Positive binary heads have logit-1 minus logit-0 slope 2 on the local bit,
  with word intercepts -3, -1, 1 for maps 00, 01, 11 respectively.
* Negative binary heads have slope -2 with intercepts -1, 1, 3 for maps
  00, 10, 11 respectively.
* S2 has local-bit slopes `(0,4,2)` for actions `(0,1,2)`. Word intercept
  vectors are `(1,-4,0)` for map 02, `(-4,0,1)` for map 21, and
  `(-4,-4,1)` for map 22.

All decoder context offsets are zero, word intercepts use only the actual
eight one-hot word features, and both local-bit decisions have strict margins.
There is no extra decoder feature. `construct_published` selects the eight
policies in the published selected order and installs these heads.

The solver uses relative-factor count order `(0,1,2,3)`; the actual context-3
order is `(3,0,1,2)`. Rotating each common history's counts accordingly, the
analytic encoder exactly matches the published lowest-word 81-table on **all
256 histories**, for both positive and negative S3 variants. An independent
rational population sum uses raw-history mass `17/50` for either equal
observation pair and `4/25` for either particular unequal pair, independently
across four factors. It obtains exactly `825479840/4687500000`, not merely a
numerical approximation. The immutable decoder-bound JSON is not changed.

For both published variants, `L=86700`, score scale `16L=1387200`, coefficient
bound `B=20559/14450`, and maximum output-row absolute weight-plus-bias sum
`1717094 < 2^24`. The per-logit tanh error is below `2.339e-21`, so the real
winning margin is at least `1 - 4.678e-21`. The smallest positive unperturbed
risk gap is `29/14450`. No special tie exception or learned coefficient is used.

`r10a_v1/encoder_witness_weights.json` publishes the complete positive-variant
finite parameter set, with integer nonzero entries and zero fill for every
named parameter and declared shape, together with the mapping and margin/risk
certificate. `load_analytic_weights` restores it without a codebook solver.
The artifact is checked against deterministic analytic regeneration and
through the actual full forward graph for all 256 common histories and all
eight private-bit triples at context 3. It is not a trained checkpoint.

It also does **not** certify an all-context optimum. R9 logits share `W h`
across contexts and vary only by the additive offsets `U[:,c]`. In particular,
for each word pair, the history-dependent score difference is shared; only a
constant threshold can vary with context. Independent rotations of optimal
per-context encoders cannot silently be substituted for this graph. The
all-context oracle lower bound versus constructive R9 upper bound remains
unresolved here.

## A6: unseen context columns are independent free extensions

For training/evaluation restricted to contexts 0,1,2, R9's code-head context-3
column is `code.weight[:,59]`; consumer context-3 columns are
`heads[i].weight[:,11]`. The associated one-hot inputs are exactly zero.
Therefore all training-data loss derivatives with respect to these columns
are exactly zero, for every sample and every differentiable objective composed
of the training-context outputs. This includes stochastic-policy likelihood
objectives. The recurrent trunk has **no context column**. Weight decay or a
chosen initialization can select a value, but contributes no context-3 data
identification.

### Exact finite train-agreeing counterexample

`heldout_extension_pair()` returns two actual finite width-56 R9 parameter
sets. Both have zero trunk and word-feature decoder weights. At training
contexts they write word 0; S1 and S3 use local identity; S2 always abstains.
Their training outputs and distributions agree for every possible input, not
merely the observed training set.

Only unused columns differ:

* extension A keeps the code offsets zero and S2's abstention bias 1;
* extension B puts offset 2 on word 7's context-3 column and offset 2 on S2
  action 0's context-3 column.

At context 3, A writes word 0 and abstains; B writes word 7 and commits to
constant 0. Decoder word weights are zero, so the word change does not confound
the risk calculation. S1 local identity has unconditional risk 1/5.
S3 local identity has unconditional parity risk 1/2, because its other factor
is independent and fair. S2's risks are respectively 9/50 and 1/2. Consequently

* `R_A(context3) = (1/5 + 9/50 + 1/2)/3 = 22/75`;
* `R_B(context3) = (1/5 + 1/2 + 1/2)/3 = 2/5`;
* `R_B - R_A = 8/75 = 0.106666666666...`.

The paired changes are finite and produce strict action margins. This is an
exact non-identifiability witness, not a fitted performance claim or the full
ambiguity diameter. Neither member of this concrete zero-trunk pair is asserted
to be training-optimal. In particular, constant-0 versus constant-1 binary
predictions both have risk 1/2 under a fair prior; they would not demonstrate
the claimed risk gap. Nor can an additive context offset reverse a fixed
binary local-bit slope.

### The same 8/75 ambiguity at any training optimum

This is not limited to the concrete zero-trunk pair. Fix **any finite training
weights**, including any minimizer of an objective depending only on the
contexts-0..2 data likelihood or predictions. Leave the trained encoder
(including its unused context-3 offsets), S1, S3, and all observed-context
parameters exactly unchanged. For S2, define its context-free logits

`g[a,w,l] = bias[a] + word_weight[a,w] + local_weight[a] l`.

There are only `3 * 8 * 2` such values, so
`B = max_(a,w,l) |g[a,w,l]|` is finite. Choose any finite `M > 2B`.
Set S2's unused context-3 column to `(0,0,M)` in extension A and `(M,0,0)`
in extension B. At context 3, A strictly chooses abstention for every possible
encoder word and private bit; B strictly chooses commitment 0 for every word
and bit. These are additive offsets, not slope changes. The entire trained
encoder is unchanged.

On contexts 0,1,2, these columns still multiply zero, so both complete
extensions have exactly the original training outputs, likelihood, and data
objective. If the original weights are training-data optimal, both extensions
remain training-data optimal. This statement does not assume that the explicit
zero-trunk demonstration is itself optimal. A regularizer penalizing unseen
columns would add an extra prior/selection objective, not observational
identification.

For the deployed deterministic argmax policy, S1/S3 heldout risks agree between
these extensions, and the S2 marginal target is a fair factor regardless of
the trained encoder. Thus A has S2 risk 9/50, B has risk 1/2, and their heldout
**joint-risk gap is exactly 8/75 at every such training optimum**. This is a
lower bound on ambiguity, not an assertion of its exact diameter or either
extension's heldout optimality. The finite-offset argument is mathematical;
if serializing arbitrary extreme weights to a fixed floating-point dtype, the
offset must also be representable. It does not claim exact forced probabilities
under finite-logit stochastic softmax sampling; the exact gap is for the
deployed deterministic evaluator.

### Symmetry and identification

The stipulated population law is invariant under cyclic factor/context
rotation. That **known modeling assumption** justifies evaluating a rotated
policy in a larger abstract policy class. It neither ties the implemented
R9 parameters nor makes independently unused context-3 offsets observable.
The actual contexts-0..2 training likelihood is exactly invariant under all
changes to these unused columns, not just a finite symmetry group. Shared
parameters can be learned on visible contexts; absent context-offset columns
cannot. Identifiable training-context predictions do not identify the unseen
extension. A rotational tying rule would be additional architecture/prior
structure and is not present in the deployed model.

Neither the numerical all-four-context optimum nor shared four-context map
counts are solved by this encoder/non-identifiability report. Any separate
capacity enumeration or optimization certificate must be assessed on its own
scope; the one-context optimum and free-column argument do not supply them.

## Separate all-context bracket and remaining certification gap

The [additional exact context analysis](r10a_v1/context_bounds.json)
evaluates the published context-3-optimal legal Arm at every context.
It proves the following bracket for the **jointly shared deployed
four-context average optimum**:

```text
5159249/29296875 <= L_shared_four_context <= 8921732/29296875.
```

The lower endpoint follows because every individual-context policy
belongs to the one-context class already bounded. The upper endpoint
is one legal shared parameter vector, not four independent lookups.
Its context risks are `10220399/29296875`, `2030728/5859375`,
`2030728/5859375`, and `5159249/29296875`.
The unrestricted R10 all-context average is exactly
`5101889/29296875` by canonical rotation.

**The deployed coupled four-context optimum is not certified exactly.**
This bracket must not be collapsed to either endpoint. Accordingly the
full A6 oracle-all-context subtask remains blocked; the exact endpoint
decomposition and held-out non-identifiability proof remain valid.

An additional universal counterexample can force S1 and S3 to constants
using their free held-out offsets as well as the two S2 extensions above.
At any training-data optimum this gives exact held-out losses `59/150`
and `1/2`, without changing any training-context prediction. These are
achievable ambiguity witnesses, not the minimum and maximum of the
extension set. There is no unique "train-only context-3 optimum" selected
by the actual untied function class alone; selecting one requires an
extra rule/prior that cannot be silently added to this audit.

## Validation

`python -m pytest r10a_v1\test_encoder_witness.py -q`: **7 passed**.
Tests independently enumerate the posterior population risk, exhaust all 256
common histories through the actual R9 runtime (including negative S3 orientation
and identical-word ties), check unused-column gradients,
check exact training agreement and the rational heldout-risk counterexample,
and bind both published optimal codebooks to their actual R9 word assignments,
legal decoder maps, and exact population objective.
