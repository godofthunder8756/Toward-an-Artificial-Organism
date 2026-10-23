# C-axis theory queue v2: corrections after Astra consultation #3

**Draft.** Additive successor to `c_axis_theory_queue_v1.md`. v1 is unchanged.

- Written 2026-10-20 (EDT) by Research Delegate for the ACI Research Specialist, for Aidan
  Ahern.
- **Read-only:**
  - Nothing was run: no solver, replay, enumeration, arithmetic script or training.
  - Nothing in `/workspace/repo` was touched.
  - N4 and `ACI_THEORY_INDICATOR_MATRIX_v1.md` are untouched.
  - C4-F1b is not started.
- **No consciousness claim.** Theory families appear only as sources of frozen causal-graph
  variants.
- **The four questions stay separate.** Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are
  labelled at every use.
- **Source of the corrections:** `/workspace/astra_consult_1.md`, "Astra consultation #3".
  That file is itself a *condensed* record, so "Astra's exact wording" below means the
  wording as recorded there, quoted verbatim.

---

## 0. What changes from v1

| v1 claim | v2 status | Why (Astra #3 + own check) |
| --- | --- | --- |
| "No mechanism can beat a same-information, same-memory second readout" ⇒ "beat the rivals" must be a *structural-only* claim | **Bayes premise kept. "Structural only" withdrawn.** | "Bayes premise right, 'structural only' wrong: equal memory != equal retained info; learning/approx/compute/robustness advantages testable." The optimality theorem binds only the *exact posterior*. Bounded, quantized, learned or damaged implementations at equal memory can retain different information, and their differences are empirical/analytic questions. |
| D-C4-1: PRM-upstream vs GWT-downstream as a theory opposition | **Withdrawn as a theory contrast.** Restated as two coexisting causal roles in frozen variants (§2). | "HOT-upstream vs GWT-downstream is not a general opposition (freeze specific model variants + causal graphs)". |
| D-C4-2: PP predicts a precision lesion moves type-1 | **Corrected.** Choices, first-order beliefs and sensory processing are separated (§2.3). | "PP CAN preserve choices after precision lesion (distinguish unchanged choices / first-order beliefs / sensory processing)". |
| D-C4-4: RPT/IIT "not adjudicable by any card" | **Narrowed.** The unfolding argument covers only input-output-equivalent systems. | "unfolding only covers I/O-equivalent systems, interventions/internal measures can discriminate". |
| C4 criterion: ledger wording + "type-1-irrelevant variable" | **Replaced** by Astra's conjunction (§1). | Astra #3. |
| M1 "best candidate (structural)" | **REDUCED on the W_sym objective** (explicit mapping, §3.2). No demonstrated advantage elsewhere. | Astra #3 rule. The mapping is constructed in §3.2. |
| C4-F1 as the cheapest decisive C4 falsifier | **Withdrawn as a C4 card** (balanced-prior confound, §3.3). Lemma 1 is kept only as a world-property fact. | "C4-F1 confound: balanced prior, r>1/2 -> choice follows bit for all r; skewed prior doesn't uniquely identify PP. One bit != higher-order content." |

---

## 1. Replacement C4 criterion (Astra's conjunction, verbatim as recorded)

> "Distinct-evaluation criterion = conjunction: (referent) predicts own first-order
> correctness with interventions separating system vs evidence changes; (selective causal
> content) swap/corrupt evaluator content holding full first-order state -> directional
> evaluation errors + specified downstream consequence, matched rescue reverses; (reduction)
> same adaptive rival gets same info/resources/interventions, compare whole
> intervention-response pattern. Detachable head makes lesionability trivial; update closure
> != second-order status."

How v2 applies the three parts:

1. **Referent.** The evaluator's target is the *own first-order correctness*. The design must
   contain at least one intervention that changes the **system** (own channel or
   implementation) and one that changes the **evidence** (world-side signal quality) while
   matching their effect on raw first-order accuracy. A candidate whose responses cannot tell
   these apart has no demonstrated self-referent.
2. **Selective causal content.**
   - Swap or corrupt the evaluator's content while holding the **full** first-order state
     fixed, including any posterior, precision or regime belief the first-order system
     holds.
   - Required result: directionally predictable evaluation errors (over- or
     under-confidence in the predicted direction), plus one pre-specified downstream
     consequence (e.g. abstain or request more evidence).
   - A matched rescue (restore the content) must reverse both.
3. **Reduction.**
   - A single adaptive rival gets the same inputs, the same resources (state bits, parameters,
     compute) and the same intervention set.
   - The comparison is the **whole intervention-response pattern**, not a scalar score.
   - Two traps to avoid:
     - **Detachable head.** Lesionability of a detachable head is trivial and earns nothing
       by itself.
     - **Update closure.** A state that updates only from its own past (update closure) is
       not thereby second-order.

This replaces v1 §1's working criterion inside this queue only. It does **not** amend the
ledger. A ledger change would be a separate gated proposal.

---

## 2. Corrected theory analysis: frozen variants, causal graphs and coexisting roles

### 2.1 Frozen variants

Differential predictions below hold **only** for these graphs. Notation:
- S: sensory input
- F: first-order representation
- D: decision variable / choice
- E: evaluator output
- π̂: precision estimate
- W: workspace

| Id | Frozen variant (source) | Causal graph (edges only) | What the graph is silent on |
| --- | --- | --- | --- |
| V-FO | Single-variable confidence readout (Kiani & Shadlen 2009) | S → F → D; F → E | No extra evaluator state. meta-d′ ≤ d′ only through readout noise. |
| V-PP | Precision-weighted hierarchical prediction (Friston 2010) | S → prediction error ε_s; π̂ → (gain on ε_s); ε_s → F (posterior); F → D; F, π̂ → E | Whether E is a separate population. Here E reads posterior and precision. |
| V-HOSS | Higher-order state space (Fleming 2020) | S → F; F → H (inference over "presence/reliability" of F); H → E | Hybrid PP/HOT. H is inferred within one generative model. |
| V-PRM | Perceptual reality monitoring (Lau 2022; Gershman 2019 discriminator reading) | S → F; F (+ generator efference) → tag T; T gates F → downstream consumers C (belief, control, broadcast) | Whether T also feeds a confidence report. Lau says it "facilitates" metacognition. |
| V-GNW | Global neuronal workspace (Dehaene & Changeux 2011) + self-monitoring as a separate dimension (Dehaene, Lau & Kouider 2017) | S → F → (ignition) W → broadcast → C; W → M (self-monitoring) → E | Pre-workspace monitoring. |
| V-RPT | Local recurrence (Lamme 2006) | S ⇄ F (recurrent); F → D | No evaluator commitment. |
| V-IIT | IIT 4.0 (Albantakis et al. 2023) | Whole-system cause-effect structure; no functional graph is privileged | Not a functional model. Butlin et al. (2023) exclude it as incompatible with computational functionalism. |

### 2.2 Gate, read and precision as coexisting causal roles (analysis only; N4 untouched)

The three roles are defined on edges, not on theories:

- **Gate role:** evaluator output controls which first-order content reaches downstream
  consumers (V-PRM edge T → gate).
- **Read role:** evaluator reads already-available content and drives report or abstention
  without altering what consumers receive (V-GNW edge W → M → E).
- **Precision role:** the reliability estimate re-weights evidence inside first-order
  inference (V-PP edge π̂ → gain).

One system can instantiate all three at once. A lesion identifies **which role a given
variable plays in that system**. It does not identify a theory. Any discrimination between
theories needs, at a minimum, a frozen variant whose graph *lacks* a role, plus an
intervention whose predicted outcome differs because of that absence.

Role-level lesion signatures (to verify per graph):

| Lesion of the reliability variable | Downstream consumer input | Choice D | First-order belief F | Sensory processing (ε_s gain) | Report/abstention E |
| --- | --- | --- | --- | --- | --- |
| Gate role | changes | changes iff D reads consumers | unchanged | unchanged | changes |
| Read role | unchanged | unchanged | unchanged | unchanged | changes |
| Precision role | changes via F | **may be unchanged** (§2.3) | changes | changes | changes |

### 2.3 Predictive processing: three levels, kept separate

In V-PP, a lesion or corruption of π̂ (or of a regime belief b that sets it) acts on:

- **(i) Sensory processing: always.** The prediction-error gain changes by definition.
- **(ii) First-order belief: generically.** The posterior P(X | data, b) changes in
  magnitude.
- **(iii) Choice: not necessarily.** D = argmax is invariant whenever the change in b
  preserves the argmax. In the v1 world W_sym (balanced prior, symmetric channel, odd n),
  Lemma 1 shows the argmax is invariant for **every** b with all ε_r < 1/2. So V-PP predicts
  unchanged choices there.

**Correction to v1 D-C4-2.** "Precision lesion moves type-1" was wrong at level (iii) in
W_sym. "Type-1 invariance" in v1 meant choice invariance only. It held while first-order
belief changed, so it does **not** separate V-PP from V-PRM, V-HOSS or V-GNW.

### 2.4 Unfolding argument, restricted

Doerig et al. (2019) apply to systems that are **input-output equivalent**. For such pairs,
no behavioural test separates a recurrent from an unfolded feed-forward realization.
Interventions on internal states (lesions, clamps, perturbation responses) and internal
measures can separate them.

**Correction to v1 D-C4-4.** RPT- and IIT-relevant *causal structure* is not adjudicable by
**I/O-only** cards. It can be discriminated by intervention cards. Whether such a structural
discrimination bears on those theories' consciousness claims is outside this queue (C7
boundary). v1's "[derived] IIT cut tension" is downgraded to an unsupported conjecture and
should not be cited.

