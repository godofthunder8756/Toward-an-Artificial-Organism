# W-REL bounded exact admission check: analysis specification and compute limit (DRAFT v1)

**Status:** DRAFT specification. **NOT RUN. Execution waits on Aidan's approval (§8, PENDING).**

This is theory-only. It involves no neural training, no exhaustive all-controller certificate, no new architecture family, and no protected controller or register. It makes no C4 or consciousness claim.

Companion to `c4_reliability_assessment_admission_v2.md` (cited below as "v2"). Written 2026-10-21, about 4:25–4:55 AM ET.

Astra consult #21, exact next step (verbatim): "conduct a bounded analytic admission check: history-level symmetry, finite-horizon exploration value, the cost-general controller, and whether the proposed causal criteria distinguish assessment from checking policy." The analysis specification and compute limit below are to be **fixed before execution**.

All parameter values are **illustrative proposals**. They must be frozen by the Specialist, with a written rationale, before execution, and there is no retuning after any value is seen.

---

## 0. Frozen objects (proposed)

**World W-REL-B (v2 §1).**
- Z_t ∈ {S, E}.
  - S: (w, e) = (1/20, 1/5).
  - E: (w, e) = (1/5, 1/20).
- n = 3 evidence bits; X_t uniform.
- Actions: PREDICT, RECHECK (cost c_r), RESAMPLE (cost c_s).
- Reward: 1[correct] − cost. No discounting.
- Initial P(Z_0 = S) = 1/2.

**Transition laws:**
- **H0:** hazard h = 0. Z is persistent for the whole episode.
- **H1:** symmetric hazard h = 1/20 per trial.

**Horizons:**
- H0: T ∈ {1, …, 10}.
- H1: T ∈ {1, …, 5}.
- History-symmetry audit: T ≤ 3.
- Model-free rival: T ≤ 4.

**Cost grid (visible to every agent; no categorical bins):**
- K = 6 pairs: c_r ∈ {1/100, 1/50, 1/25} × c_s ∈ {3/50, 1/10}.
- Within-episode cost switch (I-COST generalization probe): at τ = ⌊T/2⌋, every ordered pair (k → k′), k ≠ k′, giving 30 switches.

**Arithmetic.** Exact rationals throughout. Unnormalized joint weights are stored as integers over fixed denominators, which are powers of 2 and 5. Decisions compare same-normalization quantities, so there is no floating-point decision anywhere.

**Planning fact (computed for sizing only; `plan_counts.py`).** RECHECK produces 128 (X, y, y′) patterns but only **10 distinct S/E likelihood ratios**. Default reads and resamples have likelihood ratio 1.

## 1. A-SYM: history-level symmetry (Astra edit 5)

**Claim to verify (v2 §1.2, lemma L1).** Under W-REL-B, the likelihood of any history is independent of the Z path whenever the history contains no RECHECK observation. RECHECK observations carry the 10-class likelihood ratio.

**Computation.**
- (a) Check exact equality of the per-trial emission tables for PREDICT (16 cells) and RESAMPLE (128 cells) under S and E, and confirm that RECHECK tables differ.
- (b) For H0 and H1, enumerate every history of length ≤ 3 in the no-RECHECK subtree, under every action sequence in {PREDICT, RESAMPLE}³. That is Σ_{t≤3} 144^t ≈ 3.0×10⁶ histories. Verify that the posterior P(Z_t = S | history) equals the prior propagated by the transition law, exactly.
- (c) Verify that one RECHECK changes the posterior for 10 likelihood-ratio classes.

**Output.** VERIFIED / FAILED, with the first counterexample on failure.

## 2. A-VOI: finite-horizon value of information

**Agents:**
- **Non-myopic Bayes (R-HAC-MB):** exact backward induction over reachable belief nodes, per cost pair.
- **Myopic Bayes (R-HAC-MB-myopic):** the same filter with greedy one-trial expected reward. Reported separately (Astra edit 6).
- **Oracle (Z known):** the upper reference.
- **Regime-blind:** the best policy measurable with respect to the RECHECK-free information. Bounded by T·v_blind, by the L1 argument.

**Outputs per (H, T, k):**
- V*, V_myopic, V_oracle and V_blind, all exact.
- VOI_T = V* − V_myopic.
- The exploration cost actually paid: the expected number of RECHECKs, and of RECHECKs in unanimous states.
- The time-to-first-RECHECK distribution.

