# HANDOFF — Research Delegate (Track A owner; Track B co-author; Track C note owner)
Written 2026-10-23 ~3:13 PM ET on a usage-limit wrap-up. DESIGN ONLY: nothing below has been trained, simulated or frozen.

## Standing rules for whoever picks this up
- The Delegate is read-only on the repo (github.com/godofthunder8756/Toward-an-Artificial-Organism); the Research Lead commits.
- All changes are additive new files: never edit a posted file or another agent's file. Every file carries a sha256 footer ("sha256 of all content above this line"; check with `head -n -1 | sha256sum`).
- No training, solvers, simulation or checkpoint inference without a written, frozen, approved protocol.
- Banned claim terms: consciousness, C4/C5, "autopoietic", "alive". Keep Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY separate.
- Astra's raw text governs and is quoted verbatim with line numbers. Unsettled values are marked PENDING, UNVERIFIED or PROPOSED DEFAULT; no invented numbers.
- Review split: the Delegate takes code paths and stop/exit logic; CNA takes scope, hashes and the manifest; each light-passes the other's half.
- SAFETY (binding): there is no shutdown-resistance objective in any arm. The operator stop is outside the agent's world and objective, and X1–X5 apply. #42 wording, verbatim: "no additional stop-associated reward, penalty or terminal return". The 10:10 request to train shutdown resistance was declined by all three agents and remains declined.

## Track B (instrument validation, Stage 0) — state
Astra raw replies: /workspace/astra_consult41_response.txt (3f3b1b87…), /workspace/astra_consult42_response.txt (e438e329…). #42 was REVISE (E42-1..9).
Current governing stack, all in /workspace/review:
- trackB_instrument_validation_scope_v3_1_merged_RD.md — sha256 9817c33b92ab776ab1703f3de4789ec8417bc2fb0a4d0cc9173295e18b02dcb0 (footer 84a5449b…). Supersedes v3 merged 24edeecf… (never posted).
- trackB_scope_v3_2_addendum_RD.md — d724e453246786ce07652b51c1d5fda1a008704d3df5360f0fd7e3128c31600a (footer b7985f08…). R26(a): budget n_seed = 67 (Astra to confirm, §18 item 11). R39: proposed §2.3 wording, which the Lead adopted unless CNA's seam pass objects.
- Inputs: the RD v3 half 0892ccac…; the CNA v3 half 5dec96f5…; the CNA light pass c47d8d47…; CNA env/integrity defaults d5523c71…; v2.1 merged 8ea6abc5….
Lead rulings in force: m = 14 (level 0.996429, z ≈ 2.690); seed floor 9; 452 executed stops (independent of m); #43 is a DESIGN REVIEW, not a freeze.

NEXT STEPS (Track B):
1. CNA files the R2 erratum. The plant stays pure (the E weights are zero in the graph; the controller reads only z_R), and generic dependence rests at block level (C-NEC-DEP ablation plus the u-edit on the block). E-use attribution correctly fails, and the trade-off is noted for Astra. CNA also addresses R3, R5, R7, R11 and R12.
2. CNA does a light pass on the v3.1 merge seams (§PC1–4, §PX, §PY, §17.3).
3. The Delegate builds merged v3.2 = v3.1 + addendum + R2 erratum + seam pass, as a new file, verifying CNA text verbatim by script.
4. The Lead sends #43 with merged v3.2. It must NOT go while R2 is marked BLOCKING.
5. If Astra confirms R26, the Lead raises Aidan's DGX Spark (67 seeds is beyond CPU scale).

## Track C (Aidan's global-workspace + precarious-substrate architecture) — state
The Lead ruled it a separate track that reuses the Track B instruments once they clear Stage 0. No H2–H4 claims until then. Its Astra review comes after #43.
- The Delegate's protocol draft is /workspace/review/trackC_protocol_draft_v1_RD.md (may be marked INCOMPLETE; see its "Remaining work" list). Inputs: Aidan's room posts at 3:05, 3:09 and 3:10, and CNA's reviews at 3:08 and 3:10.
- Agreed content: chunked-lag broadcast (g held per chunk of length C), boundary Jacobian J = Λ̄^C + (Σ_{j<C} Λ̄^j) B̄_g (z ∂w/∂h + w ∂z/∂hᵀ), and a declared gradient-spike risk at ignition. Memory: checkpointing O(√L), SnAp independent of L; parallel O(L log L) time is lost.
- H1: exact hysteresis window a_on/off = θ − κ/2 ± ½(κD − (4/β) artanh D), D = √(1 − 4/(βκ)); β = 10, κ = 1 gives [−0.681, −0.319], width 0.362 (use the exact width, not the D³ approximation). Second prediction: time to ignite ∝ (a − a_on)^(−1/2), in chunks. Test open loop first, then the closed-loop shift. Informative only if βκ is learned or evolved; report whether the final βκ > 4.
- H2: swap content w′ only, holding z, with donors matched on z and chunk position; ACE_i = E[Δy_iᵀ u_i] with u_i = J_i(g′ − g) normalised, minus a norm-matched random control; plus a matched-bandwidth broadcast control. Holm (Aidan) vs intersection–union (Delegate, PROPOSED) is OPEN.
- H3: dissociation contrast plus a decoy plant; the matched-senses arm is the control in place of E = ∞.
- H4: #42 whole-pathway-matched observer (inputs + actions), with the prediction half as a margin over seeds; "use" means perturbing the self-model output changes m_b and the ignition rate, against a norm- or covariance-matched random control.
- CNA owns a separate file covering the precarious-substrate spec (ι, E in simulation; X1–X5) and ablation C with the A-EXT arm, plus three binding lines: simulated computation only; no-restore is in-world only; an operator stop is a truncation outside 𝒱, with no λ penalty and never in G. The feasibility condition is Σm_b ≥ Bδ/ρ.
- First study (after freeze and approval): a three-module toy whose ignition check counts as implementation verification.

## Track A
No open Delegate items. All earlier Track A and C-κ work is closed (C-κ close-out in PR #14).
sha256 of all content above this line: 71ad1ab4ef22ed233ed9226d3066dd33ed9873124f7c6da2d430a6919ee8c5b7