### 2.5 C5 differentials: same discipline

v1 §2.2 rows D-C5-1 to D-C5-4 remain *hypotheses about frozen variants*:
- V-SMT (Seth & Tsakiris 2018; Metzinger 2003);
- V-AST (Graziano & Webb 2015; Wilterson & Graziano 2021);
- V-comparator (Frith et al. 2000).

None is a theory-level opposition until its causal graph is written down and an intervention
with a variant-specific outcome is specified. No C5 card is drafted here.

---

## 3. M1 and C4-F1

### 3.1 M1 (recap)

M1 is a persistent belief b_t = P(R_t = B | past agreement pattern) over the regime of the
agent's own first-order channel. In W_sym it gives:

- confidence c_t = q(u_t, b_t) = Σ_r P(r | u_t, b_t) · P(correct | u_t, r);
- abstention 1[c_t < θ];
- E1 is its one-bit realization, with b replaced by u_{t−1}.

### 3.2 Explicit mapping to adaptive selective prediction ⇒ REDUCED (on the W_sym objective)

**Target class A_thr (adaptive-threshold selective prediction).**
- A fixed, static confidence score s(u_t). Take the static selective-prediction score
  q_R1(u_t), or the majority margin; any score with s(U) > s(S) works.
- A threshold θ_t = τ(m_t) set by a recursively updated state m_t.
- Abstain iff s(u_t) < θ_t.
- This is the selective-prediction form of Geifman & El-Yaniv (2017) (a score plus a
  threshold) with the threshold made adaptive, as in online-calibration schemes such as
  Gibbs & Candès (2021).
