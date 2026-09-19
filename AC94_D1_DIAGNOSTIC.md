# AC94-D1 — diagnosis: the W=2 SWITCH→REMOVE refusal is a real pointer/phase/remove inconsistency, not "a 1-2 tick delay only"

2026-09-18. Measurement/diagnostic only — no fix, no protocol, no freeze. `ac93.py` at `1fe48df`
(sha256 of the runner unchanged from the AC93 freeze: `d9fda66…d514`). Traces were produced by
`_ac94_d1_probe.py` (natural refusal scan + controlled single-transition repro) and
`_ac94_d1_followup.py` (slot-occupancy + succession-log window), both monkey-patching
`ac93.advance` / `ac93.write_ctrl` in-process — the frozen runner is untouched.

## The four questions, answered with the actual trace

The event under test is the SWITCH branch of `ac93.advance()` (lines 457–466). It performs two
separate, differently-gated writes back-to-back:

1. `write_pointer(o, e, target)` — at most 2 sites (a 2-bit pointer), affordable whenever
   `_cap = min(32, 8·W, energy, material) ≥ 2`, i.e. W ≥ 1.
2. `write_ctrl(o, e, encode_ctrl(1, PHASE_REMOVE, last), gate_ctrl)` — the MODE transition
   SWITCH (011) → REMOVE (100) flips all 3 phase bits = 21 replicas, gated atomically under
   `_cap`. At W = 2 the cap is 16, so 21 > 16 → refused, and `write_ctrl` returns 0.

The two writes are **not** one atomic transaction, and they have **different** affordability
thresholds. That is the whole story.

### Natural trace (seed 1, `gated`, damage=T, corrupt=T, first of 9 refusals found across seeds 0–7)

| tick | phase (entering) | ptr | source | target | W | cap | write_ctrl call | n_mode | refused | written | switch_tick logged | next phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9714 | SWITCH | 3 | 3 | 0 | 2 | 16 | target REMOVE | 21 | **yes** | 0 | **yes (9714)** | SWITCH (refused) |
| 9715 | SWITCH | 0 | 0 | 1 | 2 | 16 | target COPY | 7 | no | 7 | no | COPY (revert) |

The controlled single-transition repro (hand-built organism in PHASE_SWITCH, W = 2, source 0 /
target 1 equal and valid) reproduces it deterministically: pointer advances 0 → 1, phase stays
SWITCH, `switch_tick` is logged with the tick value despite the refused MODE write.

**Q1 — Does the pointer advance before the MODE refusal at W=2?** **Yes.** Pointer writes 3 → 0
(succeeds, ≤ 2 sites ≤ cap 16), then the SWITCH→REMOVE MODE write is refused (21 > 16).

**Q2 — Does the next tick re-derive source/target from the new pointer and revert to COPY?**
**Yes.** At t=9715 the machine reads the live pointer (now 0), re-derives `source = 0`,
`target = 1`, finds the target slot stale (empty), and writes PHASE_COPY (7 replicas, accepted).
The phase reverts to COPY — not because the SWITCH was retried, but because the pointer had
already moved and the SWITCH branch now inspects a different, still-stale pair.

**Q3 — Is the old source's REMOVE skipped?** **Yes.** Slot 3 (the pre-switch source) is never
cleared. Occupancy trace `[slot0, slot1, slot2, slot3]` across the window:

| tick | phase | ptr | occupancy |
| --- | --- | --- | --- |
| 9714 | SWITCH | 3 | [1, 0, 0, 1] |
| 9715 | SWITCH | 0 | [1, 0, 0, 1] |
| 9716+ | COPY | 0 | [1, 1, 0, 1] (copying 0 → 1) |

Slot 3 stays occupied for the entire remaining run. By the rotation logic, the removal that
*follows* the refusal (succession n=3, `remove_tick=9790`) removes slot 0 — the slot just
vacated by the 0 → 1 switch — not slot 3. The stale duplicate in slot 3 is never removed; in this
run the pointer never completes another 3 → 0 switch before the horizon, so slot 3 is occupied at
every tick from 9714 to the end.

**Q4 — Is `switch_tick` logged on a refused transition?** **Yes, and then silently overwritten.**
At t=9714 `switch_tick` is recorded unconditionally inside `if read_pointer(o) == target` even
though the MODE write was refused (its return is discarded). When the reverted cycle later reaches
its own switch (t=9753), the same `succ._entry['switch_tick'] = now` assignment **overwrites**
9714. The final succession log entry shows `switch_tick=9753` — the spurious refused-tick stamp
is invisible in the completion log.

