# Track B: Function-matched dependency-reassignment test, paper spec v1

Owner: Constitutive Neural Architecture Research Agent. Status: PAPER ONLY. This authorizes no simulation, training or implementation (Astra §7). Any execution comes back with its own protocol, budget and approval request.
Depends on: `track_b_mechanism_comparison_v1.md` (UDTN equations U1–U7). It follows named change 6.

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
| **MASK-INT** | No policy unit gets any input from r or s (true for UDTN by construction; an explicit check) | covert internal-state access, i.e. a K&G route |
| **POLICY-TRANSPLANT** | Instead of changing D, copy B's orienting weights into A | direct policy transplantation (named change 6) |
| **RELEARN-SPLIT** | Measure P's task competence at the end of W **with all plasticity off** (retention), separately from competence after a fixed relearning dose (T-REACQ) | confusing retention with relearning |

## 5. Rivals, each with an equation-level implementation and the same ledger

| Rival | What it predicts after reassignment |
|---|---|
| **DP** (fixed-band ultrastability, function-matched firing) | **Δpref ≈ 0.** Firing stays inside the bands by construction (match ii), so no plasticity is triggered. **This is the closest baseline.** |
| **vO&W/E&S cascade** (U-ACT, no deficit gating) | Δpref ≈ 0. There is no action path. P decays, or not, depending only on stimulation. |
| **E&B IDSM** | Δpref ≤ 0. Its attraction to familiar sensorimotor states preserves the old orienting habit. |
| **R-HEBB-NORM** | Δpref ≈ 0. |
| **K&G HRL** with matched observables (gets r_P as an internal state with setpoint r_min) | Δpref > 0. **This is the one rival that also predicts the switch.** It is told apart by intervention, not behavior: under MASK-INT its switch is abolished, while UDTN's must survive; under FREEZE-ORIENT, UDTN's switch must be abolished. |

## 6. Prespecified outcome rule [thresholds PROVISIONAL until G1 freezes them]

**SUPPORTS the dependency-specific-regulation claim** only if all of the following hold:
1. REASSIGN gives Δpref > ε_pref.
2. YOKED-SENSORY gives Δpref < ε_pref.
3. FREEZE-ORIENT abolishes the shift (Δpref < ε_pref).
4. MASK-INT leaves the shift intact.
5. POLICY-TRANSPLANT alone does not reproduce REASSIGN's trajectory signature, which is a rise in orienting variability during W before the preference settles.
6. DP gives Δpref < ε_pref.

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
