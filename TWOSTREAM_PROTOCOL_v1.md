# Two-stream world-admission protocol v1

**ANALYTIC CERTIFICATE. Freeze this file and the hashed source before the
enumeration. One run. No retuning.**

Repo owner Aidan Ahern approved this bounded certificate on 2026-10-20 under a
standing authorization covering analytic work. The approval covers the
enumeration specified here. It does not authorize neural training, a
solver or MILP, organism work, a new architecture, an edit to any existing
frozen file, protocol, result, errata, ledger, or kanban, or a mean-field arm.

Classification: analytic. Apparatus: exact rational enumeration and the proofs
below. This file is additive. `ACI_NEXT_EXPERIMENT_DECISION_v1.md` stays as
written.

## What is frozen

The generator, the horizon, the four numerical signatures, and the five arms
are the decision document's. This protocol resolves conventions the decision
document left open, reclassifies signature (iv) as an identity check, and adds
the reachable-alias audit. No numerical threshold moves.

Consultation #2 is followed where it corrects earlier drafts:

- (ii) and (iii) are not equivalent. The mass condition implies an XOR Brier
  excess of at least `1/1600`, which is below `1/1000`. A rare large
  covariance can meet (ii) and miss (iii).
- An observation can amplify a covariance that is already present. It cannot
  create covariance from a product belief.
- Alias search is exhaustive. Only a symmetry-generated collision requires a
  zero marginal mean. Unrelated histories may collide with both means nonzero.
- The audit covers terminal aliases and same-phase prefix aliases.
- No autonomous mean-field arm is added.

## Admission questions

1. **Q1.** Bounded prerequisite under C2: does this temporally distributed
   two-stream world have identifiable first-order history and product-readout
   consequences, and does the ordinary joint chart already carry them?
2. **Q2.** One question: on this frozen world, is the history-using joint
   forecast strictly better than a current-observation filter, does the
   product of the exact terminal marginals lose at least the frozen XOR Brier
   and forecast-shift mass, and does `(P(X=1), P(Y=1), Cov(X,Y))` reproduce
   the joint filter?
3. **Q3.** Falsifier of admission: gate (i), (ii), or (iii) misses its frozen
   threshold while the implementation checks hold. That verdict is REJECT for
   this world. Replay, normalization, simplex, chart, or symmetry failure is
   UNRESOLVED, which falsifies the run and does not falsify a broader claim.
4. **Q4.** Strongest same-information rival: the three-number chart, which is
   the four-state posterior in other coordinates. The product readout is a
   strictly weaker functional of those marginals. The current-only arm is the
   history-free rival. The direct-history table matches the joint forecasts
   and is charged for 256 stored entries. No mean-field arm is in this
   protocol.
5. **Q5.** The A6 effort closed UNRESOLVED. The decision document names this
   world as the next identifiable question and states that its enumeration has
   not been run. The sign of (i) and the identity (iv) are proved here; (ii)
   and (iii) are functionals of the terminal covariance and remain to be
   evaluated once.
6. **Q6.** After ADMIT, a later human gate may consider whether a learning
   protocol is worth designing. This certificate does not design or run one.
   The alias row selects a pre-written sentence inside the claim ceiling.
7. **Q7.** After REJECT, this world is not an admitted benchmark. A successor
   world needs a new written rationale and a new human gate. Noise and horizon
   stay put. After UNRESOLVED, the record is an errata plus an additive fix
   and a new freeze; the thresholds stay put.
8. **Q8.** Analytic proof plus one exact enumeration of the 256 histories.
   No neural model, organism, or solver.
9. **Q9.** Benchmark admission for a supplied first-order world. Substrate
   competence of the ordinary chart, not organizational cognition and not a
   robustness trial of a learner.
10. **Q10.** Ceiling stated in the claim-ceiling section.
11. **Q11.** Prerequisite material under C2, with a rival anchor recorded
    beside C3. No layer is promoted. C4 and above are untouched.
12. **Q12.** The O-axis is untouched. The generator is supplied to the
    evaluator. O3 is not advanced.
13. **Q13.** ADMIT: this world can be used as an admitted analytic benchmark
    with an ordinary sufficient state, which removes a reason to posit extra
    integration machinery for these forecasts. REJECT: this world is dropped
    as a benchmark, and joint information is not thereby unnecessary in
    general. UNRESOLVED: no belief change. Alias outcome A1 adds only the
    pre-written Q-EXIST sentence about exact marginals in this world.

## Frozen world

