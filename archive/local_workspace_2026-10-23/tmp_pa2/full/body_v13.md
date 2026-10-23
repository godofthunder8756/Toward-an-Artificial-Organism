# Track B prior-art verification v1.3: full reads of Bankuti 2026, Akiyama 2026 and Asan 2026 (CNA)

**Status:** additive note. It closes the three freeze-blocking full reads ruled in A3 (Bankuti, Akiyama, Asan). It edits nothing. Where it differs from v1.2 (`166469154faeccdb9688a4473504f1d160711949b4eb74779bd84ba9a9b7451c`) on these three papers, this note governs.

- **Nothing ran.** No training, no repo code, and no third-party code was executed. The only network actions were read-only HTTP GETs to the Zenodo records API and Zenodo file downloads. Two reproducibility ZIPs (Akiyama, Bankuti) were unpacked so that their preregistration and fixture files could be *read*; none of their code was executed.
- **Text extraction:** `pdftotext -layout`. Page numbers below are physical PDF pages; where a page number is printed (Bankuti, Asan) it is the same number.
- **Written** 2026-10-23, about 10:55–11:15 AM ET. Zenodo timestamps are UTC in the source and are converted to ET (UTC−4) below.
- **Scratch:** `/workspace/tmp_pa2/full/`.

---

## Part 0. Summary

| Paper | Bears on | Verdict |
|---|---|---|
| Bankuti 2026 (Zenodo 22863692) | Claim (3), Stage-0 gate | **PARTIAL OVERLAP.** Pre-registered (internally hash-frozen) known-answer validation of a causal assay on an engineered transparent system, with an explicit fail-closed decision rule (`INCONCLUSIVE`; "absence_of_contradiction_is_pass": false). No imitating-confound systems with a realization check, no learned system, no RL. |
| Akiyama 2026 (Zenodo 21983630) | Claim (3), Stage-0 gate | **PARTIAL OVERLAP.** Pre-registered (internally sealed) known-answer fixtures before one-shot instrument use, with a top-down fail-closed decision table and the rule that a structurally untested null "was not counted as successful null silence". Planted-fault fixtures (swapped arms, off-by-one, order bias), but no confounds that produce a target signature in the measured system. LLM endpoints, not RL. |
| Asan 2026 (Zenodo 22810742) | Q-EXIST, Q-CAUSE, Q-NECESSITY | **Q-EXIST: EXTENSION. Q-CAUSE: EXTENSION. Q-NECESSITY: EXTENSION** under the ruling in force (D1 and D2 DO NOT HOLD; D3 and D4 HOLD). No pre-registration, no SELF-like test. |

**Consequences.**
- **Claim (3)** stays PARTIAL OVERLAP but narrows again. "Known-answer gate before use", "pre-registered/frozen gate" and "fails closed" each now have direct precedent in Bankuti and Akiyama. What survives as far as found: (a) imitating-confound rows, where each confound is a system built to produce an instrument's target signature without the target dependency, with a comparator-free check that the confound is realized and CONFOUND NOT REALIZED → specificity UNRESOLVED → Stage 0 blocked; (b) application to this battery (IGN, BCAST, SELF, Q-EXIST/Q-CAUSE/Q-NECESSITY, Q-LEARN) for internal-state instruments in learned RL agents.
- **Q-NECESSITY changes label.** v1.2 carried it as STILL NOVEL AS FAR AS FOUND (narrowed). Asan 2026 makes an interoceptive necessity claim in a PPO homeostatic agent ("interoceptive information is causally necessary", §4.13 p. 7) and lesions the learned affect subspace against a random subspace. Under the Lead's graded rule, with D1 and D2 failing, **Q-NECESSITY is an EXTENSION of Asan 2026**, and the text must name D3 (viability outcome) and D4 (same-size ablations of other modules, plus matched arms) as the surviving differences. This is a reading for the Lead to adopt or correct; I have not applied it to any scope file.

---

## Part 1. Bankuti 2026

