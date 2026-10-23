# ACI decision package v1: amended two-stream world admission (analytic, Stage A only)

**DRAFT FOR AIDAN'S DECISION. NOT A FREEZE. NOT AN AUTHORIZATION.** Prepared 2026-10-20
(EDT) from a read-only audit of HEAD `32cfbe6` (see `/workspace/aci_frontier_audit.md`).
Nothing in this package has been computed. It is classified **ANALYTIC** under
`ACI_RESEARCH_CONSTITUTION_v3.md`.

## 0. The decision requested

Approve, amend or reject one bounded analytic step: the two-stream world-admission
enumeration from `ACI_NEXT_EXPERIMENT_DECISION_v1.md` (kanban #38), with three amendments
fixed **before** any computation:

1. **Reclassify signature (iv) as an identity check.** "Marginals + covariance match the
   joint filter" is guaranteed algebraically, as §2 shows. It verifies the implementation
   and is not admission evidence.
2. **Write the frozen generator and signatures as a hashed protocol/manifest** before the
   enumeration. The original package demands this but no file exists yet.
3. **Record the 2026-10-02 deletion (78 protected files, commit `d0ee2bb`) before the run.**
   Either restore the files additively or note them in errata, so the run's preservation
   inventory isn't born failing.

Two separate approvals, which this package does not request:
- **SUB_A0** (options 1/2/3 in `SUB_A0_CAL_RESULTS_v2.md`). SUB_A0 stays parked unless you
  choose.
- **Reviewing and merging SCARCITY_GAP_v1** (branch `elminster/loving-ptolemy-ityj4l`).

## 1. Why this rather than a "sharper" discriminator

I considered three cheaper or sharper alternatives:

| Candidate | Sharper? | Cheaper? | Why not chosen now |
| --- | --- | --- | --- |
| Two-stream admission, amended (**recommended**) | Modest. It only tests whether the *world* has consequential joint/history headroom. | Yes: seconds of exact rational arithmetic, no solver. | Already designed, on the board and awaiting you. Lowest risk. |
| SCARCITY_GAP §7.1 graded-evidence certificate (agent capacity K below sufficiency) | **Yes.** It targets the regime where agent-referent variables (selection, access, self-induced uncertainty) can be non-redundant. The audit confirms every closed study ran at or near sufficiency (`PHASE3_VERDICT_v1.md` §4; `C1_RELIABILITY_DISPOSITION_v1.md`; R10 penalty 0.0205 ≈ the 0.02 margin). | No. It needs exact bounded-optimal encoder search (branch-and-bound), which is solver-like and carries A6-style timeout/UNRESOLVED risk. | Unmerged and unreviewed. Its own certificate shows small effects (max access value 1/24), a K = 2^j alignment artifact, and brute-force coverage only for K ≤ 3. The graded extension's signatures are not yet frozen-ready. |
| SUB_A0 option 2 (sign-coded substrate) | Not for the C-axis | No: recalibration plus later training | A separate line with its own pending decision; needs explicit approval. |

**My judgment:** run the cheap, already-designed admission as Stage A. Pre-register that
its only informative signatures are (i)–(iii). Treat a capacity-bounded (ρ < 1) variant of
the **same frozen world** as the leading candidate for Stage B, to be designed only after
Stage A and a review of SCARCITY_GAP. This keeps one fixed world and puts the sharper
question on an admitted benchmark rather than a toy.

## 2. Evidence base (frozen)

- **A6 is UNRESOLVED and R9 optimization is departed**, so the package's UNRESOLVED branch
  applies (`A6_GATE_DECISION_v1.md`; `ACI_NEXT_EXPERIMENT_DECISION_v1.md`, decision table).
- **The synthesis names "first-order cognitive identifiability" as the next frontier**,
  not another workspace, confidence head or self-vector (`ACI_RESEARCH_SYNTHESIS_v1.md`,
  "Surprise review").
- **The C2/C3 gap:** there is no competent acquired multi-consumer cognition. In III-B,
  S2 always abstained, S3 was near chance, and there were 0/1,024 state-dependent switches
  (`PHASE3B_VERDICT_v1.md`; `PHASE3B_H10_DIAGNOSTICS_v1.md`).
- **Why (iv) is an identity:** a two-binary-factor law has 3 free parameters, and
  (pX, pY, cov) is a bijective reparameterization of it. The joint Bayes update is closed
  in that parameterization. A "strong reduction" pass is therefore certain.

## 3. Strongest rival

The full joint four-state Bayes filter. Equivalently, an ordinary 3-number sufficient
state (marginals + covariance), which is the constitution's own reduction anchor. Weaker
rivals: factorized marginals, current-observation-only, and a direct-history table charged
for storage.

## 4. Prospectively falsifiable question

In the frozen world:
- Hidden (X, Y) is uniform.
- C~Bern(1/5), Dx~Bern(1/50), Dy~Bern(1/40); X' = X⊕C⊕Dx, Y' = Y⊕C⊕Dy.
- 8 alternating BSC(1/5) observations; observe, then transition.
- Terminal Brier scores on X, Y and XOR; 256 histories.

The question: **is there consequential first-order history and joint (XOR) information
that a factorized estimate loses?** The admission signatures, frozen before computing,
are:
- **(i) History:** current-only has strictly positive exact excess Brier over the full
  oracle.
- **(ii) Joint headroom:** factorized XOR Brier excess ≥ 1/1000.
- **(iii) Selective content:** zero-covariance substitution, with marginals,
  normalization, observation and query preserved, shifts the XOR forecast by ≥ 1/20 on
  ≥ 1/4 of history mass. X and Y forecasts must stay exactly unchanged, and every state
  must remain in the simplex.
- **(iv) Identity check, not evidence:** marginals + covariance reproduce joint forecasts
  and updates exactly.

## 5. Cheapest apparatus

- One stdlib `fractions` enumeration of 256 histories with exact rational forward
  filtering.
- One independent integer-numerator replay, written separately.
- No solver, sweep, learner, gradient or simulation.
- Outputs: a hashed protocol/manifest, an exact certificate (normalization, risks per arm,
  intervention mass, simplex audit, storage/precision charges), the replay comparison, and
  a short disposition.

## 6. Costs

| Item | Estimate |
| --- | --- |
| Compute | Seconds to about a minute of CPU (256 × 8 steps over 4 rational states, plus replay). Negligible. |
| Agent time | Roughly 1 session to write the protocol, 1 to execute, replay and report. |
| Human time | One approval now; one review of the result and the Stage B decision. |
| Risk | Low. The main scientific risk is an uninformative outcome (admission passes but says little about mechanisms), which the claim ceiling makes explicit. |

## 7. Outcomes and consequences

| Outcome | Condition | Consequence |
| --- | --- | --- |
| **PASS** | (i), (ii), (iii) all hold; (iv) identity verified; independent replay agrees exactly; simplex audit clean. | The world is admitted as an interpretable first-order benchmark with an ordinary 3-number sufficient state. **Next human decision:** design Stage B (the capacity-bounded ρ < 1 variant of this world, after a SCARCITY_GAP review) **or** a prospective Q-LEARN protocol. Each needs separate approval. No neural run is licensed. |
| **FAIL** | Any of (i)–(iii) misses its threshold. | Reject this world under this protocol. Do **not** retune noise, horizon or flip rates. Any successor world needs an additive rationale and a new human gate (per the original package). |
| **UNRESOLVED** | The replay disagrees, normalization or simplex fails, or the implementation is defective. (Exact arithmetic cannot time out.) | Fix the implementation additively and re-replay. No reinterpretation and no threshold change. A second defect parks the node. |
| *(iv) fails* | Marginals + covariance ≠ joint. | This would indicate a code bug, since the identity is mathematical. Treat it as UNRESOLVED, not as evidence. |

## 8. Claim ceiling

At most: *this exact world has identifiable first-order history and correlation
consequences, realized by an ordinary sufficient state.*

It does **not** establish any of the following:
- learned acquisition or neural competence;
- a minimum number of neural coordinates;
- workspace, integration or C3 necessity;
- C4/C5/C6;
- organizational autonomy (any O layer);
- anything about the agent-referent or scarcity regime, because this world runs at
  sufficiency;
- consciousness or any C7 inference.

## 9. Thirteen admission answers (constitution v3)

| Q | Answer |
| --- | --- |
| Q1 | Bounded C2/C3 prerequisite: an identifiable first-order world for later acquired-cognition work, without reopening R9 (`ACI_NEXT_EXPERIMENT_DECISION_v1.md`). |
| Q2 | Does this frozen two-stream world carry consequential history and joint (XOR) predictive information beyond a factorized or current-only estimate? |
| Q3 | (i), (ii) or (iii) missing its frozen threshold falsifies admission. Replay or simplex failure defeats the conclusion as UNRESOLVED. |
| Q4 | The joint Bayes filter, equivalently the 3-number marginals + covariance state, is the reduction anchor. Rivals are matched on observations, timing, queries and targets. |
| Q5 | A6 UNRESOLVED requires departing R9 for an identifiable first-order question. III-B never achieved competent acquired multi-consumer use, so a benchmark whose headroom is certified *before* learning is needed (the R10/R10A lesson). |
| Q6 | After PASS: decide Stage B (ρ < 1 capacity axis on the same world) or a Q-LEARN protocol. Both are separately gated. |
| Q7 | After FAIL: reject the world with no retuning; the next world needs a new rationale and gate. After UNRESOLVED: additive fix and replay only. |
| Q8 | Analytic proof by exact finite enumeration plus an independent replay. No neural or organism model. |
| Q9 | Substrate/world competence prerequisite. Not organizational cognition and not an engineering advantage. |
| Q10 | See §8. Exact first-order facts of one finite world, with an ordinary sufficient realization. Nothing learned, neural, organismal or C4+. |
| Q11 | C2 (first-order content) and C3 (joint availability) prerequisites. Acquisition, multi-consumer competence and every C4+ layer remain unsupported. |
| Q12 | None directly: O0 throughout, since generator, evaluator and arithmetic are supplied. The O3 arrows are not addressed (`ACI_NEXT_EXPERIMENT_DECISION_v1.md`, final section). |
| Q13 | PASS: "first-order joint content is consequential here and ordinarily realizable", which makes this world the fixed testbed for a scarcity or learning test. FAIL: "a two-factor common-flip world at these rates is not a discriminating benchmark". UNRESOLVED changes no belief. |

## 10. Exact approval wording I would act on

> "Approved: write and hash the amended two-stream admission protocol (signatures
> i–iii, iv as identity check), then run the single exact enumeration plus independent
> replay, report, and stop. [Restore | record-in-errata] the d0ee2bb deletion first."

Anything broader, including Stage B, SUB_A0, merging SCARCITY_GAP or any learner, needs
its own explicit approval.
