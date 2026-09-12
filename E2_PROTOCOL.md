# E2 — developmental material dependence in a joint recurrent controller

Protocol frozen locally before seeds 200–215. This is not external preregistration.
E2 is a partial implementation of the E1b target, with important scaffolds below.

## Hypothesis and advance beyond E1a

H1: Activity-guided material renewal helps a single network acquire and maintain
its computational capabilities better than a fixed structural target or shuffled
activity guidance. H2: Paired developmental sensor histories create different
functional dependencies and corresponding resource priorities under a common
later environment. We predict these effects; they are not definitionally required
by our simulator. Ordinary adaptive control remains the rival explanation.

Both resource selection and delayed binary recall use the same 12 recurrent
neurons, the same maintained connections, input weights and one five-column
readout. Two columns select food gates; three select food/material A/material B.
Choices occur at different times, so the later cue cannot leak into the earlier
resource decision. No independent policy network or pretrained memory module.
Readout biases are absent. Every hidden update is gated by maintained biomass;
complete tissue lesions eliminate both sets of differentiated outputs.

The two precursor types sustain fixed, inherited groups of six target neurons.
Possible edges are fixed by a sparse mask. Continuous edge density grows and
shrinks, rather than new neurons or edge types being invented. The chemistry is
specified, not learned. Resources change actual recurrent multiplication and
all node gains. They are dimensionless simulated material, not hardware energy.

For edge i→j, biomass z, activity association a (mean absolute pre/post product),
and local store p_j:

- Proposed deposition d_ij = g (b + a_ij) (1 − z_ij) M_ij.
- Available deposition fraction f_j = min(1, p_j / mean-incoming(d_ij)).
- z'_ij = (1 − decay) z_ij + f_j d_ij.
- p'_j = p_j + accepted collection − mean-incoming(f_j d_ij).

Thus idle material can shrink; growth needs local material; the deposit ledger
includes discarded overflow. Each edge's material unit is normalized by its
target's number of possible incoming edges. A finite basal growth term supplies
an inherited scaffold. Activity itself does NOT measure causal usefulness.
Material is delivered directly to each recipient neuron; no spatial transport,
membrane, learned routing or organism-produced optimizer is implemented.

## Learning and developmental histories

All variants start from exactly the same parameters and biomass for each seed.
History A: the cue enters the A sensory bank for 2,000 trials. History B: the same
cue enters B. These are paired counterfactual histories, not independent seeds.
Both then receive the same 2,000 trials with the cue entering both banks. Routing
is externally imposed developmental experience, not spontaneous specialization.
Resource chemistry and availability never change during this development.

One global Adam optimizer trains both functions jointly from replay. Resource
Q targets maximize explicit net energy production with gamma 0.90. Recall uses
an explicit success-conditioned auxiliary loss. Developmental gate attempts
are epsilon-greedy (30% uniform); the inverse logged action probability corrects
the successful-attempt gradient. Failed attempts provide zero recall gradient.
No correct-answer label enters the neural inputs or learning target; attempted
action and scalar success are sufficient for this small binary task. There is
no material-collection bonus. This remains ordinary externally specified
learning, not motivation from nothing or locally reconstructed learning rules.

Training supplies energy at trial 0, every 128 trials and after depletion.
Each supply is logged; material and biomass persist and receive no such reset.
Replay marks periodic energy boundaries terminal. Evaluation receives a single
starting energy budget, no learning, no exploration and no energy top-ups.
Biomass renewal continues. Evaluation resets stores and energy to standardized
values while retaining developed biomass. These are finite-state assays, not
uninterrupted artificial lifetimes. Per-trial neural activation resets; weights,
edge biomass and material stores carry history across trials.

## Controls and branches

- plastic: local pre/post activity guides material renewal.
- static: ordinary recurrent learner with the identical initial fixed biomass
  target and chemistry; replaces wear but does not develop a new target.
