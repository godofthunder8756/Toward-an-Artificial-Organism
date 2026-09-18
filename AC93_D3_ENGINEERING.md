# AC93-D3 engineering: the coordinator MODE transition stalls mid-cycle at W=0 and resumes on rescue — observed live

2026-09-18. Engineering only — no protocol freeze, no final seeds, no claim. `ac93.py` (seeds 0-7,
16,384 ticks). This is the discriminating test AC92 could not run: AC92 found no succession overlaps
its 48-tick window (successions are damage-triggered and ~2400-tick rate-limited), so the
W-dependent/W-independent split of the coordinator was pinned only by unit tests. AC93-D3 lands the
interruption DURING an actual succession cycle and observes the split live.

## Two design decisions made first (resolving D2's open question)

D2 handed off a broken premise: gating `write_ctrl` under `8*W=24` truncates the LAST timestamp on
every succession, disabling the `SUCC_MIN_SPACING` rate limiter (runaway successions, one death). The
design's section-5 clean-control expectation was also falsified a second way once that was fixed. Both
are now resolved and recorded as errata in `AC93_DESIGN_v1.md`:

- **E2 (Decision 2 item 2 amended): the LAST field is NOT W-gated.** The rate-limit timestamp is
  BOOKKEEPING, not a coordinator state transition; its succession-start write is bounded by the
  timestamp VALUE DELTA (~35-69 replicas), which `8*W=24` structurally cannot fund. Fix = option (b):
  MODE (active + phase) stays W-gated (atomic under `_cap`); LAST keeps the AC88 distinct-resource
  budget (energy + material alone). Rate limiter restored (6-7 successions/16,384 ticks, matching
  ungated); the ungated comparator remains byte-identical to frozen AC92 `intact` (32/32 state_hash).
- **E3 (clean control reframed): W oscillates 2↔3, so the gate binds at W=2.** The 21-replica
  SWITCH→REMOVE transition exceeds `8*W=16` whenever W dips to 2, so the gated MODE write is refused
  for 1-2 ticks. Measured: gated == ungated on ~half the individuals (8/16 damage+corrupt, 10/16
  damage only); the rest diverge only via W=2 SWITCH→REMOVE binding, traced, never structural. The
  clean control is therefore a quantified near-equivalence, not byte-identity; runner correctness is
  carried by the equivalence check (ungated == frozen AC92), which holds 32/32.

## How the interruption is landed mid-cycle

