# Cascade finding v1: the three closure gaps are one cascade rooted in W decay

2026-09-16. Diagnostic on the AC67 closed arm (seed 0, history 0). This unifies the three gaps of
`CLOSURE_BOUNDARY_v1.md` into a single causal chain.

## The measured chain

1. **W decays to 3.** One of the four core W sites dies and is not re-birthed promptly, so the organism
   runs with `interior_W = 3` rather than 4.
2. **Renewal capacity is 8 × interior_W = 24.** The frozen renewal law writes at most
   `min(32, 8·W, energy, material)` replicas per action. At W=3 that is 24.
3. **Two co-aging routes need 42 renewals.** Both routes live in region 0 (demand `[42,0]` = two entries ×
   21 replicas = 3 bits × 7). They were deposited close together during growth and age together, so both
   cross the `life ≤ 16` threshold at once.
4. **24 < 42, so one entry expires.** The renewal (action 3) is triggered correctly by the aging signal
   (urgent bit fires at `life ≤ 16`, `ac9.observe` line 59), but it can only rewrite 24 of the 42 aging
   replicas in one action, and the entries age faster than the staggered renewals can cover both.
5. **Expiry is irreversible.** `ac9_memory.age` clears the bits of an expired replica
   (`memory.bits[expired] = 0`), so once a replica reaches life 0 its value is gone and `decoded_slot`
   returns `None` — the renewal can no longer recover it (`if entry is None: continue`).
6. **Route loss cascades.** The lost route means contacts fail, the failure streak reaches 6, `_drop`
   fires, the register is set to 1 (the majority-directed repair then cements it — gap (c)). The
   whole-organism W decay that started it is the same bimodality as gap (b).

## The consequence

The three gaps of `CLOSURE_BOUNDARY_v1.md` are causally connected — the route loss (gap a) drives the
contact failures that drive `_drop` (gap c), and the W decay that tightens the renewal budget is the same
bimodality as gap (b). But the **capacity is not the root cause**: an engineering test that raised the
renewal cap from `min(32,8·W,…)` to `min(48,16·W,…)` only *delayed* the route loss (route 0 lost at
~1024 instead of ~891) — it did not hold the routes. So the bottleneck is a **renewal-timing failure**,
not a budget one: the renewal is triggered correctly by the aging signal and runs, yet it cannot save an
entry whose oldest replicas reach the irreversible expiry (`life → 0`, bits cleared) before the renewal
rewrites them.

## The precise next step (AC69)

The open question is *why* the triggered renewal misses the expiring replicas — the leading candidates
are (a) a life-value spread across an entry's 21 replicas (some at `life ≤ 16` when the oldest are
already at `life 1`, so they expire one tick before the renewal reaches them), or (b) the one-tick
ordering where `mem.age` expires a `life == 1` replica before the renewal action runs in the same step.
AC69 instruments the renewal — per-tick `life` histogram of an expiring entry, and the exact tick order
of `mem.age` vs `renew_alloc` — to pin which, then makes the smallest declared change that lets the
renewal win the race. Until that race is measured, the route-lapse mechanism is stated as *timing*, not
capacity.
