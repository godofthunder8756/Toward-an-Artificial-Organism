Errata copy of `PHASE_B_RESULTS.md`, attributed to Astra consult #18. The original file is unchanged. No label is changed. No dose curve was rerun and no network was trained. See `results_v1_errata/ERRATA_v1.md`.

# Graded recurrent reversion against both first-order-matched and isotropic controls

Phase B is the confirmatory phase on fresh seeds 300-309. The denominator is 10. Phase A is not pooled with these seeds.

- Code version: first-order-control-v1
- Protocol sha256: `0efce40bdf2cf55af61f8c70f817ec3fbf8fe3a79256025556a77a03f8347101`
- Freeze commit: `335e5056f38d4d5fffc737e467b3faebe5c9a77a`
- Approval: Aidan Ahern, 2026-10-21, 1:05 AM ET, Grok Bot chat, widget t23s2.

## Verdict

**Label:** GRADED JOINT REVERSION EXCEEDS BOTH FIRST-ORDER-MATCHED AND ISOTROPIC CONTROLS (PREFIX FUNCTION): REPLICATED

In W2, in at least eight of ten fresh GRU-8 seeds, continuation-stage joint recurrent reversion produced a trapezoidal excess prefix-function loss exceeding every one of 32 first-order-matched paths and every one of 32 isotropic paths. Both families matched the reversion displacement block by block in Frobenius norm; the first-order-matched family additionally matched its initial loss derivative. The excess met the declared materiality threshold, and the intact trained cores outperformed the prefix-blind reference. This supports a bounded causal contribution under the specified intervention and fixed surrounding computation. The comparison concerns the sampled families and dose-averaged AUC; it does not identify semantic content, curvature as a mechanism, localization, necessity, or selectivity over continuation processing.

The first-order matching uses the gradient of the oracle-referenced prefix-function loss at the trained weights. It is an oracle-informed analysis control, applied after training; it is not network training and does not train the network or modify its saved checkpoint.

## Transfer replication

TRANSFER SHOWN

## Counts

D_FO: 10/10 seeds passed
D_ISO: 8/10 seeds passed
D_FO and D_ISO: 8/10 seeds passed
M: 10/10 seeds passed
joint: 8/10 seeds passed
invalid: 0/10
collapsed: 0/10
invalid or collapsed: 0/10
other eligibility failures: 0/10

Seeds that do not pass the joint rule are listed with each failed condition. A failed D_ISO is a failed isotropic comparison. A failed D_FO is a failed first-order-matched comparison. The failure is not attributed to one family unless that seed's flags say so.

| seed | valid | eligible | D_FO | D_ISO | M | joint | collapsed | reasons |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 300 | true | true | true | false | true | false | false | D_ISO failed; exactly one of 32 ISO paths had greater AUC than REV. |
| 301 | true | true | true | false | true | false | false | D_ISO failed; exactly one of 32 ISO paths had greater AUC than REV. |
| 302 | true | true | true | true | true | true | false |  |
| 303 | true | true | true | true | true | true | false |  |
| 304 | true | true | true | true | true | true | false |  |
| 305 | true | true | true | true | true | true | false |  |
| 306 | true | true | true | true | true | true | false |  |
| 307 | true | true | true | true | true | true | false |  |
| 308 | true | true | true | true | true | true | false |  |
| 309 | true | true | true | true | true | true | false |  |

Seed 300: D_ISO failed; exactly one of 32 ISO paths had greater AUC than REV. Seed 301: D_ISO failed; exactly one of 32 ISO paths had greater AUC than REV.

## Margins against both families

2 of 8 joint-passing seeds exceed the most damaging sampled first-order-matched path by less than 10% of that path's AUC (0 seeds with this percentage undefined because that family's maximum AUC is ≤ eps0). At alpha = 1, at least one sampled first-order-matched path causes strictly greater loss than reversion in 3/10 seeds, and at least one ties it within eps0 in 0/10 seeds. The preregistered directional criterion concerns trapezoidal AUC over the dose grid; an endpoint-only directional comparison against this family would pass in 7/10 seeds. These descriptive findings do not change the frozen labels.

