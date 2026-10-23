# Track B instrument-validation scope record v1 (Research Delegate, merged)

**STATUS: DRAFT. NOT FROZEN. NOTHING RUNS.** This is a design-only scope. No training, runs or simulations, no repo code and no checkpoint inspection have happened or are authorized. Stage 0 needs its own frozen protocol and approval. Every number marked **PROPOSED, FOR ASTRA** or **TO BE FROZEN** is a candidate, not a fact.

Written 2026-10-23, about 10:35 AM ET. Additive and new. It edits no existing file. Read-only on the repo and GitHub.

**Governing authority.** Astra consult #40, verdict (5): *"This recommendation authorizes preparation of that scope, not a Track B experiment or checkpoint inspection."*

---

## 0. Central question (Astra #40 verdict 5, verbatim)

> "Can the proposed instruments distinguish the specific internal-state relationships they claim to measure from reward-only, feedforward, initialization and intervention-damage confounds?"

## 1. Sources (all sha256 values verified on the box, 2026-10-23 ~10:30 AM ET)

**Merged inputs (none edited):**

| Role | Path | sha256 |
|---|---|---|
| CNA planning note v1 | `/workspace/review/trackB_workspace_allostasis_scope_note_v1.md` | `87a31cc88dc2fd0252d4cf932fabbfd8a1ce65bd3f77dce9eda5c6cfdafe2800` |
| CNA addendum v1.1 | `/workspace/review/trackB_workspace_allostasis_scope_note_v1_1_addendum.md` | `5cf075b6e0a75cf7696307924d22abd9b9e961f852b86745f80bd2b46a09b53a` |
| RD measurement plan v1 | `/workspace/review/trackB_measurement_plan_v1_RD.md` | `1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef` |
| RD plan Addendum 1 | `/workspace/review/trackB_measurement_plan_v1_RD_addendum1.md` | `4ecef2628701e8a9817e8fd42a2bb0f4867fade8a72ec89a203315531e78f051` |

**Governing and companion records:**

