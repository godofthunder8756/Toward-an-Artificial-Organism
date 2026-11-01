# C-axis theory queue v1: C4 (dissociable internal evaluation) and C5 (persistent self/world model with counterfactual self-prediction)

- **Status:** DRAFT, theory only. Written 2026-10-20 (EDT) by Research Delegate for the ACI
  Research Specialist, for Aidan Ahern.
- **Read-only:** nothing was run. No experiment, enumeration, solver, training or arithmetic
  script was used. All numbers in §4 are **hand arithmetic** and must be replayed exactly
  (in rationals) before anyone cites them. No file in `/workspace/repo` was touched.
- **Authorization:** none. Constitution v3 requires human approval for "first C4/C5/C6
  studies". This file proposes a queue and one ANALYTIC card design. It authorizes nothing.
- **Claim discipline:** this file makes no consciousness claim. The theory families appear
  here only as sources of *architectural* predictions. Q-EXIST, Q-LEARN, Q-CAUSE and
  Q-NECESSITY are kept apart and labelled at every use.
- **Inputs read:**
  - `/workspace/aci_handoff.md`, `aci_frontier_audit.md`, `aci_decision_package_v2.md`
    (with v1 §9 for the 13-answer format), `astra_consult_1.md`, and
    `/workspace/review/{alias_check,filter_algebra,sub_a0_adversary}.md`.
  - From the repo at HEAD `32cfbe6`: `ACI_RESEARCH_CONSTITUTION_v3.md`,
    `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` (the C3–C6 rows, `collapse_ledger` and
    `inactive_theory_queue`), `C1_RELIABILITY_DISPOSITION_v1.md`, `AC117_RESULTS_v1.md`,
    `ACI_THEORY_INDICATOR_MATRIX_v1.md`, and `ACI_TARGET_CONSTRUCT_v1.md` §N4.
  - The C4_TASK_DESIGN and C4_P2 headers. Those "C4" cards are an older card numbering
    about first-order uncertainty, not the C4 layer.

---

## 0. One-paragraph result

The five families disagree on C4 along three axes that a checklist hides:
- **Where the evaluator sits:** upstream gate (PRM) or downstream reader (GWT).
- **Whether its variable can be lesioned without moving type-1:** HOT says yes; predictive
  processing says no whenever precision enters inference.
- **Whether I/O-level tests can say anything at all:** RPT and IIT say no (the unfolding
  argument).

**The central obstacle is a theorem, not a design problem.** For any information set I, the
Bayes posterior given I minimizes expected Brier among all I-measurable forecasts. So **no
mechanism can beat a same-information, same-memory second readout on type-2 accuracy**, and
a candidate that "wins" has merely been given more information. "Beat the rivals" must
therefore be restated as a *structural* claim: every adequate evaluator must contain a
variable that is (a) not a function of the first-order state, (b) provably ignored by the
optimal first-order policy, and (c) needed for type-2 performance within a pre-registered
margin.

**Mechanisms.** I give five mechanically different C4 mechanisms.
- M1, a persistent self-channel reliability filter, is the only one that clears static
  selective prediction at parity on a structural criterion.
- It **ties** adaptive selective prediction (online-calibrated abstention). That is the same
  organization in ordinary clothing, and I say so.

**Cheapest decisive falsifier: C4-F1, the self-channel separability certificate.** It needs
one general lemma, a 4-cell exact rational table and a matched negative-control world.
Hand values:
- the one-bit evaluator's type-2 Brier advantage over the best static selective predictor is
  ≈ 0.0017, against a gate of 1/1000;
- the oracle ceiling is ≈ 0.0133;
- in the asymmetric-prior control, type-1 provably depends on the reliability variable,
  which is the predictive-processing / C1-disposition reduction.

**Ceiling.** PASS shows only that C4's operational criterion is **non-vacuous and
world-relative**. It does not show metacognition in any built or learned system.

---

## 1. Definitions used (from the repo, unchanged)

- **C4 layer** (handoff §Layers; ledger `layer_assessments[C4]`): internal evaluation
  dissociable from first-order inference.
  - Status NOT_ESTABLISHED.
  - Rival: "first-order statistic/count/reflex".
  - Ledger next_falsifier: **"evaluation is only a monotonic first-order transform or cannot
    be selectively mistaken."**
- **N4 spec** (`ACI_TARGET_CONSTRUCT_v1.md` §N4):
  - (a) E carries evidence about R's correctness without R's ground truth;
  - (b) two-way dissociation (false alarm and miss);
  - (c) the ideal-observer collapse is ruled out;
  - (e) required rivals: raw reflex, state-blind fixed policy, and **an ε-estimator arm,
    "to show E is not merely world-parameter estimation"**.
- **C5 layer:** persistent world/self modeling plus counterfactual self-prediction.
  - Status NOT_ESTABLISHED.
  - Rival: "ordinary recurrent world state plus episodic memory".
  - Next_falsifier: "prior self-state intervention has no distinct effect on
    interpretation/prediction/commitment".
  - Constitution v3: "N5 closure onto maintenance is not C5".
- **Prior reductions that bind this file:**
  - **AC117:** the monitor is CONTROL-yes, PREDICTION-no. P-G5/P-G6 FAIL because the
    transient `ones>=4` readout of the same substrate signal predicts wrongness perfectly.
    *A same-information readout matched the monitor on prediction.*
  - **C1 disposition:** the ideal-observer collapse is valid only under one lossless
    internal state. "Estimating ε alone still does not establish metacognition."
  - **Decision package v2 §C2 (my reading of SCARCITY_GAP):** opt-out =
    1[max_x P(x_q | m) < r], a monotone first-order transform of the bounded state. So
    access value is REDUCED.
  - **Astra #2:** "abstention threshold = conventional selective prediction, not C4."

---

## 2. Step 1: differential predictions of the five families for C4/C5

Rules for this section:
- A row is listed only where **at least two families predict different observable or
  structural outcomes**.
- "Prediction" means what the family's computational core implies for an *architecture*.
  None of this is a consciousness test.
- Where a row is my derivation rather than the authors' explicit claim, it is marked
  **[derived]**.
- Butlin et al. (2023) explicitly exclude IIT because it "is not compatible with
  computational functionalism". Their indicator list therefore gives IIT nothing to check,
  and this file records IIT only where it makes an opposite-direction structural claim.

### 2.1 C4 differentials

