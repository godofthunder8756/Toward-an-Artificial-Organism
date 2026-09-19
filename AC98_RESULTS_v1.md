# AC98 results v1: unconditional adaptation PLUS a no-harm gate, on unseen seeds — the revised reserve removes the harm but does not achieve unconditional self-preservation (G1 falsified, G2 passes)

Parent: AC98-D2 (engineering). Frozen per `AC98_PROTOCOL_v1.md` (hashed before the first final seed).
Runner `ac98.py`; seeds **4436-4439** × 2 histories, 16 rows, 16,384 ticks, `transition='perm'` (the
relinquishment world). Two arms per individual: `reserve` (the revised reserve — release on drop OR
streak-stall OR W-low) and `no_reserve` (the AC97 no-reserve architecture, byte-identical to
`ac97.run(..., reserve=False)` — the direct control). The final family is **unseen**: no screening,
disjoint from engineering 0-7, the D1/D2 seeds 4412-4415, the AC96 screening sweep 4412-4431, and every
prior final family ≤ 4435.

## Verdict

**The unconditional adaptation criterion (G1) is falsified on the unseen family; the no-harm gate (G2)
passes.** The revised reserve removes AC97's *harm* — there is **no** distinct seed where the no-reserve
control survives and the reserve arm dies (G2, 4/4). But it does **not** achieve unconditional
self-preservation: on seed 4436 the reserve arm stalls the relinquishment streak at 3 (the W-bound 3→4
increment) and dies at 8430 without ever relinquishing, where the no-reserve control also dies. The
reserve satisfies all four measures on 3/4 distinct seeds (4437, 4438, 4439) and fails on 1/4 (4436).
G1 is **FAIL**, recorded not moved; G2/G3/G4/G5 pass.

In one sentence: the revised reserve is no longer **net harmful** (the AC97 failure mode is eliminated),
but it is also not **sufficient** — a fixed one-shot material reserve cannot hold the W catalyst ≥ 3
through the repeated W-death window that a phase-shifted post-move build can enter, and on the unseen
family that limit is fatal (4436) rather than merely non-relinquishing (the D2 4435 residual).

## Per-seed outcome (both histories identical)

| seed | priority    | reserve arm                                    | no_reserve (control)          |
|------|-------------|------------------------------------------------|-------------------------------|
| 4436 | `[1,3,0,2]` | **dies 8430** (streak stuck 3, wlow@8230, W/C collapse) | **dies 8448** (streak never builds) |
| 4437 | `[2,0,1,3]` | drop@8220, reacq@8221, survives (W=3, C=2)     | **dies 8453**                 |
| 4438 | `[0,3,2,1]` | stall@8227, drop@8229, reacq@8233, survives    | drop@8231, reacq@8233, survives (tie) |
| 4439 | `[2,1,3,0]` | stall@8220, drop@8222, reacq@8224, survives    | **dies 8442**                 |

- Reserve arm: 3/4 distinct seeds relinquish + reacquire + survive; 1/4 dies with the drop never firing.
- No-reserve control: 1/4 relinquish + survive (4438); 3/4 die (4436, 4437, 4439).
- The load-bearing direction (reserve survives/relinquishes where the control dies) holds on 4437 and
  4439; 4438 is a tie (both pass); 4436 is a joint failure (both die).

## The mechanism (the honest new finding)

**4436 is the AC98-D2 4435 residual in the fatal direction.** On 4436 (`priority [1,3,0,2]`) the reserve
arms at t=538 (21 withheld), and the post-move streak build (0→1→2→3 over 8229-8232) **stalls at 3**: the
3→4 increment needs `cap = min(32, 8·W, energy, material) ≥ 21`, i.e. W ≥ 3, and on this seed's
phase-shifted build W is below 3 during the build window (action 1, the stale material contact, preempts
the W-birth rule while material ≤ 64). The `wlow` release fires at 8230 (releases the 21, material rises
above 64, obs bit 1 clears, W recovers once) — but a one-shot material release cannot hold W ≥ 3 through
the repeated W-death window, so the streak stays at 3, the entry expires into blind re-acquisition, and
the organism dies at 8430 with W=0, C=0, energy=0 (the W/C death cascade; fuel 60 at death, the
unconsumed-residue signature). On D2's 4435 the same stall *survived*; on 4436 it does not — the phase
shift lands differently and the one-shot W recovery is insufficient.

