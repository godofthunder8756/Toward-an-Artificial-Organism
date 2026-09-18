# AC86 protocol v1: replacement of the information-bearing components (recipe succession)

STATUS: **frozen before the first final seed.** Written 2026-09-17 after the engineering result
(`AC86_ENGINEERING_v1.md`). Final seeds declared below, disjoint from every engineering seed and
prior frozen family.

REVISION v1.1 (disclosed, pre-freeze): the first final-seed run exposed a pointer-drift bug — the
generation pointer was originally stored in the program bank's dead rule (mask bits 6-7), where it
is damaged by the *program* stream (always on, even in the `damage=False` control) but repaired only
by action 2's whole-bank majority-restore (obs bit 2, `>=4` minority over 126 bits), far too slow
for a 2-bit pointer: a 4/7 flip gets cemented (AC61). The no-damage control seed 4019 drifted to
pointer=2 / desc=57, failing G6. The fix moves the pointer to **bank 1** (recipe storage, offset
312-313) so it is damaged by the recipe stream (which `damage` actually controls) and maintained by
its own minority-count trigger (`pointer_minority >= POINTER_TRIGGER`). This is a faithful
description of a bug-corrected design, not a gate or threshold change. The run was re-frozen on the
corrected code; the pre-correction run is discarded.

SOURCES (declared): ac86.py ac80.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC86_PROTOCOL_v1.md

## Claim

AC81 (milestone 2) established that the organism's physical components (W catalysts, C converters,
B boundary) are constructed, used and replaced across many turnover cycles, driven by the internally
retained recipe (the 78-bit description). It did **not** establish that the recipe-bearing storage
itself — the physical substrate carrying the 78 bits — is replaceable. That storage sits at a fixed
location (`traces[1,:78]`), is repaired in place by majority-restore, and is never moved.

This study establishes that the recipe storage is itself a replaceable component. The recipe lives
in `SLOTS=4` interchangeable storage slots in bank 1 (`traces[1, 78*g : 78*(g+1)]`), with a 2-bit
generation pointer stored **in bank 1** (the recipe storage, at a fixed offset after the four slots,
`traces[1, 312:314]`), majority-read. The pointer is recipe metadata — which slot holds the active
copy — so it belongs in the recipe bank: it is damaged by the recipe stream and maintained by the
recipe machinery (its own minority-count trigger), not by the program bank's action-2 repair. The
generic decode reads the ACTIVE slot (the one the pointer selects). The organism, on the recipe's
own degradation signal (the active slot's minority count reaching `DESC_TRIGGER`), rate-limited by
a declared cooldown, constructs a functional successor copy of the active slot in the next slot
(paid, W-catalyzed), verifies the successor decodes to a valid program, switches the pointer, and
only then removes (clears) the old slot. Provenance (generation index, start/copy/switch/remove
ticks, source/target slot, content correctness) is tracked per succession.

The succession is a **paid capability**, not a survival necessity: in-place majority-repair already
keeps the active recipe correct against the damage stream (AC80). The claim is that the storage is
replaceable and the replacement is performed by the organism's own paid machinery on its own
vulnerable state, with the ordering discipline "remove an older copy only after the successor is
functional" enforced and verified.

## The mechanism (declared changes from AC80)

1. **Replaceable storage + generation pointer.** The 78-bit description lives in 4 slots; a 2-bit
   pointer (bank 1, `traces[1, 312:314]`, majority-read) selects the active one. The generic decode
   (`rebuild_active`) reads the active slot; the description repair (`reg_description_active`)
   majority-restores the active slot; the pointer repair (`reg_pointer`) majority-restores the 2
   pointer bits on their own integrity trigger (`pointer_minority >= POINTER_TRIGGER`); the
   re-instantiation (`reg_from_active`) rebuilds the program from the active slot and excludes the
   register bits (dynamic decision state, not program content).

2. **Order-preserving generic decode (correction of AC80).** AC80's `build_program` produces
   `prog.program` order (five rule words then four bank rules), but the ACQUIRED program is
   `ac9_priority_v2`'s reorder — resource/production words 0-3, then the four bank rules, then the
   boundary word (mask 256) LAST. AC80's re-instantiation therefore reorders the bank on every fire
   (verified in engineering: the dead rule moves from index 4 to index 5). That reorder is harmless
   for AC80's always-zero register but fatal for any decision state whose offsets are resolved
   against the acquired layout (the AC12 register lives in the dead rule, and a reorder moves the
   register too). `rebuild_active` reproduces the ACQUIRED layout (words 0-3 verbatim, bank rules by
   the convention bank b -> (1, 4<<b, 2+b), word 4 last), so re-instantiation is order-preserving.
   It is verified bit-for-bit against the acquired program for every acquisition priority (unit
   test). Still format-only: no rule word value or permutation is hard-coded.

3. **Succession.** On the active slot's minority count reaching `DESC_TRIGGER` (the recipe's own
   degradation signal — with no damage it never fires), rate-limited by `SUCC_MIN_SPACING`, the
   organism: (a) copies the active slot's majority to the next slot (paid, W-catalyzed, spread over
   ticks by a per-tick write budget), (b) verifies the successor decodes to a valid permutation and
   matches the source, (c) writes the pointer to select the successor (paid), (d) clears the old
   slot (paid). A succession completes only when the copy is complete, verified, switched and
   removed — the ordering "remove after functional" is a mechanical invariant, asserted in the
   gates.

