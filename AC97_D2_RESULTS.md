# AC97-D2 — an internal minimum resource reserve for completing relinquishment

Engineering only. No protocol, no freeze. Runner `ac97.py`; `ac96.py` and every freeze
untouched. Seeds 4412–4415 (the D1-named family), histories 0 and 1, `transition='perm'`.

## Verdict (one line)

The reserve **funds the relinquishment**: the drop's register write (7 replicas) and the
streak reset (14 replicas) are accepted where they were refused, and the maintained arm's
relinquishment count rises from **2/8 to 8/8** with **8/8 survival** — without external
rescue, and without measurably harming ordinary maintenance.

## What the reserve is

A **single maintained-state bit** (`traces[1, 540]`, a free bank-1 region; slots 0–519,
pointer 520–521, CTRL 522–539 are occupied) holding "armed (1) / disarmed (0)". When armed,
`RESERVE_LEVEL = 21` material units are withheld from the organism's spendable pool.

- **Accumulation (arm).** On the first productive *material* contact after development
  (`t >= 512`), the organism withholds 21 material from that contact's intake: it reduces
  `b.material` and `e['in_m']` by 21 and sets the bit (a paid, W-gated, atomic write). The
  reserved material is *not in `b.material`*, so no lower-priority write (repair,
  reconstruction, renewal, births, succession) can reach it. `ac4.balance`'s identity
  `b.material == M + in_m - overflow_m - spent_m` holds by construction because `in_m` is
  a variable (the AC15 primitive), and the `spent_m == writes + 4·(W_birth+C_birth) +
  2·B_birth` identity is untouched.
- **Withholding.** The reserved 21 units sit outside the spendable pool. This is the
  reviewer's "withheld from lower-priority work": the reserve is removed from `b.material`,
  not a floor on it. (A literal floor `b.material >= R` cannot work here — material income
  is gated on `observe` bit 1, `material <= 64`, so any floor > 64 silences the very contact
  that detects the stale route; a floor <= 64 is inert because the decision chain needs 77
  material but only ~53–57 is present at the first increment. The separate store is the
  only representation that both preserves the income loop and funds the drop.)
- **Release.** In `_drop`, when `material < RESERVE_LEVEL` (i.e. the pool cannot cover the
  drop's 7 + the reset's 14), the reserve is released: `b.material += 21`, `e['in_m'] += 21`
  (the reverse of arming), and the bit is cleared (paid). The drop and reset then spend
  against the augmented pool.
- **Damage + repair.** The bit is damaged by the same sticky bank-1 stream and repaired by a
  paid majority-restore (`reg_reserve`, minority >= 2), like the pointer/CTRL. It is
  genuinely vulnerable: `minority_end = 0` in every run, so it never reads spuriously.
- **Internal, not host state.** The arm/release read and write `traces[1, 540]` only. No
  host dict/flag. The `AllocEraseReserve` object holds `reserve_events` as a log only.
- **No external rescue.** The ledger records `reserve_m = 42` (two arm events x 21) and
  `reserve_released_m = 21` (one release), netting 21 still held at end-of-run
  (`reserve_armed_end = 1`) — the standing reserve for the next move. Every released unit
  was previously withheld from the organism's own income.

## D1-shortfall closure (per individual, both histories identical)

| seed | arm        | drop tick (reg bit) | reset | reacq(1) | survival | relinquish |
|------|------------|---------------------|-------|----------|----------|------------|
| 4412 | no-reserve | **never** (M=4<7)   | never | —        | dies 8444 | 0 |
| 4412 | reserve    | 8224 (True)         | yes   | 8226     | survives | 1 |
| 4413 | no-reserve | 8206 (yes, M=8)     | **refused M=1<14** | by expiry | survives | 1 |
| 4413 | reserve    | 8219 (True)         | yes   | 8220     | survives | 1 |
| 4414 | no-reserve | **never** (M=3<7)   | never | —        | dies 8415 | 0 |
| 4414 | reserve    | 8210 (True)         | yes   | 8211     | survives | 1 |
| 4415 | no-reserve | **never** (M=6<7)   | never | —        | dies 8441 | 0 |
| 4415 | reserve    | 8223 (True)         | yes   | 8225     | survives | 1 |

