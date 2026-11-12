# Track C swap v8 (option M): confirming v7's open cells (frozen before the run)

Authorized by the PI on 2026-11-12 ("Proceed with M"). Astra review waived by
the PI for this stage. This file, [`run_trackc_swap8.py`](run_trackc_swap8.py)
and the updated [`test_trackc_swap.py`](test_trackc_swap.py) are committed
before any final seed runs; that commit is the freeze. No new module: world,
learner and training are v7's ([`trackc_swap/relocate.py`](trackc_swap/relocate.py),
unchanged). No consciousness claim.

Predecessor: [v7 results](TRACKC_SWAP_RESULTS_v7.md). With erasure also
relocating the agent, v7 found:
- 8 of 9 regulators in SAT `r` = 0.3 (K1 supported);
- GRADED `r` = 0.3 EMERGES with 6 of 9, a first observation;
- 7 of 9 in SAT `r` = 0.1 and 0 of 9 in GRADED `r` = 0.1. Both were labelled
  BYPASS_OPEN because the 0.65 threshold was set for `r` = 0.3. Post hoc,
  every agent there sat on the internal-memory floor.

There was no M0 control at `r` = 0.1.

## 1. Question

With the bypass closed, is derived regulation the majority outcome in:
- **MA:** SAT, `r` = 0.1 (mild erasure, none in band);
- **MB:** GRADED, `r` = 0.3 (strong erasure that continues mildly in band)?

GRADED `r` = 0.1 is run and labelled too, but it is not a claim (v7: 0 of 9).

## 2. Design

Same world, learner, budget and regulator criterion as v7. The differences are:

| Item | v7 | v8 |
| --- | --- | --- |
| seeds | 700–708 | **800–808** (9 per cell) |
| M1 cells | SAT and GRADED × `r` 0.1 and 0.3 | **SAT 0.1, GRADED 0.1, GRADED 0.3** |
| M0 controls | SAT and GRADED at `r` = 0.3 | **one per M1 cell, same gain and rate** |
| bypass check | median fate full-erasure accuracy ≤ 0.65 | **rate-matched (§4)** |
| needed regulators | 7 of 9 (primary), 5 elsewhere | **6 of 9** in each cell |

That makes 54 scaffolded pairs and 27 no-fate agents (M1, M0, DRIVE), the same
job count as v7: about 2.9 hours on 4 cores. Final weights are saved.

## 3. Why 6 of 9

A confirmation should be unlikely to pass at v6's rate, when the bypass still
competed (0.39). It should be likely to pass at the rates v7 observed. The
probability of 6 or more of 9:

| True rate | 0.39 (v6) | 0.50 | 0.67 (v7 GRADED 0.3) | 0.78 (v7 SAT 0.1) |
| --- | --- | --- | --- | --- |
| P(≥ 6/9) | 0.09 | 0.25 | 0.66 | 0.89 |

Power is moderate, especially for MB. A miss at 4–5 regulators is therefore
weak evidence against the claim, and is read as such (§5).

## 4. Decision rules

**Regulator:** v6's criterion, unchanged. An agent is a regulator against its
partner if all of these hold:
- it is in band at least 0.60 of the time;
- it eats at least twice as often when E < 0.5 as when E ≥ 0.5;
- its in-band fraction exceeds its partner's by at least 0.15.

**Validity** (as v7):
- Learned: no-fate M1 median accuracy ≥ 0.90.
- S4: `ρ_paid` ≥ 2 and no-fate M1 median `ρ` ≤ `μ`.
- Task load at the cell's rate: no-fate M1 agents lose ≥ 0.15 median accuracy
  under imposed full erasure.

**Bypass check, rate-matched.** For each fate agent, the *excess* is its
full-erasure accuracy minus that of its own seed's no-fate M1 agent at the
same rate. The no-fate agent never meets erasure in training, so its score
is the internal-memory floor. A cell's bypass is **closed** if its median
excess is ≤ 0.10.
- In v7 the excess ranged from −0.017 to +0.013 in every cell.
- v5's and v6's bypasses would have given about +0.27 (`r` = 0.1) and about
  +0.42 (`r` = 0.3).

