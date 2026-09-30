# R10A: minimal decoder expressivity ladder

These are certified **context-3** optima using the legal existing
width-56 encoder. All constructions are analytic, not fitted.

| Level | Decoder class | Exact joint optimum |
| --- | --- | --- |
| D0 | Original three affine shared heads | `5159249/29296875` |
| D1 | Original heads plus one S3 word-bit cross feature | `5101889/29296875` |
| D2 | Original heads plus one S3 ReLU interaction unit | `5101889/29296875` |
| D3 | Unrestricted own-bit maps, as in R10 | `5101889/29296875` |

Each improvement is upper-bounded by a constructive legal policy and
lower-bounded by unrestricted R10. D0 has its separate exact class
certificate. Thus no floating solver claim is needed for this ladder.

## Functional minimality

For the new optimal codebook, only symbol 5 requires S3 inversion.
The S3 logit difference can use one global positive bit slope,
word-specific intercepts, and one additional feature:

`indicator(message == 5) * local_bit`, with coefficient `-2`.

Word 5 changes slope from `+1` to `-1`; other words retain their slope.
Interceptions are `-2` for constant zero, `1` for constant one, `-1/2`
for identity, and `1/2` for inverse. S1 and S2 are untouched.
At least one interaction is necessary because the original class has a
strictly larger certified optimum. **One scalar feature is sufficient
and dimension-minimal for closing this task's class penalty.**

D2 implements exactly the same feature using one hidden unit:

`ReLU(indicator(message == 5) + local_bit - 1)`.

It equals the conjunction on legal discrete inputs. This is not a claim
that a one-unit decoder realizes every possible lookup table.

For arbitrary single-context per-message maps, a general extension uses
word-bit cross features (seven independent contrasts suffice if the
existing scalar bit is retained). A lookup-equivalent tiny nonlinear
construction uses separate message/bit conjunction indicators. General
four-context tables additionally require context-dependent interactions;
neither D1 nor this one-unit D2 removes the encoder's additive context
restriction.

The [machine ladder certificate](r10a_v1/ladder_certificate.json) and
[constructive checker](r10a_v1/ladder.py) publish the optimal codebook,
encoder margins, selected inverse symbol, and exhaustive two-bit checks.
The [function-class report](R9_FUNCTION_CLASS_v1.md) distinguishes
task-minimal correction from universal decoder capacity.

The correction closes a **0.001957888** joint-loss expressivity penalty,
not the much larger within-class learned shortfall. Its existence does
not justify changing and training the decoder now.
