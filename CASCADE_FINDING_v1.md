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

The three gaps of `CLOSURE_BOUNDARY_v1.md` are not independent. The **root cause** is the W population
decay (gap b); the function lapse (gap a) is the renewal-capacity bottleneck it produces (24 vs 42), and
the register degradation (gap c) is the downstream of route loss. Closing gap (b) — a W population that
stays at 4 instead of collapsing toward 2–3 — would remove the capacity bottleneck and thereby the other
two gaps in the same move.

## The precise next step (AC69)

The bottleneck is the frozen renewal cap — `min(32, 8·W, energy, material)` — which is **at most 32
replicas per action**, below the 42 replicas two co-aging entries demand, so one entry is unrecoverably
lost once its oldest replicas expire. W=4 alone does not fix it (32 < 42). The candidates, in the frozen
physics, are: (a) raise the cap so one action can hold both entries (a declared world-constant change),
(b) hold one entry per region so 21 ≤ 24 always fits, or (c) stagger the deposits so the two entries do
not age together. Whichever is chosen, the study measures the cascade end-to-end — W population, renewal
capacity, routes held, and survival — and asks whether a single intervention removes all three gaps of
`CLOSURE_BOUNDARY_v1.md` at once.
