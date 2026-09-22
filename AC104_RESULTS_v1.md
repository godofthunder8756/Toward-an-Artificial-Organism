# AC104 results v1: an explicit internal spending rule — a material budget (spendable − STREAK_N×7) is a valid, no-harm, state-sufficient coordinator of reconstruction and decision, but its rescue of the marginal seed is conditional on a marginal economy and did not recur on the fresh sample

Parent: AC103. Frozen per `AC104_PROTOCOL_v1.md` (hashed before the first final seed). Runner
`ac104.py` (a parametrized copy of `ac103.py`'s `_run_core`; the ONLY change is the reconstruction's
per-tick SPEND). Seeds **5700-5707** (fresh, untouched, disjoint from every prior family),
2 histories, 2 arms, 32 rows, 16,384 ticks. `DECISION_ALLOWANCE = STREAK_N * 7 = 42`.

**Headline:** The budget-preservation rule — `budget = max(0, spendable_material −
DECISION_ALLOWANCE)`, applied throughout life with **no `CORRUPT_TICK`** in the operational code —
is a valid internal spending rule: it completes reconstruction, preserves the decision allowance no
worse than the control, and never degrades adaptation or survival (all six gates pass). Its
load-bearing positive effect is real but **conditional**: on the diagnostic marginal seeds (AC103's
5603 and the engineering marginal seed 1, both material 65 at the corruption tick) the control dies
and the budget rescues it (survives, relinquishes 2/2); the rescue **did not recur** on the fresh
sample, which contained no marginal seed (all eight survive under the control). The required
allowance is **seed-dependent** (the rescue threshold is 33 on engineering seed 1, 42 on 5603), so a
fixed declared allowance cannot be gated to rescue every unseen marginal economy — the answer to
AC103's open question is that reconstruction and the decision write *can* be coordinated internally
by a material budget, but only with an allowance large enough for the specific economy.

## Verdict

**All six gates pass.** The question — can the reconstruction and the paid decision write be
coordinated internally, without challenge-specific assistance — is answered at two levels:

- **The rule is a valid, no-harm coordinator (G1-G6 all pass).** The budget is a pure function of
  the current material and the declared constant (`budget_rule(material, allowance) =
  max(0, material − allowance)`), with no challenge-time knowledge (the AC103 defer's
  `now >= CORRUPT_TICK` gate is absent). It is non-binding whenever material exceeds
  `DECISION_ALLOWANCE + _cap` (byte-identical to the control on 6/8 final seeds), and where it
  binds it completes reconstruction (`fw == 0` everywhere), preserves the allowance no worse than
  the control, and never degrades survival or relinquishment.

- **The rescue is real but conditional (reported, not gated).** On the two diagnostic marginal
  seeds the control dies (streak stalls at 4-5, no relinquishment, W/C collapse) and the budget
  rescues it: the reconstruction defers once material reaches the allowance, the streak climbs to
  its firing threshold, the drop fires, the stale route is erased, the organism re-binds, income
  resumes, and the deferred reconstruction completes. The rescue **did not transfer to the fresh
  sample** because the fresh sample (5700-5707) contains no seed where the control dies — the
  closest is 5702 (material 66), which survives under both arms (relinquishing once).

## Per-seed outcome (both histories identical unless noted)

| seed | priority     | mat@8192 | control (persistent)     | candidate (persistent_budget)      |
|------|--------------|----------|--------------------------|------------------------------------|
| 5700 | `[1,3,0,2]`  | 127      | S, relinq 2              | S, relinq 2 (byte-identical)       |
| 5701 | `[1,3,0,2]`  | 107      | S, relinq 2              | S, relinq 2 (byte-identical)       |
| 5702 | `[2,1,0,3]`  | 66       | S, relinq 1              | S, relinq 1 (budget binds, no harm)|
| 5703 | `[3,1,2,0]`  | 89       | S, relinq 2              | S, relinq 2 (byte-identical)       |
| 5704 | `[3,1,0,2]`  | 115      | S, relinq 2              | S, relinq 2 (budget binds, no harm)|
| 5705 | `[0,3,2,1]`  | 95       | S, relinq 2              | S, relinq 2 (byte-identical)       |
| 5706 | `[1,3,2,0]`  | 96       | S, relinq 2              | S, relinq 2 (byte-identical)       |
| 5707 | `[3,2,1,0]`  | 85       | S, relinq 2              | S, relinq 2 (byte-identical)       |

"S" = survives; "relinq N" = relinquishment count. Recovery (`flipped_still_wrong == 0`) is 16/16
under both arms. No final individual dies under either arm, so the rescue (candidate survives where
control dies) is 0/16 on the final sample.

The diagnostic rescue (disclosed engineering, NOT final seeds):

| seed | priority     | mat@8192 | control       | candidate          |
|------|--------------|----------|---------------|--------------------|
| 5603 | `[1,2,3,0]`  | 65       | D8409, relinq 0 | **S, relinq 2**   |
| 1    | `[0,1,3,2]`  | 65       | D8408, relinq 0 | **S, relinq 2**   |

## The mechanism, measured

1. **The budget is preserved (measure a).** Post-corruption `allowance_breached` (ticks with
   material < 42) is far lower under the candidate on the marginal seeds — 5603: 46 → 17; engineering
   seed 1: 49 → 10 — and no worse on every other seed (G3). The budget's floor is on the
   *reconstruction's* spend only; the competing writes (action-2 repair, births, the streak itself)
   still consume material below the allowance on the death spiral, which is why the allowance is a
   *reservation*, not a global floor.

