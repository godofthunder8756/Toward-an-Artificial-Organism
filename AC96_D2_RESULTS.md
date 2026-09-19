# AC96-D2 — results: the relinquishment failure-streak in maintained state

Parent: AC96-D1 (design, `AC96_DESIGN_v1.md`). New runner `ac96.py`; `ac95.py`, `ac94.py`,
`ac12.py` and every freeze are untouched. Engineering only — **no protocol, no freeze**.

## 1. What was implemented

The second class-C host-side operational-memory leak from the AC95-D1 audit — `alloc.streak`,
the per-key (2 keys x 3 bits) count of consecutive unproductive contacts that drives the AC75
erase-on-relinquishment write — now lives in the organism's own vulnerable, paid-maintained state.
`ac95.AllocErase` kept it in a host dict (`ac12.Alloc.__init__`, read/written in `outcome`/`_drop`);
`ac96.AllocEraseMaintained` reads and writes it in the frozen program's permanently-dead rule's
six zero-valued bits. The host dict is vestigial and never read on the maintained arm.

## 2. Storage offsets

The dead rule (mask 32, action 5, word `0b01010001000001`) contributes exactly six zero-valued
word bits beyond the AC12 register (mask bits 0-3):

| field        | word bit | offset  | value in frozen program |
|--------------|----------|---------|-------------------------|
| mask bit 4   | 5        | base+5  | 0                       |
| mask bit 6   | 7        | base+7  | 0                       |
| mask bit 7   | 8        | base+8  | 0                       |
| mask bit 8   | 9        | base+9  | 0                       |
| action bit 1 | 11       | base+11 | 0                       |
| action bit 3 | 13       | base+13 | 0                       |

`base = 14 * ac12.dead_rule_index(o)`; the six offsets are
`[base+5, base+7, base+8, base+9, base+11, base+13]`, resolved **once at acquisition** (the AC12
rule: resolve register offsets from the pristine program). Key k's 3-bit counter is
`offsets[3k:3k+3]`, LSB first. Only 4 are mask bits (the task's ">= 6 mask bits" check is answered
NO); the last two are action-field bits, justified because the dead rule never fires (its mask still
requires observation bit 5, which `ac9.observe` never sets), so `prog.choose` never reads its action.

Verified on seeds 0-7 and 4404-4405: `dead_rule_index` varies (4, 5, 6, 7 observed), all six
offsets are `< 126` (max `14*8+13 = 125`), all zero in the frozen program, all distinct from the
register's `{base+1 .. base+4}` (`TestStreakOffsets`).

## 3. Damage, repair, and exclusion

- **Damage.** The six offsets are inside `traces[0,:126]`, so the sticky program stream
  (`b.traces[0,:126] |= core_flips`, 1e-4 per replica per tick) flips them exactly like the
  register and the program bank.
- **Repair.** The paid bank-0 majority-restore (frozen action 2, `ac4.react`) already covers
  `traces[0]`. Single-step test: damage 2 of 7 replicas of a streak bit, majority still reads the
  unflipped value, `ac4.react(...,2,...)` restores the 2 replicas, paid 1 energy + 1 material each
  (`TestStreakDamageRepair`).
- **Exclusion.** `reg_from_active` rebuilds the program from the description and writes every
  non-excluded bit toward the description value. The maintained arm passes `reg_offs + streak_offs`
  to `build`, so `reg_from_active`'s exclude set covers the streak alongside the register (decision
  state is not program content; otherwise reconstruction would write the six bits back to 0 and
  destroy the counter). This is the one structural change and it applies only to the maintained arm.

## 4. The read/write change

`AllocEraseMaintained.outcome` / `_drop` read/write the maintained streak; the host dict is not read.

- **Read** (majority, threshold 4): `streak_read(o, key)` = the 3-bit counter read from the
  majority of 7 replicas per bit.
- **Increment** (unproductive contact): `cur = streak_read`; if `cur + 1 >= STREAK_N` fire `_drop`,
  else `streak_write(cur + 1)`.
