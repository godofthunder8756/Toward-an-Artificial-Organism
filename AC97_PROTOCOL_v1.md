# AC97 protocol v1: an unconditional adaptation criterion on unseen seeds — the internally maintained organization affords self-preservation through the move

STATUS: **frozen before the first final seed.** Written 2026-09-19. This is the protocol + finals for
AC97-D3, the last step of the AC97 affordability line. AC97-D1 located the decisive budget shortfall
behind the AC96 "economically fragile" finding: in the relinquishment world (`transition='perm'`) the
route move zeroes the material-income channel, material drains to a floor of 3-6, and the
relinquishment decision's own writes — the drop's register write (7 replicas) and the streak reset (14
replicas, 21 material in total) — are refused at the 6th unproductive contact. AC97-D2 implemented the
fix (`ac97.py`): an internally enforced minimum material reserve (a single maintained-state bit at
`traces[1, 540]`, damaged + repaired) that withholds `RESERVE_LEVEL = 21` material from a productive
material contact's intake and releases it in `_drop` before the cap check. On the D2-named seeds
4412-4415 the reserve moved the maintained arm from **2/8 relinquish + 2/8 survive to 8/8 + 8/8**, with
no external rescue and no measurable maintenance harm, and fixed the observer-discard comparison to
per-tick. This protocol freezes the claim on **unseen** seeds: **the internally maintained
organization, with an internal minimum resource reserve, affords self-preservation through the route
move — per an unconditional, per-individual adaptation criterion.**

SOURCES (declared): ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC97_PROTOCOL_v1.md

## The question and the claim

AC96 froze state sufficiency (the trajectory is determined by maintained internal state plus the
environment) and reported, as its honest headline, that the internalized relinquishment decision is
*economically fragile*: its paid write (increment, reset) AND its repair are starved by the very income
collapse the decision exists to pre-empt, so the maintained arm relinquishes 2/8 and dies 6/8 in the
move world. AC97 asks the affordability question the card named: can the internally maintained
organization **afford** self-preservation through the move, using only its own income? The claim is
that it can, via an internal minimum resource reserve, and the decisive test is the **unconditional
adaptation criterion** below — unconditional in the specific sense that it is stated per individual and
is NOT conditioned on affordability, survivorship, or anything post-hoc. The direct control is the
frozen ac96 maintained arm (this runner with the reserve disabled, byte-identical to `ac96.run(..., 
streak_maintained=True)`), which carries the ac96 economic fragility.

The four measures, recorded for every individual of both arms:

1. **relinquishment** — the stale route (key 1, moved at t=8192) is dropped: the streak reaches the
   threshold and `_drop` fires, the register bit reads set (majority True), and the entry is erased.
2. **reacquisition** — the moved key is re-bound after the drop (a None→bound transition on key 1 at a
   tick strictly after the drop tick).
3. **continued machinery production** — W, C, and B births each continue after the move (each class has
   ≥ 1 birth in the post-move window `t >= MOVE_TICK`).
4. **survival** — `completed` (the organism survives to the horizon).

The gates (prespecified, categorical per distinct seed; the two histories are a repeated measure):

1. **G1 unconditional adaptation.** Every final distinct seed: the reserve arm satisfies all four
   measures (A1 relinquishment, A2 reacquisition, A3 continued machinery production, A4 survival).
   Stated per distinct seed (4 seeds); the two histories are a repeated measure and are verified
   identical per seed (state_hash equality), then counted once.
2. **G2 reserve is load-bearing (direct-control contrast).** On at least one distinct final seed the
   no-reserve control (the frozen ac96 maintained arm) fails to relinquish (`relinquishments == 0`)
   while the reserve arm relinquishes (≥ 1); AND on at least one distinct final seed the no-reserve
   control dies (`not completed`) while the reserve arm survives. The two measures the reserve directly
   funds — the drop write and the survival it enables.
