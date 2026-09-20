# AC101 protocol v1: composition test — internal memory + controller reconstruction + machinery turnover + adaptation in the same organism (gray_ctl + the corruption challenge)

STATUS: **frozen before the first final seed.** Written 2026-09-20. AC100 (frozen) consolidated
AC99's success as the **Gray encoding, not the reserve**: on the unseen cohort both `gray_ctl`
(Gray, no reserve) and `bin_res` (binary + reserve) satisfy the full per-move adaptation criterion
(relinquish + re-acquire after every move + continued W/C/B production + survive) on 4/4 distinct
seeds, and `gray_ctl` is adopted as the next baseline. One thing AC100 deliberately did NOT do:
every condition ran with `corrupt=False`, and the "reconstruction challenge" was carried forward as
the state-sufficiency observer-discard gate. Those are different tests — discarding observational
history does not DAMAGE the controller, so the reconstruction machinery (`reg_from_active`,
re-instantiating the 126-bit program from the maintained 130-bit description) was never exercised
against an actually-corrupted controller in the AC100 world.

This protocol freezes the **composition test**: whether the four demonstrated capabilities —
(1) **internal memory** (the acquired routes in `mem.Memory`), (2) **controller reconstruction**
(the paid, W-catalyzed re-instantiation of the program from the description after corruption),
(3) **machinery turnover** (W/C/B constituent production + the recipe-succession replacement of the
description-bearing storage), and (4) **adaptation** (the Gray relinquishment streak +
erase-on-relinquishment re-acquisition) — work together in the SAME tested organism, under the
**combined challenge** of a controller corruption AND two successive route reversals.

SOURCES (declared): ac101.py ac100.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC101_PROTOCOL_v1.md

## The claim and the composition question

AC100 established each capability separately in the gray_ctl architecture, but the internal-state
milestone (reconstruction + description maintenance + succession, AC86-89/92) and the adaptation
milestone (Gray relinquishment, AC99/AC100) were never exercised **together with the controller
actually corrupted**. The claim under test:

**The gray_ctl organism composes all four capabilities in one body under the combined challenge:
it reconstructs its corrupted controller, maintains its description, turns over its machinery, and
adapts (re-acquires) to both route reversals, while surviving — on the unseen cohort. The
engineering screen shows the composition is NOT unconditional: the reconstruction's material cost
and the move's income cut interact to hijack the program (observation bit 1) and starve the paid
internalized streak, which on one seed is fatal and on two others degrades the first-move adaptation
from active relinquishment to passive expiry.**

The four capabilities are mapped to endpoints as follows, all measured in the SAME individual:

- **Internal memory** → `routes` (both routes bound at the horizon) and the per-move re-acquisition
  (`reacquisitions_by_move`).
- **Controller reconstruction** → `fw_at_corrupt == 8` (the corruption was actually applied) and
  `flipped_still_wrong == 0` (the corrupted rule-0 bits were re-instantiated to correct).
- **Machinery turnover** → `successions >= 1` (recipe-bearing storage replaced) and W/C/B births > 0
  in every post-move window; description `130/130` (the description is maintained).
- **Adaptation** → `reacquisitions_by_move` (≥1 None→bound transition of key 1 in every post-move
  window); the active-vs-passive split (`relinquishments_by_move`) is reported, not gated.

## World, arm, seeds

World constants unchanged from AC100/AC99/AC98/AC97/AC96: PORTS=4, YIELD_M=64, YIELD_F=64,
TICKS=16384, sticky 1e-4 damage on both banks (independent streams), STREAK_N=6,
STREAK_THRESHOLD=4, REGISTER_THRESHOLD=4, the order-preserving generic-over-syntax decoder,
AC75's erase-on-relinquishment, the internalized Gray streak (ac96/ac99-d2). **No reserve**
(gray_ctl is the adopted baseline; AC100 showed the reserve is unnecessary for Gray on the tested
cohorts, and this cycle does not optimize reserve size). The architecture is `ac95.ARM_PARTS['gated']`
(repair + regen + succession + ctrl_maintain + gate_ctrl + atomic_switch + timer_maintained).