- **Reset** (productive contact, and inside `_drop`): `streak_write(0)`.
- **`streak_write`** is atomic and W-gated: write only the replicas differing from the target;
  refuse the whole transition if that count exceeds `cap = min(32, 8*available_W, energy, material)`;
  charge 1 energy + 1 material per replica into `spent_e`/`spent_m`/`writes` and a dedicated
  `streak_writes` counter.

**One deviation from the design's literal wording, made to preserve the host's drop tick.**
AC96-D1 section 3.4 says the increment is "reached only when the read was `< STREAK_N`, else `_drop`
would have fired". Taken literally (read >= 6 -> drop) that fires the drop on the **7th** consecutive
unproductive contact; the host fires on the **6th** (it increments to 6, then checks `>= STREAK_N`).
The implemented condition is `cur + 1 >= STREAK_N` -> `_drop`, which fires the drop on the same
contact as the host. `TestDropReadsMajority` pins the two arms' drop decision as identical.

## 5. Comparator

The comparator is the **host-streak control vs the maintained arm** (AC96-D1 section 5). The only
difference is where the streak lives.

- **L1 (extension correctness).** `streak_maintained=False` reproduces `ac95.run` byte-for-byte
  (`state_hash`) in the `perm` world on all 8 seeds x 2 histories, and reproduces the frozen
  `ac95_results_v1` `gated` rows in the `none` world (32/32). `TestComparator`.
- **L2 (prefix byte-identity).** The two arms are byte-identical on the shared trajectory up to
  the **first divergence tick**, which is the earlier of two events, both traceable to the
  streak-storage change: (a) the first **paid streak write** (the first development-time
  unproductive contact -- the host dict is free, the maintained write is paid), or (b) the first
  **reconstruction touching a damaged streak bit** -- `reg_from_active`'s exclude set in the host
  control covers only the register, so it resets an ambient-damaged streak bit to 0 (paid), while
  the maintained arm excludes the streak bits and skips it. Measured per individual: 14/16 first
  diverge at the first streak write (ticks 96-107); seeds 6 and 7 diverge earlier (ticks 223 and
  19) by mechanism (b), confined to the streak bits and their 1-replica cost -- not a behavioural
  divergence. The design's "up to the first streak write" is therefore corrected to "up to the
  first divergence".
- **L3 (leak closure, single-step).** With identical maintained state, toggling the vestigial host
  dict `alloc.streak` produces **identical writes** on the maintained arm; the same toggle on the
  host-streak control **changes** the writes (the AC95-D1 probe-2 leak, reproduced).
  `TestLeakClosed`.

## 6. Engineering run (seeds 0-7, `transition='perm'`, damage=True, corrupt=False)

The relinquishment world. The frozen host control relinquishes exactly once per individual and
survives 16/16; the maintained arm diverges (section 7).

| seed | host drop tick | host survives | maint drop tick | maint survives | maint streak_final(key 1) |
|------|----------------|---------------|-----------------|----------------|---------------------------|
| 0    | 8197           | yes           | 8224 (delayed)  | yes            | 0                         |
| 1    | 8222           | yes           | none            | no (8448)      | 5 (stalled)               |
| 2    | 8205           | yes           | none            | no (8444)      | 5 (stalled)               |
| 3    | 8228           | yes           | 8212 (earlier)  | yes            | 0                         |
| 4    | 8205           | yes           | none            | no (8419)      | 5 (stalled)               |
| 5    | 8211           | yes           | none            | yes            | 0                         |
| 6    | 8205           | yes           | none            | yes            | 0                         |
| 7    | 8224           | yes           | none            | no (8444)      | 5 (stalled)               |

(histories 0 and 1 are identical for every seed; the table shows one history.)

Summary over the 16 individuals: **host 16/16 relinquish and survive; maintained 4/16 relinquish
(seeds 0, 3), 8/16 die without relinquishing (seeds 1, 2, 4, 7), 4/16 survive without relinquishing
(seeds 5, 6 — the stale entry expires and the organism re-acquires blind, never firing `_drop`).**

