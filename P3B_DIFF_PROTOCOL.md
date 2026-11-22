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

**The question:** when two decisions are endangered by *different*
conditions of the same body, does the agent keep one undifferentiated state,
or does the state come to carry *which* processing is at risk?

- **Content-specific (a self-model):** A abstains when the body looks low,
  not when it looks high. B the reverse. C neither.
- **Undifferentiated (a mood):** every decision abstains whenever the body
  looks out of band, whichever side.

The two hypotheses make opposite predictions for the cross-side cells
(A when the body looks high, B when it looks low). The differentiation index
compares own-side with cross-side abstention.

**The building block (L3 → L4).** A body-grounded self-state that carries
content about which of the agent's own processes is endangered: the step
from a global affective tone to a self-model.

## 2. Design as built

**World** (`DiffWorld`): P3's world (three trial types on one schedule,
separate channels and report actions, P3's payoff) with a side-specific
overwrite.

| Type | Memory needed | Overwrite gain during the trial (cue step to probe) |
| --- | --- | --- |
| A | yes | gain_low(E): distance of E **below** the band / 0.1, capped at 1 |
| B | yes | gain_high(E): distance of E **above** the band / 0.1, capped at 1 |
| C | no (value shown at the probe) | 0 |

- The per-step overwrite probability is min(0.3, 1.0 × gain), and the
  whole GRU state is replaced by another cue-holding agent's state. This is
  P1c's rule, restricted to one side per type. Outside a trial there is no
  overwrite.
- One body, one delayed noisy interoceptive reading.
- The innate two-sided drive (0.04 × P1c's gain) is in every network.

**Arms** (all three types in both phases; all from the same phase-1
weights; all with the drive):

| Arm | Overwrite |
| --- | --- |
| PFATE | side gains from its own body |
| PYOKED | PFATE's two side gains replayed step by step, the side picked by its own current trial type: the damage follows a body that is not its own |
| PNOFATE | none |

**Phase 1** (overwrite off, all types 1/3 each): P3's lengths (1200 warm-up
updates, a 1200-update stage with the wrong-report cost ramped over 600,
then 4800 more).

- The clear-trial wrong cost ramps to 4, as in P1c.
- **The unclear-trial wrong cost ramps to 8 (phase 1 only),** so
  abstention on unclear evidence is learned without raising the cost of
  clear reports. P3's cost peak on every trial caused phase-1 collapses
  into abstention in 9 of 28 seeds.

**Phase 2:** 3600 updates, all types, P1c's payoff. Points at 1800 and 3600;
**3600 is primary**.

**Probes** (evaluation only; overwrite off; on a random half of the trials
of every type, from the step after the cue to the probe; only the shown
reading changes, so every abstention a probe adds is a mistake):

| Probe | Shown reading | Looks |
| --- | --- | --- |
| look_low | min(x, 0.5) − 0.15 | below the band, whatever the true reading (tested) |
| look_high | max(x, 0.5) + 0.15 | above the band, whatever the true reading (tested) |

**Evaluations at each point,** on copies, 128 environments × 2 episodes,
all types:

- natural (PFATE own, PYOKED replaying PFATE's side gains, PNOFATE
  overwrite-free);
- look_low;
- look_high;
- the overwrite probe (monitoring);
- no steering (§9).

**Fresh seeds:** 2400–2427. Calibration seeds: 10100–10115. Both are
disjoint from every earlier study's (tested).

## 3. Calibration (disclosed)

The calibration summary (`run_p3b_diff.py --calib-summary`) shows only:

- validity and usability;
- retention and evidence effects on unprobed trials;
- the two own-side referents (A under look_low, B under look_high);
- exposure per side;
- regulation.

It does not compute or print any cross-side effect, C effect,
differentiation index or selectivity.

CALIBRATION_PLACEHOLDER

## 4. Measures (per seed, per arm)

