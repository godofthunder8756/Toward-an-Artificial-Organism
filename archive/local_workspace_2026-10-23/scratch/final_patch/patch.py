src='/workspace/review/twostream_acquisition_protocol_draft_v2.md'
dst='/workspace/review/twostream_acquisition_protocol_FINAL.md'
t=open(src,encoding='utf-8').read()
def R(old,new,tag):
    global t
    n=t.count(old)
    assert n==1,(tag,n)
    t=t.replace(old,new)

# ---- edits-applied table (inserted after §0.1 table, before the first '---' following it)
R("""| V14 | Astra #7 | **Precision repair:** b is selected on TRAIN and confirmed on TEST, and the TEST curve is descriptive. The rules for rounding, clipping, ranges, metadata cost and invalid chart distributions are specified (§5). |
""","""| V14 | Astra #7 | **Precision repair:** b is selected on TRAIN and confirmed on TEST, and the TEST curve is descriptive. The rules for rounding, clipping, ranges, metadata cost and invalid chart distributions are specified (§5). |

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
""","table")

# ---- Edit 6: precision
R("""2. **State precision b_sel** (§5.2), and the charged state bits d × b_sel. K-TAB's buffer is exact: 8 bits.""",
"""2. **State precision b_sel** (§5.2), and the charged state bits d × b_sel. K-TAB's buffer is exact: 8 bits, and
   its logits stay float32 (no logit quantization; parameter quantization is a different resource experiment).""","E6a")
R("""- **Range.** [lo_ik, hi_ik] = the min and max of the unquantized float64 state over all TRAIN-reachable
  prefixes at stage k. These are computed once from the final checkpoint and then held constant.""",
"""- **Range.** [lo_ik, hi_ik] = the min and max of the unquantized float64 state over all TRAIN-reachable
  prefixes at stage k. These are computed once from the final checkpoint, **cast to float32 before any quantizer
  is constructed or used** (matching the charged metadata), and then held constant.""","E6b")
R("""- If no b ≤ 24 passes on TRAIN, b_sel = ">24".""",
"""- If no b ≤ 24 passes on TRAIN, b_sel = **"no qualifying precision in the declared grid"**. This can reflect
  poor fit rather than insufficient precision.""","E6c")
R("""- The exact update is then applied in float64 to the repaired chart.
- The repair is part of the quantized K-EXACT arm. It is not an error.""",
"""- The exact update is then applied in float64 to the repaired chart.
- The repair is part of the quantized K-EXACT arm. It is not an error.
- **Charged state.** The retained state between steps is the **three quantization indices only**. At each step
  the chart is reconstructed from the indices and projected (the repair above) deterministically, updated, and
  re-quantized to indices. No additional independent floating-point state is retained, so the charge of three
  b-bit coordinates is complete.""","E6d")
R("""**K-TAB.** The logits are quantized to b bits with ranges from TRAIN entries. Untrained (TEST) entries stay at 0,
which is exactly representable.""",
"""**K-TAB.** No logit quantization is applied. The history/index buffer is exact (8 bits) and the logits stay
float32.""","E6e")

# ---- Edit 3 + 4: §6.3
R("""**Subspace.**
- S_chart(A, seed) is the column space of the linear map fitted by ridge regression (λ = 10⁻³, intercept) from
  stage-4 states z₄(g) to the exact chart (m_x, m_y, c)(g).
- The fit uses all 16 stage-4 prefixes, all of which are TRAIN-reachable. It is frozen before any intervention
  is computed.
- dim S = 3, so this applies to H ≥ 4. For K-2D the whole state is used and the test is descriptive only.
- The chart is used **only as an analysis decoder**. It never enters training.""",
"""**Subspace (cross-fitted).**
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
  an analyst-defined test, not discovery of a naturally separate covariance module.""","E3")
R("""**Interventions** (Π = orthogonal projector onto S_chart):""",
"""**Interventions** (Π = Π^(f), the held-out fold's projector):""","E3b")
R("""**Statistics.** These are computed on the eligible T₄ᴴ trials, over all three queries and XOR-only.
- The tracking ratio ρ(target) = Σ‖F′ − q*(target·u)‖² / Σ‖F′ − q*(a·u)‖² is a ratio of sums over trials, so
  no per-trial denominator arises.
- Absolute error: mean ‖(F′ − F(a·u)) − Δ*‖².
- Normalized error: §6.5.""",
"""**Statistics.** These are computed on the eligible cross-fitted T₄ᴴ trials (§6.4), over all three queries
(the three-output vector) and XOR-only.
- **One trial subset.** The **same** eligible trial subset is used for the partial, complement and wrong-donor
  comparisons.
- The tracking ratio ρ(target) = Σ‖F′ − q*(target·u)‖² / Σ‖F′ − q*(a·u)‖² is a ratio of sums over trials.
  **A ratio denominator at or below 10⁻¹² is undefined and cannot pass.**
- Absolute error: mean ‖(F′ − F(a·u)) − Δ*‖². **Absolute errors are reported alongside every ratio.**
- Normalized error: §6.5.""","E4a")

