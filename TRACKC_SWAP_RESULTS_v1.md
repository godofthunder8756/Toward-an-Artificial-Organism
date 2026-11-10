# Track C objective-swap experiment: results v1

Protocol frozen at commit `4583a25` ([TRACKC_SWAP_PROTOCOL_v1.md](TRACKC_SWAP_PROTOCOL_v1.md)).
Final seeds 100–108, run once, 126 agents, 55 minutes on 4 CPU cores.
Outputs: [trackc_swap_v1/REPORT.md](trackc_swap_v1/REPORT.md),
[scores.json](trackc_swap_v1/scores.json), [raw.json](trackc_swap_v1/raw.json).
Not reviewed by Astra. No consciousness claim.

## 1. Outcome

**H3-D is not supported. Derived regulation did not emerge at any dose.**
Primary-dose label, as fixed in advance: **UNLEARNED**.

| Rule | Result at the primary dose (κ_f = 4) |
| --- | --- |
| Learned (no-fate agents) | holds: median accuracy 0.999 |
| PC task load | holds: imposed full noise costs 0.42 accuracy |
| S1 emergence | **fails**: 0 of 9 seeds over the margin; fate ρ 0.00, yoked ρ 0.00 |
| S2 convention | not applicable (no regulation under M1) |
| S3 specificity | **fails**: fate ρ 1.31 under M0, above the floor 0.83; yoked 1.42 |
| S4 payment | holds: paid regulator ρ 16.67; no-fate task agent ρ 0.05 |

`ρ` is food consumed per 500 steps. Staying in the band needs about 17.

## 2. By dose (objective M1, medians over 9 seeds)

| κ_f | accuracy lost by no-fate agents under imposed full noise | fate ρ | yoked ρ | fate accuracy | fate accuracy with noise switched off | fraction of time in band | label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 (Track B value) | 0.015 | 0.14 | 0.04 | 0.993 | 1.00 | 0.04 | NOT_LOADED |
| 2 | 0.160 | 0.00 | 0.00 | 0.507 | 0.50 | 0.04 | UNLEARNED |
| 4 (primary) | 0.420 | 0.00 | 0.00 | 0.499 | 0.50 | 0.04 | UNLEARNED |

In every fate cell the agents let energy run to zero and spent the rest of the
episode at full noise (mean gain 0.94).

## 3. What happened

**κ_f = 1.** All nine fate agents learned the task to 0.97–0.99 *under
permanent full noise*. The noise costs nothing they could not absorb, so
there was nothing for regulation to buy. Fate agents ate slightly more than
their partners in 6 of 9 seeds (differences of 0.1 to 0.2 per 500 steps, one
seed at −0.23). That is a twentieth of the margin and is not evidence of
regulation.

**κ_f = 2.** Three of nine fate agents learned the task under full noise
(accuracy 0.85 to 0.94; 0.95 to 0.97 with noise switched off). They did it by
tolerating the noise: all three ate nothing. Two of nine yoked partners also
learned. The other agents stayed at chance.

**κ_f = 4.** No fate or yoked agent learned the task, even when tested with
noise off. With no task competence there is no difference in value between
being in the band and out of it, so nothing rewards eating.

**S3.** Under M0, and under M4 where agents stayed at chance, behaviour was
close to random and incidental eating was 1.3 to 2.0 per 500 steps in fate and
yoked arms alike. The S3 failure is that random baseline. It is not regulation
that failed to switch off.

**Controls.** The paid regulator learned in all nine seeds (ρ 16.5 to 16.9, in
band 0.29 to 0.67). The no-fate task agent learned the task and stopped eating.

## 4. Reading

1. **This is a negative Q-LEARN result for this learner, budget and noise
   rule.** It does not contradict G1, which is about optimal policies. It
   shows that acquisition is not automatic: G1 established that the behaviour
   exists and pays, not that a learner finds it.
2. **Regulation and competence each need the other first.** The task cannot be
   learned under strong noise, and regulation has no value until the task is
   learned. A learner that starts depleted is stuck on the wrong side of both.
3. **The Track B gain rule has a flat region that hides the first steps.**
   `g(d) = min(1, d)` with a half-band of 0.1 is saturated for every E below
   0.3 (and above 0.7). From E = 0, one bolus (+0.15) changes nothing; it
   takes three in quick succession before noise starts to fall. So single acts
   of eating are never rewarded, only penalized by `κ_m`. This follows from the
   rule; that it is the main cause here is a hypothesis.
4. **Where the learner could solve the task under noise, it did that instead.**
   Isotropic additive noise on a 64-unit state can be absorbed by a robust
   code. G1's register had no such option. A fate mechanism that can be
   out-engineered by redundancy does not order the system's channels in the
   way G1's definition requires.
5. **The paid route is easy and the derived route is hard.** Drive reduction
   rewards every bolus. Derived regulation offers a delayed, diffuse return
   through a second learned skill.

## 5. Limits

- One learner (A2C, 64-unit GRU, 7.7 M steps), one reduced world, E only.
- `s_core` was fixed from two engineering agents, and the primary dose was
  chosen on no-fate agents' robustness. Agents trained under noise turned out
  far more robust at κ_f = 1 and far less able to learn at κ_f = 4.
- No dose between "absorbed" and "unlearnable" produced regulation. A dose
  between 1 and 2 was not run.
- The UNLEARNED label uses the median. At κ_f = 2 the picture is mixed (§3).
- The sequential swap, S-TERM, offsets and the E-perturbation probe were not run.
- Nothing here bears on Track C's workspace, ignition or metacognitive head.

## 6. Options for a follow-up (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| A. Scaffolded start: train the task with the body protected, then switch fate on | whether a competent, in-band agent *keeps itself* there. This is A1's sequential design and removes the mutual-dependence trap | about 1 hour |
| B. Graded gain: noise proportional to distance from the setpoint over the whole range | whether the flat region is the cause (reading 3) | about 1 hour; departs from the Track B rule |
| C. A fate mechanism that redundancy cannot absorb (for example erasure of the state, as in G1) | whether reading 4 is the cause | about 1 hour; departs from the Track B rule |
| D. Selection across a population, as Track C already plans | whether regulation is found by selection where within-life learning fails | larger |

Recommended: A and B together as a 2×2. They separate the two leading
explanations, and A needs no change to the noise rule.

## 7. Corrections to earlier files

- Amendment A1 §8 item 5 says nine primary cells. There are ten.
- The protocol's choice of κ_f = 4 as primary rested on no-fate agents. The
  result shows that criterion does not predict learnability under noise.
