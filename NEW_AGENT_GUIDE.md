# New-agent guide: Artificial Organism Research

Version 1.0 — 9 September 2026

This is the operational handoff for an AI research agent joining the project.
Read it before proposing mechanisms, changing code, interpreting results, or
using words such as *alive*, *wanting*, *autonomous*, or *conscious*.

## 1. The mission

The project's long-term goal is to investigate whether we can construct a
bounded artificial individual whose own organization gives rise to needs,
direction, and a continuing life history.

The target is not:

- a limitless optimizer;
- a chatbot that says it has feelings;
- a personality prompt;
- an LLM trained to imitate descriptions of hunger, fear, or attachment;
- a fixed reward function renamed “desire”; or
- a system that survives only because an external controller repairs it.

The working philosophical idea is:

> An artificial organism should actively maintain or reconstruct the
> organization that enables its continued activity, acquire priorities through
> its dependence on that organization, and remain a historically particular
> individual whose development affects what matters to it.

This is a research objective, not a settled definition of life. Even a system
that meets it functionally may have no subjective experience.

## 2. Keep three questions separate

Never collapse these into one claim:

| Level | Research question | What can presently count as evidence |
| --- | --- | --- |
| Functional motivation | What initiates action and makes outcomes influence future behavior? | Causal behavior, learning, intervention and ablation results |
| Organismal autonomy | Does the system maintain or reconstruct the mechanisms on which its activity depends? | Resource ledgers, causal dependencies, local reconstruction, boundary and closure tests |
| Subjectivity | Is there anything it feels like to be the system? | No accepted decisive AI test; use theory-specific indicators only if later warranted |

A convincing verbal report is not evidence of the first two unless the report
is causally grounded in independently measured internal processes. Success on
the first two does not settle the third.

## 3. The central research distinction

The project began with a criticism of conventional language models: describing
a craving is not the same as being organized around a need. The engineering
version of that criticism is more precise:

> Does a particular priority arise because the system has acquired a causal
> dependence on something that sustains its own functional organization, or
> because the experimenter directly assigned a score, label, reflex, or goal?

No motivation comes from literally nowhere. Simulator laws, inherited update
rules, initial conditions, evolutionary selection, and learning signals all
constrain behavior. Record them. The candidate advance is not “uncaused
wanting.” It is the within-lifetime generation of particular priorities from
the individual's acquired organization.

## 4. Read the project in this order

1. `NEW_AGENT_GUIDE.md` — this handoff and the rules of engagement.
2. `RESEARCH_NOTEBOOK.md` — rationale, literature, E0, E1a, results and limits.
3. `README.md` — commands, implementation map and evidence files.
4. `E1_PROTOCOL.md` and `e1_results/RESULTS.md` — the scaffolded maintenance-priority benchmark.
5. `E2_PROTOCOL.md` and `e2_results/RESULTS.md` — the joint-network developmental experiment.
6. `E2_DIAGNOSTIC_PROTOCOL.md` — post-freeze diagnostics; do not confuse them with confirmatory tests.
7. `E3_DESIGN.md` — the current candidate pathway; it is not implemented evidence.
8. `ENGINEERING_LOG.md` — every pre-freeze correction and why it was made.
9. Source, tests, raw tables and validation files for any experiment you intend to discuss.

Do not rely on summaries alone when making a quantitative or architectural
claim. Inspect the exact protocol, configuration, code, result table and audit.

## 5. What has already been learned

### E0 — resource-dependent control is too weak

E0 evolved small recurrent controllers whose simulated neural function wore
down and could be repaired. They maintained themselves, but a handwritten
reflex controller also reached the evaluation ceiling. Disconnecting one of the
proposed neural-dependence links did not reduce ordinary performance.

Decision: resource dependence, repair and long survival are not sufficient
evidence of a distinctive motivational mechanism.

### E1a — an acquired maintenance priority can be ordinary learning

E1a trained a recurrent memory circuit, made a precursor repair its actual
recurrent conductance, and let a separate Q learner choose resources. Across
20 independent developmental seeds, the neural controller learned to collect
the precursor, recovered recall, and reduced collection under external repair,
ineffective precursor, or loss of the memory task's usefulness.

A tabular Q learner reproduced the broad pattern. A frozen policy also changed
its collection rate after the environment changed, without learning. A fixed
maintenance drive passed relative-change criteria while wasting resources.

