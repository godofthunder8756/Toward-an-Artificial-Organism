# AC40: the split criterion — resolvability, effect size, stability, headroom

2026-09-15. `ac40_criterion.py`, `test_ac40.py`. Framework, not a study: **no world, no protocol, no
final seeds, no claim.**

## Why it exists

AC39 stopped on the criterion AC38 handed down — `|mean paired difference| / σ_difference ≥ 3`. It failed
at 2.45 while the exact paired test gave p = 0.0001 at n = 16, and a 3-seed subset of the same world gave
10.17. One number was silently standing in for four different questions. This module computes them
separately so a successor can declare each in advance.

| question | what answers it |
| --- | --- |
| **Resolvability** — can the design tell the arms apart? | power (n) and the exact sign-flip test on paired differences |
| **Effect size** — how big is the difference? | mean, sd, ratio, median, impaired fraction — *not* a significance measure |
| **Stability** — does the answer survive a resample? | the same statistics across halves of the individuals |
| **Headroom** — can the endpoint show the advantage at all? | the fraction of the maintained arm pinned at the ceiling |

## What it says about the four datasets

| | AC33 (passed) | AC36 (passed) | AC32 (G2 failed) | AC39 (stopped) |
| --- | ---: | ---: | ---: | ---: |
| n | 12 | 12 | 12 | 16 |
| exact p | 0.0005 | 0.0005 | 0.0005 | 0.0001 |
| **resolved** | **yes** | **yes** | **yes** | **yes** |
| mean difference | 1.9 | 1.7 | 1.6 | 2059 |
| ratio (mean/sd) | 4.91 | 6.95 | 7.67 | **2.45** |
| impaired fraction | 100% | 100% | 100% | **88%** |
| half-sample ratios | 4.12, 6.39, 5.69, 4.38 | 11.38, 5.43, 13.64, 5.25 | 17.44, 5.73, 17.49, 5.69 | 11.75, 1.67, 2.45, 2.45 |
| **headroom** | — | — | — | **100% at the ceiling — saturated** |

Three readings, and the second is against my own framework:

1. **Resolvability separates nothing problematic**: all four contrasts, including AC32's, are resolved at
   the exact test's floor. That confirms AC38's conclusion — AC32 failed on gate *shape* (its worst
   individual against a ceiling bar), not on contrast.
2. **The stability check as built does not discriminate.** Under my half-sample bar (spread ≤ 1.5) *every*
   study is flagged unstable, including both that passed and the one that failed: spreads of 1.55, 2.60,
   3.08, 7.03. The ratio of a mean to an sd is simply a noisy statistic at these sample sizes, so
   resampling it does not distinguish a bimodal world from a uniform one. **This is a defect in my
   metric, found by applying it to data whose answer I already knew** — which is the only reason I
   caught it rather than shipping it as a validation gate.
3. **Headroom is decisive and was missing entirely.** AC39's maintained arm sat at exactly 4096 ticks for
   every individual — 100% saturated — so a large part of that endpoint's variance structure was an
   artefact of a ceiling. No earlier criterion in this line looked at this, and it is the clearest single
   reason AC39's numbers were hard to interpret.

## What a successor should declare (before its seeds)

1. **Resolvability**: n and the exact test, with the floor `2/2ⁿ` stated up front. This is the part that
   works, and it is cheap.
2. **Headroom**: a stated ceiling and a maximum acceptable fraction of the maintained arm at it. Endpoints
   where the good arm saturates cannot show improvement and should be redesigned — AC39's saturated at
   100%.
3. **Effect size**: an explicit requirement, stated in units of the endpoint (e.g. "the median difference
   exceeds X"), *not* as a mean/sd ratio — the ratio is noisy (finding 2) and was never a significance
   measure.
4. **Stability**, if wanted, must be built from a statistic that is not resampled out of its own noise:
   report the impaired fraction and the per-individual differences directly, as AC40 does, rather than a
   ratio of moments.

## What this does and does not establish

- **Establishes**: a framework for the four questions; that all four recorded contrasts are resolved at
  the exact test; that AC39's endpoint was saturated; and that the mean/sd ratio is too noisy to gate on
  (demonstrated on data with known answers, including two passing studies).
- **Does not establish**: any criterion's numeric bar. The p-value bar (0.01), the power floor (n ≥ 8) and
  the stability bar (1.5) are declared quantities in this module, and finding 2 shows the third of them
  does not do its job — a successor must choose its own and justify it in advance.
- **Nothing about an organism**, no world run, no arm comparison performed, no claim advanced, and AC39
  remains stopped.
- Not autopoiesis, closure, or life.

## Artifacts

`ac40_criterion.py`, `test_ac40.py`, `/tmp/ac40_criterion.json`. Related: `AC39_ENGINEERING_v1.md` (the
stop that prompted this), `AC38_CRITERION_v1.md` (the ratio rule this splits), `AC33_RESULTS_v1.md` and
`AC36_RESULTS_v1.md` (whose contrasts this re-examines post hoc).
