# AC37 engineering: a self-funded world that resolves orders at short horizons — but NOT at study scale

2026-09-15. `ac37_selfsufficient.py`, `ac37_engineering.py`, engineering only. **No protocol was
written and no final seed was run: the pre-declared validity criterion fails at study scale.** This
records the mechanism, the scan, the study-scale measurement that stopped the study, and the process
finding underneath it.

> **Correction to this document's first version**, which was titled "a self-funded world that DOES
> resolve orders" and rested on the scan alone. The scan measured the endpoint at 300 ticks on a
> 72-order sample (ratio 22.1). At the study's own scoring scale — 600 ticks, the paired 12-seed set,
> a full 720-order sweep — the endpoint gives **margin 5.92 against noise sd 0.83, ratio 7.16**,
> below the criterion of 10 that this module declared before any of it was run. The study stops here.

## The problem, and the fix

AC35 had the organism's own productive sites supply its energy, and the endpoint collapsed: spread 1.00
site against 0.30 of noise, because production scales with the living population, so a population near
carrying capacity maintains itself easily and **every order converges to 76–80% of maximum**.

The fix, stated before it was tested: add a **constant metabolic drain** that does not scale with the
population. The balance becomes

    E' = E + (productive sites)/PRODUCTION_PERIOD − DRAIN − RENEW_ENERGY × renewals

so self-sufficiency requires `productive sites > DRAIN × PRODUCTION_PERIOD` — a **population floor set by
the economy**, not by carrying capacity. An order that wastes renewals sits nearer that floor; a good
order sits above it, and the punishment is graded rather than a collapse.

## The scan, and the economy it selects

18 configurations (production period 4/6/8 × drain 1–6), 72 sampled orders, 300 ticks, 2 seeds:

| | mean sites | spread | noise sd | ratio |
| --- | ---: | ---: | ---: | ---: |
| period 4, drain 1 | 22.31 | 1.50 | 0.09 | 17.6 |
| period 4, drain 2 | 22.31 | 1.50 | 0.09 | 17.6 |
| **period 4, drain 3** | **16.22** | **11.00** | **0.50** | **22.1** |
| period 6, drain 1 | 21.71 | 6.00 | 0.17 | 36.2 |
| period 4/6/8, drain ≥ 4 mostly | 0.8–4.2 | 0.5–3.0 | 0.1–0.3 | 10–52 |

**Chosen economy: production period 4, drain 3.** Self-funded (the organism's own sites produce the
energy), a population floor makes falling behind costly, and the endpoint carries an **11.00-site
spread against 0.50 of noise — ratio 22.1**.

Two things the scan makes visible:

1. **The drain is what creates the graded region.** With drain 1–2 the population saturates at 22.31 and
   the spread is 1.50 — the AC35 failure, reproduced by a different route. At drain 3 the population
   settles at 16.22 and the spread jumps to 11.00. This is the predicted mechanism, measured.
2. **A high ratio alone is not a valid endpoint.** Seventeen of the eighteen configurations exceed the
   ratio-10 criterion, but most of them sit at a mean population of ~1 site — organisms on the edge of
   death, where the "spread" is a few dying individuals rather than a graded maintenance outcome. The
   validity criterion therefore required **both** ratio ≥ 10 **and** a mean in the graded range
   (3 < mean < 20), which excluded them. Requiring only the ratio would have selected a degenerate
   world and produced a confident-looking study about nothing.

## The study-scale measurement, and the stop

At the scale the study would actually be scored at — 600 ticks, the paired 12-seed set (9000–9011), a
full 720-order sweep for the optima — the same economy gives:

| quantity | value |
| --- | ---: |
| regime A optimum (full 720 sweep, paired seeds) | `(4,5,1,2,0,3)` = **7.75** |
| regime B optimum | `(0,4,1,3,2,5)` = **7.67** |
| A's optimum rated under B | **1.75** |
| **margin** | **5.92** |
| per-order noise (8 disjoint seed sets) | **sd 0.83** |
| **margin / noise** | **7.16** — below the criterion of 10 this module declared |

The scan's ratio of 22.1 came from 300 ticks and a 72-order sample; at the study's own scale the noise
grows faster than the spread (0.83 vs 6.83). **The study stops. No protocol, no final seeds, no claim.**

**And it stops even though the arms look encouraging.** The same engineering run measured a large arm
separation: `learner_both` 5.08–7.67, `oracle_b` 7.67, `no_release` 1.75–2.58, `oracle_a` 1.75,
state-blind 1.42–3.75. Using that as licence to proceed would be precisely the failure this line's rules
forbid — adjusting the design until the hypothesis wins. The pre-declared criterion failed; the study
does not proceed.

## The process finding underneath it

The criterion is *inherited*: "margin/noise ≥ 10" was declared for AC32's endpoint and reused in AC35,
AC36 and here. But AC32's endpoint was scored by a **paired** design, in which the seed-set identity
variance cancels in the arm comparison — so the quantity that criterion measures is not obviously the
quantity that limits a paired study. AC32 passed it (16.15) and its arms separated; AC36 passed it
(16.6) and its arms separated; here it fails and the arms *also* look separated. So either the criterion
is conservative for paired designs, or an arm separation at this noise level is a coincidence.

**Both readings require the same thing, and neither licenses proceeding now**: a successor must justify
its own threshold from the variance that actually limits a paired comparison (the interaction, not the
between-seed-set variance), *before* its seeds — and if that justification is derived from the same
data that made the arms look good, it is not a justification. That is a piece of statistical design work
this line has not done yet, and it is now on the list.

## What this does and does not establish

- **Establishes**: the drain mechanism works as predicted at short horizons — a population floor creates
  a graded region (drain 1–2 saturates at 22.31 sites with a 1.50 spread; drain 3 settles at 16.22 with
  an 11.00 spread). Self-funding is not inherently incompatible with a resolving endpoint.
- **Does not establish** that this world can carry a claim: at study scale its endpoint fails the
  pre-declared criterion. No protocol exists, no final seed was spent, no claim is made.
- **Not autopoiesis, not survival, not life.** The endpoint is sites retained by an organism that pays a
  constant cost to stay alive and produces energy from its own sites. Nothing here speaks to
  self-production in any stronger sense, or to experience or understanding.
- Three prerequisite stops now stand in this line (AC31, AC35, AC37) against two passing claims
  (AC33, AC36) — all five decisions made before any final seed was spent, which is the process working.

## The next step

Two things, in order:

1. **Justify the validity threshold for paired designs** — derive the noise that actually limits a paired
   arm comparison, state it, and re-derive the criterion from it. This is analysis, not a new world, and
   it is a prerequisite for any further endpoint work.
2. Then either reduce AC37's noise (more scoring seeds per rating, longer horizon) so the existing
   criterion passes honestly, or choose a sharper economy — but with the criterion's provenance settled
   first, so the next measurement cannot be a threshold in disguise.

## Artifacts

`ac37_selfsufficient.py`, `ac37_engineering.py`, `test_ac37.py`, `/tmp/ac37_scan.json`,
`/tmp/ac37_engineering.json`. Related: `AC35_ENGINEERING_v1.md` (the same endpoint failing for a
different reason), `AC36_RESULTS_v1.md` (the passing insufficient-income study), `AC32_RESULTS_v1.md`
(where the inherited criterion was declared).
