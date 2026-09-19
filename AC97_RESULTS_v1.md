# AC97 results v1: an unconditional adaptation criterion on unseen seeds — the reserve does NOT afford self-preservation (G1 falsified)

Parent: AC97-D2 (engineering). Frozen per `AC97_PROTOCOL_v1.md` (hashed before the first final seed).
Runner `ac97.py`; seeds **4432-4435** × 2 histories, 16 rows, 16,384 ticks, `transition='perm'` (the
relinquishment world). Two arms per individual: `reserve` (the internal minimum material reserve) and
`no_reserve` (the frozen ac96 maintained arm, byte-identical to `ac96.run(..., streak_maintained=True)`
— the direct control). The final family is **unseen**: no screening, disjoint from engineering 0-7, from
the D1/D2 seeds 4412-4415, from the AC96 screening sweep 4412-4431, and from every prior final family.

## Verdict

**The claim is falsified on the unseen family.** The D2 engineering result (8/8 relinquish + 8/8
survive on seeds 4412-4415) does **not** transfer. On the unseen family the reserve arm satisfies the
unconditional adaptation criterion on **2 of 4 distinct seeds** (4432, 4433) and **dies on 2 of 4**
(4434, 4435) — where the no-reserve control *survives*. The reserve is not merely inert on those two
seeds: it converts a surviving control into a death. G1 (the unconditional criterion) is **FAIL**, and
is recorded as such, not moved.

## Per-seed outcome (both histories identical)

| seed | priority | reserve arm | no_reserve (control) |
|------|----------|-------------|----------------------|
| 4432 | `[2,0,1,3]` | drop@8208, reacq@8210, survives (W=3, C=2, routes [0,1]) | **dies 8447** (streak stuck 1, routes [None,None]) |
| 4433 | `[3,2,1,0]` | drop@8198, reacq@8199, survives (W=3, C=2, routes [1,1]) | survives, **no drop** (expiry reacq@8299, routes [1,1]) |
| 4434 | `[0,3,1,2]` | **dies 8443** (streak stuck 4, reserve armed@531 never released) | survives, no drop (expiry reacq@8306, routes [0,0]) |
| 4435 | `[0,2,1,3]` | **dies 8450** (streak stuck 3, reserve armed@547 never released) | **drop@8210**, reacq@8212, survives (routes [1,0]) |

- Reserve arm: 2/4 distinct seeds relinquish + reacquire + survive; 2/4 die with the drop never firing.
- No-reserve control: 3/4 survive (4433/4434 by entry expiry + blind reacquisition, 4435 by actual
  relinquishment); 1/4 dies (4432). 1/4 relinquish (4435).

## The mechanism (the honest new finding)

The reserve's release is gated on the drop firing — `release_reserve` runs only inside `_drop`, when
`material < RESERVE_LEVEL`. But the reserve is *armed* ~7660 ticks earlier, at the first productive
material contact (`t = 531-547`), withholding `RESERVE_LEVEL = 21` from the spendable pool. On
4434/4435 that withholding shifts the material-cycle phase in a direction that **stalls the streak
below the drop threshold**, so the drop never fires and the reserve is never released
(`reserve_m = 21`, `reserve_released_m = 0`, `reserve_armed_end = 1`). The permanently-withheld 21
units then tip the organism into the death cascade (obs bit 1 set, material contact preempts renewal,
W and C die together, energy drains).

The cleanest instance is 4435: the no-reserve control's streak builds 0→1→2→3→4→5→drop@8210 and
survives; the reserve arm's streak stalls at **3** — the 3→4 increment costs 3 bits × 7 replicas =
**21 material, exactly `RESERVE_LEVEL`** — so the withholding starves the very increment the decision
needs to reach the drop. On 4434 both arms stall the streak (reserve at 4, control at 3), but only the
reserve arm dies: its 21 units are a permanent loss, the control's are not.

This is the AC11/AC12/AC13 wall from a new direction. The fix for the affordability problem — the
reserve — is itself paid-maintained, and its withholding starves the decision's own *buildup* (the
streak increments are paid writes too). The reserve that was supposed to fund the decision can prevent
the decision from ever firing, and when that happens it is a pure harm, not a neutral "merely delays".

## Gates (prespecified in the protocol)

- **G1 unconditional adaptation — FAIL.** 2/4 distinct seeds (4434, 4435) fail A4 (survival) and A1
  (relinquishment); A3 (continued W/C/B production) also fails on them (W_births_post_move = 0). The
  criterion required every distinct seed to satisfy all four measures. Recorded, not moved.
- **G2 reserve load-bearing contrast — PASS.** Seed 4432: no-reserve dies where reserve survives; seed
  4433: no-reserve fails to relinquish where reserve relinquishes.
