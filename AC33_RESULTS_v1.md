# AC33 RESULTS v1 — re-acquisition with a steepest-ascent search: ALL EIGHT GATES PASS

2026-09-15. Frozen run: `ac33_results_v1/` (seeds **3400–3411**, 12 individuals, 6 arms, 72 rows).
Protocol frozen and hashed before the first final seed (`AC33_PROTOCOL_v1.md`, BAR = 12.00, unchanged
from AC32). **Verdict: the claim is established.**

## The gates

| id | gate | result |
| --- | --- | --- |
| G1 | `oracle_b` (scaffold ceiling) ≥ BAR | **PASS** (12.67) |
| G2 | `learner_both` **worst** ≥ BAR | **PASS** — worst **12.33** |
| G3 | `no_release` **best** < BAR | **PASS** — best 11.25 |
| G4 | `oracle_a` best < BAR | **PASS** — 10.67 exactly |
| G5 | state-blind **means** < BAR | **PASS** — 11.38 both |
| G6 | all arms complete | **PASS** |
| G7 | determinism | **PASS** |
| G8 | register in the loop | **PASS** |

## The measured arms (paired 12-seed scoring, regime B)

| arm | min | mean | max |
| --- | ---: | ---: | ---: |
| `learner_both` | **12.33** | 12.55 | **12.67** |
| `no_release` | 9.83 | 10.64 | **11.25** |
| `no_search` | 10.33 | 11.38 | 12.33 |
| `preserve` | 10.33 | 11.38 | 12.33 |
| `oracle_a` | 10.67 | 10.67 | 10.67 |
| `oracle_b` | 12.67 | 12.67 | 12.67 |

The capable arm's **worst** individual (12.33) is above the incapable arm's **best** (11.25) — a
strict, gap-separated result in the claim's own shape, with the capable arm reaching the scaffold
ceiling exactly (12.67) somewhere in the run.

## What the mechanism change bought, and what it cost

AC32's G2 failed at 11.75. AC33's is 12.33 — and 12.33 is *not* a lucky number: it is exactly the worst
local optimum that `ac33_search.py` measured before this protocol existed (24 starts, both
neighbourhoods, min 12.33). The prediction and the outcome agree, which is the strongest form the
mechanism evidence could have taken.

The replacement of random-single-swap hill climbing by **steepest ascent over all 15 swaps** was also
*cheaper*: ~36 rating calls per acquisition against AC32's ~160. A richer neighbourhood (insertions and
reversals) bought almost nothing (mean 12.62 → 12.65) and was not adopted, keeping the mechanism as
simple as it can be.

## What is established, and what is not

**Established:** in a world measured to rank orders with **margin/noise 16.15**, an organism that can
release its stored six-position order and search again re-acquires the new regime's level under
**every one of 12 individuals**, while an organism structurally unable to overwrite its stored order
stays below the bar in **every one of 12** (max 11.25). Acquisition, retention and re-acquisition now
have a passing claim in the same world.

**Not established — and deliberately not implied:**

- **Not survival-level.** The declared metabolic income keeps the budget from binding so the endpoint
  measures *ordering*. This is not an autopoiesis, viability or self-maintenance claim.
- **Not optimality.** The learner reaches one-swap local optima, some below the 12.67 ceiling.
- **Not a both-regimes or multi-regime claim**, and nothing about regimes beyond this A/B pair.
- **Not a retention claim under damage.** The register is in the loop but no damage is applied; that
  question belongs to AC29/AC30.
- **Nothing about experience, understanding or life**, and none of this is offered as evidence toward
  any of them. The measured quantities are sites retained and distinguishable rule orders.
- **The other open endpoint** — random-fallback survival — is untouched. This study aimed at
  re-acquisition.

## The pre-flight check, and why it exists

AC32 declared five hashed sources and hashed four. AC33 enforces the equality **in code**: the runner
parses the `SOURCES (declared):` line out of the protocol and asserts it equals the set it hashes,
before the first final seed. The check is tested, not merely asserted — `test_ac33.py` feeds it a
doctored protocol that omits a source and a doctored protocol that adds one, and requires both to be
rejected. The audit independently re-derives the same equality for the frozen run, and it holds
(6 declared, 6 hashed, all unchanged).

## Provenance

| file | value |
| --- | --- |
| rows | `ac33_results_v1/rows.jsonl` (72 rows) |
| pre-run snapshot | `ac33_results_v1/pre_run_snapshot.json` (6 sources, matching the declared list) |
| results + gates | `ac33_results_v1/results.json` |
| protocol | `AC33_PROTOCOL_v1.md` |
| mechanism engineering | `ac33_search.py` (`/tmp/ac33_landscape.json`) |
| verification | `test_ac33.py` (16 tests), `audit_ac33.py`, `replay_ac33.py` (2/2 exact) — not hashed, per AC17's rule |

Full suite: **294 tests**, all passing.

## Where the line stands after AC29–AC33

A developmental function of **9.49 effective bits** — a six-position order, not the frozen world's
1.00 — that is measured to be learnable (AC25/AC26/AC27), stored in a replicated register whose
integrity behaviour is quantified (AC29), acquired by a search in a world that ranks orders
(AC30), and **re-acquired when the world's demands change** (AC33, all gates passing, after AC31's
engineering falsification and AC32's single failing gate).

## The next step

The untouched open endpoint: **random-fallback survival** — whether the organism holds site
populations *without* the declared metabolic income, so that the endpoint stops being a measure of
ordering and starts being a measure of maintenance. That is a world and protocol change of its own: it
needs a declared income schedule (or none), a survival criterion stated before the fact, and the same
separation-of-minima discipline for whatever it claims. Alongside it, the AC19 line's unshown
maintenance half remains open.

## Artifacts

`ac33_reacquire.py`, `ac33_search.py`, `AC33_PROTOCOL_v1.md`, `ac33_results_v1/`, `test_ac33.py`,
`audit_ac33.py`, `replay_ac33.py`. Related: `AC32_RESULTS_v1.md` (the falsified predecessor),
`AC31_ENGINEERING_v1.md`, `AC30_ACQUIRE_v1.md`, `AC29_REGISTER_v1.md`, `AC18_PROTOCOL_v1.md`.