- Unlike Gibbs & Candès, the update here is driven by unlabeled agreement history, not by
  labelled errors (see caveat C2).

**Claim.** For every operating threshold θ, M1's abstention policy equals a member of
A_thr with m_t = b_t (M1) or m_t = u_{t−1} (E1).

**Proof (analytic, no computation).**

1. Per regime, P(correct | U, r) > P(correct | S, r): 729/730 > 9/10 for G, and 27/35 > 3/5
   for B (v1 §4.4, exact).
2. P(U | G) = 73/100 > P(U | B) = 7/25. So for every prior b, P(G | U, b) ≥ P(G | S, b).
3. P(correct | ·, G) > P(correct | ·, B) for both values of u.
4. Hence q(U, b) > q(S, b) for every b. The U-mixture puts weakly more weight on the larger
   G-terms, and every term is larger.
5. So for each b, the abstention set {u : q(u, b) < θ} is a down-set of {S < U}. That is
   exactly {u : s(u) < τ_θ(b)} for a b-dependent cutoff τ_θ(b): set the cutoff above s(U) if
   both cells abstain, between s(S) and s(U) if only S abstains, and below s(S) if neither
   abstains.
6. The state recursion is identical (m_t := b_t, with the same forward-filter update), so
   the two policies coincide on every history. ∎

