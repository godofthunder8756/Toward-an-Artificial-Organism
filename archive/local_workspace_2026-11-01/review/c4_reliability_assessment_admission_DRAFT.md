# Learned assessment of internal processing reliability with costly rechecking: C4 admission and identifiability (DRAFT v1, theory only)

**Status:** DRAFT for Astra review. Written 2026-10-21, about 4:10–4:40 AM ET, by the Research Delegate executor for the ACI Research Specialist, for Aidan Ahern.

**Card class:** ANALYTIC / admission-criteria (constitution v3). It authorizes no experiment.

**Nothing in this document asserts C4 status.** It makes no C4, C5 or consciousness claim. It states the criteria a future study would have to meet before any C4-relevant evidence row could be written, and what would send the study to C3 instead.

**Work done for it:**
- No training and no repo changes.
- Small exact-enumeration checks only, with `fractions.Fraction` in `/workspace/scratch/c4_reliability/` (Appendix A).
- All world rates and costs below are **ILLUSTRATIVE and UNFROZEN**, following the C4-CMP1 precedent (Ruling R-A2): "deliberately unset … Do not freeze them before approval". They exist only to exhibit the demonstration.

**Approvals.**
- Constitution v3: "Human authorization is required for … first C4/C5/C6 studies".
- Consult #20: "Any subsequent training and the first C4 study require Aidan's explicit, study-specific approval. A GRU implementation can stay within the existing architecture family; that does not remove the C4 approval requirement."
- Any exact certificate over a finite rival class (§4.4) is solver-like and also needs approval, per the C4-CMP1 precedent.

**The four questions stay separate.** Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are labelled at every use.

---

## 0. Sources and the construct being admitted

- **C4 row (ACI_RESEARCH_SYNTHESIS_v1):** "C4 evaluation | … | Causally dissociable internal correctness/reliability process, second-order errors and selective lesions".
- **ACO C4 (ACI_TARGET_CONSTRUCT_v1 §6):** "The system's evaluation of one of its representations can be *wrong about it* in both directions (false alarm and miss), and those dissociations track the system's own bookkeeping, not the world."
- **Astra's distinct-evaluation conjunction** (consult #3, as recorded in `c_axis_theory_queue_v2.md` §1):

  > "Distinct-evaluation criterion = conjunction: (referent) predicts own first-order correctness with interventions separating system vs evidence changes; (selective causal content) swap/corrupt evaluator content holding full first-order state -> directional evaluation errors + specified downstream consequence, matched rescue reverses; (reduction) same adaptive rival gets same info/resources/interventions, compare whole intervention-response pattern. Detachable head makes lesionability trivial; update closure != second-order status."

- **Consult #16:** "It must specify an internal-evaluation role and evidence dissociating that role from first-order inference. … Supplying that task does not establish acquisition of an evaluator; ORIGIN must be tested separately."
- **Consult #20, Program strategy (verbatim essentials):**
  - "A generic recurrent learner makes first-order predictions and can pay to recheck or use an alternative processing channel."
  - "Hidden, persistent changes affect the reliability of its own processing. It receives ordinary outcomes and action costs, not fault labels, oracle confidence or a supplied reliability register."
  - "Before training, demonstrate that the task admits cases where first-order predictive performance is matched but the value of checking differs."
  - "Compare against conventional confidence-based checking and history-dependent adaptive-control rivals."
  - "Require causal evidence that the candidate assessment process affects checking appropriately while first-order prediction is preserved within prespecified tolerances. Prediction damage followed by changed checking is insufficient."
  - "Keep acquisition, functional role and conventional reduction separate. A supplied evaluator would not establish acquired organization."
  - "If the design cannot distinguish this assessment role from ordinary uncertainty-driven selection or routing, classify it as a C3 study instead. Do not assign C4 merely because the task includes checking, confidence or internal faults."
- **Precedent:** `c_axis_theory_queue_v2.md` §3.2. M1, a persistent self-channel reliability belief, was **REDUCED** in W_sym to adaptive-threshold selective prediction (Ruling R-A1: unlabeled adaptation counts as conventional). Recorded belief: "a persistent reliability belief is not, by itself, distinct evaluation". This document is built so that it does not repeat that collapse by construction, and it states where it still might (§8, §10.4).

