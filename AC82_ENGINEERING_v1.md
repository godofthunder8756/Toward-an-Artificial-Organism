# AC82 engineering v1: combining reconstruction + description maintenance + environmental adaptation

2026-09-17. `ac82_engineering.py`. **Engineering prerequisite — no final seeds, no frozen claim.**
Milestone 3 of the internalize-the-recipe goal: combine the three capabilities established
separately — AC80's internalized reconstruction (78-bit description + generic decode), AC79's
description maintenance (paid, own trigger), and AC75's erase-on-relinquish route-move
accommodation — in ONE frozen architecture, re-enabling the route moves AC79/AC80 disabled
(`ac12.MOVE_KEYS=()`, `MOVE=10**9`). The decisive question: does the combined architecture survive,
reconstruct, and re-acquire its routes **unconditionally** (not conditioned on survivors, closing
the survivor-conditioning weakness of AC79's G1)?

## The design

The combined runner is AC80's `build` (sticky program damage, DESC_TRIGGER description repair,
generic-decode re-instantiation on obs bit 2 OR description minority) joined to AC75's
erase-on-relinquish allocation and permanent route move of channel 1 at t=8192. The intervention is
**simultaneous**: the AC80 program corruption (8 bits of rule 0 flipped at t=8192) and the AC75
route move (channel 1 relabelled at t=8192) land on the same tick, so reconstruction and
environmental adaptation are exercised together.

Arms: `internalized` (desc damaged + repaired + generic decode + erase), `pristine` (desc never
damaged, hidden-backup baseline), `unmaintained` (desc damaged, no repair), `no_repair` (loop cut),
`restore` (desc maintained + generic decode + **no** erase). Two transitions (perm, none) x two
corruption conditions.

## Declared change from AC75: the `_restore` firing condition

AC75's `AllocErase._restore` fires on **any set replica** of the register bit (`n = (sites != 0).sum() > 0`),
not only on an actual relinquishment. In the combined desc+reg world this is not inert: it is a
redundant paid repair (the register bit is already majority-repaired by action 2), and measured on
seed 1 it starves the renewal budget and loses the unmoved route (`internalized` ends
`routes=[None,0]` where AC80's `ac12.Alloc` holds `[1,0]`). `ac82_engineering.py` therefore
redefines `_restore` to fire only when the slot actually reads as relinquished
(`ac12.bit_value` majority >= `REGISTER_THRESHOLD`), the semantically correct "undo a
relinquishment" primitive. This is a new alloc class in the new runner, not an edit to `ac75.py`.

With the fix, the no-move, no-corruption control is clean (14/16 hold both routes; the two
non-holders are the known AC68 collapse seed), and the fix additionally *corrects* damage-induced
register majority-flips on productive contact (seed 2 survives in the combined world where it dies
at t=4957 under `ac12.Alloc`).

## Measured outcome (engineering seeds 0-7, 16 individuals/condition)

| condition | survive | fw=0 (reconstruct) | desc=78 | hold both routes |
| --- | --- | --- | --- | --- |
| `internalized` perm, corrupt | 14/16 | **16/16** | 14/16 | **10/16** |
| `internalized` perm, no corrupt | 14/16 | 16/16 | 16/16 | 12/16 |
| `internalized` none, corrupt | 16/16 | 16/16 | 16/16 | 14/16 |
| `pristine` perm, corrupt | 14/16 | 16/16 | 16/16 | 14/16 |
| `restore` (no erase) perm, corrupt | 10/16 | 16/16 | 10/16 | 8/16 |
| `unmaintained` perm, corrupt | 0/16 | — | — | 0/16 |
| `no_repair` perm, corrupt | 0/16 | — | — | 0/16 |

Reconstruction is **unconditional**: `flipped_still_wrong == 0` in all 16/16 individuals, including
the two collapse deaths (the corrupted rule 0 is always re-instantiated correctly before the body
collapses). Description maintenance is unconditional at the intervention (16/16 `desc=78`); the two
`desc=77`/`58` values are post-mortem degradation in the collapse seed, exactly AC79's caveat.
The controls are clean and categorical: `unmaintained` and `no_repair` die 0/16.

## The decisive question is answered NO: route re-acquisition is not unconditional

Under perm + corruption only **10/16** individuals end with both routes held. The 6 non-holders are
not the reconstruction or the description — they hold the program and description perfectly — they
**lose the unmoved route 0 during the re-acquisition transient**. Seeds 0 and 7 lose route 0 (and
survive on random fallback); seed 4 dies of the AC68 W/C collapse (t=14089).

The mechanism, pinned by an instrumented trace on seed 0:

1. t=8192: the corruption flips rule 0 (fuel) and the re-instantiation pays ~32 material to rebuild
   it; material falls 96 -> 44, so observation bit 1 (`material <= 64`) sets.
2. t=8193-8197: the route move has relabelled channel 1, so the program's answer to obs bit 1 —
   action 1 (material contact, rule 1) — misses the stale port and yields nothing; material stays
   low; obs bit 1 stays set.
3. Because rule 1 (mask 2, action 1) precedes the bank-1 rule (mask 8, action 3 = renew region 0)
   in the frozen program, the material contact **preempts the renewal**. Route 0's entry ages 12 -> 1
   unrenewed and expires at t=8205, then is never re-bound (its key was never moved; the organism
   has no signal to re-acquire it).

This is the AC74 "attention hijack" pattern (an observation bit that stays set makes the program
loop on one action and neglect the rest), here operating on route 0 rather than the organism: the
reconstruction's material cost and the move's material-income cut **interact** to drive material low
enough that the frozen priority order starves the memory renewal.

## Conclusion

The engineering screen **kills the "unconditional survival + recovery" claim** before any protocol.
What the combined architecture does unconditionally: reconstruct the corrupted controller (16/16)
and maintain the 78-bit description (16/16 at the intervention). What it does not: re-acquire the
moved route in every individual (10/16), because the reconstruction cost + the move's income cut
together trigger the material-low observation, whose frozen priority preempts the memory renewal.
Survival is the known AC68 bimodality (14/16 here), and recovery-from-collapse is not tested by any
architecture that has this interaction.

The three capabilities therefore do **not** trivially compose. The next target is the
material-low observation hijack during a simultaneous reconstruction + move: either separate the two
interventions in time (a design choice that must be declared, not discovered after the result), or
make the reconstruction cheaper / the renewal higher-priority — none of which is available without
changing a frozen law. A frozen AC82 claiming unconditional survival + recovery would be
unsatisfiable on this architecture.

## Artifacts

`ac82_engineering.py`. Scratch probes (`_*.py`) are throwaway instrumentation, not part of the
deliverable. Related: `AC80_RESULTS_v1.md` (reconstruction), `AC79_RESULTS_v1.md` (description
maintenance), `AC75_RESULTS_v1.md` (route-move accommodation), `AC74_ENGINEERING_v1.md` (the
attention-hijack cascade this re-triggers).
