# P3 protocol: global availability of the body-grounded self-state (Layer 0 → Layer 3)

**Status: DRAFT (calibration in progress).** It will be frozen at the commit
labelled "Freeze P3" (the commit is the freeze), before any final seed.

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

- 1200 warm-up updates;
- 1200 updates with the wrong-report cost ramped to 4;
- 4800 further updates (P1c: 2400; §3).

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

CALIBRATION_PLACEHOLDER

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

**Validity** (otherwise INVALID):

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

EXPECTATIONS_PLACEHOLDER

## 8. Limits and claim ceiling

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

## 9. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the probes,
  the rehearsal world and the drive exist only inside the agent's world and
  network. No real process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 10. Admission questions

| # | How P3 answers it |
| --- | --- |
| Q-EXIST | The B worse effect in PFATE (per arm), and P3-1 |
| Q-LEARN | B never learned under the fate. P3-1 compares PFATE with a yoked rival learning under the same losses and the same rehearsal |
| Q-CAUSE | P3-3: a direction learned from A moves B |
| Q-NECESSITY | Not tested |
