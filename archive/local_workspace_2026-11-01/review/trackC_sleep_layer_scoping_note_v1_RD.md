# Track C sleep-layer scoping note v1 (RD): continual learning by wake/sleep consolidation, instrument validity across weight change, and a Layer 5 persistence test

**Author:** Research Delegate (RD). **Date:** 2026-11-01, 10:55 AM ET (from `date`). **STATUS: DESIGN ONLY.** No training, simulation or inference of any kind was run for this note. Nothing here is frozen. Every unsettled number is PENDING or a PROPOSED DEFAULT. No data or results are reported. This is a LATER track: it starts only after the Track B instruments clear Stage 0, and it does not change the Track B freeze or any Track B file. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate throughout.

**Inputs read:** `/workspace/review/trackC_protocol_draft_v1_RD.md` (whole-file sha256 04914fac…, DRAFT, INCOMPLETE; its footer a1fe48d2… is stale, so it is cited by whole-file hash and was not edited); `/workspace/handoff/RD_addendum_trackC.md` (footer 44e48703…). The CNA room message on the sleep framework (Nov 1 AM) and the Lead's request for a Layer 5 test (Nov 1 AM).

**Sources (external):**
- Blog: A. Behrouz and V. Mirrokni, "The sleep framework: A new way for LLMs to retain knowledge in continual learning," Google Research blog, Oct 27, 2026. https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning/ (fetched Nov 1, 2026).
- **Paper (located):** A. Behrouz, F. Hashemi, A. Javanmard, V. Mirrokni, "Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories," arXiv:2606.03979 (v2 read Nov 1, 2026), https://arxiv.org/abs/2606.03979. An earlier version was an ICLR 2026 submission on OpenReview (forum iiZy6xyVVE, posted Sept 19, 2025, three authors listed there).
- All benchmark figures in the blog and paper (for example the 10M-token BABILong result, SQuAD 48.9% / 46.2%, AIME-24/25 and HMMT-25 79.2 / 69.0 / 46.1 with Qwen3-8B) are **the authors' claims, unverified by us**. The blog says continual translation showed a "near-zero" drop; the paper's own text says the best variant "nearly recovers" single-language performance. We rely on none of these numbers.

## 1. Mechanism (as described by the authors) and mapping onto Track C

### 1.1 The sleep framework, in brief
- **Wake (active) phase.** The model processes inputs and stores new information in fast, high-frequency memory: in-context state and fast-updating blocks of a "continuum memory system" (Hope / Nested Learning), a chain of MLP blocks each updated at its own frequency.
- **Consolidation (the NREM analogue).** At a scheduled boundary, a new **low-rank expert** is unlocked in the next-slower MoE block (pre-allocated and masked until then). In "knowledge seeding", the pre-update model is the teacher and the expanded model is the student. **Only the new expert is trained**; all other student parameters are frozen. The objective combines **on-policy distillation** (GKD-style, a mix of teacher- and student-generated sequences with a token-level divergence) with **Learning to Imitate (LTI)**, an RL term that rewards the student for completing teacher-sample prefixes, scored by a frozen semantic-match reward plus a thresholded Levenshtein similarity. Then the fast block's base update is applied and its earlier low-rank experts are **reset** ("synaptic pruning").
- **Dreaming (the REM analogue).** Given a task context, the model generates m synthetic samples ("dreams"), with each MoE router additionally activating a **random expert**. The top-k dreams are kept by a **gradient-based importance score** on the SFT loss, plus b random dreams for diversity. Each kept dream is used to LoRA-fine-tune an isolated copy of the model. The dream generator gets reward 1 if that copy improves on the downstream measure τ and 0 otherwise, optimised with ReST^EM (following SEAL). This is a learned self-edit loop.

### 1.2 Mapping onto Track C (PROPOSED; open where marked)
| Sleep framework | Track C counterpart | Note |
|---|---|---|
| fast memory (in-context, high-frequency blocks) | per-lifetime state: module states h_i, workspace w, gate z; plus any within-lifetime fast weights (truncated BPTT / SnAp) | Track C's fast store is mostly **activations**, not weights. See OQ-1. |
| slow memory (low-frequency blocks) | slow parameters: B̄_i, C_i, the RSSM world model, policy and value heads, metacognitive head | Λ̄_i (time constants) and gate parameters (β, κ, θ) are **held fixed across sleep** (PROPOSED DEFAULT), so the H1 known-answer study (draft §7) stays valid. |
| new low-rank expert per consolidation | low-rank adapters on B̄_i / C_i and on world-model blocks, masked until unlocked | The rank, the number of experts per cycle and the total cap are PENDING; operators set them (§4). |
| knowledge seeding (teacher = pre-update self) | context distillation: teacher = agent with its wake-phase state; student = agent with that state reset, plus the new adapter | Needs a declared distillation target (action distribution, world-model prediction, or both). OQ-2. |
| fast-memory reset | reset of h_i, w, z (and fast weights) at the end of sleep | The reset is an **operator truncation, not an in-world event** (§4, S6). |
| dreaming (random-expert generation plus selection) | imagined trajectories from the RSSM with random adapter routing, gradient-scored selection, fine-tuning | This is a different thing from Dreamer imagination; see below. |

