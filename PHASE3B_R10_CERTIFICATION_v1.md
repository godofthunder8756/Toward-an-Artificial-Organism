---
description: Exact EXTERNAL eight-symbol coding optimum and frozen R9 learning gap
ms.date: 2026-09-29
---

# Phase III-B R10: optimal unrestricted eight-symbol coding

## Disposition

**No neural training was performed. Phase III-B verdict B is unchanged.**
This is the separately authorized post-final execution of the optional
R10 analytic EXTERNAL control, not an additional primary rival, a new
training regime, or a Phase IV admission.

The exact optimal population joint loss with eight unrestricted symbols is
**5101889/29296875 = 0.17414447786666667**. The full-information Bayes
floor is **96/625 = 0.15360000000000000**. Exhaustively evaluating the
16 already-trained R9 checkpoints gives population mean
**2003/6000 = 0.33383333333333333**.

| Population quantity | Joint loss |
| --- | ---: |
| Full-information Bayes floor, no wire constraint | 0.15360000 |
| R10 certified optimal eight-symbol code | 0.17414448 |
| Learned R9, exact mean over frozen final checkpoints | 0.33383333 |
| Capacity penalty: R10 minus full-information floor | 0.02054448 |
| Noncapacity gap: learned R9 minus R10 | 0.15968886 |

Of R9's excess above the full-information floor, **88.6012%** lies above
the optimal eight-symbol risk; **11.3988%** is the unavoidable eight-symbol
capacity penalty for this decision problem. These are differences of
population risks, not an attribution of neural training mechanisms.

**Decision: retain the eight-symbol wire; diagnose representation/readout
and learning/credit assignment, not increased information capacity.**
Capacity is a real, certified constraint, but it cannot explain the much
larger learned gap. The oracle receives exact sufficient statistics and
unconstrained tabular decoders: this comparison does not isolate
optimization from representation restrictions, inductive bias, finite
samples, or held-out-context generalization.

There is a concrete readout restriction, not merely a generic caveat:
R9's binary S3 head is affine in the word one-hot vector, context one-hot
vector, and scalar local bit. Its local-bit logit slope has one sign across
all words. R10's published code uses both identity `(0,1)` at symbol 2 and
inverse `(1,0)` at symbol 5, each on positive-support beliefs. A single
affine head cannot implement both. The independent audit confirms this
restriction in all 16 frozen checkpoints. **This optimal table is not
representable by frozen R9's readout**, although the eight-symbol channel
can carry it.

No optimum restricted to that neural readout class was certified, nor
was the expressivity-only part of the risk gap quantified. Consequently
the 88.6% noncapacity fraction must not be relabeled as 88.6% optimizer
failure. The first nontraining diagnostic priority is separating readout
expressivity from learning/credit assignment and context generalization.
Nothing here establishes cheap learnability within the original neural
parameter, compute, sample, or search caps. No new learning experiment is
started or authorized by this report.

## Scope and exact finite reduction

The [frozen protocol](ACI_PHASE3B_PROTOCOL_v1.md) defines R10 as an
evaluator-only arbitrary eight-symbol code using the four-counter belief,
public context, all three action maps, both values of each private sensor,
and the actual losses. The encoder cannot see any private local sensor,
latent truth, or evaluator reward.

For each factor, the two common readings yield count `n` in `{0,1,2}`.
Its posterior is respectively `(1/17, 1/2, 16/17)`, and its marginal
count probability is `(17/50, 16/50, 17/50)`. The four factors are
independent, giving **81 positive-support belief states**.

Each symbol specifies one two-local-bit response map for each specialist:
four binary maps for S1, nine ternary maps for S2, and four binary maps
for S3, hence **144 possible joint decoder maps**. S2 action `2` is
abstention at cost `0.18`; S1/S3 errors and S2 wrong commitments cost one.
Joint risk averages the three specialist losses.

For every belief/map pair, the encoder's risk integrates out the local
readings before selecting a symbol. The proposer obtains integer weighted
risks by enumerating all 16 truths and each consumer's two sensor values.
The solver-free verifier independently reconstructs them from exact
posterior fractions. Both use denominator **4,687,500,000** for population
joint loss. No sample estimate enters the optimization.