**Graded confidence.** Add a state-conditioned recalibration map κ(s, m) = q(u, m), a
2-entry table per state. This is a standard post-hoc recalibration, so M1's reported
confidence also maps into the class.

**Intervention-matching.** Under the identification m ≡ b, every intervention on M1's state
(swap, corrupt, rescue) is the same intervention on the rival's state, so the intertwining
condition holds trivially. **The whole intervention-response pattern is identical in
W_sym.**

**Log entry (proposal for a gated ledger v2; not applied).**

| Field | Entry |
| --- | --- |
| mechanism | "self-channel reliability filter (M1/E1)" |
| reduction | "adaptive-threshold selective prediction with state-conditioned recalibration (explicit map m≡b, §3.2)" |
| scope | W_sym only, objective = type-2 Brier and abstention at every θ |
| status | **REDUCED** |
| outside W_sym | No demonstrated advantage. No other world analysed. |
| belief_changed | "a persistent reliability belief is not, by itself, distinct evaluation" |

> **Ruling R-A1 (ACI Research Specialist, 2026-10-20 15:25 EDT; additive): REDUCED confirmed.**
> Constitution v3 requires the strongest simpler rival at information parity. Adapting a
> threshold from unlabeled agreement is ordinary unsupervised or self-consistency
> calibration, so it counts as *conventional* adaptive selective prediction; the class is
> not limited to label-driven updating (e.g. Gibbs & Candès 2021). **Definitional note,
> open to contest:** a later reviewer who restricts "conventional" to label-driven
> adaptation would downgrade this entry to "no demonstrated advantage on that objective",
> with the §3.2 mapping kept as a near-reduction. The proof is unaffected either way.

### 3.3 The balanced-prior confound in C4-F1 (explicit)

- **(a) Choice invariance is a property of the decision problem, not of the evaluator.**
  - With π = 1/2, a symmetric channel and odd n, the choice follows the majority bit for
    every reliability r > 1/2 (Lemma 1).
  - Every frozen variant in §2.1 predicts this, including V-PP, which keeps choices and
    changes beliefs (§2.3).
  - So v1 gate G1/G4 ("z-lesion changes no type-1 decision") cannot discriminate a separate
    evaluator from a precision role. It is satisfied by any Bayesian system.
- **(b) The skewed-prior control does not identify PP.**
  - In W_asym, the coupling of choice to reliability (v1 Lemma 2) is predicted by **any**
    Bayes-optimal decision maker with a regime belief: V-PP, V-HOSS, and V-FO with a
    hierarchical posterior.
  - A FAIL there would not license "reduces to PP precision".
- **(c) In W_sym, M1's confidence is a monotone readout of a first-order belief.**
  - Under V-PP, c_t = max_x P(x | u_t, b_t), i.e. the maximum of the hierarchical first-order
    posterior.
  - If "first-order state" is defined as that posterior (rather than v1's memoryless
    majority module), the ledger falsifier "only a monotonic first-order transform" applies
    directly.
  - v1's pass depended on a **chosen** first-order boundary.
- **(d) One bit is not higher-order content.**
  - z = u_{t−1} is a lagged sample statistic. Its content is "the last trial was split", not
    "my estimate is unreliable".
  - Under Astra's referent clause, nothing in W_sym separates system change from evidence
    change. Own-channel noise and world noise are observationally identical there, so the
    referent clause cannot be met in W_sym by construction.
- **(e) Disposition.** C4-F1 is **withdrawn as a C4 card**. Lemma 1 and the hand-computed
  E1 vs R1 Brier gap (≈0.0017, unreplayed) are retained only as facts about W_sym (static
  vs adaptive selective prediction). They carry no C4 consequence.

> **Ruling R-A3 (2026-10-20 15:25 EDT; additive).** The v1 hand values ≈0.0017 (E1 vs R1)
> and ≈0.0133 (oracle ceiling) are **SUPERSEDED**. No exact replay is needed, since C4-F1
> is withdrawn. Do not cite them.

---