## 7. The divergence, traced to the streak-storage change alone

The maintained arm does **not** reproduce the host's relinquishment behaviour, and the cause is
exactly the one change this study makes: the streak is now a **paid** write (1 energy + 1 material
per replica, atomic under `cap = min(32, 8*W, energy, material)`), where the host dict was free.

- The streak's increments cost material: `3 -> 4` is a 21-replica transition, `5 -> 6` is 14.
- In the `perm` move transient the moved key's income goes to **exactly zero**, so material
  collapses to 0-4 (measured: material=0 from ~t=8222 on seed 1/0 while W is still 3).
- With material <= 4 the cap is <= 4, so the 14-replica `5 -> 6` (and the 21-replica `3 -> 4`)
  are refused **whole**. The streak stalls at 3 or 5, `_drop` never fires, and the organism either
  starves on the stale route (8/16) or escapes by a different path — entry expiry + blind
  re-acquisition (4/16).

This is the AC11/AC12/AC13 wall re-entering through the streak's own paid write: **the
relinquishment decision is itself starved by the very starvation it exists to pre-empt.** AC96-D1
section 3.4 anticipated the refusal mechanism but attributed the binding constraint to W ("at W=2
the 21-replica transition is refused whole"); in the `perm` world the binding constraint is
**material**, not W — material reaches 0 while W is still 3, and a 14-replica reset is refused even
at W=3 when material < 14. This starvation is **damage-independent**: it is the move's income cut,
not the ambient damage stream, that collapses material — the `damage=False` run shows the same
divergence on every individual (the maintained arm's decision signature differs from the host's on
16/16). The two divergence mechanisms are distinct: the **prefix** divergence of section 5 (a paid
write, or a reconstruction skipping a damaged streak bit) is local and confined to the streak bits;
the **starvation** divergence of this section propagates through the economy (material → observation
→ action stream → routes, W/C births, fuel).

The drop **tick** also moves where it still fires (seed 0 delayed 27 ticks, seed 3 earlier by 16):
the paid streak writes feed back through the organism's material, which sets observation bit 1
(material <= 64), which changes the action the program chooses and therefore *when* the unproductive
contacts happen. That feedback is a consequence of the paid write, not a second change.

## 8. Single-step verification (`test_ac96.py`, not hashed — AC17's rule)

All four prescribed checks pass at the single-step level (energy/material topped up, so the paid
write is affordable and the mechanism is exercised cleanly):

- **Leak closed**: identical maintained state + toggled host dict -> identical writes on the
  maintained arm; the host control still leaks (the contrast in one step). `TestLeakClosed`.
- **Damage + repair**: 2 minority replicas -> majority holds -> paid bank-0 restore repairs them.
  `TestStreakDamageRepair`.
- **`_drop` reads the maintained majority**: a streak that reaches the threshold drops exactly like
  the host arm (register set, entry erased, streak reset); the only difference is the 14-replica
  paid reset the host control does not pay. `TestDropReadsMajority`.
- **Productive reset**: `productive > 0` writes the maintained streak to 0 (paid, 14 replicas from
  `0b011`), leaving the register untouched. `TestProductiveReset`.

Plus the offsets invariant and the comparator regressions (host == ac95 byte-identical; frozen
reproduction 32/32; prefix byte-identity up to the first streak write).

## 9. What this does and does not claim

This completes the AC95 state-sufficiency arc's last class-C leak **in mechanism** — the streak is
vulnerable, damaged, repaired, read by majority, and steered by no host memory. It does **not**
claim the internalized streak preserves the relinquishment *behaviour* in the `perm` world: it does
not (section 7), and that falsification is recorded, not hidden. The divergence is a genuine
economic finding — the AC75 relinquishment mechanism's decision state, once made a paid vulnerable
write, is itself starved by the move's income collapse — and it is the honest headline of this
engineering study. No content self-production claim (AC78/AC79 scope unchanged); no claim that a
damaged majority flip on a streak bit is recoverable (4-of-7 is catastrophic, as everywhere).
