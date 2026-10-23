# Emergence conditions v2: corrections after Astra consultation #4

**Draft.** This is the additive successor to `emergence_conditions_v1.md`, which is left unchanged.

- **Written:** 2026-10-20 (EDT) by Research Delegate, for the ACI Research Specialist, on behalf of Aidan Ahern.
- **Scope:** theory and design only.
- **Run:** one small analytic replay script, outside the repo (§6).
- **Not done:** no training, no solver beyond that replay, no C4 study.
- **Repo:** `/workspace/repo` was not modified.
- **Claims:** no consciousness claim. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are labelled at every use.
- **Source of corrections:** `/workspace/astra_consult_1.md`, "Astra consultation #4". That file is a condensed record, so quoted wording means the wording recorded there.

---

## 0. Verdicts applied

> **Interpretation note** (added 2026-10-20 after the Specialist's rulings). The mapping of
> Astra's letters (a)–(e) to specific v1 claims, shown in the second column below, is **my
> reading**. The consultation record (`astra_consult_1.md`, "consultation #4") gives only
> the letters and the verdicts. It does not restate which claim each letter refers to. A
> reviewer with Astra's original prompt should check this mapping. If any letter maps
> differently, the matching v2 change should be re-examined. The verdict texts themselves
> are quoted verbatim as recorded.

Letters (a)–(e) are Astra's. The mapping to v1 claims is my reading, because the record does not restate the claims.

| | v1 claim (my mapping) | Astra #4 (verbatim as recorded) | v2 status |
| --- | --- | --- | --- |
| (a) | §0/E3: at sufficiency (ρ ≥ 1) a learner "has no pressure" to grow C3/C4 structure; anything that appears is explained by the rival "by construction" | "FALSE: capacity permits sufficient encoding, doesn't guarantee acquisition or causal organization; rho=logK/H(S)>=1 doesn't guarantee lossless storage (entropy != log support)." | **Withdrawn.** Sufficient capacity *permits* a sufficient encoding. It does not mean a learner acquires one, or acquires it in any particular causal organization. ρ is also the wrong sufficiency test. log K ≥ H(S) does not imply K ≥ \|supp S\|, so lossless storage is not implied. v2 defines the sufficiency control by **support**, K ≥ \|supp S\|, and reports ρ_H only descriptively. E3 is restated in §1. |
| (b) | C4-P1: scarcity alone cannot create a distinct evaluator ("access record is the memory code itself") | "exclusion unsupported; depends on diagnostic info/decisions." | **Withdrawn.** The clean-world certificate shows one optimal codebook in which access is part of the codeword. That does not exclude a distinct evaluator once diagnostic information or decision structure changes. Graded evidence, delayed queries and separate deferral decisions are examples. The status is now UNRESOLVED. |
| (c) | C4-P2: non-stationary reliability "reduces standalone" (rank 0, "decided") | "strong conventional explanation, not disqualification; learned filter can evaluate own channel — identify referent and causal role." | **Re-scoped.** The joint/volatility filter is logged as the strongest REDUCTION candidate. It does not disqualify ORIGIN or ROLE. A learned filter can evaluate the agent's own channel. The task is to identify the referent and the causal role. Rank 0 is removed. |
| (d) | C3-P4: multiple consumers are a C3 pressure "only below sufficiency" | "FALSE: distributed info, comms constraints, coordination make routing matter despite ample storage." | **Withdrawn.** Routing can matter with ample storage when information is distributed, communication is limited or coordination is required. The protocol draft now includes an ample-storage, limited-channel condition. |
| (e) | P1×P3: hidden decay "provides" C4's temporal separation, making it the leading C4 candidate | "plausible opportunity, not sufficient; need accessible evidence distinguishing damage states." | **Downgraded** to "plausible opportunity". Stale records are not enough. The agent also needs **accessible evidence that distinguishes damage states**. The §4 test varies exactly that evidence. |

**Ruling on unlabeled agreement (R-A1, v2 queue).** Astra: "correct for distinctiveness; but don't use it to veto emergence." From here on, R-A1 bears **only on REDUCTION**. It never decides ORIGIN or ROLE. The v1 caveat C3, which used R-A1 to cap rank 2 at "constructive equivalence", is withdrawn as an *emergence* verdict. It stays valid as a REDUCTION prediction.

---

## 1. Ledger format and the emergence bar

### 1.1 Three judgments per mechanism

Every mechanism gets three separate judgments (Astra #4). They never collapse into a single verdict.

| Judgment | Values | Answers | Question type |
| --- | --- | --- | --- |
| **ORIGIN** | SUPPLIED / ACQUIRED / UNRESOLVED | Was the organization put in by design, or acquired through the declared developmental process? | Q-LEARN |
| **ROLE** | Free text, plus a status of VERIFIED / CANDIDATE / NONE | What does it represent (its referent), and what does it causally do, by intervention? | Q-CAUSE (Q-EXIST as precondition) |
| **REDUCTION** | REDUCED-to-X / NOT-REDUCED-vs-X / UNRESOLVED | What is the simplest mechanism that reproduces the whole intervention-response pattern at parity? | Q-NECESSITY / distinctiveness |

The three are independent. A mechanism can be ACQUIRED, have a VERIFIED role, and still be REDUCED. That combination is a legitimate emergence result about an ordinary mechanism. M1 shows the separation (Astra: "M1 stays REDUCED; origin separate"): ORIGIN is SUPPLIED, because M1 was designed; ROLE is CANDIDATE; REDUCTION is REDUCED to adaptive-threshold selective prediction.

### 1.2 Emergence bar (Astra #4, verbatim as recorded)

> "acquired via declared developmental process, organization not explicitly supplied, causally verified."

So **EMERGED ⇔ ORIGIN = ACQUIRED and ROLE = VERIFIED.** REDUCTION is reported but is **not** part of the bar. This replaces v1's E1–E6 as follows:

| v1 | v2 |
| --- | --- |
| E1 not supplied | Kept, as part of ORIGIN. Includes Astra's post-development controls "for supplied slots/targets/labels/protected histories". |
| E2 pressure-dependence | Kept as **diagnostic evidence about which pressure did it**, not as part of the bar. A structure can be acquired without the pressure being causal. |
| E3 collapse at ρ ≥ 1 | **Withdrawn as a requirement** (verdict a). Replaced by sufficient-capacity and unpaid-upkeep *controls*. At the controls the representability certificate predicts no reward advantage. Acquisition is still possible there, so a structure found at a control is logged, not discarded as a bug. |
| E4 ceiling-separated | Kept. The analytic optimum is a Q-EXIST/representability ceiling. **"Optimal codebook != acquired organization"** (Astra #4). |
| E5 decoder-free | Kept. |
| E6 conjunction (C4) | Kept for ROLE in C4. It does not enter ORIGIN. Astra #4 adds: "No universal evaluator-vs-controller signature". The conjunction is applied per mechanism, never as a generic test. |

---

## 2. Revised ledger: v1 pressures

ORIGIN is UNRESOLVED for every row: nothing has been developed or trained. The ledger records what each judgment currently rests on, and what would settle it.

| Mechanism | ORIGIN | ROLE (referent; causal role) | REDUCTION (strongest simpler candidate) |
| --- | --- | --- | --- |
| C3-P1 shared maintained content under paid upkeep | UNRESOLVED | CANDIDATE. Referent: which contents are kept alive. Role: joint availability to consumers. Q-EXIST is small-positive at fixed K (replayed, §6); not shown for paid upkeep. | UNRESOLVED vs static duty cycle + observable threshold (Phase II), random-allocation yoke, adaptive selection comparator |
| C3-P2 shared reliability-weighted estimate | UNRESOLVED | CANDIDATE. Referent: current channel reliabilities. Role: common reweighting across consumers. | Strong candidate: scalar/joint-filter broadcast (Phase III template). Lag-coherence separates shared vs private only. |
| C3-P3 shared re-routing after own-machinery damage | UNRESOLVED | CANDIDATE. Referent: which pathways still work. Role: routing for all consumers. | UNRESOLVED vs redundancy + vote (Sub A) and per-consumer error-driven relearning |
| C3-P4 routing across specialist consumers | UNRESOLVED | CANDIDATE, **including at ample storage** (verdict d) when the information is distributed or the channel is limited | UNRESOLVED vs static partition of the channel, free code at the same channel, adaptive selection comparator |
| C4-P1 access/deferral record under scarcity | UNRESOLVED | CANDIDATE. The v1 exclusion is withdrawn (verdict b). It depends on whether the diagnostic information or decisions let an evaluator-like state diverge from content. | UNRESOLVED vs same-K monolithic readout (P(correct\|m) as a function of m), `no_opt`, static opt-out |
| C4-P2 learned evaluation of own channel | UNRESOLVED | CANDIDATE (verdict c: "learned filter can evaluate own channel"). Referent and role must be identified. | **Strong conventional candidate**: joint/volatility filter; adaptive conformal. Per R-A1, unlabeled self-consistency adaptation also counts as conventional *here and only here*. |
| C4-P4 producer-side tag for consumers | UNRESOLVED | CANDIDATE | Strong candidate: scalar LLR broadcast (Phase III) |
| **C4-P1×P3** state mediating verification/routing/deferral/maintenance under hidden decay | UNRESOLVED | CANDIDATE, "plausible opportunity, not sufficient" (verdict e). It needs accessible damage-distinguishing evidence (§4). | UNRESOLVED vs per-pathway adaptive selective prediction, redundancy + vote, elapsed-time threshold |
| M1 (for reference) | **SUPPLIED** | CANDIDATE | **REDUCED** to adaptive-threshold SP (queue v2 §3.2; R-A1) |

**Revised ranking of cheapest falsifiers.** None needs a new architecture family.

1. **C3 scarcity_v2 pressure-and-representability certificate.** See `scarcity_v2_protocol_draft.md`. It is analytic, and it is authorized under standing approval because it is C3, not C4. It covers C3-P1, C3-P4 (including the ample-storage limited-channel condition) and the C3-P3 re-routing analogue.
2. **C4-P1×P3 decoder-free design** (§4). **Gated behind C4 approval; design only.**
3. **C4-P2 referent/role identification against the joint filter.** This is C4-CMP1 in the queue v2. **C4-gated**, and parameters stay unset (R-A2).
4. **C4-P1 and C4-P4.** Each depends on the outcome of 1 or 2. **C4-gated.**

v1's rank 0 is removed (verdict c), and so is v1's ρ ≥ 1 "bug" rule (verdict a).

---

## 3. Additional pressures: social modelling, curriculum and developmental staging, intrinsic motivation

> **Status: all three are GATED or DESIGN-ONLY.** Each is kept here as a ledger entry and a
> design sketch only. **None is in the scarcity_v2 scope**, which excludes them explicitly
> (`scarcity_v2_protocol_draft.md` §0.1).
>
> | Pressure | Status | Gate |
> | --- | --- | --- |
> | Social modelling | **GATED** | Its self-evaluation part is C4, so it needs Aidan's approval. **If the multi-agent world needs a new agent class, that counts as a new architecture family. It goes to Aidan** (constitution v3, human gates) before any further design. |
> | Curriculum / staging | **DESIGN-ONLY** | Its analytic part (is the scarcity-optimal codebook still optimal at sufficiency?) would need its own card. Any staged development run is training, which needs a separately approved protocol. |
> | Intrinsic motivation | **GATED** | Competence tracking evaluates the agent's own state, so it is C4 and needs Aidan's approval. |

This section answers task (3) and uses the same format as v1 §2–3. The rows below are also ledger entries; ORIGIN is UNRESOLVED for all of them.

### 3.1 Social modelling: predicting other agents

- **Why it might produce C3/C4 structure.**
  - An agent that must predict *other* agents' behaviour has to represent that other agents act on their own, possibly false, beliefs.
  - Rabinowitz et al. (2018) trained an observer network by meta-learning on behaviour alone. It came to predict that agents with limited view persist on false beliefs after unseen object swaps.
  - The authors attribute this to "observing competent agents acting in POMDPs" rather than to a special architecture.
  - The attention-schema line (Graziano & Webb 2015) proposes that a model built to track *others'* attention is reused for the self. That proposal is the theoretical motive. It is not evidence.
- **C4 candidate.**
  - A belief-about-belief state learned for others is reused to evaluate the agent's own state: "my view did not include X, so my belief about X may be stale".
  - **Referent:** the agent's own observational access.
- **Emergence signature (decoder-free).**
  1. **Self-referent test.** Covertly change something outside the agent's own field of view (a system/access change), compared with a matched change inside its view (an evidence change). Deferral, verification or information-seeking should rise only for the out-of-view case.
  2. **Other-referent check.** The same pattern holds when the agent predicts another agent.
  3. **Shared-substrate test.** Lesion or perturb the other-model pathway, which is identified by its effect on *other*-prediction. Self-deferral should be affected in the same direction, with a matched rescue.
  - Pathways are identified by their causal effect on a task, not by a probe.
- **Conventional rival.**
  - A first-order world model that tracks "time since last observed" for each object, plus a threshold. That predicts the self-referent result without any social reuse.
  - Ordinary parameter sharing in a multi-task network (Yang et al. 2019). That predicts some lesion overlap without a self-model.
  - The discriminator is **directional, content-specific** cross-transfer with a matched rescue, not just lesion overlap.
- **Gate: GATED.** The C3 part (a shared access-tracking state used for both other and self) could be designed analytically, but only in a separate card, not in scarcity_v2. The self-evaluation part is **C4-gated**. **If the world needs a new agent class, that counts as a new architecture family. It goes to Aidan.**

### 3.2 Curriculum and developmental staging

- **Why it might produce the structure.**
  - Staged exposure can change *which* organization is acquired, even at the same final capacity, data and compute.
  - Elman (1993) found that a recurrent network learned grammatical structure only when training "started small": either the input was staged, or memory grew over training.
  - Bengio et al. (2009) formalized curriculum learning as an ordering effect on what is learned and how quickly.
- **Relevance here.**
  - Staging is a direct test of verdict (a)'s point that capacity permits but does not guarantee acquisition.
  - Two developmental paths with identical final K, budget and data can reach different organizations.
  - **Concrete C3 version.** Develop under scarcity first (ρ < 1) and then relax to sufficiency, compared with sufficiency throughout. If a selection or routing structure acquired early is retained after relaxation, and the reverse order does not produce it, the organization is *path-dependent*. That is a clean ORIGIN result.
- **Emergence signature.**
  - **Hysteresis.** At identical final conditions, the staged agent shows the C3 intervention signature from v1 §2: covert maintenance withdrawal degrades all consumers together. The unstaged agent shows the private-copy pattern.
  - **Reversal test.** Re-staging the unstaged agent through scarcity installs the signature. Holding it at sufficiency does not remove the signature from the staged agent.
- **Conventional rival.** Optimization path-dependence with no organizational content: staging lands in a different basin that happens to share content.
  - Discriminator: the whole intervention-response pattern. A shared structure predicts *coordinated* multi-consumer effects; a different basin predicts arbitrary ones.
  - Second rival: curriculum as cheaper approximate inference, which is engineering, not organization. Constitution v3 keeps that question type separate.
- **Gate: DESIGN-ONLY.** Staging changes the developmental process. It does not change the architecture family. Any staged Q-LEARN run is training, which needs a separately approved protocol. The analytic part asks whether the scarcity-optimal codebook remains optimal or near-optimal at sufficiency, so that a retained structure is not penalized. That part is cheap and is C3.

### 3.3 Intrinsic motivation: curiosity and learning progress

- **Why it might produce the structure.**
  - Learning-progress objectives reward the agent for the *change in its own predictive competence* (Oudeyer, Kaplan & Hafner 2007; Gottlieb et al. 2013).
  - Optimizing learning progress pressures the agent to keep an estimate of its own competence per region. That estimate has an agent referent (its own learning state) and a native causal role (choosing what to explore).
- **E1 / ORIGIN risk.**
  - Most implementations *supply* the evaluator. Pathak et al. (2017), for example, compute curiosity as the forward-model prediction error, delivered as an intrinsic reward. The "self-evaluation" there is a supplied target.
  - Such systems are **ORIGIN = SUPPLIED** for the evaluator. Only the *use* of it can be ACQUIRED.
  - Pathak et al. also report that learning progress is hard to measure, which is why prediction error is the common proxy.
- **Clean design.** An emergence-relevant version must not hand the agent its own error or progress signal. It should use only extrinsic reward in a world where *choosing what to practise* pays off, for example where skills decay without practice (connecting to P1). Any acquired competence-tracking state is then ACQUIRED, not SUPPLIED.
- **Emergence signature (decoder-free).**
  1. **Referent separation.** Covertly change the agent's competence (system change, e.g. degrade one skill pathway) compared with changing the region's difficulty (evidence/world change), at matched observed error rates. Practice allocation should respond differently to the two.
  2. **History transplant.** Swap the practice/outcome history for one region while holding the first-order skill state. Directional misallocation should follow, with matched rescue.
- **Conventional rival.** Count-based or error-driven exploration bonuses computed from first-order loss (prediction error *is* a first-order readout). Also an adaptive bandit over regions using outcome history. By R-A1 that rival is conventional for REDUCTION.
- **Gate: GATED.** Competence tracking is evaluation of the agent's own state, so it is **C4-gated** beyond analytic representability. The decay-of-practice world is a P1-type world, and its C3 part (selection of what to keep practised) fits the scarcity_v2 certificate family.

| Pressure | ORIGIN | ROLE | REDUCTION candidate | Gate |
| --- | --- | --- | --- | --- |
| Social modelling | UNRESOLVED | CANDIDATE (own observational access; deferral via reused other-model) | Time-since-observed threshold; multi-task parameter sharing | **GATED**: self-evaluation is C4; a new agent class counts as a new architecture family and goes to Aidan |
| Curriculum/staging | UNRESOLVED | CANDIDATE (path-dependent C3 selection/routing) | Optimization basin path-dependence; engineering speedup | **DESIGN-ONLY**: needs a separate card; training needs separate approval |
| Intrinsic motivation | UNRESOLVED (SUPPLIED if progress signal given) | CANDIDATE (own competence; practice allocation) | Error/count bonus; adaptive bandit | **GATED** (C4) |

---

## 4. P1×P3: Astra's decoder-free test (design only, behind the C4 gate)

**Status.** **C4-gated** (constitution v3, "first C4/C5/C6 studies"; Ruling R-A2 by analogy). This is design only. Decay rates, budget, evidence accuracy and costs are **unset**.

**Astra #4, verbatim as recorded:**

> "P1xP3 decoder-free test: match first-order content/resources/upkeep history while varying diagnostic evidence about own machinery; acquired state mediates native verification/routing/deferral/maintenance; intervene holding full first-order state -> directional evaluative errors, downstream consequence, selective rescue; post-development, controls for supplied slots/targets/labels/protected histories. No universal evaluator-vs-controller signature."

**Design steps:**

1. **Development.** The agent develops under the declared process. It has a maintenance budget below demand and hidden per-pathway decay. It also has an **accessible diagnostic channel**: some observable that is statistically related to which pathways have decayed, such as a self-test outcome or a pathway-specific latency. This is the "accessible evidence distinguishing damage states" required by verdict (e). Without it, the design is not admissible.
2. **Matching.** Build matched trial pairs that are identical in:
   - first-order content (the same items, looks and cue);
   - resources (the same budget remaining and the same K);
   - **upkeep history** (the same refresh decisions).

   The pairs differ **only in the diagnostic evidence** about the agent's own machinery. For example, the self-test outcome for pathway A is "ok" in one and "degraded" in the other, while the true decay state is fixed by design.
3. **Mediation (ROLE).** The test is whether an acquired state mediates the agent's native verification, routing, deferral or maintenance responses to the diagnostic difference. Examples are re-checking, re-routing away from A, deferring A-dependent queries, and spending upkeep on A. The responses are the agent's own actions. No supplied readout is used.
4. **Intervention holding the full first-order state.** Hold the first-order state fixed and alter the diagnostic-driven state, using a history transplant of the *diagnostic* history only. Predicted outcomes:
   - **directional evaluative errors**, such as deferring when A is intact or trusting A when it has decayed;
   - one pre-declared **downstream consequence**, such as misdirected upkeep in the next cycle;
   - **selective rescue**: restoring the true diagnostic history reverses those errors and only those.
5. **Post-development controls (ORIGIN).** Show that the organization was not supplied. Rule out:
   - supplied slots, such as a dedicated damage register;
   - supplied targets or labels, such as a damage-prediction loss;
   - **protected histories**, i.e. a history buffer exempt from decay or from the budget.

   Each control must remove the candidate's advantage, or must show that the advantage never depended on it.
6. **No universal signature.** Per Astra, there is no universal signature that separates an evaluator from a controller. The mechanism is classified by its specific referent and role under these interventions. The design does not label it a generic "evaluator".
7. **REDUCTION (separate).** Run the same interventions on per-pathway adaptive selective prediction, which conditions on the diagnostic channel and outcome history. Also run them on redundancy + vote and on an elapsed-time threshold. Compare the whole response pattern. R-A1 applies here only.

**Open problem O1 (carried from v1).** "Hold the full first-order state" still needs a partition. Step 4 avoids a decoder by transplanting the diagnostic *input history* rather than an internal state. This is clean only if the diagnostic history enters the agent through a channel the first-order pathway does not also read. Whether that holds is a property of the world design, and it must be shown before any run.

---

## 5. Caveats

- **C1. The (a)–(e) mapping to v1 claims is my reading.** The record gives only the letters and verdicts.
- **C2. Support-based sufficiency.** The sufficiency control (K ≥ |supp S|) is defined for the finite worlds in the protocol. Graded worlds can have large supports, which may make the sufficient-capacity control expensive to certify exactly.
- **C3. Citations.** Both earlier partial checks are now resolved (§7).
  - Rabinowitz et al. (2018): authors and the ICML 2018 venue were verified on the arXiv API and the PMLR v80 page.
  - Pathak et al. (2017): authors and the ICML 2017 venue were verified on the arXiv API and the PMLR v70 page.
- **C4. Ruling applied.** If the social-modelling world needs a new agent class, that counts as a new architecture family and goes to Aidan (§3).
- **C5. Scope of the replay (§6).** It confirms the branch numbers under my reading of the definitions. The self-induced-uncertainty column is **UNDEFINED and EXCLUDED**. It was not replayed, and no definition was reconstructed (Specialist ruling).

---

## 6. Replay record (task 1)

- **Script:** `/workspace/scratch/scarcity_replay/replay.py`. Written independently from `SCARCITY_GAP_v1.md` §5. The branch script was not read or imported.
- **Method:** Fractions are converted to common-denominator integers and evaluated by exhaustive search over all codebooks of size min(K, |rows|). This is exact. It took 49 s.
- **Output:** `replay_results.json` and `run.log`.

**Result: MATCH.**

| Quantity | Branch claim | Replay |
| --- | --- | --- |
| Max access value (K < 8) | 1/24 | **1/24** (v=1/3, r=3/4, K ∈ {3,6}) |
| Max selection value (K < 8) | 1/8 | **1/8** (v=3/4, r=1/2, K=2) |
| Access > 0 cells | 14/63 | **14/63** |
| Selection > 0 cells | 24/63 | **24/63** |
| Both > 0 | 2/63 | **2/63** |
| Collapse at K=8 | 9/9 | **9/9** (full=1, access=selection=0) |
| Access never at K ∈ {1,2,4} or r=1/2 | stated | **confirmed** |
| Selection 0 when v=1/3 | stated | **confirmed** |
| Slice values (v=1/3,r=3/4: K=3 7/8, 5/6; K=4 11/12; K=6 23/24, 11/12; v=3/4,r=1/2: K=2 7/8, 3/4; K=4 15/16, 5/6) | stated | **all match** |

**One benign difference.** At v=1/3, r=3/4, K=3 my solver returned the codebook `00- 01- 1--`, while the branch reports `0-- 10- 11-`. Both attain 7/8, and they are mirror-symmetric under swapping the roles of items 0 and 1. The optimum is therefore **not unique**. This matters for the protocol: any role claim must hold across *all* optimal codebooks (scarcity_v2 §6).

**Definitions I assumed**, read from the .md:

- uniform cue;
- q = c with probability v, otherwise uniform over the other two;
- static = all codewords share one opt-out pattern;
- no_opt = no opt-out codewords;
- cue_blind = encoder sees items only;
- access value = full − static;
- selection value = full − cue_blind.

---

## 7. Citations

### New in v2

| Ref | Status |
| --- | --- |
| Rabinowitz, N. C., Perbet, F., Song, H. F., Zhang, C., Eslami, S. M. A., & Botvinick, M. (2018). Machine theory of mind. *Proceedings of the 35th International Conference on Machine Learning* (ICML 2018), PMLR 80:4218–4227. arXiv:1802.07740 | **Verified.** The six authors were checked on the arXiv API (as "Neil C. Rabinowitz, Frank Perbet, H. Francis Song, Chiyuan Zhang, S. M. Ali Eslami, Matthew Botvinick") and on the PMLR v80 page, which gives the same six names with the middle initials dropped. Venue and pages are from PMLR. The arXiv full text was read for the content claims. |
| Elman, J. L. (1993). Learning and development in neural networks: the importance of starting small. *Cognition* 48:71–99. doi:10.1016/0010-0277(93)90058-4 | Verified (Crossref) |
| Bengio, Y., Louradour, J., Collobert, R., & Weston, J. (2009). Curriculum learning. *Proc. ICML 2009*, 41–48. doi:10.1145/1553374.1553380 | Verified (Crossref) |
| Oudeyer, P.-Y., Kaplan, F., & Hafner, V. V. (2007). Intrinsic motivation systems for autonomous mental development. *IEEE Trans. Evolutionary Computation* 11:265–286. doi:10.1109/tevc.2006.890271 | Verified (Crossref) |
| Gottlieb, J., Oudeyer, P.-Y., Lopes, M., & Baranes, A. (2013). Information-seeking, curiosity, and attention: computational and neural mechanisms. *Trends in Cognitive Sciences* 17:585–593. doi:10.1016/j.tics.2013.09.001 | Verified (Crossref) |
| Pathak, D., Agrawal, P., Efros, A. A., & Darrell, T. (2017). Curiosity-driven exploration by self-supervised prediction. *Proceedings of the 34th International Conference on Machine Learning* (ICML 2017), PMLR 70:2778–2787. arXiv:1705.05363 | **Verified.** The four authors were checked on the arXiv API and the PMLR v70 page; venue and pages are from PMLR. The arXiv full text was read for the content claims. Crossref also lists a CVPR-workshop 2017 version, doi:10.1109/cvprw.2017.70, which is not cited. |

### Carried, verified earlier

These were verified in `emergence_conditions_v1.md` §8 and in queue v1 §7:

- Graziano & Webb 2015
- Yang et al. 2019
- Song et al. 2017
- Fleming & Daw 2017
- Gibbs & Candès 2021

### Repo sources

These are as listed in v1:

- master `32cfbe6`
- branch `origin/elminster/loving-ptolemy-ityj4l` @ `33fa803`, read via `git show`