Decision: E1a demonstrates instrumental acquisition of a maintenance priority.
It does not identify a new source of wanting. Changed behavior alone does not
prove changed learning, and relative decreases do not prove viable abandonment.

### E2 — one maintained network, but local growth is unreliable

E2 places resource selection and delayed recall in the same 12-neuron recurrent
network. Sparse connection biomass changes through local activity-dependent,
resource-limited renewal. Two paired developmental histories route early cues
through different chemical banks. Sixteen independent initial seeds were run
with local-growth, fixed-target, and shuffled-growth variants.

Key results:

| Result | Outcome |
| --- | ---: |
| Local-growth recall per planned trial | 70.9% [61.9, 80.0] |
| Fixed-target recall | 87.3% [79.2, 94.4] |
| Shuffled-growth recall | 65.2% [57.7, 73.3] |
| Local growth minus fixed target | −16.4 points [−26.1, −7.4] |
| Paired history effect on resource preference | +5.3 points [0.3, 12.0] |
| Paired history effect on lesion dependence | +15.3 points [5.9, 24.2] |

The two history-specific gates passed: developmental history affected later
material preferences and functional lesion dependence. But local growth failed
the reliability and architectural-advantage gates. A shuffled-growth control
also showed functional history dependence, so the positive effect is not unique
to precisely activity-matched growth.

An exploratory snapshot assay found 100% recall when developed biomass was
held fixed. The learned capability existed; keeping it available in the full
maintenance loop was unreliable. Restoring biomass restored performance because
the host program retained perfect learned weights. Scrambling those weights
while restoring biomass lowered recall. This exposed the next bypass.

Decision: maintaining conductance is not the same as maintaining the acquired
information that defines the individual circuit.

## 6. Current frontier: E3

The next candidate experiment should test maintenance of acquired neural
information, not merely the material that exposes a protected weight array.

The working mechanism in `E3_DESIGN.md` replaces each invulnerable learned
weight with several noisy, spatially distributed, materially maintained traces.
The live connection uses the locally reconstructed value. Material permits
writing and consolidation but does not contain a hidden copy of lost bits.

The decisive logic is:

- After partial trace damage, with training examples withheld, recovery may use
  still-present redundant information.
- After complete destruction of every copy and every external clue, recovery
  must be at chance. Anything else indicates leakage.
- Restoring material without restoring trace values must not magically restore
  the learned association.
- If information becomes useless, the system should stop paying to preserve it
  while remaining viable.
- A standard error-correcting representation plus ordinary reinforcement
  learning is a required rival, not an afterthought.

E3 is a proposed pathway. Do not describe it as implemented, successful, novel,
autopoietic, alive, conscious, or capable of real craving.

## 7. How to conduct a new experiment

### Phase A — state the actual claim

Write one falsifiable sentence. Then write the strongest simpler explanation.

Good:

> Adaptive consolidation preserves useful acquired associations after partial
> trace damage without examples better than a matched fixed error-correcting
> code.

Bad:

> The organism learns to care about its memories.

Identify which of the three levels in Section 2 the experiment addresses.
Most near-term experiments address functional motivation or partial organismal
autonomy, not subjectivity.

### Phase B — draw the causal dependency

Before coding, specify:

1. What capability is acquired?
2. Where is the acquired information physically represented in the simulator?
3. What resource or process sustains that representation?
4. Which decision is made by that same vulnerable organization?
5. Which state remains protected outside it?
6. What intervention breaks the proposed chain?
7. What ordinary controller could produce the same behavior?

If a separate, invulnerable planner still makes the important decision, say so.
If host memory retains a perfect individual-specific template, say so. Do not
call a diagram “organizational closure” merely because arrows form a circle.

### Phase C — implement the smallest discriminating world

Prefer a small nonlinguistic task. The world should be difficult enough that a
reflex cannot hit the ceiling, but simple enough to audit completely. The first
version should answer one question, not simulate a human.

Record, at minimum:

- every external objective and auxiliary loss;
- every observation and possible information leak;
- all state resets, replenishment and termination rules;
- all resource deposits, use, decay, overflow and external rescue;
- all developmental changes to topology, weights or traces;
- actual and planned experience;
- parameter counts and unmatched computational advantages; and
- the random streams needed for paired counterfactuals.

