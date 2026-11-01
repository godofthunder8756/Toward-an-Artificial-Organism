# N1 / N2 reference-only checks for acquired_self_correctness_spec_v2: results v2

Recorded: 2026-10-21, about 5:18 PM ET (America/New_York). This is an additive record.
- Spec v2: sha256 `babe6423d2dadfd424427a827a00296049c695487e7966883ee0601956168cf6`.
- v1, its review, the v1 N1/N2 records and the repo are unchanged.
- There was no learner, no network and no training. N3 was skipped. No C4 or consciousness claim.

## 1. Authority and freeze

- **Authority.** Same record as v1: `/workspace/review/PI_STANDING_APPROVAL_2026-10-21_1515.md` (sha256 `5cc6f12a…`). The after-the-fact caveat in `../N1_N2_results_v1.md` §1 and `../v1_DESIGN_LABEL.md` applies here too.
- **Freeze record:** `PRE_RUN_FREEZE_v2.txt` (sha256 `da717ac17be907c1fc34c1d5f12e4e990f1aacdc731e43f418e53262529b206d`).
  - Part 1, written at 17:08:35 EDT before any v2 computation, records the C-K0 criterion text and its hand algebra.
  - Part 2, written at 17:15:20 EDT, records the hashes of spec v2, the v2 check script and the four v2 scripts. It also records the declaration that N2 v2 evaluates only two worlds: PRIMARY κ₀ = 1/16 and DIAGNOSTIC κ₀ = 0.

## 2. Commands and resources

Each command was run as `run_measured_v2.py <log> <cap> python3 <script>` → `taskset -c 0 prlimit --as=4294967296 timeout <cap> …`, with the OMP/OPENBLAS/MKL/NUMEXPR thread counts set to 1. `/usr/bin/time` is not installed, so the wrapper reports wall time, user/sys CPU and max RSS from `getrusage`.

| Invocation | Cap | Wall (s) | User CPU (s) | Max RSS (kB) | Exit |
| --- | --- | --- | --- | --- | --- |
| N1 v2 smoke | 60 s | 0.047 | 0.035 | 13,176 | 0 |
| N1 v2 primary | 900 s | 3.705 | 3.571 | 98,340 | 0 |
| N2 v2 smoke | 60 s | 0.994 | 0.981 | 18,568 | 0 |
| N2 v2 primary | 900 s | 11.140 | 11.090 | 96,960 | 0 |

The cumulative total was about 16 s.

## 3. Hashes (sha256)

| File | sha256 |
| --- | --- |
| acq_model_v2.py | 8fd03549cc66a864552864be92114f2a1117c34cbe9a1db3f310359022ea5a5b |
| n1_support_v2.py | 1c2bdbcb90f6a37917ede68011d10b02a45aa34ac11403a3cdaca75831fd5215 |
| n2_reference_v2.py | 15a1f6cd4005aeb69f93c0d27c8c05416d530f880f0f0fb7b8fbc9c497df6727 |
| run_measured_v2.py | 25e5ef9450e7c03be6a75254de6b61b30e7428568c5265b2eca37774e267ccf7 |
| N1_v2_output.json | 7a718310d6e28f7ffe7be44456192bea874224b523defc341e1bf890d71a6c7d |
| N2_v2_output.json | 6ad3af7d29f0413cff3f94e035025c008bd6896d28464e22db1bc44832f854f4 |
| N1_v2_primary.stdout.txt | 087057853a4dff084e91cab69d3ca15657f3898e42b17c2fd665c597443cc1a3 |
| N2_v2_primary.stdout.txt | a95671f1ffeff41a2a3b2d4ed2ea7d8799ad6728a6912156915da8c7d7270535 |

