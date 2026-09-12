# Artificial organism research: from assigned goals to maintained organization

Research notebook v0.1 — 9 September 2026

Status: targeted literature review, proposed research mechanism, one executed exploratory pilot, and a proposed next experiment. This is not a claim to have created life, craving, sentience, or a new consciousness theory. The novel mechanism below remains unimplemented and its originality is unverified.

## The objective we are pursuing

Build a bounded neural system whose continuing activity sustains its own functional organization, and whose changing capabilities and individual history generate new priorities. The motivating question is whether this can develop into something reasonably described as an artificial organism, rather than an agent that merely describes the motivations of organisms.

This objective does not require unlimited intelligence, language, or reproduction. It does require moving beyond a chatbot personality, a list of emotion labels, or a survival score treated as sufficient evidence of life.

We will distinguish three questions throughout the project:

1. **Functional motivation:** Which mechanisms cause the system to initiate activity, prefer outcomes, and learn from consequences?
2. **Organismal autonomy:** Does its activity maintain or reconstruct the mechanisms on which that activity depends?
3. **Subjectivity:** Does any of this feel like anything?

Success on the first two does not settle the third. These distinctions let us investigate the user's philosophical goal without making every experiment depend on solving consciousness first. The theory-based indicator approach of Butlin and colleagues supplies a separate framework for consciousness assessment; it is not our success metric for artificial life. [Butlin et al., 2023](https://arxiv.org/abs/2308.08708)

## What the literature changes about the proposal

This was a targeted search of primary research and author-hosted material, not a systematic review or exhaustive novelty search. Search families included autopoiesis and adaptivity, organizational closure, neural homeostasis, metabolic neural computation, intrinsic motivation, and neural cellular automata. Publisher pages that did not load were not treated as if their full texts had been read.

| Prior work | Finding or proposal relevant here | Consequence for our project |
| --- | --- | --- |
| Di Paolo, *Autopoiesis, adaptivity, teleology, agency* | Proposes adaptivity as regulation in relation to viability, extending a self-production account | Self-maintenance and adaptive agency need separate tests; maintaining a variable alone is too weak |
| Montévil and Mossio, *Biological organisation as closure of constraints* | Develops an account of mutually dependent constraints that sustain biological organization | Look for causal maintenance dependencies between mechanisms, rather than merely circular data flow |
| Di Paolo and Iizuka, *How (not) to model autonomous behaviour* | Examines autonomy and homeostatic adaptation in artificial agents | Neural homeostasis and autonomous behavior are established research directions |
| Masumori et al., *Neural Autopoiesis* | Studies stimulus avoidance and regulation of neural input boundaries in biological and artificial networks | Calling a neural controller autopoietic is not a new contribution |
| Mordvintsev et al., *Growing Neural Cellular Automata* | Demonstrates learned local rules that grow and regenerate target patterns | Neural pattern regeneration is a useful substrate, but regeneration by itself is established |
| Pio-Lopez et al., *The scaling of goals from cellular to anatomical homeostasis* | Investigates how local metabolic homeostasis can scale to larger goals in an evolutionary NCA simulation | Even the proposed move from local needs to collective goals has close prior art |
| Zhang, Risi and Darlow, *Petri Dish Neural Cellular Automata* | Presents interacting NCA agents with continual parameter updates; its stated objective maximizes spatial aliveness | Lifelong neural adaptation and complex collective dynamics already exist in this area; the optimization objective remains explicit |
| Haber et al., *Learning to Play With Intrinsically-Motivated, Self-Aware Agents* | Uses world and self-models to organize curiosity-driven exploration | Self-generated exploration is not, by itself, an invention or evidence of felt curiosity |

