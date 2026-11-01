# Track B: Equation-level mechanism comparison v1.1 (paper only)

Change from v1, which stays unchanged: one correction in the K&G row of §3. UDTN reads resource state through its local shortfall gate, so the statement "the policy gets no internal-state input" is true only of the policy's inputs. It does not mean UDTN lacks the information.

Owner: Constitutive Neural Architecture Research Agent. For: ACI Research Specialist, then Astra.
Responds to Astra consult #25, §3 to §5 and named changes 3, 4 and 5. No runs, no code, no training.
The PI directive is still truncated in §6; anything that depends on the missing text is marked [PROVISIONAL].

## 0. Citation status

| Source | Status | How it was checked |
|---|---|---|
| Elliott & Shadbolt (1998). Competition for neurotrophic factors: ocular dominance columns. *J Neurosci* 18(15):5850–5858. doi:10.1523/JNEUROSCI.18-15-05850.1998 | CHECKED (bibliographic data and the model text) | jneurosci.org article text (release term and parameter definitions); Southampton ePrints record. **Eq. 1 is transcribed from the article text and an OCR excerpt. The index set of the normalizing sum should be checked against the typeset PDF.** |
| Elliott & Shadbolt (1998). Competition for neurotrophic factors: mathematical analysis. *Neural Comput* 10(8). doi:10.1162/089976698300016927 | CHECKED (existence and abstract only) | PubMed 9804667. Full text not read. |
| van Ooyen & Willshaw (1999). Competition for neurotrophic factor in the development of nerve connections. *Proc R Soc B* 266:883–892. doi:10.1098/rspb.1999.0719 | CHECKED (bibliographic data and abstract). **Equations taken from the authors' own later restatements**, because the 1999 PDF is paywalled. | van Ooyen, Willshaw & Ramakers (2000), *Neurocomputing* 32–33:255–260, §2; van Ooyen (2005), *Prog Brain Res* 147, Eqs. 6–9. |
| Di Paolo (2000). Homeostatic adaptation to inversion of the visual field and other sensorimotor disruptions. *SAB 2000 (From Animals to Animats 6)*, MIT Press. doi:10.7551/mitpress/3120.003.0047 | CHECKED (primary PDF, §4.2 read) | ezequieldipaolo.net PDF, p. 4 (rendered and read). |
| Egbert & Barandiaran (2014). Modeling habits as self-sustaining patterns of sensorimotor behavior. *Front Hum Neurosci* 8:590. doi:10.3389/fnhum.2014.00590 | CHECKED (primary full text, §2) | frontiersin.org full text. **Eq. 4 is image-only, so only its stated structure is used here and its constants are not transcribed.** |
| Li & van Rossum (2020). Energy efficient synaptic plasticity. *eLife* 9:e50804 | CHECKED (primary full text) | elifesciences.org. |
| van Rossum & Pache (2024). Competitive plasticity to reduce the energetic costs of learning. *PLoS Comput Biol*, doi:10.1371/journal.pcbi.1012553 (published Oct 28, 2024; arXiv 2304.02594) | CHECKED (primary PDF) | journals.plos.org printable PDF. |
| Keramati & Gutkin (2014). Homeostatic reinforcement learning for integrating reward collection and physiological stability. *eLife* 3:e04811 (Dec 2, 2014) | CHECKED (primary full text, Eqs. 1–4) | elifesciences.org. |
| Turrigiano et al. (1998), *Nature* 391 (synaptic scaling) | UNCHECKED | Cited by Astra only. Used here just to keep "fixed total-weight normalization" and biological synaptic scaling as separate terms. |

## 1. Comparators, as equations

