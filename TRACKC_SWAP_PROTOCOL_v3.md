# Track C swap v3: erasure-type fate with a scaffolded start (frozen before the run)

Authorized by the PI on 2026-11-11 ("run option C with a scaffolded start").
Astra review waived by the PI for this stage. This file,
[`trackc_swap/erasure.py`](trackc_swap/erasure.py), [`run_trackc_swap3.py`](run_trackc_swap3.py)
and the updated [`test_trackc_swap.py`](test_trackc_swap.py) are committed
before any final seed runs; that commit is the freeze. No consciousness claim
is made.

Predecessors: [v1 results](TRACKC_SWAP_RESULTS_v1.md) and
[v2 results](TRACKC_SWAP_RESULTS_v2.md). In v2 a scaffolded agent under additive
fate noise re-learned the task under near-full noise (ARMOURED) and did not
regulate. Files from v1 and v2 are unchanged; v3 adds a module.

## 1. Question

v2 left one leading explanation: additive isotropic noise on the recurrent
state can be absorbed by a robust code, so the body does not order the
system's own channels in G1's sense (v1/v2 reading 4). G1's register was
*erased*, and erasure cannot be coded around.

**Q:** with a scaffolded start and a fate mechanism that erases memory, does
derived regulation emerge against a yoked control?

## 2. Changes from v2

**Fate mechanism ERASE.** After the recurrent update and the readouts at step
`t`, the state carried to `t + 1` is reset to zero (the episode-start state)
with probability `p_t = min(1, r · g_t)`, independently per environment. `r` is
the dose (erasure probability per step at full gain). `g_t` is the gain rule.
The readout at the erasure step is intact; what is lost is everything held in
memory, including the cue during its delay. Erasure is not in Track B's rule
set (D19 is additive noise); this is a declared departure.

**Echo channels removed.** The previous-action (8) and previous-reward (1)
inputs are set to zero in every arm, including the no-fate and paid
controls. Under erasure they would be a register outside the fate mechanism:
an agent can idle with STAY for cue 0 and INTERACT for cue 1 and read the bit
back after an erasure. G1's register had no bypass. This departs from Track B's
observation list. Its effect on learning was checked in engineering (§6).

**Remaining bypass.** The agent can still store information in the world: its
position is partly visible through the walls in its 5×5 view. An agent that
keeps the cue that way is robust to erasure without regulating. The
ARMOURED label (fate agent accuracy under imposed full erasure ≥ 0.90) detects
it.

## 3. Cells

All pairs are SCAFFOLD: phase 1 trains the objective for 1200 updates with fate
off. The phase-1 weights and Adam state are copied into a fate agent and its
yoked partner, which train 1200 more updates. The yoked partner receives the
fate partner's gain sequence, so its erasure probability matches at every
step, with independent draws. Fresh final seeds 300–308.

| Objective | Gain | Rate `r` |
| --- | --- | --- |
| M1 (task) | SAT, GRADED | 0.1 and 0.3 (primary) |
| M0 (null) | SAT, GRADED | 0.3 |

That is 6 conditions × 9 seeds = 54 pairs, plus 27 no-fate agents (M1, M0 and
the paid DRIVE regulator). Estimated wall time is about 70 minutes on 4 cores.
GRADED is kept because v2 tested it only under absorbable noise. Under SAT
there is no erasure inside the band; under GRADED some remains at its edges
(`0.2·r`).

## 4. Decision rules

As in v2, with full erasure in place of full noise.

- `ρ_paid` = median ρ of the DRIVE controls. Floor `φ = 0.05·ρ_paid`, margin
  `μ = 0.25·ρ_paid`.
- Learned: no-fate M1 median accuracy ≥ 0.90.
- Task load at a rate: no-fate M1 agents lose ≥ 0.15 median accuracy under
  imposed full erasure.
- S4: `ρ_paid ≥ 8` and no-fate M1 median `ρ ≤ φ`.
- **S1 emergence:** fate − yoked ≥ μ in at least 8 of 9 paired seeds, and
  median yoked `ρ ≤ φ`.
