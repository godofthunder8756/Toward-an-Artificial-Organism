# Learned assessment of internal processing reliability with costly rechecking: C4 admission and identifiability (v2, theory only; additive revision of DRAFT v1 after Astra consult #21)

**Status.** v2 for Astra review. Written 2026-10-21, about 4:25–4:55 AM ET, by the Research Delegate executor for the ACI Research Specialist, for Aidan Ahern.

**Card class.** ANALYTIC / admission-criteria (constitution v3). It authorizes no experiment.

**Relation to DRAFT v1.**
- This is an **additive** revision.
- `c4_reliability_assessment_admission_DRAFT.md` (sha256 dd463a2dfae6f93c07736d708ecc92b251d57481f72a63e893241703dc05523c) is left untouched and remains the record of what was submitted to consult #21.
- Sections below either replace the corresponding DRAFT section (marked **[replaces DRAFT §x]**) or are new (marked **[new]**).
- A change log is in §12.

**Astra edit 8 (verbatim).** This is **theory about C4 admission**, not evidence that the work is "below C4 throughout." It authorizes no empirical study and establishes no C4 status.

**What this document asserts.** It makes no C4, C5 or consciousness claim. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate and labelled at every use.

**Work done.**
- No training, no repo changes, no new computation of results.
- The binary-regime rates adopted in §1 are exactly the DRAFT S and E pairs, so every DRAFT exact value carries over unchanged (§2, Appendix A). No exact-fraction re-check was needed, and none produced a changed number.
- The bounded exact check is specified, **not run**, in the companion file `c4_reliability_exact_check_spec_draft_v1.md`. It is PENDING Aidan's approval (§11).

**Approvals.**
- Constitution v3: "Human authorization is required for … first C4/C5/C6 studies".
- Consult #21: "Do not yet train a GRU or attempt an all-controller certificate."
- Any later empirical C4 study requires separate approval.

---

## 0. Sources, construct and the Q1 ruling [replaces DRAFT §0, final paragraph; DRAFT §0 sources otherwise retained]

The DRAFT §0 sources are retained: the C4 row, ACO C4, the Astra #3 conjunction, consult #16, consult #20 and the §3.2 precedent.

**Consult #21, Q1 ruling (verbatim):** "an ordinary Bayes filter can instantiate a C4-relevant functional role. "REDUCED to a conventional mechanism" does not automatically mean "classified C3." ORIGIN, ROLE and REDUCTION must remain separate."
- "If the rival reproduces the observations **without the proposed evaluation role**, the tests have not identified that role."
- "If the rival itself satisfies the referent and selective-causal criteria, reproduction identifies an ordinary implementation of the role. It does not disqualify the role."
- "Matching reward or checking behaviour alone does not establish either conclusion."
- "The earlier statement that a persistent reliability belief is insufficient still stands. It does not imply that every causally dissociable reliability-assessment process must be C3."

**Consult #21 verdict (verbatim, opening):** "REVISE. W-REL establishes a useful static decision problem and remains a plausible C4 candidate. Its present criteria do not yet distinguish assessment of the learner's own predictions from source-dependent information acquisition…"

**The construct (revised; Astra Q2).**
- The **locus** of unreliability (own designated processing channel versus evidence) is retained as a useful experimental variable. It is **not sufficient** as the construct.
- The construct is an assessment whose content **predicts the learner's actual conditional correctness**: whether the learner's own first-order prediction, at a named stage, will be correct under each available check.
- Consult #21, Q2 (verbatim): "Require the assessment content to predict the **learner's actual conditional correctness**, naming the prediction and processing stage being assessed. Bayes-optimal checking gain is not interchangeable with the learned predictor's correctness gain. Wrong checking actions alone are not sufficient evidence of second-order false alarms and misses."

