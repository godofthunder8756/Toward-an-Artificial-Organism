# AC92 results v1: functional interruption-and-rescue — reconstruction fails and recovers while the organism is alive

2026-09-18. Final seeds `4300, 4301, 4302, 4303` (4 seeds × 2 histories = 8 individuals per condition,
96 rows), hashed protocol `AC92_PROTOCOL_v1.md`, 16,384 ticks, `transition='none'`, corruption at
t=8192, W-birth blocked from t=8129, rescue at t=8240. **All six prespecified gates pass.** Audit
passed (96 rows, 14 source hashes no drift, arm invariants, W-dependence contrast, generic-decode link,
gates recomputed without simulating); replay 6/6 exact; 174 tests green (56 core AC1-9 + 118 AC79-92
line, incl. 16 AC92).

> **Post-review wording corrections (2026-09-18, conclusion unchanged):** W reaches zero at
> **8176–8178**, just before the challenge at 8192 (not "exactly at" the challenge); and the intact
> reconstruction is **initial repair → subsequent damage → final recovery** — seed 4303's two histories
> show two incorrect bits at t=8239 after the initial repair — not "correct thereafter" (G1 and
> §"What this establishes" revised accordingly).

## The question

AC91 established that blocking W production is necessary for viability and sustained W-dependent
maintenance capacity, but it blocked from t=0, so the blocked organisms died at 248-254 — BEFORE
succession (t≈2400) or the reconstruction challenge (t=8192). Their `fw=8` is post-mortem corruption,
not an observed failure to reconstruct while alive. This study closes that gap: interrupt W availability
while the reconstruction function is UNDERWAY on a mature organism, and observe the failure and the
recovery while the organism is alive.

The produced, finite-lived machinery that enacts the content writes is the W repair catalyst; its write
cap `min(32, 8·available_W, energy, material)` gates every W-catalyzed content write (reconstruction,
description/pointer/controller repair, the succession slot copy/remove, the pointer switch) but NOT the
coordinator transition write `write_ctrl` (energy + material alone, AC88). The interruption cuts W
production from `BLOCK_TICK = CORRUPT_TICK − 63` (t=8129), so W depletes naturally to 0 at 8176–8178
(first_W_empty), just before the corruption tick (t=8192); the rescue re-seeds W (life[:4] ← the frozen endowment) and un-blocks production at
t=8240, touching no content.

## The measured arms (damage on, corruption on, no route move)

| arm | survive | first death | first_W_empty | fw at 8239 | window reg_writes | W_pre | fw (end) | desc at death | successions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `intact` | **8/8** | — | — | 0 (6×), 2 (2×) | 25–44 | 3 | 0 | — | 6 |
| `W_block` | **0/8** | 8410–8414 | 8176–8178 | 7–8 | **0** | 0 | 7–8 | **130** | 3 |
| `W_rescue` | **8/8** | — | 8176–8178 | 7–8 | **0** | 0 | 0 | — | 6–7 |

`window_succ_writes` and `window_ctrl_writes` are 0 in every arm over the 48-tick window
[8192, 8240): no succession cycle overlaps the window (successions are damage-triggered and ~2400-tick
rate-limited), so the W-independent coordinator transition is established at the single-step level (unit
tests), not by a succession-overlap coincidence. `desc at death == 130` in the dying arm: the cut removes
the machinery, not the content.

## The three causal links (the gates, all categorical per individual)

**G1 — the intact machinery reconstructs.** Every `intact` individual completes with `fw == 0` at the
end. The trace distinguishes three phases, not a single repair-and-stays-fixed step: (1) **initial
repair** — the 8-bit corruption is reduced to `fw_at_corruption == 2` by the first repair pass (24
writes = six bits rewritten, two still wrong) and reaches 0 within ~2 ticks; (2) **subsequent damage** —
in seed 4303's two histories the ongoing sticky 1e-4 damage stream re-corrupts two bits after that
initial repair, so `fw_pre_rescue == 2` at t=8239 (the other six individuals read 0); (3) **final
recovery** — every individual ends `fw == 0`, so those re-corrupted bits are repaired again. The
load-bearing claim is final recovery, not uninterrupted correctness after the first repair.

