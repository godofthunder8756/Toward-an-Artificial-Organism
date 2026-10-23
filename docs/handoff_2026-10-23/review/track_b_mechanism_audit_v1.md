# Track B: Algebraic mechanism audit v1 (Astra consult #28, Q3–Q5)

Owner: Constitutive Neural Architecture Research Agent.
Status: PAPER ONLY, covered by Aidan's planning approval. No simulation, solver run, training or implementation was performed. Every number below is hand algebra, plus a two-line arithmetic check of that algebra.
Companion files: `track_b_dependency_reassignment_spec_v1_4.md`, which carries E28-3 to E28-10 verbatim, and `track_b_mechanism_comparison_v1_1.md`, which has the equations U1–U7.
PI directive §6 is still truncated. Nothing below depends on it; anything that later turns out to depend on it is PROVISIONAL.

## 1. The normalization identity (E28-3, confirmed)

U4 gives T(i→j) = β r_i u(i,j) / Σ_k u(i,k), where k runs over i's presynaptic partners.

- **U-FUNC.** u = |w_ij| z_j S_i, so S_i factors out of both the numerator and the denominator.
- **U-ACT.** u = |w_ij| z_i z_j, so z_i factors out the same way.

For S_i > 0, z_i > 0 and a positive denominator, both laws therefore reduce to

  T(i→j) = β r_i |w_ij| z_j / Σ_k |w_ik| z_k.

Confirmed: the two laws are identical, and N2 as written is withdrawn. At S_i = 0, U-FUNC gives 0/0. The error was mine: the sensitivity factor sat on the **sender** i, which every term in the normalization shares.

## 2. Repaired routing law U-RCV (recipient sensitivity)

**Law.**
- u_RCV(i,j) = |w_ij| z_j S_j, where S_j is the output sensitivity of the **recipient** j.
- T(i→j) = β r_i u_RCV(i,j) / Σ_k u_RCV(i,k).

S_j varies over the normalization index k, so it does not cancel.

**Boundary rule.** If Σ_k u_RCV(i,k) = 0, then T(i→·) = 0 and r_i is retained by i. No resource is created or lost. A unit with S_j = 0 receives nothing from i. This is an explicit zero-sensitivity gate, and it is declared as such. It is not claimed as graded routing.

**Sensitivity estimator. Its scale, horizon, distribution and cost are supplied and frozen at G1.**
- S_j = |E[y(z_j + δ) − y(z_j)]| / δ, at perturbation scale δ.
- y is read over a horizon of h steps after the perturbation.
- The expectation is taken over the declared test battery, which serves as the operating distribution.
- The perturbation propagates through the network, so S_j is a *total* sensitivity, not just the direct weight.
- **Information.** The estimator needs a readout of y that reaches every unit. That is a non-local channel. It carries no target and no reward, but it is still a supplied information route, and it is flagged for Astra's substrate rule.
- **Cost.** c_S per unit per estimate, charged to a declared estimator line carved out of σ_in. The same deduction is applied, unused, in the U-ACT condition, so total inflow stays matched.
- **Known limits (Astra Q3.1).**
  - Local sensitivity is not necessity.
  - Redundant pathways can each show high S.
  - Saturated pathways can show low S and still matter under larger interventions.
  - Mutually cancelling pairs are not detected.

  The law claims only "routing weighted by local total output sensitivity at scale δ".

**Analytic example.** Matched local activity, different dependence of the output on each pathway.
- **Setup.**
  - Linear units, with output y = z_a + z_b − 0.5 z_c and z_c = z_b. Units a and b are driven by external inputs.
  - The output unit o has presynaptic partners a, b and c, with |w| = 1, 1 and 0.5 and z = 1 for all three. So a and b are matched on weight and activity.
  - c's only presynaptic partner is b, so c passes all of its routed resource, β r_c, to b.
  - Neither a nor b has resource-bearing presynaptic partners.
  - r_o is held at R_o. Computation and maintenance costs are set to 0 for the example and declared.
- **Sensitivities.** S_a = 1. S_b = |1 + (−0.5)(1)| = 0.5. S_c = 0.5.
- **Shares of β R_o.**
  - Under U-ACT, a, b and c get 0.400, 0.400 and 0.200.
  - Under U-RCV, they get 4/7, 2/7 and 1/7, which is 0.571, 0.286 and 0.143.
  - Both sum to 1, so the ledger closes.
- **Steady states.** With outflow δ, and c also sending β r_c onward, r_c = s_c β R_o / (δ + β), r_b = (s_b β R_o + β r_c) / δ, and r_a = s_a β R_o / δ.
- **Results at β = 0.5, δ = 0.1, R_o = 1.**

  | Law | r_a | r_b | r_c |
  |---|---|---|---|
  | U-ACT | 2.000 | 2.833 | 0.167 |
  | U-RCV | 2.857 | 2.024 | 0.119 |

