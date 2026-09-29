---
description: Phase III-B H15/H16 resource-accounting interpretation before scored execution
ms.date: 2026-09-29
---

# Phase III-B resource contract v1

This document interprets the prospective [Phase III-B protocol](ACI_PHASE3B_PROTOCOL_v1.md)
for an executable H16 review. It is not an amendment to the hypothesis,
endpoint, rival set, training allowance, significance rule, or numerical
caps. In particular, the protocol specifies *caps*, not equality of every
measured hardware cost between architectures. A material change to any
binding condition requires a separately versioned prospective protocol
before scored execution. No engineering or final result is reported here.

## Level 1: binding eligibility and comparison gates

Enforce, on the **entire learned arm**, at most 4,096 trainable parameters
and 80,000 executed linear forward multiply-accumulates per complete
12-tick, four-decision episode. Count all encoders, private copies,
selector, quantizers, and heads as applicable. An arm exceeding either cap
is ineligible; a cheaper arm is not padded to simulate equal hardware
consumption. These are upper bounds, not a claim of matched FLOPs, memory,
latency, or energy. The MAC cap does not silently include or assign a
fictitious conversion factor to nonlinear operations.

Every configuration receives exactly 8,192 training episodes in batches
of 32 and 256 AdamW updates with zero weight decay, the declared
likelihood-ratio objective and baseline, gradient clipping at norm 1,
and the same permitted labels. The candidate, R4, and independently
trained R9 use exactly eight on-wire words (three bits) with the declared
consumer visibility; R1/R2/R3/R8 have their explicitly disclosed wider
interfaces. All seven learned families, all six configurations per
family, engineering seeds 0-3, final seeds 1000-1015, the prescribed
selection rule, R4 training-only route enumeration, and the complete
within-seed comparator envelope are mandatory. Engineering has no
authority to change the endpoint, effect threshold, loss, rival set,
capacity, or exact final test. The R9 copied candidate subfamily is an
expressivity check, **not** an independently fitted comparator.

## Level 2: measure and disclose, without claiming equality

For each actual fit, evaluation, route search, and diagnostic as applicable,
record whole-arm parameter and recurrent-state bytes, executed linear
forward and backward MACs, annotated nonlinear and indexing operation
counts, optimizer and baseline state bytes, training episodes and
updates, wall time, search/trial expenditure, and the measured compute
consumed. Collect profiler-reported operator FLOPs, CPU allocator
activity, process working-set high-water mark, and inference timing on
representative unscored runs with their measurement conditions. Report
read bandwidth and any diagnostic's added parameters and work separately.
These measures reveal gross cost asymmetries; they do not redefine the
primary caps or convert a cheaper rival into an ineligible rival. An
actual-run meter must identify its coverage, especially uncounted
backward nonlinear kernels, loss, clipping, AdamW, and data generation.

The synthetic one-update CPU profiler currently covers a complete
forward/backward/optimizer step without scientific training. At the
highest grid widths its dry-run whole-arm parameter counts range from
3,906 to 4,058 and full-episode linear forward MACs range from 7,556 to
30,008. This shows cap eligibility only, not actual training feasibility,
hardware parity, or any measured final result. Actual-run resource logs
remain necessary.

## Level 3: quantities not measured by the current meter

Torch allocation counts and annotated logical tensor bytes are **not**
physical memory-bus traffic, cache traffic, hardware energy, or isolated
kernel memory cost. An OS process-lifetime high-water mark is **not** an
isolated per-model peak; Python `tracemalloc` does not cover the native
torch allocator. These physical quantities are unmeasured unless an
appropriate validated hardware profiler is used and its method and
coverage are recorded. No physical-traffic equality claim or fabricated
byte count is permitted. The unavailable physical measurements alone do
not prevent executing the protocol's declared caps and bounded
inductive-bias test; any conclusion that actually depends on their
equality is out of scope.

## H16 acceptance

Independent review must verify the counted caps, the real forward and
backward paths for **every** primary family, the non-MAC disclosures,
source/configuration hashes, fresh result paths, seed isolation, and
authorization provenance before removing the training lock. If the
actual experiment violates a binding condition, stop and preserve the
failure; do not relabel a resource proxy as a hardware measurement or
retroactively change the protocol.