2. **Reconstruction completes (measure b).** `fw == 0` on every final individual under the
   candidate (G2). The persistent trigger stays engaged while material is below the allowance, and
   the reconstruction resumes and completes once the decision re-establishes income.

3. **The organism adapts and survives (measure c).** On every final individual the candidate
   survives and relinquishes ≥ the control (G4). On the diagnostic marginal seeds the candidate
   survives and relinquishes 2/2 where the control dies.

4. **The rescue threshold is seed-dependent.** On engineering seed 1 (material 65, priority
   `[0,1,3,2]`) the threshold is 33; on 5603 (material 65, priority `[1,2,3,0]`) it is 42. Below
   the threshold the organism dies either with the streak stalled (allow ≤ 28, `fw == 0`) or with
   the reconstruction starved (allow 29-32, `fw > 0`). A single Gray transition (7) is
   insufficient: the reconstruction drains material below a 7-unit reserve before the streak can
   climb to its firing threshold. `STREAK_N * 7 = 42` — the full relinquishment (STREAK_N−1 = 5
   Gray increments plus the drop's register write, each 7 replicas) — is the mechanism-grounded
   value and covers both diagnostic marginal seeds. That the threshold differs between two seeds
   with identical material is the priority's effect on the material trajectory (AC39's
   seed-dependence, in the unfavourable direction for a fixed allowance).

## Gates (prespecified in the protocol)

- **G1 (control identity) — PASS 16/16.** `persistent` is byte-identical to AC103 `persistent`
  on every final individual.
- **G2 (candidate reconstructs) — PASS 16/16.** `fw_at_corrupt == 8` and `flipped_still_wrong == 0`
  on every final individual.
- **G3 (allowance preserved no worse than control) — PASS 16/16.** `allowance_breached` (candidate)
  ≤ `allowance_breached` (control) on every final individual.
- **G4 (adaptation + survival not degraded) — PASS 16/16.** Every final individual where the
  control survives, the candidate survives AND relinquishes ≥ the control.
- **G5 (state sufficiency — observer-discard on the candidate) — PASS 16/16.** Per-tick
  observer-discard on `persistent_budget` byte-identical at every tick (non-vacuous: swap applied,
  mid-streak).
- **G6 (completeness + determinism) — PASS.** 32 rows; first-row rerun byte-identical.

## Reported, not gated

- **The rescue is conditional on a marginal economy, and the fixed allowance is seed-dependent.**
  The budget rescues the two diagnostic marginal seeds; it cannot be gated to rescue every unseen
  marginal economy because the required allowance varies with the seed's priority (33 vs 42). The
  fresh sample happened to contain no marginal seed, so the rescue did not recur.
- **The budget binds without harm on two final seeds.** 5702 (material 66) and 5704 (material 115)
  differ from the control (`budget_is_persistent` False) yet survive with the same relinquishment
  count — the budget changes the material trajectory without changing the outcome.
- The relinquishment-completeness improvement seen in engineering (candidate relinq 2 vs control 1
  on engineering seeds 6/7) did not recur on the finals (every final survivor relinquishes 2/2 under
  both arms).
- The material level at the corruption tick and each seed's priority — measured covariates, reported
  not prespecified (untouched seeds).
- Survival is a bimodality-aware lower bound (AC68). No autopoiesis claim; `advance()` and
  `prog.choose` remain supplied format-level machinery.

## Verification

- `audit_ac104.py` passes: source hashes no drift; the six gates re-derived from the saved table
  WITHOUT simulating and matching the recorded result; seed-disjointness; per-arm invariants
  (corruption applied + recovered everywhere; candidate no-harm on survival, relinquishment, and
  allowance preservation; rescue count on the final sample = 0).
- `replay_ac104.py` passes: first-row rerun byte-identical; control identity on 5702 byte-identical
  to AC103 persistent; observer-discard on the candidate per-tick byte-identical; the diagnostic
  rescue (5603) confirmed and the closest-to-marginal final seed (5702) byte-identical.
- `test_ac104.py` green (11/11): control identity, the budget rule (pure function, no
  `now >= CORRUPT_TICK` gate), non-binding on healthy material, load-bearing rescue of the marginal
  seeds (engineering 1 and 5603), `DECISION_ALLOWANCE == STREAK_N * 7`, observer-discard on the
  candidate, conservation, and the recorded final outcomes (all survive under both arms, 5702
  relinq 1) read from the frozen rows.
- Core AC1-9 suite (56 tests) green. No frozen runner modified (`ac103.py`, `ac102.py` and every
  earlier freeze untouched).

## Boundary and next step

The answer to AC103's open question is that the reconstruction and the paid decision write **can**
be coordinated internally by an explicit material budget, without challenge-time knowledge: the
allowance is preserved, reconstruction completes, and the marginal seed is rescued. The limit is
that the required allowance is **seed-dependent**, so a fixed declared allowance is a coordination
mechanism, not a universal rescue — the organism can reserve a decision budget, but the right size
of that budget depends on its economy, and no single fixed value is guaranteed to cover an unseen
marginal economy. This is the same seed-dependence that has run through the whole allocation line
(AC11, AC15, AC96-99): the decision's affordability is economy-dependent, and the honest claim is
the *mechanism* (an internal budget reserve can coordinate reconstruction and decision), not a
fixed allowance's universality. Boundary unchanged: no autopoiesis claim; `advance()` +
`prog.choose` supplied; the reserve still not part of the architecture. All earlier results
preserved untouched.
