# AC85 protocol v1: internalize the bank-rule convention (the last supplied machinery on the reconstruction path)

STATUS: **frozen before the first final seed.** Written 2026-09-17 after the engineering result
(`AC85_ENGINEERING_v1.md`, `ac85.py` engineering seeds 0-7). Final seeds declared below, disjoint
from every engineering seed and prior frozen family.

SOURCES (declared): ac85.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC85_PROTOCOL_v1.md

## Claim

AC80 internalized the reconstruction recipe — the five rule words + 8-bit permutation (78 bits) live
in vulnerable, damage-streamed, paid-maintained state, and a generic decode `rebuild` re-materializes
the 126-bit controller, `rebuild == prog.program` bit-for-bit. Its recorded residual: `rebuild` still
DERIVES the four bank rules from the permutation by the architectural convention
bank b -> (enabled=1, mask=4<<b, action=2+b). That convention is supplied machinery, not stored
state.

This study removes that residual. The bank rules' masks and actions are stored as vulnerable,
damage-streamed, paid-maintained state alongside the words and permutation, and `rebuild` READS them
instead of deriving them. No function on the reconstruction path computes a mask or an action from a
bank index. The internalized arm must therefore recover the corrupted controller **as well as** the
pristine-description baseline (per-individual `fw` equality), while the unmaintained-description
control degrades and dies — exactly AC80's contrast, now with the bank-rule convention itself inside
the vulnerable state.

This is a claim about the **internalization of the reconstruction machinery**, not about content
self-production (AC78: the description's content is inherited at acquisition, not produced by the
organism).

## The mechanism (the declared change from AC80)

**130-bit description + read-the-convention decode.** The description is the five rule words
(70 bits), then the 8-bit permutation (AC76's `encode_priority`), then the four bank-rule masks
(9 bits each, in priority order), then the four bank-rule actions (4 bits each, in priority order)
= 130 bits. At acquisition it is installed as inherited content. During life, the re-instantiation
calls `rebuild(o)`, which reads the 130 bits by majority, copies the five words verbatim, and READS
the four bank rules' masks/actions from the stored state — it never applies the bank-b convention.
It knows only the format (14-bit word = enabled | mask<<1 | action<<10, the 5-word + 4-bank +
boundary layout, majority read, paid write). A degraded description decodes to `None` (invalid
permutation, or a stored mask/action inconsistent with the permutation); it is never silently
re-materialized into a wrong-but-valid controller. `prog.program` is retained **only** in the
observer (corruption setup and the cross-check that the stored content equals the convention for the
acquisition priority).

**Order-preserving (AC86's correction carried forward).** The generic decode reproduces the ACQUIRED
program (`ac9_priority_v2`'s reorder — resource words 0-3, then the four bank rules, then the
boundary word mask 256 LAST), not `prog.program` order, so re-instantiation does not move the dead
rule or the register. AC80's `build_program` produced `prog.program` order, harmless only because its
register was always zero; this runner reproduces the acquired layout (verified bit-for-bit against
the acquired program for every acquisition priority, unit test).

The description maintenance is paid (same primitive, same per-action cap) and folded into the
corruption-triggered re-instantiation, exactly as AC80. The description's own trigger is retained:
the re-instantiation fires on (obs bit 2) OR (the description's minority count
`sum over bits of min(ones, 7-ones)` reaching `DESC_TRIGGER = 2`). At 130 bits the description is
slightly larger than the program (126 bits), so it certainly cannot ride obs bit 2 (AC80's finding at
78 bits applies a fortiori).

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
the correct value, leaving 3 replicas intact (the AC76 intervention). `pristine` holds the 130-bit
description never damaged, so its recovery is the built-in baseline isolating the description-
maintenance requirement; `internalized` must recover identically (per-individual `fw` equality).

## Endpoints (per individual)

`completed`, `first_dead`, `alive_at_corruption` (alive at t=8192), `program_correct`,
`flipped_still_wrong` (of the 8 flipped bits, how many still wrong at end), `description_correct`
(130-bit description bits matching the installed value), `description_word_correct` (first 70 bits =
the five words), `description_perm_correct` (the 8 permutation bits), `description_bank_correct`
(the 52 bank-rule mask+action bits), `description_valid` (decoded permutation is a permutation),
`description_same` (decoded permutation == original priority), `bank_masks`, `bank_actions`, `W`,
`C`, `energy`, `material`, `fuel`, `routes`, `demand`, `register`, `state_hash`.

## Prespecified gates (8 individuals per condition = 4 seeds x 2 histories)

Gates G1, G2 and G5 are on clean endpoints (recovery + description integrity), not on survival
counts. Recovery and description integrity are gated on **survivors** (`completed`) only: the paid
description maintenance stops at death, and the AC68 W/C collapse kills `internalized` and
`pristine` alike. Survival is reported as a bimodality-aware lower bound, not gated to an exact
count.

- **G1 (internalized recovers)** — every `internalized` individual that **completes the horizon**
  has `flipped_still_wrong == 0` **and** `description_correct == 130` (the full description,
  including the words, permutation and bank-rule masks/actions, intact): the program's 8 corrupted
  bits are re-instantiated to correct by the generic decode. (Non-vacuous by G3's at-least-one-
  survivor clause.)
- **G2 (unmaintained fails)** — every alive-at-t=8192 `unmaintained` individual has
  `flipped_still_wrong > 0` **and** `description_valid == 0` (decoded permutation is not a
  permutation) **and** `description_word_correct < 70` (the five rule words have degraded): the
  damaged, unmaintained description cannot be decoded to the correct program.
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

The equivalences `rebuild(o) == acquired` for every acquisition priority and `rebuild` reading (not
deriving) the bank rules are **unit tests** (deterministic), not run gates. The claim passes iff
G1-G6 all pass. Thresholds are not moved; this protocol may not be edited after the first final seed.

## Boundary (stated up front)

The description is the terminal, non-regenerable reference: majority-restore cements its own
past-majority corruption (AC61 one level down) — the "catastrophic destruction" analog already out
of scope. The stored masks/actions materialize the bank-rule convention for the ACQUIRED priority;
the generic decode knows the format but not the policy, and if the description's content corrupts
past the trigger's reach, the decode refuses (invalid permutation or inconsistent mask/action) or
faithfully re-materializes a wrong-but-consistent controller — that is the failure the trigger exists
to prevent, not a hidden backup. The masks/actions are still constrained to be the four bank values;
what is now internalized is their storage and maintenance, not the fact that four bank rules exist
(format).

## Seeds

Finals: `4024, 4025, 4026, 4027` (4 seeds x 2 histories = 8 individuals per condition). Disjoint
from every frozen family (1000-3400, 5100-5507, 2600-2903, 3000-3003, 4000-4023) and from
engineering families 0-23 and 8500-8799. Engineering seeds (0-7) are excluded.

## Anti-drift rules

- The runner creates `ac85_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight:** the runner parses the `SOURCES (declared):` line and asserts it equals the hashed
  set, before the first final seed.
- `test_ac85.py`, `audit_ac85.py`, `replay_ac85.py` are **not** hashed (AC17's rule).
- If a gate fails, it fails.

## Source hashes (computed before the first final seed)

    (recorded in ac85_results_v1/pre_run_snapshot.json at freeze time)
