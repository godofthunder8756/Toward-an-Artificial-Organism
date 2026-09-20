# AC99 protocol v1: cheaper transitions (Gray-coded streak) under the standing gates, on unseen seeds

STATUS: **frozen before the first final seed.** Written 2026-09-19. This is the protocol + finals for
AC99-D4, the last step of the AC99 line. AC98 froze the revised material reserve under an unconditional
adaptation criterion plus a no-harm gate and was **falsified on G1**: the revised reserve causes no
survival reversal in that cohort (G2 passed) but still dies on seed 4436, where the binary streak's 3→4
increment (3 bits = 21 replicas, needs W ≥ 3) stalls in a W-death window and the drop never fires. AC99
reframed that failure: the W ≥ 3 requirement is a property of the *binary counter's encoding*, not an
established minimum cost of remembering another failed contact. The four steps: AC99-D1 fixed the
release/disarm atomicity defect (`ac99.py`); AC99-D2 showed a 3-bit reflected-Gray counter makes every
increment 1 bit = 7 replicas (W ≥ 1) and flips 4436 death→relinquish+survive; AC99-D3 built a paid
W-birth-priority rival that keeps W ≥ 3 and also rescues 4436, proving the stall is a *conjunction* of an
expensive increment and a starved W population — **the two fixes are alternatives, not complements**. This
protocol freezes the chosen architecture — the **Gray-coded streak** (the "cheaper transition" premise of
AC99) — under the **standing gates unchanged**, on **unseen** seeds.

SOURCES (declared): ac99_d4.py ac99_d3.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC99_PROTOCOL_v1.md

## The question and the claim

AC98 answered the affordability question negatively *for a material reserve*, and located the residue as a
*W*-denominated shortfall: the binary 3→4 increment needs W ≥ 3, and a one-shot material release cannot
hold W ≥ 3 through the W-death window. AC99 asks the follow-up AC98's result named: can the
maintenance/adaptation conflict be resolved *within the existing organization* by making the decision-state
transitions cheaper, rather than by adding another reserve? The claim is that the Gray-coded streak — which
changes the *encoding* of the relinquishment counter, not the reserve policy — affords self-preservation
through the route move on unseen seeds, under the same standing gates that AC98 froze.

The four measures, recorded for every individual of the success arm (and the binary control, for the
no-harm comparison):

1. **relinquishment** — the stale route (key 1, moved at t=8192) is dropped: the streak reaches the
   threshold and `_drop` fires, the register bit reads set (majority True), and the entry is erased.
2. **reacquisition** — the moved key is re-bound after the drop (a None→bound transition on key 1 at a
   tick strictly after the drop tick).
3. **continued machinery production** — W, C, and B births each continue after the move (each class has
   ≥ 1 birth in the post-move window `t >= MOVE_TICK`).
4. **survival** — `completed` (the organism survives to the horizon).

The gates (prespecified, categorical per distinct seed; the two histories are a repeated measure):