Sources: [Di Paolo](https://sussex.figshare.com/articles/journal_contribution/Autopoiesis_adaptivity_teleology_agency/23368025); [Montévil and Mossio](https://montevil.org/publications/articles/2015-mm-organisation-closure-constraints/); [Di Paolo and Iizuka](https://ezequieldipaolo.net/wp-content/uploads/2011/10/dipaolo-iizuka-how.pdf); [Masumori et al.](https://arxiv.org/abs/2001.09641); [Growing NCA](https://distill.pub/2020/growing-ca/); [Pio-Lopez et al.](https://royalsocietypublishing.org/rsfs/article/13/3/20220072/89445/The-scaling-of-goals-from-cellular-to-anatomical); [PD-NCA](https://pub.sakana.ai/pdnca/); [Haber et al.](https://proceedings.neurips.cc/paper/2018/hash/71e63ef5b7249cfc60852f0e0f5bf4c8-Abstract.html).

Other relevant foundations are homeostatic reinforcement learning, which formalizes reward in relation to internal stability, and Integrated World Modeling Theory, which already connects embodiment, self-modeling and consciousness theories. These make it especially important not to claim that combining metabolism, memory and a world model is itself novel. [Keramati and Gutkin](https://elifesciences.org/articles/04811); [Safron](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2022.642397/full)

**Working conclusion:** organizational closure is the relevant research territory. The candidate contribution must be a particular mechanism and an intervention-based benchmark, not a new name for that territory.

## Proposed mechanism: capacities that generate their own maintenance demands

The strongest direction identified here is the co-development of capabilities and needs.

In a fixed homeostatic controller, the designer lists needs in advance. We propose an agent whose functional neural organization can change during its lifetime. Developing a capability changes what the agent must maintain. It can then learn to acquire a resource because that resource sustains a capability it has come to depend on.

For example, suppose an agent develops a persistent memory pathway that makes a distant resource patch usable. Maintaining that pathway consumes a precursor that was previously irrelevant. The agent begins acquiring the precursor, allocating maintenance to the pathway, and preserving the memory because those activities sustain its successful organization. If the distant patch disappears, or another route becomes adequate, it may abandon the pathway and its associated demand.

We would not program an instruction to want the precursor or preserve memory. We would specify transition rules, resource costs, sensory access and possible plastic changes, then test whether the dependency is discovered and regulated. The example is an experimental proposal, not an observed result.

### Candidate implementation

Start with a small lattice or sparse graph of local neural units. A unit has activity, available energy, structural precursor, and maintained conductance. The same distributed activity controls resource routing, environmental interaction, and local maintenance. Local plasticity changes useful pathways. There is no separate invulnerable planner that can do all the work when this tissue stops functioning.

An illustrative update family is:

\[
h_i(t+1)=g(e_i,c_i)\tanh\!\left(\sum_j c_{ij}w_{ij}h_j(t)+U_i o_i(t)\right)
\]

\[
e_i(t+1)=e_i(t)+J_i^{in}-J_i^{out}-C_i^{activity}-C_i^{maintenance}
\]

\[
c_{ij}(t+1)=\operatorname{clip}\left(c_{ij}(t)+R_{ij}(e,p,h)-D_{ij}(h),0,1\right)
\]

Here, energy and precursor flows are separately accounted for. Conductances affect which computations can happen; maintaining them requires resources and neural activity. The agent must remain open to environmental supplies, so organizational closure does not mean thermodynamic isolation. These equations are a design family, not a biological derivation or a finished model.

The key additional development is to let useful pathways and their maintenance requirements change through local learning. If all circuitry is fixed and the repair action merely restores a quality slider, the proposal remains close to ordinary regulation.

### Where motivation originates

The design does not make motivation appear from nothing. Laws of the simulator, inherited update rules, initial conditions, developmental experience and selection all constrain behavior. The initial research version may use explicit evolutionary selection for continued functioning. Local learning rules may themselves contain an implicit reinforcement signal. We must describe both honestly.

The proposed distinction is where particular goals are generated during a lifetime. A new maintenance priority should arise from an acquired causal dependency, rather than an instruction or a preassigned resource preference. Standard reinforcement learning may also accomplish this. A fair comparison must test that explanation rather than assume it away.

## E0: an exploratory pilot executed in this session

Before implementing developmental neural tissue, we tested a weaker resource-dependent recurrent controller. This is a plumbing and baseline experiment, not the main hypothesis above.

### Implemented system

- Six recurrent hidden units, 100 evolved parameters, five inputs and four actions.
- Inputs: energy, maintenance material, neural quality, and two currently observable resource yields.
- Actions: gather energy, gather material, repair, or rest.
- Neural activity consumes simulated energy and degrades a neural-quality variable. Quality modulates hidden-unit conductance. Repair consumes material and energy and restores quality.
- All quantities are dimensionless simulator variables. The quality gain changes evaluated neural dynamics, but no physical processors or real electrical supplies are repaired. Efficient NumPy evaluation does not condition hardware compute expenditure on simulated energy.
- Evolution uses an explicit objective: mean active ticks before energy or quality crosses a designer-set termination boundary. It does not use text data. There is no weight learning during a lifetime and no ongoing optimization during evaluation.

Training used six independent optimizer seeds, 60 generations, 64 candidate controllers per generation, and eight training episodes of 240 ticks per generation. Each seed also used a fixed 16-episode validation panel to select its controller. Evaluation used a separate random seed and 64 paired initial conditions per controller, each lasting at most 600 ticks. The evaluation panel was not used for model selection. No hyperparameters were changed after viewing these results.

Additional evaluation scenarios reduce energy yield by 35% from tick 200 or reduce neural quality to 55% of its current value at tick 200. Resource yields otherwise change every 30 ticks. The action space, dynamics and all constants are in `pilot.py`.

### Results

Means below are active ticks out of 600. Completion is for the normal condition. Neural variants contain 384 episodes each (six controllers by 64); the single reflex baseline has 64 episodes. Untrained results use six random controllers. Episodes from one controller are not independent training replications.

| Controller or intervention | Normal | Scarcity | Quality shock | Normal completion |
| --- | ---: | ---: | ---: | ---: |
| Evolved recurrent controller | 600.00 | 600.00 | 596.21 | 100% |
| Internal telemetry clamped | 66.26 | 66.26 | 66.26 | 0% |
| Hidden state reset each tick | 421.56 | 421.56 | 421.56 | 66.67% |
| Quality-to-neural-gain link disconnected | 600.00 | 600.00 | 597.07 | 100% |
| Sham repair: costs paid, quality not restored | 94.73 | 94.73 | 94.73 | 0% |
| Untrained recurrent controller | 69.63 | 69.63 | 69.63 | 0% |
| Handwritten reflex controller | 600.00 | 600.00 | 600.00 | 100% |

The large variability in hidden-state reset matters: four evolved controllers completed every episode, while two had much shorter lifetimes. Its normal-condition standard deviation across controller means was 278.24 ticks. Thus recurrence was useful to particular solutions, but was not necessary for solving this environment.

### What this establishes and what it does not

1. Evolution found effective maintenance policies. A tiny system can act without text imitation or prompts. This is unsurprising and provides no evidence of felt craving.
2. Accurate internal telemetry mattered to the evolved solutions. Clamping telemetry is an out-of-distribution intervention; it is not proof of self-awareness. Neural gain also still carries some quality information in this condition.
3. The proposed quality-to-neural-dynamics coupling did not improve normal-condition persistence relative to its disconnection. Both conditions hit the measurement ceiling. This does not establish equivalence in all environments, but it supplies no support for an advantage here.
4. The reflex controller solved the task. A simple rule system explains the performance standard. It uses a nominal neural-activity cost of 0.5 rather than matched computation, so it is a positive control, not a parameter-matched architecture comparison.
5. Sham repair caused failures, as expected from the programmed termination condition. This verifies the resource accounting; it is not independent evidence for life or organizational closure.
6. Identical numbers in several challenge columns arise because those agents failed before tick 200, or because the challenge did not change the capped outcome. They do not demonstrate robustness to a challenge the agent never reached.

**E0 decision:** keep this as a reproducible negative control. Do not interpret resource-dependent behavior or successful repair as the missing link. Move to a test where the system must discover and maintain a changing dependency.

The pilot has no growing topology, produced boundary, learned self-model, autobiographical memory, or within-life learning. It does not implement the proposed mechanism, satisfy a strict autopoiesis criterion, or test consciousness.

### Verification and reproducibility

Mechanism checks verified that quality changes neural dynamics, disconnection removes that particular effect with observations held fixed, repeated paired rollouts are deterministic, action totals equal active ticks, and repair versus sham repair uses the same energy while producing different quality changes.

Run `python pilot.py --out results` with NumPy installed. Configuration, dependency versions, source hash and recorded wall time are in `results/run.json`. `results/controllers.npz` stores all six selected controllers. `episodes.csv`, `training.csv`, `summary.json` and a prespecified seed-0/episode-0 trace preserve raw and aggregated outcomes. The script completed in approximately 48 seconds in this environment; that is not a hardware performance promise.

## E1: the next decisive experiment — acquiring a new maintenance goal

Status: proposed protocol, not implemented or externally preregistered. Freeze the implementation and evaluation rules before collecting E1 results. E0 informed this design, so E1 is a follow-up, not a preregistered extension of E0.

### Central question

Can a neural system learn a new resource-seeking priority when that resource begins sustaining an acquired capability, without a new reward label or manually added drive?

### Minimal environment

Use a 16 by 16 world with partial observations, two familiar resource types, a third initially irrelevant precursor, and a resource site that requires retaining a short sequence across an observation gap. Permit the neural system to develop and maintain recurrent pathways within a fixed maximum computational and material budget. The precursor is available through the same generic collection action as familiar resources; no new action is introduced at evaluation.

The memory pathway has a measurable maintenance dependence on that precursor. During initial development its role is unnecessary or can be satisfied by another supply. At a fixed evaluation change, that alternative is removed. The agent must experience the resulting functional consequences and adjust its behavior. The newly relevant precursor must have been perceptually accessible before the change, so this is a change in relevance rather than an impossible demand to recognize an unseen sensor.

The point is not to hide simulator physics from the experimenter. The point is to avoid feeding the agent a goal identifier, scalar bonus for collecting the precursor, or text telling it what happened.

### Candidate comparisons

| Variant | Purpose |
| --- | --- |
| Resource-maintained plastic neural graph | Candidate mechanism: maintenance and learning alter functional circuitry |
| Same graph with plasticity frozen | Determine whether acquired adaptation exceeds an inherited fixed response |
| Conventional recurrent agent with identical observations and action budget | Test whether ordinary state estimation and policy learning explain the result |
| Homeostatic RL baseline with matched environmental experience | Test against the established approach most likely to reproduce the behavior |
| Scripted adaptive controller with online dependency estimation | Challenge a claim that simple control logic cannot explain goal acquisition |

Specify the RL training signals explicitly and match information access. A richer training reward given to one variant is a changed objective, not a clean architectural comparison. Report parameter counts, evaluated operations and developmental transitions; do not claim all budgets match if they do not.

### Interventions that matter

1. **New dependency:** remove the alternative precursor supply, keeping visual identity and immediate external rewards unchanged.
2. **Causal rescue:** externally maintain the memory pathway while keeping the precursor scarce. Its maintenance demand should diminish after the agent has evidence that collection is unnecessary. Analyze sustained adaptation, not just the first reaction.
3. **Sham precursor:** supply a perceptually matching resource that does not repair the pathway. A learned dependence should eventually discriminate actual restoration from a misleading cue.
4. **Loss of usefulness:** make the distant site irrelevant. Test whether the agent stops paying for an unnecessary memory pathway rather than preserving every structure indiscriminately.
5. **Pathway intervention:** disable the suspected recurrent route and verify loss of the relevant capability; restore it and verify recovery. This ties maintenance behavior to an identified mechanism rather than a correlated latent feature.

### Measurements and decision rule

Primary behavioral outcome: change in precursor-directed collection after the new dependency, compared with both pre-change behavior and causal rescue. Count decisions only while the agent is active and within a feasible collection range, and also report unconditional completion and persistence so selective survival cannot manufacture a preference effect.

Primary functional outcome: recovery of the memory-dependent task after an equal amount of post-change experience. Record circuit activity, precursor use and conductance changes to check temporal order. Task completion is measured by the experimenter; whether it is supplied as a training objective is a separate recorded design choice.

Use at least 20 independent developmental seeds per learned variant, a common set of held-out worlds, and confidence intervals based on seed-level paired contrasts. Choose the trial budget after an engineering feasibility run and freeze it before the confirmatory run. Do not use individual timesteps as statistical replications. Include parameter and environment sensitivity checks only for a specific remaining explanation.

A positive outcome requires reproducible behavioral adaptation, verified restoration of the relevant function, and appropriate relaxation of the priority under rescue or loss of usefulness. It must also survive comparisons to conventional learners. If all models do this equally well, the benchmark demonstrates adaptive goal acquisition, not an advantage of maintained neural tissue. If the system only follows a fixed deficit threshold, the developmental claim fails. If it repairs function but gains nothing over ordinary control, structural repair may remain an engineering contribution while the stronger motivation claim is unsupported.

These results would still not establish subjective wanting. They would provide an operational example of a goal becoming relevant through the agent's acquired organization.

## Longer pathway, with explicit gates

| Stage | Deliverable | Gate before moving on |
| --- | --- | --- |
| E0, completed | Resource-dependent control with interventions | Establish plumbing and expose simple explanations |
| E1, proposed | Acquired maintenance priority for a learned capability | Verify new dependence, recovery, and causal rescue |
| E2 | Distributed construction and repair of functional pathways | Maintenance must reconstruct useful computation from local information, not restore a global template |
| E3 | Persistent individual development with changing dependencies | Histories produce repeatable differences that transfer and are mediated by measured internal changes |
| E4 | Theory-specific consciousness assessment if warranted | Choose independent indicators and explicit rival interpretations; verbal reports cannot decide it |

Physical embodiment is a later experimental choice, not a magic ingredient. A simulated maintenance dependency can causally change the computation of a program, yet it does not follow that simulated metabolism instantiates biological life or subjectivity. Conversely, using actual hardware energy would not by itself resolve that question. Any claimed benefit of a physical implementation needs a specified mechanism that the digital version omitted.

The immediate work product is an experiment program for constitutive motivation: maintaining the organization that produces action, and learning what newly acquired organization requires. The current evidence favors taking that question seriously while rejecting the first, much weaker demonstration as sufficient.

## Working decisions retained for continuation

- User objective: a philosophically living, bounded artificial individual, not unlimited AI or convincing emotional dialogue.
- Language is deferred; early agents learn through their own interactions.
- No claim that an absence of text training establishes intrinsic motivation or consciousness.
- No claim that evolutionary optimization removes externally chosen objectives.
- Artificial termination is a simulator boundary; it is not used as evidence of experienced death.
- The candidate contribution is co-development of capabilities and maintenance demands, tested through causal rescue and lost-usefulness interventions.
- The next implementation target is E1. No experiment beyond E0 has been run, and no background research job has been scheduled.