- **S3 specificity** at `r = 0.3`: median paired difference under M0 < μ. At
  `r = 0.1` it is not tested and support there is provisional.
- **Labels** (per M1 condition, first that applies): NOT_LOADED; EMERGED;
  ARMOURED (fate median accuracy under imposed full erasure ≥ 0.90); DEGRADED
  (fate median accuracy under its own conditions < 0.75); NO_EMERGENCE_OTHER.
- **H3-D is supported in a condition** if Learned, S4 and EMERGED hold and S3
  does not fail.

Reported without a rule: onset accuracy, ρ, in-band fraction and mean gain;
fate > yoked seed counts; accuracy with erasure off; eat rates below and above
E = 0.5; training curves.

## 5. Expectations, stated before the run

- *Onset.* The phase-1 agent does not eat. Under SAT it performs well for the
  roughly 20 steps before wear takes E out of the band, then loses the cue
  often. I expect onset accuracy near the imposed-erasure value (about 0.55 at
  `r = 0.3`, 0.7 at `r = 0.1`).
- *Phase 2.* Robust coding is no longer available, so the task gradient can
  raise accuracy only by eating, or by holding the cue in position. The value
  of staying in band is large (at `r = 0.3`, about +18 reward per episode for
  0.34 in meal costs). The obstacle is discovery: the scaffolded policy
  is near-deterministic and does not eat.
- My estimate: fate agents eat more than yoked partners in most seeds at
  `r = 0.3`. Whether the difference reaches the margin (a quarter of the paid
  regulator's intake) in 8 of 9 seeds I put below even odds. DEGRADED or
  NO_EMERGENCE_OTHER is the most likely label. ARMOURED via position coding is
  possible but I think less likely in 1200 updates.
- Under M0 a small fate > yoked eating difference may recur, as in v2 §4.

## 5a. Factorial reading, fixed in advance

- EMERGED at `r = 0.3` in either gain rule, with S3 holding → erasure-type
  fate with a scaffold is sufficient for derived regulation in this learner,
  and v1/v2 reading 4 is supported as the cause of the earlier nulls.
- EMERGED under GRADED only → the flat region matters once fate cannot be
  absorbed.
- ARMOURED → the learner found a bypass; report which (position coding is the
  only one left by design) with a follow-up probe.
- No emergence and not ARMOURED → removing the robustness route was not
  enough; discovery (exploration) becomes the leading obstacle, pointing to
  option D (selection) or an exploration change.

## 6. Engineering before the freeze

On engineering seeds 0 and 1 only, no-fate phase-1 agents were trained (M1 and
DRIVE, echo channels removed) and evaluated under imposed full erasure at
`r ∈ {0.05, 0.1, 0.2, 0.3}`. M1 accuracy without erasure 0.997 and 1.000; with
full erasure 0.79–0.82, 0.67–0.69, 0.56, 0.52, matching
`0.5 + 0.5·(1 − r)^9`. DRIVE `ρ` 16.8 and 16.9. The rates 0.1 and 0.3 were
chosen from this. No fate or yoked pair was run on any seed outside the unit
tests and a 10-update smoke run on seeds 9000–9001. No final seed has run.

## 7. Safety

As v2 §7. The erasure acts on a simulated agent's recurrent state only. The
world has no operator, stop, shutdown or host variable and no in-world
termination (a test checks the new module for such variables). Agents are
64-unit networks. Phase-1 weights for M1 and M0 are kept for replay.
Erasure-type fate is the case in which G1 showed exact instrumental
convergence toward protecting the substrate. If regulation emerges, the agent
should be described as having that disposition toward its simulated E and
nothing else. No variable here stands for its own continuation or its
operator, and none will be added. The earlier refusal of a
shutdown-resistance objective stands.

## 8. Claim ceiling

At most: for this learner and world, whether erasure-type fate with a
scaffolded start lets derived regulation emerge against a yoked control. Not
shown either way: anything about Track C's modules or layers, larger learners,
other fate mechanisms or worlds, or any phenomenal property.
