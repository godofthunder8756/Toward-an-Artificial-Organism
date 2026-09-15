# AC18 results v1: the claim passes, on a gate declared before the run

Frozen final sample, seeds **2500-2503** x 2 histories = 8 individuals per arm, 11 arms,
88 rows, 4096 ticks, single-channel intervention at t=1024. Declaration:
`AC18_PROTOCOL_v1.md`, hashed into `ac18_results_v1/pre_run_snapshot.json` before the run.
Runner: `ac18.py` driving the frozen `ac17.run` unchanged.

## Verdict

| gate | requirement | measured | verdict |
| --- | --- | --- | --- |
| G1 | learner's **worst** individual >= 0.90 on the moved channel | **1.000 (all 8)** | **PASS** |
| G2 | one-way `allocate`'s **worst** individual < 0.90 | **0.429** | **PASS** |
| G3 | keeping arms exactly 0.000, no re-binding tick, every individual | holds | **PASS** |
| G4 | learner's kept channel >= 0.95 every individual | 1.000 | **PASS** |
| G5 | three consistency equalities exact (`state_hash`) | all hold | **PASS** |
| G6 | `restore_only` exactly 0.000, no re-binding (structural) | holds | **PASS** |
| G7 | no blind rival or swept configuration reaches 0.90 | 0.000 | **PASS** |
| G8 | declared arms complete the horizon | 8/8 each | **PASS** |

**G1 and G2 together are the claim, and it passes.** This is the first time the
re-acquisition claim has cleared a gate declared before the run — AC16 and AC17 were both
falsified by gate *shape*, not by the mechanism, and neither is amended by this result.

## The separation, per individual

Moved-channel productivity in the final eighth, every individual:

| arm | values (sorted) | worst |
| --- | --- | ---: |
| `allocate_restore` (two-way) | 1.000 x8 | **1.000** |
| `allocate` (one-way) | 0.429, 0.429, 0.636, 0.636, 0.778, 0.778, 0.800, 0.800 | 0.429 |
| `restore_disabled` (control) | identical to one-way | 0.429 |
| `relinquish` (crude) | 0.444, 0.444, 0.500, 0.500, 0.667, 0.667, 0.714, 0.714 | 0.444 |
| `preserve`, `no_learning`, `random`, `fixed_schedule`, `restore_only`, `fixed_period_1`, `streak_never` | 0.000 x8 each | 0.000 |

The learner is **invariant** at 1.000 while one-way ranges 0.429-0.800 and the crude
always-relinquish arm 0.444-0.714. Both rivals re-bind routes; neither can *hold* one, and
their values vary with the luck of re-binding timing. The learner's constancy is the
mechanism's signature: a route that is restored whenever it proves right does not depend on
luck.

Note what the gate does **not** require: the learner need not beat one-way on every individual
(AC17's unsatisfiable demand — on some individuals one-way also reaches the ceiling). It
requires that one-way cannot *guarantee* holding, which is what the claim actually says.

## The necessity result, now confirmed on three seed families

- **drop-only** (`allocate`): binds a route but cannot hold it — 0.429-0.800 here, 0.462-1.000
  in AC17, 0.636-0.889 in AC16.
- **restore-only** (`restore_only`): exactly 0.000 with no re-binding tick, because it never
  relinquishes and so never frees the key — the frozen deposit gate requires
  `selected is None`. Predicted from the code, then measured.
- **both directions** (`allocate_restore`): holds in every individual on every seed family
  (1.000 x8 here, x8 in AC17).

So the two-way rule is **necessary and sufficient** within this machinery: each direction
alone fails, and together they hold.

## What this closes

The project's own open item was "a controller that *acquires* the need to allocate or
relinquish maintenance resources under an intervention chosen after development, with no
protected copy and no externally fixed correct state" — the item AC11 attacked and lost to
(its own pre-run controls falsified it), and which AC12 and AC13 each failed on structural
grounds. It is now addressed, with the following honest scoping:

- **Established:** after an unannounced post-development move of one channel, in a graded
  access law, an organism whose per-slot maintenance decision is driven in both directions by
  its own realized contact outcomes **relinquishes the stale route and holds a re-acquired
  correct one in every individual**; keeping arms are structurally barred from re-binding at
  all; one-way relinquishment never guarantees holding; the valid channel is never sacrificed;
  no blind rival reaches the bar; and both directions are individually necessary.
- **Not established:** survival-level claims (the claim is behavioural and economic — every
  declared arm completes the horizon, so nothing here is a matter of life and death);
  optimality; generalization to worlds where **both** channels move (measured and excluded in
  AC17's engineering, where the crude always-relinquish arm already reaches 0.93); and
  anything about consciousness, experience or autopoiesis.

## Verification

- `audit_ac18.py`: passed — 88 rows, coverage against the declared seeds, per-row invariants,
  18 source hashes with no drift, the three G5 equalities, and all eight gates recomputed from
  the saved table **without simulating**.
- `replay_ac18.py`: **8/8 exact** — eight sampled rows across the learner, one-way, keeping
  arms, both consistency arms, `restore_only` and `relinquish`, re-simulated from scratch and
  compared field for field.
- `test_ac18.py`: 15 tests, including a satisfiability test on the gate itself (the bar is
  below the ceiling, so the separation is well posed) and a disjointness test that the seed
  family has not been used before.
- Full suite: **149 tests pass**.
- All tools hashed up front: protocol, runner, audit, replay and test file are all inside the
  frozen snapshot, with no post-freeze edit this time.

## The process lesson this sequence produced

Three consecutive versions of this mechanism were affected by gate shape: AC16's mean margin
over a partially-succeeding rival (falsified by 0.006 while the learner dominated 8/8
individuals); AC17's strict per-individual dominance (unsatisfiable at the ceiling — 2 of 8
individuals tied at 1.000); AC18's separation of worst cases (passes, and could have failed
if one-way's worst had cleared 0.90). The rule that produced the passing gate is the one worth
carrying: **classify the claim first** — "cannot hold" is a worst-case statement, so it is
tested as a separation of minima; "worse on average" needs a margin with a stated
justification; "better everywhere" is dominance and must exempt the ceiling. Both earlier
gates were avoidable at declaration time, and both falsifications stand permanently.

## Artifacts

`ac18_results_v1/` (snapshot with 18 hashes, `rows.jsonl`, `results.json`), `ac18.py`,
`test_ac18.py`, `audit_ac18.py`, `replay_ac18.py`, `AC18_PROTOCOL_v1.md`. The world, arms and
simulation are AC17's (`ac17.py`, `ac16.py`, `ac15.py`, `ac12.py` and the frozen AC9/AC4/AC5
machinery), unchanged.
