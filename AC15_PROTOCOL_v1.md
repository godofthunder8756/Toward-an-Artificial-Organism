# AC15 protocol v1: acquired allocation under a graded access law

Frozen before the first final seed. Final seeds **1900-1903** (disjoint from every
previous study, from the AC15 engineering seeds 0-2, and from the AC13 replication
seeds 3-8). Runner: `ac15.py` (collect path, `ac15_results_v1/`). Audit:
`audit_ac15.py`. Replay: `replay_ac15.py`. Tests: `test_ac15.py`.

## Claim, and its exact scope

Under a **graded access law** — a wrong stored port costs a declared fraction of the
yield instead of all of it — after an **unannounced post-development move of one
channel** (the material channel; the fuel channel stays valid), an organism whose
per-slot maintenance decision is driven by its own realized contact outcomes keeps the
still-valid route and relinquishes the stale one, earning a higher late per-channel
productivity than either state-blind extreme (keep both, drop both) and than any
state-blind fixed duty cycle at matched spending.

**Scope, stated before running.** This is a **behavioural and economic** claim. It is
**not** survival-level: engineering showed all arms viable, and the protocol therefore
requires it (G4). It says nothing about consciousness, experience, or autopoiesis. It
does not claim the organism is optimal, nor that it beats dropping everything — it
cannot, and `relinquish` is retained precisely to demonstrate that the *other* blind
extreme fails, which is what makes the middle honest.

## Why the graded access law is a prerequisite, not a convenience

The AC11/AC12/AC13 line failed structurally: with the frozen hard gate, a stale entry
earned **exactly zero**, starvation stopped renewal spending, and the decision was
downstream of an economics that had already fixed the outcome (`AC13_REPLICATION_v1.md`).
`ac15.py` grades the law: a miss takes a quarter of the yield (material 64 -> 16, fuel
32 -> 8), expressed entirely through the intake variables the frozen balance law already
carries, so no conservation law is touched. Verified: `GRADE=0` reproduces the
unmodified AC12 harness byte for byte, 6/6 state hashes.

Measured per contact with the action forced (the only unconfounded economic evidence,
since a stored entry changes the observation and hence which actions are chosen):
correct 64, stale-kept **16**, blind **36** (material). So dropping a stale route
improves yield 2.25x **and** keeping it is survivable — a decision with a consequence in
which neither option is fatal.

## World constants (all declared, none tuned to the hypothesis)

| constant | value |
| --- | --- |
| access law | graded, miss yields a quarter (`GRADE=1`) |
| material / fuel full yield | 64 / 32 |
| material / fuel miss yield | 16 / 8 |
| blind fallback | the frozen single coin, `port=int(coin)` (matches ~1/2) |
| development | 512 ticks |
| horizon | 2048 ticks |
| intervention | at t=1024 the **material** channel flips; fuel is unchanged |
| register read | majority of seven (`REGISTER_THRESHOLD=4`) |

## Arms

| arm | what it is |
| --- | --- |
| `allocate` | **the learner.** Per-slot relinquishment after `STREAK_N=6` consecutive unproductive contacts on that key, paid per replica, written into the vulnerable register. |
| `preserve` | never relinquish (the frozen decay-urgency rule's behaviour) |
| `relinquish` | always relinquish (the other state-blind extreme) |
| `random` | relinquish each slot with p=0.5 per opportunity |
| `fixed_schedule` | relinquish every `FIXED_PERIOD=2` opportunities, spending-matched |
| `no_learning` | pays for the relinquishment write but does not write it (sham) |
| `fixed_period_1` | consistency check: duty 1/1, must equal `preserve` |
| `streak_never` | consistency check: `STREAK_N=10**6`, must equal `preserve` |

Rivals are swept as families: fixed duty `FIXED_PERIOD` in {1,2,3,4,8}, random
`RANDOM_P` in {0.25,0.5,0.75}, and the learner's own family `STREAK_N` in {2,4,6,8}.
**Disclosure:** the sweep was run on engineering seeds 0-1 before this protocol was
written, and it informed the endpoint choice (per-channel productivity) and the gate
margins. Engineering seeds are excluded from the final sample. The learner's final
configuration is the one the primitive was specified with (`STREAK_N=6`), **not** the
best member of its own sweep — selecting the learner's best while comparing against the
rivals' fixed settings is exactly the error that falsified AC11.

## Endpoints

Primary: **mean late per-channel productivity** = (productivity on the kept channel +
productivity on the moved channel)/2, measured from t=1024 to the end, per individual,
averaged over the sample.

Secondary: per-channel productivity (kept / moved separately) — the mechanism, since it
shows *which* route was kept; final `demand` per region; number of relinquishments;
survival and planned-denominator activity.

Explicitly **not** an endpoint: aggregate late income. It is confounded (an entry's
presence changes the observation, so arms differ in how often they attempt contacts at
all). Reported for completeness only, never used for the claim.

## Gates, prespecified

- **G1 (the claim):** the learner's mean late per-channel productivity exceeds
  `preserve` by at least **0.08** and `relinquish` by at least **0.08**.
- **G2 (rival competence):** the learner at its prespecified `STREAK_N=6` is not beaten
  by any state-blind fixed duty cycle (periods 1-8) nor by random at p in {0.25,0.5,0.75}.
- **G3 (consistency, must reproduce exactly):** `fixed_period_1` and `streak_never` are
  each *equal to* `preserve` — same mean, same final `demand`, same `state_hash`. This is
  the check that caught AC11's failure; here it must pass.
- **G4 (scope):** every arm completes the full horizon (no deaths). If any arm dies the
  claim is relabelled survival-level and G1 is re-reported with planned denominators.
- **G5 (mechanism):** the learner's productivity on the **kept** channel is at least
  **0.95** while its productivity on the **moved** channel exceeds **0** — i.e. it kept
  what was valid and did not keep what was not.

Failure of any of G1, G2, G3, G5 falsifies the claim. This is a two-sided design: G5
can fail by keeping the stale route (like `preserve`) *or* by dropping the valid one
(like `relinquish`), so "the learner wins" cannot be reached by simply dropping more.

## Sample and analysis

4 seeds x 2 developmental histories = 8 individuals per arm, 8 arms. Seeds are the
replication unit; histories are repeated measures. Report the learner's prespecified
configuration as the headline; report the family sweep as post-hoc secondary with the
selection caveat stated. No threshold may be changed after the final run; if a gate
fails, the record says so and the design is superseded by a new version, exactly as
`AC11_PROTOCOL_v1.md` was marked UNFROZEN AND FALSIFIED.

## Known limitations, stated before running

- The horizon is 2048 ticks and the entry life is 64 ticks, so renewal is continuously
  required; the protocol does not test re-acquisition of a **correct** port after the
  move, only relinquishment of the stale one. Every engineering arm that kept its entries
  showed productivity exactly 0.000 afterwards, i.e. no re-learning. That is the stronger
  claim and it is explicitly out of scope here.
- The learner's advantage is a difference in mean productivity of order 0.1-0.2, on 8
  individuals. Report exact per-individual values, not just means.
- `relinquish`'s kept-channel productivity (its loss) is the design's guard against a
  one-sided result; if it ever *matches* the learner, the middle is not being occupied
  and the claim fails regardless of G1.
