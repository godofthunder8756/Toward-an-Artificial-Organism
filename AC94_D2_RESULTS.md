# AC94-D2 — fix: pointer-switch and phase-commit are now one atomic multi-field transition (no host-side transaction state)

2026-09-18. Implemented in a new runner `ac94.py` (ac93.py and every freeze are untouched; ac93.py
sha256 `d9fda66…d514` unchanged). The diagnosis this closes is `AC94_D1_DIAGNOSTIC.md`: at W=2 the
SWITCH branch performed the pointer write and the SWITCH→REMOVE MODE write as two separately-gated
writes, so the pointer advanced while the 21-replica MODE transition was refused, the next tick
re-derived source/target from the advanced pointer and reverted to COPY, and the old source's REMOVE
was permanently skipped; `switch_tick` was logged on the refused transition.

## The fix

`advance()`'s SWITCH branch now calls a new primitive `commit_switch(o, e, target, last)` (gated arm
only), which advances the pointer AND commits the SWITCH→REMOVE MODE transition as ONE atomic
multi-field transition:

```
refuse (write nothing) iff   n_mode > 8*W  OR  n_ptr > 8*W
                             OR  n_ptr + n_mode > energy  OR  n_ptr + n_mode > material
```

On a refusal the pointer does NOT advance, the phase stays SWITCH, and the next tick retries the SAME
source/target pair re-derived from the unchanged pointer. `switch_tick` is recorded only when the MODE
transition actually committed (non-zero return). The same "record only on commit" rule is applied to
the two other phase-transition log fields (`copy_done`, `remove_tick`/`done`).

## Why this direction (and why not the naive atomic sum)

- **Direction (a)/(c) coincide here.** The pointer is the canonical source of `source`/`target`
  (AC87: derive what is derivable), so making the pointer advance atomic with the MODE commit means a
  refused transition is *retried, not re-derived* — the exact behaviour (b) wanted, but without
  storing source/target anywhere. Direction (b) would have required holding the pair across a refusal
  in either vulnerable state (more bits, more writes, a changed economy) or a host object (forbidden
  by the constraint).
- **The naive atomic sum (`n_ptr + n_mode > _cap`) is wrong and would deadlock the switch.** The two
  writes are each bounded by the *per-write* W cap (`_cap = min(32, 8·W, energy, material)`), and
  their sum is up to 14 + 21 = 35 replicas, which exceeds the maximum cap (8·W = 24 at W=3). A
  combined `≤ _cap` check would refuse the switch at W=3 too and succession would never complete. The
  correct condition is **per-write capacity** (`n_ptr ≤ 8·W` AND `n_mode ≤ 8·W`) **plus joint
  funding** (`n_ptr + n_mode ≤ energy` AND `≤ material`). This is exactly the condition under which
  the original two-step sequence would have completed *both* writes, so it refuses precisely the
  cases that produced the inconsistency (or a partial pointer write) and accepts precisely the cases
  that succeeded — it changes nothing at healthy W.
- **Consistency lives in the organism's own vulnerable, maintained state.** The pointer and the MODE
  field are both bank-1 traces, damaged by the ambient stream and repaired by paid majority-restore;
  the atomicity is enforced by the live per-write cap, not by any Python rollback object.

## Verification

1. **Comparator reproduction (the fix is the only change).** `ac94.equivalence_check()`: the `ungated`
   arm reproduces frozen AC92 `intact` byte-for-byte — **32/32 state_hash**. The ungated arm never
   calls `commit_switch`; its two-step frozen sequence is preserved verbatim (only the
   `switch_tick`/`remove_tick`/`copy_done` logging is gated on the write_ctrl return, which is always
   non-zero in the frozen comparator).
