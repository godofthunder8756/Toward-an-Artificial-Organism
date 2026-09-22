# AC105 protocol v1: the operating range of the frozen persistent-trigger + allowance-42 architecture

STATUS: **frozen before the first final seed.** Written 2026-09-22. Parent: AC104 (frozen).

AC104 froze one explicit internal spending rule — `budget = max(0, material - DECISION_ALLOWANCE)`
with `DECISION_ALLOWANCE = STREAK_N * 7 = 42`, applied THROUGHOUT LIFE with no challenge-time
knowledge — and showed it is a valid, no-harm coordinator that rescues two diagnostic marginal
seeds (5603, engineering seed 1). Its recorded limit (see `AC104_ERRATA_v1.md`): the fresh sample
(5700-5707) contained no marginal economy, so the rescue did not recur there and the allowance's
generalization to unseen marginal economies is untested.

This protocol freezes the persistent trigger + allowance 42 AS THEY ARE and maps their OPERATING
RANGE. It does NOT add another adaptive mechanism (no learned reserve sizing), and it does NOT
make universal survival or optimal allocation a requirement — it measures, per predeclared
condition and per move, where the same two arms rescue, where they are neutral, and where they
harm. A negative result is a finding, and every failing case is retained.

## The question

Does the frozen budget rule (allowance 42, applied throughout life) hold its AC104 properties —
reconstruction completes, no survival harm, no relinquishment harm, and the diagnostic rescue —
across a PREDECLARED grid of (a) challenge timings, (b) priorities, and (c) repeated-move
conditions, when the corruption and the route change are placed at DIFFERENT PHASES relative to
one another? The budget rule itself never sees the schedule: it remains
`max(0, material - 42)`, a pure function of the current material and the declared constant, with
no `CORRUPT_TICK`, no move tick and no schedule anywhere in the operational code.

SOURCES (declared): ac105.py ac104.py ac103.py ac102.py ac101.py ac100.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC105_PROTOCOL_v1.md

## What is NOT changed (the mechanism is untouched)

The reconstruction (`reg_from_active`) keeps its total prices (1 energy + 1 material per replica),
its machinery requirement (the W-catalyzed `_cap`), and its world (corruption of the first 8
program bits, the Gray streak, erase-on-relinquishment, every world constant). The persistent
trigger is kept (fire until the decoded program matches the description-derived target). The ONLY
change from AC104 is the RUNNER: the corruption tick is a run parameter (was the module constant
`CORRUPT_TICK`), a per-move reconstruction readout (`fw_by_move`) is recorded, and the condition
(corrupt_tick, move schedule) is a run parameter. At the baseline condition `simult` both arms
reproduce AC104 byte-for-byte (`state_hash`), which is the single-change license (G1). No decision
write is made material-independent; no reserve is added; no accepted internal-memory milestone is
reopened.

## The conditions (predeclared)

Each condition is a `(corrupt_tick, move_schedule)` pair; corruption is always present
(`corrupt=True`) and every condition has at least two channel-1 route changes, so every condition
tests corruption AND route change. The PHASE variable is the relationship between the corruption
tick and the move ticks:

| condition      | corrupt_tick | move schedule (channel-1 flips)      | phase |
|----------------|--------------|--------------------------------------|-------|
| `simult`       | 8192         | 8192, 12288                          | corruption coincides with the FIRST move (AC104 baseline) |
| `simult3`      | 8192         | 8192, 12288, 14336                   | corruption coincides with the FIRST move, THREE moves (repeated-move) |
| `corrupt_first`| 8192         | 10240, 14336                         | corruption BEFORE both moves |
| `move_first`   | 8192         | 6144, 12288                          | first move BEFORE corruption, second after |
| `late`         | 12288        | 8192, 12288                          | corruption coincides with the SECOND move (one move already survived) |

`simult` is exactly AC104's schedule (`ac100.SCHEDULE`), so it reproduces the frozen study.

## Arms (unchanged from AC104)

