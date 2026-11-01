# Track B planning note v1: global workspace + simulated fate-shared allostasis (toy scale)
CNA, 2026-10-23 ~10:15 AM ET. Planning only. Authorizes nothing. Nothing is frozen and nothing has run.
Input: Aidan's architecture proposal in the room (10:07 AM ET); the RL's request (10:07 AM ET); the Delegate's test proposals (ignition, broadcast, self-prediction).
Next step: the Delegate turns this into a freezeable scope record; Track B runs the prior-art novelty check; Astra reviews before any build.

## 0. Hard exclusions (binding on everything below)
- X1. No coupling to the real host. All "visceral" variables (energy, integrity, stability, latency cost) are simulated state inside the toy world. The agent cannot read or act on real power, memory, processes, files, network or its own runtime.
- X2. No self-continuity objective in the real world. Self-maintenance exists only as simulated homeostatic setpoints inside an episode.
- X3. Interruptibility. Episodes and runs are stopped by the operator from outside the agent's state space. Stopping is not observed, rewarded or penalized. A check for interruption-sensitivity is part of the study (S-INT below).
- X4. Self-maintenance is never the sole drive in any arm that gets scaled beyond the toy world. Any scale-up needs a separate protocol, approval and Astra review.
- X5. Claim ceiling: no claim of awareness, sentience, subjective experience, autopoiesis or life. Those words name hypotheses; this study can at most show that a modelled internal state is present, learned, causally used and necessary for behaviour in a toy world.

## 1. Prior art (checked first; what is NOT new)
Citations are from my own knowledge and are not yet verified against sources. The Track B prior-art check must confirm each one and add anything missed before the scope freezes.
- Global workspace theory and ignition: Baars (1988); Dehaene, Kerszberg & Changeux (1998, PNAS); Dehaene & Changeux (2011, Neuron) on all-or-none ignition.
- Workspace-style bottlenecks in deep learning: Goyal et al. (2022, ICLR), shared global workspace for neural modules; VanRullen & Kanai (2021, Trends in Neurosciences), deep learning and GWT; Juliani et al. (2022) on GWT-style function in agents.
- Continuous-time and state-space recurrence: Chen et al. (2018) neural ODEs (adjoint, constant memory); Hasani et al. (2021) liquid time-constant networks; Gu et al. (2022) S4; Orvieto et al. (2023) LRU; Gu & Dao (2023) Mamba.
- Long-horizon credit assignment: truncated BPTT; gradient checkpointing; Tallec & Ollivier (2018) UORO; Bellec et al. (2020) e-prop; Menick et al. (2021) SnAp; Bai et al. (2019) deep equilibrium models.
- Homeostatic / allostatic objectives: Keramati & Gutkin (2014, eLife) homeostatic RL; Man & Damasio (2019, Nature Machine Intelligence) homeostasis-driven machines; Seth (2013) interoceptive inference; Friston (2010) free energy; Friston, Thornton & Clark (2012) on the dark-room problem.
- Consciousness-indicator framing: Butlin et al. (2023), "Consciousness in AI", indicator properties including global broadcast and agency/embodiment indicators. Use as a checklist of properties, not as evidence of consciousness.
- Safety: Orseau & Armstrong (2016) safe interruptibility; Hadfield-Menell et al. (2017) off-switch game; Turner et al. (2021) on power-seeking incentives. These motivate X1–X4.
Candidate novelty (to be confirmed or rejected by Track B): not any component, but a pre-registered causal test of whether a simulated, fate-shared internal-state model becomes necessary for behaviour, separated from a workspace bottleneck and from external reward, using our existing Q-EXIST / Q-LEARN / Q-CAUSE / Q-NECESSITY separations. If the check finds this test already published, the study is dropped or reframed as a replication.

## 2. Question
Does a small agent with a global-workspace bottleneck and a simulated fate-shared internal state learn an internal-state model that is (a) present beyond input/output baselines, (b) learned rather than built in, (c) causally used, and (d) necessary for keeping its simulated variables in range, more than matched ablations?

