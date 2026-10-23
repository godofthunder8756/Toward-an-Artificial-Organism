# Two-stream acquisition protocol — FINAL v1 (W2, first neural-training study)

> **Approval confirmation (2026-10-20, 4:41 PM ET).** Aidan Ahern directly confirmed approval of this two-stream neural-training study to the drafting agent in chat. The approval covers this study only.


**Status: FINAL, cleared by Astra consult #9 (FREEZE WITH NAMED EDITS, all applied). Frozen only by the freeze commit that hashes this file; nothing is run before it.** Lead edits before freeze, non-substantive: title/status updated; Q1 scope clause added; the §0.1 row V2 is historical changelog text, superseded per §0.2.

**Repo.** `/workspace/repo` was not modified. PR #4 files were read with `git show` from a scratch clone outside
the repo (`/workspace/scratch/ts_read`, FETCH_HEAD 5d9d8a7).

**Supersession.** This draft supersedes `twostream_acquisition_protocol_draft_v1.md`, which is left untouched,
including the authorization note the Specialist added to it.

**Sources:**
- the frozen W2 world from PR #4 (`TWOSTREAM_PROTOCOL_v1.md`, `TWOSTREAM_FREEZE_v1.json`, `twostream_results_v1/`);
- Astra consultation #5, RESPONSE B;
- **Astra consultation #7** (`/workspace/astra_consult_5_raw.md`, "CONSULT #7 RESPONSE");
- the Specialist's rulings of 4:34 PM ET.

No external literature is cited.

## 0. Authorization (replaces v1 §0 approval paragraph)

**Resolved.** Aidan Ahern directly approved this recurrent acquisition study in chat at 4:20 PM ET on
2026-10-20, as relayed by the ACI Research Specialist. That approval supersedes, **for this study only**, the
PR #4 certificate line stating it "does not authorize Stage B, training". It does not extend to:
- other studies;
- C4-or-higher work;
- new architecture families;
- organism work.

