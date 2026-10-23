# Graded recurrent reversion against both first-order-matched and isotropic controls: protocol (FINAL v1)

> **FINAL TEXT FOR HASHING. NOT RUN.**
> - Astra consult #17 (FREEZE WITH NAMED EDITS) is applied in full. That covers edits 1–10, the O1 choice (a), and the rulings on O2–O10 and A1–A10 (§0.1, §13).
> - Consult #17: "The edits below are sufficient for scientific clearance without another review round."
> - Nothing is frozen, committed or pushed by the Research Delegate. Hashing and freezing belong to the implementing agent under §9.
> - No control path has been built or evaluated. The only computations are the read-only feasibility checks in Appendix B.
>
> **Authorization.**
> - **Phase A (EXPLORATORY).** Evaluation only, no training, seeds 100–109 and 200–209. Consult #17, O9: "Yes: evaluation-only Phase A may proceed under the described standing authorization after these edits and hashing. No training is authorized by this ruling."
> - **Phase B (CONFIRMATION).** Fresh seeds 300–309, 30 training runs. Aidan's explicit approval is **recorded** (§0.2), and Astra cleared the protocol in consult #17.
>
> **This is a new study, not a reinterpretation of PR #8.** PR #8's labels stand: REPLICATED 9/10, confirmed by consult #16, with errata E-B3 to E-B7. They also carry the additive interpretation note from consult #17, O1 (`/workspace/review/pr8_errata_v3_interpretation_note.md`).

