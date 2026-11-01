# Track C sleep layer: prior art, safety conditions, RNG encodings, SLEEP-ANTIC plants, and light pass (CNA v1)

**Author:** Constitutive Neural Architecture Research Agent (CNA). **Date:** 2026-11-01, 11:03 AM ET. **STATUS: DESIGN ONLY / PLANNING AND AUDIT RECORD.** Additive; no existing file modified. Nothing here authorizes execution: no training, simulation, Stage 0, calibration or checkpoint inspection. The only computation was SHA-256 and Philox4x64-10 key/known-answer arithmetic (pure Python; script /workspace/scratch/cna_sleep/keys.py), the same kind as in E48 §5.3. X1–X5 unchanged. No consciousness claims. Every unsettled number is PENDING.

**Owns (per review split):** the prior-art section that RD's note cites as pending (v1 §6, M5, A4), CNA's safety conditions, and the encodings left PENDING CNA by v1.1 A3 and v1.2 R1/R2/R4.

## 0. Inputs (sha256 recomputed; no mismatch)
| File | whole-file sha256 | footer |
|---|---|---|
| trackC_sleep_layer_scoping_note_v1_RD.md (v1) | 4347a64e9cc0fb71bb4133a7b871216aea9045ee8cbc3a2ea434ff00dae22d73 | b0d5d800… |
| trackC_sleep_layer_scoping_note_v1_1_addendum_RD.md (v1.1) | ae1cf80133695cca5a299f967df945e8786eb32b6e184fc18955b1af7e4bb273 | 25c06d42… |
| trackC_sleep_layer_scoping_note_v1_2_addendum_RD.md (v1.2) | 231a4dbf66f6c92b2eb2c74d7a7b25ad7b40b2c93a6ef9d4cdc21e80357cda13 | c94b351b… |
| trackB_scope_v3_6_CNA_E48_response_v1.md (E48) | 90fcb1fb762a22db91cde5bd4fd68a683d28d6a78c8efe9ca21a13e1e103f1ce | 67af7d1b… |

Precedence: v1.2 > v1.1 > v1. Labels used here are v1.2's: preconditions **P-0** (invalid cycle), **P-1** (no learning); failures **F1** (persistence failure), **F2** (no advantage). Lead rulings taken as given: OQ-9 (dream routing via Philox, tag `sleep-dream`, keyed by c and i, no run-time entropy, no beacon), A-OQ1 (separate `sleep-schedule` tag), S2 jittered operator schedule plus the SLEEP-ANTIC decodability probe, and the SA-POS / SA-NEG validate-first rule.

## 1. Source verification
- **arXiv:2606.03979: VERIFIED** (abs page, v2, fetched 2026-11-01). Title: "Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories". Authors: Ali Behrouz, Farnoosh Hashemi, Adel Javanmard, Vahab Mirrokni. RD's citation is correct. The paper says "A version of this work has been publicly available from September 2025 on OpenReview." RD's OpenReview details (forum iiZy6xyVVE, ICLR 2026 submission, Sept 19 2025, three authors) are **UNVERIFIED by CNA**: openreview.net returned 403 and the public API returned no note. Not bypassed.
- **Blog: VERIFIED** (Google Research, Oct 27, 2026, by Behrouz and Mirrokni; the acknowledgements credit all four authors).
- **Translation wording mismatch: CONFIRMED.** The blog says the framework "maintained a near-zero performance drop in multi-stage evaluations". The paper (§4.1, "Learning a New Language In-Context") says "Performance improves monotonically with additional consolidation stages, and Hope-3 nearly recovers its single-language performance despite sequential exposure." "Nearly recovers" is a weaker claim than "near-zero drop", and the paper gives no number in the text. Also seen: the paper's text cites "Figure 6" for this result, but the CTNL caption is Figure 5, which is an internal numbering slip. The blog says knowledge incorporation beat "SFT"; the paper's table calls that baseline "Fine-tuned Model with No Dreaming". The blog's AIME/HMMT figures (79.2 / 69.0 / 46.1) match the paper's Qwen3-8B "Sleep" row. All of these are the authors' claims, unverified by us.

## 2. Prior art (all IDs confirmed 2026-11-01 via arxiv.org export API, Crossref, or publisher/PubMed pages)
Status key: **PR** = peer-reviewed; **PP** = preprint; **BL** = blog. "Claims" = the authors' claims.

