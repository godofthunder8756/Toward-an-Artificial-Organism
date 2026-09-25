# AC117 (M6) — Estimator-monitoring feasibility harness: does a maintained monitor track and
# act on the damage-component wrongness of the first-order estimate?

## Question

Does the monitor m predict the damage-component wrongness of the first-order cause estimate e,
add value beyond simpler rivals, and causally influence checking/maintenance — with effects
attributable to information use (direction knowledge) rather than added spending alone?

Parent: M5 (t_7e673e39, `M5_MONITOR_HARNESS_DESIGN_v1.md`), which froze the design. Predecessor
M4 (t_6145d172) returned the identifiability verdict: the referent "P(decoded e wrong)" splits by
observability — only the DAMAGE component is identifiable; staleness is an unavoidable miss; the
pure decision window has no error variance. This protocol commits the harness design + parameters
+ gates BEFORE the finals.

## Referent (once, for the record)

The DAMAGE component of "the decoded first-order estimate e is wrong", in the AC110 cut
condition's post-window regime [8288, 16384). The estimate e is the AC107 one-bit cause estimate
(traces[0, bel_off], 7 replicas, majority read), acquired 1 = E_world, written 0 = E_machinery by
the discriminator on open in-window contacts, damaged by the sticky-SET program stream (0->1),
repaired by action 2's bank-0 majority-restore. "Wrong" = decoded e != cause (cause = 0 under cut).

## The monitor m (substrate, inputs, readout, control)

