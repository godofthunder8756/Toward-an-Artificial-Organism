# Results review: class-fit attempt 2, PR #14 (Research Delegate)

**Status:** review record only. It establishes no result.

- **Reviewed at:** HEAD `cffe125bf50b9e16db36e071981a0642827c041e`. Written 2026-10-23, about 10:20 ET.
- **How I worked:** read-only. Nothing was rerun, and no package code was executed. All arithmetic below is Python on the stored JSON numbers.
- **Scope (split):** code paths, stop/exit, and label derivation. CNA has scope, hashes and manifest, so I do hashes only lightly.

## Verdict: CONFIRMED WITH NOTES

## 0. Light hash pass

| File | sha256 |
|---|---|
| `classfit_outputs/results.json` | `05385099c4f0b4a0ca0c71302abe42eabb4673d83f2f6c5236f6286cb82bfdd2` ✓ |
| `classfit_outputs/REPORT.md` | `c755e5eaceed928c626f306d7efc21146b79f805fd62250d1d27017f283ea5db` ✓ |
| `classfit_post_run_index.json` | `4552b79426f73c8a9ff4bf1373e0f715aa737df69d1d66aa53af94a88edad79d` ✓ |
| `classfit_manifest.json` | `e7a9d3a49b0a41cf0570536a12fff5133e9b9baf1f0adf8c6c9ff03cf2991234` ✓ |
| sealed oracle `outputs/results.json` | `6adb5de2…` (equals `pinned.py:150ff`, `ORACLE_SEALED_OUTPUT_SHA256`) |

## 1. Stop and exit

- **Stop kind.** `stop_kind.json` reads `{"exit_code": 0, "stop_kind": "COMPLETED"}`. The last line of `run.log` reads `125.321281 stop COMPLETED exit 0`. `results.json`: `.stop_kind` is "COMPLETED", `.exit_code` is 0, `.detail` is `{}`. The index has `exit_status` 0 and `incomplete` false.
- **Nothing suppressed.**
  - Every `labels[*].first_failing_reason` is null, and `VALIDATION.first_failing_reason` is null.
  - S1, S2 and S4 are each `status: "PASS"`, with no "FAIL" string in any of them:
    - S1 (`stage_S1_O1.json`): `mismatch_count` 0;
    - S2 (O2): max abs diff 2.03e-10 against tolerance 1e-8;
    - S4 (P0).
  - The JSON outputs contain no NaN or Infinity.
  - `aggregate.py:342–347` would print a stop kind into every label row. It did not.
- **Closure.** All 189 `results.json:.accounting[]` records have `closed: true` and satisfy `sum(counts) + remaining == scheduled`.
  - Every skip count and `UNKNOWN_AFTER_LAST_DURABLE` is 0, and every `remaining` is 0.
  - **Propagations:** 3,444,240 scheduled, all attempted. That is 272 exact (S1) plus 3,443,968 float (1,536 in S2 plus 3,442,432 in S6). This matches v1.3's 3,443,968 + 272 (L519) and `.exact_propagations` 272 / `.float_propagations` 3,443,968.
  - **SVDs:** fits 421 (1 at S3 plus 420 at S5) plus 120 B3 stacks at S5 makes 541, equal to `.svd_count` 541 (v1.3 L607 and L787).
  - **Loss records:** 16,128 in total, 2,304 in each of the 7 `eval_*.json` files. This matches v1.3 L768.
  - **Pooled rows:** 336, all with `formed: true`.
  - CNA's counts are confirmed.
- **Detail counts:** `attempted_detail` sums are `value_error` 0, `non_finite` 0, `guard_invalid` 0, and `valid_finite` equal to the attempted count for all three units.
- **Voids and admissibility.** Every system has 0 voids (`stage_S3_construction.json:.systems[*].voided_prefixes == []`). SYS-NC1 has 0 voids, well below the ≥5-of-16 rule (v1.3 L791, C7.1 item 5), and every system is `admissible: true`.
- **Other measures.**
  - `crossings` is 0 for every system.
  - Coverage is 1.0 for count and for law mass in every `eval_*.json:.coverage` row (120 per system).
  - There is no UNRESOLVED-B3: the `b3_status` values in `fit_freeze_SYS-{FK,NC1,NC2,NC3}.json` are PASS or null only.
- **Timing.**
  - `.t_elapsed_s` is 125.286, under 540.
  - The projection at 0.631 s: `T_rem_s` 59.97 against `projection_limit_s` 539.37, so there was no PROJECTION HALT.
  - From `run.log`: S0–S4 finished by 0.425 s, and the seven fit freezes by 0.591 s. Each eval took about 17–19 s:

    | System | Finished at (s) |
    |---|---|
    | O6 | 18.76 |
    | PC | 37.37 |
    | FK | 56.86 |
    | NC1 | 74.31 |
    | NC2 | 91.13 |
    | NC3 | 107.98 |
    | LIM | 125.23 |

- **Memory.** In `stage_S0_preflight.json`, `vmpeak_bytes` is 60,198,912 (58,788 kB × 1024) and `vmpeak_plus_budget_bytes` is 376,935,968. That is the 316,737,056 budget plus VmPeak, as the Specialist stated ✓. The final VmPeak is 84,964 kB (`results.json:.memory_observation`).