Successions are triggered by the description's own degradation signal (`desc_minority_active >=
DESC_TRIGGER=2`) AND rate-limited by `SUCC_MIN_SPACING=2400`. To pin a succession to a chosen tick:

1. **`force_succession(o, encoded)`** — a deterministic, damage-model-consistent pulse: set 2 replicas
   of the least-damaged correct-0 bit of the ACTIVE slot to 1, guaranteeing dm >= 2. Same sticky-SET
   model as the ambient stream, only scheduled rather than stochastic. Applied BEFORE the step, so
   `maintain()` reads dm >= 2 and fires the succession (the same tick's description repair runs AFTER
   dm is read, so it does not prevent the trigger). No controller content is supplied.
2. **`FORCE_TICK = 2400`** — the rate limiter is open there (`last == 0` until the first succession,
   so `2400 - 0 >= 2400`), and the organism is mature (W=3, C=2, routes held). The pulse preempts the
   natural first succession (which fires at ~2413, when ambient dm first reaches 2).
3. **W production is cut from the SAME tick** (`block_W`, bank-0 only, via `make_birth` — carried from
   ac92). W depletes naturally to 0 at 2415-2417 (measured, tight across seeds), ~15 ticks into the
   ~36-tick copy phase — mid-COPY, while the organism is alive.

`W_block` never restores W; `W_rescue` restores it at `RESCUE_TICK = 2490` via `restore_W` (AC92's
machinery-only re-seed of `life[:4]`/`pos[:4]`, labeled EXTERNAL — no description/program/pointer/
coordinator state touched, unit-tested).

## Result — uniform 16/16 (8 seeds × 2 histories, damage=True corrupt=False)

| field | W_block (16) | W_rescue (16) |
|---|---|---|
| succession_start_observed | 2400 (16/16) | 2400 (16/16) |
| first_W_empty | 2415-2417 | 2415-2417 |
| phase_at_W_empty | COPY (16/16) | COPY (16/16) |
| copy_progress_at_W_empty (of 910) | 772-789 | 772-789 |
| phase at rescue / death | COPY (at death) | COPY (at rescue) |
| copy_progress at rescue / death | 766-783 (frozen) | 766-783 (frozen) |
| phase_changes_during_stall | 0 (16/16) | 0 (16/16) |
| window succ/ctrl/reg writes | 0 / 0 / 0 (16/16) | 0 / 0 / 0 (16/16) |
| succession_completed | 0 (16/16) | 1 (16/16), tick 2549-2552 |
| outcome | dies 2622-2648, W=0 C=0 | survives, W=3 C=2 |

**The split, observed live, not in a unit test:**

- **Interruption stalls the MODE transition.** With W=0 the gated `write_ctrl` refuses the
  COPY→VERIFY mode transition (`_cap = 8*W = 0`), so the phase FREEZES at COPY — `phase_at_W_empty ==
  phase_at_rescue == 1` and `phase_changes_during_stall == 0` in every individual. The copy also
  freezes: `copy_progress` moves only 772-789 → 766-783 (a small drift from the ambient sticky damage
  stream, not from `write_toward_slot`, which is also W-gated). Every W-catalyzed write is zero over
  the stall window (succ/ctrl/reg = 0).
- **This is "stalled mid-copy", not "phase advanced but content stale".** The phase did NOT advance
  (stuck at COPY) and the content did NOT go stale (copy progress frozen, not degraded). The AC92
  split — "which coordinator operations stop and which continue" — is now visible at the organism
  level: the MODE transition stops, and nothing else advances, because every paid write on the
  reconstruction/coordination path is W-gated.
- **Rescue resumes it.** After `restore_W` (machinery only), the succession resumes from its frozen
  COPY phase and completes (tick 2549-2552) in all 16 individuals, which survive with W=3, C=2. The
  blocked arm never completes and dies via the named attention-hijack cascade (W=0 → C=0 → energy
  drain), 2622-2648.

## What is carried forward to D4 (protocol + gates)

1. The interruption timing is now a settled mechanism, not a finding: force at `FORCE_TICK=2400`, cut
   W from the same tick, rescue at `RESCUE_TICK=2490`; `first_W_empty` lands 2415-2417 mid-COPY in all
   individuals. A protocol can gate on `first_W_empty <= 2436` (before copy completion) per individual.
2. The clean control is a **quantified near-equivalence** (E3), not byte-identity: gate on the
   equivalence check (ungated == frozen AC92) for runner correctness, and report gated-vs-ungated as
   "identical except W=2 SWITCH→REMOVE binding, traced and bounded".
3. The load-bearing control (`no_repair`, cut via `no_policy_write`) is still D4's call, as the
   design deferred it; the runner retains the `ac_arm`/`cut` plumbing to add it without structural
   change.
4. The `W=0 ⇒ MODE refused` gate was already pinned by unit tests (test_ac93.py, 12/12 passing);
   D4 freezes the arm set, gates, and disjoint final seeds.

## Files

- `ac93.py` — E2 write_ctrl fix; new arms `W_block`/`W_rescue`; `force_succession`, `make_birth`,
  `restore_W`; `collect_d3` (`--d3-engineering`).
- `test_ac93.py` — 12 tests (arm config incl. D3 arms, W=0 MODE gate, LAST W-independence, low-bit-
  first truncation, force_succession, restore_W machinery-only, make_birth bank-0-only).
- `AC93_DESIGN_v1.md` — errata E2 and E3 appended.
- `ac93_d3_engineering_v1/` — 160 rows, pre_run_snapshot.json, results.json (frozen, `mkdir(exist_ok=False)`).
