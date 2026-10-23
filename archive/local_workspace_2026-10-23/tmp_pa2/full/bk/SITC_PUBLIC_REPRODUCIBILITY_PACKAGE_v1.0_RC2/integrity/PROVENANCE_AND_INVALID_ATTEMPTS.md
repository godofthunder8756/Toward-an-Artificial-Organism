# Provenance and invalid-attempt ledger

## Pre-execution attempt 001

`INVALID_PRE_EXECUTION_ATTEMPT_ONLY` — the first execution-gate validator checked a joined absolute package path where it should have checked the registered internal relative name. The gate failed closed before the campaign directory existed. No SITC target step or scientific outcome was produced. The complete attempt is preserved separately as `SITC_PRE_GATE_ATTEMPT_001_INVALID_EVIDENCE.zip` with SHA-256 `d65ea4657287eb8df7ed2743aec8d3f6ad7407b3e294eb4cae825454d8979787`.

The analyzer path validator was corrected before the valid campaign, a regression test was added, the source was committed, and the entire package/binding/QA/preflight/gate sequence was rebuilt from the new clean HEAD. This was execution infrastructure repair only; preregistered hypotheses, ontology, contrasts, thresholds, horizons, replication, and decision rules were unchanged.

## Post-outcome descriptive helpers

Two posthoc reporting attempts failed and remain recorded under `invalid_posthoc_attempts/`. Neither helper participated in the frozen analyzer decision. The first compared an intentionally different upstream state hash in the P-clamp control; the second had a report-rendering string error. The corrected helper only generated descriptive reports after `SITC_PASS`; it did not change criteria or campaign artifacts.

## Scientific campaign

Campaign 001 had exactly six registered launches and no retry. No failed or partial scientific run was replaced.
