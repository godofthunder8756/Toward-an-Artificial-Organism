# R10A: certified endpoint answer and analytic stop

## Answer to the governing question

At the frozen context-3 endpoint, the best system the **existing deployed
width-56 R9 architecture can express** has exact joint risk
**5159249/29296875 = 0.17610236586666667**.

This is attained by a legal finite-weight recurrent encoder and shared
affine heads, with a matching exact lower certificate. It is not a
decoder-only relaxation. Frozen learned R9 has risk `2003/6000`, far
above that achievable risk floor.

The exact total-excess decomposition is:

* **11.39882256% capacity**, `601889/29296875`;
* **1.08630738% deployed function-class restriction**, `3824/1953125`;
* **87.51487006% within-class learned/generalization shortfall**,
  `73936391/468750000`.

The class penalty is entirely removed by allowing one S3 message-bit
interaction (or its one-unit ReLU equivalent). S1/S2 relaxations do not
improve this endpoint optimum. That small readout correction cannot
explain or repair the large remaining shortfall by itself.

## Bounded interpretation

The representable solution was not attained in the frozen learning
regime. That does **not** identify generic optimizer failure. Context-3
encoder/head columns are unobserved in training and not tied by an
equivariance rule. Even optimal training-context predictions admit
held-out extensions separated by at least `8/75` joint loss.

This supports a large learning/generalization residual, with a
demonstrable identification problem. It does not establish that
held-out ambiguity caused all or most of the observed residual.

## Program status and explicit remaining gap

The short A0-A8 program is recorded on the
[actual board](.vscode/kanban-agent.json), without reopening the original
22 completed H-cards.

A0-A5 and A7 have their endpoint results and machine-checkable
constructions. **A6 is not fully complete**: the jointly shared
four-context deployed optimum is bracketed, not exactly certified.
The full-context decision-map counts have an exact finite feasibility
characterization but their large numeric sums were not evaluated.
Neither a one-context count nor four independently rotated policies
is falsely presented as that coupled class.

A8's final post-A0-A7 authorization decision therefore remains blocked.
This is an interim analytic stop, not a claim that every requested
all-context subproblem was solved.

**Recommendation: do not train.** Complete the coupled all-context
certificate and specify the minimal held-out extension/equivariance
assumption prospectively before authorizing any neural experiment.
No new workspace experiment, organism program, or Phase IV admission
is justified here.

## Provenance

Starting and ending HEAD:
`94f9ace0bf4582bd7ad70155a2a32df42cd08fda`.
Commit range: **none**; this additive analysis remains uncommitted.
The baseline inventory preserves **1032** original scientific files,
including the original primary archive, R10 archive and both prior
reports. Phase III-B verdict B is unchanged.

The [independent endpoint audit](r10a_v1/independent_audit.json) passed
the exact lower/upper equality, finite-weight witness, decoder ladder
and context bracket; **24 tests passed**. Its scientific-file
preservation check passed. Its broader literal-Git-blob preservation
claim is qualified: the board is intentionally modified as requested,
and pre-existing CRLF checkout normalization is not a scientific edit.
No claim of byte identity for the entire working tree to Git blobs is made.

Reports:
[baseline](R10A_BASELINE_v1.md),
[function class](R9_FUNCTION_CLASS_v1.md),
[full-class certificate](R10A_R9_CLASS_CERTIFICATE_v1.md),
[gap decomposition](R10A_GAP_DECOMPOSITION_v1.md),
[decoder ladder](R10A_DECODER_LADDER_v1.md),
[generalization](R10A_GENERALIZATION_BOUND_v1.md),
[specialist relaxations](R10A_SPECIALIST_LESIONS_v1.md).
Machine artifacts and replay commands are in
[r10a_v1](r10a_v1/README.md).
