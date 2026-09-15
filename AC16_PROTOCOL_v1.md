# AC16 protocol v1: re-acquisition — binding a correct route after the move

Frozen before the first final seed. Final seeds **2100-2103** (disjoint from AC15's
1900-1903, the AC15 deviation's 1800-1803, the AC13 replication seeds 3-8, and every
engineering seed 0-2). Runner: `ac16.py`. Audit: `audit_ac16.py`. Replay:
`replay_ac16.py`. Tests: `test_ac16.py`.

## The question AC15 left open

AC15's learner relinquished the stale route but never bound a correct new one: its
moved-channel productivity stayed at 0.398, i.e. blind-search level. The cause is
mechanical, and I found it before designing anything: in the frozen step the deposit path
— the only way the organism binds a key/port entry — is gated on `grow`, and the frozen
runner passes `grow = t<512`. Growth stops at development; AC15's intervention is at
t=1024. **Re-acquisition was switched off in the world AC15 used**, not attempted and
failed.

## Claim

With the growth window left open, after an unannounced post-development move of one
channel, an organism whose maintenance decision is driven **in both directions** by its
own realized contact outcomes — relinquishing a route that persistently fails, and
restoring maintenance when a route proves right — re-acquires a correct route for the
moved channel and **holds** it, while:

1. an organism that **keeps** the stale entry cannot bind anything at all, and
2. an organism that relinquishes **one-way** can bind a new route but cannot hold it.

Scope: behavioural and economic, not survival-level. No claim about consciousness,
experience or autopoiesis.

## Why the design discriminates (the frozen gate supplies the control)

`mem.deposit` is only reachable when `selected is None` — the organism may not bind a key
it already holds — and it binds the port that **just proved productive**
(`mem.deposit(memory, body, action, port, ...)`, value = the port of the matching
contact). Therefore:

- keeping a stale entry makes re-binding **impossible** for that key. Arms that keep are
  barred by the frozen gate itself; no scaffold or oracle arm is needed to demonstrate it;
- relinquishing makes re-binding possible **but** the AC12 register is one-way, so the
  newly bound entry is never renewed, lapses within its 64-tick life, and productivity
  settles at the intermediate level of a route that is live only part of the time (AC15
  measured 0.600 for this);
- restoring maintenance on a productive contact closes the loop, so the re-bound route
  survives.

A productive contact on a stored port is **proof** the port is right: the frozen gate can
only be passed by a match, and the deposit binds exactly the port that matched. A failed
contact is one noisy observation. That asymmetry is why the drop rule requires a streak
while the restore rule does not, and it is stated here as a design commitment rather than
a tuned parameter.

## World constants (declared)

| constant | value |
| --- | --- |
| access law | graded, miss yields a quarter (`GRADE=1`, from AC15) |
| material / fuel full yield | 64 / 32 |
| blind fallback | the frozen single coin, `port=int(coin)` (~1/2) |
| development window | 512 ticks |
| **growth** | **left open (`grow=True` throughout)** — AC16's single declared change |
| activation after development | `[True, True]`, the frozen runner's own post-development state |
| horizon | 4096 ticks (a lapsed entry plus a productive contact must both occur) |
| intervention | at t=1024 the **material** channel flips; fuel is unchanged |
| register read | majority of seven (`REGISTER_THRESHOLD=4`) |

No new world physics is introduced. The deposit path, the register, the payment and the
graded access law are all the frozen or AC15-verified machinery; the only new primitive is
the restore rule below.

## The restore primitive

Symmetric with the drop, and equally paid:

    on a productive contact for key k:            clear the register replicas for k's slot
    on STREAK_N consecutive unproductive contacts: set them

Both writes cost one energy and one material per replica and land in the same vulnerable
`traces[0,:126]` bits that the damage stream flips and the paid bank-0 repair fixes. The
restore is not free state and not a protected copy.

## Arms

| arm | what it is |
| --- | --- |
| `allocate_restore` | **the learner**: two-way — drop on an unproductive streak, restore on a productive contact |
| `allocate` | one-way relinquishment (AC15's learner) |
| `preserve` | never relinquish |
| `relinquish` | never renew |
| `random` | renew with p=0.5 per opportunity |
| `fixed_schedule` | renew every 2nd opportunity |
| `no_learning` | pays for the relinquishment without writing it (sham) |
| `fixed_period_1` | G-consistency: duty 1/1, must equal `preserve` |
| `streak_never` | G-consistency: unreachable drop threshold, must equal `preserve` |
| `restore_disabled` | G-consistency: the two-way arm with the restore rule off, must equal `allocate` exactly |

Rivals swept as families: fixed duty in {1,2,4,8}, random p in {0.25,0.5,0.75}, and the
learner's own drop threshold in {2,4,6,8}. **Disclosure:** all of these were run on
engineering seeds 0-2 before this protocol was written; that informed the endpoint choice
(per-channel productivity in the last eighth of the post-move run, plus the tick of
re-binding) and the gate margins. Engineering seeds are excluded from the final sample.

## Endpoints

Primary: **moved-channel productivity in the final eighth of the post-move run**
(t = 3584..4096), per individual, averaged over the sample.

Secondary: the **tick of re-binding** (first tick at/after the move at which a *correct*
stored entry exists for the moved key); kept-channel productivity (must not degrade);
relinquishments and restorations; final stored routes versus the true mapping; per-eighth
productivity trajectory (the mechanism, since it shows the route's life history);
survival and planned-denominator activity.

## Gates, prespecified

- **G1 (the claim):** the learner's final-eighth moved-channel productivity is at least
  **0.90** — i.e. it holds a correct route, not merely samples it.
- **G2 (one-way is not enough):** the learner exceeds one-way `allocate` by at least
  **0.25** on that endpoint.
- **G3 (keeping cannot re-bind):** `preserve` and `no_learning` are at most **0.05**, and
  neither ever records a re-binding tick.
- **G4 (the valid route is not sacrificed):** the learner's kept-channel productivity is at
  least **0.95**.
- **G5 (consistency, exact):** `fixed_period_1` and `streak_never` reproduce `preserve`,
  and `restore_disabled` reproduces `allocate` — **same `state_hash`** in each case.
- **G6 (scope):** every arm completes the horizon.
- **G7 (not beaten by a blind rival):** the learner is not beaten on the primary endpoint by
  any fixed duty cycle or random configuration.

Failure of G1-G5 or G7 falsifies the claim. G3 is the causal control and cannot be passed
by doing more of anything: an arm that keeps its entry is barred from binding by the frozen
deposit gate.

## Sample and analysis

4 seeds x 2 histories = 8 individuals per arm, 10 arms. Seeds are the replication unit;
histories are repeated measures. Report the learner's prespecified configuration
(drop-threshold 6) as the headline and the family sweep as post-hoc secondary with the
selection caveat. Thresholds may not be changed after the final run; a failed gate is
recorded and the design superseded by a new version.

## Known limitations, stated before running

- Leaving the growth window open also leaves the region-W birth loop available. The frozen
  `grow` flag gates both, and I do not separate them; the change is therefore "the
  developmental window is not closed", not "deposits only".
- The restore rule fires on a *single* productive contact because such a contact proves the
  port. If a world allowed a productive contact with a wrong port, this would be unsound;
  the frozen gate does not.
- The claim is about re-acquiring a route for a **moved** channel, not about learning the
  world's structure. Nothing here tests whether the organism could acquire a route for a
  channel it never held.
