# AC99 results v1: cheaper transitions (Gray-coded streak) under the standing gates, on unseen seeds — G1 PASS, all five gates pass

Parent: AC99-D3. Frozen per `AC99_PROTOCOL_v1.md` (hashed before the first final seed). Runner
`ac99_d4.py` (delegating to the verified engineering runners `ac99.py` / `ac99_d2.py` /
`ac99_d3.py`); seeds **4440-4443** × 2 histories, 24 rows, 16,384 ticks, `transition='perm'` (the
relinquishment world). Three arms per individual: `gray` (the SUCCESS arm — the 3-bit reflected-Gray
streak + the AC98/AC99 reserve), `binary` (the DIRECT CONTROL — the binary streak + the same reserve,
i.e. the AC98/AC99 revised-reserve architecture), and `wb_first` (the LABELED RIVAL — the binary
streak + the paid W-birth-priority swap). The final family is **unseen**: no screening, disjoint from
engineering 0-7, the D1/D2/D3 seeds 4412-4415/4436-4439, the AC96 screening sweep 4412-4431, and every
prior final family ≤ 4439.

## Verdict

**The unconditional adaptation criterion (G1) PASSES on the unseen family; all five gates pass.** The
Gray-coded streak — the "cheaper transition" fix, which changes the relinquishment counter's *encoding*
and nothing else — satisfies all four measures (relinquishment, reacquisition, continued W/C/B
production, survival) on **all 4 distinct seeds**, with no external rescue. The binary control dies on
1/4 seeds (4442), so the load-bearing direction is real: the Gray encoding flips a seed that the binary
predecessor architecture (the AC98/AC99 revised reserve) cannot survive. The no-harm gate passes (no
seed where the binary control survives and the Gray arm dies).

The labeled `wb_first` rival resolves D3's open question in the **negative**: it dies on 1/4 seeds
(4441, at t=5501, *before* the move), where both the Gray arm and the binary control survive. The
priority swap is the only change in that arm (G5 arm identity: `wb_first=False` is byte-identical to the
binary control), so the pre-move death is the priority change's own cost. The cheaper *transition*
(Gray encoding) is the correct fix; the priority *reorder* is not a safe alternative.

In one sentence: within the existing organization, making the relinquishment decision's transitions
cheaper (a Gray-coded counter) resolves the W-bound stall that AC98's binary streak could not, on unseen
seeds — while the orthogonal fix (reordering the program to prioritize W-birth) trades that rescue for a
new pre-move death on another seed.

## Per-seed outcome (both histories identical)

| seed | priority    | gray (success arm)                    | binary (control)                  | wb_first (labeled rival)              |
|------|-------------|---------------------------------------|-----------------------------------|---------------------------------------|
| 4440 | `[2,3,0,1]` | drop@8199, reacq@8200, survive        | drop@8199, reacq@8200, survive    | 0 drops, reacq@8289, survive          |
| 4441 | `[1,3,2,0]` | drop@8226, reacq@8227, survive        | drop@8226, reacq@8227, survive    | **dies 5501 (pre-move)**              |
| 4442 | `[1,3,2,0]` | drop@8234, reacq@8235, survive        | **dies 8442 (streak stuck 5)**    | drop@8223, reacq@8226, survive        |
| 4443 | `[2,3,1,0]` | drop@8220, reacq@8224, survive        | drop@8221, reacq@8224, survive    | 0 drops, reacq@8265, survive          |

- **Gray arm:** 4/4 distinct seeds relinquish + reacquire + continue W/C/B production + survive.
- **Binary control:** 3/4 survive + relinquish; 1/4 dies (4442, streak stuck at 5, the AC96 economic
  failure mode).
- **wb_first rival:** 1/4 dies pre-move (4441); 1/4 relinquishes + survives (4442); 2/4 survive WITHOUT
  an active drop (4440, 4443 — the stale entry lapses by natural expiry, D3's 4438 pattern).
- The load-bearing direction (Gray survives/relinquishes where the binary control dies) holds on 4442.

## The mechanism (the honest new findings)

**4442 is the binary streak's economic failure recurring on an unseen seed, and Gray flips it.** On 4442
(`priority [1,3,2,0]`) the binary control reaches streak 5 but the drop's register write is starved by
the move's income collapse (the AC96 finding: the paid increment is starved by the very income collapse
the decision exists to pre-empt), and the organism dies at 8442 with W=0, C=0, streak stuck at 5, zero
post-move W births. The Gray arm builds the streak with 1-bit increments (7 replicas each, W ≥ 1 instead
of W ≥ 3), the drop fires at 8234 funded by the reserve's `drop` release, and the organism re-acquires
and survives. The 3→4 W-bound stall that kills AC98's 4436 (the 21-replica increment refused at W < 3)
was established in the engineering runs (D2/D3 on 4436). The final 4442 failure is the broader economic
stall — the binary streak reaches 5 but cannot afford the paid relinquishment — so Gray's benefit on the
finals is broader affordability (cheaper increments throughout plus a funded drop), not another direct
demonstration of the 3→4 increment.

