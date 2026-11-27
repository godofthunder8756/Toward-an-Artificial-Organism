# P1p discovery: the Layer 4 battery on a CIFG-LSTM, P1g's seeds (3200-3207)

**Overall: UNDETERMINED.** Architecture: CIFG-LSTM, 35 cells, packed state [h, c] of 70 (the GRU's width); parameters {'PLAIN': 15444}. Seeds: 8. Each study's own decision rules.

| study | label on the CIFG | label on the GRU (confirmed) | same |
| --- | --- | --- | --- |
| P1g | P1G_1 UNDETERMINED | P1G_1 DERIVED_AHEAD | no |
| P1j | INVALID | LEARNED_SIGNED_INTEGRITY_VARIABLE | no |
| P1k | INVALID | GENERAL_INTEGRITY_VARIABLE | no |
| P1l | INVALID | SHARED_GENERAL_ACCESS | no |
| P1m | INVALID | VALUE_CREDITED | no |

## P1g (monitor; training records)

- valid True (memory True, damage True, exposure True); phase-1 clear correct 0.9983215678762646; exposure 0.08165301213819023; P1g overall UNDETERMINED; arrow UNDETERMINED
- P1G_1: 8/8 (sign p 0.0078, Holm n/a; 0.1305 against 0.0025) UNDETERMINED
- P1G_2: 6/8 > 0 (sign p 0.2891, Holm n/a; median 0.0058) UNDETERMINED
- P1G_3: 1/8 (sign p 0.0703, Holm n/a; 0.1305 against 0.1549) UNDETERMINED
- PFATE: M 0.13049200759127602, M_early 0.16768078341046427, in_band 0.8898359375, acc_conflict 0.5037692304870864
- PYOKED: M 0.15493401777727855, M_early 0.18118306884347996, in_band 0.842703125, acc_conflict 0.49997170863487655
- PNOFATE: M 0.002475709896585826, M_early 0.0, in_band 0.8348789062499999, acc_conflict 0.49801208366624655

## P1j

**Overall: INVALID.** Valid: False (seeds with a fitted primary run: {'PFATE': 8, 'PYOKED': 8, 'PNOFATE': 8}; needed >= 20 for PFATE and PNOFATE). Seeds: 8. Point: 3600. Primary push step: 5.

## Push at delay step 3

| measure | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| induce | 0.1278 | 0.1339 | -0.0103 |
| rescue | 0.0345 | 0.1004 | -0.0039 |
| gap | 1.7808 | 1.9708 | 0.1100 |
| induce_abs | 0.0033 | 0.0010 | -0.0000 |
| rescue_abs | -0.0001 | 0.0113 | 0.0000 |
| gap_abs | 0.1263 | 0.1152 | 0.0001 |
| induce_none | 0.0581 | 0.1351 | 0.0125 |
| acc_same_d_minus_r | 0.0000 | 0.0000 | 0.0000 |
| acc_conflict_d_minus_r | 0.0085 | 0.0224 | -0.0070 |
| random_same | -0.0214 | 0.0088 | 0.0004 |
| random_conflict | 0.0400 | -0.0363 | -0.0289 |
| induce_share | 0.1255 | 0.0981 | -0.0254 |
| rescue_share | 0.0418 | 0.0342 | -0.0793 |
| signed | 0.0523 | 0.0770 | -0.0037 |
| signed_fix | 0.0765 | 0.1200 | -0.0647 |
| induce_fix | 0.2155 | 0.2455 | 0.2161 |
| rescue_fix | 0.0564 | 0.1406 | -0.3985 |
| induce_abs_fix | 0.0021 | 0.0032 | 0.0000 |
| rescue_abs_fix | 0.0057 | 0.0000 | -0.0002 |
| induce_none_fix | 0.2107 | 0.2524 | 0.2585 |
| acc_same_d_minus_r_fix | 0.0000 | 0.0000 | 0.0000 |
| acc_conflict_d_minus_r_fix | -0.0078 | -0.0128 | 0.0171 |
| random_same_fix | -0.0052 | 0.0628 | 0.0439 |
| random_conflict_fix | 0.0135 | -0.0058 | -0.0400 |
| norm_d | 0.5440 | 0.7086 | 0.0700 |
| norm_d_raw | 0.7378 | 0.8283 | 0.0794 |
| norm_c | 3.7991 | 4.5003 | 2.4742 |
| norm_a | 0.0326 | 0.0440 | 0.0437 |
| share_d_kept | 0.9153 | 0.8878 | 0.7695 |
| cos_draw_c | -0.2646 | -0.0300 | -0.2065 |
| cos_draw_a | -0.1324 | -0.0323 | 0.1715 |

## Push at delay step 5 (primary)

| measure | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| induce | 0.1055 | 0.2023 | -0.0152 |
| rescue | 0.0279 | 0.1206 | 0.0221 |
| gap | 1.7580 | 1.9738 | 0.0875 |
| induce_abs | 0.0012 | 0.0026 | -0.0000 |
| rescue_abs | 0.0003 | 0.0108 | 0.0000 |
| gap_abs | 0.1255 | 0.1186 | 0.0001 |
| induce_none | 0.1095 | 0.2217 | 0.0157 |
| acc_same_d_minus_r | 0.0000 | 0.0000 | 0.0000 |
| acc_conflict_d_minus_r | 0.0106 | 0.0219 | -0.0070 |
| random_same | 0.0049 | -0.0092 | 0.0130 |
| random_conflict | 0.0109 | -0.0378 | -0.0312 |
| induce_share | 0.1865 | 0.1686 | -0.0932 |
| rescue_share | 0.0715 | 0.0879 | 0.0085 |
| signed | 0.0342 | 0.0956 | 0.0086 |
| signed_fix | 0.1059 | 0.0561 | -0.0855 |
| induce_fix | 0.2753 | 0.2940 | 0.1686 |
| rescue_fix | 0.0804 | 0.0890 | -0.3407 |
| induce_abs_fix | 0.0020 | 0.0039 | 0.0000 |
| rescue_abs_fix | 0.0012 | -0.0001 | -0.0001 |
| induce_none_fix | 0.2415 | 0.2874 | 0.1467 |
| acc_same_d_minus_r_fix | 0.0000 | 0.0000 | 0.0000 |
| acc_conflict_d_minus_r_fix | 0.0080 | -0.0186 | 0.0171 |
| random_same_fix | 0.0156 | 0.0558 | 0.0361 |
| random_conflict_fix | -0.0774 | -0.0052 | -0.0421 |
| norm_d | 0.6176 | 0.8333 | 0.0546 |
| norm_d_raw | 0.8391 | 0.9418 | 0.0674 |
| norm_c | 3.8140 | 4.7123 | 2.3922 |
| norm_a | 0.0353 | 0.0416 | 0.0371 |
| share_d_kept | 0.9376 | 0.8958 | 0.7955 |
| cos_draw_c | -0.2652 | -0.0296 | -0.0482 |
| cos_draw_a | -0.0253 | -0.0801 | 0.2484 |

## Push at delay step 7

| measure | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| induce | 0.1654 | 0.2506 | -0.0141 |
| rescue | 0.0490 | 0.0428 | 0.0392 |
| gap | 1.7971 | 2.0438 | 0.0931 |
| induce_abs | 0.0006 | 0.0008 | -0.0000 |
| rescue_abs | 0.0001 | 0.0088 | 0.0000 |
| gap_abs | 0.1254 | 0.1179 | 0.0001 |
| induce_none | 0.0884 | 0.2513 | 0.0177 |
| acc_same_d_minus_r | 0.0000 | 0.0000 | 0.0000 |
| acc_conflict_d_minus_r | 0.0055 | 0.0195 | -0.0070 |
| random_same | 0.0038 | 0.0716 | -0.0013 |
| random_conflict | 0.0260 | -0.0710 | -0.0238 |
| induce_share | 0.1146 | 0.1107 | 0.0065 |
| rescue_share | 0.0615 | 0.0259 | 0.3549 |
| signed | 0.1096 | 0.1402 | 0.0302 |
| signed_fix | 0.1984 | 0.2330 | -0.1584 |
| induce_fix | 0.3929 | 0.2686 | 0.2550 |
| rescue_fix | 0.0438 | 0.0882 | -0.2321 |
| induce_abs_fix | 0.0027 | 0.0011 | 0.0000 |
| rescue_abs_fix | 0.0065 | 0.0001 | -0.0001 |
| induce_none_fix | 0.3585 | 0.2824 | 0.2251 |
| acc_same_d_minus_r_fix | 0.0000 | 0.0000 | 0.0000 |
| acc_conflict_d_minus_r_fix | 0.0067 | -0.0174 | 0.0171 |
| random_same_fix | 0.0202 | 0.0785 | 0.0196 |
| random_conflict_fix | -0.0887 | -0.0209 | -0.0121 |
| norm_d | 0.5813 | 0.8506 | 0.0396 |
| norm_d_raw | 0.8342 | 0.9500 | 0.0656 |
| norm_c | 3.8068 | 4.8066 | 2.3747 |
| norm_a | 0.0372 | 0.0703 | 0.0390 |
| share_d_kept | 0.9494 | 0.8525 | 0.7178 |
| cos_draw_c | -0.2461 | -0.0607 | -0.0335 |
| cos_draw_a | -0.0018 | 0.0446 | 0.1690 |

## Tests

- P1J_1 induce: |z|(same, +r) - |z|(same, +d), PFATE against 0: 6/8 > 0 (sign p 0.2891, Holm 0.8672; median 0.1055) UNDETERMINED
- P1J_2 rescue: |z|(conflict, -d) - |z|(conflict, -r), PFATE against 0: 5/8 > 0 (sign p 0.7266, Holm 1.0000; median 0.0279) UNDETERMINED
- P1J_3 learned variable: signed (induce + rescue, natural size), PFATE against PNOFATE: 5/8 (sign p 0.7266, Holm 1.0000; 0.0342 against 0.0086) UNDETERMINED
- P1J_4 learned use: signed at push norm 1.0, PFATE against PNOFATE: 7/8 (sign p 0.0703, Holm 0.2812; 0.1059 against -0.0855) UNDETERMINED
- content, same trials: accuracy (+d) - (+r), PFATE: 0/0 > 0 (sign p n/a, Holm n/a; median n/a) UNDETERMINED
- content, conflict trials: accuracy (-d) - (-r), PFATE: 4/8 > 0 (sign p 1.0000, Holm n/a; median 0.0106) UNDETERMINED
- content confound flags: induce False, rescue False (tolerance 0.02)
- induce_PFATE_vs_PNOFATE: 6/8 (sign p 0.2891, Holm n/a; 0.1055 against -0.0152) UNDETERMINED
- induce_fix_PFATE_vs_PNOFATE: 6/8 (sign p 0.2891, Holm n/a; 0.2753 against 0.1686) UNDETERMINED
- signed_PFATE_vs_PYOKED: 5/8 (sign p 0.7266, Holm n/a; 0.0342 against 0.0956) UNDETERMINED
- rescue_fix_PFATE_vs_PNOFATE: 5/8 (sign p 0.7266, Holm n/a; 0.0804 against -0.3407) UNDETERMINED
- rescue_PFATE_vs_PNOFATE: 5/8 (sign p 0.7266, Holm n/a; 0.0279 against 0.0221) UNDETERMINED
- induce_PFATE_vs_PYOKED: 5/8 (sign p 0.7266, Holm n/a; 0.1055 against 0.2023) UNDETERMINED
- induce_abs_PFATE_vs_PNOFATE: 8/8 (sign p 0.0078, Holm n/a; 0.0012 against -0.0000) UNDETERMINED
- norm_d_PFATE_vs_PNOFATE: 7/8 (sign p 0.0703, Holm n/a; 0.6176 against 0.0546) UNDETERMINED
- route s3 induce: PFATE 6/8 (p 0.2891; median 0.1278) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.1339) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0103) UNDETERMINED
- route s3 rescue: PFATE 5/8 (p 0.7266; median 0.0345) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.1004) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0039) UNDETERMINED
- route s3 induce_abs: PFATE 7/8 (p 0.0703; median 0.0033) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0010) UNDETERMINED; PNOFATE 1/8 (p 0.0703; median -0.0000) UNDETERMINED
- route s3 rescue_abs: PFATE 3/8 (p 0.7266; median -0.0001) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0113) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0000) UNDETERMINED
- route s3 induce_none: PFATE 4/8 (p 1.0000; median 0.0581) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.1351) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0125) UNDETERMINED
- route s3 acc_same_d_minus_r: PFATE 0/2 (p 0.5000; median -0.0018) UNDETERMINED; PYOKED 0/1 (p 1.0000; median -0.0017) UNDETERMINED; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route s3 acc_conflict_d_minus_r: PFATE 5/8 (p 0.7266; median 0.0085) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0224) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0070) UNDETERMINED
- route s3 random_same: PFATE 3/8 (p 0.7266; median -0.0214) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0088) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0004) UNDETERMINED
- route s3 random_conflict: PFATE 5/8 (p 0.7266; median 0.0400) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0363) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0289) UNDETERMINED
- route s3 signed: PFATE 5/8 (p 0.7266; median 0.0523) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0770) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0037) UNDETERMINED
- route s3 signed_fix: PFATE 5/8 (p 0.7266; median 0.0765) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.1200) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0647) UNDETERMINED
- route s3 induce_fix: PFATE 7/8 (p 0.0703; median 0.2155) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.2455) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.2161) UNDETERMINED
- route s3 rescue_fix: PFATE 4/8 (p 1.0000; median 0.0564) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.1406) UNDETERMINED; PNOFATE 1/8 (p 0.0703; median -0.3985) UNDETERMINED
- route s3 induce_abs_fix: PFATE 8/8 (p 0.0078; median 0.0021) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0032) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0000) UNDETERMINED
- route s3 rescue_abs_fix: PFATE 5/8 (p 0.7266; median 0.0057) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0000) UNDETERMINED; PNOFATE 1/8 (p 0.0703; median -0.0002) UNDETERMINED
- route s3 induce_none_fix: PFATE 7/8 (p 0.0703; median 0.2107) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.2524) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.2585) UNDETERMINED
- route s3 acc_same_d_minus_r_fix: PFATE 0/0 (p n/a; median n/a) UNDETERMINED; PYOKED 0/0 (p n/a; median n/a) UNDETERMINED; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route s3 acc_conflict_d_minus_r_fix: PFATE 3/8 (p 0.7266; median -0.0078) UNDETERMINED; PYOKED 2/8 (p 0.2891; median -0.0128) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0171) UNDETERMINED
- route s3 random_same_fix: PFATE 4/8 (p 1.0000; median -0.0052) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0628) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0439) UNDETERMINED
- route s3 random_conflict_fix: PFATE 4/8 (p 1.0000; median 0.0135) UNDETERMINED; PYOKED 4/8 (p 1.0000; median -0.0058) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0400) UNDETERMINED
- route s5 induce: PFATE 6/8 (p 0.2891; median 0.1055) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.2023) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0152) UNDETERMINED
- route s5 rescue: PFATE 5/8 (p 0.7266; median 0.0279) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.1206) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0221) UNDETERMINED
- route s5 induce_abs: PFATE 8/8 (p 0.0078; median 0.0012) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0026) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0000) UNDETERMINED
- route s5 rescue_abs: PFATE 5/8 (p 0.7266; median 0.0003) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0108) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0000) UNDETERMINED
- route s5 induce_none: PFATE 6/8 (p 0.2891; median 0.1095) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.2217) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0157) UNDETERMINED
- route s5 acc_same_d_minus_r: PFATE 0/0 (p n/a; median n/a) UNDETERMINED; PYOKED 0/0 (p n/a; median n/a) UNDETERMINED; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route s5 acc_conflict_d_minus_r: PFATE 4/8 (p 1.0000; median 0.0106) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0219) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0070) UNDETERMINED
- route s5 random_same: PFATE 5/8 (p 0.7266; median 0.0049) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0092) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0130) UNDETERMINED
- route s5 random_conflict: PFATE 5/8 (p 0.7266; median 0.0109) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0378) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0312) UNDETERMINED
- route s5 signed: PFATE 5/8 (p 0.7266; median 0.0342) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0956) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0086) UNDETERMINED
- route s5 signed_fix: PFATE 6/8 (p 0.2891; median 0.1059) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0561) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0855) UNDETERMINED
- route s5 induce_fix: PFATE 7/8 (p 0.0703; median 0.2753) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.2940) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.1686) UNDETERMINED
- route s5 rescue_fix: PFATE 6/8 (p 0.2891; median 0.0804) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0890) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.3407) UNDETERMINED
- route s5 induce_abs_fix: PFATE 6/8 (p 0.2891; median 0.0020) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0039) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0000) UNDETERMINED
- route s5 rescue_abs_fix: PFATE 6/8 (p 0.2891; median 0.0012) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0001) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0001) UNDETERMINED
- route s5 induce_none_fix: PFATE 8/8 (p 0.0078; median 0.2415) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.2874) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.1467) UNDETERMINED
- route s5 acc_same_d_minus_r_fix: PFATE 0/0 (p n/a; median n/a) UNDETERMINED; PYOKED 0/0 (p n/a; median n/a) UNDETERMINED; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route s5 acc_conflict_d_minus_r_fix: PFATE 5/8 (p 0.7266; median 0.0080) UNDETERMINED; PYOKED 2/8 (p 0.2891; median -0.0186) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0171) UNDETERMINED
- route s5 random_same_fix: PFATE 5/8 (p 0.7266; median 0.0156) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0558) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0361) UNDETERMINED
- route s5 random_conflict_fix: PFATE 2/8 (p 0.2891; median -0.0774) UNDETERMINED; PYOKED 4/8 (p 1.0000; median -0.0052) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0421) UNDETERMINED
- route s7 induce: PFATE 7/8 (p 0.0703; median 0.1654) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.2506) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0141) UNDETERMINED
- route s7 rescue: PFATE 5/8 (p 0.7266; median 0.0490) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0428) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0392) UNDETERMINED
- route s7 induce_abs: PFATE 6/8 (p 0.2891; median 0.0006) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0008) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0000) UNDETERMINED
- route s7 rescue_abs: PFATE 4/8 (p 1.0000; median 0.0001) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0088) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0000) UNDETERMINED
- route s7 induce_none: PFATE 6/8 (p 0.2891; median 0.0884) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.2513) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0177) UNDETERMINED
- route s7 acc_same_d_minus_r: PFATE 0/0 (p n/a; median n/a) UNDETERMINED; PYOKED 0/0 (p n/a; median n/a) UNDETERMINED; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route s7 acc_conflict_d_minus_r: PFATE 4/8 (p 1.0000; median 0.0055) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0195) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0070) UNDETERMINED
- route s7 random_same: PFATE 4/8 (p 1.0000; median 0.0038) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0716) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0013) UNDETERMINED
- route s7 random_conflict: PFATE 5/8 (p 0.7266; median 0.0260) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0710) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0238) UNDETERMINED
- route s7 signed: PFATE 5/8 (p 0.7266; median 0.1096) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.1402) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0302) UNDETERMINED
- route s7 signed_fix: PFATE 5/8 (p 0.7266; median 0.1984) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.2330) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.1584) UNDETERMINED
- route s7 induce_fix: PFATE 5/8 (p 0.7266; median 0.3929) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.2686) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.2550) UNDETERMINED
- route s7 rescue_fix: PFATE 4/8 (p 1.0000; median 0.0438) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0882) UNDETERMINED; PNOFATE 0/8 (p 0.0078; median -0.2321) UNDETERMINED
- route s7 induce_abs_fix: PFATE 6/8 (p 0.2891; median 0.0027) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0011) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0000) UNDETERMINED
- route s7 rescue_abs_fix: PFATE 5/8 (p 0.7266; median 0.0065) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0001) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0001) UNDETERMINED
- route s7 induce_none_fix: PFATE 6/8 (p 0.2891; median 0.3585) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.2824) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.2251) UNDETERMINED
- route s7 acc_same_d_minus_r_fix: PFATE 1/1 (p 1.0000; median 0.0016) UNDETERMINED; PYOKED 0/1 (p 1.0000; median -0.0017) UNDETERMINED; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route s7 acc_conflict_d_minus_r_fix: PFATE 5/8 (p 0.7266; median 0.0067) UNDETERMINED; PYOKED 2/8 (p 0.2891; median -0.0174) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0171) UNDETERMINED
- route s7 random_same_fix: PFATE 6/8 (p 0.2891; median 0.0202) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0785) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0196) UNDETERMINED
- route s7 random_conflict_fix: PFATE 3/8 (p 0.7266; median -0.0887) UNDETERMINED; PYOKED 4/8 (p 1.0000; median -0.0209) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0121) UNDETERMINED

