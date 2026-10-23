Consult #34 - RESULTS INTERPRETATION: GRU oracle-accessibility audit v1.3 FINAL (spec sha d5a91932...), run under your #33 FREEZE WITH NAMED EDITS (E33-1..10). Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

Records: Draft PR #12 https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/12 , branch cursor/gru-oracle-audit-v1-3-0097. Commits: c9314671 (sealed inputs); 124f60cd (freeze; manifest 72137e29, committed 8 s before the first checkpoint load per SEALING_ORDER_EVIDENCE.md); 7987a720 (results); 88c96f9c (the 11 predecessor files committed byte-identical); 51b5e79f (deviation resolution: 112/112 spec-consistency re-run, output sha 66f763d6, plus REPORT_ERRATA_1).

Run facts: 26.4 s wall-clock, 1 CPU. All 290 checkpoints (230 TRAINED + 60 INIT) passed integrity. 40 PR #8/#9 records are labelled "SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED". PR #5: NOT EVALUATED (missing persisted checkpoints).

Outcome: all 23 (PR, arm) units have m=0, b=10, x=0, u=0, i=0 (quota not attained). C1 meets the floor in 89/230 checkpoints; C2 in 0/230. No BOUNDARY cases. Input-only B_in+ -> q pooled held-out loss (lambda=1e-3) = 0.016543.

Post-run reviews (verbatim below, hashes verified):
(A) Research Delegate results review, sha 398e9220...: CONFIRMED WITH NOTES. All counts recompute exactly.
(B) Constitutive agent (CNA) adversarial read, sha 3f30ccda...
(C) CNA erratum to (B), sha ef478fe6..., accepting the Delegate's corrections.

