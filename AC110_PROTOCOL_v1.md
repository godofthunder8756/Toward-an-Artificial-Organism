# AC110 (C3) — Isolate ongoing repair after successful acquisition

## Question

Does maintaining an ALREADY-ACQUIRED, correct representation depend on ongoing REPAIR of its
vulnerable storage, distinct from RE-ACQUIRING the answer via fresh diagnostics?

Parent: C2 (t_a5ef427b) established a task where the current observation is identical across the two
AC107/108 causes while their histories differ — the occluded-used_held gate (Bernoulli(q) occludes the
used_held bit on channel-1 contacts), so a maintained cause-estimate is load-bearing. C1 (AC109)
measured the stored estimate inert in the un-gated world; C2 made history load-bearing.

## Hypothesis (the support claim, tested for falsification)

After the estimate is acquired (correctly written), its ongoing CORRECTNESS and USE depend on paid
repair of its vulnerable storage, separable from re-acquiring via fresh diagnostics.

The falsification that this study is built to detect and record: repair is unnecessary — accuracy and
use hold without it, because reacquisition (bel_write) dominates during the decision-relevant window.
The study does NOT claim maintenance dependence the data does not establish.

## The representation and its two maintenance paths

The representation is the AC107 one-bit cause estimate e in {E_world=1, E_machinery=0}, stored in the
dead-rule action bit (traces[0, bel_off], 7 replicas, acquired value 1 = E_world), damaged by the
sticky-SET program stream (0->1), read by majority (>= 4 of 7), and repaired by the paid bank-0
majority-restore (action 2). It is EXCLUDED from reg_from_active (reconstruction), so action 2 is its
ONLY repair path.

  - REPAIR        = action 2's bank-0 majority-restore (restores each bank-0 bit to its 7-replica
                    majority; carries no diagnostic input).
  - REACQUISITION = bel_write (reads the current (bound, used_held, productive) triple and re-writes
                    the conclusion; re-derives the answer from fresh diagnostics).

## The contrast (both arms keep reacquisition; only repair differs)

  - `maintained` : action 2 repairs the estimate's storage (full repair).
  - `no_repair`  : action 2's bank-0 majority-restore EXCLUDES the estimate bit (selective cut of the
                    representation's repair); bel_write (reacquisition) is untouched.

The cut is performed by source surgery on ac4.react: the repair block's site list is filtered to drop
`bel_off` when `skip_est` is set, leaving every other bank-0 bit's majority-restore intact. The
maintained arm runs ac4.react itself (byte-identical to frozen by construction).

## Declared damage regime

The FROZEN ambient sticky-SET stream (1e-4 per replica per tick, `b.traces[0,:126]|=core_flips`),
which reaches the estimate by construction (the estimate lives in bank 0). NO elevated rate is used:
the ambient rate already flips the estimate's 7 replicas to a majority over the post-window horizon,
so the repair cut is exercised without degrading the whole organism. This is the smallest justified
damage regime — the frozen one. (An elevated BEL_DAMAGE knob exists in the runner as an engineering
diagnostic only; the frozen study runs at BEL_DAMAGE = 0.0.)

## World constants (declared)

  - Q = 0.5 (Bernoulli occlusion probability of used_held on channel-1 contacts; the C2 gate).
  - PORTS = 4 (blind fallback 1/4), WINDOW = 96 (read-cut window), STREAK_N = 6.
  - TICKS = 16384, DEV = 512, MOVE_TICK = CUT_TICK = 8192.
  - BEL_DAMAGE = 0.0 (ambient frozen stream).

## Conditions

  - `no_cause` : no intervention (estimate = 1 = E_world, acquired value, never written). Clean control.
  - `move`     : channel-1 mapping flips at t=8192; entry intact but stale. Correct: relinquish
                 (e = 1 = E_world). The estimate is 1 throughout; sticky-SET (0->1) is inert. Clean control.
  - `cut`      : read of route-1 suppressed for [8192, 8288); entry intact and correct. Correct: hold
                 (e = 0 = E_machinery). The estimate is written to 0 by bel_write and the ambient
                 sticky-SET stream degrades it toward 1 — the only condition where the repair cut is
                 exercised.

