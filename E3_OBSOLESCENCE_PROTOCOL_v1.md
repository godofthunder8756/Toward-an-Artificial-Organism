---
title: E3-OB1 obsolescence experiment local protocol
description: Can an individual learn from its own usage history that a memory has become obsolete, reduce its maintenance, and use the released repairs to preserve functioning elsewhere?
ms.date: 2026-09-14
---

## Status and disclosure

E3-OB1 is a separately declared experiment in the side branch recorded in
`E3_BRANCH_RECORD_2026-09-14.md`. It is not an external preregistration. It
makes no claim about the frozen `e3/` package, and it does not replace the
main-line E3k/E3l work, whose artifacts are not in this workspace.

The protocol was written after the E3-OB1 world audit
(`e3_fep_seed_results/ob1/audit_ob1.json`) and before any configuration
selection or allocator run in this world. Every allocator was defined before
any run, and no allocator performance has been observed in this world.

Prior knowledge that shaped the design:

- The v2 confirmatory result: damage-depth triage beats recency and
  round-robin.
- The finding that loss-model allocators misuse timing information. They are
  excluded here.

## 1. Question and claim

> Can the individual learn that a previously useful dependency has become
> obsolete, reduce its maintenance, and use the released resources to preserve
> functioning elsewhere?

The operational claim is that `depth_learned` preserves more recall than
`depth_first` at equal budget while spending a smaller share of its repairs on
obsolete memories.

- **Level:** functional allocation and learning of a usage statistic. Not
  autonomy or subjectivity.
- **Strong baseline:** `depth_first`, which has no consequence information.

## 2. World

`e3_obsolescence_world.py` keeps the confirmed binary-trace substrate and
repair rule and adds the rules below.

Each cue is in one of four relevance states:

| State | Query weight |
| --- | --- |
| HOT | 1 |
| SHORT dormancy | 0.05 |
| LONG dormancy | 0 (silent) |
| OBSOLETE (absorbing) | 0 |

Transitions and schedule:

- HOT goes dormant with probability 0.02 per tick; the episode is LONG with
  probability 0.2.
- SHORT returns with probability 0.01 per tick; LONG returns with probability
  1/800.
- There are 24 cues, 12 of which become permanently OBSOLETE at ticks drawn
  uniformly from [1000, 3000).
- Runs are 6,000 ticks; the trace width is 9.

Silent LONG dormancy is indistinguishable from obsolescence until the cue
returns. Mistaken abandonment is therefore possible, and it counts through
recall and the reported abandonment rates.

"Obsolete" means never queried again. Usefulness is defined by the external
query process.

## 3. Allocators (all defined before any run)

All policies receive only an `Observation`: a read-only copy of their traces
and the tick. `depth_flag` alone also receives the current OBSOLETE flags.
Policies are also told which cue is queried each tick, but never whether the
answer was correct. They repair one bit per chosen cue, up to the budget,
except `ample`.

| Allocator | Priority among damaged cues | Consequence information |
| --- | --- | --- |
| `depth_learned` (candidate) | Not deprioritized, then deepest, then stalest repair | Deprioritized when silent longer than the 0.99 quantile of its own completed inter-query gaps. Needs ≥ 50 gaps; recomputed every 50 ticks. Reinstated on the next query. The 0.99 risk level is supplied. |
| `depth_first` (strong baseline) | Deepest, then stalest | None |
| `depth_flag` (conventional, supplied knowledge) | Not flagged, then deepest, then stalest | Exact current obsolescence flag |
| `depth_timeout_400` (conventional, hand-set) | As `depth_learned` | Fixed 400-tick timeout, 4× mean SHORT dormancy |
| `depth_timeout_2000` (conventional, hand-set) | As `depth_learned` | Fixed 2,000-tick timeout, 2.5× mean LONG dormancy |
| `learned_override_x0.25`, `learned_override_x4` (interventions) | As `depth_learned` | Threshold overwritten with ×0.25 or ×4 of its value at tick 1,500, then frozen |
| `uniform`, `recency` | As in v4 | None |
| `none`, `ample` | Controls | None |

Deprioritized cues are still repaired when the budget allows, so abandonment
is soft. `depth_learned` never observes obsolescence. It learns the
distribution of gaps it has observed, which is biased by censoring, because
ongoing gaps are not yet complete.

## 4. Configuration selection

- **Grid:** trace width 9, 24 cues, budget {2, 3, 4} × flip probability
  {0.015, 0.02, 0.025}.
- **Seeds:** engineering seeds 0–7.
- **Policies run:** controls only (`none`, `ample`, `uniform`, `depth_first`,
  `depth_flag`). The candidate, timeouts and interventions are not run.

A configuration passes when all of the following hold, on means over seeds of
per-seed recall:

1. `ample` ≥ 0.90. Maintenance is feasible without a budget.
2. `none` ≤ 0.65. Maintenance is necessary.
3. `depth_first` budget-binding fraction ≥ 0.50.
4. `depth_flag` − `depth_first` ≥ 0.05. Relinquishment can matter.
5. `depth_flag` ≥ 0.80. Supplied-knowledge triage keeps live memories viable.

