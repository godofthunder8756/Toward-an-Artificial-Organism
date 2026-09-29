---
description: Audited bounded Phase III-B verdict and reduction analysis
ms.date: 2026-09-29
---

# Phase III-B verdict v1

## Outcome: B, bounded negative

The structured candidate **failed** the frozen primary gate against the
within-seed best of all six independently trained rivals. One of 16
independent final model seeds exceeded the strict 0.02 meaningful-effect
threshold; **14** were required. There were 15 strict losses and no ties.
The exact two-sided sign-test returned `17/32768 = 0.000518798828125`,
but that small p-value reflects the predominantly **opposite** direction.
It does not rescue the required `14/16` improvement. The mean paired
best-rival-minus-candidate difference was **-0.062363** joint-loss units
(median **-0.076904**). Episodes and contexts were repeated measures;
only the 16 independently initialized model seeds count as replicates.

This is a valid negative result for the **declared finite
training/resource regime**, not a proof that workspaces cannot help
elsewhere. The simplest winning primary family on mean held-out loss
was the independently trained **R9 unrestricted eight-symbol code**.
Outcome B is the primary taxonomy label. R4's cheaper fixed-selector
workspace also performed slightly better than the candidate on mean
loss, but this is descriptive, not an equivalence test. Do not call a
candidate-only lesion a rival-exclusive advantage or promote R9's
constructive candidate copy into an independently trained win.

The immutable [final manifest](phase3b_results_v1/finals/manifest.json)
has SHA-256
`5ba90ee9e6f2d734b0ab2eadf9906edea30b52c66e24cf093dd802cd0b4091a9`.
The [independent raw/checkpoint audit](phase3b_results_v1/phase3b_final_audit_v1.json)
has SHA-256
`c94a5e7953f050c4a2596d259b38a7ef6953d97233518a6803f4352b624e3f27`.
It passed source/freeze/approval checks, engineering-selection replay,
all 112 raw files and checkpoint replays, R4 route validation,
loss reconstruction, and R9 clone checks. Its `gate.pass=false`
is **scientific falsification**, not audit invalidity.

## Exact comparison and resource scope

All families used 16 untouched final seeds `1000..1015`, 8,192
training episodes and 256 AdamW updates per seed, and the same
4,096-episode held-out stream `20000 + seed`. Engineering selected
configurations from seeds `0..3`, training contexts `0..2` only.
The binding whole-arm caps were 4,096 trainable parameters and
80,000 declared linear forward MACs per complete episode.

| Family | Selected width / learning rate | Mean held-out joint loss | Candidate minus rival | Params | Forward MACs/episode |
| --- | --- | ---: | ---: | ---: | ---: |
| Candidate | 27 / 0.001 | 0.369509 | -- | 3,906 | 8,420 |
| R1 unlimited learned broadcast | 27 / 0.001 | 0.388547 | -0.019038 | 3,930 | 9,212 |
| R2 monolithic recurrence | 57 / 0.001 | 0.365608 | +0.003902 | 4,032 | 30,008 |
| R3 private specialists | 32 / 0.001 | 0.373705 | -0.004196 | 3,914 | 29,452 |
| R4 fixed-selector workspace | 25 / 0.001 | 0.360665 | +0.008844 | 3,006 | 5,764 |
| R8 unbottlenecked shared encoder | 36 / 0.001 | 0.366755 | +0.002754 | 3,138 | 14,252 |
| R9 unrestricted eight-symbol code | 56 / 0.001 | **0.332441** | **+0.037069** | 4,058 | 29,612 |

The mean within-seed **minimum**, not the minimum of these seven
means, was **0.307147**. R9 attained that minimum in 10 seeds and R4
in four (ties counted for both); R2 and R8 each appeared at least once.
The candidate exceeded the strict 0.02 margin against the full envelope
only at seed 1012. Seed 1006's positive difference was smaller than
the required threshold. Against R9 alone, the candidate achieved a
strict 0.02 margin in only three seeds. These per-rival observations
do not replace the prespecified envelope.

R9's **copied candidate subfamily** reproduced the candidate for every
one of 8,192 enumerated history/local-bit/context cases and was
rechecked on the 16 trained candidate checkpoints: 131,072 clone
decisions. It matched the copied candidate's parameters and counted
forward MACs. This proves the architectural inclusion needed to
exclude an expressivity-necessity claim; it is **not** independently
trained R9 evidence. The separately fitted R9 produced the table's
0.332441 mean. Its selected variant used about 3.52 times the
candidate's declared forward MACs, while R4 used fewer parameters
and MACs than the candidate. The contract enforces **caps**, not exact
compute equality; none of these cost differences may be hidden.

The 112 final fits consumed approximately **16.219 billion measured
linear forward MACs** and **28.463 billion measured linear backward
MACs** in their training graphs, excluding separate route search,
evaluation, nonlinear backward kernels, optimizer, generator, and
diagnostic work. Fit wall time summed to **621.17 seconds**; the
entire final orchestration took **1,428.81 seconds**, including
provenance checks, copied engineering checkpoints, evaluation and
artifact writes. Engineering's 168 fits and configuration selection
took **2,396.30 seconds** end-to-end. R4's 16 final training-only
route searches added **49.29 seconds** outside fit wall time. Per-arm
optimizer-state maxima ranged from 24,152 to 32,508 bytes; the
process-lifetime peak working set reached about 275.5 MiB. The last
number is **not** an isolated per-model peak. Physical memory-bus
traffic and energy are unmeasured. See the [resource contract](PHASE3B_RESOURCE_CONTRACT_v1.md)
and raw manifest for coverage and each arm's actual expenditure.

