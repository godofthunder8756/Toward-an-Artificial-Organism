# AC15 results v1: acquired allocation under a graded access law

Frozen final sample, seeds **1900-1903** x 2 histories = 8 individuals per arm, 8 arms,
64 rows, 2048 ticks, intervention at t=1024. Declaration: `AC15_PROTOCOL_v1.md` (written
and hashed before the run; its hash is in `ac15_results_v1/pre_run_snapshot.json`).
Primitive and its engineering record: `ac15.py`, `AC15_ENGINEERING_v1.md`.

## Verdict

**All five prespecified gates pass.**

| gate | requirement | measured | verdict |
| --- | --- | --- | --- |
| G1 | learner beats `preserve` and `relinquish` by >= 0.08 on mean late per-channel productivity | +0.199 and +0.260 | **PASS** |
| G2 | learner not beaten by any state-blind rival (fixed duty 1-8, random p in {0.25,0.5,0.75}) | 0.6989 vs best rival 0.5000 | **PASS** |
| G3 | `fixed_period_1` and `streak_never` reproduce `preserve` exactly, state hash included | identical on all 8 individuals | **PASS** |
| G4 | every arm completes the horizon | 64/64 | **PASS** |
| G5 | learner keeps the valid channel (>= 0.95) and does not keep the stale one (> 0) | kept 1.000, moved 0.398 | **PASS** |

Scope, as declared before running: this is a **behavioural and economic** result. It is
not survival-level (G4 holds: nothing dies), and it makes no claim about consciousness,
experience, or autopoiesis.

## The result, per arm

Mean late per-channel productivity over t=1024..2048 (kept channel = fuel, still valid;
moved channel = material, stale after the intervention):

| arm | alive | kept | moved | mean | final demand (region 0) | relinquishments |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `allocate` (learner) | 8/8 | **1.000** | **0.398** | **0.699** | 21.0 | 1.0 |
| `preserve` | 8/8 | 1.000 | 0.000 | 0.500 | 42.0 | 0.0 |
| `relinquish` | 8/8 | 0.343 | 0.534 | 0.439 | 0.0 | 0.0 |
| `random` (p=0.5) | 8/8 | 1.000 | 0.000 | 0.500 | 42.0 | 0.0 |
| `fixed_schedule` (period 2) | 8/8 | 1.000 | 0.000 | 0.500 | 42.0 | 0.0 |
| `no_learning` (sham write) | 8/8 | 1.000 | 0.000 | 0.500 | 42.0 | 17.8 |
| `fixed_period_1` (G3) | 8/8 | 1.000 | 0.000 | 0.500 | 42.0 | 0.0 |
| `streak_never` (G3) | 8/8 | 1.000 | 0.000 | 0.500 | 42.0 | 0.0 |

Exact per-individual learner values (the protocol requires these, not only means):

| individual | kept | moved | mean | demand | relinquishments |
| --- | ---: | ---: | ---: | --- | ---: |
| seed1900h0 / h1 | 1.000 | 0.441 | 0.721 | [21,0] | 1 |
| seed1901h0 / h1 | 1.000 | 0.400 | 0.700 | [21,0] | 1 |
| seed1902h0 / h1 | 1.000 | 0.378 | 0.689 | [21,0] | 1 |
| seed1903h0 / h1 | 1.000 | 0.371 | 0.686 | [21,0] | 1 |

All eight relinquish exactly one slot, keep the valid route at productivity 1.000, and
end with one region-0 slot occupied ([21,0] = one live entry at 21 cells). No individual
contradicts the aggregate.

The design is two-sided by construction, and the measurements show both ways to fail it
being failed: `preserve` keeps what it should not (moved 0.000, mean 0.500), and
`relinquish` loses what it should keep (kept 0.343, mean 0.439). Only a decision driven
by the organism's own realized outcomes occupies the middle.

## G2: the rival sweep on the final seeds

| configuration | mean late per-channel productivity | alive |
| --- | ---: | ---: |
| fixed duty, period 1 | 0.5000 | 8/8 |
| fixed duty, period 2 | 0.5000 | 8/8 |
| fixed duty, period 3 | 0.5000 | 8/8 |
| fixed duty, period 4 | 0.5000 | 8/8 |
| fixed duty, period 8 | 0.5000 | 8/8 |
| random p=0.25 | 0.5000 | 8/8 |
| random p=0.5 | 0.5000 | 8/8 |
| random p=0.75 | 0.5000 | 8/8 |
| learner, streak 2 | 0.6989 | 8/8 |
| learner, streak 4 | 0.6989 | 8/8 |
| learner (prespecified), streak 6 | 0.6989 | 8/8 |
| learner, streak 8 | 0.6989 | 8/8 |

