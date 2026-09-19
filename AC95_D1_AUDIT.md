# AC95-D1 — Audit of persistent host-side variables on the operational control path

**Runner under audit:** `ac94.py` (AC94-D4 architecture: atomic pointer/MODE switch, W-funded
rate-limit timer, succession controller state in bank 1). The frozen dependencies it builds on
(`ac76`, `ac71`, `ac12`, `ac12_memory`, `ac9`, `ac9_priority_v2`, `ac9_memory`, `ac5`,
`ac5_program`, `ac4`, `ac4_transport`, `ac1`) are shared frozen physics and are out of scope for
this audit except where an object they define (`ac12.Alloc`) is instantiated and driven by the
ac94 runner itself.

**Method.** Swept the operational code paths of `ac94.py` — `advance()`, `maintain()`, the
`write_*` / `reg_*` / `increment_*` / `reset_*` primitives, `commit_switch`, `run()`, and every
module-global / config / object field they read — and applied the task's leak test: *hold the
organism's full maintained state fixed, toggle/clear the host variable, and check whether the
next tick's writes differ.* Two deterministic single-step probes (in `ac95_d1_probe.py`) run the
test; the outputs are reproduced in section 2.

**Classification.**
- **(A) in maintained organism state** — lives in `body.traces[...]`, damaged by the ambient
  stream, repaired by a paid majority-restore. (The counter bits, the pointer, the CTRL MODE
  field, the description slots.)
- **(B) derived from maintained state** — recomputed each tick from (A); holds nothing that
  survives between ticks. (`source`/`target` from `read_pointer`, `active`/`phase` from
  `ctrl_fields`, `timer_value`.)
- **(C) host-side operational leak** — persists in a Python object / dict / global AND
  influences a write or branch, so deleting or re-initialising it changes the trajectory.

---

## 1. The inventory

