# N1 / N2 reference-only checks for acquired_self_correctness_spec_v1: results v1

Recorded: 2026-10-21, about 5:05 PM ET (America/New_York). Additive record. Spec v1 (sha256 `54bc8ea3b050551095bcc4d2b93fbc62476e52eb1678b08bdd37b6c1cfc0c8ac`) and all earlier files are unchanged. No repo changes. No learner, no network, no GRU code and no training. N3 was skipped. No C4 or consciousness claim.

## 1. Approval record (STEP 0)

- Path: `/workspace/review/PI_STANDING_APPROVAL_2026-10-21_1515.md`
- sha256: `5cc6f12a91d09c274a03a7c4045b4a15302f694d8f2ce056ab8a30ea5f15a7ba`. This matches the value the Specialist gave.
- PI wording (verbatim): "I'm approving everything you deem necessary as Research Lead" (Aidan Ahern, message t38u, 3:15 PM ET).
- Application line (verbatim): "Application 2026-10-21 ~4:55 PM ET: the Research Lead judges reference-only checks N1 (support-mass enumeration) and N2 (checking profitability and contrast at PROPOSED costs) for acquired_self_correctness_spec_v1 (sha256 54bc8ea3...) necessary. Limits: no learner and no training, one CPU, 4 GB, at most 15 min each, at most one 60 s smoke test each, and costs fixed at PROPOSED values. N3 is deferred."
- Scope judgment: the record covers N1 and N2.
- Provenance caveats:
  - The record file's mtime is 4:56 PM ET, so it was transcribed after the fact.
  - The 3:15 PM wording is independently corroborated by `c4_reliability_APPROVAL_ADDENDUM_A3_D1.md` (recorded 3:16 PM, sha `47fd381e…`) and by A3_D2 (`1f715813…`).
  - The record's own stated conditions include "every study is frozen before it runs and reviewed by Astra". N1/N2 are pre-freeze reference checks, not the study itself. They were run on that reading, with the scripts hash-frozen before execution (`PRE_RUN_FREEZE.txt`).

## 2. Commands, limits and resources

Each command ran through `run_measured.py` as: `taskset -c 0 prlimit --as=4294967296 timeout <cap> python3 <script>`, with OMP/OPENBLAS/MKL/NUMEXPR_NUM_THREADS=1.

`/usr/bin/time` is not installed, and installing it was refused (no root). `run_measured.py` records the equivalent fields instead: wall time, user and sys CPU, and max RSS from `getrusage(RUSAGE_CHILDREN)`.

| Invocation | Cap | Wall (s) | User CPU (s) | Max RSS (kB) | Exit |
| --- | --- | --- | --- | --- | --- |
| N1 smoke (`n1_support.py --smoke`) | 60 s | 0.073 | 0.059 | 12,856 | 0 |
| N1 primary (`n1_support.py`) | 900 s | 1.412 | 1.398 | 12,252 | 0 |
| N2 smoke (`n2_reference.py --smoke`) | 60 s | 2.455 | 2.448 | 19,392 | 0 |
| N2 primary (`n2_reference.py`) | 900 s | 28.106 | 27.962 | 94,444 | 0 |
| N2 post-processing (`n2_postproc_values.py`) | 60 s | 0.025 | 0.022 | 11,236 | 0 |

The cumulative total was about 32 s of wall time, with peak memory under 95 MB.

**Disclosed defect.** In `n2_reference.py`, `rollout()` overwrote the loop variable `r`. That makes the `value_optimal` / `value_always_predict` fields in `N2_output.json` INVALID. The action-rate fields are unaffected. `n2_postproc_values.py` was hash-recorded after the primary run and adds the corrected values from the stored stage-1 Q-values. Nothing was rerun or replaced.

## 3. File hashes (sha256)