3. **G3 state sufficiency (per-tick observer-discard).** Every final individual (4 seeds × 2 histories):
   the reserve-arm run with the succession observer AND the alloc (clearing the vestigial host streak
   dict) discarded at a mid-streak tick is **byte-identical at every tick** (`per_tick_identical`, the
   trajectory-level comparison D2's correction #1 requires — not the terminal state_hash), non-vacuously
   (`swap_applied`, `streak_at_swap == 2`).
4. **G4 endogenous reserve (no external rescue).** Every final reserve individual: the reserve was
   armed from the organism's own income (`reserve_m > 0`) and no more is ever released than was withheld
   (`reserve_released_m <= reserve_m`, net standing ≥ 0). There is **no rescue arm** in the finals; the
   reserved material is the organism's own previously-withheld intake, not an injected resource.
5. **G5 completeness + determinism + control equivalence.** Row count == seeds × 2 histories × 2 arms
   (16); a sampled exact rerun of the first row is byte-identical (state_hash); and the no-reserve
   control is byte-identical to `ac96.run(..., streak_maintained=True)` on every final individual — the
   reserve is the only change from the frozen ac96 architecture.

## The mechanism (what changed, and why)

- **D1 — diagnosis.** In the ac96 relinquishment world, the move zeroes the material-income channel,
  material drains to 3-6, and the drop's register write (7 replicas) and the streak reset (14 replicas)
  — 21 material in total — are refused at the 6th unproductive contact, while energy (120-127) and W
  (2-3) are abundant. The decision's own writes are the shortfall.
- **D2 — the reserve.** A single maintained-state bit at `traces[1, RESERVE_OFFS = 540]` (a free bank-1
  region; slots 0-519, pointer 520-521, CTRL 522-539 are occupied) holds "armed (1) / disarmed (0)".
  When armed, `RESERVE_LEVEL = 21` material units are withheld from the organism's spendable pool.
  - *Accumulation (arm).* On the first productive *material* contact after development (`t >= DEV = 512`),
    the organism withholds 21 material from that contact's intake (`b.material -= 21`, `e['in_m'] -= 21`,
    the AC15 "intake is a variable" identity, so `ac4.balance` holds by construction) and sets the bit
    (a paid, W-gated, atomic write). The reserved material is not in `b.material`, so no lower-priority
    write can reach it.
  - *Release.* In `_drop`, when `material < RESERVE_LEVEL` (the pool cannot cover the drop's 7 + the
    reset's 14), the reserve is released (`b.material += min(21, room)`, `e['in_m'] += …`) and the bit
    cleared (paid). The drop and reset then spend against the augmented pool.
  - *Damage + repair.* The bit is damaged by the same sticky bank-1 stream and repaired by a paid
    majority-restore (`reg_reserve`, minority ≥ RESERVE_TRIGGER = 2). It is genuinely vulnerable
    (majority read, `RESERVE_THRESHOLD = 4`).
  - *Internal, not host state.* The arm/release read and write `traces[1, 540]` only; `reserve_events`
    is an observational log, never read to steer a write.
  - *No external rescue.* The reserved material is the organism's own income, withheld then released;
    `reserve_released_m <= reserve_m` is the endogeneity invariant.
- **D3 — no new mechanism.** D3 adds the finals collector, freezes the unconditional criterion, and
  re-uses the per-tick observer-discard hook (`swap_at`) that D2 already implemented. Nothing about the
  organism changes in D3.

## World, arms, seeds

World constants unchanged from AC96, `transition='perm'` (the relinquishment world). PORTS=4, YIELD=64,
TICKS=16384, CORRUPT_TICK=8192, MOVE_TICK=8192, sticky 1e-4 damage on both banks (independent streams),
STREAK_N=6, STREAK_THRESHOLD=4, REGISTER_THRESHOLD=4, RESERVE_LEVEL=21, RESERVE_OFFS=540,
RESERVE_THRESHOLD=4, RESERVE_TRIGGER=2, the order-preserving generic-over-syntax decoder, AC75's
erase-on-relinquish. `corrupt=False` for every condition (the move is the sole event; corruption at
t=8192 would be a second, unrelated challenge).

Two arms per individual:

- `reserve` — `reserve=True`, `damage=True` (the arm under test).
- `no_reserve` — `reserve=False`, `damage=True` (the direct control: the frozen ac96 maintained arm,
  byte-identical to `ac96.run(..., streak_maintained=True)`).

16 rows = 4 seeds × 2 histories × 2 arms. History is a trivial repeated measure (the runner gates
`activation=[True,True]` and the RNG seeds depend on seed, not history), so the two histories are
identical per seed; the criterion is stated per distinct seed, with history identity verified per seed.

Final seeds `4432, 4433, 4434, 4435` (4 seeds × 2 histories = 8 individuals), **unseen**: disjoint from
engineering 0-7, from the D1/D2 engineering seeds (4412-4415), from the AC96 screening sweep (4412-4431),
from every prior final family ≤ 4415 (AC93 4400-4403, AC94 4404-4407, AC95 4408-4411, AC96 4412-4415),
and from the separate 4600-4871 order-line families and the 5100-5507 confirmatory families. **No
screening of this final family** — the gates above were shaped by the D2 engineering result on the
disjoint D1-named seeds 4412-4415 (disclosed below), and the final family itself is untouched.

## Screening disclosed (before this protocol was frozen)

The gate shapes were informed by the D2 engineering run on the disjoint seeds 4412-4415 (recorded in
`AC97_D2_RESULTS.md`), not by the final family. Measured there: the reserve arm relinquishes and
survives 8/8 (every drop followed by re-acquisition of key 1 within 1-3 ticks, W=3 C=2, both routes bound
at end-of-run); the no-reserve control relinquishes 2/8 (seed 4413 only) and survives 2/8, the other 3/4
seeds dying at 8415-8444 with the streak stalled at 5. The AC96 screening of 4412-4431 independently
found the ac96 maintained arm relinquishes on exactly one of 20 seeds (4413). Consequences, all reflected
in the gate shapes above: G1 is the reserve arm's own per-individual criterion (not a margin over the
rival — AC16/17/18); G2 is a per-seed contrast, not a mean; G4 is the endogeneity invariant (there is no
external rescue in the success arm); the maintenance trade-off is reported, not gated (it is a
behavioural finding, not the claim). A family where the reserve arm fails to relinquish on a seed would
fail G1; a family where the no-reserve control relinquishes and survives on every seed would fail G2 —
both are the honest possibilities and neither is pre-smoothed.

