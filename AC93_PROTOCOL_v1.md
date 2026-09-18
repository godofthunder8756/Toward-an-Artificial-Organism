# AC93 protocol v1: coordinator transitions enacted by produced machinery — write_ctrl becomes W-gated

STATUS: **frozen before the first final seed.** Written 2026-09-18. This is a NEW architecture, not a
re-run. AC92 established the functional interruption-and-rescue of reconstruction and pinned the
W-DEPENDENT / W-INDEPENDENT split at both levels; its one residual was that the coordinator's own
transition write `write_ctrl` is W-INDEPENDENT (energy + material alone, AC88's distinct-resource
model). AC93 revokes that declaration on the NEXT architecture and measures the consequence. The
frozen AC88/AC92 rows are never edited; they are the comparator.

SOURCES (declared): ac93.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC93_PROTOCOL_v1.md

## The question and the claim

The succession coordinator's own transition write `write_ctrl` is made dependent on the same
finite-lived, autocatalytically produced W repair catalyst (bank 0, `body.life[:4]`, life 64, born by
action 6) that already enacts every other content write. The gating rule (Decision 2 of
AC93_DESIGN_v1.md, as amended by errata E2) is a field split:

1. **MODE field (bits 0-3: active + phase) — atomic, all-or-nothing, now W-gated** under
   `_cap = min(32, 8·available_W, energy, material)`. If the transition's replicas exceed `_cap`, the
   whole transition is refused (retried next tick); otherwise all mode replicas are written.
2. **LAST field (bits 4-17: start timestamp) — rate-limit BOOKKEEPING, budgeted by energy + material
   alone, never W-gated** (E2). Its succession-start write is bounded by the timestamp VALUE DELTA
   (~35-69 replicas), which `8*W=24` cannot fund; a permanently-truncated timestamp disables the
   `SUCC_MIN_SPACING` rate limiter (E1). The rate limiter's integrity is load-bearing, so the timestamp
   keeps its distinct budget.

So the honest statement (Decision 3, carried over) is: every paid write the coordinator and
reconstruction machinery performs is W-gated; the only non-W-gated paid activity is the production of
the machinery itself (the production reactions cannot be 8·W-gated without circularity — W produces W)
and the region-catalyst renewal (banks 1-2), both enacted by produced catalysts under their own
physical prerequisites.

## The three causal links, and the correction of D3's attribution (read this first)

D3's engineering observed a succession stall mid-cycle at W=0 and attributed it to the gated
`write_ctrl` refusing the COPY→VERIFY transition. **That attribution is corrected here.** A direct
probe of the ungated architecture under the same W cut (the `W_block_ungated` arm, added for D4) shows
the phase freezes IDENTICALLY: `window_ctrl_writes == 0` and `phase_changes_during_stall == 0` in both
arms. The reason is structural: in `advance()`, the COPY→VERIFY mode transition is attempted only when
the slot copy is complete (`np.array_equal(read_slot(target), src_maj)`), and the slot copy
(`write_toward_slot`) is itself W-gated — so at W=0 the copy never completes, the COPY→VERIFY transition
is never attempted, and the `write_ctrl` gate is never exercised. The stall is the pre-existing
W-dependence of the slot copy, not the new gate. The three causal links are therefore:

1. **Block production → the succession stalls while alive.** Cutting W production from the same tick
   that forces a succession depletes W to 0 mid-COPY (the copy is ~37 ticks; W empties 15-17 ticks in),
   the slot copy stops, the phase freezes at COPY (the copy precondition is never met), and the organism
   dies via the named W-loss cascade with the description intact. This is the machinery dependency of the
   succession function, observed live on a mature organism (the "interrupt an ongoing operation" test AC91
   demanded, applied to the succession).
2. **Restore the machinery → the stalled succession resumes and completes.** A machinery-only re-seed of W
   (life[:4]/pos[:4], EXTERNAL, no content touched) lets the copy resume and the succession finish from its
   frozen phase; the organism survives.