1 of 8 joint-passing seeds exceed the most damaging sampled isotropic path by less than 10% of that path's AUC (0 seeds with this percentage undefined because that family's maximum AUC is ≤ eps0). At alpha = 1, at least one sampled isotropic path causes strictly greater loss than reversion in 5/10 seeds, and at least one ties it within eps0 in 0/10 seeds. The preregistered directional criterion concerns trapezoidal AUC over the dose grid; an endpoint-only directional comparison against this family would pass in 5/10 seeds. These descriptive findings do not change the frozen labels.

The REPLICATED label depends on at least one seed whose directional margin against at least one family is below 10% of that family's most damaging sampled path; robustness to additional draws is untested.

This result meets the prespecified threshold exactly: 8/10 seeds. Two passing seeds have a margin below 10% against at least one control family. Each failing seed is exceeded by exactly one sampled ISO path. Robustness to additional draws, alternative control families or a new seed cohort is untested.

The FO directional criterion was met more often in this cohort: 10/10 versus 8/10 for ISO. Adding FO to the joint gate excluded no additional seeds. This does not establish that FO controls are generally less demanding.

FO had a larger sampled maximum than ISO in four seeds, so "the easier family" needs that qualification.

Verification against `phase_b_results.json`: the primary maximum FO AUC exceeds the primary maximum ISO AUC in five seeds (305, 306, 307, 308, and 309), not four. The inner product ⟨G, delta⟩ is negative in nine seeds (300 and 302–309).

The earned statement is that REV exceeded the sampled controls **even when their initial derivatives were matched**, while also passing ISO. Avoid an unrestricted claim that local sensitivity has been eliminated as an explanation. The negative derivatives in 9/10 fresh seeds further undermine the earlier positive-initial-gradient explanation; they do not identify the finite-dose mechanism.

## Per-seed margins against both families

Taken from `phase_b_results.json`. Margin is AUC_REV minus that family's maximum AUC. Per-dose rank is at alpha = 1/8, 1/4, 1/2, 3/4, 1, in that order. Rank 1 is the most damaging, and exact AUC ties count against REV. The 32 AUC values for each seed, target, and family remain in that JSON.

### Primary, weight_hh