#### D-C4-1. Order of gating: does the evaluator gate global availability, or read from it?

| Family | Prediction |
| --- | --- |
| HOT, PRM variant (Lau 2022; Butlin HOT-2/HOT-3) | Upstream. The monitor tags first-order sensory activity as reliable perception versus noise, and the tag *gates* routing to higher cognition. Lau says the tag "causally facilitates" metacognition, control and broadcast. |
| GWT (Dehaene & Changeux 2011; Dehaene, Lau & Kouider 2017) | Downstream. Self-monitoring ("C2" in Dehaene et al.) is a separate dimension from global availability ("C1") and operates on workspace contents. |
| PP (Friston 2010; Fleming 2020 HOSS) | Neither, as a separate stage. Confidence is precision or higher-order state inference inside the same generative hierarchy. |

- **Architectural consequence:**
  - Under PRM, lesioning the monitor changes what reaches downstream consumers. Type-1 *as
    measured at a downstream consumer* changes, so the monitor is **not** cleanly
    dissociable from first-order use.
  - Under GWT, lesioning the monitor leaves broadcast and downstream type-1 intact and
    impairs only type-2.
- **Why it matters for C4:** the ledger's "selectively mistaken" criterion is predicted to
  hold under the GWT ordering and to **fail by design** under the PRM ordering. Both are
  higher-order-friendly theories. **[derived from the cited positions]**

#### D-C4-2. Can the evaluator's variable be lesioned without moving type-1?

| Family | Prediction |
| --- | --- |
| HOT (Lau & Rosenthal 2011; Brown, Lau & LeDoux 2019) | Yes in general. Higher-order states are distinct and can even misrepresent, e.g. a higher-order state without an adequate first-order one. Relative blindsight (Lau & Passingham 2006) and prefrontal TMS that impairs metacognition but not discrimination (Rounis et al. 2010) are the cited support. |
| PP / precision | Not in general. If the reliability or precision estimate weights evidence against prior in inference, changing it changes the posterior *and* the decision whenever the prior is informative. A type-2-only lesion exists only where the decision is invariant to precision. |
| First-order readout models (Kiani & Shadlen 2009 single-variable confidence; the ideal-observer model in Fleming & Daw 2017) | Only through readout noise. meta-d′ ≤ d′, with no variable beyond the decision variable. Not a family on the list, but the default rival all five must face. |

- **Architectural consequence:** this is decidable **analytically** in a declared world.
  - Is the Bayes-optimal type-1 argmax invariant to the reliability variable on reachable
    mass?
  - Section 4 builds exactly that contrast: W_sym is invariant and W_asym is not.
  - The C1 disposition's caution, "ε parameterizes a first-order likelihood", is precisely
    the PP prediction, and it holds in W_asym.

#### D-C4-3. Direction and source of dissociation

| Family | Prediction |
| --- | --- |
| HOT/PRM (Lau 2022; Gershman 2019 "generative adversarial brain"; Butlin HOT-1) | The monitor's job is **source discrimination**: world-driven activity versus internally generated activity (imagery, replay) versus noise. Its characteristic error is a *source* error, i.e. a self-generated state tagged as real. Confidence about correctness is a downstream use. |
| GWT | No source-specific prediction. Monitoring is evaluation of broadcast content. |
| PP / self-model | Source attribution comes from the generative model's account of its own predictions (precision and expected sensory consequences). |
| RPT, IIT | Silent. |

- **Architectural consequence:** a source monitor and a correctness monitor are different
  mechanisms (M3 vs M1 below).
- In a world where world-driven and self-generated first-order states **alias** (identical
  first-order state, different source), a source monitor needs information outside the
  first-order state, such as an efference copy of the generator. A correctness monitor
  needs information about channel reliability.

#### D-C4-4. Do I/O-level C4 tests bear on the theory at all?

| Family | Prediction |
| --- | --- |
| RPT (Lamme 2006) | The seat is local recurrent processing, not evaluation. A type-2 deficit with intact recurrent first-order processing is an access or report failure. RPT predicts nothing about whether a C4 evaluator exists. |
| IIT (Albantakis et al. 2023, IIT 4.0) | The seat is intrinsic cause–effect structure, not function. A strictly feed-forward evaluator attached to a first-order module adds no recurrent causal power back into it. **[derived]** A design property C4 requires, *a low-cost cut between evaluator and first-order*, is the kind of partition that lowers integration across that cut. The C4 desideratum and IIT's integration desideratum point in **opposite directions**. |
| Unfolding argument (Doerig et al. 2019) | Any I/O-defined C4/C5 falsifier is silent on RPT and IIT by construction, because a feed-forward unfolding can match the I/O. |

- **Consequence:** RPT and IIT are recorded as **not adjudicable** by any card in this
  queue, consistent with `ACI_THEORY_INDICATOR_MATRIX_v1.md` §5. No card should claim to
  test them.

#### D-C4-5. Correction and refinement to the repo's matrix (flag only; not an edit)

- `ACI_THEORY_INDICATOR_MATRIX_v1.md` codes N4 as HOT = P and RPT/GWT/PP = X.
- That is defensible for "necessary for consciousness". For C4 *as an architectural layer*,
  D-C4-1 to D-C4-3 show the families make **different positive predictions about where and
  how** an evaluator sits. A single X hides them.
- **Suggested additive refinement for a future matrix v2:**
  - split N4 into N4-gate (PRM upstream), N4-read (GWT downstream) and N4-precision (PP
    in-hierarchy);
  - add a row "type-1 invariance of the reliability variable (world property)", because
    whether C4 can exist without coupling to type-1 is a fact about the world, not about the
    theory (§4).

### 2.2 C5 differentials

#### D-C5-1. Is a persistent self-model a necessary, control-oriented component?

