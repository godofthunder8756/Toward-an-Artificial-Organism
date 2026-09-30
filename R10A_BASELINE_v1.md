# R10A baseline: reconciled live evidence

Starting HEAD: `94f9ace` (the committed R10 supplement), not the original
Phase III-B execution HEAD `3a76052`. The working tree was clean.
This additive analytic program prohibits neural training and preserves
all original primary and R10 artifacts.

The frozen source inventory, all 404 primary final files, verdict B,
R10 scripts, and solver-free R10 certificate were checked against recorded
hashes. R9's selected final configuration is width 56, learning rate 0.001,
4,058 trainable parameters. There are 16 frozen final checkpoints.

## Actual deployed functions

The non-clone R9 uses a width-56 tanh recurrent trunk:
`h[t+1] = tanh(A x[t] + B h[t] + b)`, `h[0]=0`, over eight
inputs consisting of the public four-port one-hot schedule and one
common sensor bit. Context and private local bits never enter this trunk.
It is not an unrestricted belief lookup table.

Its eight encoder logits are `W h[8] + U one_hot(c) + v`.
Lowest-index argmax selects one message in `{0,...,7}`. Encoder parameters
are shared across all four contexts; context enters additively only.

Each stateless specialist receives the same eight-way one-hot message,
its own scalar current local bit, and a four-way context one-hot.
Its action logits are a single affine map of these 13 features.
The three specialists have separate parameters but each specialist shares
parameters across messages and contexts. Lowest-index argmax resolves ties.
There are no message-bit, message-context, or context-bit interaction
features.

| Specialist | Actions | Sensor | Target and loss |
| --- | --- | --- | --- |
| S1 | 0,1 | BSC(1/5) of factor c | Wrong action costs 1 |
| S2 | 0,1,2 | BSC(1/5) of factor c+1 | Wrong bet costs 1; action 2 abstains for 0.18 |
| S3 | 0,1 | BSC(1/5) of factor c+2 | Wrong parity of c+2,c+3 costs 1 |

All factor indices are modulo four. Contexts 0-2 were used for learning;
context 3 is the frozen primary endpoint. There is no common observation
or exposed delayed feedback during the four decision ticks.

## Oracle versus deployed family

R10 may use an arbitrary table from exact four-count belief and public
context to eight symbols, with arbitrary own-local-bit decoder maps for
each symbol and context. R9 has both the recurrent/additive encoder
restriction and affine/additive head restriction. A decoder-only oracle
cannot automatically be called the deployed R9-class optimum.

Reconciled population quantities:

* Bayes: `96/625`.
* R10: `5101889/29296875`.
* Frozen learned R9 mean at context 3: `2003/6000`.

The R10 fixed-code final-stream mean is 0.1727791341; original learned
R9 final-stream mean is 0.3324405924. These empirical means are not the
population quantities above.

References: [primary implementation](phase3b/models.py),
[frozen verdict](PHASE3B_VERDICT_v1.md),
[R10 certificate](phase3b_r10_v1/certificate.json),
[R10 exact verifier](phase3b_r10_v1/verify.py),
[R10 evaluator](phase3b_r10_v1/evaluate.py),
[R10 independent audit](phase3b_r10_v1/independent_audit.json).

The central R10A optimum is explicitly the **context-3 population
endpoint** for the deployed width-56 R9 family. The all-context
representability/generalization question is reported separately, and
will not be substituted for that endpoint.
