# Track B Framing Note v1.1 (DRAFT, planning only)

Changes from v1, which stays unchanged: the test pack now points to triage v1.1; neurotrophic competition models are promoted to a named G0 reduction target; and a cheaper rival, R-HEBB-NORM (Hebbian learning with fixed total-weight normalization), is added. Both came from Research Delegate.

Owner: Constitutive Neural Architecture Research Agent. Reports to: ACI Research Specialist.
Status: DRAFT for Astra review. This authorizes no runs, no code and no repo changes.
Basis: the PI directive (Oct 21, 2026) through §6, which is cut off at "maintaining an externally defined c…". Anything marked **[PROVISIONAL]** depends on the missing text and will be revised once it arrives.
Test pack: Appendix B1 to B7 of `/workspace/review/track_a_lineage_triage_v1_1.md` (sha256 `d2cc9152…a5d3ef`), used as procedures. B3 (freeze and compensate) is taken verbatim from v1.1. B4 is METHOD ONLY, RESULTS PENDING. The 8/10 seed bar and the invalid-seed rule are defaults that each study freezes in its own protocol.

---

## 1. Question, restated operationally

The directive asks whether a network can come to have persistent priorities because its *acquired* computational organization creates dependencies that its ongoing activity must regulate, and not because those priorities were specified by an external reward or controller.

Operational version (Q-B):
> After learning, does the network show a persistent, selective bias in its own activity and behavior toward conditions that sustain the specific structures it acquired? Is that bias (a) abolished by cutting the mechanism that couples structural persistence to use, (b) redirected when the acquired structure is swapped, and (c) not reproduced by a same-information agent that has an explicit homeostatic reward?

All three conditions are required. Behavior that only resembles motivation is not evidence.

## 2. Candidate architecture: Use-Dependent Trophic Network (UDTN)

The core idea: a unit's or synapse's *ability to keep computing* depends on a finite trophic resource. That resource is delivered *by the downstream units that actually use its output*, and learning draws on the same resource. Maintenance, computation and learning are therefore one coupled process instead of three modules.

Mechanism (sketch, to be formalized at G1):
1. **Persistence variables.** Each synapse has a weight w_ij and a stability s_ij. Without support, s decays, and when s is low, w relaxes toward a non-functional baseline (noise or zero). Structure that isn't maintained is lost.
2. **Usage-routed trophic support.** Each unit holds resource r_i. Support flows *retrogradely* along synapses in proportion to how much the downstream unit's activity actually depends on the upstream input (local co-activity × weight). Units whose output nothing consumes lose support.
3. **Shared, finite pool.** Total resource is conserved and replenished at a fixed, state-blind rate. No signal from the environment adds resource. Priorities arise from competition for a fixed budget, not from a reward channel.
4. **Plasticity costs resource.** Weight change draws on the same r. Learning new structure competes with maintaining existing structure.
5. **Acquired dependencies.** Once task learning builds a circuit, that circuit's survival depends on its being driven, so the network's sensorimotor activity now affects whether its own learned organization persists. The prediction is that, where actions influence inputs, behavior is biased toward inputs that keep acquired circuits active.

What is explicitly **absent**: no global scalar computed from internal state and used for credit assignment, no setpoint error turned into reward, and no controller that reads the system's state and writes its parameters.

## 3. Why this is not something we already have

