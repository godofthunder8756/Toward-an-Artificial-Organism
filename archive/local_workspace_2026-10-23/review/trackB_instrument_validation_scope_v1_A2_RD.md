# Track B instrument-validation scope v1: Amendment A2 (additive; RD)
- **Amends:** v1 `7b9bf34d7b4c10c8c2a7063aa6177d94e888fbbe76f78d0cd33afbe0c905c56a` and A1 `8572152647a03524365675a24f254dc33ed4af67f091aee9762a23ff18bb9c99`. Both are unchanged.
- **Source:** CNA's light pass, 2026-10-23, about 10:39 ET.
- **Status:** DRAFT, NOT FROZEN, NOTHING RUNS.

## A2-1. CNA erratum cited
The scope cites `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1_erratum1.md` (sha256 `41c1a414e27239d5763736d35562b79e25c33d53f29d42198de39effb4debcc5`) alongside CNA's section `377f99ba…`. The erratum remaps four uses of UNAVAILABLE in that section (L44, L60, L71, L108). Confound-row labels are PASS, FAIL and CONFOUND NOT REALIZED only.

## A2-2. AQ-C2 confirmed by CNA, with one rule added
RAND-INIT is reported only under Q-EXIST. It is pass/fail under Q-LEARN and under ignition claimed as learned.

**New rule:** a Q-EXIST MET obtained while RAND-INIT is realized may never be described as acquired or learned.

## A2-3. P3 restored
A1-3 replaced v1 P1–P4 and left out P3. P3 is restored as an open pre-freeze item: repeat the OpenAlex and Semantic Scholar lookups, which were rate-limited in CNA's v1 pass. Its owner is CNA.

## A2-4. Open items: one place to look
The open items are listed in A1-3 (F1–F5) plus P3. CNA's v1.2 note in progress covers F1–F4. F5 (the Zenodo and Registered Reports searches) and P3 stay open until they are filed.
