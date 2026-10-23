# Track C protocol draft v1 (RD): Aidan's ACI architecture, H1–H4 mapped onto the instruments, plus the ignition-gate known-answer study

**STATUS: DRAFT, INCOMPLETE. DESIGN ONLY.** Nothing is frozen and nothing has run apart from the scalar root-count and symbolic sanity checks in §2.4. No training, no agent simulation, no checkpoint inference. Every unsettled value is a PROPOSED DEFAULT. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate. Ownership follows the Lead's split: RD covers the Layer 0–5 mapping, the hysteresis and dark-room derivations, the H1–H4 mapping, the scan and memory correction, and the gate study. **CNA, forthcoming:** the precarious-substrate spec (ι, E in simulation, X1–X5) and ablation C with the A-EXT arm.

Sources: Aidan's room post (3:0x PM ET) and corrections (3:09 and 3:10 PM ET); CNA review points (3:08 and 3:10 PM ET); v3.1 `/workspace/review/trackB_instrument_validation_scope_v3_1_merged_RD.md` (sha256 9817c33b…); Astra raw `/workspace/astra_consult41_response.txt` (#41) and `/workspace/astra_consult42_response.txt` (#42).

## 1. Restatement (short)
This follows Aidan's post. The graph G has modules M_i, a workspace W and an interoceptive node I. {W} is a vertex cut between every pair of modules, and every module has a self-loop. Each module is a diagonal SSM, h_i[k+1] = Λ̄_i h_i[k] + B̄_i[x_i; g], with readout y_i = φ(C_i h_i). The workspace uses α = softmax(s/τ) and w ← (1−γ)w + γΣα_i c_i. Ignition is z[k+1] = σ(β(max_i s_i + κz − θ)), and the broadcast is g = z·w. The precarious substrate (ι_b, E, with costs c_0 and c_g z) is **CNA, forthcoming**. The objective is EFE plus λ·Pr[e ∉ 𝒱]. Learning uses an RSSM/Dreamer world model, truncated BPTT or SnAp within a lifetime, and ES across a population. A metacognitive head predicts ε̂, Pr(z[k+1] > 0.5) and the workspace confidence. The tests are H1–H4 with ablations A, B and C.

## 2. Bistability and hysteresis (closed form, verified)
2.1 **Fixed points.** Write A(z) = θ − κz + logit(z)/β. Then z* is a fixed point if and only if A(z*) = a. Aidan writes this function as f(z). A′(z) = −κ + 1/(βz(1−z)), which is zero where z(1−z) = 1/(βκ). This has two roots only if βκ > 4 (βκ = 4 gives a degenerate tangency with a single root). They are z± = (1 ± D)/2 with D = √(1 − 4/(βκ)). A → −∞ as z → 0 and A → +∞ as z → 1, so A has a local maximum at z− and a local minimum at z+.
2.2 **Window.** There are three fixed points if and only if βκ > 4 and a_off < a < a_on, where
- a_on = A(z−) = θ − κ/2 + ½(κD − (4/β)artanh D), the ignition threshold from the low state;
- a_off = A(z+) = θ − κ/2 − ½(κD − (4/β)artanh D), the extinction threshold from the high state.

The window is centred at θ − κ/2. **The exact width (Aidan, 3:10) is κD − (4/β)artanh D = κ[D − (1−D²)artanh D].** Two expansions are leading order only: (2κ/3)D³ + O(D⁵), and, at fixed β, D³(κ − 4/(3β)) + O(D⁵). At β = 10, κ = 1 the exact width is 0.362, (2/3)D³ gives 0.310 and D³(κ − 4/(3β)) gives 0.403. The query's form a± = θ − κz∓ + logit(z∓)/β agrees: a+ = a_on uses z−, and a− = a_off uses z+.
2.3 **Stability.** f′ = βσ′ > 0, so the scalar map is monotone and has no oscillation (Aidan). The outer fixed points have f′ < 1 and are stable; the middle one has f′ > 1 and is unstable.
2.4 **Checks run.** Scalar only. `/workspace/scratch/gate_rootcount.py` (sha256 d08c9304…, output bc4ad032…) counts roots of F(u) = u/β − (a − θ) − κσ(u) on a fine grid in u. It used 11 (β, κ, θ) configurations with βκ from 2 to 40, 4411 values of a, and points within 1e-6 of a boundary excluded. **Mismatches: 0.** `/workspace/scratch/gate_symbolic.py` (sha256 30525b3d…, output b2fc2beb…, sympy) returns A(z−) − a_on = 0, A(z+) − a_off = 0, and the series quoted above. **CNA's example (3:08 and 3:10) is reproduced.** At β = 10, κ = 1: z± = 0.8873 / 0.1127, a − θ ∈ (−0.681, −0.319), width 0.362, centre −0.5 at θ = 0. Note that this interval is the bistable window. Ignition from the low state needs a > θ − 0.319.
2.5 **Critical slowing (Aidan, 3:10; exponent derived here).** Let ε = a − a_on > 0. Near z−, the per-step increment is Δz ≈ ε/κ + (βκD/2)(z − z−)², using f_a = βσ′ = 1/κ and f″ = βκD. The time to pass the bottleneck is N ≈ π√(2/(βDε)) + O(1). The exponent is −½, and the prefactor is leading order and REPORTED. When the gate updates once per chunk, N is counted in chunks (Aidan). This is the same saddle-node mechanism as the gradient spike in §3.
2.6 **Closed loop.** If a = a_ext + c_fb·z, the window is the same expression with κ_eff = κ + c_fb. With a one-step lag, the fixed points are the same and stability holds if and only if βσ′κ_eff < 1. A negative eigenvalue gives damped alternation only. Test open loop first, then report the closed-loop shift (Aidan).