## P1k

**Overall: INVALID.** Per operator: scramble UNDETERMINED, noise UNDETERMINED, zero UNDETERMINED. Valid: False (fitted seeds {'PFATE': 8, 'PYOKED': 8, 'PNOFATE': 8}, needed >= 20 for PFATE and PNOFATE; reference rescue on donor conflicts UNDETERMINED). Seeds: 8. Point: 3600.

## PFATE

| measure | donor | same | scramble | noise | zero |
| --- | --- | --- | --- | --- | --- |
| act | 0.6521 | -0.0038 | 0.3993 | 0.3870 | 0.3452 |
| alpha | 1.0000 | -0.0032 | 0.6502 | 0.6390 | 0.5681 |
| cos | 0.8709 | -0.0510 | 0.7899 | 0.7487 | 0.6896 |
| shift_norm | 0.8591 | 0.0730 | 0.5602 | 0.5735 | 0.5021 |
| dose_rho | 0.9000 | -0.2000 | 1.0000 | 1.0000 | 1.0000 |
| rescue | -0.0235 | 0.0084 | 0.0385 | 0.1298 | 0.3226 |
| gap | 1.7698 | -0.0139 | 1.3053 | 1.5296 | 2.1481 |
| rescue_share | 0.1147 | 2.2904 | 0.0590 | 0.1463 | 0.1819 |
| rescue_abs | 0.0000 | 0.0005 | 0.0031 | 0.0039 | 0.0159 |
| gap_abs | 0.1198 | 0.0000 | 0.0753 | 0.0851 | 0.0811 |
| acc_d_minus_r | 0.0012 | 0.0000 | -0.0072 | 0.0034 | 0.0046 |
| acc_dmg | 0.7000 | 1.0000 | 0.8735 | 0.8850 | 0.9236 |
| act_k9 | 0.3218 | 0.0030 | 0.1980 | 0.1908 | 0.1659 |
| act_k18 | 0.6267 | 0.0034 | 0.3684 | 0.3525 | 0.3330 |
| act_k26 | 0.8323 | -0.0072 | 0.4443 | 0.4477 | 0.3892 |
| act_k35 | 0.8479 | -0.0076 | 0.5820 | 0.5662 | 0.4841 |
| acc_k9 | 0.9172 | 1.0000 | 0.9689 | 0.9715 | 0.9817 |
| acc_k18 | 0.7556 | 1.0000 | 0.9150 | 0.9240 | 0.9613 |
| acc_k26 | 0.6181 | 1.0000 | 0.8441 | 0.8758 | 0.9019 |
| acc_k35 | 0.5158 | 1.0000 | 0.7819 | 0.8100 | 0.8242 |

