# Research understanding: Toward an Artificial Organism

Consolidated on 14 September 2026 against repository commit `a52e825`.
This is an onboarding synthesis of the available project record, not a new
experiment, revised protocol, external literature review, or claim of breakthrough.
Historical protocols, results, freezes and corrections retain their authority.

## 1. The intended breakthrough

The goal is to construct a bounded artificial individual whose activity
maintains the organization that makes that activity possible, and whose
development creates particular dependencies and priorities during its lifetime.

The proposed causal chain is:

**Individual experience → acquired functional organization → dependence on
maintaining that organization → learned allocation and resource acquisition →
continued functioning and further development.**

For example, acquiring a memory capability could make a previously irrelevant
precursor necessary. The individual would discover that dependence, obtain the
precursor, and maintain the relevant circuit. If the capability ceased to matter,
it could relinquish its maintenance while continuing to function.

The difficult part is closing this chain through the individual's own vulnerable
organization, including the machinery that makes maintenance decisions. A
protected controller maintaining a damaged memory bank establishes less.

The project explicitly separates:

| Question | What would support it |
| --- | --- |
| Functional motivation | Acquired priorities, learning and causal behavioral interventions |
| Organismal autonomy | Activity maintaining or reconstructing the organization on which it depends |
| Subjectivity | A separate, unresolved question; functional success does not establish experience |

Language, unlimited intelligence, reproduction and physical embodiment are not
prerequisites for the early experiments. The original ambition includes a
historically particular individual, but fluent self-description, long survival
and a designer-assigned survival objective are insufficient evidence.

Sources: [guide](NEW_AGENT_GUIDE.md), [notebook](RESEARCH_NOTEBOOK.md),
[original E3 design](E3_DESIGN.md).

## 2. Philosophy and scientific commitments

The central distinction is between an experimenter assigning a particular
priority and an individual acquiring that priority through a real functional
dependency. This does not require motivation to arise without causes: physics,
initial conditions, inherited rules, teaching and selection remain supplied.
Every such contribution must be disclosed.

The recorded literature work places the project near autopoiesis, enactivism,
adaptivity and closure of constraints: mechanisms sustaining one another, not
just arrows making a circle. Neural self-organization and memory consolidation
provide candidate mechanisms. Free-energy and active-inference ideas later
motivated an allocation proposal, but the implemented bonus was a heuristic,
not a formal active-inference system. None of these labels establishes novelty.

The literature reviews also sharpened the conventional alternatives: ordinary
reinforcement learning, error-correcting codes, memory scrubbing, selective
consolidation and fixed maintenance schedules. The project must face competent
versions of these methods. A conventional solution is an informative finding.

Research standards that recur throughout the work:

- State a falsifiable claim and its strongest simpler explanation first.
- Keep engineering, prospectively frozen final comparisons, and later
  exploratory diagnosis separate. Local freezes are not external preregistration.
- Retain unsuccessful individuals and report planned denominators, survival
  and missing responses; dying cannot improve the apparent success rate.
- Treat independently developed seeds as replication units, keeping paired
  histories and conditions together.
- Account for all acquired information, including weights, optimizer state,
  replay, metadata, scratch space, random streams and resource distributions.
- Distinguish passive decoding, reconstruction of redundancy and relearning.
  In a binary task, answer plus correctness feedback reveals the target even
  when explicit examples are withheld.
- Complete erasure must eliminate every target-dependent channel. Restoring
  material must not recreate arbitrary information from nothing.
- Preserve historical failures and corrections rather than rewriting freezes
  or weakening rivals until a desired result appears.

Sources: [guide](NEW_AGENT_GUIDE.md),
[E3 literature review](E3_LITERATURE_REVIEW_v0_1.md),
[research handoff](E3_RESEARCH_HANDOFF_v0_1.md).

## 3. Experimental history and what each step taught

### E0: resource-dependent control

