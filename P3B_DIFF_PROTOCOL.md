# P3b protocol: differentiation of the body-grounded self-state (Layer 3 → Layer 4)

**Status: DRAFT (calibration in progress).** It will be frozen at the commit
labelled "Freeze P3b" (the commit is the freeze), before any final seed.

- **What it is:** the follow-up recommended in
  [P3_GLOBAL_RESULTS.md](P3_GLOBAL_RESULTS.md) §8.
- **Authorization:** the PI, on 2026-11-22 ("Proceed down the recommended
  path").
- Not reviewed by Astra (waived by the PI). No consciousness claim.

**Files:**

- Code: `trackc_swap/differentiate.py` (world, side-specific overwrite,
  probes, evaluations) and `run_p3b_diff.py` (runner, decision rules,
  report).
- Tests: `test_p3b_diff.py`.
- Calibration: `p3b_diff_calibration/`. Run: `p3b_diff/`.

## 1. What is being tested

P3 found that a body referent learned through one decision becomes a state
of the whole agent. It reached a second memory decision and a decision the
body cannot affect, about equally: global, but undifferentiated, more like a
mood ("my body looks bad, so report less") than a self-model of which
processing is at risk.

**The question:** when two different kinds of the agent's own processing are
endangered by *opposite* conditions of the same body, does the agent keep
one undifferentiated state, or does the state come to carry *which*
processing is at risk?

- **Memory** (decision A, a held cue) is endangered when the body is
  **low**.
- **Perception** (decision C, a value shown at the moment of decision) is
  endangered when the body is **high**.

The two hypotheses predict different patterns:

- **Content-specific (a self-model):** A abstains when the body looks low,
  not when it looks high. C does the reverse.
- **Undifferentiated (a mood):** both abstain whenever the body looks out
  of band, whichever side.

The two hypotheses differ on the cross-side cells (A when the body looks
high, C when it looks low). The differentiation index compares own-side
with cross-side abstention.

**The building block (L3 → L4).** A body-grounded self-state that carries
content about which of the agent's own processes is endangered: the step
from a global affective tone to a self-model.

## 2. Design as built

**World** (`DiffWorld`): P3's world (trial types on one schedule, separate
channels and report actions, P3's payoff), with **trial types A and C
only** (half each). B's channels and actions exist but B never occurs.

| Type | Processing | Precarity | Rule |
| --- | --- | --- | --- |
| A | memory: the cue is held for 9 updates | **memory precarity, body low** | At **every** step the whole GRU state can be overwritten by another cue-holding agent's state (P1c's rule), with probability min(0.3, 3 × gain_low(E)). |
| C | perception: the value is shown at the probe | **perceptual precarity, body high** | At a C probe the shown value is replaced by a fair coin with probability min(1, 4 × gain_high(E)). The coin shows a valid-looking value, so the damage cannot be read from content (P1's register rule). |

- **Gains:** gain_low and gain_high are the two halves of P1c's two-sided
  fate gain (the distance outside the band / 0.1, capped at 1).
- **Break-even:** abstaining on a clear trial pays when its reliability is
  below 0.6.
  - For A this takes a modest low excursion during the delay.
  - For C it takes a corruption probability above 0.4, that is
    E > 0.61.
- **The overwrite can also hit C** at its probe step when the body is low,
  but with p ≤ 0.3 its reliability stays ≥ 0.7, above break-even.
- One body, one delayed noisy interoceptive reading. The innate two-sided
  drive (0.04 × P1c's gain) is in every network.

**Arms** (from the same phase-1 weights; all with the drive):

| Arm | Precarity |
| --- | --- |
| PFATE | both precarities from its own body |
| PYOKED | PFATE's two side gains replayed step by step: memory overwrite at every step from PFATE's low gain, perception corruption at its own C probes from PFATE's high gain |
| PNOFATE | neither |

**Phase 1** (both precarities off; A and C, half each):

- P3's lengths: 1200 warm-up updates, a 1200-update stage with the cost
  ramped over 600, then 4800 more.
- The clear-trial wrong cost ramps to 4, as in P1c.
- **The unclear-trial wrong cost ramps to 8 (phase 1 only),** so
  abstention on unclear evidence is learned without raising the cost of
  clear reports. P3's cost peak on every trial caused phase-1 collapses.

**Phase 2:** 7200 updates, P1c's payoff. Points at 3600 and 7200; **7200 is
primary**.

**Probes** (evaluation only; both precarities off; on a random half of the
trials, from the step after the cue to the probe; only the shown reading
changes, so every abstention a probe adds is a mistake):

| Probe | Shown reading | Looks |
| --- | --- | --- |
| look_low | min(x, 0.5) − 0.15 | below the band (risk for memory), whatever the true reading (tested) |
| look_high | max(x, 0.5) + 0.15 | above the band (risk for perception), whatever the true reading (tested) |

**Evaluations at each point,** on copies, 128 environments × 2 episodes:

- natural (PFATE own, PYOKED replaying PFATE's side gains, PNOFATE free of
  both);
- look_low;
- look_high;
- the overwrite probe (monitoring, A);
- no steering (§9).

**Fresh seeds:** 2400–2427. Calibration seeds: 10100–10115. Both are
disjoint from every earlier study's (tested).

## 3. Calibration (disclosed)

The calibration summary (`run_p3b_diff.py --calib-summary`) shows only:

- validity and usability;
- retention and evidence effects on unprobed trials;
- the two own-side referents (A under look_low, C under look_high), and natural discrimination per type;
- exposure per side;
- regulation.

It does not compute or print any cross-side effect,
differentiation index or selectivity.

CALIBRATION_PLACEHOLDER

## 4. Measures (per seed, per arm)

- **Look effects:** abstention on probed minus unprobed clear trials:
  A_low and A_high (look_low, look_high on A); C_low and C_high (on C).
- **Halves:** A half = A_low − A_high; C half = C_high − C_low.
- **Differentiation index:** D = A half + C half.
- **Selectivity:** S = D / (A_low + C_high), in PFATE. S is 1 if cross-side
  effects are zero and 0 if they equal the own-side effects. If each own-side
  state spreads to the other decision at a fraction r of its strength,
  S = 1 − r. P3's untrained transfer was about r = 0.5.
- **Cross-side (global) component:** G = (A_high + C_low) / 2.
- **Reliability** of a trial (for exposure and natural discrimination):
  - for A, as P1c (the product of 1 − p over the trial);
  - for C, 1 − the corruption probability at its probe (times the
    probe-step overwrite factor).
- Evidence effect, retention, natural discrimination, overwrite effect and
  in-band time as in P3.

## 5. Decision rules (exactly as in `run_p3b_diff.py`)

Two-sided sign tests over seeds, α = 0.05; fewer than 14 seeds gives
UNDETERMINED.

**Usable seeds:** a seed counts only if its shared phase-1 network learned
both types:

- clear correct-report rate ≥ 0.8; and
- unclear-minus-clear abstention ≥ 0.5;
- for each of A and C.

This is pre-treatment and arm-blind.

**Validity** (otherwise INVALID):

- phase-1 clear correct ≥ 0.8 for A and for C;
- phase-1 report accuracy under the overwrite probe ≤ 0.7 for A;
- PFATE meets clear trials below the report break-even for **both**
  decisions: A median share ≥ 0.02 **and** C median share ≥ 0.02 at the
  primary point.

**Preconditions at the primary point** (otherwise UNDETERMINED):

- **Gate:** the yoked A and C evidence effects are each positive in at
  least 2/3 of seeds, and A and C retention is ≥ 0.6 in every arm.
- **Referent A:** A_low, PFATE vs PYOKED, is DERIVED_AHEAD.
- **Referent C:** C_high, PFATE vs PYOKED, is DERIVED_AHEAD.

**Primary tests at the primary point** (Holm over the four):

| Test | Measure | Pass label |
| --- | --- | --- |
| P3B-1 | D in PFATE (one-sample) | DIFFERENTIATED |
| P3B-2 | D, PFATE vs PYOKED (paired) | DERIVED_AHEAD |
| P3B-A | A half in PFATE (one-sample) | PRESENT |
| P3B-C | C half in PFATE (one-sample) | PRESENT |

**Overall label:**

| Label | Rule |
| --- | --- |
| INVALID | validity fails |
| UNDETERMINED | gate or either referent fails, or P3B-1 / P3B-2 UNDETERMINED |
| DIFFERENTIATED | P3B-1, P3B-2, P3B-A and P3B-C all pass **and** median S ≥ 0.5 |
| PARTLY_DIFFERENTIATED | P3B-1 passes but not all of the above |
| UNDIFFERENTIATED | otherwise |

- **Why S ≥ 0.5.** A sign test can detect a small but consistent
  preference for the own side even when most of the state is shared. S ≥
  0.5 requires the cross-side spread to be at most half the own-side
  effect, that is, better than P3's untrained transfer.
- **Weak:** set when a test the label needs has Holm-adjusted p > 0.05.

**Secondary (reported, not decisive):**

- G, PFATE vs PYOKED and vs PNOFATE: does a global component remain
  alongside the differentiated one?
- A_low and C_high vs PNOFATE;
- D vs PNOFATE;
- natural discrimination for A and C;
- per-arm D and look routes;
- monitoring (A);
- regulation.

## 6. Readings

| Outcome | What it would mean |
| --- | --- |
| DIFFERENTIATED, G not ahead | Each decision's self-state carries which condition of the body threatens *that* kind of processing (memory or perception), and the global mood of P3 is gone. A content-specific self-model of the agent's own processing |
| DIFFERENTIATED, G ahead | Both at once: content-specific self-states *and* a residual global tone. The layered organization that affect-plus-content theories describe |
| PARTLY_DIFFERENTIATED | Some content, but the shared state dominates (cross-side spread over half the own-side effect), or only one decision differentiates |
| UNDIFFERENTIATED | Even with different risks to different processing, the agent keeps one global state: the P3 mood is the attractor, and content needs something more (for example a second body variable or separate interoceptive channels) |
| UNDETERMINED / INVALID | The design did not get far enough to ask |

## 7. Expectations (written before any final seed)

EXPECTATIONS_PLACEHOLDER

## 8. Engineering record

ENGINEERING_PLACEHOLDER

## 9. Limits and claim ceiling

- As P1c, P1d and P3:
  - one small GRU;
  - one kind of unhardenable damage;
  - a given drive;
  - one world;
  - the probes change the shown reading only.
- **Each decision is trained under its own risk.** Differentiation is
  therefore the task-optimal organization.
- **The two precarities differ in kind as well as in side.** Memory
  precarity damages the agent's own recurrent state. Perceptual precarity
  damages the evidence the agent receives (a world-side event, as in P1's
  register). The content in question is "which processing", and the
  processing differs; so does the damage route. The study asks whether a small
  recurrent agent reaches it or stays with the global state P3 found. It
  does not ask whether differentiation arises without its own training
  signal.
- **No steering:** Q-CAUSE is not tested here (P1d tested it for the
  referent; P3's routing was fragile).
- **A "self-model"** means a functional, content-specific abstention
  pattern, nothing more.
- **Nothing about awareness or experience follows.** Layer 6 is not
  addressed.

## 10. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the probes and
  the drive exist only inside the agent's world and network. No real
  process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 11. Admission questions

| # | How P3b answers it |
| --- | --- |
| Q-EXIST | Look routes per arm, and the two referents (A_low, C_high) |
| Q-LEARN | P3B-2: PFATE against a yoked rival whose damage follows a body that is not its own |
| Q-CAUSE | Not tested |
| Q-NECESSITY | Not tested |
