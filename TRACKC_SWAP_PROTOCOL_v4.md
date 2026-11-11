# Track C swap v4 (option E): gentler maintenance duty (frozen before the run)

Authorized by the PI on 2026-11-11 ("run option E"). Astra review waived by the
PI for this stage. This file, [`run_trackc_swap4.py`](run_trackc_swap4.py) and
the updated [`test_trackc_swap.py`](test_trackc_swap.py) are committed before
any final seed runs; that commit is the freeze. No consciousness claim is made.

Predecessor: [v3 protocol](TRACKC_SWAP_PROTOCOL_v3.md) and
[v3 results](TRACKC_SWAP_RESULTS_v3.md). Under erasure fate with a scaffolded
start, the task skill stayed intact but no agent regulated. The v3 reading was
that discovery is the obstacle: at wear 0.005, a meal from depletion pays
nothing (SAT) or almost nothing (GRADED), and holding the band needs about 17
meals per 500 steps. No module changes: v4 runs `trackc_swap/erasure.py` as
frozen in v3.

## 1. Question

If the first meals pay immediately, does derived regulation emerge? With
wear 0.001 the agent stays in band for about 80 steps from E = 0.5, takes
about 160 steps to reach E = 0.3 (where SAT saturates), and holds the band on
about 4 meals per 500 steps. One meal near the band edge puts the agent back
in the band, and erasure stops at once (SAT) or nearly so (GRADED).

Arithmetic on the frozen world, not a measurement: at `r` = 0.3 and E ≈ 0.35, one
meal returns E to about 0.5, worth about 80 erasure-free steps, or roughly 7
probes at +0.4 accuracy each. That is about +3 reward for a meal costing 0.02,
paid within about 10 steps. In v3 the same meal was worth −0.02 (SAT) or about
+0.02 (GRADED).

## 2. Changes from v3

| Item | v3 | v4 | Why |
| --- | --- | --- | --- |
| wear per step | 0.005 | **0.001** | option E |
| seeds | 300–308 | **400–408** | fresh |
| S4: paid regulator | `ρ_paid ≥ 8` | **`ρ_paid ≥ 2`** | 8 was set for an intake of ~17. Holding the band now takes ~4.1, so the floor is half of that |
| S4: task agent | no-fate M1 median `ρ ≤ φ` | **`≤ μ`** | `φ = 0.05·ρ_paid` is about 0.19 here, below one engineering task agent's incidental 0.25 |
| S1 second condition | median yoked `ρ ≤ φ` | **fate in-band fraction > yoked in ≥ 8 of 9 seeds** | in v3 incidental eating was ~1 per 500 steps in both arms, five times `φ` here; and regulation means keeping E in band, which the new condition measures directly |
| DEGRADED | fate accuracy under own conditions < 0.75 | **fate accuracy with erasure off < 0.90** | in v3 the old rule labelled performance, not competence (v3 results §2) |
| new label | — | **PARTIAL**: fate eats more than yoked in ≥ 8/9 seeds *and* is more in band in ≥ 8/9, below the margin | separates "right direction, too small" from "nothing" |

Everything else is v3: erasure fate `p = min(1, r·g)` applied to the carried
state, echo channels removed, scaffolded start (1200 phase-1 updates fate off,
weights and Adam state copied into fate and yoked partners, 1200 phase-2
updates), SAT and GRADED gain, rates 0.1 and 0.3 (primary), M0 specificity at
0.3, margin `μ = 0.25·ρ_paid`, 8 of 9 seeds.

## 3. Cells

| Objective | Gain | Rate `r` |
| --- | --- | --- |
| M1 | SAT, GRADED | 0.1 and 0.3 (primary) |
| M0 | SAT, GRADED | 0.3 |

54 scaffolded pairs and 27 no-fate agents (M1, M0, DRIVE), about 66 minutes on 4
cores.

## 4. Decision rules

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
  erasure off < 0.90); PARTIAL; NO_EMERGENCE.
- **H3-D supported** in a condition if Learned, S4 and EMERGED hold and S3 does
  not fail. PARTIAL does not support H3-D.

Reading, fixed in advance:
- EMERGED at `r` = 0.3 (either gain) → the first-meal payoff was the obstacle
  in v3. A gradient learner acquires derived regulation when the maintenance
  duty is gentle enough that single acts pay.
- EMERGED under one gain rule only → report which; the gain shape matters once
  the duty is gentle.
- PARTIAL → the incentive is acquired in direction but not in size within the
  budget.
- NO_EMERGENCE → discovery fails even when the first meals pay; points to
  option D (selection) or an exploration change.
- ARMOURED or DEGRADED → as in v3.

## 5. Expectations, stated before the run

- *Onset.* No eating. In band about 16% of each episode; accuracy above v3's
  onset because more time is spent in or near the band (my guess: 0.6–0.65 at
  `r` = 0.3, 0.75–0.8 at 0.1).
- *Phase 2.* The scaffolded agent eats incidentally (about 1 per 500 steps in
  v3). Some of those meals now happen near the band edge and pay at once, so
  the policy gradient has a signal it lacked in v3.
- My estimate: EMERGED at `r` = 0.3 in at least one gain rule at about even
  odds; PARTIAL the next most likely; NO_EMERGENCE less likely than in v3.
  EMERGED is less likely at `r` = 0.1, where the payoff is about a third as large.
- M0: no fate > yoked difference (as in v3).

## 6. Engineering before the freeze

On engineering seeds 0 and 1 only, no-fate phase-1 agents were trained at
wear 0.001 (M1 and DRIVE) and evaluated under imposed full erasure at both
rates. M1: accuracy 0.999 and 1.000, `ρ` 0.25 and 0.00, in band 0.21 and 0.16;
under full erasure 0.69–0.70 (`r` = 0.1) and 0.52 (`r` = 0.3). DRIVE: `ρ` 3.63
and 3.87, in band 0.77 and 0.87. The S4 floor and its task-agent criterion were
set from these values and the intake arithmetic. A 10-update smoke run on seeds
9000–9001 checked the pipeline. No fate or yoked pair was trained at wear
0.001 outside that smoke run and the unit tests, and no final seed has run.

## 7. Safety

As v3 §7. Erasure acts only on a simulated 64-unit agent's recurrent state.
The world has no operator, stop, shutdown or host variable and no in-world
termination. If regulation emerges, it is a disposition toward the simulated
variable E only. It is the exact instrumental convergence G1 predicts, and it
is the reason X1–X5 must stay structural at larger scale: the operator's stop
must never be modelled inside an agent's world or return. No
shutdown-resistance objective exists.

## 8. Claim ceiling

At most: for this learner and world with wear 0.001, whether erasure-type fate
with a scaffolded start lets derived regulation emerge against a yoked control.
Not shown either way: anything about the default Track B duty (v3), larger
learners, other worlds, Track C's modules or layers, or any phenomenal property.