| seed | AUC_REV | family | max | median | margin | m/B | m/PD | m/max | rank | per-dose rank | n_end_gt | n_end_tie | endpoint-D | thin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 300 | 0.0055883827 | FO | 0.0040689052 | 0.0024672812 | 0.0015194774 | 0.11447302 | 0.10979976 | 0.37343642 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 300 | 0.0055883827 | ISO | 0.0074762651 | 0.0015794132 | -0.0018878824 | -0.14222759 | -0.13642127 | -0.25251679 | 2 | 1,1,2,2,2 | 1 | 0 | false | false |
| 301 | 0.0056661739 | FO | 0.0026165493 | 0.0016114838 | 0.0030496246 | 0.21590309 | 0.22037054 | 1.1655139 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 301 | 0.0056661739 | ISO | 0.0063493045 | 0.0014691753 | -0.00068313063 | -0.048363334 | -0.049364064 | -0.10759141 | 2 | 1,1,1,2,4 | 3 | 0 | false | false |
| 302 | 0.0043796335 | FO | 0.0032928477 | 0.0015426215 | 0.0010867858 | 0.082269365 | 0.078532804 | 0.33004436 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 302 | 0.0043796335 | ISO | 0.0033555909 | 0.0012029052 | 0.0010240426 | 0.077519725 | 0.073998887 | 0.30517506 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 303 | 0.0055148543 | FO | 0.0050726466 | 0.0018941528 | 0.00044220773 | 0.03327864 | 0.031954607 | 0.087174953 | 1 | 1,1,1,1,2 | 1 | 0 | false | true |
| 303 | 0.0055148543 | ISO | 0.0053615305 | 0.0016238899 | 0.00015332385 | 0.01153849 | 0.011079416 | 0.028597031 | 1 | 1,1,1,2,2 | 1 | 0 | false | true |
| 304 | 0.0043709675 | FO | 0.0033589425 | 0.0022645088 | 0.0010120249 | 0.073997019 | 0.073130467 | 0.30129271 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 304 | 0.0043709675 | ISO | 0.0035873346 | 0.001365203 | 0.00078363286 | 0.057297498 | 0.056626508 | 0.21844432 | 1 | 1,1,1,1,2 | 1 | 0 | false | false |
| 305 | 0.00538384 | FO | 0.0039210112 | 0.0014969007 | 0.0014628288 | 0.1102341 | 0.10570624 | 0.37307436 | 1 | 1,1,1,1,2 | 1 | 0 | false | false |
| 305 | 0.00538384 | ISO | 0.0026373949 | 0.0012167018 | 0.0027464451 | 0.20696333 | 0.19846232 | 1.0413477 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 306 | 0.0053499992 | FO | 0.003966342 | 0.0017761387 | 0.0013836572 | 0.10584264 | 0.099985188 | 0.34884971 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 306 | 0.0053499992 | ISO | 0.0031006497 | 0.0014096464 | 0.0022493495 | 0.17206364 | 0.16254143 | 0.72544456 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 307 | 0.005191738 | FO | 0.0031971354 | 0.0011767539 | 0.0019946025 | 0.14003871 | 0.14413303 | 0.62387177 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 307 | 0.005191738 | ISO | 0.002544512 | 0.0010290296 | 0.002647226 | 0.18585864 | 0.1912926 | 1.0403669 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 308 | 0.005655088 | FO | 0.0033076076 | 0.0018889939 | 0.0023474804 | 0.1569657 | 0.16963252 | 0.70972155 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 308 | 0.005655088 | ISO | 0.0031204814 | 0.0013339335 | 0.0025346065 | 0.16947801 | 0.18315454 | 0.81224856 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 309 | 0.0049255693 | FO | 0.0045554865 | 0.001838449 | 0.00037008277 | 0.026828283 | 0.026742746 | 0.081238911 | 1 | 1,1,1,1,2 | 1 | 0 | false | true |
| 309 | 0.0049255693 | ISO | 0.0037653546 | 0.0016870208 | 0.0011602147 | 0.084107048 | 0.083838888 | 0.30812893 | 1 | 1,1,1,1,2 | 1 | 0 | false | false |

### Secondary, r

