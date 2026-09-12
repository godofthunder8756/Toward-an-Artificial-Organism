---
title: E3 targeted literature review
description: Primary-source constraints on acquired-information maintenance and conventional rivals
ms.date: 2026-09-09
---

## Status and scope

Research completed for the bounded review, with access limitations below.
No E3 experiment has been implemented or executed. This is not a systematic
review, an external preregistration, or a demonstration of originality.

The immediate assignment in [NEW_AGENT_GUIDE.md](NEW_AGENT_GUIDE.md) is to turn
[E3_DESIGN.md](E3_DESIGN.md) into a falsifiable test. The central distinction is
between making preserved information available again and reconstructing damaged
storage from information that genuinely survives inside the tested system.

Two independent research passes inspected primary sources. Detailed access
records, source anchors and limitations are preserved in the
[memory review](.copilot-tracking/research/subagents/2026-09-09/memory-maintenance-literature.md)
and [coding review](.copilot-tracking/research/subagents/2026-09-09/error-correction-literature.md).
The table below contains 13 distinct sources; Growing NCA appeared in both passes.
Full-text inspection means relevant body sections were read, not replication.

## Evidence and consequences

| Source and access                                       | Supported finding                                                         | Consequence for E3                                                        |
|---------------------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|
| Frey and Morris, 1997; abstract (1)                       | Transient synaptic tags can capture products supporting persistent LTP.    | Tags are acquired state, not information-free repair instructions.         |
| Fusi, Drew and Abbott, 2005; abstract (2)                 | Metaplastic cascades improve acquisition-retention trade-offs.             | Count hidden states; interference resistance is not destruction recovery.  |
| Benna and Fusi, 2016; abstract and 2015 preprint body (3) | Coupled fast and slow variables can extend memory lifetimes.               | Slow stores are surviving information; damage and cost them too.           |
| Hopfield, 1982; abstract (4)                              | Collective dynamics support associative recall and error correction.       | Completing a cue is not repairing the learned storage itself.              |
| Li and van Rossum, 2020; article body (5)                 | Transient caching and selective consolidation can reduce modeled costs.    | Threshold caching is a simpler rival; costs are model assumptions.         |
| Placais and Preat, 2013; abstract (6)                     | Starvation suppresses costly aversive long-term-memory formation.          | Formation gating is not selective relinquishment of existing memories.     |
| Mordvintsev et al., 2020; article body (7)                | Trained local NCA rules can regenerate a target pattern after damage.      | Target-trained update weights can retain the pattern outside cell state.   |
| Zhang, Risi and Darlow, 2025; author article body (8)     | NCA agents can update parameters throughout competitive development.       | Continual learning and spatial aliveness do not prove memory maintenance.  |
| Hamming, 1950; original article OCR (9)                   | Redundant parity enables detection and correction of specified errors.     | Parity values carry acquired information; the coding law can be generic.   |
| Wade et al., 2012; article body (10)                      | Surviving synapses compensate for reduced transmission in a neural model.  | Restored firing does not demonstrate recovery of arbitrary learned bits.   |
| Kirkpatrick et al., 2017; author preprint body (11)       | EWC protects task parameters; a separate test probes parameter noise.      | Anchors, Fisher estimates and replay are additional acquired state.        |
| Yoon and Erez, 2010; abstract (12)                        | Flexible ECC separates frequent detection from less frequent correction.   | Conventional rivals need not pay maximal correction costs on every read.   |
| Patel and Hsiao, 1972; abstract (13)                      | Adaptive correction addresses the cost of rare multi-error events.         | Adaptive correction effort is established territory, not generic novelty.  |

### Primary-source links

