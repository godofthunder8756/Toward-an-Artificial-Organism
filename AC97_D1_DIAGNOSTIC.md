# AC97-D1 — the decisive budget shortfall behind the stuck streak-5

Diagnosis only. No fix proposed (D2 designs the reserve). No protocol, no freeze.

## Question

In the AC96 `transition='perm'` world, 3 of 4 maintained-arm seeds (4412, 4414, 4415)
die with the moved route's relinquishment streak stuck at 5. The 6th unproductive
contact should fire the drop (`cur + 1 >= STREAK_N`, cur=5), but a paid write is
refused by the income collapse. Which write, and why?

## Method

`ac97_d1_probe.py` monkeypatches the three paid write primitives and records,
immediately before each event, `energy`, `material`, `W`, `_cap = min(32, 8*W,
energy, material)`, the write's replica count, and whether it was accepted or
refused. The instrumented trajectory is byte-identical to the frozen run
(`state_hash` equal to `ac96_results_v1/rows.jsonl` for all 8 individuals).

## Verdict (one line)

The decisive refusal is the **relinquishment (`_drop`) register write itself** — 7
replicas, refused because `material (3–6) < 7` at the 6th unproductive contact —
while energy (120–127) and W (2–3, i.e. 8·W = 16–24) are abundant; the streak is
stuck at 5 not because the counter is unaffordable but because the **decision's own
write is**, by a shortfall of **1–4 material units**.

## Per-individual trace (tick, event, energy, material, W, cap, replicas, accepted)

`cap = min(32, 8·W, energy, material)`; the binding term is material in every row.
Both histories are identical per seed (deterministic); one table per seed.

### seed 4412 — dies at 8444, relinquishments 0, streak_final 5

| tick | event             | energy | material | W | cap | n  | accepted |
|------|-------------------|--------|----------|---|-----|----|----------|
| 8228 | increment 0→1     | 127    | 60       | 3 | 24  | 7  | yes      |
| 8229 | increment 1→2     | 127    | 53       | 3 | 24  | 14 | yes      |
| 8230 | increment 2→3     | 120    | 39       | 3 | 24  | 7  | yes      |
| 8231 | increment 3→4     | 120    | 32       | 3 | 24  | 21 | yes      |
| 8232 | increment 4→5     | 114    | 11       | 2 | 11  | 7  | yes      |
| 8233 | **drop (register)** | 122  | **4**    | 2 | **4** | **7** | **no — M=4 < 7** |

### seed 4414 — dies at 8415, relinquishments 0, streak_final 5

| tick | event             | energy | material | W | cap | n  | accepted |
|------|-------------------|--------|----------|---|-----|----|----------|
| 8200 | increment 0→1     | 117    | 62       | 3 | 24  | 7  | yes      |
| 8201 | increment 1→2     | 125    | 55       | 3 | 24  | 14 | yes      |
| 8202 | increment 2→3     | 126    | 41       | 3 | 24  | 7  | yes      |
| 8203 | increment 3→4     | 123    | 31       | 3 | 24  | 21 | yes      |
| 8204 | increment 4→5     | 117    | 10       | 3 | 10  | 7  | yes      |
| 8205 | **drop (register)** | 125  | **3**    | 3 | **3** | **7** | **no — M=3 < 7** |

### seed 4415 — dies at 8441, relinquishments 0, streak_final 5

| tick | event             | energy | material | W | cap | n  | accepted |
|------|-------------------|--------|----------|---|-----|----|----------|
| 8215 | increment 0→1     | 127    | 63       | 3 | 24  | 8  | yes      |
| 8216 | increment 1→2     | 126    | 55       | 3 | 24  | 14 | yes      |
| 8217 | increment 2→3     | 127    | 41       | 3 | 24  | 7  | yes      |
| 8218 | increment 3→4     | 127    | 34       | 3 | 24  | 21 | yes      |
| 8219 | increment 4→5     | 121    | 13       | 3 | 13  | 7  | yes      |
| 8220 | **drop (register)** | 121  | **6**    | 3 | **6** | **7** | **no — M=6 < 7** |