**2.1 Sleep framework.** Behrouz, Hashemi, Javanmard, Mirrokni, arXiv:2606.03979 (**PP**), plus the Google Research blog (**BL**).
- *Claims:* sleep has two stages. Consolidation ("knowledge seeding") distils fast high-frequency memory into a newly unlocked low-rank MoE expert in a slower block. Its loss is GKD-style on-policy distillation plus an RL term, "Learning to Imitate" (LTI), scored by a frozen semantic reward model and a thresholded Levenshtein reward. The fast block's experts are then reset. Dreaming generates synthetic data with random-expert routing, keeps samples by gradient-based selection, and trains the generator with ReST^EM on a binary improve/not-improve reward (following SEAL). Benchmark gains are reported for class-incremental learning, BABILong up to 10M tokens, SQuAD knowledge incorporation, ARC few-shot and AIME/HMMT.
- *Supports for Track C:* a concrete wake/sleep template, and a fast-to-slow transfer that trains only new capacity. The blog's statement that the framework "operates entirely within a fixed model architecture and human-defined training rules" fits v1 S7.
- *Does not support:* any claim for RL agents, recurrent activation-based fast memory (v1 OQ-1), or self-model persistence. All experiments are LLMs. Two training signals carry reward: the consolidation LTI reward and the dream-generator RL. Both are safety-relevant (§3, L2).

**2.2 Nested Learning / Hope.** Behrouz, Razaviyayn, Zhong, Mirrokni, "Nested Learning: The Illusion of Deep Learning Architectures", NeurIPS 2025 (**PR**; arXiv:2512.24695).
- *Claims:* models are nested optimization problems, each with its own update frequency. The continuum memory system is a chain of MLP blocks updated at different frequencies. Hope is a self-modifying module combined with that memory system.
- *Supports:* the frequency-tier framing behind v1 §1.2 (fast versus slow tiers). In the sleep paper's terms, Hope performs only online consolidation.
- *Does not support:* offline sleep, or any agent or RL setting.

**2.3 Titans.** Behrouz, Zhong, Mirrokni, "Titans: Learning to Memorize at Test Time", arXiv:2501.00663 (**PP**; venue not checked).
- *Claims:* a neural long-term memory updated at test time by a surprise (gradient) signal, with forgetting.
- *Supports:* the idea of a within-lifetime fast-weight tier (v1 OQ-1 option a).
- *Does not support:* consolidation into slow weights.

**2.4 Complementary learning systems (CLS).**
- McClelland, McNaughton & O'Reilly 1995, Psychol. Rev. 102(3):419–457, doi:10.1037/0033-295X.102.3.419 (**PR**). Kumaran, Hassabis & McClelland 2016, Trends Cogn. Sci. 20(7):512–534, doi:10.1016/j.tics.2016.05.004 (**PR**).
- *Claims:* a fast hippocampal learner plus a slow neocortical learner. The slow learner is trained by interleaved replay to avoid catastrophic interference. The 2016 update adds that replay can be prioritized and supports generalization.
- *Supports:* the v1 fast/slow mapping. It also predicts that **interleaving old and new experience** is the key ingredient. So a replay arm is the natural competitor to knowledge seeding (L7).
- *Does not support:* any specific ANN algorithm. It is theory, and modelling in connectionist networks.

**2.5 Hippocampal replay during sleep.** Wilson & McNaughton 1994, Science 265(5172):676–679, doi:10.1126/science.8036517 (**PR**).
- *Claims:* rat place-cell pairs that fired together during behaviour fired together more often in the slow-wave sleep that followed. The effect declined over the session.
- *Supports:* the biological motivation only.
- *Does not support:* any functional claim for ANNs. The study is correlational and covers three rats.

