# AC96 results v1: the relinquishment failure-streak is carried by maintained state — state sufficiency completed

Parent: AC96-D3 (engineering). Frozen per `AC96_PROTOCOL_v1.md` (hashed before the first final seed).
Runner `ac96.py`; seeds 4412-4415 × 2 histories, 24 rows, 16,384 ticks, `transition='perm'` (the
relinquishment world). Three conditions per individual: `maintained` (streak in maintained state,
damage on), `host` (the frozen ac95 host-streak control, damage on), `maintained_nodmg` (damage off
— the G3 damage-vs-undamaged comparison).

## The claim, and what the evidence earns

The claim was: the relinquishment failure-streak — the last host-side operational memory on the
control path — is now carried by the organism's vulnerable, maintained state, and combined with AC95
the state-sufficiency claim drops its "succession-path-only" qualifier.

**State sufficiency holds, without the qualifier.** G1 (observer-discard on the streak) is 8/8
byte-identical: discarding the succession observer AND clearing the vestigial host streak dict at a
mid-streak tick (streak reads 2 on key 1, a bound entry going stale) leaves the trajectory
`state_hash`-identical on every individual. The two class-C leaks the AC95-D1 audit found
(`timer_reset_done`, `alloc.streak`) are now both organism-side, so the trajectory is fully
determined by maintained internal state plus the environment — no host-side operational memory
steers it.

**The relinquishment *decision* is economically fragile — a new finding, not a failure of the
claim.** The internalized streak is *paid* (increment, reset, and its repair are W- and
material-gated writes), and in the relinquishment world the route move's income collapse starves
those writes. On this finals family the `maintained` arm relinquishes 2/8 individuals (seed 4413 ×
2 histories) versus the `host` control's 8/8, and the other 6/8 die (8415-8444) with the streak
stalled at 5 and routes `[None, None]`. The internalization preserves the *mechanism* and the
*state-sufficiency* property, but not the host's *behaviour* — because the host dict was free
operational memory, and the maintained write is paid. This is the AC11/AC12/AC13 wall one level
down: the decision's own write (and its repair) is starved by the very income collapse the decision
exists to pre-empt.

## Gates (prespecified in the protocol, all PASS)

- **G1 state sufficiency (observer-discard) — PASS 8/8.** Every final individual: the `maintained`
  trajectory with the observer + host streak dict discarded at a mid-streak tick is byte-identical
  (`state_hash`). Non-vacuous on all 8: `swap_applied=True`, `streak_at_swap == 2`.
- **G2 relinquishment mechanism (conditional) — PASS.** Test-world: 2/8 individuals relinquish
  (seed 4413, both histories). Well-formed drop on each: drop@8206 with the register bit set
  (majority True), entry erased, key 1 re-acquired at 8209 — the streak reached 5 (6th consecutive
  unproductive contact) and the drop fired.
- **G3 streak maintained (single-step) — PASS.** `test_ac96.py::TestStreakDamageRepair` (the streak
  bits are damaged by the program stream and repaired by the paid bank-0 majority-restore) and
  `TestProductiveReset` (a productive contact resets the streak to 0 via a maintained write) are
  green.
- **G4 interruption + W-gating + machinery-only rescue — PASS 8/8.** Cutting W at a mid-streak tick
  stops every paid streak write (`streak_writes_after_cut == 0`) and fires no drop
  (`relinquishments == 0` — no host-assisted completion), degrades the streak only sub-threshold
  (`streak_degraded_bits_end == 0`, no majority flip) and the organism dies (8409-8447); a
  machinery-only rescue restores the correct count (`streak_at_rescue == streak_at_cut == {0:0, 1:2}`)
  with paid writes resuming (34-105) and survival.
- **G5 completeness + determinism + host-equivalence — PASS.** 24 rows (= 4 × 2 × 3); a sampled
  exact rerun is byte-identical; the `host` control is byte-identical to `ac95.run('gated')` on all
  8 final individuals — the runner is a correct extension and the streak storage is the only change.

## The economic finding, in numbers

