---
title: E3 allocation study v2 local protocol
description: Confirmatory test on fresh seeds of the exploratory finding that observable damage-depth allocation beats recency in the binary-trace toy
ms.date: 2026-09-14
---

## Status and disclosure

This is a local protocol for the exploratory side branch described in
`E3_BRANCH_RECORD_2026-09-14.md`. It is not an external preregistration and
makes no claim about the frozen `e3/` package.

It was written after `E3_ALLOCATION_PROTOCOL_v1.md` stopped at phase 1 and
after two exploratory analyses (branch record, section 5). The author had
therefore already seen the following:

- Exploratory paired recall differences of `deepest_then_stale` (now
  `depth_first`) versus `uniform` on engineering seeds 8–15:
  - +0.179 at width 9/p 0.02/budget 3
  - +0.054 at width 9/p 0.03/budget 3
  - +0.257 at width 9/p 0.03/budget 4
- `uniform` recall on seeds 0–7:
  - 0.831 at 9/0.02/3
  - 0.547 at 7/0.02/2
  - 0.508 at 9/0.03/2
- `uniform` recall on seeds 8–15:
  - 0.815 at 9/0.02/3
  - 0.523 at 9/0.03/3
  - 0.605 at 9/0.03/4
- Earlier v1/v2 outcomes of `recency`, `precision` and `uniform`.

No outcome of `depth_first` versus `recency` and no outcome of
`depth_then_recency` has been observed. No final seed of this protocol has
been run. The selection rule was chosen as a principled feasibility band. It
was not tuned to include or exclude particular configurations. It still
cannot be blind to the exploration above, so fresh final seeds are the
safeguard.

## 1. Claim

> Allocating scarce repair by observable closeness to irreversible loss (damage
> depth) preserves more recall than allocating by recent activity.

The simplest rival is `recency`.

This is the recoverability half of the claim restated on 2026-09-14. It uses
no relevance, rate, self-model or learned quantity. `depth_first` is
essentially a conventional most-endangered-first scrubbing heuristic for
repetition-coded memory. A positive result would therefore confirm that
standard engineering triage beats recency here. It would not show a mechanism
beyond ordinary error correction, which is the discrimination E3 ultimately
needs.

## 2. Allocators

The world is `e3_fep_engineering_seed_v4.py`: v3 world rules, odd widths.
Audit `e3_fep_seed_results/v4/audit_v4.json` found:

- v4 reproduces v3 exactly.
- `depth_first` reproduces the explored scheduler decision for decision.
- Truth-blind policies are invariant under truth relabelling.

| Allocator | Priority among damaged cues |
| --- | --- |
| `depth_first` (candidate) | Largest minority count; ties go to longest since last repair. |
| `depth_then_recency` (secondary) | Largest minority count; ties go to highest recency EMA. |
| `recency` (primary rival) | Highest recency EMA. |
| `uniform`, `random`, `precision`, `recov_supplied`, `recov_learned` | As in v3. |
| `blind_oracle` | As in v3, run for the secondary replication of the ceiling failure. |
| `truth_oracle` | Leak demonstration only; excluded from every analysis. |
| `none`, `ample` | Controls. |

## 3. Fixed world settings

These are identical to v1, section 3:

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

## 4. Configuration selection

Selection uses no new simulation. The rule is applied to the existing
control-only phase-1 data (`e3_fep_seed_results/v3/phase1_controls.json`,
engineering seeds 0–7; LF-normalized SHA-256 `dd081b3f…069a93e37`).

A configuration passes when all of the following hold, each on the mean over
seeds of per-seed overall recall:

1. `ample` ≥ 0.90.
2. `none` ≤ 0.65.
3. `uniform` budget-binding fraction ≥ 0.50.
4. 0.55 ≤ `uniform` ≤ 0.90, so budgeted round-robin is neither hopeless nor
   saturated. This replaces v1's headroom criterion, whose ceiling turned out
   to be weaker than round-robin.
5. `ample` last-third recall ≥ first-third recall − 0.05.

Rank the passing configurations by |`uniform` − 0.725|, ascending, and take up
to three. If none passes, stop and run no comparison.

