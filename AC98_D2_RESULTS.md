# AC98-D2 — results: the revised reserve flips 4434/4435 and does no harm

Parent: AC98-D1 (`AC98_DESIGN_v1.md`). Runner `ac98.py` (new); `ac97.py` and every freeze
untouched. Engineering only — **no protocol, no freeze**. World: the AC96/AC97 relinquishment
world (`transition='perm'`, damage on, corrupt off, 16,384 ticks, move at 8192). Seeds: the
AC97 finals 4432–4435 plus the D1/D2 family 4412–4415, both histories (16 individuals).

## 0. What changed vs AC97

One change: the reserve's release gate is broadened from drop-only to three release-on-
maintained-state triggers (design §1). Arming (first productive material contact after DEV),
level (21), storage (`traces[1, 540]`, majority-read, damaged + repaired), and repair
(paid majority-restore on minority >= 2) are unchanged. The release conditions, in evaluation
order:

1. `drop`  — inside `_drop`, when material < 21 (the AC97 original).
2. `stall` — a streak increment is refused (`ac96.streak_write` returns 0 in the cur->cur+1
   branch; the only return-0 path there, since new = cur+1 != cur). Returns the 21 so the
   increment and the drop are funded.
3. `wlow`  — on a key-1 contact, available_W < 3 and material <= 64. Returns the 21 so material
   rises above 64, clearing obs bit 1 and letting the frozen priority order run W-birth
   (action 6) instead of the stale material contact (action 1).

The stall/wlow paths read organism state only (`o.body.material`, `ac4.available(o.body)`,
the maintained streak) and write `traces[1, 540]` + the material ledger. No host flag.

## 1. The flip table (per distinct seed, both histories agree)

| seed | no-reserve control        | reserve (revised)                    | release kind(s)    | no-harm |
|------|---------------------------|--------------------------------------|--------------------|---------|
| 4434 | survive, no drop (expiry) | **relinquish + survive** (was death) | stall @8221        | helps   |
| 4435 | survive, relinquish       | **survive, no drop** (was death)     | wlow @8230, stall @8299 | no harm |
| 4432 | dies 8447                 | relinquish + survive                 | drop @8208         | helps   |
| 4433 | survive, no drop          | relinquish + survive                 | drop @8198         | helps   |
| 4412 | dies 8444                 | relinquish + survive                 | drop @8224         | helps   |
| 4413 | relinquish + survive      | relinquish + survive                 | drop @8219         | tie     |
| 4414 | dies 8415                 | relinquish + survive                 | drop @8210         | helps   |
| 4415 | dies 8441                 | relinquish + survive                 | drop @8223         | helps   |

**4434 flips fully** (death -> relinquish + re-acquire + survive). Tick-by-tick (matches the
design §6 trace): 3->4 succeeds at 8220; the 4->5 increment is refused at 8221 (M=6 < 7, W=3);
the stall release returns 21 (M->27); the 4->5 increment (7) then the drop (7) are funded; the
drop fires at 8223 with the register bit set; key 1 re-acquired at 8225; the reset (14) is paid
from resumed income. `relinquishments = 1`, `completed = True`.

**4435 flips to survival, not to relinquishment** (the honest residual, recorded not hidden):
the 3->4 increment is W-bound (needs W >= 3; the phase-shifted build starts at W=2 and action 1
preempts W birth). The wlow release at 8230 clears obs bit 1 and recovers W once, but a one-shot
material release cannot hold W >= 3 through the repeated W-death window, so the streak stalls at
3, the entry expires into blind re-acquisition. `relinquishments = 0`, `completed = True`. A
later stall release (8299) returns the re-armed reserve, so the withholding is never a permanent
loss — but it cannot make the drop fire.

## 2. No-harm check (per individual; the AC97 gate-shape lesson)

```
for each (seed, history):  assert not (no_reserve.completed and not reserve.completed)
```

Passes 16/16. No distinct seed (and no individual) on which the no-reserve control survives and
the reserve arm dies. On 4435 the control survives *and* the reserve survives, so the survival
direction is preserved even where the drop does not fire. The reverse (reserve survives where
control dies) is the load-bearing direction and holds on 4432, 4412, 4414, 4415, 4434.

## 3. State sufficiency — per-tick observer-discard (unchanged)

`observer_discard_equivalence` discards the succession observer and the alloc (clearing the
vestigial host streak dict) at a mid-streak tick (streak == 2) and requires the trajectory to be
byte-identical at **every** tick. Result: `per_tick_identical = True` on all 16 individuals
(no `no_mid_streak` skips; terminal `state_hash` also identical). The reserve bit is maintained
state (`minority_end = 0` on every reserve arm), so the release conditions are pure functions of
organism state and the discard changes nothing.