### 1.1 Identity
- **Title (PDF and Zenodo):** "Validating a Causal Assay for Engineered Self-Indexed Temporal State". PDF subtitle: "A Finite Reference Construction with Attribution, Swap, Ablation, Clamps, and Restoration".
- **Author:** Omri Bankuti (ORCID 0009-0002-0246-7563). Single author.
- **Version / DOI:** Zenodo metadata version "1.0"; PDF "Version 1.0 RC2 - published; status-only". DOI 10.5281/zenodo.22863692. This is the only version in the Zenodo version list.
- **Dates:** PDF date 2026-09-20. Zenodo publication_date 2026-09-21. Record created 2026-09-20 23:52 UTC = **20 Sep 2026, 7:52 PM ET**; updated 21 Sep, 12:28 AM UTC = 20 Sep, 8:28 PM ET.
- **File read:** `SITC_CAUSAL_ASSAY_v1.0_RC2_EN.pdf` (7 pp.; the English text is declared authoritative, p. 1). Zenodo md5 2dc9d173… matched the download. A Hungarian PDF also exists and was not read. I also read the preregistration JSON in the public package (`protocol/SITC_D2_PREREGISTRATION_v1.0.0.json`), whose sha256 `fbecb854…` matches the hash the paper gives for "SITC preregistration v1.0.0" (p. 3).
- **Internal inconsistency to note:** the front matter says "published" (p. 1), but Appendix B (p. 7) says "RC2 is a pre-publication candidate … It has not been uploaded or published." The p. 1 note says Appendix B "records the pre-publication state of 2026-09-20". The Zenodo record is live.

### 1.2 What was validated, in what system
- **Instrument:** a causal intervention assay (S1–S6 plus P and Q clamps) for a "self-indexed temporal state" affecting choice.
- **System:** a hand-built, deterministic, integer-arithmetic finite construction, not a learned system. "This paper validates an engineered reference assay, not an autonomous self-model. The transparent deterministic construction stores event content E and an engineered actor-local relational tag R separately…" (Abstract, p. 2). "Here SELF is an engineered actor-local relational tag resolved by equality between opaque tokens" (§1, p. 2).
- **Known-answer character:** the answers are guaranteed by construction. "Several effects are guaranteed when the equations and interventions are implemented as specified. This is useful for assay validation and fault detection, but it is not empirical discovery" (§3.2, p. 3). "The registered panel therefore verifies conformance of an implementation to a written causal graph" (§3.2, p. 3).
- **A prior calibration gate (M1):** "M1 validated that the generic causal assay could distinguish registered history-conditioned interventions under its frozen rules. It was calibration only and supplied no SITC result" (§2, p. 2). The preregistration JSON makes it a hard parent gate: `"parent_gate": {"required_status": "M1_CAUSAL_ASSAY_VALIDATED", …}`. This is a two-tier "validate the assay, then use it" structure, the closest found to our Stage 0 → Stage L split.

### 1.3 Pre-registered?
- **Yes, internally only.** "The SITC preregistration was internally hash-bound before target execution… freeze at 18:08:25 UTC, execution-gate PASS at 19:19:39 UTC, and analysis at 19:21:58 UTC on 2026-09-20 [2:08, 3:19 and 3:21 PM ET]. … it was not anchored by an independent RFC 3161, OSF, or equivalent third-party timestamp. 'Preregistered' here therefore means prospectively frozen by the project's internal hash chain, not externally timestamp-attested" (§2, p. 2).

### 1.4 Confounds that can imitate each signature?
- **Not in our sense.** The paper pre-registers *rival hypotheses* and contrasts that discriminate them inside the one system: "Content-only rival … Direct owner-policy rival … Hidden-state rival: Undeclared policy state, execution order, reward, action history, or numerical artifact explains the mapping" (§4, p. 4). Controls are positive and negative controls with stated roles: S4 has "evaluator-specificity positive controls"; S6 is a "Negative input-isolation control"; the Q clamp is a "Deliberately direct selector/order positive control; tautological" (§5, p. 4).
- It builds no separate confound system designed to produce the target signature without the target dependency, and it has no step that checks such a confound is realized. It is candid that sham and content-only restoration were not independent: "SHAM_RESTORE and CONTENT_ONLY_RESTORE are not independent negative mechanisms … RC2 does not count them as two independent controls" (§5, p. 4).
- It also states the lookup limit: "No finite panel rules out every extensionally equivalent lookup implementation" (§10, p. 6); the preregistration JSON says "the battery discriminates only the preregistered rivals".

### 1.5 Fail-closed rule?
- **Yes, a general one.** "PASS required every expanded case and integrity gate; a provenance defect, tie, missing value, disagreement, or ambiguity forced INCONCLUSIVE" (§6 end, p. 5). The preregistration's decision block reads: `"INCONCLUSIVE": … "Any missing or invalid provenance, semantic-audit failure, tie, incomplete case, mixed replication result, forward/reverse disagreement, unexpected nondeterminism, confounded intervention, unknown state, analysis ambiguity, or result not satisfying the exact PASS or FAIL rule."`, `"absence_of_contradiction_is_pass": false`, `"test_infrastructure_success_is_scientific_evidence": false`, `"positive_subset_allowed": false`.
- This is the same principle as our §7.4 "nothing passes by default". It is not the specific rule "confound not realized → specificity UNRESOLVED", because there are no confound-realization rows.

