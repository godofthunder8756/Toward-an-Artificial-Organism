# AC98 protocol v1: an unconditional adaptation criterion PLUS a no-harm gate, on unseen seeds

STATUS: **frozen before the first final seed.** Written 2026-09-19. This is the protocol + finals for
AC98-D3, the last step of the AC98 affordability line. AC97 froze an unconditional adaptation criterion
on unseen seeds and was **falsified**: the fixed internal reserve (release gated on `_drop` only) moved the
maintained arm from 2/8 to 8/8 relinquish+survive on the D1-named seeds 4412-4415, but on the unseen
family 4432-4435 the reserve arm satisfied the criterion on 2/4 seeds and **died on 2/4 (4434, 4435)
where the no-reserve control survives** — the reserve's one-time 21-unit withholding (armed ~7660 ticks
before the move) stalled the streak's own paid buildup below the drop threshold, so the drop never fired
and the withholding became a permanent loss. AC98-D1 located the two corrected mechanisms (4434: the 4→5
increment starved by 1 material unit; 4435: the 3→4 increment W-bound after a phase-shifted build) and
designed the revised reserve; AC98-D2 implemented it (`ac98.py`) and verified in engineering that the
revised release gate flips 4434/4435 and does no harm. This protocol freezes the claim on **unseen**
seeds, under **two** prespecified gates: the unconditional adaptation criterion (kept) AND a **no-harm
gate** (new) — the gate AC97's positive-only load-bearing contrast missed, and the gate that would have
caught AC97's failure.

SOURCES (declared): ac98.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC98_PROTOCOL_v1.md

## The question and the claim

AC97 answered the affordability question **negatively** for a fixed reserve whose release was gated on the
very decision it funds. AC98 asks the follow-up the AC97 result named: can a reserve whose withholding
**cannot starve the decision it funds** afford self-preservation through the route move? The claim is
that it can — the revised reserve (release on drop OR streak-stall OR W-low, all read from maintained
organism state) funds the relinquishment when it fires and **returns the withheld material the moment
continuing to withhold would starve the buildup or the repair catalyst**, so the withholding is never a
permanent loss and never tips the organism into the death cascade. The decisive test is the same
**unconditional adaptation criterion** as AC97 (kept), plus a new **no-harm gate** that pins the direction
AC97 missed.

The four measures, recorded for every individual of both arms:

1. **relinquishment** — the stale route (key 1, moved at t=8192) is dropped: the streak reaches the
   threshold and `_drop` fires, the register bit reads set (majority True), and the entry is erased.
2. **reacquisition** — the moved key is re-bound after the drop (a None→bound transition on key 1 at a
   tick strictly after the drop tick).
3. **continued machinery production** — W, C, and B births each continue after the move (each class has
   ≥ 1 birth in the post-move window `t >= MOVE_TICK`).
4. **survival** — `completed` (the organism survives to the horizon).

The gates (prespecified, categorical per distinct seed; the two histories are a repeated measure):