Hidden state `(X, Y)` is a pair of bits. The initial law is uniform on the
four states. Neither the latent state nor the model parameters are inputs to
a future learner. This stage has no learner. The evaluator uses the generator
for the oracles and for scoring.

Each transition draws independent `C ~ Bernoulli(1/5)`, `Dx ~ Bernoulli(1/50)`,
and `Dy ~ Bernoulli(1/40)`, then sets

```text
X' = X xor C xor Dx
Y' = Y xor C xor Dy
```

Eight readings alternate X and Y. Each reading is an independent BSC with
crossover `1/5`. The order, which the decision document left open, is frozen
as X, Y, X, Y, X, Y, X, Y. Reading 1 observes X. Reading 8 observes Y.

Timing, frozen from the decision document:

- The stage-k belief is the posterior after reading k, before any transition.
- For k < 8 the transition is applied after that belief, and the result is
  the prior for reading k+1.
- After reading 8 there is no transition. Terminal queries use the stage-8
  belief.
- Queries predict `X`, `Y`, and `XOR(X, Y)` from the same history. Forecasts
  are first-order world probabilities.

State index `s = X + 2Y`: `0 = (0,0)`, `1 = (1,0)`, `2 = (0,1)`, `3 = (1,1)`.
A history integer stores reading 1 in the least significant bit.

Derived constants used in the proofs:

```text
a   = 1 - 2/5   = 3/5
b_x = 1 - 2/50  = 24/25
b_y = 1 - 2/40  = 19/20
eta = 1 - 2/5   = 3/5
1 - a^2 = 16/25
e(1 - e) = 4/25
```

## Coordinates

Write `m_x = P(X=1)`, `m_y = P(Y=1)`, and `c = Cov(X,Y) = p_11 - m_x m_y`.
Spins `μ_x = 1 - 2 m_x`, `μ_y = 1 - 2 m_y`, and `κ = 4c`. The inverse chart is

```text
p11 = m_x m_y + c
p10 = m_x (1 - m_y) - c
p01 = (1 - m_x) m_y - c
p00 = (1 - m_x)(1 - m_y) + c
```

These four numbers sum to 1 and recover the marginals and the covariance.
They are nonnegative exactly on the Fréchet interval

```text
max(-m_x m_y, -(1-m_x)(1-m_y)) ≤ c ≤ min(m_x(1-m_y), (1-m_x)m_y)
```

So `(m_x, m_y, c)` is a bijection from the 3-simplex to that set. The chart
has three numbers because the joint distribution has three degrees of freedom.

Observation of X with bit `o ∈ {0,1}`, writing `P(O=1) = e + eta m_x`:

```text
o = 1:  m_x' = (1-e) m_x / P1,   m_y' = m_y + eta c / P1,   c' = e(1-e) c / P1^2
o = 0:  m_x' = e m_x / P0,       m_y' = m_y - eta c / P0,   c' = e(1-e) c / P0^2
```

Observation of Y swaps the two marginals. In both cases `c'` is proportional
to `c`. A product belief stays a product. For a marginal in `[0,1]` the
predictive probability lies in `[e, 1-e] = [1/5, 4/5]`, so the rescaling
factor `e(1-e)/P(o)^2` lies in `[1/4, 4]`. An observation may therefore
amplify an existing covariance by as much as 4, and it may shrink it to a
quarter. It contributes nothing when `c = 0`.

Transition:

```text
m_x' = 1/2 + a b_x (m_x - 1/2)
m_y' = 1/2 + a b_y (m_y - 1/2)
c'   = b_x b_y [ c + (1 - a^2) (m_x - 1/2)(m_y - 1/2) ]
```

The common flip cancels in the parity `XY`. Parity decays only through the
private flips. From the uniform start, `m_y` remains `1/2` until the first Y
reading, so the transition after reading 1 creates no covariance. The first
nonzero covariance can appear only on the transition after reading 2. No
magnitude is claimed.

## Brier convention

The score of a forecast `q` of a bit `Z` is the one-component square
`(q - Z)^2`. The two-class sum equals twice that square and is not used.
This matches the one-component mean square in `_m6_analyze.py`.

If `q` is a function of the history `h` and `q* = E[Z|h]`, then

```text
E[(q - Z)^2 | h] = (q - q*)^2 + q*(1 - q*)
```

The second term depends only on the oracle. The excess of an arm over the
joint oracle is `E[(q - q*)^2]`, with the expectation under `P(h)`.

Aggregation, frozen here because the decision document did not choose one:

- Gate (ii) uses the XOR query alone. Its threshold `1/1000` is unchanged.
- Gate (i) uses the sum of the three one-component excesses, X plus Y plus
  XOR. The mean of the three has the same sign. The gate is the strict
  positivity of the sum. Components are reported separately.
- Gate (iii) is a probability-mass gate on the absolute XOR forecast change.
  It is not a Brier gate.
- Gate (iv) compares forecasts and the update law exactly. It is not a Brier
  gate.

The factorized arm is the terminal product of the oracle's exact marginals,
`q = m_x + m_y - 2 m_x m_y`. It is not a filter that projects after every
step. Under that definition, `q_factorized - q_joint = 2c` and the XOR excess
equals `4 E[c^2]`, with `c` the stage-8 covariance.

## Arms

All five arms see the same readings, timing, and queries.

1. **Joint Bayes oracle.** The four-state filter. External. Known generator.
2. **Factorized terminal projection.** Same exact stage-8 marginals, covariance
   replaced by 0, then the product XOR formula. X and Y forecasts stay the
   marginals.
3. **Marginals plus covariance.** The chart inverse `p_11 = m_x m_y + c`,
   updated by the maps above. This is the ordinary sufficient state.
4. **Current observation only.** The exact Bayes posterior given reading 8
   alone, from the unconditional uniform prior. Reading 8 observes Y, so
   `m_x = 1/2`, `c = 0`, `m_y = 4/5` if the bit is 1, and `m_y = 1/5` if the
   bit is 0. Readings 1–7 are ignored. The XOR forecast is `1/2`.
5. **Direct-history table.** The 256 stage-8 posteriors stored as entries.
   Forecasts equal arm 1. The arm is scored by stored entries and bit length,
   which is the resource charge in the decision document.

There is no sixth arm. An autonomous mean-field filter would be an apparatus
change and is deferred.

## Proof of gate (iv)

**Theorem.** On every belief in the simplex, `(m_x, m_y, c)` determines the
four masses, the three terminal forecasts, and both the observation map and
the transition map. Arm 3 therefore matches arm 1 on forecasts and on the
update law, for every reachable history and every off-manifold legal belief.

**Proof.** The HMM posterior is sufficient for the terminal bits and for every
future observation. The chart is a bijection, so the triple is sufficient.
The observation and transition formulas are functions of the triple alone, with
denominators `P(o) ∈ [1/5, 4/5]` and hence nonzero. Composing them stays inside
the triple. Sufficiency and closure follow. The triple is the posterior, written
in three coordinates, so the match is an algebraic identity. It is not a
compression and it is not evidence about integration machinery.

The enumeration checks the identity on every reachable belief at stages 1..8
(510 beliefs) and checks `q_factorized - q_joint = 2c` on every terminal
history. A mismatch is an implementation defect. Gate (iv) then FAILs and the
run is UNRESOLVED. A match certifies the implementation. It carries no separate
scientific weight about the world.

## Proof that gate (i) is strictly positive

**Theorem.** Under the frozen generator, order, timing, and one-component sum,
the current-only excess over the joint oracle is a strictly positive rational.

**Proof.**

1. **Uniform invariant.** The initial point `(m_x, m_y, c) = (1/2, 1/2, 0)` is
   fixed by the transition map, because every deviation from `1/2` is
   multiplied by a coefficient and the created-covariance term has a factor
   `(m_x - 1/2)(m_y - 1/2)`. The unconditional law is therefore uniform before
   every reading, and `X_t` is independent of `Y_t` at each fixed t. Equivalently,
   the transition is convolution on the group `(Z/2)^2` and preserves Haar
   measure.

2. **Current-only forecasts.** Conditioning the uniform independent prior on a
   BSC(Y) reading gives `P(O=1) = 1/2`, `P(Y=1 | O=1) = 4/5`,
   `P(Y=1 | O=0) = 1/5`, `P(X=1 | O) = 1/2`, and `c = 0` because the
   observation map multiplies `c` by a finite factor. The XOR forecast is
   `1/2`.

3. **Some terminal posterior has `m_x ≠ 1/2`.** Use spins and `eta = 3/5 ≠ 0`.
   After any length-6 prefix, let `μ` be the pre-reading-7 X-spin. Reading 7
   observes X. The two extensions are
   `(μ ± eta) / (1 ± eta μ)`. Both cannot be zero, because that would require
   `μ = -eta` and `μ = eta`. The following transition multiplies the surviving
   nonzero spin by `a b_x = 72/125 ≠ 0`. Reading 8 observes Y, and the X-spin
   update is `(μ_x + eta o ρ) / (1 + eta o μ_y)` for `o ∈ {+1,-1}`. Both
   extensions vanish only if `μ_x = ρ = 0`, which contradicts the previous
   sentence. So at least one full history has terminal `μ_x ≠ 0`.