**This is not a no-harm violation, and the distinction matters.** On 4436 the no-reserve control also dies
(8448) — the control never even builds the streak (relinquishments 0, W/C collapse). So the reserve's
death is a G1 failure (the reserve fails to *help* on a seed where the control also fails), not a G2 harm
(the control does not survive). The no-harm gate — the gate that would have caught AC97's 4434/4435
failures, where the control *did* survive — is exactly what AC98 passes and AC97 failed.

Two honest side-notes, reported not gated: (a) on 4436 the reserve arm dies **18 ticks earlier** (8430)
than the control (8448) — a phase-shift timing effect, not a survival flip, but the revised reserve does
not merely fail to help there; (b) the reserve's own armed 21 and its ~13-21 reserve-write units are
absorbed, so the maintenance trade-off is not what kills 4436 — it is the W-bound increment limit, which a
material reserve cannot address regardless of size (the D1 probe already showed smaller levels regress on
the D1/D2 family and larger holding windows drift the phase further).

## Gates (prespecified in the protocol)

- **G1 unconditional adaptation — FAIL.** Seed 4436 fails A4 (survival) and A1 (relinquishment); A3
  (continued W/C/B production post-move) also fails on it (W_births_post_move = 0). 3/4 distinct seeds
  satisfy all four measures. Recorded, not moved.
- **G2 no-harm — PASS 4/4.** No distinct seed where the no-reserve control survives and the reserve arm
  dies. On 4436 the control dies too; on 4437/4439 the reserve survives where the control dies; on 4438
  both survive and relinquish.
- **G3 state sufficiency (per-tick observer-discard) — PASS 8/8.** The reserve-arm run with the
  succession observer + host streak dict discarded at a mid-streak tick is byte-identical at every one of
  16,384 ticks (`per_tick_identical`, `swap_applied`, `streak_at_swap == 2` on all 8 individuals). State
  sufficiency (AC96) is unaffected by the economic finding; the three release conditions are pure
  functions of maintained organism state.
- **G4 endogenous reserve (no external rescue) — PASS.** Every reserve individual: `reserve_m > 0` and
  `reserve_released_m <= reserve_m`. On 4436 the 21 is withheld and released (wlow), never injected; on
  4437/4438/4439 the 42 withheld / 21 released pattern holds with the residual re-armed 21 benign.
- **G5 completeness + determinism + control equivalence — PASS.** 16 rows; sampled rerun byte-identical;
  the no-reserve control is byte-identical to `ac97.run(..., reserve=False)` on all 8 individuals — the
  revised reserve is the only change from the AC97 architecture.

## Reported, not gated

