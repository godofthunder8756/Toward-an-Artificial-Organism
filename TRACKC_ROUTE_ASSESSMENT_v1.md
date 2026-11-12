# Track C swap: route assessment after v8 and option P (2026-11-12)

> **[Swap erratum 1](TRACKC_SWAP_ERRATUM_1.md) (2026-11-12):** in every scaffolded pair of v2–v8 the fate and yoked
> agents shared Adam optimizer state, so their learning was coupled. Read this file with that caveat.

Requested by the PI before option Q: "verify that we are on a promising route
to breakthrough". This is a judgment, not a result. It weighs the swap line
(v1–v8, K, P) against the program's own claims and against prior work. No
consciousness claim.

## 1. Verdict

**The route is sound, and it has produced one real result. It is not yet on
the part of the path where a breakthrough would be decided.**

- The line has established its first link firmly: dependence produces
  regulation.
- The thesis's central claim sits two links further on, and nothing run so
  far tests it.
- Options Q and L refine the first link. They are worth their cost, but they
  cannot move the verdict. The experiments that can are in §4.

## 2. What is established

| Claim | Evidence | Strength |
| --- | --- | --- |
| A learner paid only for a task comes to regulate a body variable its memory depends on | v6 (7/18), v7 (8/9), v8 (9/9 and 9/9); frozen criteria; 0 of 108 yoked and M0 controls | strong, for this learner and world |
| It needs the dependence to be non-bypassable | v6 bypass (11/18), K diagnosis, v5 → v7 in the same cells (6, 0, 0 → 8, 7, 6 of 9) | strong |
| It needs the incentive to be large enough | GRADED 0.1: 3 of 18 | moderate |
| The regulation reads interoception and partly anticipates | option P: P2 41/42; the scramble abolishes eat timing in 42/42 (descriptive) | moderate; P3's frozen verdict is UNDETERMINED |

This matches what G1 derived analytically (Theorem C, fate-sharing), and G1
was frozen before any of these runs. An analytic prediction, a replicated
learner result and a mechanism probe now agree. That is the program's best
evidence chain to date.

## 3. Why it is not yet a breakthrough

1. **The central result is expected.**
   - If being out of band erases the memory a reward needs, a policy-gradient
     learner that finds this will learn to stay in band.
   - It is instrumental sub-goal learning, and theory predicts it
     (instrumental convergence; G1's own theorem).
   - Showing it took eight runs because the learner kept finding other
     routes. The outcome itself was not in doubt.
   - The less expected findings are the bypass competition and the
     anticipation.
2. **The chain still ends in an evaluator.** The agents regulate because an
   external task reward makes memory valuable. The result is "no evaluator
   rewards regulation". It is not "no evaluator". The thesis says Layer 2
   content in current AI is grounded by evaluators. Our regulators' regulation
   is also grounded by one, at one remove.
3. **The thesis's actual claim is untested.**
   - The claim is that grounding in the system's own dependence makes a
     difference to what sits above it (Layer 2).
   - No run compares a derived regulator with a paid regulator on anything
     downstream.
   - Until one does, the swap line shows only *that* regulation can be
     derived. It does not show that deriving it matters.
4. **G1's largest predicted effect has not been touched.** G1 found that
   fate-sharing matters most for self-evaluation: knowing one's own
   reliability was worth a median 13% of value, against 0.3% for control of
   the body. Every run so far tests the 0.3% effect.
5. **One small learner, one small world.** The result covers a 64-unit GRU
   on a 7×7 grid with one body variable. It has not been repeated on any
   other learner, world or variable.
6. **The non-bypassability condition cuts against easy application.** The
   world needed three changes (no echo, low wear, relocation) before the
   dependence could not be routed around. Organisms get this condition from
   metabolism. A designed system gets it only by construction, and capable
   learners find bypasses. That is a real limit on the thesis as an
   engineering claim. It is also a finding in its own right.

**Prior work** (web search, 2026-11-12, not exhaustive):
- Homeostatic reinforcement learning defines the reward as drive reduction, so
  regulation is paid for by design
  ([Keramati and Gutkin 2011](https://proceedings.neurips.cc/paper/2011/file/9778d5d219c5080b9a6a17bef029331c-Paper.pdf),
  [2014](https://elifesciences.org/articles/04811);
  [Yoshida, Sprekeler and Gutkin 2025](https://arxiv.org/abs/2507.04998)).
- Related proposals argue from precariousness or mortality
  ([Ovalle and Lucas 2020](https://arxiv.org/pdf/2007.09297);
  [mortal agents, 2024](https://arxiv.org/html/2411.12304v1)).
- I found no experiment in which regulation is derived from the dependence of
  the agent's own memory on the variable, with yoked controls.

So the design appears to be new. The underlying principle is not.

## 4. What would decide it

In order of value to the thesis:

| Step | Question | Why it is decisive |
| --- | --- | --- |
| **R. Derived against paid** | Train a paid regulator (task reward plus a homeostatic reward, no fate) to the same in-band level. Does the derived regulator differ downstream? Candidates: anticipation and the E code (option P's measures); behaviour when the reward is withdrawn or the world shifts (bolus size, wear). | This is the thesis's claim in one experiment. If the two are indistinguishable, grounding by dependence adds nothing measurable here. |
| **S. Self-evaluation** | Does a fate agent come to know its own reliability from its body history (G1's 13% effect)? For example, a confidence or opt-out action at the probe. | G1's largest prediction, and the direct link to Track C's metacognitive head. |
| **G. Generality** | A larger learner, a second body variable. | Without it, nothing above generalizes. |
| **T. Remove the last evaluator** | Replace the task reward with selection on persistence, computed outside the agent's world (option D, with the safety constraints already fixed). | Tests grounding with no evaluator's reward in the loop. It is the hardest step, and the most safety-sensitive. |

Q and L are refinements. Q is cheap, and it closes option P's open points, so
it is run now as requested.

## 5. Recommendation

After Q, run **R**. Each outcome of R is useful:
- If derived and paid regulators differ downstream, the thesis has its first
  direct support.
- If they do not, the program learns that before investing in scale.
