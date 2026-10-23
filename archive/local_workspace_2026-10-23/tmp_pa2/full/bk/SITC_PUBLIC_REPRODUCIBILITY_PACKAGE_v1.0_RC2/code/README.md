# Public SITC verification and reference code

This directory contains the portable code needed to verify the normalized
public evidence and to execute a fresh reproduction of the engineered finite
reference construction. It has no dependency on a Git checkout, a Windows
process API, the caller's current working directory, or private/internal
campaign directories.

## Required package layout

The code resolves all scientific inputs relative to the extracted package:

```text
PACKAGE_ROOT/
  code/
    public_verify.py
    run_public_reference.py
    sitc_core.py
    sitc_experiment.py
    sitc_plan.py
    sitc_score.py
  protocol/
    SITC_D2_PREREGISTRATION_v1.0.0.json
    SITC_D2_FREEZE_RECEIPT.json
  evidence/
    ANALYSIS.json
    NORMALIZED_SCIENTIFIC_PROJECTION.json
  receipts/
    NORMALIZED_REPLICATION_RECEIPT.json
```

Python 3.10 or later is required. No third-party Python package is required.

## Mode 1: frozen normalized-evidence verification

Run from any working directory:

```text
python /path/to/PACKAGE_ROOT/code/public_verify.py
```

Expected status:

```text
PUBLIC_NORMALIZED_EVIDENCE_VERIFIED
```

This mode verifies the exact preregistration, freeze receipt, historical
analysis, and normalized-projection hashes; checks the six historical summary
entries; and re-scores the normalized projection. It does not execute the
reference construction, load the six historical raw arrays, replay historical
process provenance, or reconstruct the historical campaign.

## Mode 2: fresh public reference execution

```text
python /path/to/PACKAGE_ROOT/code/run_public_reference.py --output reference_output
```

The output directory must not already exist. This mode launches six new child
processes in the registered forward/reversed order, uses unique prospective run
nonces, scores each new raw result, and checks that every normalized projection
equals the published projection hash. Add `--keep-raw` only if the large new
raw outputs are needed.

This is a fresh execution of the public reference construction. It is not a
reconstruction of the historical six-run campaign and does not replay that
campaign's absolute command binding or operating-system process-provenance
record.

## Source provenance

- `sitc_core.py` and `sitc_experiment.py` are byte-identical to the accepted
  frozen campaign sources.
- `sitc_plan.py` is a new package-relative adapter that reads the single
  canonical public preregistration under `protocol/`.
- `sitc_score.py` contains the scientific constants and scoring functions
  extracted from the accepted frozen analyzer, without its historical
  execution-infrastructure validators.
- `public_verify.py` and `run_public_reference.py` are RC2 publication tools;
  neither was the historical campaign runner.

`REFERENCE_CODE_PROVENANCE.json` records source hashes and the extraction
boundary. The code files are licensed under MPL-2.0. This README and the
provenance record are documentation licensed under CC BY 4.0 according to the
package's file-by-file license map.

## Claim boundary

The maximum registered claim is:

> In the registered finite construction, a relationally self-indexed temporal
> state causally influenced future-directed choice through the separately
> intervened prospective-evaluation path.

The code and its successful execution do not establish phenomenal
consciousness, subjective experience, personhood, AGI, human-equivalent
selfhood, spontaneous emergence of a self-model, or architectural novelty.

