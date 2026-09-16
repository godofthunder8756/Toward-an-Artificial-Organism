# AC63 engineering: the grace period is the structural control on corruption's cost

2026-09-15. Engineering prerequisite. **No protocol, no final seeds, no claim.**

## The finding

AC62 found the repair/re-acquisition complementarity (AC61) is dynamically inert: corruption produces a
random order, and the critical region survives anyway, so repair-only loses ~0–4% versus re-acquire.
AC62's proposed fix — make the critical region low-stress (rare-urgent) so a random order risks it — was
tested and did *not* work: corruption remained cheap (median 618, though a bimodal mean gap of ~7,800
showed a few catastrophic seeds).

The actual control is the **grace period** — the `URGENT` window, the number of ticks a stressed site has
before it expires. Swept with the critical region low-stress:

| URGENT window | corruption (optimal − random) p | median | optimal mean | random mean |
| --- | --- | --- | --- | --- |
| 16 (default) | 0.0107 | 751 | 68,197 | 57,360 |
| 8 | 0.0010 | 19,902 | 66,326 | 42,365 |
| 4 | 0.0039 | 39,672 | 61,406 | 33,414 |
| 2 | 0.0039 | 25,959 | 39,224 | 19,426 |

The mechanism is simple and general: the order repairs one region per tick, so an urgent site is caught
within roughly `REGIONS` ticks of the order reaching its region. When the grace period (16) comfortably
exceeds that, a *random* order still catches the critical region — corruption is cheap. When the grace
period (4) is comparable to or below the regions-per-tick budget, a random order *misses* the critical
region's brief urgency — corruption is costly, and re-acquisition's recovery is worth having.

## Consequence

The complementarity AC61 identified is freezable at **URGENT = 4**: there, corruption is costly (median
~39,700, ~65% of the optimal arm), so the contrast repair-only vs. repair+re-acquire has room to resolve.
URGENT = 2 degrades the world too far (optimal mean collapses to 39,224). URGENT = 4 is the operating
point.

## Bounds

No claim. Engineering prerequisite. The next study would freeze the complementarity at URGENT = 4, using
AC62's single-disruption design (repair-freeze vs re-search).

## Artifacts

This document (the sweep was an inline check). Related: `AC62_ENGINEERING_v1.md` (the inertness),
`AC61_ENGINEERING_v1.md` (the complementarity), `ac29_register.py` (the register).
