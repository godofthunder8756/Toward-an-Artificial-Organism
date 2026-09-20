# AC99-D2 — results: Gray-coded streak vs binary — cheaper increments, and 4436 flips to relinquish + survive

Parent: AC99-D1 (the atomic release+disarm fix). Runner `ac99_d2.py` (new); `ac99.py`, `ac98.py`,
`ac97.py` and every freeze are untouched (`ac98.py` sha256 `1ae3d37…` unchanged; `audit_ac98.py`
still passes). Engineering only — **no protocol, no freeze**. World: the AC96/AC97/AC98
relinquishment world (`transition='perm'`, damage on, corrupt off, 16,384 ticks, move at 8192),
the AC98 finals 4436–4439 plus the D1/D2 seeds 4412–4415, both histories, binary reserve arm
(`ac99.run(reserve=True)`) vs Gray reserve arm (`ac99_d2.run(reserve=True)` on the same
individuals. Held constant: `STREAK_N = 6`, the sticky 1e-4 damage model, the 7-replica majority
read (threshold 4), prices (1 energy + 1 material per replica), and the AC98/AC99-D1 reserve
(level 21, drop/stall/wlow triggers, atomic release). The ONLY change is the counter's code
(binary ⇄ 3-bit reflected Gray).

## 0. Verdict

**The hypothesis is confirmed.** The binary streak's `3→4` increment is the W-bound stall that kills
4436: it flips three logical bits = 21 replicas, so `_cap = min(32, 8·W, …) ≥ 21` needs W ≥ 3, and
4436's phase-shifted post-move build runs through a repeated W-death window where W < 3. The Gray
`3→4` is a **single** bit = 7 replicas (needs W ≥ 1), so the streak builds straight through the
W-death window and the drop fires.

On seed 4436 (the AC98 G1 failure): **binary dies at 8430 with the streak stuck at 3 and no
relinquishment; Gray relinquishes, re-acquires both routes, and survives** (both histories
identical). **No regression** on the other seven seeds — every one still relinquishes and survives
under Gray, and none of the 16 binary-vs-Gray individuals flips the wrong way (0/16 regressions).

But Gray is **not uniformly cheaper or more robust**, and three of the task's stated arithmetic
facts are wrong in a way that matters (corrected in §4). The net effect is real and positive, but
it is narrower than "cheaper everywhere": Gray buys cheaper *increments* and pays a *dearer reset*
and a *different damage failure mode*.

## 1. Cost table (binary vs Gray, 7 replicas per logical bit)

| transition    | binary bits | binary replicas | gray bits | gray replicas |
|---------------|------------:|----------------:|----------:|--------------:|
| 0→1           | 1           |  7              | 1         |  7            |
| 1→2           | 2           | 14              | 1         |  7            |
| 2→3           | 1           |  7              | 1         |  7            |
| **3→4**       | **3**       | **21**          | **1**     | **7**         |
| 4→5           | 1           |  7              | 1         |  7            |
| **5→0 (reset)** | 2         | 14              | **3**     | **21**        |

- Every Gray increment is **one bit** (7 replicas). The binary 3→4 is 3 bits (21 replicas) and the
  binary 1→2 is 2 bits (14 replicas) — so Gray removes *two* W-bound increments, not one: the 1→2
  needs W ≥ 2 in binary (8·W ≥ 14) and the 3→4 needs W ≥ 3 (8·W ≥ 21); in Gray both need only
  W ≥ 1 (8·W ≥ 7).
- The **reset is dearer in Gray**: 5→0 is 3 bits (21 replicas) in Gray vs 2 bits (14) in binary.
  A full cycle 0→1→2→3→4→5 plus reset is 5 + 3 = 8 bits (56 replicas) in Gray vs 8 + 2 = 10 bits
  (70 replicas) in binary — Gray is still cheaper over the whole cycle, but the reset is the one
  operation where Gray loses.

## 2. The 4436 outcome (the decisive flip)

Per individual (both histories agree):

| code   | completed | first_dead | relinquishments | routes     | streak_final | streak_writes | release kinds        |
|--------|-----------|-----------:|----------------:|------------|--------------|--------------:|----------------------|
| binary | False     | 8430       | 0               | [None,None]| {0:0, 1:3}   | 28            | wlow @8230            |
| gray   | True      | —          | 1               | [0, 1]     | {0:0, 1:0}   | 56            | wlow @8230            |

Gray tick-by-tick (key 1, post-move): 0→1 @8229, 1→2 @8230, 2→3 @8231, **3→4 @8232**, 4→5 @8233,
drop @8234 (register bit set, entry expired), re-acquire @8236. The 3→4 increment — the exact
transition that stalls the binary streak — succeeds at W < 3 because it is a single bit (7
replicas). The binary streak on the same seed stalls at 3 (3→4 refused every time W dips below 3),
the entry expires into blind re-acquisition, and the W/C collapse kills the organism at 8430 with
W=0, C=0, energy=0 (reproduces AC98's recorded death exactly).

Two mechanics worth stating:

- **The `wlow` release still fires on 4436 under Gray** (8230), and it is what recovers W once the
  material-low observation clears — but under Gray that one-shot recovery is *enough*, because the
  subsequent increments are 1-bit and affordable at W = 1–2. In binary the same one-shot recovery
  cannot hold W ≥ 3 through the repeated W-death window, so the streak stalls.
- **The Gray reset is deferred, not blocked.** At the drop the reset (5→0, 21 replicas) is refused
  because drop (7) + reset (21) = 28 > the fixed `RESERVE_LEVEL = 21` (binary's drop 7 + reset 14
  = 21 exactly fills it). The reset self-heals on the post-re-acquisition productive contact
  (streak_final = 0). This is the same benign deferral AC98-D2 documented, now slightly more likely
  because the reset is 7 replicas dearer. It does not block the drop or survival, but it means the
  reserve no longer *fully* funds the drop+reset under Gray — a consequence of holding
  `RESERVE_LEVEL = 21` fixed (which the task required).

## 3. Regression check and the maintenance trade-off

| seed | binary (reserve)                     | gray (reserve)                       | regression |
|------|--------------------------------------|--------------------------------------|-----------:|
| 4436 | dies 8430 (streak stuck 3)           | **relinquish + survive**             | no (flip)  |
| 4437 | relinquish + survive (drop@8220)     | relinquish + survive (drop@8229)     | no         |
| 4438 | relinquish + survive (stall@8227)    | relinquish + survive (no release)    | no         |
| 4439 | relinquish + survive (stall@8220)    | relinquish + survive (drop@8221)     | no         |
| 4412 | relinquish + survive (drop@8224)     | relinquish + survive (no release)    | no         |
| 4413 | relinquish + survive (drop@8219)     | relinquish + survive (no release)    | no         |
| 4414 | relinquish + survive (drop@8210)     | relinquish + survive (no release)    | no         |
| 4415 | relinquish + survive (drop@8223)     | relinquish + survive (no release)    | no         |

16/16 Gray individuals survive and relinquish; **0/16 regress** (no seed where the binary reserve
arm survives and the Gray arm dies).

A secondary finding the task did not ask for, but which follows directly from the cheaper
increments: **Gray makes the reserve's release triggers fire far less often.** On 4438 and
4412–4415 the Gray arm arms the reserve once (`reserve_m = 21`) and **never releases it**
(`reserve_released_m = 0`, no release kind) — the 1-bit increments never stall (no `stall`
release) and never collapse the pool at the drop (no `drop` release). On those seeds the decision is
funded by the cheaper writes themselves. On 4436/4437/4439 the reserve still arms twice and
releases once (wlow/drop; only 4436's `wlow` is survival-critical, recovering W). Whether the reserve
is *redundant* is not established here — no Gray-without-reserve arm was run, so the release-frequency
shift is a descriptive finding, not a redundancy claim (the Gray-without-reserve comparison is carried
to the AC100 consolidation study). Total streak writes are lower under Gray on 7/8 seeds
(56–98 vs 70–126); on 4436 they are higher (56 vs 28) precisely because Gray completes the cycle the
binary streak stalls out of.

## 4. Corrections to the task's arithmetic (measured, not assumed)

Three facts in the task's "Measure" section are wrong, and two of them under-state Gray's costs. All
three are pinned by `test_ac99_d2.py`.

1. **"3→4 (011→010 in Gray)" is the wrong bit pattern.** 011→010 is the *2→3* transition. The 3→4
   transition is **010→110** (bit 2 flips). The single-bit claim is still true — only the
   parenthetical code is wrong. (Gray: 2=011, 3=010, 4=110.)
2. **The reset is NOT "same as binary 101→000".** Binary 5 = 101 → 000 changes **2** bits = 14
   replicas (bit 1 is already 0); Gray 5 = 111 → 000 changes **3** bits = 21 replicas. The Gray
   reset is **7 replicas dearer**, not equal.
3. **"A single-bit sticky flip in Gray changes the count by 1 (adjacent code)" is false for a
   3-bit code.** The adjacency property of Gray code is that *consecutive counts* differ in one bit
   — that is what makes increments cheap. It does **not** mean an arbitrary single-bit flip moves
   to an adjacent count. Measured (single logical bit 0→1, sticky SET is a no-op on a set bit):

   | value | binary flip reads (Δ) | gray flip reads (Δ)                       |
   |------:|-----------------------|--------------------------------------------|
   | 0     | 1, 2, 4 (+1,+2,+4)    | 1, 3, 7 (+1, +3, +7)                       |
   | 1     | 3, 5 (+2,+4)          | 2, 6 (+1, +5)                              |
   | 2     | 3, 6 (+1,+4)          | 5 (+3)                                     |
   | 3     | 7 (+4)                | 2, 4 (−1, +1)  ← a **decrease**            |
   | 4     | 5, 6 (+1,+2)          | 5 (+1)                                     |
   | 5     | 7 (+2)                | (none — 111 has no clear bit)              |

   The damage model is sticky SET (replicas only go 0→1), so:
   - **Binary** sticky damage only ever *increases* the count (+1/+2/+4) and can reach 6/7 (≥
     STREAK_N, an immediate drop on the next unproductive contact). It can only *accelerate*
     relinquishment.
   - **Gray** sticky damage can *decrease* the count (value 3 → 2 by setting bit 0), and can jump
     by ±1/±3/±5/±7. Every 3-bit pattern is a valid Gray code, so there is no "invalid" read — but
     the new failure mode is that damage can *erase* streak progress and delay relinquishment. At
     value 5 Gray is immune to the SET stream (all three bits set), which binary 5 (bit 1 clear) is
     not.

   This is a robustness *trade*, not a win: at the frozen 1e-4/replica/tick rate the sub-majority
   damage is rare (AC67: ~3 differing replicas of 882 over 4096 ticks), so the decrease path is
   unlikely to fire before the paid majority-restore cements the bit — but it is the failure mode
   to watch if the damage rate is ever raised, and it is why the task's "count by 1" hand-wave
   would have been misleading.

## 5. What this does and does not establish

- **Established:** the binary streak's W-bound `3→4` increment is the cause of the 4436 death, and
  replacing the counter with a reflected Gray code removes it — 4436 relinquishes + re-acquires +
  survives, with no regression on the other seven seeds. Gray is strictly cheaper on every
  increment and cheaper over the full cycle, at the price of a dearer reset and a damage mode that
  can decrease the count.
- **Not established / honest residuals:** (a) the Gray reset (21) + drop (7) = 28 now exceeds the
  fixed `RESERVE_LEVEL = 21`, so the reserve no longer fully funds the drop+reset — benign here (the
  reset self-heals) but a real change to the maintenance economy; (b) the reserve's release
  triggers fire less often under Gray (5/8 seeds never release), so on those seeds the *decision*
  is funded by the cheaper writes — but redundancy is not shown (no Gray-without-reserve arm was run;
  carried to the AC100 consolidation study); (c) the single-bit damage distribution is a
  *trade* (Gray can decrease the count), not a strict improvement.
- **Boundary (unchanged):** this is a code change to the decision state's *encoding*, not a new
  capability. The reserve is still a fixed minimum reserve (not an acquired allocation);
  `advance()` and `prog.choose` remain supplied format-level machinery. No autopoiesis claim.
  Whether the Gray streak should become the AC99 architecture (with a re-sized reserve to match
  the 28-replica drop+reset, and a damage-robustness gate) is D3/D4's decision; this task only
  measures the comparison.

## 6. Verification

- `test_ac99_d2.py` 10/10 green (Gray round-trip + adjacency, per-transition replica counts, the
  single-bit 3→4 write, value-0 identity, and the recorded 4436 flip binary-dies/gray-survives).
- `test_ac99.py` 6/6 green (D1 atomicity fix still passes; `ac99.py` untouched).
- Core AC1–9 suite 56/56 green.
- No frozen runner modified: `ac98.py` sha256 `1ae3d37…` unchanged, `ac97.py`/`ac96.py` and every
  earlier freeze untouched.
- Data: `ac99_d2_engineering_v1/` (32 rows: 8 seeds × 2 histories × binary/gray), `results.json`
  with the cost table, damage-read table, and per-individual comparison.

## Files

- `ac99_d2.py` — the runner (new; Gray streak read/write/encode/decode + `GrayAllocEraseReserve`;
  imports `ac99` for the reserve primitives and `ac96` for the streak storage).
- `test_ac99_d2.py` — verification only, **not hashed** (AC17's rule).
- `ac99_d2_engineering_v1/` — `rows.jsonl`, `results.json`. No `pre_run_snapshot.json` (no freeze).
- Scratch (measurement only): `_ac99_d2_graycheck.py`, `_ac99_d2_smoke.py`, `_ac99_d2_summary.py`,
  `_ac99_d2_detail.py`, `_ac99_d2_reacq.py`.