# ---- Edit 4: eligibility
R("""**Wrong-donor eligibility (prespecified).** For trial (a, b, u), a donor c ∉ {a, b} at stage 4 is eligible iff:""",
"""**Trial eligibility (prespecified).** A cross-fitted T₄ᴴ trial (a, b, u) is eligible iff the **intended donor's
oracle XOR change |Δ*_XOR(a→b, u)| ≥ 1/100** and an eligible wrong donor exists under the conditions below.

**Coverage.** Eligible trials must cover **at least 10% of cross-fitted T₄ᴴ**, with **at least four distinct
recipients and four distinct intended donors in each fold**. Otherwise E3 is **UNRESOLVED**, not "not localized".

**Wrong-donor eligibility (prespecified).** For trial (a, b, u), a donor c ∉ {a, b} at stage 4, **in the same
held-out fold**, is eligible iff:""","E4b")
R("""Among eligible donors, the one closest in norm is chosen; ties go to the lowest prefix integer. Trials with no
eligible c are dropped from this control, and the drop count is reported.""",
"""Among eligible donors, the one closest in norm is chosen; ties go to the lowest prefix integer. Trials with no
eligible c are dropped from **all three comparisons** (common subset), and the drop count is reported.""","E4c")

# ---- Edit 5: K-FR paragraph in §6.4
R("""**Same intervention on K-FR.** The partial-intervention statistics are computed on the K-FR network of the same
seed: frozen random recurrence, trained readout, its own S_chart. This tells whether the localization pattern
needs recurrent training.""",
"""**Same intervention on K-FR.** The cross-fitted partial-intervention statistics are computed on the K-FR network
of the same seed: frozen random recurrence, trained readout, its own cross-fitted S_chart. Whether K-FR meets
A-FIT is reported alongside, since poor prediction alone can prevent donor tracking. The comparison can show only
whether a pattern is **observed in CAND but not in the matched frozen-recurrence control under this budget**.""","E5a")

# ---- G2: K-FR scope
R("""It is run for every recurrent configuration (GRU-4/8/16, RNN-8, K-2D, K-2D-MLP).""",
"""It is run for all four candidate configurations (GRU-4/8/16, RNN-8). It is **not** run for K-2D or K-2D-MLP,
whose role is performance reproduction, not origin attribution (Consult #9, G2).""","G2a")
R("""The only difference is `requires_grad=False` on the recurrent parameters (and, for K-2D-MLP,
on W_a, b_a, W_b, b_b).""",
"""The only difference is `requires_grad=False` on the recurrent parameters.""","G2b")
R("""  - K-FR for each of these and for K-2D and K-2D-MLP.
  - K-2D, K-2D-MLP, K-TAB, K-PCO.
  - Total 14 configurations × 10 = 140 runs. CPU, single-threaded, deterministic.""",
"""  - K-FR for each of these.
  - K-2D, K-2D-MLP, K-TAB, K-PCO.
  - Total 12 configurations × 10 = 120 runs. CPU, single-threaded, deterministic.""","G2c")

# ---- Edit 1
R("""Reference quantities on TEST and TRAIN are computed at freeze from the frozen `results.json`:
- E_CUR: total current-only excess;""",
"""Reference quantities on TEST and TRAIN are computed at freeze from the frozen `results.json`:
- E_CUR(split): the **split-specific** total current-only excess. Within each split, the optimal current-only
  forecast is computed by averaging q*(h), weighted by P(h), separately for each final reading (reading 8). Its
  excess over the full-history oracle is then computed within that split. PR #4's unconditional current-only
  forecasts are **not** merely reweighted, because conditioning on the TRAIN/TEST selection changes the
  distribution. This split-specific reference is used wherever E_CUR appears;""","E1")

# ---- Edit 2: §8.2
R("""**Paired statistic per seed.** ratio_s = E_CAND,total(TEST) / E_K-FR,total(TEST). The XOR version is also
reported.""",
"""**Paired statistic per seed.** ratio_s = E_CAND,total(TEST) / E_K-FR,total(TEST). The XOR version is also
reported.
- A seed counts toward "recurrent adaptation supported" only if its CAND and K-FR runs are both **intact and
  valid** (integrity holds for both).
- A K-FR excess at or below 10⁻¹² is a **numerical tie**, not evidence for a ratio improvement. Such a seed
  cannot satisfy ratio_s ≤ ½.""","E2a")
R("""| **ACQUIRED READOUT OVER SUPPLIED RECURRENT DYNAMICS** | K-FR satisfies A-FIT in at least 8/10 seeds **and** ratio_s ≤ ½ in at most 2/10 |""",
"""| **FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET** | K-FR satisfies A-FIT in at least 8/10 seeds **and** ratio_s ≤ ½ in at most 2/10. The label describes **K-FR**, not how CAND works. CAND's recurrent contribution is recorded as **not established by this comparison**. |""","E2b")