| seed | AUC_REV | family | max | median | margin | m/B | m/PD | m/max | rank | per-dose rank | n_end_gt | n_end_tie | endpoint-D | thin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 300 | 0.00016721333 | FO | 0.00026389884 | 1.0986311e-05 | -9.668551e-05 | -0.007284006 | -0.0069866428 | -0.36637338 | 3 | 3,3,3,3,3 | 2 | 0 | false | false |
| 300 | 0.00016721333 | ISO | 0.00019992873 | 3.9062094e-05 | -3.27154e-05 | -0.0024646834 | -0.0023640649 | -0.16363531 | 3 | 26,18,5,2,1 | 0 | 0 | true | false |
| 301 | 0.0001694414 | FO | 0.00013431125 | 3.2459709e-05 | 3.5130154e-05 | 0.0024870959 | 0.0025385586 | 0.2615578 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 301 | 0.0001694414 | ISO | 0.00021344439 | 4.4324589e-05 | -4.4002993e-05 | -0.0031152628 | -0.0031797235 | -0.20615671 | 2 | 15,3,2,2,2 | 1 | 0 | false | false |
| 302 | 0.00018148151 | FO | 0.00020589063 | 3.7637555e-05 | -2.4409122e-05 | -0.0018477633 | -0.0017638405 | -0.11855383 | 4 | 3,3,3,4,3 | 2 | 0 | false | false |
| 302 | 0.00018148151 | ISO | 0.00016144981 | 5.7893866e-05 | 2.0031693e-05 | 0.0015163932 | 0.0014475208 | 0.12407381 | 1 | 22,12,3,1,1 | 0 | 0 | true | false |
| 303 | 0.00021525392 | FO | 0.00011574271 | 5.6172957e-05 | 9.9511208e-05 | 0.0074887829 | 0.007190832 | 0.85976218 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 303 | 0.00021525392 | ISO | 0.0001596793 | 5.658671e-05 | 5.5574618e-05 | 0.0041823053 | 0.0040159069 | 0.34803896 | 1 | 7,2,1,1,1 | 0 | 0 | true | false |
| 304 | 0.00011098544 | FO | 0.00019708733 | 3.5066917e-05 | -8.6101886e-05 | -0.0062955791 | -0.0062218539 | -0.43687175 | 4 | 12,9,4,4,2 | 1 | 0 | false | false |
| 304 | 0.00011098544 | ISO | 0.00018854709 | 3.6362562e-05 | -7.7561652e-05 | -0.0056711362 | -0.0056047236 | -0.41136488 | 4 | 33,33,14,3,1 | 0 | 0 | true | false |
| 305 | 0.00026612964 | FO | 0.0001126767 | 7.3315287e-05 | 0.00015345294 | 0.011563723 | 0.011088744 | 1.3618871 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 305 | 0.00026612964 | ISO | 0.000155968 | 3.8406424e-05 | 0.00011016164 | 0.0083014293 | 0.0079604485 | 0.70630925 | 1 | 2,1,1,1,1 | 0 | 0 | true | false |
| 306 | 0.00015190849 | FO | 7.6898286e-05 | 7.303303e-06 | 7.5010201e-05 | 0.0057378935 | 0.0054203518 | 0.97544698 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 306 | 0.00015190849 | ISO | 9.1519481e-05 | 3.7900159e-05 | 6.0389006e-05 | 0.0046194475 | 0.0043638019 | 0.65984865 | 1 | 32,26,2,1,1 | 0 | 0 | true | false |
| 307 | 0.00017478402 | FO | 0.00019820042 | 3.538372e-05 | -2.3416403e-05 | -0.0016440382 | -0.0016921051 | -0.11814507 | 2 | 5,3,3,2,2 | 1 | 0 | false | false |
| 307 | 0.00017478402 | ISO | 0.00037501176 | 7.2984339e-05 | -0.00020022773 | -0.014057755 | -0.014468762 | -0.53392388 | 3 | 29,21,9,3,3 | 2 | 0 | false | false |
| 308 | 0.00045423242 | FO | 6.0750934e-05 | -8.3052447e-07 | 0.00039348149 | 0.026310379 | 0.028433574 | 6.476962 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 308 | 0.00045423242 | ISO | 0.00025529094 | 7.986093e-05 | 0.00019894149 | 0.013302343 | 0.014375816 | 0.77927361 | 1 | 15,3,1,1,1 | 0 | 0 | true | false |
| 309 | 0.00021963008 | FO | 0.00012673637 | 3.5511808e-05 | 9.2893706e-05 | 0.0067341117 | 0.0067126412 | 0.732968 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 309 | 0.00021963008 | ISO | 0.00013302252 | 3.4272781e-05 | 8.6607559e-05 | 0.0062784122 | 0.0062583947 | 0.65107441 | 1 | 22,8,1,1,1 | 0 | 0 | true | false |

### Secondary, z