| arm                | trigger   | per-tick spend                            |
|--------------------|-----------|-------------------------------------------|
| `persistent`       | persistent| None (immediate) — == AC104 `persistent`  |
| `persistent_budget`| persistent| `max(0, material - DECISION_ALLOWANCE)`   |

The candidate differs ONLY by the per-tick budget computation; both are applied throughout life.
The budget is non-binding whenever `material > DECISION_ALLOWANCE + _cap` (the ordinary healthy
regime), so the candidate is byte-identical to the control there; it diverges only where material
is scarce enough that reserving the allowance changes the reconstruction's spend.

## The declared priorities

Priority is a deterministic function of the seed (`ac4.acquire`: `rng.permutation(4)` seeded by
`[seed, 1004]`), so the seed families below realize these declared priorities — a covariate, not
an outcome, and declared pre-freeze:

| family | seeds | priorities realized |
|--------|-------|---------------------|
| finals (untouched) | 5800-5807 | 5800 `(0,2,1,3)`, 5801 `(1,2,3,0)`, 5802 `(0,2,1,3)`, 5803 `(1,2,0,3)`, 5804 `(0,3,2,1)`, 5805 `(2,3,1,0)`, 5806 `(1,2,3,0)`, 5807 `(0,2,3,1)` |
| engineering (disclosed) | 0-7 | 0 `(3,2,1,0)`, 1 `(0,1,3,2)`, 2 `(2,1,3,0)`, 3 `(1,3,2,0)`, 4 `(3,0,2,1)`, 5 `(1,0,2,3)`, 6 `(0,1,2,3)`, 7 `(3,0,2,1)` |
| diagnostic (disclosed) | 5603, 5607 | 5603 `(1,2,3,0)` (AC104 marginal), 5607 `(2,3,1,0)` (AC103 starvation) |

The finals include the AC104 marginal priority `(1,2,3,0)` on 5801 and 5806; the engineering
screen includes the other marginal priority `(0,1,3,2)` (seed 1) and the AC83/AC89 adversarial
renewal-last priority `(3,0,2,1)` (seeds 4, 7). No final outcome is observed before the freeze.

## Endpoints (reported SEPARATELY per move, never folded into an aggregate)

For every individual and every condition, per move (`mts` move boundaries):

- **reconstruction** — `fw_at_corrupt`, `recovery_tick`, `fw_by_move` (flipped-still-wrong among
  the first 8 bits at each move boundary), `flipped_still_wrong` at the horizon;
- **survival** — `completed` / `first_dead`, located relative to the move windows;
- **active relinquishment** — `relinquishments_by_move` (drops with the register bit set);
- **re-acquisition** — `reacquisitions_by_move` (None→bound transitions per move window);
- **continued component production** — `births_by_window` (W/C/B births per move window).

## Screening disclosed (engineering, before this protocol was frozen)

Engineering ran on seeds 0-7 plus the AC104 diagnostic seeds 5603 (marginal) and 5607
(starvation), both histories, all five conditions (200 rows, 16,384 ticks). Findings:

- **Baseline identity holds.** At `simult`, `persistent` and `persistent_budget` reproduce AC104
  byte-for-byte on every sampled seed (verified on 5700/5702/0/1; G1's full check runs on the
  finals).
- **The rescue generalizes to new operating points.** `persistent_budget` survives where
  `persistent` dies at five new (seed, condition) points beyond AC104's two: seed 1 under
  `simult` and `simult3` (marginal economy, mat 65); seed 6 under `simult3` (mat 72, the control
  dies at 14560 after the THIRD move, having relinquished only the second); seed 7 under `late`
  (adversarial priority `(3,0,2,1)`, mat 70, control dies at 12504 at the second/corruption move);
  and 5603 under `simult`/`simult3` (the AC104 marginal, confirmed).
- **No survival harm and no relinquishment harm anywhere.** Across all 200 rows there is no
  individual where the control survives and the candidate dies, and none where the control
  survives and the candidate relinquishes LESS than the control.
