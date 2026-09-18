# AC87 protocol v1: the integrated successor -- full stored description + recipe succession, with the succession controller's working state under maintenance

STATUS: **frozen before the first final seed.** Written 2026-09-18 after the engineering result
(`ac87.py` engineering seeds 0-7). Final seeds declared below, disjoint from every engineering seed
and prior frozen family.

SOURCES (declared): ac87.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC87_PROTOCOL_v1.md

## Claim

AC85 internalized the bank-rule convention (130-bit description: five rule words + 8-bit permutation
+ four bank-rule masks + four bank-rule actions, read not derived). AC86 made the recipe-bearing
storage a replaceable component (SLOTS interchangeable slots + a generation pointer), but it copied
the OLDER 78-bit description (bank rules still synthesized externally) and its succession coordinator
held `phase/source/target/active/timing` as Python fields that never undergo the damage+maintenance
applied to the recipe and pointer.

This study builds ONE integrated successor: the complete 130-bit description lives in interchangeable
slots selected by a generation pointer, and the succession coordinator's persistent working state
(active / phase / last-start) lives in the SAME vulnerable, damage-streamed, paid-maintained substrate
as the recipe and pointer. The coordinator's source/target are not stored -- they are derived from the
generation pointer, which is itself vulnerable and maintained. Both the source and the successor
storage are exposed to the declared damage model (not only the active slot), and the verify step is a
REAL gate: the pointer switches only after the successor decodes to a syntactically valid program AND
matches the source. The generic decode is made generic over SYNTAX: a stored mask/action that is
syntactically valid but not the designer's convention decodes faithfully to a working, possibly worse
program -- it is not rejected by an external correctness rule `m == (4<<b) and a == (2+b)`. The decode
is order-preserving throughout (the acquired ac9_priority_v2 layout).

The combined architecture (reconstruction + description maintenance + route-move adaptation) is
re-tested with the corrected order-preserving decoder, on AC83's corrupt-then-move schedule.

This is an internalization claim: the recipe (including the bank-rule content) is stored in, and
replaced through, vulnerable paid-maintained machinery whose own working state is in that same
substrate. It is not a content self-production claim (AC78) and not a better-controller claim.

## The mechanism (declared changes from AC85/AC86)

1. **Full stored description + replaceable storage.** The 130-bit description (AC85's layout: five
   rule words at bits 0-69, the 8-bit permutation at 70-77, four bank-rule masks at 78-113, four
   bank-rule actions at 114-129) lives in `SLOTS=4` interchangeable slots in bank 1
   (`traces[1, 130*g : 130*(g+1)]`). A 2-bit generation pointer (`traces[1, 520:522]`, majority-read)
   selects the active slot. The successor copies the FULL 130 bits including the bank-rule content.

2. **Succession controller state in the maintained substrate.** The coordinator's persistent working
   state is an 18-bit word in bank 1 (`traces[1, 522:540]`): ACTIVE (1 bit), PHASE (3 bits: idle /
   copy / verify / switch / remove), LAST_START (14 bits, the tick the current succession began). It
   is damaged by the same recipe stream and majority-maintained by `reg_ctrl` on its own minority
   trigger (`CTRL_TRIGGER`), exactly as the pointer. source/target are NOT stored: source = the
   active slot (read_pointer) during copy/verify/switch, the slot to clear during remove is
   (pointer-1)%SLOTS, and target = (pointer+1)%SLOTS -- so the coordination is embodied in the
   maintained pointer + slots.

3. **Both source and successor exposed to damage; verify is a real gate.** The recipe stream damages
   the ACTIVE slot AND the successor (target) slot (plus the pointer and controller state), so the
   copy itself can be hit. The verify phase is a real gate: the pointer switches only after the
   successor decodes to a syntactically valid program AND matches the source; a switch phase re-checks
   both and falls back to copy on any mismatch.

