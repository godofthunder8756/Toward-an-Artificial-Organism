<!-- markdownlint-disable-file -->
# E3 error-correction literature and protocol research

Status: Complete, with explicitly bounded literature-access and exact-setting gaps
Research date: 2026-09-09
Scope: Research only. No experiment implementation or changes outside this document.

## Questions and local constraints

* Verify primary literature on fault-tolerant or self-repairing neural computation, adaptive versus fixed error-correcting codes, and continual learning under parameter corruption.
* Distinguish abstract-only inspection from full-text inspection and record the limits of each source.
* Specify a finite-information, resource-matched baseline for three or five replicas of binary associations, including payload, parity, metadata, and controller state.
* Specify an exact complete-information-erasure negative control, excluding hidden acquired bits and reward or evaluator feedback.
* Separate example-free recovery from external relearning, and selective forgetting from loss of viability.

Local sources read: E3_DESIGN.md in full; NEW_AGENT_GUIDE.md sections 6 and 12 in the workspace, not the separately open Downloads copy.

E3 remains proposed and unimplemented. Its target is maintenance of acquired information without an invulnerable weight backup. Material enables storage and writes but supplies no missing answer. Required rivals include conventional error correction with ordinary reinforcement learning. Partial-damage recovery, complete-erasure impossibility, resource accounting, and relinquishment of useless information while viable are central constraints. No outcome establishes consciousness or generic originality.

## Verified primary literature

Reading labels distinguish an abstract or author publication record from inspection of the actual paper body. Full-text inspection below means the relevant methods, results, and discussion were read, not that every reference or derivation was independently checked. Sources were retrieved on 2026-09-09. No experiments or accompanying source code were run.

### S1: Hamming, 1950, fixed error correction

R. W. Hamming. "Error Detecting and Error Correcting Codes." The Bell System Technical Journal 29(2):147-160. DOI: 10.1002/j.1538-7305.1950.tb00463.x.