Six evolved recurrent controllers operated a small world with energy,
maintenance material, neural quality and repair. Normal survival reached the
600-tick ceiling. A handwritten reflex also reached that ceiling, including
the challenge conditions. Disconnecting quality from neural gain did not
reduce normal survival.

**Lesson:** resource accounting and successful repair do not distinguish the
proposed organismal mechanism. The world was too easy for that inference.
The pilot remains a useful negative control, not a demonstration of wanting.

Evidence: [pilot](pilot.py), [saved results](results/summary.json),
[notebook](RESEARCH_NOTEBOOK.md).

### E1a: acquiring an instrumental maintenance priority

A trained 16-unit recurrent circuit remembered two bits. Precursor restored its
actual recurrent conductance. A separate Q learner chose resources using an
explicit net-energy objective, with no direct precursor bonus for the primary
learner. Twenty developmental seeds produced 4,480 evaluation episodes.

For the neural Q controller:

| Condition | Precursor choices | Correct recall / planned trials |
| --- | ---: | ---: |
| Before supply withdrawal | 0.0% | 100.0% |
| Immediately after withdrawal | 6.7% | 45.4% |
| After adaptation | 26.7% | 99.8% |
| External repair after further learning | 0.0% | 100.0% |
| Memory no longer supplies food | 3.8% | 31.9% |

Precursor percentages use active opportunities. The last condition has 90%
episode completion; reduced recall is not itself failure when memory is useless.

Ordinary tabular Q learning reproduced the broad acquisition and relinquishment
pattern. A frozen neural policy changed behavior without learning when its
observations changed. An assigned maintenance-drive controller passed the
relative-change gates but still wasted precursor when memory became useless,
completing only 17.5% of those episodes.

**Lesson:** an acquired instrumental maintenance priority is real and measurable,
but ordinary learning explains it. Changed behavior does not necessarily mean
learning, and reduced maintenance does not necessarily mean viable abandonment.
The separate controller and protected learned weights remained major scaffolds.

Engineering records preserve correction of an unstable tabular learning rate
before the final freeze; the baseline was improved rather than left weak.

Evidence: [protocol](E1_PROTOCOL.md), [results](e1_results/RESULTS.md),
[engineering log](ENGINEERING_LOG.md), [controller source](e1/control.py).

### E2: memory and resource choices in one maintained network

E2 used one 12-neuron recurrent network for delayed binary recall and resource
selection. Sparse edge biomass underwent local resource-limited renewal. Early
cue routing through two chemical banks created paired developmental histories.
Sixteen initial seeds, two histories and three structural variants produced
9,216 evaluation episodes.

| Finding | Result |
| --- | ---: |
| Activity-guided growth recall / planned | 70.9% |
| Fixed-target structure recall / planned | 87.3% |
| Shuffled-growth recall / planned | 65.2% |
| Growth minus fixed target | −16.4 points; 95% interval [−26.1, −7.4] |
| History effect on resource preference | +5.3 points [0.3, 12.0] |
| History effect on lesion dependence | +15.3 points [5.9, 24.2] |

History-specific priority, history-specific dependence and viable relinquishment
passed their gates. Functional reliability, selective value of growth and
chemistry-swap recovery failed. Shuffled growth also produced history-dependent
function, limiting claims for the precise activity-matching rule.

Exploratory snapshots achieved 100% recall when developed biomass was fixed.
The capability had been learned, but the maintenance loop did not reliably
keep it available. Crucially, biomass restoration could expose intact host-held
weights again. Those weights, the target network, replay and optimizer state
were not themselves reconstructed by the organism.

**Lesson:** developmental history can affect later dependencies and behavior,
but maintaining conductance is not maintaining the acquired information that
defines the circuit. E2's original aim remains incompletely realized.

Engineering revisions corrected exploration, viability economics, oversized
material stores and nearly saturated growth. Final settings were retained even
though fixed structure often won.

