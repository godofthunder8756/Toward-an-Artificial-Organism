# Reproducibility modes and claim limits

**Version:** `1.0-rc2`  
**Reserved DOI:** `10.5281/zenodo.22863692`  
**Publication state:** not uploaded; not published

This document separates four operations that answer different questions. A successful operation in one row must not be reported as completion of a stronger row.

| Mode | Primary question | Required inputs | What the RC2 package supports | What success establishes | What success does not establish |
|---|---|---|---|---|---|
| 1. Normalized evidence verification | Are the public hashes, normalized 88-case projection, compact campaign summaries, and scoring rules mutually consistent? | Extracted RC2 package; Python 3.10+ | Directly supported by `code/public_verify.py` | Integrity and re-scoring of the public normalized evidence within the declared public scope | Execution of the mechanism; inspection of six historical raw arrays; replay of process provenance; historical reconstruction; independent replication |
| 2. Public reference execution | Does the packaged transparent reference construction, run now, produce a normalized result matching the public projection? | Extracted RC2 package; Python 3.10+; writable new output directory | Directly supported by `code/run_public_reference.py` | A new execution of the public reference construction and comparison with the frozen normalized projection | Replay of the historical command path, OS process evidence, timestamps, or exact historical environment |
| 3. Independent fresh rerun | Can a separate investigator or environment independently execute and audit the public reference construction? | RC2 package plus an actually independent operator/environment and preserved rerun outputs | Enabled by the package, but not created merely by packaging or by the author's own rerun | External reproducibility of the public reference construction to the extent documented by the independent runner | Independent validation of broad theory, spontaneous selfhood, population inference, or historical reconstruction |
| 4. Historical reconstruction | Can the accepted historical campaign be rebuilt and checked from its original raw outputs, process records, command binding, and environment? | All six omitted historical raw arrays; full process-provenance records; exact command binding; full frozen environment; all hash-bound freeze artifacts | Not supported by this compact public package | Nothing unless all required historical inputs are supplied and pass their original gates | Mode 1, 2, or 3 success cannot substitute for this mode |

## Mode 1: normalized evidence verification

Run:

```text
python /path/to/PACKAGE_ROOT/code/public_verify.py
```

The verifier must fail closed on missing or mismatched public inputs. A pass means that the declared preregistration, freeze receipt, analysis summary, normalized projection, and compact six-run summary records satisfy the published integrity and scoring checks. Its receipt must explicitly state:

- the reference construction was not executed;
- the six historical raw arrays were not loaded;
- historical process provenance was not replayed; and
- the historical campaign was not reconstructed.

## Mode 2: public reference execution

Run:

```text
python /path/to/PACKAGE_ROOT/code/run_public_reference.py --output reference_output
```

This launches six new workers in the registered forward/reversed sequence and uses prospective run nonces. The newly created result is a public-reference execution. It is not one of the historical campaign runs and must receive its own output directory, receipt, hashes, environment record, and timestamp.

## Mode 3: independent fresh rerun

Independence is a property of who or what executes and audits the package, not a flag emitted by the code. A fresh run qualifies only when the rerun report identifies the separate operator or environment, preserves exact package identity, records the commands and interpreter, and reports deviations. A matching normalized hash establishes external reproducibility of this engineered finite reference implementation. It does not convert deterministic re-execution into a population-level statistical replication.

## Mode 4: historical reconstruction

The RC2 deposit intentionally omits the six large historical raw arrays and portions of the internal campaign infrastructure. It also withholds the exact D0 architecture bytes because they contain unpublished cross-project material. Consequently, the compact deposit cannot independently re-establish the complete historical campaign. Hashes and project-issued receipts preserve identity claims about omitted objects; they are not substitutes for publishing and loading those objects.

## Quantitative unit warning

Across six accepted deterministic executions, the campaign recorded 528 case instances and 1,752 trace endpoints. Each endpoint was read 256 times without state mutation, yielding 448,512 stored probe records. Treating those records as 448,512 independent observations would be pseudoreplication. The six same-implementation executions test deterministic reproducibility plus order/token invariance; they are not six independent scientific replications.

## Claim boundary

> In the registered finite construction, a relationally self-indexed temporal state causally influenced future-directed choice through the separately intervened prospective-evaluation path.

All four modes remain bounded by this exact claim. None establishes phenomenal consciousness, sentience, subjective experience, personhood, life, AGI, human-equivalent selfhood, spontaneous self-model emergence, or architectural novelty.
