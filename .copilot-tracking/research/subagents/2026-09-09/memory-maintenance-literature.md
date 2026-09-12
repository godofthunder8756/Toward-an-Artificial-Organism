<!-- markdownlint-disable-file -->
# E3 memory maintenance: targeted primary-literature review

Date: 2026-09-09

Status: Complete for the bounded four-area review, with access and source gaps
listed below. Research only; no experiment implementation or protocol freeze.

## Scope and project constraints

Read E3_DESIGN.md and NEW_AGENT_GUIDE.md, especially sections 6 and 12.
Investigate four requested areas: synaptic consolidation/tagging; palimpsest and
distributed associative memory; material/energy-constrained plasticity; lifelong
neural developmental programs. Verify primary-source metadata and state exactly
which abstracts or full-text sections were accessed. No novelty claims.

Questions: What can preserve acquired information without an external template?
What known mechanisms are simpler rivals? Which costs, hidden copies and recovery
conditions must an E3 protocol distinguish?

## Verified primary-source evidence

Access date: 2026-09-09. "Abstract only" means the original authors' abstract and
bibliographic record were read, not the paper's methods or figures. "Full HTML"
means substantive article text was retrieved and relevant sections examined; it
does not imply code execution, replication, or verification of every derivation.
Search snippets and papers mentioned in another article's bibliography are not
counted as independently reviewed sources. Implications below are E3 design
inferences, not findings these papers established about E3.

