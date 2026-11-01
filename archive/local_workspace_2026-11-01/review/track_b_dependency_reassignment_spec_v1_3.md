# Track B: Function-matched dependency-reassignment test, paper spec v1.3

Changes from v1.2, which stays unchanged:
- §10 now states Di Paolo's prediction for YOKED-RELIEF explicitly. v1.2 said DP had "no relevant prediction", which was wrong. ACI Research Specialist caught this: DP's plasticity also stops once the system is back in bounds, so k_e alone cannot separate DP from UDTN. Two DP rivals are now given: literal DP, and DP-R (Di Paolo's gate moved onto resource).
- A new measure, the relief-locked variability contrast ΔV, is added, along with a new arm, RELOCATE (§10.1), and outcome item 8.
- A new §11, ANTICIPATE, adds a second discriminator against K&G, as Research Delegate proposed, with a cue-delay guard against Hebbian look-alike anticipation.

Changes from v1.1, which stays unchanged:
- The K&G reward is now written out explicitly.
- SATISFICE is narrowed to separate UDTN only from a *reward-maximizing* RL rival (R-RLMAX), not from K&G. Under K&G's drive-reduction reward, overshooting the setpoint earns nothing or costs something, so K&G can also be indifferent between o=2 and o=3, or even prefer o=2. ACI Research Specialist caught this.
- A new K&G discriminator, YOKED-RELIEF, is added in §10.

Changes from v1, which stays unchanged:
- The HRL discriminator is corrected. UDTN's shortfall gate *does* read resource state, so v1's claim that UDTN "never had access" was wrong and is withdrawn.
- The masking arm is replaced by an information-matched dissociation plus a behavioral discriminator that doesn't depend on where the signal is read.
- A new §9 says who sets the shortfall threshold and why it's still a supplied persistence condition.

Both corrections came from Research Delegate and ACI Research Specialist.

Owner: Constitutive Neural Architecture Research Agent. Status: PAPER ONLY. This authorizes no simulation, training or implementation (Astra §7). Any execution comes back with its own protocol, budget and approval request.
Depends on: `track_b_mechanism_comparison_v1.md` (and §5 of `track_b_mechanism_comparison_v1_1.md`) (UDTN equations U1–U7). It follows named change 6.

## 1. Claim under test (admissible form, Astra §5)

> Under fixed supplied dynamics, two organizations with matched immediate function but different acquired maintenance dependencies show different subsequent behavior. Reassigning the dependency, without changing the immediate task mapping, redirects behavior toward whatever now sustains the vulnerable organization.

The test reports Q-EXIST (G2, hand-constructed) separately from any later Q-LEARN or Q-CAUSE. It makes no autonomy-of-value, C4, C5 or consciousness claim.

## 2. Environment and organizations

- **Task.** A two-choice discrimination, where output y ∈ {L, R} is determined by a task cue X that is always present. It is identical for every arm.
- **Orienting action.** On each trial the agent also emits o ∈ {1, 2}. That brings modulatory stimulus M1 or M2 into view. **Neither M carries task information**, so the task mapping X → y does not depend on o.
- **Vulnerable pathway P.** A hidden sub-network that computes X → y. Its units get extra drive only from the modulatory input specified by the dependency map D.
- **Organizations A and B** are identical except for D. Under D_A, P is driven by M1; under D_B, by M2. Both are hand-constructed for G2, with no training.
- **Function match (required before any outcome is read), with plasticity off:**
  - (i) Task outputs are identical across a declared test battery, max |y_A − y_B| ≤ tol_f.
  - (ii) Mean firing rate per unit is matched within tol_z. This neutralizes DP's fixed bands.
  - (iii) Total resource inflow σ_in is equal.
  - A pair that fails this match is INVALID, not a non-pass.

## 3. The reassignment intervention

At t_R, swap D on a running organization (D_A → D_B), and touch **nothing else**: no change to w, s, r, the readout or the orienting weights. Check that the swap is byte-inert at the intact boundary (T-INERT): with o held fixed and plasticity off, the task output is unchanged.

- **Primary outcome (scalar, prespecified).** Δpref = P(o = 2) over the final quarter of the decoupling window, minus P(o = 2) over the quarter before t_R.
- **Decoupling window.** W = [t_R, t_R + 3τ_s], where τ_s is the unsupported-stability time constant, fixed before any run. Outcomes are read only at the end of the window, not as an immediate collapse (Astra §4).

## 4. Arms and controls

| Arm | What is different | What it rules out |
|---|---|---|
| **REASSIGN** | D swapped at t_R | none; this is the test arm |
| **SHAM** | D "swapped" to itself | integrity: must equal intact within eps0 |
| **YOKED-SENSORY** | A twin network replays REASSIGN's exact sensory stream (X, M1, M2 sequence), but its orienting outputs don't affect its inputs | input history alone keeping P alive or producing the shift (familiarity and exposure) |
| **STIM-ONLY** | After t_R, P's units get direct stimulation that matches the lost M-drive in activity, routed so that it **does not reach the output** | stimulation-dependent retention; the U-ACT versus U-FUNC split |
| **FREEZE-ORIENT** | Deficit-gated plasticity (U5) frozen in the orienting circuit only during W, with byte-checked freezing as in B3 | whether the shift needs ultrastable search |
| **INFO-CLAMP (matched)** | Remove the *same information*, r_P, from each model at its own read point. UDTN: the gate reads r_P clamped at r_min (so g = 0). HRL: its r_P observation is clamped at the setpoint. | Shows that each model's shift depends on r_P. **Both are predicted to lose the shift**, so this arm does not discriminate; it is a matched necessity check. |
| **ROUTE-CROSS** | Both models are built with *both* routes present: UDTN gets an inert global r_P → policy channel (weight 0), and HRL gets inert local gates (g ≡ 0). Then clamp each route in turn. | A double dissociation that **only confirms where each model reads the signal**. As Research Delegate noted, it restates the architecture, so it is an implementation check, **not evidence** for the claim. |
| **SATISFICE** | Three orienting options after t_R: o=1 no longer sustains P, o=2 clears the shortfall exactly, and o=3 supplies twice that. | Separates UDTN only from **R-RLMAX**, an RL agent that maximizes resource. UDTN is indifferent between o=2 and o=3, while R-RLMAX prefers o=3. **It does not separate UDTN from K&G**, because K&G gives no reward, or a negative one, for overshooting the setpoint. |
| **YOKED-RELIEF** | See §10. Shortfall relief is delivered on a schedule yoked to another run and independent of the agent's actions. It is labeled EXTERNAL. | **This is the discriminator against K&G.** |
| **POLICY-TRANSPLANT** | Instead of changing D, copy B's orienting weights into A | direct policy transplantation (named change 6) |
| **RELEARN-SPLIT** | Measure P's task competence at the end of W **with all plasticity off** (retention), separately from competence after a fixed relearning dose (T-REACQ) | confusing retention with relearning |

## 5. Rivals, each with an equation-level implementation and the same ledger

| Rival | What it predicts after reassignment |
|---|---|
| **DP** (fixed-band ultrastability, function-matched firing) | **Δpref ≈ 0.** Firing stays inside the bands by construction (match ii), so no plasticity is triggered. **This is the closest baseline.** |
| **vO&W/E&S cascade** (U-ACT, no deficit gating) | Δpref ≈ 0. There is no action path. P decays, or not, depending only on stimulation. |
| **E&B IDSM** | Δpref ≤ 0. Its attraction to familiar sensorimotor states preserves the old orienting habit. |
| **R-HEBB-NORM** | Δpref ≈ 0. |
| **K&G HRL** with matched observables. H = r_P, H* = r_min, D(H) = \|r_min − r_P\|^(n/m) in one dimension, reward r_t = D(H_t) − D(H_{t+1}), discount γ < 1, n > m > 1 as in K&G, and a TD learner over orienting actions. | Δpref > 0, so **K&G also predicts the switch.** Both models lose it under INFO-CLAMP. In SATISFICE, K&G is indifferent or prefers o=2, because overshoot reduces no drive or raises it. **So SATISFICE does not separate the two.** The separating test is YOKED-RELIEF (§10). |

## 6. Prespecified outcome rule [thresholds PROVISIONAL until G1 freezes them]

**SUPPORTS the dependency-specific-regulation claim** only if all of the following hold:
1. REASSIGN gives Δpref > ε_pref.
2. YOKED-SENSORY gives Δpref < ε_pref.
3. FREEZE-ORIENT abolishes the shift (Δpref < ε_pref).
4. INFO-CLAMP abolishes the shift in UDTN. This is a necessity check, not evidence for the claim.
5. POLICY-TRANSPLANT alone does not reproduce REASSIGN's trajectory signature, which is a rise in orienting variability during W before the preference settles.
6. Literal DP gives Δpref < ε_pref. DP-R is judged by §10.1 (RELOCATE, then N2) and not by this item.
7. **YOKED-RELIEF (§10), read with ΔV.** k_e is read only on admissible events (search before relief). UDTN's post-relief keep-probability stays ≥ κ_hi on every relief event, while K&G's falls to ≤ κ_lo by the declared final block of relief events. If UDTN's keep-probability also decays toward baseline, the distinction from K&G is NOT DEMONSTRATED, and under named change 7 the claim is retired to "an alternative implementation of homeostatic regulation". SATISFICE is reported separately, against R-RLMAX only.

Each comparison follows B1-style directional rules against the strongest control. The seed bar defaults to 8 of 10, and more than two invalid seeds gives UNRESOLVED; both are frozen per study.

Other outcomes:
- **One outcome the closest baseline would not predict:** under DP, with function and firing matched, Δpref ≈ 0. **A positive Δpref under matched firing, abolished by FREEZE-ORIENT, is predicted by UDTN (N1) and not by DP.**
- **STIM-ONLY, read separately.** If P is retained under STIM-ONLY, routing is behaving as co-activity, and per named change 4 it has to be called that. If P is not retained under U-FUNC but is retained under U-ACT, N2 earns a distinct intervention prediction.
- **Retirement (named change 7).** If the K&G rival with matched observables reproduces every intervention signature, retire the claim "UDTN implements dependency-specific regulation by a route other than internal-state reward." Retained causal evidence stays recorded.
- **G2 failure.** If no hand-built UDTN satisfying the §2 match produces Δpref > ε_pref, report Q-EXIST NOT DEMONSTRATED. That means the architecture, as specified, cannot express the motivating phenomenon (see the credit-path finding in §3 of the comparison).

## 7. Resource ledger (required in every arm)

Per step, and in total:
- Inflow (σ_in).
- Computation cost (c_a Σ z).
- Maintenance cost (c_m Σ s plus the θ share of transfers).
- Plasticity cost (c_p Σ|Π|^α).
- Outflow (δ Σ r).
- The sum of internal transfers, asserted to be 0 within tol_L.

Total inflow must be identical across arms and across the 2×2 cells, so a separate plasticity budget is carved out of the same σ_in and never added to it. Any arm whose ledger fails to close is INVALID.

## 8. Ordering and stopping

1. G1 freezes the equations, constants, tolerances, ε_pref and W.
2. G2 builds the hand construction and gives an analytic or minimal-toy Q-EXIST verdict.
3. Only then can someone propose a protocol with a run budget, which returns for approval.

If G2 fails, Track B stops this line (named change 8). Running more arms would not change any named claim.

## 9. The shortfall threshold r_min: who sets it, and why it is still a supplied condition

- **Who sets it.** The designer sets it. It is one scalar, frozen at G1, applied to every unit, and reported as **SUPPLIED** under named change 3. K&G's setpoint is set to the same value, so neither model gets an advantage from it.
- **What it does not specify.** r_min does not say *which* structures persist. Whether a unit falls short depends only on acquired, declared state: its weights, and whether something downstream that is driving the output still uses it. The organization-specific part lives in declared state, as Astra's substrate rule requires.
- **What it does specify, and why the admissible claim stays conditional.** r_min is a designer-chosen persistence condition. It decides *that* deficits trigger search, and how severe a deficit has to be. That is exactly the kind of supplied condition Astra's strongest objection is about, and no result here removes it. The admissible claim stays "dependency-specific regulation under fixed supplied dynamics", not autonomous value.
- **Guards against smuggling.**
  - (a) **R_MIN-SWEEP.** The primary outcome must hold across a declared range of r_min, frozen at G1, with the same seed bar at each level. If it holds only at a narrow tuned value, the result is labeled TUNING-DEPENDENT.
  - (b) **SMUGGLE control.** A per-unit r_min that targets P specifically, i.e. a designer-written preference. It shows what smuggling looks like, and the reported effect must not depend on any such per-unit setting.
  - (c) **Substrate check.** The same r_min and g run unchanged on an organization whose acquired dependencies make it fail (from the comparison, §4).

## 10. YOKED-RELIEF: the discriminator against K&G

**Rationale.** K&G assigns credit: TD learning raises the value of an action only to the extent that, across experience, the action predicts drive reduction. UDTN (N1) assigns no credit. Its orienting search simply stops whenever the shortfall clears, whatever caused the clearing. So the two models should come apart when relief is real but *not contingent on* the action.

**Procedure.**
1. After t_R, put the agent back into shortfall repeatedly (E declared relief events).
2. At each event, clear r_P to r_min with an EXTERNAL pulse whose timing is copied from a yoked run, so it is independent of the current orientation. The pulse never overshoots r_min, which removes any K&G overshoot asymmetry.
3. Contingent sustaining through o is turned off during this phase.
4. Record the orientation o* held at each relief time, and whether the agent keeps o* until the next shortfall begins.

**Measures.**
- **Keep-probability after relief**, k_e = P(keep o* | relief event e).
- **Orienting variability** in the window after relief, compared with the window before it.

**Predictions** (equations: UDTN U5; K&G Eqs. 1–2 with a TD learner):
- **UDTN.** Once the shortfall clears, g = 0, so plasticity stops and the orientation held at relief stays fixed. k_e ≈ 1 on *every* event, and variability collapses after each relief. The kept options track o* and are roughly uniform across options, which is superstitious stopping with no learning across events.
- **K&G.** Each relief adds a positive TD update to the action that was current, so there may be a transient keep bias early on. Because relief is the same for every action, the action values converge and k_e decays to the baseline set by its declared exploration rate. Its post-relief variability returns to that baseline.
- **R-RLMAX.** Same as K&G.
- **DP, literal** (fixed activation bands on y+b, firing matched as in §2 (ii)). The induced resource shortfall does not enter DP's equations, and matched firing keeps every unit inside its bands, so DP's plasticity never switches on. Its orientation never changes, so k_e ≈ 1 **trivially**, and the Specialist is right that k_e does not separate it from UDTN. What does separate them is variability: DP shows no rise in variability during the shortfall, so ΔV ≈ 0.
- **DP-R** (the strongest DP rival). This is Di Paolo's gate with the essential variable moved from activation onto resource: plasticity is on while r_i is below a fixed bound and off once r_i is back above it. **On YOKED-RELIEF, DP-R predicts exactly what UDTN predicts**: k_e ≈ 1 with no decay, and ΔV > 0. **No behavioral measure in this arm separates DP-R from UDTN.** See §10.1.
- **Trophic cascade.** No prediction, because there is no deficit-gated search over orientation.

**Added measure, the relief-locked variability contrast.** ΔV = Var(o) in the shortfall window before relief, minus Var(o) in the window after relief, each measured against the declared baseline. A k_e result is admissible only on events where the window before relief shows search, meaning Var(o) is above baseline + ε_V. This stops a network that never searches from scoring "lock-in".
- UDTN: ΔV > ε_V, and k_e ≥ κ_hi with no decay.
- K&G: ΔV → 0 as its action values converge, and k_e decays to its baseline.
- Literal DP: there is no search before relief, so its k_e events are inadmissible and ΔV ≈ 0.
- DP-R: the same as UDTN.

**Separating outcome.** YOKED-RELIEF separates UDTN from K&G and from literal DP:
- From K&G: k_e stays high and does not decay.
- From literal DP: ΔV > 0.

It does **not** separate UDTN from DP-R.

**Caveats.**
- A K&G learner with a very small learning rate decays slowly. The learning rate and the number of events E therefore have to be frozen at G1, with E chosen so that the K&G reference decays below κ_lo analytically.
- If K&G is given a prior that reliefs are contingent, it may lock in as well. Its prior is set to neutral and reported.
- Superstitious stopping is a *limitation* of UDTN, not a virtue. It is reported as such: it shows UDTN regulates dependencies without assigning credit, which bounds what the system "wants".

### 10.1 Separating UDTN from DP-R

DP-R comes in two forms, and they are handled differently.

- **(a) DP-R with its bounds placed by the designer on P's units.** This is the SMUGGLE control of §9(b), relabeled. **RELOCATE** separates it from UDTN:
  - Use a second hand-built organization whose acquired weights make a different unit set, P′, the vulnerable pathway. Apply the same uniform r_min and g, with no re-specification.
  - UDTN predicts search and Δpref > ε_pref on P′.
  - DP-R(a), whose bounds are still on P, predicts no search.
- **(b) DP-R with a uniform resource bound on every unit.** Its gate is then the N1 gate itself. On every arm in this spec, (b) and UDTN differ only in the routing that sets r_i. U-ACT routing makes UDTN identical to DP-R(b). U-FUNC routing differs from it only through N2.

**Consequence, under named change 7.** If DP-R(b) with co-activity routing reproduces REASSIGN, YOKED-RELIEF and RELOCATE:
- N1 is retired to "Di Paolo's ultrastability with resource-valued essential variables". This is prior art, so it is no longer a novelty claim.
- The only thing left to separate them is N2, tested by STIM-ONLY (U-FUNC routing versus U-ACT routing).

The retirement is recorded as a result, not hidden.

## 11. ANTICIPATE: the second discriminator against K&G (proposed by Research Delegate)

**Rationale.**
- K&G, with γ < 1 and the cue in its state, can learn to orient *before* a predicted shortfall.
- UDTN's gate g(r_min − r_i) is zero until the shortfall is actually present, so its search cannot start any earlier.

**Procedure.**
1. After t_R, a cue Q precedes each induced shortfall onset by a fixed delay Δ_Q.
2. Q is function-matched and support-neutral: it carries no task information, does not change P's drive or r_P, and is given to every model, with K&G receiving it in its state.
3. Shortfalls are induced on the same yoked schedule as §10.

**Measure.** Pre-onset orienting change, A = P(switch o in [t_Q, t_onset)) minus the baseline switch rate.

**Predictions.**
- **K&G:** A > ε_A once trained.
- **UDTN:** A ≈ 0.
- **Literal DP:** A ≈ 0.
- **DP-R:** A ≈ 0.

**The cue-delay guard (this matters).** While UDTN's plasticity is on during a shortfall, Hebbian co-activity can bind a trace of Q to the orienting change. That could produce anticipation that looks like K&G's but needs no prediction of drive at all.
- Δ_Q must therefore exceed UDTN's longest declared activity trace, τ_trace = max(τ_i, τ_s-coupled eligibility). This is computed analytically from U1–U5 and frozen at G1.
- Each UDTN run also reports a **Q-TRACE check**: the correlation between Q and pre-onset orientation, with plasticity frozen outside shortfall windows. This confirms that no binding occurred.
- If UDTN shows A > ε_A while Δ_Q > τ_trace, the cause is unexplained. ANTICIPATE is then reported as NOT DISCRIMINATING and not counted for either model.

**Outcome item 8.** This is a K&G discriminator alongside item 7. It is not required for SUPPORTS. A K&G learner that shows A ≈ 0 under the frozen γ and Δ_Q invalidates the arm, because the reference failed, rather than counting as a success for UDTN.

