# AC107 engineering v1 — a minimal cause-estimator discriminates the two causes and survives where the reactive baseline and the longer counter each fail

2026-09-22. **Engineering report, not a study.** No protocol, no `pre_run_snapshot.json`, no
disjoint final seed family, no freeze. Seeds 0-7 (16 individuals). This is K5's deliverable
(task t_ba0b451e): the estimator K4 said was identifiable, implemented against the fixed
observation interface, plus the rivals the card names, all verified against the frozen/engineering
sources in the repo. A positive result here unblocks K6 (a confirmatory protocol) only on the
question of *feasibility*; it is not itself a frozen claim.

---

## 1. The question, and the answer

**Question (K5):** does a minimal estimator, supported by the K4 identifiability analysis,
discriminate the causes and do something the reactive baseline does not?

**Answer: yes on discrimination, yes on "does something", with one sharply bounded redundancy.**

- The estimator reads the correct cause at decision times in **16/16 move and 16/16 cut
  individuals** (0 mistakes, measured not assumed — §3).
- It does something no single fixed threshold can do: it survives **both** worlds by using the
  *right* threshold in each. The reactive baseline (threshold 6) dies in the cut (seed 4); the
  longer counter (threshold 24) dies in the move (seeds 1, 2, 4). The candidate survives all 16
  (§4). That is the two-sided discriminator C1 §5 predicted, and AC106 could not have produced it
  because its update rule was confounded.
- The one redundancy: the candidate's *proactive renewal* consumption adds nothing over the frozen
  reactive renewal (the longer-counter rival keeps the entry alive through the cut without it). This
  is exactly the C1 §7 anticipated outcome, and it is reported, not hidden (§6).

---

## 2. What changed from AC106 (the two fixes the card requires)

AC106 (db0ef2f) failed because its estimator read `productive` alone. Two defects, both fixed here:

**Fix 1 — the discriminator reads the organism's own memory (K1 P2, K4 §9).** AC106's rule fired
`e = E_machinery` on any productive contact that followed a failure, so a blind re-bind of a dropped
stale route was mislabelled as "productivity resumed". AC107 forwards the `(bound, used_held)`
observation and gates every conclusion on it:

| observation (per channel-1 contact) | conclusion |
|---|---|
| `bound=1 & used_held=0` | **E_machinery** — the read is suppressed while the entry is still bound (the cut signature; fires on *every* in-window contact, blind failure and blind success alike) |
| `used_held=1 & productive=0` | **E_world** — F1: a held entry failed, so the entry is stale |
| `bound=0 & productive=1` | **E_world** — a blind re-bind after a drop (re-acquisition) |