Evidence: [protocol](E2_PROTOCOL.md), [results](e2_results/RESULTS.md),
[diagnostic protocol](E2_DIAGNOSTIC_PROTOCOL.md),
[network source](e2/model.py), [notebook update](RESEARCH_NOTEBOOK.md).

## 4. Main E3: acquired-information maintenance and its stopping decision

E3 moves the target from material exposing protected weights to finite,
damageable acquired information. The intended recovery uses surviving internal
redundancy, with no external perfect copy or answer feedback.

The work divided into **E3a**, a conventional finite-memory maintenance benchmark,
and deferred **E3b**, the more ambitious coupled neural substrate. E3a's hypotheses
concern paid maintenance improving later recall (H1) and reducing spending on
obsolete information while preserving useful function (H2).

The substantial specification sequence covers:

| Contract | Contribution |
| --- | --- |
| v0.1 protocol | Claims, representations, controls, erasure and recovery logic |
| v0.2 state | Exact finite state, observations and delayed queries |
| v0.3 operations | Paid reads/writes, services, admission and scratch lifetime |
| v0.4 physics | Faults, aging, conditioning, resource routes and support |
| v0.5 policy | Explicit objective, finite learner and conventional rivals |
| v0.6 control | Executable instruction paths and payment bounds |
| v0.8 evaluation | Selected branch roster, reset logic and replay requirements |
| v0.9 interface | Worker boundaries, provenance and compact archive schema |
| v0.10 conformance | Privileged diagnostics and bounded scripted controls |
| v0.11 integration | Combined design and explicit final-experiment NO-GO |

The implementation is substantial but partial. `e3/` includes a 276-byte state
representation, repetition/block coding, arithmetic, metering, physical rules,
policy references, instruction execution, optimized fragments, transport/input
codecs, archives and paid service components. Teaching now includes LESSON and
COMMIT foundations, superseding older inventories that list all acquisition
services as absent. These are not a complete linked worker, isolated process,
phase runner or demonstrated full-runtime conformance implementation.

Two mathematical findings limited the scientific case before a full run:

1. Under the reviewed clean-parent repetition assumptions, competent periodic
   repair leaves at most about **1.64 percentage points** of expected adaptive
   advantage, below the proposed five-point adaptive gate. This conditional
   bound is not a theorem about every developed parent or finite sample.
2. Fixed/frozen repetition can afford conditioning plus maximal correction for
   **28 + 5 = 33 material units per source, below the supplied 36**. This refutes
   the universal claim that this budget financially forces sacrifice of obsolete
   code. It does not establish perfect recall or universal survival.

The main v0.11 final experiment is therefore **NO-GO**. Numerical H2 criteria
could conceivably pass without restoring its refuted stronger interpretation.
More documentation, faster execution or successful scripts cannot settle that
logical mismatch. Narrow component engineering remains useful when justified;
no full main-E3 empirical H1/H2 result is present.

Sources: [integration decision](E3_INTEGRATION_DECISION_v0_11.md),
[readiness review](.copilot-tracking/reviews/2026-09-10/e3-engineering-readiness.md),
[state implementation](e3/state.py), [teaching implementation](e3/teaching.py).

## 5. The September 14 allocation and obsolescence side branch

This standalone binary-trace toy shares neither the main E3 state layout nor
its complete resource tariffs and runtime. Its results cannot be promoted into
evidence that the main E3 machinery works. Its decision machinery and statistics
remain protected scaffolding.

### Early proposal and corrections

The revised proposal compared a recency allocator with one adding a staleness
bonus, motivated by uncertainty and anticipated relevance. Early runs exposed
an inverted bonus, unstable seed construction, shared random streams that broke
policy pairing, and biased ties in even-width repetition codes.

Later audits withdrew claims that the mechanism was statistically refuted or
that the substrate was structurally defective. Overlapping intervals do not
establish equivalence. Majority repair correctly restores redundancy below its
error threshold and reinforces the wrong majority above it; changing to continuous
traces does not automatically solve that information problem.