- shuffled: permutes activity across valid incoming edges within each target;
  breaks the particular association-edge match. Each column's activity sum is
  preserved; actual deposition costs can differ because masses subsequently
  differ. It is not an exact material/compute-matched control.

The static learner has the same trainable parameter count, observations,
learning rules, initial biomass and planned transitions. Actual material cost,
structural trajectories, realized active training and wall time are reported;
there is no claim of equal physical compute or universal architectural fairness.

From each developed checkpoint, clone weights, optimizer, target, replay,
stores and biomass. Each branch gets 1,800 learning trials:

1. normal: continued original dependency.
2. rescue: external deposition meets actual demand; inventory is not charged.
3. sham: both collected materials are ineffective, with unchanged observations.
4. lost: memory-gate food disappears and visible direct-food yield becomes
   sufficient (0.30). This is a changed opportunity, not a hidden usefulness test.
5. swap: the A and B resource actions secretly exchange delivery chemistry.
6. frozen_weights: normal environment, no parameter updates; local biomass
   dynamics and the same exploration protocol continue.

Evaluate both acute and learned branches, plus entire-tissue and each chemical
bank lesion. All modes share pre-drawn random cues/noise/action streams. Frozen
weights can change behavior as internal state changes, so a changed collection
rate alone cannot establish learning. Whole-bank lesions also affect the
resource controller; they are not isolated memory-route lesions.

## Sample, measurements and frozen decision rules

16 independent initial seeds, 200–215; paired A/B histories; three variants.
Each evaluation: six common held-out worlds × 240 planned trials. Training seed
families are disjoint from evaluation seeds 80,000,000–80,000,005. Evaluation
includes fresh random realizations of a binary task, not novel concepts.
No filtering of failed seeds or selective survival denominators.

Report correct recalls, collection and active duration per planned trial,
active-only collection, completion, resource deposition and biomass. Average
worlds and histories within seed for architecture contrasts. For history effects,
first calculate within-seed differences between paired histories. Use 10,000
seed bootstrap resamples, descriptive 95% percentile intervals. They condition
on the common world panel, have no multiplicity correction and no power claim.

Frozen gates (conjunctive, not individually promoted discoveries):

- Functional development: plastic developed recall per planned trial ≥ 0.85,
  active fraction ≥ 0.90, and learned minus initial recall lower CI > 0.
- Selective value of local development: plastic minus static AND plastic minus
  shuffled developed recall ≥ 0.05, each lower paired CI > 0.
- History-specific priority: D = [(A−B collection)_historyA −
  (A−B collection)_historyB]/2 ≥ 0.02, lower CI > 0.
- History-specific functional dependence: L = [(recall_lesionB −
  recall_lesionA)_historyA − (recall_lesionB − recall_lesionA)_historyB]/2
  ≥ 0.05, lower CI > 0. Both D and L must pass to support H2.
- Viable relinquishment: lost branch active fraction ≥ 0.90, material collection
  ≤ 0.05 of planned trials, and normal minus lost collection lower CI > 0.
- Recovery from chemistry swap: adapted minus acute recall ≥ 0.10, lower CI > 0.
  Report failure if acute performance is already too high to pass this gate.

Rescue and sham results are diagnostic, not additional gates. Reduced collection
in a dying sham agent is not evidence of intelligent relinquishment. The all-zero
output tie is resolved with the pre-drawn random action, avoiding an artificial
forage-default advantage after complete lesions. Failed planned trials remain
zero in unconditional recall and collection; completion is always reported.

## Interpretation boundary

Positive outcomes support functional, history-sensitive resource dependence.
If static or shuffled controls perform as well, do not attribute success to
local structural plasticity. No result here tests consciousness, phenomenal
craving, full autopoiesis, a produced boundary, or neural reconstruction of the
learning machinery. Novelty remains unestablished. LNDP and neural homeostatic
work are close prior art; E2 is an intervention benchmark and partial substrate
advance, not a claim to have invented organismal autonomy.