4. **Generic-over-syntax, order-preserving decode.** `build_program` copies the five words verbatim,
   reads the four bank rules' masks/actions from state, and places the boundary word last (the
   acquired layout). The only validity check is syntactic: the stored permutation must be a
   permutation. A stored mask/action that is syntactically valid but not `4<<b` / `2+b` decodes
   faithfully (never rejected by an external correctness rule). `rebuild == acquired` bit-for-bit for
   every acquisition priority (unit test); `prog.program` survives only in the observer.

5. **Erase-on-relinquish (AC75) + the corrected `_restore` (AC82).** The two-way outcome-driven
   allocation with erase-on-relinquish (the drop also clears the stale entry), and `_restore` fires
   only when the slot actually reads as relinquished (majority >= `REGISTER_THRESHOLD`), not on any
   set replica.

## World constants

`PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=16384`, `DEV=512`, `REGISTER_THRESHOLD=4`, sticky
program-bank damage (`|=`) at 1e-4 per replica per tick (stream `rng=[seed,1509]`), sticky recipe
damage (`|=`) at 1e-4 per replica per tick from an independent stream (`rng1=[seed,1609]`) applied to
the ACTIVE slot, the successor slot, the 2 pointer bits and the 18 controller-state bits (all in bank
1). `DESC_TRIGGER=2`, `POINTER_TRIGGER=2`, `CTRL_TRIGGER=2`, `SLOTS=4`, `SUCC_MIN_SPACING=2400`,
`SUCC_BUDGET=6` (max succession slot-writes per tick; the controller-state word is written atomically,
bounded by 22x7=... 18x7=126 replicas). Interventions: program rule 0 (bits 0-7) majority-flipped to
the wrong value at `CORRUPT_TICK=8192`; channel 1 permanently relabelled at `MOVE_TICK=12288`
(corrupt-then-move, AC83 schedule A).

## Arms

All arms use erase-on-relinquish and the generic order-preserving decode.

| arm | in-place repair (desc+pointer) | controller-state maintenance | succession | re-instantiation (regen) | loop |
| --- | --- | --- | --- | --- | --- |
| `succession` | yes | yes | yes (real) | yes | closed |
| `repair` | yes | yes | no | yes | closed |
| `ctrl_unmaintained` | yes | **no** | yes (real) | yes | closed |
| `unmaintained` | no | no | no | yes | closed |
| `no_repair` | no | no | no | no | **cut** (no_policy_write) |

`damage=True/False` turns the recipe+pointer+controller damage stream on/off (no-damage control: the
mechanism is inert). `corrupt=True` flips rule 0 at t=8192. `transition='perm'` relabels channel 1 at
t=12288; `'none'` leaves it unchanged.

## Endpoints (per individual)

`completed`, `first_dead`, `alive_at_corruption`, `alive_at_move`, `successions` (completed cycles),
`succession_log` (per-cycle `start`/`copy_done`/`switch_tick`/`remove_tick`/`source`/`target`/
`verified_valid`/`target_correct`/`source_correct`), `pointer`, `ctrl` (final active/phase/last),
`ctrl_idle_end`, `ctrl_minority_end`, `description_correct` (active slot vs installed 130 bits),
`description_valid`, `description_same`, `program_correct`, `flipped_still_wrong`, `W`, `C`, `energy`,
`material`, `fuel`, `writes`, `reg_writes`, `succ_writes`, `ctrl_writes`, `routes`, `route1_correct`,
`demand`, `register`, `relinquishments`, `restorations`, `state_hash`.

## Prespecified gates (8 individuals per condition = 4 seeds x 2 histories)

Clean endpoints (succession provenance, description integrity, controller-state cleanliness) are gated
on **survivors** (`completed`): the paid maintenance stops at death and the AC68 W/C collapse kills
maintained and unmaintained alike (AC79/AC80/AC85). Survival is reported as a bimodality-aware lower
bound, not gated to an exact count.

- **G1 (succession occurs)** -- every `succession` individual that completes the horizon has
  `successions >= 2`.
