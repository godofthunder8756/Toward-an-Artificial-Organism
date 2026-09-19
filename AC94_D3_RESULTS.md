# AC94-D3 — the rate limiter becomes a bounded, resumable, machinery-dependent timer

2026-09-18. Engineering step (not a freeze). D4 will write the protocol and run finals.

D2 closed the succession-atomicity defect (pointer advance + SWITCH→REMOVE MODE as one atomic
commit). D3 closes the boundary the task names: the rate limiter's start timestamp (the LAST
field) was still funded by **energy + material alone** — the AC88 distinct-resource model, kept by
AC93 errata E2 because its 35–69-replica value delta cannot fit the W cap `8·W=24`. E1 established
only that the *existing timestamp write* fails under the smaller budget; it did not establish that
correct rate limiting needs a W-independent write service. D3 replaces the timestamp with a
**W-funded unary counter**, so the rate limiter is now a service the produced W catalyst performs,
like every other coordinator write.

## The mechanism (the chosen alternative)

A unary (thermometer) **counter** living in the CTRL register's former LAST field
(`TIMER_BITS = 13` bits, `TIMER_K = 200` coarse ticks):

- It counts **up** from 0 (the natural all-zero acquisition state) to `TIMER_MAX = 13`; the
  succession may fire only when the counter is full.
- Each `TIMER_K` host ticks one bit is set 0→1 (`increment_timer`, **atomic**, ≤7 replicas,
  W-gated by `_cap`). At W=0 it is refused whole — the counter freezes.
- A succession start **resets** it to 0 (`reset_timer`, **resumable**, monotone clear, W-gated):
  the 91-replica reset is paid incrementally across actions, never truncated (the E1 failure mode).

The counter reuses the frozen LAST field, so the ambient damage stream and `reg_ctrl` already
cover it — it is vulnerable and paid-maintained by construction, with **no new storage layer** and
**no pending target to store** (the reset target is the constant "all-set", the increment target is
"lowest clear bit").

## Why the counter, and why not the alternatives (recorded)

- **Resumable timestamp with a stored target** (option b): needs a separate pending-target field
  (a second 14-bit write to maintain) and still leaves a torn-value-read window unless the write
  order is disciplined. Rejected as more moving parts for no gain over the counter.
- **Coarse/compressed timestamp** (option a): the per-succession write is the Hamming distance
  between values ~2400/K apart, still ~3–5 bits (21–35 replicas) — it does **not** reduce the write
  below the W cap, and it has the same quantisation jitter. Only a representation whose per-step
  delta is one unit is genuinely bounded; that is the counter, not a timestamp.
- **Count-down per tick** (option c, literal): a per-tick decrement costs ~2 bits × 7 × 16384 ≈
  229k replicas — ~6× the organism's total material income. The coarse phase (every `TIMER_K`)
  is what makes it affordable; the count-up direction is chosen so the initial state is the natural
  all-zero substrate (no host-supplied initial value).

So the design is option (c) *countdown* with a coarse phase, expressed as a count-up unary counter.

## Verification

1. **Runner correctness (regression).** `equivalence_check`: the `ungated` comparator reproduces
   frozen AC92 `intact` **byte-for-byte, 32/32 state_hash**. The D3 change touches only the gated
   arm's rate limiter.
2. **E1 failure reproduced, then eliminated.** The E1 mode is structural to a timestamp (its write
   is bounded by the value delta, so a 24-replica budget truncates the low bits and the rate limiter
   reads a small `last` and fires continuously, 86–137 successions). The counter has no such write:
   the increment is a single bit (≤7 replicas) and the reset is resumable, so there is no
   "permanently truncated value" state. Pinned in `test_ac94.TestTimerPrimitives`.
3. **Healthy rate.** The `gated` arm (W-funded counter) holds **6 successions** per individual,
   16/16 complete, `fw = 0`, W=3, C=2 — the healthy band, not the runaway 86–137. The count is 6
   rather than the frozen 6–7 because the coarse timer quantises the spacing to
   (`TIMER_MAX−1`)·`TIMER_K`..`TIMER_MAX`·`TIMER_K` = 2400–2600 ticks (measured first succession
   2600–2637, spacing ~2566–2665); the frozen 7th succession was a *torn-timestamp* artifact the
   bounded timer eliminates. This is the honest re-classification: a clean 6, not a defect.
4. **Machinery-dependence (cut W → timer degrades).** `timer_block` cuts bank-0 W at t=1000 (W=0 at
   1007–1063). The counter freezes at **5** (measured `timer_at_W_empty = 5 < 13`),
   `timer_increments_after_W_empty = 0` in **16/16**, the succession never arms (`successions = 0`),
   and the organism dies (W=0, C=0, deaths 1237–1273) via the AC13 cascade. `timer_rescue`
   (machinery-only re-seed at t=1100) lets the counter resume: 16/16 complete with 6 successions,
   W=3, C=2. Read the **live** timer at W=0/death, not `timer_end` — the post-mortem damage stream
   ORs the counter bits to 1, so `timer_end` reads full in the blocked arm (the AC79 distinction).
5. **No new W-independent write.** `write_ctrl` on the gated path now writes the MODE field only;
   the LAST timestamp write is gone. After D3, every paid write the coordinator and reconstruction
   machinery performs is W-gated. What remains non-W-gated (unchanged, Decision 3): machinery
   production and memory-region renewal — both enacted by produced catalysts, not a host service.

## Files

- `ac94.py` — the runner, extended with the D3 counter (D2's `commit_switch` and the frozen
  comparator untouched; `ungated` ≡ AC92 by the equivalence check).
- `test_ac94.py` — 15 tests (10 D2 + 5 timer), all pass; not hashed (AC17 rule).
- `ac94_d3_engineering_v1/` — 160 rows (8 seeds × 2 histories × 10 conditions), `pre_run_snapshot.json`.
- `references/ac94-d3.md` (skill) — the design lessons.

## Carried forward to D4

D4 freezes the protocol on disjoint final seeds with the four gates above as the prespecified set
(plus a determinism rerun). The coarse-timer quantisation (6 vs 6–7 successions, spacing 2400–2665)
is a declared property to report, not a defect; if a protocol wants the exact frozen count, the
`TIMER_K`/`TIMER_BITS` pair must be re-chosen, but the mechanism's claims (bounded W-funded writes,
resumable reset, machinery-dependence) do not depend on the exact spacing.