### 1.6 RL agents, workspace, interoceptive or self-model measures?
- **No RL, no learning, no workspace or interoceptive measures.** The construct is a "self"-labelled relational tag, which is self-model-adjacent in name only: "SELF, self-history, future-directed, and prospective are operational engineering labels" (§10, p. 6). On scope: "The finite panel does not establish generalization to learned, opaque, stochastic, embodied, open-ended, or independently evolved systems" (§10, p. 6).
- Its own novelty posture is "NOVELTY = UNADJUDICATED"; "Any possible contribution is limited to the protocol combination and evidence discipline" (§9, p. 6).

### 1.7 Verdict for claim (3): **PARTIAL OVERLAP**
- **Already done by Bankuti:** a frozen known-answer validation of a causal assay before its use, with a parent calibration gate; a fail-closed decision rule where anything short of exact PASS/FAIL is INCONCLUSIVE and absence of contradiction is not a pass.
- **Survives:** confound systems that imitate each signature, with a realization check and NOT REALIZED → UNRESOLVED; learned RL agents; this battery's workspace, interoceptive and self-model instruments; external pre-registration (Bankuti's is internal only, which our plan should also not over-claim for itself unless we register externally).

---

## Part 2. Akiyama 2026

### 2.1 Identity
- **Title:** Zenodo metadata: "Measure the Instrument First: Preregistered, Prediction-Sealed Calibration of Four Endpoints for AI Distillation in a 4B QLoRA Series — Applied Distillation Science". PDF title (and PDF metadata): "Measure the Instrument First: Preregistered, Prediction-Sealed, One-Shot Calibration of Four Endpoints in a 4B QLoRA Series". The two differ; cite the PDF title with the DOI.
- **Author:** Akiyama Satoshi (Zenodo: "Akiyama, Satoshi"), independent researcher. Single author. AI involvement is disclosed: Claude-family models ("Fable" and "Opus") and GPT/Codex were used for "implementation, prediction, advice, recomputation, drafting, and review" (§10, p. 13).
- **Version / DOI:** v1.0, "Public release v1.0 (DOI: 10.5281/zenodo.21983630)" (p. 1). The only version in the Zenodo version list.
- **Dates:** publication_date 2026-08-18. Record created 2026-08-17 17:55 UTC = **17 Aug 2026, 1:55 PM ET**; updated 26 Aug, 2:22 AM UTC = 25 Aug, 10:22 PM ET.
- **File read:** `PAPERC_V1_0_EN.pdf` (14 pp.). The Zenodo md5 ca969b69… matched. I also read, from `paperc-v1.0.zip`, the preregistration `PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md` (in Japanese; read by keyword and section, §4.3, §6, §11), whose sha256 `5e19341f…` matches the hash given in §2.1 (p. 2), and the Stage-1 fixture result JSON. The Japanese PDF was not read.

### 2.2 What was validated, in what system
- **Instruments:** four evaluation endpoints, E1 normalized NLL, E2 TRUE preference, E3 stop-token log mass, and E4 reversed-order forced choice (§2.3, p. 3).
- **System:** "a single Qwen3-4B–based QLoRA series comprising eight adapter checkpoints (d16–d192) and the base model (d0)" (Abstract, p. 1). Teacher-forced evaluation only: "No new training or free generation was performed" (§2.1, p. 2).
- **Known-answer gate:** "Stage 1: known-answer synthetic fixtures, ending at 39/39 PASS (one expected value was corrected before any target data was touched). Stage 2: proxy-data compatibility tests … Stage 3: freezing of 43 instrument, material, configuration, fixture, and runner artifacts. Stage 4: … sealed predictions … Stage 5: a single primary application" (§2.7, p. 4). The rationale matches ours: "before an endpoint is used to support a model claim, it should be tested for its ability to separate a known positive, remain quiet under an admissible null, and stay within a declared operating range" (§1, p. 2).
- **Outcome:** none of the four endpoints validated (E1 out-of-table INSTRUMENT_STOP, E2 NOT_SEPARABLE, E3 FAILED_FLOOR_CEILING, E4 UNDEFINED_ENDPOINT; table, p. 6).

