# Track C swap v2: results of the 2×2 (start × gain rule)

> **[Swap erratum 1](TRACKC_SWAP_ERRATUM_1.md) (2026-11-12):** in every scaffolded pair of v2–v8 the fate and yoked
> agents shared Adam optimizer state, so their learning was coupled. Read this file with that caveat.

Protocol frozen at commit `19ddd89` ([TRACKC_SWAP_PROTOCOL_v2.md](TRACKC_SWAP_PROTOCOL_v2.md)).
Final seeds 200–208, run once: 27 no-fate agents and 108 fate/yoked pairs,
7338 s on 4 CPU cores. Outputs: [trackc_swap_v2/REPORT.md](trackc_swap_v2/REPORT.md),
[scores.json](trackc_swap_v2/scores.json), [raw.json](trackc_swap_v2/raw.json),
and the M1/M0 phase-1 weights in `trackc_swap_v2/phase1_weights/`. The SHA-256
of every source file, recorded in `raw.json`, matches the freeze commit.
Not reviewed by Astra (waived by the PI for this stage). No consciousness claim.

## 1. Outcome

**H3-D is supported in no condition. Derived regulation did not emerge in any
cell of the 2×2.** By the factorial reading fixed in advance (protocol §4),
this is "emergence in none → neither factor suffices for this learner".

| Rule | Result |
| --- | --- |
| Learned | holds: no-fate M1 median accuracy 1.000 |
| S4 payment | holds: paid regulator `ρ_paid` 16.87; no-fate task agent `ρ` 0.00 |
| Task load, κ_f = 4 | holds: imposed full noise costs 0.422 accuracy |
| Task load, κ_f = 2 | **fails narrowly**: 0.148 against the 0.15 threshold (v1, on other seeds: 0.160) |
| S1 emergence | fails in all 8 M1 cells: 0 of 9 seeds over the margin (4.22) in every cell |
| S3 specificity (κ_f = 4) | holds in all 4 cells (it does not fail; see §4 for a pattern it does not test) |

`ρ` is food eaten per 500 steps; staying in the band takes about 17.

## 2. The 2×2 at κ_f = 4 (the loaded dose), objective M1, medians over 9 seeds

| | NAIVE | SCAFFOLD |
| --- | --- | --- |
| **SAT** | UNLEARNED: acc 0.502, `ρ` 0.00 / 0.00 | ARMOURED: acc 0.965 (0.964 under full noise), `ρ` 0.18 / 0.20 |
| **GRADED** | UNLEARNED: acc 0.501, `ρ` 0.00 / 0.00 | ARMOURED: acc 0.980 (0.975 under full noise), `ρ` 0.21 / 0.16 |

`ρ` is fate / yoked. In every cell the fraction of time in band is 0.04 for
both arms. That is the first 20 or so steps of each episode, before wear takes
E out of the band from its start at 0.5; no agent re-entered the band. Mean
gain was 0.90 (GRADED) and 0.94 (SAT), i.e. near-permanent full noise. Paired
fate − yoked differences in `ρ` were within ±0.16 for every seed of every M1
cell.

At κ_f = 2 all four cells are NOT_LOADED by the rule. The scaffolded agents
there end at 0.995–0.997 accuracy, and naive agents split between seeds that
learn under noise (0.8 to 0.98) and seeds at chance, as in v1.

## 3. What happened

**The scaffold removed the mutual-dependence trap, and the agent learned to
absorb the noise instead of avoiding it.**

- *Onset.* The phase-1 agent, competent with no fate (accuracy 1.000), was
  evaluated with fate on before any phase-2 update. At κ_f = 4 its accuracy
  fell to 0.61 (SAT) and 0.63 (GRADED). It ate 0.02–0.03 per 500 steps, as
  expected of a no-fate agent, so E ran out and the noise reached full strength.
- *Phase 2.* Median training accuracy of the fate agents rose from 0.60 at the
  first evaluation point to 0.89 after a quarter of phase 2 and 0.96–0.98 at the
  end. Their yoked partners, which received the same noise magnitudes with no
  dependence on their own body, followed the same curve to within 0.01 at every
  point shown below, and their final eating was the same. In band stayed at
  0.04 throughout.

| phase-2 point (of 120) | 0 | 8 | 30 | 60 | 119 |
| --- | --- | --- | --- | --- | --- |
| SAT: fate / yoked accuracy | 0.600 / 0.604 | 0.703 / 0.709 | 0.888 / 0.885 | 0.954 / 0.952 | 0.958 / 0.965 |
| GRADED: fate / yoked accuracy | 0.622 / 0.620 | 0.738 / 0.730 | 0.889 / 0.893 | 0.958 / 0.964 | 0.980 / 0.978 |

The naive cells repeat v1 at κ_f = 4: no fate or yoked agent learned the task,
even with the noise switched off (0.50), so nothing rewarded eating.

**The graded gain made no difference.** In each start condition the GRADED and
SAT cells got the same label, and the medians differ by at most 0.03 in
accuracy and 0.03 in `ρ`. A meal lowers graded noise by 0.3 of its maximum, but
no agent ate often enough to turn that into a lasting reduction.

## 4. Pattern under M0 (reported, not scored)

Under the null objective M0 (reward +1 per probe whatever the action, minus
`κ_m` per meal) there is no reason to eat, yet fate agents ate more than their
yoked partners in 9/9 seeds (GRADED/NAIVE), 8/9 (GRADED/SCAFFOLD), 7/9
(SAT/NAIVE) and 5/9 (SAT/SCAFFOLD). Median differences were 1.22, 0.35, 0.54
and 0.01, all below the margin 4.22 (at most 7% of the paid level). Under M1
no such sign pattern appeared (between 3/9 and 6/9 positive).

