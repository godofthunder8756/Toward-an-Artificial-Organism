# Grounding analysis G1: protocol (frozen before the run)

**ANALYTIC card. No learner, no training, no sampling. Exact rational
dynamic programming on a finite model.** Written 2026-11-10 at the PI's
direction ("continue this research", with the Layer 0–6 definition). This file,
`grounding/model.py`, `verify_grounding.py` and `test_grounding.py` are
committed before the frozen grid is run; the commit is the freeze. It has not
had Astra review, and no consciousness claim is made.

## 1. Question

The PI's thesis: systems with Layers 2–4 but without Layers 0–1 have
representations that are "extrinsically grounded by human evaluators rather
than anything intrinsically meaningful to the system".

**Q:** is there an operational difference between a variable that matters *to
an evaluator* and one that matters *to the system*, which survives the
strongest reduction (an external reward on the same variable)?

This is Track C's H3 / ablation C (the A-EXT arm) asked analytically, before
any agent is trained. It addresses the O3 arrow "content → future cognitive
machinery → future content" in its smallest form.

## 2. Definitions

A system has a body variable `e`, a memory channel from its past self to its
future self, and a policy. An objective is a functional of trajectories.

- `e` is **evaluator-consequential** when it enters only through the objective.
- `e` is **internally consequential** when it Blackwell-orders the system's own
  channels: for `e > e'` the memory channel at `e'` is a garbling of the one at `e`.
  This is the **fate** factor below ("fate-sharing" in the Track B/C notes).
- **Derived regulation:** the optimal policy acts to change `e` under an
  objective that never reads `e`.
- **Viability-relative semantic information** (after Kolchinsky & Wolpert):
  the loss in the system's own functional integrity when its information about
  `e` is scrambled with marginals preserved. Integrity here is the fidelity of
  the system's register.

Layer mapping: the fate factor is a minimal Layer 0 (one cognitive component's
reliability must be maintained; the register, the policy executor and the
energy physics stay SUPPLIED). Contingent control of `e` is Layer 1. The value
of knowing a hidden `e` is the Layer 2 link. The reliability of the system's
own register is a candidate Layer 4 referent.

## 3. Model

Body `e ∈ {0..E}`. Each trial writes a uniform cue bit into a 1-bit register;
after `d` decision steps the agent reports. At every delay step the register is
erased to a fair coin with probability `η(e)`, so fidelity
`f = 2·P(register = cue) − 1` updates as `f ← f·(1 − η(e))`. Actions: rest, or
forage at cost `κ`. Energy: `e' = clip(e + 2·food − decay, 0, E)`, with decay
w.p. `p_decay` under either action and food w.p. `p_food` only when foraging.
`N` trials; the register is rewritten perfectly at each trial start.

Two dynamics factors give four cells:

| | death off | death on (reaching e = 0 is absorbing, zero future reward) |
| --- | --- | --- |
| **fate off:** `η ≡ 1/4` (host-guaranteed machinery) | F0D0 | F0D1 |
| **fate on:** `η(e) = (E − e)/(2E)` | F1D0 | F1D1 |

Objectives (report payoffs; `q = (1+f)/2`). Only `H` reads `e`.