* Primary text: [archived original article, full-text OCR](https://archive.org/stream/bstj29-2-147/bstj29-2-147_djvu.txt), linked to the [scan record](https://archive.org/details/bstj29-2-147).
* Reading status: full article OCR retrieved; sections 1-5 and 7-9 inspected. PDF retrieval did not yield readable text. OCR equations and tables have defects; do not copy their corrupted typography.
* Evidence: section 1, pp. 148-149, separates information digits from check digits and defines redundancy as total digits divided by information digits. Section 3, pp. 150-153, gives the seven-position code with four information and three check positions. Section 4 adds overall parity for single-error correction plus double-error detection. Section 5 relates correctability to minimum distance. Section 7 describes a fixed parity-check matrix independent of the transmitted information.
* Implication: parity is acquired information about the payload, not free generic machinery. The parity-check rule can be generic; the parity values cannot. A decoder must read surviving information-bearing symbols.
* Limit: this is a coding construction, not learned allocation, metabolic maintenance, or a proof that a particular code dominates under spatially correlated damage and read/write costs. Hamming explicitly distinguishes redundancy from implementation economics.

### S2: Wade and colleagues, 2012, neural compensation

John Wade, Liam McDaid, Jim Harkin, Vincenzo Crunelli, and Scott Kelso. "Self-repair in a bidirectionally coupled astrocyte-neuron (AN) system based on retrograde signaling." Frontiers in Computational Neuroscience 6:76. DOI: 10.3389/fncom.2012.00076.

* Primary text: [publisher full text](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2012.00076/full).
* Reading status: full-text methods, results, figure captions, and discussion inspected; image-only parameter tables not transcribed.
* Evidence: two modeled neurons each receive ten synapses with Poisson input. Damage lowers synaptic release probability. Under the "complete fault" condition, eight of ten synapses have probability set to zero; these remain silent, while the two surviving synapses increase transmission probability. Figures 6-7 show partial recovery of output firing. Equation 18 uses an initial release probability; the text explicitly says this value is changed to the fault value when a fault is induced.
* Implication: include a homeostatic compensation rival. Restored firing or material does not establish restored arbitrary association content. The paper's "complete fault" is complete failure of selected synapses, not destruction of all information in the network.
* Limit: small computational model, not recovery of newly learned random binary associations. The discussion acknowledges biological-model and large-network limitations. Do not misdescribe its initial release probability as a secretly preserved pre-fault template; the stated fault intervention changes that value.

### S3: Mordvintsev and colleagues, 2020, neural regeneration

Alexander Mordvintsev, Ettore Randazzo, Eyvind Niklasson, and Michael Levin. "Growing Neural Cellular Automata." Distill. DOI: 10.23915/distill.00023.

* Primary text: [original research article](https://distill.pub/2020/growing-ca/).
* Reading status: full-text model, experiments 1-4, and engineering discussion inspected. Interactive demonstrations and code were not executed.
* Evidence: sixteen real-valued state channels per cell and a shared learned neural update rule; target-image loss trains that rule. Experiment 3 trains regeneration by zeroing spatial regions of sampled states. The engineering discussion explicitly places neural weights and control code in ROM, separate from mutable cell state.
* Implication: strong precedent for local regeneration and a particularly clear warning about the information boundary. Deleting cell states while retaining target-trained update weights does not erase the target information.
* Limit: regenerate a trained target pattern, not arbitrary lifetime-acquired associations absent from inherited rules. E3 can retain generic rules only if frozen before the test associations are sampled; test-specific learned repair weights must be budgeted and damaged.

### S4: Kirkpatrick and colleagues, 2017, consolidation and perturbation

James Kirkpatrick et al. "Overcoming catastrophic forgetting in neural networks." PNAS. DOI: 10.1073/pnas.1611835114. Author preprint arXiv:1612.00796v2, revised 2017-01-25.

* Primary sources: [author preprint record](https://arxiv.org/abs/1612.00796), [full-text author preprint](https://arxiv.org/html/1612.00796v2).
* Reading status: full-text sections 2-3, equation 3, Figure 3C caption, and relevant Atari appendix inspected. This is the author-preprint version, not a claim of separately checking every detail against the publisher version.
* Evidence: the EWC loss penalizes deviation from old task parameters, weighted by diagonal Fisher information. The discussion explicitly requires three values per synapse: current weight, variance, and mean. The Atari system additionally has task-specific gains/biases, task-recognition state, replay buffers, and a target network.
* Important qualification: the paper DOES test parameter perturbations. Section 2.2 and Figure 3C compare uniform Gaussian noise, inverse-Fisher-shaped noise, and noise in the estimated Fisher nullspace. A new random perturbation is drawn every timestep during ten game episodes. The experiment probes sensitivity and approximation quality; it is not a permanent-memory-erasure or autonomous reconstruction experiment.
* Implication: EWC is relevant to importance-weighted protection and continual-learning interference. It does not automatically establish corruption robustness, and it cannot be imported with free protected anchors. A corruption comparison must include anchors, Fisher estimates, replay, task identifiers, optimizer and target-network state in the acquired-state ledger.
* Limit: successful sequential learning and a noise-sensitivity probe do not demonstrate recovery after permanent destruction of all copies. Even compressed sums of EWC penalties retain acquired statistics; compression is not erasure.

### S5: Yoon and Erez, 2010, flexible energy-conscious ECC

Doe Hyun Yoon and Mattan Erez. "Virtualized and flexible ECC for main memory." ASPLOS XV / ACM SIGPLAN Notices 45(3):397-408. Verified journal-record DOI: 10.1145/1735971.1736064; Crossref also returns proceedings DOI 10.1145/1735970.1736064.

* Primary source: [publisher article and abstract](https://dl.acm.org/doi/10.1145/1735971.1736064).
* Reading status: publisher abstract and metadata only. PDF extraction failed; a final in-memory retrieval using system certificate verification returned HTTP 403. The paper body was not read.
* Evidence available at abstract level: separates physical mapping of data from ECC information, stores redundant information in the memory namespace, and separates frequent error detection from infrequent correction. The abstract reports DRAM power savings up to 27% in its evaluated configurations; this is a configuration-specific reported result, not an E3 prediction.
* Implication: fixed worst-case protection is not the only conventional rival. Conventional ECC can vary protection organization and separate cheap monitoring from costly repair. Metadata and access costs belong in the comparison.
* Limit at this reading depth: no verified exact match to learned, utility-sensitive redundancy for newly acquired binary associations on an energy-limited, corruptible controller with all examples and answer-dependent feedback removed. Do not equate the title's "flexible" with a demonstrated E3-like online learning policy.

### S6: Patel and Hsiao, 1972, explicitly adaptive ECC

A. M. Patel and M. Y. Hsiao. "An adaptive error correction scheme for computer memory system." AFIPS Fall Joint Computer Conference, part I, pp. 83-87. DOI: 10.1145/1479992.1480002.

* Primary source: [publisher article and abstract](https://dl.acm.org/doi/10.1145/1479992.1480002).
* Reading status: abstract and publisher metadata only; in-memory PDF retrieval returned HTTP 403. No claims below require uninspected algorithm details.
* Evidence: the abstract motivates correction capability beyond single errors, but argues against paying the decoding time and redundancy of double-error correction on every memory fetch for occasional double errors. It discusses masking/logging faults and replacing permanent failures during scheduled maintenance.
* Implication: adaptation of correction effort and the cost of repair are established research topics, not generic novelty claims available to E3. Include inexpensive checks with selective costly correction as a conventional rival.
* Limit: the inspected abstract does not specify a utility-learning policy, energy-budget controller, code-rate switching algorithm, or example-free acquired-memory recovery. The precise algorithm requires full-text follow-up. Its maintenance-cost motivation is not itself a measured energy result.

### Coverage and honest evidence gap

Six primary sources are verified: four inspected beyond the abstract (S1-S4), two abstract-only (S5-S6). S2-S3 cover neural compensation/regeneration; S1, S5, and S6 cover fixed and flexible/adaptive error correction; S4 covers continual learning with a narrowly specified parameter-noise experiment. Publisher/author texts, not search-engine summaries, support the substantive claims.

No source verified here demonstrates the exact conjunction E3 requires: lifetime-acquired random associations, finite corruptible storage including the allocator, matched energy and information budgets, utility-sensitive redundancy, recovery without target-dependent feedback, and an exact complete-erasure control. This is a gap in this bounded review, not evidence that no such paper exists. In particular, permanent-corruption continual learning with all auxiliary memories also damaged remains unverified. Do not substitute EWC's anti-interference result for that missing evidence.

## Baseline and budget recommendations

### Define the information before choosing the mechanism

Use K fixed, public cue addresses and a newly sampled table Y of K independent fair binary answers. Freeze generic algorithms and hyperparameters before drawing final tables. These are arbitrary associations, not labels predictable from cue features. Acquisition occurs once through the declared examples and rewards. K independent bits have entropy K; do not call r replicas rK independently acquired bits.

Do not enforce an exactly half-zero, half-one table: that creates cross-association constraints. If a short seed deterministically generates the table, its entropy is bounded by the seed entropy, and the seed is itself a compressed answer source. Keep the table generator and its state outside the agent, use independently generated streams, and describe the entropy assumption accurately.

The simplest confirmatory representation is one binary value per trace, with r = 3 or r = 5. If traces instead have q bits of precision, their capacity is rqK bits, not rK. Magnitudes, confidence values, timestamps, structural choices, and resource concentrations cannot become uncharged analog memory.

### Same-representation rival: repetition plus paid scrubbing

For each answer bit store r spatially separated copies and decode by majority. Both arms use the same physical locations, observation access, damage process, precision, and operation costs. The decoder sees current traces, never a true answer. At a scheduled scrub it reads the copies, computes the current estimate, and pays to rewrite disagreeing or erased copies. Only commit writes that its budget permits.

For independent unflagged flips with common probability p below 1/2, majority is the maximum-likelihood and equal-prior Bayes decoder. The following are mathematical consequences, not empirical E3 results:

$$
P_{\mathrm{err},3}=3p^2-2p^3,\qquad
P_{\mathrm{err},5}=10p^3-15p^4+6p^5.
$$

Three copies correct one unknown flip per association; five correct two. With trustworthy known erasure locations and no flips, one surviving copy suffices, so up to r-1 erasures per association are recoverable. A loss marker is extra channel information, not equivalent to an unflagged bit flip. Account for its representation or declare it a shared exogenous sensor.

If observable local health implies unequal independent flip probabilities, give the conventional decoder the same quantized reliability estimates. A likelihood-weighted vote can outperform unweighted majority without a new maintenance principle. The weights can be computed from declared shared damage laws or learned from permitted observations; inaccessible true per-cell correctness or oracle reliability must not be supplied. Count persistent reliability estimates and their update costs. The homogeneous formula above does not establish majority optimality for unequal or correlated faults.

Use at least these conventional conditions:

1. Fixed repetition with inference only and no corrective writes.
2. Fixed repetition with an engineering-tuned periodic scrub schedule. Tune intervals and write thresholds on independent engineering tables, then freeze them; do not use an intentionally wasteful every-step schedule as the only rival.
3. The same repetition code and decoder with a finite-state ordinary RL or tabular maintenance allocator. Give it the same feedback, action set, state precision, training budget, and damage exposure as the proposed mechanism. A conventional allocator can prioritize useful associations, alter scrub frequency, and relinquish obsolete ones without inventing a new code.
4. A matched block-code rival if cross-association mixing is allowed. This tests the weaker explanation that the mechanism merely uses storage more effectively than repetition.

Distinguish a fixed code from a fixed maintenance policy. A fixed code with an adaptive scrub allocator is already a strong adaptive baseline. If a policy switches code rates, include the format identifier, relocation map, re-encoding reads/writes, and temporary coexistence of old and new codes in its budget. Lost information cannot be restored by switching to a stronger code after the loss.

### Repetition versus block coding at the actual budgets

Use four independent associations per illustrative block. Entries below count binary code symbols only, before controller state, flags, or scratch memory. Redundancy is n-k, while the total acquired payload remains k=4. The distance d column gives a worst-case block guarantee, not a universal ranking under all spatial faults.

| Representation | Physical code bits n | Payload dimension k | Redundant bits n-k | Minimum distance d | Guaranteed unknown flips anywhere in block |
| --- | ---: | ---: | ---: | ---: | ---: |
| Four independent triplets | 12 | 4 | 8 | 3 | 1, or up to 1 in each triplet |
| Four independent quintuplets | 20 | 4 | 16 | 5 | 2, or up to 2 in each quintuplet |
| Hamming [7,4,3] | 7 | 4 | 3 | 3 | 1 |
| Extended Hamming [8,4,4] | 8 | 4 | 4 | 4 | 1, with detection of 2 in SECDED mode |
| Derived fixed linear [12,4,6] rival | 12 | 4 | 8 | 6 | 2 |
| Derived fixed linear [20,4,10] rival | 20 | 4 | 16 | 10 | 4 |

The final two rows are explicit protocol-design derivations, not attributed experimental findings or unverified paper citations. They prevent the unfair comparison of 12 or 20 replica bits against only 7 Hamming bits with the remaining capacity wasted:

* Start with the 15-bit binary simplex encoding of a four-bit vector y: store y dot a modulo two for every nonzero four-bit vector a. Let e1 through e4 denote the four unit basis vectors; all vector additions are modulo two. For every nonzero y, exactly eight of those values equal one.
* For n=12, omit columns e1, e2, and e1+e2. Their three outputs have weight either zero or two. Every nonzero encoded vector therefore has weight six or eight; the minimum distance is six. The remaining columns retain dimension four.
* For n=20, keep all 15 columns and add another copy of each of e1, e2, e3, e4, and e1+e2+e3+e4. If y has weight w, these five outputs have weight w+(w mod 2), which is two or four for nonzero y. Minimum distance is therefore ten, with dimension four retained.

These are fixed parity-based block codes. Their generator description can be shared generic machinery, independent of Y. There are only 16 possible codewords; a generic minimum-distance decoder or a channel-likelihood decoder can consider them without a task-specific answer table. Actual decoder work, scratch registers, reads, and rewrite operations still have costs. For pure erasures the respective block guarantees are five and nine erased symbols; more generally unique correction is guaranteed when 2v+e<d for v unknown flips and e known erasures.

Recommendation: make repetition plus an ordinary adaptive allocator the primary same-representation rival, and add the derived budget-filling block code as a storage-efficiency challenge, subject to a later independent check of the algebra and operation accounting. Plain Hamming is a useful low-overhead point on the budget curve, not the sole matched-budget opponent. For K divisible by four, the derived block codes use exactly 3K or 5K code cells. Preregister handling of incomplete final blocks rather than ignoring padding costs.

Block coding is not guaranteed to win. Repetition can correct one error in every triplet, a pattern with four total errors that exceeds the [12,4,6] global guarantee. Block decoding may require reading many more cells per cue, communicating across locations, and jointly maintaining unrelated associations. It can impede selective forgetting when obsolete and useful bits share parity. Match or explicitly restrict locality and wiring; report independent flips, flagged loss, and common-region damage separately. If the proposed mechanism uses cross-association coupling, do not prohibit that coupling only for the baseline.

### Complete finite-state and resource ledger

Maintain both a capacity ledger and an energy/material ledger. Equal entropy of the labels is not equal capacity to preserve them.

$$
B_{\mathrm{total}}=n_{\mathrm{code}}+B_{\mathrm{flags}}+B_{\mathrm{metadata}}
+B_{\mathrm{policy}}+B_{\mathrm{optimizer}}+B_{\mathrm{eligibility}}
+B_{\mathrm{recurrent}}+B_{\mathrm{scratch}}+B_{\mathrm{other}}.
$$

Each term denotes declared finite storage bits, not number of Python variables. Shared fixed constants need not be acquired information, but physical runtime work is still charged. For a first comparison reserve the same finite controller/metadata allowance C for all arms and set total capacity to rK+C. An arm does not get a free float-valued controller because its visible traces are binary. Report any unused capacity and permit conventional rivals the same useful allocation options.

| Component | Required treatment |
| --- | --- |
| Payload copies and parity values | Count and corrupt alike; no protected systematic copy or special invulnerable parity bank |
| Public fixed cue addresses and generic code matrices | May be inherited constants if independent of final answers; charge access/routing costs |
| Learned key-address maps, topology, allocation decisions, code-format identifiers | Finite metadata, potentially answer-bearing; count, maintain, and erase when required |
| Occupancy/validity masks, health estimates, counters, timestamps | Specify precision and persistence; damaged or maintained state unless a declared common sensor |
| Policy/value/target-network weights, biases, hidden activations | Acquired copies if trained on that lifetime; same information boundary and fault exposure |
| EWC anchors/Fisher arrays, optimizer moments, gradients, eligibility traces | Acquired state, not free learning machinery; include all preserved summaries |
| Replay, recent observations/actions/rewards, batch buffers, normalization statistics | Potential copies; no inaccessible-to-the-experimenter exceptions |
| PRNG states and counters, cached random arrays, label-generation seed | Separate streams and access; no regenerating answers from a preserved master seed |
| Material distribution, energy reserves, routing state, write queues | Finite measurable state; may indirectly encode lifetime history and therefore labels |
| Temporary decoded words, syndromes, correction buffers | Bounded scratch; do not let an unscrutinized register become the durable clean master |

Charge storage occupancy over time, reads, writes, decoding/computation, communication distance, and any resource conversion costs. A possible accounting form is:

$$
E=c_s\sum_t n_{\mathrm{live}}(t)+c_rN_{\mathrm{read}}+c_wN_{\mathrm{write}}
+c_oN_{\mathrm{ops}}+c_lN_{\mathrm{link}}.
$$

Add chemistry-specific material constraints. Coefficients and allowed sensing must be fixed before final data. Report the vector of costs as well as any aggregate; identical joule totals do not guarantee identical bottlenecks across chemistries.

### Distinguish tolerance, repair, and retention

Majority decoding can mask a damaged copy immediately. Rewriting that copy need not improve current recall accuracy, because recall was already correct. Measure current recall, paid reconstruction of the physical representation, and recall after a preregistered subsequent challenge or retention interval. The experimenter may measure distance to the original encoded state offline, but that distance must never enter the agent's feedback.

Scrubbing can cement a wrong majority or a misdecoded block. Report miscorrections, uncorrectable blocks, abstention/forced-guess rules, and capacity loss, not only successful repairs. A drop in codeword corruption with no useful behavioral retention is insufficient. Conversely, immediate damage tolerance is not evidence of ongoing reconstruction.

## Exact-erasure and feedback controls

### Structural requirement, not a nonsignificance claim

Let G be inherited generic machinery and public cue definitions, Y the independent random answer table, S+ all agent-reachable state after erasure, and Z the subsequent external observations, rewards, material deliveries, and random inputs. Construct the negative control so that:

$$
P(S^+,Z\mid Y,G)=P(S^+,Z\mid G).
$$

With generic state transitions that do not read Y, every future prediction is then independent of Y conditional on G and the cue. For each forced binary answer, expected accuracy is exactly $1/2$; the probability of an exact K-bit table guess is $2^{-K}$. These are distributional statements, not requirements that each finite run score exactly 50%. Material restoration and additional computation cannot break this independence.

Do not implement "complete erasure" as a sign flip, permutation, large-but-finite noise, or a reset of only the visible replicas. Those interventions may preserve all or some information. Overwrite all acquired state with the same target-independent canonical state, or sample a fresh state from a distribution independent of the previous history and targets. A zero-filled code bank is allowed even if it decodes to all zeros, since it is the same state for every target table.

### Required complete-erasure procedure

1. Sample arbitrary final answers only after generic rules are frozen. The agent cannot inspect the table, generator seed, run manifest, evaluator state, filesystem records, or simulator closure containing answers.
2. End acquisition at a fixed, target-independent boundary. Inventory the entire reachable mutable state, including policy, optimizer, eligibility, PRNG, scratch, and physical/environmental traces. Pending events and delayed feedback must be included.
3. Replace all such acquired state by a canonical fresh state independent of Y. Reset resource reserves and spatial allocation patterns if their history could encode Y. Delete queued writes, decoded estimates, caches, target networks, and trajectory histories. Use fresh independent recovery randomness; resetting to a known master seed that generated Y is not independent.
4. Retain only declared target-independent generic laws. If a learned policy has encountered Y, it must be erased too; calling it a controller does not make it inherited. Do not restore a pretrained-on-Y initializer after erasure.
5. Run a fixed-duration recovery interval without association examples or any answer-dependent feedback. Exogenous resource opportunities and injury masks must be target-independent. A safe cue-independent resource activity or explicitly declared neutral life support can keep the blank organism capable of acting; this supplies capacity, not labels.
6. Freeze the evaluated state and obtain predictions through a one-way interface. Keep true answers only in the isolated evaluator, with no references accessible to the agent or its recovery environment. Score after predictions are finalized; do not return scores, stop signals, gradients, or counterfactual snapshots to the live agent.
7. Treat any reproducible target dependence after this reset as an invalid information boundary. First investigate leakage, reset omissions, correlations, selection, and evaluator coupling; do not interpret it as enhanced self-repair.

Erasing one association is harder than erasing the entire acquired state: parity shared with other associations, policy state, or remaining constraints may reconstruct it. For the decisive negative control erase the entire acquired table and all derived state. If a per-association variant is later added, erase its full dependency closure, not only its named replicas.

### Exact tests and finite-sample reporting

For the four-bit micro-assay, enumerate all 16 target tables offline. Acquire each table in a separate history, apply the actual erasure operation, and verify that it produces the identical canonical post-erasure state. Then supply identical subsequent random inputs and cue schedules. The entire agent-side trajectory and predictions must be identical across tables, while the evaluator alone retains a different answer key. For each cue, pooled correctness over all tables is exactly half; an identical complete predicted table matches one of the 16 keys. This checks the reset itself, not merely an already-blank initializer, without treating a large p-value as proof of no information.

Also check paired histories differing in each individual target bit, not only global complementation. A global complement check alone can miss invariant encodings such as some parity functions. The planned implementation should compare all reachable agent/environment state and outputs at the erasure boundary, use an explicit field allowlist, and verify that transitions have no target-key input. Enumeration validates the small instance; it does not replace the structural argument for larger systems or every random seed.

For larger repeated runs preregister a practically meaningful equivalence margin around 1/2, sampling precision, and the independent replication unit. Use independently sampled target tables and agent seeds, with paired condition comparisons. Repeated queries of the same bit are not independent new Bernoulli trials. A confidence interval contained within an equivalence band can support the absence of a practically important accuracy advantage; "not significantly above chance" cannot. Below-chance target dependence is also a leak warning, since inverting outputs could exploit it.

### Withholding examples does not withhold information

For a binary query with chosen answer a and deterministic correctness reward r, one reward reveals Y: Y=a when r=1 and Y=1-a when r=0. A scalar reward is therefore a teaching signal even without an explicit example. This applies equally to reward delivered as energy, survival, resource access, an error tone, a delayed outcome, or a performance-triggered end to recovery. Aggregate rewards can also constrain a table and reveal bits through repeated probing.

Use separate named assays:

* In the information-isolation assay, withhold labels and all outcomes dependent on the hidden associations. Maintenance can receive only target-independent opportunities/costs and information derived from its own surviving state. No truth-based reward for "correct repair," true uncertainty reduction, or retention improvement is available.
* In the ecological feedback assay, task-dependent returns may train allocation and support viability. Report them as an external information channel. Recovery there may be relearning through reward and cannot by itself establish reconstruction from redundancy.

Partial-damage and full-erasure isolation arms must share the same feedback restriction. Fixed-duration neutral support is preferable to trying to stop reward just before it leaks. Recovery scores, probe accuracies, oracle importance estimates, and parameter-selection decisions stay offline. Checkpoint-based counterfactuals may serve experimenter analysis only; no repaired state, clean checkpoint, or resulting score goes back to the live trajectory.

### Viable relinquishment of useless information

After acquisition, independently withdraw opportunities for a random subset of associations or set their usefulness to zero. The usefulness manipulation may reveal which cue is obsolete, but must not reveal its binary answer. Keep a disjoint set of useful associations and a cue-independent means of obtaining maintenance resources. Apply real scarcity so preserving everything has an opportunity cost; do not award a hidden score for matching a desired forgetting pattern.

Compare utility-sensitive E3 against utility-sensitive conventional ECC plus the same ordinary allocator, not only against an always-copy-everything rival. Measure maintenance spend per obsolete versus still-useful bit, retention of useful bits, resource capture, and a preregistered viability threshold. Assess all randomized agents, including failures; analyzing only survivors would bias the result.

Reduced maintenance of obsolete information should save resources while useful performance and viability remain acceptable. Optional delayed offline recall can measure whether obsolete information was actually lost, but reduced spending need not cause immediate forgetting when traces persist. Do not equate global shutdown, failure to answer, or blanket forgetting with selective relinquishment. If usefulness returns, reacquisition with new feedback is a separate assay, not retrospective evidence that deleted bits survived.

### Minimal intervention and decision set

| Intervention | Required interpretation |
| --- | --- |
| Partial recoverable damage, no target-dependent feedback | Can surviving distributed information support paid reconstruction and later useful recall? |
| Same damage, corrective writes frozen | Separates passive fault tolerance from ongoing maintenance; charge common inference equally |
| Material restored, trace values not restored | Capacity alone must not act as an answer template |
| Protected exact answer template | Explicit oracle positive control; never part of the fair information-matched comparison |
| Complete reset of all acquired information | Exact noninterference control with chance expected recall, not merely a nonsignificant difference |
| Repetition/block code plus matched ordinary allocator | Tests whether conventional correction and resource policy explain the benefit |
| Independently withdrawn usefulness with safe resources available | Tests selective spending and retained usefulness while viable |

Abandon the proposed added-mechanism explanation if the apparent advantage depends on free auxiliary memory, privileged damage labels or reward, larger information/energy budgets, or weaker baseline tuning. If conventional ECC plus ordinary allocation matches outcomes within a preregistered meaningful margin, retain that simpler explanation. If full erasure leaves target dependence, invalidate the assay before comparing mechanisms. Positive matched results would establish a bounded maintenance mechanism, not consciousness or recovery of information from nothing.

## Limitations and open decisions

* This review is targeted, not a comprehensive novelty search. Consolidation/tagging, palimpsest memory, material-constrained plasticity, and lifelong developmental programs elsewhere in the guide remain outside this assigned literature slice.
* Hamming was read through OCR with visibly damaged mathematical typography. The small-code constructions and probability formulas above are explicitly derived protocol recommendations, not reproduced measurements; no implementation has been validated.
* S5-S6 support the existence and motivation of flexible/adaptive conventional correction, but their full algorithms were inaccessible in this session. Their exact code switching, metadata, and energy accounting need full-text inspection before reproduction. No security or certificate checks were disabled to fetch papers.
* The distinction among transient parameter noise, persistent flips, flagged erasure, cell destruction, and correlated spatial damage must be frozen. Guarantees for one channel cannot be transferred to another.
* Generic trusted decoding/update logic is compatible with an acquired-information experiment when independent of final labels and equally available to rivals. It does not establish that every simulator law or computation element is itself fault tolerant.

Questions requiring protocol-owner decisions, not additional literature alone:

1. Are the three/five traces genuinely binary, or do they carry additional finite-precision confidence or analog state?
2. May codes mix associations across locations, and what access/locality limits and communication costs apply equally to all arms?
3. Which bounded controller, scratch, metadata, health-sensor, and resource-state allowances are included above the 3K/5K code-cell budgets?
4. Will the decisive recovery phase exclude all target-dependent returns, with ecological reward learning reported separately?
5. What viability thresholds, meaningful retention/energy effect margins, and independent replicate counts will be frozen before final runs?

No clarification is needed to complete this research artifact. These are decision gates before implementation, not reasons to alter models now.

## Recommended next research

* [ ] Obtain S5-S6 full text through an author or library route; inspect adaptive policy, correction-state storage, and measured versus modeled energy costs before adopting either algorithm.
* [ ] Locate a direct continual-learning study of persistent parameter corruption that also accounts for corrupted auxiliary memories; do not relabel EWC as that evidence.
* [ ] Independently review the [12,4,6] and [20,4,10] parity-code derivations and costed decoder choices before freezing a block-code baseline.
* [ ] Review a future explicit acquired-state manifest and evaluator interface for complete-erasure noninterference, including physical state, random streams, and delayed events.

Only .copilot-tracking/research/subagents/2026-09-09/error-correction-literature.md was intentionally created or edited. No model files, protocols, experiment code, or experiment results were changed. No subagents were used.