# Grounding analysis G1: results

**ANALYTIC card. Exact rational computation on a finite model with optimal
policies. No learner, no training, no consciousness claim.**

Protocol frozen at commit `7f8fd60`
([GROUNDING_PROTOCOL_v1.md](GROUNDING_PROTOCOL_v1.md)); the 36-point grid was
run once afterwards (185 s). Outputs: [grounding_v1/REPORT.md](grounding_v1/REPORT.md),
[grounding_v1/results.json](grounding_v1/results.json). The protocol's §7
lists what was seen before the freeze. Not yet reviewed by Astra.

## 1. The question and the answer

The PI's thesis is that systems without Layers 0–1 have Layer 2 content that
is grounded by evaluators and not by anything that matters to the system. The
analysis asks what, operationally, makes a variable matter *to the system*.

The answer in this model class has four parts.

1. **Not the objective.** Calling an objective intrinsic changes nothing
   (Theorem A). A homeostatic reward makes a variable matter to an evaluator.
2. **Not death.** With termination alone, maintenance follows the sign of the
   evaluator's reward. Under a penalty-only objective the optimal agent lets
   itself die.
3. **Fate-sharing.** When the reliability of the system's own memory depends
   on the body variable, maintaining that variable is valuable under every
   goal that uses memory, with no viability term in the objective and
   regardless of the reward's sign or offset (Theorem C).
4. **The largest effect is on self-evaluation, not on control.** Under
   fate-sharing the system's own reliability depends on its body history, and
   knowing it is worth a median 13% of the optimal value. Knowing the body in
   order to regulate it is worth a median 0.3%.

## 2. Model in one paragraph

A body variable `e` decays and is restored by foraging at cost `κ`. A 1-bit
register must hold a cue across a 4-step delay. With **fate on**, the register's
erasure rate rises as `e` falls. With **fate off**, the rate is constant
(host-guaranteed machinery). With **death on**, reaching `e = 0` ends all future
reward. Six task objectives never read `e`; `H_homeo` is the evaluator's
reward for keeping `e` up. Every number is an exact optimum.

## 3. Theorem-backed claims: 7 of 7 hold at 36 of 36 points

| ID | Claim | Result |
| --- | --- | --- |
| U1 | fate off, death off: no task objective ever forages | 36/36 |
| U2 | death off: adding a constant to every step's reward never changes the optimal policy | 36/36 |
| U3 | fate on: value never decreases in `e`, for every task; fate off: value does not depend on `e` | 36/36 |
| U4 | fate off, death off: observing `e` is worth exactly 0 for every task | 36/36 |
| U5 | death only: no maintenance under a penalty-only objective, or when each alive step costs more than it earns | 36/36 |
| U6 | evaluator-paid homeostat on host-guaranteed machinery: scrambling its body input leaves its memory fidelity exactly unchanged | 36/36 |
| U7 | objectives that differ by a constant or by relabeling yield the same regulation; the memory-free task never forages | 36/36 |

## 4. Parameter-dependent claims: coverage

| ID | Claim | Holds at | Expected region (stated before the run) |
| --- | --- | --- | --- |
| R1 | fate on: every memory task forages, with no viability term | 33/36 | `κ ≤ 1/50`: confirmed, and wider |
| R2 | death only: maintenance appears when the reward stream is positive, even for the memory-free task | 36/36 | everywhere: confirmed |
| R3 | fate on: observing `e` has positive value for all four affine tasks | 25/36 | intermediate `κ`: confirmed |
| R4 | fate on: scrambling the body input lowers both value and memory fidelity | 29/36 | as R3: confirmed |
| R5 | fate on: each task's regulation policy is within 25% regret under the others | 28/36 | wherever R1 holds: **not confirmed** (28 of 33) |
| R6 | abstain task: both "report" and "abstain" are reached under fate, only one without | 36/36 | non-empty: confirmed everywhere |
| R7 | scrambling the evaluator-paid homeostat costs the evaluator | 36/36 | where contingent: confirmed everywhere |

R1 fails only at the highest forage cost with poor food or fast decay, where
foraging is not worth it. R3 and R4 fail where regulation is not contingent
on the body: at the cheapest `κ` a fixed, near-constant forage schedule is
already optimal, and at the highest `κ` with poor food there is little or no
foraging. R5's misses are all at `κ ≥ 1/20`. There the right amount of foraging
depends on the stakes of the particular task, and a policy tuned for one task
can do worse on another than not foraging at all.

## 5. Reference point (`κ = 1/50`, `p_food = p_decay = 1/2`)

Expected forage actions out of 16 steps under the optimal policy:

| Objective | fate off, death off | fate on, death off | death only | fate and death |
| --- | --- | --- | --- | --- |
| T1 gain (+1 / 0) | 0 | 14.30 | 6.22 | 13.97 |
| T2 penalty (0 / −1) | 0 | 14.30 | 0 | 0.07 |
| T3 signed (+1 / −1) | 0 | 14.97 | 6.22 | 14.55 |
| T4 anti (−1 / +1) | 0 | 14.97 | 6.22 | 14.55 |
| T5 memory-free | 0 | 0 | 8.76 | 8.76 |
| T6 abstain | 0 | 14.62 | 0 | 14.34 |
| H homeostatic reward | 13.57 | 13.57 | 13.18 | 13.18 |

With a reward of −1 per alive step, the two death-off columns are unchanged and
every entry in the two death-on columns drops to 0.04 or less, including the
homeostat's. With +1 per alive step, the death-only column rises to between
10.8 and 13.2 for every objective, including the memory-free one.

Mean register fidelity at report under the T1 optimum is 0.784 with fate on
and 0.316 with fate off.

