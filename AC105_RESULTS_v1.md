# AC105 results v1: the frozen allowance-42 budget holds across the operating range — it rescues a new marginal priority (5804), never harms, and improves relinquishment completeness under late corruption; one move-first boundary (5802) kills both arms

Parent: AC104. Frozen per `AC105_PROTOCOL_v1.md` (hashed before the first final seed). Runner
`ac105.py` (a faithful copy of `ac104.py`'s `_run_core`; the ONLY changes are the corruption tick
as a run parameter, a per-move reconstruction readout `fw_by_move`, and the condition
(corrupt_tick, move schedule) as a run parameter). Seeds **5800-5807** (fresh, untouched, disjoint
from every prior family), 2 histories, 2 arms, **5 conditions**, **160 rows**, 16,384 ticks.
`DECISION_ALLOWANCE = STREAK_N * 7 = 42`, unchanged.

**Headline:** The frozen budget rule (allowance 42, applied throughout life with no challenge-time
knowledge) holds its AC104 properties across the operating range, and it rescues a *new* marginal
priority `(0,3,2,1)` (5804, material 71) on the untouched finals. It never harms (no survival
reversal, no relinquishment harm), and under late corruption (coincident with the second move) it
improves relinquishment completeness on three seeds where the control leaves the second move
un-relinquished. The one operating-range boundary — 5802 under `move_first`, where BOTH arms die
with reconstruction complete — is not budget-specific.

## Verdict

**All six gates pass.** The question — does the frozen budget rule hold its AC104 properties across
a predeclared grid of challenge timings, priorities and repeated-move conditions — is answered:

- **The rule is a valid, no-harm coordinator everywhere (G1-G6 all pass).** At the baseline
  condition `simult` both arms are byte-identical to AC104 (G1); the candidate completes
  reconstruction on every final individual at every condition (G2); and there is no individual,
  at any condition, where the candidate dies where the control survives (G3) or relinquishes less
  (G4). State sufficiency is unaffected (G5, per-tick observer-discard byte-identical 16/16).

- **The rescue transfers to the untouched finals, on a NEW priority (reported, not gated).** Seed
  5804 (priority `(0,3,2,1)`, material 71 at the corruption tick) dies under the control
  (8408, streak stalls, no relinquishment) and survives under the budget (relinquishes 2/2, and
  3/3 under `simult3`), in both histories and both simultaneous schedules. This is a marginal
  economy with a priority distinct from AC104's two diagnostics (`(1,2,3,0)` and `(0,1,3,2)`), so
  the rescue is not a re-run of the diagnostic seeds — it is a fresh instance of the mechanism.

- **The operating range has one non-budget-specific boundary.** Under `move_first` (first move at
  6144, before the corruption), seed 5802 dies under BOTH arms (12539 control, 12540 candidate)
  with reconstruction complete (`fw == 0`) and the second move never re-acquired
  (`reacquisitions_by_move [1,0]`). The budget neither rescues nor harms it — the failure is in the
  architecture's re-acquisition path, not in the spending rule.

- **A diagnostic reconstruction-level harm is retained as a finding.** Under `late` (corruption at
  the second move), the AC104 marginal seed 5603 dies under both arms, but the candidate fails to
  complete reconstruction (`fw == 2`, `recovery_tick is None`) where the control recovered
  (`fw == 0`): reserving 42 material starves the reconstruction in an economy already doomed. This
  did NOT recur on the finals (0 reconstruction-harm on 5800-5807); it is disclosed engineering, and
  it tells us the allowance is not free — on a marginal economy under late corruption it trades
  reconstruction completeness for a decision reserve it cannot use.

## Per-seed outcome (both histories identical unless noted)

`S` = survives; `D< tick>` = dies at `< tick>`; `rN` = relinquishment count; `[x,y]` =
`relinquishments_by_move`. Every individual applies the corruption (`fw_at_corrupt == 8`) and
recovers (`flipped_still_wrong == 0`). The table shows the arms side by side per condition.