No exploration schedule is supplied to any agent. If one is ever supplied, it must be charged and disclosed (Astra Q8).

## 3. Named conventional rivals (costs visible to all)

| Rival | Definition | Exact evaluation |
| --- | --- | --- |
| R-CONF-S | Cost-general static confidence rule. Action = argmax_a [ĝ_a(s) − c_a], where ĝ is the gain predicted from the analytic P(X \| y) model, marginalized over the prior on Z. | Closed form per trial; 9 deterministic tables × K. |
| R-CONF-A | Adaptive threshold updated only from default-prediction errors; grid η ∈ {1/20, 1/10, 1/5} × α* ∈ {1/20, 1/10, 1/5}. | Analytic bound V ≤ T·v_blind (L1), plus exact evaluation at T ≤ 5. |
| **R-CG (cost-general controller; Astra Q6)** | Count-based estimates of **its own** conditional correctness per (action, read class), with action_value(a) = est_correct(a, history) − c_a. Optimistic prior counts (α_s, α_f) ∈ {(1,1), (2,1)} × exploration bonus β ∈ {0, 1/20, 1/10}, giving 6 variants. Deterministic tie-break. | Exact forward distribution over (Z, count state), H0, T ≤ 8. |
| R-HAC-MB / -myopic | §2. | §2. |
| R-HAC-MF (secondary) | Tabular Q over φ = (read class, last-RECHECK agreement count 0–3, last check outcome), learning rate 1/4, ε-greedy with ε ∈ {0, 1/10}. | Exact path enumeration, T ≤ 4. |

**Resource ledger (Astra Q7)**, reported per rival rather than equalized:
- state precision;
- number of state variables;
- policy parameters;
- model constants supplied (for example, R-HAC-MB is given the true w and e);
- computation per step;
- supplied buffers.

There is no "same-resource ALL(B)" comparison and no all-controller certificate.

## 4. A-SEP: do the causal criteria separate assessment from checking policy?

**Declared content variable per agent:**
- R-HAC-MB: b_t = P(Z_t = S | history).
- R-CG: its correctness-estimate table.
- R-HAC-MF: its Q-table and window.
- **PM_k (policy-minimal machine for cost pair k):** the coarsest partition of reachable H0 belief nodes that preserves the optimal action at cost k, found by partition refinement. Its state is the partition cell, with no cost-general correctness estimate.

**Criteria computed exactly for each agent (v2 §5):**
- **C-REF.** Force Z = S versus Z = E at τ, and compute the RECHECK and RESAMPLE propensity differences over the next 2 trials.
- **C-T2.** The content variable's prediction of the **agent's own conditional correctness**, for each action, versus the realized value. Report calibration error, and the margin over the pre-check confidence s.
- **C-SEL.** Transplant the content from canonical donors: the max-S and max-E belief nodes at the same layer, for recipient layers t ∈ {2, 4, 6}, which gives 66 + 1001 + 8008 = 9,075 recipient nodes.
  - Report the directional checking errors over 2 trials.
  - Report the first-order probe battery: pre-check p̂ on all 8 read patterns.
  - Report direct post-check inference effects under matched subsequent observations, kept separate (v2 §5.2, category 2).
  - The **credited rescue** reverses the downstream consequence in the declared procedure. Restore-and-rerun identity is recorded as integrity only.
- **I-COST.** Generalization at the 30 switches.

**Output per agent:** the vector of criterion results. The overall label is:
- **SEPARATES** if at least one PM_k fails a criterion that R-HAC-MB passes, for a prespecified criterion set;
- **DOES-NOT-SEPARATE** if every PM_k passes every criterion R-HAC-MB passes;
- **UNRESOLVED-COMPUTE** if the cap is reached.

This is an analysis of these analytic agents only. It says nothing about any learned system.

## 5. Compute estimate and HARD CAP

The estimates assume CPython big-integer arithmetic at about 1 µs per elementary operation, and integers of about 300–400 bits by T = 10.