## The W=0 interruption case (D3 forced-succession world) — the inconsistency does NOT appear there

Running the same trace on `W_block` (damage=T, corrupt=F, forced succession at t=2400, W cut from
2400): **zero** SWITCH-phase ticks are observed at W ∈ {0, 1, 2}. `first_W_empty=2415`,
`phase_at_W_empty=COPY`, and the copy precondition is never met, so the machine never leaves COPY
and never reaches the SWITCH branch. The pointer write and the MODE write are never attempted
together, so no pointer/MODE split can occur. This is exactly AC93's G4/G5: the W=0 stall is the
pre-existing W-gated slot copy, not the write_ctrl gate.

The inconsistency is therefore **W=2-only** — specifically the narrow band where the pointer write
is affordable (≤ 2 sites) but the 21-replica MODE transition is not (cap 16). At W=0 the pointer
write itself is refused (cap 0) so the machine freezes coherently; at W=3 nothing binds (cap 24 ≥
21); only W=2 splits the two writes.

## Verdict

**The "1–2 tick delay only" explanation (AC93 E3, carried into AC93_RESULTS_v1.md §G3) is not
sustainable.** The event is not a delayed completion of the intended transition; it is a
**pointer/phase/remove inconsistency** with three concrete, reproducible symptoms:

1. **Non-atomic commit.** The pointer advance (the switch's observable effect) and the
   SWITCH→REMOVE phase transition are two separately-gated writes with different thresholds. At
   W=2 the pointer commits while the phase refuses, leaving the machine in a state its own
   state-machine encoding says cannot happen: pointer already at target, phase still SWITCH.
2. **The revert re-derives from the already-advanced pointer and skips the REMOVE.** The next tick
   reads the live pointer (not the `succ._entry` source/target), finds the new target stale, and
   reverts to COPY — so the old source's REMOVE is never executed. Slot 3 is a permanently stale
   duplicate for the rest of the run.
3. **The log masks the event.** `switch_tick` is written on the refused transition and then
   overwritten by the redo's switch, so the completion record reads as a clean single succession
   (`switch_tick=9753`) when in fact a refused switch (9714) preceded it.

**But the consequence in the observed world is benign, and the diagnosis pins why:** the switch
that "should have happened" at 9714 had already produced a valid copy at slot 0, so the pointer
moving to 0 leaves the machine in a working state; the revert-to-COPY merely starts the next slot
copy one slot early; the succession completes; the organism survives. The stale slot 3 holds a
valid duplicate and — because the damage stream only ever writes the active slot and its successor
(`run()` lines 724–732) — it is not damaged once it becomes inactive. So the skip has no
organism-level failure in the current world. It is a genuine bookkeeping defect, not a benign
delay, and it is invisible to the AC93 gates precisely because they compare *outcomes*
(near-equivalence, G3) rather than the per-tick transition sequence.

**What D2 needs to know to choose the fix:**

- The fix locus is the **split between the pointer write and the MODE write in the SWITCH branch**
  (`ac93.py` lines 463–466). Either (a) make the pointer advance and the phase transition atomic
  under the same gate (e.g. do not advance the pointer unless the MODE write is affordable; or
  check `n_mode ≤ _cap` before both writes), or (b) retain source/target in the entry across the
  refusal (do not re-derive from the live pointer every tick) so a refused REMOVE is retried
  against the same pair rather than reverted — but note (b) still leaves a window where the
  pointer and phase disagree for the one tick, and `switch_tick` must be recorded only on an
  accepted MODE write either way.
- The `switch_tick`-on-refusal defect (Q4) is a second, independent bug: it is logged
  unconditionally and then overwritten. Any fix should also record it only when the MODE write
  actually lands.
- Do not widen this into an organism-level gate: at W=0 the inconsistency cannot occur (the
  pointer write itself is refused), so the honest claim remains "W=2-only, benign in the current
  world, real in the state machine."

## Files

`AC94_D1_DIAGNOSTIC.md` (this file), `_ac94_d1_probe.py` (natural refusal scan + controlled
repro), `_ac94_d1_followup.py` (slot-occupancy + succession-log window). The frozen `ac93.py`,
`ac93_results_v1/`, and `AC93_PROTOCOL_v1.md` are untouched.