| seed | priority    | condition      | persistent (control)   | persistent_budget (candidate) |
|------|-------------|----------------|------------------------|-------------------------------|
| 5800 | `(0,2,1,3)` | simult/simult3 | S r2 `[1,1]` / S r3 `[1,1,1]` | S r2 `[1,1]` / S r3 `[1,1,1]` |
| 5800 |             | corrupt_first  | S r2 `[1,1]`           | S r2 `[1,1]` |
| 5800 |             | move_first     | S r2 `[1,1]`           | S r2 `[1,1]` |
| 5800 |             | late           | S r1 `[1,0]`           | **S r2 `[1,1]`** |
| 5801 | `(1,2,3,0)` | all            | S (r2/r3/r2/r2/r2)     | S (identical) |
| 5802 | `(0,2,1,3)` | move_first     | **D12539 r2 `[1,1]`, reacq `[1,0]`** | **D12540 r2 `[1,1]`, reacq `[1,0]`** |
| 5802 |             | other 4 conds  | S                     | S (identical) |
| 5803 | `(1,2,0,3)` | all            | S (r2/r3/r2/r2/r2)     | S (identical; `late` recovery 12289 vs 12300) |
| 5804 | `(0,3,2,1)` | simult         | **D8408 r0**           | **S r2 `[1,1]`** |
| 5804 |             | simult3        | **D8408 r0**           | **S r3 `[1,1,1]`** |
| 5804 |             | corrupt_first  | S r2 `[1,1]`           | S r2 `[1,1]` |
| 5804 |             | move_first     | S r2 `[1,1]`           | S r2 `[1,1]` |
| 5804 |             | late           | S r2 `[1,1]`           | S r2 `[1,1]` |
| 5805 | `(2,3,1,0)` | late           | S r1 `[1,0]`           | **S r2 `[1,1]`** |
| 5805 |             | other 4 conds  | S                     | S (identical) |
| 5806 | `(1,2,3,0)` | late           | S r1 `[1,0]`           | **S r2 `[1,1]`** |
| 5806 |             | other 4 conds  | S                     | S (identical) |
| 5807 | `(0,2,3,1)` | all            | S (r2/r3/r2/r2/r2)     | S (identical) |

Counts on the final sample: **rescue 4/160** individuals (5804 under `simult` + `simult3`, both
histories), **both-die 2/160** (5802 under `move_first`), **relinquishment-completeness
improvement 6/160** (5800/5805/5806 under `late`, both histories), **reconstruction-harm 0/160**.

## The mechanism, measured

1. **The budget is a global spending policy, not a challenge-timed defer.** In the `late`
   condition the arms diverge *before* the corruption tick (5800: `mat_at_corrupt` 70 for both;
   elsewhere the candidate ends the pre-corruption phase with more material where ambient-damage
   reconstruction was deferred). This is the intended "applied throughout life" behaviour: the rule
   is `max(0, material - 42)` at every tick, identical before and after the challenge, so there is
   no schedule anywhere in the operational code (verified by unit test: the gate pattern
   `now >= CORRUPT_TICK` is absent from the AC104 budget surgery and present in the AC103 defer
   contrast).

2. **The rescue is the same cascade AC104 measured, on a new economy.** On 5804 (material 71, the
   corruption drops material below the obs-bit-1 threshold, the material contact preempts the
   streak, the streak stalls and W/C collapses). Under the budget, the reconstruction defers once
   material reaches the allowance, the streak climbs to its firing threshold, the drop fires, the
   stale route is erased, re-binding restores income, and the deferred reconstruction completes.
   The rescue threshold for 5804 is covered by 42 (the same mechanism-grounded value).

3. **Under late corruption the budget earns the second relinquishment.** On 5800/5805/5806, with
   the corruption coinciding with the second move, the control relinquishes the first move
   (`[1,0]`) but its streak stalls after the corruption and the second move is left un-relinquished;
   the budget, reserving the allowance, completes the second relinquishment (`[1,1]`). This is the
   decision-allowance doing exactly what it was declared to do — funding the decision transition —
   in a phase where the control starves it.

4. **The reconstruction-level harm is a recovery trade-off, not a survival reversal.** On the
   diagnostic 5603 under `late` (material 65/67) both arms die, but the candidate dies 6 ticks
   earlier (12506 vs 12512) with `fw == 2` (reconstruction never completed) where the control
   recovered (`fw == 0`). Reserving the allowance starves the reconstruction in an economy that is
   already doomed, so the budget buys neither reconstruction nor survival there. It did not recur
   on the finals.

## Gates (prespecified in the protocol)

- **G1 (control identity) — PASS 16/16.** At `simult`, `persistent` and `persistent_budget` are
  byte-identical to AC104 (both arms, every final individual).
