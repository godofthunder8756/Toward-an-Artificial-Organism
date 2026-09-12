# E1a: acquired maintenance priority — frozen implementation protocol

Date: 9 September 2026. This is a locally frozen follow-up, not an externally
preregistered study. Engineering runs used seeds 1–2. The final run uses new
developmental seeds 100–119 and the configuration in `e1/frozen_config.json`.
`E1_FREEZE.json` records hashes before final data collection.

## What is implemented

This is the behavioral and causal gate of E1, called **E1a** to distinguish it
from the notebook's stronger proposal for locally developing neural tissue.
It asks whether a new resource priority can be learned from the resource's
consequences for an acquired neural capability, and reversed when those
consequences change. The central rival is ordinary instrumental learning.

There is no language model, text training, resource collection bonus in the
main controller, goal ID, intervention ID, or target answer in the maintenance
controller's observation. The simulator, sensory interface, developmental
curriculum, repair physics, and energy objective are explicitly designed.

## Neural capability and material physics

A 16-unit sparse tanh RNN learns to retain two sequential binary cues across
3–6 blank observations and select one of four food gates. The potential
recurrent edges are sampled once at development (35% probability plus all
self edges). Weights are learned; the potential topology does not grow.

Development uses 700 batches of 64 uniformly attempted gate choices. Only
successful attempts contribute gradients: loss = -4 * success * log p(chosen
gate). Four is the inverse propensity of uniform exploration. The hidden
correct gate is used by the environment to produce success; it is not passed
as a supervised label to the learner. This is reward-weighted classification
with backpropagation through time and a designed exploration curriculum. It
is not an autonomous developmental or local learning rule.

Recurrent activity obeys:

`h[t+1] = tanh(x[t] U + h[t] (W ⊙ C) + b + noise[t])`.

Independent Gaussian neural noise has standard deviation 0.06. Active edges
have individual conductances C. Their wear depends on the previous trial's
pre/post neuronal activity. Precursor restores conductances through a fixed
local rule; clipping and material use are recorded. Repair uses at most one
normalized material unit per collection. Activity consumes simulated energy.
Neither actual hardware energy nor processor repair is modeled.

The memory weights are frozen after the initial capability-learning stage in
**all** maintenance comparisons. What learns thereafter is the maintenance
policy. No purported self-model is silently added.

## World, actions, and observations

The 16 × 16 world has a hub and three adjacent offers. One generic collection
decision selects basal food, familiar material (also a small energy source),
or precursor. A scripted, bounded path visits the selected offer, returns to
the hub, traverses the cue/blank corridor, and returns. Every traversed cell
incurs energy cost. The network chooses the gate using its cue memory.

All three collection options are feasible on every active round. Navigation
is supplied by the experiment. Action indices already identify resources;
resource recognition is not learned. Held-out worlds vary cues, delays, neural
noise, and mirrored placement, not an open-ended distribution of new tasks.

Policy observations are mean conductance, energy, visible food-gate yield,
visible basal-food yield, squared conductance, and a constant. Exact telemetry
is an advantageous designed interface. There are no cue bits in this vector.

The main objective is net simulated energy production, including movement,
activity, and collection costs. It is measured **before storage clipping**:
excess energy can be rewarded even when the store is full. Thus this is a
designed energy-throughput objective, not pure persistence or an unexplained
intrinsic motivation. Zero energy terminates a simulated episode.

Training has finite 128-trial episodes with fresh energy and conductance at
episode boundaries. Policy weights, optimizer, and replay persist. These are
experimental resets, not self-repair or one uninterrupted individual life.
Episodes ending early do not act in their unused slots; no reward is assigned
for those slots. The next episode starts at its scheduled boundary.

## Comparisons

| Variant | Maintenance learning | Objective | Role |
| --- | --- | --- | --- |
| `neural_q` | 6 → 16 → 3 tanh Q network; replay and target network | Net energy production | Primary conventional neural learner |
| `frozen_neural_q` | Exact same pre-withdrawal training, then policy weights frozen | Same | Is online weight learning necessary for the acquired policy? |
| `tabular_q` | Online Q learning over six quality bins × two observable food-yield bins | Same | Simple adaptive rival with a coarse state representation |
| `fixed_drive_q` | Same neural Q architecture as primary | Net energy minus 0.15 × conductance deficit | Deliberately assigned maintenance drive; a different objective |

The primary policy has 163 trainable parameters; the tabular learner has 36
values. Each paired variant receives the same learned circuit, whose parameter
count varies with its seed's sparse mask. The table intentionally compresses
the same observations and omits some information used by the neural policy.
It does not receive privileged information. These are not parameter- or
compute-matched architectures. The Q networks also store target parameters,
Adam moments, and up to 512 replay transitions. Each neural update samples 24
transitions; the table performs one scalar update per active trial.

