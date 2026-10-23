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
