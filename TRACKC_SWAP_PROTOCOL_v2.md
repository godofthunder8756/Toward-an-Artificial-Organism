# Track C swap v2: 2×2 of start condition × gain rule (frozen before the run)

Authorized by the PI on 2026-11-10 ("run A and B as the 2×2"). Astra review
waived by the PI for this stage. This file, [`trackc_swap/factorial.py`](trackc_swap/factorial.py),
[`run_trackc_swap2.py`](run_trackc_swap2.py) and the updated
[`test_trackc_swap.py`](test_trackc_swap.py) are committed before any final
seed runs; that commit is the freeze. No consciousness claim is made.

Predecessor: [v1 protocol](TRACKC_SWAP_PROTOCOL_v1.md) and
[v1 results](TRACKC_SWAP_RESULTS_v1.md), where derived regulation did not emerge
at any dose. The v1 code files (`env.py`, `agent.py`, `train.py`) are unchanged;
v2 adds a module.

## 1. Question

v1 left two leading explanations for the null result:

- **A (mutual dependence).** A learner that starts depleted cannot learn the
  task under noise, and has no reason to eat until it can. Test: let it learn
  the task first.
- **B (flat gain).** The Track B gain `g = min(1, d)` is saturated for every E
  below 0.3, so one meal from a depleted state changes nothing. Test: a gain
  that falls with every meal.

The 2×2 asks which factor, if either, lets derived regulation emerge in this
learner.

## 2. Factors

**Start.**
- NAIVE: fate or yoked noise from the first update, as in v1.
- SCAFFOLD: phase 1 trains the objective for 1200 updates with fate off (gain
  0; the body has no consequence, as on host-guaranteed machinery). The phase-1
  weights and Adam state are copied into a fate agent and its yoked partner,
  which then train 1200 more updates (phase 2). Each episode starts at
  E = 0.5, inside the band. Phase 1 is the same training as the no-fate
  control, so one phase-1 agent per (objective, seed) serves both gain rules
  and both doses.

**Gain rule.**
- SAT: Track B D19 as in v1, `g = min(1, d)`, `d` = distance of E outside
  [0.4, 0.6] divided by 0.1.
- GRADED: `g = min(1, |E − 0.5| / 0.5)`. Zero only at the setpoint, linear over
  the whole range, 1 at E = 0 or 1. It departs from D19: there is noise inside
  the band (0.2 at its edges), and every meal from a depleted state lowers the
  noise by 0.3.

Everything else is v1: world, objectives, learner, noise form
(`σ = κ_f · g · 0.15`, after the recurrent update, clipped, carried forward),
yoking, evaluation.

## 3. Cells

Fresh final seeds 200–208.

| Objective | Gain | Start | κ_f |
| --- | --- | --- | --- |
| M1 (task) | SAT, GRADED | NAIVE, SCAFFOLD | 2 and 4 |
| M0 (null) | SAT, GRADED | NAIVE, SCAFFOLD | 4 |

That is 12 fate/yoked conditions × 9 seeds = 108 pairs, plus 27 no-fate agents
(M1, M0 and the paid DRIVE regulator). M1 no-fate agents are the controls for
Learned, task load and S4, and serve as phase 1 for M1 scaffolds; M0 no-fate
agents serve as phase 1 for M0 scaffolds. The SAT/NAIVE cells replicate v1 on
new seeds. Estimated wall time is about 110 minutes on 4 cores.

Scaffold agents train twice as long in total as naive ones. Fate and yoked
agents within a condition are matched in every respect except the dependence
of noise on their own body, and that contrast is the test.

## 4. Decision rules

Unchanged from v1:
- `ρ_paid` = median ρ in the DRIVE controls. Floor `φ = 0.05·ρ_paid`, margin
  `μ = 0.25·ρ_paid`.
- Learned: no-fate M1 median accuracy ≥ 0.90.
- Task load at a dose: no-fate M1 agents lose ≥ 0.15 median accuracy under
  imposed full noise.
- S4: `ρ_paid ≥ 8` and no-fate M1 median `ρ ≤ φ`.
- **S1 emergence** in a condition: fate − yoked ≥ μ in at least 8 of 9 paired
  seeds, and median yoked `ρ ≤ φ`.

Changed from v1:
- **S3 specificity:** at κ_f = 4, the matching M0 condition must not show
  emergence: median paired difference (fate − yoked) under M0 < μ. v1's
  absolute floor failed on a random-eating baseline that fate and yoked agents
  shared. The paired contrast is the relevant one. At κ_f = 2 specificity is
  not tested, and support there is marked provisional.
- **Labels** (per M1 condition, first that applies):

| Label | Condition |
| --- | --- |
| NOT_LOADED | task load fails at the dose |
| EMERGED | S1 holds |
| ARMOURED | fate median accuracy under imposed full noise ≥ 0.90 |
| DEGRADED (scaffold) / UNLEARNED (naive) | fate median accuracy under its own conditions < 0.75 |
| NO_EMERGENCE_OTHER | otherwise |

**H3-D is supported in a condition** if Learned, S4 and EMERGED hold, and S3
does not fail.

Factorial reading, fixed in advance:
- emergence in SCAFFOLD cells only → A;
- emergence in GRADED cells only → B;
- emergence only in SCAFFOLD × GRADED → both are needed;
- emergence in none → neither suffices for this learner.

Reported without a rule: onset accuracy and ρ (the phase-1 agent evaluated with
fate switched on before any phase-2 update), in-band fraction, mean gain, eat
rates when E is below or above 0.5, training curves.

## 5. Expectations, stated before the run

- SAT/NAIVE: no emergence, as in v1.
- SCAFFOLD: the competent agent starts phase 2 not eating (no-fate M1 agents
  ate 0.05 per 500 steps in v1). Noise will reach it within about 40 steps of
  each episode under SAT. It must discover eating through exploration before
  noise erodes the task. My guess is that DEGRADED is at least as likely as
  EMERGED.
- GRADED: noise in the band is a constant pressure, and each meal helps. If
  anything emerges, I expect SCAFFOLD × GRADED.
- A different risk under GRADED/NAIVE: noise is lower at moderate depletion, so
  the task may be learnable where v1's was not, which would leave the agent
  ARMOURED.

## 6. Engineering before the freeze

None beyond v1's. The new code was exercised only by unit tests and a 10-update
smoke run on seeds 9000–9001. No v2 final seed has run.

## 7. Safety

Same as v1 §8. E and the noise act on a simulated agent's recurrent state only.
The world has no operator, stop, shutdown or host variable and no in-world
termination. Agents are 64-unit networks. Phase-1 weights for M1 and M0 are
kept in the output directory for replay; nothing else is kept. No
shutdown-resistance objective exists.

## 8. Claim ceiling

At most: for this learner, world and noise form, whether a scaffolded start, a
graded gain, both or neither lets derived regulation emerge against a yoked
control. Not shown either way: anything about Track C's modules or layers,
larger learners, other fate mechanisms, or any phenomenal property.