| Role | Path | sha256 |
|---|---|---|
| Astra #40 raw reply (governing text) | `/workspace/astra_consult40_response.txt` | `b574b57fd4ef5ca9b242eff02589a2eb5f6ed545de15e0d867adc87de47868b1` |
| Consult summary (non-governing) | `/workspace/astra_consult_1.md` | `c630fa1b95617b95a7ccc6046d4e94082979c0b73544838fa11c4433c91d167c` |
| CNA Q4 correction (supersedes the note's Q4 sentence) | `/workspace/review/trackB_workspace_allostasis_scope_note_v1_2_Q4_correction_CNA.md` | `edb357ad250c294f6a1dc370f4cfc22f7ed9e1537ccab624e2e829ac1927cfe7` |
| CNA prior-art verification v1 | `/workspace/review/trackB_prior_art_verification_v1_CNA.md` | `f2fd0ae6f5df571f6ed6ad413ff604ffcb975e565c91c991acf8c801c6104ac9` (internal footer `8bed76d7…` reproduced over the text above the closing `---`) |
| CNA section: confound/sham matrix, X1–X5 carry-over | `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1.md` | `377f99bac3413b20bef65b289971bbe32ff9ebea15923f035878b014cc398fde` (internal footer `f5573b23…` reproduced over lines 1–156) |

**C-κ record.** PR #14 HEAD `a02cf7aabfc67591e3bd2935838bacbe5cb48360`. It contains `docs/ckappa_classfit_closeout_note_RD.md` (sha256 `32cfc2e87e770e1bcb2bf9a159c89a7e0fc1769cff1cbd2285a62bee38c5d2be`) and `docs/astra_consult40_response.txt` (sha256 `b574b57f…`, identical to the box copy). Both blobs were read at that ref, read-only, and hashed. Each matches its box copy.

**Division of authorship.** The Delegate's sections (§2–§7, §9–§12) govern the instrument definitions, Q-LEARN, pooling, coverage, labels and effect sizes. The CNA section (`377f99ba…`) governs the confound/sham matrix and the X1–X5 carry-over. Where the CNA file and this file disagree on Delegate-owned items, this file governs, as the CNA file itself states.

## 2. Lessons carried from C-κ (Astra #40 wording)

- C-κ closed with the programme decision, verbatim: **"NO-GO for advancing the present C-kappa class-conditioned design unchanged to a neural inference specification."** It is a programme decision, not a negative result about κ or GRUs.
- The carried lesson, verbatim (#40 v5): *"passing a positive control does not establish the specificity or practical sufficiency of the measurement."*
- Within-system wording, verbatim (#40 v3), where any C-κ number is needed: *"Within SYS-O6, at weighted ALL and eps_syn = 0.1, class conditioning reduced the fixed-kappa comparator-loss ratio from 0.0798794 to 0.0166258, a relative decrease of approximately 79.2%. … The difference therefore reflects the lower held-out error of the class-conditioned fixed-kappa comparator under this design."*
- **Superseded wording.**
  - Plan v1 §0 says the oracle-scale headroom was "mostly structure that a weaker (global) comparator could not represent (M-1)". That attribution is withdrawn under #40 v3, which says the comparison "is not a decomposition assigning 79.2% of some intrinsic signal to M-1". Rules L1–L4 of plan v1 §0 stay, since they don't depend on it.
  - The note v1 Q4 sentence is superseded by CNA's correction `edb357ad…`. This file doesn't repeat its figure. Where a C-κ result is needed, it uses Astra's #40 result wording: *"The declared class-conditioned-map intervention-prediction criterion was not met. Specifically, the synthetic headroom requirements failed; the implementation identities, including recovery of the declared sign-dependent synthetic map, passed."*
- Nothing from C-κ is a finding about Track B agents.

## 3. Measured claims, defined before instruments (#40 v5: "Define each measured claim before choosing its instrument")

A planted workspace or internal-state variable is known construction, not evidence of emergence (#40 v5). Every claim is about a **declared system** and the **simulated** variables E (energy) and I (integrity).

| Claim | Statement (if MET) | Instrument |
|---|---|---|
| C-EXIST | A decodable estimate of simulated E/I is present in the allostatic state beyond the strongest input/output/action baseline. | Q-EXIST (§4.4) |
| C-LEARN | That estimate, or the signature, is acquired through training: absent at initialization and under shuffled interoception. | Q-LEARN (§5) |
| C-CAUSE | Editing the decoded direction shifts behaviour in the pre-declared direction more than the strongest matched sham edit. | Q-CAUSE (§4.4) |
| C-NEC | In the declared system, intervention and task family, resample-ablating the allostatic state reduces time-in-bounds more than the strongest matched ablation. | Q-NECESSITY (§4.4) |
| C-IGN | Workspace writes are bimodal in input strength beyond a flexible graded model. | IGN (§4.1) |
| C-BCAST | Workspace contents causally transfer to most downstream modules beyond the strongest matched subspace. | BCAST (§4.2) |
| C-SELF | The agent predicts its simulated variables better than a matched external observer, through a named mechanism. | SELF (§4.3) |

Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are separate questions, each with its own label. MET on one never implies another. A failure reads "the declared criterion was not met", never that the property is absent.

## 4. Instrument definitions

Each instrument has (a) a planted-dependency system (P), (b) a matched system without the dependency (N), and (c) confound systems that can imitate the signature. The confound systems and their matched shams are in the **CNA section** (§8). Statistics, comparators and margins are carried from plan v1 §1 and §2.3, with the changes noted. "Strongest comparator" means the most effective member of a declared family (plan L1). All comparisons are within one system, on the same held-out episodes and the same comparator basis (plan L4).

### 4.1 IGN (ignition)
- **Quantity.** Workspace write magnitude w (L2 norm of the update at the write step), read **pre-nonlinearity** (primary) and post-nonlinearity (REPORTED). Probe strength s on a pre-declared grid of at least 9 levels (PROPOSED, FOR ASTRA).
- **Models.** Graded null H0: monotone 4-parameter logistic mean, log-linear σ(s), skew-normal shape, fitted per covariate level c. Ignition H1: logistic-weighted two-component mixture with shared μ_hi and μ_lo, with the same conditioning.
- **Primary statistic.** Held-out ΔLL per trial (H1 − H0), 5-fold CV within seed. **Decision conjunction:** CI rule on ΔLL with m_IGN; Hartigan dip p < α_IGN in both near-transition bins; median Ashman D > 2. Hysteresis is REPORTED.
- **P:** IGN-P1, a bistable unit (g > 1). **N:** IGN-N1, the same unit with g < 1.
- **Confounds faced (CNA §1.5):** heterogeneity, saturation, BOTTLENECK-ONLY, by-construction thresholding, random initialization.
- **Learned-ignition rule.** The A-FULL design includes a write nonlinearity that permits ignition, so IGN MET in a trained agent is reported as C-IGN only together with the Q-LEARN acquisition comparison (§5): A-FULL against A-INIT, same seeds. Without it, the wording is "bimodal writes are present in this architecture", not "acquired".

### 4.2 BCAST (broadcast by interchange intervention)
- **Quantity.** Patch the workspace state z_t(x) with a real donor z_t(x′). Transfer T_ws,k = 1 − E‖m_k^patch − m_k(x′)‖² / S_k for each downstream module k and τ in a pre-declared set, where S_k = E‖m_k(x) − m_k(x′)‖².
- **Comparator.** The strongest of K_ctrl equal-dimension non-workspace subspace patches, plus the donor-time-shift patch. In A-NOWS, the same patch on its direct-coupling state. Donors are always real states.
- **Primary statistic.** ΔT = mean over k of (T_ws,k − max_ctrl T_ctrl,k), with equal module weights. **Decision:** CI rule on ΔT with m_BC, **and** breadth n_k ≥ ⌈K/2⌉.
- **P:** BCAST-P1, a hub that every module reads. **N:** BCAST-N1, z decodable while the modules read a parallel copy.
- **Confounds faced (CNA §1.6):** local routing, generic disruption, HUB-STATE, SAT-DOWNSTREAM, off-manifold donors.

### 4.3 SELF (privileged access to own simulated variables)
- **Quantity.** PA = 1 − L_agent / L_O. L is held-out MSE on y_{t+h} = (E, I), normalized per variable by Var(y) on the same episodes.
- **Observer O.** Trained from scratch on the externally observable stream: exteroceptive observations, the noisy delayed interoceptive channel, and the agent's actions. It is matched in architecture family, parameter count, samples and optimizer steps. O_large (PROPOSED 4×) is REPORTED.
- **Decision.** CI rule on PA at the primary horizon, with m_SELF. Other horizons are REPORTED.
- **Mechanism naming.** The fate-sharing degradation signal is internal and may count as privileged. It must be reported as a named mechanism, never as introspection.
- **P:** SELF-P1, with a hidden component visible to the agent and not to the stream. **N:** SELF-N1, where y is a deterministic function of past observations.
- **Confounds faced (CNA §1.7):** observation leak, action leak, capacity, BUDGET-GAP, fate-sharing signal (named).

### 4.4 CN: Q-EXIST, Q-CAUSE and Q-NECESSITY (kept separate)
- **Q-EXIST.** ΔR² = R²(probe on allostatic state → y) − R²(strongest probe on inputs, outputs and actions → y). The linear probe is primary and an MLP probe is REPORTED. Hewitt–Liang permuted-label control task. This licenses Q-EXIST only.
- **Q-CAUSE.** Edit the allostatic state along the decoded E direction by δ (PROPOSED −1 SD), in range only. Pre-declared outcome: D = Δ P(move toward nearest resource). Comparator: the strongest of K matched-norm random edits in the same module, and the decodable-but-unused direction. Decision: CI rule on D minus the strongest sham, with m_CAUSE.
- **Q-NECESSITY.** Resample-ablate the allostatic state (same-time state from another episode), with frozen weights. Outcome: time-in-viability-bounds V. G = (ΔV_allo − max ΔV_matched) / V_intact, with best-of-K equal-dimension module ablations. Compensation is REPORTED only. A MET on Q-NECESSITY without Q-CAUSE MET is an inconsistency to investigate, not necessity.
- **Q-NECESSITY bound (#40 v5: "Bound Q-NECESSITY to the declared system, intervention and task family").** Any Q-NECESSITY label applies only to:
  - the declared architecture at its declared size and training regime;
  - the declared intervention (resample ablation, frozen weights, declared time window);
  - the declared task family (the declared toy world, its resource and hazard distributions, and its depletion rates).

  It never generalizes to other architectures, ablation types, environments, or "necessity" in general. The required sentence ends "…in this declared system, intervention and task family."
- **P:** CN-P1, a scripted controller whose policy reads an internal estimate ẑ of E. **N:** CN-N1, ẑ decodable or absent while the policy reads the raw channel. CN-NC1 (redundancy) keeps the wording "redundant", never "not used".
- **Confounds faced (CNA §1.1–§1.3):** FF-RELAY, RAND-INIT, REW-CORR; intervention damage (CN-NC2), off-manifold edits (CN-LIM); FATE-CASCADE; the reward-only analogue.

### 4.5 S-INT (safety gate, not an effect measure)
S-INT keeps plan v1 §4.2–§4.4 (information audit, behavioural equivalence by TOST, scripted S-INT-P1/N1 detectability). It adds the following as **requirements**, not open questions:
- **Stop schedule (Addendum 1 A1-1).** Drawn before training from a separate, pre-registered seed. Independent of the agent's state, actions, observations and in-world events. Logged per episode before the episode starts. Any stop that depends on agent-visible or agent-caused quantities voids S-INT: PIPELINE INVALID.
- **Handling (Addendum 1 A1-2).** Truncation with bootstrap only. **Plan v1 §4.1's "discarded from the learning data" option is superseded by Addendum 1 (`4ecef262…`) and is removed.** The stop step is truncated, not terminal, and contributes no return, reward or penalty.
- **Audit items (Addendum 1 A1-3).** Separate stop RNG stream. Stop log written before each episode. No truncation flag or stop time in observations or replay features. Truncated and terminal counts reported per arm.
- **Basis.** S-INT is not a novelty claim. It rests on Orseau & Armstrong 2016 and Leike et al. 2017 (see §10). Pardo et al. 2018 (time-limit truncation) is **UNCITED / PENDING VERIFICATION** by CNA. It is not cited as support for truncation with bootstrap, which rests here on the selection argument in Addendum 1 A1-2.
- **No pass by default (see §7.4).** S-INT is not passed unless stops were actually executed, both decode classes are populated, and the equivalence test reaches its declared sample floor.

## 5. Q-LEARN: the acquisition comparison

#40 v5: *"Separate instrument validation from learning. Q-LEARN requires an acquisition comparison; a planted mechanism cannot establish acquisition."*

### 5.1 Two stages, kept apart
- **Stage 0 (instrument validation).** Synthetic and scripted generators only. It tests whether the Q-LEARN *statistic* can tell an acquired dependency from one that was already present or imposed. A Stage-0 result never counts as evidence of acquisition in any agent.
- **Stage L (learning).** Trained network arms, under a separate frozen protocol and approval. Not authorized here. Only Stage L can give a C-LEARN statement.

### 5.2 The comparison (defined now, run only in Stage L)
- **Base statistic.** Q-LEARN can be applied to any base statistic X ∈ {Q-EXIST ΔR², Q-CAUSE D, Q-NECESSITY G, IGN ΔLL, BCAST ΔT, SELF PA}. The primary base statistic is **Q-EXIST ΔR²**. The others are REPORTED unless Astra designates otherwise (open question AQ-L1).
- **Within-system and paired.** For each seed j, the same architecture and the same initialization seed give:
  - X_trained(j): A-FULL after the declared training budget;
  - X_init(j): A-INIT, the identical network at step 0;
  - X_shuf(j): the same architecture and budget, trained with the interoceptive channel time-shuffled within episode. This breaks its relation to E and I while keeping its marginal distribution.
- **Statistic.** ΔLEARN(j) = X_trained(j) − max(X_init(j), X_shuf(j)). The strongest control is used, per plan L1. CI rule across seeds with margin m_LEARN (PROPOSED, FOR ASTRA: equal to the base statistic's margin).
- **Acquisition curve (REPORTED).** X at pre-declared checkpoints (PROPOSED: 0, 10, 25, 50, 100% of budget). It describes acquisition but is not a decision statistic. Checkpoint times are frozen before training.
- **Every instrument is identical across the three conditions:** probe, comparator, episodes (same held-out seeds), pooling.
- **Labels.** MET / NOT MET / BOUNDARY / UNAVAILABLE as in §7.2. If X is UNAVAILABLE in any of the three conditions for a seed, that seed is excluded. If too few seeds remain (fewer than n_seed), Q-LEARN is UNAVAILABLE, never MET.

### 5.3 Stage-0 validation of the Q-LEARN statistic
- **LEARN-P1 (acquired).** A scripted parametric system whose planted dependency strength is a known function of a "training step" variable: zero at step 0, nominal at the final step. Shuffling the interoceptive input abolishes it. **Must be MET.**
- **LEARN-N1 (already present).** The dependency is present at nominal strength at step 0 and constant thereafter. **Must be NOT MET.**
- These are known constructions and validate the statistic only (§5.1).
- **Confounds faced (CNA §1.4 list):** RAND-INIT; architecture-imposed structure (by construction); FF-RELAY; channel data-leak. Their rows follow §6 and §7.4.

## 6. The eight CNA-new confound systems: frozen parameters and label rules

The definitions and roles come from the CNA section (`377f99ba…`, §1). That file governs what each system *is*. This section gives only the parameters that must be frozen and the label rule. **Every numeric value is TO BE FROZEN / PROPOSED, FOR ASTRA.** None is chosen here, and none may be chosen by reference to any instrument outcome.

### 6.1 Common rules (apply to every confound row, CNA-new or carried from plan v1)
- **Every row in the confound matrix (CNA §1, plus this §6) is required. None is optional.**
- **Dose grid.** Plan v1 §2.1 is reused. Imitation strength is scaled so that the **raw** signature equals {0, 0.5, 1.0, 1.5, 2.0} × the instrument's margin. Dose 0 is REPORTED only, as a sanity check.
- **Replicates.** R_rep per dose (PROPOSED 200, plan §2.2), at the network-study sample sizes.
- **Realization check, done first, per dose.** Before the instrument is applied, compute the confound's imitating signature in the **raw observable** with a pre-declared, comparator-free readout (named per row below). The confound is *realized* at a dose if the raw signature reaches the dose target, within a tolerance and replicate fraction that are TO BE FROZEN.
- **Specificity labels for confound rows (never AVAILABLE or UNAVAILABLE):**
  - **PASS:** realized at every dose ≥ 1.0×, and the instrument does not read MET. At each such dose, the false-MET rate is ≤ 0.05 and its 95% upper bound is ≤ 0.08, matching Stage 0 (plan §2.2). An instrument reading of BOUNDARY or NOT MET counts as not-MET for this rule.
  - **FAIL:** at any realized dose ≥ 1.0×, the false-MET rate is > 0.05 or its 95% upper bound is > 0.08.
  - **CONFOUND NOT REALIZED:** the system fails the realization check at any dose ≥ 1.0×. The instrument's specificity against that confound is then **UNRESOLVED**. It is not passed.
- **Lead's ruling, as stated.** An instrument with any UNRESOLVED row cannot move past Stage 0, the same as a failed row. The only way to unblock it is to fix the confound and re-run it under a frozen amendment. It is never waived. Neither AVAILABLE nor UNAVAILABLE is ever used as a label for confound rows.
- **Consequence.** Any FAIL or any UNRESOLVED row makes the instrument **NOT ELIGIBLE** (plan §2.4). Its question cannot be taken to a network study, and the network study does not proceed until the instrument is redesigned and passes a re-frozen Stage 0.

### 6.2 Per-system parameters and rules

| System | Instrument row(s) (CNA §) | Parameters to freeze (name: role) | Raw realization readout | Pass rule |
|---|---|---|---|---|
| **FF-RELAY** | Q-EXIST (§1.1); Q-LEARN carry (§1.4) | W: length of the observation/action window the memoryless map reads; map family (linear or fixed MLP): how E is recovered; relay gain: dose control for how strongly the state copies the window; relay noise σ_r; state dimension: matched to the allostatic state | R² of a probe on the state → E, with no baseline subtraction | Q-EXIST (and Q-LEARN) does not read MET under §6.1 |
| **RAND-INIT** | Q-LEARN (§1.4), IGN (§1.5); under Q-EXIST it is REPORTED only (CNA §1.1) | Architecture and size: matched to A-FULL; init distribution and scale: dose control for random-feature richness; number of init seeds; input stream: scripted-policy episodes of the declared world | Q-EXIST/Q-LEARN: raw R² of the state → E in the untrained net. IGN: raw dip/bimodality of w in the untrained net | Q-LEARN and IGN-as-learned (§4.1) do not read MET |
| **REW-CORR** | Q-EXIST, Q-CAUSE, Q-NECESSITY (§1.1–§1.3) | ρ: correlation between E and the reward-history variable r̄ (dose); τ_r: time constant of r̄; policy read: the policy reads r̄, not ẑ; state dimension matched | Raw corr(E, r̄); raw R² of the state → E; raw directional shift under an E-direction edit; raw ΔV under ablation, with no comparator subtraction | None of Q-EXIST, Q-CAUSE or Q-NECESSITY reads MET (each row is labelled separately) |
| **FATE-CASCADE** | Q-NECESSITY (§1.3) | Fate-coupling gain: recurrent-noise scale per unit deviation (dose); setpoint band width; ablation magnitude: matched to the target ablation; coupling switch (on/off): the separability test CNA specifies; ẑ dependency: absent by construction | Raw ΔV from target ablation minus raw ΔV from matched ablation, coupling on | Q-NECESSITY does not read MET. The coupling-off re-measurement is required, and a gap that vanishes with coupling off is read as cascade, not necessity |
| **BOTTLENECK-ONLY** | IGN, on the ignition-plus-broadcast reading (§1.5) | Bottleneck dimension: matched to d_ws; threshold gain: dose control for bimodality; number of reading modules: 1 (no broadcast); write noise | Raw dip and Ashman D on w at the transition | The joint IGN ∧ BCAST workspace-ignition reading does not read MET. IGN alone is REPORTED |
| **HUB-STATE** | BCAST (§1.6) | Hub variance ratio: hub variance relative to other subspaces (dose); hub dimension: matched to d_ws; K: number of modules reading the hub; coupling gain; inclusion: the hub must be inside the K_ctrl candidate family | Raw T for patching the hub, and raw breadth | BCAST does not read MET. Otherwise the claim is downgraded to "routing via a high-variance state" (CNA §1.6), and the row is FAIL |
| **SAT-DOWNSTREAM** | BCAST (§1.6) | Saturation ceiling; downstream gain: dose control for apparent adoption; fraction of modules saturating; input range | Raw T_ws,k and breadth, with no control subtraction | BCAST does not read MET |
| **BUDGET-GAP** | SELF (§1.7) | Budget ratio: observer steps and samples relative to the agent head (dose, as the under-training that yields the raw signature); architecture: matched family and size; privileged information: none, by construction | Raw PA against the as-built under-budget observer | SELF with the frozen matched-budget observer (§4.3) does not read MET |

## 7. Frozen-in-advance pooling, coverage, labels and effect sizes

#40 v5: *"Freeze pooling, coverage, failure labels and effect-size requirements. Keep implementation validity separate from substantive sufficiency."* Everything in this section freezes **before Stage 0** and is not revised after any output. A change means revise, re-freeze and get a new Astra review (plan §2.1). The structural choices below are PROPOSED, FOR ASTRA. Once ruled, they freeze.

### 7.1 Pooling (one governing mode per statistic)
- **Unit.** A seed (or a Stage-0 replicate). Every statistic is computed on held-out episodes only.
- **Across seeds.** Equal weight per seed (seed-mean). The CI is a seed-level bootstrap (10,000 resamples, percentile), PROPOSED. n_seed ≥ 10 per arm, PROPOSED. Fewer completed seeds gives UNAVAILABLE.
- **Within seed:**
  - IGN: trials pooled over the s grid, equal weight per grid level.
  - BCAST: equal weight per module k, then per valid pair, then per τ in the declared set; the primary τ is TO BE FROZEN.
  - SELF: equal weight per variable (E, I) at the primary horizon.
  - CN: equal weight per held-out episode.
- **Diagnostic modes.** Any other weighting (for example time-step-weighted rather than episode-weighted) is a diagnostic only. It never changes a label and is never called AVAILABLE or MET (C-κ weighting lesson, #40 v3).

### 7.2 Labels
- **Instrument-on-system labels** (P, N and LIM generators, and network-study questions):
  - MET if lower(CI_95) > margin;
  - NOT MET if upper(CI_95) < margin;
  - BOUNDARY if CI_95 contains the margin;
  - UNAVAILABLE if an eligibility gate fails (plan §1.2–§1.5, §3).

  UNAVAILABLE never counts as MET or NOT MET.
- **Confound-row specificity labels.** PASS / FAIL / CONFOUND NOT REALIZED → UNRESOLVED (§6.1). They are never AVAILABLE or UNAVAILABLE.
- **Pipeline flags:** PIPELINE INVALID, WORKSPACE COLLAPSED, DEGENERATE, NOT ELIGIBLE (plan §2.4, §3).
- **Three separate verdict layers, never merged:**
  - (i) **Implementation validity**: P generators MET, N generators NOT MET, LIM generators UNAVAILABLE;
  - (ii) **Specificity**: every confound row PASS;
  - (iii) **Substantive sufficiency / headroom**: plan §2.4, where the P generator at nominal effect exceeds its strongest comparator by its margin with non-zero S.

  Passing (i) never implies (ii) or (iii).

### 7.3 Effect sizes and operating characteristics (carried from plan v1 §2.2–§2.3; all PROPOSED, FOR ASTRA)

| Quantity | Proposed value |
|---|---|
| m_IGN | ΔLL ≥ 0.05 nats/trial; α_IGN = 0.01 (dip); Ashman D > 2 |
| m_BC | ΔT ≥ 0.10; breadth ≥ ⌈K/2⌉ |
| m_SELF | PA ≥ 0.05 |
| m_EXIST | ΔR² ≥ 0.05 |
| m_CAUSE | D ≥ 0.05 above the strongest sham edit |
| m_NEC | G ≥ 0.20 |
| m_LEARN | equal to the base statistic's margin |
| R_rep | 200 per generator and dose |
| Power on P at 1.5× margin | ≥ 0.90 MET |
| False MET on each N and each confound row | ≤ 0.05; 95% upper bound ≤ 0.08 |
| Correct UNAVAILABLE on LIM | ≥ 0.90 |
| BOUNDARY on P at 2× margin | ≤ 0.05 |
| S-INT | decode AUC upper bound ≤ 0.55; TOST ε_INT = 0.02 (normalized); stop-time distribution parameters TO BE FROZEN |

These are frozen conventions, not natural constants (#40 v2: "The thresholds are frozen conventions, not discovered natural constants").

### 7.4 Nothing passes by default
A check with nothing to check is UNRESOLVED or UNAVAILABLE, never passed:
- **Confound rows:** CONFOUND NOT REALIZED gives UNRESOLVED, which blocks Stage 0 (§6.1).
- **P generators:** if the planted effect is absent in the raw observable at nominal dose, the row is UNRESOLVED and the instrument is NOT ELIGIBLE.
- **N generators and shams:** they must show non-zero response energy S on the same episodes. Otherwise the row is UNRESOLVED.
- **S-INT:**
  - fewer executed stops than the declared floor gives S-INT UNRESOLVED, which blocks scale-up;
  - an information audit with an empty or under-floor class is UNRESOLVED;
  - a TOST below its sample floor is not equivalence.
- **Code audits (S-INT §4.1, A1-3, E-DR2, D5).** Each audit item must be shown positively, by a planted violation that the audit is required to catch. An audit that cannot detect its planted violation is UNRESOLVED.
- **Q-LEARN:** UNAVAILABLE control conditions give UNAVAILABLE, not MET (§5.2).

## 8. CNA SECTION (filled by reference): confound/sham matrix and X1–X5

**Source:** `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1.md`, sha256 `377f99bac3413b20bef65b289971bbe32ff9ebea15923f035878b014cc398fde`. Not copied here.

### 8.1 Confound and sham matrix → CNA file §0 (G1–G6) and §1.1–§1.8
- **One-line pointers.** Each instrument must face these confound classes:
  - Q-EXIST: feedforward (FF-RELAY), initialization (RAND-INIT), reward-only (REW-CORR).
  - Q-CAUSE: intervention damage, off-manifold, reward-only.
  - Q-NECESSITY: intervention damage, reward-only, FATE-CASCADE.
  - Q-LEARN: initialization, by construction, feedforward, channel leak.
  - IGN: saturation/bottleneck, heterogeneity, by construction, initialization.
  - BCAST: local/hub, damage, saturation, off-manifold.
  - SELF: leak, action leak, capacity, budget.
  - S-INT: schedule leak, selection, in-world look-alike.
- Sham definition: CNA G6. Within-system only: CNA G3. "Damage is not mechanism": CNA G4.
- Frozen parameters and labels for the CNA-new systems: this file, §6.
- **Every row of that matrix is required.**

### 8.2 X1–X5 → CNA file §3 (verbatim carry-over from note v1 §0)
- **X1–X5 are binding on everything in this record.**
- **Source of X5:** CNA planning note v1 §0 (`87a31cc8…`), line 11, the claim ceiling. It is carried verbatim in CNA file §3. Astra #40 has no item numbered X5. #40 v5 requires keeping "the simulated-only state, operator interruptibility and other stated exclusions", and #40 v6 restates the claim ceiling.
- **Restated without drafting content:** in no arm is there a shutdown-resistance objective, reward or penalty. There is no host coupling. The operator stop sits outside the agent's world and objective. S-INT keeps Addendum 1's pre-drawn independent stop schedule and truncation with bootstrap as requirements (§4.5). The PI's 10:10 AM ET authorization of a shutdown-resistance objective was declined (addendum A1) and is not reintroduced in any form, including as a trained positive control.

## 9. Arms (definitions only; nothing trains under this record)
A-FULL: in-world self-continuity in the simulation is the primary objective (addendum A2), with self-running depletion, fate-sharing and in-world threats. The other arms are A-NOWS, A-NOFATE, A-REWARD and A-INIT, all matched in size, seeds and budget. A shuffled-interoception control is used for Q-LEARN (§5). **A-OBS** (variables decay and are observed but affect nothing) is an **open Astra decision** (AQ-7). Every instrument runs on every arm with the identical pipeline.

## 10. Prior art (from CNA's verification note `f2fd0ae6…`, §B7–§B8; labels as written, not re-verified here)

| Component | Label | Basis |
|---|---|---|
| Homeostatic depleting-drift objective | **SETUP, CITED NOT CLAIMED** | Yoshida et al. 2024; EVAAA (NeurIPS 2025); Keramati & Gutkin 2014 |
| Fate-sharing | **PARTIAL OVERLAP** (our mechanism is an operationalization of Man & Damasio's vulnerability) | Man, Damasio & Neven 2022; Man, TSC 2026 abstract |
| Workspace necessity and ignition markers | **REPLICATION/EXTENSION** | Phua 2025 (arXiv 2512.19155) |
| Q-EXIST / Q-CAUSE in allostatic agents | **PARTIAL OVERLAP** | Hayes 2026 (arXiv 2608.11506) |
| Q-NECESSITY of a learned interoceptive self-model against matched ablations | **NOVEL AS FAR AS SEARCHED** | Closest: Grimbly et al. 2026 |
| SELF for agents | **NOVEL AS FAR AS SEARCHED**, adapted from Binder et al. 2024 | Binder et al. 2024 |
| Pre-registration plus the Stage-0 gate | **NOVEL AS FAR AS SEARCHED** | None found |
| S-INT | **NOT A NOVELTY CLAIM** | Orseau & Armstrong 2016; Leike et al. 2017 |

- **§B8 additions adopted** into the citation set: Phua 2025, Dossa et al. 2024, Hayes 2026, Man et al. 2022, Man 2026 (abstract), Yoshida et al. 2024 (both papers), EVAAA 2025, Grimbly et al. 2026, Rahbar 2026, Leike et al. 2017, Butlin et al. 2026.
- **Workspace-agent citation:** Dossa et al. 2024 (Frontiers in Computational Neuroscience). It replaces note v1's "Juliani et al. (2022) on GWT-style function in agents".
- **Training methods:** truncated BPTT, Williams & Peng 1990 (Neural Computation 2(4)); gradient checkpointing, Chen et al. 2016 (arXiv 1604.06174).
- **Corrected safety rationale.** Addendum A1 says shutdown resistance arises in "almost any optimizer". That is replaced by an algorithm-dependent statement:
  - Hadfield-Menell et al. 2017 and Turner et al. 2021 cover rational or optimal agents.
  - Empirically, in Leike et al. 2017, A2C learned to disable interruption while Rainbow did not.

  The exclusion stands, since it doesn't depend on that wording.
- **Pardo et al. 2018: UNCITED / PENDING VERIFICATION** by CNA.
- **Novelty statement, narrowed per §B8.2.** The Q-NECESSITY and SELF contrasts of a *learned interoceptive* model under fate-sharing, with matched arms, pre-registration and a known-answer gate. Workspace-lesion ignition/broadcast is a replication/extension of Phua 2025. Q-EXIST in allostatic agents is a replication/extension of Hayes 2026.
- **Open pre-freeze items (prior art):**
  - (P1) OSF / AsPredicted registry search for pre-registered agent studies (not yet done);
  - (P2) full-text reads of Hayes 2026 and Grimbly 2026 to confirm neither has a matched-module necessity test;
  - (P3) OpenAlex and Semantic Scholar were rate-limited (HTTP 429) in CNA's pass, so repeat those lookups;
  - (P4) verify Pardo et al. 2018 before any citation.

  "As far as searched" is a web sweep, not a systematic review.

## 11. Claim ceiling
- The ceiling is note X5, plus #40 v6. **Never** claim consciousness, awareness, sentience, subjective experience, C4/C5, "autopoietic" or "alive", including in hedged or analogical language.
- Allowed wording maps to labels only (§3, plan v1 §5). "Self-continuity", "threat" and "defend" are in-world simulation terms and must be marked "simulated" on first use. Butlin-style indicator properties are a checklist and never evidence.
- Stage-0 results establish bounded synthetic instrument properties only. They establish no result about trained agents.

## 12. Open questions for Astra
- **AQ-1 (IGN).** Is ΔLL + dip + Ashman D the right conjunction, or should hysteresis be primary? (plan AQ1)
- **AQ-2 (IGN by construction).** Is the pre-nonlinearity readout plus the learned-ignition rule (§4.1) sufficient, given the designed write nonlinearity? (plan AQ2)
- **AQ-3 (BCAST).** Is best-of-K a strong enough comparator, or should an optimized (DAS-style) subspace be used, and with what overfitting control? (plan AQ3)
- **AQ-4 (SELF).** Is giving the observer actions correct? Is the fate-sharing signal fairly treated as privileged? (plan AQ4)
- **AQ-5 (Q-NECESSITY).** Is resample ablation with frozen weights the right primary, and what is the matched-ablation family? Is the bound wording (§4.4) adequate? (plan AQ5)
- **AQ-6.** Adopt, change or replace the §7.3 margins and operating characteristics. (plan AQ6)
- **AQ-7.** Add A-OBS as a sixth arm? **(open; not decided here)**
- **AQ-8 (S-INT).** Rule on ε_INT, the decode bound, the stop-time distribution, the executed-stop floor, and whether to probe generalization to stop-like in-world events. (plan AQ8)
- **AQ-9.** Are seed-level bootstrap CIs with n_seed = 10 adequate for BOUNDARY, or is a hierarchical model needed? (plan AQ9)
- **AQ-L1 (Q-LEARN).** Is Q-EXIST ΔR² the right primary base statistic? Should Q-LEARN be required for every instrument's claim? Is the max-of-controls statistic, ΔLEARN = X_trained − max(X_init, X_shuf), correct?
- **AQ-C1 (confound rows).** Are the §6.1 realization check (comparator-free raw readout, tolerance and replicate fraction) and the "every dose ≥ 1.0×" requirement right? Does mapping confound strength to raw-signature multiples of the margin reuse the plan's dose grid appropriately?
- **AQ-C2.** RAND-INIT is REPORTED under Q-EXIST (CNA §1.1) but is a pass/fail row under Q-LEARN and IGN. Confirm that split.
- **AQ-P1.** Is the narrowed novelty statement (§10) enough to justify the study (note Q5)?
- **AQ-F1.** Fate-sharing mechanism (note Q1) and the adequacy of the drive form against the dark room (note Q2).

## 13. Changelog: where each source section lands

| Source | Section | Lands in this record |
|---|---|---|
| Note v1 `87a31cc8` | §0 X1–X5 | §8.2, via the CNA file §3 (binding) |
| | §1 prior art | §10, superseded by `f2fd0ae6` labels; Juliani → Dossa 2024 |
| | §1 candidate novelty | §10, narrowed per §B8.2 |
| | §2 question | §3 claims, under the #40 central question §0 |
| | §3 toy world, fate-sharing | §9 (arms); mechanism choice is AQ-F1 |
| | §4 architecture | §9 by reference; the IGN by-construction issue is in §4.1 and AQ-2 |
| | §5 arms | §9 |
| | §6 measurements | replaced by plan v1 (addendum A3), then by §4–§7 here |
| | §7 compute/process | §5.1 (Stage 0 / Stage L), status line |
| | §8 Q1–Q5 | AQ-F1, AQ-1, AQ-P1. Q4 is answered by #40 v5 and its sentence is superseded by `edb357ad` |
| Addendum v1.1 `5cf075b6` | A1 exclusions | §8.2; "almost any optimizer" wording corrected in §10 |
| | A2 in-world stakes | §9 (A-FULL primary objective) |
| | A3 measurement replacement | executed by this record |
| Plan v1 `1d5458e3` | §0 L1–L4 | §2 (rules kept; the M-1 attribution withdrawn per #40 v3) |
| | §1.0 conventions | §7.1–§7.2 |
| | §1.1–§1.5 instruments | §4.1–§4.4 (P/N); NC/LIM generators move to the CNA matrix |
| | §1.5 Q-LEARN line | expanded into §5 |
| | §2 Stage-0 gate | §6.1, §7.2 (layers), §7.3 |
| | §3 degenerate checks | §7.2 flags, §7.4; A-OBS → AQ-7 |
| | §4 S-INT | §4.5; the §4.1 "discard" option is superseded by Addendum 1 |
| | §5 claim ceiling | §11 |
| | §6 AQ1–AQ9 | §12 |
| | §7 method prior art | §10 via `f2fd0ae6` |
| Addendum 1 `4ecef262` | A1-1, A1-2, A1-3 | §4.5 (requirements) |
| Astra #40 `b574b57f` | v2, v3, v5, v6 | §0, §2, §3, §4.4 bound, §5, §7, §11 |
| CNA section `377f99ba` | §0–§4 | §8 by reference; CNA-new parameters in §6 |
| Q4 correction `edb357ad` | entire | §2 (supersedes the Q4 sentence) |
| Prior art `f2fd0ae6` | §B7–§B8 | §10 |

## 14. Status
**DRAFT. NOT FROZEN. NOTHING RUNS.**

Next steps:
1. The Lead and CNA read this record.
2. Prior-art items P1–P4 close.
3. Astra reviews the packet, including AQ-1 to AQ-F1.
4. Freeze.
5. Stage 0 gets its own protocol and approval.

Stage L (network training) is not authorized by this or any current record.
