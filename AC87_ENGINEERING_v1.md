# AC87 engineering v1: the integrated successor — all nine gates pass on engineering seeds

2026-09-18. Engineering only — no protocol freeze, no final seeds, no claim. `ac87.py` (seeds 0-7,
16,384 ticks, 640 rows). Supersedes an earlier 2026-09-17 engineering attempt
(`AC87_ENGINEERING_v1_PRIOR-20260917.md`, `ac87_engineering_v1_prior-20260917/`) that used a
122-bit no-permutation description, no composition, and a different runner; that attempt is preserved
as a record, not built upon.

## What was measured

The AC85/AC86 review left one decisive step, and this card combines it with the AC82/AC83 composition.
Five capabilities in one architecture:

1. **Full stored description + recipe succession.** AC85's complete 130-bit description (five rule
   words + 8-bit permutation + four bank-rule masks + four bank-rule actions) lives in `SLOTS=4`
   interchangeable slots selected by a 2-bit generation pointer. The successor copies the FULL 130
   bits, bank-rule content included.
2. **Succession controller state in the maintained substrate.** The coordinator's persistent working
   state (active / phase / last-start, 18 bits) lives in bank 1, damaged by the recipe stream and
   majority-maintained (`reg_ctrl`) on its own trigger. source/target are derived from the pointer
   (not stored), so the coordination is embodied in the maintained pointer + slots.
3. **Both source and successor exposed to damage; verify is a real gate.** The recipe stream damages
   the ACTIVE slot AND the successor slot (plus pointer and controller state); the pointer switches
   only after the successor decodes to a syntactically valid program AND matches the source.
4. **Generic-over-syntax, order-preserving decode.** `build_program` copies the words verbatim and
   READS the bank-rule masks/actions from state; the only syntax check is "the permutation is a
   permutation". A stored mask/action that is syntactically valid but not `4<<b`/`2+b` decodes
   faithfully. `build_program == acquired` bit-for-bit for every acquisition priority.
5. **Composition.** reconstruction (corruption at t=8192) + description maintenance + route-move
   adaptation (permanent move of channel 1 at t=12288), with the order-preserving decoder throughout.

## Findings

1. **`build_program == acquired` for 12/12 priorities** (unit test), and the decode is generic over
   syntax: flipping a stored mask to another syntactically valid value (e.g. 8 instead of `4<<b`) is
   followed faithfully — the rebuilt program carries the new mask, not the convention — and is never
   rejected by an external correctness rule.

2. **Succession works with the internalized state, all four slots cycled.** Every `succession`
   individual (16/16 survive) performs 6-7 complete cycles (pointer 0→1→2→3→0→1→2), each cycle
   `verified_valid == 1` and `target_correct == 1` (the full 130-bit description), with
   `remove_tick >= switch_tick >= copy_done >= start`. The internalized controller state ends idle
   (`ctrl_idle_end == 1`) with `ctrl_minority_end` 0-1: the 18 state bits were damaged and repaired
   without ever cementing a wrong majority.

3. **The controller state is genuinely vulnerable.** In `ctrl_unmaintained` (desc+pointer repaired,
   controller state NOT), the state degrades to `ctrl_minority_end` 4-30 (vs 0-1 maintained) and the
   succession count becomes erratic (0-9 vs 6-7) — on seed 5 the machinery stalls at 0 successions.
   The maintenance is what keeps the coordinator's own state clean. (The organism survives either way,
   because source/target are derived from the maintained pointer and in-place repair keeps the recipe.)

4. **Recipe maintained, contrast categorical.** `succession` and `repair` keep 130/130; `unmaintained`
   degrades to 36-95/130 and dies 14/16 (2 survive with a degraded, uncalled-upon description — AC86's
   finding 3: without a corruption intervention the degraded description is simply never called upon).

5. **The composition works — and route-holding is now clean.** Under perm+corrupt, `succession`
   survives 16/16, reconstructs (`fw=0`) and maintains the description (130/130) in all 16, and holds
   BOTH routes 16/16; `unmaintained` dies 0/16 and `no_repair` dies 0/16 (deaths 366-1050). `repair`
   (no succession) survives 14/16 (seed 0 collapses at 12540 — the AC68 W/C bimodality, reported as a
   lower bound). AC83's route-holding failure (seed 4 losing both routes under the move) does not
   recur on engineering seeds with the order-preserving decoder + succession machinery.

## Recovery table (engineering, seeds 0-7, 16,384 ticks)

| arm | survive | successions | description | controller state | first_dead |
| --- | --- | --- | --- | --- | --- |
| `succession` | 16/16 | 6-7 | 130/130 | idle, minority 0-1 | — |
| `repair` | 16/16 | 0 | 130/130 | maintained at idle | — |
| `ctrl_unmaintained` | 16/16 | 0-9 (erratic) | 130/130 | minority 4-30 | — |
| `unmaintained` | 2/16 | 0 | 36-95/130 | degraded | 857-3179 |
| `no_repair` | 0/16 | 0 | 36-95/130 | degraded | 366-1050 |

Composition (perm + corrupt): `succession` 16/16 survive, fw=0 + desc=130 in 16/16, hold both routes
16/16; `repair` 14/16 (deaths 12540); `unmaintained` 0/16; `no_repair` 0/16.

Writes: `succession` total ~20,005-20,681, of which `succ_writes` ~2,674-3,135 and `ctrl_writes`
~719-856 (the extra cost over AC86 is the 130-bit copy, the all-slots+successor damage, and the
controller-state maintenance). The no-damage control is byte-identical across `succession`==`repair`
(0 successions, 130/130, per-individual `state_hash` equality).

## Conclusion carried into the protocol

The replacement machinery's persistent coordination state is stored, damaged and maintained; the
complete description (including bank-rule content) is replaced through it; the decoder is generic over
syntax and order-preserving; the verify step is a real gate; and the combined architecture
(reconstruction + description maintenance + route-move adaptation) holds routes with the corrected
decoder. All nine gates pass on engineering seeds. Finals on disjoint seeds 4028-4031.
