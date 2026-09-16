# AC46 RESULTS v1 — the self-sufficiency line is closed: the AC37 world passes under the correct paired test

## What ran

`ac46_selfsufficiency.py finals` on the self-funded world (production period 4, drain 3, unchanged from
AC37), seeds 4700–4711 = 12 individuals, the AC33/AC36 arm family, endpoint = sites retained at 600 ticks
under regime B. Protocol `AC46_PROTOCOL_v1.md` was registered and its source list hashed before the first
final seed; the AC40 four-check and the re-opening measurement were recorded in `AC46_ENGINEERING_v1.md`
first.

## Verdict: all nine gates pass — a clean, verified claim

| gate | result | measured |
| --- | --- | --- |
| G1 resolvable | **PASS** | sign-flip p = 0.00049 (the 2/2¹² floor), n = 12 |
| G2 effect size in endpoint units | **PASS** | median paired difference 4.58 sites ≥ 3.0 |
| G3 separation of minima | **PASS** | learner worst 5.00 ≥ 4.0; no_release best 2.25 < 4.0 |
| G4 oracle_b ceiling above bar | **PASS** | 7.67 ≥ 4.0, every individual |
| G5 oracle_a floor below bar | **PASS** | 1.75 < 4.0, every individual |
| G6 state-blind means below bar | **PASS** | no_search/preserve mean 2.34 < 4.0 |
| G7 completeness | **PASS** | 12/12, no substitution |
| G8 determinism | **PASS** | two individuals re-run exact |
| G9 register in the loop | **PASS** | every held order a 6-tuple through the register |

## The numbers (fresh seeds 4700–4711)

| arm | min | mean | max |
| --- | ---: | ---: | ---: |
| learner_both (releases + re-acquires) | 5.00 | 6.56 | 7.67 |
| no_release (keeps the stale order) | 1.75 | 1.81 | 2.25 |
| no_search / preserve (random order) | 0.83 | 2.34 | 4.83 |
| oracle_a (A-optimum under B) | 1.75 | 1.75 | 1.75 |
| oracle_b (B-optimum) | 7.67 | 7.67 | 7.67 |

All 12 individuals are impaired (learner > no_release in every one); the paired difference hits the
sign-flip test's power floor.

## What this closes

The **self-sufficiency line** has been open since AC35 (spread 1.00 vs noise 0.30) and AC37 (ratio 7.16
< 10), both stopped before a final seed. AC46 closes it, and the route is not a retuned world but a
**corrected test**: AC37's stop criterion measured the *marginal* noise (sd of one order across seed
sets), which a paired arm comparison never faces. AC38 supplied the honest test — the exact sign-flip
test on paired per-individual differences — and AC46 applied it to the unchanged AC37 world. The world
was valid all along; the criterion was not.

This is the **fourth verified frozen claim** (AC33, AC36, AC43, AC46), and the first where the organism's
own production funds its maintenance under a constant metabolic drain — maintenance is load-bearing
because self-sufficiency requires `productive sites > 12`, a population floor set by the economy rather
than by carrying capacity.

## Verification performed

- `audit_ac46.py` — PASS: nine gates recomputed independently, 6 source hashes unchanged.
- `replay_ac46.py` — PASS: two individuals × six arms reproduce exactly in a fresh process.
- `test_ac46.py` — 12 tests OK: all nine gates, power-floor p, separation of minima, seed disjointness,
  source hashes, preflight, claim discipline.

## What this does and does not establish

- **Establishes**: in a self-funded world, after the regime changes, the ability to release a stale order
  and re-acquire retains more population than keeping it — under the correct paired test, on fresh seeds,
  with the oracle and state-blind controls in place.
- **Does not establish**: autopoiesis or closure. "Self-sufficiency" means the organism's own sites fund
  its energy and a constant drain makes that funding load-bearing; nothing is claimed about
  self-production in any stronger sense. Not survival (AC34's rejected endpoint). Not experience,
  understanding, or life; the endpoint is sites retained.

## Next

The self-sufficiency line is closed. The AC19 maintenance line (AC43/AC45) and the self-sufficiency line
(AC46) both now stand as verified claims. The remaining open route from the record is the
broader-developmental-function arc (AC20–AC28, 9.49 effective bits of order structure), whose machinery
has room to be extended.