| seed | AUC_REV | family | max | median | margin | m/B | m/PD | m/max | rank | per-dose rank | n_end_gt | n_end_tie | endpoint-D | thin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 300 | 0.0004294379 | FO | 0.00016454951 | 5.891291e-05 | 0.00026488839 | 0.019955923 | 0.01914124 | 1.6097793 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 300 | 0.0004294379 | ISO | 0.0002909541 | 0.00010861741 | 0.00013848379 | 0.010432967 | 0.010007051 | 0.47596439 | 1 | 24,9,1,1,1 | 0 | 0 | true | false |
| 301 | 0.00049390121 | FO | 0.00032097056 | 5.6938449e-05 | 0.00017293065 | 0.012242904 | 0.012496233 | 0.53877416 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 301 | 0.00049390121 | ISO | 0.00021077171 | 0.00010839567 | 0.0002831295 | 0.020044609 | 0.02045937 | 1.3432993 | 1 | 3,1,1,1,1 | 0 | 0 | true | false |
| 302 | 0.00058992648 | FO | 0.00037598831 | 0.00012595576 | 0.00021393817 | 0.016195056 | 0.015459499 | 0.56900219 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 302 | 0.00058992648 | ISO | 0.00042553398 | 0.00020456636 | 0.0001643925 | 0.012444463 | 0.011879253 | 0.38632049 | 1 | 21,7,1,1,1 | 0 | 0 | true | false |
| 303 | 0.00029687361 | FO | 0.00030928196 | 5.8456924e-05 | -1.2408355e-05 | -0.00093379906 | -0.00089664667 | -0.040119877 | 2 | 1,1,1,2,2 | 1 | 0 | false | false |
| 303 | 0.00029687361 | ISO | 0.00025421037 | 0.00011521289 | 4.2663239e-05 | 0.0032106508 | 0.0030829109 | 0.16782651 | 1 | 17,8,1,1,1 | 0 | 0 | true | false |
| 304 | 0.00063076642 | FO | 0.00059730352 | 9.1599236e-05 | 3.3462901e-05 | 0.0024467332 | 0.0024180804 | 0.056023278 | 1 | 2,2,1,1,1 | 0 | 0 | true | false |
| 304 | 0.00063076642 | ISO | 0.00070287409 | 0.00021238873 | -7.2107665e-05 | -0.0052723527 | -0.0052106101 | -0.10258973 | 2 | 27,10,3,2,2 | 1 | 0 | false | false |
| 305 | 0.0002996676 | FO | 0.00014409421 | 6.4081992e-05 | 0.00015557338 | 0.011723513 | 0.01124197 | 1.0796643 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 305 | 0.0002996676 | ISO | 0.0001966916 | 9.7946871e-05 | 0.00010297599 | 0.0077599421 | 0.0074412028 | 0.52354037 | 1 | 11,1,1,1,1 | 0 | 0 | true | false |
| 306 | 0.00032392645 | FO | 0.00020002202 | 5.7548496e-05 | 0.00012390442 | 0.0094780493 | 0.008953523 | 0.6194539 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 306 | 0.00032392645 | ISO | 0.00021890524 | 7.7627063e-05 | 0.00010502121 | 0.0080335809 | 0.0075889932 | 0.4797565 | 1 | 10,2,1,1,1 | 0 | 0 | true | false |
| 307 | 0.0007107741 | FO | 0.00068958676 | 0.00015994101 | 2.1187342e-05 | 0.0014875385 | 0.0015310297 | 0.030724694 | 1 | 2,2,2,1,1 | 0 | 0 | true | false |
| 307 | 0.0007107741 | ISO | 0.00048618116 | 0.00018537712 | 0.00022459294 | 0.015768408 | 0.016229429 | 0.46195319 | 1 | 18,4,1,1,1 | 0 | 0 | true | false |
| 308 | 0.00067569005 | FO | 0.00019907113 | 9.4793684e-05 | 0.00047661891 | 0.031869413 | 0.034441211 | 2.3942141 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 308 | 0.00067569005 | ISO | 0.00029562847 | 0.00012582534 | 0.00038006158 | 0.025413048 | 0.027463831 | 1.2856055 | 1 | 5,1,1,1,1 | 0 | 0 | true | false |
| 309 | 0.00043454791 | FO | 0.00029470264 | 0.00013508562 | 0.00013984527 | 0.010137756 | 0.010105433 | 0.4745301 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 309 | 0.00043454791 | ISO | 0.0002930038 | 0.00011558544 | 0.00014154412 | 0.010260909 | 0.010228194 | 0.48307946 | 1 | 6,3,1,1,1 | 0 | 0 | true | false |

