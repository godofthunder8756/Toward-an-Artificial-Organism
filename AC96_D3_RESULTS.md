# AC96-D3 — results: relinquishment fires, observer-discard on the streak, interruption during a streak

Parent: AC96-D2 (implementation, `ac96.py`). Engineering only — **no protocol, no freeze**. Runner is
still `ac96.py` (extended with D3 instrumentation); `ac95.py`, `ac94.py`, `ac12.py` and every freeze
remain untouched. Tests in `test_ac96_d3.py` (not hashed, AC17's rule).

## 0. What was added

`_run_internal` gained three observational hooks, none of which steer a write: `swap_at` (replace the
succession observer AND the alloc — clearing the vestigial host streak dict — with fresh objects, then
rebind both in the injected step's globals), `cut_tick`/`rescue_tick` (the AC95 machinery-only W cut /
restore primitives, applied before the step so `ac4.balance` holds), and `damage_rate` (the program
stream's flip rate, default 1e-4 = frozen; stated with the majority read threshold `STREAK_THRESHOLD=4`
per AC14). New per-individual endpoints: `streak_events` (unproductive contacts only), `reacquire_ticks`,
`first_W_empty`, `streak_writes_after_cut`, `streak_at_cut`/`streak_at_rescue`, `streak_bits_at_cut`,
`streak_minority_*` (sub-majority damage), and `streak_degraded_bits_end` (a should-be-0 streak bit whose
majority later flips — damage-induced degradation of the counter's read value, separated from outcome
advance by construction). The host-streak control arm is byte-identical to D2's (the D2 suite re-passes,
11/11, 252 s).

Seeds 0 and 3 are the two individuals the D2 handoff named as the only ones where the maintained streak
relinquishes in the `perm` world; histories 0 and 1 are identical for every measurement (the runner gates
`activation=[True,True]`, so `history` is a trivial repeated measure). "Individual" below = seed; history
is reported once.

## 1. Relinquishment fires (item 1)

Per individual, the maintained streak reaches `STREAK_N`, `_drop` fires (decision register bit set, entry
erased), and the organism re-acquires (AC75):

| seed | first unproductive contact | streak progression (tick: before→after)        | drop tick | register at drop | re-acquisition tick | routes |
|------|----------------------------|-----------------------------------------------|-----------|------------------|---------------------|--------|
| 0    | 8219                       | 8219 0→1, 8220 1→2, 8221 2→3, 8222 3→4, 8223 4→5 | 8224      | True             | 8228                | [0, 1] |
| 3    | 8207                       | 8207 0→1, 8208 1→2, 8209 2→3, 8210 3→4, 8211 4→5 | 8212      | True             | 8214                | [1, 0] |

The `_drop` write sets the decision register bit to 1 (majority read True at the drop tick), erases the
memory entry (`slot_of_key -> None`), and the organism re-binds the moved key within 2–4 ticks (8228 and
8214, respectively). The "real work" equivalence holds: relinquishments == 1, not 0.

