# ACI primary prior-art and reduction audit v1

Targeted public-source audit for three candidate routes. No training, simulation,
architecture construction or novelty claim. These are mechanism precedents and
reduction attacks, not evidence that the ACI system realizes them.

Primary paper text was verified in a separate research review. This is not an
exhaustive survey. Earlier mistaken knapsack/NIPS references and guessed Boots
PMLR pages are discarded. Wikipedia is not the primary PSR reference.

## Verified primary sources

| ID | Reference | Primary source and evidence locator |
| --- | --- | --- |
| P1 | Littman, Sutton, Singh, *Predictive Representations of State*, 2001, NeurIPS 14 | [Primary PDF](https://proceedings.neurips.cc/paper_files/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf), sections 1-3. The PDF includes Singh; current landing metadata omits him. |
| P2 | Singh, James, Rudary, *Predictive State Representations: A New Theory for Modeling Dynamical Systems*, UAI 2004, 512-519 | [Primary paper](https://arxiv.org/pdf/1207.4167), sections 2-5, Lemmas 4-5 and Theorem 6. The 2012 arXiv deposit is not the publication year. |
| P3 | Boots, Siddiqi, Gordon, *Closing the Learning-Planning Loop with Predictive State Representations*, RSS VI, 2010 | [Official proceedings](https://www.roboticsproceedings.org/rss06/p36.html), [paper](https://www.roboticsproceedings.org/rss06/p36.pdf), [DOI](https://doi.org/10.15607/RSS.2010.VI.036), sections II-IV. |
| E1 | Scellier, Bengio, *Equilibrium Propagation: Bridging the Gap Between Energy-Based Models and Backpropagation*, 2016 preprint / 2017 journal | [Correct arXiv](https://arxiv.org/abs/1602.05179), [inspected v5](https://arxiv.org/pdf/1602.05179v5), [DOI](https://doi.org/10.3389/fncom.2017.00024), sections 2-3 and Theorem 1. |
| E2 | Hopfield, *Neural networks and physical systems with emergent collective computational abilities*, PNAS 79(8), 1982, 2554-2558 | [Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC346238/), [DOI](https://doi.org/10.1073/pnas.79.8.2554), energy argument at equations 7-8. |
| L1 | Mordvintsev, Randazzo, Niklasson, Levin, *Growing Neural Cellular Automata*, Distill, 2020 | [Primary article](https://distill.pub/2020/growing-ca/), [DOI](https://doi.org/10.23915/distill.00023), Model, Experiments 1-3, Discussion. |
| L2 | Varela, Maturana, Uribe, *Autopoiesis: The organization of living systems, its characterization and a model*, BioSystems 5(4), 1974, 187-196 | [Original university-hosted scan](https://homepages.math.uic.edu/~kauffman/MUV.pdf), [DOI](https://doi.org/10.1016/0303-2647(74)90031-8), sections 3, 6-9 and Appendix. Publisher access failed; original scan and bibliographic metadata were checked. |

## Route 1: predictive state / ordinary estimation and control

**Primitive:** maintain predictions of selected future action-observation tests;
update that state recursively from permitted experience.

P1 constructs predictive state from a supplied finite POMDP. P2 describes the
history-by-test system-dynamics matrix and its finite-rank linear realization.
P3 learns transformed predictive state from observable moments and couples
filtering with approximate planning. These are substantial precedents for
first-order representation without a workspace or explicit self-module.

**Supplied:** observation/action interface, initial conditions, basis/model
parameters or their identification procedure, rewards and planning machinery.
Sensorimotor feedback is not production of the estimator's enabling organization.
Controlled action predictions require interventions, not merely correlations
under a behavior policy.

**Reduction:** recursive sufficient statistics + system identification +
conventional control. This is the principal null explanation, not an inherently
inferior baseline.

**Cheapest attack:** determine which histories require distinct action-conditioned
future predictions and whether an ordinary filter already retains exactly those
distinctions. Derive basis/update closure when possible; compare finite-state,
direct-history and monolithic recurrent alternatives on the same information.

**Limits:** linear predictive dimension is not a universal minimum neural-state
dimension. A finite empirical Hankel matrix does not certify the exact infinite
rank; nonlinear representations can be smaller. Arbitrary-precision real
coordinates can hide enormous information, so state/precision/resource assumptions
must be explicit. PSRs are not all equivalent to finite POMDPs.

No autopoiesis, O3 closure, temporal individuality or consciousness follows.

## Route 2: recurrent energy / attractor / constraint dynamics

**Primitive:** cognition as recurrent settling toward a state satisfying shared
constraints, rather than retrieval of a privileged stored object.

E2 shows associative attractors with energy decrease under its symmetric,
asynchronous update assumptions. E1 combines a free equilibrium and a weakly
target-nudged equilibrium to obtain a gradient estimator under stated assumptions.
This is gradient-based learning prior art, NOT authorization to perform it here.

**Supplied:** units, connectivity, energy/constraints, update law, memories or
targets, and phase control. With fixed parameters, gradient-flow decrease
explains activity restoration; it does not rebuild the constraints themselves.

**Reduction:** ordinary associative memory, error correction, fixed-point
iteration or Lyapunov descent.

**Cheapest attack:** separate damaged activity from damaged enabling structure.
Derive the actual update's settling invariant where one exists. Test whether a
matched filter, redundant code or conventional recurrent circuit reproduces the
claimed causal role.

**Limits:** symmetric asynchronous energy arguments do not transfer automatically
to asymmetric/synchronous dynamics. Returning activity to a basin is not
maintenance of the architecture. Failure of an energy proof is not positive
evidence of closure. Efficient recovery could be engineering value without
distinctive organizational necessity.

## Route 3: locally reconstructed graph / process organization

**Primitive:** local processes reconstruct functionally necessary state,
components or relations; the produced organization may enable the processes
that continue producing it.

L1's local residual neural updates, gradient perception, stochastic masks and
living-cell masks support learned pattern persistence/regeneration. The lattice,
shared update network and externally trained weights remain supplied. Regrowth
principally restores cell-state organization, not processors or the update rule.
The mechanism is closely related to a recurrent residual convolutional network.

L2's catalyst converts substrate to boundary links; retention enables production,
and link renewal maintains retention. This is stronger than image restoration:
the produced boundary helps enable its own production.

**Supplied:** grid, initial constituents, chemistry/update law, transport,
permeability, masking or externally optimized target. L2 allows certain permanent
necessary constitutive components; an unproduced catalyst is therefore a limit,
not automatically a violation of that paper's own criterion. Do not claim its
catalytic capacities are regenerated.

**Reduction:** local reaction/transport, conventional feedback, redundant coding,
template propagation or an attractor. Such a description can still instantiate
bounded organizational closure; ordinary mechanism is not automatically a
refutation of closure.

**Cheapest attack:** audit exactly what is regenerated, what remains pristine,
and which produced components enable future producing processes. Lesion the
alleged enabling relation, not just visible state. For boundary retention,
permeability intervention with externally supplied retention rescue isolates
that dependency.

**Limits:** image regeneration does not establish process-production closure.
Neither source establishes arbitrary cognitive-graph reconstruction, cognitive
individuality or consciousness. Reopening an organism/local-architecture branch
requires human authorization and an identifiable question not already answered
by the existing material-boundary studies.

## Cross-route discriminator

Distinguish:

1. prediction/control with maintained sufficient state;
2. restored activity under intact implementing constraints;
3. restoration of enabling organization through processes depending on it.

The key question is **what is restored, and whether it restores the conditions
enabling restoration**. Compare causal organization, not aesthetic resemblance
to a brain or organism. Match information, developmental experience, substrate,
resource and vulnerability assumptions. Supplied primitive physics is permitted;
an undeclared protected cognitive mechanism is not.

The [next-experiment package](ACI_NEXT_EXPERIMENT_DECISION_v1.md) uses these
reductions to rank candidates after A6 and evidence synthesis. Its proposals
are not findings and are not execution permissions.