Pointwise component dominance leaves **36 maps**. The verifier checks
that every one of the 144 original maps has a retained replacement with
no higher cost at every belief, rather than trusting the pruning code.
Replacing dominated symbols cannot increase risk or require more symbols.

The encoder can select a new symbol for each public context. Rotating the
four counts into canonical target order `(c,c+1,c+2,c+3) mod 4` gives
identical population problems at all four decision ticks. The heads are
stateless, receive only their own current sensor, and cannot revise settled
actions; there is no additional common observation or revealed delayed
feedback between these decisions. Costs are additive. Thus the certified
per-context joint mean is also the four-tick average; its four-tick sum
is `4 * 5101889/29296875`. This does not assume an extra cross-tick channel.

Order within histories sharing the same counts contains no additional
information about truth. A history-dependent encoder induces a stochastic
code on these sufficient statistics, and cannot outperform its
minimum-risk deterministic assignment for fixed heads. More generally,
with all other policies fixed, expected loss is linear in each encoder or
decoder distribution; deterministic extreme points suffice for a global
optimum. Shared randomization is a mixture of deterministic policies and
cannot improve their minimum. The finite reduction therefore covers
unrestricted randomized as well as deterministic eight-symbol coding
under the specified inputs.

## Published optimal codebook

Pairs list actions for local sensor values `(0,1)`. Symbol numbers are
arbitrary labels, not truthful source addresses.

| Symbol | S1 map | S2 map | S3 map |
| ---: | --- | --- | --- |
| 0 | `(0,0)` | `(0,2)` | `(0,0)` |
| 1 | `(0,0)` | `(2,1)` | `(1,1)` |
| 2 | `(0,1)` | `(0,2)` | `(0,1)` |
| 3 | `(0,1)` | `(0,2)` | `(1,1)` |
| 4 | `(0,1)` | `(2,1)` | `(0,0)` |
| 5 | `(0,1)` | `(2,1)` | `(1,0)` |
| 6 | `(1,1)` | `(0,2)` | `(0,0)` |
| 7 | `(1,1)` | `(2,1)` | `(1,1)` |

The [certificate](phase3b_r10_v1/certificate.json) publishes all retained
maps, these eight selections, the ordered 81 beliefs, and the encoder's
81-word lookup table. The encoder minimizes exact integrated conditional
risk over these eight symbols, breaking ties by lowest symbol. It never
selects using the realized private bits or final outcomes. The certificate
SHA-256 is
`c7aba24a1e0ef6ed1d30c5c1900111e6a30e0509abfce53a03d9f79a5be2d510`.
This is one optimal codebook, not a claim of uniqueness.

## Exact optimality certificate, not floating solver status

The [proposer](phase3b_r10_v1/r10.py) uses SciPy/HiGHS MILP only to propose
a feasible codebook (installed SciPy version `1.15.3`). It then builds a
complete binary branch certificate
on retained decoder availability. The proof has **11 nodes and six leaves**.
All final leaf bounds and the feasible upper bound are checked with exact
integers by the independent [solver-free verifier](phase3b_r10_v1/verify.py).
There is **zero unresolved optimality gap**.

Subtract each belief row's minimum and divide remaining costs by five.
The exact baseline numerator is `720000000`; the optimal integer regret
is `19260448`. Thus `720000000 + 5 * 19260448 = 816302240`, giving the
stated fraction after division by `4687500000`.

For any integer row prices `alpha[i]` at scale `S=1000000`, define
`B[j] = sum_i max(0, alpha[i] - S * regret[i,j])`. At a branch with
included decoder set `I`, excluded set `E`, and remaining decoder set `F`,
the following is a valid lower bound in scaled regret units:

```text
sum_i alpha[i] - sum_{j in I} B[j]
              - sum of the largest (8 - |I|) values B[j] for j in F
```

This follows directly from assignment to available facilities and the
at-most-eight cardinality constraint. Any proposed row prices are valid:
there is no numerical dual-feasibility test to trust. Each certified leaf
has lower bound strictly above `(19260448 - 1) * S`, excluding every better
integer objective. Every branch checks both availability values of a
previously free policy. The verifier rejects incomplete, repeated, cyclic,
or unreachable nodes and invalid dominance coverage. The achievable upper
bound and global lower bound coincide exactly.