4. **In-place repair retained.** The active slot is majority-restored on the same trigger as AC80
   (obs bit 2 OR active-slot minority `>= DESC_TRIGGER`), so the recipe content stays correct while
   the organism lives, exactly as AC80. The pointer is additionally majority-restored on its own
   integrity trigger (`pointer_minority >= POINTER_TRIGGER`), because it is a 2-bit state damaged by
   the same recipe stream but too small to ride the program bank's action-2 repair (obs bit 2 needs
   `>=4` minority over all 126 program bits — a 2-bit pointer would reach a cemented majority flip
   first).

## World constants

`PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=16384`, `DEV=512`, `REGISTER_THRESHOLD=4`, sticky
program-bank damage (`|=`) at 1e-4 per replica per tick, sticky recipe-slot damage (`|=`) at 1e-4
per replica per tick from an independent stream (`rng1 = default_rng([seed,1609])`) applied to the
ACTIVE slot **and the 2 pointer bits** (both in bank 1). No route move, no program-corruption
intervention. `DESC_TRIGGER=2`, `POINTER_TRIGGER=2`, `SLOTS=4`, `SUCC_MIN_SPACING=2400`,
`SUCC_BUDGET=6` (max succession writes per tick).

## Arms

| arm | in-place repair | succession machinery | description damage |
| --- | --- | --- | --- |
| `succession` | yes | yes (real, paid) | yes |
| `repair` | yes | no | yes |
| `unmaintained` | no | no | yes |

`damage=True/False` turns the recipe damage stream on/off (this stream damages the active slot AND
the 2 pointer bits in bank 1). With `damage=False` every arm is inert (the recipe never degrades,
the pointer never degrades, the succession never fires), and `succession` must be byte-identical to
`repair` (state_hash equality). The `repair` arm is AC80's in-place-repair mechanism (no succession
machinery, pointer maintained at its acquired value 0) run through this runner's corrected
order-preserving decode.

## Endpoints (per individual)

`completed`, `first_dead`, `successions` (completed replacement cycles), `succession_log`
(per-cycle `start`/`copy_done`/`switch_tick`/`remove_tick`/`source`/`target`/`verified_valid`/
`target_correct`/`source_correct`), `pointer`, `description_correct` (active slot vs installed 78
bits), `description_valid`, `program_correct`, `W`, `C`, `energy`, `material`, `fuel`, `writes`,
`reg_writes`, `succ_writes`, `routes`, `demand`, `state_hash`.