## 6. Findings

**F1. Without fate-sharing, the body has no standing except through the
evaluator.** No task forages, the value function ignores `e`, and observing
`e` is worth nothing (U1, U3, U4). The homeostat forages 13.6 times, entirely
because it is paid to. Scrambling what it knows about `e` costs the evaluator
0.119 and changes nothing in the system's own functioning (U6). This is an
exact form of "extrinsically grounded".

**F2. With fate-sharing, regulation is derived, and it does not depend on the
reward convention.** Every memory task forages about as much as the paid
homeostat, with no term for `e` in its objective. Penalty-only, sign-flipped
and offset objectives give the same or nearly the same policy (U2, U7, R1).
The memory-free task forages 0: the effect requires that the goal use the
precarious component.

**F3. Termination is not the active ingredient, and it can undo F2.**
- Death alone produces maintenance only when being alive pays: 6.2 forages for
  T1, 0 for the penalty-only T2, and 8.8 for the memory-free task.
- With fate and death together, the penalty-only agent forages 0.07 times and
  survives the horizon with probability 0.019. Across the grid its survival is
  below 0.1 at 22 of 36 points; it survives where food is plentiful and
  maintaining the body costs almost nothing.
- So an "existential threat" modelled as a terminal state makes
  self-maintenance a function of the evaluator's sign convention. Graded
  dependence of capacity on the body does not.

**F4. An evaluator-paid homeostat is nearly indistinguishable under one
objective.** On the fate-shared substrate, the homeostat's regulation policy
loses a median 5% of the achievable gain when scored on T1 (within 25% at 27
of the 33 points where regulation exists). Its forage rate equals its rate on
host-guaranteed machinery at every grid point. A comparison under a single
objective cannot separate "regulates because paid" from "regulates because its
own machinery depends on it". Swapping the objective separates them: remove
the payment and the first agent's regulation goes to zero (U1), while the
second agent's persists (R1).

**F5. Contingent control of the body is worth little here; knowing one's own
reliability is worth a lot.**

| Quantity (fate on, death off) | Median over grid | Range |
| --- | --- | --- |
| value of observing `e`, T1, as % of the optimal value | 0.3% | 0 to 3.4% |
| value loss from scrambling the body input, T1 | 1.1% | 0 to 11% |
| fidelity loss from the same scramble | 0.017 | 0 to 0.18 |
| value of observing `e`, T6 abstain | 12.8% | 0.1 to 100% |
| value loss from scrambling, T6 abstain | 52% | 0.3% to above 100% |

For the affine tasks a nearly fixed forage schedule is close to optimal, which
matches the program's earlier reductions of learned maintenance to a tuned
duty level. The abstain task differs because its payoff depends on whether
the register can be trusted *this time*. Under fate that depends on the
system's own body history; under host-guaranteed machinery it is a constant,
and the optimal report rule is the same in every state (R6, 36/36).

**F6. Hypothesis from F5: Layer 0 supplies the referent for Layer 4.** On
host-guaranteed machinery, the system's reliability varies only with the
evidence, so a confidence signal can always be reduced to a first-order
statistic. That is the pattern in AC117 and in the theory queue's C4
reductions. When machinery is precarious, reliability also varies with the
system's own state, which is the "system versus evidence" dissociation the
distinct-evaluation criterion asks for. This is a hypothesis for a future
card, not a result about metacognition.

## 7. What this changes for Track C

1. **H3 / ablation C.** A-EXT compared under one objective will reproduce the
   intrinsic arm (F4, Theorem A). The discriminating design is an **objective
   swap with the viability weight at zero**: train on a task that never reads
   the body, and test whether regulation appears under fate and not under the
   yoked-noise control. Then swap the task and test whether regulation persists.
2. **Termination bookkeeping.** With a terminal viability exit, regulation
   depends on the sign and offset of the return (F3). Report results under at
   least two reward offsets, or keep termination out of the return and let the
   degraded substrate carry the cost.
3. **Yoked control.** The fate-off cell here is the "comparable noise, no
   dependence on own state" control that Astra #41 asked for. It should be the
   primary contrast, ahead of `E = ∞`.
4. **H4.** Give the metacognitive head a target that fate-sharing makes
   non-trivial: the reliability of a component whose noise depends on the
   body. Test the head with the system-versus-evidence pair of interventions.
5. **Layer 1 expectation.** Expect a fixed maintenance schedule to be a strong
   rival for contingent regulation (F5). Size H3's margins accordingly.

## 8. Limits

- Optimal policies in a tiny model. Whether any learner acquires them is
  Q-LEARN and untouched.
- Only one component is precarious. The register, the policy executor and the
  physics are supplied, so this is O1-like maintenance of state reliability,
  not production of machinery (O2).
- The fate-off noise level (1/4) is a design choice. The universal claims do
  not depend on it; the effect sizes do.
- The value-of-interoception numbers use 2 trials and compare a fully
  observed body with a fully hidden one.
- Effect sizes are for this grid. R5 missed its stated region.
- "Matters to the system" here means "orders the system's own channels". That
  is a functional definition. It says nothing about experience, and Layer 6 is
  outside this card.

## 9. Safety

Theorem C and F2 are instrumental convergence in exact form: a fate-shared
agent has a reason to protect its substrate under nearly any goal. Any agent
built this way would have that reason toward whatever it models as affecting
its substrate. X1–X5 therefore have to hold by construction: simulated
variables only, and the operator's stop kept outside the agent's world and
return. The model here contains no operator, stop or host variable.

## 10. Reproduce

```bash
python -m unittest -v test_grounding
python verify_grounding.py --config frozen --out reproduced_grounding   # ~3 min on 4 cores
```
