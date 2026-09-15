# AC34 engineering: binary survival is the wrong endpoint in this world — use graded retention

2026-09-15. `ac34_survival.py`, engineering only. **No protocol, no final seeds, no claim.** This
records a design finding and two of my own errors, and it changes what the survival study should be.

## Why this was attempted

Random-fallback survival is the one untouched open endpoint. AC30's world cannot support it: it
declares a metabolic income (1 material + 1 energy per tick) precisely so the budget never binds and
the score measures *ordering*. A survival endpoint needs the organism's own state to fund its
maintenance, so `ac34_survival.py` removes the declared income and gives the world the feedback loop
the frozen line actually had — **living sites produce energy**, which funds renewals.

## Two errors of mine, both caught by the numbers

1. **Idling was counted as starving.** The first version incremented the starvation counter whenever
   the organism took no action, but no action is taken when nothing is urgent — so deaths clustered at
   exactly the threshold (median death 25 ticks = the threshold). Fixed: starvation is *wanting* to act
   and being unable to afford it.
2. **The first economy was far too loose.** With cheap renewals every order survived on some seeds and
   died on others (mixed in 720/720), which looks like discrimination but is seed noise. Fixed by
   making renewals dear (20 energy) and funding them only from production.

## The finding: the binary endpoint is UNSTABLE, so it is not a usable endpoint

A 12-configuration scan (renewal cost 5/10/20/40 × production period 4/8/16, 120 orders each):

| survive fraction | configurations |
| --- | --- |
| **1.00** (every order survives) | 4, 8, 16 with renewal 5; 4 with renewal 10 |
| **0.00** (every order dies) | the other 7 |
| **intermediate** | none *on this grid* |

**Correction to my first reading of this table, which claimed the endpoint was "cleanly bistable":**
it is not. A finer look found an intermediate value — renewal 5 / period 16 gives **0.40** over 12
sampled orders at 400 ticks — and the *same* configuration gives **0.00** at 800 ticks. So intermediate
outcomes exist, and they flip with the run horizon and with which orders were sampled. The coarse grid
found only extremes, which is why a coarse grid is not evidence of bistability.

The cause is the same either way: production is proportional to the living population, so affording
renewals sustains itself and failing to do so collapses to zero sites and zero income. The outcome is
decided by the economy near a threshold, not by the order — and the measured spread between best and
worst order (5.00 sites of 24, 21%) is far too small to move that threshold by more than a razor-thin
window whose width depends on the horizon.

An endpoint that flips with the run horizon and the sampled orders is not a sound thing to build a
claim on. This is the AC11/AC13 lesson in a new place. A binary alive/dead criterion also discards the
graded information the order actually controls.

**And the graded version survives here:** at renewal 5 / period 4, sampled orders end with **17, 18 or
19 sites of 24** — graded, discriminating, and no longer all-or-nothing. That is the endpoint the
survival study should declare.

## What the survival study should be instead

**Graded maintenance without a declared income.** The world keeps production-funded maintenance, and
the endpoint becomes **population retained at the end of the run** — the AC30 score, but paid for out
of the organism's own production rather than a declared trickle. That is a *maintenance* measure, not
merely an ordering measure: the order decides which sites are saved, production decides how many
renewals are affordable, and the two feed back.

Prerequisite for that study, to be measured before its protocol: the spread in retained population
across orders must exceed the measurement noise (the same validity criterion AC32 declared, margin/noise
≥ 10), and the endpoint must be graded rather than bistable — the failure mode this module has just
measured and recorded.

## Not done, plainly

- No protocol, no final seeds, no frozen directory, no claims.
- The death criterion used here is **provisional engineering**, declared in the module for the
  measurement and not offered as a result.
- Nothing about experience, understanding or life; nothing about autopoiesis. The phrase "maintenance"
  here means sites retained under a cost, nothing more.
- `ac34_survival.py` is engineering and will be **superseded** by the study it informs, not frozen as a
  result.

## Artifacts

`ac34_survival.py`, `test_ac34.py`, `/tmp/ac34_survival_engineering.json`. Related:
`AC30_ACQUIRE_v1.md` (the world and the declared income), `AC33_RESULTS_v1.md` (the endpoint this
complements), `AC11_DESIGN_CONTROLS_v2.md` and `AC13_REPLICATION_v1.md` (the same lesson earlier).
