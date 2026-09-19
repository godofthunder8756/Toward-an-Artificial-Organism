# AC95 protocol v1: state sufficiency — the trajectory is carried by maintained state alone

STATUS: **frozen before the first final seed.** Written 2026-09-18. This is the protocol + finals for
AC95-D4, the last step of the AC95 state-sufficiency line. AC95-D1 audited every persistent host
variable on the AC94 operational control path and found exactly two class-C leaks: the succession
timer's `timer_reset_done` host flag and `alloc.streak`. AC95-D2 closed the first by moving the
reset-progress flag into the organism's own vulnerable, paid-maintained state as a single
reset-in-progress (RIP) bit in the CTRL register's spare bit 17, and made the succession observer
strictly observational. AC95-D3 built the machinery to interrupt the multi-tick counter RESET
mid-way (a direct W cut, the mirror of the AC92 direct W restoration) and rescue it machinery-only,
and showed in engineering that the observer-discard at the rescue tick (mid-reset, mid-succession)
is byte-identical. This protocol freezes that claim: **the organism's trajectory is fully determined
by its vulnerable, maintained internal state plus the environment — no host-side operational memory
steers it.**

SOURCES (declared): ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC95_PROTOCOL_v1.md

## The question and the claim

AC94 froze the coherent resumable succession; AC95 asks the deeper question of whether the machinery
that enacts it depends on host-side operational memory. The decisive test is **observer-discard
equivalence**: preserve the organism's maintained state, discard the host's observational history
(replace the succession observer with a fresh object), resume, and the organism continues correctly —
byte-identical trajectory (`state_hash`). The claim is that the fixed architecture satisfies this
for every individual, at two discard points: **during an active succession** (mid-COPY, the ordinary
case) and **mid-reset** (the strongest point — the counter is part-way cleared, a succession is in
progress, and the machinery has just been restored). The claim further requires that a mid-reset
machinery cut freezes the reset (no host-assisted completion) and a machinery-only rescue resumes it
from maintained state alone. The comparator arms (the `split` rival, the frozen `ungated` comparator,
the `ungated_block` under-cut rival) prove the fixes are the only changes.

The gates (prespecified, categorical per individual):

1. **G1 state sufficiency (observer-discard equivalence).** Every final individual: the `gated`
   trajectory with the observer discarded at `succ_start + MID_SUCC_OFFSET` (mid-COPY, during an
   active succession) is byte-identical (`state_hash`) to the undisturbed `gated` run; and the
   `reset_rescue` trajectory with the observer discarded at the rescue tick (mid-reset) is
   byte-identical to the undisturbed `reset_rescue` run.
2. **G2 reset interruption + resume.** Every final individual: `reset_block` froze the reset part-way
   (`0 < reset_progress_at_cut < TIMER_MAX`), never completed it without W (`reset_completed_tick is
   None` — no host memory completes it), completed no succession, and died; `reset_rescue` froze, then
   completed the reset after the machinery-only rescue (`reset_completed_tick > reset_start +
   RESET_CUT_OFFSET`), survived, and completed a healthy rate-limited succession count (`>= 4`).
3. **G3 coherence carry-forward.** Every final individual re-derives AC94's four requirement-gates on
   the AC95 arms: correct source preservation, verified successor activation (atomic switch), correct
   old-source removal (`gated`, damage=T corrupt=T), and rate limiting across interruptions
   (`timer_block` freezes at W=0 with no runaway; `timer_rescue` resumes to a healthy count). The
   RIP-bit fix is behaviour-preserving.
4. **G4 completeness + determinism.** Row count == seeds × 2 × 17, and a sampled exact rerun of the
   first row is byte-identical (`state_hash`).

Plus **logs-observational** (a single-step pin, reported alongside G1): no branch reads back a log
field. `test_ac95.py` asserts at the single-step level that an identical idle state produces the same
write whether the observer is cleared, kept, or carries a stale host flag — the class-C leak is
closed. G1 is the whole-trajectory version of the same assertion.

## The mechanism (what changed, and why)