**The wb_first rival is not a safe alternative — it kills 4441 pre-move.** On 4441 the rival dies at
t=5501, well before the move (t=8192), with W=0, C=0, material=0, energy drained to 0, fuel 44 residual
(the W/C collapse with exhausted material). The priority swap is the only change in the arm (G5: the
`wb_first=False` path is byte-identical to the binary control), so the reorder itself causes the
pre-move death — where both the Gray arm and the binary control survive. D3's engineering found "0/4
regressions" on 4436-4439; that did not transfer to the unseen family (AC39). The two fixes are
alternatives, and they are not symmetric: the Gray encoding changes only how the counter counts (it
never reorders the program), but it is not guaranteed harmless before the move — it changes write costs,
reset costs, and responses to damage wherever the counter operates, so no "cannot cause a pre-move death"
claim is made (no Gray arm died pre-move in this cohort, but that is an observation, not a guarantee).
The priority reorder changes the whole development trajectory from t=0 and can (and here did, on 4441).

**The reserve's release triggers fire less often where the increments are cheap, but redundancy is not
shown.** On 4440 and 4441 the Gray arm arms the reserve once (`reserve_m = 21`) and never releases it
(`reserve_released_m = 0`): the 1-bit increments never stall, so on those two seeds the decision is
funded by the cheaper writes. On 4442 (drop release) and 4443 (stall release) the reserve arms twice and
releases once. The reserve is armed in **every** final Gray run and released on 2/4 seeds, so it has not
been shown redundant — that requires a Gray-without-reserve comparison, carried by the AC100 consolidation
study. The encoding reduces how often the release triggers fire; it does not by itself show the reserve
is dispensible.

## Gates (prespecified in the protocol)

- **G1 unconditional adaptation — PASS 4/4.** Every distinct seed's Gray arm satisfies A1
  (`relinquishments >= 1`, a drop tick with the register bit set), A2 (`reacquire_ticks[1]` non-empty
  and after the drop), A3 (W/C/B births all > 0 post-move), and A4 (`completed`). No external rescue.
- **G2 no-harm — PASS 4/4.** No distinct seed where the binary control survives and the Gray arm dies.
  On 4442 the control dies and Gray survives (the load-bearing direction, carried by G1); on 4440/4441/
  4443 both survive.
- **G3 state sufficiency (per-tick observer-discard, on the Gray arm) — PASS 8/8.** The Gray-arm run with
  the succession observer + host streak dict discarded at a mid-streak tick is byte-identical at every one
  of 16,384 ticks (`per_tick_identical`, `swap_applied`, `streak_at_swap == 2` on all 8 individuals). The
  Gray streak and the reserve are recovered from maintained state alone; the encoding change does not
  reintroduce any host-side operational memory.
