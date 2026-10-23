# Two-stream acquisition protocol — DRAFT v1 (W2, first neural-training study)

> **Authorization note (added 2026-10-20, 4:32 PM ET).** The ACI Research Specialist reports that Aidan Ahern directly approved this recurrent acquisition study in chat at 4:20 PM ET on 2026-10-20. That explicit approval supersedes the PR #4 certificate line stating it "does not authorize Stage B, training", for THIS STUDY ONLY. It does not extend to other studies, C4-or-higher work, or new architecture families. (Approval relayed by the ACI Research Specialist; not independently observed by the drafter.)


Status: **DRAFT ONLY. Nothing was run and nothing is frozen.** No training, no solvers, no enumeration.
The repo (/workspace/repo) was not modified. PR #4 files were read with `git show` from a scratch
clone outside the repo (/workspace/scratch/ts_read, FETCH_HEAD 5d9d8a7).
Every value marked PROPOSED is an open choice to settle before the freeze.

Sources:
- the frozen W2 world from PR #4 (branch `cursor/twostream-admission-certificate-c107`):
  `TWOSTREAM_PROTOCOL_v1.md`, `TWOSTREAM_FREEZE_v1.json` (freeze commit c69deb44…, freeze-file SHA-256 c654a121…)
  and `twostream_results_v1/{RESULTS.md, results.json, alias_audit.json}`;
- Astra consultation #5, RESPONSE B (`/workspace/astra_consult_5_raw.md`).

This protocol cites no external literature. The numeric reference values below are copied from the frozen
`results.json` and not recomputed.

---

## 0. Scope, approval and claim ceiling

**Approval chain.** The ACI Research Specialist reports that Aidan has approved drafting this study. The PR #4
certificate's own ceiling says it does not authorize Stage B or training. So running this protocol needs the
user to confirm directly before the freeze (flag F1).

**Architecture bound.**
- Only a standard small GRU or vanilla (Elman) RNN with a small MLP readout.
- No covariance slot, joint-state slot, protected controller or protected register.
- No exact filter equations inside the learner. No organism work.

**Claim ceiling (fixed in advance).** On ADMIT, the strongest permitted statement is:

> Within a supplied generic recurrent architecture, gradient training on ordinary readings and realized terminal
> outcomes acquired history-dependent state whose experimentally verified causal influence supports joint (XOR)
> prediction in the frozen W2 world; its mechanism is characterized relative to the declared rivals.