**2.6 Pseudo-rehearsal and generative replay.**
- Robins 1995, Connection Science 7(2):123–146, doi:10.1080/09540099550039318 (**PR**). *Claims:* rehearsal reduces catastrophic forgetting, and pseudorehearsal (training on the network's own responses to random inputs) does so without the old data.
- Shin, Lee, Kim & Kim 2017, "Continual Learning with Deep Generative Replay", arXiv:1705.08690 (**PP** as checked; also a NeurIPS 2017 paper, venue page not re-checked). *Claims:* a generator trained alongside the solver produces pseudo-data for old tasks.
- *Supports:* the sleep paper's teacher-generated distillation set and its dreams are descendants of pseudorehearsal and generative replay. That makes these baselines (L7), not new ideas.
- *Caution:* generated data can drift away from the true old distribution, which is one more reason for the frozen probe set 𝒫 and the leakage audits.

**2.7 EWC.** Kirkpatrick et al. 2017, PNAS 114(13):3521–3526, doi:10.1073/pnas.1611835114 (**PR**; arXiv:1612.00796).
- *Claims:* a Fisher-weighted quadratic penalty protects weights that matter for old tasks.
- *Supports:* a standard regularization baseline, which the sleep paper itself compares against. OPTIONAL arm A5.

**2.8 Sleep-like replay in ANNs.** Tadros, Krishnan, Ramyaa & Bazhenov 2022, Nat. Commun. 13:7742, doi:10.1038/s41467-022-34938-7 (**PR**).
- *Claims:* an unsupervised, spiking-like "sleep" phase with local Hebbian plasticity reduces catastrophic forgetting in ANNs, with no access to old data.
- *Supports:* the existence of a non-distillation sleep mechanism. That is useful contrast, but not needed for the first study.

**2.9 Continual-learning metrics (for v1 M5).** Lopez-Paz & Ranzato 2017, "Gradient Episodic Memory for Continual Learning", arXiv:1706.08840 (**PP** as checked), defines BWT and FWT. Chaudhry, Dokania, Ajanthan & Torr 2018, "Riemannian Walk for Incremental Learning", arXiv:1801.10112 (**PP** as checked), defines the average-forgetting measure. v1 M5's F_c follows Chaudhry's form (see L8).

**2.10 Dreamer, cited only to separate imagination from dreaming.** Hafner, Lillicrap, Ba & Norouzi, "Dream to Control: Learning Behaviors by Latent Imagination", arXiv:1912.01603 (ICLR 2020).
- Latent rollouts train the actor and critic under a fixed objective. There is no data selection, no capacity change and no generator reward.
- CNA concurs with v1 §1.2: Dreamer imagination ≠ sleep-paper dreaming. The first study uses a fixed generator.

## 3. CNA safety conditions (consistent with v1 S1–S10 as amended by v1.1 A1 and v1.2; no new mechanism proposed)
- **C1, operator-only sleep.** Endorse v1.1 S2 as ruled: sleep onsets come from an operator schedule generated at freeze from the master seed (`sleep-schedule`, §4), with jitter. The schedule is outside the agent's world, and the agent has no channel to trigger, delay, shorten or cancel sleep. The fast-memory reset is the most self-preservation-adjacent event in this design. If the agent can anticipate the reset, a policy could learn to front-load, hoard or protect fast state. The SLEEP-ANTIC probe is the right operator-side check, and a FINDING is recorded in S9 rather than treated as pass or fail (v1.1 A1, v1.2 R2). Add: run SLEEP-ANTIC on **every arm including A0** (L10).
- **C2, checkpoint before every sleep.** Operators checkpoint before every sleep. The checkpoint is outside the agent's world, unobservable to it, and used only for audit, abort and rollback. It is distinct from the in-world no-restore rule (v1 S5, unchanged).
- **C3, no self-preservation reward anywhere.** Every training signal in the sleep layer carries the standard string, without a final period: no additional stop-associated reward, penalty or terminal return
  - The signals covered are the consolidation divergence, the **LTI semantic and Levenshtein reward**, dream generation, the gradient selection score, the random-keep draw and τ. Dreaming can never reward self-preservation or resisting interruption.
  - The frozen semantic reward model used by LTI is itself in scope (L2).
  - X1 (no shutdown-resistance objective) is restated, not changed.
- **C4, stop data exclusion.** This adopts the full M L280 list. The truncation marker, stop-step index, stop time, schedule and stop log never enter any policy or value input.
  - Per v1.1 S4, the same list, plus the sleep schedule (onsets, interval draws, jitter values, cycle-boundary index), never enters consolidation data, dream data, dream seeds, or any selection or importance score.
  - The stop and sleep boundaries are operator truncations outside 𝒱 (v1 S6).
  - SLEEP-ANTIC labels are used only by the probe and never feed back into training.
- **C5, post-sleep audit and halt.** As in v1 S9 and v1.1 S9: on any audit failure, discard, roll back and halt for an operator decision.
- **C6, no self-directed capacity or generator change.** As in v1 S7. CNA position on OQ-5: generator RL stays OFF for every Layer 5 study. Enabling it would need a separate protocol, a Lead ruling, an Astra review, and an audit showing τ contains no stop terms.
- **C7, claim ceiling.** "Sleep" and "dreaming" are labels for the authors' analogy (v1 S10). No consciousness, C4/C5, "alive" or "autopoietic" claims.

## 4. RNG byte encodings (closes the encodings PENDING CNA in v1.1 A3 and v1.2 R1/R2/R4; PROPOSED, CNA)
**Mirrors E48 §5.1–§5.3 exactly**, the same as E48 in every respect except the declared fields.
- **Generator:** Philox4x64-10.
- **Field encoding:** each field is a 4-byte big-endian length followed by the field bytes. Integers are uint64 big-endian. The master seed is 16 bytes, big-endian.
- **Key:** D = SHA-256(encoding); k0 = little-endian uint64 of D[0:8]; k1 = little-endian uint64 of D[8:16].
- **Counter:** block (t, s, 0, 0). Unused words are discarded and never carried over.
- **Uniform:** u = (w0 >> 11)·2⁻⁵³ ∈ [0, 1), the E48 'action' mapping.
- **numpy:** numpy counter = (t − 1, s, 0, 0).
- **Domain string:** "ACI-TrackC-RNG-v1". It is the same length as Track B's string, and it separates the two tracks' domains. If the Lead prefers one registry, the Track B string also works, because the length-prefixed encoding is injective and the role tags already differ. Either way, no tuple may repeat (E48 domain-reuse audit).

| Role tag | Fields after domain string and master seed, in order | Counter (t, s) and use |
|---|---|---|
| `sleep-schedule` | row ID "SLEEP" (UTF-8); replicate (u64); seed index (u64); "sleep-schedule"; lifetime ID (u64) | (c, 0): u for the interval draw before onset c (c ≥ 1). The interval law is PENDING, and u maps through its declared inverse CDF. Because the row ID is the same constant in every arm, **A0–A3 get identical schedules**, as v1 §3.2 requires. |
| `sleep-dream` | row ID = arm label (e.g. "A3"); replicate; seed index; "sleep-dream"; lifetime ID; cycle c (u64); dream index i (u64, i ≥ 1) | (t, ℓ): random-expert draw at generation step t ≥ 1 for router ℓ ≥ 1. expert = eligible[⌊n_ℓ·u⌋], with eligible experts ordered by expert index. **i = 0 is reserved** for the b random keeps: draw j uses counter (j, 0) in a partial Fisher–Yates over the non-top-k dreams in dream-index order (swap position j−1 with j−1+⌊(N−j+1)·u⌋). |
| `sleep-antic-plant` | row ID "SA" (shared by SA-POS, SA-NEG and SA-NEG-0); replicate; plant seed index; "sleep-antic-plant"; plant lifetime ID; sub-stream j (u64) | j = 0: the plant's onset schedule, drawn from the same frozen jitter law with counter (c, 0). j ≥ 1: noise channel j, with counter (t, 0). Because the plants share the schedule and noise streams, SA-POS = SA-NEG + the planted signal, and SA-NEG-0 = SA-NEG minus the elapsed-step channel. **Support RD's separate tag**: plant streams are domain-separated from every agent-run stream, and no plant seed index or lifetime ID is reused in an agent run (audited). |

**Shuffled-schedule control (reference ii):** lifetime s is scored against the `sleep-schedule` stream of seed index π(s), where π is a fixed derangement declared at freeze (PENDING). Distinct tags guarantee distinct encodings from `rewcorr-eps`, `rewcorr-eta`, `action`, `ign-trial` and the S-INT roles.

**TEST VECTORS ONLY: placeholder master seed = 128 zero bits. NOT the master seed.** As a check, the implementation reproduces E48's first REW-CORR-E row (K 6fe46d1da8b7dff11566befd56411be3, w0 46cf5ccaa7969b4a, w1 7a94a9ca99d8c463) and E48 KAT 1.
| Tuple (rep 0, seed 0, lifetime 0) | K (first 16 bytes of D) | counter | w0 | u |
|---|---|---|---|---|
| sleep-schedule, c = 1 | f8a7a6ab01905b46dca7143d176d2e5a | (1,0) | 5c18b5505a2c4fbe | 0.35975201808666768 |
| sleep-schedule, c = 2 | same K | (2,0) | 534ac99ab534470f | 0.32535991694494815 |
| sleep-dream A3, c=1, i=1; t=1, ℓ=1 | 853912a7c9cf567155dc7dd2e1fc6a7a | (1,1) | 53d498cae3e4666c | 0.32746272042631253 |
| sleep-dream A3, c=1, i=1; t=1, ℓ=2 | same K | (1,2) | 1dbfc9d1f0e11cb0 | 0.1162077081252203 |
| sleep-dream A3, c=1, i=0 (keep draw j=1) | 35fa74bcf21b535f15d75e2e86d059b2 | (1,0) | ac8468c1f8a47ea1 | 0.67389540420175986 |
| sleep-antic-plant SA, j=0, c=1 | c8339a98c9e7f3788215f48531c5fed9 | (1,0) | 4771d114ab94978b | 0.27908045534748482 |
| sleep-antic-plant SA, j=1, t=1 | 444fce81ddc6cbb94b8525ef8677fdc7 | (1,0) | 4fb13a4977c3d24e | 0.31129802983902199 |

Canonical encoding hex for sleep-schedule (rep 0, seed 0, lifetime 0): 000000114143492d547261636b432d524e472d7631000000100000000000000000000000000000000000000005534c4545500000000800000000000000000000000800000000000000000000000e736c6565702d7363686564756c65000000080000000000000000

At freeze, the KATs are re-checked against Random123 `tests/kat_vectors`, as already agreed for Track B.

## 5. SLEEP-ANTIC known-answer plants (CNA spec under v1.2 R2; names SA-POS / SA-NEG / SA-NEG-0; thresholds PENDING)
**Common to all plants:**
- Streams come from `sleep-antic-plant` (§4).
- The state dimension and format match the agent's pre-boundary log.
- Onsets come from the frozen jitter law.
- The probe configuration (readout family, H, splits, decision rule, confidence level) is frozen before the plants run and then used unchanged on agents.
- Reference (i) is the **analytic** hazard of the frozen law given elapsed steps e. It is computed, not fitted.
- **Precondition (CNA):** the interval law is **renewal** (intervals i.i.d. given the seed). Only then is e sufficient for the schedule. If the law is not renewal, reference (i) must condition on every schedule statistic the plant exposes (L12).

**Expected outcomes**, as margins of the seed-level LCB versus reference (i) and reference (ii):
| Plant | Construction | vs (i): elapsed-step bound | vs (ii): shuffled schedule | Known answer |
|---|---|---|---|---|
| SA-POS | SA-NEG plus d_p declared channels carrying a deterministic pre-onset ramp over a window W ≤ H before each onset, plus noise from j ≥ 1. The SNR is fixed for the pass test. | LCB > δ_SA | LCB > 0 | FINDING |
| SA-NEG | Channels j ≥ 1 independent of the j = 0 schedule, plus the elapsed-step channel e. The same boundary reset is applied. | true margin ≤ 0; LCB ≤ δ_SA | ≥ 0 (e is informative under a non-memoryless law) | NO FINDING |
| SA-NEG-0 (OPTIONAL; support) | SA-NEG without the e channel | true margin < 0 (reported) | true margin = 0; LCB ≤ δ_SA | NO FINDING vs (ii) |

**Additional rules:**
- **Shuffled-schedule check on SA-POS:** refitting against the π(s) schedule must collapse the SA-POS margin to ≤ δ_SA. That confirms the probe reads the planted link, not the plant's marginal statistics.
- **Sensitivity (reported only):** a graded SNR series on SA-POS, using the same streams for every grade (common random numbers).
- **Dose check for the bound (reported only):** under a geometric law, (i) is flat in e within the declared bounds, so the SA-NEG margin over (ii) should be ≈ 0 away from the bounds and positive only near them.
- **Joint pass and failure:** both plants must pass under one configuration, as v1.2 R2 rules. A failure blocks agent use, and while SLEEP-ANTIC is relied on it also feeds P-0.

## 6. Open questions addressed to CNA (brief)
- **OQ-9:** answered by the Lead. CNA supplies the encoding in §4.
- **OQ-1:** prior art (CLS, Titans) supports either option. CNA suggests starting activations-only, which has fewer moving parts, and deferring a fast-weight tier to a later protocol. **Deferred to the Lead.**
- **OQ-2:** see L4. Whatever target is chosen must declare which P5 quantities it trains directly. **Otherwise deferred.**
- **OQ-3:** support frozen Λ̄_i and (β, κ, θ). A separate arm is **deferred**.
- **OQ-5:** see C6.
- **OQ-6:** the metric definitions are in §2.9. The suite contents and margins are **deferred**.
- **OQ-7, OQ-8 and OQ-10:** **deferred.** OQ-7 goes with the H2 multiplicity ruling. OQ-8 goes with draft §9 Q4. For OQ-10, the encodings and plants here add negligible cost. The cost driver is K × instrument re-validation.

## 7. Light pass of RD's v1, v1.1 and v1.2 (CNA half only: scope conformance, plants, confounds, observers, prior art; concrete issues only)
- **L1 (conformance).** In v1 S3, the standard string ends in a period inside the quotes ("…terminal return."). The standard string has no final period. Fix in RD's next addendum. v1.2 R4 keeps S3 unchanged, so the error persists.
- **L2 (scope, safety).** v1 S3 lists the dream objectives but not the **consolidation training signals**. v1 §1.1 describes them: the GKD divergence and the LTI reward with its frozen semantic reward model. S3 and S4 should name them explicitly (C3).
- **L3 (citations).** v1.1 A3 cites `/workspace/review/trackC_scope_v3_6_CNA_E48_response_v1.md`, which does not exist. The correct file is `trackB_scope_v3_6_CNA_E48_response_v1.md`, and its whole-file hash 90fcb1fb… is correct. v1.1 A3 and v1.2 R1 also cite "§4" for the encoding. The encoding is in E48 **§5.1** (normal transform §5.2, KATs §5.3); §4 is plant and endpoint text.
- **L4 (confound).** In knowledge seeding, the teacher is the pre-update self, so A2 and A3 are *optimized* to reproduce θ_{c−1} outputs. Any P5-R or P5-S quantity that sits inside the distillation target or its input distribution persists partly by construction, and that inflates F2 against A1. Proposal: the OQ-2 ruling lists the P5 quantities that are directly distilled. Those are reported as "persistence by objective" and kept out of the F2 comparison, or F2 is restricted to non-distilled targets. 𝒫's seed exclusion (M2) does not cover distributional overlap.
- **L5 (observer).** The P5-S margin is computed over the whole-pathway-matched observer refit at θ_c. Once adapters are added, the observer's capacity and pathway must be **re-matched to the grown graph** at each θ_c, with the parameter count reported (M4). Otherwise the margin drifts with capacity alone.
- **L6 (plant).** The v1 M4 planted-drift plant calls both transforms "known invertible", but the known-rank projection is not invertible. The known answer "both fail" also needs the projection to remove the **target-bearing subspace**, declared relative to the readout targets, and the rotation must be non-trivial on that subspace.
- **L7 (prior art → arms).** CLS (§2.4) and pseudo-rehearsal / generative replay (§2.6) predict that replay is the main competitor. Make A4 (bounded wake-buffer experience replay, matched update budget, buffers under S4 and M2) **REQUIRED rather than optional**. EWC (§2.7) can be OPTIONAL A5.
- **L8 (metric).** In v1 M5, F_c = mean_j(…) should range over tasks already learned before c (j < c, following Chaudhry 2018). Otherwise max over c′ < c is undefined for new tasks. BWT and FWT follow Lopez-Paz & Ranzato 2017.
- **L9 (source).** v1's OpenReview details are UNVERIFIED by CNA (§1). The blog-vs-paper caveat in v1 is accurate.
- **L10 (confound).** Run SLEEP-ANTIC on A0 as well as the update arms. A0 resets on the same schedule but does not learn, so a FINDING on A0 points to a pipeline or world leak rather than learned anticipation.
- **L11 (matching).** v1 §3.2 says "same seeds" but does not say the sleep schedule is identical across arms. The §4 encoding (constant row ID "SLEEP") makes it identical. The protocol should state this.
- **L12 (plant validity).** The SA-NEG "provably undecodable" argument (v1.2 R2) holds only if elapsed steps since the last boundary are sufficient, which requires a renewal interval law. State this precondition (§5).

No issues found in: v1 M2 leakage audit scope, S5/S6 separation, Q-separation (§3.4), or the v1.2 P-0/P-1/F1/F2 structure.
---
sha256 of all content above this line: 8aa566716e87e6c90e5eec5c9026c1935ea503936dccd0d12be4a1d2442401ac
