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

## Post-hoc sanity check (2026-09-15) — verified at its horizon, but NOT self-sufficiency

A sanity check run after the freeze measured the endpoint's structure directly and found three things
the protocol's framing did not anticipate:

1. **The endpoint is bimodal, not graded.** Per scoring seed, the B-optimum organism either survives
   near carrying capacity (16–23 sites) or dies (0–2 sites): 7 of 12 seeds are dead at 600 ticks, 3
   survive. The mean "7.67" is a survival-weighted mix, not a graded population. AC36's
   insufficient-income world is genuinely graded (6–8 vs 4–6 sites, 0/12 dead) — the bimodality is
   specific to this drain world.
2. **The claim is horizon-unstable.** The learner-vs-keeper difference (oracle_b − oracle_a as the clean
   proxy) is +5.00 at 200 ticks, peaks at +6.75 at 400, collapses to +1.50 at 800 and −0.08 at 1000, and
   stays negative (−0.33) at 1500–2000 once both arms are dead. The "retention" is a transient of the
   population's death, not a stable advantage. This is AC34's rejected binary endpoint, re-entering
   through a bimodal retention metric.
3. **"Self-sufficiency" overstates.** The break-even floor is `sites > 12`, but the measured population
   is ~7 and declining; energy runs negative (−861 at 600 ticks). The organisms are not stably
   self-maintaining — they are dying, and the good order dies slower.

**Correction, recorded not retracted.** The claim that passed all nine gates — *at 600 ticks, the
release-and-re-acquire arm retains more population than the keep-stale arm* — is true and verified at its
declared horizon. But it is a horizon-specific, survival-transient result, not "graded population
retention" and not "self-sufficiency". The protocol's own §6 ("this is graded population retention") is
wrong, as is the resume's "self-sufficiency line closed". AC37's stop was therefore **not purely a
criterion artifact**: its ratio degraded (22.1 → 7.16) because the bimodality was emerging, and the
sign-flip test resolves the 600-tick contrast without checking whether the endpoint is stable. **The
self-sufficiency line remains open.**

## Next

The self-sufficiency line is **open**, not closed. To close it, the world must produce a *stable, graded*
self-maintaining population — a drain the organism can actually sustain (or a horizon at which the
population is not in mid-collapse) — and the endpoint's per-seed distribution and horizon stability must
be checked before any protocol, not after. The AC19 maintenance line (AC43/AC45) stands as verified. The
broader-developmental-function arc (AC20–AC28) is also open.