This was not a pre-stated test, and 9/9 is exploratory (exact two-sided sign
test p = 0.004 if taken alone). The mechanism is not identified. Because M0
rewards nothing that eating buys, the difference must come from how
body-coupled noise shapes behaviour, not from regulation that pays. Its
practical consequence is that a fate-versus-yoked difference in eating is not
by itself evidence of derived regulation. That justifies keeping the paired
S3 contrast in later protocols.

## 5. Expectations against outcomes

| Stated before the run (protocol §5) | Outcome |
| --- | --- |
| SAT/NAIVE: no emergence, as in v1 | **confirmed** (UNLEARNED) |
| SCAFFOLD starts phase 2 not eating | **confirmed** (onset `ρ` 0.02–0.03) |
| SCAFFOLD: DEGRADED at least as likely as EMERGED | **wrong in kind**: neither; ARMOURED in both gain rules |
| If anything emerges, SCAFFOLD × GRADED | nothing emerged |
| GRADED/NAIVE may become ARMOURED | **not seen** (UNLEARNED) |

I did not anticipate that a learner which could not acquire the task under
κ_f = 4 noise from scratch would recover it under the same noise once it
already had it.

## 6. Reading

1. **Neither A nor B is the obstacle, as these runs tested them.** Once the
   task was learned before fate, the mutual-dependence trap (v1 reading 2) was
   gone. A gain with no flat region (v1 reading 3) changed nothing. Both
   explanations are weakened as the main cause.
2. **v1 reading 4 is now the leading explanation.** Isotropic additive noise on
   a 64-unit recurrent state can be absorbed by a code learned for the task. A
   competent agent took that route in every scaffolded seed and reached 0.96–0.98
   at mean gain above 0.9. If noise can be engineered around, the body does not
   Blackwell-order the system's channels in the sense of G1, and fate gives no
   reason to regulate. In G1 the register had no such route: erasure cannot be
   coded around.
3. **Robustness depends on the training path.** The same κ_f = 4 noise that
   blocks acquisition from scratch is absorbed by a learner that starts
   competent (phase 2 lifted accuracy from 0.61 to 0.97). This is a Q-LEARN
   fact about this learner. It also means the scaffold changes which solution
   gets found, not only how fast.
4. **Why robustness beats regulation for a gradient learner here** (a
   hypothesis, not tested). Making the code robust lowers the cost of noise at
   every step, and the ordinary task gradient finds it. Regulation needs a
   detour to food, pays `κ_m` per meal, shows its effect only after the
   interoceptive delay, and has to be repeated about every 30 steps to hold the
   band against wear. The paid regulator learns that schedule because each meal
   is rewarded at once; under fate the return arrives only through accuracy on
   later probes.

## 7. Limits

- One learner (A2C, 64-unit GRU), one world, one noise form, E only.
  Scaffolded agents trained twice as long in total as naive ones.
- κ_f = 2 missed the task-load threshold by 0.002, so its four cells are
  NOT_LOADED by rule. Effectively only κ_f = 4 tested the 2×2.
- Doses above 4 were not run. A dose high enough to defeat a robust code might
  change the result, or might only produce DEGRADED.
- No probe measured *how* the code became robust (for example larger
  separation of task states or use of the clipping bounds). The `hidden_sd`
  recorded in `raw.json` includes the injected noise and cannot separate the two.
- The M0 pattern (§4) is exploratory and unexplained.
- Nothing here bears on Track C's workspace, ignition or metacognitive head.

## 8. Run disclosure

The final command was launched twice. The first launch, under a shell with a
2-hour limit, finished phase 1 (836 s). It was stopped when its timing showed
that the pairs would exceed the limit. At that point it had written only
`phase1_weights/` and progress lines. No pair had run and no score existed. I
deleted its output directory and kept its log out of the repository. I then
relaunched the identical frozen command (same code, seeds and output path) as
a detached process, and it ran to completion once. Phase 1 is deterministic
given the seed, so the relaunch repeated it.

## 9. Options for a follow-up (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| C. A fate mechanism a code cannot absorb: with probability rising in `g`, reset the recurrent state (erasure, as G1's register), in place of additive noise | reading 2 directly. G1's theorem C applies to erasure | about 2 hours with a scaffold; departs from the Track B rule |
| C′. A diagnostic first: freeze the scaffold agent's task weights in phase 2 and train only the action head | whether regulation emerges when robustness cannot be learned. It says nothing about a free learner | about 1 hour |
| D. Selection across a population | whether selection finds regulation where gradient learning finds robustness | larger |

Recommended: C, with a SCAFFOLD start only, since v2 showed the naive start
fails for a separate reason. C′ is a cheap check on reading 4 if the PI wants
one first.

## 10. Safety

Same as the protocol §7. The noise and E are simulated and act only on a
64-unit agent's recurrent state. The world has no operator, stop, shutdown or
host variable. No shutdown-resistance objective exists. Option C would keep
these lines. Erasure-type fate is the condition under which G1 showed exact
instrumental convergence toward protecting the substrate, so any agent where it
*does* produce regulation should be treated as having that disposition toward
whatever it models as its substrate. X1–X5 remain structural.

## 11. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_swap2.py --mode final --out <new dir>   # about 2 hours on 4 cores
python run_trackc_swap2.py --score trackc_swap_v2   # rescore the committed run
```