- **G2 (successor functional, full description)** -- every completing `succession` individual has
  `successions >= 2`, every completed cycle has `verified_valid == 1` (syntactically valid) and
  `target_correct == 1` (equals the installed 130-bit description, bank-rule content included), and
  the individual ends `description_correct == 130` and `description_valid == 1`.
- **G3 (remove after verify)** -- every completed cycle satisfies
  `remove_tick >= switch_tick >= copy_done >= start`.
- **G4 (recipe maintained)** -- every completing `succession` and `repair` individual has
  `description_correct == 130`; every `unmaintained` individual (damage on) has
  `description_correct < 130`.
- **G5 (succession is the replacer)** -- `repair` and `unmaintained` have `successions == 0`; every
  completing `succession` individual has `successions >= 2`.
- **G6 (controller state in the maintained substrate)** -- every completing `succession` individual
  ends `ctrl_idle_end == 1` (the machinery returned to idle) and `ctrl_minority_end <= 1` (the state
  is clean); every `ctrl_unmaintained` individual (maintenance cut, damage on) ends
  `ctrl_minority_end >= 4` (the state is degraded). This is the maintenance contrast: without
  `reg_ctrl` the coordinator's own state degrades.
- **G7 (control clean)** -- with `damage=False`, `succession` and `repair` both have
  `successions == 0` and `description_correct == 130`, and `succession` is byte-identical to `repair`
  (per-individual `state_hash` equality): the mechanism is inert.
- **G8 (composition)** -- under `corrupt=True` + `transition='perm'`, every `succession` individual
  that completes has `flipped_still_wrong == 0` and `description_correct == 130` (reconstruction +
  description maintenance), every `unmaintained` individual dies, every `no_repair` individual dies,
  and at least one `succession` individual completes (non-vacuity). Route-holding under the move is
  reported as a lower bound, not gated (AC83: it is seed/priority-dependent, AC68's renewal
  contention).
- **G9 (completeness and determinism)** -- 4 seeds x 2 histories x 5 arms x 2 damage x 2 corrupt x 2
  transition (320 rows) all present; re-running the first individual reproduces it exactly
  (`state_hash` included).

The equivalences `build_program == acquired` for every acquisition priority, the generic-over-syntax
property (a flipped stored mask/action decodes faithfully), and the read-not-derive property are
**unit tests** (deterministic), not run gates. The claim passes iff G1-G9 all pass. Thresholds are not
moved; this protocol may not be edited after the first final seed.

## Boundary (stated up front)

The succession does not claim recovery from catastrophic recipe-content corruption: a successor is a
copy of the active slot's majority, so a majority-flipped description bit would be copied faithfully
(AC61 one level down). The four bank rules are still four bank rules; what is internalized is their
mask/action content (storage + maintenance + replacement), not the fact that four bank rules exist
(format). The succession state machine (copy -> verify -> switch -> remove) is supplied format-level
machinery operating on vulnerable values, exactly as `prog.choose` is the interpreter for the program
bank. No content self-production (AC78 blocked). The controller-state maintenance keeps the
coordinator's state clean, but because source/target are derived from the pointer and the machinery's
own transitions overwrite active/phase/last, the succession is robust to controller-state degradation
(a reported robustness finding, not a survival claim).

## Seeds

Finals: `4028, 4029, 4030, 4031` (4 seeds x 2 histories = 8 individuals per condition). Disjoint from
every frozen family (1000-3400, 5100-5507, 2600-2903, 3000-3003, 4000-4027) and from engineering
families 0-23. Engineering seeds (0-7) are excluded.

## Anti-drift rules

- The runner creates `ac87_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight:** the runner parses the `SOURCES (declared):` line and asserts it equals the hashed
  set, before the first final seed.
- `test_ac87.py`, `audit_ac87.py`, `replay_ac87.py` are **not** hashed (AC17's rule).
- If a gate fails, it fails.

## Source hashes (computed before the first final seed)

    (recorded in ac87_results_v1/pre_run_snapshot.json at freeze time)
