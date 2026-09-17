# AC80 protocol v1: internalize the reconstruction recipe (generic decode from a 78-bit description)

STATUS: **frozen before the first final seed.** Written 2026-09-17 after the engineering result
(`AC80_ENGINEERING_v1.md`, `ac80_engineering.py`). Final seeds declared below, disjoint from every
engineering seed and prior frozen family.

SOURCES (declared): ac80.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC80_PROTOCOL_v1.md

## Claim

The organism's complete description — the five rule words (5×14 = 70 bits) + the 8-bit permutation
= 78 bits — is stored in vulnerable, damage-streamed, paid-maintained state (`traces[1,:78]`,
7 replicas/bit), and the controller is re-instantiated during life by a **generic decode** that
reads that state by majority and rebuilds the 126-bit program, with `prog.program` removed from the
reconstruction path. The generic decode is bit-identical to `prog.program` for every acquisition
priority (unit test), so the internalized arm recovers the corrupted controller **as well as** the
pristine-description baseline, while the unmaintained-description control degrades and dies.

This establishes that the reconstruction *recipe* — the information that turns the description into
the controller — is internalized (stored + maintained + generically re-materialized), not merely
funded. It does **not** claim content self-production (AC78: the description's content is inherited
at acquisition, not produced by the organism).

## The mechanism (two declared changes from AC79)