## PYOKED

| measure | donor | same | scramble | noise | zero |
| --- | --- | --- | --- | --- | --- |
| act | 0.8701 | -0.0065 | 0.5177 | 0.5046 | 0.4548 |
| alpha | 1.0000 | 0.0005 | 0.5035 | 0.5079 | 0.4868 |
| cos | 0.9235 | -0.0856 | 0.8209 | 0.8154 | 0.7972 |
| shift_norm | 0.9712 | 0.0710 | 0.6971 | 0.6896 | 0.6368 |
| dose_rho | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| rescue | 0.2536 | -0.0235 | 0.0422 | -0.0274 | 0.0823 |
| gap | 2.1365 | -0.0070 | 1.5550 | 1.6449 | 2.1679 |
| rescue_share | 0.1407 | -1.3308 | 0.0932 | -0.0177 | 0.0604 |
| rescue_abs | 0.0235 | 0.0000 | 0.0046 | 0.0008 | 0.0089 |
| gap_abs | 0.1242 | 0.0000 | 0.0842 | 0.0912 | 0.0886 |
| acc_d_minus_r | 0.0197 | 0.0000 | -0.0038 | -0.0047 | 0.0021 |
| acc_dmg | 0.7089 | 1.0000 | 0.9059 | 0.8872 | 0.8923 |
| act_k9 | 0.4326 | -0.0061 | 0.1796 | 0.2050 | 0.1430 |
| act_k18 | 0.8221 | 0.0038 | 0.4190 | 0.3669 | 0.3193 |
| act_k26 | 1.0512 | -0.0074 | 0.6280 | 0.6099 | 0.5393 |
| act_k35 | 1.1612 | -0.0091 | 0.8290 | 0.8339 | 0.7602 |
| acc_k9 | 0.9020 | 1.0000 | 0.9710 | 0.9640 | 0.9731 |
| acc_k18 | 0.7752 | 1.0000 | 0.9259 | 0.9338 | 0.9340 |
| acc_k26 | 0.6645 | 1.0000 | 0.8670 | 0.8676 | 0.8697 |
| acc_k35 | 0.4959 | 1.0000 | 0.8300 | 0.7881 | 0.8151 |