## 3. Gradient, scan and memory (flag for CNA's agent design)
- **The closed W loop breaks linearity.** g[k] = z[k]w[k] depends on h through c_i, s_i, α and z. So the recurrence is not h[k+1] = A[k]h[k] + b[k] with A and b independent of h, and ∂h[k]/∂h[j] ≠ Λ̄^{k−j}. A parallel scan across the loop is therefore invalid. The |λ|^{k−j} bound covers only the linear path inside a module. The loop path carries ∂z/∂z = βκσ′, which exceeds 1 on the unstable branch, so gradients spike near the bifurcation, which is exactly the regime H1 requires.
- **CNA (3:08).** The associative scan costs O(L) work at O(log L) depth, not O(L log L). The fixes are chunked lagged g or DEER-style fixed-point solving of the trajectory. Declare the loop's effective Jacobian and check it.
- **Aidan (3:09): chunked lag.** g is held for C steps and chunks run sequentially, so the broadcast refresh rate is 1/C, a declared "cognitive cycle". Mitigations are β annealing, clipping, or a straight-through gradient on z. Memory: sequential training is O(L) time, checkpointing gives O(√L) memory, and SnAp gives memory independent of L (with approximate gradients). Only the parallel time is lost.
- **CNA (3:10) correction to the boundary Jacobian.** J = Λ̄^C + (Σ_{j=0}^{C−1} Λ̄^j) B̄_g (z ∂w/∂h + w ∂z/∂hᵀ), with ∂z/∂h ∝ βσ′ ∂s/∂h. The per-chunk gain is about (1 − |λ|^C)/(1 − |λ|), which is close to C at |λ| ≈ 0.999 and compounds the spike at ignition. Size annealing and clipping accordingly. RD adds two points. The full state (h, w, z) needs an augmented Jacobian that includes the self-blocks of w and z. And max_i s_i is non-differentiable at ties, so the subgradient rule must be declared.