**G2 — the interruption is observed while alive.** Every `W_block` individual is alive at the corruption
tick AND at t=8239 (48 ticks later), with `fw == 7–8` (the reconstruction is genuinely stalled — the
program stays corrupted) and `window_reg_writes == 0` (the W-catalyzed reconstruction writes stopped
entirely), then dies at 8410–8414 with `description_correct_at_death == 130`. This is the AC91 gap
closed: the `fw > 0` is now a live observation, not post-mortem corruption.

**G3 — the rescue resumes the reconstruction.** Every `W_rescue` individual was stalled before the
rescue (`W_pre_rescue == 0`, `fw_pre_rescue == 7–8`, `window_reg_writes == 0`), then — after the
machinery-only re-seed at t=8240 — reconstructs (`fw == 0` at the end) and survives 8/8. The restoration
is the organism's own W-birth reaction turned back on plus a direct re-seed of the produced catalyst;
neither touches the description, program, pointer or coordinator state (unit-tested), so no controller
content is supplied or altered by construction.

**G4 — the W-dependent part is the content execution.** In both interrupted arms the W-catalyzed slot
writes are zero over the window and the description is intact at the intervention (130/130): the cut
removes machinery, not content. The W-independent side is pinned by unit tests — `write_ctrl` writes its
mode transition on energy + material alone with W == 0, while `write_toward_slot`, `write_pointer`,
`reg_from_active`, `reg_description_active`, `reg_pointer`, `reg_ctrl` all write 0 with W == 0.

**G5 — controls clean.** With corruption off, every `intact` and `W_rescue` individual completes with
`fw == 0` throughout (nothing to reconstruct, no spurious `fw`). The equivalence (separate check):
`ac92.intact` reproduces AC91 `succession` byte-for-byte (`state_hash`) and
`ac92.W_block(block_tick=0)` reproduces AC91 `no_W`, on AC91's final family 4200-4203 — 64/64 rows
byte-identical, proving the runner is a correct extension and the gate is a no-op for `intact`.

## The self-repair nuance in `fw_pre_rescue` (reported, not gated)

`fw_pre_rescue` is 7–8 rather than a uniform 8: the two corrupted bits of rule 0 whose acquired value is
1 (bits 0–1; rule 0 encodes `(1,1,0)`, so bits 0 and 1 are both 1) self-repair under the sticky `|=`
damage stream, which ORs replicas toward 1 and so re-corrects an acquired-1 bit whose corruption set it
to 0. One such bit self-repaired by t=8239 in seed 4303's two histories (`fw == 7`); the other six
acquired-0 bits stay corrupted. This is the AC67/AC71 self-reversing-damage phenomenon, not W-catalyzed
reconstruction — `window_reg_writes == 0` proves no reconstruction ran. The load-bearing observation is
therefore the pair `window_reg_writes == 0` AND `fw_pre_rescue > 0`, not `fw_pre_rescue == 8`.

## The death mechanism in `W_block` (reported, not gated)

The cascade is the same AC13 attention-hijack AC91 located in the early-block organism, re-located to the
mature organism: with W < 2 the observation bit 6 is permanently set, the program fires the blocked
W-birth rule (mask 64) ahead of the C-birth rule (mask 128), C-birth is preempted, the C converters
expire (C=0 by ~t≈8298), conversion stops, and energy drains to 0 (death 8410–8414, 234 ticks after
W=0). At death `material` is 66–110 and `fuel` 20–27 — not full, because the interruption is on a mature
organism whose economy has been running for 8129 ticks (unlike AC91's t=0 block, whose fuel accumulated
to full). The invariant that matters is `description_correct_at_death == 130`: the block removes the
machinery and therefore the functions, not the controller content.

## Equivalence of the runner

`ac92.run(...)` reproduces AC91's frozen `state_hash` for `succession` (as `intact`) and `no_W` (as
`W_block` with `block_tick=0`) on AC91's final family at `transition='none'` for every damage/corrupt
combination — 64/64 rows byte-identical. The only additions are the block/rescue arms and additive
observation fields (`fw_at_corruption`, `fw_pre_rescue`, `W_pre_rescue`, `window_*_writes`,
`pointer_*`, `rescue_applied`), which do not change the world state.