3. **The write_ctrl gate is pinned at the single-step level, and its organism-level signature is the
   near-equivalence.** With W == 0, gated `write_ctrl` MODE refuses (writes 0) while ungated writes on
   energy + material alone (unit tests). At the healthy fixed point W=3 the gate is inert (gated ≡ ungated
   on every OUTCOME); the gate binds gradedly only at W=2, where the 21-replica SWITCH→REMOVE transition
   exceeds `8*W=16` and is refused for 1-2 ticks (E3). The gate is real and pinned, but its organism-level
   effect is a graded 1-2 tick delay, not a categorical stall — because at W=0 the copy stalls first.

## The design / the interruption (carried from D3 engineering)

`force_succession(o, encoded)` induces a succession at `FORCE_TICK = 2400`: a deterministic,
damage-model-consistent pulse sets 2 replicas of the least-damaged correct-0 bit of the ACTIVE slot to 1,
guaranteeing `desc_minority_active >= DESC_TRIGGER` (2), applied BEFORE the step (the same tick's repair
runs after dm is read, so the trigger still fires). The rate limiter is open there (`last == 0` until the
first succession, so `2400 - 0 >= SUCC_MIN_SPACING`). W production (bank 0 only) is cut from the SAME tick
via `make_birth` (carried from ac92), so W depletes to 0 at 2415-2417, mid-COPY. `W_rescue` restores W at
`RESCUE_TICK = 2490` via `restore_W` (machinery-only, EXTERNAL, unit-tested); `W_block` and `W_block_ungated`
never restore.

## World, arms, seeds

World constants unchanged from AC92: PORTS=4, YIELD=64, TICKS=16384, CORRUPT_TICK=8192 (8 bits of rule 0
flipped), sticky 1e-4 damage on both banks (independent streams), DESC_TRIGGER=2, POINTER_TRIGGER=2,
CTRL_TRIGGER=2, SLOTS=4, SUCC_MIN_SPACING=2400, SUCC_BUDGET=6, REGISTER_THRESHOLD=4, the atomic MODE /
budgeted LAST controller write, the order-preserving generic-over-syntax decoder, AC75's erase-on-relinquish.
`transition='none'` (the coordinator question is about the succession, not the AC75 route move, which is
already tested in AC87/89). FORCE_TICK=2400, RESCUE_TICK=2490.

Five arms:

- `gated` — the AC93 architecture (`write_ctrl` MODE W-gated). Baseline mechanism arm.
- `ungated` — the frozen comparator (`write_ctrl` NOT W-gated; the AC88/AC92 distinct-resource model).
- `W_block` — `gated` + W production cut from FORCE_TICK, never restored.
- `W_rescue` — `gated` + W production cut from FORCE_TICK, machinery-only restore at RESCUE_TICK.
- `W_block_ungated` — `ungated` + W production cut from FORCE_TICK, never restored (the direct rival).

Condition schedule: `gated`/`ungated` sweep all four (damage × corrupt) conditions for the
near-equivalence record; `W_block`/`W_rescue`/`W_block_ungated` run on damage=True, corrupt=False only
(the succession is the sole event; corruption at t=8192 would be a second, unrelated challenge). 11
conditions per individual.

Final seeds `4400, 4401, 4402, 4403` (4 seeds × 2 histories = 8 individuals per condition, 88 rows),
disjoint from engineering 0-7 and every prior final family ≤ 4303. Engineering seeds 0-7.

## Gates (prespecified, categorical per individual)

- **G1 (baseline mechanism reconstructs).** Every `gated` (damage=T, corrupt=T) individual: `completed`
  and `flipped_still_wrong == 0` — the W-gated architecture still reconstructs the corrupted program and
  survives (the gate does not break reconstruction at W=3).
- **G2 (comparator reconstructs).** Every `ungated` (damage=T, corrupt=T) individual: `completed` and
  `flipped_still_wrong == 0`. (Runner correctness is the separate pre-final equivalence check: `ungated`
  reproduces frozen AC92 `intact` byte-for-byte, 32/32 state_hash.)
- **G3 (the gate is inert at the healthy fixed point — near-equivalence).** For every (damage, corrupt)
  condition, `gated` and `ungated` agree per individual on `completed`, `flipped_still_wrong`, and
  `description_correct`, and `successions` differs by at most 1. The state_hash divergence (the W=2
  SWITCH→REMOVE 1-2 tick delay) is reported, not gated (E3).