The whole state-blind family sits at exactly 0.5000, i.e. identical to `preserve`, and the
learner's whole family sits at 0.6989. Two things are worth stating plainly rather than
burying:

- **No blind rival ever lets the stale entry lapse.** These arms decide whether to
  *renew*, not whether to relinquish: with renewal opportunities frequent and duty
  periods up to 8 (or random p as low as 0.25) the entry's 64-tick life is always
  extended, so they keep the stale route and score exactly `preserve`. Their family is
  therefore conservative in this world, and G2 is a real but *weak* test — it shows no
  blind rival beats the learner, not that none could be designed to.
- **The learner's own threshold makes no difference (0.6989 for streaks 2, 4, 6 and 8.)**
  This is the same shape as AC11's side-finding that the optimum is a *level*, not a
  *switch*, and it is why the protocol required the learner's prespecified setting rather
  than the best member of its own sweep. Here it is not a defect: the learner beats every
  rival at *every* setting of its parameter, so no selection was needed to get the result.

## Verification

- `test_ac15.py`: 13 tests pass (primitive faithfulness, the graded economics, the
  productivity definition, every gate re-derived from the frozen table, declared
  constants, protocol hashing).
- `audit_ac15.py`: passed — 64 rows, coverage exact, per-row invariants, no hash drift,
  protocol hashed, and all five gates recomputed from the saved table without simulating.
- `replay_ac15.py`: **6/6 exact** — six sampled rows (both learner seeds, both extremes,
  both consistency arms) re-simulated from scratch and compared field for field. The
  first run of this reported 0/6, entirely because JSON round-trips integer keys to
  strings in `chan_late`/`chan_productivity`; the values were identical. The comparison now
  normalises those keys rather than excusing the fields.
- `GRADE=0` equivalence with the unmodified AC12 harness: 6/6 identical state hashes
  (`AC15_ENGINEERING_v1.md`).

## Deviation, disclosed

The first final run used seeds **1800-1803**, not the protocol's declared **1900-1903**:
`ac15.py`'s entry point still carried a placeholder seed family from before the protocol
was written. `audit_ac15.py` caught it as a coverage mismatch. Handling, per the project's
freeze discipline:

1. The deviating run is preserved intact at `ac15_deviation_seeds1800_v1/` — not deleted
   and not overwritten.
2. **The protocol was not amended.** Changing a declared seed family after seeing the
   result would be exactly the retro-fitting the project forbids.
3. `ac15.py` was corrected to read `FINALS`; the only change was the seed list. No gate,
   arm, constant, endpoint or gate margin changed, and the correction restores conformance
   to the protocol rather than departing from it.
4. The corrected run is the final sample reported above.

The deviating run's own gate evaluation agrees with the final: G1 +0.200 (vs preserve) and
+0.282 (vs relinquish), G5 kept 1.000 / moved 0.400, G4 64/64, G3 exact. Two independent
seed families therefore give the same verdict, which is a robustness check the protocol did
not require.

## What this establishes, and what it does not

Establishes: under a graded access law, after an unannounced post-development move of one
channel, an organism whose per-slot maintenance decision is driven by its own realized
contact outcomes relinquishes the stale route while keeping the still-valid one, and
thereby achieves a higher late per-channel productivity than either state-blind extreme and
than any state-blind rival tested — with all arms viable, so the decision is not forced by
starvation.

Does not establish:

- **Re-acquisition.** The learner *relinquishes* the stale route; it does not learn a
  correct new one. Every keeping arm showed productivity 0.000 after the move, and the
  learner's moved-channel value (0.398) is consistent with blind search (~1/2), not with
  re-learning. The stronger claim is untested and is the natural next step.
- **Optimality.** The learner occupies the middle of two blind extremes; it is not shown to
  be optimal among all policies.
- Anything survival-level, and anything about experience, consciousness or autopoiesis.

## Artifacts

`ac15_results_v1/` (`pre_run_snapshot.json` with 12 source hashes including the protocol,
`rows.jsonl` written incrementally, `results.json`, `g2_rival_sweep.json`),
`ac15_deviation_seeds1800_v1/` (the disclosed deviating run), `ac15_engineering_v1/`,
`ac15.py`, `test_ac15.py`, `audit_ac15.py`, `replay_ac15.py`, `g2_ac15_sweep.py`,
`AC15_PROTOCOL_v1.md`, `AC15_ENGINEERING_v1.md`.