The **combined challenge** (the only change from AC100): `corrupt=True` alongside the two route
reversals. The controller corruption is the AC80/85/87/89/92 challenge: at `CORRUPT_TICK == 8192`
the first 8 bits of rule 0 (`(1,1,0)`, the fuel-contact rule) are flipped (4 of 7 replicas set to
the wrong value), and the organism must re-instantiate the program through its paid, W-catalyzed
`reg_from_active`. `CORRUPT_TICK == MOVE_TICK == 8192`, so the corruption and the first move land on
the SAME tick (the AC89 simultaneous schedule); the second move is at `t=12288` (flip back), giving
two successive disruptions each followed by a 4096-tick re-acquisition window. At `corrupt=False`
this runner reproduces AC100's `gray_ctl` **byte-for-byte** (state_hash) at the same schedule — that
equivalence (the G4 arm identity) licenses attributing any difference to the corruption alone
(AC89's rule).

One arm per individual: `gray_ctl` (Gray streak, no reserve) with `corrupt=True`. No factorial, no
reserve arm (the task does not spend this cycle on the reserve).

Two seed strata, predeclared:

- **UNSEEN** `4448, 4449, 4450, 4451` (4 seeds): fresh, priorities reported not prespecified.
- **ADVERSARIAL** `4466, 4481, 4504, 4510` (4 seeds): fresh seeds whose acquired priority is AC83's
  adversarial `[3,0,2,1]` (the bank-1 renewal rule ranked last), predeclared SEPARATELY from the
  unseen stratum.

8 seeds × 2 histories = 16 individuals; history is a trivial repeated measure (the runner gates
`activation=[True,True]` and the RNG seeds depend on seed, not history), so the criterion is stated
per distinct seed with history identity verified. Both strata are disjoint from engineering 0-7,
from every prior final family ≤ 4447 (… AC100 4444-4447), from the D1/D2/D3/screening seeds
4412-4439, and from the 4600-4871 order-line and 5100-5507 confirmatory families. **No screening of
either final stratum** — the gates were shaped by the engineering screen on the disjoint seeds 0-7
(disclosed below).

## Screening disclosed (before this protocol was frozen)

The engineering screen ran `gray_ctl + corrupt=True` on seeds **0-7** (both histories) under the
two-move schedule, recorded in `ac101_engineering_v1/` (no freeze). Measured there:

- **The internal-state composition is unconditional.** Every individual (8/8): corruption applied
  (`fw_at_corrupt == 8`) and recovered (`flipped_still_wrong == 0`); description intact (130/130,
  or 130/130 at death for the one non-survivor); ≥1 succession cycle (3-6); per-tick observer-discard
  byte-identical (state sufficiency).
- **The behavioural composition is NOT unconditional.** 7/8 survive and re-acquire at every move.
  On seed **1** (priority `[0,1,3,2]`) the organism dies at **8408** with production stopping
  entirely in the first post-move window (`births_by_window[1]` = 0/0/0) and the route never
  re-acquired. On seeds **6, 7** (priorities `[0,1,2,3]`, `[3,0,2,1]`) the first-move adaptation is
  **passive** (`relinquishments_by_move == [0,1]`): the stale entry expires naturally (~t≈8274)
  rather than being actively relinquished, while the second move is actively relinquished.
- **The seed-1 mechanism (the composition interaction).** The corruption forces the bank-0 repair
  (action 2) which spends ~32 material over t=8192-8193, dropping material below 64 and setting
  observation bit 1 (material ≤ 64); the program then answers with action 1 (material contact) on
  the now-stale route 1, which is unproductive. The internalized streak increments are **paid**, so
  with material ~0 the increment stalls at 4 (< STREAK_N=6); the drop never fires, the stale entry
  is never erased, W/C birth is preempted (obs bit 1 fires ahead of the birth rules), and the
  organism dies of the W/C collapse at 8408 (energy 0, fuel still 18) with the description INTACT at
  death (130/130) and the reconstruction complete (fw=0). This is the AC96 economic finding (the
  paid decision-state write is starved by the income collapse the decision exists to pre-empt)
  re-entering through the reconstruction's material cost.

Consequences, all reflected in the gate shapes below: G1 gates the unconditional internal-state
composition (reconstruction + description + recipe turnover) per individual; G2 gates the behavioural
composition (adaptation + production + survival) per individual, which the engineering screen says
is 7/8 and which may fail on the finals (a recorded failure would be the finding, not a licence to
amend); G6 applies both to the adversarial stratum.

## Gates (prespecified, categorical per distinct seed)

- **G1 (internal-state composition — reconstruction + description + recipe turnover).** For every
  distinct final seed, the `gray_ctl` arm satisfies: (a) the corruption was applied
  (`fw_at_corrupt == 8`); (b) it was recovered (`flipped_still_wrong == 0`); (c) the description is
  intact — `description_correct == 130` for a survivor, `description_correct_at_death == 130` for a
  non-survivor; (d) machinery turnover: `successions >= 1`. Both histories must satisfy it.
- **G2 (behavioural composition — adaptation + production + survival).** For every distinct final
  seed, the `gray_ctl` arm satisfies: (a) re-acquisition — ≥1 None→bound transition of key 1 in
  every post-move window; (b) continued production — W, C and B births all > 0 in every post-move
  window; (c) survival — `completed`.
- **G3 (state sufficiency — observer-discard on gray_ctl).** Every final individual: the gray_ctl
  run with the succession observer AND the alloc (clearing the vestigial host streak dict) discarded
  at a mid-streak tick is **byte-identical at every tick** (`per_tick_identical`, trajectory-level),
  non-vacuously (`status != 'no_mid_streak'`, `swap_applied`, `streak_at_swap == 2`). The Gray streak
  must be recovered from maintained state alone, now under the combined challenge.
- **G4 (corrupt-is-the-only-change — arm identity).** Every final individual: gray_ctl with
  `corrupt=False` reproduces AC100's `gray_ctl` byte-for-byte (state_hash) at the same two-move
  schedule — proving the corruption parameter is the ONLY change vs the adopted baseline (AC89's
  single-change equivalence rule).
- **G5 (completeness + determinism).** Row count == 8 seeds × 2 histories × 1 arm (16); a sampled
  exact rerun of the first row is byte-identical (state_hash).
- **G6 (adversarial-priority stratum).** Every adversarial seed (`[3,0,2,1]`): the G1 AND G2
  criteria hold (reconstruction + description + recipe turnover + adaptation + production +
  survival).

A gate failure is recorded, not moved (AC16/17). G2 is prespecified as a real behavioural gate; if
the seed-1 interaction transfers to the finals it will FAIL, and that failure is the finding (the
composition is not unconditional), not a licence to amend the gate.

## Reported, not gated

- **Active vs passive relinquishment.** `relinquishments_by_move` per seed (the Gray arm actively
  drops vs the stale entry expiring naturally) — reported, since the AC100 discriminator was active
  drops, but under corruption the first-move adaptation can degrade to passive expiry while still
  re-acquiring and surviving.
- **The seed-1 interaction mechanism** (reconstruction material cost → obs bit 1 → paid-streak
  starvation → W/C collapse), reported with its named cascade.
- **The unseen stratum's priorities** — reported, not prespecified (unseen seeds).
- **Survival is a bimodality-aware lower bound** (AC68).
- **Supplied machinery remains** — `advance()` and `prog.choose` are still host-supplied
  format-level machinery; no autopoiesis claim.

## Anti-drift rules

- The runner creates `ac101_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed
  set (which includes this protocol file).
- `test_ac101.py`, `audit_ac101.py`, `replay_ac101.py` are NOT hashed into the frozen snapshot
  (AC17's rule).
- Engineering seeds (0-7) are excluded from the final sample and are disjoint from both final strata.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.
- The frozen AC100 results and every earlier freeze are untouched.

## Source hashes (computed before the first final seed)

    (recorded in ac101_results_v1/pre_run_snapshot.json at freeze time)
