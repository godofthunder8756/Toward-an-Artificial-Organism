# AC47 engineering: a stable, graded self-funded world does not exist in this architecture

2026-09-15. `ac47_stable_world.py`, engineering prerequisite. **No protocol was written and no final
seed was run.** This is a world-design scan that answers, in the negative, the question AC46's sanity
check left open: is there a self-funded world whose population and energy reach a *stationary band*
while the order still meaningfully differentiates the outcome?

## The scan

63 configurations — production period {4, 6, 8} × stress multiplier {1, 2, 3} × drain
{1.0 … 3.0} — each with the B-optimum order run at horizons 300/600/900/1500 over 8 scoring seeds,
reporting mean sites, mean energy and dead-seed count. Two criteria:

- **stable** — population not declining across horizons, energy non-negative, 0/8 seeds dead;
- **graded** — B-vs-A spread ≥ 3 sites (the order matters).

| | count |
| --- | ---: |
| configs scanned | 63 |
| stable | 9 |
| graded (spread ≥ 3) | 7 |
| **both** | **0** |

The two requirements exclude each other, and not by tuning luck — by structure.

## The two failure modes are two faces of one limit

- **Stable configs are saturated.** The best spread any stable config achieves is **2.0 sites**
  (p4, stress 3, drain ≤ 2.0): B-optimum 21.8 sites vs A-optimum 20.3, both near capacity 24, 0/12 dead,
  energy rising. The order keeps 91% vs 84% of maximum — barely distinguishable. This is AC35's
  saturation ("every order converges to 76–80% of maximum"), reproduced at every stable setting.
- **Graded configs are collapsing.** The only configs with spread ≥ 3 (up to 9.4 sites) all carry dead
  seeds (1–8 of 8) and a declining population, and the worst of them go energy-negative. The spread
  exists only while the population is dying — AC46's bimodal, horizon-unstable regime.

## Why this is structural, not a matter of more search

Self-funding means production ∝ population. At any stable equilibrium the energy balance is

    population / period  =  drain  +  renewal_cost × (renewal rate)

which pins the equilibrium population to the economics (drain, production period, renewal cost),
**independent of the order**. The order only shifts the effective renewal rate (a good order renews the
right sites, so it needs fewer renewals per site alive). That shift moves the equilibrium population
noticeably only when the renewal rate is near the viability threshold — i.e. when the denominator
`1/period − renewal_cost/lifetime` is close to zero. Below that threshold (low drain) everyone saturates;
near it, the stochastic stress makes the outcome bimodal (survive-or-die). The graded region is
therefore a *transient of collapse* by construction, never a stable equilibrium.

AC35 (saturation), AC37 (ratio degradation), AC46 (bimodal, horizon-unstable) are not three failures —
they are the same limit observed three ways.

## What a non-trivial fix would require

The order must affect a quantity that is **not** population-at-equilibrium, because the feedback erases
order differences there. Candidates:

1. **Production efficiency** — make a site's energy yield depend on which site it is and which order
   keeps it alive, so the order matters even when the population is saturated.
2. **A graded maintenance target** — the order must maintain a specific *structure* (not merely "keep N
   sites alive"), where getting the structure right is graded and worth more than a raw site count.
3. **Abandon self-funding for the maintenance claim** — AC36 already achieves stable, graded maintenance
   under a *fixed external* income; the self-funding feedback is precisely what erases the graded
   region, so "self-sufficiency" and "graded" are in direct tension here.

## What this does and does not establish

- **Establishes**: within this architecture (population-proportional production + fixed drain +
  stochastic stress), no configuration yields a stable *and* graded self-funded world; the graded
  region exists only during collapse. This delimits how far the present architecture can go toward
  "self-sufficiency" — the review's own stated test.
- **Does not establish**: any claim about an organism. No protocol, no final seeds, no frozen
  directory, no claim. It is a measurement about a world's endpoint structure, and it is a *negative*
  result. Not autopoiesis, closure, or life.

## Artifacts

`ac47_stable_world.py`. Related: `AC46_RESULTS_v1.md` (the sanity check that posed the question),
`AC35_ENGINEERING_v1.md` (saturation), `AC37_ENGINEERING_v1.md` (the drain fix that introduced the
collapse), `AC36_RESULTS_v1.md` (the fixed-income world that *does* grade stably).
