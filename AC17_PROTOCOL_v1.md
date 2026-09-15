# AC17 protocol v1: re-acquisition, with gates shaped like the claim

Frozen before the first final seed. Final seeds **2300-2303** (disjoint from AC16's
2100-2103, the AC15 deviation's 1800-1803, AC15's 1900-1903, the AC13 replication seeds
3-8, and every engineering seed 0-2). Runner: `ac17.py`, building on the frozen `ac16.py`.
Audit: `audit_ac17.py`. Replay: `replay_ac17.py`. Tests: `test_ac17.py`.

## Why a new version, stated plainly

AC16 v1 is **falsified and remains falsified**: its G2 asked for a mean margin of +0.25 over
one-way relinquishment and measured +0.2437, while the learner was strictly better in 8/8
individuals. Nothing here amends that. What AC16's G2 measured was how *often* one-way gets
lucky by re-binding repeatedly — a seed-dependent quantity that has nothing to do with the
claim, which is categorical: a one-way rule **cannot hold** a re-bound route; a two-way rule
**can**.

AC17 therefore declares **categorical and dominance gates**, chosen on that principle and
written down before the run. They are *stricter* than AC16's mean margin, not laxer: every
individual must satisfy them. The world, arms, horizon, intervention and primitive are
unchanged from AC16; only the seeds and the gates' shape differ, plus one new arm.

## Claims

**Claim 1 (categorical).** In the graded world with the growth window open, after an
unannounced post-development move of the material channel, an organism whose maintenance
decision is driven in both directions by its own realized contact outcomes **holds a correct
route for the moved channel in every individual** (final-eighth productivity >= 0.90), and
**strictly beats one-way relinquishment in every individual** — while never sacrificing the
still-valid channel.

**Claim A (structural, and therefore the strongest kind of prediction here).** The
relinquishment direction is **necessary**: an arm with the restore rule but no drop rule can
never free the key, so the frozen deposit gate (`selected is None`) bars it from binding at
all. It must score **exactly 0.000** on the moved channel with **no re-binding tick** in
every individual. This is predicted from the frozen code, not from prior measurement.

Scope: behavioural and economic, single-channel move, not survival-level, and no claim about
consciousness, experience or autopoiesis.

## Explicitly out of scope, and why (decided by measurement before this protocol)

**The both-channels-move world is not claimed.** Engineering measured the crude
always-relinquish arm there at 0.93 mean (ch0 1.000, ch1 0.857) against the learner's 0.75:
an arm that never renews is always free to re-bind the current correct port, so the two-way
rule adds nothing in that world. Rather than reframe the claim to fit, the world is excluded
and the measurement recorded (`AC17_ENGINEERING_v1.md`). This is the same practice that
killed the AC16 design's third claim before it reached a protocol.

## World constants (unchanged from AC16 except the seeds)

| constant | value |
| --- | --- |
| access law | graded, miss yields a quarter |
| growth | open throughout (`grow=True`) |
| activation after development | `[True, True]` |
| development window | 512 ticks |
| horizon | 4096 ticks |
| intervention | at t=1024 the **material** channel flips; fuel unchanged |
| register read | majority of seven |

## Arms

| arm | what it is |
| --- | --- |
| `allocate_restore` | **the learner**: drop on an unproductive streak, restore on a productive contact |
| `allocate` | one-way relinquishment (the rival Claim 1 is stated against) |
| `restore_only` | **Claim A**: restore rule, no drop rule |
| `preserve` | never relinquish |
| `no_learning` | pays for the relinquishment without writing it (sham) |
| `relinquish` | never renew |
| `random`, `fixed_schedule` | blind rivals: renew with p=0.5, or every 2nd opportunity |
| `fixed_period_1` | consistency: duty 1/1, must equal `preserve` |
| `streak_never` | consistency: unreachable drop threshold, must equal `preserve` |
| `restore_disabled` | consistency: the learner with the restore rule off, must equal `allocate` |

## Endpoints

Primary: **moved-channel productivity in the final eighth** (t = 3584..4096), per individual.
Secondary: kept-channel productivity; the tick of re-binding; relinquishments and
restorations; final stored route versus the true mapping. Aggregate income is **not** an
endpoint (confounded by the observation depending on whether an entry exists).

## Gates, prespecified

- **G1 (Claim 1, categorical):** the learner's moved-channel final-eighth productivity is
  >= 0.90 in **every** individual.
- **G2 (dominance, categorical):** the learner strictly exceeds one-way `allocate` in
  **every** individual.
- **G3 (barred, categorical):** every keeping arm (`preserve`, `no_learning`,
  `fixed_schedule`, `random`) scores **exactly 0.000** on the moved channel and records
  **no** re-binding tick, in every individual.
- **G4 (no sacrifice, categorical):** the learner's kept-channel productivity is >= 0.95 in
  every individual.
- **G5 (consistency, exact):** `fixed_period_1` and `streak_never` each reproduce `preserve`,
  and `restore_disabled` reproduces `allocate` — same `state_hash`, in every individual.
- **G6 (Claim A, categorical, structural):** `restore_only` scores exactly 0.000 on the moved
  channel with no re-binding tick, in every individual.
- **G7 (rival competence, categorical):** no blind rival (`fixed_schedule`, `random`, or any
  swept duty/period configuration) reaches 0.90 in any individual.
- **G8 (scope):** the learner, `allocate`, `preserve`, `no_learning`, `restore_only`, both
  consistency arms and `restore_disabled` complete the horizon in every individual. The
  crude `relinquish` extreme is excluded from this gate by declaration: it is not a
  comparator for the claim, and AC16 showed it can die. Its survival is reported, not gated.

Failure of G1-G7 falsifies the claim. Any gate failing on even one individual falsifies it:
that is what "categorical" is bought with.

## Sample and analysis

4 seeds x 2 histories = 8 individuals per arm, 11 arms, 88 rows. Seeds are the replication
unit; histories are repeated measures. The learner's configuration (drop threshold 6) is
prespecified, not chosen from its family. Report every individual's value, not only means.
Thresholds may not be changed after the final run; a failed gate is recorded, and any
successor version declares its gates afresh on fresh seeds.

## Known limitations, stated before running

- Opening the growth window also leaves the region-W birth loop available; the frozen `grow`
  flag gates both and they are not separated.
- The restore fires on a **single** productive contact because such a contact proves the
  port. If a world allowed a productive contact with a wrong port this would be unsound; the
  frozen gate does not.
- Claim A's prediction depends on `mem.deposit` requiring `selected is None`. If a future
  version of the deposit path relaxed that, Claim A would need restating.