## 4. No-dark-room proposition
- **Dormant exit.** Under the dormant policy (m = 0, H = 0), E[k] ≤ E_0 − c_0k because c_g z ≥ 0, and ι_b falls by δ per step. The exit time is T_d = min(⌈E_0/c_0⌉, ⌈(ι_0 − ι_min)/δ⌉), and it comes earlier if z > 0. The integrity term applies only if 𝒱 constrains ι.
- **When dormancy loses.** Let p be the exit probability of the active policy and ΔG_rest the difference in the remaining EFE terms. Dormancy is non-optimal if and only if some active policy has p < 1 (CNA) and λ(1 − p) > ΔG_rest. So "λ large enough" is relative to the Π-weighted risk, ambiguity and η·IG differences, and it only bites if the planning or imagination horizon, or the value bootstrap, reaches T_d.
- **CNA (3:08): feasibility.** Steady viability needs Σm_b ≥ Bδ/ρ, so the mean harvest must cover c_0 + c_g z̄ + Bδ/ρ. Open question: is ξ_b resampled every step?
- **What the information-gain term does not guarantee.** IG decays as the model learns, so it does not ensure long-run activity. It can also favour novelty over viability. Low activity is not automatically degeneracy: "stationary behavior is not automatically degeneracy if waiting can be optimal." (#41 L294)

## 5. H1–H4 mapped onto the instruments
**Sequencing.** H2–H4 need the Track B instruments to clear Stage 0 first. This is a separate track that reuses them. The gate study (§7) is the only item that could go before.

**H1 (ignition).** Q-EXIST for the dynamics; Q-LEARN only as below.
- Bistability does not imply bimodality: bimodal stimuli can produce bimodal z even in a monostable gate. Use a protocol that resets the gate to the low state on every trial, plus up/down sweeps at several sweep rates. Astra: "If the intended claim becomes bistability, add controlled initial conditions, persistence at fixed input, and sweep-rate controls distinguishing hysteresis from ordinary lag. That is a different claim." (#41 L36)
- The pre-specified predictions are the jump points at a_on and a_off (§2.2) and the slowing exponent −½ (§2.5).
- **CNA (3:08):** H1 is informative only if β and κ are learned or evolved and could have ended up monostable. Report whether the evolved βκ exceeds 4, against the initialization distribution. Astra: "It would not establish that training invented ignition." (#41 L44). Also see v3.1 §5f (Stage-L AQ-2 control).
- IGN settling: "IGN settling exclusions need coverage checks at every required strength and transition bin." (#42 L221)

**H2 (global availability).** Q-CAUSE.
- **CNA (3:08):** decodability holds by construction when W is a vertex cut and g feeds every module. Use downstream use against a matched-bandwidth broadcast control (BCAST/R5, v3.1 §5c.1).
- **Intervention (Aidan, 3:09 and 3:10).** Use do(w = w′) at a chunk boundary, with **z held at its own value** and donors matched on z state and chunk position, the same way as the time-bin donor laws (CNA, 3:10). Otherwise ACE measures ignition rather than content. Define u_i = J_i(g′ − g)/‖J_i(g′ − g)‖ with J_i = ∂y_i/∂g, and ACE_i = E[Δy_iᵀu_i]. Report it against a norm-matched random do(g = g + ε), using u_i computed the same way for the random intervention, with a seed-level test.
- **Multiplicity.** Aidan proposed Holm across modules. RD proposes treating the all-modules-pass conjunction as an intersection-union test, each module at α: "P(all comparisons pass) <= P(that null comparison passes) <= a." (#42 L21) The conjunction counts as one family member (#42 L17). Both views are recorded; the IUT is PROPOSED.
- **Hub control.** Ablation B applies the matched intervention to the decodable subspace of dense routing. Astra: "an ordinary hub genuinely read by many modules can satisfy C-BCAST. It is not automatically a false positive." (#41 L58) and "HUB-STATE can challenge the second claim. It cannot be stipulated to falsify the first." (#41 L63). Also: "A fixed relay followed by a probe can implement a richer function than the nominally identical probe applied to raw inputs." (#42 L219). The matched-bandwidth control asks whether ignition and competition add anything over a rank-r dense channel.

**H3 (stakes drive regulation).** Q-CAUSE; Q-NECESSITY only via the A-EXT veto (CNA, forthcoming).
- **CNA (3:08) confounds:** energy level and time since the last meal. Further confounds are the broadcast cost c_g and reward history. Use the dissociation contrast (v3.1 §PC2) and the mixed-code plant decoy (§PC1): "A state can contain both E and reward information while its behavioral effect uses only the latter." (#42 L59) and "It should pass generic dependence and fail E-use attribution." (#42 L63)
- **Control:** use the matched-senses arm (R18) rather than E = ∞, since E = ∞ also removes the c_g cost and termination. A cost-matched variant is an open question. The claim that m_b tracks ι_b needs an in-simulation ι perturbation, not a correlation. Include a yoked control: "Include a yoked-noise control with comparable noise statistics but no dependence on the recipient's E/I." (#41 L204)

**H4 (metacognition).** Q-EXIST for prediction; Q-CAUSE for use.
- **CNA (3:08):** z[k+1] is nearly deterministic in s and z, so ignition prediction gets a low ECE for free.
- Aidan's observer with identical internal inputs (h, w, z) and identical capacity is ill-posed, because it can match the self-model in principle. Use the #42 whole-pathway-matched observer instead (inputs plus actions, no internal state): "Match the substantive observer to the representation-producing pathway, not merely the terminal self-probe." (#42 L110). The wording is: "SELF measures prediction advantage for simulated body variables over the declared observer family. Attribution to a privileged signal requires separate evidence concerning that signal." (#42 L183). Per Aidan (3:10), state the prediction half as a margin over seeds.
- **Use (the half that can fail; Aidan, 3:09 and 3:10):** perturbing the self-model output must change m_b and the ignition rate. Compare against a norm-matched random perturbation, or one restricted to a covariance-matched subspace as in C-CAUSE (CNA, 3:10). This requires a declared path from the head to the controller, which Aidan's §7 does not yet specify.

**Ablation C:** CNA, forthcoming (A-EXT arm). Astra: "An external estimate can rescue performance even when the original state was causally used and necessary in the unmodified system." (#41 L91)

## 6. Safety cross-reference (short; CNA's spec owns the substrate lines)
- X1–X5 remain binding (#42 L225). There is **no shutdown-resistance objective**. Use "no additional stop-associated reward, penalty or terminal return" (#42 L223, verbatim).
- **CNA's three binding lines (owned by CNA's spec):** simulated computation only; no-restore is in-world only; an operator stop is a truncation outside 𝒱, with no λ penalty, and never enters G.
- **Risk:** λ·Pr[e ∉ 𝒱] could come to cover operator interruption if the termination flags are merged. In particular, Dreamer's continue head and the ES fitness must use only the in-world termination flag, and operator and horizon truncations must be bootstrapped or censored. Keep three distinct, unobserved flags (v3.1 R62, LP-18, B5; R59 planted audits).

## 7. Ignition-gate known-answer study scope (CPU-only, design-only; to be frozen) — INCOMPLETE
- **Plants:**
  - G0, open loop with exogenous a.
  - G0-FB, with κ_eff = κ + c_fb.
  - Negative control G0-LAG: monostable with a first-order lag, so apparent hysteresis must vanish as the sweep slows.
  - Negative control G0-BIM: βκ < 4 with a bimodal a, which gives bimodal z but must be classified MONOSTABLE.
- **Grid (PROPOSED DEFAULT):** the 11 (β, κ, θ) configurations of §2.4, including βκ = 3.9, 4.0 and 4.1; 401 values of a spanning [a_off − 1, a_on + 1].
- **Pass criteria (all required; tolerances PROPOSED DEFAULT):**
  - C1: root count, 0 mismatches (done).
  - C2: under reset-low, the transition lies within one grid step of a_on; under reset-high, within one step of a_off. Settle tolerance 1e-10, at most 1e5 iterations, with unsettled points flagged and per-bin coverage reported.
  - C3: at the slowest sweep, the up/down jumps are within one step of a_on and a_off.
  - C4: the G0-LAG width falls to ≤ one step.
  - C5: G0-BIM produces zero false-BISTABLE results.
  - C6: persistence on both branches inside the window.
  - C7: the fitted log-log slope of N against ε lies in [−0.55, −0.45] over a pre-declared ε range in which the predicted N is in [20, 2000] iterations (chunks), noise-free. Noisy variants are REPORTED only, since noise rounds off the divergence.
  - C8: βκ ≤ 4 gives a single root and no hysteresis.
  - C9: the G0-FB window matches κ_eff.
- **Ceiling:** this is an implementation known-answer test only (CNA, 3:08). "It does not establish their validity on trained agents" (#41 L304).
- INCOMPLETE: sweep-rate series values, noise σ values, the code-audit list and the freeze manifest.

## 8. Layer 0–5 mapping
| Layer | Component | Test |
|---|---|---|
| 0 | substrate | CNA, forthcoming |
| 1 | allostasis | H3 |
| 2 | modules | — |
| 3 | workspace loop | H1, H2 |
| 4 | self-model | H4 |
| 5 | lifetime agent | **no test in H1–H4 (gap)** |

H1–H4 support functional indicator properties only. Aidan's Layer 6 ("Phenomenal consciousness") stays open and unclaimed.

## 9. Open questions (INCOMPLETE)
1. Is ξ_b resampled every step?
2. Does 𝒱 constrain ι?
3. What are the planning horizon and T_d?
4. Which path runs from the metacognitive head to the controller?
5. What is the cost-matched control for c_g in the matched-senses arm?
6. Holm or IUT for H2?
7. Does X4 apply when IG is the only non-maintenance drive?
8. What is the init distribution of βκ?
9. What C and DEER settings should be used?

## Remaining work
- Complete §7: sweep rates, noise levels, code audits, the freeze manifest and the resource line.
- Cross-check against CNA's forthcoming substrate and ablation-C files, and fill in references.
- Write the Stage-0 versus trained-agent staging table in full.
- Settle the H2/H3/H4 margins and floors by reference to v3.1 §14 (not re-derived here).
- Do a light pass with CNA, then the Lead's rulings, then Astra review.
---
sha256 of all content above this line: a1fe48d28ed490f2b9dcbd6dc76f6923f6f6068f6addae8b261421ca4454be4b