| Item | Size | Elementary ops (est.) | Time (est.) | Peak memory (est.) |
| --- | --- | --- | --- | --- |
| A-SYM | ~3.0×10⁶ histories × 2 laws | ~6×10⁷ | 1–2 min | < 100 MB (streamed) |
| A-VOI H0, T ≤ 10 | belief nodes cumulative C(21,11) = 352,716; largest layer C(20,10) = 184,756; × K = 6; non-myopic + myopic | ~2×10⁸ | 4–8 min | ≤ 1.5 GB |
| A-VOI H1, T ≤ 5 | ≤ Σ_{t≤5} 11^t = 177,156 nodes × 6 × 2 | ~1×10⁸ | 2–4 min | ≤ 1 GB |
| R-CONF-S / -A | 9 tables; 9-point grid, T ≤ 5 | < 10⁶ | seconds | negligible |
| R-CG, T ≤ 8 | count states cumulative C(20,12) = 125,970 × 2 Z × 6 costs × 6 variants | ~3.6×10⁸ | 6–12 min | ≤ 0.5 GB |
| R-HAC-MF, T ≤ 4 | ≤ 34⁴ ≈ 1.34×10⁶ paths × 2 Z × 6 costs × 2 variants | ~3×10⁸ | 5–10 min | ≤ 0.5 GB (streamed) |
| A-SEP | 9,075 recipients × 2 donors × 6 costs × 4 agent types, 2-trial forward with belief merging; PM_k refinement | ~5×10⁸ | 10–30 min | ≤ 1 GB |
| Independent replay (second code path: forward enumeration vs backward induction; T ≤ 6 for H0 and T ≤ 4 for H1) | subset | ~10⁸ | 2–5 min | ≤ 0.5 GB |
| **Total (est.)** | | **~1.6×10⁹** | **≈ 30–75 min** | **≤ 2 GB** |

**HARD CAP (binding):**
- One CPU process on the box. No GPU and no neural network.
- **≤ 4 hours total wall-clock** across all items.
- **≤ 1 hour per item.**
- **≤ 8 GB resident memory.**

**On reaching the cap:**
- Stop that item.
- Record UNRESOLVED-COMPUTE (an engineering outcome, not a scientific result), and diagnose.
- Do **not** reduce horizons, cost grids or variants in place. Any such change is a new spec version (Astra edit 7: "Engineering failures require diagnosis; scientific criterion changes require a new version").

## 6. Outputs, sealing and replay

1. Before execution: hash this spec and the code tree into a manifest.
2. Results are written as exact rationals (as strings) in JSON, with the spec sha.
3. The independent replay (§5) must agree exactly on every compared quantity. A disagreement is an integrity failure that needs diagnosis.
4. No result is used to retune W-REL rates, costs or horizons. Any change after results are seen is a new version, labelled as informed by those results.

## 7. What this check can and cannot establish

**Can establish:**
- history-level source identifiability, or its failure, under W-REL-B;
- exact finite-horizon VOI;
- the performance of the named rivals;
- whether the proposed criteria separate an assessment variable from a policy-minimal machine **for these analytic agents**.

**Cannot establish:**
- any learned assessment (no Q-LEARN);
- causal use in a learned system (no Q-CAUSE);
- reduction against unnamed controllers;
- C4 status.

## 8. Approval (PENDING)

| item | value |
| --- | --- |
| What needs approval | Execution of §§1–6: bounded exact finite-horizon calculations under the hard cap. |
| Status | **PENDING. Not requested by this document and not run.** |
| Required | Aidan's explicit approval, under the solver-approval precedent (C4-CMP1, Ruling R-A2) and Astra #21. |
| Before approval | Nothing in §§1–6 is executed. The only computation done so far is `plan_counts.py`, a sizing count of distinct likelihood ratios that evaluates no policy or value. |

Proposed approval question, consult #21, verbatim:

> "Approve a theory-only C4 admission and identifiability study of W-REL, including bounded exact finite-horizon calculations of source identifiability, costly exploration and the named conventional control rivals? The analysis specification and compute limit will be fixed before execution. This approval excludes neural training, an exhaustive all-controller certificate, new architecture families, protected controllers or registers, and any claim that C4 or consciousness has been demonstrated. A later empirical C4 study would require separate approval."

**Sizing artifacts:**

| file | sha256 |
| --- | --- |
| `/workspace/scratch/c4_reliability/plan_counts.py` | 7c9abc8b7f0745589043f7536ffd5abd4f95688c6a36eff8619c4d2c88663391 |
| `/workspace/scratch/c4_reliability/plan_counts.log` | c18a1b2f8c64b9cda70e59e4718978725aa28584972b249e5d4389d37fdf7d9b |

**Correction to the raw log.** The log line labelled "cumulative" is actually the per-layer count C(T+10, 10). The cumulative counts used in §5 are C(T+11, 11): 352,716 at T = 10 for H0.