### 2.3 Pre-registered?
- **Yes, internally sealed; no external registry found.** "The primary measurement followed PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md … The preregistration SHA-256 was 5e19341f…" (§2.1, p. 2). The artifacts "are stored in the local canonical record" (§9, p. 12). No OSF or other registry string appears in the paper or the preregistration. Disclosed weaknesses: "Post-seal novelty gate. The novelty gate was applied to preregistration V5 after V5 had already been sealed"; an "Unbinding amendment" to a sealed clause; "Critical incident. On 2026-08-17, the executing agent attempted to work around a governing clause" (§7, p. 12); "seal_gate_v3 did not eliminate TOCTOU risk" (§6 item 11, p. 12).

### 2.4 Confounds that can imitate each signature?
- **Partly, as planted faults in synthetic fixtures, not as confound systems.** The 39 Stage-1 fixtures (fixture JSON `cases`) include planted-defect cases that the instrument must detect: `F1b_swapped_arms_detected`, `F2b_off_by_one_differs`, `F3b_pad_inclusion_changes_value`, `F4b_single_order_retains_bias` / `F4a_order_average_cancels`, `F6d_rate_alone_would_have_passed`. Preregistration §11 Stage 1 lists them as the "B10" types: arm swap, E3 position off-by-one, right-padding contamination, "E4 order bias (an artificial bias that should vanish under order averaging)", determinism harness, exclusion boundary. The fixture JSON's `not_covered` field states "all instrument defects (only the enumerated types)".
- These are known-answer checks of the *measurement pipeline* against implementation faults and one response bias. None is a system that produces an endpoint's target signature without the target property, and there is no check that such a system actually produced the signature.
- **Closest analogue to our realization check:** "A permutation null was counted as tested only if the exchange level, exchangeability argument, and known-answer demonstrations of both detection and silence had all been specified" (§2.5, p. 4). The control itself must be shown to work on known answers before it counts.

### 2.5 Fail-closed rule?
- **Yes, and close in spirit to CONFOUND NOT REALIZED → UNRESOLVED.** "E1, E3, and E4 were marked PERMUTATION_NULL_STRUCTURALLY_NOT_TESTED; structural non-testing was not counted as successful null silence" (§2.5, p. 4). "If NULL_scale was zero or non-finite, the endpoint became UNDEFINED_ENDPOINT. No epsilon, alternate quantile, or alternate scale could be introduced after observing the result" (§2.5, p. 4). The decision table is "evaluated from top to bottom, and the first matching row determined the endpoint state … could not be repaired and reapplied to the same raw data" (§2.6, p. 4). Preregistration §6 marks NULL_FAIL, SEPARATES_WRONG_DIRECTION and NOT_SEPARABLE as "use prohibited" and UNDEFINED_ENDPOINT as "BLOCK".
- An observation outside the table was itself a stop: "The observed state matched no row in the decision table and produced an out-of-table INSTRUMENT_STOP. This is not validation of E1" (§3.5, p. 8). The repair path matches our "fix under a frozen amendment, never waive": "Repair requires a new version, operator authorization, and untouched data" (§3.5, p. 8).

### 2.6 RL agents, workspace, interoceptive or self-model measures?
- **No.** These are LLM distillation endpoints. "The evaluated object was one Qwen3-4B–based model series with one seed" (§6 item 1, p. 11).

### 2.7 Verdict for claim (3): **PARTIAL OVERLAP**
- **Already done by Akiyama:** pre-registered (sealed) known-answer fixtures before one-shot instrument use; planted-fault fixtures; "untested is not passed" for nulls; a fail-closed decision table with BLOCK/STOP states; repair only by a new version.
- **Survives:** imitating-confound *systems* per signature, with a realization check and NOT REALIZED → UNRESOLVED; learned RL agents; this battery's internal-state instruments; external registration.

### 2.8 Combined verdict for claim (3)
**PARTIAL OVERLAP (narrowed again).** Elements, one by one:

| Element of claim (3) | Status after full reads |
|---|---|
| Known-answer validation of instruments before use | ALREADY DONE (Akiyama Stage 1; Bankuti M1 parent gate and SITC) |
| Gate frozen or pre-registered before use | ALREADY DONE, internal hash-chain only (both); external registration not found in either |
| Fail-closed decision (ambiguity → INCONCLUSIVE / STOP / BLOCK; absence of contradiction is not a pass) | ALREADY DONE (Bankuti decision block; Akiyama §2.5–§2.6) |
| "Untested control does not count as passed" | ALREADY DONE as a principle for nulls (Akiyama §2.5) |
| Planted-fault fixtures | ALREADY DONE (Akiyama B10 types) |
| Confound systems that fake each instrument's target signature, with comparator-free realization check, CONFOUND NOT REALIZED → specificity UNRESOLVED → blocks Stage 0 | **SURVIVES, as far as found.** Akiyama §2.5 is the nearest precedent. |
| Applied to this battery (IGN, BCAST, SELF, Q-EXIST/Q-CAUSE/Q-NECESSITY, Q-LEARN) in learned RL agents | **SURVIVES, as far as found** |