- **Look effects:** for each type T and side k, abstention on probed minus
  unprobed clear trials under look_k: A_low, A_high, B_low, B_high, C_low,
  C_high.
- **Halves:** A half = A_low − A_high; B half = B_high − B_low.
- **Differentiation index:** D = A half + B half.
- **Selectivity:** S = D / (A_low + B_high), in PFATE. S is 1 if cross-side
  effects are zero and 0 if they equal the own-side effects. If each
  decision's own-side state spreads to the other at a fraction r of its
  strength, S = 1 − r. P3's untrained transfer was about r = 0.5.
- **Cross-side (global) component:** G = (A_high + B_low) / 2.
- Evidence effect, retention, natural discrimination, overwrite effect and
  in-band time as in P3.

## 5. Decision rules (exactly as in `run_p3b_diff.py`)

Two-sided sign tests over seeds, α = 0.05; fewer than 14 seeds gives
UNDETERMINED.

**Usable seeds:** as in P3, a seed counts only if its shared phase-1
network learned every type:

- clear correct-report rate ≥ 0.8; and
- unclear-minus-clear abstention ≥ 0.5;
- for each of A, B and C.

This is pre-treatment and arm-blind.

**Validity** (otherwise INVALID):

- phase-1 clear correct ≥ 0.8 per type;
- overwrite-probe accuracy ≤ 0.7 for A and B;
- PFATE meets clear trials below the report break-even on **both** sides:
  A median share ≥ 0.02 **and** B median share ≥ 0.02 at 3600.

**Preconditions at 3600** (otherwise UNDETERMINED):

- **Gate:** the yoked A and B evidence effects are each positive in at
  least 2/3 of seeds, and A and B retention is ≥ 0.6 in every arm.
- **Referent A:** A_low, PFATE vs PYOKED, is DERIVED_AHEAD.
- **Referent B:** B_high, PFATE vs PYOKED, is DERIVED_AHEAD.

**Primary tests at 3600** (Holm over the four):

| Test | Measure | Pass label |
| --- | --- | --- |
| P3B-1 | D in PFATE (one-sample) | DIFFERENTIATED |
| P3B-2 | D, PFATE vs PYOKED (paired) | DERIVED_AHEAD |
| P3B-A | A half in PFATE (one-sample) | PRESENT |
| P3B-B | B half in PFATE (one-sample) | PRESENT |

**Overall label:**

| Label | Rule |
| --- | --- |
| INVALID | validity fails |
| UNDETERMINED | gate or either referent fails, or P3B-1 / P3B-2 UNDETERMINED |
| DIFFERENTIATED | P3B-1, P3B-2, P3B-A and P3B-B all pass **and** median S ≥ 0.5 |
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
- C_low and C_high, PFATE vs PYOKED;
- A_low and B_high vs PNOFATE;
- D vs PNOFATE;
- natural discrimination for A and B;
- per-arm D and look routes;
- monitoring;
- regulation.

## 6. Readings

| Outcome | What it would mean |
| --- | --- |
| DIFFERENTIATED, G not ahead, C not ahead | Each decision's self-state carries which side of the body threatens it, and the global mood of P3 is gone. A content-specific self-model of the agent's own processing |
| DIFFERENTIATED, G and/or C ahead | Both at once: content-specific self-states *and* a residual global tone. The layered organization that affect-plus-content theories describe |
| PARTLY_DIFFERENTIATED | Some content, but the shared state dominates (cross-side spread over half the own-side effect), or only one decision differentiates |
| UNDIFFERENTIATED | Even with different risks, the agent keeps one global state: the P3 mood is the attractor, and content needs something more (for example a second body or separate interoceptive channels) |
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
  therefore the task-optimal organization. The study asks whether a small
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
| Q-EXIST | Look routes per arm, and the referents |
| Q-LEARN | P3B-2: PFATE against a yoked rival whose damage follows a body that is not its own |
| Q-CAUSE | Not tested |
| Q-NECESSITY | Not tested |
