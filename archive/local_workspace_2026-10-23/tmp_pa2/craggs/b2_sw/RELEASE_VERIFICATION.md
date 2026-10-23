# B2 Release Verification

Release candidate: B2 Causal Maintenance Network Software v1.0.0  
Verification date: 3 October 2026  
Reserved Zenodo DOI: 10.5281/zenodo.23122125  
Companion Dataset DOI: 10.5281/zenodo.23122412

The public-release candidate was tested after clean extraction.

Results:

- Packaged software test suite: **22/22 tests passed**.
- Internal software checksum manifest: **PASS**.
- Companion dataset checksum manifest: **PASS**.
- Portable `analyze_b2_confirmatory.py` regenerated the archived substantive analysis artefacts bit-for-bit from the clean-extracted companion raw dataset.

Bit-for-bit verified artefacts:

- `b2_confirmatory_analysis_record.json`
- `b2_per_seed_terminal_metrics.csv`
- `h13_feedforward_ablation_effects.csv`
- `h13_reciprocal_ablation_effects.csv`
- `h14_rescue_effects.csv`
- `h16_bypass_ablation_comparison.csv`
- `b2_path_viability_by_disturbance.png`
- `B2_CONFIRMATORY_ANALYSIS_RECORD.md`

The portability change to the public analysis script affects only file-path handling; the preregistered statistical logic, bootstrap seed, resample count, thresholds and decision rules are unchanged.
