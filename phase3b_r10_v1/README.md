# R10 exact post-final supplement

This directory is outside the frozen `phase3b/` source inventory and
`phase3b_results_v1/finals/` artifact set. It executes the authorized
EXTERNAL optimal eight-symbol coding bound. **There is no neural training.**
See the [certification report](../PHASE3B_R10_CERTIFICATION_v1.md).

* [r10.py](r10.py): exact finite cost table, MILP codebook proposal, and
  exact branch lower-bound certificate generation.
* [certificate.json](certificate.json): optimal eight-symbol codebook,
  encoder for all 81 beliefs, and complete 11-node proof tree.
* [verify.py](verify.py): solver-free Fraction/integer optimality replay,
  including coverage of all 144 legal decoder maps.
* [evaluate.py](evaluate.py): fixed-code scoring on archived streams and
  exhaustive inference-only population evaluation of frozen R9.
* [evaluation/evaluation.json](evaluation/evaluation.json): comparisons,
  raw-trace hashes, frozen-source preservation and HEAD distinction.
* [independent_audit.json](independent_audit.json): independent mathematical
  and execution audit.
* [test_r10.py](test_r10.py): exact-cost, certificate tamper, legal local
  inputs and context-rotation tests.

Replay the published certificate and tests:

```powershell
python phase3b_r10_v1\verify.py phase3b_r10_v1\certificate.json
python -m pytest phase3b_r10_v1\test_r10.py -q
```

Recompute only into **fresh, explicitly chosen** paths:

```powershell
python phase3b_r10_v1\r10.py C:\chosen\fresh_certificate.json
python phase3b_r10_v1\evaluate.py phase3b_r10_v1\certificate.json C:\chosen\fresh_evaluation
```

The proposer needs installed NumPy and SciPy; exact verification uses only
the Python standard library. Scoring uses the original frozen NumPy/Torch
dependencies. It checks their hashes, all frozen source hashes, final
manifest/checkpoint/raw hashes, exact R9 episode replay, and preservation
of the entire frozen final directory plus verdict B. The supplement does
not weaken or rerun the original exact-HEAD authorization gate.

Expected certified loss: `5101889/29296875 = 0.17414447786666667`.
Expected full-information floor: `96/625 = 0.1536`.
Current frozen R9 population mean: `2003/6000 = 0.33383333333333333`.
No new learned arm, primary gate, or Phase IV admission follows.
