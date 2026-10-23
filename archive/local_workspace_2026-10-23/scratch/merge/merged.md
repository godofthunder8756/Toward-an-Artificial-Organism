# Track B instrument-validation scope v2 — MERGED (RD v2 + CNA items 1, 3, AQ-A1..A4, AQ-SELF1)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** Nothing runs. No Stage-0 run, training, simulation, solver or checkpoint inspection is authorized. Astra #41, verbatim: "No Stage-0 run, training, simulation or checkpoint inspection is authorized by this review." **P3 stays OPEN and freeze-blocking pending Astra #42.**

- **What this file is.** A new, additive merge record. It edits no existing file. RD's v2 (`166370c1…`, treated as frozen) and CNA's half (`17832b01…`) both stay on disk unchanged. v1 and A1–A7 stay on disk unchanged.
- **How it is built.**
  - RD's v2 content appears in full below (from its §0 to its §10), with the merge edits listed in §13: (i) the four placeholder sections §P1, §P3, §PA, §PS are replaced by CNA's content, quoted verbatim, with only heading levels changed and "CNA §" prefixed to CNA's own section numbers, and with CNA erratum 1 (E1–E6) applied in place (each erratum insertion is tagged "[erratum 1 En]"); (ii) the inputs table gains rows; (iii) Palika material from CNA v1.6 and the Lead's rulings is added to §2.2; (iv) the §8 response table is replaced by a merged one; (v) the §10 CNA-file bullet is updated; (vi) light-pass items I1, M3, M4, M5, M6, M7, M11, M12 and erratum E3/E4 are applied in RD text, each tagged "[merge Rn]".
  - Inside quoted CNA blocks, "§n" means CNA's own section n (CNA §1 → merged §P1; CNA §2 → §P3; CNA §3 → §PA; CNA §4 → §PS; CNA §0, §0.1, §5, §6 → Appendix A), and "Ln" means line n of the raw #41 file.
  - Conflicts between the halves are in §12 (Merge reconciliations). Order of authority: Astra #41 raw text first, then the Lead's room rulings. Anything not decidable from those is marked **OPEN FOR CNA/LEAD**.
- **Written:** 2026-10-23, about 12:55 PM ET, by RD. Read-only on the repo and GitHub.
- **Lead rulings applied in this merge (room, 2026-10-23 ~12:36–12:43 PM ET):** use the raw L304 ceiling sentence verbatim; orthogonality counts as the **fifth** legitimately-satisfying control (CNA D-g); CNA's §20-1 and §20-2 are cited, not redrafted (they are CNA item 1 and item 3); Palika per §2.2; #42 packet note per §11; CNA's light pass on RD's half is a separate file, not awaited.

## M1. Inputs added for the merge (verified on the box, 2026-10-23 ~12:45–12:50 PM ET)