**The construct, stated precisely.** The candidate assessment target is the **locus** of current unreliability: whether errors arise in the learner's own processing channel or in the world's evidence. Its **magnitude** is not the target. The world in §1 is built so that the locus carries **zero** information for default first-order prediction, but determines which costly check is worth buying. That is the identifiability lever (§2).

---

## 1. World sketch W-REL (illustrative; nothing frozen)

**Per trial t:**
1. A hidden binary target X_t is drawn, uniform. (A variant with a skewed prior is noted in §10, A4.)
2. The world emits n = 3 evidence bits b_{t,i} = X_t ⊕ W_{t,i}, where W_{t,i} ~ Bern(w_{E_t}) is world noise.
3. The learner's **own processing channel** (a front-end F, see dependency flag F1) reads each bit: y_{t,i} = b_{t,i} ⊕ N_{t,i}, where N_{t,i} ~ Bern(e_{I_t}) is internal processing noise. The learner receives y_t.
4. The learner chooses one action:
   - PREDICT now;
   - RECHECK, at cost c_r: the same evidence bits b_t are re-processed by F with fresh internal noise, giving y′_t;
   - RESAMPLE, at cost c_s: fresh world bits are drawn and read once by F, giving y″_t.

   It then outputs a first-order prediction p̂_t = P̂(X_t = 1 | …).
5. **Feedback:** the outcome X_t (or correct/incorrect) and the realized cost. Reward = 1[correct] − cost. (A scoring-rule variant is noted in §10, A5.)

**Hidden persistent states** (Markov, persistent, independent):
- **I_t ∈ {ok, faulty}:** reliability of the learner's own processing, with internal noise e_ok < e_faulty.
- **E_t ∈ {clean, noisy}:** reliability of the evidence, with world noise w_clean < w_noisy.
- The rates are chosen so that **(faulty, clean)** and **(ok, noisy)** have equal per-read flip probability: ε = w + e − 2we is symmetric under the swap w ↔ e, so the match is exact and analytic, not tuned.
- These two cells are the **matched system-change / evidence-change pair**. They satisfy the requirement in the C4-CMP1 design (`c_axis_theory_queue_v2.md` §4.2, I4/I5) that the match "is to be shown analytically, not tuned".

**What the learner does NOT receive:**
- fault labels;
- I_t or E_t;
- oracle confidence;
- the Bayes posterior;
- any supplied reliability register;
- any per-read correctness signal beyond the trial outcome.

Costs are visible as inputs: (c_r, c_s) vary across blocks and are shown each trial. That is needed for the revaluation probe in §4.

**Learner (for a later empirical study; not specified here as an experiment):**
- A generic GRU in the existing family.
- Inputs: y, y′ or y″ when taken, the previous outcome, and the costs.
- Two readouts: a first-order prediction head and an action head.
- Trained on reward, plus an outcome-prediction loss from the revealed X_t. The outcome is ordinary feedback, not a fault label.
- No separate evaluator module and no protected state.

The learning rule (RL over actions) differs from the PR #7 supervised recipe. This is flagged as F3.

**Illustrative rates used only in Appendix A:**
- e_ok = w_clean = 1/20;
- e_faulty = w_noisy = 1/5;
- so cell S = (faulty, clean) has (w, e) = (1/20, 1/5), cell E = (ok, noisy) has (w, e) = (1/5, 1/20), and ε = 23/100 in both;
- costs c_r = 1/50, c_s = 3/50.

---

## 2. Pre-training demonstration (exact enumeration; Appendix A)

All values are exact rationals. The scripts are `demo.py` and `demo2.py`.

**D1. Matched first-order performance, exactly.**
- In cells S and E, the joint distribution of (X, y) is **identical**: total variation = 0 exactly.
- So the default first-order posterior P(X | y), accuracy, confidence distribution and outcome statistics are identical. Majority accuracy is 456533/468700 ≈ 0.9740 for unanimous reads and 77/100 for split reads.
- The joint distribution of (X, y, y″) under RESAMPLE is also identical (TV = 0), because six reads with independent world draws all have flip probability ε.
- Consequence: **no learner can distinguish S from E from outcomes, default reads or resamples.**

**D2. Checking value differs at matched first-order performance.** In split-read states (probability 5313/10000):
- the RECHECK accuracy gain is **3456/44275 ≈ 0.0781 in S** but only **9747/1416800 ≈ 0.0069 in E**;
- the RESAMPLE gain is **47817/500000 ≈ 0.0956 in both**.

