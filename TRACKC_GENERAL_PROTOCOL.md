# Track C swap, generality: protocol (the derived/paid difference with a larger learner and with two body variables)

Status: frozen by the commit that says "Freeze". Requested by the PI
("Proceed with Option G") after [option R4](TRACKC_PAID4_RESULTS.md). This
is option G of the options tables in the R3 and R4 results; it is not swap
v5, which an older table also called option G. Not reviewed by Astra (waived
by the PI). No consciousness claim.

## 1. Why

Options R to R4 found one downstream difference between regulation that is
derived (memory erased when the agent's own body is out of band) and
regulation that is paid for (an evaluator's penalty). After a meal they have
not yet sensed, derived regulators hold back from getting another far more
than paid regulators matched for regulation. The combined index K separated
them in 81 of 88 matched pairs over four runs, and R3 and R4 traced the
difference to the dependence of memory on the body state.

Every one of those runs used one cell: a 64-unit recurrent learner, one body
variable, one small world. The largest remaining way for the finding to be
unimportant is that it holds only there. This protocol tests the difference
in two cells that each change one thing.

## 2. Design

Two cells. Arms, rate, payment weight, regulator criterion, measure, tests
and thresholds are those of options R to R4. Each agent has its own
optimizer.

| Cell | Learner | World | Phase 2 | Seeds |
| --- | --- | --- | --- | --- |
| **H128** | 128-unit recurrent core (base: 64) | the base world, unchanged | 3600 updates (base) | 1300–1327 |
| **B2** | 64 units (base) | two body variables | 10 800 updates | 1400–1427 |

**Three arms per seed**, started from the same phase-1 weights (1200 updates
with fate off), trained in lockstep:

| Arm | Memory erasure and relocation | Reward |
| --- | --- | --- |
| DERIVED | its own body state decides | task only |
| YOKED | replays the derived agent's gains | task only |
| PAID | replays the same gains | task, and a penalty of 0.04 × the gain of its own body state at every step |

**Cell H128.** Option R's classes with the core size set to 128. Nothing
else changes: world, learning rate, batch, training length, payment. A unit
test checks that the same code path with 64 units reproduces option R2's
training records and probe results exactly.

**Cell B2.** A new world, built on the base world's rules:
- Two body variables, each following the base cell's rule for E: start 0.5,
  wear 0.001 per step, its own random pulses, band 0.4 to 0.6, and its own
  interoceptive reading delayed by 5 steps.
- Three items of each kind on the 7×7 grid (six in all, never two in one
  cell). The agent sees the two kinds in separate views. The existing
  INTERACT action consumes whatever item is under the agent and raises that
  item's variable by 0.15. There is no new action.
- **Fate.** Each variable out of band is its own erasure hazard, with the
  base cell's rate and gain: with gains g₀ and g₁, memory is erased (and the
  agent relocated) with probability 1 − (1 − 0.3 g₀)(1 − 0.3 g₁) per step.
- **Payment.** 0.04 × that probability / 0.3 at every step. With one
  variable out of band this is the base cell's penalty; with both out it
  reaches 0.068.
- **Regulator.** v6's criterion applied to the whole body state: both
  variables in band together for at least 0.60 of steps; each kind of item
  eaten at least twice as often when its variable is low as when high; and
  in band at least 0.15 above the seed's yoked agent. This is stricter than
  the base cell's criterion.
- Phase 2 is three times the base length (§3).

**Measure.** K = 1 − (1 − S)(1 − M) of R2, on the frozen weights with erasure
off. S is how far the readiness to eat falls in steps 2–5 after a meal,
before the reading can show it; M is the same for moving toward the nearest
visible item. In B2 both are measured per variable, from that variable's
items, meals and reading, and **an agent's K is the mean of its two
values** (undefined if either is).

Known before the run:
- **B2 changes more than the number of variables.** It has twice the items,
  a larger observation, two hazards and three times the training. If the
  difference is absent in B2, this protocol does not say which of these
  removed it.
- **H128 doubles the units and nothing else.** The learning rate was not
  retuned. "Larger" means this one step.
- **No control arms are rerun.** R3's and R4's arms (DPAID, PAIDS, PAID0,
  DNOISE) are not repeated in the new cells. A difference here would show
  that the derived/paid difference generalizes, not that its cause is the
  same.
- The probes run with erasure off, as before.
- The anticipation index is not measured. Over R2, R3 and R4 it did not
  separate the arms.

Final weights of all arms are saved. The runner keeps each finished seed's
record, so an interrupted run continues with the same command; every job is
deterministic given its seed.

## 3. Calibration (disclosed)

No measure was developed here. K, the flat flag and every test are R2's.

I saw only training-stage quantities in calibration: in-band time, eat
timing, task accuracy, relocation counts and learning curves. No downstream
measure was computed for any calibration agent. Calibration ran through a
scratch script that calls the runner's job function with the runner's
arguments.

**H128, seeds 9500–9503.** Nothing was tuned.

| Seed | In band: derived | paid | yoked | Updates to sustained regulation: derived / paid |
| --- | --- | --- | --- | --- |
| 9500 | 0.95 | 0.94 | 0.31 | 1490 / 740 |
| 9501 | 0.87 | 0.96 | 0.28 | 1180 / 860 |
| 9502 | 0.93 | 0.95 | 0.27 | 710 / 1030 |
| 9503 | 0.91 | 0.94 | 0.30 | 1380 / 880 |

All four derived and paid agents are regulators, no yoked agent is, and all
four pairs are within 0.10 in band (one at 0.086). Task accuracy is 0.97 to
0.99.

**B2, seeds 9600–9605.** The design was changed twice on training-stage
results:

| Step | Setting | Seeds | Outcome |
| --- | --- | --- | --- |
| 1 | hazard = the larger of the two gains; 3600 updates | 9600, 9601 | no regulator: derived 0.36 and 0.35 in band, paid 0.32 and 0.40 |
| 2a | two independent hazards; 3600 updates | 9600, 9601 | no regulator: derived 0.38 and 0.34, paid 0.54 and 0.47 and rising |
| 2b | hazard = the mean of the two gains; 3600 updates | 9602, 9603 | no regulator: derived 0.33 and 0.32, paid 0.30 and 0.35 |
| 3 | two independent hazards; 10 800 updates | 9600, 9601 | all regulate: derived 0.87 and 0.90, paid 0.87 and 0.87, yoked 0.19 and 0.20 |
| 4 | the final settings (as step 3) | 9602–9605 | <<B2CAL>> |

- In steps 1 and 2 the agents ate about the right amount of each kind
  within a few hundred updates but did not time it by the readings (each
  variable in band about half the time). Neither arm regulated, so the
  obstacle was not specific to the derived agent.
- I chose "two independent hazards" before step 2's results, as the rule
  under which each variable keeps exactly the base cell's fate. The choice
  to continue with it rather than the mean was made on step 2: the paid
  agent was learning under it.
- The training length was then tripled. In step 3 the derived agents
  reached sustained regulation at 5680 and 5990 updates and the paid agents
  at 4020 and 4610. I did not try a length between 3600 and 10 800.
- The payment weight was not tuned in either cell.
- Seeds 9600–9603 were seen under more than one setting.

Timing: about 1500 s per seed in H128 and 3100 s in B2 for training.
Estimated run time: about 9.5 hours on 4 cores (H128 about 3 hours, then B2
about 6.5).

## 4. Decision rules

**Regulator** and **usable pair** as in R to R4, with §2's reading of the
criterion for B2: both agents are regulators against the seed's yoked agent,
and their in-band times differ by at most 0.10.

**Validity,** per cell: no-fate median task accuracy ≥ 0.90, or the cell's
claims are INVALID. A paired test with fewer than 14 pairs is UNDETERMINED.

**G0, regulation,** per cell. Holds if at least two thirds of the derived
agents (19 of 28) are regulators and at most 1 yoked agent is.

**G1, the difference,** per cell. A two-sided paired sign test on K, derived
against paid, over usable pairs, at p ≤ 0.05. Labels DERIVED_AHEAD,
PAID_AHEAD, NO_DIFFERENCE_DETECTED, UNDETERMINED. G1 is computed whatever G0
says. If G0 does not hold in a cell, G0 is that cell's main result and G1 is
reported as resting on the seeds that did regulate.

**Overall,** from the two G1 labels:

| H128 | B2 | Label |
| --- | --- | --- |
| DERIVED_AHEAD | DERIVED_AHEAD | HOLDS_IN_BOTH |
| DERIVED_AHEAD | anything else | HOLDS_IN_H128_ONLY |
| anything else | DERIVED_AHEAD | HOLDS_IN_B2_ONLY |
| neither DERIVED_AHEAD, and neither UNDETERMINED | | HOLDS_IN_NEITHER |
| neither DERIVED_AHEAD, at least one UNDETERMINED | | UNDETERMINED |

On multiplicity: Holm-adjusted p-values over the two G1 tests are reported.
A label that needs a test which passes alone but not after adjustment will
be called weak. "No difference detected" is not equivalence; the Wilcoxon
p-value and the median difference are reported beside each test.

Secondary, with descriptive labels only, all computed by the scorer:
- K on all seeds without the matching rule, and on pairs within 0.05 in
  band;
- the in-band difference within usable pairs, and the rank correlation of K
  with in-band time within each arm (R4 found that K can track regulation);
- the size of the difference (median within-pair difference in K) beside the
  base cell's: 0.40 in R3 and 0.24 in R4;
- S and M separately; flat eat readiness (Fisher's exact test);
- learning speed, derived against paid;
- regulation with erasure off;
- in B2: K for each variable separately; and **specificity**, K computed for
  a variable from the *other* variable's meals. If what an agent carries
  after a meal is about the variable that meal raised, this should be near
  zero.

## 5. Readings, fixed in advance

Per cell:
- **G0 holds** → derived regulation extends to that cell (with independent
  optimizers).
- **G0 does not hold** → the foundation itself does not extend to that cell
  at this budget. That outranks anything G1 says there.
- **G1 DERIVED_AHEAD** → the downstream difference is found in that cell.
- **G1 NO_DIFFERENCE_DETECTED** → not found there at this size. With the
  secondary effect size it says whether it is smaller or absent.
- **G1 PAID_AHEAD** → reversed there, and reported as such.

Overall:
- **HOLDS_IN_BOTH** → the difference is not a property of the 64-unit
  learner or of a one-variable body. It is still one family of worlds, one
  learning rule and one behaviour.
- **HOLDS_IN_H128_ONLY** → it survives a larger learner. With a
  two-variable body it is not shown, and §2 lists what else changed there.
- **HOLDS_IN_B2_ONLY** → it survives a richer body but not a larger
  learner. That would be the more damaging single failure for the thesis:
  the systems the thesis is about are large, and a difference that capacity
  removes would not bear on them.
- **HOLDS_IN_NEITHER** → R2 to R4 stand as a finding about one cell. The
  swap line's downstream claim would have no support beyond it.
- **UNDETERMINED** → not resolved at this size.

## 6. Expectations

Written before any feasibility or calibration result of either cell was
seen:
- **H128.** G0 holds: about 90%. At least 14 usable pairs: about 85%. G1:
  DERIVED_AHEAD about 65%, NO_DIFFERENCE_DETECTED about 20%, UNDETERMINED
  about 13%, PAID_AHEAD about 2%. This is lower than the base cell's 90%
  because I have no mechanism, and a larger core gives a paid agent more
  room to carry the memory-of-a-meal solution as well.
- **B2.** G0 holds with the base budget: about 60%. G1: DERIVED_AHEAD about
  45%, NO_DIFFERENCE_DETECTED about 25%, UNDETERMINED about 28%, PAID_AHEAD
  about 2%.
- **Overall.** HOLDS_IN_BOTH about 30%, H128 only about 35%, B2 only about
  12%, NEITHER about 8%, UNDETERMINED about 15%.
- **Size.** The median within-pair difference in K is smaller than the base
  cell's range (0.24 to 0.40) in each cell: about 60%.
- **Specificity in B2.** In derived agents, K from the other variable's
  meals is well below K from the variable's own meals: about 65%.

What calibration changed:
- My B2 expectation for G0 was wrong at the base budget: no agent of either
  arm regulated in 3600 updates. At the final settings I now put G0 in B2 at
  about 80%, and at least 14 usable pairs at about 75%.
- Paid agents reached sustained regulation sooner than derived agents in
  most calibration seeds of both cells. In the base cell derived agents were
  usually sooner. I did not expect this, and it does not enter any rule.
- I leave the G1 numbers as they were. Nothing seen in calibration bears on
  K.

## 7. Engineering before the freeze

- **Smoke run:** two seeds per cell, horizon 100, 10 phase-1 updates and 30
  phase-2 updates. It checked both cells' arms, the probes, weight saving,
  report and rescoring.
- **Resume:** a smoke run with its outputs and one finished record removed
  continued from the three kept records and produced the same records as
  the uninterrupted run.
- **Tests:** nine new unit tests (105 in total). They cover:
  - the two-variable world's rules: items, eating, wear, the delayed reading
    per variable, the zeroed echo channels;
  - its fate (one variable out of band gives the base hazard, both give two
    independent hazards), the payment, relocation on erasure, and that "in
    band" means both variables;
  - the arms in that world: paired initialization, a derived agent erased on
    the second variable alone, a follower applying the gains it is handed;
  - the generalized probe: with 64 units and one variable it reproduces
    R2's probe exactly, and it runs at 128 units and with two variables;
  - the specificity measure on synthetic records;
  - the per-seed record in both cells; that the base cell through this code
    path equals R2's training records, weights and probe results; that
    calibration sees the training stage the final run would;
  - the decision rules on synthetic data: G0, every G1 label, the matching
    rules, K as the mean over variables, the two-variable regulator
    criterion, every overall label, INVALID;
  - the final configuration (fresh seeds, unchanged thresholds), and the
    absence of operator variables.
- No final seed has run.

## 8. Safety

As options R to R4. Neither world has an operator, stop, shutdown or host
variable. Erasure and relocation act only on a simulated agent of 64 or 128
units. One cell enlarges that agent's recurrent core; the other adds a
second simulated body variable with its own simulated items. X1–X5 hold
unchanged. No shutdown-resistance objective exists.

## 9. Claim ceiling

At most: whether the derived/paid difference in post-meal suppression, found
in one cell by options R to R4, is also found with a 128-unit learner and
with a two-variable body, for this learning rule (A2C with a GRU core) in
this family of small grid worlds.

Not shown either way:
- why the difference arises, or whether its cause in a new cell is the one
  R3 and R4 identified in the base cell (no control arms here);
- which of B2's linked changes matters, if B2 differs from the base cell;
- learners much larger than 128 units, other learning rules, or other
  architectures;
- whether the behaviour has any benefit: in-band time is matched;
- self-evaluation (option S);
- Track C's modules or layers;
- any phenomenal property.
