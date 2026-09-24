# AC113 (P6) — frozen confirmation of the heterogeneous-likelihood-ratio two-counter estimate

2026-09-24. The P6 deliverable (task `t_9c80a9ad`): the frozen confirmation of the P5
(`t_96dbc363`) AC112 candidate. P5's feasibility decision fixed the design; this protocol
freezes it and is hashed BEFORE the finals are accessed.

---

## 1. Question and the hypothesis under test

**Question.** On untouched confirmation seeds, at high occlusion (q ≥ 0.9), does the
maintained two-counter weighted estimate beat the strongest single-counter rival on a
GRADED (income / latency) endpoint — or is the result equivalence / no-advantage?

**Support hypothesis (the claim being tested for falsification).** In the
informative-heterogeneous regime (ε ≤ 0.125, q = 0.9), the two-counter's two-dimensional
non-integer weighting is load-bearing: it buys a strictly better decision (higher
post-cause income, earlier move-relinquishment, fewer cut false-relinquishments) than any
single integer counter, at the organism scale.

**Named falsifications (all legitimate findings, none converted into a passing gate):**

- **F1 (equivalence).** The single counter matches the two-counter on the graded endpoint
  within noise → heterogeneous weighting is NOT load-bearing; a maintained integer counter
  suffices (P2's conclusion survives the heterogeneous LR).
- **F2 (no-advantage).** The two-counter is informative (its content causally matters) but
  offers no graded advantage over the single counter (or is worse).
- **F3 (no-information).** The accumulator's read content does not causally matter even
  against the read-forced (0,0) scramble — the estimate carries no information at q = 0.9.

## 2. Architecture (frozen: the AC112 runner, unchanged)

The world and arms are the P5 AC112 architecture (imported unmodified; the income
accumulator added in `ac113.py` is purely observational — verified byte-identical to
`ac112.run` at the same parameters, `state_hash` included, before any freeze). The world is
the AC107/AC110 two-cause world — **move** (channel-1 mapping flips at t=8192; the route-1
entry is stale) vs **cut** (route-1 read suppressed for [8192, 8288); the entry is intact) —
with two declared world changes applied uniformly to every arm:

1. **Occlusion gate (q = 0.9).** On a Bernoulli(q) fraction of channel-1 contacts the
   `used_held` bit is forwarded as `2` (occluded). The P5 decision fixes q = 0.9 — the
   regime where the accumulator is load-bearing (at q=0.7 the open decisive path, 1−q =
   30%, does most of the work).
2. **Residual yield (ε).** Under move a stale HELD entry yields with residual probability ε
   instead of never. Primary ε = 0.08 (P5's default); secondary ε = 0.02 (the most
   heterogeneous end, P4's largest predicted gap).

The candidate is the maintained two-counter accumulator (n_u, n_p in the dead rule's free
bits, Gray-coded, plus a one-bit hold latch), weights supplied (`w_u = log((4/3)(1−ε))`,
`w_p = log(4ε)`), threshold θ. Rivals: `single_counter` (one integer counter, productive
weight w, threshold N), `immediate` (no state), `scramble` (candidate with the counter read
forced to (0,0), writes intact).

## 3. Declared world constants

  - q = 0.9, ε ∈ {0.08 (primary), 0.02 (secondary)}, PORTS = 4, WINDOW = 96.
  - TICKS = 16384, DEV = 512, MOVE_TICK = CUT_TICK = 8192.
  - YIELD_M = 64, YIELD_F = 64 (the AC107/110 world), blind fallback uniform over 4 ports.

## 4. Conditions

  - `no_cause` : no intervention. Clean control — 0 relinquishments in every arm.
  - `move`     : channel-1 mapping flips at t=8192. Correct: relinquish (stale route).
  - `cut`      : route-1 read suppressed for [8192, 8288). Correct: hold (entry intact).

## 5. Endpoints (measured per individual, reported separately)

  1. **Post-cause income** (`income_post` = Σ_{t≥8192} (in_m + in_f)) — the PRIMARY graded
     decision-utility endpoint, per condition. Combined score = income_post(move) +
     income_post(cut).
  2. **Move latency** = first drop tick − 8192 under move (None if never dropped).
  3. **Cut false-relinquish** = relinquishment count under cut.
  4. **Expenditure** = counter_writes, reg_writes, writes.
  5. **Viability** = completed, first_dead (reported, NOT gated — the P4/P5 decision is
     decision utility, not survival).

## 6. Prespecified parameter grids (both families swept — AC11's rule)

  - two_counter θ ∈ {0.5, 0.55, 0.6, 0.66, 0.7, 0.8, 0.9}
  - single_counter (w, N) ∈ {(−6,1), (−6,2), (−6,4), (−4,2), (−4,4), (−2,2), (−2,4), (0,1), (0,2)}

## 7. Cohort, tuning, and stopping rule

  - **Engineering** (DISCLOSED, excluded from the finals): seeds 0–7. Used ONLY to select
    the fixed comparison parameters θ* (two-counter) and (w,N)* (single-counter) by
    maximising combined post-cause income, and to confirm the arms discriminate. The chosen
    values are recorded here before the finals:
      **Primary ε = 0.08**: **θ* = 0.5** (two_counter, combined move+cut income 306,240 on 8
      engineering seeds), **(w,N)* = (−6, 4)** (single_counter, combined income 306,240 — the
      two arms TIE in total at their respective optima).
      **Secondary ε = 0.02** (the most heterogeneous end): **θ* = 0.5**, **(w,N)* = (−6, 1)**
      (both families tie at 153,024 on the 4-seed engineering screen). The two arms tie at
      their optima on engineering in BOTH regimes; the per-seed distributions differ, which
      the finals' paired test resolves.
  - **Finals** (confirmation, untouched): seeds 6400–6407 (8 seeds × 2 histories = 16
    individuals), disjoint from every prior family (AC107 6000s, AC108 6100s, AC110 6200s,
    AC111 6300s, P5 0–7).
  - **Stopping rule.** The finals are the confirmatory sample, run ONCE after this protocol
    is hashed. Gates are NOT moved after seeing the result; a failed gate is recorded with
    its measured value. No individual, seed, condition, or configuration is dropped post hoc.

## 8. Gates (prespecified; validity gates must pass, the comparison is a measured verdict)

**V1 (clean control).** In `no_cause`, every arm has 0 relinquishments and completes, 16/16
per arm. (The no-cause identity; the arms may write different decision-state bytes but make
no relinquishment.)

**V2 (causal role / information carried).** At q = 0.9 the accumulator's read content
causally matters. Evaluated at θ = 0.6 (not θ* = 0.5): at θ = 0.5 the decision threshold
passes exactly through the scramble's (0,0) read point, so the read-forced control
degenerates to the candidate — a declared boundary, not a gate failure. Concretely, at
θ = 0.6: (a) under `move`, the two-counter relinquishes the stale route in 16/16 while the
scramble relinquishes in ≤ 15/16 (its accumulated weak-M evidence lets the candidate drop
earlier than the rare 10% open held-fail path); (b) under `cut`, the two-counter
false-relinquishes in ≥ 1 individual while the scramble false-relinquishes in 0. Failure of
BOTH (a) and (b) = F3 (no-information).

**V3 (observer-discard, inherited).** The candidate's trajectory is per-tick byte-identical
under a mid-window observer+allocator swap, 16/16. (The decision state lives in maintained
state, not the host.)

**G-COMPARE (the scientific question — a measured verdict, not a pass/fail gate).** At the
fixed parameters (θ*, (w,N)*) selected on engineering, compute the per-individual paired
combined-income difference d_i = income_post(two_counter) − income_post(single_counter) on
the finals, and the exact sign-flip p over the 2^16 sign assignments (AC38/AC46's paired
test). Verdict:

  - SUPPORT (bounded) if mean(d_i) > 0 AND p ≤ 0.05 — heterogeneous weighting is
    load-bearing at the organism scale.
  - F2 (no-advantage) if mean(d_i) < 0 AND p ≤ 0.05.
  - F1 (equivalence) otherwise (|mean(d_i)| small or p > 0.05).

The full finals surface (both θ and (w,N) grids) is also reported as a declared diagnostic
(P4's min-mean), but the verdict rests on the fixed-parameter comparison — no in-sample
selection on the finals.

## 9. Reporting scope

Every endpoint is reported per independent seed, and the two histories (correlated matched
arm-runs, same seed) are reported separately from the across-seed sample. If the verdict is
F1/F2/F3, that is the finding — the support hypothesis is recorded as falsified, with the
measured statistic pinned, never reframed as a pass. If SUPPORT, the claim is bounded to
"heterogeneous weighting is load-bearing at the organism scale in the tested regime", and is
NOT a survival, maintenance-dependence, or consciousness claim.

## 10. SOURCES (declared, hashed pre-run)

ac113.py ac112.py AC113_PROTOCOL_v1.md + the AC112 transitive frozen dependency set
(ac110.py ac107.py ac106.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py
ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py
ac4_transport.py ac1.py). Verification tools (audit_ac113.py, replay_ac113.py, test_ac113.py)
are NOT in the frozen hash set (AC16/AC17's rule).