## 2. Label derivation

### v1.3 text

- **Statistic** (C7.3, L1133): "**H = L_μ,class** for SYS-PC at ε_syn = 0.1, with √H and R = H/S, for ALL and MARG."
- **Thresholds** (L1134): "ALL √H ≥ 10⁻³ and R ≥ 0.05; MARG √H ≥ 10⁻⁴ and R ≥ 0.02 … Labels are HEADROOM NOT MET / BOUNDARY / MET under the inherited band rule (v1_4_N L15–16)." The word is **and**: MET requires *both* statistics to pass, and either clear failure gives NOT MET.
- **R wording:** "comparator squared prediction error divided by actual response energy" (C10.2, L1316).
- **Pooling** (C3.10, L801–802, "E36-5, inherited"): "Occurrences are pooled with their original w(a,u) … normalized once over the pooled scoreable occurrences."

### The code

`aggregate.py:557–578` selects SYS-PC, `fit_type == "class"`, `eps_syn == "0.1"`, `mode == "weighted"`.

`_headroom_one` (`:495–554`) works in this order:
1. Validation, then rank, coverage, formation and S = 0 gates.
2. Computes √H = sqrt(L_mu) and R = L_mu/S.
3. Clear failure (`x < t(1−1e-6)`, `:29–30`) first, giving NOT MET.
4. Then the band (`|x−t| ≤ 1e-6·t`, `:33–34`), giving BOUNDARY.
5. Otherwise MET, or AVAILABLE for MARG (RL-7).

This mirrors `ckappa_oracle/outcomes.py:17–22` and `:90–99`.

`pool_records` (`:88–157`) weights each record's L_mu and S by `law_mass_scoreable` and normalizes once. This is E36-5's pooled w-normalization, since each record is itself the w-normalized mean over its occurrences.

### Recomputation from `eval_SYS-PC.json:.loss_records`

48 records each for ALL and MARG (fit class, eps 0.1, weighted):

| | L_mu = H | S | R | √H | Threshold | Outcome |
|---|---|---|---|---|---|---|
| ALL | 4.89556152279922e-07 | 2.96924922266903e-05 | 0.016487539966074785 | 6.99682894e-4 | R 0.05, √H 1e-3 | **both clearly below → NOT MET** ✓ |
| MARG | 1.4442664459245487e-07 | 8.166569635158952e-06 | 0.0176851053801911 | 3.80035057e-4 | R 0.02, √H 1e-4 | R clearly below (ratio 0.884), √H passes (3.8×) → **NOT MET** ✓ |

- These match `results.json:.HEADROOM.{ALL,MARG}.values` exactly. `clearly_below` reads `["sqrt_H","R"]` for ALL and `["R"]` for MARG ✓.
- MARG NOT MET with √H passing is correct under the "and" rule and clear-failure-first ordering.
- No statistic lies within 1e-6 relative of its threshold. The closest is MARG R, 11.6% below.
- SYS-PC class `L_full` is 2.96e-33 for ALL and 1.68e-33 for MARG (about 1e-33, as CNA said ✓). The full predictor is exact, so H equals the measured class gain (4.896e-07), as v1.3 L892 expects.

### VALIDATION

`.VALIDATION.label` reads "CLASS-FIT VALIDATION MET". This is correct under C7.2 (L1110–1118):
- O1, O2 and P0 passed. They are mandatory and would have stopped the run.
- Every required identity is PASS:

  | System | Fit | Rows |
  |---|---|---|
  | O6 | global | 30 |
  | O6 | class | 120 |
  | PC | global | 60 |
  | PC | class | 120 |
  | FK | global | 84 |
  | FK | class | 336 |

  Source: `results.json:.labels[*].flags.identity_status`.
- Every rank category is FULL/FULL.
- Nothing is NOT EVALUATED, UNRESOLVED or NOT_APPLICABLE_RANK.

The code path is `aggregate.py:390–456`, with `_identity_label` at `:215–228`.

### Tolerances

- The largest residual-to-tolerance ratio is 7.8e-7 (`D7-CD->AB-Y` and `O6-B-class-CD->AB-Y`: 7.77e-16 against `tolerance_abs` 1e-9).
- The finite-equality identities use `tolerance_abs` 1e-9 (e.g. `eval_SYS-PC.json:.identities[0]`).
- Zero-gain identities use `1e-18 + 1e-9·S` (v1.3 L1050). The worst is NC1 at 2.5e-23 against 2.7e-16.
- Every pass is by orders of magnitude.

### D6 and D7 (RL-3)

- D6 has 6 rows, all `REPORTED`, with no PASS or FAIL. D7 has 12 rows, all PASS. Both are in `eval_SYS-LIM.json:.d6_d7` and `fit_freeze_SYS-LIM.json`.
- `.d7_investigate` is `[]`.
- `_required_identities` (`aggregate.py:200–202`) excludes D6 and D7 from the label identity sets.
- SYS-NC1–NC3 and SYS-LIM are REPORTED (`:363–364`).
- Confirmed.