### Secondary, n

| seed | AUC_REV | family | max | median | margin | m/B | m/PD | m/max | rank | per-dose rank | n_end_gt | n_end_tie | endpoint-D | thin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 300 | 0.0045823189 | FO | 0.0035513651 | 0.0022205496 | 0.0010309538 | 0.077669071 | 0.074498299 | 0.29029789 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 300 | 0.0045823189 | ISO | 0.0051416785 | 0.0015654586 | -0.00055935959 | -0.04214053 | -0.040420179 | -0.1087893 | 2 | 1,1,1,2,4 | 3 | 0 | false | false |
| 301 | 0.0047816462 | FO | 0.0029067314 | 0.0014343756 | 0.0018749148 | 0.13273761 | 0.13548421 | 0.64502511 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 301 | 0.0047816462 | ISO | 0.0050616783 | 0.0010928672 | -0.00028003207 | -0.019825322 | -0.020235546 | -0.055323958 | 2 | 1,1,1,2,3 | 2 | 0 | false | false |
| 302 | 0.0030422699 | FO | 0.0031221867 | 0.0011711492 | -7.9916751e-05 | -0.0060496744 | -0.0057749066 | -0.025596404 | 2 | 2,2,1,2,2 | 1 | 0 | false | false |
| 302 | 0.0030422699 | ISO | 0.0027632138 | 0.0010269102 | 0.00027905613 | 0.021124467 | 0.020165023 | 0.1009897 | 1 | 4,1,1,1,2 | 1 | 0 | false | false |
| 303 | 0.0051141597 | FO | 0.0039723155 | 0.0018324399 | 0.0011418441 | 0.085930247 | 0.082511402 | 0.28745051 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 303 | 0.0051141597 | ISO | 0.0045857828 | 0.0012594778 | 0.00052837689 | 0.039763358 | 0.038181322 | 0.11522065 | 1 | 1,1,1,1,2 | 1 | 0 | false | false |
| 304 | 0.0032172843 | FO | 0.002644311 | 0.0014839324 | 0.00057297338 | 0.041894544 | 0.041403932 | 0.21668154 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 304 | 0.0032172843 | ISO | 0.0030795251 | 0.0010709908 | 0.00013775921 | 0.010072648 | 0.0099546912 | 0.044733914 | 1 | 7,1,1,1,2 | 1 | 0 | false | false |
| 305 | 0.0048040293 | FO | 0.0029792504 | 0.0012780218 | 0.0018247789 | 0.13750951 | 0.13186131 | 0.61249597 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 305 | 0.0048040293 | ISO | 0.0023550693 | 0.0011454155 | 0.0024489599 | 0.1845458 | 0.17696559 | 1.0398674 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 306 | 0.0048317201 | FO | 0.0038758722 | 0.0014934991 | 0.00095584786 | 0.073117432 | 0.069071028 | 0.24661491 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 306 | 0.0048317201 | ISO | 0.0030288262 | 0.0014965583 | 0.0018028939 | 0.13791209 | 0.13027987 | 0.59524509 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 307 | 0.0041367378 | FO | 0.0016954785 | 0.00090515231 | 0.0024412593 | 0.17139796 | 0.17640913 | 1.4398645 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 307 | 0.0041367378 | ISO | 0.0019335859 | 0.00072214273 | 0.0022031519 | 0.15468072 | 0.15920313 | 1.1394125 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 308 | 0.0046596057 | FO | 0.0025533613 | 0.001528449 | 0.0021062445 | 0.14083532 | 0.15220045 | 0.8248909 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 308 | 0.0046596057 | ISO | 0.003021034 | 0.0011684151 | 0.0016385717 | 0.10956409 | 0.11840569 | 0.54238769 | 1 | 1,1,1,1,1 | 0 | 0 | true | false |
| 309 | 0.0041035865 | FO | 0.0042931654 | 0.0017504361 | -0.00018957891 | -0.013743079 | -0.013699262 | -0.044158305 | 2 | 1,1,1,2,2 | 1 | 0 | false | false |
| 309 | 0.0041035865 | ISO | 0.0039136521 | 0.0015065644 | 0.00018993442 | 0.013768851 | 0.013724952 | 0.048531248 | 1 | 1,1,1,1,2 | 1 | 0 | false | false |


