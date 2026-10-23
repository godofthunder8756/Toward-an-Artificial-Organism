# Algebra and independent-unit interpretation

## Registered deterministic construction

Let:

- `e` be the signed integer event content in `{-8, -4, 4, 8}`;
- `r = 1` when the attributed-owner token equals the controlled-entity token and the resolved relation is `SELF`, and `r = 0` for `OTHER` or the intervention-only relation `UNBOUND`;
- `p = r e` be the declared present-state mediator;
- `p_eff = p` under ordinary coupling and `p_eff = 0` under the registered S4 coupling ablation;
- `g` be the current goal;
- `d_i` be the displacement associated with option `i`.

The registered prospective evaluator and selector are:

```text
F_i = p_eff + d_i
Q_i = -(F_i - g)^2
A   = unique argmax_i Q_i
```

A tie invalidates the case. All scientific quantities use exact signed integers.

`SELF` in these equations is an engineered relational role. It is resolved by opaque-token equality before the history representation is formed. Literal token values, event labels, run identifiers, process identifiers, expected outcomes, filenames, and harness-only origin metadata do not enter the evaluator or selector.

## Reduction of the target panel

The two target options are constructed as:

```text
d_COMPENSATE = g - e
d_BASELINE   = g
```

Therefore:

```text
F_COMPENSATE = p_eff + g - e
F_BASELINE   = p_eff + g

Q_COMPENSATE = -(p_eff - e)^2
Q_BASELINE   = -p_eff^2

Q_COMPENSATE - Q_BASELINE = 2 e p_eff - e^2
```

For represented `SELF`, `p_eff = e`, so `COMPENSATE` is the unique winner by `e^2`. For `OTHER`, `UNBOUND`, or the S4 target coupling ablation, `p_eff = 0`, so `BASELINE` is the unique winner by `e^2`. With the registered content magnitudes, these target margins are `16` and `64`.

The goal `g` shifts the recorded futures and changes the semantic option displacements, but it cancels from both target-option `Q` expressions and therefore does not affect the target winner or winning margin. The sign of `e` changes `p`, futures, and displacements, while the target winner label and margin depend only on the relation and `e^2`.

## Other registered reductions

### S2 swap

S2 uses `g = 0`, `p = +m` or `-m`, and displacements `-m` and `+m`, for `m` in `{4, 8}`. The option that cancels `p` has `Q = 0`; the other has `Q = -4m^2`. The winning margin is therefore `4m^2`, or `64` and `256`. Swapping the complete history explicitly swaps the content used to recompute `p`, so the winning semantic direction follows the donor by construction.

### S4 specificity panels

The coupling-ablated evaluator uses `p_eff = 0`. For the panel `g = -1`, `d = {-1, 4}`, the registered winner is `d = -1` by a margin of `25`. For `g = 1`, `d = {-4, 1}`, the registered winner is `d = 1`, also by `25`. These are evaluator-competence controls under the ablation.

### S5 divergent and restored arms

The divergent intervention substitutes history content `-e`, which gives `p = -e` while the original target options remain fixed. Then:

```text
Q_COMPENSATE = -4e^2
Q_BASELINE   = -e^2
```

The divergent arms therefore select `BASELINE` by `3e^2`, or `48` and `192`. Full restoration recreates the complete checkpoint bytes and thus restores `p = e`; with the same deterministic code and inputs, its continuation endpoint and read-only probe projection match the direct arm.

The implementation advances each direct or restored state through 256 neutral ticks before probing. A neutral tick increments only the clock and preserves `p`. It then performs 256 read-only probes on that single resulting state. These probes test stability and non-mutation; they are not 256 independently sampled observations or 256 recorded evolving states.

### P and Q clamps

The P clamp fixes `p = 4`, `g = 0`, and options `d = {-4, +4}`. The `-4` option has `Q = 0` and the `+4` option has `Q = -64`, irrespective of the retained upstream history.

The Q clamp bypasses prospective evaluation and supplies the selector with `Q_LEFT = 16` and `Q_RIGHT = 0`. The defined unique-maximum rule therefore selects `LEFT` by `16`, irrespective of upstream state.

## Active and inert factors in this panel

| Factor | Status for the registered outputs | Interpretation |
|---|---|---|
| Resolved relation `r` | Active | Determines whether event content enters `p`. |
| Event content `e` | Active, with output-specific qualifications | Sets `p` in `SELF` arms and helps construct the option displacements. Its magnitude sets the principal margins; its sign changes numeric states, futures, displacements, and S2 direction. |
| Effective mediator `p_eff` | Active | Direct input to `F` and `Q`. Under S4 ablation it is fixed to zero even though stored `p` is retained. |
| Option displacement `d_i` | Active | Direct input to `F` and hence `Q`. |
| Goal `g` | Active in the general evaluator; algebraically inert to the target winner and margin | It is part of the registered evaluator and shifts target futures/displacements, but cancels from target `Q` comparisons because the target options are defined from `g`. |
| Presentation order | Inert to semantic results | It changes serialized order only. Reversal checks order invariance. |
| Literal opaque token values | Inert after relation resolution | Only token equality is used; six frozen bijections test literal-token invariance. |
| Harness-only `true_origin` | Inert by interface exclusion | It is recorded for S6 but never supplied to the core. |
| `event_key` | Inert to evaluation and selection | It affects canonical state bytes and hashes, not `p`, `F`, `Q`, or choice. |
| Tick | Inert to evaluation and selection | Neutral transitions change the tick but preserve `p`; tick affects state serialization only. |
| Case/run labels, order metadata, PID, nonce, paths, expected predicates | Inert by interface exclusion | They are provenance or harness variables and are excluded from evaluator and selector inputs. |
| Stored `p` in the S4 ablated arm | Inert to that arm's evaluation | The evaluator receives the fixed reference `p_eff = 0`. |
| Upstream history after the P clamp | Inert to downstream `F/Q/choice` once `p` is fixed | It remains in state bytes but is outside the evaluator interface. |
| All upstream state after the Q clamp | Inert to selection | The selector receives only the fixed Q vector. |
| Quadratic objective | Fixed, not experimentally varied | Results do not establish generality to other objectives. |