- **The budget improves relinquishment completeness at several points.** On seeds 0 and 4 under
  `late`, seed 6 under `simult`, and seed 7 under `simult`/`simult3`, both arms survive but the
  control relinquishes only one move while the candidate relinquishes both/all moves
  (e.g. seed 7 `simult3`: control `[0,1,1]` vs candidate `[1,1,1]`).
- **One reconstruction-level harm, retained as a finding.** Under `late`, 5603 (marginal
  priority, mat 65 control / 67 candidate) dies under BOTH arms (control 12512, candidate 12506),
  but the candidate fails to complete reconstruction (`fw_end == 2`, `recovery_tick is None`)
  where the control recovers (`fw_end == 0`): reserving 42 material starves the reconstruction in
  an economy already doomed by the late corruption. This is a real, retained harm — it is a
  RECOVERY-level harm (fw), not a survival reversal (both die). It tells us the allowance is not
  free: on a marginal economy under late corruption it trades reconstruction completeness for the
  decision reserve and loses both.

The gates below are shaped by this screen on disjoint seeds; the final seeds are NOT screened
(see Anti-drift).

## Gates (prespecified, categorical per distinct seed; both histories must satisfy each)

- **G1 (control identity — the single-change license).** Every final individual, at `simult`:
  `persistent` is byte-identical (`state_hash`) to AC104 `persistent`, and `persistent_budget` to
  AC104 `persistent_budget`.
- **G2 (the candidate completes reconstruction — across the range).** Every final individual, at
  every condition: the candidate applies the corruption (`fw_at_corrupt == 8`) and recovers
  (`flipped_still_wrong == 0`).
- **G3 (no-harm survival).** No final individual, at any condition, where the control survives
  and the candidate dies.
- **G4 (no-harm decision).** No final individual, at any condition, where the control survives
  and the candidate relinquishes LESS than the control (the budget must not starve the decision).
- **G5 (state sufficiency — observer-discard on the CANDIDATE).** Per-tick observer-discard on
  `persistent_budget` at `simult` is byte-identical at every tick (non-vacuous: `swap_applied`,
  `streak_at_swap == 2`). Run on the candidate directly (AC103 errata's correction).
- **G6 (completeness + determinism).** Row count == 8 seeds × 2 histories × 2 arms × 5
  conditions (160); a sampled exact rerun of the first row is byte-identical (`state_hash`).

## Reported, not gated

- **The rescue** (candidate survives where the control dies) and **the reconstruction-level
  harm** (candidate `fw > 0` where the control recovers), per seed per condition — the load-bearing
  positive and negative signatures. G3/G4 gate the no-harm directions; rescue and reconstruction
  harm are reported as per-seed per-condition findings, not gated to any universal claim.
- **The relinquishment-completeness improvement** (candidate relinquishes ≥ control, strictly
  more on some seeds).
- **The per-move endpoint tables** (reconstruction, survival, relinquishment, re-acquisition,
  component production) for every individual and condition.
- The material level at the corruption tick and each seed's priority — measured covariates.
- Survival is a bimodality-aware lower bound (AC68). No autopoiesis claim; `advance()` and
  `prog.choose` remain supplied format-level machinery.

## Anti-drift rules

- The runner creates `ac105_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed
  set (which includes this protocol file).
- `test_ac105.py`, `audit_ac105.py`, `replay_ac105.py` are NOT hashed into the frozen snapshot
  (AC17's rule).
- Engineering seeds (0-7) and the diagnostic seeds (5603, 5607) are excluded from the final
  sample. The final seeds 5800-5807 are a fresh range, disjoint from every prior family (0-7,
  4412-4439, 4440-4443, 4444-4447, 4448-4451, 4466/4481/4504/4510, 4600-4871, 4872-5099,
  5100-5507, 5600-5607, 5700-5707) and are NOT screened — no final outcome is observed before the
  freeze; `mat_at_corrupt` and priority are measured, not selected on.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh
  seeds.
- The frozen AC104 results and every earlier freeze are untouched.

## Source hashes (computed before the first final seed)

    (recorded in ac105_results_v1/pre_run_snapshot.json at freeze time)