4. **Every history has positive probability.** For every current state and
   every target state, `C = 0`, `Dx =` the required X flip, and `Dy =` the
   required Y flip realizes that transition, and each of those bits has
   probability in `(0,1)`. Every BSC likelihood is `1/5` or `4/5`. The initial
   masses are positive. Every finite history therefore has `P(h) > 0`.

5. The X excess of the current-only arm is `E[(m_x(h) - 1/2)^2]`. Step 3
   supplies a nonzero summand and step 4 supplies a positive weight, so the
   X excess is positive. The Y excess and the XOR excess are nonnegative
   because the oracle forecast is the conditional mean and the current-only
   forecast is a function of `h`. Their sum is strictly positive.

The proof fixes the sign. It does not evaluate the rational. The enumeration
reports that rational. A computed value that is not strictly positive
contradicts the proof, is recorded as an integrity failure, and makes the run
UNRESOLVED. It is not a reason to change the generator.

## Gates

History probability is `P(h)`, not the uniform count over the 256 strings.
The uniform count is reported as a descriptive non-gating fraction.

| Gate | Frozen comparison | Role |
| --- | --- | --- |
| (i) | `Δ_X + Δ_Y + Δ_XOR > 0`, current-only minus joint | scientific |
| (ii) | `E[4 c_h^2] ≥ 1/1000` | scientific |
| (iii) | `P(\|2 c_h\| ≥ 1/20) ≥ 1/4`, and X/Y forecasts unchanged on every history | scientific mass; the X/Y clause is an identity |
| (iv) | chart and forecasts match on every reachable belief | identity / implementation |

`\|2c\| ≥ 1/20` is the same event as `\|c\| ≥ 1/40`. The inequality is
inclusive. The zero-covariance substitution is exactly arm 2. It preserves
marginals, normalization, the observed history, and the query. `c = 0` lies in
the Fréchet interval whenever the marginals lie in `[0,1]`, so the substituted
belief is a legal distribution. When the reachable `c` is already 0, the
substitution coincides with the reachable posterior. When `c ≠ 0`, the
substituted belief is off-manifold and is not an alias witness.

### Threshold logic, with no world value

If `\|c\| ≥ 1/40` on a set of probability at least `1/4`, then
`E[4c^2] ≥ (1/4) · 4 · (1/40)^2 = 1/1600`. Since `1/1600 < 1/1000`, (iii)
does not imply (ii). Since `\|c\| ≤ 1/4`, a point mass of size `1/250` at
`\|c\| = 1/4` yields `E[4c^2] ≥ 1/1000` with intervention mass below `1/4`,
so (ii) does not imply (iii). Passing both is two views of one omitted scalar,
the law of terminal `\|c_h\|`. The X/Y clause of (iii) holds because the
substitution keeps the marginals.

## Integrity and verdict

The run is an implementation failure, and the verdict is **UNRESOLVED**, if
any of the following fail:

- Path A, Path B, and Path C disagree on any history at any stage `1..8`.
- The history probabilities fail to sum to 1, or any history has probability 0.
- A reachable belief leaves the simplex, or a chart round trip fails.
- The integer joint weights fail to sum to the global denominator.
- The X-flip or Y-flip symmetry fails.
- `q_factorized - q_joint` is not `2c`, or the XOR excess is not `4 E[c^2]`.
- The factorized arm changes an X or Y forecast.
- The current-only closed form disagrees with one Bayes step from the uniform prior.
- Gate (i) is not strictly positive.
- A symmetry-labeled alias fails the zero-mean identity.
- The terminal posterior fails to average to the uniform law:
  `E[m_x] = 1/2`, `E[m_y] = 1/2`, and `E[p_11] = 1/4`. These are the tower
  property applied to the uniform invariant, and the certificate records the
  three values.

Gate labels when the agreed terminal posteriors exist:

- (i) PASS if the excess is `> 0`, else FAIL.
- (ii) PASS if the XOR excess is `≥ 1/1000`, else FAIL.
- (iii) PASS if the intervention mass is `≥ 1/4` and every X/Y forecast is
  unchanged, else FAIL.