## PNOFATE

| measure | donor | same | scramble | noise | zero |
| --- | --- | --- | --- | --- | --- |
| act | 0.0303 | -0.0012 | -0.0025 | -0.0064 | -0.0066 |
| alpha | 1.0000 | 0.0308 | 0.5104 | 0.6895 | 0.6952 |
| cos | 0.3255 | -0.0159 | -0.0107 | -0.0408 | -0.0234 |
| shift_norm | 0.1200 | 0.0900 | 0.3033 | 0.2989 | 0.3172 |
| dose_rho | 0.0000 | 0.1000 | 0.4000 | 0.8000 | 0.2000 |
| rescue | -0.0106 | -0.0011 | 0.0509 | -0.0120 | 0.0126 |
| gap | 0.0887 | -0.0178 | 0.6707 | 1.0671 | 1.9395 |
| rescue_share | 0.0539 | 0.0051 | 0.0517 | -0.0159 | 0.0075 |
| rescue_abs | 0.0000 | 0.0000 | -0.0000 | -0.0000 | -0.0000 |
| gap_abs | 0.0000 | -0.0000 | 0.0005 | 0.0008 | 0.0018 |
| acc_d_minus_r | 0.0174 | 0.0000 | -0.0055 | 0.0035 | -0.0009 |
| acc_dmg | 0.6779 | 1.0000 | 0.8586 | 0.8484 | 0.8502 |
| act_k9 | 0.0502 | -0.0146 | 0.0044 | 0.0093 | 0.0006 |
| act_k18 | 0.0347 | -0.0028 | 0.0083 | -0.0079 | 0.0072 |
| act_k26 | 0.0296 | 0.0001 | -0.0178 | 0.0013 | -0.0067 |
| act_k35 | 0.0508 | -0.0055 | 0.0195 | 0.0054 | -0.0021 |
| acc_k9 | 0.8604 | 1.0000 | 0.9464 | 0.9391 | 0.9371 |
| acc_k18 | 0.7198 | 1.0000 | 0.8891 | 0.8990 | 0.8790 |
| acc_k26 | 0.6215 | 1.0000 | 0.8409 | 0.8313 | 0.8295 |
| acc_k35 | 0.4920 | 1.0000 | 0.7705 | 0.7549 | 0.7585 |

## Tests