## Gates (prespecified, categorical per distinct seed)

- **G1 (unconditional adaptation).** For every distinct final seed, the reserve arm satisfies A1
  (`relinquishments >= 1`, a drop tick with the register bit set), A2 (`reacquire_ticks[1]` non-empty
  and its first tick > the first drop tick), A3 (`W_births_post_move > 0` and `C_births_post_move > 0`
  and `B_births_post_move > 0`), and A4 (`completed`). Both histories must satisfy it (identity verified
  per seed).
- **G2 (reserve is load-bearing).** ≥ 1 distinct seed with no-reserve `relinquishments == 0` and reserve
  `relinquishments >= 1`; AND ≥ 1 distinct seed with no-reserve `not completed` and reserve `completed`.
- **G3 (state sufficiency, per-tick observer-discard).** Every individual: `status != 'no_mid_streak'`,
  `swap_applied`, `streak_at_swap == 2`, and `per_tick_identical` (byte-identical at every one of 16,384
  ticks — trajectory-level, not endpoint-level).
- **G4 (endogenous reserve).** Every reserve individual: `reserve_m > 0` and `reserve_released_m <=
  reserve_m`. No rescue arm in the finals.
- **G5 (completeness + determinism + control equivalence).** 16 rows; sampled rerun of rows[0]
  byte-identical; no-reserve control byte-identical to `ac96.run(..., streak_maintained=True)` on all 8
  final individuals.

## Reported, not gated

- **The maintenance trade-off.** The 21-unit withholding is absorbed by the material cycle's slack
  (material oscillates 37-128 on a 64-unit contact cycle), not converted into fewer W/C/B births or
  reg/succ/ctrl writes — measured at the move tick, where both arms are alive and differ only by the
  one-time withholding. The end-of-run production gap is the *survival* effect (dying seeds stop
  maintaining), not the withholding. Reported per individual, not gated.
- **Survival is a bimodality-aware lower bound** (AC68). The reserve arm's survival is reported per
  distinct seed as a lower bound on the true rate — 4 surviving seeds do not guarantee every seed
  survives, and the no-reserve control's deaths are the material-starve / attention-hijack cascade.
- **The reserve is a fixed minimum reserve, not an acquired allocation decision.** `RESERVE_LEVEL = 21`
  is a declared world constant sized to the drop (7) + reset (14), and the release trigger is the fixed
  "material < 21" shortfall test. Whether the organism *acquires* how much to save is a separate, still-
  open question (AC96-D4's open item, one level up). This study establishes affordability, not an
  acquired allocation policy.
- **Priorities.** The final family's acquired priorities are reported in the results doc, not prespecified
  (unseen seeds). The relinquishment is a streak/register decision, not a renewal-contention decision, so
  the priority ordering does not confound the mechanism.
- **Supplied machinery remains.** `advance()` (the transition logic) and `prog.choose` (the interpreter)
  are still host-supplied format-level machinery. Affordability is about whether the internalized
  decision is *payable*, not about internalizing the transition logic — that boundary is unchanged from
  AC90/AC96.

## Anti-drift rules

- The runner creates `ac97_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed set
  (which includes this protocol file).
- `test_ac97.py`, `audit_ac97.py`, `replay_ac97.py` are NOT hashed into the frozen snapshot (AC17's rule).
- Engineering seeds (0-7, 4412-4431) are excluded from the final sample and are disjoint from the final
  family.
- The equivalence (declared, verified before finals): `ac97.run(..., reserve=False)` reproduces
  `ac96.run(..., streak_maintained=True)` byte-for-byte (state_hash) in the perm world — proving the
  runner is a correct extension and the reserve is the only change.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.

## Source hashes (computed before the first final seed)

    (recorded in ac97_results_v1/pre_run_snapshot.json at freeze time)