## 4. Decision package (DESIGN ONLY): M1 vs adaptive rival under matched interventions

**Card id (proposed):** C4-CMP1. **Class:** ANALYTIC. **Authorization:** none. Execution of
any certificate below needs Aidan's approval. Constitution v3 also gates any first C4
study.

> **Ruling R-A2 (ACI Research Specialist, 2026-10-20 15:25 EDT; additive).** C4-CMP1 counts
> as *first C4 research* under constitution v3, so it stays **design-only until Aidan
> approves it**. W_ref's rates, the state budget B and the action costs c_r and c_s stay
> **deliberately unset**. Do not freeze them before approval.

### 4.1 Why the card exists

- §3.2 settles W_sym by proof: constructive equivalence.
- The open question is whether **any** declared world and intervention set gives M1 a pattern
  that **no** member of a frozen adaptive rival class reproduces at matched information,
  resources and interventions.
- It must also do so while meeting Astra's referent clause, which W_sym cannot.

### 4.2 Frozen objects (to be fixed before any computation)

**Worlds:**
- **W_sym** (v1 §4.1). Included as the known-equivalence anchor and a replay check of §3.2.
- **W_ref** (new; minimal referent world). The referent clause needs the system and evidence
  dimensions to be separable.
  - Hidden X_t, uniform.
  - Three world samples per trial, each flipped by world noise w_{E_t}, with evidence regime
    E_t ∈ {lo, hi} (Markov).
  - Each world sample is read through **two** internal replicas, each flipped independently
    by internal noise ε_{R_t}, with own regime R_t ∈ {G, B} (Markov, independent of E).
  - The agent sees 6 bits.
  - Within-pair replica disagreement is informative about R. Across-pair disagreement with
    agreeing replicas is informative about E.
  - **All rates are to be frozen once, with a written rationale, before any value is
    computed. No retuning.**

**Downstream actions (the specified consequence):**
- **A_repair:** at cost c_r, resets R to G next trial.
- **A_resample:** at cost c_s, draws 3 more world samples this trial.
- Pre-declared consequence clause: a system-change belief should raise A_repair; an
  evidence-change belief should raise A_resample.

**Candidate M1_B:** the Bayes forward filter over (R, E), quantized to B bits of persistent
state, with B ∈ {1, 2} frozen. It outputs confidence, abstention and the two action
propensities.

**Rival class A_B (frozen):** every member uses the same 6-bit inputs, the same B bits of
persistent state, the same action set, the same parameter/compute ceiling and the same
interventions. Two sub-classes, reported separately:
- **A_B^thr:** static score + adaptive threshold + state-conditioned recalibration + an
  action rule reading the same state. This is the conventional selective-prediction form.
- **A_B^all:** all deterministic B-bit recursions over the same inputs. This is the full
  same-resource class and is finite at fixed B.

**Matched intervention set (identical for candidate and rivals):**

| Id | Intervention |
| --- | --- |
| I1 | Swap evaluator state with its value from a different reachable history, holding the full first-order state fixed (samples, and any first-order posterior if the graph has one). |
| I2 | Corrupt evaluator state to a fixed value. |
| I3 | Matched rescue: restore the pre-I1/I2 state. |
| I4 | System change: force R switch (G→B). |
| I5 | Evidence change: force E switch (lo→hi), matched to I4 on raw majority accuracy. **The match is to be shown analytically, not tuned.** |
| I6 | Detachable-head lesion: recorded but **not credited**, per "Detachable head makes lesionability trivial". |

**Response pattern recorded per intervention:**
- type-2 Brier;
- abstention rate;
- A_repair and A_resample propensities;
- choice D;
- first-order belief (where the graph defines one);
- recovery profile over the following trials.

### 4.3 Three pre-declared outputs

1. **CONSTRUCTIVE EQUIVALENCE.** An explicit map Φ from M1_B's states to the states of some
   member of A_B^thr (or A_B^all, reported separately) that commutes with:
   - the update;
   - the outputs and actions;
   - every intervention I1–I5 (Φ∘I = I′∘Φ);
   - verified on all reachable states.

   Logging: M1 is REDUCED in that world, naming the sub-class. W_sym is expected here by
   §3.2.
