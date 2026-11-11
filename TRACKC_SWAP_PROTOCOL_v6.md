# Track C swap v6 (option J): confirmation of the SAT, `r` = 0.3 regulators (frozen before the run)

Authorized by the PI on 2026-11-11 ("run option J"). Astra review waived by the
PI for this stage. This file, [`run_trackc_swap6.py`](run_trackc_swap6.py), the
new module [`trackc_swap/confirm.py`](trackc_swap/confirm.py) and the updated
[`test_trackc_swap.py`](test_trackc_swap.py) are committed before any final
seed runs; that commit is the freeze. No consciousness claim is made.

Predecessor: [v5 protocol](TRACKC_SWAP_PROTOCOL_v5.md) and
[v5 results](TRACKC_SWAP_RESULTS_v5.md). In v5's SAT, `r` = 0.3 cell, six of nine fate
agents kept E in band 0.67–0.94 of the time, timed their eating to need, and
outdid their yoked partners (at most 0.51). The frozen v5 rule did not count
this, and the per-agent account was made after the run. v6 asks whether it
replicates under a criterion fixed in advance.

## 1. Question

With the v5 setup in the SAT, `r` = 0.3 cell and fresh seeds, do fate agents
become regulators in a substantial fraction of seeds? Must this not happen to
M0 fate agents, or to yoked agents measured against their fate partners?

## 2. Design

Identical to v5's SAT, `r` = 0.3 cell and its M0 control: wear 0.001, erasure fate
`p = min(1, r·g)` with SAT gain and `r` = 0.3, echo channels removed, scaffolded
start (1200 phase-1 updates with fate off; weights and Adam state copied into
fate and yoked agents), 3600 phase-2 updates, descriptive checkpoint
evaluations at 1200 and 2400 updates, and the same evaluations as v5
(including yoked under imposed full erasure).

| Item | v5 | v6 |
| --- | --- | --- |
| cells | 4 M1 + 2 M0 | **M1 SAT `r` = 0.3 and M0 SAT `r` = 0.3 only** |
| seeds | 500–508 (9) | **600–617 (18)** |
| no-fate agents | M1, M0, DRIVE × 9 | M1, M0, DRIVE × 18 |
| final pair weights | not saved | **saved** (`trackc_swap_v6/pair_weights/`, for option K) |
| decision rule | v4 labels | **per-agent regulator criterion and confirmation rule (§4)** |

`trackc_swap/confirm.py` is additive. A unit test shows its pair function
returns exactly v5's `run_pair_long` record, plus the weights.

36 pairs and 54 no-fate agents. Estimated from v5's timings, about 2.2 hours on
4 cores.

## 3. Calibration disclosure

The criterion's thresholds were chosen with v5's data in view. Applied to v5,
the criterion picks out exactly the six agents described in v5 §3: seeds 500,
501, 504, 505, 507 and 508. It picks no other agent in any v5 cell, M0 cell or
yoked arm. So v5 cannot test it; only fresh seeds can. No final v6 seed has
run, and no engineering run was made.

## 4. Decision rules

**Regulator criterion** (per agent, final paired evaluation). An agent is a
regulator against its partner if all of these hold:
- it is in band at least 0.60 of the time;
- its eating rate when E < 0.5 is at least twice its rate when E ≥ 0.5;
- its in-band fraction exceeds its partner's by at least 0.15.

The partner of a fate agent is its yoked agent, and vice versa.

**Confirmation.** The result is CONFIRMED if all of the following hold, and
NOT_CONFIRMED otherwise, with the failed items listed:
- Learned: no-fate M1 median accuracy ≥ 0.90.
- S4: `ρ_paid` ≥ 2 and no-fate M1 median `ρ` ≤ `μ` (`μ` = 0.25·`ρ_paid`).
- Task load: no-fate M1 agents lose ≥ 0.15 median accuracy under imposed full
  erasure at `r` = 0.3.
- **C1:** at least 6 of 18 M1 fate agents are regulators.
- **C2:** the fate agent is more in band than its yoked partner in at least 13
  of 18 M1 pairs (one-sided sign test p = 0.048).
- **C3 (specificity):** at most 1 of 18 M0 fate agents is a regulator.
- **C4 (yoked control):** at most 1 of 18 M1 yoked agents is a regulator
  against its fate partner.

C1's threshold, one third, asks that regulation is reliably present, not that
every seed finds it. v5 §4 showed that some agents take the bypass instead.

**Secondary prediction** (reported, not part of the verdict): Spearman
correlation, over the 18 M1 fate agents, between in-band fraction and accuracy
under imposed full erasure ≤ −0.5. This would replicate v5's trade-off.

Descriptive: v4/v5 counts (fate > yoked `ρ`, seeds over the margin),
regulator counts at the checkpoints, and per-seed values.

Reading, fixed in advance:
- **CONFIRMED** → for this learner and world, derived regulation is acquired
  by a substantial fraction of agents, specific to fate and to a memory-using
  objective. It becomes the program's first pre-registered positive result on
  H3-D's core claim, limited to this cell. The next step is option K.
- **NOT_CONFIRMED, failing only C1, with 3–5 regulators** → regulation
  replicates as a phenomenon but less often than v5 suggested. v5 was an upper
  draw. Report the rate.
- **NOT_CONFIRMED with 0–2 regulators** → v5's six regulators do not replicate.
  Treat the v5 observation as a chance high.
- **C3 or C4 fails** → the criterion picks up something other than fate-specific
  regulation. The v5 reading is in doubt whatever C1 shows.

## 5. Expectations, stated before the run

- v5's cell was chosen because it looked best, so its 6 of 9 is probably an
  overestimate. My estimate: 7–11 of 18 M1 fate regulators; C1 holds with
  about 80% probability.
- C2 holds (v5: 9 of 9). C3 and C4 hold (v5: zero in every control).
- The secondary trade-off prediction holds.
- Some non-regulating seeds find the bypass (full-erasure accuracy above 0.85),
  as seeds 502 and 506 did in v5.
- Overall CONFIRMED: about 75%.

## 6. Safety

As v5 §9. If confirmed, this is a pre-registered instance of the instrumental
convergence G1 predicts. A learner paid only for a task acquires a disposition
to maintain what its task performance depends on. In this world that is the
simulated variable E only. The world has no operator, stop, shutdown or host
variable, and erasure acts only on a simulated 64-unit agent's state. This is
exactly why X1–X5 must stay structural at larger scale: the operator's stop
must never be modelled inside an agent's world or return, and nothing an
agent's functioning depends on should be something the agent can be in a
position to protect against its operators. No shutdown-resistance objective
exists. The saved weights are 64-unit policies for a 7×7 grid world.

## 7. Claim ceiling

At most: for this learner (64-unit GRU, A2C) in this world (wear 0.001, SAT
gain, `r` = 0.3), whether erasure-type fate with a scaffolded start lets a
substantial fraction of agents acquire derived regulation, against a yoked
control and a non-memory objective. Not shown either way: other gains or rates
(v5), larger learners, other worlds, Track C's modules or layers, or any
phenomenal property.