## 5. Final sample

- **Seeds:** 200–231 (32 seeds), disjoint from engineering seeds 0–15 and from
  v1's unused final seeds 100–131.
- **Coverage:** every v4 policy, on every selected configuration.
- **Replication unit:** the seed.

No seeds are added, removed or rerun.

## 6. Validity checks on final seeds, per configuration

- Environment digests are identical across all policies for every seed.
- Criteria 1, 2, 3 and 5 of section 4 hold.
- 0.50 ≤ `uniform` ≤ 0.95.

If any check fails, the configuration's comparisons are reported but labelled
uninterpretable, and they don't count toward the overall status.

## 7. Primary analysis

**Endpoint:** overall recall per planned query, per seed.

**Comparison:** `depth_first` − `recency`, paired within seed, in each
selected configuration. The family size m is the number of selected
configurations.

**Interval:** percentile bootstrap over seeds, with 10,000 resamples and
generator seed 20260914. The two-sided level is 1 − 0.05/m.

**Minimum useful advantage:** 0.03.

**Decision per configuration:**

| Decision | Condition |
| --- | --- |
| Useful advantage | Mean ≥ 0.03 and interval lower bound > 0 |
| No useful advantage | Interval upper bound < 0.03 |
| Inconclusive | Otherwise |

**Overall status**, using valid configurations only:

| Status | Condition |
| --- | --- |
| Supported in this toy | Useful advantage in every valid configuration |
| Not supported in this toy | No useful advantage in every valid configuration |
| Mixed or inconclusive | Otherwise |
| Uninterpretable | No valid configuration |

## 8. Secondary analyses

All secondary analyses are descriptive, with 95% intervals.

**Paired overall-recall differences:**

- `depth_first` − `uniform`
- `depth_then_recency` − `depth_first`
- `depth_first` − `recov_supplied`
- `depth_first` − `ample`
- `blind_oracle` − `uniform`
- `recov_supplied` − `recency`
- `recov_learned` − `recov_supplied`
- `precision` − `recency`

**Also reported:**

- Paired post-return recall for the primary comparison.
- Per-policy means of harmful-repair fraction, binding fraction, lost-at-return
  fraction and repairs per hot and cold cue-tick.

## 9. Interpretation fixed in advance

| Result | Reading |
| --- | --- |
| Supported | In this symmetric-relevance toy, triage by observable closeness to irreversible loss beats triage by recent activity. This confirms the recoverability half of the claim. It is ordinary ECC-style scrubbing priority: no evidence of self-modeling, anticipation, or anything beyond conventional error correction. |
| `depth_then_recency` − `depth_first` near zero or negative | Recent-activity information adds nothing within a depth class when every memory keeps equal long-run value. |
| `depth_then_recency` − `depth_first` clearly positive | Some consequence information helps once recoverability is accounted for. |
| Not supported | The exploratory advantage did not replicate on fresh seeds. Treat section 5 of the branch record as a selection or forking artifact. |
| Inconclusive | Insufficient precision. No extension of the sample. |

Nothing here bears on the frozen `e3/` machinery, learned relevance,
unobservable deterioration rates, FEP, autopoiesis, organismal autonomy or
consciousness.

Worlds where memories differ in lasting importance (for example, become
permanently obsolete) are the natural next test of the consequence half. They
require a world-rule change and a new protocol.

## 10. Freeze and conduct

`E3_ALLOCATION_FREEZE_v2.json` records raw and LF-normalized SHA-256 hashes
for these files:

- this protocol
- `e3_fep_engineering_seed_v4.py`
- `e3_fep_engineering_seed_v3.py` (imported by the audit)
- `explore_e3_ceiling_search.py` (imported by the audit)
- `e3_allocation_study_v2.py`
- `audit_e3_allocation_v4.py`
- the v4 audit output
- the phase-1 data
- the selection output

The final phase verifies the LF-normalized hashes and refuses to run on a
mismatch.

All outcomes are reported. Nothing changes after the freeze. Later analyses
are labelled exploratory.