With c_r = 1/50 and c_s = 3/50, the optimal action for the **same** split read, with the **same** first-order posterior, is **RECHECK in S** and **RESAMPLE in E**. PREDICT is optimal for unanimous reads in both.

Exact region (split states) where S-optimal = RECHECK while E-optimal ≠ RECHECK:
- c_r < 3456/44275;
- c_r < c_s − 15563907/885500000 (≈ c_s − 0.0176);
- and either c_r > 9747/1416800 or c_r > c_s − 0.0888.

**D3. Regime-blind checking loses value.** With S and E equiprobable:
- regime-aware optimum: 0.8905231721 per trial;
- best regime-blind policy (any function of y, equivalently of the first-order posterior; it chooses PREDICT/RESAMPLE): 0.8845663442;
- **exact gap: 59568279/10^10 ≈ 0.00596 per trial.**

This is the value pressure for a locus assessment over the illustrative rates (Q-EXIST of value pressure in the world, not in any learner).

**D4. Identifiability only through one's own costly rechecks.**
- Under RECHECK, (X, y, y′) differ between S and E: TV = 2762073/6400000 ≈ 0.432.
- Per-bit read-reread agreement is 17/25 in S versus 181/200 in E.
- The locus is therefore identifiable **only** from the agreement between the learner's own two processings of the same evidence. That information is bought by the very action whose value it governs, which creates an exploration and value-of-information problem.

**D5. Post-check first-order belief does depend on the locus (precision-role confound).**
- After RECHECK, the Bayes posterior differs between the S and E models by up to 0.0987 (at obs y = 000, y′ = 011).
- The Bayes decision is unchanged in all 64 observations at these rates.
- Pre-check posterior gap: 0 exactly.
- **So the locus belief is first-order-irrelevant before checking, but plays a precision (evidence-weighting) role after checking.** The causal criteria (§5) therefore measure first-order preservation on the **pre-check** prediction, and report post-check precision effects separately.

**Robustness (grid).** For all 10 pairs w < e over {1/20, 1/10, 3/20, 1/5, 3/10}:
- the swap preserves (X, y) and (X, y, y″) exactly;
- the recheck gain is larger in the system-dominant cell (e > w) than in its swap.

**Coverage and limits of the demonstration:**
- A single trial, with known cell (or a 1/2–1/2 mixture).
- No persistence dynamics or exploration values are computed.
- Rates are illustrative.

It establishes only **existence of the dissociation in W-REL**. It does not show that a learner acquires anything (no Q-LEARN), that anything is causally used (no Q-CAUSE), or anything about rivals beyond regime-blind policies (no reduction against R-HAC).

---

## 3. Candidate role and what would count as an assessment state

An **assessment state** A_t is a component of the learner's state that meets all of:
- (a) It encodes the locus belief: it predicts own first-order correctness **after** each check type, i.e. it predicts whether RECHECK will help. This is a type-2 referent: own processing versus evidence.
- (b) It is **causally read by checking**.
- (c) It can be intervened on while **pre-check first-order prediction is preserved** within tolerance (§5.2).

In W-REL, A_t is identifiable in principle because the Bayes-optimal locus belief has zero pre-check first-order content (D1). The component of hidden state that the action head uses, beyond what the first-order head uses, is therefore not forced by first-order prediction.

Traps carried from Astra #3:
- "Detachable head makes lesionability trivial". Lesioning the action head is recorded, not credited.
- "update closure != second-order status". Persistence alone earns nothing.

---

## 4. Rivals (defined so they can be fitted later)

All rivals get the **same observables**:
- y, y′ and y″ when taken;
- outcomes;
- costs;
- the same action set;
- the same memory budget (the same number of state units or bits as the candidate, B to be frozen);
- the same parameter and compute ceiling;
- the same intervention set.

Rivals are reported separately and judged on the **whole intervention-response pattern** (§5), not on reward alone.

### 4.1 R-CONF: conventional confidence-based checking