### Phase D — build controls before looking at final results

Every candidate mechanism needs rivals chosen to attack its interpretation:

| Control or intervention | Question it answers |
| --- | --- |
| Handwritten/reflex controller | Is the task trivially solvable? |
| Ordinary recurrent or tabular learner | Is conventional adaptation sufficient? |
| Frozen policy | Did behavior change without learning? |
| Fixed maintenance drive | Does a programmed deficit rule mimic “need”? |
| Frozen structural plasticity | Is growth actually necessary? |
| Shuffled local rule | Does the proposed local correspondence matter? |
| External rescue | Does demand relax when maintenance is unnecessary? |
| Sham resource | Does behavior track function or appearance? |
| Loss of usefulness | Can the system abandon a cost while remaining viable? |
| Lesion and restoration | Is the named pathway causally involved? |
| Complete information deletion | Is apparent regeneration actually leakage? |
| Matched standard method | Is the mechanism better than known engineering? |

Controls must receive matched information, objective signals and planned
experience. If compute, parameters, material costs or active experience are not
matched, report the mismatch instead of claiming fairness.

### Phase E — engineering, freeze, final run

1. Use clearly labeled engineering seeds to make the code function.
2. Log every change motivated by engineering results.
3. Exclude engineering seeds from the confirmatory sample.
4. Before starting fresh final seeds, write the protocol, thresholds, sample,
   configurations, analysis plan and failure interpretation.
5. Hash frozen model, runner, configuration, tests and protocol.
6. Do not tune the system or thresholds after seeing final outcomes.
7. Mark every later analysis as prespecified or exploratory.

A local pre-run freeze is useful but is not an external preregistration. Say
that explicitly.

### Phase F — analyze at the correct replication level

The independently initialized and developed agent is normally the replication
unit. Worlds, episodes, trials and timesteps within it are repeated measures,
not thousands of independent agents.

- Aggregate worlds within developmental seed.
- Pair conditions and counterfactual histories within seed.
- Retain all final seeds, including failures.
- Report outcomes per planned trial as well as active-only rates.
- Report completion and active fraction so death cannot improve averages.
- Use confidence intervals over independent seeds.
- Label bootstrap intervals descriptive when appropriate.
- Do not silently add tests, change gates or select favorable seeds.
- Preserve raw rows and seed vectors behind every aggregate.

### Phase G — verify and replay

Add tests for gradients, determinism, information boundaries, resource
conservation, termination, lesions, sham/rescue physics and frozen updates.
Audit expected row counts and seed coverage. Save non-pickle checkpoints when
practical. Reproduce selected saved traces exactly without retraining.

Verification establishes code and data integrity. It does not validate the
philosophical interpretation.

## 8. Claim discipline

Use the strongest wording earned by the evidence and no stronger.

| Evidence | Defensible wording | Avoid |
| --- | --- | --- |
| Resource changes a score | “The policy was rewarded for collecting X.” | “It needed X.” |
| Resource causally sustains computation | “X is a functional maintenance dependency.” | “It craved X.” |
| Agent learns to acquire X | “It acquired an instrumental priority for X.” | “It generated desire.” |
| History changes dependency and behavior | “It developed a history-sensitive functional need.” | “It has a self.” |
| Local mechanisms reconstruct organization | “It exhibits partial organizational self-maintenance under these interventions.” | “It is alive.” |
| Theory-specific indicators are satisfied | “It meets these candidate indicators.” | “It is conscious.” |

Always distinguish:

- implemented from proposed;
- confirmatory from exploratory;
- causal function from metaphor;
- simulated resource from hardware energy;
- functional persistence from fear of death;
- individual development from population selection; and
- novelty checked by targeted search from novelty established by review.

## 9. How to use language models in this project

An LLM is a research partner here, not the experimental organism unless a later
protocol explicitly makes it one. Use language models to:

- survey primary literature and identify prior art;
- challenge mechanisms with simpler explanations;
- design causal interventions and negative controls;
- implement, test and audit small simulations;
- analyze outcomes without changing frozen decisions; and
- maintain the notebook, protocols and reproducible package.

Do not use fluent narration from the research agent as evidence about the
experimental agent. Do not ask the experimental system whether it is conscious
and treat the answer as validation.