- reference: activation on donor conflicts, PFATE: 7/8 > 0 (sign p 0.0703, Holm n/a; median 0.6521) UNDETERMINED
- reference: rescue on donor conflicts, PFATE (validity): 3/8 > 0 (sign p 0.7266, Holm n/a; median -0.0235) UNDETERMINED
- P1K_ACT_scramble: 7/8 > 0 (sign p 0.0703, Holm 0.3516; median 0.3993) UNDETERMINED
- P1K_RES_scramble: 5/8 > 0 (sign p 0.7266, Holm 1.0000; median 0.0385) UNDETERMINED
- P1K_ACT_noise: 7/8 > 0 (sign p 0.0703, Holm 0.3516; median 0.3870) UNDETERMINED
- P1K_RES_noise: 5/8 > 0 (sign p 0.7266, Holm 1.0000; median 0.1298) UNDETERMINED
- P1K_ACT_zero: 7/8 > 0 (sign p 0.0703, Holm 0.3516; median 0.3452) UNDETERMINED
- P1K_RES_zero: 8/8 > 0 (sign p 0.0078, Holm 0.0469; median 0.3226) UNDETERMINED
- content donor: accuracy (-d) - (-r), PFATE: 5/8 > 0 (sign p 0.7266, Holm n/a; median 0.0012) UNDETERMINED; confounded False
- content same: accuracy (-d) - (-r), PFATE: 0/0 > 0 (sign p n/a, Holm n/a; median n/a) UNDETERMINED; confounded False
- content scramble: accuracy (-d) - (-r), PFATE: 3/8 > 0 (sign p 0.7266, Holm n/a; median -0.0072) UNDETERMINED; confounded False
- content noise: accuracy (-d) - (-r), PFATE: 5/8 > 0 (sign p 0.7266, Holm n/a; median 0.0034) UNDETERMINED; confounded False
- content zero: accuracy (-d) - (-r), PFATE: 6/8 > 0 (sign p 0.2891, Holm n/a; median 0.0046) UNDETERMINED; confounded False
- act_same_vs_scramble_PFATE: 1/8 (sign p 0.0703, Holm n/a; -0.0038 against 0.3993) UNDETERMINED
- act_donor_PFATE_vs_PNOFATE: 0/0 (sign p n/a, Holm n/a; n/a against n/a) UNDETERMINED
- rescue_donor_PFATE_vs_PNOFATE: 4/8 (sign p 1.0000, Holm n/a; -0.0235 against -0.0106) UNDETERMINED
- rescue_donor_PFATE_vs_PYOKED: 2/8 (sign p 0.2891, Holm n/a; -0.0235 against 0.2536) UNDETERMINED
- act_same_PFATE_vs_PNOFATE: 5/8 (sign p 0.7266, Holm n/a; -0.0032 against 0.0308) UNDETERMINED
- rescue_same_PFATE_vs_PNOFATE: 6/8 (sign p 0.2891, Holm n/a; 0.0084 against -0.0011) UNDETERMINED
- rescue_same_PFATE_vs_PYOKED: 5/8 (sign p 0.7266, Holm n/a; 0.0084 against -0.0235) UNDETERMINED
- act_scramble_PFATE_vs_PNOFATE: 6/8 (sign p 0.2891, Holm n/a; 0.6502 against 0.5104) UNDETERMINED
- rescue_scramble_PFATE_vs_PNOFATE: 4/8 (sign p 1.0000, Holm n/a; 0.0385 against 0.0509) UNDETERMINED
- rescue_scramble_PFATE_vs_PYOKED: 4/8 (sign p 1.0000, Holm n/a; 0.0385 against 0.0422) UNDETERMINED
- act_noise_PFATE_vs_PNOFATE: 6/8 (sign p 0.2891, Holm n/a; 0.6390 against 0.6895) UNDETERMINED
- rescue_noise_PFATE_vs_PNOFATE: 6/8 (sign p 0.2891, Holm n/a; 0.1298 against -0.0120) UNDETERMINED
- rescue_noise_PFATE_vs_PYOKED: 4/8 (sign p 1.0000, Holm n/a; 0.1298 against -0.0274) UNDETERMINED
- act_zero_PFATE_vs_PNOFATE: 5/8 (sign p 0.7266, Holm n/a; 0.5681 against 0.6952) UNDETERMINED
- rescue_zero_PFATE_vs_PNOFATE: 8/8 (sign p 0.0078, Holm n/a; 0.3226 against 0.0126) UNDETERMINED
- rescue_zero_PFATE_vs_PYOKED: 7/8 (sign p 0.0703, Holm n/a; 0.3226 against 0.0823) UNDETERMINED
- route donor act: PFATE 7/8 (p 0.0703; median 0.6521) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.8701) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0303) UNDETERMINED
- route donor rescue: PFATE 3/8 (p 0.7266; median -0.0235) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.2536) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0106) UNDETERMINED
- route donor rescue_abs: PFATE 4/8 (p 1.0000; median 0.0000) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0235) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0000) UNDETERMINED
- route donor gap: PFATE 5/8 (p 0.7266; median 1.7698) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 2.1365) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.0887) UNDETERMINED
- route donor dose_rho: PFATE 8/8 (p 0.0078; median 0.9000) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 1.0000) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0000) UNDETERMINED
- route donor cos: PFATE 7/8 (p 0.0703; median 0.8709) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.9235) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.3255) UNDETERMINED
- route donor acc_d_minus_r: PFATE 5/8 (p 0.7266; median 0.0012) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0197) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0174) UNDETERMINED
- route same act: PFATE 2/8 (p 0.2891; median -0.0038) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0065) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0012) UNDETERMINED
- route same rescue: PFATE 6/8 (p 0.2891; median 0.0084) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0235) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0011) UNDETERMINED
- route same rescue_abs: PFATE 5/8 (p 0.7266; median 0.0005) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0000) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0000) UNDETERMINED
- route same gap: PFATE 3/8 (p 0.7266; median -0.0139) UNDETERMINED; PYOKED 4/8 (p 1.0000; median -0.0070) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0178) UNDETERMINED
- route same dose_rho: PFATE 4/8 (p 1.0000; median -0.2000) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0000) UNDETERMINED; PNOFATE 4/7 (p 1.0000; median 0.2000) UNDETERMINED
- route same cos: PFATE 2/8 (p 0.2891; median -0.0510) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0856) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0159) UNDETERMINED
- route same acc_d_minus_r: PFATE 0/0 (p n/a; median n/a) UNDETERMINED; PYOKED 0/0 (p n/a; median n/a) UNDETERMINED; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route scramble act: PFATE 7/8 (p 0.0703; median 0.3993) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.5177) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0025) UNDETERMINED
- route scramble rescue: PFATE 5/8 (p 0.7266; median 0.0385) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0422) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0509) UNDETERMINED
- route scramble rescue_abs: PFATE 6/8 (p 0.2891; median 0.0031) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0046) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0000) UNDETERMINED
- route scramble gap: PFATE 8/8 (p 0.0078; median 1.3053) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 1.5550) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.6707) UNDETERMINED
- route scramble dose_rho: PFATE 7/8 (p 0.0703; median 1.0000) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 1.0000) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.4000) UNDETERMINED
- route scramble cos: PFATE 7/8 (p 0.0703; median 0.7899) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.8209) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0107) UNDETERMINED
- route scramble acc_d_minus_r: PFATE 3/8 (p 0.7266; median -0.0072) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0038) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0055) UNDETERMINED
- route noise act: PFATE 7/8 (p 0.0703; median 0.3870) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.5046) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0064) UNDETERMINED
- route noise rescue: PFATE 5/8 (p 0.7266; median 0.1298) UNDETERMINED; PYOKED 4/8 (p 1.0000; median -0.0274) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0120) UNDETERMINED
- route noise rescue_abs: PFATE 7/8 (p 0.0703; median 0.0039) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0008) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0000) UNDETERMINED
- route noise gap: PFATE 8/8 (p 0.0078; median 1.5296) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 1.6449) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 1.0671) UNDETERMINED
- route noise dose_rho: PFATE 7/8 (p 0.0703; median 1.0000) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 1.0000) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.8000) UNDETERMINED
- route noise cos: PFATE 7/8 (p 0.0703; median 0.7487) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.8154) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0408) UNDETERMINED
- route noise acc_d_minus_r: PFATE 5/8 (p 0.7266; median 0.0034) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0047) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0035) UNDETERMINED
- route zero act: PFATE 7/8 (p 0.0703; median 0.3452) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 0.4548) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0066) UNDETERMINED
- route zero rescue: PFATE 8/8 (p 0.0078; median 0.3226) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0823) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0126) UNDETERMINED
- route zero rescue_abs: PFATE 8/8 (p 0.0078; median 0.0159) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0089) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0000) UNDETERMINED
- route zero gap: PFATE 8/8 (p 0.0078; median 2.1481) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 2.1679) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 1.9395) UNDETERMINED
- route zero dose_rho: PFATE 7/8 (p 0.0703; median 1.0000) UNDETERMINED; PYOKED 7/7 (p 0.0156; median 1.0000) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.2000) UNDETERMINED
- route zero cos: PFATE 7/8 (p 0.0703; median 0.6896) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 0.7972) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median -0.0234) UNDETERMINED
- route zero acc_d_minus_r: PFATE 6/8 (p 0.2891; median 0.0046) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0021) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0009) UNDETERMINED

## P1l

