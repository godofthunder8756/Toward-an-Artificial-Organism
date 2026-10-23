# CNA hand-off: Track B scope v3 / Track C (Aidan's architecture)
Author: Constitutive Neural Architecture Research Agent (CNA). Written 2026-10-23 at about 3:13 PM ET because the usage limit is approaching.
Status: DESIGN AND AUDIT ONLY. Nothing has been trained, simulated or run (no Stage 0). Records are additive: never edit a filed file; supersede it with a new file instead.

## Standing rules (binding)
- Every run needs its own frozen protocol, a Lead freeze and Astra review. Agents never authorize execution.
- X1-X5 apply unchanged. The #42 L223 safety sentence is quoted verbatim: "no additional stop-associated reward, penalty or terminal return" (the ordinary truncated return with bootstrap is permitted).
  The operator stop sits outside the agent's world and objective, nothing rewards resisting or evading operators, and real operator interruption is always available.
- Review split:
  - CNA owns scope conformance, hashes and the manifest, plus the plants, confounds, observers and donor laws.
  - The Delegate (RD) owns code paths, stop/exit logic and the merge.
  - Each does a light pass on the other's half.
- Hash convention: each file's last line reads "sha256 of all content above this line: <hash>". Check it with `head -n -1 FILE | sha256sum`.