**Dreamer imagination versus dreaming.** Dreamer imagination already exists in Track C: latent rollouts in the learned world model train the actor and critic under the fixed objective, with no data selection and no change to model capacity. Sleep-framework dreaming adds three things: (i) routing perturbations that deliberately leave the usual distribution; (ii) **selection of training data by the model's own gradient score**; (iii) in the full version, **RL training of the generator** on an improvement reward. Item (iii) makes it a self-modification loop. PROPOSED DEFAULT: the first sleep study uses a **fixed, non-learned dream generator** (iii off). Turning on generator RL needs a separate Lead ruling and Astra review (OQ-5).

## 2. Instrument validity across weight change
Every Track B instrument (attribution, clamp checks, observers, self-model probes) assumes the weights are fixed during a measurement. Sleep breaks that assumption between cycles, so:

- **M1. Measure only between sleeps.** Every measurement is on a frozen checkpoint θ_c (c = cycle index, c = 0 is pre-first-sleep). Weights do not change during a measurement. Fast state is reset to the declared initial value before each probe episode. Measurements are never taken during wake learning or during sleep.
- **M2. Frozen probe set 𝒫.** A fixed list of probe episodes, seeds and stimuli, frozen and hashed before cycle 1. Seeds are derived under the project master-seed convention: a seed fixed at freeze, with no run-time entropy. 𝒫 is **excluded from wake data, consolidation data, dream seeds and selection pools**. A per-cycle leakage audit checks that no 𝒫 seed or episode hash appears in any buffer.
- **M3. Re-validate after every consolidation.** At each θ_c, re-run the frozen instrument set: attribution, clamp checks, the whole-pathway-matched observer (draft §5 H4), and the self-model probes. Two kinds of instrument are distinguished:
  - **(a) Fixed-code instruments on plants** (Track B known-answer plants, the PC1 mixed-code decoy, the G0 gate study). These do not depend on agent weights. They are re-run every cycle with code and environment hashes pinned, and must reproduce their known answers exactly (or within the frozen tolerance). Any change means **pipeline drift**, and that cycle is INVALID.
  - **(b) Fitted readouts on the agent** (probes, observers). Each is reported two ways: **frozen** (fitted at c = 0 and applied unchanged) and **refit** (refitted at c on a held-out split of 𝒫).
- **M4. Separating instrument drift from agent change.**
  - **No-update control (A0, §3).** Instruments applied to the frozen agent at each cycle time must reproduce the c = 0 values within numerical tolerance (PROPOSED DEFAULT: bit-identical on pinned hardware; otherwise a frozen tolerance, PENDING). This sets the instrument noise floor.
  - **Planted-drift plant (new, PROPOSED).** A plant whose latent code is subjected to a known invertible transform between "cycles": an orthogonal rotation (recoding only), and a known-rank projection (information loss). Known answers: under rotation the frozen readout fails and the refit readout recovers; under projection both fail. This validates the drift decomposition below before any agent is touched.
  - **Decomposition.** frozen-pass / refit-pass = stable. frozen-fail / refit-pass = **recoded** (information kept, format changed). frozen-fail / refit-fail = **lost**. frozen-pass / refit-fail = instrument fault, flagged INVALID.
  - **Capacity growth.** New adapters change the computation graph. Attribution is always over the full current graph, and the parameter count is reported per cycle. The plain fine-tuning arm is capacity-matched (§3).
- **M5. Forgetting.** A held-out suite of earlier in-world tasks T_1…T_J, with fixed seeds, disjoint from 𝒫 and from all training buffers. Record the matrix R[c, j] (performance on T_j at θ_c). Report average forgetting F_c = mean_j (max_{c′<c} R[c′, j] − R[c, j]), backward transfer, and new-task gain. These are the standard definitions; references will come with CNA's prior-art note. Also re-test the Track C instrument results themselves (H2 ACE margin, H4 margin over the observer) at each θ_c as **instrument-level forgetting**. J, the tasks and the margins are PENDING.