The protocol does **not** support any of these:
- an irreducible joint state (PR #4 is A0, so an exact stage-indexed two-marginal filter exists on the reachable set);
- necessity of a third coordinate (Q-NECESSITY is not addressed);
- C4 or any higher class;
- consciousness or awareness of any kind;
- organism re-entry, or unblocking A8.

**Question separation.**

| Question | Addressed here? | How |
| --- | --- | --- |
| Q-EXIST | descriptive only | probe decodability of the posterior chart from hidden state (accessibility, not use) |
| Q-LEARN | **primary** | before/after training; held-out forecast fit against the exact oracle (A-FIT) |
| Q-CAUSE | **primary** | native hidden-state transplants with filter-predicted changes, shams, restoration (§6) |
| Q-NECESSITY | **not addressed** | A0 world; no necessity claim is possible or attempted |

---

## 1. Frozen world (inherited unchanged from PR #4)

- **Hidden state and transition.** Hidden bits (X,Y) with a uniform initial law. Between readings:
  C~Bern(1/5), Dx~Bern(1/50), Dy~Bern(1/40); X'=X⊕C⊕Dx, Y'=Y⊕C⊕Dy.
- **Readings.** Eight readings in the order X,Y,X,Y,X,Y,X,Y. Each is a BSC with crossover 1/5. There is no
  transition after reading 8.
- **Queries.** X, Y and XOR at stage 8. The loss is the one-component Brier (q−Z)².
- **History integer h ∈ {0..255}.** Reading k is bit k−1, so reading 1 is the LSB. RESULTS.md prints
  reading 1 as the leftmost character; for example h=1 is `10000000`. This was checked against `per_history`.
- **Frozen reference values** (whole set, P(h)-weighted, 50-digit truncations from `results.json`):
  - Oracle Brier: X 0.212406, Y 0.155028, XOR 0.214954.
  - Current-only excess: X 0.037594, Y 0.004972, XOR 0.035046; total 0.077612.
  - Factorized (product) XOR excess = 4E[c²] = 0.0079539. E[c²] = 0.0019885. max|c| = 0.129753.
  - Intervention mass (|c|≥1/40) = 0.642566. Every history has c ≠ 0.
  - Alias audit: K1 = **A0** (T-PROJ and T-CLOSE hold). Terminal alias pairs, same-phase prefix alias pairs and
    cross-stage marginal coincidences are all 0. At stage k there are 2^k distinct marginal keys, so every
    reachable prefix has a distinct posterior.
  - Minimum marginal separation (descriptive): stage 5 0.0069, stage 6 0.0058, stage 7 0.00044,
    stage 8 0.00052.

The learner never receives the latent state, the model parameters, the chart, or oracle probabilities as input.
Training labels are the **realized** terminal bits (X₈, Y₈, X₈⊕Y₈) of each sampled episode, i.e. ordinary
prediction outcomes (flag F5).

---

## 2. Learner (candidate arm)

**Cell.**
- Primary: PyTorch `nn.GRU`, 1 layer, hidden size H.
- Secondary: `nn.RNN` (tanh), 1 layer.
- No other cell types.

**Input at step k (k=1..8).**
- The reading as ±1.
- A one-hot stage code e_k ∈ R⁸.
- Input size 9. The stage code is supplied identically to every recurrent arm and is charged in §5 (flag F6).

**Initial state.** h₀ = 0. No learned initial state.

**Readout.** The same for every recurrent arm: an MLP from h₈ with H→32 (tanh) →3 logits, then a sigmoid per
head, giving q_X, q_Y, q_XOR. The XOR head is a free output; it is not computed from q_X and q_Y.

**Loss.** L = (q_X−X₈)² + (q_Y−Y₈)² + (q_XOR−(X₈⊕Y₈))², with equal weights, averaged over the batch.
There are no auxiliary losses, no intermediate-stage targets, no covariance or chart targets and no
regularizer beyond §7.

**Hidden sizes (PROPOSED).**
- GRU: H ∈ {4, 8, 16}; the primary configuration is GRU-8.
- RNN: H = 8 (secondary, non-gating).

**Precision.** Training on CPU in float32. Evaluation in float64, with weights cast from the float32 checkpoint.

---

## 3. Fixed held-out split over the 256 histories

**Rule (deterministic, no seed).** Let p = h mod 16 (readings 1–4, the prefix) and s = ⌊h/16⌋ (readings 5–8,
the continuation).

> **h ∈ TEST ⇔ (p + s) mod 4 = 0.**  Otherwise h ∈ TRAIN.

**Counts.** |TEST| = 64 and |TRAIN| = 192. For each prefix p, the held-out continuations are the four values
s ∈ {s : s ≡ −p (mod 4)}.

**Properties (by construction, checkable at freeze):**
- Every 4-reading prefix and every 4-reading continuation occurs in TRAIN with 12 partners. TEST therefore tests
  prefix–continuation **recombination**.
- For a TEST history, the length-6 prefix fixes p and s mod 4, and with them the split. So **no stage-6, 7 or 8
  prefix of a TEST history is ever seen in training**. Some, but not all, stage-5 prefixes are seen.
  This is a strong generalization demand (flag F10).

**Explicit list.** The list is generated by the rule; the freeze file stores it as a 64-integer list with its
SHA-256:

```
TEST = sorted(h for h in range(256) if ((h & 15) + (h >> 4)) % 4 == 0)
```

**Weighting.** Evaluation uses P(h | split) ∝ P(h), with the frozen exact rationals renormalized within each
split. The split masses P(TEST) and P(TRAIN) are computed at freeze, from `results.json` only.

**Episode sampling.** Episodes are drawn from the frozen generator: latent trajectory first, then readings.
Any episode whose history is in TEST is discarded and redrawn. The redraw count is logged. The training
distribution is therefore P(h | TRAIN) with the correct conditional outcome law.

---

## 4. Comparators

| ID | Arm | Trained? | Role |
| --- | --- | --- | --- |
| K-EXACT | exact joint filter, i.e. the PR #4 oracle (frozen rationals) | no | ceiling; every excess is measured from it |
| K-2M | **stage-indexed two-marginal recurrent learner with nonlinear readout**: GRU with H=2 and the same input, readout MLP (2→32→3) and loss as the candidate | yes, identically | the A0 complete rival (Astra B); a **trained** learner, not an oracle supplying marginals |
| K-TAB | **history-table learner**: 256 entries × 3 logits indexed by the full terminal history, initialized at 0 (q=½), trained by the same optimizer, loss, batches and budget | yes, identically | the memorization explanation; held-out entries stay untrained |
| K-PROD | **product-of-marginals readout**: the GRU-8 candidate with the XOR head removed and q_XOR := q_X+q_Y−2q_Xq_Y, trained on the same three-term loss (gradient flows through the product) | yes, identically | shows that joint information is required beyond the marginals |
| K-PROD* | analytic factorized arm (PR #4 arm 2) | no | fixed reference: XOR excess 4E[c²] |
| K-CUR | analytic current-only arm (PR #4 arm 4) | no | fixed reference for the A-FIT scale |

**Notes.**
- **K-2M and the A0 world.** The rival is "exact stage-indexed two-marginal update plus nonlinear readout".
  A GRU-2 is a generic 2-dimensional recurrent learner of that kind. It may not be able to represent the exact
  stage-indexed marginal update. Separating late-stage histories through marginals needs resolution of about
  5×10⁻⁴ (§1). A deep-transition 2-state RNN (MLP update) would match the rival more closely, but may exceed
  "standard small RNN/GRU". It is listed as **OPTIONAL K-2M-DT, not included** pending a ruling (flag F4).
- **Beating K-2M is not required.** Matching K-EXACT is the ceiling. Reduction to K-2M describes what emerged;
  it does not negate acquisition.
- **No mean-field arm.** PR #4 deferred an "autonomous mean-field filter" as an apparatus change. K-2M is a
  learned two-state filter, not a per-step product projection (flag F4).

---

## 5. Accounting rule (precision, state dimension, stage information, update/readout)

Every arm, including K-EXACT, is charged by the same four-part ledger.

1. **State bits S = d × b_min.**
   - d is the persistent state dimension: H for the GRU/RNN arms; 3 for K-EXACT (m_x, m_y, c);
     for K-TAB, 0 persistent state but a table of 510 prefix keys.
   - b_min is the smallest b in {2,3,4,5,6,8,10,12,16,20,24} such that the arm still passes A-FIT (§8) on TEST
     when its state is **uniformly quantized to b bits per coordinate after every update**.
   - The quantization range per coordinate and stage is the [min, max] over TRAIN prefixes at that stage, so
     there is no test leakage.
   - For K-EXACT the chart is quantized the same way, in float64.
   - If no b ≤ 24 passes, b_min = ">24" and the arm fails A-FIT at finite precision. The float32 result is
     reported separately.
   - This charges precision explicitly. Two real numbers at unbounded precision can encode the whole history
     (Astra B accounting caveat), so state dimension alone is never reported as the resource.
2. **Stage information.** All recurrent arms receive the same 3 bits per step (log₂ 8) through the one-hot stage
   code. This charge is identical across arms, so it is noted rather than differenced. K-TAB is keyed by the full
   history, which subsumes stage. K-EXACT uses the stage implicitly through the alternating schedule (also 3 bits).
3. **Update resources.** The number of trainable recurrent parameters, plus the float precision (32). For
   K-EXACT: 0 trainable parameters, plus the exact rational update constants a, b_x, b_y, η.
4. **Readout resources.** The number of readout parameters, the same MLP shape for every recurrent arm. For K-TAB,
   all 256×3 logits count as readout/storage. For K-EXACT, 0 (the closed form).

The comparison table reports S, the stage bits, the update parameters, the readout parameters and the TEST
excess together. No single scalar ranking is preregistered.

---

## 6. Causal tests (Q-CAUSE)

### 6.1 Notation and trial set

- z_k(g) is the native hidden state after the prefix g of length k. F(z, u) is the stage-8 forecast vector
  (q_X, q_Y, q_XOR) obtained by running the trained network from state z at stage k on the continuation u
  (8−k readings).
- q*(h) is the exact oracle forecast.

**Primary trial set T₄ (stage k=4).**
- All ordered pairs (a, b) of distinct 4-prefixes, crossed with all 16 continuations u:
  240 × 16 = 3840 trials, weighted uniformly over trials.
- **Held-out confirmation set T₄ᴴ:** the trials with b·u ∈ TEST.
- **Joint-relevant subset T₄ᴶ:** the trials with |q*_XOR(b·u) − q*_XOR(a·u)| ≥ 1/20.

**Secondary trial set T₆ (k=6).** 64×63 pairs × 4 continuations. Descriptive and non-gating.

### 6.2 Native whole-state transplant (CAUSE-1)

**Intervention.** Run a to stage k, then replace z_k(a) with z_k(b) and run u. The predicted change from the
exact filter is Δ*(a→b, u) = q*(b·u) − q*(a·u).

**Statistics** (summed over the three queries; XOR-only versions are reported too):

- donor-tracking ratio ρ = Σ‖F_T − q*(b·u)‖² / Σ‖F_T − q*(a·u)‖²;
- predicted-change error ε = mean ‖(F_T − F(z_k(a),u)) − Δ*‖² / mean ‖Δ*‖².

**Important caveat (flag F2).** The GRU/RNN state is the network's whole memory. A whole-state transplant at
stage k followed by u is therefore **computationally identical to running b·u**. The test inherits its content
from A-FIT on the trials. Its added value comes from:
- the shams, which show that content and not perturbation magnitude drives the change;
- the before-learning comparison;
- T₄ᴴ, where b·u was never trained.

The protocol says so explicitly and does not count CAUSE-1 as independent of A-FIT.

### 6.3 Shams

**S-NORM: matched-norm random-direction donor.**
- Replace z_k(a) with z_k(a) + ‖z_k(b)−z_k(a)‖·v, where v is a seeded random unit vector (seed = 7000 + run seed).
- Prediction: no donor tracking, so ρ_NORM ≥ 1/2.

**S-WRONG: matched-norm reachable wrong donor.**
- For each trial, take the donor c ≠ a, b at the same stage whose ‖z_k(c)−z_k(a)‖ is closest to
  ‖z_k(b)−z_k(a)‖.
- Prediction: forecasts track c (ρ_c ≤ 1/4) and do not track b (ρ_b ≥ 1/2).
- This shows that the change follows donated **content**.

**S-NEAR: nearest-posterior donor.**
- No exact same-posterior donor exists on the reachable set: all 2^k prefixes at stage k have distinct
  marginals, and hence distinct posteriors (flag F3).
- Use the donor n minimizing the total-variation distance between exact stage-k posteriors.
- Prediction: the learner's change matches the small exact change. Criterion: ε_NEAR ≤ 1/4 against
  Δ*(a→n, u), plus a descriptive report of mean‖F_T − F(z_k(a),u)‖.

**S-SELF: self-donor (a = b).** The change must be exactly 0 (≤ 10⁻¹²). This is an integrity check.

### 6.4 Restoration / rescue

**Procedure.** After a transplant at stage k, re-insert the recipient's own state z_{k'}(a·u_{1..k'−k}) at a later
stage k' ∈ {k+1, …, 7}, then continue.

**Prediction.** F returns to the unperturbed forecast within 10⁻⁶.

**Status.** In a deterministic closed RNN this is an integrity check, not evidence (flag F2). It is reported
and gates integrity only.

### 6.5 Subspace localization (CAUSE-2, mechanism; gates only the "localized" sub-claim)

**Subspace.** P_S projects onto the top r=3 principal components of {z₄(g)} over the TRAIN-reachable
4-prefixes (PROPOSED r=3; flag F9). The PCA uses network states only; no oracle quantity enters.

**Interventions.**
- Partial transplant: z' = z₄(a) + P_S(z₄(b) − z₄(a)).
- Complement: z' = z₄(a) + (I−P_S)(z₄(b) − z₄(a)).
- Random-subspace sham: a seeded random r-dimensional subspace, with the perturbation rescaled to the norm of
  the partial transplant.

**Localized sub-claim (made only if all three hold):**
- ρ_partial ≤ 1/4;
- ρ_complement ≥ 1/2;
- ρ_random ≥ 1/2.

**Otherwise** the state is reported as "distributed / not localized at r=3". That is not a REJECT.

There is no covariance-only intervention: none exists on the reachable set with both marginals fixed, and the
zero-covariance clamp is off-manifold (PR #4; Astra B). Not required.

### 6.6 Before vs after learning

- Every CAUSE statistic is computed on each seed's **initialization** (step 0) and its final checkpoint.
  A descriptive checkpoint at 10% of the budget is added.
- CAUSE-1 counts as learning-dependent only if ρ_init > 1/2 on T₄ᴶ.
- If the untrained network already tracks the donor, CAUSE-1 is UNRESOLVED for that seed.

---

## 7. Seeds, budget, stopping (all frozen before any training)

All values are PROPOSED.

**Seeds.**
- Run seeds 0–9: 10 per configuration.
- Torch init seed = run seed. Episode-sampler seed = 1000 + run seed. Sham seed = 7000 + run seed.
- No seed is added, dropped or replaced after the freeze.

**Configurations.**
- GRU-4, GRU-8 (primary), GRU-16, RNN-8, K-2M, K-PROD, K-TAB.
- 7 × 10 = 70 runs, CPU only, `torch.set_num_threads(1)`, deterministic algorithms on.

**Optimizer.** Adam, lr 1e-3 with cosine decay to 1e-4, batch 256, gradient-norm clip 1.0, no weight decay.

**Budget.** Exactly 4000 steps, i.e. 1,024,000 sampled TRAIN episodes per run. That is about 5,300 draws per
TRAIN history on average.

**Stopping.**
- Fixed budget only. No early stopping, no validation-based checkpoint selection. The **final** checkpoint is
  evaluated.
- A NaN/Inf loss stops the run. The run is counted as an integrity failure and is not retried.

**Evaluation.** Exact enumeration of all 256 histories (and all prefixes for §6). No sampling noise enters the
evaluation, so per-seed statistics are exact functions of the checkpoint and no confidence intervals are needed.

**Location.** Code would live in `/workspace/scratch/twostream_acq/` (outside the repo). It is not written yet.

---

## 8. Outcomes and thresholds (fixed in advance)

**Reference quantities on TEST** are computed at freeze from frozen `results.json`, before any training:
E_CUR(TEST) (total current-only excess), E_PROD,XOR(TEST) (4E[c²|TEST]) and E_TAB(TEST) (the untrained-entry
excess, i.e. the q=½ excess). The whole-set analogues are 0.0776 and 0.00795.

**Per-seed criteria** (E = TEST P(h)-weighted Brier excess over K-EXACT, in float64):

| Criterion | Definition |
| --- | --- |
| **A-FIT** | E_total(TEST) ≤ ¼·E_CUR(TEST) **and** E_XOR(TEST) ≤ ¼·E_PROD,XOR(TEST) |
| **A-LEARN** | A-FIT fails at initialization, i.e. step 0 does not pass |
| **A-CAUSE** | on T₄ᴴ ∩ T₄ᴶ: ρ ≤ ¼ and ε ≤ ¼ (all three queries and XOR-only); S-NORM ρ ≥ ½; S-WRONG ρ_c ≤ ¼ and ρ_b ≥ ½; S-NEAR ε ≤ ¼; ρ_init > ½ |
| **A-INTEG** | S-SELF and restoration exact; no NaN; budget completed; split and redraw log consistent; oracle values match frozen rationals |

**Study verdict** (primary configuration GRU-8 only; the other configurations are reported, not gating):

- **ADMIT:** at least 8/10 seeds satisfy A-FIT, A-LEARN, A-CAUSE and A-INTEG. The claim is the §0 ceiling, plus
  the localized sub-claim only if CAUSE-2 holds in at least 8/10 seeds.
- **REJECT-ACQ:** at most 2/10 seeds satisfy A-FIT, with A-INTEG holding in at least 8/10. Meaning: acquisition
  was not shown in this architecture, budget and split. This is not evidence of incapacity in general.
- **REJECT-CAUSE:** at least 8/10 satisfy A-FIT but at most 2/10 satisfy A-CAUSE, with valid shams and integrity.
  Meaning: the forecast fit is not carried by transplantable, content-specific state in the predicted way.
- **UNRESOLVED:** any other seed count; or A-INTEG failing in more than 2 seeds; or ρ_init ≤ ½ in more than 2
  seeds; or any frozen-reference mismatch.

**Mechanism / REDUCTION** is reported, not gated (Astra B: reduction identifies what emerged, it does not
negate acquisition):

- **R-2M:** K-2M passes A-FIT in at least 8/10 seeds with S_2M ≤ S_GRU-8. The behaviour is reproducible by a
  learned two-marginal recurrent filter (expected in an A0 world).
- **R-TAB:** the candidate's E_XOR(TEST) ≥ ½·E_TAB,XOR(TEST). The behaviour is consistent with history lookup
  (no recombinational generalization).
- **R-FILT:** neither of the above. Additionally, a linear probe from z₈ to (m_x, m_y, c), fitted on TRAIN, has
  TEST R² ≥ 0.9 for all three. This is descriptive Q-EXIST and is labelled accessibility, not use.
- **R-OTHER:** none of the above.

The K-PROD result is reported as the joint-information check. The expectation is E_XOR(TEST) ≥ E_PROD,XOR(TEST)
up to optimization error. If K-PROD passes A-FIT on XOR, that is an integrity alarm: either the split or the
oracle reference is wrong.

---

## 9. ORIGIN / ROLE / REDUCTION judgments (prospective)

| Item | ORIGIN | ROLE | REDUCTION |
| --- | --- | --- | --- |
| GRU/RNN cell, readout MLP, loss, stage code, h₀=0, split, sampler | SUPPLIED | apparatus | — |
| Hidden-state organization at stages 1–8 | **UNRESOLVED** now; **ACQUIRED** if ADMIT (A-LEARN + A-FIT) | carries history for terminal X/Y/XOR prediction (A-CAUSE) | judged by R-2M / R-TAB / R-FILT / R-OTHER |
| Joint (XOR-relevant) information in state | UNRESOLVED; ACQUIRED if A-FIT on XOR beats K-PROD | supports joint prediction (T₄ᴶ transplants) | an A0 world means a two-marginal reduction exists in principle; R-2M tests whether it is learnable at parity |
| Covariance as a separate coordinate | NOT CLAIMED | — | not testable on the reachable set (no marginal-fixed intervention) |

**Emergence bar (constitution ledger).** "Acquired via declared developmental process, organization not
explicitly supplied, causally verified." ADMIT meets the first two by A-LEARN and A-FIT and the third by A-CAUSE,
within the ceiling.

---

## 10. Scaffold accounting table

| Scaffold | Supplied? | Could it carry the result? | Control |
| --- | --- | --- | --- |
| Generic GRU/RNN cell | yes | capacity only, no content | the same cell in K-2M, K-PROD; untrained baseline |
| Stage one-hot input | yes | supplies the clock (3 bits/step) | identical across arms; charged in §5 |
| XOR head + XOR loss | yes | supplies the **demand** for joint information, not its form | K-PROD removes the head |
| Realized-bit labels | yes | ordinary outcomes; no posterior or chart targets | — |
| Held-out split | yes | defines generalization | deterministic rule; frozen list hash |
| Readout MLP | yes | could compute nonlinear functions of state | same shape for all recurrent arms; parameters charged |
| Float32 precision | yes | could encode the whole history | b_min quantization charge (§5) |
| Covariance slot, joint slot, chart targets, filter equations, protected register/controller | **no** | — | absent by construction |
| Exact oracle | used for **evaluation only** | — | never an input or target |

---

## 11. The 13 admission answers

1. **Q1 Ultimate question.** Can a generic recurrent learner, trained only on readings and realized outcomes,
   acquire history-dependent state that causally supports joint prediction?
2. **Q2 One hypothesis.** GRU-8 trained per §7 acquires such state: A-FIT on held-out recombinations, plus
   content-specific transplant effects predicted by the exact filter.
3. **Q3 Falsifier.** REJECT-ACQ or REJECT-CAUSE under the §8 thresholds.
4. **Q4 Strongest simpler rival at parity.** K-2M, trained identically and charged by the §5 ledger. K-TAB is
   the memorization rival.
5. **Q5 Frozen evidence.** The PR #4 world and oracle rationals (freeze commit c69deb44…). The split rule and
   list hash, seeds, budget and thresholds are to be frozen before training.
6. **Q6 After success.** Record ORIGIN=ACQUIRED for the hidden-state organization at the §0 ceiling, with the
   REDUCTION label. No C4 claim. The next step would need a separate approval.
7. **Q7 After failure/unresolved.** Record the failure mode (ACQ vs CAUSE vs integrity). The world stays
   admitted. Any change of budget or architecture is a new protocol, not a rerun.
8. **Q8 Minimum apparatus.** One small GRU, a CPU, the frozen generator, and the exact enumeration for
   evaluation.
9. **Q9 Organizational / substrate / engineering.** Organizational: acquired state organization.
   Engineering: the training setup. Substrate: no claim.
10. **Q10 Claim ceiling.** The §0 statement. Not irreducible joint state, not C4, not consciousness.
11. **Q11 Cognitive layer.** History-integrating belief-like state for prediction (filtering vs lookup,
    characterized only).
12. **Q12 Organizational layer / supplied substrate.** The supplied cell, stage code, readout and losses
    (§10). Acquired: the state organization.
13. **Q13 Belief change.** An ADMIT would move the ledger from "acquisition untested" toward "acquisition of
    joint-predictive state shown in W2", for C3-type claims only. C4 stays NOT_ESTABLISHED. A REJECT would
    record that generic small recurrent learners did not acquire it at this budget.

---

## 12. Open choices (to settle before the freeze)

O1 hidden sizes; O2 budget and learning rate; O3 the split rule (alternative: a SHA-256-ranked random 64);
O4 the ¼ / ½ thresholds and the 8/10 seed rule; O5 r=3 and the PCA basis for CAUSE-2; O6 whether to add
K-2M-DT; O7 the stage code vs clockless input; O8 the b-grid for the precision charge.
