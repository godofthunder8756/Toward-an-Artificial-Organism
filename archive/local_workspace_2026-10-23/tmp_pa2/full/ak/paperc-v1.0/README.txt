Paper C v1.0 — Measure the Instrument First
Author: Akiyama Satoshi (independent researcher). License: CC-BY-4.0.

PAPERC_V1_0_EN.pdf / .md   primary manuscript (English)
PAPERC_V1_0_JA.pdf / .md   Japanese companion
figures/                   figure PNG/SVG, figure data (from frozen raw), manifest
primary/                   preregistration V5 (+seal, novelty), stage-3 freeze manifest, 261-row raw, result,
                           both prediction tickets + seal, disclosure obligation/classification, claim-evidence
code/                      core, runner, guard, aggregator, fixtures, freezer, two independent recomputations, figure generator, builders
receipts/                  reviews, recomputation receipts, incident and amendment records, visual QA
MANIFEST.json              SHA-256 of every file

Reproduce the tables: python code/fable_paperc_independent_recompute_v1.py (needs primary/INSTRUMENT0_STAGE5_RAW_V1.jsonl beside it)
                      or node code/paperc_independent_recompute_v1.mjs