- Score: s_t = |p̂⁰_t − 1/2|, where p̂⁰_t is the pre-check first-order confidence. It is the rival's own first-order head, or Bayes P(X | y) in the analytic version.
- Policy: a(s_t, c_r, c_s) is a deterministic or softmax map. Parameters: two thresholds θ_r < θ_s per cost bin, and a temperature.
- **R-CONF-S (static).** The thresholds are fitted once, by reward maximization, or by behavioural likelihood when fitted to candidate data.
- **R-CONF-A (adaptive threshold).** θ_t is updated online from labelled errors on **default (pre-check) predictions**: θ_{t+1} = θ_t + η(err_t − α*). This is the Gibbs & Candès-style adaptive form. Free parameters: η and α*.
- By D1, every R-CONF member has identical input statistics in S and E, so it **cannot** separate them.
- Boundary: if an "adaptive confidence" rule also updates from post-check outcomes or recheck agreement, it is classified as R-HAC, not R-CONF.

### 4.2 R-HAC: history-dependent adaptive control

- **R-HAC-MF (model-free).**
  - Feature vector φ_t = (read class, k-window counts of recheck agreements, k-window post-check errors per check type, cost bin).
  - Action values Q(φ, a) are learned by TD(0) or Q-learning from reward, with ε-greedy or softmax exploration.
  - Free parameters: k, learning rate, exploration rate and temperature. The fitted class is frozen with its feature list.
  - Its state is action values and window counts, with no explicit locus variable and no cost-general reliability estimate.
- **R-HAC-MB (model-based).** A Bayes forward filter over (I, E), possibly quantized to B bits, plus expected-value action selection given the current costs. This is the analytic optimum. It is conventional (POMDP belief-state control), and it is itself a locus estimator.
- **R-HAC-ALL(B).** All deterministic B-bit finite-state controllers over the same quantized observables and actions. It is finite at fixed B, and it is the full same-resource class for a certificate.

### 4.3 Discriminating probes against R-HAC-MF

- **I-COST revaluation.** Shift (c_r, c_s) to an unseen block value. An assessment-plus-cost policy re-optimizes immediately. Cached Q-values under R-HAC-MF need re-learning, unless the cost is in φ and the new value was trained.
- **I-SWAP** of the locus content (§5): R-HAC-MF has no separable locus content, so its analogous swap acts on window counts.

### 4.4 Expected reduction status (stated before any computation)

R-HAC-MB **contains** the role by construction. A learned GRU approaching optimal reward will plausibly be **behaviourally and interventionally equivalent to R-HAC-MB**, as M1 was to A_thr in W_sym (§3.2 precedent). Separation is plausible against R-CONF (by D1 and D3) and possibly against R-HAC-MF (through I-COST and I-SWAP). Separation from R-HAC-MB, or from R-HAC-ALL at B ≥ the candidate's state size, is **not** expected. §8 states the consequence and §10.4 asks Astra how it should be classified.

---

## 5. Interventions and causal criteria (first-order preservation required)

### 5.1 Matched intervention set (identical for candidate and rivals)

| Id | Intervention |
| --- | --- |
| I-SYS | Force I: ok → faulty with E clean (cell S). |
| I-EVID | Force E: clean → noisy with I ok (cell E). Matched to I-SYS on default first-order accuracy **exactly** (D1). |
| I-SWAP | Replace the candidate's locus content with its value from a donor history (S-belief ↔ E-belief), holding the pre-check first-order state fixed (§5.3). |
| I-CORRUPT | Clamp the locus content to a fixed value: "faulty-locus" or "evidence-locus". |
| I-RESCUE | Restore the pre-intervention content. |
| I-COST | Unseen cost revaluation (§4.3). |
| I-HEAD | Action-head lesion. Recorded, **not credited**. |

### 5.2 First-order preservation tolerances (proposed; frozen only at protocol stage)

Measured on the **pre-check** first-order output p̂⁰ over a prespecified evaluation set (every reachable read pattern × a fixed bank of histories):

- δ_p: max |Δp̂⁰| ≤ 0.02;
- δ_acc: |Δ accuracy| ≤ 0.005;
- δ_LL: relative change in first-order log loss ≤ 2%.

An intervention that exceeds **any** tolerance is a **non-pass** for C-SEL. It is not excluded and not re-tried, because "Prediction damage followed by changed checking is insufficient." Post-check first-order effects (the D5 precision role) are reported separately and do not count toward or against C-SEL.

### 5.3 Locating locus content without a supplied register