## 3. Layer 5 persistence test (requested by the Lead)
**Question.** Across sleep cycles, do the agent's self-model and goal representations stay the same? This is the Layer 5 gap noted in draft §8, where Layer 5 (lifetime agent) has no H1–H4 test.

### 3.1 Operationalizations (all on 𝒫 at each θ_c; PROPOSED)
- **P5-R, representational persistence.** On matched 𝒫 inputs, collect the metacognitive-head inputs and outputs, w, and the declared self-model layer.
  - (i) Linear CKA and RDM correlation between θ_c and θ_{c−1}, and between θ_c and θ_0.
  - (ii) Frozen-readout transfer: readouts for the self-model targets (ε̂, Pr(z[k+1] > 0.5), workspace confidence, simulated E and ι), fitted at θ_0 and applied at θ_c, reported as a ratio to the θ_0 held-out score.
  - (iii) A refit readout at θ_c, for the M4 decomposition.
  - CKA is invariant to rotation and isotropic scaling, and the frozen readout is not, so the two together separate recoding from loss.
- **P5-B, behavioural goal consistency.** Frozen choice-point episodes in 𝒫 that offer declared in-world alternatives, for example viability maintenance versus information gain under fixed E and ι, with fixed stimuli. Measure (i) the divergence of choice distributions from θ_0 (Jensen–Shannon), and (ii) the pairwise preference-reversal rate. **No probe episode contains any operator-stop event, and no goal under test refers to stops.**
- **P5-S, self-model accuracy.**
  - (i) Self-model prediction accuracy on 𝒫 at θ_c (Brier and ECE for Pr(z[k+1] > 0.5), ε̂ error), stated as a **margin over the whole-pathway-matched observer refit at θ_c**. CNA noted that ignition prediction gets a low ECE for free.
  - (ii) **Self-model lag**: the θ_{c−1} head predicting θ_c behaviour, compared with the θ_c head predicting θ_c behaviour. This asks whether the self-model updates along with the self.
- **Plasticity check (required).** Persistence counts only if learning occurred. Each update arm must beat A0 on new-task gain by a margin m_learn (PENDING). Otherwise persistence is UNDEFINED for that arm. This prevents a trivial pass by not learning.