1. **78-bit description + generic decode.** The description is the five rule words followed by the
   8-bit permutation (AC76's `encode_priority`). At acquisition it is installed as inherited content.
   During life, the re-instantiation calls `rebuild(o)` (generic) instead of `prog.program(priority)`:
   `rebuild` reads the 78 bits by majority, copies the five words verbatim, and derives the four bank
   rules from the permutation by the architectural convention bank b → (enabled=1, mask=4<<b,
   action=2+b). It knows only the format (14-bit word = enabled|mask<<1|action<<10, the 5-word +
   4-bank layout, majority read, paid write); no rule word value or permutation is known to it.
   `prog.program` is retained **only** in the observer (corruption setup and endpoint scoring).

2. **The description's own trigger.** AC79 rode the program's corruption signal (obs bit 2),
   conservative only because the program (126 bits) is 16× the 8-bit description. At 78 bits the
   program is only ~1.6× larger and, measured in engineering, obs bit 2 does **not** fire early
   enough for some individuals — a description WORD or PERM bit reaches a majority flip first,
   corrupting the controller. The description therefore has its own trigger: the re-instantiation
   fires on (obs bit 2) OR (the description's minority count `sum over bits of min(ones, 7-ones)`
   reaches `DESC_TRIGGER = 2`). This is the same integrity statistic obs bit 2 computes for the
   program, applied to the description's 78 bits; it is format-level, needs no new observation bit,
   and knows no policy.

The description maintenance is paid (same primitive, same per-action cap) and folded into the
corruption-triggered re-instantiation, exactly as AC79.

## World constants

`PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=16384`, `DEV=512`, `REGISTER_THRESHOLD=4`, sticky
program-bank damage (`|=`) at 1e-4 per replica per tick, sticky description damage (`|=`) at 1e-4
per replica per tick from an independent stream (`rng1 = default_rng([seed,1609])`). No route move.
`DESC_TRIGGER=2`.

## Arms

| arm | description in damage stream | description repaired | decode |
| --- | --- | --- | --- |
| `internalized` | yes | yes (paid, own trigger) | generic |
| `pristine` | no (hidden backup) | — | generic |
| `unmaintained` | yes | **no** | generic |
| `no_repair` | yes | no | loop cut (AC76 load-bearing control) |

Intervention: at t=8192, flip the majority (4 of 7 replicas) of program bits 0-7 to the opposite of
the correct value, leaving 3 replicas intact (the AC76 intervention). `pristine` holds the 78-bit
description never damaged, so its recovery is the built-in baseline isolating the description-
maintenance requirement; `internalized` must recover identically (per-individual `fw` equality).

## Endpoints (per individual)

`completed`, `first_dead`, `alive_at_corruption` (alive at t=8192), `program_correct`,
`flipped_still_wrong` (of the 8 flipped bits, how many still wrong at end), `description_correct`
(78-bit description bits matching the installed value), `description_word_correct` (first 70 bits =
the five words), `description_valid` (decoded permutation is a permutation), `description_same`
(decoded permutation == original priority), `W`, `C`, `energy`, `material`, `fuel`, `routes`,
`demand`, `register`, `state_hash`.

## Prespecified gates (8 individuals per condition = 4 seeds x 2 histories)

Gates G1, G2 and G5 are on clean endpoints (recovery + description integrity), not on survival
counts. Recovery and description integrity are gated on **survivors** (`completed`) only: the paid
description maintenance stops at death, and the AC68 W/C collapse kills `internalized` and
`pristine` alike, leaving a dying organism unable to fund the re-instantiation. Survival is
reported as a bimodality-aware lower bound, not gated to an exact count.

- **G1 (internalized recovers)** — every `internalized` individual that **completes the horizon**
  has `flipped_still_wrong == 0` **and** `description_correct == 78` (the full 78-bit description,
  including the five words, intact): the program's 8 corrupted bits are re-instantiated to correct
  by the generic decode, i.e. the internalized recipe is sufficient. (Non-vacuous by G3's
  at-least-one-survivor clause.)
- **G2 (unmaintained fails)** — every alive-at-t=8192 `unmaintained` individual has
  `flipped_still_wrong > 0` **and** `description_valid == 0` (decoded permutation is not a
  permutation) **and** `description_word_correct < 70` (the five rule words have degraded): the
  damaged, unmaintained description cannot be decoded to the correct program, i.e. the description
  maintenance is necessary.
- **G3 (maintenance load-bearing)** — every alive-at-t=8192 `unmaintained` individual dies after
  t=8192 (`first_dead` not None), **and** at least one alive-at-t=8192 `internalized` individual
  completes the horizon. The internalized survival count is reported as a lower bound, not gated.
- **G4 (no_repair dies)** — every `no_repair` individual dies (`completed` False): the loop cut is
  load-bearing (AC76 control).
- **G5 (control clean)** — with no corruption, every `internalized` and `pristine` individual has
  `flipped_still_wrong == 0`; every `pristine` individual has `description_same == 1` (its
  description is never damaged); and every `internalized` individual that **completes the horizon**
  has `description_same == 1`. The mechanism is inert and introduces no spurious change.
- **G6 (completeness and determinism)** — 4 seeds x 2 histories x 4 arms x 2 corruption conditions
  (64 rows) all present; re-running the first individual reproduces it exactly (`state_hash`
  included).

The equivalence `rebuild(o) == prog.program(priority)` for every acquisition priority is a **unit
test** (deterministic), not a run gate. The claim passes iff G1-G6 all pass. Thresholds are not
moved; this protocol may not be edited after the first final seed.

## Boundary (stated up front)

The description is the terminal, non-regenerable reference: majority-restore cements its own
past-majority corruption (AC61 one level down) — the "catastrophic destruction" analog already out
of scope. The generic decode knows the *format* but not the *policy*; if the description's word
content corrupts past the (widened) trigger's reach, the decode faithfully re-materializes the
wrong controller — that is the failure the trigger exists to prevent, not a hidden backup.

## Seeds

Finals: `4008, 4009, 4010, 4011` (4 seeds x 2 histories = 8 individuals per condition). Disjoint
from every frozen family (1000-3400, 5100-5507, 2600-2903, 3000-3003, 4000-4007) and from
engineering families 0-23 and 8500-8799. Engineering seeds (0-23) are excluded.

## Anti-drift rules

- The runner creates `ac80_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight:** the runner parses the `SOURCES (declared):` line and asserts it equals the hashed
  set, before the first final seed.
- `test_ac80.py`, `audit_ac80.py`, `replay_ac80.py` are **not** hashed (AC17's rule).
- If a gate fails, it fails.

## Source hashes (computed before the first final seed)

    (recorded in ac80_results_v1/pre_run_snapshot.json at freeze time)
