---
title: E3-OB2 return-prediction relinquishment local protocol
description: Learned versus supplied return-within-horizon predictions through one allocation rule, against a mandatory conservative timeout, with calibration and matched accounting
ms.date: 2026-09-14
---

## Status and disclosure

E3-OB2 is a separately declared, bounded experiment in the side branch
recorded in `E3_BRANCH_RECORD_2026-09-14.md`. It is not an external
preregistration. It makes no claim about `e3/` and doesn't replace the E3k/E3l
main line, whose artifacts are not in this workspace.

It was written after the E3-OB1 result, the OB1 spillover check, the OB2
invariants audit (`e3_fep_seed_results/ob2/audit_ob2.json`) and the building of
the supplied return table. It was written before any timeout tuning, allocator
run or final seed in OB2. No OB2 allocator outcome has been observed.

Known from OB1, on seeds 300–331:

| Policy (soft eligibility) | Recall, budget 3/p 0.02 | Recall, budget 4/p 0.025 |
| --- | ---: | ---: |
| `depth_first` | 0.690 | 0.673 |
| `depth_flag` | 0.800 | 0.811 |
| `depth_timeout_2000` | 0.719 | 0.720 |
| `depth_learned` | 0.575 | 0.573 |

Under soft eligibility, 41–45% of `depth_learned`'s repairs reached cues it had
deprioritized. OB2 changes eligibility to hard, so those numbers do not carry
over.

## 1. Question

> Given a memory's current silence, can the individual predict whether it will
> be needed within the next H ticks accurately enough that one fixed allocation
> rule, using its learned predictions, preserves more useful recall than a
> conservative fixed timeout, while spending less on obsolete memories and
> without excessive loss of returning ones?

**Separating prediction failure from decision failure.** `return_learned` and
`return_supplied` use the identical rule: a cue is eligible for repair iff its
predicted P(query within 500 ticks) ≥ 0.10. Only the source of the probability
differs.

**Level:** functional allocation plus learning of a usage statistic. Not
autonomy. The decision machinery and the estimator's retained state are
protected host scaffolds, declared in section 5.

## 2. World and configurations

The world is `e3_obsolescence_world.py`, unchanged from OB1: 24 cues, 12 of
them permanently obsolete at ticks drawn from [1000, 3000); LONG dormancy is
silent; trace width 9; 6,000 ticks.

The configurations are OB1's selected pair, **budget 3/p 0.02** and
**budget 4/p 0.025**, reused without reselection.

Queries are observed regardless of a memory's eligibility, repair or content
state, so a policy cannot suppress the evidence of a mistaken abandonment.

## 3. Allocators

All allocators are in `e3_obsolescence_world_v2.py`.

**Rules applied to every eligibility policy:**

- **Eligibility:** an ineligible cue receives no repair.
- **Budget:** at most `budget` repairs per tick, one bit per cue. Unused budget
  is not redirected.
- **Order among damaged eligible cues:** deepest, then stalest repair, then a
  random tie-break.
- **Resumption:** eligibility returns as soon as a cue's prediction or silence
  qualifies again. Lost content is never restored.

| Allocator | Eligibility |
| --- | --- |
| `return_learned` (candidate) | Kaplan–Meier estimate of P(query within 500 \| silence) ≥ 0.10 |
| `return_supplied` (same rule, supplied predictions) | Table P(query within 500 \| silence bin, time bin) ≥ 0.10, estimated from 64 independent reference seeds (500–563) |
| `timeout_2000` (mandatory conventional baseline) | Silence ≤ 2,000 |
| `timeout_tuned` (conventional rival) | Silence ≤ T\*, where T\* ∈ {300, 500, 750, 1000, 1500, 2000, 3000, 4000} maximizes mean recall on engineering seeds 0–7 for that configuration; ties go to larger T. Tuning ends before final seeds. |
| `depth_first` (baseline) | All cues |
| `depth_flag` (supplied knowledge) | Not currently obsolete |
| `return_learned_c0.05`, `return_learned_c0.2`, `return_supplied_c0.05`, `return_supplied_c0.2` | Cutoff sensitivity, secondary |
| `return_learned_frozen1500` (intervention) | Estimator state and survival curve frozen at their last refresh before tick 1,500 |
| `none`, `ample` | Controls |

**`return_learned` details.** "Silence" is the time since a cue's last observed
query, or since tick 0.

- **Data:** completed silences, binned into 10-tick bins.
- **Censoring:** every cue's ongoing silence is included as right-censored at
  each refresh, every 50 ticks.
- **Declared assumptions:**
  - Silences are exchangeable across cues and over time. This is false in this
    world, because obsolescence happens only in [1000, 3000).
  - The hazard is not extrapolated beyond observed returns.
  - Warm-up: until 30 completed silences of at least 100 ticks have been seen,
    every cue is predicted to return.
- **Mixture of short active gaps and long dormant intervals:** handled by
  conditioning on elapsed silence, P(return within H | silence ≥ s). No hidden
  phase or episode label is used.

**`return_supplied` details.** It conditions on silence and calendar time, so
it captures the non-stationarity that `return_learned` assumes away. It is
supplied world knowledge, not an oracle about any individual cue.

## 4. Final sample and validity

