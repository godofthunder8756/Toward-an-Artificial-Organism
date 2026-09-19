# AC95-D3 — interrupt during the multi-tick reset, resume from internal state alone

**Runner:** `ac95.py` (extended from the D2 runner; `ac94.py` untouched). **Task:** close the AC94
coverage gap — the multi-tick counter RESET (the resumable 91-replica clear at succession start) had
never been interrupted live; AC94's `timer_block`/`timer_rescue` cut W during the counter's first
COUNT-UP. Engineering step — not frozen (the protocol + finals are AC95-D4).

## The physics finding that shaped the intervention

The reset is **5 ticks** at W=3 (the counter clears 3 bits ≈ 21 replicas per tick: 13 → 10 → 7 → 4 →
1 → 0). The bank-0 birth-block (`make_birth`) depletes W over **~50 ticks** (measured: 47–51 ticks,
seed-dependent, because the W population's age distribution is stochastic). A birth-block therefore
can only freeze the COUNT-UP (AC94-D3's arms) or land *after* the reset has completed — it cannot land
W=0 inside the 5-tick reset window. No fixed block tick works: the measured W→0 delay varies 17–51
ticks across seeds.

To interrupt the reset itself mid-way, the cut must remove W **directly** (instant), the exact mirror
of the direct W *restoration* AC92 already established as the correct way to intervene at W=0. So
`cut_W` (below) is the cut; `restore_W` (machinery-only, EXTERNAL) is the rescue. Both touch only the
W population (`body.life[:4]`); content, coordinator state, memory, energy, material and fuel are
untouched by construction.

## What was added

- `cut_W(o)` — machinery-only W cut, labeled EXTERNAL (mirror of `restore_W`). Zeroes `body.life[:4]`.
- Two arms: `reset_block` (cut W mid-reset, never restore → the reset must stay frozen and the
  organism dies via the AC13 attention-hijack cascade) and `reset_rescue` (cut mid-reset, restore W at
  `reset_start + RESET_RESCUE_OFFSET` → the reset resumes from maintained state alone).
- The intervention is **state-detected, not host-timed**: the run loop watches the maintained RIP bit
  for the 0→1 transition (reset start), cuts W at `reset_start + RESET_CUT_OFFSET`, and restores at
  `reset_start + RESET_RESCUE_OFFSET`. The cut/restore schedule is an external experimenter input read
  from the organism's own maintained state, never handed back as a "reset phase was in progress" hint.
- Per-individual endpoints: `reset_start`, `reset_progress_at_cut`, `reset_completed_tick`,
  `reset_froze`, `reset_restore_done`.

`RESET_CUT_OFFSET = 2` lands the cut with the counter at 10–11 (3 bits already cleared, part-way).
`RESET_RESCUE_OFFSET = 40` sits inside the safe window (sweep below): rescue before the W=0 window
kills C and drains energy, so the restored machinery can still pay the reset *and* the repair debt
accumulated while W=0.

## Verification (engineering seeds 0–7, damage=True, corrupt=False)

`reset_block` (16/16 individuals): the reset froze mid-way — `reset_progress_at_cut` = 10–11,
`reset_completed_tick = None` (the reset never completed), `timer_resets` stops after the single
pre-cut clear, and the interrupted succession never completes (`successions = 0`). The organism dies
at 2808–2815 with W=0. (The counter *reads* 13 at death, up from the frozen 10, because the sticky-SET
damage stream re-sets the cleared bits while `reg_ctrl` is offline at W=0 — a damage phenomenon, not
reset progress.)

`reset_rescue` (16/16 individuals): the reset froze, then — after the machinery-only restore — resumed
and completed from the maintained RIP bit + counter alone (`reset_completed_tick` ≈ `reset_start` +
43), the organism survived the interruption (`completed = True`), and the succession rate returned to
healthy (`successions = 6`, identical to the uninterrupted gated run; the interrupted cycle's copy
completes after rescue: seed 0 start=2637 → copy_done=2712 → switch=2731 → remove=2768).

`observer-discard` (16/16 individuals): replacing the succession observer with a fresh object at the
rescue tick (`swap_succ_at='rescue'`) leaves the trajectory **byte-identical** (`state_hash`) to the
uninterrupted-resume run. This is the decisive state-sufficiency check: the reset completion is carried
entirely by the maintained RIP bit + counter, with no host-side "reset was in progress" memory.

`test_ac95.py` now has a `TestResetInterruption` class (5 tests: `cut_W` is machinery-only, the reset
writes nothing at W=0, `reset_block` freezes, `reset_rescue` resumes+completes, observer-discard
identical at the rescue tick). Full suite: **15/15 green** (10 D2 + 5 D3), including the byte-identity
comparators (`ungated` == frozen AC92 32/32, `split` == frozen AC94 32/32 — the new arms do not touch
them).

## The rescue-offset sweep (reported so D4 can prespecify a satisfiable gate)

`RESET_RESCUE_OFFSET` ∈ {20, 30, 40}: 16/16 survive AND reset-complete AND 6 successions each.
50 → 14/16; 60 → 10/16; 100 → 1/16. The window closes because a longer W=0 exposure kills C (energy
converter, life 64) and drains energy, so at rescue the restored machinery cannot pay the reset plus
the accumulated program/description/pointer repair debt. A finals gate "every individual survives and
resets" is therefore satisfiable only inside the safe window; D4 should gate survival as a
bimodality-aware lower bound (AC68) and gate the *mechanism* (reset froze, then completed after a
machinery-only restore, observer-discard identical) categorically.

## No new host-side dependency discovered (D1 audit unchanged)

The reset-interruption arms introduce no new class-C leak. The reset completion is driven by the
maintained RIP bit (D2's fix), and the observer-discard equivalence at the rescue tick proves the
trajectory does not depend on `succ._entry`. The intervention-schedule locals in `run()`
(`reset_start`, `reset_progress_at_cut`, `reset_cut_done`, `reset_restore_done`) are external
experimenter inputs read from the organism's own RIP bit for timing and recorded as endpoints; they
are not read by the injected step. `alloc.streak` (the second D1 class-C leak) remains **deferred** as
in D2 — inert in the finals (transition='none'), and its fix would change the byte-identity comparator
digests.

## Files

- `ac95.py` — `cut_W`, the `reset_block`/`reset_rescue` arms, the state-detected interruption in
  `run()`, and the new endpoints.
- `test_ac95.py` — `TestResetInterruption` (5 tests).
- `_ac95_d3_*` — throwaway probes (not part of any freeze).