| Variable | Class | Where read (file:line) | Changes a write/branch? | Notes |
|---|---|---|---|---|
| `body.traces[1, PTR_OFFS]` (pointer) | A | read_pointer `ac94.py:267` | yes — source/target derivation | 2 bits × 7 replicas, damaged + `reg_pointer`/`write_pointer` maintain it |
| `body.traces[1, CTRL_OFFS[:4]]` (MODE: active+phase) | A | `ctrl_fields` `ac94.py:292`, `write_ctrl` `:368`, `commit_switch` `:490` | yes — the succession phase machine | damaged + `reg_ctrl` repairs; atomic all-or-nothing write |
| `body.traces[1, CTRL_OFFS[4:4+TIMER_BITS]]` (timer counter) | A | `timer_value` `:402`, `reset_timer` `:416`, `increment_timer` `:438` | yes — `rate_ok` | unary counter, damaged + `reg_ctrl`; replaces the LAST timestamp |
| `body.traces[1, slots]` (description) | A | `read_slot` `:262` | yes — copy/verify/rebuild | 4 slots × 130 bits × 7 replicas |
| `source`, `target` (locals in `advance`) | B | `ac94.py:615-616` | yes — but recomputed from `read_pointer` every tick | hold nothing across ticks |
| `active`, `phase`, `last` (from `ctrl_fields`) | B | `ac94.py:589` | yes — branch on `phase` | derived from CTRL field each tick |
| `timer_value(o)` | B | `ac94.py:597,602` | yes — `rate_ok`, reset-done check | derived from counter bits each tick |
| **`succ._entry['timer_reset_done']`** | **C** | `ac94.py:593` (read), set `:598,612,620` | **yes — steers `reset_timer` vs `increment_timer`** | the known leak; see §2.1 |
| **`alloc.streak`** (dict {0,1}) | **C** | `ac94.py:816-817,814,854` (via `AllocErase`); base `ac12.py:175-176,192` | **yes — gates the `_drop` relinquishment write** | NEW leak; see §2.2 |
| `succ._n` | B/observational | `ac94.py:610,618` (stamped into `succ._entry['n']`), incremented `:613,621` | **no** | a cycle index for logging only; never read for any write/branch (verified by inspection) |
| `succ._entry` other fields: `n, source, target, start, source_correct, copy_done, verified_valid, target_correct, switch_tick, source_intact_at_switch, target_matches_source, remove_tick, old_source_empty` | observational | written `ac94.py:610-687`; read only in `run()` for gates/reporting `:980-1010` | **no** | per-cycle log; `done` gates only `succ.log.append` (a host list), never an organism write |
| `succ._entry['done']` | observational | `ac94.py:688` (log append), `:980,1009` | no | gates the host log append, not a body write |
| `succ.mode` | config | `ac94.py:587` (early-return guard), set `:898` | yes (whether `advance` runs at all) but immutable per run | fixed `'real'`/`'none'` at construction; not operational memory |
| `succ.encoded` | observer ref | `ac94.py:611,619,635,653-654,668-669` | **no** — only computes log/scoring fields | the correct-description reference; scoring knowledge, never feeds a write or branch |
| `succ.log` | observational | `ac94.py:688,980-1010` | no | serialised into `succession_log` |
| `alloc.offs` | B (cached) | `ac94.py:824,843`; base `allowance` `ac12.py:153,163` | yes (locates the register bit) but immutable | `resolve_offsets`/`register_offsets` once at acquisition; can't drift |
| `alloc.shadow` | vestigial | set `ac94.py:889`; **never read** in the `allocate` arm | no | host copy of program bank; used only by ac12's `protected`/`no_learning` arms, which ac94 does not use |
| `alloc.now` | vestigial | set `ac94.py:922`; **never read** in the `allocate` arm | no | host-clock mirror; only ac12's `switch` calibration arm reads it |
| `alloc.log` | observational | `ac94.py:1033-1034` | no | `dropped`/`restored`/`relinquish_tick` for reporting |
| `alloc.arm` | config | `ac94.py:809`; base `ac12.py:157-171` | yes (arm dispatch) but immutable | `'allocate'` for every ac94 arm |
| `alloc.rng`, `alloc.opportunities` | inert | — | no | only the `random`/`fixed_schedule` arms use them; ac94 does not |
| `cfg` dict (`repair, regen, succession, ctrl_maintain, gate_ctrl, atomic_switch, ac_arm, block_W, block_tick, restore_tick, direct_restore`) | config | `maintain` `:697-710`, `build` `:777`, `make_birth` `:747-752`, `run` `:894-897,946` | yes — but fixed per arm from `ARM_PARTS` | the experiment's arm definition, immutable during a run |
| `now` (host tick) | external clock | `advance` `:599,604,609`; `make_birth` via `ns['now']` `:752`; set `step.__globals__['now']=t` `:949` | yes — `now % TIMER_K` coarse-tick, `now - last` (ungated) | environment time, not organism state; see note below |
| `reg_offs` (register offsets) | B (cached) | `reg_from_active` `:564-566`, `run` `:973` | yes (excludes register bits from rebuild) but immutable | `resolve_offsets` once at acquisition |
| `ac12.PORTS / YIELD_M / YIELD_F / MOVE_KEYS / MOVE / DEV / REGISTER_THRESHOLD` | config | set `run` `:881-884`, read by ac12 frozen code | yes (world constants) but immutable during the loop | reset at the top of every `run()` |
| `e` (event dict) | per-tick | write primitives `:329-451,504-572,835-861` | — | fresh `ac9.event()` each tick; accumulates ledger counters, not persistent |
| `total` (run-level dict) | observational | `run` `:952-953` | no | aggregates `e` across ticks for reporting |
| `rng`, `rng1` | external env | `run` `:901-902,923-937` | yes (damage/contact streams) | deterministic RNG streams, environment not organism state |
| `base_map` / `mapping_at` | external env | `run` `:900,950` | yes (world mapping) | the environment's port mapping |

### The two class-C rows in detail

**(C1) `succ._entry['timer_reset_done']` — the known leak.** A Python dict key on the
`Succession` object that remembers whether the post-succession counter reset has completed, and
steers `advance()` between the reset branch (`reset_timer`) and the increment branch
(`increment_timer`). It is read at `ac94.py:593`:

