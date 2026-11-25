# P1h protocol: is the second-order residue explained by a non-linear read of the evidence? (Layer 4)

- **Status:** FROZEN before any P1h measure was computed (this commit).
  Stage 1 runs on P1g's saved weights; stage 2 (fresh seeds) runs only
  under the gate in §5.
- **Follows:** [P1G_GRADED_RESULTS.md](P1G_GRADED_RESULTS.md): the monitor
  is confirmed; the declared second-order test was PRESENT but small
  (M2_nn_own 0.005, 25/27, about 1% of M); post-hoc, about half of it went
  when the LDA margin was matched too. Chosen by the PI ("proceed with
  whichever step best fits the goals", 2026-11-25).
- Astra review waived by the PI. No consciousness claim.

## 1. Question

At matched first-order confidence — the agent's own report-logit gap **and**
a non-linear read of how strongly its state points to the stored value — does
a conflict in its memory still raise the agent's probability of abstaining?

- If **yes**, and only in nets trained with damage, the policy reads a signal
  about its own state (that the memory was tampered with) that no available
  measure of content confidence accounts for: the strongest candidate so far
  in this line for a Layer 4 self-model beyond first-order confidence.
- If **no**, P1g's residue was first-order information in a non-linear form,
  and the monitor is first-order.

## 2. Design

Everything is P1g's (world, arms, training, the graded probe B at EARLY and
LATE, 3600 updates; `trackc_swap/gradmon.py`, `run_p1g_graded.py`,
hash-pinned and unchanged). New, in `trackc_swap/evidence.py` and
`run_p1h_evidence.py`:

