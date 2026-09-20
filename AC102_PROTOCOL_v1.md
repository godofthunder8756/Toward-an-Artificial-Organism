# AC102 protocol v1: does the TIMING of necessary maintenance cause the composition failure? (matched runs + budget trace + a staged repair schedule)

STATUS: **frozen before the first final seed.** Written 2026-09-20. Parent: AC101 (frozen).
AC101 froze the composition test — internal memory + controller reconstruction + machinery
turnover + adaptation in the SAME organism under the combined challenge of a controller
corruption (t=8192) and two route reversals (t=8192, t=12288) — and recorded a split: the
internal-state composition (reconstruction `fw` 8→0, description intact, recipe turnover) is
UNCONDITIONAL (8/8), while the behavioural composition (adaptation + production + survival) fails
on the unseen seed 4450 (dies 8408) and the engineering seed 1 (dies 8408). AC101 left a
HYPOTHESIS for that failure, not an established mechanism: the reconstruction's material spend
(~32 over t=8192-8193) drops material below 64, sets observation bit 1 (material ≤ 64), the
program answers with a material contact on the now-stale route 1, the paid internalized Gray
streak stalls below its drop threshold, the stale entry is never erased, and the organism dies of
the W/C collapse. AC101's boundary named two candidate fixes — "a decision write that is not
material-denominated, or a reconstruction staged not to drop material below the obs-bit-1
threshold" — and flagged that confirming the cascade needs a direct causal test.

This protocol freezes that direct test. **The question: whether the TIMING of necessary
maintenance (rather than its existence or price) causes the composition failure** — i.e. whether
the shared resource demands can be coordinated sufficiently to preserve the whole organism. Two
experiments, both in the adopted `gray_ctl` architecture (Gray streak, no reserve), 16,384 ticks.

SOURCES (declared): ac102.py ac101.py ac100.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC102_PROTOCOL_v1.md

## What is NOT changed (the resource model is untouched)

The reconstruction (`reg_from_active`) keeps its total prices (1 energy + 1 material per replica),
its machinery requirement (the W-catalyzed `_cap = min(32, 8·available_W, energy, material)` still
applies), and its trigger (`reg_trigger = obs2 or (repair and (desc/pointer minority ≥ trigger))`).
The corruption challenge, the two-move schedule, the Gray streak, the erase-on-relinquishment, the
observer-discard, and every world constant are byte-for-byte the AC101 world. No decision write is
made material-independent; no reserve is added; no write cost changes; no accepted internal-memory
milestone is reopened. The ONLY new degree of freedom is a per-tick write budget on the
reconstruction, mirroring the succession's existing `SUCC_BUDGET`.

## The two experiments

### Experiment 1 — the interaction (2x2 matched runs)

Four arms per individual, {corrupt, no-corrupt} × {move, no-move}:

| arm          | corrupt | schedule            | equals                |
|--------------|---------|---------------------|-----------------------|
| `neither`    | False   | no moves            | the bare organism     |
| `move_only`  | False   | two moves           | AC100 `gray_ctl`      |
| `corrupt_only`| True   | no moves            | corruption alone      |
| `both`       | True    | two moves           | AC101 `gray_ctl`      |

Recorded per individual: survival, reconstruction recovery (`fw` at corruption → end), the
recovery tick, active relinquishment, re-acquisition, post-challenge production, and the material
level at the corruption tick. The interaction claim: **the death (if any) requires BOTH
challenges** — neither alone may kill.

### Experiment 2 — the repair schedule (one internally controlled schedule)

Three arms on the `both` condition (corrupt=True, two moves), differing ONLY in the per-tick
reconstruction write budget:

| arm     | regen_budget | meaning                                             |
|---------|--------------|-----------------------------------------------------|
| `both`  | None         | immediate (unchanged): writes up to `_cap` (~24/tick at W=3) |
| `staged`| REPAIR_BUDGET = 8 | bound to 8 replica-writes/tick (the test)      |
| `never` | 0            | no reconstruction write ever (must FAIL)             |

