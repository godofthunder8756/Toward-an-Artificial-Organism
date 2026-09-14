---
title: E3 allocation study v1 local protocol
description: Recoverability-and-consequence maintenance allocation vs recency in the binary-trace toy; selection rule, sample, gates and interpretation fixed before selection and final runs
ms.date: 2026-09-14
---

## Status

This is a local protocol for an exploratory side branch in H2's lineage (see
`E3_BRANCH_RECORD_2026-09-14.md`). It is not an external preregistration. It
is not part of the frozen `e3/` package and makes no claim about it.

- **Written:** after the v3 invariants audit
  (`e3_fep_seed_results/v3/audit_v3.json`) and before any configuration
  selection or candidate-allocator comparison.
- **Candidate outcomes seen so far:** the author has seen v1/v2 outcomes for
  `precision`, `recency`, `uniform`, `random` and a truth-leaking oracle. No
  performance outcome of `recov_supplied`, `recov_learned` or `blind_oracle`
  has been observed.
- **Hash freeze:** hashes are recorded in `E3_ALLOCATION_FREEZE_v1.json`
  after configuration selection and before the final seeds run.

## 1. Claim

> An individual can allocate scarce maintenance resources according to
> predicted future recoverability and functional consequence, rather than only
> recent activity.

Operationally, in a configuration where maintenance is scarce but feasible,
`recov_supplied` achieves higher recall per planned query than `recency` at
equal budget. This is tested for `recov_supplied` and `recov_learned`.

- **Level:** functional allocation only. Not organismal autonomy or
  subjectivity.
- **Simplest rival:** `recency`, allocation by recent query activity. `uniform`
  and `random` are weaker rivals.

## 2. What each allocator receives

All budgeted allocators see the same things:

- Their own current trace bits.
- Which cue was queried on each tick.
- Their own repair history.

No allocator receives correctness feedback.

| Allocator | Additional inputs |
| --- | --- |
| `recency`, `precision`, `uniform` | Their v1/v2 statistics, unchanged |
| `recov_supplied` | True corruption rate; true relevance-chain rates, cold query weight and initial hot probability |
| `recov_learned` | The same chain inputs. Corruption rate is estimated online from new minority bits in cues that were consistent after the previous repair; it keeps one integer per cue. |
| `blind_oracle` (ceiling) | True corruption rate and true future query times. Never truth. |
| `truth_oracle` (leak demonstration) | Truth. Excluded from every comparison and criterion. |

`recov_*` and `blind_oracle` use the myopic loss model documented in
`e3_fep_engineering_seed_v3.py` with a 300-round horizon. Relevance inference
uses a mean-field forward filter over query identities.

Limitation fixed in advance: audit E found the learned rate within 1% of
truth, because damage is directly observable here. `recov_learned` versus
`recov_supplied` is therefore not the hard problem of learning an unobservable
deterioration rate. It cannot address the E3k/E3l finding, which is not in
this workspace. Relevance-chain rates are supplied to both `recov` variants,
so nothing here concerns learned relevance.

## 3. World and fixed settings

The v3 world rules apply, with odd widths only. The following settings are
fixed:

| Setting | Value |
| --- | --- |
| Cues | 16 |
| Hot to cold rate | 0.02 |
| Cold to hot rate | 0.01 |
| Cold query weight | 0.05 |
| Recency decay | 0.05 |
| UCB constant | 0.05 |
| Post-return window | 20 ticks |
| Ticks per run | 6,000 |

## 4. Configuration selection, fixed before phase 1

- **Grid:** widths {5, 7, 9} × flip probability {0.01, 0.02, 0.03} × budget
  {2, 3, 4}.
- **Seeds:** engineering seeds 0–7.
- **Policies run:** controls only (`none`, `random`, `uniform`,
  `blind_oracle`, `ample`). No candidate or rival allocator is run in phase 1.

A configuration passes when all five criteria hold. Each criterion uses the
mean over seeds of per-seed overall recall.

1. `ample` ≥ 0.90. Maintenance is feasible with unlimited truth-blind repair.
2. `none` ≤ 0.65. Maintenance is necessary.
3. `uniform` budget-binding fraction ≥ 0.50. Scarcity binds.
4. `blind_oracle` − max(`uniform`, `random`) ≥ 0.08. Allocation can matter.
5. `ample` last-third recall ≥ first-third recall − 0.05. Recall is not
   dominated by long-run relaxation.

Selection:

- Rank passing configurations by criterion-4 headroom, descending; break ties
  by higher `ample` recall.
