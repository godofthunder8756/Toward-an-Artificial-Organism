# AC99-D3 — a paid W-birth-priority rival: the 4436 stall is catalyst-production/priority, and the AC98 "W recovers once" narrative is wrong

Parent: AC99-D2. Engineering only — **no protocol, no freeze**. Runner `ac99_d3.py` (new);
`ac98.py`, `ac99.py`, `ac99_d2.py` and every freeze are untouched (`ac98.py` sha256
`1ae3d373…` unchanged). World: the AC96/AC97/AC98 relinquishment world (`transition='perm'`,
damage on, corrupt off, 16,384 ticks, move at 8192), the AC98 finals 4436–4439, both histories,
binary reserve arm (`ac99_d3.run(..., wb_first=False)`, byte-identical to `ac99.run(reserve=True)`)
vs the W-birth-priority rival (`wb_first=True`).

## 0. Verdict

**The rival keeps W ≥ 3 through the post-move build and the binary 3→4 increment then succeeds —
so on 4436 the bottleneck is catalyst production / priority, not (only) the counter's write cost.**
On the AC98 G1 failure seed 4436 the rival relinquishes, re-acquires both routes, and survives
(both histories), where the binary reserve arm dies at 8430 with the streak stuck at 3. No survival
regression on the other three seeds (0/4).