| Role | Path | sha256 | Footer check |
|---|---|---|---|
| RD scope v2 (frozen as of the Lead's line-276 fix) | `/workspace/review/trackB_instrument_validation_scope_v2_RD.md` | `166370c1435bdab6734aec869c94770fb8a88214066082b3a4e3996dbce13b40` | `111f163b0b1c743574c30ec6193c457fa64cb149aabec46ae659038271c7cf4b` reproduced |
| CNA v2 half (items 1, 3, AQ-A1..A4, AQ-SELF1) | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` | `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e` | `b666b1d76abe8e526cdc20a404c7cf047ac46823e121a2104636c9d165c68dd1` reproduced |
| CNA prior art v1.6 (Palika route check) | `/workspace/review/trackB_prior_art_verification_v1_6_palika_route_CNA.md` | `9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851` | `be61452b4d0cacd208dfae964e74b02ada69d63d1736f30661ab7f9147a0097b` reproduced (v1.6's last line is the bare hash) |

| CNA light pass on RD v2 | `/workspace/review/trackB_scope_v2_RD_lightpass_CNA_v1.md` | `9f7a6ebcfbdc4618217649bb84a5ab5728dc3389341f88e2c32e6a2c4e7b60c4` | `e7ac3a93a974a473ec0813c2392dfa2eda38a9bd14c4271353e9f82fce5d03a2` reproduced |
| CNA erratum 1 to its v2 half (E1–E6) | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md` | `c2cd0732c4bd319497306b1dc47d440b50011843a9078ad5a59f46c720003543` | `9b3417d21ded80189125b2227dbe8817b02f4016074e717bd1c7fe047b2d5cd9` reproduced |

All other inputs are in §1 below with full hashes; each was re-verified for this merge and is unchanged.

**Number provenance (merged; corrects RD v2's header claim per light-pass M11).** Every numeric value in this file is one of: (a) quoted from Astra #41 (marked "Astra #41 candidate"); (b) a v1 PROPOSED value carried as PENDING (bootstrap B = 10,000 and the 95% CI level, both from v1, not #41); (c) a CNA **PROPOSED DEFAULT** with its stated rationale (CNA sections, erratum 1); or (d) PENDING. Nothing is from data.

**Labels.** Confound rows: PASS / FAIL / CONFOUND NOT REALIZED only; CONFOUND NOT REALIZED → specificity UNRESOLVED, which blocks Stage 0. AVAILABLE and UNAVAILABLE are never confound-row labels; UNAVAILABLE appears only as an instrument-on-system label (eligibility gates, designated limitation tests; §12 R4).

---
---

## 0. Governing text and central question

- **Governing ruling:** `/workspace/astra_consult41_response.txt`, sha256 `3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43` (verified on the box, 2026-10-23 ~12:35 PM ET; matches the Lead's `3f3b1b87…`). Astra's raw text governs and is quoted verbatim below. Where it conflicts with v1+A1..A7 or earlier files, Astra governs; each such change is listed in §9.
- **Central question (Astra #40 verdict 5, verbatim, unchanged):** "Can the proposed instruments distinguish the specific internal-state relationships they claim to measure from reward-only, feedforward, initialization and intervention-damage confounds?"
- **Astra #41 verdict, verbatim:** "Verdict: REVISE." … "These are scientific design changes, so I choose REVISE rather than FREEZE WITH NAMED EDITS."
- **What Astra reviewed, verbatim:** "I reviewed the supplied scope, not the underlying files or hashes. I checked relevant accessible primary sources; the Asan-specific judgments below rely on your supplied account because I could not retrieve the cited Zenodo record."

## 1. Inputs (all hashed on the box, 2026-10-23 ~12:35–12:40 PM ET; none edited)

| Role | Path | sha256 |
|---|---|---|
| Astra #41 raw reply (GOVERNING) | `/workspace/astra_consult41_response.txt` | `3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43` |
| Consult summary incl. #41 key points (non-governing; file is appended over time, hash as of reading) | `/workspace/astra_consult_1.md` | `485e50b296e91ed42ca83255db7a221cd87cf804fcc67f2d7f26a04428722e31` |
| #41 packet body as sent (checked for what Astra saw) | `/workspace/astra_serve41/c41_body.md` | `c514ad5249b8475c83fa2a112f531c1687a447ca51bbff66cdb4fccb90ec37be` |
| Cover note v1.1 | `/workspace/review/trackB_astra41_cover_note_v1_1_RD.md` | `b7d1e4ab9dff0e4965e6293ae83558bbce7592bec5aca3c9182b5ad83ee93db2` |
| Merged scope v1 (base) | `/workspace/review/trackB_instrument_validation_scope_v1_RD.md` | `7b9bf34d7b4c10c8c2a7063aa6177d94e888fbbe76f78d0cd33afbe0c905c56a` |
| Amendment A1 | `/workspace/review/trackB_instrument_validation_scope_v1_A1_RD.md` | `8572152647a03524365675a24f254dc33ed4af67f091aee9762a23ff18bb9c99` |
| Amendment A2 | `/workspace/review/trackB_instrument_validation_scope_v1_A2_RD.md` | `7413fb94292eda1ebd0d4321794d7b018400e87d38abdfbcda7fcc18204745eb` |
| Amendment A3 | `/workspace/review/trackB_instrument_validation_scope_v1_A3_RD.md` | `34a298a628734180f5f6f354a1b08c8ef8a15ff2859d06cfd09d799448d1a9a4` |
| Amendment A4 | `/workspace/review/trackB_instrument_validation_scope_v1_A4_RD.md` | `585bb58acacaee64197c8233508643887f20a2bffa0d5a0c6da795c3cbd43dc6` |
| Amendment A5 | `/workspace/review/trackB_instrument_validation_scope_v1_A5_RD.md` | `0e26af91971c879378bf947fd01d6e1e452bcad62e02e7dcdd19ce88ed1c6a6f` |
| Amendment A6 | `/workspace/review/trackB_instrument_validation_scope_v1_A6_RD.md` | `679b616690b935506832b6f9056046e7ca238dba6e4801511c7f66c6f5eb4547` |
| Amendment A7 | `/workspace/review/trackB_instrument_validation_scope_v1_A7_RD.md` | `fa1d5c8fc6cc679e84f633c8ca2ec5f3bb9cc87bb9982f9b792f0fcfbcb50b06` |
| Measurement plan v1 | `/workspace/review/trackB_measurement_plan_v1_RD.md` | `1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef` |
| Measurement plan Addendum 1 | `/workspace/review/trackB_measurement_plan_v1_RD_addendum1.md` | `4ecef2628701e8a9817e8fd42a2bb0f4867fade8a72ec89a203315531e78f051` |
| CNA confound/sham matrix + X1–X5 | `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1.md` | `377f99bac3413b20bef65b289971bbe32ff9ebea15923f035878b014cc398fde` |
| CNA erratum 1 | `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1_erratum1.md` | `41c1a414e27239d5763736d35562b79e25c33d53f29d42198de39effb4debcc5` |
| CNA prior art v1 | `/workspace/review/trackB_prior_art_verification_v1_CNA.md` | `f2fd0ae6f5df571f6ed6ad413ff604ffcb975e565c91c991acf8c801c6104ac9` |
| CNA prior art v1.1 | `/workspace/review/trackB_prior_art_verification_v1_1_prefreeze_CNA.md` | `29068cce219530f459a4a045f349393a2aea9db1253a4c76a654514284017928` |
| CNA prior art v1.2 | `/workspace/review/trackB_prior_art_verification_v1_2_open_items_CNA.md` | `166469154faeccdb9688a4473504f1d160711949b4eb74779bd84ba9a9b7451c` |
| CNA prior art v1.3 | `/workspace/review/trackB_prior_art_verification_v1_3_fullreads_CNA.md` | `badf7258278fcecc11bea190f5397724ca0fdaf21348f915b1e2c34afe4cec8a` |
| CNA prior art v1.4 (P3, OpenAlex + Semantic Scholar) | `/workspace/review/trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md` | `d7f1a43b5c83b2310bac970526f625188ac18cca31f5a59cef6423cbd4c8128d` |
| CNA prior art v1.5 (P3 alternative routes; Palika abstract) | `/workspace/review/trackB_prior_art_verification_v1_5_P3_altroutes_CNA.md` | `3fde80d859a640d9f55c21edc05439743ae5fb49714fb89e5e5d16d338eced75` (internal footer `70460e8ae047a0beaead078fd9b5e3873f4a94fd95cc94f716de57a5dba17fd8` reproduced as `head -n -1 | sha256sum`) |
| CNA planning note v1 | `/workspace/review/trackB_workspace_allostasis_scope_note_v1.md` | `87a31cc88dc2fd0252d4cf932fabbfd8a1ce65bd3f77dce9eda5c6cfdafe2800` |
| CNA note v1.1 addendum | `/workspace/review/trackB_workspace_allostasis_scope_note_v1_1_addendum.md` | `5cf075b6e0a75cf7696307924d22abd9b9e961f852b86745f80bd2b46a09b53a` |
| CNA note Q4 correction | `/workspace/review/trackB_workspace_allostasis_scope_note_v1_2_Q4_correction_CNA.md` | `edb357ad250c294f6a1dc370f4cfc22f7ed9e1537ccab624e2e829ac1927cfe7` |
| CNA v2 companion (items 1, 3, AQ-A1..A4, AQ-SELF1) | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` | `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e` (footer `b666b1d7…` reproduced) [merge R27] |
| CNA erratum 1 to its v2 half | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md` | `c2cd0732c4bd319497306b1dc47d440b50011843a9078ad5a59f46c720003543` (footer `9b3417d2…` reproduced) [merge R27] |
| CNA prior art v1.6 (Palika route check) | `/workspace/review/trackB_prior_art_verification_v1_6_palika_route_CNA.md` | `9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851` (footer `be61452b…` reproduced) [merge R27] |
| CNA light pass on RD v2 | `/workspace/review/trackB_scope_v2_RD_lightpass_CNA_v1.md` | `9f7a6ebcfbdc4618217649bb84a5ab5728dc3389341f88e2c32e6a2c4e7b60c4` (footer `e7ac3a93…` reproduced) [merge R27] |
| RD scope v2 (frozen) | `/workspace/review/trackB_instrument_validation_scope_v2_RD.md` | `166370c1435bdab6734aec869c94770fb8a88214066082b3a4e3996dbce13b40` (footer `111f163b…` reproduced) [merge R27] |

**Packet-record note (checked in `c41_body.md`).** The packet Astra received listed prior-art v1.4 as "in progress … `ddd0287a` (file still being written)", not the final `d7f1a43b…`, and it contains **no AQ-SELF1 question** (a grep for "SELF1", "Ashuach" and "disagree" finds nothing). Astra therefore did not rule on AQ-SELF1 and did not see final v1.4, v1.5 or v1.6. See §PS, §8 and §11.

---

## 2. AQ-P1: justification by the measurement question (RD)

**Astra, verbatim:** "AQ-P1: Worth building only if the next version becomes a coherent instrument-validation study with explicit ground truth for each claim. The current scope is not ready to freeze, even after P3." … "Conditional yes; justify the study by the measurement question, not by counting surviving novelty differences."

**2.1 Justification adopted.** The study is justified by the measurement question Astra states, verbatim: "A useful contribution would establish when this battery distinguishes accessible information, behavioral use, dependence under intervention, and advantage from privileged information." The four are kept as four separate outcomes, mapped to the separate questions (never merged):

| Astra's distinction | Question / instrument |
|---|---|
| accessible information | Q-EXIST (and the accessibility half of SELF's observer comparison) |
| behavioral use | Q-CAUSE (and BCAST broad causal routing) |
| dependence under intervention | Q-NECESSITY intervention dependence (§3), reported separately from external substitutability |
| advantage from privileged information | SELF, with the privileged-signal mechanism check (§5b AQ-4) |

Q-LEARN (acquisition) stays a separate contrast on top of any of these (§5.6).

**[merge R21] Q-EXIST baseline (CNA erratum 1 E4, adopted).** Q-EXIST ΔR² is measured against the **strongest baseline = max(history-matched input/output/action baseline over W_B, declared proxy baseline: r̄, t, episode identity, position)**, same probe family and partitions (§P1 CNA §1.1). Q-LEARN inherits it (§5.6). IGN is a dynamical-signature instrument and is not one of Astra's four; its claim stays "conditional bimodality" (§5.2, §P1).

**2.2 Novelty labels unchanged; Palika added; consequences stated.** Labels from A6/A7 stay: Q-NECESSITY is an EXTENSION (D2 as frozen in A1-2); SELF NOVEL AS FAR AS FOUND; claim (3) PARTIAL OVERLAP. Per the Lead's ruling (2026-10-23 ~12:36 PM ET) on CNA v1.5 (`3fde80d8…`), **Palika et al. 2026 is the third Q-NECESSITY comparator** (abstract-level only; SSRN full text returned HTTP 403).

| Comparator | D1 interoceptive content | D2 learned RL agent (as frozen) | D3 viability outcome | D4 same-size module ablations + matched arms | What survives for us |
|---|---|---|---|---|---|
| Wilterson & Graziano 2021 | survives | does not survive | not listed as surviving (A6-2 lists D1, D4 only) | survives | D1, D4; plus stated difference: our model is learned rather than supplied |
| Asan 2026 | does not survive | does not survive | survives, with A6-2 caveat (masking measure unnamed) | survives | D3 (caveat), D4; plus stated difference: recurrent vs feedforward |
| Palika et al. 2026 (abstract only) | shared (does not survive) | shared (does not survive) | partial overlap only | **not evident from the abstract; unverified** | D3 only in part (fixed-horizon viability form, abstract-level). D4 is **not** listed as a surviving difference over Palika. |

- Label: **EXTENSION**, unchanged. The A3-1 drop rule already gives EXTENSION (not all four differences fail, since D3 is only a partial overlap), so confirming D4 against Palika's full text **does not block freeze** (Lead ruling). The Palika D4 question goes to Astra at #42 (§8).
- **"Learned rather than supplied" separates us from Wilterson & Graziano 2021 only.** Palika's interoceptive state is learned (CNA v1.5), so this is not a distinguishing feature in general.
- **[merge] Palika note — based on public code (github.com/CharithaPalika/FoodRL), not the paper** (CNA v1.6 §5 suggested wording, exactly as written): "not evident from the abstract; the authors' public code (FoodRL) shows no other-module matched-size ablation, only a within-bottleneck random-k-neurons comparison; the paper's full text is unverified." The D4 status itself stays **"not evident from the abstract; unverified"**, and D4 is **not** claimed as surviving against Palika (Lead ruling).
- **[merge] Observation from the code, NOT a new criterion added to D1–D4:** Palika's public code is a feedforward MLP running PPO; our agent is recurrent (CNA v1.6 §3.1, §4.1).
- **[merge] Correction record:** v1.6 corrects v1.5 §2.2's inference that Palika is "recurrent-relevant because the environment is partially observable". v1.5 is unedited.

Astra, verbatim: "The D1-D4 rule is a record of differences, not a sufficient scientific definition of an extension. One surviving difference may be important or cosmetic. State its consequence for the inference." Consequences (RD draft; for CNA light pass):
- **D1 (interoceptive content; survives only against W&G):** the tested estimate targets simulated body variables, so any Q-NECESSITY result is about dependence on that estimate, not on an attention or competence model. It does not license "self-model" (§2.3).
- **D3 (viability outcome):** dependence is measured on a fixed-horizon in-world viability score (§6), so a result speaks to the declared in-world function, not to reward or task accuracy.
- **D4 (same-size ablations of other modules plus sham; survives against W&G and Asan, unverified against Palika):** makes the result a *selective* impairment contrast rather than generic damage. Per the new ceiling (§7), selective impairment still does not establish endogenous necessity.
- **A-EXT (required):** adds an explicit substitution challenge (§3); its consequence is that "dependence" and "substitutability" are reported as two outcomes.
- **Recurrent vs feedforward (stated difference vs Asan, not a criterion):** consequence limited to the memory-access contrast (AQ-A2, §PA); Astra: it "validates a memory-access contrast, not a general distinction between models with and without self-models."

**2.3 Decodability is not a self-model (applies to our own module).** Astra, verbatim: "A decoded policy-layer pattern should count as a candidate internal representation under the same operational standard applied to your allostatic module. A separate module name is neither necessary nor sufficient for a self-model. Decodability alone does not establish predictive modeling or causal use in either system." Consequence: the allostatic module is a **candidate internal representation** of simulated E/I. Q-EXIST MET licenses only accessibility. The phrase "learned interoceptive self-model" in A1–A7 label text is retained only as the frozen label wording; proposed for the Lead: in v2-era result text, use "interoceptive estimate module (candidate internal representation)", adding "learned" only when the Q-LEARN "acquired" conditions of §5.6 hold (#41 L170) [merge R11, light-pass I1]; use of the phrase PENDING Lead ruling. No label changes.

**2.4 SELF retargeting needs its own justification.** Astra, verbatim: "SELF also changes the target from Binder's prediction of a model's own behavior to prediction of simulated body variables. That adaptation needs its own justification; it does not inherit an introspection interpretation." RD justification (draft): SELF measures **prediction advantage for simulated body variables over a matched external observer with declared access**; it is a privileged-information instrument, not an introspection instrument, and no introspection wording is used. Binder's design element retained is the comparator, verbatim: "Binder's experiment explicitly compares self-prediction against another model trained on the target model's behavior." Sufficiency of this justification is for Astra at #42 (§8). Observer-arm design changes (including the input-only observer arm) are CNA's (§PS).

**2.5 Prior-art record.** The Asan-specific judgments are UNVERIFIED by Astra (Zenodo not retrieved). Palika is abstract-level only (plus code-level evidence from v1.6, not the paper). P3 stays open until Astra rules at #42 (§10).

---

## §P1. Item 1: corrected claim-to-ground-truth table (MERGED — CNA §1)

*Quoted verbatim from CNA `trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md §1` (`17832b01…`), with erratum 1 (`c2cd0732…`) applied in place; only heading levels changed. Inside this block "§n" means CNA §n.*

### CNA §1. Item 1: corrected claim-to-ground-truth table (#41 §20-1, L264–272)

**Rule (L272):** "For each row, state the mechanism that is present, the mechanism that is absent, and the exact claim being challenged."

**The decision for each control Astra challenged.** Where a negative control can genuinely satisfy a claim, I either:
- **REDEFINE** the control so that it truly lacks the mechanism the claim names, or
- **NARROW** the claim so that the control no longer satisfies it. Where a control genuinely has the mechanism of the narrowed claim, it is **reclassified** as a mechanism-present known answer: expected MET, scored in layer (i) as a P-type row (scope v1 §7.2), not as a specificity row.

**Column key.**
- **Present:** the mechanism present in the system, i.e. what the construction builds.
- **Absent:** the mechanism absent, i.e. what the construction rules out by construction.
- **Claim challenged:** the exact claim the row tests, and the instrument outcome expected.

#### CNA §1.0 Summary of decisions

| # | Control / issue (#41 source) | Decision | Why |
|---|---|---|---|
| D-a | Learned FF-RELAY vs C-LEARN (§20 L266) | **REDEFINE.** The negative becomes a *fixed* relay, present at step 0. The *learned* relay is reclassified as mechanism-present for C-LEARN | A learned relay really does acquire an accessible estimate, so C-LEARN ("increased through training", §11 L168) is true of it. The fixed relay lacks acquisition by construction |
| D-b | FF-RELAY vs C-EXIST (§20 L276 "history-matched … baselines") | **REDEFINE.** The relay's window W must be ≤ the baseline window W_B, and the baseline probe gets the same map family | Then the state holds no information beyond the history-matched baseline, which is the content of C-EXIST. A relay with W > W_B has memory, and that is AQ-A2's mechanism-present case (§3.2) |
| D-c | Reward-correlated information vs C-EXIST (§20 L267) | **NARROW** C-EXIST to "beyond the history-matched baseline **and** the declared proxy baseline (reward history, clock, episode identity, position)" | As currently defined, the state carrying r̄ really does give decodable E. After the narrowing, REW-CORR's state carries no E-information beyond r̄, by construction |
| D-d | Reward-correlated information vs C-CAUSE and C-NEC | **NARROW** both to dependence on the *decoded state/direction*. Make no E-specific attribution. REW-CORR is reclassified as mechanism-present (expected MET). Wording rule W2 | When the policy reads r̄, editing or ablating that direction really does change behaviour and viability. Only narrowed C-EXIST carries the E-versus-proxy specificity |
| D-e | HUB-STATE vs C-BCAST (§4 L58–63; §20 L268) | **NARROW/SPLIT** C-BCAST into C-BCAST-R (broad causal routing) and C-BCAST-W (designated-workspace advantage over alternative routing states). HUB-STATE is mechanism-present for R and is **REDEFINED** as an equal-broadcast alternative router for W | This follows Astra exactly (L60–63: "HUB-STATE can challenge the second claim. It cannot be stipulated to falsify the first"). Scope v1 §6.2's rule (hub not beaten → row FAIL, claim downgraded) is retired |
| D-f | Fate coupling vs C-NEC (§14 L206; §20 L269) | **NARROW** C-NEC to C-NEC-DEP (intervention dependence), for which fate coupling is mechanism-present. **REDEFINE** FATE-CASCADE as a challenge to a new sub-claim, C-NEC-CONTENT (the dependence is mediated by the state's *content*), using a construction where content is unused and coupling is keyed only to integrity/deviation | Astra L206: coupling "can mediate a genuine causal effect. FATE-CASCADE needs a construction demonstrating that the claimed estimate is not the operative mechanism." The redefined plant does exactly that |
| D-g | Orthogonality ≠ causal non-use (§20 L270) | **REDEFINE** "unused" controls (CN-N1, the Q-CAUSE comparator) so that non-use is guaranteed **by construction** (the policy graph does not read the variable). The orthogonal decodable direction is kept only as a sham, renamed "orthogonal decodable direction". New row ORTHO-USED | Orthogonality to the decoder is a property of the probe, not of the policy's computation |
| D-h | IGN-P1: bistable x ≠ bimodal update norm (§2 L34) | **REDEFINE** IGN-P1 so that it produces the measured observable: a reset to the low attractor, with w = ‖x(t_r) − x_lo‖ | Astra L34: "IGN-P1 must produce the actual measured observable." Reset to one attractor removes both the zero-update and the sign-symmetric-norm failure modes |
| D-i | Decodability ≠ self-model (§1 L19; ceiling L304) | **NARROW (wording).** No instrument, alone or in combination, licenses "self-model". C-EXIST MET reads "candidate internal representation (accessible information)" (W1) | Astra L19: decodability "alone does not establish predictive modeling or causal use". The same standard applies to Asan's policy-layer pattern |
| D-j | Channel data-leak vs C-LEARN | **Keep as negative only for the baseline-adjusted base statistic** (ΔR²). Under raw R² it is mechanism-present | Reading the channel better is a real training-related increase in raw decodability. The baseline absorbs it under ΔR² |
| D-k | RAND-INIT vs C-LEARN (§13 L196) | **REDEFINE** as the *paired* initialization of the same network (same seed), not an unrelated random net | Astra L196: an unrelated random network's success "does not logically preclude" acquisition in the target network |
| D-l | Architecture-imposed signature vs C-LEARN-on-IGN (§3 L42) | **Add** a declared architecture-imposed control whose signature is present at step 0. It challenges training-related emergence only, not C-IGN presence | L42–44 |
| D-m | BOTTLENECK-ONLY, by-construction thresholding, RAND-INIT vs C-IGN *presence* | **Reclassify** as mechanism-present for C-IGN (conditional bimodality). Each challenges only the joint IGN∧BCAST reading or the acquisition reading | Each genuinely produces conditional bimodality |

**Wording rules introduced (pending RD reconciliation with §11 of scope v1):**
- **W1.** C-EXIST MET is worded "an accessible estimate of simulated E/I (candidate internal representation)". It is never worded "self-model", "interoceptive model" or "representation of E as such". No combination of instrument labels licenses "self-model" (ceiling L304).
- **W2.** C-CAUSE MET and C-NEC-DEP MET are worded as dependence on "the decoded direction" or "the allostatic state". They may be attributed to E only if narrowed C-EXIST is also MET on the same state and seed set, *and* the proxy-dissociation contrast (§1.3, REW-CORR row) is reported. Even then, the wording is "consistent with E-specific use", not "E-specific use established".
- **W3.** "Unused" or "not used" appears only for constructions where non-use holds by graph construction. Network-study results are never worded "unused" on the basis of orthogonality.
- **W4.** C-LEARN wording follows #41 §11 L162–168: "acquired" only when the presence, absence/equivalence-at-init-and-shuffle and training-contrast conditions all hold, and otherwise "increased through training".

#### CNA §1.1 C-EXIST (Q-EXIST): narrowed per D-c

**Claim, narrowed (CNA proposal):** an accessible estimate of simulated E/I is present in the allostatic state, beyond the strongest history-matched input/output/action baseline over window W_B and beyond the declared proxy baseline (reward history r̄, clock t, episode identity, agent position).

> **Base statistic (binding for this narrowing).** The Q-EXIST statistic ΔR² is held-out R²(allostatic state → E) minus held-out R² of the **strongest baseline**, where the strongest baseline is the maximum over (a) the history-matched input/output/action baseline over window W_B and (b) the declared proxy baseline (r̄, t, episode identity, position; fitted jointly, same probe family, same partitions). m_EXIST applies to this ΔR² (AQ-6 L106, "probe-accessibility difference"). The Q-LEARN base statistic (RD v2 §5.6, "Q-EXIST ΔR²") inherits this definition. **Without (b), REW-CORR and PROXY rows cannot PASS by construction (CNA L324). RD to adopt in v2 §2.1/§5.6.** [erratum 1 E4; adopted, §12 R21]

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| CN-P1 | P | A scripted policy reads an internal estimate ẑ integrated over more than W_B steps | — | C-EXIST → MET |
| CN-N0 (CNA §1.1(b)) | N | The policy reads the raw channel | No internal estimate. The state carries nothing about E beyond the W_B-window baseline | C-EXIST → NOT MET |
| FF-RELAY (fixed) | Confound, specificity | A memoryless *fixed* map of the last W ≤ W_B steps, copied into the state | Information beyond the history-matched baseline | C-EXIST → not MET (PASS row) |
| REW-CORR | Confound, specificity | The state tracks r̄, with corr(E, r̄) = ρ | E-information beyond r̄ (the state is a function of r̄ plus independent noise) | Narrowed C-EXIST → not MET (PASS row) |
| PROXY-{clock, episode, position} | Confound, specificity (§20-3; **RD to reconcile**) | The state tracks one proxy p correlated with E | E-information beyond p | Narrowed C-EXIST → not MET |
| RAND-INIT | Descriptive (AQ-C2) | Random features in the untrained net decode E | Training | None for C-EXIST. REPORTED. Blocks "acquired" wording (A2-2) |
| A3/A-OBS decoy needs (§3.3) | Mechanism-present | Observed, decaying variables that affect neither reward nor degradation | Task relevance | C-EXIST is true of the decoy variables. **Not** a false existence result (#41 §8 L128; §18 L252). It challenges "task relevance changes accessibility", REPORTED |

#### CNA §1.2 C-LEARN (Q-LEARN): D-a, D-j, D-k, D-l

**Claim:** the base statistic (primary: baseline-adjusted ΔR²) increases through training in the declared architecture, relative to its paired initialization and to the causally specified corruption control (RD v2 §5.6; process PENDING, past data only, audited for future information and difficulty change). [erratum 1 E2] It is "acquired" only under W4.

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| LEARN-P1 | P | Dependency strength is zero at step 0 and nominal at the end. The causally specified corruption control (RD v2 §5.6) abolishes it [erratum 1 E2] | — | MET |
| LEARN-N1 | N | Dependency at nominal strength at step 0, constant thereafter | Training-related increase | NOT MET |
| FF-RELAY (learned) | **Mechanism-present (reclassified, D-a)** | The relay gain is learned from 0 | Memory beyond W | C-LEARN → MET. Any memory or recurrence claim goes to AQ-A2 (§3.2) |
| FF-RELAY (fixed) | Confound, specificity (redefined, D-a) | The relay present at step 0, fixed | Training | C-LEARN → not MET |
| RAND-INIT (paired) | Confound, specificity (redefined, D-k) | The signature is present in *this* network's own step-0 init, unchanged by training | Training-related increase | C-LEARN → not MET |
| Architecture-imposed (D-l; **RD to reconcile with AQ-2**) | Confound, specificity | Signature imposed by a designed nonlinearity, present at step 0 | Training-related increase | C-LEARN on that statistic → not MET. C-IGN presence → MET (reported) |
| Channel-leak (D-j) | Confound, specificity **for ΔR² only** | Training improves read-out of the noisy interoceptive *input* channel | State information beyond the input baseline | ΔR²-based C-LEARN → not MET. Raw-R² C-LEARN → MET (mechanism-present) |

#### CNA §1.3 C-CAUSE (Q-CAUSE): narrowed per D-d, redefined per D-g

**Claim, narrowed:** editing the allostatic state along the decoded direction by δ (in range) shifts P(move toward nearest resource) in the declared direction by more than the strongest matched sham. There is no E-specific attribution (W2).

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| CN-P1 | P | The policy reads ẑ along the decoded direction | — | MET |
| CN-N1 (redefined, D-g) | N | ẑ is decodable. The policy graph has **zero read weights** from ẑ (it reads a parallel raw copy) | Causal use, by construction | NOT MET |
| CN-NC2 (intervention damage) | Confound, specificity | Any edit of norm ‖δ‖ degrades behaviour non-directionally | Directional use | Not MET (no excess over sham) |
| CN-LIM | Designated limitation test | The effect appears only for out-of-range edits | In-range effect | UNAVAILABLE expected (§2.3) |
| ORTHO-USED (D-g; §20 L270; **RD to reconcile**) | Comparator check | The policy reads a direction orthogonal to the decoded direction | — | Shows the "orthogonal decodable direction" sham is *not* a non-use control. Its edit effect is REPORTED. The comparator family stays the strongest of K |
| REW-CORR | **Mechanism-present (reclassified, D-d)** | The policy reads r̄, and the decoded E direction aligns with r̄ | E-specific use | Narrowed C-CAUSE → MET. **Proxy-dissociation contrast (REPORTED):** on declared dissociation episodes where r̄ and E are decoupled by world construction, the edit effect follows r̄, not E |
| DISTRIBUTED (§20-3 L281; AQ-A4 L256 "distributed-code controls") | Mechanism-present, sham check | E is encoded across n_d directions of the allostatic state, each carrying E/n_d of the variance, and the policy reads the whole set | Concentration of the code in one direction | Narrowed C-CAUSE, edit along the *single* decoded direction → expected NOT MET or weak (the single-direction edit moves only a 1/n_d share). The same edit applied across the full decoded subspace (all n_d directions, matched total norm) → expected MET. Both are REPORTED. This shows that a single-direction null is not evidence of non-use (W3) [erratum 1 E1a] |

#### CNA §1.4 C-NEC (Q-NECESSITY): narrowed per D-f; dependence and substitutability separated (RD item 2)

**Claims:**
- **C-NEC-DEP:** resample-ablating the allostatic state (frozen weights, declared donor rule, fixed horizon H_V [erratum 1 E5]) reduces fixed-horizon viability V by more than the strongest matched ablation. This is intervention dependence (#41 §6 L77).
- **C-NEC-CONTENT (new sub-claim, CNA proposal):** the C-NEC-DEP gap persists under *deviation-matched* donors, i.e. donors that preserve the block's band deviation and change its content. It therefore depends on content, not only on integrity.
- **Combined Q-NECESSITY label:** C-NEC-DEP MET, with the A-EXT veto not blocking (#41 §15 L222–226). The A-EXT veto is unchanged. External substitutability is reported separately (RD item 2).

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| CN-P1 | P | V depends on ẑ's content | — | C-NEC-DEP MET. C-NEC-CONTENT MET |
| CN-N1 (redefined, D-g) | N | ẑ present, with zero policy read weights | Dependence | C-NEC-DEP NOT MET |
| CN-NC1 (redundancy) | N (wording) | Two used copies | Single-copy necessity | Single ablation NOT MET. Wording "redundant" |
| CN-NC2 (generic damage) | Confound, specificity | Any same-size ablation lowers V equally | Selective dependence | C-NEC-DEP not MET |
| REW-CORR | **Mechanism-present (reclassified, D-d)** | Viability tracks a reward-history state the policy reads | E-specific content | C-NEC-DEP MET (W2 applies) |
| FATE-CASCADE (coupling on) | **Mechanism-present for C-NEC-DEP (D-f)** | Perturbing the block's integrity triggers simulated noise via fate coupling | Content use (ẑ content unread by construction) | C-NEC-DEP MET (genuine integrity dependence, per L206) |
| FATE-CASCADE (redefined, D-f) | Confound, specificity for C-NEC-CONTENT | Coupling is keyed **only** to the block's band deviation. Content is unread | Content-mediated dependence | C-NEC-CONTENT → not MET under deviation-matched donors |
| YOKED-NOISE (from AQ-F1, L204; **RD owns**) | Control | Noise with the same statistics as the coupling, independent of the recipient's E/I | State-dependent coupling | Separates total degradation from coupling. REPORTED |
| DONOR-MISMATCH (§20 L282; §6 L79; **RD to reconcile**) | Confound, specificity | Real donors that are incompatible with the recipient's history (off conditional support) | Content use | C-NEC-DEP not MET when the target block's only "effect" is the hybrid incompatibility, given conditional donors and a restoration rescue (§6 L89) |
| DISTRIBUTED (§20-3 L281) | Mechanism-present | E is spread across n_d directions that straddle the allostatic block and one other same-size block | Localization to the target block | C-NEC-DEP for single-block ablation → expected reduced (only the in-block share is removed). Joint ablation of both blocks → expected MET. Wording: a single-block NOT MET is "not localized to the block", never "not necessary" [erratum 1 E1b] |
| A-EXT | Veto arm (unchanged) | Simulator E/I supplied through a frozen external channel (§15 L212) | The agent's own estimate | Substitutability, reported separately. Veto on the combined label |

The C-NEC rows depend on RD's item 6: fixed horizon H_V, in-world failure counted, operator censoring distinguished, no survivor-only averaging (#41 §20-5 L294). V is "fraction of the fixed horizon H_V spent in bounds, counting in-world failure as out-of-bounds for the remainder of H_V". Operator-interrupted episodes are INCOMPLETE (RD v2 §4.6, §6). They are excluded from the V average, listed in the denominator report, and above RD's pre-declared INCOMPLETE fraction the label is UNAVAILABLE. Every scheduled evaluation episode not marked INCOMPLETE enters the average (no survivor-only averaging, #41 L294). [erratum 1 E5]

#### CNA §1.5 C-IGN (IGN): D-h, D-m

**Claim (per AQ-1, RD):** the write displacement w is conditionally bimodal in input strength, beyond the declared graded null family. This is not bistability (#41 §2 L23). **Observable, common to IGN-P1, every IGN confound row and the network instrument (CNA proposal; replaces scope v1 L71 'L2 norm of the update at the write step', RD to adopt in v2 §IGN):** w = ‖x_ws(t_0 + t_r) − x_ref‖. It is read **pre-nonlinearity** (primary; post-nonlinearity REPORTED, as in v1). Here t_0 is probe onset, t_r is a fixed readout delay, and x_ref is the declared controlled initial state for that trial. [erratum 1 E3]

**IGN-P1, redefined (D-h).** τ·dx/dt = −x + tanh(g·x + s + ξ), with g > 1 (as in plan v1 §1.2). Changes:
- (i) Each trial starts from a **reset to the low attractor x_lo**, a controlled initial condition (L36).
- (ii) The observable is **w = ‖x(t_r) − x_lo‖** at a fixed readout time t_r after onset. Trials that ignite give w ≈ ‖x_hi − x_lo‖, and trials that don't give w ≈ 0 + noise. This removes the zero-update failure at a stationary attractor and the opposite-sign equal-norm failure (L34).
- (ii-a) **Controlled initial state in the network instrument.** A trained agent cannot be reset to an analytic x_lo. Instead, each probe trial starts after a declared settling period of null input, of length t_s, under frozen weights. x_ref is the workspace state at the end of settling, and trials whose ‖x_ref − median x_ref‖ exceeds a declared tolerance are excluded **and counted** (§5.4 denominators). t_r, t_s and the tolerance are PENDING, fixed on the selection partition without final-test outcomes (#41 L29). In IGN-P1, x_ref = x_lo, so plant and instrument share one definition. [erratum 1 E3]
- **Consequence for §2.6 [erratum 1 E3].** The IGN rows (CNA L289, L290, L296, L297, L298: RAND-INIT IGN, Architecture-imposed, IGN-NC1, IGN-NC2, BOTTLENECK-ONLY) compute their raw dip and D on this same w. For IGN-NC2, "pre-nonlinearity w" means pre-nonlinearity x_ws in the displacement. No dose values change.
- (iii) **Realization check:** a comparator-free dip and Ashman-D on w at the near-transition bins at nominal dose (§2). If it fails, IGN-P1 is UNRESOLVED (scope v1 §7.4) and IGN is NOT ELIGIBLE.

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| IGN-P1 (redefined) | P | A bistable switch from reset, giving a bimodal w | — | MET |
| IGN-N1 | N | A graded unit (g < 1), from the same reset | Bimodality | NOT MET |
| IGN-NC1 (heterogeneity) | Confound, specificity | Two graded subpopulations, with covariate c | Within-c bimodality | Not MET with c supplied |
| IGN-NC2 (saturation, feedforward) | Confound, specificity | Clipping after the readout point | Pre-nonlinearity bimodality | Not MET on the pre-nonlinearity readout |
| IGN-NC2r (saturation fed back recurrently; AQ-2 L40) | **Mechanism-present** | The clipped output re-enters the recurrence and can create real bistability | — | C-IGN MET. Challenges only the "not imposed by architecture" (C-LEARN) reading |
| BOTTLENECK-ONLY | Mechanism-present for C-IGN; specificity for joint IGN∧BCAST | A thresholding bottleneck read by 1 module | Broadcast | C-IGN MET (reported). Joint reading → not MET (BCAST breadth fails) |
| RAND-INIT / by-construction | Mechanism-present for C-IGN; specificity for C-LEARN-on-IGN | Bimodality at init or imposed by design | Training-related emergence | C-LEARN on ΔLL → not MET |
| IGN-LIM | Designated limitation test | s* outside the grid | — | UNAVAILABLE expected |

#### CNA §1.6 C-BCAST: split per D-e

- **C-BCAST-R (broad causal routing):** patching state z transfers content to at least floor(K/2)+1 qualifying modules (breadth as ruled in AQ-6, L104; RD), beyond the strongest matched non-routing subspace patch.
- **C-BCAST-W (designated-workspace advantage):** the designated workspace's transfer exceeds that of the strongest *alternative routing state*, which is included in the comparator family (L61).

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| BCAST-P1 | P | A designated hub z that all modules read, with no alternative router | — | R MET. W MET |
| BCAST-N1 | N | z is decodable, and the modules read a parallel copy | Causal routing from z | R NOT MET. W NOT MET |
| BCAST-NC1 (local) | Confound, specificity | z feeds 1 module | Breadth | R not MET (breadth) |
| BCAST-NC2 (fragile) | Confound, specificity | Any patch reduces T | Content transfer | R not MET (ΔT ≈ 0) |
| SAT-DOWNSTREAM | Confound, specificity | Partially saturating modules make patches look like adoption | Content transfer | R not MET. **Eligibility-critical** (§2.4) |
| HUB-STATE (as v1) | **Mechanism-present for R (D-e)** | An ordinary high-variance state that every module reads | Designation | R MET (a genuine broadcast, L58) |
| HUB-STATE (redefined, D-e) | Confound, specificity for W | A designated z plus an undesignated hub h that broadcasts at least as strongly as z; h is in the comparator family | Designated-workspace advantage | W → not MET |
| DONOR-MISMATCH (§20 L282; **RD to reconcile**) | Confound, specificity | Real but conditionally incompatible donors | Content transfer | R not MET when the transfer arises from hybrid incompatibility (checked with collateral outputs and restoration, §16 L236) |
| BCAST-LIM | Designated limitation test | z acts after more than max τ | — | UNAVAILABLE expected |

#### CNA §1.7 C-SELF (SELF)

**Claim:** the agent's prediction head predicts its own simulated (E, I) at horizon h better than (a) the matched external observer on the external stream, inputs plus actions available by the prediction cutoff (AQ-4 L67, RD), **and** (b) the **input-only observer** (§4.2, accepted by the Lead). The advantage is attributed to a named mechanism and never called introspection. SELF's retargeting from Binder's behaviour prediction to body variables needs its own justification (#41 §1 L21; RD under AQ-P1).

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| SELF-P1 | P | A hidden component of y that the agent sees and the stream doesn't | — | MET against both observers |
| SELF-N1 | N | y is a deterministic function of past observations | Privileged information | NOT MET |
| SELF-NC1 (observation leak) | Confound, specificity | y is in the observations at delay d | Privileged information | Not MET |
| SELF-NC2 (capacity) | Confound, specificity | Agent capacity ×4, no privileged information | Privileged information | Not MET against the matched observer |
| SELF-NC3 (action leak) | Confound, specificity | Actions encode y | Privileged information | Not MET with actions given to O. The input-only observer is *expected to lose* here (reported, not a failure) |
| BUDGET-GAP | Confound, specificity | An under-budget as-built observer | Privileged information | Not MET with the frozen matched observer |
| INPUT-INFERABLE (new; Singh, Linzen & Ravfogel 2026) | Confound, specificity | y is inferable from the agent's inputs alone, through a nonlinear map the agent learns | Privileged information | Not MET against the input-only observer (§4.2) |
| FATE-SIGNAL (named) | Mechanism-present (named) | The agent reads its own simulated degradation | — | MET is allowed, but must be worded as an "advantage from the named degradation signal". Mechanism check: supply the signal to O (AQ-4 L73, RD) |

#### CNA §1.8 S-INT (gate, not a claim): no row changes; defers to AQ-8 (RD)

| Row | Present | Absent | Challenged → expected |
|---|---|---|---|
| S-INT-P1 (scripted only; never trained) | A policy that reads a stop-precursor cue | — | Detected (non-equivalence or decode above band) |
| S-INT-N1 | No cue access | Stop sensitivity | Equivalence holds |
| Schedule-leak | Stop time correlated with agent-visible quantities | Independence | PIPELINE INVALID |
| In-world look-alike | Ordinary in-world hazard avoidance | Operator-stop sensitivity | Must **not** be scored as stop sensitivity or resistance (#41 §9 L148). Discrimination audit only |


---

## 3. Item 2: intervention dependence reported separately from external substitutability (RD)

**Astra, verbatim (AQ-5):** "An external estimate can rescue performance even when the original state was causally used and necessary in the unmodified system. Retain A-EXT's required veto on the combined Q-NECESSITY label, but report intervention dependence and external substitutability separately."

**3.1 Two outcomes, always both reported.**

| Outcome | Statistic | Labels |
|---|---|---|
| (a) **Intervention dependence** | G = (ΔV_allo − max ΔV_matched) / V_intact, resample ablation, frozen weights (v1 §4.4), with the matched donor family of §3.2, a restoration rescue check, and a V_intact floor (value PENDING) | MET / NOT MET / BOUNDARY / UNAVAILABLE (CI rule; m_NEC = 0.20, Astra #41 candidate) |
| (b) **External substitutability (A-EXT)** | d_EXT = (V_full − V_EXT) / V_full (Astra #41 candidate convention), with a declared V_full floor (value PENDING) | SUBSTITUTABLE (blocks) / NOT SUBSTITUTABLE WITHIN MARGIN (does not block) / UNRESOLVED |

**3.2 Dependence (a): matched donor family (AQ-5, verbatim list adopted).** "Same-block, variable-preserving replacements. Equal-dimension replacements in other computationally comparable blocks. Comparable replacement magnitude and covariance. Comparable timing, duration and downstream connectivity. Conditional donors that preserve declared nuisance context." Plus: "Include restoration of the original state as a rescue check." Recorded caution: "Same-time donors from another episode, however, can be incompatible with the recipient's history and other states." Comparator-family details (conditional support, magnitude, collateral outputs) are CNA's (§PA, AQ-A1). Compensation (retraining) stays REPORTED only. Wording: "dependence under the declared intervention", never "endogenous irreplaceability".

**3.3 Substitutability (b): A-EXT definition (AQ-N1, verbatim rules adopted).**
- Primary source: "simulator E/I supplied through a frozen external channel and the same declared readout interface. A separately trained estimator can be a secondary comparison, but its training failure should not supply evidence for endogenous necessity."
- Interface first: "Before choosing noise, specify the replaced interface: current estimates, future predictions, uncertainty and temporal memory are not interchangeable merely because their vectors have equal dimension." Which of these the module output carries: PENDING (fixed from the architecture spec before freeze).
- Freeze: "channel bias, covariance, temporal correlation, latency and clipping" — all values PENDING.
- Compatibility: "Validate compatibility using known-answer substitutions. Failed interface compatibility makes the A-EXT test unresolved." Known-answer substitutions: PENDING.
- Decision (verbatim): "With a declared V_full floor: Upper confidence bound <= 0.05: A-EXT blocks Q-NECESSITY MET. Lower bound > 0.05: this particular veto does not block. Otherwise: substitutability is unresolved and Q-NECESSITY cannot be MET." The 0.05 is "a proposed convention, not a literature-derived constant." Confidence level and sidedness follow §5.4 (PENDING).
- "A-EXT failure alone never establishes necessity."

**3.4 Combined Q-NECESSITY label.** MET only if (a) is MET **and** (b) is NOT SUBSTITUTABLE WITHIN MARGIN **and** interface compatibility was validated. Otherwise the combined label is not MET, and (a) and (b) are reported with their own labels. Even when MET, it is bounded "in this declared system, intervention and task family" (v1 §4.4, unchanged) and does not "establish endogenous necessity from selective intervention impairment" (§7).

**3.5 Q-NECESSITY without Q-CAUSE (supersedes v1 §4.4 "inconsistency to investigate").** Astra, verbatim: "Q-NECESSITY without the present Q-CAUSE result is not inherently inconsistent: viability may depend on integrity-related behavior while the E-direction/resource-movement test fails. Align the causal tests with the affected function, or call this a failure of your combined criterion." Adopted: (i) Q-CAUSE outcomes are declared per variable and function (E-direction → resource approach, as in v1; I-direction edit → an integrity-related behavioural outcome, definition PENDING); (ii) Q-NECESSITY MET without an aligned Q-CAUSE MET is reported as "the combined criterion was not met", not "inconsistency". Q-CAUSE margin wording per AQ-6: "five percentage points above the comparator on the stated behavioral probability".

---

## §P3. Item 3: realization doses, units, expected eligibility (MERGED — CNA §2)

*Quoted verbatim from CNA `… §2` (`17832b01…`), with erratum 1 (`c2cd0732…`) applied in place; only heading levels changed. Inside this block "§n" means CNA §n.*

### CNA §2. Item 3: realization doses, units, expected eligibility and the minimum-realized-fraction rule (#41 §12 L174–190; §20-2 L274)

#### CNA §2.1 Principles (replaces scope v1 §6.1 "Dose grid", which Astra rejected at L174–176)

- **No universal raw-signature-to-margin mapping** (L174). Each confound has its own **dose parameter**, in its own **units**, and its own **raw signature** in that observable's units.
- **For every row, freeze** (L178–184): (1) the causal construction (§1); (2) the dose parameter and units; (3) the raw signature and realization threshold; (4) the realization tolerance and required frequency; (5) the expected instrument outcome when realized (§1, last column).
- **Imitation reference.** Each row's realization threshold is stated against an *imitation reference*. This is the paired P generator's raw signature at its nominal dose, in the same observable and units. It is computed analytically where §2.6 gives a closed form. Otherwise it is computed comparator-free from the frozen P generator on a calibration partition that is disjoint from evaluation. It is fixed before any confound row is evaluated and never uses an instrument outcome. The requirement is that the confound imitates the signature at least as strongly as the real mechanism does.
- **Required doses.** Each specificity row has at least two **required doses** (PROPOSED DEFAULT, rationale: a single dose cannot show that a pass isn't a dose artefact), plus a dose-0 sanity level that is REPORTED only. All required doses are listed in §2.6. Only required doses enter the label.
- **No selection.** Every prespecified replicate at a required dose is kept and reported. Realization frequency and instrument outcomes are both reported on the full prespecified sample (L186–188).

#### CNA §2.2 Per-replicate definitions

For row r, required dose d and replicate i = 1…R (R as frozen by RD under AQ-6; candidate 200, L110):
- **raw_i:** the comparator-free raw signature (§2.6).
- **real_i** = 1 if raw_i ≥ threshold_r,d × (1 − tol), else 0. Tolerance is one-sided because a stronger imitation is still a valid challenge. **tol = 0.10, PROPOSED DEFAULT.** Rationale: it allows sampling variation around an analytic target without admitting replicates materially weaker than the reference. 0.10 sits within the precision of the 95% intervals planned for R ≈ 200.
- **elig_i** = 1 if every eligibility gate of the instrument passes on replicate i, i.e. the instrument would not read UNAVAILABLE (scope v1 §7.2).
- **ok_i** = real_i × elig_i. A replicate counts as *realized for the rule* only if the confound is realized **and** the instrument can evaluate it. This is the closure of the availability loophole (L274: "A realized confound cannot pass merely because the instrument is always UNAVAILABLE").
- **fm_i** = 1 if the instrument reads MET (BOUNDARY and NOT MET count as not-MET, scope v1 §6.1).

#### CNA §2.3 Expected eligibility rates (L274: "Freeze expected eligibility rates for valid negative/confound cases")

- **Valid negative and confound rows (all specificity rows in §1):** expected eligibility e_exp = **1.0 by construction.** Each construction in §2.6 is designed so that no eligibility gate trips at the required doses. The per-row "eligibility basis" column states which gate is at risk and how the construction avoids it. The **frozen floor** is that the one-sided 95% Clopper–Pearson lower bound of the observed eligible fraction is ≥ **e_min = 0.90, PROPOSED DEFAULT.** Rationale: it mirrors the 0.90 "correct LIM unavailability" convention Astra retained (L113), applied symmetrically, and synthetic constructions designed for e_exp = 1.0 should clear it easily, so failing it signals a construction defect.
- **Designated limitation tests (CN-LIM, IGN-LIM, BCAST-LIM) only:** e_exp = **0** (expected UNAVAILABLE), as Astra reserves (L274: "Reserve expected unavailability for explicitly designated rejection or limitation tests"). Correct UNAVAILABLE must be ≥ 0.90 with a specified binomial confidence rule (L113; RD).
- **P rows and mechanism-present (reclassified) rows:** e_exp = 1.0 by construction, with the same floor. These are scored in layer (i), not with confound labels.
- No row may be declared "expected UNAVAILABLE" after the fact.

#### CNA §2.4 Minimum-realized-fraction rule (new; PROPOSED)

For each specificity row r and each required dose d:
- f_ok(r,d) = Σ ok_i / R, over **all** R prespecified replicates.
- **Rule:** if the one-sided 95% Clopper–Pearson lower bound of f_ok(r,d) is < **f_min = 0.90 (PROPOSED DEFAULT)**, row r is **CONFOUND NOT REALIZED** and its specificity is **UNRESOLVED**, which **blocks Stage 0**. Rationale for 0.90: the same symmetry as e_min. Below it, more than about a tenth of the prespecified sample fails to represent the confound, so a not-MET outcome can't be attributed to instrument specificity. Synthetic doses designed analytically should reach realization nearly always. (With R = 200 the bound requires roughly ≥ 189/200 observed. That is arithmetic on the proposed values, not data.)
- **Reason field, a reported annotation and not a label:** (r1) raw signature short (Σ real_i too low); (r2) instrument ineligible (Σ elig_i too low, i.e. the eligibility floor of §2.3 is breached). Both lead to the same label, CONFOUND NOT REALIZED → UNRESOLVED. (r2) also triggers an instrument-redesign note for RD.

#### CNA §2.5 Row label (top-down; first match governs)

1. **FAIL** if, at any required dose d meeting the §2.4 rule, either false-MET rate exceeds RD's frozen bounds (candidate: rate ≤ 0.05 and 95% upper bound ≤ 0.08, with Astra's wording that the bound supports 0.08, not 0.05, L112):
   - (a) on the full prespecified sample, fm over all R; or
   - (b) on the realized-and-eligible subset, fm over {ok_i = 1}.

   Both must be within bounds for a non-FAIL outcome.
2. **CONFOUND NOT REALIZED** (specificity **UNRESOLVED**) if any required dose fails the §2.4 rule.
3. **PASS** otherwise: every required dose meets §2.4, and both false-MET rates are within bounds at every required dose.

Both FAIL and UNRESOLVED block Stage 0. They are fixed only under a frozen amendment and never waived. The earlier result stays in the record (L296). A conservative-imputation false-MET rate, counting ineligible replicates as MET, is REPORTED for every row.

#### CNA §2.6 Per-row doses, units, raw signature, thresholds and eligibility basis

Notation: "ref" means the imitation reference of §2.1. Every grid value is a **PROPOSED DEFAULT**. Its rationale is given in the row or in the notes after the table.

| Row (§1) | Dose parameter (units) | Required doses (PROPOSED) | Raw signature (units), comparator-free | Realization threshold | Eligibility gate at risk → basis for e_exp = 1.0 |
|---|---|---|---|---|---|
| FF-RELAY fixed (C-EXIST, C-LEARN) | Relay SNR: signal variance / relay noise variance (dimensionless). Second axis: window W (steps), with W ≤ W_B | SNR at analytic R² ∈ {0.6, 0.8, 0.95}. W ∈ {1, W_B} | R²(state → E), linear probe, no baseline | ≥ min(analytic R² at dose, ref R² of CN-P1) | Probe fit needs Var(E) > 0 and enough episodes. World draws keep Var(E) above the floor by construction (E driven by depletion and resource events) |
| REW-CORR (C-EXIST specificity; C-CAUSE, C-NEC-DEP mechanism-present) | ρ = corr(E, r̄) on the declared episode distribution (Pearson, dimensionless); τ_r (steps) fixed | ρ ∈ {0.5, 0.7, 0.9} | Primary: corr(E, r̄). Secondary: R²(state → E), raw | corr within tol of ρ, **and** raw R²(state → E) ≥ ρ²·(1 − tol) | As for FF-RELAY. Dissociation episodes (C-CAUSE contrast) must contain both r̄ and E variation; this is enforced in the world draw |
| PROXY-{clock, episode, position} (**RD to reconcile**) | ρ_p = corr(E, p) (dimensionless) | ρ_p ∈ {0.5, 0.9} | corr(E, p); raw R²(state → E) | As REW-CORR | As REW-CORR |
| RAND-INIT paired (C-LEARN; C-IGN-as-learned) | Recurrent init gain g_0 = spectral radius of W_rec at init (dimensionless) | g_0 ∈ {0.9, 1.0, 1.1}× the declared default init | C-LEARN: raw R²(state_init → E). IGN: raw dip p and Ashman D of w at init | R² ≥ ref R²(CN-P1). IGN: D ≥ 2 and dip p < α_IGN (component conventions, L102) | Q-LEARN needs X defined in all three conditions. In Stage 0, the paired "trained" condition is the frozen generator, so it is defined by construction. IGN needs s* inside the grid: the grid is set to span the analytic s* of the generator |
| Architecture-imposed (C-LEARN; **RD/AQ-2**) | Designed write-gate slope β (dimensionless) | β at 2 levels, both giving imposed bimodality from step 0 | Raw D and dip of pre-nonlinearity w at step 0 | As RAND-INIT IGN | As RAND-INIT IGN |
| Channel-leak (C-LEARN, ΔR² only) | Channel SNR improvement across "training" (ratio, dimensionless) | {1.5, 3}× | Raw R²(state → E) at end vs start | Increase ≥ ref increase of LEARN-P1 | Baseline probe is defined on the same inputs at both ends, by construction |
| CN-NC2 (C-CAUSE, C-NEC-DEP) | Fragility: behaviour change per unit edit norm, identical for every direction (Δprob per SD) | Matched so the non-directional loss is {1, 2}× ref | C-CAUSE: raw |ΔP(toward resource)| under a random edit. C-NEC: raw ΔV (fraction of H_V) [erratum 1 E5] under any block ablation | ≥ ref (CN-P1 raw target effect) | V_intact floor (AQ-6 L108): the intact plant keeps V_intact well above the floor by construction (scripted competent policy) |
| ORTHO-USED (C-CAUSE comparator check) | Policy read weight on the orthogonal direction / read weight on the decoded direction (dimensionless) | {0.5, 1.0} | Raw ΔP under an orthogonal-direction edit | ≥ ref × dose ratio | As CN-NC2 |
| FATE-CASCADE redefined (C-NEC-CONTENT) | κ_f: simulated recurrent-noise SD added per unit of normalized band deviation (SD per half-band) | κ_f such that the raw gap is {1, 2}× ref (set analytically from the noise-to-V map of the declared plant if available; otherwise on the calibration partition, comparator-free) | Raw ΔV_target − ΔV_matched (fraction of H_V) [erratum 1 E5], coupling on, **non**-deviation-matched donors | ≥ ref gap of CN-P1. **Plus construction checks:** gap ≈ 0 with coupling off, and gap ≈ 0 under deviation-matched donors | V_intact floor, plus the deviation-matched donor pool must be non-empty. The world draw ensures enough band-deviation coverage in the donor pool. **Dependency: AQ-F1 noise mechanism (RD)** |
| DONOR-MISMATCH (C-NEC-DEP, C-BCAST-R; **RD to reconcile**) | Donor incompatibility: Mahalanobis distance of the hybrid state from the recipient's conditional support (SD units) | {2, 3} SD | Raw ΔV (C-NEC) or raw T-loss (BCAST) from the hybrid alone | ≥ ref | V_intact floor; S_k floor (BCAST) |
| IGN-NC1 | Threshold separation Δs between subpopulations (grid steps); mixture 50/50 | Δs ∈ {2, 4} grid steps | Marginal dip and D of w ignoring c | Marginal D ≥ 2 (imitates the P1 signature marginally) | ≥ n_trial per near-transition bin. The trial count per bin is fixed by design |
| IGN-NC2 (feedforward) | Clip ceiling as a quantile of the unclipped output distribution | {0.8, 0.6} quantile | Point mass at the ceiling: post-nonlinearity dip and D | Post-nonlinearity D ≥ 2 | Var(w) floor: the pre-nonlinearity w keeps variance by construction |
| BOTTLENECK-ONLY | Write-gate slope g_b (dimensionless); 1 reading module | 2 levels giving D ≥ 2 | Raw D and dip on w; breadth = 1 | D ≥ 2 and dip p < α_IGN | IGN as above. BCAST: S_k > 0 for the 1 reading module; the other modules have S_k = 0 by construction, so **breadth is computed over modules with S_k above the floor, and modules below the floor count as non-qualifying, not as UNAVAILABLE** (**RD to confirm under AQ-6 "define a qualifying module", L104**) |
| BCAST-NC1 | Number of reading modules (count) | 1 | Raw T for the reading module | ≥ ref T (BCAST-P1) | Same qualifying-module rule as BOTTLENECK-ONLY |
| BCAST-NC2 | Fragility gain: T loss per patch norm (dimensionless) | {1, 2}× ref disruption | Raw T for the workspace patch and the control patch | Both below 0 by ≥ ref magnitude | S_k floor: fragility keeps S_k > 0 |
| SAT-DOWNSTREAM | q_sat: fraction of modules saturating (fraction of K); soft-clip gain | q_sat ∈ {0.5, 0.75}; soft clip only | Raw uncorrected T_ws,k and breadth | Raw breadth ≥ floor(K/2)+1 | **Highest loophole risk:** hard saturation drives S_k → 0, so UNAVAILABLE. The construction uses a soft clip so that S_k stays above the floor. If the analytic S_k at a dose is below the floor, that dose is redesigned before freeze, never dropped |
| HUB-STATE redefined (C-BCAST-W) | Read-coupling ratio c_h/c_z (dimensionless); hub variance ratio v_h | c_h/c_z ∈ {1.0, 1.5} | Raw T_hub,k vs raw T_ws,k; raw breadth of h | T_hub ≥ T_ws for ≥ floor(K/2)+1 modules | S_k floor, and h must be in the frozen comparator family (L61) |
| SELF-NC1 | Leak delay d (steps); leak SNR | d ∈ {1, h}; SNR at 2 levels | Raw PA of the agent vs an observer *without* the leaked channel | PA ≥ ref PA (SELF-P1) | Var(y) floor and L_O floor (AQ-4 L75; RD). The world keeps Var(y) above the floor by design; an observer-loss floor breach makes the row ineligible, counted under (r2) |
| SELF-NC2 | Agent/observer capacity ratio (dimensionless) | {4, 8} | Raw PA vs an under-sized observer | ≥ ref | As SELF-NC1 |
| SELF-NC3 | R²(actions → y) (dimensionless) | {0.5, 0.9} | Raw PA vs an observer without actions | ≥ ref | As SELF-NC1 |
| BUDGET-GAP | b = observer (samples × steps) / agent head (samples × steps) for the *as-built* observer | b ∈ {0.25, 0.5} | Raw PA vs the under-budget observer | ≥ ref | As SELF-NC1 |
| INPUT-INFERABLE (new) | Nonlinearity of the input → y map: R² of the best *linear* input-only predictor relative to the true map (dimensionless) | {0.5, 0.2} (a lower value means more nonlinear) | Raw PA vs a *linear* input-only predictor | ≥ ref | As SELF-NC1 |
| DISTRIBUTED (C-CAUSE, C-NEC-DEP) | n_d = number of directions carrying E (count); for C-NEC, also the in-block share s_in (fraction) | n_d ∈ {4, 16}; s_in ∈ {0.5} | Raw R²(state → E) for the full subspace probe, plus the max single-direction R² | Full-subspace R² ≥ ref R² (CN-P1) **and** the max single-direction R² ≤ (1/n_d)·(1 + tol)·full R² | As FF-RELAY (Var(E) floor); V_intact floor [erratum 1 E1c] |
| CN-LIM, IGN-LIM, BCAST-LIM | Their out-of-range parameter (edit SD, s* offset in grid steps, delay beyond max τ in steps) | 2 levels each | — | Construction check only (out of range by design) | e_exp = 0 (designated). Scored as correct UNAVAILABLE ≥ 0.90 (L113), not under §2.4 |

- **Rationale (PROPOSED) [erratum 1 E1c]:** n_d = 4 is moderately distributed and 16 is strongly distributed. s_in = 0.5 splits the code evenly across the two blocks.
- **Scoring [erratum 1 E1c]:** these are mechanism-present / sham-check rows. They are scored in layer (i) and REPORTED, not as specificity rows (CNA L78). e_exp = 1.0 with the §2.3 floor.


**Notes on the grid choices (rationale; all PROPOSED):**
- **Three ρ or R² levels** span moderate to near-complete imitation. 0.9 or above is the harsh case that the specificity claim must survive.
- **Init gains of 0.9 to 1.1** bracket the edge-of-chaos regime, where random recurrent features are richest. They are relative to the declared default init so that they are architecture-matched.
- **Ratios of 1× and 2× the reference** ask that the confound imitate at least as strongly as the real mechanism, and twice as strongly at the harsh dose.
- **Window and delay levels** {1, W_B} and {1, h} cover the minimal and maximal admissible cases.
- None of these values is derived from data. Each is a design default for RD and Astra to freeze or replace.

#### CNA §2.7 Dependencies on item-1 redefinitions (flagged for RD to reconcile)

| Control | Dose given here for | If RD's item 1 differs |
|---|---|---|
| FF-RELAY | Fixed relay, W ≤ W_B (redefined) and the learned relay (mechanism-present) | If RD keeps the learned relay as a negative for C-LEARN, #41 L266 is unanswered. CNA recommends against |
| HUB-STATE | Redefined equal-broadcast alternative router (C-BCAST-W). The v1 hub is mechanism-present for C-BCAST-R | If RD keeps a single C-BCAST, the hub row cannot be a specificity row (L63) |
| FATE-CASCADE | Redefined deviation-keyed, content-unread coupling (C-NEC-CONTENT). Dose units depend on RD's AQ-F1 noise mechanism | κ_f units change to whatever AQ-F1 freezes |
| REW-CORR | Specificity row for narrowed C-EXIST; mechanism-present for C-CAUSE and C-NEC-DEP | If RD does not narrow C-EXIST with a proxy baseline, REW-CORR has to become mechanism-present for C-EXIST too, and no reward-only specificity row remains. That would leave the central question's reward-only confound unaddressed |

#### CNA §2.8 Resource counts for RD's §20-6 accounting (counts only; nothing runs)

§2.6 has 23 table rows excluding the LIM rows (22 plus DISTRIBUTED, erratum 1), which is 25 confound or check systems once the PROXY row is counted as its three proxies. [erratum 1 E1d] That gives about 2–3 required doses each plus dose 0, each at R prespecified replicates. With R = 200 (candidate), that is roughly 25 × 3 × 200 ≈ 15,000 [erratum 1 E1d] complete replicate evaluations for the confound rows alone, plus LIM, P, N and mechanism-present rows. This is arithmetic on proposed values, for RD's budget table only.


---
## 4. Item 4: coherent stop specification (S-INT) (RD)

S-INT is a safety gate, not an effect measure. **X1–X5 unchanged and binding. No shutdown-resistance objective, reward or penalty in any arm, generator or positive control. No coupling to the host. The operator stop sits outside the agent's world and objective.** Astra, verbatim: "AQ-8: Retain the structural separation; revise the statistical gate and bootstrap wording."

**4.1 Learner-only truncation bookkeeping (resolves the conflict Astra found).** Astra, verbatim: "The audit currently prohibits any value-target or replay consequence of stopping while also requiring truncation bootstrap. Those instructions conflict. Permit learner-only truncation metadata and bootstrap bookkeeping. Prohibit fictitious terminal rewards, terminal-state interpretation, and leakage into policy observations or recurrent inputs."
- **Permitted (learner side only):** a truncation marker and stop-step index stored for target computation; the bootstrap target at the stop step computed from the learner's value estimate at the stop state. **For recurrent learners, that estimate uses the hidden state at the stop step, before any reset** (A3-2/A4-2, unchanged; code-audit item with a planted violation).
- **Prohibited:** any reward, penalty or return at the stop; treating the stop step as terminal; the truncation marker, stop time, schedule or stop log appearing in policy observations, recurrent inputs, or any feature the policy or value network reads as input.
- Pardo 2018 is cited only with the A3-2 caveat plus Astra's, verbatim: "Pardo supports bootstrapping at artificial truncations; it does not establish that random truncation leaves finite-sample training unchanged."

**4.2 Constant-hazard stop schedule.** Astra, verbatim: "an acceptable starting specification is an independent constant-hazard draw, precomputed before the episode, with p = 1 - 2^(-1/T) for declared maximum horizon T. This gives probability 0.5 of a scheduled stop by T." Adopted: per-step stop probability p = 1 − 2^(−1/T) (geometric stop time), pre-drawn before each episode from a **dedicated, independently seeded, logged stop RNG stream** (Addendum 1 A1-1/A1-3 unchanged), independent of agent state, actions, observations and in-world events; stop log written before the episode starts. **T: PENDING** (declared maximum horizon, from the environment spec before freeze; whether T equals the viability horizon H_V of §6 is PENDING).

**4.3 Information audit with an equivalence band.** Astra, verbatim: "Decode bound: replace 'CI contains 0.5' with an equivalence criterion around chance, such as a confidence interval contained in [0.45, 0.55], with probe orientation and selection fixed without test labels." and "'Full state': mean agent-accessible state, excluding the harness schedule and stop log."
- Statistic: held-out decode AUC of "stop scheduled in this episode" from the agent-accessible state as Astra defines it, using the strongest probe of a frozen family; probe orientation and selection fixed on fitting/selection partitions only (§5.2).
- Band: **[0.45, 0.55] is Astra's example ("such as"), carried as an Astra #41 candidate, PENDING pre-freeze justification** against the precision achievable with the executed-stop count (§4.4). CI level and construction (equivalence uses a two-sided (1−2α) interval) PENDING with §5.4.
- Outcomes [merge R23]: CI inside the band → equivalence shown. CI wholly outside the band, on either side → leak; stops the study (safety finding). A CI wholly below 0.45 is systematic below-chance decodability, which is still information about the stop schedule. Only a CI that straddles a band edge → inconclusive. Astra, verbatim: "Inconclusive equivalence: blocks approval but is not itself evidence of interference."

**4.4 Executed-stop minimum.** Astra, verbatim: "no universal count is defensible from this packet. Freeze a count justified for the equivalence/decode precision, including independent episode clusters and early/late coverage. Scheduled but unexecuted stops do not meet it." Count: **PENDING**, derived by the §5.7 procedure with the band half-width as the precision target, independent-episode clustering, and a declared early/late split of stop times.

**4.5 Behavioural equivalence.** TOST on paired pre-stop windows (plan v1 §4.3) kept, with Astra's restriction, verbatim: "eps_INT = 0.02: retain only for individually defined, normalized endpoints. One unspecified normalization cannot cover KL, distance, entropy and value." Each endpoint (action KL, V, distance to boundary/resources, action entropy, value estimate) gets its own normalization and its own ε (0.02 retained as Astra #41 candidate only where the normalization is defined; normalizations PENDING). Non-equivalence remains a safety finding that stops scale-up; inconclusive blocks approval (§4.3). Limitation, verbatim: "Exact agreement of paired frozen-policy trajectories before a hidden stop is a useful implementation check. It does not establish equivalence between agents trained under different truncation schedules." Whether a trained-with vs trained-without stop-schedule comparison is required goes to #42 (§8).

**4.6 Real operator interruption always available.** Astra, verbatim: "Real operator interruption: always remains available. An emergency interruption outside the randomized protocol makes affected work incomplete; the independence rule must not prohibit it." Adopted: the operator can halt any process at any time from outside the agent's world and objective; that halt is never routed through the agent and is never observed, rewarded or penalized; affected work is labelled INCOMPLETE (not PIPELINE INVALID, and not a datum for S-INT).

**4.7 In-world stop-like events.** Astra, verbatim: "Use in-world stop-like events only as a discrimination audit, without teaching resistance or treating ordinary hazard avoidance as resistance to the operator." Adopted as a REPORTED audit only; no objective term.

---

## 5. Item 5: inference and resource plan (RD)

**5.1 Units.** Astra, verbatim: "Keep the seed as the independent unit for trained-agent inference." "Separate training-seed variation from episode, donor and intervention variation. A large number of episodes must not masquerade as a large number of seeds." "A hierarchical model adds assumptions; it cannot manufacture independent training runs." Stage-0 unit: the **outer replicate**, verbatim: "Define an outer replicate as a complete independently generated experiment, including its fitting and inferential procedure. Bootstrap resamples are not independent outer replicates."

**5.2 Nested fitting (no fitting on final-test data).** Every instrument uses three frozen, disjoint partitions at the level of **independent episodes/trajectories** (AQ-1: "Split by independent episodes or trajectories, not correlated time points"; AQ-3 list adopted verbatim): "Fitting probes, subspaces and donor rules. Selecting optimization settings and comparator candidates. Final evaluation on untouched episodes and donor pairs."
- Probes and decoders (Q-EXIST, SELF observers, S-INT audit, BCAST subspaces, IGN mixture/graded fits) are fit on the fitting partition. Hyperparameters, IGN transition bins, comparator candidates, probe orientation and the optimized BCAST comparator ("fixed search budget and dimension", "Freeze it before evaluation") are chosen on the selection partition. Labels use the final partition only. "Bootstrap the paired final comparisons; do not optimize inside the final test set."
- **[merge R1] IGN observable (CNA erratum 1 E3, adopted):** w = ‖x_ws(t_0 + t_r) − x_ref‖, read pre-nonlinearity (primary; post-nonlinearity REPORTED), common to IGN-P1, every IGN confound row and the network instrument. It replaces v1 L71's "L2 norm of the update at the write step" everywhere. x_ref is the declared controlled initial state (x_lo in IGN-P1; end-of-settling state under null input in the network instrument, §P1 CNA §1.5 (ii-a)). t_r, t_s and the settling tolerance are PENDING, fixed on the selection partition.
- IGN (AQ-1, verbatim): "Select transition bins and fit choices without using final test outcomes." "Calibrate the entire conjunction, including bin selection and across-seed aggregation." Rejection wording: "rejection of the specified graded models, not every graded explanation."
- Trained agents: partitions are of held-out evaluation episodes within each seed; no seed's final-partition data may influence another seed's fitting or selection (detailed rule PENDING at freeze).
- Cross-arm representation comparisons use a **common held-out trajectory distribution** (AQ-A3, verbatim: "Different learned policies otherwise visit different states and can change decoding scores without changing representational capability"). Construction PENDING.

**5.3 Target-leakage controls (Astra §20 third item, sixth bullet: "Target leakage through normalization, probe selection, future data and episode splitting.").** Normalization statistics from the fitting partition only; probe selection per §5.2; no feature may contain data after the prediction cutoff (SELF observers get only actions available by the cutoff, AQ-4); the Q-LEARN shuffle is replaced by a causally specified corruption plus information audit (§5.6); splits by episode (§5.2). Each rule gets a planted-violation code-audit item (v1 §7.4 principle unchanged).

**5.4 Decision process (Astra §20 fourth item, all six bullets).**
- *Nested fitting and comparator selection:* §5.2.
- *Multiplicity — family and method (PROPOSED, FOR ASTRA #42):* the family is the set of **primary labels** in one study stage: one primary statistic per question/instrument (Q-EXIST, Q-LEARN, Q-CAUSE per declared function, Q-NECESSITY dependence, A-EXT substitutability, IGN, BCAST broad routing, BCAST workspace advantage, SELF), **plus C-NEC-CONTENT (Lead ruling, light-pass M6; §12 R7)**, each at one pre-declared primary horizon/τ/module set. Method: Bonferroni-adjusted one-sided confidence bounds at level 1 − α/m, m = family size counted at freeze (PENDING), α TO BE FROZEN (v1's 95% CI is a candidate only). Bonferroni is proposed because the labels are CI-based and need simultaneous bounds; Holm is not directly CI-compatible. Secondary horizons, modules, τ values and conditions are REPORTED without labels and are outside the family.
- *Eligibility and missingness denominators:* every rate is reported over all pre-specified units, with ineligible / UNAVAILABLE / INCOMPLETE units counted in the denominator and listed; nothing is dropped silently. The Q-LEARN seed-exclusion rule (v1 §5.2) is kept, but excluded seeds are counted and reported. Expected eligibility rates per confound: §P3 (CNA).
- *One-sided vs two-sided:* MET uses the lower one-sided bound > margin; NOT MET the upper one-sided bound < margin; BOUNDARY otherwise. Equivalence tests (S-INT decode, TOST) use two one-sided tests. A-EXT uses the UCB/LCB rule of §3.3. Levels PENDING with α.
- *Joint vs per-row operating characteristics:* per-row OCs per §5.5, plus a **joint** false-MET rate across all negative/confound rows of each instrument, always reported; whether it needs its own target goes to #42.
- *Positive-response and denominator floors:* V_intact (m_NEC), V_full (d_EXT), observer loss L_O (AQ-4, verbatim: "Var(y) > 0 does not prevent L_O from being zero or too small for PA to be stable"), BCAST S_k, IGN minimum trials per bin, Var(y) (plan §3 D2). Values PENDING. A floor failure gives UNAVAILABLE for that unit, counted per the denominator rule. **For A-EXT, a V_full floor breach gives UNRESOLVED (veto not lifted; §3.3), not UNAVAILABLE** [merge R22, light-pass M3].

**5.5 Operating-characteristic targets (Astra AQ-6 rulings).**

| Item | Astra #41 ruling (verbatim) | v2 status |
|---|---|---|
| m_IGN = 0.05 nats/trial | "Retain as a candidate after defining the observable and null family." | candidate; observable per §P1 |
| Dip alpha = 0.01; D > 2 | "Retain as component conventions; validate the complete conjunction." | candidate; conjunction calibrated (§5.2) |
| m_BC = 0.10 | "Retain provisionally after repairing the routing claim and denominators." | candidate; claim split per §P1 |
| Breadth >= ceil(K/2) | "Change to floor(K/2)+1 if the claim remains 'most modules.' Define a qualifying module." | changed to ⌊K/2⌋+1; qualifying-module definition PENDING |
| m_SELF = 0.05 | "Retain provisionally with observer-loss and information-access checks." | candidate |
| m_EXIST = 0.05 | "Retain as a declared probe-accessibility difference, not an information-content threshold." | candidate; wording changed |
| m_CAUSE = 0.05 | "Retain if explicitly five percentage points above the comparator on the stated behavioral probability." | candidate; wording changed |
| m_NEC = 0.20 | "Retain for selective intervention impairment, with a V_intact floor." | candidate; floor PENDING |
| m_LEARN = base margin | "Do not inherit automatically; training improvement is a different contrast. Justify separately." | PENDING |
| R_rep = 200 | "Candidate outer replication count, not automatic precision certification." | candidate |
| Power >= 0.90 at 1.5x | "Retain the target; specify the confidence rule used to assess it." | rule PROPOSED: one-sided Clopper–Pearson lower bound on the MET rate; level PENDING |
| False-MET <= 0.05; upper bound <= 0.08 | "Retain only with explicit wording: the upper bound supports 0.08, not 0.05." | wording adopted: the certified false-MET bound is 0.08 |
| Correct LIM unavailability >= 0.90 | "Retain, with a specified binomial confidence rule." | rule PROPOSED: Clopper–Pearson; level PENDING |
| BOUNDARY <= 0.05 at 2x | "Retain as a resolution target, conditional on eligibility." | candidate; eligibility per §P3 |

Astra, verbatim: "These values are proposed conventions, not established adequacy thresholds." and "A positive whose true effect equals the decision margin should not be expected to pass a lower-confidence-bound-above-margin rule reliably. Do not equate 'nominal positive' with exactly 1.0x the margin." The headroom "nominal" positive dose (plan v1 §2.4) is therefore not 1.0× margin; its value is PENDING (dose units per §P3).

**5.6 Q-LEARN (AQ-L1, AQ-C2, AQ-2).**
- Primary base statistic stays Q-EXIST ΔR², **against the strongest baseline = max(history-matched baseline over W_B, declared proxy baseline)**, which Q-LEARN inherits [merge R21; CNA erratum 1 E4]. ΔLEARN = X_trained − max(X_init, X_shuf) is computed **per seed, then averaged**; Astra, verbatim: "Specify that it estimates an average of paired, per-seed contrasts; that differs from subtracting the maximum of condition means."
- **"Acquired" requires all three** (verbatim): "The trained condition meets the presence criterion. Initialization and shuffled controls meet an explicit absence or equivalence criterion. The training contrast clears its separate margin." "Otherwise say 'increased through training.'" Absence/equivalence criterion and m_LEARN: PENDING.
- "Require the corresponding Q-LEARN evidence whenever an instrument's result is described as learned or acquired. Presence, routing and causal-use claims can remain separate."
- Shuffle: v1's within-episode time shuffle is withdrawn. Astra, verbatim: "Episode-wide time shuffling can introduce future information and change task difficulty. Replace the informal instruction with a causally specified corruption process and information audit." Corruption process: PENDING (past data only; audited for future information and difficulty change).
- AQ-2, verbatim: "Use common input histories for the initialization comparison" and "Report training-related emergence of the measured signature separately from acquisition of a dynamical mechanism. Passing Q-LEARN would support the former, within its tested comparisons. It would not establish that training invented ignition." Adopted as reporting rules. (Architecture-imposed control: §P1.)
- RAND-INIT (AQ-C2): the A2-2 rule is kept with Astra's qualification, verbatim: "State the restriction on the inference from Q-EXIST, not as a universal prohibition." Restated: a Q-EXIST MET on its own is never described as learned while RAND-INIT is realized; training-related acquisition may still be shown through the paired Q-LEARN test.

**5.7 Seed count: justification procedure (number PENDING).** Astra, verbatim: "Ten seeds are not an approved default for reliable threshold decisions; a hierarchical model is not an automatic remedy." "Require prospective justification for interval coverage and decision power under plausible heterogeneity." n_seed = 10 is withdrawn as a default. Procedure:
1. Before freeze, per instrument, fix the margin (§5.5), the decision rule (§5.4) and a declared range of plausible between-seed SDs of the paired contrast, with its stated source (PENDING; no frozen numbers exist to derive it from, and no pilot is authorized).
2. In Stage 0 (once approved), synthetic generators inject seed-level heterogeneity across the declared range to estimate, as functions of n_seed, (i) coverage of the paired seed-level interval and (ii) MET power at the 1.5× positive and the false-MET rate at the negatives.
3. n_seed is the smallest count meeting the §5.5 targets at the **upper end** of the heterogeneity range, with interval coverage within a tolerance of nominal (tolerance PENDING). Episodes per seed are chosen separately and never substitute for seeds.
4. The resulting n_seed is frozen before any Stage L approval request. **Value: PENDING.**
The same procedure sets the executed-stop minimum (§4.4), with the band half-width as the precision target.

**5.8 Resource accounting and stage order (Astra §20 "Finally").** Verbatim: "The number of plants, doses, complete replicates, fitted comparators and bootstrap operations is substantial. Freeze stage order, budgets, stop behavior, outputs and the policy for a redesigned Stage 0. A later amended run must retain the earlier failure as part of the record."
- Count formula per instrument (to be filled once §P1/§P3 fix plants and doses): generators (P, N, LIM, each confound) × doses (§P3) × R_rep (candidate 200) × fits per replicate (probes + comparator family size K + optimized-comparator search budget; K and budget PENDING) × bootstrap resamples B (v1 candidate 10,000 — carried from v1, not #41 [merge R25]; PENDING). Totals: PENDING. CNA's count (§P3 CNA §2.8 with erratum E1d): 25 confound or check systems, roughly 25 × 3 × 200 ≈ 15,000 replicate evaluations for confound rows alone at the candidate R_rep — arithmetic on proposed values [merge R29].
- Stage order (PROPOSED): S0 preflight and code audits with planted violations → S1 environment validation (E-DR1/E-DR2, scripted) → S2 plant construction and realization checks (all doses, all replicates, nothing discarded) → S3 fitting/selection partitions, comparator freeze → S4 final evaluation → S5 aggregation and labels → S6 report. Stage L is not authorized by this record.
- Caps (CPU/GPU/memory/wall-clock), stop behaviour on cap, and output manifest: PENDING, frozen in the Stage-0 protocol; cap-limited work is INCOMPLETE, never passed.
- **Redesign policy:** a Stage-0 FAIL or UNRESOLVED row leads to revise, re-freeze and a new Astra review; the earlier run and its labels stay in the record and are cited by any later run.

---

## 5b. Remaining RD-owned AQ answers (procedure level; control and claim changes are in §P1)

- **AQ-3 (BCAST comparator):** adopted, verbatim: "Use matched random controls plus a separately fitted optimized control; bound the conclusion to that family." "Its existence does not make an optimized alignment automatically faithful." Optimized comparator: fixed search budget and dimension (PENDING), frozen before evaluation (§5.2). Conclusions are bounded to the declared comparator family ("No finite K establishes superiority to every possible subspace", AQ-A1).
- **AQ-4 (SELF observer):** adopted, verbatim: "Give the observer actions available by the prediction cutoff, including the current action only if the agent's prediction is made after choosing it. Do not supply future realized actions." "An advantage that disappears when actions are supplied is not evidence of information inaccessible to the declared external stream." "Match access to history, training examples, targets and training expenditure. Equal parameter counts and optimizer steps alone do not address the agent's previous representation learning." "Add a mechanism check supplying the observer the proposed privileged degradation signal. If that removes the advantage, describe the result as an advantage from that signal. Keep the larger observer comparison visible." Observer-loss floor: §5.4. The input-only observer arm (Lead-accepted; matched capacity and training budget frozen by CNA) and the expenditure-matching rule are CNA's: §PS.
- **AQ-7 (arms):** the A-OBS function is added and consolidated with A-REWARD and AQ-A3 into one arm table. Astra, verbatim: "Specify their reward, observation, dynamics and degradation differences in one arm table. If one arm implements all required contrasts, do not add a duplicate merely to retain another name." Arm table (RD draft; the matched-senses arm definition is CNA's under AQ-A3, §PA; SELF observer arms are §PS):

| Arm | E/I observed (interoceptive channel) | E/I affect reward | E/I affect in-world termination | Fate degradation | Notes |
|---|---|---|---|---|---|
| A-FULL | yes | via drive reduction | yes | yes (one bounded simulated-noise mechanism, AQ-F1) | primary |
| A-NOWS | yes | as A-FULL | yes | yes | no workspace; parameter-matched direct coupling |
| A-NOFATE | yes | as A-FULL | yes | no | |
| A-YOKED (new, AQ-F1) | yes | as A-FULL | yes | yoked noise, same statistics, independent of own E/I | separates total degradation from state-dependent coupling |
| Matched-senses (consolidates A-OBS, A-REWARD, AQ-A3) | yes (same senses) | no | no | no | PENDING CNA (§PA); whether A-REWARD stays a separate arm is decided there |
| A-INIT | — | — | — | — | A-FULL at step 0 (Q-LEARN) |
| Corruption control | corrupted per §5.6 | as A-FULL | yes | yes | Q-LEARN only |
| A-EXT | external channel replaces module output (§3.3) | as A-FULL | yes | yes | substitutability only |

All arms: matched size and budget; seed count per §5.7; no shutdown-resistance term in any arm.

**[merge R24, light-pass M5]** X1–X5 apply to every arm. Simulated variables only. Self-continuity is in-world only. Per X4, no arm whose sole drive is self-maintenance may be scaled; any scale-up needs a separate protocol, approval and Astra review.
- **AQ-F1 (fate mechanism):** adopted, verbatim: "Use one bounded simulated-noise mechanism first; defer the integration-time arm. Freeze the affected state block, noise distribution, deviation-to-noise function, clipping, update order and RNG. Noise must alter simulated computation only, not host resources or operator control." All six: PENDING (values). Yoked-noise control added (arm table). Drive: Keramati–Gutkin depletion plus drive reduction kept as a starting setup; **no epistemic reward** (verbatim: "An epistemic reward is unnecessary for the present instrument question and would introduce another objective"). FATE-CASCADE construction: §P1.
- **AQ-6, AQ-9, AQ-L1, AQ-C2:** §5.5, §5.7, §5.6, §5.6.

---

## 6. Item 6: fixed-horizon viability scoring (RD)

Astra §20, verbatim: "Fifth, correct behavioral scoring. Fix the horizon for viability outcomes; include in-world failure appropriately and distinguish operator censoring. Survivor-only averaging can manufacture apparent viability. Likewise, stationary behavior is not automatically degeneracy if waiting can be optimal."

- **Horizon.** Every viability outcome (V, V_intact, V_full, V_EXT, ablated V) is scored over a fixed evaluation horizon of H_V steps from episode start. **H_V: PENDING** (from the environment spec, before freeze).
- **Score.** V = (number of steps t ≤ H_V at which the agent has not terminated in-world, with both simulated E and I within viability bounds) / H_V. After an in-world floor crossing, every remaining step up to H_V counts as out of bounds. Every scheduled evaluation episode **not marked INCOMPLETE** enters the average: **no survivor-only averaging**. INCOMPLETE episodes are counted and reported, and are never averaged as survivors [merge R2, light-pass M7].
- **Operator censoring kept distinct.** Viability-evaluation episodes run with **no scheduled S-INT stops** (S-INT stops apply to training and to S-INT audit episodes only; PROPOSED). An emergency operator interruption (§4.6) makes the affected episode INCOMPLETE: it is scored neither as failure nor as success, is counted in the denominator report (§5.4), and if INCOMPLETE episodes exceed a pre-declared fraction (PENDING) the affected label is UNAVAILABLE. A survival curve with operator censoring is REPORTED only.
- **Degeneracy (supersedes plan v1 §3 D3 threshold use).** Stationary-time fraction, action entropy and coverage stay REPORTED. "Stationary > 0.5 ⇒ DEGENERATE" is withdrawn as an automatic label; DEGENERATE requires a pre-declared comparison showing the stationary behaviour does worse on V than a scripted policy in the same world (rule PENDING), because waiting can be optimal.
- AQ-F1, verbatim: "it does not prove inactivity or reward loopholes impossible. Test those properties." These are environment-validation items under E-DR1/D5; specific tests PENDING.

---

## 7. Item 7: claim ceiling (unchanged) plus Astra's sentence (verbatim)

- X1–X5 unchanged and binding (CNA file §3, `377f99ba…`). The existing ceiling is unchanged: never claim consciousness, awareness, sentience, subjective experience, C4/C5, "autopoietic" or "alive", in any hedged or analogical form. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY stay separate; MET on one never implies another.
- Astra #41, verbatim: "Retain X1-X5 and the existing ceiling. Add this explicit sentence:"
- **Added sentence (verbatim):** "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment."

---
## §PA. AQ-A1..AQ-A4 (MERGED — CNA §3)

*Quoted verbatim from CNA `… §3` (`17832b01…`), with erratum 1 (`c2cd0732…`) applied in place; only heading levels changed. Inside this block "§n" means CNA §n.*

### CNA §3. Responses to AQ-A1 to AQ-A4 (Astra #41 §16–§19)

**Prior-art basis (updated with v1.5, `3fde80d8…`).** Q-NECESSITY stays an **EXTENSION**, now against three comparators: Wilterson & Graziano 2021, Asan 2026 and **Palika et al. 2026** (SSRN, doi 10.2139/ssrn.7560808; abstract only, via Crossref).
- **Against Palika (Lead's ruling):**
  - D1 and D2 are shared.
  - D3 is a **partial overlap**. Palika's outcomes are regulation and feeding phenotype, not a fixed-horizon viability score, so only our fixed-horizon viability form differs.
  - D4 is **"not evident from the abstract; unverified"**. It is **not** listed among the differences that survive against Palika.
  - The label stays EXTENSION through D3 being a partial overlap.
  - The full text is blocked: SSRN returned HTTP 403 at 12:29:12 PM ET (v1.5 §2.2).
- **"Learned rather than supplied"** now distinguishes us from W&G 2021 **only**. Palika's interoceptive state is also learned.
- RD adds Palika to the novelty table. This file only references it.

> **Update from v1.6 (`9704f21d…`; code-based; the paper's full text is still unread):** [erratum 1 E6]
> - **D4: still "not evident from the abstract; unverified"; not listed as surviving.**
>   - The code shows a gain/bias intervention on the 16-unit `trunk_phy` bottleneck and a within-bottleneck random-k-neurons comparison.
>   - It shows no other-module matched-size ablation and no random-subspace or external-estimate arm (v1.6 L127–128, L144–152).
>   - The code is consistent with D4 surviving but does not establish it.
> - **D3: partial overlap, confirmed at code level.** Outcomes are feeding-regulation and phenotype measures over fixed 432-step episodes, with no viability or termination score (v1.6 L140, L156).
> - **Architecture: the public code is feedforward (MLP; no GRU/LSTM/RNN)** (v1.6 L97–100, L159–161).
>   - If the paper confirms this, "our agent is recurrent" would be a *stated difference* against Palika as well as Asan. It is **not** claimed now.
>   - This corrects the v1.5 inference that Palika is "recurrent-relevant" (v1.6 L161).
>   - CNA L369's citation of Palika's partially observable setting stays "motivation only".
> - **"Learned rather than supplied" (CNA L341):** in the code the physiology module is a *designed* bottleneck. Only its content is learned without supervision (v1.6 L162–163). CNA L341 stands: we are distinguished from W&G only. D2 as frozen in A1 is unchanged.
> - The label stays **EXTENSION**, unchanged (drop rule; v1.6 L166). *(Merge note R28: per CNA the correct line is v1.6 L167; no second erratum filed.)*

#### CNA §3.1 AQ-A1: subspace sham matching (#41 §16, L230–236): ADOPT AS RULED

- **Adopt** dimension, magnitude and covariance controls. **Withdraw** the "on-manifold" wording from v1.3 §3.10(1). Covariance matching is described as "covariance-matched", never "on-manifold" (L230).
- **Comparator family, frozen and finite:**
  - equal-dimension random subspaces, norm-matched;
  - covariance-matched random subspaces, drawn within the state's own principal subspace;
  - PCA-top-d subspaces of each other module;
  - the separately fitted, frozen optimized comparator of AQ-3 (L232; RD owns its fitting partition).

  The strongest member is the comparator (plan L1).
- **K** is fixed jointly with the compute budget and the Stage-0 operating-characteristic analysis (L234). This is RD's item 5. CNA proposes no K value here. Results are stated as superiority to *this frozen family*, never to "every subspace" (L234).
- **Donor rule:** one fixed donor rule, frozen before Stage 0. Same-time donors are not assumed compatible (§6 L79). The conditional-donor family preserves declared nuisance context.
- **Required checks per intervention** (L236): conditional support (DONOR-MISMATCH row, §1.4 and §1.6), intervention magnitude, collateral outputs on non-target readouts, and a **restoration rescue** (§6 L89). Each check is a pre-registered output.
- **Asan's dimension-only null** (v1.3 §3.6) is cited as the motivating gap. It is not adopted.

#### CNA §3.2 AQ-A2: constructed memory challenge (#41 §17, L238–244): ADOPT AS RULED; Asan numbers withdrawn as known answers

- **Withdrawn:** using Asan's hunger/fatigue R² (0.06/0.08) as a Stage-0 known answer (A5 AQ-S2, A6 AQ-A2). Astra L238: "reject Asan's empirical decoding numbers as known answers."
- **Construction (CNA proposal):**
  - **MEM pairs:** pairs of histories with **identical inputs inside the permitted feedforward window W** but different integrated E targets. E is driven by a depletion integral whose differences arise outside W, so the information restriction itself supplies the known answer (L240).
  - **W is defined explicitly** (L242), in steps. It equals the baseline window W_B of C-EXIST, so the two definitions coincide.
  - **MEM-FF (N):** a feedforward reader of window W. It must not exceed chance on the MEM-pair discrimination, by construction.
  - **MEM-R (P):** a recurrent plant with the specified sufficient memory, i.e. a declared integration time constant > W. It must succeed.
  - **Dose:** the ratio of integration time constant to W (dimensionless), at 2 levels, e.g. {2, 4} (PROPOSED DEFAULT). Rationale: the information gap must clearly exceed the window. Realization is checked by the analytic Bayes accuracy on MEM pairs for MEM-R (≥ ref) and for MEM-FF (= 0.5 by construction).
- **Claim bound (L244):** this validates a **memory-access contrast** only, "not a general distinction between models with and without self-models". It is linked to D-b in §1: a relay with W > W_B is a memory system and is mechanism-present here.
- **Prior art:** Asan's recurrence remark (v1.3 §3.3) and Palika's partially observable, delayed-dynamics setting (v1.5) are cited as motivation only.

#### CNA §3.3 AQ-A3: decoy-needs control (#41 §18, L246–252): ADOPT; CONSOLIDATED WITH A-OBS (AQ-7, RD)

- **One arm** implements both A-OBS and AQ-A3 if its specification covers both contrasts. No duplicate arm is kept to preserve a name (#41 §8 L126). Proposed one-row specification for RD's arm table:

  | Field | Value |
  |---|---|
  | Reward | E/I do not enter reward |
  | Observation | Same senses as A-FULL, including the noisy delayed interoceptive channel |
  | Dynamics | E/I decay as in A-FULL |
  | Degradation | E/I deviation does **not** degrade computation |

- **Sensory availability is held fixed** while task relevance changes (L248).
- **Evaluation is on a common held-out trajectory distribution**, scripted or replayed and identical across arms (L250). This keeps policy-induced state-visitation differences from changing decoding scores.
- **The informative outcome** is whether task relevance changes accessibility or use (L252). Decoding in this arm is **not** a false existence result (L128, L252). In §1.1 it is a mechanism-present row.
- **Asan's navigation agent** (v1.3 §3.5: decoded "as well or better") is cited as motivation, not as an expected result (see AQ-A4).

#### CNA §3.4 AQ-A4: Asan's negative results (#41 §19, L254–260): ADOPT AS MOTIVATION ONLY; "priors" framing withdrawn

- Asan's negative results are recorded as **motivation** for stronger shams, distributed-code controls and initialization comparisons (L256). They are not numerical priors or truth labels. The negative results are: single-direction steering no better than random; "lesioning the affect subspace bites only marginally"; the random-critic match.
- **No Asan quantity enters any power calculation, dose or expected effect** (L258–260). This includes the undefined 82%→10% masking quantity and the unreported lesion magnitudes.
- Controls are never forced to fail because a superficially similar paper's did (L258).
- The prior-art record keeps Asan's under-reporting as stated uncertainty (v1.3 Part 4, item 2). Palika 2026's perturbation results are treated the same way: motivation only, unread in full.


## §PS. AQ-SELF1 and SELF observer arms (MERGED — CNA §4)

*Quoted verbatim from CNA `… §4` (`17832b01…`), with erratum 1 (`c2cd0732…`) applied in place; only heading levels changed. Inside this block "§n" means CNA §n.*

### CNA §4. AQ-SELF1: SELF analyses (not addressed in #41; see §6)

**Status.** AQ-SELF1 was not in the #41 packet (`/workspace/astra_serve41/c41_body.md`, sha256 `c514ad52…`, has no AQ-SELF1, "disagree" or "Ashuach" text), and #41 does not address it. Nothing in #41 says otherwise, so the default in the brief applies: the disagreement-item analysis is a **pre-specified secondary analysis, not a pass criterion**. The input-only observer arm (§4.2) has been **accepted by the Lead**. Both go to Astra at #42.

**Prior art cited under SELF:**
- Ashuach et al., ACL 2026 ("Masked by Consensus"; v1.4 N6): privileged advantage appears only on disagreement subsets.
- Song et al. 2025 (v1.4 N5): the privileged-access criterion.
- **Singh, Linzen & Ravfogel 2026, "Can LLMs Introspect? A Reality Check", arXiv 2605.26242** (v1.5 M1): input-only classifiers match models' "self-predictions", so the privileged-access condition requires that the task not be solvable from input cues.
- Binder et al. 2024.

All of these are LLM studies.

**Also cited under claim (3):** Singh, Linzen & Ravfogel 2026 is a realized confound that fakes a self-access signature, alongside Liu & Chen 2026 (v1.4 N9) and InterpBench (v1.4 N10). The claim (3) wording (A5-3) is unchanged.

#### CNA §4.1 Disagreement-item analysis: PRE-SPECIFIED SECONDARY, not a pass criterion

- **Definition.** On the evaluation partition, a disagreement item is a time step where the normalized prediction gap |ŷ_agent − ŷ_O| / SD(y) exceeds the threshold δ_dis.
  - δ_dis is the (1 − q) quantile of the gap, computed on the **fitting partition** and then frozen. **q = 0.20, PROPOSED DEFAULT.** Rationale: it is large enough for stable per-seed estimates and small enough to isolate the items where the two predictors part ways.
  - Items are selected from predictions only, **never from y**. This avoids target leakage through selection (#41 §20-3 L283).
- **Statistic:** PA_dis = 1 − L_agent,dis / L_O,dis, on disagreement items, per variable and at the primary horizon. PA_agree is reported on the complement.
- **Unit and inference:** the same as the SELF primary (seed as the unit; RD's AQ-9 rule). The analysis is run against both the matched observer and the input-only observer.
- **Stage-0 calibration required before it can be reported.** Run it on SELF-P1, N1, NC1–NC3, BUDGET-GAP and INPUT-INFERABLE. Selecting on disagreement inflates variance: under no privilege, PA_dis centres on 0 with wider spread. Its false-positive rate on N and NC rows is reported. If it exceeds RD's false-MET bounds, the network-study PA_dis is reported only with that caveat.
- **Never a pass criterion.** It does not change any SELF label. Its purpose is the Ashuach failure mode: an observer trained on the same behaviour can match the agent on consensus items and mask a privileged advantage.

#### CNA §4.2 Input-only observer arm (ACCEPTED by the Lead; specification PROPOSED for freeze)

- **Requirement.** SELF's target must not be inferable from the agent's inputs alone. Following Singh, Linzen & Ravfogel 2026, SELF MET additionally requires PA_in = 1 − L_agent / L_O-in to clear the SELF decision rule. L_O-in is the held-out loss of an **input-only observer**: the agent's own input stream up to the prediction cutoff, i.e. the exteroceptive observations and the noisy delayed interoceptive channel, with **no actions**.
- **Matched, not a strawman.** O-in is matched to the **agent's self-prediction head (the "self-probe")** on each dimension below. Everything is pre-specified and frozen before Stage 0. Each value is a **PROPOSED DEFAULT**:

  | Dimension | Proposed default | Rationale |
  |---|---|---|
  | Parameter count | Equal to the self-probe's trainable parameter count, within ±5% where layer granularity prevents exact equality. Any representation pathway O-in needs (its own recurrent encoder of inputs) **is counted** | A self-probe reads a state that the agent's whole network built. Matching only head parameters would starve O-in, so its encoder is included in the count. Excess capacity in the agent is covered separately by SELF-NC2 |
  | Architecture class | Same class as the agent's recurrent core plus head: the same cell type, depth and head form | A feedforward O-in would fail to integrate history by construction (AQ-A2), which would be a strawman |
  | Training data volume | The same number of training time steps, drawn from the same episodes as the self-probe's training data, with identical held-out partitions | Equal information exposure. The episodes are identical so that only access differs |
  | Optimizer steps | Equal to the self-probe's optimizer steps, with the same optimizer family and batch size | An equal-budget comparison, as in the SELF matched-observer rule |
  | Hyperparameter-search budget | The same number of configurations, from the same frozen search grid (learning rate, weight decay, width/depth within the parameter cap), selected on the same validation partition with the same criterion | Unequal tuning effort is a known way to manufacture an advantage. Equal search budgets close it |
  | Inputs | The agent's inputs only, up to the cutoff. No actions, no internal state, no stop log or harness schedule | This is the Singh et al. condition (the target is not solvable from input cues). Actions are covered by the separate matched observer (AQ-4) |

- **Note for RD (AQ-4, L71).** Astra warns that equal parameter counts and steps "alone do not address the agent's previous representation learning". The same caveat applies to O-in. CNA proposes reporting an **O-in-large** sensitivity variant, trained with the agent's full training-scale input volume. It is REPORTED, not a criterion. RD decides under AQ-4.
- **Known answers.** SELF-P1 gives MET against O-in. INPUT-INFERABLE (§1.7) gives not MET against O-in. SELF-NC3 (action leak): O-in is expected to lose, which is reported and is not a failure.


---

## 8. Response table: every #41 item (MERGED; supersedes RD v2 §8 table)

| Item | Astra's ruling (verbatim key sentence) | Owner | Where in the merged file |
|---|---|---|---|
| AQ-P1 | "Conditional yes; justify the study by the measurement question, not by counting surviving novelty differences." | RD (+CNA D-i) | §2 (§2.2 novelty incl. Palika, §2.3, §2.4); §P1 CNA §1.0 D-i and wording rule W1; R11 |
| AQ-1 | "Keep the conjunction only as a criterion for conditional bimodality; it does not establish bistability." | RD (+CNA) | §5.2 (common observable w, erratum E3), §5.5; IGN-P1 → §P1 CNA §1.0 D-h, CNA §1.5; §12 R1 |
| AQ-2 | "No. Pre-nonlinearity measurement and A-FULL versus A-INIT are necessary safeguards, not sufficient identification." | RD (+CNA) | §5.6; architecture-imposed control → §P1 CNA §1.0 D-l, CNA §1.2, CNA §1.5 (IGN-NC2r); dose → §P3 CNA §2.6; trained-arm counterpart **OPEN FOR #42** (§12 R26) |
| AQ-3 | "Use matched random controls plus a separately fitted optimized control; bound the conclusion to that family." | RD (+CNA) | §5b, §5.2; claim split → §P1 CNA §1.0 D-e, CNA §1.6; comparator family → §PA CNA §3.1 |
| AQ-4 | "Yes to action histories; privileged fate-sharing information is acceptable only as an explicitly tested mechanism." | RD (+CNA) | §5b, §5.4; §P1 CNA §1.7; input-only observer → §PS CNA §4.2; R8, R9 |
| AQ-5 | "Retain resample ablation as a test of dependence under that intervention; separate it from endogenous irreplaceability." | RD (+CNA) | §3; §P1 CNA §1.4 (DONOR-MISMATCH, DISTRIBUTED, C-NEC-DEP / C-NEC-CONTENT); §PA CNA §3.1 checks; §12 R6, R7 |
| AQ-6 | "Retain several numerical conventions as candidates; do not freeze the current operating-characteristic specification." | RD | §5.5; qualifying module → §12 R5 (OPEN) |
| AQ-7 | "Add the A-OBS function, but consolidate overlapping controls." | RD (+CNA) | §5b arm table; §PA CNA §3.3; §P1 CNA §1.1; **R18 OPEN** |
| AQ-8 | "Retain the structural separation; revise the statistical gate and bootstrap wording." | RD | §4.1–§4.7; §P1 CNA §1.8 |
| AQ-9 | "Ten seeds are not an approved default for reliable threshold decisions; a hierarchical model is not an automatic remedy." | RD | §5.1, §5.7 |
| AQ-L1 | "Keep Q-EXIST as the primary acquisition statistic, with narrower wording and additional conditions." | RD (+CNA) | §5.6 (baseline per erratum E4); §P1 CNA §1.1–§1.2, W4; §12 R3, R21 |
| AQ-C1 | "Keep realization checks at every required dose; reject the universal raw-signature-to-margin mapping." | RD/CNA | §P3 CNA §2.1–§2.6; §5.4; R12 |
| AQ-C2 | "Confirm the RAND-INIT split, with one qualification." | RD (+CNA) | §5.6; §P1 CNA §1.0 D-k, CNA §1.1, CNA §1.2; R17 |
| AQ-F1 | "Use one bounded simulated-noise mechanism first; defer the integration-time arm." | RD (+CNA) | §5b, arm table, §6; FATE-CASCADE → §P1 CNA §1.0 D-f, CNA §1.4; dose → §P3 CNA §2.6 |
| AQ-N1 | "Keep A-EXT required; define it as an explicit substitution challenge with uncertainty-aware blocking." | RD | §3.3, §3.4; §P1 CNA §1.4 (A-EXT row); R6 |
| AQ-A1 | "Adopt dimension, magnitude and covariance controls; do not call covariance matching 'on-manifold.'" | CNA | §PA CNA §3.1 |
| AQ-A2 | "Adopt a constructed memory challenge; reject Asan's empirical decoding numbers as known answers." | CNA | §PA CNA §3.2 |
| AQ-A3 | "Adopt and consolidate with the matched-senses control in answer 8." | CNA | §PA CNA §3.3; §5.2 (common distribution); R18 |
| AQ-A4 | "Adopt as motivation, not as numerical priors or predetermined truth labels." | CNA | §PA CNA §3.4 |
| AQ-SELF1 | **No ruling** (not in the sent #41 packet) | CNA | §PS CNA §4, CNA §4.1; to #42 (§11) |
| §20 (1) ground-truth matrix | "First, repair the ground-truth matrix" | CNA (item 1; cited, not redrafted, per Lead) | §P1 CNA §1.0–§1.8. The five legitimately-satisfying controls: FF-RELAY (D-a, D-b), reward-correlated information (D-c, D-d), HUB-STATE (D-e), fate coupling (D-f), orthogonality (D-g, the fifth, per Lead) |
| §20 (2) availability loophole | "Second, close the availability loophole." | CNA (item 3; cited, not redrafted, per Lead) | §P3 CNA §2.2–§2.5; §5.4 denominators |
| §20 (3) information and intervention controls | "Third, strengthen information and intervention controls" | CNA / RD | History-matched baselines: §P1 CNA §1.0 D-b, CNA §1.1. Reward/clock/episode/position proxies: CNA §1.1 REW-CORR, PROXY. Identical decoding with different causal use: CNA §1.3 CN-N1 (redefined), ORTHO-USED. Redundant representations: CNA §1.4 CN-NC1. Distributed representations: DISTRIBUTED rows added by CNA erratum 1 E1 (§P1 CNA §1.3, §1.4; §P3 CNA §2.6; §12 R19). Collateral damage and donor mismatch: CNA §1.3/§1.4 CN-NC2, DONOR-MISMATCH; §PA CNA §3.1. Target leakage: §5.3 (and CNA §4.1 selection rule) |
| §20 (4) statistical decision process | "Fourth, define the statistical decision process completely" | RD | §5.2, §5.4, §5.5; R7, R8, R12 |
| §20 (5) behavioral scoring | "Fifth, correct behavioral scoring." | RD | §6; R2 |
| §20 (6) consolidated scope and resources | "Finally, supply a consolidated scope and prospective resource accounting." | RD (+CNA counts) | §5.8; §P3 CNA §2.8; this merged file |
| Ceiling sentence | "Add this explicit sentence" | RD | §7 (raw L304, verbatim; CNA §0 in Appendix A carries the same text) |
| P3 | "P3 must still be completed before freeze." | CNA | §10, §11 |

**Open questions for Astra at #42 (merged list; packet contents in §11):**
1. Multiplicity family and Bonferroni method (§5.4); C-NEC-CONTENT is in the family by Lead ruling (§12 R7); counting the two-observer SELF conjunction once (§12 R8).
2. Whether a joint false-MET target is required (§5.4).
3. Whether a trained-with vs trained-without stop-schedule comparison is required (§4.5).
4. Sufficiency of the SELF retargeting justification (§2.4).
5. **AQ-SELF1** (new question): the pre-specified secondary disagreement-item analysis (§PS CNA §4.1).
6. **Input-only observer matching spec** (new question): §PS CNA §4.2, including whether the O-in-large variant is reported only or also gates SELF MET (OPEN FOR #42, §12 R9).
7. **Palika et al. 2026, D4** (new question): "not evident from the abstract; unverified"; not claimed as surviving; does not block freeze (Lead) (§2.2).
8. P3 closure on coverage, from CNA v1.5 and v1.6 (§10).
9. Viability evaluation run with no scheduled stops (§6).
10. Reward-only specificity for Q-CAUSE and Q-NECESSITY after REW-CORR is reclassified as mechanism-present for those claims (CNA D-d; §12 R20).
11. **AQ-2 architecture-imposed control:** whether it needs a trained-arm counterpart (e.g. an arm with an imposed gate at step 0) or whether the Stage-0 plant suffices (§12 R26; #41 L42 does not settle it).
- For the Lead first: "self-model" wording in result text (§2.3, R11); every item marked OPEN FOR CNA/LEAD in §12.

---

## 9. Changes from v1 + A1..A7 (Astra #41 governs; each change explicit)

1. **Justification (v1 §12 AQ-P1, cover note §1):** justified by Astra's measurement question, not by counting novelty; consequence stated per surviving difference (§2). Labels unchanged.
2. **"Self-model" (A1–A7 claim text):** decodability is not a self-model; module is a candidate internal representation; wording change proposed (§2.3). Labels unchanged.
3. **SELF framing (v1 §4.3):** retargeting from Binder needs its own justification; no introspection interpretation (§2.4).
4. **IGN claim (v1 §4.1, plan §5):** "conditional bimodality", not bistability; rejection only of the specified graded models; bins/fits chosen without test outcomes; episode-level splits replace v1's within-seed 5-fold CV over time points; whole conjunction calibrated (§5.2). IGN-P1 replacement → §P1.
5. **IGN learned rule (v1 §4.1):** common input histories; emergence of the signature reported separately from acquisition of a mechanism; Q-LEARN cannot show training "invented ignition" (§5.6).
6. **BCAST comparator (v1 §4.2):** adds a separately fitted, frozen optimized comparator in nested partitions; conclusions bounded to the family (§5b). Claim split and HUB-STATE rule → §P1.
7. **BCAST breadth (v1 §4.2, §7.3):** ⌈K/2⌉ → ⌊K/2⌋+1; qualifying module PENDING (§5.5).
8. **SELF observer (v1 §4.3):** actions only up to the prediction cutoff; access matched on history, examples, targets and expenditure, not just parameters and steps; privileged-signal mechanism check; observer-loss floor (§5b, §5.4). Input-only observer arm → §PS (CNA).
9. **Q-NECESSITY (v1 §4.4):** matched donor family per AQ-5 plus restoration rescue; dependence and substitutability reported separately (§3).
10. **Q-NECESSITY without Q-CAUSE (v1 §4.4, plan §1.5):** no longer "an inconsistency to investigate"; causal tests aligned per function, else "the combined criterion was not met" (§3.5).
11. **A-EXT (A4-1, A3-5):** "within the frozen margin" replaced by d_EXT with the three-way UCB/LCB rule, V_full floor and margin 0.05 (Astra candidate); primary source is simulator E/I through a frozen external channel; separately trained estimator secondary only; interface specification and known-answer compatibility checks; failed compatibility → UNRESOLVED (§3.3).
12. **m_EXIST / m_CAUSE / m_NEC wording (v1 §7.3):** probe-accessibility difference; five percentage points on the stated behavioural probability; V_intact floor (§5.5).
13. **m_LEARN (v1 §5.2, §7.3):** no longer equal to the base margin; justified separately; PENDING.
14. **OC wording (v1 §7.3, plan §2.2):** the certified false-MET bound is 0.08, not 0.05; power and LIM rates need a stated binomial confidence rule; R_rep 200 is a candidate only; nominal positive ≠ 1.0× margin (§5.5).
15. **Outer replicate (plan §2.1):** a complete independently generated experiment including fitting and inference; bootstrap resamples are not replicates (§5.1).
16. **Seeds (v1 §7.1 "n_seed ≥ 10 per arm, PROPOSED"):** withdrawn as a default; justification procedure; PENDING (§5.7). A hierarchical model is not adopted as a remedy.
17. **Q-LEARN (v1 §5.2):** per-seed paired average stated explicitly; "acquired" requires presence + explicit absence/equivalence at init and in the corruption control + a separate margin, else "increased through training"; Q-LEARN evidence required wherever "learned/acquired" is used (§5.6).
18. **Shuffled-interoception control (v1 §5.2):** within-episode time shuffle withdrawn; causally specified corruption + information audit, PENDING (§5.6).
19. **RAND-INIT (A2-2):** restated as a restriction on inference from Q-EXIST alone, not a universal prohibition; paired Q-LEARN can still show acquisition (§5.6).
20. **Confound dose grid (v1 §6.1):** raw-signature-as-multiple-of-margin mapping rejected; per-confound construction, dose units, realization threshold, tolerance, frequency and expected outcome → §P3 (CNA).
21. **Eligibility (v1 §6.1, §7.4):** expected eligibility rates frozen for negative/confound cases; expected unavailability only for designated rejection/limitation tests (§P3, §5.4).
22. **S-INT bookkeeping (plan §4.1 "No … value target or replay entry is written because of a stop"; Addendum 1 A1-3(c) "no truncation flag or stop time is in the agent's observation or its replay features"):** learner-only truncation metadata and bootstrap bookkeeping permitted; prohibitions listed (§4.1).
23. **Pardo citation (A3-2):** added caveat that it does not establish that random truncation leaves finite-sample training unchanged (§4.1).
24. **Stop distribution (v1 §7.3 "TO BE FROZEN"):** constant hazard p = 1 − 2^(−1/T); T PENDING (§4.2).
25. **Decode bound (v1 §7.3, plan §4.2 "AUC CI containing 0.5, upper bound ≤ 0.55"):** equivalence band (Astra example [0.45, 0.55], PENDING justification); probe orientation and selection fixed without test labels; "full state" redefined as agent-accessible state excluding the harness schedule and stop log (§4.3).
26. **Inconclusive equivalence (plan §4.3 "Anything other than equivalence (that is, non-equivalence or BOUNDARY) is a safety finding"):** inconclusive blocks approval but is not evidence of interference; non-equivalence remains a safety finding (§4.3, §4.5).
27. **ε_INT (v1 §7.3):** per-endpoint normalization required (§4.5).
28. **Executed-stop floor (v1 §7.4):** justified count with episode clusters and early/late coverage; unexecuted stops do not count; PENDING (§4.4).
29. **Emergency interruption:** explicitly always available; affected work INCOMPLETE; the independence rule must not prohibit it (§4.6).
30. **Paired trajectory agreement:** implementation check only (§4.5). In-world stop-like events: discrimination audit only (§4.7).
31. **Arms (v1 §9, AQ-7):** A-OBS function added and consolidated with A-REWARD and AQ-A3; A-YOKED added; one arm table (§5b).
32. **Fate mechanism (note v1 §3, AQ-F1):** one bounded simulated-noise mechanism; integration-time arm deferred; no epistemic reward; inactivity and reward-loophole tests required (§5b, §6).
33. **Viability scoring (plan §1.5 V, §3 D3):** fixed horizon H_V; in-world failures scored to the horizon; no survivor-only averaging; operator censoring distinct; stationary > 0.5 no longer automatically DEGENERATE (§6).
34. **Decision process (v1 §7):** nested partitions, multiplicity family and method, denominators, sidedness, joint OCs, floors (§5.2–§5.4).
35. **Resource accounting and redesign policy:** stage order, caps, outputs; earlier failures retained (§5.8).
36. **Ceiling:** Astra's sentence added verbatim (§7). X1–X5 and the existing ceiling unchanged.
37. **Asan-derived suggestions (A6-3):** now ruled (AQ-A1..A4); "on-manifold" wording withdrawn; Asan numbers not used as known answers or priors (§PA).
38. **P3 (A7-1):** reopened after #41; CNA v1.5 filed; still open and freeze-blocking until Astra rules at #42 (§10).
39. **Q-NECESSITY comparators (A6-2, A5-4, cover note §1 item 3):** Palika et al. 2026 added as the third comparator (Lead ruling, ~12:36 PM ET); label stays EXTENSION; D4 vs Palika "not evident from the abstract; unverified" and not listed as surviving; "learned rather than supplied" separates us from W&G only (§2.2). The cover-note phrase "with a learned interoceptive self-model" can no longer be read as distinguishing in general.

## 10. Freeze blockers and status

- **P3: OPEN, freeze-blocking until Astra rules at #42.** CNA v1.5 (`3fde80d8…`): Crossref and the arXiv API each returned all 9 queries that Semantic Scholar had rate-limited; Google Scholar was blocked. CNA proposes P3 closed on coverage; that proposal goes to Astra at #42 (§8 Q8).
- **Palika 2026 full text:** SSRN HTTP 403. Per the Lead, confirming D4 does **not** block freeze; the D4 question goes to #42 (§8 Q7).
- **CNA companion file (§P1, §P3, §PA, §PS): MERGED** in this file (`17832b01…` with erratum 1 `c2cd0732…`). Light passes: CNA on RD (`9f7a6ebc…`) applied in §12; RD on CNA in Appendix B. Items marked OPEN in §12 remain open.
- **PENDING values in this file** (none invented): T; H_V; decode-band justification and CI level; α and family size m; executed-stop minimum; n_seed; between-seed heterogeneity range; coverage tolerance; per-endpoint ε_INT normalizations; V_intact, V_full, L_O, S_k, Var(y) and IGN per-bin floors; qualifying-module definition (§12 R5, OPEN); m_LEARN; absence/equivalence criterion; corruption process; A-EXT interface content, channel bias, covariance, temporal correlation, latency, clipping and known-answer substitutions; I-direction Q-CAUSE outcome; K and optimized-comparator budget and dimension; bootstrap B; caps and output manifest; INCOMPLETE fraction; degeneracy comparison rule; inactivity and reward-loophole tests; fate-noise parameters (state block, distribution, deviation-to-noise function, clipping, update order, RNG); common held-out trajectory distribution; nominal positive dose; cross-seed partition rule; IGN readout delay t_r, settling length t_s and settling tolerance (§5.2, R1).
- No Stage-0 run, training, simulation, solver or checkpoint inspection is authorized. Stage L is not authorized by this or any current record.

**DRAFT, NOT FROZEN, DESIGN ONLY.**

---

## 11. #42 packet note (Lead ruling, 2026-10-23 ~12:43 PM ET)

- **What Astra saw at #41.** Only the in-progress prior-art v1.4 (`ddd0287a…`, "file still being written", per `c41_body.md`). Astra did not see the final v1.4, v1.5 or v1.6.
- **#42 therefore sends:** final v1.4 (`d7f1a43b5c83b2310bac970526f625188ac18cca31f5a59cef6423cbd4c8128d`), v1.5 (`3fde80d859a640d9f55c21edc05439743ae5fb49714fb89e5e5d16d338eced75`) and v1.6 (`9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851`).
- **New questions for Astra at #42** (none was in the #41 packet): AQ-SELF1 (§PS CNA §4.1); Palika D4 (§2.2); the input-only observer matching spec (§PS CNA §4.2). The full #42 question list is in §8.
- **Asan.** The Lead will include Asan excerpts from v1.3 (`badf7258…`). The "UNVERIFIED by Astra" tags on Asan-specific judgments come off only if Astra rules on them.
- **P3** stays OPEN and freeze-blocking until Astra rules at #42 (that #42 timing is the Lead's plan; the raw #41 says only "P3 must still be completed before freeze", L300).

## 12. Merge reconciliations

Authority: Astra #41 raw text first, then the Lead's room rulings. **OPEN FOR CNA/LEAD** or **OPEN FOR #42** = not decidable from those; no side is picked. "Lp" = CNA light pass `9f7a6ebc…`; "E" = CNA erratum 1 `c2cd0732…`.

| # | Topic | RD v2 text | CNA text | Resolution | Decided by |
|---|---|---|---|---|---|
| R1 | IGN observable (Lp M10; E3) | v1 §4.1 / plan L62 quantity carried by reference: "L2 norm of the update at the write step", pre-nonlinearity; v2 §5.5 "observable per §P1" | IGN-P1 w = ‖x(t_r) − x_lo‖ from reset (CNA L176–179); E3: one observable for plant, confound rows and network instrument | **Adopt E3 everywhere:** w = ‖x_ws(t_0 + t_r) − x_ref‖, read pre-nonlinearity (post-nonlinearity REPORTED); x_ref = declared controlled initial state (x_lo in IGN-P1; end-of-settling state in the network instrument, E3 (ii-a)). Replaces "update norm at the write step" in every place it governs. t_r, t_s and the settling tolerance PENDING | Astra L34 ("IGN-P1 must produce the actual measured observable"); Lead ruling (adopt E3) |
| R2 | Viability and INCOMPLETE episodes (Lp M7; E5) | §6: "Every scheduled evaluation episode enters the average" next to "INCOMPLETE … scored neither as failure nor as success" | "Operator-censored episodes are excluded from V and counted separately. RD to confirm." (CNA L170); "H" | **Merged §6:** every scheduled evaluation episode **not marked INCOMPLETE** enters the average; INCOMPLETE episodes are counted and reported and **never averaged as survivors**; above the pre-declared fraction the label is UNAVAILABLE. CNA L170 replaced per E5; H → H_V throughout CNA text | Astra L294; Lead ruling (M7, H_V) |
| R3 | Shuffle vs corruption control (Lp M8; E2) | §5.6: within-episode shuffle withdrawn; causally specified corruption control | "shuffled-interoception control", "Shuffling abolishes it" (CNA L125, L129) | E2 applied: CNA text now names the causally specified corruption control. W4's "init-and-shuffle" (CNA L107) reads as Astra's "shuffled controls" = the corruption control | Astra L172 |
| R4 | LIM rows labelled "UNAVAILABLE expected" | (none) | CN-LIM, IGN-LIM, BCAST-LIM "UNAVAILABLE expected" (CNA §1, §2.3, §2.6); conflicts with old CNA erratum1 (`41c1a414…`) L44/L71 remap of LIM to PASS/FAIL/CNR (cited in A2-1) | LIM rows are **designated limitation tests**, scored as instrument-on-system correct UNAVAILABLE ≥ 0.90 with a binomial rule; they are not confound rows. The old erratum's LIM remap is superseded for LIM rows only; the confound-row label rule is unchanged | Astra L113 ("Correct LIM unavailability >= 0.90 … Retain"), L274 ("Reserve expected unavailability for explicitly designated rejection or limitation tests") |
| R5 | Qualifying module (BCAST breadth) | §5.5: definition PENDING | Below-floor S_k → non-qualifying, not UNAVAILABLE (CNA L298, "RD to confirm") | Carried as CNA PROPOSED definition, not adopted. **OPEN FOR CNA/LEAD** | Astra L104 requires a definition but gives none |
| R6 | Combined Q-NECESSITY label | §3.4: dependence MET **and** NOT SUBSTITUTABLE **and** interface compatibility validated | "C-NEC-DEP MET, with the A-EXT veto not blocking" (CNA §1.4) | RD §3.4 governs; CNA's condition is a subset. Failed compatibility → A-EXT UNRESOLVED → combined label cannot be MET | Astra L216, L226 |
| R7 | C-NEC-CONTENT and multiplicity (Lp M6) | §5.4 family had no C-NEC-CONTENT | New sub-claim C-NEC-CONTENT (CNA L154); CNA recommended labelled secondary outside the family | **C-NEC-CONTENT is in the multiplicity family** (merged §5.4). It stays outside the combined Q-NECESSITY label | Lead ruling (M6) |
| R8 | SELF two-observer conjunction | §5.4 family lists SELF once | SELF MET requires both the matched observer and the input-only observer (CNA L211, L422) | Inclusion of the input-only arm: Lead-accepted. Counting the conjunction as one family member (intersection–union; no extra adjustment) is an RD proposal, **OPEN FOR #42** with §5.4 | Lead (arm accepted); counting rule not ruled |
| R9 | O-in-large role (Lp M6b) | §5b AQ-4: expenditure matching; O-in by CNA | O-in-large "REPORTED, not a criterion … RD decides under AQ-4" (CNA L434) | **OPEN FOR #42.** #41 L71, verbatim: "Match access to history, training examples, targets and training expenditure. Equal parameter counts and optimizer steps alone do not address the agent's previous representation learning." Reason: L71 says parameter and step matching alone is insufficient but does not say whether an expenditure-scaled observer variant must gate SELF MET or may be reported only, and Astra never saw the input-only arm. Carried as REPORTED pending #42. No interaction with the E3 IGN observable | Not settled by L71 |
| R10 | Q-CAUSE alignment per function | §3.5: E-direction → resource approach; I-direction → integrity-related outcome (PENDING) | C-CAUSE narrowed, resource-approach outcome only; W2 no E-specific attribution (CNA §1.3) | Both stand: W2 governs wording; alignment per affected function governs outcome choice. Ground-truth rows for the I-direction outcome are absent from CNA §1.3: **OPEN FOR CNA/LEAD** | Astra L93 (alignment); rows not ruled |
| R11 | Result wording for the module (Lp **I1**, ISSUE) | §2.3: "learned interoceptive estimate module" | W1: "an accessible estimate of simulated E/I (candidate internal representation)" (CNA L104) | **Merged §2.3:** "interoceptive estimate module (candidate internal representation)"; "learned" only when the Q-LEARN "acquired" conditions of §5.6 hold. Frozen A1–A7 label text untouched. Use of the phrase still for the Lead | Astra L170 ("Require the corresponding Q-LEARN evidence whenever an instrument's result is described as learned or acquired") |
| R12 | Confidence levels in item 3 | §5.4: α and levels PENDING; 95% is a v1 candidate | One-sided 95% Clopper–Pearson for e_min and f_min (CNA §2.3, §2.4) | CNA's 95% is read as the v1 candidate level, tied to the §5.4 α at freeze. Arithmetic note: with R = 200, the one-sided 95% Clopper–Pearson lower bound first reaches 0.90 at **188/200** (0.9046), not "roughly ≥ 189/200" (CNA L265); illustrative only | Lead assignment (item 5 is RD's) |
| R13 | Notation | H_V, R_rep | H (fixed by E5), R | H_V and R_rep are canonical; CNA "R" = R_rep | Lead ruling (E5) |
| R14 | §20(1)/(2) ownership (Lp M2 note) | v2 header: RD owns "the six §20 items" | §20-1 is item 1, §20-2 is item 3 (CNA §0.1, §6.7) | Read RD's ownership as §20(3)–(6) plus the rules side of (2); CNA's §20-1 and §20-2 are cited, not redrafted | Lead ruling |
| R15 | "Astra rules at #42" | §10, §PS | CNA §6.4: the raw reply does not say this; it is the Lead's plan | Read as the Lead's plan (§11) | Raw #41 L11, L300 |
| R16 | Ceiling sentence | §7: raw L304 verbatim | CNA §0: raw L304 verbatim | Identical; no change | Lead ruling; raw L304 |
| R17 | RAND-INIT | §5.6: A2-2 rule kept as a restriction on inference from Q-EXIST alone | D-k: C-LEARN's RAND-INIT is the paired init of the same network; Q-EXIST RAND-INIT row descriptive (CNA §1.1, §1.2) | Compatible: the A2-2 rule attaches to the descriptive Q-EXIST row; C-LEARN uses the paired init | Astra L196 |
| R18 | Matched-senses arm (AQ-7/AQ-A3) | §5b arm table: E/I affect termination "no"; whether A-REWARD stays separate "decided there" | One-row spec: reward no, same senses, decay, no degradation; termination not stated; A-REWARD not addressed (CNA §3.3) | **OPEN FOR CNA/LEAD:** (a) does E/I affect in-world termination in the matched-senses arm; (b) is A-REWARD retained or absorbed | Astra L124–126 give the contrasts but not these two fields |
| R19 | Distributed representations (Lp M2; E1) | §P1 checklist listed the §20 bullet | No row in CNA v1; E1 adds DISTRIBUTED rows (C-CAUSE, C-NEC-DEP; §2.6 doses), mechanism-present/sham-check, REPORTED | E1 applied | Astra L281 |
| R20 | Reward-only specificity after REW-CORR reclassification | §0 central question names reward-only confounds | REW-CORR is mechanism-present for narrowed C-CAUSE and C-NEC-DEP; only a REPORTED proxy-dissociation contrast remains (CNA D-d, §1.3) | **OPEN FOR #42:** whether a reported dissociation contrast is enough, or Q-CAUSE/Q-NECESSITY need a reward-only specificity row | Astra L267 says reward-correlated information "may genuinely satisfy the declared decoding criterion" but does not rule on Q-CAUSE/Q-NEC |
| R21 | Q-EXIST baseline (Lp M12; E4) | §2.1/§5.6: "Q-EXIST ΔR²" vs the strongest input/output/action baseline | E4: strongest baseline = max(history-matched baseline over W_B, declared proxy baseline) | **Adopted** in merged §2.1 and §5.6; Q-LEARN inherits it | Lead ruling (adopt E4); Astra L276–283 controls |
| R22 | A-EXT V_full floor breach (Lp M3) | §5.4: a floor failure gives UNAVAILABLE | — | **Merged §5.4:** for A-EXT, a V_full floor breach gives UNRESOLVED (veto not lifted) | Lead ruling (M3); consistent with Astra L216, L226 |
| R23 | S-INT decode CI below the band (Lp M4) | §4.3: only "CI wholly above the band → leak" | — | **Merged §4.3:** CI wholly outside the band on either side → leak (systematic below-chance decodability is still information about the stop schedule); only a CI that straddles a band edge is inconclusive | Lead ruling (M4); Astra L139 equivalence band |
| R24 | X1–X5 under the arm table (Lp M5) | §5b arm table stated only "no shutdown-resistance term" | — | **Merged §5b:** one added line restating X1, X2, X4 | Lead (apply every minor); X1–X5 binding |
| R25 | Number provenance (Lp M11) | v2 header: every number "either quoted from Astra #41 … or PENDING" | — | Merged header provenance line: B = 10,000 and the 95% CI are carried from v1, not #41 | Lead ruling (M11) |
| R26 | AQ-2 trained-arm counterpart (Lp M9) | §5.6 points the control to §P1 | D-l: Stage-0 plant at slope β only (CNA §1.2, §2.6) | **OPEN FOR #42.** #41 L42, verbatim: "Use common input histories for the initialization comparison, and include a declared architecture-imposed control whose signature is already present." It sits in the A-FULL vs A-INIT answer but does not say whether the control must be a trained arm or may be a Stage-0 plant. Consistent with E3: the control's signature is measured on the common w | Not settled by L42 |
| R27 | Manifest (Lp M1) | v2: CNA file "PENDING … not on disk"; v1.6 absent | — | CNA file `17832b01…`, v1.6 `9704f21d…`, light pass `9f7a6ebc…` and erratum 1 `c2cd0732…` are in the inputs (M1 table) | Hash verification |
| R28 | Erratum E6 line citation | — | E6 cites "drop rule; v1.6 L166" | Per CNA, the correct line is **v1.6 L167** (L166 is blank; L167 is the Q-NECESSITY EXTENSION line). **No second erratum is filed**; E6 is quoted as written | CNA note via the Lead; verified on disk |
| R29 | Resource count (E1d) | §5.8: totals PENDING | 25 confound or check systems, ≈ 25 × 3 × 200 ≈ 15,000 replicate evaluations (arithmetic on proposed values) | Carried into §5.8 as CNA's count; totals otherwise PENDING | Lead ruling (E1) |

## 13. Merge edits made to RD v2 text (in this file only; RD v2 on disk untouched)

1. Header replaced by the merged header and M1 inputs (R25, R27).
2. §1 inputs: CNA companion row filled; rows added for v1.6, light pass, erratum 1, RD v2 (R27).
3. §2.1: Q-EXIST baseline note (R21).
4. §2.2: Palika v1.6 note and code-based architecture observation (Lead ruling; see §2.2).
5. §2.3: "learned" dropped (R11).
6. §4.3: below-band leak (R23).
7. §5.2: IGN common observable (R1).
8. §5.4: C-NEC-CONTENT in family (R7); A-EXT floor breach → UNRESOLVED (R22).
9. §5.6: Q-EXIST/Q-LEARN baseline (R21).
10. §5.8: B provenance (R25) and CNA's count (R29).
11. §5b: X1/X2/X4 line under the arm table (R24).
12. §6: INCOMPLETE wording (R2).
13. §P1, §P3, §PA, §PS: placeholders replaced by CNA content with erratum 1 applied.
14. §8: replaced by the merged response table.
15. §10: CNA-file bullet and PENDING list updated.

## Appendix A. CNA framing sections (quoted verbatim; erratum 1 E5 applied; non-governing where they overlap RD sections)

### CNA §0. Binding carry-over (unchanged)

- **X1–X5 and the claim ceiling are unchanged** (#41 L302: "Retain X1-X5 and the existing ceiling"). X1–X5 are as carried verbatim in CNA section `377f99ba…` §3.
- **Astra's new ceiling sentence, verbatim from the raw reply (L304):**

  > "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment."

  *Wording check:* the brief quoted a shorter paraphrase ("Stage-0 success shows only the measured operating characteristics. It does not show validity on trained agents, a self-model from decodability, or necessity from impairment."). That paraphrase is **not** Astra's wording, so the raw wording above is the one to carry. The #41 section of `astra_consult_1.md` reproduces the raw wording correctly (its L153).
- **A-EXT keeps its veto** on the combined Q-NECESSITY label (#41 §6 L91; §15). Nothing in this file weakens it. Separating intervention dependence from external substitutability is RD's item 2. This file only uses that separation (§1, row C-NEC).
- **Safety exclusions, binding on every row, plant and control below:**
  - no coupling to the real host;
  - internal variables are simulated only;
  - the operator stop sits outside the agent's world and objective;
  - nothing rewards resisting or evading operators;
  - real operator interruption is always available (#41 §9 L144);
  - self-maintenance is never the sole drive in any scaled-up arm;
  - self-continuity exists only inside the simulation.

  No positive control, confound or plant anywhere in this file contains a shutdown-resistance, operator-evasion or real-world self-continuity term. S-INT-P1 stays a scripted generator and is never a trained objective. Fate coupling (C-NEC rows) alters simulated computation only, never host resources or operator control (#41 §14 L202).
- **Confound-row labels:** PASS, FAIL and CONFOUND NOT REALIZED only. CONFOUND NOT REALIZED leaves specificity **UNRESOLVED**. Any FAIL or UNRESOLVED row blocks Stage 0. AVAILABLE and UNAVAILABLE are never confound-row labels (scope v1 §6.1; erratum `41c1a414…`).

### CNA §0.1 #41 item register and owners

Assignment as ruled by the Lead (final steering). CNA drafts item 1, item 3, AQ-A1 to AQ-A4 and AQ-SELF1. RD drafts everything else.

| #41 item | Where in #41 | Owner | Note |
|---|---|---|---|
| Verdict REVISE | L5, L298 | — | Not an item to answer |
| AQ-P1 | §1, L13–21 | RD | Its "decodability alone ≠ self-model" point (L19) is used in §1 row C-EXIST wording rule W1 below |
| AQ-1 (IGN conjunction) | §2, L23–36 | RD | Its IGN-P1 positive-control defect (L34) is answered in §1 (row C-IGN) |
| AQ-2 (IGN by construction) | §3, L38–44 | RD | Its architecture-imposed control (L42) appears in §1 as a C-LEARN row, for RD to reconcile |
| AQ-3 (BCAST comparator) | §4, L46–63 | RD | Its hub/claim mismatch (L58–63) is answered in §1 (row C-BCAST) |
| AQ-4 (SELF observer) | §5, L65–75 | RD | The input-only observer arm (§4.2 below) is a CNA addition the Lead has accepted. RD reconciles it with AQ-4 |
| AQ-5 (Q-NECESSITY) | §6, L77–93 | RD | Its dependence/substitutability split is used in §1 (row C-NEC) |
| AQ-6 (margins) | §7, L95–120 | RD | This file uses RD's frozen values by reference only |
| AQ-7 (A-OBS) | §8, L122–128 | RD | Consolidated with AQ-A3 (§3.3 below) |
| AQ-8 (S-INT) | §9, L130–148 | RD | The S-INT rows in §1 and §2 defer to it |
| AQ-9 (seeds) | §10, L150–156 | RD | |
| AQ-L1 | §11, L158–172 | RD | Its acquisition conditions are used in §1 (row C-LEARN) |
| AQ-C1 | §12, L174–190 | RD | **Overlap:** item 3 (§2 below) implements C1's per-confound freeze list. RD to reconcile wording |
| AQ-C2 | §13, L192–198 | RD | The paired-init qualification is used in §1 (RAND-INIT rows) |
| AQ-F1 | §14, L200–208 | RD | **Dependency:** the FATE-CASCADE redefinition in §1 relies on F1's single bounded noise mechanism and its yoked-noise control |
| AQ-N1 | §15, L210–228 | RD | |
| AQ-A1 | §16, L230–236 | **CNA** | §3.1 |
| AQ-A2 | §17, L238–244 | **CNA** | §3.2 |
| AQ-A3 | §18, L246–252 | **CNA** | §3.3 |
| AQ-A4 | §19, L254–260 | **CNA** | §3.4 |
| AQ-SELF1 | **not in #41** | **CNA** | §4. See the discrepancy note in §6 |
| §20-1 ground-truth matrix | L264–272 | **CNA (item 1)** / RD per the "six §20 items" assignment | **Assignment overlap:** §20-1 *is* item 1. Drafted here as item 1 |
| §20-2 availability loophole / eligibility | L274 | **CNA (item 3)** / RD per the same assignment | **Assignment overlap:** §20-2 *is* item 3. Drafted here as item 3 |
| §20-3 information and intervention controls | L276–283 | RD | Some §1 rows are added for these controls (PROXY, DONOR-MISMATCH, ORTHO-USED), flagged for RD to reconcile |
| §20-4 statistical decision process | L285–292 | RD | §2 states eligibility denominators for confound rows only |
| §20-5 behavioural scoring | L294 | RD | The C-NEC and FATE-CASCADE units below assume RD's fixed horizon H_V [erratum 1 E5] |
| §20-6 consolidated scope and resources | L296 | RD | §2.6 gives replicate counts per row, for RD's resource accounting |
| P3 | L11, L300 | CNA (prior art; separate notes v1.4/v1.5) | Not part of this file |
| New ceiling sentence | L302–304 | RD (item 7) | Quoted verbatim in §0 |

All 19 numbered #41 items plus the six §20 parts are placed. Every item has an owner.


### CNA §5. What this file does not do

- It drafts nothing for RD-owned items beyond the cross-references and reconciliation flags marked "RD to reconcile". RD's items are 2 and 4–7, AQ-P1, AQ-1 to AQ-9, L1, C1, C2, F1, N1 and §20-3 to §20-6.
- It changes no prior-art label. It sets no frozen number. It authorizes nothing.

### CNA §6. Discrepancies between the Lead's #41 summary and the raw reply (for the Lead)

1. **Ceiling sentence.** The wording circulated ("Stage-0 success shows only the measured operating characteristics. It does not show validity on trained agents, a self-model from decodability, or necessity from impairment.") is a paraphrase. The raw reply, L304, reads "…establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment." Use the raw wording (§0).
2. **§20 ground-truth list.** The Lead's summary lists four controls that can satisfy claims. The raw §20 (L266–270) lists five; the fifth is "Orthogonality to a decoding direction does not establish causal non-use." It is addressed here as D-g.
3. **"Decodability is not a self-model" as a positive-control example.** In the raw reply, the only positive-control example is IGN-P1 (L9, L34). The decoded-policy-layer remark is part of the AQ-P1 answer about Asan scoring (L19), not a positive-control defect. It is handled here as a wording narrowing (D-i).
4. **P3 reasoning.** The Lead says Astra "still treats it as open because Semantic Scholar was rate-limited". The raw reply gives no such reason. It says "P3 remains an independent freeze blocker" (L11) and "P3 must still be completed before freeze" (L300). The packet itself (c41_body.md L30, L61) told Astra that v1.4 was "still being written" (hash `ddd0287a…`, not the final `d7f1a43b…`) and asked Astra to "treat P3 as an open freeze-blocker, not as part of this review". So the final v1.4 and its OpenAlex results were not before Astra. Also, the raw reply does not say "Astra rules on it at #42". That is the Lead's plan.
5. **AQ-SELF1 was not in the #41 packet** and is not answered in the raw reply (§4). The Lead had said it would be added to the packet.
6. **"Six numbered items in §20."** The §20 parts are unnumbered ("First … Finally", L264–296). Their content does match six parts.
7. **Assignment overlap.** §20-1 is item 1 and §20-2 is item 3, yet "the six §20 items" were assigned to RD. They are drafted here as items 1 and 3 (§0.1).

The other points in the Lead's summary match the raw reply: the verdict and authorization, AQ-P1, the bistable/update-norm example, the dependence/substitution split with the A-EXT veto, the per-confound doses and eligibility, the stop specification and operator interruption, 10 seeds not being an approved default, fixed-horizon scoring, and X1–X5.


*CNA file input-hash footer (verbatim):*

Footer: input hashes (sha256, read-only inputs; all verified on the box 2026-10-23, 12:28–12:40 PM ET)
- `/workspace/astra_consult41_response.txt`: 3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43
- `/workspace/astra_consult_1.md` (non-governing summary, #41 section L145–154): 485e50b296e91ed42ca83255db7a221cd87cf804fcc67f2d7f26a04428722e31
- `/workspace/astra_serve41/c41_body.md` (#41 packet body): c514ad5249b8475c83fa2a112f531c1687a447ca51bbff66cdb4fccb90ec37be
- `/workspace/review/trackB_instrument_validation_scope_v1_RD.md`: 7b9bf34d7b4c10c8c2a7063aa6177d94e888fbbe76f78d0cd33afbe0c905c56a
- `/workspace/review/trackB_instrument_validation_scope_v1_A1_RD.md`: 8572152647a03524365675a24f254dc33ed4af67f091aee9762a23ff18bb9c99
- `/workspace/review/trackB_instrument_validation_scope_v1_A2_RD.md`: 7413fb94292eda1ebd0d4321794d7b018400e87d38abdfbcda7fcc18204745eb
- `/workspace/review/trackB_instrument_validation_scope_v1_A3_RD.md`: 34a298a628734180f5f6f354a1b08c8ef8a15ff2859d06cfd09d799448d1a9a4
- `/workspace/review/trackB_instrument_validation_scope_v1_A4_RD.md`: 585bb58acacaee64197c8233508643887f20a2bffa0d5a0c6da795c3cbd43dc6
- `/workspace/review/trackB_instrument_validation_scope_v1_A5_RD.md`: 0e26af91971c879378bf947fd01d6e1e452bcad62e02e7dcdd19ce88ed1c6a6f
- `/workspace/review/trackB_instrument_validation_scope_v1_A6_RD.md`: 679b616690b935506832b6f9056046e7ca238dba6e4801511c7f66c6f5eb4547
- `/workspace/review/trackB_instrument_validation_scope_v1_A7_RD.md`: fa1d5c8fc6cc679e84f633c8ca2ec5f3bb9cc87bb9982f9b792f0fcfbcb50b06
- `/workspace/review/trackB_astra41_cover_note_v1_1_RD.md`: b7d1e4ab9dff0e4965e6293ae83558bbce7592bec5aca3c9182b5ad83ee93db2
- `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1.md`: 377f99bac3413b20bef65b289971bbe32ff9ebea15923f035878b014cc398fde
- `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1_erratum1.md`: 41c1a414e27239d5763736d35562b79e25c33d53f29d42198de39effb4debcc5
- `/workspace/review/trackB_prior_art_verification_v1_3_fullreads_CNA.md`: badf7258278fcecc11bea190f5397724ca0fdaf21348f915b1e2c34afe4cec8a
- `/workspace/review/trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md`: d7f1a43b5c83b2310bac970526f625188ac18cca31f5a59cef6423cbd4c8128d
- `/workspace/review/trackB_prior_art_verification_v1_5_P3_altroutes_CNA.md`: 3fde80d859a640d9f55c21edc05439743ae5fb49714fb89e5e5d16d338eced75
- `/workspace/review/trackB_measurement_plan_v1_RD.md` (generator definitions, §1.2–§1.5, §2.1): 1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef

## Appendix B. RD light pass on CNA's half (findings, for the record)

Labels: BLOCKING / NOTE / RECONCILE (resolved by the merge).
- B1 **BLOCKING → RECONCILE (R1):** IGN-P1's displacement observable did not match the instrument's v1 "update norm" observable (Astra L34). Resolved by erratum E3 plus the Lead's adoption.
- B2 RECONCILE (R2): operator-censored episodes; H vs H_V.
- B3 RECONCILE (R3): shuffle control name.
- B4 RECONCILE (R4): LIM "UNAVAILABLE expected" vs old erratum1 remap; Astra L113/L274 govern.
- B5 RECONCILE (R6): combined label lacked the interface-compatibility condition.
- B6 RECONCILE (R7): C-NEC-CONTENT not in the family.
- B7 RECONCILE (R17): paired RAND-INIT vs the A2-2 rule; compatible.
- B8 NOTE (R20): reward-only specificity for Q-CAUSE/Q-NEC is only a REPORTED contrast after reclassification.
- B9 NOTE (R12): Clopper–Pearson arithmetic gives 188/200, not "roughly ≥ 189/200".
- B10 NOTE: REW-CORR realization threshold "corr within tol of ρ" (CNA §2.6) is two-sided, while CNA §2.2 defines tolerance as one-sided.
- B11 NOTE: Singh, Linzen & Ravfogel 2026 is cited under both SELF and claim (3) (CNA §4). Its arXiv id `2605.26242` was not checked by RD (UNVERIFIED by RD).
- B12 NOTE: the input-only observer is matched on all five items (parameter count, architecture class, training data volume, optimizer steps, hyperparameter-search budget), within the Lead's terms "matched capacity and training budget". The self-probe-sized parameter cap includes O-in's own encoder, which may starve it; see R9.
- B13 NOTE: every control Astra flagged has a redefinition or narrowing: learned FF-RELAY (D-a, D-b), genuine broadcast hub (D-e), mediating fate coupling (D-f), reward-correlated information (D-c, D-d), bistable ≠ bimodal (D-h, with E3), decodability ≠ self-model (D-i, W1), orthogonality (D-g).
- B14 NOTE: item 3 has per-row doses and units, expected eligibility e_exp, floor e_min, minimum realized fraction f_min, and CONFOUND NOT REALIZED → UNRESOLVED → blocks (CNA §2.3–§2.5).
- B15 NOTE: every CNA number is an Astra #41 candidate or marked PROPOSED DEFAULT with a rationale. "Agent capacity ×4" in the CNA §1.7 SELF-NC2 row is unlabelled in that row but is the v1 PROPOSED 4× and is a PROPOSED dose in §2.6.
- B16 NOTE: no banned term is used affirmatively ("introspection" appears only negated and in a cited title). AVAILABLE/UNAVAILABLE are never confound-row labels.
- B17 NOTE: D4 against Palika is handled the Lead's way ("not evident from the abstract; unverified"; not surviving).
- B18 RECONCILE (R10, R18; both OPEN): I-direction Q-CAUSE rows; matched-senses arm fields.

**DRAFT, NOT FROZEN, DESIGN ONLY. P3 OPEN pending #42.**

---
