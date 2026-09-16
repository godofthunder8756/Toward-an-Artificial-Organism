# AC49 engineering: heterogeneous site value breaks the self-funding limit — a stable, graded world exists

2026-09-15. `ac49_heterogeneous.py`, engineering prerequisite. **No protocol, no final seeds, no claim.**
This tests the one fix AC47/AC48 left open and finds that it works.

## What was tested

AC47/AC48 showed that under *homogeneous* sites, the self-funded world cannot be both stable and graded:
the order's only lever (which site to renew) moves the outcome only under scarcity, and scarcity in
self-funding is the death regime — so the graded region is a transient of collapse, under every
production shape and stress regime.

AC49 changes what the order acts on: sites are **heterogeneous in production value**
(`REGION_VALUES = (5, 4, 3, 2, 1, 0.5)`), production is the value-weighted sum of living sites, and the
endpoint is **cumulative value-weighted production** (horizon-robust, like AC43's ledger totals). Scarcity
is provided by the renewal *action rate* (one site per tick), with energy kept abundant by a low drain so
there is no death spiral.

## Result: stable, horizon-robust, resolvable

At period 4, stress 3, drain 2 (12 scoring seeds, 600 ticks):

- **0/12 seeds dead** — and this holds at every config scanned (stress 3–8 × drain 1–3).
- Production is **linear in time** (B: 8,850 at 600 → 22,020 at 1500) — a steady state, not a transient.
- B-vs-A production: **8,850 vs 7,644, ratio 1.16, mean paired difference +1,206, p = 0.00146**, 11/12
  individuals impaired.

## The mechanism is the order's priority, not survival

Per-region living sites (4 seeds): B-opt keeps the high-value region 0 at 4/4 while A-opt lets it deplete
to 1.75/4 (keeping low-value regions instead). Total value retained: **B 58 vs A 46**. The order's renewal
priority decides *which* sites survive; with heterogeneous values that becomes a persistent production
difference, at a stable equilibrium where the population is near capacity and nothing dies.

## What this changes

AC47/AC48's delimiter ("self-funding and order-valued maintenance are incompatible") is **overturned for
homogeneous sites only**. With heterogeneous site value, the graded region is no longer a transient of
collapse — it is a stable, horizon-robust property. The earlier line (AC35/AC37/AC46/AC47/AC48) was
delimiting the *homogeneous* world, and the fix is site heterogeneity, exactly as AC47's "production
efficiency" clause named.

## What remains before a frozen study

1. **Crisp the re-acquisition claim.** Make the value structure align with the regime (so "re-acquiring
   under B" means re-prioritizing for B's value), and re-derive the optima for the value-weighted world
   rather than inheriting the homogeneous optima.
2. **Strengthen the effect.** The current ratio 1.16 is real but modest (AC36's fixed-income world shows
   1.37). A wider value spread should widen it; check that it stays stable and resolvable.
3. Then the usual cycle: AC40 four-check → protocol → finals → audit → replay → tests.

## Artifacts

`ac49_heterogeneous.py`. Related: `AC47_ENGINEERING_v1.md` / `AC48_ENGINEERING_v1.md` (the delimiter this
overturns), `AC36_RESULTS_v1.md` (the fixed-income graded world this now parallels in a self-funded form).