- (iv) PASS if the mismatch count is 0, else FAIL.

**Verdict**

- **UNRESOLVED** if any integrity check fails, or if gate (iv) FAILs, or if a
  gate cannot be scored. A FAIL of (i) that contradicts the sign proof is this
  case.
- **ADMIT** if every integrity check holds and (i), (ii), (iii), and (iv) PASS.
- **REJECT** if every integrity check holds, (iv) PASSes, and at least one of
  (i), (ii), (iii) FAILs.

REJECT rejects this benchmark under this protocol. It does not authorize a new
noise level, a new horizon, or a larger model. UNRESOLVED authorizes an
additive correction and a new freeze, not a reinterpretation of the thresholds.

## Reachable-alias audit

The audit is additive and non-gating. It does not change a threshold, an arm,
or the ADMIT / REJECT / UNRESOLVED rule. It selects one pre-written sentence
about what gates (ii) and (iii) mean.

**Same-phase prefix.** Two distinct histories of the same length k. They have
seen the same number of readings, so they sit at the same stage of the
alternating schedule. Stages 1 and 3 are both post-X and are not the same
phase; a collision between them is cross-stage.

**Terminal alias.** A same-phase pair at k = 8 with equal exact marginals and
unequal covariance. Equal marginals and unequal covariance is exactly an
unequal XOR forecast, because the forecasts differ by `2c`.

**Prefix alias.** The same relation at a stage k < 8. For a clocked filter this
is the recurrent-state witness. It is also a continuation witness: if the
marginals agree and `κ` differs, the transition preserves the disagreement
(its coefficients `a b_x`, `a b_y`, and `b_x b_y` are nonzero), and the next
reading of the other variable moves that other marginal by a term proportional
to `κ`. At stage 7 the same disagreement appears in the terminal XOR forecast
after reading 8. A pair with equal marginals and equal covariance is the same
belief. It is a benign merge, not an alias.

**Reachable versus clamped.** Both members of a witness are posteriors of
histories. The zero-covariance substitution is excluded. Cross-stage pairs are
counted in a separate clockless ledger and are never added to the witness
counts.

**Mechanism, assigned after the pairs are found.** `symmetry-X` if the
histories are flips of every X reading, `symmetry-Y` if they are flips of every
Y reading, and `accidental` otherwise. A zero mask is not a flip. The flip
identities are: flipping every X reading sends `(μ_x, μ_y, κ)` to
`(-μ_x, μ_y, -κ)` and preserves `P(h)`; flipping every Y reading sends it to
`(μ_x, -μ_y, -κ)`. A symmetry witness therefore has a zero mean on the flipped
coordinate. An accidental witness is not required to have a zero mean. The
audit does not assume that every witness is a flip.

**T-PROJ** holds when the terminal alias count is 0. **T-CLOSE** holds when
every stage `1..8` has alias count 0. Outcome priority:

| Code | Condition | Sentence selected |
| --- | --- | --- |
| A1 | terminal alias count > 0 | The exact marginal pair is informationally insufficient for the terminal XOR forecast on reachable histories, at exact precision, with the stage known. Q-EXIST for this world. |
| A2 | no terminal alias, and some prefix alias | A marginal-only state has no exact autonomous update on the reachable set, while the terminal marginals do separate the histories. |
| A0 | no same-phase alias at any stage | Exact marginals determine the XOR forecast, and a stage-indexed marginal lookup is exact on the reachable set. Gates (ii) and (iii) measure the product readout. |

If the clockless ledger is nonempty, outcome A3 is reported beside the K1 code
and does not replace it: a clockless marginal state confounds stages. That is
a fact about time or modality.

A lookup that realizes A0 is a table over the reachable marginal keys. Its
entry count and bit length are charged in the same style as arm 5. Sufficiency
of the marginal information is not economy of the table. Descriptive only, and
licensing nothing: per stage, the minimum infinity-norm gap between marginals
of pairs whose covariances differ, or null when no such pair exists.

No alias result may rewrite gates (i)–(iv) or the claim ceiling.

## Claim ceiling

ADMIT supports only this statement: on this generator, this horizon, and this
noise, history changes the first-order forecasts relative to the current
observation, the product of the exact terminal marginals discards XOR
information by the two frozen functionals of one covariance, and the ordinary
chart `(m_x, m_y, c)` matches the joint filter because it is that filter.

