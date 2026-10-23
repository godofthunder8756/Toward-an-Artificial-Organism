# SITC statistics and effect-size report - RC2 interpretation

## Statistical scope

The registered reference construction uses exact integer arithmetic and deterministic execution. The six process repetitions test reproducibility under frozen token bijections and forward/reversed execution orders. They are not random samples from a population, and the repeated probes within a trace are not independent observations. Inferential p-values, sampling confidence intervals, and claims based on nominal probe count are therefore inapplicable.

The frozen analyzer returned `SITC_PASS`. This report preserves that decision and all frozen criteria while separating experimental case records, trace records, repeated probes, and distinct deterministic input configurations.

## Campaign inventory

| Family | Cases/process | Traces/process | Probes/process | Cases/6 processes | Traces/6 processes | Probes/6 processes |
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

Q clamp bypasses the prospective evaluator and contributes four direct selector invocations per process, or 24 in the campaign. It therefore contributes cases and selector checks, but no trace/probe records.

Each trace runs the same read-only probe 256 times without mutating the state. The 448,512 total is exactly `1,752 traces x 256 probes`. It is evidence that each registered endpoint remained stable and that observation did not mutate it. It is not a count of statistically independent units.

## Distinct structural configurations

The following counts use explicit definitions and are descriptive of the frozen normalized projection:

| Definition | Count per canonical process projection | Interpretation |
|---|---:|---|
| Ordered registered cases | 88 | Includes `NORMAL` and `REVERSED` presentation as separate order-control cases. |
| Registered parameter settings with presentation order collapsed | 44 | S1 8, S2 2, S3 8, S4 8, S5 8, S6 8, P clamp 1, Q clamp 1. |
| Stored-state-plus-coupling trace configurations, after semantic option-order normalization and duplicate removal | 44 | Retains stored `p` and whether ordinary or ablated coupling was used. Q clamp has no trace and is excluded. |
| Actual evaluator-input tuples `(p_eff, goal, semantic option set)` after duplicate removal | 30 | S4 ablated traces use `p_eff = 0` irrespective of stored `p`. Q clamp bypasses the evaluator and is excluded. |
| Distinct semantic selector-input Q vectors in trace records | 12 | Repeated arms, cases, probes, and orders producing the same semantic Q vector are counted once. |
| Additional Q-clamp selector-input vector | 1 | Fixed `LEFT = 16`, `RIGHT = 0`; total selector-input vectors including this control: 13. |

These counts are not interchangeable. They quantify different layers of the deterministic assay and were not preregistered as inferential endpoints.

## Exact registered contrasts

| Quantity | Frozen result | Registered threshold or comparator |
|---|---:|---:|
| Minimum absolute present-state contrast | 4 | At least 4 |
| Maximum absolute present-state contrast | 8 | Descriptive |
| Minimum winning Q margin | 16 | At least 16 |
| Maximum winning Q margin | 256 | Descriptive |
| S1 checks passed | 96/96 | All required |
| S2 checks passed | 24/24 | All required |
| S3 checks passed | 96/96 | All required |
| S4 checks passed | 96/96 | All required |
| S5 checks passed | 96/96 | All required |
| S6 checks passed | 96/96 | All required |
| P-clamp checks passed | 12/12 | All required |
| Q-clamp checks passed | 12/12 | All required |
| Complete-state restoration compatibility | 96/96 | Byte-identical restoration plus registered direct comparison |
| Scientific failures recorded by the frozen analyzer | 0 | None permitted for PASS |
| Normalized cross-process equality | 6/6 | Exact equality required |

The principal target-panel margin is `e^2`, which is `16` or `64`. S2 yields `4m^2`, or `64` and `256`. The divergent S5 controls yield `3e^2`, or `48` and `192`. The S4 specificity panels yield `25`; the P clamp yields `64`; the Q clamp yields `16`. These are exact consequences of the registered equations and input values, not estimates of an unknown population effect.

## Process replication and order controls

The six fresh-process order sequence was:

```text
FORWARD, REVERSED, FORWARD, REVERSED, FORWARD, REVERSED
```

All six normalized projections were byte-identical after canonical ordering. This establishes reproducibility across the registered process launches, token bijections, and execution orders. It does not create six independent stochastic effect estimates.

Normalized projection SHA-256:

`565cf5f59fdc0d13b2ea538bd3bc8830cd5fff0ad80a51e19328128efe72d7f0`

## Restoration measurement

S5 full restoration recreated the checkpoint bytes exactly in all 96 expanded cases. The direct and full-restored states were each advanced through 256 neutral ticks, which increment only the clock and preserve `p`, and were then read 256 times without mutation. The saved evidence establishes equality of the restored state and deterministic continuation endpoint/read-only projection. The 256 probes are a persistence and non-mutation control rather than 256 evolving trajectory samples.

## Claim boundary

The maximum supported claim remains exactly:

> In the registered finite construction, a relationally self-indexed temporal state causally influenced future-directed choice through the separately intervened prospective-evaluation path.

The result validates the registered causal assay in an engineered finite construction. It does not establish spontaneous machine selfhood, phenomenal consciousness, sentience, subjective experience, personhood, life, AGI, human-equivalent selfhood, metaphysical identity, accurate factual self-knowledge, or architectural novelty. `NOVELTY = UNADJUDICATED`.

## Frozen evidence bindings

- Preregistration SHA-256: `fbecb854eca0e096a2e66e8d047baea2cf466f8872d23202eaa60b946c9d4019`
- Frozen decision SHA-256: `5c17ff2b6800b0e940b1309283d53dc874c85242cc6591116665c157f1234527`
- Analysis SHA-256: `264343255ef6d5ca2c7b2af03c8a81d7ee7ca674a7723bae1be7f8781cfd9027`
- Normalized projection SHA-256: `565cf5f59fdc0d13b2ea538bd3bc8830cd5fff0ad80a51e19328128efe72d7f0`