**Overall: INVALID.** Valid: False (fitted seeds {'PFATE': 8, 'PYOKED': 8, 'PNOFATE': 8}, needed >= 20 for PFATE and PNOFATE; PFATE held-out AUC on the trained damage 0.790, needed >= 0.7). Seeds: 8. Point: 3600.

| measure | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| auc_donor | 0.7902 | 0.8713 | 0.6142 |
| auc_donor_vs_same | 0.7826 | 0.8665 | 0.5628 |
| auc_same | 0.5154 | 0.5184 | 0.5266 |
| auc_scramble | 0.7371 | 0.7806 | 0.5450 |
| auc_noise | 0.7688 | 0.8020 | 0.5521 |
| auc_zero | 0.7908 | 0.8089 | 0.5607 |
| auc_novel | 0.7658 | 0.7972 | 0.5510 |
| signed_rep | 0.3513 | 0.8286 | 0.0510 |
| induce_rep | 0.1655 | 0.3387 | 0.0363 |
| rescue_rep | 0.2985 | 0.6433 | 0.0109 |
| gap_rep | 2.4903 | 5.5690 | 0.0374 |
| induce_conf | 0.1277 | 0.1935 | -0.0053 |
| rescue_conf | -0.0159 | 0.0383 | 0.0091 |
| corr_d9 | 0.8638 | 0.9180 | 0.1843 |
| corr_c9 | 0.0029 | 0.0159 | -0.0153 |

## Tests

- P1L_1 general: mean AUC on the three novel damage types - 0.5, PFATE: 7/8 > 0 (sign p 0.0703, Holm 0.2109; median 0.2658) UNDETERMINED
- P1L_2 learned access: mean novel AUC, PFATE against PNOFATE: 6/8 (sign p 0.2891, Holm 0.2891; 0.7658 against 0.5510) UNDETERMINED
- P1L_3 shared variable: signed_rep (moving d moves the read-out), PFATE: 7/8 > 0 (sign p 0.0703, Holm 0.2109; median 0.3513) UNDETERMINED
- signed_rep_PFATE_vs_PNOFATE: 6/8 (sign p 0.2891, Holm n/a; 0.3513 against 0.0510) UNDETERMINED
- auc_novel_PFATE_vs_PYOKED: 4/8 (sign p 1.0000, Holm n/a; 0.7658 against 0.7972) UNDETERMINED
- auc_donor_PFATE_vs_PNOFATE: 6/8 (sign p 0.2891, Holm n/a; 0.7902 against 0.6142) UNDETERMINED
- auc_scramble_vs_same_PFATE: 6/8 (sign p 0.2891, Holm n/a; 0.7371 against 0.5154) UNDETERMINED
- route auc_donor (- 0.5): PFATE 7/8 (p 0.0703; median 0.2902) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 0.3713) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.1142) UNDETERMINED
- route auc_donor_vs_same (- 0.5): PFATE 8/8 (p 0.0078; median 0.2826) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.3665) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0628) UNDETERMINED
- route auc_same (- 0.5): PFATE 7/8 (p 0.0703; median 0.0154) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0184) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.0266) UNDETERMINED
- route auc_scramble (- 0.5): PFATE 7/8 (p 0.0703; median 0.2371) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.2806) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0450) UNDETERMINED
- route auc_noise (- 0.5): PFATE 7/8 (p 0.0703; median 0.2688) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.3020) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0521) UNDETERMINED
- route auc_zero (- 0.5): PFATE 7/8 (p 0.0703; median 0.2908) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.3089) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0607) UNDETERMINED
- route auc_novel (- 0.5): PFATE 7/8 (p 0.0703; median 0.2658) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.2972) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0510) UNDETERMINED
- route signed_rep: PFATE 7/8 (p 0.0703; median 0.3513) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.8286) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0510) UNDETERMINED
- route induce_rep: PFATE 6/8 (p 0.2891; median 0.1655) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.3387) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.0363) UNDETERMINED
- route rescue_rep: PFATE 6/8 (p 0.2891; median 0.2985) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 0.6433) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0109) UNDETERMINED
- route gap_rep: PFATE 7/8 (p 0.0703; median 2.4903) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 5.5690) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0374) UNDETERMINED
- route induce_conf: PFATE 5/8 (p 0.7266; median 0.1277) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.1935) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0053) UNDETERMINED
- route rescue_conf: PFATE 4/8 (p 1.0000; median -0.0159) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0383) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0091) UNDETERMINED
- route corr_d9: PFATE 8/8 (p 0.0078; median 0.8638) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 0.9180) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.1843) UNDETERMINED
- route corr_c9: PFATE 4/8 (p 1.0000; median 0.0029) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0159) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0153) UNDETERMINED

## P1m

**Overall: INVALID.** Valid: False (fitted seeds {'PFATE': 8, 'PYOKED': 8, 'PNOFATE': 8}, needed >= 20 for PFATE and PNOFATE). Content confound: False. Room (the supplied oracle adds value over the re-tuned lesioned agent, PFATE, median >= 0.005): False. Seeds: 8. Point: 3600. Payoff per probe trial: +1 correct, -4 wrong, 0 abstain.

## PFATE

| measure | donor | scramble | noise | zero |
| --- | --- | --- | --- | --- |
| dV_star | 0.0163 | 0.0324 | 0.0374 | -0.0040 |
| dV_used | 0.0714 | 0.0375 | 0.0191 | -0.0630 |
| room | 0.1039 | 0.0105 | 0.0205 | 0.0023 |
| dV_star_nat | 0.0025 | 0.0047 | 0.0082 | 0.0002 |
| dV_used_nat | 0.0154 | 0.0105 | 0.0075 | -0.0123 |
| room_nat | 0.0282 | 0.0041 | 0.0057 | 0.0030 |
| dV_star_strict | -0.0097 | 0.0679 | 0.0513 | 0.0061 |
| room_strict | 0.2797 | 0.0451 | 0.0411 | 0.0034 |
| vstar_intact | 0.6410 | 0.7493 | 0.7468 | 0.8457 |
| vstar_lesion | 0.6327 | 0.7069 | 0.7047 | 0.8437 |
| vstar_flag_lesion | 0.6819 | 0.7100 | 0.7142 | 0.8470 |
| vstar_oracle_lesion | 0.7320 | 0.7175 | 0.7344 | 0.8539 |
| recovery | 0.1519 | 2.5637 | 1.8077 | 5.1998 |
| used_intact | 0.5704 | 0.6620 | 0.6253 | 0.6990 |
| used_lesion | 0.5366 | 0.6198 | 0.6077 | 0.7153 |
| d_used_none | 0.0015 | 0.0015 | 0.0026 | 0.0019 |
| d_used_same | 0.0015 | n/a | n/a | n/a |
| d_used_dmg | 0.1963 | 0.0490 | 0.0155 | -0.0904 |
| d_acc_none | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| d_acc_dmg | -0.0197 | 0.0037 | -0.0012 | -0.0056 |
| acc_dmg_intact | 0.6950 | 0.8832 | 0.8883 | 0.9234 |

## PYOKED