Combined with AC99-D2, the two rivals triangulate the same failure from opposite directions. The
binary streak's `3→4` increment is 3 logical bits = 21 replicas, so `_cap = min(32, 8·W, energy,
material) ≥ 21` needs **W ≥ 3**. On 4436 the frozen priority order (material contact before W-birth)
starves the W-birth rule during the material-≤-64 window, so W decays below 3 and the increment is
refused. **D2** (Gray encoding) makes the increment 1 bit = 7 replicas, so W ≥ 1 suffices; **D3**
(W-birth priority) keeps W ≥ 3, so the 21-replica increment is affordable. Both independently rescue
4436. The honest reading is that the stall is a *conjunction* — an expensive increment **and** a
starved W population — and either fix alone is sufficient.

## 1. The rival (a paid architectural change)

The acquired program's nine rules are ordered (word 0 = fuel contact, word 1 = material contact
mask 2, word 2 = W-birth mask 64, word 3 = C-birth, words 4–7 = bank rules, word 8 = B-birth). When
material ≤ 64 (obs bit 1) **and** W < 2 (obs bit 6), the material contact (word 1) wins and the stale
channel-1 contact preempts W-birth. The rival swaps the two fixed words:

- **description** (bank 1, the stored priority): word 1 → (mask 64, action 6), word 2 → (mask 2,
  action 1). Installed at acquisition exactly as the frozen description is installed.
- **program** (bank 0, the developed controller): the same two words are rewritten **paid** — 1
  energy + 1 material per changed replica, W-gated by `_cap`. Cost = 2 words × 5 changed logical bits
  × 7 replicas = **70 replicas = 70 energy + 70 material**.

The write is **internal** (no external W supply, no external correct state): it goes through the
organism's own program bank. One implementation note worth recording: the frozen acquisition
endowment is **energy 64**, material 128, so the 70-replica swap exceeds the one-tick energy budget
and is paid **incrementally over the first few ticks** as the body's own fuel→energy conversion
replenishes energy. `priority_writes = 70` on every rival individual (the full declared cost). The
`wb_first=False` path is byte-identical to `ac99.run` (state_hash) on 4436, so the swap is the only
change.

## 2. Per-seed outcome (both histories identical)

| seed | priority    | binary reserve (frozen)                 | W-birth-priority rival                  | regression |
|------|-------------|-----------------------------------------|-----------------------------------------|-----------:|
| 4436 | `[1,3,0,2]` | **dies 8430** (streak stuck 3, W=0)     | **drop@8208, reacquire, survive (W=3)** | no (flip)  |
| 4437 | `[2,0,1,3]` | drop@8220, survive                       | stall@8204 → drop, survive              | no         |
| 4438 | `[0,3,2,1]` | stall@8227 → drop, survive (1 relinquish)| stall@8200 + wlow@8264, **0 relinquish**| see below  |
| 4439 | `[2,1,3,0]` | stall@8220 → drop, survive               | stall@8203 → drop, survive              | no         |

- **4436**: binary dies 8430 (streak stuck 3, W_births_post_move = 0); rival drop@8208, re-acquires
  both routes `[0,1]`, W = 3 throughout, W_births_post_move = 768. The exact `3→4` increment that
  stalls the frozen arm succeeds under the rival at W = 3 (cap 24 ≥ 21).
- **4437/4439**: both arms relinquish + survive; the drop tick shifts by a few ticks (the rival's
  streak cadence changes because W-birth preempts some material contacts). No regression.
- **4438**: a real behavioral difference, not a survival regression. The frozen arm actively
  relinquishes (1 drop); the rival does **not** (0 drops) yet survives holding correct routes `[0,0]`
  — under the W-birth priority the streak never accumulates STREAK_N consecutive unproductive
  contacts, so the stale entry lapses by natural expiry and re-binds instead of being actively
  dropped. This is a cost of the priority change to flag: W-birth-first weakens the *active*
  relinquishment on seeds where the material contact is what drives the streak. It does not change
  survival or the final route state.

## 3. The demand-vs-production verdict

Per the task's decision rule: the rival keeps W ≥ 3 and the binary 3→4 succeeds, so **the bottleneck
is catalyst production / priority** — the frozen material-contact-first order starves the W-birth
rule while material ≤ 64, and W decays below the increment's W ≥ 3 requirement. It is **not purely
write demand**: a priority-only fix (no encoding change) rescues 4436.

The synthesis with D2 is that neither is *the* sole cause. The W-bound 3→4 increment is the proximate
stall, and it has two independent contributing causes, each of which a different rival removes:
(a) the binary *encoding* makes the increment 21 replicas (D2's Gray reduces it to 7), and (b) the
frozen *priority* starves W below 3 (D3's rival restores W ≥ 3). A single fix suffices; the failure
needs both.

## 4. The reconciled W availability-vs-birth trace (item 3)

The AC98 results say the wlow release "releases the 21, material rises above 64, obs bit 1 clears, W
recovers once", and attributes the death to "repeated W-death windows", while that same row records
`W_births_post_move == 0`. Traced per tick on 4436/0 (frozen arm), the narrative is **wrong on all
three claims**.

Frozen 4436, ticks 8227–8235 (post-move):

```
 8227  W=3  mat=67   8228  W=3  mat=62   8229  W=3  mat=55  (contact)
 8230  W=2  mat=55  (wlow release)       8231  W=1  mat=48
 8232  W=1  mat=46   8233  W=1  mat=46   ...  8241  W=0   (then W=0 to death 8430)
