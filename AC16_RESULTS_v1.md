# AC16 results v1: re-acquisition — the claim as specified is FALSIFIED, by 0.006

Frozen final sample, seeds **2100-2103** x 2 histories = 8 individuals per arm, 10 arms,
80 rows, 4096 ticks, intervention at t=1024. Declaration: `AC16_PROTOCOL_v1.md`, hashed
into `ac16_results_v1/pre_run_snapshot.json` before the run. Primitive and runner:
`ac16.py`.

## Verdict

| gate | requirement | measured | verdict |
| --- | --- | --- | --- |
| G1 | learner's final-eighth moved-channel productivity >= 0.90 | **1.000** | **PASS** |
| G2 | learner exceeds one-way `allocate` by >= 0.25 | +0.2437 | **FAIL** |
| G3 | `preserve` and `no_learning` <= 0.05 and never re-bind | 0.000, no re-binding recorded | **PASS** |
| G4 | learner's kept-channel productivity >= 0.95 | 1.000 | **PASS** |
| G5 | three consistency equalities, `state_hash` exact | all three hold | **PASS** |
| G6 | every arm completes the horizon | `relinquish` dies 4/8 | **FAIL** |
| G7 | not beaten by a blind rival | rivals all 0.000 | **PASS** |

The protocol states that failure of G1-G5 or G7 falsifies the claim. **G2 failed, so the
claim as specified is falsified.** I did not amend the protocol, and I did not move the
threshold: the margin was declared at +0.25 before the run and the measurement is +0.2437,
short by 0.006. G6 failed too, but G6 is deliberately not in the falsification list — it is
a scope note, and the only arm that dies is the crude always-relinquish extreme, which the
claim does not depend on.

## What the data actually shows

| arm | alive | kept | moved | final-eighth moved, per individual |
| --- | ---: | ---: | ---: | --- |
| `allocate_restore` (two-way) | 8/8 | 1.000 | **1.000** | 1.000 x8 |
| `allocate` (one-way) | 8/8 | 1.000 | 0.756 | 0.800, 0.800, 0.889, 0.889, 0.700, 0.700, 0.636, 0.636 |
| `preserve` | 8/8 | 1.000 | 0.000 | 0.000 x8 |
| `no_learning` (sham) | 8/8 | 1.000 | 0.000 | 0.000 x8 |
| `fixed_schedule`, `random` | 8/8 | 1.000 | 0.000 | 0.000 x8 |
| `relinquish` | 4/8 | 0.375 | 0.694 | — (dies in 4 of 8) |
| `restore_disabled` (G5) | 8/8 | 1.000 | 0.756 | identical to `allocate` |
| `fixed_period_1`, `streak_never` (G5) | 8/8 | 1.000 | 0.000 | identical to `preserve` |

The **categorical** pattern is exactly as predicted, and it is a three-way separation:

1. **Keeping cannot re-bind at all.** `preserve`, `no_learning`, `fixed_schedule`, `random`
   never record a re-binding tick and score exactly 0.000 on the moved channel. This is not
   a behavioural tendency but a structural bar: the frozen deposit gate requires
   `selected is None`, so an organism holding a stale entry for that key cannot bind
   anything. The control is supplied by the frozen code, not by a scaffold arm.
2. **One-way relinquishment can bind but not hold.** `allocate` and `relinquish` do
   re-bind — at ticks 1139-1309, just after the stale entry lapses — but the one-way
   register means the re-bound route is never renewed, so it lapses again within its
   64-tick life and is re-bound repeatedly. They therefore score 0.636-0.889.
3. **The two-way rule holds what it binds.** `allocate_restore` scores **1.000 in all eight
   individuals**, which is only possible with a live, correct stored route on every
   contact, and it restores maintenance 3.2 times on average after one relinquishment.

The learner is **strictly better than one-way on every one of the eight individuals**
(+0.111 to +0.364). It is the *mean* margin, diluted by the seeds where one-way happens to
re-bind frequently, that fell 0.006 short of the declared threshold.