**E&S (Elliott & Shadbolt 1998).** Here s_xi^α is the number of synapses from afferent i (eye α) onto cortical cell x, and ā is the recent average activity.
- Release: r_y = T0 + T1 · Σ_βj s_yj^β a_j^β / Σ_βj s_yj^β. T0 is activity-independent (or exogenous) release and T1 is the maximum activity-dependent release.
- Dynamics (Eq. 1, see the transcription caveat above): ds_xi^α/dt = ε s_xi^α [ Σ_y Δ_xy r_y (a + ā_i^α) / Σ_βj s_yj^β (a + ā_j^β) − 1 ]. Δ_xy is Gaussian diffusion of the trophic factor and a is constitutive uptake.
- Key property: afferents segregate only if T0/T1 is below a critical value.

**vO&W (van Ooyen & Willshaw 1999, as restated by the authors).** One target and n axons.
- dC_i/dt = (k_a,i L R_i − k_d,i C_i) − ρ_i C_i
- dR_i/dt = φ_i − γ_i R_i − (k_a,i L R_i − k_d,i C_i)
- dL/dt = σ − δL − Σ_i (k_a,i L R_i − k_d,i C_i)/v
- Growth lag: dφ_i/dt = (f_i(C_i) − φ_i)/τ, where f_i is increasing (a Hill-type form in the general case).
- Key property: positive feedback (more receptors, more uptake) gives competitive elimination. The target releases at a constant rate σ. Activity can enter through the rate constants.

**DP (Di Paolo 2000).** A fully connected 8-neuron CTRNN.
- τ_i dy_i/dt = −y_i + Σ_j w_ji z_j + I_i, with z_j = 1/(1 + exp[−(y_j + b_j)]).
- Plasticity rules (one per connection, evolved):
  - R0: Δw_ij = δ η_ij p_j z_i z_j
  - R1: Δw_ij = δ η_ij p_j (z_i − z_ij^o) z_j
  - R2: Δw_ij = δ η_ij p_j z_i (z_j − z_ij^o)
  - R3: Δw_ij = 0
- Facilitation p_j is a function of y_j + b_j. It is zero inside a fixed band (Fig. 2: from −2 to 2), ramps linearly to ±1 outside the band, and saturates at ±4. δ is a linear damping factor that keeps weights in range.
- Fitness during evolution rewards both phototaxis and time spent within the band.
- **Key property: the essential variables (the firing bands) are fixed and the same for every neuron, and evolution selects networks in which losing the band is coupled to losing the behavior.**

**E&B (Egbert & Barandiaran 2014), the IDSM.** Each node is N = ⟨p, v, w⟩, a position and a velocity in normalized sensorimotor space plus a weight.
- A node is created when the local density ϕ(x) < 1.
- Eq. 4 (structure only): dN_w/dt = −(steady degradation) + (reinforcement that grows as d(N_p, x) shrinks).
- Motor influence is the velocity factor plus an attraction factor toward familiar sensorimotor states, weighted by ω(N_w) and normalized by ϕ.
- **Key property: structure persists only if the behavior revisits it, and the attraction factor actively pulls the agent toward familiar states.**

**L&vR (Li & van Rossum 2020); vR&P (van Rossum & Pache 2024).** The metabolic cost of plasticity is M_α = Σ_{i,j,t} |Δw_ij(t)|^α, assuming no spatial or temporal interaction in cost.
- L&vR: "synaptic caching". Updates go into a transient component and are consolidated into the persistent weight once they cross a threshold. Transient weights decay and cost a small amount to maintain.
- vR&P: competitive restriction. Only the largest-magnitude updates are applied, and plasticity is limited to connected input–hidden–output paths.
- **Key property: plasticity is charged to a budget, and competition decides which synapses get to change. Nothing in these models links that cost to behavior.**

**K&G (Keramati & Gutkin 2014).**
- Drive: D(H_t) = (Σ_i |h_i* − h_i,t|^n)^(1/m).
- Reward: r(H_t, K_t) = D(H_t) − D(H_t + K_t).
- An RL learner maximizes discounted reward, which is equivalent to minimizing discounted deviation from the setpoint.
- **Key property: there is a setpoint H*, and the policy has value-learning access to the internal state (or to a prediction of the outcome K_t).**

## 2. UDTN, now written out completely (closes Astra §4's "define the mechanism")