- **G4 (interruption stalls the succession — the COPY — while alive).** Every `W_block` (damage=T,
  corrupt=F) individual: `succession_start_observed == FORCE_TICK`, `first_W_empty` is not None,
  `phase_at_W_empty == PHASE_COPY`, `0 < copy_progress_at_W_empty < SLOT_BITS*7` (mid-copy), the slot
  copy and coordinator writes both stopped over the stall window (`window_succ_writes == 0`,
  `window_ctrl_writes == 0`), the phase froze (`phase_changes_during_stall == 0`), the succession never
  completed (`succession_completed == 0`), the description is intact at death
  (`description_correct_at_death == 130`), and the organism died (`not completed`, `W == 0`, `C == 0`).
- **G5 (the stall is the copy, NOT the gate — the direct rival).** Every `W_block_ungated` (damage=T,
  corrupt=F) individual has the SAME stall signature: `succession_start_observed == FORCE_TICK`,
  `phase_at_W_empty == PHASE_COPY`, `window_succ_writes == 0`, `window_ctrl_writes == 0`,
  `phase_changes_during_stall == 0`, `succession_completed == 0`, `description_correct_at_death == 130`,
  dies with `W == 0`, `C == 0`. Removing the gate does NOT change the stall — the gate is not the causal
  mechanism of the stall; the copy's pre-existing W-dependence is.
- **G6 (rescue resumes the succession).** Every `W_rescue` (damage=T, corrupt=F) individual: stalled
  before the rescue (`phase_at_rescue == PHASE_COPY`, `W_at_rescue == 0`, `window_succ_writes == 0`,
  `phase_changes_during_stall == 0`), then the succession completes after the rescue
  (`succession_completed == 1`, `RESCUE_TICK < succession_completion_tick < RESCUE_TICK + 80`) and the
  organism survives (`completed`, `W == 3`, `C == 2`). The rescue supplies no content by construction
  (unit-tested).
- **G7 (controls clean).** Every `gated`/`ungated` (damage=F, corrupt ∈ {T,F}) individual: `completed`
  and `flipped_still_wrong == 0` (no damage → no succession fires; corruption, when present, is
  reconstructed).
- **G8 (completeness + determinism).** Row count == seeds × 2 × 11, and a sampled exact rerun of the first
  row is byte-identical (`state_hash`). Seed disjointness and the 32/32 equivalence check are asserted in
  the audit and pre-final respectively.

## Reported, not gated

- The `gated`-vs-`ungated` **state_hash divergence** (E3, the graded W=2 SWITCH→REMOVE binding) — quantified
  per condition, never folded into G3.
- The exact `first_W_empty` tick range (measured 2415-2417 in engineering) — the gate uses
  `phase_at_W_empty == PHASE_COPY`, which is the mechanism claim; the tick range is carried as data.
- The death mechanism in `W_block`/`W_block_ungated` (the AC13 attention-hijack: obs bit 6 stays set, the
  blocked W-birth rule preempts C-birth, C dies, energy drains) — a named finding, not a gate.
- **The write_ctrl gate's W=0 refusal is pinned at the single-step level** (unit tests: gated refuses,
  ungated writes), not at the organism level — at W=0 no MODE transition is ever attempted during a
  succession (the copy stalls first), so the gate's organism-level signature is the near-equivalence (G3),
  not a categorical stall.
- Survival is a bimodality-aware lower bound (AC68 W/C collapse is seed-family dependent): the
  `gated`/`ungated`/`W_rescue` survival asserted here is on the engineering and final families, not a
  per-seed-family guarantee.
- The final priorities (recorded at freeze) are not expected to matter: the succession copies rule words
  verbatim and the corruption challenges rule 0 (a fixed word), so the mechanism is priority-independent.

## Anti-drift rules

- The runner creates `ac93_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed set.
- `test_ac93.py`, `audit_ac93.py`, `replay_ac93.py` are NOT hashed into the frozen snapshot (AC17's rule).
- Engineering seeds (0-7) are excluded from the final sample and are disjoint from the final family.
- The equivalence (declared, verified before finals): `ac93.ungated` reproduces frozen AC92 `intact`
  byte-for-byte (`state_hash`), 32/32 on AC92's final family 4300-4303 — proving the runner is a correct
  extension and the gate toggle is a no-op when disabled.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.

## Source hashes (computed before the first final seed)

    (recorded in ac93_results_v1/pre_run_snapshot.json at freeze time)