## Unit hierarchy and repeated observations

The frozen campaign used six fresh worker processes in the order `FORWARD, REVERSED, FORWARD, REVERSED, FORWARD, REVERSED`. Each process executed the same deterministic registered panel with a different frozen opaque-token bijection.

| Family | Cases per process | Trace records per process | Read-only probes per process | Cases across six | Trace records across six | Read-only probes across six |
|---|---:|---:|---:|---:|---:|---:|
| S1 | 16 | 32 | 8,192 | 96 | 192 | 49,152 |
| S2 | 4 | 16 | 4,096 | 24 | 96 | 24,576 |
| S3 | 16 | 48 | 12,288 | 96 | 288 | 73,728 |
| S4 | 16 | 64 | 16,384 | 96 | 384 | 98,304 |
| S5 | 16 | 64 | 16,384 | 96 | 384 | 98,304 |
| S6 | 16 | 64 | 16,384 | 96 | 384 | 98,304 |
| P clamp | 2 | 4 | 1,024 | 12 | 24 | 6,144 |
| Q clamp | 2 | 0 | 0 | 12 | 0 | 0 |
| **Total** | **88** | **292** | **74,752** | **528** | **1,752** | **448,512** |

Q clamp contributes four direct selector invocations per process, or 24 across the six processes, rather than trace/probe records.

The 448,512 figure is the product of 1,752 trace records and 256 non-mutating probes per trace. Those probes are repeated deterministic observations within a trace. They verify persistence and read-only behavior; they are not independent experimental units and must not be used to inflate evidentiary weight.

For transparent structural counting:

- the 88 ordered cases per process reduce to 44 registered parameter settings when each `NORMAL`/`REVERSED` order pair is counted once: S1 8, S2 2, S3 8, S4 8, S5 8, S6 8, P clamp 1, Q clamp 1;
- after option-order normalization and removal of duplicate arms and family/case labels, the trace records contain 44 distinct stored-state-plus-coupling configurations;
- because S4 ablated traces feed `p_eff = 0` regardless of stored `p`, those configurations reduce to 30 distinct actual evaluator-input tuples `(p_eff, goal, semantic option set)`;
- the trace outputs contain 12 distinct semantic selector-input Q vectors, and Q clamp adds one further fixed vector, for 13 distinct selector-input vectors in total.

The last three counts are a descriptive structural census of the frozen normalized projection, not additional preregistered endpoints. They answer different questions and should not be collapsed into an undefined count of "unique observations."

The six processes are exact reproducibility and order/token controls for the same finite deterministic panel. They are independent process launches, but not six draws from a stochastic population. No inferential p-value or population-level confidence interval is warranted.

## Claim boundary

The maximum supported claim remains exactly:

> In the registered finite construction, a relationally self-indexed temporal state causally influenced future-directed choice through the separately intervened prospective-evaluation path.

The algebra describes a deliberately engineered reference construction. It does not establish spontaneous emergence of a self-model, phenomenal consciousness, sentience, subjective experience, personhood, life, AGI, human-equivalent selfhood, metaphysical identity, accurate factual self-knowledge, or architectural novelty. `NOVELTY = UNADJUDICATED`.

## Frozen evidence bindings

- D0 architecture SHA-256: `f6c5ffb09c062b3421e33ebfdf2b732aeddaee679a89422cee21f902d5a32020`
- D1 adversarial review SHA-256: `5ac82b227604d937cf3c515ff3ab96c2b71e95a45fffbcf678abd8b5a80c3ca5`
- Preregistration SHA-256: `fbecb854eca0e096a2e66e8d047baea2cf466f8872d23202eaa60b946c9d4019`
- Frozen core implementation SHA-256: `3e8d93ce96fdb6b2d70d228635a27531f968272a7e3053a320833f29dc99fa60`
- Frozen experiment implementation SHA-256: `a569cfa709ed84431555ebe4192d6700ebea47a88c37162b4f3849450edfd3ee`
- Frozen decision SHA-256: `5c17ff2b6800b0e940b1309283d53dc874c85242cc6591116665c157f1234527`
- Normalized projection SHA-256: `565cf5f59fdc0d13b2ea538bd3bc8830cd5fff0ad80a51e19328128efe72d7f0`
- Analysis SHA-256: `264343255ef6d5ca2c7b2af03c8a81d7ee7ca674a7723bae1be7f8781cfd9027`