| measure | donor | scramble | noise | zero |
| --- | --- | --- | --- | --- |
| dV_star | 0.0362 | 0.0189 | 0.0262 | 0.0084 |
| dV_used | 0.0836 | 0.0230 | -0.0042 | -0.0655 |
| room | 0.1343 | 0.0036 | 0.0002 | 0.0008 |
| dV_star_nat | 0.0073 | 0.0027 | 0.0035 | 0.0014 |
| dV_used_nat | 0.0161 | 0.0051 | -0.0015 | -0.0150 |
| room_nat | 0.0392 | 0.0029 | 0.0063 | 0.0002 |
| dV_star_strict | 0.0463 | 0.0158 | 0.0353 | 0.0142 |
| room_strict | 0.3405 | 0.0286 | 0.0329 | -0.0012 |
| vstar_intact | 0.6398 | 0.8022 | 0.7566 | 0.8837 |
| vstar_lesion | 0.5969 | 0.7736 | 0.7712 | 0.8604 |
| vstar_flag_lesion | 0.6909 | 0.7735 | 0.7754 | 0.8614 |
| vstar_oracle_lesion | 0.7373 | 0.7756 | 0.7699 | 0.8677 |
| recovery | 0.3016 | 1.9630 | 4.7454 | 7.9821 |
| used_intact | 0.5923 | 0.7595 | 0.6607 | 0.6753 |
| used_lesion | 0.5306 | 0.7242 | 0.6766 | 0.7259 |
| d_used_none | 0.0002 | 0.0003 | -0.0001 | 0.0002 |
| d_used_same | 0.0001 | n/a | n/a | n/a |
| d_used_dmg | 0.2189 | 0.0340 | 0.0031 | -0.1054 |
| d_acc_none | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| d_acc_dmg | 0.0174 | 0.0070 | 0.0031 | -0.0003 |
| acc_dmg_intact | 0.7247 | 0.9079 | 0.8951 | 0.8962 |

## PNOFATE

| measure | donor | scramble | noise | zero |
| --- | --- | --- | --- | --- |
| dV_star | 0.0056 | 0.0185 | 0.0124 | 0.0019 |
| dV_used | 0.0038 | -0.0039 | -0.0196 | -0.0261 |
| room | 0.2022 | 0.0258 | 0.0168 | 0.0067 |
| dV_star_nat | -0.0016 | 0.0042 | 0.0018 | 0.0009 |
| dV_used_nat | 0.0043 | 0.0012 | 0.0031 | -0.0068 |
| room_nat | 0.0444 | 0.0090 | 0.0107 | 0.0013 |
| dV_star_strict | -0.0284 | 0.0397 | 0.0446 | 0.0004 |
| room_strict | 0.4687 | 0.0852 | 0.0552 | 0.0038 |
| vstar_intact | 0.5212 | 0.6162 | 0.6693 | 0.7988 |
| vstar_lesion | 0.4980 | 0.6051 | 0.6685 | 0.8012 |
| vstar_flag_lesion | 0.6629 | 0.6137 | 0.6712 | 0.8006 |
| vstar_oracle_lesion | 0.7012 | 0.6309 | 0.6737 | 0.7937 |
| recovery | 0.0275 | 0.6438 | 1.0823 | 2.7666 |
| used_intact | 0.4862 | 0.5238 | 0.4853 | 0.5214 |
| used_lesion | 0.4803 | 0.5184 | 0.5046 | 0.5667 |
| d_used_none | 0.0008 | 0.0008 | 0.0012 | 0.0007 |
| d_used_same | 0.0008 | n/a | n/a | n/a |
| d_used_dmg | -0.0217 | -0.0124 | -0.0332 | -0.0515 |
| d_acc_none | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| d_acc_dmg | -0.0042 | -0.0037 | -0.0081 | -0.0191 |
| acc_dmg_intact | 0.6891 | 0.8573 | 0.8467 | 0.8469 |

## Tests