1. Frey and Morris, *Synaptic tagging and long-term potentiation*.
   [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/9020359/),
   [DOI](https://doi.org/10.1038/385533a0).
2. Fusi, Drew and Abbott, *Cascade models of synaptically stored memories*.
   [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/15721245/),
   [DOI](https://doi.org/10.1016/j.neuron.2005.02.001).
3. Benna and Fusi, *Computational principles of synaptic memory consolidation*.
   [Published abstract](https://pubmed.ncbi.nlm.nih.gov/27694992/),
   [2015 preprint](https://arxiv.org/html/1507.07580v1), titled
   *Computational principles of biological memory*. The journal and preprint
   versions were not assumed identical.
4. Hopfield, *Neural networks and physical systems with emergent collective
   computational abilities*. [Primary abstract](https://europepmc.org/article/MED/6953413),
   [DOI](https://doi.org/10.1073/pnas.79.8.2554).
5. Li and van Rossum, *Energy efficient synaptic plasticity*.
   [Full article](https://elifesciences.org/articles/50804).
6. Placais and Preat, *To favor survival under food shortage, the brain disables
   costly memory*. [Primary abstract](https://europepmc.org/article/MED/23349289),
   [DOI](https://doi.org/10.1126/science.1226018).
7. Mordvintsev et al., *Growing Neural Cellular Automata*.
   [Full article](https://distill.pub/2020/growing-ca/).
8. Zhang, Risi and Darlow, *Petri Dish Neural Cellular Automata*.
   [Author article](https://pub.sakana.ai/pdnca/), dated 2025-10-31.
   Peer-reviewed publication status was not established.
9. Hamming, *Error Detecting and Error Correcting Codes*.
   [Original scan](https://archive.org/details/bstj29-2-147),
   [OCR text](https://archive.org/stream/bstj29-2-147/bstj29-2-147_djvu.txt).
10. Wade et al., *Self-repair in a bidirectionally coupled astrocyte-neuron (AN)
    system based on retrograde signaling*.
    [Full article](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2012.00076/full).
11. Kirkpatrick et al., *Overcoming catastrophic forgetting in neural networks*.
    [Author preprint](https://arxiv.org/html/1612.00796v2),
    [DOI](https://doi.org/10.1073/pnas.1611835114).
12. Yoon and Erez, *Virtualized and flexible ECC for main memory*.
    [Publisher abstract](https://dl.acm.org/doi/10.1145/1735971.1736064).
13. Patel and Hsiao, *An adaptive error correction scheme for computer memory
    system*. [Publisher abstract](https://dl.acm.org/doi/10.1145/1479992.1480002).

## What changes in the experiment

### Separate preservation, reconstruction and relearning

An intact majority can already answer correctly after one replica is lost.
Writing a replacement may therefore improve robustness without improving
immediate accuracy. Measure paid storage changes and performance after an
additional held-out damage challenge, not only immediate post-repair recall.

In a binary task, the chosen answer plus a correctness reward identifies the
target. Removing explicit examples while retaining task-dependent energy,
success feedback or termination still permits relearning. The isolated recovery
phase must remove every answer-dependent consequence.

### Inventory information, not nominal parameters

Potential copies include redundant traces, slow variables, learned policies,
optimizer moments, replay, topology, transient decoded answers, resource layouts,
PRNG state and delayed events. Fixed-precision metadata and scratch storage count
too. A finite number of unrestricted real numbers is not a finite-bit budget.

Generic coding/update laws may remain protected if fixed independently of the
individual's assignments. That does not establish self-maintenance of the laws
or of the hardware executing them.

### Build the conventional explanation first

The strongest current account is ordinary error correction, paid scrubbing and
ordinary reward-trained resource allocation. A fixed code may have an adaptive
maintenance policy. Beating an always-copy or no-repair controller is not evidence
against this account.

Use the same representation with fixed, disabled and RL-controlled scrubbing to
isolate allocation. Add a capacity-matched block code when cross-association
communication is allowed. Report its extra read, decoder and transport costs
rather than declaring a universal fairness match from code size alone.

### Do not interpret complete erasure through a p-value alone

Construct post-erasure state and subsequent inputs to be independent of the
answer table. Test paired histories differing in individual bits and exhaustive
small tables. A finite sample need not be exactly 50% correct; failure to reject
chance is not evidence of noninterference. Unexpected below-chance dependence
also matters because reversing predictions could exploit it.

## Mathematical baseline proposal

For independent unknown flips with probability $p$, majority decoding has error
probability $3p^2-2p^3$ with three replicas, and
$10p^3-15p^4+6p^5$ with five. These are theoretical channel results, not E3 data.
Known erasures, unequal error rates and correlated damage require separate rules.

A four-bit payload with five replicas uses 20 code bits. Comparing it only with
a seven-bit Hamming code wastes the rival's available capacity. A fixed binary
linear $[20,4,10]$ code is a stronger capacity-matched challenge: encode against
all 15 nonzero four-bit columns, then repeat the four unit columns and their XOR.
Minimum distance is ten. The analogous punctured $[12,4,6]$ construction removes
the columns $e_1,e_2,e_1+e_2$ from the 15-column code. These are derived candidate
constructions, not algorithms attributed to Hamming's article.

Read-only enumeration checked all 16 codewords and 120 pairwise distances for
each construction: minimum distances six and ten respectively. Enumeration of
flip patterns at $p=0.1$ also agreed with the majority formulas. These analytical
checks are not E3 simulation results or a validation of the cost model.

The [coding review](.copilot-tracking/research/subagents/2026-09-09/error-correction-literature.md)
gives the derivation and locality caveats. Algebraic validation does not establish
energy advantage or a good selective-forgetting policy.

## Limits and decision

Full texts were not obtained for the tagging, cascade, Hopfield, starvation, or
two adaptive/flexible ECC sources. The review of EWC distinguishes its transient
noise test from permanent corruption. A direct persistent-corruption continual
learner with all auxiliary memories also damaged remains an evidence gap.
No absence-of-prior-art claim follows from that gap.

The next bounded step is the proposed E3a information-maintenance assay in
[E3_PROTOCOL_v0_1.md](E3_PROTOCOL_v0_1.md), followed only later by E3b's coupled
neural substrate. This staging exposes the conventional explanation before
adding architecture. It does not establish life, wanting, or subjectivity.