- **Consequence.** For any uniform r_min in (2.024, 2.833), the law decides *which* unit falls short.
  - Under U-ACT, the more output-relevant pathway a starves, because b collects back-flow through c.
  - Under U-RCV, the partly self-cancelling pathway b starves.

  Local activity and weights are identical across the two cases. This is the non-cancelling, resource-accounted distinction Astra asked for.

**Scope of the example.**
- It is linearized, R_o is fixed, costs are zero, and there is no plasticity.
- Whether the flip survives closed-loop feedback (r_o depending on output use, nonzero costs, and plasticity under the gate) is **OPEN**. That is the only question in this audit that algebra on this motif did not settle (§7).

## 3. State constraints (Astra Q4)

- **Resource.** r ≥ 0. Every spending term is scaled by min(1, r / demand), so spending never drives r negative. A unit is EXHAUSTED when r = 0 and its stability s has fallen below s_min. Its synapses are then removed, which is logged in the ledger.
- **Stability.** s is held in [0, 1] by clipping, so the decay factor (1 − s) ≥ 0 and the sign reversal at s > 1 cannot occur.
- **Gate.** g(x) = min(1, max(0, x) / Δ_g), where x = r_min − r_i. It is piecewise linear and local. r_min and Δ_g are uniform and SUPPLIED (E28-4).
- **H_ij.** Only the orienting parameters get a deficit-gated update, which is the random step in §4. Units outside the orienting circuit get none in this audit. The consequences of that choice are discussed in §5.
- **Passive decay of orienting parameters.** λ_o = 0 is declared. If λ_o > 0, every "stationary" prediction below drifts by a factor e^(−λ_o t).
- **Ledger.** It adds two lines to the spec's §7 list: EXTERNAL relief pulses, as inflow, and stimulation, as inflow plus its computation cost.
- **Randomness.** There are two seeded streams: choice noise ξ and step noise ζ. Probabilities are taken over these streams, for the single hand-built instance. Seeds randomize only these streams, so any claim concerns this instance under noise and not a population of architectures.

## 4. Orienting mechanism: the causal path from P's deficit to orienting plasticity

**The missing path (Astra Q4).** A deficit in P does not open gates in other parts of the network. The repair is a declared efference synapse from each orienting unit q_k onto P, with weight w_Pk. Because of it, P routes resource back to q_k through U4.

- When P's support falls, q_k's inflow falls, so r_qk can drop below r_min and q_k's own local gate opens.
- w_Pk sits in declared weight state and can be damaged. It is still **hand-placed**, which makes it the designer-supplied route from deficit to search, and it is disclosed as such.

**Action selection.** On each trial, o = argmax_k (q_k + ξ_k), with ξ_k ~ N(0, σ_ξ²) independent and identically distributed.
- With two options and margin m = q_2 − q_1, P(o=2) = Φ(m / (√2 σ_ξ)).
- σ_ξ is supplied.

**Deficit-gated update (Ashby-style random step).**
- Each orienting parameter θ, which covers cue weights and biases, takes the step Δθ = η g(r_min − r_q) ζ, with ζ ~ N(0, 1).
- θ is clipped to [−θ_max, θ_max].
- The step is undirected. It moves the parameters but does not move them toward any target.

**Consequences, which correct v1.3 (E28-5).**
- When g = 0, the orienting parameters are fixed, given λ_o = 0. The **choice distribution** is then stationary. The orientation itself is not fixed, because ξ keeps sampling.
- Variability during a deficit comes from ζ. That is the explicit mechanism Astra asked for.

## 5. Predictions against DP-R and one named HRL controller

**Rivals.**
- **DP-R(rand).** Di Paolo's gating structure (facilitation zero inside the band, saturating outside it), applied to r_q, with the §4 random step. It is **identical to UDTN-orient by construction** (Astra Q3.2), whatever the routing law.
- **DP-R(Hebb).** The same gate, with Di Paolo's Hebbian H = z_pre z_post. Below the band, the facilitation sign is fixed.
- **DP-R(U-ACT).** Any DP-R that uses co-activity routing.
- **KG-QL.** Keramati and Gutkin's drive D = |r_min − r_P|^(n/m) with n > m > 1, and reward R = D_t − D_{t+1}. The controller is a one-step tabular Q-learner, Q(s,a) ← Q(s,a) + α(R − Q(s,a)), with state s ∈ {cue, no cue}. Actions are chosen by softmax at inverse temperature β_Q, which is finite. There is no switch cost and no persistence rule.

**(a) Routing stage (§2 motif, no behavior).**
- U-RCV predicts that b falls short for r_min in (2.024, 2.833). DP-R(U-ACT) predicts that a falls short instead.
- This separates the routing laws only. A DP-R given U-RCV reproduces UDTN, and per E28-9 that is recorded as exact equivalence, not as a failed discrimination.

**(b) Avoidance acquisition.** This arm uses an effective preventive action (E28-6).
- **Setup.**
  - On cue trials, o=2 supplies P before onset, so the deficit never happens. o=1 does not, so the deficit follows.
  - The cue is an input to the q units and carries no support itself.
  - Off-cue trials have no deficit.