The certificate does not promote C2 or C3, does not advance O3, does not
resolve A6, and does not unblock A8. It does not establish a universal minimum
of three neural coordinates, acquisition, a workspace, C4 or C5, organizational
autonomy, cognitive individuality, or phenomenal consciousness. It does not
show that every nonlinear function of the marginals loses XOR information;
only alias outcome A1 says the exact marginal pair itself loses the terminal
XOR forecast, and that sentence remains a Q-EXIST fact about this world. It
does not authorize Stage B, training, organism re-entry, or a ledger edit.

Wording that stays available: "World admitted; acquisition untested." "This
world lacks frozen-threshold headroom." "The ordinary three-number state is
sufficient here because it is the posterior." "One covariance, measured two
ways." "The product projection loses XOR information."

## Replay

Three paths, exact `fractions.Fraction` or integers, no floating point and no
NumPy in the enumeration modules.

- **Path A**, `twostream_filter.py`. A length-4 belief. The transition matrix
  is built in that file by enumerating `C, Dx, Dy`. Observe, normalize,
  transition. No transition after the last reading. The product of the
  observation normalizers is `P(h)`.
- **Path B**, `twostream_replay.py`. Direct sum over all `4^n` latent
  trajectories. Integer transition numerators are built again in that file
  from `C, Dx, Dy`, with weights `(4,1)`, `(49,1)`, `(39,1)`. Observation
  weights are 4 on a match and 1 on a mismatch. The common denominator is
  `4 · (5·50·40)^(n-1) · 5^n`. Grouping trajectories by their latent
  observation bits is distributivity of that sum, not a second model.
  Fractions are formed after the sum. Path B does not import Path A.
- **Path C**, `twostream_moments.py`. The closed maps in the coordinate
  section. Path C does not import Path A or Path B.

Mandatory equalities at every stage `1..8` and every history: the four masses
agree, the history probability agrees, the moments agree with the chart of the
filter, the simplex holds, and both flip symmetries hold. Any disagreement
stops the scientific verdict.

Hand checks locked before the admission horizon, and used by the unit tests:

- Uniform prior, observe X=1: masses `(1/10, 2/5, 1/10, 2/5)` in state-index
  order, `m_x = 4/5`, `m_y = 1/2`, `c = 0`, predictive probability `1/2`.
- Uniform prior, observe Y=0: masses `(2/5, 2/5, 1/10, 1/10)`, `m_y = 1/5`.
- Transition after that X=1 posterior: `m_x = 841/1250`, `m_y = 1/2`, `c = 0`.
- At horizons 1 and 2, every reachable covariance is 0.

## Storage

Arm 5 is charged as 256 entries, four reduced masses per entry, three of them
free, with numerator and denominator bit lengths. The same table is also
reported over the single Path-B denominator. The online filter is charged as
three retained numbers, not 256 entries; the terminal bit length of the
reached belief equals that history's table row.

The marginal index at each stage is charged by its number of distinct exact
marginal keys. It is an exact decoder of covariance only at stages where the
alias count is zero.

## Execution

From the repository root, after the freeze commit:

```text
python -m unittest -v test_twostream
python twostream_run.py
```

`twostream_run.py` checks `TWOSTREAM_FREEZE_v1.json` against the source bytes,
enumerates horizons 1..8 once each, and writes `twostream_results_v1/`. A
second invocation must refuse if that directory exists. Unit tests are part
of the frozen source. They exercise horizons 1..3 and synthetic gate
arithmetic. They must not contain the eight-reading gate values.

Pre-specified outputs, all produced by that single run:

- `twostream_results_v1/RESULTS.md` — verdict, gate table with exact rationals
  and 50-digit truncations, alias outcome, storage, terminal history table.
- `twostream_results_v1/results.json` — the same values as exact numerator and
  denominator strings, plus per-history beliefs and joint numerators.
- `twostream_results_v1/alias_audit.json` — every same-phase witness and every
  cross-stage coincidence.

Reported descriptives, none of them gates: per-query oracle Brier and arm
Brier, `E[c^2]`, max `|c|`, `P(c = 0)`, the uniform fraction of histories with
`|c| ≥ 1/40`, off-manifold clamp counts, bit lengths, per-stage alias counts
and mechanisms, and the minimum marginal separation.

## Freeze rule

`TWOSTREAM_FREEZE_v1.json` records the SHA-256 of this protocol and of every
certificate module, including the tests and the runner. That file is committed
before `twostream_run.py` writes a result. The results commit is a later
commit. A code change after a disagreement requires a new freeze commit before
a replacement result is written. The thresholds in this file do not change in
that correction.
