# AC92 protocol v1: functional interruption-and-rescue — observe reconstruction/succession fail and recover while alive

STATUS: **frozen before the first final seed.** Written 2026-09-18. This is a NEW experiment, not a
re-run: it closes the one gap AC91 explicitly left open. AC91 established that blocking W production
kills the organism at 248-254 — BEFORE the succession (t≈2400) or the reconstruction challenge
(t=8192) — so its `fw=8` is post-mortem corruption, not an observed failure to reconstruct while
alive. This study interrupts W availability while the reconstruction function is UNDERWAY, on a
mature organism, and measures a SHORT interval before the energy/converter collapse obscures the
effect.

SOURCES (declared): ac92.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC92_PROTOCOL_v1.md

## The question and the design

The produced, finite-lived machinery that enacts the content writes is the W repair catalyst (4
slots, life 64, born by action 6, autocatalytic). Its per-action write cap `min(32, 8·available_W,
energy, material)` gates every W-catalyzed content write — reconstruction (`reg_from_active`),
description/pointer/controller repair, the succession slot copy/remove, the pointer switch. It does
NOT gate the coordinator transition write `write_ctrl` (energy + material alone, AC88's
distinct-resource model). The design interrupts W production so the W population depletes naturally
to 0 exactly at the reconstruction challenge, observes the reconstruction stall while the organism is
still alive, then restores W availability (machinery only) and observes the reconstruction resume.

**The interruption (production cut).** W-birth is gated from `BLOCK_TICK = CORRUPT_TICK − 63`
(t=8129). W is at a deterministic steady state (W=3, staggered ~21-tick lives), and every live W
catalyst has life ≤ 64, so cutting production at t=8129 guarantees W == 0 by t=8192, exactly when the
8-bit corruption lands and the reconstruction challenge begins. `first_W_empty` is recorded per seed
to verify this (expected in [8164, 8192]). The cut is the same production gate AC91 used; it isolates
exactly the W-birth reaction (bank 0 only), writes no content, and is injected only for the
`W_block`/`W_rescue` arms.

**The rescue (machinery only, labeled EXTERNAL).** At `RESCUE_TICK = 8240` (a 48-tick window after
the corruption, well before the C-converter collapse ~t≈8285 and death ~t≈8400), the `W_rescue` arm
re-seeds the W catalyst population (`life[:4]` ← the frozen acquisition endowment `[32,48,64,0]`,
`pos[:4]` ← interior) and un-blocks W-birth. No description, program, pointer, controller, memory,
energy, material or fuel is touched — the restoration supplies no controller content by construction
(unit-tested). It is a direct experimental restoration of W, clearly labeled EXTERNAL: AC91 separately
established endogenous W production; no single intervention must prove both at once.

## The three matched conditions

Same seed/history, hence same initial content and resources; the arms share identical trajectories
until `BLOCK_TICK` (the gate is a no-op before it, and neither the gate nor the rescue draws RNG).

1. `intact` — normal copying, reconstruction, phase progression. Byte-identical to AC91's
   `succession` arm (no gate injected).
2. `W_block` — W production cut from t=8129 forever. Measures which operations stop (the W-catalyzed
   content writes) and which continue (the W-independent coordinator transition write); the organism
   dies via the named W-loss cascade.
3. `W_rescue` — W production cut from t=8129, then the machinery-only rescue at t=8240; the stalled
   reconstruction resumes and completes.

## The W-dependent vs W-independent split (how "which part remains externally enabled" is settled)

Two levels:

- **Organism level** (the run): in both interrupted arms the W-catalyzed content writes are zero over
  the window `[CORRUPT_TICK, RESCUE_TICK)` (`window_reg_writes == 0` and `window_succ_writes == 0`)
  while the organism is alive, and the reconstruction stays stalled (`fw == 8`); in `W_rescue` the
  reconstruction resumes to `fw == 0` when W returns. `window_ctrl_writes` is recorded and reported,
  not gated — a succession may or may not overlap the 48-tick window (successions are damage-triggered
  and ~2400-tick rate-limited, seed-dependent).
- **Single-step level** (unit tests, deterministic): with W == 0, `write_toward_slot`, `write_pointer`,
  `reg_from_active`, `reg_description_active`, `reg_pointer`, `reg_ctrl` all write 0 replicas (each is
  gated by `_cap`'s 8·W term), while `write_ctrl` writes its mode transition on energy + material
  alone. This is the cleanest demonstration of the split, and the test pins it.

The coordinator transition write `write_ctrl` is NOT claimed to be gated by W (AC91's precision,
carried over).

## World, arms, seeds

World constants unchanged from AC91: PORTS=4, YIELD=64, TICKS=16384, CORRUPT_TICK=8192 (8 bits of
rule 0 flipped), sticky 1e-4 damage on both banks (independent streams), DESC_TRIGGER=2,
POINTER_TRIGGER=2, CTRL_TRIGGER=2, SLOTS=4, SUCC_MIN_SPACING=2400, SUCC_BUDGET=6, REGISTER_THRESHOLD=4,
the corrected MODE/last atomic controller write, the order-preserving generic-over-syntax decoder,
AC75's erase-on-relinquish. `transition='none'` (the function-underway question is about
reconstruction/succession, not the AC75 route-move, which is already tested in AC87/89).