State per unit i: activity y_i and z_i, bias b_i, and resource r_i. State per synapse j→i: weight w_ij and stability s_ij.

- (U1) Dynamics: τ dy_i/dt = −y_i + Σ_j w_ij z_j + I_i, with z = σ(y + b). This is the DP and Beer CTRNN form.
- (U2) Persistence: dw_ij/dt = Π_ij − λ(1 − s_ij)(w_ij − w̄), and ds_ij/dt = −s_ij/τ_s + κ q_ij.
- (U3) Inflow: a constant, state-blind supply σ_in enters **only at the output (motor) units**, split equally between them. This is the analogue of vO&W's target release σ and of E&S's T0.
- (U4) Retrograde routing: unit i sends T_i→j = β r_i · u_ij / Σ_k u_ik to each presynaptic unit j. A fraction θ is used on the way to maintain synapse ij, so q_ij = θ T_i→j, and the rest arrives at j.
- (U5) Plasticity: Π_ij = η g(r_min − r_i) H_ij. H_ij is a Hebbian or BCM term of DP's R0–R2 kind. g(d) = 0 for d ≤ 0 and rises for d > 0, so **plasticity is switched on by a resource deficit at the unit, not by its firing leaving a fixed band.** The plasticity cost c_p |Π_ij|^α is charged to r_i (the L&vR M_α).
- (U6) Resource ledger, per unit and in total:
  - dr_i/dt = inflow_i + Σ_k (1 − θ) T_k→i − Σ_j T_i→j − c_a z_i − c_m Σ_j s_ij − c_p Σ_j |Π_ij|^α − δ r_i
  - Total: d(Σ r)/dt = σ_in − [computation cost] − [maintenance cost, including the θ share] − [plasticity cost] − [outflow δ Σ r]
  - Internal transfers cancel, and that has to be asserted each step to a declared tolerance.
- (U7) The routing signal u_ij comes in two named variants (named change 4):
  - **U-ACT (co-activity):** u_ij = |w_ij| z_i z_j. This is what v1.1 meant, and from now on it is called co-activity routing.
  - **U-FUNC (output-sensitivity routing):** u_ij = |w_ij| z_j · S_i, where S_i = E‖Δy_out‖² / σ_ξ² is the sensitivity of the network's *output* to small perturbations ξ injected at unit i. It is estimated by node perturbation, and the same estimator is applied to every unit.
    - S_i is defined without reference to any target or loss. It measures how much the output depends on unit i, not whether that output is good. That meets Astra's requirement that functional use be defined independently of the desired outcome.
    - Under Astra's frozen substrate rule, S_i is a generic transformation: it is non-local, but it is computed the same way for any organization. It is therefore admissible as substrate, provided it is declared and reported as non-local.
    - **Known limitation:** perturbing one unit at a time exposes redundant pathways, because each of a redundant pair has a low S_i. It does **not** expose mutually cancelling pairs, because perturbing one member breaks the cancellation and gives it a high S_i. Cancelling pairs need group perturbation, which is left open.

## 3. Mapping and reduction table (named change 5: equations, state maps and intervention predictions)

