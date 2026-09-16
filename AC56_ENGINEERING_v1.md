# AC56 engineering: the re-acquisition benefit is negligible in the concentrated-value world

2026-09-15. `ac56_engineering.py`, engineering prerequisite. **No protocol, no final seeds, no claim.**
This measured AC28's stated next step (acquisition + re-acquisition) after AC55 proved the order
load-bearing. It found the re-acquisition contrast **negligible** — and diagnosed why.

## The measurement

Regime A (region 0 critical, value 100) and regime B (region 5 critical, value 100), stress reversed
with the value (the AC50 shape). Climb-found optima: `OPT_A = (5, 4, 3, 0, 1, 2)`, `OPT_B = (1, 2, 0, 5, 3, 4)`.
Contrast: learner (OPT_B, re-acquired under B) vs no_release (OPT_A, stale under B), scored under B.

| | family 1 | family 2 |
| --- | --- | --- |
| p | 0.0005 | 0.0063 |
| median difference | 196 | 264 |
| impaired | 0/12 | 2/12 |
| learner mean | 62804 | 62802 |
| no_release mean | 62541 | 62596 |

The re-acquisition benefit is ~0.3% of production — two orders of magnitude below AC55's ~30%
optimal-vs-worst effect, and not resolvable across two families.

## Why: the deadline balance makes staleness cheap

AC55's WORST order `(2, 4, 1, 0, 3, 5)` puts region 5 *last*, so it neglects the critical region and
loses ~30%. But the *stale* A-optimal order is `(5, 4, 3, 0, 1, 2)` — region 5 *first*. The value-optimal
order is not "highest value first"; it is "rarest urgency first" (deadline scheduling): a high-stress
region is urgent almost every tick, so it is repaired regardless of its position, whereas a low-stress
region is urgent only rarely and must sit early in the order to be caught during its brief window. Under
regime A the low-stress region is region 5, so OPT_A leads with region 5.

The regime reversal swaps stress and value together, so the new critical region (region 5 under B) is
exactly the region the stale order already leads with — staleness is nearly free. The region the stale
order neglects (region 0, fourth) is worth only 1 under B. So keeping the stale order loses ~0.3%.

## What this establishes (negatively, and usefully)

- **Load-bearing and re-acquisition benefit pull in opposite directions on the value structure.**
  AC55 needed *concentrated* value to make the order load-bearing (a large optimal-vs-worst gap); AC50's
  re-acquisition benefit (~30%) was a property of the *graded*-value world, where the reversal changes
  which region's value matters and the stale order's value-priority is wrong by a lot. In the
  concentrated world the reversal changes the optimal *order* but not the optimal *value* — both the
  stale and re-acquired orders keep the single critical region alive.
- **The re-acquisition claim needs a world where the regime change makes the stale order mis-handle the
  new critical region.** A candidate: reverse the *value* but keep the *stress* fixed (so the new
  critical region is one the stale order deprioritises for deadline reasons), or use a partial value
  spread between the graded and concentrated extremes. Not tested here.

## Bounds

No claim. Engineering prerequisite. Not autopoiesis, closure, or life.

## Artifacts

`ac56_engineering.py`. Related: `AC55_RESULTS_v1.md` (load-bearing), `AC50_RESULTS_v1.md` (re-acquisition
in the graded world), `AC28_REGIONS_v1.md` (the acquisition/retention goal).