A truth-informed scheduler was also an invalid maintenance ceiling: its choice
of when to repair leaked the answer. The default world rarely constrained the
budget, while the stress world defeated even ample truth-blind repair. Neither
was initially a good discriminator of allocation.

### Allocation v1 and v2

Allocation v1 stopped at its controls-only feasibility stage: none of 27
configurations passed the declared headroom criterion. No final comparison or
freeze followed for that version. Exploratory searches then identified ordinary
damage-depth triage as a strong candidate.

Allocation v2 froze a new test and ran 32 fresh seeds, 200–231, in two selected
configurations. **Depth-first repair beat recency by +33.39 and +34.33 percentage
points**, with 97.5% intervals [30.77, 36.51] and [31.36, 37.26]. Every seed favored
depth-first in both configurations. Recall was 98.6% and 89.1% versus recency's
65.2% and 54.8%.

Depth means observable disagreement among stored copies, not access to the
correct answer. The result is a strong conventional baseline: repair memories
nearest loss of their current majority first. It does not show autonomous needs.

Exploratory follow-up explained why exact future queries hurt the particular
loss-model scheduler: it ignored later repairs and diverted effort from deeply
damaged memories toward imminent queries. Extending its horizon did not help.
Accurate corruption-rate learning was causally used, yet the true rate was not
the best input to that flawed allocation rule. More accurate information alone
does not make a decision rule better.

### OB1: learned abandonment fails

OB1 introduced permanent obsolescence alongside short and long dormancy.
Thirty-two seeds, 300–331, tested a learned silence threshold.

Relative to depth-first, learned allocation lowered recall by **11.53 and 10.03
points** and cut obsolete-repair share by only about 6.5 and 5.1 points, below
the required ten-point reduction. Overall: **not supported in this world**.

The learned statistic accurately described its observed completed gaps but
answered the wrong question. Frequent short gaps dominated, long unfinished
gaps were censored, and returning dormant memories were abandoned prematurely.
Soft deprioritization also let repairs spill back into deprioritized cues.
A conservative 2,000-tick timeout performed better; supplied obsolescence flags
showed that useful relinquishment was possible with privileged information.

### OB2: better formulation, still no learned advantage

OB2 used a survival estimator incorporating ongoing censored silences, estimated
return within 500 ticks, and hard repair eligibility. Engineering selection
retained the 2,000-tick timeout. Final seeds were 400–431.

| Primary check | Budget 3 | Budget 4 |
| --- | ---: | ---: |
| Learned minus timeout recall | −3.16 points | −0.72 points |
| Obsolete-repair share versus depth-first | −16.12 points | about −16.0 points |
| Long-silence calibration error | 0.120 | 0.120 |

The calibration gate required at most 0.10. The learned rule did not demonstrate
a recall advantage over the timeout. Both configurations were **not supported**.
Even a well-calibrated supplied predictor, used through the same probability
cutoff, did not demonstrate an improvement over the timeout. Learning also
retained approximately 25 times the state of the simple rule.

OB2 substantially reduced OB1's mistaken abandonment, but cross-experiment
improvement is not a new paired confirmatory contrast. The frozen OB1 verdict
stands. The branch's final conclusion is to preserve this as completed diagnostic
and baseline work. Better estimation of this same statistic through this rule
has not earned another claim of progress toward autonomy. Silence leaves long
dormancy and permanent obsolescence partly ambiguous.

Sources: [corrected branch record](E3_BRANCH_RECORD_2026-09-14.md),
[allocation protocol](E3_ALLOCATION_PROTOCOL_v2.md),
[allocation data](e3_fep_seed_results/v4/final_results.json),
[OB1 data](e3_fep_seed_results/ob1/final_results.json),
[OB2 protocol](E3_OBSOLESCENCE_PROTOCOL_v2.md),
[OB2 data](e3_fep_seed_results/ob2/final_results.json).

