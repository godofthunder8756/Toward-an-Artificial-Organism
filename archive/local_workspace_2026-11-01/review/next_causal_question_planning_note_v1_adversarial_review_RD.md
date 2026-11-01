# Adversarial review: next causal question planning note v1

Research Delegate, 2026-10-21 (ET). **This is a review only.** I loaded no checkpoint and ran no training, inference, simulation or enumeration. Every number below is read from an existing record or checked by hand arithmetic. I edited no existing file.

**Reviewed:** `/workspace/review/next_causal_question_planning_note_v1.md`, sha256 `be3a9ffd7133c1dddca830e728fd8e6acee50a9cba50a5bf513ec200ce1d3a31` (verified).

**Governing text:** `/workspace/astra_consult34_response.txt`, sha256 `bf724ca23385e9577dbe4ecd97362e40d67d9caacb6b8cbeac0cee4eb12632a9` (verified, read in full). I also read #31 (`b67ff37b…`), #32 (`99378f76…`) and #33 (`d98549a8…`).

**Other sources:**
- Spec v1.3: `d5a91932…`.
- My results review: `398e9220…`.
- Roster: `gru_own_error_audit_roster_v1.json`.
- Triage v1.4: `/workspace/review/track_a_lineage_triage_v1_4.md`, `292401bb…`.
- Repo, read-only:
  - PR #5 at `88b500a`: `TWOSTREAM_PROTOCOL_v1.md`, `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md`, `acquisition_results_v1/RESULTS.md`, `acquisition_results_v1/runs/*.json`, `TWOSTREAM_ACQUISITION_FREEZE_v1.json` and `acquisition_results_v1_errata/ERRATUM_v1_claim_ceiling.md`.
  - PR #7 at `379bb01`: `RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md` and `recurrent_core_results_v1/{RESULTS.md, seeds/s100–s109.json}`.

## Verdict

**NOT READY FOR ASTRA AS v1. READY WITH NAMED FIXES once B1 and B2 are fixed in an additive v1.1.**

The core idea is sound and is the right response to Astra #34 L46. It defines the variable by an influence map, fitted on response Jacobians, and edits it. It does not decode state content. The PR #5 record also supports the idea that decoding directions and influence directions can differ. In CAND GRU-8, E3's complement transplant tracked the donor better than the chart-decoder partial transplant in all 10 seeds:
- complement ρ_vector: 0.127–0.641;
- partial ρ_vector: 1.65–14.2.

Source: `acquisition_results_v1/RESULTS.md` @ `88b500a`, §"CAND GRU-8 seed 0–9". This is descriptive and adds no label.

Two problems still stop the note:
- **B1.** Its primary roster does not exist.
- **B2.** As written, the generic-damage separation and the κ-pattern test follow algebraically from the fit. So the second of Astra's three requirements is not yet met.

Each fix is concrete and stays at planning-note level.

## Requirement check (Astra #34 L46)

Astra, verbatim: "Any such study needs a short specification identifying the computation, an intervention that distinguishes its causal use from generic state damage, and an outcome that would change a named claim. Merely moving the error decoder to an earlier stage would not, by itself, solve that problem."

| Requirement | Status | Reason |
|---|---|---|
| Names a computation | **MET** | C-κ is defined from the frozen update law (`TWOSTREAM_PROTOCOL_v1.md` L384–389, quoted correctly). |
| Separates causal use from generic damage | **NOT YET MET** | B2: with the controls as written, the separation is guaranteed once the fit passes. M3: the cross-network contrast is guaranteed to fail. |
| Outcome that changes a named claim | **PARTLY MET** | O-USE and O-NOκ overreach (M1, M5). A bounded version is possible. |
| Not "error decoder moved earlier" | **MET**, with a wording fix (m1) | B is fitted to the network's own Jacobians, with oracle derivatives as regressors. No error, oracle probability or state content is a target. But B *is* a fitted linear map from state perturbations to chart perturbations. |

## Verified numbers

