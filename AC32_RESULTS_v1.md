# AC32 RESULTS v1 — re-acquisition, re-engineered: 7 of 8 gates pass, G2 FAILS

2026-09-15. Frozen run: `ac32_results_v1/` (seeds **3300–3311**, 12 individuals, 6 arms, 72 rows).
Protocol frozen and hashed before the first final seed (`AC32_PROTOCOL_v1.md`, BAR = 12.00).
**Verdict: the claim's positive half is FALSIFIED as stated. Its negative half is established.**

## The gates

| id | gate | result |
| --- | --- | --- |
| G1 | `oracle_b` (scaffold ceiling) ≥ BAR | **PASS** (12.67) |
| G2 | `learner_both` **worst** ≥ BAR | **FAIL** — worst **11.75** < 12.00 |
| G3 | `no_release` **best** < BAR | **PASS** — best 11.00 |
| G4 | `oracle_a` best < BAR | **PASS** — 10.67 exactly |
| G5 | `no_search` / `preserve` **means** < BAR | **PASS** — 11.51 both |
| G6 | all arms complete | **PASS** |
| G7 | determinism spot check | **PASS** |
| G8 | register in the loop, read-back | **PASS** |

**Seven of eight. G2 fails by 0.25 sites.** No threshold is moved, and this study is not re-run with a
better-chosen bar.

## The measured arms (paired scoring, 12 shared seeds, regime B)

| arm | min | mean | max |
| --- | ---: | ---: | ---: |
| `learner_both` | **11.75** | 12.35 | 12.42 |
| `no_release` | 10.58 | 10.77 | **11.00** |
| `no_search` | 11.17 | 11.51 | 12.42 |
| `preserve` | 11.17 | 11.51 | 12.42 |
| `oracle_a` | 10.67 | 10.67 | 10.67 |
| `oracle_b` | 12.67 | 12.67 | 12.67 |

## What is established

1. **The negative half of the claim holds, and holds strictly.** `no_release` — structurally unable to
   overwrite its stored order — lands **below BAR in all 12 individuals** (max 11.00), as does
   `oracle_a` (exactly 10.67, the old optimum rated under the new regime). An organism that cannot
   release its stored order does not re-acquire. This is the AC16/AC18 shape, reproduced in a world
   that ranks orders with a **margin/noise ratio of 16.15**.
2. **The mechanism is real, just not reliable.** 11 of 12 `learner_both` individuals sat at
   12.33–12.42, i.e. within 0.25 of the scaffold ceiling of 12.67. One individual (3309) fell to
   **11.75**.
3. **The measurement fix worked.** AC31's unpaired design produced a mean *below* the arms it was
   meant to beat; with paired 12-seed scoring the ordering is clean and reproducible, and the one
   failure is a single individual rather than a comparison swamped by noise.

## What is NOT established

- **The claim as stated.** "Reliably re-acquires" was declared as *every individual at or above BAR*.
  One individual is below. That is a falsification of the declared claim, not a near-miss to be
  rounded.
- **Not survival-level, not optimality, not a both-regimes claim.** The endpoint is sites retained
  under regime B, averaged over scoring seeds, with the declared metabolic income that keeps the
  budget from binding so the score measures *ordering*. Nothing here is an autopoiesis, viability or
  optimality claim.
- **Nothing about experience, understanding or life**, and none of this is offered as evidence
  towards any of them.

## Diagnosis of the single failure

Individual 3309's search converged to an order rated 11.75 while its peers reached 12.33+. This is the
AC30 diagnosis again, attenuated but not eliminated: mutate-and-keep still has local optima it cannot
leave, and 4 restarts × 40 evaluations did not escape this one. The fix is a mechanism change —
restarts that diversify (rather than 4 independent climbs), a population, or an acceptance rule that
tolerates flat moves — and it must be engineered and declared in a **new** study, before its seeds.

## The disclosure that turned out to matter

The protocol recorded **in advance** that individual `no_search`/`preserve` runs could reach as high as
12.17 in engineering, so G5 was stated on the *mean* and no separation-of-minima claim was made for
those arms. In the finals one such individual reached **12.42 — above BAR**, the same as the best
`learner_both` individual. A single random order can be as good as a searched one in this world
(AC30 measured a random order at ≈88% of optimal). Had the protocol claimed "state-blind arms are
always below BAR", it would have been falsified too. Recording predictions in advance is what made
that visible instead of quietly survivable.

## Provenance

| file | value |
| --- | --- |
| rows | `ac32_results_v1/rows.jsonl` (72 rows) |
| pre-run snapshot | `ac32_results_v1/pre_run_snapshot.json` (5 sources) |
| results + gates | `ac32_results_v1/results.json` |
| verification | `test_ac32.py`, `audit_ac32.py`, `replay_ac32.py` — deliberately **not** hashed into the snapshot, so editing a verification tool cannot create a self-inflicted drift (AC17's lesson) |

## Protocol compliance — one discrepancy, recorded not repaired

The protocol declared a pre-run snapshot of **five** sources including `ac27_schedule.py`. The runner
hashed **four**: `ac32_reacquire.py`, `ac30_acquire.py`, `ac29_register.py`, `AC32_PROTOCOL_v1.md`.
`ac27_schedule.py` was omitted by the runner's `SOURCES` list.

- The omission is **not repaired**. `ac32_reacquire.py` is itself inside the hashed set, so editing it
  now would create exactly the self-inflicted drift the anti-drift rules exist to prevent. The
  protocol is also not edited after the fact.
- The gap is **harmless in substance and verified post hoc**: `ac27_schedule.py` hashes to
  `402ae74b6c60943dbe982048b502e531d9ef111b350c97e44d977e68addc1896`, unchanged since AC27 and
  imported only for its `all_pairs()` helper, which this study does not use in its endpoint.
- `test_ac32.py` asserts the discrepancy **as recorded** rather than asserting a tidy five, so it
  cannot silently become invisible.

**Process lesson for the next study:** run a pre-flight check that the runner's hash set equals the
protocol's declared hash set *before* the first final seed — the same kind of cheap consistency check
that AC15 used to pin its degenerate-arm hash. This is the third process finding in this line of the
same family as the AC17 hash-hygiene rule: verification infrastructure is the part of these studies
that most often disagrees with its own declaration.

## The next step

Two honest options, and they are not the same thing:

1. **A new study with a sharper mechanism**: better search (diversified restarts or a population) to
   remove the 1-in-12 failure, with its own protocol, its own declared seeds, and the same
   separation-of-minima gate. This tests the *mechanism* claim as stated.
2. **A new, weaker claim, declared as such**: "the capable arm's *mean* reaches the ceiling and its
   worst exceeds the incapable arms' best" — an aggregate claim with its own gate. Legitimate only as
   a **new** pre-declared claim; it must never be presented as AC32's result, and AC32 remains
   falsified as written.

## Artifacts

`ac32_reacquire.py`, `AC32_PROTOCOL_v1.md`, `ac32_results_v1/`, `test_ac32.py`, `audit_ac32.py`,
`replay_ac32.py`. Related: `AC31_ENGINEERING_v1.md` (the falsified predecessor), `AC30_ACQUIRE_v1.md`
(the world and the single-seed diagnosis), `AC18_PROTOCOL_v1.md` (the gate shape).
