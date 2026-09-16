# AC48 engineering: the self-funding limit is not about production shape or stress variance

2026-09-15. `ac48_concave.py`, engineering prerequisite. **No protocol, no final seeds, no claim.** This
tests two candidate fixes for the AC47 delimitation and rules both out.

## The two hypotheses AC47 left open, and their tests

AC47 showed the self-funded world (linear production ∝ population, fixed drain, stochastic stress) cannot
be both stable and graded: stable configs saturate (order effect ≤ 2 sites of 24), graded configs
collapse (bimodal death). Two plausible "just tune it" fixes remained:

1. **Stress variance** — the death tails come from correlated stress bursts (unlucky seeds).
   Test: set `BURST_PROBABILITY = 0` (no correlated bursts) and re-scan.
2. **Production shape** — the death spiral is the linear production∝population feedback.
   Test: make production *concave* in population (diminishing returns: high per-site production at low
   population, saturating at high), the standard mechanism that turns a death spiral into a stable
   interior equilibrium. Scanned cap {48, 60, 80, 120} × drain {2.0–4.0}.

## Results: both fail, in the same way

**Burst test** (period 4, stress 3, drain 2.0–3.0): with zero correlated bursts the pattern is unchanged
— stable configs (drain ≤ 2.25) still saturate (spread 1.5, 0 dead), graded configs (drain ≥ 2.5) still
decline and die (4–9/12 dead by 1500).

**Concave test** (normalized so production at 24 sites equals the linear world's): identical. Stable
configs have spread ≤ 2.2 (e.g. cap 48, drain 3.0: B 21.9→20.3, A 19.4, spread 2.2, 0/12 dead); the
first configs to grade (spread ≥ 3.5) all collapse (12/12 dead, or 7/12 and declining).

| variant | stable configs (0 dead) | graded configs (spread ≥ 3) |
| --- | --- | --- |
| linear (AC47) | spread ≤ 2.0 | dead seeds 1–8/8, declining |
| linear, burst = 0 | spread ≤ 1.5 | dead seeds 4–9/12, declining |
| concave (AC48) | spread ≤ 2.2 | dead seeds 7–12/12, declining |

## Why the shape and the noise are both irrelevant

The order's only lever is *which* site to renew when several are urgent. That lever moves the outcome
only when renewal is scarce — some sites must die for the choice to matter. And in a self-funded world,
scarcity means the population is below the break-even where production covers drain plus renewal, which
is exactly the regime where the population-proportional feedback runs the organism down: fewer sites →
less production → less renewal → more death. Concave production and reduced noise move the *threshold*
of that regime; neither removes the coupling between "the order matters" and "the population is dying".

So AC47's delimitation is robust across production shape and stress variance. The graded region is a
transient of collapse by construction.

## The one remaining untested lead

The fixes that change the *world dynamics* (production shape, stress) are now ruled out. What remains is
a fix that changes what the order acts on — **heterogeneous site value** (AC47's "production efficiency"
fix, not yet tested): give sites different production values and make the order determine *which* survive,
with a value-weighted endpoint, under an action-rate-limited scarcity (renewal capped at one site per
tick, energy abundant) rather than an energy-limited one. Whether that produces a stable graded endpoint
is an open question — and if it too fails, the conclusion would be that "self-funding" and "order-valued
maintenance" are incompatible in this architecture, full stop.

## What this does and does not establish

- **Establishes**: the self-funding limit does not come from production shape or stress variance; it is
  structural to the population-proportional feedback. AC35/AC37/AC46/AC47/AC48 are one limit.
- **Does not establish**: any claim about an organism. Prerequisite only. Not autopoiesis, closure, or
  life.

## Artifacts

`ac48_concave.py`. Related: `AC47_ENGINEERING_v1.md` (the delimitation this strengthens),
`AC35_ENGINEERING_v1.md`, `AC37_ENGINEERING_v1.md`, `AC46_RESULTS_v1.md`.
