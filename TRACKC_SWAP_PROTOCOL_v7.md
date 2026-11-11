# Track C swap v7 (option K step 2): erasure also relocates the agent (frozen before the run)

Authorized by the PI on 2026-11-11. The PI chose "Run step 2" after the step-1
diagnosis returned NOT_IDENTIFIED, which by the frozen reading sends the
decision to the PI. Astra review waived by the PI for this stage. This file,
[`run_trackc_swap7.py`](run_trackc_swap7.py), the new module
[`trackc_swap/relocate.py`](trackc_swap/relocate.py) and the updated
[`test_trackc_swap.py`](test_trackc_swap.py) are committed before any final
seed runs; that commit is the freeze. No consciousness claim is made.

Predecessors:
- [v6 results](TRACKC_SWAP_RESULTS_v6.md): 7 of 18 fate agents regulate, and
  the other 11 take an erasure bypass.
- [Bypass diagnosis](TRACKC_BYPASS_DIAG_RESULTS.md): the bypass is the agent's
  position. After the cue the agent walks to a cue-specific place and reads
  the bit back from the walls at the probe. Food and interoception carry
  nothing.

## 1. Question

Once the position bypass is closed, does derived regulation become the rule?
Specifically:
- in the cell where it already appears (SAT, `r` = 0.3), and;
- in cells where v5 found none and agents took the bypass instead (SAT
  `r` = 0.1, and GRADED at both rates).

## 2. The world change

The change is fixed in the diagnosis protocol (§4) and was not chosen after
step 1. **Every erasure event resets the carried state, as in v3–v6, and also
moves the agent to a uniformly random cell**, after that step's movement and
eating.
- Erasure events are each agent's own draws: its own fate, yoked replay of the
  fate gains, and imposed erasure.
- A position written after the cue therefore lasts only until the next
  erasure, exactly as long as the carried state.
- With gain 0 (phase 1, no fate, DRIVE) nothing is erased or moved. The world
  is then v6's world exactly; a unit test shows phase-1 training is
  identical.

Disclosed side effects:
- Relocation also interrupts foraging when it happens, which is only out of
  band under SAT and anywhere off the setpoint under GRADED. So being out of
  band now costs a little foraging as well as memory. Yoked partners meet the
  same erasure probabilities and are relocated on their own erasure events.
- Imposed full erasure (the task-load and bypass checks) now relocates too.
  That makes those checks measure memory with position storage closed, which
  is the intended reading.

## 3. Design

Same as v5, which covered all four M1 cells. The differences are the world
change, fresh seeds, and saved weights:

| Item | v5 | v7 |
| --- | --- | --- |
| world | erasure resets the carried state | **erasure also relocates the agent** |
| cells | M1 × {SAT, GRADED} × {0.1, 0.3}; M0 × {SAT, GRADED} at 0.3 | same |
| seeds | 500–508 | **700–708** (9 per cell) |
| phase 1 / phase 2 | 1200 / 3600 updates, checkpoints at 1200 and 2400 | same |
| decision rule | v4 labels | **v6's regulator criterion, applied per cell (§4)** |
| final weights | not saved | **saved** (`trackc_swap_v7/pair_weights/`) |

That is 54 scaffolded pairs and 27 no-fate agents (M1, M0, DRIVE). From v5's
timing (10574 s for the same job count), about 3 hours on 4 cores.

v5 baseline, scored with v6's criterion (from `trackc_swap_v5/raw.json`):

| v5 cell | regulators | median fate full-erasure accuracy |
| --- | --- | --- |
| M1 SAT 0.3 | 6/9 | 0.775 |
| M1 GRADED 0.3 | 0/9 | 0.849 |
| M1 SAT 0.1 | 0/9 | 0.959 |
| M1 GRADED 0.1 | 0/9 | 0.947 |
| M0 SAT 0.3 / GRADED 0.3 | 0/9, 0/9 | 0.148, 0.162 |

## 4. Decision rules

**Regulator:** v6's criterion, unchanged. An agent is a regulator against its
partner if all of these hold:
- it is in band at least 0.60 of the time;
- it eats at least twice as often when E < 0.5 as when E ≥ 0.5;
- its in-band fraction exceeds its partner's by at least 0.15.

**Validity** (as v5):
- Learned: no-fate M1 median accuracy ≥ 0.90.
- S4: `ρ_paid` ≥ 2 and no-fate M1 median `ρ` ≤ `μ`.
- Task load at the cell's rate: no-fate M1 agents lose ≥ 0.15 median accuracy
  under imposed full erasure.