## 4. Maintenance trade-off numbers

Per individual (both histories identical unless noted):

| seed | reserve_m (withheld) | reserve_released_m | reserve_writes | release kinds |
|------|----------------------|--------------------|----------------|---------------|
| 4434 | 42 (2 arms)          | 21                 | 20             | stall         |
| 4435 | 63 (3 arms)          | 42                 | 35             | wlow, stall   |
| 4432 | 42                   | 21                 | 20             | drop          |
| 4433 | 42                   | 21                 | 20             | drop          |
| 4412 | 42                   | 21                 | 21             | drop          |
| 4413 | 42                   | 21                 | 21             | drop          |
| 4414 | 42                   | 21                 | 21             | drop          |
| 4415 | 42                   | 21                 | 20             | drop          |

Interpretation: the reserve withholds a one-time 21 material (one arm at ~t 530–550, plus one or
two re-arms after re-acquisition), and its paid arm/disarm writes cost ~20–35 material total
across the run — a small fraction of the ~2290–2430 paid bank-1 repair writes in the same run.
In exchange it funds the drop (7) + reset (14) at the income-collapse threshold where the AC97
reserve starved them. On 4434 the stall release pays the increment + drop; on 4435 the wlow
release pays its own disarm and clears the obs bit. The residual armed 21 on drop seeds sits
unreleased after re-acquisition (the organism re-arms on the next productive contact) but is
benign — income has resumed and every organism completes the horizon, so there is no
permanent-loss death (the AC97 failure mode is gone).

## 5. Sizing check (task item 4)

- **Funds drop (7) + reset (14) at the threshold:** level 21 = 7 + 14. On every drop seed the
  release lands at or just before the drop and the drop (7) is paid; the reset (14) is either
  paid from the same release (drop-trigger seeds) or deferred to post-re-acquisition income
  (the stall seed 4434 and the AC97-D1 pattern — the observed, harmless deferral: streak
  temporarily stuck then self-heals). No seed dies with the streak stuck.
- **Withholding absorbed where the drop fires:** on 4432/4412/4414/4415/4434 the release is
  absorbed into the drop + reset within 3 ticks (release at 8208–8224, drop 2–3 ticks later).
- **Returned where it does not (no permanent-loss path):** on 4435 the wlow + stall releases
  return 42 of 63 withheld, and the organism survives; on every seed `reserve_released_m <=
  reserve_m` (endogenous — no external rescue), and `reserve_m > 0` (the reserve actually arms).

## 6. Consistency / control checks

- **No-reserve control byte-identical to `ac97.run` no-reserve arm:** 16/16 (`state_hash`),
  asserted by `test_ac98.py` and recorded as `control_equivalence` in `results.json`. The
  stall/wlow paths are gated on `self.reserve`, so they never disturb the rng stream or the
  frozen write order when the reserve is disabled.
- **`drop`-only release reproduces the AC97 baseline:** the revision is a strict superset of
  the release conditions, so the drop-trigger path (4432/4433/4412–4415) is byte-identical to
  AC97's reserve arm on those seeds — they relinquish + survive exactly as under AC97-D2.

## 7. What this does and does not establish

- **Established:** the reserve's release is no longer gated on the very decision it funds. It
  releases on a stall (the withholding can no longer be a permanent loss) and on W-low (the
  withholding can no longer tip the organism into the death cascade). On 4434 the stall release
  funds the starved increment and the drop fires; on every seed where the no-reserve control
  survives, the reserve arm also survives (no harm, 16/16).
- **Not established (honest residual):** the reserve does **not** make 4435's drop fire.
  4435's 3->4 increment is W-bound and a one-shot material release cannot hold W >= 3 through
  the repeated W-death window. This is a phase-shift limit of any pre-move material reserve,
  not a release-timing bug, and it is reported as a limitation — the task's literal requirement
  (drop fires on 4434/4435) is met for 4434 only.
- **Boundary (unchanged):** the reserve is a fixed minimum reserve, not an acquired allocation;
  `advance()` and `prog.choose` remain supplied format-level machinery. No autopoiesis claim.

## Files

- `ac98.py` — the runner (new; imports `ac97` for the no-reserve comparator).
- `test_ac98.py` — verification only, **not hashed** (AC17's rule).
- `ac98_d2_engineering_v1/` — `rows.jsonl` (32 rows), `results.json` (summary, per-seed table,
  control_equivalence, observer_discard). No `pre_run_snapshot.json` (no freeze).