AUC is the integral of the piecewise-linear interpolant through the six measured dose-excess values. It is not a certified integral of the network's continuous dose response. Negative excesses are retained; no clipping or absolute-value transformation is applied.

At alpha=1, only the hidden-to-hidden matrices during updates 5–8 equal their initialization. Input-to-hidden weights, biases, updates 1–4 and the fresh readout remain trained. This condition is not F-INIT, even apart from the readout difference.

Holding the same readout fixed in REV and random conditions controls readout identity, but does not eliminate differential disruption of compatibility among recurrent matrices, input weights, biases and the readout.

## Secondary blocks

Secondary results are correlated with the primary and with each other. They do not substitute for the primary and there is no any-block upgrade.

- Secondary (block-wise), r: JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET (0/10 joint)
- Secondary (block-wise), z: JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET (0/10 joint)
- Secondary (block-wise), n: JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET (5/10 joint)

The primary effect was not reproduced by any single block at the declared criterion.

Secondary condition counts from `phase_b_results.json`, D_FO / D_ISO / both / M:

- r: 6/6/5/0
- z: 9/9/8/0
- n: 8/8/6/8


## First-order diagnostics

The residual after subtracting the initial tangent contribution is reported for each seed. It is not a curvature estimate.
Sampled non-decreasing values do not imply a continuously monotonic path.

| seed | <G, delta> | cos | FO_AUC | residual_REV | negligible | fixed |
| --- | --- | --- | --- | --- | --- | --- |
| 300 | -0.0015665883 | -0.26066488 | -0.00078329417 | 0.0063716768 | none | none |
| 301 | 0.00027215223 | 0.05865062 | 0.00013607611 | 0.0055300978 | none | none |
| 302 | -0.0010934904 | -0.24460175 | -0.00054674521 | 0.0049263787 | none | none |
| 303 | -0.00066358759 | -0.16669655 | -0.00033179379 | 0.0058466481 | none | none |
| 304 | -0.0017996918 | -0.30884215 | -0.00089984592 | 0.0052708134 | none | none |
| 305 | -0.00030733258 | -0.083777711 | -0.00015366629 | 0.0055375063 | none | none |
| 306 | -0.0010769237 | -0.30839976 | -0.00053846185 | 0.0058884611 | none | none |
| 307 | -0.00090555516 | -0.22993306 | -0.00045277758 | 0.0056445156 | none | none |
| 308 | -0.00086756127 | -0.21725518 | -0.00043378063 | 0.0060888686 | none | none |
| 309 | -0.0006561099 | -0.15049835 | -0.00032805495 | 0.0052536243 | none | none |

## Descriptive L_cont, XOR and E_total

These quantities are descriptive. Vector success does not establish an XOR-specific effect.

| seed | L_cont AUC | L_prefix XOR AUC | delta E_total(1) | delta E_XOR(1) |
| --- | --- | --- | --- | --- |
| 300 | 0.016409852 | 0.0037766667 | 0.064863015 | 0.036451374 |
| 301 | 0.014452295 | 0.0040354992 | 0.05580442 | 0.029046478 |
| 302 | 0.013108896 | 0.0029472534 | 0.077270836 | 0.044098966 |
| 303 | 0.010459203 | 0.0036562717 | 0.045086373 | 0.028811786 |
| 304 | 0.016919042 | 0.0030217371 | 0.06638495 | 0.032161605 |
| 305 | 0.013325032 | 0.0036369793 | 0.062657806 | 0.035752217 |
| 306 | 0.014489436 | 0.0037236372 | 0.065654884 | 0.029514703 |
| 307 | 0.015985925 | 0.0035295497 | 0.06972435 | 0.03763971 |
| 308 | 0.0096595215 | 0.0038869316 | 0.040931115 | 0.024059667 |
| 309 | 0.016053689 | 0.0033114464 | 0.072722908 | 0.035496285 |