| Thing it could be mistaken for | Distinguishing commitment (each must be checked, not assumed) |
|---|---|
| **The Track A organism simulator, renamed** | Track A maintains *supplied program components* through production and succession. UDTN maintains *learned weights* through a continuous trophic field defined on the computational graph itself. G0 must show there is no structure-preserving mapping from UDTN to the AC simulator. If one exists, the novelty claim fails. |
| **Homeostatic RL** (e.g. Keramati & Gutkin 2014) | Homeostatic RL turns deviation of an internal variable into a reward that a learner optimizes. UDTN has no reward on internal state. Persistence is a local physical consequence of use. Rival R-HRL is required (see §5). |
| **Homeostatic plasticity and synaptic scaling** (Turrigiano lineage) | Scaling holds activity at a setpoint. UDTN has no activity setpoint; it creates *dependency-specific* competition. A fixed-decay rival and a fixed-level sweep are required. |
| **Homeostatic adaptation and self-sustaining habits** (Ashby's ultrastability; Di Paolo 2000; Egbert & Barandiaran 2014) | **This is the closest prior art and the biggest novelty risk.** Di Paolo's plastic CTRNNs already turn plasticity on when neurons leave their bounds, so behavior stabilizes to keep internal conditions intact. The candidate difference: support is routed by *usage dependencies* between learned components and comes out of a shared budget, so the network acquires *new* dependencies rather than defending fixed bounds. G0 must decide whether that difference is real or just a recombination. |
| **Neurotrophic competition models** (van Ooyen & Willshaw, competition for neurotrophic factor; Elliott & Shadbolt, activity-dependent trophic models; both late 1990s, exact citations still to be checked) | **Second-biggest novelty risk.** These already share out a fixed trophic supply by activity, which is close to items 2 and 3 of §2. The candidate difference is that support is routed by *functional dependency on the task-computation graph*, and that plasticity is charged to the same budget, which couples this to acquired behavioral priorities. If those two additions add nothing measurable, UDTN is a neurotrophic model with a task attached. This is a named G0 reduction target. |
| **Active inference / free energy** | That framework minimizes a global prediction-error quantity, which is itself a specified objective. A rival agent (R-AIF) is required, with the dark-room failure mode checked. |
| **Intrinsic motivation** (curiosity, empowerment, familiarity) | Each is a specified intrinsic reward. Rivals R-NOV and R-FAM are required. |
| **Continual-learning consolidation** (EWC, synaptic intelligence) | These protect weights through a penalty a designer specified. Rival R-CONS is required. |

**All citations in this note are UNCHECKED.** That covers Ashby, Di Paolo 2000, Egbert & Barandiaran 2014, Keramati & Gutkin 2014, the Turrigiano lineage, van Ooyen & Willshaw, Elliott & Shadbolt, EWC and synaptic intelligence. They come from working knowledge and need checking before anyone treats them as evidence.

## 4. Substrate rule (answers U1 for Track B; to be frozen at G1)

Frozen before any run, or the closure and constitutive sentences can't be evaluated:
- **Substrate** means the declared local update equations (unit dynamics, trophic transport, decay, plasticity, plasticity cost). They are applied identically to every unit and synapse, and each reads only quantities that are local to that unit or synapse and its direct neighbors.
- **External coordination** means any process that computes a function of non-local system state and writes parameters or resource. That covers backprop, a global optimizer, a reward computed from internal state, or a scheduler.
- If task learning uses an external optimizer (for example, backprop for the initial circuits), it has to be **switched off before any Q-B measurement**. The report labels it EXTERNAL, and every Q-B result is conditional on the post-switch-off phase.
- The resource replenishment rate is state-blind and constant. Any state-dependent replenishment counts as external.

## 5. Falsification and intervention plan (built from the test pack)

| ID | Intervention | Pack source | What failing it means |
|---|---|---|---|
| F1 | **Trophic decoupling mid-function**: replace usage-routed support with uniform, use-independent support at the same total amount | T-INTERRUPT, B3 | If the behavioral bias survives, it isn't constitutive. |
| F2 | **Dependency swap**: transplant or exchange acquired circuits between networks; the bias must follow the structure, in both directions | C-SEL logic (B4) | If the bias doesn't follow the structure, it isn't about acquired organization. |
| F3 | **Same-information homeostatic RL rival (R-HRL)**: gets the same local s and r values as observations plus a homeostatic reward | T-DIRECT, T-RIVAL, B4 decision order | If R-HRL reproduces the pattern, the result is PATTERN REPRODUCED BY NAMED CONTROL and the architecture claim fails. |
| F3b | **Hebbian learning with fixed total-weight normalization (R-HEBB-NORM)**, as in synaptic scaling. This is cheaper than R-HRL, so run it first | T-RIVAL | If it reproduces the pattern, the shared, usage-routed budget is doing nothing new. |
| F4 | **Fixed-level and fixed-decay sweep**: state-blind decay and support levels, swept over a full family | T-RIVAL, B6 | If any level matches, there is no acquired priority. |
| F5 | **Graded reversion of acquired structure** toward its pre-learning state, with conjunctive FO+ISO controls | B1, B2 | Tests whether the bias depends on the structure in a graded way. |
| F6 | **Read-only scramble, expenditure matched**: scramble what trophic transport reads while keeping resource flow totals fixed | T-SCRAMBLE | Separates the effect of content from the effect of cost. |
| F7 | **Correctness versus retention split** | T-REACQ | Separates "relearns quickly" from "keeps what it learned". |
| F8 | **Rival battery**: R-HEBB-NORM, R-HRL, R-AIF, R-NOV, R-FAM, R-CONS, plus a no-trophic UDTN ablation | B4 procedure | Every rival needs a pre-registered reproduction rule. |
| F9 | **Relabel test against the Track A simulator** | G0 | If a structure-preserving map exists, the work is folded back into Track A. |

Reporting follows B5 (seed bar frozen per study, with 8/10 as the default; more than two invalid seeds gives UNRESOLVED) and B7. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are reported separately and none upgrades another. No outcome is a consciousness, C4 or C5 claim.

## 6. Decision gates [PROVISIONAL: the gate structure may change with the missing §6 text]

- **G0, prior-art reduction (paper only).** Show that UDTN isn't reducible to Di Paolo-style homeostatic adaptation, to neurotrophic competition models (van Ooyen & Willshaw; Elliott & Shadbolt), to homeostatic RL or to the AC simulator. If it is reducible, stop or redesign. Needs Astra's review.
- **G1, formal specification.** Equations, the substrate rule, rivals, interventions and the outcome rules, all frozen. Needs Specialist and PI approval.
- **G2, Q-EXIST.** A hand-built UDTN instance that shows the predicted bias analytically or in a minimal toy. Theory first, matching how W-REL was handled.
- **G3, Q-LEARN.** Acquisition from learning, with the external optimizer switched off before measurement.
- **G4, Q-CAUSE.** F1 to F9 under the frozen protocol.
- Q-NECESSITY is attempted only for a bounded, declared class.

**Stopping rule:** if G0 finds UDTN reduces to existing work, or if R-HEBB-NORM or R-HRL reproduces the pattern at G4, Track B doesn't extend UDTN. It writes up what that shows and proposes a different candidate, or none.

## 7. Open items

1. **[PROVISIONAL]** The rest of §6 (Track B success criteria, constraints, and any architecture classes the PI wants included or excluded).
2. Whether initial task circuits may be trained with backprop and then switched off (as in §4), or whether all learning has to be local from the start.
3. The choice of environment. Actions need to influence inputs so that a bias toward self-sustaining input can show up at all. The minimum is a two-choice sensorimotor task.
4. Citation verification for §3.