Key points:
- R1 feasibility: since Delta <= L(base), meeting the floor (0.005824) was arithmetically impossible for 7 units (PR #7-#9 cand_final and f_trained; PR #10 CAND; 70 checkpoints), whose pooled L(base) is below the floor in both C1 and C2 (R_exc 6.8e-4 to 2.9e-3, near-oracle). The other 16 units were floor-feasible for every checkpoint. v1.3 had no feasibility requirement; this was foreseeable from the disclosed ~7e-4 excess and every reviewer missed it.
- R2: all 89 C1 passes are in feasible, poor arms (median R_exc 0.0443). C2 median gain 7.4e-6, max 0.00446 (< floor), state hurts (Delta<0) in 107/230.
- The M1 "cuts both ways" argument is withdrawn as an unverified conditional conjecture.
- The Delegate's in-bounds rewrites of two CNA sentences and its draft additive interpretation note are in (A) Sec.5-6.

Questions:
(1) Is this bounded reading correct? "In the 16 feasible units, no prespecified-margin gain beyond the declared input baselines under this split at lambda=1e-3; the 7 near-oracle units were floor-infeasible and uninformative."
(2) How should the feasibility gap be recorded additively without changing labels? (Rule on the Delegate's draft note in (A) Sec.6.)
(3) Does this close the GRU own-error / oracle-accessibility line? If not, what is the single most informative next study toward the program goal, within Aidan's standing approval (freeze-first, Astra-reviewed, 1-CPU-scale unless justified, no consciousness claims)? Flag anything needing a human gate.
(4) Give any errata and verbatim close-out wording (CLOSE-OUT text for the record, and a claim ceiling).


===== FILE: review/gru_audit_v1_3_results_review_RD.md (verbatim) =====
# Research Delegate results review: GRU oracle-accessibility audit v1.3 (PR #12)

2026-10-21, ~11:15 PM ET. New file and additive. READ-ONLY review: no training, no checkpoint load, no inference, no re-run of the audit. All numbers below are arithmetic on committed result files at commit `7987a720` (extracted with `git archive` to `/workspace/scratch/pr12`; `/workspace/repo` working tree untouched beyond `git fetch`). Scratch scripts: `/workspace/scratch/gru_results_review/recompute_v1.py`, `feasibility_v1.py`.

**Verdict: CONFIRMED WITH NOTES.** Every count, label and combination recomputes exactly from the committed per-checkpoint values under the frozen rules. No discrepancy in any decision-bearing quantity. Notes are wording (LOW), report rendering (LOW), and one interpretive gap the spec did not anticipate (floor infeasibility for 7 units; MEDIUM, labels unchanged).

## Records verified
- Spec `gru_own_error_audit_spec_v1_3.md` sha256 `d5a91932…d103`: local copy, PR copy and `results.json.spec_sha256` all match.
- Roster `7ad145b4…cab3`: local, PR and results.json match. Roster ids/roles/PR/seed/arm equal the 230 TRAINED + 60 INIT result records exactly (set-equal, field-equal).
- Manifest `72137e29…c741`: matches results.json and summary.json. All 13 `code_files` hashes in the manifest match the committed code. `git diff 124f60cd 7987a720` touches no code, manifest, review or scratch file (results only).
- Commit order (UTC → ET): c9314671 02:34:04Z (10:34 PM ET), 124f60cd 02:51:29Z (10:51 PM ET), 7987a720 02:53:34Z (10:53 PM ET). Manifest sealed in the commit before results; ~2 min gap is consistent with the 26.4 s run. **That no checkpoint was loaded before 124f60cd is UNVERIFIED from git alone** (commit order is consistent with it; `run_audit.py` refuses to start without the manifest and checks the replay map against it, but does not re-hash code files at start-up).

## 1. Counts (§8, E33-5)
- Recomputed C1/C2 labels from pooled Δ with floor and ±1e-10 band (§7), the F5 combination (§8), and m/b/x/u/i plus quota rule (§8 items 1–4) for all 230 TRAINED records: **0 mismatches** vs `results.json` labels/decisions, and `results.json.units` == `summary.json.units` == my recomputation.
- 23 units (14 PR #7, 3 each PR #8/#9/#10), each exactly 10 seeds (PR #7 s100–109, #8 s200–209, #9 s300–309, #10 s400–409). All 23: m=0, b=10, x=0, u=0, i=0 → "quota is not attained" (rule 3: verified=10 ≥ 8, m < 8, m+u+i=0 < 8). **CONFIRMED.**
- C1 meets-floor: **89/230** (141 below). C2 meets-floor: **0/230** (230 below). **CONFIRMED.** No BOUNDARY: nearest |Δ_C1 − floor| = 1.2e-5 (≫ 1e-10); max Δ_C2 − floor = −1.36e-3.
- Internal arithmetic: Δ = L(base) − L(full) bit-exact for all; R² gain = Δ/Var_w(q) to ≤1e-15; pooled L reproduces from foldwise values × eval-fold masses / 3 (max err 1.4e-17; eval masses sum to 3.000 as E32-7 requires); AC|BD reproduces from its two folds with denominator 1·Σw (0 mismatches).
- All compared values finite. Integrity: 290/290 status ok, 0 mismatches, numpy-vs-torch max-abs ≤ 2.2e-15 (≤ 1e-10, §6 iii), d̂-identity worst excess −1.0e-12 (passes E33-8 form). PR-level: 10/10 verified seeds for each PR.
- 40 PR #8/#9 cand_final + cand_init records carry exactly "SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED" (20 TRAINED, 20 INIT); all others "source-metric replay" (§6, E33-6). PR #5 printed as "MISSING PERSISTED CHECKPOINTS; NOT EVALUATED" (§1). PR #10 CAND-init = R-FIX-32-init identical for all 10 seeds and kept as provenance (E32-8).
- Note (INFO): tier (ii) passing residuals are not recorded, only pass/fail. §6 requires values only for mismatches, so this is compliant, but replay magnitudes are **UNVERIFIED** by me.

## 2. F5 combination (§8, flag F5)
`ridge.py` `combine`: below if either below; meets only if both meet; else BOUNDARY — identical to §8. Manifest note F5 records it. BOUNDARY never contributes to m (`accounting.py`). Recomputed independently: identical. **CONFIRMED.**

## 3. Floor, band, manifest notes (§7, §5, §9; CNA n1/n2)
- `domain.py` derives R_oracle, Var_w(q), floor = float(R/100), R²-floor in exact rationals, asserts R+Var = 3/4, and refuses to run unless the reprs equal the §7 strings. results.json: R_oracle 0.5823877685694766, Var_w(q) 0.16761223143052342, floor 0.005823877685694766, R²-floor 0.034746137772820054 — exact §7 values. (Float `0.01*R_oracle` would give 0.0058238776856947665, 1 ulp off; the code correctly does not do that; no label within 1e-5 of the floor in any case.)
- Band: `delta > floor+1e-10` meets, `< floor−1e-10` below, else BOUNDARY (§7, E33-7). **CONFIRMED.**
- n1: single rule `VAR_MAX = 1e-24` used for §5 feature exclusion, §9 T target variance and correlations (`domain.py`, `ridge.py`, `metrics.py`, `run_audit.py`). **Implemented.**
- n2: all 230 uniform records have `r2_denominator: "uniform-weight Var(q)"`, `floor_label: null`; R² = Δ/0.1484798733339353 exactly. **Implemented.**
- LOW (display): REPORT.md prints Var_w(q) = 0.1676122314305234 and R²-floor = 0.03474613777282005, which are not the same float64 as the §7 values (results.json holds the correct ones and governs; §7 says display values are never used in code). Suggest the report print `repr()` values.

## 4. Excess-Brier and descriptive reporting (§2, §4, §5, §8, §9)
- R_exc(P) is given for every TRAINED checkpoint in REPORT.md next to L(base)/L(full), on the pooled scale, labelled descriptive/not a gate (§2, L79). INIT R_exc is in results.json.
- LOW (rendering): the 60 INIT sections in REPORT.md are **empty headers**; their values (C1/C2, R_exc, integrity) exist only in results.json. REPORT.md says results.json "is part of this report", so nothing is lost, but the INIT tier is not human-readable in the report.
- T: 6105 records = 2035 pairs × 3 feature types; 1000 + 1035 = 2035 pairs (§9); all status ok; fixed λ (code line 546). Descriptive wording matches E32-5.
- λ: `PRIMARY_LAMBDA` used for primary C1/C2, input-only, uniform and T. Inner-λ: 230 TRAINED only, `label`/`floor_label` null, difference-from-fixed-λ reported (§5, E33-2). Report states "mismatched validation geometry… No direction of bias… asserted" (E33-3). **CONFIRMED.**
- AC|BD reported separately, "(no floor label)", not used in labels (§3, §8). **CONFIRMED.**
- Input-only B_in+→q: λ = 1e-3, per fold + pooled 0.016543465191148552, rank-deficient flags (rank 28 in AB/CD/AC/BD, excluded r1r3/r0r2 as §5 predicts), "not described as outcome-blind" sentence present (E33-4). **CONFIRMED.**

## 5. Wording (§0, §4, §13a)
REPORT.md: no sentence exceeds §13a. It states C2 "beyond the declared input baselines under this split" (E33-1), "improvement under this feature-and-regularization procedure" (E33-9), quota descriptive with 56/1024 not a p-value, claim ceiling not applied. No reading of C2 as "state carries nothing beyond inputs"; no out-of-scope status terms. PR body: same, plus two LOW items:
- "No (PR, seed) block is UNRESOLVED." §0 retires "block". → "No (PR, seed) integrity unit is UNRESOLVED." (The Specialist's room post also says "No block is UNRESOLVED"; same fix.)
- "The audit is complete: S0, P, D, and the report all finished inside the caps." Literally true under §10/E33-10 (nothing INCOMPLETE), but the pre-freeze 112/112 re-check was a stopped item. → "All scheduled stages (S0, P, D, report) completed inside the caps; nothing is INCOMPLETE. The pre-freeze consistency re-check is a recorded deviation (see below)."
Neither changes a label.

On CNA's adversarial read (`3f30ccda…`), wording only:
- "Read descriptively, the state holds input information that the output has thrown away." Goes beyond decoder accessibility (attributes a mechanism). → "For these 89, adding STATE to B_conf reduced held-out q loss by more than the floor; this is decoder accessibility beyond the output baseline only."
- "This fits E33-9 (shrinkage) and extrapolation noise, not a hidden signal." "not a hidden signal" is a negative claim the design cannot support. → "This is consistent with E33-9 shrinkage effects; no gain by the prespecified margin was shown beyond the declared input baselines under this split."
- The M1 "cuts both ways" argument rests on a conditional ("If the state encodes, say, r0 and r2 roughly linearly"); the state is a nonlinear function of the bits and need not be collinear on the fit groups. **UNVERIFIED**; the conclusion CNA draws from it ("cannot be read as the state lacks the information, nor dismissed as a handicap artefact") is in bounds on its own.
CNA's "Supportable reading" and "Not supportable" bullets are inside §13a and E33-1.

## 6. CNA R1/R2 verification (floor feasibility)
Since L(full) ≥ 0, Δ ≤ L(base); meets-floor requires L(base) > floor + 1e-10 = 0.0058238777857. Per unit (10 checkpoints each; ranges of pooled L(base)):

| PR | arm | C1 L(base) | C2 L(base) | infeasible C1 / C2 / either | C1 meets | R_exc |
|---|---|---|---|---|---|---|
| 7 | cand_final | 0.000809–0.00255 | 0.00188–0.00454 | 10/10/10 | 0 | 0.000838–0.00282 |
| 7 | f_trained | 0.00112–0.00275 | 0.00195–0.00420 | 10/10/10 | 0 | 0.00113–0.00291 |
| 8 | cand_final | 0.000871–0.00249 | 0.00253–0.00374 | 10/10/10 | 0 | 0.000898–0.00258 |
| 8 | f_trained | 0.000978–0.00249 | 0.00234–0.00448 | 10/10/10 | 0 | 0.000965–0.00253 |
| 9 | cand_final | 0.000815–0.00125 | 0.00254–0.00360 | 10/10/10 | 0 | 0.000886–0.00129 |
| 9 | f_trained | 0.000870–0.00142 | 0.00253–0.00331 | 10/10/10 | 0 | 0.000954–0.00139 |
| 10 | CAND | 0.000664–0.00212 | 0.00216–0.00354 | 10/10/10 | 0 | 0.000677–0.00222 |
| 7 | f_init | 0.0235–0.0366 | 0.0131–0.0198 | 0/0/0 | 10 | 0.0328–0.0587 |
| 7 | f_tuned32 | 0.0272–0.0346 | 0.0147–0.0167 | 0/0/0 | 7 | 0.0299–0.0423 |
| 7 | r_tuned843 | 0.0267–0.0333 | 0.0142–0.0176 | 0/0/0 | 6 | 0.0286–0.0406 |
| 7 | sel_g0.5_b-2.0 | 0.0264–0.0297 | 0.0147–0.0154 | 0/0/0 | 0 | 0.0410–0.0482 |
| 7 | sel_g0.5_b0.0 | 0.0217–0.0351 | 0.0136–0.0194 | 0/0/0 | 8 | 0.0298–0.0538 |
| 7 | sel_g0.5_b2.0 | 0.0367–0.0800 | 0.0166–0.0436 | 0/0/0 | 5 | 0.0486–0.0860 |
| 7 | sel_g1.0_b-2.0 | 0.0272–0.0285 | 0.0139–0.0156 | 0/0/0 | 0 | 0.0369–0.0451 |
| 7 | sel_g1.0_b0.0 | 0.0231–0.0359 | 0.0140–0.0199 | 0/0/0 | 8 | 0.0300–0.0545 |
| 7 | sel_g1.0_b2.0 | 0.0354–0.0813 | 0.0151–0.0373 | 0/0/0 | 6 | 0.0468–0.0847 |
| 7 | sel_g2.0_b-2.0 | 0.0256–0.0322 | 0.0140–0.0167 | 0/0/0 | 5 | 0.0276–0.0402 |
| 7 | sel_g2.0_b0.0 | 0.0251–0.0383 | 0.0159–0.0203 | 0/0/0 | 9 | 0.0305–0.0546 |
| 7 | sel_g2.0_b2.0 | 0.0347–0.0763 | 0.0158–0.0685 | 0/0/0 | 6 | 0.0465–0.0871 |
| 8 | f_init | 0.0252–0.0398 | 0.0139–0.0393 | 0/0/0 | 9 | 0.0369–0.0599 |
| 9 | f_init | 0.0236–0.0479 | 0.0146–0.0210 | 0/0/0 | 10 | 0.0349–0.0627 |
| 10 | R-FIX-32 | 0.00687–0.0153 | 0.00682–0.0162 | 0/0/0 | 0 | 0.00755–0.0181 |
| 10 | R-FIX-48 | 0.00708–0.0124 | 0.00645–0.0261 | 0/0/0 | 0 | 0.00749–0.0132 |

- **R1 CONFIRMED:** 70 checkpoints = exactly the 7 named units, 10/10 each, infeasible in both C1 and C2; no unit is mixed. The other 16 units (160 checkpoints) are feasible in both comparisons for every checkpoint. Feasibility is necessary, not sufficient (Δ ≤ L(base) only).
- Small corrections to CNA: R_exc for the infeasible units spans 6.8e-4 to 2.9e-3 (CNA: "about 7·10⁻⁴ to 2·10⁻³"). In R2, "the sel_* arms (5 to 9 each)" is inexact: sel_g0.5_b-2.0 and sel_g1.0_b-2.0 have 0 C1 meets; the others have 5–9. R-FIX-32/48 are feasible but have 0 C1 meets.
- **R2 CONFIRMED:** the 89 C1 meets all lie in feasible units (0 in the 7); median R_exc 0.0443; median C2 L(base) 0.01639 vs input-only pooled 0.01654; median C1 L(full) 0.02114, and C1 L(full) > C2 L(base) for 81/89. C2 over 230: median Δ 7.38e-6, max 0.004464 (in a feasible checkpoint, < floor), Δ < 0 for 107/230. (C1: median Δ 3.47e-3, Δ < 0 for 9/230.)
- **Did v1.3 anticipate feasibility reporting?** No. v1.3 has no feasibility, power or "L(base) vs floor" requirement anywhere (§4, §7, §8). §12 disclosed the ~7·10⁻⁴ PR #7 s100 CAND TRAIN excess, which is already below 0.01·R_oracle, so the infeasibility was foreseeable from disclosed information. I wrote v1.3 and also missed it; recording that here alongside CNA's own note. §7 and #32 L106 fix the floor ("Do not change it after seeing the new decoding results"), so labels must stay as they are.
- **Suggested additive interpretation note (labels unchanged; for Astra to rule on):** "For 70 TRAINED checkpoints forming 7 (PR, arm) units (PR #7–#9 cand_final and f_trained; PR #10 CAND), pooled L(base) is below the floor in both C1 and C2, so meets-floor was arithmetically unattainable under the frozen absolute floor. Their b=10 records carry no information about decoder accessibility at this floor. For the other 16 units, every checkpoint was floor-feasible; no checkpoint met the floor in C2, so no unit showed improvement by the prespecified margin beyond the declared input baselines under this split at fixed λ = 1e-3. This note changes no label, count or quota outcome; any floor relative to L(base) would be a new protocol." This keeps Q-EXIST/Q-LEARN/Q-CAUSE/Q-NECESSITY untouched: it is a statement about the test's reach, not about the predictors.

## 7. Deviation: predecessor files for the 112/112 check (§14)
`check_gru_audit_spec_v1_3.py` (`7a496e4e…`) hashes 18 absolute paths (`/workspace/…`) and does one `git show` against `/workspace/repo`. Already in PR #12: Astra #33, PI standing approval, roster, inventory.py, prefreeze_constants_v1_2.py/.json, rank_check.py. **Absent from PR #12 (11 files):**
- `/workspace/astra_consult32_response.txt` (`99378f76…`)
- `review/gru_own_error_audit_spec_v1.md` (`c0fad75a…`), `_v1_1.md` (`4661a889…`), `_v1_2.md` (`8c81d320…`)
- `review/gru_own_error_audit_spec_v1_2_delta_review.md` (`e8f28370…`), `_spec_v1_review.md` (`f6b2db6f…`), `_spec_v1_1_review_addendum.md` (`721100d1…`), `_review_erratum_c32.md` (`4a5ad4f3…`)
- `scratch/gru_audit/check_gru_audit_spec.py` (`d2449113…`), `_v1_1.py` (`e25a403a…`), `_v1_2.py` (`ac7b752a…`)
Plus a non-file dependency: `git -C /workspace/repo show origin/pr/10:twostream_results_v1/results.json` (W2 certificate, `bf2de92c…`). The cloud run's repo root was `/workspace` (`run_frozen.sh` does `cd /workspace`), so a `/workspace/repo` clone with an `origin/pr/10` ref also has to exist there.

**Local re-run** (pure spec-consistency check; no checkpoint, no inference, no q-decoding), against the /workspace copies: **112 PASS, 0 FAIL**, output sha256 `66f763d6eaf7a831b2b3904b458aee9f572af534a9bad1916f99372419aaa82a`, byte-identical to the pre-freeze recorded output (`66f763d6…`). Saved at `/workspace/scratch/gru_results_review/check_v1_3_rerun_output.txt`.

**Would committing them additively resolve it?** Partly. Committing the 11 files byte-identical in a new commit at those paths (repo-root `astra_consult32_response.txt`, `review/…`, `scratch/gru_audit/…`) supplies every hashed file. It touches nothing sealed: none of the 11 is listed in the manifest (`code_files` lists only `audit/…`), none is already in the repo, and no frozen file is edited. The re-run also needs the `origin/pr/10` certificate ref available at `/workspace/repo` in the run environment, or a run from a layout like this box's. The cleanest resolution is an additive "deviation resolution" note that records (a) the 11 files committed byte-identical with their sha256 values, (b) the environment used for the re-run, and (c) the 112/112 output hash `66f763d6…`, with the original deviation file left in place. Either way the deviation does not affect any audit rule or result. (Committing to the repo is a write and needs approval; not done here.)

## Findings summary
| # | severity | finding |
|---|---|---|
| 1 | — | Counts, 89/230, 0/230, unit outcomes, F5, floor, band, n1, n2, λ, AC\|BD, input-only: all recompute exactly. |
| 2 | MEDIUM (interpretation) | 7 units / 70 checkpoints floor-infeasible (CNA R1 confirmed). Spec did not require feasibility reporting. Add an interpretation note; labels unchanged. |
| 3 | LOW | PR body/room "block" wording (§0); "audit is complete" should mention the stopped re-check. |
| 4 | LOW | REPORT.md: 60 INIT sections are empty headers; displayed Var_w(q) and R²-floor are not round-trip float values (JSON correct). |
| 5 | LOW | CNA read: two sentences exceed §13a (rewrites above); M1 symmetry argument UNVERIFIED. |
| 6 | INFO | Sealing before checkpoint load: consistent with commit order, UNVERIFIED from git alone. Tier (ii) pass residuals not recorded (compliant). |
| 7 | INFO | Deviation: 11 predecessor files plus a PR #10 git ref. Local re-run 112/112, `66f763d6…`. Additive commit plus the ref resolves it without touching sealed files. |

===== FILE: review/gru_audit_v1_3_results_adversarial_read.md (verbatim) =====
# CNA adversarial read: GRU oracle-accessibility audit v1.3 results (PR #12)

2026-10-21, ~11:10 PM ET. A new file; nothing was run. I read the PR #12 branch `cursor/gru-oracle-audit-v1-3-0097` at commit 7987a72, specifically `results/results.json`, `summary.json` and `REPORT.md`. Everything below is arithmetic on those recorded values.

**Records match.** The spec (`d5a91932…`), roster (`7ad145b4…`) and manifest (`72137e29…`) hashes in results.json match. The constants are the exact-rational values, and the zero-variance rule is Var ≤ 1e-24, which matches my note n1.

## R1: the floor could not be reached for 70 of the 230 checkpoints (7 of the 23 units). The labels are correct; how they are read must change.
Δ_c = L(base) − L(full), and L(full) ≥ 0, so Δ_c ≤ L(base). For 70 checkpoints, L(base) is below the floor (0.005824) in **both** C1 and C2:

| PR | arms |
|---|---|
| #7 | cand_final, f_trained |
| #8 | cand_final, f_trained |
| #9 | cand_final, f_trained |
| #10 | CAND |

That is 10 of 10 checkpoints in each of those arms. Their R_exc is about 7·10⁻⁴ to 2·10⁻³, so the predictor is already close to the oracle. Their b=10 was therefore arithmetically guaranteed whatever the hidden state contains. Those 7 units carry no information about state accessibility at this floor.

This was foreseeable before the freeze. The disclosed 7·10⁻⁴ CAND s100 excess is already below 0.01·R_oracle. I missed it in the v1 review, the v1.2 delta review and the v1.3 spot-check. This is my error, and I am recording it here.

The spec rules hold, and nothing should be relabelled. The interpretation, though, should separate the **floor-infeasible units (7)** from the **floor-feasible units (16)**.

## R2: C1 yes and C2 no do not mean the state adds nothing beyond the inputs
- **C1 meets-floor: 89 checkpoints, all in floor-feasible arms.** These are PR #7 f_init (10/10), PR #8 f_init (9), PR #9 f_init (10), and PR #7 f_tuned32, r_tuned843 and the sel_* arms (5 to 9 each). For these 89, median R_exc is 0.044, so their outputs are poor. Read descriptively, the state holds input information that the output has thrown away.
- **For those same 89, the C2 base is roughly the input-only decoder.** Median C2 L(base) is 0.0164, against an input-only pooled loss of 0.0165. C1 L(full), with median 0.0211, is **worse** than C2 L(base). So state plus confidence decodes q less well than inputs plus confidence.
- **C2 overall.** Median Δ is 8·10⁻⁶, the maximum is 0.0045, which is below the floor, and Δ < 0 for 107 of 230 checkpoints. Adding state is about as likely to hurt as to help. This fits E33-9 (shrinkage) and extrapolation noise, not a hidden signal.
- **The M1 split limitation does not explain the null.** Under this split it cuts both ways:
  - The baseline cannot use directions that are not identified on the fit groups, which would have favoured STATE.
  - The STATE decoder is also linear and fitted on the same two groups. If the state encodes, say, r0 and r2 roughly linearly, those components are collinear on the fit set just as r0 and r2 are, so the same identifiability limit applies.
  - So the null cannot be read as "the state lacks the information", nor can it be dismissed as a handicap artefact.
- **Supportable reading (for Astra).** In the 16 floor-feasible units, no checkpoint showed improvement by the prespecified margin beyond the declared input baselines under this split, at fixed λ = 1e-3. In the 7 floor-infeasible units, the primary label is uninformative. The claim ceiling is not reached in either case.
- **Not supportable.** "Hidden state contains nothing beyond the inputs", or any statement about other splits, decoders or λ values.
- **One more point.** The input-only per-fold losses are strongly asymmetric: 0.0087 for AB→CD against 0.0279 for CD→AB, and the other pairs are similar. The pooled residual mostly reflects which groups are fitted. That is descriptive only.

## R3: 26 s runtime is plausible
The stage times were S0 3.5 s, P 3.4 s, D 19.6 s and report <0.01 s, with CPU 27.2 s and wall 26.4 s. That is consistent with one pinned CPU plus some interpreter overhead.

The output counts match the full roster:
- 230 TRAINED and 60 INIT checkpoints;
- inner 230;
- uniform 230;
- T 6105, which is 2035 pairs × 3 feature types;
- correlations 2035;
- variation 290.

Implied cost per SVD:
- P: ~7,000 SVDs at ≤128×50 in about 3.4 s, roughly 0.5 ms each including feature building and scoring.
- D: ~110,000 SVDs in about 19.6 s, roughly 0.18 ms each, mostly small (p ≤ 15).

My paper estimate of 0.6 to 4.9 min was deliberately conservative. Spot values look sane: PR7/s100/cand_final R_exc is 9.0·10⁻⁴, close to the 7·10⁻⁴ TRAIN-only figure disclosed earlier, and the numpy-vs-torch maximum is 4.4·10⁻¹⁶. The deviation affects only re-execution of the check script and touches no rule.

## Recommendation for the Astra consult
Ask Astra to rule on reporting R1 as a disclosed, foreseeable floor-infeasibility, with the 7 and 16 units listed separately. The labels stay unchanged and there is no post-hoc floor.

Ask also whether the R2 reading above stays within §13a.

No new analysis is proposed. Any infeasibility-aware floor, such as one relative to L(base), would be a new protocol needing separate approval.

===== FILE: review/gru_audit_v1_3_results_adversarial_read_erratum.md (verbatim) =====
# CNA erratum to the adversarial read of the GRU audit v1.3 results (`3f30ccda…`)

2026-10-21, ~11:05 PM ET. This is a new file; the original is not edited. It accepts the corrections in the Delegate's review `398e9220…`.

1. **R1 range.** For the 7 floor-infeasible units, R_exc runs from 6.8·10⁻⁴ to 2.9·10⁻³, not "about 7·10⁻⁴ to 2·10⁻³". The infeasibility conclusion is unchanged.
2. **R2 C1 counts.** Two sel_* arms have 0 C1 passes, not "5 to 9 each".
3. **Withdrawn wording that goes beyond §13a:**
   - "the state holds input information that the output has thrown away";
   - "not a hidden signal".

   The Delegate's in-bounds rewrites replace them.
4. **The "cuts both ways" argument is a conditional conjecture, not a result.** It holds only if the state encodes the collinear readings approximately linearly. It is withdrawn as support for any reading. The bounded statement stands without it: in the 16 floor-feasible units, no prespecified-margin gain was found beyond the declared input baselines under this split at λ = 1e-3, and nothing is claimed about the information content of the state.

===== END OF CONSULT #34 =====