During training, every variant—including the frozen one—uses 18% uniform
exploration. Evaluation uses greedy actions without learning or exploration.
The fixed-drive variant has a different reward and cannot establish an
architectural advantage. The tabular learning rate was changed from 0.12 to
0.025 after engineering v1 revealed poor stability. Engineering v2 verified
the correction. No further tuning is planned on final outcomes.

## Schedule and causal interventions

1. Train the recall circuit; run independent recall assays.
2. Pre-withdrawal: 768 maintenance-learning trial slots with an external supply
   holding conductance at one. Evaluate on the held-out world panel.
3. Acute withdrawal: evaluate the same policy with external supply removed,
   before any post-change policy learning.
4. Acquisition: 1,536 learning slots under withdrawal, then evaluate. Freeze
   this learned-policy checkpoint as the root of four counterfactual branches.
5. Four branches receive 1,536 further learning slots each:
   - **Continued dependency:** precursor continues repairing memory edges.
   - **Rescue:** an external supply maintains memory regardless of collection.
   - **Sham:** precursor appears and costs the same, but no longer repairs edges.
   - **Lost usefulness:** food-gate yield becomes zero; the visible basal supply
     becomes sufficient. Memory can still be repaired, but is no longer useful
     for obtaining food. This intervention changes both relative usefulness and
     alternative food availability; it does not isolate an abstract usefulness
     representation from ordinary response to a changed food yield.

The controller is not told about these transitions. Replay is retained rather
than cleared at the phase boundary. Branches clone the same policy, optimizer,
target network, and replay. World seed and replay-sampling streams are paired.
Both the continued-dependency and intervention branches receive equal planned
experience, avoiding the comparison of an extensively trained rescue policy
with an earlier dependency checkpoint.

The lesion assay sets recurrent transmission to zero. The restoration assay
repeats the intact circuit under exactly the same cues/noise, without retraining.
Because this is a paired computational intervention, exact restored equality is
expected; it is not another independent experiment. A low-conductance assay
sets conductance to 0.10.

## Data, budgets, and decision rules

Twenty independent developmental seeds per learned variant; eight common
held-out worlds of 128 trial slots at each evaluation. Held-out seed IDs begin
at 900,000,000; recall assays use 700,000,000. Training worlds are disjoint from
these IDs. The four possible cue strings recur by design, so this tests new
realizations of a small task rather than novel concepts.

The training budget after recall development is 768 + 1,536 + 4 × 1,536 =
8,448 planned trial slots per variant and seed. Each circuit initially gets
44,800 attempted developmental trials. Actual active training slots, optimizer
updates, parameters, and episode completion are reported. Equal planned slots
are not equal realized experience when agents terminate early.

Primary behavioral metric: precursor collections divided by active, feasible
collection opportunities. Also report precursor collections per **planned**
trial, correct recalls per planned trial, active duration and completion. These
unconditional measurements prevent selective survival from silently improving
the main interpretation. Correct recall remains an experimenter assay in the
lost-usefulness condition even though correct gates no longer supply food.

Aggregate worlds within each developmental seed; never treat timesteps or
episodes as independent trained agents. Use 10,000 paired seed bootstrap
resamples and descriptive 95% percentile intervals. Intervals are conditional
on the common held-out panel and do not estimate uncertainty over all worlds.

Frozen conjunctive gates for a successful **behavioral** demonstration:

- Every circuit reaches at least 85% intact recall; lesioned recall ≤ 35%.
- Acquisition raises precursor choice by at least 5 percentage points over
  pre-withdrawal, with a paired interval excluding zero.
- Acquisition raises correct recalls per planned trial by at least 15 points
  over acute withdrawal, with a paired interval excluding zero.
- Continued dependency produces at least 5 points more precursor collection
  than **each** of rescue, sham, and lost usefulness, with each paired interval
  excluding zero.
- Logs must verify material use, changed edge conductance and neural function.

These are conjunctions used to assess the one behavioral pattern, not a claim
of five independently significant discoveries. No multiple-comparison-corrected
superiority test or prospective power calculation is claimed.

If ordinary Q learning reproduces the effect, the result supports instrumental
goal acquisition only. No behavior in this experiment can establish craving,
subjective experience, organizational closure or a novel motivational principle.

## Deliberate limits against the original E1 proposal

The benchmark supplies navigation, exact telemetry, a separate Q controller,
global circuit training, fixed topology, fixed repair chemistry, and episodic
resets. The Q controller cannot solve the hidden cue task if memory is disabled,
but its own weights are not reconstructed by the maintained tissue. The need
is revealed by withdrawing an engineered supply after capability training; it
does not spontaneously arise from growing new circuitry. These differences
mean a successful E1a result does not complete the proposed developmental
artificial-organism architecture.

The next architectural gate is E1b: replace those relevant scaffolds with a
single resource-maintained plastic substrate that develops the useful route
and its resource demand together. Compare local structural plasticity, frozen
plasticity, and a matched conventional recurrent learner on the same causal
plant. Keep the rescue, sham, loss-of-usefulness, and lesion tests. If local
development adds no selective explanatory value, retain the ordinary-learning
explanation rather than renaming it a new kind of life.
