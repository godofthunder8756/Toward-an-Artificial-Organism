# AC100 results v1: consolidation — the Gray encoding, not the reserve, carries AC99's success; all six gates pass on unseen seeds

Parent: AC99. Frozen per `AC100_PROTOCOL_v1.md` (hashed before the first final seed). Runner
`ac100.py` (a schedule-based extension of the verified `ac99.py` / `ac99_d2.py` arms); seeds
**4444-4447** × 2 histories, 32 rows, 16,384 ticks, repeated route changes (channel-1 port flips
at t=8192 and flips back at t=12288). Four arms per individual — the 2×2 factorial
{binary, gray} streak × {no-reserve, reserve}: `bin_ctl`, `bin_res`, `gray_ctl`, `gray_res`. The
final family is **unseen**: disjoint from engineering 0-7, the D1/D2/D3 seeds 4412-4415/4436-4439,
the AC96 screening sweep 4412-4431, and every prior final family ≤ 4443.

**Headline:** Gray encoding without a reserve supports active adaptation through two route
reversals on four unseen seeds. The reserve is unnecessary on this cohort; one of eight engineering
seeds exhibits a reserve-associated survival reversal.

## Verdict

**All six gates pass.** The consolidation answer is clean: **AC99's success does NOT depend on the
reserve — it depends on the Gray encoding.** On the unseen cohort both `gray_ctl` (Gray, no
reserve) and `bin_res` (binary + reserve) satisfy the full per-move adaptation criterion (relinquish
+ re-acquire after every move + continued W/C/B production + survive) on **all 4 distinct seeds**,
with no external rescue. The 2×2 therefore establishes **two successful alternatives** on this
cohort: binary+reserve and Gray-no-reserve — so the reserve is *unnecessary for Gray on the tested
cohorts* (Q1, answered in the negative), not *necessary* for Gray. The Gray encoding *generalizes*
(Q2): it survives the seed (4446) where the binary-no-reserve arm dies, and no-harm holds in both
directions (G2, G3 pass). The acquired function is *sustainable across two route changes* (Q3): the
dearer 28-replica Gray reset does not compound under the two moves. Only `bin_ctl` (binary, no
reserve) — which relies on natural expiry (0-1 drops) — dies on 4446.

The one caveat, reported not gated: the engineering cohort (seeds 0-7) contained a seed (7) where
the Gray+reserve *combination* dies at t=12546 while the Gray-no-reserve arm survives — the reserve's
early 21-material withholding phase-shifts the second post-move build into the W-death window and
re-introduces the exact W-bound stall the Gray encoding removes. That harmful-combination did **not**
recur on the unseen finals (0/4; G3 passed), so it is a rare (1/8 engineering seeds) failure mode of
the *combination*, recorded as the honest residual — the reserve is unnecessary for Gray on the
tested cohorts and, under repetition, potentially harmful.

In one sentence: consolidating AC99 shows the Gray-coded streak is the thing that works — the
reserve is unnecessary for Gray and the 28-replica reset is sustainable across two route changes —
and both the reserve (with binary) and the Gray encoding (without reserve) carry the full
adaptation on this cohort, while the AC98/99 reserve+Gray *combination* carries a rare
engineering-seed failure mode the no-reserve Gray does not.

## Per-seed outcome (both histories identical)

| seed | priority    | bin_ctl (binary, no reserve)          | bin_res (binary + reserve)         | gray_ctl (Gray, no reserve)        | gray_res (Gray + reserve)          |
|------|-------------|---------------------------------------|------------------------------------|------------------------------------|------------------------------------|
| 4444 | `[0,3,2,1]` | survive, 1 drop (expiry), reacquires  | drop@8209 + drop@12327, survive    | drop@8227 + drop@12316, survive    | drop@8209 + drop@12302, survive    |
| 4445 | `[2,0,3,1]` | survive, 1 drop (expiry), reacquires  | drop@8202 + drop@12302, survive    | drop@8223 + drop@12307, survive    | drop@8201 + drop@12311, survive    |
| 4446 | `[1,0,3,2]` | **dies 8448** (streak stuck 5, 0 drops) | drop@8228 + drop@12331, survive  | drop@8232 + drop@12323, survive    | drop@8228 + drop@12330, survive    |
| 4447 | `[0,3,2,1]` | survive, 0 drops (both moves by expiry)  | drop@8205 + drop@12300, survive  | drop@8220 + drop@12328, survive    | drop@8216 + drop@12308, survive    |

- **gray_ctl** and **bin_res** (the two consolidated architectures): 4/4 distinct seeds relinquish +
  re-acquire (relinq_by_move `[1,1]`) + keep producing at **every** move, and survive.
