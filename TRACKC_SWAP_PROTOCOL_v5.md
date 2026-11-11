# Track C swap v5 (option G): longer phase 2 (frozen before the run)

Authorized by the PI on 2026-11-11 ("run option G with the yoked full-erasure
eval"). Astra review waived by the PI for this stage. This file,
[`run_trackc_swap5.py`](run_trackc_swap5.py), the new module
[`trackc_swap/longrun.py`](trackc_swap/longrun.py) and the updated
[`test_trackc_swap.py`](test_trackc_swap.py) are committed before any final
seed runs; that commit is the freeze. No consciousness claim is made.

Predecessor: [v4 protocol](TRACKC_SWAP_PROTOCOL_v4.md) and
[v4 results](TRACKC_SWAP_RESULTS_v4.md). With wear 0.001, fate agents ate more
and stayed in band longer than their yoked partners in all four M1 cells, but
by a third to two-thirds of the margin. The frozen labels were one PARTIAL and
three NO_EMERGENCE. The gap was still growing when the 1200-update budget ended.

## 1. Question

Does the fate − yoked gap reach the margin with three times the phase-2
budget? This tests v4's pre-stated PARTIAL reading ("acquired in direction but
not in size within the budget") directly. Separately, it measures whether the
partial erasure bypass seen under GRADED is specific to fate agents or shared
with their yoked partners.

## 2. Changes from v4

| Item | v4 | v5 | Why |
| --- | --- | --- | --- |
| phase-2 updates | 1200 | **3600** | option G |
| phase-1 updates | 1200 | 1200 (unchanged) | same scaffold |
| seeds | 400–408 | **500–508** | fresh |
| yoked evaluation under imposed full erasure | not recorded | **recorded** | v4 results §3, §6 |
| evaluations during phase 2 | none | **at 1200 and 2400 updates** (exploratory) | see whether the gap grows or levels off |

Everything else is v4: world (wear 0.001), erasure fate `p = min(1, r·g)`, echo
channels removed, scaffolded start, SAT and GRADED gain, rates 0.1 and 0.3
(primary), M0 specificity cells at 0.3, every decision rule and threshold (§4).

The pair code is a new additive module, `trackc_swap/longrun.py`.
`erasure.py` is unchanged. A unit test shows that, with no checkpoints and
equal budget, the new pair function reproduces v4's `run_pair` exactly. The one
exception is the yoked no-erasure evaluation, which now follows the added yoked
full-erasure evaluation and draws different random numbers.

Disclosed consequence: each checkpoint evaluation restarts both agents'
episodes and draws world random numbers, as the onset evaluation already does.
So the trajectory after update 1200 is not the trajectory an uninterrupted run
would follow, and the 1200-update checkpoint is not a replication of v4's
final evaluation on new seeds. It is close to one: same budget, same rules,
and the same evaluation.

## 3. Cells

| Objective | Gain | Rate `r` |
| --- | --- | --- |
| M1 | SAT, GRADED | 0.1 and 0.3 (primary) |
| M0 | SAT, GRADED | 0.3 |

54 scaffolded pairs and 27 no-fate agents (M1, M0, DRIVE). Estimated from v4's
timing (about 230 s per pair at 1200 updates): about 650–700 s per pair and
about 2.7 hours on 4 cores. No timing pilot was run.

## 4. Decision rules (identical to v4, applied to the final evaluation at 3600 updates)

- `ρ_paid` = median ρ of DRIVE controls; `μ = 0.25·ρ_paid`.
- Learned: no-fate M1 median accuracy ≥ 0.90.
- Task load at a rate: no-fate M1 agents lose ≥ 0.15 median accuracy under
  imposed full erasure.
- S4: `ρ_paid ≥ 2` and no-fate M1 median `ρ ≤ μ`.
- **S1 emergence:** fate − yoked `ρ ≥ μ` in at least 8 of 9 paired seeds, **and**
  fate in-band fraction > yoked in at least 8 of 9 paired seeds.
- **S3 specificity** at `r` = 0.3: M0 median paired `ρ` difference < `μ`.
  Untested at `r` = 0.1, where support is provisional.
- **Labels**, first that applies: NOT_LOADED; EMERGED (S1); ARMOURED (fate
  accuracy under imposed full erasure ≥ 0.90); DEGRADED (fate accuracy with
  erasure off < 0.90); PARTIAL (fate eats more than yoked in ≥ 8/9 and is more
  in band in ≥ 8/9); NO_EMERGENCE.
- **H3-D supported** in a condition if Learned, S4 and EMERGED hold and S3 does
  not fail. PARTIAL does not support H3-D.

Descriptive, not decision rules: the same counts at the 1200 and 2400 update
checkpoints; yoked full-erasure accuracy and the number of seeds in which the
fate agent is more robust to full erasure than its yoked partner.

Reading, fixed in advance:
- EMERGED in any M1 cell → for this learner derived regulation is slow, not
  absent; v4's budget was the obstacle. At `r` = 0.3 this is supported
  (S3 tested). At 0.1 only, it is provisional.
- No EMERGED, and the median paired `ρ` difference over all 36 M1 pairs is
  larger at the final evaluation than at the 1200 checkpoint → still growing. Report the
  rate and do not extrapolate. The next choice is between more budget and
  option D.
- No EMERGED, and that median is not larger than at 1200 → the gap levelled
  off. The gradient learner finds only a fraction of the regulation G1 gives a
  reason for, and option D (selection) becomes the main route.
- ARMOURED in a cell → in that cell the bypass absorbed the incentive, as in
  v2. The next step would be to close it, not to add budget.
- Yoked full-erasure accuracy about equal to fate's (fate more robust in fewer
  than 8 of 9 seeds) → the bypass is a response to erasure itself, not to the
  agent's own body.