- **D2 — the RIP bit.** The reset-progress flag (`succ._entry['timer_reset_done']`) is moved into
  maintained state as CTRL bit 17 (`RIP_OFFS`), written 1 at succession start and 0 when the counter
  first reads 0. It is inside `CTRL_OFFS`, so the ambient bank-1 damage stream reaches it and
  `reg_ctrl` repairs it. The write is atomic and W-gated like the MODE field (`write_rip`, paid 1
  energy + 1 material per replica, refused whole at W=0). The fixed architecture (`gated` +
  `timer_block`/`timer_rescue`/`reset_block`/`reset_rescue`) uses `timer_maintained=True`; the
  `split` rival and the `ungated`/`ungated_block` comparators keep the frozen host-flag / timestamp
  behaviour by construction (`timer_maintained=False`).
- **D3 — reset interruption.** `cut_W` (zero `body.life[:4]`, machinery-only, EXTERNAL) freezes a
  W-gated write mid-flight; `restore_W` (re-seed `life[:4]`/`pos[:4]`, machinery-only, EXTERNAL)
  resumes it. The cut/restore schedule is state-detected from the organism's own RIP bit (0→1
  transition), not a host tick: cut at `reset_start + RESET_CUT_OFFSET`, restore at `reset_start +
  RESET_RESCUE_OFFSET`.
- **D4 — no new mechanism.** The observer-discard hook already exists (`swap_succ_at`); D4 adds the
  mid-succession discard point (`swap_succ_at='mid_succession'` = `succ_start + MID_SUCC_OFFSET`) and
  freezes the gates. Nothing about the organism changes in D4.

## World, arms, seeds

World constants unchanged from AC94: PORTS=4, YIELD=64, TICKS=16384, CORRUPT_TICK=8192 (8 bits of
rule 0 flipped), sticky 1e-4 damage on both banks (independent streams), DESC_TRIGGER=2,
POINTER_TRIGGER=2, CTRL_TRIGGER=2, SLOTS=4, SUCC_BUDGET=6, REGISTER_THRESHOLD=4, the order-preserving
generic-over-syntax decoder, AC75's erase-on-relinquish. `transition='none'` (no route move; the
coordinator question is about the succession and its state sufficiency, not the AC75 route move).
TIMER_BITS=13, TIMER_K=200, TIMER_BLOCK_TICK=1000, TIMER_RESCUE_TICK=1100, RESET_CUT_OFFSET=2,
RESET_RESCUE_OFFSET=40, MID_SUCC_OFFSET=10.

Eight arms:

- `gated` — the fixed architecture (atomic switch + W-funded timer + RIP bit). Baseline mechanism arm.
- `split` — the AC93 gated rival (two-step switch, host reset flag). Direct rival for the atomicity
  fix (G3).
- `ungated` — the frozen comparator (write_ctrl NOT W-gated, timestamp rate limiter). Byte-identical
  to frozen AC92 `intact` (equivalence check).
- `ungated_block` — the AC93 ungated-under-cut rival: `ungated` + the same W cut.
- `timer_block` / `timer_rescue` — `gated` + the W cut (machinery-block vs machinery-rescue; the
  `timer_rescue` re-seed is EXTERNAL and labeled a diagnostic).
- `reset_block` / `reset_rescue` — `gated` + the mid-reset W cut (freeze vs machinery-only rescue).

Condition schedule: `gated`/`split`/`ungated` sweep all four (damage × corrupt) conditions for the
coherence record; `ungated_block`/`timer_block`/`timer_rescue`/`reset_block`/`reset_rescue` run on
damage=True, corrupt=False only (the rate limiter, and the counter reset, are each the sole event;
corruption at t=8192 would be a second, unrelated challenge). 17 conditions per individual.

Final seeds `4408, 4409, 4410, 4411` (4 seeds × 2 histories = 8 individuals per condition, 136 rows),
disjoint from engineering 0-7 and every prior final family ≤ 4407 (and the separate 4600-4871
order-line families and the 5100-5507 confirmatory families). Engineering seeds 0-7.

## Gates (prespecified, categorical per individual)

