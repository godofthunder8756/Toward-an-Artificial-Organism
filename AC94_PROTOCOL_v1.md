# AC94 protocol v1: coherent, resumable succession under produced-machinery limits

STATUS: **frozen before the first final seed.** Written 2026-09-18. This is a NEW architecture, not a
re-run. AC93 revoked the coordinator transition write's W-independence (`write_ctrl` MODE becomes
W-gated) but left two residuals that its near-equivalence framing masked: (D1/D2) at W=2 the SWITCH
branch performed the pointer write and the SWITCH→REMOVE MODE write as two separately-gated writes, so
the pointer advanced while the 21-replica MODE transition was refused, the next tick re-derived
source/target from the advanced pointer and reverted to COPY, and the old source's REMOVE was
permanently skipped — a pointer/phase/remove inconsistency, not "a 1-2 tick delay only"; and (D3) the
rate limiter's start timestamp was funded by energy + material alone (the AC88 distinct-resource model),
whose 35-69-replica value delta is structurally unbounded by the W cap, so a W-gated timestamp would be
permanently truncated and the rate limiter would run away (E1). AC94 fixes both: D2 makes the pointer
advance and the MODE commit one atomic multi-field transition (`commit_switch`), and D3 replaces the
timestamp with a bounded, resumable, W-funded unary counter. This protocol freezes the fixed
architecture and measures the four requirement-gates of a **coherent resumable succession**, against the
direct rival controls. The frozen AC88/AC92/AC93 rows are never edited; they are the comparators.

SOURCES (declared): ac94.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC94_PROTOCOL_v1.md

## The question and the claim

A succession that transfers the recipe from the active slot to a successor must be **coherent** (the
source is preserved while the successor is built; the pointer switches only after the successor is
verified valid and equal to the source, atomically with the MODE commit; the old source is actually
cleared after the switch) and **resumable** (the rate limit is enforced by machinery that survives
interruption and rescue — no runaway, no hidden W-independent service). The claim is that the fixed
architecture satisfies all four requirement-gates, and that the two rivals that remove one fix each
(the `split` rival removes the atomicity fix; the `ungated`/`ungated_block` rivals remove the W-gating
of the coordinator write and of the rate limiter) fail the corresponding coherence property.

The four requirement-gates (prespecified, categorical per individual):

1. **G1 correct source preservation** — the copy leaves the source intact while the successor is built:
   every completed succession in every `gated` individual reads the source slot intact at the switch
   (`source_intact_at_switch == 1`), and the succession's own writes never target the source slot (the
   copy is strictly source→target; pinned at the single-step level in `test_ac94.py`).
2. **G2 verified successor activation** — the pointer switches only after the successor decodes valid
   AND matches the source (the AC86/87 verify gate), and the pointer/MODE transition is atomic: every
   completed succession has `verified_valid == 1` and `target_matches_source == 1`, and
   `split_events == 0` (no tick where the pointer advanced while the MODE transition was refused).
3. **G3 correct old-source removal** — the old source is actually cleared after the switch, not skipped:
   every completed succession has `old_source_empty == 1`, and no stale slot remains
   (`occupied_slots_end <= 2` — the active slot plus at most one successor under construction).
4. **G4 rate limiting across interruptions** — the succession remains rate-limited even when the timing
   machinery is interrupted and rescued: in `timer_block` the W-funded counter freezes at W=0 (zero
   increments after `first_W_empty`, `timer_at_W_empty < TIMER_MAX`, `successions == 0` — no runaway),
   and in `timer_rescue` the counter froze before the rescue and then resumed, completing a healthy
   rate-limited count (`1 <= successions <= 8`, not the E1 runaway 86-137).

Plus **G5 (bookkeeping)** — row count == seeds × 2 × 15 and a sampled exact rerun is byte-identical
(`state_hash`).

## The mechanism (what changed, and why)