- **G3 state sufficiency (per-tick observer-discard) — PASS 8/8.** The reserve-arm run with the
  succession observer + host streak dict discarded at a mid-streak tick is byte-identical at every one
  of 16,384 ticks (trajectory-level; `per_tick_identical`, `swap_applied`, `streak_at_swap == 2` on all
  8 individuals). State sufficiency (AC96) is unaffected by the economic finding.
- **G4 endogenous reserve (no external rescue) — PASS.** Every reserve individual: `reserve_m > 0` and
  `reserve_released_m <= reserve_m`. On the dying seeds nothing is ever released (21 withheld, 0
  released) — the organism's own income, never injected.
- **G5 completeness + determinism + control equivalence — PASS.** 16 rows; sampled rerun byte-identical;
  the no-reserve control is byte-identical to `ac96.run(..., streak_maintained=True)` on all 8
  individuals — the reserve is the only change from the frozen ac96 architecture.

## A gate-shape lesson (carry forward)

G2 as written — "the reserve helps on ≥ 1 seed" — is satisfiable even when the reserve is net-harmful,
because it checks only the positive direction. The claim "affords self-preservation" is carried
entirely by G1 (unconditional, every individual), and G1 is the gate that caught the failure. The
missing contrast is the **no-harm direction**: the reserve must not turn a surviving control into a
death. On 4434/4435 that direction is falsified (no-reserve survives, reserve dies). A future
affordability study needs a prespecified no-harm gate — "no distinct seed where the control survives
and the success arm dies" — in addition to the unconditional success criterion, or its "load-bearing"
contrast is satisfiable by a mechanism that sometimes helps and sometimes kills.

## Reported, not gated

- **The maintenance trade-off is seed-dependent and can invert.** D2 measured the 21-unit withholding
  as "absorbed by cycle slack" on 4412-4415. On 4434/4435 the same withholding is a permanent loss that
  causes death. The trade-off is not a uniform small cost; it is benign when the drop fires and fatal
  when it does not.
- **The reserve is a fixed minimum reserve, not an acquired allocation.** `RESERVE_LEVEL = 21` and the
  `material < 21` release trigger are declared world constants. The failure is in the fixed mechanism's
  interaction with the paid streak increments (the 3→4 increment costs exactly 21), not in an acquired
  policy. The question "does the organism *acquire* how much to save" remains open and is now joined by
  "can a reserve be sized and triggered so it does not starve the decision it funds".
- **Survival is a bimodality-aware lower bound.** Reported per distinct seed (above); no uniform
  survival count is gated.
- **Priorities.** 4432 `[2,0,1,3]`, 4433 `[3,2,1,0]`, 4434 `[0,3,1,2]`, 4435 `[0,2,1,3]` — none is
  AC83's adversarial `[3,0,2,1]`. The relinquishment is a streak/register decision, not a
  renewal-contention decision, so the priority ordering does not confound the mechanism.
- **Supplied machinery remains.** `advance()` and `prog.choose` are still host-supplied format-level
  machinery; no autopoiesis claim. Affordability is the question, and the answer here is negative for
  the unconditional criterion.

## Verification

- `audit_ac97.py` passes: 16 rows, 16 hashes no drift, arm invariants (reserve-arm deaths 8443/8450,
  no-reserve survival/relinquishment), observer-discard record 8/8 per-tick, control-equivalence 8/8,
  gates re-derived WITHOUT simulating and matching the recorded result — including the recorded G1
  FAIL (a falsification is preserved, not concealed).
- `replay_ac97.py` passes: 2/2 exact (state_hash + endpoint fields), observer-discard 1/1 per-tick
  byte-identical, control-equivalence 1/1.
- `test_ac97.py` 14/14 green: single-step reserve primitive (arm withholds 21 + paid write 7, refuses
  when poor / when W=0, release restores + disarms with `released <= withheld`, majority read, atomic
  write), per-tick observer-discard on all 4 finals, control equivalence, seed-disjointness, and a
  **recorded-outcome regression** pinning the G1 falsification (reserve dies on 4434/4435 while the
  control survives) so a future code change that moves the record is caught.
- Core AC1-9 suite 56/56 green. No frozen runner was modified.

## Boundary and next step

The internally maintained organization does **not** afford self-preservation through the move under an
unconditional, per-individual criterion: the internal reserve funds the relinquishment on half the
unseen family and kills the organism on the other half, by starving the streak's own paid buildup when
the drop never fires. The affordability question AC97 asked is answered **negatively** for this fixed
reserve, on this unseen family. The next architecture needs a reserve whose withholding cannot starve
the decision it funds — e.g. a smaller or staged reserve, a release trigger that also fires on streak
stall (not only inside `_drop`), or arming the reserve only after the streak has passed the expensive
increment — none of which changes the standing boundary (transition logic + interpreter still supplied;
no autopoiesis claim). All earlier results (ac96_results_v1, ac97_d2_engineering_v1, and every prior
freeze) are preserved untouched.
