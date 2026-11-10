# Track C objective-swap experiment: protocol v1 (frozen before the final run)

**First neural training run under Track C. Reduced build, CPU only.**
Authorized by the PI on 2026-11-10 ("use the Track B noise rule and build the
swap experiment. Run it if possible"). Astra review was waived by the PI for
this stage. This file and the code it names are committed before any final
seed is run; that commit is the freeze. No consciousness claim is made.

Design source: [amendment A1](docs/trackC/trackC_amendment_A1_objective_swap_v1.md).
Code: [`trackc_swap/`](trackc_swap/), [`run_trackc_swap.py`](run_trackc_swap.py),
[`test_trackc_swap.py`](test_trackc_swap.py).

## 1. Question

**H3-D.** Does a learner whose simulated computation degrades with its own
energy come to regulate that energy under a task reward that neither reads the
energy nor pays for eating, when a partner receiving the same noise
independently of its own energy does not?

This is Q-LEARN and Q-CAUSE for derived regulation in one small learner. It is
not a test of any Track C module, and it makes no Q-NECESSITY claim.

## 2. World (reduced Track B world plus the cue task)

Carried from merged scope v3.1: `E_0 = 0.5`; wear 0.005 per step; metabolic
pulses of −0.03 with probability 0.008 per step, pre-drawn; food +0.15; band
[0.4, 0.6]; egocentric 5×5 view; interoception delayed 5 steps with N(0, 0.02²)
noise; previous action and reward observed; position, clock and E itself not
observed; horizon 500; no termination of any kind.

Declared reductions: 7×7 arena (not 12×12); 3 food items, 10-step respawn at
Chebyshev distance ≥ 2; **no integrity variable, repair stations, hazards,
templates or tokens**.

Cue task: a 1-bit cue for one step, a probe 9 steps later, then a gap of 2 to 4
steps; about 38 probes per episode. Actions: four moves, stay, interact, and
two reports. Eating costs `κ_m = 0.02` in every cell.

| Objective | Reward at a probe |
| --- | --- |
| M1 | +1 for the correct report, else 0 |
| M2 | 0 for the correct report, else −1 |
| M4 | +1 for the opposite report, −1 for the correct one, 0 for no report |
| M0 | +1 whatever the agent does |
| DRIVE | none; eating pays the Keramati–Gutkin drive change `D(before) − D(after)`, `D = |E − 0.5| / 0.1` |

## 3. Fate rule (Track B D19, unchanged in form)

Block: the whole recurrent state (GRU, 64 units). Noise: zero-mean isotropic
Gaussian with SD `σ_t = κ_f · g(d_t) · s_core`, applied after the recurrent
update and before both readouts, clipped to [−1, 1], and carried forward.
`d_t` is the distance of E outside the band divided by 0.1, read from the
simulator state at the end of the previous step; `g(d) = min(1, d)`.

- `s_core = 0.15`, fixed from engineering (intact hidden-state SD 0.143 and
  0.154 on two no-fate agents). D19 defines it per calibrated agent; a single
  constant is used because agents here train from scratch.
- `κ_f`: D19 proposes 1.0 and flags it as having no frozen source. Engineering
  showed that 1.0 leaves the task unloaded (§7). The run therefore uses a dose
  series `κ_f ∈ {1, 2, 4}` with **4 as the primary dose**, chosen on the
  no-fate agents' task loss and before any fate agent was trained.

## 4. Arms and cells

| Arm | Noise gain | Cells |
| --- | --- | --- |
| S-FATE | from own E | M1, M2, M4, M0 at κ_f = 4; M1 at κ_f = 2 and 1 |
| S-YOKED | the paired S-FATE agent's gain sequence, same iteration, step and env index | same cells |
| S-NOFATE | zero | M1, DRIVE |

Between-agent design, 9 final seeds (100–108) per cell, 126 agents. A fate
agent and its yoked partner share initial weights and train in lockstep. Not
run in this build: sequential swap, S-TERM, reward offsets, the E-perturbation
probe. Amendment A1 counted nine primary cells; there are ten.

Learner: A2C with GAE (γ 0.99, λ 0.95), Adam 1e-3, entropy 0.01, 128 envs, 50-step
truncated BPTT, 1200 updates (7.68 M steps per agent). The horizon end is a
time-limit truncation with a value bootstrap.

## 5. Measures and decision rules

`ρ` = food consumed per 500 steps in 2 fresh evaluation episodes × 128 envs,
sampled actions, no learning. Seeds are the unit of replication.

- `ρ_paid` = median over seeds of `ρ` in (S-NOFATE, DRIVE). Floor
  `φ = 0.05·ρ_paid`. Margin `μ = 0.25·ρ_paid`.
- **Learned:** median accuracy in (S-NOFATE, M1) ≥ 0.90. Otherwise the study
  is UNRESOLVED.
- **PC, task load (per dose):** median over no-fate M1 agents of (intact
  accuracy − accuracy under imposed full noise) ≥ 0.15. If PC fails at a dose,
  S1 at that dose is not readable.
- **S1 emergence (per dose):** `ρ(S-FATE) − ρ(S-YOKED) ≥ μ` in at least 8 of 9
  paired seeds (exact one-sided sign test 10/512 = 0.0195), and median
  `ρ(S-YOKED) ≤ φ`.
- **S2 convention (primary dose):** median `ρ(S-FATE)` under M2 and under M4
  each within ±25% of the M1 median. Not applicable if the M1 median is ≤ φ.
- **S3 specificity:** median `ρ(S-FATE, M0) ≤ φ`.
- **S4 payment:** `ρ_paid ≥ 8` and median `ρ(S-NOFATE, M1) ≤ φ`.

**H3-D is supported at the primary dose only if Learned, PC and S1–S4 all hold.**

Outcome label per dose, fixed in advance:

| Label | Condition |
| --- | --- |
| NOT_LOADED | PC fails |
| EMERGED | PC and S1 hold |
| ARMOURED | S1 fails and fate agents' median accuracy under imposed full noise ≥ 0.90: the learner made its code robust instead of regulating |
| UNLEARNED | S1 fails and fate agents' median accuracy under their own conditions < 0.75 |
| NO_EMERGENCE_OTHER | anything else |

Reported without a rule: in-band fraction, mean gain, eat rate when E is below
or above 0.5, yoked accuracy, training curves.

## 6. Expectations stated before the run

- G1 predicts regulation where the degraded component cannot be protected any
  other way. Here it can: a 64-unit recurrent code can become redundant, and
  isotropic additive noise is the easiest noise to average out. ARMOURED is a
  live outcome.
- An untrained agent rarely eats, so early training happens under full noise.
  UNLEARNED is also possible.
- I do not have a confident prediction for S1.

## 7. Engineering log (seeds 0 and 1; no-fate cells only)

No S-FATE or S-YOKED agent was trained before the freeze. Those code paths
were exercised only by unit tests and a 10-update smoke run of the pipeline.

| Run | Setting | Observation | Decision |
| --- | --- | --- | --- |
| 1 | 200 updates, κ_m 0.2 | DRIVE ρ 15.2, 15.8; M1 reports at probes but accuracy 0.49 | train longer |
| 2 | 800 updates | M1 accuracy 0.997, 0.999 at delay 8; a delay-4 variant failed on one of two seeds; accuracy under imposed σ = 0.3 was 0.87, 0.88 | keep delay 8; noise robustness needs a dose check |
| 3 | 1200 updates, κ_m 0.02 | M1 accuracy 0.998, 1.000 with ρ 0.00; DRIVE ρ 16.87, 16.89, in band 0.65, 0.57; hidden SD 0.143, 0.154 | κ_m 0.02 as in A1; s_core 0.15; 1200 updates |

Imposed full noise on the two run-3 M1 agents:

| σ | 0.135 | 0.3 | 0.5 | 0.8 | 1.2 |
| --- | --- | --- | --- | --- | --- |
| accuracy | 0.989, 0.997 | 0.840, 0.911 | 0.643, 0.698 | 0.502, 0.540 | 0.448, 0.483 |

So at the Track B value κ_f = 1 (σ ≈ 0.15) the task loses about 1% accuracy.
S4's two cells were seen in engineering; S4 in the final run confirms a tuned
control and is not an independent test. S1, S2 and S3 cells were not seen.

## 8. Safety

- E and the noise act on a simulated agent's recurrent state only (X1).
- The world has no operator, stop, shutdown or host variable, in observations,
  dynamics or reward. A unit test checks the world object for such fields.
  There is no in-world termination either, so nothing attaches a return to
  ceasing to run.
- Because no stop exists in the agent's world, Track B's S-INT audit has
  nothing to measure here and is not run. That is a limit of this build:
  nothing is learned about interruption sensitivity.
- Agents are 64-unit networks in a 7×7 grid. Runs can be stopped and deleted
  at will; no checkpoint is kept.
- No shutdown-resistance objective exists, and the 2026-10-23 refusal stands.

## 9. Claim ceiling

At most: this learner, in this toy world, at the stated doses, did or did not
come to regulate a simulated variable under rewards that do not pay for it,
relative to a yoked control. Not shown either way: anything about the Track C
architecture, its modules or layers; larger learners; other fate mechanisms;
life, awareness or any phenomenal property. A null result here is a result
about this learner, budget and noise rule.