## 6. What has been established, and what remains open

The strongest supported progression is:

1. Maintenance behavior is easily produced by ordinary control.
2. Ordinary learning can acquire a resource priority because that resource
   sustains a learned capability.
3. Developmental history can alter later resource preferences and functional
   dependencies in a shared maintained network, with substantial reliability limits.
4. Protecting acquired information requires accounting for every surviving copy;
   material restoration alone is not informational reconstruction.
5. Conventional damage-aware repair is a much stronger baseline than recency.
6. Learning a statistic accurately is insufficient when it answers the wrong
   question or feeds an ineffective allocation rule.

The intended breakthrough has **not** been demonstrated. The missing causal
closure is that the acquired, vulnerable organization both generates action and
maintains the information and mechanisms that enable its own decisions.
Self-produced boundaries, continuous individual development, and subjectivity
are also unestablished.

My synthesis of the next research target, not a new approved protocol:

> Can acquired organization create and regulate a new maintenance dependency
> when the information needed to recognize and manage that dependency is itself
> vulnerable and maintained through the same substrate?

A useful proposal must specify its surviving information, protected generic
machinery and objective signals, and discriminate against competent conventional
control. It should retain partial-damage recovery without feedback, complete-loss
noninterference, causal rescue/sham interventions, and viable relinquishment.
This requires a new prospective question; it is not an instruction to resume
the stopped main E3 experiment or tune the completed side branch until it wins.

## 7. Record reconciliation and verification in this session

- README, the original guide and notebook remain valuable for motivation and
  E0–E2, but their E3 status/next-step passages predate later implementation.
- The September 10 readiness review is newer than the original handoff, but
  parts of its component inventory are superseded by current teaching source.
- Early sections of the September 14 branch record describe an unfrozen toy;
  later sections record the frozen allocation/OB studies. Read corrections and
  later outcomes before adopting an early conclusion.
- E3k/E3l are mentioned as external prior work, but their actual artifacts are
  absent from the available repository. The record reports broader unsuccessful
  searches. Their findings cannot be reconstructed or independently endorsed here.
- Git has three commits through `a52e825`; statements in earlier notes that it
  has only one commit are historical. Git provides coarse milestones, while
  protocols, engineering logs and tracking reviews preserve the detailed history.
- This session checked all **23 LF-normalized file entries across the allocation
  v2, OB1 and OB2 freezes**: no mismatches. Their frozen inputs remain intact.
- Across the six final configurations, checked **2,304 saved policy/seed rows**:
  expected rectangular coverage, unique policy/seed pairs and one recorded
  environment digest per seed. Recomputed primary recall differences agree with
  saved means to better than 1e-12. This checks recorded pairing, not a rerun of
  environment generation. Bootstrap intervals were read, not recomputed.
- Ran the existing **24 E1/E2 tests successfully** with Python 3.12.10 ARM64 and
  NumPy 2.3.5. Default Python 3.14 lacked NumPy; an initial sandboxed attempt with
  the compatible interpreter hit a temporary-file permission error. The approved
  rerun passed. No training or full E3 suite was rerun.
- The main E3 design verifier still reports the documented guide byte/hash
  mismatch. The branch erratum identifies mixed LF/CRLF conventions in the
  historical freeze. No old file or hash was changed to force a pass.
- Historical integrity caveats also remain: the E1 engineering-log hash predates
  its E2 appendix; earlier cross-environment replay checks found tiny continuous
  differences rather than exact matches; PACKAGE_MANIFEST is historical and
  incomplete. These are distinct from the passing current side-branch freezes.

This review read the principal narratives, protocols, decision/review records,
selected implementation paths, result tables, embedded per-seed rows and audits.
It is not an exhaustive line-by-line review of every contract, test or checkpoint,
nor a new verification of the cited external literature. No experiments, frozen
sources or historical evidence were modified. This synthesis is the only added
project artifact.