`bound = o.memory.read(1) is not None` (the organism's own introspection, *not* shimmed by the cut);
`used_held = selected is not None` (the shimmed retrieval result, already computed at `ac9.step`
line 86 and merely forwarded — an interface change, not a new sensor).

**K4's F2 ("read `bound` at the productive resumption") is deliberately *not* implemented as a
separate streak-gated rule.** It is subsumed by the first rule above (`bound=1 → E_machinery` is
already established on the first in-window contact) and the third (`bound=0 → E_world`). A
streak-gated "resume after a run of failures" is *ambiguous*: after a relinquishment the frozen Gray
reset (5→0 = 21 replicas) is refused at W=2 (the AC100 "dear Gray reset"), so the streak stays > 0
and a re-bound entry's yield would be mislabelled as "resumed without re-binding" — the K1 confound
reappearing through the streak. This was found by running the first build and reading the `move`
trajectory's `bel_events` (`machinery_resume` firing at the post-re-bind yield), not by inspection.

**Fix 2 — the longer-window rival has its own counter (K1 P1).** AC106's r4 was
`BeliefAlloc(estimate=False, threshold=HOLD_N)` with `HOLD_N == STREAK_N == 6` on the 3-bit Gray
streak, which saturates at 7 — so "a raw counter with a bigger threshold" was never implemented. r4
here carries a per-key host-integer counter with `HOLD_N = 24` (representable where the streak is
not), counts all failures, makes no attribution, and does no proactive renewal. It receives the same
`(bound, used_held)` interface (matched), but is state-blind by construction.

The scramble arm is also fixed (K1 P5): the *read* of e is forced to E_world, while the estimate's
paid *writes* and the proactive-renewal code path are left intact — it runs the identical
discriminator+write code with only the read forced. It is a read-only causal-role control, not
AC106's three-way confound (read + writes + proactive all removed). The estimate spend is
byte-matched to the candidate's on the 8/16 hold-individuals; on the re-bind individuals the
scramble writes the bit a second time (the discriminator's `world_rebind` rule at re-acquisition),
which is a downstream consequence of the trajectory the forced read induces, not a spend suppression.

---

## 3. Discrimination is measured at decision times, not the horizon (K1 P3)

Per individual, the estimator's own maintained value is read from the body at the decision:

- **move:** at the first relinquishment (`bel_at_first_drop`), e reads **E_world (1) in 16/16**.
- **cut:** at the window end (`bel_at_cut_end`), e reads **E_machinery (0) in 16/16**.
- **mistakes** (post-intervention `bel_events` writing the wrong label): **0** across all 32
  individuals (the field exists to catch a residual confound; it catches none).
- **latency** (`first_correct_tick − CUT_TICK`): the estimate reaches the correct value on the first
  in-window channel-1 contact, i.e. **~13-46 ticks after the intervention**, dominated by how soon
  the program chooses to contact channel 1 after t=8192 — not by any discrimination delay.

The horizon value alone (`bel_at_horizon`) would have reported the same 16/16 here, but it is the
wrong read in principle and AC106's errata P3 documents why; AC107 records both and gates on the
decision-time values.

---

## 4. The two-sided discriminator is survival-relevant (the headline)

Survival, per arm and condition, seeds 0-7 (16 individuals):

| arm | mechanism | cut (E_machinery) | move (E_world) |
|---|---|---|---|
| **candidate** | estimate e, right threshold per cause | **16/16 survive, 0 relinquish** | **16/16 survive, drop @6** |
| r2 | Gray streak, threshold 6 | 14/16 — **dies seed 4** (relinquishes a valid route) | 16/16 |
| r4 | raw counter, threshold 24 | 16/16 survive (holds) | **13/16 — dies seeds 1, 2, 4** (holds the stale route too long) |
| scramble | read forced E_world | 14/16 — **dies seed 4** | (same as r2) |
| r1 | reactive, threshold 1 | survives (drops + re-binds) | survives |

The candidate is the **only arm that survives both worlds**. Each rival fails in exactly the world
its fixed threshold is wrong for:

- **r2 (6) is too eager** in the cut: on the priority-corner seed 4 the streak reaches 6 during the
  outage, relinquishes a *valid* route (deposit gated off post-development → permanent loss), and
  the organism dies at 8443. The candidate reads E_machinery on the first in-window contact, holds,
  and survives. This is C1 §8 P1, confirmed per individual.
- **r4 (24) is too slow** in the move: on seeds 1, 2, 4 it holds the *stale* route (never reaches 24
  consecutive failures before the material collapse) and dies at 8444-8447. The candidate reads
  E_world on the first held-entry failure, drops at 6, re-binds, and survives. The longer threshold
  trades the cut-failure for a move-failure.
- **scramble** (read forced E_world) reproduces r2's cut death — the *read* of the maintained bit is
  causal (C1 §8 P4), and its estimate writes are **not suppressed** (the AC106 three-way-confound fix:
  matched to the candidate's byte-for-byte on the hold-individuals, §7).

The discriminator's value is precisely that **one maintained bit selects the correct behaviour in
each world**, which no single fixed threshold can express. This is the "flexibly consumed" bar from
C1 §5, met at the level of survival.

---

## 5. Per-measurement reporting (the card's list, each separate)

- **Mistakes:** 0 (defined in §3; the field is non-trivial — AC106's build would have recorded 3 on
  seed 0 alone).
- **Latency:** first correct estimate 13-46 ticks post-intervention; the move first-drop at 8205-8238
  (candidate) vs 8216 or *never* (r4, on the seeds where it dies).
- **Behavioural consequences:** candidate holds route-1 through the cut (0 drops in-window, entry
  survives to window end) and relinquishes the stale route in the move (1 drop); r2 relinquishes on
  seeds 3/4/5/7 cut; r4 never relinquishes in the move on seeds 1/2/4 and dies holding the stale
  route.
- **Expenditure:** the estimate bit is written once (7 replicas, 1 energy + 1 material) on the first
  in-window contact; proactive renewal adds ~97-140 extra replicas in the cut that §6 shows to be
  redundant. No arm's survival difference is explained by spend (the candidate and r2/r4 differ in
  *which* threshold they use, not in magnitude of maintenance spend).
- **Survival:** §4. Candidate 16/16; r2 and scramble each 2 deaths (seed 4 cut); r4 6 deaths (seeds
  1/2/4 move). Reported per arm, per condition, not summed across arms (AC86's correction).

---

## 6. The bounded redundancy: proactive renewal is inert here (reported, not hidden)

The candidate's E_machinery branch does two things — hold, and *proactively renew* the entry. The
hold is load-bearing (seed 4). The proactive renewal is **not**: r4 (no proactive renewal) keeps the
entry alive through the 96-tick window on **every** individual via the frozen reactive renewal
(obs bits 3/4 fire at life ≤ 16), so `entry_life_at_cut_end > 0` for r4 in 16/16, identical to the
candidate. The candidate's ~97-140 proactive replicas buy nothing that the reactive renewal was not
already buying.

This is the C1 §7 anticipated outcome ("the estimate's renewal behaviour turns out to be
indistinguishable from the frozen renewal-urgent-triggered renewal") and AC106 finding #3, now
measured with the *correct* longer-counter rival rather than a no-op duplicate. It does **not**
undercut the discriminator: the load-bearing consumption is the *hold* (threshold selection), not
the renewal. Any K6 protocol must gate on the threshold-selection survival contrast (§4), and must
not promise a proactive-renewal advantage the data do not support.

---

## 7. Rival verification, host-field audit, state sufficiency

- **Rivals differ as advertised** (measured): `HOLD_N = 24 > 7` (the streak's max) and
  `HOLD_N ≠ STREAK_N`; r2 and r4 differ behaviourally in both conditions (r2 relinquishes in the cut
  where r4 holds; r4 dies in the move where r2 survives). r4's counter is per-key, mirroring the
  frozen streak's per-key structure (a first build used a single counter that channel-0 productive
  contacts reset — caught by reading the move trajectory, fixed).
- **No-cause identity (P3):** candidate byte-identical (`state_hash`) to r2 in `no_cause` on 16/16
  individuals; the estimate is inert by construction when no cause is present. r2 at PORTS=2
  reproduces `ac100` `gray_ctl` byte-for-byte (the single-change license).
- **Host-field audit:** the candidate's host fields are config constants (`bel_off`, `estimate`,
  `proactive`, `scramble`, `threshold`) or observational logs (`bel_events`, `streak_events`, `log`,
  `bel_attempts`, `bel_refused`); the inherited `ac12.Alloc.streak` dict is vestigial and never read.
  No host field steers a write — e is read from `traces[0, bel_off]` (majority), the streak from
  `traces[0, streak_offs]` (Gray majority). r4's host counter is a disclosed rival-side comparator.
- **State sufficiency:** per-tick observer-discard on the candidate (fresh succession observer +
  fresh alloc mid-cut) leaves the trajectory byte-identical at every tick, 16/16.
- **Attempted vs completed writes:** the estimate bit flip is logged as `bel_attempts` (1 per
  cause-onset) separate from `bel_writes` (7 replicas) and `bel_refused` (0); the split is exercised
  structurally (the `bel_write` primitive returns the three values and refuses whole under the cap).

---

## 8. Claim discipline and boundary

- This is **level-(c)** representational machinery, engineering-grade. The strongest wording it earns:
  "**a maintained one-bit cause-estimate, updated from the organism's own (bound, used_held,
  productive) history, discriminates the two causes at decision times and selects the behaviour that
  survives each world, where the reactive baseline and the longer counter each fail in one.**"
- It makes **no** level-(d) claim, no metacognition claim, no autopoiesis claim, no "alive" claim.
- **Seeds are the replication unit; engineering seeds 0-7 do not transfer to finals** (AC39, and the
  AC68/AC39 bimodality lesson — survival here is 16/16 clean, but the confirmatory protocol must use
  disjoint finals and a bimodality-aware gate). The cut does not bite r2 on seeds 0/1/2/6 (the
  streak never reaches 6 there); that is a non-vacuity note carried into K6, not a failure.
- The proactive-renewal redundancy (§6) is a scope note on *which* consumption is load-bearing, not
  a revision of the discriminator result.
- The bound/used_held interface is available to **every** rival (it is the organism's own memory and
  retrieval result); the candidate is not credited with a sensor its rivals lack.

---

## 9. What this hands to K6

Feasibility is **supported**: the estimator discriminates and the discrimination is survival-relevant
in both directions. A confirmatory study (K6) should (a) gate on the §4 threshold-selection survival
contrast (candidate survives where r2 dies in the cut AND where r4 dies in the move) on disjoint
finals, (b) carry the no-cause identity and observer-discard as gates, (c) drop the proactive-renewal
advantage from the gate list (it is inert), and (d) record per-arm per-condition counts, never a
summed N.