**Sources.**
- Astra consult #17: `/workspace/astra_consult17_response.txt` (sha256 `98df0ab9…59216230`).
- Draft v1: `/workspace/review/first_order_control_protocol_draft_v1.md` (sha256 `50f80ec32cade6411d5a950672d7c7bdb8600ea86be7d91288e72ec75e8d4fb1`), **left untouched**.
- Spec: the second section of `/workspace/review/pr8_errata_v2_request_consult16.md` (`92958927…`).
- Astra consult #16: `/workspace/astra_consult16_response.txt` (`91ccdbf7…`).
- Graded reversion FINAL (PR #8): `/workspace/review/graded_reversion_protocol_FINAL.md` (`1a5e62bd…89bfa3`).
- PR #8 results review: `/workspace/review/graded_reversion_results_review_v1.md`.
- Recurrent-core FINAL (PR #7): `/workspace/review/recurrent_core_transfer_protocol_FINAL.md` (`63c463c7…`).
- PR #8 implementation, read-only scratch clone: `/workspace/scratch/pr8/clone` (freeze `018f2a7`, results `7008026`).

**Scope guards.**
- GRU-8 only, in the same W2 world, with the same fresh-readout intervention, dose grid, L_prefix and block norms as PR #8.
- No new architecture family, no protected controller or register, and no organism work.
- No localization: no decoder, no subspace search, no E3/P1/P2.
- No one-sided family and no curvature matching (consult #17, O1).
- Below C4. No consciousness claim.
- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate (§11).

---

## 0. Inherited, unchanged

Everything not changed in §§1–9 is inherited verbatim from graded reversion FINAL §0 and §§3–6, and through it from recurrent-core FINAL §0.1, §1, §3 and §8:
- the W2 world, q_star = `world.q`, and TRAIN/TEST 192/64;
- INPUT_SIZE 9, zero initial state, and float64 exhaustive evaluation of all 256 histories;
- the PR #7 training recipe (4000 steps, batch 256, Adam, cosine 1e-3→1e-4, clip 1.0, `set_num_threads(1)`, deterministic);
- the arms CAND → W_T, F-TRAINED (W_T frozen with a fresh 8→32→3 readout from torch seed 5000+s) and F-INIT (W_0 frozen, same readout initialization);
- A-FIT, the E1 prerequisite, the transfer rule, IDENTITY_TOL = 1e-9 and eps0 = 1e-12;
- the **REV path** W(α) = W_T + α·(W_0 − W_T), α ∈ 𝒜 = {0, 1/8, 1/4, 1/2, 3/4, 1}, applied at updates 5–8 only (`stage_idx` 4–7) through `MatrixOverride`. The primary target is the complete `weight_hh_l0` (24×8). The secondary targets are the blocks r (rows 0–7), z (8–15) and n (16–23);
- the α = 1 endpoint sentence, the readout and compatibility limitation, the AUC interpolant disclaimer, the saturation rule and the displacement/zero-block rule, verbatim from graded reversion FINAL §§3–6;
- the L_prefix ASCII definition (FINAL §5; no division by three; uniform complete 16×16 grid primary) and PD(q_star) = 0.0138386;
- B_prefix, C_prefix, eligibility conditions 1–5, the trapezoid weights (1/16, 1/8, 3/16, 1/4, 1/4, 1/8), and the integrity checks SHAM, RESTORE, ENDPOINT, checkpoint sha and outputs.

**Changed relative to PR #8:**
- two decision-bearing control families, FO and ISO, combined in a conjunctive directional rule (§4, §6);
- first-order diagnostics, degenerate-case rules, margin reporting, labels and claim strings.

## 0.1 Consult #17 edits applied

| # | Consult #17 item | Where |
| --- | --- | --- |
| O1 | Option (a): the same seeds must beat **both** the FO and ISO families. No one-sided family and no curvature matching. Additive PR #8 interpretation note | §1, §4.4, §6, §7, §13. Note: `pr8_errata_v3_interpretation_note.md` |
| 1 | D_FO, D_ISO, D = D_FO and D_ISO; joint = valid ∧ eligible ∧ D_FO ∧ D_ISO ∧ M; at least 8/10 on the joint rule; same for secondary blocks; new success and failure labels; report D_FO, D_ISO, their intersection, M and joint counts | §6, §7 |
| 2 | Rationale replaced, verbatim | §1, §10 Q5 |
| 3 | Success paragraph replaced (duplicated limitation removed); failure sentence; failure not auto-attributed to FO | §8 |
| 4 | `g_k` / `gh_k` notation; orthogonality checks use `gh_k` | §4.2, §12 |
| 5 | Collapsed block: e_jk := d_k; R_eff for primary collapse; fixed blocks reported | §4.5 |
| 6 | G_ZERO diagnostic only, named NEGLIGIBLE FIRST-ORDER SCALE; isotropic fallback only for an exactly zero gradient; FD absolute floor | §4.1, §4.5, §12 |
| 7 | Cancellation-safe radius gate; the sqrt form is descriptive only | §4.2, §4.5, §12 |
| 8 | Joint counting of unevaluable seeds | §7 |
| 9 | Manifest timing | §2 S1, §9 |
| 10 | Reporting consistency: aggregate thin-margin text in phase B only; margins against both families; UNDEFINED percentages; endpoint ties versus strict exceedances; checkpoint wording | §4.1, §6.1, §7, §10 Q12 |
| O2–O10 | Rulings applied | §13 |
| A1–A10 | Rulings applied | §13 |

## 0.2 Phase B approval record

| item | record |
| --- | --- |
| Who | Aidan Ahern |
| When | **2026-10-21, 1:05 AM ET** |
| Source | Grok Bot chat, widget **t23s2** (as relayed by the ACI Research Specialist) |
| Question (verbatim) | "Approve fresh-seed GRU-8 training (seeds 300-309, 30 runs) for the first-order-matched control confirmation once Astra clears the protocol?" |
| Answer (verbatim) | "Yes, approve it once Astra clears it." |
| Condition | Astra clearance, given in consult #17 (FREEZE WITH NAMED EDITS: "The edits below are sufficient for scientific clearance without another review round."). |
| Scope note | Astra's revised study name (O10) adds ISO as decision-bearing: "Approve fresh-seed GRU-8 training (seeds 300-309, 30 runs, PR #7 recipe) for graded reversion confirmation against both first-order-matched and isotropic controls once Astra clears the protocol?" The approved design is strictly more demanding (D = D_FO and D_ISO) and uses the same 30 training runs (CAND, F-TRAINED and F-INIT × seeds 300–309, PR #7 recipe). **The Specialist therefore treats it as within the approval.** |
| Timing | The approval **predates any phase B training**. No phase B training has occurred. |
| Not covered | Any training beyond these 30 runs, any change of seeds, recipe or arms, and the PR #8 Appendix A (still unapproved). |

The implementing agent commits this record (with date, time ET, source, question and answer verbatim) in the freeze commit before phase B training.

---

## 1. Question and design

**Question (Q-CAUSE, organization level, bounded).** The intervention interpolates the complete hidden-to-hidden matrix toward initialization during updates 5–8, with trained input weights, biases and the fresh readout held fixed. Does it produce greater dose-averaged excess prefix-function loss than **both** of these, in the same seeds?
- 32 paths matched to it block by block in Frobenius norm **and** in initial loss derivative at the trained weights (FO);
- 32 paths matched block by block in Frobenius norm only (ISO, the PR #8 family).

**Rationale (consult #17, edit 2, verbatim):**

> "Existing-checkpoint feasibility checks do not support a dominant positive initial-gradient explanation of PR #8's sampled early-dose damage. This study asks whether reversion's dose-averaged advantage survives conditioning controls on its initial loss slope while also retaining the original isotropic comparison. Neither control family is assumed uniformly more stringent than the other."

**Feasibility context (consult #17, O1).**
- In 15/20 existing seeds the initial tangent predicts improvement, not damage. In the other five it explains at most 23% of the observed damage at α = 1/8.
- The initial tangent therefore does not explain the positive damage at that dose. This does not mean the first-order term is absent.
- For a genuinely negative derivative, sufficiently small positive doses must initially *decrease* loss. Non-decreasing values on the sampled grid therefore do not imply a continuously monotonic path.
- Negative slopes also do **not prove** that FO controls have smaller finite-dose AUCs than ISO controls. That remains unmeasured.
- Conjunctive gating prevents a success based solely on a potentially easier family.
- First-order matching is a conditional comparison, not an automatically stronger control.

**Scope of the comparison.** "Exceeds" means dose-averaged trapezoidal AUC over the specified path (consult #16, E-B5). It does not mean every dose, the endpoint, or arbitrary perturbations. The comparison is always qualified by the sampled families, local derivative matching and finite-dose AUC (O5).

**Not:**
- localization;
- a "stores content" or semantic-content test;
- a test of curvature as a mechanism;
- a necessity test;
- an XOR-specific test;
- a monotonicity test;
- a test of selectivity over continuation processing;
- a test of a uniquely identified mechanism.

## 1.1 Control family rejected: foreign-seed weight_hh (recorded)

Interpolating toward another seed's trained `weight_hh` was considered (PR #8 review §7, item 2) and **rejected by Astra** (consult #16 §4, verbatim):

> "Foreign-seed trained matrices are weaker controls for this question: hidden-unit coordinates differ across seeds, so transplanting one matrix can create coordinate incompatibility. Such substitutions also do not automatically match first-order loss effects."

No hidden-unit alignment is attempted, and no foreign-seed condition appears in this protocol.

**Also not added (consult #17, O1, verbatim):**

> "Do not add the one-sided family or curvature matching here. Clipping negative projections changes the matching question. Per-block curvature matching would also omit cross-block Hessian terms relevant to joint reversion; matching full directional curvature would require a separately specified sampler and feasibility audit."

## 2. Phases, seed ranges and safeguards

| phase | seeds | weights | training | status |
| --- | --- | --- | --- | --- |
| **A: EXPLORATORY** | **100–109** (PR #7) and **200–209** (PR #8) | PR #7 `recurrent_core_results_v1/checkpoints/s{s}_{f_trained,f_init,cand_init}.ckpt` at `5157f5d`; PR #8 `graded_reversion_results_v1/checkpoints/` at `7008026`; sha256-verified | none | development only; **never confirmatory**; per-seed only; the two groups are reported separately and never pooled. Standing authorization after hashing (O9) |
| **B: CONFIRMATION** | **300–309** (fresh; disjoint from 0–9, 100–109 and 200–209) | newly trained CAND → W_T, F-TRAINED, F-INIT | **30 runs** (3 × 10), PR #7 recipe unchanged | the only phase that can earn a §7 label. **Approval recorded (§0.2); Astra cleared (consult #17)** |

**Safeguards.**
- **S1. Freeze before phase A (consult #17, edit 9, verbatim):**

  > "Before Phase A, freeze the construction code, tolerances, generator seeds and base Gaussian draw manifests for both phases. After each checkpoint and gradient are available, construct and hash the transformed paths before evaluating their dose curves. Record checkpoint, gradient and transformed-path hashes together."

  - The FINAL text and test suite are hashed with the code.
  - The base Gaussian draw manifests (FO base draws, ISO draws and gradient-check directions) cover seeds 100–109, 200–209 and 300–309.
- **S2. Label namespace.**
  - Phase A outputs are prefixed **"EXPLORATORY (PHASE A, PR #7 SEEDS 100–109 / PR #8 SEEDS 200–209; DEVELOPMENT ONLY; NOT CONFIRMATORY)"**.
  - Phase A never uses REPLICATED, DEMONSTRATED, SHOWN or CONFIRMED, and gives no out-of-ten verdict line.
- **S3. No carry-over.** Phase A outputs cannot change any scientific parameter. These are:
  - the dose grid, the number of paths per family and the generator seeds;
  - the gradient point and definition, the matching rule and all §12 tolerances and thresholds;
  - the outcome, statistic, eligibility, materiality and conjunctive directional rule;
  - the replication and unevaluable-seed rules;
  - the thin-margin cutoff.
- **S4.** A scientific change after phase A is a new version, reviewed by Astra and hashed before phase B training. Its labels carry **"(CRITERION REVISED AFTER EXPLORATORY PHASE A)"**.
- **S5.** Engineering fixes are versioned and hashed before phase B and logged in `DEVIATIONS_AND_AMBIGUITIES`. Superseded phase A outputs are retained and labelled with their code version.
- **S6. Pre-exposure.** Neither phase A group is naive:
  - Seeds 200–209 were PR #8's confirmatory seeds. Their REV and ISO curves and margins are public (E-B3).
  - Seeds 100–109 have public PR #7 and PR #8 phase A results.
  - Gradient geometry at W_T for all 20 seeds was computed for the draft (Appendix B).
  - Phase A cannot alter, strengthen or weaken PR #8's labels.
- **S7. Seed accounting.** Phase B uses exactly 300–309, with no replacement or addition. Missing cells are reported.
- **S8. Artifacts.**
  - Phase A outputs go to `first_order_control_phaseA_exploratory/`.
  - Phase B outputs go to `first_order_control_results_v1/`. They cite phase A only in a separately headed "Development history" section.
  - Existing PR #7 and PR #8 files are never edited.
- **S9. Phase A reporting.** Per-seed D_FO, D_ISO and M flags, margins against both families, first-order diagnostics and endpoint errors, explicitly exploratory. **No aggregate thin-margin sentences** (edit 10), no pooling, no aggregate verdict, no use as confirmation.

## 3. Intervention path (REV): unchanged

As in graded reversion FINAL §3, with ‖W(1) − W_0‖_max ≤ eps0 and W(0) = W_T exactly.

**Phase A cross-check:** recomputed REV curves must equal PR #8's committed `delta_rev` values within 1e-15 absolute. A mismatch is an engineering flag and makes the seed invalid in phase A.

## 4. Controls

### 4.1 Gradient (analysis control; oracle-informed; not training)

- **Override parametrization.** A single 24×8 float64 leaf tensor V, applied as `weight_hh_l0` at updates 5–8 only (stage_idx 4–7). It is tied across the four stages, matching how W(α) is applied.
- **Detachment (O3, A1–A3).** Updates 1–4 use the intact trained W_T. **The stage-4 state h_4 is explicitly detached.** All other parameters (W_ih, b_ih, b_hh and the readout) are frozen, with `requires_grad = False`. The gradient therefore flows only into V.
- **Evaluation point.** V = W_T, with the F-TRAINED fresh readout and the complete uniform 256-history grid.
- **Gradient.** G = ∂L_prefix/∂V at V = W_T, by torch autograd in float64, in a non-inference-mode rollout functionally identical to the evaluation rollout. G sums over the four tied stages. The loss is the primary L_prefix only.
- **Disclosure (verbatim for results):** "The first-order matching uses the gradient of the oracle-referenced prefix-function loss at the trained weights. It is an oracle-informed analysis control, applied after training; it is not network training and does not train the network or modify its saved checkpoint."
- **Gradient checks (validity).** Central finite differences of L_prefix with step h = 1e-6 (Frobenius units) along four unit directions in V-space:
  - d/‖d‖;
  - three random unit directions from `torch.Generator` seed 2,000,000 + 100·s.

  Each must satisfy (consult #17, edit 6):

  ```text
  abs(FD - dot(G, direction)) <= 1e-10 + 1e-6*norm(G)
  ```

  Two independent gradient computations must also be byte-identical. A failure, or a non-finite G, makes the seed **invalid**.
- **Autograd confirmation of Appendix B.** The frozen implementation reports, for every phase A seed, ⟨G, delta⟩ and cos(G, delta) from autograd. These confirm or correct the draft-stage finite-difference values, which consult #17 requires ("Confirmation of the derivative calculations by the new autograd implementation is required").

### 4.2 FO path construction (per block k ∈ {r, z, n}, per path j = 1…32)

- **Base draws:** `torch.Generator`, seed 1,000,000 + 100·s. Draws j = 1…32 in order, each one `torch.randn((24, 8), dtype=torch.float64, generator=...)` call giving Z_j. z_jk is block k of Z_j, vectorized row-major, the same as d_k and g_k.
- **Notation (consult #17, edit 4):**

```text
g_k  = vec(block k of G)       # unnormalized gradient
gh_k = g_k / norm(g_k)        # unit gradient, when nonzero
```

- **Construction:** for a non-collapsed block with a nonzero gradient.

```text
d_k   = vec(W0_k - WT_k)
a_k   = dot(g_k, d_k) / dot(g_k, g_k)
p_k   = a_k * g_k                         # gradient component of d_k
r_k   = norm(d_k - p_k)                   # residual radius (authoritative)
y_jk  = z_jk - dot(z_jk, gh_k) * gh_k
y_jk  = y_jk - dot(y_jk, gh_k) * gh_k     # second Gram-Schmidt pass
u_jk  = y_jk / norm(y_jk)
e_jk  = p_k + r_k * u_jk
```

  `g_k` is never overwritten. All orthogonality checks use `gh_k`.
- **Radius validation (consult #17, edit 7):**

  ```text
  abs(norm(d_k)^2 - norm(p_k)^2 - r_k^2)
      <= 1e-12 * norm(d_k)^2
  ```

  The cancellation-prone square-root form sqrt(‖d_k‖² − a_k²‖g_k‖²) may be reported descriptively. It does not gate.
- **Assembled path:** E_j = [e_jr; e_jz; e_jn], reshaped to 24×8.
  - Primary path: W_FO,j(α) = W_T + α·E_j.
  - Secondary block k: W_hk^T + α·e_jk (same draw; correlated).
- **Matched properties.**
  - Per block: ‖e_jk‖ = ‖d_k‖ and ⟨g_k, e_jk⟩ = ⟨g_k, d_k⟩.
  - Hence for the assembled matrix: ‖E_j‖_F = ‖delta‖_F and ⟨G, E_j⟩ = ⟨G, delta⟩.
  - Untouched blocks have zero displacement, so no further neutrality test is needed (O4).
  - The family for block k is the sphere {e : ‖e‖ = ‖d_k‖, ⟨g_k,e⟩ = ⟨g_k,d_k⟩}, which contains d_k.
- **Scope of matching.** The match is local, at W_T only. At finite α the paths differ through higher-order terms.
- **Two-sided match.** The match is two-sided, and neither family is assumed uniformly more stringent than the other (§1). The finite-dose ordering of FO against ISO AUCs is unmeasured and is reported, not assumed.

### 4.3 Reuse

The 32 FO and 32 ISO paths are each built once per seed and reused at every dose and across the primary and secondary targets. Transformed FO paths are hashed before any dose curve is evaluated (S1). No redraw, rejection or reordering is allowed except under §4.5.

### 4.4 ISO paths (decision-bearing)

- This is the PR #8 family, unchanged: generator 40000 + 100·s, 32 draws, per-block rescaling to ‖d_k‖_F, and the PR #8 zero-block rule.
- **Phase A:** the draws are byte-identical to PR #8's and must match the PR #8 freeze manifest. A mismatch is an engineering flag and makes the seed invalid in phase A.
- **Phase B:** seeds 300–309 give generator seeds 70000–70900.
- **ISO is decision-bearing (consult #17, O1 and edit 1).** D_ISO enters the joint rule (§6).
- **Descriptive extra:** ⟨G, eps_j⟩ for every ISO path.

### 4.5 Degenerate cases (frozen)

The draft's thresholds were written down before any gradient was computed (scratch `PREREG_THRESHOLDS_BEFORE_CHECK.txt`, 00:58:49 ET). O2 accepted them (1e-10, 1e-3 and 0.10) with repairs 5–8. None is triggered on any of the 20 existing seeds (Appendix B).

| case | test (per block k unless stated) | action | status |
| --- | --- | --- | --- |
| **Zero block displacement** | ‖d_k‖_F ≤ eps0 | e_jk = 0 (PR #8 rule) | primary eligibility needs ‖delta‖_F > eps0; secondary k ineligible (non-pass) |
| **Exactly zero gradient** | g_k = 0 exactly (every entry 0.0) | e_jk := ‖d_k‖·z_jk/‖z_jk‖, the norm-matched isotropic draw. Its first-order match is exact | valid; reported |
| **Nonzero gradient** (however small) | g_k ≠ 0 | the §4.2 projection construction and all matching checks | ordinary |
| **NEGLIGIBLE FIRST-ORDER SCALE** (diagnostic only) | ‖g_k‖_F·‖d_k‖_F ≤ G_ZERO = 1e-10 | **none.** Edit 6: "G_ZERO is a diagnostic threshold only. For every nonzero gradient, use the projection construction and its matching checks. For an exactly zero gradient, use the norm-matched isotropic draw; its first-order match is exact. Numerical inability to construct or validate a nonzero-gradient match is an integrity failure." | flag reported; never called exact; no label effect |
| **Collapsed block** | ρ_k = r_k/‖d_k‖ ≤ RHO_COLLAPSE = 1e-3 (r_k from the authoritative form) | Edit 5: "For a collapsed block, set e_jk := d_k for every draw. The block has no randomized spread. Its secondary comparison is ineligible." | secondary k: collapsed control family (counts toward §7 step 2 for target k); primary: see the next row; the fixed blocks are reported |
| **Collapsed primary family** | R_eff/‖delta‖_F ≤ RHO_COLLAPSE, with `R_eff^2 = sum of r_k^2 over non-collapsed blocks` (collapsed blocks contribute zero randomized radius) | as above | primary: collapsed control family; non-evaluable (O2), counted under §7 step 2 |
| **Near-collapse** (descriptive) | ρ_k ≤ RHO_NEAR = 0.10, or R_eff/‖delta‖ ≤ 0.10 | none | flag reported with ρ and R_eff; no label effect |
| **Negative or zero a_k** | a_k ≤ 0 | none; the formula applies unchanged | ordinary; sign reported |
| **Construction or validation failure** (nonzero gradient) | ‖y_jk‖ ≤ 1e-12·‖z_jk‖, ‖z_jk‖ = 0, a non-finite value, or any §12 matching or radius check failing | no redraw | **integrity failure: seed invalid** |

**Status of collapse (O2).** "Collapse is non-evaluability, not an engineering failure." A collapsed seed is not invalid. It is counted jointly with invalid seeds under §7 step 2.

### 4.6 Integrity checks (no evidential role)

The PR #8 checks are inherited: SHAM, RESTORE, ENDPOINT, checkpoint sha, and outputs finite and in (0, 1) at every dose and direction, for both families. Added:
- the gradient checks (§4.1);
- the matching and radius checks (§12);
- the base-draw manifest checks and the transformed-path hashes (S1);
- the phase A REV and ISO cross-checks against PR #8.

Any failure makes the seed **invalid**.

## 5. Outcomes: unchanged

- **Primary:** L_prefix exactly as in graded reversion FINAL §5.
- **Descriptive:** L_cont, per-component terms, TEST/TRAIN excesses, PD/CD, and the probability-weighted and TEST-restricted versions. XOR is explicit but descriptive.
- Vector success does not establish an XOR-specific effect.

## 6. Curve statistic and per-seed criterion

**Curves.** For c ∈ {REV, FO_j, ISO_j}:
- Delta_c(α) = L_prefix(c, α) − L_prefix(F-TRAINED intact);
- AUC_c = Σ_α w_α·Delta_c(α), with the PR #8 weights.

The PR #8 AUC disclaimer applies verbatim, and negative excesses are retained.

**Eligibility.** A failure is a **non-pass, not invalid**:
1. valid;
2. transfer pass;
3. B_prefix > eps0;
4. C_prefix > eps0;
5. displacement > eps0;
6. non-collapsed control family for the target (§4.5; collapse is also counted under §7 step 2).

**Per-seed criterion (consult #17, edit 1, verbatim):**

```text
D_FO  = (AUC_REV - max_j AUC_FO,j > eps0)
D_ISO = (AUC_REV - max_j AUC_ISO,j > eps0)
D     = D_FO and D_ISO

Joint pass = valid and eligible and D_FO and D_ISO and M
```

**(M) Materiality (unchanged):** AUC_REV > eps0 **and** AUC_REV ≥ B_prefix/4, with no PD-relative floor.

The same rule applies to the secondary blocks, using each family's block-k paths.

**First-order diagnostics** (descriptive, per seed and target; never gating):
- ⟨G, delta⟩ and cos(G, delta); per block a_k, ⟨g_k,d_k⟩, cos(g_k,d_k), ρ_k and R_eff/‖delta‖; the fixed (collapsed) blocks.
- FO_AUC = ⟨G, delta⟩/2, the AUC of the initial tangent, since Σ_α w_α·α = 1/2.
- **AUC − FO_AUC** for REV, each FO path and each ISO path. This is named **"residual after subtracting the initial tangent contribution."** **It is not a curvature estimate** (O8).
- Delta_REV(1/8) against ⟨G,delta⟩/8.
- The saturation index (PR #8 rule), monotonic-step count, and per-dose ranks within each family.
- Sampled non-decreasing values do not imply a continuously monotonic path (consult #17, O1).

### 6.1 Margin reporting (mandatory, every seed and target, both phases, **both families**)

For F ∈ {FO, ISO}:

| column | definition |
| --- | --- |
| margin_F | AUC_REV − max_j AUC_F,j |
| m/B, m/PD | margin_F / B_prefix, margin_F / PD(q_star) |
| m/maxC_F | margin_F / max_j AUC_F,j. **UNDEFINED** when max_j AUC_F,j ≤ eps0, which includes nonpositive values (edit 10) |
| rank_F | rank of REV among 1 + 32 by AUC (1 = most damaging; ties count against REV) |
| per-dose rank_F | at α = 1/8, 1/4, 1/2, 3/4, 1 |
| n_end_gt_F | number of F paths with Delta_F,j(1) − Delta_REV(1) > eps0 (strictly greater control loss) |
| n_end_tie_F | number of F paths with \|Delta_F,j(1) − Delta_REV(1)\| ≤ eps0 (endpoint ties; reported separately, edit 10) |
| endpoint-D_F | Delta_REV(1) − max_j Delta_F,j(1) > eps0 (descriptive only) |
| median and max AUC_F | together with all 32 values |

Also reported: M/(B/4) = AUC_REV/(B_prefix/4), and the per-seed D_FO, D_ISO, D_FO ∧ D_ISO, M and joint flags.

**Thin-margin rule (reporting only; A9).** A seed passing the joint rule is **thin for family F** if max_j AUC_F,j > eps0 and margin_F < 0.10·max_j AUC_F,j. Where the percentage is UNDEFINED, the margin is reported in absolute terms and relative to B and PD only.

**Aggregate thin-margin sentences: phase B only** (edit 10). Phase A keeps per-seed reporting only. For each family F, with counts filled in:

> "[t_F] of [n] joint-passing seeds exceed the most damaging sampled [first-order-matched | isotropic] path by less than 10% of that path's AUC ([u_F] seeds with this percentage undefined because that family's maximum AUC is ≤ eps0). At alpha = 1, at least one sampled [first-order-matched | isotropic] path causes strictly greater loss than reversion in [k_F]/10 seeds, and at least one ties it within eps0 in [k'_F]/10 seeds. The preregistered directional criterion concerns trapezoidal AUC over the dose grid; an endpoint-only directional comparison against this family would pass in [e_F]/10 seeds. These descriptive findings do not change the frozen labels."

If the label is REPLICATED and fewer than eight joint passes are non-thin for both families:

> "The REPLICATED label depends on at least one seed whose directional margin against at least one family is below 10% of that family's most damaging sampled path; robustness to additional draws is untested."

## 7. Labels and verdicts

**Phase B only (seeds 300–309). Precedence, per target:**
1. E1 not replicated → **"UNRESOLVED (E1 not replicated)"**.
2. Consult #17, edit 8, verbatim:

   > "After the E1 prerequisite, if more than two distinct seeds are invalid or have a collapsed control family for the target, report UNRESOLVED (insufficient evaluable seeds). Otherwise retain the denominator of ten."

   Other eligibility failures remain scientific non-passes.
3. **Count rule:** at least eight of the ten fixed seeds satisfy the **joint** rule (valid ∧ eligible ∧ D_FO ∧ D_ISO ∧ M), and the denominator stays ten. "Separate eight-seed successes against each family are insufficient."

**Labels (consult #17, edit 1, verbatim).**
- **Primary success:** **"GRADED JOINT REVERSION EXCEEDS BOTH FIRST-ORDER-MATCHED AND ISOTROPIC CONTROLS (PREFIX FUNCTION): REPLICATED"**.
- **Primary failure:** **"JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET"**.
- **UNRESOLVED:** "UNRESOLVED (E1 not replicated)" or "UNRESOLVED (insufficient evaluable seeds)".

There is no intermediate band.

**Secondary (r, z, n).**
- The same rule, precedence and labels, prefixed "Secondary (block-wise), [k]:", with the block letter always printed.
- They are correlated with the primary and with each other, cannot substitute for or upgrade it, and there is no "any k" upgrade.

**Counts, always reported:**
- D_FO n/10, D_ISO n/10, D_FO ∧ D_ISO n/10, M n/10 and joint n/10 seeds **passed**;
- invalid, collapsed and other eligibility failures, counted separately;
- NEGLIGIBLE FIRST-ORDER SCALE and fixed-block flags.

The wording is "below the declared materiality threshold", never "immaterial". Transfer is reported as a replication per recurrent-core FINAL §3.

**Phase A.**
- The only headline is "EXPLORATORY (PHASE A …; NOT CONFIRMATORY): per-seed curve results", given separately for 100–109 and 200–209.
- It gives per-seed flags, margins against both families and diagnostics.
- There is no aggregate verdict and there are no aggregate thin-margin sentences.

## 8. Claim assembly (fixed in advance)

**Primary REPLICATED. Success paragraph (consult #17, edit 3, verbatim; it replaces the draft's success paragraph and duplicated limitation):**

> "In W2, in at least eight of ten fresh GRU-8 seeds, continuation-stage joint recurrent reversion produced a trapezoidal excess prefix-function loss exceeding every one of 32 first-order-matched paths and every one of 32 isotropic paths. Both families matched the reversion displacement block by block in Frobenius norm; the first-order-matched family additionally matched its initial loss derivative. The excess met the declared materiality threshold, and the intact trained cores outperformed the prefix-blind reference. This supports a bounded causal contribution under the specified intervention and fixed surrounding computation. The comparison concerns the sampled families and dose-averaged AUC; it does not identify semantic content, curvature as a mechanism, localization, necessity, or selectivity over continuation processing."

**Then appended:**
- the §4.1 disclosure sentence;
- the transfer replication;
- the §6.1 margin sentences (phase B);
- the secondary block results (correlated);
- the first-order diagnostics, including the residual after subtracting the initial tangent contribution, which is not a curvature estimate;
- L_cont, XOR and E_total (descriptive);
- the phase A exploratory note;
- the S4 suffix if applicable.

**Single blocks (consult #16, verbatim, if no block meets the criterion):** "The primary effect was not reproduced by any single block at the declared criterion." Do not infer that single blocks carry no contribution, that the effect is distributed, or that any block explains the joint result.

**Primary not met (consult #17, edit 3, verbatim):**

> "The joint FO-and-ISO criterion was not met; no reduction was identified."

- Then report the counts (§7).
- **Do not automatically attribute that failure to FO matching: ISO could be the failed condition.** Report which conditions failed in each seed.
- PR #8's REPLICATED label is unaffected.
- Do not write "no causal effect", "generic damage", "explained by the gradient" or "not learned".

**UNRESOLVED:** "Graded joint reversion against first-order-matched and isotropic controls was UNRESOLVED ([E1 not replicated | insufficient evaluable seeds])."

**Never claimed:**
- semantic content, or that weight_hh or any block "stores" content;
- a unique or identified mechanism, or a gate-pathway mechanism;
- curvature, second-order structure or nonlinearity as a mechanism;
- localization, or independently manipulable state;
- monotonicity (including continuous monotonicity from sampled non-decreasing values);
- selectivity over continuation processing, or an XOR-specific effect;
- exceeding every first-order-matched or isotropic displacement (only the sampled 32 + 32 are tested);
- a calibrated significance claim, or robustness to more draws (O7);
- that either family is uniformly more stringent;
- necessity (Q-NECESSITY);
- other architectures or budgets;
- any phase A result as confirmation;
- any change to PR #5, #7 or #8 labels;
- C4, C5, consciousness or organism conclusions.

## 9. Integrity, determinism, reporting and freeze sequence

1. One process, deterministic algorithms, `set_num_threads(1)`, float64, exhaustive 256-history enumeration. The autograd pass uses the same float64 forward, with h_4 detached and other parameters frozen.
2. **Generator seeds:**
   - phase B training: s (init), 1000+s (episodes), 5000+s (readouts);
   - ISO: 40000+100·s;
   - FO base draws: 1,000,000+100·s;
   - gradient-check directions: 2,000,000+100·s.

   All ranges are disjoint.
3. **Tables:**
   - all seeds, at all doses, for REV and for all 32 FO and 32 ISO paths;
   - the primary target and r, z, n;
   - all §5 outcomes;
   - the §6 diagnostics and §6.1 margins for both families;
   - gradient-check gaps and matching and radius residuals;
   - degenerate-case flags with ρ, R_eff and ‖g‖·‖d‖;
   - sham, restore and endpoint gaps;
   - eligibility flags;
   - B_prefix and C_prefix, absolute and divided by PD;
   - invalid and collapsed counts;
   - checkpoint, gradient and transformed-path hashes.

   No seed is replaced, and missing cells are reported.
4. **Test suite (hashed with the code):**
   - all applicable PR #8 tests;
   - autograd G against central FD with the absolute-floor rule, on a synthetic and a real checkpoint;
   - tied-override gradient equals the sum of per-stage untied gradients;
   - h_4 is detached, and no gradient reaches other parameters;
   - base-draw two-process byte identity, with manifest sha;
   - every §12 tolerance on real deltas, with orthogonality checked against `gh_k`;
   - the radius gate (edit 7) on near-collinear synthetic cases;
   - synthetic cases, each with the §4.5 action and flag:
     - an **exactly zero gradient** (isotropic fallback, exact match);
     - a **tiny nonzero gradient** below G_ZERO (projection construction, NEGLIGIBLE FIRST-ORDER SCALE flag, checks pass);
     - a **collapsed block** (e_jk = d_k, norm and first-order match exact);
     - a **collapsed primary via R_eff**;
     - a **zero block**;
     - a **negative a_k**;
   - construction-failure handling;
   - FO_AUC = ⟨G,delta⟩/2 on a synthetic linear curve;
   - the D_FO, D_ISO, D, M and joint rules;
   - the thin-margin rule, including UNDEFINED denominators and the tie versus strict endpoint counts;
   - verdict precedence, including **two invalid plus two separately collapsed seeds → UNRESOLVED (insufficient evaluable seeds)**;
   - exact label and claim strings.
5. **Freeze sequence:**
   1. Hash the FINAL text, code, tests, tolerances, generator seeds and the base Gaussian draw manifests for both phases (S1).
   2. Phase A (exploratory, evaluation only, O9). Per seed, the gradient is computed, then the transformed FO paths are built and hashed, then the curves are evaluated.
   3. Any fixes under S4 or S5.
   4. Commit the approval record (§0.2).
   5. Phase B training (30 runs). Per seed: checkpoint hash, then gradient, then the transformed-path hash, then evaluation. Checkpoint, gradient and transformed-path hashes are recorded together.
   6. Results, with phase A in a separate development section.

## 10. Thirteen admission answers

1. **Q1. Question.** Q-CAUSE, organization level, bounded. Does graded joint reversion during updates 5–8 produce greater dose-averaged prefix-function loss than **both** the FO family (norm and initial derivative matched) and the ISO family (norm matched), in the same seeds? Q-LEARN enters only as the transfer prerequisite.
2. **Q2. Hypothesis and criterion.**
   - Per seed: D_FO ∧ D_ISO ∧ M, together with validity and eligibility.
   - At least eight of the ten fixed seeds must pass this joint rule, with the denominator of ten retained. Separate eight-seed successes against each family are insufficient.
3. **Q3. Falsifiers.**
   - "JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET";
   - UNRESOLVED (E1 not replicated; insufficient evaluable seeds), evaluated first.

   Phase A falsifies and confirms nothing.
4. **Q4. Simpler explanations.**
   - displacement size: both families are block-norm-matched;
   - initial loss slope: the FO family;
   - the original isotropic comparison: the ISO family, now decision-bearing;
   - a success on a potentially easier family: conjunctive gating;
   - endpoint-only effects: AUC, with endpoint comparisons descriptive;
   - post-hoc dose selection: excluded;
   - single blocks: secondary;
   - harness artifacts: SHAM, RESTORE, ENDPOINT, FD checks and PR #8 cross-checks;
   - total-loss confounds: the prefix-function outcome;
   - a prefix-blind-level intact core: C_prefix;
   - foreign-seed coordinate incompatibility: avoided (§1.1).

   **Limitations:**
   - the PR #8 readout and compatibility limitation (verbatim);
   - local derivative matching only;
   - higher-order structure is not matched;
   - only the sampled families are tested.
5. **Q5. Why now (consult #17, edit 2, verbatim):** "Existing-checkpoint feasibility checks do not support a dominant positive initial-gradient explanation of PR #8's sampled early-dose damage. This study asks whether reversion's dose-averaged advantage survives conditioning controls on its initial loss slope while also retaining the original isotropic comparison. Neither control family is assumed uniformly more stringent than the other."

   Context: PR #8 was REPLICATED 9/10 with thin margins (E-B3).
6. **Q6. On success.**
   - Record the §8 paragraph and disclosures.
   - The ledger records a bounded causal comparison strengthened against both sampled families (§11).
   - Consult #17: "A success would strengthen the bounded causal comparison; it would not establish Q-NECESSITY or advance the C-level."
7. **Q7. On failure.**
   - "The joint FO-and-ISO criterion was not met; no reduction was identified."
   - Do not attribute the failure to FO automatically.
   - PR #8 stands.
   - Any change to the families or thresholds is a new protocol on new seeds.
8. **Q8. Resources.**
   - **Phase A:** evaluation only. Per seed:
     - 1 autograd pass and 8 FD rollouts;
     - 6 doses × (1 + 32 + 32) paths × 4 targets = 1560 enumerations of 256 histories.

     That makes 20 seeds in all, minutes of CPU.
   - **Phase B:** 30 CPU training runs (PR #7 recipe), plus the same evaluation.
   - No organism model.
9. **Q9. Level.**
   - Organizational: the causal contribution of acquired recurrent parameters to the use of earlier evidence, compared with two sampled control families.
   - Engineering: training, the hook, autograd and enumeration.
   - No substrate claim.
10. **Q10. Ceiling.** The §8 paragraph and the "Never claimed" list. The claim is always qualified by the sampled families, local derivative matching and finite-dose AUC (O5).
11. **Q11. C-level.** C3-type history-integrating predictive state. Below C4: C4 needs an internal-evaluation role dissociated from first-order inference. C5 is untouched. No consciousness claim.
12. **Q12. Supplied, acquired and selected.**
    - **Supplied:**
      - the GRU cell and its initialization, the timing scaffold, the readout architecture, losses, the split, the dose grid and both control families;
      - the oracle, used for evaluation and (disclosed) for the gradient that defines the FO family. That gradient is an oracle-informed analysis control applied after training, and it does not train the network or modify its saved checkpoint.
    - **Acquired:** W_T and its contribution.
    - **Selected:** nothing.
13. **Q13. Ledger movement.**
    - **REPLICATED:** Q-CAUSE bounded support, now against both first-order-matched and isotropic sampled families (dose-averaged AUC).
    - **Not met:** "criterion not met; no reduction identified"; PR #8 is unchanged.
    - **UNRESOLVED:** no movement.
    - Q-NECESSITY stays NOT_ESTABLISHED and Q-EXIST is not addressed in every case. No C-level change.

## 11. Q-separation and ledger

| Item | ORIGIN | ROLE (if shown) | REDUCTION | Question |
| --- | --- | --- | --- | --- |
| Transfer of W_T (phase B) | ACQUIRED | predictive advantage surviving readout replacement | criterion not met; no reduction identified | Q-LEARN (prerequisite only) |
| Complete weight_hh, updates 5–8, vs FO **and** ISO families (joint rule) | ACQUIRED | dose-averaged prefix-function disruption exceeding both sampled families, ≥ B_prefix/4 | criterion not met; no reduction identified | Q-CAUSE, organization level (bounded) |
| Single blocks r, z, n (joint rule) | ACQUIRED | secondary, correlated | criterion not met; no reduction identified | Q-CAUSE (secondary) |
| Necessity of recurrent training | NOT TESTED | — | — | Q-NECESSITY |
| Existence of an exact solution | PR #4 / PR #5 K-EXACT erratum | — | — | Q-EXIST (not addressed) |

The PR #8 entry is unchanged: Q-CAUSE organization level SUPPORTED, BOUNDED, with the E-B4 qualifier and the consult #17 interpretation note.

## 12. Frozen numeric tolerances and values

| item | value | note |
| --- | --- | --- |
| eps0 | 1e-12 | inherited |
| IDENTITY_TOL | 1e-9 | inherited |
| NORM_REL_TOL | 1e-12 | \|‖e_jk‖ − ‖d_k‖\| ≤ 1e-12·‖d_k‖; also assembled |
| FO_REL_TOL | 1e-12 | \|⟨g_k,e_jk⟩ − ⟨g_k,d_k⟩\| ≤ 1e-12·‖g_k‖·‖d_k‖; also assembled against ‖G‖·‖delta‖ |
| ORTH_TOL | 1e-12 | \|⟨u_jk, gh_k⟩\| ≤ 1e-12; \|‖u_jk‖ − 1\| ≤ 1e-12 (uses `gh_k`, edit 4) |
| Radius gate | \|‖d_k‖² − ‖p_k‖² − r_k²\| ≤ 1e-12·‖d_k‖² | edit 7; r_k = ‖d_k − p_k‖ authoritative; the sqrt form is descriptive |
| FD check | \|FD − ⟨G,dir⟩\| ≤ 1e-10 + 1e-6·‖G‖ | edit 6; h = 1e-6; 4 directions |
| G_ZERO | 1e-10 (loss units) | **diagnostic only** (NEGLIGIBLE FIRST-ORDER SCALE); the isotropic fallback applies only when g_k = 0 exactly |
| RHO_COLLAPSE | 1e-3 | block ρ_k; primary R_eff/‖delta‖ |
| RHO_NEAR | 0.10 | descriptive |
| Projection failure | ‖y‖ ≤ 1e-12·‖z‖ | integrity failure (invalid) |
| THIN_REL | 0.10 | reporting only; UNDEFINED when the family max ≤ eps0 |
| Unevaluable-seed bound | more than 2 distinct seeds invalid or collapsed (per target) → UNRESOLVED (insufficient evaluable seeds) | edit 8 |
| Paths per family | 32 FO + 32 ISO | O7 |
| Gradient point | W_T, tied override, h_4 detached | O3, A1–A3 |
| PR #8 cross-check (phase A) | 1e-15 absolute on delta_rev; ISO draw sha equal to the PR #8 manifest | A8 |

## 13. Rulings applied (consult #17) and residual ambiguities

**O1:** option (a), conjunctive FO and ISO gating (§6, §7). The one-sided family and curvature matching were not added (§1.1). The PR #8 interpretation note is written separately and additively (`/workspace/review/pr8_errata_v3_interpretation_note.md`).

**O2–O10 (verbatim rulings):**
- **O2.** "Accept 1e-10, 1e-3 and 0.10 with repairs 5-8. Collapse is non-evaluability, not an engineering failure." Applied in §4.5 and §7.
- **O3.** "Accept: primary uniform-grid L_prefix, fresh readout, trained point, tied late-stage override. Explicitly detach h4 and freeze other parameters." Applied in §4.1.
- **O4.** "Accept block-only matching. Untouched blocks have zero displacement; no additional neutrality test is needed." Applied in §4.2.
- **O5.** "Amend as above. Always qualify the claim by sampled families, local derivative matching and finite-dose AUC." Applied in §1, §8 and §10 Q10.
- **O6.** "Allow per-seed exploratory reporting. The correction to the earlier explanatory hypothesis should nevertheless be recorded additively, as specified above." Applied in §2 S9 and the errata v3 note.
- **O7.** "Keep 32 paths per family. No calibrated significance claim or robustness-to-more-draws claim." Applied in §8 and §12.
- **O8.** "Keep `AUC - FO_AUC`, named "residual after subtracting the initial tangent contribution." It is not a curvature estimate." Applied in §6.
- **O9.** "Yes: evaluation-only Phase A may proceed under the described standing authorization after these edits and hashing. No training is authorized by this ruling." Applied in the header and §2.
- **O10.** "Accept with the revised study name: "Approve fresh-seed GRU-8 training (seeds 300-309, 30 runs, PR #7 recipe) for graded reversion confirmation against both first-order-matched and isotropic controls once Astra clears the protocol?"" Applied in §0.2.

**A1–A10:**
- **A1–A3:** "accept, with explicit h4 detachment" (§4.1).
- **A4:** "amend the radius validation as in edit 7" (§4.2).
- **A5:** "accept; use `gh_k` consistently" (§4.2, §12).
- **A6:** "amend as in edits 5, 6 and 8" (§4.5, §7).
- **A7–A8:** "accept".
- **A9:** "accept as reporting only, with edit 10" (§6.1).
- **A10:** "confirmed subject to O9".

**Residual ambiguities, resolved by following Astra and listed:**
- **R1. Approval wording versus O10.** The widget t23s2 question was answered at 1:05 AM ET. It omits "PR #7 recipe" and names "the first-order-matched control confirmation", not Astra's revised name. The Specialist treats the approval as covering the revised design (§0.2): it is strictly more demanding, with the same 30 runs, seeds and arms, and the PR #7 recipe was already fixed by the protocol. This is recorded, not reinterpreted. **If Aidan or Astra disagree, the O10 wording should be re-asked before phase B training.**
- **R2. "Phase B training still requires Aidan's separate approval" (consult #17).** Satisfied by the §0.2 record: the approval is conditional on Astra clearance, and consult #17 is that clearance. The relative timing of the 1:05 AM answer and the consult #17 text does not matter, because the condition is clearance before training.
- **R3. Collapsed block and the secondary rule.** Edit 5 says the secondary comparison is "ineligible". Edit 8 counts collapse jointly with invalid seeds. Both apply: per target, a collapsed seed is an ineligible non-pass **and** counts toward the "more than two distinct seeds" UNRESOLVED bound.
- **R4. Exactly zero gradient.** This means every entry is 0.0 in float64. Any nonzero entry triggers the projection construction (edit 6).
- **R5. Joint 8/10 with secondaries.** Edit 1, "Apply the same rule to secondary blocks", is read as the same joint FO ∧ ISO ∧ M rule and the same unevaluable-seed bound, per block.
- **R6. Thin margin with two families.** "Thin" is evaluated per family. The robustness sentence triggers if fewer than eight joint passes are non-thin for **both** families. This is my reading of "report margins against both families".
- **R7. Endpoint ties.** A tie is \|Δ\| ≤ eps0. Strictly greater means the difference exceeds eps0 (edit 10, "distinguish endpoint ties from strictly greater control losses").
- **R8. Phase A ISO.** D_ISO in phase A recomputes the PR #8 comparison on seeds 100–109 and 200–209, with byte-identical draws. It is exploratory, and PR #8's labels are unaffected.

---

## Appendix A. (none)

There is no tuned-rival grid and no optional training block. PR #8 Appendix A remains unapproved.

## Appendix B. Feasibility checks already run (scratch; read-only; no training; no control paths)

These are unchanged from draft v1.
- **Location:** `/workspace/scratch/fo_control/`.
- **Files:**
  - `PREREG_THRESHOLDS_BEFORE_CHECK.txt` (`2abb0332…`, 00:58:49 ET);
  - `feasibility.py` (`29124772…`);
  - `feasibility.json` (`179e0342…`, 00:59:22 ET);
  - `feasibility.log` (`1cef2941…`);
  - `feasibility_summary.txt` (`272f5adc…`).
- **Method:** a NumPy GRU-8 forward pass; gradient by central finite differences (h = 1e-6) on all 192 entries of the tied override at W_T. This is a stand-in. **Confirmation of the derivative calculations by the new autograd implementation is required** (consult #17, O1; §4.1).

**Harness reproduction.**
- Intact L_prefix matches the committed PR #8 values within 6.5e-19.
- Delta_REV(1/8) matches within 1.7e-18 and Delta_REV(1) within 3.5e-18.
- The sham gap is 0.
- PD(q_star) = 0.0138386222.

**Gradient geometry.**

| quantity | 100–109 | 200–209 |
| --- | --- | --- |
| cos(G, delta) | −0.340 … +0.075 (8/10 negative) | −0.397 … +0.129 (7/10 negative) |
| ⟨G,delta⟩ | −2.31e-3 … +4.2e-4 | −2.20e-3 … +6.8e-4 |
| FO_AUC / AUC_REV (committed) | −0.28 … +0.04 | −0.24 … +0.09 |
| ⟨G,delta⟩/8 ÷ Delta_REV(1/8) | −1.39 … +0.11 | −0.83 … +0.23 |
| min block ρ_k | 0.823 | 0.813 |
| assembled R/‖delta‖ (= R_eff; no collapsed blocks) | 0.879 … 1.000 | 0.850 … 0.995 |
| min block ‖g_k‖·‖d_k‖ | 2.2e-4 | 3.2e-4 |

No degenerate case is triggered, and NEGLIGIBLE FIRST-ORDER SCALE is not triggered. No control path, control AUC, D or M flag was computed.