- **G1 (state sufficiency).** Every individual: `gated` with `swap_succ_at='mid_succession'` is
  byte-identical to `gated` undisturbed, and `reset_rescue` with `swap_succ_at='rescue'` is
  byte-identical to `reset_rescue` undisturbed (both `state_hash`).
- **G2 (reset interruption + resume).** Every `reset_block` (damage=T, corrupt=F) individual:
  `reset_froze`, `0 < reset_progress_at_cut < TIMER_MAX`, `reset_completed_tick is None`,
  `successions == 0`, `not completed`. Every `reset_rescue` (damage=T, corrupt=F) individual:
  `reset_froze`, `reset_completed_tick is not None` and `> reset_start + RESET_CUT_OFFSET`,
  `completed`, `successions >= 4`.
- **G3 (coherence carry-forward).** Every `gated` (damage=T, corrupt=T) individual: `successions >= 1`,
  `source_intact_at_switch_all`, `verified_all`, `split_events == 0`, `removal_all`,
  `occupied_slots_end <= 2`. Every `timer_block` individual: `first_W_empty is not None`,
  `timer_at_W_empty < TIMER_MAX`, `timer_increments_after_W_empty == 0`, `successions == 0`,
  `not completed`, `W == 0`. Every `timer_rescue` individual: `first_W_empty is not None`,
  `timer_increments_after_W_empty == 0`, `1 <= successions <= 8`, `completed`, `W >= 3`.
- **G4 (completeness + determinism).** Row count == seeds × 2 × 17, and a sampled exact rerun of the
  first row is byte-identical (`state_hash`).

## Reported, not gated

- The `split` rival's `split_events` count and `occupied_slots_end` — the D1 defect is W=2-during-
  SWITCH and seed-dependent (AC39), so it is reported per individual, never a per-individual gate;
  its single-step form is pinned by `test_ac95.py`.
- The `ungated_block` rival's rate-limiter contrast (its timestamp is NOT frozen by W=0; the
  succession still stalls at the W-gated copy) — pinned at the single-step level, reported, not gated.
- The coherence fields (`source_intact_at_switch_all`, `verified_all`) are recorded only on the
  `gated`/`split` arms (which pass through the instrumented switch branch); the frozen `ungated`
  comparator's two-step switch does not record them, so its rows read False there by construction.
- Survival is a bimodality-aware lower bound (AC68 W/C collapse is seed-family dependent): the
  observed survival counts are reported, not a per-seed-family guarantee. `reset_block` is expected
  to die (the frozen reset cannot complete without W); `reset_rescue` survives inside the safe rescue
  window (RESET_RESCUE_OFFSET=40, swept 20-40 → 16/16 in engineering).
- The final priorities `[0,3,2,1]`, `[1,2,3,0]`, `[1,2,0,3]`, `[2,0,1,3]`: seed 4408's `[0,3,2,1]`
  ranks bank-1 renewal last (the AC83 adversarial pattern in spirit), but the succession copies rule
  words verbatim and the corruption challenges rule 0 (a fixed word), so the mechanism is
  priority-independent — recorded as a scope note, not a gate.
- `alloc.streak` (the second D1 class-C leak) remains deferred: inert in the finals
  (`transition='none'` leaves no stale route), and its fix would change the byte-identity comparator
  digests. The state-sufficiency claim does not cover it until it is closed (flagged, not silent).

## Anti-drift rules

- The runner creates `ac95_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed set
  (which includes this protocol file).
- `test_ac95.py`, `audit_ac95.py`, `replay_ac95.py` are NOT hashed into the frozen snapshot (AC17's
  rule).
- Engineering seeds (0-7) are excluded from the final sample and are disjoint from the final family.
- The equivalence (declared, verified before finals): `ac95.ungated` reproduces frozen AC92 `intact`
  byte-for-byte (`state_hash`), 32/32 on AC92's final family 4300-4303; `ac95.split` reproduces frozen
  AC94-D4 `split` byte-for-byte, 32/32 on 4404-4407 — proving the runner is a correct extension and
  the RIP-bit fix is applied only to the fixed architecture.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.

## Source hashes (computed before the first final seed)

    (recorded in ac95_results_v1/pre_run_snapshot.json at freeze time)