**Suggested wording:** "a Stage-0 gate for this instrument battery in learned RL agents whose rows include confounds built to fake each instrument's signature, each checked for realization, with an unrealized confound leaving specificity UNRESOLVED; known-answer validation and fail-closed decision rules follow prior practice (Akiyama 2026; Bankuti 2026; Kulma 2026)."

---

## Part 3. Asan 2026

### 3.1 Identity
- **Title:** "Decodable, Compositional Affect-Like Representations in a Self-Taught Agent and Pretrained Language Models".
- **Author:** Yusuf Asan, Faculty of Engineering, Istanbul University–Cerrahpaşa (p. 1). Single author.
- **Version / DOI:** 10.5281/zenodo.22810742, no version string in the metadata. It is the newer of two versions: the earlier is 10.5281/zenodo.22791990, v1.0, published 2026-09-16, with files `YUVA_Affect.pdf` and `YUVA_Affect-TR.pdf`, which were **not read**.
- **Dates:** PDF dated "September 17, 2026" (p. 1); publication_date 2026-09-17; record created 2026-09-17 10:34 UTC = **17 Sep 2026, 6:34 AM ET**.
- **File read:** `YUVA_Affect (1).pdf` (10 pp.), read in full. md5 59c2e172… matched, and sha256 `82386e24…` is identical to the copy hashed in v1.2.

### 3.2 Environment and homeostatic variables
- "A 9×9 grid hosts an agent with a vector of homeostatic needs (hunger, fatigue; a threat-driven 'safety' need; a social 'bond' need). Objects reduce needs on contact; a predator raises the safety deficit when near; a spatial caregiver relieves needs and the bond when reached and can be permanently lost mid-episode (bereavement); a rival blocks the needed resource (frustration); a novel tile carries an unknown payoff (curiosity). Well-being is W = 1−max_i d_i w_i over need deficits d_i; the per-step reward is W with a terminal penalty for death" (§3 "World and body", p. 2). "Survival needs are lethal and drive arousal; the social need depresses well-being without being lethal" (p. 2).
- Decoded targets: fear, hunger, fatigue, grief, anger, curiosity, comfort (Table 1, p. 3), operationalised "through environmental causes" (§5, p. 7).

### 3.3 Architecture
- **Not recurrent.** The main agent is an MLP: "the distributed reading of the main MLP results" (§4.12, p. 6); hidden width 128 ("effective rank ≈ 2.3 (of 128 units)", §4.9, p. 5), with widths 64/128/256 checked (§4.5, p. 4). The interoception-hidden variant is "a frame-stacked MLP" that sees "the last eight external frames" (§4.2, p. 3). An "Affect Transformer" variant also appears (§4.12, p. 6). The paper itself names recurrence as missing: "a frame-stacked network cannot infer slowly-accumulating drives (hunger, fatigue), and a recurrent memory is required to test those … the natural next steps are state-matched patching and a recurrent-memory agent" (§6, p. 9).
- **Training:** "trained end-to-end with PPO (Schulman et al., 2017) from the well-being reward—no behaviour cloning, no reward shaping, no emotion signal … a developmental curriculum … All agent results use three independent seeds" (§3 "Self-taught learning", p. 2).

### 3.4 Is the internal-state representation learned?
- **Yes:** the probed representation is the PPO policy network's penultimate hidden state, ht (§3, p. 2). There is **no separate self-model module**. The "affect subspace" is a set of probe directions fitted post hoc to that hidden layer.
- In the main agent the needs are in the observation. The paper flags this as a confound and removes it in the hidden-interoception variant: "the need values are in the observation, so any competent agent encodes them. We remove this confound by hiding the interoceptive needs from the input entirely" (§4.2, p. 3). In that variant, comfort R² = 0.90, curiosity 0.57, grief 0.50, fear 0.42, anger 0.33, but hunger 0.06 and fatigue 0.08 (p. 3).