- **bin_ctl** (binary, no reserve): 1/4 dies (4446, the AC96 economic/W-bound stall at streak 5); the
  other 3/4 survive only by *natural expiry* of the stale entry (0 or 1 active drops, not 2) — the
  binary counter cannot afford the relinquishment at every move.
- **bin_res** and **gray_res**: 4/4 survive with 2 drops each (relinq_by_move `[1,1]` on every seed).
- The load-bearing direction (gray_ctl survives/relinquishes where bin_ctl dies) holds on 4446.

## The mechanism (the honest new findings)

**The Gray encoding is what carries the relinquishment, and it is sustainable across two moves.**
On every seed, gray_ctl actively drops and re-acquires at both moves (2 drops), while bin_ctl on the
3 surviving seeds manages only 0-1 drops and relies on the stale entry expiring (life 64) and
re-binding blind. On 4446 bin_ctl cannot even do that: the binary 3→4 increment (21 replicas, W ≥ 3)
stalls in the post-move W-death window, the streak freezes at 5, and the organism dies of the W/C
collapse at 8448. The Gray 1-bit increments (7 replicas, W ≥ 1) build straight through both windows.
(A third or fourth move would extend the evidence; it would not add robustness beyond the two-move
demonstration.)

**The reserve is unnecessary for Gray, and the 28-replica reset does not compound.** On every final
seed, gray_res releases the reserve's drop/stall/wlow triggers at most once or twice and the release
is never load-bearing for the relinquishment itself — gray_ctl (which has no reserve at all) does the
identical relinquishment. The Gray 5→0 reset (21 replicas) + drop (7) = 28 exceeds `RESERVE_LEVEL=21`,
but the reset self-heals on the post-re-acquisition productive contact (streak_final = 0 on every
individual), exactly as AC99-D2 predicted — so the "dearer reset" does not compound over two moves.

**The reserve is not only unnecessary — it is potentially harmful (the engineering seed 7, reported not
gated).** On engineering seed 7, `gray_res` arms the reserve at t≈525 (withholds 21 material), the
withholding phase-shifts the material trajectory, and at the second move the build lands in a W-death
window. The second relinquishment **fires** at 12335 (drop succeeds, `relinquishments=2`,
relinq_by_move `[1,1]`, register bit set) — but it is the organism's last functional act, and the
failure is **downstream of the recorded drop, not a stalled increment**. After the second move W-birth
stops entirely (`W_birth` in window 2 = 0), so two things fail together: (1) the Gray reset write
(5→0, 21 replicas) is refused for lack of W, leaving the streak stuck at 5 even though the drop fired;
and (2) re-acquisition cannot happen — the deposit path needs `8·interior_W ≥ 21` to re-bind key 1, so
with W gone a productive blind contact cannot be stored (`reacquire_ticks` has no move-2 entry). W and
C die together, energy drains, and the organism dies at 12546 with material still 98 (so it is the W/C
collapse, not material starvation). This is the AC97/AC98 failure mode (a fixed *material* reserve
cannot answer a *W*-denominated shortfall) now caused by the reserve *combined with* repetition. It
recurred 0/4 on the finals, so it is a 1/8-engineering-seed failure mode of the *combination* — the
honest residual, not a gate.

**The reversal of AC99's load-bearing direction is a combination effect, not a Gray effect.** AC99
showed gray_res survives where bin_res dies (4442). Under repeated moves the opposite can happen on a
single engineering seed (7: bin_res survives, gray_res dies) — but that is the *reserve* harming the
Gray arm, not the Gray encoding being weaker: on that same seed gray_ctl (Gray, no reserve) survives
and bin_ctl (binary, no reserve) dies, so the Gray encoding is still the stronger factor at the
no-reserve level. The no-harm gates G2 and G3 passed on the finals, pinning that the encoding harms
nothing and the reserve harmed nothing on this cohort.

## Gates (prespecified in the protocol)

- **G1 sustained adaptation without the reserve — PASS 4/4.** Every distinct seed's `gray_ctl` arm
  satisfies A1 (≥1 drop with the register bit set in each post-move window), A2 (≥1 None→bound
  transition of key 1 in each window), A3 (W/C/B births > 0 in every post-move window), A4
  (`completed`). Both histories identical per seed.
- **G2 no-harm, encoding direction — PASS 4/4.** No seed where `bin_res` survives and `gray_res` dies.
- **G3 no-harm, reserve direction — PASS 4/4.** No seed where `gray_ctl` survives and `gray_res` dies.
- **G4 state sufficiency (per-tick observer-discard, on gray_res) — PASS 8/8.** The gray_res run with
  the succession observer + host streak dict discarded at a mid-streak tick is byte-identical at every
  one of 16,384 ticks (trajectory-level; `swap_applied`, `streak_at_swap == 2` on all 8 individuals).