### seed 4413 — survives, relinquishments 1 (the control contrast)

| tick | event             | energy | material | W | cap | n  | accepted |
|------|-------------------|--------|----------|---|-----|----|----------|
| 8201 | increment 0→1     | 126    | 64       | 3 | 24  | 7  | yes      |
| 8202 | increment 1→2     | 126    | 57       | 3 | 24  | 14 | yes      |
| 8203 | increment 2→3     | 127    | 43       | 3 | 24  | 7  | yes      |
| 8204 | increment 3→4     | 127    | 36       | 3 | 24  | 21 | yes      |
| 8205 | increment 4→5     | 121    | 15       | 3 | 15  | 7  | yes      |
| 8206 | **drop (register)** | 121  | **8**    | 3 | **8** | **7** | **yes — M=8 ≥ 7** |
| 8206 | reset 5→0         | 114    | **1**    | 3 | **1** | 14 | no — M=1 < 14 |

The surviving individual had material 8 at the threshold (one unit to spare); the
three dying individuals had 3–6 (one to four units short). The margin between
dropping and dying is **material 7 vs 3–6**.

## Why the counter is not the problem (correcting the D3 note's generalisation)

AC96-D3 reported "the drop's own register write (≤7 replicas) succeeds but the
streak RESET inside `_drop` (5→0, 14 replicas) is refused". That is **seed 4413's
story** — the one survivor. In the three dying seeds the register write is refused
one step earlier, so the reset (14 replicas) is never even attempted: it sits
downstream of a refused register write, and `_drop` returns before reaching it.
The D3 note under-generalised from the surviving seed; the deaths are caused by the
drop write, not the reset.

The increment is also exonerated: 0→1 … 4→5 all succeed (the last, 4→5, costs 7
replicas and is accepted at M = 11/10/13). The "increment that never reaches 6" is a
misnomer — the 5→6 transition is never *attempted*, because `cur + 1 >= STREAK_N`
routes cur=5 straight to `_drop`.

## The bank-0 repair is not the competing consumer

`reg_from_active` (the reconstruction that maintains the program, register and
streak excluded) is measured in the critical window: it fires but writes **0
replicas** (either `build_program` returns None on a degraded active slot, or
`n_avail == 0` because the program already matches the description). It consumes no
material in the window around the first drop refusal, so option 4 ("the repair being
preempted by the material-contact") is not the cause. The material-contact hijack
*is* operating — obs bit 1 (material ≤ 64) makes the program fire action 1 (the
stale material channel) every tick, which is why the streak increments on five
consecutive ticks — but the write it starves is the drop, not the repair.

## Root cause of the collapse (for D2's sizing, not a fix)

The moved key is key 1, which is **channel 1 = action 1 = the material-income
contact** (`e['in_m'] = 64`). Flipping it sends material income to zero, while the
fuel channel (action 0) and the energy conversion path are untouched — hence energy
sits at ~120 and W stays 2–3, but material drains (births at 4 each, renewals and
repairs at 1 per write, the streak increments at 7–21) to a floor of 3–6. The drop
write is paid 1 material per replica, all 7 replicas flip 0→1, so it needs 7 and is
refused whole.

Facts D2 needs, measured not assumed:

- the relinquishment register write costs exactly **7 material** (n=7, all seven
  replicas 0→1);
- at the tick it must fire, material is **3–6** (shortfall **1–4**);
- **energy and W are not the binding term** (energy 120–127, W 2–3 → 8·W = 16–24,
  both ≥ 7);
- the reset, if the drop were funded, needs a further **14 material** (seed 4413
  shows it is refused at M=1 immediately after the 7-replica drop spend) — so a
  reserve that funds only the drop still leaves the counter stuck at 5 unless it
  also covers the reset. D2 must size for the drop (7) **and** the reset (14) as two
  separate paid writes at the same threshold, per AC96-D3's rule.