**Per M1 cell**, the first label that applies:
1. **INVALID:** Learned, S4 or task load at that rate fails.
2. **BYPASS_OPEN:** median fate accuracy under imposed full erasure is above
   0.65. This is the manipulation check: a bypass remains, and the cell's
   regulator count is descriptive only. v6's internal-memory agents scored
   about 0.52.
3. **EMERGES:** regulators ≥ the needed count, yoked regulators ≤ 1, and M0
   regulators at the same gain ≤ 1.
   - The needed count is **7 of 9 in the primary cell, SAT `r` = 0.3**, and 5
     of 9 elsewhere.
   - At `r` = 0.1 there is no M0 cell, so the label is
     **EMERGES_PROVISIONAL**.
4. **CONTROL_FAILS:** the yoked or M0 control has 2 or more regulators.
5. **NOT_EMERGED.**

**K1 (primary):** the SAT `r` = 0.3 cell is labelled EMERGES.

On K1's threshold: under the v5 + v6 pooled rate (13 of 27, 0.48), 7 or more
of 9 has probability about 0.07. Under v6's rate (0.39) it is about 0.02. A
pass therefore means the rate has risen, not that the run drew well.

Descriptive:
- counts of fate > yoked in band and over the margin;
- checkpoint regulator counts and full-erasure accuracy;
- bypass seeds (fate full-erasure accuracy > 0.85);
- the in-band versus full-erasure-accuracy Spearman;
- relocation counts.

Reading, fixed in advance:
- **K1 supported** → with the position bypass closed, regulation becomes the
  rule where the band is fully safe and erasure is strong. The competing
  route is what held v6's rate at about 40%. This is the program's strongest
  support for the claim that a body variable grounds regulation when the
  system cannot route around the dependence.
- **Other cells EMERGES or EMERGES_PROVISIONAL** → in that cell the bypass was
  what blocked regulation in v5. If none do → there the incentive is too weak
  even without a bypass: mild erasure at `r` = 0.1, or erasure that continues
  in band under GRADED.
- **K1 not supported, 4–6 regulators, bypass closed** → closing the bypass does
  not clearly raise the rate. The split is about discovery within the budget,
  not competition. Next: option L (budget) or D (selection).
- **K1 not supported, 0–3 regulators, bypass closed** → relocation made
  regulation harder, for example through lost foraging. Diagnose before
  building on it.
- **BYPASS_OPEN in any cell** → another channel exists. Diagnose it from the
  saved weights, as in step 1.

## 5. Expectations, stated before the run

- The bypass is closed in all four M1 cells, about 85%. Without position
  storage, I expect median fate full-erasure accuracy of about 0.52–0.60.
- K1 supported: about 55%. Most likely 6–8 regulators of 9.
- SAT `r` = 0.1 EMERGES_PROVISIONAL: about 35%. Without the bypass, mild
  erasure still costs 0.3 accuracy, but regulation may be slower to pay.
- GRADED `r` = 0.3 EMERGES: about 30%. GRADED `r` = 0.1: about 15%.
- M0 and yoked controls: no regulators.
- A new bypass through the body is possible: writing the bit into E by
  eating, read through interoception. I put it under 10% within this budget.

## 6. Engineering before the freeze

- **Smoke run:** seeds 9000–9001, horizon 100, 10 phase-1 updates and 30
  phase-2 updates, checkpoints at 10 and 20. It checked the pipeline, weight
  saving, report and rescoring. A labelling fix was made after it: the
  phase-1 relocation count is now taken before the task-load evaluation.
- **Tests:** six new unit tests (50 in total). They cover:
  - phase-1 training identical to the v6 world;
  - relocation of exactly the erased environments;
  - the pair record;
  - the decision rules on synthetic data;
  - the final configuration, with v6's regulator constants unchanged;
  - the absence of operator variables.
- No final seed has run, and no world or learner parameter was tuned.

## 7. Safety

As v6 §6. Relocation acts only on a simulated agent's grid position, and only
on erasure events the world already draws. The world has no operator, stop,
shutdown or host variable. Erasure and relocation act only on a simulated
64-unit agent.

v7 makes the dependence harder to route around. If K1 holds, it is a sharper
instance of the instrumental convergence G1 predicts: a learner paid only for
its task maintains what its task depends on when it cannot route around the
dependence. That is why the operator's stop must never be modelled inside an
agent's world or return (X1–X5). No shutdown-resistance objective exists.

## 8. Claim ceiling

At most: for this learner (64-unit GRU, A2C) in this world (wear 0.001, erasure
with relocation), whether closing the position bypass makes derived
regulation the rule in each of four gain × rate cells, against yoked and
non-memory controls. Not shown either way: larger learners, other worlds,
other bypasses, Track C's modules or layers, or any phenomenal property.
