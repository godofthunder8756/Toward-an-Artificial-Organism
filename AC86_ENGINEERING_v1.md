# AC86 engineering v1: recipe succession — the storage is replaceable, and the fix is order-preserving rebuild

2026-09-17. Engineering only — no protocol freeze, no final seeds, no claim. `ac86.py` (final
design), plus throwaway diagnostics (`ac86_probe*.py`, `ac86_diag_*.py`, `ac86_sweep*.py`).

POST-ENGINEERING CORRECTION (recorded for the record): the first final-seed run exposed a
pointer-drift bug. The generation pointer was originally stored in the program bank's dead rule
(mask bits 6-7); there it is damaged by the *program* stream (which runs even in the no-damage
control) but repaired only by action 2's whole-bank majority-restore (obs bit 2), too slow for a
2-bit pointer, so a 4/7 flip got cemented. The fix moves the pointer to bank 1 (recipe storage,
offset 312-313), damaged by the recipe stream and maintained by its own minority-count trigger.
This document is the pre-fix engineering record; the frozen design and results are in
`AC86_PROTOCOL_v1.md` (rev 1.1) and `AC86_RESULTS_v1.md`.

## What the card requires

AC81 (milestone 2) showed the organism repeatedly replaces its physical components (W/C/B) but
never the recipe-bearing storage itself — the 78-bit description in `traces[1,:78]` is repaired in
place and never moves. AC86 makes that storage a replaceable component: the organism constructs a
functional successor copy of its recipe, begins using it, and replaces it again, removing each
older copy only after its successor is verified functional. Automatic repair is fine; the
requirement is that the repair/replacement activity depend on identifiable, replaceable internal
machinery whose production the organization supports — which the paid, W-catalyzed succession
provides.

## Finding 1 (the decisive fix): AC80's rebuild reorders the acquired program, and that is fatal for any stored decision state

The acquired program (from `ac9_priority_v2.acquire`) is REORDERED: resource/production rule words
0-3, then the four bank rules (masks 4/8/16/32 in priority order), then the boundary word
(mask 256) LAST. `ac80.build_program` — which AC80's `rebuild` calls and unit-tests as equal to
`prog.program` — produces `prog.program` order (five rule words then four bank rules, boundary word
at index 4). These differ: the mask-32 dead rule sits at index 4 in the acquired program but index
5 in `prog.program` order.

Measured consequence: AC80's re-instantiation REORDERS the program bank on every reg fire. Running
AC80's `internalized` arm on seed 0, the masks change from the acquired `[1,2,64,128,32,16,8,4,256]`
to `prog.program` order `[1,2,64,128,256,32,16,8,4]` within the first ~170 ticks, and `acquired !=
prog.program` is True. This is harmless for AC80 (its register is always zero), but the AC12
register bits live in the dead rule, and a reorder moves them too — fatal for any decision state
whose offsets are resolved against the acquired layout.

Fix: `rebuild_active` reproduces the ACQUIRED layout (words 0-3 verbatim, bank rules by the
convention bank b -> (1, 4<<b, 2+b), word 4 last), verified bit-for-bit against the acquired
program for every acquisition priority. Re-instantiation is now order-preserving. This is a
correction of AC80's `build_program`, not an edit of it; the AC80 frozen rows are untouched.

## Finding 2: the succession is affordable only when it does not front-load

The first v1 design fired the succession on the same `dm >= DESC_TRIGGER` signal as the in-place
repair, rate-limited by `SUCC_MIN_SPACING`, but the copy was written at the full frozen per-action
cap (~24-32 writes/tick). Measured: the first succession completes a ~300-write copy+remove burst
in the first ~50 ticks (t~27, right when the description first accumulates 2 minority replicas),
starving the young organism and tipping it into the AC68 W/C collapse — succession arm survived
2/8 while repair survived 6/8.

Fix: the copy and remove are spread over ticks by a per-tick write budget (`SUCC_BUDGET=6`), so a
succession is a slow background process (~50 ticks) rather than a burst. With that, the succession
arm survives 16/16 on engineering seeds 0-7.

## Finding 3: "unmaintained dies" is AC80's claim, not AC86's

AC86 has no program-corruption intervention, so an unmaintained description is simply never called
upon (the program is maintained by the frozen action-2 repair); the `unmaintained` arm's
description degrades to 22-25/78 but the organism may survive (seed 0 does; seeds 1-7 die of the
AC68 collapse). The honest maintenance gate is therefore on the RECIPE CONTENT (`unmaintained`
degrades, `succession`/`repair` keep 78/78), not on survival.

## Measured engineering outcome (seeds 0-7, 16,384 ticks, all 7 gates pass)

| arm | survive | successions | description | pointer |
| --- | --- | --- | --- | --- |
| `succession` | 16/16 | 7 per survivor | 78/78 | 3 (4 slots cycled) |
| `repair` | 16/16 | 0 | 78/78 | 0 |
| `unmaintained` | 1/16 | 0 | 22-25/78 | 0 |

Every `succession` cycle in every survivor is verified functional (`verified_valid == 1`,
`target_correct == 1`) and satisfies the remove-after-verify ordering. The succession writes are
paid (`succ_writes ~2111` over the horizon vs `repair`'s ~16,000 total writes) and W-catalyzed. The
control is clean: with `damage=False` every arm is inert, 0 successions, 78/78, and `succession`
is byte-identical to `repair` (state_hash equality).

## Design carried into the protocol

Arms `succession` (repair + paid succession), `repair` (AC80's in-place repair, no succession), and
`unmaintained` (neither), each x `damage` on/off. Endpoints: `successions` + per-cycle provenance
(`start`/`copy_done`/`switch_tick`/`remove_tick`/`source`/`target`/`verified_valid`/`target_correct`/
`source_correct`), `pointer`, `description_correct`/`valid`, `program_correct` (vs the acquired
program), `writes`/`reg_writes`/`succ_writes`, survival. Seven gates: succession occurs, successor
functional, remove-after-verify, recipe maintained, succession is the replacer, control clean,
completeness/determinism.
