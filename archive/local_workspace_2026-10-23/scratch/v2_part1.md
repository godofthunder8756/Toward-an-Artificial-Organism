# Track B instrument-validation scope v2 (Research Delegate; CNA co-drafts named sections)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** Nothing runs. No Stage-0 run, training, simulation, solver or checkpoint inspection is authorized. Astra #41, verbatim: "No Stage-0 run, training, simulation or checkpoint inspection is authorized by this review."

- **Supersedes nothing by edit.** v1 (`7b9bf34d…`) and amendments A1–A7 remain on disk, unchanged. Once the Lead accepts this file and the CNA companion file is merged, v2 is the new governing scope draft. Until then it is a draft only.
- **Answers:** Astra consult #41, verdict **REVISE**.
- **Written:** 2026-10-23, about 12:40 PM ET. Additive and new. Read-only on the repo and GitHub.
- **Authorship split (the Lead's assignment and steering, 2026-10-23 ~12:29 PM ET):**
  - **RD (this file):** item 2 (dependence vs substitutability), item 4 (stop spec), item 5 (inference and resource plan), item 6 (viability scoring), item 7 (ceiling); answers to AQ-P1, AQ-1..AQ-9, AQ-L1, AQ-C1, AQ-C2, AQ-F1, AQ-N1 and the six §20 items.
  - **CNA (separate companion file, PENDING CNA FILE; expected path `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md`, hash TBD, not on disk when this file was written):** item 1 (claim-to-ground-truth table and every control redefinition or claim narrowing), item 3 (realization doses, units, expected eligibility rates), AQ-A1..AQ-A4 and AQ-SELF1 (including the Lead-accepted SELF input-only observer arm). This file holds **placeholder sections only** for those (§P1, §P3, §PA, §PS), each quoting Astra's verbatim requirements so the merge is mechanical. RD does not draft their content.
- **Labels.** Confound rows: PASS / FAIL / CONFOUND NOT REALIZED only (never AVAILABLE or UNAVAILABLE). Anything unsettled is PENDING or UNVERIFIED. No number here is invented: every numeric value is either quoted from Astra #41 (marked "Astra #41 candidate") or PENDING.

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
| CNA v2 companion (items 1, 3, AQ-A1..A4, AQ-SELF1) | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` | **PENDING CNA FILE** (not on disk at time of writing; hash TBD; content not merged here) |

**Packet-record note (checked in `c41_body.md`).** The packet Astra received listed prior-art v1.4 as "in progress … `ddd0287a` (file still being written)", not the final `d7f1a43b…`, and it contains **no AQ-SELF1 question** (a grep for "SELF1", "Ashuach" and "disagree" finds nothing). Astra therefore did not rule on AQ-SELF1 and did not see final v1.4 or v1.5. See §PS and §8.

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

Q-LEARN (acquisition) stays a separate contrast on top of any of these (§5.6). IGN is a dynamical-signature instrument and is not one of Astra's four; its claim stays "conditional bimodality" (§5.2, §P1).

**2.2 Novelty labels unchanged; Palika added; consequences stated.** Labels from A6/A7 stay: Q-NECESSITY is an EXTENSION (D2 as frozen in A1-2); SELF NOVEL AS FAR AS FOUND; claim (3) PARTIAL OVERLAP. Per the Lead's ruling (2026-10-23 ~12:36 PM ET) on CNA v1.5 (`3fde80d8…`), **Palika et al. 2026 is the third Q-NECESSITY comparator** (abstract-level only; SSRN full text returned HTTP 403).

| Comparator | D1 interoceptive content | D2 learned RL agent (as frozen) | D3 viability outcome | D4 same-size module ablations + matched arms | What survives for us |
|---|---|---|---|---|---|
| Wilterson & Graziano 2021 | survives | does not survive | (as A6-2) | survives | D1, D4; plus stated difference: our model is learned rather than supplied |
| Asan 2026 | does not survive | does not survive | survives, with A6-2 caveat (masking measure unnamed) | survives | D3 (caveat), D4; plus stated difference: recurrent vs feedforward |
| Palika et al. 2026 (abstract only) | shared (does not survive) | shared (does not survive) | partial overlap only | **not evident from the abstract; unverified** | D3 only in part (fixed-horizon viability form, abstract-level). D4 is **not** listed as a surviving difference over Palika. |

- Label: **EXTENSION**, unchanged. The A3-1 drop rule already gives EXTENSION (not all four differences fail, since D3 is only a partial overlap), so confirming D4 against Palika's full text **does not block freeze** (Lead ruling). The Palika D4 question goes to Astra at #42 (§8).
- **"Learned rather than supplied" separates us from Wilterson & Graziano 2021 only.** Palika's interoceptive state is learned (CNA v1.5), so this is not a distinguishing feature in general.

Astra, verbatim: "The D1-D4 rule is a record of differences, not a sufficient scientific definition of an extension. One surviving difference may be important or cosmetic. State its consequence for the inference." Consequences (RD draft; for CNA light pass):
- **D1 (interoceptive content; survives only against W&G):** the tested estimate targets simulated body variables, so any Q-NECESSITY result is about dependence on that estimate, not on an attention or competence model. It does not license "self-model" (§2.3).
- **D3 (viability outcome):** dependence is measured on a fixed-horizon in-world viability score (§6), so a result speaks to the declared in-world function, not to reward or task accuracy.
- **D4 (same-size ablations of other modules plus sham; survives against W&G and Asan, unverified against Palika):** makes the result a *selective* impairment contrast rather than generic damage. Per the new ceiling (§7), selective impairment still does not establish endogenous necessity.
- **A-EXT (required):** adds an explicit substitution challenge (§3); its consequence is that "dependence" and "substitutability" are reported as two outcomes.
- **Recurrent vs feedforward (stated difference vs Asan, not a criterion):** consequence limited to the memory-access contrast (AQ-A2, §PA); Astra: it "validates a memory-access contrast, not a general distinction between models with and without self-models."

**2.3 Decodability is not a self-model (applies to our own module).** Astra, verbatim: "A decoded policy-layer pattern should count as a candidate internal representation under the same operational standard applied to your allostatic module. A separate module name is neither necessary nor sufficient for a self-model. Decodability alone does not establish predictive modeling or causal use in either system." Consequence: the allostatic module is a **candidate internal representation** of simulated E/I. Q-EXIST MET licenses only accessibility. The phrase "learned interoceptive self-model" in A1–A7 label text is retained only as the frozen label wording; proposed for the Lead: in v2-era result text, use "learned interoceptive estimate module" (PENDING Lead ruling). No label changes.

**2.4 SELF retargeting needs its own justification.** Astra, verbatim: "SELF also changes the target from Binder's prediction of a model's own behavior to prediction of simulated body variables. That adaptation needs its own justification; it does not inherit an introspection interpretation." RD justification (draft): SELF measures **prediction advantage for simulated body variables over a matched external observer with declared access**; it is a privileged-information instrument, not an introspection instrument, and no introspection wording is used. Binder's design element retained is the comparator, verbatim: "Binder's experiment explicitly compares self-prediction against another model trained on the target model's behavior." Sufficiency of this justification is for Astra at #42 (§8). Observer-arm design changes (including the input-only observer arm) are CNA's (§PS).

**2.5 Prior-art record.** The Asan-specific judgments are UNVERIFIED by Astra (Zenodo not retrieved). Palika is abstract-level only. P3 stays open until Astra rules at #42 (§10).

---

## §P1. PLACEHOLDER — Item 1: corrected claim-to-ground-truth table (PENDING CNA FILE, path/hash TBD)

**Owner: CNA.** RD does not draft this table. The CNA file must, for every claim/instrument (IGN, BCAST, SELF, Q-EXIST, Q-LEARN, Q-CAUSE, Q-NECESSITY, kept separate), give: mechanism present (positive control and why it MUST produce the measured observable), mechanism absent (negative control), claim challenged; and for each problem control state **redefine the control** or **narrow the claim**, and why.

Astra's verbatim requirements to be satisfied (merge checklist):
- §20: "First, repair the ground-truth matrix: A learned FF-RELAY may genuinely acquire an accessible estimate. It is not necessarily negative for the current Q-LEARN claim. Reward-correlated information may genuinely satisfy the declared decoding criterion. HUB-STATE may genuinely broadcast. Fate coupling may mediate real dependence. Orthogonality to a decoding direction does not establish causal non-use. For each row, state the mechanism that is present, the mechanism that is absent, and the exact claim being challenged."
- AQ-P1: "Several required negative controls can satisfy the claims as presently defined, while some positive controls need not produce the measured signature. Numerical acceptance rules cannot resolve those contradictions."
- AQ-1 (IGN-P1): "bistability of x does not guarantee bimodality of the write-update norm. Stationary attractors can have zero update, and opposite signed updates can have identical norms. IGN-P1 must produce the actual measured observable." "If the intended claim becomes bistability, add controlled initial conditions, persistence at fixed input, and sweep-rate controls distinguishing hysteresis from ordinary lag. That is a different claim."
- AQ-2: "include a declared architecture-imposed control whose signature is already present."
- AQ-3 (HUB-STATE): "an ordinary hub genuinely read by many modules can satisfy C-BCAST. It is not automatically a false positive. Distinguish: Broad causal routing. A designated workspace's advantage over alternative routing states. HUB-STATE can challenge the second claim. It cannot be stipulated to falsify the first."
- AQ-7: "Decoding in this control is informative. It is not automatically a failure of Q-EXIST."
- AQ-F1 (FATE-CASCADE): "Do not automatically classify a loss that disappears with coupling disabled as generic damage: coupling can mediate a genuine causal effect. FATE-CASCADE needs a construction demonstrating that the claimed estimate is not the operative mechanism."
- AQ-A3: "Decoding an irrelevant variable is not inherently a false existence result."
- AQ-C1: "This principle is valuable, but its validity depends on whether the mechanism actually is a confound for the stated claim."
- AQ-C2: "Random initialization can genuinely contain decodable information. An existence instrument should not be required to deny that."
- §20 third item (controls for CNA to place in rows): "History-matched input/output/action baselines. Reward, clock, episode-identity and position proxies. Identical decoding with different causal use. Redundant and distributed representations. Collateral intervention damage and conditional donor mismatch." (The sixth bullet, target leakage, is RD's: §5.3.)

v1 text that §P1 must replace (see §9): v1 §6.2 HUB-STATE pass rule ("Otherwise … the row is FAIL"); v1 §6.2 FATE-CASCADE rule ("a gap that vanishes with coupling off is read as cascade, not necessity"); v1 §4.1 IGN-P1 "a bistable unit (g > 1)"; plan v1 §1.5 Q-CAUSE "decodable-but-unused direction … orthogonal to the y-direction" used as a non-use comparator.

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

## §P3. PLACEHOLDER — Item 3: realization doses, units and expected eligibility rates (PENDING CNA FILE, path/hash TBD)

**Owner: CNA.** RD supplies no doses, units, thresholds or rates. Requirement stated here, binding on the CNA file:

- **No confound may pass by always failing to realize, and no instrument may pass a confound row by always being UNAVAILABLE.** CONFOUND NOT REALIZED leaves specificity UNRESOLVED, and UNRESOLVED blocks Stage 0 exactly as FAIL does (v1 §6.1, erratum 1; unchanged).
- Astra §20, verbatim: "Second, close the availability loophole. A realized confound cannot pass merely because the instrument is always UNAVAILABLE. Freeze expected eligibility rates for valid negative/confound cases. Reserve expected unavailability for explicitly designated rejection or limitation tests."
- Astra AQ-C1, verbatim: "Keep realization checks at every required dose; reject the universal raw-signature-to-margin mapping." "For every confound, freeze: Its causal construction. Its own dose parameter and units. Its raw signature and realization threshold. Realization tolerance and required frequency. The instrument outcome expected when that mechanism is realized." "Do not tune doses on final instrument outcomes. Do not select only successful realization replicates and silently discard the rest." "Report both realization frequency and the instrument's outcomes on the prespecified sample. Failure to realize a required dose remains unresolved."
- Astra AQ-6, verbatim: "BOUNDARY <= 0.05 at 2x | Retain as a resolution target, conditional on eligibility."
- Superseded: v1 §6.1 "Imitation strength is scaled so that the raw signature equals {0, 0.5, 1.0, 1.5, 2.0} × the instrument's margin." (Astra: "The proposed raw observables have different meanings and units … cannot all be doses of a margin in DeltaLL or comparator-adjusted gain.")
- RD's statistical side (denominators, eligibility counted in the denominator, confidence rule for realization frequency) is §5.4.

---