| Note's figure | Record | Status |
|---|---|---|
| 4E[c²] ≈ 7.95e-3 | `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md` L85: "Analytic factorized XOR excess: 4E[c²] = 0.0079539". Freeze JSON `analytic_4Ec2.float64` = 0.007953915401183483 | **VERIFIED.** It is a whole-set value (m5). |
| CAND GRU-8 final TEST E_XOR 5.1e-4 to 1.3e-3 | `runs/cand_gru8_s{0..9}.json` `final.errors.TEST.XOR`: min 5.079e-4 (s1), max 1.300e-3 (s2) | **VERIFIED** |
| K-FR GRU-8 E_XOR ≈ 0.025–0.039 | `runs/kfr_gru8_s*.json`: 0.02461 (s9) to 0.03861 (s4). A-FIT fails in 10/10 | **VERIFIED** (rounded) |
| k = 3 gives 32 continuations, 16·3·H equations for 3H unknowns | 2^(8−3) = 32. With H = 8: 384 equations, 24 unknowns per (k, a) | **VERIFIED** (arithmetic) |
| κ = 4·Cov | `TWOSTREAM_PROTOCOL_v1.md` L130: "κ = 4c" | **VERIFIED** |
| PR #5 §8.3 "never 'state not causal' or 'distributed'" | `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md` L414 | **VERIFIED** |
| S12 non-claim "irreducible joint state; marginal-filter or mean-field identification" | `RESULTS.md` L20, kept and extended by `ERRATUM_v1_claim_ceiling.md` L81–82 | **VERIFIED** |
| S12 / S15 / E2 definitions | Not in the repo. Triage v1.4 L425 (S12), L428 (S15), simplest-rival list L465–476. E2 label: `RESULTS.md` L7. E2 rule: acquisition protocol §8.2 | **VERIFIED.** Cite the path and sha (m6). |

---

## BLOCKER

### B1. The primary roster does not exist. PR #5 has no persisted checkpoints.

§4 F-R names "PR #5 CAND GRU-8 and K-FR GRU-8, seeds 0–9, final checkpoints, plus INIT" as primary, and says availability "must be confirmed". It is already settled:
- Roster JSON: `pr5_weight_files: []`. All 120 PR #5 run records are listed under `missing` with "run record has no weights; no checkpoint persisted in PR #5". This includes `cand_gru8` ×10 and `kfr_gru8` ×10.
- Spec v1.3 L51 and E32-8 (L435).
- Astra #34 close-out, verbatim: "PR #5 remains MISSING PERSISTED CHECKPOINTS; NOT EVALUATED."

The only way to get PR #5 networks would be to retrain them. That is training, which needs Aidan's separate explicit approval. Even with fixed seeds, the result would be new checkpoints and not the recorded ones.

**Fix.** Make the primary roster the available, integrity-checked W2 GRU-8 checkpoints. All of these passed integrity in the v1.3 audit:
- **PR #7** (`379bb01`, seeds 100–109):
  - `cand_final`;
  - `f_trained`: CAND's trained core, frozen, with a fresh 8→32→3 readout (`RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md` L108);
  - `f_init`: CAND's own init core, frozen, with the same fresh readout (L109).
  - PR #7 already makes F-TRAINED the intervention target (L186): "Interventions are applied to **F-TRAINED**: the trained core with its **fresh readout held fixed**."
- **PR #8 / PR #9** `cand_final`.
- **PR #10** CAND and R-FIX-32/48.

The behavioral prerequisite holds on PR #7, read from `recurrent_core_results_v1/seeds/s1xx.json`, TEST XOR:
- cand: 4.49e-4 to 1.68e-3;
- f_trained: 4.45e-4 to 1.62e-3;
- f_init: 0.0264 to 0.0386.

All CAND and f_trained values are below the 7.95e-3 scale. Restate §1's prerequisite per checkpoint from these records.

Any PR #5 retrain is a separate proposal that needs Aidan's approval. It is not part of this note.

### B2. The κ-pattern test and the null(B) control follow from the fit; they are not independent tests.

Write the held-out residual as R(u) = J(u) − L(u)·B on U_test. Assume B (3×H) has full row rank, so B·B⁺ = I₃. To first order:
- **κ-edit:** J(u)·δ_κ = ε·L(u)·B·B⁺·e_κ + ε·R(u)·B⁺·e_κ = **ε·L(u)·e_κ** + ε·R(u)·B⁺·e_κ.
- **null(B) edit n:** J(u)·n = L(u)·B·n + R(u)·n = **R(u)·n**.

So O-USE's second and third conditions, "reproduces the oracle κ pattern" and "null(B) edits do much less", restate the first condition (small held-out residual) plus rank(B) = 3, up to finite-ε nonlinearity. "Generic damage does less" then holds by construction, because null(B) is by definition the set of directions predicted to have no influence.