**Cross-validation.** The DIAGNOSTIC world (κ₀ = 0) reproduces every v1 reference value that does not depend on the target definition, exactly. These are E[#RECHECK] 44353/884736, E[#RESAMPLE] 676981/1179648, the optimal value 71317153/94371840 (equal to the v1 post-processing value), always-predict 183/256, the self-assessment gap 4883/48860 and the checking gap 11249/20940.

## 4. N1 v2: supports on distinct learner states (κ₀ = 1/16)

**Verdict: PASS. 82 of 82 checks passed, and every exact value matches the spec v2 hand algebra.**

Confirmed exactly:
- Every one of the 22,620 received states has positive mass, including under F = 0 alone.
- Stage counts are 12 / 144 / 1,728 / 20,736.
- The split on R carries exactly 1/2 of the mass in every stage, prefix and cue. The 2^−(k−1) weight normalizes.
- P(F=1 | DIS) = 112/205 and P(F=1 | CON) = 976/5119.

Per event and per split (S_E and S_I are identical):

| Event | Mass | Distinct states | States per cue (lo, hi) | (i) mass ≥ 1/100 | (ii) ≥ 4 states, ≥ 1 per cue |
| --- | --- | --- | --- | --- | --- |
| stage 2 (FIRST, RECHECK), DIS | 1025/12288 | 30 | (15, 15) | PASS | PASS |
| stage 2 (FIRST, RECHECK), CON | 5119/12288 | 6 | (3, 3) | PASS | PASS |
| K3 DIS × forced RECHECK × ỹ₃ | 1025/12288 | 180 | (90, 90) | PASS | PASS |
| K3 CON × forced RECHECK × ỹ₃ | 5119/12288 | 36 | (18, 18) | PASS | PASS |
| decoder S_I, stages 1–3 | 1/2 per stage | 942 (6 + 72 + 864) | (471, 471) | — | (iii) ≥ 38: PASS |

**Note for Astra.** CON has only 6 distinct recipient states per split, 3 per cue. That meets the declared minimum of 4 but is thin for class means and for the random-donor population.

## 5. N2 v2 results (costs 1/100, 3/50; φ = 1/4, κ = 1/4; exact rationals)

### 5.1 B1 check: class means of m_PREDICT on R (R-HIST as the learner)

| World | m̄_P CON | m̄_P DIS | CON − DIS | ≥ μ_contrast = 1/100? |
| --- | --- | --- | --- | --- |
| PRIMARY κ₀ = 1/16 | 14913/20476 | 652/1025 | **1935473/20987900 ≈ 0.0922** | yes |
| DIAG κ₀ = 0 | 1017/1396 | 22/35 | 4883/48860 ≈ 0.0999 | yes |

- **B1 is resolved.** The contrast is nonzero with m on R, in both worlds, in both splits and pooled. It was exactly 0 under v1's target on H.
- **Signs (§12.4 c):**
  - Checking at stage 2 is higher after DIS: 14/15 against 8113/20476, a gap of 164969/307140 ≈ 0.537 (PRIMARY).
  - Self-assessment is higher after CON.
- **Donor vectors** are non-identical: L1 = 746496/1049395 (PRIMARY).

### 5.2 §12.4(a) under both readings

| World | Stage-1 reading (RECHECK / RESAMPLE) | Some-decision-stage reading | E[#RECHECK], E[#RESAMPLE] per episode | Value: optimal vs always-predict |
| --- | --- | --- | --- | --- |
| PRIMARY κ₀ = 1/16 | **holds / holds** | holds | 386357621/452984832 ≈ 0.853, 45384857/75497472 ≈ 0.601 | 90311421197/120795955200 ≈ 0.7476 vs 721/1024 ≈ 0.7041 |
| DIAG κ₀ = 0 | **fails** (RECHECK never first) / holds | holds | ≈ 0.0501, ≈ 0.574 | ≈ 0.7557 vs 183/256 |

**PRIMARY stage-1 detail:**
- RECHECK is optimal for the extreme reads: lo ỹ ∈ {1, 6} and hi ỹ ∈ {1, 2, 5, 6}. The gains are small, +0.0099 at lo and +0.0012 to +0.0016 at hi. With κ₀ > 0, an extreme read is worth re-checking for a processing fault.
- RESAMPLE is optimal for the middle reads.
- So §12.4(a) holds under both readings in the PROPOSED world.

This is a finding about the v2 world, not a ruling. **Which reading applies stays OPEN for Astra (Q-A12).**

### 5.3 CF1a recomputed on R, with the m − o decomposition (room item 2)

- For R-HIST as the learner, m = o^R, so the learner-specific term λ is 0 identically. All of m − o is fault exposure Δ^F = o^R − o.
- The S_E and S_I values are identical: the R-parity split pairs each state with its y ↦ 7−y mirror image.

| Quantity | v1: target on H (from v1 N2) | DIAG κ₀ = 0, target on R | PRIMARY κ₀ = 1/16, target on R |
| --- | --- | --- | --- |
| D (RMS divergence), S_E | 0.0144 (2^−(k−1)) / 0.0149 (4^−(k−1)) | **0.0232** | **0.0327** |
| M (mass with \|Δ\| ≥ 1/20), S_E | 0 | 47607/1048576 ≈ 0.0454 | 51301387/452984832 ≈ 0.1133 |
| Mean signed Δ^F (P, R, S) | — | (−0.0127, −0.0086, −0.0143) | (−0.0215, −0.0136, −0.0241) |
| CF1a at δ_div = ν_div = 1/20 | fail | **fail** (D < 1/20, M < 1/20) | **fail on D** (0.0327 < 1/20); M passes |

- **CNA's suspicion is partly confirmed.** Moving the target from H to R, in the same world, raises D from about 0.0144 to 0.0232 and M from 0 to about 0.045. The v1 number was depressed by the same marginalization behind B1.
- κ₀ = 1/16 raises D further, to 0.0327, and M to 0.113.
- **CF1a still fails, on the RMS criterion D^F ≥ 1/20.**
- This is reported as a finding. δ_div, ν_div and the fault strength (φ, κ) were not changed. **They stay OPEN for Astra (Q-A13).** No other world was evaluated.

## 6. Verdicts

- **N1 v2: PASS.** All supports on distinct learner states meet the v2 minimums. All hand masses and counts are exact.
- **N2 v2: PASS on B1, contrast, signs, donors and §12.4(a) under both readings. FAIL on CF1a** (D^F ≈ 0.0327 < δ_div = 1/20). The spec v2 Stage 0 rule (§1.1, §12.5) would give `DESIGN NOT ADMITTED (CF1a: fault exposure below threshold)` at the PROPOSED thresholds.

## 7. Implications for v3 (for Astra; nothing is changed here)

1. **Q-A13 is now the binding question.** Choose δ_div, or the fault strength (φ, κ), or redefine D^F (for example pooled versus per-action RMS), by a criterion that does not look at these numbers. Alternatively, accept that the PROPOSED world does not exercise the motivating question at the declared threshold.
2. **Mirror symmetry of the R-parity split.** Every S_E state has a mirror twin in S_I (y ↦ 7−y with Y relabelled), with identical reference statistics. Held-out generalization is therefore partly mirror generalization. Astra may want a split that breaks the symmetry; this would be a new open question.
3. **CON support is thin:** 6 states per split.
4. With κ₀ > 0, stage-1 RECHECK appears for extreme reads. Q-A12 matters less in the PROPOSED world but stays open.