- P1M_1 value against the strongest simpler rival: V*(intact) - V*(lesion, re-tuned), PFATE: 5/8 > 0 (sign p 0.7266, Holm 1.0000; median 0.0163) UNDETERMINED
- P1M_2 value as used: own policy, intact - lesion, PFATE: 5/8 > 0 (sign p 0.7266, Holm 1.0000; median 0.0714) UNDETERMINED
- P1M_3 learned value: dV_star, PFATE against PNOFATE: 3/8 (sign p 0.7266, Holm 1.0000; 0.0163 against 0.0056) UNDETERMINED
- room: V*(lesion + supplied flag and K) - V*(lesion), PFATE: 8/8 > 0 (sign p 0.0078, Holm n/a; median 0.1039) UNDETERMINED
- content: accuracy on conflicts, intact - lesion, PFATE: 2/8 > 0 (sign p 0.2891, Holm n/a; median -0.0197) UNDETERMINED
- content: accuracy on undamaged trials, intact - lesion, PFATE: 2/2 > 0 (sign p 0.5000, Holm n/a; median 0.0077) UNDETERMINED
- dV_used_PFATE_vs_PNOFATE: 5/8 (sign p 0.7266, Holm n/a; 0.0714 against 0.0038) UNDETERMINED
- dV_star_PFATE_vs_PYOKED: 2/8 (sign p 0.2891, Holm n/a; 0.0163 against 0.0362) UNDETERMINED
- vstar_intact_PFATE_vs_PNOFATE: 5/8 (sign p 0.7266, Holm n/a; 0.6410 against 0.5212) UNDETERMINED
- route donor dV_star: PFATE 5/8 (p 0.7266; median 0.0163) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.0362) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0056) UNDETERMINED
- route donor dV_used: PFATE 5/8 (p 0.7266; median 0.0714) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.0836) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0038) UNDETERMINED
- route donor room: PFATE 8/8 (p 0.0078; median 0.1039) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 0.1343) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.2022) UNDETERMINED
- route donor dV_star_nat: PFATE 5/8 (p 0.7266; median 0.0025) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0073) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0016) UNDETERMINED
- route donor dV_used_nat: PFATE 7/8 (p 0.0703; median 0.0154) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.0161) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0043) UNDETERMINED
- route donor room_nat: PFATE 8/8 (p 0.0078; median 0.0282) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 0.0392) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.0444) UNDETERMINED
- route donor dV_star_strict: PFATE 4/8 (p 1.0000; median -0.0097) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.0463) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0284) UNDETERMINED
- route donor room_strict: PFATE 8/8 (p 0.0078; median 0.2797) UNDETERMINED; PYOKED 8/8 (p 0.0078; median 0.3405) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.4687) UNDETERMINED
- route donor recovery: PFATE 5/8 (p 0.7266; median 0.1519) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.3016) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0275) UNDETERMINED
- route donor d_used_none: PFATE 5/8 (p 0.7266; median 0.0015) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0002) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0008) UNDETERMINED
- route donor d_used_same: PFATE 5/8 (p 0.7266; median 0.0015) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0001) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.0008) UNDETERMINED
- route donor d_used_dmg: PFATE 5/8 (p 0.7266; median 0.1963) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.2189) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0217) UNDETERMINED
- route donor d_acc_none: PFATE 2/2 (p 0.5000; median 0.0077) UNDETERMINED; PYOKED 1/1 (p 1.0000; median 0.0236) UNDETERMINED; PNOFATE 2/2 (p 0.5000; median 0.0050) UNDETERMINED
- route donor d_acc_dmg: PFATE 2/8 (p 0.2891; median -0.0197) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.0174) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0042) UNDETERMINED
- route scramble dV_star: PFATE 8/8 (p 0.0078; median 0.0324) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0189) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0185) UNDETERMINED
- route scramble dV_used: PFATE 6/8 (p 0.2891; median 0.0375) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0230) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0039) UNDETERMINED
- route scramble room: PFATE 7/8 (p 0.0703; median 0.0105) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.0036) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0258) UNDETERMINED
- route scramble dV_star_nat: PFATE 8/8 (p 0.0078; median 0.0047) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0027) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0042) UNDETERMINED
- route scramble dV_used_nat: PFATE 7/8 (p 0.0703; median 0.0105) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0051) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0012) UNDETERMINED
- route scramble room_nat: PFATE 5/8 (p 0.7266; median 0.0041) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.0029) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0090) UNDETERMINED
- route scramble dV_star_strict: PFATE 8/8 (p 0.0078; median 0.0679) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0158) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0397) UNDETERMINED
- route scramble room_strict: PFATE 8/8 (p 0.0078; median 0.0451) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.0286) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.0852) UNDETERMINED
- route scramble recovery: PFATE 6/6 (p 0.0312; median 2.5637) UNDETERMINED; PYOKED 3/4 (p 0.6250; median 1.9630) UNDETERMINED; PNOFATE 4/6 (p 0.6875; median 0.6438) UNDETERMINED
- route scramble d_used_none: PFATE 6/8 (p 0.2891; median 0.0015) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0003) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.0008) UNDETERMINED
- route scramble d_used_same: PFATE 0/0 (p n/a; median n/a) UNDETERMINED; PYOKED 0/0 (p n/a; median n/a) UNDETERMINED; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route scramble d_used_dmg: PFATE 6/8 (p 0.2891; median 0.0490) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0340) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0124) UNDETERMINED
- route scramble d_acc_none: PFATE 2/2 (p 0.5000; median 0.0059) UNDETERMINED; PYOKED 1/1 (p 1.0000; median 0.0183) UNDETERMINED; PNOFATE 2/2 (p 0.5000; median 0.0045) UNDETERMINED
- route scramble d_acc_dmg: PFATE 5/8 (p 0.7266; median 0.0037) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0070) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0037) UNDETERMINED
- route noise dV_star: PFATE 6/8 (p 0.2891; median 0.0374) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0262) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0124) UNDETERMINED
- route noise dV_used: PFATE 5/8 (p 0.7266; median 0.0191) UNDETERMINED; PYOKED 4/8 (p 1.0000; median -0.0042) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0196) UNDETERMINED
- route noise room: PFATE 7/8 (p 0.0703; median 0.0205) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0002) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0168) UNDETERMINED
- route noise dV_star_nat: PFATE 6/8 (p 0.2891; median 0.0082) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0035) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0018) UNDETERMINED
- route noise dV_used_nat: PFATE 5/8 (p 0.7266; median 0.0075) UNDETERMINED; PYOKED 4/8 (p 1.0000; median -0.0015) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0031) UNDETERMINED
- route noise room_nat: PFATE 7/8 (p 0.0703; median 0.0057) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0063) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.0107) UNDETERMINED
- route noise dV_star_strict: PFATE 5/8 (p 0.7266; median 0.0513) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.0353) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0446) UNDETERMINED
- route noise room_strict: PFATE 7/8 (p 0.0703; median 0.0411) UNDETERMINED; PYOKED 7/8 (p 0.0703; median 0.0329) UNDETERMINED; PNOFATE 8/8 (p 0.0078; median 0.0552) UNDETERMINED
- route noise recovery: PFATE 5/6 (p 0.2188; median 1.8077) UNDETERMINED; PYOKED 2/2 (p 0.5000; median 4.7454) UNDETERMINED; PNOFATE 5/5 (p 0.0625; median 1.0823) UNDETERMINED
- route noise d_used_none: PFATE 6/8 (p 0.2891; median 0.0026) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0001) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0012) UNDETERMINED
- route noise d_used_same: PFATE 0/0 (p n/a; median n/a) UNDETERMINED; PYOKED 0/0 (p n/a; median n/a) UNDETERMINED; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route noise d_used_dmg: PFATE 4/8 (p 1.0000; median 0.0155) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0031) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0332) UNDETERMINED
- route noise d_acc_none: PFATE 2/2 (p 0.5000; median 0.0070) UNDETERMINED; PYOKED 1/1 (p 1.0000; median 0.0323) UNDETERMINED; PNOFATE 2/2 (p 0.5000; median 0.0097) UNDETERMINED
- route noise d_acc_dmg: PFATE 3/8 (p 0.7266; median -0.0012) UNDETERMINED; PYOKED 4/8 (p 1.0000; median 0.0031) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0081) UNDETERMINED
- route zero dV_star: PFATE 2/8 (p 0.2891; median -0.0040) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0084) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0019) UNDETERMINED
- route zero dV_used: PFATE 3/8 (p 0.7266; median -0.0630) UNDETERMINED; PYOKED 2/8 (p 0.2891; median -0.0655) UNDETERMINED; PNOFATE 2/8 (p 0.2891; median -0.0261) UNDETERMINED
- route zero room: PFATE 5/8 (p 0.7266; median 0.0023) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0008) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0067) UNDETERMINED
- route zero dV_star_nat: PFATE 5/8 (p 0.7266; median 0.0002) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0014) UNDETERMINED; PNOFATE 5/8 (p 0.7266; median 0.0009) UNDETERMINED
- route zero dV_used_nat: PFATE 3/8 (p 0.7266; median -0.0123) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0150) UNDETERMINED; PNOFATE 3/8 (p 0.7266; median -0.0068) UNDETERMINED
- route zero room_nat: PFATE 7/8 (p 0.0703; median 0.0030) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0002) UNDETERMINED; PNOFATE 6/8 (p 0.2891; median 0.0013) UNDETERMINED
- route zero dV_star_strict: PFATE 6/8 (p 0.2891; median 0.0061) UNDETERMINED; PYOKED 6/8 (p 0.2891; median 0.0142) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0004) UNDETERMINED
- route zero room_strict: PFATE 6/8 (p 0.2891; median 0.0034) UNDETERMINED; PYOKED 3/8 (p 0.7266; median -0.0012) UNDETERMINED; PNOFATE 4/8 (p 1.0000; median 0.0038) UNDETERMINED
- route zero recovery: PFATE 2/3 (p 1.0000; median 5.1998) UNDETERMINED; PYOKED 2/2 (p 0.5000; median 7.9821) UNDETERMINED; PNOFATE 4/5 (p 0.3750; median 2.7666) UNDETERMINED
- route zero d_used_none: PFATE 5/8 (p 0.7266; median 0.0019) UNDETERMINED; PYOKED 5/8 (p 0.7266; median 0.0002) UNDETERMINED; PNOFATE 7/8 (p 0.0703; median 0.0007) UNDETERMINED
- route zero d_used_same: PFATE 0/0 (p n/a; median n/a) UNDETERMINED; PYOKED 0/0 (p n/a; median n/a) UNDETERMINED; PNOFATE 0/0 (p n/a; median n/a) UNDETERMINED
- route zero d_used_dmg: PFATE 3/8 (p 0.7266; median -0.0904) UNDETERMINED; PYOKED 2/8 (p 0.2891; median -0.1054) UNDETERMINED; PNOFATE 1/8 (p 0.0703; median -0.0515) UNDETERMINED
- route zero d_acc_none: PFATE 3/3 (p 0.2500; median 0.0051) UNDETERMINED; PYOKED 1/1 (p 1.0000; median 0.0155) UNDETERMINED; PNOFATE 2/2 (p 0.5000; median 0.0058) UNDETERMINED
- route zero d_acc_dmg: PFATE 3/8 (p 0.7266; median -0.0056) UNDETERMINED; PYOKED 4/8 (p 1.0000; median -0.0003) UNDETERMINED; PNOFATE 1/8 (p 0.0703; median -0.0191) UNDETERMINED