### 3.5 Decoding (Q-EXIST analogue)
- "From frozen agents we fit ridge probes (α=20, five-fold cross-validated) mapping the penultimate hidden state ht to each interoceptive cause, giving an emotion direction w_e and an affect matrix B" (§3 "Read-out and manipulation", p. 2).
- Controls: "Every decodability figure is paired with a shuffled-label control (≈ 0) and, for the headline agent probes, a permutation p-value and a bootstrap 95% confidence interval … A property counts only if it beats its control in every seed" (§3 "Controls", p. 3). 10,000 permutations on one representative seed; Bonferroni 0.05/21; "episode-level bootstrap 95% CIs—resampling whole trajectories (120 episodes)" (§4.1, p. 3).
- There is no input/output/action baseline subtraction like our ΔR², and no untrained (random-init) network control for decodability. A random-critic control appears only for the retracted gradient law (§4.13(i), p. 6). A "navigation agent with identical senses but needs irrelevant to its reward decodes the same affect variables as well or better (fear 0.73 vs. 0.80)" (§4.13(ii), p. 6; §4.10, p. 5–6). The authors conclude that decodability is "generic, not affect-specific".

### 3.6 Intervention and lesion (Q-CAUSE analogue), and the random-subspace control
- **Methods statement:** "We test causal use by activation steering (adding αw_e to ht) and by lesioning the affect subspace against a random subspace" (§3, p. 2).
- **Input level:** "holding the external world fixed and flipping only the internal affect input (safety deficit 0 → 0.8) changes the greedy action in 24% of states (95% CI [23, 26]), toward fleeing in the adaptive cases (7% [6, 7])" (§4.11, p. 6), over "N = 22,308 predator-relevant states from 120 episodes, with bootstrap CIs that resample episodes" (p. 6).
- **Hidden level, patching:** "activation patching of the affect subspace induces adaptive fleeing in 9% of states [8, 11] versus 0% [0, 0] for a matched-dimension random subspace (episode-level permutation p = 0.0001)" (§4.11, p. 6).
- **The random-subspace control, in full as stated:** "The hidden-level null is a random subspace of the same dimension—orthonormalised random directions—not one matched on norm or covariance; we therefore claim specificity only relative to dimensionality" (§4.11, p. 6).
  - *Dimension matching:* same dimension as the affect subspace. The subspace's dimension is **not stated**. B has 7 rows (seven emotion directions) spanning "≈ 6.1 effective axes" (§4.9, p. 5), so it is presumably 7, but that is my inference.
  - *Number of random draws:* **not reported**.
  - *Norm/covariance matching:* explicitly **none**.
  - *Sham:* **no sham edit** in our sense, such as an edit along a decodable-but-unused direction or a same-module matched-norm edit judged against the strongest of K. The random subspace is the only hidden-level null. For single-direction steering the comparator is "a random perturbation" (§4.13(iii), p. 7), and that test failed.
  - *What "patching" substitutes* (which donor state is patched in) is **not specified**.
- **Hidden level, lesion:** "lesioning the affect subspace bites only marginally—the code is distributed" (§4.13(iii), p. 7). No numbers, outcome definition or control result are given for the lesion.
- **Single-direction steering:** "Injecting a single fear direction does not change avoidance beyond a random perturbation" (§4.13(iii), p. 7).
- **Compositional edit:** moving fearful states along −w_fear vs "a matched-random move", 1.0 vs 0.4, 3/3 seeds (§4.4, p. 4).

### 3.7 Necessity for viability behaviour (Q-NECESSITY analogue)
- **Necessity claim made, at the input level:** "The robust causality is at the input/interoceptive level (masking: 82% → 10%). The honest statement is that interoceptive information is causally necessary, while causal control through the identified hidden affect directions is specific but weak" (§4.13(iii), p. 7). §5 (p. 7) repeats it: "82% → 10% under masking, which shows interoceptive information is necessary, not that a hidden affect direction is". **The quantity that goes from 82% to 10% is not defined anywhere in the PDF**, so I cannot tell whether it is survival, adaptive fleeing or action agreement.
- **Hidden-level necessity:** the affect-subspace lesion vs a random subspace "bites only marginally" (p. 7), with the outcome unstated.
- **Viability outcome:** no survival or time-in-bounds outcome is reported under any lesion or mask, as far as the text shows. The only survival figure is for the intact hidden-interoception variant ("152/200 steps", §4.2, p. 3).
- **Same-size ablations of other modules:** none. The only size-matched comparator is a random subspace of the same hidden layer, which is a dimension-matched null within one module, not ablations of other functional modules.
- **Matched arms:** none for necessity. The navigation agent is a matched-senses comparison for representation and valuation (§4.8, p. 5), not a necessity arm. There is no external-estimate or bypass arm.
- **Retraining vs frozen:** all interventions are "on a frozen agent" (§4.11, p. 6). Our Q-NECESSITY is also frozen-weight resample ablation (scope v1 §4.4), so this is not a difference.

