# AC98-D1 — design: a revised reserve whose withholding cannot starve the decision it funds

Parent: AC98 goal. **Design only — no code, no protocol, no freeze.** The implementer (D2) is the
audience: the exact arming/release conditions, the level, the storage/repair path, the no-harm test,
and the re-derived sizing. `ac97.py`, `ac96.py` and every freeze stay untouched; the runner is a new
file `ac98.py` (parent decision).

---

## 0. The failure to eliminate, corrected

AC97-D3 recorded the failure as a coincidence: "`RESERVE_LEVEL = 21` equals the streak's 3→4 increment
(3 bits × 7 = 21), so the withholding starves the increment." That is **imprecise in a way that matters
for the fix**, and this design corrects it with a tick-by-tick trace. Measured with an instrumented
probe (byte-identical to the frozen `state_hash` on every individual), the two deaths are two *different*
mechanisms:

**4434 (`priority [0,3,1,2]`)** — the 3→4 increment **succeeds**; the *4→5* increment is starved by
**material**, not by the 21-coincidence:

```
t     event       pre-M   W   cap   n   accepted
8216  0→1         58      3   24    7   yes
8217  1→2         51      3   24    14  yes
8219  2→3         27      3   24    7   yes
8220  3→4         27      3   24    21  yes      <- the "expensive" increment PASSES
8221  4→5         6       3    6    7   NO  (M=6 < 7)  <- starved here, by 1 material unit
```

The reserve's 21 units are sitting out of the pool exactly when the pool is 1 short of the 4→5
increment; the streak stalls at 4, the drop never fires, the reserve never releases, the 21 is a
permanent loss, and the organism dies (8443). The release gate (`_drop` only) is the bug.

**4435 (`priority [0,2,1,3]`)** — the 3→4 increment is starved by **W**, not material. The reserve's
one-time 21-unit withholding at `t≈547` shifts the material cycle's *phase*; on this seed the phase
shift leaves the reserve arm at **material 124 at the move tick** (vs **82** for the no-reserve control),
so the post-move streak build is delayed **25 ticks** (starts 8230 vs 8205). That delay carries the build
into a W-death window:

```
t     no-reserve W   reserve W   (reserve M at same tick)
8205  3 (build starts)  3        102
8229  3                  3         61
8230  3                  2         54  <- W + region-0 catalyst die together
8231  3                  2         ...
8232  3                  2         ...
8233  3                  1         31  <- 3→4 refused: cap = 8·W = 8 < 21
```

The 3→4 increment needs `cap = min(32, 8·W, energy, material) ≥ 21`, i.e. **W ≥ 3**. At W=2 the
increment is refused *regardless of material* (8·2 = 16 < 21), and material ≤ 64 keeps observation bit 1
set, which keeps action 1 (the stale material contact) ahead of action 6 (W birth) in the frozen
priority order — so W can only decay further (2→1→0), never recover, during the build. The no-reserve
control builds at 8205–8209 (W=3 throughout) and drops at 8210, *before* the W death.

**Corrected mechanism, in one sentence:** a fixed material reserve armed ~7660 ticks before an
unannounced move perturbs the material oscillator's phase seed-dependently; on some seeds the phase
shift delays the post-move streak build until it collides with a W-death (or leaves the pool one unit
short of an increment), so the decision's own buildup is starved and the reserve — released only inside
`_drop` — becomes a permanent loss that kills the organism.

---

## 1. The revision: release-on-streak-stall (primary) + release-on-W-low (survival)

**Chosen revision: (b) release-on-streak-stall, plus one survival-preserving trigger.** This is a
justified combination, and the choice is forced by measurement, not preference:

