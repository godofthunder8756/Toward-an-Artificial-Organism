# Addendum A1 verification manifest

This file locks the verification code before it runs. The frozen world, thresholds and procedures are unchanged. This manifest does not retune them and does not contain the git commit that adds it.

## Scope

One bounded completion of the missing ITEM-8 replay at `T_SEP = 3`, both `K_SEP` cost pairs:

- every R-CG intervention and rescue statistic required by spec section 5.4;
- the reference C-FO check;
- a reference policy rebuilt in this process, without loading the primary policy object.

No attainability scan. No new setting. No label-rule change. Original outputs are not rewritten. Results go to `outputs/verification_A1/`.

## File

SHA256 `wrel/verification_a1.py` `f8deb34b82d7695a2a3bbf283135839c5e595d0855f1465e29eec175c95169dc`

## Exact run command

Working directory: `c4_reliability_exact_check_v1`

```text
taskset -c 0 python3 -u -m wrel.verification_a1
```

One CPU process. No GPU. Hard limit: 30 cumulative minutes of wall clock inside the process, including retries, and 8 GB resident memory. If either limit is hit, the process stops and writes the partial result it has. Exact rational arithmetic.