1. **G1 unconditional adaptation** (AC97's criterion, kept). Every final distinct seed: the reserve arm
   satisfies all four measures (A1 relinquishment, A2 reacquisition, A3 continued machinery production,
   A4 survival), with NO external rescue. Stated per distinct seed (4 seeds); the two histories are a
   repeated measure and are verified identical per seed (state_hash equality), then counted once.
2. **G2 no-harm** (new, from AC97's gate-shape lesson). No distinct final seed where the no-reserve
   control survives and the reserve arm dies. Formally, for every distinct seed s:
   `not (no_reserve[s] survives AND reserve[s] dies)`. This is the direction AC97's "load-bearing
   contrast" never checked, and it is the gate that would have caught the AC97 failure (4434/4435: the
   control survives, the reserve dies). The reverse direction — the reserve survives where the control
   dies — is the *load-bearing* direction and is carried by G1 (the reserve must satisfy the four measures
   on every seed) rather than by a positive-only contrast.
3. **G3 state sufficiency (per-tick observer-discard).** Every final individual (4 seeds × 2 histories):
   the reserve-arm run with the succession observer AND the alloc (clearing the vestigial host streak
   dict) discarded at a mid-streak tick is **byte-identical at every tick** (`per_tick_identical`, the
   trajectory-level comparison — not the terminal state_hash), non-vacuously (`swap_applied`,
   `streak_at_swap == 2`). The three release conditions read organism state only, so the discard must
   change nothing.
4. **G4 endogenous reserve (no external rescue).** Every final reserve individual: the reserve was armed
   from the organism's own income (`reserve_m > 0`) and no more is ever released than was withheld
   (`reserve_released_m <= reserve_m`, net standing ≥ 0). There is **no rescue arm** in the finals; the
   reserved material is the organism's own previously-withheld intake, not an injected resource.
5. **G5 completeness + determinism + control equivalence.** Row count == seeds × 2 histories × 2 arms
   (16); a sampled exact rerun of the first row is byte-identical (state_hash); and the no-reserve
   control is byte-identical to `ac97.run(..., reserve=False)` on every final individual — the revised
   reserve is the only change from the AC97 architecture.

## The mechanism (what changed, and why)

The runner is `ac98.py` (new, from AC98-D2); `ac97.py` and every earlier freeze are untouched. The change
from AC97 is exactly one: the reserve's release gate is broadened from drop-only to three
release-on-maintained-state triggers, evaluated in this order:

1. **`drop`** (unchanged from AC97): inside `_drop`, when `material < RESERVE_LEVEL`, before the cap check.
   Funds the drop register write (7) and the streak reset (14) at the moment they are refused by the
   income collapse.
2. **`stall`** (the revision): a streak increment is refused (`ac96.streak_write` returns 0 in the
   `cur → cur+1` branch — reached only when `cur+1 < STREAK_N`, and `new = cur+1 != cur` so 0 means the
   write was refused). Returns the 21 units so the increment and the subsequent drop are funded. This is
   the direct fix for AC97 seed 4434 (the 4→5 increment starved by 1 material unit at M=6).
3. **`wlow`** (survival): on a key-1 contact when `available_W < 3` and `material <= 64`. Releasing the 21
   units lifts material above 64, clearing observation bit 1, so the frozen priority order runs the W-birth
   rule (action 6) instead of the stale material contact (action 1) and W recovers before the death cascade.
   This stops AC97 seed 4435 from *dying*; it does not (cannot) make 4435's 3→4 increment succeed, because
   that increment is W-bound (a phase-shift limit, recorded below as a scope note).

Arming (first productive material contact at `t >= DEV`, withhold `RESERVE_LEVEL = 21` from intake), the
level (21 = drop 7 + reset 14), storage (`traces[1, RESERVE_OFFS = 540]`, majority-read, damaged by the
bank-1 sticky stream, repaired by a paid majority-restore on minority >= RESERVE_TRIGGER = 2), and the
paid W-gated atomic arm/release writes are all **unchanged from AC97**. The two new release paths read
organism state only (`o.body.material`, `ac4.available(o.body)`, the maintained streak) and write
`traces[1, 540]` plus the material ledger — no host-side flag, so the per-tick observer-discard (G3)
still applies. The no-reserve control (`reserve=False`) is byte-identical to `ac97.run(..., reserve=False)`
because the stall/wlow paths are gated on `self.reserve` and never disturb the rng stream or the frozen
write order when the reserve is disabled.

## World, arms, seeds

World constants unchanged from AC97/AC96, `transition='perm'` (the relinquishment world). PORTS=4,
YIELD=64, TICKS=16384, CORRUPT_TICK=8192, MOVE_TICK=8192, sticky 1e-4 damage on both banks (independent
streams), STREAK_N=6, STREAK_THRESHOLD=4, REGISTER_THRESHOLD=4, RESERVE_LEVEL=21, RESERVE_OFFS=540,
RESERVE_THRESHOLD=4, RESERVE_TRIGGER=2, the order-preserving generic-over-syntax decoder, AC75's
erase-on-relinquish. `corrupt=False` for every condition (the move is the sole event; corruption at
t=8192 would be a second, unrelated challenge).

Two arms per individual:

- `reserve` — `reserve=True`, `damage=True` (the arm under test: the revised reserve).
- `no_reserve` — `reserve=False`, `damage=True` (the direct control: the AC97 no-reserve architecture,
  byte-identical to `ac97.run(..., reserve=False)`).

16 rows = 4 seeds × 2 histories × 2 arms. History is a trivial repeated measure (the runner gates
`activation=[True,True]` and the RNG seeds depend on seed, not history), so the two histories are
identical per seed; the criterion is stated per distinct seed, with history identity verified per seed.

Final seeds `4436, 4437, 4438, 4439` (4 seeds × 2 histories = 8 individuals), **unseen**: disjoint from
engineering 0-7, from the D1/D2 engineering seeds (4412-4415), from the AC96 screening sweep (4412-4431),
from every prior final family ≤ 4435 (AC93 4400-4403, AC94 4404-4407, AC95 4408-4411, AC96 4412-4415,
AC97 4432-4435), and from the separate 4600-4871 order-line families and the 5100-5507 confirmatory
families. **No screening of this final family** — the gates above were shaped by the D2 engineering result
on the disjoint seeds 4432-4435/4412-4415 (disclosed below), and the final family itself is untouched.

## Screening disclosed (before this protocol was frozen)

The gate shapes were informed by the AC97-D3 falsification (recorded in `AC97_RESULTS_v1.md`) and the
AC98-D2 engineering run on the disjoint seeds 4432-4435/4412-4415 (recorded in `AC98_D2_RESULTS.md`),
not by the final family. Measured there: the revised reserve flips 4434 death→relinquish+reacquire+survive
(via the stall release) and 4435 death→survive-without-relinquishment (the honest residual); no regression
on 4432/4433/4412-4415; no-harm 16/16; no-reserve control byte-identical to `ac97.run(..., reserve=False)`
16/16; per-tick observer-discard identical 16/16. Consequences, all reflected in the gate shapes above: G1
is the reserve arm's own per-individual criterion (not a margin over the rival — AC16/17/18); G2 is the
no-harm direction per distinct seed (the contrast AC97 missed); G4 is the endogeneity invariant (there is
no external rescue in the success arm); the maintenance trade-off is reported, not gated. A family where
the reserve arm fails to relinquish on a seed (like the 4435 residual) would fail G1; a family where the
no-reserve control survives and the reserve arm dies would fail G2 — both are the honest possibilities and
neither is pre-smoothed.

## Gates (prespecified, categorical per distinct seed)

- **G1 (unconditional adaptation).** For every distinct final seed, the reserve arm satisfies A1
  (`relinquishments >= 1`, a drop tick with the register bit set), A2 (`reacquire_ticks[1]` non-empty and
  its first tick > the first drop tick), A3 (`W_births_post_move > 0` and `C_births_post_move > 0` and
  `B_births_post_move > 0`), and A4 (`completed`). Both histories must satisfy it (identity verified per
  seed). No external rescue.
- **G2 (no-harm).** For every distinct final seed s: `not (no_reserve[s] survives AND reserve[s] dies)`,
  where "survives" = the arm is `completed` and "dies" = the arm is not `completed`. Stated per distinct
  seed (the two histories are a repeated measure).
- **G3 (state sufficiency, per-tick observer-discard).** Every individual: `status != 'no_mid_streak'`,
  `swap_applied`, `streak_at_swap == 2`, and `per_tick_identical` (byte-identical at every one of 16,384
  ticks — trajectory-level, not endpoint-level).
- **G4 (endogenous reserve).** Every reserve individual: `reserve_m > 0` and `reserve_released_m <=
  reserve_m`. No rescue arm in the finals.
- **G5 (completeness + determinism + control equivalence).** 16 rows; sampled rerun of rows[0]
  byte-identical; no-reserve control byte-identical to `ac97.run(..., reserve=False)` on all 8 final
  individuals.

## Reported, not gated

- **The maintenance trade-off.** The one-time 21-unit withholding (plus one or two re-arms after
  re-acquisition) and its ~20-35 reserve-write units are a small fraction of the ~2290-2430 paid bank-1
  repair writes in the same run. The trade-off is **seed-dependent** (AC97's lesson): benign when the drop
  fires, and under the revised release gate the withholding is returned the moment it would otherwise
  starve the buildup (`stall`) or the repair catalyst (`wlow`), so it is never a permanent loss. Reported
  per individual, not gated.
- **Survival is a bimodality-aware lower bound** (AC68). The reserve arm's survival is reported per
  distinct seed as a lower bound on the true rate — 4 surviving seeds do not guarantee every seed
  survives. The no-reserve control's deaths are the material-starve / attention-hijack cascade.
- **The reserve is a fixed minimum reserve, not an acquired allocation decision.** `RESERVE_LEVEL = 21` is
  a declared world constant sized to the drop (7) + reset (14), and the release triggers are fixed tests
  (`drop`/`stall`/`wlow`). Whether the organism *acquires* how much to save is a separate, still-open
  question (AC96-D4's open item, one level up). This study establishes affordability, not an acquired
  allocation policy.
- **The 4435 residual may recur.** On the engineering family, 4435 survives but does **not** relinquish:
  its 3→4 increment is W-bound, and a one-shot material release cannot hold W ≥ 3 through the repeated
  W-death window. A final seed with the same W-bound phase-shift would survive but fail A1 (and therefore
  G1) — that is an honest falsification of the *unconditional* criterion, not a release-timing bug, and is
  recorded as such rather than hidden.
- **Priorities.** The final family's acquired priorities are reported in the results doc, not prespecified
  (unseen seeds). The relinquishment is a streak/register decision, not a renewal-contention decision, so
  the priority ordering does not confound the mechanism.
- **Supplied machinery remains.** `advance()` (the transition logic) and `prog.choose` (the interpreter)
  are still host-supplied format-level machinery. Affordability is about whether the internalized decision
  is *payable*, not about internalizing the transition logic — that boundary is unchanged from AC90/AC96.

## Anti-drift rules

- The runner creates `ac98_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed set
  (which includes this protocol file).
- `test_ac98.py`, `audit_ac98.py`, `replay_ac98.py` are NOT hashed into the frozen snapshot (AC17's rule).
- Engineering seeds (0-7, 4412-4435) are excluded from the final sample and are disjoint from the final
  family.
- The equivalence (declared, verified before finals): `ac98.run(..., reserve=False)` reproduces
  `ac97.run(..., reserve=False)` byte-for-byte (state_hash) in the perm world — proving the runner is a
  correct extension and the revised reserve is the only change.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.

## Source hashes (computed before the first final seed)

    (recorded in ac98_results_v1/pre_run_snapshot.json at freeze time)
