# Coupled four-context Stage-A analysis

**Analytic only; no training. The Stage-A gate remains unresolved.**
See the [status report](../SHARED4_STAGE_A_STATUS_v1.md).

The exact bracket is:
`5159249/29296875 <= L_R9_SHARED4 <= 1031759/4687500`.
Do not treat either bound as an exact optimum or a failed upper search
as architectural impossibility.

## Artifacts

* [baseline hashes](baseline_hashes.json): 1064 earlier files preserved.
* [shared witness](shared_witness.json): sparse parameters of one actual
  shared Arm plus exact population and margin checks.
* [constructor report](SHARED_WITNESS.md): finite gain, 24 active units,
  shared W/U/heads, and bounded proposal scopes.
* [lower investigation](COUPLED_LOWER.md) and
  [lower results](coupled_lower_result.json): exact necessary-condition
  checks, not a closed global optimum certificate.
* [independent final upper](independent_upper_final.json): exact risk
  on a fresh repository Arm, with verifier/constructor digests.
* [independent audit](independent_audit.json): scope-qualified Stage-A review.

The earlier `independent_upper.json` precedes the constructor's
no-overwrite safeguard; it has the same population result and is
superseded for final source provenance by `independent_upper_final.json`.

## Replay without optimization

```powershell
python -m pytest shared4_v1 -q
python shared4_v1\preservation.py shared4_v1\baseline_hashes.json --check
python shared4_v1\coupled_lower.py --verify-only
python shared4_v1\verify_witness.py shared4_v1\shared_witness.py C:\chosen\fresh_upper_replay.json
```

The upper verifier exhausts the exact population; it never trains.
The lower verifier replays rational certificates without LP/MIP solving.
The original R10/R10A files are read-only inputs.

The actual encoder can change its message with context. Any proposed
bound that silently holds `m(H)` fixed across all four contexts is not
a valid R9-family lower bound. A regression test explicitly verifies
context-changing words.

The user-selected joint gate and strict specialist baselines are in
[the prospective gate](../SHARED4_STAGE_A_GATE_v1.md). Nothing in this
directory authorizes Stage B or Stage C while that gate is unresolved.
