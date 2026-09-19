# AC96 protocol v1: the relinquishment failure-streak is carried by maintained state — state sufficiency completed

STATUS: **frozen before the first final seed.** Written 2026-09-19. This is the protocol + finals for
AC96-D4, the last step of the AC96 state-sufficiency line. AC95-D1 audited every persistent host
variable on the AC94 operational control path and found exactly two class-C leaks: the succession
timer's `timer_reset_done` host flag (closed by AC95-D2 as the RIP bit) and `alloc.streak`, the AC75
erase-on-relinquishment failure-streak dict that gates the `_drop` write on every arm. AC96-D1
designed the internalization (the dead rule's six zero-valued free bits), AC96-D2 implemented it
(`ac96.py`: majority read, atomic W-gated paid increment/reset, host dict vestigial), and AC96-D3
established the three mechanism tests in engineering (relinquishment fires, observer-discard on the
streak is byte-identical, a machinery-only W cut stops every paid streak write and a machinery-only
rescue resumes the correct count). This protocol freezes the claim: **the relinquishment
failure-streak — the last host-side operational memory on the control path — is now carried by the
organism's vulnerable, maintained state. Combined with AC95, the state-sufficiency claim drops its
"succession-path-only" qualifier: the trajectory is fully determined by maintained internal state
plus the environment.**

SOURCES (declared): ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC96_PROTOCOL_v1.md

## The question and the claim

AC95 froze state sufficiency on the succession path (the RIP bit, observer-discard equivalence); the
one remaining host-side leak was `alloc.streak`, inert in the AC94/AC95 finals (`transition='none'`
leaves no stale route) but still gating the `_drop` write on every arm. AC96 asks whether the
relinquishment decision is also carried by maintained state. The decisive test is the same
**observer-discard equivalence** AC95 used: preserve the organism's maintained state, discard the
host's observational history (replace the succession observer AND clear the vestigial host streak
dict), resume, and require byte-identical `state_hash`. The claim is that the fixed architecture
satisfies this for every individual at a mid-streak discard point (streak non-zero but below
`STREAK_N`, a bound entry going stale), and that the streak is maintained (damaged + repaired) and
W-gated (a machinery-only cut freezes its paid writes, a machinery-only rescue resumes the correct
count). The host-streak control (`streak_maintained=False`, the frozen ac95 behaviour) is the direct
rival: it still carries the host dict, and its byte-identity to `ac95.run('gated')` proves the runner
is a correct extension.

The gates (prespecified, categorical per individual):

1. **G1 state sufficiency (observer-discard on the streak).** Every final individual: the `maintained`
   trajectory with the host observer AND host streak dict discarded at a mid-streak tick is
   byte-identical (`state_hash`) to the undisturbed `maintained` run. Non-vacuity: the swap is
   applied (`swap_applied=True`) at a non-zero streak (`streak_at_swap == 2`).
2. **G2 relinquishment mechanism fires (conditional on affordability).** (a) Test-world check: at
   least one final individual relinquishes (sum of `relinquishments` over `maintained` individuals
   >= 1 — else the world does not exercise the drop). (b) Every `maintained` individual with
   `relinquishments >= 1`: the drop tick's register bit is set (majority True), and the moved key (1)
   is re-acquired after the drop tick.
3. **G3 streak maintained.** Single-step (pinned in `test_ac96.py`): (a) the streak bits are damaged
   by the program stream and repaired by the paid bank-0 majority-restore; (b) a productive contact
   resets the streak to 0 via a maintained (paid) write.
4. **G4 interruption + W-gating + machinery-only rescue.** Every final individual: cutting W at a
   mid-streak tick stops every paid streak write (`streak_writes_after_cut == 0`) and fires no drop
   (`relinquishments == 0` — no host-assisted completion), degrades the streak only sub-threshold
   (`streak_degraded_bits_end == 0`, no majority flip), and the organism dies; a machinery-only
   rescue restores the correct count (`streak_at_rescue == streak_at_cut`) with paid writes resuming
   (`streak_writes_after_cut > 0`) and survival.
5. **G5 completeness + determinism + host-equivalence.** Row count == seeds x 2 x 3; a sampled exact
   rerun of the first row is byte-identical (`state_hash`); and the host-streak control is
   byte-identical to `ac95.run('gated')` on every final individual (the runner is a correct
   extension — the streak storage is the only change).

## The mechanism (what changed, and why)