- **(a) arm-after-expensive-increment is infeasible.** The "expensive increment" (3→4) happens *after*
  the move, on the post-move streak build. After the move the material channel is stale, so there is
  **no material income to arm from** (`e['in_m']` is zero on every post-move contact). A reserve can
  only be accumulated pre-move; it cannot be armed "after the 3→4 increment" without external material.
  The tick-by-tick trace above shows the 3→4 increment is the wrong target anyway (4434's 3→4 succeeds;
  4435's 3→4 fails on W, not on an armable resource).

- **(c) smaller/staged regresses.** A smaller level reduces the phase shift and *does* fix 4435 (L14:
  8/8 finals relinquish+survive), but it under-funds the drop+reset and kills the seeds the AC97-D2
  reserve was built to save (L14: 4433 and 4412 die; L7: 4412 and 4413 die). A reserve smaller than
  `drop+reset` cannot fund the decision it exists to fund. Measured, not assumed.

- **(b) release-on-stall is the fix for the material starvation (4434), and a W-low release is the only
  way the reserve can avoid *killing* 4435**, where the no-reserve control survives. The reserve's job
  is to help; the release conditions below implement "fund the decision when it fires, and return the
  withheld material the moment continuing to withhold would starve the buildup or the repair catalyst."

### Exact arming condition (unchanged from AC97)

On a productive material contact (`key == 1`, `e['productive'] > 0`) at `t >= DEV`, when the reserve is
disarmed and `material >= RESERVE_LEVEL` and `e['in_m'] >= RESERVE_LEVEL`: withhold `RESERVE_LEVEL`
material from that contact's intake (`b.material -= RESERVE_LEVEL`, `e['in_m'] -= RESERVE_LEVEL`, the
AC15 "intake is a variable" identity so `ac4.balance` holds by construction) and set the reserve bit with
a paid, W-gated atomic write (≤ 7 replicas). If the arm write is refused, the withholding is rolled back
(never a half-armed reserve). Exactly as `ac97.arm_reserve`; unchanged.

### Exact release conditions (revised)

The reserve releases — `b.material += rel`, `e['in_m'] += rel` (`rel = min(RESERVE_LEVEL, 256 - material)`),
and the reserve bit cleared with a paid W-gated write — when **any** of these three fires, in this order of
evaluation:

1. **`drop`** (original): inside `_drop`, when `material < RESERVE_LEVEL`, before the cap check. Funds the
   drop register write (7) and the streak reset (14) at the moment they are refused by the income collapse.
2. **`stall`** (the revision): when a streak increment is refused — `ac96.streak_write` returns 0 for a
   `cur → cur+1` transition (reached only when `cur+1 < STREAK_N`). This is the direct fix for 4434: the
   refused 4→5 increment (M=6) releases the 21 units, M→27, and the next tick's 4→5 (7) then the drop (7)
   are funded. The release is read from the maintained streak (organism state), not a host flag.
3. **`wlow`** (survival): when `available_W < 3 and material <= 64` on a key-1 contact. This releases the
   21 units so `material` rises above 64, clearing observation bit 1, which lets the frozen priority order
   run the W-birth rule (action 6) instead of the stale material contact (action 1) — recovering W and the
   region-0 catalyst before the death cascade. This is what stops 4435 from *dying*; it does not (and
   cannot) make 4435's 3→4 increment succeed, because that increment is W-bound and the one-shot release
   cannot hold W ≥ 3 through the repeated W-death window (see §6, the honest residual).

`rel` is capped by the 256-material cap exactly as in AC97; `release_reserve` returns 0 and leaves the bit
set if nothing is released. The release is a **separate store drain**, never a paid counter write (AC97-D2's
rule): a single armed/disarmed bit (≤ 7 replicas) fits the W cap even at W=2, and is paid once the released
material has landed.

### Exact level

`RESERVE_LEVEL = 21` (unchanged). Re-derived in §4.

---

## 2. Storage + repair (unchanged from AC97)

- **Storage.** One maintained-state bit at `traces[1, 540]` (a free bank-1 region; slots 0–519, pointer
  520–521, CTRL 522–539 are occupied). `1 = armed` (21 material withheld), `0 = disarmed`. Read by
  majority (`>= 4` of 7 replicas). The reserved material lives **outside `b.material`** (it is subtracted
  from intake, not a floor on the pool), so no lower-priority write can reach it — and, critically, no
  floor above 64 silences the material-contact observation (AC97-D2).
- **Damage.** The bit is damaged by the same sticky bank-1 stream as the description/pointer/CTRL
  (`traces[1, 540] |= (rng1.random(7) < 1e-4)`), so it is genuinely vulnerable; `minority_end = 0` in
  every AC97 run (it never reads spuriously).