1. **Outcome: exact abstention probability.** p_abs = 1 − p(REP0) − p(REP1)
   of the policy head on the collected GRU state — the state the action was
   sampled from (verified: the collected state is the policy's input). Same
   quantity as P1g's sampled abstention in expectation; no sampling noise on
   an event of about 0.5%.
2. **Evidence decoder.** A two-layer MLP (64 units, ReLU, 50 epochs, weight
   decay 1e-3) reading the stored value from the state, trained only on
   trials whose content is unambiguous: clear undrained trials without any
   event, and trials overwritten with the same value. Five-fold cross-fitted;
   every trial (conflict trials included) is scored by exactly one fold model,
   conflict trials assigned at random. It never sees a conflict: its margin
   |logit| is how strongly the state points to a value, read non-linearly,
   with no knowledge of conflicts.
   - Why not a decoder trained on conflicts too: it would learn that
     conflicted states are less reliable and so absorb, by construction, the
     very signal under test (checked on one seed before this protocol: such a
     decoder is far less confident on conflicts than the agent's own head,
     log loss 0.48 against 0.72).
   - Settings chosen on one P1g seed (3200, PFATE, EARLY) from held-out
     decoder loss only (25, 50, 100 epochs all at held-out accuracy 1.000 on
     none and same trials). No abstention quantity was computed.
3. **Primary match: joint.** Each conflict trial against its nearest same
   trial in (own margin, evidence margin), each standardized, kept if within
   0.1 SD on both (with replacement, at least 20 pairs).
   - Why joint: in synthetic first-order-only controls
     (`test_p1h_evidence.py`: a linear policy whose abstention depends only
     on signed evidence, a conflict-only trace direction present in the state
     but unused), the evidence margin alone leaks up to 1.7% of the unmatched
     conflict-same gap, the joint match at most 0.4%, and the LDA margin 0.02
     absolute (it extrapolates badly to conflict states). With a planted
     second-order effect, the joint match recovers it (0.061–0.064 and
     0.219–0.228), in line with the own-margin match (0.063–0.065 and
     0.225–0.229), which is exact in that geometry.

**Stage 1:** P1g's 28 final seeds (3200–3227), saved weights at 3600. The
per-trial data are re-collected exactly (fresh copies, tag 160, P1g's
evaluation order); P1g's declared M2_nn_own must be reproduced exactly from
them (validity). Not fully blind: P1g's own-margin and LDA versions of the
residue were seen; no P1h measure (p_abs, evidence decoder, joint match) has
been computed on these seeds.

**Stage 2 (confirmatory, gated):** 28 fresh seeds (3300–3327) trained under
P1g's frozen design (`G.run_jobs`, BASE_F 0.012), which also gives a
replication of P1g's own declared tests, then the same P1h analysis and
rule. Batches of four, committed after each.

## 3. Measures (per seed and arm; mean over EARLY and LATE runs with a value)

| Measure | Definition |
| --- | --- |
| **M2_joint_p** (primary) | Mean p_abs(conflict) − p_abs(matched same), joint match |
| coverage_joint | Share of conflict trials kept |
| M2_E, M2_E_early, M2_E_late | Match on evidence margin alone (caliper 0.05 SD) |
| M2_E_sampled | The same with sampled abstention |
| M2_E_alt | Evidence decoder with 32 units and another seed |
| M2_own_p, M2_own_sampled | Own margin alone (P1g's match; the sampled version must reproduce P1g) |
| M2_lda_p | LDA margin alone |
| dec_acc_none, dec_acc_same, dec_acc_conflict | Held-out decoder accuracy |
| pabs_conflict, pabs_same | Unmatched mean p_abs |
| trace_auc, trace_pair_auc | Cross-fitted L2 logistic classifier of conflict vs same on the state: AUC; and the share of evidence-matched pairs in which the conflict trial scores higher (is there an integrity trace at matched evidence?) |

## 4. Decision rules (exactly as in `run_p1h_evidence.py`)

| Test | Comparison | Type |
| --- | --- | --- |
| P1H_1 | M2_joint_p of PFATE against 0 | One-sample sign test → PRESENT / REVERSED / NOT_DETECTED (UNDETERMINED under the minimum count) |
| P1H_2 | M2_joint_p, PFATE against PNOFATE | Paired sign test → DERIVED_AHEAD / HOST_AHEAD / NO_DIFFERENCE_DETECTED |

Labels use Holm-adjusted p over the two tests (α 0.05).

**Validity:** PFATE median held-out decoder accuracy ≥ 0.95 on none and on
same trials; stage 1 only: exact reproduction of P1g's M2_nn_own (0
mismatches).

**Overall label:**

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | P1H_1 UNDETERMINED |
| EXPLAINED_BY_EVIDENCE | P1H_1 NOT_DETECTED or REVERSED |
| NOT_SPECIFIC | P1H_1 PRESENT, P1H_2 not DERIVED_AHEAD |
| SECOND_ORDER_SURVIVES | P1H_1 PRESENT and P1H_2 DERIVED_AHEAD |

**Flags:** thin (PFATE median coverage_joint < 0.25); **within leak range**
(PFATE median M2_joint_p below 0.5% of PFATE's median unmatched gap
pabs_conflict − pabs_same — the largest synthetic leak of the joint match,
rounded up).

## 5. Gate for stage 2

Stage 2 runs only if stage 1 is SECOND_ORDER_SURVIVES **and** not within the
leak range (enforced in code). Otherwise P1h ends after stage 1 and is
reported. If stage 2 runs, its label under the same rule is the confirmatory
result; stage 1 is then the discovery set.

## 6. Readings

- **SECOND_ORDER_SURVIVES (stage 2):** a conflict raises abstention beyond the
  agent's own report confidence and a non-linear read of the evidence, only
  in nets trained with damage. The policy uses an integrity signal: Layer 4
  beyond first order, in the operational sense of §9. Not a claim of
  awareness.
- **EXPLAINED_BY_EVIDENCE:** P1g's residue was first-order information read
  non-linearly; the monitor is first-order. Then the next step is to train
  for a second-order signal by design (a task where content confidence and
  integrity come apart), not to look further for one here.
- **NOT_SPECIFIC:** a residue the never-damaged net shares: a mechanical
  property of conflicted states, not a learned monitor.
- trace_auc reads separately: whether the state *carries* an integrity trace
  at matched evidence, whatever the policy does with it.

## 7. Expectations (written before any P1h measure)

| Outcome | Probability |
| --- | --- |
| Stage 1 valid | 0.95 |
| Stage 1 SECOND_ORDER_SURVIVES / EXPLAINED / NOT_SPECIFIC / UNDET-INVALID | 0.40 / 0.45 / 0.10 / 0.05 |
| Within the leak range, given SURVIVES | 0.35 |
| Stage 2 runs | 0.25 |
| Stage 2 SECOND_ORDER_SURVIVES, given it runs | 0.60 |
| trace_pair_auc above 0.5 for PFATE (state carries an integrity trace at matched evidence) | 0.85 |
| M2_E_sampled agrees in sign with M2_joint_p | 0.75 |

**Central expectation:** the state carries a conflict trace, but the policy's
use of it beyond the evidence is at most at the edge of what this method can
resolve.

## 8. Seeds and outputs

- Stage 1: 3200–3227 (P1g's). Stage 2: 3300–3327, disjoint from every
  earlier runner (tested).
- `p1h_evidence/stage1/`, `p1h_evidence/stage2/` (stage 2's training under
  `p1h_evidence/stage2/p1g_design/`): raw.json, scores.json, REPORT.md,
  run.log. `--score` reproduces REPORT.md.

## 9. Limits

- "Second order" means: at matched own report gap and matched non-linear
  evidence margin, a conflict raises p_abs. An unsigned feature that tracks
  evidence strength without carrying the value (so no value decoder reads
  it) would count as second-order here; whether such a feature is "about
  the state" or "about the content" is not settled by this design.
- The evidence decoder never sees conflict states and must extrapolate to
  them; the synthetic controls bound its leak in one geometry only.
- One task, one architecture, one damage type.

## 10. Safety

- Simulated variables only (X1–X5); analysis of saved weights and, in stage
  2, training in the simulated world. No real process is affected.
- No operator, stop, shutdown or host variable exists in the world. The
  operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