## Prespecified gates (8 individuals per condition = 4 seeds x 2 histories)

Clean endpoints (succession provenance, description integrity) are gated on **survivors**
(`completed`): the paid maintenance stops at death and the AC68 W/C collapse kills maintained and
unmaintained alike (AC79/AC80). Survival is reported as a bimodality-aware lower bound, not gated
to an exact count.

- **G1 (succession occurs)** — every `succession` individual that completes the horizon has
  `successions >= 2`: at least two complete replacement cycles (construct successor, use it,
  replace it again).
- **G2 (successor functional)** — in every completing `succession` individual, every completed
  cycle has `verified_valid == 1` (the successor decodes to a valid permutation) **and**
  `target_correct == 1` (the successor's content equals the installed recipe), and the individual
  ends with `description_correct == 78` and `description_valid == 1`: each successor is a functional,
  correct copy.
- **G3 (remove after verify)** — in every completing `succession` individual, every completed cycle
  satisfies `remove_tick >= switch_tick >= copy_done >= start`: the old copy is removed only after
  the successor is functional.
- **G4 (recipe maintained)** — every completing `succession` and `repair` individual has
  `description_correct == 78` (the recipe content is preserved by the maintenance), and every
  `unmaintained` individual has `description_correct < 78` (without maintenance the recipe content
  degrades). This is the maintenance contrast; it does not gate survival (AC80 established that
  unmaintained dies under a program-corruption intervention; AC86 has no such intervention, so
  unmaintained's degraded description is simply never called upon and it may survive).
- **G5 (succession is the replacer)** — every `repair` and `unmaintained` individual has
  `successions == 0`, and every completing `succession` individual has `successions >= 2`: the
  replacement is performed by the succession machinery, not by in-place repair.
- **G6 (control clean)** — with `damage=False`, every arm has `successions == 0` and
  `description_correct == 78`, and `succession` is byte-identical to `repair` (per-individual
  `state_hash` equality): the mechanism is inert and introduces no spurious change.
- **G7 (completeness and determinism)** — 4 seeds x 2 histories x 3 arms x 2 damage conditions
  (48 rows) all present; re-running the first individual reproduces it exactly (`state_hash`
  included).

Thresholds are not moved; this protocol may not be edited after the first final seed.

## Boundary (stated up front)

The succession does not claim recovery from catastrophic corruption of the recipe content — the
successor is a copy of the active slot's majority, so a majority-flipped description bit would be
copied faithfully, exactly as AC80's majority-restore cements its own past-majority corruption
(AC61 one level down). The "destroy every usable copy" analog is out of scope (AC81). The generic
decode still derives the four bank rules from the permutation by the architectural convention
(AC80's residual (4), supplied machinery, not stored state). The succession machinery is supplied
format-level machinery (the copy/verify/switch/remove sequence); what is demonstrated is that the
recipe-bearing storage is replaceable and the replacement is paid, W-catalyzed and performed on
vulnerable state.

## Seeds

Finals: `4016, 4017, 4018, 4019` (4 seeds x 2 histories = 8 individuals per condition). Disjoint
from every frozen family (1000-3400, 5100-5507, 2600-2903, 3000-3003, 4000-4015) and from
engineering families 0-23. Engineering seeds (0-7) are excluded.

## Anti-drift rules

- The runner creates `ac86_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight:** the runner parses the `SOURCES (declared):` line and asserts it equals the hashed
  set, before the first final seed.
- `test_ac86.py`, `audit_ac86.py`, `replay_ac86.py` are **not** hashed (AC17's rule).
- If a gate fails, it fails.

## Source hashes (computed before the first final seed)

    (recorded in ac86_results_v1/pre_run_snapshot.json at freeze time)