Rank the passing configurations by criterion-4 difference, descending, with
ties going to higher `depth_flag` recall, and take the top two. If none
passes, stop.

Selection uses the strong baseline's performance, but not the candidate's.

## 5. Final sample and validity

- **Seeds:** 300–331 (32 seeds), disjoint from every earlier seed.
- **Coverage:** all 11 allocators, on every selected configuration.

Validity checks on the final seeds, per configuration:

- Environment digests are identical across policies.
- Criteria 1–3 hold.
- `depth_flag` − `depth_first` ≥ 0.025.
- `depth_flag` ≥ 0.75.

A configuration that fails any check is reported as uninterpretable.

## 6. Primary analysis

Per selected configuration, both contrasts are paired within seed:

- **A. Recall:** `depth_learned` − `depth_first`, overall recall per query.
- **B. Expenditure:** `depth_learned` − `depth_first`, share of repairs spent
  on cues that were OBSOLETE at the time.

**Interval:** percentile bootstrap over seeds, with 10,000 resamples and
generator seed 20260914. The two-sided level is 1 − 0.05/(2 × number of
selected configurations), applied to both contrasts.

**Decision per configuration:**

| Decision | Condition |
| --- | --- |
| Demonstrated | A: mean ≥ 0.03 and lower bound > 0; and B: mean ≤ −0.10 and upper bound < 0 |
| Not demonstrated | A upper bound < 0.03, or B lower bound ≥ 0 |
| Inconclusive | Otherwise |

**Overall status**, using valid configurations only:

| Status | Condition |
| --- | --- |
| Supported in this world | Demonstrated in every valid configuration |
| Not supported in this world | Not demonstrated in every valid configuration |
| Mixed or inconclusive | Otherwise |
| Uninterpretable | No valid configuration |

Recall and expenditure are always reported together. Abandoning everything
fails contrast A, because abandoned dormant memories return lost.

## 7. Secondary analyses

All secondary analyses are descriptive, with 95% intervals.

**Paired differences in recall and obsolete-repair share:**

- `depth_flag` − `depth_learned`: the cost of uncertainty relative to supplied
  knowledge.
- `depth_learned` − `depth_timeout_400`, and `depth_learned` −
  `depth_timeout_2000`: learned versus hand-set conventional rules.
- `learned_override_x0.25` − `depth_learned`, and `learned_override_x4` −
  `depth_learned`: whether the stored threshold is causally used.
- `depth_first` − `uniform`, and `depth_first` − `recency`: replication of the
  baseline.

**Per-policy means:**

- mistaken-abandonment fraction (returns while deprioritized)
- lost-at-return fraction, overall and for LONG returns
- correct-relinquishment fraction (obsolete cue-ticks deprioritized)
- false-abandonment exposure (dormant cue-ticks deprioritized)
- binding fraction, repairs per tick, last-third recall

**Parameter accuracy.** Compare `depth_learned`'s final threshold with two
reference values:

- The 0.99 quantile of completed gaps in the same run. This is a plumbing
  check, since it uses the same data.
- The 0.99 quantile of completed gaps in a 120,000-tick world with the same
  parameters and no obsolescence (seeds 900 and 901). This is the population
  target without censoring by obsolescence.

## 8. Interpretation fixed in advance

| Result | Reading |
| --- | --- |
| Supported | From its own usage history, the individual learned a silence statistic that let it stop maintaining memories that had become obsolete. The released repairs preserved more recall than damage-depth triage. What it learned is a statistic under a supplied risk level; it neither observed obsolescence nor modelled why memories stop mattering. |
| Supported, and learned ≈ a timeout rule | Learning adds little over a sensible hand-set conventional rule in this world. |
| Supported, and learned clearly beats both timeouts | Learning the silence scale matters when fixed scales are wrong. |
| Overrides change decisions and recall or spend | The stored threshold is causally used. |
| Overrides change nothing | The result is insensitive to the learned value; don't credit learning. |
| Large `depth_flag` − `depth_learned` gap | Uncertainty about obsolescence is costly. |
| Not supported | Learned relinquishment did not beat damage-depth triage here. Report mistaken abandonment and spend to show why. |
| Inconclusive | No sample extension. |

This experiment cannot establish anything about:

- the frozen `e3/` machinery
- causal dependency learning beyond usage statistics
- whether the individual maintains the machinery making these decisions, which
  stays protected and external
- FEP, autopoiesis, autonomy or consciousness

## 9. Freeze and conduct

`E3_OBSOLESCENCE_FREEZE_v1.json` records raw and LF-normalized SHA-256 hashes
for these files:

- this protocol
- `e3_obsolescence_world.py`
- `audit_e3_obsolescence.py` and its output
- `e3_obsolescence_study.py`
- the selection outputs

The final phase verifies the LF-normalized hashes and refuses to run on a
mismatch.

All outcomes are reported. Nothing changes after the freeze.