### CNA point (2): weighting mode

**The mode is fixed. It is not open.**
- v1.3 C3.10 (L801–802) adopts E36-5.
- The oracle governing record `review/ckappa/ckappa_oracle_scope_record_v1_3_E36.md` says the same at L34 ("Pool evaluated occurrences using their original w(a,u) … normalize once over the pooled scoreable occurrences") and in the E36-5 row at L94.
- The inherited oracle label code uses `_pool(tables, "weighted", …)` (`ckappa_oracle/stages.py:487`).
- Unweighted records exist only because C3.6(c) (L766) asks for both modes as diagnostics.
- So the code's `mode == "weighted"` (`aggregate.py:573`) is the governed choice.

The unweighted values are stored in `results.json:.pooled` (SYS-PC class, 0.1, unweighted), so I could read them without running anything:
- **MARG:** R 0.020109810490499952 and √H 3.92e-4. Both would clear, so MARG would read AVAILABLE.
- **ALL:** R 0.01901381936019044 and √H 7.32e-4. It fails either way.

CNA's figures are confirmed. The MARG result is sensitive to the mode, which deserves a report note, but it does not change the label.

## 3. The oracle comparison (CNA point 1)

The sealed oracle `outputs/results.json:.section5.ALL.values` gives R 0.07987942230238843 and √H 1.5406e-3, with MARG R 0.0786525. That is SYS-O6 (the oracle system) with the **global** comparator.

The weighted pooled R values in `classfit results.json:.pooled` at eps 0.1, for ALL:

| System | Fit | R | Note |
|---|---|---|---|
| SYS-O6 | global | 0.07987942230238844 | equals the oracle to the last digits, so a true reproduction ✓ |
| SYS-O6 | class | 0.016625781241345363 | |
| SYS-PC | global | 0.0792154 | gain 0, as derived |
| SYS-PC | class | 0.016487539966074785 | |

So "PC class 0.0165 against oracle 0.080" compares across both system and fit type. **It is not a like-for-like comparison.**

The legitimate comparisons are within a system: O6 global 0.0799 against O6 class 0.0166, and PC global 0.0792 against PC class 0.0165. Both show that most of the oracle-scale headroom was carried by structure a class-conditioned μ map can represent. This agrees with CNA and M-1. The Specialist's wording should state the basis explicitly.

## 4. Claim ceiling

- **REPORT.md is within the ceiling.**
  - Its stored-label block matches `results.json`.
  - The success sentence is template-only and conditional. It is not asserted, because ALL is not MET.
  - It contains no GRU or checkpoint claim and no general κ claim. "No new claim is stated."
  - E38-15, E37-10, E37-3 and E37-4 appear verbatim (L1–17).
- **"Design does not proceed unchanged."** This phrase is not in REPORT.md or any committed file I searched. I could not see the Specialist's text, so its wording is **UNVERIFIED**.
  - **In:** read as a programme decision, it is within the ceiling. C7.4 (L1138) licenses a neural-specification decision only on VALIDATION MET *and* HEADROOM MET, and that condition fails.
  - **Out:** any statement that κ is unused, absent, unnecessary or irrelevant in GRUs, or any "negative result about κ".
    - The thresholds are "synthetic reporting conventions only … no neural response floor" (L1134–1137, C10).
    - The failure wording must be the REPORT.md sentence: "The declared class-conditioned-map intervention-prediction criterion was not met."

## 5. Anomalies

- No value lies at a threshold. Nothing is in the BOUNDARY band, including law mass, where all coverage is 1.0.
- No NaN, no UNRESOLVED-B3, no non-FULL rank category, no voids and no crossings.
- **SYS-LIM.** Its class R is 0.211 and its global R is 0.0799, with gain −2.39e-6. The negative gain is kept, as the record intends (#38 L94). The result is REPORTED only: it enters neither VALIDATION nor HEADROOM, and its D7 rows pass, so there is no INVESTIGATE.
- **Negative REPORTED gains.** NC1 class has gain −9.96e-9, NC3 class −2.84e-8, and FK has gains of about −1e-33 (rounding). These are retained, as v1.3 requires.
- **Minor.**
  - `stage_S1_O1.json:.val_readout_rejection` is "UNVERIFIED" while S1 is PASS. This is pre-declared and does not gate.
  - REPORT.md attributes memory to "the run.log observation", but the figures it prints come from `results.json:.memory_observation`. This is cosmetic.

## 6. Provisional NO-GO

**Supported.**
- VALIDATION is MET, so the pipeline is trustworthy for this question.
- HEADROOM ALL is clearly NOT MET on both statistics and in both weighting modes. That alone fails the C7.4 licence condition.
- MARG NOT MET is correct under the governed weighted mode.

Notes to carry forward:
- **(i)** The MARG margin is narrow and sensitive to the mode. Report it, but don't re-label.
- **(ii)** The oracle comparison must be stated within each system (O6 global against O6 class).
- **(iii)** The NO-GO is a decision not to proceed with this neural specification unchanged. It is not a scientific negative about κ or GRUs (E38-15).
