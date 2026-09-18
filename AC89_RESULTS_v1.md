# AC89 results v1: the adversarial priority and the simultaneous challenge both close — composition holds 8/8

2026-09-18. Final seeds `4052, 4054, 4096, 4110` (4 seeds x 2 histories = 8 individuals per
condition, 320 rows), hashed protocol `AC89_PROTOCOL_v1.md`, 16,384 ticks, SIMULTANEOUS schedule
(`MOVE_TICK == CORRUPT_TICK == 8192`). **All nine prespecified gates pass.** Audit passed (320 rows,
14 source hashes no drift, generic-decode link verified, seeds and schedule verified, gates
recomputed without simulating); replay 6/6 exact; 143 tests green (56 core AC1-9 + 79 AC79-88 line
+ 8 AC89).

## The question

AC87's composition (succession holds both routes under corrupt@8192 + move@12288) carried two
recorded caveats, both closed here as a bounded re-test, not new machinery:

1. AC87's finals (4028-4031) had priorities `[3,2,1,0]`, `[1,2,3,0]`, `[1,2,0,3]`, `[3,0,1,2]` —
   NONE ranked the bank-1 renewal rule last. AC83 had located the route-holding failure in exactly
   the priority `[3,0,2,1]` (renewal last).
2. AC87 separated the interventions in time; AC82 showed the SIMULTANEOUS (coincident-tick)
   corruption+move drives the non-composition (reconstruction cost + the move's income cut set obs
   bit 1, preempting renewal).

## The result

Under the corrected post-AC88 runner — the MODE/last atomic controller write, the distinct-resource
model, the order-preserving generic-over-syntax decoder, and AC75's erase-on-relinquish route
adaptation — **both gaps close**. The composition (succession, simultaneous perm+corrupt) on the
adversarial-priority finals:

| arm | survive | reconstruct (fw==0) | desc 130/130 (end) | desc 130/130 (intervention) | hold both routes |
| --- | --- | --- | --- | --- | --- |
| `succession` | **8/8** | **8/8** | **8/8** | **8/8** | **8/8** |
| `repair` | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 |
| `unmaintained` | 0/8 | — | — | — | 0/8 |
| `no_repair` | 0/8 | — | — | — | 0/8 |

Reconstruction is **unconditional** (`flipped_still_wrong == 0` in all 8 individuals, dead or
alive), description integrity holds both at the intervention and at end in every survivor, and both
routes are held (`demand=[42,0]` — two live entries — and `route1_correct` in all 8). Every
individual survives (8/8) with the body intact (W=3, C=2, energy 119-124). The controls are clean
and categorical: `unmaintained` and `no_repair` die 8/8, so reconstruction and the repair loop are
load-bearing under this schedule and priority.

Engineering (seeds 0-7, disjoint) gave the same picture: 9/9 gates, composition 16/16 survive,
16/16 fw=0, 16/16 desc=130/130, 16/16 hold both routes.

## Why the previously-failing conditions no longer fail

Two mechanisms, both already introduced by AC86/AC87 and now measured under the adversarial
priority and the simultaneous schedule:

1. **The order-preserving decoder moved the boundary rule LAST.** AC83's failure was the boundary
   rule (mask 256) preempting the bank-1 renewal rule. That ordering was an artifact of AC80's
   non-order-preserving decode, which placed the five fixed words (boundary included) BEFORE the
   bank rules. AC86 corrected `build_program` to reproduce the ACQUIRED layout (`ac9_priority_v2`'s
   reorder), where the boundary word sits at position 8 — AFTER the four bank rules. For
   `[3,0,2,1]` the renewal rule (bank 1) is therefore at position 7, ahead of the boundary, so the
   specific "boundary preempts renewal" path AC83 located is structurally gone. The re-test confirms
   it empirically: route-holding is now independent of whether the priority ranks renewal last.

2. **The simultaneous material-low hijack is transient under erase-on-relinquish.** A trace on
   seed 4052 shows the corruption's ~32-material cost still drives material to 51 (< 64) at t=8195,
   setting obs bit 1, and the program answers with the material contact (action 1). But the
   erase-on-relinquish adaptation drops the stale route-1 entry on the failure streak and the next
   contact re-binds it; material recovers to 83 by t=8200, obs bit 1 clears, and the renewal (action
   3) fires at t=8200 with the unmoved route 0 never having lapsed (its life stays 16-52 throughout).
   In AC82's non-order-preserving, no-succession build the material contact missed repeatedly and
   obs bit 1 stayed set, starving renewal until route 0 expired; here the hijack lasts ~5 ticks, far
   short of route 0's remaining life.

## Scope and caveats

- **Route-holding is reported unconditionally (8/8) and also held in the diagnostic on the
  collapse-heavy 8-15 family (16/16, not frozen).** It is a property of the corrected decoder +
  succession, not a seed coincidence on the finals.
- **Survival is a bimodality-aware lower bound.** 8/8 finals and 16/16 engineering survive here,
  but the AC68 W/C collapse is seed-family dependent (AC39's lesson), so survival is reported as the
  observed count, not a guarantee for every seed family. The 8-15 diagnostic (16/16 survive, W=3
  C=2 intact) suggests the succession machinery's periodic rebuilds also blunt the collapse, but
  that is not claimed here — it would need its own long-horizon study.
- This is a **re-test of composition**, not a new internalization step. The boundary conditions of
  AC87/88 (no recovery from catastrophic recipe-content corruption; four-bank-rule format; no
  content self-production) are unchanged. What this closes is the recorded claim that the
  integrated architecture's route-holding was "only a lower bound" and untested on the simultaneous
  schedule.

## Equivalence of the runner

`ac89.run(..., move_tick=12288)` reproduces AC88's frozen rows field-for-field on seed 4028 (40/40
conditions, `state_hash` included). The runner is a correct extension of ac88: the only differences
are the schedule constant (`MOVE_TICK == CORRUPT_TICK`) and the final seed family.

## Files

`ac89.py` (runner, sha256 `6cf341febb3939e438dc1815c2b4028231ba3a76037558276133543dcd6f1c62`),
`AC89_PROTOCOL_v1.md` (hashed protocol), `test_ac89.py` (8 tests: schedule, seeds, order-preserving
decoder, AC88 equivalence, unconditional gate shape, recorded freeze), `audit_ac89.py` (split
audit), `replay_ac89.py` (sampled exact reruns), `ac89_results_v1/` (frozen rows, pre-run snapshot,
results), `ac89_engineering_v1/` (engineering, seeds 0-7).