- SUBSTRATE: the retained write-value (last bel_write direction), stored in the dead rule's action
  bit 2 (word bit 12 = 14*dead_rule_index + 12), a free '1' bit acquired as 1 = "retained
  E_world", written 0 = "retained E_machinery" under cut. Distinct from bel_off (word bit 10) and
  the streak free bits (word bits 5,7,8,9,11,13). Majority-read (>=4/7), W-gated paid writes, IN
  the sticky-SET program damage stream, repaired by action 2, excluded from reg_from_active
  (decision state, not program content). The discriminator writes BOTH e and m_off in every arm
  (a shared substrate record); only `monitor` READS m_off for control (a documented interpretation
  of M5's "whether they store m", required so H1 is well-defined on the fixed_duty trajectory).
- INPUTS: (1) directioned count ones at bel_off; (2) retained write-value m_off; (3) shared obs
  bit 2 + resource signals (W<2 / material<=64 / fuel<=8 / _cap refusal), with repair_at_risk
  DERIVED from the resource signals.
- READOUT r in {0,1,2,3}: r = min(3, ones) when last_write==0 else 0; repair_at_risk contributes
  r=3 even when ones<=3. Categorical: unreliable iff (last_write==0 AND ones>=4) OR
  (last_write==0 AND repair_at_risk).
- CONTROL (H2): when unreliable, a targeted per-bit repair of bel_off toward the retained value,
  W-gated by ac95._cap (NOT action 2: a single estimate bit contributes <=3 minority replicas and
  can never trigger obs bit 2, AC110 rule 1).

## The five arms (maintenance policy of e; all share action 2's bank-0 repair)

- monitor   : readout m; targeted repair toward the retained value when unreliable.
- fixed_duty: state-blind; majority-restore e every DUTY_PERIOD ticks (spend-matched).
- reflex    : the obs-bit-2 watchdog; action 2 only (== AC110 `maintained`). The correct null.
- direct    : readout ones>=4 (no retained direction); majority-restore (cements, no fix).
- history   : state-blind to e; a corruption-event counter; majority-restore on threshold.

## World constants (declared)

- Q = 0.5 (C2 occlusion), PORTS = 4, WINDOW = 96, STREAK_N = 6, TICKS = 16384, MOVE_TICK =
  CUT_TICK = 8192, POST_WINDOW = 8288.
- BEL_DAMAGE = 0.01 (DECLARED elevated sticky-SET on the estimate bit). At the frozen ambient rate
  (1e-4) the non-vacuity check FAILS: case 3 base rate = 0 (action 2 maintains e below the flip
  threshold), so the harness is vacuous. 0.01 is the M5 section-8.3 prescription ("declare the
  elevated-damage diagnostic with the rate and read threshold stated together"), and it makes e
  drift so the monitor's catch is exercised. Read threshold = ones>=4 (majority), stated with the
  rate.
- DUTY_PERIOD = 12 (fixed_duty schedule). Selected on the engineering cohort: fixed_duty's spend
  is discontinuous (preventive majority-restore ~513 writes at K=12 vs cementing ~50 at K>=20);
  K=12 is the cheapest state-blind schedule that keeps e correct, ~19% above the monitor's ~432
  directional spend. Disclosed BEFORE the finals.
- HISTORY_THRESHOLD = 2 (corruption-event count before a history majority-restore).

## The two hypotheses (separated)

- H1 PREDICTION: m's readout tracks e's wrongness, scored on the fixed_duty trajectory (repair
  held at the fixed schedule, so e drifts and the four cases arise). The four readouts {monitor,
  reflex, direct, history} and the truth decoded e != cause are recorded per tick t>=8192.
- H2 CONTROL: the five arms compared pairwise on maintenance endpoints (e-correctness, targeted
  repair writes, route retention, income) and reported cost.

## Gates (prespecified; engineering informs endpoints, not outcomes)

H1 (prediction, on the fixed_duty trajectory, cut condition):
- P-G1 case-1 read convention: at ones=3 (damaged, still correct) m reads reliable.
- P-G2 case-3 catch over reflex: at ones>=4 with obs bit 2 silent, m reads unreliable, reflex
  reads reliable.
- P-G3 case-4 leading indicator + move decoupling: under cut with repair_at_risk and ones<=3, m
  reads unreliable (declared false alarm); under move m reads reliable.
- P-G4 P1 referent separation: under move, m reads reliable throughout while direct reads
  unreliable (ones=7>=4) and reflex reads unreliable only when obs bit 2 fires. m decoupled from
  both -> its referent is correctness, not damage.
- P-G5 calibration/proper scoring: m's ECE <= each rival's, and its Brier <= each rival's.
- P-G6 discrimination: m's AUC > each rival's AUC.

H2 (control, pairwise monitor vs each rival, cut condition):
- C-G1 clean control: all five arms byte-identical (state_hash) in no_cause and move.
- C-G2 utility: per-seed post-window route-1 retention (and income) of monitor >= each rival's,
  sign-flip on per-seed differences; gated on dominance/separation-of-minima, not a mean margin.
- C-G3 content inertness (P5): the spend-matched fixed_duty rival does NOT reproduce monitor's
  maintenance behaviour (they differ on repair scheduling and/or the endpoint). If it does, m's
  stored content is inert.
- C-G4 causal role (engineering): scramble_m (force m's readout reliable) removes the targeted
  repair while the decision is unchanged; scramble_e (force e's decision read) changes the
  decision while the maintenance mechanism is unchanged.

Reported, not gated: survival (bimodality-aware lower bound), resource cost (separate table), the
case-2 staleness miss, and the ambient-damage redundancy finding (below).

## The ambient finding (non-vacuity, recorded before the elevated-damage run)

At BEL_DAMAGE = 0.0 (the frozen ambient rate), the monitor's targeted repair is REDUNDANT with
action 2: action 2 fires post-window on other program corruption and restores e's sub-majority
flips before they reach the majority threshold, so case 3 (ones>=4) never arises (base rate 0/8096
post-window ticks) and monitor == reflex on bel_wrong_ever for every seed tested. This is the
M5 section-8.3 non-vacuity failure, and it is the reason the declared study runs at
BEL_DAMAGE = 0.01. Both regimes are reported; the elevated rate is the diagnostic that exercises
the mechanism, not a frozen-law change.

## Cohort and stopping rule

- Engineering: seeds 0-7 (16 individuals, both histories), excluded from the finals, used for the
  non-vacuity check, the DUTY_PERIOD/HISTORY_THRESHOLD tuning, and the causal-role checks.
- Finals: seeds 6800-6815 (16 seeds, 32 individuals), disjoint from AC107 6000s, AC108 6100s,
  AC110 6200s, AC111 6300s, AC115/AC116 6600s. Run ONCE after this protocol is hashed.
- Stopping rule: gates are NOT moved after seeing the result; a failed gate is recorded and its
  measured value pinned. No individual, seed, or condition is dropped post hoc.

## Claim ceiling

If the gates pass, the strongest wording earned: the organism maintains a second-order state whose
referent is the damage component of its first-order estimate's correctness, computed from its
maintenance bookkeeping, dissociable from the estimate (P-G4), discriminating against
shared-bookkeeping rivals (P-G5/G6), and causally effective on maintenance (C-G2/G3/G4). Not
licensed: "metacognitive" unqualified, any staleness claim, or any level-(e) wording. A negative
result bounds THIS design and THIS target.

SOURCES (declared): ac117.py ac110.py ac107.py ac106.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC117_PROTOCOL_v1.md