2. **Unit tests** (`test_ac94.py`, 10 tests, not hashed per AC17's rule):
   - single-step isolation: `commit_switch` refuses BOTH writes at W=0, W=1, W=2 and commits both at
     W=3; joint-funding refusal when energy < n_ptr + n_mode;
   - the named invariant "a refused transition never advances the pointer alone" asserted across
     W ∈ {0,1,2};
   - `switch_tick`/`remove_tick` recorded only on commit;
   - the ungated ≡ frozen AC92 equivalence re-run inside the suite.
3. **Engineering (seeds 0–7, all 5 arms, 320 rows).** `gated` diverges from `ungated` in state_hash
   only under damage=True (14 of 64 gated rows; the W=2 refusal band); no-damage conditions are
   byte-identical. No outcome field (`completed`, `flipped_still_wrong`, `description_correct`)
   differs between gated and ungated on any individual.
4. **Single-tick close of the D1 defect** (seed 1, corrupt=T, the D1 refusal at t=9714): the refusal
   now shows `ptr 3→3, phase SWITCH→SWITCH` (pointer does not advance alone), the next tick commits
   `ptr 3→0, phase→REMOVE` atomically, and the old source slot 3 is removed (final occupancy
   `[0,0,1,1]` — a healthy rotation, not the stale duplicate the frozen runner left from t=9714).
   "SWITCH ticks where pointer advanced but phase stayed SWITCH": **0** (was the defect).

## Does the fix change any AC93 final-seed outcome?

**It changes state, not outcome.** Running ac94's `gated` arm on finals 4400–4403 and comparing to
frozen `ac93_results_v1`:

- state_hash differs in exactly the **6** conditions where the frozen gated already differed from
  frozen ungated (seeds 4402/4403, damage=True) — i.e. exactly the W=2 refusal cases.
- The succession count is **unchanged** in all 6 (6 stays 6). Survival (`completed`), reconstruction
  (`flipped_still_wrong`), and description correctness are unchanged everywhere.
- The D3 interruption arms (W_block / W_rescue / W_block_ungated) are **byte-identical** to frozen
  ac93 (0/24 mismatches) — they stall in COPY at W=0 and never reach SWITCH, so the gated SWITCH-branch
  fix cannot touch them.

So the old AC93 "1–2 tick delay only" framing was **wrong about the mechanism** (D1 proved a real
pointer/phase/remove inconsistency) but its **outcome implication is confirmed by the fix**: the
headline outcome (survival, reconstruction, succession count) is unchanged.

## What the fix does NOT change — the residual gated/ungated divergence is the gate, not the bug

The fixed gated arm still completes a different succession count than the ungated comparator on some
individuals (engineering: seed 1 gated 6 vs ungated 7, seed 2 gated 8 vs ungated 6, seed 5 ±1; finals:
seed 4403 gated 6 vs ungated 7). This ±1 is **not** the bookkeeping defect — it persists after the
atomic fix — and it is **not** masked: it is a genuine, small consequence of the W=2 MODE refusal
delaying a succession past the SUCC_MIN_SPACING rate-limiter window. The gate binds at W=2 (21 > 16),
the switch waits ~1–2 ticks for W=3, and occasionally that shifts one succession across the 2400-tick
spacing boundary. The AC93 G3 near-equivalence gate already budgeted for this ("succession count may
differ by at most 1"); the fix makes the *mechanism* of that near-equivalence honest (an atomic
retry) without changing its *outcome*. The honest claim for the next protocol: the gate's
organism-level effect is a ±1 succession-count shift under damage, zero effect on survival and
reconstruction.

## Files

- `ac94.py` — the fixed runner (new; ac93.py untouched).
- `test_ac94.py` — the unit suite (not hashed).
- `ac94_engineering_v1/` — engineering run (320 rows, 5 arms, seeds 0–7).
- `_ac94_verify_finals.py`, `_ac94_verify_d3.py`, `_ac94_verify_remove.py`,
  `_ac94_gated_vs_ungated.py`, `_ac94_compare_eng.py`, `_ac94_inspect_frozen.py` — verification
  probes (record of the comparison).

Caveat on `ac93_engineering_v1/`: it is the stale pre-E1-fix artifact (succession counts 86–137, the
truncated-timestamp bug), so it is **not** a valid baseline for the D2 comparison; the valid baselines
are frozen AC92 (comparator) and frozen AC93 finals (E1-fixed).