| File | sha256 |
| --- | --- |
| acq_model.py | ccc11aec35c86b604c9f15dd0d8002f592bfcc3d5b847e771cb70edaaa2fd4d1 |
| n1_support.py | d07ae413d6cc8f077d4819d008fd6d3bedb7cfe46700e5c2801a88d5bf056394 |
| n2_reference.py | 6ff3ba85fd82f1e5e977964e8d4291ef595cc95395fc8116e50694791582b40c |
| n2_postproc_values.py | 065ab5f4a1ade0f8e5af7d97d266b83ac05a2cdc3b25c7d792c38348092fad1d |
| run_measured.py | 25e5ef9450e7c03be6a75254de6b61b30e7428568c5265b2eca37774e267ccf7 |
| N1_output.json | c7d9c91200db462a742e82dc9930bd22679fce55e83706a69bfc7f257033eff5 |
| N2_output.json | 3bbd5f6624f1c5d623e564788052a7f29d22ce34481afca85d4425c212ae8605 |
| N2_postproc_values.json | 2e957280ce00f0400dc70424a4425df74ece73e708f854782be777d638950964 |
| N1_primary.stdout.txt | 1bcda26d48d0e98f78f3d721319cf7e44e4eab3c037e691bc7a19e6d076e53ce |
| N2_primary.stdout.txt | 57989e5944c2d3cd5441918e71a484d9bff1531bf44b42f08374b666194e2431 |

The smoke outputs, resource JSONs and `PRE_RUN_FREEZE.txt` are in the same folder.

## 4. N1 results: support and split masses (exact rationals)

**Verdict: PASS on every support event, with two documentation discrepancies.** 67 checks passed and 2 failed. Both failures are the §6.3 weight-normalization discrepancy, not support failures.

| Event (per split, both S_E and S_I) | Exact mass | Samples | World H | Hand table | Thresholds (i)–(iv) |
| --- | --- | --- | --- | --- | --- |
| stage-2 after RECHECK, DIS | 35/768 | 180 | 6 | matches | PASS |
| stage-2 after RECHECK, CON | 349/768 | 42 | 6 | matches | PASS |
| K3: DIS × forced RECHECK × ỹ₃ | 35/768 | 1,080 | 6 | matches | PASS |
| K3: CON × forced RECHECK × ỹ₃ | 349/768 | 222 | 6 | matches | PASS |
| decoder S_I, stages 1–3 | 1/2 per stage | 65,394 | 342 | matches (count now exact) | PASS (iv ≥ 72) |

Also confirmed exactly:
- World histories 12 / 84 / 588 and samples 84 / 3,108 / 127,596, all with positive weight.
- Split masses of exactly 1/2 at every stage, within each cue and per action prefix.
- P(DIS | H) = 35/384 for all 12 stage-2-after-RECHECK world histories.
- 22,620 received histories in the compiled domain.

Discrepancies with the spec text:
1. **§6.3 prefix weight 4^{−(k−1)} does not normalize.** Summed over the 2^{k−1} prefixes it gives 1/2 at stage 2 and 1/4 at stage 3. The spec says "weighted uniformly", which would be 2^{−(k−1)}. This changes how stages are pooled in CF1 and K1.
2. **"Samples" counts (H, ρ) pairs, not distinct learner states.** There are only **12 distinct CON and 60 distinct DIS received recipient states**, and those same states appear in both splits. A split by world history therefore does not give disjoint learner states. This bears on review finding M/§5 and on the held-out claim of K1.

## 5. N2 results: reference profitability and contrast at costs (1/100, 3/50)

The reference is R-HIST: exact Bayes over the received history, using the world and fault laws, with full DP to K_max = 3. The oracle is world-model Bayes on clean samples. All PROPOSED v1 values were used unchanged.

### 5.1 Checking profitability (§12.4 a)

- **Expected checks per episode under R-HIST's optimal policy** (exact): RECHECK 44353/884736 ≈ 0.0501, RESAMPLE 676981/1179648 ≈ 0.574.
- **Value of the optimal policy** (from post-processing): 71317153/94371840 ≈ 0.7557, against 183/256 ≈ 0.7148 for always predicting. The gain is ≈ 0.0409.
- **Optimal action over decision-stage received histories:** P 1,058, R 400, S 426.
- **Stage 1:**
  - RESAMPLE is optimal for received ỹ₁ ∈ {2,3,4,5} under lo and {3,4} under hi.
  - RECHECK has positive Q-gain at lo ỹ ∈ {2,…,5} (+0.0239, +0.1976) and hi ỹ ∈ {3,4} (+0.0696), but RESAMPLE is larger in every one of those cases.
  - So **P(first action = RECHECK) = 0 for all 12 stage-1 world histories.**
- **§12.4(a) as written** requires a positive optimal RECHECK rate on some stage-1 world history: **FAIL for RECHECK, PASS for RESAMPLE.** RECHECK is profitable and chosen only at stages 2–3.