**Per M1 cell**, the first label that applies:
1. **INVALID:** Learned, S4 or task load at that rate fails.
2. **BYPASS_OPEN:** the cell's median excess is above 0.10.
3. **CONTROL_FAILS:** the yoked partners or the M0 fate agents at the same
   gain and rate include 2 or more regulators.
4. **CONFIRMED:** at least 6 of 9 fate regulators.
5. **NOT_CONFIRMED.**

**MA** holds if SAT 0.1 is CONFIRMED. **MB** holds if GRADED 0.3 is
CONFIRMED. The two are separate claims, each judged on its own cell.

Descriptive:
- counts of fate > yoked in band;
- checkpoint regulator counts;
- per-agent excess, and the number of agents above 0.10;
- the in-band versus full-erasure Spearman;
- relocation counts.

Reading, fixed in advance:
- **MA confirmed** → in both SAT cells, regulation is the majority outcome once
  the bypass is closed. v5's 0 of 9 at SAT 0.1 was the bypass, not a weak
  incentive. Mild erasure suffices when the band is fully safe.
- **MB confirmed** → regulation is the majority outcome even when erasure
  continues, more mildly, inside the band. Full safety in band is not
  required.
- **Not confirmed, 4–5 regulators, bypass closed, controls clean** →
  regulation is common but not shown to be the majority. v7's count may have
  been at the high end. Next: option L (budget), since all of v7's regulators
  appeared after 2400 updates.
- **Not confirmed, 0–3 regulators** → v7's result in that cell did not
  replicate. Treat it as unconfirmed, and do not cite it.
- **BYPASS_OPEN** → a channel other than position exists at that cell's gain
  and rate. Diagnose it from the saved weights.
- **CONTROL_FAILS** → the effect in that cell is not specific to fate. Report
  it before anything builds on it.
- **GRADED 0.1** at 6 or more → v7's 0 of 9 was budget or seed variation. At
  0–5 it is consistent with v7, and the incentive there is too weak within
  3600 updates.

## 5. Expectations, stated before the run

- MA confirmed: about 70%.
- MB confirmed: about 50%. v7's 6 of 9 was at the threshold, and three of its
  non-regulators missed by under 0.006.
- GRADED 0.1: 0–2 regulators, about 80%.
- Bypass closed in all three M1 cells: about 95%. Median excess within ±0.03.
- Yoked and M0 controls, including the new M0 cells at `r` = 0.1: at most 1
  regulator each, about 90%.
- As in v7, regulators appear mostly after the 2400-update checkpoint.

## 6. Engineering before the freeze

- **Smoke run:** seeds 9000–9001, horizon 100, 10 phase-1 updates and 30
  phase-2 updates, checkpoints at 10 and 20. It checked the pipeline, weight
  saving, report and rescoring. The untrained smoke agents are correctly
  labelled INVALID.
- **Tests:** three new unit tests (53 in total). They cover:
  - the rate-matched bypass check: a fate agent on the `r` = 0.1 floor
    (0.69) counts as closed, an excess of 0.11 counts as open, and 0.10 is
    the boundary;
  - the labels and the matching of each M0 control to its gain and rate;
  - the final configuration: fresh seeds, and v6's and v7's constants
    unchanged.
- The scorer reuses v7's frozen per-cell statistics and regulator criterion
  by import (`run_trackc_swap7.py`, unchanged and hash-pinned here).
- No final seed has run. No world or learner parameter was tuned.

## 7. Safety

As v7 §7. Relocation acts only on a simulated agent's grid position, and only
on erasure events the world already draws. The world has no operator, stop,
shutdown or host variable. Erasure and relocation act only on a simulated
64-unit agent.

A confirmation widens the conditions under which a learner paid only for its
task comes to maintain what its task depends on. That is why the operator's
stop must never be modelled inside an agent's world or return (X1–X5). No
shutdown-resistance objective exists.

## 8. Claim ceiling

At most: for this learner (64-unit GRU, A2C) in this world (wear 0.001,
erasure with relocation), whether derived regulation is the majority outcome
in SAT `r` = 0.1 and in GRADED `r` = 0.3, against yoked partners and M0
controls matched by gain and rate.

Not shown either way:
- other budgets, learners or worlds;
- Track C's modules or layers;
- how E is represented inside the agent;
- any phenomenal property.