Three arms × damage × corrupt = 3 × 2 × 2 = 12 conditions per individual. Final seeds
`4300, 4301, 4302, 4303` (4 seeds × 2 histories = 8 individuals per condition, 96 rows), disjoint from
engineering 0-7 and every prior final family ≤ 4203. Engineering seeds 0-7.

## Gates (prespecified, categorical per individual)

- **G1 (baseline — the intact machinery reconstructs).** Every `intact` (damage=T, corrupt=T)
  individual: `completed` and `flipped_still_wrong == 0`.
- **G2 (interruption observed while alive).** Every `W_block` (damage=T, corrupt=T) individual:
  `alive_at_corruption` and `alive_pre_rescue` (alive through the window), `fw_pre_rescue > 0` (the
  reconstruction is STALLED while alive), `window_reg_writes == 0` (the W-catalyzed reconstruction
  writes stopped), and `not completed` (the block is fatal).
- **G3 (rescue resumes the reconstruction).** Every `W_rescue` (damage=T, corrupt=T) individual:
  `completed`, `flipped_still_wrong == 0` (reconstruction resumed and completed), `W_pre_rescue == 0`
  and `fw_pre_rescue > 0` (it WAS stalled before the rescue), `window_reg_writes == 0` (stalled
  through the window). The rescue supplies no content by construction (unit-tested).
- **G4 (the W-dependent part is the content execution; the cut removes machinery, not content).**
  Every `W_block` and `W_rescue` (damage=T, corrupt=T) individual: `window_succ_writes == 0` (the slot
  writes stopped with the content writes) and `description_correct_intervention == 130` (the
  description is intact at the intervention).
- **G5 (controls clean).** Every `intact` and `W_rescue` (damage=T, corrupt=F) individual:
  `completed`, `flipped_still_wrong == 0`, `fw_at_corruption == 0`, `fw_pre_rescue == 0` — with no
  corruption there is nothing to reconstruct, so `fw` is 0 throughout (the `fw > 0` in G2/G3 is
  specific to the interrupted reconstruction, not a spurious measurement).
- **G6 (completeness + determinism).** Row count == seeds × 2 × 12, and a sampled exact rerun is
  byte-identical.

## Reported, not gated

- The death mechanism in `W_block` (the AC13 attention-hijack re-located to the mature organism: obs
  bit 6 stays set, the blocked W-birth rule preempts C-birth, C dies, energy drains while fuel stays
  full). Reported as a named finding; the specific death ticks (8354-8413 in engineering) are carried
  as data, not a gate.
- `window_ctrl_writes` and `window_succ_writes`: whether a succession overlaps the window is
  seed-dependent, so these are recorded per individual and reported; the W-dependent/W-independent
  split is gated at the single-step level (unit test) and organism level (G2/G3/G4), not by a
  succession-overlap coincidence.
- `description_correct_at_death` in the dying `W_block` arm (expected 130 — the cut removes machinery,
  not content; AC79's post-mortem-degradation caveat means the live measure is at death, not end).
- Survival is a bimodality-aware lower bound (AC68 W/C collapse is seed-family dependent): the
  `intact`/`W_rescue` survival asserted here is on the engineering and final families, not a
  per-seed-family guarantee.
- The final priorities (recorded at freeze) are not expected to matter: the reconstruction challenge
  corrupts rule 0 (a fixed word), and W-birth is a fixed word, so the mechanism is priority-independent.

## Anti-drift rules

- The runner creates `ac92_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the hashed set.
- `test_ac92.py`, `audit_ac92.py`, `replay_ac92.py` are NOT hashed into the frozen snapshot (AC17's
  rule). If a gate fails, it fails. This protocol may not be edited after the first final seed.
- Engineering seeds (0-7) are excluded from the final sample and are disjoint from the final family.
- The equivalence (declared, verified before finals): `ac92.intact` reproduces AC91 `succession`
  byte-for-byte (`state_hash`) and `ac92.W_block(block_tick=0)` reproduces AC91 `no_W`, on AC91's
  final family 4200-4203 — proving the runner is a correct extension and the gate is a no-op for
  `intact`.

## Source hashes (computed before the first final seed)

    (recorded in ac92_results_v1/pre_run_snapshot.json at freeze time)
