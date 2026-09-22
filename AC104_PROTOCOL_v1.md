# AC104 protocol v1: one explicit internal spending rule — budget reconstruction from spendable material minus a declared decision-transition allowance (no CORRUPT_TICK)

STATUS: **frozen before the first final seed.** Written 2026-09-21. Parent: AC103 (frozen).

AC103 separated premature termination (a RECOVERY failure, closed on five of six staged-recovery
seeds by a persistent trigger) from resource shortage (a SURVIVAL failure, present even when the
reconstruction completes, `fw == 0`). Its state-dependent defer (`budget = 0` while
`now >= CORRUPT_TICK and material <= 64`) used advance knowledge of the challenge tick and tested
"stop once scarce," NOT "limit spending to preserve a decision budget" — an organism just above 64
can still spend its way below it. The defer's failure (5603 dies 8410 with `fw == 2`) therefore
does NOT reject the budget-preservation hypothesis (see `AC103_ERRATA_v1.md`).

This protocol freezes the direct test of that hypothesis, with ONE explicit spending rule and NO
search. The reconstruction's per-tick spend is

    budget = max(0, spendable_material - DECISION_ALLOWANCE)

where `DECISION_ALLOWANCE` is a declared constant reserving material for the next internal decision
transition. The budget is applied **THROUGHOUT LIFE** — there is **no `CORRUPT_TICK`** (or any other
challenge-time knowledge) in the operational code; the budget is a pure function of the current
material and the declared constant, identical before and after the challenge. It is further bounded
by the frozen W-catalyzed capacity `_cap = min(32, 8·W, energy, material)`, so the policy never
exceeds the produced machinery's capacity.

SOURCES (declared): ac104.py ac103.py ac102.py ac101.py ac100.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC104_PROTOCOL_v1.md

## What is NOT changed (the resource model is untouched)

