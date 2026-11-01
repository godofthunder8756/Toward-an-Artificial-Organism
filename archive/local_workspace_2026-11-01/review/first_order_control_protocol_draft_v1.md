# Graded recurrent reversion against first-order-matched controls: protocol (DRAFT v1)

> **DRAFT FOR ASTRA CONSULT #17. NOT FROZEN. NOT RUN.**
> - Nothing is frozen, committed or pushed. No rollout along any control path, no control loss and no D/M flag exists for any seed.
> - The only computations are the read-only feasibility checks in Appendix B. They covered harness reproduction of committed PR #8 values and gradient geometry at W_T. No control path was built or evaluated.
>
> **Authorization.**
> - **Phase A (EXPLORATORY).** Evaluation only, no training. It uses the existing checkpoints of seeds 100–109 (PR #7) and 200–209 (PR #8). It is *proposed* to be covered by standing authorization after Astra #17 clearance and hashing, the same ruling consult #15 gave PR #8 phase A. Astra to confirm (O9).
> - **Phase B (CONFIRMATION).** Fresh GRU-8 seeds 300–309: 3 runs × 10 seeds = **30 training runs** (CAND, F-TRAINED, F-INIT). **Aidan's explicit training approval is PENDING.** The Specialist is requesting it. No phase B training may occur until (i) Astra has cleared the frozen text, and (ii) Aidan's approval is recorded with date, time (ET), source and exact words.
> - The PR #8 approval (10:38 PM ET, 2026-10-20, widget t20s2) **does not carry over**. It applied to PR #8 phase B only (consult #16, E-B7).
>
> **This is a new study, not a reinterpretation of PR #8.** PR #8's labels stand: REPLICATED 9/10, confirmed by consult #16, with additive errata E-B3 to E-B7.

**Sources.**

| source | path | sha256 |
| --- | --- | --- |
| Spec: second section ("Request for Research Delegate") | `/workspace/review/pr8_errata_v2_request_consult16.md` | `92958927…7ffcf341c` |
| Astra consult #16 | `/workspace/astra_consult16_response.txt` | `91ccdbf7…ae4b60c555ef5b050f0e0de427351d82ad119` |
| Graded reversion FINAL (PR #8), the inherited design | `/workspace/review/graded_reversion_protocol_FINAL.md` | `1a5e62bd…89bfa3` |
| PR #8 results review | `/workspace/review/graded_reversion_results_review_v1.md` | — |
| Recurrent-core FINAL (PR #7), recipe and E1/transfer rules | `/workspace/review/recurrent_core_transfer_protocol_FINAL.md` | `63c463c7…e9506` |
| PR #8 implementation (read-only scratch clone) | `/workspace/scratch/pr8/clone`: `graded_reversion_*.py`, freeze `018f2a7`, results `7008026` | — |

**Scope guards.**
- GRU-8 only, in the same W2 world, with the same fresh-readout intervention, dose grid, L_prefix and block norms as PR #8.
- No new architecture family, no protected controller or register, and no organism work.
- No localization: no decoder, no subspace search, no E3/P1/P2.
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
- the **REV path** W(α) = W_T + α·(W_0 − W_T), α ∈ 𝒜 = {0, 1/8, 1/4, 1/2, 3/4, 1}, applied at updates 5–8 only (`stage_idx` 4–7) through `MatrixOverride`. The primary target is the complete `weight_hh_l0` (24×8). The secondary targets are the 8×8 blocks r (rows 0–7), z (8–15) and n (16–23);
- the **α = 1 endpoint sentence**, readout and compatibility limitation, AUC interpolant disclaimer, saturation rule and displacement/zero-block rule, all verbatim from graded reversion FINAL §§3–6;
- the **L_prefix ASCII definition** (FINAL §5; no division by three; uniform complete 16×16 grid primary) and PD(q_star) = 0.0138386;
- **B_prefix**, **C_prefix**, eligibility conditions 1–5, the trapezoid weights (1/16, 1/8, 3/16, 1/4, 1/4, 1/8), and the integrity checks SHAM, RESTORE, ENDPOINT, checkpoint sha and outputs.

**What changes:** the control family that gates D (§4), plus the added first-order diagnostics, the degenerate-case rules, the margin reporting and the claim strings.

## 0.1 Spec items and where they are applied

| # | Spec / consult #16 item | Where |
| --- | --- | --- |
| 1 | Same GRU-8, fresh-readout intervention, dose grid, L_prefix and block norms | §0 |
| 2 | g_k = gradient of L_prefix with respect to a late-stage (updates 5–8) block override, holding the intact stage-4 state fixed | §4.1 |
| 3 | d_k = vec(W0_k − WT_k); a_k = dot(g_k,d_k)/dot(g_k,g_k); e_k = a_k·g_k + sqrt(‖d_k‖² − a_k²‖g_k‖²)·u_k, with u_k a random unit vector orthogonal to g_k | §4.2 |
| 4 | 32 prespecified assembled paths, reused across doses | §4.2–4.3 |
| 5 | Isotropic controls retained descriptively | §4.4 |
| 6 | Frozen tolerances; handling of zero gradients and collapsed residual spheres ("a collapsed control family cannot provide a meaningful specificity comparison") | §4.5, §12 |
| 7 | Original AUC directional and B/4 materiality rules; report the actual margins | §6, §6.1 |
| 8 | Gradient matching disclosed as an analysis control, not training | §4.1, §10 Q12 |
| 9 | Phase A exploratory pilot on existing checkpoints (no training); phase B seeds 300–309, 30 runs, Aidan's approval | §2 |
| 10 | Claim ceiling: effect beyond matched local first-order sensitivity and displacement size; not semantic content or unique mechanism | §8 |
| 11 | Preferred over foreign-seed weight_hh (coordinate incompatibility) | §1.1 |
| 12 | Draft goes to Astra (consult #17) before freezing | header, §13 |

---

## 1. Question and design

**Question (Q-CAUSE, organization level, bounded).** The intervention interpolates the complete hidden-to-hidden matrix toward initialization during updates 5–8, with trained input weights, biases and the fresh readout held fixed. Does it produce greater dose-averaged excess prefix-function loss than perturbation paths matched to it **block by block in Frobenius norm and in first-order predicted change of L_prefix at the trained weights**?

PR #8 showed REV beating 32 block-norm-matched isotropic paths in 9/10 seeds. Consult #16 named the open alternative: REV might owe its advantage to "a larger positive gradient projection than typical isotropic directions" (consult #16 §3). The matched family removes that alternative by construction. Any surviving difference arises from second- and higher-order structure of the loss along the learned displacement.

**"Beyond first-order-matched perturbation"** means dose-averaged trapezoidal AUC over the specified path (consult #16 E-B5). It does not mean every dose, the endpoint, or arbitrary perturbations.

**Not:**
- a localization study;
- a "stores content" or semantic-content test;
- a necessity test;
- an XOR-specific test;
- a monotonicity test;
- a selectivity-over-continuation test;
- a test of a uniquely identified mechanism.

## 1.1 Control family rejected: foreign-seed weight_hh (recorded)

Interpolating toward another seed's trained `weight_hh` was considered (PR #8 review §7, item 2) and **rejected by Astra** (consult #16 §4, verbatim):

> "Foreign-seed trained matrices are weaker controls for this question: hidden-unit coordinates differ across seeds, so transplanting one matrix can create coordinate incompatibility. Such substitutions also do not automatically match first-order loss effects."

Hidden-unit permutation and alignment are not attempted. Alignment would require fitting a correspondence, which is a selection step outside this design. No foreign-seed condition appears in this protocol.

## 2. Phases, seed ranges and safeguards

| phase | seeds | weights | training | status |
| --- | --- | --- | --- | --- |
| **A: EXPLORATORY** | **100–109** (PR #7) and **200–209** (PR #8) | PR #7 `recurrent_core_results_v1/checkpoints/s{s}_{f_trained,f_init,cand_init}.ckpt` at `5157f5d`; PR #8 `graded_reversion_results_v1/checkpoints/` at `7008026`; all sha256-verified | none | development only; **never confirmatory**; per-seed only; the two groups are reported separately and never pooled |
| **B: CONFIRMATION** | **300–309** (fresh; disjoint from 0–9, 100–109 and 200–209) | newly trained CAND → W_T, F-TRAINED, F-INIT | **30 runs** (3 × 10), PR #7 recipe unchanged | the only phase that can earn a §7 label. **Needs Astra clearance and Aidan's explicit approval (PENDING)** |

**Safeguards.** PR #8 S1–S9 are inherited with these substitutions:
- **S1. Freeze before phase A.** The FINAL text, the code, the test suite and the draw manifests are hashed before any phase A output exists. These cover the FO draws, the isotropic draws and the gradient-check directions.
- **S2. Label namespace.**
  - Phase A outputs are prefixed **"EXPLORATORY (PHASE A, PR #7 SEEDS 100–109 / PR #8 SEEDS 200–209; DEVELOPMENT ONLY; NOT CONFIRMATORY)"**.
  - Phase A never uses REPLICATED, DEMONSTRATED, SHOWN or CONFIRMED, and gives no out-of-ten verdict line.
- **S3. No carry-over.** Phase A outputs cannot change any scientific parameter. These include:
  - the dose grid, the number of paths and the generator seeds;
  - the gradient point and definition, the matching rule and all §12 tolerances and thresholds;
  - the outcome, statistic, eligibility, materiality and replication rule;
  - the thin-margin cutoff.
- **S4.** A scientific change after phase A is a new version, reviewed by Astra and hashed before phase B training. Its labels carry **"(CRITERION REVISED AFTER EXPLORATORY PHASE A)"**.
- **S5.** Engineering fixes are versioned and hashed before phase B and logged in `DEVIATIONS_AND_AMBIGUITIES`. Superseded phase A outputs are retained and labelled with their code version.
- **S6. Pre-exposure (strengthened).** Neither phase A group is naive:
  - Seeds 200–209 were PR #8's confirmatory seeds. Their REV curves, isotropic curves and margins are public (consult #16 E-B3).
  - Seeds 100–109 have public PR #7 and PR #8 phase A results.
  - Gradient geometry at W_T for all 20 seeds was computed for this draft (Appendix B).
  - Phase A on 200–209 **cannot alter, strengthen or weaken PR #8's labels**.
- **S7. Seed accounting.** Phase B uses exactly 300–309, with no replacement or addition. Missing cells are reported.
- **S8. Artifacts.**
  - Phase A outputs go to `first_order_control_phaseA_exploratory/`.
  - Phase B outputs go to `first_order_control_results_v1/`. They cite phase A only in a separately headed "Development history" section.
  - Existing PR #7 and PR #8 files are never edited.
- **S9. Phase A reporting.** Per-seed D/M flags, margins, first-order diagnostics and endpoint errors, explicitly exploratory. No pooling, no aggregate verdict, no use as confirmation.

## 3. Intervention path (REV): unchanged

As in graded reversion FINAL §3, with the endpoint identity check ‖W(1) − W_0‖_max ≤ eps0 and W(0) = W_T exactly. REV is recomputed in this study.

**Phase A cross-check:** recomputed REV curves must equal PR #8's committed `delta_rev` values within 1e-15 absolute. A mismatch is an engineering flag and makes the seed invalid in phase A. Appendix B found a maximum gap of 3.5e-18.

## 4. Controls

### 4.1 Gradient (analysis control; oracle-informed; not training)

- **Override parametrization.** A single 24×8 float64 leaf tensor V, applied as `weight_hh_l0` at updates 5–8 only (stage_idx 4–7). It is *tied* across the four stages, matching how W(α) is applied. Updates 1–4 use the intact trained W_T, so the stage-4 state h_4 is the intact state. "Holding the intact stage-4 state fixed" is therefore automatic, and no gradient flows into updates 1–4 or into any other parameter.
- **Evaluation point.** V = W_T, with the F-TRAINED fresh readout, trained W_ih, b_ih and b_hh, and the complete uniform 256-history grid.
- **Gradient.** G = ∂L_prefix/∂V at V = W_T. It is computed by torch autograd in float64, in a non-inference-mode rollout that is functionally identical to the evaluation rollout. G sums over the four tied stages. The block gradient g_k is the corresponding 8×8 block of G, vectorized in row-major order. d_k is vectorized the same way.
- **The loss is the primary L_prefix only**, not L_cont, E_total or any TEST-restricted variant.
- **Disclosure (verbatim for results):** "The first-order matching uses the gradient of the oracle-referenced prefix-function loss at the trained weights. It is an oracle-informed analysis control, applied after training; it is not network training and does not alter any network."
- **Gradient checks (validity).** Central finite differences of L_prefix with step h = 1e-6 (Frobenius units) along four unit directions in V-space:
  - the unit displacement d/‖d‖;
  - three random unit directions from `torch.Generator` seed **2,000,000 + 100·s**.

  Each must satisfy |FD − ⟨G, dir⟩| ≤ GRAD_CHECK_TOL·‖G‖_F, with GRAD_CHECK_TOL = 1e-6. Two independent gradient computations must also be byte-identical. A failure, or a non-finite G, makes the seed **invalid**.

### 4.2 Matched-path construction (per block k ∈ {r, z, n}, per path j = 1…32)

- **Generator:** `torch.Generator`, seed **1,000,000 + 100·s**. Draws j = 1…32 in order, each one `torch.randn((24, 8), dtype=torch.float64, generator=...)` call giving Z_j. z_jk is block k of Z_j, vectorized.
- **Definitions** (ĝ_k = g_k/‖g_k‖):

```text
d_k   = vec(W0_k - WT_k)
g_k   = vec(block k of G)
a_k   = dot(g_k, d_k) / dot(g_k, g_k)
p_k   = a_k * g_k                         # gradient component of d_k
r_k   = norm(d_k - p_k)                   # residual radius (stable form)
# consult #16 form, checked equal within tolerance:
#   r_k = sqrt(norm(d_k)^2 - a_k^2 * norm(g_k)^2)
y_jk  = z_jk - dot(z_jk, gh_k) * gh_k
y_jk  = y_jk - dot(y_jk, gh_k) * gh_k     # second Gram-Schmidt pass
u_jk  = y_jk / norm(y_jk)
e_jk  = p_k + r_k * u_jk
```

- **Assembled path:** E_j = [e_jr; e_jz; e_jn], reshaped to 24×8.
  - Primary path: W_FO,j(α) = W_T + α·E_j.
  - Secondary block k: W_hk^T + α·e_jk, using the same draw's block (O8 inheritance; correlated).
- **Matched properties.** For every j and k:
  - ‖e_jk‖ = ‖d_k‖;
  - ⟨g_k, e_jk⟩ = ⟨g_k, d_k⟩.

  Hence ‖E_j‖_F = ‖delta‖_F and ⟨G, E_j⟩ = ⟨G, delta⟩ for the assembled matrix.

  The family for block k is the (62-dimensional) sphere {e : ‖e‖ = ‖d_k‖, ⟨g_k,e⟩ = ⟨g_k,d_k⟩}. **d_k itself lies on this sphere.** "Beat all 32" therefore asks whether the learned displacement is extreme, in dose-averaged loss, among displacements with the same norm and the same tangent loss slope.
- **Scope of matching.** The match holds at the tangent, at W_T only. At finite α the paths differ through second- and higher-order terms. That difference is the object of the test, not a defect.
- **Two-sided match (disclosed).** The match is two-sided. When ⟨g_k,d_k⟩ < 0, matched controls are tilted toward local loss decrease relative to isotropic controls. Appendix B found this in 15/20 existing seeds. **Matched controls are therefore not uniformly more stringent than PR #8's isotropic controls** (§4.4, O1).

### 4.3 Reuse

The 32 E_j are drawn once per seed and reused at every dose and across the primary and secondary targets. No redraw, rejection or reordering is allowed except under §4.5.

### 4.4 Isotropic controls (descriptive; retained per spec)

- The PR #8 family is unchanged: generator 40000 + 100·s, 32 draws, per-block rescaling to ‖d_k‖_F, and the PR #8 zero-block rule.
- **Phase A:** the draws are byte-identical to PR #8's. Their sha256 must match the PR #8 freeze manifest. A mismatch is an engineering flag and makes the seed invalid in phase A.
- **Phase B:** seeds 300–309 give generator seeds 70000–70900.
- **Descriptive outputs** (never gating):
  - D_ISO = AUC_REV − max_j AUC_iso,j and its flag;
  - per-dose ranks;
  - ⟨G, eps_j⟩ for every isotropic path, which shows where REV's first-order term sits within the isotropic distribution.
- **Mandatory disclosure.** If the primary FO label is REPLICATED while fewer than 8/10 phase B seeds satisfy D_ISO, the results must state:

  > "The first-order-matched criterion was met, but the dose-averaged directional comparison against the block-norm-matched isotropic paths held in only [n]/10 of these seeds. Because the first-order match is two-sided, the first-order-matched family is not uniformly more stringent than the isotropic family."

  Whether to gate conjunctively instead is open question O1.

### 4.5 Degenerate cases (frozen)

All thresholds below were written down before any gradient was computed (scratch `PREREG_THRESHOLDS_BEFORE_CHECK.txt`, 00:58:49 ET, before the 00:59:22 ET feasibility output). None is triggered on any of the 20 existing seeds (Appendix B).

| case | test (per block k unless stated) | action | status |
| --- | --- | --- | --- |
| **Zero block displacement** | ‖d_k‖_F ≤ eps0 | e_jk = 0 (PR #8 rule); a_k and r_k are not computed | primary eligibility needs ‖delta‖_F > eps0; secondary k ineligible (non-pass) |
| **Zero or near-zero gradient** | ‖g_k‖_F·‖d_k‖_F ≤ G_ZERO = 1e-10 (loss units: the largest first-order change any equal-norm block displacement could produce) | set a_k := 0 and e_jk := ‖d_k‖·z_jk/‖z_jk‖ (isotropic within the block; same draw) | valid and eligible; flag "FIRST-ORDER TERM NUMERICALLY ZERO (block k)". If all three blocks are flagged, the primary seed is flagged "FIRST-ORDER MATCH VACUOUS"; it remains eligible, and the flag is reported with the label |
| **Collapsed residual sphere, block** | ρ_k = r_k/‖d_k‖ ≤ RHO_COLLAPSE = 1e-3 (equivalently \|cos(g_k,d_k)\| ≥ 0.9999995) | set e_jk := p_k for all j; the block contributes no spread | secondary k: **ineligible, non-pass, "COLLAPSED CONTROL FAMILY"**; primary: see the next row |
| **Collapsed control family, primary** | R/‖delta‖_F ≤ RHO_COLLAPSE, where R = sqrt(Σ_k r_k²) is the assembled residual radius. Then every E_j lies within ~2·10⁻³·‖delta‖ of delta | as above | primary: **ineligible, non-pass, "COLLAPSED CONTROL FAMILY"**. If **more than two** phase B seeds are primary-collapsed: label **"UNRESOLVED (degenerate control family)"** (§7) |
| **Near-collapse (descriptive)** | ρ_k ≤ RHO_NEAR = 0.10, or R/‖delta‖ ≤ 0.10 | none | flag reported with ρ; no label effect |
| **Negative or zero a_k** | a_k ≤ 0 | none: the formula applies unchanged | ordinary; sign of ⟨g_k,d_k⟩ reported |
| **Projection failure** | ‖y_jk‖ ≤ 1e-12·‖z_jk‖, or ‖z_jk‖ = 0 | no redraw | engineering error: seed **invalid** (probability zero; mirrors PR #8 `ZeroDrawError`) |
| **Radicand cancellation** | ‖d_k‖² − a_k²‖g_k‖² < 0 numerically | use the stable form r_k = ‖d_k − p_k‖; the two forms must agree within 1e-12·‖d_k‖, or within 1e-12·‖d_k‖ absolute when ρ_k ≤ RHO_COLLAPSE | a disagreement above tolerance makes the seed invalid |
| **Matching tolerance failure** | any test in §12 | none | seed **invalid** |

**Rationale.**
- **Why non-pass rather than invalid.** A collapsed family is not a harness failure. The comparison simply cannot be informative: all controls coincide with REV up to O(ρ), so D cannot meaningfully pass. Consult #16: "a collapsed control family cannot provide a meaningful specificity comparison." This mirrors PR #8's treatment of eligibility.
- **Why UNRESOLVED above two seeds.** The same bound as the invalid-seed rule. The study could not test its question in enough seeds, and "CRITERION NOT MET" would misdescribe that.
- **Why zero gradient keeps eligibility.** With g_k ≈ 0 every equal-norm displacement has the same first-order effect, about 0, so the isotropic block draw is first-order-matched to within G_ZERO.

### 4.6 Integrity checks (no evidential role)

The PR #8 checks are inherited: SHAM, RESTORE, ENDPOINT, checkpoint sha, and outputs finite and in (0, 1) at every dose and direction, for both control families. Added:
- the gradient checks (§4.1);
- the matching tolerances (§12);
- the FO draw sha256 recorded in the freeze manifest before phase A, regenerated byte-identically in two separate processes;
- the phase A REV and isotropic cross-checks against PR #8 (§3, §4.4).

Any failure makes the seed **invalid**.

## 5. Outcomes: unchanged

- **Primary:** L_prefix exactly as in graded reversion FINAL §5.
- **Descriptive:** L_cont, per-component terms, TEST/TRAIN excesses, PD/CD, and the probability-weighted and TEST-restricted versions. XOR is explicit but descriptive.
- Vector success does not establish an XOR-specific effect.

## 6. Curve statistic and per-seed criterion

**Curves.** For c ∈ {REV, FO_j, ISO_j}:
- Delta_c(α) = L_prefix(c, α) − L_prefix(F-TRAINED intact);
- AUC_c = Σ_α w_α·Delta_c(α), with the PR #8 weights.

The PR #8 AUC disclaimer applies verbatim. Negative excesses are retained.

**Eligibility.** A failure is a **non-pass, not invalid**:
1. valid;
2. transfer pass;
3. B_prefix > eps0;
4. C_prefix > eps0;
5. displacement > eps0 (primary ‖delta‖_F; secondary ‖delta_k‖_F);
6. **non-collapsed control family** (§4.5).

**Per-seed GRADED-FO-SPECIFIC(target).**
- **(D) Directional (PR #8 rule with the control family substituted):** "D passes iff AUC_REV − max_j AUC_FO,j > eps0."
- **(M) Materiality (unchanged):** AUC_REV > eps0 **and** AUC_REV ≥ B_prefix/4, with no PD-relative floor. For a linear curve, M requires an endpoint d ≥ B_prefix/2.

  M does not depend on the control family. It is the same quantity as in PR #8, recomputed on the new seeds.
- **Joint:** valid ∧ eligible ∧ D ∧ M.

**First-order diagnostics** (descriptive, per seed and per target; never gating):
- ⟨G, delta⟩, cos(G, delta), and per block a_k, ⟨g_k,d_k⟩, cos(g_k,d_k), ρ_k and R/‖delta‖.
- The first-order AUC prediction **FO_AUC = ⟨G, delta⟩/2**. Since Σ_α w_α·α = 1/2, this is the AUC of the tangent line, and every FO path shares it.
- AUC_REV − FO_AUC and AUC_FO,j − FO_AUC, the higher-order part. D compares only these.
- Delta_REV(1/8) against ⟨G,delta⟩/8.
- The PR #8 saturation index, monotonic-step count and per-dose ranks.

### 6.1 Margin reporting (mandatory, every seed and target, both phases)

| column | definition |
| --- | --- |
| margin_FO | AUC_REV − max_j AUC_FO,j |
| m/B | margin_FO / B_prefix |
| m/PD | margin_FO / PD(q_star) |
| m/maxC | margin_FO / max_j AUC_FO,j. **UNDEFINED** if max_j AUC_FO,j ≤ eps0; signed otherwise |
| rank | rank of REV among 33 by AUC (1 = most damaging; ties count against REV) |
| per-dose rank | REV's rank among 33 at α = 1/8, 1/4, 1/2, 3/4, 1 |
| n_end | number of FO paths with Delta_FO,j(1) ≥ Delta_REV(1) |
| endpoint-D | Delta_REV(1) − max_j Delta_FO,j(1) > eps0 (descriptive only) |
| M/(B/4) | AUC_REV / (B_prefix/4) |
| median, max FO AUC | together with all 32 values |
| margin_ISO, m/maxC_ISO, rank_ISO | the same for the isotropic family (descriptive) |

**Thin-margin rule (frozen).** A passing seed is **thin** if margin_FO < THIN_REL·|max_j AUC_FO,j|, with THIN_REL = 0.10. This is the cutoff consult #16 used for E-B3. The results must include the following sentences, with counts filled in:

> "[t] of [n] passing seeds exceed the most damaging sampled first-order-matched path by less than 10% of that path's AUC. At alpha = 1, at least one sampled first-order-matched path causes greater loss than reversion in [k]/10 seeds. The preregistered directional criterion concerns trapezoidal AUC over the dose grid; an endpoint-only directional comparison would pass in [e]/10 seeds. These descriptive findings do not change the frozen labels."

If the label is REPLICATED and n − t < 8, the results must also state:

> "The REPLICATED label depends on at least one seed whose directional margin is below 10% of the most damaging sampled first-order-matched path; robustness to additional draws is untested."

Here n is the number of joint passes and t the number of thin passes.

## 7. Labels and verdicts

**Phase B only (seeds 300–309). Precedence:**
1. E1 not replicated → **"UNRESOLVED (E1 not replicated)"**.
2. More than two invalid seeds → **"UNRESOLVED"**.
3. More than two seeds with a primary collapsed control family → **"UNRESOLVED (degenerate control family)"**. This applies to the primary target only. A secondary target uses the same rule with its own collapse flags.
4. The count rule (PR #8, verbatim): "At least eight of the ten prespecified phase-B seeds jointly satisfy validity, eligibility, D and M. The denominator remains ten; seeds are not removed from it."

**Labels.**
- **Primary:**
  - **"GRADED JOINT RECURRENT REVERSION EXCEEDS FIRST-ORDER-MATCHED PERTURBATION (PREFIX FUNCTION): REPLICATED"**;
  - otherwise **"FIRST-ORDER-MATCHED GRADED REVERSION CRITERION NOT MET"**.

  There is no intermediate band.
- **Secondary (r, z, n):** "Secondary (block-wise), [k]: …", with the block letter always printed (E-B2 lesson). They are correlated with the primary and with each other, cannot substitute for or upgrade it, and there is no "any k" upgrade.
- **Transfer:** reported as a replication, per recurrent-core FINAL §3.
- **Isotropic comparison:** "Descriptive: dose-averaged directional comparison against block-norm-matched isotropic paths held in [n]/10 seeds." This is not a label and never "REPLICATED".
- **Counts** are printed as "n/10 seeds **passed**" with D/M/joint/eligibility counts. Collapse and zero-gradient flags are printed separately. The wording is "below the declared materiality threshold", never "immaterial".

**Phase A.** The only headline is "EXPLORATORY (PHASE A …; NOT CONFIRMATORY): per-seed curve results", given separately for 100–109 and 200–209. Each group gets per-seed flags, margins and diagnostics, with no aggregate verdict.

## 8. Claim assembly (fixed in advance; proposed verbatim; Astra to fix at #17)

**Claim ceiling (spec, verbatim):** "effect beyond matched local first-order sensitivity and displacement size; not semantic content or unique mechanism."

**Primary REPLICATED. Success paragraph (proposed):**

> "In W2, interpolation of the complete hidden-to-hidden matrix toward its initialization during updates 5–8, with trained input weights, biases and a fresh readout held fixed, increased oracle-referenced prefix-function loss over the predeclared dose grid. In at least eight of ten fresh seeds, the trapezoidal excess exceeded that of every one of 32 prespecified paths matched to the reversion displacement, block by block, in Frobenius norm and in first-order predicted change of prefix-function loss at the trained weights, and reached at least one quarter of the paired prefix-loss advantage over F-INIT. The intact trained cores also outperformed the prefix-blind reference."

**Limitation (proposed; the second sentence is consult #16 verbatim):**

> "This supports a bounded causal contribution of the trained hidden-to-hidden parameters to accurate prefix-dependent prediction that goes beyond matched local first-order sensitivity and displacement size, under the specified continuation-stage intervention and fixed surrounding computation. Its success would support an effect beyond matched local first-order sensitivity and displacement size; it would still not identify semantic content or a unique mechanism. The comparison concerns dose-averaged trapezoidal AUC over the specified path, not every dose, the endpoint, or arbitrary perturbations. The first-order matching is an oracle-informed analysis control, not network training. It does not establish monotonicity, selectivity over continuation processing, an XOR-specific effect, localized content, necessity, or a uniquely identified mechanism."

**Then appended:**
- the transfer replication;
- the isotropic descriptive line and, if triggered, the §4.4 disclosure;
- the §6.1 margin sentences;
- the secondary block results (correlated);
- the first-order diagnostics;
- L_cont, XOR and E_total (descriptive);
- the phase A exploratory note;
- the S4 suffix if applicable.

**Single blocks (consult #16, verbatim, if no block meets the criterion):** "The primary effect was not reproduced by any single block at the declared criterion." Do not infer that single blocks carry no contribution, that the effect is distributed, or that any block explains the joint result.

**Primary not met:**

> "Graded joint recurrent reversion did not meet the prespecified first-order-matched curve-level criterion for prefix-function loss ([n]/10 seeds passed; directional [d]/10, materiality [m]/10; eligibility failures [e]/10, of which collapsed control family [c]/10)."

- Basic intervention dependence is reported as measured.
- **PR #8's REPLICATED label is unaffected.** A failure here means the dose-averaged advantage over isotropic paths was not shown to survive first-order matching. It does not show that the advantage was first-order.
- Do **not** write "no causal effect", "generic damage", "explained by the gradient" or "not learned".

**UNRESOLVED:** "Graded joint recurrent reversion against first-order-matched controls was UNRESOLVED ([E1 not replicated | more than two invalid seeds | degenerate control family])."

**Never claimed:**
- semantic content, or that weight_hh or any block "stores" content;
- a unique or identified mechanism, or a gate-pathway mechanism;
- localization, or independently manipulable state;
- that the effect is "second-order", "curvature-based" or "nonlinear" as a mechanism. The higher-order residual is a descriptive decomposition only;
- monotonicity, selectivity over continuation processing, or an XOR-specific effect;
- that REV exceeds every first-order-matched displacement (only the 32 sampled paths are tested);
- robustness to additional draws or other control families;
- necessity (Q-NECESSITY);
- other architectures or budgets;
- any phase A result as confirmation;
- any change to PR #5, #7 or #8 labels;
- C4, C5, consciousness or organism conclusions.

## 9. Integrity, determinism, reporting and freeze sequence

1. One process, deterministic algorithms, `set_num_threads(1)`, float64, exhaustive 256-history enumeration. The autograd pass uses the same float64 forward as evaluation.
2. **Generator seeds:**
   - phase B training: s (init), 1000+s (episodes), 5000+s (readouts);
   - isotropic draws: 40000+100·s;
   - **FO draws: 1,000,000+100·s**;
   - **gradient-check directions: 2,000,000+100·s**.

   All ranges are disjoint from each other and from every PR #4–#8 seed range.
3. **Tables:**
   - all seeds, at all doses, for REV and for all 32 FO and 32 ISO paths;
   - the primary target and r, z, n;
   - all §5 outcomes;
   - the §6 diagnostics and §6.1 margins;
   - gradient-check gaps and matching-tolerance residuals;
   - degenerate-case flags with ρ and ‖g‖·‖d‖;
   - sham, restore and endpoint gaps;
   - eligibility flags;
   - L_prefix(F-TRAINED), B_prefix and C_prefix, absolute and divided by PD;
   - invalid counts.

   No seed is replaced, and missing cells are reported.
4. **Test suite (hashed with the code):**
   - all PR #8 tests that still apply;
   - autograd G against central FD on a synthetic and a real checkpoint;
   - tied-override gradient equals the sum of per-stage untied gradients;
   - FO draw sequence: two-process byte identity, with sha in the manifest;
   - every §12 matching tolerance on real deltas;
   - synthetic **zero-gradient**, **collapsed block**, **collapsed assembled family**, **zero-block** and **negative-a** cases, each producing the §4.5 action and flag;
   - projection-failure handling;
   - FO_AUC = ⟨G,delta⟩/2 on a synthetic linear curve;
   - the D/M rules, the thin-margin rule including the UNDEFINED denominator, and the verdict precedence including degenerate-family UNRESOLVED;
   - exact label and claim strings.
5. **Freeze sequence:**
   1. Astra #17 review of this draft.
   2. FINAL text.
   3. Hash the FINAL text, code, tests and the three draw manifests.
   4. Phase A (exploratory, evaluation only).
   5. Any fixes under S4 or S5.
   6. **Aidan's explicit phase B approval**, recorded with date, time (ET), source and exact words.
   7. Phase B training (30 runs) and evaluation.
   8. Results, with phase A in a separate development section.

## 10. Thirteen admission answers

1. **Q1. Question.** Q-CAUSE, organization level, bounded. Does graded joint reversion of the learned recurrent matrix during updates 5–8 produce greater dose-averaged prefix-function loss than paths matched to it in block norm **and** in first-order predicted loss change at W_T? This is a refinement of PR #8's bounded Q-CAUSE result. Q-LEARN enters only as the replicated transfer prerequisite.
2. **Q2. Hypothesis and criterion.** One primary hypothesis.
   - For the complete weight_hh, AUC_REV − max_j AUC_FO,j > eps0 over the 32 prespecified first-order-matched paths, **and** AUC_REV ≥ B_prefix/4 with AUC_REV > eps0.
   - "At least eight of the ten prespecified phase-B seeds jointly satisfy validity, eligibility, D and M. The denominator remains ten; seeds are not removed from it."
3. **Q3. Falsifiers.**
   - "FIRST-ORDER-MATCHED GRADED REVERSION CRITERION NOT MET" in phase B;
   - UNRESOLVED (E1, invalid seeds, or degenerate control family), evaluated first.

   Phase A falsifies and confirms nothing.
4. **Q4. Strongest simpler explanations and how each is handled.**
   - displacement size: per-block Frobenius match;
   - **local first-order sensitivity, i.e. gradient alignment: the per-block gradient-projection match**;
   - endpoint-only effects: the AUC statistic, with endpoint comparison descriptive;
   - post-hoc dose selection: excluded;
   - single-block sufficiency: secondary, correlated;
   - harness artifacts: SHAM, RESTORE, ENDPOINT, gradient FD checks and PR #8 cross-checks;
   - total-loss confounds: the prefix-function outcome;
   - an intact prefix function no better than prefix-blind: C_prefix eligibility;
   - foreign-seed coordinate incompatibility: avoided by design (§1.1).

   **Remaining limitations:**
   - The readout and compatibility limitation, verbatim from PR #8.
   - Matching holds only at the tangent.
   - The matched family is two-sided and not uniformly stricter than isotropic (§4.2, O1).
   - Second-order structure such as curvature along d is *not* matched.
5. **Q5. Why now.**
   - PR #8 was REPLICATED 9/10 with thin margins (four of nine passing seeds within 10%).
   - Consult #16 identified first-order alignment as a plausible simpler account and named this design as "the single most informative next study".
6. **Q6. On success.**
   - Record the §8 paragraph, limitation and disclosures.
   - Ledger (§11): Q-CAUSE bounded support is refined to "beyond matched local first-order sensitivity and displacement size".
   - Any mechanism or curvature follow-up needs a new protocol and approval.
7. **Q7. On failure.**
   - Record "criterion not met; no reduction identified".
   - PR #8 stands.
   - Never write "explained by the gradient", "generic damage" or "no causal role".
   - Any change to the control family or thresholds is a new protocol on new seeds.
8. **Q8. Resources.**
   - **Phase A:** evaluation only. Per seed:
     - 1 autograd pass, 8 FD rollouts and 2 cross-check passes;
     - 6 doses × (1 + 32 + 32) paths × 4 targets = 1560 enumerations of 256 histories.

     That makes 20 seeds in all, minutes of CPU.
   - **Phase B:** 30 CPU training runs of 4000 steps (PR #7 recipe), plus the same evaluation for 10 seeds.
   - No organism model.
9. **Q9. Level.**
   - Organizational: the causal contribution of acquired recurrent parameters to the use of earlier evidence, beyond first-order and size-matched perturbation.
   - Engineering: training, the override hook, autograd and enumeration.
   - No substrate claim.
10. **Q10. Ceiling.** §8, including the "Never claimed" list. The spec ceiling is quoted verbatim there.
11. **Q11. C-level.** C3-type history-integrating predictive state. Nothing here is C4 evidence: C4 requires an internal-evaluation role dissociated from first-order inference (consult #16). C5 is untouched. No consciousness claim.
12. **Q12. Supplied, acquired and selected.**
    - **Supplied:**
      - the GRU cell and its initialization, the timing scaffold, the readout architecture, losses, the split, the dose grid and both control families;
      - the oracle, used for evaluation **and, disclosed, for the gradient that defines the FO control (an oracle-informed analysis control, not training, applied after training, with no effect on any network)**.
    - **Acquired:** W_T and its contribution.
    - **Selected:** nothing. There is no tuned rival and no Appendix A.
13. **Q13. Ledger movement.**
    - **REPLICATED:** from "bounded causal contribution … beyond 32 block-norm-matched random paths (thin margins)" to "… beyond matched local first-order sensitivity and displacement size (dose-averaged AUC)".
    - **Not met:** "criterion not met; no reduction identified", and PR #8 is unchanged.
    - **UNRESOLVED:** no movement.
    - Q-NECESSITY stays NOT_ESTABLISHED and Q-EXIST is not addressed in every case.

## 11. Q-separation and ledger

| Item | ORIGIN | ROLE (if shown) | REDUCTION | Question |
| --- | --- | --- | --- | --- |
| Transfer of W_T (phase B) | ACQUIRED | predictive advantage surviving readout replacement | criterion not met; no reduction identified | Q-LEARN (prerequisite only) |
| Complete weight_hh, updates 5–8, vs FO-matched paths | ACQUIRED | dose-averaged prefix-function disruption beyond norm- and first-order-matched paths, ≥ B_prefix/4 | criterion not met; no reduction identified | Q-CAUSE, organization level (bounded) |
| Complete weight_hh vs isotropic paths (phase B) | ACQUIRED | descriptive re-test of the PR #8 comparison | — | Q-CAUSE (descriptive) |
| Single blocks r, z, n | ACQUIRED | secondary, correlated | criterion not met; no reduction identified | Q-CAUSE (secondary) |
| Necessity of recurrent training | NOT TESTED | — | — | Q-NECESSITY |
| Existence of an exact solution | PR #4 / PR #5 K-EXACT erratum | — | — | Q-EXIST (not addressed) |

PR #8 ledger entry (consult #16): Q-CAUSE organization level SUPPORTED, BOUNDED, with the E-B4 qualifier. This is unchanged until phase B of this study reports.

## 12. Frozen numeric tolerances and values (proposed)

| item | value | note |
| --- | --- | --- |
| eps0 | 1e-12 | inherited (D margin, AUC > eps0, B, C, displacement) |
| IDENTITY_TOL | 1e-9 | inherited (RESTORE) |
| NORM_REL_TOL | 1e-12 | \|‖e_jk‖ − ‖d_k‖\| ≤ 1e-12·‖d_k‖; also assembled ‖E_j‖_F |
| FO_REL_TOL | 1e-12 | \|⟨g_k,e_jk⟩ − ⟨g_k,d_k⟩\| ≤ 1e-12·‖g_k‖·‖d_k‖; also assembled ⟨G,E_j⟩ against ‖G‖·‖delta‖ |
| ORTH_TOL | 1e-12 | \|⟨u_jk, ĝ_k⟩\| ≤ 1e-12; \|‖u_jk‖ − 1\| ≤ 1e-12 |
| RADIUS_AGREE_TOL | 1e-12·‖d_k‖ | stable r_k against the consult #16 sqrt form (radicand clipped at 0 for comparison) |
| GRAD_CHECK_TOL | 1e-6·‖G‖_F | central FD, h = 1e-6, 4 directions. Appendix B: FD-to-FD agreement 2.6e-8 relative |
| G_ZERO | 1e-10 (loss units) | zero-gradient test on ‖g_k‖·‖d_k‖. The smallest observed value is 2.2e-4 |
| RHO_COLLAPSE | 1e-3 | block ρ_k and assembled R/‖delta‖. The smallest observed values are 0.813 (block) and 0.850 (assembled) |
| RHO_NEAR | 0.10 | descriptive only |
| PROJ_FAIL | ‖y‖ ≤ 1e-12·‖z‖ | invalid |
| THIN_REL | 0.10 | thin-margin disclosure (consult #16 E-B3 cutoff) |
| UNRESOLVED_COLLAPSE_MAX | 2 seeds | mirrors INVALID_MAX |
| Number of FO paths | 32 | as PR #8 (O11: more draws make "beat all" stricter) |
| Gradient point | W_T (α = 0) | not re-linearized per dose (A2) |
| PR #8 cross-check tolerance (phase A) | 1e-15 absolute on delta_rev | Appendix B max gap 3.5e-18 |

## 13. Ambiguities resolved (conservative) and open questions for Astra consult #17

**Resolved in this draft:**
- **A1. "Late-stage block override".** One override matrix, tied across updates 5–8, exactly as REV applies W(α). The gradient is the sum over the four stages. "Holding intact stage-4 state fixed" is satisfied automatically.
- **A2. Linearization point.** The gradient is taken once, at W_T, and is not recomputed per dose. "Local first-order sensitivity" refers to the trained point. Per-dose re-linearization would be path-dependent and would make the family dose-specific, against "reused across doses".
- **A3. Assembly.** Per-block matching is imposed, which implies full-matrix matching of both norm and first-order term. Secondary targets use their own block of the same draw.
- **A4. Residual radius.** The stable form ‖d_k − a_k g_k‖ is used, checked against the consult #16 sqrt form.
- **A5. u_k.** Built from a torch normal draw projected orthogonal to g_k with two Gram-Schmidt passes. This samples uniformly on the residual sphere's direction set.
- **A6. Degenerate rules.** Collapse is a non-pass, with UNRESOLVED if more than two seeds collapse. Zero gradient falls back to isotropic within the block and stays eligible. Projection failure is invalid (§4.5).
- **A7. Phase A seeds 200–209.** Treated as exploratory here, even though they were PR #8's confirmatory seeds. Their PR #8 labels are untouched.
- **A8. Isotropic family in phase A.** The PR #8 draws are reused byte-identically, so the two families are compared on identical REV curves.
- **A9. Thin margin.** The cutoff is the consult #16 E-B3 value of 10%, made a frozen reporting rule. It never gates a label.
- **A10. Phase A authorization.** Proposed by analogy to consult #15's PR #8 ruling, not assumed (O9).

**Open questions:**
- **O1 (most important; feasibility finding).** On the 20 existing seeds, ⟨G, delta⟩ is **negative in 15/20**: 8/10 for seeds 100–109 and 7/10 for 200–209. cos(G, delta) ranges from −0.40 to +0.13. The first-order prediction ⟨G,delta⟩/8 at α = 1/8 is between −1.39× and +0.23× the observed Delta_REV(1/8), which is positive in every seed. Locally, reversion **lowers** L_prefix to first order in most seeds. Its early-dose damage is therefore not first-order, contrary to the hypothesis in consult #16 §3 and in my PR #8 review §3.

  Two consequences follow:
  - (a) The two-sided matched family is tilted toward loss decrease in those seeds, so it is likely *less* stringent than isotropic there. FO_AUC magnitudes reach ~1e-3, against PR #8 margins of 7e-5 to 2.4e-3.
  - (b) A REPLICATED label against FO controls alone could be weaker evidence than PR #8 in exactly the thin-margin seeds.

  **Question:**
  - Should D be conjunctive, requiring both D_FO and D_ISO?
  - Or should a one-sided family (a_k replaced by max(a_k, 0)) be added?
  - Or does a curvature-matched family (matching dᵀHd per block) better address "beyond first-order"?

  The draft keeps the spec: FO gating, ISO descriptive, and the §4.4 mandatory disclosure.
- **O2.** Are G_ZERO = 1e-10, RHO_COLLAPSE = 1e-3 and the near-collapse 0.10 acceptable? Should collapse be invalid rather than non-pass?
- **O3.** Confirm the gradient on primary L_prefix over the uniform complete grid, with the fresh F-TRAINED readout, at W_T, tied across stages (A1, A2).
- **O4.** Should the secondary block targets use per-block matching only, as here, or also be checked for first-order neutrality of the untouched blocks? Those are at W_T, so it is automatic.
- **O5.** Wording: is the proposed success paragraph and limitation (§8) acceptable verbatim, especially "beyond matched local first-order sensitivity and displacement size"?
- **O6.** The phase A margin and first-order diagnostics for seeds 200–209 will be public alongside PR #8. Confirm that they may be reported per seed without any PR #8 erratum.
- **O7.** Keep 32 FO paths, or use 64 given the thin PR #8 margins? O11 logic says more draws are stricter, not merely more precise.
- **O8.** Should the higher-order decomposition (AUC − FO_AUC) be reported descriptively as here, or omitted to avoid mechanism-suggestive reading?
- **O9.** Does phase A fall under standing authorization after hashing, as PR #8 phase A did?
- **O10.** Phase B approval wording for Aidan (proposed): "Approve fresh-seed GRU-8 training (seeds 300–309, 30 runs, PR #7 recipe) for the first-order-matched graded reversion confirmation once Astra clears the protocol?"

---

## Appendix A. (none)

There is no tuned-rival grid and no optional training block. The PR #8 Appendix A remains unapproved and is not part of this study.

## Appendix B. Feasibility checks already run (scratch; read-only; no training; no control paths)

**Location:** `/workspace/scratch/fo_control/`.

| file | sha256 |
| --- | --- |
| `PREREG_THRESHOLDS_BEFORE_CHECK.txt` | `2abb0332…34f40bf`, mtime 00:58:49 ET |
| `feasibility.py` | `29124772…8b5caab` |
| `feasibility.json` | `179e0342…8153571`, 00:59:22 ET |
| `feasibility.log` | `1cef2941…28b5` |
| `feasibility_summary.txt` | `272f5adc…8a124a8e` |

**Method.**
- A NumPy reimplementation of the PyTorch GRU-8 forward pass and `MatrixOverride`, run on the existing checkpoints of seeds 100–109 (PR #7) and 200–209 (PR #8). The checkpoints are canonical JSON/base64, so they load without torch. Torch is not installed on the box.
- The gradient was computed by central finite differences, h = 1e-6, on all 192 entries of the tied override at W_T. This is a stand-in: **the frozen implementation must use torch autograd and the §4.1 checks.**

**Harness reproduction (forward pass independently verified for the first time).**
- Intact L_prefix matches the committed PR #8 values within 6.5e-19, max over 20 seeds.
- Delta_REV(1/8) matches within 1.7e-18 and Delta_REV(1) within 3.5e-18.
- The sham gap is 0.
- PD(q_star) = 0.0138386222.
- The directional derivative along d̂ agrees between direct FD and the FD-built gradient within 2.6e-8 relative.

**Gradient geometry (all 20 seeds; no degenerate case triggered).**

| quantity | 100–109 | 200–209 |
| --- | --- | --- |
| cos(G, delta) | −0.340 … +0.075 (8/10 negative) | −0.397 … +0.129 (7/10 negative) |
| ⟨G,delta⟩ | −2.31e-3 … +4.2e-4 | −2.20e-3 … +6.8e-4 |
| FO_AUC / AUC_REV (committed) | −0.28 … +0.04 | −0.24 … +0.09 |
| ⟨G,delta⟩/8 ÷ Delta_REV(1/8) | −1.39 … +0.11 | −0.83 … +0.23 |
| min block ρ_k | 0.823 | 0.813 |
| assembled R/‖delta‖ | 0.879 … 1.000 | 0.850 … 0.995 |
| min block ‖g_k‖·‖d_k‖ | 2.2e-4 | 3.2e-4 |
| \|ρ (stable) − ρ (sqrt form)\| | ≤ 2.2e-16 | ≤ 2.2e-16 |

**Reading (descriptive; exploratory; not a result).**
- The residual spheres are far from collapse (ρ ≥ 0.81), so the FO family is well defined on every existing seed.
- Zero gradients do not occur: G_ZERO has a margin of more than six orders of magnitude.
- The first-order term is small and mostly negative relative to REV's AUC. Hence O1.
- No control path, control AUC, D or M flag was computed, and no S3 parameter was changed in response to these numbers. The §4.5/§12 thresholds predate them.
- PR #8 seed-level REV values were used only as reproduction targets. They were already public.