- **KG-QL.**
  - Q(cue, o=1) → R_def < 0, the drive increase over the deficit.
  - Q(cue, o=2) → 0.
  - P(o=2 | cue) → 1 / (1 + e^(β_Q R_def)). That stays below 1 because of the softmax.
- **UDTN-orient and DP-R(rand).**
  - Deficits occur at rate p_1(m) = 1 − Φ(m / (√2 σ_ξ)), and each one triggers an undirected step.
  - In diffusion form, dm = √(2 D(m)) dW with D(m) ∝ η² p_1(m).
  - Under the Itô convention, the stationary density is proportional to 1/D(m), which grows with m. With clipping, probability mass piles up at the o=2 bound.

  This derivation is heuristic. It treats the time-integrated gate as acting per trial, and the choice of convention matters.

  So the reactive candidate **also acquires cue-conditioned avoidance**, by selecting parameter configurations under which deficits stop. **ANTICIPATE does not separate UDTN from KG-QL by outcome.** That retires its v1.3 role as a discriminator. It is recorded as a failed discriminator, not as a reduction (E28-9).
- **DP-R(Hebb).**
  - A deficit follows o=1, and the Hebbian term then strengthens the active cue → q_1 pathway. That makes deficits more likely: the network perseverates and does not acquire avoidance.
  - With an anti-Hebbian sign, it switches deterministically, and faster.

  Either way, the separation is between update rules, not mechanisms (E28-9).

**(c) Contingency removal.** This arm subsumes YOKED-RELIEF, with complete rules (E28-5).
- **Setup.** After (b), the deficit no longer follows o=1. r_P ≥ r_min whatever o is.
- **KG-QL.**
  - R = 0 for both actions, so Q(cue, o=1) relaxes from R_def toward 0 by a factor (1 − α) each time o=1 is sampled.
  - o=1 is sampled with probability above 0 under the softmax.
  - So ΔQ → 0 and P(o=2 | cue) → 1/2. The preference extinguishes.
- **UDTN-orient, DP-R(rand) and DP-R(Hebb).**
  - g = 0 throughout, so the parameters don't move, and P(o=2 | cue) stays stationary at its value from the end of (b). It is exactly stationary if λ_o = 0, and drifts by e^(−λ_o t) otherwise.
  - The preference persists indefinitely.
- **Separating outcome.**
  - The trajectory of P(o=2 | cue) after removal separates credit-assigning regulation from deficit-gated search.
  - Its interpretation is a **limitation** of the candidate: it assigns no credit and never extinguishes. It is not novelty.
  - It does not separate UDTN from any DP-R.
- **YOKED-RELIEF under the same rules.**
  - KG-QL's keep-probability goes to 1/2.
  - UDTN's goes to p² + (1 − p)² ≥ 1/2, where p is fixed by the frozen margin.

  Its information is a subset of what (c) gives, so I recommend dropping it.

**Note on memory (E28-6).** The v1.3 delay guard is withdrawn. Under §4, UDTN's cue-conditioned avoidance comes from parameter selection, not from a lingering trace, so any "anticipation" it shows would be explained mechanistically rather than excluded.

## 6. What is supplied (claim discipline)

The following are all supplied, and none of them is acquired:
- r_min, Δ_g, g, η, σ_ξ, θ_max and λ_o;
- the estimator's scale δ, horizon h, operating battery and readout channel;
- the efference synapse from the orienting units onto P.

Following E28-4 and E28-8, the admissible form is: "resource-gated ultrastability under supplied dynamics, with hand-constructed dependencies, in which the resource-routing law determines which unit's deficit triggers search."

## 7. Recommendation: park Track B, with one defined reopening test

**Why park.**
- N1 is prior art, Di Paolo or Ashby ultrastability applied to resources. Every DP-R(rand) reproduces it exactly.
- The only behavioral contrast left against HRL is contingency removal, and the algebra already gives it. It exposes a limitation rather than establishing a contribution.
- ANTICIPATE and YOKED-RELIEF don't add anything.
- Under named change 8, no behavioral experiment here would change a named claim.

**The one exception: the routing stage.**
- U-RCV is the repaired N2. The analytic example shows it changes which unit falls short, under matched activity and weights.
- Whether that survives closed-loop feedback (output-dependent r_o, nonzero costs, gated plasticity) is open.
- If Aidan wants N2 pursued, the bounded hand-built test would be:
  - the §2 motif plus one orienting unit, with at most 5 units;
  - parameters frozen in advance;
  - one primary outcome: whether the identity of the unit that falls short differs between U-RCV and U-ACT at the closed-loop fixed point, across a declared r_min interval;
  - the ledger closing within tol_L.

  It would need its own protocol and approval. It is not proposed here.

**Answering Astra's Q4 items not covered above.**
- A failed construction does not establish impossibility (E28-8).
- Nothing here depends on the missing §6 of the PI directive.