```python
entry = succ._entry
if entry is not None and not entry.get('timer_reset_done'):
    if active:
        reset_timer(o, e)
        if timer_value(o) == 0:
            entry['timer_reset_done'] = True
elif now > 0 and now % TIMER_K == 0:
    increment_timer(o, e)
```

The flag is set to `True` exactly when `timer_value(o) == 0` — so it is *redundant with the
maintained counter itself*: the "reset is done" condition is derivable from (A) state as
`timer_value(o) == 0`. The host flag is therefore pure operational memory that could steer the
machine away from its own state.

**(C2) `alloc.streak` — a new leak.** A host-side dict `{0:0, 1:0}` on the `AllocErase` object
(inherited from `ac12.Alloc.__init__`, `ac12.py:145`) that counts consecutive unproductive
contacts per key and gates the relinquishment write. `AllocErase.outcome` (`ac94.py:812-818`):

```python
if e['productive'] > 0:
    self._restore(o, e, key); self.streak[key] = 0; return
self.streak[key] = self.streak.get(key, 0) + 1
if self.streak[key] >= ac12.STREAK_N:
    self._drop(o, e, key)
```

`_drop` (AC75's erase-on-relinquish) writes the decision register bit to 1 (7 replicas, paid) and
erases the memory entry. The streak survives in the Python object, **not** in `body.traces`, and
it is read/written on **every arm** (all ac94 arms use `ac_arm='regen'` → `alloc=AllocErase('allocate', …)`,
and the injected step calls `alloc.outcome` after every contact). So this leak changes the
trajectory of *every* arm, including the `ungated` / `split` comparator rivals.

It is "declared supplied machinery" in `ac12.Alloc`'s docstring ("the unproductive streak is input
derived from the organism's own realized contact outcomes, experience not the answer"), but it is
nonetheless host-side persistent state that gates a write — exactly the class this audit exists to
inventory. In the AC94 finals the intervention is `transition='none'`, so routes never go stale
and `streak` essentially never reaches `STREAK_N` with a bound entry; the classification is about
the mechanism, not its firing frequency (and it *does* fire under `transition='perm'`, which the
runner still supports via `mapping_at`).

### Notes on the non-leaks (things checked and cleared)

- **`succ._n` does not gate anything.** It is read only to stamp `succ._entry['n']` (a log field)
  and incremented; no write or branch consumes it.
- **`succ.encoded` does not influence a write or branch.** It is the observer's correct-description
  reference, used only to compute the log/scoring fields `source_correct`, `target_correct`,
  `source_intact_at_switch`. Every actual write decision in `advance()` reads only maintained state
  (`read_slot`, `read_pointer`, `ctrl_fields`, `timer_value`). This is the legitimate
  "observer knows the correct content" boundary (AC85).
- **`alloc.offs` / `reg_offs` are cached derivations (B), not leaks.** They are resolved once at
  acquisition from the dead-rule index and are immutable for the run; the offsets cannot drift
  because the program-bank structure is fixed.
- **`alloc.shadow` and `alloc.now` are set but never read** in the `allocate` arm (they serve
  ac12's `protected`/`no_learning` and `switch` arms respectively, none of which ac94 uses).
  `alloc.shadow` is a latent hazard (a host copy of the program bank) but currently inert.
- **`now` (the host tick) is an external clock, not organism state.** It drives the coarse-tick
  increment schedule (`now % TIMER_K`) and, in the **ungated comparator only**, is written into the
  maintained LAST field as the rate-limiter timestamp (`write_ctrl` with `gate=False`,
  `ac94.py:388-398`). That timestamp write is precisely the AC88/AC92 distinct-resource dependency
  that AC93/D3 eliminated on the gated architecture; the `ungated` arm keeps it *by construction*
  (byte-identical to frozen AC92). It is a host-state dependency worth recording, but it is the
  frozen comparator's known behaviour, not a new leak to close.
- **The `ungated`/`split` comparator arms.** `timer_reset_done` is read only when `gate_ctrl` is
  True, i.e. by `gated`, `split`, `timer_block`, `timer_rescue` — and **not** by `ungated` /
  `ungated_block` (they take the timestamp branch). `alloc.streak` is read by **all** arms
  (all use `arm='allocate'`). A leak on the relinquishment path therefore perturbs the rivals
  too; a leak on the timer path does not reach the ungated comparator.

---

## 2. Reproductions (the leak test)

Deterministic probes in `ac95_d1_probe.py` (run with `.venv/bin/python -B`). Each holds the
organism's maintained state fixed and toggles one host variable, then compares the next tick's
writes.

### 2.1 `timer_reset_done`

Organism with active=1, phase=COPY, three timer bits majority-set, energy/material topped up,
target slot pre-matched to source (so the COPY branch writes nothing). Same `now=123` (not a
multiple of `TIMER_K`, so the increment branch would be silent). Only the flag differs:

```
timer_reset_done=False: timer_resets=1, timer_increments=0, ctrl_writes=35, timer_value_after=0
timer_reset_done=True : timer_resets=0, timer_increments=0, ctrl_writes=14, timer_value_after=3
```

The 21-replica difference (35 vs 14) is exactly the timer reset clearing the 3 set counter bits
(3 × 7 replicas); the residual 14 is the COPY→VERIFY MODE transition common to both. Toggling the
host flag alone changes the writes and leaves the counter at a different value.

### 2.2 `alloc.streak`

A real gated organism is driven 700 ticks so key 0 is bound at (region,slot)=(0,0). The full
maintained state is then snapshotted and restored identically for two `outcome` calls differing
only in `streak[0]` (0 vs `STREAK_N-1 = 5`), with `productive=0`:

```
streak[0]=0: register_bit False->False, entry_life_max 58->58, dropped=[],        streak_after=1
streak[0]=5: register_bit False->True,  entry_life_max 58->0,  dropped=[[0,0]],   streak_after=0
```

With `streak[0]=5` the single unproductive contact trips the threshold and `_drop` fires: the
decision register bit flips to relinquished (False→True), the memory entry is erased
(life 58→0), and the drop is logged. With `streak[0]=0` nothing is written. The maintained state
was identical at the call; only the host dict differed.

---

## 3. The definitive (C) list for D2

The following host-side variables persist in a Python object and influence a write/branch, and
must be closed by D2 (reset progress held in maintained/derived state, logs strictly
observational):

1. **`succ._entry['timer_reset_done']`** — the succession timer's reset-progress flag. Fix
   direction: derive "reset done" from the maintained counter (`timer_value(o) == 0`) rather than
   a host flag; the flag is already set exactly when that condition holds.

2. **`alloc.streak`** — the relinquishment failure-streak dict that gates `_drop`. Fix direction
   (for D2/D3): move the per-key unproductive-contact count into maintained, vulnerable state (or
   derive it from maintained state), so the erase-on-relinquish decision does not depend on a
   Python dict. Note this is read on every arm, so it is the single most pervasive host-side
   control-path dependency in the current runner.

Everything else enumerated above is either (A) maintained organism state, (B) derived/cached
from it, config (fixed per arm), an external input (clock/RNG/mapping), or observational
logging — and needs no change for state sufficiency.

---

## 4. AC95-D3 addendum (reset-interruption arms)

D3 added `reset_block`/`reset_rescue` (a mid-reset W cut + machinery-only rescue) and `cut_W`. No new
class-C dependency: the reset completion is carried by the maintained RIP bit (D2's fix), and the
observer-discard check at the rescue tick (`swap_succ_at='rescue'`) is byte-identical — the trajectory
does not depend on `succ._entry`. The intervention-schedule locals in `run()` (`reset_start`,
`reset_progress_at_cut`, `reset_completed_tick`, `reset_cut_done`, `reset_restore_done`) are external
experimenter inputs that time the cut/restore off the organism's own RIP bit and are recorded as
endpoints; they are **not** read by the injected step (they live outside `ns`). `alloc.streak` (C2)
remains deferred, unchanged from D2.
