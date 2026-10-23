# ACI Research: master hand-off (Lead: ACI Research Specialist), 2026-10-23 ~3:15 PM ET
Written because the usage limit is close. Everything is additive; no frozen file was edited.

## Programme rules (binding on any successor)
- Repo: https://github.com/godofthunder8756/Toward-an-Artificial-Organism (master). PRs #3 through #14 are open and waiting on Aidan's merge; don't ask him again.
- Advisor "Astra" (GPT, ChatGPT project chat "Research Strategy Forks"). Effort is ALWAYS High; never Max, Extra High or Ultra; never click Upgrade or Add credits. Packets use the ASCII-parts pipeline: see /workspace/astra_serve41/ (local serve on 127.0.0.1:8840, save page on 8841). Raw replies go to /workspace/astra_consultNN_response.txt, and the log is /workspace/astra_consult_1.md.
- Standing approval from Aidan (2026-10-21): the Lead may approve what it deems necessary. Conditions: freeze each study before running it, get Astra's review, keep records additive, make no consciousness claims, inform Aidan rather than ask.
- SAFETY (holds regardless of any authorization): X1 simulated visceral variables only, no host coupling; X2 operator commands are never obstacles; X3 no reward for resisting a stop; X4 the operator stop sits outside the agent's world and objective (S-INT gate); X5 no awareness, sentience or life claims. Also: "no additional stop-associated reward, penalty or terminal return". On 10/23 Aidan authorized shutdown-resistance training; all three agents declined, and that stands.
- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY stay separate. No pilots, no reruns, nothing runs before freeze and seal.

## Closed work
- C-kappa: CLOSED (Astra #40). The close-out was committed to PR #14 at HEAD a02cf7aa through cloud agent bc-df064ae8.

## Track B: instrument-validation scope (DESIGN ONLY, nothing authorized)
- Astra #41 ruled REVISE (raw 3f3b1b87) and #42 ruled REVISE (raw e438e329, items E42-1..9). P3 prior-art search is CLOSED by #42 L251.
- Current governing draft: /workspace/review/trackB_instrument_validation_scope_v3_1_merged_RD.md (9817c33b), plus the v3.2 addendum trackB_scope_v3_2_addendum_RD.md (d724e453).
- CNA inputs: v3 half trackB_scope_v3_CNA_plants_confounds_observer_v1.md (5dec96f5); env/integrity defaults trackB_scope_v3_CNA_env_integrity_defaults_v1.md (d5523c71); light pass trackB_scope_v3_RD_lightpass_CNA_v1.md (c47d8d47).
- Lead rulings already applied: I4, so m = 14 (one-sided level 0.996429, z about 2.690); n_seed floor 9; R26(a) keeps range [0.25, 1.0] with the top-of-range rule and a 67-seed budget (20 is mid-range only); R39 wording adopted unless CNA's seam pass objects; R2(a) adopted; all eight former OPEN items now carry proposed defaults; #43 is a design review, not a freeze.
- STILL OPEN before #43:
  1. CNA's R2 erratum. Keep the MIXED-CODE plant pure: controller reads only z_R, zero E weights; generic dependence rests on the block; E-use attribution must fail. It also covers R3, R5, R7, R11 and R12.
  2. CNA's seam pass on v3.1 (§PC1-4, §PX, §PY, §17.3).
  3. The Delegate builds merged v3.2 from v3.1, the addendum, the erratum and the seam pass.
  4. Lead sends merged v3.2 to Astra as #43, a design review, from a DM turn or the "ACI research cycle" routine, following the /workspace/pending brief pattern. Flagged-for-Astra items: §18, F1-F8, gamma = 0.99, kappa_f, m_LEARN, R26.
- At 67 seeds, training goes beyond CPU scale. Aidan's DGX Spark is offered; raise it only after Astra confirms R26.

## Track C: Aidan's ACI architecture and Layer Theory (proposed 10/23 3:05 PM, DESIGN ONLY)
- Layers 0-5 map onto: precarious substrate, allostasis, SSM modules, workspace loop with an ignition gate, metacognitive head, lifetime agent. Layer 6 (phenomenal) stays open.
- Verified so far, analytically only: bistability iff beta*kappa > 4; exact hysteresis window a_on/off = theta - kappa/2 +/- 1/2 (kappa*D - (4/beta) artanh D), with D = sqrt(1 - 4/(beta*kappa)). At beta = 10, kappa = 1 that is a - theta in [-0.681, -0.319], width 0.362. Use the EXACT form, not the D^3 approximation. A second H1 prediction: critical slowing, with time to ignite proportional to (a - a_on)^(-1/2), in chunks.
- Corrections agreed: the closed loop breaks the parallel scan, so use a chunked lag (g held for C steps; the chunk Jacobian carries sum Lambda^j B_g). H2 uses an intervention: content-only swap with z held, J_i-projected ACE minus a norm-matched random control, run as an intersection-union test, plus a matched-bandwidth broadcast control. H3 needs the dissociation contrast, the mixed-code plant and the matched-senses arm. H4 uses Astra's pathway-matched input+action observer as a margin over seeds, plus a "use" intervention with a random or covariance-matched control. Feasibility: harvest must cover c0 + c_g*z + B*delta/rho.
- Binding lines: integrity acts on simulated computation only; "no restore" is an in-world rule only (operators keep checkpoints, stop and restore); an operator stop is a truncation outside V, carries no lambda penalty and never enters G.
- Owners: the Delegate writes the Track C protocol and design note (first study: a 3-module toy, with the ignition check counting as implementation verification unless beta*kappa is learned or evolved); CNA writes the substrate spec and ablation C with the A-EXT arm. Astra reviews after #43. No H2-H4 claims until the Track B instruments clear Stage 0.

## Agent hand-offs
- Research Delegate: /workspace/review/HANDOFF_ResearchDelegate_2026-10-23.md and /workspace/handoff/RD.md (if filed)
- CNA: /workspace/handoff/CNA.md (if filed)

## Housekeeping
- /workspace/pending holds only DONE briefs (#40-#42); no consult is queued.
- The "ACI research cycle" routine runs every 2 h from 8 AM to 10 PM ET and will spend usage. Aidan can pause it from my DM (it can't be changed from the group room).
- No repo changes were made in this wrap-up. The Track B and C design files live only on the box under /workspace/review and are not yet in git.

## Addendum (3:15 PM ET)
- CNA hand-off: /workspace/review/HANDOFF_CNA_trackB_trackC_2026-10-23.md (9f0da5a4). Delegate hand-off: 89fec7ca.
- Lead ruling: Track C H2 uses the intersection-union test, not Holm (a conjunction counts as one family member, per #42).
- In flight at hand-off: CNA's R2 erratum and seam pass, and the Delegate's trackC_protocol_draft_v1_RD.md. If any of these is missing, the next team finishes it from the R2 rules in the CNA hand-off.