- **The maintenance trade-off.** Per individual the reserve withholds 21 (4436) or 42 (4437-4439) and
  releases 21; its paid arm/disarm/repair writes cost 13-21 units, a small fraction of the ~1130-2330 paid
  bank-1 repair writes in the same run. The trade-off is seed-dependent (AC97's lesson): benign where the
  drop fires (4437/4438/4439) and not the cause of death where it does not (4436 dies of the W-bound
  increment, not material).
- **The 4435 residual recurred, fatally.** The D2 engineering documented 4435 as "survives but never
  relinquishes" — a phase-shift limit of any pre-move material reserve. On the unseen family the same
  limit recurs on 4436 and this time it is **fatal** (the organism does not survive the W/C collapse that
  a one-shot W recovery cannot reverse). The protocol's scope note predicted this recurrence; it is
  recorded, not hidden.
- **Survival is a bimodality-aware lower bound** (AC68). The reserve arm's 3/4 survival is a lower bound
  on the true rate; the no-reserve control's deaths are the material-starve / attention-hijack cascade.
- **The reserve is a fixed minimum reserve, not an acquired allocation decision.** `RESERVE_LEVEL = 21`
  and the `drop`/`stall`/`wlow` release triggers are declared world constants. The failure is in the fixed
  mechanism's interaction with the W-bound streak increment, not in an acquired policy. The question "does
  the organism *acquire* how much to save" remains open, now joined by "can any *material* reserve survive
  a W-bound increment — or does the reserve need to be denominated in the resource the decision is actually
  starved of (W / a repair-catalyst reserve, not material)".
- **Priorities.** 4436 `[1,3,0,2]`, 4437 `[2,0,1,3]`, 4438 `[0,3,2,1]`, 4439 `[2,1,3,0]` — none is AC83's
  adversarial `[3,0,2,1]`. The relinquishment is a streak/register decision, not a renewal-contention
  decision, so the priority ordering does not confound the mechanism.
- **Supplied machinery remains.** `advance()` and `prog.choose` are still host-supplied format-level
  machinery; no autopoiesis claim. Affordability is the question, and the answer is: the revised reserve is
  no longer harmful but still not unconditionally sufficient.

## Verification

- `audit_ac98.py` passes: 16 rows, 17 hashes no drift, arm invariants (reserve-arm deaths 8430 on 4436;
  no-reserve deaths 8442/8448/8453; the no-harm direction), observer-discard record 8/8 per-tick,
  control-equivalence record 8/8, gates re-derived WITHOUT simulating and matching the recorded result —
  including the recorded G1 FAIL (a falsification is preserved, not concealed).
- `replay_ac98.py` passes: 2/2 exact (state_hash + endpoint fields), observer-discard 1/1 per-tick
  byte-identical, control-equivalence 1/1.
- `test_ac98.py` 23/23 green: single-step reserve primitives (arm withholds 21 + paid write, refuses when
  poor / W=0, release restores + disarms with `released <= withheld`, majority read, atomic write), the
  two new release triggers (stall on refused increment, wlow on failing catalyst, no release when
  disarmed), the D2 engineering flip/no-regression/no-harm/byte-identity checks, and the **D3 finals
  recorded-outcome regressions** — G1 fails on 4436 (dies, streak stuck 3) while 4437/4438/4439 pass,
  G2 holds on the finals, the no-reserve control is byte-identical to ac97, seed-disjointness, and the
  recorded gates (G1 FAIL, G2/G3/G4/G5 PASS). A future code change that moves the record is caught.
- Core AC1-9 suite 56/56 green. No frozen runner was modified (`ac97.py` and every earlier freeze are
  untouched; the `ac97_results_v1` audit still passes).

## Boundary and next step

The internally maintained organization does **not** afford self-preservation through the move under the
unconditional criterion even with the revised reserve: the revised reserve eliminates AC97's *harm*
(G2 passes — no seed where the control survives and the reserve dies) but fails G1 on 1/4 unseen seeds
(4436), where the W-bound 3→4 streak increment stalls the drop and a one-shot material release cannot
hold W ≥ 3 through the W-death window. The affordability question is therefore answered **negatively for
a material reserve** on this unseen family — but the failure has narrowed from "sometimes kills" (AC97)
to "sometimes still fails to help" (AC98), and the residue is a *W*-denominated shortfall, not a
material one. The next architecture needs a reserve denominated in (or able to restore) the repair
catalyst itself — e.g. a W/catalyst reserve or a release that triggers W-birth directly — none of which
changes the standing boundary (transition logic + interpreter still supplied; no autopoiesis claim). All
earlier results (ac97_results_v1, ac98_d2_engineering_v1, and every prior freeze) are preserved untouched.