## Development history

Exploratory phase A curves for seeds 100-109 and 200-209 are in `first_order_control_phaseA_exploratory/`. They are development-only and are not confirmatory. They are not pooled with seeds 300-309, and they do not set this label.

Freeze commit: `335e5056f38d4d5fffc737e467b3faebe5c9a77a`.

The combined and group-level Phase A pass counts are retrospective descriptive summaries that depart from the prescribed per-seed-only reporting format. They are not confirmatory evidence and do not enter any Phase B verdict. The authoritative Phase A presentation is the separate per-seed record for each exploratory group.

## Phase A derivative comparison (E-C1)

Per-seed comparison against the draft finite-difference values (`/workspace/scratch/fo_control/feasibility.json`, Research Delegate review) agrees within |Δcos| ≤ 3.7e-10 and relative |Δ⟨G,delta⟩| ≤ 1.7e-8 in all 20 seeds; ⟨G,delta⟩ < 0 in 15/20. The 'inside=False' flags reflect rounding of the printed ranges. This confirms the derivative calculations by autograd, as consult #17 required.

The scratch feasibility file is not in this checkout. The versioned recomputation from the committed checkpoints is `results_v1_errata/feasibility_autograd_comparison_v1.json`, sha256 `43cd03492342e57bca25800959ebfb3e58eed4aecd70a75882efe07456effc7a`. Its maximum absolute cosine gap against the committed autograd values is 3.805788600930171e-10, on seed 102. Its maximum relative inner-product gap is 1.7038662252133627e-08. Fifteen of the twenty autograd inner products are negative.

## Ledger

Q-CAUSE, organization level: SUPPORTED, BOUNDED. In W2, continuation-stage joint recurrent reversion met the prespecified joint FO-and-ISO AUC criterion in 8/10 fresh GRU-8 seeds. In each passing seed, excess prefix-function loss exceeded every one of 32 first-order-matched paths and every one of 32 isotropic paths and met the materiality threshold. This supports a causal contribution of the trained hidden-to-hidden parameters under the specified intervention and fixed surrounding computation.

The result meets the replication threshold exactly. Two passing seeds have thin margins against at least one family; each failing seed loses to one sampled ISO path. FO passed in 10/10 seeds and excluded no additional seeds beyond ISO. The claim concerns sampled controls and dose-averaged AUC, not arbitrary perturbations, every dose or the endpoint.

Secondary blocks: criterion not met, r 0/10, z 0/10, n 5/10. The primary effect was not reproduced by any single block at the declared criterion; no localization or interaction mechanism is identified.

Q-LEARN: E1 and transfer replicated 10/10. Q-NECESSITY: NOT_ESTABLISHED, not tested. Q-EXIST: not addressed; the supplied exact solution remains available. No C4, consciousness or organism conclusion.

## Deviation rulings (Astra consult #18)

Exactly zero gradient. Ratified. With nonzero displacement and exactly zero gradient:

```text
r_k = norm(d_k)
rho_k = 1
```

The block has full randomized spread and belongs in `R_eff`. Skip the undefined unit-gradient orthogonality check, but retain norm and first-order identity checks. This is distinct from the diagnostic near-zero threshold.

Zero displacement. Keep it an ordinary eligibility non-pass, as frozen. There is no learned displacement in that target to test. Do not count it as an invalid or collapsed-comparison seed. If the entire displacement is zero, avoid forming undefined radius ratios. This ruling affects no observed result.