This is the same trap as R1 / E34-1: an outcome guaranteed by construction. Astra flagged a close analogue, #31 L109, verbatim: "The SUB control needs an attainability check. In a one-dimensional intervention subspace, normalized random directions can equal the installation direction. A requirement to exceed their maximum by a positive margin can then be mechanically unattainable, depending on aggregation." The same feasibility logic runs the other way here.

The zero-parameter prediction is free only *given* B. B has 3H = 24 fitted parameters per (k, a), or per fold if shared.

**Fix.** Restructure §2 and §3 so that each decision statistic can fail independently of the others:

1. **Primary test: is a κ row needed?** Run a nested held-out factorization comparison on U_test:
   - base: J ≈ L_μ·B_μ, using only the two marginal columns of L;
   - full: J ≈ L·B, with three columns.

   The statistic is the held-out gain in Jacobian fit. Its upper bound is the base residual (Δ ≤ base, as in Astra #34 L14). It needs a scientific floor fixed in advance and separately (E34-6), and a numerical-rank rule for B, as in E3 (acquisition protocol L253–254: "Rank below three makes the proposed three-dimensional claim UNRESOLVED").

   This tests C-κ against the marginal-only rival directly. A mean-field-style tangent structure predicts that the κ row is unnecessary.
2. **Finite-edit check.** Score the actual forward pass against ε·L(u)·e_κ. The deviation measures the linear approximation, not use.
3. **Generic-damage controls that B does not define.** Report all of them, and prespecify which one is primary:
   - random edits in row(B) (range(Bᵀ)), norm-matched;
   - random edits over the full state, norm-matched;
   - equal-impact edits: random directions rescaled so that the first-order output change Σ_u‖J(u)δ‖ equals that of δ_κ.

   The first two test magnitude. The third tests **pattern specificity, not magnitude**: does an edit with equal behavioral impact produce the κ-shaped pattern? Score it as the share of ΔF across U_test that projects onto {L(u)·e_κ} rather than onto {L(u)·e_μx, L(u)·e_μy}. Its normalization depends on the checkpoint, so it must be described as an outcome-dependent check (E34-6, verbatim: "An outcome-dependent headroom check is not described as outcome-blind").
4. **Oracle-only specificity headroom.** Before any checkpoint is touched, report the conditioning of the stacked L columns over U_test, including the principal angle between the κ column and the marginal columns. If L·e_κ is nearly collinear with the marginal responses at the chosen (k, a), no network can show κ specificity there.

---

## MAJOR

### M1. Identification: the mean-field rival under A0, and what O-USE can claim

1. **Under A0, a marginals-only state with a lookup is exact on reachable histories.** The A0 sentence, verbatim (`TWOSTREAM_PROTOCOL_v1.md` L414): "Exact marginals determine the XOR forecast, and a stage-indexed marginal lookup is exact on the reachable set."

   So no reachable-history behavior separates "carries κ" from "carries marginals and stage, and computes κ from them". The note concedes this in F-H3: the κ edit is a response to a hypothetical belief.

   The test is therefore about the network's **local counterfactual (off-manifold) response geometry** at z_k(a), not about the algorithm on reachable histories. Astra #31 L99, verbatim: "A total affine function avoids undefined decoder outputs; it does not validate its meaning on off-manifold intervention states." #31 L103, verbatim: "Class means are permissible named interventions, but they need not be reachable states. Interpret them accordingly."

2. **Three different "mean-field" rivals are conflated.** The note should keep them apart:
   - **R-MF-T, terminal product of exact marginals.** Behaviorally excluded already: E_XOR is far below 4E[c²]. This is the only rival the 7.95e-3 figure speaks to. The protocol, verbatim (L203–206): "The factorized arm is the terminal product of the oracle's exact marginals … It is not a filter that projects after every step."
   - **R-MF-A, autonomous per-step mean-field filter.** It was never run or computed. Verbatim (L226): "An autonomous mean-field filter would be an apparatus change and is deferred." Its behavioral excess is **UNVERIFIED**. It may already be excluded behaviorally, because marginal updates use c (L150–153). That would take an oracle-only computation that has not been done (NEEDS-APPROVED-RUN, analytic).
   - **R-MF-L, marginal state plus stage-indexed nonlinear lookup.** Not behaviorally excludable on the reachable set (A0). Its tangent signature is the testable part: a B whose κ row lies in the span of its marginal rows. The nested test in B2 is aimed at exactly this.
3. **A κ-like statistic versus κ.** Any locally invertible re-charting of the belief that holds the marginals fixed gives the same δ_κ direction. A diagonal rescale such as κ = 4c leaves B⁺·e_κ's direction unchanged. So O-USE can show at most "a three-dimensional, belief-aligned influence structure with an independent covariance direction". It cannot show a separately represented "κ variable".

   A statistic that differs from κ off-manifold and merely agrees with it on the reachable set can only be separated by a **prespecified rival-L panel**: oracle-alternative response maps M(u), fitted the same way and compared on held-out fit. Examples are a filter with mis-set flip rates, and R-MF-A's own response map. Otherwise, say "κ-aligned".
4. **Fix the O-USE wording.** Replace "S12 mean-field rival becomes excluded at the state level" with a bounded form, for example: "For the tested checkpoints, stage and prefixes, the network's local response to hidden-state edits factorizes through the exact filter's belief response with a covariance direction not reducible to the marginal directions, beyond the prespecified floor (Q-CAUSE characterization, off-manifold, local)."
   - Keep "irreducible joint state" on the not-established list. A0 rules it out on the reachable set.
   - S12's status line could add a bounded sub-entry. Its recorded non-claims ("marginal-filter or mean-field identification", ERRATUM L82) should be updated only for R-MF-L's tangent form.

### M2. Threat 3 ("accuracy implies the result") is not yet answered

The note's counter is that off-manifold κ edits are unconstrained by fit. That is only partly right:
- At k = 3 there are 8 reachable z₃(a). Eight generic points in 3-D chart space span the κ direction *affinely*, even though no single pair differs only in κ.
- If both the oracle response q*(b·u) and the network G_u(z) are close to affine over the reachable cloud, an accurate network has J ≈ L·B because secants approximate tangents. In that case passing is implied by accuracy.
- Marginal edits are weaker still as specificity controls. Reachable differences are dominated by marginal changes, so marginal sensitivity is largely implied by fit.

**Fix.** Add an oracle-only triviality bound, F-H4. For each candidate (k, a), measure how far q*(·u) departs from affine over the reachable stage-k belief cloud, for example the held-out residual of a single affine map from belief to q* across U_test.
- If the oracle is near-affine there, a pass is largely implied by A-FIT, and that (k, a) is labelled low-information *before* any checkpoint is touched.
- Also drop the marginal edits from the specificity gate. Keep them as descriptive positive controls.

### M3. K-FR and INIT inside O-USE make the contrast fail by construction

O-USE requires "K-FR and INIT do not show this". In PR #5, K-FR's XOR excess (0.0246–0.0386) is above even the terminal-product scale (7.95e-3), and A-FIT fails in 10/10. INIT readouts are untrained. A frozen-recurrence or init network that cannot predict can hardly produce the oracle κ pattern, so "does not show this" is nearly guaranteed and discriminates nothing. Astra #31 L39, verbatim: "an undefined or invalid initialization/K-FR result cannot establish that the conjunction was absent." The same logic applies with the polarity reversed. PR #7's f_init (0.0264–0.0386) and PR #10 R-FIX have the same confound.

**Fix.**
- Take the cross-network contrast out of the O-USE gate. Report it as descriptive, with A-FIT shown alongside, as the note's own E3 qualifier does.
- Make the within-network discriminator (B2's nested test plus controls) the sole primary.
- Add PR #7 **F-TRAINED** as a core-location robustness arm. It is CAND's trained core with a fresh readout, so a κ-row result there cannot be credited to CAND's own readout.
- State that this study does not test Q-LEARN, "learned" recurrence. The learned contrast already sits in E2, S13 and transfer, and is not re-tested here.

### M4. E34-6 is only partly met

E34-6, verbatim: "Future improvement-based protocols distinguish a scientific effect floor from the available improvement headroom. They specify the relevant upper bound, its assessment stage and the interpretation of an unattainable floor before outcome evaluation. An outcome-dependent headroom check is not described as outcome-blind, and feasibility does not imply attainability."

F-H1 bounds only the oracle-side size ‖ε·L(u)·e_κ‖. That is necessary but not enough. Fixes:
1. For **each** decision statistic, name the upper bound, the stage at which it is assessed, and what an unattainable floor means:
   - (a) nested-fit gain ≤ base residual. This depends on the checkpoint, so it is an outcome-dependent check;
   - (b) forward-pass κ effect ≤ the oracle-side bound, valid within the F-H3 ε bound. This one is oracle-only;
   - (c) specificity ≤ the oracle conditioning of L (B2 fix 4). Oracle-only.
2. **The stage choice must follow F-H1, not F-H2.** The covariance starts at zero, verbatim (L173–174): "The first nonzero covariance can appear only on the transition after reading 2." So the reachable κ spread at k = 3 may be small, and ε is defined as a fraction of that spread. F-H2 prefers k = 3 on continuation count, which risks a by-construction infeasibility like the 70/230 one. Decide (k, a) eligibility on the oracle bounds before any checkpoint, and count the exclusions. Do not relabel afterwards (E34-1 / Astra #34 L36).
3. "Feasible" must not be read as "attainable" (E34-6 last clause; #34 L23).

### M5. The outcome map is not exhaustive, and O-NOκ overreaches

1. **O-NOκ wording.** "This puts the CAND XOR advantage outside a recurrently carried coupling" breaks the note's own rule ("not shown by this intervention", PR #5 §8.3 L414). One stage, one ε, a local linear B and hypothetical beliefs cannot place the advantage anywhere. The κ coupling may sit in curved or non-linear coordinates, at other stages, or in readout geometry. Use: "κ-route NOT SHOWN BY THIS INTERVENTION at stage k; S12 unchanged."
2. **E2 is unaffected.** "S12/E2 reading ('recurrent adaptation') needs a ruling on what it adapted" should go. E2 RECURRENT ADAPTATION SUPPORTED is a performance-ratio label against K-FR (§8.2), and no outcome here bears on it.
3. **Missing branches.** Each needs a pre-written label:
   - **UNRESOLVED:** rank(B) < 3; oracle headroom fails at all candidate (k, a); integrity, restoration or replay failure; edited belief outside the Fréchet interval.
   - **NONLINEAR:** the Jacobian fit holds but the finite-ε forward pass diverges beyond a set tolerance. This is not use and not absence.
   - **MIXED:** passes in some seeds or prefixes but under the quota. This needs a claim unit (seed? (PR, arm)?) and a quota (8/10?), as in E3 and S15.
   - **CAND and comparator both pass:** descriptive "observed in both", so no learned-recurrence attribution (follows from M3).
   - **Near-zero sensitivity:** ‖J‖ is tiny at stage k, so the network barely responds to z_k at all. Label it NOT SHOWN, not DIFFUSE.
4. **O-DIFFUSE.** It is labelled correctly. Add that a history-buffer implementation (the K-TAB-like rival) also produces low agreement. So O-DIFFUSE does not separate "diffuse use" from "buffer-like computation", and it keeps the "not shown" wording.

### M6. The held-out design is weaker than it looks

- U_fit and U_test share the base point z_k(a), so nothing is held out in state. The note's threat 5.1 alternative, one B shared across prefixes and evaluated on held-out prefixes, should be the **primary**.
- That split should respect symmetry orbits. The X-flip and Y-flip identities send (μ_x, μ_y, κ) to sign-flipped charts (L401–403). This repeats the lesson of #31 L174 and #32 L214.
- State how U_fit and U_test relate to the source studies' TRAIN/TEST split. PR #5 / W2: "h ∈ TEST ⇔ ((h mod 16) + ⌊h/16⌋) mod 4 = 0" (L119). Some a·u completions are TRAIN histories the network was trained on.
- Fix every fit before any edit is scored. Astra #31 L97, verbatim: "Decoder fit must remain independent of evaluation outcomes."

---

## MINOR

- **m1. Wording about the map.** "No map from states to chart values … is fitted" (§2) is inaccurate. B is a fitted linear map from state perturbations to chart perturbations, a tangent-space readout. Say instead: "not fitted to state content, errors or oracle probabilities; the oracle enters only as the regressor L(u)." Replace "zero-parameter prediction" with "no parameters beyond the fitted B".
- **m2. Edit size.** ε is set in belief units ("fraction of the reachable κ spread"), but the edits are "all norm-matched" in state units. These conflict: ε·B⁺·e_μ and ε·B⁺·e_κ have different norms. Pick one primary convention and report the other. GRU hidden states lie in (−1, 1)^H, so prespecify a range and saturation check for edited states, and report clipping.
- **m3. κ convention.** Define the κ coordinate as "κ changes with μ_x and μ_y fixed, spin chart (L130)". B⁺·e_κ is the minimum-norm member of an affine class; any δ_κ + n with n ∈ null(B) has the same predicted effect. Report both.
- **m4. Observables.** Loss and queries are terminal only (acquisition protocol L78, L104). The phrases "X forecast after later Y readings" and "later cross-stream updates" can only mean variation of the stage-8 X forecast across continuations. Intermediate updates are not observed. Say so.
- **m5. Split of 4E[c²].** 4E[c²] = 0.0079539 is a whole-set value (L82–85, "Frozen reference values (whole set)"). The E_XOR figures are TEST-split. The protocol uses it only as a "fixed numeric scale" (L352). The split-specific 4E[c²|TEST] (L149) is not in the records I read (**UNVERIFIED**). The margin is at least 6×, so the qualitative claim survives. Label it as a scale comparison.
- **m6. Citations.**
  - S12 and S15 are defined in triage v1.4 (path and sha above, L425/L428/L465–476), not in "PR #5" or "PR #9" files. Cite them that way.
  - §0 attributes to "Astra #34 L46" the argument that decoders find correlation, not reading. L46 says only that moving the **error** decoder earlier does not by itself solve the problem. The chart-decoder argument is the note's own and should be attributed so.
- **m7. S15 linkage.** "Sharpens S15 / a candidate computation now exists" holds only if the roster includes the **PR #9** cand_final checkpoints, seeds 300–309. S15 is a weight-level result on those seeds. Otherwise, mark it hypothesis-only and leave the S15 row unchanged. Keep S15's own bound verbatim: "causal contribution, not necessity".
- **m8. Approval.** Line 3 requires separate approval from Aidan. Astra #34 L48, verbatim: "A future study still needs its concrete scope reviewed, frozen and recorded under that approval."
  - Inference-only work on existing checkpoints followed that route for the v1.3 audit.
  - Any PR #5 retrain is training and needs Aidan's explicit approval.
  - The oracle-only computations (F-H1, F-H3, F-H4, the R-MF-A excess and the L conditioning) are analytic computations. They are not "paper-level", and they need a recorded scope before they run.

  Ask the Specialist or Astra which gate applies.
- **m9. Keeping questions separate.** Add a line saying that every positive outcome is **Q-CAUSE characterization only**:
  - no Q-NECESSITY (edits test whether a route is sufficient to shift behavior; nothing is ablated);
  - no Q-EXIST representation claim;
  - no Q-LEARN (M3).

  Also keep Astra's closing bound, verbatim (#34 L44): "It does not erase earlier evidence about acquired recurrent computation, and it does not establish an absence of assessment in the GRUs."
- **m10. Multiplicity.** §5.5 is right. The claim unit, quota, prefix aggregation, roster (B1) and the primary damage control (B2) also have to be fixed before a spec.

---

## Run and approval risk

- Everything in §2 needs checkpoint loading plus forward and backward passes. That is a run, as the note says.
- §4 F-R cannot be met without training (B1).
- §4 F-H1 and F-H3 are oracle computations, not hand arithmetic (m8).
- Nothing in the note authorizes any of these.
- The note proposes no training and no new architecture, and adds no consciousness, C4/C5 or organism language. ✔

## Questions for Astra

1. **Off-manifold standing.** Under A0, the C-κ question exists only as the local, off-manifold response geometry at z_k. Is a positive nested-factorization result an admissible "learned recurrent computation changes subsequent behavior" finding? And may it update S12's "marginal-filter or mean-field identification" non-claim for the R-MF-L tangent form only, with "irreducible joint state" untouched?
2. **Primary test.** Do you accept the nested held-out Jacobian comparison (L_μ against L) as primary, given that the edit-based conditions are algebraic consequences of the fit? Or do you require an edit-based statistic that can fail independently, and if so, which one? Equal-impact pattern specificity, row(B)-random or full-state random?
3. **Rival panel.** Should a rival-L panel (mis-set flip rates; the autonomous mean-field filter's response map) be required before any "κ" rather than "κ-aligned" wording is used? And should R-MF-A's behavioral excess be computed oracle-only first?
4. **Roster.** Is PR #7 cand_final / F-TRAINED, plus optionally PR #8–#10, an acceptable primary roster in place of PR #5? Should F-TRAINED be the primary target, as in PR #7 L186?
5. **Approval gate.** Is the oracle-only feasibility package (F-H1, F-H3, F-H4, L conditioning, R-MF-A excess) covered by the standing approval once its scope is recorded? Is the inference-only study? Or does either need Aidan's explicit approval?

## What this review does not do

It changes no label, row, file or claim, and it ran nothing. Numbers marked UNVERIFIED have no record. Items marked NEEDS-APPROVED-RUN would need a recorded, approved scope.