- **D2 — atomic switch.** `commit_switch(o, e, target, last)` advances the pointer AND commits the
  SWITCH→REMOVE MODE transition as ONE atomic multi-field transition, refused together iff
  `n_mode > 8·W` or `n_ptr > 8·W` or `n_ptr + n_mode > energy` or `n_ptr + n_mode > material`. On
  refusal NOTHING is written — the pointer does not advance alone, the next tick retries the same
  source/target pair re-derived from the unchanged pointer. `switch_tick` (and `copy_done`,
  `remove_tick`/`done`) are recorded only on the write's actual commit. The naive combined sum
  (`n_ptr + n_mode <= _cap`) is wrong: it exceeds the per-write cap 8·W=24 at W=3 and deadlocks.
- **D3 — W-funded unary counter rate limiter.** The CTRL register's former LAST field holds a unary
  counter (`TIMER_BITS=13`), counting up from 0 (the natural all-zero state) to `TIMER_MAX`; the
  succession may fire only when it is full. Each `TIMER_K=200` host ticks one bit is set (atomic, ≤7
  replicas, W-gated); a succession start resets it to 0 (resumable, monotone clear, W-gated). No
  energy+material-only write service remains for the rate limiter — the E1 "permanently truncated
  timestamp" mode is structurally gone.

## The interruption (machinery-dependence of the timer)

Bank-0 W production is cut from `TIMER_BLOCK_TICK = 1000` (via `make_birth`, bank 0 only, content never
touched), so W depletes naturally to 0 ~63 ticks later; the counter can no longer advance (W-gated
increment refuses whole at W=0). `timer_rescue` re-seeds the W catalyst at `TIMER_RESCUE_TICK = 1100`
(`restore_W`: `life[:4]`/`pos[:4]` only, EXTERNAL, no content touched) so the counter resumes and a
succession completes. There is no forced succession — the timer arms cut W during the counter's first
count-up, before any succession has fired; the rate limiter is the sole event.

## World, arms, seeds

World constants unchanged from AC92/AC93: PORTS=4, YIELD=64, TICKS=16384, CORRUPT_TICK=8192 (8 bits of
rule 0 flipped), sticky 1e-4 damage on both banks (independent streams), DESC_TRIGGER=2,
POINTER_TRIGGER=2, CTRL_TRIGGER=2, SLOTS=4, SUCC_BUDGET=6, REGISTER_THRESHOLD=4, the order-preserving
generic-over-syntax decoder, AC75's erase-on-relinquish. `transition='none'` (the coordinator question
is about the succession, not the AC75 route move, which is already tested in AC87/89). TIMER_BITS=13,
TIMER_K=200, TIMER_BLOCK_TICK=1000, TIMER_RESCUE_TICK=1100.

Six arms:

- `gated` — the fixed architecture (D2 atomic switch + D3 W-funded timer). Baseline mechanism arm.
- `split` — the AC93 gated rival: W-gated MODE + W-funded timer, but the SWITCH branch does the AC93
  two-step (write_pointer then write_ctrl separately, `switch_tick` logged unconditionally). At W=2 the
  pointer advances while the 21-replica MODE transition is refused — it still exhibits the D1
  pointer/phase split. Direct rival for G2/G3.
- `ungated` — the frozen comparator (write_ctrl NOT W-gated, the AC88/AC92 distinct-resource timestamp
  rate limiter, the two-step switch). Byte-identical to frozen AC92 `intact` (equivalence check).
- `ungated_block` — the AC93 ungated-under-cut rival: `ungated` + the same W cut. Its rate limiter is
  the W-independent timestamp (NOT frozen by W=0), but the succession still stalls at the W-gated copy.
- `timer_block` — `gated` + the W cut, never restored (machinery-block).
- `timer_rescue` — `gated` + the W cut, machinery-only restore at t=1100 (machinery-rescue; the re-seed
  is EXTERNAL and labeled a diagnostic, not a result).