- Take the top two.
- If exactly one passes, use it.
- If none passes, stop. Record that no feasible discriminating configuration
  exists in this grid, and run no allocator comparison.

## 5. Final sample

- **Seeds:** 100–131 (32 seeds), disjoint from all engineering seeds 0–15.
- **Coverage:** every policy in `v3.POLICIES`, on every selected
  configuration.
- **Replication unit:** the seed, meaning one independently generated
  environment. Every policy replays that seed's environment.

No seeds are added, removed or rerun after outcomes are seen.

## 6. Validity checks on final seeds, per configuration

- The environment digest is identical across all policies for every seed.
- Criteria 1, 2, 3 and 5 of section 4 hold on the final seeds.
- Criterion 4 holds with its threshold relaxed to 0.04.

If any check fails, that configuration's allocator comparisons are still
reported but are labelled uninterpretable, and they don't count toward the
overall status.

## 7. Primary analysis

**Endpoint:** overall recall per planned query over the whole run, per seed.

**Primary comparisons** (paired within seed):

- `recov_supplied` − `recency`
- `recov_learned` − `recency`

Both are made in each selected configuration, so the family size is m = 2 ×
(number of selected configurations).

**Interval:** percentile bootstrap over seeds, with 10,000 resamples and
generator seed 20260914. The two-sided level is 1 − 0.05/m.

**Minimum useful advantage (MUA):** 0.03 absolute recall. The value was fixed
here before any `recov` outcome was seen. It is smaller than the 0.08 headroom
selection requires, so an advantage of this size is achievable. The 0.05 gate
in v0.11 applies to a different quantity and is not borrowed.

**Decision for each comparison:**

| Decision | Condition |
| --- | --- |
| Useful advantage | Mean ≥ 0.03 and interval lower bound > 0 |
| No useful advantage | Interval upper bound < 0.03 |
| Inconclusive | Otherwise |

**Overall status**, using valid configurations only:

| Status | Condition |
| --- | --- |
| Supported in this toy | `recov_supplied` − `recency` is a useful advantage in every valid configuration |
| Not supported in this toy | It is "no useful advantage" in every valid configuration |
| Mixed or inconclusive | Otherwise |
| Uninterpretable | No configuration is valid |

`recov_learned` is reported alongside the overall status and doesn't change
it.

## 8. Secondary analyses

All secondary analyses are descriptive, with 95% intervals and no decisions.

**Paired differences:**

- Post-return recall for both primary comparisons.
- `recov_learned` − `recov_supplied`.
- `blind_oracle` − `recov_supplied`.
- `recov_supplied` − `uniform`.
- `precision` − `recency`.

**Per-policy means:**

- Harmful-repair fraction.
- Budget-binding fraction.
- Fraction lost at return.
- Repairs per hot and cold cue-tick.
- `recov_learned`'s final rate estimate.

## 9. Interpretation fixed in advance

| Result | Reading |
| --- | --- |
| `recov_supplied` useful advantage | In this toy, ranking damaged memories by predicted loss of future recall beats recent activity at equal budget. |
| `recov_learned` also useful | Rate learning is not a bottleneck when damage is directly observable. This is expected from audit E, not a discovery. |
| `recov_supplied` useful, `recov_learned` not | A rate-estimation cost exists even with observable damage. This would be surprising; inspect before interpreting. |
| No useful advantage in valid configurations | A substantive negative for this allocator class in this toy: the configuration was feasible and the truth-blind ceiling showed headroom. It does not bear on FEP, autopoiesis or E3. |
| Inconclusive | Precision was insufficient. The sample is not extended after seeing results. |
| A `recov` policy exceeds `blind_oracle` | Allowed. The oracle is a greedy ceiling heuristic, not a proven optimum. |

This study cannot establish anything about:

- the frozen `e3/` machinery
- learned relevance
- learning unobservable deterioration rates
- organismal autonomy, wanting, life or consciousness

## 10. Freeze and conduct

`E3_ALLOCATION_FREEZE_v1.json` records SHA-256 hashes, of both the raw bytes
and the LF-normalized bytes, for these files:

- this protocol
- `e3_fep_engineering_seed_v3.py`
- `e3_allocation_study.py`
- `audit_e3_allocation.py`
- the audit output
- the phase-1 results and selection

The final phase verifies the LF-normalized hashes and refuses to run on a
mismatch. That rule follows the line-ending erratum in the branch record.

All outcomes are reported, including negative, inconclusive and
uninterpretable ones. No source, setting, threshold or sample changes after
the freeze. Any later analysis is labelled exploratory.
