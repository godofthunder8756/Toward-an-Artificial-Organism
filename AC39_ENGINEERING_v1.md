# AC39 engineering: prerequisite NOT MET — but the contrast is real and the criterion is the wrong question

2026-09-15. `ac39_occupancy.py`, `test_ac39.py`. Engineering only. **No protocol, no final seeds, no
claim.** The pre-declared prerequisite failed, so the study does not proceed — and the way it failed
points at a flaw in the criterion I imported, which is worth more than the study would have been.

## The claim being prepared

From AC19-M's diagnosis: an organism whose register **occupancy** is maintained by repair stays active
longer than one whose occupancy is not, **with corruption absent** (`reg_rate = 0`) so the integrity
channel AC14 studied is switched off by construction. Endpoint: active ticks.

## The prerequisite, declared before measuring

1. |mean paired difference| / σ_difference ≥ 3 (AC38's paired-form rule);
2. power: n ≥ 8, since the exact sign-flip test's floor at n individuals is 2/2ⁿ (n=4 → 0.125, which can
   never be significant — the mistake every earlier engineering pass made);
3. integrity channel off by construction.

## Measured, 16 individuals (seeds 0–7 × two histories), corruption absent

| quantity | value |
| --- | ---: |
| live `two_way` active ticks | **4096** for every individual (= every tick) |
| cut `two_way_no_repair` active ticks | 1202 … 2894, **mean 2037** |
| paired differences | 2894, 2894, 2296, 2296, 2470, 2470, 2568, 2568, **0, 0**, 1681, 1681, 2269, 2269, 2293, 2293 |
| mean difference | 2059 |
| σ_difference | **841** |
| **ratio** | **2.45** → criterion ≥ 3 **NOT MET** |
| sign-flip test | observed 2059, **p = 0.0001** |
| n | 16 → power sufficient |
| integrity channel | off by construction |

**The study stops.** No protocol, no final seeds, no claim — the criterion was declared before the
measurement and it failed.

## Why this failure is different from AC35's and AC37's, and what it exposes

This contrast is **statistically overwhelming**: p = 0.0001 at n = 16, with every live individual acting
on every tick. The criterion failed on *effect size*, not on resolvability — and the reason is visible in
the differences: **two of the sixteen individuals show zero impairment.** The cut arm is not uniformly
damaged; it is bimodal. σ_difference = 841 is mostly *heterogeneity*, not noise.

That exposes a conflation in the rule AC38 handed down. "|mean Δ| / σ_Δ ≥ 3" was written as a
*resolvability* criterion, but a ratio of mean to sd is an **effect-size** measure in disguise: a
heterogeneous population with a large mean effect can fail it while being unambiguous. And the ratio is
not merely mislabelled — it is **unstable**: the same world gives **2.45 over 8 seeds and 10.17 over the
first 3**, because the bimodality puts most of the variance in *which individuals are sampled*. A gate
that swings by a factor of four on a seed subset cannot be the thing a study's validity rests on. Had I
used the sign-flip test and n as the criterion, this study would proceed; with the ratio it stops.

**Neither choice may be made now.** Picking between the two criteria after seeing this data is exactly
choosing the threshold that fits the result. The honest outcome is the stop, plus the finding:

> **AC39's contribution: the paired criterion needs to be stated in two parts — resolvability (power and
> an exact test on paired differences) and a separate, explicit effect-size requirement — because a
> single mean/sd ratio silently mixes them and can reject a contrast it was designed to protect.**

A successor must declare both parts, in advance, and must not inherit this document's ambiguity.

## What the data suggests, without being a claim

Two structural facts worth recording as observations, not results: the cut arm is *bimodal* (some
individuals unimpaired, most roughly halved), and the live arm saturates the endpoint at 4096 ticks — so
the live arm's endpoint has no headroom, which is also why a ratio built on σ_difference is a poor fit
for it. A successor measuring "occupancy maintained by repair" should probably also state an endpoint
with headroom for the *maintained* arm, or report the impaired fraction of individuals alongside the mean.

## What is not established

- Nothing about an organism: no protocol, no declared final seeds, no results directory, no claim.
- Not autopoiesis, closure, or life. The endpoint is ticks on which the organism acts; "occupancy
  maintained by repair" is machinery, and this diagnosis does not upgrade AC19 from exploratory status.
- The bimodality is unexplained. It is recorded as an observation that a successor should predict, not
  as a finding.

## Artifacts

`ac39_occupancy.py`, `test_ac39.py`, `/tmp/ac39_prerequisite.json`. Related: `AC19M_MAINTENANCE_v1.md`
(the diagnosis this would have tested), `AC38_CRITERION_v1.md` (whose paired rule this shows is
incomplete), `AC14_CLOSURE_v1.md` (the integrity finding it holds fixed by construction).