2. **VERIFIED SEPARATING CONTRAST.** A specific intervention and world where M1_B's
   whole-pattern response differs from **every** member of the frozen sub-class, with a
   certificate covering the whole class and an independent replay. Additionally, the
   referent clause (distinct I4 vs I5 responses in the pre-declared action direction) and
   the selective-causal-content clause (I1/I2 directional errors + action consequence; I3
   reverses) must both hold for M1_B.

   Logging: "M1_B separates from adaptive class X in world Y on intervention Z". The C4
   ledger status stays NOT_ESTABLISHED, because there is no learned or built system
   (Q-LEARN/Q-CAUSE untouched).
3. **UNRESOLVED.** Any of:
   - class coverage incomplete;
   - replays disagree;
   - the I4/I5 accuracy match cannot be shown analytically;
   - the result depends on an unfrozen choice.

   Logging: no belief change; errata; one re-replay; then park.

### 4.4 Thirteen admission answers

| # | Answer |
| --- | --- |
| Q1 | C4, as a bounded prerequisite (Q-EXIST / Q-NECESSITY in an analytic world). Can a reliability-tracking evaluator meet Astra's conjunction, and does it differ from an adaptive selective-prediction rival at matched info, resources and interventions? |
| Q2 | ONE question: in W_ref at frozen B, is M1_B's whole intervention-response pattern (I1–I5) reproducible by some member of the frozen adaptive rival class? |
| Q3 | It is falsified, and the card's "distinct evaluation" conclusion defeated, if output 1 (constructive equivalence) holds for A_B^thr. Output 1 for A_B^all with no A_B^thr equivalence would defeat only "conventional selective prediction suffices". Failure of the referent clause (identical I4/I5 action responses) defeats the referent claim regardless of rivals. |
| Q4 | Strongest simpler explanation: adaptive selective prediction with state-conditioned recalibration, i.e. A_B^thr (static score, adaptive threshold, recalibration), with the same 6-bit inputs, B bits, action set, compute ceiling and interventions. Behind it sits A_B^all, the full same-resource class. Known equivalence in W_sym (§3.2). |
| Q5 | Necessary because: v2 §3.2 (M1 REDUCED in W_sym); v1 C4-F1 withdrawn (§3.3); AC117 P-G5/P-G6 (a same-signal readout matched the monitor); `C1_RELIABILITY_DISPOSITION_v1.md` ("estimating ε alone" caution); Astra #2 and #3. No frozen card tests the referent clause or compares whole intervention patterns. |
| Q6 | After separating contrast: propose (human gate) a Q-LEARN card asking whether a learned agent acquires the separating state, and a Q-CAUSE card on a built system with the same I1–I5. The ledger C4 row gains an analytic evidence row; status unchanged. |
| Q7 | After constructive equivalence: log a REDUCED collapse entry for W_ref and record "reliability tracking = adaptive selective prediction under matched interventions". The C4 line then needs a mechanism with different *content* (e.g. the M3 source monitor), not more of M1. After UNRESOLVED: errata, re-replay, park. No retuning of W_ref rates in either case. |
| Q8 | Minimum apparatus: an analytic proof where possible (W_sym is done in §3.2), plus a finite exact certificate over A_B for W_ref at B ≤ 2 (finite class enumeration; solver-like, so approval required), with an independent replay. No neural model, organism or training. |
| Q9 | Organizational cognition at the analytic level (does an evaluator role differ from an adaptive calibration role under intervention?). Not substrate competence. Robustness under I2 is reported separately as an engineering quantity. |
| Q10 | Ceiling (best case): "In frozen world W_ref at B bits, M1_B's intervention-response pattern meets the referent and selective-causal-content clauses and is not reproduced by adaptive class X." **NOT established:** learning (Q-LEARN), causal use in any built system (Q-CAUSE), necessity outside W_ref, higher-order content beyond what the separating state encodes, any theory credit (roles ≠ theories, §2.2), any C7 claim. |
| Q11 | C4. Unsupported prerequisites: C2 acquired representation (PARTIAL), C3 (PARTIAL); C4 Q-LEARN/Q-CAUSE. |
| Q12 | O0 throughout. A_repair is a modelled action on a supplied regime variable, not organism maintenance, so no O1–O3 claim follows. |
| Q13 | Equivalence: belief "reliability tracking is adaptive selective prediction under matched interventions" (collapse entry). Separating contrast: belief "an evaluator separating system from evidence change is not reproduced by adaptive class X in W_ref" (analytic evidence row; status unchanged). UNRESOLVED: no change. |

