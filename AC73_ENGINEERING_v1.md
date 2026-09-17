# AC73 engineering v1: self-directed rule production is information-limited, not local-optimum-limited

2026-09-17. `ac73_engineering.py`, `ac73_engineering_addendum.py`. **No protocol, no final seeds, no
claim.** Prerequisite measurement for the "self-produced rules" study that AC72 flagged as the one
remaining gap.

## The question

AC72's next step named a mechanism: a **population-based self-directed learner** to eliminate the local
optima that AC30's single-climber hit (63% of the margin captured). The premise to test: the 63% cap is a
*search* problem (single-climber gets stuck), so a population — which maintains diversity and applies
selection pressure — should escape the basins and reach the level the world permits.

## What was measured

In the AC32/33 regime-B world (ceiling `(2,0,1,3,5,4)` = 12.67 sites), on engineering seeds 8000–8011,
four mechanisms scored by two different signals. "Single-life" = the organism's own realized outcome (one
800-tick run, one seed — self-directed, no external oracle). "Oracle" = the 12-seed mean used by
AC32/AC33 (external, reporting the true order quality).

| mechanism | scoring signal | gap to ceiling (mean of 12 seeds) |
| --- | --- | ---: |
| single-climber (AC30's mutate-and-keep) | single-life | **0.87** |
| population (16 × 10 gens) | single-life | **0.84** |
| population, running-mean across 12 environments | single-life (accumulated) | **0.86** |
| population (12 × 8 gens, 4 seeds) | **oracle** | **0.09** |

The population is a sound search: with oracle scoring it reaches the ceiling (0.09), beating AC33's
steepest ascent (0.34). But on the organism's own signal it is indistinguishable from the single-climber.

## Why: the signal, not the search

The decisive measurement is the single-life noise against the fine gap it must resolve:

| quantity | value |
| --- | ---: |
| single-life score of the **ceiling** order (200 seeds) | mean 12.15, **sd 0.94**, range 9–14 |
| single-life score of a **mediocre** order `(0,1,2,3,4,5)` | mean 12.27, sd 1.05 |
| true (oracle) gap, ceiling − mediocre | **0.25 sites** |
| single-life gap, ceiling − mediocre | **−0.12** (mediocre looks *better*) |

The ceiling order and a mediocre order differ by only **0.25 sites** on average, while a single life's
noise is **0.94 sites** — nearly 4× the gap. A single lifetime cannot even tell them apart (the mediocre
order scores *higher* on single lives). The orders near the ceiling form a plateau whose internal
differences are below the single-life noise floor. No search mechanism — climber, population, or an
accumulating population — can resolve a difference the signal does not carry.

The running-mean accumulation did not help either, for a concrete reason: selection acts every generation
on a *partial* mean, and new children are born with no history, so a promising mutation is selected out on
a one-sample estimate before it can accumulate the lives that would verify it. (12 environments is also
only enough to bring a survivor's estimate partway to the oracle's 12-seed precision.)

## What this corrects

The handoff's premise — that the 63% cap is a local-optima problem a population fixes — is **falsified by
measurement**. The 63% (≈0.85 sites below ceiling here) is the **information floor of single-lifetime
evaluation**: the organism's own production signal, over one life (or a few accumulated lives), does not
carry enough information to distinguish the ceiling rule from a good-enough rule. AC30's "local optima"
were never the obstacle; the signal was.

The positive reading: a self-directed learner still captures the *bulk* of the margin (it reliably finds
a good-enough rule, ~0.85 of 12.67 — far above random), and that may be all an organism needs for
viability. What is *not* obtainable self-directedly is the fine last ~0.25 of ranking.

## The reframed question for the self-produced-rules study

"Make the rules produced by the organism's own activity" is now two distinct questions:

1. **Mechanism** (solved here, negatively): no search algorithm lifts the single-life cap. A population
   is not the fix.
2. **Signal horizon**: does a long-lived organism accumulate enough *independent* environmental signal
   within one lifetime to resolve the fine plateau? In the AC30 world the "environment" is a fixed 800-tick
   life; in the main organism the environment changes over 65,536 ticks (route moves, damage). Whether that
   changing context supplies the multi-environment averaging the ceiling needs — without an external
   oracle, and without the confound that the rule interacts with the environment — is the real open
   question, and it is a *world* question, not a *search* question.

## Bounds

Engineering prerequisite. No claim, nothing frozen, nothing about autopoiesis/consciousness/life. The
measured quantities are sites retained and gap-to-ceiling in a declared ranking world.

## Artifacts

`ac73_engineering.py`, `ac73_engineering_addendum.py`. Related: `AC72_FINDING_v1.md` (the gap this
scopes), `AC30_ACQUIRE_v1.md` (the 63% and the "population" suggestion), `AC33_RESULTS_v1.md` (the oracle
that reaches the ceiling), `AC32_RESULTS_v1.md` (the paired-scoring noise measurement).