**One concrete finding surfaces in the streak progression.** The drop event reads `before=5, after=5`
(not `after=0`): the streak **reset** inside `_drop` is refused. `_drop` first writes the register bit
(≤7 replicas, affordable), then calls `streak_write(0)` to reset 5→0 (14 replicas), and that second write
is refused whole by `cap = min(32, 8W, energy, material) < 14` — material has collapsed (the perm move's
income cut), so the counter stays stuck at 5. The drop (the relinquishment decision's own write) succeeds;
the reset (a separate paid write) is starved. The stale `streak=5` is harmless here because the entry was
already erased and re-acquired, so the next productive contact resets it — but it is the D2 economic
finding (the paid streak write is starved by the very starvation it exists to pre-empt) now visible *one
write down*, on the reset rather than the increment.

## 2. Observer-discard on the streak (item 2)

At the mid-streak tick where the streak first reads 2 (8219's contact → 8221 for seed 0, 8209 for seed 3),
the runner replaces the succession observer **and** the alloc (fresh `streak={0:0,1:0}` host dict, fresh
log) and rebinds both in the injected step; the maintained bits still encode streak=2. Byte-identity is
required and holds on every individual:

| seed | swap tick | streak at swap | host dict cleared | swap applied | state_hash identical |
|------|-----------|----------------|-------------------|--------------|----------------------|
| 0    | 8221      | 2              | True              | True         | True                 |
| 3    | 8209      | 2              | True              | True         | True                 |

The streak is recovered from maintained state alone: clearing the host dict and discarding the observer at
a non-zero streak leaves the trajectory `state_hash`-identical. The `swap_applied=True` flag (plus the
non-zero `streak_at_swap`) proves the swap actually fired rather than being a silent no-op (AC95-D4's
non-vacuity discipline).

## 3. Interruption during a streak (item 3)

Cut W (machinery-only, `ac95.cut_W`) at the same mid-streak tick (streak=2, key 1's bound entry going
stale), rescue at cut+30 (`ac95.restore_W`). Per individual:

| seed | cut tick | streak at cut | cut: writes after | cut: minority end | cut: degraded bits | cut: death | rescue: streak at rescue | rescue: writes after | rescue: survives |
|------|----------|---------------|-------------------|-------------------|--------------------|------------|--------------------------|----------------------|------------------|
| 0    | 8221     | {0:0, 1:2}    | 0                 | 1                 | 0                  | 8442       | {0:0, 1:2}               | 21                   | True (W=3, C=2)   |
| 3    | 8209     | {0:0, 1:2}    | 0                 | 0                 | 0                  | 8442       | {0:0, 1:2}               | 49                   | True (W=3, C=2)   |

Three results, each clean:

1. **W-gating holds — no host-assisted drop.** `streak_writes_after_cut == 0` on both cut arms: at W=0
   every paid streak write (increment, reset) is refused whole (`_cap = min(32, 8·W, …) = 0`), and
   `relinquishments == 0` — the drop write is also W-gated, so no relinquishment fires. The cut arms die
   at 8442 (the AC91/AC92 W=0 cascade: W=0 → C dies → energy drains), with the streak frozen at its
   cut-time value 2.
2. **Degradation is sub-threshold only, at the frozen rate.** Over the ~220-tick W=0 window before death,
   the streak accumulates 0–1 damaged replicas (`streak_minority_end` 0 or 1) and **no** should-be-0 bit
   majority-flips (`streak_degraded_bits_end == 0`). The read value stays 2 throughout. This is the
   AC14/AC67 redundancy result: 7 replicas × the frozen 1e-4 stream × a ~220-tick window is far short of
   a 4-of-7 flip, so the decision state is *not* majority-perturbed before the death cascade ends the
   window. A damaged streak below threshold must not drop — and it does not (`relinquishments == 0`).
3. **The machinery-only rescue restores the correct count from maintained state.** At the rescue tick the
   streak reads `{0:0, 1:2}` — exactly its cut-time value, with no spurious advance (the frozen paid writes
   never fired) and no spurious degradation (no majority flip). Paid writes then resume
   (`streak_writes_after_cut` 21/49) and the repair cleans the sub-majority damage (seed 0's
   `streak_minority_end` returns 0; seed 3's stays 1, one surviving damaged replica, no flip).

**Distinguishing degradation from advance is by construction, not interpretation.** At W=0 the paid
`streak_write` is refused (advance = 0), so *any* change to the streak bits during the window is damage.
`streak_writes_after_cut` (advance) and `streak_minority_end`/`streak_degraded_bits_end` (degradation) are
separate counters; the cut arms show advance = 0 and degradation = 0–1 sub-majority, never confused.

**The rescue arm does not relinquish.** With the streak frozen at 2 for 30 ticks, the intervening perm-move
material collapse then starves the resumed increments (the D2 finding), so the streak never reaches 5
again and the entry expires + re-acquires blind (`streak_final` ends {0:0, 1:0}, `relinquishments == 0`).
This is the same economic limit D2 reported, now shown to be robust to a brief machinery cut+rescue: the
relinquishment decision is W-dependent *and* material-dependent, and a W cut at the critical moment
shunts the organism onto the entry-expiry path.

## 4. The degradation-vs-rate diagnostic (a confound, recorded not used)

A companion sweep (`d3_degradation_sweep`) raised the program-stream rate to try to make the W=0-window
degradation visible. It is **confounded and is not used to support item 3**:

| seed | rate | streak at cut | minority end | degraded bits | death |
|------|------|---------------|--------------|---------------|-------|
| 0    | 1e-4 | {0:0, 1:2}    | 1            | 0             | 8442  |
| 0    | 1e-3 | {0:0, 1:3}    | 8            | 1             | 8441  |
| 0    | 5e-3 | {0:7, 1:7}    | 10           | 0             | 6490 (pre-cut) |
| 3    | 1e-3 | {0:0, 1:5}    | 5            | 0             | 8416  |

At 1e-3 the streak already reads 3 or 5 *at the cut* (not 2), and at 5e-3 seed 0 dies at 6490 — before the
8221 cut — so the sweep measures pre-cut corruption, not the W=0 window. The cause is the AC61 property:
majority-restore *cements* a bit whose majority has already flipped, so a higher stream flips streak bits
faster than the (still-running, pre-cut) paid repair can prevent, and the counter is already corrupted
before W is cut. A rate sweep therefore cannot isolate "degradation under W=0" — the frozen-rate
measurement of section 3 is the only clean one, and its answer is *sub-threshold*: the streak does not
majority-degrade in the window the death cascade permits.

## 5. What this does and does not claim

All three D3 items are established on the two seeds where the maintained relinquishment fires, with the
D2 economic caveat carried forward: the internalized streak is correct and state-sufficient (recovered
from maintained state under observer-discard; W-gated; rescued by machinery alone), but it is *paid*, and
in the perm world that payment is starved by the move's income collapse — so the internalized streak
preserves the *mechanism*, not the *behaviour* (D2's headline, unchanged). The streak's own reset is
starved one write down from the drop (section 1). No content self-production claim (AC78/AC79 scope
unchanged); the streak's damage limit is the register's and program's limit (4-of-7 on a bit is
catastrophic, unrecoverable by majority-restore).