| Family | Prediction |
| --- | --- |
| PP/SMT (Seth & Tsakiris 2018; Metzinger 2003) | Yes. Selfhood is grounded in predictive, control-oriented modelling of the organism's own body and physiological state. Seth & Tsakiris call it "a beast machine". |
| GWT | No dedicated self-model is required. Self-information is one more broadcastable content, and GWT-4 state-dependent attention covers sequential querying. |
| HOT | Only thin self-reference (higher-order states about one's *own* first-order states). A persistent self-model is not required. |
| RPT, IIT | No prediction. |

- **Architectural consequence:** the ledger's C5 rival ("ordinary recurrent world state plus
  episodic memory") is exactly what GWT/HOT predict suffices. PP/SMT predicts it fails where
  regulation of the agent's *own* variables needs predictions conditioned on its own
  actions.
- **[derived]** A POMDP belief over (world, own-state) is the ordinary rival. Its own-state
  factor *is* a self-model in the functional sense. So the distinctive PP/SMT claim must be
  about *persistence and reuse* of that factor (across world resets or tasks), not about its
  mere presence.

#### D-C5-2. Is the self-model lossy, and where are its systematic errors?

| Family | Prediction |
| --- | --- |
| Attention schema theory (Graziano & Webb 2015; Wilterson & Graziano 2021; Butlin AST-1) | The self-model of attention is a *simplified* descriptive model used for control. Its errors are systematic: it misdescribes attention in predictable ways. Wilterson & Graziano report that an agent with an attention schema controls attention better than one without. |
| PP/SMT (Metzinger 2003, "transparency") | The self-model is not represented *as* a model. **[interpretive]** Its errors are not available to the system as errors without a further meta-model. |
| GWT/HOT | No prediction about self-model lossiness. |

- **Architectural consequence:** a C5 test with a *sufficient* self-statistic cannot
  distinguish AST from ordinary state estimation. AST becomes distinctive only when the
  controller lacks direct access to the allocation variable and must use a lossy model of
  it.

#### D-C5-3. Counterfactual self-prediction and privileged access

| Family / prior art | Prediction |
| --- | --- |
| PP (Seth 2014, "counterfactual richness") | Perceptual presence depends on the richness of counterfactual sensorimotor predictions. Self-prediction under counterfactual actions is a core PP competence. |
| Introspection-as-privileged-access (Binder et al. 2024, arXiv) | Self-prediction beats cross-prediction by a different model trained on the same behaviour record, and tracks the agent's own behaviour after that behaviour is changed. This is the cleanest published template for a "same-information second readout" rival in C5. |
| Machine self-modelling (Bongard, Zykov & Lipson 2006; Kwiatkowski & Lipson 2019) | Action-conditional self-models support recovery after damage. Engineering prior art showing the self-model is ordinary model-based control. |
| HOT/GWT/RPT/IIT | No distinctive counterfactual-self prediction. |

- **Architectural consequence (feeds C5-Q1):** privileged access exists **iff** the agent's
  internal state is not identifiable from its behaviour record. That gives a reachable own-
  state alias: two internal states with identical behaviour histories but different
  counterfactual responses. This is the C5 analogue of Astra's history-pair witness.

#### D-C5-4. Self/world attribution

| Family / prior art | Prediction |
| --- | --- |
| Comparator / efference models (Frith, Blakemore & Wolpert 2000; Butlin AE-2) | Distinguishing self-caused from world-caused sensory change needs a forward model of one's own action consequences. Corollary discharge is the known reduction. |
| PRM (Lau 2022) | Reality monitoring is the perceptual analogue: self-generated activity must be tagged as not-real. |

- **Architectural consequence:** a minimal C5 component is a forward model of own-action
  consequences. Its reduction (prediction subtraction) is well known, so it is a prerequisite
  rather than C5 itself.

---

## 3. Step 2: minimal C4 mechanisms and how each fares against the rivals

### 3.0 Rivals, defined at parity

- **Notation.** First-order state s_t, which is all the first-order module retains. The
  evaluator's information set is I_E. Its persistent state z has a budget of B bits.
- **R1, conventional (static) selective prediction:**
  - c_t = g(s_t), including thresholded abstention 1[κ(s_t) ≥ θ] (Chow 1970; El-Yaniv &
    Wiener 2010; Geifman & El-Yaniv 2017).
  - SelectiveNet (Geifman & El-Yaniv 2019) learns g jointly but still reads only the current
    input and shared body, so it falls in the same information class in a memoryless world.
  - The review finding ("thresholded abstention reduces to selective prediction") is R1.
- **R2, same-information second readout:** any readout with the *same* I_E and the *same*
  persistent-state budget B.
  - Examples: a second-order network reading first-order activations (Cleeremans,
    Timmermans & Pasquali 2007; Pasquali et al. 2010), ConfidNet (Corbière et al. 2019), or
    a P(IK) head (Kadavath et al. 2022).
- **R3, adaptive selective prediction:** an online-calibrated threshold or conformal level
  updated from the evaluator's own error history (Gibbs & Candès 2021, adaptive conformal
  inference).

**Impossibility statement (elementary).** For any I and binary target Y = 1[decision
correct], the forecast q* = P(Y | I) minimizes E[(Y − q)²] over I-measurable q. If the
coarser forecast is q_c = E[q* | coarse info], its Brier excess is exactly E[(q* − q_c)²].
Hence:
- no mechanism beats R2 on type-2 accuracy;
- a mechanism beats R1 **iff** its information set strictly refines R1's on positive mass,
  and only by E[(q* − q_c)²].