## Why the gate failed, stated plainly

The +0.25 margin was an engineering-informed number, not a derived one, and it is the wrong
kind of test for this claim. The claim is categorical — one-way *cannot hold* a route, a
two-way rule *can* — and a margin over a rival that partially succeeds by re-binding
repeatedly measures how *often* one-way gets lucky, which varies by seed (0.636 to 0.889)
and has nothing to do with whether holding is possible. A dominance criterion (strictly
better in every individual, which holds 8/8) or a categorical one (holding >= 0.90 in every
individual, which holds at 1.000 x8 for the learner against 0.000 x8 for every keeping arm)
tests the claim as stated.

That diagnosis is **not** a licence to re-run AC16 with a better-chosen threshold: choosing
the gate after seeing the result is exactly the practice this project's protocol discipline
exists to prevent. The correct route is a new version with its gates declared in advance on
fresh seeds, and I am recording it that way rather than retrofitting this one.

## Verification

- `audit_ac16.py`: passed — 80 rows, coverage against the protocol's declared seeds,
  per-row invariants, no hash drift, all three G5 equalities recomputed, all seven gates
  recomputed from the saved table without simulating.
- `replay_ac16.py`: **7/7 exact** — seven sampled rows across the learner, both extremes,
  both consistency arms and the restore-disabled control, re-simulated from scratch and
  compared field for field.
- `test_ac16.py`: 17 tests pass. Two of them are regression tests that assert the
  *recorded* gate failures (G2 stays below +0.25 with per-individual dominance; only
  `relinquish` fails to complete), so any future code change that alters the record is
  caught rather than silently absorbed.
- Conservation: the frozen identity
  `spent_m == writes + 4*(W_birth + C_birth) + 2*B_birth` holds exactly with the restore
  booked, so the new write is paid through the existing law.

## Disclosed bookkeeping gap

`test_ac16.py` was authored *after* the final run started, so it is not in the frozen
pre-run snapshot. It cannot affect the run (tests only verify), it is committed alongside,
and its checks pass. `audit_ac16.py` reports this on every run as a warning rather than
letting it pass silently. The runner, the protocol and all frozen dependencies are hashed.

## What this establishes, and what it does not

Establishes: with the growth window open, re-binding a route after the move is **possible
only for an organism that relinquishes the stale one** (the frozen deposit gate bars every
keeping arm, 0.000 in all 8 individuals); a one-way relinquishment binds but cannot hold
(0.636-0.889); and a two-way outcome-driven rule — relinquish on a failing route, restore
maintenance when a route proves right — **holds a correct route at 1.000 in every
individual**, with the valid channel never sacrificed. The restore is paid, lands in the
same vulnerable bank as the drop, and its own control (`restore_disabled`) reproduces the
one-way arm exactly.

Does not establish: the claim *as specified* (G2 failed). Also not established: optimality,
any survival-level reading (`relinquish` dies 4/8, and the other arms' viability is a
property of this world's graded law), and anything about consciousness, experience or
autopoiesis.

## Next version (declared here, to be protocolled and run on fresh seeds)

AC17 should test the same mechanism with gates that match the claim's shape: (a) the
learner holds a correct route in **every** individual (>= 0.90 each) while every keeping arm
scores **exactly 0.000** and records no re-binding; (b) the learner strictly dominates
one-way in every individual; (c) the three existing consistency equalities. No margin over
a partially-succeeding rival. Fresh seeds, protocol hashed first, one-way and keeping arms
unchanged.

## Artifacts

`ac16_results_v1/` (snapshot, `rows.jsonl`, `results.json`), `ac16_engineering_sweep.json`
(rival sweep on engineering seeds), `ac16.py`, `test_ac16.py`, `audit_ac16.py`,
`replay_ac16.py`, `AC16_PROTOCOL_v1.md`.