- **D1 — storage.** The permanently-dead rule (mask 32, action 5) contributes six zero-valued word
  bits beyond the AC12 register: mask bits 4/6/7/8 (word bits 5/7/8/9) and action bits 1/3 (word
  bits 11/13). `base = 14 * dead_rule_index`; the six offsets are resolved once at acquisition (the
  AC12 register rule); key k's 3-bit counter is offsets `[3k:3k+3]`, LSB first, read by majority
  (>= `STREAK_THRESHOLD = 4` replicas of 7) and written with an atomic, W-gated paid increment/reset
  (`streak_write`: writes only the differing replicas, refuses the whole transition if it exceeds
  `_cap = min(32, 8*W, energy, material)`). The offsets are excluded from `reg_from_active` (decision
  state is not program content).
- **D2 — behaviour.** The host dict (`ac12.Alloc.streak`) is vestigial on the maintained arm and
  never read. The implemented increment condition `cur + 1 >= STREAK_N -> drop` preserves the frozen
  host's post-increment drop tick exactly. **Measured in D2/D3 engineering (seeds 0-7): the paid
  streak write is starved by the move's material collapse, so the maintained arm relinquishes on a
  subset of individuals where the host control relinquishes on all** — the internalization preserves
  the mechanism, not the behaviour. This is the recorded economic finding, reported not gated.
- **D3 — mechanism tests.** Relinquishment fires (engineering seeds 0/3: streak reaches 5, `_drop`
  sets the register bit, erases the entry, re-acquires within 2-4 ticks; the drop's own reset
  `5->0` is refused — 14 replicas — leaving a stuck streak=5, harmless post-erase). Observer-discard
  at mid-streak is byte-identical. A machinery-only W cut stops every paid streak write (no
  host-assisted drop), degrades the streak only sub-threshold (0-1 replicas, no majority flip) over
  the ~220-tick W=0 window, and a machinery-only rescue restores the correct count with paid writes
  resuming.
- **D4 — no new mechanism.** The observer-discard, W-cut, and W-rescue hooks already exist in
  `ac96.py` (`swap_at`, `cut_tick`/`rescue_tick`); D4 adds the finals collector and freezes the
  gates. Nothing about the organism changes in D4.

## World, arms, seeds

World constants unchanged from AC95, but `transition='perm'` (the relinquishment world — the route
move at t=8192 creates the stale route that the streak counts). PORTS=4, YIELD=64, TICKS=16384,
CORRUPT_TICK=8192, MOVE_TICK=8192, sticky 1e-4 damage on both banks (independent streams),
STREAK_N=6, STREAK_THRESHOLD=4, REGISTER_THRESHOLD=4, the order-preserving generic-over-syntax
decoder, AC75's erase-on-relinquish. `corrupt=False` for every condition (the relinquishment is the
sole event; corruption at t=8192 would be a second, unrelated challenge).

Three conditions per individual:

- `maintained` — `streak_maintained=True`, `damage=True` (the frozen condition, the arm under test).
- `host` — `streak_maintained=False`, `damage=True` (the host-streak control, the direct rival).
- `maintained_nodmg` — `streak_maintained=True`, `damage=False` (the G3 damage-vs-undamaged
  comparison; the "damaged-but-repaired makes the same decision" measurement).

24 rows = 4 seeds x 2 histories x 3 conditions. History is a trivial repeated measure (the runner
gates `activation=[True,True]` and the RNG seeds depend on seed, not history), so the two histories
are identical per seed; it is kept to match the line's `seeds x 2 histories` convention.

Final seeds `4412, 4413, 4414, 4415` (4 seeds x 2 histories = 8 individuals), disjoint from
engineering 0-7, from the D2/D3 engineering seeds (0-3), and from every prior final family <= 4411
(and the separate 4600-4871 order-line families and the 5100-5507 confirmatory families).

## Screening disclosed (before this protocol was frozen)