1. **G1 unconditional adaptation** (AC97/98's criterion, kept). Every final distinct seed: the **Gray**
   success arm satisfies all four measures (A1 relinquishment, A2 reacquisition, A3 continued machinery
   production, A4 survival), with NO external rescue. Stated per distinct seed (4 seeds); the two histories
   are a repeated measure and are verified identical per seed (state_hash equality), then counted once.
2. **G2 no-harm** (the AC98 gate, applied to the new comparison). No distinct final seed where the
   **binary control** survives and the **Gray** success arm dies. Formally, for every distinct seed s:
   `not (binary[s] survives AND gray[s] dies)`. The binary control is the AC98/AC99 revised-reserve
   architecture (binary streak + reserve, the D1 atomicity fix) — the direct predecessor, from which the
   Gray arm differs only in the streak's encoding. The reverse direction — the Gray arm survives where the
   binary control dies — is the *load-bearing* direction and is carried by G1, not by a positive-only
   contrast (AC97's gate-shape lesson).
3. **G3 state sufficiency (per-tick observer-discard), on the success arm.** Every final individual
   (4 seeds × 2 histories): the Gray-arm run with the succession observer AND the alloc (clearing the
   vestigial host streak dict) discarded at a mid-streak tick is **byte-identical at every tick**
   (`per_tick_identical`, the trajectory-level comparison — not the terminal state_hash), non-vacuously
   (`swap_applied`, `streak_at_swap == 2`). The Gray streak and the reserve must be recovered from
   maintained state alone.
4. **G4 endogenous reserve (no external rescue).** Every final Gray individual: the reserve was armed
   from the organism's own income (`reserve_m > 0`) and no more is ever released than was withheld
   (`reserve_released_m <= reserve_m`, net standing ≥ 0). There is **no rescue arm** in the finals; the
   reserved material is the organism's own previously-withheld intake, not an injected resource.
5. **G5 completeness + determinism + arm identity.** Row count == seeds × 2 histories × 3 arms (24); a
   sampled exact rerun of the first row is byte-identical (state_hash); and the `wb_first` rival's no-swap
   path (`wb_first=False`) is byte-identical to the binary control on every final individual — proving the
   priority swap is the *only* change in the rival arm (the Gray arm differs from the binary control only
   in the streak encoding, pinned at the single-step level in `test_ac99_d2.py` and by D2's byte-identity
   checks).

## The mechanism (what changed, and why)

The runner is `ac99_d4.py` (new), which **delegates** to the three verified engineering runners — it does
not re-implement any arm, so each arm is exact (`state_hash`) by construction:

- **`gray`** (the success arm) = `ac99_d2.run(..., reserve=True)`: the 3-bit reflected-Gray streak
  (`g = n ^ (n >> 1)`, decode `g ^ (g>>1) ^ (g>>2)`), where every successive increment changes ONE logical
  bit = 7 replicas (W ≥ 1). The binary 3→4 increment (3 bits = 21 replicas, W ≥ 3) and 1→2 (2 bits = 14,
  W ≥ 2) are both removed. The reserve policy (level 21, drop/stall/wlow triggers, atomic release+disarm
  from D1), the sticky 1e-4 damage, the 7-replica majority read (threshold 4), prices (1 energy + 1
  material per replica), and STREAK_N=6 are all **unchanged from AC99-D1**.
- **`binary`** (the direct control) = `ac99.run(..., reserve=True)`: the binary streak + the same reserve.
  This is the AC98/AC99 architecture (the D1 atomicity fix), the exact architecture that died on AC98's
  4436. The Gray arm differs from it **only** in the counter's encoding.
- **`wb_first`** (the labeled rival, NOT the success arm) = `ac99_d3.run(..., reserve=True,
  wb_first=True)`: the binary streak + the paid W-birth-priority program swap (2 words × 5 logical bits ×
  7 replicas = 70 energy + 70 material, internal, paid over the first few ticks). It rescues 4436 by
  keeping W ≥ 3 rather than by making the increment cheaper — the orthogonal fix D3 triangulated.

Everything else (the AC96 relinquishment world, the AC75 erase-on-relinquish, the order-preserving
generic-over-syntax decoder, the reserve storage at `traces[1, 540]` and its paid majority-restore) is
byte-for-byte the AC99-D1/D2/D3 architecture. The world is the AC96/AC97/AC98 relinquishment world:
`transition='perm'`, PORTS=4, YIELD=64, TICKS=16384, MOVE_TICK=8192, sticky 1e-4 damage on both banks
(independent streams), `corrupt=False` for every condition (the move is the sole event).

## World, arms, seeds

World constants unchanged from AC98/AC97/AC96. PORTS=4, YIELD_M=64, YIELD_F=64, TICKS=16384,
MOVE_TICK=8192, CORRUPT_TICK=8192, sticky 1e-4 damage on both banks (independent streams), STREAK_N=6,
STREAK_THRESHOLD=4, REGISTER_THRESHOLD=4, RESERVE_LEVEL=21, RESERVE_OFFS=540, RESERVE_THRESHOLD=4,
RESERVE_TRIGGER=2, the order-preserving generic-over-syntax decoder, AC75's erase-on-relinquish.
`corrupt=False` for every condition.

Three arms per individual (all `reserve=True`):

- `gray` — `ac99_d2.run(..., reserve=True)` — the success arm / chosen architecture.
- `binary` — `ac99.run(..., reserve=True)` — the direct control (the AC98/AC99 revised-reserve architecture).
- `wb_first` — `ac99_d3.run(..., reserve=True, wb_first=True)` — the labeled rival (not the success arm).

24 rows = 4 seeds × 2 histories × 3 arms. History is a trivial repeated measure (the runner gates
`activation=[True,True]` and the RNG seeds depend on seed, not history), so the two histories are
identical per seed; the criterion is stated per distinct seed, with history identity verified per seed.

Final seeds `4440, 4441, 4442, 4443` (4 seeds × 2 histories = 8 individuals), **unseen**: disjoint from
engineering 0-7, from the D1/D2/D3 engineering seeds (4412-4415, 4436-4439), from the AC96 screening
sweep (4412-4431), from every prior final family ≤ 4439 (AC93 4400-4403, AC94 4404-4407, AC95 4408-4411,
AC96 4412-4415, AC97 4432-4435, AC98 4436-4439), and from the separate 4600-4871 order-line families and
the 5100-5507 confirmatory families. **No screening of this final family** — the gates above were shaped
by the D1/D2/D3 engineering results on the disjoint seeds 4412-4415/4436-4439 (disclosed below), and the
final family itself is untouched.

## Screening disclosed (before this protocol was frozen)

The gate shapes were informed by the AC98-D3 falsification (recorded in `AC98_RESULTS_v1.md`) and the
AC99-D1/D2/D3 engineering runs on the disjoint seeds 4412-4415/4436-4439 (recorded in
`AC99_D1_RESULTS.md`, `AC99_D2_RESULTS.md`, `AC99_D3_RESULTS.md`), not by the final family. Measured there:
the Gray streak flips 4436 death→relinquish+reacquire+survive with no regression on the other seven
engineering seeds (16/16 Gray relinquish + survive, 0/16 regress); the binary control dies on 4436 (the
recorded AC98 G1 failure, reproduced byte-for-byte); the `wb_first` rival also flips 4436 (via a different
path, keeping W ≥ 3) but weakens the *active* relinquishment on 4438 (0 drops; the stale entry lapses by
natural expiry) — a labeled cost, not a survival regression; per-tick observer-discard is byte-identical
on every Gray individual. Consequences, all reflected in the gate shapes above: G1 is the success arm's
own per-individual criterion (not a margin over a rival — AC16/17/18); G2 is the no-harm direction against
the binary predecessor (the direction AC97 missed and AC98 added); G3 is the trajectory-level discard on
the success arm; G4 is the endogeneity invariant; the maintenance trade-off and the rival's costs are
reported, not gated. A family where the Gray arm fails to relinquish on a seed (like AC98's 4436 residual
recurring) would fail G1; a family where the binary control survives and the Gray arm dies would fail G2 —
both are the honest possibilities and neither is pre-smoothed.

## Gates (prespecified, categorical per distinct seed)

- **G1 (unconditional adaptation).** For every distinct final seed, the **gray** arm satisfies A1
  (`relinquishments >= 1`, a drop tick with the register bit set), A2 (`reacquire_ticks[1]` non-empty and
  its first tick > the first drop tick), A3 (`W_births_post_move > 0` and `C_births_post_move > 0` and
  `B_births_post_move > 0`), and A4 (`completed`). Both histories must satisfy it (identity verified per
  seed). No external rescue.
- **G2 (no-harm).** For every distinct final seed s: `not (binary[s] survives AND gray[s] dies)`, where
  "survives" = the arm is `completed` and "dies" = the arm is not `completed`. Stated per distinct seed.
- **G3 (state sufficiency, per-tick observer-discard, on the gray arm).** Every individual:
  `status != 'no_mid_streak'`, `swap_applied`, `streak_at_swap == 2`, and `per_tick_identical`
  (byte-identical at every one of 16,384 ticks — trajectory-level, not endpoint-level).
- **G4 (endogenous reserve).** Every gray individual: `reserve_m > 0` and `reserve_released_m <=
  reserve_m`. No rescue arm in the finals.
- **G5 (completeness + determinism + arm identity).** 24 rows; sampled rerun of rows[0] byte-identical;
  the `wb_first` rival's no-swap path (`wb_first=False`) byte-identical to the binary control on all 8
  final individuals (the priority swap is the only change in the rival arm).

## Reported, not gated

- **The maintenance trade-off.** The reserve withholds 21 (or 42, if re-armed) and releases 21; its paid
  arm/disarm/repair writes cost a small fraction of the paid bank-1 repair writes in the same run. Under
  the Gray streak the reserve's release triggers become near-redundant on the seeds where the 1-bit
  increments never stall (D2's finding: on 4438/4412-4415 the reserve arms once and never releases — the
  decision is funded by the cheaper writes, not the reserve). Reported per individual, not gated.
- **The Gray reset is dearer.** Gray 5→0 reset is 3 bits = 21 replicas vs binary 2 bits = 14, so
  drop (7) + reset (21) = 28 now exceeds the fixed `RESERVE_LEVEL = 21` (binary's 7 + 14 = 21 exactly
  filled it). The reset self-heals on the post-re-acquisition productive contact (D2 verified
  `streak_final == 0`), but the reserve no longer *fully* funds the drop+reset under Gray. Reported, not
  gated (holding `RESERVE_LEVEL = 21` fixed was the AC99 premise).
- **The Gray damage mode is a trade.** Sticky-SET damage on a Gray counter can *decrease* the count (erase
  streak progress) and jump ±1/±3/±5/±7, where binary sticky damage only ever increases. At the frozen
  1e-4/replica/tick rate the sub-majority damage is rare (AC67), but it is the failure mode to watch if
  the damage rate is raised. Reported, not gated.
- **The rival's cost.** The `wb_first` swap costs 70 energy + 70 material (paid over the first few ticks),
  and it weakens the *active* relinquishment on seeds where the material contact drives the streak (D3:
  4438 drops 0 under `wb_first` vs 1 under the frozen binary). The rival is labeled, not the success arm;
  its outcome is reported, not gated.
- **Survival is a bimodality-aware lower bound** (AC68). The success arm's survival is reported per
  distinct seed as a lower bound on the true rate — 4 surviving seeds do not guarantee every seed
  survives. The binary control's deaths are the material-starve / attention-hijack cascade.
- **The reserve is still a fixed minimum reserve, not an acquired allocation decision.** The Gray change
  touches the counter's *encoding*, not the reserve policy; `RESERVE_LEVEL = 21` and the
  drop/stall/wlow triggers are declared world constants. Whether the organism *acquires* how much to save
  remains open (AC96-D4's open item).
- **Priorities.** The final family's acquired priorities are reported in the results doc, not prespecified
  (unseen seeds). The relinquishment is a streak/register decision, not a renewal-contention decision, so
  the priority ordering does not confound the mechanism.
- **Supplied machinery remains.** `advance()` (the transition logic) and `prog.choose` (the interpreter)
  are still host-supplied format-level machinery. Affordability — whether the internalized decision is
  *payable* — is the question, not internalizing the transition logic; that boundary is unchanged from
  AC90/AC96.

## Anti-drift rules

- The runner creates `ac99_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed set
  (which includes this protocol file).
- `test_ac99.py`, `audit_ac99.py`, `replay_ac99.py` are NOT hashed into the frozen snapshot (AC17's rule).
- Engineering seeds (0-7, 4412-4439) are excluded from the final sample and are disjoint from the final
  family.
- The arm identity (declared, verified before finals): `ac99_d3.run(..., wb_first=False)` reproduces
  `ac99.run(..., reserve=True)` byte-for-byte (state_hash) in the perm world — proving the runner is a
  correct extension and the priority swap is the only change in the rival arm. The Gray arm differs from
  the binary control only in the streak encoding (pinned in `test_ac99_d2.py`).
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.

## Source hashes (computed before the first final seed)

    (recorded in ac99_results_v1/pre_run_snapshot.json at freeze time)