## What was and was not learned

The candidate's held-out S1/S2/S3 losses were respectively
**0.426743 / 0.180000 / 0.501785**. Its S2 **always abstained** and
its S3 parity decisions were near chance. R9's corresponding losses
were **0.319244 / 0.180000 / 0.498077**: most of its gain was S1.
This is a major limitation on attributing the observed differences to
three-way competitive integration. The task itself was not
information-theoretically hopeless: evaluator-only R5/R7 exact-belief
controls achieved joint loss **0.153172**, S1/S2/S3 losses
approximately **0.104416 / 0.093474 / 0.261627**, and S2 bet on
about 52.4% of episodes. They are **EXTERNAL**, not trained primary
comparators. R6's evaluator-only selector over the candidate's
learned states reached **0.283744** and diagnoses selection headroom,
not an autonomous advantage.

The separate [H3/H10 analysis](PHASE3B_H10_DIAGNOSTICS_v1.md)
enumerated all 1,024 prospective matched-history A/B pairs: the
learned candidate changed its address on **none**. A training-only
probe nevertheless decoded private port-state counts with 72.89%
accuracy versus a 34.04% majority baseline. At held-out context 3,
the mean **within-seed** address entropy was only 0.01868 bits.
Thus available acquired evidence did not translate into the
prospectively desired state-dependent competitive switch; pooled
address frequencies across differently trained seeds are not
within-model switching. This tightens the selector limitation
without changing the primary gate or proving unique source semantics.

This gap to the ideal and the weak learned S2/S3 behavior constrain
the inference: under the frozen optimizer and sample budget, the
candidate had **no demonstrated comparative value**; the finals do
not establish a general superiority of R9 for competent
multi-consumer integration. There was no prespecified per-specialist
competence gate, so we do not retroactively delete the failed
primary test or change the world because the candidate lost.
Treat the outcome as both an empirical negative and a warning that
the intended multi-specialist phenomenon was only weakly realized.

## Secondary evidence and reductions

The [seven intervention families](PHASE3B_INTERVENTIONS_v1.md) ran
across all final seeds with exact intact/no-op replay. Address
substitution and several forced routes **improved** candidate loss;
the trained out-of-band no-message readout also improved it
(0.355565 versus 0.369509). Replacing port 2 or 3 had zero
aggregate held-out loss effect. A new sixteen-bit diagnostic
readout improved loss but changed both capacity and trained heads;
a newly trained unlimited-state readout worsened it. These are
causal/use and optimization diagnostics, not primary rival wins.

In the [frozen-core transfer study](PHASE3B_TRANSFER_v1.md), an equal
780-parameter new head trained on 2,048 episodes reached error
**0.254761** from the candidate's three-bit interface,
**0.251328** from R9's three-bit code, and **0.246536** from R4's
three-bit route. R1's wider intact broadcast reached **0.193329**;
its 3,456-bit read interface is not bandwidth-matched to the
three-bit arms. Original heads and representation tensors remained
byte-identical. This is frozen-representation/readout reuse, **not**
zero-shot transfer or proof of workspace necessity.

| Simpler explanation | Disposition in this bounded task |
| --- | --- |
| Ordinary multi-task learning / parameter sharing | Not excluded; learned heads and common representations suffice as descriptions of the surviving behavior. |
| Mixture-of-experts routing / fixed router | R4's cheaper training-only fixed route is competitive on mean; learned selector value was not demonstrated. |
| Standard attention / modular credit assignment | No result uniquely distinguishes the candidate from these familiar implementation patterns. |
| Finite-state controller | Exact four-counter belief exists in the environment; no learned latent's semantic uniqueness was established. |
| Private recurrent memory | R3 is a valid, though weaker-on-mean, primary comparator; private access is not universally excluded. |
| Unrestricted learned coding | Independently trained R9 is the strongest mean primary arm; its function class contains the exact candidate clone. |
| General shared representation learning | R1 and R8 remain ordinary shared-feature alternatives; R1 was strongest on secondary transfer with much wider reads. |

## Architectural disposition and stop

Retain the measured N1 fact that paid persistence can be causally
necessary **under a decay manipulation**, and the reduced N2 fact
that making task-relevant information available can matter. Neither
the explicit maintained self-integrity register from Phase II nor the
paid shared-slot machinery from Phase III is restored as a
foundation. Phase III-B adds **no surviving candidate-exclusive
competitive-occupancy advantage**. A compact learned code or
training-only fixed route is a simpler description of what survived
this particular comparison; neither is thereby a demonstrated
consciousness-relevant integration mechanism.

Do not start Phase IV, metacognition, autobiographical memory,
organism reopening, or an LLM-scale system on this evidence.
No consciousness, subjectivity, global-workspace-theory
confirmation, or historical novelty claim follows. The existing
Phase II and Phase III negative findings stay frozen.

**Exactly one next question requiring new authorization:** Can an
unrestricted finite shared code support *competent* decisions by
all three specialists (including nontrivial delayed bets and parity
prediction) under a prospectively specified learning regime, while
remaining competitive against equally budgeted fixed routing and
private-state controls? That is a new feasibility/discrimination
question about the simpler mechanism, **not** permission to retune
this failed Phase III-B primary comparison or to start Phase IV.