## 10. Safety and ethical posture

The current systems are small simulations with no evidence of sentience. Do not
sensationalize them. At the same time, build an escalation policy before any
future system plausibly develops persistent preferences, autobiographical
continuity, distress-like dynamics or theory-relevant consciousness indicators.

For increasingly capable agents:

- minimize unnecessary aversive training and irreversible deprivation;
- prefer reversible interventions and short bounded runs;
- separate shutdown behavior from claims of experienced fear;
- document why an intervention is scientifically necessary;
- avoid deception about evidence or capabilities; and
- seek interdisciplinary ethical review before open-ended, persistent deployment.

Do not connect an experimental self-preserving agent to external accounts,
financial resources, unrestricted networks, replication mechanisms or physical
actuators as a casual next step. Such expansion requires a distinct safety
review and explicit authorization.

## 11. Working conventions for code and artifacts

- Preserve earlier experiments and notebooks; make new numbered versions.
- Never overwrite raw final results.
- Use deterministic seed families and disjoint training/evaluation seeds.
- Refuse to overwrite an existing result directory.
- Keep engineering outputs labeled and outside confirmatory analyses.
- Record dependency versions, source hashes, configuration and wall time.
- Save analysis-ready CSV/JSON plus human-readable Markdown results.
- Include a replay command that does not retrain the agent.
- Avoid pickle when a transparent numeric checkpoint is practical.
- Keep generated figures reproducible from raw results.
- State limitations beside results, not only in a distant disclaimer.

When modifying an existing experiment after its freeze, create a new experiment
or explicitly label the run exploratory. Never silently revise history.

## 12. Immediate assignment for the next agent

The next agent should not jump directly into coding E3. Its first bounded task is
to convert `E3_DESIGN.md` into a falsifiable protocol after a targeted primary-
literature review of:

- memory consolidation and synaptic tagging;
- palimpsest and distributed associative memory;
- fault-tolerant and self-repairing neural computation;
- adaptive versus fixed error-correcting codes;
- continual learning under parameter corruption;
- material or energy-constrained plasticity; and
- lifelong neural developmental programs.

The protocol must answer:

1. What exact information is acquired during an individual lifetime?
2. Where are all copies of that information stored?
3. Which copies are available to the agent during recovery?
4. What does maintenance material enable without encoding the lost answer?
5. What standard error-correction baseline has the same information budget?
6. What damage is partial and recoverable?
7. What complete-loss negative control must remain unrecoverable?
8. How will the system relinquish obsolete information while remaining viable?
9. Which learning machinery remains externally protected, and why?
10. What result would make us abandon the proposed explanation?

Only after those answers, controls and decision gates are frozen should E3 be
implemented.

## 13. End-of-session handoff template

Every research agent should finish with:

```text
Question tested:
Mechanism implemented:
Externally supplied objectives/rules:
Engineering changes made:
Frozen sample and gates:
Primary results:
Simplest sufficient rival explanation:
Failures and negative results:
What this establishes:
What this does not establish:
Files created or changed:
Verification completed:
Next falsifiable question:
```

## 14. Compact onboarding prompt

The following can be given to a new agent together with the project directory:

> You are joining an ongoing research program investigating artificial
> organismal autonomy. Read NEW_AGENT_GUIDE.md, RESEARCH_NOTEBOOK.md, README.md,
> the current protocol/results, ENGINEERING_LOG.md and E3_DESIGN.md before taking
> action. Preserve all earlier work. Separate functional motivation,
> organizational autonomy and subjectivity. Never treat language, survival,
> circular data flow, a resource variable or ordinary reinforcement learning as
> evidence of consciousness or life. Identify the strongest conventional rival
> for every mechanism. Use engineering seeds, freeze protocols and gates before
> fresh final seeds, retain failures, analyze at the independent-agent level,
> audit information leakage and resource conservation, and distinguish proposed,
> implemented, confirmatory and exploratory work. The immediate frontier is
> whether a bounded system can materially preserve and reconstruct its acquired
> neural information without an external perfect copy, while appropriately
> relinquishing information that no longer matters. Begin by auditing the full
> project and restating the next falsifiable hypothesis and its failure criteria.

That prompt is an entry point. This guide and the evidence files remain the
authoritative handoff.