| ID / area | Verified authors, title, year and URL | Access actually obtained | Finding warranted | Limits and concrete E3 implication |
| --- | --- | --- | --- | --- |
| S1 / tagging | U. Frey; R. G. Morris. **Synaptic tagging and long-term potentiation** (1997), Nature 385:533-536. [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/9020359/); [DOI](https://doi.org/10.1038/385533a0). | Abstract only, via browser PubMed and Europe PMC; Nature full text not obtained. | Weak stimulation can produce persistent LTP when another input to the same neuronal population previously received strong stimulation. Results support transient, protein-synthesis-independent tags capturing products needed for late LTP. | Hippocampal LTP is not arbitrary-memory regeneration or demonstrated reward-based selection. Use finite-lived local eligibility and a separately limited consolidation resource; tags and signed labile changes themselves carry acquired information and must be costed and vulnerable. |
| S2 / palimpsest consolidation | Stefano Fusi; Patrick J. Drew; L. F. Abbott. **Cascade models of synaptically stored memories** (2005), Neuron 45:599-611. [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/15721245/); [DOI](https://doi.org/10.1016/j.neuron.2005.02.001). | Abstract only. Elsevier link returned a routing/script page, not readable full text. | A cascade of metaplastic states with different plasticities improves the acquisition-retention trade-off relative to compared models. | Protection against later learning is not protection against material destruction. Compare a fixed multistate/timescale mechanism before adding a learned allocator; count internal metaplastic states, not only visible synaptic efficacy. No detailed cascade scaling claim is inferred from this abstract. |
| S3 / complex synapses | Marcus K. Benna; Stefano Fusi. **Computational principles of synaptic memory consolidation** (2016), Nature Neuroscience 19:1697-1706. [Published abstract](https://pubmed.ncbi.nlm.nih.gov/27694992/); [DOI](https://doi.org/10.1038/nn.4401). Related author preprint: **Computational principles of biological memory** (2015), [record](https://arxiv.org/abs/1507.07580), [full HTML v1](https://arxiv.org/html/1507.07580v1). | Published abstract plus full 2015 preprint HTML; especially benchmark, model construction, limitations, M.5, S.3, S.7 and S.11-S.13. Published full text not obtained; versions not assumed identical. | Bidirectional fast-slow coupling supports strong initial traces and approximately linear memory-capacity scaling under the model assumptions. Preprint analyzes bounded, discretized hidden variables and retrieval circuits. | Main benchmark assumes random uncorrelated modifications and uses an ideal observer; excess leakage and input imbalance impair performance. Slow hidden variables are surviving memory, not information-free repair. Cost and damage every compartment; compare coupled, uncoupled and simple low-complexity baselines. Large-system scaling does not predict an advantage in tiny E3. |
| S4 / distributed association | J. J. Hopfield. **Neural networks and physical systems with emergent collective computational abilities** (1982), PNAS 79:2554-2558. [Primary abstract and metadata](https://europepmc.org/article/MED/6953413); [DOI](https://doi.org/10.1073/pnas.79.8.2554). | Abstract only. The page advertises free full text, but only its abstract/metadata were retrieved; PNAS redirected and PMC initially challenged access. | Asynchronous collective dynamics provide content-addressable recall from sufficiently large partial cues, error correction and tolerance to individual-device failures. | Completing a corrupted activity pattern is not rebuilding corrupted synaptic storage. Separate cue corruption, storage corruption and material loss. Ordinary attractor retrieval is a required explanation for apparent recovery, not evidence for adaptive maintenance. |
| S5 / energy-constrained plasticity | Ho Ling Li; Mark CW van Rossum. **Energy efficient synaptic plasticity** (2020), eLife 9:e50804. [Full article](https://elifesciences.org/articles/50804); [DOI](https://doi.org/10.7554/eLife.50804). | Full HTML, including synaptic caching, efficiency results, discussion and methods. | Cheap transient changes followed by threshold-triggered consolidation can reduce modeled plasticity expenditure. The favorable threshold depends on transient decay and maintenance costs. | Costs are assumed in arbitrary units, not measured ATP or hardware joules. The main cost model does not require active preservation of persistent weights. Include threshold caching as a strong simpler rival, but make both fast and persistent stores subject to declared E3 material costs and corruption. |
| S6 / biological resource trade-off | P.-Y. Plaçais; T. Preat. **To favor survival under food shortage, the brain disables costly memory** (2013), Science 339:440-442. [Primary abstract and metadata](https://europepmc.org/article/MED/23349289); [DOI](https://doi.org/10.1126/science.1226018). | Abstract only; no methods or numerical effect sizes independently checked. | In starved Drosophila, aversive long-term-memory formation is suppressed; artificial activation of implicated dopaminergic neurons restores formation with reduced survival. The abstract distinguishes appetitive memory. | This concerns gating formation, not selective erasure of obsolete stored content or reconstructing lost traces. Test cost-sensitive withholding of consolidation separately from relinquishment of an already acquired association; require continued viability and preservation of still-useful memories. |
| S7 / fixed developmental program | Alexander Mordvintsev; Ettore Randazzo; Eyvind Niklasson; Michael Levin. **Growing Neural Cellular Automata** (2020), Distill. [Full article](https://distill.pub/2020/growing-ca/); [DOI](https://doi.org/10.23915/distill.00023). | Full HTML, including model, experiments 1-4 and implementation discussion; interactive demos and notebooks not executed. | Local shared neural rules trained against a target pattern can grow, persist and regenerate that pattern; training on damaged states improves regeneration. | Fixed update-rule parameters retain the trained target; sample pools and pixel losses supply training information. Regeneration is not later-acquired episodic memory maintenance. Freeze generic developmental rules before drawing individual associations; exclude target-bearing rules, training pools and target losses from recovery. |
| S8 / within-lifetime developmental adaptation | Ivy Zhang; Sebastian Risi; Luke Darlow. **Petri Dish Neural Cellular Automata** (2025), author-hosted research article dated October 31. [Full article](https://pub.sakana.ai/pdnca/); [author project page](https://sakanaai.github.io/pdnca/). The site's suggested citation uses the shorter title **Petri Dish NCA**. | Full author HTML, including methods, learning ablation, searches and extensions. Linked PDF could not be extracted; peer-reviewed publication status not established. | Distinct NCA agents update parameters by gradient descent throughout the simulation; learned and non-learning conditions exhibit different dynamics. Optimization explicitly rewards total spatial aliveness. | Spatial competition/softmax is not an energy or material ledger. Parameters and gradient-based optimization remain separate from grid aliveness; the text does not establish their material maintenance or acquired-memory recovery. E3 must expose this protected learning machinery and avoid interpreting complexity, occupancy or continual gradients as informational self-maintenance. |

## Evidence anchors and key distinctions

* S3 preprint M.5 explicitly limits representational precision; S.7 warns that
  small memory systems may favor simpler synapses. Match total writable state and
  precision rather than neuron count, and do not extrapolate asymptotic advantages.
* S3 preprint S.3 identifies extra leakage as a limit on memory lifetime; S.11
  distinguishes event-triggered from continuously running dynamics. E3 wear must
  continue in elapsed simulation time when examples stop. Silencing input must not
  accidentally turn decay off.
* S5 "Synaptic caching" makes the live weight the sum of transient and persistent
  components. Both are copies of acquired information. Its discussion separates
  plasticity costs from signaling and resting-potential costs; E3 should likewise
  disclose which costs it models rather than call all computation energetically matched.
* S7 experiments 1-3 separate reaching a target, stabilizing it and regenerating
  it. The target is prescribed during training. S8 "Optimization objective" makes
  the territorial objective explicit, and its "Main Extensions" acknowledges
  unresolved measurements of cooperation and information use. Grid entropy or
  video incompressibility is not recovered association content.

## Strongest simpler explanation

Ordinary error-correcting storage, refreshed by a fixed decoder, plus an ordinary
reward-trained resource policy may explain the entire proposed result. Surviving
redundancy supplies the answers; repair supplies writable capacity; the policy
learns to fund refresh when useful and to stop when its reward disappears. Fast-slow
caching and passive attractor relaxation can additionally imitate delayed recovery
without a learned maintenance mechanism. S2-S5 and S7 warrant taking these rivals
seriously; this review does not assert that any one paper implements this exact
combined rival.

Use two complementary baseline comparisons:

1. Hold the finite-state representation, readout, damage and resource policy
   fixed; vary only consolidation/refresh allocation: adaptive, fixed periodic,
   fixed threshold, activity-shuffled and disabled. This tests the contribution of
   allocation rather than extra storage or a better decoder.
2. Compare the complete candidate against a matched standard error-correcting
   representation with ordinary reinforcement learning, plus a simple
   single-timescale/fast-slow caching rival. Match message information, total
   writable bits, spatial exposure, observations, rewards, actions and operation
   costs. Matching only the number of nominal weights is insufficient.

A protected exact-template control is informative but explicitly privileged, not
a fair competitor. If conventional correction and learning suffice, retain that
explanation. None of these outcomes establishes subjectivity or organismal autonomy
beyond the specific functional dependency tested.

## Concrete recommendations for the E3 protocol

Candidate falsifiable statement, not a frozen claim: under a declared corruption
and resource budget, adaptive consolidation preserves and restores independently
assigned, within-life associations after partial storage damage without answer
feedback, exceeding the matched fixed-refresh/code rivals by a prespecified
meaningful margin while preserving viability.

The following choices answer the guide's ten protocol questions at design level;
numerical values and the precise representation remain to be selected and frozen.

| Guide question | Recommended specification |
| --- | --- |
| 1. Acquired information | Learn independent uniformly assigned $K$-way outputs for opaque cue identities after generic rules are frozen. For $M$ cues this supplies $M\log_2 K$ bits of target entropy. Do not impose a learnable arithmetic mapping or a one-to-one assignment that permits deduction from other labels. |
| 2. All copies | Inventory traces, slow variables, tags, recurrent activity, learned readout/policy parameters, topology, resource allocation patterns, optimizer state and replay buffers. Count the combined finite-state capacity, including redundancy and writable metadata; nominal real-valued parameter count is not an information budget. |
| 3. Recovery access | Permit only surviving, declared in-agent state and cue identities. An evaluator may retain an isolated answer table for scoring, but no lookup, gradient, checkpoint restore, correctness reward or answer-dependent environment transition may feed it back during the decisive recovery block. |
| 4. Material's role | Material enables occupancy, writes and/or reduced future corruption, never a target value. Specify maintenance, read, communication, consolidation and write costs separately. Resource refill without writes cannot reverse an information-erasing intervention. Label units simulated, not ATP or hardware joules. |
| 5. Matched code | At minimum include repetition/majority refresh; select a stronger conventional code appropriate to the frozen error/erasure channel before implementation. Give it the same writable budget, local communication constraints, storage exposure and training signals, including costs for decoding and refresh. Pair it with the same resource-policy machinery where possible. |
| 6. Partial loss | Distinguish independent symbol errors, known erasures and spatially correlated losses; a known erasure location is extra information available equally to all variants. Freeze damage levels with recoverable redundancy. Include material-only restoration, intact material with trace damage, no damage, and consolidation-off counterfactuals. |
| 7. Complete loss | Overwrite every accessible target-bearing state with target-independent values and remove all external answer channels; mere attenuation or an invertible permutation is not deletion. Reinitialize material identically without restoring trace content. Expected forced-choice accuracy is $1/K$, subject to sampling uncertainty, not exactly chance in every finite run. |
| 8. Relinquishment | Change usefulness in a separately labeled feedback-enabled phase. Compare maintenance spending on obsolete versus still-useful, age/exposure-matched associations; require absolute savings with viable activity and retained useful recall. General starvation, inactivity, or forgetting everything does not pass. |
| 9. Protected machinery | Declare common simulator/update laws frozen before association assignment. Any machinery adapted to an individual's assignments is acquired state even if called an optimizer, genome, allocator or controller. Either place it under the same vulnerability/budget or narrow the claim and provide a matched protected-controller control. |
| 10. Abandonment criteria | Reject an adaptive advantage if it disappears under matched coding/feedback/budgets, persists unchanged with consolidation disabled, or depends on a privileged template. Complete-loss recovery materially above its frozen chance tolerance invalidates the information-boundary test and triggers a leakage audit. Failure to acquire the task or remain viable is a failed functional prerequisite, not evidence about consciousness. |

Separate development, no-answer-feedback recovery, and usefulness-change phases.
All variants receive identical permitted observations and objective signals within
each phase. Continuing association-dependent reward during recovery would turn the
test into relearning, even if no explicit target is presented.

Measure baseline recall, immediate post-damage recall, delayed recall and actual
trace changes. Compare delayed gain with inference-preserving consolidation-off
controls so passive decoding/relaxation cannot be renamed repair. A diagnostic
probe on an isolated clone after clearing fast inference activity can test whether
improvement persists in the declared storage rather than only in transient activity;
never return that clone or its labels to the live agent. Treat different coordinate
encodings as equivalent when measuring function; exact restoration of the original
weight array is not required.

Report useful recall per planned trial, completion/active fraction, viability,
resource expenditure, write counts and unused/obsolete-memory spending separately.
Do not equate raw grid entropy, trace agreement or mutual correlation between
redundant copies with information about the target. If estimating recovered bits,
prespecify a target-dependent estimator and its assumptions; $M\log_2 K$ is available
target entropy, not automatically the amount learned or retained.

Freeze a finite recovery horizon, a meaningful superiority margin, a viability
floor, a complete-loss chance tolerance and uncertainty method before fresh final
seeds. Use independent developed agents as replicates, pair interventions within
seed, retain failures, and separate engineering seeds. A nonsignificant departure
from chance is not proof of deletion; the audit and a prespecified chance-equivalence
criterion are both needed.

## Information-leakage checklist

* Scalar feedback can teach the answer: in a deterministic binary task, the action
  plus correct/incorrect feedback identifies the label. For K-way tasks repeated
  attempts can do the same. Keep all target-dependent rewards and physiological
  consequences out of the isolated recovery block, not only training examples.
* Hidden slow components are legitimate surviving information only when declared,
  costed and damaged consistently. Erasing visible weights but leaving eligibility,
  cached decoded weights, recurrent state, momentum or a teacher network intact is
  not complete loss.
* Connection placement, lesion locations, resource concentrations, timestamps and
  cue schedules can encode assignments. If an individual's own actions wrote such
  state, count it as memory; prevent simulator side channels from supplying labels.
* Independent label randomness must not be recoverable from an agent-visible seed,
  shared pseudorandom state or procedural cue generator. Use independent streams
  for targets, initialization, observation schedules and damage.
* Evaluation clones, saved checkpoints and source-run archives are experimenter
  records only. No recovery routine may load them or use their true-loss gradients.
  Predictions of maintenance value must use allowed local information; ground-truth
  counterfactual performance belongs only in an oracle control or offline analysis.
* Fixed NCA rules trained to a particular target are already a target-bearing copy.
  Freeze inherited rules before generating lifetime assignments and test on unseen
  assignment families. Continual global backpropagation, as in S8, must not silently
  furnish richer feedback than the local-rule or reinforcement-learning rivals.

## Access limitations and unresolved source gaps

* Full texts of S1, S2, S4 and S6 were not examined. Nature/PNAS redirects, initial
  PubMed/PMC cookie challenges and an Elsevier routing page limited direct access;
  browser PubMed and Europe PMC supplied original abstracts and verified metadata.
* S3's full-text evidence is the 2015 author preprint with a different title, not
  the 2016 journal version. Some extracted mathematical square roots were flattened;
  the recommendations rely on explicit prose and section-level findings, not copied
  rendered formulas. The paper versions have not been compared line by line.
* S8 is a primary author-hosted research report, not assumed peer reviewed. Its
  linked PDF failed extraction. Its quantitative claims about open-endedness and
  cooperation were not independently validated and are not adopted as E3 evidence.
* This bounded review covers the four requested areas. It does not complete the
  guide's separate primary-source obligations for adaptive versus fixed coding,
  fault-tolerant neural storage, or continual learning under destructive parameter
  corruption. S4/S7 provide adjacent evidence, not a substitute for those reviews.
* None of the accessed evidence demonstrates the complete E3 combination of
  within-life random associations, costly vulnerable storage, answer-free recovery,
  same-substrate maintenance control and viable selective relinquishment. This is
  a limit of the reviewed evidence, not an assertion of originality or absence of
  prior work.

## Recommended next research not completed

* [ ] Verify a primary conventional error-correcting-code baseline against the
  intended finite-state, locality, noise/erasure and operation-cost constraints.
* [ ] Review primary continual-learning and fault-tolerant-memory studies with
  destructive parameter corruption, distinguishing protected reference weights,
  replay datasets and optimizer state from vulnerable storage.
* [ ] Obtain S1/S2/S4 full texts and compare S3's published version before importing
  detailed biological protocols, model equations or claimed capacity constants.

No clarification is needed to complete this literature task. Before protocol
freeze, choose the message alphabet/load, quantization, topology, material cost law,
damage channel, permissible controller state, seed count and decision margins.
These are experimental commitments, not facts settled by the cited papers.

## Session handoff

Question investigated: Which primary evidence and simpler rivals constrain E3
memory maintenance? All four requested areas have verified sources.

Mechanism implemented: None. Externally supplied objectives/rules: reviewed and
flagged, not changed. Engineering changes, frozen sample and experimental results:
none. Simplest sufficient rival: conventional correction/caching plus ordinary
reinforcement learning. Failures: source-access gaps listed above.

Established: a bounded, access-qualified literature basis and discriminating
protocol recommendations. Not established: an E3 result, novelty, autonomy or
subjectivity. Only this research document was authored or edited; sources were
read through web tools, and no notebooks, experiments or subagents were run.

Next falsifiable question: Does adaptive maintenance outperform matched fixed
refresh and coding after partial storage loss without any target-answer channel?