| seed | host (free streak dict) | maintained (paid streak) | maintained_nodmg (no damage) |
|------|-------------------------|--------------------------|------------------------------|
| 4412 | drop@8205, survives     | dies 8444 (streak stuck 5) | drop, survives |
| 4413 | drop@8216, survives     | drop@8206, survives       | drop, survives |
| 4414 | drop@8233, survives     | dies 8415 (streak stuck 5) | drop, survives |
| 4415 | drop@8223, survives     | dies 8441 (streak stuck 5) | survives, no drop (entry expiry + blind re-acquisition) |

The maintained arm relinquishes 2/8 vs the host control's 8/8, and drop ticks shift where the
maintained arm fires (4413: host 8216 vs maintained 8206, −10). The paid increment `4→5` and the
drop's register write are refused once material collapses below their replica cost — the D2/D3
finding, confirmed on fresh finals.

## The damage-vs-undamaged interaction (G3's "same decision" clause, reported not gated)

`maintained` (damage=T) vs `maintained_nodmg` (damage=F) differ on 3/4 seeds: 4412 and 4414 drop and
survive without damage but stall and die with it; 4415 survives without damage (by expiry) but dies
with it. The streak's *read value* is never corrupted by damage (G4's `streak_degraded_bits_end == 0`),
so the difference is not a corrupted read — it is the paid bank-0 repair (which maintains the streak
AND the program) competing with the paid increment for the collapsing material. A
"damaged-but-repaired streak makes the same decision as an undamaged one" is therefore false in this
world; the honest G3 is the single-step damage+repair pin, and this interaction is a recorded
finding, not a gate.

## Reported, not gated

- **The economic headline** (above): state sufficiency holds; the internalized decision is
  economically fragile. These are distinct claims and are reported separately.
- **Streak reset starvation.** Where the drop fires, the drop's register write (≤7 replicas)
  succeeds but the reset `5→0` (14 replicas) is refused, leaving a stuck streak=5 — harmless
  post-erase (the next productive contact resets it), the D3 finding.
- **Survival is a bimodality-aware lower bound** (AC68). The 6 deaths are the material-starve
  cascade (obs bit 1 set by `material ≤ 64`, the material contact preempts the renewal, W and C die
  together, energy drains). Reported per individual, not a survival guarantee.
- **Priorities.** The final family includes 4412 = `[3,0,2,1]` (AC83's adversarial "renewal last"
  priority). The relinquishment is a streak/register decision, not a renewal-contention decision, so
  the priority ordering does not confound the mechanism — a scope note.
- **Supplied machinery remains.** `advance()` (the transition logic) and `prog.choose` (the
  interpreter) are still host-supplied format-level machinery; the machinery-only W rescue in G4 is
  EXTERNAL (labeled diagnostic). State sufficiency is about *where the operational memory lives*,
  not about internalizing the transition logic — that boundary is unchanged from AC90/AC95.

## Verification

- `audit_ac96.py` passes: 24 rows, 15 hashes no drift, arm invariants (the maintained-vs-host
  economic finding, the damage-vs-undamaged difference), observer-discard record 8/8, interruption
  record 8/8, host-equivalence 8/8, gates recomputed without simulating.
- `replay_ac96.py` passes: 3/3 exact (state_hash + endpoint fields), observer-discard 1/1
  byte-identical, interruption 1/1 W-gated+rescue.
- `test_ac96.py` 14/14 green (single-step isolation, streak damage/repair, productive reset, host
  comparator, seed-disjointness, finals observer-discard); `test_ac96_d3.py` 5/5 green; core
  AC1-9 suite 56/56 green.

## Boundary

Full autopoiesis is not claimed. What AC96 establishes is that the organism's *operational memory*
— the succession reset flag (AC95) and now the relinquishment failure-streak (AC96) — is fully
organism-side: the trajectory is carried by vulnerable, maintained internal state plus the
environment, with no host-side operational memory steering it. The transition logic and interpreter
remain supplied format-level machinery, the machinery-only rescues are EXTERNAL, and the internalized
relinquishment decision is economically fragile in the move world — the mechanism is preserved, the
behaviour is not. No content self-production (AC78) and no consciousness claim.