- **Repair.** A paid majority-restore (`reg_reserve`) fires when `minority >= RESERVE_TRIGGER = 2`,
  folded into `maintain` exactly as in AC97. Nothing changes.
- **No host-side flag.** The three release conditions read organism state only — `b.material`,
  `available_W`, and the maintained streak (`ac96.streak_read`) — and write `traces[1, 540]` plus the
  material ledger. `reserve_events` remains an observational log, never read to steer a write. The
  observer-discard test (per-tick) still applies: discarding the succession observer and the alloc at a
  mid-streak tick must reproduce the trajectory byte-for-byte, because the release conditions are pure
  functions of `o.body`/`o.memory` (maintained state) and the reserve bit is maintained state.

---

## 3. No-harm test (prespecified, catches AC97's failure mode)

The gate that would have caught AC97-D3 is the **no-harm direction** (AC97-D3's own lesson, and the parent
card's `constraints_carried`): *no distinct seed on which the no-reserve control survives and the reserve
arm dies*. Prespecified for D2/D3, and measured per distinct seed as:

```
for each distinct seed s:
    assert not (no_reserve[s].completed and not reserve[s].completed)
```

measured on survival (`completed`), with relinquishment reported separately (not gated — a seed where the
reserve survives but does not relinquish is a *behavioural* finding, not a harm). The engineering probe
in §6 verifies this on the D1/D2 seeds 4412–4415 **and** the AC97 finals 4432–4435, both directions:
the reserve arm must survive wherever the no-reserve control survives, and it must additionally relinquish
on every seed where the no-reserve control dies (that is the load-bearing, positive direction — the
contrast the AC97 G2 checked only one way).

This is the design's acceptance test, stated in the design (not the protocol): **the revised reserve must
convert every AC97 reserve-arm death into a survival, and must not introduce any new death.**

---

## 4. Sizing

`RESERVE_LEVEL = 21 = drop (7 replicas) + reset (14 replicas)`, the D1 derivation, and it is unchanged.

- The **drop** register write flips the decision bit 0→1: 7 replicas (7 material), paid 1 energy + 1
  material per replica.
- The **reset** clears the streak `5→0` (`0b101 → 0b000`, two bits): 14 replicas (14 material).

The reserve releases 21 as a lump and funds **both** where the drop fires on the threshold (AC97-D2's
case). Under release-on-stall the 21 is released *one increment earlier* (at the stall, before the drop),
so it funds the remaining increment (7) + the drop (7) + part of the reset (14), and the reset's remainder
is **deferred to post-reacquisition** — the organism re-acquires the route, income resumes, and the still-
pending reset is paid from the resumed cycle. That deferral is already the observed, harmless pattern:
AC97-D1 seed 4413 drops at M=8 but the reset is refused at M=1 and the organism survives with the streak
temporarily stuck at 5; 4435's no-reserve control does the same (reset refused at M=2, succeeds two ticks
after re-acquisition). The reserve's obligation is the **drop** (the decision); the reset is bookkeeping
that self-heals. The level therefore stays 21 — the smallest level that fully funds the drop+reset when
the drop fires on the threshold, and no smaller level saves the D1/D2 family (measured: L7 and L14 both
kill seeds the L21 reserve saves).

---

## 5. What this does and does not establish

- **Established:** the reserve's release is no longer gated on the very decision it funds. It releases on
  a stall (so the withholding can never be a permanent loss) and on W-low (so the withholding cannot tip
  the organism into the death cascade). On 4434 the stall release funds the starved increment and the drop
  fires; on every seed where the no-reserve control survives, the reserve arm also survives (no harm).
- **Not established (honest residual):** the reserve does **not** make 4435's drop fire. 4435's 3→4
  increment is W-bound (needs W ≥ 3; the phase-shifted build starts at W=2 and W only decays during the
  build because action 1 preempts W birth). A one-shot material release recovers W once (probe: W→3 for
  one tick at 8231) but cannot hold it through the repeated W-death window, so the streak stalls at 3 and
  the entry expires into blind re-acquisition — the organism survives, it does not relinquish. This is a
  *phase-shift* limit of any pre-move material reserve, not a release-timing bug, and it is carried into
  the protocol as a reported limitation, not hidden.