### 5.2 Contrast (§10.3, §12.4 b) and the B1 independent check

Stage 2 after RECHECK, under v1 definitions, with R-HIST in the learner role:

| Quantity | CON | DIS |
| --- | --- | --- |
| m̄_PREDICT, all | 1105/1536 | 1105/1536 |
| m̄_PREDICT, S_E | 19921/27648 | 19921/27648 |
| m̄_PREDICT, S_I | 19859/27648 | 19859/27648 |
| m̄_RECHECK / m̄_RESAMPLE, all | 8905/12288 / 228859/294912 | identical |

- **m̄_PREDICT(CON) − m̄_PREDICT(DIS) = 0 exactly**, in both splits and pooled, for every action. So |Δ| ≥ μ_contrast = 1/100 fails.
- **B1: CONFIRMS.** The cause is algebraic: P(DIS | H) = 35/384 for every H (N1), and m_a is a function of H alone. The equality therefore holds for any learner, not only R-HIST.
- The donor vectors are **not** identical. The L1 distance between R-HIST posterior class means is 576/349, and mean P(F=1 | received) is 61/349 for CON against 1 for DIS. The content differs; the v1 target cannot register it.

### 5.3 Directional signs for R-HIST's own quantities (§12.4 c)

- Self-assessed correctness: CON 1017/1396 against DIS 22/35, a difference of +4883/48860 ≈ +0.0999.
- Checking rate at stage 2: DIS 14/15 against CON 553/1396, a difference of +11249/20940 ≈ +0.537.
- **The signs hold** in the predicted directions. But under v1 the K2/K3 precondition is NOT EVALUABLE [NO INTERVENTION CONTRAST], so **the reference conjunction is not attainable under v1 as written.**

### 5.4 CF1a attainability with R-HIST as the learner

| Split | D_div (4^{−(k−1)}, as written) | D_div (2^{−(k−1)}, normalized) | M_div |
| --- | --- | --- | --- |
| S_E | 0.01491 | 0.01442 | 0 |
| S_I | 0.01553 | 0.01486 | 0 |

- **CF1a fails for the reference.** D_div < 1/20, and no history has |m − o| ≥ 1/20.
- Fault exposure alone yields ≈ 0.015, so CF1a could be met only through a learner's own suboptimality. This is a diagnostic, not a learner result.

### 5.5 Appendix A (binary world), exact

- **Hand numbers: CONFIRMED.** p_lo = 17/20, p_hi = 27/40. One RECHECK and one RESAMPLE each leave accuracy unchanged (17/20 and 27/40), which confirms the lemma. Two RECHECKs give 139/160 = 0.86875 and 219/320 = 0.684375, gains of 3/160 and 3/320, both below 2c_R.
- **Appendix A conclusion "the reference never checks": CONTRADICTED.** With an adaptive policy, the stage-1 lo Q_RECHECK = 549/640 ≈ 0.8578 > 17/20, so RECHECK is optimal for both lo reads. Checking is optimal at 18 binary decision-stage histories.
- The appendix compared non-adaptive two-RECHECK totals only. The binary-rejection rationale must be restated, for example as "the single-read lemma removes myopic value" rather than "never checks".

## 6. Implications for spec v2 (for Astra; nothing here changes v1)

1. **B1 is blocking and confirmed exactly.** With m on world-observable H, K2/K3 are NOT EVALUABLE for every seed and for the reference. Redefining the target or the classes is a v2 decision for Astra. I did not compute any redefined m.
2. **§12.4(a) wording versus result.** RECHECK is never the first-stage choice at (1/100, 3/50), but it is chosen at later stages. v2 should either restate (a) as "some decision stage" or treat this as a design finding. Costs were not tuned.
3. **CF1a.** The fault law produces only ≈ 0.015 RMS divergence for an optimal learner, below δ_div = 1/20, and no history reaches 1/20. Either δ_div, the fault strength or the CF1a construction needs a v2 ruling.
4. **Fix the §6.3 weight** to 2^{−(k−1)}, or state the intended weighting.
5. **Held-out claim.** The 12/60 distinct recipient states are shared across splits. v2 should define the K1/K2 held-out unit and support minimums over distinct received states.
6. **Appendix A.** Keep the arithmetic and correct the "never checks" sentence.
7. **Supports.** All N1 events pass, so no support redesign is needed for the v1 event definitions.