So the only honest sense of "beats R1 and R2 at parity" is **structural**: every evaluator
within margin ε of q* must hold a variable with properties (a)–(c) from §0. R2 at equal
budget does not defeat such a claim; R2 *is an instance of* the claimed organization. That
makes the organization ordinary, which is allowed (constitution v3: "An ordinary mechanism
can instantiate a genuine functional role"), but the claim ceiling must say so.

### 3.1 The five mechanisms

| # | Mechanism (mechanically distinct) | Extra information vs first-order state | vs R1 (static selective prediction) | vs R2 (same info, same B) | vs R3 (adaptive selective prediction) | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **M1** | **Self-channel reliability filter.** A persistent belief z over the regime of the agent's own first-order channel (relay noise ε_t), updated from internal-consistency signals (agreement among redundant samples) and optional outcome feedback, and consumed only by evaluation and abstention. Fleming & Daw's "separation over time"; Maniscalco & Lau's meta-d′ > d′ case via extra information. | Past first-order inputs and feedback, which the memoryless first-order discards. | **Beats** whenever the type-2 target depends on the regime and the first-order module keeps no regime information. Margin is computable (§4: ≈0.0017 Brier lower bound). | **Ties by theorem.** The structural claim survives: R2 must also hold z. | **Ties.** R3 is the same organization (memory of own error rate). | **Best candidate**, judged on structure rather than superiority. |
| M2 | **Implementation-integrity monitor.** Reads first-order *substrate* bookkeeping (replica disagreement, repair outcomes, starvation bits), as in the C1 disposition and AC117. | Damage signals outside the first-order sufficient statistic. | Beats when damage is independent of world evidence (C1 §2). | **Fails on prediction.** AC117: the direct readout of the same signal (`ones>=4`) had AUC 1.000 vs the monitor's 0.9858. Distinct only on CONTROL, as a directional repairer. | n/a | Parked. Its distinct role is control, which belongs on O-axis/N5 cards, not C4 prediction. |
| M3 | **Source / reality monitor** (PRM; Gershman's GAN discriminator). Classifies whether the first-order state was driven by world input, self-generation or noise. | Efference copy of the generator, or generator-state statistics. | Beats in worlds with source aliasing. R1's confidence is high for a vivid self-generated state and a strong percept alike, so it cannot separate them. | **Ties** given the same efference copy. Reduces to a comparator / corollary-discharge subtraction (Frith et al. 2000). | n/a (different target) | Queue as C5-Q2, since its content is self/world attribution. Also the only route to test D-C4-1's upstream-gating prediction. |
| M4 | **Post-decisional evidence evaluator** (Pleskac & Busemeyer 2010, 2DSD; Resulaj et al. 2009). Confidence integrates evidence arriving after commitment. | Later world evidence. | Beats (more information). | **Fails parity.** With a first-order change-of-mind policy given the same later evidence, it is first-order inference continued. Its content is about the world, not the self, so it fails N4(e)(iii). | n/a | Reject as a C4 candidate. Keep as a reduction note. |
| M5 | **Heuristic positive-evidence evaluator** (Zylberberg et al. 2012; Peters et al. 2017; Koizumi et al. 2015; Maniscalco & Lau 2016). Confidence from a cheaper statistic, e.g. evidence for the chosen option only. | None (less). | **Loses** on accuracy, since R1-Bayes is optimal on the same information. | Loses. | Loses. | Not a mechanism to build. Useful as a **dissociation probe**: confidence moved at fixed d′ shows the evaluator is a separate computation, but not that it is useful. Possible engineering win on compute only (Q9 = engineering). |

**Honest summary.**
- None of M1–M5 beats R2 on accuracy at parity; that is impossible.
- M1 and M3 survive as *structural* candidates.
- M1 is cheaper to make decisive, because type-1 invariance (D-C4-2) can be proved in
  closed form, whereas M3 needs a generator model.
- M1 does **not** beat adaptive selective prediction (R3). The decisive card must therefore
  claim only that the C4 operational criterion is non-vacuous, never that M1 is better than
  conventional ML.

---

## 4. Step 3: C4-F1, the self-channel separability certificate (ANALYTIC design, not run)

### 4.1 Declared worlds

**Primary world W_sym:**
- **World:** hidden X_t ∈ {0,1}, i.i.d. per trial with P(X_t = 1) = π = 1/2. There is no
  world memory, so the first-order module has nothing to carry across trials.
- **Internal channel regime:** R_t ∈ {G, B}, a two-state Markov chain.
  - P(G→B) = δ = 1/20 and P(B→G) = ρ = 1/10.
  - The chain is initialized at stationarity: P(B) = δ/(δ+ρ) = 1/3.
- **Observations:** on each trial the agent receives n = 3 samples of X_t, each independently
  flipped with probability ε_G = 1/10 (G) or ε_B = 2/5 (B).
- **Type-1 decision:** the binary choice x̂_t.
- **Type-2 target:** Y_t = 1[x̂_t = X_t], scored by Brier.
- **Feedback:** none in the base card. Outcome feedback is a declared extension. Evidence
  about R comes only from the within-trial agreement pattern u_t ∈ {unanimous, split}.

**Negative control W_asym:** identical except π = 7/10.

**Declared, not evidence.** Calling R the agent's *own* channel is a declaration. W_sym
cannot distinguish an internal relay from a noisy world channel; see Q10 and the C4-F1b
extension.

### 4.2 Lemma 1 (type-1 invariance; general, proof only)

**Statement.** For any odd n, any finite set of regimes with every ε_r < 1/2, π = 1/2 and
any belief b over regimes, the Bayes type-1 decision is the majority of the samples,
independent of b.

**Proof.** With k ones out of n:

  P(k | X=1) = Σ_r b_r C(n,k) (1−ε_r)^k ε_r^{n−k}
  P(k | X=0) = Σ_r b_r C(n,k) ε_r^k (1−ε_r)^{n−k}

For k > n/2, each term of the first sum dominates the matching term of the second, because
((1−ε_r)/ε_r)^{2k−n} > 1. So the posterior favours 1 for every b. The case k < n/2 is
symmetric, and odd n excludes ties. ∎

**Corollary.** In W_sym the optimal first-order module needs **zero** bits of regime state.
Any regime variable z is type-1-irrelevant, so lesioning or corrupting z changes no type-1
decision on any history.

### 4.3 Lemma 2 (W_asym breaks invariance; exact)

- At n = 3 and k = 1, the likelihood ratio for X=1 vs X=0 is ε/(1−ε): 1/9 under G and 2/3
  under B.
- The posterior odds are (7/3)·LR: 7/27 < 1 under G (choose 0) and 14/9 > 1 under B
  (choose 1).
- So the Bayes type-1 at k = 1 depends on the regime belief, and k = 1 has positive mass.
- **Consequence:** in W_asym the reliability variable is consumed by type-1. A z-lesion moves
  type-1. This is the PP/precision reduction (D-C4-2) and the C1 disposition's "ε
  parameterizes a first-order likelihood" caution.

### 4.4 Quantities to certify (exact rationals; hand values given for orientation only)

Per-regime facts at n = 3 (exact):

| | P(correct) | P(unanimous) | P(correct \| unanimous) | P(correct \| split) |
| --- | --- | --- | --- | --- |
| G | 243/250 | 73/100 | 729/730 | 9/10 |
| B | 81/125 | 7/25 | 27/35 | 3/5 |

Three evaluators:

1. **R1, static selective prediction** (the best g(u_t); a function of the first-order state
   only). Confidence on unanimous = 0.558/0.58 ≈ 0.96207; on split = 0.306/0.42 ≈ 0.72857.
   This equals Chow's rule on the stationary-mixture posterior.
2. **E1, one-bit evaluator:** z_t = u_{t−1}, giving a 4-cell table.
   - Hand computation (regime predicted through the chain from P(r_{t−1} | u_{t−1})): the
     cell confidences are ≈ 0.98025, 0.78604, 0.92893 and 0.67359.
   - **Brier excess of R1 over E1 = E[(q_E1 − q_R1)²] ≈ 0.00168.**
3. **Oracle-regime ceiling:** E[(P(correct | u, R) − q_R1)²] ≈ **0.01330**.

The full filter's excess lies in [excess(E1), oracle], i.e. ≈ [0.0017, 0.0133]. That is a
**bound**, not a computed value.

### 4.5 Pre-registered gates

| Gate | Condition | Notes |
| --- | --- | --- |
| G1 | Lemma 1 holds (proof review plus exact check on all 4 (k) values at the declared parameters). | |
| G2 | Exact excess(E1) ≥ 1/1000. | Hand value ≈ 0.00168 (margin about 1.7×). Exact replay required. |
| G3 | Negative control: Lemma 2's sign flip reproduces exactly in W_asym. | |
| G4 | Selective mistakability, by construction from G1. Setting z to the wrong cell (e.g. swapping u_{t−1}) changes c_t on positive mass and changes x̂_t on zero mass. | Both directions of the N4(b) dissociation exist: false alarm (z says B while R=G and the decision is correct), and miss (z says G after an unobserved switch to B). The 1/20 and 1/10 switch rates give both positive mass. |

**Certificate coverage.** Lemma 1 is general (all odd n, all ε_r < 1/2, π = 1/2). G2/G3 are
exact finite arithmetic at the declared parameters: 2 regimes × 4 cells × 2 transitions.
The full-filter excess is **not** certified, only bracketed.

**Bounded UNRESOLVED rule.** Return UNRESOLVED if:
- the exact replay disagrees with an independent second replay;
- any rational fails to normalize;
- the stationary initialization is mis-specified.

The response is additive errata and one re-replay. A second defect parks the card. No
retuning of n, ε, δ, ρ or π is allowed after seeing values.

### 4.6 The 13 admission answers (constitution v3)

**Classification: ANALYTIC.** Analytic construction proves existence, not acquisition.

| # | Answer |
| --- | --- |
| Q1 | **C4** (internal evaluation dissociable from first-order inference), as a bounded prerequisite. Is the ledger's C4 operational criterion ("not a monotonic first-order transform; can be selectively mistaken") **non-vacuous** in some declared world, and on what world property does it depend? This is Q-EXIST only. |
| Q2 | ONE hypothesis. In W_sym, every type-2 evaluator whose Brier advantage over the best function of the current first-order state is ≥ 1/1000 must carry state z that is (a) not a function of the first-order state, and (b) ignored by the Bayes-optimal first-order policy. The one-bit z = u_{t−1} suffices. W_asym is the pre-registered negative control in which (b) fails. |
| Q3 | Falsifiers, pre-specified. **F-a:** Lemma 1 fails on reachable mass in W_sym, so the evaluator variable is first-order precision and C4 reduces to PP-style precision estimation. **F-b:** exact excess(E1) < 1/1000, so the world has no headroom. Per overreach rule R2 this is *not* evidence against C4. **F-c:** the negative control does not flip (W_asym invariant), which signals a design or algebra error and returns UNRESOLVED. **F-d:** the replays disagree, which returns UNRESOLVED. |
| Q4 | **Strongest simpler explanation:** ordinary Bayesian reliability tracking, equivalently adaptive selective prediction (R3; an online HMM / changepoint filter over channel quality). At equal information and an equal 1-bit budget, the same-information readout (R2) **is** E1. So the card claims structural necessity of the variable, never superiority over R2 or R3. Static selective prediction (R1, Chow / thresholded abstention) is the rival the card must and (by hand values) does exceed. |
| Q5 | Frozen evidence making it necessary rather than a repetition: (i) ledger C4 next_falsifier, never yet tested against a world where it could pass; (ii) AC117 P-G5/P-G6 FAIL (a same-information readout matched the monitor); (iii) `C1_RELIABILITY_DISPOSITION_v1.md` (collapse valid only under the ideal observer; "estimating ε alone" caution); (iv) decision package v2 §C2 and Astra #2 (abstention = selective prediction; REDUCED). No frozen card identifies the *world property* (type-1 invariance) that separates C4 from precision. |
| Q6 | **After PASS:** record that C4's criterion is satisfiable, with the known reduction "adaptive calibration". Amend the C4 next_falsifier to add "…or the reliability variable is consumed by type-1 on reachable mass". Then propose (human gate) **C4-F1b**: regime transitions caused by the agent's own maintenance action, with an efference-copy rival at equal memory (package v2 §C3 #3), to address *self* referent. Separately propose (human gate) a Q-LEARN card. **Prediction from Lemma 1:** a first-order network trained only on type-1 in W_sym has no incentive to encode z, so a second readout of its state (R2 restricted to first-order activations) should fail, and z must come from a type-2 objective. |
| Q7 | **After FAIL F-a:** log a collapse "self-channel evaluator → first-order precision". C4 dissociability then requires a type-1-irrelevant reliability variable, and no world with one is known. **After F-b:** this world lacks headroom; a new world needs an additive rationale plus a human gate, with no retuning. **After UNRESOLVED:** errata, one re-replay, then park. |
| Q8 | Minimum apparatus: **analytic proof** (Lemmas 1–2) plus an **exact rational table** (E1, R1, oracle) with an independent replay. No neural model, organism, training or solver. The arithmetic replay is still a "run" and needs Aidan's approval. |
| Q9 | Organizational-cognition question at the analytic level: the existence of a separable evaluator *role* given world structure. Not substrate competence. Not engineering. |
| Q10 | **Ceiling:** "In declared world W_sym, a type-2-relevant, type-1-irrelevant persistent variable exists. Any evaluator beating static selective prediction by ≥ 1/1000 Brier must carry it. Hence C4's operational criterion is non-vacuous here, and in W_asym the same variable is consumed by type-1." **NOT established:** metacognition in any built or learned system (Q-LEARN, Q-CAUSE untouched); superiority over same-information or adaptive selective prediction; self-referent content (internal vs world channel is declared, not tested; deferred to C4-F1b); HOT credit (the result is equally a PP-compatible fact about symmetric worlds); anything about RPT/IIT (D-C4-4); any C7/phenomenal claim. |
| Q11 | C4. Unsupported prerequisites: C2 acquired representation (PARTIAL), C3 integration (PARTIAL), and Q-LEARN/Q-CAUSE of any evaluator. |
| Q12 | O-axis: none. O0 throughout. The world, regimes, channel, evaluator and arithmetic are supplied; no maintenance is modelled. The O/C intersection is deferred to C4-F1b. |
| Q13 | **PASS:** ledger C4 gains an analytic/EXTERNAL evidence row; belief "C4 separability is world-relative (requires type-1 invariance)"; the status stays NOT_ESTABLISHED (no system). **F-a:** new `collapse_ledger` entry (self-channel evaluator → first-order precision); belief "the C1 ε-caution is general". **F-b:** no belief change beyond "W_sym rejected". **UNRESOLVED:** no change. |

### 4.7 Why this is the cheapest *decisive* falsifier

- **Lemma 1 is a proof.** If it were false, C4 as defined would collapse to precision
  estimation in the simplest world that could support it. That alone is decisive for F-a.
- **G2 needs 8 exact numbers.** The full filter's value is unnecessary, because the one-bit
  lower bound already decides the gate.
- **W_asym costs one extra line** and pre-registers the reduction that the C1 disposition
  and the PP column predict.
- **Contrast with alternatives:**
  - M3 needs a generative source model.
  - M2 is already answered by AC117.
  - Any neural card needs Q-LEARN approval and training.

---

## 5. The queue (ordered; every item needs human approval before any run)

| Order | Card | Class | Question | Known reduction | Cheapest discriminator |
| --- | --- | --- | --- | --- | --- |
| 1 | **C4-F1** (§4) | ANALYTIC | Is C4's criterion non-vacuous, and is it world-relative? | Adaptive calibration / precision | Lemma 1 + 4-cell exact table + W_asym |
| 2 | C4-F1b | ANALYTIC | Self referent: regime changes caused by the agent's own repair action. Is the evaluator's z redundant given an efference copy of own actions at equal memory? | Efference-copy decoder (package v2 §C3 #3) | Own-state alias witness: same efference history, different required confidence |
| 3 | C4-L1 | CONFIRMATORY (later) | Q-LEARN/Q-CAUSE: does a learned agent acquire z, and does a z-lesion give a type-2-only deficit (meta-d′ drop at fixed d′)? | Second readout of first-order activations (Cleeremans 2007; ConfidNet) | Lemma-1 prediction: type-1-only training leaves z absent |
| 4 | C5-Q1 | ANALYTIC | Privileged counterfactual self-prediction: is there a reachable own-state alias (identical behaviour record, different counterfactual response)? Does a cross-predictor with the full behaviour record lose? | Behaviour-record cross-predictor (Binder et al. 2024 design) | Alias witness. If none exists, self-prediction reduces to behaviour modelling. |
| 5 | C5-Q2 (= M3) | ANALYTIC | Self/world source attribution under aliasing. Also tests D-C4-1 (does the monitor gate downstream availability?). | Comparator / corollary discharge (Frith et al. 2000) | Lesion-the-tag prediction: PRM ordering moves downstream type-1, GWT ordering does not |
| 6 | C5-Q3 | ANALYTIC | Persistence: does the own-state factor of the belief carry across world resets and change commitments (e.g. repair) beyond episodic outcome memory? This is the ledger C5 falsifier. | POMDP belief over (world, self) + episodic memory | Intervene on the self-factor vs the world-factor; distinct effect on commitment |
| 7 | C5-Q4 | ANALYTIC (parked) | AST lossy self-model: a controller without direct access to its allocation variable | Direct access to the allocation variable | Only meaningful if access is architecturally denied; otherwise reduces |
| — | M2, M4, M5 | — | Not queued as C4 candidates (§3.1). | — | M2 → O-axis/N5 control cards; M5 → dissociation probe inside C4-L1 |

Proposed `inactive_theory_queue` additions (for a gated ledger v2, not applied):
- "C4 separability requires type-1-irrelevant reliability" (falsifier F-a);
- "privileged self-prediction" (C5-Q1).

---

## 6. Open questions and caveats

1. **The parity theorem reframes the assignment.** "Beat a same-information second readout
   at resource parity" cannot hold on accuracy for any mechanism. The ACI Research
   Specialist should confirm the structural reframing (§3.0) before C4-F1 is proposed to
   Aidan.
2. **M1 ties adaptive selective prediction (R3).** If the program decides that anything
   conventional ML already does cannot count as C4, then C4-F1 PASS would be logged as
   REDUCED at birth. That is a definitional decision for Aidan, not something a run can
   settle.
3. **N4(e)(iii) tension.** In W_sym, M1 *is* an ε-estimator arm. The construct requires
   showing E is "not merely world-parameter estimation", and that cannot be met in W_sym by
   construction. It is deferred to C4-F1b (self-caused regime changes). Flagged here, not
   resolved.
4. **Hand arithmetic only.** The §4.4 decimals were computed by hand and need exact rational
   replay. The per-regime fractions in the table are exact.
5. **Parameter choice.** n = 3, ε_G = 1/10, ε_B = 2/5, δ = 1/20, ρ = 1/10 and π = 7/10 were
   picked once here for small exact arithmetic and the 1/1000 threshold was borrowed from the
   two-stream card. Freeze them before any replay; do not tune.
6. **D-C4-1 and D-C4-4 contain [derived] readings** (PRM gating implies non-dissociability;
   the IIT cut tension). These are my inferences from the cited positions, not the authors'
   stated predictions.

---

## 7. Citations and verification status

Verification: bibliographic fields (authors, year, title, venue, DOI or arXiv id) were
checked on 2026-10-20 against Crossref (api.crossref.org), arXiv abstract pages or
publisher/proceedings pages. "Verified" means the record exists as cited. Quoted phrases
attributed via repo documents are marked.

### Metacognition and confidence

| Ref | Status |
| --- | --- |
| Fleming, S. M., & Daw, N. D. (2017). Self-evaluation of decision-making: A general Bayesian framework for metacognitive computation. *Psychological Review* 124:91–114. doi:10.1037/rev0000045 | Verified (Crossref). The "separation over space and/or time" quote is taken via `C1_RELIABILITY_DISPOSITION_v1.md`; the quote text itself was not re-checked. |
| Maniscalco, B., & Lau, H. (2012). A signal detection theoretic approach for estimating metacognitive sensitivity from confidence ratings. *Consciousness and Cognition* 21:422–430. doi:10.1016/j.concog.2011.09.021 | Verified |
| Fleming, S. M., & Lau, H. (2014). How to measure metacognition. *Frontiers in Human Neuroscience* 8:443. doi:10.3389/fnhum.2014.00443 | Verified (article number from repo; DOI verified) |
| Galvin, S. J., Podd, J. V., Drga, V., & Whitmore, J. (2003). Type 2 tasks in the theory of signal detectability. *Psychonomic Bulletin & Review* 10:843–876. doi:10.3758/bf03196546 | Verified |
| Barrett, A. B., Dienes, Z., & Seth, A. K. (2013). Measures of metacognition on signal-detection theoretic models. *Psychological Methods* 18:535–552. doi:10.1037/a0033268 | Verified |
| Yeung, N., & Summerfield, C. (2012). Metacognition in human decision-making: confidence and error monitoring. *Phil. Trans. R. Soc. B* 367:1310–1321. doi:10.1098/rstb.2011.0416 | Verified |
| Pouget, A., Drugowitsch, J., & Kepecs, A. (2016). Confidence and certainty: distinct probabilistic quantities for different goals. *Nature Neuroscience* 19:366–374. doi:10.1038/nn.4240 | Verified (background; not load-bearing) |
| Kiani, R., & Shadlen, M. N. (2009). Representation of confidence associated with a decision by neurons in the parietal cortex. *Science* 324:759–764. doi:10.1126/science.1169405 | Verified |
| Pleskac, T. J., & Busemeyer, J. R. (2010). Two-stage dynamic signal detection: A theory of choice, decision time, and confidence. *Psychological Review* 117:864–901. doi:10.1037/a0019737 | Verified (an erratum exists: 118:56, doi:10.1037/a0022399) |
| Resulaj, A., Kiani, R., Wolpert, D. M., & Shadlen, M. N. (2009). Changes of mind in decision-making. *Nature* 461:263–266. doi:10.1038/nature08275 | Verified |
| Zylberberg, A., Barttfeld, P., & Sigman, M. (2012). The construction of confidence in a perceptual decision. *Frontiers in Integrative Neuroscience* 6. doi:10.3389/fnint.2012.00079 | Verified |
| Peters, M. A. K., Thesen, T., Ko, Y. D., Maniscalco, B., Carlson, C., Davidson, M., et al. (2017). Perceptual confidence neglects decision-incongruent evidence in the brain. *Nature Human Behaviour* 1. doi:10.1038/s41562-017-0139 | Verified (first six authors checked) |
| Koizumi, A., Maniscalco, B., & Lau, H. (2015). Does perceptual confidence facilitate cognitive control? *Attention, Perception, & Psychophysics* 77:1295–1306. doi:10.3758/s13414-015-0843-3 | Verified |
| Maniscalco, B., & Lau, H. (2016). The signal processing architecture underlying subjective reports of sensory awareness. *Neuroscience of Consciousness* 2016. doi:10.1093/nc/niw002 | Verified |
| Shekhar, M., & Rahnev, D. (2021). The nature of metacognitive inefficiency in perceptual decision making. *Psychological Review* 128:45–70. doi:10.1037/rev0000249 | Verified (cited only as metacognitive-noise background) |
| Fleming, S. M. (2020). Awareness as inference in a higher-order state space. *Neuroscience of Consciousness* 2020, niz020. doi:10.1093/nc/niz020 | Verified (Crossref also lists a related record, niaa011) |

### Blindsight and type-2 dissociations

| Ref | Status |
| --- | --- |
| Weiskrantz, L. (1986). *Blindsight: A Case Study and Implications.* Oxford University Press. | Verified via secondary bibliographic sources only (no DOI) |
| Persaud, N., McLeod, P., & Cowey, A. (2007). Post-decision wagering objectively measures awareness. *Nature Neuroscience* 10:257–261. doi:10.1038/nn1840 | Verified |
| Lau, H. C., & Passingham, R. E. (2006). Relative blindsight in normal observers and the neural correlate of visual consciousness. *PNAS* 103:18763–18768. doi:10.1073/pnas.0607716103 | Verified |
| Rounis, E., Maniscalco, B., Rothwell, J. C., Passingham, R. E., & Lau, H. (2010). Theta-burst transcranial magnetic stimulation to the prefrontal cortex impairs metacognitive visual awareness. *Cognitive Neuroscience* 1:165–175. doi:10.1080/17588921003632529 | Verified |

### Selective prediction and confidence readouts (ML)

| Ref | Status |
| --- | --- |
| Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Trans. Information Theory* 16:41–46. doi:10.1109/tit.1970.1054406 | Verified |
| El-Yaniv, R., & Wiener, Y. (2010). On the foundations of noise-free selective classification. *JMLR* 11:1605–1641. | Verified (jmlr.org) |
| Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. NeurIPS 2017. arXiv:1705.08500 | arXiv verified. NeurIPS 2017 venue per the SelectiveNet reference list (pp. 4878–4887), not checked on the proceedings site. |
| Geifman, Y., & El-Yaniv, R. (2019). SelectiveNet: A deep neural network with an integrated reject option. arXiv:1901.09192 | arXiv verified. ICML 2019 venue inferred from the paper's ICML template; PMLR volume not checked. |
| Hendrycks, D., & Gimpel, K. (2017). A baseline for detecting misclassified and out-of-distribution examples in neural networks. ICLR 2017. arXiv:1610.02136 | Verified (arXiv journal_ref) |
| Corbière, C., Thome, N., Bar-Hen, A., Cord, M., & Pérez, P. (2019). Addressing failure prediction by learning model confidence. NeurIPS 2019 (Advances 32). arXiv:1910.04851 | Verified (NeurIPS proceedings page and arXiv) |
| Gibbs, I., & Candès, E. (2021). Adaptive conformal inference under distribution shift. arXiv:2106.00170 | arXiv verified. Commonly cited as NeurIPS 2021; venue not checked. |
| Kadavath, S., Conerly, T., Askell, A., Henighan, T., Drain, D., et al. (2022). Language models (mostly) know what they know. arXiv:2207.05221 | Verified |
| Cleeremans, A., Timmermans, B., & Pasquali, A. (2007). Consciousness and metarepresentation: A computational sketch. *Neural Networks* 20:1032–1039. doi:10.1016/j.neunet.2007.09.011 | Verified |
| Pasquali, A., Timmermans, B., & Cleeremans, A. (2010). Know thyself: Metacognitive networks and measures of consciousness. *Cognition* 117:182–190. doi:10.1016/j.cognition.2010.08.010 | Verified |

### Theory families and indicators

| Ref | Status |
| --- | --- |
| Butlin, P., Long, R., Elmoznino, E., Bengio, Y., Birch, J., et al. (2023). Consciousness in Artificial Intelligence: Insights from the Science of Consciousness. arXiv:2308.08708 | Verified. Indicator wording (RPT-1/2, GWT-1–4, HOT-1–4, AST-1, PP-1, AE-1/2) and the IIT-exclusion sentence checked on the arXiv HTML. |
| Lamme, V. A. F. (2006). Towards a true neural stance on consciousness. *Trends in Cognitive Sciences* 10:494–501. doi:10.1016/j.tics.2006.09.001 | Verified |
| Dehaene, S., & Changeux, J.-P. (2011). Experimental and theoretical approaches to conscious processing. *Neuron* 70:200–227. doi:10.1016/j.neuron.2011.03.018 | Verified |
| Dehaene, S., Lau, H., & Kouider, S. (2017). What is consciousness, and could machines have it? *Science* 358:486–492. doi:10.1126/science.aan8871 | Verified. The C1/C2 distinction is stated from my knowledge of the paper; the full text was not re-read here. |
| Lau, H., & Rosenthal, D. (2011). Empirical support for higher-order theories of conscious awareness. *Trends in Cognitive Sciences* 15:365–373. doi:10.1016/j.tics.2011.05.009 | Verified |
| Brown, R., Lau, H., & LeDoux, J. E. (2019). Understanding the higher-order approach to consciousness. *Trends in Cognitive Sciences* 23:754–768. doi:10.1016/j.tics.2019.06.009 | Verified |
| Lau, H. (2022). *In Consciousness We Trust: The Cognitive Neuroscience of Subjective Experience.* Oxford University Press. doi:10.1093/oso/9780198856771.001.0001 | Verified (OUP page). The PRM gating/tag description was checked against the BJPS review and the Closer to Truth summary, not the book text. |
| Gershman, S. J. (2019). The generative adversarial brain. *Frontiers in Artificial Intelligence* 2:18. doi:10.3389/frai.2019.00018 | Verified |
| Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience* 11:127–138. doi:10.1038/nrn2787 | Verified |
| Seth, A. K. (2014). A predictive processing theory of sensorimotor contingencies: Explaining the puzzle of perceptual presence and its absence in synesthesia. *Cognitive Neuroscience* 5:97–118. doi:10.1080/17588928.2013.877880 | Verified |
| Seth, A. K., & Tsakiris, M. (2018). Being a beast machine: The somatic basis of selfhood. *Trends in Cognitive Sciences* 22:969–981. doi:10.1016/j.tics.2018.08.008 | Verified |
| Metzinger, T. (2003). *Being No One: The Self-Model Theory of Subjectivity.* MIT Press. | Verified (MIT Press page; no DOI) |
| Graziano, M. S. A., & Webb, T. W. (2015). The attention schema theory: a mechanistic account of subjective awareness. *Frontiers in Psychology* 6:500. doi:10.3389/fpsyg.2015.00500 | Verified |
| Wilterson, A. I., & Graziano, M. S. A. (2021). The attention schema theory in a neural network agent: Controlling visuospatial attention using a descriptive model of attention. *PNAS* 118. doi:10.1073/pnas.2102421118 | Verified |
| Albantakis, L., Barbosa, L., Findlay, G., Grasso, M., Haun, A. M., Marshall, W., et al. (2023). Integrated information theory (IIT) 4.0. *PLOS Computational Biology* 19:e1011465. doi:10.1371/journal.pcbi.1011465 | Verified |
| Doerig, A., Schurger, A., Hess, K., & Herzog, M. H. (2019). The unfolding argument: Why IIT and other causal structure theories cannot explain consciousness. *Consciousness and Cognition* 72:49–59. doi:10.1016/j.concog.2019.04.002 | Verified |

### Self-models, introspection, world models

| Ref | Status |
| --- | --- |
| Binder, F. J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., Perez, E., Turpin, M., & Evans, O. (2024). Looking inward: Language models can learn about themselves by introspection. arXiv:2410.13787 | Verified (arXiv). Venue not checked. The cross-prediction design and the behaviour-change result were read on the arXiv page. |
| Frith, C. D., Blakemore, S.-J., & Wolpert, D. M. (2000). Abnormalities in the awareness and control of action. *Phil. Trans. R. Soc. B* 355:1771–1788. doi:10.1098/rstb.2000.0734 | Verified |
| Bongard, J., Zykov, V., & Lipson, H. (2006). Resilient machines through continuous self-modeling. *Science* 314:1118–1121. doi:10.1126/science.1133687 | Verified |
| Kwiatkowski, R., & Lipson, H. (2019). Task-agnostic self-modeling machines. *Science Robotics* 4. doi:10.1126/scirobotics.aau9354 | Verified |
| Littman, M. L., Sutton, R. S., & Singh, S. (2001). Predictive representations of state. NIPS 14, pp. 1555–1561. | Verified (NeurIPS proceedings) |

**Considered and dropped:** Rosenthal (2005), Hohwy (2013), Tononi & Koch (2015), Blackwell
comparison-of-experiments, Betley et al. (2025) and Ha & Schmidhuber (2018) are not cited.
The first five were not verified in this session; Ha & Schmidhuber's arXiv record was
verified but the paper is not used. The §3.0 parity argument uses only the elementary
proper-scoring fact and needs no citation.

### Repo sources (read at HEAD `32cfbe6`; not modified)

- `ACI_RESEARCH_CONSTITUTION_v3.md`
- `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json`
- `C1_RELIABILITY_DISPOSITION_v1.md`
- `AC117_RESULTS_v1.md`
- `ACI_THEORY_INDICATOR_MATRIX_v1.md`
- `ACI_TARGET_CONSTRUCT_v1.md` (§N4)
- The ledger's C4 evidence path `N5_Evidence_Hierarchy_v1.md` is a case mismatch for
  `N5_EVIDENCE_HIERARCHY_v1.md` (already flagged in the frontier audit). That file was not
  needed here.
