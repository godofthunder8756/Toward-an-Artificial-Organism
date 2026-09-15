# AC1: acquired controller maintenance

Date: 2026-09-14. New standalone engineering study. This does not amend or
execute the stopped E3 v0.11 experiment. No full-autopoiesis or novelty claim.

## Research finding and change in question

The project has often asked whether an organism-inspired allocator beats a
conventional method. That tests algorithmic advantage, not by itself whether
the allocator maintains its own acquired organization. A conventional mechanism
can be the constructive witness for the latter property. We should measure
causal dependence first, and keep novelty and broader autonomy as separate gates.

### Primary literature inspected in this session

| Source | Access and relevant result | Design consequence (our inference) |
| --- | --- | --- |
| [Montévil & Mossio, 2015](https://montevil.org/publications/articles/2015-mm-organisation-closure-constraints/) | Author-hosted full text, especially sections 3–5: constraints are conserved over their operating timescale and maintained through dependence on other constraints over longer scales. | Identify actual maintained mechanisms, their timescales and intervention-sensitive dependencies. Circular arrows or a survival score are insufficient. |
| [Villalobos & Dewhurst, 2017/2018](https://link.springer.com/article/10.1007/s11229-017-1386-z) | Publisher full text, especially section 7: considers computational systems whose continuing operation depends on enabling conditions sustained through their computations. This is a conceptual argument, not an experimental proof. | A conventional computational implementation is not disqualified merely for being conventional. Test removal of enabling relations while preserving environmental supplies. |
| [Di Paolo, 2005](https://ezequieldipaolo.net/wp-content/uploads/2011/10/autopoiesis_teleology_2005.pdf) | Author-hosted paper: distinguishes autopoiesis and adaptivity. | Maintenance, adaptive regulation and a self-produced individual boundary need separate evidence. |
| [Growing Neural Cellular Automata, 2020](https://distill.pub/2020/growing-ca/) | Author article: cells regenerate patterns using trained update weights; its hardware discussion places the genome and control in ROM. | Damaging cell state while preserving target-specific update weights does not close our particular acquired-controller loophole. |
| [Neural Network Quine, 2018](https://arxiv.org/abs/1803.05859) | Abstract inspected: trains networks to output their own weights, including auxiliary-task variants. | Weight reproduction is prior art. Our discriminator must include vulnerability, ongoing resource payment, acquired information and causal interventions. |
| [Functional Error Correction for Robust Neural Networks, 2020](https://arxiv.org/abs/2001.03814) | Abstract inspected: error protection can optimize network performance rather than only bit error rates. | Error correction of a controller is a competent conventional construction, not automatically a novel algorithm. |

This is a targeted review, not an exhaustive novelty search. A search also found
“Experimental probes of autopoietic self-maintenance” (2026), but the publisher
page failed to open; it is not used as evidential support here. No absence-of-prior-
art claim follows. The proposed implementation below is ours, not attributed to
these papers.

## Exact engineering claim

After supervised acquisition, a finite controller can retain its own acquired
decision table under continuing information corruption by choosing and paying
for repairs to the same storage from which it computes its maintenance actions.
Disabling writes to that controller storage should impair later decisions and
viability; an explicitly protected controller is a rescue control.

Strongest simpler explanation: a demonstrated truth-table policy plus ordinary
repetition coding and scrubbing. That explanation is accepted. The intended
advance is moving the acquired policy inside the vulnerability/maintenance loop.
It does not establish learned goals, a new learning rule, a self-produced
interpreter, metabolism, membrane, or full organismal autonomy.

## Why this construction

Three candidate routes were considered:

1. Self-reproducing neural weights: interesting, but a weight-generation loss
   and protected generative parameters risk relocating the same template.
2. A self-producing spatial reaction network with learned catalysts and a
   produced boundary: closer to material autopoiesis, but adds several untested
   mechanisms simultaneously. It remains the stronger subsequent target.
3. A vulnerable acquired controller that pays to repair its own decision bits:
   chosen as the smallest direct test of the missing acquired-policy link.

A positive AC1 result must not be relabelled completion of route 2.

## Complete causal and information inventory

The live body contains four banks of repeated bits. Banks 0–1 store the acquired
controller; banks 2–3 store arbitrary acquired payload bits. Each controller row
holds a three-bit action. There are 64 observation rows (192 controller bits),
split evenly across the two controller banks. Each payload bank also holds 96
bits. Each bit has seven replicas. Total vulnerable trace storage is 2,688 bits.

Observations consist of low-energy and low-material flags plus one damage flag
for each bank. A bank's damage flag means at least four minority copies, summed
over its 96 code bits. This is observable copy disagreement, not target error.
All sensing, addressing, majority decoding and execution are protected generic
physics. They contain no individual-specific policy or payload templates.

Actions 0 and 1 collect energy and precursor; actions 2–5 scrub a selected bank.
Codes 6–7 do nothing. A generic scrub writes at most 32 minority copies toward
their currently decoded majority, using one precursor and one energy unit per
bit. It cannot consult the originally learned value. It may reinforce an error.
One energy unit pays living/decision cost each tick. The full repair price and
finite reservoir ceilings will be explicit configuration fields.

Supervised acquisition presents every observation/action demonstration once in
a randomized order. The demonstrated controller collects resources when low,
otherwise services flagged banks with a lifetime-specific demonstrated tie
priority; when none are flagged it rests. This is direct tabular learning from
demonstrations, not autonomous discovery of needs or online reinforcement learning.
No update from rewards/examples occurs after acquisition. Independent random
payloads make information-loss tests meaningful. The teacher and evaluator's
targets never enter the live decision/repair function.

The only persistent live quantities outside traces are bounded energy/material
reservoirs and termination. They contain no decoded policy cache. Clock, injected
noise and observer counters are external. Temporary decoded data exists only
within an operation; it is recomputed from current traces next tick. There is
no recurrent hidden state, optimizer, replay or learned host array in the body.

All random damage is generated from a separate exogenous stream and supplied
equally to each paired arm even when it terminates. Repair is deterministic for
a supplied body; it never draws from the environment generator. The observer
alone holds the original targets and scores snapshots. Reservoirs can convey
action consequences, so complete-erasure noninterference explicitly resets them
too and uses identical future inputs and physics.

## Arms and interventions

| Arm | Purpose |
| --- | --- |
| self | Vulnerable acquired policy chooses all its own collection/repair actions |
| no_policy_write | Same policy, corruption and costs; controller-bank writes are sham, payload repairs remain effective |
| no_write | All repair writes are sham, with their attempted costs paid |
| protected | Explicit protected acquired-policy copy drives actions; all body traces still decay and are repairable |
| fixed | Protected generic maintenance rule, using canonical bank priority; a strong ordinary reference, not a target-information-free organism |
| random | Protected uniform random action source with paired exogenous action stream |
| policy_scramble | Controller bits independently randomized at release; healthy reservoirs and original payload retained |
| resource_rescue | Vulnerable policy with reservoirs externally topped up each tick; separates resource shortage from controller-bit restoration |

Paired damage challenges: no pulse, and a partial pulse that flips two distinct
replicas of every bit at tick 200. It is below majority threshold only when the
pre-pulse bit was clean; accumulated damage can make some bits unrecoverable.
The exact clean-state repair property is separately tested exhaustively.

Complete-information loss is a separate negative assay: set every trace and
reservoir to identical canonical values in two differently acquired individuals,
then apply identical future inputs. Entire states and action traces must agree
exactly. Payload accuracy is measured against balanced counterfactual truth
tables, so aggregate chance is exact by construction, not a nonsignificant test.

## Engineering plan fixed before first run

Use seeds 0–7 for initial feasibility. Run 3,000 ticks at per-copy flip rates
0.0005, 0.001 and 0.002; both pulse conditions; all eight arms. Starting reservoirs
are 64 energy and 128 precursor. Collection adds 32 energy or 64 precursor, with
ceilings 128 and 256. Low flags use energy <=48 and precursor <=64. All constants
are engineering choices; no biological interpretation of their units.

Report every configuration and arm, including failures. Endpoints are active
ticks / planned ticks, all-64-row controller accuracy and payload accuracy at
the end (also report function multiplied by survival), repair spending and
trace replacement counts. Dead individuals receive zero functional endpoints,
while their raw final information accuracy is separately retained. A new
confirmatory study would need independent review and a separate source freeze.

Engineering support criteria (not a confirmatory statistical declaration):

- at least one tested environment supports >=0.90 mean planned activity in self;
- self minus no_policy_write mean planned activity >=0.20 there;
- protected control mean planned activity >=0.90 there;
- controller-bit turnover is positive, with every bank receiving paid writes;
- all integrity, truth-blindness, complete-erasure and resource-ledger tests pass.

All differences use paired seeds; intervals are descriptive 95% percentile
bootstrap over eight seeds, 10,000 resamples, seed 20260914. Report all 6
configurations; do not treat selection of a successful configuration as independent
confirmation. Revisions must have their changes and reasons appended before
new runs, preserve original data, and stay labelled engineering.

## Failure interpretation and claim boundaries

If self fails but protected works, the vulnerable policy/repair loop is not
robust under that configuration. If neither works, investigate feasibility.
If self and no_policy_write both thrive, those settings do not establish a need
to preserve the controller over the tested horizon. A positive effect here is
not evidence of an adaptive advantage over fixed; fixed is a competent comparator.

Autopoietic merit is a checklist, not a single victory word:

- acquired policy physically represented and causally used: tested;
- policy information maintained through its own paid actions: tested;
- sustained dependence, intervention and recovery from surviving information: tested;
- maintenance goals acquired without demonstration: NOT tested;
- decision/execution machinery materially produced: NOT implemented;
- boundary produced and maintained by its internal processes: NOT implemented;
- autonomous development or subjective experience: NOT established.

The next stronger gate, conditional on an informative AC1 result, is a
self-produced executor/actuator and boundary with measured mutual dependencies.
It must preserve the acquired-policy tests and add physical causal interventions,
not add a membrane variable with an arbitrary death threshold and call that proof.