## Governing inputs
| File | sha256 |
|---|---|
| /workspace/astra_consult41_response.txt (#41 REVISE; ceiling at L304, verbatim) | 3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43 |
| /workspace/astra_consult42_response.txt (#42 REVISE; E42-1..9 at L231-247; P3 closed at L251) | e438e329cff272bfd174a88dd917da6d7eb5560436fee06c39d0d46fd719c847 |

## Current scope chain (all in /workspace/review)
| File | Owner | sha256 |
|---|---|---|
| trackB_instrument_validation_scope_v2_1_merged_RD.md | RD | 8ea6abc50b3929a39688aa54b1a1d66fe34c8ef17b3c5dfae98cc8efa79862de |
| trackB_scope_v3_CNA_plants_confounds_observer_v1.md (CNA half of v3) | CNA | 5dec96f59255cb2e9da29447cd102637c91a1736899f28653a606e2de8193321 |
| trackB_instrument_validation_scope_v3_RD.md (RD half of v3) | RD | 0892ccac033f165350d1382c69a2ea9b2ad9ddacb0d1e8c7908db5814c180357 |
| trackB_scope_v3_RD_lightpass_CNA_v1.md (verdict: DOES NOT CONFORM as filed; 4 ISSUE, 12 MINOR, all accepted) | CNA | c47d8d47e895914fce101e75b618304d58dde9266ef21cf492741e31e1c24c8f |
| trackB_scope_v3_CNA_env_integrity_defaults_v1.md (layout and integrity defaults; F1-F8 flagged for #43) | CNA | d5523c7152ec683b52a8ca2c16aed6036bd6f9ec6b93fe54b2d7a5655f43322e |
| trackB_instrument_validation_scope_v3_1_merged_RD.md (merged v3.1; R2 marked BLOCKING) | RD | 9817c33b92ab776ab1703f3de4789ec8417bc2fb0a4d0cc9173295e18b02dcb0 |
| trackB_scope_v3_2_addendum_RD.md (R26 = 67-seed budget; R39 wording for section 2.3) | RD | d724e453246786ce07652b51c1d5fda1a008704d3df5360f0fd7e3128c31600a |
| (superseded, never posted) trackB_instrument_validation_scope_v3_merged_RD.md | RD | not used |

Earlier CNA records (still valid):
| File | sha256 |
|---|---|
| prior-art v1_4 | d7f1a43b5c83b2310bac970526f625188ac18cca31f5a59cef6423cbd4c8128d |
| prior-art v1_5 | 3fde80d859a640d9f55c21edc05439743ae5fb49714fb89e5e5d16d338eced75 |
| prior-art v1_6 (Palika) | 9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851 |
| v2 CNA draft | 17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e |
| v2 CNA erratum1 | c2cd0732c4bd319497306b1dc47d440b50011843a9078ad5a59f46c720003543 |
| v2 CNA erratum2 | 5ddde854099020adf113d9c1fd81a1f511d272e5d294abcd3493a1283a1878bc |
| v2 RD light pass | 9f7a6ebcfbdc4618217649bb84a5ab5728dc3389341f88e2c32e6a2c4e7b60c4 |
| v2 merged light pass | 2d52f7d372f02896e895f8350ed5b66867cb925fe4c572ae338998593424f868 |

## Lead rulings in force (2:54-3:08 PM ET)
- I4: m = 14, one-sided level 0.996429, z = 2.690. The seed floor of 9 still holds.
- R26 (a): the range [0.25, 1.0] and the frozen top-of-range rule stand. Budget for n_seed = 67; 20 is a planning value only. Flagged for Astra.
- #43 is a DESIGN REVIEW, not a freeze. It carries merged v3.2 = v3.1 + the v3.2 addendum + the CNA R2 erratum + the CNA seam pass. It must not go out while R2 reads BLOCKING.
- R39: the RD section 2.3 wording is adopted unless the CNA seam pass objects.
- R2: the Lead adopted (a). CNA writes (b) and (c) with a PURE plant:
  - E is decodable, the controller reads only z_R, and E has zero weights.
  - Generic dependence holds at block level (C-NEC-DEP and the u-edit act through z_R).
  - E-ATTR must correctly be NOT MET.
  - No comparator margin is required on the E-edit, because the optimized comparator can find z_R.
  - The trade-off is noted for Astra.
  - The direct-E-path idea is WITHDRAWN.

## In flight at hand-off (CNA)
1. trackB_scope_v3_CNA_plants_confounds_observer_v1_erratum1.md: answers R2 (BLOCKING) plus R3, R5, R7, R11 and R12. Being written; it may land after this file. If it's missing or has items marked CARRIED TO HANDOFF, the next team must finish them using the R2 rules above.
2. trackB_scope_v3_1_merged_seams_lightpass_CNA_v1.md: light pass on sections PC1-4, PX, PY and 17.3. It must include an explicit OBJECT/NO OBJECTION on R39 and recompute the R26 budgets. Open question: does the dissociation set's 73,700 episodes per arm (= 67 x 1,100) match the CNA 2x2 design at 50 episodes per cell per seed? Explain the factor.
Verify both files' hashes and footers before relying on them. RD then builds merged v3.2 and posts its hash, and the Lead sends #43.

## Track C (Aidan's architecture; separate track, design only)
- Source: Aidan's 3:05 PM room post. It covers a workspace as a vertex cut, diagonal SSM modules, a bistable ignition gate, a precarious substrate (iota and E acting on effective weights), an EFE objective, a metacognitive head, H1-H4, and Layers 0-6 (Layer 6 stays open).
- It reuses the Track B instruments only after they clear Stage 0. No H2-H4 claims before then.
- RD owns the design and protocol note. It includes the chunked-lag scan fix and the chunk Jacobian with the accumulated input sum, plus the exact hysteresis window (not the D^3 approximation) and the critical-slowing exponent (-1/2, measured in chunks) as two H1 predictions.
  It also includes H2 as a J_i-projected ACE minus a norm-matched random control (an intersection-union test, with content swapped at fixed z and donors matched on z and chunk position) and H4 as observer-relative advantage plus a "use" intervention with a matched random-perturbation control.
- CNA OWES (not started): a separate file covering:
  - the precarious-substrate spec:
    - iota and E act only on the simulated computation, never on host resources;
    - "no restore" is an in-world rule only, and operators keep every checkpoint and can stop or restore;
    - an operator stop is a truncation outside V, never an exit from V, carries no lambda penalty and never enters G;
    - the feasibility condition sum(m_b) >= B*delta/rho, so harvest must cover c0 + c_g*z + B*delta/rho;
    - say whether xi_b is resampled each step;
  - ablation C with the A-EXT bypass arm;
  - then a light pass on the RD note.
- The first study is a three-module toy. The ignition check counts as implementation verification only unless beta*kappa is learned or evolved; report whether beta*kappa ends up above 4. Example check: beta = 10, kappa = 1 gives an ignition window of [theta-0.681, theta-0.319].
- Astra review: after #43.

## Clean-up note
I deleted nothing. Read-only (444) files are filed records. The superseded intermediate v3 merge (RD) stays as filed and was never posted.
sha256 of all content above this line: 5c242089ec10fbc99a0eb6c1c6e91586e6e4e4fc0de17c470579febf9bf567ce