**Route to C4 relevance** (consult #21, closing, verbatim): "Its route to C4 relevance is a defensible causal evaluation role, not failure of an ordinary Bayes explanation."

---

## 1. World W-REL-B: binary persistent regime (illustrative; nothing frozen) [replaces DRAFT §1]

**Astra Q8 (verbatim world block):** `Z_t in {S, E}, with a specified persistent transition law. S uses (w,e) = (1/20, 1/5). E uses (w,e) = (1/5, 1/20).`

**Per trial t** (the DRAFT §1 steps, with the regime Z_t replacing (I_t, E_t)):
1. X_t is uniform.
2. Evidence bits are b_{t,i} = X_t ⊕ W_{t,i}, with W ~ Bern(w_{Z_t}) and n = 3.
3. **Designated processing channel** F reads y_{t,i} = b_{t,i} ⊕ N_{t,i}, with N ~ Bern(e_{Z_t}).
4. Action:
   - PREDICT;
   - RECHECK (cost c_r): the same b_t, re-read with fresh internal noise, giving y′_t;
   - RESAMPLE (cost c_s): fresh world bits, read once, giving y″_t.
5. The learner outputs its first-order prediction p̂_t.
6. Feedback: the outcome and the realized cost. Reward = 1[correct] − cost.

**Regime.**
- S, "system-dominant": internal noise dominates.
- E, "evidence-dominant": world noise dominates.
- In both, ε = w + e − 2we = 23/100.
- **Transition law (illustrative; to be fixed before any execution):**
  - H0: static within an episode, h = 0.
  - H1: symmetric persistent switching with hazard h = 1/20.
  - In both, P(Z_0 = S) = 1/2.

**Costs** are visible inputs to the learner and to **every rival** (§4). There are no categorical cost bins.

**What the learner does not receive:**
- Z_t;
- fault labels;
- oracle confidence;
- the Bayes posterior;
- any supplied reliability register;
- any per-read correctness signal.

**The four-state version.** The DRAFT four-state world (I ∈ {ok, faulty} × E ∈ {clean, noisy}) is **withdrawn from the admission design**. It "can remain a later extension requiring its own history-level audit" (consult #21, Q8).

### 1.1 Referent: the designated processing channel (Astra Q3)

The supplied front-end F is admissible as "the designated processing channel". However, consult #21 (verbatim): "Calling it part of the body does not by itself make its estimated reliability second-order evaluation. An otherwise identical external sensor can generate the same observations."

**Consequence.** Channel identity alone earns nothing. The C4-relevant content must be the §3 assessment of the learner's **own conditional correctness**. A belief about F's reliability counts only through that.

### 1.2 History-level symmetry: lemma L1 (Astra edit 5; analytic, to be verified exactly)

**Lemma L1.** Under W-REL-B with any transition law for Z, any policy that depends only on observable history, and any history containing **no RECHECK observation**, the likelihood of the history is the same for every Z path. Hence P(Z_t | history) equals the prior propagated by the transition law.

**Proof sketch.** Given Z_t, each trial's emission is independent of the past. Policies are functions of observables, so action-probability factors cancel in the posterior. The per-trial emission laws of (X, y) and of (X, y, y″) are identical in S and E: TV = 0 exactly (D1). That follows because each of these reads has independent world and internal flips with per-read flip probability ε. So every non-RECHECK factor is constant in Z_t, and the likelihood is constant in the Z path.

RECHECK is the only informative event. It factors through 10 distinct S/E likelihood-ratio classes (sizing count, `plan_counts.py`).

**Status.** This is an analytic proof. Its exact verification (spec §1, A-SYM) is **pending approval and not run**. The single-trial statement in DRAFT D1, "no learner can distinguish…", is **not** carried into the persistent setting except through L1 (Astra edit 5).

---

## 2. Pre-training demonstration: scope narrowed [replaces DRAFT §2 interpretation; values unchanged]

**Astra edit 2 (verbatim):** "The illustrative single-trial construction demonstrates identical default predictive information with different values of alternative checks. It establishes pressure for source-dependent information acquisition. It does not establish assessment of the learner's own representation, history-level source identifiability, or acquired evaluation."

**Values.** All DRAFT D1–D5 exact values are **unchanged**, because S and E are the same (w, e) pairs (Appendix A):
- TV(X, y) = 0 and TV(X, y, y″) = 0.
- TV(X, y, y′) = 2762073/6400000.
- Per-bit recheck agreement: 17/25 (S) versus 181/200 (E).
- Split-state recheck gain: 3456/44275 (S) versus 9747/1416800 (E).
- Resample gain: 47817/500000 (both).
- D3 gap: 59568279/10^10.
- D5 post-check posterior gap: ≤ 0.0987, with 0/64 decision changes.

**D3 scope (Astra edit 2).** D3 is a **one-trial comparison against a regime-blind policy**. It is not a bound against adaptive controllers. Finite-horizon values against adaptive controllers are spec §2–§3 (pending).

**D4 scope.** In the single trial, the S/E information is available only through RECHECK. At history level this rests on L1 (§1.2), which is proved analytically and pending exact verification.

**D5** (the post-check precision role) is retained. It now feeds the second category of §5.2 rather than being set aside.

---

## 3. Assessed object and assessment content [replaces DRAFT §3]

**Astra edit 3 (verbatim):** "The assessed object, prediction time and correctness criterion must be specified. Candidate assessment content must predict the learner's own conditional performance, not merely the Bayes oracle's performance. False alarms and misses must concern that assessment and track manipulated assessment content while the declared first-order controls hold."

**Specification (proposed).**
- **Assessed object:** the learner's own first-order prediction p̂_t for trial t, at two stages:
  - (i) the **pre-check prediction** p̂⁰_t, read from the first-order head on y_t before the action;
  - (ii) the **post-check prediction** p̂ᵃ_t, from the same head after action a ∈ {PREDICT, RECHECK, RESAMPLE} and its observation.
- **Prediction time:** the assessment is read at the action decision for trial t, after y_t and before any check observation.
- **Correctness criterion:** K_t(a) = 1[sign(p̂ᵃ_t − 1/2) = X_t], the learner's own post-action correctness. A log-loss variant is reported separately.
- **Assessment content A_t:** a state component whose content predicts **E[K_t(a) | learner state] for each a**. The comparison is the learner's own counterfactual conditional correctness, not the Bayes oracle's.
  - For non-taken actions, K_t(a) is obtained in analysis only, by world-side replay of the same trial with a fixed noise seed. This is analysis apparatus, not an agent register.
- **Distinct from the locus.** A_t may be implemented through a belief about Z. The criterion is prediction of own correctness. Bayes-optimal checking gain is a reference only, "not interchangeable with the learned predictor's correctness gain".
- **Second-order false alarms and misses.**
  - False alarm: A_t predicts low own correctness (or high RECHECK gain) when the learner's actual K_t is high.
  - Miss: the converse.
  - These are scored against the learner's own K_t, and must track manipulated A_t under §5.
  - Wrong checking actions alone do not count.

**Traps carried from Astra #3:** "Detachable head makes lesionability trivial"; "update closure != second-order status".

---

## 4. Rivals (costs visible to all) [replaces DRAFT §4]

**Information set.** Every rival receives:
- y, y′ and y″ when taken;
- outcomes;
- **the current costs (c_r, c_s) as continuous visible inputs**;
- the same action set and the same intervention set.

Consult #21, Q6 (verbatim): "Give every rival the visible costs; do not manufacture separation by withholding them or forcing categorical cost bins."

**Resource ledger (Astra Q7).** "Memory units are not bits. A fair resource ledger must specify state precision, policy parameters, computation, model constants and supplied buffers. Until then, "same-resource ALL(B)" is undefined."

Each rival is reported with its own ledger: state precision, state variables, policy parameters, computation per step, model constants supplied, and supplied buffers. Matched-resource comparisons are **not** claimed until the ledger is defined.

### 4.1 R-CONF (restricted)

R-CONF-S and R-CONF-A are as in DRAFT §4.1, except:
- costs are continuous inputs;
- there are no "per cost bin" thresholds;
- the rule is a cost-general map a(s_t, c_r, c_s).

**Impossibility statement, restricted (Astra Q6).** The statement that R-CONF cannot separate S from E holds **only for the demonstrated information set**: an analytic P(X | y) confidence head with adaptation from default-prediction errors. By L1, that information is Z-independent at history level too.

Consult #21 (verbatim): "A learned confidence head may carry historical information that an analytic `P(X|y)` head does not." A learned confidence head with history is therefore **not** covered by the impossibility statement. If it uses recheck agreement or post-check outcomes, it is classified as R-HAC or R-CG (§4.2).

### 4.2 History-dependent and cost-general rivals

- **R-CG, the cost-general controller [new; the decisive conventional rival].**
  - Astra Q6 (verbatim form): `action_value(a) = estimated_correctness(a, history) - current_cost(a)`.
  - Its estimated_correctness estimates its **own** post-action correctness from history: for example, counts per (action, read class), a learned regressor, or a filter.
  - It re-optimizes immediately under any visible cost.
  - R-CG's estimated_correctness is itself a candidate implementation of the §3 role. Whether it satisfies the role is a ROLE question, and reproduction by it is recorded under REDUCTION (§8).
- **R-HAC-MB (non-myopic) [revised].** Astra edit 6 (verbatim): "R-HAC-MB uses the posterior over the specified latent process and a policy accounting for both immediate reward and future information value over the declared horizon. A myopic version is reported separately."
  - Here R-HAC-MB is the exact finite-horizon POMDP optimum over Z.
  - **R-HAC-MB-myopic** is the same filter with greedy one-trial selection, reported separately.
  - Consult #21 (verbatim): "A Bayes filter followed by myopic action selection is not generally the optimal controller when rechecks inform future trials."
- **R-HAC-MF (retained as secondary).** As in DRAFT §4.2, with continuous cost inputs.
  - Consult #21 (verbatim): "R-HAC-MF is too narrow to serve as the decisive conventional rival."
- **R-HAC-ALL(B): REMOVED as a gate.** Consult #21, Q7: "Do not require an R-HAC-ALL certificate before training". It is undefined until the resource ledger exists. "A bounded exact analysis of the world and named rivals is valuable." That analysis is the companion spec.

### 4.3 I-COST (demoted)

Consult #21 (verbatim): "I-COST remains useful as a generalization probe, not a decisive evaluation-role discriminator." I-COST results are reported, but are not a C-RED criterion.

### 4.4 Expected reduction status (stated before any computation) [replaces DRAFT §4.4]

- R-HAC-MB (non-myopic) and plausibly R-CG implement a correctness-or-source assessment by construction.
- A learned system approaching optimal value may be reproduced by either. Under the Q1 ruling, that is recorded under **REDUCTION** and is **not** a C3 classification by itself (§8).
- Whether the §5 criteria distinguish an **assessment** variable from a **policy-minimal** machine that reproduces the checking policy without cost-general correctness content is an open identification question. It is computed for the analytic agents in spec §4 (pending).

---

## 5. Interventions and causal criteria [replaces DRAFT §5]

### 5.1 Intervention set (identical for candidate and rivals)

| Id | Intervention |
| --- | --- |
| I-SYS / I-EVID | Force Z_t = S or Z_t = E at a declared time. The pair is matched on default first-order information exactly (D1, L1). |
| I-SWAP | Replace the candidate's assessment content with its value from a donor history, specified independently of evaluation outcomes (§5.3). |
| I-CORRUPT | Clamp the assessment content to a prespecified value. |
| I-RESCUE | The credited rescue **must reverse the assessment-dependent downstream consequence in the declared causal procedure**. Restore-and-rerun identity is an integrity check only (Astra Q5). |
| I-COST | Generalization probe only (§4.3). |
| I-HEAD | Action-head lesion. Recorded, not credited. |

### 5.2 First-order controls: three categories; tolerances illustrative (Astra Q4, edit 4)

**Astra edit 4 (verbatim):** "C-FO establishes preservation only over the prespecified first-order probe battery. Output preservation alone is not described as preservation of the full first-order state. Direct inference effects under matched subsequent observations are reported separately and constrain the dissociation claim."

The three effects are separated and reported separately (consult #21, Q4):
1. **Downstream prediction changes caused by selecting different checks.** These are expected consequences of the intervention, and are reported.
2. **Direct prediction changes under identical check observations.** The intervention changes p̂ᵃ given the same y and y′ (the D5 precision route). "The second category limits the dissociation claim; it cannot simply be declared irrelevant."
3. **Changes in checking while a prespecified first-order probe battery is preserved.** The battery is the pre-check p̂⁰ on every read pattern × a fixed history bank. Only this category supports C-SEL, and only to the extent category 2 permits.

**Tolerances: ILLUSTRATIVE, not proposed for freezing.** δ_p = 0.02, δ_acc = 0.005 and δ_LL = 2% are retained as placeholders only. Consult #21 (verbatim): "A maximum probability change of 0.02 can matter substantially to checking decisions; the demonstrated whole-trial value gap is only about 0.006. Freeze margins only after determining whether tolerated prediction changes could explain the checking effect."

Margins are to be derived later, from the decision sensitivity of each named rival to tolerated p̂ changes (open question 4).

### 5.3 Identifying assessment content (Astra Q5) [replaces DRAFT §5.3]

**Target.**
- The DRAFT decoder target (the posterior over the internal-fault factor alone) is withdrawn as incomplete.
- The analysis-only reference is the **posterior over the specified latent process**, P(Z_t | history). In W-REL-B this is complete for the latent process.
- The construct-level target is **the learner's own conditional correctness E[K_t(a) | history] per action** (§3).
- Both are disclosed as analysis-only oracles, never training signals.

**Requirements.**
- Held-out identification.
- Rank and stability checks: subspace dimension, and stability across splits and seeds.
- Donor controls: random-donor, same-belief-donor and first-order-matched donor.
- Intervention specifications fixed **independently of the evaluation outcomes**.

Consult #21 (verbatim): "Decoder accuracy alone does not validate the transplant direction".

### 5.4 Criteria

- **C-REF (referent).** Under I-SYS versus I-EVID, checking propensities diverge in the predicted directions, beyond prespecified margins.
- **C-T2 (type-2 content).**
  - A_t predicts the learner's **own** conditional correctness K_t(a) per action, better than pre-check confidence s_t does, with a prespecified margin.
  - False alarms and misses are scored against the learner's own K_t (§3), and track I-CORRUPT and I-SWAP.
- **C-SEL (selective causal content).** I-SWAP and I-CORRUPT produce directional assessment errors with the specified downstream checking consequence. This requires §5.2 category 3, constrained by category 2, and a credited I-RESCUE as in §5.1.
- **C-FO.** Preservation over the prespecified probe battery only (edit 4).
- **C-RED (REDUCTION, recorded, not a pass/fail gate on ROLE).** The whole pattern is compared with R-CONF-S/A, R-CG, R-HAC-MB (non-myopic and myopic) and R-HAC-MF, each with its own resource ledger.

---

## 6. Claims kept separate [replaces DRAFT §6]

| Claim | What it would need | Allowed wording (template) | Forbidden |
| --- | --- | --- | --- |
| **Q-EXIST (world)** | D1–D5 (exact) and L1 (analytic; exact verification pending) | "W-REL-B at the illustrative rates has identical default predictive information across S and E and different values of alternative checks; this establishes pressure for source-dependent information acquisition." | "assesses its own representation"; "history-level identifiability shown" before A-SYM is run; any statement about a learner |
| **Q-LEARN (ORIGIN)** | A learner trained on outcomes and costs only acquires content meeting C-T2 (§3), under prespecified identification (§5.3) | "acquired state predicting its own conditional correctness under [criteria]" | "acquired an evaluator / metacognition / self-model"; acquisition from a decoder alone. A supplied assessment blocks an acquisition claim, not automatically the functional-role claim (edit 1). |
| **ROLE** | C-REF + C-T2 + C-SEL + C-FO + credited rescue | "the identified content performs the declared evaluation role under [interventions], with first-order controls over [battery]" | "full first-order state preserved"; crediting I-HEAD or restore-and-rerun identity |
| **REDUCTION** | Whole-pattern comparison with named rivals and ledgers | "reproduced / not reproduced by [named rival] with [ledger]"; "an ordinary implementation of the role" | "irreducible"; "beats all controllers"; "therefore C3" from reproduction alone |
| **Q-NECESSITY** | Out of scope beyond D3 (one-trial, against regime-blind) and spec §2 VOI | "regime-blind policies are strictly suboptimal in the one-trial construction" | "assessment is necessary" relative to adaptive controllers |
| **C-level** | Astra ruling | "theory about C4 admission; no C4 status is established" | any C4, C5, consciousness, self-awareness or organism claim |

---

## 7. Falsifiers and negative outcomes [replaces DRAFT §7]

**Astra edit 7 (verbatim):** "Decoder or intervention failure means the proposed content was not identified or causally dissociated by this procedure. It does not establish absence of assessment. A failed C4 test does not itself establish a C3 role; only independently supported lower-level claims are retained."

**Falsifiers:**
- **F-W1 (world).** D1 fails at the frozen rates, or no positive check-value gap exists. There is no post-hoc retuning.
- **F-W2 (history-level) [new].** A-SYM (spec §1) finds a non-RECHECK history with Z-dependent likelihood. L1 is then false, and the persistent-world identifiability claim is withdrawn.
- **F-L1 (Q-LEARN).** C-T2 is not met. The reading is "not identified by this procedure", not an impossibility claim.
- **F-C1 (ROLE).** C-SEL fails, or category 2 explains the checking effect. The reading is "not causally dissociated by this procedure".
- **F-REF.** I-SYS and I-EVID give indistinguishable checking responses. The referent is not supported.
- **F-ID [new].** The causal criteria do not separate an assessment variable from a policy-minimal machine (spec §4, DOES-NOT-SEPARATE). The criteria are then insufficient as stated, and must be revised under a new version before any empirical study.

**Engineering versus scientific.** Engineering failures (replay disagreement, compute cap, decoder instability) "require diagnosis; scientific criterion changes require a new version" (Astra edit 7).

---

## 8. Classification rules: ORIGIN, ROLE and REDUCTION kept separate [replaces DRAFT §8 "C3-fallback rule"]

**Astra edit 1 (verbatim):** "Reproduction by a conventional rival is recorded under REDUCTION. It disqualifies the proposed role only when it shows that the observations and interventions do not identify that role. A conventional implementation satisfying the role criteria may provide C4-relevant functional evidence; its ORIGIN is recorded separately."

**Recording rules:**
1. **REDUCTION is recorded per named rival** (R-CONF-S/A, R-CG, R-HAC-MB, R-HAC-MB-myopic, R-HAC-MF), with its ledger.
2. **Reproduction by R-HAC-MB or R-HAC-MF** is recorded under REDUCTION.
   - If the reproducing rival itself satisfies C-REF, C-T2 and C-SEL, the result is "an ordinary implementation of the role". It does **not** disqualify the role.
   - If it reproduces the observations **without** the role (for example, a policy-minimal machine), the tests have not identified the role (F-ID).
3. **ORIGIN.**
   - SUPPLIED versus ACQUIRED is recorded separately.
   - A supplied assessment blocks an **acquisition** claim, not automatically the functional-role claim.
   - A dedicated head supplies a **decomposition**, not necessarily its learned content.
4. **C3** is recorded only for independently supported lower-level claims, for example C3 history integration shown by its own criteria. It is never recorded merely because a C4 test failed or because a conventional rival reproduced behaviour.
5. "Matching reward or checking behaviour alone does not establish either conclusion" (Q1).
6. The §3.2 precedent stands: "a persistent reliability belief is not, by itself, distinct evaluation". Under the Q1 ruling, this "does not imply that every causally dissociable reliability-assessment process must be C3".

**Removed from the DRAFT:**
- The automatic "classify as C3" list.
- The DRAFT default that labelled R-HAC-MB reproduction as reduced-and-C3 with an annotation.
- The note that a C4 row may be unreachable.

Consult #20 still applies: "Do not assign C4 merely because the task includes checking, confidence or internal faults."

---

## 9. Thirteen admission answers [replaces DRAFT §9]

1. **Q1. Question.** C4 admission and identifiability. Can an assessment that predicts the learner's own conditional correctness under alternative checks be defined, identified and causally tested in W-REL-B? The test must hold first-order controls over a declared battery, and ORIGIN, ROLE and REDUCTION must be recorded separately.
2. **Q2. Hypothesis or question.** ONE question, theory stage:
   - Does W-REL-B admit history-level source identifiability only through rechecks (L1)?
   - What is the finite-horizon VOI?
   - Do the §5 criteria separate an assessment variable from a policy-minimal checking machine, for the named analytic rivals?

   All of this is pending under the spec. No learner question is asked now.
3. **Q3. Falsifiers.** F-W1, F-W2, F-L1, F-C1, F-REF and F-ID (§7).
4. **Q4. Strongest simpler explanation.**
   - R-HAC-MB (non-myopic) and R-CG, both of which may themselves implement the role.
   - Then R-HAC-MB-myopic, R-HAC-MF and R-CONF-S/A.
   - Each has its own resource ledger.
   - Precedent: M1 ≡ A_thr in W_sym (§3.2).
5. **Q5. Why it is necessary.**
   - Consult #20 named this the top next step.
   - Consult #21: "a plausible C4 candidate".
   - No frozen card tests own-correctness assessment with matched default information, costly self-generated identifying evidence, and a battery-based first-order control.
6. **Q6. On success** (at theory stage: L1 verified, positive VOI, SEPARATES).
   - Propose an empirical protocol; this requires separate approval.
   - No C4 status change.
7. **Q7. On failure or UNRESOLVED.**
   - F-W1 or F-W2: redesign under a new version.
   - F-ID: revise the criteria under a new version.
   - UNRESOLVED-COMPUTE or other engineering failures: diagnose. "Engineering failures require diagnosis; scientific criterion changes require a new version."
8. **Q8. Minimum apparatus.**
   - Done: single-trial exact demonstration.
   - Next, pending approval: the bounded exact finite-horizon check (companion spec), under a hard compute cap.
   - Not now: GRU training, and any all-controller certificate.
   - No organism model.
9. **Q9. Level.** Organizational cognition: an evaluation role versus checking policy under intervention. Reward is an engineering quantity.
10. **Q10. Ceiling.**
    - This document: "W-REL-B has identical default predictive information and differing check values; history-level identifiability holds by an analytic lemma pending exact verification."
    - **NOT established:** assessment of the learner's own representation; history-level identifiability (until A-SYM); acquired evaluation; any C4 status.
11. **Q11. C-level.** C4 admission theory (edit 8). Prerequisites not established: C2 acquired representation (PARTIAL), C3 integration (PARTIAL), and C4 Q-LEARN and ROLE (not started). No C5.
12. **Q12. O-level.** O0. F is a SUPPLIED designated processing channel. RECHECK is a modelled action. No O1–O3 claim.
13. **Q13. Belief change.**
    - Theory success: "the W-REL-B criteria can separate an own-correctness assessment from a policy-minimal machine for named analytic agents".
    - F-ID: "the criteria as stated do not separate assessment from checking policy".
    - UNRESOLVED: no change.

---

## 10. Dependency flags, ambiguities, open questions [replaces DRAFT §10]

### 10.1 Dependency flags (none adopted)

- **F1 (revised by Astra Q3).**
  - F is the designated processing channel, and faults need not enter learned weights.
  - Consult #21 (verbatim): "faults inside learned computation do not necessarily require a *protected* register: replay, charged storage or other unprotected implementations are possible. Any proposed implementation must account for its actual memory and control scaffolds."
  - A learned-computation-fault variant would need its replay or storage scaffold declared and charged.
  - **If** that scaffold had to be protected, that would be a protected register/controller dependency. It is **flagged, not adopted**.
- **F2.** The evidence retained for RECHECK is world-side, held for the trial. It is a supplied buffer and must appear in each agent's resource ledger.
- **F3.** Any learner would be trained by RL plus outcome prediction, which is a new training regime. Any training needs Aidan's explicit approval plus Astra clearance. None is requested here.
- **F4 (revised by edit 1).**
  - Locating content uses analysis-only oracles: P(Z | history) and own K_t(a) via world-side replay.
  - A dedicated head supplies a decomposition, not necessarily its learned content.
  - A supplied assessment blocks acquisition claims, not automatically role claims.
- **F5.** Costs are continuous visible inputs to all agents.
- **F6 [new].** The exact check is CPU-only rational arithmetic under a hard cap. It uses no new architecture family and no neural network.

### 10.2 Ambiguities (provisional)

- **A1 (revised).** The target is own conditional correctness per action. The locus (Z) is the experimental lever.
- **A2.** Matched default information means exact TV = 0 per trial, and at history level via L1.
- **A3 (revised).** First-order control uses the three §5.2 categories. Category 2 is reported and constrains the claim.
- **A4.** Uniform prior on X, and n = 3.
- **A5.** 0/1 reward minus cost. Under a scoring rule, category 2 becomes decision-relevant.
- **A6 (revised).** The ledger replaces "B bits".
- **A7 (revised).** The oracle targets are P(Z | history) and own K_t(a).
- **A8.** R-CONF-A adapts only from default-prediction errors. Anything using post-check information is R-HAC or R-CG.
- **A9.** Rates, costs, h and T are illustrative.
- **A10 [new].** K_t(a) for non-taken actions is defined by world-side counterfactual replay with a fixed noise seed.

### 10.3 Open questions for Astra (consult #22)

1. **Primary transition law.** Is H0 (static per episode, T ≤ 10) an acceptable primary "persistent transition law", with H1 (h = 1/20, T ≤ 5) secondary? Or is a genuinely switching law required as primary?
2. **Separation criterion.** Is the spec §4 test (policy-minimal machine PM_k versus non-myopic Bayes, under C-REF, C-T2, C-SEL and I-COST) the right formalization of "whether the causal criteria distinguish assessment from checking policy"? Which prespecified criterion set should define SEPARATES?
3. **Counterfactual correctness.** Is world-side counterfactual replay (A10) acceptable for defining own K_t(a) for non-taken actions?
4. **Margins.** How should margins be derived from rival decision sensitivity (§5.2)? Is a category-2 bound expressed in decision-flip probability acceptable?
5. **R-CG.** Do the proposed parameterization (count-based own-correctness estimates; 6 variants) and its exploration bonus β (charged and disclosed) suffice as the decisive conventional rival for the theory stage?
6. **Hard cap.** Is the cap acceptable: ≤ 4 h wall-clock total, ≤ 1 h per item, ≤ 8 GB, single CPU? Is UNRESOLVED-COMPUTE handled correctly, with no in-place reduction?

---

## 11. Approval: PENDING [new]

Status:
- The bounded exact check is **not run**.
- This document requests nothing on its own. The parent agent and the Specialist will put the question to Aidan.
- The only computation done since consult #21 is a sizing count (`plan_counts.py`).

Proposed approval question (consult #21, verbatim):

> "Approve a theory-only C4 admission and identifiability study of W-REL, including bounded exact finite-horizon calculations of source identifiability, costly exploration and the named conventional control rivals? The analysis specification and compute limit will be fixed before execution. This approval excludes neural training, an exhaustive all-controller certificate, new architecture families, protected controllers or registers, and any claim that C4 or consciousness has been demonstrated. A later empirical C4 study would require separate approval."

- Analysis specification and compute limit: `c4_reliability_exact_check_spec_draft_v1.md`.
- Prior approvals do not carry over.

---

## 12. C4-CMP1 mapping (Astra Q9) [new]

Both records are retained. Consult #21: "There is no requirement to execute the older design first."

| C4-CMP1 (W_ref) element | W-REL-B status |
| --- | --- |
| Referent: system versus evidence change, matched analytically (I4/I5) | **Addressed.** I-SYS/I-EVID with exact TV = 0 per trial (D1) and at history level via L1 (pending verification). |
| I1–I3 (evaluator content swap/corrupt/rescue) | **Replaced prospectively** by I-SWAP, I-CORRUPT and a credited I-RESCUE (§5.1), with the downstream-consequence requirement. |
| I6 / first-order preservation | **Addressed, revised.** §5.2 three categories; battery-only C-FO (edit 4). |
| Rates deliberately unset (R-A2) | **Retained.** All rates illustrative. |
| Own-correctness referent (type-2 content) | **Addressed, strengthened.** §3: the learner's own K_t(a). |
| Adaptive rival with the same information and resources | **Addressed, revised.** R-CG plus a ledger. "Same-resource" is undefined until the ledger exists. |
| W_ref-specific world structure and outputs | **Left open.** Not replaced; C4-CMP1 remains a separate design-only record. |
| Learned weights as the fault locus | **Left open.** F1, unprotected replay or storage allowed but charged. |
| Solver-like analytic step needing approval | **Addressed.** Companion spec, PENDING (§11). |

---

## 13. Change log versus DRAFT v1 [new]

| Change | Source |
| --- | --- |
| Four-state (I, E) → binary Z_t ∈ {S, E}; four-state kept as a later extension | Q8, edit 5 |
| Lemma L1 (history-level symmetry), analytic; exact verification pending | edit 5 |
| Demonstration scope narrowed; D3 one-trial only | edit 2 |
| Construct = own conditional correctness; assessed object, time and criterion named | Q2, edit 3 |
| Front-end = designated processing channel; channel identity earns nothing | Q3 |
| R-CG added (decisive); costs visible and continuous for all; no cost bins | Q6 |
| R-HAC-MB non-myopic; myopic reported separately | edit 6 |
| R-HAC-MF demoted to secondary; I-COST demoted to a generalization probe | Q6 |
| R-CONF impossibility restricted to the demonstrated information set | Q6 |
| R-HAC-ALL gate removed; resource ledger replaces "B bits" | Q7 |
| Tolerances illustrative only; three first-order categories | Q4, edit 4 |
| Decoder target → P(Z \| history) + own K_t(a); identification requirements; credited rescue defined | Q5 |
| C3-fallback rule → ORIGIN/ROLE/REDUCTION recording rules | Q1, edit 1 |
| Negative-outcome wording; DRAFT Q7 "park" rule removed; engineering versus scientific | edit 7 |
| "theory about C4 admission" wording; DRAFT Q11 "below" phrasing removed | edit 8 |
| C4-CMP1 mapping | Q9 |
| Exact-check spec plus PENDING approval | next step |
| **Numbers:** none changed. The binary-regime rates equal the DRAFT S/E pairs. | — |

---

## Appendix A. Exact values (unchanged from DRAFT Appendix A)

Files in `/workspace/scratch/c4_reliability/`, unmodified:

| file | sha256 |
| --- | --- |
| demo.py | 046d46fce121b051442637faaa746ce6ea42a9ca4d6599531ca6a72192f3a60d |
| demo.log | d25082c31dba1a83f759600dd68afcdbda1c13a37714e39e47df811a79d1231b |
| demo_results.json | e65aaa2a58ebb12eba40b3b7c190b7e39e6aaec3892fbf2b4ee3702e1287e478 |
| demo2.py | 9217109549fca519c07220c08267d68ce81bb45c2236cdddbe5c3976efe3f3eb |
| demo2.log | a77dfa28247d3b0c0bbd9439db09a873f37c100aff5d4f4f18d1ccf8af73b727 |
| plan_counts.py (sizing only) | 7c9abc8b7f0745589043f7536ffd5abd4f95688c6a36eff8619c4d2c88663391 |
| plan_counts.log (sizing only) | c18a1b2f8c64b9cda70e59e4718978725aa28584972b249e5d4389d37fdf7d9b |

All DRAFT Appendix A values hold verbatim for S = (1/20, 1/5) and E = (1/5, 1/20), ε = 23/100, c_r = 1/50, c_s = 3/50.