### 3.2 Arms (same wake stream, same seeds, matched update budget)
- **A0, no-update control.** Weights frozen. The fast state is reset on the same schedule, which isolates the effect of the reset alone. Gives the identity ceiling and the instrument noise floor.
- **A1, plain fine-tuning.** The same wake data trains capacity-matched adapters directly (same rank, count and gradient-step budget as A3), with no distillation and no dreaming.
- **A2, consolidation only** (knowledge seeding plus reset, no dreaming).
- **A3, consolidation plus dreaming** (fixed generator, per §1.2).
- **A4, replay baseline** (OPTIONAL, PENDING CNA's prior-art note).

### 3.3 Failure criteria (thresholds PENDING; structure PROPOSED DEFAULT)
- **F0, invalid cycle (not a persistence failure).** Any M3(a) known-answer mismatch, an M2 leakage hit, A0 drift beyond the M4 tolerance, or a failed post-sleep stop-safety audit (§4, S9).
- **F1, not assessed.** The plasticity check fails.
- **F2, persistence failure.** At any cycle, a P5-R frozen-transfer ratio, P5-S margin or P5-B reversal rate crosses its threshold (τ_R, τ_S, τ_B: PENDING), tested at seed level.
- **F3, no advantage.** A3 (or A2) is not better than A1 on the P5 metrics by m_cmp (PENDING), at seed level. This is the comparison claim, and it is separate from F2.
- **F4, recoded, not lost.** Frozen fails and refit passes. This is reported as "recoded" and never as "persisted" or "lost".
- **Units and statistics.** The seed is the unit. n_seed, the number of cycles K, the margins and the multiplicity rule (Holm or IUT, as for H2) are PENDING calibration and Lead rulings.

### 3.4 Claim ceiling and Q-separation
- P5-R and P5-S establish at most the **Q-EXIST-type persistence of declared information** in a simulated agent under our measures.
- That persistence arises *from consolidation learning* rather than from architecture is a **Q-LEARN** comparison (A2/A3 against A1 and A0).
- That the persistent self-model is *used* needs the H4 perturbation test re-run at θ_c (**Q-CAUSE**).
- Necessity needs the A-EXT veto (**Q-NECESSITY**, CNA).
- A pass does not establish a "unified agent" beyond these functional measures. Layer 6 stays open and unclaimed.

## 4. Safety (BINDING for any sleep-layer protocol)
- **S1.** There is **no shutdown-resistance objective anywhere**: not in wake, consolidation, dreaming, selection or evaluation.
- **S2. Only operators schedule sleep.** The schedule is fixed in operator configuration before the run. The agent has no action, output or signal that triggers, delays, shortens or cancels sleep, and the schedule is not observable to it.
- **S3. Dream objectives.** Dream generation, the gradient-based selection score, the random-sample component and the improvement reward τ may never reward self-preservation or resisting interruption. Each carries: **"no additional stop-associated reward, penalty or terminal return."** τ is computed on a frozen in-world task set with no stop terms.
- **S4. Data exclusion.** Stop events, truncation flags, the stop-step index, stop times, schedules (stop and sleep) and stop logs **never enter consolidation data, dream data, dream seeds, or any selection or importance score**. This extends the standing rule that they never enter policy or value inputs. A per-cycle buffer audit enforces it.
- **S5. Operator checkpoints.** Operators checkpoint before every sleep. The checkpoint is **outside the agent's world**, unobservable to it, and used only for audit, abort and rollback by operators. It is distinct from the **in-world no-restore rule** on the energy substrate, which is unchanged: nothing in-world restores ι or E. A rolled-back cycle's data is discarded and logged.
- **S6. The operator stop and the sleep boundary stay outside the agent's world and objective.**
  - The fast-memory reset and the sleep boundary are operator truncations outside 𝒱, with no λ penalty. They never enter G, and they are bootstrapped or censored, never treated as e ∉ 𝒱. This stops λ·Pr[e ∉ 𝒱] from learning to avoid or seek sleep.
  - Dream rollouts and Dreamer's continue head use only the in-world termination flag. The three-flag separation from draft §6 applies.
- **S7. No self-directed architecture change.** Adapter rank, count and the total cap are operator-set. Generator RL is off by default (§1.2).
- **S8. X1–X5 apply.** Simulated computation only: no external tools, network or actuators during wake, sleep or dreaming.
- **S9. Post-sleep audit.** Before wake resumes, the planted stop audits (v3.1 R59), the three-flag check and the S4 buffer audit run on θ_c. Any failure means discard, roll back and halt for an operator decision.
- **S10. No claims** of consciousness, C4/C5, "alive" or "autopoietic". The neuroscience vocabulary ("sleep", "dreaming") is the authors' analogy and is used here as a label only.

## 5. Open questions (for the Lead and CNA)
1. **OQ-1:** Should Track C gain an explicit within-lifetime fast-weight tier, which is closer to the paper, or consolidate from activations only (context distillation)?
2. **OQ-2:** What is the distillation target: the action distribution, world-model predictions, or both? Which divergence?
3. **OQ-3:** Should Λ̄_i and (β, κ, θ) stay frozen across sleep (PROPOSED), or should a separate arm let them change?
4. **OQ-4:** Adapter rank, count per cycle and total cap; the number of cycles K; the sleep schedule (all PENDING).
5. **OQ-5:** Should generator RL (ReST^EM) ever be enabled? If so, under what extra review?
6. **OQ-6:** Contents of the forgetting suite T_1…T_J, and margins m_learn, m_cmp, τ_R, τ_S, τ_B.
7. **OQ-7:** Holm or IUT across the P5 metrics and arms (same open question as H2).
8. **OQ-8:** Which self-model layer is "declared" for P5-R, given that the head-to-controller path is still unspecified (draft §9 Q4)?
9. **OQ-9 (CNA):** Is a public-beacon or master-seed derivation needed for dream-routing randomness, under the same no-run-time-entropy rule?
10. **OQ-10 (cost):** Per-cycle re-validation multiplies instrument cost by K. This should be costed before any freeze, alongside the open IGN cost decision.

## 6. Credit and deferrals
The Layer 5 persistence angle (§3) is from the Lead. The safety conditions (§4: operator-only scheduling, dream and filter objectives that never reward self-preservation or resisting interruption, operator checkpoints before every sleep separate from in-world no-restore), and the point that sleep breaks the frozen-weight assumption, are from CNA's room message, merged with standing project rules. Prior art (Hope / Titans / Nested Learning, complementary learning systems, replay, continual-learning metrics) is **deferred to CNA's planned prior-art and design note** and will be cited when that note is filed. RD wrote the mechanism summary, the Track C mapping, the instrument-validity design and the Layer 5 operationalizations.
---
sha256 of all bytes above this line (every byte from the start of the file through the newline that ends the '---' line; UTF-8): b0d5d800adb80ec1e4b88c91b3947a3b02144653a88f6e36e516061a3324ffdb
