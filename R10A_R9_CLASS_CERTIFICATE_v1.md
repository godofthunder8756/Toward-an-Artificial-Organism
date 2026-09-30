# R10A: exact deployed R9-class endpoint optimum

## Certified result

For the **non-clone, width-56 deployed R9 functional class**, evaluated at
the frozen context-3 population endpoint:

**L_R9_CLASS = 5159249/29296875 = 0.17610236586666667.**

The constructive upper and certified lower numerators both equal
`825479840`, with denominator `4687500000`. This is not a decoder-only
bound mislabeled as a neural-family optimum. It includes an explicit legal
tanh recurrent encoder and affine action heads.

The [machine certificate](r10a_v1/class_certificate.json) publishes the
eight decoder maps, rational head coefficients, all 256 history-to-word
assignments, finite-gain encoder construction, exact margin information,
loss decomposition, and source hashes.

## Lower bound

Allow the encoder to choose any eight-symbol partition of the 81 beliefs.
This relaxes the actual recurrent encoder and therefore gives a lower
bound, not automatically an achievable value.

Each binary S3 affine head has one global local-bit slope. Its codebook
uses `{00,01,11}` or `{00,10,11}`; zero slope is contained in both.
Both orientations are solved separately. To lower-bound each, allow
unrestricted S1 and S2 two-bit maps. Exact pointwise dominance reduces
them to S1 `{00,01,11}` and S2 `{02,21,22}`. Thus each orientation has
27 retained joint maps. Every omitted legal map has a no-worse retained
replacement at every positive-support belief.

Both orientation optima have exact numerator `825479840`. Each is
certified by a **single exact-integer Lagrangian root bound**. The full
cost table, chosen eight maps and integer row prices are in
[decoder_bounds.json](r10a_v1/decoder_bounds.json). The
[solver-free checker](r10a_v1/verify_bounds.py) reconstructs the rational
population risks and exact dominance/bounds. Floating MILP only proposes
the codebook and row prices; its status is not the certificate.

The lower bound covers all deployed head slopes and all actual encoders,
including order-sensitive histories. Stochastic codes cannot improve
their minimum expected loss for fixed stateless decoder functions.

## Constructive upper: actual recurrent encoder, not lookup bypass

The [analytic encoder constructor](r10a_v1/encoder_witness.py) instantiates
`Arm("R9",56)` and sets finite, nonlearned weights. It uses only **12**
of the 56 hidden coordinates:

* eight signed-bit shift-register units;
* four conjunction units for the four cross-products between the two
  readings of global factors 1 and 2.

All other weights can be zero. This is the same recurrent topology,
input access, eight-symbol output layer and parameter dimensions as the
deployed model; it adds no input or hidden unit.

The posterior is affine in a factor's count:
`q(n) = 1/17 + (15/34)n`. Conditional specialist risks are therefore
linear in the relevant raw readings, except parity which additionally
needs four pairwise products. Each word's exact expected loss is a
quadratic polynomial in those legal observations. Its negative,
plus a rational lowest-word tie perturbation, is implemented by the
existing linear eight-logit output layer.

Gain 32 makes every matured signed bit and conjunction uniformly close
to its ideal value. A rational tail bound and a strict selector margin
prove the ideal-real decision map. Integer-scaled selector weights and
all possible partial dot-product sums fit below `2^24`. Exhaustive
execution also verifies the actual float32 implementation on every
common history and private-bit triple. No neural optimizer is used.

The eight selected head maps are jointly feasible: S1/S3 use one
positive slope and S2 uses slopes ordered `s0 < s2 < s1`. The
certificate publishes independently checked rational coefficients.
The heads can repeat this same table across contexts, preserving actual
parameter sharing; only context 3 is claimed optimal.

## Independent replay

[verify_class.py](r10a_v1/verify_class.py) verifies the lower-bound
certificate, reconstructs the actual deployed Arm, installs the
published rational heads, and directly integrates over:

* all 256 common histories;
* all 16 truths with exact prior/common likelihoods;
* both sensor outcomes for each consumer;
* all eight realized private-bit triples for runtime isolation checks.

It obtains the same exact numerator without using the optimizer's
aggregated-count upper-risk calculation.

```powershell
python r10a_v1\verify_class.py r10a_v1\class_certificate.json
python r10a_v1\verify_bounds.py r10a_v1\decoder_bounds.json
```

The [independent audit](r10a_v1/independent_audit.json) is separate from
the constructor and published checkers. It **passed** the final
context-3 class, rational finite-gain witness, minimal decoder ladder
and all-context bracket checks; all **24** analytic tests passed.
The class certificate SHA-256 is
`8b2a52b83833666dfb119799b1d970d540db3ff44caacedfec6f9362c0ec4ece`.
The independent audit SHA-256 is
`1fb0ebf4a2fbbe74f9685451b5eb514f0f7462b21a982fd7752e9c01486e61d9`.

## Scope boundary

This answers the original **held-out-context endpoint** question. It is
not a certificate for the jointly optimal four-context average with a
single shared encoder/head parameter vector. Shared context offsets
impose additional restrictions; four independently rotated optimum
tables cannot silently be treated as a legal deployed all-context model.
See the [generalization analysis](R10A_GENERALIZATION_BOUND_v1.md).
Mathematical decision-map counts concern real affine coefficients,
not the number of floating-point parameter bit patterns.

No frozen primary/R10 file is changed and no model is retrained.