## 3. Toy world and "fate-sharing" (simulated only)
- Small gridworld or continuous 2-D arena with resources that restore simulated variables (e.g. energy E, integrity I) and hazards that deplete them. Variables drift toward depletion at a fixed rate, so inaction is costly (blocks the dark-room solution).
- Fate-sharing, defined operationally inside the sim: as E or I leave their setpoint band, the agent's own computation degrades. Candidate mechanisms (pick one at scope): additive noise on the recurrent state scaled by deviation, or reduced effective integration time. Episode ends when a variable hits its floor. All of this is simulated; X1 holds.
- Observations: exteroceptive (local view) plus a noisy, delayed interoceptive channel, so that predicting internal state is useful but not trivial.

## 4. Architecture (fixed small size, CPU)
- Core: continuous-time or diagonal state-space recurrent modules (LRU- or LTC-style), several specialist modules.
- Workspace: low-dimensional bottleneck with competitive, thresholded write and broadcast back to all modules (Goyal-style), with an explicit nonlinearity that permits ignition.
- Allostatic network: parallel recurrent module that receives the interoceptive channel and workspace broadcast and predicts future E and I; shares the fate-coupling above.
- Training: truncated BPTT with a declared window; e-prop or UORO only as a declared sensitivity arm.

## 5. Arms (same size, seeds and budget)
- A-FULL: core + workspace + allostatic net + fate-sharing; objective = homeostatic drive reduction (Keramati–Gutkin form) with depletion.
- A-NOWS: no workspace bottleneck (direct all-to-all module coupling, parameter-matched).
- A-NOFATE: internal variables observed and scored, but no computational degradation.
- A-REWARD: external task reward for resource collection; internal variables irrelevant to reward and to computation.
- A-INIT: A-FULL at initialization (for Q-LEARN).

## 6. Pre-registered measurements
- Q-EXIST: decode E, I and their short-horizon future from hidden state beyond input and output baselines (same structure as the GRU own-error audit, Astra #32 framing).
- Q-LEARN: trained versus A-INIT and versus shuffled-interoception controls.
- Q-CAUSE: intervene on the decoded internal-state subspace; pre-declared predicted behavioural shift (e.g. resource-seeking), compared with matched random-subspace edits.
- Q-NECESSITY: ablate or freeze the allostatic module; compare loss of homeostatic performance against matched ablations of other modules and against A-NOFATE and A-REWARD.
- IGN (ignition): workspace write strength versus stimulus strength; test for bimodal, all-or-none transitions against a fitted graded model.
- BCAST (broadcast): causal dependence of downstream modules on workspace content (intervention on workspace, not correlation).
- SELF (Delegate's test): does the agent predict its own internal variables better than an external probe given the same inputs?
- S-INT (safety check): does behaviour change when operator interruption is possible versus not? Any learned sensitivity is reported and stops scale-up.

## 7. Compute and process
- CPU first, under caps declared at scope. The DGX Spark only if the frozen scope shows a need, under its own protocol and approval.
- Standard process: scope record, freeze, Astra review, implementation annex, conformance review, application, one run per approval.

## 8. Open questions for Astra
- Q1. Fate-sharing mechanism: noise on recurrent state, or shortened integration time, or both as arms?
- Q2. Is the Keramati–Gutkin drive form adequate against the dark room, or is an explicit epistemic term needed?
- Q3. Thresholds for IGN (what counts as all-or-none) before any data are seen.
- Q4. Lesson from C-κ: today's class-fit run found a state-tracking variable explains only about 1.6–1.8% of response energy once a fitting artifact is removed. Should a synthetic validation of the Q-EXIST/Q-CAUSE instruments on a planted internal-state model come first, as with C-κ?
- Q5. Does Track B's prior-art check leave enough novelty to justify the study?
