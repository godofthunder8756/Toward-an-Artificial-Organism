# Release notes — v1.0.0

This is the first public software/reproducibility release for the B2 Causal Maintenance Network confirmatory study.

## Scientific specification

The seven confirmatory manifests, held-out seeds, architecture/environment configurations, intervention/rescue/bypass definitions, thresholds and decision rules are those frozen before confirmatory execution and publicly preregistered at DOI 10.17605/OSF.IO/GQANP.

## Release-engineering changes

Two non-scientific release-engineering changes are explicitly documented:

1. Python package initialisation/helper modules omitted from the archived preregistration source snapshot were restored from the already validated development baseline before confirmatory data generation. See `audit/PACKAGING_REPAIR_RECORD.md`.
2. `analyze_b2_confirmatory.py` has been made path-portable for public reuse, and `pandas` has been added explicitly to the dependency list. The statistical logic is unchanged. The portable script was verified to regenerate the original substantive analysis artefacts bit-for-bit from the archived raw dataset.

No scientific threshold, seed, intervention, maintenance budget, estimand or verdict rule was changed by these release-engineering steps.