- No-reserve (the frozen ac96 maintained arm): 2/8 relinquish (4413 only), 2/8 survive.
- Reserve: **8/8 relinquish, 8/8 survive**, every drop followed by re-acquisition of key 1
  within 1–3 ticks and a healthy W=3, C=2, both routes bound at end-of-run.
- The 4413 row closes the *reset* refusal (D1's "survivor-only" story); the other three close
  the *drop* refusal (D1's decisive shortfall). Both are the same reserve release: the 21
  units cover the 7-replica register write and the 14-replica reset at the same threshold.

## Maintenance trade-off (harms vs merely delays)

Measured at the move tick (t=8192), before any drop, where both arms are alive and differ
only by the reserve's one-time 21-unit withholding:

| seed | arm        | W/C/B births | reg/succ/ctrl writes |
|------|------------|--------------|----------------------|
| 4412 | no-reserve | 764/127/834  | 1164/1331/838        |
| 4412 | reserve    | 764/128/835  | 1170/1332/839        |
| 4414 | no-reserve | 764/128/837  | 1155/1343/838        |
| 4414 | reserve    | 764/127/836  | 1171/1343/835        |
| 4415 | no-reserve | 764/128/838  | 1178/1331/842        |
| 4415 | reserve    | 764/127/838  | 1149/1333/841        |

The 21-unit withholding is **absorbed by the material cycle's slack** (material oscillates
37–128 on a 64-unit contact cycle), not converted into fewer births or writes: W/C/B births
and reg/succ/ctrl writes are within ±2 of the no-reserve arm at the move tick. The
withholding **merely shifts the material-cycle phase** (the reserve arm's drop lands a few
ticks later, 8210–8224 vs 8206), it does not degrade maintenance. The large end-of-run gap
in births (764 vs 1532 W, 128 vs 255 C) is entirely the *survival* effect — the no-reserve
seeds stop maintaining at death (~8440), the reserve seeds keep producing to the horizon
and match the no-reserve survivor (4413: 1532/255/~1674) field-for-field.

## Observer-discard (per-tick, the review's correction #1)

`observer_discard_equivalence()` now compares the **per-tick trajectory digest**, not just
the terminal state_hash. At a mid-streak tick (streak == 2, key 1), the succession observer
AND the alloc (clearing the vestigial host streak dict) are replaced with fresh objects and
the run resumes. Result: **8/8 individuals byte-identical at every one of 16,384 ticks**
(first divergence `null`), with the terminal state_hash equality kept as a regression. The
streak and the reserve are recovered from maintained state alone.

## What this does and does not establish

- **Established:** the internalized relinquishment decision can be made *affordable* by an
  internally enforced, paid, vulnerable reserve — the AC96-D4 "economically fragile" gap
  closes without any host state or external resource.
- **Not established:** the reserve is a *standing* minimum reserve (armed whenever income
  flows, released on demand). It is not a demonstrated *decision* about how much to save —
  `RESERVE_LEVEL = 21` is a declared world constant sized to the drop (7) + reset (14), and
  the trigger is the fixed "material < 21" shortfall test, not an acquired allocation. That
  is the next, separate question (AC96-D4's open item, one level up).
- The two-arm divergence begins at the first arm write (~t=513–545), i.e. the reserve and
  no-reserve arms are byte-identical up to the first post-development productive material
  contact, as the no-reserve reproduction (8/8 state_hash equal to ac96's maintained arm)
  guarantees.

## Files

- `ac97.py` — the runner (reserve toggle; no-reserve control reproduces ac96 byte-for-byte).
- `ac97_d2_engineering_v1/` — rows.jsonl + results.json (8 individuals x 2 arms).
- `_ac97_d2_probe.py`, `_ac97_d2_sizing.py`, `_ac97_d2_tradeoff.py` — measurement scratch
  (material trajectory, pre-move ceiling, maintenance-at-move comparison).