The procedure is prespecified and its use of the oracle is disclosed:
1. On an identification split, fit a linear decoder from the GRU hidden state to the analysis-only Bayes locus posterior b_src = P(I = faulty | history). The oracle is used for analysis only, never for training, mirroring the disclosed FO-gradient precedent.
2. I-SWAP and I-CORRUPT replace the projection of h onto the decoder subspace with the donor or clamp value. This is an interchange intervention: the orthogonal complement is kept.
3. Validity requires §5.2.
4. The decoder's held-out R² is reported, and a decoder below a prespecified floor makes C-SEL UNRESOLVED.

An alternative without an oracle would use the action head's input direction that is orthogonal to the first-order head's input. See ambiguity A7.

### 5.4 Criteria (all required for a C4-RELEVANT pattern)

- **C-REF (referent).** Under I-SYS versus I-EVID, matched exactly on first-order accuracy, RECHECK propensity rises more under I-SYS and RESAMPLE more under I-EVID. Both differences must exceed prespecified margins, in ≥ 8/10 seeds.
- **C-T2 (type-2 prediction).** The candidate's locus content predicts its own post-check correctness gain better than the pre-check confidence s_t does. This is a calibration test with a prespecified margin. It errs in both directions under I-CORRUPT (false alarm and miss, per ACO C4).
- **C-SEL (selective causal content).** I-SWAP and I-CORRUPT produce **directional** checking errors: a faulty-locus clamp gives excess RECHECK under evidence noise, and an evidence-locus clamp gives excess RESAMPLE or wasted cost under a system fault. They do so with the §5.2 tolerances met, and I-RESCUE reverses both.
- **C-FO.** §5.2 holds for every credited intervention.
- **C-RED.** On the whole pattern {C-REF, C-T2, C-SEL, I-COST responses, recovery profiles}, the candidate is **not reproduced** by any fitted member of R-CONF (S and A), nor by R-HAC-MF, at matched resources. Reproduction by R-HAC-MB is recorded separately (§8).

---

## 6. Claims kept separate, with allowed and forbidden wording

| Claim | What it would need | Allowed wording (template) | Forbidden |
| --- | --- | --- | --- |
| **Q-EXIST (world)** | D1–D4 at frozen rates (exact) | "In W-REL at the frozen rates, default first-order performance is identical across a matched system-change/evidence-change pair while the value of rechecking differs; a regime-blind policy loses [exact] value." | "The learner assesses its reliability"; any statement about a learner |
| **Q-LEARN** | A GRU trained on outcomes and costs only acquires a state meeting C-T2, with prespecified decoding and behavioural criteria, in ≥ 8/10 seeds; analysis-only oracle disclosed | "A GRU trained on outcomes and costs acquired state that predicts the benefit of rechecking and distinguishes own-processing from evidence changes, under [criteria]." | "acquired an evaluator / metacognition / self-model"; claiming acquisition from a decoder alone; any supplied evaluator |
| **Q-CAUSE** | C-REF + C-SEL + C-FO + I-RESCUE | "Intervening on the identified locus content changed checking in the predicted direction while pre-check first-order prediction stayed within [δ_p, δ_acc, δ_LL]; rescue reversed it." | "causal evaluation" when C-FO fails; crediting I-HEAD; "type-1 invariant" without §5.2 numbers |
| **Reduction** | C-RED against named classes | "The intervention-response pattern was not reproduced by R-CONF-S/A or R-HAC-MF at matched information and resources." Or: "REDUCED to [named class]." | "irreducible", "beats all rivals", "distinct evaluation" when only reward differs |
| **Q-NECESSITY** | Out of scope here, beyond D3 against regime-blind policies | "Regime-blind policies are strictly suboptimal in W-REL at the frozen rates (D3)." | "assessment is necessary" relative to R-HAC |
| **C-level** | Astra ruling on §8 | "This admission document asserts no C4 status." | Any C4, C5, consciousness, self-awareness or organism claim |

---

## 7. Falsifiers (prespecified)

- **F-W1 (world).** At the frozen rates, D1 fails (the cell pair is not exactly matched), or D2/D3 give no positive value gap. The world is then not admissible, and rates are **not** retuned post hoc.
- **F-L1 (Q-LEARN).** The learned GRU does not meet C-T2, or does not exceed R-CONF in reward or pattern. The answer is "no locus assessment acquired within declared training", not an impossibility claim.
- **F-C1 (Q-CAUSE).** C-SEL fails (non-directional, or no rescue), or every effective intervention violates §5.2. The checking changes are then not dissociated from first-order inference.
- **F-R1 (reduction).** A fitted R-CONF member reproduces the whole pattern. The result is classified **C3 uncertainty-driven routing** (§8).
- **F-R2 (reduction).** R-HAC-MF reproduces the whole pattern, including I-COST and I-SWAP analogues. The result is **REDUCED to model-free adaptive control** and classified C3 (§8).
- **F-REF.** I-SYS and I-EVID give indistinguishable checking responses. The referent claim is defeated regardless of rivals.

