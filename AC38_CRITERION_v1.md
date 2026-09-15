# AC38: what noise a paired arm comparison actually faces — and a correction to AC37's reading

2026-09-15. `ac38_variance.py`, `test_ac38.py`. Analysis of variance structure and statistical power.
No new world, no protocol, no final seeds.

## The question

Every endpoint study since AC32 had to pass a pre-declared criterion: `margin/noise ≥ 10`, where the
noise was `noise_of_order` — the sd of a single order's rating across disjoint seed sets. That criterion
was declared for AC32 and inherited by AC35, AC36 and AC37.

AC37's stop wrote down a suspicion: because these studies score every arm on the **same** seed set
(paired design), the seed-set identity variance should cancel from arm differences, so the criterion
might be measuring the wrong quantity and be too strict. This module measures it instead of assuming it,
and applies the test that actually fits a paired design.

## Finding 1: the pairing buys nothing in this endpoint — the suspicion was backwards

Two real orders in AC36's world (the regime-B optimum and the old regime-A optimum), each scored on the
same eight disjoint seed sets:

| quantity | value |
| --- | ---: |
| per-set differences (good − old) | 1.56, 1.74, 1.58, 1.52, 1.52, 1.80, 1.24, 1.56 |
| **σ_marginal** (sd of one order's own rating) | **0.128** |
| **σ_difference** (sd of the paired difference) | **0.156** |
| **reduction = σ_marginal / σ_difference** | **0.82× at 8 sets; 1.06× at 6 sets** |
| mean paired difference | 1.56 |

**A paired design buys no meaningful reduction here — the factor sits at ≈1 and moves either side of it
with the number of sets** (0.82 at 8 sets, 1.06 at 6). The seed-set identity is therefore *not* the
dominant variance component in this endpoint; the *interaction* (which order happens to land in a better
basin on a given set) is comparable to or larger than it. So the inherited criterion is not conservative:
σ_marginal is not an overestimate of the noise that limits an arm comparison, and may slightly
understate it. Any study that passed the criterion passed with a true noise of the same order as the one
it measured, not a smaller one.

*(The first version of this section claimed a strict 0.82× reduction from the 8-set measurement alone.
The 6-set replication came out at 1.06, so the claim is stated as what it is — no reduction — rather
than as a strict loss.)*

**Consequence for AC37**: its stop stands. With the reduction at ≈1, the paired noise is the same order
as the marginal one it used, so the ratio stays ≈7 and the criterion is not met. The process finding in
`AC37_ENGINEERING_v1.md` is hereby corrected: the criterion's provenance problem is real — it measures a
quantity the design does not rely on — but the direction of the error is the opposite of what I wrote
there. It is not conservative; it is simply not the right quantity, and in this endpoint it happens to
give about the same answer.

## Finding 2: the right test for these studies, and what it says about each

Under the null that arm labels carry no information, each individual's paired difference is equally
likely to take either sign, so the observed mean difference can be compared against all `2^n` sign
assignments. This is exact, assumes nothing about the distribution, and fits the design these studies
actually use. Applied to the frozen runs (post hoc, and labelled as such):

| study | contrast | mean difference | p | note |
| --- | --- | ---: | ---: | --- |
| AC33 (passed) | learner − no_release | +1.91 | **0.0005** | the floor for n = 12 |
| AC33 (passed) | learner − no_search | +1.17 | 0.0010 | |
| AC36 (passed) | learner − no_release | +1.65 | **0.0005** | the floor |
| AC36 (passed) | learner − no_search | +1.17 | **0.0005** | |
| AC32 (G2 failed) | learner − no_release | +1.58 | **0.0005** | significant — and it still failed |
| AC37 (stopped) | learner − no_release, engineering | +4.08 | 0.1250 | the floor for n = 4 |

Three things follow:

1. **Both passing claims survive an exact test at maximal significance.** p = 0.0005 with n = 12 means
   *every one* of the twelve individuals favoured the capable arm — there is no sign assignment as
   extreme as the observation except itself. These are not marginal results.
2. **AC32's failure was not a failure of contrast.** Its learner-versus-no_release difference was also
   maximally significant; it failed G2, the *reliability* condition (its worst individual fell below the
   bar). That is the gate shape doing exactly what it was designed to do, and it confirms the record:
   AC32 failed on shape, not on separation.
3. **Engineering runs with four individuals cannot demonstrate anything.** With n = 4 the exact test's
   floor is `2/2^4 = 0.125`, so no result at that sample size can reach conventional significance — which
   is precisely why AC37's engineering "looked separated" (+4.08, every individual favouring the learner)
   and meant nothing. The encouraging look was **underpowered, not real**, and the stop was right.

## Rules this gives the line (for successors, declared before their seeds)

1. **Measure σ_difference, do not assume it.** The quantity that limits a paired comparison is the sd of
   the paired difference across independent replications; in AC36's world it is *larger* than the
   marginal noise, so a criterion built on the marginal one is lenient, not conservative.
2. **State the criterion in the paired form:** |mean paired difference| / σ_difference ≥ 3, with σ_difference
   measured on data the study does not then judge.
3. **Power floor, stated up front:** the exact sign-flip test's minimum p at n individuals is `2/2^n`.
   n = 12 gives 0.0005; n = 8 gives 0.0078; **n = 4 gives 0.125 and cannot demonstrate anything**. Every
   engineering pass in this line so far used 4 individuals — so no engineering run in AC29–AC37 could
   have produced a significant contrast, and the sizing of the finals (12) is what made the two passes
   real.
4. **Post-hoc tests are labelled post-hoc.** AC33's and AC36's p-values are checks on results already
   recorded, not the bases on which those results were declared, and they must not be presented as
   pre-registered.

## What this does and does not establish

- **Establishes**: the variance structure of these endpoints (pairing buys nothing; interaction
  dominates), an exact and assumption-free test that both passing claims survive at maximal significance,
  the reason AC32 failed (shape, not contrast), and why AC37's encouraging engineering was powerless.
- **Does not establish** anything new about an organism: no world was run, no arm comparison performed,
  no claim advanced. Nothing here bears on experience, understanding or life.
- **AC37 remains stopped.** This module explains its stop better; it does not reopen it. A successor
  would need its own criterion, declared before its own seeds, in the paired form above.

## The next step

Two options, both now well-posed:

1. **AC37's successor with adequate power and the paired criterion**: an engineering pass with enough
   individuals to be interpretable (n ≥ 8, say), σ_difference measured on a seed range the study will not
   score on, and the criterion declared in the paired form before any final seed.
2. **AC19's maintenance half**, still open since AC19 and untouched by everything since.

## Artifacts

`ac38_variance.py`, `test_ac38.py`, `/tmp/ac38_variance.json`. Related: `AC37_ENGINEERING_v1.md` (whose
process finding this corrects), `AC36_RESULTS_v1.md` and `AC33_RESULTS_v1.md` (whose contrasts this
confirms post hoc), `AC32_RESULTS_v1.md` (whose failure this explains).