## Endpoints (measured per individual, reported separately)

  1. STATE DEGRADATION: bel_at_horizon (estimate majority read at t=16383), bel_minority_end,
     bel_ones_at_cut_end, bel_ones_ever, bel_min_ever, bel_wrong_ever, first_wrong_read.
  2. ACCURACY: bel_wrong_in_window (ticks in [8192, 8288) where the estimate reads != true cause),
     bel_at_cut_end (read at window end). True cause = 0 (cut) / 1 (move).
  3. BEHAVIOURAL USE: relinquishments, routes, drop_ticks, reacquire_ticks.
  4. EXPENDITURE: reg_writes (repair writes), bel_writes (reacquisition writes), writes (total),
     proactive_writes, memory_writes.
  5. VIABILITY: completed, first_dead.

## Gates (prespecified before confirmation; engineering informed the endpoints, not the outcome)

  - G1 (clean control / intervention validity): no_repair == maintained (state_hash) in no_cause and
    move, 32/32. The repair cut is inert where the estimate is 1 (sticky-SET 0->1 is a no-op).
  - G2 (accuracy independence — FALSIFIES the support claim on correctness): in cut, per-individual
    bel_wrong_in_window is equal across arms AND bel_at_cut_end == 0 (correct) for both arms, 16/16.
    Cutting repair does not degrade the estimate's correctness during the decision window.
  - G3 (use independence — FALSIFIES the support claim on use): in cut, per-individual relinquishments
    AND routes are equal across arms, 16/16. Cutting repair does not degrade behavioural use.
  - G4 (storage dependence / non-vacuity): in cut, per-individual maintained bel_at_horizon == 0 AND
    no_repair bel_at_horizon == 1, 16/16. Repair IS load-bearing for storage — the only place the arms
    differ — and this is post-window, decision-irrelevant (a latched conclusion drifting after the cause
    has passed; no second cause re-reads it in this world).
  - G5 (viability identity): no_repair == maintained on completed AND first_dead in ALL conditions,
    48/48. The repair cut does not affect viability. (The AC107 move-condition collapse is shared by
    both arms identically; it is a route-move consequence, not a repair effect.)

G2 and G3 record the falsification; G4 proves the arms are not running identical configs (non-vacuity),
so the G2/G3 equalities are a genuine "repair cut changes storage but not correctness/use" contrast.

## Cohort and stopping rule

  - Engineering: seeds 0-7 (16 individuals, both histories). Informs the endpoints and gate shapes;
    DISCLOSED here, excluded from the final sample.
  - Finals: seeds 6200-6207 (16 individuals, disjoint from engineering, AC107 6000-6007, and AC108
    6100-6107). Run ONCE after this protocol is hashed.
  - Stopping rule: the finals are the confirmatory sample. Gates are NOT moved after seeing the result;
    a failed gate is recorded as a failure and its measured value pinned (AC16/AC17 discipline). No
    individual, seed, or condition is dropped post hoc.

## Reporting scope

If G2/G3 pass and G4 passes, the honest verdict is FALSIFICATION of the support hypothesis: ongoing
repair is not necessary for the acquired representation's correctness or use under the tested
conditions; its correctness is maintained by reacquisition, and the repair path (action 2) is
structurally unable to fire during the decision window (a single estimate bit contributes at most 3
minority replicas, below the whole-bank minority>=4 trigger; the ambient program damage is too slow
within 96 ticks). The repair's only measured effect is on decision-irrelevant post-window storage.

SOURCES (declared): ac110.py ac107.py ac106.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC110_PROTOCOL_v1.md