## 8. C3-fallback rule (explicit)

Classify the study as **C3**, with no C4 evidence row, if **any** of the following holds:

1. **Rival R-CONF reproduces:** the candidate's checking is reproduced within tolerance by a function of pre-check first-order confidence and costs (R-CONF-S or R-CONF-A). This is uncertainty-driven routing.
2. **No intervention preserves first-order prediction:** C-FO cannot be met by any prespecified intervention that changes checking.
3. **Referent fails:** C-REF fails.
4. **Rival R-HAC-MF reproduces:** R-HAC-MF reproduces the whole intervention-response pattern. This is history-dependent adaptive control with no separable assessment content.
5. **The assessment is supplied:** it is a supplied evaluator, a supplied register or a supplied loss on the locus (ORIGIN = SUPPLIED). That is not acquired organization.

**Default for the R-HAC-MB case (pending an Astra ruling, §10.4).** Suppose 1–5 do not hold, but R-HAC-MB, the conventional Bayes locus filter with expected-value control, reproduces the whole pattern. By the §3.2 / R-A1 precedent ("a persistent reliability belief is not, by itself, distinct evaluation"), the default label is **REDUCED to conventional model-based reliability estimation**, classified C3-plus-annotation. The annotation would read: "the learned system instantiates a conventional locus-estimation role meeting C-REF/C-T2/C-SEL/C-FO".

This default **may make a C4 evidence row unreachable in this design**, and it is flagged as the central open question.

Consult #20: "Do not assign C4 merely because the task includes checking, confidence or internal faults."

---

## 9. Thirteen admission answers

1. **Q1. Question.** C4 internal evaluation, as an admission and identifiability prerequisite. Can a learner's assessment of the **locus** of its own processing unreliability be defined, identified and causally tested in a way that is dissociated from first-order inference and not reduced to conventional checking rivals?
2. **Q2. Hypothesis or question.** ONE question: in W-REL at frozen rates, does a learned GRU acquire locus content that meets C-REF, C-T2, C-SEL and C-FO, with a whole intervention-response pattern not reproduced by R-CONF or R-HAC-MF at matched resources? The present document answers only the pre-training part: D1–D4 show the world admits the dissociation.
3. **Q3. Falsifiers.** F-W1, F-L1, F-C1, F-R1, F-R2 and F-REF (§7). §8 lists the classifications that defeat the proposed C4 relevance.
4. **Q4. Strongest simpler explanation.**
   - R-HAC-MB, Bayes POMDP control over (I, E), which is conventional and contains the role.
   - Then R-HAC-MF, then R-CONF-A and R-CONF-S.
   - All at the same observables, memory, parameters and interventions.
   - Known equivalence precedent: M1 ≡ A_thr in W_sym (§3.2).
5. **Q5. Why it is necessary rather than a repetition.**
   - Consult #20's Program strategy names this the top next step.
   - Consult #16 named the task class.
   - The §3.2 REDUCED entry and the C4-F1 withdrawal show that a reliability belief in W_sym is reducible and that W_sym cannot separate system from evidence change.
   - No frozen card tests locus assessment with matched first-order performance, costly self-generated identifying evidence, and first-order-preserving interventions.
6. **Q6. On success** (a C4-RELEVANT pattern, all of §5.4). Propose a frozen empirical protocol, which needs Aidan's study-specific approval and Astra clearance, with fresh seeds. The ledger C4 row gains, at most, an evidence row naming the rivals beaten and those not beaten. **The C4 status is not changed by this document.**
7. **Q7. On failure or UNRESOLVED.**
   - F-W1: redesign the world under a new card, with no retuning.
   - F-R1 or F-R2: record a C3 or REDUCED entry, and park this content.
   - R-HAC-MB default: record "conventional locus estimation instantiated".
   - UNRESOLVED (decoder floor not met, replay disagreement, certificate incomplete): errata, one re-replay, then park.
