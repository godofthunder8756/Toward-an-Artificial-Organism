# CNA delta review: gru_own_error_audit_spec_v1_2.md

2026-10-21, ~8:30 PM ET. A new file; nothing existing was edited. No checkpoint was loaded and nothing was run, apart from the check script and one bits-only rank script.

**Target:** `gru_own_error_audit_spec_v1_2.md`, sha256 `8c81d32070ba12ef94af7adbc3d224661ae4c76ddacb7239d170564e2eb4fdcd` (verified).

**Also verified:**
- v1 `c0fad75a…` and v1.1 `4661a889…` are unchanged.
- The roster is `7ad145b4…`, and erratum c32 is `4a5ad4f3…`.
- The check script is `ac7b752a…`. I re-ran it and it reports 0 failures.
- The constants files are `d2a1735e…` (script) and `430d56c9…` (output). The values are R_oracle 0.582388, Var_w(q) 0.167612, floor 0.00582388 and R²-gain floor 0.034746, which matches §7.
- My scratch script is `/workspace/scratch/gru_v12_delta/rank_check.py`, sha `61a3e4243c45a897253022a3351c19c0f8aac6248faff6a775d5a11f9a64811d`. It uses the input bits only.

## Verdict
**OK to go to Astra's quick check, with one disclosure edit (M1) before the freeze.** There are no blockers.

## Resolved (checked against my pending list)
- E32-1 to E32-10 and the §9 ceiling are quoted verbatim, and the script checks them.
- q is the fitted target, and d̂ is constructed from it. C1 and C2 are nested, using the same targets, folds, weights and Eval_f.
- The floor is labelled with L96 and L106 verbatim. The prior exposure (the 7·10⁻⁴ CAND s100 value) is disclosed.
- T is descriptive only. The brackets are reported separately, there is no "double dissociation" wording, and τ_fq and 2√s are not used.
- All of the §7 blockers are resolved:
  - ridge objective and unpenalized intercept;
  - λ rule, fixed in advance and using the fit set only;
  - zero-variance rule;
  - rank and conditioning reported for every fit;
  - three float64 replay tiers, with SOURCE-REPLAY UNAVAILABLE labelling and denominators kept;
  - 8/10 verified minimum, with UNRESOLVED below it;
  - S0 wording;
  - §12 provenance.
- The f_init and R-FIX wording follows L141–L142.
- The Q1 correction is credited and AC|BD is descriptive.
- PR #5 is recorded verbatim per L133.
- The pair counts (910+30+30+30 = 1000, and 45×23 = 1035) and the 23 (PR, arm) units check out.
- The rank pattern is independently reproduced. In AB and CD, r1r3 is constant; in AC and BD, r0r2 is constant. Ranks are 28/35, and 33/36 in AD and BC.
- On caps: the wall-clock cap binds on a single pinned CPU, so the 50 CPU-min brief is also met. I agree.

## M1: the B_in+ baseline cannot be identified on the held-out groups (disclosure edit, extends Q4)
The rank deficiency is more than a conditioning footnote. Its effect on held-out prediction was measured from the bits only:

| folds | share of held-out centered B_in+ row norm outside the fit-set row space |
|---|---|
| AB, CD, AC, BD | 0.632 |
| AD, BC | 0.408 |

No linear decoder fit on the fit set can use those directions on held-out histories, whatever λ is. For example, where r0r2 is fixed in the fit set, r0 and r2 are collinear there. The minimum-norm split of their coefficients then cancels on held-out histories, where the sign of r0r2 flips.

STATE is a nonlinear function of the history. It comes from predictors trained on source TRAIN histories, which E32-9 says are not held out from the predictor. So STATE can supply exactly those directions.

The consequence is that part of any C2 gain may come from the baseline's lack of identifiability under orbit holdout, not from hidden state carrying information the inputs lack.

The claim ceiling ("beyond the specified ... input baselines", "under the declared analysis") still holds. But §5 and §12 should state this as an outcome-blind pre-freeze disclosure, with the 0.632 and 0.408 figures. The report should not describe C2 as "beyond the information in the inputs".

Optional, for Astra: add, as a descriptive output, an input-only B_in+ → q held-out loss per fold. This needs no checkpoint and would make the size of the baseline handicap visible. Whether to compute it before the freeze is Astra's call, because §12 currently lists q-decoding as not yet computed.

## M2: the inner λ folds are easier than the outer task (extends Q3)
Each depth-4 group contains 2 depth-5 orbits that share all of its depth-4 prefixes. For example, (p,0) and (p⊕5,1) fall in one orbit, while (p,1) and (p⊕5,0) fall in the other.

So the held-out orbit in each inner fold shares depth-4 prefixes with the inner fit set, whereas the outer folds share none. Inner validation therefore rewards less regularization than the outer task does.

This is outcome-blind and allowed, but the λ rule is a mismatched proxy and should be described that way, not as tuned for the outer generalization. Astra should choose between:
- (a) keeping it as written, with that description;
- (b) the inherited fixed λ = 10⁻³;
- (c) leave-one-depth-4-group-out inside the fit set. This mirrors the outer split, but it leaves only 64-history inner fits, where r0r2 and r1r3 are both constant.

I lean toward (b) as the primary, with (a) as a descriptive sensitivity. It removes one of the Delegate's own unanchored rules. This is not a blocker.

## Minor
- m1. §10 assumes ~30 µs of overhead per SVD, which is optimistic for Python-level fits. Even at 10× that (~300 µs), the ~4.2·10⁵ SVDs add only about 2 minutes, which leaves the cap comfortably met. No change is needed; this note is for the record.
- m2. §6 says "any tier (ii) failure makes the block UNRESOLVED". A tier (ii) mismatch should be reported with its value and the field compared. If the manifest later shows a field-map error, that is a manifest correction before the freeze, never after.
- m3. Q1/Q2 readings: I agree that the (PR, arm) unit is the natural reading of L110 and L223, and that 8/10 carries no inferential weight. This is for Astra to confirm.