Condition schedule: `gated`/`split`/`ungated` sweep all four (damage × corrupt) conditions for the
coherence record; `ungated_block`/`timer_block`/`timer_rescue` run on damage=True, corrupt=False only
(the rate limiter is the sole event; corruption at t=8192 would be a second, unrelated challenge). 15
conditions per individual.

Final seeds `4404, 4405, 4406, 4407` (4 seeds × 2 histories = 8 individuals per condition, 120 rows),
disjoint from engineering 0-7 and every prior final family ≤ 4403 (and the separate 4600-4871 order-line
families). Engineering seeds 0-7.

## Gates (prespecified, categorical per individual)

- **G1 (source preservation).** Every `gated` (damage=T, corrupt=T) individual: `successions >= 1` and
  `source_intact_at_switch_all` (every completed succession left the source intact at the switch).
- **G2 (verified activation).** Every `gated` (damage=T, corrupt=T) individual: `successions >= 1`,
  `verified_all` (every completed succession decodes valid AND matches the source), and
  `split_events == 0` (the switch was atomic — no pointer advance without the MODE commit).
- **G3 (correct removal).** Every `gated` (damage=T, corrupt=T) individual: `successions >= 1`,
  `removal_all` (every completed succession cleared its old source), and `occupied_slots_end <= 2`
  (no stale slot).
- **G4 (rate limiting across interruptions).** Every `timer_block` (damage=T, corrupt=F) individual:
  `first_W_empty` is not None, `timer_at_W_empty < TIMER_MAX`, `timer_increments_after_W_empty == 0`,
  `successions == 0`, `not completed`, `W == 0`. Every `timer_rescue` (damage=T, corrupt=F) individual:
  `first_W_empty` is not None, `timer_increments_after_W_empty == 0`, `1 <= successions <= 8`,
  `completed`, `W >= 3`.
- **G5 (completeness + determinism).** Row count == seeds × 2 × 15, and a sampled exact rerun of the
  first row is byte-identical (`state_hash`).

## Reported, not gated

- The `split` rival's `split_events` count (the D1 defect exercised) and its `occupied_slots_end` —
  reported per individual, never a per-individual gate (the defect is W=2-only and seed-dependent).
- The `ungated_block` rival's rate-limiter contrast (its timestamp is NOT frozen by W=0; the succession
  still stalls at the copy) — pinned at the single-step level, reported, not gated.
- The `gated`-vs-`ungated` succession-count difference (6 vs 6-7, the coarse-timer quantisation of the
  spacing to 2400-2600 ticks) — a declared property, not a defect.
- The coherence fields (`source_intact_at_switch_all`, `verified_all`) are recorded only on the
  `gated`/`split` arms (which pass through the instrumented switch branch); the frozen `ungated`
  comparator's two-step switch does not record them, so its rows read False there by construction.
- Survival is a bimodality-aware lower bound (AC68 W/C collapse is seed-family dependent): the
  `gated`/`split`/`ungated`/`timer_rescue` survival asserted here is the observed count, not a
  per-seed-family guarantee.
- The final priorities (recorded at freeze) are not expected to matter: the succession copies rule words
  verbatim and the corruption challenges rule 0 (a fixed word), so the mechanism is priority-independent.

## Anti-drift rules

- The runner creates `ac94_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed set
  (which includes this protocol file).
- `test_ac94.py`, `audit_ac94.py`, `replay_ac94.py` are NOT hashed into the frozen snapshot (AC17's rule).
- Engineering seeds (0-7) are excluded from the final sample and are disjoint from the final family.
- The equivalence (declared, verified before finals): `ac94.ungated` reproduces frozen AC92 `intact`
  byte-for-byte (`state_hash`), 32/32 on AC92's final family 4300-4303 — proving the runner is a correct
  extension and that the atomic-switch / gate toggles are no-ops when disabled.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.

## Source hashes (computed before the first final seed)

    (recorded in ac94_results_v1/pre_run_snapshot.json at freeze time)
