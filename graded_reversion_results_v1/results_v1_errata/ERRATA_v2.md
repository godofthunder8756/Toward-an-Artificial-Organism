# Errata v2

Additive notes for the graded joint recurrent reversion phase B report. Attributed to Astra consult #16 (2026-10-21, about 12:55 AM ET). No existing file is modified. No label is changed. No network was trained and no evaluation was rerun.

The counts in E-B3 were recomputed from the committed `phase_b_results.json`. The corrected reading is `../PHASE_B_RESULTS_v3.md`. E-B1 and E-B2 remain in `ERRATA_v1.md` and `../PHASE_B_RESULTS_v2.md`. The original report remains `../PHASE_B_RESULTS.md`.

## E-B3. Directional margins

Primary target `weight_hh`. Margin is `AUC_REV` minus the largest of the 32 random-path AUCs, taken from the stored `D_margin`. The relative margin divides that difference by the largest random-path AUC. A passing seed is one whose stored joint flag is true (seeds 201–209). A thin margin is a passing seed whose relative margin is below 0.10.

At alpha = 1, excess loss is `delta_L_prefix`. Every path has the same alpha = 0 baseline, so the same comparison on `L_prefix` selects the same seeds. An endpoint directional pass uses the frozen rule: the reversion endpoint excess exceeds the largest random endpoint excess by more than eps0 (1e-12).

| seed | joint | AUC_REV | max random AUC | margin | margin/max random AUC | thin margin | alpha=1 rev excess | alpha=1 max random excess | random exceeds rev | endpoint directional |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 200 | false | 0.005148719367 | 0.007231463092 | -0.002082743725 | -0.288011 | no | 0.01003712907 | 0.01814027194 | yes | no |
| 201 | true | 0.003925281173 | 0.003281668182 | 0.0006436129911 | 0.196124 | no | 0.008739229539 | 0.009678902671 | yes | no |
| 202 | true | 0.004728781362 | 0.004659221587 | 6.955977415e-05 | 0.014929 | yes | 0.01018162326 | 0.01395088224 | yes | no |
| 203 | true | 0.005613930148 | 0.003653093918 | 0.00196083623 | 0.536760 | no | 0.01145759407 | 0.01097191832 | no | yes |
| 204 | true | 0.005993524643 | 0.005099530801 | 0.0008939938419 | 0.175309 | no | 0.01192876023 | 0.01581097967 | yes | no |
| 205 | true | 0.006243345304 | 0.003811052191 | 0.002432293114 | 0.638221 | no | 0.01178295799 | 0.01086141445 | no | yes |
| 206 | true | 0.004681302994 | 0.004330601813 | 0.0003507011814 | 0.080982 | yes | 0.009795116571 | 0.01254550922 | yes | no |
| 207 | true | 0.005176810334 | 0.003865639176 | 0.001311171158 | 0.339186 | no | 0.01094648036 | 0.01086090402 | no | yes |
| 208 | true | 0.005168081041 | 0.004855587129 | 0.0003124939118 | 0.064358 | yes | 0.01049349887 | 0.01218311881 | yes | no |
| 209 | true | 0.005876473218 | 0.005526569338 | 0.0003499038801 | 0.063313 | yes | 0.01229177895 | 0.0160354408 | yes | no |

Four of the nine passing seeds are thin: 202, 206, 208, and 209. At alpha = 1, at least one random path has greater excess loss than reversion in seeds 200, 201, 202, 204, 206, 208, and 209 (7/10). An endpoint-only directional comparison passes in seeds 203, 205, and 207 (3/10).

Four of nine passing seeds exceed the most damaging sampled random path by less than 10% of that path's AUC. At alpha = 1, at least one sampled random path causes greater loss than reversion in 7/10 seeds. The preregistered directional criterion concerns trapezoidal AUC over the dose grid; an endpoint-only directional comparison would pass in 3/10 seeds. These descriptive findings do not change the frozen labels.

## E-B4. Ledger qualifier

Support is relative to the 32 prespecified block-norm-matched random paths. Directional margins are small in several passing seeds; robustness to additional draws or stronger control families is untested.

## E-B5. Scope of what the replicated label licenses

"Beyond matched random perturbation" means the dose-averaged trapezoidal AUC over the specified path. It does not mean every dose, the endpoint, or arbitrary perturbations.

The earned claim is:

In W2, the trained hidden-to-hidden parameters make a bounded causal contribution to accurate prefix-dependent prediction under the specified continuation-stage intervention and fixed surrounding computation. In 9/10 fresh seeds, reversion produced greater dose-averaged excess prefix-function loss than each of 32 prespecified block-norm-matched random paths and met the declared materiality threshold.

This does not replace the frozen claim paragraph and does not change the frozen label. It is not selectivity, not an XOR-specific effect, not localized content, and not a uniquely identified mechanism.

## E-B6. Single blocks

The primary effect was not reproduced by any single block at the declared criterion.

This does not support an inference that single blocks carry nothing, that the effect is distributed, or that n explains the joint result.

## E-B7. Approval provenance

The approval file is unchanged.

The approval recorded at 10:38 PM ET on 2026-10-20 answered widget t20s2: 'Approve fresh-seed GRU-8 training for the graded reversion confirmation once Astra clears the protocol?' Aidan answered: 'Yes, approve it once Astra clears it.' This approval applied to Phase B of this study; Appendix A remained unapproved and was not run.

## Ledger

Q-CAUSE organization level SUPPORTED, BOUNDED (+E-B4). Q-NECESSITY and C-levels unchanged. No C4. No consciousness claim.

This note does not edit the protocol ledger. Q-NECESSITY stays NOT_ESTABLISHED. C-levels stay where the frozen protocol left them.