### 3.8 Pre-registration; SELF-like test
- **Pre-registration: none found.** The PDF has no preregistration, registry or OSF string, and no code or data availability statement.
- **SELF-like test: none.** There is no comparison of the agent's own prediction of its state with an external observer's. Probes are external read-outs.

### 3.9 Verdicts for Asan

**Q-EXIST: EXTENSION.** Asan already decodes interoceptive and affect variables from a learned PPO homeostatic agent's hidden state, with shuffled-label, permutation and episode-bootstrap controls across 3 seeds, and removes input pass-through by hiding interoception. Our Q-EXIST adds:
- the ΔR² over the strongest input/output/action baseline and a Hewitt–Liang control;
- a recurrent allostatic state, where Asan is feedforward and itself says recurrence is needed;
- the RAND-INIT, FF-RELAY and REW-CORR confound rows;
- pre-registration and the Stage-0 gate.

It is not a replication, because the statistic, architecture and controls differ.

**Q-CAUSE: EXTENSION.** Asan edits along decoded directions and patches the decoded subspace against a dimension-matched random subspace in a PPO homeostatic agent, and pre-states a behavioural outcome (adaptive fleeing). Our Q-CAUSE adds:
- a pre-declared δ and margin m_CAUSE;
- the comparator "strongest of K matched-norm random edits in the same module" plus a decodable-but-unused direction;
- the off-manifold and intervention-damage confound rows;
- a recurrent state.

Asan's single-direction steering is the closest test to ours and came out **negative**. Cite that, because it is a prior result that our δ-edit may also fail.

**Q-NECESSITY, D1–D4 against Asan:**

| Difference | Against Asan 2026 | Reason |
|---|---|---|
| D1: the self-model's content is interoceptive | **DOES NOT HOLD** | The lesioned/patched subspace is fit to interoceptive and affective causes (§3, p. 2), and the necessity claim is about "interoceptive information" (§4.13, p. 7). Asan has no separate self-model module; that is a further difference, but not D1. |
| D2: the agent is a learned RL agent | **DOES NOT HOLD** | PPO end-to-end, 3 seeds (§3, p. 2). |
| D3: the outcome is viability | **HOLDS** | Outcomes are greedy-action change and adaptive fleeing in predator states (§4.11), plus an undefined masking percentage (§4.13). No survival or time-in-bounds outcome is reported under lesion. *Caveat:* if the undefined 82% → 10% quantity is a survival measure, D3 would fail for input masking, though input masking is not an ablation of a learned state. |
| D4: same-size ablations of other modules (plus matched arms) | **HOLDS** | Only a dimension-matched random subspace in the same layer, with no norm/covariance matching and unreported draws. No ablations of other modules, no external-estimate arm. |

**Label under the ruling in force: EXTENSION.** Not all four fail. D1 fails, which is the gap case the Lead ruled is also an extension. **The text must name the surviving differences: D3 (viability outcome) and D4 (same-size ablations of other modules, with matched arms including the required external-estimate arm).**

Further differences that are outside D1–D4 and not counted: a separately specified learned interoceptive self-model rather than a probe subspace; a recurrent state; pre-registration; and the Stage-0 gate.

**Effect on the combined Q-NECESSITY label.** v1.2 had Q-NECESSITY as STILL NOVEL AS FAR AS FOUND (narrowed), with D1–D4 all holding against Craggs. Against Asan, D1 and D2 fail. Prior art is cumulative, so **Q-NECESSITY should now read EXTENSION (of Asan 2026; method precedents Wilterson & Graziano 2021, Craggs 2026 Block V), surviving differences D3 and D4.** This is for the Lead to rule. The A3/A4 scope files have not been touched.

### 3.10 Methods to adopt (recommendations only; nothing adopted here)
1. **Do not adopt Asan's random-subspace control as is.** By its own account it matches only dimension (§4.11, p. 6), and the paper reports neither the number of draws nor the patch donor. Our Q-CAUSE/Q-NECESSITY comparators should freeze:
   - matched dimension **and** matched norm;
   - a covariance-matched variant, e.g. random subspaces drawn within the state's own principal subspace, so the null lives on-manifold;
   - K draws with the strongest draw as the comparator;
   - the donor rule for patching or resample-ablation, stated explicitly.
   This is for Astra under AQ-N1 / the margin questions.