- **G2 (candidate reconstructs, across the range) — PASS 80/80.** `fw_at_corrupt == 8` and
  `flipped_still_wrong == 0` on every final individual at every condition.
- **G3 (no-harm survival) — PASS.** No individual, at any condition, where the control survives
  and the candidate dies.
- **G4 (no-harm decision) — PASS.** No individual, at any condition, where the control survives
  and the candidate relinquishes less.
- **G5 (state sufficiency) — PASS 16/16.** Per-tick observer-discard on the candidate at `simult`
  byte-identical at every tick (swap applied, `streak_at_swap == 2`).
- **G6 (completeness + determinism) — PASS.** 160 rows; first-row rerun byte-identical.

## Reported, not gated

- **The rescue** (4/160 individuals, seed 5804 priority `(0,3,2,1)` under `simult`/`simult3`) and
  **the reconstruction-level harm** (diagnostic 5603 under `late`, `fw 2 vs 0`), per seed per
  condition. G3/G4 gate the no-harm directions; rescue and harm are per-seed per-condition findings,
  not a universal claim.
- **The relinquishment-completeness improvement** (5800/5805/5806 under `late`: control `[1,0]`,
  candidate `[1,1]`).
- **The move-first boundary** (5802 dies under both arms, `reacquisitions_by_move [1,0]`, `fw == 0`
  both) — the architecture's re-acquisition path, not the budget.
- **The engineering screen's additional rescues** (disclosed): seed 1 `(0,1,3,2)` under
  `simult`/`simult3`, seed 6 `(0,1,2,3)` under `simult3` (control dies 14560 after the third move),
  seed 7 `(3,0,2,1)` under `late` (adversarial renewal-last priority), 5603 under
  `simult`/`simult3` — and zero harm across all 200 engineering rows.
- The material level at the corruption tick and each seed's priority — measured covariates,
  reported not prespecified (untouched seeds).
- Survival is a bimodality-aware lower bound (AC68). No autopoiesis claim; `advance()` and
  `prog.choose` remain supplied format-level machinery.

## Verification

- `audit_ac105.py` passes: source hashes no drift; the six gates re-derived from the saved table
  WITHOUT simulating and matching the recorded result; seed-disjointness; per-arm invariants
  (corruption applied + recovered everywhere, candidate no-harm on survival and relinquishment);
  findings counted (rescue 4, reconstruction-harm 0, relinquishment-improvement 6).
- `replay_ac105.py` passes: first-row rerun byte-identical; baseline identity (both arms == AC104)
  on 5800/0; observer-discard per-tick byte-identical; sampled finals byte-identical across
  conditions; the 5603 diagnostic rescue and the `late` both-die boundary confirmed.
- `test_ac105.py` green (17/17): baseline identity, the budget rule (pure function, no
  `now >= CORRUPT_TICK` gate), `DECISION_ALLOWANCE == STREAK_N * 7`, the five-condition grid,
  the load-bearing rescue (seed 1 and 5603), the `late` reconstruction-harm boundary, conservation,
  and the recorded final outcomes (all six gates, 5804 rescue, 5802 both-die, late relinquishment
  improvement, no reconstruction-harm) read from the frozen rows.
- Core AC1-9 suite (56 tests) green. `audit_ac104.py` still passes (no hash drift) — AC104 and
  every earlier freeze untouched.

## Boundary and next step

The answer to AC104's open question — does allowance 42 generalize to unseen marginal economies —
is **yes on one fresh instance and no-harm everywhere else**: the budget rescues a new marginal
priority `(0,3,2,1)` (5804) on the untouched finals, is neutral or beneficial at every other
operating point, and its only reconstruction-level cost (5603 under `late`) is a diagnostic economy
where both arms die. The operating range is therefore wider than AC104's two diagnostic seeds
suggested, with two named boundaries: (a) `move_first` (5802) kills both arms via the re-acquisition
path, independent of the budget; (b) `late` on a marginal economy (5603, diagnostic) makes the
allowance trade reconstruction completeness for a decision reserve it cannot use. The honest claim
is still the *mechanism* — an internal material budget reserves the decision transition and
coordinates it with reconstruction across timings, priorities and repeated moves — not a fixed
allowance's universality. Boundary unchanged: no autopoiesis claim; `advance()` + `prog.choose`
supplied; the reserve still not part of the architecture. All earlier results preserved untouched.
