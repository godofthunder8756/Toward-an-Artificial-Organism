# AC95-D2 — reset progress in maintained state; logs strictly observational

**Runner:** `ac95.py` (new; derived from `ac94.py`, which is untouched). **Task:** close the
class-C leak AC95-D1 found on the timer path, and make the succession observer strictly
observational. Engineering step — not frozen (the protocol + finals are AC95-D4).

## What was fixed

The one host-side operational leak on the timer path — `succ._entry['timer_reset_done']`, a Python
dict key steering `reset_timer` vs `increment_timer` in `advance()` — is moved into the organism's
own vulnerable, maintained state as a single **reset-in-progress (RIP) bit** in the CTRL register's
spare bit 17 (`TIMER_BITS=13` occupies bits 4–16, so bit 17 is free in the gated arm).

- `rip(o)` reads bit 17 by majority (`traces[1, RIP_OFFS].sum() > 3`); `RIP=1` = reset pending,
  `RIP=0` = count-up.
- `write_rip(o, e, val)` is an **atomic, W-gated, paid** write (1 energy + 1 material per replica,
  under `_cap` like the MODE field). Refused whole at W=0 — the machinery-dependence the timer
  already has.
- The succession-start transition sets `RIP=1` (right after `write_ctrl` commits `active=1`); the
  reset loop drives the counter toward 0 and clears `RIP=0` when `timer_value(o)==0`.
- The RIP bit is **inside `CTRL_OFFS`**, so the ambient bank-1 damage stream reaches it and
  `reg_ctrl` repairs it — it is the organism's state, not host memory.

The succession observer (`succ._entry` / `succ.log`) is now strictly observational: the fixed
architecture reads **no** observer field back to steer a write or branch. The remaining fields
(`copy_done`, `switch_tick`, `remove_tick`, `done`, `source_intact_at_switch`, `verified_valid`,
`target_matches_source`) are written-only record, consumed by `run()` after the loop for gates and
reporting.

## Why a maintained bit, not a derivation

D1's suggested fix — "derive reset-done from `timer_value(o)==0`" — is **not exact**. The flag is a
*latched mode bit* (reset vs count-up), not a function of the current counter value: once the reset
completes (counter 0) the machine must switch to count-up and stay there while the counter refills
toward full *during the same succession*, so `timer_value(o)==0` is also true at the start of
count-up and cannot tell the two apart. The counter's bit pattern (unary prefix in count-up, suffix
in reset) fails at the two endpoints — all-full means "succession just started, reset needed" while
`active`, and "count-up completed" while idle. A maintained bit has no such edge case and is the
exact relocation of the flag.

## Verification (all green)

`test_ac95.py` (10 tests, `unittest`, ~3.3 min — the comparator byte-identity tests run 64 full
16,384-tick simulations):

- **Reviewer's isolated harness closed.** Identical idle state (counter=5, `active=0`), the
  observer cleared vs kept vs carrying a stale `timer_reset_done=False/True` all return **the same**
  `timer_value=6`, 7 energy, 7 ctrl writes. The write is now a function of maintained state alone.
- **RIP bit is maintained state.** Reset completes through the RIP bit (mid-reset organism clears to
  0 and clears RIP, no host memory); RIP damage (2 minority replicas) is repaired by `reg_ctrl`;
  `write_rip` is W-gated and paid (refused at W=0, 7 replicas at W=3).
- **Observer-discard equivalence.** Replacing `succ` with a fresh object at a mid-run tick
  (`run(..., swap_succ_at=t)`) leaves the gated trajectory **byte-identical** (state_hash) at swap
  ticks 2000 and 8192, and across engineering seeds 0–3.
- **Comparator arms untouched.** `ungated` reproduces frozen AC92 `intact` byte-for-byte (32/32);
  `split` reproduces frozen AC94-D4 `split` byte-for-byte (32/32).

Engineering (gated, seeds 0–7, all 4 damage×corrupt conditions, 64 rows): all complete, 6
successions per individual, `flipped_still_wrong=0`, `description_correct=130`, `split_events=0`.
The fix changes no behaviour — succession count, survival, reconstruction and description integrity
are field-for-field identical to the frozen AC94-D4 `gated` rows.

## The one intended consequence: the flag now costs

The RIP bit's paid writes (set + clear, up to 14 replicas per succession) shift the gated arm's
economy by a small, bounded amount relative to AC94's gated arm (measured on finals 4404–4407:
`ctrl_writes` +84 ≈ 6 successions × 14; final energy −4, material −28, fuel +40 on one seed — the
organism re-balances). Categorical behaviour is unchanged. This is the *intended* cost of making the
reset-progress flag vulnerable, paid-maintained organism state instead of a free host dict; it is
reported here so it is not mistaken for a new divergence.

## Deferred, not silently left: `alloc.streak` (the second class-C leak)

D1's audit found a second class-C leak: `alloc.streak`, the AC75 relinquishment failure-streak dict
(`ac12.py:145`, driven by `AllocErase.outcome`), which gates the `_drop` relinquishment write and is
read on **every** arm including the `ungated`/`split` rivals. It is **inert in the finals**: with
`transition='none'` no route goes stale, the streak never reaches `STREAK_N`, and measured
`relinquishments == 0` for every gated/ungated row of the AC94-D4 finals. Its fix — moving a per-key
3-bit counter into maintained, vulnerable, repairable state — is architecturally the *same* gated-only
relocation as the RIP bit, but needs its own storage/damage/repair design (6 bits, a damage stream and
a repair path not specified by this task), and it cannot ride the byte-identity comparators (it would
change their digests). **This is a follow-up, not part of AC95-D2**; the AC95 state-sufficiency claim
must not be read as covering it until it is closed.

## Files

- `ac95.py` — the fixed runner.
- `test_ac95.py` — the verification suite (not hashed, AC17's rule).
- `_ac95_*` — throwaway probes used during development (not part of any freeze).