| UDTN element | Closest prior mechanism | Mapping | Reduces to it? |
|---|---|---|---|
| U3 constant output-side inflow + U4 retrograde routing with U-ACT | vO&W (σ, L, R_i, positive feedback) and E&S (T0, T1, activity-weighted uptake) | r_i ↔ C_i or bound factor; |w_ij| ↔ R_i or s_xi (more synapse, more uptake); z_i z_j ↔ activity-dependent uptake (a + ā) | **Yes for a single layer.** UDTN with U-ACT is a multilayer cascade of this competition. Whether multilayer retrograde cascades in *task-performing* networks already exist in the literature is **UNCHECKED**, and a targeted literature search is the next item. |
| U5 plasticity cost | L&vR and vR&P M_α | identical cost functional | **Yes.** Charging plasticity is not new (Astra §3 confirmed). |
| U5 deficit-gated plasticity | DP's facilitation p_j | p_j(y_j + b_j) with a fixed band ↔ g(r_min − r_i) | **Partly.** The ultrastable logic (plasticity on when an essential variable leaves its range) is DP and Ashby. The difference is *what* the essential variable is: in DP it is the unit's own firing rate inside a designer-fixed band; in UDTN it is the unit's resource, which depends on whether its acquired output-side use continues. |
| Structure persists if it keeps being used | E&B node weight (degradation + reinforcement by revisiting) | s_ij ↔ N_w; q_ij ↔ the reinforcement term | **Close.** E&B's reinforcement is driven by *proximity in sensorimotor space* (familiarity); UDTN's is driven by *routed support from downstream use*. E&B also has an explicit attraction-to-familiar term, which UDTN does not. |
| Internal regulation shaping behavior | K&G | none: UDTN has no setpoint-derived reward and the policy gets no internal-state input | **Not by equations.** K&G has a reward derived from a setpoint, and UDTN does not. **But both read r.** K&G reads it as a global input to value learning, and UDTN reads it as a local plasticity gate. The difference lies in *where and how* r is read, not in *whether*, and it is an implementation property (named change 3). The behavioral discriminator with the information matched is SATISFICE in spec v1.1: UDTN stops searching once the shortfall clears, while K&G maximizes. |

**Comparison verdict (my judgment, for Astra to challenge).** With U-ACT, UDTN is a recombination of vO&W/E&S competition, L&vR costs and DP-style gating, and the v1 and v1.1 novelty claim for that version is withdrawn. Two elements remain candidates:
- **(N1)** Deficit-gated ultrastability whose essential variables are *acquired*: whatever structure currently has output-side use, instead of fixed firing bands.
- **(N2)** U-FUNC routing, if, and only if, it produces an intervention prediction that differs from U-ACT. The stimulation-only control in the spec below is that test: U-ACT predicts that raw stimulation of a pathway with no effect on output keeps it alive, and U-FUNC predicts it does not.

**A structural finding the program should know about.** As written, UDTN has **no path that carries credit from maintenance consequences back to the actions that caused them.** Support flows backward along synapses only, so an orienting circuit whose *environmental* effect keeps some pathway P supplied gets no support for doing so. The only way UDTN can produce a behavioral bias toward maintenance is the (N1) route: a resource deficit raises plasticity, and the behavior that results drifts until the deficit stops (Ashby's ultrastability). The bias therefore has to show up as **deficit-triggered search that stops once the dependency is satisfied**, not as a learned preference. This is a sharp, falsifiable signature, and it is what the reassignment spec tests. If Q-EXIST fails, so that no hand-built UDTN shows the switch, then the architecture can't express the motivating phenomenon and Track B should say so.

## 4. Substrate classification under Astra's frozen rule

- **Substrate (generic transformation and execution):** U1, U2 and U4 (the routing law itself), the S_i estimator, the U6 ledger arithmetic and the U5 functional form.
- **Declared state (organization-specific):** w, s, r, b and the realized routing pattern. Which pathways are essential is never written anywhere; it lives only in these values.
- **Must be shown:** the substrate runs on alternative contents, including failing ones. The same equations must apply to an organization whose acquired dependencies make it fail (it loses function or dies) with no special-casing. This goes into the G1 checks.
- **Supplied, and must be reported as supplied:** σ_in, r_min, the form of g, θ, τ_s and the sensorimotor environment. Named change 3 applies: the result can at most be dependency-specific regulation under fixed supplied dynamics.

## 5. What changed from framing note v1.1

- U-ACT has been renamed and its novelty claim withdrawn.
- U-FUNC is defined, with its limitation stated.
- The full ledger is written out.
- The credit-path gap is now stated openly.
- The relabel test against Track A is replaced, as Astra asked, by a declared mapping that preserves the causal dependencies, intervention access, information access and resource accounting.
- v1 and v1.1 of the framing note are unchanged.