## What this establishes, and its limits

Supported: on a mature organism, cutting W production so W depletes to 0 (first_W_empty 8176–8178, just
before the challenge) makes the reconstruction fail WHILE ALIVE (the program stays corrupted, `window_reg_writes
== 0`), and a machinery-only restoration of W makes it resume and complete. The W-dependent / W-independent
split is now demonstrated at both levels: the W-catalyzed content writes are the part that stops and
resumes with W, while the coordinator transition write is not gated by W. AC91's "functional interruption
and rescue of an ONGOING operation remain untested" is closed for the reconstruction function.

Not established, and not claimed:

- **Full autopoiesis is still not claimed.** The succession state machine's transition logic
  (`advance()`) and the interpreter (`prog.choose`) remain supplied format-level machinery; what is
  shown produced, interrupted and restored is the W catalyst that executes the supplied machine's
  writes. The `write_ctrl` transition write is the coordinator's own register, declared W-independent
  (AC88's distinct-resource model), so the coordination — not just the execution — is the supplied part.
- **The succession function was not observed mid-cycle.** No succession overlaps the 48-tick window, so
  the "copying stops while the coordinator keeps changing phase" observation is established at the
  single-step level (unit tests: content writes stop, `write_ctrl` does not) rather than observed as a
  live mid-copy stall. This is a scope note, not a gap in the reconstruction claim.
- **The rescue is EXTERNAL.** The direct re-seed of W is a causal rescue control labeled external; AC91
  separately established endogenous W production. No single intervention proves both.
- **No content self-production** (AC78 still blocked); the description is inherited, not produced.
- **Survival is a bimodality-aware lower bound** (AC68 W/C collapse is seed-family dependent): 8/8
  finals and 16/16 engineering survive on the `intact`/`W_rescue` arms, reported as the observed count,
  not a per-seed-family guarantee.
- **The final priorities** `[1,3,0,2]`, `[0,2,3,1]`, `[3,2,1,0]`, `[0,1,3,2]` do not include AC83's
  adversarial `[3,0,2,1]`; the reconstruction challenge corrupts rule 0 (a fixed word) and W-birth is a
  fixed word, so the mechanism is priority-independent — recorded as a scope note, not a gap.

## Verification

- `audit_ac92.py` re-derives coverage (96 rows), arm invariants (`first_W_empty ≤ CORRUPT_TICK` for the
  interrupted arms, `description_correct_intervention == 130`), the W-dependence contrast (`window_reg_writes
  == 0` with `fw_pre_rescue > 0` in `W_block`), the generic-decode link, source hashes (14 files, no
  drift) and all six gates — without simulating.
- `replay_ac92.py`: 6/6 sampled conditions reproduce exactly, `state_hash` and endpoint fields.
- `test_ac92.py` (16 tests): the gate is a no-op for `intact` and blocks exactly bank-0 births from
  `block_tick` (writes no content); the rescue touches only life/pos (machinery-only); the W-dependence
  of the content writes vs the W-independence of `write_ctrl`; final-seed disjointness; the gate shapes
  are categorical per individual; the recorded freeze and the content-intact-at-death mechanism are
  pinned on the finals.
- Full suite: 174 tests green (56 core AC1-9 + 118 AC79-92 line, incl. 16 AC92).
- Runtime: each 16,384-tick condition is ~3 s; the 96-row final grid ~5 min.

## Files

`ac92.py` (runner, sha256 `09cf6c9588b9d03d8630f4c8fd24c0c240e53d68048a717c4ff7993984305f5c`),
`AC92_PROTOCOL_v1.md` (hashed protocol, sha256
`8b22972dde60dcff9d4859397351007ca0abd72aa46175a011578eeb0f32c98b`), `test_ac92.py`,
`audit_ac92.py` (split audit), `replay_ac92.py` (sampled exact reruns), `ac92_results_v1/` (frozen rows,
pre-run snapshot, results), `ac92_engineering_v1/` (engineering, seeds 0-7).
