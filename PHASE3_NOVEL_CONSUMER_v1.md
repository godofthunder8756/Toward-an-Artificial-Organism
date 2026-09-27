# Phase-III novel-consumer test v1 — reusing frozen W for a new specialist without retraining the inference

2026-09-27. Deliverable for the G7 card (t_0f6dae3e): *can a NEW specialist trained
on a novel task reuse frozen W without retraining the inference machinery — establishing
W as reusable content rather than a behavior-tied activation?* Category B/F — **design /
formalization; do not execute.**

This is a **derived document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It specifies the novel-consumer test
that G10 implements **on top of** the six frozen arms of `PHASE3_ARCHITECTURES_v1.md`
(G4) and the three specialists of `PHASE3_SPECIALISTS_v1.md` (G3), on the task of
`PHASE3_INFERENCE_TASK_v1.md` (G2). It does **not** define the training objective or
the frozen protocol (G10's); it fixes only the frozen-reuse measurement that G9's
reduction question (6) ("is the novel-consumer test merely ordinary representation
transfer?") and G10's gate set then read.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is a consciousness claim. (2) Seeds are
the replication unit; every endpoint is a planned-denominator readout reported per seed
family, never a per-family guarantee (AC39/AC68). (3) "Reusable content" is the claim
under test, never the premise: a new consumer that *does not* reuse W to the ceiling is
an admissible Phase-III result, not a defect to paper over (G9's standing bar — a simple
rival winning is acceptable). (4) The G0 demotions bind: V is absent, the maintenance
rule A is fixed/reactive (verdict D), the new specialist does **not** re-introduce a
learned allocator, and S_reg remains a readout (G3 §8). (5) The novel task is over the
**same** latent cause and the **same** token stream as G2 — "novel" names the function
computed, never the information.

---

## 0. The one-paragraph answer

The novel-consumer test freezes the inference network **and** W after the initial
training (encoder, W's acquisition write, and the three specialists S_pol / S_plan /
S_reg), leaves W's paid maintenance π running, and attaches a **new specialist** trained
on a **novel task that requires the same latent cause z** — with the new specialist
reading only W and its training gradient barred from the frozen core. The novel task is
**not** a new environment and **not** a new generative model: it is a **new function of
the same belief**, chosen so that the analytic optimum is a function of the sufficient
statistic W that no trained specialist was taught to compute. The primary new consumer
is **S_conf**, the calibrated-posterior readout `P̂ = σ(W)` (a graded proper-scoring
objective — it needs the **full b-bit magnitude** of W, which none of the three trained
specialists ever used); its companion is **S_bias**, an asymmetric-cost forced decision
`ẑ = A iff W > θ_bias` (a **shifted decision boundary**, same output alphabet as S_pol,
different threshold). If the candidate's frozen W lets S_conf reach the Bayes-calibrated
ceiling and S_bias reach the asymmetric-cost optimum — while the old three specialists'
outputs stay **byte-identical** — then W is *reusable content* (a complete sufficient
statistic), not a *behavior-tied activation* (a hidden state entangled with the specific
outputs it was co-trained to support). The rival arms freeze their own core the same
way and expose exactly the property each removes: **R1** cannot serve the new consumer
without a fourth encoder (retraining, forbidden), a piggyback on one private W_i (not
shared), or a 3×-content concat (unfair); **R2**'s h_t is reusable only as an external
probe or a joint retraining that damages the old heads (the modularity/interference
contrast); **R3**'s raw history is reusable but at M tokens instead of b bits (the
information-required contrast); **R4**'s supplied S_t is *also* reusable and is the
**ceiling** — the candidate must **match** it (equivalence, not `>`), separating only on
the learned/paid-maintained status (G2's contrast) and the maintenance economy; **R5**'s
three identical copies tie on performance and lose only on single-write identity. The
test's load-bearing discriminations are therefore **structural** (one frozen W serves a
fourth consumer with zero retraining and b bits; one write reaches all four) and
**empirical** (the learning-curve sample cost, the frozen-probe ceiling of R2's h_t) —
and it is scoped strictly to *reuse by one added consumer*, never to "global broadcast"
or a "workspace seat" (O3/GWT), which the card's "transfer alone ≠ global accessibility"
caution excludes.

---

## 1. What "novel consumer" means — and what it is forbidden to mean

The card's distinction is between two hypotheses about what W *is* after training:

- **Reusable content.** W is a *complete* sufficient statistic of z (G2 §2.1). Because
  it is complete, **any** downstream function of z is computable from W alone — a new
  consumer can be trained to compute a never-before-trained function of z by reading W,
  with no access to the history and no retraining of the inference. The reuse is a
  theorem about the representation, not a training artifact.
- **Behavior-tied activation.** W is a hidden state that was co-adapted to the three
  specific specialists; it carries only the quantities those three happened to need
  (a sign bit, two thresholds, one magnitude gate) and nothing more. A new consumer
  would then find W insufficient and would need the history back, a retrain of the
  encoder, or a new private inference.

The test separates these by choosing a novel task whose optimum **requires a quantity no
trained specialist used**. The three existing specialists consume W as follows (G3 §4):

| specialist | function of W | invariance class | what of W it uses |
| --- | --- | --- | --- |
| S_pol | sign (ẑ = A iff W > 0) | odd, magnitude-invariant | the **sign bit** |
| S_plan | two-sided threshold (commit iff \|W\| crosses a/b) | sign-and-magnitude | sign + two coarse magnitudes |
| S_reg | even gate (preserve iff \|W\| ≥ θ) | even, sign-invariant | coarse \|W\| vs θ |

**None of the three ever used the precise graded magnitude of W** as a value — S_pol is
magnitude-invariant, S_plan and S_reg only compare \|W\| to a threshold. The novel task
that most sharply tests completeness is therefore one whose optimum is a **strict,
continuous, graded function of W**: the calibrated posterior. A behavior-tied W that
retained only sign + coarse thresholds could not support it; a complete W can, to the
Bayes ceiling.

Three readings of "novel consumer" are possible and two are excluded:

1. **FORBIDDEN — "novel" = a new generative model / new environment.** If the latent
   cause, likelihood, or token stream changed, the sufficient statistic would change and
   W would not be reusable *by construction* — that would test environment transfer, not
   content reuse. The novel task here keeps z, the λ's, and the token stream identical
   (G2 §1); only the **function** computed over the belief is new.
2. **FORBIDDEN — "novel" = a relabelled old consumer.** A fourth head trained against an
   output isomorphic to one of the three existing objectives (e.g. another sign readout
   at threshold 0) is not novel; it is the single-objective-collapse rival (G3 §1) in a
   new coat. The new consumers below differ in objective kind and in the *function of W*
   (a new invariance class, and a new decision boundary), never in label alone.
3. **KEPT — "novel" = a new function of the same sufficient statistic.** A consumer whose
   optimum is a function of S_H = W that none of the trained specialists computes, over
   the identical generative model. This is exactly the test that W is *content* (complete)
   rather than *behavior-tied* (co-adapted).

**The transfer-alone caution (the card's explicit bar).** A capacity-capped readout that
can learn a new function from frozen W is *ordinary representation transfer* — the same
frozen-features probe G8's decoder uses, and it is **necessary but not sufficient** for
the claim. What lifts the test above bare transfer is the **architecture-controlled
comparison**: the same instrument is applied to six arms whose organizational property
(shared vs unshared, learned+paid vs fixed+free, compressed vs raw, modular vs
monolithic) is the only thing that varies (G4 §8), and the four measures below pin down
the *organizational* facts — zero-retraining reuse, the information required, the
single-write-reaches-four identity, and the byte-identity of the old consumers — that a
bare probe does not. §9 states this for G9's reduction question (6) explicitly.

---

## 2. The novel task(s): two new functions of the same belief

Both new consumers read the **same maintained W** and are scored at t = H on the **same
episodes** as the original three (same seeds, same z, same token stream). They are
attached *after* the core is frozen (§3). Neither reads the history, neither reads z, and
neither is a forward input to any old specialist.

### 2.1 S_conf — the calibrated-posterior readout (primary, new invariance class)

- **Role.** A graded belief readout: emit the system's posterior probability of cause A,
  `P̂(A | x_1..x_H) = σ(W_H)`, as a real in [0, 1]. This is the consumer that needs the
  **full b-bit magnitude** of W — the quantity none of the three trained specialists used.
- **Inputs.** W only. **No** x_t (the current token would leak z in accumulation — G8's
  L7 pathway), no history, no bookkeeping. A context-free readout: the posterior is a
  function of the sufficient statistic alone (G2 §2.1 Eq. 3).
- **Function of W.** `P̂ = σ(W)` (logistic). **Strictly monotone increasing**, continuous,
  graded: it uses every increment of W's b-bit value, not a threshold.
- **Objective kind.** **Calibration / proper scoring** — log loss (or Brier, G10's choice,
  recorded) against z. This is a *different kind* from S_pol's accuracy, S_plan's
  speed-accuracy-cost, and S_reg's resource economy: it scores the *probability*, not a
  decision, and a wrong-but-confident belief is penalized more than a wrong-but-timid one
  (which is precisely what S_reg's even gate and S_pol's sign cannot see).
- **Output space.** [0, 1] graded — distinct from {A, B}, {commit-A, commit-B, postpone},
  and {preserve, release}.
- **Invariance signature.** **Order-isomorphic to W (a fourth class).** `σ(−W) = 1 − σ(W)`
  (belief reversal → probability complement, so it is *not* even), and it is sensitive to
  **every** magnitude change (so it is *not* magnitude-invariant like S_pol). It therefore
  collapses with none of the three: S_pol is magnitude-invariant, S_plan is two-sided
  thresholded, S_reg is even. Adding S_conf preserves the G3 §3.2 non-collapse guarantee
  and extends it to a fourth class.
- **Analytic optimum (kept as the rival, derived before training).** `P̂* = σ(S_H)`, the
  true posterior (G2 §2.1 Eq. 3). The Bayes-calibrated log loss is the posterior entropy
  `H = E[−log P̂*]`, the ceiling a readout of the exact sufficient statistic attains. The
  candidate's W is the b-bit quantization of S_H (resolution ≈ 0.39 < λ_lo = 0.35, G2
  §4.2), so it must reach the ceiling **to the quantization floor** — equivalence, not
  excess (AC16/17: R4 is the ceiling rival, G2 §4.1).
- **Why it is the sharpest completeness test.** S_pol, S_plan and S_reg are all
  *discrete threshold* functions of W; they could be served by a W that had lost every
  bit of graded magnitude and kept only "sign" and "strong/weak". S_conf **cannot** — a
  behavior-tied W that retained only those coarse bits would leave S_conf off the
  calibrated ceiling, and the only repair would be to re-open the history (AVAILABLE
  failure) or retrain the encoder (reuse failure). S_conf reaching the ceiling from
  frozen W alone is therefore the content claim in its strongest single-consumer form.

### 2.2 S_bias — the asymmetric-cost decision (companion, same class, new boundary)

- **Role.** A second forced-choice decision consumer with **asymmetric error costs**:
  the consequence structure (G3 §2.1's "consequence structure" field) is no longer
  symmetric. Saying A when the truth is B costs `c_AB`; saying B when the truth is A
  costs `c_BA`, with `c_AB ≠ c_BA` (default `c_AB > c_BA`, "A is the risky claim").
- **Inputs.** W only (the sufficient statistic; no x_t, no history).
- **Function of W.** `ẑ = A iff W > θ_bias`, where `θ_bias = log(c_BA / c_AB)` is the
  posterior-odds threshold shifted by the cost ratio. A **new decision boundary**: the
  same sign form as S_pol but centered at θ_bias ≠ 0, not at 0.
- **Objective kind.** **Asymmetric expected cost** — distinct from S_pol's symmetric
  accuracy (G3 §2.1: S_pol's consequence structure is symmetric; here it is not). A
  different objective *kind* (risk), not a scalarization of S_pol's reward.
- **Output space.** {A, B} — **deliberately the same alphabet as S_pol**. This is the
  minimal novel-decision case: a consumer that differs from an existing one *only* in its
  decision rule (the threshold), to show the reuse is of the **content** (the LLR value),
  not of the trained rule.
- **Invariance signature.** Odd about θ_bias, magnitude-invariant — the **same class as
  S_pol**. It is specified *despite* not adding a new class, for exactly that reason: if
  only S_conf were tested, one could object that "reuse" was special to a graded readout;
  S_bias shows a threshold decision at a **new** threshold is equally computable from W.
- **Analytic optimum (kept as the rival).** `ẑ* = A iff S_H > θ_bias`, the Bayes rule for
  asymmetric costs — derived from the same S_H before training (the G2 §2 "derive before
  training" discipline). The candidate differs from it only in learned-vs-fixed update
  and shared-maintained-vs-broadcast, never in the decision form (G2 §4.1, per consumer).
- **Why it matters.** It pins that W carries the *value* of the LLR, not just the three
  trained specialists' threshold bits: a new threshold θ_bias (which no specialist was
  trained to use) is computable from W to the Bayes optimum without re-opening the
  history. It is the "same information, new decision rule" half of the completeness claim.

**The two are a level family, not a menu.** S_conf is the primary (it is the only
consumer in a fourth invariance class and the only one needing the full graded magnitude);
S_bias is the swept companion (the minimal novel decision). Both are attached in every
arm (§5), both are scored at H, and both are held to the same freeze protocol (§3). The
G3 §3.2 differential-scramble check is re-run with four (or five, with S_bias) consumers,
and the §3.2 matrix gains a row: a sign flip sends S_conf to its complement `1−σ` and
S_bias across its shifted threshold, neither of which equals any existing specialist's
response — the non-collapse guarantee is preserved and extended.

---

## 3. The freeze protocol (what "reuse without retraining" means operationally)

The test has a strict two-phase structure; the phases are what make "reuse" measurable
rather than asserted.

1. **Phase 0 — train.** Train the full arm (encoder + W + the three original specialists,
   per G4's topology) to convergence, exactly as G10's training protocol will specify.
   This is the pre-freeze state.
2. **Phase 1 — freeze.** Freeze **everything learned**: the encoder's parameters
   (candidate/R1/R2), W's acquisition/update write, and the three specialists' weights.
   Two things are **not** frozen, and the distinction is load-bearing:
   - **π and A continue** (candidate and R1): W remains *paid-maintained* throughout the
     novel task, by the fixed/reactive rule A on `(s, E, d)` (verdict D, G0 §3.3). The
     new specialist reuses a variable that is still being *held alive* at cost — it does
     not inherit a static snapshot. This is what keeps the MAINTAINED predicate in the
     loop (G1 §2.5): a probe of a *decayed* W would measure the no-maintenance baseline,
     not reuse.
   - **W's content continues to be driven by the frozen encoder** (the acquisition write
     still runs; only its *parameters* are frozen). The new specialist reads the live W,
     which the frozen encoder keeps integrating from the token stream.
3. **Phase 2 — attach and train the new specialist.** Add S_conf (and S_bias) as a
   **read-only head** of the arm's content variable (W / S_t / copy i / W_i / h_t / the
   window, per §5). Train **only** the new head, on novel-task episodes, with **no
   gradient flowing into any frozen parameter**. The old three specialists run alongside,
   untouched, and their outputs are compared to the Phase-1 (pre-extension) run on the
   same seeds for byte-identity (§4.4).

**The freeze is the instrument, not the claim.** "Freeze the inference and W" is what
makes "zero retraining samples" a well-defined number: the candidate's new consumer
costs **zero** episodes of inference re-learning, because the encoder is barred from
updating. Any rival arm that must un-freeze to serve the new consumer (R1's fourth
encoder, §5) is *measured* to cost the full retraining it requires — that cost is the
rival's loss, not a handicap imposed on it (G4 §8 rule 3: R1's robustness variant runs
each encoder at full capacity; the retraining it needs is its defining property, not a
hidden saving the candidate is granted).

**Byte-identity at the intact boundary (P7).** Phase 1 must reproduce the frozen
no-extension run byte-for-byte before any Phase-2 difference is attributed to the new
consumer (AC83's method). In the candidate, the old three specialists' outputs and W's
trajectory must be byte-identical across the Phase-1/Phase-2 boundary on every seed —
any drift is a wiring bug (a gradient leak into the core, or the new head writing W), not
a result (AC85). This is the interference measure in its cleanest form.

---

## 4. The four measures (the card's endpoint set)

Each is recorded per seed (planned denominator, never pooled), per arm, per new consumer
(S_conf, S_bias), with disjoint engineering and finals families (AC39).

### 4.1 Sample efficiency (the learning-curve cost of the *readout*)

The number of novel-task episodes the new head needs to reach its ceiling, measured as
the per-seed learning curve `loss(N) → ceiling`. The quantity is **graded**, so it is
reported as a curve with a prespecified threshold (e.g. "reaches 95% of its ceiling in
≤ N_0 episodes"), never as a bare mean margin (AC16/47). Two sub-quantities, both
reported:
- **Retraining cost** (inference samples): 0 for any arm whose core stays frozen
  (candidate, R4, R5, R3 — none has a learned encoder to retrain; R2's probe). For R1's
  fourth-encoder arm (§5), the full inference-retraining sample count. This is the
  categorical half: the candidate's is **exactly 0** by construction.
- **Readout cost** (head samples): the episodes to fit the new function. Expected low for
  a scalar readout (candidate/R4/R5: a 1-D → sigmoid / 1-D → threshold mapping), higher
  for R2's d_h-dimensional probe and R3's M-token reader. Reported as a curve; the
  ordering is a *prediction*, not a gate.

### 4.2 Frozen-core performance (does the frozen content reach the ceiling?)

The asymptotic novel-task score the new head reaches with the core frozen:
- **S_conf ceiling** = the Bayes-calibrated log loss (posterior entropy, §2.1), attained
  by reading the exact sufficient statistic. The candidate's b-bit W must reach it **to
  the quantization floor** — an **equivalence** gate against R4, never `>` (AC16/17: R4's
  S_t *is* S_H).
- **S_bias ceiling** = the Bayes asymmetric-cost optimum (§2.2).
This is the completeness claim in categorical form: the candidate reaches the ceiling
from frozen W alone, on **every** seed, or W is not complete (a behavior-tied W would
fall short, and the shortfall is the measured incompleteness — reported, not re-classified).

### 4.3 Information required (what inputs the new head minimally needs)

The input dimensionality and content the new consumer consumes to reach its ceiling:
- **Candidate / R4 / R5:** b bits (the scalar), no history, no x_t.
- **R3:** M tokens (the full window, M ≥ H).
- **R2:** d_h bits (the hidden vector, d_h ≥ b).
- **R1:** depends on the wiring sub-arm (§5): 1 W_i (piggyback), 3 W_i (concat), or a
  retrained W_4.
The structural contrast — **b bits vs M tokens** — is the candidate-vs-R3 loss; it is
asserted at the source level (the head reads W, nothing else) and pinned by the
sever-history test extended to the new consumers (G3 §6 gate 5, G1 §2.4-c): hold W fixed
and remove all history access from S_conf/S_bias; outputs byte-unchanged. A new consumer
whose output degrades was reconstructing the history — an AVAILABLE failure, and the
content-reuse claim fails with it.

### 4.4 Interference (does modifying the new specialist damage old consumers?)

After Phase 2, the three original specialists' outputs (and W's trajectory) must be
**byte-identical** to the Phase-1 run, on every seed. This is the modularity fact the
card's "modifying the new specialist damages old consumers" names, and it separates the
candidate cleanly:
- **Candidate:** byte-identity is structural — W is read-only for consumers, the head's
  gradient is barred from the core, the old heads are frozen (G5 §6 I3's consumer-cut is
  the inverse operation, and the same byte-identity logic applies to a consumer *add*).
- **R2:** the monolithic RNN cannot add a consumer *inside* its policy without joint
  retraining, which changes h_t and the old heads. Its two honest sub-arms are (a) an
  **external probe** on frozen h_t (no interference by construction — but then the new
  head is not part of the monolithic policy; it is a bolt-on, which is precisely the
  modularity the candidate *has* and R2 *lacks*), and (b) a **joint retrain** (measured
  interference on the old heads). The contrast is reported, not gated as a prediction
  about R2's numbers.

**What is NOT a measure here.** Aggregate novel-task income (none of the new consumers
has an income; they are discrimination/calibration consumers on the same episodes — the
AC15 confound does not arise); any coordination number (G6's); any leakage rate (G8's);
any π-cut decay (G2's, MAINTAINED). The novel-consumer test is the *reuse* half of N2;
the other halves own their own endpoints.

---

## 5. Per-arm application (the discriminations, and the honest R1 wiring question)

Every arm freezes its core per §3 and attaches the same two new heads. The table states,
per arm, what the new head reads, what the arm's "reuse" costs, and which measure the
arm loses on. Grades are the card's four rivals plus R5 (G4's fifth arm, carried for
completeness).

| Arm | New head reads | Retraining cost | Info required | Frozen-core ceiling | What it loses (if the candidate wins) |
| --- | --- | --- | --- | --- | --- |
| **CANDIDATE (SLW)** | the one W | **0** (frozen encoder) | b bits | must **match** R4 (equivalence) | — (the claim) |
| **R1 private-state** | see the three sub-arms below | sub-arm-dependent | 1 / 3 W_i / retrain | ≈ ceiling (each W_i is a good inference) | **SHARED**: no single content to reuse |
| **R4 suff-stat broadcast** | S_t (free register) | 0 | b bits | **the ceiling** (exact S_H) | nothing on performance — **ties**; separates only on learned/paid-maintained (G2) |
| **R5 separate copies** | copy i | 0 | b bits | ≈ ceiling (identical content) | **the sharing mechanism**: one write must reach 4, not 4 copies |
| **R2 monolithic RNN** | h_t (external probe) or joint retrain | 0 (probe) / full (retrain) | d_h bits | **empirical** (entanglement) | **modularity**: no in-policy consumer addition without retraining |
| **R3 history-access** | x_1..x_M (reader) | 0 | M tokens | ≥ ceiling (full history) | **compressed W**: M tokens vs b bits; sample cost of summarizing |

**The R1 wiring question (resolved here, not deferred).** R1 has three private W_i and
no shared variable; "reuse the content" is under-specified until the new head's input is
fixed. Three honest sub-arms, all run and disclosed:

- **R1-concat.** The new head reads `[W_1, W_2, W_3]` (concatenated). This is the
  *advantaged* rival: 3× the content, 3× the readout capacity (G4 §8 rule 3/4 — the
  asymmetry favors the rival and is disclosed). Its ceiling bounds what R1 can reach by
  throwing content at the problem. It does **not** demonstrate reuse — it demonstrates
  that three private inferences, concatenated, carry the content the candidate carries in
  one b-bit variable.
- **R1-piggyback.** The new head reads **one** W_i (W_pol, the first private state). This
  is the *literal* reuse arm, and it exposes the failure: the new consumer borrows S_pol's
  **private** state, so the reuse is not "shared content consumed by a fourth module" but
  "one module's private inference read by a second head" — the single-write test fails
  (a write to W_plan does not reach the new head, G1 §2.1-c), and the "shared" reading of
  reuse is absent.
- **R1-retrain.** The new head is served by a **fourth private encoder W_4 + π_4**,
  trained from scratch (the core is *not* frozen for this sub-arm). This is the honest
  cost arm: it measures the sample count of re-solving the inference a fourth time. The
  candidate matches R1-retrain's ceiling with **zero** retraining samples — that gap is
  the sample-efficiency half of the SHARED loss, made concrete.

The card's "private-state" comparison is read through these three sub-arms together:
R1 can *concatenate* (unfair capacity), *piggyback* (not shared), or *retrain* (not
frozen). None is "reuse the one shared content with a frozen core" — which is exactly
the candidate's capability under test.

**The card's four named rivals, mapped.** private-state → R1 (three sub-arms);
monolithic → R2 (probe + retrain); raw-history → R3; sufficient-statistic-broadcast → R4.
R5 is the fifth arm carried from G4 and loses on the single-write identity, exactly as it
does in G5/G6.

---

## 6. The comparability contract (G4 §8, inherited and extended)

All five G4 §8 rules bind, plus three clauses specific to a frozen-reuse test:

1. **Same task, same token stream, same seeds — for the novel task too.** S_conf and
   S_bias are scored on the **identical** episodes as the original three (same z, same
   λ's, same H/K), so the reuse is over the same information, never a re-drawn world.
2. **No z to any new consumer, in any arm.** z remains a training-only scaffold for the
   encoder (G2 §1.1); S_conf's and S_bias's training signal is the novel-task objective
   (log loss / asymmetric cost) with z entering **only** as the comparison target, never
   as a forward input (G8 L4).
3. **The new head's capacity is capped and identical across arms.** The head is a
   capacity-capped readout (logistic / threshold, or a single hidden layer ≤ 64 at G10's
   option, recorded) — the same instrument G8 §2.1 fixes for its decoder, so "reuse" is
   measured on one scale. A rival is never allowed a richer head than the candidate
   (G4 §8 rule 3's spirit, applied to the head).
4. **Information asymmetries favor the rival and are disclosed.** R1-concat reads 3 W_i,
   R2's probe reads d_h ≥ b bits, R3 reads the full window, R4 reads the exact S_H. Every
   asymmetry gives the rival more content or more capacity than the candidate's single
   b-bit W; the candidate's burden is the organizational claim alone (G4 §8 rule 4).
5. **Freezing is symmetric.** Every arm freezes whatever it *has* to freeze: candidate/R1
   freeze their encoders; R2 freezes its RNN (probe sub-arm); R3/R4/R5 have no learned
   inference to freeze (their "core" is the fixed update / the window / the register, all
   frozen by construction). No arm is asked to freeze something it does not possess, and
   no arm is granted a warmer start than another.
6. **Maintenance continues where it exists.** Candidate and R1 keep π + A running through
   the novel task; R2/R3/R4/R5 have no π, and that is their defining property, not a
   hidden saving the candidate is denied (G4 §8 rule 5).
7. **The new consumer is experimenter-supplied, in every arm.** S_conf/S_bias are added
   by the experimenter, not acquired by the organism; the claim is about *reusability of
   the content*, not about the organism *discovering* a new consumer. This is the card's
   "transfer alone ≠ global accessibility" boundary, stated as a contract term (§9).

---

## 7. Pre-declared gates (consistency checks G10 must assert)

Each gate is pre-declared here and none may be amended after seeing results (AC16/17
discipline). Gate shape matches claim shape: categorical completeness claims gate on
per-individual dominance / a threshold met by every seed, never a mean margin (AC16);
equivalence claims gate on exact/byte equality, never "similar" (P7).

1. **Frozen-core completeness (the content claim).** On the finals family, the
   candidate's S_conf reaches the Bayes-calibrated ceiling to the quantization floor, and
   S_bias reaches the asymmetric-cost optimum, on **every** seed, reading W alone. A seed
   that falls short is an incompleteness finding, reported — not re-classified (AC16: do
   not move a threshold after seeing the result).
2. **Zero-retraining reuse (the structural reuse).** The candidate's new consumers are
   served with the encoder frozen and **exactly 0** inference-retraining samples, on every
   seed — verified by the Phase-1/Phase-2 byte-identity of W's trajectory and the encoder
   parameters (a changed core is a protocol violation, not a result).
3. **Ceiling equivalence with R4 (the rival that must not be beaten).** The candidate's
   S_conf/S_bias scores equal R4's on every seed **to the quantization floor** — an
   equivalence gate, never `>` (AC16/17: R4's S_t is the exact sufficient statistic, the
   ceiling). A candidate that *exceeds* R4 is a wiring bug (it secretly read more than
   b-bit W); a candidate that *falls short* fails completeness. R3 may exceed (full
   history) and is reported as the information-ceiling rival, not gated as a candidate
   failure.
4. **Information required (AVAILABLE extends to the new consumers).** The candidate's
   S_conf/S_bias read b bits and **nothing else**: sever-history leaves them
   byte-unchanged, and no x_t reaches them (G3 §6 gate 5, G8 L7). R3's reader reads M
   tokens — asserted at the source level, per arm.
5. **Single-write reaches four consumers (SHARED extends).** One write to the candidate's
   W changes S_pol, S_plan, S_reg **and** S_conf (and S_bias) — four/five consumers from
   one write. In R1-piggyback and R5, reaching the same consumers requires a write per
   copy. Categorical, on every seed (G5 §10 gate 1, extended by one consumer).
6. **Modular extension (interference).** After Phase 2, the candidate's three original
   specialists' outputs are **byte-identical** to the Phase-1 run, on every seed (P7,
   AC83). R2's joint-retrain sub-arm reports the measured interference on its old heads
   as its reduction, not gated as a candidate claim.
7. **R1's honest reuse cost.** R1-retrain's sample count to match the ceiling is measured
   and reported; the candidate matches it with 0 retraining samples. The contrast is
   categorical (0 vs the measured full-retrain count), and R1-concat/R1-piggyback are
   reported with their wiring disclosed, never silently merged into one "R1 reuse" number
   (AC14's arm-name lesson: the sub-arm's wiring must match its label).
8. **Non-collapse with a fourth class.** On the G3 §3.2 differential-scramble matrix
   (now four/five consumers), S_conf responds as a strict monotone readout and S_bias as a
   shifted-threshold decision — neither co-varies identically with any existing specialist
   (G3 §6 gate 1, extended). A S_conf that co-varies with S_pol (e.g. magnitude-invariant)
   is a wiring bug, not a new consumer.

The rival-family sweep (P6 rule 2) binds: the novel consumers' head capacity, the S_conf
scoring rule (log loss / Brier), and S_bias's cost ratio are swept as level families
alongside the arms' own hyperparameters, never fixed while selecting another's best
member (AC11's fatal error).

---

## 8. Parameters (concrete defaults, swept as level families)

| Parameter | Symbol | Default | Swept / note |
| --- | --- | --- | --- |
| New consumers | — | S_conf (primary), S_bias (companion) | both attached in every arm; S_conf is the fourth invariance class, S_bias the same-class new boundary |
| S_conf function | P̂ | σ(W) | fixed form (G2 §2.1 Eq. 3); scoring rule swept {log loss, Brier}, recorded |
| S_conf scoring | — | log loss | the Bayes ceiling is the posterior entropy; reported with the three G2 anchors |
| S_bias cost ratio | c_AB : c_BA | 3 : 1 | swept as a level family; θ_bias = log(c_BA/c_AB) |
| S_bias threshold | θ_bias | log(c_BA/c_AB) | derived, never tuned (G2 §2 "derive before training") |
| New-head capacity | \|S_new\| | logistic / threshold (or 1 hidden ≤ 64) | identical across arms (§6.3); the G8 §2.1 instrument scale |
| Freeze boundary | — | encoder + W-acquisition + 3 specialists frozen | π + A continue (candidate/R1); §3 |
| W quantization | b | 5 bits | swept; rival at same b (G2 §4.2) |
| Horizon / probe | H, K | 32, 8 | G2 §6 |
| Seeds | — | disjoint eng/finals families | AC39: per-family, never mixed; new-head trained on disjoint family from evaluation (G8 §2.4) |

The analytic optima (§2) are computed from the same S_H and cost model before training,
exactly as G2 derived the decision threshold and G3 the per-specialist optima. No new
consumer enriches W beyond the b-bit sufficient statistic (D2/P5): the novelty is in the
*function of W*, not in giving the new consumer a richer representation.

---

## 9. Claim ceiling, the transfer-alone caution, and G9's question (6)

- **What a pass earns, at most.** That, in the candidate, the frozen maintained W is a
  **complete** sufficient statistic reusable by a **new** objective-distinct consumer —
  the new head reaches the Bayes ceiling for a never-trained function of z from W alone,
  with zero inference retraining, at b bits, while the original three consumers stay
  byte-unchanged — and that each rival loses on the property it removes (R1 on sharing,
  R2 on modularity, R3 on compression, R5 on the sharing mechanism), with R4 tied on
  performance and separated only on learned/paid-maintained status. This is the *reuse*
  half of N2 (the AVAILABLE + SHARED + MAINTAINED face, extended by one consumer), nothing
  stronger.
- **Transfer alone is NOT global accessibility (the card's bar, stated as a result
  boundary).** A frozen-features probe that learns a new function is ordinary
  representation transfer — G8's decoder does it, and any of the six arms' content
  variable admits one. The novel-consumer test is *architecture-controlled* transfer: the
  same instrument over six arms whose organizational property is the only thing varying
  (§6), plus the four measures (§4) that pin the *organizational* facts a bare probe does
  not — zero-retraining, b-bits-not-M-tokens, single-write-reaches-four, and
  byte-identical old consumers. A pass therefore earns "reusable content for one added
  consumer," **not** "global broadcast," "workspace seat" (O3/GWT), open-ended
  accessibility, or any claim that the organism *acquires* consumers on its own. The
  consumer is experimenter-supplied (§6.7), which is precisely what keeps the claim at
  level (b)/(c).
- **Answer to G9's reduction question (6) — "is the novel-consumer test merely ordinary
  representation transfer?", stated here for G9 to read.** The *instrument* is ordinary
  transfer (a capped readout on frozen features); the *claim* is not, because (a) the
  reused variable is **paid-maintained** — the new head reads a live W whose persistence
  is still being paid by π, so the reuse inherits the N1 substrate rather than a static
  snapshot (a bare probe of any arm's content does not require its content to be
  *maintained*); (b) the **six-arm control** makes the organizational property the
  independent variable, so "reuse" is a difference across architectures, not an absolute
  capability of one; and (c) the **interference** measure (old consumers byte-unchanged
  under consumer-addition) is a modularity fact no transfer probe states. Whether the
  *contrast* resolves in the candidate's favor is G10's to measure — G9's job is to audit
  whether the contrast is real or whether a monolithic RNN with a probe head collapses it,
  which this document arms it to answer (R2's probe sub-arm is the exact collapse
  candidate, and gate 6 is where it would surface).
- **Not claimed:** any novel *environment* transfer (the token stream is unchanged, §1.1);
  that the organism discovers or acquires the new consumer (it is supplied); any
  coordination result (G6's), leakage result (G8's), or maintained-decay result (G2's);
  that R4/R3 must lose on performance (R4 ties, R3 may exceed — and neither is a candidate
  failure); any consciousness, autopoiesis, or level-(d)/(e) claim. This is a
  level-(b)/(c) design.

---

## 10. Provenance

Instantiates the novel-consumer question over the six arms of
`PHASE3_ARCHITECTURES_v1.md` (G4 — candidate SLW + R1–R5, §8 comparability contract,
§9 "the primary place R1, R4, R5 and R3 are expected to lose," §10 "G7 = frozen-W reuse
and sample-efficiency/interference measures"), the three specialists of
`PHASE3_SPECIALISTS_v1.md` (G3 — the three invariance classes §4, the differential-scramble
§5, the sever-history gate §6.5), and the task of `PHASE3_INFERENCE_TASK_v1.md` (G2 — the
scalar-LRR sufficient statistic §2.1, the b-bit quantization §4.2, the probe §1.3, the
anchors §2.3). The five-predicate vocabulary is `SHARED_CONTENT_DEFINITION_v1.md` (G1 §2 —
AVAILABLE §2.4 as the completeness reading, the single-write test §2.1-c, the conjunction
§3). The freeze/byte-identity discipline is `PHASE3_CAUSAL_PLAN_v1.md` (G5 §3 surgical
discipline, §7 byte-identity) and G8's decode instrument (`PHASE3_LEAKAGE_AUDIT_v1.md`
§2.1 — the capped readout, and §2.4 the disjoint-seed decoder). The demotions (no V,
fixed/reactive A, S_reg a readout) are `PHASE3_BASELINE_v1.md` (G0 §3). The gate-shape and
rival-sweep discipline is `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (P6, P7, D1–D8). Organism
study references read from the skill's `references/` dir where named (`ac11`/`ac16`/`ac17`
— gate shape matched to claim shape, never move a threshold post-hoc; `ac14` — arm names
must match the wiring; `ac39`/`ac68` — seed/bimodality; `ac47` — graded vs saturated
endpoints, the learning curve is graded not a margin; `ac83`/`ac85` — byte-identity
license and the silently-wrong-wiring failure mode; `ac109`/`ac110` — the causal claim is
made where the content is the only carrier, and correctness rides content).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is a
novel-consumer test design, not a result.