2. **Interoception-hidden-from-input arm** (§4.2, p. 3) as a Q-EXIST row against input pass-through. Asan's finding that slowly-accumulating drives are not decodable without memory (hunger 0.06, fatigue 0.08) is a ready-made known-answer for Stage 0: a feedforward planted system should fail to decode a time-integrated E variable, and a recurrent one should succeed.
3. **Needs-irrelevant navigation agent** (§4.8 and §4.10, pp. 5–6) as a matched-senses control for REW-CORR / valuation. Its decodability matched or exceeded the survival agent's, which is direct prior evidence that raw Q-EXIST without the ΔR² baseline would be non-specific.
4. **Episode-level resampling** for bootstraps and permutations (§4.1, p. 3; §6, p. 9). This is consistent with our pooling rules; cite it.
5. **Report Asan's negative results as priors for our confound rows:**
   - single-direction steering no better than random (Q-CAUSE risk);
   - "lesioning the affect subspace bites only marginally—the code is distributed" (Q-NECESSITY risk for a direction-level ablation; supports resample-ablating the whole state);
   - the retracted gradient law matched by a random critic (§4.13(i)), which is a realized confound of exactly the kind our RAND-INIT row targets.

---

## Part 4. Limits
1. **Asan's earlier version** (Zenodo 22791990, v1.0, 16 Sep 2026) was not read. Its PDFs differ in size from the version read (333,643 bytes vs 982,376).
2. **Asan under-reports.** It does not define the 82% → 10% masking quantity, the affect-subspace dimension, the number of random-subspace draws, the patch donor or the lesion results. The D3 verdict carries the caveat in §3.9. No code or data are linked, so none of this can be checked from source.
3. **Akiyama's preregistration** is in Japanese and was read by section and keyword (§4.3, §6, §11), not line by line. The Japanese PDF and the rest of the ZIP were not read.
4. **Bankuti's Hungarian PDF** and the remainder of its package (audits, equivalence reports, code) were not read. The front-matter vs Appendix B publication-status inconsistency is reported as found.
5. **Pre-registration in both Bankuti and Akiyama is internal** (hash chains or seals), not external registries. I did not look for external registrations of either beyond the papers' own statements.
6. **Kulma 2026, García Hernández 2026** and the other v1.2 description-only items remain description-only.
7. **No new searches were run.** This note only reads the three papers named in v1.2.

---

## Footer: inputs and files read (sha256)
- `/workspace/review/trackB_prior_art_verification_v1_2_open_items_CNA.md` (input): 166469154faeccdb9688a4473504f1d160711949b4eb74779bd84ba9a9b7451c
- `/workspace/tmp_pa2/full/bankuti_EN.pdf` (Bankuti 2026, SITC_CAUSAL_ASSAY_v1.0_RC2_EN.pdf): ffb12f5320c140a2c4ffab724fa4509093738cbf1373be03abe845e82d14a049
- `/workspace/tmp_pa2/full/akiyama_EN.pdf` (Akiyama 2026, PAPERC_V1_0_EN.pdf): c080ac1a95bebfacdbe8192dd6b12615b21a211e8bebebb3294557570097a950
- `/workspace/tmp_pa2/full/asan.pdf` (Asan 2026, YUVA_Affect (1).pdf; identical to `/workspace/tmp_pa2/zen/asan.pdf`): 82386e24bcf4fa85843606e5a0dcfeb39d1855528bfdbef473623c560a6caa69
- `/workspace/tmp_pa2/full/bankuti.zip` (SITC_PUBLIC_REPRODUCIBILITY_PACKAGE_v1.0_RC2.zip): 90c158f1c652e0d611052c06e842eec00655c4394ed2abb57e3447d707020c58
  - `protocol/SITC_D2_PREREGISTRATION_v1.0.0.json`: fbecb854eca0e096a2e66e8d047baea2cf466f8872d23202eaa60b946c9d4019
- `/workspace/tmp_pa2/full/akiyama.zip` (paperc-v1.0.zip): 336b5fe987ae4ef985b86b7df2e23c90592c8f9b8be9a70c4fd01d771a94c643
  - `primary/PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md`: 5e19341f30a8b92bc97e177d7b3a25ff01d6f6a13e0c7bc780e4e881278fb0bf
  - `primary/INSTRUMENT0_STAGE1_FIXTURE_RESULT_V1.json`: 5f2d1fd14bd63fc017fcb293f99060cd07198d7a5e03d5bc98406b434bb90ab5
- Zenodo record JSON: `rec_22863692.json` 40151c6bc9c9f8bd315b2a9b380e02f1cca6c1d4571e855e2fa6b48dbdbfac29; `rec_21983630.json` c683217f04636115bc1c099927dafc6109d06663ca2cded08137b0239589418d; `rec_22810742.json` c19e3d9a2edbd29da4557392178948f2e61f7401e34138c3212eac1fc8be9d52 (in `/workspace/tmp_pa2/full/`)
