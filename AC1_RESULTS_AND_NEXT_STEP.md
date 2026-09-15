# AC1: an acquired controller maintaining its own decision information

14 September 2026. **Positive bounded engineering result; full autonomy and
autopoiesis remain unestablished.**

## What changed

We implemented a controller whose acquired decision table is itself stored in
the damaged, resource-maintained body. The controller chooses collection and
repair actions by reading that current table. Those actions preserve the bits
that determine its later maintenance decisions. No protected learned-policy copy
drives the self-maintaining arm.

This directly addresses one architectural limitation of E2 and the E3 side
branch. It is a conventional construction: tabular acquisition from demonstrations,
seven-copy repetition coding and paid majority scrubbing. We are not claiming
algorithmic novelty, a superior allocator, or a complete artificial organism.

The useful change in research strategy is to separate two claims:

1. **Does acquired decision information participate in its own maintenance loop?**
   AC1 gives a constructive, intervention-tested example within this simulator.
2. **Does that system generate its own needs and produce its enabling machinery
   and boundary?** AC1 does not establish this. AC2 specifies the stronger target.

The primary literature supports examining enabling dependencies and their
maintenance across timescales; applying those ideas to this particular program
is our model-relative interpretation, not a verdict supplied by the literature.
See [Montévil and Mossio](https://montevil.org/publications/articles/2015-mm-organisation-closure-constraints/)
and [Villalobos and Dewhurst](https://link.springer.com/article/10.1007/s11229-017-1386-z).

## Construction and acquisition

- Four banks hold 96 binary values each, with seven replicas per value.
- The first two banks encode a 64-row policy with three-bit actions.
- The other two hold 192 arbitrary acquired payload bits.
- The 64 observations encode low energy, low precursor and four damage flags.
- The policy selects food, precursor, repair of a particular bank, or rest.
- Repair copies surviving majority information, paying one energy and one
  precursor per attempted bit. Living/decision cost is one energy per tick.
- Corruption can change the controller's choices; its repair actions can change
  the storage from which it subsequently chooses.

The policy is acquired by memorizing one demonstration for every observation.
Its demonstrated bank-priority order varies between developmental histories.
Most priorities, including collection thresholds, are supplied by the teacher.
This is supervised acquisition, not discovery of dependencies. The policy
family contains only 24 possible priority permutations: at most about 4.585 bits
of history-specific variation, despite 192 bits of nominal table storage.

The trace state has 2,688 logical binary storage sites. NumPy implements these
as 2,688 bytes; Python overhead and temporary arrays are additional host memory.
The simulated resource prices are not hardware energy measurements. Bounded
energy/material reservoirs and termination also persist. Temporary decoding is
recomputed from live traces; no teacher, target array, replay buffer, optimizer
or policy cache is in the live body. The observer holds targets only for scoring.

Protected generic sensing, majority decoding, execution, addressing, world laws
and write actuation remain. These are explicit limitations for broader closure,
not covert individual-specific templates. This is a trusted in-process model,
not a separately sandboxed experimental worker.

## First engineering run: all declared environments retained

The protocol and source snapshot preceded the run. Eight seeds (0–7), six
environments, eight arms and 3,000 planned ticks produced 384 rows. Each arm for
a seed received the same exogenous corruption. Rates below are per copy per tick.
A pulse flips two distinct replica positions per bit at tick 200 in addition
to background corruption; pre-existing damage can make the combined event
unrecoverable.

**Mean active fraction of the planned horizon:**

| Flip rate | Pulse | Self | No controller writes | No writes | Protected policy | Fixed policy | Random | Scrambled policy | Resource rescue |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0005 | No | 1.000 | 0.494 | 0.524 | 1.000 | 1.000 | 0.711 | 0.016 | 1.000 |
| 0.0005 | Yes | 0.929 | 0.317 | 0.317 | 1.000 | 1.000 | 0.063 | 0.016 | 1.000 |
| 0.001 | No | 1.000 | 0.187 | 0.199 | 1.000 | 1.000 | 0.056 | 0.013 | 1.000 |
| 0.001 | Yes | 0.689 | 0.111 | 0.112 | 1.000 | 1.000 | 0.044 | 0.013 | 1.000 |
| 0.002 | No | 1.000 | 0.092 | 0.088 | 1.000 | 1.000 | 0.011 | 0.012 | 1.000 |
| 0.002 | Yes | 0.431 | 0.063 | 0.063 | 1.000 | 1.000 | 0.011 | 0.012 | 1.000 |

Four environments passed the original aggregate engineering criteria. The two
stronger pulse environments failed the self-activity criterion. Even the lowest
pulse condition lost one of eight individuals. These failures are preserved.

At p=0.001 without the pulse, every self-maintaining controller finished with
100% correct policy rows and payload bits. Each performed roughly 2,000 paid
bit writes to each bank over the horizon, including both controller banks.
Thus persistence was accompanied by extensive replacement, not just survival
of untouched initial storage. The canonical fixed protected policy also
performed perfectly; no adaptive superiority is claimed.

Resource rescue is explicitly external support. It can keep execution active
while acquired information degrades: in the p=0.001 pulse condition its mean
final policy accuracy was 79.5%, despite 100% activity. Survival alone remains
an inadequate information-maintenance metric.

## Follow-up: remove the wasted-cost explanation

The first controller-write ablation pays for ineffective writes. To challenge
the possibility that futile spending alone explained failure, a separately
documented follow-up made those controller-bank attempts free. The original
model and data were preserved.

The follow-up used 32 new seeds (1000–1031), all six environments, and four arms:
self, paid controller ablation, free controller ablation and protected policy.
No physical parameter was tuned. Its 768 rows are exploratory validation, not
an independently reviewed confirmatory experiment.

| Rate | Pulse | Self activity | Free-ablation activity | Paired difference [descriptive 95% interval] | Self completion |
| --- | --- | ---: | ---: | --- | ---: |
| 0.0005 | No | 1.000 | 0.435 | +0.565 [0.494, 0.634] | 32/32 |
| 0.0005 | Yes | 1.000 | 0.222 | +0.778 [0.725, 0.824] | 32/32 |
| 0.001 | No | 1.000 | 0.246 | +0.754 [0.718, 0.791] | 32/32 |
| 0.001 | Yes | 0.810 | 0.144 | +0.666 [0.545, 0.777] | 22/32 |
| 0.002 | No | 0.938 | 0.132 | +0.806 [0.725, 0.867] | 27/32 |
| 0.002 | Yes | 0.286 | 0.091 | +0.196 [0.092, 0.312] | 5/32 |

The protected-policy arm completed 32/32 in every environment. The free-ablation
arm completed 0/32 in every environment. The ablation advantage in resources
therefore does not remove the dependence on controller-information repair.

At the middle rate without a pulse, self retained 100% policy and payload
accuracy; the free-ablation arm's raw policy accuracy averaged 45.3% at its final
state. Dead individuals receive zero in the separate functional endpoints, so
raw retained information is not confused with continuing useful operation.

The follow-up also exposes the limit of the original eight-seed result:
five of 32 individuals failed at the highest rate even without the pulse.
Strong combined damage is a genuine vulnerability. Majority copying cannot
reconstruct the original value after the surviving majority has become wrong.

Intervals resample independent seeds within each environment (10,000 bootstrap
draws). They are descriptive and uncorrected across the six settings; they
are not six separately confirmed discoveries. Repeated environments and arms
do not turn 40 total developmental seeds into 1,152 independent individuals.

## Mechanism and integrity checks

[The audit](AC1_AUDIT_v1.json) passes:

- all original and follow-up source snapshot hashes;
- all 1,152 expected rows, unique seed/arm coverage and recorded environment pairing;
- resource ledgers, finite reservoir bounds and write counts for every row;
- recomputed arm means and all saved bootstrap contrasts;
- 24 exact sampled reruns (first seed of each study, all environments, self and
  the relevant controller ablation), including action/final-state digests;
- eight mechanism tests, including every seven-bit pattern for majority repair;
- a direct policy intervention changing a food decision to rest;
- forbidden external action override in the self arm;
- equal reset state and equal future inputs producing exactly equal trajectories
  after different acquisition histories;
- exact 50% payload accuracy across complementary counterfactual target tables
  after complete erasure; this is a noninterference check, not a recovery claim;
- reservoir restoration alone leaving erased trace information unchanged;
- refund equivalence and conservation in the favorable ablation control.

These checks establish behavior of this code and the integrity of these stored
runs. They do not replace independent scientific review or a physical experiment.

## What this earns—and what the next step must add

**Earned claim:** in this finite simulated system, acquired controller information
is causally used to make maintenance decisions and is itself preserved by those
paid decisions. Disabling that maintenance breaks sustained operation, even when
the disabled repairs are free. Recovery/preservation uses surviving redundancy.

This is a direct constructive witness for the specific acquired-policy
self-maintenance property that was missing from the prior implemented agents.
It gives the autonomy program a firmer starting point. It does not establish
full organizational closure under every relevant definition.

**Not earned:** spontaneous needs, continuous autonomous development, production
of its own decoder/actuator, a self-produced physical boundary, algorithmic
novelty, full autopoiesis, or subjective experience. Those are substantive remaining
questions. The simplicity of supervised acquisition also limits generalization
to a developing neural organism.

The next proposed architecture makes **write/assembly catalysts, energy-conversion
catalysts and a spatial boundary** produced constituents, with the vulnerable
controller allocating their production. Their actual production and retention
must sustain controller repair in turn. Each proposed dependency needs a causal
intervention and a resource ledger. [AC2 design direction](AC2_DESIGN_DIRECTION_v0_1.md)
spells out that work and its falsification tests; it is not implemented evidence.

## Reproduction and files

Run from the repository with an installed NumPy environment:

```powershell
py -3.12-arm64 -B -m unittest -v test_ac1
py -3.12-arm64 -B ac1.py --out new_ac1_engineering
py -3.12-arm64 -B ac1_followup.py --out new_ac1_followup
```

Runners refuse an existing output directory. Python 3.12.10 ARM64 and NumPy 2.3.5
were used. Recorded model-run times were about 25 and 57 seconds respectively;
these are host observations, not performance guarantees. `audit_ac1.py` reads
the retained original output directories and refuses to overwrite its audit.

| Artifact | Purpose |
| --- | --- |
| [Research and original protocol](AC1_RESEARCH_AND_PROTOCOL_v1.md) | Literature, hypothesis, inventory, arms and pre-run engineering criteria |
| [Original snapshot](AC1_ENGINEERING_FREEZE_v1.json) | Original model/test/protocol hashes |
| [Model](ac1.py) and [tests](test_ac1.py) | Minimal implementation and mechanism tests |
| [Original data](ac1_results_v1/results.json) | All 384 initial rows, periodic snapshots, ledgers and contrasts |
| [Follow-up protocol](AC1_FOLLOWUP_PROTOCOL_v1.md) | Prospectively specified cost-refund diagnostic on new seeds |
| [Follow-up runner](ac1_followup.py) and [snapshot](ac1_followup_results_v1/pre_run_snapshot.json) | Favorable ablation implementation and pre-run source hashes |
| [Follow-up data](ac1_followup_results_v1/results.json) | All 768 validation rows and comparisons |
| [Audit code](audit_ac1.py) and [audit](AC1_AUDIT_v1.json) | Integrity, numerical recomputation and exact sampled replay |

Existing E0–E3 sources, protocols, freezes and raw results were not changed.
