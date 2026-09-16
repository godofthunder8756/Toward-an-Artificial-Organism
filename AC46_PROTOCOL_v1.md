# AC46 PROTOCOL v1 — registered before the first final seed

**Endorsement.** This protocol was written and its source list hashed **before** any final seed was run.
The result directory is created with `mkdir(exist_ok=False)`, so a frozen directory can never be
overwritten. A self-declared defect elsewhere causes a hash mismatch; none is declared here.

## 1. The claim, in the form its own shape permits

*In a self-funded world — the organism's own productive sites supply its energy, and a constant metabolic
drain sets a population floor — after the stress regime changes so a different order is best, an organism
that can release its stored order and search again retains more population than one that cannot.*

The endpoint is **sites retained** (population) at the end of 600 ticks under regime B. The world is
unchanged from AC37 (production period 4, drain 3), whose stop was re-examined and re-opened by
AC46's engineering (see AC46_ENGINEERING_v1.md).

**Why the paired test, not the old criterion.** AC37 stopped on "margin/noise ≥ 10", which measures the
*marginal* noise (sd of one order across seed sets). AC38 showed a paired arm comparison does not face
that variance, and supplied the correct test: the exact sign-flip test on paired per-individual
differences. The claim's shape is categorical (the learner retains more in every individual), so the gate
set carries both the sign-flip test (G1) and the separation of minima (G3).

## 2. Design

| item | declared value |
| --- | --- |
| world | self-funded: production period 4, drain 3 (AC37's economy) |
| capable arm | `learner_both` (releases the stored order, searches again under B) |
| cut arm | `no_release` (keeps the A-acquired order under B) |
| state-blind controls | `no_search`, `preserve` (both hold the random initial order) |
| oracle controls | `oracle_b` (B-optimum, ceiling), `oracle_a` (A-optimum, floor) |
| endpoint | sites retained at 600 ticks under regime B, rated on the shared 12-seed scoring set |
| individuals | **seeds 4700–4711 = 12** |
| freshness | engineering used seeds 4600–4611; these 12 are disjoint from it and from every prior family |
| **separation bar** | **BAR = 4.0** — between learner worst (5.00) and no_release best (2.50) on engineering |
| **effect-size bar** | **median paired difference ≥ 3.0 sites** — engineering median 4.50 |
| runner | `ac46_selfsufficiency.py` (`main`), result directory `ac46_results_v1/` |
| sources | hashed into `pre_run_snapshot.json` before the first individual |

## 3. Declared gates — all nine must pass

| gate | criterion | declared from |
| --- | --- | --- |
| **G1 resolvable** | sign-flip test on the 12 paired differences, **p ≤ 0.01** and n ≥ 8 | AC38's lesson: resolvability is tested, not assumed; engineering hit the floor 0.00049 |
| **G2 effect size in endpoint units** | **median paired difference ≥ 3.0 sites** | engineering median 4.50, in the endpoint's own units (AC41's error was copying another ledger's unit) |
| **G3 separation of minima** | min(`learner_both`) ≥ 4.0 **and** max(`no_release`) < 4.0 | engineering: 5.00 vs 2.50, a 2.5-site gap |
| **G4 oracle_b ceiling above bar** | min(`oracle_b`) ≥ 4.0 | the B-optimum must clear the bar, bracketing the claim's top |
| **G5 oracle_a floor below bar** | max(`oracle_a`) < 4.0 | the A-optimum must sit below, bracketing the bottom |
| **G6 state-blind means below bar** | mean(`no_search`) < 4.0 **and** mean(`preserve`) < 4.0 | a random order must not clear the bar on average; one lucky individual does not falsify (AC36's precedent) |
| **G7 completeness** | all 12 declared individuals present, no substitution | — |
| **G8 determinism** | re-running two individuals reproduces them exactly | — |
| **G9 register in the loop** | every held order is a 6-tuple that was written to and read from the register | the re-acquisition goes through the register, not a hidden copy |

**This gate set is frozen.** No threshold may be moved after results are seen. If a gate fails, the study
is recorded as failed and a successor protocol is written; the existing result directory is never re-run.

## 4. The AC40 four-check, run before this protocol

Applied to the paired differences at engineering seeds 4600–4611 (disjoint from the finals 4700–4711),
before this protocol was written:

| check | result |
| --- | --- |
| resolvability | p = 0.00049, n = 12 — resolved at the power floor |
| effect size | median +4.50 sites, min +3.25 — in the endpoint's own units |
| stability | ratio unstable (AC40 finding #2: the ratio does not discriminate); impaired fraction and per-individual differences reported directly |
| headroom | learner at 5.0–7.67 of 24 sites — no ceiling, not saturated |

## 5. Predictions registered in advance

1. The 12 paired differences resolve at p ≤ 0.01 (the floor 2/2¹² = 0.00049 if all are positive).
2. Separation of minima: every learner individual ≥ 4.0, every no_release individual < 4.0.
3. Median paired difference ≥ 3.0 sites.
4. oracle_b ≥ 4.0 (ceiling) and oracle_a < 4.0 (floor) for every individual.
5. State-blind means < 4.0.

## 6. What is excluded from the claim, in advance

- Not an experience, an understanding, or a life; the endpoint is sites retained.
- Not autopoiesis or closure. "Self-sufficiency" here means the organism's own sites fund its energy, and
  a constant drain makes that funding load-bearing; nothing is claimed about self-production in any
  stronger sense.
- Not survival: the binary alive/dead endpoint was rejected in AC34; this is graded population retention.
- Not a general law of development: it is a measured difference between one action set and one
  degradation of it, on a frozen world, at declared seeds.
- Comparisons to anything outside this line are not offered.

## 7. Verification to be performed after the finals

- `audit_ac46.py`: recompute every gate from `rows.jsonl`, independently of the runner.
- `replay_ac46.py`: reproduce two individuals in a fresh process.
- `test_ac46.py`: assert the recorded gate values, the frozen shas, and that the protocol's declared
  source list equals the hashed set (`preflight`).

SOURCES (declared): ac46_selfsufficiency.py ac33_search.py ac30_acquire.py ac29_register.py ac38_variance.py AC46_PROTOCOL_v1.md