`REPAIR_BUDGET = 8` is 1/3 of the W=3 `_cap` (24), so the 32-site reconstruction is spread over
≥ 4 ticks instead of 2. The budget is a property of the reconstruction primitive (uniform from
t=0, exactly like `SUCC_BUDGET`), applied by asserted source surgery on `ac95.reg_from_active` /
`ac95.maintain`; at budget=None the surgery reproduces `ac95.maintain` byte-for-byte (verified by
the `staged_nobudget_identity` check). The `never` arm (budget=0) disables ALL reconstruction
including ambient-damage repair from t=0 — it is the "schedule that delays repair indefinitely",
which must FAIL; note this makes its pre-corruption trajectory diverge from `both` (the ambient
repair is also disabled), which is expected, not a clean single-change.

The schedule test has two required properties, per the task: (a) eventual controller recovery AND
adaptation — a schedule that delays repair indefinitely must FAIL (the fix must not be "never
repair"); (b) if a staged schedule that still recovers + adapts exists, the timing hypothesis is
vindicated (staging rescues the composition); if no such schedule exists, the timing hypothesis is
falsified and the failure is caused by the PRICE on a marginal economy.

## The timing hypothesis under test

H_timing: the reconstruction's single-tick spend (dropping material below 64) is what trips the
obs-bit-1 hijack, so a staged spend (which keeps material above 64 per tick) rescues the organism.

The direct test: on the death-prone seeds, does `staged` survive where `both` dies? The engineering
screen (below) already shows NO — `both` and `staged` die at the SAME tick (8408) — and the budget
sweep shows staging is HARMFUL to the immediate-survivors (it stalls the reconstruction via the
program's cementing majority repair). Both directions falsify H_timing.

## Screening disclosed (before this protocol was frozen)

Engineering ran on seeds 0-7 (disjoint from both final strata) plus a disclosed scan of the fresh
range 4872-5099 (disjoint from every prior family: 0-7, 4412-4439, 4440-4443, 4444-4447, 4448-4451,
4466/4481/4504/4510, 4600-4871, 5100-5507). Measured there:

- **The interaction (2x2).** On every engineering seed the three single-challenge arms
  (`neither`, `move_only`, `corrupt_only`) survive; the composition (`both`) kills seed 1 (dies
  8408, streak stalls at 4) and no other engineering seed. The death requires BOTH challenges.
- **The budget trace.** The reconstruction (`reg_from_active`) spends ~24-25 material in ONE tick
  at t=8192 (material ~66 → ~41), dropping material below 64 and setting obs bit 1; the program
  then does a material contact (action 1) on the stale route 1 (unproductive), and the paid Gray
  streak increment (7 material/tick) starves. The failing seed's material at the corruption tick
  (66) is the lowest of the cohort; the survivors' is 72-122. The program's OWN majority repair
  (action 2) does NOT fire in the immediate arm (obs bit 1 outranks obs bit 2), and where it does
  fire (high material, staged) it CEMENTS the 4/7 majority flip — majority restore writes the 3
  correct replicas to the wrong value.
- **The staged sweep (budgets 16/8/4/2/1/0).** Budgets 16/8 leave the failing seed's death
  UNCHANGED (8408) and turn the immediate-survivors into deaths (reconstruction stalls via the
  cementing path); budgets 2/1 kill every seed with the reconstruction incomplete; budget 0 kills
  every seed with `fw`=8 (no reconstruction at all).
- **The death is material-level-dependent.** The 24 deaths in the 4872-5099 scan are confined to
  seeds with material ≤ 74 at the corruption tick. The final UNSEEN stratum is therefore selected
  (disclosed, pre-freeze) to span that regime — two death-prone seeds (4934, 5002) and two
  survival seeds (4880, 4950) — so the interaction and the timing hypothesis are testable on fresh
  finals. The ADVERSARIAL stratum is 4 fresh `[3,0,2,1]` seeds (4883, 4901, 4928, 5038), all of
  which survive `both` in the scan (the adversarial priority is not the breaking point).

The gates below are shaped by this engineering screen on the disjoint seeds; the final strata are
not re-screened (the selection is the disclosed stratification above, fixed before any final run).

## Gates (prespecified, categorical per distinct seed)

Both histories must satisfy each gate.

- **G1 (interaction — the death requires both challenges).** Every distinct seed: `neither`,
  `move_only`, and `corrupt_only` all survive (`completed`). The composition death, if any, is
  thereby confined to `both`.
- **G2 (reconstruction recovers under `both`).** Every distinct seed's `both` individual:
  `fw_at_corrupt == 8` (the corruption was applied) and `flipped_still_wrong == 0` (recovered).
  This is AC101's unconditional internal-state composition, restated.
- **G3 (timing hypothesis — staging rescues the composition failure).** Every distinct seed that
  dies under `both` survives under `staged`. **Expected to FAIL**: the engineering screen shows the
  death seeds die under BOTH arms at the SAME tick (8408). The failure records that the lump-spend
  timing is NOT the cause of the composition failure (H_timing falsified). Non-vacuous by
  construction: the disclosed death-prone seeds 4934/5002 supply the `both`-deaths.
- **G4 (the staged schedule preserves recovery).** Every distinct seed's `staged` individual:
  `flipped_still_wrong == 0` (eventual controller recovery). **Expected to FAIL**: the engineering
  screen shows the staged reconstruction stalls (fw nonzero) via the cementing path on some
  immediate-survivors. The failure records that the reconstruction's immediate schedule is
  load-bearing — staging is not a viable schedule.
- **G5 (never-repair must fail).** Every distinct seed's `never` individual:
  `flipped_still_wrong > 0` (no recovery) AND not `completed` (death). The fix must not be "never
  repair".
- **G6 (state sufficiency — observer-discard on `both`).** Every final individual: the `both` run
  with the succession observer AND the alloc discarded at a mid-streak tick is byte-identical at
  every tick (trajectory-level; non-vacuous: `swap_applied`, `streak_at_swap == 2`). Carried from
  AC101's G3, now on the `both` arm.
- **G7 (adversarial-priority stratum).** Every adversarial seed (`[3,0,2,1]`): the G1 single-challenge
  arms survive AND the G2 reconstruction criterion holds under `both` (the adversarial priority is
  not the breaking point under the interaction).
- **G8 (completeness + determinism + arm identity).** Row count == 8 seeds × 2 histories × 6 arms
  (96); a sampled exact rerun of the first row is byte-identical (`state_hash`); `move_only` ==
  AC100 `gray_ctl` (state_hash); `both` == AC101 `gray_ctl` (state_hash); and the budgeted maintain
  at budget=None == the frozen maintain (state_hash) — the regen_budget is the ONLY change in the
  `staged`/`never` arms (AC89's single-change rule).

G3 and G4 are the falsification gates: G3 records that staging does NOT rescue the composition
failure (the timing hypothesis is false); G4 records that staging actively breaks recovery (the
reconstruction must be immediate). Both are recorded, not moved (AC16/17). A gate failure is a
finding, not a licence to amend.

## Reported, not gated

- **The budget trace** (which writes consume material, when the streak becomes unaffordable, when
  W fails) — recorded per row in `budget_trace` (t = 8188..8223) for the audit, summarized in the
  results. Distinguishes the reconstruction (`reg_from_active`, curative) from the program's
  majority repair (action 2, cementing for a 4/7 majority flip).
- **The second-move death mode** (deaths at ~12,500 with the streak stuck at 5) seen in the scan —
  a distinct failure mode from the first-move 8408 death, not a gate.
- **Active vs passive relinquishment** per seed per move.
- **The unseen stratum's priorities** — reported, not prespecified.
- **The material level at the corruption tick** per seed — the economic covariate that sorts
  death-prone from survival seeds, reported not gated.
- **Survival is a bimodality-aware lower bound** (AC68).
- **Supplied machinery remains** — `advance()` and `prog.choose` are still host-supplied
  format-level machinery; no autopoiesis claim.

## Anti-drift rules

- The runner creates `ac102_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed
  set (which includes this protocol file).
- `test_ac102.py`, `audit_ac102.py`, `replay_ac102.py` are NOT hashed into the frozen snapshot
  (AC17's rule).
- Engineering seeds (0-7) and the scan range are excluded from the final sample and disjoint from
  both final strata.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.
- The frozen AC101 results and every earlier freeze are untouched.

## Source hashes (computed before the first final seed)

    (recorded in ac102_results_v1/pre_run_snapshot.json at freeze time)