## Executed scoring and frozen R9 comparison

The [evaluation](phase3b_r10_v1/evaluation/evaluation.json) includes
16 new fixed-code R10 raw traces on the original `20000 + seed` streams
for seeds `1000..1015`, with **no tuning to those streams**.

| Same-stream held-out context-3 result | Mean joint loss |
| --- | ---: |
| Original independently trained R9 | 0.33244059 |
| Fixed certified R10 code | 0.17277913 |
| Paired R9 minus R10 | 0.15966146 |

R10 is strictly better on all 16 streams. This descriptive post-final
oracle comparison is not a new primary test. The empirical R10 mean
differs from its population optimum because the streams are finite.
Its empirical specialist losses are S1 `0.13237000`, S2 `0.10247437`,
S3 `0.28349304`; S2 is better than always abstaining and S3 is better than
chance. These summaries describe this optimal code, not unique per-head
optima or a new learned result.

The same code's **exact population** specialist losses are:

| Specialist | Exact loss | Decimal loss |
| --- | --- | ---: |
| S1 | `259531/1953125` | 0.1328798720 |
| S2 | `1019884/9765625` | 0.1044361216 |
| S3 | `111374/390625` | 0.2851174400 |

Their arithmetic mean equals the certified joint optimum exactly. Thus
useful S1 control, nontrivial S2 commitment, and better-than-chance S3
parity are achievable together on the existing three-bit wire, without
claiming perfect decisions or simultaneous full-information Bayes maps.

For the population R9 comparison, every frozen checkpoint was evaluated
without gradients on all **256 common histories and eight private-bit
triples at all four contexts**. The population risk reported above is
context 3, matching the frozen endpoint. Actual common-history
probabilities, both values of each local sensor, and the true loss ledger
are integrated exactly. Within-count history multiplicities are removed
before summing; R9 is not assumed to use counts only. Message invariance
to private bits and each head's isolation from the other local bits are
checked exhaustively. Each R9 checkpoint also replays its original raw
actions, words and losses exactly on the original evaluation stream.

## Preservation, audit and replay

The evaluation records and rechecks hashes of **all 404 frozen final
files**, the primary source inventory, dependencies, and
[verdict B](PHASE3B_VERDICT_v1.md). The verdict file remains byte-identical
with SHA-256
`a98940518d8fb936a7f44108bb78fa3e4a60ae437460ce133b36aa248fe39d4d`.
No original result, checkpoint, selection, approval, endpoint or primary
gate was rewritten.

Execution HEAD was `3a7605233436479084fa178dc8b3902ac2bad927`. The
subsequent archive/documentation commit made the supplement's HEAD
`276bad6`; this supplement explicitly reports the HEAD mismatch. Frozen
source/dependency bytes still match. It does not alter or bypass the old
freeze verifier or claim a new exact-HEAD primary execution.

The [independent R10 audit](phase3b_r10_v1/independent_audit.json) records
the separate mathematical and replay attestation, including coverage of
all **30,260,340** eight-policy subsets of the dominance-reduced family.
It certified the unrestricted EXTERNAL optimum and separately verified
the neural readout restriction. Its SHA-256 is
`690fe60c937e23b53f6a5b9dbad23a4797128e1c24aaa09e8ff0a8bdb401b58f`.
The original primary audit remains separate and unchanged.

From the repository root:

```powershell
python phase3b_r10_v1\verify.py phase3b_r10_v1\certificate.json
python -m pytest phase3b_r10_v1\test_r10.py -q
```

The eight tests cover independent exact-risk agreement, the objective
certificate, five tamper cases, local-bit isolation, and context rotation.
Proposer and scoring commands are in the
[supplement README](phase3b_r10_v1/README.md); they require fresh output
paths and never invoke training.

The next diagnostic target is the gap to this fixed, competent finite code:
readout expressivity, representation learning, credit assignment and
generalization should be separated before considering more channel
capacity. That is a research disposition, not authorization to start
another neural program. Phase III-B remains **B**, and Phase IV remains
**unauthorized**.
