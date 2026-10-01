# A6 resource-supervisor correction and bounded continuation v2

Independent implementation review found three resource-accounting/enforcement
defects in the frozen v1 supervisor:

1. A second supervisor could skip a live started job and launch another.
2. Missing node counts retained an internal zero, and F3 counts were omitted
   from the initial independent replay.
3. The parent timeout began after startup instead of using an absolute
   whole-process deadline.

These are resource defects, not an invalidation of the exact population,
conditional lemmas or rational dual mathematics. No actual parallel execution
or prefix watchdog overrun was demonstrated. Unknown node use is not zero.

The owned v1 supervisor was stopped after the first positive F1 job completed
and the negative F1 job started. Both consume the original allocation and will
NOT be rerun. Preserve their source, protocol, contract, root certificates and
raw diagnostics unchanged; record the interruption and corrections additively.

Only the original four unconsumed jobs may continue: F2 positive/negative and F3
bank/singleton. Frozen gate, actual graph, constructive coefficient boxes,
100,000-node/900-second/4-GiB limits and no-training restriction do not change.
This is not a seventh search or a new architecture.

Before F2 has run, an additional exact [gate-reduction theorem](../../A6_GATE_REDUCTION_v1.md)
shows every specialist gate is implied by the joint threshold for R9.
F2 can therefore use scalar count-dominance rather than the more expensive
256-history conjunction image. It also compactly factors the retained decoder
alphabet and uses proved S1 word-label symmetry. The successor freezes this
prospective formulation change before its two jobs; three major formulations
and six total slots remain the same. No old result is reclassified as a stronger
bound and no fixed-message assumption is introduced.

The successor:

- acquires an exclusive supervisor lock;
- reserves all remaining original journals before execution, so the legacy
  supervisor cannot advance into another job;
- refuses an unclosed launched job;
- fixes one absolute monotonic deadline before process creation and passes it
  through the handshake and worker budget;
- explicitly terminates only its assigned Job Object at the deadline;
- preserves unknown aggregate node counts and accounts for F3;
- reports observed cutoff compliance, rather than hiding scheduler/cleanup
  timing under a success-shaped assertion.

The resource continuation contract freezes this new supervisor before the four
remaining jobs. Original scientific source hashes remain unchanged. Read-only
replay does not relax the execution HEAD lock. A6 still requires an independently
certified PASS/FAIL, or an honest bounded UNRESOLVED disposition.