The remaining stop is scientific protocol repair (Astra #7). Freezing and running still wait for a freeze
verdict.

## 0.1 Changes from v1

| # | Source | Change |
| --- | --- | --- |
| V1 | Astra #7 main edit | **New arm K-FR (frozen recurrence, trained readout).** For each seed and each recurrent configuration, the network is frozen at initialization and only the identical MLP readout is trained, on the same episodes and budget (§4). |
| V2 | Astra #7 / ruling | Evidence is split into **E1 readout/predictive acquisition**, **E2 recurrent adaptation** and **E3 causal organization**, each with its own evidence and labels (§8). If K-FR matches the candidate, the record reads "**acquired readout over supplied recurrent dynamics**". |
| V3 | Ruling | Acquisition never depends on beating the product-constrained model (§8). |
| V4 | F2 ruling | The whole-state transplant is an **integrity / behavioral-identity check only**. Narrower mechanism claims use **prespecified partial interventions with controls** (§6). Restoration remains integrity-only. |
| V5 | F3 ruling | Nearest-posterior donors are a **graded sensitivity control only**. They use the continuation-specific oracle change and a prespecified tiny-denominator rule, and report absolute plus normalized error (§6.5). |
| V6 | F4 ruling | Learned two-dimensional arms are renamed **K-2D** (GRU-2) and **K-2D-MLP** (declared 2-d MLP-update variant, included and charged). Neither is "two-marginal" and neither is an autonomous mean-field filter (§4). |
| V7 | F5 ruling | States explicitly that the **environment supplies the feedback** (§1). |
| V8 | F6 ruling | The stage code is a declared **external timing scaffold**. Clockless is a separate experiment. K-TAB now charges history/index buffering (§5). |
| V9 | F7 ruling | Quarter-gap and 8/10 are **prospective engineering criteria**. Continuous per-seed results and init→final changes are reported (§8.4). |
| V10 | F8 ruling | Defaults accepted. Rank-3 PCA is **exploratory**: failure means "not localized by this intervention" (§6.4). |
| V11 | Astra #7 | K-PROD becomes the **product-constrained output model (K-PCO)**. All three errors are reported. Its false lower bound and the "integrity alarm" are removed (§4). |
| V12 | Astra #7 | Wrong-donor eligibility uses a prespecified minimum oracle-continuation separation. Random-direction effects are descriptive. REJECT-CAUSE is replaced by the weaker "not shown / not localized by this intervention" (§6, §8). |
| V13 | Astra #7 | R-2M / R-TAB / R-FILT are replaced by **literal observation labels** (§8.3). |
| V14 | Astra #7 | **Precision repair:** b is selected on TRAIN and confirmed on TEST, and the TEST curve is descriptive. The rules for rounding, clipping, ranges, metadata cost and invalid chart distributions are specified (§5). |

## 0.2 Edits applied (Astra Consult #9: FREEZE WITH NAMED EDITS)

This file is draft v2 verbatim plus only the edits below.

| Consult #9 item | Section(s) changed |
| --- | --- |
| G1: keep ¼ of the analytic product-readout excess | §13 G1 (ruling recorded; §8.1 unchanged) |
| G2: drop K-FR for the 2-d rivals (120 runs); keep K-FR for all 4 candidate configurations | §4 (K-FR row, Pairing), §7 (Configurations), §13 G2 |
| G3: thresholds accepted as engineering choices | §13 G3 |
| G4: cross-fitting | §6.3 (via Edit 3), §13 G4 |
| G5: TRAIN precision selection accepted | §13 G5 |
| Edit 1: split-specific current-only reference | §8 (reference quantities) |
| Edit 2: E2 label FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET; K-FR-only claim; recurrent contribution not established; ≤10⁻¹² tie; intact valid paired runs | §8.2, §9, §10, §12 Q3 |
| Edit 3: cross-fitted E3 (parity folds, centered ridge, projection onto col(W), rank rule, all-16 fit descriptive) | §6.3, §6.4 (K-FR paragraph) |
| Edit 4: common trial subset, intended-donor XOR change ≥ 1/100, coverage rule, both statistics, undefined denominators, absolute errors | §6.3 (Statistics), §6.4 (eligibility), §8.3 |
| Edit 5: narrowed E3 claim and qualifier, K-FR A-FIT reported, no origin implication, permitted wording | §6.4 (K-FR paragraph), §8.3, §9 |
| Edit 6: precision accounting (float32 endpoints, wording for failure, K-TAB logits float32 unquantized, K-EXACT indices as charged state) | §5.1, §5.2 |

---

## 1. Frozen world (unchanged from v1 §1)

**Generator, readings and queries.**
- Uniform initial (X,Y). C~Bern(1/5), Dx~Bern(1/50), Dy~Bern(1/40).
- Readings X,Y,X,Y,X,Y,X,Y, each through a BSC(1/5). Terminal queries X, Y and XOR; one-component Brier.
- History integer h: reading k is bit k−1. This was checked against `per_history`; RESULTS.md prints reading 1
  leftmost.

**Frozen reference values (whole set):**
- Oracle Brier: X 0.212406, Y 0.155028, XOR 0.214954.
- Current-only excess: total 0.077612.
- Analytic factorized XOR excess: 4E[c²] = 0.0079539.
- Alias audit: A0. At stage k there are 2^k distinct marginal keys.
- Minimum marginal separation: 4.4×10⁻⁴ at stage 7, 5.2×10⁻⁴ at stage 8.

**Feedback (F5).** The **environment supplies feedback** after each episode: the realized terminal bits X₈, Y₈
and X₈⊕Y₈. These are supervised outcomes, not oracle probabilities, chart values or latent trajectories.

- The prediction **demand** is supplied by the environment.
- Whether its **solution** is learned is what this study tests.
- No latent state, model parameter, chart value or oracle probability is ever a learner input or target.

## 2. Candidate learner (unchanged except where noted)

| Element | Specification |
| --- | --- |
| Cell | `nn.GRU` with H ∈ {4, **8** (primary), 16}; `nn.RNN` (tanh), H = 8 (secondary) |
| Input at step k | reading as ±1; one-hot stage code e_k (a declared **external timing scaffold**, §5) |
| Initial state | h₀ = 0 |
| Readout | MLP H→32 (tanh)→3, sigmoid per head; the XOR head is free |
| Loss | (q_X−X₈)² + (q_Y−Y₈)² + (q_XOR−X₈⊕Y₈)², terminal only; no auxiliary or chart targets |
| Hardware | CPU only |
| Numerics | float32 training; float64 evaluation |

**Parameter counts (PyTorch conventions; input size 9).**

| Configuration | Recurrent parameters | Readout parameters |
| --- | --- | --- |
| GRU-4 | 180 | 259 |
| GRU-8 | 456 | 387 |
| GRU-16 | 1296 | 643 |
| RNN-8 | 152 | 387 |

## 3. Split (unchanged)

**Rule.** h ∈ TEST ⇔ ((h mod 16) + ⌊h/16⌋) mod 4 = 0.
- 64 TEST histories and 192 TRAIN histories.
- No stage-6, 7 or 8 prefix of a TEST history is ever trained.
- Rejection-sampled training episodes; evaluation is P(h)-weighted within each split.

The split was accepted by Astra #7.

---

## 4. Arms

| ID | Arm | Training | Role |
| --- | --- | --- | --- |
| CAND | GRU-H / RNN-8 (§2), all parameters trained | full | candidate |
| **K-FR** | **The same network, frozen at the seed's initialization.** Recurrent weights stay at their initialized values. **Only the identical MLP readout is trained**, with the same readout initialization, episode stream (same sampler seed), optimizer, schedule, batch and budget as CAND. It is run for all four candidate configurations (GRU-4/8/16, RNN-8). It is **not** run for K-2D or K-2D-MLP,
whose role is performance reproduction, not origin attribution (Consult #9, G2). | readout only | origin control: can readout training over supplied random recurrent dynamics produce the behavior? |
| **K-2D** | GRU with H = 2, same input, readout MLP 2→32→3 (195 params), recurrent 78 params | full | declared two-dimensional rival. It learns an arbitrary 2-d state, **not necessarily marginals**. |
| **K-2D-MLP** | Declared recurrent architecture **variant** (not a new family, per the F4 ruling). State z ∈ R², z_k = tanh(W_b·tanh(W_a[z_{k−1}; o_k; e_k] + b_a) + b_b), with W_a 16×11 and W_b 2×16. Recurrent params 226 (charged); readout 2→32→3 (195). | full | 2-d rival with a more flexible update |
| K-TAB | Table of 256 × 3 logits, indexed by the full history, init 0, same optimizer, loss and budget. **Charges** an 8-bit history/index buffer (§5). | full | history-table explanation |
| **K-PCO** | **Product-constrained output model.** GRU-8 with the XOR head removed and q_XOR := q_X + q_Y − 2q_Xq_Y, trained on the same three-term loss | full | descriptive comparison only (see below) |
| K-EXACT, K-PROD*, K-CUR | Frozen analytic arms from PR #4 | — | references |

**K-2D and K-2D-MLP.**
- Neither is guaranteed to realize the exact stage-indexed marginal update.
- Neither is an **autonomous mean-field filter**: that would require an explicit independence projection during
  filtering, which neither has.
- The name "two-marginal" is reserved for a semantically verified implementation, and none is included.

**K-PCO.**
- Its jointly trained X/Y heads may trade marginal accuracy for XOR accuracy. Its XOR excess **can fall below**
  the analytic product excess 4E[c²|TEST].
- So **no lower bound is predicted**, and K-PCO passing A-FIT is **not** an integrity alarm.
- Reported: E_X, E_Y and E_XOR on TEST and TRAIN, at init and final.
- It does not show that information beyond the marginal pair is required, and nothing is gated on it.

**Pairing.** For seed s, CAND and K-FR share the torch init seed s, the sampler seed 1000+s and every
hyperparameter. The only difference is `requires_grad=False` on the recurrent parameters.

---

## 5. Accounting rule (repaired)

### 5.1 Ledger columns, the same for every arm

1. **Persistent state.**
   - Recurrent arms: d = H (2 for K-2D/K-2D-MLP).
   - K-EXACT: 3 (the chart).
   - **K-TAB: a history/index buffer of k bits at stage k, max 8 bits (2^k configurations).** It is not zero.
2. **State precision b_sel** (§5.2), and the charged state bits d × b_sel. K-TAB's buffer is exact: 8 bits, and
   its logits stay float32 (no logit quantization; parameter quantization is a different resource experiment).
3. **Stage information.** 3 bits/step, an **information-accounting convention** for the declared external timing
   scaffold (8 stages). It is not the physical cost of the float one-hot input. It is identical across the
   recurrent arms and K-EXACT. K-TAB's index subsumes it.
4. **Update parameters.** Trainable recurrent parameter count × 32 bits. K-FR is reported as "0 trained +
   N frozen-random". K-EXACT has 0 (exact constants).
5. **Readout / storage parameters.** Readout parameter count × 32. K-TAB: 768 logits × 32.
6. **Quantizer metadata** (§5.2): 2 float32 constants per coordinate per stage, i.e. 64·d·8 bits. Reported
   separately; not added to state bits.

### 5.2 Precision procedure (no TEST selection)

**Quantizer (frozen).** For arm A, coordinate i and stage k:
- **Range.** [lo_ik, hi_ik] = the min and max of the unquantized float64 state over all TRAIN-reachable
  prefixes at stage k. These are computed once from the final checkpoint, **cast to float32 before any quantizer
  is constructed or used** (matching the charged metadata), and then held constant.
- **Constant coordinate.** If hi_ik − lo_ik < 10⁻¹², the coordinate is constant at stage k. It is replaced by lo_ik
  and charged 0 bits at that stage.
- **Clipping.** Values outside the range are clipped to it. The clip count is logged per stage.
- **Rounding.** Round to the nearest of the 2^b levels lo + j(hi−lo)/(2^b − 1), j = 0..2^b−1, ties to even j.
- **Application.** Quantize **after every recurrent update** (stages 1..8). The quantized state is the next
  step's input and z₈ feeds the readout. The readout itself stays float64.

**Grid.** b ∈ {2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24}.

**Selection on TRAIN.**
- b_sel(A, seed) is the smallest b at which A's **TRAIN** errors meet the A-FIT inequalities (§8.1), with
  TRAIN reference quantities.
- If no b ≤ 24 passes on TRAIN, b_sel = **"no qualifying precision in the declared grid"**. This can reflect
  poor fit rather than insufficient precision.

**Confirmation on TEST.**
- Report whether A-FIT holds on TEST at b_sel (CONFIRMED / NOT CONFIRMED).
- The full TEST curve E(b) is reported **descriptively only**. No TEST-selected b is ever reported as a resource
  estimate.

**K-EXACT chart quantization.**
- Quantize (m_x, m_y, c) per coordinate as above, with ranges from TRAIN-reachable exact charts.
- **Repair of invalid distributions.** After quantization:
  - clip m_x and m_y to [0, 1];
  - clip c to the Fréchet interval [max(−m_x m_y, −(1−m_x)(1−m_y)), min(m_x(1−m_y), m_y(1−m_x))], so that all
    four masses lie in [0, 1] and sum to 1.
- Each repair is counted and reported per stage.
- The exact update is then applied in float64 to the repaired chart.
- The repair is part of the quantized K-EXACT arm. It is not an error.
- **Charged state.** The retained state between steps is the **three quantization indices only**. At each step
  the chart is reconstructed from the indices and projected (the repair above) deterministically, updated, and
  re-quantized to indices. No additional independent floating-point state is retained, so the charge of three
  b-bit coordinates is complete.

**K-TAB.** No logit quantization is applied. The history/index buffer is exact (8 bits) and the logits stay
float32.

**Invalid learner outputs.** The sigmoid outputs always lie in (0,1). Any NaN or Inf is an integrity failure.

---

## 6. Causal and mechanism tests

### 6.1 Trial sets (unchanged)

- **T₄:** ordered pairs of distinct 4-prefixes × 16 continuations (3840 trials).
- **T₄ᴴ:** b·u ∈ TEST.
- **T₆:** descriptive.
- The oracle continuation change is Δ*(a→b,u) = q*(b·u) − q*(a·u), computed per continuation.

### 6.2 Whole-state transplant: integrity / behavioral identity only (F2)

**Check.** Replace z₄(a) with z₄(b) and run u. In this deterministic architecture the forecast must equal the
native forecast on b·u to within 10⁻⁹ in float64. A failure is an **integrity failure**.

**Reporting.** The donor-tracking ratio is reported as a behavioral consistency description. It adds **no**
mechanism evidence beyond predictive fit on the corresponding histories.

**Restoration** (re-inserting the recipient's own later state) is integrity-only, at 10⁻⁹.

### 6.3 Primary partial intervention (prespecified; E3)

**Subspace (cross-fitted).**
- **Folds.** The 16 four-reading prefixes are partitioned into two fixed folds by the **parity of their bit
  count**: fold 0 = even bit count, fold 1 = odd bit count (8 prefixes each).
- **Fit.** For each fold f, the ridge map is fitted on the **other** fold's eight prefixes, from stage-4 states
  z₄(g) ∈ R^H to the exact chart (m_x, m_y, c)(g). The regression is **centered least squares plus
  10⁻³‖W‖_F²**, with an **unpenalized intercept**: W ∈ R^{H×3} minimizes ‖Z̃W − Ỹ‖_F² + 10⁻³‖W‖_F², where Z̃ and Ỹ
  are the centered states and charts, and the intercept is mean(Y) − mean(Z)·W.
- **Subspace.** S_chart^(f)(A, seed) = col(W) ⊂ R^H. Π^(f) is the orthogonal projector onto it.
- **Numerical rank.** The rank is the number of singular values of W exceeding 10⁻⁸ times the largest. **Rank below
  three makes the proposed three-dimensional claim UNRESOLVED.**
- **Held-out use.** For fold f, only recipients, intended donors and wrong donors **from fold f** are used, with
  Π^(f). Held-out intervention results are pooled across the two folds. The cross-fitted T₄ᴴ is the set of T₄ᴴ
  trials (a, b, u) with a and b in the same fold.
- **All-16 fit.** A fit on all 16 prefixes is retained as **descriptive only**.
- Each fit is frozen before any intervention is computed.
- dim S = 3, so this applies to H ≥ 4. For K-2D the whole state is used and the test is descriptive only.
- The chart is used **only as an analysis decoder**. It never enters training. The chart-guided intervention is
  an analyst-defined test, not discovery of a naturally separate covariance module.

**Interventions** (Π = Π^(f), the held-out fold's projector):
- Partial transplant: z′ = z₄(a) + Π(z₄(b) − z₄(a)).
- Complement transplant: z′ = z₄(a) + (I − Π)(z₄(b) − z₄(a)).
- Wrong-donor partial transplant: z′ = z₄(a) + Π(z₄(c) − z₄(a)), with c chosen by §6.4.

**Statistics.** These are computed on the eligible cross-fitted T₄ᴴ trials (§6.4), over all three queries
(the three-output vector) and XOR-only.
- **One trial subset.** The **same** eligible trial subset is used for the partial, complement and wrong-donor
  comparisons.
- The tracking ratio ρ(target) = Σ‖F′ − q*(target·u)‖² / Σ‖F′ − q*(a·u)‖² is a ratio of sums over trials.
  **A ratio denominator at or below 10⁻¹² is undefined and cannot pass.**
- Absolute error: mean ‖(F′ − F(a·u)) − Δ*‖². **Absolute errors are reported alongside every ratio.**
- Normalized error: §6.5.

### 6.4 Controls

**Trial eligibility (prespecified).** A cross-fitted T₄ᴴ trial (a, b, u) is eligible iff the **intended donor's
oracle XOR change |Δ*_XOR(a→b, u)| ≥ 1/100** and an eligible wrong donor exists under the conditions below.

**Coverage.** Eligible trials must cover **at least 10% of cross-fitted T₄ᴴ**, with **at least four distinct
recipients and four distinct intended donors in each fold**. Otherwise E3 is **UNRESOLVED**, not "not localized".

**Wrong-donor eligibility (prespecified).** For trial (a, b, u), a donor c ∉ {a, b} at stage 4, **in the same
held-out fold**, is eligible iff:
- **‖q*(c·u) − q*(b·u)‖_∞ ≥ σ_sep = 1/10** (oracle continuation forecasts differ); and
- ‖q*(c·u) − q*(a·u)‖_∞ ≥ σ_sep; and
- ‖Π(z₄(c) − z₄(a))‖ lies within ±20% of ‖Π(z₄(b) − z₄(a))‖ (norm-matched).

Among eligible donors, the one closest in norm is chosen; ties go to the lowest prefix integer. Trials with no
eligible c are dropped from **all three comparisons** (common subset), and the drop count is reported.

**Random-direction / random-subspace perturbations** (matched norm, seed 7000+s) are **descriptive only**. No null
prediction is made.

**Rank-3 PCA subspace** (top-3 PCs of TRAIN stage-4 states): **exploratory**. Failure reads "not localized by
this intervention".

**Same intervention on K-FR.** The cross-fitted partial-intervention statistics are computed on the K-FR network
of the same seed: frozen random recurrence, trained readout, its own cross-fitted S_chart. Whether K-FR meets
A-FIT is reported alongside, since poor prediction alone can prevent donor tracking. The comparison can show only
whether a pattern is **observed in CAND but not in the matched frozen-recurrence control under this budget**.

### 6.5 Nearest-posterior donors: graded sensitivity control (F3)

**Donor.** For recipient a, n = the stage-4 prefix (≠ a) minimizing the TV distance between exact stage-4
posteriors.

**Per continuation u:**
- the continuation-specific oracle change Δ*(a→n, u) = q*(n·u) − q*(a·u);
- the learner change ΔF = F(n·u) − F(a·u) under the whole-state transplant (equal to native, §6.2), plus the
  partial version.

**Reported:**
- absolute error |ΔF − Δ*| (per query and summed);
- **normalized** error |ΔF − Δ*| / ‖Δ*‖₂, **only for trials with ‖Δ*‖₂ ≥ τ_den = 1/100**. Trials below τ_den
  appear only in the absolute-error summary, and their count is reported.

This control is graded and **non-gating**. It is not a substitute for same-posterior donors, which do not exist
on the reachable set.

---

## 7. Seeds, budget, stopping (frozen before training; defaults accepted, F8)

- **Seeds** 0–9 per configuration. Torch seed s; sampler 1000+s; sham 7000+s. No replacements.
- **Configurations.**
  - CAND: GRU-4, GRU-8, GRU-16, RNN-8.
  - K-FR for each of these.
  - K-2D, K-2D-MLP, K-TAB, K-PCO.
  - Total 12 configurations × 10 = 120 runs. CPU, single-threaded, deterministic.
- **Training.** Adam, lr 1e-3 cosine-decayed to 1e-4, batch 256, clip 1.0, **4000 steps** (1,024,000 episodes).
  Fixed budget; final checkpoint only; NaN is an integrity failure with no retry. Convergence is not assured
  (Astra).
- **Evaluation.** Exhaustive over all histories and prefixes. This removes history-sampling error **but not
  seed-to-seed variation**, which is reported (§8.4).

---

## 8. Evidence components, criteria and outcomes

All thresholds below are **prospective engineering criteria** (F7), not theoretical significance thresholds.
Reference quantities on TEST and TRAIN are computed at freeze from the frozen `results.json`:
- E_CUR(split): the **split-specific** total current-only excess. Within each split, the optimal current-only
  forecast is computed by averaging q*(h), weighted by P(h), separately for each final reading (reading 8). Its
  excess over the full-history oracle is then computed within that split. PR #4's unconditional current-only
  forecasts are **not** merely reweighted, because conditioning on the TRAIN/TEST selection changes the
  distribution. This split-specific reference is used wherever E_CUR appears;
- E_PROD*,XOR: analytic 4E[c²], used only as a **fixed numeric scale**, not a comparison with K-PCO.

### 8.1 E1: predictive acquisition (Q-LEARN, behavior)

**A-FIT(seed).**
- E_total(TEST) ≤ ¼·E_CUR(TEST); and
- E_XOR(TEST) ≤ ¼·E_PROD*,XOR(TEST).

**A-LEARN(seed).** A-FIT fails at initialization.

**E1 label (primary GRU-8):**
- **SHOWN:** at least 8/10 seeds satisfy A-FIT, A-LEARN and integrity.
- **NOT SHOWN:** at most 2/10 satisfy A-FIT, with integrity in at least 8/10.
- **UNRESOLVED:** otherwise.

E1 does **not** depend on K-PCO, K-2D, K-2D-MLP or K-TAB.

### 8.2 E2: recurrent adaptation (ORIGIN of the recurrent contribution)

**Paired statistic per seed.** ratio_s = E_CAND,total(TEST) / E_K-FR,total(TEST). The XOR version is also
reported.
- A seed counts toward "recurrent adaptation supported" only if its CAND and K-FR runs are both **intact and
  valid** (integrity holds for both).
- A K-FR excess at or below 10⁻¹² is a **numerical tie**, not evidence for a ratio improvement. Such a seed
  cannot satisfy ratio_s ≤ ½.

**E2 label (GRU-8 pair):**

| Label | Condition |
| --- | --- |
| **RECURRENT ADAPTATION SUPPORTED** | ratio_s ≤ ½ in at least 8/10 seeds |
| **FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET** | K-FR satisfies A-FIT in at least 8/10 seeds **and** ratio_s ≤ ½ in at most 2/10. The label describes **K-FR**, not how CAND works. CAND's recurrent contribution is recorded as **not established by this comparison**. |
| **READOUT-ONLY INSUFFICIENT, RECURRENT CONTRIBUTION UNCLEAR** | K-FR fails A-FIT in at least 8/10, but the ratio criterion is not met in at least 8/10 |
| **UNRESOLVED** | otherwise |

**Descriptive companions:**
- the recurrent weight change ‖θ_final − θ_init‖ / ‖θ_init‖;
- the change of the stage-wise state geometry between init and final, i.e. the pairwise state distance matrices
  of the 16 stage-4 prefixes, compared by correlation.

Localization is **not** inferred from E2.

### 8.3 E3: causal organization (partial interventions, Q-CAUSE characterization)

**Per seed (GRU-8 CAND), on eligible cross-fitted T₄ᴴ trials,** LOCALIZED(seed) holds iff all three hold:
- partial transplant ρ(b) ≤ ½;
- wrong-donor partial transplant ρ(c) ≤ ½;
- complement transplant ρ(b) ≥ ¾.

Each inequality must hold for **both** the three-output vector and the XOR-only statistic. An undefined ratio
(denominator ≤ 10⁻¹²) cannot pass. If the coverage rule (§6.4) fails or the numerical rank is below three (§6.3),
E3 is UNRESOLVED.

**E3 label:**
- **LOCALIZED BY THE CHART-DECODER INTERVENTION:** at least 8/10 seeds.
- **NOT LOCALIZED BY THIS INTERVENTION:** at most 2/10.
- **UNRESOLVED:** otherwise.

**Qualifier.** "**Observed in CAND but not in the matched frozen-recurrence control under this budget**" is
added only if K-FR is NOT LOCALIZED in at least 8/10 seeds. Whether K-FR meets A-FIT is reported alongside that
comparison, since poor prediction alone can prevent donor tracking.

**Not-localized results** are never read as "state not causal" or "distributed" (v1's REJECT-CAUSE is
withdrawn).

**Integrity gates** (whole-state identity and restoration, §6.2) apply to every run.

### 8.4 Continuous reporting (all arms, every seed)

- E_X, E_Y, E_XOR and E_total on TRAIN and TEST, at **init and final**, with the init→final change.
- The paired CAND − K-FR differences.
- The precision curves, b_sel, and CONFIRMED / NOT CONFIRMED.
- All §6 statistics.
- Median and range across seeds. No significance claims.

### 8.5 Literal observation labels (replacing R-2M / R-TAB / R-FILT)

| Label | Condition (GRU-8 seeds unless stated) |
| --- | --- |
| **"Two-dimensional rival reproduces performance"** | K-2D or K-2D-MLP satisfies A-FIT in at least 8/10 of its seeds (reported per variant, with its ledger) |
| **"Frozen-recurrence readout reproduces performance"** | K-FR satisfies A-FIT in at least 8/10 seeds |
| **"Held-out generalization weak"** | CAND E_XOR(TEST) ≥ ½·K-TAB E_XOR(TEST), **or** E_total(TEST) ≥ 4·E_total(TRAIN), in at least 8/10 seeds |
| **"Chart linearly accessible"** | the stage-8 ridge probe (fitted on TRAIN) has TEST R² ≥ 0.9 for each of m_x, m_y and c, in at least 8/10 seeds. Accessibility only (Q-EXIST); not filtering. |

Behavioral reproduction by a rival is **not** identification of the candidate's mechanism. Weak generalization
does **not** identify lookup.

### 8.6 Study verdict

- **ADMIT:** E1 SHOWN, with integrity holding in at least 8/10 seeds. The recorded claim is assembled from the
  E2 and E3 labels and the §9 ceiling text.
- **REJECT:** E1 NOT SHOWN. Acquisition of the prediction function was not shown in this architecture, budget
  and split.
- **UNRESOLVED:** any other outcome, or an integrity failure in more than 2 seeds.

E2 and E3 never turn an ADMIT into a REJECT. They determine **which** acquisition claim is recorded.

---

## 9. Claim ceiling (assembled; fixed in advance)

**Base claim (ADMIT).**

> Within a supplied generic recurrent architecture with an external timing scaffold, gradient training on
> environment-supplied terminal outcomes acquired a history-dependent prediction function for X, Y and XOR in
> the frozen W2 world.

**Appended according to the labels:**

| Label | Appended text |
| --- | --- |
| E2 = FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET | "A frozen-recurrence control (K-FR: the same initialized network with only the readout trained, same episodes and budget) also met A-FIT at this budget. CAND's recurrent contribution is not established by this comparison." |
| E2 = RECURRENT ADAPTATION SUPPORTED | "…with a reliable contribution from recurrent adaptation relative to a frozen-recurrence readout." |
| E3 = LOCALIZED | "…and a chart-decodable 3-d subspace of native state carries donor-specific forecast content under the prespecified partial intervention" (+ "observed in CAND but not in the matched frozen-recurrence control under this budget" if qualified) |
| Literal observation labels | appended verbatim |

**Never:**
- "hidden-state organization acquired", or any claim that E2 plus E3 establishes the origin of the localized
  subspace or that it is an independently manipulable natural module. When E2 = SUPPORTED and E3 = LOCALIZED, the
  permitted wording is: "**Training recurrent parameters improved prediction relative to K-FR, and a cross-fitted
  chart-decoder subspace redirected forecasts under the specified partial interventions.**" These are two
  supported findings, not proof that training created that subspace;
- irreducible joint state;
- marginal-filter or mean-field identification;
- C4;
- consciousness;
- organism claims.

---

## 10. ORIGIN / ROLE / REDUCTION

| Item | ORIGIN | ROLE | REDUCTION (literal) |
| --- | --- | --- | --- |
| Cell, readout architecture, stage code (external timing scaffold), loss, environment feedback, split | SUPPLIED | apparatus | — |
| History-dependent prediction function | UNRESOLVED → **ACQUIRED** if E1 SHOWN | terminal X/Y/XOR prediction | observation labels §8.5 |
| Readout mapping | ACQUIRED if E1 SHOWN (trained in every learned arm) | maps state to forecasts | — |
| Recurrent dynamics organization | If E2 = FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET: CAND's trained recurrent dynamics are **not** labelled SUPPLIED; the recurrent contribution is **not established by this comparison**. **ACQUIRED (in part)** if E2 = SUPPORTED; else UNRESOLVED | carries history | "frozen-recurrence readout reproduces performance" if observed |
| Causal localization of forecast content | UNRESOLVED unless E3 LOCALIZED | donor-specific content under partial transplant | "chart linearly accessible" is reported separately (accessibility ≠ use) |

---

## 11. Scaffold accounting

| Scaffold | Supplied? | Control / charge |
| --- | --- | --- |
| Generic GRU/RNN cell and **its random initialization** | yes | **K-FR** tests whether supplied random dynamics plus a trained readout suffice |
| Stage one-hot (external timing scaffold) | yes | 3-bit convention, identical across arms; clockless = separate experiment |
| XOR head and loss; environment feedback | yes | supplies the demand, not the solution; K-PCO is descriptive |
| Readout MLP | yes | identical shape; parameters charged |
| Float precision | yes | b_sel selected on TRAIN, confirmed on TEST (§5.2) |
| K-TAB history buffer | yes (for K-TAB) | charged 8 bits (§5.1) |
| Covariance or joint slot; chart targets; filter equations; protected register/controller | **no** | absent |
| Exact oracle / chart | evaluation and analysis decoder only | never an input or target |

---

## 12. Thirteen admission answers (v1 updated)

1. **Q1.** Can generic recurrent training on environment-supplied outcomes acquire a history-dependent
   prediction function for joint queries? And is the recurrent organization itself acquired? (Answerable here only within the bounded E2/E3 wording of §9: E2 compares against the matched frozen-recurrence control at this budget; E3 tests localization by this intervention; neither establishes where the subspace came from.)
2. **Q2.** GRU-8 satisfies E1. E2 and E3 then determine whether the acquisition lies in the readout, in recurrent
   adaptation, and/or in causally localized state.
3. **Q3.** E1 NOT SHOWN. For the narrower claims: E2 = frozen-recurrence readout sufficient at this budget; E3 = not localized
   by this intervention.
4. **Q4.** K-FR (origin rival); K-2D and K-2D-MLP (dimension rivals); K-TAB (lookup); K-PCO (descriptive).
5. **Q5.** The PR #4 frozen world and oracle; the split rule; seeds; budget; thresholds; σ_sep; τ_den; λ; the
   quantizer, all to be frozen before training.
6. **Q6.** Record the assembled §9 claim; then any next step goes through a separate approval.
7. **Q7.** Record which component failed. Any change of architecture or budget is a new protocol.
8. **Q8.** Small GRUs on CPU; frozen generator; exact enumeration for evaluation.
9. **Q9.** Organizational (acquired function and state); engineering (training); no substrate claim.
10. **Q10.** §9.
11. **Q11.** A history-integrating predictive state; its mechanism is characterized only by literal labels.
12. **Q12.** Supplied: cell, random init, timing scaffold, readout, losses and feedback. Acquired: per E1–E3.
13. **Q13.** ADMIT moves the ledger from "acquisition untested" to the assembled claim, for C3-type claims only.
    C4 stays NOT_ESTABLISHED.

---

## 13. Flags

- **G1 (RULED, Consult #9): keep ¼ of the analytic product-readout excess** (a fixed accuracy requirement, not a requirement to beat K-PCO). *Original flag:* **G1. A-FIT's XOR clause uses the analytic product excess as a fixed numeric scale.** It is not a comparison
  with K-PCO. If the Specialist reads it as "must beat a product model", replace it with ¼ of the current-only
  XOR excess (whole-set analog 0.0088).
- **G2 (RULED, Consult #9): dropped.** K-FR is not run for K-2D or K-2D-MLP; total 120 runs. K-FR is kept for all
  four candidate configurations. *Original flag:* **K-FR for K-2D and K-2D-MLP.** These are included for symmetry. The total grows to 140 runs on CPU,
  which is still small. The extra arms can be dropped if wanted.
- **G3 (RULED, Consult #9): accepted as engineering choices**, subject to the Edit 4 denominator and coverage rules; no theoretical guarantee of coverage or significance. *Original flag:* **G3. The E2 ratio threshold ½ and the E3 thresholds (½, ¾) are new engineering choices,** as are σ_sep = 1/10,
  the ±20% norm match, τ_den = 1/100 and ridge λ = 10⁻³. All are PROPOSED.
- **G4 (RULED, Consult #9): cross-fitting adopted** (§6.3). *Original flag:* **G4. The E3 primary subspace uses the exact chart as an analysis decoder,** on 16 points in 8 dimensions (so
  there is overfitting risk). PCA is the exploratory alternative. Neither uses the chart in training.
- **G5 (RULED, Consult #9): accepted.** In-sample calibration then untouched TEST confirmation; no third split. *Original flag:* **G5. Selecting b_sel on TRAIN is in-sample** (there is no third split). The ruling allowed "select elsewhere,
  confirm on TEST". A dedicated validation split would shrink TRAIN; not proposed.
- **G6. K-2D-MLP** is included as a declared variant per the F4 ruling. No other architecture is added. No
  protected controller or register. No organism work.
- **G7. v1 untouched.** It now carries the Specialist's authorization note (md5 68ff5f5c…).
