# AC89 protocol v1: re-test the integrated architecture on the previously-failing priority and the simultaneous challenge

STATUS: **frozen before the first final seed.** Written 2026-09-18. This is a BOUNDED RE-TEST of
the AC87/AC88 integrated successor, not new machinery. It closes the two gaps AC87's results doc
recorded: (a) the adversarial priority `[3,0,2,1]` (renewal rule last) was not exercised on AC87's
finals, and (b) AC87 separated the two interventions in time, so the AC82 SIMULTANEOUS
(coincident-tick) challenge was not tested. If either breaks composition, that is the honest answer
and is recorded, not softened.

SOURCES (declared): ac89.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC89_PROTOCOL_v1.md

## The two declared changes from ac88.py (everything else is byte-identical)

1. **Simultaneous schedule.** `MOVE_TICK == CORRUPT_TICK == 8192`: the program-bank corruption
   (8 bits of rule 0 flipped) and the channel-1 route move land on the SAME tick, AC82's
   coincident-tick challenge. AC88 (and AC87) used `MOVE_TICK = 12288` (separated). The
   `run(..., move_tick=...)` parameter is the only schedule switch; the frozen final run uses
   `move_tick=8192`.
2. **Adversarial-priority final seeds.** The final family is `4052, 4054, 4096, 4110`, every one of
   which has acquisition priority `[3,0,2,1]` (verified from `ac4.acquire`'s
   `rng.permutation(4)` with `rng = default_rng([seed, 1004])`). In the acquired, order-preserving
   layout `[3,0,2,1]` ranks bank 1 (the renewal rule, mask 8 / action 3) LAST among the four bank
   rules — the priority AC83 pinned the route-holding failure to. The seeds are disjoint from
   engineering (0-7) and every prior final family (≤ 4031).

## Equivalence of the runner (declared, verified in engineering before finals)

`ac89.run(..., move_tick=12288)` on AC88's finals must reproduce AC88's frozen rows field-for-field
(`state_hash` included). This is the proof that the runner is a correct extension and that the ONLY
differences are the schedule constant and the seed family. The new fields
`description_correct_intervention` (read at `t == CORRUPT_TICK`, after the step) and `move_tick`
are additive observations only; they do not change the world state, so the `state_hash` is
unchanged.

## Arms, world, seeds

Unchanged from AC88: five arms (`succession`, `repair`, `ctrl_unmaintained`, `unmaintained`,
`no_repair`), the damage/corrupt/transition condition grid (5 x 2 x 2 x 2 = 40 conditions per
individual), world constants (PORTS=4, YIELD=64, TICKS=16384, sticky 1e-4 damage on both banks from
independent streams, DESC_TRIGGER=2, POINTER_TRIGGER=2, CTRL_TRIGGER=2, SLOTS=4,
SUCC_MIN_SPACING=2400, SUCC_BUDGET=6, REGISTER_THRESHOLD=4), the corrected MODE/last atomic
controller write, the distinct-resource model, the order-preserving generic-over-syntax decoder, and
AC75's erase-on-relinquish route adaptation. Final seeds `4052, 4054, 4096, 4110` (4 seeds x 2
histories = 8 individuals per condition, 320 rows). Engineering seeds 0-7 (disjoint).

## Gates (prespecified; G8 is the re-test)

G1-G7 are the AC88 mechanism gates unchanged (they operate on the no-corruption, no-move core,
`damage=True, corrupt=False, transition='none'`, which the schedule change does not touch). They
re-establish the succession machinery on the adversarial-priority seeds.

G8 is reshaped for the composition re-test, and is UNCONDITIONAL on reconstruction (per individual,
dead or alive — AC82's finding that reconstruction holds even in collapse deaths):

- `flipped_still_wrong == 0` for EVERY succession individual under `corrupt=True, transition='perm'`
  (reconstruction unconditional, no survivor-conditioning);
- `description_correct_intervention == 130` for every such individual (description intact at the
  intervention, AC82's "unconditional at the intervention");
- `description_correct == 130` for every SURVIVOR among them (post-mortem degradation excluded —
  AC79's caveat: a dying organism's paid repair stops at death while the damage stream continues);
- `unmaintained` and `no_repair` die (reconstruction/repair is load-bearing);
- non-vacuity: at least one succession individual survives.

Survival and route-holding are **reported, not gated** (the card's four unconditional endpoints).
Survival is reported as a bimodality-aware lower bound (the AC68 W/C collapse is seed-family
dependent). Route-holding (both routes bound and `route1_correct`) is the endpoint that may
legitimately fail under the adversarial priority + simultaneous challenge; if it does, the per-
individual values are recorded, not softened.

## Anti-drift rules

- The runner creates `ac89_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the hashed set.
- `test_ac89.py` is not hashed (AC17's rule). If a gate fails, it fails. This protocol may not be
  edited after the first final seed.
- The route-holding outcome is NOT known at protocol-writing time; the protocol prespecifies the
  gate SHAPE (unconditional reconstruction + load-bearing controls + reported route-holding), which
  is exactly the shape required whether route-holding holds or fails.

## Source hashes (computed before the first final seed)

    (recorded in ac89_results_v1/pre_run_snapshot.json at freeze time)