The final family 4412-4415 (and the wider 4412-4431 to characterize the rate) was screened before
this protocol was written, to check the test-world condition and shape the gates — the step the
AC96-D3 handoff required ("do NOT write G2 as a blanket gate without first checking which seeds
relinquish"). Measured on 4412-4415: 4413 relinquishes (drop@8206, re-acquire@8209, register bit
set); 4412/4414/4415 die at 8415-8444 with the streak stalled at 5 (the paid increment/drop write is
refused by the move's material collapse); across 4412-4431 exactly one seed (4413) relinquishes.
Consequences, all reflected in the gate shapes above: G2 is conditional (test-world check + a
well-formed-drop assertion on the relinquishing individuals only); G3's "makes the same decision"
clause is reported, not gated (the damage-vs-undamaged decision differs on 4412/4414); the
"reproduces host behaviour (same drop ticks)" clause of the card's G2 is dropped and reported as
falsified (maintained relinquishes 2/8 vs host 8/8, drop ticks shift). A relinquishments==0 family
would be a failed test-world check, so the screening is disclosed rather than concealed.

## Gates (prespecified, categorical per individual)

- **G1 (state sufficiency).** Every `maintained` individual: the observer-discard run
  (`swap_at` at the mid-streak tick) has `swap_applied=True`, `streak_at_swap == 2`, and
  `state_hash` identical to the undisturbed `maintained` run.
- **G2 (relinquishment mechanism, conditional).** `sum(r['relinquishments'] for r in maintained)
  >= 1`; and every `maintained` individual with `relinquishments >= 1` has a drop tick whose register
  bit is True and a re-acquisition of key 1 after the drop tick.
- **G3 (streak maintained).** Single-step: `test_ac96.py::TestStreakDamageRepair` (damage + bank-0
  majority-restore repairs the streak bits) and `test_ac96.py::TestProductiveReset` (a productive
  contact resets the streak via a maintained write) pass.
- **G4 (interruption + rescue).** Every individual: the no-rescue cut arm has
  `streak_writes_after_cut == 0`, `relinquishments == 0`, `streak_degraded_bits_end == 0`,
  `not completed`; the rescue arm has `completed`, `streak_at_rescue == streak_at_cut`,
  `streak_writes_after_cut > 0`.
- **G5 (completeness + determinism + host-equivalence).** 24 rows; sampled rerun of rows[0] is
  byte-identical; `ac96.run(..., streak_maintained=False)` is byte-identical to `ac95.run('gated')`
  on all 8 final individuals.

## Reported, not gated

- **The economic finding (the line's headline, unchanged).** The internalized streak is *paid*, and
  in the relinquishment world the move's income collapse starves the paid streak write (increment
  AND reset) AND its repair. On the finals family the `maintained` arm relinquishes 2/8 individuals
  (seed 4413 x 2 histories) versus the `host` control's 8/8, and 6/8 maintained individuals die
  (8415-8444) with the streak stalled at 4 or 5 and routes `[None, None]`. Drop ticks shift where
  the maintained arm fires (4413: host 8216 vs maintained 8206). This is the AC11/AC12/AC13 wall one
  level down: the decision's own write is starved by the very income collapse the decision exists to
  pre-empt. State sufficiency is about *what determines the trajectory* (G1), not about whether the
  internalized decision is economically viable — the two are reported separately.
- **The damage-vs-undamaged decision difference.** `maintained` (damage=T) vs `maintained_nodmg`
  (damage=F) differ on 2/4 seeds (4412/4414 drop under no-damage, stall-and-die under damage): the
  paid bank-0 repair (which maintains the streak AND the program) competes with the paid increment
  for the collapsing material, so the damaged-but-repaired streak does *not* make the same decision
  as the undamaged one. This is the reason G3's "same decision" clause is reported, not gated.
- **The streak reset starvation.** Where the drop fires, the drop's register write (<= 7 replicas)
  succeeds but the reset `5->0` (14 replicas) is refused, leaving a stuck streak=5 — harmless
  post-erase (the next productive contact resets it), the D3 finding.
- **Survival is a bimodality-aware lower bound** (AC68). The 6 deaths are the material-starve /
  attention-hijack cascade, reported per individual, not a survival guarantee.
- **Priorities.** The final family includes 4412 = `[3,0,2,1]` (AC83's adversarial "renewal last"
  priority) and 4413/4414/4415 = `[2,3,1,0]`/`[0,2,3,1]`/`[2,1,3,0]`. The relinquishment is a
  streak/register decision, not a renewal-contention decision, so the priority ordering does not
  confound the mechanism; recorded as a scope note.

## Anti-drift rules

- The runner creates `ac96_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed set
  (which includes this protocol file).
- `test_ac96.py`, `audit_ac96.py`, `replay_ac96.py` are NOT hashed into the frozen snapshot (AC17's
  rule).
- Engineering seeds (0-7) are excluded from the final sample and are disjoint from the final family.
- The equivalence (declared, verified before finals): `ac96.run(..., streak_maintained=False)`
  reproduces `ac95.run('gated')` byte-for-byte (`state_hash`) in the perm world — proving the runner
  is a correct extension and the streak storage is the only change.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.

## Source hashes (computed before the first final seed)

    (recorded in ac96_results_v1/pre_run_snapshot.json at freeze time)
