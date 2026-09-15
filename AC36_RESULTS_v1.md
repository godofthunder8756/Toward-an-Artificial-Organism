# AC36 RESULTS v1 — graded maintenance under an insufficient income: ALL EIGHT GATES PASS

2026-09-15. Frozen run: `ac36_results_v1/` (seeds **3500–3511**, 12 individuals, 6 arms, 72 rows).
Protocol frozen and hashed before the first final seed (`AC36_PROTOCOL_v1.md`, BAR = 6.45).
**Verdict: the claim is established.**

## The gates

| id | gate | result |
| --- | --- | --- |
| G1 | `oracle_b` ≥ BAR | **PASS** (6.83) |
| G2 | `learner_both` **worst** ≥ BAR | **PASS** — worst **6.67** |
| G3 | `no_release` **best** < BAR | **PASS** — best 5.67 |
| G4 | `oracle_a` best < BAR | **PASS** — 5.00 |
| G5 | state-blind **means** < BAR | **PASS** — 5.53 both |
| G6 | all arms complete | **PASS** |
| G7 | determinism | **PASS** |
| G8 | register in the loop | **PASS** |

## The measured arms (paired 12-seed scoring, regime B)

| arm | min | mean | max |
| --- | ---: | ---: | ---: |
| `learner_both` | **6.67** | 6.71 | **6.83** |
| `no_release` | 4.75 | 5.06 | **5.67** |
| `no_search` | 4.75 | 5.53 | 6.25 |
| `preserve` | 4.75 | 5.53 | 6.25 |
| `oracle_a` | 5.00 | 5.00 | 5.00 |
| `oracle_b` | 6.83 | 6.83 | 6.83 |

The capable arm's **worst** (6.67) is above the structurally-incapable arm's **best** (5.67), and it
reaches the ceiling exactly (6.83) in one individual. Populations sit between 4.75 and 6.83 sites of 24
— nowhere near carrying capacity, which is what makes the comparison informative.

## Why this endpoint works where two others did not

This line tried three economies for a maintenance endpoint, and the difference is visible in one number
— the spread across orders:

| world | spread | outcome |
| --- | ---: | --- |
| AC30: generous declared income | 5.00 sites | endpoint measured ordering, not maintenance |
| AC35: production-funded by the organism's own sites | **1.00** | prerequisite FAILED (noise sd 0.30; production scales with the living population and equalizes every order toward carrying capacity) |
| **AC36: fixed income below demand** | **2.17** | **margin/noise 16.6, all gates pass** |

The insufficiency is what does the work: energy arrives at 1/tick independent of the organism's state
and a renewal costs 5, so the organism refuses a renewal it wanted on roughly one tick in five
(≈119 per 600-tick run, measured before the protocol). Nothing about the organism's own state scales the
budget, so nothing equalizes outcomes, and the order has to choose.

## What is established, and what is not

**Established:** in a world where maintenance is unaffordable in full, an organism that can release its
stored six-position order and search again retains more population under a changed regime than one
structurally unable to overwrite its order — in every one of 12 individuals, against a pre-declared bar
derived from engineering, with the margin 16.6× the measurement noise.

**Not established — and deliberately not implied:**

- **Not self-sufficiency.** The organism does not fund its own maintenance; it is given an income. AC35
  tested self-funding and the endpoint there could not resolve orders at all. Nothing here says the
  organism sustains itself, and AC35's negative result stands.
- **Not survival.** No individual dies in these runs (the endpoint is population retained, and death is
  never reached). A binary alive/dead endpoint was rejected in AC34 as horizon-unstable.
- **Not optimality**, not a multi-regime claim, not retention under damage.
- **Nothing about experience, understanding or life**, and none of this is offered as evidence toward
  any of them. The measured quantity is sites retained under a cost.
- **The AC19 line's maintenance half** remains open.

## Provenance and verification

| file | value |
| --- | --- |
| rows | `ac36_results_v1/rows.jsonl` (72 rows) |
| pre-run snapshot | `ac36_results_v1/pre_run_snapshot.json` (6 sources, matching the declared list) |
| results + gates | `ac36_results_v1/results.json` |
| protocol | `AC36_PROTOCOL_v1.md` (final seeds 3500–3511, BAR 6.45, hashes) |
| engineering | prerequisite + arm sizing in `/tmp/ac36_optima.json`, `/tmp/ac36_engineering.json` |
| verification | `test_ac36.py` (18 tests), `audit_ac36.py` (provenance, recomputed gates, 2/2 determinism replay across processes) — not hashed, per AC17's rule |

The pre-flight check that AC32's drift taught and AC33 introduced runs here too: the runner parses the
protocol's `SOURCES (declared):` line and asserts it equals the set it hashes.

## Where the line stands

Two claims now pass in the six-position world, both with all eight gates: **AC33** (re-acquisition to
the new regime's level, ordering endpoint) and **AC36** (population retained under an insufficient
income, maintenance endpoint). Between them sit four recorded failures and stops — AC31 (design
falsified by engineering), AC32 (G2 failed by 0.25), AC34 (binary endpoint horizon-unstable), AC35
(prerequisite failed, spread 1.00 vs noise 0.30) — each of which narrowed the design rather than being
retried with a looser bar.

## The next step

The remaining untouched endpoints, in the order they now look tractable:

1. **Self-sufficiency**, the hard version: find an economy where the organism funds its own maintenance
   AND the endpoint still resolves orders. AC35 measured why the obvious version fails (production
   proportional to population equalizes outcomes); the fix would be a maintenance cost that does *not*
   scale with population while production does, or a population-independent overhead, so that being
   behind is punished without the feedback erasing all differences. Prerequisite first, as here.
2. **AC19's maintenance half** — the closure/propagation line's unshown direction — which has been open
   since AC19 and is untouched by everything since.

## Artifacts

`ac36_survival.py`, `AC36_PROTOCOL_v1.md`, `ac36_results_v1/`, `test_ac36.py`, `audit_ac36.py`.
Related: `AC35_ENGINEERING_v1.md` (the failed sibling), `AC34_ENGINEERING_v1.md` (the rejected
binary endpoint), `AC33_RESULTS_v1.md` (the ordering claim), `AC30_ACQUIRE_v1.md` (the generous-income
world).