```

- **W availability** (the live W population count, `(life[:4] > 0).sum()`): 3 through 8229, then a
  **monotone decay** 3→2 (8230), 2→1 (8231), 1→0 (8241), and 0 forever after — the last W catalyst's
  death is autocatalytically irreversible (no live W parent, so action 6 can never birth again).
  **W never "recovers".**
- **W birth** (action 6 firing): `W_births_post_move == 0` — zero action-6 birth events after the
  move. (Note: in the AC9 line `e['W_birth']` counts action-6 births of bank 0 *and* the memory-region
  catalysts, so 0 means the W-birth *rule* produced no birth of any kind post-move.)
- **"material rises above 64" is false.** Material goes 67→62→55 and then stays at 46–55 — it never
  clears 64. The wlow release at 8230 credits +21, but the same tick's streak increment (1→2, 14
  replicas) and disarm write (7 replicas) spend exactly 21, so material is unchanged (55) and obs bit
  1 stays set. The material contact therefore keeps preempting W-birth.
- **"obs bit 1 clears" is false** (material stays ≤ 64, obs bit 1 stays set), and the corollary
  **"W recovers once" is false** (W monotonically decays, never increases).

The correct mechanism: the move makes key 1's entry stale; material ≤ 64 sets obs bit 1; the material
contact (word 1, mask 2) preempts W-birth (word 2, mask 64) every tick, so W-birth never fires; W
decays 3→2→1→0; the streak's 3→4 increment (needs W ≥ 3) is refused; the entry expires into blind
re-acquisition; W=0 collapses C (which needs a W parent to birth), conversion stops, energy drains,
death at 8430. The failure attribution must rest on the **availability trace** (a single monotone W
collapse), not on births and not on any "recovery" — there is none. "Repeated W-death windows" should
read "a single irreversible W collapse (3→0)".

## 5. What this does and does not establish

- **Established:** on the AC98 G1 failure seed 4436, a paid W-birth-priority rival (no encoding
  change) keeps W ≥ 3, lets the binary 3→4 increment succeed, and the organism relinquishes +
  re-acquires + survives — so the failure's catalyst-production/priority component is real and
  independently sufficient. The AC98 "W recovers once" narrative is corrected (W never recovers; it
  monotonically collapses 3→0 with zero post-move W-births).
- **Honest residuals:** (a) the priority change is not a free win — on 4438 it removes the active
  relinquishment (0 drops; the stale entry lapses by natural expiry instead), a cost of starving the
  material-contact rule; (b) the swap costs 70 energy + 70 material, paid over the first few ticks
  because the 64-energy acquisition endowment cannot fund it in one action; (c) the rival and D2's
  Gray are two different fixes for the same W-bound increment — the honest finding is that the stall
  requires *both* an expensive increment *and* a starved W population, and either fix alone resolves
  it.
- **Boundary (unchanged):** this is a rival's *architectural* rule-order change, not a new
  capability; `advance()` and `prog.choose` remain supplied format-level machinery; the reserve is
  still a fixed minimum reserve (not an acquired allocation); no autopoiesis claim. Whether the
  W-birth priority should become the AC99 architecture is D4's decision, not this task's.

## 6. Verification

- `test_ac99_d3.py` 10/10 green: the cost (10 bits / 70 replicas), the description swap (word 1/2),
  the rebuilt-program order (word 1 = mask 64 action 6, word 2 = mask 2 action 1), byte-identity of
  `wb_first=False` with `ac99.run` on 4436, the recorded 4436 flip (binary dies / rival survives +
  relinquishes + W=3), the 70-replica paid swap, and the W reconciliation (monotone W decay, zero
  post-move W-births, material never clears 64).
- `test_ac99.py` 6/6, `test_ac99_d2.py` 10/10, core AC1–9 suite 56/56 — all green.
- No frozen runner modified: `ac98.py` sha256 `1ae3d373…` unchanged; `ac99.py`, `ac99_d2.py`,
  `ac97.py` and every earlier freeze untouched.
- Data: `ac99_d3_engineering_v1/` (16 rows: 4 seeds × 2 histories × frozen/rival), `results.json`
  with the priority-change cost and the per-individual comparison.

## Files

- `ac99_d3.py` — the runner (new; `wb_first_description`, the W-birth-first program swap paid over
  the first few ticks, `run(..., wb_first=...)`, `collect`, `frozen_reproduction`, the W trace).
- `test_ac99_d3.py` — verification only, **not hashed** (AC17's rule).
- `ac99_d3_engineering_v1/` — `rows.jsonl`, `results.json`. No `pre_run_snapshot.json` (no freeze).
- Scratch (measurement only): `_ac99_d3_smoke.py`, `_ac99_d3_verify.py`, `_ac99_d3_wtrace.py`,
  `_ac99_d3_reconcile.py`, `_ac99_d3_rivalstreak.py`, `_ac99_d3_costprobe.py`, `_ac99_d3_clean.py`.
