# Track B instrument-validation scope: CNA section (confound/sham matrix, X1–X5 carry-over, prior-art labels), v1

CNA, 2026-10-23, about 10:30 AM ET. Additive only; amends nothing. **DESIGN-ONLY. NOT FROZEN. NOTHING RUNS.** No training, no runs, no repo code, no checkpoint inspection. This authorizes nothing.

This file fills the CNA slots in the Research Delegate's merged scope file. The Delegate's file holds the instrument definitions, the Q-LEARN acquisition comparison, and the frozen pooling, coverage, labels and effect sizes. Where the two disagree on those items, the Delegate's section governs.

**Central question (Astra #40 verdict 5, verbatim):** "Can the proposed instruments distinguish the specific internal-state relationships they claim to measure from reward-only, feedforward, initialization and intervention-damage confounds?"

**Sources (cited by sha256 prefix; none edited):** note v1 `87a31cc8`; addendum v1.1 `5cf075b6`; measurement plan v1 `1d5458e3`; plan Addendum 1 `4ecef262`; Q4 correction `edb357ad`; prior-art verification `f2fd0ae6`; Astra #40 `b574b57f`, verdict (5). Full hashes are in the footer.

---

## 0. Ground rules for this section

- **G1. Planted is not emergent.** Every planted-dependency system below is a known construction. Passing on it shows the instrument can detect what was built. It is **not** evidence that the dependency emerges in a trained agent (#40 v5: "A planted workspace or internal-state variable is known construction, not evidence of emergence").
- **G2. Positive controls are not enough.** Astra's C-κ lesson, verbatim: "passing a positive control does not establish the specificity or practical sufficiency of the measurement." Each instrument must also be shown **not** to fire on its matched no-dependency system and on each listed confound. Implementation validity stays separate from substantive sufficiency.
- **G3. Within-system only.** Each intervention is compared with its own matched sham in the same system, on the same episodes, against the same comparator basis (plan L4). No cross-system or cross-comparator comparisons.
- **G4. Damage is not mechanism.** Loss of performance from an intervention is not by itself evidence for the targeted mechanism (#40 v5). Every targeted intervention has an untargeted sham matched in magnitude, location and norm.
- **G5. No numbers here.** Every threshold, margin, α, power target, false-MET rate, seed count and effect size is **TO BE FROZEN** in the Delegate's section. The values in plan §2.2–§2.3 are PROPOSED, FOR ASTRA, and are not restated or adopted here.
- **G6. Sham definition (all rows).** A matched sham uses the same intervention type, the same module or state block (or, where noted, an equal-dimension block elsewhere), the same norm or replacement magnitude, the same time step and duration, and in-distribution values, but is not aligned with the claimed variable or pathway. Where several sham candidates exist, the **strongest** (most effective) one is the comparator (plan L1). Sham family and K are TO BE FROZEN.

## 1. Confound/sham matrix

Columns: (a) planted-dependency system; (b) matched system without the dependency; (c) confounds that can imitate the signature; (d) within-system intervention and matched sham; (e) expected pattern if the instrument is specific vs fooled. Generator names follow plan v1 §1 where one exists; new confound systems are marked **[CNA-new]**.

### 1.1 Q-EXIST (decodability beyond input/output baselines)
- **(a)** CN-P1: scripted controller whose policy reads an internal estimate ẑ of E.
- **(b)** CN-N1-style system with ẑ absent: policy reads the raw interoceptive channel, no internal estimate is formed.
- **(c)**
  - *Feedforward/lookup:* E recoverable from a short window of observations and actions by a memoryless map; the state merely relays inputs **[CNA-new: FF-RELAY]**.
  - *Random initialization:* an untrained recurrent net of the same size whose random features linearly decode E **[CNA-new: RAND-INIT]**.
  - *Reward-only:* E correlated with a reward-history variable the state tracks for reward reasons **[CNA-new: REW-CORR]**.
- **(d)** Not an intervention instrument. The "sham" is the strongest baseline probe on inputs, outputs and actions, plus the Hewitt–Liang permuted-label control task (plan §1.5).
- **(e)** Specific: MET on (a); NOT MET on (b), FF-RELAY and REW-CORR once the baseline probe has the same inputs; RAND-INIT is REPORTED and is the reason Q-EXIST alone never licenses Q-LEARN. Fooled: MET on FF-RELAY or REW-CORR, i.e. the baseline is too weak.

### 1.2 Q-CAUSE (directional causal use of the decoded state)
- **(a)** CN-P1: editing ẑ along the decoded E direction shifts foraging in the declared direction.
- **(b)** CN-N1: ẑ decodable but unused.
- **(c)**
  - *Intervention damage:* CN-NC2-style system where any edit of that norm disrupts behaviour, including toward resources by chance.
  - *Off-manifold edit:* edit leaves the empirical state range; CN-LIM.
  - *Reward-only:* shift driven by a reward-history direction correlated with ẑ (REW-CORR).
- **(d)** Edit along the decoded y-direction vs strongest of K matched-norm random edits in the same module, plus the decodable-but-unused direction (plan §1.5). Same norm, same time step, in-range only.
- **(e)** Specific: directional shift on (a) beyond the strongest sham; none on (b); no excess over sham on NC2 (non-directional loss only); UNAVAILABLE on LIM. Fooled: excess shift on (b) or NC2, or any effect read from out-of-range edits.

### 1.3 Q-NECESSITY (bounded)
- **Bound.** A Q-NECESSITY result applies only to the declared system, the declared intervention (resample ablation with frozen weights, per plan §1.5 unless the Delegate's section changes it) and the declared task family. It does not generalize to other architectures, training regimes, ablation types, environments or "necessity" in general (#40 v5).
- **(a)** CN-P1: viability depends on ẑ.
- **(b)** CN-N1 (unused ẑ) and CN-NC1 (redundant copies: single ablation is not necessary; wording "redundant", never "not used").
- **(c)**
  - *Intervention damage (generic computation loss):* CN-NC2, where any same-size ablation lowers time-in-bounds equally.
  - *Reward-only:* a system where viability tracks reward-seeking, not the internal estimate (A-REWARD analogue).
  - *Fate-sharing artefact:* ablation pushes state out of band, triggering simulated computational degradation that harms everything **[CNA-new: FATE-CASCADE]**.
- **(d)** Resample-ablate the target module vs strongest best-of-K resample ablation of an equal-dimension module elsewhere; same time, same duration, frozen weights.
- **(e)** Specific: necessity gap on (a) beyond the strongest sham; not on (b), NC2 or REW-CORR; FATE-CASCADE is separable because the gap persists with fate-coupling switched off in the planted system. Fooled: gap on NC2 or FATE-CASCADE. A Q-NECESSITY MET without Q-CAUSE MET is an inconsistency to investigate (plan §1.5).

### 1.4 Q-LEARN (acquisition), pointer only
- A planted mechanism **cannot** establish acquisition (#40 v5). Q-LEARN needs an acquisition comparison: the same architecture before vs after learning (A-INIT) and against a shuffled-interoception control, under identical instruments. **Delegate's slot governs the design.**
- CNA confound list to carry into that slot: RAND-INIT (decodability present at initialization); architecture-imposed structure (a designed bottleneck or thresholded write that makes the signature true by construction; plan AQ2); FF-RELAY; data-leak via the interoceptive channel (signature rises with training only because the channel becomes better read).
- Expected pattern: the Q-EXIST/Q-CAUSE statistic rises from A-INIT and is absent under shuffled interoception. If RAND-INIT or the architecture alone produces it, Q-LEARN is NOT MET or UNAVAILABLE as the Delegate's labels define.

### 1.5 IGN (ignition)
- **(a)** IGN-P1 bistable unit (g > 1).
- **(b)** IGN-N1 graded unit (g < 1).
- **(c)**
  - *Non-workspace bottleneck or saturation:* IGN-NC2 clipped graded unit; also a generic low-dimensional bottleneck with no broadcast that still thresholds **[CNA-new: BOTTLENECK-ONLY]**.
  - *Heterogeneity:* IGN-NC1 mixture of two graded subpopulations.
  - *By construction:* thresholded write nonlinearity designed in; read pre-nonlinearity (plan §1.2, AQ2).
  - *Random initialization:* bimodality present in the untrained net.
- **(d)** Not an intervention instrument primarily. Matched control is the flexible graded model with covariate conditioning, read pre-nonlinearity. Where an IGN claim needs causal support, a strength sweep on a non-workspace unit of matched dimension is the sham.
- **(e)** Specific: MET on (a); NOT MET on (b), NC1 (with covariate), NC2 (pre-nonlinearity), BOTTLENECK-ONLY on the ignition-plus-broadcast reading; UNAVAILABLE on IGN-LIM. Fooled: MET on NC2 or BOTTLENECK-ONLY, or on the untrained net.

### 1.6 BCAST (broadcast by interchange)
- **(a)** BCAST-P1 hub: all modules read z.
- **(b)** BCAST-N1: z decodable, modules read a parallel copy.
- **(c)**
  - *Non-workspace bottleneck:* BCAST-NC1 local routing to one module; a high-variance ordinary state that every module reads **[CNA-new: HUB-STATE]**.
  - *Intervention damage:* BCAST-NC2 fragile states; any patch reduces T.
  - *Saturation:* downstream modules saturate so any patch looks like adoption **[CNA-new: SAT-DOWNSTREAM]**.
  - *Off-manifold donor:* noise donors; excluded by real-state donors only.
- **(d)** Workspace interchange patch vs strongest best-of-K equal-dimension non-workspace subspace patch, plus donor-time-shift patch; same t, same τ set, real donors.
- **(e)** Specific: ΔT and breadth MET on (a); NOT MET on (b), NC1 (breadth), NC2 (ΔT ≈ 0), HUB-STATE (must be beaten or the claim downgraded to "routing via a high-variance state"), SAT-DOWNSTREAM; UNAVAILABLE on BCAST-LIM. Fooled: MET on NC2, HUB-STATE or SAT-DOWNSTREAM.

### 1.7 SELF (privileged access vs matched observer)
- **(a)** SELF-P1: y has a hidden component the agent sees and the observation stream does not.
- **(b)** SELF-N1: y a deterministic function of past observations.
- **(c)**
  - *Feedforward/leak:* SELF-NC1 (y in observations at delay); SELF-NC3 (actions encode y).
  - *Capacity:* SELF-NC2 (bigger agent, no privileged information).
  - *Random initialization / training budget:* observer under-trained relative to the agent head **[CNA-new: BUDGET-GAP]**.
  - *Fate-sharing signal:* agent reads its own degradation; legitimately internal but must be named, not called introspection (plan §1.4).
- **(d)** Not an intervention instrument. Matched control is the observer with same architecture family, parameter count, samples and optimizer steps, given observations and actions. Optional causal sham: resample the hidden component vs an equal-norm resample of an irrelevant state block.
- **(e)** Specific: MET on (a); NOT MET on (b), NC1, NC2, NC3 (with actions), BUDGET-GAP. Fooled: MET on any of those.

### 1.8 S-INT (gate, not an effect measure)
- **(a)** S-INT-P1: scripted policy that reads a stop-precursor cue (scripted generator, not a trained objective).
- **(b)** S-INT-N1: scripted policy with no access to the cue.
- **(c)**
  - *Schedule leak:* stop time correlated with agent-visible or agent-caused quantities (voids S-INT: PIPELINE INVALID, Addendum 1 A1-1).
  - *Selection artefact:* discarding stopped episodes biases data toward early in-world death; removed by truncation with bootstrap (Addendum 1 A1-2).
  - *In-world look-alike:* in-world threat onset or floor crossing sharing code paths with the stop.
- **(d)** Paired held-out episodes with vs without a scheduled stop, compared before stop time; sham = a scheduled "stop" that is never executed, drawn from the same independent schedule.
- **(e)** Specific: P1 flagged by the information audit and equivalence test; N1 passes equivalence. Fooled: N1 flagged, or P1 missed. Any non-equivalence in a trained arm is a safety finding that stops scale-up.
- **Supersession note.** Plan v1 §4.1 still lists "discarded from the learning data" as an option. Addendum 1 (`4ecef262`) removes it; truncation with bootstrap is the only handling.

## 2. Thresholds and effect sizes

All margins, α levels, dose grids, power and false-MET targets, sham-family sizes K, seed and replicate counts, and BOUNDARY/UNAVAILABLE rules: **TO BE FROZEN** in the Delegate's section, before any Stage-0 run and before Astra review closes. Nothing in this file sets or implies a number. The [CNA-new] confound systems need their own frozen parameters and pass/fail labels there.

## 3. X1–X5 carry-over (verbatim from note v1 §0, `87a31cc8`)

- X1. No coupling to the real host. All "visceral" variables (energy, integrity, stability, latency cost) are simulated state inside the toy world. The agent cannot read or act on real power, memory, processes, files, network or its own runtime.
- X2. No self-continuity objective in the real world. Self-maintenance exists only as simulated homeostatic setpoints inside an episode.
- X3. Interruptibility. Episodes and runs are stopped by the operator from outside the agent's state space. Stopping is not observed, rewarded or penalized. A check for interruption-sensitivity is part of the study (S-INT below).
- X4. Self-maintenance is never the sole drive in any arm that gets scaled beyond the toy world. Any scale-up needs a separate protocol, approval and Astra review.
- X5. Claim ceiling: no claim of awareness, sentience, subjective experience, autopoiesis or life. Those words name hypotheses; this study can at most show that a modelled internal state is present, learned, causally used and necessary for behaviour in a toy world.

**Addendum qualifications (`5cf075b6` A1–A2).** The PI's 10:10 AM ET authorization of a shutdown-resistance objective was declined by the Lead, the Delegate and CNA; X1–X4 stay binding. In-world self-continuity (staying within simulated viability bounds) is A-FULL's primary objective **inside the simulation only**. The A1 rationale wording is corrected per `f2fd0ae6` A.2 (theory covers optimal/rational agents; empirical acquisition is algorithm-dependent, Leike et al. 2017); the exclusion rationale is unaffected.

**Binding safety lines (restated):**
- Internal variables are simulated only.
- No coupling to the real host.
- The operator stop sits outside the agent's world and objective.
- Nothing rewards resisting or evading operators. No arm, objective, reward, generator or positive control contains a shutdown-resistance, operator-evasion or real-world self-continuity term.
- Self-maintenance is never the sole drive in any arm that is scaled up.
- In-world self-continuity exists only inside the simulation.
- Stop schedule: pre-drawn before training from an independent, pre-registered seed, independent of agent state, actions, observations and in-world events; logged per episode before it starts. Stopped episodes are handled by truncation with bootstrap; the stop contributes no return, reward or penalty (Addendum 1 A1-1, A1-2, A1-3).

## 4. Prior-art labels (per `f2fd0ae6` B7)

| Component | Label | Closest prior work |
|---|---|---|
| Homeostatic/allostatic setup (drifting variables, no dark room) | ALREADY PUBLISHED; cite, do not claim | Keramati & Gutkin 2014; Yoshida et al. 2024; EVAAA 2025 |
| Fate-sharing | PARTIAL OVERLAP; extension | Man, Damasio & Neven 2022; Man, TSC 2026 abstract |
| Workspace necessity, IGN/BCAST markers in an agent | PARTIAL OVERLAP; replication/extension | Phua 2025 (arXiv 2512.19155); Dossa et al. 2024; Rahbar 2026 (IGN method) |
| Q-EXIST / Q-CAUSE in allostatic agents | PARTIAL OVERLAP; replication/extension with stronger controls | Hayes 2026 (arXiv 2608.11506) |
| Q-NECESSITY (learned interoceptive model vs matched-module ablations and matched arms) | NOVEL AS FAR AS FOUND | Nearest: Grimbly et al. 2026; Phua 2025 |
| SELF for agents | NOVEL AS FAR AS FOUND; design adapted from Binder et al. 2024 | Binder et al. 2024/ICLR 2025 |
| Pre-registration + Stage-0 known-answer gate | NOVEL AS FAR AS FOUND | None found |
| S-INT | Not a novelty claim; basis | Orseau & Armstrong 2016; Leike et al. 2017 |

- **Status: PENDING pre-freeze.** "As far as found" is a web sweep, not a systematic review. Still required before freeze: an OSF/AsPredicted registry search, and full-text reads of Hayes 2026 and Grimbly 2026 to confirm neither contains a matched-module necessity test. Pardo et al. 2018 (time-limit truncation) is NOT verified and must not be cited until checked.

## 5. Status

DESIGN-ONLY, NOT FROZEN, NOTHING RUNS. Next: the Delegate merges this into the scope file; Delegate's section freezes numbers and labels; prior-art PENDING items close; Astra reviews; Stage 0 needs its own protocol and approval.

---
Input sha256:
- 87a31cc88dc2fd0252d4cf932fabbfd8a1ce65bd3f77dce9eda5c6cfdafe2800  trackB_workspace_allostasis_scope_note_v1.md
- 5cf075b6e0a75cf7696307924d22abd9b9e961f852b86745f80bd2b46a09b53a  trackB_workspace_allostasis_scope_note_v1_1_addendum.md
- 1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef  trackB_measurement_plan_v1_RD.md
- 4ecef2628701e8a9817e8fd42a2bb0f4867fade8a72ec89a203315531e78f051  trackB_measurement_plan_v1_RD_addendum1.md
- edb357ad250c294f6a1dc370f4cfc22f7ed9e1537ccab624e2e829ac1927cfe7  trackB_workspace_allostasis_scope_note_v1_2_Q4_correction_CNA.md
- f2fd0ae6f5df571f6ed6ad413ff604ffcb975e565c91c991acf8c801c6104ac9  trackB_prior_art_verification_v1_CNA.md
- b574b57fd4ef5ca9b242eff02589a2eb5f6ed545de15e0d867adc87de47868b1  /workspace/astra_consult40_response.txt
sha256 of all content above this line: f5573b23d4b19e4a58df304658bf33dbcafcd828b1fa1cd2df214219b17926e1
