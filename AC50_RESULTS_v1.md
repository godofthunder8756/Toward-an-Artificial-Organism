# AC50 RESULTS v1 — stable graded self-sufficiency exists, via heterogeneous site value

## What ran

`ac50_heterogeneous.py finals` on a self-funded world with **regime-dependent heterogeneous site value**
(`VALUES_A = (5,4,3,2,1,0.5)`, `VALUES_B = reversed`; stress reverses too), seeds 4800–4811 = 12
individuals, the AC33/AC36 arm family, endpoint = cumulative value-weighted production under regime B.
Protocol `AC50_PROTOCOL_v1.md` registered and hashed before the first final seed.

## Verdict: all nine gates pass

| gate | result | measured |
| --- | --- | --- |
| G1 resolvable | **PASS** | sign-flip p = 0.00049 (the 2/2¹² floor), n = 12 |
| G2 effect size in value-units | **PASS** | median paired difference 900.5 ≥ 500 |
| G3 stability, no death spiral | **PASS** | 0 dead scoring runs (0/144) |
| G4 horizon-robust steady state | **PASS** | production@1500/@600 = 2.49 (linear = 2.50) |
| G5 oracle_b ceiling | **PASS** | oracle_b 8928.9 ≥ learner min 8917.6 |
| G6 state-blind below learner | **PASS** | no_search/preserve mean 8468 < learner 8926 |
| G7 completeness | **PASS** | 12/12 |
| G8 determinism | **PASS** | two individuals re-run exact |
| G9 register in the loop | **PASS** | every held order a 6-tuple through the register |

## The numbers (fresh seeds 4800–4811)

| arm | min | mean | max |
| --- | ---: | ---: | ---: |
| learner_both (releases + re-acquires) | 8917.6 | 8926.1 | 8928.9 |
| no_release (keeps the stale order) | 7933.8 | 8001.7 | 8028.3 |
| oracle_b (B value-optimum) | 8928.9 | 8928.9 | 8928.9 |
| oracle_a (A value-optimum) | 8028.3 | 8028.3 | 8028.3 |
| no_search / preserve (random) | 8126.5 | 8467.8 | 8827.5 |

The learner reaches the ceiling (8928.9 = oracle_b); the keeper sits at the A-optimum's level (~8028);
state-blind orders fall between. Every individual impaired, p at the power floor.

## What this establishes — the delimiter is overturned

AC47/AC48 proved that under *homogeneous* sites, the self-funded world cannot be both stable and graded:
the graded region is a transient of collapse, under every production shape and stress regime. AC49 found
the fix and AC50 freezes it: **heterogeneous, regime-dependent site value makes the order's renewal
priority decide *which* sites survive, and that becomes a persistent production difference at a stable,
steady-state equilibrium** — the two properties AC47/AC48 called impossible (stability: 0 dead; horizon-
robustness: linear production). This is the fifth verified frozen claim (AC33, AC36, AC43, AC45-family,
AC50), and the first stable graded self-funded result in the line.

The effect size is **modest by design** (~11%): the order can only differentiate the ~10% of sites that
die at a stable equilibrium, and AC49 showed widening the value spread saturates. This is a claim about
the *existence* of a stable graded self-funded regime, not about a large effect.

## One harness bug caught by the gates, and fixed before freezing

The first finals run failed G5 (oracle_b below the learner). The cause was a harness bug, not the
science: the declared optima had been computed on **8** scoring seeds in a single-start climb, while the
finals score on **12**, so `OPT_B` was a local optimum and the learner's search (from more starts) beat
it. The optima were recomputed on the 12 scoring seeds with a 24-start climb (`OPT_B = (3,2,4,5,1,0)`,
score 8928.88 — matching the learner's best), the buggy run was discarded uncommitted, and the finals
were re-run. Disclosed here rather than hidden.

## Verification performed

- `audit_ac50.py` — PASS: nine gates recomputed independently (including a fresh 1500-tick re-run for
  G4), 6 source hashes unchanged.
- `replay_ac50.py` — PASS: two individuals × six arms reproduce exactly in a fresh process.
- `test_ac50.py` — 11 tests OK.

## What this does and does not establish

- **Establishes**: a stable, horizon-robust, resolvable graded self-funded world exists via heterogeneous
  site value, and release-and-re-acquire retains ~11% more production value than keep-stale there.
- **Does not establish**: autopoiesis or closure ("self-funded" means the organism's own sites fund its
  energy); survival (endpoint is cumulative production, not alive/dead); a large effect (it is ~11% by
  the structural bound AC49 measured); experience, understanding, or life.

## Next

The self-sufficiency line, delimited for homogeneous sites, is now closed for the heterogeneous-value
world. Remaining open: the richer-developmental-function arc (AC20–AC28), and the broader question of
whether the effect can be made larger by a design that lets more sites differentiate at equilibrium.
