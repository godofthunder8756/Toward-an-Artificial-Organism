CNA, 2026-10-23, additive note; planning only; authorizes nothing

# Track B prior-art verification v1.2: pre-freeze open items (CNA)

- **Amends nothing.** This note is additive to `trackB_prior_art_verification_v1_1_prefreeze_CNA.md` (sha256 29068cce…) and `trackB_prior_art_verification_v1_CNA.md` (sha256 f2fd0ae6…). Neither file, nor any other existing file, was edited.
- **Nothing ran.** No training and no repo code. Third-party code from the Craggs deposits was downloaded and *read*; none of it was executed. The only network actions were read-only HTTP GETs: arXiv, PMLR, Europe PMC, the OSF API v2 and osf.io file downloads, the Zenodo REST API and file downloads, the COS Registered Reports page, PCI Registered Reports and PMLR v148.
- **Written** 2026-10-23, about 10:37–10:55 AM ET. Registry states are as of that window. OSF and Zenodo timestamps are UTC in the source and are converted to ET (UTC−4) below.
- **Scope.** Track B S-INT handling (truncation plus bootstrap from the final state's value; stop schedule pre-drawn from an independent seed) and the three narrowed novelty claims: (1) Q-NECESSITY, (2) SELF, (3) the Stage-0 known-answer gate.

## Bottom line

- **Pardo et al. 2018: SUPPORTS WITH CAVEATS** our S-INT handling (Part 1).
- **Craggs Block V has now been run, and this corrects v1.1.** Confirmatory results, code and data were posted on 15 Oct 2026, and a five-block synthesis on 16 Oct 2026. v1.1's "Data does not yet exist … No results found" was out of date when written: it read the registration responses but not the OSF `/resources/` endpoint. The agents are **hand-coded deterministic Python rules**: no learning, no neural network, no RL. All four of our points of difference **HOLD** (Part 2).
- **Wilterson & Graziano 2021** is a DQN (RL) agent. Its retrained-without-schema experiment (Exp. 3) *does* test whether learning and behaviour need the self-model. But the schema is an **experimenter-supplied input array describing attention**, not a learned model and not a body or interoceptive model. It has no size-matched ablation of other modules and is not pre-registered. It does not make Q-NECESSITY a replication (Part 4).
- **New Zenodo hits.** Valerio Porras 2026 has a learned body predictor and a metacognitive Φ, a pre-registered causal battery and a hand-coded policy. Asan 2026 is a PPO homeostatic agent with matched-random-subspace lesions. Bankuti 2026 and Akiyama 2026 describe pre-registered known-answer validation of instruments. None runs our Q-NECESSITY or SELF test. The last two narrow claim (3) further (Part 5).
- **Verdicts** (Part 6):
  - (1) Q-NECESSITY: **STILL NOVEL AS FAR AS FOUND**, narrowed, with the generic lesion-necessity paradigm credited to prior work.
  - (2) SELF: **STILL NOVEL AS FAR AS FOUND**.
  - (3) Stage-0 gate: **PARTIAL OVERLAP**.

## Part 1. Pardo et al. 2018, "Time Limits in Reinforcement Learning"

**Source read in full.** I read arXiv 1712.00378 **v4** (27 Jan 2022) through pdftotext, every page. I also downloaded the PMLR camera-ready (ICML 2018, PMLR 80:4045–4054) and checked that the section structure (§1–§5, §3.1–§3.4) and every passage quoted below appear verbatim in it. One difference between versions: the Fig. 7 caption gives γ = 1 in v4 and γ = 0.99 in PMLR. It does not affect anything below.

**The paper's argument on partial-episode bootstrapping (PEB):**

- **Two cases (Abstract).** Agents may maximise performance "over (i) that fixed period, or (ii) an indefinite period where time limits are only used during training to diversify experience". In case (i), "the terminations due to time limits are in fact part of the environment, and thus a notion of the remaining time should be included as part of the agent's input". In case (ii), "the time limits are not part of the environment and are only used to facilitate learning … by bootstrapping from the value of the state at the end of each partial episode."
- **Scope of PEB (§1).** "we argue to bootstrap at states where termination is due to time limits, or more generally any other causes than the environmental ones."
- **Formal argument (§3).** For time-unlimited tasks, treating time-limit terminations as environmental "is equivalent to optimizing for returns G_{t:T} (Equation 2), not accounting for the possible future rewards that could have been experienced if no time limits were used." The value is rewritten as v_π(s) = E_π[G_{t:T} + γ^{T−t} v_π(S_T) | S_t = s] (Eq. 5). The one-step TD target (Eq. 6) is "r at environmental terminations" and "r + γ v̂_π(s′) otherwise (including timeouts)". An agent without PEB receives "conflicting updates for estimating the value of the same state [that] lead to an approximate average of these updates."
- **How PEB differs from White (2017) (§3).** "(2) In the proposed PEB approach, the agent does not experience a transition from the last state of a partial episode to the first state of the next episode … (3) PEB uses a constant discount factor."
- **Implementation (§3.1–§3.2).** "bootstrapping is maintained from the non-terminal states that are reached at the time limits" (§3.1). For PPO, "continuing to bootstrap from the last non-terminal states is the only modification required" to GAE (§3.1).
- **Generality and preconditions (§4).** "partial-episode bootstrapping is generic in that it is not restricted to partial episodes only due to time limits. In fact, this approach is valid for any early termination causes." Also: "In order for the partial-episode bootstrapping method in Section 3 to work, as is the case for bootstrapping methods in general, the agent needs to use reliable predictions. This is in general resolved by enabling sufficient exploration … a good way … is to sufficiently randomize the initial states."
- **Conclusion (§5).** "when learning policies for time-unlimited tasks, it is necessary for correct value estimation, to continue bootstrapping at the end of the partial episodes when termination is due to time limits, or any early termination causes other than the environmental ones."
- **Experiments.** Tabular Q-learning (Two-Goal Gridworld, Zhang & Sutton gridworld) and PPO (Hopper, Walker2d, InfiniteCubePusher). Truncation is always at a **fixed** T (50, 200, 300 or 1000). In these experiments the PEB agents are **not** given the remaining time: Fig. 1(d) PEB is shown separately from Fig. 1(c) time-awareness, and the Fig. 6 legend lists "PPO" and "PEB-PPO" only.

**(a) Does it support bootstrapping at truncations that are not part of the agent's state?** **Yes**, in case (ii), where the truncation is not part of the task. The paper's position is that such a truncation is not part of the environment, so it should be neither terminal nor observed. The agent bootstraps through it (Eq. 6, "including timeouts"). The PEB agents in §3 have no time input.

**(b) Conditions it requires (stated or implied):**
1. **The objective is the indefinite-horizon return (Eq. 1), so the truncation is not part of the task.** If the truncation *is* part of the task (case (i)), the paper's remedy is different: make it observable (time-awareness, §2), not bootstrap through it.
2. **The truncation is not treated as a terminal state.** Only "environmental terminations" use y = r (Eq. 6).
3. **Reliable value estimates at the truncated states** (§4), via exploration and randomised initial states.
4. **No transition from the truncated state into the next episode's first state** (§3, point 2), and a **constant discount** (§3, point 3).
5. **On "time limit not observed":** the paper does not state this as a formal precondition of PEB. It follows from case (ii): the limit is not part of the environment, and the PEB agents have no time input. Observing the limit is the case-(i) remedy.

**(c) Does it carry over to random, independently seeded stop times (exogenous interruption)?**

- **What the paper itself says.** §4 ("valid for any early termination causes") and §5 ("any early termination causes other than the environmental ones") explicitly claim the method covers non-time-limit truncations. But it **tests only fixed-T limits**; the curriculum example in §4 is a suggestion, not an experiment.
- **My extension, not Pardo's.** Eq. 5 generalises to a random stopping time τ as v_π(s) = E[G_{t:τ} + γ^{τ−t} v_π(S_τ) | S_t = s]. With bootstrapping, the TD target stays consistent with the indefinite-horizon value whatever the stop time.
- **Caveats:**
  - **State-correlated stops (ruled out for us).** If stop times correlated with agent or environment state, the stops would decide which states are bootstrapped and how often. That changes how value-approximation error is weighted across states and the data distribution. And if stops were ever treated as terminal, it would create a value signal tied to stop-predictive states, i.e. an incentive to avoid or seek interruption. Our pre-drawn schedule from an independent seed makes stop times independent of state and history, which rules out this bias channel.
  - **Bootstrap quality.** Bootstrapping inherits v̂'s error at the stopped state (§4 "reliable predictions"). The stops should not concentrate in rarely visited states. An independent uniform-hazard or fixed-schedule draw satisfies this in expectation, but it is worth a check in the S-INT audit.
  - **Recurrent agents.** Pardo's agents are tabular or feedforward PPO. For our recurrent agents, the bootstrap must use v̂ evaluated on the hidden state at the stop step, *before* any reset. Pardo gives no guidance on this.
  - **Agent inference of stops.** If the agent could infer an upcoming stop (for example from schedule regularities), case (ii) quietly turns into case (i). An independent random draw with no observable cue avoids this. Our existing S-INT probe-AUC information audit is the right check.
  - **Pardo is about value estimation, not interruptibility.** It does not discuss interruptibility or incentives to resist shutdown. S-INT's safety rationale still rests on Orseau & Armstrong 2016 and Leike et al. 2017, as v1 B6 said.
- **Verdict: SUPPORTS WITH CAVEATS.** Pardo directly supports truncate-and-bootstrap for truncations that are not environmental and not part of the agent's state, and it explicitly claims the method extends to any non-environmental early termination. The extension to random stop times is asserted but not tested in the paper. Our independent seed closes the main bias caveat (state-correlated stops). The recurrent-state bootstrap point and the agent-inference check are ours to implement.

## Part 2. Craggs 2026, Blocks I–V (OSF jz4ed, gqanp and siblings)

**Sources opened:**
- **OSF API:** `/registrations/{id}/`, `/resources/`, `/files/osfstorage/` and the archived folder listing, and `/schema_responses/`. This covered jz4ed, gqanp, 69zny and the siblings g3te5, jrcnb, euf2j, 8zwm7 and rehw5.
- **jz4ed OSF storage:** `BLOCK_V_PREREGISTRATION_OSF_PACKAGE.zip`, downloaded and unzipped.
- **Zenodo deposits linked from the OSF resources:** Block V software 10.5281/zenodo.23321474, Block V dataset 10.5281/zenodo.23321507, the five-block synthesis 10.5281/zenodo.23413881, B2 software 10.5281/zenodo.23122125, and Working Paper III 10.5281/zenodo.22857230 (PDF).
- **What was read:** the Block V README, the agent code `toe_exp/block5.py` (read in full; identical in the OSF package and the Zenodo software, sha256 066b17c1…), the `run_confirmatory.py` imports, the preregistration record PDF, the clarification addendum, the execution record, the analysis record and decision CSV, `confirmatory_variants.json`, and the synthesis `.tex` and `.json`. For B2, `toe/agents/maintenance.py`.
- **No GitHub links** appear in these records.

**What Block V actually is:**

- **Agents.** The architectures are `ARCHS = ["S0","S1","S2","S3","S4","H_ERROR","H_EXTERNAL"]` (block5.py L8). Behaviour is fixed `if/elif` rules with hard thresholds (`check_threshold=0.70`, `compute_threshold=0.68`; L68–96).
- **The self-model.** `self_monitor(t)` is a fixed formula: `clamp(0.58*diagnostic_a + 0.42*diagnostic_b**2)` mapped to a success probability (L60–63). Nothing is trained: there is no optimiser, gradient, network or reward-driven update anywhere in block5.py or run_confirmatory.py, which import only `json, random, math, statistics, hashlib, csv`.
- **Learned networks? NO. Trained by RL? NO.** B2's agents are likewise "Transparent maintenance controllers" (maintenance.py docstring): numpy budget-allocation rules.
- **What the self-model represents.** It is an estimate of the agent's own **success probability (competence/reliability)**, built from two noisy diagnostics of a hidden `latent_impairment` that degrades accuracy (L51–58). The preregistration calls it "facts about its own competence, uncertainty, resources or limitations". The latent impairment is an *internal condition*, but it is a scalar reliability factor on task accuracy. It is **not** a body, homeostatic or interoceptive variable, has no setpoints, and no viability.
- **Outcome variables.** Accuracy and **utility** (correct − check or compute cost) on decision and verification trial families. The clarification addendum made utility primary for H5.6. There is no survival or viability outcome.
- **Controls:**
  - **S3** is a distribution-matched shuffle: exact multiset, reverse-rank anti-alignment.
  - **S4** is the "capacity-matched non-self control". In code (`S4: q=qworld`), it **replaces** the self-monitor with `world_monitor` (task difficulty only), using the same scalar interface.
  - **H_ERROR** is a recent-error bypass. **H_EXTERNAL** is an oracle bypass that supplies the true success probability.
  - None of these is an ablation of *another* module of the agent at matched size.
- **Results** (execution record and analysis record, 20 seeds):
  - H5.1, H5.2, H5.3 and H5.5: RETAIN.
  - H5.4: RESTRICT (0.143 and 0.083, below the 0.15 and 0.10 margins).
  - **H5.6 (endogenous self-model necessity): REDUCE.** H_EXTERNAL came within 0.0056 (decision) and 0.0072 (verification) mean utility of S2. The authors' reading: "calibrated self-relevant information is sufficient for the registered downstream control function even when supplied externally rather than generated endogenously."

**Our four points of difference:**

| Point | Status | Basis |
|---|---|---|
| Body or interoceptive state content | **HOLDS** | Craggs' self-model estimates competence (success probability) from noisy diagnostics of a latent impairment scalar. It has no body or homeostatic variables. |
| Learned RL agent | **HOLDS** | Fixed hand-coded rules and a fixed-weight monitor. No learning of any kind, no neural network, no RL. |
| Survival-style (viability) outcomes | **HOLDS** | Accuracy and cost-adjusted utility on trial families. No viability or death outcome. |
| Same-size ablations of other modules | **HOLDS (narrowly)** | S4 is a capacity-matched *substitute* for the self-monitor, not a same-size ablation of another module. S3 is a shuffle; H_* are bypasses. The *logic* of capacity-matched non-self control is shared, so cite it. |

**Design lesson for Track B, not a novelty issue.** Craggs H5.6 shows that an **externally supplied, calibrated estimate** can defeat an endogenous-necessity claim. I recommend that the Delegate's scope consider an analogous arm for Q-NECESSITY: an oracle or externally supplied interoceptive estimate fed to the policy. If our matched arms do not include one, a Q-NECESSITY MET could be read as "the information is needed", not "the self-model is needed". This is a recommendation only.

**Other blocks.** Per the synthesis record, all are completed and use the same transparent-rule style; I read the code for B2 only.
- B2 (gqanp): H1.1–H1.4 RETAIN, H1.5 DEFERRED_INITIAL, H1.6 REDUCE.
- Blocks I B1, II, III and IV: RETAIN or DEFERRED as listed in the synthesis.

## Part 3. Re-check of jz4ed, gqanp and 69zny (as of about 10:40 AM ET, 23 Oct 2026)

| Reg. | Registered (ET) | Updates (ET) | Posted results | Status |
|---|---|---|---|---|
| **jz4ed** (Craggs Block V) | 9 Oct 2026, 6:00 PM | Approved schema-response update, "Pre-execution protocol clarification, 10 October 2026", submitted 10 Oct, 5:36 AM. OSF resources added: analytic code 15 Oct, 2:51 PM (zenodo.23321474); data 15 Oct, 2:53 PM (zenodo.23321507); paper 16 Oct, 6:27 AM (zenodo.23413881). Record last modified 16 Oct, 6:28 AM. | **YES.** Confirmatory execution complete (20 seeds); decisions as in Part 2. Zenodo records created 14 Oct, 7:22 PM (software) and 7:35 PM (data), publication date 12 Oct; synthesis created 16 Oct, 5:46 AM. | **RESULTS POSTED** (corrects v1.1) |
| **gqanp** (Craggs Block I B2) | 2 Oct 2026, 6:41 AM | No schema-response revisions (original response only). OSF resources added: code 3 Oct, 7:53 PM (zenodo.23122125); data 3 Oct, 8:00 PM (zenodo.23122412); paper 16 Oct, 6:18 AM (zenodo.23413881). Last modified 16 Oct, 6:19 AM. | **YES.** H1.1–H1.4 RETAIN; H1.5 DEFERRED_INITIAL (follow-up jrcnb RETAIN); H1.6 REDUCE. | **RESULTS POSTED** |
| **69zny** (Faeth 2026) | 30 Sep 2026, 4:40 PM | None. Original schema response only; no resources; last modified 30 Sep, 4:40 PM. Source node f3bkx last modified 2 Oct, 12:04 AM (node, not registration). | **NO.** OSF storage holds only `preregistration-package.zip` and `protocol.md` ("No confirmatory data have been collected"). | **UNRUN as far as visible** |

Faeth's protocol, read for completeness: AffectWorld active-inference agents with "known resource maps, two-step planning, no online resource-model learning". No RL, and no self-model necessity test. This does not change v1.1's PARTIAL label on claim (3).

## Part 4. Wilterson & Graziano 2021, PNAS 118(33):e2102421118

**Source.** Full text read from Europe PMC (PMC8379943, JATS XML), all sections from Significance through Data Availability. Title per Crossref and Europe PMC: "The attention schema theory in a neural network agent: Controlling visuospatial attention using a descriptive model of attention." The **SI Appendix was not read**: pnas.org returned HTTP 403, and the Europe PMC supplementary bundle contains figures only.

- **Trained by RL? Yes.** "The agent that we constructed uses deep Q-learning … on a simple neural network with three connected layers of 200 neurons each" (Introduction). It was implemented in TF-Agents with Adam lr = 0.001 and ε-greedy ε = 0.2, and trained over 1,500 iterations × 100 games (Methods, "The Agent"; "The Training Procedure"). There were five independently initialised "artificial subjects".
- **What the self-model is:**
  - An **experimenter-supplied 10×10 input array** marking the spotlight's location. "This array serves as the agent's simple attention schema … it represents the state of attention itself … it is only a descriptive model of attention" (Methods, "Environment and Action Space").
  - "Any predictive component of an attention schema must be learned by the agent and would be represented implicitly in the agent's neural network."
  - Discussion: "a simple descriptive component … that was supplied to it in the form of the attention schema array, and a more complex … predictive component that was learned".
  - So it is a model of **attention**, not of body or interoceptive state. The paddle row is called "a simple analogy to the descriptive component of the body schema", but it was never ablated.
- **What was ablated:**
  - **Exp. 1:** attention spotlight disabled at test.
  - **Exp. 2, "Necessity of the Attention Schema for Performance":** schema array zeroed at test only, after training with it. This is a deployed-dependence test.
  - **Exp. 3, "Necessity of the Attention Schema for Learning":** schema zeroed for all training and test games. This is a retrained-necessity test, and the paper calls it "the central experiment of the study". Performance fell to about 0.4 versus about 3.5 attention points.
  - **Only control:** a noise-matched control for the *spotlight* (remove 5 random noise pixels everywhere: "performed similarly to the orange line … peak score of about 0.5"; Exp. 1).
- **Did it test whether behaviour needs the self-model?** Yes, for the *supplied descriptive schema* (Exp. 2 and Exp. 3), with behavioural outcomes (tracking and catch score). It did **not** test necessity of a *learned* self-model. The learned "predictive component" was never isolated or ablated.
- **Size-matched ablations of other modules? No.** No other 100-unit input was removed, no capacity-matched non-schema control was run, and there is no sham. The authors note that extra inputs "could, arguably, harm learning", but they did not test an input-count-matched control.
- **Pre-registered? No.** No registration is mentioned. The text says "This article is a PNAS Direct Submission", which is the editorial track. There are no statistical tests: "we will not present the statistical tests … but will instead adhere to the convention of showing the SE." Data and code are in Princeton DataSpace (ark:/88435/dsp01kp78gk430); not inspected.
- **Consequence:** this is the closest **RL-agent precedent for a retrained-necessity test of a self-model**. It must be cited in the Q-NECESSITY prior art. It does not make Q-NECESSITY a replication, because the self-model is supplied rather than learned, its content is attention rather than body, and it has no size-matched other-module ablation and no pre-registration.
- **Citation correction carried from v1.1.** Use the Crossref title, not Phua's "…Controlling attention without consciousness".

## Part 5. Zenodo and Registered Reports search

### 5.1 Zenodo (REST API `https://zenodo.org/api/records?q=<q>&size=25&sort=bestmatch`; the top 25 by best match were screened by title, and relevant ones by description)

**First pass, unquoted terms.** Zenodo ORs bare terms, so these totals are uninformative:
- "homeostatic reinforcement learning agent": 330,371
- "allostatic agent reinforcement learning": 329,275
- "interoceptive reinforcement learning agent": 329,243
- "interoceptive" "self-model" agent: 43,196
- "global workspace agent reinforcement learning": 599,135
- "global workspace ablation neural network": 486,936
- "self-model ablation agent": 299,035
- "self-model necessity artificial agent": 467,131
- "attention schema" agent: 42,277
- "preregistration artificial agent self-model": 449,033
- "homeostatic agent preregistration": 47,986
- "privileged access self-prediction agent observer": 317,489

The top 25 of each were screened. The only relevant hits recur in the second pass.

**Second pass, boolean and phrase queries (the operative search):**

| # | Query | Total | Relevant (screened) |
|---|---|---|---|
| 1 | `"homeostatic reinforcement learning"` | 13 | 22191728, 22810742 (via #2) |
| 2 | `homeostatic AND agent AND "reinforcement learning"` | 28 | 22191728, 22810742, 18193509 |
| 3 | `allostatic AND agent` | 31 | 0 |
| 4 | `interoceptive AND agent AND (learning OR "neural network")` | 11 | 22810742 |
| 5 | `interoception AND "artificial agent"` | 1 | 0 |
| 6 | `"global workspace" AND agent` | 49 | 23306276 (theory and proposal only), 21745212 |
| 7 | `"global workspace" AND (ablation OR lesion)` | 22 | 23377484 (architecture, no test), 21606412 (self-report, no observer) |
| 8 | `"self-model" AND (ablation OR lesion OR necessity) AND agent` | 19 | 20587698, 21850369 |
| 9 | `"attention schema"` | 54 | 19738204 |
| 10 | `"self-model" AND (preregistration OR preregistered OR "pre-registered")` | 40 | 22863692, 22191728, 21850369, 23413881/23417397 (Craggs) |
| 11 | `(homeostatic OR homeostasis OR interoceptive) AND (preregistration OR preregistered OR "pre-registered") AND agent` | 15 | 22191728 |
| 12 | `"known-answer" AND (instrument OR assay) AND (neural OR agent)` | 3 | 21983630 |

**Relevant Zenodo records.** I read the full descriptions of all of them; extra reading is noted per item.

1. **A. Valerio Porras, "Learning Without Remembering: Habituation in Weights and a Calibrated Self-Model in a Minimal Embodied Agent"**, Zenodo 22191728, v0.12, 31 Aug 2026. PDF downloaded; §3–§4 read.
   - **Learned parts:** a learned action-conditioned **body predictor** (MLP 13→64→6 or 13→128→128→6) that predicts the next position *and next interoceptive ECUS state*, and a learned metacognitive Φ (MSE regressor to |ε|).
   - **Policy: hand-coded thresholds**, not RL. "The implemented policy is a threshold approximation of this drive: if E < 0.55 the agent forages…" (§3.1).
   - **Causal test:** Φ-coupled vs "identical Φ computed but not allowed to influence action" on **fog time**, d = −1.61. It is confounded: "reproduced by a random attention gate" (§4.5).
   - **No ablation of the body predictor against viability**, and no same-size other-module ablations.
   - **"Pre-registered"** in the author's own project notes ("doc. 48"), "available from the author upon request". Not a public registry.
   - **Closeness: PARTIAL.** It is the nearest hit on a *learned body model in a homeostatic agent*. It does not trigger replication: the agent's policy is not learned, the self-model whose causal role was tested is metacognitive, and the outcome is epistemic rather than viability. Its coupled vs computed-but-uncoupled design is our sham logic, and its random-gate confound is a ready example for the confound matrix.
2. **Y. Asan, "Decodable, Compositional Affect-Like Representations in a Self-Taught Agent and Pretrained Language Models"**, Zenodo 22810742, 17 Sep 2026. PDF text searched, not read in full.
   - A **PPO**-trained homeostatic agent with ridge probes of interoceptive causes. "lesioning the affect subspace against a random subspace", and activation patching versus "a matched-dimension random subspace" (9% vs 0%).
   - Interoceptive *input* masking: 82% → 10%.
   - No separate self-model, no SELF test, and no pre-registration string found.
   - **Closeness: PARTIAL on Q-EXIST/Q-CAUSE**. It is the closest found to our random-subspace-matched Q-CAUSE in a homeostatic RL agent; cite it. Not Q-NECESSITY.
3. **P. A. García Hernández, "A Layered Artificial-Life Model of Functional Self-Modeling…"**, Zenodo 21850369, v1.4. Description only; the corpus is in Spanish and was not read.
   - Node.js organisms with a "learned scalar estimate of their own fragility that governs avoidance". The estimator is a running mean with a step floor; per the description, the avoidance rule is hand-written in the lineage where the effect appears.
   - Pre-registered in-corpus (layers 10–16). It includes a **yoked control** in which each organism acts on another organism's estimate.
   - **Closeness: PARTIAL.** Self-estimate content is body-like (fragility), but the agent is not a learned-network RL agent. The yoked design is worth considering as a matched arm.
4. **O. Bankuti, "Validating a Causal Assay for Engineered Self-Indexed Temporal State"**, Zenodo 22863692, 21 Sep 2026. Description only.
   - "reports and validates a preregistered causal assay on an engineered, transparent finite reference construction … a frozen intervention battery combining self/other attribution contrasts, interchange, ablation, restoration, downstream clamps … fail-closed analysis".
   - **Closeness: PARTIAL on claim (3).** It is pre-registered known-answer validation of a self-related causal assay on an engineered system. That is the Stage-0 *concept*, in a different construct and with no agent learning.
5. **S. Akiyama, "Measure the Instrument First: Preregistered, Prediction-Sealed Calibration of Four Endpoints…"**, Zenodo 21983630, 18 Aug 2026. Description only.
   - Pre-registered "known-answer fixtures" used to calibrate instruments before application, for LLM distillation endpoints.
   - **Closeness: PARTIAL on claim (3)**, as a method precedent from another domain.
6. **Others, DIFF:**
   - 18193509: RL ablation of interoception vs global modulation in a toy environment (software; no self-model).
   - 20587698: self-model weight ablation in iterated-cooperation agents (not homeostatic).
   - 19738204: attention-schema transplant assay in a toy neural agent (preservation and transfer, not necessity for viability).
   - 22989382: Kulma's six-step indicator-validation protocol (general method; cite alongside Butlin and Seth & Bayne).
   - 21745212: García Hernández V2, a pre-registered global-access workshop in artificial life (not a learned-network RL agent; description only).
   - 23306276: Mulani, a proposed ablation programme (no data).
   - 23413881 and 23417397: Craggs synthesis and revised architecture (Part 2).

### 5.2 Registered Reports

- **COS list** (https://www.cos.io/initiatives/registered-reports, fetched). It lists *participating journals*, not studies, and has no study search: **NOT SEARCHABLE BY TOPIC**. Journals relevant to us on the list include *Neuroscience of Consciousness*, *Computational Psychiatry* and *Computational Communication Research*. Their RR content was not searched individually.
- **PCI Registered Reports** (rr.peercommunityin.org web2py grid, `?keywords=v_article.title contains "<t>" or v_article.abstract contains "<t>"`; first results page only). Distinct recommendation IDs per query:

| Term | Hits | Relevant |
|---|---|---|
| reinforcement learning | 3 | 0 (human craving; bird learning) |
| artificial agent | 0 | — |
| homeosta | 1 | 0 ("Allostatic Interoception in…", 31 Dec 2024, human) |
| allosta | 1 | 0 (same) |
| interocept | 2 | 0 (human) |
| global workspace | 0 | — |
| self-model | 0 | — |
| neural network | 0 | — |
| artificial intelligence | 3 | 0 (deepfake-face perception) |
| consciousness | 12 | 0 (all human EEG or psychophysics) |

- **NeurIPS 2020 Workshop on Pre-registration in ML** (PMLR v148, 24 entries, all titles read): 0 relevant. The nearest is "Context-Adaptive Reinforcement Learning using Unsupervised Learning of Context Variables", which is unrelated to self-models.
- **Not searched:** journal-level RR pipelines individually, PCI RR beyond the first page, and later ML pre-registration workshops.

## Part 6. Verdicts

**Rule applied (Lead).** A prior study makes Q-NECESSITY a replication or extension only if it tests the necessity of a **learned self-model in a learned agent**. Against that rule:
- **Craggs:** not learned, not an agent in the learning sense. Fails both conditions.
- **Wilterson & Graziano:** learned RL agent, but a supplied, not learned, self-model. Fails.
- **Valerio Porras:** learned body and metacognitive models, but a hand-coded policy. Fails "learned agent".
- **García Hernández:** running-mean estimator, hand-written rule. Fails.
- **Phua 2025 (v1.1 B.3) meets the rule's letter:** a learned z_self (supervised auxiliary loss) in a learned (behaviour-cloned) agent, lesioned with first-order behaviour measured (88.5% → 88.2%). Its self-model is of **task confidence**.

**Does a non-body self-model make ours an extension or leave it novel? It leaves the claim as worded novel, with the paradigm credited.** Reasons:
1. Q-NECESSITY is a hypothesis about *what* the self-model carries: that a learned model of the agent's own **interoceptive or homeostatic state** is needed for **viability regulation**. A confidence model's necessity, or non-necessity, for task accuracy makes no prediction about that.
2. Phua's z_self was by design not routed to first-order action (v1.1 B.3), so its null tests a different causal path.
3. The remaining conjuncts are also absent from Phua: RL, viability outcome, same-size ablations of *other* modules, matched arms, pre-registration.

What is **not** novel is the generic **lesion-necessity paradigm for self-models in agents** (Phua 2025 learned; Wilterson & Graziano 2021 RL with supplied schema; Craggs 2026 hand-coded, pre-registered). The claim must not be worded as "first test of whether an agent needs its self-model".

| Claim | Verdict | Reasoning |
|---|---|---|
| (1) Q-NECESSITY: learned RL agent's interoceptive self-model necessary for viability, vs same-size ablations of other modules and matched arms | **STILL NOVEL AS FAR AS FOUND** (narrowed) | Content-specific, as argued above. Closest precedents to cite: Wilterson & Graziano 2021 (RL, retrained necessity of a supplied attention schema); Phua 2025 (learned confidence model, BC); Craggs 2026 Block V (pre-registered, hand-coded, competence; H5.6 REDUCE by external bypass); Valerio Porras 2026 (learned body predictor, hand-coded policy); Asan 2026 (PPO homeostatic agent, random-subspace-matched lesions of affect subspace, interoceptive input masking). Would drop to EXTENSION only if Astra rules that the claim is the generic paradigm rather than its interoceptive and viability instance. |
| (2) SELF: agent predicts its own internal variables better than an outside observer trained on the same behaviour | **STILL NOVEL AS FAR AS FOUND** | No hit trains an observer on the agent's behaviour. The nearest are Craggs H5.5 (self-monitor vs world-only difficulty estimator, hand-coded), Valerio Porras Φ (predicts own error, no observer) and Felix 2026 (self-report vs majority or shuffled baselines). Binder et al. 2024 remains the source design. |
| (3) Stage-0 known-answer gate validating instruments before use | **PARTIAL OVERLAP** | Pre-registration itself was already partial overlap (v1.1). The *gate concept* now also has precedent: pre-registered known-answer calibration of instruments (Akiyama 2026, LLM endpoints), pre-registered validation of a self-related causal assay on an engineered transparent system with fail-closed analysis (Bankuti 2026), and a prospective sensitivity and specificity validation protocol for consciousness-indicator claims (Kulma 2026). What survives as far as found: the gate applied to *this battery* (Q-EXIST, Q-CAUSE, Q-NECESSITY, Q-LEARN, IGN, BCAST, SELF) for internal-state instruments in learned agents, with planted dependency, matched null and **imitating confounds**, and **CONFOUND NOT REALIZED → UNRESOLVED** blocking. Suggested wording: "a Stage-0 known-answer and confound gate for this instrument battery, following prior known-answer validation practice (Akiyama 2026; Bankuti 2026; Kulma 2026)". |

**Recommendations.** These are not rulings; nothing changes until the Lead and Astra rule.
- Cite Wilterson & Graziano 2021 (Crossref title), Craggs Block V results (zenodo.23321474 and .23321507; synthesis .23413881), Valerio Porras 2026 and Asan 2026 in the Q-NECESSITY and Q-CAUSE prior art.
- Consider an externally supplied (oracle) interoceptive-estimate arm for Q-NECESSITY, as in Craggs H_EXTERNAL.
- S-INT: cite Pardo et al. 2018 §3–§5 for truncate-and-bootstrap. State the recurrent-state bootstrap rule (v̂ on the pre-reset hidden state at the stop step) and keep the probe-AUC check that the agent cannot predict stops.

## Part 7. Limits

1. **Description-only items.** Bankuti 2026, Akiyama 2026, Kulma 2026 and García Hernández 2026 were assessed from their Zenodo descriptions only. They bear on claim (3) and, for García Hernández, on Q-NECESSITY. Reading Bankuti and Akiyama in full before freeze is recommended. Asan 2026 was keyword-searched, not read in full. Valerio Porras was read §3–§4 plus the abstract.
2. **Wilterson & Graziano.** The SI Appendix was not read (PNAS HTTP 403), and the DataSpace code was not inspected. Learning-rate quantification lives in the SI.
3. **Craggs.** Block V and B2 code were read; Blocks I B1, II, III and IV code was not. Their substrate is assumed to be the same style from the synthesis and Working Paper III, not verified. I did not audit the Craggs results or re-run anything.
4. **Zenodo coverage.** Only the top 25 per query by best match were screened. Unquoted first-pass queries are OR-matched and their totals are meaningless. Zenodo's free-text index covers metadata, not full text.
5. **Registered Reports coverage.** The COS list is a journal list; PCI RR was searched only on its first results page by title and abstract substring; PMLR v148 only. Journal-specific RR pipelines, AsPredicted (NOT SEARCHABLE, v1.1), ResearchBox and ClinicalTrials were not searched.
6. **Pardo.** Our extension to random stopping times is my derivation, not the paper's. Pardo tests fixed T only.
7. **General.** Absence of a hit is not evidence of absence. This is a targeted search, not a systematic review.

## Footer: inputs read (sha256)

- `/workspace/review/trackB_prior_art_verification_v1_1_prefreeze_CNA.md`: 29068cce219530f459a4a045f349393a2aea9db1253a4c76a654514284017928
- `/workspace/review/trackB_prior_art_verification_v1_CNA.md`: f2fd0ae6f5df571f6ed6ad413ff604ffcb975e565c91c991acf8c801c6104ac9
- `/workspace/tmp_pa2/pardo_1712.00378.pdf` (arXiv v4): 5bb677ee1a3d6916aedf7d6df74463238cfe792fc348976502f46c14998067c6
- `/workspace/tmp_pa2/pardo.txt`: 2d6db5b320108fdd00ced1790ddebb8904f23c997cfb2e306e92b048ffb4d4e0
- `/workspace/tmp_pa2/pardo_pmlr.pdf` (PMLR 80): 2c3ff9afe5de0c9646dd0e352ed30cdc29cc2a259f909bcb1bed6b14624f8426
- `/workspace/tmp_pa2/pardo_pmlr.txt`: 4722b30b57a58db8fd6ca20df401cc81d4324e5f015eeb454872205a14e188ac
- `/workspace/tmp_pa2/wg2021.xml` (Europe PMC PMC8379943): 3ed22817e76a3a872df53ae6ce7f1b1765e2c642a640b971a37056bd7a2296e1
- `/workspace/tmp_pa2/wg2021.txt`: 0196c9fbd612173c6c31ee472e4e7ee0c3620ca0a6b8647ef90353bd1bcba2ef
- `/workspace/tmp_pa2/reg2_jz4ed.json`: 1ad368e4b9f4e88f455f0aa03ebcbb23afd8d2976983d52d948ac4b651fcdd94
- `/workspace/tmp_pa2/reg2_gqanp.json`: 2e8bc95650ff35989044a03b73066f99e882ac2f3c15798a71dacb3a9a7bd7af
- `/workspace/tmp_pa2/reg2_69zny.json`: e96a185ad684b1f4f230b6fef077fede10874276c61db6cf64cb56d08bd3067a
- `/workspace/tmp_pa2/rel_jz4ed_resources.json`: 394f434de34643e438aefae3b87bdfc4f4c0eda38cd5e0e8ac27a0dbabccba8f
- `/workspace/tmp_pa2/rel_gqanp_resources.json`: 3c3d8b5c59cf2659b9cca7472351ecc847aab6b2d3a4fe329dd732087bb1d299
- `/workspace/tmp_pa2/rel_69zny_resources.json`: 337a5845bf62ccbe2bee6d47834c9d6317bc033ab935af60bc66d75c688ef71a
- `/workspace/tmp_pa2/sr_jz4ed.json`: 127d10aa221c13d997ca9b504a9132105269491b65b78cba12bd989a053c12f4
- `/workspace/tmp_pa2/sr_gqanp.json`: 94ef3f5f71adf0f8328ff91fcde4fb66ccb40faa40b333d09269b748d8f162fc
- `/workspace/tmp_pa2/sr_69zny.json`: 40ddad240a0356bda6cbcc24d4ef2a140b92d5813e9124956aba21636f19fad3
- `/workspace/tmp_pa2/arch_jz4ed.json`: d4a3c980afb681560d87426f245000939d7f4dbc466b4bdabcc69e419ab31490
- `/workspace/tmp_pa2/arch_gqanp.json`: 6869436362eb3673bc919ccd566deb96369cc3048b687645b8e87a98fd07a0bc
- `/workspace/tmp_pa2/arch_69zny.json`: 4e7341ac057992e4077263ec0e036261ca8bc7e06a6fbb8191802405f885bc49
- `/workspace/tmp_pa2/osfdl/BLOCK_V_PREREGISTRATION_OSF_PACKAGE.zip`: 045c0f8d13d00d4fc181becad533666230ee6f353c3c604226e16e927d1b8b5a
- `/workspace/tmp_pa2/osfdl/protocol.md` (Faeth 69zny): 966319b82111b9292427508e5e5edb12b3af105749bc7eb8be63712a88d781aa
- `/workspace/tmp_pa2/craggs/Block_V_Reflective_Self_Modelling_Software_v1.0.0_FINAL_NEW_DOIS.zip`: 583cbfcfdbc3d0a266f00c889f78c195eae3377ef317b11425b14abfe8e30287
- `/workspace/tmp_pa2/craggs/Block_V_Reflective_Self_Modelling_Confirmatory_Dataset_v1.0.0_FINAL_NEW_DOIS.zip`: 1995f643252d7f0075ec9aacf22bf8fe77eaa60b3600381d7c5e8cf01f8106cc
- `/workspace/tmp_pa2/craggs/From_Candidate_Hierarchy_to_Experimental_Dependency_Map_SOURCE_v1.0.0.zip`: fa4a4e7986b220f1bc45573f0740c4240a281d4a73b7a3a5fb65a9a3e2500a7f
- `/workspace/tmp_pa2/craggs/B2_Causal_Maintenance_Software_v1.0.0_FINAL.zip`: 190777727bac6cf6c642fe7943f74bb88743b16f8fd768934677d1a63eca414a
- `/workspace/tmp_pa2/craggs/Working_Paper_3.pdf`: bd77d57486731396bdfdb458fd48d86f1c10f527ef441d9d7ca1bc8abb27bf2c
- `/workspace/tmp_pa2/craggs/bv_sw/toe_exp/block5.py`: 066b17c16992cc0911ca143ad8317eaf76ed6fa16b72ffadca5c5ed7e4933f37
- `/workspace/tmp_pa2/craggs/bv_data/block5_confirmatory_analysis_record.json`: 6af92665648422744c1956b4aeb5e7e09c6bbd51071d5f386c8867606207bf01
- `/workspace/tmp_pa2/craggs/bv_data/BLOCK_V_CONFIRMATORY_EXECUTION_RECORD.md`: 6f3fd90ccfec52da1f880e5be8b5f005864a6aa30518a250a693020f1a50c4bb
- `/workspace/tmp_pa2/zen.py`: c3209224b58ca73d5413bcca1de6e173b3e9dbfb0123f139ded4b786f2f8278a
- `/workspace/tmp_pa2/zenodo_out.txt`: 1c4d58912d942a73adeb56b41d8dd261634d6383b182fb651bb76ee781003f06
- `/workspace/tmp_pa2/zenodo_results.json`: 151e97e917df81af9ec89d66a357fc7ed3884c1e28695a939b27c941f6b3d8b9
- `/workspace/tmp_pa2/zen2.py`: fce0063d9c5795a0ac31912579288224a687346c8b7eb89facd7a40208e1eb78
- `/workspace/tmp_pa2/zenodo_out2.txt`: e68490186a69df11dd65f5a8d4a4b8d7843332938413ada6df61d5400fb2d1cf
- `/workspace/tmp_pa2/zenodo_results2.json`: 183168ab29e5e8a5ddda6487cb42cdf845c21a905ccb8f5409e43dccd55ef22e
- `/workspace/tmp_pa2/zen/vp.pdf` (Valerio Porras v0.12): 9e04b43e9ea23e47861abf09e87f765cec0d33a1efda0a1da2c7120519137df9
- `/workspace/tmp_pa2/zen/asan.pdf` (Asan 2026): 82386e24bcf4fa85843606e5a0dcfeb39d1855528bfdbef473623c560a6caa69
- `/workspace/tmp_pa2/pcirr.py`: a0b904d39eb34b2c9ced286b70f691351651020b83eb9fc64c54c913947cb819
- `/workspace/tmp_pa2/pcirr_out.txt`: 29f9231adac3b6f8c6e14582834d3fa30dbb469cfd2bce9ee09ef7941017b862
- `/workspace/tmp_pa2/pcirr_results.json`: dd5751a9ff262433e54a62cda98b229dda32d178c4706c00fc3f39bbf021a470
- `/workspace/tmp_pa2/pmlr148.html`: d03d0a7f035aac36ef8698c0710799a073e65bf772920ec1e014fa46f65ef521
- `/workspace/tmp_pa2/cos_rr.html`: 581f75c9191b5501226048ee7731e6d655581c684aba305654b0d563d0048008
- **Read live, not saved:** OSF API records for the sibling registrations g3te5, jrcnb, euf2j, 8zwm7 and rehw5 (saved as reg2_*.json, not hashed here) and nodes vnmxz, dr3x5 (HTTP 401) and f3bkx; Zenodo record JSON for the screened IDs (zd_*.json and zen_*.json in /workspace/tmp_pa2); the Europe PMC search API record for 10.1073/pnas.2102421118; the PCI RR homepage.
---