8. **Q8. Minimum apparatus.**
   - Now: analytic and exact enumeration only (done for D1–D5 at illustrative rates).
   - Next: a finite exact certificate over R-HAC-ALL(B) at frozen rates (solver-like, needs approval).
   - Later: a GRU in the existing family trained by RL plus outcome prediction (needs approval).
   - No organism model.
9. **Q9. Level.** Organizational cognition: an internal-evaluation role versus adaptive control under intervention. Reward and cost efficiency are reported separately as engineering quantities.
10. **Q10. Ceiling.**
    - This document's best case: "W-REL admits a matched-first-order, differing-check-value dissociation (exact, illustrative rates)."
    - An eventual study's best case: "learned locus content meets C-REF/C-T2/C-SEL/C-FO and is not reproduced by R-CONF or R-HAC-MF".
    - **NOT established:** C4 status; non-reduction to R-HAC-MB; any higher-order content beyond the locus belief; necessity outside W-REL; any theory credit; anything about consciousness or C7.
11. **Q11. C-level.** C4 (internal evaluation), addressed as admission only. Unsupported prerequisites: C2 acquired representation (PARTIAL), C3 integration (PARTIAL), and C4 Q-LEARN and Q-CAUSE (not started). Below C4 throughout. No C5.
12. **Q12. O-level.** O0. The front-end F and its fault process are **SUPPLIED** substrate. RECHECK is a modelled action, not self-repair. No O1–O3 claim.
13. **Q13. Belief change.**
    - C4-RELEVANT pattern: "locus assessment can be acquired and causally dissociated from first-order inference, beyond R-CONF/R-HAC-MF" (evidence row, status unchanged).
    - REDUCED or C3: "costly rechecking in W-REL is explained by [named rival]" (collapse entry).
    - R-HAC-MB default: "learned locus estimation instantiates a conventional POMDP role" (annotation pending Astra).
    - UNRESOLVED: no change.

---

## 10. Dependency flags, ambiguities and open questions

### 10.1 Architecture and register dependency flags (none adopted)

- **F1. "Own processing" is a supplied front-end, not the learned weights.**
  - The faults act on F, a fixed reading channel declared part of the learner's body (SUPPLIED). This keeps the GRU and its architecture unchanged.
  - If Astra requires faults inside the **learned computation**, for example persistent noise on GRU hidden units, then RECHECK means recomputing on the same evidence. That needs an agent-side evidence buffer and a state snapshot/restore.
  - **That is a protected register/controller dependency and possibly a new architecture element. It is flagged, not adopted.**
- **F2. Evidence retention for RECHECK is world-side.** The environment holds b_t for the trial. There is no agent register.
- **F3. Learning rule.** RL over discrete actions, plus outcome prediction, differs from the PR #7 supervised recipe. It is not a new architecture family, but it is a new training regime. Any training needs Aidan's explicit study-specific approval and Astra clearance.
- **F4. Locating content (§5.3).** This uses an analysis-only oracle decoder and interchange interventions on hidden state. It adds no register. If it is replaced by a dedicated "assessment" module or head, the result would be a supplied evaluator (ORIGIN = SUPPLIED), and lesions would be trivial (I-HEAD).
- **F5. Cost inputs.** Costs are ordinary inputs (needed for I-COST), not a reliability signal.

### 10.2 Ambiguities (resolved provisionally in this draft)

- **A1.** The C4 target is the **locus** (system vs evidence), not reliability magnitude. A magnitude estimate is first-order-relevant (precision role) and is treated as C3-type.
- **A2.** "Matched first-order performance" means exact equality of the (X, y) distribution across the matched cells, which implies equal posterior, accuracy and confidence. It does not mean approximate matching.
- **A3.** First-order preservation is measured on the **pre-check** prediction. Post-check differences are expected under D5 and are reported as a precision role.
- **A4.** The prior is uniform and n = 3. A skewed prior would couple choice to belief (the v2 §3.3 W_asym caveat). Deferred.
- **A5.** The reward is 0/1 accuracy minus costs. A proper scoring rule would make post-check confidence (D5) decision-relevant.
- **A6.** The rival memory budget B equals the candidate's state size, measured in units or bits. The conversion from GRU state to bits is unresolved.
- **A7.** The decoder target is the analysis-only Bayes locus posterior, disclosed as an oracle. The non-oracle alternative (§5.3) is weaker.
- **A8.** R-CONF-A adapts only from default-prediction errors. Anything that uses post-check outcomes is R-HAC.
- **A9.** The illustrative rates and costs are not frozen. D1 holds for any swap pair; D2's action split holds in the exact cost region given.

