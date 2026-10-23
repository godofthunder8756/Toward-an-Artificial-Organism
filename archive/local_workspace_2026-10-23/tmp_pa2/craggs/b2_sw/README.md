# Theory of Everything Research Programme — B2 Causal Maintenance Network
## Confirmatory Experiment Software and Reproducibility Package, v1.0.0

Author: Kenneth Craggs  
Release date: 3 October 2026  
Licence: MIT  
OSF preregistration: https://doi.org/10.17605/OSF.IO/GQANP  
Related experimental framework: https://doi.org/10.5281/zenodo.22857230  
Zenodo software DOI: https://doi.org/10.5281/zenodo.23122125  
Companion confirmatory dataset: https://doi.org/10.5281/zenodo.23122412

## Purpose

This release contains the software and frozen configuration used to execute and analyse B2, the causal-maintenance experiment in Experimental Block I of the Theory of Everything Research Programme.

B2 asks whether an artificial system can preserve its operational organisation through causally identifiable internal maintenance rather than merely through passive stability or external support. The confirmatory study compares five architecture classes:

- passive persistence;
- external maintenance;
- internal feed-forward maintenance;
- reciprocal internal maintenance;
- a budget-matched brute-force internal bypass.

The confirmatory design was publicly preregistered on OSF before any held-out B2 confirmatory seed was executed.

## Preregistered confirmatory study

The release includes the seven frozen v1.0.0 confirmatory manifests and lock files for:

- low-disturbance maintenance;
- medium-disturbance maintenance;
- high-disturbance maintenance;
- external-support withdrawal;
- targeted C1 ablation;
- specific functional rescue;
- equal-budget irrelevant rescue.

Twenty held-out seeds are stored in `configs/seeds/B2_CONFIRMATORY_SEEDS_V1.txt`.

The registered viability threshold is 0.35 for each component. Active architecture maintenance budget is 0.03. The decisive ablation occurs at step 200. The specific and irrelevant rescue amount is 0.012. The primary causal-edge threshold is epsilon_w = 0.25.

## Confirmatory verdict vector

The confirmatory study produced the preregistered mixed result:

- H1.1 Active maintenance vs passive persistence: **RETAIN**
- H1.2 Internal vs external maintenance: **RETAIN**
- H1.3 Reciprocal topology / targeted propagation: **RETAIN**
- H1.4 Specific functional rescue: **RETAIN**
- H1.5 Boundary/timescale robustness: **DEFERRED**
- H1.6 Reciprocal-topology necessity: **REDUCE_RECIPROCAL_NECESSITY**

The result supports artificial functional/causal internal maintenance within the registered architecture family and validates a specific reciprocal causal edge. It does not support reciprocal closure-like topology as necessary for the measured maintenance capacity, because the preregistered budget-matched brute-force bypass satisfied all non-inferiority conditions.

## Packaging-repair audit

The first confirmatory execution attempt stopped before simulation data were generated because the archived preregistration source snapshot omitted several Python package initialisation/helper modules. Those import-support modules were restored from the already validated B2 development baseline. Shared Python source files were checked by SHA-256, the preregistered scientific manifests/configurations remained unchanged, and the repair is documented in `audit/PACKAGING_REPAIR_RECORD.md`.

This release therefore contains the complete executable source used for successful confirmatory execution, together with the frozen preregistration records needed to audit the scientific specification.

## Installation

Python 3.11 or later is required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the virtual environment using the appropriate command for your shell.

## Validation

Run the packaged test suite:

```bash
pytest
```

Validate any frozen manifest with:

```bash
python validate_manifest.py validate configs/confirmatory/b2/B2_MAINT_HIGH_CONFIRM_001.yaml
```

Verify a frozen manifest/lock pair with:

```bash
python validate_manifest.py verify configs/confirmatory/b2/B2_MAINT_HIGH_CONFIRM_001.yaml
```

## Re-running a confirmatory condition

For example:

```bash
python run_experiment.py \
  configs/confirmatory/b2/B2_MAINT_HIGH_CONFIRM_001.yaml \
  --project-root . \
  --output-root reproduced_runs
```

Reproductions should be labelled as reproductions. They are not replacements for the original confirmatory raw trajectories archived in the companion dataset release.

## Regenerating the registered analysis

Extract the companion B2 dataset release and point the portable analysis script to its `raw/` directory:

```bash
python analyze_b2_confirmatory.py \
  --raw-root /path/to/extracted_dataset/raw \
  --output-root reproduced_analysis
```

The release version of this script differs from the execution-environment copy only in accepting portable input/output paths and in declaring the already-used `pandas` dependency explicitly. Statistical logic, thresholds, bootstrap seed (20261002), 10,000 bootstrap resamples and verdict rules are unchanged. This portable version was verified to regenerate the original substantive analysis artefacts bit-for-bit.

## Repository structure

- `configs/` — frozen manifests, locks, environment and architecture configurations, registries, schemas and held-out seeds.
- `toe/` — experiment runner, provenance infrastructure, agents and maintenance-network environment.
- `tests/` — automated validation tests.
- `preregistration/` — frozen public preregistration record and integrity reference.
- `audit/` — unlock and packaging-repair records.
- `analyze_b2_confirmatory.py` — registered confirmatory analysis, made path-portable for this release.
- `run_experiment.py` — manifest-driven execution entry point.

## Scope

B2 concerns artificial functional/causal maintenance within a preregistered three-component architecture family. It does not establish biological life, universal organisational closure, the historical origin of life, intelligence, consciousness, or universal necessity for Transition Problem 1.


## Citation

Craggs, K. (2026). *Theory of Everything Research Programme: B2 Causal Maintenance Network Confirmatory Experiment Software and Reproducibility Package* (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.23122125

Companion confirmatory dataset and decision record: https://doi.org/10.5281/zenodo.23122412