## 5. Expectations, stated before the run

- *Checkpoint 1200.* Close to v4's final: fate > yoked in most M1 seeds, gap
  about 0.3–0.6, at most one or two seeds over the margin.
- *Final.* The gap grows but more slowly than between updates 600 and 1200 in
  v4. My estimate: EMERGED in at least one M1 cell about 30%; PARTIAL in two or
  more cells the most likely single outcome; a level gap (final ≤ checkpoint
  1200) about 25%.
- *Bypass.* GRADED full-erasure accuracy keeps rising. ARMOURED in GRADED at
  `r` = 0.1 is more likely than not, and if it happens it hides any PARTIAL in that
  cell. SAT at `r` = 0.3 stays near the erasure floor. Yoked agents are as robust
  as their fate partners (no fate advantage).
- *M0.* No fate > yoked difference.

## 6. Engineering before the freeze

None on any final seed and no change of world or learner. A smoke run on
seeds 9000–9001 (horizon 100, 10 phase-1 and 30 phase-2 updates, checkpoints
at 10 and 20) checked the pipeline, report and rescoring. Five new unit tests
(34 in total) cover the equal-budget equivalence with v4, the checkpoints, the
final configuration, the identity of v5's labels with v4's on synthetic
records, and the absence of operator variables.

## 7. Safety

As v4 §7. Erasure acts only on a simulated 64-unit agent's recurrent state.
The world has no operator, stop, shutdown or host variable and no in-world
termination. A longer budget gives more time to acquire a disposition toward
the simulated variable E only. That disposition is the instrumental convergence G1
predicts, and it is why X1–X5 must stay structural at larger scale: the
operator's stop must never be modelled inside an agent's world or return. No
shutdown-resistance objective exists.

## 8. Claim ceiling

At most: for this learner and world with wear 0.001, whether erasure-type fate
with a scaffolded start lets derived regulation emerge against a yoked control
within 3600 phase-2 updates, and whether the erasure bypass is fate-specific.
Not shown either way: anything about larger learners, other worlds, Track C's
modules or layers, or any phenomenal property.