- **Boundary (unchanged):** the reserve is a fixed minimum reserve, not an acquired allocation; `advance()`
  and `prog.choose` remain supplied format-level machinery. No autopoiesis claim.

---

## 6. Verification (engineering probe, not the runner)

`_ac98_d1_probe3.py` (config sweep) and `_ac98_d1_probe4.py` (trigger sweep) implement the revised
release conditions on top of `ac97.py` (byte-identical when the triggers are the AC97 default), and run
the AC97 finals 4432–4435 plus the D1/D2 seeds 4412–4415, reserve vs no-reserve, `transition='perm'`,
16,384 ticks. Results for the chosen design — **release triggers `{drop, stall, wlow}`, level 21**:

| seed | no-reserve (control)        | reserve (revised)                     | no-harm |
|------|-----------------------------|---------------------------------------|---------|
| 4432 | **dies** 8447               | relinquish + survive (W=3,C=2)        | helps   |
| 4433 | survive, no drop            | relinquish + survive                  | helps   |
| 4434 | survive, no drop (expiry)   | **relinquish + survive** (was death)  | helps   |
| 4435 | survive, **relinquish**     | survive, **no drop** (stall→expiry)   | no harm (survives) |
| 4412 | dies                        | relinquish + survive                  | helps   |
| 4413 | relinquish + survive        | relinquish + survive                  | tie     |
| 4414 | dies                        | relinquish + survive                  | helps   |
| 4415 | dies                        | relinquish + survive                  | helps   |

- **4434 fixed, tick by tick:** 3→4 succeeds at 8220; 4→5 refused at 8221 (M=6); the stall release
  returns 21 (M→27); the 4→5 increment (7) then the drop (7) are funded; `relinquishments = 1`,
  `completed = True`.
- **4435 survives (no harm):** the 3→4 increment is refused at 8233 on W (W=1, `cap=8 < 21`, M=31
  sufficient); the wlow release at 8230 already cleared obs bit 1 so W recovered 2→3 for one tick, but the
  repeated W-death window (8229 and 8232) drops it again; the streak stalls at 3, the entry expires,
  blind re-acquisition, `completed = True`, `relinquishments = 0`. Recorded honestly.
- **No regression:** 4432/4433 and 4412–4415 all relinquish and survive exactly as under AC97-D2.
- **Consistency check:** `drop`-only release reproduces the AC97 baseline exactly (the revision is a
  strict superset of the release conditions, so the no-reserve control and the drop-trigger path are
  byte-identical to AC97).

**Diagnostic that shaped the diagnosis (not the design):** `_ac98_d1_probe7.py` sweeps the arm threshold
and finds the phase drift is *duration-dependent and non-monotonic* — arming at `t≥4096` or `t≥7680`
makes both 4434 and 4435 relinquish+survive, but arming at `t≥6144` still kills 4435 (build starts at
W=2), and arming at the AC97 default `t≥512` kills 4434. This confirms the root cause (the 21 units held
for ~7660 ticks drift the material phase; a short holding period drifts less) but offers **no principled
arm condition**: the organism cannot know the move tick, so any fixed late threshold is a magic constant
that merely re-rolls the seed-dependent phase onto a different family. The release-on-stall revision is
chosen precisely because it does *not* rely on the phase landing well — it returns the withheld material
the moment continuing to withhold would starve the buildup.

The three claims D2 must re-verify with the real runner (not the probe) before any protocol: (1) 4434
death→relinquish+survive, (2) no-regress on 4432/4433/4412–4415, (3) no-harm (no reserve death where the
control survives) on 4434/4435 and the whole family.

---

## Files (scratch, measurement only — not part of the freeze)

- `_ac98_d1_probe3.py` — level × release-trigger sweep (the table above).
- `_ac98_d1_probe4.py` — release-trigger combinations.
- `_ac98_d1_probe5.py` — W / region-catalyst / material trajectory (the phase-shift and W-death evidence).
- `_ac98_d1_probe6.py` — wlow-release trace (why W recovers once then re-collapses).
- `_ac98_d1_probe7.py` — arm-threshold sweep (the duration-dependent, non-monotonic phase drift).
