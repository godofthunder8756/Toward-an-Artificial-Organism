# AC87 results v1: the integrated successor — frozen, all nine gates pass

2026-09-18. Final seeds 4028-4031 (4 seeds x 2 histories = 8 individuals per condition, 320 rows),
hashed protocol `AC87_PROTOCOL_v1.md`, 16,384 ticks, sticky 1e-4 damage on the program bank and (for
the damaged arms) on the active slot + successor slot + pointer + controller state from an independent
stream. Engineering seeds (0-7) excluded. **All nine predeclared gates pass.** Audit passed (320 rows,
14 source hashes no drift, generic-decode link verified, gates recomputed without simulating); replay
6/6 exact; 120 tests green (56 core AC1-9 + 64 AC80-87 line).

## Result

The replacement machinery's own coordination is now inside the organization it coordinates. The
complete 130-bit description (five rule words + 8-bit permutation + four bank-rule masks + four
bank-rule actions) lives in four interchangeable slots selected by a generation pointer; the
succession coordinator's working state (active / phase / last-start) lives in the same vulnerable,
damage-streamed, paid-maintained substrate; both source and successor are exposed to damage and the
pointer switches only after a real verify (syntactically valid AND matches the source); the generic
decode is generic over syntax and order-preserving; and the combined architecture (reconstruction +
description maintenance + route-move adaptation) holds routes with the corrected decoder.

## The measured arms (core succession, damage on, no corruption, no move)

| arm | survive | successions | description | controller state |
| --- | --- | --- | --- | --- |
| `succession` | 8/8 | 6-7 | 130/130 | idle, minority 0-1 |
| `repair` | 8/8 | 0 | 130/130 | maintained at idle |
| `ctrl_unmaintained` | 8/8 | 5-7 | 130/130 | minority 6-10 |
| `unmaintained` | 0/8 | 0 | 55-74/130 | degraded |
| `no_repair` | 0/8 | 0 | 55-74/130 | degraded |

Every `succession` cycle in every survivor is `verified_valid == 1` and `target_correct == 1` (the
successor equals the full 130-bit installed description, bank-rule content included) and satisfies
`remove_tick >= switch_tick >= copy_done >= start`. The controller state ends idle with
`ctrl_minority_end` 0-1: it was damaged and repaired without cementing a wrong majority. In
`ctrl_unmaintained` (maintenance cut) the same state degrades to minority 6-10, so the maintenance is
what keeps the coordinator's own state clean.

## The composition (perm + corrupt: rule 0 flipped at t=8192, channel 1 moved at t=12288)

| arm | survive | reconstruct (fw=0) + desc=130 | hold both routes |
| --- | --- | --- | --- |
| `succession` | 8/8 | 8/8 | 8/8 |
| `repair` | 8/8 | 8/8 | 8/8 |
| `unmaintained` | 0/8 | — | 0/8 |
| `no_repair` | 0/8 | — | 0/8 |

`succession` reconstructs the corrupted controller (`flipped_still_wrong == 0`) and keeps the
130-bit description intact in all 8 individuals, holds both routes (route 1 re-acquired to the
relabelled port), and survives 8/8. `unmaintained` dies 8/8 (deaths 888-2496) and `no_repair` dies
8/8 (deaths 514-912): reconstruction and the repair loop are load-bearing. The no-damage control is
byte-identical across `succession`==`repair` (0 successions, 130/130, `state_hash` equality): the
mechanism is inert.

## What changed from AC85/AC86 (and what it closes)

1. **Full description + succession.** AC86 copied the 78-bit description (bank rules synthesized
   externally); AC87 copies the full 130-bit description, bank-rule masks/actions included
   (`target_correct == 1` is the 130-bit equality). This closes the AC85/AC86 review's "two
   capabilities, not one architecture" note.
2. **Controller state internalized.** AC86's `Succession` held `phase/source/target/active/timing` as
   Python fields; AC87 stores active/phase/last-start in bank 1 (damage-streamed, paid-written,
   `reg_ctrl`-maintained) and derives source/target from the maintained pointer. The maintenance is
   load-bearing for the state's cleanliness (G6), not for survival.
3. **Verify is a real gate.** The pointer switches only after the successor decodes valid AND matches
   the source, with a re-check in the switch phase; AC86 logged `verified_valid` and switched
   regardless. Both source and successor are damaged, so the gate is exercised.
4. **Generic-over-syntax decode.** `build_program` reads the masks/actions and keeps only the
   "permutation is a permutation" syntax check; a stored mask/action flipped to another valid value
   decodes faithfully (unit test) — no `m == (4<<b)` / `a == (2+b)` correctness rule.
5. **Composition with the order-preserving decoder.** Under perm+corrupt, `succession` holds both
   routes 8/8. This is the re-run the card asked for (AC83 attributed route loss to seed/priority
   renewal contention; AC86 showed AC80's decode reordered the bank).

## Boundary (unchanged from protocol)

No recovery from catastrophic recipe-content corruption (a successor is a copy of the active slot's
majority — AC61 one level down). The four bank rules are still four bank rules (format); what is
internalized is their mask/action content. The succession state machine is supplied format-level
machinery operating on vulnerable values. No content self-production (AC78 blocked). Two caveats,
stated plainly: (a) route-holding is reported as a lower bound, and the final seeds 4028-4031 happen
not to include AC83's adversarial priority (renewal rule last, `[3,0,2,1]`) — their priorities are
`[3,2,1,0]`, `[1,2,3,0]`, `[1,2,0,3]`, `[3,0,1,2]`, none of which ranks bank 1 (renewal) last, so the
seed-dependent renewal-contention limit (AC83) is not exercised on these finals; (b) the controller-
state maintenance keeps the coordinator's state clean, but the succession is robust to its degradation
(source/target derived from the maintained pointer), so G6 is a state-cleanliness contrast, not a
survival claim.

## Process note

This run supersedes an earlier 2026-09-17 engineering attempt preserved at
`AC87_ENGINEERING_v1_PRIOR-20260917.md` and `ac87_engineering_v1_prior-20260917/` (122-bit no-
permutation description, no composition, different runner). That attempt is a record, not a base; this
runner is a fresh implementation.

## Files

`ac87.py` (runner), `AC87_PROTOCOL_v1.md` (hashed protocol), `AC87_ENGINEERING_v1.md` (engineering),
`test_ac87.py` (14 tests), `audit_ac87.py` (split audit), `replay_ac87.py` (sampled exact reruns),
`ac87_results_v1/` (frozen rows, pre-run snapshot, results), `ac87_engineering_v1/` (engineering).
