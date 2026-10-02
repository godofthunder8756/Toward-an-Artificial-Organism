# SUB-A0 supplied-substrate boundary v1

2026-10-01. Boundary freeze authorized by the user's A0 design-only request.
Starting repository HEAD: `415e3b12a1ab6624bc8d94dfcefad3d53a268d2e`.
This boundary is fixed before the new prior-art review or design formulation.
It is not an experimental protocol freeze and authorizes no execution.
Historical A0 autonomy documents are a separate lineage; SUB-A0 names this
neural substrate proposal.

## 1. Supplied physics

The host may provide generic matrix multiplication, addition, fixed
nonlinearities, scalar comparison, indexing, a clock, random draws and a
uniform write primitive. Generic evaluation of a computation graph is supplied.
The topology, precision and writable address space must be declared in the
eventual protocol. A fixed topology is not a clean parameter template.

The uniform write primitive accepts an address and update computed by the live
system and applies the same rule to every writable coefficient. It cannot
choose targets, infer a corrective value, compare with originals, privilege
repair circuitry, restore an initial coefficient or consult task truth.
Any uniform clipping or write-budget enforcement must be content-blind,
declared before execution, identical across banks and rivals.

Generic physics is not the hypothesis. No claim of hardware independence,
unqualified production closure or an entirely self-produced system follows.

## 2. Performing machinery

EVERY learned coefficient participating in the computation of repair targets,
update magnitudes, routing, priorities, addresses or predicted consequences is
performing machinery. This includes coefficients computing updates to their
own bank, and learned write decoders, recurrent controllers, replay generators,
embeddings, biases, normalization gains and any learned optimizer.

All such coefficients must be writable and damageable under the declared
substrate law. The same rule applies to learned task parameters. Banks cannot
be exempted from corruption because a functioning repairer is convenient.
Persistent recurrent states, replay samples, eligibility traces, cached outputs
and optimizer moments are also vulnerable; no persistent acquired information
may reside outside the declared damage domain.

A frozen pretrained repair network violates this boundary. A live gain gating
an otherwise host-computed content-specific correction is not an implementation
of vulnerable performing repair. Host median, majority or a clean teacher may
be used as explicitly EXTERNAL controls, never silently as the candidate's
content-specific repair computation.

## 3. Content and source boundary

Initial development may receive declared task examples and task/prediction
objectives. Learned repair organization is learned information, even if it is
shared across individuals. Once a maintenance assay starts, no protected
checkpoint, target-weight array, teacher output cache, labels, evaluator answer
or outside parameter-generating network may be accessible to the candidate.
Any allowed within-assay environmental feedback must be declared; an assay
claiming recovery without re-teaching permits no answer-bearing feedback.

The repairer's outputs must be computed using the currently damaged live
organization and allowed inputs. Exact copying is not automatically correction.
Corruption may destroy all recoverable acquired information; complete deletion
with no remaining source must not restore arbitrary acquired content.

## 4. Separation from evaluator

True damage events, intact counterfactual states, original labels and scoring
functions belong to a read-only evaluator inaccessible to the agent.
Evaluator snapshots may support paired causal branches, but cannot be restored
into a continuing candidate life or supplied as repair targets.
Bank names and functional classification may be used by the evaluator for
analysis; they are not privileged allocator inputs.

No learned parameter may be relabeled as supplied physics after observing a
failure. Discovering a boundary violation invalidates the proposed endogenous
interpretation rather than authorizing a repair exemption.

## 5. Frozen scope and changes

This file is immutable after its SHA-256 is recorded in the separate boundary
freeze record. Corrections require a new version and explicit identification
of the changed assumption. No old scientific artifact, protocol or verdict is
superseded. Allocation hypotheses, model choices, prior-art comparisons and
prospective outcome rules belong in separate design documents.

TLS certificate verification must remain enabled for all literature retrieval.
Use verified HTTPS through the tool transport or a system-trust-store client;
never use an insecure flag or disable verification to work around a failure.
