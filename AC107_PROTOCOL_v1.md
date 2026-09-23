# AC107 protocol v1 — confirmatory freeze of the maintained cause-estimate (K6)

Written before any final-seed run. This is the K6 deliverable (task t_036aeceb): freeze the K5
engineering mechanism (`ac107.py`, seeds 0-7, `AC107_ENGINEERING_v1.md`) and confirm it on an
untouched seed family, answering the card's four questions separately.

K5's feasibility verdict (SUPPORTED) established, on engineering seeds, that the estimate
discriminates the two causes at decision times and that the discrimination is survival-relevant in
both directions. This protocol freezes that mechanism unchanged and re-tests it on disjoint finals.

---

## 1. The mechanism under test (unchanged from ac107.py)

One maintained bit e ∈ {E_world=1, E_machinery=0} in the dead-rule action bit
(`14*dead_rule_index + 10`, acquired value 1 = E_world — the AC12 inverted-semantics pattern),
damaged by the sticky program stream, read by majority, written by the paid W-gated `bel_write`,
excluded from `reg_from_active`. The update rule reads the organism's own
(bound, used_held, productive) triple and gates every conclusion on its own memory (K1's confound
closed):

- `bound & not used_held` → e = E_machinery (cut signature; fires on every in-window contact);
- `used_held & not productive` → e = E_world (F1: held entry failed);
- `not bound & productive` → e = E_world (blind re-bind after a drop).

Consumption: e = E_world → frozen Gray streak relinquishment (threshold STREAK_N=6);
e = E_machinery → withhold relinquishment + proactive renewal.

Arms: `candidate`, `r2` (frozen Gray streak, threshold 6), `r4` (raw per-key counter, HOLD_N=24),
`r1` (reactive, threshold 1), `scramble` (read forced E_world, writes intact).

World: AC100 Gray-streak architecture, corrupt=False, TICKS=16384, DEV=512, PORTS=4, mapping over
{0,1}; `move` flips the channel-1 mapping at t=8192; `cut` suppresses the channel-1 read for
[8192, 8192+96).

## 2. Cohort selection

Final seeds **6000-6007** (8 seeds × 2 histories = 16 individuals), a fresh range disjoint from
every prior family (engineering 0-7; 4412-4439; 4440-4451; 4466/4481/4504/4510; 4600-4872;
4880-4950; 5100-5508; 5600-5607; 5700-5707; 5800-5807; 5900-5907). Engineering seeds 0-7 are
excluded from the final sample.

## 3. Endpoints (registered separately, the card's four questions)

- **Q1 representational function (discrimination):** e reads E_machinery (0) at the cut window end
  and E_world (1) at the first drop in `move`, per individual; post-intervention mistakes.
- **Q2 content causal influence:** the read-only `scramble` (writes intact, read forced E_world)
  changes behaviour in `cut` relative to the candidate.
- **Q3 maintenance dependence:** the estimate's value lives in vulnerable maintained state and is
  read from there (state sufficiency), and its storage is paid-maintained; the scope note below
  states the limit.
- **Q4 comparative advantage:** per-individual survival dominance over r2 (cut) and r4 (move).

Distinguished: representational function (Q1), comparative advantage (Q4), and maintenance
dependence (Q3) are reported as separate endpoints; none is taken to imply another.

## 4. Gates (prespecified)

- **G1 discrimination:** every individual reads bel_at_cut_end == 0 (cut) and
  bel_at_first_drop == 1 (move), with the cut actually experienced (entry bound at cut start), and
  total mistakes == 0.
- **G2 content causal:** candidate relinquishments == 0 in `cut` for every individual; scramble
  relinquishes in `cut` on ≥1 individual and dies on ≥1 individual where the candidate survives.
- **G3 state sufficiency:** observer-discard per-tick byte-identical on the candidate in `cut` for
  every individual.
- **G4 no-cause identity:** candidate == r2 (`state_hash`) in `no_cause` for every individual.
- **G5 comparative advantage:** candidate cut-survival ≥ 12/16 and move-survival ≥ 12/16
  (bimodality-aware lower bound); r2 dies in `cut` on ≥1 individual where the candidate survives;
  r4 dies in `move` on ≥1 individual where the candidate survives.
- **G6 completeness/determinism:** row count == 8×5×3×2 = 240 and a re-run of the first row
  reproduces its `state_hash`.
- **G7 rival distinctness:** HOLD_N > 7 and HOLD_N != STREAK_N; r2 and r4 differ behaviourally in
  both conditions.

## 5. Non-vacuity notes (carried from K5, not hidden)

- The cut does **not** bite r2 on every individual: the streak must reach 6 during the 96-tick
  window, which happens only on priority-corner seeds (engineering: seed 4). G5's r2-death clause is
  the non-vacuity requirement; if no final individual exhibits it, G5 fails vacuously and is
  reported as such.
- The move bites r4 only where the threshold-24 counter holds the stale route into material
  collapse (engineering: seeds 1, 2, 4).
- Proactive renewal is **dropped from the gate list** (K5 measured it inert: r4 keeps the entry
  alive through the cut via the frozen reactive renewal). It is recorded, not gated.

## 6. Scope note on Q3 (maintenance dependence)

The estimate's storage is vulnerable and paid-maintained, but in this architecture the maintenance
is the **single paid write** at cause-onset (measured: bel_writes == 7 replicas, 1 attempt). The
decision window (96 ticks) is short relative to the sticky damage rate (1e-4/replica/tick), so the
storage is not perturbed fast enough for an ongoing-repair loop to be exercised — the AC13 wall.
A "no-maintenance" ablation arm is therefore **not** carried: because the acquired value is the
wrong one (E_world), "never write" and "read forced to E_world" are behaviourally degenerate, and
the `scramble` arm already isolates the read of the maintained storage. Q3 is answered by G3 (the
value is read from maintained state, not host state) + G4 (the estimate is inert absent a cause) +
the vulnerable-storage audit (bit in the damage stream, paid write, excluded from reg_from_active).
This is a bounded answer: the function depends on the maintained storage's *content*; ongoing
*repair* of that storage is not load-bearing in this world and is not claimed.

## 7. Stopping rule

A clean negative on any gate is a finding, not a program failure. Do **not** move a prespecified
gate after seeing the result; record the failure and supersede on fresh seeds only if the mechanism
or information assumption changes (K6's constraint). Any re-open requires a named mechanism change
and a new discriminating prediction.

SOURCES (declared): ac107.py ac106.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC107_PROTOCOL_v1.md