**Seeds:** 400–431 (32), disjoint from every other seed family used in this
branch.

**Validity checks per configuration on final seeds.** Failure makes the
configuration uninterpretable.

- Environment digests are identical across policies.
- `ample` ≥ 0.90.
- `none` ≤ 0.65.
- The `depth_first` binding fraction is ≥ 0.50.
- `depth_flag` − `depth_first` ≥ 0.025.
- There are zero repairs to ineligible cues across all eligibility policies.

## 5. Accounting

Each policy reports the integers and floats it retains, and the supplied
floats it receives:

| Policy | Retained state |
| --- | --- |
| `depth_first`, timeouts | 48 integers |
| `return_learned` | 50 integers and 1,203 floats |
| `return_supplied` | 48 integers plus a 12 × 19 supplied table |
| `depth_flag` | 48 integers plus 24 supplied flags per tick |

All of this lives in protected host memory: a declared scaffold, not charged
to the repair budget. The comparison is matched in repair budget, eligibility
rule and ordering rule, not in retained state. That mismatch is reported, not
hidden.

## 6. Primary analysis

**Paired contrasts per configuration:**

| Contrast | Measure |
| --- | --- |
| A | `return_learned` − `timeout_2000`, overall recall |
| B | `return_learned` − `depth_first`, obsolete-repair share |
| C | `return_learned` − `depth_first`, lost-at-return fraction |

**Gate D (deterministic).** `return_learned`'s expected calibration error for
silences ≥ 400, pooled over final seeds. It uses ten equal-width
predicted-probability bins and samples every 25 ticks, where the horizon lies
within the run.

**Intervals:** percentile bootstrap over seeds, with 10,000 resamples and
generator seed 20260914. The two-sided level is 1 − 0.05/6 = 0.99167.

**Decision per configuration:**

| Decision | Condition |
| --- | --- |
| Demonstrated | A: mean ≥ 0.03 and lower bound > 0; B: mean ≤ −0.10 and upper bound < 0; C: mean ≤ +0.05 and upper bound < +0.10; D ≤ 0.10 |
| Not demonstrated | A upper bound < 0.03, or B lower bound ≥ 0, or C lower bound ≥ +0.10, or D > 0.10 |
| Inconclusive | Otherwise |

**Overall status**, using valid configurations only:

- **Supported in this world:** demonstrated in every valid configuration.
- **Not supported in this world:** not demonstrated in every valid
  configuration.
- **Mixed or inconclusive:** anything else.
- **Uninterpretable:** no valid configuration.

## 7. Secondary analyses

All are descriptive, with 95% intervals.

**Separating prediction from decision failure:**

- `return_supplied` − `timeout_2000`
- `return_learned` − `return_supplied`

Each is reported for recall, obsolete share and lost-at-return.

**Rivals:**

- `return_learned` − `timeout_tuned`
- `depth_flag` − `return_learned`
- `timeout_tuned` − `timeout_2000`

**Cutoff sensitivity:** each predictor at 0.05 and 0.2, against itself at 0.10.

**Intervention:** `return_learned_frozen1500` − `return_learned`.

**Calibration:** expected calibration error and Brier score for learned and
supplied predictors, by silence class ([0,100), [100,400), [400,1000),
[1000,2000), ≥ 2000).

**Per-policy means:**

- mistaken abandonment (returns while ineligible)
- LONG-return lost fraction
- relinquished-obsolete fraction
- ineligible-dormant fraction
- unspent budget per tick
- repairs per tick
- last-third recall
- state size

## 8. Interpretation fixed in advance

| Result | Reading |
| --- | --- |
| Supported | Using only its own query history, the individual predicted near-term need for its memories well enough that a fixed relinquishment rule beat a conservative hand-set timeout and cut obsolete spending without excessive loss of returning memories. It learned a usage statistic under supplied model assumptions, a supplied horizon and a supplied cutoff, with protected decision machinery. This is not dependency discovery in a causal sense, and not autopoiesis. |
| `return_supplied` beats `timeout_2000`, `return_learned` does not, and learned calibration is worse | The limitation is prediction (learning), plausibly the stationarity assumption. |
| Neither predictor beats `timeout_2000` | The limitation is the decision rule, the cutoff or the repair economics, not prediction. |
| `return_learned` calibrated (D ≤ 0.10) but fails A, B or C | Accurate prediction did not produce better allocation through this rule. This would be a third instance of the branch's repeated lesson. |
| `timeout_tuned` ≥ `return_learned` | A tuned conventional rule is as good as learned prediction here. Learning is not credited. |
| The frozen intervention changes decisions or outcomes | Continued learning is causally used. |
| Inconclusive | No sample extension. |

## 9. Freeze and conduct

`E3_OBSOLESCENCE_FREEZE_v2.json` records raw and LF-normalized SHA-256 hashes
for these files:

- this protocol
- `e3_obsolescence_world.py` and `e3_obsolescence_world_v2.py`
- `audit_e3_obsolescence_v2.py` and its output
- the supplied return table
- `e3_obsolescence_study_v2.py`
- the tuning output

The final phase verifies the hashes and refuses to run on a mismatch. All
outcomes are reported, and nothing changes after the freeze.