# ---- Edit 5: §8.3
R("""- partial transplant ρ(b) ≤ ½;
- wrong-donor partial transplant ρ(c) ≤ ½;
- complement transplant ρ(b) ≥ ¾.""",
"""- partial transplant ρ(b) ≤ ½;
- wrong-donor partial transplant ρ(c) ≤ ½;
- complement transplant ρ(b) ≥ ¾.

Each inequality must hold for **both** the three-output vector and the XOR-only statistic. An undefined ratio
(denominator ≤ 10⁻¹²) cannot pass. If the coverage rule (§6.4) fails or the numerical rank is below three (§6.3),
E3 is UNRESOLVED.""","E4d")
R("""**Per seed (GRU-8 CAND), on eligible T₄ᴴ trials,**""","""**Per seed (GRU-8 CAND), on eligible cross-fitted T₄ᴴ trials,**""","E4e")
R("""**Qualifier.** "Requires recurrent training" is added only if K-FR is NOT LOCALIZED in at least 8/10 seeds.""",
"""**Qualifier.** "**Observed in CAND but not in the matched frozen-recurrence control under this budget**" is
added only if K-FR is NOT LOCALIZED in at least 8/10 seeds. Whether K-FR meets A-FIT is reported alongside that
comparison, since poor prediction alone can prevent donor tracking.""","E5b")

# ---- §9
R("""| E2 = ACQUIRED READOUT OVER SUPPLIED RECURRENT DYNAMICS | "…realized as an acquired readout over supplied (untrained) recurrent dynamics." |""",
"""| E2 = FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET | "A frozen-recurrence control (K-FR: the same initialized network with only the readout trained, same episodes and budget) also met A-FIT at this budget. CAND's recurrent contribution is not established by this comparison." |""","E2c")
R("""(+ "requiring recurrent training" if qualified)""","""(+ "observed in CAND but not in the matched frozen-recurrence control under this budget" if qualified)""","E5c")
R("""- "hidden-state organization acquired" without both E2 SUPPORTED and E3 LOCALIZED;""",
"""- "hidden-state organization acquired", or any claim that E2 plus E3 establishes the origin of the localized
  subspace or that it is an independently manipulable natural module. When E2 = SUPPORTED and E3 = LOCALIZED, the
  permitted wording is: "**Training recurrent parameters improved prediction relative to K-FR, and a cross-fitted
  chart-decoder subspace redirected forecasts under the specified partial interventions.**" These are two
  supported findings, not proof that training created that subspace;""","E5d")

# ---- §10
R("""| Recurrent dynamics organization | **SUPPLIED (random init)** if E2 = acquired-readout; **ACQUIRED (in part)** if E2 = SUPPORTED; else UNRESOLVED |""",
"""| Recurrent dynamics organization | If E2 = FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET: CAND's trained recurrent dynamics are **not** labelled SUPPLIED; the recurrent contribution is **not established by this comparison**. **ACQUIRED (in part)** if E2 = SUPPORTED; else UNRESOLVED |""","E2d")

# ---- §12 Q3
R("""E2 = acquired readout over supplied dynamics;""","""E2 = frozen-recurrence readout sufficient at this budget;""","E2e")

# ---- §13 G rulings
R("""- **G2. K-FR for K-2D and K-2D-MLP.** These are included for symmetry. The total grows to 140 runs on CPU,""",
"""- **G2 (RULED, Consult #9): dropped.** K-FR is not run for K-2D or K-2D-MLP; total 120 runs. K-FR is kept for all
  four candidate configurations. *Original flag:* **K-FR for K-2D and K-2D-MLP.** These are included for symmetry. The total grows to 140 runs on CPU,""","G2d")
for tag,old,new in [
 ("G1","- **G1. A-FIT's XOR clause","- **G1 (RULED, Consult #9): keep ¼ of the analytic product-readout excess** (a fixed accuracy requirement, not a requirement to beat K-PCO). *Original flag:* **G1. A-FIT's XOR clause"),
 ("G3","- **G3. The E2 ratio threshold","- **G3 (RULED, Consult #9): accepted as engineering choices**, subject to the Edit 4 denominator and coverage rules; no theoretical guarantee of coverage or significance. *Original flag:* **G3. The E2 ratio threshold"),
 ("G4","- **G4. The E3 primary subspace","- **G4 (RULED, Consult #9): cross-fitting adopted** (§6.3). *Original flag:* **G4. The E3 primary subspace"),
 ("G5","- **G5. Selecting b_sel on TRAIN","- **G5 (RULED, Consult #9): accepted.** In-sample calibration then untouched TEST confirmation; no third split. *Original flag:* **G5. Selecting b_sel on TRAIN")]:
    R(old,new,tag)
open(dst,'w',encoding='utf-8').write(t)
print('ok')
