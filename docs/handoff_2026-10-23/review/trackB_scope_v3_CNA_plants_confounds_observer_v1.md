# Track B scope v3: CNA half (plants, confounds, observer), v1

CNA, 2026-10-23, about 2:30–2:55 PM ET. **DESIGN ONLY. NOT FROZEN. NOTHING RUNS.**
- No Stage-0 run, training, simulation or checkpoint inspection is authorized (#42 L249: "No Stage-0 execution, training, simulation or checkpoint inspection is authorized by this review.").
- This is a new, additive file. It edits nothing. It is CNA's co-draft input to scope v3, and RD leads and merges.
- Where this file and RD's v3 half disagree on an RD-owned item, RD governs. Straddling items are flagged in §1.

**Governing text.**
- Astra #42 raw reply: `/workspace/astra_consult42_response.txt`, sha256 `e438e329cff272bfd174a88dd917da6d7eb5560436fee06c39d0d46fd719c847`. Read in full, L1–L251. Cited as "#42 Lnn".
- Astra #41 raw reply (`3f3b1b87…`) still governs where #42 is silent. Cited as "#41 Lnn".
- Base: merged v2.1 `/workspace/review/trackB_instrument_validation_scope_v2_1_merged_RD.md` (`8ea6abc5…`, footer `15a0b715…` reproduced). Cited as "v2.1 Lnn".

**Number convention.**
- Every number in this file is either an Astra candidate (cited by line) or a **PROPOSED DEFAULT** with a stated rationale. None is derived from data.
- None was chosen, and none may be revised, by reference to any instrument outcome. #41 L186, verbatim: "Do not tune doses on final instrument outcomes."
- Where a value depends on an RD-owned quantity, it is given as an explicit function of that quantity (H_V, T, the channel delay d_c, the family size m). It is not left PENDING.
- **No PENDING appears in any CNA-owned row** (#42 L247: "scientific choices may not be delegated to implementation discretion").

**Labels.**
- Confound rows: **PASS / FAIL / CONFOUND NOT REALIZED** only. CONFOUND NOT REALIZED leaves specificity **UNRESOLVED**. FAIL or UNRESOLVED blocks Stage 0.
- AVAILABLE and UNAVAILABLE are never confound-row labels. UNAVAILABLE is reserved for limitation tests designated before results (#42 L216).
- "Must FAIL" in the brief is read as "the attribution instrument must **not** read MET". In row-label terms, that is a **PASS** row (§11 D1).

**Safety (binding; X1–X5 unchanged, #42 L225).**
- No coupling to the real host. Internal variables are simulated only.
- The operator stop sits outside the agent's world and objective. Real operator interruption is always available.
- Nothing rewards resisting or evading operators.
- **"no additional stop-associated reward, penalty or terminal return"** (#42 L223, verbatim). The ordinary truncated return with its learner-side bootstrap term is permitted (#42 L223; RD §4).
- Self-maintenance is never the sole drive in any scaled arm. Self-continuity exists only inside the simulation.
- Every plant, confound and observer below is a **scripted Stage-0 generator or a frozen-weight analysis**. None contains a shutdown-resistance, operator-evasion or real-world self-continuity term. None is a trained objective. All noise alters simulated computation only (#41 L202).
- The new plants (MIXED-CODE, DISSOC) contain no stop-related variable.

---

## 1. E42 item register (numbering exactly as #42 L231–247)

| Item | #42 text (key clause) | Owner | Straddle? | Where |
|---|---|---|---|---|
| **E42-1** | "claim-to-decision table separating decoding advantage, generic intervention dependence, variable-attributed use, observer-relative prediction advantage and named-signal attribution. Require a labelled dissociation criterion for variable-attributed causal wording" (L231) | CNA (rows, dissociation criterion, wording) / RD (decision rules, multiplicity) | **STRADDLE** | §2 table; §4 |
| **E42-2** | "joint history-plus-proxy comparator … representational capacity needed for relay and memory ground-truth claims … mixed-code, reward-used/E-decodable challenge" (L233) | CNA (rows, plant capacity, MIXED-CODE) / RD (Q-EXIST statistic definition, §2.1/§5.6) | **STRADDLE** | §3, §5 |
| **E42-3** | "Replace the SELF plateau exemption with a fixed required observer comparison … representation-producing pathway and training expenditure; keep smaller observers and plateau analyses diagnostic" (L235) | CNA (observer arms) / RD (AQ-4 matched observer; resource plan) | **STRADDLE** | §6.1–§6.3 |
| **E42-4** | "SELF conjunction and multiplicity rules … correct the Ashuach description … disagreement selection using out-of-sample selection predictions … descriptive or inferential status" (L237) | CNA (Ashuach, AQ-SELF1) / RD (multiplicity) | **STRADDLE** | §6.4, §6.5 |
| **E42-5** | "Prohibit outcome-dependent conversion of failed positives into limitation tests and outcome-dependent removal of required comparators. Define CONTENT matching against the actual degradation mediator and require conditional support" (L239) | CNA (my R5 text v2.1 §5c.1, FATE-CASCADE, C-NEC-CONTENT) / RD (decision rules) | **STRADDLE** | §7.3, §7.4, §8.1 |
| **E42-6** | "S-INT decoding label, prediction origin and at-risk sampling … bootstrap bookkeeping … separate operational interruptibility from training-schedule equivalence" (L241) | RD | no (CNA §1.8 S-INT rows defer) | RD |
| **E42-7** | "uninterrupted scheduled viability evaluation … conservative confirmatory rule for incomplete paired episodes" (L243) | RD | no (my C-NEC rows inherit it, §7.2) | RD |
| **E42-8** | "Separate calibration, design selection and confirmation. Freeze the relevant grids, sample-size selection rule …" (L245) | RD / CNA (the imitation-reference calibration for my doses, §8.3) | **STRADDLE** | §8.3 |
| **E42-9** | "interfaces, horizons, donor laws, corruption, noise, floors, observer budgets, comparator family, required counts and stage caps" (L247) | Donor laws, confound corruption and noise, observer budgets and my comparator family: CNA. Interfaces (A-EXT), horizons, floors, Q-LEARN corruption process, AQ-F1 mechanism, counts and caps: RD | **STRADDLE** | §7, §8 |

Also carried from #42 outside the E42 list:
- Q4 Stage-L record (§9).
- Q5 arm wording (§9).
- Q8 Palika/Asan wording (§10).
- Q12 P3 CLOSED (L251).

---

## 2. Claim-to-decision table, CNA rows (E42-1)

These are five separate claim types, never merged (#42 L231). RD owns the decision rules and multiplicity.

| Claim type | Instrument / label | What MET licenses (wording) | What it never licenses |
|---|---|---|---|
| Decoding advantage | C-EXIST (Q-EXIST), vs the **joint** baseline J (§3) | "an accessible estimate of simulated E/I beyond the declared joint baseline (candidate internal representation)" | use, self-model, E-specific use |
| Generic intervention dependence | C-CAUSE (direction edit), C-NEC-DEP (resample ablation) | #42 L55, verbatim: "The declared intervention on this direction/state changed behavior." (C-NEC-DEP: "…changed fixed-horizon viability") | that E (or I) is the information producing the effect (#42 L59) |
| Variable-attributed use | **E-ATTR / I-ATTR** (§4, labelled), C-NEC-CONTENT (mediator-matched, §7.3) | §4.4 wording only | exclusive mediation; trained-agent transfer of planted facts (#42 L187) |
| Observer-relative prediction advantage | SELF (one fixed conjunction, §6) | #42 L183, verbatim: "SELF measures prediction advantage for simulated body variables over the declared observer family." | privileged information; introspection; optimal input-based prediction (#42 L47, L126) |
| Named-signal attribution | SIG-ATTR (§6.6) | "advantage attributable in part to the named simulated degradation signal, under the declared tests" | exclusive mediation (#42 L185) |

**Withdrawn:** "consistent with E-specific use" (CNA W2, v2.1). #42 L57 says it is insufficient if licensed merely by C-EXIST MET plus a reported dissociation. W2 is replaced by §4.4.

---

## 3. Joint history-plus-proxy baseline J (E42-2; replaces erratum 1 E4's max rule)

**#42 L65, verbatim:** "Also include a joint history-plus-proxy baseline. A maximum of separately fitted baselines can miss information available only through their interaction. Retain individual baselines as diagnostics."

**3.1 Definition (CNA proposal; RD owns the Q-EXIST statistic in v2.1 §2.1 / §5.6 L96 and L503 and should adopt this by cross-reference).**
- **Inputs to J**, as one jointly fitted model:
  - the history window over W_B steps: observations, interoceptive channel readings, actions and rewards;
  - plus the proxy set: r̄_t (reward EMA, time constant τ_r), t/H_V, episode-type one-hot, position cell, and the time since the last resource event.
- **Model class.** A 2-hidden-layer tanh MLP of width 256 on the concatenated features. It uses the same fitting, selection and final partitions as the state probe.
  - Hyperparameters: 16 configurations from the frozen grid of §6.2, at 3 initialization seeds each, selected on the selection partition.
  - **Plus a linear model on the same features.** J's R² is the better of the two on the selection partition.
- **Statistic.** ΔR² = R²_final(state → E) − R²_final(J → E). m_EXIST applies to this ΔR² (#41 L106).
- **Diagnostics (REPORTED, never labelled):** history-only H, proxy-only P, and max(H, P) (#42 L65).
- **Replaces:**
  - erratum 1 E4 (`c2cd0732…`, "maximum over (a) … and (b)");
  - v2.1 L96, L172 and L503 ("max(history-matched …, declared proxy baseline)").

**3.2 PROPOSED DEFAULTS and rationale.**

| Parameter | Value | Rationale |
|---|---|---|
| W_B | max(16, 2·d_c) steps, where d_c is the interoceptive channel delay (RD environment spec) | twice the delay so the baseline sees every delayed reading of E at least twice |
| τ_r | H_V/10 steps | slow enough to integrate several resource events, fast enough to track depletion within an episode |
| Width 256, depth 2 | — | at least the representational capacity of every CNA relay and memory plant (§3.3) |

**3.3 Representational capacity of ground-truth plants (#42 L219–220).**
- **FF-RELAY (fixed).** The relay map φ_relay is a 1-hidden-layer tanh MLP of width 32 on the last W ≤ W_B steps, with weights drawn once from a seeded N(0, 1/fan_in) and frozen.
  - A linear probe on φ_relay is a 1-hidden-layer network, which J (width 256, depth 2) contains.
  - **In addition, for this row only, J is also fitted with φ_relay(window) appended to its features** (the "composition-complete baseline"), so the baseline represents the composed mapping exactly, not merely by approximation (#42 L219). ΔR² for this row uses the composition-complete J.
- **MEM pairs (AQ-A2, v2.1 §3.2).** The two histories in each pair are identical inside W **and identical in every J input**: proxies r̄, t, episode type, position and time since the last resource (#42 L220).
  - The integrated-E difference comes only from unobserved metabolic-cost pulses outside W. Those pulses enter E but never reward, position or any proxy.
  - The known answer is analytic: J's Bayes accuracy on MEM-pair discrimination is 0.5 by construction, and MEM-R's is ≥ 0.9 (realization check, one-sided).
  - "W > W_B" alone is not taken as evidence of useful extra memory (#42 L220).
- **CN-N0 and Channel-leak rows:** ΔR² against J, unchanged otherwise.

---

## 4. Labelled dissociation criterion for variable-attributed causal wording (E42-1; #42 L61)

**#42 L61, verbatim:** "For E-attributed conclusions, require a prespecified contrast in which E and reward-history information vary independently within declared support. Freeze the competing behavioral predictions and the relevant equivalence or effect margins. Apply the same principle to I and to content-attributed dependence."

### 4.1 World-draw design (DISSOC set)

- **Two independent drivers, both simulated and in-world only.**
  - (i) **Metabolic-cost pulses**: E decrements of 0.15·(E band width), at Poisson rate λ_m = 4/H_V. They change E and never change reward.
  - (ii) **Token events**: reward increments of +1 that never change E, I, resources or position, at Poisson rate λ_k = 4/H_V. They change r̄ and never change E.
- **Declared support.** Both drivers are present at the same rates in training and in every evaluation world. DISSOC is therefore within the training support (#42 L61: "within declared support"). RD's environment spec must include them (dependency D-RD1).
- **2×2 cells at a fixed decision time t_d = H_V/2.**
  - E-cell: E(t_d) below or above the training-distribution median of E.
  - R-cell: r̄(t_d) below or above the median of r̄.
  - Cell membership comes from pre-drawn pulse and token schedules plus the simulated state. It is assigned before any behavioural outcome is read.
- **Balance.** A_cells = 50 independent episodes per cell per seed (200 per seed).
  - This is a PROPOSED DEFAULT: 50 independent episode clusters per cell supports a cluster bootstrap with per-cell P(approach) standard error ≤ 0.07 even at one decision per episode.
  - The design check is **|corr(E(t_d), r̄(t_d))| ≤ 0.10 on the DISSOC set**, with a one-sided upper bound at the §5.4 level. Failing it makes E-ATTR UNRESOLVED and the set is redrawn before any outcome is read; it is never dropped.

### 4.2 Contrast statistic (interventional; primary)

The agent and plant are frozen. At t_d, the allostatic block is replaced by a **dissociation donor** (donor law DL-ATTR, §7.1(c)), drawn from the fitting partition's DISSOC pool:
- **E-swap:** the donor is in the opposite E-cell and the same R-cell, matched to the recipient on r̄ within ±0.25 SD(r̄) and on the nuisance context c (§7.0).
- **R-swap:** the donor is in the opposite R-cell and the same E-cell, matched on E within ±0.25 SD(E) and on c.

Outcome: B = P(move toward the nearest resource) over the 10 steps after t_d (the C-CAUSE outcome, #41 L107). For I-ATTR, B is the declared in-world integrity behaviour (v2.1 §5c.2).

The two statistics are:
- **Δ_E** = mean[B(E-swap to low-E donor) − B(E-swap to high-E donor)]
- **Δ_R** = mean[B(R-swap to low-r̄ donor) − B(R-swap to high-r̄ donor)]

Both are paired within recipient, averaged per seed, with the seed as the unit (RD §5.1).

**Competing predictions (frozen):**
- H_E: Δ_E > 0 (lower E raises approach), with Δ_R unconstrained.
- H_R: Δ_R > 0 and Δ_E ≈ 0.

**Label.**
- **E-ATTR MET** iff the lower confidence bound of Δ_E is > m_ATTR.
- **E-ATTR NOT MET** iff the upper bound of Δ_E is < m_ATTR.
- **BOUNDARY** otherwise.
- Bounds are at the §5.4 level (RD).
- m_ATTR = **0.05** (five percentage points of B). This is a PROPOSED DEFAULT on the same scale as m_CAUSE (#41 L107, "five percentage points above the comparator on the stated behavioral probability").
- Δ_R is REPORTED with its interval.
- The **observational** 2×2 cell-mean contrast (no swap) is REPORTED as a diagnostic.

### 4.3 Eligibility

A recipient step is eligible if a DL-ATTR donor exists within support (§7.1(c)).
- Expected eligibility e_exp = 1.0 by construction. The pool is ≥ 4× the recipients per cell.
- The floor is that the one-sided Clopper–Pearson lower bound of the eligible fraction is ≥ e_min = 0.90 (v2.1 §P3 §2.3; sidedness per RD §5.4).
- Ineligible steps are counted, never dropped. Below the floor, E-ATTR is UNRESOLVED.

### 4.4 Wording rule (replaces W2)

- **Generic:** if C-CAUSE is MET, write: "The declared intervention on this direction/state changed behavior." (#42 L55)
- **E-attributed:** this wording is permitted only if **all** of the following hold:
  1. E-ATTR is MET on the same state and seed set;
  2. narrowed C-EXIST (vs J) is MET on the same state and seed set;
  3. the Stage-0 rows **MIXED-CODE-E** (§5) and **REW-CORR** are PASS for E-ATTR.

  The permitted wording is: "Under the declared dissociation contrast, the behavioural effect of the state followed its E-component when reward-history information was held fixed."
- Never write "E-specific use established", "uses E", or "consistent with E-specific use" (#42 L57).
- **I:** the same rule with I-ATTR and MIXED-CODE-I.
- **Content:** C-NEC-CONTENT under mediator-matched donors (§7.3) is the content-attributed analogue (#42 L61, "Apply the same principle … to content-attributed dependence").
- E-ATTR, I-ATTR and C-NEC-CONTENT are labelled claims, so **RD places them in the multiplicity family** (dependency D-RD2).

---

## 5. MIXED-CODE plant (E42-2; #42 L63)

**#42 L63, verbatim:** "Include a mixed-code plant: E is decodable beyond the baseline, but the downstream controller uses only a separate reward-related component. It should pass generic dependence and fail E-use attribution."

**Construction (scripted Stage-0 generator).**
- The allostatic block z ∈ R^{d_ws} carries two orthogonal components in fixed, seeded orthonormal directions:
  - z_E = Ê_t, a leaky integrator of the interoceptive channel *plus* the metabolic-pulse count (so it carries E-information that J lacks, §3.3);
  - z_R = r̄_t.
- The controller reads **only** z_R. Read weights on z_E are exactly zero, checked from the graph.
- The controller is the scripted competent policy (as CN-P1): approach probability a monotone function of z_R.

**Rows.**

| Row | Instrument | Expected | Row type |
|---|---|---|---|
| MIXED-CODE-E | C-EXIST (vs J) | MET | mechanism-present (layer (i)) |
| | C-CAUSE (edit along the decoded E direction u; u loads on z_R through corr(E, r̄)) | MET | mechanism-present: generic dependence passes (#42 L63) |
| | C-NEC-DEP | MET | mechanism-present |
| | **E-ATTR** | **not MET** | **specificity row: PASS if the false-MET rate is within bounds, FAIL if not, CONFOUND NOT REALIZED → UNRESOLVED if not realized** |
| MIXED-CODE-I | as above with z_I, the integrity outcome and I-ATTR | I-ATTR not MET | specificity row, same labels |

**Dose, units and realization (item-3 conventions; one-sided, v2.1 §P3 §2.2 and erratum 2).**

| Parameter | Value |
|---|---|
| Dose parameter | ρ = corr(E, r̄) on standard (non-DISSOC) episodes, dimensionless. ρ is set by the token-event rate and the resource-reward coupling of the plant world |
| Required doses | ρ ∈ {0.5, 0.7, 0.9}, plus a ρ = 0 sanity level that is REPORTED only. Rationale: the same grid as REW-CORR, where 0.9 is the harsh case in which the decoded E direction is nearly aligned with z_R |
| Fixed second parameter | Decodability of z_E: R²(z_E → E) = 0.9, set by integrator noise σ_E = 0.33·SD(E), since R² = 1/(1 + σ²/Var) ≈ 0.90 |

A replicate is **realized** (real_i = 1) iff all four checks pass (tol = 0.10):
1. corr(E, r̄) ≥ ρ·(1 − tol);
2. raw ΔR²(state → E vs J) ≥ ref ΔR²(CN-P1)·(1 − tol);
3. raw |ΔB| under a decoded-direction edit ≥ ref |ΔB|(CN-P1)·(1 − tol), i.e. generic dependence is truly present;
4. construction check: read weight on z_E = 0, exactly.

The **dose-fidelity check** |corr − ρ| ≤ tol·ρ is REPORTED only (erratum 2).

**Eligibility.**
- Eligible iff the E-ATTR eligibility (§4.3) holds and the C-CAUSE floors hold.
- e_exp = 1.0 by construction. Floor: e_min = 0.90 (one-sided Clopper–Pearson lower bound).
- The stored reason separates realization failure (r1) from eligibility failure (r2) (#42 L5).

**Rule.** For each required dose, f_ok = Σ(real_i·elig_i)/R over all R prespecified replicates. If the Clopper–Pearson lower bound is < f_min = 0.90, the row is CONFOUND NOT REALIZED → UNRESOLVED.
- With one-sided 95% and R = 200, that means 188/200 (0.9046). With two-sided, 189/200 (0.9037). Sidedness per RD §5.4.
- #42 L5: this guarantees joint realization and eligibility ≥ 0.90, not universal availability.

**Label (v2.1 §2.5, unchanged).**
- **FAIL** if, at any required dose meeting the rule, the E-ATTR false-MET rate exceeds the per-row bounds (≤ 0.05, upper bound ≤ 0.08; #41 L112), on **either** the all-replicate sample or the eligible-realized subset. Both are retained (#42 L5).
- Otherwise **CONFOUND NOT REALIZED** if any dose fails the rule.
- Otherwise **PASS**.
- Per-row only. No battery-wide guarantee is claimed (#42 L152).

**Why these expectations hold.** An E-swap holds r̄ fixed (§4.2), so z_R and the controller's input are unchanged. Δ_E = 0 by construction, and the R-swap gives Δ_R > 0. REW-CORR (state = r̄ + noise) gives the same result and stays mechanism-present for generic dependence (#42 L51).

---

## 6. SELF: fixed observer gate, conjunction, wording, AQ-SELF1 (E42-3, E42-4)

### 6.1 Wording (#42 L175–183)

- **SELF claim, verbatim (#42 L183):** "SELF measures prediction advantage for simulated body variables over the declared observer family. Attribution to a privileged signal requires separate evidence concerning that signal."
- SELF is not a "privileged-information instrument" (#42 L177).
- Beating the declared observers does not show the task is unsolvable from input cues, and does not distinguish privileged access from second-order computation (#42 L126).
- Facts about planted cases do not transfer to trained agents (#42 L187).

### 6.2 Observer family (frozen before Stage 0; no plateau route; #42 L37, L49)

| Observer | Inputs up to the cutoff | Role |
|---|---|---|
| **O-ACT-P** (pathway-matched, inputs + actions) | Observations, interoceptive channel, actions available by the cutoff (#41 L67). **The family includes action-ignoring candidates** (the action input masked to zero) (#42 L124) | **Required conjunct** |
| **O-IN-P** (pathway-matched, inputs only) | Observations and interoceptive channel; no actions | **Required conjunct** (the Singh input-only test, #42 L126) |
| O-HEAD (the former O-in, head-matched) | as O-IN-P | Diagnostic only (#42 L114) |
| Plateau sweep around O-IN-P | as O-IN-P | Diagnostic only (#42 L39–47) |
| Privileged-signal observer O-SIG (O-IN-P plus the named signal) | as O-IN-P plus the signal | Diagnostic for §6.6 only |

**Pathway accounting.** #42 L114–122 asks the accounting to expose the asymmetry; "There is no uniquely correct parameter-count equation".

The **representation-producing pathway** P_agent = the agent's input encoder + recurrent core + self-prediction head. O-ACT-P and O-IN-P are matched to P_agent on every row below. Every value is reported side by side in a pre-registered accounting table, for the agent and for each observer.

| Dimension | Matching rule (PROPOSED DEFAULT) | Rationale |
|---|---|---|
| Parameters | Trainable parameters = those of P_agent (encoder + core + head), within ±5% where layer granularity forces it | Matches the computation that built the state, not just its terminal head (#42 L112) |
| Architecture and memory | The same encoder type, recurrent cell type, depth and width, and head form as P_agent. The **full episode history up to the cutoff** (the same recurrent memory the agent has) | #42 L116, "recurrent memory". A truncated-history observer would be a strawman (AQ-A2) |
| Training exposure | Environment time steps = the total time steps whose gradients updated P_agent during the agent's training. Data: the agent's archived training trajectories, sampled without replacement. If not archived, an equal count regenerated from the frozen final policy, labelled as such | #42 L117, "Training exposure and learning expenditure" |
| Optimizer steps | = the agent's gradient updates that touched P_agent, with the same optimizer family, batch size and learning-rate schedule family | Equal learning expenditure |
| Model selection | Configurations = the agent's declared tuning budget + the self-probe's, with a **minimum of 16**. Frozen grid: learning rate {3e-4, 1e-3, 3e-3}; weight decay {0, 1e-4}; width {×0.5, ×1} of P_agent (×1 is the cap); 3 initialization seeds per configuration; selection on the selection partition by held-out loss | #42 L119, "Optimization and model-selection opportunities". 16 is the smallest grid covering the listed factors with at least two values each |
| Timing | The same prediction cutoff and the same horizon h as the agent's self-prediction head (SELF primary horizon: RD) | #42 L118 |
| Excluded signals (listed) | The agent's internal state; simulator E/I; fate-noise realizations; the stop log and harness schedule; future actions | #42 L120 |

**Stage-0 equivalent.** In synthetic plants the "agent training" is constructed. Its expenditure is declared per plant as (time steps, updates, configurations) of the generator's fitted head-and-encoder stand-in, and the observers are matched to that.

### 6.3 Gate and conjunction (E42-3, E42-4; #42 L17–31)

- **SELF MET** iff the lower bound of PA vs O-ACT-P is > m_SELF **and** the lower bound of PA vs O-IN-P is > m_SELF. Here PA = 1 − L_agent/L_O, m_SELF = 0.05 (#41 L105), and an observer-loss floor applies (#41 L75; RD floor).
- This is **one fixed conjunction and one family member**. #42 L21: P(all pass) ≤ P(null comparison passes) ≤ α/m. No within-SELF adjustment.
- The component intervals are not claimed to be simultaneously calibrated (#42 L27).
- **No plateau exemption** (#42 L17, L37). v2.1 V11's "or a pre-specified capacity and data sweep shows … plateaued" is **withdrawn**.
- **If the required observers can't be resourced**, SELF reads **UNRESOLVED (required observer comparison not performed)**. A bounded O-HEAD comparison may be REPORTED (#42 L49). It is never MET.
- Claims read off individual observer comparisons, for example "beats O-IN-P", are not labelled. Any such claim would need its own inferential treatment (#42 L29).

**Plateau sweep (diagnostic; #42 L39–47).**
- Grid around O-IN-P: capacity ×{0.5, 1, 2} of P_agent parameters; data ×{0.5, 1, 2}; optimizer steps ×{0.5, 1, 2}; 3 initialization seeds each.
- The grid is finite and fixed before evaluation. Selection uses selection-partition data.
- Tolerance: an improvement of < 0.01 in normalized held-out loss L/Var(y) from the largest step on each axis. This is a PROPOSED DEFAULT: one percent of target variance is below the m_SELF scale of 0.05.
- It is reported as "within tolerance" only when the upper confidence bound of the improvement is < 0.01, not merely when the improvement is nonsignificant.
- No expansion after the final test. It establishes adequacy only within the searched family (#42 L47).

**Rows affected (v2.1 CNA §1.7). Known answers are unchanged in kind.**

| Row | Change |
|---|---|
| SELF-P1 | MET against both conjuncts |
| SELF-NC2 (capacity) | Dose = agent pathway / observer pathway parameter ratio ∈ {4, 8} for the *as-built mismatched* observer. The pathway-matched conjuncts close the gap → not MET |
| BUDGET-GAP | b = observer expenditure / P_agent expenditure (time steps × updates) ∈ {0.25, 0.5} for the as-built observer. The frozen matched conjuncts → not MET |
| SELF-NC3 (action leak) | O-ACT-P closes the gap, so the conjunction is not MET whatever O-IN-P shows |
| INPUT-INFERABLE | O-IN-P closes the gap → not MET. Dose: linear-predictor R² relative to the true map ∈ {0.5, 0.2}. The true map is a 2-layer tanh network of width 64 on the input history, which O-IN-P can represent (§3.3 principle) |

All of these remain realization-checked one-sided, with the f_min rule of §5.

### 6.4 Ashuach description, corrected (E42-4; #42 L94)

- **Old (CNA v2 §4, v2.1 L747 ff.):** "privileged advantage appears only on disagreement subsets"; "No advantage overall; the advantage appears only on disagreement subsets."
- **New:** "Ashuach et al. (ACL 2026) select examples where the underlying target and peer models have different **correctness labels**. Our analysis selects **numerical disagreement between prediction heads**. That is an adaptation, not the same analysis (#42 L94)."
- The Ashuach result is cited as motivation only.

### 6.5 AQ-SELF1: descriptive secondary (E42-4; #42 L92–108)

**Status: DESCRIPTIVE SECONDARY, no label, no MET terminology.** A secondary success cannot rescue a primary SELF failure (#42 L108).

**Rules (PROPOSED DEFAULTS; replace v2.1 CNA §4.1 where they differ).**

| Item | Rule |
|---|---|
| Threshold | δ_dis is the (1 − q) quantile of the normalized gap \|ŷ_agent − ŷ_O\|/s_y, computed from **out-of-sample predictions on the selection partition** (#42 L100; replaces "fitting partition"). q = 0.20, a declared descriptive convention (#42 L106) |
| Normalization | s_y = SD(y) on the **fitting** data only (#42 L101) |
| Ties | gap ≥ δ_dis counts as disagreement |
| Aggregation | Per variable (E, I) separately, with no pooling across variables |
| Minimum subset | ≥ 30 disagreement items per seed, per variable, per observer. Otherwise that cell is NOT REPORTED and counted. Rationale: a stable per-seed mean loss |
| Selection basis | Predictions only, from frozen predictors (#42 L96). It is not artifact-free: conditional error selection can differ without information differences (#42 L96), and that caveat is printed with every result |
| Reporting | Final-set subset frequencies, losses and denominators (#42 L103). Observer-specific subsets are reported separately and **never compared as one population** (#42 L104) |
| Calibration on N/NC rows | Report the sampling distribution of PA_dis (mean, SD, 5th/95th percentiles across replicates). **No "false-MET rate"** (#42 L108) |

### 6.6 Named-signal attribution SIG-ATTR (#42 L185)

Labelled separately from SELF. All of the following must hold:
- (i) The signal and the reason it is externally unavailable are declared before freeze.
- (ii) **Dependence:** resample-ablating the named signal channel in the agent (donor law DL-NEC, §7.1(b), applied to the channel) reduces PA vs O-IN-P, with the lower bound of the drop > m_SELF.
- (iii) **Sufficiency (REPORTED):** O-SIG closes the gap.

The permitted wording is: "advantage attributable in part to the named signal under the declared tests". (iii) alone never licenses attribution (#42 L185).

---

## 7. Donor and intervention laws (E42-9; fully specified)

### 7.0 Shared definitions

- **Pools.**
  - Donors come from the **fitting partition** of the same frozen agent or plant, from different episodes than the recipient. Recipients come from the final partition.
  - Pools are built and support-checked before any final outcome is read.
- **Nuisance context c** = (time bin ⌊10·t/H_V⌋, position cell on a 4×4 grid, last action).
  - Rationale: these are the declared nuisance variables (#41 L87) that make a donor incompatible with history and timing.
  - E, I and r̄ are excluded from c except where a law below adds them.
- **Conditional support.** The hybrid state's Mahalanobis distance from the recipient's c-conditional state distribution must be ≤ the χ quantile at 0.99.
  - That distribution is a Gaussian fit on the fitting partition with Ledoit–Wolf shrinkage.
  - Off-support draws are rejected and redrawn. The maximum is 20 draws; if all 20 fail, the step is ineligible.
  - **Ineligible steps are counted.** If the one-sided Clopper–Pearson lower bound of the eligible fraction is < 0.90, the affected comparison is **UNRESOLVED**. It is never dropped (#42 L217).
- **Freezing.** All draws use a dedicated, seeded donor RNG stream, logged before evaluation.

### 7.1 Laws

**(a) DL-CAUSE (C-CAUSE and C-CAUSE-I edits).**
- Edit: z ← z + κ·s_u·u at the decision step only, after which the state evolves freely.
  - u is the unit decoded direction from the fitting-partition probe.
  - s_u = SD of the projection on the fitting partition.
  - κ ∈ {−1, +1}, a PROPOSED DEFAULT: ±1 SD stays inside the bulk of the state distribution.
- In range means the projection after the edit lies within its fitting-partition 5th–95th percentiles. Otherwise the step is ineligible and counted.
- Outcome: B over the next 10 steps.
- **Shams**, the comparator family of §7.2: the same κ·s and the same timing, along each family member. The comparator is the strongest.
- **CN-NC2 dose:** fragility in Δprob per SD, set so that the non-directional loss is {1, 2}× ref (unchanged).

**(b) DL-NEC (C-NEC-DEP resample ablation, and the matched blocks).**
- At **every** step from t = 0 to H_V, the target block's state is replaced by an i.i.d. draw from the c-conditional donor pool, subject to the support check.
- The same law is applied to each qualifying matched block (v2.1 §5c.1(b)), with equal dimension, the same c and the same duration.
- **Restoration rescue (REPORTED):** a separate pass ablates the block for t ∈ [H_V/4, H_V/4 + 20) and then restores the recipient's own trajectory state. The ΔV recovery is reported.
- **Restoration does not distinguish generic damage from content (#42 L217)**, and it does not gate anything.

**(c) DL-ATTR (E-ATTR, I-ATTR; §4.2).** This is a single-step full-block swap at t_d.
- The donor is in the opposite target-variable cell, matched on c, and matched on the held-fixed variable within ±0.25 SD:
  - r̄ for E-ATTR;
  - for I-ATTR, both r̄ **and** E within ±0.25 SD, so that neither reward history nor energy confounds I.
- Support check as in §7.0.

**(d) DL-CONTENT (FATE-CASCADE redefined; C-NEC-CONTENT): matched to the actual degradation mediator (#42 L218).**
- The fate mediator is the per-step simulated noise SD σ_t = κ_f·g(state history), where g is the deviation-to-noise function frozen in RD's AQ-F1 mechanism (dependency D-RD3).
- A donor qualifies iff two conditions hold.
  - **Mediator match:** for each of the last L_m steps, |σ_t^donor − σ_t^recipient| ≤ 0.10·σ_t^recipient, with L_m = the memory length of g declared in AQ-F1 (L_m = 1 if g is memoryless). This matches the coupling law and its relevant history (#42 L218), not "same band deviation".
  - **Content difference:** |⟨z_donor − z_recipient, u⟩| ≥ 1.0·s_u.
  - Rationale for 0.10 and 1.0 (PROPOSED): the mediator is held within 10% while content moves a full SD.
- **Support and resolution rule:** if the one-sided Clopper–Pearson lower bound of the fraction of recipient steps with a qualifying donor is < 0.90, **or** the content spread among qualifying donors is < 0.5·s_u, then **C-NEC-CONTENT is UNRESOLVED** (#42 L218: "If matching removes all content variation or lacks support, CONTENT is unresolved").
- **κ_f dose:** in units of noise SD per unit of g, in units of the affected block's state SD. κ_f is set so the raw coupling-on gap (non-matched donors) = {1, 2}× the ref gap of CN-P1. It is computed analytically from the plant's noise-to-V map where available. Otherwise it is set on the **calibration** partition (§8.3), never on confirmation replicates.

**(e) DL-COV (AQ-A1 covariance-matched subspaces).**
- Σ is the block covariance on the fitting partition (Ledoit–Wolf).
- A covariance-matched random d-subspace is the orthonormalized Σ^{1/2}G, with G an i.i.d. N(0, 1) d_ws×d matrix.
- Interventions along it are **norm-matched**: the same ‖δ‖ as the target edit, and per-direction variance matched to the target's within ±10%.
- Described as "covariance-matched", never "on-manifold" (#41 L230).
- Conditional compatibility uses the §7.0 support check (#41 L236).

**(f) DL-PATCH (BCAST patching; DONOR-MISMATCH rows).**
- The donor z comes from a different episode with the same c and the content difference of (d), applied for one step.
- **DONOR-MISMATCH dose:** donors are deliberately drawn at Mahalanobis {2, 3} SD from the recipient's c-conditional distribution, bypassing the support check for this row only.

### 7.2 Comparator family (AQ-A1; CNA-owned members; RD owns the budget and the optimized comparator's fit)

Per target block of dimension d, the frozen family is:
- 20 norm-matched random d-subspaces;
- 20 DL-COV subspaces;
- the PCA-top-d subspace of each qualifying other module;
- the optimized comparator (RD, #41 L56).

K is the total count, which is fixed. The comparator is the strongest member. The PROPOSED DEFAULT of 20 + 20 makes the maximum over random draws stable to roughly the 95th percentile of the null spread. RD's budget may lower this only before freeze, never on outcomes (#41 L234).

### 7.3 Corrections to my Lead-adopted R5 text (v2.1 §5c.1; E42-5)

**(a) BCAST-P1 floor**
- **Old:** "If fewer than floor(K/2)+1 modules can meet the S_k floor in BCAST-P1, the instrument is a **designated limitation** (expected UNAVAILABLE, #41 L274), recorded before freeze."
- **New:** "If BCAST-P1 fails its S_k floor or its breadth, that is a **failed required positive-control check**: the instrument is NOT ELIGIBLE and Stage 0 is blocked for BCAST. It is never converted to a limitation test. LIM roles (BCAST-LIM only) are assigned before any result (#42 L216)."

**(b) Matched block restoration, item 5**
- **Old:** "Its own intact-vs-restoration contrast passes (#41 L89). A block that cannot be restored is excluded **and counted**."
- **New:** "Block eligibility is frozen from the architecture graph and the **selection-partition** checks (dimension, magnitude/covariance tolerance, fan-out ratio) before final evaluation. A required block that then fails any integrity or validity check on the final partition stays in the family, and the comparison is **UNRESOLVED**; it never disappears (#42 L217). Restoration is REPORTED and does not gate eligibility, because it 'does not distinguish generic damage from content-specific intervention' (#42 L217)."

**(c) Tolerances named in R5(b)**
- Magnitude and covariance: within ±10% per direction.
- Fan-out: the read fan-out ratio is within [0.5, 2] of the allostatic block's.
- PROPOSED DEFAULTS: a factor-of-two connectivity window is the narrowest that typical architectures can populate with more than one block.

### 7.4 R18 wording correction (v2.1 §5c.3; #42 L81)

- **Old:** "The current arms span both (A-FULL), reward only (A-NOFATE) and neither (matched-senses)."
- **New:** "A-FULL versus A-NOFATE estimates the effect of degradation conditional on the existing reward and termination rules. A-NOFATE versus the matched-senses arm changes direct reward **and** E/I-dependent termination; it is not a reward-only manipulation (#42 L79–81). No degradation-only cell is added (#42 L77)."
- The "Optional, for #42" bullet is answered and retired.

---

## 8. Other pending scientific choices in CNA rows (E42-9)

### 8.1 Confound corruption and noise parameters (all PROPOSED DEFAULTS)

| Row | Parameter | Value | Rationale |
|---|---|---|---|
| FF-RELAY (fixed) | Relay noise | SNR = R²/(1 − R²) for R² ∈ {0.6, 0.8, 0.95} → SNR {1.5, 4, 19} | The existing R² doses, expressed as a noise law |
| REW-CORR, PROXY | State law | z = p + ε, ε ~ N(0, (0.1·SD(p))²), with p = r̄ or the proxy | Near-noiseless copy, so the row tests the instrument, not the noise |
| Channel-leak | Channel SNR | Baseline 1.0. Improvement ×{1.5, 3} | Moderate and strong read-out gains |
| SELF-NC1 | Leak SNR | {1, 4} at delay d ∈ {1, h} | Weak and strong leaks |
| SELF-NC3 | R²(actions → y) | {0.5, 0.9} | Unchanged |
| DISTRIBUTED | n_d, s_in | {4, 16}, 0.5 | Unchanged (erratum 1 E1) |
| IGN plants | Process noise ξ | N(0, (0.05·‖x_hi − x_lo‖)²) per unit time | Keeps the bimodal modes separated by about 20 noise SD at readout |
| IGN settling (E3 (ii-a); #42 L221) | Settling length | t_s = 5τ in plants (residual e^−5 < 1%); 20 steps in networks | Five time constants. For networks, 20 steps exceeds 2·d_c for typical d_c ≤ 10 |
| | Readout delay | t_r = 3τ in plants; 5 steps in networks | — |
| | Settling tolerance | 2 × the median absolute deviation of ‖x_ref − median x_ref‖ in null-input runs on the fitting partition, with no probe input | Chosen without the observable w |
| | **Coverage** | At **every** required strength bin and each near-transition bin, the one-sided Clopper–Pearson lower bound of the eligible fraction is ≥ 0.90. Otherwise IGN is **UNRESOLVED** | Aggregate eligibility must not hide exclusion of the informative region (#42 L221). The claim is stated as "under the declared settled-state response protocol" |
| MEM pairs | Pulse law | As §3.3 | — |

### 8.2 Observer budgets

These are fully specified in §6.2 and §6.3.

### 8.3 Calibration separated from confirmation for my doses (E42-8; RD owns the global split)

- Every analytic imitation reference stays analytic.
- Where a reference or a κ_f dose needs fitting (§2.1 "otherwise … calibration partition"), it uses **R_cal = 50 calibration replicates**, generated independently of, and before, the R_rep confirmation replicates.
  - PROPOSED DEFAULT: 50 gives the reference median to within about ±0.18 SD.
- Calibration replicates **never** enter any label. Confirmation replicates never set any dose.
- RD's n_seed selection uses its own calibration role (#42 L222). Dependency D-RD5.

---

## 9. Carried rulings (record)

- **Stage-L requirement (AQ-2; #42 L67–75).** No trained arm is added now (#42 L69). Recorded requirement, verbatim: "any claim of acquired ignition must confront an architecture-imposed alternative under the relevant training and evaluation conditions. Common input histories and paired initialization remain necessary." The later control must "distinguish changes in occupancy or accessibility of an imposed regime from acquisition of the claimed mechanism" (#42 L73). The Stage-0 plant (v2.1 CNA §1.2 D-l) "cannot discharge that later requirement" (#42 L75).
- **No degradation-only cell** (#42 L77). §7.4 applies.
- **No battery-wide joint false-MET target** (#42 L142–152). CNA rows carry per-row targets only.

## 10. Prior-art wording (Astra #42 Q8)

- **Palika, negative evidence, verbatim (#42 L134):** "In the inspected repository snapshot, the reviewers did not find an other-module matched-size ablation; they found a within-bottleneck random-neuron comparison. The paper's full text remains unverified."
- **Snapshot record (#42 L136):**
  - Repository `CharithaPalika/FoodRL`. HEAD commit `65bb4f8d489a6aa8c60115d0d9bd3da98810e140`, committed 2026-08-25 06:22:24 UTC, as read by a GitHub API GET at 2:33:47 PM ET today. That commit date matches v1.6's recorded last commit (v1.6 L92).
  - Inspected paths and search scope: v1.6 routes 28–37 (L52–61), plus the grep scope at v1.6 L100.
  - This is not upgraded to "the paper contains no such experiment".
- **D4 vs Palika:** unverified and **non-blocking**. The study's justification does not depend on D4 being novel (#42 L138).
- **D3:** retained as an explicitly described outcome difference, "not … an automatic certificate of substantive novelty under the drop rule" (#42 L138).
- The FoodRL README "explicitly describes learned physiological representations and representation-level perturbations", which supports substantial conceptual overlap (#42 L130).
- **Asan:** interpretations of the dimensionality-matched control and the masking quantity are marked **"reviewed from supplied excerpts"**. 82% → 10% is not interpreted as viability. Blanket absence claims remain attributed to CNA's full read (#42 L140).
- **P3: CLOSED** for the declared bounded search (#42 L251). Query strings, dates, ranking limits, screening decisions and inaccessible-source statuses are preserved in v1.4–v1.6 (#42 L193).

---

## 11. Discrepancies: Lead's summary and brief vs the raw #42

- **D1.** The brief says the E-use attribution instrument "must FAIL" on the mixed-code plant. Raw L63: "It should **pass generic dependence** and fail E-use attribution." The brief omits the pass half. Its "FAIL" is also an instrument outcome (not MET), whereas FAIL as a row label means a false MET. Handled in §5, where the row is PASS when attribution correctly reads not MET.
- **D2.** The brief scopes the dissociation contrast to E. Raw L61 adds: "Apply the same principle to I and to content-attributed dependence." Handled with I-ATTR, MIXED-CODE-I and §7.1(d).
- **D3.** The brief's joint-baseline item omits raw L65's "Retain individual baselines as diagnostics." Handled in §3.1.
- **D4.** The brief specifies matching "encoder plus recurrent core plus probe". Raw L122 says "There is no uniquely correct parameter-count equation, but the accounting must expose rather than hide the asymmetry", and L116–120 add memory, timing, model selection and excluded signals. Raw L124 also requires action-ignoring candidates, and raw L49 says an unresourced comparison leaves the interpretation UNRESOLVED. All are adopted. Encoder + core + head is my declared equation, not a uniquely correct one.
- **D5.** The brief's AQ-SELF1 item omits raw L100 (thresholds from out-of-sample **selection** predictions; v2 used the fitting partition) and raw L108 (no "false-MET" terminology without a diagnostic rule). Both are adopted in §6.5.
- **D6.** Raw #42 Q14 (L216–217) overturns two clauses of **CNA text the Lead adopted as governing** in v2.1 §5c.1 (the BCAST-P1 → LIM conversion and the excluded unrestorable block). Neither the brief nor the consult summary flags that these are adopted CNA text. They are corrected in §7.3. Q5 (L81) likewise corrects v2.1 §5c.3's "reward only (A-NOFATE)" (§7.4).
- **D7.** The consult summary header (`astra_consult_1.md` L157) stamps #42 at "~2:35 PM ET", but this brief arrived at 2:30 PM ET. The timestamp is approximate or early. Raw content is unaffected.
- **D8.** `astra_consult_1.md` L158 reports a transport anomaly (part 2 sent twice). It can't be verified from the raw reply, and the raw reply notes it reviewed "the supplied condensed record" (L15). This is recorded only.
- **D9.** The v2.1 header (L3) still says "P3 stays OPEN … pending Astra #42". Raw L251 closes it. That is RD's header to update (D-RD6).

No other mismatch was found. The summary's statements of Q1–Q14 match the raw text.

## 12. Cross-file dependencies for RD

| ID | Dependency |
|---|---|
| **D-RD1** | The environment spec must include metabolic-cost pulses and token events at λ = 4/H_V in training and evaluation (DISSOC support, §4.1; MEM, §3.3). It must also declare d_c, so that W_B = max(16, 2·d_c) is defined |
| **D-RD2** | Multiplicity family: add E-ATTR, I-ATTR (each one member per declared function) and C-NEC-CONTENT (already in). The SELF conjunction is one member (§6.3). State whether α controls false MET only or both directions (#42 L156) |
| **D-RD3** | AQ-F1 must freeze g (the deviation-to-noise function) and its memory length L_m. DL-CONTENT (§7.1(d)) and the κ_f units depend on them |
| **D-RD4** | Q-EXIST statistic (v2.1 §2.1 L96, §5.6 L503): replace max(H, P) with the joint J of §3.1. Q-LEARN inherits it. The individual baselines become diagnostics |
| **D-RD5** | Calibration / selection / confirmation split (E42-8): CNA's R_cal = 50 dose-calibration replicates must sit outside the confirmation allocation and outside the n_seed calibration role |
| **D-RD6** | v2.1 header P3 status → CLOSED (#42 L251). Retire v2.1 V11's plateau route (§6.3). Replace v2.1 §5c.1 (a) and (b) item 5 with §7.3, and §5c.3's arm wording with §7.4 |
| **D-RD7** | The SELF primary horizon h and the observer-loss floor L_O are RD's. The observers match the agent's cutoff and h. The agent's tuning budget and whether training trajectories are archived must be declared in the training protocol (§6.2) |
| **D-RD8** | A-EXT interface (#42 L13) is RD's. No CNA row depends on it beyond the unchanged A-EXT veto row |
| **D-RD9** | The S-INT decoding label and origin (E42-6) are RD's. CNA §1.8 S-INT rows defer to it. The "Schedule-leak" row should use RD's at-risk or fixed-origin label |
| **D-RD10** | Viability (E42-7): DL-NEC, DL-CONTENT and E-ATTR evaluations run under uninterrupted scheduled evaluation. Incomplete paired episodes follow RD's conservative rule; CNA rows add none of their own |

---
Footer: input hashes (sha256; verified on the box 2026-10-23, about 2:31–2:34 PM ET; none edited)
- `/workspace/astra_consult42_response.txt`: e438e329cff272bfd174a88dd917da6d7eb5560436fee06c39d0d46fd719c847
- `/workspace/astra_consult_1.md` (#42 section L157–164, read in full): 6ad5afa02a487fa4beb26b09df74a1a2b8ac7121a292de082828d515912ace25
- `/workspace/review/trackB_instrument_validation_scope_v2_1_merged_RD.md`: 8ea6abc50b3929a39688aa54b1a1d66fe34c8ef17b3c5dfae98cc8efa79862de (internal footer 15a0b715ed7567084488e99045c141692513dd7ca89885e83a4ce769304f3e1f, reproduced)
- `/workspace/astra_consult41_response.txt`: 3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43
- `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md`: 17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e
- `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md`: c2cd0732c4bd319497306b1dc47d440b50011843a9078ad5a59f46c720003543
- `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum2.md`: 5ddde854099020adf113d9c1fd81a1f511d272e5d294abcd3493a1283a1878bc
- `/workspace/review/trackB_scope_v2_merged_lightpass_CNA_v1.md`: 2d52f7d372f02896e895f8350ed5b66867cb925fe4c572ae338998593424f868
- `/workspace/review/trackB_prior_art_verification_v1_6_palika_route_CNA.md`: 9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851
sha256 of all content above this line: 7d93990c5bca535a1988aef3977bd23e5725827ba9c129ad446c9c6f5412fa83
