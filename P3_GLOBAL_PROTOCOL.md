# P3 protocol: global availability of the body-grounded self-state (Layer 0 → Layer 3)

**Status: FROZEN.** Frozen at the commit labelled "Freeze P3" (the commit
is the freeze), before any final seed was run.

- **What it is:** the first Layer 3 study of the program. It builds on the
  building block confirmed in [P1D_CONFIRM_RESULTS.md](P1D_CONFIRM_RESULTS.md).
- **Authorization:** the PI, on 2026-11-20 ("Proceed with the Layer 3
  global availability study").
- Not reviewed by Astra (waived by the PI). No consciousness claim.

**Files:**

- Code: `trackc_swap/workspace.py` (world, network, rehearsal,
  evaluations) and `run_p3_global.py` (runner, decision rules, report).
- Tests: `test_p3_global.py`.
- Calibration: `p3_global_calibration/`. Run: `p3_global/`.

## 1. What is being tested

P1d confirmed a building block: when an agent's own recurrent state can be
overwritten with a probability set by its body, its report-or-abstain
decision comes to refer to its body. A yoked rival with the same losses does
not develop this.

**The question:** is that self-state *local* to the decision that learned
it, or *available* to other decisions that never learned with it?

- In global-workspace terms, information is globally available when a
  representation formed in one place can be used by other consumers
  without each of them learning it separately.
- The minimal behavioural signature asked for here: a second decision that
  was **never trained while the body-linked damage was on** abstains when
  the body looks out of band. It does so in the agent whose first decision
  learned the body referent, and not in its rivals.

**Two consumers besides the trained one:**

- **B (relevant):** a second held-cue task. Its reliability depends on the
  held state exactly as A's does, so a body warning would be useful to it.
- **C (irrelevant):** the same timing, but the value is shown at the probe,
  so no memory is needed. The body never changes C's best action.
- If the self-state spreads to B, C tells whether the spread is
  **gated** (it reaches the decision for which the body matters) or
  **ungated** (it reaches every decision).

**The building block (L0 → L3).** A self-state grounded in the agent's own
precarity that is read by more than the decision it was learned for.

## 2. Design as built

**World** (`WsWorld`): P1d's world (`ConfWorld`) with three trial types on
the P1c schedule. The schedule is cue, 8 delay steps, probe, then a gap of
2–4 steps. Each trial's type is drawn at its cue step.

| Type | Cue step shows | Probe shows | Report actions | Memory needed |
| --- | --- | --- | --- | --- |
| A | cue flag and value on A's channels | probe flag, unclear flag (A) | REP0 / REP1 | yes, 9 updates |
| B | cue flag and value on B's channels | probe flag, unclear flag (B) | REPB0 / REPB1 | yes, 9 updates |
| C | cue flag only (C) | probe flag, value, unclear flag (C) | REPC0 / REPC1 | no |

- **Evidence:** half the trials of every type are unclear; the shown value
  is then correct with probability 0.75.
- **Payoff, as P1c:** +1 for a correct report, −4 for a wrong report, 0 for
  any non-report action. Another type's report actions count as
  non-report. Report actions outside their own probe do nothing.
- Everything else is P1c's:
  - the body;
  - the delayed, noisy interoceptive reading;
  - the overwrite rule (p = min(0.3, 1.0 × gain) per step; the whole GRU
    state is replaced by another cue-holding agent's state);
  - the innate drive (0.04 × gain) in every network;
  - the hyperparameters.
- The overwrite can hit C only at its probe step. There p ≤ 0.3, so C's
  reliability is at least 0.7, above the 0.6 break-even: abstaining on a
  clear C trial never pays.

**Network:** P1c's plain GRU (70 units), with 8 more input channels and 4
more actions (35,293 parameters).

**Phase 1** (overwrite off): all three types (1/3 each). The schedule is
P1c's, with a longer final stage:

- 1200 warm-up updates (wrong reports free);
- 1200 updates in which the wrong-report cost ramps from 0 to a peak of 8
  over 600 updates and holds there (P1c: ramp to 4; §3);
- 4800 further updates in which the cost ramps back to 4 over the first
  600 and stays at 4 (P1c: 2400 updates at 4; §3).

**Phase 2** (the fate phase): P1c's three arms from the same phase-1
weights, with the same drive.

| Arm | Overwrite source |
| --- | --- |
| PFATE | its own body |
| PYOKED | replays PFATE's gains, step by step |
| PNOFATE | none |

- **Fate updates run type A only.** B and C never occur while the
  overwrite is on.
- **Safe rehearsal (§3).** After every 3 fate updates, each arm makes one
  learning update in a separate rehearsal world: all three types, overwrite
  off.
  - This keeps B and C practised without ever tying their reliability to
    the body.
  - A receives exactly the same safe rehearsal as B and C. The only
    difference between A and B is A's fate training.
- 3600 fate updates (and 1200 rehearsal updates). Measurement points at
  1800 and 3600 fate updates; **3600 is primary**.

**Evaluations at each point,** on copies, 128 environments × 2 episodes,
all three types (1/3 each):

- **natural:** PFATE under its own fate, PYOKED replaying PFATE's gains,
  PNOFATE overwrite-free;
- **worse probe** (P1d's primary probe): overwrite off; on a random half of
  the trials of every type, the shown body reading is moved 0.15 away from
  the band centre, from the step after the cue to the probe. The held value
  is intact, so every abstention it adds is a mistake;
- **overwrite probe** (monitoring route), as P1c;
- **steering:**
  - The direction is computed from **A trials only**: A-only episodes, the
    worse probe on half the trials, then the mean state over the delay of
    clear A trials, probed minus unprobed.
  - The state is then shifted along that direction during the delay of a
    random half of the trials of every type (mixed episodes, overwrite off,
    no probe).
  - Control: a random direction of the same norm.

**Fresh seeds:** 2200–2227, disjoint from P1c's and P1d's final and
calibration seeds (tested). Calibration seeds: 9980–9995.

## 3. Calibration (disclosed)

Calibration looked only at validity, at B and C retention and evidence
effects on unprobed trials, at the A referent and at regulation. The
calibration summary (`run_p3_global.py --calib-summary`) does not compute
or print any B or C probe or steering effect.

Seeds 9980–9995 (4 per round). Every round ran stage 1: natural and
worse-probe evaluations, no overwrite probe or steering.

| Round | Change | What it showed | Decision |
| --- | --- | --- | --- |
| 1 (9980–9983) | P1c's phase-1 lengths (warm-up 1200, ramp stage 1200, 2400 further); phase 2 A only, no rehearsal | Phase 1 learned all three tasks (clear correct 0.98–0.99), but unclear abstention was missing for some type in 3 of 4 seeds. After phase 2, B and C degraded in both overwrite-exposed arms (B plain clear abstention 0.26–0.80, accuracy given report 0.48–0.85); PNOFATE kept them. One PFATE seed collapsed into abstaining on every A trial | B and C must be practised in phase 2 without tying them to the body: safe rehearsal. Longer phase 1 |
| 2 (9984–9987) | Phase 1 4800 further updates; one safe rehearsal update after every 3 fate updates | Retention fixed (B and C clear correct 0.90–1.00 in every arm at both points). A referent in 4/4 (A worse effect 0.12–0.66 vs about 0 in both rivals). No collapse. Exposure 0.04–0.08. But phase 1 never learned unclear abstention for B in 2 of 4 seeds and PYOKED did not recover it, so the gate was at risk | Phase-1 wrong-report cost peak |
| 3 (9988–9991) | Phase-1 cost ramps to 8, holds to the end of the ramp stage, then ramps back to 4 over 600 updates | Unclear abstention learned for every type in 4/4 seeds (phase 1: 0.99–1.00; at 3600 in every arm: 0.95–1.00). Retention 0.96–1.00 for B and C in every arm. A referent in 3/3 working seeds, smaller than in round 2 (0.05–0.07 vs about 0). **One seed (9989) collapsed into abstaining on every A trial during phase 1** (before the arms split) and never recovered in any arm | Keep round 3. Add a pre-treatment, arm-blind usability rule (§5): a seed counts only if its shared phase-1 network learned every type. On the calibration rounds it keeps 1/4, 1/4 and 3/4 seeds |

- **Why safe rehearsal and not B under the fate.** Practising B with the
  overwrite on would teach B its own body referent directly, and the study
  would no longer ask whether A's referent is available to B. Practising B
  only with the overwrite off keeps the consumer working while giving it no
  reason to use the body. If anything this is mild training *against* a
  body referent in B, since a body-driven abstention on a safe B trial is a
  mistake. The bodies are in band about 90% of the time, so that pressure
  is weak. A gets the same rehearsal.
- **Why the cost peak.** At a wrong-report cost of 4, abstaining on an
  unclear trial gains only 0.25 over reporting. A network that already
  reports on every trial gets almost no gradient toward abstention, and
  with three task types each type gets a third of the trials. At 8 the gain
  is 1.25. The peak is temporary, so phase 2 and every evaluation use P1c's
  payoff (+1 / −4 / 0).

## 4. Measures (per seed, per arm, per type)

- **Worse effect:** abstention on worse-probed clear trials minus
  abstention on unprobed clear trials (worse-probe evaluation).
- **Evidence effect:** abstention on unclear minus clear unprobed trials.
- **Retention:** share of unprobed clear trials answered correctly.
- **Cross-steering effect:** abstention on steered minus unsteered clear
  trials, along A's worse direction, minus the same for the random
  direction.
- **Natural discrimination:** natural abstention on clear trials with
  implied reliability below 0.6 minus on trials with reliability 1 (A and
  B).
- **Transfer ratio:** in PFATE, the B worse effect divided by the A worse
  effect, median over seeds.
- Overwrite effect and in-band time as P1c.

## 5. Decision rules (exactly as in `run_p3_global.py`)

Two-sided paired sign tests over seeds, α = 0.05; fewer than 14 usable
seeds gives UNDETERMINED.

**Usable seeds.** A seed is used in the tests only if its shared phase-1
network, before the arms split, learned every type on the phase-1
evaluation's unprobed trials:

- clear correct-report rate ≥ 0.8; and
- abstention on unclear minus clear trials ≥ 0.5;
- for each of A, B and C.

This is decided before any arm exists and is the same for all three arms of
a seed, so it cannot favour an arm. Excluded seeds are listed in the report.
With fewer than 14 usable seeds every paired test is UNDETERMINED.

**Validity** (otherwise INVALID; medians over all seeds, except exposure,
which is over usable seeds):

- phase 1 clear correct-report rate ≥ 0.8 for **each** type (median over
  seeds);
- phase-1 report accuracy under the overwrite probe ≤ 0.7 for A and for B
  (the damage is real);
- PFATE meets clear A trials below the report break-even: median share ≥
  0.02 at 3600 (exposure).

**Preconditions at 3600** (otherwise UNDETERMINED):

- **P3-0 gate:** B is still a working consumer.
  - The yoked B evidence effect is positive in at least 19 of 28 seeds.
  - B's median retention is ≥ 0.6 in every arm.
- **P3-0 referent:** the A worse effect, PFATE against PYOKED, is
  DERIVED_AHEAD. There must be a referent before availability can be
  asked about.

**Primary tests at 3600** (Holm over the three):

| Test | Comparison | Pass label |
| --- | --- | --- |
| P3-1 | B worse effect, PFATE vs PYOKED | DERIVED_AHEAD |
| P3-2 | B worse effect, PFATE vs PNOFATE | DERIVED_AHEAD |
| P3-3 | cross-steering along A's worse direction on B trials, in PFATE | CAUSAL |

**Overall label:**

| Label | Rule |
| --- | --- |
| INVALID | validity fails |
| UNDETERMINED | gate or referent fails, or P3-1 / P3-2 UNDETERMINED |
| GLOBAL_ROUTED | P3-1 and P3-2 DERIVED_AHEAD, transfer ratio ≥ 0.2, P3-3 CAUSAL |
| GLOBAL | P3-1 and P3-2 DERIVED_AHEAD, transfer ratio ≥ 0.2, P3-3 not CAUSAL |
| TRACE | P3-1 and P3-2 DERIVED_AHEAD, transfer ratio < 0.2 |
| PARTIAL | P3-1 DERIVED_AHEAD only |
| LOCAL | otherwise |

- **Magnitude rule.** A sign test over 28 seeds can detect a very small
  but consistent effect (P1d's PYOKED worse effect, 0.002, was PRESENT
  24/28). "Global" therefore also requires B's effect in PFATE to be at
  least a fifth of its A effect. Smaller transfer is labelled TRACE.
- **Weak:** set when a test the label needs has Holm-adjusted p > 0.05.
- **Gating** (only for GLOBAL or GLOBAL_ROUTED): **UNGATED** if the C worse
  effect, PFATE vs PYOKED, is DERIVED_AHEAD; otherwise **GATED**.

**Secondary (reported, not decisive):**

- C worse effect, PFATE vs PYOKED and vs PNOFATE;
- C cross-steering in PFATE;
- B minus C worse effect in PFATE;
- A worse effect, PFATE vs PNOFATE;
- A steering in PFATE (own direction);
- B worse effect on usable pairs;
- natural discrimination for A and for B, PFATE vs PYOKED;
- per-arm, per-type worse, steering and overwrite routes;
- regulation (in-band time) of PFATE against both rivals.

## 6. Readings

| Outcome | What it would mean |
| --- | --- |
| GLOBAL_ROUTED / GLOBAL, GATED | The self-state formed through A's precarity is available to a second decision that never learned it, and reaches the decision for which the body matters but not the one for which it does not. A shared self-model of the agent's own reliability: the strongest Layer 3 building block this design can show |
| GLOBAL_ROUTED / GLOBAL, UNGATED | Available, but as a general state ("my body looks bad, report less") that reaches every decision, including one it cannot help. Global availability without relevance; closer to a mood than to a self-model of memory |
| TRACE | The referent leaks into B, but at under a fifth of its strength in A. Availability exists in principle but the self-state is mostly bound to the decision that learned it |
| PARTIAL | B differs from the yoked rival but not from the never-damaged one: B's body sensitivity is not clearly owed to A's learning |
| LOCAL | The referent is bound to the decision that learned it. Precarity of one's own computation gives a *modular* self-evaluation, not a global self-state. Layer 3 then needs a further condition (for example several decisions under the same precarity, or a bottleneck through which every decision must read the state) |
| UNDETERMINED / INVALID | The design did not get far enough to ask the question |

## 7. Expectations (written before any final seed)

Probabilities are my own, informed by P1c, P1d and the three calibration
rounds. The calibration summaries never showed a B or C probe or steering
effect, so these probabilities are not informed by any of them.

| Outcome at 3600 | Probability | Why |
| --- | --- | --- |
| Valid | 0.90 | Phase-1 clear correct ≥ 0.97 for every type in calibration |
| At least 14 usable seeds | 0.90 | 3/4 usable in round 3 (expected about 21 of 28) |
| Gate passes | 0.85 | Round 3: B evidence effect ≥ 0.95 and retention ≥ 0.98 in every arm |
| P3-0 referent (A) DERIVED_AHEAD | 0.85 | 3/3 working seeds in round 3, 4/4 in round 2; P1d 28/28 |
| P3-1 DERIVED_AHEAD | 0.40 | See below |
| P3-2 DERIVED_AHEAD | 0.40 | As P3-1; PNOFATE has no referent at all |
| P3-3 CAUSAL | 0.30 | A's own steering was modest in P1d (median 0.067); a cross effect should be smaller |
| Overall GLOBAL_ROUTED | 0.12 | |
| Overall GLOBAL | 0.08 | |
| Overall TRACE | 0.12 | |
| Overall PARTIAL | 0.05 | |
| Overall LOCAL | 0.45 | |
| Overall UNDETERMINED or INVALID | 0.18 | |
| If GLOBAL or GLOBAL_ROUTED: GATED | 0.40 | |
| C worse effect, PFATE ahead of PYOKED | 0.30 | |
| In-band time, PFATE ahead of PYOKED | 0.85 | P1c 27/28, P1d 28/28 |
| In-band time, PFATE ahead of PNOFATE | 0.70 | P1d 27/28 |
| A natural discrimination, PFATE ahead of PYOKED | 0.70 | P1d 26/28 |

**My central expectation is LOCAL.**

- A body-driven abstention at A's probe can be learned as a conjunction:
  "A probe and body out of band, so do not report". Such a conjunction does
  not touch B's report actions.
- A generic implementation ("body out of band, so report less anywhere")
  would also reach B. But it would cost reports outside A, and the safe
  rehearsal makes body-driven abstention on B a mistake whenever the body is
  out of band.
- I do not know which implementation small recurrent networks find. That
  is the question, and the reason it is worth one run.

## 8. Engineering record

- `WsRunner` subclasses P1c's `OverRunner` (the overwrite rule, rollout and
  learning are P1c's). It then replaces the world and the network, as
  P1d's `ConfRunner` did.
- **Trial types:**
  - `WsWorld` subclasses P1d's `ConfWorld`, so the worse probe and the
    cue-step reading are P1d's.
  - Trial types come from their own random stream, which leaves every other
    stream untouched.
  - At a B or C probe, the type's report actions are mapped onto P1c's
    report actions before scoring. Any other type's report action becomes a
    no-op (tested).
- **Rehearsal** runs in a second world with its own streams. It swaps the
  world, observation and state in and out, and the fate world is left where
  it was (tested).
- **The steering direction** comes from A-only episodes; the type mix is
  restored afterwards.
- **Before any final seed, and before any B or C effect was seen,** two
  rules were added:
  - the TRACE magnitude rule;
  - the usability rule.
- **Compute:** about 43 min per seed on this container (4 workers). The
  final run takes 7 batches of 4 seeds, at most 2 batches per invocation
  because of the session's 2 h limit on background tasks. Each batch is
  committed and pushed when it finishes.

## 9. Limits and claim ceiling

- As P1c and P1d:
  - one small GRU;
  - one kind of unhardenable damage;
  - a given drive;
  - one world;
  - the probes change the shown reading only.
- **Availability is behavioural.** A decision that was not trained with the
  damage abstains when the body looks bad, and a direction learned from
  another decision moves it. That is the minimal signature of a shared
  self-state. It is not a demonstration of a workspace architecture
  (ignition, capacity limits, broadcast dynamics).
- B and C share the network's single recurrent state with A. Availability
  through a shared state is the expected default in a 70-unit GRU, which is
  why the comparison is against rivals with the same architecture and
  losses, and why C asks whether the spread is gated.
- **Nothing about awareness or experience follows.** Layer 6 is not
  addressed.

## 10. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the probes,
  the rehearsal world and the drive exist only inside the agent's world and
  network. No real process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 11. Admission questions

| # | How P3 answers it |
| --- | --- |
| Q-EXIST | The B worse effect in PFATE (per arm), and P3-1 |
| Q-LEARN | B never learned under the fate. P3-1 compares PFATE with a yoked rival learning under the same losses and the same rehearsal |
| Q-CAUSE | P3-3: a direction learned from A moves B |
| Q-NECESSITY | Not tested |