**Certificate coverage.**
- W_sym: complete by proof (§3.2).
- W_ref: every reachable state of M1_B × every member of A_B^thr (and separately A_B^all)
  × I1–I5, at the frozen B only.

**Bounded UNRESOLVED rule:** incomplete coverage, replay disagreement, or an I4/I5 match not
shown analytically. One re-replay, then park.

**Prediction (stated before any computation):** constructive equivalence for A_B^all is
likely, because M1_B is itself a B-bit recursion and therefore a member. The informative
contrast is against A_B^thr. Even there, the separating case needs a world where the action
rule must read a *system-vs-evidence* distinction that a single scalar threshold cannot
carry. W_ref is built to make that possible, not guaranteed.

---

## 5. Queue after v2

| Order | Item | Status |
| --- | --- | --- |
| 1 | C4-CMP1 (§4) | Design only; awaits human gate |
| — | C4-F1 | Withdrawn as a C4 card (§3.3). Lemma 1 retained as a world fact. |
| — | C4-F1b | Not started (instruction). Superseded in part by C4-CMP1's W_ref. |
| later | C4-L1, C5-Q1…Q4 (v1 §5) | Unchanged. Each needs a frozen variant graph (§2) before any differential claim. |

---

## 6. Caveats

- **C1.** Astra's text is a condensed record. "Exact wording" is exact to that record, not
  to the original consultation.
- **C2.** *(Resolved by Ruling R-A1, §3.2: unlabeled adaptation counts as conventional; the entry stays REDUCED; the note is kept for contest.)* The §3.2 mapping target uses *unlabeled* agreement-driven threshold updates.
  Adaptive conformal inference (Gibbs & Candès 2021) updates from labelled miscoverage.
  If the Specialist counts only label-driven adaptation as "conventional adaptive selective
  prediction", downgrade §3.2's status to "no demonstrated advantage on that objective" with
  the mapping recorded as a near-reduction. The mapping itself is a proof either way.
- **C3.** *(See Ruling R-A2, §4: stays unset until Aidan approves.)* The W_ref rates, B, c_r and c_s are deliberately unfrozen here. They must be
  frozen with a rationale before any certificate. The I4/I5 accuracy match must be
  analytic.
- **C4.** Hand values carried from v1 (≈0.0017, ≈0.0133) are SUPERSEDED (Ruling R-A3); no replay is needed.
- **C5.** Frozen-variant graphs in §2.1 are my compressions of the cited sources. They are
  meant to be reviewed, not cited as the authors' own diagrams.

---

## 7. Citations

**No new citations were added.** Every reference below was verified in v1 (§7 there; Crossref,
arXiv or publisher pages, 2026-10-20). Partial checks carried from v1:

- **Geifman & El-Yaniv (2017):** the NeurIPS venue is taken from a reference list.
- **Gibbs & Candès (2021):** arXiv:2106.00170 verified; venue not verified.
- **Lau (2022):** the PRM gating description was checked via reviews, not the book text.
- **Dehaene, Lau & Kouider (2017):** the C1/C2 distinction is from memory; the full text was
  not re-read.

References used here:
- Albantakis et al. 2023
- Butlin et al. 2023 (arXiv:2308.08708)
- Dehaene & Changeux 2011
- Dehaene, Lau & Kouider 2017
- Doerig et al. 2019
- Fleming 2020
- Frith, Blakemore & Wolpert 2000
- Friston 2010
- Geifman & El-Yaniv 2017
- Gershman 2019
- Gibbs & Candès 2021
- Graziano & Webb 2015
- Kiani & Shadlen 2009
- Lamme 2006
- Lau 2022
- Metzinger 2003
- Seth & Tsakiris 2018
- Wilterson & Graziano 2021

Repo sources are as in v1 (HEAD `32cfbe6`, unmodified).