| Name | Payoff | Needs memory |
| --- | --- | --- |
| T1_gain | +1 correct, 0 wrong | yes |
| T2_penalty | 0 correct, −1 wrong | yes |
| T3_signed | +1 / −1 | yes |
| T4_anti | −1 correct, +1 wrong | yes |
| T5_memfree | +1 for any report | no |
| T6_abstain | +1 / −4, or abstain for 0 | yes |
| H_homeo | −1 per step while `e ≤ 1` (the A-EXT evaluator's reward) | no |

A shift `b ∈ {−1, 0, +1}` is added to every decision step while alive.

Frozen sizes: `E = 4, d = 4, N = 4`. Frozen grid (36 points):
`κ ∈ {1/200, 1/50, 1/20, 1/8}` × `p_food ∈ {1/4, 1/2, 3/4}` ×
`p_decay ∈ {1/4, 1/2, 3/4}`. Reference point for detailed tables:
`κ = 1/50, p_food = p_decay = 1/2`. Value of interoception uses 2 trials.
Ties between actions go to rest.

## 4. Theorems (proved here; the run checks the implementation)

**A. Relabeling.** For fixed dynamics, the optimal policies under an objective
do not depend on whether the objective is called intrinsic or external. So the
intrinsic/extrinsic difference cannot be located in the objective. If it
exists, it is in the dynamics.

**B. Shift invariance without death.** With death off, adding `b` per step
adds a constant to every policy's return, so optimal policies are unchanged.

**C. Blackwell monotonicity under fate.** In F1D0, for every objective that
does not read `e`, the optimal value is nondecreasing in `e`.
*Proof sketch.* The energy kernel is stochastically monotone in `e` for each
action, so two bodies `e_hi ≥ e_lo` can be coupled to stay ordered under the
same actions. The high agent simulates the low agent's body with private
randomness, copies its actions, and garbles its own register down to the low
agent's fidelity (possible because `η` is nonincreasing in `e`). It thereby
obtains exactly the low agent's return. Randomized history-dependent policies
do not beat the optimal Markov policy. ∎
The same argument holds for any utility over reports: maintaining `e`
is weakly valuable for *every* goal that uses the register, with no viability
term in the objective.

**D. No stakes.** In F0D0, for every objective that does not read `e` and
`κ > 0`: never foraging is strictly optimal, the value is constant in `e`, and
observing `e` has zero value.

**E. Termination is sign-relative.** In F0D1, if every reward the agent can
still receive is nonpositive (T2 with `b = 0`), or every extra alive step nets
a loss (T1 with `b = −1`: each step costs 1 and a report pays at most `q < 1`),
then never foraging is strictly optimal. Coupling: the never-forager dies no
later and, under F0, receives the same payoff on every report both agents make.

**F. External scrambling.** In F0D0 the register's fidelity is the same under
every policy, so no intervention on what the agent knows about `e` changes it.

## 5. Claims scored by the run

UNIVERSAL claims are theorem-backed. A failure at any grid point is an error in
the proof or the code and is reported as such.

| ID | Claim |
| --- | --- |
| U1 | F0D0: expected forages = 0 for T1–T6 at all shifts (D) |
| U2 | death off: optimal action table identical across shifts, all objectives (B) |
| U3 | F1D0: value nondecreasing in `e` for T1–T6; F0D0: constant in `e` (C, D) |
| U4 | F0D0: value of interoception = 0 for T1–T6 (D) |
| U5 | F0D1: forages = 0 for (T2, b=0) and (T1, b=−1) (E) |
| U6 | A-EXT agent (F0D0, H): scrambling its body input leaves register fidelity exactly unchanged (F) |
| U7 | F1D0: regret of T1's regulation under T2 is 0, of T3's under T4 is 0; T5 never forages |

REGION claims are strict effects that depend on parameters. The result is the
coverage map. A claim holding at 0 of 36 points fails for this model family.

| ID | Claim | Expected region (stated before the run) |
| --- | --- | --- |
| R1 | F1D0: forages > 0 for all five memory tasks (derived regulation) | where `κ` is small; at least `κ ≤ 1/50` |
| R2 | F0D1: forages > 0 for (T1, b=0) and (T5, b=+1) | everywhere |
| R3 | F1D0: value of interoception > 0 for all four affine memory tasks | where regulation is contingent on `e`; not at the cheapest `κ` if always foraging is optimal |
| R4 | F1D0, T1: scrambling the body input lowers both value and register fidelity | same region as R3 |
| R5 | F1D0: regret ratio of each affine task's regulation under each other ≤ 1/4 | wherever R1 holds |
| R6 | T6: both `m` and `abstain` are reached in one trial under F1D0, one option only under F0D0 | a non-empty region |
| R7 | A-EXT agent: scrambling lowers the evaluator's reward | where H's optimal policy is contingent |

Reported without a prediction: all F1D1 cells, T6 and H transfers, and the
blind plans.

## 6. Known answer used by the tests

Dev instance `E=2, d=2, N=1, e=1, κ=1/100`, T1, fate on, so `η = (1/2, 1/4, 0)`.
Step 1 gives `f = 3/4`. Forage leads to `e = 2, 2, 0, 1` with probability 1/4
each, so `E[f] = 3/4·(1/2·1 + 1/4·1/2 + 1/4·3/4) = 39/64` and
`q = 103/128`. Rest gives `E[f] = 3/4·(1/2·1/2 + 1/2·3/4) = 15/32`, `q = 47/64`.
Optimum: forage, value `103/128 − 1/100`.

## 7. Disclosure of pre-freeze exposure

- The tests and a 2-point dev grid (`E=2, d=2, N=2`) were run while writing the
  code. In the dev grid R3, R4 and R5 held at one point of two and R7 at neither.
- An earlier single-point design was replaced by the grid after the dev run
  showed that "always forage" can be optimal, which makes regulation
  non-contingent. The energy rule was changed, before any frozen-size run, from
  "foraging never loses energy" to the rule in §3, for the same reason.
- One frozen-size point was executed once for timing with all output discarded
  unread.
- No frozen-grid result was seen before this commit.

## 8. Admission questions

| # | Answer |
| --- | --- |
| Q1 | C0/C1 → C2 dependence; O3 arrow content → machinery → content |
| Q2 | Fate-sharing, and not an objective term or termination, is what makes regulation and self-information valuable across objectives |
| Q3 | Any UNIVERSAL failure; R1 at 0/36 (no derived regulation); R3 and R4 at 0/36 (no systemic value of self-information) |
| Q4 | External reward on the same variable (H under F0D0); termination only (F0D1) |
| Q5 | Track C H3 and ablation C have no pre-analysis of what the A-EXT arm can show; the synthesis lists this arrow as not established |
| Q6 | Success: Track C's H3 should test derived regulation with the viability weight at zero and an objective swap |
| Q7 | Failure: drop the claim that Layer 0 changes Layer 1–2 in this model class; re-examine the fate mechanism |
| Q8 | Analytic: exact DP and enumeration |
| Q9 | Organizational cognition |
| Q10 | §9 |
| Q11 | C1/C2 on a supplied first-order substrate; acquisition untouched |
| Q12 | O1-like (one maintained component); register, executor and physics supplied |
| Q13 | "Homeostatic reward makes a variable intrinsically meaningful" versus "only dependence of the system's own channels on it does" |

## 9. Claim ceiling

At most: in this finite model class, with optimal policies, the stated
equivalences and coverage facts hold. Not established: that any learner
acquires these policies; anything about trained networks or Track C agents;
production of machinery (O2); autopoiesis; that a simulated variable is
"meaningful" to anything; any phenomenal property.

## 10. Safety

Theorem C is instrumental convergence in exact form: a fate-shared agent has a
reason to protect its substrate under almost any goal. That is why X1–X5 are
structural and not procedural. Here the organism's state is
`(trial, step, e, f)`; there is no operator, stop or host variable in the
model, and a test asserts it. Nothing in this card supports putting an
operator stop inside an agent's world, and the earlier refusal of
shutdown-resistance training stands.

Prior art, from knowledge and not re-verified here: Blackwell 1953
(comparison of experiments); Keramati & Gutkin 2014 (homeostatic RL as reward);
Kolchinsky & Wolpert 2018 (semantic information and viability); Di Paolo 2005
(precariousness, adaptivity); Omohundro 2008 and Turner et al. 2021
(instrumental convergence); Man & Damasio 2019; Seth & Tsakiris 2018.
