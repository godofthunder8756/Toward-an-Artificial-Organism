# Phase III-B result archive

This is a byte-identical repository mirror of the independently audited
Phase III-B outputs. The original execution used an exclusive fresh
directory; this mirror was copied only after the final audit. The
`finals/` directory contains the exact 404-file final artifact set,
including the signed engineering/final approvals, source/dependency
freeze, seven engineering selections, all engineering checkpoints,
and 112 final checkpoints with their raw episode traces.

Run `phase3b.audit.audit(Path("phase3b_results_v1/finals"))` from the
repository root to recompute the negative primary gate and replay the
checkpoints. The [independent audit](phase3b_final_audit_v1.json),
[EXTERNAL controls](phase3b_external_controls_v1.json),
[I1-I7 traces](interventions/summary.json),
[H3/H10 analysis](phase3b_h10_diagnostics_v1.json), and
[secondary transfer index](transfer/transfer_index.json) are separate
results, not additional intact primary arms. No private signing key
is included.

The post-final diagnostic scripts are retained here byte-for-byte
because their hashes appear in the corresponding result records.
Their paths pin the original Windows session location; to rerun them
elsewhere, one must make a **new versioned run** and report the new
script digest. Do not edit an archived script in place and claim its
old hash. The primary package and protocol are in `../phase3b/`
and `../ACI_PHASE3B_PROTOCOL_v1.md`.

The archive's primary outcome is a valid negative (1/16 required
effect wins, not 14/16), not an audit failure. See the
[bounded verdict](../PHASE3B_VERDICT_v1.md) for interpretation
and resource limitations.