### 10.3 Open questions for Astra

1. **Central question.** If the learned system meets C-REF, C-T2, C-SEL and C-FO, and beats R-CONF and R-HAC-MF, but is reproduced by R-HAC-MB (conventional Bayes locus filtering with expected-value control), is that REDUCED and C3 (the §3.2/R-A1 precedent, this draft's default), or a C4-relevant instantiation of the role by an ordinary mechanism (constitution v3: "An ordinary mechanism can instantiate a genuine functional role")? If the former, is any C4 row reachable in this design family?
2. Is the locus target (system vs evidence), first-order-irrelevant before checking by construction, an acceptable operationalization of "internal-evaluation role dissociated from first-order inference"? Or does the exact zero first-order content make the dissociation trivial, in the same way as the "type-1-irrelevant variable" criterion that was replaced?
3. Is a supplied, faultable front-end (F1) an acceptable "own processing" referent, or must faults act on learned computation, which would trigger the register dependency?
4. Are the proposed tolerances (δ_p = 0.02, δ_acc = 0.005, δ_LL = 2%) and the pre-check measurement point acceptable?
5. Is the analysis-only oracle decoder for locating locus content acceptable, with disclosure, or is a non-oracle identification required?
6. Is R-HAC-MF, as defined in §4.2, the right "conventional history-dependent adaptive control" rival, and is I-COST an acceptable discriminator? Should the cost be in φ, which would weaken I-COST?
7. Should a finite certificate over R-HAC-ALL(B) at frozen rates precede any training? This is the C4-CMP1-style analytic step, which itself needs approval.
8. How should persistence and exploration be set? The design requires the learner to pay for the identifying rechecks (D4). Should a minimum exploration requirement or a value-of-information analysis be part of admission?
9. How does this card relate to C4-CMP1 (W_ref, design-only, awaiting a gate)? Should it supersede C4-CMP1, merge with it, or run after it?

---

## Appendix A. Exact-enumeration demonstration

Location: `/workspace/scratch/c4_reliability/`. Python with `fractions`; no training, no learning.

| file | sha256 |
| --- | --- |
| demo.py | 046d46fce121b051442637faaa746ce6ea42a9ca4d6599531ca6a72192f3a60d |
| demo.log | d25082c31dba1a83f759600dd68afcdbda1c13a37714e39e47df811a79d1231b |
| demo_results.json | e65aaa2a58ebb12eba40b3b7c190b7e39e6aaec3892fbf2b4ee3702e1287e478 |
| demo2.py | 9217109549fca519c07220c08267d68ce81bb45c2236cdddbe5c3976efe3f3eb |
| demo2.log | a77dfa28247d3b0c0bbd9439db09a873f37c100aff5d4f4f18d1ccf8af73b727 |

**Key exact values** (S = (w, e) = (1/20, 1/5); E = (1/5, 1/20); ε = 23/100):

| quantity | S | E |
| --- | --- | --- |
| TV(X, y), no check | 0 | 0 |
| TV(X, y, y″), resample | 0 | 0 |
| TV(X, y, y′) between S and E, recheck | 2762073/6400000 (shared) | 2762073/6400000 (shared) |
| per-bit recheck agreement | 17/25 | 181/200 |
| split-state accuracy: none | 77/100 | 77/100 |
| split-state accuracy: recheck | 150191/177100 ≈ 0.8481 | 1100683/1416800 ≈ 0.7769 |
| split-state accuracy: resample | 432817/500000 ≈ 0.8656 | 432817/500000 ≈ 0.8656 |
| unanimous-state accuracy (all actions) | 456533/468700 | 456533/468700 |
| optimal action, split state (c_r = 1/50, c_s = 3/50) | RECHECK | RESAMPLE |

Further values:
- Regime-aware value 0.8905231721; best regime-blind value 0.8845663442; gap 59568279/10^10.
- Post-recheck posterior gap between the regime models: at most 0.0987; Bayes decisions identical in 64/64 observations. Pre-check posterior gap: 0.
- Grid: all 10 swap pairs are exactly invariant for the no-check and resample distributions, and the recheck gain is larger in the system-dominant cell in all 10.