The reconstruction (`reg_from_active`) keeps its total prices (1 energy + 1 material per replica),
its machinery requirement (the W-catalyzed `_cap`), and its world (corruption at t=8192, two route
reversals at t=8192 and t=12288, the Gray streak, the erase-on-relinquishment, every world
constant). The persistent trigger is kept (fire until the decoded program matches the
description-derived target). The ONLY change is the per-tick spend: `budget = max(0, material -
DECISION_ALLOWANCE)` instead of the AC103 defer's `0 if (now >= CORRUPT_TICK and material <= 64)
else None`. No decision write is made material-independent; no reserve is added; no accepted
internal-memory milestone is reopened.

## The declared allowance

The internal decision (relinquishment) fires after `STREAK_N = 6` failure events: `STREAK_N - 1 =
5` Gray streak increments (each a 1-bit transition, 7 replicas = 7 material) plus the terminal
drop's register write (up to 7 replicas). Every event is a 7-replica Gray transition. The full
decision therefore needs `STREAK_N * 7 = 42` material, and that is the declared value:

    DECISION_ALLOWANCE = STREAK_N * 7 = 42

Rationale (from the disclosed engineering screen below): a *single* transition (7) is insufficient
— the reconstruction drains material below a 7-unit reserve before the streak can climb to its
firing threshold — and the rescue threshold is seed-dependent (33 on the engineering marginal seed,
42 on the AC103 marginal seed 5603). `STREAK_N * 7 = 42` is the mechanism-grounded value covering
both. The allowance is a floor on the *reconstruction's* spend, NOT a global material floor: the
competing writes (action-2 repair, W/C/B births, memory renewal, the streak write itself) can still
consume material below 42, which is exactly what measure (a) quantifies.

## Arms (all on `corrupt=True` + the two-move SCHEDULE)

| arm                | trigger   | per-tick spend                    |
|--------------------|-----------|-----------------------------------|
| `persistent`       | persistent| None (immediate) — == AC103 `persistent` |
| `persistent_budget`| persistent| `max(0, material - DECISION_ALLOWANCE)` |

`persistent` is byte-identical to AC103's persistent arm (the frozen reference); the candidate
differs ONLY by the per-tick budget computation. The budget is non-binding whenever `material >
DECISION_ALLOWANCE + _cap` (the ordinary healthy regime), so the candidate is byte-identical to
the control there; it diverges only where material is scarce enough that reserving the allowance
changes the reconstruction's spend.

## Screening disclosed (engineering, before this protocol was frozen)

Engineering ran on seeds 0-7 (disjoint from the final sample) plus the AC103 failure seeds 5603
(marginal), 5607 (starvation) and 5601/5602/5604/5605/5606 (cementing) as diagnosis, 16,384 ticks,
both histories:

- **The budget is a valid single change.** `persistent` is byte-identical to AC103 `persistent`
  (control identity, seeds 0-2 verified).
- **The allowance value matters (a sweep, not a search).** On the engineering marginal seed 1
  (material 65) the rescue threshold is 33; on the AC103 marginal seed 5603 (material 65, priority
  `[1,2,3,0]`) it is 42. Below the threshold the organism dies either with the streak stalled (allow
  ≤ 28, `fw == 0`, relinq 0) or with the reconstruction starved (allow 29-32, `fw > 0`). A single
  transition (7) is insufficient. `STREAK_N * 7 = 42` covers both.
- **The budget rescues the marginal seeds and harms nothing.** `persistent_budget` (allow 42)
  survives + relinquishes 2/2 where `persistent` dies (engineering seed 1 and final 5603, both
  histories); on every seed where the control survives it is byte-identical (no harm); on
  engineering seeds 6/7 it relinquishes on BOTH moves where the control relinquishes once (relinq
  2 vs 1).
- **The allowance is preserved.** Post-corruption `allowance_breached` (ticks with material < 42)
  is far lower under the candidate on the marginal seeds (5603: 46 → 17; engineering seed 1: 49 →
  10), and no worse anywhere else.

The gates below are shaped by this engineering screen on disjoint seeds; the final seeds are NOT
screened (see Anti-drift).

## Gates (prespecified, categorical per distinct seed; both histories must satisfy each)

- **G1 (control identity — the single-change license).** Every final individual: `persistent` is
  byte-identical (`state_hash`) to AC103 `persistent`.
- **G2 (the candidate completes reconstruction — measure b).** Every final individual: the
  candidate applies the corruption (`fw_at_corrupt == CORRUPT_BITS`) and recovers
  (`flipped_still_wrong == 0`).
- **G3 (the allowance is preserved no worse than the control — measure a).** Every final
  individual: the candidate's post-corruption `allowance_breached` is ≤ the control's (the budget
  reserves the decision allowance without making the reserved-material loss worse).
- **G4 (adaptation + survival are not degraded — measure c).** Every final individual where the
  control survives: the candidate survives AND the candidate's relinquishment count is ≥ the
  control's (the budget does not starve the decision).
- **G5 (state sufficiency — observer-discard on the CANDIDATE).** Per-tick observer-discard on
  `persistent_budget` is byte-identical at every tick (non-vacuous: `swap_applied`,
  `streak_at_swap == 2`). Run on the candidate directly (AC103 errata's correction).
- **G6 (completeness + determinism).** Row count == 8 seeds × 2 histories × 2 arms (32); a sampled
  exact rerun of the first row is byte-identical (`state_hash`).

## Reported, not gated

- **The rescue** (the candidate survives where the control dies) — the load-bearing positive
  signature. On the diagnostic seeds it holds on the two marginal seeds (engineering 1, final 5603);
  whether it recurs on the fresh sample is reported per seed, not gated (the rescue threshold is
  seed-dependent, so a fixed declared allowance cannot be gated to rescue every unseen marginal
  economy).
- **The relinquishment-completeness improvement** (candidate relinq 2 vs control 1 on engineering
  seeds 6/7).
- The seed-dependence of the rescue threshold (33 vs 42) and its mechanism (the allowance must
  cover the full streak climb, `STREAK_N * 7`, not a single transition).
- The material level at the corruption tick and each seed's priority — covariates, reported not
  prespecified (untouched seeds).
- Survival is a bimodality-aware lower bound (AC68). No autopoiesis claim; `advance()` and
  `prog.choose` remain supplied format-level machinery.

## Anti-drift rules

- The runner creates `ac104_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed
  set (which includes this protocol file).
- `test_ac104.py`, `audit_ac104.py`, `replay_ac104.py` are NOT hashed into the frozen snapshot
  (AC17's rule).
- Engineering seeds (0-7) and the diagnostic seeds (5601-5607) are excluded from the final sample.
  The final seeds 5700-5707 are a fresh range, disjoint from every prior family (0-7, 4412-4439,
  4440-4443, 4444-4447, 4448-4451, 4466/4481/4504/4510, 4600-4871, 4872-5099, 5100-5507,
  5600-5607) and are NOT screened — no final outcome is observed before the freeze; `mat_at_corrupt`
  and priority are measured, not selected on.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh
  seeds.
- The frozen AC103 results and every earlier freeze are untouched.

## Source hashes (computed before the first final seed)

    (recorded in ac104_results_v1/pre_run_snapshot.json at freeze time)
