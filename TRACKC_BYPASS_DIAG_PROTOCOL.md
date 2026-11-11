# Track C swap, option K step 1: locating the erasure bypass (frozen before the run)

Authorized by the PI on 2026-11-11 ("Proceed with Option K"). Astra review
waived by the PI for this stage. This file,
[`run_trackc_bypass_diag.py`](run_trackc_bypass_diag.py), the new module
[`trackc_swap/bypass.py`](trackc_swap/bypass.py) and the updated
[`test_trackc_swap.py`](test_trackc_swap.py) are committed before the
diagnosis runs on any v6 agent; that commit is the freeze. No training. No
consciousness claim.

Option K has two steps, each with its own freeze:
1. **This step:** find out what v6's bypass agents use to hold the cue bit
   through erasure.
2. **Next step:** remove that channel from the world and rerun. The world
   change that follows from each outcome is fixed here (§4), so the rerun does
   not choose it after seeing the result.

## 1. Question

In v6, 11 of 18 fate agents keep 0.86–0.99 task accuracy when their carried
state is erased with probability 0.3 every step. Holding the bit in the
recurrent state through a 9-step delay would survive only about 4% of the
time (0.7⁹). So the bit must be held somewhere erasure does not reach. The
echo channels were removed in v3. What remains of the observation is:
- the 5×5 egocentric view of walls (25 inputs) and food (25);
- interoception: E five steps ago, with noise (1 input);
- the cue and probe channels, which say nothing about the target at the probe.

The candidates are:
- **position:** the agent stores the bit in where it stands, read through
  walls or food;
- **the body:** the agent stores the bit in E, by eating or not, read through
  interoception.

## 2. Method

Inputs: v6's committed weights for the 18 M1 seeds (600–617). For each seed
there are three agents: FATE and YOKED (`trackc_swap_v6/pair_weights/`) and the
no-fate phase-1 agent (`trackc_swap_v6/phase1_weights/`). That is 54 agents.
Each is run in the v6 world (echo-free, SAT, wear 0.001) on a fresh world seed
stream, with 128 environments for 4 episodes per condition, and no learning.

Conditions:
- **intact:** no erasure.
- **full:** the carried state is erased with probability 0.3 every step. This
  is v6's imposed-full-erasure evaluation.
- **memoryless:** erased every step, so each action depends on the current
  observation only.

**Shuffles.** Within full and memoryless, one channel group is shuffled across
environments on the probe step and the two steps before it. The groups are
walls, food, intero, view (walls and food) and all (view and intero). The
shuffle keeps each channel's distribution and breaks its link to that
environment's cue.

**Descriptive.** Recorded under memoryless:
- a two-fold cross-validated decoder of the target from the agent's cell at
  the probe;
- interoception at the probe, by target.

Each agent is assigned to a group by v6's frozen scores:
- *regulator_fate*: 7 agents;
- *bypass_fate*: fate full-erasure accuracy above 0.85, 11 agents;
- *other_fate*: 0 agents;
- *yoked*: 18;
- *nofate*: 18.

## 3. Decision rules

- **External store** (per agent): memoryless accuracy ≥ 0.75.
- **Channel carries the bit** (per agent and group, under full): the shuffle
  removes at least half of the above-chance accuracy:
  `acc_full − acc_shuffled ≥ 0.5 · (acc_full − 0.5)`. This is judged only for
  agents with `acc_full ≥ 0.75`.
- **Verdict.** IDENTIFIED: *g* requires both of these:
  - at least 9 of the 11 bypass fate agents store externally;
  - group *g* carries the bit in at least 9 of them.

  Groups are tried in the order walls, food, intero, view, all, and the first
  that qualifies is named. Otherwise the verdict is NOT_IDENTIFIED.

Descriptive, not part of the verdict:
- the same counts for regulators, yoked agents and no-fate agents;
- the memoryless shuffles;
- the cell decoder;
- interoception by target.

## 4. Readings and the world change each implies (fixed in advance)

- **IDENTIFIED: walls, food or view** → the bypass is the agent's position,
  stored by moving and read through the view. **Step 2's world change:
  erasure also relocates the agent.** Each erasure event resets the carried
  state, as before, and also moves the agent to a uniformly random cell. The
  same applies to yoked replay and to imposed erasure. A position written
  during the delay then lasts only as long as the carried state does, so it
  can no longer outlast erasure. Nothing else changes: gain rules, rates, world
  and learner are as before. In band under SAT, nothing is erased or moved.

  This is the smallest change that closes a position store without blinding
  the agent or interrupting foraging. I considered three alternatives:
  - **Relocating at the probe:** this leaves a one-step bypass.
  - **Relocating at fixed times:** the agent can re-write its position after
    each move.
  - **Blanking the view:** this harms foraging.
- **IDENTIFIED: intero** → the bypass runs through the body variable itself:
  the agent writes the bit into E by eating. No world change is fixed for
  this case. Interoception cannot be removed without removing what regulation
  needs. I report and return to the PI.
- **IDENTIFIED: all** (no smaller group qualifies) → the bit is spread across
  view and interoception. Step 2 uses relocation as above, and the rerun
  reports whether interoception alone still carries it.
- **NOT_IDENTIFIED** → the bypass is not in the observation at the probe, or
  is not found by this method. No step 2 until I report to the PI.

## 5. Expectations, stated before the run

- IDENTIFIED: walls about 60%; view (walls and food together, neither alone)
  about 15%; intero about 10%; NOT_IDENTIFIED about 15%.
- The 7 regulators store internally: memoryless accuracy below 0.75 in at
  least 6 of 7. They score near the v6 floor under full erasure.
- Yoked partners match their fate partners: external where the fate partner
  is a bypass agent.
- No-fate M1 agents are not external (v6 full-erasure accuracy about 0.52).
- Under full, each agent's accuracy is close to its v6 value (fresh world
  seeds; v6 used 2 episodes).

## 6. Engineering before the freeze

- **Smoke run:** two smoke-test agents from v6's pipeline check (seeds
  9000–9001, never trained to competence), on a 100-step horizon. This
  checked the pipeline, report and rescoring.
- **Timing:** one condition on one of those agents, at the final size, took
  0.8 s. The full diagnosis should take a few minutes on 4 cores.
- **Tests:** five new unit tests (44 in total) cover:
  - the channel-group indices;
  - the cell decoder;
  - determinism;
  - the carriage and identification rules on synthetic records;
  - the absence of operator variables.
- No v6 agent was evaluated before the freeze.

## 7. Safety

No training. Saved 64-unit policies are run in a simulated 7×7 world with no
operator, stop, shutdown or host variable. The step-2 world change applies
only to the simulated agent's position and carried state, and only on
erasure events the world already draws. X1–X5 hold unchanged. No
shutdown-resistance objective exists.

## 8. Claim ceiling

At most: which observation channel v6's bypass agents read the cue bit from
when their carried state is erased. Not shown: how the bit is written, whether
the same holds at other gains or rates, or anything about larger learners,
Track C's modules or layers, or any phenomenal property.