- **G4 endogenous reserve (no external rescue) — PASS.** Every Gray individual: `reserve_m > 0` and
  `reserve_released_m <= reserve_m` (never release more than withheld; the reserved material is the
  organism's own withheld intake).
- **G5 completeness + determinism + arm identity — PASS.** 24 rows; sampled rerun of rows[0]
  byte-identical; the `wb_first` rival's no-swap path is byte-identical to the binary control on all 8
  individuals — the priority swap is the only change in the rival arm.

## Reported, not gated

- **The maintenance trade-off.** Per individual the reserve withholds 21 (4440/4441) or 42
  (4442/4443) and releases 0 or 21; its paid arm/disarm/repair writes cost a small fraction of the paid
  bank-1 repair writes in the same run. Under the Gray streak the release triggers fire only on the seeds
  where the increments stall (4442's drop, 4443's stall) — on 4440/4441 the reserve is armed and never
  released (D2's finding, now observed on unseen seeds).
- **The Gray reset is dearer (unfunded by the fixed reserve).** Gray 5→0 reset is 3 bits = 21 replicas vs
  binary 2 bits = 14, so drop (7) + reset (21) = 28 exceeds `RESERVE_LEVEL = 21`. The reset self-heals on
  the post-re-acquisition productive contact (`streak_final == 0` on every Gray individual), but the
  reserve no longer *fully* funds the drop+reset under Gray. Holding `RESERVE_LEVEL = 21` fixed was the
  AC99 premise; re-deriving it for the 28-replica drop+reset is left to a later study.
- **The Gray damage mode is a trade.** Sticky-SET damage on a Gray counter can *decrease* the count
  (erase progress) and jump ±1/±3/±5/±7, where binary sticky damage only ever increases. At the frozen
  1e-4/replica/tick rate the sub-majority damage is rare (AC67), so it did not fire here; it is the
  failure mode to watch if the damage rate is raised.
- **The rival's cost.** The `wb_first` swap costs 70 energy + 70 material (paid over the first few ticks,
  `priority_writes = 70` on every rival individual), and it causes a pre-move death on 4441 and weakens
  the active relinquishment on 4440/4443 (0 drops; the stale entry lapses by natural expiry). The rival
  is labeled, not the success arm; these outcomes are reported, not gated.
- **Survival is a bimodality-aware lower bound** (AC68). The Gray arm's 4/4 survival is an observed
  fraction on this cohort, not a statistical lower bound on the true rate. The binary control's 4442
  death is the material-starve / economic-stall cascade.
- **The reserve is still a fixed minimum reserve, not an acquired allocation decision.** The Gray change
  touches the counter's *encoding*, not the reserve policy. Whether the organism *acquires* how much to
  save remains open (AC96-D4's open item).
- **Priorities.** 4440 `[2,3,0,1]`, 4441 `[1,3,2,0]`, 4442 `[1,3,2,0]`, 4443 `[2,3,1,0]` — none is
  AC83's adversarial `[3,0,2,1]`, and none is AC98's 4436 priority `[1,3,0,2]`. The relinquishment is a
  streak/register decision, not a renewal-contention decision, so the priority ordering does not confound
  the mechanism.
- **Supplied machinery remains.** `advance()` and `prog.choose` are still host-supplied format-level
  machinery; no autopoiesis claim. Affordability is the question, and the answer is: the cheaper
  transition (a Gray-coded counter) makes the internalized relinquishment decision *payable* on unseen
  seeds, within the existing organization.

## Verification

- `audit_ac99.py` passes: 24 rows, 20 hashes no drift, arm invariants (Gray adaptation 4/4; binary
  control death 8442 on 4442; wb_first death 5501 on 4441; the no-harm direction), observer-discard
  record 8/8 per-tick, arm-identity record 8/8, gates re-derived WITHOUT simulating and matching the
  recorded result.
- `replay_ac99.py` passes: 3/3 exact (state_hash + endpoint fields, one per arm), observer-discard 1/1
  per-tick byte-identical, arm-identity 1/1.
- `test_ac99.py` 20/20 green: single-step release atomicity (D1), Gray code cost/damage (round-trip, the
  3→4 one-bit transition, the dearer reset, the damage-decrease trade), the D4 finals recorded-outcome
  regressions (G1 pass; binary dies 4442 streak 5; wb_first dies 4441 pre-move; no-harm), per-tick
  discard on the Gray arm, seed-disjointness, and the recorded gates.
- `test_ac99_d2.py` 10/10, `test_ac99_d3.py` 10/10, core AC1-9 suite 56/56 — all green.
- No frozen runner modified: `ac98.py` sha256 `1ae3d373…` unchanged; `ac97.py`, `ac96.py` and every
  earlier freeze untouched; `audit_ac98.py` still passes (the AC98 architecture is the direct control,
  reproduced byte-for-byte as the `binary` arm).

## Boundary and next step

The internally maintained organization now **affords self-preservation through the move under the
unconditional criterion**, by making the relinquishment decision's transitions cheaper — a Gray-coded
counter that removes the W ≥ 3 requirement on the 3→4 increment. The conflict AC97/AC98 measured (a
fixed *material* reserve cannot answer a *W*-denominated shortfall) is resolved **within the existing
organization**, not by adding another reserve: the fix is the decision state's *encoding*. The labeled
W-birth-priority rival shows the orthogonal fix is real but costly — it trades the rescue for a new
pre-move death on a different seed, so it is not the architecture.

The boundary is unchanged: `advance()` and `prog.choose` are still supplied format-level machinery, no
autopoiesis claim, the reserve is a fixed minimum reserve (not an acquired allocation), and the Gray
reset's 28-replica drop+reset exceeds the fixed `RESERVE_LEVEL = 21` (reported, not gated). The next open
items are the ones AC96-D4 already named — whether the organism *acquires* how much to save (an acquired
allocation policy), and whether the reserve level should be re-derived for the Gray reset width — none of
which changes the standing boundary. All earlier results (ac98_results_v1, ac99_d1/d2/d3_engineering_v1,
and every prior freeze) are preserved untouched.