- **G5 endogenous reserve (no external rescue) — PASS.** Every reserve-arm individual
  (`gray_res`, `bin_res`): `reserve_m > 0` and `reserve_released_m <= reserve_m`.
- **G6 completeness + determinism + arm identity — PASS.** 32 rows; sampled rerun byte-identical;
  each arm reproduces its AC99 runner **byte-for-byte** (state_hash) at the single-move schedule
  `[(8192, 'flip')]` — the schedule is the only change in the runner.

## Reported, not gated

- **The load-bearing direction.** gray_ctl survives/relinquishes where bin_ctl dies (4446). Reported
  per seed, not gated (a positive-only contrast would be AC97's mistake).
- **The harmful combination (engineering seed 7).** Reserve withholding phase-shifts the second
  post-move build into the W-death window; the second relinquishment **fires** at 12335 (drop
  succeeds, relinq_by_move `[1,1]`), then re-acquisition and the streak reset both fail because W-birth
  stops after the move — W/C collapse at 12546 with material 98 (not starvation). 1/8 engineering
  seeds; 0/4 finals.
- **The reserve's maintenance trade-off.** reserve_m 21-63, released 21-42, paid arm/disarm/repair
  writes a small fraction of bank-1 repair; under the Gray streak the release triggers are
  near-redundant (D2's prediction, now under repeated moves).
- **Active vs passive relinquishment.** bin_ctl on the 3 surviving finals relinq drops only 0-1
  times (natural expiry), while every Gray arm and bin_res drop actively at both moves (relinq_by_move
  `[1,1]` on every final seed) — the Gray encoding (and, independently, the reserve) make the
  *decision* affordable, not just the survival.
- **Survival is a bimodality-aware lower bound** (AC68).
- **Priorities.** 4444/4447 `[0,3,2,1]`, 4445 `[2,0,3,1]`, 4446 `[1,0,3,2]` — none is AC83's
  adversarial `[3,0,2,1]`; the relinquishment is a streak/register decision, not a
  renewal-contention decision.
- **Supplied machinery remains.** `advance()` and `prog.choose` are still host-supplied format-level
  machinery; no autopoiesis claim. The reserve is still a fixed minimum reserve, not an acquired
  allocation decision (AC96-D4's open item).

## Verification

- `audit_ac100.py`: 32 rows, arm invariants (the 2×2 outcomes, the no-harm directions, history
  identity, the load-bearing direction), observer-discard record 8/8, arm-identity record 32/32,
  gates re-derived WITHOUT simulating and matching the recorded result. All 19 source hashes match
  the freeze (no drift); `AC100_PROTOCOL_v1.md` is byte-frozen.
- `replay_ac100.py` passes: 4/4 exact (state_hash + endpoint fields, one per arm), observer-discard
  1/1 per-tick byte-identical, arm-identity 4/4.
- `test_ac100.py` green (schedule mapping = frozen perm at single move; single-move byte-identity of
  all four arms; finals recorded-outcome regressions pinning G1 pass, the 4446 binary death, both
  no-harm gates, reserve-redundancy, seed-disjointness, the recorded gates; per-tick observer-discard
  on the finals).
- `test_ac99.py`, `test_ac99_d2.py`, `test_ac99_d3.py` and the core AC1-9 suite remain green.
- No frozen runner modified: `ac99.py`, `ac99_d2.py`, `ac99_d3.py`, `ac99_d4.py`, `ac98.py` and every
  earlier freeze are untouched; `audit_ac99.py` still passes (the AC99 result is intact).
- **Errata:** the post-freeze wording corrections (engineering 0-7, two successful alternatives,
  seed-7 failure downstream of the drop, the regenerated per-seed table, the headline and claim
  wording) are recorded in `AC100_ERRATA_v1.md`. `AC100_PROTOCOL_v1.md` is restored to its frozen
  bytes (`f7990a73…`), so the protocol no longer drifts; the corrections live in the errata file
  instead of in a hash-drifting protocol edit.

## Boundary and next step

The internally maintained organization affords self-preservation through two *successive* route
changes on unseen seeds, and the consolidation isolates that the **Gray encoding** — not the reserve —
is what carries it. The reserve is unnecessary for Gray on the tested cohorts and, on one of eight
engineering seeds, harmful under repetition (the fixed *material* reserve re-introduces the
*W*-denominated stall when combined with a second move). The next open items are unchanged from
AC99/AC96-D4: whether the organism *acquires* how much to save (an acquired allocation policy), and
whether `RESERVE_LEVEL` should be re-derived for the Gray reset width — neither changes the standing
boundary (`advance()` and `prog.choose` supplied; no autopoiesis claim). All earlier results are
preserved untouched.
